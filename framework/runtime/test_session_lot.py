import json

import paths
import session_lot as sl


def test_rebreak_matches_break_count_without_dangling_words():
    assert sl.rebreak('a[01]b c', 'um dois tres quatro') == 'um dois[01]tres quatro'
    assert sl.rebreak('a b', 'um[01]dois') == 'um dois'
    assert sl.rebreak('a[01]b', 'um[01]dois') == 'um[01]dois'
    assert sl.rebreak('a[01]b', 'ele foi para a casa dela') == 'ele foi[01]para a casa dela'
    assert sl.rebreak('a[01]b', 'ele veio, mas nao quis ficar') == 'ele veio,[01]mas nao quis ficar'


def test_plan_groups_scenes_and_leaves_duplicates_out(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({}), encoding="utf-8")
    for sc, txt in (("ch_1_01", "Hi"), ("ch_1_02", "Hi"), ("ch_1_03", "Bye")):
        d = paths.scene_dir(tmp_path, sc)
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text(f"offset,text_source\nX:{sc}:1,{txt}\n", encoding="utf-8")
    sl._init(tmp_path)
    out = tmp_path / "plan.json"
    sl.cmd_plan(out)
    plan = json.loads(out.read_text(encoding="utf-8"))
    assert plan["lots"] == [{"scenes": ["ch_1_01", "ch_1_03"], "lines": 2}]
    assert plan["dups"] == {"ch_1_01": ["ch_1_02"]}


def test_install_only_changed_files_and_keeps_backup(tmp_path):
    out, src, game = (tmp_path / n for n in ("out", "src", "game"))
    for d in (out, src, game):
        d.mkdir()
    (src / "A.DAT").write_bytes(b"orig")
    (game / "A.DAT").write_bytes(b"orig")
    (out / "A.DAT").write_bytes(b"new")
    (src / "B.DAT").write_bytes(b"same")
    (out / "B.DAT").write_bytes(b"same")
    sl.cmd_install(out, src, game, go=True)
    assert (game / "A.DAT").read_bytes() == b"new" and (game / "A.DAT.bak").read_bytes() == b"orig"
    assert not (game / "B.DAT").exists()
