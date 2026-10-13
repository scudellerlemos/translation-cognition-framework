"""events + obs_report: etapa medida, excecao registrada, gate com rastro, visao unica por cena."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import events  # noqa: E402
import obs_report  # noqa: E402


def test_events_feed_the_single_scene_view(tmp_path):
    art = tmp_path / "artifacts"
    events.emit(tmp_path, "gate.kb", "pass", "S1")            # sem artifacts/: nao grava nem derruba
    assert events.read(tmp_path) == []
    art.mkdir()
    (art / "run_state.json").write_text(json.dumps({"scenes": {"S1": {"status": "verified", "n_lines": 4, "high": 1}}}),
                                        encoding="utf-8")
    (art / "metrics.jsonl").write_text(json.dumps({"scene": "S1", "back_pass_rate": 1.0}) + "\n", encoding="utf-8")

    events.emit(tmp_path, "gate.connector", "block", problems=1)
    events.emit(tmp_path, "gate.connector", "pass")
    with events.stage(tmp_path, "scene", "S1") as ev:        # 1a execucao: para AGUARDANDO
        ev["result"] = "awaiting_translation"
    with events.stage(tmp_path, "translate", "S1"):          # o pack roda dentro da traducao
        events.emit(tmp_path, "pack", "ok", "S1", dur_s=0.0)
    with events.stage(tmp_path, "verify", "S1") as ev:
        ev.update(result="fail", individual_overflow=2)
    with events.stage(tmp_path, "verify", "S1") as ev:
        ev.update(individual_overflow=0)
    with pytest.raises(RuntimeError), events.stage(tmp_path, "scene", "S1"):
        raise RuntimeError("quebrou no meio do lote")

    evs = events.read(tmp_path)
    assert all({"t", "run", "stage", "result"} <= set(e) for e in evs) and len({e["run"] for e in evs}) == 1
    assert evs[-1]["result"] == "error" and evs[-1]["error"] == "RuntimeError" and evs[-1]["dur_s"] >= 0

    rep = obs_report.report(tmp_path)
    s = rep["scenes"]["S1"]
    assert (s["runs"], s["verify_fails"], s["overflow"], s["back_pass_rate"]) == (2, 1, 0, 1.0)
    assert rep["gates"]["gate.connector"] == {"pass": 1, "block": 1, "last": "pass", "last_t": evs[1]["t"]}
    assert [f["result"] for f in rep["failures"]] == ["block", "fail", "error"]
    assert "S1" in obs_report._fmt(rep)
