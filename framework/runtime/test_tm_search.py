"""Testes de contrato para tm_search.py (índice semântico flat-file).

Marcados com pytest.mark.skipif quando sentence-transformers não está instalado
(comportamento esperado na CI que usa só requirements-dev.txt).
"""
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

try:
    import sentence_transformers  # noqa: F401
    _HAS_ML = True
except ImportError:
    _HAS_ML = False

needs_ml = pytest.mark.skipif(not _HAS_ML, reason="sentence-transformers não instalado")

import tm_search  # noqa: E402


@needs_ml
def test_build_index_creates_files(tmp_path):
    entries = [
        {"source": "Hello world", "target": "Olá mundo", "speaker": "Haku", "src_key": "k1"},
        {"source": "Goodbye friend", "target": "Tchau amigo", "speaker": "Kuon", "src_key": "k2"},
        {"source": "The battle begins", "target": "A batalha começa", "speaker": "Haku", "src_key": "k3"},
        {"source": "Run away now", "target": "Fuja agora", "speaker": "Kuon", "src_key": "k4"},
        {"source": "Victory is ours", "target": "A vitória é nossa", "speaker": "Haku", "src_key": "k5"},
    ]
    n = tm_search.build_index(entries, tmp_path)
    assert n == 5
    assert (tmp_path / "tm_embeddings.npy").is_file()
    meta = json.loads((tmp_path / "tm_index.json").read_text())
    assert meta["n"] == 5
    assert meta["model"] == tm_search._MODEL_NAME
    assert len(meta["entries"]) == 5


@needs_ml
def test_build_index_cache_hit(tmp_path):
    entries = [{"source": "Hello", "target": "Olá", "speaker": "X", "src_key": "k1"}]
    tm_search.build_index(entries, tmp_path)
    # segunda chamada com mesmo n → pula (retorna 0)
    n = tm_search.build_index(entries, tmp_path)
    assert n == 0


@needs_ml
def test_build_index_invalidates_on_n_change(tmp_path):
    entries1 = [{"source": "Hello", "target": "Olá", "speaker": "X", "src_key": "k1"}]
    tm_search.build_index(entries1, tmp_path)
    entries2 = entries1 + [{"source": "World", "target": "Mundo", "speaker": "X", "src_key": "k2"}]
    n = tm_search.build_index(entries2, tmp_path)
    assert n == 2


def test_load_index_returns_none_when_missing(tmp_path):
    result = tm_search.load_index(tmp_path)
    assert result is None


@needs_ml
def test_load_index_returns_dict(tmp_path):
    entries = [{"source": "Hello", "target": "Olá", "speaker": "X", "src_key": "k1"}]
    tm_search.build_index(entries, tmp_path)
    index = tm_search.load_index(tmp_path)
    assert index is not None
    assert "vecs" in index
    assert "entries" in index
    assert index["vecs"].shape[0] == 1


@needs_ml
def test_search_excludes_exact_keys(tmp_path):
    entries = [
        {"source": "Hello world", "target": "Olá mundo", "speaker": "A", "src_key": "exact"},
        {"source": "Hello there friend", "target": "Olá amigo", "speaker": "B", "src_key": "similar"},
    ]
    tm_search.build_index(entries, tmp_path)
    index = tm_search.load_index(tmp_path)
    results = tm_search.search("Hello world", index, top_k=5, exclude_keys={"exact"})
    keys = {r["source"] for r in results}
    assert "Hello world" not in keys


@needs_ml
def test_search_deterministic(tmp_path):
    entries = [
        {"source": f"Line {i}", "target": f"Linha {i}", "speaker": "X", "src_key": f"k{i}"}
        for i in range(20)
    ]
    tm_search.build_index(entries, tmp_path)
    index = tm_search.load_index(tmp_path)
    r1 = tm_search.search("Some line to query", index)
    r2 = tm_search.search("Some line to query", index)
    assert [h["source"] for h in r1] == [h["source"] for h in r2]


def test_build_index_import_error_when_no_ml(tmp_path):
    """Sem sentence-transformers: build_index lança ImportError (não retorna silencioso)."""
    if _HAS_ML:
        pytest.skip("sentence-transformers presente — teste só vale quando ausente")
    with pytest.raises(ImportError):
        tm_search.build_index([{"source": "x", "target": "y", "speaker": "", "src_key": "k"}],
                               tmp_path)
