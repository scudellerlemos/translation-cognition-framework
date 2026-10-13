"""test_labels.py — rotulos em imagem: montagem da palavra (sintetico) e a folha real, se o jogo estiver ai."""
import os
import struct
from pathlib import Path

import imgcodec
import labels
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

_column = st.lists(st.sampled_from([2, 4, 9, 0xB]), min_size=8, max_size=8).map(lambda c: [0] + c[1:7] + [0])
_glyphs = st.dictionaries(st.sampled_from('abcdefgh'), st.lists(_column, min_size=1, max_size=5),
                          min_size=1, max_size=8)


@settings(max_examples=200, deadline=None)
@given(_glyphs, st.data(), st.sampled_from([1, 7]))
def test_render_roundtrip(g, data, fill):
    """Palavra -> colunas -> letras de volta; o contorno so aparece colado ao corpo."""
    g = {ch: [[v if v != fill else 3 for v in col] for col in cols] for ch, cols in g.items()}
    text = data.draw(st.text(sorted(g), min_size=1, max_size=9))
    out = labels.render(g, text, fill)
    assert len(out) == sum(len(g[c]) for c in text) + len(text) + 1
    body = [[v if v != fill else 0 for v in col] for col in out]
    assert labels._segments(body) == [g[c] for c in text]
    for x, col in enumerate(out):
        for y, v in enumerate(col):
            if v == fill:
                assert any(body[i][j] for i in range(max(x - 1, 0), min(x + 2, len(out)))
                           for j in range(max(y - 1, 0), min(y + 2, 8)))


def test_accent_keeps_the_letter_and_adds_the_mark():
    g = {'a': [[0, 0, 5, 5, 5, 5, 5, 0]] * 4, 'i': [[0, 5, 0, 5, 5, 5, 5, 0]]}
    plain, acute = labels._glyph(g, 'a', 5), labels._glyph(g, 'á', 5)
    assert [c[2:] for c in acute] == [c[2:] for c in plain] and sum(map(sum, acute)) == sum(map(sum, plain)) + 10
    assert labels._glyph(g, 'í', 5)[0][:3] == [0, 5, 0] and len(labels._glyph(g, 'í', 5)) == 2


_SRC = Path(os.environ.get('BOF4_DAT_DIR', ''))


@pytest.mark.parametrize('name,sec,table', [('START.DAT', 1, 'principal'), ('INIT.DAT', 2, 'sistema'),
                                            ('AB000_00.DAT', 4, 'batalha')])
def test_real_sheet_only_label_rectangles_change(name, sec, table):
    from reinsert import patch_dat_file
    if not (_SRC / name).is_file():
        pytest.skip('sem os .DAT do jogo')
    dat = (_SRC / name).read_bytes()
    off, size = struct.unpack_from('<2I', dat, sec * 16)
    raw = imgcodec.decode(dat[off:off + size], 32768)
    rows = labels.pixels(imgcodec.untile(raw, labels.COLS))
    assert labels.SHEETS[labels._area_hash(rows)] == (table, frozenset())
    assert imgcodec.tile(labels.pack(rows), labels.COLS) == raw
    before = [list(r) for r in rows]
    cells = labels.TABLES[table]
    inside = {(x, y + r) for y, x0, x1, *_ in cells for x in range(x0, x1) for r in range(8)}
    g = labels.atlas(rows, table=table)
    if table == 'batalha':                                # botoes e ordinais: mesma folha, antes dos rotulos
        btn = labels.buttons(rows, g[7])
        labels.ordinals(rows)
        assert sum(a != b for a, b in btn) >= 6
        inside |= {(x, y + r) for y, x0, x1, *_ in labels.TABLES['botoes'] for x in range(x0, x1) for r in range(9)}
        inside |= {(x, y) for x0, x1, y0, y1 in labels._ORDINALS
                   for x in range(x0 - 1, x1 + 1) for y in range(y0 - 1, y1 + 1)}
    done = labels.translate(rows, table=table, g=g)
    changed = {(x, y) for y in range(256) for x in range(256) if rows[y][x] != before[y][x]}
    assert changed and changed <= inside
    assert sum(a != b for a, b in done) >= 20
    for (_y, _x0, _x1, text, cands, *_), (_, got) in zip(cells, done, strict=True):
        assert got == text or got in cands
    new = labels.patch(dat, patch_dat_file)
    off, size = struct.unpack_from('<2I', new, sec * 16)
    assert labels.pixels(imgcodec.untile(imgcodec.decode(new[off:off + size], 32768), labels.COLS)) == rows
    assert labels.patch(new, patch_dat_file) is new       # folha ja traduzida nao e reconhecida de novo


def test_patch_dat_file_updates_size_of_first_section():
    """Secao 0 que cresce: o tamanho dela no TOC acompanha (a folha de sistema e a secao 0 em um dos arquivos)."""
    from reinsert import patch_dat_file
    dat = struct.pack('<8I', 32, 8, 0, 0, 40, 4, 0, 0) + b'A' * 8 + b'B' * 4
    new = patch_dat_file(dat, 0, b'C' * 16)       # cresce um multiplo do alinhamento do TOC
    assert struct.unpack_from('<8I', new) == (32, 16, 0, 0, 48, 4, 0, 0) and new[32:] == b'C' * 16 + b'B' * 4
