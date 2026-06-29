"""bench_local.py — Benchmark Ollama local vs baseline Sonnet aprovado.

Traduz uma cena com --backend ollama e compara linha a linha com as
traduções aprovadas do BoF4. Reporta: tempo, tokens, cobertura, divergências.

Uso:
  python bench_local.py <bof4_root> <scene> [--model qwen2.5:14b] [--out bench_result.json]
  python bench_local.py projects/breath_of_fire_4 AREAD001
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import context_pack  # noqa: E402
import model as M  # noqa: E402
import paths  # noqa: E402
from ollama_client import OLLAMA_MODEL_DEFAULT, health_check, list_models  # noqa: E402


def _load_approved(root: Path, scene: str) -> dict:
    """Carrega as traduções aprovadas do BoF4 para a cena. {offset: target}"""
    scene_dir = paths.scenes_dir(root) / scene
    approved = {}
    for csv_path in sorted(scene_dir.glob("approved_*.csv")):
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                off = row.get("offset", "")
                tgt = row.get("target", row.get("text_pt", ""))
                if off and tgt:
                    approved[off] = tgt
    return approved


def _compare(ollama_lines: dict, approved: dict) -> dict:
    """Compara saída Ollama com baseline aprovado."""
    all_offsets = set(approved) | set(ollama_lines)
    exact_match = sum(
        1 for o in all_offsets
        if ollama_lines.get(o, {}).get("t") == approved.get(o)
    )
    missing_in_ollama = [o for o in approved if o not in ollama_lines]
    missing_in_approved = [o for o in ollama_lines if o not in approved]
    divergent = [
        {"offset": o,
         "baseline": approved.get(o, ""),
         "ollama": (ollama_lines.get(o) or {}).get("t", "")}
        for o in all_offsets
        if o in approved and o in ollama_lines
        and ollama_lines[o].get("t") != approved.get(o)
    ][:20]  # primeiros 20 para não explodir o output
    return {
        "total_offsets": len(all_offsets),
        "exact_match": exact_match,
        "exact_match_pct": round(exact_match / max(len(all_offsets), 1) * 100, 1),
        "missing_in_ollama": len(missing_in_ollama),
        "missing_in_approved": len(missing_in_approved),
        "divergent_sample": divergent,
    }


def run_bench(bof4_root: Path, scene: str, model: str = None,
              out_path: Path = None) -> dict:
    model = model or OLLAMA_MODEL_DEFAULT

    print(f"[bench] Verificando Ollama em {bof4_root}...")
    if not health_check():
        print("ERRO: Ollama não responde. Inicie com `ollama serve`.")
        sys.exit(1)

    available = list_models()
    if available and not any(model in m for m in available):
        print(f"AVISO: modelo '{model}' não encontrado. Disponíveis: {available}")
        print(f"       Baixe com: ollama pull {model}")

    print(f"[bench] Montando context pack para {scene}...")
    pack = context_pack.write_pack(bof4_root, scene)
    n_lines = pack["n_lines"]
    print(f"        {n_lines} linhas no pack.")

    print(f"[bench] Traduzindo com Ollama ({model})...")
    t0 = time.time()
    data, usage, meta = M._ollama_translate(bof4_root, scene, pack, model)
    elapsed = round(time.time() - t0, 1)
    tok_s = round(usage.get("out", 0) / max(elapsed, 1), 1)

    print(f"        {elapsed}s | {usage.get('out', 0)} tokens saída | ~{tok_s} tok/s")
    print(f"        reuso TM: {meta['reused']} | novas ao modelo: {meta['novel']}")

    print("[bench] Carregando baseline aprovado do BoF4...")
    approved = _load_approved(bof4_root, scene)
    if not approved:
        print("        AVISO: nenhuma tradução aprovada encontrada para comparação.")

    print("[bench] Comparando outputs...")
    comparison = _compare(data.get("lines", {}), approved)

    result = {
        "scene": scene,
        "model": model,
        "n_lines": n_lines,
        "elapsed_s": elapsed,
        "tok_s": tok_s,
        "usage": usage,
        "meta": meta,
        "comparison": comparison,
    }

    print(f"\n{'='*50}")
    print(f"  Cena:          {scene}")
    print(f"  Modelo:        {model}")
    print(f"  Linhas:        {n_lines}")
    print(f"  Tempo:         {elapsed}s  (~{tok_s} tok/s)")
    print(f"  Tokens out:    {usage.get('out', 0)}")
    print(f"  Match exato:   {comparison['exact_match_pct']}% ({comparison['exact_match']}/{comparison['total_offsets']})")
    print(f"  Faltando:      {comparison['missing_in_ollama']} offsets")
    if comparison["divergent_sample"]:
        print("\n  Primeiras divergências:")
        for d in comparison["divergent_sample"][:5]:
            print(f"    [{d['offset']}]")
            print(f"      baseline: {d['baseline'][:80]!r}")
            print(f"      ollama:   {d['ollama'][:80]!r}")
    print(f"{'='*50}\n")

    if out_path:
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[bench] Resultado salvo em {out_path}")

    return result


def main():
    ap = argparse.ArgumentParser(description="Benchmark Ollama local vs baseline Sonnet.")
    ap.add_argument("bof4_root", help="Raiz do projeto BoF4 (com traduções aprovadas)")
    ap.add_argument("scene", help="Cena a benchmarkar (ex: AREAD001)")
    ap.add_argument("--model", default=None, help=f"Modelo Ollama (default: {OLLAMA_MODEL_DEFAULT})")
    ap.add_argument("--out", default=None, help="Salva resultado JSON neste arquivo")
    a = ap.parse_args()
    run_bench(
        Path(a.bof4_root), a.scene, a.model,
        Path(a.out) if a.out else None,
    )


if __name__ == "__main__":
    main()
