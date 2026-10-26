#!/usr/bin/env python3
"""
espera_reset.py — quanto esperar ate a cota da assinatura voltar (usado pelo rodar_ondas.ps1).

Le a saida do `claude -p` (stdin ou arquivo) e, se ela traz aviso de limite de sessao ou de semana com o
horario de liberacao, imprime os segundos ate la (+ margem de 2 min). Sem aviso de limite: imprime nada e
sai com 1. Formatos aceitos: `resets 3pm`, `resets 3:30pm`, `resets Oct 21, 9am`, `resets Oct 21 at 9am` e o
antigo `usage limit reached|<epoch>`. Horario sem data = proxima ocorrencia (hoje, ou amanha se ja passou).

Uso:  python espera_reset.py [arquivo]      (sem arquivo le o stdin)
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta

MARGEM = 120
_MESES = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
_LIMITE = re.compile(r"limit", re.I)
_EPOCH = re.compile(r"usage limit reached\|(\d{9,11})", re.I)
_HORA = re.compile(r"resets\s+(?:(?P<mes>[A-Za-z]{3})[a-z]*\.?\s+(?P<dia>\d{1,2})(?:,|\s+at)?\s+)?"
                   r"(?P<h>\d{1,2})(?::(?P<m>\d{2}))?\s*(?P<ap>am|pm)", re.I)


def segundos_ate_reset(texto: str, agora: datetime | None = None) -> int | None:
    """Segundos de espera (>= 1, com margem) ou None se o texto nao traz aviso de limite com horario."""
    agora = agora or datetime.now()
    e = _EPOCH.search(texto)
    if e:
        return max(1, int(e.group(1)) - int(agora.timestamp()) + MARGEM)
    if not _LIMITE.search(texto):
        return None
    m = _HORA.search(texto)
    if not m:
        return None
    h = int(m["h"]) % 12 + (12 if m["ap"].lower() == "pm" else 0)
    alvo = agora.replace(hour=h, minute=int(m["m"] or 0), second=0, microsecond=0)
    if m["mes"] and m["mes"].lower() in _MESES:
        alvo = alvo.replace(month=_MESES[m["mes"].lower()], day=int(m["dia"]))
        if alvo < agora:
            alvo = alvo.replace(year=alvo.year + 1)
    elif alvo < agora:
        alvo += timedelta(days=1)
    return max(1, int((alvo - agora).total_seconds()) + MARGEM)


def main() -> None:
    texto = open(sys.argv[1], encoding="utf-8", errors="replace").read() if len(sys.argv) > 1 else sys.stdin.read()
    s = segundos_ate_reset(texto)
    if s is None:
        sys.exit(1)
    print(s)


if __name__ == "__main__":
    main()
