import json

import box_width
import paths


def _proj(root, cfg, sources):
    (root / "project.json").write_text(json.dumps(cfg), encoding="utf-8")
    d = paths.scene_dir(root, "ch_1_01")
    d.mkdir(parents=True)
    (d / "dialogs.csv").write_text("offset,text_source\n", encoding="utf-8")
    paths.translation_plan(root, "ch_1_01", "1_01").write_text(
        json.dumps({"lines": [{"offset": f"0x{i}", "text_source": s} for i, s in enumerate(sources)]}), encoding="utf-8")


def test_limit_default_derive_and_explicit(tmp_path):
    _proj(tmp_path, {}, ["short", "x" * 20 + "\n" + "y" * 30])
    assert box_width.limit(tmp_path) == 62                      # sem config: padrao antigo
    (tmp_path / "project.json").write_text(json.dumps({"line_width": "derive"}), encoding="utf-8")
    assert box_width.limit(tmp_path) == 30                      # maior segmento visivel do ingles
    (tmp_path / "project.json").write_text(json.dumps({"line_width": "derive", "line_width_max": 40}), encoding="utf-8")
    assert box_width.limit(tmp_path) == 40                      # explicito vence


def test_rewrap_never_cuts_a_word():
    assert box_width.rewrap("aaa bbb ccc dddddddddd", 7, "|") == "aaa bbb|ccc|dddddddddd"
