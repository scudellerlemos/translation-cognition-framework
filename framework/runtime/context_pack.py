#!/usr/bin/env python3
"""
context_pack.py — monta o CONTEXTO LIMITADO e AUTO-CONTIDO de UMA cena (a peca central do harness).

Em vez de carregar glossario inteiro + decision_log + capitulos anteriores na janela da LLM (contexto
O(historico) -> estoura a sessao), monta um pacote O(cena): so o que ESTA cena precisa.

Pacote = doutrina cacheavel (a Carta) + regras do conector (project.json) + SUBCONJUNTO do glossario
(so termos que aparecem) + voice cards dos falantes relevantes + decisoes relevantes (por tag/universal)
+ hits de memoria de traducao (TM) + as linhas-fonte + byte budgets.

Emite, no dir da cena (`<projeto>/artifacts/<scene>/`):
  - scene_prompt.md : auto-contido, pronto p/ o modelo responder em UM turno (caminho assinatura: da
                      p/ rodar 1 cena por sessao limpa -> contexto nunca acumula).
  - pack.json       : a mesma informacao, estruturada (consumida pelo run_scene / caminho API).

GOVERNANCA: determinista (rodar 2x -> byte-identico), sem rede, sem work-text hardcoded. Le os indices
de `state_index.py` (auto-constroi se faltarem).

Uso:  python context_pack.py <dir-do-projeto> <scene>     ex.: python context_pack.py projects/utawarerumono ch_12_01
"""
from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import state_index  # noqa: E402  (sibling no mesmo dir)

FRAMEWORK = _HERE.parent
CARTA_PATH = FRAMEWORK / "skills" / "translation_governance.md"
TOKEN = chr(92) + "n"

MAX_DECISIONS = 12          # universal + matched, teto p/ manter o pacote limitado
MAX_TM_VOICE_PER_SPEAKER = 3  # exemplos de "voz estabelecida" por falante presente


def scene_id_of(scene: str) -> str:
    return scene[3:] if scene.startswith("ch_") else scene


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def load_dialogs(p: Path):
    rows = []
    with p.open(encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        textcol = "text_source" if "text_source" in (rdr.fieldnames or []) else "text_en"
        for r in rdr:
            rows.append({"offset": r["offset"], "source": r.get(textcol, ""),
                         "byte_budget": int(r["byte_budget"])})
    return rows


def load_glossary(p: Path):
    out = []
    if not p.is_file():
        return out
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append(r)
    return out


def _present(needle: str, blob_low: str) -> bool:
    n = (needle or "").strip().lower()
    if not n:
        return False
    if n.isalnum():
        # tolera plural/inflexao inglesa (termo + s/es opcional): 'gigiri' casa 'gigiris', 'cohort' casa
        # 'cohorts', 'general' casa 'generals'. Possessivo ("ukon's") ja casa pelo \b no apostrofo.
        # Conservador (so sufixo plural) -> mais recall sem virar substring solta. Primitiva unica de
        # match: vale p/ glossario, vozes e gatilhos de spoiler de uma vez.
        return re.search(r"\b" + re.escape(n) + r"(?:e?s)?\b", blob_low) is not None
    return n in blob_low


def select_glossary(glossary, blob_low):
    sub = []
    for g in glossary:
        terms = [g.get("term", "")] + [a for a in (g.get("aliases", "") or "").split(";") if a]
        if any(_present(t, blob_low) for t in terms):
            sub.append({"term": g.get("term", ""), "category": g.get("category", ""),
                        "target_translation": g.get("target_translation", ""),
                        "handling_rule": g.get("handling_rule", ""),
                        "spoiler_level": g.get("spoiler_level", ""),
                        "notes": g.get("notes", "")})
    return sorted(sub, key=lambda x: x["term"].lower())


def select_voices(voice_cards, blob_low):
    """Falantes relevantes = high-criticality (sempre, narracao/voz principal) ∪ os citados na cena."""
    sel = {}
    for name, card in voice_cards.items():
        names = [name] + card.get("aliases", [])
        matched = any(_present(x, blob_low) for x in names)
        if card.get("criticality") == "high" or matched:
            sel[name] = card
    return dict(sorted(sel.items()))


def select_decisions(decisions, present_terms, present_speakers):
    toks = {t.lower() for t in present_terms} | {s.lower() for s in present_speakers}
    chosen, seen = [], set()
    for d in decisions:                       # universais primeiro (regras do conector)
        if d.get("universal") and d["title"] not in seen:
            chosen.append(d); seen.add(d["title"])
    for d in decisions:                       # depois: casadas por TAG (titulo) OU pelo SUMMARY (conteudo)
        if d["title"] in seen:
            continue
        tags = {t.lower() for t in d.get("tags", [])}
        summ = (d.get("summary", "") or "").lower()
        # match por conteudo do summary aumenta o recall de decisoes relevantes que o tag de titulo nao
        # pega (ex.: decisao sobre um termo citado so no corpo). Continua bounded por MAX_DECISIONS.
        if (toks & tags) or any(_present(t, summ) for t in toks):
            chosen.append(d); seen.add(d["title"])
    return chosen[:MAX_DECISIONS]


def load_tm(p: Path):
    tm = []
    if not p.is_file():
        return tm
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            tm.append(json.loads(line))
    return tm


def select_tm(tm, scene_rows, present_speakers):
    """Hits exatos (mesma fala ja traduzida antes) + amostra de voz estabelecida por falante presente."""
    by_key = {}
    for e in tm:
        by_key.setdefault(e["src_key"], e)
    exact = []
    seen_keys = set()
    for r in scene_rows:
        k = state_index._key(r["source"])
        if k in by_key and k not in seen_keys:
            h = by_key[k]
            exact.append({"source": h["source"], "target": h["target"],
                          "speaker": h["speaker"], "from_scene": h["scene"]})
            seen_keys.add(k)
    voice = []
    speakers_low = {s.lower() for s in present_speakers}
    per = {}
    for e in tm:                              # ordem estavel (TM ja vem ordenada)
        sp = (e.get("speaker") or "").lower()
        if sp in speakers_low and per.get(sp, 0) < MAX_TM_VOICE_PER_SPEAKER:
            voice.append({"speaker": e["speaker"], "source": e["source"], "target": e["target"]})
            per[sp] = per.get(sp, 0) + 1
    return exact, voice


def _pos(scene_id: str):
    """scene_id '12_03' -> (12, 3) p/ comparacao numerica de posicao narrativa."""
    return tuple(int(p) for p in str(scene_id).split("_") if p.isdigit())


def select_spoiler_guards(ledger: dict, blob_low: str, scene_id: str) -> list:
    """FILTRO TEMPORAL: para os fatos cujo reveal e FUTURO em relacao a esta cena, retorna o guard de
    ambiguidade se a entidade aparece nesta cena. Disparo por (a) `scenes` explicitas (scene_id) ou (b)
    `triggers` casados por LIMITE DE PALAVRA (_present, evita 'system' em 'system of gears').
    reveal='beyond_frontier' = sempre futuro p/ cenas na fronteira; reveal=<scene_id> = futuro se > a cena."""
    out = []
    here = _pos(scene_id)
    for e in (ledger or {}).get("entries", []):
        rev = e.get("reveal", "beyond_frontier")
        future = True if rev == "beyond_frontier" else (_pos(rev) > here)
        if not future:
            continue
        in_scenes = scene_id in {scene_id_of(s) for s in e.get("scenes", [])}
        by_trigger = any(_present(t, blob_low) for t in e.get("triggers", []))
        if in_scenes or by_trigger:
            out.append({"entity": e.get("entity", ""), "fact": e.get("fact", ""),
                        "spoiler_level": e.get("spoiler_level", ""), "guard": e.get("pre_reveal", "")})
    return out


def project_constraints(cfg: dict) -> dict:
    conn = cfg.get("connector", {})
    return {
        "formatting_tokens": cfg.get("formatting_tokens", []),
        "formatting_token_patterns": cfg.get("formatting_token_patterns", []),
        "system_line_convention": cfg.get("system_line_convention", ""),
        "length_constraints": cfg.get("length_constraints", {}),
        "newline_token": TOKEN,
        "target_charset_supported": conn.get("target_charset_supported", True),
        "charset_note": conn.get("charset_note", ""),
        "space_strategy": conn.get("space_strategy", ""),
    }


def build_pack(root: Path, scene: str) -> dict:
    root = Path(root)
    art = root / "artifacts"
    scene_dir = art / scene
    if not (scene_dir / "dialogs.csv").is_file():
        raise SystemExit(f"ERRO: {scene_dir/'dialogs.csv'} nao encontrado")
    state = art / "state"
    if not (state / "translation_memory.jsonl").is_file():
        state_index.build(root)               # auto-constroi os indices se faltarem

    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    rows = load_dialogs(scene_dir / "dialogs.csv")
    blob_low = "\n".join(r["source"] for r in rows).lower()

    glossary = load_glossary(art / "glossary.csv")
    voice_cards = json.loads(_read(state / "voice_cards.json") or "{}")
    decisions = json.loads(_read(state / "decision_index.json") or "[]")
    tm = load_tm(state / "translation_memory.jsonl")

    gsub = select_glossary(glossary, blob_low)
    voices = select_voices(voice_cards, blob_low)
    present_terms = [g["term"] for g in gsub]
    present_speakers = list(voices.keys())
    dsel = select_decisions(decisions, present_terms, present_speakers)
    tm_exact, tm_voice = select_tm(tm, rows, present_speakers)

    ledger = json.loads(_read(art / "spoiler_ledger.json") or "{}")
    spoiler_guards = select_spoiler_guards(ledger, blob_low, scene_id_of(scene))

    return {
        "scene": scene, "scene_id": scene_id_of(scene), "n_lines": len(rows),
        "doctrine": "framework/skills/translation_governance.md",
        "project_constraints": project_constraints(cfg),
        "glossary_subset": gsub,
        "voice_cards": voices,
        "decisions": dsel,
        "tm_exact": tm_exact,
        "tm_voice": tm_voice,
        "spoiler_guards": spoiler_guards,
        "lines": rows,
    }


# ------------------------------ render scene_prompt ----------------------------

def render_prompt(pack: dict, carta: str) -> str:
    pc = pack["project_constraints"]
    L = []
    L.append(f"# Cena {pack['scene']} — pacote de traducao ({pack['n_lines']} linhas)")
    L.append("")
    L.append("> Pacote AUTO-CONTIDO e LIMITADO (so o que esta cena precisa). Traduza EN -> pt-BR")
    L.append("> seguindo a Carta abaixo. Saida exigida ao final. Nao precisa de contexto externo.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 1. CARTA DE GOVERNANCA (contrato de qualidade)")
    L.append("")
    if carta.strip():
        L.append(carta.strip())
    else:
        L.append("> (Carta fornecida no system cacheado — `framework/skills/translation_governance.md`.)")
    L.append("")
    L.append("## 2. Regras do conector / projeto")
    L.append(f"- Token de quebra de linha: `{pc['newline_token']}` (literal; preservar EXATO, mesma posicao).")
    L.append(f"- Tokens de formatacao a preservar verbatim: {pc['formatting_tokens']} "
             f"+ padroes {pc['formatting_token_patterns']}.")
    if pc.get("system_line_convention"):
        L.append(f"- Convencao de linha de sistema: {pc['system_line_convention']}.")
    lc = pc.get("length_constraints", {})
    if lc:
        L.append(f"- Restricao de comprimento: {lc} (orcamento em bytes por linha — ver coluna byte_budget).")
    if not pc.get("target_charset_supported", True):
        L.append(f"- ATENCAO charset: {pc['charset_note'][:200]}")
        L.append("  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: \"você\", "
                 "\"coração\"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — "
                 "nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido "
                 "(ex.: evite pares que so diferem por acento), pois ele some no jogo.")
    L.append("")
    L.append("## 3. Glossario relevante (subconjunto desta cena)")
    if pack["glossary_subset"]:
        L.append("| termo | categoria | traducao | regra | spoiler |")
        L.append("|---|---|---|---|---|")
        for g in pack["glossary_subset"]:
            L.append(f"| {g['term']} | {g['category']} | {g['target_translation']} | "
                     f"{g['handling_rule']} | {g['spoiler_level']} |")
    else:
        L.append("_(nenhum termo do glossario aparece nesta cena)_")
    L.append("")
    L.append("## 4. Vozes presentes")
    for name, card in pack["voice_cards"].items():
        al = f" (aliases: {', '.join(card['aliases'])})" if card.get("aliases") else ""
        L.append(f"### {name} — criticality: {card.get('criticality','')}{al}")
        for b in card.get("lines", []):
            L.append(f"- {b}")
    L.append("")
    L.append("## 5. Decisoes relevantes (do decision_log)")
    for d in pack["decisions"]:
        flag = " [universal]" if d.get("universal") else ""
        L.append(f"- **{d['title']}**{flag}: {d['summary']}")
    L.append("")
    guards = pack.get("spoiler_guards", [])
    if guards:
        L.append("## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena")
        L.append("> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a")
        L.append("> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).")
        for g in guards:
            L.append(f"- **{g['entity']}** ({g['spoiler_level']}): {g['guard']}")
        L.append("")
    L.append("## 6. Memoria de traducao (consistencia — nao reinventar)")
    if pack["tm_exact"]:
        L.append("**Falas identicas ja traduzidas (reusar):**")
        for e in pack["tm_exact"]:
            L.append(f"- `{e['source']}` -> `{e['target']}` ({e['speaker']}, {e['from_scene']})")
    if pack["tm_voice"]:
        L.append("**Voz estabelecida dos falantes (amostra):**")
        for e in pack["tm_voice"]:
            L.append(f"- {e['speaker']}: `{e['source']}` -> `{e['target']}`")
    if not pack["tm_exact"] and not pack["tm_voice"]:
        L.append("_(sem memoria previa para esta cena)_")
    L.append("")
    L.append("## 7. Linhas a traduzir")
    L.append("> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`")
    L.append("> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR")
    L.append("> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**")
    L.append("> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o")
    L.append("> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.")
    L.append("| offset | byte_budget | source |")
    L.append("|---|---|---|")
    for r in pack["lines"]:
        src = r["source"].replace("|", "\\|")
        L.append(f"| {r['offset']} | {r['byte_budget']} | {src} |")
    L.append("")
    L.append("## 8. Formato de saida EXIGIDO")
    L.append(f"Escreva `translations_{pack['scene_id']}.json` com a forma:")
    L.append("```json")
    L.append('{ "lines": {')
    L.append('  "<offset>": {"speaker": "...", "tone_register": "...", "intent": "...",')
    L.append('    "risk_level": "low|medium|high|critical", "risk_notes": "(se >= medium)",')
    L.append('    "t": "<traducao pt-BR canonica, com acentos, com o token de quebra exato>"},')
    L.append("  ... 1 entrada por offset acima ...")
    L.append("} }")
    L.append("```")
    L.append("Regras: cobrir TODOS os offsets; preservar o token de quebra; risco >= medium exige")
    L.append("risk_notes; interjeicoes/onomatopeias = traducao (localizar, nao copiar). O build_plan")
    L.append("valida cobertura/tokens/risk_notes; linhas risco>=high passam por back-translation.")
    L.append("")
    return "\n".join(L)


def write_pack(root: Path, scene: str) -> dict:
    pack = build_pack(root, scene)
    scene_dir = Path(root) / "artifacts" / scene
    carta = _read(CARTA_PATH)
    (scene_dir / "scene_prompt.md").write_text(render_prompt(pack, carta), encoding="utf-8")
    (scene_dir / "pack.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    return pack


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        sys.exit("uso: python context_pack.py <dir-do-projeto> <scene>")
    root, scene = Path(args[0]), args[1]
    pack = write_pack(root, scene)
    print(f"OK context_pack {scene}: {pack['n_lines']} linhas")
    print(f"  glossario: {len(pack['glossary_subset'])} termos | vozes: {len(pack['voice_cards'])} "
          f"| decisoes: {len(pack['decisions'])} | TM exato: {len(pack['tm_exact'])} "
          f"| TM voz: {len(pack['tm_voice'])}")
    print(f"  -> artifacts/{scene}/scene_prompt.md + pack.json")


if __name__ == "__main__":
    main()
