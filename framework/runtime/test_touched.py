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


def test_drift_lista_so_cena_verified_com_texto_alterado(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    _scene(tmp_path, {"a": "um"})
    st = {"t_hashes": touched.fingerprint(tmp_path, "ch_1_01")}
    _scene(tmp_path, {"a": "um"}, **st)
    assert touched.drift(tmp_path) == {}
    _scene(tmp_path, {"a": "UM editado"}, **st)
    assert touched.drift(tmp_path) == {"ch_1_01": ["a"]}
    _scene(tmp_path, {"a": "UM editado"}, status="planned", **st)
    assert touched.drift(tmp_path) == {}


def test_origem_conta_reuso_da_memoria_e_traducao(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    d = paths.scene_dir(tmp_path, "ch_1_01")
    d.mkdir(parents=True)
    paths.translations(tmp_path, "ch_1_01", "1_01").write_text(json.dumps({"lines": {
        "a": {"t": "x", "intent": "reuso_tm"}, "b": {"t": "y", "intent": "reuso_tm"}, "c": {"t": "z"}}}), encoding="utf-8")
    assert touched.origem(tmp_path, "ch_1_01") == {"reuso_tm": 2, "traducao": 1}
