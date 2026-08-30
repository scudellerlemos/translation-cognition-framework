#!/usr/bin/env python3
"""
build_plan_chapter.py — Trails in the Sky 2nd Chapter

Monta translation_plan + approved de UMA cena (1 arquivo scena/*.dat).

GOVERNANÇA: NÃO contém work-text. Lê:
  - artifacts/scenes/<scene>/dialogs.csv         (source + byte_budget, de split_scenes.py)
  - artifacts/scenes/<scene>/translations_*.json (traduções da IA; chave 'lines')
e emite:
  - artifacts/scenes/<scene>/translation_plan_<sfx>.json
  - artifacts/scenes/<scene>/approved_<sfx>.csv  (offset, text_target)

Valida: cobertura total (todo offset com tradução) e preservação dos tokens de formatação do
engine (formatting_tokens + formatting_token_patterns em project.json — mapeados em 2026-08-23
via varredura regex sobre as 41.834 strings, ver project.json). Truncamento por byte_budget é
tratado no reinsert/verify (same-size replace, sem realocação) — não é validado aqui.

Uso: python build_plan_chapter.py <scene>   ex.: python build_plan_chapter.py mp0000
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_RISK = frozenset({"low", "medium", "high", "critical"})
_FRAMEWORK_CONNECTORS = ROOT.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (structural_token_rx compartilhada com model.py, #124)


def _structural_token_rx(root: Path):
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    return connector_io.structural_token_rx(
        cfg.get("formatting_tokens", []), cfg.get("formatting_token_patterns", []))


def load_dialogs(p: Path) -> tuple[dict, list]:
    rows, order = {}, []
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["offset"]] = {"text_en": r["text_en"], "byte_budget": int(r.get("byte_budget") or 0)}
            order.append(r["offset"])
    return rows, order


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python build_plan_chapter.py <scene>")
    scene_dir = ROOT / "artifacts" / "scenes" / sys.argv[1]
    if not scene_dir.is_dir():
        sys.exit(f"ERRO: diretorio nao encontrado: {scene_dir}")

    structural_rx = _structural_token_rx(ROOT)

    trans_files = sorted(scene_dir.glob("translations_*.json"))
    if len(trans_files) != 1:
        sys.exit(f"ERRO: esperado exatamente 1 translations_*.json em {scene_dir}, achei {len(trans_files)}")
    sfx = trans_files[0].stem.replace("translations_", "")

    dialogs, order = load_dialogs(scene_dir / "dialogs.csv")
    trans = json.loads(trans_files[0].read_text(encoding="utf-8"))["lines"]

    errors = []
    miss = [o for o in order if o not in trans]
    extra = [o for o in trans if o not in dialogs]
    if miss:
        errors.append(f"{len(miss)} offset(s) sem traducao: {miss[:5]}")
    if extra:
        errors.append(f"{len(extra)} offset(s) na traducao inexistentes no source: {extra[:5]}")

    plan_lines, approved = [], []
    for off in order:
        if off not in trans:
            continue
        src = dialogs[off]["text_en"]
        t = trans[off]
        tgt = t["t"]
        src_tokens = Counter(structural_rx.findall(src))
        tgt_tokens = Counter(structural_rx.findall(tgt))
        if src_tokens != tgt_tokens:
            errors.append(f"{off}: tokens de formatacao divergentes "
                          f"(src={sorted(src_tokens.elements())} tgt={sorted(tgt_tokens.elements())})")
        risk = t.get("risk_level")
        if risk not in _RISK:
            errors.append(f"{off}: risk_level ausente/invalido '{risk}'")
            risk = "low"
        line = {"offset": off, "text_source": src, "speaker": t.get("speaker", ""),
               "risk_level": risk, "base_translation": tgt,
               "byte_budget": dialogs[off]["byte_budget"]}
        if "risk_notes" in t:
            line["risk_notes"] = t["risk_notes"]
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

    plan = {"scene": sys.argv[1], "lines": plan_lines, "total_lines": len(plan_lines),
           "high_lines": sum(1 for ln in plan_lines if ln["risk_level"] in ("high", "critical"))}
    (scene_dir / f"translation_plan_{sfx}.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    with (scene_dir / f"approved_{sfx}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerows(approved)

    print(f"OK: {len(plan_lines)} linha(s) -> translation_plan_{sfx}.json + approved_{sfx}.csv")


if __name__ == "__main__":
    main()
