"""test_connector_smoke.py — cobre a protecao de encoding/timeout de connector_smoke.py (#76):
o smoke test de conector novo deve delegar em connector_mgr._run (mesma defesa Windows-safe
ja usada por run_scene), nunca chamar subprocess.run cru sem timeout/encoding."""
import csv
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_smoke as cs  # noqa: E402


def _write_extract(tmp_path, body):
    connector_dir = tmp_path / "connector"
    connector_dir.mkdir()
    (connector_dir / "extract.py").write_text(body, encoding="utf-8")


def test_smoke_survives_non_utf8_stdout(tmp_path):
    """extract.py que imprime byte fora de UTF-8 nao pode derrubar o smoke com UnicodeDecodeError
    (mesmo bug que connector_mgr.py ja corrigiu uma vez para o run_scene)."""
    _write_extract(tmp_path, (
        "import sys\n"
        "sys.stdout.buffer.write(b'\\xe9\\n')\n"
        "sys.exit(0)\n"
    ))
    (tmp_path / "project.json").write_text(json.dumps({"source": {"id_column": "offset"}}), encoding="utf-8")
    # dialogs.csv nao existe -> invariantes 2/3 falham, mas smoke() nao pode lancar excecao alguma
    ok = cs.smoke(tmp_path)
    assert ok is False


def test_smoke_delegates_timeout_to_connector_mgr(tmp_path, monkeypatch):
    """extract.py travado (loop infinito) nao pode travar o smoke indefinidamente -- confirma que
    smoke() delega a connector_mgr._run com timeout explicito, em vez de subprocess.run sem teto."""
    _write_extract(tmp_path, "while True:\n    pass\n")
    (tmp_path / "project.json").write_text(json.dumps({"source": {"id_column": "offset"}}), encoding="utf-8")
    calls = []

    def fake_run(cmd, timeout=None):
        calls.append(timeout)
        return 1, "[timeout] conector nao respondeu"

    monkeypatch.setattr(cs.connector_mgr, "_run", fake_run)
    ok = cs.smoke(tmp_path)
    assert ok is False
    assert calls == [300]


def test_roundtrip_delegates_timeout_to_connector_mgr(tmp_path, monkeypatch):
    """reinsert.py travado nao pode travar o round-trip -- confirma timeout explicito (600s, mais
    generoso que o extract por reinsercao poder ser mais lenta)."""
    connector_dir = tmp_path / "connector"
    connector_dir.mkdir()
    (connector_dir / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    source = tmp_path / "game.bin"
    source.write_bytes(b"HELLO\x00")
    project_json = tmp_path / "project.json"
    project_json.write_text(json.dumps(
        {"connector": {"source_binary": "game.bin"}, "source": {"id_column": "offset"}}),
        encoding="utf-8")
    dialogs_csv = tmp_path / "artifacts" / "dialogs.csv"
    dialogs_csv.parent.mkdir(parents=True)
    with dialogs_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["offset", "text_en", "byte_budget"])
        w.writeheader()
        w.writerow({"offset": "0x0", "text_en": "HELLO", "byte_budget": 5})

    calls = []

    def fake_run(cmd, timeout=None):
        calls.append(timeout)
        return 1, "erro simulado"

    monkeypatch.setattr(cs.connector_mgr, "_run", fake_run)
    ok, detail = cs._run_roundtrip(tmp_path, None, dialogs_csv, project_json, "offset")
    assert ok is False
    assert calls == [600]


# ---------------------------------------------------------------------------
# #95: cobertura de smoke() -- invariantes 1/2/3, flag --roundtrip, extract.py ausente
# ---------------------------------------------------------------------------

def _write_dialogs_csv(tmp_path, rows, fieldnames=("offset", "text_en", "byte_budget")):
    dialogs_csv = tmp_path / "artifacts" / "dialogs.csv"
    dialogs_csv.parent.mkdir(parents=True, exist_ok=True)
    with dialogs_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return dialogs_csv


def test_smoke_missing_extract_py_exits_2(tmp_path):
    with pytest.raises(SystemExit) as exc:
        cs.smoke(tmp_path)
    assert exc.value.code == 2


def test_smoke_reports_and_forwards_game_data_dir(tmp_path, monkeypatch, capsys):
    _write_extract(tmp_path, "import sys\nsys.exit(0)\n")
    game_data_dir = tmp_path / "gamedata"
    game_data_dir.mkdir()
    calls = []

    def fake_run(cmd, timeout=None):
        calls.append(cmd)
        return 0, ""

    monkeypatch.setattr(cs.connector_mgr, "_run", fake_run)
    cs.smoke(tmp_path, game_data_dir)

    assert str(game_data_dir) in calls[0]
    assert f"game_data_dir: {game_data_dir}" in capsys.readouterr().out


def test_smoke_dialogs_csv_missing_required_column(tmp_path, monkeypatch, capsys):
    _write_extract(tmp_path, "import sys\nsys.exit(0)\n")
    _write_dialogs_csv(tmp_path, [{"offset": "0x0", "text_en": "hi"}],
                        fieldnames=("offset", "text_en"))
    monkeypatch.setattr(cs.connector_mgr, "_run", lambda cmd, timeout=None: (0, ""))

    ok = cs.smoke(tmp_path)

    assert ok is False
    assert "colunas faltando" in capsys.readouterr().out


def test_smoke_dialogs_csv_missing_text_column(tmp_path, monkeypatch, capsys):
    _write_extract(tmp_path, "import sys\nsys.exit(0)\n")
    _write_dialogs_csv(tmp_path, [{"offset": "0x0", "byte_budget": "5"}],
                        fieldnames=("offset", "byte_budget"))
    monkeypatch.setattr(cs.connector_mgr, "_run", lambda cmd, timeout=None: (0, ""))

    ok = cs.smoke(tmp_path)

    assert ok is False
    assert "nenhuma coluna text_*" in capsys.readouterr().out


def test_smoke_happy_path_survives_malformed_project_json(tmp_path, monkeypatch, capsys):
    """project.json malformado nao pode derrubar smoke() -- so cai no id_col default."""
    _write_extract(tmp_path, "import sys\nsys.exit(0)\n")
    (tmp_path / "project.json").write_text("{not valid json", encoding="utf-8")
    _write_dialogs_csv(tmp_path, [
        {"offset": "0x0", "text_en": "", "byte_budget": "5"},
        {"offset": "0x1", "text_en": "ola mundo", "byte_budget": "10"},
    ])
    monkeypatch.setattr(cs.connector_mgr, "_run", lambda cmd, timeout=None: (0, ""))

    ok = cs.smoke(tmp_path)

    out = capsys.readouterr().out
    assert ok is True
    assert "1 linhas não-vazias extraídas" in out
    assert "ola mundo" in out


def test_smoke_roundtrip_flag_delegates_to_run_roundtrip(tmp_path, monkeypatch):
    _write_extract(tmp_path, "import sys\nsys.exit(0)\n")
    monkeypatch.setattr(cs.connector_mgr, "_run", lambda cmd, timeout=None: (0, ""))
    calls = []

    def fake_roundtrip(project_root, game_data_dir, dialogs_csv, project_json, id_col):
        calls.append(project_root)
        return True, "ok"

    monkeypatch.setattr(cs, "_run_roundtrip", fake_roundtrip)
    cs.smoke(tmp_path, roundtrip=True)

    assert calls == [tmp_path]


# ---------------------------------------------------------------------------
# #95: cobertura de _run_roundtrip() -- pre-condicoes ausentes
# ---------------------------------------------------------------------------

def test_run_roundtrip_missing_reinsert_py(tmp_path):
    dialogs_csv = _write_dialogs_csv(tmp_path, [{"offset": "0x0", "text_en": "x", "byte_budget": "1"}])
    ok, detail = cs._run_roundtrip(tmp_path, None, dialogs_csv, tmp_path / "project.json", "offset")
    assert ok is False
    assert "reinsert.py não encontrado" in detail


def test_run_roundtrip_missing_dialogs_csv(tmp_path):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    ok, detail = cs._run_roundtrip(tmp_path, None, tmp_path / "artifacts" / "dialogs.csv",
                                    tmp_path / "project.json", "offset")
    assert ok is False
    assert "dialogs.csv não existe" in detail


def test_run_roundtrip_source_not_found(tmp_path):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    dialogs_csv = _write_dialogs_csv(tmp_path, [{"offset": "0x0", "text_en": "x", "byte_budget": "1"}])
    ok, detail = cs._run_roundtrip(tmp_path, None, dialogs_csv, tmp_path / "project.json", "offset")
    assert ok is False
    assert "fonte original não encontrada" in detail


def test_run_roundtrip_dialogs_csv_without_text_column(tmp_path):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    source = tmp_path / "game.bin"
    source.write_bytes(b"X")
    project_json = tmp_path / "project.json"
    project_json.write_text(json.dumps({"connector": {"source_binary": "game.bin"}}), encoding="utf-8")
    dialogs_csv = _write_dialogs_csv(tmp_path, [{"offset": "0x0", "byte_budget": "1"}],
                                      fieldnames=("offset", "byte_budget"))
    ok, detail = cs._run_roundtrip(tmp_path, None, dialogs_csv, project_json, "offset")
    assert ok is False
    assert "vazio ou sem coluna text_*" in detail


def test_run_roundtrip_success_matches_hash_and_restores_backup(tmp_path, monkeypatch):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    dialogs_csv = _write_dialogs_csv(tmp_path, [{"offset": "0x0", "text_en": "hello", "byte_budget": "5"}])
    source = tmp_path / "game.bin"
    source.write_bytes(b"ORIGINAL-BYTES")
    project_json = tmp_path / "project.json"
    project_json.write_text(json.dumps({"connector": {"source_binary": "game.bin"}}), encoding="utf-8")

    approved = tmp_path / "artifacts" / "approved_translations.csv"
    approved.write_text("old-approved-content", encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "game.bin").write_bytes(b"ORIGINAL-BYTES")

    game_data_dir = tmp_path / "gamedata"
    calls = []

    def fake_run(cmd, timeout=None):
        calls.append(cmd)
        return 0, ""

    monkeypatch.setattr(cs.connector_mgr, "_run", fake_run)

    ok, detail = cs._run_roundtrip(tmp_path, game_data_dir, dialogs_csv, project_json, "offset")

    assert ok is True
    assert "SHA256 idêntico" in detail
    assert str(game_data_dir) in calls[0]
    assert approved.read_text(encoding="utf-8") == "old-approved-content"
    assert not (tmp_path / "artifacts" / "approved_translations.smoke_backup").exists()


def test_run_roundtrip_hash_mismatch(tmp_path, monkeypatch):
    (tmp_path / "connector").mkdir()
    (tmp_path / "connector" / "reinsert.py").write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
    dialogs_csv = _write_dialogs_csv(tmp_path, [{"offset": "0x0", "text_en": "hello", "byte_budget": "5"}])
    source = tmp_path / "game.bin"
    source.write_bytes(b"ORIGINAL-BYTES")
    project_json = tmp_path / "project.json"
    project_json.write_text(json.dumps({"connector": {"source_binary": "game.bin"}}), encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "game.bin").write_bytes(b"DIFFERENT-BYTES")

    monkeypatch.setattr(cs.connector_mgr, "_run", lambda cmd, timeout=None: (0, ""))

    ok, detail = cs._run_roundtrip(tmp_path, None, dialogs_csv, project_json, "offset")

    assert ok is False
    assert "SHA256 diverge" in detail


# ---------------------------------------------------------------------------
# #95: cobertura de _find_source() e _find_output()
# ---------------------------------------------------------------------------

def test_find_source_bad_json_with_game_data_dir_returns_none(tmp_path):
    project_json = tmp_path / "project.json"
    project_json.write_text("{not valid json", encoding="utf-8")
    game_data_dir = tmp_path / "gd"
    game_data_dir.mkdir()

    assert cs._find_source(tmp_path, project_json, game_data_dir) is None


def test_find_source_nothing_declared_returns_none(tmp_path):
    project_json = tmp_path / "project.json"  # nao existe
    assert cs._find_source(tmp_path, project_json, None) is None


def test_find_output_missing_output_dir_returns_none(tmp_path):
    source = tmp_path / "src.bin"
    source.write_bytes(b"x")
    assert cs._find_output(tmp_path, source) is None


def test_find_output_exact_name_match(tmp_path):
    source = tmp_path / "src.bin"
    source.write_bytes(b"x")
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    target = out_dir / "src.bin"
    target.write_bytes(b"y")

    assert cs._find_output(tmp_path, source) == target


def test_find_output_same_suffix_fallback(tmp_path):
    source = tmp_path / "src.bin"
    source.write_bytes(b"x")
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    other = out_dir / "renamed.bin"
    other.write_bytes(b"z")

    assert cs._find_output(tmp_path, source) == other


def test_find_output_no_match_returns_none(tmp_path):
    source = tmp_path / "src.bin"
    source.write_bytes(b"x")
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    (out_dir / "other.txt").write_bytes(b"z")

    assert cs._find_output(tmp_path, source) is None
