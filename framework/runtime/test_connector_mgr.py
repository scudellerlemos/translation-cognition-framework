"""test_connector_mgr.py — cobre a interface com os scripts de conector (sandbox, hash, run, status)."""
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import connector_mgr as cm  # noqa: E402
import paths  # noqa: E402


def test_connector_script_accept_and_reject(tmp_path):
    (tmp_path / "connector").mkdir()
    p = cm._connector_script(tmp_path, {}, "verify_script", "verify_chapter.py")
    assert p == tmp_path / "connector" / "verify_chapter.py"
    with pytest.raises(ValueError, match="fora do projeto"):
        cm._connector_script(tmp_path, {"connector": {"verify_script": "../../../etc/x.py"}},
                             "verify_script", "verify_chapter.py")


def test_connector_hash(tmp_path):
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("codigo", encoding="utf-8")
    h = cm._connector_hash(tmp_path, {})
    assert isinstance(h, str) and len(h) == 12
    assert len(cm._connector_hash(tmp_path / "sem_conector", {})) == 12   # ausente -> hash de vazio


def test_run_executes_subprocess():
    code, out = cm._run([sys.executable, "-c", "print('ola-mundo')"])
    assert code == 0 and "ola-mundo" in out


def test_verify_status_parse():
    assert cm._verify_status('x\nVERIFY_STATUS: {"fitting_failure": true}\ny') == {"fitting_failure": True}
    assert cm._verify_status("sem linha de status") == {}
    assert cm._verify_status("VERIFY_STATUS: nao-e-json") == {}


def test_warn_if_connector_stale(tmp_path, capsys):
    conn = tmp_path / "connector"
    conn.mkdir()
    (conn / "build_plan_chapter.py").write_text("codigo", encoding="utf-8")
    rs = paths.run_state(tmp_path)
    rs.parent.mkdir(parents=True, exist_ok=True)
    rs.write_text(json.dumps({"scenes": {"S1": {"connector_hash": "HASHANTIGO12"}}}), encoding="utf-8")
    cm._warn_if_connector_stale(tmp_path, "S1", {})
    assert "conector mudou" in capsys.readouterr().out
