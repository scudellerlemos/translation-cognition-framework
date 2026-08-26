"""test_s06_translation.py — cobre o gate de entrada e os retornos de erro precoces do
wrapper de skill (sem invocar run_scene de verdade -- essa parte e cognitiva/precisa de
backend). Sem depender de nenhum corpus real."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
for _p in (str(_HERE), str(_RUNTIME)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from s06_translation import TranslationSkill  # noqa: E402


def test_check_inputs_rejects_missing_project_json(tmp_path):
    problems = TranslationSkill().check_inputs(tmp_path)
    assert problems == ["project.json não encontrado"]


def test_check_inputs_rejects_missing_scenes_dir(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    problems = TranslationSkill().check_inputs(tmp_path)
    assert any("extração" in p for p in problems)


def test_run_reports_error_when_inputs_missing(tmp_path):
    result = TranslationSkill().run(tmp_path, scene="X")
    assert result["status"] == "error"
    assert result["artifacts"] == []


def test_run_requires_scene(tmp_path):
    (tmp_path / "artifacts" / "scenes").mkdir(parents=True)
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    result = TranslationSkill().run(tmp_path)
    assert result["status"] == "error"
    assert "scene" in "".join(result["problems"])
