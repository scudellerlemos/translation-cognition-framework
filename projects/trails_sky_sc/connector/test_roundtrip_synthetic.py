"""
test_roundtrip_synthetic.py — oráculo de round-trip SEMPRE ativo em CI.

Monta, EM MEMÓRIA, um contêiner FPAC sintético com 1 arquivo `scena/e0000.dat` (`#scp` +
strings heurísticas) — não é o jogo, é um fixture pequeno e comitável que exercita a MESMA
lógica determinística (`_scan_strings` / `rebuild_pac` / `read_scena_strings`) usada por
extract.py/reinsert.py sobre o `.pac` real. Roda sempre, sem skip, sem depender do jogo
instalado (que é gitignored/licenciado — ver test_roundtrip.py pro gate contra dado real).
"""
import struct
import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
from extract import _scan_strings  # noqa: E402
from fpac_unpack import read_index  # noqa: E402
from reinsert import read_scena_strings, rebuild_pac, truncate_for_budget  # noqa: E402

_HEADER = struct.Struct("<4sIII")
_ENTRY = struct.Struct("<IIQQQ")


def _build_scena_dat() -> bytes:
    """`#scp` sintético: header de 16 bytes (magic + 3 campos dummy) + bytecode fake com 2
    strings de diálogo (com espaço, devem ser extraídas) e 1 label de função sem espaço
    (deve ser filtrado — mesmo padrão de `sound.PlayBGM`/`OnMapReinit` no jogo real)."""
    body = (
        b"\x01\x02\x03"
        b"OnMapReinit\x00"                            # label -> sem espaco, filtrado
        b"\x04\x05"
        b"Our story begins in Rolent.\x00"            # dialogo 1
        b"\x06"
        b"My name is Estelle Bright.\x00"              # dialogo 2
        b"\x07\x08\x09"
    )
    header = struct.pack("<4sIII", b"#scp", 0x18, 0, 1)
    return header + body


def _build_fpac(files: dict[str, bytes]) -> bytes:
    """Espelha fpac_unpack._demo() — monta um contêiner FPAC mínimo válido a partir de
    {nome: conteúdo}."""
    names = list(files.keys())
    contents = list(files.values())

    name_table = b"\x00".join(n.encode("ascii") for n in names) + b"\x00"
    name_offsets = []
    pos = 0
    for n in names:
        name_offsets.append(pos)
        pos += len(n) + 1

    entries_size = _ENTRY.size * len(names)
    name_table_addr = _HEADER.size + entries_size
    data_start = name_table_addr + len(name_table)

    data_blobs = b""
    data_addrs = []
    pos = data_start
    for c in contents:
        data_addrs.append(pos)
        data_blobs += c
        pos += len(c)

    entries_bytes = b"".join(
        _ENTRY.pack(0, 0, name_table_addr + name_offsets[i], len(contents[i]), data_addrs[i])
        for i in range(len(names))
    )

    return (
        _HEADER.pack(b"FPAC", len(names), data_start, 1)
        + entries_bytes + name_table + data_blobs
    )


def _fixture_pac() -> bytes:
    return _build_fpac({
        "script_en/scena/e0000.dat": _build_scena_dat(),
        "script_en/ani/fis0016.dat": b"nao e scena, fora do escopo do extract\x00",
    })


def _load(pac_bytes: bytes):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "script_en.pac"
        p.write_bytes(pac_bytes)
        return read_index(p)


def test_scan_strings_filters_labels_without_space():
    strings = dict(_scan_strings(_build_scena_dat()))
    assert "Our story begins in Rolent." in strings.values()
    assert "My name is Estelle Bright." in strings.values()
    assert "OnMapReinit" not in strings.values()


def test_only_scena_dat_files_are_in_scope():
    _data, entries = _load(_fixture_pac())
    names = [e[0] for e in entries]
    assert "script_en/scena/e0000.dat" in names
    assert "script_en/ani/fis0016.dat" in names  # no indice do FPAC, mas fora do escopo de extract/reinsert


def test_roundtrip_identity_byte_for_byte():
    """rebuild_pac(translations={}) reproduz o .pac sintético byte-a-byte — o oráculo central."""
    data, entries = _load(_fixture_pac())
    new_bytes, changed = rebuild_pac(data, entries, {}, {})
    assert changed == 0
    assert new_bytes == data, "round-trip de identidade NAO e byte-identico"


def test_roundtrip_translated_reextracts_correctly():
    """Traduz 1 string, reinsere e re-extrai: a string alvo muda, as vizinhas não."""
    data, entries = _load(_fixture_pac())
    original = read_scena_strings(data, entries)
    target_key = next(k for k, v in original.items() if v == "Our story begins in Rolent.")
    budgets = {k: len(v) + 1 for k, v in original.items()}

    # probe >= _MIN_LEN e com espaco -- read_scena_strings re-varre com a MESMA heuristica de
    # extract.py; uma traducao curta ("Oi") ficaria abaixo do MIN_LEN e desapareceria do
    # re-scan (falso negativo do helper de teste, nao do reinsert -- reinsert.py real nao
    # depende de re-scan, escreve direto no offset conhecido via dialogs.csv).
    new_bytes, changed = rebuild_pac(data, entries, {target_key: "Oi, tudo bem?"}, budgets)
    assert changed == 1

    reextracted = read_scena_strings(new_bytes, entries)
    assert reextracted[target_key] == "Oi, tudo bem?"
    for key, text in original.items():
        if key == target_key:
            continue
        assert reextracted[key] == text, f"{key} mudou sem ser tocada"


def test_roundtrip_accented_translation_utf8_safe_truncation():
    """pt-BR acentuado (UTF-8) grava corretamente e, quando truncado, nunca corta um caractere
    multibyte ao meio -- charset do #scp confirmado como UTF-8 em 2026-08-23 (ver
    table_schema.md), reinsert.py trocou de .encode("ascii") pra .encode("utf-8")."""
    data, entries = _load(_fixture_pac())
    original = read_scena_strings(data, entries)
    target_key = next(k for k, v in original.items() if v == "My name is Estelle Bright.")
    budgets = {k: len(v) + 1 for k, v in original.items()}

    text_pt = "Nome: é"
    budget = budgets[target_key]
    assert len(text_pt.encode("utf-8")) <= budget - 1, "fixture do teste precisa caber no budget"
    new_bytes, changed = rebuild_pac(data, entries, {target_key: text_pt}, budgets)
    assert changed == 1

    file_part, _, off_part = target_key.partition(":")
    name, _size, addr, _crc = next(e for e in entries if e[0].endswith(file_part))
    offset = int(off_part, 16)
    abs_off = addr + offset
    written = new_bytes[abs_off:abs_off + budget]
    assert written.decode("utf-8") == text_pt + "\x00" * (budget - len(text_pt.encode("utf-8")))

    # texto mais longo, forcando truncamento bem no meio de um caractere multibyte
    long_text = "Meu nome verdadeiro é Estellê Br" + "í" * 10
    new_bytes2, changed2 = rebuild_pac(data, entries, {target_key: long_text}, budgets)
    assert changed2 == 1
    written2 = new_bytes2[abs_off:abs_off + budget]
    payload = written2.rstrip(b"\x00")
    decoded = payload.decode("utf-8")  # nao pode levantar UnicodeDecodeError
    assert long_text.startswith(decoded)
    assert len(payload) <= budget - 1


def test_roundtrip_translation_longer_than_budget_is_truncated():
    """pt-BR mais longo que o budget original é truncado, sem corromper a string vizinha —
    consequência documentada do replace same-size (ver docstring de reinsert.py)."""
    data, entries = _load(_fixture_pac())
    original = read_scena_strings(data, entries)
    target_key = next(k for k, v in original.items() if v == "My name is Estelle Bright.")
    budgets = {k: len(v) + 1 for k, v in original.items()}

    long_text = "Este texto em portugues e bem mais longo que o original em ingles"
    new_bytes, changed = rebuild_pac(data, entries, {target_key: long_text}, budgets)
    assert changed == 1

    reextracted = read_scena_strings(new_bytes, entries)
    assert reextracted[target_key] == long_text[: budgets[target_key] - 1]
    for key, text in original.items():
        if key == target_key:
            continue
        assert reextracted[key] == text, f"{key} foi corrompida pelo truncamento da vizinha"


# --------------------- Hypothesis: truncate_for_budget (CLAUDE.md) -----------------

@given(text=st.text(), budget=st.integers(min_value=1, max_value=256))
@settings(max_examples=200)
def test_truncate_for_budget_always_exact_size(text, budget):
    """Para qualquer texto/budget, o payload gravado tem SEMPRE exatamente `budget` bytes
    (invariante do replace same-size do reinsert.py — nunca pode desalinhar a string seguinte)."""
    payload = truncate_for_budget(text, budget)
    assert len(payload) == budget


@given(text=st.text(), budget=st.integers(min_value=1, max_value=256))
@settings(max_examples=200)
def test_truncate_for_budget_never_splits_multibyte_utf8(text, budget):
    """O payload, sem o padding de \\0, decodifica como UTF-8 valido e e sempre um PREFIXO do
    texto original -- nunca corta um caractere multibyte ao meio (bug historico do reinsert.py
    antes de trocar .encode("ascii") por .encode("utf-8"))."""
    payload = truncate_for_budget(text, budget)
    stripped = payload.rstrip(b"\x00")
    decoded = stripped.decode("utf-8")          # nao pode levantar UnicodeDecodeError
    assert text.startswith(decoded)
    assert len(stripped) <= budget - 1


# ------------------ Hypothesis: rebuild_pac (roundtrip generalizado) --------------

@given(new_text=st.text(min_size=1, max_size=80))
@settings(max_examples=50)
def test_roundtrip_arbitrary_translation_never_corrupts_neighbor(new_text):
    """Generaliza test_roundtrip_translated_reextracts_correctly: qualquer texto (curto, longo,
    acentuado, vazio de espaco) aplicado a UMA string nunca corrompe a string vizinha nem
    ultrapassa o budget original."""
    data, entries = _load(_fixture_pac())
    original = read_scena_strings(data, entries)
    target_key = next(k for k, v in original.items() if v == "My name is Estelle Bright.")
    budgets = {k: len(v) + 1 for k, v in original.items()}

    new_bytes, changed = rebuild_pac(data, entries, {target_key: new_text}, budgets)
    assert changed == 1

    file_part, _, off_part = target_key.partition(":")
    _name, _size, addr, _crc = next(e for e in entries if e[0].endswith(file_part))
    abs_off = addr + int(off_part, 16)
    budget = budgets[target_key]
    written = new_bytes[abs_off:abs_off + budget].rstrip(b"\x00")
    assert len(written) <= budget - 1
    assert new_text.startswith(written.decode("utf-8"))

    # vizinha inalterada byte-a-byte fora da janela [abs_off, abs_off+budget) da string traduzida
    assert new_bytes[:abs_off] == data[:abs_off]
    assert new_bytes[abs_off + budget:] == data[abs_off + budget:]
