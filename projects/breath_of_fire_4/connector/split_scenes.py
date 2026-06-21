#!/usr/bin/env python3
"""
split_scenes.py — Breath of Fire IV

Divide o artifacts/dialogs.csv flat em sub-diretórios por arquivo DAT:
  artifacts/scenes/<stem>/dialogs.csv   (ex.: artifacts/scenes/AREAD001/dialogs.csv)

Pré-requisito para run_scene.py: o harness espera dialogs.csv por cena.
Determinístico e idempotente.

Uso: python split_scenes.py [project_root]   (default: diretório pai deste script)
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDNAMES = ["offset", "file", "entry_idx", "ptr_idx", "text_en", "byte_budget", "speaker_code"]


def main(root: Path = ROOT) -> None:
    flat = root / "artifacts" / "dialogs.csv"
    if not flat.is_file():
        sys.exit(f"ERRO: {flat} não encontrado — rode extract.py primeiro")

    by_file: dict[str, list[dict]] = defaultdict(list)
    with flat.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_file[row["file"]].append(row)

    created = []
    for fname, rows in sorted(by_file.items()):
        stem = Path(fname).stem  # AREAD001.DAT -> AREAD001
        scene_dir = root / "artifacts" / "scenes" / stem
        scene_dir.mkdir(parents=True, exist_ok=True)
        out = scene_dir / "dialogs.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        created.append((stem, len(rows)))

    print(f"OK: {len(created)} cenas em artifacts/scenes/")
    print("  " + "  ".join(f"{stem} ({n} strings)" for stem, n in created))


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    main(root)
