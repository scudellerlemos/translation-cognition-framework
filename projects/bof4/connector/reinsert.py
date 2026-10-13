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
- Overflow individual (string excede byte_budget E a seção não cabe): reportar para reescrita.
- O binário-fonte NUNCA é sobrescrito; saída vai para output/.
"""

import csv
import json
import math
import struct
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK = _HERE.parent.parent.parent / "framework" / "runtime"
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
for _p in (_FRAMEWORK, _FRAMEWORK_CONNECTORS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import cards  # noqa: E402
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)
import font  # noqa: E402
import labels  # noqa: E402
import paths as _paths  # noqa: E402
from extract import (
    encode_string,
    extract_section_strings,
    parse_toc,
    split_virtual,
    string_spans,
    sub_blocks,
    text_sections,
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

    # Escreve na ordem ORIGINAL dos offsets, e so poe terminador onde o original tinha: ponteiro para
    # o meio de outra string (sharing) continua colado no trecho seguinte. ptr_idx que dividiam o
    # mesmo offset so continuam dividindo se a traducao final for IGUAL; se divergirem, cada um
    # ganha seu slot (antes so a do primeiro alias era gravada e as demais sumiam em silencio).
    spans = string_spans(original_section)
    by_ptr: dict[int, list[int]] = defaultdict(list)
    for ptr_idx, orig_ptr, _raw in original_strings:
        by_ptr[orig_ptr].append(ptr_idx)
    new_string_data = bytearray()
    ptr_idx_to_new_offset: dict[int, int] = {}
    for orig_ptr in sorted(by_ptr):
        terminated = spans[orig_ptr][1]
        written: dict[bytes, int] = {}
        for ptr_idx in by_ptr[orig_ptr]:
            raw = ptr_idx_to_bytes[ptr_idx] if terminated or not written else next(iter(written))
            if raw not in written:
                written[raw] = first_ptr + len(new_string_data)
                new_string_data += raw + (b'\x00' if terminated else b'')
            ptr_idx_to_new_offset[ptr_idx] = written[raw]

    # Reconstrói a tabela de ponteiros
    new_ptr_table = bytearray(original_section[:first_ptr])    # tabela de tamanho impar (0x201): byte final preservado
    for i, orig_ptr in enumerate(original_ptrs):
        new_ptr = ptr_idx_to_new_offset.get(i, orig_ptr)
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
def _toc_alignment(entries: list, toc_size: int) -> int:
    """Maior potencia de 2 (<=16) que divide TODOS os offsets do TOC: alinhamento que o formato ja usa."""
    g = toc_size
    for off, *_ in entries[1:]:
        if off:
            g = math.gcd(g, off)
    a = 1
    while a < 16 and g % (a * 2) == 0:
        a *= 2
    return a


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
    sub = split_virtual(entry_idx)
    if sub:     # sub-bloco de secao-conteiner: troca dentro da secao-mae, acerta o cabecalho dela e segue o caminho normal
        parent_idx, k = sub
        p_off, p_sz = entries[parent_idx][0], entries[parent_idx][1]
        parent = bytearray(original_data[p_off:p_off + p_sz])
        a, b = sub_blocks(bytes(parent))[k]
        # menor que o original: completa com zeros e o cabecalho nao muda; maior: cresce alinhado em 4 como os offsets
        new_section = new_section.ljust(b - a, b'\x00')
        new_section += b'\x00' * (-len(new_section) % 4)
        for j in range(k + 1, struct.unpack_from('<I', parent, 0)[0] // 4):
            struct.pack_into('<I', parent, j * 4, struct.unpack_from('<I', parent, j * 4)[0] + len(new_section) - (b - a))
        parent[a:b] = new_section
        return patch_dat_file(original_data, parent_idx, bytes(parent))
    sec_off, sec_sz = entries[entry_idx][0], entries[entry_idx][1]

    # delta multiplo do alinhamento: as secoes seguintes mantem os offsets alinhados como no original
    align = _toc_alignment(entries, struct.unpack_from('<I', original_data, 0)[0])
    new_section = new_section + b'\x00' * ((sec_sz - len(new_section)) % align)
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
        for i in range(toc_size // 16):      # a entrada 0 tambem: o offset dela e o proprio toc_size (nunca desloca)
            entry_off = i * 16
            off_i = struct.unpack_from('<I', new_data, entry_off)[0]

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

    # Resolve diretório DAT do jogo — CLI > BOF4_DAT_DIR env var > falha (nunca lê de project.json)
    game_dat_dir = connector_io.resolve_source_path(
        cli_arg=source_override, env_var="BOF4_DAT_DIR", allow_missing=True)
    # Path("") == Path(".") (CWD) -- .is_dir() sempre True, entao "nao configurado" (None) precisa
    # de check explicito ANTES do is_dir(), senao a checagem abaixo nunca dispara.
    if game_dat_dir is None or not game_dat_dir.is_dir():
        raise SystemExit(
            "Diretório DAT não configurado.\n"
            "Opções:\n"
            "  1. Variável de ambiente: BOF4_DAT_DIR=<caminho>\n"
            "  2. CLI: python reinsert.py <project_root> <DAT_DIR>\n"
            "Ver projects/bof4/.env.example"
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

    for off, b in cfg.get('byte_budget_exceptions', {}).items():   # excecao pontual, decidida pelo humano
        if off in string_meta:
            string_meta[off]['byte_budget'] = int(b)

    # Carrega traduções aprovadas dos approved_*.csv por cena (artifacts/scenes/<scene>/)
    translations: dict[str, str] = {}  # offset_id -> text_target
    scenes_dir = _paths.scenes_dir(root)
    if not scenes_dir.is_dir():
        sys.exit(f"ERRO: {scenes_dir} nao existe -- rode split_scenes primeiro")
    for scene_dir in sorted(scenes_dir.iterdir()):
        if not scene_dir.is_dir():
            continue
        for appr in sorted(scene_dir.glob("approved_*.csv")):
            with appr.open(encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    target = row.get('text_target') or ''
                    if target.strip():   # strip so p/ testar vazio (igual Souldiers/Trails): espaco final e conteudo
                        translations[row['offset']] = target

    # '?' silencioso no jogo = corrupcao: traducao que nao cabe no ASCII do font aborta ANTES de gravar
    unmappable = []
    for offset_id, text_target in translations.items():
        try:
            encode_string(text_target, strict=True)
        except ValueError as exc:
            unmappable.append(f"{offset_id}: {exc}")
    if unmappable:
        sys.exit("ERRO: traducao(oes) com caractere fora do ASCII do font (revise no approved):\n  "
                 + "\n  ".join(unmappable[:10]) + (f"\n  ... (+{len(unmappable) - 10})" if len(unmappable) > 10 else ""))

    # Agrupa por arquivo: {fname: {ptr_idx: text_decoded}}
    per_file: dict[tuple[str, int], dict[int, str]] = defaultdict(dict)   # (arquivo, secao) -> {ptr_idx: texto}
    orphans = sorted(k for k in translations if k not in string_meta)
    if orphans:      # approved desatualizado (extract re-rodou / key errada): sem isto so sobra "reinseridas" menor
        print(f"[reinsert] AVISO: {len(orphans)} traducao(oes) aprovada(s) sem linha em dialogs.csv -- "
              f"NAO reinseridas: {orphans[:5]}{' ...' if len(orphans) > 5 else ''}")
    for offset_id, text_target in translations.items():
        meta = string_meta.get(offset_id)
        if meta is None:
            continue
        per_file[meta['file'], meta['entry_idx']][meta['ptr_idx']] = text_target

    # Fallback: para strings sem tradução, usa o original (garante round-trip)
    for _offset_id, meta in string_meta.items():
        per_file[meta['file'], meta['entry_idx']].setdefault(meta['ptr_idx'], meta['text_en'])

    # Processa cada arquivo com traduções
    out_dir = _paths.output_dir(root)   # nunca escreve na instalação do jogo
    out_dir.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    overflow_count = 0
    files_modified = 0

    for fname in sorted({f for f, _ in per_file}):
        dat_path = game_dat_dir / fname
        if not dat_path.exists():
            report.append(f"- {fname}: ARQUIVO NÃO ENCONTRADO no diretório")
            continue

        original_data = dat_path.read_bytes()
        entries = parse_toc(original_data)
        if len(entries) < 2:
            continue

        new_data = original_data
        for entry_idx, sec_off, sec_sz in text_sections(fname, original_data, entries):
            file_translations = per_file.get((fname, entry_idx), {})
            section = original_data[sec_off:sec_off + sec_sz]

            # Verifica overflow individual (strings que excedem byte_budget próprio)
            for meta in string_meta.values():
                if (meta['file'], meta['entry_idx']) != (fname, entry_idx):
                    continue
                ptr_idx = meta['ptr_idx']
                encoded = encode_string(file_translations.get(ptr_idx, meta['text_en']))
                budget = meta['byte_budget']
                if len(encoded) + 1 > budget:
                    report.append(
                        f"- {fname}:{ptr_idx} individual_overflow {len(encoded)+1}>{budget}b"
                    )
                    overflow_count += 1

            # Reconstrói a seção e aplica patch (o indice da secao nao muda; os offsets seguintes sim)
            try:
                new_section = rebuild_section(section, file_translations)
            except OverflowError as exc:
                print(f"OverflowError em {fname}: {exc}")
                sys.exit(3)
            new_data = patch_dat_file(new_data, entry_idx, new_section)

            delta = len(new_section) - sec_sz
            tier = 'unchanged' if delta == 0 else ('shrunk' if delta < 0 else 'expanded')
            report.append(f"- {fname} [{tier}] seção {entry_idx}: {sec_sz}->{len(new_section)} (delta={delta:+d}b)")
        if new_data is original_data:
            continue
        if fname == 'INIT.DAT':
            # Fonte de dialogo com os acentos sobrepostos (font.py): sem ela os codigos 0xA0+ desenham lixo
            new_data = font.extend_atlas(new_data)
            report.append("- INIT.DAT [fonte] atlas de 24 px estendido com acentos (0xA0-0xAB)")

        (out_dir / fname).write_bytes(labels.patch(cards.patch(fname, new_data), patch_dat_file))
        files_modified += 1

    if ('INIT.DAT', 5) not in per_file:
        sys.exit("ERRO: INIT.DAT fora do dialogs.csv -- re-extraia (a fonte com acento vai nele)")

    # Grava relatório
    report_text ="\n".join(report)
    (root / 'artifacts' / 'reinsertion_report.md').write_text(
        f"# Reinsertion Report — Breath of Fire IV\n\n"
        f"Arquivos modificados: {files_modified}\n"
        f"Strings em overflow individual: {overflow_count}\n\n"
        f"{report_text}\n",
        encoding='utf-8',
    )
    if overflow_count:
        print(f"ATENÇÃO: {overflow_count} strings em overflow individual -> reescrita LLM em lote")
    print(f"Output gravado em {out_dir} ({files_modified} arquivos)")


if __name__ == '__main__':
    # argv[1] = raiz do projeto (nao project.json) -- mesma convencao de souldiers/trails_sky_sc
    # e do que connector_smoke.py ja passa; sem isso, o smoke --roundtrip falha sempre p/ este conector.
    proj_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj_root / 'project.json', override)
