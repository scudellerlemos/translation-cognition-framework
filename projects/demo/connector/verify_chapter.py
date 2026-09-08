#!/usr/bin/env python3
"""
verify_chapter.py — conector do projeto de demonstracao (projects/demo).

Formato sintetico: nao ha binario real, entao o oraculo de round-trip e o mais simples
possivel — reconstruir o texto SEM nenhuma traducao (approved={}) tem que reproduzir
connector/source.txt byte-a-byte. E o suficiente para provar o protocolo de saida do
conector (exit codes + linha VERIFY_STATUS) fim-a-fim sem depender de nenhum jogo real.

Protocolo de saida (igual a todo conector do framework):
  exit 0 = OK (round-trip + cobertura bateram)
  exit 1 = falha dura
  + linha "VERIFY_STATUS: {json}" com {ok, fitting_failure, n_fails}

Uso: python verify_chapter.py <scene>
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _rebuild(scene: str, dialogs: dict, approved: dict) -> tuple[bool, bool, list[str]]:
    """round_trip_ok: juntar dialogs (sem nenhuma traducao) com '\\n' reproduz connector/source.txt
    byte-a-byte -- o oraculo deste formato sintetico (sem binario/tokens de tamanho, entao
    fitting_failure e sempre False)."""
    original_path = ROOT / "connector" / "source.txt"
    original = original_path.read_text(encoding="utf-8") if original_path.is_file() else ""
    rebuilt_untranslated = "\n".join(dialogs.values()) + "\n"
    round_trip_ok = rebuilt_untranslated == original

    fails: list[str] = []
    if not round_trip_ok:
        fails.append(f"round-trip falhou: reconstrucao sem traducao nao bate com {original_path.name}")
    missing = [o for o in dialogs if o not in approved]
    if missing:
        fails.append(f"{len(missing)} offset(s) sem traducao aprovada: {missing[:5]}")
    return round_trip_ok, False, fails


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <scene>")
    scene = sys.argv[1]
    scene_dir = ROOT / "artifacts" / "scenes" / scene
    if not scene_dir.is_dir():
        sys.exit(f"ERRO: diretorio nao encontrado: {scene_dir}")

    appr_files = sorted(scene_dir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(f"ERRO: esperado 1 approved_*.csv em {scene_dir}, achei {len(appr_files)}")

    dialogs: dict[str, str] = {}
    with (scene_dir / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = row["text_en"]

    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    round_trip_ok, fitting_failure, fails = _rebuild(scene, dialogs, approved)

    print(f"Cena {scene}: {len(dialogs)} string(s)")
    print(f"  round-trip: {'OK' if round_trip_ok else 'FALHOU'}")

    print("VERIFY_STATUS: " + json.dumps(
        {"ok": not fails, "fitting_failure": fitting_failure, "n_fails": len(fails)},
        ensure_ascii=False))

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(3 if fitting_failure else 1)

    print(f"\nOK: cena {scene} reinsere e round-trip integro.")


if __name__ == "__main__":
    main()
