"""conftest.py — fixtures compartilhadas dos testes de framework/db.

Migra o BoF4 UMA vez por sessão (fixture bof4_migrated) em vez de cada teste re-migrar
~6k linhas — corta o passo de DB de ~2min para ~15s. Os testes que usam o fixture são
read-only sobre o banco; só o teste de idempotência re-migra (banco próprio).
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

BOF4 = ROOT / "projects" / "breath_of_fire_4"


@pytest.fixture(scope="session")
def bof4_migrated(tmp_path_factory):
    """(db_path, result) — BoF4 migrado uma vez para um SQLite temporário da sessão."""
    from migrate_from_flat import migrate
    db = tmp_path_factory.mktemp("bof4db") / "bof4.db"
    result = migrate(BOF4, db, project_id="bof4")
    return db, result
