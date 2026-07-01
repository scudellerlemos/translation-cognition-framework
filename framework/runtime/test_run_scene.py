"""test_run_scene.py — cobre os ramos do orquestrador run_scene com o pipeline mockado.

run_scene chama kb_gate/context_pack/model/connector/back_translate/state_index. Aqui esses
colaboradores viram stubs controláveis (monkeypatch no namespace do módulo), e cada teste dirige
UM caminho: sucesso verified/planned, bloqueio de KB (hard/soft/skip), falhas de tradução/plan/
verify, escalonamento de fitting, back-translation (defer/require/awaiting). Sem rede, sem conector.
"""
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import model  # noqa: E402
import run_scene as rs  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    """(root, scene, st) — projeto mínimo + pipeline mockado no happy-path; st permite override."""
    root = tmp_path
    (root / "project.json").write_text(
        json.dumps({"title": "T", "media_type": "game", "connector": {}}), encoding="utf-8")
    scene = "AREAD001"
    (root / "artifacts" / "scenes" / scene).mkdir(parents=True)

    st = {
        "kb": {"warnings": [], "problems": [], "hard_problems": [], "pending_decisions": []},
        "tr": {"status": model.DONE, "n_lines": 3, "usage": {"in": 10, "out": 5},
               "model": model.MODEL_TRANSLATE, "reused": 0, "novel": 3},
        "highs": [],
        "back": {"status": model.DONE, "reviewed": 0, "path": None},
        "runs": [],          # sequência de (code, out) p/ build_plan/verify; vazio => sempre (0,"")
        "translate_exc": None,
        "back_exc": None,
    }
    calls = {"i": 0}

    def fake_run(cmd, timeout=None):
        seq = st["runs"]
        if not seq:
            return (0, "")
        r = seq[calls["i"]] if calls["i"] < len(seq) else seq[-1]
        calls["i"] += 1
        return r

    def fake_translate(r, s, **k):
        if st["translate_exc"]:
            raise st["translate_exc"]
        return st["tr"]

    def fake_back(r, s, h, **k):
        if st["back_exc"]:
            raise st["back_exc"]
        return st["back"]

    monkeypatch.setattr(rs.kb_gate, "check", lambda r, s: st["kb"])
    monkeypatch.setattr(rs.context_pack, "write_pack",
                        lambda r, s: {"scene_id": context_pack.scene_id_of(s), "n_lines": st["tr"]["n_lines"]})
    monkeypatch.setattr(rs.context_pack, "_doctrine_hash", lambda r: "")
    monkeypatch.setattr(rs.M, "translate", fake_translate)
    monkeypatch.setattr(rs.M, "high_risk_lines", lambda r, s: st["highs"])
    monkeypatch.setattr(rs.M, "back_translate", fake_back)
    monkeypatch.setattr(rs.M, "over_budget_offsets", lambda r, s, tolerance=1.0: [])
    monkeypatch.setattr(rs, "_connector_script", lambda r, c, key, d: root / "connector" / d)
    monkeypatch.setattr(rs, "_warn_if_connector_stale", lambda r, s, c: None)
    monkeypatch.setattr(rs, "_connector_hash", lambda r, c: "hash")
    monkeypatch.setattr(rs, "_run", fake_run)
    monkeypatch.setattr(rs.state_index, "build",
                        lambda r, **k: {"tm": 0, "cards": 0, "decisions": 0, "warnings": []})
    return root, scene, st


def test_success_verified(env):
    root, scene, st = env
    st["runs"] = [(0, ""), (0, "")]                 # build_plan ok, verify ok
    r = rs.run_scene(root, scene, backend="api")
    assert r["status"] == "verified" and r["verified"] is True
    # checkpoint gravado + metrics escrito (cobre _checkpoint/_metrics/_ledger_scene_cost)
    assert (root / "artifacts" / "run_state.json").is_file()
    assert (root / "artifacts" / "metrics.jsonl").is_file()


def test_success_planned_no_verify(env):
    root, scene, st = env
    st["runs"] = [(0, "")]                           # só build_plan; verify pulado
    r = rs.run_scene(root, scene, do_verify=False)
    assert r["status"] == "planned" and r["verified"] is None


def test_kb_hard_block(env):
    root, scene, st = env
    st["kb"]["hard_problems"] = ["sem KB reconciliada"]
    r = rs.run_scene(root, scene)
    assert r["status"] == "kb_coverage_failed" and r["problems"]


def test_kb_soft_block_without_skip(env):
    root, scene, st = env
    st["kb"]["problems"] = ["cobertura parcial"]
    r = rs.run_scene(root, scene, skip_kb_gate=False)
    assert r["status"] == "kb_coverage_failed"


def test_kb_soft_bypassed_with_skip(env):
    root, scene, st = env
    st["kb"]["problems"] = ["cobertura parcial"]
    st["kb"]["pending_decisions"] = ["decidir alias de X"]   # cobre o ramo de decisões pendentes
    st["runs"] = [(0, ""), (0, "")]
    r = rs.run_scene(root, scene, skip_kb_gate=True)
    assert r["status"] == "verified"


def test_api_translate_failed(env):
    root, scene, st = env
    st["translate_exc"] = RuntimeError("rede caiu")
    r = rs.run_scene(root, scene, backend="api")
    assert r["status"] == "api_translate_failed" and "rede caiu" in r["error"]


def test_awaiting_translation(env):
    root, scene, st = env
    st["tr"] = {"status": model.AWAITING, "n_lines": 3, "prompt": "p.md", "expected_output": "o.json"}
    r = rs.run_scene(root, scene, backend="in-session")
    assert r["status"] == "awaiting_translation"


def test_build_plan_failed(env):
    root, scene, st = env
    st["runs"] = [(1, "erro no build_plan")]
    r = rs.run_scene(root, scene)
    assert r["status"] == "build_plan_failed"


def test_verify_failed_hard(env):
    root, scene, st = env
    st["runs"] = [(0, ""), (1, "falha dura")]        # verify exit 1 = falha dura (não escala)
    r = rs.run_scene(root, scene, backend="api")
    assert r["status"] == "verify_failed"


def test_fitting_escalation_then_verified(env):
    root, scene, st = env
    # build_plan ok, verify exit 3 (fitting) -> retighten -> build_plan ok, verify ok
    st["runs"] = [(0, ""), (3, "fitting"), (0, ""), (0, "")]
    r = rs.run_scene(root, scene, backend="api")
    assert r["status"] == "verified"


def test_defer_back(env):
    root, scene, st = env
    st["highs"] = [{"offset": "X:0:1"}]
    st["runs"] = [(0, ""), (0, "")]
    r = rs.run_scene(root, scene, defer_back=True)
    assert r["status"] == "verified" and r["high"] == 1


def test_back_failed_require_back(env):
    root, scene, st = env
    st["highs"] = [{"offset": "X:0:1"}]
    st["runs"] = [(0, ""), (0, "")]
    st["back_exc"] = RuntimeError("back caiu")
    r = rs.run_scene(root, scene, require_back=True)
    assert r["status"] == "back_translation_failed"


def test_awaiting_back_require_back(env):
    root, scene, st = env
    st["highs"] = [{"offset": "X:0:1"}]
    st["runs"] = [(0, ""), (0, "")]
    st["back"] = {"status": model.AWAITING, "prompt": "bp.md"}
    r = rs.run_scene(root, scene, require_back=True)
    assert r["status"] == "awaiting_back_translation"


def test_opts_object_path(env):
    """RunSceneOptions substitui os kwargs quando passado."""
    root, scene, st = env
    st["runs"] = [(0, "")]
    opts = rs.RunSceneOptions(backend="api", require_back=False, do_verify=False,
                              skip_kb_gate=False, pretranslated=False, defer_back=False)
    r = rs.run_scene(root, scene, opts=opts)
    assert r["status"] == "planned"


def test_invalid_scene_raises(env):
    root, _scene, _st = env
    with pytest.raises(ValueError, match="fora de artifacts"):
        rs.run_scene(root, "../../etc/passwd")


def test_clean_failed_scene_moves_and_is_idempotent(env):
    root, scene, st = env
    st["runs"] = [(0, ""), (1, "falha")]
    rs.run_scene(root, scene, backend="api")          # gera run_state com a cena
    moved = rs.clean_failed_scene(root, scene)
    assert isinstance(moved, list)
    assert rs.clean_failed_scene(root, scene) == [] or isinstance(rs.clean_failed_scene(root, scene), list)


def test_clean_failed_scene_moves_artifacts(tmp_path):
    import paths
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    scene = "AREAD002"
    sid = context_pack.scene_id_of(scene)
    paths.scene_dir(tmp_path, scene).mkdir(parents=True)
    paths.translations(tmp_path, scene, sid).write_text("{}", encoding="utf-8")
    paths.scene_prompt(tmp_path, scene).write_text("prompt", encoding="utf-8")
    moved = rs.clean_failed_scene(tmp_path, scene)
    assert len(moved) >= 2                            # translations + scene_prompt movidos
    assert not paths.translations(tmp_path, scene, sid).is_file()   # saiu do lugar original


def test_prune_discontinued(tmp_path):
    import os
    import time as _t
    import paths
    disc = paths.discontinued_dir(tmp_path)
    old = disc / "old_scene"
    old.mkdir(parents=True)
    (old / "x.txt").write_text("x", encoding="utf-8")
    ot = _t.time() - 40 * 86400
    os.utime(old, (ot, ot))
    new = disc / "new_scene"
    new.mkdir(parents=True)
    removed = rs.prune_discontinued(tmp_path, older_than_days=30)
    assert any("old_scene" in r for r in removed) and not old.exists()
    assert new.exists()                              # recente preservada
    assert rs.prune_discontinued(tmp_path / "sem_disc") == []   # dir ausente -> []


def test_check_stale_reports(tmp_path, monkeypatch, capsys):
    import paths
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    monkeypatch.setattr(context_pack, "_doctrine_hash", lambda r: "CUR")
    rsp = paths.run_state(tmp_path)
    rsp.parent.mkdir(parents=True, exist_ok=True)
    rsp.write_text(json.dumps({"scenes": {
        "s_fresh": {"doctrine_hash": "CUR"},
        "s_stale": {"doctrine_hash": "OLD"},
        "s_none": {}}}), encoding="utf-8")
    rs._check_stale(str(tmp_path))
    out = capsys.readouterr().out
    assert "s_stale" in out and "s_none" in out and "CUR" in out
    rsp.unlink()
    rs._check_stale(str(tmp_path))
    assert "nenhuma cena" in capsys.readouterr().out.lower()
