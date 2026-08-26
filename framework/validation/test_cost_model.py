#!/usr/bin/env python3
"""
test_cost_model.py — sanity do modelo de custo (pytest).

Não trava um valor exato (é estimativa), mas trava as RELAÇÕES que precisam valer:
números positivos e coerentes, e model-mix + caching ⇒ mais barato que o modelo forte.

Rodar:  pytest framework/validation/
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cost_model as C  # noqa: E402


def _synthetic_project(tmp_path):
    """Projeto sintetico minimo (project.json + translation_plan.json) -- so mecanica de
    custo generica (relacoes entre cenarios, incl. back-translation de linha de alto risco),
    sem depender de corpus real do cliente."""
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    art = tmp_path / "artifacts"
    art.mkdir()
    (art / "translation_plan.json").write_text(json.dumps({"lines": [
        {"text_source": "Hero picks up the Widget and looks around the room.",
         "base_translation": "O heroi pega a Bugiganga e olha ao redor da sala.",
         "risk_level": "low"},
        {"text_source": "I see... this changes everything, she said quietly.",
         "base_translation": "Entendo... isso muda tudo, ela disse baixinho.",
         "risk_level": "medium"},
        {"text_source": "This is my final wish before I die.",
         "base_translation": "Este e meu ultimo desejo antes de morrer.",
         "risk_level": "high"},
    ]}), encoding="utf-8")
    return tmp_path


def test_scenarios_positive_and_ordered(tmp_path):
    r = C.cost_scenarios(_synthetic_project(tmp_path))
    sc = r["scenarios"]
    for name, s in sc.items():
        assert s["total"] > 0, f"custo não-positivo em {name}"
    # model-mix é mais barato que tudo-forte; caching não encarece
    assert sc["mix"]["total"] < sc["forte"]["total"], "model-mix deveria ser mais barato que o forte"
    assert sc["mix_cache"]["total"] <= sc["mix"]["total"], "caching não deveria encarecer"


def test_per_1k_and_projection_sane(tmp_path):
    r = C.cost_scenarios(_synthetic_project(tmp_path))
    e = r["estimate"]
    assert e["n"] > 0 and e["src_tok"] > 0
    per_k = r["scenarios"]["forte"]["total"] / e["n"] * 1000
    assert 0 < per_k < 1000, f"$/1k fora de faixa plausível: {per_k}"


def test_cache_read_cheaper_than_full_input():
    # 1 chamada com caching paga 0.1× pelo contexto vs input cheio
    full = C._call_cost(10_000, 1_000, "opus", ctx_tok=8_000, cache=False)
    cached = C._call_cost(10_000, 1_000, "opus", ctx_tok=8_000, cache=True)
    assert cached < full
