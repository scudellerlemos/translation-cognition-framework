#!/usr/bin/env python3
"""
verify_chapter.py — Breath of Fire IV

Verifica a reinserção de UMA cena (1 arquivo DAT) pelo protocolo do harness:
  1. Round-trip: rebuild_section(translations={}) reproduz o DAT byte-a-byte
  2. Apply: rebuild_section(translations) → ler strings de volta == encode_string(target)
  3. T4: strings que individualmente excedem byte_budget

GOVERNANÇA: sem work-text. Lê os binários DAT somente-leitura; não escreve no jogo.
game_dat_dir: project.json connector.game_dat_dir  OU  variável BOF4_DAT_DIR.

Protocolo de exit code (consumido por run_scene.py):
  exit 0 = OK
  exit 3 = falha SOMENTE de fitting (T4 individual → re-traduzir mais curto pode ajudar)
  exit 1 = falha dura (round-trip ou leitura — apertar o budget não cura)

Uso: python verify_chapter.py <scene>   ex.: python verify_chapter.py AREAD001
"""
import csv
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import extract as E   # noqa: E402
import reinsert as R  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _dat_dir(root: Path) -> Path:
    env = os.environ.get("BOF4_DAT_DIR")
    if env:
        return Path(env)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    d = cfg.get("connector", {}).get("game_dat_dir", "")
    if not d or "TBD" in str(d):
        sys.exit(
            "ERRO: game_dat_dir não configurado em project.json connector.game_dat_dir\n"
            "      Edite project.json com o caminho do diretório english/DAT\n"
            "      ou exporte: set BOF4_DAT_DIR=<caminho>"
        )
    return Path(d)


def _section_strings(section: bytes) -> dict[int, bytes]:
    """ptr_idx → raw bytes (sem terminador null)."""
    return {s[0]: s[2] for s in E.extract_section_strings(section)}


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python verify_chapter.py <scene>  (ex.: AREAD001)")

    scene = sys.argv[1]
    chdir = ROOT / "artifacts" / "scenes" / scene
    if not chdir.is_dir():
        sys.exit(f"ERRO: diretório não encontrado: {chdir}")

    appr_files = sorted(chdir.glob("approved_*.csv"))
    if len(appr_files) != 1:
        sys.exit(
            f"ERRO: esperado 1 approved_*.csv em {chdir}, achei {len(appr_files)}"
        )

    dat_dir = _dat_dir(ROOT)

    # Dialogs da cena (per-scene, não o flat)
    dialogs: dict[str, dict] = {}
    with (chdir / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = {
                "file": row["file"],
                "ptr_idx": int(row["ptr_idx"]),
                "text_en": row["text_en"],
                "byte_budget": int(row["byte_budget"]),
            }

    # Aprovados
    approved: dict[str, str] = {}
    with appr_files[0].open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            approved[row["offset"]] = row["text_target"]

    touched_files = sorted({meta["file"] for meta in dialogs.values()})

    fails: list[str] = []
    t4_count = 0
    checked = 0

    for fname in touched_files:
        dat_path = dat_dir / fname
        if not dat_path.is_file():
            fails.append(f"{fname}: arquivo não encontrado em {dat_dir}")
            continue

        original_data = dat_path.read_bytes()
        entries = E.parse_toc(original_data)
        result = E.find_text_section(original_data, entries)
        if result is None:
            fails.append(f"{fname}: seção de texto não encontrada")
            continue

        entry_idx, sec_off, sec_sz = result
        section = original_data[sec_off:sec_off + sec_sz]

        # --- 1) Round-trip ---
        try:
            rt_section = R.rebuild_section(section, {})
        except Exception as exc:
            fails.append(f"{fname}: round-trip — rebuild_section falhou: {exc}")
            continue

        if rt_section != bytes(section):
            fails.append(f"{fname}: round-trip falhou (seção difere com translations vazio)")
        else:
            rt_data = R.patch_dat_file(original_data, entry_idx, rt_section)
            if rt_data != original_data:
                fails.append(
                    f"{fname}: round-trip falhou (arquivo difere com translations vazio)"
                )

        # --- 2) Monta translations {ptr_idx: text} para este arquivo ---
        file_translations: dict[int, str] = {}
        for off, meta in dialogs.items():
            if meta["file"] != fname:
                continue
            file_translations[meta["ptr_idx"]] = (
                approved[off] if off in approved else meta["text_en"]
            )

        try:
            new_section = R.rebuild_section(section, file_translations)
        except OverflowError as exc:
            fails.append(f"{fname}: overflow de ponteiro — {exc}")
            continue

        # --- 3) T4 individual: strings acima do byte_budget ---
        for off, meta in dialogs.items():
            if meta["file"] != fname or off not in approved:
                continue
            encoded = E.encode_string(approved[off])
            if len(encoded) + 1 > meta["byte_budget"]:
                fails.append(
                    f"{off}: T4_individual "
                    f"{len(encoded) + 1}>{meta['byte_budget']}b"
                )
                t4_count += 1

        # --- 4) Leitura de volta ---
        new_strings = _section_strings(new_section)
        for off, meta in dialogs.items():
            if meta["file"] != fname or off not in approved:
                continue
            ptr_idx = meta["ptr_idx"]
            want = E.encode_string(approved[off])
            got = new_strings.get(ptr_idx, b"")
            if got == want:
                checked += 1
            else:
                fails.append(
                    f"{off}: lido {E.decode_string(got)!r} "
                    f"!= aprovado {E.decode_string(want)!r}"
                )

    # Fitting = só há T4 individuals, sem falhas duras de round-trip ou leitura
    hard_fails = [f for f in fails if "T4_individual" not in f]
    fitting_only = bool(fails) and not hard_fails

    print(
        f"Cena {scene}: {len(dialogs)} strings em "
        f"{len(touched_files)} arquivo(s) {touched_files}"
    )
    rt_ok = not any("round-trip" in f for f in fails)
    print(f"  round-trip: {'OK' if rt_ok else 'FALHOU'}")
    print(f"  strings conferidas (lido == approved encoded): {checked}/{len(approved)}")
    print(f"  T4 individual (overflow de byte_budget): {t4_count}")

    print("VERIFY_STATUS: " + json.dumps({
        "ok": not fails,
        "fitting_failure": fitting_only,
        "t4_individual": t4_count,
        "n_fails": len(fails),
    }, ensure_ascii=False))

    if fails:
        print("\nFALHAS:")
        for x in fails:
            print("  -", x)
        sys.exit(3 if fitting_only else 1)

    print(f"\nOK: cena {scene} reinsere e round-trip íntegro.")


if __name__ == "__main__":
    main()
