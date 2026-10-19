

def test_ptpt_tem_de_only_before_infinitive():
    import quality_review
    assert quality_review._PTPT.search("Ele tem de ir embora")
    assert not quality_review._PTPT.search("Tem de sobra por aqui")


def test_width_only_flags_lines_the_author_broke(tmp_path):
    import json

    import paths
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    d = paths.scene_dir(tmp_path, "ch_1_01")
    d.mkdir(parents=True)
    (d / "dialogs.csv").write_text("offset,text_source\n", encoding="utf-8")
    long = "x" * 80
    lines = [{"offset": "a", "text_source": "one long run " + long, "base_translation": long},        # motor quebra
             {"offset": "b", "text_source": "aa\nbb", "base_translation": long + "\nok"}]              # autor quebrou
    paths.translation_plan(tmp_path, "ch_1_01", "1_01").write_text(json.dumps({"lines": lines}), encoding="utf-8")
    import pattern_lint
    assert pattern_lint.lint(tmp_path)["blocking"] == {"largura": [("ch_1_01", "b")]}
