"""Tabela A x B do benchmark intercalado: python ab_resumo.py
Le logs/ab_plano.jsonl (lote -> braco) e a tabela por onda de logs/resumo_lote_<n>.md (gerada pelo resumo_lote.py);
imprime uma linha por onda e a media/dispersao por braco das metricas por fala."""
import json
import re
import statistics
from pathlib import Path

logs = Path(__file__).resolve().parent / "logs"
plano = [json.loads(x) for x in (logs / "ab_plano.jsonl").read_text(encoding="utf-8-sig").splitlines() if x.strip()]
por_braco: dict = {"A": [], "B": []}
print("| lote | braco | falas | US$/fala | janela US$/fala | 1o turno cache (tok) | janela saida (tok)/fala | tradutor US$/fala | 5c/5d US$/fala |")
print("|---|---|---|---|---|---|---|---|---|")
for p in plano:
    f = logs / f"resumo_lote_{p['lote']}.md"
    if not f.is_file():
        continue
    for ln in f.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in ln.strip("|").split("|")]
        if len(c) == 9 and re.fullmatch(r"[0-9a-f]{8}", c[0]) and c[1] != "0":
            fal = int(c[1])
            r = {"falas": fal, "usd": float(c[2]), "jan": float(c[3]) / fal, "t1": int(c[4]), "out": int(c[6]) / fal,
                 "trad": float(c[7]) / fal, "outros": float(c[8]) / fal}
            por_braco[p["braco"]].append(r)
            print(f"| {p['lote']} | {p['braco']} | {fal} | {r['usd']:.4f} | {r['jan']:.4f} | {r['t1']} | {r['out']:.0f} | {r['trad']:.4f} | {r['outros']:.4f} |")
print()
for b, rs in por_braco.items():
    if not rs:
        continue
    for k, nome in (("usd", "US$/fala"), ("jan", "janela US$/fala"), ("t1", "1o turno cache"), ("out", "saida janela/fala"), ("outros", "5c/5d US$/fala")):
        v = [r[k] for r in rs]
        print(f"braco {b} (n={len(rs)}): {nome} media {statistics.mean(v):.4f} dp {statistics.pstdev(v):.4f}")
