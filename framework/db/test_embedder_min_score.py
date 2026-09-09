"""test_embedder_min_score.py — cobre o corte por min_score em Embedder.search() (#172).

Nao carrega sentence-transformers/sqlite-vec (stack pesada, pode nao estar instalada):
Embedder e construido sem __init__ e encode()/_ensure_vec_table()/con.execute() sao stubados.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from embedder import Embedder  # noqa: E402


class _FakeCursor:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return self._rows


class _FakeCon:
    """distance -> score via score = 1 - distance**2/2 (ver embedder.search).
    distance=0.0 -> score 1.0 (identico); distance=1.0 -> score 0.5; distance=1.5 -> score -0.125."""

    def __init__(self, rows):
        self._rows = rows

    def execute(self, _sql, _params):
        return _FakeCursor(self._rows)


def _make_embedder(rows):
    emb = Embedder.__new__(Embedder)
    emb._ensure_vec_table = lambda con, kind="translation": None
    emb.encode = lambda texts: [[0.0]]
    emb._rerank = lambda query, hits: hits  # sem FlashRank no teste
    con = _FakeCon(rows)
    return emb, con


def _row(translation_id, distance):
    return (translation_id, distance, "sc1", 0, "src", "tgt", "spk", "neutral", "low")


def test_sem_min_score_mantem_todos_os_hits():
    rows = [_row(1, 0.0), _row(2, 1.0), _row(3, 1.5)]
    emb, con = _make_embedder(rows)
    hits = emb.search(con, "query", project_id="p1", k=3)
    assert len(hits) == 3


def test_min_score_corta_hits_fracos():
    rows = [_row(1, 0.0), _row(2, 1.0), _row(3, 1.5)]
    emb, con = _make_embedder(rows)
    hits = emb.search(con, "query", project_id="p1", k=3, min_score=0.6)
    assert [h["translation_id"] for h in hits] == [1]
    assert all(h["score"] >= 0.6 for h in hits)


if __name__ == "__main__":
    test_sem_min_score_mantem_todos_os_hits()
    test_min_score_corta_hits_fracos()
    print("OK")
