#!/usr/bin/env python3
"""
glossary_lint.py — CONSISTENCIA DE GLOSSARIO cross-capitulo (gate determinístico, $0, sem IA).

A TM da consistencia de REUSO (fala repetida reaparece igual), mas nada AUDITAVA se um termo do
glossario foi seguido em TODO o jogo. Este linter fecha essa lacuna: varre todas as cenas e, para cada
entrada do glossario, sinaliza linhas onde o EN usa o termo mas o pt-BR NAO usa a forma canonica:
  - handling_rule = manter_original  -> o pt-BR deve conter o termo VERBATIM (nome proprio preservado);
  - handling_rule = traduzir (com target) -> o pt-BR deve conter a traducao canonica.
Aliases (coluna do glossario) contam como forma valida.

Saida = CANDIDATOS p/ revisao humana (como o naturalness_lint): alta precisao, mas pode haver
falso-positivo legitimo (ex.: nome trocado por pronome — "Kuon disse" -> "ela disse"). Por isso o humano
confere; a correcao em massa de um termo errado e do `tm_correct` (find->replace governado).

Uso:  python glossary_lint.py <projeto> [--json]
Exit: 1 se houver candidatos (alimenta o loop "corrige -> re-roda ate zerar"); 0 se limpo.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io   # noqa: E402
import paths         # noqa: E402


def _fold(s: str) -> str:
    """minuscula + dobra acento (NFD) + colapsa espaco — p/ casar 'Mestre de Guerra' robustamente."""
    s = "".join(c for c in unicodedata.normalize("NFD", s or "") if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


# Palavras-comuns/papeis genericos: traduzidos POR CONTEXTO (man->homem/cara/rapaz/...), NAO sao termo
# fixo -> auditar consistencia deles e so ruido. So filtramos a regra `traduzir` (nome 'manter_original'
# e sempre auditado). Game-agnostico (papeis genericos de qualquer obra).
_GENERIC = frozenset("""
man woman girl boy child kid lad lass guy gal master mistress lord lady sir madam dame
guardian soldier soldiers warrior knight commander captain general officer guard guards
king queen prince princess emperor empress duke lord noble noble lady servant maid
innkeeper merchant trader smith priest priestess monk nun doctor nurse teacher student
friend brother sister mother father son daughter uncle aunt cousin husband wife
man's woman's people person folk crowd enemy enemies ally allies
""".split())


def _load_glossary(root: Path):
    """[(term, expected[list], rule)] — expected = formas validas no pt-BR (target + aliases).
    `traduzir` de palavra-comum generica (ver _GENERIC) e PULADO (traducao por contexto = ruido)."""
    g = paths.glossary(root)
    out = []
    if not g.is_file():
        return out
    for r in csv.DictReader(g.open(encoding="utf-8")):
        term = (r.get("term") or "").strip()
        if len(term) < 3:
            continue
        rule = (r.get("handling_rule") or "").strip()
        tgt = (r.get("target_translation") or "").strip()
        aliases = [a.strip() for a in re.split(r"[;|]", r.get("aliases") or "") if a.strip()]
        if rule == "manter_original":
            expected = [term] + aliases                      # nome proprio: deve aparecer verbatim, sempre
        elif tgt:
            if term.lower() in _GENERIC:
                continue                                      # palavra-comum -> traducao por contexto, nao audita
            expected = [tgt] + aliases                        # termo coined: a forma canonica
        else:
            continue                                          # sem alvo definido -> nao audita
        out.append((term, expected, rule))
    return out


def lint(root) -> list[dict]:
    root = Path(root)
    gloss = _load_glossary(root)
    if not gloss:
        return []
    # pre-compila regex de presenca do termo EN (limite de palavra, case-insensitive)
    compiled = [(term, [_fold(e) for e in expected], rule,
                 re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.I)) for term, expected, rule in gloss]
    found = []
    for scene in artifact_io.scenes(root, None):
        # fonte por offset
        src = {}
        d = paths.dialogs(root, scene)
        if d.is_file():
            for r in csv.DictReader(d.open(encoding="utf-8")):
                src[r.get("offset", "")] = r.get("text_source", "")
        tmap = artifact_io.translations_map(root, scene) or {}
        for off, v in tmap.items():
            s = src.get(off, "")
            if not s:
                continue
            t = v.get("t", "") if isinstance(v, dict) else ""
            tf = _fold(t)
            for term, exp_folded, rule, rx in compiled:
                if not rx.search(s):
                    continue                                  # termo nao esta na fonte desta linha
                if any(e and e in tf for e in exp_folded):
                    continue                                  # forma canonica (ou alias) presente -> ok
                found.append({"scene": scene, "offset": off, "term": term, "rule": rule,
                              "expected": exp_folded[0], "source": s, "target": t})
    return found


def main():
    ap = argparse.ArgumentParser(description="Consistencia de glossario cross-capitulo (candidatos p/ revisao).")
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    found = lint(a.project)
    out = paths.artifacts(Path(a.project)) / "glossary_lint.json"
    out.write_text(json.dumps({"count": len(found), "findings": found}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    if a.json:
        print(json.dumps({"count": len(found)}, ensure_ascii=False))
    else:
        from collections import Counter
        by_term = Counter(f["term"] for f in found)
        print(f"glossary_lint: {len(found)} candidato(s) de inconsistencia -> {out}")
        for term, n in by_term.most_common(25):
            print(f"  {term:24} {n}")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
