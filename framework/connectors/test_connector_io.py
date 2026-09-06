"""test_connector_io.py — cobre os utilitarios compartilhados entre conectores (#86):
resolucao de caminho (CLI > env var > project.json) e escrita de dialogs.csv/extraction_log.md."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_io as cio  # noqa: E402


def test_resolve_source_path_prefers_cli_arg(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_ENV_VAR", str(tmp_path / "from_env"))
    p = cio.resolve_source_path(cli_arg=str(tmp_path / "from_cli"), env_var="FAKE_ENV_VAR")
    assert p == tmp_path / "from_cli"


def test_resolve_source_path_falls_back_to_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_ENV_VAR", str(tmp_path / "from_env"))
    p = cio.resolve_source_path(cli_arg=None, env_var="FAKE_ENV_VAR")
    assert p == tmp_path / "from_env"


def test_resolve_source_path_falls_back_to_project_json(tmp_path, monkeypatch):
    monkeypatch.delenv("FAKE_ENV_VAR", raising=False)
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {"data_dir": "declared/path"}}), encoding="utf-8")
    p = cio.resolve_source_path(cli_arg=None, env_var="FAKE_ENV_VAR",
                                project_json=pj, cfg_key="data_dir")
    assert p == Path("declared/path")


def test_resolve_source_path_relative_base_applies_only_to_project_json(tmp_path, monkeypatch):
    monkeypatch.delenv("FAKE_ENV_VAR", raising=False)
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {"source_binary": "rel/bin.dat"}}), encoding="utf-8")
    p = cio.resolve_source_path(cli_arg=None, project_json=pj, cfg_key="source_binary",
                                relative_base=tmp_path)
    assert p == tmp_path / "rel/bin.dat"

    # CLI arg NAO recebe o ajuste de relative_base (comportamento original do Utawarerumono)
    p2 = cio.resolve_source_path(cli_arg="rel/bin.dat", project_json=pj, cfg_key="source_binary",
                                 relative_base=tmp_path)
    assert p2 == Path("rel/bin.dat")


def test_resolve_source_path_raises_when_nothing_resolves(tmp_path):
    pj = tmp_path / "project.json"
    pj.write_text(json.dumps({"connector": {}}), encoding="utf-8")
    try:
        cio.resolve_source_path(project_json=pj, cfg_key="data_dir",
                                error_hint="caminho nao configurado", exc=RuntimeError)
        assert False, "deveria levantar RuntimeError"
    except RuntimeError as e:
        assert "caminho nao configurado" in str(e)


def test_resolve_source_path_allow_missing_returns_none(tmp_path):
    assert cio.resolve_source_path(allow_missing=True) is None


def test_write_dialogs_csv_creates_parent_and_writes_rows(tmp_path):
    out = tmp_path / "artifacts" / "dialogs.csv"
    cio.write_dialogs_csv(out, ["offset", "text_en"], [{"offset": "0x1", "text_en": "Hi"}])
    assert out.is_file()
    assert out.read_text(encoding="utf-8").splitlines() == ["offset,text_en", "0x1,Hi"]


def test_write_extraction_log_creates_parent_and_writes_text(tmp_path):
    out = tmp_path / "artifacts" / "extraction_log.md"
    cio.write_extraction_log(out, "# Log\n\nOK\n")
    assert out.read_text(encoding="utf-8") == "# Log\n\nOK\n"


def test_normalize_speaker_matches_canonical_case_insensitive():
    assert cio.normalize_speaker("Ryu", frozenset({"Ryu", "Nina"})) == "Ryu"
    assert cio.normalize_speaker("ryu", frozenset({"Ryu", "Nina"})) == "Ryu"


def test_normalize_speaker_maps_system_words_as_whole_tokens():
    assert cio.normalize_speaker("System", frozenset()) == "system"
    assert cio.normalize_speaker("Narrator", frozenset()) == "system"
    assert cio.normalize_speaker("Instructor", frozenset()) == "system"


def test_normalize_speaker_does_not_match_system_words_as_substring():
    # achado do code review: regex sem word-boundary classificava qualquer nome que
    # CONTIVESSE "system"/"narrator"/etc. como falante de sistema (ex.: "Ecosystem Guardian").
    assert cio.normalize_speaker("Ecosystem Guardian", frozenset()) == "npc"
    assert cio.normalize_speaker("Narratorial Kin", frozenset()) == "npc"


def test_normalize_speaker_unknown_for_empty():
    assert cio.normalize_speaker("", frozenset()) == "unknown"
