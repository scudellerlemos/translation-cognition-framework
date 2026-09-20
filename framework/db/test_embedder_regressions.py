"""test_embedder_regressions.py — regressoes de Embedder com encoder FAKE deterministico + sqlite-vec real.

Cobre: (1) KNN do vec0 roda sobre TODOS os projetos -- o top-k de um projeto nao pode sumir por
causa de vetores de outro; (2) texto alterado depois de indexado tem que ser reindexado (vetor
obsoleto servia RAG/TM com conteudo velho). Pula sem numpy/sqlite-vec (stack opcional, requirements-ml).
"""
import sys
import zlib
from pathlib import Path

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sqlite_vec")

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import embedder  # noqa: E402
from store import Store  # noqa: E402


class _FakeST:
    def __init__(self, name):
        pass

    def encode(self, texts, **_kw):
        out = []
        for t in texts:
            seed = zlib.crc32(t.encode())
            v = np.random.RandomState(seed).randn(384)
            out.append(v / np.linalg.norm(v))
        return np.array(out)


@pytest.fixture
def emb(monkeypatch):
    monkeypatch.setattr(embedder, "_load_sentence_transformers", lambda: _FakeST)
    e = embedder.Embedder()
    e._rerank = lambda query, hits: hits          # sem FlashRank no teste
    return e


def test_search_nao_perde_hits_para_vetores_de_outro_projeto(tmp_path, emb):
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("a", "A")
        db.upsert_project("b", "B")
        for i in range(30):
            db.upsert_translation("b", "s", f"o{i}", source=f"Hello {i}", target="x", approved=True)
        db.upsert_translation("a", "s2", "o9", source="Hello 99", target="y", approved=True)
        emb.index_project(db._con, "a")
        emb.index_project(db._con, "b")
        hits = emb.search(db._con, "Hello 5", project_id="a", k=5)
    assert [h["source"] for h in hits] == ["Hello 99"]


def test_texto_alterado_e_reindexado(tmp_path, emb):
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("a", "A")
        db.upsert_translation("a", "s", "o1", source="dragon of wind", target="x", approved=True)
        assert emb.index_project(db._con, "a") == 1
        assert emb.index_project(db._con, "a") == 0           # nada mudou -> nada a reindexar
        db.upsert_translation("a", "s", "o1", source="lore about the moon", target="y", approved=True)
        assert emb.index_project(db._con, "a") == 1           # texto novo -> reindexa
        hits = emb.search(db._con, "lore about the moon", project_id="a", k=3)
    assert hits and hits[0]["source"] == "lore about the moon"
    assert hits[0]["score"] == pytest.approx(1.0, abs=1e-3)   # vetor NOVO (nao o de "dragon of wind")
