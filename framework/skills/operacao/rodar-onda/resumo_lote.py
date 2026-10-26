"""Resumo de um lote de ondas: python resumo_lote.py <projeto> <t0_epoch> <lote> <log> [<log> ...]
Le api_ledger.jsonl e run_state.json do projeto; imprime e grava logs/resumo_lote_<lote>.md. Unico efeito alem do
resumo: alerta (alerts.jsonl/webhook) as cenas que o lote deixou paradas por defeito da traducao sem correcao."""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "framework" / "runtime"))
import alerts  # noqa: E402

MAX_REQ_FALA = float(os.environ.get("MAX_REQ_FALA", "0.5"))   # acima disso o lote custou mais idas e voltas por fala que o esperado
proj, t0, lote, logs = Path(sys.argv[1]), float(sys.argv[2]), sys.argv[3], [Path(p) for p in sys.argv[4:]]
art = proj / "artifacts"
led = [json.loads(x) for x in (art / "api_ledger.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
# Sessao que ja gastava antes do disparo (a que lancou o lote) nao e custo do lote: so entram as sessoes `claude -p` das ondas.
antigas = {r.get("session") for r in led if r.get("t", 0) < t0 and r.get("session")}
fora = [r for r in led if r.get("t", 0) >= t0 and r.get("session") in antigas]
led = [r for r in led if r.get("t", 0) >= t0 and r.get("session") not in antigas]
tot = sum((r.get("api_equiv_usd") or 0) for r in led)
ovh = sum((r.get("api_equiv_usd") or 0) for r in led if r.get("attribution") == "overhead")
req = sum(r.get("n_requests", 0) for r in led)
por_tipo: dict = {}   # subagente por tipo (traducao x retraducao/verificacao): custo de trabalho, nao de orquestracao
for r in led:
    if r.get("agent_type"):
        por_tipo[r["agent_type"]] = por_tipo.get(r["agent_type"], 0) + (r.get("api_equiv_usd") or 0)
sc = json.loads((art / "run_state.json").read_text(encoding="utf-8"))["scenes"]
new = {k: v for k, v in sc.items() if v.get("verified") and v.get("_ts", 0) >= t0}
falas = sum(v.get("n_lines", 0) for v in new.values())
vc_p = art / "state" / "voice_cards.json"
cards = set(json.loads(vc_p.read_text(encoding="utf-8"))) if vc_p.is_file() else set()
spk: dict = {}
for k in new:   # falante com nome, sem voice card, com >=5 falas na onda (a voz dele esta sendo inventada por cena)
    tp = art / "scenes" / k / f"translations_{k}.json"
    for v in (json.loads(tp.read_text(encoding="utf-8")).get("lines", {}).values() if tp.is_file() else ()):
        s = v.get("speaker", "")
        if s and s not in cards and s not in ("npc", "system", "unknown"):
            spk[s] = spk.get(s, 0) + 1
no_card = {s: n for s, n in spk.items() if n >= 5}
por_onda: dict = {}   # uma sessao `claude -p` = uma onda: janela (sem agent_type) x tradutor x retraducao/5d, para comparar bracos A x B
for r in led:
    o = por_onda.setdefault(r.get("session") or "?", {"cenas": set(), "janela": 0.0, "trad": 0.0, "outros": 0.0, "w_cw": 0, "t1_cw": 0, "w_out": 0, "w_req": 0})
    usd, u = (r.get("api_equiv_usd") or 0), (r.get("usage") or {})
    if r.get("scene") in new:
        o["cenas"].add(r["scene"])
    if not r.get("agent_type"):
        o["janela"] += usd; o["w_cw"] += u.get("cache_write", 0) + u.get("cache_write_1h", 0)
        if r.get("attribution") == "window":
            o["t1_cw"] += u.get("cache_write", 0) + u.get("cache_write_1h", 0)   # 1o turno da janela: alvo de -PrefixoEstavel
        o["w_out"] += u.get("out", 0); o["w_req"] += r.get("n_requests", 0)
    elif r["agent_type"] == "scene-translator":
        o["trad"] += usd
    else:
        o["outros"] += usd
linhas_onda = ["| onda (sessao) | falas | US$/fala | janela US$ | 1º turno cache escrito (tok) | janela cache escrito (tok) | janela saida (tok) | tradutor US$ | 5c/5d etc. US$ |", "|---|---|---|---|---|---|---|---|---|"]
for sid, o in sorted(por_onda.items()):
    f = sum(new[c].get("n_lines", 0) for c in o["cenas"])
    tt = o["janela"] + o["trad"] + o["outros"]
    linhas_onda.append(f"| {sid} | {f} | {tt / f:.4f} | {o['janela']:.2f} | {o['t1_cw']} | {o['w_cw']} | {o['w_out']} | {o['trad']:.2f} | {o['outros']:.2f} |" if f
                       else f"| {sid} | 0 | - | {o['janela']:.2f} | {o['t1_cw']} | {o['w_cw']} | {o['w_out']} | {o['trad']:.2f} | {o['outros']:.2f} |")
pend = alerts.alertar_correcoes_pendentes(proj)   # o wave nao alerta esta parada na hora; o que sobrou ao fim do lote, sim
rows = ["| log | fim |", "|---|---|"]
for lg in logs:
    last = [x for x in lg.read_text(encoding="utf-8-sig", errors="replace").splitlines() if x.strip()]
    rows.append(f"| {lg.name} | {re.sub(r'[|]', '/', last[-1])[:110] if last else '(vazio)'} |")
out = [f"# Resumo do lote {lote}", "",
       f"- Cenas `verified` no lote: {len(new)} | falas: {falas}",
       f"- Custo equivalente API: ${tot:.2f} em {req} req | overhead: {100 * ovh / tot:.0f}%" if tot else "- Sem custo no ledger",
       ("- Subagentes por tipo: " + ", ".join(f"{k} ${v:.2f}" for k, v in sorted(por_tipo.items(), key=lambda x: -x[1]))) if por_tipo else "",
       f"- Fora da conta (sessao que disparou o lote): ${sum((r.get('api_equiv_usd') or 0) for r in fora):.2f} em {sum(r.get('n_requests', 0) for r in fora)} req" if fora else "",
       f"- Cenas fechadas por fala: ${tot / falas:.4f}/fala" if falas else "",
       f"- AVISO: {req / falas:.2f} requisicoes por fala, acima do limite de {MAX_REQ_FALA} (variavel MAX_REQ_FALA): conferir falhas e retrabalho do lote" if falas and req / falas > MAX_REQ_FALA else "",
       f"- PENDENTE DE CORRECAO DA TRADUCAO (alertado): {', '.join(pend)}" if pend else "",
       ("- Falantes com nome, sem voice card, >=5 falas na onda: " + ", ".join(f"{s} ({n})" for s, n in sorted(no_card.items(), key=lambda x: -x[1])))
       if no_card else "", "", *linhas_onda, "", *rows]
txt = "\n".join(out)
print(txt)
(logs[0].parent / f"resumo_lote_{lote}.md").write_text(txt, encoding="utf-8") if logs else None
