import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cota_uso  # noqa: E402


def _ev(five, seven):
    return json.dumps({"type": "rate_limit_event", "rate_limit_info": {"unifiedWindows": {
        "five_hour": {"utilization": five, "resetsAt": 100}, "seven_day": {"utilization": seven, "resetsAt": 200}}}})


def test_parse_pega_o_ultimo_evento_e_ignora_lixo():
    s = "\n".join(["{}", "nao e json", _ev(0.1, 0.5), '{"type":"rate_limit_event" quebrado', _ev(0.3, 0.6)])
    assert cota_uso.parse(s) == {"five_hour": 0.3, "seven_day": 0.6, "reset_five_hour": 100}


def test_parse_sem_evento_devolve_none():
    assert cota_uso.parse('{"type":"result"}') is None
