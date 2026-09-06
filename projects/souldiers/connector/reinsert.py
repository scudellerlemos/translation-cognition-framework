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
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FRAMEWORK_CONNECTORS = _HERE.parent.parent.parent / "framework" / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))
import connector_io  # noqa: E402  (utilitarios compartilhados entre conectores, #86)

_CSV_DELIMITER = "~"
_ID_COL = "::ID::"

_DIALOGUE_TABLES: dict[str, str] = {
    "texts_DIALOGS":        "8bbb65e6bcd747af3bbead6db0716968.bundle",
    "texts_INGAME_DIALOGS": "8d47b47a21c47126bf303e267a66fc73.bundle",
    "texts_SIDE_DIALOGS":   "a77305a96d09041b74e5948e4f67851e.bundle",
}

# Coluna de destino pt-BR NÃO é uniforme entre tabelas — descoberto rodando de verdade contra o
# jogo instalado (2026-07-02): texts_DIALOGS/INGAME_DIALOGS têm "::PT::" (Portugal); SIDE_DIALOGS
# não tem "::PT::" — só "::BR::" (Brasil). Usar "::BR::" ali é mais correto pra pt-BR, não é workaround.
_PT_COL_BY_TABLE: dict[str, str] = {
    "texts_DIALOGS":        "::PT::",
    "texts_INGAME_DIALOGS": "::PT::",
    "texts_SIDE_DIALOGS":   "::BR::",
}


def _resolve_data_dir(project_json: Path, cli_override: str | None) -> Path:
    """Resolve o diretório de dados do jogo: CLI > env var > project.json > falha."""
    return connector_io.resolve_source_path(
        cli_arg=cli_override, env_var="SOULDIERS_DATA_DIR",
        project_json=project_json, cfg_key="data_dir", exc=RuntimeError,
        error_hint="Caminho do jogo não encontrado. Defina SOULDIERS_DATA_DIR ou passe como argumento.",
    )


def _rewrite_csv_text(text: str, pt_col: str, translations: dict[str, str]) -> tuple[str, int]:
    """Aplica `translations` na coluna `pt_col` de um CSV ~-delimitado (lógica PURA, sem UnityPy/
    bundle — isolada aqui pra ser testável sem o jogo instalado, ver test_rebuild_table_logic.py).
    Retorna (novo texto CSV, nº de linhas alteradas)."""
    reader = csv.DictReader(io.StringIO(text), delimiter=_CSV_DELIMITER)
    fieldnames = reader.fieldnames or []
    rows = list(reader)
    changed = 0

    for row in rows:
        row_id = row.get(_ID_COL, "").strip().strip('"')
        if row_id in translations:
            row[pt_col] = translations[row_id]
            changed += 1

    out_buf = io.StringIO()
    writer = csv.DictWriter(out_buf, fieldnames=fieldnames,
                            delimiter=_CSV_DELIMITER, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)
    return out_buf.getvalue(), changed


def rebuild_table(table_name: str, bundle_path: Path, translations: dict[str, str]) -> tuple[bytes, int]:
    """Retorna (bytes do bundle com `translations` aplicadas na tabela `table_name`, nº de linhas
    dessa tabela efetivamente alteradas).

    translations={} -> bytes ORIGINAIS do arquivo, sem passar pelo UnityPy (fast-path de
    identidade). Reserializar via UnityPy mesmo sem mudança nenhuma NÃO garante round-trip
    byte-idêntico (reempacotamento pode reordenar/realinhar o container) — por isso a cópia crua
    é o único jeito seguro de provar round-trip. Usado por verify_chapter.py e test_roundtrip.py.
    """
    if not translations:
        return bundle_path.read_bytes(), 0

    import UnityPy
    pt_col = _PT_COL_BY_TABLE.get(table_name, "::PT::")
    env = UnityPy.load(str(bundle_path))
    table_changed = 0

    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        d = obj.read()
        if getattr(d, "m_Name", "") != table_name:
            continue

        text = d.m_Script
        was_bytes = isinstance(text, bytes)  # m_Script normalmente é str no Unity deste jogo;
        if was_bytes:                        # preservar o tipo original evita AttributeError no
            text = text.decode("utf-8", errors="replace")  # TypeTree writer do UnityPy ao salvar.

        new_text, table_changed = _rewrite_csv_text(text, pt_col, translations)

        d.m_Script = new_text.encode("utf-8") if was_bytes else new_text
        d.save()
        break

    buf = io.BytesIO()
    for file in env.file.files.values():
        buf.write(file.save())
    return buf.getvalue(), table_changed


def read_table(table_name: str, data: bytes) -> dict[str, str]:
    """Lê os bytes de um bundle (já modificado ou original) e retorna {::ID:: -> coluna PT/BR
    da tabela} — a coluna varia por tabela, ver _PT_COL_BY_TABLE. Usado por verify_chapter.py
    para conferir o que foi de fato gravado."""
    import UnityPy
    pt_col = _PT_COL_BY_TABLE.get(table_name, "::PT::")
    env = UnityPy.load(io.BytesIO(data))
    out: dict[str, str] = {}
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        d = obj.read()
        if getattr(d, "m_Name", "") != table_name:
            continue
        text = d.m_Script
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="replace")
        for row in csv.DictReader(io.StringIO(text), delimiter=_CSV_DELIMITER):
            row_id = row.get(_ID_COL, "").strip().strip('"')
            if row_id:
                out[row_id] = row.get(pt_col, "").strip().strip('"')
        break
    return out


def reinsert(project_root: Path, data_dir: Path) -> int:
    """Aplica as traduções aprovadas nos bundles e salva cópias em output/.

    Retorna o número de linhas reinseridas.
    """
    try:
        import UnityPy  # noqa: F401  (checagem antecipada de dependência; rebuild_table importa de novo)
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

        new_bytes, table_inserted = rebuild_table(table_name, bundle_path, translations)
        out_bundle = output_dir / bundle_file
        out_bundle.write_bytes(new_bytes)

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
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    data_dir_arg = sys.argv[2] if len(sys.argv) > 2 else None
    project_json = project_root / "project.json"
    data_dir = _resolve_data_dir(project_json, data_dir_arg)
    reinsert(project_root, data_dir)


if __name__ == "__main__":
    main()
