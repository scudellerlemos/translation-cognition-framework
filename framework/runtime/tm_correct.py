#!/usr/bin/env python3
"""
tm_correct.py — CORRECAO GOVERNADA cross-capitulo de termos ja traduzidos (risco #3).

A TM e os artefatos de traducao eram efetivamente APPEND-ONLY: uma vez gravada uma cena, nao havia
ferramenta p/ corrigir um termo que se propagou. Ex.: um nome/glossario decidido errado no cap.11 e
repetido por 8 capitulos — corrigir a mao em N arquivos e erro-propenso e nao deixa rastro. Sem isso,
a CONSISTENCIA (a espinha dorsal da TM) so degrada.

Esta ferramenta aplica um lote de correcoes find->replace nos artefatos de traducao, de forma SEGURA:

  - As correcoes vem de um arquivo de DADOS (CSV), NAO do codigo. Governanca do projeto:
    IA PROPOE (gera/edita o CSV) -> humano/gate APROVA -> este script APLICA. Sem work-text no .py.
  - Match por LIMITE DE PALAVRA por padrao (nao corrompe substring: 'Ukon' nao casa dentro de outra
    palavra). `mode=literal` no CSV desliga a borda p/ casos com pontuacao/espaco.
  - Corrige OS DOIS artefatos coerentes: `translations_<id>.json` (campo `t`, o que o reinsert usa) E
    `translation_plan_<id>.json` (campo `base_translation`, fonte da TM). Corrigir so um reintroduziria
    o drift no proximo rebuild da TM.
  - DRY-RUN por padrao: lista cada (cena, offset, antes->depois) sem gravar. `--apply` grava.

CSV de correcoes (cabecalho obrigatorio): colunas `find,replace,note[,mode]`.
  find    = texto pt-BR a substituir (ex.: nome/termo errado)   replace = texto correto
  note    = motivo (rastro humano)                              mode    = word (default) | literal

DEPOIS de --apply (loop governado, NAO automatizado aqui de proposito):
  1) `python state_index.py <projeto> --rebuild`  -> a TM passa a refletir as correcoes.
  2) `python verify_chapter ...` (conector)        -> revalida CHARSET (uma correcao pode introduzir um
     caractere fora da fonte) e o round-trip. Este script NAO valida charset — quem valida e o gate.

Uso:  python tm_correct.py <projeto> <correcoes.csv> [--chapter 19] [--apply] [--json]
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
import artifact_io   # noqa: E402  (leitura compartilhada: scenes/scene_chapter)
import context_pack  # noqa: E402
import paths          # noqa: E402


def load_corrections(csv_path) -> list[dict]:
    """Le o CSV de correcoes -> [{find, replace, note, mode}]. Ignora linhas sem find/replace."""
    out = []
    p = Path(csv_path)
    if not p.is_file():
        raise FileNotFoundError(f"arquivo de correcoes nao encontrado: {csv_path}")
    with p.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            find = (r.get("find") or "").strip()
            if not find:                              # sem termo a buscar -> linha ignorada
                continue
            out.append({"find": find, "replace": r.get("replace", ""),
                        "note": (r.get("note") or "").strip(),
                        "mode": (r.get("mode") or "word").strip().lower()})
    return out


def _compile(find: str, mode: str):
    """Compila o padrao de busca. mode='word' usa limite de palavra (nao casa substring); 'literal' nao."""
    esc = re.escape(find)
    if mode == "literal":
        return re.compile(esc)
    # limite por lookaround em \w: funciona p/ termo unico e frase ('a gente'); preserva acento (\w unicode)
    return re.compile(r"(?<!\w)" + esc + r"(?!\w)")


def _apply_text(text: str, rules) -> tuple[str, int]:
    """Aplica todas as regras (compiladas) a um texto. Retorna (novo_texto, n_substituicoes)."""
    total = 0
    for rx, repl in rules:
        text, n = rx.subn(repl, text)
        total += n
    return text, total


def plan(root, corrections, chapter=None) -> list[dict]:
    """Calcula (sem gravar) todas as substituicoes. Retorna lista de hits:
    {scene, scene_id, artifact, offset, field, before, after, find, replace, note}."""
    root = Path(root)
    # pre-compila por regra (uma vez)
    compiled = [(c, _compile(c["find"], c["mode"]), c["replace"]) for c in corrections]
    hits = []
    for scene in artifact_io.scenes(root, chapter):
        sid = context_pack.scene_id_of(scene)
        # translations_<id>.json: lines = {offset: {... "t": ...}}
        tf = paths.translations(root, scene, sid)
        _collect(hits, tf, scene, sid, "translations", "t", _iter_translations, compiled)
        # translation_plan_<id>.json: lines = [{offset, base_translation, ...}]
        pf = paths.translation_plan(root, scene, sid)
        _collect(hits, pf, scene, sid, "plan", "base_translation", _iter_plan, compiled)
    return hits


def _iter_translations(data):
    """Itera (offset, valor_dict) do translations_<id>.json."""
    for off, v in (data.get("lines", {}) or {}).items():
        if isinstance(v, dict):
            yield off, v


def _iter_plan(data):
    """Itera (offset, valor_dict) do translation_plan_<id>.json (lines = lista)."""
    for v in (data.get("lines", []) or []):
        if isinstance(v, dict):
            yield v.get("offset", ""), v


def _collect(hits, path, scene, sid, artifact, field, iterator, compiled):
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    for off, v in iterator(data):
        before = v.get(field, "")
        if not before:
            continue
        after = before
        applied = None
        for c, rx, repl in compiled:
            new, n = rx.subn(repl, after)
            if n:
                after = new
                applied = c
        if after != before and applied is not None:
            hits.append({"scene": scene, "scene_id": sid, "artifact": artifact, "offset": off,
                         "field": field, "before": before, "after": after,
                         "find": applied["find"], "replace": applied["replace"], "note": applied["note"]})


def apply(root, corrections, chapter=None) -> dict:
    """Aplica as correcoes em disco. Retorna {files: N, replacements: M, hits: [...]}.
    Reescreve cada arquivo afetado UMA vez (idempotente: re-rodar sem novas regras nao muda nada)."""
    root = Path(root)
    compiled = [(c, _compile(c["find"], c["mode"]), c["replace"]) for c in corrections]
    hits = plan(root, corrections, chapter)            # p/ relatorio (mesmo calculo)
    files_changed, repl_count = 0, 0
    for scene in artifact_io.scenes(root, chapter):
        sid = context_pack.scene_id_of(scene)
        for path, field, iterator in (
                (paths.translations(root, scene, sid), "t", _iter_translations),
                (paths.translation_plan(root, scene, sid), "base_translation", _iter_plan)):
            if not path.is_file():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            changed = False
            for off, v in iterator(data):
                before = v.get(field, "")
                if not before:
                    continue
                rules = [(rx, repl) for _, rx, repl in compiled]
                after, n = _apply_text(before, rules)
                if n:
                    v[field] = after
                    repl_count += n
                    changed = True
            if changed:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                files_changed += 1
    return {"files": files_changed, "replacements": repl_count, "hits": hits}


def main():
    ap = argparse.ArgumentParser(description="Correcao governada cross-capitulo (dados propoem; script aplica).")
    ap.add_argument("project")
    ap.add_argument("corrections", help="CSV de correcoes: find,replace,note[,mode]")
    ap.add_argument("--chapter", default=None, help="restringe a um capitulo (ex.: 19); default: todos")
    ap.add_argument("--apply", action="store_true", help="grava em disco (default: dry-run)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    corr = load_corrections(a.corrections)
    if not corr:
        print("Nenhuma correcao valida no CSV (precisa de colunas find,replace).")
        sys.exit(2)
    if not a.apply:
        hits = plan(a.project, corr, a.chapter)
        if a.json:
            print(json.dumps(hits, ensure_ascii=False, indent=2))
        elif not hits:
            print(f"DRY-RUN: nenhuma ocorrencia das {len(corr)} regra(s) nos artefatos.")
        else:
            print(f"DRY-RUN: {len(hits)} substituicao(oes) em {len({(h['scene'], h['artifact']) for h in hits})} "
                  f"arquivo(s). Nada gravado. Rode com --apply p/ aplicar.")
            for h in hits:
                print(f"  {h['scene']}/{h['artifact']} {h['offset']} '{h['find']}' -> '{h['replace']}'"
                      + (f"  ({h['note']})" if h["note"] else ""))
                print(f"      antes: {h['before'][:90]}")
                print(f"      depois: {h['after'][:90]}")
        sys.exit(0)
    r = apply(a.project, corr, a.chapter)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"APLICADO: {r['replacements']} substituicao(oes) em {r['files']} arquivo(s).")
        print("Proximos passos (loop governado):")
        print(f"  1) python {Path(__file__).with_name('state_index.py').name} {a.project} --rebuild   # TM reflete a correcao")
        print("  2) verify_chapter do conector  # revalida CHARSET (correcao pode introduzir char fora da fonte) + round-trip")
    sys.exit(0)


if __name__ == "__main__":
    main()
