"""test_skills_run.py — cobre os caminhos run() das skills (subprocess/run_scene mockados).

s00 (extract) e s08 (reinsert) rodam scripts do conector via subprocess; s06 (translate) chama
run_scene. Aqui esses são stubados — testa sucesso, erro (returncode!=0), timeout e o gate.
"""
import json
import subprocess
import sys
import types
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import s00_extraction as s00  # noqa: E402
import s06_translation as s06  # noqa: E402
import s08_reinsertion as s08  # noqa: E402


def _proj(root: Path, key: str, script: str = "connector/x.py"):
    (root / "connector").mkdir(parents=True)
    (root / Path(script)).write_text("# dummy", encoding="utf-8")
    (root / "project.json").write_text(json.dumps(
        {"title": "T", "media_type": "game", "connector": {key: script},
         "source": {"file": "artifacts/dialogs.csv"}}), encoding="utf-8")


def _proc(returncode=0, stdout="ok", stderr=""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


# ------------------------------- s00 extract ----------------------------------

def test_s00_run_success(tmp_path, monkeypatch):
    _proj(tmp_path, "extract_script")
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hi\n", encoding="utf-8")
    monkeypatch.setattr(s00.subprocess, "run", lambda *a, **k: _proc())
    r = s00.ExtractionSkill().run(tmp_path, dat_dir="/fake/dat")
    assert r["status"] == "ok" and r["n_strings"] == 1


def test_s00_run_subprocess_error(tmp_path, monkeypatch):
    _proj(tmp_path, "extract_script")
    monkeypatch.setattr(s00.subprocess, "run", lambda *a, **k: _proc(returncode=2, stderr="boom"))
    r = s00.ExtractionSkill().run(tmp_path)
    assert r["status"] == "error" and r["returncode"] == 2


def test_s00_run_no_dialogs(tmp_path, monkeypatch):
    _proj(tmp_path, "extract_script")
    (tmp_path / "artifacts").mkdir()
    monkeypatch.setattr(s00.subprocess, "run", lambda *a, **k: _proc())     # sucesso mas sem dialogs.csv
    r = s00.ExtractionSkill().run(tmp_path)
    assert r["status"] == "error" and "dialogs.csv" in r["error"]


def test_s00_run_timeout(tmp_path, monkeypatch):
    _proj(tmp_path, "extract_script")

    def _boom(*a, **k):
        raise subprocess.TimeoutExpired(cmd="x", timeout=300)
    monkeypatch.setattr(s00.subprocess, "run", _boom)
    r = s00.ExtractionSkill().run(tmp_path)
    assert r["status"] == "error" and "timeout" in r["error"].lower()


def test_s00_gate_blocks_without_script(tmp_path):
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game","connector":{}}', encoding="utf-8")
    r = s00.ExtractionSkill().run(tmp_path)
    assert r["status"] == "error" and r["problems"]


# ------------------------------ s08 reinsert ----------------------------------

def test_s08_run_success(tmp_path, monkeypatch):
    _proj(tmp_path, "reinsert_script")
    (tmp_path / "output").mkdir()
    (tmp_path / "output" / "patch.ips").write_text("x", encoding="utf-8")
    monkeypatch.setattr(s08.subprocess, "run", lambda *a, **k: _proc())
    r = s08.ReinsertionSkill().run(tmp_path, dat_dir="/fake")
    assert r["status"] == "ok" and any("patch.ips" in a for a in r["artifacts"])


def test_s08_run_error(tmp_path, monkeypatch):
    _proj(tmp_path, "reinsert_script")
    monkeypatch.setattr(s08.subprocess, "run", lambda *a, **k: _proc(returncode=1, stderr="fail"))
    r = s08.ReinsertionSkill().run(tmp_path)
    assert r["status"] == "error" and r["returncode"] == 1


def test_s08_gate_blocks_without_script(tmp_path):
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game","connector":{}}', encoding="utf-8")
    r = s08.ReinsertionSkill().run(tmp_path)
    assert r["status"] == "error"


# ------------------------------ s06 translate ---------------------------------

def test_s06_run_delegates_to_run_scene(tmp_path, monkeypatch):
    (tmp_path / "artifacts" / "scenes").mkdir(parents=True)
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    called = {}

    def fake_run_scene(project, scene, **k):
        called["scene"] = scene
        called["backend"] = k.get("backend")
        return {"status": "verified", "scene": scene}

    import run_scene as rs
    monkeypatch.setattr(rs, "run_scene", fake_run_scene)
    r = s06.TranslationSkill().run(tmp_path, scene="AREAD001", backend="api")
    assert r["status"] == "verified" and called["scene"] == "AREAD001"
    assert "artifacts" in r                                   # normalizado


def test_s06_run_requires_scene(tmp_path):
    (tmp_path / "artifacts" / "scenes").mkdir(parents=True)
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    r = s06.TranslationSkill().run(tmp_path)                  # sem scene
    assert r["status"] == "error" and "scene" in str(r["problems"]).lower()
