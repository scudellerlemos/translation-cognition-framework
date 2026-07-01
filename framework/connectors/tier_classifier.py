"""
tier_classifier.py — classifica um diretório de jogo em T1/T2/T3.

T1: engine conhecida no registry → conector reutilizável direto (sem LLM).
T2: engine desconhecida, mas texto legível → LLM gera candidato de conector.
T3: cifrado/ofuscado → requer engenharia reversa (fora do escopo do framework).

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

# Entropia acima deste limiar indica cifrado/comprimido → T3
_ENTROPY_BLOCKED = 7.0
# Densidade de string abaixo deste limiar indica dados sem texto legível → T3
_DENSITY_BLOCKED = 0.05
# Limiar mínimo de score para classificar como T1 (0.0–1.0)
_T1_MIN_SCORE = 0.5


def classify(evidence: dict, registry: list[dict]) -> dict:
    """Classifica as evidências e retorna o tier + detalhes de decisão.

    Retorna:
      tier       : "T1" | "T2" | "T3"
      engine_id  : str | None  (T1: id do engine; T2/T3: None)
      confidence : float 0.0–1.0
      reasons    : list[str]
      blocked    : bool  (T3 por entropia alta)
    """
    # T3-bloqueado: cifrado/comprimido detectado antes de qualquer match
    if _is_blocked(evidence):
        return {
            "tier": "T3",
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

    if best_engine and best_score >= _T1_MIN_SCORE:
        return {
            "tier": "T1",
            "engine_id": best_engine["id"],
            "confidence": round(best_score, 3),
            "reasons": best_reasons,
            "blocked": False,
        }

    # T2: texto legível mas engine desconhecida
    t2_reasons = ["engine não encontrada no registry"]
    if evidence.get("string_density", 0) > _DENSITY_BLOCKED:
        t2_reasons.append(
            f"densidade de texto {evidence['string_density']:.2f} indica dados legíveis"
        )
    return {
        "tier": "T2",
        "engine_id": None,
        "confidence": round(1.0 - best_score, 3),
        "reasons": t2_reasons,
        "blocked": False,
    }


def _is_blocked(evidence: dict) -> bool:
    """T3-bloqueado: entropia muito alta (cifrado) OU densidade de string muito baixa."""
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


def load_registry(registry_path: Path | None = None) -> list[dict]:
    """Carrega o registry JSON. Padrão: connector_registry.json no mesmo diretório."""
    if registry_path is None:
        registry_path = Path(__file__).resolve().parent / "connector_registry.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    return data.get("engines", [])
