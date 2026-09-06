"""test_run_chapter.py — cobre o driver de capítulo (orçamento, batch, glob, QA-export, guards).

run_chapter reusa run_scene (mockado aqui) + descobre cenas por glob. Testa: capítulo vazio,
sucesso completo (com export de QA), parada na 1ª falha, teto de orçamento (pré-voo e por-cena),
modo batch (fase 1 + pós-passe), discovery por scenes-glob, e os guards/helpers.
"""
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import run_chapter as rc  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    for s in ("ch_12_01", "ch_12_02"):
        d = root / "artifacts" / "scenes" / s
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hi\nX:0:2,Bye\n", encoding="utf-8")

    st = {"fail": None}   # fail=scene => run_scene devolve verify_failed nessa cena

    def fake_run_scene(root, scene, **k):
        if st["fail"] == scene:
            return {"status": "verify_failed", "scene": scene}
        return {"status": "verified", "scene": scene, "high": 0, "verified": True}

    monkeypatch.setattr(rc.RS, "run_scene", fake_run_scene)
    monkeypatch.setattr(rc.kb_gate, "check",
                        lambda r, s: {"problems": [], "hard_problems": [], "warnings": [], "pending_decisions": []})
    monkeypatch.setattr(rc.connector_gate, "check",
                        lambda r: {"hard_problems": [], "problems": [], "warnings": []})
    monkeypatch.setattr(rc.cost_report, "report", lambda r, chapter=None: {"total_usd": 0.0, "n_calls": 0})
    monkeypatch.setattr(rc.quality_review, "export", lambda r, c: [{"revisar": ""}])
    monkeypatch.setattr(rc.quality_review, "write_xlsx",
                        lambda rows, out: Path(out).write_text("xlsx", encoding="utf-8"))
    monkeypatch.setattr(rc.M, "batch_translate", lambda r, scenes: {s: "written" for s in scenes})
    monkeypatch.setattr(rc.M, "batch_back_translate", lambda r, scenes: {s: "reviewed" for s in scenes})
    return root, st


def _mark_verified(root, scene):
    p = paths.run_state(root)
    st = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"scenes": {}}
    st.setdefault("scenes", {})[scene] = {"status": "verified", "verified": True}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st), encoding="utf-8")


def test_empty_chapter(env):
    root, _ = env
    r = rc.run_chapter(root, "99")               # não há ch_99_*
    assert r["status"] == "empty"


def test_complete_with_qa_export(env):
    root, _ = env
    r = rc.run_chapter(root, "12", backend="in-session")
    assert r["status"] == "complete"
    assert all(x["status"] == "verified" for x in r["scenes"])
    # QA obrigatório: XLSX gerado no outbox
    assert (paths.qa_outbox(root) / "review_cap_12.xlsx").is_file()


def test_complete_persists_spoiler_audit(env):
    root, _ = env
    r = rc.run_chapter(root, "12", backend="in-session")
    assert r["status"] == "complete"
    # auditoria obrigatoria: roda SEMPRE (mesmo sem spoiler_ledger.json) e persiste o resultado
    out = paths.spoiler_audit(root)
    assert out.is_file()
    rep = json.loads(out.read_text(encoding="utf-8"))
    assert rep == {"name_leaks": [], "gender_flags": [], "clean": True}


def test_resumable_skips_verified(env):
    root, _ = env
    _mark_verified(root, "ch_12_01")
    r = rc.run_chapter(root, "12", backend="in-session")
    by = {x["scene"]: x["status"] for x in r["scenes"]}
    assert by["ch_12_01"] == "skipped" and by["ch_12_02"] == "verified"


def test_stops_on_failure(env):
    root, st = env
    st["fail"] = "ch_12_02"
    r = rc.run_chapter(root, "12", backend="in-session")
    assert r["status"] == "stopped" and r["stopped_at"] == "ch_12_02"


def test_budget_preflight_abort(env):
    root, _ = env
    r = rc.run_chapter(root, "12", max_usd=0.0)   # nem a 1a cena cabe
    assert r["status"] == "stopped_budget_preflight"


def test_budget_excludes_second_scene(env):
    root, _ = env
    # cada cena = 2 linhas * 0.0014 = 0.0028; teto 0.003 cabe 1, adia a 2a
    r = rc.run_chapter(root, "12", backend="in-session", max_usd=0.003)
    assert r["status"] == "stopped_budget"
    assert any(x["status"] == "skipped_budget" for x in r["scenes"])


def test_batch_mode(env):
    root, _ = env
    r = rc.run_chapter(root, "12", backend="api", batch=True)
    assert r["status"] == "complete"


def test_batch_mode_rebuilds_state_index_once_per_chapter(env, monkeypatch):
    # modo batch: 1 rebuild pro capitulo INTEIRO (2 cenas), nao 1 por cena -- redundante no batch
    # (a rodada de traducao ja terminou antes do rebuild ser util). Ver _rebuild_index_phase.
    root, _ = env
    calls = []
    monkeypatch.setattr(rc.state_index, "build",
                        lambda r, **k: calls.append(1) or {"tm": 0, "cards": 0, "decisions": 0, "warnings": []})
    r = rc.run_chapter(root, "12", backend="api", batch=True)
    assert r["status"] == "complete"
    assert calls == [1]


def test_scenes_glob_discovery(env):
    root, _ = env
    r = rc.run_chapter(root, "rotulo", backend="in-session", scenes_glob="ch_12_*")
    assert r["status"] == "complete" and len(r["scenes"]) == 2


def test_batch_failure_aborts_by_default(env, monkeypatch):
    # ADR 0009: batch em SI falhando (nao a cena) deve abortar o capitulo, nunca cair
    # silenciosamente pro caminho interativo full-price sem avisar (era o bug original).
    root, _ = env

    def boom(r, scenes):
        raise RuntimeError("batch API rejected request")
    monkeypatch.setattr(rc.M, "batch_translate", boom)
    r = rc.run_chapter(root, "12", backend="api", batch=True)
    assert r["status"] == "batch_failed"
    assert r["scenes"] == []


def test_batch_failure_falls_back_with_flag(env, monkeypatch):
    # --allow-interactive-fallback destrava o comportamento antigo de proposito.
    root, _ = env

    def boom(r, scenes):
        raise RuntimeError("batch API rejected request")
    monkeypatch.setattr(rc.M, "batch_translate", boom)
    r = rc.run_chapter(root, "12", backend="api", batch=True, allow_interactive_fallback=True)
    assert r["status"] == "complete"
    assert all(x["status"] == "verified" for x in r["scenes"])


def test_chapter_arg_traversal_blocked(env):
    root, _ = env
    with pytest.raises(ValueError, match="separador de path"):
        rc.run_chapter(root, "../evil")


def test_helpers_estimate_and_fit_budget(env):
    root, _ = env
    est = rc._estimate(root, ["ch_12_01", "ch_12_02"])
    assert est["lines"] == 4 and est["hi"] > est["lo"] > 0
    fit, dropped = rc._fit_budget(root, ["ch_12_01", "ch_12_02"], 0.003)
    assert fit == ["ch_12_01"] and dropped == ["ch_12_02"]
    assert rc._fit_budget(root, ["ch_12_01"], None) == (["ch_12_01"], [])


def test_verified_helper(env):
    root, _ = env
    assert rc._verified(root, "ch_12_01") is False
    _mark_verified(root, "ch_12_01")
    assert rc._verified(root, "ch_12_01") is True
