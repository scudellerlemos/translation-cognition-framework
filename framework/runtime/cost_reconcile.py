#!/usr/bin/env python3
"""cost_reconcile.py — concilia o ledger (api_ledger.jsonl) com a fatura do provedor, mes a mes.

O ledger e a verdade de gasto DO FRAMEWORK; a fatura e a verdade do provedor. Se divergem alem da tolerancia,
ou o ledger perde chamadas (log best-effort, tabela de precos velha) ou ha uso fora do framework na mesma chave.
So conta a API paga (`cost_usd`); o equivalente de sessao nao entra na fatura.

Uso: python cost_reconcile.py <projeto> --invoice 2026-10=12.34 [--invoice 2026-09=8.00 ...] [--tolerance 0.05]
Sai 1 se algum mes diverge acima da tolerancia (fracao da fatura) ou nao tem linha no ledger e tem fatura.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import cost_report  # noqa: E402
import paths  # noqa: E402

TOLERANCIA = 0.05


def por_mes(root) -> dict[str, float]:
    """Gasto da API paga por mes (AAAA-MM, hora local) segundo o ledger."""
    out: dict[str, float] = {}
    for r in cost_report.read_ledger(Path(root)):
        if r.get("t"):
            m = time.strftime("%Y-%m", time.localtime(r["t"]))
            out[m] = out.get(m, 0.0) + float(r.get("cost_usd", 0.0))
    return out


def conciliar(ledger: dict[str, float], faturas: dict[str, float], tolerancia: float = TOLERANCIA) -> list[dict]:
    """Uma linha por mes de fatura: ledger, fatura, diferenca (USD e fracao da fatura) e se esta ok."""
    rows = []
    for mes, fat in sorted(faturas.items()):
        led = round(ledger.get(mes, 0.0), 4)
        dif = round(led - fat, 4)
        frac = abs(dif) / fat if fat else (0.0 if not led else 1.0)
        rows.append({"mes": mes, "ledger_usd": led, "fatura_usd": fat, "dif_usd": dif,
                     "dif_frac": round(frac, 4), "ok": frac <= tolerancia})
    return rows


def _parse(par: str) -> tuple[str, float]:
    mes, _, v = par.partition("=")
    time.strptime(mes, "%Y-%m")                       # valida o formato
    return mes, float(v)


def main() -> int:
    ap = argparse.ArgumentParser(description="Concilia o ledger de gasto com a fatura do provedor.")
    ap.add_argument("project")
    ap.add_argument("--invoice", action="append", required=True, metavar="AAAA-MM=USD")
    ap.add_argument("--tolerance", type=float, default=TOLERANCIA)
    a = ap.parse_args()
    root = paths.require_project(a.project)
    try:
        faturas = dict(_parse(p) for p in a.invoice)
    except ValueError as exc:
        print(f"--invoice invalido (use AAAA-MM=USD): {exc}", file=sys.stderr)
        return 2
    rows = conciliar(por_mes(root), faturas, a.tolerance)
    for r in rows:
        print(f"{r['mes']}  ledger ${r['ledger_usd']:9.4f}  fatura ${r['fatura_usd']:9.4f}  "
              f"dif ${r['dif_usd']:+9.4f} ({100 * r['dif_frac']:.1f}%)  {'ok' if r['ok'] else 'DIVERGE'}")
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
