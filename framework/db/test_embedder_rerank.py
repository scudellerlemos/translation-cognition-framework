"""test_embedder_rerank.py — o rerank FlashRank e refinamento opcional: modelo ausente/corrompido
(NoSuchFile do onnxruntime, sem rede) nao pode derrubar a busca; cai na ordem vetorial com aviso."""
import sys
import types
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import embedder  # noqa: E402


def test_rerank_falls_back_to_vector_order_when_ranker_breaks(monkeypatch):
    fake = types.ModuleType("flashrank")

    class _Ranker:
        def __init__(self, **_kw):
            raise RuntimeError("[ONNXRuntimeError] NO_SUCHFILE")

    fake.Ranker, fake.RerankRequest = _Ranker, object   # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "flashrank", fake)
    hits = [{"source": "a"}, {"source": "b"}]
    e = embedder.Embedder.__new__(embedder.Embedder)
    with pytest.warns(RuntimeWarning, match="rerank FlashRank indisponivel"):
        assert e._rerank("q", hits) == hits
