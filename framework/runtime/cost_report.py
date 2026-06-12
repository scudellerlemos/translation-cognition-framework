#!/usr/bin/env python3
"""
cost_report.py — contabilidade REAL de gasto de API a partir do api_ledger.jsonl.

O metrics.jsonl e um resumo SO-DE-SUCESSO (1 linha por cena que fechou no verify). Ele perde:
  - cenas que falharam DEPOIS de ja chamar a API (cobertura estourou -> excecao; verify reprovou);
  - cada re-traducao do escalonamento de fitting (1.40->1.15->1.0) — varias chamadas, 1 cena;
  - back-translations que quebraram no parse mas ja foram cobradas.
Foi por isso que a estimativa (~$9-10) ficou abaixo do real (~$15): o que falhou gastou e nao apareceu.

O api_ledger.jsonl (escrito por model.log_api_call, 1 linha por chamada CONCLUIDA, ANTES de qualquer
parse/gate) e a VERDADE de gasto. Este script o agrega: total, por modelo, por tipo (translate/back),
por cena, e — cruzando com run_state.json — quanto foi DESPERDICADO (cenas que nao terminaram `verified`).

GOVERNANCA: read-only (le ledger + run_state). Sem rede, sem work-text.

Uso:  python cost_report.py <projeto> [--by-scene] [--json]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def _read_ledger(root: Path) -> list[dict]:
    p = root / "artifacts" / "api_ledger.jsonl"
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def _verified_scenes(root: Path) -> set[str]:
    p = root / "artifacts" / "run_state.json"
    if not p.is_file():
        return set()
    scenes = json.loads(p.read_text(encoding="utf-8")).get("scenes", {})
    return {s for s, st in scenes.items()
            if st.get("status") == "verified" and st.get("verified") is True}


def report(root, chapter=None) -> dict:
    """Agrega o ledger. `chapter` (ex.: "15") filtra so as cenas `ch_15_*` -> mostra o DELTA do capitulo
    em vez do acumulado de todo o ledger (que confunde: o total cresce a cada capitulo)."""
    root = Path(root)
    rows = _read_ledger(root)
    if chapter is not None:
        pref = f"ch_{chapter}_"
        rows = [r for r in rows if str(r.get("scene", "")).startswith(pref)]
    verified = _verified_scenes(root)
    total = round(sum(r.get("cost_usd", 0.0) for r in rows), 4)
    n_calls = len(rows)

    by_model, by_kind, by_scene = {}, {}, {}
    tok_in = tok_out = tok_cache_r = tok_cache_w = 0
    for r in rows:
        c = r.get("cost_usd", 0.0)
        by_model[r.get("model", "?")] = round(by_model.get(r.get("model", "?"), 0.0) + c, 5)
        by_kind[r.get("kind", "?")] = round(by_kind.get(r.get("kind", "?"), 0.0) + c, 5)
        sc = r.get("scene", "?")
        d = by_scene.setdefault(sc, {"cost_usd": 0.0, "calls": 0})
        d["cost_usd"] = round(d["cost_usd"] + c, 5)
        d["calls"] += 1
        u = r.get("usage", {}) or {}
        tok_in += u.get("in", 0); tok_out += u.get("out", 0)
        tok_cache_r += u.get("cache_read", 0); tok_cache_w += u.get("cache_write", 0)

    # gasto DESPERDICADO: chamadas em cenas que NAO terminaram verified (falha/retry abandonado).
    # uma cena com >1 chamada que terminou verified NAO e desperdicio (retries que convergiram);
    # so conta como desperdicio o gasto de cenas cujo estado final nao e verified.
    wasted = round(sum(d["cost_usd"] for s, d in by_scene.items() if s not in verified), 4)

    return {
        "total_usd": total, "n_calls": n_calls,
        "wasted_usd": wasted,                       # gasto em cenas que nao fecharam (verde = baixo)
        "by_model": dict(sorted(by_model.items(), key=lambda x: -x[1])),
        "by_kind": dict(sorted(by_kind.items(), key=lambda x: -x[1])),
        "by_scene": dict(sorted(by_scene.items())),
        "tokens": {"in": tok_in, "out": tok_out, "cache_read": tok_cache_r, "cache_write": tok_cache_w},
        "verified_scenes": len(verified),
        "chapter": chapter,
    }


def _fmt(rep: dict, by_scene: bool) -> str:
    L = []
    if rep.get("chapter") is not None:
        L.append(f"GASTO DO CAPITULO {rep['chapter']} (delta — so cenas ch_{rep['chapter']}_*) "
                 f"— {rep['n_calls']} chamada(s)")
    else:
        L.append(f"GASTO REAL DE API (api_ledger.jsonl, ACUMULADO) — {rep['n_calls']} chamada(s)")
    L.append(f"  total       : ${rep['total_usd']:.4f}")
    w = rep["wasted_usd"]
    tag = "ok" if w == 0 else ("baixo" if rep["total_usd"] and w / rep["total_usd"] < 0.15 else "ALTO")
    L.append(f"  desperdicado: ${w:.4f}  (cenas que nao fecharam verified) [{tag}]")
    t = rep["tokens"]
    L.append(f"  tokens      : in={t['in']:,} out={t['out']:,} "
             f"cache_read={t['cache_read']:,} cache_write={t['cache_write']:,}")
    cr, cw = t["cache_read"], t["cache_write"]
    if cr or cw:
        hit = cr / (cr + cw) if (cr + cw) else 0.0
        # cache LIDO (0.1x) vs ESCRITO (1.25x): alto = Carta reaproveitada entre cenas; baixo = re-escrita
        # a cada cena (o gap "cache morto" — cenas espacadas > TTL de 5min, ou 1a cena de cada run).
        ct = "bom" if hit >= 0.6 else ("baixo" if hit >= 0.2 else "MORTO (re-escreve a cada cena)")
        L.append(f"  cache       : {100*hit:.0f}% lido (read/{cr+cw:,}) [{ct}]")
    L.append("  por modelo  : " + ", ".join(f"{k} ${v:.4f}" for k, v in rep["by_model"].items()))
    L.append("  por tipo    : " + ", ".join(f"{k} ${v:.4f}" for k, v in rep["by_kind"].items()))
    if by_scene:
        L.append("  por cena:")
        for s, d in rep["by_scene"].items():
            L.append(f"    {s:14s} ${d['cost_usd']:.4f}  ({d['calls']} chamada(s))")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Contabilidade real de gasto de API (ledger).")
    ap.add_argument("project")
    ap.add_argument("--chapter", help='delta de UM capitulo (ex.: "15" -> so cenas ch_15_*)')
    ap.add_argument("--by-scene", action="store_true", help="detalha custo por cena")
    ap.add_argument("--json", action="store_true", help="saida JSON crua")
    a = ap.parse_args()
    rep = report(a.project, chapter=a.chapter)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(_fmt(rep, a.by_scene))
    sys.exit(0)


if __name__ == "__main__":
    main()
