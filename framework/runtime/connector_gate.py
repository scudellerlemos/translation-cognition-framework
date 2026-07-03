#!/usr/bin/env python3
"""
connector_gate.py — GATE DE COMPLETUDE DE CONECTOR (D6, espelha kb_gate.py).

Descoberto no onboarding do Souldiers (2026-07-02): `project.json` declarava "Fase 0 concluida" com
so `extract.py`/`reinsert.py` prontos -- `build_plan_chapter.py`/`verify_chapter.py` nunca existiram,
ou seja, round-trip NUNCA tinha sido validado de verdade. Mesma classe de bug do gap de KB: "fase
declarada concluida" sem nenhum gate automatico checando o conjunto completo de artefatos antes do
primeiro gasto real em traducao.

Checagens (deterministas, sem rede):
  HARD (bloqueiam sempre, nao bypassavel):
    - build_plan_script E verify_script (via connector_mgr, resolve overrides de project.json)
      existem no disco. Sem eles, nenhum round-trip e fisicamente possivel.
  problems (bloqueiam salvo --skip-connector-gate):
    - nenhuma cena do projeto tem verified=True em run_state.json -- round-trip nunca rodou verde
      nem uma vez. Reusa o `run_state.json` que ja existe (connector_mgr grava `connector_hash` la
      a cada verify bem-sucedido) -- nao precisa de manifest/timestamp novo.
  warnings (nunca bloqueiam):
    - connector/test_roundtrip.py ausente -- dev-only (pytest), nao e chamado pelo runtime.

connector_gate roda ANTES do kb_gate (em run_scene.py e run_chapter.py): sem conector completo, uma
KB reconciliada nao serve de nada (nao ha como traduzir/validar nada de verdade).

Uso (CLI):  python connector_gate.py <projeto>
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
from connector_mgr import (
    _connector_script,  # noqa: E402  (mesmo resolvedor de path que run_scene usa)
)


class StaleReadError(RuntimeError):
    """D5 — gate de leitura completa: o conteudo alegado como lido nao bate com o disco AGORA."""

_SCRIPTS = (("build_plan_script", "build_plan_chapter.py"), ("verify_script", "verify_chapter.py"))


def _has_green_roundtrip(root: Path) -> bool:
    """True se ALGUMA cena do projeto ja tem verified=True em run_state.json -- reusa o estado que
    connector_mgr/run_scene ja gravam a cada verify bem-sucedido (connector_hash + verified)."""
    rs = paths.run_state(root)
    if not rs.is_file():
        return False
    try:
        scenes = json.loads(rs.read_text(encoding="utf-8")).get("scenes", {})
    except (json.JSONDecodeError, OSError):
        return False
    return any(v.get("verified") is True for v in scenes.values())


def check(root) -> dict:
    """Retorna {hard_problems: [...], problems: [...], warnings: [...]}. Nao depende de cena (a
    completude de conector e uma propriedade do PROJETO, nao de uma cena especifica)."""
    root = Path(root)
    cfg_path = root / "project.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    hard_problems: list[str] = []
    for key, default in _SCRIPTS:
        p = _connector_script(root, cfg, key, default)
        if not p.is_file():
            hard_problems.append(
                f"{key} ausente ({p}) — sem ele nenhum round-trip e possivel. Este gate nao pode ser pulado."
            )
    problems: list[str] = []
    if not hard_problems and not _has_green_roundtrip(root):
        problems.append(
            "nenhuma cena com round-trip verde registrado (run_state.json) — rode build_plan+verify "
            "de ao menos 1 cena antes de traduzir em escala, ou use --skip-connector-gate (nao recomendado)."
        )
    warnings: list[str] = []
    if not (root / "connector" / "test_roundtrip.py").is_file():
        warnings.append(
            "connector/test_roundtrip.py ausente — round-trip nunca validado via teste automatizado "
            "(dev-only, nao bloqueia o runtime)."
        )
    return {"hard_problems": hard_problems, "problems": problems, "warnings": warnings}


def assert_fresh_read(script_path, claimed_content: str) -> None:
    """D5 — gate de LEITURA COMPLETA: antes de editar um conector existente, o caller PRECISA ter
    lido o arquivo por inteiro AGORA (nao de memoria antiga). Interpretacao operacional escolhida
    (a mais codificavel/testavel de provar programaticamente): o caller passa o CONTEUDO INTEIRO
    que alega ter lido (nao um path) -- a unica forma de produzir isso e te-lo lido de verdade. O
    gate compara o hash do conteudo alegado contra o hash do arquivo NO DISCO agora; diverge =
    ou o arquivo mudou desde a leitura, ou o conteudo nunca foi lido de verdade (alucinado/stale).
    Levanta StaleReadError (nunca retorna False silenciosamente) -- forca o caller a lidar com isso."""
    script_path = Path(script_path)
    if not script_path.is_file():
        raise StaleReadError(f"{script_path} nao existe — nada para validar leitura")
    actual = hashlib.sha1(script_path.read_bytes(), usedforsecurity=False).hexdigest()
    claimed = hashlib.sha1(claimed_content.encode("utf-8"), usedforsecurity=False).hexdigest()
    if actual != claimed:
        raise StaleReadError(
            f"{script_path}: conteudo alegado nao bate com o disco agora — releia antes de editar"
        )


def main():
    ap_project = sys.argv[1] if len(sys.argv) > 1 else None
    if not ap_project:
        print("uso: python connector_gate.py <projeto>")
        sys.exit(2)
    r = check(ap_project)
    for w in r["warnings"]:
        print(f"[warn] {w}")
    for p in r["hard_problems"]:
        print(f"[HARD-BLOCK] {p}")
    for p in r["problems"]:
        print(f"[BLOCK] {p}")
    all_problems = r["hard_problems"] + r["problems"]
    print("\nOK: conector completo." if not all_problems else
          f"\nBLOQUEADO: {len(all_problems)} problema(s) de completude de conector.")
    sys.exit(1 if all_problems else 0)


if __name__ == "__main__":
    main()
