#!/usr/bin/env python3
"""
extract.py — Souldiers (Forge Reply, 2022 — Unity Addressables + tilde-CSV)

Contrato:
    entrada : Souldiers_Data/StreamingAssets/aa/StandaloneWindows64/
              via env var SOULDIERS_DATA_DIR ou arg CLI ou project.json[connector][data_dir]
    saída   : artifacts/dialogs.csv  (offset, table, text_en, speaker)
              artifacts/extraction_log.md

Escopo — Fase 0: SOMENTE diálogos de personagem (tabelas DIALOGS, INGAME, SIDE).
UI/Menus/Nomes/Tutorial = fase futura separada.

Regras:
- 100% determinístico. NUNCA usar LLM aqui.
- speaker extraído do ID (STR_DIALOGS_<cena>_D<n>_<SPEAKER>_<linha>).
- Tokens _100_/_300_/etc. e tags TMP <color=X> são preservados no CSV — o reinsert
  os escreve de volta verbatim.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)

# ---------------------------------------------------------------------------
# Escopo — Fase 0: diálogo de personagem com falante
# ---------------------------------------------------------------------------
_DIALOGUE_TABLES: dict[str, str] = {
    "texts_DIALOGS":        "8bbb65e6bcd747af3bbead6db0716968.bundle",
    "texts_INGAME_DIALOGS": "8d47b47a21c47126bf303e267a66fc73.bundle",
    "texts_SIDE_DIALOGS":   "a77305a96d09041b74e5948e4f67851e.bundle",
}

_CSV_DELIMITER = "~"
_ID_COL  = "::ID::"
_EN_COL  = "::EN::"

# STR_DIALOGS_CAVE_23_D1_BALOF_1 → BALOF
# STR_DIALOGS_CAVE_23_INTER_D1_BALOF_1 → BALOF
_SPEAKER_RE = re.compile(r"(?:_INTER)?_D\d+_([A-Z0-9]+)_\d+$", re.IGNORECASE)


def _parse_speaker(row_id: str) -> str:
    m = _SPEAKER_RE.search(row_id)
    return m.group(1).upper() if m else ""


def _resolve_data_dir(project_json: Path, cli_override: str | None) -> Path:
    """Resolve o diretório de dados do jogo: CLI > env var > project.json > falha."""
    return connector_io.resolve_source_path(
        cli_arg=cli_override, env_var="SOULDIERS_DATA_DIR",
        project_json=project_json, cfg_key="data_dir", exc=RuntimeError,
        error_hint=(
            "Caminho do jogo não encontrado. Defina SOULDIERS_DATA_DIR ou passe como argumento.\n"
            "Exemplo: python extract.py projects/souldiers "
            "C:\\Souldiers_Data\\StreamingAssets\\aa\\StandaloneWindows64"
        ),
    )


def extract(project_root: Path, data_dir: Path) -> int:
    """Extrai diálogos EN dos bundles e grava artifacts/dialogs.csv.

    Retorna o número de linhas extraídas.
    """
    try:
        import UnityPy
    except ImportError:
        raise ImportError(
            "UnityPy não instalado. Execute: pip install UnityPy\n"
            "Documentação: https://github.com/K0lb3/UnityPy"
        )
    import io

    artifacts = project_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    out_csv  = artifacts / "dialogs.csv"
    out_log  = artifacts / "extraction_log.md"

    rows: list[dict] = []
    log_lines: list[str] = ["# Extraction Log — Souldiers\n"]

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
                # texts_* às vezes tem o ::EN:: igual ao ::ID:: — placeholder de dev/lorem ipsum
                # nunca traduzido pelo estúdio, não é diálogo real (achado real: 73/2561 linhas,
                # inclui uma cena literalmente chamada LOREM_IPSUM). Tratar como vazio.
                if not row_id or not text_en or text_en == row_id:
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

    connector_io.write_dialogs_csv(out_csv, ["offset", "table", "text_en", "speaker"], rows)

    log_lines.append(f"\nTotal: {len(rows)} linhas extraídas\n")
    connector_io.write_extraction_log(out_log, "".join(log_lines))

    print(f"Extraido: {len(rows)} linhas -> {out_csv}")
    return len(rows)


def main():
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    project_json = project_root / "project.json"
    data_dir = _resolve_data_dir(project_json, data_dir_arg)
    extract(project_root, data_dir)


if __name__ == "__main__":
    main()
