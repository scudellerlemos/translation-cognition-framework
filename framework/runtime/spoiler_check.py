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


def main():
    ap = argparse.ArgumentParser(description="Verificacao de nao-vazamento de spoiler (pos-traducao).")
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    leaks = check(a.project)
    if a.json:
        print(json.dumps(leaks, ensure_ascii=False, indent=2))
    elif not leaks:
        print("OK: nenhum vazamento de spoiler (nome/titulo pos-reveal em cena anterior ao reveal).")
    else:
        print(f"VAZAMENTO DE SPOILER — {len(leaks)} linha(s):")
        for k in leaks:
            print(f"  {k['scene']} {k['offset']}: '{k['forbidden']}' ({k['entity']}) vazou ANTES do reveal")
            print(f"      -> {k['text'][:90]}")
    sys.exit(1 if leaks else 0)


if __name__ == "__main__":
    main()
