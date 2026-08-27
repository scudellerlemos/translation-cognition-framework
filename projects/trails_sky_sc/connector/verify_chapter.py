#!/usr/bin/env python3
"""
verify_chapter.py — Trails in the Sky 2nd Chapter

Adaptado do skeleton (framework/connectors/_skeleton/verify_chapter.py) pro contêiner FPAC
compartilhado: as strings de uma cena vivem em 1 (ou poucos) `scena/*.dat` embutidos no MESMO
buffer `script_en.pac` — não há arquivo isolado por cena.

Oráculos (nesta ordem, todos sobre o buffer do .pac REAL lido de TRAILS_SKY_SC_DATA_DIR):
  1. round-trip vazio: rebuild_pac(pac, entries, {}, budgets) == pac_bytes original (identidade).
  2. round-trip significativo: reinserir o PRÓPRIO text_en de cada offset da cena (budget ==
     len(text_en)+1 exatamente, por construção do extract.py) deve reproduzir os bytes originais
     byte a byte — exercita de verdade o write path (replace + padding), não só o fast-path vazio.
  3. apply real: rebuild_pac com `approved` (fallback pro text_en se faltar aprovação).
  4. overflow individual: encode(utf-8)+1 > byte_budget -> falha SÓ de fitting (fitting_failure).
  5. readback por offset (não re-scan — ver reinsert.read_scena_strings docstring): bytes lidos
     de volta em abs_off:abs_off+budget, sem padding, devem bater com truncate_for_budget().
  6. sem corrupção fora da cena: bytes fora dos entries tocados == bytes originais.

Uso: python verify_chapter.py <scene> [data_dir]
"""
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import fpac_unpack  # noqa: E402
import reinsert as R  # noqa: E402

ROOT = _HERE.parent


def _rebuild(scene: str, dialogs: dict, approved: dict, data_dir_arg: str | None
             ) -> tuple[bool, bool, list[str]]:
    fails: list[str] = []
    fitting_failure = False

    data_dir = R._resolve_data_dir(data_dir_arg)
    pac_path = data_dir / R._SCRIPT_PAC
    pac_bytes, entries = fpac_unpack.read_index(pac_path)

    budgets = {off: meta["byte_budget"] for off, meta in dialogs.items()}
    touched_files = sorted({meta["file"] for meta in dialogs.values()})
    touched = [e for e in entries if "scena/" + e[0].split("/scena/", 1)[-1] in touched_files
               if "/scena/" in e[0] and e[0].endswith(".dat")]
    if not touched:
        return False, False, [f"nenhum entry scena/ do .pac corresponde aos arquivos da cena {touched_files}"]

    # 1. round-trip vazio (fast-path de identidade)
    empty_bytes, _ = R.rebuild_pac(pac_bytes, entries, {}, budgets)
    round_trip_ok = empty_bytes == pac_bytes
    if not round_trip_ok:
        fails.append("round-trip vazio nao reproduz o .pac original byte a byte")

    # 2. round-trip significativo: reinserir o proprio text_en (budget = len+1 exato)
    identity = {off: meta["text_en"] for off, meta in dialogs.items()}
    identity_bytes, _ = R.rebuild_pac(pac_bytes, entries, identity, budgets)
    if identity_bytes != pac_bytes:
        round_trip_ok = False
        fails.append("round-trip com text_en original nao reproduz o .pac byte a byte (write path quebrado)")

    # 3. apply real (fallback pro original se a cena tiver offset sem aprovacao)
    real = {off: approved.get(off, meta["text_en"]) for off, meta in dialogs.items()}
    new_bytes, changed = R.rebuild_pac(pac_bytes, entries, real, budgets)

    # 4 + 5. overflow individual + readback por offset
    for name, size, addr, _crc in touched:
        rel_name = "scena/" + name.split("/scena/", 1)[1]
        for off, meta in dialogs.items():
            if meta["file"] != rel_name:
                continue
            _, _, off_hex = off.partition(":")
            budget = meta["byte_budget"]
            text = real[off]
            encoded = text.encode("utf-8")
            if len(encoded) + 1 > budget:
                fitting_failure = True
                fails.append(f"individual_overflow {off}: {len(encoded)+1}b > budget={budget}")

            abs_off = addr + int(off_hex, 16)
            expected = R.truncate_for_budget(text, budget).rstrip(b"\x00")
            actual = new_bytes[abs_off:abs_off + budget].rstrip(b"\x00")
            if actual != expected:
                fails.append(f"readback {off}: esperado {expected!r}, lido {actual!r}")

    # 6. sem corrupcao fora da cena
    ranges = sorted((addr, addr + size) for name, size, addr, _crc in touched)
    prev_end = 0
    for start, end in ranges:
        if new_bytes[prev_end:start] != pac_bytes[prev_end:start]:
            fails.append(f"bytes alterados fora da cena, regiao [{prev_end}:{start}]")
        prev_end = end
    if new_bytes[prev_end:] != pac_bytes[prev_end:]:
        fails.append(f"bytes alterados fora da cena, regiao [{prev_end}:fim]")

    if changed == 0 and dialogs:
        fails.append("apply real nao alterou nenhuma string (esperado >=1)")

    return round_trip_ok, fitting_failure, fails


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <scene> [data_dir]")
    scene = sys.argv[1]
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    scene_dir = ROOT / "artifacts" / "scenes" / scene
    if not scene_dir.is_dir():
        sys.exit(f"ERRO: diretorio nao encontrado: {scene_dir}")

    appr_files = sorted(scene_dir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(f"ERRO: esperado 1 approved_*.csv em {scene_dir}, achei {len(appr_files)}")

    dialogs: dict[str, dict] = {}
    with (scene_dir / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = {"text_en": row["text_en"], "file": row["file"],
                                       "byte_budget": int(row["byte_budget"])}

    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    round_trip_ok, fitting_failure, fails = _rebuild(scene, dialogs, approved, data_dir_arg)

    hard_fails = [f for f in fails if not f.startswith("individual_overflow")]
    fitting_only = bool(fails) and not hard_fails

    print(f"Cena {scene}: {len(dialogs)} string(s)")
    print(f"  round-trip: {'OK' if round_trip_ok else 'FALHOU'}")

    print("VERIFY_STATUS: " + json.dumps(
        {"ok": not fails, "fitting_failure": fitting_only, "n_fails": len(fails)},
        ensure_ascii=False))

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(3 if fitting_only else 1)

    print(f"\nOK: cena {scene} reinsere e round-trip integro.")


if __name__ == "__main__":
    main()
