"""test_back_translate.py — cobre os caminhos de back-translation (sem SDK vivo).

back_translate seleciona candidatos, monta o request (determinista) e roda o crivo pt-BR->EN.
Aqui: no-highs, in-session (escreve prompt/AWAITING), api (mock do streaming), e os helpers
determinísticos (_back_params/_write_back_prompt/_ln_entry).
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import back_translate as bt  # noqa: E402
import paths  # noqa: E402


def _proj(root: Path):
    (root / "artifacts" / "scenes" / "S1").mkdir(parents=True)
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")


HIGHS = [{"offset": "X:0:1", "source": "Hi there", "target": "Oi", "speaker": "Ryu",
          "risk_notes": "ambiguo"}]


def test_no_high_lines_is_noop(tmp_path):
    _proj(tmp_path)
    r = bt.back_translate(tmp_path, "S1", [], backend="api")
    assert r["status"] == bt.DONE and r["reviewed"] == 0 and r["path"] is None


def test_in_session_writes_prompt_and_awaits(tmp_path):
    _proj(tmp_path)
    r = bt.back_translate(tmp_path, "S1", HIGHS, backend="in-session")
    assert r["status"] == bt.AWAITING and r["reviewed"] == 1
    prompt = Path(r["prompt"]).read_text(encoding="utf-8")
    assert "back-translation" in prompt.lower() and "X:0:1" in prompt


def test_unknown_backend_raises(tmp_path):
    _proj(tmp_path)
    import pytest
    with pytest.raises(ValueError, match="backend desconhecido"):
        bt.back_translate(tmp_path, "S1", HIGHS, backend="xpto")


def test_api_path_mocked(tmp_path, monkeypatch):
    _proj(tmp_path)
    monkeypatch.setattr(bt, "_client", lambda: object())
    monkeypatch.setattr(bt, "_stream_final", lambda c, **k: "MSG")
    monkeypatch.setattr(bt, "_usage_of", lambda m: {"in": 5, "out": 3})
    monkeypatch.setattr(bt, "_text_of", lambda m: json.dumps(
        {"entries": [{"offset": "X:0:1", "back_en": "Hi there", "verdict": "pass", "note": "ok"}]}))
    monkeypatch.setattr(bt, "log_api_call", lambda *a, **k: None)
    r = bt.back_translate(tmp_path, "S1", HIGHS, backend="api")
    assert r["status"] == bt.DONE and r["reviewed"] == 1
    data = json.loads(paths.back_translation(tmp_path, "S1", "S1").read_text(encoding="utf-8"))
    assert data["entries"][0]["verdict"] == "pass"


def test_back_params_is_deterministic_request():
    p = bt._back_params(HIGHS, "claude-opus-4-8")
    assert p["model"] == "claude-opus-4-8"
    assert p["output_config"]["format"]["type"] == "json_schema"
    # o payload embute offset/source/target de cada linha
    content = p["messages"][0]["content"]
    assert "X:0:1" in content and "Oi" in content


def test_ln_entry_normalizes():
    e = bt._ln_entry({"offset": "A:0:1", "text_source": "Hi", "base_translation": "Oi",
                      "speaker": "Ryu", "risk_notes": "x"})
    assert e == {"offset": "A:0:1", "source": "Hi", "target": "Oi", "speaker": "Ryu",
                 "risk_notes": "x"}
