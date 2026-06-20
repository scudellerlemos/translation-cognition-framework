#!/usr/bin/env python3
"""
extract.py — Breath of Fire IV (PC port, Capcom, 2000)

Contrato (ver framework/connectors/hex_binary.md):
    entrada : diretório english/DAT do jogo (CLI arg ou project.json[connector][game_dat_dir])
    saída   : artifacts/dialogs.csv (offset, file, entry_idx, ptr_idx, text_en, byte_budget)
              artifacts/extraction_log.md

Regras:
- 100% determinístico. NUNCA usar LLM aqui.
- Compartilha encode/decode com reinsert.py (garante round-trip).
- byte_budget = len(raw_bytes) + 1 (inclui terminador null).
"""

import csv
import json
import re
import struct
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Constantes do formato
# ---------------------------------------------------------------------------
_ASCII_RANGE = range(0x20, 0x7F)
_CTRL_RE = re.compile(r'\[([0-9A-Fa-f]{2})\]')


# ---------------------------------------------------------------------------
# 1. ENCODE / DECODE  (round-trip perfeito)
# ---------------------------------------------------------------------------
def decode_string(raw: bytes) -> str:
    """Bytes sem terminador → string CSV. ASCII → chr, outros → [XX]."""
    parts = []
    for b in raw:
        if b in _ASCII_RANGE:
            parts.append(chr(b))
        else:
            parts.append(f'[{b:02X}]')
    return ''.join(parts)


def encode_string(text: str) -> bytes:
    """String CSV → bytes sem terminador. Inverso de decode_string."""
    out = bytearray()
    i = 0
    while i < len(text):
        m = _CTRL_RE.match(text, i)
        if m:
            out.append(int(m.group(1), 16))
            i = m.end()
        else:
            ch = text[i]
            if ord(ch) in _ASCII_RANGE:
                out.append(ord(ch))
            else:
                # Caracter fora do ASCII imprimível — transliterar para '?' para segurança
                out.append(0x3F)
            i += 1
    return bytes(out)


# ---------------------------------------------------------------------------
# 2. PARSER DE TOC
# ---------------------------------------------------------------------------
def parse_toc(data: bytes) -> list[tuple[int, int, int, int]]:
    """Retorna lista de (offset, size, flags, type) para cada entrada do TOC."""
    if len(data) < 4:
        return []
    toc_size = struct.unpack_from('<I', data, 0)[0]
    if toc_size == 0 or toc_size > min(len(data), 0x10000):
        return []
    entries = []
    for i in range(toc_size // 16):
        off = i * 16
        if off + 16 > toc_size:
            break
        v0, v1, v2, v3 = struct.unpack_from('<IIII', data, off)
        entries.append((v0, v1, v2, v3))
    return entries


# ---------------------------------------------------------------------------
# 3. LOCALIZAR SEÇÃO DE TEXTO
# ---------------------------------------------------------------------------
def find_text_section(data: bytes, entries: list) -> tuple[int, int, int] | None:
    """
    Heurística robusta: procura seção com tabela de ponteiros 2-byte + strings ASCII.

    Critérios (todos devem ser satisfeitos para pontuar):
    1. first_ptr (tamanho da tabela) está em [4, min(0x1000, sz/2)]
    2. Ao menos 70% dos ponteiros na tabela apontam para [first_ptr, sz)
    3. Conteúdo após a tabela tem >= 40% de bytes ASCII
    4. Conteúdo pós-tabela cabe em uint16 (total bytes < 0xFFFF)

    Retorna (entry_idx, section_offset, section_size) ou None.
    """
    best = None
    best_score = 0.0

    for i, (off, sz, _flags, _typ) in enumerate(entries[1:], 1):
        if sz < 64 or off == 0 or off + sz > len(data):
            continue
        section = data[off:off + sz]

        # Tabela de ponteiros: primeiro uint16 = tamanho da tabela em bytes
        first_ptr = struct.unpack_from('<H', section, 0)[0]
        # first_ptr deve ser pequeno (máx. 0x1000=4096 bytes = 2048 entradas)
        # e não pode ser maior que metade da seção
        if first_ptr < 4 or first_ptr >= sz or first_ptr > min(0x1000, sz // 2):
            continue

        # Critério 2: maioria dos ponteiros deve apontar para dentro da seção
        ptr_count = first_ptr // 2
        valid_ptrs = 0
        for p in range(0, first_ptr, 2):
            if p + 2 > len(section):
                break
            v = struct.unpack_from('<H', section, p)[0]
            if first_ptr <= v < sz:
                valid_ptrs += 1
        if ptr_count > 0 and (valid_ptrs / ptr_count) < 0.70:
            continue

        # Critério 3: conteúdo após a tabela deve ser majoritariamente ASCII
        sample = section[first_ptr:first_ptr + 256]
        if len(sample) < 10:
            continue

        ascii_count = sum(1 for b in sample if b in _ASCII_RANGE)
        ascii_pct = ascii_count / len(sample)
        if ascii_pct < 0.40:
            continue

        # Critério 4: total de bytes de strings deve caber em uint16
        # (ponteiros são uint16 relativos ao início da seção)
        if sz > 0xFFFF:
            continue

        words = re.findall(rb'[A-Za-z]{4,}', sample)
        score = ascii_pct * 100 + len(words) * 5 + valid_ptrs * 0.1

        if score > best_score:
            best_score = score
            best = (i, off, sz)

    return best


# ---------------------------------------------------------------------------
# 4. EXTRAIR STRINGS DA SEÇÃO
# ---------------------------------------------------------------------------
def extract_section_strings(section: bytes) -> list[tuple[int, int, bytes]]:
    """
    Retorna lista de (ptr_idx, ptr_offset_in_section, raw_bytes_sem_terminador).
    ptr_idx = índice na tabela de ponteiros.
    Aliases (dois índices com mesmo offset) são listados separadamente.
    """
    if len(section) < 4:
        return []
    first_ptr = struct.unpack_from('<H', section, 0)[0]
    if first_ptr < 2 or first_ptr > len(section):
        return []

    results = []
    for i in range(0, first_ptr, 2):
        if i + 2 > len(section):
            break
        ptr = struct.unpack_from('<H', section, i)[0]
        if ptr < first_ptr or ptr >= len(section):
            continue
        end = section.find(b'\x00', ptr)
        if end == -1:
            end = min(ptr + 255, len(section))
        raw = section[ptr:end]
        results.append((i // 2, ptr, raw))

    return results


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
def main(project_json: Path, source_override: str | None = None) -> None:
    cfg = json.loads(project_json.read_text(encoding='utf-8'))
    root = project_json.parent

    # Resolve diretório DAT do jogo
    if source_override:
        game_dat_dir = Path(source_override)
    else:
        game_dat_dir = Path(cfg['connector'].get('game_dat_dir', ''))

    if not game_dat_dir.is_dir():
        raise SystemExit(
            f"Diretório DAT não encontrado: {game_dat_dir}\n"
            "Passe o caminho como CLI: python extract.py project.json <DAT_DIR>"
        )

    rows: list[dict] = []
    files_processed = 0
    files_with_text = 0

    for dat_path in sorted(game_dat_dir.glob('*.DAT')):
        fname = dat_path.name
        data = dat_path.read_bytes()
        if len(data) < 64:
            continue

        entries = parse_toc(data)
        if len(entries) < 2:
            continue

        result = find_text_section(data, entries)
        if result is None:
            continue

        entry_idx, sec_off, sec_sz = result
        section = data[sec_off:sec_off + sec_sz]
        strings = extract_section_strings(section)
        files_processed += 1

        file_has_text = False
        for ptr_idx, _ptr, raw in strings:
            if not any(b in _ASCII_RANGE for b in raw):
                continue
            file_has_text = True
            string_id = f"{fname}:{entry_idx}:{ptr_idx}"
            rows.append({
                'offset': string_id,
                'file': fname,
                'entry_idx': entry_idx,
                'ptr_idx': ptr_idx,
                'text_en': decode_string(raw),
                'byte_budget': len(raw) + 1,
            })

        if file_has_text:
            files_with_text += 1

    # Grava dialogs.csv
    out_csv = root / cfg['source']['file']
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['offset', 'file', 'entry_idx', 'ptr_idx', 'text_en', 'byte_budget']
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Grava log
    log = root / 'artifacts' / 'extraction_log.md'
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(
        f"# Extraction Log — Breath of Fire IV\n\n"
        f"- Diretório DAT: `{game_dat_dir}`\n"
        f"- Arquivos com seção de texto: {files_with_text}\n"
        f"- Total de strings extraídas: {len(rows)}\n"
        f"- Container: Capcom DAT (TOC + seções)\n"
        f"- Encoding: ASCII com escapes hex `[XX]`\n",
        encoding='utf-8',
    )
    print(f"Extraídas {len(rows)} strings de {files_with_text} arquivos -> {out_csv}")


if __name__ == '__main__':
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('project.json')
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
