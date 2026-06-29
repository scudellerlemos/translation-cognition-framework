"""test_migrate.py — contrato da migração flat-files → SQLite.

Guarda a regressão do "silent-zero": a migração importava 0 linhas de
glossary/entities por mismatch de nome de coluna (o BoF4 usa `target_translation`
e `canonical_name`, não `translation`/`name`). Esses testes falham se a migração
voltar a descartar silenciosamente um tipo de artefato que existe no projeto.

Usa só stdlib (sqlite/csv/json via store.py) — roda em CI sem as deps de ML.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # framework/db → framework → raiz do repo
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "framework" / "runtime"))

from migrate_from_flat import migrate  # noqa: E402
from store import Store  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def test_migrate_bof4_imports_all_present_artifacts(tmp_path):
    """Migra o BoF4 e exige > 0 em cada tipo de artefato que o projeto TEM versionado.

    (scenes/translations/glossary/entities/jobs existem; voice_cards não — BoF4 guarda
    voz em .md, então fica de fora propositalmente.)
    """
    result = migrate(BOF4, tmp_path / "t.db", project_id="bof4")
    assert result["scenes"] > 0, result
    assert result["translations"] > 0, result
    assert result["glossary"] > 0, "glossary.csv existe mas importou 0 — mismatch de coluna?"
    assert result["entities"] > 0, "entities.csv existe mas importou 0 — mismatch de coluna?"
    assert result["jobs"] > 0, result


def test_migrate_counts_roundtrip_to_store(tmp_path):
    """As contagens reportadas pela migração batem com o que o banco devolve."""
    result = migrate(BOF4, tmp_path / "t.db", project_id="bof4")
    with Store(tmp_path / "t.db") as db:
        summary = db.summary("bof4")
    assert summary["scenes"] == result["scenes"], (summary, result)
    assert summary["tm_approved"] == result["translations"], (summary, result)


def test_migrate_idempotent(tmp_path):
    """Rodar a migração duas vezes no mesmo banco não duplica (upsert, não insert)."""
    db_path = tmp_path / "t.db"
    first = migrate(BOF4, db_path, project_id="bof4")
    migrate(BOF4, db_path, project_id="bof4")
    with Store(db_path) as db:
        summary = db.summary("bof4")
    assert summary["tm_approved"] == first["translations"], (summary, first)
