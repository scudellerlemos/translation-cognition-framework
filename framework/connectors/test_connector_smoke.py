"""test_connector_smoke.py — cobre a protecao de encoding/timeout de connector_smoke.py (#76):
o smoke test de conector novo deve delegar em connector_mgr._run (mesma defesa Windows-safe
ja usada por run_scene), nunca chamar subprocess.run cru sem timeout/encoding."""
import csv
import json
import sys
from pathlib import Path

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
