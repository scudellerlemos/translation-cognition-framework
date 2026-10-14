#!/usr/bin/env python3
"""
pilot_gate.py — Breath of Fire IV

Gate de cobertura do piloto, pré-requisito do gate visual in-game (ROADMAP 2.7).

O connector_gate já responde "o que devia ser traduzido foi extraído?" (texto residual). Este responde a
pergunta seguinte: "o que foi extraído e está no trajeto do piloto foi mandado para tradução?". Nos testes
in-game run1 e run2 apareceram cenas em inglês que estavam extraídas mas fora da lista do piloto, porque a
lista era uma escolha manual. Os IDs das cenas não seguem a ordem da história, então o escopo é declarado
cena a cena em artifacts/pilot_scope.csv (scene, no_piloto, confianca, local, evidencia).

Bloqueia quando:
  - uma cena extraída não tem linha no escopo (ninguém decidiu se ela é do trajeto);
  - `no_piloto` não é `sim` nem `nao` (decisão em aberto);
  - uma cena `sim` não está `verified` no run_state.json, ou passou com gate pulado.

GOVERNANÇA: sem work-text. Lê só IDs de cena e status.

Uso: python pilot_gate.py   (exit 0 = OK, 1 = bloqueado)
"""
import contextlib
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / "framework" / "runtime"))
import events  # noqa: E402  (rastro do gate: passou/bloqueou e quando)


def check(extracted, scope, state) -> list[str]:
    """extracted: IDs de cena; scope: {cena: 'sim'|'nao'|...}; state: run_state['scenes']."""
    problems = []
    for scene in sorted(extracted):
        want = scope.get(scene)
        if want is None:
            problems.append(f"{scene}: extraída e sem linha no escopo do piloto")
        elif want not in ("sim", "nao"):
            problems.append(f"{scene}: no_piloto={want!r} — decidir sim ou nao")
        elif want == "sim":
            st = state.get(scene) or {}
            if st.get("status") != "verified":
                problems.append(f"{scene}: no trajeto do piloto e não traduzida/verificada")
            elif st.get("bypassed_gates"):
                problems.append(f"{scene}: verificada com gate pulado ({', '.join(st['bypassed_gates'])})")
    return problems


def main() -> None:
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")
    art = ROOT / "artifacts"
    with open(art / "dialogs.csv", encoding="utf-8", newline="") as f:
        extracted = {r["file"].split(".")[0] for r in csv.DictReader(f)}
    scope_path = art / "pilot_scope.csv"
    scope = {}
    if scope_path.is_file():
        with open(scope_path, encoding="utf-8", newline="") as f:
            scope = {r["scene"]: r["no_piloto"].strip().lower() for r in csv.DictReader(f)}
    state = json.loads((art / "run_state.json").read_text(encoding="utf-8")).get("scenes", {})
    problems = check(extracted, scope, state)
    n_in = sum(v == "sim" for k, v in scope.items() if k in extracted)
    events.emit(ROOT, "gate.pilot", "block" if problems else "pass", problems=len(problems), in_scope=n_in)
    for p in problems:
        print(f"[BLOCK] {p}")
    print(f"\nOK: {n_in} cenas no trajeto do piloto, todas verificadas ({len(extracted)} extraídas)."
          if not problems else f"\nBLOQUEADO: {len(problems)} problema(s) de cobertura do piloto.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
