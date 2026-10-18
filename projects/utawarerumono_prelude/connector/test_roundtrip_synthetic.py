"""
test_roundtrip_synthetic.py — oráculo de round-trip SEMPRE ativo em CI (o binário real é gitignored).

Monta um .sdat sintético em memória (contêiner + membros de texto 4 colunas JA/KO/ZH/EN) com Hypothesis e
verifica: (1) rebuild sem tradução é byte-idêntico; (2) trocar a coluna EN muda só ela (JA/KO/ZH intactas,
tabela Pack coerente, cauda preservada) e o readback devolve o texto aprovado.
"""
import struct

from extract import EN_COL, LANGS, build_text_member, read_sdat, read_text_member, text_members
from hypothesis import given, settings
from hypothesis import strategies as st
from reinsert import rebuild

_STR = st.text(alphabet=st.characters(blacklist_characters="\0", blacklist_categories=("Cs",)), max_size=30)
_ROWS = st.lists(st.lists(_STR, min_size=4, max_size=4), min_size=1, max_size=6)
_SCENES = st.lists(_ROWS, min_size=1, max_size=4)


def _sdat(scenes: list[list[list[str]]]) -> bytes:
    names = [f"ScriptTextData_00_00_{i:02d}.bin".encode() for i in range(len(scenes))] + [b"Other.bin"]
    members = [build_text_member(len(r), 4, [s.encode() for row in r for s in row]) for r in scenes] + [b"\x01\x02\x03"]
    nm = b"".join(n + b"\0" for n in names)
    head_len = 16 + 4 + len(nm) + 12 + 8 + 8 * len(members)
    head_len = (head_len + 15) // 16 * 16
    h = bytearray(b"Filename    " + struct.pack("<II", 0, 4) + nm + b"Pack        "
                  + struct.pack("<II", 8 * len(members), len(members)))
    pairs_at = len(h)
    h += b"\0" * (8 * len(members))
    h += b"\0" * (head_len - len(h))
    body, off = b"", len(h)
    for i, m in enumerate(members):
        pad = (-off) % 16
        body += bytes(pad) + m
        off += pad
        struct.pack_into("<II", h, pairs_at + 8 * i, off, len(m))
        off += len(m)
    return bytes(h) + body + b"TAIL"


@given(_SCENES)
@settings(max_examples=60, deadline=None)
def test_identity_rebuild(scenes):
    data = _sdat(scenes)
    assert rebuild(data, {})[0] == data


@given(_SCENES, _STR)
@settings(max_examples=60, deadline=None)
def test_replace_en_only(scenes, new):
    data = _sdat(scenes)
    out, orphans = rebuild(data, {"00_00_00:0": new})
    assert orphans == []
    a, b = read_sdat(data), read_sdat(out)
    assert b.tail == a.tail == b"TAIL" and b.members[-1] == a.members[-1]
    got = {sc: read_text_member(b.members[i])[2] for sc, i, *_ in text_members(b)}
    old = {sc: read_text_member(a.members[i])[2] for sc, i, *_ in text_members(a)}
    for sc in old:
        for j, s in enumerate(old[sc]):
            tgt = new.encode() if (sc, j) == ("00_00_00", EN_COL) else s
            assert got[sc][j] == tgt
    assert len(LANGS) == 4
