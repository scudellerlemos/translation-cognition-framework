#!/usr/bin/env python3
"""
split_scenes.py — materializa artifacts/scenes/<scene>/dialogs.csv a partir do dialogs.csv FLAT
gerado por extract.py (Passo 00), agrupando por uma coluna do corpus (default: "file").

Gap descoberto no bring-up do Trails Sky SC (2026-08-23): run_scene/build_plan_chapter exigem
artifacts/scenes/<scene>/dialogs.csv (paths.py, contrato congelado), mas extract.py de todo
conector so escreve o flat artifacts/dialogs.csv (paths.dialogs_flat) -- nao havia NENHUMA
ferramenta generica no framework pra fazer essa ponte; os projetos existentes (BoF4/Souldiers/
Utawarerumono) resolveram isso ad hoc, fora do framework versionado.

Escopo deliberado: cobre o caso em que 1 coluna do corpus ja identifica a cena 1:1 (ex.: "file" —
o padrao do BoF4 e agora do Trails Sky SC: 1 arquivo-fonte = 1 cena). Projetos com regra de
agrupamento diferente (Souldiers: prefixo do offset; Utawarerumono: extract.py roda 1x por cena)
continuam fora do escopo desta ferramenta — nao forca um contrato que os 3 nao compartilham.

Uso:
    python split_scenes.py <projeto> [--by COLUNA] [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402  (fonte unica do contrato de paths de artefato)

_FRAMEWORK_CONNECTORS = _HERE.parent / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (write_dialogs_csv compartilhado com extract.py dos conectores)

_UNSAFE = re.compile(r"[^A-Za-z0-9_.-]")


def _scene_name(value: str) -> str:
    """Deriva um nome de cena seguro pra filesystem a partir do valor da coluna de agrupamento:
    stem do ultimo componente de path, sem extensao, sanitizado (scene_dir nao aceita separador)."""
    stem = Path(value).stem
    return _UNSAFE.sub("_", stem) or "scene"


def split(root: Path, by: str = "file", dry_run: bool = False) -> dict:
    flat = paths.dialogs_flat(root)
    if not flat.is_file():
        sys.exit(f"ERRO: {flat} nao existe -- rode extract.py primeiro (Passo 00).")
    with flat.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        if by not in fieldnames:
            sys.exit(f"ERRO: coluna '{by}' nao existe em {flat} (colunas: {fieldnames}).")
        rows = list(reader)

    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(_scene_name(row[by]), []).append(row)

    if not dry_run:
        for scene, scene_rows in groups.items():
            connector_io.write_dialogs_csv(paths.dialogs(root, scene), fieldnames, scene_rows)

    return {"scenes": len(groups), "rows": len(rows), "by": by}


def main() -> None:
    ap = argparse.ArgumentParser(description="Divide o dialogs.csv flat em artifacts/scenes/<cena>/dialogs.csv.")
    ap.add_argument("project", help="raiz do projeto (ex.: projects/trails_sky_sc)")
    ap.add_argument("--by", default="file", help="coluna de agrupamento (default: file)")
    ap.add_argument("--dry-run", action="store_true", help="so reporta contagens, nao escreve")
    args = ap.parse_args()

    root = Path(args.project)
    result = split(root, by=args.by, dry_run=args.dry_run)
    tail = " (dry-run, nada escrito)" if args.dry_run else f" em {paths.scenes_dir(root)}"
    print(f"OK: {result['rows']} linha(s) -> {result['scenes']} cena(s) agrupadas por '{result['by']}'{tail}")


if __name__ == "__main__":
    main()
