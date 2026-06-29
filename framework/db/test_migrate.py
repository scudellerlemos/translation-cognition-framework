"""test_migrate.py — contrato da migração flat-files → SQLite.

Guarda regressões de "silent-zero" (migração importando 0 de um artefato que existe, por
mismatch de coluna/path) e garante que o banco bate com o que a migração reporta. Usa o
fixture `bof4_migrated` (migração única por sessão); só o teste de idempotência re-migra.
Usa só stdlib — roda em CI sem deps de ML.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

from migrate_from_flat import migrate  # noqa: E402
from store import Store  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def test_migrate_bof4_imports_all_present_artifacts(bof4_migrated):
    """> 0 em cada tipo de artefato que o BoF4 TEM versionado. (decisions/spoiler estão
    vazios — decision_index=[], ledger sem entries — então só checa as chaves presentes.)"""
    _db, result = bof4_migrated
    assert result["scenes"] > 0, result
    assert result["scene_lines"] > 0, "dialogs.csv por cena existe mas scene_lines importou 0"
    assert result["translations"] > 0, result
    assert result["glossary"] > 0, "glossary.csv existe mas importou 0 — mismatch de coluna?"
    assert result["entities"] > 0, "entities.csv existe mas importou 0 — mismatch de coluna?"
    assert result["voice_cards"] > 0, "voice_cards.json existe (artifacts/state/) mas importou 0 — path errado?"
    assert result["jobs"] > 0, result
    assert "decisions" in result and "spoiler" in result, result


def test_migrate_counts_roundtrip_to_store(bof4_migrated):
    db_path, result = bof4_migrated
    with Store(db_path) as db:
        summary = db.summary("bof4")
    assert summary["scenes"] == result["scenes"], (summary, result)
    assert summary["scene_lines"] == result["scene_lines"], (summary, result)
    assert summary["translations"] == result["translations"], (summary, result)
    assert summary["tm_approved"] == result["approved"], (summary, result)
    assert summary["glossary"] == result["glossary"], (summary, result)
    assert summary["entities"] == result["entities"], (summary, result)
    assert summary["voice_cards"] == result["voice_cards"], (summary, result)
    assert summary["decisions"] == result["decisions"], (summary, result)
    assert summary["spoiler"] == result["spoiler"], (summary, result)


def test_migrate_glossary_lossless(bof4_migrated):
    """O glossário no DB preserva aliases/category (que o context_pack usa/renderiza)."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        g = db.get_glossary("bof4")
    assert g, "glossary vazio"
    assert any(r.get("category") for r in g), "category não migrou (regressão lossy)"
    assert any(r.get("aliases") for r in g), "aliases não migrou (regressão lossy)"


def test_migrate_voice_cards_keep_lines(bof4_migrated):
    """Voice cards preservam o formato do context_pack (aliases + lines)."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        vc = db.get_voice_cards("bof4")
    assert vc, "voice_cards vazio"
    assert any(c.get("lines") for c in vc), "lines não migraram (formato context_pack perdido)"


def test_migrate_idempotent(tmp_path):
    """Rodar a migração 2x no mesmo banco não duplica (upsert, não insert)."""
    db_path = tmp_path / "t.db"
    first = migrate(BOF4, db_path, project_id="bof4")
    migrate(BOF4, db_path, project_id="bof4")
    with Store(db_path) as db:
        summary = db.summary("bof4")
    assert summary["translations"] == first["translations"], (summary, first)
    assert summary["tm_approved"] == first["approved"], (summary, first)
    assert summary["scene_lines"] == first["scene_lines"], (summary, first)


def test_migrate_translations_have_content(bof4_migrated):
    """REGRESSÃO: translations migravam com source/target VAZIOS (o approved_*.csv só tem
    offset,text_target — não tem as colunas lidas). Agora o conteúdo vem do translation_plan."""
    db_path, _ = bof4_migrated
    with Store(db_path) as db:
        tm = db.get_translations("bof4", approved_only=False)
    assert tm, "translations vazio"
    empty = [t for t in tm if not (t.get("source") and t.get("target"))]
    assert not empty, f"{len(empty)}/{len(tm)} translations com source/target vazio"
