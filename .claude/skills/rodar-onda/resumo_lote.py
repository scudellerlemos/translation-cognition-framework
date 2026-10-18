"""Resumo de um lote de ondas: python resumo_lote.py <projeto> <t0_epoch> <lote> <log> [<log> ...]
Le api_ledger.jsonl e run_state.json do projeto; imprime e grava logs/resumo_lote_<lote>.md. So le, nao altera nada."""
import json
import re
import sys
from pathlib import Path

proj, t0, lote, logs = Path(sys.argv[1]), float(sys.argv[2]), sys.argv[3], [Path(p) for p in sys.argv[4:]]
art = proj / "artifacts"
led = [json.loads(x) for x in (art / "api_ledger.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
led = [r for r in led if r.get("t", 0) >= t0]
tot = sum((r.get("api_equiv_usd") or 0) for r in led)
ovh = sum((r.get("api_equiv_usd") or 0) for r in led if r.get("attribution") == "overhead")
req = sum(r.get("n_requests", 0) for r in led)
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
rows = ["| log | fim |", "|---|---|"]
for lg in logs:
    last = [x for x in lg.read_text(encoding="utf-8-sig", errors="replace").splitlines() if x.strip()]
    rows.append(f"| {lg.name} | {re.sub(r'[|]', '/', last[-1])[:110] if last else '(vazio)'} |")
out = [f"# Resumo do lote {lote}", "",
       f"- Cenas `verified` no lote: {len(new)} | falas: {falas}",
       f"- Custo equivalente API: ${tot:.2f} em {req} req | overhead: {100 * ovh / tot:.0f}%" if tot else "- Sem custo no ledger",
       f"- Cenas fechadas por fala: ${tot / falas:.4f}/fala" if falas else "",
       ("- Falantes com nome, sem voice card, >=5 falas na onda: " + ", ".join(f"{s} ({n})" for s, n in sorted(no_card.items(), key=lambda x: -x[1])))
       if no_card else "", "", *rows]
txt = "\n".join(out)
print(txt)
(logs[0].parent / f"resumo_lote_{lote}.md").write_text(txt, encoding="utf-8") if logs else None
