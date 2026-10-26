import struct

import extract as ex


def _database_sdat(keys: list[int]) -> bytes:
    """DataBase.sdat minimo: so o EventManagerData.bin, registros de 48 bytes com a chave do evento no campo 3."""
    names = b"EventManagerData.bin\0"
    pk = 20 + len(names)
    ev = struct.pack("<I", len(keys)) + b"".join(struct.pack("<12I", 0, 0, 0, k, *([0] * 8)) for k in keys)
    head = bytes(16) + struct.pack("<I", 4) + names + b"Pack        " + bytes(4) + struct.pack("<I", 1)
    return head + struct.pack("<II", pk + 28, len(ev)) + ev


def _key(a: int, b: int, c: int) -> int:
    return a * 100000 + b * 1000 + c * 10


def test_story_order_follows_the_event_table_and_keeps_only_project_scenes():
    db = _database_sdat([_key(11, 2, 3), _key(10, 1, 0), _key(11, 2, 3)])
    assert ex.story_order(db, {"10_01_00", "11_02_03", "99_99_99"}) == ["11_02_03", "10_01_00"]   # ordem do jogo, sem repetir
    assert ex.story_order(db, {"10_01_00"}) == ["10_01_00"]                                       # so cena do projeto


def test_write_story_order_reads_the_game_db_or_keeps_the_existing_file(tmp_path):
    (tmp_path / "artifacts").mkdir()
    src = tmp_path / "Data" / "DataBase2.sdat"
    src.parent.mkdir()
    out = tmp_path / "artifacts" / "ordem_cenas.txt"
    assert "NAO confirmada" in ex.write_story_order(tmp_path, src, {"10_01_00"})
    out.write_text("10_01_00\n", encoding="utf-8")
    assert "mantido" in ex.write_story_order(tmp_path, src, {"10_01_00"}) and out.read_text() == "10_01_00\n"
    (src.parent / "ENG").mkdir()
    (src.parent / "ENG" / "DataBase.sdat").write_bytes(_database_sdat([_key(11, 2, 3), _key(10, 1, 0)]))
    assert "2 de 2" in ex.write_story_order(tmp_path, src, {"10_01_00", "11_02_03"})
    assert out.read_text().split() == ["11_02_03", "10_01_00"]
