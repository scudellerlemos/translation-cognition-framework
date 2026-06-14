#!/usr/bin/env python3
"""
kb_review.py — DIGEST do delta de KB por capitulo (risco #4: a IA reconcilia a propria KB).

A Fase 0 (`kb_phase`) garante COBERTURA (todo nome recorrente esta na KB) e o marcador `reconciled` no
research_log — mas "reconciled" e so um marcador: a IA pesquisou a wiki sozinha e decidiu lore/genero/
timing de spoiler. Um erro decidido uma vez PROPAGA via TM por todos os capitulos seguintes. Faltava o
"segundo par de olhos": um relance auditavel do que foi ADICIONADO num capitulo, p/ um humano (ou uma 2a
passada de IA) ratificar ANTES de confiar.

Este modulo NAO e um gate (nao bloqueia, sempre exit 0) — de proposito, p/ nao virar o motor pesado de
reconciliacao que o H5 advertia ser overengineering. Ele so DESTILA: cruza as linhas novas de
glossary.csv/entities.csv (marcadas `(cap.N)` nas notas) com a secao `## cap.N` do research_log.md e
sinaliza o que merece olho humano:
  - `sem fonte declarada` : a entidade nao aparece na secao do research_log daquele capitulo;
  - `genero a confirmar`  : a nota admite genero incerto (risco direto de concordancia pt-BR errada);
  - `beyond_frontier`     : lore em quarentena de spoiler (conferir o guard no spoiler_ledger).

Governanca: read-only, sem rede, sem work-text. Uso:
  python kb_review.py <projeto> <capitulo> [--json]
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths          # noqa: E402


def _research_section(md: str, chap: str) -> str:
    """Texto da secao '## cap.<chap>' do research_log.md (ate o proximo '## '). '' se nao houver."""
    # casa '## cap.19' / '## cap.19 — ...' (limite em '.' p/ nao casar cap.1 com cap.19)
    pat = re.compile(r"^##\s+cap\.%s\b.*$" % re.escape(chap), re.MULTILINE)
    m = pat.search(md)
    if not m:
        return ""
    start = m.end()
    nxt = re.compile(r"^##\s", re.MULTILINE).search(md, start)
    return md[start:nxt.start()] if nxt else md[start:]


def _rows_for_chapter(path: Path, name_col: str, chap: str) -> list[dict]:
    """Linhas do CSV cujas notas marcam '(cap.<chap>)'. Retorna dicts crus (com name_col garantido)."""
    out = []
    if not path.is_file():
        return out
    marker = f"(cap.{chap})"
    with path.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if marker in (r.get("notes", "") or ""):
                out.append(r)
    return out


def _ratified_set(root) -> set:
    """Nomes ja ratificados pelo HUMANO (kb_ratified.csv, coluna 'name'). Vazio se nao houver arquivo.
    E o SEGUNDO PAR DE OLHOS: so o humano edita este arquivo (a IA nunca se auto-ratifica)."""
    p = paths.kb_ratified(root)
    if not p.is_file():
        return set()
    out = set()
    with p.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            n = (r.get("name") or "").strip().lower()
            if n:
                out.add(n)
    return out


# flags que BLOQUEIAM o gate. 'sem fonte declarada' bloqueia SEMPRE (ancora externa checavel = mata a
# invencao silenciosa); 'nao ratificado' e 'genero a confirmar' bloqueiam so em --strict (antes do build).
_BLOCK_ALWAYS = {"sem fonte declarada"}
_BLOCK_STRICT = {"nao ratificado", "genero a confirmar"}


def digest(root, chapter) -> list[dict]:
    """Delta de KB do capitulo: cada item {kind, name, category, confidence, target, in_research,
    flags[], note}. kind in {glossary, entity}. Vazio = nenhuma entidade nova marcada no capitulo."""
    root = Path(root)
    chap = str(chapter)
    section = _research_section(context_pack._read(paths.research_log(root)), chap).lower()
    ratified = _ratified_set(root)
    items = []

    def _flags(name, note):
        low = note.lower()
        fl = []
        if not (section and context_pack._present(name.lower(), section)):
            fl.append("sem fonte declarada")
        if "a confirmar" in low or "genero a confirmar" in low:
            fl.append("genero a confirmar")
        if "beyond_frontier" in low or "quarentena" in low:
            fl.append("beyond_frontier")
        if name.lower() not in ratified:
            fl.append("nao ratificado")
        return fl

    for r in _rows_for_chapter(paths.glossary(root), "term", chap):
        name, note = r.get("term", ""), r.get("notes", "") or ""
        items.append({"kind": "glossary", "name": name, "category": r.get("category", ""),
                      "confidence": "", "target": r.get("target_translation", ""),
                      "in_research": bool(section and context_pack._present(name.lower(), section)),
                      "flags": _flags(name, note), "note": note})
    for r in _rows_for_chapter(paths.entities(root), "canonical_name", chap):
        name, note = r.get("canonical_name", ""), r.get("notes", "") or ""
        items.append({"kind": "entity", "name": name, "category": r.get("category", ""),
                      "confidence": r.get("confidence", ""), "target": "",
                      "in_research": bool(section and context_pack._present(name.lower(), section)),
                      "flags": _flags(name, note), "note": note})
    return sorted(items, key=lambda x: (x["kind"], x["name"].lower()))


def blocking(root, chapter, *, strict=False) -> list[dict]:
    """Itens que BLOQUEIAM o gate de KB. 'sem fonte declarada' sempre; em strict, +'nao ratificado'/
    'genero a confirmar'. Cada item ganha 'blockers' (subset das flags que bloqueiam). Vazio = pode passar.
    E como o #5 (IA propoe E aprova) morre: fonte = ancora externa checavel; ratificacao = humano."""
    block_tags = _BLOCK_ALWAYS | (_BLOCK_STRICT if strict else set())
    out = []
    for it in digest(root, chapter):
        b = [f for f in it["flags"] if f in block_tags]
        if b:
            out.append({**it, "blockers": b})
    return out


def main():
    ap = argparse.ArgumentParser(description="Digest/gate do delta de KB por capitulo.")
    ap.add_argument("project")
    ap.add_argument("chapter", help="prefixo do capitulo, ex.: 19")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gate", action="store_true", help="exit 1 se houver item bloqueante (fonte/ratificacao)")
    ap.add_argument("--strict", action="store_true", help="com --gate: tambem bloqueia nao-ratificado/genero-a-confirmar")
    a = ap.parse_args()
    if a.gate:
        blk = blocking(a.project, a.chapter, strict=a.strict)
        if a.json:
            print(json.dumps(blk, ensure_ascii=False, indent=2))
        elif not blk:
            print(f"OK: delta de KB do cap.{a.chapter} passa o gate (fonte declarada"
                  + (" + ratificado + genero ok" if a.strict else "") + ").")
        else:
            print(f"BLOQUEADO — {len(blk)} entidade(s) do cap.{a.chapter} sem ancora:")
            for i in blk:
                print(f"  ({i['kind']}) {i['name']}: {', '.join(i['blockers'])}")
        sys.exit(1 if blk else 0)
    items = digest(a.project, a.chapter)
    if a.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        sys.exit(0)
    if not items:
        print(f"cap.{a.chapter}: nenhuma entidade/termo nova marcada '(cap.{a.chapter})' na KB.")
        sys.exit(0)
    flagged = [i for i in items if i["flags"]]
    print(f"DIGEST KB cap.{a.chapter} — {len(items)} entrada(s) nova(s), {len(flagged)} com flag p/ revisao:")
    for i in items:
        conf = f" conf={i['confidence']}" if i["confidence"] else ""
        tag = f"  [FLAGS: {', '.join(i['flags'])}]" if i["flags"] else ""
        print(f"  ({i['kind']}) {i['name']} <{i['category']}>{conf}{tag}")
        print(f"      {i['note'][:120]}")
    print("\n(digest informativo — ratifique as flags; nao bloqueia o pipeline.)")
    sys.exit(0)


if __name__ == "__main__":
    main()
