#!/usr/bin/env python3
"""scene_scope.py — o que o dialogs.csv traz, por categoria, para decidir o escopo (`dialogo` x `completo`).

Separa as "unidades" do projeto (a coluna `scene` dos `artifacts/scenes/*/dialogs.csv`) em:
  - sequencia: cena da historia (id com a forma dos ids da historia), na ordem do jogo (`artifacts/ordem_cenas.txt`, gerado pelo conector a partir dos
    dados do jogo; sem o arquivo, a forma do id decide e a ordem NAO e confirmada);
  - tabela: texto de sistema (nome, unidade, mensagem, menu), sem lugar na ordem da historia.
Por categoria: unidades, strings, quantas trazem `byte_budget` e a faixa dele. Tabela com orcamento curto e
rotulo de interface/nome (largura e bytes limitados), ponto de um piloto cedo.

Uso: python scene_scope.py <pasta_do_projeto>
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

_ROTULO_BYTES = 16        # orcamento ate aqui = rotulo/nome curto


def _shape(sid: str) -> str:
    return re.sub(r"[A-Za-z]+", "a", re.sub(r"\d+", "0", sid))


def ordem(art: Path) -> list[str]:
    f = art / "ordem_cenas.txt"
    return f.read_text(encoding="utf-8").split() if f.is_file() else []


def classify(units: list[str], ordem_l: list[str]) -> dict[str, str]:
    """{unidade: 'sequencia' | 'tabela'}. Sequencia = id com a forma dos ids da historia (NN_NN_NN): os da
    `ordem_cenas.txt` quando existe, senao a forma mais comum. Cena fora da lista do jogo mas com essa forma
    continua sequencia (so a ordem dela e inferida); nome de tabela (NameTextData...) nao tem essa forma."""
    formas = Counter(_shape(o) for o in ordem_l) or Counter(_shape(u) for u in units)
    forma = formas.most_common(1)[0][0] if formas else ""
    return {u: "sequencia" if u in ordem_l or _shape(u) == forma else "tabela" for u in units}


def scan(project: Path) -> dict:
    art = Path(project) / "artifacts"
    rows: dict[str, list[int | None]] = {}
    for d in sorted((art / "scenes").iterdir()) if (art / "scenes").is_dir() else []:
        f = d / "dialogs.csv"
        if f.is_file():
            with f.open(encoding="utf-8-sig", newline="") as fh:
                rows[d.name] = [int(r["byte_budget"]) if (r.get("byte_budget") or "").isdigit() else None
                                for r in csv.DictReader(fh)]
    ordem_l = ordem(art)
    kind = classify(list(rows), ordem_l)
    cats: dict[str, dict] = {}
    for u, budgets in rows.items():
        c = cats.setdefault(u if kind[u] == "tabela" else "(sequencia)",
                            {"kind": kind[u], "units": 0, "strings": 0, "budgets": []})
        c["units"] += 1
        c["strings"] += len(budgets)
        c["budgets"] += [b for b in budgets if b is not None]
    return {"ordem_confirmada": bool(ordem_l), "cats": cats}


def report(res: dict) -> str:
    out = ["ORDEM: " + ("confirmada (ordem_cenas.txt)" if res["ordem_confirmada"]
                        else "NAO confirmada (sem ordem_cenas.txt: o conector deve gera-lo a partir dos dados do jogo)"),
           f"{'categoria':24} {'tipo':10} {'unid':>5} {'strings':>8} {'c/ orcamento':>12} {'bytes min-max':>14} {'<=%d B' % _ROTULO_BYTES:>7}"]
    for name, c in sorted(res["cats"].items(), key=lambda kv: (kv[1]["kind"] != "sequencia", kv[0])):
        b = c["budgets"]
        faixa = f"{min(b)}-{max(b)}" if b else "-"
        out.append(f"{name:24} {c['kind']:10} {c['units']:>5} {c['strings']:>8} {len(b):>12} {faixa:>14} "
                   f"{sum(1 for x in b if x <= _ROTULO_BYTES):>7}")
    tab = [n for n, c in res["cats"].items() if c["kind"] == "tabela"]
    if tab:
        out.append("\nTABELAS DE SISTEMA: " + ", ".join(tab) + ". Orcamento de bytes curto = rotulo/nome com limite de"
                   " largura; vale um piloto cedo delas, antes das ultimas ondas da historia.")
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(report(scan(Path(sys.argv[1]))))


if __name__ == "__main__":
    main()
