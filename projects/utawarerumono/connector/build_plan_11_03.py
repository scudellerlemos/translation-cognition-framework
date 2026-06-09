#!/usr/bin/env python3
"""
build_plan_11_03.py — monta o translation_plan + approved do cap. 11_03 (calibracao).

GOVERNANCA: NAO contem work-text (nenhuma traducao/fala hardcoded). Le os dados de:
  - artifacts/ch_11_03/dialogs.csv             (source + byte_budget, do extract)
  - artifacts/ch_11_03/translations_11_03.json (traducoes curadas pela IA)
e emite:
  - artifacts/ch_11_03/translation_plan_11_03.json  (schema do translation_plan)
  - artifacts/ch_11_03/approved_11_03.csv           (offset,text_target)

Tambem valida invariantes baratos (cobertura total, token \\n preservado por linha,
interjeicao != source). Falha ruidosamente se algo nao bate.

Determinista. Sem rede. Sem escrita no binario.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "artifacts" / "ch_11_03"
DIALOGS = CH / "dialogs.csv"
TRANS = CH / "translations_11_03.json"
OUT_PLAN = CH / "translation_plan_11_03.json"
OUT_APPROVED = CH / "approved_11_03.csv"

TOKEN = chr(92) + "n"  # a barra-n literal (token de quebra do motor), sem ambiguidade de escape

# tone_registers que sao interjeicao/onomatopeia: a regra "nao copiar do source" se aplica,
# EXCETO grito/rosnado so de vogais/consoantes-animal (universal) e rotulo interno.
INTERJ_PREFIX = ("interjeicao_",)
ANIMAL = ("onomatopeia_animal",)


def load_dialogs():
    rows = {}
    order = []
    with DIALOGS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            off = r["offset"]
            rows[off] = {"text_source": r["text_source"], "byte_budget": int(r["byte_budget"])}
            order.append(off)
    return rows, order


def main():
    dialogs, order = load_dialogs()
    trans = json.loads(TRANS.read_text(encoding="utf-8"))["lines"]

    errors = []
    warns = []

    # cobertura: toda linha do source tem traducao e vice-versa
    miss = [o for o in order if o not in trans]
    extra = [o for o in trans if o not in dialogs]
    if miss:
        errors.append(f"{len(miss)} offsets sem traducao: {miss[:5]}")
    if extra:
        errors.append(f"{len(extra)} offsets na traducao que nao existem no source: {extra[:5]}")

    plan_lines = []
    approved = []
    for off in order:
        if off not in trans:
            continue
        src = dialogs[off]["text_source"]
        budget = dialogs[off]["byte_budget"]
        t = trans[off]
        tgt = t["t"]

        # invariante de token: se o source tem \n, o alvo tambem precisa ter (e vice-versa)
        if (TOKEN in src) != (TOKEN in tgt):
            errors.append(f"{off}: token \\n divergente (src={TOKEN in src} tgt={TOKEN in tgt})")

        # interjeicao localizada: nao deixar identica ao source (exceto animal/rotulo)
        tr = t.get("tone_register", "")
        if tr.startswith(INTERJ_PREFIX) and tgt.strip() == src.strip():
            errors.append(f"{off}: interjeicao identica ao source ('{src}') — localizar")

        line = {
            "offset": off,
            "text_source": src,
            "speaker": t.get("speaker", ""),
            "entities_present": [t.get("speaker", "")] if t.get("speaker") not in ("", "rotulo") else [],
            "tone_register": tr,
            "intent": t.get("intent", ""),
            "risk_level": t.get("risk_level", "low"),
            "base_translation": tgt,
            "byte_budget": budget,
            "glossary_flags": t.get("glossary_flags", []),
            "spoiler_flags": t.get("spoiler_flags", []),
        }
        if "risk_notes" in t:
            line["risk_notes"] = t["risk_notes"]
        if t.get("needs_review"):
            line["needs_human_review"] = True
        plan_lines.append(line)
        approved.append((off, tgt))

    # risco >= medium exige risk_notes (Carta)
    for ln in plan_lines:
        if ln["risk_level"] in ("medium", "high", "critical") and "risk_notes" not in ln:
            errors.append(f"{ln['offset']}: risk={ln['risk_level']} sem risk_notes")

    if errors:
        print("ERROS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    plan = {
        "scene": "11_03_000C.BIN",
        "lines": plan_lines,
        "total_lines": len(plan_lines),
        "high_lines": sum(1 for l in plan_lines if l["risk_level"] in ("high", "critical")),
        "medium_lines": sum(1 for l in plan_lines if l["risk_level"] == "medium"),
        "needs_review": [l["offset"] for l in plan_lines if l.get("needs_human_review")],
        "plan_version": "cal-11_03-v1",
    }
    OUT_PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    with OUT_APPROVED.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerows(approved)

    print(f"OK: {len(plan_lines)} linhas -> {OUT_PLAN.name} + {OUT_APPROVED.name}")
    print(f"  risco: {plan['high_lines']} high, {plan['medium_lines']} medium, "
          f"{len(plan_lines)-plan['high_lines']-plan['medium_lines']} low")
    print(f"  needs_human_review: {plan['needs_review']}")
    if warns:
        print("AVISOS:", *warns, sep="\n  - ")


if __name__ == "__main__":
    main()
