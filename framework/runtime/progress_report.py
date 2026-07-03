#!/usr/bin/env python3
"""
progress_report.py — observabilidade de progresso do JOGO INTEIRO (P2.5): % concluido, linhas/min,
ETA, taxa de falha. Complementa `cost_report.py` (que so mede GASTO); aqui a metrica e COBERTURA
do corpus (linhas verified vs. total), independente de custo.

Puro/deterministico: NAO chama time.time() nem datetime.now() internamente -- `elapsed_s` (se usado
p/ linhas/min e ETA) e passado pelo caller (`run_game.py` captura o tempo real fora daqui). Sem isso,
o modulo nao seria testavel sem monkeypatch de tempo.

Uso:  python progress_report.py <projeto> [--scenes-glob G]   (todas as cenas do projeto; --scenes-glob
      filtra como no run_chapter, senao descobre TODAS as ch_*/dialogs.csv)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
from run_chapter import (
    _count_lines,  # noqa: E402  (reusa a mesma contagem de linhas do run_chapter)
)


def _scene_statuses(root: Path) -> dict:
    p = paths.run_state(root)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8")).get("scenes", {})


def report(root, scenes, *, elapsed_s: float | None = None) -> dict:
    """Progresso do JOGO (dado o conjunto `scenes` que compoe o jogo inteiro -- run_game.py descobre
    isso, este modulo so mede). Retorna {scenes_total, scenes_verified, lines_total, lines_verified,
    pct_done, failure_rate} + {lines_per_min, eta_s} SE `elapsed_s` for passado (>0)."""
    root = Path(root)
    statuses = _scene_statuses(root)
    verified_scenes = [s for s in scenes
                       if statuses.get(s, {}).get("status") == "verified" and statuses.get(s, {}).get("verified")]
    attempted = [s for s in scenes if s in statuses]
    failed = [s for s in attempted if statuses[s].get("status") not in ("verified", "planned")]

    lines_total = _count_lines(root, scenes)
    lines_verified = _count_lines(root, verified_scenes)

    out = {
        "scenes_total": len(scenes), "scenes_verified": len(verified_scenes),
        "lines_total": lines_total, "lines_verified": lines_verified,
        "pct_done": round(100 * lines_verified / lines_total, 1) if lines_total else 0.0,
        "failure_rate": round(len(failed) / len(attempted), 3) if attempted else 0.0,
    }
    if elapsed_s is not None and elapsed_s > 0 and lines_verified > 0:
        lines_per_min = lines_verified / (elapsed_s / 60)
        out["lines_per_min"] = round(lines_per_min, 2)
        remaining = max(0, lines_total - lines_verified)
        out["eta_s"] = round(remaining / lines_per_min * 60, 1) if lines_per_min > 0 else None
    return out


def format_line(rep: dict) -> str:
    """1 linha de resumo legivel — impressa pelo run_game.py apos cada capitulo/unidade."""
    parts = [f"{rep['scenes_verified']}/{rep['scenes_total']} cena(s)",
             f"{rep['pct_done']}% do jogo ({rep['lines_verified']}/{rep['lines_total']} linhas)",
             f"falha={rep['failure_rate'] * 100:.1f}%"]
    if "lines_per_min" in rep:
        parts.append(f"{rep['lines_per_min']} linhas/min")
        if rep.get("eta_s") is not None:
            parts.append(f"ETA ~{rep['eta_s'] / 60:.0f}min")
    return " | ".join(parts)


def main():
    import argparse

    import run_chapter
    ap = argparse.ArgumentParser(description="Progresso do jogo inteiro (cobertura, nao custo).")
    ap.add_argument("project")
    ap.add_argument("--scenes-glob", default=None,
                    help="glob(s) customizados (projeto flat); senao descobre todas as ch_<N>_*")
    a = ap.parse_args()
    root = Path(a.project)
    if a.scenes_glob:
        scenes = run_chapter._scenes_of_glob(root, a.scenes_glob)
    else:
        art = paths.artifacts(root)
        scenes = sorted({p.parent.name for p in (art / "scenes").glob("*/dialogs.csv")})
    rep = report(root, scenes)
    print(format_line(rep))


if __name__ == "__main__":
    main()
