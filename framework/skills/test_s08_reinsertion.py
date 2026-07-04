"""test_s08_reinsertion.py — cobre o sandbox contra path traversal (#87): s08_reinsertion deve
reusar connector_mgr._connector_script(), a mesma validacao ja aplicada por run_scene/connector_mgr,
em vez de concatenar project/reinsert_script diretamente."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import s08_reinsertion as s08  # noqa: E402
from s08_reinsertion import ReinsertionSkill  # noqa: E402


def _write_project(tmp_path, reinsert_script):
    (tmp_path / "project.json").write_text(json.dumps(
        {"connector": {"reinsert_script": reinsert_script}}), encoding="utf-8")


def test_check_inputs_rejects_path_traversal(tmp_path):
    _write_project(tmp_path, "../../../evil.py")
    skill = ReinsertionSkill()
    problems = skill.check_inputs(tmp_path)
    assert problems
    assert "fora do projeto" in problems[0]


def test_run_rejects_path_traversal_without_subprocess(tmp_path):
    _write_project(tmp_path, "../../../evil.py")
    skill = ReinsertionSkill()
    result = skill.run(tmp_path)
    assert result["status"] == "error"
    assert "fora do projeto" in "".join(result.get("problems", [])) + result.get("error", "")


def test_check_inputs_accepts_valid_script(tmp_path):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("pass", encoding="utf-8")
    _write_project(tmp_path, "connector/reinsert.py")
    skill = ReinsertionSkill()
    assert skill.check_inputs(tmp_path) == []


def test_check_inputs_rejects_missing_project_json(tmp_path):
    skill = ReinsertionSkill()
    problems = skill.check_inputs(tmp_path)
    assert problems == ["project.json não encontrado"]


def test_check_inputs_rejects_missing_reinsert_script_file(tmp_path):
    _write_project(tmp_path, "connector/reinsert.py")  # declarado mas nunca criado
    skill = ReinsertionSkill()
    problems = skill.check_inputs(tmp_path)
    assert any("não encontrado" in p for p in problems)


def test_run_timeout(tmp_path, monkeypatch):
    _write_project(tmp_path, "connector/reinsert.py")
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("pass", encoding="utf-8")

    def _boom(*a, **k):
        import subprocess
        raise subprocess.TimeoutExpired(cmd="x", timeout=600)
    monkeypatch.setattr(s08.subprocess, "run", _boom)
    result = ReinsertionSkill().run(tmp_path)
    assert result["status"] == "error" and "timeout" in result["error"].lower()


def test_run_reports_generic_spawn_failure(tmp_path, monkeypatch):
    _write_project(tmp_path, "connector/reinsert.py")
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("pass", encoding="utf-8")

    def _boom(*a, **k):
        raise OSError("spawn falhou")
    monkeypatch.setattr(s08.subprocess, "run", _boom)
    result = ReinsertionSkill().run(tmp_path)
    assert result["status"] == "error" and "spawn falhou" in result["error"]
