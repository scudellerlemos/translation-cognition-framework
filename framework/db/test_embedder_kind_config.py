"""test_embedder_kind_config.py — contrato de _KIND_CONFIG (#169).

embedder.py só importa sentence-transformers/sqlite-vec DENTRO das funções que precisam (lazy),
então _KIND_CONFIG é inspecionável sem as deps de ML instaladas — roda em CI (STACK.md: o
retriever semântico é opt-in, mas essa checagem de config não depende dele).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from embedder import _KIND_CONFIG  # noqa: E402

_SCHEMA = (HERE / "schema.sql").read_text(encoding="utf-8")


def test_kb_kind_registered_without_chunk_fn():
    """kb reaproveita a MESMA estrutura de translation/decision (#169: sem chunk_fn no
    embedder — a KB já chega pré-chunkada por seção na ingestão, ver migrate_from_flat)."""
    assert "kb" in _KIND_CONFIG
    assert set(_KIND_CONFIG["kb"]) == set(_KIND_CONFIG["translation"])
    assert "chunk_fn" not in _KIND_CONFIG["kb"]
    assert _KIND_CONFIG["kb"]["table"] == "kb"
    assert _KIND_CONFIG["kb"]["text_col"] == "content"


def test_kb_embeddings_table_exists_in_schema():
    """kb_vectors (vec0) é criada em runtime por embedder.py; kb_embeddings (metadados) tem
    que existir no schema estático, senão index_project(kind="kb") falha no INSERT."""
    c = _KIND_CONFIG["kb"]
    assert re.search(rf"CREATE TABLE IF NOT EXISTS {c['emb_table']}", _SCHEMA)
    assert re.search(rf"{c['id_col']}\s+INTEGER PRIMARY KEY REFERENCES kb\(id\)", _SCHEMA)


def test_all_kinds_share_the_same_key_shape():
    """Todo kind novo tem que caber na indexação genérica (index_project/_ensure_vec_table) sem
    branch especial — se um kind precisar de uma chave a mais, o generalizador quebrou."""
    shapes = {kind: set(cfg) for kind, cfg in _KIND_CONFIG.items()}
    assert len(set(map(frozenset, shapes.values()))) == 1, shapes


if __name__ == "__main__":
    test_kb_kind_registered_without_chunk_fn()
    test_kb_embeddings_table_exists_in_schema()
    test_all_kinds_share_the_same_key_shape()
    print("ok")
