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


def test_index_and_search_kb_end_to_end(tmp_path):
    """#169 smoke test com Embedder/sqlite-vec REAIS -- só roda se a stack ML estiver
    instalada (requirements-ml.txt); skip limpo em test.yml (push/PR, mesmo padrão de
    test_load_kb_semantic_respects_reveal_gate em framework/runtime/test_context_pack.py), mas
    roda de verdade semanalmente em ml-coverage-optional.yml (#181)."""
    import pytest
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from embedder import Embedder
    from store import Store

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        db.upsert_kb("p", [
            {"section": "Dragão do Vento", "content": "guardião ancestral dos ares", "reveal": "safe"},
            {"section": "Receitas de cozinha", "content": "como fazer bolo de fubá", "reveal": "safe"},
        ])
        emb = Embedder()
        n = emb.index_project(db._con, project_id="p", kind="kb")
        assert n == 2
        hits = emb.search_kb(db._con, "quem é o guardião ancestral dos ares?", project_id="p", k=2)
        assert hits[0]["section"] == "Dragão do Vento"          # top-1 tem que ser o relevante
        assert hits[0]["score"] > hits[1]["score"]


def test_search_filters_project_before_top_k(tmp_path):
    """k do vec0 era aplicado na tabela inteira ANTES do filtro de projeto/aprovado: vizinhos de
    outro projeto ocupavam o top-k e a busca devolvia < k hits. Encode falso (só sqlite-vec)."""
    import pytest
    pytest.importorskip("sqlite_vec")
    from embedder import _DIM, Embedder
    from store import Store

    emb = Embedder.__new__(Embedder)
    emb.model_name = "fake"
    emb.encode = lambda texts: [[1.0 if t.startswith("a") else 0.0] + [0.0] * (_DIM - 1)
                                for t in texts]
    with Store(tmp_path / "p.db") as db:
        for pid, text in (("near", "a1"), ("near", "a2"), ("far", "b1"), ("far", "b2")):
            db.upsert_project(pid, pid)
            db.upsert_decision(pid, text, summary=text)
        emb.index_project(db._con, project_id="near", kind="decision")
        emb.index_project(db._con, project_id="far", kind="decision")
        # query "a" é mais próxima dos vetores de "near"; k=2 em "far" tem que achar os 2 de "far"
        hits = emb.search_decisions(db._con, "a", project_id="far", k=2)
        assert sorted(h["title"] for h in hits) == ["b1", "b2"]
        # linha editada: reindex troca o vetor (antes ficava o velho)
        db.upsert_decision("far", "b1", summary="a-editado")
        # antes do reindex: sem emb row -> fora da busca (nao ranqueia pelo vetor velho)
        assert [h["title"] for h in emb.search_decisions(db._con, "a", project_id="far", k=2)] == ["b2"]
        assert emb.index_project(db._con, project_id="far", kind="decision") == 1
        assert emb.search_decisions(db._con, "a", project_id="far", k=1)[0]["title"] == "b1"


def test_search_max_score_excludes_exact_before_top_k(tmp_path):
    """Fala curta ("Yes.") com >=k matches exatos: o exato ocupava o top-k e o vizinho real sumia.
    max_score corta no SQL, antes do LIMIT. Encode falso (só sqlite-vec)."""
    import pytest
    pytest.importorskip("sqlite_vec")
    from embedder import _DIM, Embedder
    from store import Store

    emb = Embedder.__new__(Embedder)
    emb.model_name = "fake"
    vecs = {"Yes.": [1.0, 0.0], "Yes?": [0.6, 0.8], "Yes~": [0.99897, (1 - 0.99897 ** 2) ** 0.5]}
    emb.encode = lambda texts: [vecs.get(t, [0.8, 0.6]) + [0.0] * (_DIM - 2) for t in texts]
    emb._rerank = lambda q, hits: hits
    with Store(tmp_path / "p.db") as db:
        db.upsert_project("p", "p")
        for i, src in enumerate(["Yes.", "Yes.", "Yes.", "Yes!"]):
            db.upsert_translation("p", "s", str(i), src, target=f"Sim{i}", approved=True)
        emb.index_project(db._con, project_id="p")
        assert [h["source"] for h in emb.search(db._con, "Yes.", project_id="p", k=1)] == ["Yes."]
        hits = emb.search(db._con, "Yes.", project_id="p", k=1, max_score=0.999)
        assert [h["source"] for h in hits] == ["Yes!"]
        # fronteira: cortes no score CRU (0.99897 < 0.999 fica, exibido arredondado 0.999; min idem)
        db.upsert_translation("p", "s", "8", "Yes~", target="Sim~", approved=True)
        emb.index_project(db._con, project_id="p")
        hits = emb.search(db._con, "Yes.", project_id="p", k=1, max_score=0.999)
        assert [(h["source"], h["score"]) for h in hits] == [("Yes~", 0.999)]
        # min_score no cru: 0.99897 < 0.999 sai (no arredondado 0.999 passava)
        assert "Yes~" not in {h["source"] for h in emb.search(db._con, "Yes.", project_id="p", k=9, min_score=0.999)}
        # mesmo par (source, target) em N cenas ocupa 1 slot, nao N
        for sc in ("s2", "s3"):
            db.upsert_translation("p", sc, "9", "Yes!", target="Sim3", approved=True)
        db.upsert_translation("p", "s", "5", "Yes?", target="Sim?", approved=True)
        emb.index_project(db._con, project_id="p")
        hits = emb.search(db._con, "Yes.", project_id="p", k=3, max_score=0.999)
        assert sorted(h["source"] for h in hits) == ["Yes!", "Yes?", "Yes~"]
        # >1 = sem corte superior: o exato fica (nem complex no bind, nem clamp que corta L2=0)
        assert emb.search(db._con, "Yes.", project_id="p", k=1, max_score=1.5)[0]["source"] == "Yes."


if __name__ == "__main__":
    test_kb_kind_registered_without_chunk_fn()
    test_kb_embeddings_table_exists_in_schema()
    test_all_kinds_share_the_same_key_shape()
    print("ok")
