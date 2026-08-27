"""test_split_scenes.py — cobre split_scenes.py (materializacao de artifacts/scenes/<cena>/dialogs.csv
a partir do flat dialogs.csv, agrupado por coluna)."""
import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import split_scenes  # noqa: E402


def _write_flat(root: Path, rows, fieldnames=("offset", "file", "text_en", "byte_budget")):
    p = paths.dialogs_flat(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def test_groups_by_file_column(tmp_path):
    _write_flat(tmp_path, [
        {"offset": "scena/mp0000.dat:0x1", "file": "scena/mp0000.dat", "text_en": "Hi", "byte_budget": "3"},
        {"offset": "scena/mp0000.dat:0x2", "file": "scena/mp0000.dat", "text_en": "Bye", "byte_budget": "4"},
        {"offset": "scena/mp0001.dat:0x1", "file": "scena/mp0001.dat", "text_en": "Yo", "byte_budget": "3"},
    ])
    result = split_scenes.split(tmp_path)
    assert result == {"scenes": 2, "rows": 3, "by": "file"}
    assert paths.dialogs(tmp_path, "mp0000").is_file()
    assert paths.dialogs(tmp_path, "mp0001").is_file()
    with paths.dialogs(tmp_path, "mp0000").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert [r["offset"] for r in rows] == ["scena/mp0000.dat:0x1", "scena/mp0000.dat:0x2"]


def test_dry_run_writes_nothing(tmp_path):
    _write_flat(tmp_path, [{"offset": "a:0x1", "file": "a", "text_en": "Hi", "byte_budget": "3"}])
    result = split_scenes.split(tmp_path, dry_run=True)
    assert result["scenes"] == 1
    assert not paths.scenes_dir(tmp_path).exists()


def test_missing_column_exits(tmp_path, capsys):
    _write_flat(tmp_path, [{"offset": "a:0x1", "file": "a", "text_en": "Hi", "byte_budget": "3"}])
    try:
        split_scenes.split(tmp_path, by="nope")
        assert False, "deveria ter chamado sys.exit"
    except SystemExit as e:
        assert "nope" in str(e)


def test_missing_flat_file_exits(tmp_path):
    try:
        split_scenes.split(tmp_path)
        assert False, "deveria ter chamado sys.exit"
    except SystemExit as e:
        assert "dialogs.csv" in str(e)
