#!/usr/bin/env python3
"""
extract_template.py — TEMPLATE para Unity Addressables + tilde-CSV (TextAsset)

Engine T1: Unity Addressables com localização em CSVs armazenados como TextAsset dentro
de bundles. Delimitador ~. Colunas ::ID:: / ::EN:: (e ::PT:: / ::ES:: se já localizado).

Projeto de referência: projects/souldiers/connector/extract.py
Registry: framework/connectors/connector_registry.json → id "unity_addressables_csv"

ADAPTAÇÃO NECESSÁRIA (marcar com TODO abaixo):
  1. _DIALOGUE_TABLES — dict {nome_da_tabela: nome_do_bundle_hash}
  2. ENV_VAR_NAME — nome da env var específica do jogo (ex: SOULDIERS_DATA_DIR)
  3. _SPEAKER_RE — padrão de ID do jogo para extrair speaker (se aplicável)
  4. Colunas de saída — dialogs.csv pode precisar de colunas extras (ex: speaker)

COMO DESCOBRIR OS BUNDLE HASHES:
  1. python framework/connectors/discover.py <game_dir> — classifica a engine
  2. Abrir catalog.json em StreamingAssets/aa/ e buscar pelo nome da tabela
  3. Ou: listar todos os TextAsset com UnityPy e filtrar pelo m_Name

Contrato (igual ao conector de referência):
  entrada : <game>_Data/StreamingAssets/aa/StandaloneWindows64/
            via env var <ENV_VAR_NAME> ou arg CLI
  saída   : artifacts/dialogs.csv  (offset, table, text_en, speaker)
            artifacts/extraction_log.md
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# TODO 1: mapear {nome_TextAsset: nome_do_arquivo_bundle}
# Descobrir via catalog.json ou listando TextAssets com UnityPy.
# ---------------------------------------------------------------------------
_DIALOGUE_TABLES: dict[str, str] = {
    # "texts_DIALOGS":        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.bundle",
    # "texts_INGAME_DIALOGS": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy.bundle",
}

_CSV_DELIMITER = "~"
_ID_COL = "::ID::"
_EN_COL = "::EN::"

# TODO 2: nome da env var para o caminho de dados do jogo
_ENV_VAR = "GAME_DATA_DIR"

# TODO 3: regex para extrair speaker do ID (adaptar ao padrão do jogo)
# Exemplo Souldiers: STR_DIALOGS_CAVE_23_D1_BALOF_1 → BALOF
_SPEAKER_RE = re.compile(r"_D\d+_([A-Z0-9]+)_\d+$", re.IGNORECASE)


def _parse_speaker(row_id: str) -> str:
    m = _SPEAKER_RE.search(row_id)
    return m.group(1).upper() if m else ""


def _resolve_data_dir(project_json: Path, cli_override: str | None) -> Path:
    if cli_override:
        return Path(cli_override)
    env = os.environ.get(_ENV_VAR)
    if env:
        return Path(env)
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    d = cfg.get("connector", {}).get("data_dir")
    if d:
        return Path(d)
    raise RuntimeError(
        f"Caminho do jogo não encontrado. Defina {_ENV_VAR} ou passe como argumento.\n"
        f"Exemplo: python extract.py projects/<jogo> C:\\<Jogo>_Data\\StreamingAssets\\aa\\StandaloneWindows64"
    )


def extract(project_root: Path, data_dir: Path) -> int:
    try:
        import UnityPy
    except ImportError:
        raise ImportError(
            "UnityPy não instalado. Execute: pip install UnityPy\n"
            "Documentação: https://github.com/K0lb3/UnityPy"
        )

    if not _DIALOGUE_TABLES:
        raise RuntimeError(
            "_DIALOGUE_TABLES está vazio. Preencher com {nome_tabela: nome_bundle} antes de usar."
        )

    artifacts = project_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    out_csv = artifacts / "dialogs.csv"
    out_log = artifacts / "extraction_log.md"

    rows: list[dict] = []
    log_lines: list[str] = [f"# Extraction Log — {project_root.name}\n\n"]

    for table_name, bundle_file in _DIALOGUE_TABLES.items():
        bundle_path = data_dir / bundle_file
        if not bundle_path.is_file():
            log_lines.append(f"- AVISO: bundle não encontrado: {bundle_file} ({table_name})\n")
            continue

        env = UnityPy.load(str(bundle_path))
        found = False
        for obj in env.objects:
            if obj.type.name != "TextAsset":
                continue
            d = obj.read()
            if getattr(d, "m_Name", "") != table_name:
                continue
            found = True
            text = d.m_Script
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")

            reader = csv.DictReader(io.StringIO(text), delimiter=_CSV_DELIMITER)
            table_rows = 0
            skipped = 0
            for row in reader:
                row_id = row.get(_ID_COL, "").strip().strip('"')
                text_en = row.get(_EN_COL, "").strip().strip('"')
                if not row_id or not text_en:
                    skipped += 1
                    continue
                speaker = _parse_speaker(row_id)
                rows.append({
                    "offset":  row_id,
                    "table":   table_name,
                    "text_en": text_en,
                    "speaker": speaker,
                })
                table_rows += 1

            log_lines.append(
                f"- {table_name}: {table_rows} linhas extraídas, {skipped} vazias ignoradas\n"
            )

        if not found:
            log_lines.append(f"- AVISO: TextAsset não encontrado em {bundle_file}\n")

    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["offset", "table", "text_en", "speaker"])
        writer.writeheader()
        writer.writerows(rows)

    log_lines.append(f"\nTotal: {len(rows)} linhas extraídas\n")
    out_log.write_text("".join(log_lines), encoding="utf-8")
    print(f"Extraído: {len(rows)} linhas -> {out_csv}")
    return len(rows)


def main() -> None:
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    project_json = project_root / "project.json"
    data_dir = _resolve_data_dir(project_json, data_dir_arg)
    extract(project_root, data_dir)


if __name__ == "__main__":
    main()
