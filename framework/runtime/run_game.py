#!/usr/bin/env python3
"""
run_game.py — DRIVER ponta-a-ponta: roda TODOS os capitulos/cenas de um projeto em sequencia.

Elimina o "invocar run_chapter cap-a-cap manualmente". Descobre a estrutura do projeto sozinho:
  - modo CAPITULADO (ch_<N>_*): 1 chamada de run_chapter POR capitulo, na ordem numerica.
  - modo FLAT (sem ch_*, ex.: Souldiers): 1 UNICA chamada de run_chapter com --scenes-glob
    (rotulo sintetico "full", mesma convencao ja usada em producao pro Souldiers).

`--max-usd` aqui e um TETO GLOBAL (projeto inteiro), nao por capitulo: a cada unidade, encolhe o
teto repassado pro `run_chapter` com o que sobrou (`cost_report.report` ja soma o projeto inteiro) --
NAO rateia entre capitulos, so aborta quando o teto global estourar, seja qual for a unidade.

Retomada automatica: ZERO estado novo. `run_chapter`/`run_scene` ja pulam cena `verified` via
`run_state.json`; rodar `run_game` de novo apos uma parada e IDENTICO a rodar pela 1a vez (a unidade
ja completa retorna quase instantaneo, sem nova chamada de API).

Uso:  python run_game.py <projeto> [--backend api|in-session] [--no-batch] [--max-usd N]
                        [--scenes-glob G] [--skip-kb-gate] [--require-back]
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import cost_report  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
import progress_report  # noqa: E402
import run_chapter  # noqa: E402

_CHAP_RE = re.compile(r"ch_(\d+)_")


def _discover_chapters(root: Path) -> list[str]:
    """Prefixos numericos de capitulo via ch_<N>_*/dialogs.csv. [] se o projeto for flat (sem essa
    convencao — ex.: Souldiers), sinalizando o modo FLAT pro caller."""
    art = paths.artifacts(root)
    nums = {m.group(1) for p in (art / "scenes").glob("ch_*_*/dialogs.csv")
           if (m := _CHAP_RE.match(p.parent.name))}
    return sorted(nums, key=int)


def _all_scenes(root: Path, chapters: list[str], scenes_glob: str | None) -> list[str]:
    """TODAS as cenas do jogo (p/ progress_report) — reusa a MESMA discovery do run_chapter, nao
    duplica a logica de glob."""
    if chapters:
        out: list[str] = []
        for c in chapters:
            out += run_chapter._scenes_of(root, c)
        return out
    return run_chapter._scenes_of_glob(root, scenes_glob or "*")


def run_game(root, *, backend="api", batch=True, max_usd=None, scenes_glob=None,
            skip_kb_gate=False, require_back=False, skip_connector_gate=False,
            started_at=None) -> dict:
    root = Path(root)
    chapters = _discover_chapters(root)
    units = chapters if chapters else ["full"]           # rotulo sintetico do modo flat
    all_scenes = _all_scenes(root, chapters, scenes_glob)
    print(f"run_game: {len(units)} {'capitulo(s)' if chapters else 'unidade (modo flat)'}, "
          f"{len(all_scenes)} cena(s) no total"
          + (f" | teto GLOBAL: ${max_usd:.2f}" if max_usd is not None else ""))

    results = []
    for unit in units:
        if max_usd is not None:
            spent = cost_report.report(root).get("total_usd", 0.0)
            remaining = max_usd - spent
            if remaining <= 0:
                print(f"\nABORTADO por teto GLOBAL de gasto: projeto ja custou ${spent:.2f} >= "
                      f"--max-usd ${max_usd:.2f} (parado ANTES de {unit}; rode de novo apos recarga).")
                return {"chapters": results, "status": "stopped_budget", "stopped_at": unit}
        else:
            remaining = None
        chap_label = unit if chapters else "full"
        chap_glob = None if chapters else (scenes_glob or "*")
        r = run_chapter.run_chapter(root, chap_label, backend=backend, batch=batch,
                                    max_usd=remaining, scenes_glob=chap_glob,
                                    skip_kb_gate=skip_kb_gate, require_back=require_back,
                                    skip_connector_gate=skip_connector_gate)
        results.append(r)
        elapsed = (time.time() - started_at) if started_at is not None else None
        prog = progress_report.report(root, all_scenes, elapsed_s=elapsed)
        print(f"[progresso] {progress_report.format_line(prog)}")
        if r["status"] not in ("complete", "empty"):
            print(f"\nPAROU em {chap_label}: status = {r['status']} "
                  f"(corrija e rode de novo; run_game retoma sozinho de onde parou).")
            return {"chapters": results, "status": r["status"], "stopped_at": chap_label}
    print(f"\nOK run_game: {len(units)} {'capitulo(s)' if chapters else 'unidade'} completa(s).")
    return {"chapters": results, "status": "complete"}


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Driver ponta-a-ponta: roda o jogo inteiro em sequencia.")
    ap.add_argument("project")
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--no-batch", dest="batch", action="store_false",
                    help="desliga o modo batch (default: ligado)")
    ap.set_defaults(batch=True)
    ap.add_argument("--max-usd", type=float, default=None,
                    help="teto de gasto GLOBAL (projeto inteiro, nao por capitulo)")
    ap.add_argument("--scenes-glob", default=None,
                    help="glob(s) p/ projetos flat (ex.: Souldiers); ignorado em projetos capitulados")
    ap.add_argument("--skip-kb-gate", action="store_true")
    ap.add_argument("--skip-connector-gate", action="store_true",
                    help="ignora o gate de completude de conector (nao recomendado)")
    ap.add_argument("--require-back", action="store_true")
    a = ap.parse_args()
    r = run_game(a.project, backend=a.backend, batch=a.batch, max_usd=a.max_usd,
                scenes_glob=a.scenes_glob, skip_kb_gate=a.skip_kb_gate,
                require_back=a.require_back, skip_connector_gate=a.skip_connector_gate,
                started_at=time.time())
    sys.exit(0 if r["status"] == "complete" else 1)


if __name__ == "__main__":
    main()
