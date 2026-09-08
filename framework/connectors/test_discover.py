"""test_discover.py — cobre run()/--generate-stub do CLI de descoberta.

#108: --generate-stub gerava só extract.py, forçando reinsert.py a ser sempre 100% manual.
Agora gera o PAR (mesma evidência -> mesmo padrão). known_engine/blocked nunca geram nada
(existence_gate() já formaliza isso, coberto em test_tier_classifier_gate.py) -- aqui cobrimos
o efeito em discover.run() especificamente para unknown_engine.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import discover  # noqa: E402

_UNKNOWN_EVIDENCE = {
    "file_count": 3, "families": {}, "magic_bytes": {},
    "sample_encodings": {"ascii": 0.9}, "has_control_tokens": False,
    "entropy_mean": 4.0, "string_density": 0.5,
}


def _stub_collect_and_registry(monkeypatch, evidence):
    monkeypatch.setattr(discover, "collect", lambda game_dir: evidence)
    monkeypatch.setattr(discover, "load_registry", lambda: [])


def test_generate_stub_writes_extract_and_reinsert_pair(tmp_path, monkeypatch):
    _stub_collect_and_registry(monkeypatch, _UNKNOWN_EVIDENCE)
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    out_dir = tmp_path / "connector"

    rc = discover.run(game_dir, generate_stub=out_dir)

    assert rc == 0
    extract = out_dir / "extract.py"
    reinsert = out_dir / "reinsert.py"
    assert extract.is_file() and reinsert.is_file()
    assert "GERADO AUTOMATICAMENTE" in extract.read_text(encoding="utf-8")
    assert "GERADO AUTOMATICAMENTE" in reinsert.read_text(encoding="utf-8")
    assert "Par de: extract.py" in reinsert.read_text(encoding="utf-8")


def test_generate_stub_pair_uses_same_pattern(tmp_path, monkeypatch):
    """extract.py e reinsert.py candidatos precisam vir do MESMO padrão (mesma evidência) --
    nunca um token_table pareado com um pointer_table, por exemplo."""
    ev = dict(_UNKNOWN_EVIDENCE, has_control_tokens=True)
    _stub_collect_and_registry(monkeypatch, ev)
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    out_dir = tmp_path / "connector"

    discover.run(game_dir, generate_stub=out_dir)

    extract_txt = (out_dir / "extract.py").read_text(encoding="utf-8")
    reinsert_txt = (out_dir / "reinsert.py").read_text(encoding="utf-8")
    assert "Padrão escolhido: TOKEN_TABLE" in extract_txt
    assert "Padrão escolhido: TOKEN_TABLE" in reinsert_txt


def test_generate_stub_not_written_when_dir_missing_flag(tmp_path, monkeypatch):
    """Sem --generate-stub (generate_stub=None): só reporta, não escreve nada."""
    _stub_collect_and_registry(monkeypatch, _UNKNOWN_EVIDENCE)
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir, generate_stub=None)

    assert rc == 0
    assert not (tmp_path / "extract.py").exists()


# ---------------------------------------------------------------------------
# #95: cobertura de erro/relatório de discover.run() e _print_report()
# ---------------------------------------------------------------------------

_KNOWN_REGISTRY = [{
    "id": "known_engine", "name": "Known Engine",
    "reference_connector": "projects/ref/connector",
    "signatures": {"file_patterns": ["*.KNOWN"], "min_file_count": 1},
}]
_KNOWN_EVIDENCE = {
    "file_count": 5, "families": {"X.KNOWN": 5}, "magic_bytes": {},
    "sample_encodings": {"ascii": 0.9}, "has_control_tokens": False,
    "entropy_mean": 4.0, "string_density": 0.5,
}
_BLOCKED_EVIDENCE = {
    "file_count": 5, "families": {}, "magic_bytes": {},
    "sample_encodings": {"ascii": 0.9}, "has_control_tokens": False,
    "entropy_mean": 7.9, "string_density": 0.5,
}


def test_run_missing_game_dir_returns_2(tmp_path):
    rc = discover.run(tmp_path / "does_not_exist")
    assert rc == 2


def test_run_evidence_collection_error_returns_2(tmp_path, monkeypatch):
    monkeypatch.setattr(discover, "collect", lambda game_dir: {"error": "falha ao ler arquivo"})
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir)

    assert rc == 2


def test_run_known_engine_prints_reference_connector(tmp_path, monkeypatch, capsys):
    _stub_collect_and_registry(monkeypatch, _KNOWN_EVIDENCE)
    monkeypatch.setattr(discover, "load_registry", lambda: _KNOWN_REGISTRY)
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir)

    assert rc == 0
    out = capsys.readouterr().out
    assert "Known Engine" in out
    assert "projects/ref/connector" in out


def test_run_blocked_prints_reasons(tmp_path, monkeypatch, capsys):
    _stub_collect_and_registry(monkeypatch, _BLOCKED_EVIDENCE)
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir)

    assert rc == 1
    out = capsys.readouterr().out
    assert "Bloqueado" in out
    assert "engenharia reversa" in out


def test_run_unknown_engine_prints_top_families(tmp_path, monkeypatch, capsys):
    ev = dict(_UNKNOWN_EVIDENCE, families={"DATA.BIN": 12, "TEXT.STR": 4})
    _stub_collect_and_registry(monkeypatch, ev)
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir)

    assert rc == 0
    out = capsys.readouterr().out
    assert "DATA.BIN: 12 arquivos" in out
