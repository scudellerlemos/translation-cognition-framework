"""test_store.py — cobre Store diretamente (schema/migração aditiva de coluna, roundtrip).

#85: spoiler_entries ganhou forbidden_pre_reveal/gender_quarantine (colunas ausentes no schema
original — spoiler_check dependia delas mas o DB nunca as carregava). Este teste prova o
roundtrip via upsert/get e a migração idempotente (ALTER TABLE ADD COLUMN) para bancos criados
antes das colunas existirem. Só stdlib.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from store import Store  # noqa: E402


def test_spoiler_entry_roundtrip_new_fields(tmp_path):
    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        db.upsert_spoiler_entry(
            project_id="p1", entity="Oshtor", fact="e Ukon",
            reveal="13_08", forbidden_pre_reveal=["Oshtor"], gender_quarantine=True,
        )
        entries = db.get_spoiler_entries("p1")
    assert len(entries) == 1
    e = entries[0]
    assert e["forbidden_pre_reveal"] == ["Oshtor"]
    assert e["gender_quarantine"] is True


def test_batch_persists_all_writes_with_single_commit(tmp_path):
    """db.batch(): commits individuais de cada upsert_* viram 1 soh no fim do bloco, mas o
    resultado final e o MESMO de rodar sem batch -- todas as linhas persistem apos o `with`."""
    db_path = tmp_path / "t.db"
    with Store(db_path) as db, db.batch():
        db.upsert_project("p1", "Projeto Teste")
        for i in range(5):
            db.upsert_scene(project_id="p1", scene_id=f"S{i}", status="pending")
    with Store(db_path) as db:
        assert len(db.get_scenes("p1")) == 5


def test_batch_rolls_back_all_writes_on_error(tmp_path):
    """Excecao dentro do bloco -> rollback de TUDO que foi escrito ali (mesma garantia
    tudo-ou-nada que os commits individuais davam um passo por vez, so que em lote)."""
    import pytest

    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        with pytest.raises(RuntimeError):
            with db.batch():
                db.upsert_scene(project_id="p1", scene_id="S0", status="pending")
                raise RuntimeError("falha simulada no meio do lote")
        assert db.get_scenes("p1") == []


def test_spoiler_entry_new_fields_default_empty(tmp_path):
    """Entry sem os campos novos -> forbidden_pre_reveal=[] e gender_quarantine=False (não None/erro)."""
    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        db.upsert_spoiler_entry(project_id="p1", entity="Kuon", reveal="beyond_frontier")
        entries = db.get_spoiler_entries("p1")
    assert entries[0]["forbidden_pre_reveal"] == []
    assert entries[0]["gender_quarantine"] is False


def test_migrate_schema_adds_columns_to_preexisting_db(tmp_path):
    """Banco criado ANTES das colunas novas existirem no schema.sql -> _migrate_schema() as
    adiciona via ALTER TABLE (idempotente). Simula abrindo o mesmo arquivo 2x (2ª abertura
    não deve falhar nem duplicar coluna)."""
    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        db.upsert_spoiler_entry(project_id="p1", entity="X", gender_quarantine=True)
    # reabre o mesmo arquivo -- _migrate_schema roda de novo, deve ser no-op seguro
    with Store(db_path) as db2:
        cols = {r["name"] for r in db2._con.execute("PRAGMA table_info(spoiler_entries)").fetchall()}
        assert {"forbidden_pre_reveal", "gender_quarantine"} <= cols
        entries = db2.get_spoiler_entries("p1")
    assert entries[0]["gender_quarantine"] is True


def test_decision_reveal_roundtrip(tmp_path):
    """#105: upsert_decision/get_decisions preserva reveal (None por default -- default-deny)."""
    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        db.upsert_decision("p1", "Regra do dragão", summary="preservar nome", reveal="safe")
        db.upsert_decision("p1", "Trama pendente", summary="sem revisao ainda")
        decisions = {d["title"]: d for d in db.get_decisions("p1")}
    assert decisions["Regra do dragão"]["reveal"] == "safe"
    assert decisions["Trama pendente"]["reveal"] is None


def test_migrate_schema_adds_reveal_column_to_preexisting_decisions(tmp_path):
    """Banco criado ANTES de decisions.reveal existir no schema.sql -> ALTER TABLE aditivo,
    mesmo padrão de test_migrate_schema_adds_columns_to_preexisting_db. Remove a coluna e
    FECHA a conexão -- _migrate_schema só roda de novo na PRÓXIMA abertura (__init__)."""
    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        db._con.execute("ALTER TABLE decisions DROP COLUMN reveal")
        db._con.commit()
    # reabre -- _migrate_schema roda de novo e re-adiciona a coluna removida
    with Store(db_path) as db2:
        cols = {r["name"] for r in db2._con.execute("PRAGMA table_info(decisions)").fetchall()}
        assert "reveal" in cols
        db2.upsert_decision("p1", "Sem reveal ainda", summary="x")
        decisions = db2.get_decisions("p1")
    assert decisions[0]["reveal"] is None


def test_reindex_pending_embeddings_never_raises(tmp_path, monkeypatch):
    """#171: uma falha de embedding (extensão nativa incompatível, hardware ROCm indisponível,
    etc. — qualquer coisa além de ImportError) nunca pode derrubar o write-path. Embedding é
    busca semântica opcional sobre dados já persistidos em SQL; regressão real encontrada ao
    conectar reindex_pending_embeddings no migrate() (a exceção só era pega se ImportError)."""
    import types
    fake_embedder = types.ModuleType("embedder")

    class BoomEmbedder:
        def __init__(self):
            raise RuntimeError("falha nativa simulada (nao-ImportError)")

    fake_embedder.Embedder = BoomEmbedder
    monkeypatch.setitem(sys.modules, "embedder", fake_embedder)

    db_path = tmp_path / "t.db"
    with Store(db_path) as db:
        db.upsert_project("p1", "Projeto Teste")
        result = db.reindex_pending_embeddings("p1")
    assert result is None


def test_upsert_translation_reupsert_updates_source(tmp_path):
    """Re-upsert do mesmo (project, scene, offset) com source novo (ex.: extract re-rodado com texto
    corrigido) tem que trocar o source -- senao TM exata e embeddings ficam pareados ao texto velho."""
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("p1", "P")
        db.upsert_translation("p1", "s1", "0x1", source="Hello", target="Ola", approved=True)
        db.upsert_translation("p1", "s1", "0x1", source="Hello there", target="Ola ai", approved=True)
        assert db.search_tm_exact("Hello", "p1") == []
        hit = db.search_tm_exact("Hello there", "p1")
    assert [h["target"] for h in hit] == ["Ola ai"]


def test_source_change_drops_embedding_metadata(tmp_path):
    """Trigger: mudar translations.source apaga o metadado de embedding (o reindex refaz o vetor)."""
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("p1", "P")
        db.upsert_translation("p1", "s1", "0x1", source="Hello", target="Ola", approved=True)
        tid = db._con.execute("SELECT id FROM translations").fetchone()[0]
        db._con.execute("INSERT INTO tm_embeddings(translation_id, model_name, dim) VALUES(?,?,?)",
                        (tid, "m", 384))
        # mesmo source: metadado permanece
        db.upsert_translation("p1", "s1", "0x1", source="Hello", target="Oi", approved=True)
        assert db._con.execute("SELECT count(*) FROM tm_embeddings").fetchone()[0] == 1
        # source novo: metadado some
        db.upsert_translation("p1", "s1", "0x1", source="Bye", target="Tchau", approved=True)
        assert db._con.execute("SELECT count(*) FROM tm_embeddings").fetchone()[0] == 0


def test_upsert_translation_empty_source_keeps_existing_source(tmp_path):
    """Caller sem source (migrate_from_flat / sync_translations_db sem plan) nao pode apagar o source bom."""
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("p1", "P")
        db.upsert_translation("p1", "s1", "0x1", source="Hello", target="Ola", approved=True)
        db.upsert_translation("p1", "s1", "0x1", source="", target="Oi", approved=True)
        hit = db.search_tm_exact("Hello", "p1")
    assert [h["target"] for h in hit] == ["Oi"]


def test_upsert_entity_reupsert_updates_first_scene_and_notes(tmp_path):
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("a", "A")
        db.upsert_entity("a", "Ryu", canonical_pt="Ryu")
        db.upsert_entity("a", "Ryu", first_scene="ch_02", notes="protagonista")
        db.upsert_entity("a", "Ryu", canonical_pt="Ryu")     # None nao pode apagar o que ja existe
        e = db.get_entities("a")[0]
    assert e["first_scene"] == "ch_02" and e["notes"] == "protagonista"


def test_upserts_with_null_key_columns_are_idempotent(tmp_path):
    """NULL em coluna de chave UNIQUE conta como distinto no SQLite: fact/source ausentes duplicavam a cada re-migracao."""
    with Store(tmp_path / "t.db") as db:
        db.upsert_project("p1", "Projeto Teste")
        for _ in range(2):
            db.upsert_spoiler_entry(project_id="p1", entity="Kuon", reveal="beyond_frontier")
            db.upsert_warnings("p1", [{"t": 1.0, "warnings": ["w"]}])
            db.upsert_qa_effectiveness("p1", [{"t": 1.0, "applied": 1}])
        assert len(db.get_spoiler_entries("p1")) == 1
        assert len(db.get_warnings("p1")) == 1
        assert db._con.execute("SELECT COUNT(*) FROM qa_effectiveness").fetchone()[0] == 1
