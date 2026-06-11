#!/usr/bin/env python3
"""
bench_translate.py — utilitario de BENCHMARK (dev). NAO faz parte do pipeline de producao.

Roda o backend `api` (model._api_translate) numa cena com um modelo dado e grava a saida num
arquivo PARALELO (`translations_<scene_id>.<tag>.json`), SEM tocar no `translations_<scene_id>.json` aprovado.
Serve p/ comparar modelos (ex.: Sonnet vs Opus) e como smoke-test do caminho de rede/schema/streaming.

Uso:  python bench_translate.py <projeto> <scene> [--model claude-sonnet-4-6] [--tag sonnet]
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import model as M     # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Benchmark do backend api (saida paralela).")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--model", default=M.MODEL_TRANSLATE)
    ap.add_argument("--tag", default=None, help="sufixo do arquivo paralelo (default: derivado do modelo)")
    ap.add_argument("--effort", default=M.EFFORT_TRANSLATE, choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--think", action="store_true", help="liga adaptive thinking (default: desligado)")
    a = ap.parse_args()
    root = Path(a.project)
    tag = a.tag or a.model.split("-")[1]      # 'sonnet' / 'opus'
    scene_id = context_pack.scene_id_of(a.scene)
    pack = context_pack.build_pack(root, a.scene)
    t0 = time.time()
    data, usage, meta = M._api_translate(root, a.scene, pack, a.model, effort=a.effort, think=a.think)
    dt = time.time() - t0
    # NAO usar prefixo 'translations_' (colide com o glob do build_plan_chapter, que exige exatamente 1)
    out = root / "artifacts" / a.scene / f"bench_{scene_id}.{tag}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    n = len(data.get("lines", {}))
    print(f"OK {a.scene} via {a.model}: {n} linhas em {dt:.1f}s -> {out}")
    print(f"   usage: in={usage['in']} out={usage['out']} "
          f"cache_read={usage['cache_read']} cache_write={usage['cache_write']}")


if __name__ == "__main__":
    main()
