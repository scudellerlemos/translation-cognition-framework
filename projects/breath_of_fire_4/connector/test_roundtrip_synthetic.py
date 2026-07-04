"""
test_roundtrip_synthetic.py — oracle de round-trip SEMPRE ativo em CI (#84).

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
    for (ptr_idx, _ptr, raw), expected in zip(strings, _STRINGS):
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
