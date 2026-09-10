#!/usr/bin/env python3
"""
mine_scene_order.py — Breath of Fire IV (#183)

Tabela complementar ao extract.py: NÃO produz dialogs.csv (escopo de tradução
permanece só AREAD/AREAS, ver table_schema.md). Produz só metadado de ordem
narrativa por entidade, pra destravar `reveal:` em universe_knowledge_base.md.

Reusa os parsers binários de extract.py (TOC, seção de texto, strings) —
mesmo container em todas as famílias DAT (ver table_schema.md §1: "mesmo
formato se aplica a todos os tipos"). Amplia o escopo de família só aqui,
pra mineração de 1ª-menção, porque AREAE/AREAM contêm texto narrativo real
(falas com [14][XX]@, definições de local) apesar de fora do escopo Fase 0
de tradução — achado empírico #183, ver table_schema.md §1 nota.

Contrato:
    entrada : diretório DAT do jogo (CLI arg ou BOF4_DAT_DIR) + entities.csv
    saída   : artifacts/state/entity_first_scene.json
              (só scene_id + contagens — nunca texto de diálogo, seguro pra commit)

100% determinístico. NUNCA usar LLM aqui.
"""

import csv
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import extract as ex  # noqa: E402 — reusa parse_toc/find_text_section/extract_section_strings/decode_string

_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402

# Famílias com texto narrativo real (achado empírico #183, scan completo das
# 972 DAT do jogo): AREAD/AREAS = diálogo de história (escopo Fase 0);
# AREAE/AREAM = falas de NPC via trigger de área + definições de local,
# fora do escopo de tradução mas úteis pra ordem narrativa.
_NARRATIVE_FAMILIES = {'AREAD', 'AREAS', 'AREAE', 'AREAM'}
_FAMILY_PRI = {'AREAD': 0, 'AREAS': 1, 'AREAE': 2, 'AREAM': 3}
_CTRL_RE = re.compile(r'\[[0-9A-Fa-f]{2}\]')


def _narrative_key(p: Path) -> tuple:
    m = re.match(r'([A-Za-z]+?)(\d+)', p.stem)
    num = int(m.group(2)) if m else 9999
    fam = m.group(1).upper() if m else p.stem
    return (num, _FAMILY_PRI.get(fam, 99), p.name)


def _clean(text: str) -> str:
    return _CTRL_RE.sub(' ', text)


def mine(dat_dir: Path, entities_csv: Path) -> list[dict]:
    entities = list(csv.DictReader(open(entities_csv, encoding='utf-8')))

    files = [p for p in dat_dir.glob('*.DAT') if ex._file_family(p.name) in _NARRATIVE_FAMILIES]
    files.sort(key=_narrative_key)

    scene_seq: list[str] = []
    seen: set[str] = set()
    clean_rows: list[tuple[str, str]] = []

    for dat_path in files:
        sid = dat_path.stem
        data = dat_path.read_bytes()
        if len(data) < 64:
            continue
        entries = ex.parse_toc(data)
        if len(entries) < 2:
            continue
        result = ex.find_text_section(data, entries)
        if result is None:
            continue
        _entry_idx, sec_off, sec_sz = result
        section = data[sec_off:sec_off + sec_sz]
        strings = ex.extract_section_strings(section)
        file_has_text = False
        for _ptr_idx, _ptr, raw in strings:
            if not any(b in ex._ASCII_RANGE for b in raw):
                continue
            text = ex.decode_string(raw)
            clean_rows.append((sid, _clean(text)))
            file_has_text = True
        if file_has_text and sid not in seen:
            seen.add(sid)
            scene_seq.append(sid)

    scene_pos = {sid: i for i, sid in enumerate(scene_seq)}

    results = []
    for e in entities:
        name = e['canonical_name']
        names = [name]
        for a in (e.get('aliases') or '').split(';'):
            a = re.sub(r'\(.*?\)$', '', a).strip()
            if a:
                names.append(a)
        pats = [re.compile(r'\b' + re.escape(n) + r'\b', re.IGNORECASE) for n in names if len(n) > 2]

        first_scene = None
        first_idx = None
        count = 0
        for sid, text in clean_rows:
            if any(p.search(text) for p in pats):
                count += 1
                if first_scene is None and sid in scene_pos:
                    first_scene = sid
                    first_idx = scene_pos[sid]
        results.append({
            'canonical_name': name,
            'category': e['category'],
            'first_scene': first_scene,
            'scene_order_index': first_idx,
            'mentions_in_dialogue': count,
        })

    results.sort(key=lambda r: (r['scene_order_index'] is None, r['scene_order_index'] or 0))
    return results


def main(project_json: Path, source_override: str | None = None) -> None:
    root = project_json.parent
    game_dat_dir = connector_io.resolve_source_path(
        cli_arg=source_override, env_var="BOF4_DAT_DIR", allow_missing=True)
    if not game_dat_dir or not game_dat_dir.is_dir():
        raise SystemExit(
            "Diretório DAT não configurado.\n"
            "  1. Variável de ambiente: BOF4_DAT_DIR=<caminho>\n"
            "  2. CLI: python mine_scene_order.py project.json <DAT_DIR>\n")

    results = mine(game_dat_dir, root / 'artifacts' / 'entities.csv')
    out = root / 'artifacts' / 'state' / 'entity_first_scene.json'
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"entity_first_scene.json: {len(results)} entidades, "
          f"{sum(1 for r in results if r['first_scene'])} com 1ª cena encontrada -> {out}")


if __name__ == '__main__':
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('project.json')
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
