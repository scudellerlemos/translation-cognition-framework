"""Onda 3 (custo): ledger integro e consistente — regra verificada em linhas sinteticas e em todo ledger do repo."""
from pathlib import Path

import cost
import cost_integrity
import cost_report
import pytest
import session_usage

REPO = Path(__file__).resolve().parents[2]
USO = {"in": 1000, "out": 500, "cache_read": 2000, "cache_write": 300, "cache_write_1h": 0}
MODELO = "claude-sonnet-5-5"


def _paga(**kw):
    return {"t": 1.0, "scene": "s", "kind": "x", "model": MODELO, "usage": dict(USO),
            "cost_usd": round(cost.cost_of(MODELO, USO), 5), **kw}


def test_linha_boa_passa():
    sessao = {"t": 1.0, "scene": "_session", "source": "session", "model": MODELO, "usage": dict(USO),
              "cost_usd": 0.0, "api_equiv_usd": 1.2}
    assert cost_integrity.problemas([_paga(), sessao]) == []


@pytest.mark.parametrize("ruim,trecho", [
    ({"usage": {**USO, "cache_write": -5}}, "negativo"),
    ({"cost_usd": 9.99}, "recalculado"),
    ({"model": ""}, "faltam"),
    ({"source": "session", "cost_usd": 0.5, "api_equiv_usd": 1.0}, "sessao"),
])
def test_linha_com_defeito_e_apontada(ruim, trecho):
    assert any(trecho in p for p in cost_integrity.problemas([_paga(**ruim)]))


def test_modelo_sem_preco_nao_e_recalculado():
    assert cost_integrity.problemas([_paga(model="ollama:local", cost_usd=0.0)]) == []


def test_usage_de_sessao_nunca_sai_negativo():
    """Regressao: ephemeral_1h maior que o total de cache criado gerava cache_write negativo no ledger."""
    u = session_usage._usage({"cache_creation_input_tokens": 100, "cache_creation": {"ephemeral_1h_input_tokens": 250}})
    assert u["cache_write"] == 0 and u["cache_write_1h"] == 100
    assert min(session_usage._usage({}).values()) == 0


def test_todo_ledger_do_repo_e_integro():
    ledgers = sorted(REPO.glob("projects/*/artifacts/api_ledger.jsonl"))
    for lp in ledgers:
        probs = cost_integrity.problemas(cost_report.read_ledger(lp.parent.parent))
        assert not probs, f"{lp.parent.parent.name}: {probs[:3]}"
