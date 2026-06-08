#!/usr/bin/env python3
"""
test_cost_model.py — sanity do modelo de custo (pytest).

Não trava um valor exato (é estimativa), mas trava as RELAÇÕES que precisam valer:
números positivos e coerentes, e model-mix + caching ⇒ mais barato que o modelo forte.

Rodar:  pytest framework/validation/
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cost_model as C  # noqa: E402

REPO = HERE.parent.parent
REF = REPO / "projects" / "utawarerumono"


@pytest.mark.skipif(not REF.is_dir(), reason="projeto de referência ausente")
def test_scenarios_positive_and_ordered():
    r = C.cost_scenarios(REF)
    sc = r["scenarios"]
    for name, s in sc.items():
        assert s["total"] > 0, f"custo não-positivo em {name}"
    # model-mix é mais barato que tudo-forte; caching não encarece
    assert sc["mix"]["total"] < sc["forte"]["total"], "model-mix deveria ser mais barato que o forte"
    assert sc["mix_cache"]["total"] <= sc["mix"]["total"], "caching não deveria encarecer"


@pytest.mark.skipif(not REF.is_dir(), reason="projeto de referência ausente")
def test_per_1k_and_projection_sane():
    r = C.cost_scenarios(REF)
    e = r["estimate"]
    assert e["n"] > 0 and e["src_tok"] > 0
    per_k = r["scenarios"]["forte"]["total"] / e["n"] * 1000
    assert 0 < per_k < 1000, f"$/1k fora de faixa plausível: {per_k}"


def test_cache_read_cheaper_than_full_input():
    # 1 chamada com caching paga 0.1× pelo contexto vs input cheio
    full = C._call_cost(10_000, 1_000, "opus", ctx_tok=8_000, cache=False)
    cached = C._call_cost(10_000, 1_000, "opus", ctx_tok=8_000, cache=True)
    assert cached < full
