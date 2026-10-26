import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conformidade_onda as c  # noqa: E402


def _proj(tmp_path, ledger, cenas, log_txt):
    art = tmp_path / "artifacts"
    art.mkdir()
    (art / "api_ledger.jsonl").write_text("\n".join(json.dumps(r) for r in ledger), encoding="utf-8")
    (art / "run_state.json").write_text(json.dumps({"scenes": cenas}), encoding="utf-8")
    log = tmp_path / "onda.log"
    log.write_text(log_txt, encoding="utf-8")
    return log


def test_lote_conforme_e_janela_errada_reprova(tmp_path):
    led = [{"t": 10, "session": "s", "model": "claude-haiku-5-5", "attribution": "overhead"},
           {"t": 10, "session": "s", "model": "claude-opus-5-5", "attribution": "agent", "agent_type": "general-purpose"}]
    log = _proj(tmp_path, led, {"01_01": {"verified": True, "_ts": 10}}, "x\nONDA_OK 01_01\n")
    assert all(ok for ok, _ in c.conferir(tmp_path, 5, "haiku", [log]))
    falhas = [m for ok, m in c.conferir(tmp_path, 5, "sonnet", [log]) if not ok]
    assert len(falhas) == 1 and "modelo da janela" in falhas[0]


def test_sem_onda_ok_ou_com_bypass_reprova(tmp_path):
    log = _proj(tmp_path, [], {"01_01": {"verified": True, "_ts": 10}}, "rodei com --skip-kb-gate\nPARADA: x\n")
    falhas = " | ".join(m for ok, m in c.conferir(tmp_path, 5, "haiku", [log]) if not ok)
    assert "ONDA_OK em 0 de 1" in falhas and "bypass" in falhas
