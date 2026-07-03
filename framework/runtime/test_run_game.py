"""test_run_game.py — cobre o driver ponta-a-ponta (P2.5): descoberta capitulada/flat, teto global
de gasto, parada na 1a falha, e retomada idempotente. `run_chapter.run_chapter` e mockado nos testes
que nao precisam do pipeline real; o teste de retomada usa o real (todas as cenas ja verified ->
nenhuma chamada de API acontece, run_chapter pula tudo sozinho).
"""
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import run_game as rg  # noqa: E402


@pytest.fixture
def chaptered_env(tmp_path):
    root = tmp_path
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    for s in ("ch_12_01", "ch_12_02", "ch_13_01"):
        d = root / "artifacts" / "scenes" / s
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hi\n", encoding="utf-8")
    return root


@pytest.fixture
def flat_env(tmp_path):
    root = tmp_path
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    for s in ("AREAD001", "AREAD002"):
        d = root / "artifacts" / "scenes" / s
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hi\n", encoding="utf-8")
    return root


def test_run_game_discovers_and_runs_chapters_in_order(chaptered_env, monkeypatch):
    root = chaptered_env
    called = []

    def fake_run_chapter(root_, chap, **k):
        called.append(chap)
        return {"chapter": chap, "scenes": [], "status": "complete"}
    monkeypatch.setattr(rg.run_chapter, "run_chapter", fake_run_chapter)
    r = rg.run_game(root, backend="api")
    assert called == ["12", "13"]
    assert r["status"] == "complete"


def test_run_game_flat_mode_when_no_chapters_found(flat_env, monkeypatch):
    root = flat_env
    called = []

    def fake_run_chapter(root_, chap, **k):
        called.append((chap, k.get("scenes_glob")))
        return {"chapter": chap, "scenes": [], "status": "complete"}
    monkeypatch.setattr(rg.run_chapter, "run_chapter", fake_run_chapter)
    r = rg.run_game(root, backend="api", scenes_glob="AREAD*")
    assert called == [("full", "AREAD*")]
    assert r["status"] == "complete"


def test_run_game_stops_on_chapter_failure(chaptered_env, monkeypatch):
    root = chaptered_env
    called = []

    def fake_run_chapter(root_, chap, **k):
        called.append(chap)
        if chap == "12":
            return {"chapter": chap, "scenes": [], "status": "stopped"}
        return {"chapter": chap, "scenes": [], "status": "complete"}
    monkeypatch.setattr(rg.run_chapter, "run_chapter", fake_run_chapter)
    r = rg.run_game(root, backend="api")
    assert called == ["12"]      # 13 NUNCA e chamado
    assert r["status"] == "stopped"


def test_run_game_shrinks_max_usd_across_chapters(chaptered_env, monkeypatch):
    root = chaptered_env
    seen_max_usd = []
    spent = {"total": 0.0}

    def fake_run_chapter(root_, chap, **k):
        seen_max_usd.append(k.get("max_usd"))
        spent["total"] += 1.0   # simula $1 de gasto por capitulo
        return {"chapter": chap, "scenes": [], "status": "complete"}
    monkeypatch.setattr(rg.run_chapter, "run_chapter", fake_run_chapter)
    monkeypatch.setattr(rg.cost_report, "report", lambda r, **k: {"total_usd": spent["total"]})
    r = rg.run_game(root, backend="api", max_usd=3.0)
    assert seen_max_usd == [3.0, 2.0]   # cap.13 recebe o RESTANTE do teto global, nao o original
    assert r["status"] == "complete"


def test_run_game_resume_is_idempotent(chaptered_env, monkeypatch):
    root = chaptered_env
    monkeypatch.setattr(rg.run_chapter.connector_gate, "check",
                        lambda r: {"hard_problems": [], "problems": [], "warnings": []})
    # marca TODAS as cenas como ja verified -- run_chapter (real, sem mock) deve pular tudo sem
    # nenhuma chamada de API, exatamente como rodar de novo apos uma parada anterior.
    rs = {"scenes": {s: {"status": "verified", "verified": True}
                     for s in ("ch_12_01", "ch_12_02", "ch_13_01")}}
    (root / "artifacts" / "run_state.json").write_text(json.dumps(rs), encoding="utf-8")
    r = rg.run_game(root, backend="in-session")
    assert r["status"] == "complete"
    assert all(c["status"] == "complete" for c in r["chapters"])
