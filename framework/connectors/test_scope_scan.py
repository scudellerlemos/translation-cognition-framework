import scope_scan


def test_scan_marks_uncovered_extensions(tmp_path):
    g = tmp_path / "game"
    g.mkdir()
    (g / "A.DAT").write_bytes(b"x" * 10)
    (g / "B.DAT").write_bytes(b"x" * 20)
    (g / "sheet.png").write_bytes(b"x" * 5)
    d = tmp_path / "dialogs.csv"
    d.write_text("offset,text_source\nsc:A.DAT:1:2,Hi\n", encoding="utf-8")
    r = scope_scan.scan(d, g)
    assert r[".dat"] == {"files": 2, "covered": 1, "bytes": 30, "uncovered_bytes": 20}
    assert r[".png"]["covered"] == 0
