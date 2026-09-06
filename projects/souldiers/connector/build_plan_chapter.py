#!/usr/bin/env python3
"""
build_plan_chapter.py — Souldiers

Monta translation_plan + approved de UMA cena.

GOVERNANÇA: NÃO contém work-text. Lê:
  - artifacts/scenes/<scene>/dialogs.csv         (source, do split_scenes)
  - artifacts/scenes/<scene>/translations_*.json (traduções da IA; chave 'lines')
e emite:
  - artifacts/scenes/<scene>/translation_plan_<sfx>.json
  - artifacts/scenes/<scene>/approved_<sfx>.csv  (offset, text_target)

Valida: cobertura total, tokens de timing (_N_) e tags TMP (<color=X>, <b>) preservados por
linha (estruturais do engine — ver project.json connector.control_codes), risk>=medium exige
risk_notes. Sem resíduo/byte_budget (project.json length_constraints.mode="none" — engine faz wrap
automático), diferente do BoF4.

Uso: python build_plan_chapter.py <scene>   ex.: python build_plan_chapter.py EUDER_PRESENTATION
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (normalize_speaker compartilhado entre conectores)

ROOT = Path(__file__).resolve().parent.parent
_RISK = connector_io.RISK_LEVELS

_TIMING_RX = re.compile(r"_\d+_")
_TAG_RX = re.compile(r"<[^>]+>")


def _load_known_speakers(root: Path) -> frozenset:
    vc = root / "artifacts" / "state" / "voice_cards.json"
    names = set(json.loads(vc.read_text(encoding="utf-8")).keys()) if vc.is_file() else set()
    return frozenset(names | {"npc", "system", "unknown"})


def load_dialogs(p: Path) -> tuple[dict, list]:
    rows, order = {}, []
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["offset"]] = {
                "text_en": r["text_en"],
                "byte_budget": int(r["byte_budget"]),
            }
            order.append(r["offset"])
    return rows, order


def _tokens(text: str) -> Counter:
    """Tokens de timing (_100_ etc.) e tags TMP (<color=X>, </color>, <b>, </b>) — estruturais do
    engine Unity, devem sobreviver à tradução verbatim (ver control_codes em project.json)."""
    return Counter(_TIMING_RX.findall(text) + _TAG_RX.findall(text))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python build_plan_chapter.py <scene>  (ex.: EUDER_PRESENTATION)")
    chdir = ROOT / "artifacts" / "scenes" / sys.argv[1]
    if not chdir.is_dir():
        sys.exit(f"ERRO: diretório não encontrado: {chdir}")

    trans_files = sorted(chdir.glob("translations_*.json"))
    if len(trans_files) != 1:
        sys.exit(
            f"ERRO: esperado exatamente 1 translations_*.json em {chdir}, "
            f"achei {len(trans_files)}"
        )
    sfx = trans_files[0].stem.replace("translations_", "")

    dialogs, order = load_dialogs(chdir / "dialogs.csv")
    trans = json.loads(trans_files[0].read_text(encoding="utf-8"))["lines"]
    canonical_speakers = _load_known_speakers(ROOT)

    errors = []
    miss = [o for o in order if o not in trans]
    extra = [o for o in trans if o not in dialogs]
    if miss:
        errors.append(f"{len(miss)} offsets sem tradução: {miss[:5]}")
    if extra:
        errors.append(
            f"{len(extra)} offsets na tradução inexistentes no source: {extra[:5]}"
        )

    plan_lines, approved = [], []
    for off in order:
        if off not in trans:
            continue
        src = dialogs[off]["text_en"]
        budget = dialogs[off]["byte_budget"]
        t = trans[off]
        tgt = t["t"]

        # tokens de timing/tags TMP são estruturais do engine — devem sobreviver verbatim
        if _tokens(src) != _tokens(tgt):
            errors.append(
                f"{off}: tokens de timing/tags TMP divergentes "
                f"(src={sorted(_tokens(src).elements())} tgt={sorted(_tokens(tgt).elements())})"
            )

        risk = t.get("risk_level")
        if risk not in _RISK:
            errors.append(f"{off}: risk_level ausente/invalido '{risk}'")
            risk = "low"

        line = {
            "offset": off,
            "text_source": src,
            "speaker": connector_io.normalize_speaker(t.get("speaker", ""), canonical_speakers),
            "tone_register": t.get("tone_register", ""),
            "intent": t.get("intent", ""),
            "risk_level": risk,
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

    for ln in plan_lines:
        if ln["risk_level"] in ("medium", "high", "critical") and "risk_notes" not in ln:
            errors.append(f"{ln['offset']}: risk={ln['risk_level']} sem risk_notes")

    if errors:
        print("ERROS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    plan = {
        "scene": sys.argv[1],
        "scene_group": sfx,
        "lines": plan_lines,
        "total_lines": len(plan_lines),
        "high_lines": sum(
            1 for ln in plan_lines if ln["risk_level"] in ("high", "critical")
        ),
        "medium_lines": sum(
            1 for ln in plan_lines if ln["risk_level"] == "medium"
        ),
        "needs_review": [
            ln["offset"] for ln in plan_lines if ln.get("needs_human_review")
        ],
        "plan_version": f"souldiers-{sfx}-v1",
    }
    (chdir / f"translation_plan_{sfx}.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (chdir / f"approved_{sfx}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["offset", "text_target"])
        w.writerows(approved)

    n_low = len(plan_lines) - plan["high_lines"] - plan["medium_lines"]
    print(
        f"OK: {len(plan_lines)} linhas -> "
        f"translation_plan_{sfx}.json + approved_{sfx}.csv"
    )
    print(
        f"  risco: {plan['high_lines']} high, "
        f"{plan['medium_lines']} medium, {n_low} low"
    )
    print(f"  needs_human_review: {plan['needs_review'] or 'nenhum'}")


if __name__ == "__main__":
    main()
