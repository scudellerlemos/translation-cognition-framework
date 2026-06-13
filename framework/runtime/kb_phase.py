#!/usr/bin/env python3
"""
kb_phase.py — DRIVER de Fase 0 (cabeia a pesquisa reconciliada como pre-requisito de escala).

A doutrina (skill 03) exige KB RECONCILIADA antes de traduzir um arco novo. O `kb_gate` ja BLOQUEIA
cenas alem da fronteira (`kb_frontier`); o que faltava era automatizar a parte DETERMINISTA da Fase 0 —
DESCOBRIR o que falta pesquisar e VALIDAR a cobertura — sem violar a governanca:

  IA PROPOE (worklist = cobranca)  ->  humano+IA RECONCILIAM (skill 03)  ->  script VALIDA + avanca a fronteira.

Este driver NAO pesquisa nem reconcilia sozinho (isso e o gate humano). Ele:
  - descobre os candidatos de lore/nome-proprio que aparecem nas cenas do capitulo e que a KB
    (glossary + entities) NAO cobre — usando a MESMA primitiva de match (`context_pack._present`) que o
    tradutor usa, entao o gap reportado e EXATAMENTE o que o context_pack falharia em surfar; e
  - valida a cobertura (gap fechado + research_log `reconciled`) e propoe/aplica o avanco de `kb_frontier`.

Heuristica honesta: candidatos = sequencias capitalizadas no source. Single-word so conta como nome
proprio "forte" se aparecer em MEIO de frase ao menos 1x (capitalizacao de inicio de frase = ruido,
reportada so como aviso). Multi-word capitalizado = sinal forte (sempre). Nao e exaustivo — e uma
COBRANCA de candidatos pro humano, nao um classificador.

Modos (CLI):
  python kb_phase.py <projeto> <cap>                  # discover: escreve artifacts/kb_phase_worklist_<cap>.md
  python kb_phase.py <projeto> <cap> --check          # valida cobertura: exit 0 se pronto p/ avancar
  python kb_phase.py <projeto> <cap> --check --apply-frontier   # se OK, avanca project.json kb_frontier
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
import paths          # noqa: E402  (H2: fonte unica de paths)
from context_pack import scene_id_of, _present, _pos  # noqa: E402

# sequencia de 1+ palavras capitalizadas (pega "Oshtor", "Eight Pillar Generals", "Oshtor's").
_CAP_RUN = re.compile(r"[A-Z][A-Za-z'’\-]+(?:\s+[A-Z][A-Za-z'’\-]+)*")

# STOPLIST de palavras COMUNS do ingles: um nome proprio, por definicao, NAO esta aqui. Filtra a
# capitalizacao de inicio de frase ("What", "She", "And"...) que vaza mesmo do teste de meio-de-frase
# (dialogo com virgula/travessao). Generosa de proposito — reduzir ruido > recall (a worklist e uma
# cobranca; falso-negativo raro de nome que COINCIDE com palavra comum e aceitavel). Game-agnostica.
_STOP = frozenset("""
a an the and or but nor so yet for of to in on at by from with without within into onto upon over under
above below between among through during before after since until while as than then thus hence therefore
however moreover meanwhile otherwise instead besides though although unless because if whether when where
why how what who whom whose which that this these those there here it its it's i i'm i'll i've i'd me my
mine myself we we're we'll we've us our ours ourselves you you're you'll you've your yours yourself yourselves
he he's him his himself she she's her hers herself they they're they'll they've them their theirs themselves
is am are was were be been being do does did doing done have has had having will would shall should can could
may might must ought need dare used get gets got gotten go goes going gone come comes coming came make makes
making made take takes taking took taken give gives giving gave given know knows knowing knew known think
thinks thinking thought see sees seeing saw seen say says saying said tell tells telling told want wants
wanting wanted look looks looking looked find finds finding found feel feels feeling felt seem seems seeming
let lets letting put puts putting keep keeps keeping kept turn turns turning let's
not no nor none nothing nobody nowhere never neither yes yeah yep nope ok okay sure fine well now soon
just only even still also too very much many more most less least few little lot lots some any all both
each every either other another such same own enough quite rather almost about around nearly really truly
indeed perhaps maybe please thanks thank sorry hello hi hey oh ah huh hmm wow ugh eh um uh aha alright
again once twice always often sometimes usually ever forever today tomorrow yesterday day days night
time times moment way ways thing things one two three four five six seven eight nine ten first second third
last next good bad big small new old long short high low right left up down out off away back forward
man woman men women people person child children boy girl friend friends home house world life death war
like hold help leave love hold papa mama behind starting searching accompanying succeeding asking allow
dear guess getting nice we'd ahaha agh wheh pweeaase
wait cheers ooh thou fate game perfect sisters mmmmm damn mayhap methinks barkeep
urgh unhand regardless understood pardon oohh failure preposterous highness guardian
it'll what're nah remember puffs expecting inform
dammit sounds hahahaha hip it'd boys
hand hands eye eyes face heart head room door water fire light dark good great
mister miss missus sir lord lady master mom dad mother father brother sister son daughter missy
don't won't can't cant didn't doesn't isn't aren't wasn't weren't haven't hasn't hadn't wouldn't couldn't
shouldn't mustn't ain't y'all let's that's there's here's what's who's how's gah heh hah hmph tch ugh argh
grr ow ouch yikes whoa woah oops phew aww hmm err umm hush shh psst ahem ha haha hehe nngh hngh tsk hoo
whatever whenever wherever however whoever whomever everyone everything everywhere everybody someone
something somewhere somebody anyone anything anywhere anybody
despite god gods mysterious gonna wanna gotta gimme lemme dunno kinda sorta cause cuz
lords ladies masters mistress mistresses prince princes princess princesses king kings queen queens
emperor empress general generals captain captains commander commanders chief chiefs boss colonel
sirs madam madams milord milady yessir yep yup nope
""".split())


def _scenes_of(root: Path, chap: str) -> list[str]:
    """Cenas do capitulo por glob de artifacts/ch_<cap>_*/dialogs.csv (ordem por scene_id)."""
    names = [p.parent.name for p in paths.artifacts(root).glob(f"ch_{chap}_*/dialogs.csv")]
    return sorted(set(names), key=scene_id_of)


def _kb_blob_from(glossary_terms, entity_names) -> str:
    """Blob lowercased a partir de listas (puro, testavel sem disco): glossary terms+aliases e
    entities canonical+aliases ja achatados em strings."""
    return "\n".join(list(glossary_terms) + list(entity_names)).lower()


def _kb_blob(root: Path) -> str:
    """Blob lowercased de TUDO que a KB conhece como nome/termo: glossary (term+aliases) + entities
    (canonical+aliases). E contra ISTO que perguntamos se um candidato esta coberto (via _present)."""
    g_parts, e_parts = [], []
    g = paths.glossary(root)
    if g.is_file():
        with g.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                g_parts.append(r.get("term", "") or "")
                g_parts.append(r.get("aliases", "") or "")
    e = paths.entities(root)
    if e.is_file():
        with e.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                e_parts.append(r.get("canonical_name", "") or "")
                e_parts.append(r.get("aliases", "") or "")
    return _kb_blob_from(g_parts, e_parts)


def _norm_tok(s: str) -> str:
    """Normaliza UM token: tira pontuacao das bordas e o possessivo final ('s)."""
    s = (s or "").strip().strip("-'’.,!?;:\"")
    low = s.lower()
    if low.endswith("'s") or low.endswith("’s"):
        s = s[:-2]
    return s.strip()


def _clean_cand(run: str) -> str:
    """Constroi o candidato LIMPO de um run capitalizado, removendo ruido que a capitalizacao funde:
      - ALL-CAPS (grito/enfase: 'CARRY', 'DAMN') — nome proprio e Title-case, nao caixa-alta;
      - gagueira ('M-Master' -> 'Master', 'Wh-What' -> 'What') — pega o segmento final completo;
      - stopwords nas BORDAS ('Despite Maroro' -> 'Maroro', 'The Mystery Twins' -> 'Mystery Twins').
    Stopword INTERIOR ('General of the Right') e mantida. Retorna '' se nada sobrar."""
    toks = []
    for raw in run.split():
        t = _norm_tok(raw)
        if not t:
            continue
        if t.isupper() and len(t) > 1:                 # ALL-CAPS = grito, nao nome
            continue
        if "-" in t:                                   # gagueira: usa o segmento final se capitalizado
            seg = t.split("-")[-1]
            if seg[:1].isupper():
                t = seg
        toks.append(t)
    while toks and toks[0].lower() in _STOP:           # apara stopword das bordas
        toks.pop(0)
    while toks and toks[-1].lower() in _STOP:
        toks.pop()
    return " ".join(toks)


def _excerpt(text: str, pos: int, span: int = 32) -> str:
    """Janela de ~span chars ao redor de pos, numa linha (token de quebra -> espaco), p/ a worklist."""
    a, b = max(0, pos - span), min(len(text), pos + span)
    frag = text[a:b].replace(context_pack.TOKEN, " ").replace("\n", " ")
    frag = re.sub(r"\s+", " ", frag).strip()
    return ("…" if a > 0 else "") + frag + ("…" if b < len(text) else "")


def _scan(root: Path, scenes: list[str]):
    """[(scene_id, source_text)] por cena (concatena as linhas-fonte do dialogs.csv)."""
    per = []
    for scene in scenes:
        f = paths.dialogs(root, scene)
        if not f.is_file():
            continue
        rows = context_pack.load_dialogs(f)
        per.append((scene_id_of(scene), "\n".join(r["source"] for r in rows)))
    return per


def _midsentence(word: str, corpus: str) -> bool:
    """True se `word` aparece ao menos 1x em MEIO de frase (precedido por minuscula/digito/virgula) —
    forte sinal de nome proprio (vs. capitalizacao so de inicio de frase)."""
    pat = re.compile(r"[a-z0-9,;:)\"'’]\s+" + re.escape(word) + r"\b")
    return pat.search(corpus) is not None


def _present_norm(tok: str, kb_low: str) -> bool:
    """_present com depluralizacao do CANDIDATO: a tolerancia de plural do _present e do lado da AGULHA
    (termo do glossario), entao candidato plural ('Cohorts') nao casava KB singular ('Cohort'). Aqui
    tentamos tambem a forma singular do candidato -> 'Cohorts' casa o termo 'Cohort'."""
    if _present(tok, kb_low):
        return True
    t = tok.lower()
    for suf in ("es", "s"):
        if t.endswith(suf) and len(t) - len(suf) >= 3 and _present(t[:-len(suf)], kb_low):
            return True
    return False


def _covered(cand: str, kb_low: str) -> bool:
    """Coberto pela KB se o candidato casa direto OU (multi-palavra) se o NUCLEO de nome proprio — os
    tokens fora da stoplist — esta todo na KB. Assim 'Master Haku'/'Lady Rulutieh'/'Ukon Cohorts' contam
    como cobertos via 'Haku'/'Rulutieh'/'Ukon'+'Cohort' (titulo/plural + nome ja conhecido)."""
    if _present_norm(cand, kb_low):
        return True
    toks = cand.lower().split()
    if len(toks) > 1:
        core = [t for t in toks if t not in _STOP]
        return bool(core) and all(_present_norm(t, kb_low) for t in core)
    return False


def _strong(rec: dict, corpus: str) -> bool:
    """Sinal de nome proprio forte o bastante p/ BLOQUEAR (vs. so reportar). Multi-palavra (com nucleo
    nao-comum) = forte. Single-word so e forte se RECORRENTE (>=2x) e em meio de frase, e nao for
    contracao/advervio-`ly`/gagueira (ruido que escapa da stoplist). One-off single-word -> 'fraco'
    (aviso): nome citado 1x e baixa confianca; o humano revisa, mas nao trava a fronteira."""
    low = rec["cand"].lower()
    if rec["multi"]:
        return True
    if low.endswith(("n't", "'t", "ly")) or "-" in low:
        return False
    return rec["count"] >= 2 and _midsentence(rec["cand"], corpus)


def discover(root, chap) -> dict:
    """Descobre candidatos de lore/nome no capitulo e os classifica vs. a KB. Retorna
    {chapter, scenes, gap:[fortes nao cobertos], weak:[fracos nao cobertos], covered:[ja na KB]}."""
    root = Path(root)
    scenes = _scenes_of(root, chap)
    kb_low = _kb_blob(root)
    per = _scan(root, scenes)
    corpus = "\n".join(t for _, t in per)
    agg = {}
    for scene_id, text in per:
        for m in _CAP_RUN.finditer(text):
            cand = _clean_cand(m.group(0))             # limpa ALL-CAPS/gagueira/stopword de borda
            low = cand.lower()
            # ruido se vazio, single-letter, ou TODOS os tokens comuns ("What", "Oh No").
            if not cand or len(low) <= 2 or all(tok in _STOP for tok in low.split()):
                continue
            rec = agg.get(low)
            if rec is None:
                rec = agg[low] = {"cand": cand, "count": 0, "scenes": set(),
                                  "first": scene_id, "multi": (" " in cand), "example": ""}
            rec["count"] += 1
            rec["scenes"].add(scene_id)
            if not rec["example"]:
                rec["example"] = _excerpt(text, m.start())
    gap, weak, covered = [], [], []
    for low, rec in agg.items():
        rec["scenes"] = sorted(rec["scenes"], key=_pos)
        if _covered(rec["cand"], kb_low):
            covered.append(rec)
            continue
        rec["strong"] = _strong(rec, corpus)
        (gap if rec["strong"] else weak).append(rec)
    gap.sort(key=lambda r: (-r["count"], r["cand"].lower()))
    weak.sort(key=lambda r: (-r["count"], r["cand"].lower()))
    covered.sort(key=lambda r: r["cand"].lower())
    # BLOQUEANTE = gap que RECORRE em >=2 cenas distintas OU >=3x: recorrencia cross-cena e quase sempre
    # nome proprio/lore real (ruido de frase raramente recorre fundido identico). One-off entra no gap
    # (worklist) mas so AVISA — nome citado 1x e baixa confianca; o humano revisa sem travar a fronteira.
    block = [r for r in gap if len(r["scenes"]) >= 2 or r["count"] >= 3]
    return {"chapter": chap, "scenes": [scene_id_of(s) for s in scenes],
            "gap": gap, "block": block, "weak": weak, "covered": covered}


def _reconciled(root: Path) -> bool:
    rl = paths.research_log(root)
    return rl.is_file() and bool(
        re.search(r"status[:*\s]+reconciled", rl.read_text(encoding="utf-8"), re.I))


def coverage(root, chap) -> dict:
    """Valida se o capitulo esta pronto p/ avancar a fronteira: gap fechado + research reconciliada.
    problems != [] => NAO avancar (rode/estenda a Fase 0). Limite honesto: 'gap fechado' = todos os
    nomes proprios fortes ja estao na KB; nao garante que a pesquisa foi PROFUNDA, so que esta presente."""
    root = Path(root)
    d = discover(root, chap)
    problems, warnings = [], []
    if d["block"]:
        sample = [f"{r['cand']} ({len(r['scenes'])} cenas)" for r in d["block"][:12]]
        problems.append(f"{len(d['block'])} candidato(s) RECORRENTE(s) de lore/nome NAO cobertos pela KB "
                        f"— pesquise+reconcilie (skill 03) e adicione a glossary/entities: {sample}")
    if not _reconciled(root):
        problems.append("research_log.md sem 'status: reconciled' — reconcilie a pesquisa IA+humano.")
    one_off = [r for r in d["gap"] if r not in d["block"]]
    if one_off:
        warnings.append(f"{len(one_off)} candidato(s) de baixa confianca (citados 1x) — nao bloqueiam; "
                        f"confira na worklist se algum e nome proprio real: "
                        f"{[r['cand'] for r in one_off[:10]]}")
    return {"problems": problems, "warnings": warnings, "discover": d}


def apply_frontier(root, chap):
    """Avanca project.json `kb_frontier` p/ o ultimo scene_id do capitulo (NUNCA regride). Edita so o valor
    (preserva o resto do arquivo). Retorna o novo valor, ou o atual se ja >=. So deve ser chamado apos
    coverage() passar (gate)."""
    root = Path(root)
    scenes = _scenes_of(root, chap)
    if not scenes:
        return None
    last = scene_id_of(scenes[-1])
    cfgp = root / "project.json"
    txt = cfgp.read_text(encoding="utf-8")
    m = re.search(r'("kb_frontier"\s*:\s*")([^"]*)(")', txt)
    if not m:
        return None                                    # sem campo -> nao inserir cegamente; reportar
    cur = m.group(2)
    if cur and _pos(cur) >= _pos(last):
        return cur                                     # nunca regride
    new = txt[:m.start()] + m.group(1) + last + m.group(3) + txt[m.end():]
    cfgp.write_text(new, encoding="utf-8")
    return last


def write_worklist(root, chap) -> Path:
    """Escreve artifacts/kb_phase_worklist_<cap>.md — a COBRANCA: o que a IA pede ao humano pesquisar."""
    root = Path(root)
    d = discover(root, chap)
    reconc = _reconciled(root)
    L = [f"# Fase 0 — capitulo {chap} — worklist de cobertura de KB", "",
         "> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem",
         "> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise",
         "> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa",
         "> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> {0} --check`.".format(chap),
         "",
         f"- cenas do capitulo: {', '.join(d['scenes']) or '(nenhuma)'}",
         f"- research_log reconciliado: {'sim' if reconc else 'NAO — bloqueia o avanco'}",
         f"- nao cobertos: **{len(d['block'])} bloqueante(s)** (recorrem >=2 cenas) + "
         f"{len(d['gap']) - len(d['block'])} de baixa confianca | fracos (ruido): {len(d['weak'])} | "
         f"ja cobertos: {len(d['covered'])}", ""]
    block_keys = {r["cand"] for r in d["block"]}
    L.append("## Candidatos NAO cobertos — PESQUISAR (cobranca)")
    L.append("> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser "
             "pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.")
    if d["gap"]:
        L.append("| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |")
        L.append("|---|---|---|---|---|---|")
        for r in d["gap"]:
            ex = r["example"].replace("|", "\\|")
            mark = "**SIM**" if r["cand"] in block_keys else "—"
            L.append(f"| {r['cand']} | {mark} | {r['count']} | {r['first']} | "
                     f"{', '.join(r['scenes'])} | {ex} |")
    else:
        L.append("_(nenhum — todos os nomes proprios fortes do capitulo ja estao na KB)_")
    L.append("")
    if d["weak"]:
        L.append("## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)")
        L.append("| candidato | ocorr. | exemplo |")
        L.append("|---|---|---|")
        for r in d["weak"][:40]:
            ex = r["example"].replace("|", "\\|")
            L.append(f"| {r['cand']} | {r['count']} | {ex} |")
        if len(d["weak"]) > 40:
            L.append(f"| … | … | (+{len(d['weak']) - 40} mais) |")
        L.append("")
    L.append("## Ja cobertos pela KB (conferencia)")
    L.append(", ".join(r["cand"] for r in d["covered"]) or "_(nenhum)_")
    L.append("")
    out = paths.kb_worklist(root, chap)
    out.write_text("\n".join(L), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description="Driver de Fase 0 (descobre gap de KB / valida cobertura).")
    ap.add_argument("project")
    ap.add_argument("chapter", help='prefixo do capitulo, ex.: "13"')
    ap.add_argument("--check", action="store_true",
                    help="valida cobertura (gap fechado + reconciled); exit 1 se faltar")
    ap.add_argument("--apply-frontier", action="store_true",
                    help="com --check OK, avanca project.json kb_frontier p/ o ultimo scene_id do capitulo")
    a = ap.parse_args()
    root = Path(a.project)

    if a.check:
        cov = coverage(root, a.chapter)
        for w in cov["warnings"]:
            print(f"[warn] {w}")
        for p in cov["problems"]:
            print(f"[BLOCK] {p}")
        if cov["problems"]:
            print(f"\nBLOQUEADO: Fase 0 do cap {a.chapter} incompleta "
                  f"({len(cov['problems'])} problema(s)). Rode/estenda a pesquisa reconciliada.")
            sys.exit(1)
        print(f"OK: Fase 0 do cap {a.chapter} coberta (gap fechado + research reconciliada).")
        if a.apply_frontier:
            new = apply_frontier(root, a.chapter)
            print(f"  kb_frontier -> {new}" if new else "  (kb_frontier nao encontrado em project.json)")
        sys.exit(0)

    out = write_worklist(root, a.chapter)
    d = discover(root, a.chapter)
    print(f"OK kb_phase discover cap {a.chapter}: {len(d['gap'])} candidato(s) nao cobertos (fortes), "
          f"{len(d['weak'])} fraco(s), {len(d['covered'])} coberto(s).")
    print(f"  -> {out}")
    if d["gap"]:
        print("  PESQUISAR: " + ", ".join(r["cand"] for r in d["gap"][:15]))


if __name__ == "__main__":
    main()
