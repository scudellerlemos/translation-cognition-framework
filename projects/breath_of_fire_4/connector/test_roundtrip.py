"""
test_roundtrip.py — testes de contrato do conector (Breath of Fire IV)

Adaptado de framework/connectors/_skeleton/test_connector_contract.py.

Status: FASE 00 — os testes de round-trip ficam em skip até o binário ser
fornecido e o conector implementado. Os testes de integridade de código
(sem texto hardcoded, sem caminhos absolutos) já estão ativos.

Rodar: pytest connector/test_roundtrip.py -v
"""

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_BINARY = PROJECT_ROOT / "artifacts" / "dialogs.csv"  # atualizar p/ o binário real
EXTRACT_SCRIPT = PROJECT_ROOT / "connector" / "extract.py"
REINSERT_SCRIPT = PROJECT_ROOT / "connector" / "reinsert.py"
DIALOGS_CSV = PROJECT_ROOT / "artifacts" / "dialogs.csv"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


@pytest.mark.skip(reason="FASE 00 — mapear conector antes de habilitar (ver table_schema.md)")
def test_round_trip_byte_identical():
    """extract → reinsert sem tradução deve ser byte-idêntico ao original."""
    # Habilitar após:
    #  1. Mapear charset em connector/table_schema.md
    #  2. Implementar load_table e iter_string_offsets em extract.py
    #  3. Implementar encode_string em reinsert.py
    #  4. Atualizar SOURCE_BINARY acima para o binário real
    pass


@pytest.mark.skip(reason="FASE 00 — dialogs.csv ainda não existe")
def test_dialogs_csv_has_required_columns():
    """dialogs.csv deve ter colunas offset, text_en, byte_budget."""
    assert DIALOGS_CSV.exists()
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
    assert "offset" in cols
    assert "byte_budget" in cols
    assert any(c.startswith("text_") for c in cols)


def test_no_hardcoded_work_text_in_connector_scripts():
    """Nenhum script .py do conector deve conter texto da obra hardcoded.

    Ativo mesmo antes de ter dialogs.csv — verifica invariante estrutural.
    Quando dialogs.csv existir, será data-driven.
    """
    if not DIALOGS_CSV.exists():
        # sem corpus ainda — só verifica que os scripts existem
        assert EXTRACT_SCRIPT.exists(), "extract.py não encontrado"
        assert REINSERT_SCRIPT.exists(), "reinsert.py não encontrado"
        return

    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        text_cols = [c for c in (reader.fieldnames or []) if c.startswith("text_")]
        texts = {row[col].strip().lower() for row in reader for col in text_cols if row.get(col, "").strip()}

    connector_dir = PROJECT_ROOT / "connector"
    for py_file in connector_dir.glob("*.py"):
        source = py_file.read_text(encoding="utf-8", errors="replace").lower()
        for text in texts:
            if len(text) > 8 and text in source:
                pytest.fail(f"{py_file.name} contém texto da obra hardcoded: {text[:60]!r}")


def test_no_hardcoded_paths_in_connector_scripts():
    """Scripts do conector não devem ter caminhos absolutos hardcoded."""
    import re
    abs_path_rx = re.compile(r'(?:[A-Za-z]:\\|/home/|/Users/|/root/)')
    connector_dir = PROJECT_ROOT / "connector"
    for py_file in connector_dir.glob("*.py"):
        if py_file.name.startswith("test_"):  # os próprios testes podem ter regex com padrões de path
            continue
        source = py_file.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(source.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if abs_path_rx.search(line):
                pytest.fail(f"{py_file.name}:{i} — caminho absoluto hardcoded: {line.strip()!r}")
