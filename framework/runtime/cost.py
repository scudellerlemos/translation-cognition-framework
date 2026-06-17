"""cost.py — PRECO e LEDGER de gasto (fonte unica de custo do harness).

Extraido do model.py (que estava virando god-module). Aqui ficam: a tabela de precos, o calculo de
custo de uma chamada, e o append ao api_ledger.jsonl. `model`/`run_scene`/`cost_report` importam daqui
(re-exportado por `model` p/ compatibilidade — sem mudar call sites). NAO importa model (camada abaixo).
"""
from __future__ import annotations
import json
import os
import time
from pathlib import Path

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


_MAX_LEDGER_MB = 100


def _warn_ledger_size(p: Path) -> None:
    """Emite RuntimeWarning se o ledger ultrapassa _MAX_LEDGER_MB — sinal de que precisa rotacao."""
    try:
        mb = p.stat().st_size / (1024 * 1024)
        if mb > _MAX_LEDGER_MB:
            import warnings as _warnings
            _warnings.warn(
                f"api_ledger.jsonl tem {mb:.1f} MB > {_MAX_LEDGER_MB} MB — "
                f"considere arquivar/rotacionar o ledger.",
                RuntimeWarning, stacklevel=3)
    except OSError:
        pass


def _ledger_append(p: Path, line: str):
    """Append atomico ao ledger: usa lock-file cross-platform (O_CREAT|O_EXCL e atomico em POSIX e
    Windows). Best-effort: se nao conseguir o lock em 1 s, escreve sem lock (ledger e auditoria, nao
    banco de dados — corrida improvavel e aceitavel como fallback)."""
    lock = p.with_suffix(".lock")
    acquired = False
    for _ in range(50):
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            acquired = True
            break
        except FileExistsError:
            time.sleep(0.02)
    try:
        with p.open("a", encoding="utf-8") as f:
            f.write(line)
    finally:
        if acquired:
            try:
                lock.unlink()
            except Exception:
                pass


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
    lp = paths.ledger(root)
    _warn_ledger_size(lp)          # fora do try: warning.warn nao e excecao por padrao
    try:
        _ledger_append(lp, json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return rec
