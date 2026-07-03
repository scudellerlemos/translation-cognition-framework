#!/usr/bin/env python3
"""
batch_status.py — checagem HONESTA de batches em andamento na conta.

Por que existe: `client.messages.batches.retrieve().request_counts.succeeded` NAO reflete
progresso em tempo real durante `processing_status='in_progress'` — descoberto ao vivo
(Souldiers, 2026-07-03): um batch de 146 requests ficou reportando 0 sucesso por 111+ minutos;
ao cancelar por achar que estava travado, `results()` revelou que 134/146 (92%) ja tinham
sucedido de verdade. O cancelamento so matou as ~12 que ainda estavam genuinamente em voo —
perda evitavel. Ver memory `anthropic-batch-progress-unreliable`.

Este script NUNCA cancela nada — so reporta, com o aviso embutido, pra qualquer decisao de
cancelar ser deliberada e feita separadamente (client.messages.batches.cancel(batch_id)).

Uso:
  python batch_status.py                 # lista todos os batches in_progress
  python batch_status.py <batch_id>      # detalhe de 1 batch
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from llm_client import _client  # noqa: E402

_WARNING = (
    "AVISO: 'succeeded' pode ficar em 0 mesmo com a maior parte do batch pronta — "
    "esse contador NAO atualiza em tempo real durante in_progress (confirmado ao vivo, "
    "2026-07-03: 0/146 por 111min, mas 134 ja tinham sucedido). NAO cancelar por isso. "
    "So cancelar por decisao deliberada (SLA de 24h estourado, ou incidente confirmado em "
    "status.claude.com) — cancelar mata o que ainda esta genuinamente em voo."
)


def _age(created_at) -> str:
    delta = datetime.now(timezone.utc) - created_at
    h, rem = divmod(int(delta.total_seconds()), 3600)
    m = rem // 60
    return f"{h}h{m:02d}m"


def report_one(client, batch_id: str) -> None:
    b = client.messages.batches.retrieve(batch_id)
    print(f"{b.id}")
    print(f"  status: {b.processing_status} | idade: {_age(b.created_at)}")
    print(f"  counts: {b.request_counts}")
    if b.processing_status == "in_progress":
        print(f"  [!] {_WARNING}")


def main() -> None:
    client = _client()
    if len(sys.argv) > 1:
        report_one(client, sys.argv[1])
        return
    batches = list(client.messages.batches.list(limit=20))
    in_progress = [b for b in batches if b.processing_status == "in_progress"]
    if not in_progress:
        print("Nenhum batch in_progress no momento.")
        return
    print(f"{len(in_progress)} batch(es) in_progress:\n")
    for b in in_progress:
        report_one(client, b.id)
        print()


if __name__ == "__main__":
    main()
