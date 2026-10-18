"""Gaps de custo e performance.
Uso: python gaps.py projects/<nome> [--sessao <prefixo do id>...] [--cenas <cena>...]
  (le artifacts/: api_ledger, events, metrics, run_state). --sessao recorta o ledger por sessao (overhead de uma onda);
  --cenas recorta ledger, eventos e metricas por cena. Sem filtro: acumulado do projeto."""
import argparse
import collections
import json
import statistics as st
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("project"); ap.add_argument("--sessao", nargs="+", default=[]); ap.add_argument("--cenas", nargs="+", default=[])
args = ap.parse_args()
art = Path(args.project) / "artifacts"
jl = lambda n: [json.loads(l) for l in (art / n).read_text(encoding="utf-8").splitlines() if l.strip()]
led, ev, met = jl("api_ledger.jsonl"), jl("events.jsonl"), jl("metrics.jsonl")
if args.sessao:
    led = [r for r in led if any(str(r.get("session") or "").startswith(x) for x in args.sessao)]
if args.cenas:
    led = [r for r in led if r.get("scene") in args.cenas]   # overhead (_session) nao tem cena: use --sessao
    ev = [e for e in ev if e.get("scene") in args.cenas]
    met = [m for m in met if m.get("scene") in args.cenas]
if args.sessao or args.cenas:
    print(f"(recorte: sessao={args.sessao or 'todas'} cenas={args.cenas or 'todas'}; a atribuicao por cena do ledger e aproximada; overhead so aparece com --sessao)")
U = lambda r, k: (r.get("usage") or {}).get(k, 0)
usd = lambda rs: sum(r.get("api_equiv_usd") or 0 for r in rs)
tot = usd(led) or 1e-9

print("== 1. ONDE VAI O DINHEIRO (equivalente API)")
for k in ("agent", "window", "overhead"):
    rs = [r for r in led if r.get("attribution") == k]
    print(f"  {k:9} ${usd(rs):7.2f} ({100*usd(rs)/tot:4.1f}%)  {sum(r.get('n_requests',0) for r in rs):5} req")
oh = collections.defaultdict(float)
for r in led:
    if r.get("attribution") == "overhead": oh[r.get("activity")] += r.get("api_equiv_usd") or 0
print("  overhead por atividade:", {k: round(v, 2) for k, v in sorted(oh.items(), key=lambda x: -x[1])})

print("== 1b. POR MODELO E POR FASE (atribuicao por janela de tempo)")
for label, key in (("modelo", lambda r: r.get("model") or "?"), ("fase", lambda r: r.get("phase") or "?")):
    g = collections.defaultdict(list)
    for r in led: g[key(r)].append(r)
    for k, rs in sorted(g.items(), key=lambda x: -usd(x[1])):
        print(f"  {label} {k:20} ${usd(rs):7.2f} ({100*usd(rs)/tot:4.1f}%)  {sum(r.get('n_requests',0) for r in rs):5} req  saida {sum(U(r,'out') for r in rs):,} tok")
if not any(r.get("phase") == "back" for r in led):
    print("  retrotraducao (phase=back): $0.00, 0 req (nenhuma rodada ainda; o custo aparece aqui quando houver)")

print("== 2. CACHE E TOKENS")
i, o, cr, cw = (sum(U(r, k) for r in led) for k in ("in", "out", "cache_read", "cache_write"))
cw += sum(U(r, "cache_write_1h") for r in led)
print(f"  cache_read/(entrada total) = {100*cr/max(i+cr+cw,1):.1f}% | saida {o:,} tok | escrita de cache {cw:,} tok")

print("== 3. POR CENA (so cenas verified com custo)")
rows = []
for m in met:
    s = m.get("session") or {}
    if m.get("verified") and s.get("n_requests") and m["n_lines"]:
        rows.append((m["scene"], m["n_lines"], s["n_requests"], s["usage"]["out"], s["api_equiv_usd"]))
for sc, n, rq, out, c in sorted(rows, key=lambda r: -r[4] / r[1])[:5]:
    print(f"  {sc}: {n} falas, {rq} req, {out} tok saida, ${c:.3f} = ${c/n:.4f}/fala")
if rows:
    pf = [c / n for _, n, _, _, c in rows]; med = st.median(pf)
    print(f"  mediana ${med:.4f}/fala | req/fala {sum(r[2] for r in rows)/sum(r[1] for r in rows):.3f} | saida tok/fala {sum(r[3] for r in rows)/sum(r[1] for r in rows):.0f}")
    print("  outliers (>2x mediana):", [r[0] for r in rows if r[4] / r[1] > 2 * med] or "nenhum")

print("== 4. RETRABALHO (eventos)")
c = collections.Counter((e["stage"], e.get("result")) for e in ev)
ver = c[("scene", "verified")] or 1
bf, vf, ae = c[("build_plan", "fail")], c[("verify", "fail")], c[("translate", "error")]
print(f"  build_plan fail {bf} | verify fail {vf} | erro de traducao {ae} | por cena verified: {(bf+vf)/ver:.2f} falhas")
print(f"  gate.connector block {c[('gate.connector','block')]}x (suspeito: registro, nao bloqueio real)")

codes = collections.Counter(e.get("code") or "sem-codigo" for e in ev if e.get("result") in ("fail", "error", "invalid_output"))
if codes:
    print("  por causa (campo code dos eventos):", dict(codes.most_common()))
by_scene = collections.Counter(e["scene"] for e in ev if e.get("result") in ("fail", "error") and e.get("scene"))
if by_scene:
    print("  falhas por cena:", dict(by_scene.most_common(8)))

print("== 4b. CACHE POR REQUISICAO (janela principal e agentes)")
for k in ("window", "agent"):
    rs = [r for r in led if r.get("attribution") == k and r.get("n_requests")]
    n = sum(r["n_requests"] for r in rs)
    if n:
        print(f"  {k:7} {n:5} req | leitura de cache {sum(U(r, 'cache_read') for r in rs) / n:,.0f} tok/req | escrita {sum(U(r, 'cache_write') + U(r, 'cache_write_1h') for r in rs) / n:,.0f} tok/req")

print("== 5. PROJECAO")
state = json.loads((art / "run_state.json").read_text(encoding="utf-8")).get("scenes", {})
falas = sum(len(list(__import__('csv').DictReader((d / "dialogs.csv").open(encoding="utf-8-sig")))) for d in (art / "scenes").iterdir() if (d / "dialogs.csv").is_file())
feitas = sum(v["n_lines"] for v in state.values() if v.get("verified"))
if rows and not (args.sessao or args.cenas):
    pf_all = sum(r[4] for r in rows) / sum(r[1] for r in rows)
    print(f"  ${pf_all:.4f}/fala medio -> {falas-feitas} falas restantes = ${pf_all*(falas-feitas):.0f} (so traducao; overhead de conversa/framework nao entra)")
