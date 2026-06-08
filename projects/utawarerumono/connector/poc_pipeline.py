#!/usr/bin/env python3
"""
poc_pipeline.py — Passos 05 (planejamento) + 06 (tradução), no arco extraído (dialogs.csv).

DETERMINÍSTICO. Não contém nenhuma frase da obra:
- A PROPOSTA de tradução é um artefato de DADOS autorado na etapa cognitiva:
  artifacts/translation_plan.json (campo `base_translation` por offset).
- Este script LÊ essa proposta + dialogs.csv (source/byte_budget), valida tokens e
  byte_budget, e EMITE artifacts/approved_translations.csv (offset, text_target) + relatório de fit.

No fluxo real há um gate de aprovação humana entre a proposta (translation_plan.json) e o
arquivo aprovado (approved_translations.csv). Na POC, a aprovação é o snapshot do plano.
"""
import csv
import json
from pathlib import Path

ART = Path(__file__).resolve().parent.parent / "artifacts"
TOKENS = ["{W75}", "{W80}", "{W10}", "{COLOR}", "{END}"]


def tok_counts(s: str):
    return {t: s.count(t) for t in TOKENS}, s.count("\\n")


def main():
    # source (offset -> byte_budget, text_source)
    src = {r["offset"]: (r["text_source"], int(r["byte_budget"]))
           for r in csv.DictReader((ART / "dialogs.csv").open(encoding="utf-8"))}

    # PROPOSTA (dado cognitivo, não código): translation_plan.json
    plan = json.loads((ART / "translation_plan.json").read_text(encoding="utf-8"))

    out_rows, report = [], []
    fit_ok = 0
    for line in plan["lines"]:
        off = line["offset"]
        tgt = line["base_translation"]
        source_text, budget = src[off]
        tgt_bytes = len(tgt.encode("utf-8"))
        fits = tgt_bytes <= budget
        if fits:
            fit_ok += 1
        # verificação de tokens (determinística): proposta preserva os tokens do source?
        st, snl = tok_counts(source_text)
        tt, tnl = tok_counts(tgt)
        tokens_ok = (st == tt) and (snl == tnl)
        # APROVADO -> approved_translations.csv (id, text_target)
        out_rows.append({"offset": off, "text_target": tgt})
        report.append((off, budget, tgt_bytes, fits, tokens_ok))

    # escreve approved_translations.csv (APROVADO — snapshot da POC)
    with (ART / "approved_translations.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["offset", "text_target"])
        w.writeheader()
        w.writerows(out_rows)

    # relatório
    print("=== FIT DE BYTE-BUDGET (reinserção in_place) ===")
    print(f"{'offset':>8} {'orç':>4} {'pt':>4} {'fit':>4} {'tok':>4}")
    for off, b, tb, fits, tok in report:
        print(f"{off:>8} {b:>4} {tb:>4} {('OK' if fits else 'XX'):>4} {('ok' if tok else 'ERR'):>4}")
    print(f"\nCabem in_place: {fit_ok}/{len(report)}  ({100 * fit_ok // len(report)}%)")
    print(f"Estouram in_place: {len(report) - fit_ok}/{len(report)} -> exigiriam repoint ou abreviação")
    print(f"approved_translations.csv -> {ART / 'approved_translations.csv'}")


if __name__ == "__main__":
    main()
