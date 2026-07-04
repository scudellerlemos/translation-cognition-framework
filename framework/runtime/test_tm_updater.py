"""test_tm_updater.py — cobre sync/reset da TM por serie: grava com source_game, idempotente
(sem duplicata), reset remove SO do jogo certo, reset avisa antes de remover.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
import tm_lookup as tl  # noqa: E402
import tm_updater as tu  # noqa: E402


def _setup_verified_scene(root: Path, scene: str, offset: str, source: str, target: str):
    sid = context_pack.scene_id_of(scene)
    sd = paths.scene_dir(root, scene)
    sd.mkdir(parents=True, exist_ok=True)
    (sd / f"translation_plan_{sid}.json").write_text(json.dumps(
        {"lines": [{"offset": offset, "text_source": source, "base_translation": target, "speaker": "X"}]}),
        encoding="utf-8")
    rs = paths.run_state(root)
    rs.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(rs.read_text(encoding="utf-8")) if rs.is_file() else {"scenes": {}}
    state.setdefault("scenes", {})[scene] = {"status": "verified", "verified": True}
    rs.write_text(json.dumps(state), encoding="utf-8")


def test_sync_scenes_writes_with_source_game(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path / "_repo")
    root = tmp_path / "game1"
    _setup_verified_scene(root, "ch_01_01", "0x1", "Hello", "Ola")
    n = tu.sync_scenes(root, {"series": "bof"}, ["ch_01_01"], approved_at="2026-07-03T00:00:00Z")
    assert n == 1
    tm = tl.load_series_tm("bof")
    assert len(tm) == 1
    assert tm[0]["source_game"] == "game1" and tm[0]["target"] == "Ola"


def test_sync_scenes_is_idempotent_no_duplicates(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path / "_repo")
    root = tmp_path / "game1"
    _setup_verified_scene(root, "ch_01_01", "0x1", "Hello", "Ola")
    tu.sync_scenes(root, {"series": "bof"}, ["ch_01_01"], approved_at="t1")
    tu.sync_scenes(root, {"series": "bof"}, ["ch_01_01"], approved_at="t2")   # roda de novo
    tm = tl.load_series_tm("bof")
    assert len(tm) == 1
    assert tm[0]["approved_at"] == "t2"   # atualizou, nao duplicou


def test_sync_scenes_skips_unverified_scenes(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path / "_repo")
    root = tmp_path / "game1"
    sid = context_pack.scene_id_of("ch_01_01")
    sd = paths.scene_dir(root, "ch_01_01")
    sd.mkdir(parents=True)
    (sd / f"translation_plan_{sid}.json").write_text(
        json.dumps({"lines": [{"offset": "0x1", "text_source": "Hi", "speaker": "X"}]}), encoding="utf-8")
    import csv
    with (sd / f"approved_{sid}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerow(["0x1", "Oi"])
    # NENHUM run_state.json -- cena nunca foi marcada verified
    n = tu.sync_scenes(root, {"series": "bof"}, ["ch_01_01"], approved_at="t")
    assert n == 0
    assert tl.load_series_tm("bof") == []


def test_reset_game_removes_only_that_game(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    p = tl.series_tm_path("bof")
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps([
        {"source_game": "game1", "src_key": "k1", "source": "A", "target": "A-pt"},
        {"source_game": "game2", "src_key": "k2", "source": "B", "target": "B-pt"},
    ]), encoding="utf-8")
    removed = tu.reset_game("bof", "game1")
    assert removed == 1
    tm = tl.load_series_tm("bof")
    assert len(tm) == 1 and tm[0]["source_game"] == "game2"


def test_reset_game_warns_before_removing(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    p = tl.series_tm_path("bof")
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps([{"source_game": "game1", "src_key": "k1"}]), encoding="utf-8")
    tu.reset_game("bof", "game1")
    out = capsys.readouterr().out
    assert "AVISO" in out and "IRREVERSIVEL" in out
