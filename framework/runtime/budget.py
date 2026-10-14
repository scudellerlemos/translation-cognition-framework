"""budget.py — FONTE UNICA da conta de orcamento de bytes (modelo, ferramentas locais e conferencias usam esta).

Regra: bytes UTF-8 reais quando o conector NAO translitera (`target_charset_supported` estritamente True);
senao a forma TRANSLITERADA (NFKD sem combinantes), que e o que o reinsert grava. `budget_reserves_terminator`
reserva 1 byte pro \0. Token de controle (ex.: `[07]`) que o conector grava em 1 byte entra via `token_rx`.
Excecao pontual de +1 byte decidida pelo humano: `byte_budget_exceptions` no project.json (`effective_budget`).
"""
from __future__ import annotations

import unicodedata


def translit_len(t, token_rx=None) -> int:
    s = unicodedata.normalize("NFKD", t or "")
    if token_rx is not None:
        s = token_rx.sub("x", s)
    return len("".join(c for c in s if not unicodedata.combining(c)))


def budget_len(t, pc: dict | None = None, token_rx=None) -> int:
    if (pc or {}).get("target_charset_supported") is True:
        return len((token_rx.sub("x", t or "") if token_rx is not None else (t or "")).encode("utf-8"))
    return translit_len(t, token_rx)


def usable(budget, pc: dict | None = None):
    """Limite usavel: o budget menos o byte do terminador, quando o conector o reserva."""
    return None if budget is None else budget - (1 if (pc or {}).get("budget_reserves_terminator") else 0)


def effective_budget(off, budget, project_cfg: dict | None = None):
    """Aplica `byte_budget_exceptions` ({offset: novo_budget}) do project.json. Sem excecao, devolve o budget."""
    ex = (project_cfg or {}).get("byte_budget_exceptions") or {}
    return int(ex[off]) if off in ex else budget


def over_budget(t, budget, pc: dict | None = None, tol: float = 1.0, token_rx=None) -> bool:
    """True se `t` excede o limite usavel * tol. budget None = sem orcamento declarado; 0 e orcamento zero real."""
    if budget is None:
        return False
    return budget_len(t, pc, token_rx) > usable(budget, pc) * tol
