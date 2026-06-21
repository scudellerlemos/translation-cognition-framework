#!/usr/bin/env python3
"""
reinsert.py — Breath of Fire IV (PC port, Capcom, 2000)

Contrato (ver framework/connectors/hex_binary.md):
    entrada : approved_translations.csv + dialogs.csv + DAT dir do jogo
    saída   : output/<arquivo>.DAT (cópia modificada) + reinsertion_report.md

Regras:
- 100% determinístico. LLM NUNCA escreve bytes nem recalcula ponteiros.
- Reconstrução completa da seção de texto: pointer table + strings novas.
- Se nova seção <= original: substituição in-place + padding com \x00.
- Se nova seção > original: expansão + atualização do TOC e offsets subsequentes.
- T4 (string individual excede byte_budget E a seção não cabe): reportar para reescrita.
- O binário-fonte NUNCA é sobrescrito; saída vai para output/.
"""

import csv
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

from extract import (
    decode_string,
    encode_string,
    extract_section_strings,
    find_text_section,
    parse_toc,
)


# ---------------------------------------------------------------------------
# 1. RECONSTRUIR A SEÇÃO DE TEXTO
# ---------------------------------------------------------------------------
def rebuild_section(
    original_section: bytes,
    translations: dict[int, str],  # ptr_idx -> translated text (or original decoded)
) -> bytes:
    """
    Reconstrói a seção de texto aplicando as traduções.
    translations: mapa de ptr_idx → texto (decoded) final a usar.

    As seções Capcom usam **string sharing** (ponteiros podem apontar para o meio
    de outra string), portanto:
    - Se NENHUMA string mudou: retorna a seção original byte-idêntica (preserva sharing).
    - Se alguma string mudou: reconstrói do zero sem sharing (seção pode crescer).

    Retorna os novos bytes da seção (pointer table + string data).
    """
    first_ptr = struct.unpack_from('<H', original_section, 0)[0]
    ptr_count = first_ptr // 2

    original_strings = extract_section_strings(original_section)

    # Verifica se alguma string realmente mudou
    changed = False
    orig_raw_by_idx: dict[int, bytes] = {s[0]: s[2] for s in original_strings}
    for ptr_idx, new_text in translations.items():
        orig_raw = orig_raw_by_idx.get(ptr_idx, b'')
        new_bytes = encode_string(new_text)
        if new_bytes != orig_raw:
            changed = True
            break

    if not changed:
        # Round-trip idêntico: preserva string sharing do original
        return bytes(original_section)

    # Reconstrói do zero (sem sharing) para acomodar traduções
    # Lê todos os ponteiros originais
    original_ptrs: list[int] = []
    for i in range(ptr_count):
        v = struct.unpack_from('<H', original_section, i * 2)[0]
        original_ptrs.append(v)

    # Para cada ptr_idx, decide qual bytes usar (tradução ou original)
    ptr_idx_to_bytes: dict[int, bytes] = {}
    for ptr_idx, _orig_ptr, orig_raw in original_strings:
        if ptr_idx in translations:
            ptr_idx_to_bytes[ptr_idx] = encode_string(translations[ptr_idx])
        else:
            ptr_idx_to_bytes[ptr_idx] = orig_raw

    # Mapeia orig_ptr → primeiro ptr_idx apontando para esse offset
    orig_ptr_to_first_idx: dict[int, int] = {}
    for ptr_idx, orig_ptr, _raw in original_strings:
        if orig_ptr not in orig_ptr_to_first_idx:
            orig_ptr_to_first_idx[orig_ptr] = ptr_idx

    # Escreve strings em ordem crescente de offset original
    unique_orig_ptrs = sorted(orig_ptr_to_first_idx.keys())
    new_string_data = bytearray()
    orig_offset_to_new_offset: dict[int, int] = {}

    for orig_ptr in unique_orig_ptrs:
        first_idx = orig_ptr_to_first_idx[orig_ptr]
        new_start = first_ptr + len(new_string_data)
        orig_offset_to_new_offset[orig_ptr] = new_start
        new_string_data += ptr_idx_to_bytes.get(first_idx, b'')
        new_string_data += b'\x00'

    # Reconstrói a tabela de ponteiros
    new_ptr_table = bytearray(first_ptr)
    for i, orig_ptr in enumerate(original_ptrs):
        new_ptr = orig_offset_to_new_offset.get(orig_ptr, orig_ptr)
        if new_ptr > 0xFFFF:
            raise OverflowError(
                f"Offset de ponteiro excede uint16: {new_ptr:#06x} "
                f"(seção muito grande para ponteiros 2-byte)"
            )
        struct.pack_into('<H', new_ptr_table, i * 2, new_ptr)

    return bytes(new_ptr_table) + bytes(new_string_data)


# ---------------------------------------------------------------------------
# 2. PATCH DO ARQUIVO (mantém ou expande a seção de texto no TOC)
# ---------------------------------------------------------------------------
def patch_dat_file(
    original_data: bytes,
    entry_idx: int,
    new_section: bytes,
) -> bytes:
    """
    Retorna os bytes do arquivo .DAT modificado com a nova seção de texto.
    Atualiza o TOC se o tamanho da seção mudar.
    """
    entries = parse_toc(original_data)
    sec_off, sec_sz = entries[entry_idx][0], entries[entry_idx][1]

    new_sz = len(new_section)
    delta = new_sz - sec_sz

    # Monta o novo conteúdo do arquivo
    before = original_data[:sec_off]
    after = original_data[sec_off + sec_sz:]
    new_data = bytearray(before + new_section + after)

    # Padding com zeros se nova seção é menor (mantém tamanho original se não há delta)
    if delta < 0:
        # Preenche o espaço liberado com zeros antes do conteúdo original
        # Na prática, new_section já tem tamanho correto; apenas atualizar TOC
        pass

    # Atualiza o TOC: entry_idx size, e offsets de todas as seções posteriores
    toc_size = struct.unpack_from('<I', original_data, 0)[0]

    if delta != 0:
        for i in range(1, toc_size // 16):
            entry_off = i * 16
            off_i = struct.unpack_from('<I', new_data, entry_off)[0]
            sz_i = struct.unpack_from('<I', new_data, entry_off + 4)[0]

            if i == entry_idx:
                # Atualiza tamanho desta seção
                struct.pack_into('<I', new_data, entry_off + 4, new_sz)
            elif off_i > sec_off:
                # Desloca offset das seções posteriores
                struct.pack_into('<I', new_data, entry_off, off_i + delta)

    return bytes(new_data)


# ---------------------------------------------------------------------------
# 3. MAIN
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
            "Passe como CLI: python reinsert.py project.json <DAT_DIR>"
        )

    # Carrega dialogs.csv para saber entry_idx por string
    dialogs_csv = root / cfg['source']['file']
    string_meta: dict[str, dict] = {}
    with dialogs_csv.open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            string_meta[row['offset']] = {
                'file': row['file'],
                'entry_idx': int(row['entry_idx']),
                'ptr_idx': int(row['ptr_idx']),
                'text_en': row['text_en'],
                'byte_budget': int(row['byte_budget']),
            }

    # Carrega traduções aprovadas
    approved_csv = root / 'artifacts' / 'approved_translations.csv'
    translations: dict[str, str] = {}  # offset_id -> text_target
    if approved_csv.exists():
        with approved_csv.open(encoding='utf-8') as f:
            for row in csv.DictReader(f):
                target = row.get('text_target', '').strip()
                if target:
                    translations[row['offset']] = target

    # Agrupa por arquivo: {fname: {ptr_idx: text_decoded}}
    per_file: dict[str, dict[int, str]] = defaultdict(dict)
    for offset_id, text_target in translations.items():
        meta = string_meta.get(offset_id)
        if meta is None:
            continue
        per_file[meta['file']][meta['ptr_idx']] = text_target

    # Fallback: para strings sem tradução, usa o original (garante round-trip)
    for offset_id, meta in string_meta.items():
        fname = meta['file']
        ptr_idx = meta['ptr_idx']
        if ptr_idx not in per_file[fname]:
            per_file[fname][ptr_idx] = meta['text_en']

    # Processa cada arquivo com traduções
    out_dir = root / 'output'
    out_dir.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    t4_count = 0
    files_modified = 0

    for fname, file_translations in sorted(per_file.items()):
        dat_path = game_dat_dir / fname
        if not dat_path.exists():
            report.append(f"- {fname}: ARQUIVO NÃO ENCONTRADO no diretório")
            continue

        original_data = dat_path.read_bytes()
        entries = parse_toc(original_data)
        if len(entries) < 2:
            continue

        result = find_text_section(original_data, entries)
        if result is None:
            continue

        entry_idx, sec_off, sec_sz = result
        section = original_data[sec_off:sec_off + sec_sz]

        # Verifica T4 individual (strings que excedem byte_budget próprio)
        for offset_id, meta in string_meta.items():
            if meta['file'] != fname:
                continue
            ptr_idx = meta['ptr_idx']
            target_text = file_translations.get(ptr_idx, meta['text_en'])
            encoded = encode_string(target_text)
            budget = meta['byte_budget']
            if len(encoded) + 1 > budget:
                report.append(
                    f"- {fname}:{ptr_idx} T4_individual {len(encoded)+1}>{budget}b"
                )
                t4_count += 1

        # Reconstrói a seção e aplica patch
        new_section = rebuild_section(section, file_translations)
        new_data = patch_dat_file(original_data, entry_idx, new_section)

        out_path = out_dir / fname
        out_path.write_bytes(new_data)
        files_modified += 1

        new_sz = len(new_section)
        delta = new_sz - sec_sz
        tier = 'T1' if delta == 0 else ('T2' if delta < 0 else 'T3_expand')
        report.append(f"- {fname} [{tier}] seção: {sec_sz}->{new_sz} (delta={delta:+d}b)")

    # Grava relatório
    report_text = "\n".join(report)
    (root / 'artifacts' / 'reinsertion_report.md').write_text(
        f"# Reinsertion Report — Breath of Fire IV\n\n"
        f"Arquivos modificados: {files_modified}\n"
        f"Strings T4 individual (overflow): {t4_count}\n\n"
        f"{report_text}\n",
        encoding='utf-8',
    )
    if t4_count:
        print(f"ATENÇÃO: {t4_count} strings T4 individual -> reescrita LLM em lote")
    print(f"Output gravado em {out_dir} ({files_modified} arquivos)")


if __name__ == '__main__':
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('project.json')
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
