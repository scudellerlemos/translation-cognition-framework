#!/usr/bin/env python3
"""
quality_sample.py — MEDIDA DE QUALIDADE: taxa de erro por amostra aleatoria julgada pelo humano, taxa da
triagem e acerto do juiz. $0, sem IA: so sorteia, monta a planilha e faz a conta.

  export  sorteia N pares unicos (fonte+traducao) do jogo inteiro e junta os que o juiz da triagem apontou
          (risk_triage). A planilha nao diz de onde veio cada fala — o humano julga as cegas.
  score   le a planilha com a coluna `veredito` preenchida (ok / erro) e calcula:
            - taxa de erro da amostra aleatoria, com intervalo de 95% (a medida de qualidade);
            - taxa da triagem: quanto do que o juiz leu ele apontou (indicador por onda);
            - acerto do juiz: precisao (apontou e era erro) e alcance (erro da amostra que ele pegou).
          Grava um registro em qa_effectiveness.jsonl (historico, sem texto de fala).

Uso:
  python quality_sample.py export <projeto> [--n 200] [--seed q1]
  python quality_sample.py score  <projeto> --reviewer NOME [planilha.csv]
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import risk_triage  # noqa: E402

NAME = "amostra_qualidade"
COLS = ["id", "scene", "offset", "source_en", "target_pt", "veredito", "nota"]


def _h(seed: str, pid: str) -> str:
    return hashlib.sha1(f"{seed}|{pid}".encode(), usedforsecurity=False).hexdigest()


def export(root, n: int = 200, seed: str = "q1") -> dict:
    root = Path(root)
    allp = risk_triage.pairs(root, everything=True)
    seen, flagged = risk_triage.judged(root)
    sample = sorted(allp, key=lambda pid: _h(seed, pid))[:n]          # sorteio estavel: mesma seed, mesma amostra
    rows = sorted(set(sample) | (flagged & set(allp)), key=lambda pid: _h(seed + "|ordem", pid))   # embaralhado
    out = paths.qa_outbox(root)
    out.mkdir(parents=True, exist_ok=True)
    with (out / f"{NAME}.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        for pid in rows:
            scene, off = allp[pid]["where"][0]
            w.writerow([pid, scene, off, allp[pid]["source"], allp[pid]["target"], "", ""])
    (out / f"{NAME}.json").write_text(json.dumps({
        "seed": seed, "population": len(allp), "sample": sample, "flagged": sorted(flagged), "seen": len(seen),
        "weight": {pid: len(allp[pid]["where"]) for pid in rows}}), encoding="utf-8")
    return {"rows": len(rows), "sample": len(sample), "flagged": len(flagged), "population": len(allp),
            "path": str(out / f"{NAME}.csv")}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de 95% de uma proporcao (Wilson): honesto com amostra pequena e taxa perto de zero."""
    if not n:
        return 0.0, 1.0
    p, d = k / n, 1 + z * z / n
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    mid = (p + z * z / (2 * n)) / d
    return max(0.0, mid - half), min(1.0, mid + half)


def _sheet(root: Path, path) -> Path:
    if path:
        return Path(path)
    back = paths.qa_inbox(root) / f"{NAME}.csv"
    return back if back.is_file() else paths.qa_outbox(root) / f"{NAME}.csv"


def score(root, reviewer: str, path=None) -> dict:
    root = Path(root)
    meta = json.loads((paths.qa_outbox(root) / f"{NAME}.json").read_text(encoding="utf-8"))
    sheet = _sheet(root, path)
    raw = sheet.read_text(encoding="utf-8-sig")
    rows = csv.DictReader(raw.splitlines(), delimiter=";" if raw.count(";") > raw.count(",") else ",")
    verdict = {}
    for r in rows:
        v = (r.get("veredito") or "").strip().lower()
        if v:
            verdict[r["id"]] = v.startswith("e")              # erro / errado; qualquer outra coisa = ok
    sample, flagged, weight = set(meta["sample"]), set(meta["flagged"]), meta["weight"]
    s = [p for p in sample if p in verdict]
    s_err = [p for p in s if verdict[p]]
    f = [p for p in flagged if p in verdict]
    lo, hi = wilson(len(s_err), len(s))
    w_all, w_err = sum(weight[p] for p in s), sum(weight[p] for p in s_err)
    rec = {
        "t": round(time.time(), 3), "source": "quality_sample", "reviewer": reviewer, "seed": meta["seed"],
        "population": meta["population"], "judged": len(s), "errors": len(s_err),
        "error_rate": round(len(s_err) / len(s), 4) if s else None, "ci95": [round(lo, 4), round(hi, 4)],
        "error_rate_weighted": round(w_err / w_all, 4) if w_all else None,      # pesa fala repetida pelo nº de copias
        "triage_rate": round(len(flagged) / meta["seen"], 4) if meta["seen"] else None,
        "judge_precision": round(sum(verdict[p] for p in f) / len(f), 3) if f else None,
        "judge_flagged_judged": len(f),
        # alcance: so vale se o juiz ja leu o jogo todo — erro em lote ainda sem veredito conta como nao pego
        "judge_recall": round(sum(p in flagged for p in s_err) / len(s_err), 3) if s_err and meta["seen"] else None,
        "unjudged": len(sample - set(verdict)),
    }
    with paths.qa_effectiveness(root).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Medida de qualidade por amostra julgada pelo humano.")
    ap.add_argument("cmd", choices=["export", "score"])
    ap.add_argument("project")
    ap.add_argument("sheet", nargs="?", default=None)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", default="q1")
    ap.add_argument("--reviewer", default=None)
    a = ap.parse_args()
    if a.cmd == "export":
        r = export(a.project, a.n, a.seed)
        print(f"amostra: {r['rows']} fala(s) para julgar ({r['sample']} sorteadas de {r['population']} pares unicos"
              f" + {r['flagged']} apontadas pelo juiz, misturadas) -> {r['path']}")
        print("  preencha a coluna `veredito` com ok ou erro; depois: quality_sample.py score <projeto> --reviewer NOME")
        return
    if not a.reviewer:
        ap.error("--reviewer NOME e obrigatorio: o veredito e de um humano")
    r = score(a.project, a.reviewer, a.sheet)

    def pct(x):
        return "n/d" if x is None else f"{100 * x:.1f}%"
    print(f"taxa de erro : {pct(r['error_rate'])} ({r['errors']}/{r['judged']}; 95%: {pct(r['ci95'][0])} a "
          f"{pct(r['ci95'][1])}) | pesada por repeticao: {pct(r['error_rate_weighted'])}")
    print(f"triagem      : juiz apontou {pct(r['triage_rate'])} do que leu")
    print(f"juiz         : precisao {pct(r['judge_precision'])} ({r['judge_flagged_judged']} apontada(s) julgada(s))"
          f" | alcance {pct(r['judge_recall'])}")
    if r["unjudged"]:
        print(f"  AVISO: {r['unjudged']} fala(s) da amostra sem veredito — a taxa vale so para as julgadas.")


if __name__ == "__main__":
    main()
