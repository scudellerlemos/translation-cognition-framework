#!/usr/bin/env python3
"""
build_plan_chapter.py — monta translation_plan + approved de UM capitulo isolado (meia-maratona).

Generico (reusavel por capitulo). GOVERNANCA: NAO contem work-text. Le os dados de:
  - artifacts/<chapter_dir>/dialogs.csv             (source + byte_budget, do extract)
  - artifacts/<chapter_dir>/translations_*.json     (traducoes curadas pela IA; chave 'lines')
e emite:
  - artifacts/<chapter_dir>/translation_plan_<sfx>.json
  - artifacts/<chapter_dir>/approved_<sfx>.csv      (offset,text_target)
onde <sfx> = sufixo do translations_<sfx>.json.

Valida invariantes baratos: cobertura total, token \\n preservado por linha, interjeicao != source,
risk>=medium exige risk_notes. Falha ruidosamente.

Uso: python build_plan_chapter.py <chapter_dir>     ex.: python build_plan_chapter.py ch_11_04
Determinista. Sem rede. Sem escrita no binario.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = chr(92) + "n"
INTERJ_PREFIX = ("interjeicao_",)   # interjeicao localizavel: nao pode ser identica ao source


def load_dialogs(p):
    rows, order = {}, []
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["offset"]] = {"text_source": r["text_source"], "byte_budget": int(r["byte_budget"])}
            order.append(r["offset"])
    return rows, order


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python build_plan_chapter.py <chapter_dir>  (ex.: ch_11_04)")
    chdir = ROOT / "artifacts" / sys.argv[1]
    if not chdir.is_dir():
        sys.exit(f"ERRO: diretorio nao encontrado: {chdir}")
    trans_files = sorted(chdir.glob("translations_*.json"))
    if len(trans_files) != 1:
        sys.exit(f"ERRO: esperado exatamente 1 translations_*.json em {chdir}, achei {len(trans_files)}")
    sfx = trans_files[0].stem.replace("translations_", "")

    dialogs, order = load_dialogs(chdir / "dialogs.csv")
    trans = json.loads(trans_files[0].read_text(encoding="utf-8"))["lines"]

    errors = []
    miss = [o for o in order if o not in trans]
    extra = [o for o in trans if o not in dialogs]
    if miss:
        errors.append(f"{len(miss)} offsets sem traducao: {miss[:5]}")
    if extra:
        errors.append(f"{len(extra)} offsets na traducao inexistentes no source: {extra[:5]}")

    plan_lines, approved = [], []
    for off in order:
        if off not in trans:
            continue
        src = dialogs[off]["text_source"]
        budget = dialogs[off]["byte_budget"]
        t = trans[off]
        tgt = t["t"]
        if (TOKEN in src) != (TOKEN in tgt):
            errors.append(f"{off}: token \\n divergente (src={TOKEN in src} tgt={TOKEN in tgt})")
        tr = t.get("tone_register", "")
        if tr.startswith(INTERJ_PREFIX) and tgt.strip() == src.strip():
            errors.append(f"{off}: interjeicao identica ao source ('{src}') - localizar")
        line = {
            "offset": off, "text_source": src,
            "speaker": t.get("speaker", ""),
            "entities_present": [t["speaker"]] if t.get("speaker") not in ("", "rotulo") else [],
            "tone_register": tr, "intent": t.get("intent", ""),
            "risk_level": t.get("risk_level", "low"),
            "base_translation": tgt, "byte_budget": budget,
            "glossary_flags": t.get("glossary_flags", []),
            "spoiler_flags": t.get("spoiler_flags", []),
        }
        if "risk_notes" in t:
            line["risk_notes"] = t["risk_notes"]
        if t.get("needs_review"):
            line["needs_human_review"] = True
        plan_lines.append(line)
        approved.append((off, tgt))

    for ln in plan_lines:
        if ln["risk_level"] in ("medium", "high", "critical") and "risk_notes" not in ln:
            errors.append(f"{ln['offset']}: risk={ln['risk_level']} sem risk_notes")

    if errors:
        print("ERROS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    plan = {
        "scene_group": sfx,
        "lines": plan_lines, "total_lines": len(plan_lines),
        "high_lines": sum(1 for l in plan_lines if l["risk_level"] in ("high", "critical")),
        "medium_lines": sum(1 for l in plan_lines if l["risk_level"] == "medium"),
        "needs_review": [l["offset"] for l in plan_lines if l.get("needs_human_review")],
        "plan_version": f"chapter-{sfx}-v1",
    }
    (chdir / f"translation_plan_{sfx}.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    with (chdir / f"approved_{sfx}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerows(approved)

    print(f"OK: {len(plan_lines)} linhas -> translation_plan_{sfx}.json + approved_{sfx}.csv")
    print(f"  risco: {plan['high_lines']} high, {plan['medium_lines']} medium, "
          f"{len(plan_lines)-plan['high_lines']-plan['medium_lines']} low")
    print(f"  needs_human_review: {plan['needs_review'] or 'nenhum'}")


if __name__ == "__main__":
    main()
