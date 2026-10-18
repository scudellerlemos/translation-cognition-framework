"""Onda 3 (RAG): recall@k do RAG com o modelo REAL num corpus sintetico, contra piso e baseline.

A parte real pula sem a stack ML (roda no workflow `ml-coverage`); a logica de piso/baseline roda sempre."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import rag_eval  # noqa: E402

BOM = {"recall@1": 0.95, "recall@3": 1.0, "recall@5": 1.0, "mrr": 0.97, "n_casos": 40}


def test_problemas_piso_e_baseline():
    assert rag_eval.problemas(BOM, BOM) == []
    ruim = {**BOM, "recall@1": 0.5}
    assert any("abaixo do piso" in p for p in rag_eval.problemas(ruim, None))
    queda = {**BOM, "recall@1": 0.88}                       # acima do piso, mas 0,07 abaixo do baseline
    assert rag_eval.problemas(queda, None) == []
    assert any("caiu" in p for p in rag_eval.problemas(queda, BOM))


def test_baseline_gravado_passa_no_proprio_piso():
    base = json.loads(rag_eval.BASELINE.read_text(encoding="utf-8"))
    assert rag_eval.problemas(base, base) == []
    assert base["n_casos"] == len(rag_eval.CASOS)


def test_corpus_sem_duplicata():
    fontes = [f for f, _ in rag_eval.CASOS]
    assert len(set(fontes)) == len(fontes) >= 40


def test_rag_real_nao_regrediu():
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    res = rag_eval.executar()
    base = json.loads(rag_eval.BASELINE.read_text(encoding="utf-8"))
    assert rag_eval.problemas(res, base) == [], res
