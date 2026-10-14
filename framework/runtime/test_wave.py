import argparse
import subprocess
import wave

import paths


def _proj(root):
    (root / "project.json").write_text("{}", encoding="utf-8")
    for sc in ("ch_1_01", "ch_1_02", "ch_1_03"):
        d = paths.scene_dir(root, sc)
        d.mkdir(parents=True)
        txt = "Bye" if sc == "ch_1_03" else "Hi"
        (d / "dialogs.csv").write_text(f"offset,text_source\nX:{sc}:1,{txt}\n", encoding="utf-8")
    (root / "artifacts").mkdir(exist_ok=True)


def test_duplicate_scene_waits_for_original_then_goes_through_gates(tmp_path, monkeypatch):
    _proj(tmp_path)
    names = [n for n, _ in wave.steps(str(tmp_path), ["ch_1_01", "ch_1_02", "ch_1_03"], "in-session", False)]
    assert names[:2] == ["run_scene", "scene_dedup"]
    ran = []

    def fake(cmd, **k):
        ran.append(cmd[3:])
        out = "ch_1_02" if cmd[3].endswith("scene_dedup.py") else "ok"
        return argparse.Namespace(returncode=0, stdout=out, stderr="")
    monkeypatch.setattr(subprocess, "run", fake)
    assert wave.run(str(tmp_path), ["ch_1_01", "ch_1_02", "ch_1_03"]) == 0
    runs = [c for c in ran if c[0].endswith("run_scene.py")]
    assert len(runs) == 2 and "ch_1_02" not in runs[0] and "ch_1_02" in runs[1]


def test_no_duplicates_keeps_old_steps(tmp_path):
    _proj(tmp_path)
    assert "scene_dedup" not in [n for n, _ in wave.steps(str(tmp_path), ["ch_1_03"], "api", False)]


def test_dedup_copy_is_limited_to_requested_scenes(tmp_path):
    import scene_dedup
    _proj(tmp_path)
    d = paths.scene_dir(tmp_path, "ch_1_04")
    d.mkdir()
    (d / "dialogs.csv").write_text("offset,text_source\nX:ch_1_04:1,Hi\n", encoding="utf-8")
    rs = paths.run_state(tmp_path)
    rs.write_text('{"scenes": {"ch_1_01": {"status": "verified"}}}', encoding="utf-8")
    assert scene_dedup.copy(tmp_path, only=["ch_1_02"]) == ["ch_1_02"]
