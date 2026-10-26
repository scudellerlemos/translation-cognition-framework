#!/usr/bin/env python3
"""
cota_uso.py — % de cota usada da assinatura, lida do `rate_limit_event` que o `claude -p --output-format stream-json
--verbose` emite (medido em 2026-10-21, claude 2.1.306: `unifiedWindows.five_hour|seven_day.utilization`, 0..1, e `resetsAt`).

A leitura custa uma chamada minima em Haiku (~US$ 0,003): use no inicio e no fim do lote, nao a cada minuto.
`parse` aceita o texto do stream (uma linha JSON por evento), entao o runner pode reaproveitar o stream de uma onda
em vez de fazer chamada extra.

Uso:  python cota_uso.py            (chama o claude -p e imprime "5h=<pct>% 7d=<pct>% reset5h=<hora>")
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime


def parse(stream: str) -> dict | None:
    """Ultimo `rate_limit_event` do stream -> {five_hour, seven_day (fracao 0..1), reset_five_hour (epoch)}; None se nao veio."""
    achado = None
    for ln in stream.splitlines():
        if '"rate_limit_event"' not in ln:
            continue
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        w = (ev.get("rate_limit_info") or {}).get("unifiedWindows") or {}
        if "five_hour" in w or "seven_day" in w:
            achado = {"five_hour": (w.get("five_hour") or {}).get("utilization"),
                      "seven_day": (w.get("seven_day") or {}).get("utilization"),
                      "reset_five_hour": (w.get("five_hour") or {}).get("resetsAt")}
    return achado


def ler() -> dict | None:
    r = subprocess.run(["claude", "-p", "ok", "--model", "haiku", "--no-chrome", "--output-format", "stream-json", "--verbose"],
                       capture_output=True, text=True, encoding="utf-8", timeout=120, check=False)
    return parse(r.stdout)


def main() -> int:
    c = ler()
    if not c:
        print("cota indisponivel (o claude -p nao emitiu rate_limit_event)")
        return 1
    reset = datetime.fromtimestamp(c["reset_five_hour"]).strftime("%H:%M") if c["reset_five_hour"] else "?"
    print(f"5h={100 * (c['five_hour'] or 0):.0f}% 7d={100 * (c['seven_day'] or 0):.0f}% reset5h={reset}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
