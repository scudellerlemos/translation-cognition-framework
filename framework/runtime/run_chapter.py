#!/usr/bin/env python3
"""
run_chapter.py — DRIVER de capitulo (tira o loop de cenas do chat).

Roda todas as cenas de um capitulo como jobs stateless, em sequencia, via run_scene. Cada cena e uma
requisicao isolada (backend api -> 1 chamada HTTP por cena); o chat so LANCA este driver e LE o resumo,
entao o footprint de sessao e constante, independente do nº de cenas/capitulos.

Propriedades:
  - RESUMIVEL: pula cenas ja `verified` em run_state.json (a menos de --redo).
  - PARA NA 1ª FALHA: build_plan/verify/api falhou -> interrompe e reporta (nao mascara erro).
  - Determinista: descobre as cenas por glob de artifacts/ch_<cap>_*/dialogs.csv (ordem por sfx).
  - Reusa run_scene + state_index; nada de logica de IA aqui.

Uso:  python run_chapter.py <projeto> <cap> [--backend api|in-session] [--require-back] [--redo] [--no-verify]
      <cap> = "12" roda ch_12_01, ch_12_02, ... na ordem.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack   # noqa: E402
import run_scene as RS  # noqa: E402

_OK = ("verified", "planned")          # estados que permitem seguir p/ a proxima cena
_DONE = ("verified",)                  # estados que contam como "ja feito" (skip em modo resumivel)


def _scenes_of(root: Path, chap: str) -> list[str]:
    art = root / "artifacts"
    names = [p.parent.name for p in art.glob(f"ch_{chap}_*/dialogs.csv")]
    return sorted(set(names), key=context_pack.sfx_of)


def _verified(root: Path, scene: str) -> bool:
    p = root / "artifacts" / "run_state.json"
    if not p.is_file():
        return False
    st = json.loads(p.read_text(encoding="utf-8")).get("scenes", {}).get(scene, {})
    return st.get("status") in _DONE and st.get("verified") is True


def run_chapter(root, chap, *, backend="api", require_back=False, redo=False, do_verify=True):
    root = Path(root)
    scenes = _scenes_of(root, chap)
    if not scenes:
        print(f"nenhuma cena encontrada p/ cap {chap} (esperado artifacts/ch_{chap}_*/dialogs.csv)")
        return {"chapter": chap, "scenes": [], "status": "empty"}
    print(f"capitulo {chap}: {len(scenes)} cena(s) -> {', '.join(scenes)}")
    results = []
    for scene in scenes:
        if not redo and _verified(root, scene):
            print(f"[skip] {scene} ja verified")
            results.append({"scene": scene, "status": "skipped"})
            continue
        print(f"\n=== {scene} ({backend}) ===")
        r = RS.run_scene(root, scene, backend=backend, require_back=require_back, do_verify=do_verify)
        results.append({"scene": scene, "status": r["status"]})
        if r["status"] not in _OK:
            print(f"\nPAROU em {scene}: status = {r['status']} "
                  f"(corrija e rode de novo; cenas verified serao puladas)")
            return {"chapter": chap, "scenes": results, "status": "stopped", "stopped_at": scene}
    done = sum(1 for x in results if x["status"] in ("verified", "skipped"))
    print(f"\nOK capitulo {chap}: {done}/{len(scenes)} cena(s) prontas.")
    return {"chapter": chap, "scenes": results, "status": "complete"}


def main():
    ap = argparse.ArgumentParser(description="Driver determinista de capitulo (loop de cenas).")
    ap.add_argument("project")
    ap.add_argument("chapter", help='prefixo do capitulo, ex.: "12"')
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true")
    ap.add_argument("--redo", action="store_true", help="reprocessa mesmo cenas ja verified")
    ap.add_argument("--no-verify", action="store_true")
    a = ap.parse_args()
    r = run_chapter(a.project, a.chapter, backend=a.backend, require_back=a.require_back,
                    redo=a.redo, do_verify=not a.no_verify)
    sys.exit(0 if r["status"] in ("complete", "empty") else 1)


if __name__ == "__main__":
    main()
