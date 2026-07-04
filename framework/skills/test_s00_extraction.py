"""test_s00_extraction.py — cobre o sandbox contra path traversal (#87): s00_extraction deve
reusar connector_mgr._connector_script(), a mesma validacao ja aplicada por run_scene/connector_mgr,
em vez de concatenar project/extract_script diretamente."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import s00_extraction as s00  # noqa: E402
from s00_extraction import ExtractionSkill  # noqa: E402


def _write_project(tmp_path, extract_script):
    (tmp_path / "project.json").write_text(json.dumps(
        {"connector": {"extract_script": extract_script}}), encoding="utf-8")


def test_check_inputs_rejects_path_traversal(tmp_path):
    _write_project(tmp_path, "../../../evil.py")
    skill = ExtractionSkill()
    problems = skill.check_inputs(tmp_path)
    assert problems
    assert "fora do projeto" in problems[0]


def test_run_rejects_path_traversal_without_subprocess(tmp_path):
    _write_project(tmp_path, "../../../evil.py")
    skill = ExtractionSkill()
    result = skill.run(tmp_path)
    assert result["status"] == "error"
    assert "fora do projeto" in "".join(result.get("problems", [])) + result.get("error", "")


def test_check_inputs_accepts_valid_script(tmp_path):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "extract.py").write_text("pass", encoding="utf-8")
    _write_project(tmp_path, "connector/extract.py")
    skill = ExtractionSkill()
    assert skill.check_inputs(tmp_path) == []


def test_run_survives_non_utf8_stdout(tmp_path):
    # Conector que emite um byte nao-utf-8 no stdout (acento cp1252, dump binario etc.) nao pode
    # derrubar a skill com UnicodeDecodeError/TypeError -- so retornar status=error estruturado.
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "extract.py").write_text(
        "import sys\nsys.stdout.buffer.write(b'\\xe9\\n')\n", encoding="utf-8")
    _write_project(tmp_path, "connector/extract.py")
    skill = ExtractionSkill()
    result = skill.run(tmp_path)  # nao deve levantar excecao
    assert result["status"] == "error"
    assert "dialogs.csv" in result["error"]


def test_check_inputs_rejects_missing_project_json(tmp_path):
    skill = ExtractionSkill()
    problems = skill.check_inputs(tmp_path)
    assert problems == ["project.json não encontrado"]


def test_check_inputs_rejects_missing_extract_script_file(tmp_path):
    _write_project(tmp_path, "connector/extract.py")  # declarado mas nunca criado
    skill = ExtractionSkill()
    problems = skill.check_inputs(tmp_path)
    assert any("não encontrado" in p for p in problems)


def test_run_reports_generic_spawn_failure(tmp_path, monkeypatch):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "extract.py").write_text("pass", encoding="utf-8")
    _write_project(tmp_path, "connector/extract.py")

    def _boom(*a, **k):
        raise OSError("spawn falhou")
    monkeypatch.setattr(s00.subprocess, "run", _boom)
    result = ExtractionSkill().run(tmp_path)
    assert result["status"] == "error" and "spawn falhou" in result["error"]
