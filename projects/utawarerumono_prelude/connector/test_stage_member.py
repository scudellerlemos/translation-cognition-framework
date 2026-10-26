"""
test_stage_member.py — round-trip do StageTextData (nomes de fase), sempre ativo em CI (o binário real é gitignored).

No jogo, o pool traz JA, KO, ZH, EN em sequência, mas os ponteiros das colunas 2 e 3 estão errados (a coluna 3 cai
no ZH; a coluna 2 cai de -10 a +21 bytes em torno do EN). O leitor lê o pool; o construtor aponta as colunas 2 e 3
para o EN. Aqui o membro sintético nasce com esses mesmos ponteiros defeituosos.
"""
import struct

import pytest
from extract import Unsupported, build_stage_member, read_sdat, read_stage_member, read_text_member
from hypothesis import given, settings
from hypothesis import strategies as st
from reinsert import rebuild
from test_roundtrip_synthetic import _sdat

_STR = st.text(alphabet=st.characters(blacklist_characters="\0", blacklist_categories=("Cs",)), max_size=20)
_ROWS = st.lists(st.lists(_STR, min_size=4, max_size=4), min_size=1, max_size=8)


def _jogo(rows: list[list[str]], desvio: int = 3) -> bytes:
    """Membro com o layout defeituoso do jogo: col 0/1 certas, col 3 no ZH, col 2 deslocada do EN."""
    pos, ptrs = 4 + 16 * len(rows), []
    for ja, ko, zh, en in ([s.encode() for s in r] for r in rows):
        p_ko = pos + len(ja) + 1
        p_zh = p_ko + len(ko) + 1
        p_en = p_zh + len(zh) + 1
        ptrs += [pos, p_ko, p_en + desvio, p_zh]
        pos = p_en + len(en) + 1
    pool = b"".join(s.encode() + b"\0" for r in rows for s in r)
    return struct.pack("<I", len(rows)) + struct.pack(f"<{len(ptrs)}I", *ptrs) + pool


def _cells(b: bytes) -> list[int]:
    return list(struct.unpack_from(f"<{4 * struct.unpack_from('<I', b, 0)[0]}I", b, 4))


@given(_ROWS)
@settings(max_examples=60, deadline=None)
def test_le_o_pool_e_nao_os_ponteiros(rows):
    n, cols, strings = read_stage_member(_jogo(rows))
    assert (n, cols) == (len(rows), 4)
    assert [s.decode() for s in strings] == [s for r in rows for s in r]


@given(_ROWS)
@settings(max_examples=60, deadline=None)
def test_construtor_aponta_colunas_2_e_3_para_o_en_e_e_idempotente(rows):
    n, _, strings = read_stage_member(_jogo(rows))
    b = build_stage_member(n, strings)
    assert len(b) == len(_jogo(rows))  # so os ponteiros mudam: o pool e o mesmo
    assert read_stage_member(b)[2] == strings
    cells = _cells(b)
    for r in range(n):
        ja, ko, zh, en = (cells[4 * r + c] for c in range(4))
        assert b[en:b.index(b"\0", en)] == strings[4 * r + 3]
        assert cells[4 * r + 2] == en
        assert b[ja:b.index(b"\0", ja)] == strings[4 * r] and b[ko:b.index(b"\0", ko)] == strings[4 * r + 1]
    assert build_stage_member(n, read_stage_member(b)[2]) == b


@given(_ROWS, _STR, st.integers(min_value=0))
@settings(max_examples=60, deadline=None)
def test_reinsercao_troca_so_o_en_da_linha(rows, novo, qual):
    idx = qual % len(rows)
    jogo = _jogo(rows)
    out, orphans = rebuild(_sdat_com_stage(jogo), {f"StageTextData:{idx}": novo})
    assert orphans == []
    strings = read_stage_member(_membro(out, "StageTextData.bin"))[2]
    antes = read_stage_member(jogo)[2]
    for i, s in enumerate(strings):
        assert s == (novo.encode() if i == 4 * idx + 3 else antes[i])


def _sdat_com_stage(membro: bytes) -> bytes:
    """Contêiner sintético com um ScriptTextData e o StageTextData como último membro."""
    return _sdat([[["a", "b", "c", "d"]]], (b"StageTextData.bin", membro))


def _membro(data: bytes, nome: str) -> bytes:
    sd = read_sdat(data)
    return sd.members[sd.names.index(nome)]


def test_sem_traducao_o_stage_e_so_corrigido_nunca_perde_texto():
    jogo = _jogo([["ja", "ko", "zh", "Revolt"]])
    n, _, strings = read_stage_member(jogo)
    assert read_stage_member(build_stage_member(n, strings))[2] == strings


@pytest.mark.parametrize("quebrar", ["pool_curto", "ja_fora_do_lugar", "vazio"])
def test_layout_fora_do_esperado_e_recusado(quebrar):
    b = bytearray(_jogo([["ja", "ko", "zh", "en"], ["a", "b", "c", "d"]]))
    if quebrar == "pool_curto":
        b = b[:-2]
    elif quebrar == "ja_fora_do_lugar":
        struct.pack_into("<I", b, 4, 99)
    else:
        b = bytearray(struct.pack("<I", 0))
    with pytest.raises(Unsupported):
        read_stage_member(bytes(b))


def test_texto_normal_continua_sendo_lido_pelo_leitor_padrao():
    # o leitor padrao nao serve ao Stage (ponteiros fora de ordem): fica recusado, o despacho e por nome
    with pytest.raises(Unsupported):
        read_text_member(_jogo([["ja", "ko", "zh", "en"]]))
