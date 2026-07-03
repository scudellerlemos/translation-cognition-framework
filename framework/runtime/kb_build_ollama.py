#!/usr/bin/env python3
"""
kb_build_ollama.py — sintetiza um RASCUNHO de research_log.md + universe_knowledge_base.md usando
Ollama LOCAL (zero custo de API), a partir do cache produzido por kb_fetch.py.

Parte 2 do pipeline hibrido de KB (P1.7-E). NAO substitui a Fase 1B (reconciliacao IA+humano) da
skill 03 -- produz so o INSUMO BRUTO (extracao factual por entidade, com citacao de fonte), sempre
com status: draft_ollama (NUNCA reconciled). kb_gate.py ja bloqueia rascunho nao-reconciliado sem
nenhuma mudanca (a regex de status nao casa draft_ollama) -- a promocao pra reconciled continua
manual/via sessao Claude, depois de comparar com a pesquisa humana (Fase 1B de verdade).

confianca do Ollama e estruturalmente limitada a low/medium (nunca high, ver _SCHEMA) -- alta
confianca exige reconciliacao, que este script nao faz. Guiado por entities.csv (so importance
main/secondary): nao extrai entidade nova, so busca o que a Fase 1/2 ja validou -- mesma doutrina
"nao inventar" da skill 03.

Uso:  python kb_build_ollama.py <projeto> [--model qwen2.5:14b]
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
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)

_MAX_CONTEXT_CHARS = 12_000   # teto de contexto por chamada -- qwen2.5:14b local, run barato/rapido
_CONFIDENCE_ALLOWED = ("low", "medium")

_SCHEMA = {
    "type": "object",
    "required": ["found", "definicao", "fontes", "confianca"],
    "properties": {
        "found": {"type": "boolean"},
        "definicao": {"type": "string"},
        "fontes": {"type": "array", "items": {"type": "string"}},
        "confianca": {"type": "string", "enum": list(_CONFIDENCE_ALLOWED)},
    },
}

_FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def _parse_cache_file(path: Path) -> dict:
    """Le 1 arquivo de artifacts/research_cache/*.md: front-matter (fonte/tipo/fetched_em/truncado/
    encontrada_por) + texto normalizado. Retorna {"hash", "fonte", "tipo", "texto", "encontrada_por"}.
    Cache antigo sem 'encontrada_por' (gerado antes deste campo existir) cai no default -- nao quebra."""
    raw = path.read_text(encoding="utf-8")
    m = _FRONT_RE.match(raw)
    meta: dict = {}
    texto = raw
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        texto = raw[m.end():]
    return {"hash": path.stem, "fonte": meta.get("fonte", path.stem),
            "tipo": meta.get("tipo", "?"), "texto": texto,
            "encontrada_por": meta.get("encontrada_por", "ia")}


def _load_cache(root: Path) -> list[dict]:
    d = paths.research_cache_dir(root)
    if not d.is_dir():
        return []
    return [_parse_cache_file(p) for p in sorted(d.glob("*.md"))]


def _load_entities(root: Path) -> list[dict]:
    """Entidades main/secondary de entities.csv -- guia o que o Ollama busca (nao extrai entidade
    nova). Pre-requisito da skill 03 (Passo 1/2), ja deve existir neste ponto do pipeline."""
    f = paths.entities(root)
    if not f.is_file():
        return []
    with f.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return [r for r in rows if (r.get("importance") or "").strip() in ("main", "secondary")]


def _context_for(cache: list[dict], budget: int) -> tuple[str, list[str]]:
    """Concatena os textos do cache com marcador [FONTE:hash], truncado a `budget` caracteres --
    qwen2.5:14b local tem janela de contexto limitada; teto conservador e documentado. Retorna
    (texto, hashes_descartados) -- fontes que nao couberam NADA no orcamento (nao so as truncadas
    parcialmente). NUNCA descartar em silencio: o caller avisa o humano (mesmo padrao ja usado no
    resto do projeto p/ qualquer corte por teto, ex.: budget_excluded do run_chapter)."""
    parts, used, dropped = [], 0, []
    for c in cache:
        if used >= budget:
            dropped.append(c["hash"])
            continue
        chunk = f"[FONTE:{c['hash']}]\n{c['texto']}\n"
        if used + len(chunk) > budget:
            chunk = chunk[: max(0, budget - used)]
        parts.append(chunk)
        used += len(chunk)
    return "".join(parts), dropped


def _prompt_for(entity_name: str, aliases: str, context: str) -> str:
    names = entity_name if not aliases else f"{entity_name} (aliases: {aliases})"
    return (
        f"Fontes de pesquisa (marcadas [FONTE:hash]):\n\n{context}\n\n"
        f"Baseado SOMENTE no texto acima, descreva a entidade '{names}'. "
        "Se as fontes NAO mencionarem essa entidade, responda found=false e definicao vazia -- "
        "NAO invente. Se mencionarem, escreva uma definicao curta (1-3 frases) baseada exclusivamente "
        "no texto, liste os hashes de FONTE usados (ex: [\"abc123\"]), e uma confianca "
        "'low' (fonte fraca/ambigua) ou 'medium' (fonte clara e direta)."
    )


def _clamp_confidence(v) -> str:
    v = str(v or "").strip().lower()
    return v if v in _CONFIDENCE_ALLOWED else "low"


def _default_chat(model, messages, fmt):
    from ollama_client import OLLAMA_MODEL_DEFAULT, _chat, _text_of
    resp = _chat(model or OLLAMA_MODEL_DEFAULT, messages, fmt=fmt)
    return json.loads(_text_of(resp))


def build(root, *, chat_fn=None, model=None) -> dict:
    """Le artifacts/research_cache/*.md + entities.csv (main/secondary), pergunta ao Ollama (1
    chamada por entidade, JSON schema estrito) e escreve research_log.md + universe_knowledge_base.md
    RASCUNHO (status: draft_ollama, NUNCA reconciled). Retorna {entities_covered, entities_unsourced,
    sources_read}. `chat_fn(model, messages, fmt) -> dict` injetavel p/ teste (default: Ollama real).
    Sem cache (nenhuma fonte buscada ainda) -> toda entidade vira UNSOURCED sem chamar o modelo
    (nao ha o que extrair; evita chamada inutil e garante "nao inventar" mesmo sem fontes)."""
    root = Path(root)
    chat = chat_fn or _default_chat
    cache = _load_cache(root)
    entities = _load_entities(root)

    # contexto e o MESMO p/ toda entidade -- monta 1x (nao a cada iteracao) e avisa se alguma fonte
    # nao coube no orcamento (nunca descartar em silencio).
    context, dropped = ("", []) if not cache else _context_for(cache, _MAX_CONTEXT_CHARS)
    if dropped:
        print(f"[kb_build_ollama] AVISO: {len(dropped)} fonte(s) nao couberam no contexto "
              f"(teto de {_MAX_CONTEXT_CHARS} chars) e foram descartadas p/ TODAS as entidades: "
              f"{dropped}. Considere rodar kb_fetch com fontes menores/mais focadas, ou aumentar "
              f"_MAX_CONTEXT_CHARS.")

    kb_sections, covered, unsourced = [], 0, 0
    for ent in entities:
        name = (ent.get("canonical_name") or "").strip()
        if not name:
            continue
        aliases = (ent.get("aliases") or "").strip()
        if not cache:
            data = {"found": False, "definicao": "", "fontes": [], "confianca": "low"}
        else:
            messages = [{"role": "user", "content": _prompt_for(name, aliases, context)}]
            try:
                data = chat(model, messages, _SCHEMA)
            except Exception as e:
                data = {"found": False, "definicao": "", "fontes": [], "confianca": "low", "_erro": str(e)}
        if data.get("found"):
            covered += 1
            conf = _clamp_confidence(data.get("confianca"))
            fontes = data.get("fontes") or []
            fontes_md = "\n".join(f"- {f}" for f in fontes) if fontes else "- (nenhuma citada pelo Ollama)"
            kb_sections.append(
                f"## {name}\n\n"
                f"**Definicao:**\n{str(data.get('definicao', '')).strip()}\n\n"
                f"**Fontes:**\n{fontes_md}\n\n"
                "**Relacoes:**\n(nao avaliado -- Ollama nao infere relacoes; revisar na reconciliacao)\n\n"
                "**Papel narrativo:**\n(nao avaliado -- revisar na reconciliacao)\n\n"
                "**Contexto de uso:**\n(nao avaliado -- revisar na reconciliacao)\n\n"
                f"**Status de confianca:**\n{conf} (rascunho Ollama -- nunca 'high' antes de reconciliacao humana)\n"
            )
        else:
            unsourced += 1
            kb_sections.append(
                f"## {name}\n\n"
                "**Definicao:**\nUNSOURCED -- nenhuma fonte do cache menciona esta entidade.\n\n"
                "**Fontes:**\n(nenhuma)\n\n**Relacoes:**\n(nenhuma)\n\n"
                "**Papel narrativo:**\n(nenhum)\n\n**Contexto de uso:**\n(nenhum)\n\n"
                "**Status de confianca:**\nUNSOURCED\n"
            )

    _write_research_log(root, cache)
    _write_kb(root, kb_sections)
    return {"entities_covered": covered, "entities_unsourced": unsourced, "sources_read": len(cache)}


def _write_research_log(root: Path, cache: list[dict]):
    rows = "\n".join(
        f"| SRC-{i + 1:03d} | {c['fonte']} | {c['tipo']} | ? | ? | {c['fonte']} | "
        f"{'Usuario' if c['encontrada_por'] == 'usuario' else 'IA'} (rascunho Ollama) | Sim | "
        "tier a atribuir na reconciliacao |"
        for i, c in enumerate(cache)
    ) or "| (nenhuma fonte no cache -- rode kb_fetch.py primeiro) |"
    txt = (
        "# Research Log (rascunho Ollama)\n\n"
        "**Status:** draft_ollama\n"
        "**human_input:** pending\n\n"
        "> Gerado por kb_build_ollama.py -- extracao factual bruta, SEM reconciliacao IA+humano.\n"
        "> Nao promover pra 'reconciled' sem rodar a Fase 1B da skill 03 (comparar com a pesquisa\n"
        "> humana, resolver conflitos, atribuir tier de verdade).\n\n"
        "## Fontes Avaliadas\n\n"
        "| ID | Fonte | Tipo | Tier | Cobertura de Spoiler | URL/Caminho | Encontrada por | Usada | Notas |\n"
        "|----|-------|------|------|----------------------|-------------|-----------------|-------|-------|\n"
        f"{rows}\n\n"
        "## Conflitos Resolvidos\n\n(nenhum -- reconciliacao ainda nao rodou)\n\n"
        "## Gaps de Pesquisa\n\n(preencher na reconciliacao, apos comparar com entidades UNSOURCED do KB)\n"
    )
    out = paths.research_log(root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")


def _write_kb(root: Path, sections: list[str]):
    header = (
        "# Universe Knowledge Base (rascunho Ollama)\n\n"
        "> status: draft_ollama -- gerado por kb_build_ollama.py, extracao factual por entidade a\n"
        "> partir do cache de kb_fetch.py. NAO reconciliado -- revisar cada entrada na Fase 1B da\n"
        "> skill 03 antes de considerar esta KB pronta para traduzir.\n\n"
    )
    out = paths.artifacts(root) / "universe_knowledge_base.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + "\n---\n\n".join(sections), encoding="utf-8")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Sintetiza rascunho de KB via Ollama local (nunca reconciled).")
    ap.add_argument("project")
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    r = build(a.project, model=a.model)
    print(f"[kb_build_ollama] {r['entities_covered']} entidade(s) coberta(s), "
          f"{r['entities_unsourced']} UNSOURCED, {r['sources_read']} fonte(s) lida(s).")
    print("status: draft_ollama -- rode a reconciliacao (skill 03, Fase 1B) antes de traduzir.")


if __name__ == "__main__":
    main()
