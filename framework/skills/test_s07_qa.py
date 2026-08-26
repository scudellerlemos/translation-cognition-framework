"""test_s07_qa.py — cobre o wrapper de skill em torno de quality_gate.check: gate de
entrada (project.json/scenes ausentes) e status ok/blocked conforme revise/uncovered.
Mocka quality_gate.check (unidade isolada) -- sem depender de nenhum corpus real."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
for _p in (str(_HERE), str(_RUNTIME)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from s07_qa import QaSkill  # noqa: E402


def _write_project(tmp_path, with_scenes=True):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    if with_scenes:
        (tmp_path / "artifacts" / "scenes").mkdir(parents=True)


def test_check_inputs_rejects_missing_project_json(tmp_path):
    problems = QaSkill().check_inputs(tmp_path)
    assert problems == ["project.json não encontrado"]


def test_check_inputs_rejects_missing_scenes_dir(tmp_path):
    _write_project(tmp_path, with_scenes=False)
    problems = QaSkill().check_inputs(tmp_path)
    assert any("scenes" in p for p in problems)


def test_run_reports_error_when_inputs_missing(tmp_path):
    result = QaSkill().run(tmp_path)
    assert result["status"] == "error"
    assert result["artifacts"] == []


def test_run_ok_when_gate_clean(tmp_path, monkeypatch):
    _write_project(tmp_path)
    fake_gate = type("M", (), {
        "check": staticmethod(lambda root, chapter: {
            "revise": [], "uncovered": [], "coverage": {"lines": 3, "pct": 100},
        })})
    monkeypatch.setitem(sys.modules, "quality_gate", fake_gate)
    result = QaSkill().run(tmp_path, chapter="19")
    assert result["status"] == "ok"
    assert result["revise"] == 0 and result["uncovered"] == 0


def test_run_blocked_when_gate_finds_issues(tmp_path, monkeypatch):
    _write_project(tmp_path)
    fake_gate = type("M", (), {
        "check": staticmethod(lambda root, chapter: {
            "revise": [{"offset": "0x1"}], "uncovered": [{"offset": "0x2"}, {"offset": "0x3"}],
            "coverage": {"lines": 3, "pct": 33.3},
        })})
    monkeypatch.setitem(sys.modules, "quality_gate", fake_gate)
    result = QaSkill().run(tmp_path)
    assert result["status"] == "blocked"
    assert result["revise"] == 1 and result["uncovered"] == 2
    assert result["coverage"]["pct"] == 33.3
