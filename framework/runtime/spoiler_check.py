#!/usr/bin/env python3
"""
spoiler_check.py — VERIFICACAO POS-TRADUCAO de nao-vazamento de spoiler (contraparte observavel).

O `context_pack` injeta guards de spoiler ANTES de traduzir (preventivo: filtro temporal +
`pre_reveal`). Faltava o lado OBSERVAVEL: depois de traduzir, checar se algum spoiler VAZOU de fato.
Sem isso, um vazamento (ex.: o nome 'Oshtor' numa cena ANTES do reveal em 13_08, onde a fonte usa
'Ukon') so seria pego por QA humano de olho — risco DURANTE a producao (o vazamento de spoiler e o
unico risco que persiste enquanto se traduz, nao so antes/depois).

Sinal de ALTA confianca (deterministico): cada entry do `spoiler_ledger.json` pode declarar
`forbidden_pre_reveal` — strings (nome/titulo canonico pos-reveal) que NAO podem aparecer na traducao
de uma cena ANTERIOR ao `reveal`. O checker varre os `translations_<scene_id>.json` das cenas
pre-reveal e flagra qualquer ocorrencia (casada por LIMITE DE PALAVRA, reusa context_pack._present).

NB de escopo honesto: o vazamento de GENERO pt-BR (ele/ela onde a fonte e neutra) e o outro risco que
a memoria do projeto enfatiza. `check_gender` marca no ledger QUAIS entidades tem genero em quarentena
(`gender_quarantine: true`) e continua flagrando por CO-OCORRENCIA na linha (RECALL preservado — perder
um vazamento real e pior que um falso-positivo extra), mas agora ATRIBUI o token de genero ao referente
mais provavel: cada flag carrega `confident` (True se a mencao da entidade em quarentena e a mais proxima,
em distancia de caracteres, do marcador entre as entidades do ledger citadas na linha; False se outra
entidade do ledger esta mais perto — ainda flagrado, so com prioridade de revisao menor). Nao e
coreferencia real (sem parser sintatico). Ver #106.
Governanca: read-only, sem rede, sem work-text.

Uso:  python spoiler_check.py <projeto> [--json]   (exit 1 se houver vazamento; 0 se limpo)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Uso completo:
#   python spoiler_check.py <projeto>                   # verifica vazamentos (exit 1 se houver)
#   python spoiler_check.py <projeto> --list-guards     # lista guards ativos no ledger
#   python spoiler_check.py <projeto> --json            # saida JSON (compativel com CI)

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402


def _future(reveal: str, scene_id: str) -> bool:
    """A cena `scene_id` esta ANTES do reveal? (reveal 'beyond_frontier' = sempre futuro)."""
    if reveal == "beyond_frontier":
        return True
    return context_pack._pos(reveal) > context_pack._pos(scene_id)


def check(root) -> list[dict]:
    """Retorna a lista de VAZAMENTOS: cada {scene, scene_id, entity, forbidden, offset, text}. Vazio = ok.
    So considera cenas com translations_<id>.json em disco (cenas ja traduzidas)."""
    root = Path(root)
    entries = context_pack.load_spoiler_ledger(root).get("entries", [])
    guarded = [(e, e.get("forbidden_pre_reveal") or []) for e in entries]
    guarded = [(e, fb) for e, fb in guarded if fb]
    if not guarded:
        return []
    leaks = []
    for scene, sid, lines in context_pack.load_translated_scenes(root):
        if not lines:
            continue
        for entry, forbidden in guarded:
            if not _future(entry.get("reveal", "beyond_frontier"), sid):
                continue                                  # cena no/apos o reveal -> nome ja e seguro
            for off, v in lines.items():
                t = v.get("target", "")
                if not t:
                    continue
                low = t.lower()
                for fb in forbidden:
                    if context_pack._present(fb.lower(), low):
                        leaks.append({"scene": scene, "scene_id": sid,
                                      "entity": entry.get("entity", ""), "forbidden": fb,
                                      "offset": off, "text": t})
    return leaks


# Marcadores de GENERO pt-BR de alta precisao (palavra inteira). Conservador de proposito: pronomes
# pessoais/possessivos/demonstrativos com genero + honorificos. Evita 'o/a/lo/la' (artigos/clise sao
# ruido demais). O ingles nao forca genero -> se a fonte e neutra e a entidade tem genero EM SEGREDO,
# qualquer um destes na MESMA linha que cita a entidade e um vazamento candidato.
_GENDER_MARKERS = ["ele", "ela", "dele", "dela", "nele", "nela", "aquele", "aquela", "senhor", "senhora"]


def _entity_names(entry: dict) -> list[str]:
    names = (entry.get("triggers") or []) + [entry.get("entity", "")]
    return [n for n in names if n]


def _mention_positions(name: str, low: str) -> list[int]:
    """Posicoes (indice do char inicial) de cada mencao de `name` em `low`, mesmo casamento de
    `context_pack._present` (limite de palavra + plural tolerado p/ termo alfanumerico)."""
    n = (name or "").strip().lower()
    if not n:
        return []
    pat = r"\b" + re.escape(n) + r"(?:e?s)?\b" if n.isalnum() else re.escape(n)
    return [m.start() for m in re.finditer(pat, low)]


def _nearest_referents(marker_pos: int, entities: list[tuple[str, list[str]]], low: str) -> list[str]:
    """Entre as entidades do ledger CITADAS em `low`, quais tem a mencao mais proxima (em chars) de
    `marker_pos`? Empate -> todas as entidades empatadas (conservador: se a em quarentena estiver no
    empate, ainda flagra p/ o humano decidir)."""
    best_dist = None
    best = []
    for entity_name, names in entities:
        dmin = min((abs(p - marker_pos) for n in names for p in _mention_positions(n, low)), default=None)
        if dmin is None:
            continue
        if best_dist is None or dmin < best_dist:
            best_dist, best = dmin, [entity_name]
        elif dmin == best_dist:
            best.append(entity_name)
    return best


def check_gender(root) -> list[dict]:
    """Contraparte OBSERVAVEL do vazamento de GENERO (o que o pt-BR forca e o ingles nao tem).
    Para entries do ledger com `gender_quarantine: true`, em cenas ANTES do reveal, flagra linhas que
    citam a entidade E contem um marcador de genero pt-BR — RECALL preservado de proposito (perder um
    vazamento real e pior que um falso-positivo extra pro humano descartar; distancia em caracteres
    nao e gramatica, entao um referente mais perto no texto pode nao ser o referente real da frase).
    Cada flag carrega tambem `confident`: True quando a mencao da entidade em quarentena e a mais
    proxima (por distancia de char, entre as entidades DO LEDGER citadas na linha) do marcador — ou
    seja, o token FOI atribuido ao referente mais provavel, nao so contabilizada a co-ocorrencia; False
    quando outra entidade do ledger esta mais perto do marcador (ainda flagrado, mas com prioridade
    menor de revisao humana — pode ser o marcador se referindo a essa outra entidade). Retorna
    [{scene, scene_id, entity, marker, offset, text, confident}]. ESCOPO HONESTO: nearest-mention por
    distancia de caracteres entre entidades DO LEDGER — nao e parsing sintatico/coreferencia real, e so
    enxerga entidades listadas no ledger (um referente fora dele nao entra no calculo de confianca)."""
    root = Path(root)
    entries = context_pack.load_spoiler_ledger(root).get("entries", [])
    guarded = [e for e in entries if e.get("gender_quarantine")]
    if not guarded:
        return []
    all_entities = [(e.get("entity", "?"), _entity_names(e)) for e in entries if _entity_names(e)]
    flags = []
    for scene, sid, lines in context_pack.load_translated_scenes(root):
        if not lines:
            continue
        for entry in guarded:
            if not _future(entry.get("reveal", "beyond_frontier"), sid):
                continue                                  # no/apos o reveal -> genero ja e publico
            ent_name = entry.get("entity", "?")           # mesmo default de all_entities (match consistente)
            names = _entity_names(entry)
            for off, v in lines.items():
                t = v.get("target", "")
                if not t:
                    continue
                low = t.lower()
                if not any(context_pack._present(n.lower(), low) for n in names):
                    continue                              # entidade nao citada nesta linha
                for mk in _GENDER_MARKERS:
                    positions = _mention_positions(mk, low)
                    if not positions:
                        continue
                    referents = _nearest_referents(positions[0], all_entities, low)
                    flags.append({"scene": scene, "scene_id": sid, "entity": ent_name,
                                  "marker": mk, "offset": off, "text": t,
                                  "confident": ent_name in referents})
                    break                                 # 1 flag por linha basta
    return flags


def audit_and_persist(root) -> dict:
    """check() + check_gender() sobre o PROJETO INTEIRO, persistidos em artifacts/spoiler_audit.json.
    Chamado OBRIGATORIAMENTE por run_chapter a cada capitulo -- antes so existia como CLI manual
    (`python spoiler_check.py <projeto>`), e foi exatamente por depender de alguem lembrar de rodar
    que um projeto (Souldiers) nunca chegou a ser auditado, mesma classe do gap ja documentado em
    onboarding-scaffold-kb-gate-drift (fase declarada pronta sem gate automatico verificando).
    Retorna {name_leaks, gender_flags, clean}; nunca levanta (projeto sem ledger -> tudo vazio,
    clean=True). Sobrescreve o artefato -- e o estado CORRENTE, nao historico incremental."""
    root = Path(root)
    leaks = check(root)
    gender = check_gender(root)
    rep = {"name_leaks": leaks, "gender_flags": gender, "clean": not (leaks or gender)}
    out = paths.spoiler_audit(root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def list_guards(root) -> list[dict]:
    """Guards ativos no ledger: entidade, reveal, strings proibidas pré-reveal, gender_quarantine."""
    root = Path(root)
    entries = context_pack.load_spoiler_ledger(root).get("entries", [])
    return [{"entity": e.get("entity", "?"),
             "reveal": e.get("reveal", "beyond_frontier"),
             "forbidden_pre_reveal": e.get("forbidden_pre_reveal") or [],
             "gender_quarantine": bool(e.get("gender_quarantine")),
             "notes": e.get("notes", "")}
            for e in entries]


def main():
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Verificacao de nao-vazamento de spoiler (pos-traducao).")
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-guards", action="store_true",
                    help="lista todos os guards ativos no ledger (inspecao, nao verifica vazamentos)")
    a = ap.parse_args()

    if a.list_guards:
        guards = list_guards(a.project)
        if not guards:
            print("Nenhum guard ativo (spoiler_ledger.json vazio ou ausente).")
            sys.exit(0)
        if a.json:
            print(json.dumps(guards, ensure_ascii=False, indent=2))
            sys.exit(0)
        print(f"{len(guards)} guard(s) ativo(s) no spoiler_ledger:")
        for g in guards:
            fb = ", ".join(g["forbidden_pre_reveal"]) if g["forbidden_pre_reveal"] else "(sem string proibida)"
            gq = "  [gender_quarantine]" if g["gender_quarantine"] else ""
            print(f"  {g['entity']:<22} reveal={g['reveal']:<15}  proibido={fb}{gq}")
            if g["notes"]:
                print(f"    nota: {g['notes']}")
        sys.exit(0)
    leaks = check(a.project)
    gender = check_gender(a.project)
    if a.json:
        print(json.dumps({"name_leaks": leaks, "gender_flags": gender}, ensure_ascii=False, indent=2))
        sys.exit(1 if (leaks or gender) else 0)
    if not leaks:
        print("OK: nenhum vazamento de spoiler (nome/titulo pos-reveal em cena anterior ao reveal).")
    else:
        print(f"VAZAMENTO DE SPOILER (nome/titulo) — {len(leaks)} linha(s):")
        for k in leaks:
            print(f"  {k['scene']} {k['offset']}: '{k['forbidden']}' ({k['entity']}) vazou ANTES do reveal")
            print(f"      -> {k['text'][:90]}")
    if not gender:
        print("OK: nenhum marcador de genero junto a entidade gender_quarantine pre-reveal.")
    else:
        print(f"GENERO A REVISAR (heuristica, pode ter falso-positivo) — {len(gender)} linha(s):")
        for k in gender:
            conf = "referente provavel" if k.get("confident") else "outra entidade mais perto, revisar"
            print(f"  {k['scene']} {k['offset']}: '{k['marker']}' junto a {k['entity']} "
                  f"(genero em quarentena, {conf})")
            print(f"      -> {k['text'][:90]}")
    sys.exit(1 if (leaks or gender) else 0)


if __name__ == "__main__":
    main()
