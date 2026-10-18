"""Panorama de falas e plano de ondas. Uso: python panorama.py projects/<nome> [n_ondas=8, 0=todas]
Ordem das cenas: artifacts/ordem_cenas.txt (um id de cena por linha, gerado por extrai_ordem.py a partir do jogo); sem ele, ordem numerica (NAO confirmada)."""
import contextlib
import csv
import io
import json
import sys
from collections import OrderedDict
from pathlib import Path

proj = Path(sys.argv[1]); n_plan = int(sys.argv[2]) if len(sys.argv) > 2 else 8
art = proj / "artifacts"
buf = io.StringIO(); _out = contextlib.redirect_stdout(buf); _out.__enter__()
sizes = {d.name: sum(1 for _ in csv.DictReader((d / "dialogs.csv").open(encoding="utf-8-sig")))
         for d in sorted((art / "scenes").iterdir()) if (d / "dialogs.csv").is_file()}
st = json.loads((art / "run_state.json").read_text(encoding="utf-8")).get("scenes", {})
done = {s for s, v in st.items() if v.get("status") == "verified" and v.get("verified") is True}
ordem = art / "ordem_cenas.txt"
ordem_l = ordem.read_text().split() if ordem.is_file() else []
def key(s):  # cena fora da lista do jogo entra logo depois da ultima cena listada do mesmo NN_NN (depois do mesmo NN)
    if s in ordem_l: return (ordem_l.index(s), s)
    for n in (5, 2):
        pos = [k for k, o in enumerate(ordem_l) if o[:n] == s[:n]]
        if pos: return (pos[-1] + .5, s)
    return (len(ordem_l) + 1, s)
prefs = ordem_l
cenas = sorted(sizes, key=key)

tot, ok = sum(sizes.values()), sum(sizes[s] for s in done if s in sizes)
print(f"FALAS: {ok} de {tot} ({100*ok/tot:.1f}%) | CENAS: {len(done & set(sizes))} de {len(sizes)} verified")
print("ORDEM:", "confirmada pelos dados do jogo (EventManagerData, ordem_cenas.txt)" if prefs else "NAO CONFIRMADA (prefixo numerico; ver ROADMAP)")
g = OrderedDict()
for s in cenas:
    a = g.setdefault(s[:2], [0, 0, 0, 0]); a[0] += 1; a[1] += sizes[s]
    if s in done: a[2] += 1; a[3] += sizes[s]
print("\ngrupo  cenas  falas  feitas(cenas/falas)")
for k, (c, f, dc, df) in g.items(): print(f"{k:>5} {c:>6} {f:>6}  {dc}/{c}  {df}/{f}")

todo = [s for s in cenas if s not in done]; ondas = []; cur = []
for s in todo:
    n = sum(sizes[x] for x in cur)
    if cur and (len(cur) == 6 or n + sizes[s] > 700): ondas.append(cur); cur = []
    cur.append(s)
if cur: ondas.append(cur)
print(f"\nPLANO: {len(ondas)} ondas restantes (até 6 cenas, ~400-700 falas; cena maior que 700 vai sozinha)")
for i, o in enumerate(ondas, 1):
    print(f" onda +{i}: {' '.join(o)} = {sum(sizes[x] for x in o)} falas")
_out.__exit__(None, None, None)
txt = buf.getvalue()
lim = n_plan or 10**6
print(chr(10).join(l for l in txt.split(chr(10)) if not l.startswith(" onda +") or int(l.split("+")[1].split(":")[0]) <= lim))
(art / "panorama_ondas.md").write_text(f"```{chr(10)}{txt}```{chr(10)}", encoding="utf-8")
print("gravado em", art / "panorama_ondas.md")
