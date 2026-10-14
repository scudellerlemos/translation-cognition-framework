import json

import context_pack
import paths
import touched


def _scene(root, ts, status="verified", **extra):
    d = paths.scene_dir(root, "ch_1_01")
    d.mkdir(parents=True, exist_ok=True)
    paths.translations(root, "ch_1_01", "1_01").write_text(
        json.dumps({"lines": {o: {"t": t} for o, t in ts.items()}}), encoding="utf-8")
    rs = paths.run_state(root)
    rs.parent.mkdir(parents=True, exist_ok=True)
    rs.write_text(json.dumps({"scenes": {"ch_1_01": {"status": status, **extra}}}), encoding="utf-8")


def test_only_changed_or_new_lines_are_touched(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    _scene(tmp_path, {"a": "um", "b": "dois"})
    st = {"t_hashes": touched.fingerprint(tmp_path, "ch_1_01")}
    _scene(tmp_path, {"a": "um", "b": "DOIS", "c": "tres"}, **st)
    assert touched.touched(tmp_path, "ch_1_01") == ["b", "c"]
    _scene(tmp_path, {"a": "um", "b": "dois"}, **st)
    assert touched.touched(tmp_path, "ch_1_01") == []


def test_unchanged_needs_same_doctrine_and_connector(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    _scene(tmp_path, {"a": "um"})
    st = {"t_hashes": touched.fingerprint(tmp_path, "ch_1_01"), "connector_hash": "h1",
          "doctrine_hash": context_pack._doctrine_hash(tmp_path)}
    _scene(tmp_path, {"a": "um"}, **st)
    assert touched.unchanged(tmp_path, "ch_1_01", "h1")
    assert not touched.unchanged(tmp_path, "ch_1_01", "h2")          # conector mudou
    _scene(tmp_path, {"a": "um"}, status="verify_failed", **st)
    assert not touched.unchanged(tmp_path, "ch_1_01", "h1")          # nao estava verified
