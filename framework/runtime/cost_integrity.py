#!/usr/bin/env python3
"""cost_integrity.py — o ledger (api_ledger.jsonl) e integro e consistente?

Verifica, linha a linha: campos obrigatorios (t, model, usage), nenhum contador de uso negativo, linha de API
paga com `cost_usd` igual ao recalculado de `usage` pela tabela de precos (cost.cost_of), linha de sessao com
`cost_usd` 0 e `api_equiv_usd` >= 0. Linha de sessao agrega varias requisicoes (o degrau de contexto longo e por
requisicao), por isso o equivalente dela nao e recalculado aqui. Modelo sem preco na tabela (ex.: local/ollama)
nao e recalculado.

Uso: python cost_integrity.py <projeto> [<projeto> ...]   (sai 1 se achar problema)
"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import cost  # noqa: E402
import cost_report  # noqa: E402
import paths  # noqa: E402

TOL = 1e-4


def problemas(rows: list[dict]) -> list[str]:
    out = []
    for n, r in enumerate(rows, 1):
        tag = f"linha {n} (cena {r.get('scene')})"
        usage = r.get("usage")
        if not isinstance(r.get("t"), int | float) or not r.get("model") or not isinstance(usage, dict):
            out.append(f"{tag}: faltam t/model/usage")
            continue
        if any(not isinstance(v, int | float) or v < 0 for v in usage.values()):
            out.append(f"{tag}: contador de uso negativo ou nao numerico {usage}")
        if r.get("source") == "session":
            if r.get("cost_usd", 0) != 0 or (r.get("api_equiv_usd") or 0) < 0:
                out.append(f"{tag}: linha de sessao com cost_usd != 0 ou equivalente negativo")
        elif r["model"] in cost._PRICE:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                esperado = cost.cost_of(r["model"], usage, batch=bool(r.get("batch")))
            if abs(esperado - r.get("cost_usd", 0.0)) > TOL:
                out.append(f"{tag}: cost_usd {r.get('cost_usd')} != recalculado {esperado:.5f}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Confere a integridade e a consistencia do ledger de gasto.")
    ap.add_argument("project", nargs="+")
    a = ap.parse_args()
    rc = 0
    for proj in a.project:
        probs = problemas(cost_report.read_ledger(paths.require_project(proj)))
        print(f"{proj}: " + ("ledger integro" if not probs else f"{len(probs)} problema(s)"))
        for p in probs[:20]:
            print("  " + p)
        rc |= bool(probs)
    return rc


if __name__ == "__main__":
    sys.exit(main())
