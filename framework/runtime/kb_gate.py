#!/usr/bin/env python3
"""
kb_gate.py — GATE DE COBERTURA DE CONHECIMENTO (cabeia a doutrina no runtime).

A doutrina (skills 01-04 + invariante #9 do _index) exige KB reconciliada ANTES de traduzir. O harness
de escala consumia os artefatos sem exigir isso -> arco novo podia ser traduzido "as cegas". Este gate
fecha a lacuna: o run_scene chama check() ANTES de traduzir e bloqueia se a cobertura falhar.

Checagens (deterministas, sem rede):
  HARD (bloqueiam):
    - research_log.md existe e tem `status: reconciled` (pesquisa IA+humano conciliada).
    - artefatos de KB presentes e nao-vazios: glossary.csv, universe_knowledge_base.md, voice_cards.json.
  FRONTEIRA (bloqueia se declarada): project.json `kb_frontier` = sfx max coberto pela pesquisa
    (ex.: "12_17"). Cena alem disso -> a KB nao cobre este ponto narrativo -> rode a Fase 0 ate aqui.
    Se `kb_frontier` nao for declarado, a fronteira do research_log e so REPORTADA (warning), nao bloqueia.

Uso (CLI):  python kb_gate.py <projeto> <scene>
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402

_KB_ARTIFACTS = ("glossary.csv", "universe_knowledge_base.md")


def _pos(sfx: str):
    """sfx '12_03' -> (12, 3) p/ comparacao numerica robusta (evita pegadinha lexicografica 9 vs 12)."""
    return tuple(int(p) for p in str(sfx).split("_") if p.isdigit())


def check(root, scene) -> dict:
    """Retorna {problems: [...], warnings: [...]}. problems != [] => bloquear traducao."""
    root = Path(root)
    art = root / "artifacts"
    problems, warnings = [], []

    rl = art / "research_log.md"
    if not rl.is_file():
        problems.append("research_log.md ausente — rode a Fase 0 (skill 03, pesquisa IA+humano).")
    else:
        txt = rl.read_text(encoding="utf-8")
        # tolera markdown: "**Status:** reconciled", "status : reconciled", etc.
        if not re.search(r"status[:*\s]+reconciled", txt, re.I):
            problems.append("research_log.md sem 'status: reconciled' — reconcilie a pesquisa IA+humano.")

    for name in _KB_ARTIFACTS:
        f = art / name
        if not f.is_file() or not f.read_text(encoding="utf-8").strip():
            problems.append(f"{name} ausente/vazio — KB incompleta (skills 03/04).")
    vc = art / "state" / "voice_cards.json"
    if not vc.is_file() or not vc.read_text(encoding="utf-8").strip():
        problems.append("voice_cards.json ausente — rode state_index (deriva do tone_analysis.md).")

    # fronteira: declarada em project.json (machine-readable) tem prioridade; senao, so reporta a do log
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    frontier = cfg.get("kb_frontier")
    sfx = context_pack.sfx_of(scene)
    if frontier:
        if _pos(sfx) > _pos(frontier):
            problems.append(f"cena {sfx} ALEM da fronteira de KB pesquisada (kb_frontier={frontier}) — "
                            f"estenda a Fase 0 ate aqui antes de traduzir.")
    elif rl.is_file():
        m = re.search(r"Fronteira de spoiler:\s*(.+)", rl.read_text(encoding="utf-8"))
        fr = m.group(1).strip() if m else "(nao declarada)"
        warnings.append(f"kb_frontier nao declarada em project.json; research_log diz: \"{fr[:120]}\". "
                        f"Sem fronteira machine-readable, o gate NAO bloqueia por posicao de cena.")
    return {"problems": problems, "warnings": warnings}


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Gate de cobertura de KB (pre-traducao).")
    ap.add_argument("project")
    ap.add_argument("scene")
    a = ap.parse_args()
    r = check(a.project, a.scene)
    for w in r["warnings"]:
        print(f"[warn] {w}")
    for p in r["problems"]:
        print(f"[BLOCK] {p}")
    print("OK: cobertura de KB suficiente." if not r["problems"] else
          f"\nBLOQUEADO: {len(r['problems'])} problema(s) de cobertura.")
    sys.exit(1 if r["problems"] else 0)


if __name__ == "__main__":
    main()
