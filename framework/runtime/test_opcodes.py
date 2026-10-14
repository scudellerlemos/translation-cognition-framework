import json

import opcodes

TBL = {"01": "newline", "07": {"name": "var_value", "params": 1, "width": 3, "values": ["00", "03"]}}


def _tbl(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({"connector": {"control_codes": TBL}}), encoding="utf-8")
    return opcodes.table(tmp_path)


def test_parameter_is_not_a_code_and_breaks_split_segments(tmp_path):
    t = _tbl(tmp_path)
    assert opcodes.tokens("HP [07][03] ok[01]fim", t) == [
        ("text", "HP "), ("code", "07", ["03"]), ("text", " ok"), ("code", "01", []), ("text", "fim")]
    # [03] e valor do 07 (nao quebra); o [01] quebra; a variavel soma 3 glifos
    assert opcodes.segments("HP [07][03] ok[01]fim", t) == [(3 + 3 + 3, "HP  ok"), (3, "fim")]


def test_invalid_param_value_is_reported(tmp_path):
    t = _tbl(tmp_path)
    assert opcodes.invalid_params("a [07][03] b [07][09]", t) == ["[07][09]"]
