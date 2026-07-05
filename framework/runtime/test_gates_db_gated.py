"""test_gates_db_gated.py — #85: gates de governança sob projeto DB-gated.

spoiler_check.py, glossary_lint.py e o check de glossário do kb_gate.py liam SEMPRE os flat
files (paths.spoiler_ledger/dialogs.csv/glossary.csv), mesmo em projeto com `db` populado —
divergência silenciosa entre o que o gate validava e a fonte real de verdade. Este teste
constrói um projeto DB-only mínimo (sem artifacts/scenes/ em disco) e prova que os 3 gates
enxergam os dados via SQLite em vez de reportar 'limpo'/'sem candidatos' por não achar nada.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
_DB_DIR = str(_HERE.parent / "db")
if _DB_DIR not in sys.path:
    sys.path.insert(0, _DB_DIR)

import context_pack  # noqa: E402
import glossary_lint  # noqa: E402
import kb_gate  # noqa: E402
import spoiler_check as sc  # noqa: E402
from store import Store  # noqa: E402


def _db_project(tmp_path) -> Path:
    db_path = tmp_path / "t.db"
    (tmp_path / "project.json").write_text(json.dumps({
        "title": "T", "media_type": "game",
        "db": {"path": "t.db", "project_id": "p1"},
    }), encoding="utf-8")
    return db_path


def test_spoiler_check_db_gated_detects_leak(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_translation(project_id="p1", scene_id="11_01", offset="X:0:1",
                               source="He appears", target="O Oshtor aparece na porta.")
        db.upsert_spoiler_entry(project_id="p1", entity="Oshtor", reveal="13_08",
                                forbidden_pre_reveal=["Oshtor"])
    leaks = sc.check(tmp_path)
    assert leaks and leaks[0]["forbidden"] == "Oshtor" and leaks[0]["scene_id"] == "11_01"


def test_spoiler_check_db_gated_no_leak_after_reveal(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_translation(project_id="p1", scene_id="14_01", offset="X:0:1",
                               source="He appears", target="O Oshtor aparece.")
        db.upsert_spoiler_entry(project_id="p1", entity="Oshtor", reveal="13_08",
                                forbidden_pre_reveal=["Oshtor"])
    assert sc.check(tmp_path) == []


def test_spoiler_check_db_gated_gender_flag(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_translation(project_id="p1", scene_id="11_01", offset="X:0:1",
                               source="She is Kuon", target="Ela e a Kuon disfarcada.")
        db.upsert_spoiler_entry(project_id="p1", entity="Oshtor", reveal="13_08",
                                gender_quarantine=True, triggers=["Kuon"])
    flags = sc.check_gender(tmp_path)
    assert flags and flags[0]["marker"] == "ela"


def test_glossary_lint_db_gated_finds_inconsistency(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_glossary(project_id="p1", term="Warmaster", translation="Mestre de Guerra",
                           handling_rule="traduzir")
        db.upsert_translation(project_id="p1", scene_id="ch1", offset="0x2",
                              source="The Warmaster arrived.", target="O comandante chegou.")
    found = glossary_lint.lint(tmp_path)
    assert found and found[0]["term"] == "Warmaster"


def test_glossary_lint_db_gated_canonical_form_present_is_clean(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_glossary(project_id="p1", term="Warmaster", translation="Mestre de Guerra",
                           handling_rule="traduzir")
        db.upsert_translation(project_id="p1", scene_id="ch1", offset="0x2",
                              source="The Warmaster arrived.", target="O Mestre de Guerra chegou.")
    assert glossary_lint.lint(tmp_path) == []


def test_kb_gate_db_gated_glossary_undated_flags_problem(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_glossary(project_id="p1", term="Kuon", translation="Kuon")
        db._con.execute("UPDATE glossary SET updated_at=NULL WHERE term='Kuon'")
        db._con.commit()
    r = kb_gate.check(tmp_path, "ch_11_01")
    assert any("updated_at" in p for p in r["problems"])


def test_kb_gate_db_gated_glossary_dated_no_updated_at_problem(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_glossary(project_id="p1", term="Kuon", translation="Kuon")
    r = kb_gate.check(tmp_path, "ch_11_01")
    assert not any("updated_at" in p for p in r["problems"])


def test_load_translated_scenes_db_gated_shape(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_translation(project_id="p1", scene_id="11_01", offset="X:0:1",
                              source="Hi", target="Oi")
    cfg = json.loads((tmp_path / "project.json").read_text(encoding="utf-8"))
    out = context_pack.load_translated_scenes(tmp_path, cfg)
    assert out == [("11_01", "11_01", {"X:0:1": {"source": "Hi", "target": "Oi"}})]


def test_load_spoiler_ledger_db_gated_carries_new_fields(tmp_path):
    db_path = _db_project(tmp_path)
    with Store(db_path) as db:
        db.upsert_project("p1", "T")
        db.upsert_spoiler_entry(project_id="p1", entity="Oshtor", reveal="13_08",
                                forbidden_pre_reveal=["Oshtor"], gender_quarantine=True)
    cfg = json.loads((tmp_path / "project.json").read_text(encoding="utf-8"))
    ledger = context_pack.load_spoiler_ledger(tmp_path, cfg)
    e = ledger["entries"][0]
    assert e["forbidden_pre_reveal"] == ["Oshtor"] and e["gender_quarantine"] is True
