"""test_spoiler_check.py — cobre a verificação pós-tradução de vazamento de spoiler.

check (nome/título proibido pré-reveal), check_gender (marcador de gênero pt-BR junto à entidade
em quarentena), list_guards e _future. Constrói um projeto com spoiler_ledger + translations por cena.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
import spoiler_check as sc  # noqa: E402


def _scene(root: Path, scene: str, t: str):
    sid = context_pack.scene_id_of(scene)
    sd = paths.scene_dir(root, scene)
    sd.mkdir(parents=True, exist_ok=True)
    (sd / "dialogs.csv").write_text("offset,text_source\nX:0:1,He appears\n", encoding="utf-8")
    paths.translations(root, scene, sid).write_text(
        json.dumps({"lines": {"X:0:1": {"t": t}}}), encoding="utf-8")
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")


def _ledger(root: Path, **entry):
    entry.setdefault("entity", "Oshtor")
    entry.setdefault("reveal", "13_08")
    paths.spoiler_ledger(root).write_text(json.dumps({"entries": [entry]}), encoding="utf-8")


def test_detects_name_leak_pre_reveal(tmp_path):
    _scene(tmp_path, "ch_11_01", "O Oshtor aparece na porta.")   # 11_01 < reveal 13_08
    _ledger(tmp_path, forbidden_pre_reveal=["Oshtor"])
    leaks = sc.check(tmp_path)
    assert leaks and leaks[0]["forbidden"] == "Oshtor" and leaks[0]["scene_id"] == "11_01"


def test_no_leak_after_reveal(tmp_path):
    _scene(tmp_path, "ch_14_01", "O Oshtor aparece.")            # 14 > reveal 13_08 -> seguro
    _ledger(tmp_path, forbidden_pre_reveal=["Oshtor"])
    assert sc.check(tmp_path) == []


def test_check_no_ledger_is_empty(tmp_path):
    _scene(tmp_path, "ch_11_01", "texto qualquer")
    assert sc.check(tmp_path) == []                              # sem spoiler_ledger.json


def test_check_no_forbidden_strings_is_empty(tmp_path):
    _scene(tmp_path, "ch_11_01", "O Oshtor aparece.")
    _ledger(tmp_path)                                           # sem forbidden_pre_reveal
    assert sc.check(tmp_path) == []


def test_check_gender_flags_marker_near_entity(tmp_path):
    _scene(tmp_path, "ch_11_01", "Ela é a Kuon disfarçada.")
    _ledger(tmp_path, gender_quarantine=True, triggers=["Kuon"])
    flags = sc.check_gender(tmp_path)
    assert flags and flags[0]["marker"] == "ela" and flags[0]["entity"] == "Oshtor"


def test_list_guards(tmp_path):
    _scene(tmp_path, "ch_11_01", "x")
    _ledger(tmp_path, forbidden_pre_reveal=["Oshtor"], gender_quarantine=True, notes="twist central")
    g = sc.list_guards(tmp_path)
    assert g[0]["entity"] == "Oshtor" and g[0]["gender_quarantine"] is True
    assert g[0]["forbidden_pre_reveal"] == ["Oshtor"]


def test_future_helper():
    assert sc._future("beyond_frontier", "11_01") is True
    assert sc._future("13_08", "11_01") is True
    assert sc._future("11_01", "13_08") is False
