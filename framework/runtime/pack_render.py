"""pack_render.py — renderiza o scene_prompt.md a partir do pacote (ADR 0019).

Nucleo compartilhado: o caminho de sessao grava o prompt, o de API monta a mensagem de usuario com ele. Funcao pura
(pacote + Carta -> texto), sem I/O e sem dependencia dos dois caminhos. `context_pack` reexporta `render_prompt`.
Uma funcao por secao do prompt; a ordem das secoes e a de `render_prompt`.
"""
from __future__ import annotations

import state_index


def _linhas_com_tm(pack: dict) -> int:
    """Quantas linhas do pacote tem traducao exata na TM (a TM pode trazer fala de fora do pacote, entao nao basta contar)."""
    chaves = {state_index._key(e.get("source", "")) for e in pack["tm_exact"]}
    return sum(1 for r in pack["lines"] if state_index._key(r.get("source", "")) in chaves)


def _cabecalho(pack: dict) -> list[str]:
    return [
        f"# Cena {pack['scene']} — pacote de traducao ({pack['n_lines']} linhas)",
        "",
        "> Pacote AUTO-CONTIDO e LIMITADO (so o que esta cena precisa). Traduza EN -> pt-BR",
        "> seguindo a Carta abaixo. Saida exigida ao final. Nao precisa de contexto externo.",
        f"> Memoria de traducao: {_linhas_com_tm(pack)} de {pack['n_lines']} linhas ja tem traducao exata (secao TM).",
        "",
        "---",
        "",
    ]


def _carta(carta: str) -> list[str]:
    L = ["## 1. CARTA DE GOVERNANCA (contrato de qualidade)", ""]
    if carta.strip():
        L.append(carta.strip())
    else:
        L.append("> (Carta fornecida no system cacheado — `framework/skills/translation_governance.md`.)")
    L.append("")
    return L


def _regras(pc: dict) -> list[str]:
    L = ["## 2. Regras do conector / projeto"]
    L.append(f"- Token de quebra de linha: `{pc['newline_token']}` (literal; preservar EXATO, mesma posicao).")
    L.append(f"- Tokens de formatacao a preservar verbatim: {pc['formatting_tokens']} "
             f"+ padroes {pc['formatting_token_patterns']}.")
    L.append("- CRITICO — token `[02]` e QUEBRA DE PAGINA (page break do jogo): "
             "quando o source tem `[02]`, o campo `t` DEVE ter o mesmo numero de `[02]` "
             "na posicao equivalente. Omitir `[02]` causa falha de validacao e texto sem paginacao. "
             "Nao confunda com `[01]` (quebra de linha dentro da mesma pagina). "
             "Regra: contagem de `[02]` em `t` == contagem de `[02]` no texto source.")
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
    return L


def _glossario(pack: dict) -> list[str]:
    L = ["## 3. Glossario relevante (subconjunto desta cena)"]
    if pack["glossary_subset"]:
        curta = any(g.get("forma_curta") for g in pack["glossary_subset"])    # coluna so existe se o glossario a usa
        L.append("| termo | categoria | traducao | regra | spoiler |" + (" forma curta (se a traducao nao couber no byte_budget) |" if curta else ""))
        L.append("|---|---|---|---|---|" + ("---|" if curta else ""))
        for g in pack["glossary_subset"]:
            L.append(f"| {g['term']} | {g['category']} | {g['target_translation']} | "
                     f"{g['handling_rule']} | {g['spoiler_level']} |" + (f" {g.get('forma_curta', '')} |" if curta else ""))
    else:
        L.append("_(nenhum termo do glossario aparece nesta cena)_")
    L.append("")
    return L


def _vozes(pack: dict) -> list[str]:
    L = ["## 4. Vozes presentes"]
    for name, card in pack["voice_cards"].items():
        al = f" (aliases: {', '.join(card['aliases'])})" if card.get("aliases") else ""
        L.append(f"### {name} — criticality: {card.get('criticality','')}{al}")
        for b in card.get("lines", []):
            L.append(f"- {b}")
    L.append("")
    return L


def _decisoes(pack: dict) -> list[str]:
    L = ["## 5. Decisoes relevantes (do decision_log)"]
    for d in pack["decisions"]:
        flag = " [universal]" if d.get("universal") else ""
        L.append(f"- **{d['title']}**{flag}: {d['summary']}")
    _dec_shown = {d["title"] for d in pack["decisions"]}
    dec_sem = [d for d in pack.get("decisions_semantic", []) if d["title"] not in _dec_shown]
    if dec_sem:
        L.append("**Decisoes SEMELHANTES (semantica — aplique se couber no contexto):**")
        for d in dec_sem:
            L.append(f"- (~{d['score']}) **{d['title']}**: {d['summary']}")
    L.append("")
    return L


def _spoiler(pack: dict) -> list[str]:
    guards = pack.get("spoiler_guards", [])
    if not guards:
        return []
    L = ["## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena"]
    L.append("> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a")
    L.append("> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).")
    for g in guards:
        L.append(f"- **{g['entity']}** ({g['spoiler_level']}): {g['guard']}")
    L.append("")
    return L


def _kb(pack: dict) -> list[str]:
    L: list[str] = []
    if pack.get("kb"):
        L.append("## 5c. Lore relevante (KB — apenas fatos JA revelados ate esta cena)")
        for s in pack["kb"]:
            L.append(f"### {s['section']}")
            L.append(s["content"])
        L.append("")
    _kb_shown = {s["section"] for s in pack.get("kb", [])}
    kb_sem = [s for s in pack.get("kb_semantic", []) if s["section"] not in _kb_shown]
    if kb_sem:
        L.append("## 5d. Lore SEMELHANTE (semantica, ADAPTE ao contexto — apenas ja revelada)")
        for s in kb_sem:
            L.append(f"### {s['section']} (~{s['score']})")
            L.append(s["content"])
        L.append("")
    return L


def _memoria(pack: dict) -> list[str]:
    L = ["## 6. Memoria de traducao (consistencia — nao reinventar)"]
    if pack["tm_exact"]:
        L.append("**Falas identicas ja traduzidas (reusar):**")
        for e in pack["tm_exact"]:
            L.append(f"- `{e['source']}` -> `{e['target']}` ({e['speaker']}, {e['from_scene']})")
    if pack["tm_voice"]:
        L.append("**Voz estabelecida dos falantes (amostra):**")
        for e in pack["tm_voice"]:
            L.append(f"- {e['speaker']}: `{e['source']}` -> `{e['target']}`")
    if pack.get("tm_semantic"):
        L.append("**Falas SIMILARES (nao identicas) — use p/ voz/fraseado, ADAPTE ao contexto:**")
        for e in pack["tm_semantic"]:
            L.append(f"- (~{e['score']}) `{e['source']}` -> `{e['target']}`")
    if pack.get("tm_series"):
        L.append("")
        L.append("### 6b. Memoria de traducao da SERIE (outro jogo da mesma franquia)")
        L.append("**Termos ja traduzidos em outro jogo da serie — usar p/ CONSISTENCIA entre jogos:**")
        for e in pack["tm_series"]:
            L.append(f"- `{e['source']}` -> `{e['target']}` (jogo: {e['from_game']})")
    if not pack["tm_exact"] and not pack["tm_voice"] and not pack.get("tm_semantic") and not pack.get("tm_series"):
        L.append("_(sem memoria previa para esta cena)_")
    L.append("")
    return L


def _disciplina_orcamento(pc: dict) -> list[str]:
    L: list[str] = []
    if pc.get("target_charset_supported") is True:
        L.append("> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao em **bytes UTF-8 REAIS**")
        L.append("> (acentos NAO somem na gravacao — cada `c` de cedilha/acento custa byte(s) extra) deve")
        L.append("> **CABER** no byte_budget da linha. pt-BR costuma ser ~15-20% mais longo que EN: em")
        L.append("> linhas curtas/UI (budget baixo) **seja conciso** (ex.: 'adicionado ao' -> 'no'; corte")
        L.append("> redundancia), preservando sentido. Estourar muito o orcamento causa overflow no jogo.")
        L.append("> Conte os tokens de formatacao ({c5} etc.) no tamanho.")
    else:
        L.append("> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`")
        L.append("> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR")
        L.append("> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**")
        L.append("> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o")
        L.append("> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.")
    if pc.get("budget_reserves_terminator"):
        L.append("> O byte_budget listado ja reserva 1 byte para o terminador `\\0` — o texto")
        L.append("> traduzido precisa caber em `byte_budget - 1` bytes, nao no byte_budget cheio.")
    return L


def _linhas(pack: dict, pc: dict) -> list[str]:
    L = ["## 7. Linhas a traduzir"]
    L += _disciplina_orcamento(pc)
    tok = pc.get("newline_token") or ""
    if tok:
        L.append(f"> `nl` = quantas vezes o token de quebra `{tok}` aparece no source: o `t` precisa ter EXATAMENTE `nl`.")
    L.append("| offset | byte_budget | nl | source |")
    L.append("|---|---|---|---|")
    for r in pack["lines"]:
        nl = r["source"].count(tok) if tok else 0
        src = r["source"].replace("|", "\\|")
        L.append(f"| {r['offset']} | {r['byte_budget']} | {nl} | {src} |")
    L.append("")
    return L


def _formato_saida(pack: dict) -> list[str]:
    L = ["## 8. Formato de saida EXIGIDO"]
    L.append(f"Escreva `translations_{pack['scene_id']}.json` com a forma:")
    _known_voices = sorted(pack.get("voice_cards", {}).keys())
    _voice_hint = (", ".join(f"'{v}'" for v in _known_voices) + " ") if _known_voices else ""
    L.append(f"**Campo `speaker`:** use o nome EN exato da secao 4 para personagens conhecidos "
             f"({_voice_hint}); `'npc'` para NPCs sem perfil de voz; `'system'` para "
             f"narrador/sistema/tutorial; `'unknown'` se nao identificavel. "
             f"NAO use descricoes em portugues (ex.: NAO escreva 'Personagem' ou 'Vilao/NPC').")
    L.append("```json")
    L.append('{ "lines": {')
    L.append('  "<offset>": {"speaker": "<nome EN da sec4 | npc | system | unknown>", "tone_register": "...", "intent": "...",')
    L.append('    "risk_level": "low|medium|high|critical", "risk_notes": "(se >= medium)",')
    L.append('    "t": "<traducao pt-BR canonica, com acentos, com o token de quebra exato>"},')
    L.append("  ... 1 entrada por offset acima ...")
    L.append("} }")
    L.append("```")
    L.append("Regras: cobrir TODOS os offsets; preservar o token de quebra; risco >= medium exige")
    L.append("risk_notes; interjeicoes/onomatopeias = traducao (localizar, nao copiar). O build_plan")
    L.append("valida cobertura/tokens/risk_notes; linhas risco>=high passam por back-translation.")
    L.append("")
    return L


def render_prompt(pack: dict, carta: str) -> str:
    pc = pack["project_constraints"]
    L: list[str] = []
    L += _cabecalho(pack)
    L += _carta(carta)
    L += _regras(pc)
    L += _glossario(pack)
    L += _vozes(pack)
    L += _decisoes(pack)
    L += _spoiler(pack)
    L += _kb(pack)
    L += _memoria(pack)
    L += _linhas(pack, pc)
    L += _formato_saida(pack)
    return "\n".join(L)
