#!/usr/bin/env python3
"""
cost_model.py — modelo de CUSTO DE PRODUÇÃO (via API) do pipeline de tradução.

Estima o custo em $ de traduzir um corpus sob o processo da Carta (lotes + micro-QA +
back-translation de alto risco + QA final), em 3 cenários, e projeta para o jogo inteiro.
Genérico: lê `project.json` + artefatos reais; calibra os tokens no conteúdo do próprio arco.

⚠️ HONESTIDADE:
- Estima o custo de PRODUÇÃO (chamadas de API em lote com caching) — NÃO o custo desta sessão
  conversacional. É o número que prevê a meia-maratona / run de 33k.
- Tokens são ESTIMADOS por heurística (≈chars/3.8). Para um número fechado, recontar com a API
  `messages.count_tokens` (ver skill claude-api / shared/token-counting.md). A precisão aqui é de
  ORDEM DE GRANDEZA + os deltas relativos entre cenários, não centavos.

Preços (US$/Mtok, cache do skill claude-api em 2026-05-26):
  Opus 4.8  : in 5.00  / out 25.00      Sonnet 4.6: in 3.00 / out 15.00      Haiku 4.5: in 1.00 / out 5.00
  cache write ≈ 1.25× input (TTL 5min) ; cache read ≈ 0.1× input

Uso:  python cost_model.py <dir-do-projeto> [--report]   (--report grava artifacts/cost_report.md)
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

# --- preços US$ por TOKEN (Mtok/1e6). Fonte: skill claude-api, cache 2026-05-26 ---
PRICE = {
    "opus":   {"in": 5.00e-6, "out": 25.00e-6},
    "sonnet": {"in": 3.00e-6, "out": 15.00e-6},
    "haiku":  {"in": 1.00e-6, "out":  5.00e-6},
}
CACHE_WRITE = 1.25   # × input (TTL 5min)
CACHE_READ = 0.10    # × input

# --- heurísticas do processo (documentadas; ajustáveis) ---
CHARS_PER_TOKEN = 3.8
META_TOK_PER_LINE = 60      # speaker/tone/intent/risk por linha (saída do plano)
INSTR_TOK = 400            # overhead de instrução por chamada
QA_OUT_TOK_PER_LINE = 15   # achados de micro-QA por linha revista
FINAL_QA_OUT_PER_LINE = 5  # relatório de QA final por linha


def _toks(s: str) -> int:
    return int(len(s or "") / CHARS_PER_TOKEN) + 1


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def estimate(root: Path) -> dict:
    root = Path(root)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    batch = int(cfg.get("batch_size", 200))
    art = root / "artifacts"

    # contexto CACHEÁVEL por prompt (glossário + voz + Carta/regras + fatia de KB)
    ctx_chars = sum(len(_read(art / f)) for f in
                    ("glossary.csv", "tone_analysis.md", "translation_rules.md",
                     "universe_knowledge_base.md"))
    carta = _read(root.parent.parent / "framework" / "skills" / "translation_governance.md")
    ctx_tok = _toks(" " * ctx_chars) + _toks(carta)

    # corpus: tokens de source e alvo por linha; nº de linhas; nº de alto risco
    plan_f = art / "translation_plan.json"
    if plan_f.is_file():
        lines = json.loads(plan_f.read_text(encoding="utf-8")).get("lines", [])
        src_tok = sum(_toks(l.get("text_source", "")) for l in lines)
        tgt_tok = sum(_toks(l.get("base_translation", "")) for l in lines)
        n = len(lines)
        n_high = sum(1 for l in lines if l.get("risk_level") in ("high", "critical"))
        risk = {"low": sum(1 for l in lines if l.get("risk_level") == "low"),
                "medium": sum(1 for l in lines if l.get("risk_level") == "medium"),
                "high": n_high}
    else:
        rows = list(csv.DictReader((art / "dialogs.csv").open(encoding="utf-8")))
        src_tok = sum(_toks(r.get("text_source", "")) for r in rows)
        n = len(rows); tgt_tok = src_tok; n_high = 0; risk = {"low": n, "medium": 0, "high": 0}

    n_batches = max(1, (n + batch - 1) // batch)
    return {"batch": batch, "ctx_tok": ctx_tok, "src_tok": src_tok, "tgt_tok": tgt_tok,
            "n": n, "n_high": n_high, "n_batches": n_batches, "risk": risk}


def _call_cost(in_tok, out_tok, model, ctx_tok=0, cache=False):
    """Custo de 1 chamada. Se cache=True, o contexto é cache-read (0.1×); senão input cheio."""
    p = PRICE[model]
    if cache:
        cost_in = (in_tok - ctx_tok) * p["in"] + ctx_tok * p["in"] * CACHE_READ
    else:
        cost_in = in_tok * p["in"]
    return cost_in + out_tok * p["out"]


def _scenario(e, *, models, cache):
    """models: dict com 'low'/'medium'/'high'/'qa'/'back' -> nome do modelo.
    cache: aplica prompt caching do contexto. Retorna $ total + breakdown."""
    ctx = e["ctx_tok"]; batch = e["batch"]; nb = e["n_batches"]
    src_per = e["src_tok"] / e["n"]; tgt_per = e["tgt_tok"] / e["n"]
    # tradução: 1 chamada por lote. in = ctx + batch*src + instr ; out = batch*(tgt+meta)
    trans = 0.0
    for _ in range(nb):
        in_tok = ctx + batch * src_per + INSTR_TOK
        out_tok = batch * (tgt_per + META_TOK_PER_LINE)
        # modelo médio do lote: mistura por risco (aprox: usa 'medium' como base, 'low' p/ baratos)
        m = models["medium"]
        trans += _call_cost(in_tok, out_tok, m, ctx, cache)
    # caching: o 1º lote ESCREVE o cache (1.25×) em vez de ler
    if cache:
        p = PRICE[models["medium"]]
        trans += ctx * p["in"] * (CACHE_WRITE - CACHE_READ)   # diferença write-vs-read no 1º lote
    # micro-QA: 1 chamada por lote
    qa = 0.0
    for _ in range(nb):
        in_tok = ctx + batch * (src_per + tgt_per) + INSTR_TOK
        out_tok = batch * QA_OUT_TOK_PER_LINE
        qa += _call_cost(in_tok, out_tok, models["qa"], ctx, cache)
    # back-translation: 1 chamada em lote com as linhas de alto risco
    back = 0.0
    if e["n_high"]:
        in_tok = ctx + e["n_high"] * (src_per + tgt_per) + INSTR_TOK
        out_tok = e["n_high"] * (src_per + 20)
        back = _call_cost(in_tok, out_tok, models["back"], ctx, cache)
    # QA final: 1 passe no corpus
    in_tok = ctx + e["src_tok"] + e["tgt_tok"] + INSTR_TOK
    out_tok = e["n"] * FINAL_QA_OUT_PER_LINE
    final = _call_cost(in_tok, out_tok, models["qa"], ctx, cache)
    total = trans + qa + back + final
    return {"total": total, "trans": trans, "qa": qa, "back": back, "final": final}


def cost_scenarios(root: Path) -> dict:
    e = estimate(root)
    sc = {
        # 1) tudo no modelo forte, sem cache (baseline pessimista)
        "forte": _scenario(e, models=dict(low="opus", medium="opus", high="opus",
                                          qa="opus", back="opus"), cache=False),
        # 2) model-mix: tradução Sonnet, QA Sonnet, back-translation Opus
        "mix": _scenario(e, models=dict(low="haiku", medium="sonnet", high="opus",
                                        qa="sonnet", back="opus"), cache=False),
        # 3) model-mix + prompt caching do contexto estável
        "mix_cache": _scenario(e, models=dict(low="haiku", medium="sonnet", high="opus",
                                              qa="sonnet", back="opus"), cache=True),
    }
    return {"estimate": e, "scenarios": sc}


def main():
    args = sys.argv[1:]
    report = "--report" in args
    root = Path(next((a for a in args if not a.startswith("--")), "."))
    r = cost_scenarios(root)
    e = r["estimate"]; n = e["n"]
    GAME = 33000
    lines = [
        f"Arco: {n} linhas | lotes de {e['batch']} ({e['n_batches']}) | alto risco: {e['n_high']} "
        f"| risco {e['risk']}",
        f"Contexto cacheável ~{e['ctx_tok']} tok | source ~{e['src_tok']} tok | alvo ~{e['tgt_tok']} tok",
        "",
        f"{'cenário':<12}{'$ arco':>10}{'$/1k linhas':>14}{'$ ~33k (proj.)':>18}",
    ]
    for name, sc in r["scenarios"].items():
        per_k = sc["total"] / n * 1000
        proj = per_k * GAME / 1000
        lines.append(f"{name:<12}{sc['total']:>10.3f}{per_k:>14.3f}{proj:>18.2f}")
    base = r["scenarios"]["forte"]["total"]
    save = 100 * (1 - r["scenarios"]["mix_cache"]["total"] / base) if base else 0
    lines += ["", f"Economia mix+cache vs forte: -{save:.0f}%",
              "(estimativa por heurística de tokens ≈chars/3.8 + caching; refinar com count_tokens)"]
    out = "\n".join(lines)
    print(out)
    if report:
        rp = root / "artifacts" / "cost_report.md"
        rp.write_text("# Cost Report — modelo de custo de PRODUÇÃO (via API)\n\n"
                      "> Estima o custo de produção (API, lotes + caching), **não** o desta sessão.\n"
                      "> Tokens ≈chars/3.8 (refinar com `messages.count_tokens`). Preços: skill claude-api 2026-05-26.\n\n"
                      "```\n" + out + "\n```\n", encoding="utf-8")
        print(f"\nrelatório -> {rp}")


if __name__ == "__main__":
    main()
