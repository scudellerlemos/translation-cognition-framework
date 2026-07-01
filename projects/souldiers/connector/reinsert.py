#!/usr/bin/env python3
"""
reinsert.py — Souldiers (Forge Reply, 2022 — Unity Addressables + tilde-CSV)

Contrato:
    entrada : approved_translations.csv (offset, text_pt) + data_dir (bundles)
    saída   : output/<bundle>.bundle (cópia modificada com ::PT:: preenchido)
              artifacts/reinsertion_report.md

Regras:
- 100% determinístico. LLM NUNCA toca nos bundles diretamente.
- O bundle original NUNCA é sobrescrito; cópias vão para output/.
- Tokens _100_/_300_/etc. e tags TMP devem estar na tradução verbatim.
- Linhas ausentes no approved_translations.csv ficam com a coluna PT original do bundle.
"""
from __future__ import annotations

import csv
import io
import json
import os
import shutil
import sys
from pathlib import Path

_CSV_DELIMITER = "~"
_ID_COL = "::ID::"
_PT_COL = "::PT::"

_DIALOGUE_TABLES: dict[str, str] = {
    "texts_DIALOGS":        "8bbb65e6bcd747af3bbead6db0716968.bundle",
    "texts_INGAME_DIALOGS": "8d47b47a21c47126bf303e267a66fc73.bundle",
    "texts_SIDE_DIALOGS":   "a77305a96d09041b74e5948e4f67851e.bundle",
}


def _resolve_data_dir(project_json: Path, cli_override: str | None) -> Path:
    if cli_override:
        return Path(cli_override)
    env = os.environ.get("SOULDIERS_DATA_DIR")
    if env:
        return Path(env)
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    d = cfg.get("connector", {}).get("data_dir")
    if d:
        return Path(d)
    raise RuntimeError(
        "Caminho do jogo não encontrado. Defina SOULDIERS_DATA_DIR ou passe como argumento."
    )


def reinsert(project_root: Path, data_dir: Path) -> int:
    """Aplica as traduções aprovadas nos bundles e salva cópias em output/.

    Retorna o número de linhas reinseridas.
    """
    try:
        import UnityPy
    except ImportError:
        raise ImportError("UnityPy não instalado. Execute: pip install UnityPy")

    artifacts = project_root / "artifacts"
    approved_csv = artifacts / "approved_translations.csv"
    if not approved_csv.is_file():
        raise FileNotFoundError(f"Arquivo de traduções não encontrado: {approved_csv}")

    # Carrega traduções aprovadas: offset → text_pt
    translations: dict[str, str] = {}
    with approved_csv.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = row.get("offset", "").strip()
            val = row.get("text_pt", "").strip()
            if key and val:
                translations[key] = val

    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_lines: list[str] = [
        "# Reinsertion Report — Souldiers\n",
        f"Traduções carregadas: {len(translations)}\n\n",
    ]

    total_inserted = 0

    for table_name, bundle_file in _DIALOGUE_TABLES.items():
        bundle_path = data_dir / bundle_file
        if not bundle_path.is_file():
            report_lines.append(f"- AVISO: bundle não encontrado: {bundle_file}\n")
            continue

        out_bundle = output_dir / bundle_file
        shutil.copy2(bundle_path, out_bundle)

        env = UnityPy.load(str(out_bundle))
        table_inserted = 0

        for obj in env.objects:
            if obj.type.name != "TextAsset":
                continue
            d = obj.read()
            if getattr(d, "m_Name", "") != table_name:
                continue

            text = d.m_Script
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")

            reader = csv.DictReader(io.StringIO(text), delimiter=_CSV_DELIMITER)
            fieldnames = reader.fieldnames or []
            rows = list(reader)

            for row in rows:
                row_id = row.get(_ID_COL, "").strip().strip('"')
                if row_id in translations:
                    row[_PT_COL] = translations[row_id]
                    table_inserted += 1

            # Reconstrói CSV com delimitador ~
            out_buf = io.StringIO()
            writer = csv.DictWriter(out_buf, fieldnames=fieldnames,
                                    delimiter=_CSV_DELIMITER, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)

            new_text = out_buf.getvalue().encode("utf-8")
            d.m_Script = new_text
            d.save()
            break

        # Grava o bundle modificado
        with out_bundle.open("wb") as f:
            for file in env.file.files.values():
                f.write(file.save())

        total_inserted += table_inserted
        report_lines.append(
            f"- {table_name}: {table_inserted} linhas reinseridas → {out_bundle.name}\n"
        )
        print(f"  {table_name}: {table_inserted} linhas → {out_bundle.name}")

    report_path = artifacts / "reinsertion_report.md"
    report_lines.append(f"\nTotal reinserido: {total_inserted} linhas\n")
    report_path.write_text("".join(report_lines), encoding="utf-8")
    print(f"\nReinserido: {total_inserted} linhas. Relatório: {report_path}")
    return total_inserted


def main():
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    project_json = project_root / "project.json"
    data_dir = _resolve_data_dir(project_json, data_dir_arg)
    reinsert(project_root, data_dir)


if __name__ == "__main__":
    main()
