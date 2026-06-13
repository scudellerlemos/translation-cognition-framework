#!/usr/bin/env python3
"""
spoiler_check.py — VERIFICACAO POS-TRADUCAO de nao-vazamento de spoiler (H6, contraparte observavel).

O `context_pack` injeta guards de spoiler ANTES de traduzir (preventivo: filtro temporal +
`pre_reveal`). Faltava o lado OBSERVAVEL: depois de traduzir, checar se algum spoiler VAZOU de fato.
Sem isso, um vazamento (ex.: o nome 'Oshtor' numa cena ANTES do reveal em 13_08, onde a fonte usa
'Ukon') so seria pego por QA humano de olho — risco DURANTE a producao (H6 = o unico hardening com
risco enquanto se traduz).

Sinal de ALTA confianca (deterministico): cada entry do `spoiler_ledger.json` pode declarar
`forbidden_pre_reveal` — strings (nome/titulo canonico pos-reveal) que NAO podem aparecer na traducao
de uma cena ANTERIOR ao `reveal`. O checker varre os `translations_<scene_id>.json` das cenas
pre-reveal e flagra qualquer ocorrencia (casada por LIMITE DE PALAVRA, reusa context_pack._present).

NB de escopo honesto: o vazamento de GENERO pt-BR (ele/ela onde a fonte e neutra) e o outro risco que
a memoria do projeto enfatiza — mas detecta-lo com precisao exige marcar no ledger QUAIS entidades tem
genero em quarentena (campo futuro) + atribuir o token de genero ao referente certo na linha (NLP). Aqui
entregamos o sinal CATCHAVEL e deterministico (nome/titulo); o de genero fica como extensao (ver ROADMAP
H6). Governanca: read-only, sem rede, sem work-text.

Uso:  python spoiler_check.py <projeto> [--json]   (exit 1 se houver vazamento; 0 se limpo)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths          # noqa: E402


def _future(reveal: str, scene_id: str) -> bool:
    """A cena `scene_id` esta ANTES do reveal? (reveal 'beyond_frontier' = sempre futuro)."""
    if reveal == "beyond_frontier":
        return True
    return context_pack._pos(reveal) > context_pack._pos(scene_id)


def check(root) -> list[dict]:
    """Retorna a lista de VAZAMENTOS: cada {scene, scene_id, entity, forbidden, offset, text}. Vazio = ok.
    So considera cenas com translations_<id>.json em disco (cenas ja traduzidas)."""
    root = Path(root)
    led = paths.spoiler_ledger(root)
    if not led.is_file():
        return []
    entries = json.loads(led.read_text(encoding="utf-8")).get("entries", [])
    guarded = [(e, e.get("forbidden_pre_reveal") or []) for e in entries]
    guarded = [(e, fb) for e, fb in guarded if fb]
    if not guarded:
        return []
    leaks = []
    for sc_dir in sorted(paths.artifacts(root).glob("ch_*")):
        if not sc_dir.is_dir():
            continue
        scene = sc_dir.name
        sid = context_pack.scene_id_of(scene)
        tf = paths.translations(root, scene, sid)
        if not tf.is_file():
            continue
        try:
            lines = json.loads(tf.read_text(encoding="utf-8")).get("lines", {})
        except Exception:
            continue
        for entry, forbidden in guarded:
            if not _future(entry.get("reveal", "beyond_frontier"), sid):
                continue                                  # cena no/apos o reveal -> nome ja e seguro
            for off, v in lines.items():
                t = (v or {}).get("t", "") if isinstance(v, dict) else ""
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


def check_gender(root) -> list[dict]:
    """Contraparte OBSERVAVEL do vazamento de GENERO (o que o pt-BR forca e o ingles nao tem).
    Para entries do ledger com `gender_quarantine: true`, em cenas ANTES do reveal, flagra linhas que
    citam a entidade E contem um marcador de genero pt-BR. Retorna [{scene, scene_id, entity, marker,
    offset, text}]. ESCOPO HONESTO: heuristica de CO-OCORRENCIA por linha (referente unico) — nao e
    coreferencia; pode ter falso-positivo (por isso reporta o trecho p/ o humano decidir)."""
    root = Path(root)
    led = paths.spoiler_ledger(root)
    if not led.is_file():
        return []
    entries = json.loads(led.read_text(encoding="utf-8")).get("entries", [])
    guarded = [e for e in entries if e.get("gender_quarantine")]
    if not guarded:
        return []
    flags = []
    for sc_dir in sorted(paths.artifacts(root).glob("ch_*")):
        if not sc_dir.is_dir():
            continue
        scene = sc_dir.name
        sid = context_pack.scene_id_of(scene)
        tf = paths.translations(root, scene, sid)
        if not tf.is_file():
            continue
        try:
            lines = json.loads(tf.read_text(encoding="utf-8")).get("lines", {})
        except Exception:
            continue
        for entry in guarded:
            if not _future(entry.get("reveal", "beyond_frontier"), sid):
                continue                                  # no/apos o reveal -> genero ja e publico
            names = (entry.get("triggers") or []) + [entry.get("entity", "")]
            names = [n for n in names if n]
            for off, v in lines.items():
                t = (v or {}).get("t", "") if isinstance(v, dict) else ""
                if not t:
                    continue
                low = t.lower()
                if not any(context_pack._present(n.lower(), low) for n in names):
                    continue                              # entidade nao citada nesta linha
                for mk in _GENDER_MARKERS:
                    if context_pack._present(mk, low):
                        flags.append({"scene": scene, "scene_id": sid,
                                      "entity": entry.get("entity", ""), "marker": mk,
                                      "offset": off, "text": t})
                        break                             # 1 flag por linha basta
    return flags


def main():
    ap = argparse.ArgumentParser(description="Verificacao de nao-vazamento de spoiler (pos-traducao).")
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
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
            print(f"  {k['scene']} {k['offset']}: '{k['marker']}' junto a {k['entity']} (genero em quarentena)")
            print(f"      -> {k['text'][:90]}")
    sys.exit(1 if (leaks or gender) else 0)


if __name__ == "__main__":
    main()
