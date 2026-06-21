"""
test_roundtrip.py — testes de contrato do conector (Breath of Fire IV)

Rodar: pytest connector/test_roundtrip.py -v
Rodar com jogo: pytest connector/test_roundtrip.py -v --dat-dir "C:/...english/DAT"
"""

import csv
import hashlib
import os
import re
import struct
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
EXTRACT_SCRIPT = PROJECT_ROOT / "connector" / "extract.py"
REINSERT_SCRIPT = PROJECT_ROOT / "connector" / "reinsert.py"
DIALOGS_CSV = PROJECT_ROOT / "artifacts" / "dialogs.csv"

# Adiciona connector/ ao path para importar diretamente
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
from extract import decode_string, encode_string, parse_toc, find_text_section, extract_section_strings


# ---------------------------------------------------------------------------
# Fixture: diretório DAT (opcional via --dat-dir ou env DAT_DIR)
# pytest_addoption está em conftest.py
# ---------------------------------------------------------------------------
@pytest.fixture
def dat_dir(request):
    d = request.config.getoption("--dat-dir") or os.environ.get("DAT_DIR")
    if d:
        return Path(d)
    return None


# ---------------------------------------------------------------------------
# Testes de codec (sempre rodam)
# ---------------------------------------------------------------------------
def test_encode_decode_roundtrip_ascii():
    """encode(decode(raw)) deve ser byte-idêntico ao original para strings ASCII puras."""
    samples = [
        b"Hello, World!",
        b"Checking MEMORY CARD...",
        b"You can rest here.",
        b"",
    ]
    for raw in samples:
        decoded = decode_string(raw)
        encoded = encode_string(decoded)
        assert encoded == raw, f"Falha para {raw!r}: decode={decoded!r} encode={encoded!r}"


def test_encode_decode_roundtrip_ctrl_codes():
    """encode(decode(raw)) preserva tokens de controle."""
    samples = [
        bytes([0x14, 0xC1, 0x40, 0x01, 0x02]),
        bytes([0x0C, 0x05, 0x14, 0x01, 0x4E, 0x6F, 0x00]),
        bytes(range(0x00, 0x20)),
        bytes([0x7F, 0x80, 0xFF]),
    ]
    for raw in samples:
        if b'\x00' in raw:
            raw = raw.split(b'\x00')[0]
        decoded = decode_string(raw)
        encoded = encode_string(decoded)
        assert encoded == raw, f"Falha ctrl para {raw.hex()}: {decoded!r}"


def test_ctrl_code_representation():
    """Tokens de controle devem ser representados como [XX] maiúsculo."""
    raw = bytes([0x01, 0x02, 0x0B, 0x0C, 0x14])
    decoded = decode_string(raw)
    assert decoded == "[01][02][0B][0C][14]"


def test_encode_decode_mixed():
    """Strings mistas ASCII + ctrl codes."""
    raw = b"\x14\xC1\x40" + b'"Hello, friend!"' + b"\x02"
    decoded = decode_string(raw)
    encoded = encode_string(decoded)
    assert encoded == raw


# ---------------------------------------------------------------------------
# Testes de formato (sempre rodam, sobre arquivos reais se dat_dir disponível)
# ---------------------------------------------------------------------------
def test_dialogs_csv_schema():
    """dialogs.csv deve ter colunas obrigatórias quando existir."""
    if not DIALOGS_CSV.exists():
        pytest.skip("dialogs.csv não existe ainda")
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
    assert "offset" in cols, "Coluna 'offset' ausente"
    assert "byte_budget" in cols, "Coluna 'byte_budget' ausente"
    assert any(c.startswith("text_") for c in cols), "Nenhuma coluna text_* presente"


def test_dialogs_csv_offset_format():
    """Offsets em dialogs.csv devem seguir o formato FILE:entry:ptr."""
    if not DIALOGS_CSV.exists():
        pytest.skip("dialogs.csv não existe ainda")
    pattern = re.compile(r'^[A-Z0-9_]+\.DAT:\d+:\d+$')
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            assert pattern.match(row["offset"]), f"Formato inválido: {row['offset']!r}"


def test_dialogs_csv_byte_budget_positive():
    """byte_budget deve ser >= 1 para todas as strings."""
    if not DIALOGS_CSV.exists():
        pytest.skip("dialogs.csv não existe ainda")
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            assert int(row["byte_budget"]) >= 1, f"byte_budget inválido: {row}"


# ---------------------------------------------------------------------------
# Teste de round-trip (requer --dat-dir)
# ---------------------------------------------------------------------------
@pytest.mark.skipif(
    not DIALOGS_CSV.exists(),
    reason="dialogs.csv não existe — rodar extract.py primeiro"
)
def test_round_trip_byte_identical(dat_dir, tmp_path):
    """
    Para cada arquivo com texto, extract → reinsert sem tradução → byte-idêntico ao original.
    Requer --dat-dir ou env DAT_DIR.
    """
    if dat_dir is None:
        pytest.skip("Passe --dat-dir <english/DAT> para rodar o round-trip test")

    # Lê quais arquivos têm texto
    files_tested = set()
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            files_tested.add(row["file"])

    errors = []
    for fname in sorted(files_tested)[:20]:  # Testa os primeiros 20 arquivos
        dat_path = dat_dir / fname
        if not dat_path.exists():
            continue

        original = dat_path.read_bytes()
        entries = parse_toc(original)
        if len(entries) < 2:
            continue

        result = find_text_section(original, entries)
        if result is None:
            continue

        entry_idx, sec_off, sec_sz = result
        section = original[sec_off:sec_off + sec_sz]
        strings = extract_section_strings(section)

        # Re-encode todas as strings sem tradução (identidade)
        identity_translations = {
            ptr_idx: decode_string(raw)
            for ptr_idx, _ptr, raw in strings
        }

        from reinsert import rebuild_section, patch_dat_file
        new_section = rebuild_section(section, identity_translations)
        new_data = patch_dat_file(original, entry_idx, new_section)

        if new_data != original:
            # Encontra primeira diferença
            for i, (a, b) in enumerate(zip(original, new_data)):
                if a != b:
                    errors.append(f"{fname}: primeiro byte diferente em 0x{i:X} (orig={a:02X} new={b:02X})")
                    break
            if len(new_data) != len(original):
                errors.append(f"{fname}: tamanho original={len(original)} new={len(new_data)}")

    assert not errors, "Round-trip falhou:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# Invariantes estruturais (sempre rodam)
# ---------------------------------------------------------------------------
def test_no_hardcoded_paths_in_connector_scripts():
    """Scripts do conector não devem ter caminhos absolutos hardcoded."""
    abs_path_rx = re.compile(r'(?:[A-Za-z]:\\|/home/|/Users/|/root/)')
    connector_dir = PROJECT_ROOT / "connector"
    for py_file in connector_dir.glob("*.py"):
        if py_file.name.startswith("test_"):
            continue
        source = py_file.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(source.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if abs_path_rx.search(line):
                pytest.fail(f"{py_file.name}:{i} — caminho absoluto: {line.strip()!r}")


def test_no_hardcoded_work_text_in_connector_scripts():
    """Scripts do conector não devem conter texto da obra hardcoded."""
    if not DIALOGS_CSV.exists():
        assert EXTRACT_SCRIPT.exists()
        assert REINSERT_SCRIPT.exists()
        return

    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        text_cols = [c for c in (reader.fieldnames or []) if c.startswith("text_")]
        texts = {
            row[col].strip().lower()
            for row in reader
            for col in text_cols
            if row.get(col, "").strip()
        }

    connector_dir = PROJECT_ROOT / "connector"
    for py_file in connector_dir.glob("*.py"):
        if py_file.name.startswith("test_"):
            continue
        source = py_file.read_text(encoding="utf-8", errors="replace").lower()
        for text in texts:
            if len(text) > 8 and text in source:
                pytest.fail(f"{py_file.name} contém texto da obra: {text[:60]!r}")
