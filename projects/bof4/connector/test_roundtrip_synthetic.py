"""
test_roundtrip_synthetic.py — oracle de round-trip SEMPRE ativo em CI.

Problema que fecha: `.github/workflows/test.yml` só roda o round-trip byte-idêntico contra o
binário REAL do jogo, que é gitignored (licenciamento) — no runner do GitHub Actions ele nunca
existe, então `test_round_trip_byte_identical` (test_roundtrip.py) sempre pula (`pytest.skip`).
O "oráculo" mais citado do projeto (round-trip byte-idêntico prova que a tradução não corrompeu
o binário) nunca era de fato verificado de forma contínua.

Este arquivo constrói, EM MEMÓRIA, um arquivo .DAT sintético mínimo que reproduz a estrutura real
do formato Capcom (TOC de 16 bytes/entrada + seção de texto = tabela de ponteiros uint16 + strings
null-terminated) — não é o jogo, é um fixture pequeno e comitável que exercita a MESMA lógica
determinística (`parse_toc`/`find_text_section`/`extract_section_strings`/`rebuild_section`/
`patch_dat_file`) usada por extract.py/reinsert.py sobre o binário real. Roda sempre, sem skip,
sem dependência de hardware/arquivo local — fecha a lacuna descrita na issue.
"""
import struct
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
from extract import (  # noqa: E402
    decode_string,
    extract_section_strings,
    find_text_section,
    parse_toc,
)
from reinsert import patch_dat_file, rebuild_section  # noqa: E402

_STRINGS = [
    b"Hello there my friend",
    b"Bye for now my friend",
    b"Thanks a lot dear friend",
    b"See you soon my friend",
]


def _build_synthetic_dat(strings: list[bytes] = _STRINGS) -> bytes:
    """Monta um .DAT sintético: TOC (2 entradas, 32 bytes) + 1 seção de texto (ponteiros + strings).

    entries[0] é sempre ignorado por find_text_section (varre `entries[1:]`) — seu campo `off`
    coincide com o próprio toc_size (mesmos 4 bytes lidos 2x), como no formato real. entries[1]
    descreve a seção de texto que construímos logo em seguida.
    """
    first_ptr = len(strings) * 2
    blob = bytearray()
    ptrs = []
    for s in strings:
        ptrs.append(first_ptr + len(blob))
        blob += s + b"\x00"
    section = bytearray()
    for p in ptrs:
        section += struct.pack("<H", p)
    section += blob
    assert len(section) >= 64, "seção precisa ser >=64 bytes p/ passar find_text_section"

    toc_size = 32
    section_off = toc_size
    toc = bytearray(toc_size)
    struct.pack_into("<IIII", toc, 0, toc_size, 0, 0, 0)                       # entries[0] (ignorado)
    struct.pack_into("<IIII", toc, 16, section_off, len(section), 0, 0)       # entries[1] (texto)
    return bytes(toc) + bytes(section)


def test_synthetic_dat_is_recognized():
    """parse_toc + find_text_section devem localizar a seção sintética (entry_idx=1)."""
    data = _build_synthetic_dat()
    entries = parse_toc(data)
    assert len(entries) == 2
    result = find_text_section(data, entries)
    assert result is not None, "heurística não reconheceu o fixture sintético"
    entry_idx, sec_off, sec_sz = result
    assert entry_idx == 1
    assert sec_off == 32
    section = data[sec_off:sec_off + sec_sz]
    strings = extract_section_strings(section)
    assert len(strings) == len(_STRINGS)
    for (ptr_idx, _ptr, raw), expected in zip(strings, _STRINGS, strict=False):
        assert raw == expected, (ptr_idx, raw, expected)


def test_roundtrip_identity_byte_for_byte():
    """extract -> reinsert SEM traduzir (identidade) reproduz o arquivo original byte-a-byte —
    o oráculo central do projeto, verificado aqui sem depender do binário comercial."""
    original = _build_synthetic_dat()
    entries = parse_toc(original)
    entry_idx, sec_off, sec_sz = find_text_section(original, entries)
    section = original[sec_off:sec_off + sec_sz]
    strings = extract_section_strings(section)

    identity_translations = {ptr_idx: decode_string(raw) for ptr_idx, _ptr, raw in strings}
    new_section = rebuild_section(section, identity_translations)
    new_data = patch_dat_file(original, entry_idx, new_section)

    assert new_data == original, "round-trip de identidade NÃO é byte-idêntico"


@pytest.mark.parametrize("ptr_idx,new_text,expect_shrink_or_equal", [
    (0, "Oi amigo", True),                                    # bem mais curto -> seção encolhe
    (1, "Ate mais amigo!", None),                              # tamanho parecido
])
def test_roundtrip_translated_reextracts_correctly(ptr_idx, new_text, expect_shrink_or_equal):
    """Traduzir 1 string e reinserir deve produzir um arquivo que, re-extraído, devolve EXATAMENTE
    a tradução na string alterada e o ORIGINAL byte-a-byte nas demais (prova que reconstrução não
    corrompe strings vizinhas nem a tabela de ponteiros)."""
    original = _build_synthetic_dat()
    entries = parse_toc(original)
    entry_idx, sec_off, sec_sz = find_text_section(original, entries)
    section = original[sec_off:sec_off + sec_sz]
    strings = extract_section_strings(section)
    orig_by_idx = {i: raw for i, _p, raw in strings}

    translations = {i: decode_string(raw) for i, _p, raw in strings}
    translations[ptr_idx] = new_text                          # só esta string muda

    new_section = rebuild_section(section, translations)
    new_data = patch_dat_file(original, entry_idx, new_section)

    # RE-EXTRAI do arquivo modificado (oráculo completo: extract(reinsert(...)) == esperado)
    new_entries = parse_toc(new_data)
    new_entry_idx, new_sec_off, new_sec_sz = find_text_section(new_data, new_entries)
    new_section_bytes = new_data[new_sec_off:new_sec_off + new_sec_sz]
    new_strings = {i: raw for i, _p, raw in extract_section_strings(new_section_bytes)}

    assert decode_string(new_strings[ptr_idx]) == new_text
    for i, raw in orig_by_idx.items():
        if i == ptr_idx:
            continue
        assert decode_string(new_strings[i]) == decode_string(raw), (
            f"string vizinha ptr_idx={i} foi corrompida pela reconstrução")

    if expect_shrink_or_equal:
        assert new_sec_sz <= sec_sz


def test_roundtrip_expansion_updates_toc():
    """Tradução MAIS LONGA que o original -> seção expande e o TOC é atualizado (size/offset),
    sem quebrar a estrutura do arquivo (regressão: reinsert.py não pode deixar o TOC desatualizado)."""
    original = _build_synthetic_dat()
    entries = parse_toc(original)
    entry_idx, sec_off, sec_sz = find_text_section(original, entries)
    section = original[sec_off:sec_off + sec_sz]
    strings = extract_section_strings(section)

    translations = {i: decode_string(raw) for i, _p, raw in strings}
    translations[0] = "This translation is much much longer than the original English string"

    new_section = rebuild_section(section, translations)
    new_data = patch_dat_file(original, entry_idx, new_section)

    assert len(new_section) > sec_sz, "tradução mais longa deveria expandir a seção"
    assert len(new_data) == len(original) + (len(new_section) - sec_sz)

    new_entries = parse_toc(new_data)
    assert new_entries[entry_idx][1] == len(new_section), "TOC nao reflete o novo tamanho da secao"

    new_entry_idx, new_sec_off, new_sec_sz = find_text_section(new_data, new_entries)
    new_section_bytes = new_data[new_sec_off:new_sec_off + new_sec_sz]
    new_strings = {i: raw for i, _p, raw in extract_section_strings(new_section_bytes)}
    assert decode_string(new_strings[0]) == translations[0]


def test_literal_bracket_bytes_roundtrip_not_confused_with_control_code():
    """ASCII literal '[AB]' (5B 41 42 5D) virava o byte 0xAB no re-encode; agora '[' sai como [5B]."""
    from extract import encode_string
    raw = b"x[AB]y\x8f"
    text = decode_string(raw)
    assert "[5B]" in text and encode_string(text) == raw


def test_encode_strict_rejects_unmappable_char():
    from extract import encode_string
    with pytest.raises(ValueError):
        encode_string("\u65e5\u672c", strict=True)
    assert encode_string("\u65e5", strict=False) == b"?"


def test_patch_dat_file_keeps_size_delta_multiple_of_toc_alignment():
    original = _build_synthetic_dat()
    entries = parse_toc(original)
    entry_idx, sec_off, sec_sz = find_text_section(original, entries)
    section = original[sec_off:sec_off + sec_sz]
    translations = {i: decode_string(raw) for i, _p, raw in extract_section_strings(section)}
    translations[0] = "Oi"
    new_data = patch_dat_file(original, entry_idx, rebuild_section(section, translations))
    assert (len(new_data) - len(original)) % 16 == 0


def test_rebuild_section_raises_when_pointer_exceeds_uint16():
    original = _build_synthetic_dat()
    section = original[32:]
    with pytest.raises(OverflowError):
        rebuild_section(section, {0: "x" * 70000})


def test_reinsert_main_exits_3_on_pointer_overflow(tmp_path):
    """Overflow de ponteiro uint16 aborta com exit 3 (antes: traceback cru), sem gravar o .DAT."""
    from reinsert import main as reinsert_main

    dat_dir = tmp_path / "dat"
    dat_dir.mkdir()
    (dat_dir / "A.DAT").write_bytes(_build_synthetic_dat())
    scene = tmp_path / "artifacts" / "scenes" / "ch_01_01"
    scene.mkdir(parents=True)
    rows = ["offset,file,entry_idx,ptr_idx,text_en,byte_budget"]
    rows += [f"A:{i},A.DAT,1,{i},{s.decode()},{len(s) + 1}" for i, s in enumerate(_STRINGS)]
    (tmp_path / "artifacts" / "dialogs.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (scene / "approved_01.csv").write_text(f"offset,text_target\nA:0,{'x' * 70000}\n", encoding="utf-8")
    (tmp_path / "project.json").write_text(
        '{"source": {"file": "artifacts/dialogs.csv"}}', encoding="utf-8")

    with pytest.raises(SystemExit) as ei:
        reinsert_main(tmp_path / "project.json", str(dat_dir))
    assert ei.value.code == 3
    assert not (tmp_path / "output" / "A.DAT").exists()


@pytest.mark.parametrize("raw,kept", [
    (b'\x05\x03Food\x06', True),            # destaque azul em label: e texto
    (b'Beer', True),                          # label curto
    (b'\x14A', False),                        # so speaker; 'A' e parametro
    (b'\x0c\x05\x14A', False),                # comando + speaker
    (b'--\x81', False),
    (b'\x14\x05\x04"...\x0b..."', False),     # fala sem letra
])
def test_content_filter_ignores_control_param_bytes(raw, kept):
    import extract
    assert bool(extract._LETTER_RE.search(extract._CTRL_PARAM_RE.sub(b'', raw))) is kept


# --- Acento sobreposto (font.py): 'á' = [A0] + 'a' ----------------------------------------------
from hypothesis import given  # noqa: E402
from hypothesis import strategies as st

_PT = "áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ"


@given(st.text(alphabet=_PT + "abcXYZ ,.!?", max_size=40))
def test_accent_overlay_costs_utf8_bytes_and_keeps_base_letters(text):
    """Cada acento pt-BR custa 2 bytes (= UTF-8, que e o que o orcamento conta) e, tirando os
    bytes de acento, sobra exatamente o texto transliterado -- nenhuma letra some ou vira '?'.
    O 'í' e glifo proprio (0x3E, 1 byte): custa 1 a menos e volta a ser 'i' na comparacao."""
    import connector_io
    from extract import encode_string
    raw = encode_string(text, strict=True)
    assert len(raw) == len(text.encode("utf-8")) - text.count("í")
    assert (bytes(b for b in raw if b < 0xA0).decode("ascii").replace(">", "i")
            == connector_io.transliterate(text))
    assert encode_string(decode_string(raw), strict=True) == raw


def test_extend_atlas_is_idempotent_and_keeps_stock_glyphs():
    import font
    stock = bytes(range(1, 256)) * 200
    stock = stock[:font.STOCK * font.GLYPH]
    toc = struct.pack("<4I", 0xA0, 0, 0, 0) * 9 + struct.pack("<4I", 0xA0, len(stock), 5, 0x18000000)
    dat = font.extend_atlas(toc + stock)
    off, size = struct.unpack_from("<2I", dat, font.SECTION * 16)
    slot = (font.I_ACUTE - 0x20) * font.GLYPH       # unica vaga original redesenhada ('í')
    assert size == (0xAC - 0x20) * font.GLYPH
    assert dat[off:off + slot] == stock[:slot] and dat[off + slot + font.GLYPH:off + len(stock)] == stock[slot + font.GLYPH:]
    assert font.extend_atlas(dat) == dat


def test_zero_param_inside_string_is_kept_and_survives_rebuild():
    """0x00 pode ser parametro de control code ([14][00][00]"..."): a string vai ate o proximo
    ponteiro. Cortar no primeiro 0x00 perdia o resto da fala na extracao E na reinsercao."""
    from extract import encode_string
    a, b, c = b'\x14\x00\x00"Hi there"', b'Wha-\x0e\x0f\x00What now?', b'Bye'
    table = struct.pack("<3H", 6, 6 + len(a) + 1, 6 + len(a) + len(b) + 2)
    section = table + a + b"\x00" + b + b"\x00" + c + b"\x00"
    assert [s[2] for s in extract_section_strings(section)] == [a, b, c]
    assert decode_string(a) == '[14][00][00]"Hi there"' and encode_string(decode_string(b)) == b
    new = rebuild_section(section, {2: "Tchau, ate mais"})
    assert [s[2] for s in extract_section_strings(new)] == [a, b, b"Tchau, ate mais"]


def test_pointer_into_middle_of_string_stays_glued_after_rebuild():
    """Sharing: ptr 1 aponta para o meio da string de ptr 0 -- o trecho 0 nao ganha terminador."""
    table = struct.pack("<3H", 6, 6 + 6, 6 + 12)
    section = table + b"Hello World\x00" + b"End\x00"
    new = rebuild_section(section, {2: "Fim da linha"})
    assert new[6:18] == b"Hello World\x00" and struct.unpack_from("<3H", new) == (6, 12, 18)


@given(st.binary(max_size=3000), st.integers(0, 40))
def test_image_codec_round_trip(data, repeat):
    """Codec das secoes de imagem (LZ77 + Huffman dinamico): o que `encode` grava, `decode` devolve
    igual -- inclusive com repeticao longa (copias) e fluxo vazio (so o marcador de fim)."""
    import imgcodec
    raw = data + data[:64] * repeat
    assert imgcodec.decode(imgcodec.encode(raw), len(raw)) == raw


def test_image_codec_refuses_stream_past_tree_rebuild():
    """Acima de 32768 simbolos o jogo reconstroi a arvore com regra nao decodificada: recusar e melhor
    que gravar imagem que o jogo abre errado."""
    import random

    import imgcodec
    with pytest.raises(NotImplementedError):
        imgcodec.encode(random.Random(0).randbytes(imgcodec.REBUILD + 8))


def test_chapter_card_patch_swaps_only_the_card_section():
    pytest.importorskip("PIL")
    import cards
    import imgcodec
    if not cards.FONT.is_file():
        pytest.skip("fonte do cartao ausente")
    old = imgcodec.encode(bytes(32768))
    name, sec = next(iter(cards.SECTIONS.items()))
    toc_size = (sec + 2) * 16
    toc = b"".join(struct.pack("<4I", toc_size, 0, 0, 0) for _ in range(sec))
    toc += struct.pack("<4I", toc_size, len(old), cards.FLAGS, 0x12000208)
    toc += struct.pack("<4I", toc_size + len(old), 4, 0, 0)
    dat = cards.patch(name, toc + old + b"tail")
    off, size = struct.unpack_from("<2I", dat, sec * 16)
    assert imgcodec.untile(imgcodec.decode(dat[off:off + size], 32768), cards.COLS) == cards.render()
    assert dat[struct.unpack_from("<I", dat, (sec + 1) * 16)[0]:] == b"tail"
    assert cards.patch("AREAD001.DAT", toc + old) == toc + old


def test_short_scene_with_fixed_256_pointer_table_is_found():
    """Cena curta: tabela fixa de 256 ponteiros, poucas falas, o resto repete o ultimo ponteiro.
    O corte antigo (5% de destinos unicos) descartava a secao e a cena ficava fora do corpus."""
    strings = [b'"Something is wrong here, line %d of this short scene."' % n for n in range(11)]
    ptrs, pos = [], 512
    for text in strings:
        ptrs.append(pos)
        pos += len(text) + 1
    table = struct.pack("<256H", *ptrs, *[ptrs[-1]] * (256 - len(ptrs)))
    section = table + b"".join(t + b"\x00" for t in strings)
    dat = struct.pack("<4I", 32, 0, 0, 0) + struct.pack("<4I", 32, len(section), 0, 0) + section
    found = find_text_section(dat, parse_toc(dat))
    assert found == (1, 32, len(section))
    assert [x[2] for x in extract_section_strings(section)] == strings + strings[-1:] * 245


# ---------------------------------------------------------------------------
# Secao-conteiner (sub-blocos de texto dentro de uma secao): trocar um sub-bloco nao mexe nos outros
# ---------------------------------------------------------------------------
def _block(strings: list[bytes]) -> bytes:
    first_ptr, blob, ptrs = len(strings) * 2, bytearray(), []
    for s in strings:
        ptrs.append(first_ptr + len(blob))
        blob += s + b"\x00"
    raw = b"".join(struct.pack("<H", p) for p in ptrs) + bytes(blob)
    return raw + b"\x00" * (-len(raw) % 4)


_NAME = st.text(alphabet="abcXYZ '", min_size=1, max_size=14).filter(lambda s: s.strip())


@given(st.lists(st.lists(_NAME, min_size=2, max_size=5), min_size=2, max_size=4), st.data())
def test_nested_block_roundtrip(tables, data):
    from extract import _SUB_BASE, decode_string, sub_blocks

    blocks = [_block([n.encode() for n in t]) for t in tables]
    head = len(blocks) * 4
    offs = [head + sum(len(b) for b in blocks[:i]) for i in range(len(blocks))]
    parent = b"".join(struct.pack("<I", o) for o in offs) + b"".join(blocks)
    tail = b"\xAA" * 8
    toc = bytearray(48)
    struct.pack_into("<IIII", toc, 0, 48, 0, 0, 0)
    struct.pack_into("<IIII", toc, 16, 48, len(parent), 0, 0)
    struct.pack_into("<IIII", toc, 32, 48 + len(parent), len(tail), 0, 0)
    dat = bytes(toc) + parent + tail

    k = data.draw(st.integers(0, len(blocks) - 1))
    new_names = {i: data.draw(_NAME) for i in range(len(tables[k]))}
    out = dat
    for j, blk in enumerate(blocks):        # identidade em todos, traducao so no k
        tr = new_names if j == k else {i: decode_string(n.encode()) for i, n in enumerate(tables[j])}
        out = patch_dat_file(out, _SUB_BASE + 100 + j, rebuild_section(blk, tr))

    entries = parse_toc(out)
    sec = out[entries[1][0]:entries[1][0] + entries[1][1]]
    assert out[entries[2][0]:entries[2][0] + entries[2][1]] == tail
    for j, (a, b) in enumerate(sub_blocks(sec)):
        got = [decode_string(raw) for _i, _p, raw in extract_section_strings(sec[a:b])]
        assert got == ([new_names[i] for i in range(len(tables[k]))] if j == k else tables[j])


def test_system_scenes_match_project_json():
    """A trava 'API so traduz dialogo' le `system_scenes` do project.json: tem de bater com o conector."""
    import json
    from pathlib import Path

    import extract
    cfg = json.loads((Path(__file__).resolve().parent.parent / 'project.json').read_text(encoding='utf-8'))
    want = {f[:-4] for f in list(extract._SYSTEM_SECTIONS) + list(extract._NESTED_SECTIONS)}
    assert set(cfg['system_scenes']) == want
