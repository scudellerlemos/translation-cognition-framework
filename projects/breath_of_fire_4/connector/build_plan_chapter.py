#!/usr/bin/env python3
"""
build_plan_chapter.py — Breath of Fire IV

Monta translation_plan + approved de UMA cena (1 arquivo DAT).

GOVERNANÇA: NÃO contém work-text. Lê:
  - artifacts/<scene>/dialogs.csv         (source + byte_budget, do split_scenes)
  - artifacts/<scene>/translations_*.json (traduções da IA; chave 'lines')
e emite:
  - artifacts/<scene>/translation_plan_<sfx>.json
  - artifacts/<scene>/approved_<sfx>.csv  (offset, text_target)

Valida: cobertura total, token [02] (page break) preservado por linha, risk>=medium
exige risk_notes. [01] é newline dentro da caixa (wrap) — sua contagem varia
legitimamente entre EN e PT-BR conforme o tamanho da frase; não é validado.

Uso: python build_plan_chapter.py <scene>   ex.: python build_plan_chapter.py AREAD001
"""
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (normalize_speaker compartilhado entre conectores)

ROOT = Path(__file__).resolve().parent.parent
PAGE_BREAK = "[02]"  # page break do BoF4 — estrutural (ritmo de leitura)
_RISK = frozenset({"low", "medium", "high", "critical"})


def _load_known_speakers(root: Path) -> frozenset:
    vc = root / "artifacts" / "state" / "voice_cards.json"
    names = set(json.loads(vc.read_text(encoding="utf-8")).keys()) if vc.is_file() else set()
    return frozenset(names | {"npc", "system", "unknown"})


def _load_portrait_codes(root: Path) -> dict:
    """speaker_code ([14][XX], extraído deterministicamente do binário) -> nome canônico.

    Ver artifacts/state/portrait_codes.json. Chaves iniciadas com '_' são metadados,
    não códigos (ex.: '_meta').
    """
    pc = root / "artifacts" / "state" / "portrait_codes.json"
    if not pc.is_file():
        return {}
    data = json.loads(pc.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def _resolve_speaker(code: str, llm_guess: str, portrait_codes: dict, canonical: frozenset) -> str:
    """speaker_code determinístico tem precedência sobre o guess do LLM.

    Código presente e mapeado em portrait_codes -> nome canônico direto (#64).
    Caso contrário, cai no comportamento anterior: guess do LLM normalizado.
    """
    if code and code in portrait_codes:
        return portrait_codes[code]
    return connector_io.normalize_speaker(llm_guess, canonical)


def load_dialogs(p: Path) -> tuple[dict, list]:
    rows, order = {}, []
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[r["offset"]] = {
                "text_en": r["text_en"],
                "byte_budget": int(r["byte_budget"]),
                "speaker_code": r.get("speaker_code", ""),
            }
            order.append(r["offset"])
    return rows, order


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python build_plan_chapter.py <scene>  (ex.: AREAD001)")
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
    portrait_codes = _load_portrait_codes(ROOT)

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

        # [02] = page break (estrutural: controla ritmo de leitura); deve ser preservado
        if (PAGE_BREAK in src) != (PAGE_BREAK in tgt):
            errors.append(
                f"{off}: token [02] (page break) divergente "
                f"(src={PAGE_BREAK in src} tgt={PAGE_BREAK in tgt})"
            )

        risk = t.get("risk_level")
        if risk not in _RISK:
            errors.append(f"{off}: risk_level ausente/invalido '{risk}'")
            risk = "low"

        line = {
            "offset": off,
            "text_source": src,
            "speaker": _resolve_speaker(
                dialogs[off].get("speaker_code", ""), t.get("speaker", ""),
                portrait_codes, canonical_speakers,
            ),
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
        "plan_version": f"bof4-{sfx}-v1",
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
