#!/usr/bin/env python3
"""
kb_concordance.py — sinaliza concordancia entre o rascunho draft_ollama (kb_build_ollama.py) e a
pesquisa humana ja registrada, como TRIAGEM pra Fase 1B (skill 03) -- read-only, nunca bloqueia
(mesmo padrao "digest" de kb_review.py). Nao existe hoje nenhuma "pesquisa humana" estruturada
comparavel (kb_ratified.csv e so nome+data, sem texto) -- a comparacao viavel e entre a
'definicao' do rascunho e o texto das fontes do cache marcadas 'encontrada_por: usuario' (as que
o humano indicou como confiaveis, ver kb_fetch.py).

O gate de promocao (kb_reconcile.py::promote(), kb_ratified.csv + humano) NAO muda -- este modulo
so reduz o esforco de comparacao, nunca decide sozinho.

Uso: python kb_concordance.py <projeto>
     python kb_reconcile.py <projeto> --concordance
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_WORD_BOUNDARY_CACHE: dict[str, re.Pattern] = {}


def _name_pattern(name_low: str) -> re.Pattern:
    """Regex com fronteira de palavra p/ o nome da entidade -- \\b evita casar substring dentro
    de outra palavra (ex.: 'Ana' dentro de 'banana'). Nomes comuns em pt-BR usados como entidade
    (ex.: 'Sistema', 'Tio') ainda podem casar legitimamente como palavra solta sem relacao com a
    entidade -- limitacao conhecida e aceitavel aqui: este modulo e so TRIAGEM (nunca decide
    sozinho, ver docstring do modulo); um falso positivo so faz uma entidade comum ganhar uma
    comparacao a mais, nunca bloqueia nem promove nada."""
    pat = _WORD_BOUNDARY_CACHE.get(name_low)
    if pat is None:
        pat = re.compile(rf"\b{re.escape(name_low)}\b")
        _WORD_BOUNDARY_CACHE[name_low] = pat
    return pat

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
from kb_reconcile import _ENTITY_BLOCK_RE  # noqa: E402  (reusa parser de entidade do rascunho)

_FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
_DEFINICAO_RE = re.compile(r"\*\*Definicao:\*\*\n(.+?)\n\n", re.S)

# cosine similarity >= isto -> "alta" concordancia; < isto -> "baixa". Ponto de partida arbitrario
# (nenhum dado real de calibracao existe ainda) -- ajustavel conforme uso real acumula.
_HIGH_THRESHOLD = 0.85


def _load_human_cache_texts(root: Path) -> list[tuple[str, str]]:
    """[(hash, texto)] das fontes do cache marcadas 'encontrada_por: usuario' -- unico artefato
    hoje que se aproxima de 'pesquisa humana' registrada e comparavel por texto."""
    d = paths.research_cache_dir(root)
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.md")):
        raw = p.read_text(encoding="utf-8")
        m = _FRONT_RE.match(raw)
        meta: dict = {}
        texto = raw
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            texto = raw[m.end():]
        if meta.get("encontrada_por") == "usuario":
            out.append((p.stem, texto))
    return out


def _entity_definitions(root: Path) -> dict[str, str]:
    """{nome: definicao} do rascunho universe_knowledge_base.md -- so entidades com conteudo
    afirmado (found=true); UNSOURCED nao tem definicao real pra comparar."""
    kb = paths.artifacts(root) / "universe_knowledge_base.md"
    if not kb.is_file():
        return {}
    txt = kb.read_text(encoding="utf-8")
    out = {}
    for m in _ENTITY_BLOCK_RE.finditer(txt):
        name, body = m.group(1).strip(), m.group(2)
        def_m = _DEFINICAO_RE.search(body)
        definicao = def_m.group(1).strip() if def_m else ""
        if definicao and not definicao.upper().startswith("UNSOURCED"):
            out[name] = definicao
    return out


def _get_embedder():
    """Import tardio -- so exige sentence-transformers instalado quando ha de fato entidade com
    fonte humana pra comparar (mesmo padrao lazy do proprio embedder.py)."""
    db_dir = str(Path(__file__).resolve().parents[1] / "db")
    if db_dir not in sys.path:
        sys.path.insert(0, db_dir)
    from embedder import Embedder
    return Embedder()


def concordance(root, *, embed_fn=None) -> list[dict]:
    """Read-only, nunca bloqueia. Retorna lista ordenada por nome de
    {name, level, score, human_sources}. level in {"alta", "baixa", "sem_pesquisa_humana"};
    score e None quando level == "sem_pesquisa_humana" (nunca um score 0 silencioso).

    `embed_fn(texts: list[str]) -> list[list[float]]` injetavel p/ teste (default: Embedder real
    de framework/db/embedder.py -- mesmo padrao de chat_fn em kb_build_ollama.build())."""
    root = Path(root)
    definitions = _entity_definitions(root)
    if not definitions:
        return []
    human_cache = _load_human_cache_texts(root)

    results = []
    to_embed = []  # (name, definicao, texto_humano_concatenado, n_fontes)
    for name, definicao in definitions.items():
        pat = _name_pattern(name.lower())
        matches = [texto for _hash, texto in human_cache if pat.search(texto.lower())]
        if not matches:
            results.append({"name": name, "level": "sem_pesquisa_humana", "score": None,
                            "human_sources": 0})
            continue
        to_embed.append((name, definicao, "\n".join(matches), len(matches)))

    if not to_embed:
        return sorted(results, key=lambda r: r["name"].lower())

    embed = embed_fn or _get_embedder().encode
    draft_vecs = embed([t[1] for t in to_embed])
    human_vecs = embed([t[2] for t in to_embed])
    for (name, _definicao, _human_txt, n_sources), dv, hv in zip(
        to_embed, draft_vecs, human_vecs, strict=True
    ):
        # vetores unit-norm (Embedder.encode normaliza) -> cosine = produto escalar direto.
        score = round(sum(a * b for a, b in zip(dv, hv, strict=True)), 4)
        level = "alta" if score >= _HIGH_THRESHOLD else "baixa"
        results.append({"name": name, "level": level, "score": score, "human_sources": n_sources})

    return sorted(results, key=lambda r: r["name"].lower())


def _print_report(items: list[dict]):
    if not items:
        print("[kb_concordance] nenhuma entidade com definicao no rascunho "
              "(rode kb_build_ollama.py primeiro).")
        return
    for it in items:
        score = f" score={it['score']:.4f}" if it["score"] is not None else ""
        print(f"  {it['name']}: {it['level']}{score} ({it['human_sources']} fonte(s) humana(s))")
    print("\n(triagem informativa -- nao substitui --promote/kb_ratified.csv.)")


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Sinaliza concordancia rascunho x pesquisa humana (triagem, nao gate).")
    ap.add_argument("project")
    a = ap.parse_args()
    _print_report(concordance(a.project))


if __name__ == "__main__":
    main()
