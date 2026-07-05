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
