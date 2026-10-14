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

import json
import re
import struct
import sys
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)

if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import font  # noqa: E402  (acentos sobrepostos na fonte de dialogo)

# ---------------------------------------------------------------------------
# Constantes do formato
# ---------------------------------------------------------------------------
_ASCII_RANGE = range(0x20, 0x7F)
_CTRL_RE = re.compile(r'\[([0-9A-Fa-f]{2})\]')

# Pontuação tipográfica comum em diálogo pt-BR gerado por LLM que NFD não decompõe (não são
# acentos, são glifos distintos) -- sem isto, viravam '?' (0x3F) em silêncio, e
# verify_chapter.py comparava encode_string(x) contra encode_string(x) (mesma função em
# ambos os lados), entao o round-trip passava verde mesmo com a perda.
_PUNCT_FALLBACK = {
    '–': '-', '—': '-',              # en/em dash
    '‘': "'", '’': "'",              # aspas simples curvas
    '“': '"', '”': '"',              # aspas duplas curvas
    '…': '...',                      # reticências
}

# ---------------------------------------------------------------------------
# Escopo de extração — Fase 0: apenas diálogo de história
#
# Regra do framework (games.md): o Passo 00 extrai SOMENTE diálogo de
# personagem + falante. UI, itens, batalha = fase futura separada.
#
# Famílias incluídas:
#   AREAD = scripts de diálogo principal (field events)
#   AREAS = scripts de área (cutscenes, NPCs com fala)
#   AREAM = cidades e mapas (NPCs, lojas, minijogos)
#   AREAE = eventos (narração de abertura, cutscenes, tutoriais)
#
# Filtro de conteúdo: só sai string sem nenhuma letra visível ("--[81]", "5", "[14]A").
# Byte de parâmetro de control code não conta como letra: [14] leva 2 bytes; [04] [05] [09]
# [0C] [0F] [12] [16] levam 1 (ex.: "[0C][05][14]A" é só comando + speaker, sem texto).
# [05][03]...[06] NÃO é descrição de item: é a cor azul de destaque, usada em fala comum.
# Label curto ("Beer", "Food") aparece na tela da cena e precisa de tradução.
# ---------------------------------------------------------------------------
_DIALOGUE_FAMILIES = {'AREAD', 'AREAS', 'AREAM', 'AREAE'}
# Textos de sistema (menu, barraca, loja, salvar, tela inicial, fim de batalha, tabela de itens/habilidades):
# mesmo formato do dialogo, em secoes fixas. Achadas por varredura de todos os .DAT do jogo; a mesma secao
# se repete em varios arquivos (a tabela comum esta em 7) e cada copia precisa ser traduzida igual.
# Escopo: so entram com "extraction_scope": "completo" no project.json (caminho de sessao). O padrao,
# "dialogo", extrai so as familias de dialogo -- e o escopo do caminho de API.
_SYSTEM_SECTIONS = {
    'INIT.DAT': (5, 6), 'AB000_00.DAT': (2,), 'BTLEND.DAT': (5,), 'BTLRET.DAT': (2,), 'CAMP.DAT': (5, 6),
    'COMMU03.DAT': (5, 6), 'COMMU09B.DAT': (7,), 'D141BTL.DAT': (1, 13), 'D142BTL.DAT': (1, 13),
    'D143END.DAT': (8,), 'D152BTL.DAT': (1, 18), 'DEMO.DAT': (2,), 'E077BTL.DAT': (1, 15), 'MASTER.DAT': (5, 6),
    'MSHOP.DAT': (5, 6), 'SAVE.DAT': (6,), 'SGAMEN.DAT': (6, 7), 'SGAMENX.DAT': (2,), 'SHOP.DAT': (5, 6),
    'START.DAT': (5,),
}
# Secao-conteiner: cabecalho de offsets de 4 bytes e, em cada sub-bloco, uma tabela de texto no formato de sempre
# (INIT 7 = nomes de item/arma/armadura/acessorio/habilidade/item-chave; AB000_00 1 = ajuda e bestiario de batalha).
# ponytail: o sub-bloco k da secao e vira o "entry_idx" virtual _SUB_BASE + e*100 + k, para o id continuar
# arquivo:inteiro:inteiro em todo o pipeline. Trocar por id de 4 partes se um dia houver secao >= 100 ou 100 sub-blocos.
# INIT 7 fica FORA por decisao do usuario (2026-10-12): nome de item/habilidade nao e traduzido. Para voltar atras,
# acrescentar 'INIT.DAT': (7,) aqui e testar no jogo se a tabela pode crescer.
_NESTED_SECTIONS = {'AB000_00.DAT': (1,)}
_NAME_TABLES = {'INIT.DAT'}     # nome curto: o limite e o maior nome da tabela (largura da caixa), nao o do proprio nome
_SUB_BASE = 10000
_FAMILY_RE = re.compile(r'^([A-Z]+?)\d', re.IGNORECASE)
_LETTER_RE = re.compile(rb'[A-Za-z]')
_CTRL_PARAM_RE = re.compile(rb'\x14.{0,2}|[\x04\x05\x09\x0c\x0f\x12\x16].', re.DOTALL)

# Speaker: [14][XX] no início da string identifica o falante por código de cor
_SPEAKER_RE = re.compile(r'^\[14\]\[([0-9A-Fa-f]{2})\]')


def _file_family(fname: str) -> str:
    m = _FAMILY_RE.match(fname.upper())
    return m.group(1) if m else ''


def _extract_speaker(text: str) -> str:
    m = _SPEAKER_RE.match(text)
    return f'[14][{m.group(1).upper()}]' if m else ''


# ---------------------------------------------------------------------------
# 1. ENCODE / DECODE  (round-trip perfeito)
# ---------------------------------------------------------------------------
def decode_string(raw: bytes) -> str:
    """Bytes sem terminador → string CSV. ASCII → chr, outros → [XX]."""
    parts = []
    for b in raw:
        if b in _ASCII_RANGE and b != 0x5B:      # '[' literal vira [5B]: senao "[AB]" ASCII re-encodava como 0xAB
            parts.append(chr(b))
        else:
            parts.append(f'[{b:02X}]')
    return ''.join(parts)


def encode_string(text: str, strict: bool = False) -> bytes:
    """String CSV → bytes sem terminador. Inverso de decode_string.

    Acento pt-BR (á, ã, ç, ô...) vira acento sobreposto + letra-base (font.overlay: 'á' -> [A0]a,
    2 bytes). O que nao tem acento desenhado (ñ, ü...) e transliterado via NFD (connector_io.transliterate).
    Sem isso, todo acento virava '?' (0x3F) silenciosamente: verify_chapter.py compara
    decode(rebuild(encode(x))) contra encode_string(x), entao o round-trip comparava
    corrompido-com-corrompido e passava verde."""
    text = font.overlay(unicodedata.normalize('NFC', text))
    text = connector_io.transliterate(text)
    text = "".join(_PUNCT_FALLBACK.get(c, c) for c in text)
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
            elif strict:
                raise ValueError(f"caractere sem mapeamento ASCII: {ch!r} (U+{ord(ch):04X}) em {text!r}")
            else:
                # ainda nao mapeavel apos NFD+_PUNCT_FALLBACK (ex.: CJK) — ultimo recurso, mas
                # avisado (verify_chapter.py nao pega isso: compara encode_string(x) contra
                # encode_string(x), entao um '?' silencioso passaria verde nos dois lados).
                print(f"[extract] AVISO: caractere sem mapeamento ASCII substituido por '?': {ch!r} "
                      f"(U+{ord(ch):04X}) em {text!r}")
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
def text_sections(fname: str, data: bytes, entries: list) -> list[tuple[int, int, int]]:
    """Secoes de texto do arquivo: a de dialogo (find_text_section) ou as fixas de _SYSTEM_SECTIONS."""
    fixed = _SYSTEM_SECTIONS.get(fname.upper())
    if fixed is None:
        found = find_text_section(data, entries)
        return [found] if found else []
    out = [(i, entries[i][0], entries[i][1]) for i in fixed]
    for e in _NESTED_SECTIONS.get(fname.upper(), ()):
        off, sz = entries[e][0], entries[e][1]
        out += [(_SUB_BASE + e * 100 + k, off + a, b - a) for k, (a, b) in enumerate(sub_blocks(data[off:off + sz]))]
    return out


def split_virtual(entry_idx: int) -> tuple[int, int] | None:
    """entry_idx virtual -> (secao, sub-bloco); None se for secao comum."""
    return divmod(entry_idx - _SUB_BASE, 100) if entry_idx >= _SUB_BASE else None


def sub_blocks(section: bytes) -> list[tuple[int, int]]:
    """(inicio, fim) de cada sub-bloco de uma secao-conteiner, na ordem do cabecalho."""
    n = struct.unpack_from('<I', section, 0)[0] // 4
    offs = list(struct.unpack_from(f'<{n}I', section, 0))
    return list(zip(offs, offs[1:] + [len(section)], strict=True))


def find_text_section(data: bytes, entries: list) -> tuple[int, int, int] | None:
    """
    Heurística robusta: procura seção com tabela de ponteiros 2-byte + strings ASCII.

    Critérios (todos devem ser satisfeitos para pontuar):
    1. first_ptr (tamanho da tabela) está em [4, 0x1000] e cabe na seção
    2. Ao menos 70% dos ponteiros na tabela apontam para [first_ptr, sz)
    3. Ao menos 2 destinos distintos e metade deles logo depois de um 0x00 (fim da string anterior)
    4. Conteúdo após a tabela tem >= 40% de bytes ASCII
    5. Conteúdo pós-tabela cabe em uint16 (total bytes < 0xFFFF)

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
        # (sem teto relativo ao tamanho: cena de 2-3 falas tem tabela fixa de 512 bytes maior que o texto)
        if first_ptr < 4 or first_ptr >= sz or first_ptr > 0x1000:
            continue

        # Critério 2: maioria dos ponteiros deve apontar para dentro da seção
        ptr_count = first_ptr // 2
        valid_ptrs = 0
        unique_dests: set[int] = set()
        for p in range(0, first_ptr, 2):
            if p + 2 > len(section):
                break
            v = struct.unpack_from('<H', section, p)[0]
            if first_ptr <= v < sz:
                valid_ptrs += 1
                unique_dests.add(v)
        if ptr_count > 0 and (valid_ptrs / ptr_count) < 0.70:
            continue

        # Critério 3: destinos distintos que começam onde outra string termina.
        # Proporção de únicos não serve: cena curta tem tabela fixa de 256 ponteiros e ~10 falas
        # (o resto repete o último) -- o corte de 5% deixava 21 cenas fora do corpus.
        starts = sum(section[v - 1] == 0 for v in unique_dests if v > first_ptr)
        if len(unique_dests) < 2 or starts < 0.5 * (len(unique_dests) - 1):
            continue

        # Critério 4: conteúdo após a tabela deve ser majoritariamente ASCII
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
def string_spans(section: bytes) -> dict[int, tuple[int, bool]]:
    """ptr -> (fim do conteudo, tem terminador). A string vai do ponteiro ate o PROXIMO ponteiro
    distinto, nao ate o primeiro 0x00: control code com parametro 0x00 ([14][00][00], [0F][00],
    [19][00]...) tem texto depois dele. Cortar no primeiro 0x00 perdia esse resto na extracao e na
    reinsercao (~25% das strings). Sem 0x00 no fim = ponteiro para o meio de outra string (sharing)."""
    first_ptr = struct.unpack_from('<H', section, 0)[0]
    ptrs = sorted({v for (v,) in struct.iter_unpack('<H', section[:first_ptr & ~1])
                   if first_ptr <= v < len(section)})
    spans = {}
    for start, nxt in zip(ptrs, ptrs[1:] + [len(section)], strict=False):
        terminated = section[nxt - 1] == 0
        end = nxt - 1 if terminated else nxt
        if nxt == len(section):         # ultima string: zeros a mais sao padding de alinhamento da secao
            end = max(start, len(section[start:nxt].rstrip(b'\x00')) + start)
        spans[start] = (end, terminated)
    return spans


def extract_section_strings(section: bytes) -> list[tuple[int, int, bytes]]:
    """
    Retorna lista de (ptr_idx, ptr_offset_in_section, raw_bytes_sem_terminador).
    ptr_idx = índice na tabela de ponteiros.
    Aliases (dois índices com mesmo offset) são listados separadamente.
    0x00 no meio do raw e parametro de control code (vira [00] no CSV) -- ver string_spans.
    """
    if len(section) < 4:
        return []
    first_ptr = struct.unpack_from('<H', section, 0)[0]
    if first_ptr < 2 or first_ptr > len(section):
        return []

    spans = string_spans(section)
    results = []
    for i in range(0, first_ptr & ~1, 2):
        ptr = struct.unpack_from('<H', section, i)[0]
        if ptr in spans:
            results.append((i // 2, ptr, section[ptr:spans[ptr][0]]))
    return results


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
def main(project_json: Path, source_override: str | None = None) -> None:
    cfg = json.loads(project_json.read_text(encoding='utf-8'))
    root = project_json.parent
    max_pct = cfg.get('length_constraints', {}).get('dialogue_max_pct', 100) / 100
    system = _SYSTEM_SECTIONS if cfg.get('extraction_scope', 'dialogo') == 'completo' else {}

    # Resolve diretório DAT do jogo — CLI > BOF4_DAT_DIR env var > falha (nunca lê de project.json)
    _dir_error = (
        "Diretório DAT não configurado.\n"
        "Opções:\n"
        "  1. Variável de ambiente: BOF4_DAT_DIR=<caminho>\n"
        "  2. CLI: python extract.py <project_root> <DAT_DIR>\n"
        "Ver projects/bof4/.env.example"
    )
    game_dat_dir = connector_io.resolve_source_path(
        cli_arg=source_override, env_var="BOF4_DAT_DIR", allow_missing=True)
    # Path("") == Path(".") (CWD) -- .is_dir() sempre True, entao "nao configurado" (None) precisa
    # de check explicito ANTES do is_dir(), senao a checagem abaixo nunca dispara e o run prossegue
    # calado com a CWD como diretorio DAT (0 arquivos .DAT, dialogs.csv vazio, exit 0).
    if game_dat_dir is None or not game_dat_dir.is_dir():
        raise SystemExit(_dir_error)

    rows: list[dict] = []
    files_processed = 0
    files_with_text = 0
    skipped_family = 0
    skipped_no_letter = 0

    # Ordem narrativa: AREAD antes de AREAS dentro do mesmo número de área.
    _FAMILY_PRI = {'AREAD': 0, 'AREAS': 1, 'AREAM': 2, 'AREAE': 3}

    def _narrative_key(p: Path) -> tuple:
        import re as _re
        m = _re.match(r'([A-Za-z]+?)(\d+)', p.stem)
        num = int(m.group(2)) if m else 9999
        fam = m.group(1).upper() if m else p.stem
        return (num, _FAMILY_PRI.get(fam, 99), p.name)

    for dat_path in sorted(game_dat_dir.glob('*.DAT'), key=_narrative_key):
        fname = dat_path.name

        # Filtra por família: só famílias de diálogo de história
        if _file_family(fname) not in _DIALOGUE_FAMILIES and fname.upper() not in system:
            skipped_family += 1
            continue

        data = dat_path.read_bytes()
        if len(data) < 64:
            continue

        entries = parse_toc(data)
        if len(entries) < 2:
            continue

        sections = text_sections(fname, data, entries)
        if not sections:
            continue
        files_processed += 1

        file_has_text = False
        for entry_idx, sec_off, sec_sz in sections:
            strings = extract_section_strings(data[sec_off:sec_off + sec_sz])
            name_cap = max((len(r) for *_, r in strings), default=0) if (
                split_virtual(entry_idx) and fname.upper() in _NAME_TABLES) else 0
            for ptr_idx, _ptr, raw in strings:
                if not _LETTER_RE.search(_CTRL_PARAM_RE.sub(b'', raw)):
                    skipped_no_letter += 1
                    continue

                text = decode_string(raw)

                file_has_text = True
                string_id = f"{fname}:{entry_idx}:{ptr_idx}"
                rows.append({
                    'offset': string_id,
                    'file': fname,
                    'entry_idx': entry_idx,
                    'ptr_idx': ptr_idx,
                    'text_en': text,
                    # tabela aninhada nao cresce (decisao do usuario 2026-10-12): limite = tamanho original.
                    # ponytail: limite por texto; a folga real e por lista — somar por lista se abreviar ficar feio.
                    'byte_budget': (name_cap or (len(raw) if split_virtual(entry_idx)
                                                 else int(len(raw) * max_pct))) + 1,
                    'speaker_code': _extract_speaker(text),
                })

        if file_has_text:
            files_with_text += 1

    out_csv = root / cfg['source']['file']
    fieldnames = ['offset', 'file', 'entry_idx', 'ptr_idx', 'text_en', 'byte_budget', 'speaker_code']
    connector_io.write_dialogs_csv(out_csv, fieldnames, rows)

    connector_io.write_extraction_log(
        root / 'artifacts' / 'extraction_log.md',
        f"# Extraction Log — Breath of Fire IV\n\n"
        f"- Diretório DAT: `{Path(game_dat_dir).name}`\n"
        f"- Escopo: famílias de diálogo ({', '.join(sorted(_DIALOGUE_FAMILIES))}) + sistema ({', '.join(system) or 'fora do escopo'})\n"
        f"- Arquivos com diálogo: {files_with_text}\n"
        f"- Strings extraídas: {len(rows)}\n"
        f"- Excluídas por família fora do escopo: {skipped_family} arquivos\n"
        f"- Excluídas por não ter nenhuma letra: {skipped_no_letter} strings\n"
        f"- Container: Capcom DAT (TOC + seções)\n"
        f"- Encoding: ASCII com escapes hex `[XX]`\n"
        f"- Speaker: coluna speaker_code = [14][XX] do início da string\n",
    )
    print(f"Extraídas {len(rows)} strings de diálogo de {files_with_text} arquivos -> {out_csv}")


if __name__ == '__main__':
    # argv[1] = raiz do projeto (nao project.json) -- mesma convencao de souldiers/trails_sky_sc
    # e do que connector_smoke.py ja passa; sem isso, o smoke test falha sempre p/ este conector.
    proj_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj_root / 'project.json', override)
