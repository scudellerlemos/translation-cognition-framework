"""
tier_classifier.py — classifica um diretório de jogo pela dificuldade de descoberta de engine.

known_engine: engine conhecida no registry → conector reutilizável direto (sem LLM).
unknown_engine: engine desconhecida, mas texto legível → LLM gera candidato de conector.
blocked: cifrado/ofuscado → requer engenharia reversa (fora do escopo do framework).

Sem dependências externas. Determinístico.

Uso:
    from tier_classifier import classify
    registry = json.loads(Path("connector_registry.json").read_text())["engines"]
    result = classify(evidence, registry)
"""
from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path

# Entropia acima deste limiar indica cifrado/comprimido → blocked
_ENTROPY_BLOCKED = 7.0
# Densidade de string abaixo deste limiar indica dados sem texto legível → blocked
_DENSITY_BLOCKED = 0.05
# Limiar mínimo de score para classificar como known_engine (0.0–1.0)
_KNOWN_ENGINE_MIN_SCORE = 0.5


def classify(evidence: dict, registry: list[dict]) -> dict:
    """Classifica as evidências e retorna o tier + detalhes de decisão.

    Retorna:
      tier       : "known_engine" | "unknown_engine" | "blocked"
      engine_id  : str | None  (known_engine: id do engine; demais: None)
      confidence : float 0.0–1.0
      reasons    : list[str]
      blocked    : bool  (tier "blocked" por entropia alta)
    """
    # bloqueado: cifrado/comprimido detectado antes de qualquer match
    if _is_blocked(evidence):
        return {
            "tier": "blocked",
            "engine_id": None,
            "confidence": 1.0,
            "reasons": [
                f"entropia média {evidence.get('entropy_mean', 0):.2f} > {_ENTROPY_BLOCKED} "
                "(dados cifrados ou comprimidos — requer engenharia reversa)",
            ],
            "blocked": True,
        }

    best_engine = None
    best_score = 0.0
    best_reasons: list[str] = []

    for engine in registry:
        score, reasons = _score_engine(evidence, engine)
        if score > best_score:
            best_score = score
            best_engine = engine
            best_reasons = reasons

    if best_engine and best_score >= _KNOWN_ENGINE_MIN_SCORE:
        return {
            "tier": "known_engine",
            "engine_id": best_engine["id"],
            "confidence": round(best_score, 3),
            "reasons": best_reasons,
            "blocked": False,
        }

    # engine desconhecida: texto legível mas não encontrado no registry
    unknown_reasons = ["engine não encontrada no registry"]
    if evidence.get("string_density", 0) > _DENSITY_BLOCKED:
        unknown_reasons.append(
            f"densidade de texto {evidence['string_density']:.2f} indica dados legíveis"
        )
    return {
        "tier": "unknown_engine",
        "engine_id": None,
        "confidence": round(1.0 - best_score, 3),
        "reasons": unknown_reasons,
        "blocked": False,
    }


def _is_blocked(evidence: dict) -> bool:
    """Tier bloqueado: entropia muito alta (cifrado) OU densidade de string muito baixa."""
    entropy = evidence.get("entropy_mean", 0.0)
    density = evidence.get("string_density", 1.0)
    return entropy > _ENTROPY_BLOCKED or (density < _DENSITY_BLOCKED and entropy > 5.0)


def _score_engine(evidence: dict, engine: dict) -> tuple[float, list[str]]:
    """Calcula score de 0.0–1.0 para um engine do registry vs evidências.

    Pesos:
      file_patterns    0.50 — famílias de arquivo
      magic_bytes      0.30 — magic bytes exatos
      encoding         0.10 — encoding esperado
      control_tokens   0.10 — padrão de tokens de controle
    """
    sig = engine.get("signatures", {})
    score = 0.0
    reasons: list[str] = []

    # --- file_patterns (peso 0.50) ---
    patterns = sig.get("file_patterns") or []
    families = evidence.get("families", {})
    matched_patterns = []
    matched_count = 0
    for pat in patterns:
        for fam, count in families.items():
            if fnmatch.fnmatch(fam, pat.upper()):
                matched_patterns.append(f"{fam} ({count} arquivos)")
                matched_count += count
    if matched_patterns:
        min_count = sig.get("min_file_count", 1)
        pattern_score = min(1.0, matched_count / max(min_count, 1)) * 0.50
        score += pattern_score
        reasons.append(f"file_patterns: {', '.join(matched_patterns[:3])}")

    # --- magic_bytes (peso 0.30) ---
    expected_magic = (sig.get("magic_bytes") or "").lower()
    if expected_magic:
        all_magics = {m.lower() for m in evidence.get("magic_bytes", {})}
        for found_magic in all_magics:
            if found_magic.startswith(expected_magic) or expected_magic.startswith(found_magic):
                score += 0.30
                reasons.append(f"magic_bytes: {found_magic[:16]}")
                break

    # --- encoding (peso 0.10) ---
    expected_enc = (sig.get("encoding") or "").lower()
    if expected_enc:
        sample_encs = evidence.get("sample_encodings", {})
        enc_score = sample_encs.get(expected_enc, 0.0)
        score += enc_score * 0.10
        if enc_score > 0.5:
            reasons.append(f"encoding {expected_enc}: {enc_score:.0%}")

    # --- control_tokens (peso 0.10) ---
    expected_pattern = sig.get("control_token_pattern")
    if expected_pattern and evidence.get("has_control_tokens"):
        score += 0.10
        reasons.append("tokens de controle detectados")
    elif not expected_pattern:
        score += 0.05  # engine que não usa tokens de controle: bônus parcial se ausentes

    return score, reasons


def existence_gate(evidence: dict, registry: list[dict]) -> dict:
    """Gate de existencia: formaliza (testavel, reusavel por qualquer caller) o que discover.py
    ja fazia implicitamente via if/elif (so chama script_generator.generate() no branch de engine
    desconhecida). Retorna {**classify(...), must_generate, reference_connector}.

    must_generate=True SOMENTE quando tier == unknown_engine -- e o UNICO caso onde gerar
    candidato via LLM e permitido. known_engine (engine ja no registry) aponta direto pro conector
    de referencia, NUNCA aciona o gerador; blocked (cifrado/comprimido) tambem nunca aciona. Isso
    remove a possibilidade ESTRUTURAL de chamar o LLM p/ gerar um candidato quando ja existe um
    conector de referencia pronto ou quando e logicamente impossivel."""
    result = classify(evidence, registry)
    reference_connector = None
    if result["tier"] == "known_engine":
        engine = next((e for e in registry if e["id"] == result["engine_id"]), {})
        reference_connector = engine.get("reference_connector")
    return {**result, "must_generate": result["tier"] == "unknown_engine",
            "reference_connector": reference_connector}


def load_registry(registry_path: Path | None = None) -> list[dict]:
    """Carrega o registry JSON. Padrão: connector_registry.json no mesmo diretório."""
    if registry_path is None:
        registry_path = Path(__file__).resolve().parent / "connector_registry.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    return data.get("engines", [])
