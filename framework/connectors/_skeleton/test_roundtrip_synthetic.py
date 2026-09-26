"""
test_roundtrip_synthetic.py — oráculo de round-trip SEMPRE ativo em CI (padrão BoF4/Trails, #84).

O binário real é gitignored, então test_roundtrip.py pula no CI. Este arquivo exercita a MESMA
lógica determinística (decode_string do extract.py / encode_string do reinsert.py) sobre uma
tabela sintética em memória, com Hypothesis gerando os textos: encode → decode tem que devolver o
texto e o byte_budget exatos, isolado e com várias strings contíguas no mesmo buffer.

ADAPTAR: _TABLE ao formato real (largura de caractere, control codes, terminador) e, se o formato
tiver contêiner/tabela de ponteiros, acrescentar um fixture sintético do arquivo inteiro (ver
projects/breath_of_fire_4/connector/test_roundtrip_synthetic.py). Enquanto encode_string ainda for
o esqueleto (NotImplementedError) o módulo pula — não conta como round-trip verde.
"""
import pytest
from extract import decode_string
from hypothesis import given
from hypothesis import strategies as st
from reinsert import encode_string

# ADAPTAR — tabela sintética no formato de load_table(): (byte_to_char, control_map, terminator)
_CHARS = [c for c in map(chr, range(0x20, 0x7F)) if c not in "{}[]"]  # {}: tokens; []: marcador [XX]
_TABLE = (
    {bytes([ord(c)]): c for c in _CHARS},
    [(b"\x02\x05", "{PAUSE}"), (b"\x01", "{NL}")],  # len desc, como load_table exige
    b"\x00",
)

try:
    encode_string("", _TABLE)
except NotImplementedError:
    pytest.skip("encode_string ainda é o esqueleto — adaptar reinsert.py", allow_module_level=True)

_TEXT = st.lists(st.one_of(st.sampled_from(_CHARS), st.sampled_from(["{NL}", "{PAUSE}"])),
                 max_size=40).map("".join)


@given(_TEXT)
def test_encode_decode_roundtrip(text):
    enc = encode_string(text, _TABLE)
    assert enc.endswith(_TABLE[2])
    assert decode_string(enc, 0, _TABLE) == (text, len(enc))


@given(st.lists(_TEXT, min_size=1, max_size=8))
def test_contiguous_strings_decode_at_their_offsets(texts):
    buf, offsets = b"", []
    for t in texts:
        offsets.append(len(buf))
        buf += encode_string(t, _TABLE)
    assert [decode_string(buf, o, _TABLE)[0] for o in offsets] == texts
