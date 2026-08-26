"""conftest.py — fixtures compartilhadas dos testes de framework/db.

Migra o BoF4 UMA vez por sessão (fixture bof4_migrated) em vez de cada teste re-migrar
~6k linhas — corta o passo de DB de ~2min para ~15s. Os testes que usam o fixture são
read-only sobre o banco; só o teste de idempotência re-migra (banco próprio).
"""
import json
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


@pytest.fixture(scope="session")
def synthetic_migrated(tmp_path_factory):
    """(root, db_path, result) — projeto SINTETICO minimo (todo tipo de artefato de
    migrate_from_flat presente), migrado uma vez por sessão. Cobre scene_lines/translations/
    back_translations, que o BoF4 real não tem mais versionado (purga de dado do cliente —
    ver CLAUDE.md/ADR). Não substitui bof4_migrated: esse fixture continua apontando pro BoF4
    real porque test_db_sources_match_flat_for_deterministic_fields lê os flats reais direto."""
    from migrate_from_flat import migrate
    root = tmp_path_factory.mktemp("synproj")
    (root / "project.json").write_text(json.dumps({"title": "Synthetic"}), encoding="utf-8")
    art = root / "artifacts"
    (art / "state").mkdir(parents=True)
    (art / "run_state.json").write_text(
        json.dumps({"scenes": {"s1": {"status": "translated", "n_lines": 2}}}), encoding="utf-8")
    (art / "glossary.csv").write_text(
        "term,category,target_translation,handling_rule,aliases\n"
        "Widget,item,Bugiganga,traduzir,\n", encoding="utf-8")
    (art / "entities.csv").write_text(
        "name,canonical_pt,entity_type\nHero,Heroi,character\n", encoding="utf-8")
    (art / "state" / "voice_cards.json").write_text(
        json.dumps({"Hero": {"aliases": [], "lines": ["Hi"], "criticality": "medium"}}),
        encoding="utf-8")
    (art / "universe_knowledge_base.md").write_text(
        "## Mundo\nUm mundo sintetico de teste.\n", encoding="utf-8")
    (art / "api_ledger.jsonl").write_text(
        json.dumps({"scene": "s1", "kind": "translate", "model": "m",
                    "usage": {"in": 10, "out": 5}, "cost_usd": 0.01}) + "\n", encoding="utf-8")
    (art / "metrics.jsonl").write_text(
        json.dumps({"scene": "s1", "n_lines": 2}) + "\n", encoding="utf-8")
    (art / "warnings.jsonl").write_text(
        json.dumps({"t": 1.0, "source": "x", "warnings": ["w"]}) + "\n", encoding="utf-8")
    (art / "qa_effectiveness.jsonl").write_text(
        json.dumps({"t": 1.0, "note": "ok"}) + "\n", encoding="utf-8")
    sc = art / "scenes" / "s1"
    sc.mkdir(parents=True)
    (sc / "dialogs.csv").write_text(
        "offset,text_source,byte_budget\n"
        "0x1,Hero picks up the Widget.,60\n"
        "0x2,Hero says hello.,60\n", encoding="utf-8")
    (sc / "approved_a.csv").write_text(
        "offset,text_target\n"
        "0x1,O heroi pega a Bugiganga.\n"
        "0x2,[14]Ola[01]tudo bem?\n", encoding="utf-8")
    (sc / "back_translation_a.json").write_text(
        json.dumps({"entries": [{"offset": "0x1", "back": "The hero picks up the Widget."}]}),
        encoding="utf-8")
    db = tmp_path_factory.mktemp("syndb") / "syn.db"
    result = migrate(root, db, project_id="syn")
    return root, db, result
