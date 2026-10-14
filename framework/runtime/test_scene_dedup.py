import json

import paths
import scene_dedup


def _scene(root, sc, offs, text="Hi"):
    d = paths.scene_dir(root, sc)
    d.mkdir(parents=True)
    (d / "dialogs.csv").write_text("offset,text_source\n" + "".join(f"{o},{text}\n" for o in offs), encoding="utf-8")


def test_copy_remaps_offsets_by_position(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    _scene(tmp_path, "ch_1_01", ["A.DAT:1:1", "A.DAT:1:2"])
    _scene(tmp_path, "ch_1_02", ["B.DAT:7:1", "B.DAT:7:2"])
    _scene(tmp_path, "ch_1_03", ["C.DAT:1:1"], text="outro")          # texto diferente: fora do grupo
    paths.run_state(tmp_path).write_text(json.dumps({"scenes": {"ch_1_01": {"status": "verified"}}}), encoding="utf-8")
    import context_pack
    paths.translations(tmp_path, "ch_1_01", context_pack.scene_id_of("ch_1_01")).write_text(
        json.dumps({"lines": {"A.DAT:1:1": {"t": "Oi \"x\""}, "A.DAT:1:2": {"t": "Ola"}}}), encoding="utf-8")
    assert scene_dedup.groups(tmp_path) == {"ch_1_01": ["ch_1_02"]}
    assert scene_dedup.copy(tmp_path) == ["ch_1_02"]
    out = json.loads(paths.translations(tmp_path, "ch_1_02", context_pack.scene_id_of("ch_1_02")).read_text("utf-8"))
    assert out["lines"] == {"B.DAT:7:1": {"t": "Oi \"x\""}, "B.DAT:7:2": {"t": "Ola"}}


def test_groups_use_text_en_column_and_split_by_text(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    for sc, txt in (("ch_1_01", "Hi"), ("ch_1_02", "Hi"), ("ch_1_03", "Other")):
        d = paths.scene_dir(tmp_path, sc)
        d.mkdir(parents=True)
        (d / "dialogs.csv").write_text(f"offset,text_en,byte_budget\nX:{sc}:1,{txt},9\n", encoding="utf-8")
    assert scene_dedup.groups(tmp_path) == {"ch_1_01": ["ch_1_02"]}
