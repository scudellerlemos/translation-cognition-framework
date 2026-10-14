"""session_usage: 1 requisicao = 1 message.id; subagente de uma cena = custo exato da cena; cursor por arquivo."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import cost  # noqa: E402
import cost_report  # noqa: E402
import session_usage as su  # noqa: E402

SID = "abcdef12-0000-0000-0000-000000000000"
OPUS = "claude-opus-5-5"


def _req(mid, sec, i, o, cmd=None, model=OPUS):
    content = [{"type": "tool_use", "id": f"tu_{mid}", "name": "Bash", "input": {"command": cmd}}] if cmd else [{"type": "text"}]
    return json.dumps({"type": "assistant", "timestamp": f"2026-01-01T00:00:{sec:02d}Z", "message": {
        "id": mid, "model": model, "content": content, "usage": {
            "input_tokens": i, "output_tokens": o, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 7,
            "cache_creation": {"ephemeral_1h_input_tokens": 7, "ephemeral_5m_input_tokens": 0}}}})


def _out(sec, stdout, mid):
    return json.dumps({"type": "user", "timestamp": f"2026-01-01T00:00:{sec:02d}Z", "toolUseResult": {"stdout": stdout},
                       "message": {"content": [{"type": "tool_result", "tool_use_id": f"tu_{mid}"}]}})


RUN = "python ../../framework/runtime/run_scene.py . {} --backend in-session"


def _env(tmp_path):
    tdir = tmp_path / "transcripts"
    (tdir / SID / "subagents").mkdir(parents=True)
    main = [
        _req("m0", 5, 9, 9),                                # conversa: overhead
        _req("m1", 10, 1, 10, RUN.format("S1")),            # abre S1 (empacota)
        _req("m1", 11, 1, 10, RUN.format("S1")),            # mesma requisicao, outro bloco: conta uma vez
        "lixo", _out(12, "[2/6] AGUARDANDO traducao", "m1"),
        _req("m2", 20, 2, 5),                               # traducao de S1 na sessao principal
        _req("m3", 30, 4, 8, RUN.format("S1")),
        _out(31, "saida filtrada, sem o status", "m3"),     # nao esta mais AGUARDANDO -> fecha
        _req("m4", 40, 3, 3),                               # depois de fechar: overhead
    ]
    (tdir / f"{SID}.jsonl").write_text("\n".join(main), encoding="utf-8")
    (tdir / SID / "subagents" / "agent-a1.jsonl").write_text("\n".join([
        _req("a0", 41, 5, 50, model="claude-sonnet-5"),     # antes do comando: ainda assim e da cena
        _req("a1", 42, 5, 50, RUN.format("S2"), model="claude-sonnet-5"),
    ]), encoding="utf-8")
    (tdir / "outra-sessao.jsonl").write_text(_req("x0", 1, 999, 999), encoding="utf-8")   # nao tocou o projeto
    root = tmp_path / "proj"
    (root / "artifacts").mkdir(parents=True)
    (root / "artifacts" / "run_state.json").write_text(json.dumps({"scenes": {"S1": {}, "S2": {}}}), encoding="utf-8")
    return root, tdir


def test_sync_attributes_requests_and_is_incremental(tmp_path):
    root, tdir = _env(tmp_path)
    rows = su.sync(root, tdir)
    assert {(r["scene"], r["phase"]): r["n_requests"] for r in rows if r["scene"] == "S1"} == {
        ("S1", "other"): 1, ("S1", "translate"): 2}                   # m1 abre; m2 e m3 vem depois do AGUARDANDO
    by = {(r["scene"], r["attribution"]): r for r in rows if r["phase"] != "translate"}
    assert set(by) == {("S1", "window"), ("S2", "agent"), ("_session", "overhead")}
    assert su.scene_total(root, "S1")["usage"]["in"] == 7 and su.scene_total(root, "S1")["n_requests"] == 3
    assert by["S2", "agent"]["usage"]["out"] == 100 and by["S2", "agent"]["agent"] == "a1"
    assert by["_session", "overhead"]["usage"]["in"] == 12            # m0 + m4; a outra sessao fica de fora
    assert all(r["cost_usd"] == 0.0 and r["api_equiv_usd"] > 0 for r in rows)
    assert su.sync(root, tdir) == []                                  # nada novo -> nada anexado

    with (tdir / SID / "subagents" / "agent-a1.jsonl").open("a", encoding="utf-8") as f:
        f.write("\n" + _req("a2", 50, 1, 1, model="claude-sonnet-5"))  # cauda do subagente, depois do run_scene
    (tail,) = su.sync(root, tdir)
    assert tail["scene"] == "S2" and tail["n_requests"] == 1
    assert su.scene_total(root, "S2")["usage"]["in"] == 11 and su.scene_total(root, "S3") is None

    rep = cost_report.report(root)
    assert rep["total_usd"] == 0.0 and rep["by_source"]["session"]["calls"] == 8
    assert rep["by_source"]["session"]["api_equiv_usd"] > 0
    assert rep["by_scene"]["S2"]["attribution"] == "agent"
    assert rep["split"]["translate"] > 0 and rep["split"]["governance"] == 0
    assert set(rep["by_activity"]) == {"conversa"} and rep["by_activity"]["conversa"]["calls"] == 2   # m0 + m4
    assert su._activity([{"type": "tool_use", "input": {"command": "pytest framework/runtime"}}]) == "framework"
    assert su._activity([{"type": "tool_use", "input": {"file_path": "projects/x/connector/extract.py"}}]) == "conector"


def test_price_uses_model_cache_multiplier_and_1h_write():
    u = {"in": 0, "out": 0, "cache_read": 1_000_000, "cache_write": 0, "cache_write_1h": 1_000_000}
    assert round(cost.cost_of(OPUS, u), 6) == 0.20 + 8.00             # 0.05x lido, 2x escrita de 1 h
    assert round(cost.cost_of("claude-opus-4-8", {"cache_read": 1_000_000}), 6) == 0.50


def test_missing_final_usage_is_estimated_and_stage_mark_applies(tmp_path):
    import json as _j

    import cost as _c
    root = tmp_path / "proj"
    (root / "artifacts" / "scenes" / "S1").mkdir(parents=True)
    tdir = tmp_path / "t"
    tdir.mkdir()

    def line(mid, out, stop, ts, cmd=None):
        blocks = [{"type": "text", "text": "x" * 1000}] + (
            [{"type": "tool_use", "id": "x", "input": {"command": cmd}}] if cmd else [])
        return _j.dumps({"type": "assistant", "timestamp": ts, "message": {
            "id": mid, "model": "claude-sonnet-5-5", "stop_reason": stop, "content": blocks,
            "usage": {"input_tokens": 1, "output_tokens": out}}})
    (tdir / "aaaaaaaa-1.jsonl").write_text("\n".join([
        line("m1", 50, "end_turn", "2026-01-01T00:00:10Z", cmd="python run_scene.py . S1"),   # final gravado: exato
        line("m2", 2, None, "2026-01-01T00:00:20Z"),                                          # so o parcial: estima
    ]) + "\n", encoding="utf-8")
    su.mark(root, "fase3", t=1767225615.0)          # entre m1 (00:00:10) e m2 (00:00:20)
    rows = su.sync(root, tdir)
    assert sum(r["usage"]["out"] for r in rows) == 50 + 520 and sum(r.get("out_est", 0) for r in rows) == 520
    assert sorted(str(r.get("stage")) for r in rows) == ["None", "fase3"]
    # Haiku 5.5: prompt acima de 100 mil tokens paga 5x em tudo
    hk = "claude-haiku-5-5"
    assert abs(_c.cost_of(hk, {"in": 100_001}) / _c.cost_of(hk, {"in": 100_000}) - 5) < 0.01


def test_sonnet5_has_own_fit_and_report_states_estimate_error():
    assert "claude-sonnet-5" in su._OUT_FIT
    import inspect

    import cost_report as cr
    assert "erro da estimativa na soma" in inspect.getsource(cr)
