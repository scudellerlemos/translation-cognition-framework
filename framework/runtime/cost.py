"""cost.py — PRECO e LEDGER de gasto (fonte unica de custo do harness).

Extraido do model.py (que estava virando god-module). Aqui ficam: a tabela de precos, o calculo de
custo de uma chamada, e o append ao api_ledger.jsonl. `model`/`run_scene`/`cost_report` importam daqui
(re-exportado por `model` p/ compatibilidade — sem mudar call sites). NAO importa model (camada abaixo).
"""
from __future__ import annotations
import json
import time

import paths  # noqa: E402

# precos US$/token (skill claude-api 2026-05-26); cache_read=0.1x in, cache_write=1.25x in.
_PRICE = {"claude-opus-4-8":   {"in": 5.00e-6, "out": 25.00e-6},
          "claude-sonnet-4-6": {"in": 3.00e-6, "out": 15.00e-6},
          "claude-haiku-4-5":  {"in": 1.00e-6, "out":  5.00e-6}}


def cost_of(model: str, u: dict, *, batch: bool = False) -> float:
    """Custo US$ de uma chamada a partir do usage (in/out/cache_read/cache_write). A Batch API tem
    desconto de 50% sobre TODO o uso (batch=True -> 0.5x)."""
    p = _PRICE.get(model)
    if not p or not u:
        return 0.0
    base = (u.get("in", 0) * p["in"] + u.get("cache_read", 0) * p["in"] * 0.10
            + u.get("cache_write", 0) * p["in"] * 1.25 + u.get("out", 0) * p["out"])
    return base * (0.5 if batch else 1.0)


def log_api_call(root, scene, kind, model, usage, *, batch=False):
    """Anexa 1 linha a artifacts/api_ledger.jsonl por chamada de API CONCLUIDA (cada tentativa de
    cobertura e cada escalonamento de fitting). E a VERDADE de gasto: registra TODA chamada cobrada,
    INCLUSIVE as de cenas que depois falham (cobertura/verify) ou retries — exatamente o que o
    metrics.jsonl (resumo so-de-sucesso) perde. Sem isso o saldo surpreende (estimado << real).
    Best-effort (nunca derruba a traducao por falha de log). Ver cost_report.py p/ o agregado."""
    if not usage:
        return None
    rec = {"t": round(time.time(), 3), "scene": scene, "kind": kind, "model": model,
           "batch": bool(batch), "usage": dict(usage),
           "cost_usd": round(cost_of(model, usage, batch=batch), 5)}
    try:
        p = paths.ledger(root)
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return rec
