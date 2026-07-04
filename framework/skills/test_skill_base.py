"""test_skill_base.py — cobre o contrato comum (Skill): gate de required_inputs e __repr__."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from skill_base import Skill  # noqa: E402


class _DummySkill(Skill):
    skill_id = "99"
    name = "Dummy"

    @property
    def required_inputs(self) -> list[str]:
        return ["artifacts/dialogs.csv"]

    def run(self, project: Path, **kwargs) -> dict:
        return {"status": "ok", "artifacts": []}


def test_check_inputs_flags_missing_required_artifact(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({"title": "T"}), encoding="utf-8")
    skill = _DummySkill()
    problems = skill.check_inputs(tmp_path)
    assert problems == ["artefato obrigatório ausente: artifacts/dialogs.csv"]


def test_check_inputs_passes_with_required_artifact_present(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({"title": "T"}), encoding="utf-8")
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "dialogs.csv").write_text("x", encoding="utf-8")
    skill = _DummySkill()
    assert skill.check_inputs(tmp_path) == []


def test_repr():
    assert repr(_DummySkill()) == "<Skill 99: Dummy>"
