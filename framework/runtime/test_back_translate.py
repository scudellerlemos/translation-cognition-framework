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


def test_has_stale_only_for_candidate_offsets(tmp_path):
    out = tmp_path / "bt.json"
    out.write_text(json.dumps({"entries": [{"offset": "a", "stale": True}, {"offset": "b"}]}), encoding="utf-8")
    assert bt._has_stale(out, [{"offset": "a"}])                 # verdict velho -> re-julgar
    assert not bt._has_stale(out, [{"offset": "b"}])             # so 'b' e candidato e nao esta stale
    assert not bt._has_stale(tmp_path / "nope.json", [{"offset": "a"}])


def test_merge_back_replaces_only_rejudged_lines(tmp_path):
    out = tmp_path / "bt.json"
    out.write_text(json.dumps({"entries": [{"offset": "a", "stale": True, "verdict": "pass"},
                                           {"offset": "b", "verdict": "pass"}]}), encoding="utf-8")
    assert bt._stale_offsets(out) == {"a"}
    merged = bt._merge_back(out, {"entries": [{"offset": "a", "verdict": "revise"}]})
    assert sorted((e["offset"], e["verdict"], e.get("stale", False)) for e in merged["entries"]) == [
        ("a", "revise", False), ("b", "pass", False)]            # 'b' (valido) preservado, 'a' re-julgado


def _plan(root: Path, levels: dict):
    p = paths.translation_plan(root, "S1", "S1")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"lines": [{"offset": o, "risk_level": r, "text_source": "s", "base_translation": "t"}
                                       for o, r in levels.items()]}), encoding="utf-8")


def test_back_risk_default_cobre_high_e_critical(tmp_path):
    _proj(tmp_path)
    _plan(tmp_path, {"S1:0": "low", "S1:1": "high", "S1:2": "critical"})
    assert [c["offset"] for c in bt.high_risk_lines(tmp_path, "S1")] == ["S1:1", "S1:2"]


def test_back_risk_do_project_json_restringe_a_critical(tmp_path):
    _proj(tmp_path)
    (tmp_path / "project.json").write_text('{"back_translation_risk":["critical"]}', encoding="utf-8")
    _plan(tmp_path, {"S1:0": "low", "S1:1": "high", "S1:2": "critical"})
    assert [c["offset"] for c in bt.high_risk_lines(tmp_path, "S1")] == ["S1:2"]


def test_back_risk_valor_invalido_volta_ao_padrao(tmp_path):
    _proj(tmp_path)
    (tmp_path / "project.json").write_text('{"back_translation_risk":["urgente"]}', encoding="utf-8")
    _plan(tmp_path, {"S1:1": "high"})
    assert [c["offset"] for c in bt.high_risk_lines(tmp_path, "S1")] == ["S1:1"]


def test_quality_gate_so_exige_cobertura_dos_niveis_configurados(tmp_path):
    import quality_gate as qg
    _proj(tmp_path)
    (tmp_path / "artifacts" / "scenes" / "S1" / "dialogs.csv").write_text("offset\n", encoding="utf-8")
    _plan(tmp_path, {"S1:1": "high", "S1:2": "critical"})
    assert {u["offset"] for u in qg.check(tmp_path)["uncovered"]} == {"S1:1", "S1:2"}
    (tmp_path / "project.json").write_text('{"back_translation_risk":["critical"]}', encoding="utf-8")
    assert {u["offset"] for u in qg.check(tmp_path)["uncovered"]} == {"S1:2"}
