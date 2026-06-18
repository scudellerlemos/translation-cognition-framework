"""
test_connector_contract.py — testes de contrato do conector (genérico, data-driven)

Copiar para projects/<título>/connector/test_roundtrip.py e adaptar as constantes
marcadas com # ADAPTAR.

Verifica que o conector implementa corretamente a interface do framework antes de
qualquer tradução:
  1. Round-trip byte-idêntico (extract → reinsert-sem-tradução = original)
  2. Nenhum texto da obra hardcoded nos .py do conector
  3. Nenhum caminho de input hardcoded nos .py do conector

Rodar: pytest connector/test_roundtrip.py -v
"""

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# ADAPTAR — caminhos relativos à raiz do projeto
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent          # projects/<título>/
SOURCE_BINARY = PROJECT_ROOT / "artifacts" / "DIALOG.BIN"   # ADAPTAR
EXTRACT_SCRIPT = PROJECT_ROOT / "connector" / "extract.py"
REINSERT_SCRIPT = PROJECT_ROOT / "connector" / "reinsert.py"
DIALOGS_CSV = PROJECT_ROOT / "artifacts" / "dialogs.csv"
OUTPUT_BINARY = PROJECT_ROOT / "output" / "DIALOG.BIN"      # ADAPTAR
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


@pytest.mark.skipif(not SOURCE_BINARY.exists(), reason="binário fonte ausente (forneça o arquivo)")
def test_round_trip_byte_identical(tmp_path):
    """extract → reinsert-sem-tradução deve reproduzir o binário original byte a byte."""
    subprocess.run(
        [sys.executable, str(EXTRACT_SCRIPT), str(SOURCE_BINARY)],
        check=True, capture_output=True, text=True,
    )
    assert DIALOGS_CSV.exists(), "extract.py não gerou dialogs.csv"

    subprocess.run(
        [sys.executable, str(REINSERT_SCRIPT), str(DIALOGS_CSV)],
        check=True, capture_output=True, text=True,
    )
    assert OUTPUT_BINARY.exists(), "reinsert.py não gerou o arquivo de saída"

    assert _sha256(SOURCE_BINARY) == _sha256(OUTPUT_BINARY), (
        "Round-trip FALHOU — o conector está perdendo informação. "
        "Corrigir antes de traduzir qualquer linha."
    )


@pytest.mark.skipif(not SOURCE_BINARY.exists(), reason="binário fonte ausente")
def test_dialogs_csv_has_required_columns():
    """dialogs.csv deve ter as colunas offset, text_<lang> e byte_budget."""
    assert DIALOGS_CSV.exists(), "extract.py deve ser rodado antes deste teste"
    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
    assert "offset" in cols, f"dialogs.csv falta coluna 'offset'; tem: {cols}"
    assert "byte_budget" in cols, f"dialogs.csv falta coluna 'byte_budget'; tem: {cols}"
    text_cols = [c for c in cols if c.startswith("text_")]
    assert text_cols, f"dialogs.csv falta coluna 'text_<lang>'; tem: {cols}"


def test_no_hardcoded_work_text_in_connector_scripts():
    """Nenhum script .py do conector deve conter texto da obra hardcoded.

    Regra: scripts são determinísticos e leem frases de artefatos (CSV/JSON).
    Falha se qualquer string de dialogs.csv aparecer num .py do conector.
    """
    if not DIALOGS_CSV.exists():
        pytest.skip("dialogs.csv não existe ainda — rode extract.py primeiro")

    with open(DIALOGS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        text_cols = [c for c in (reader.fieldnames or []) if c.startswith("text_")]
        texts = {row[col].strip().lower() for row in reader for col in text_cols if row.get(col, "").strip()}

    connector_dir = PROJECT_ROOT / "connector"
    for py_file in connector_dir.glob("*.py"):
        source = py_file.read_text(encoding="utf-8", errors="replace").lower()
        for text in texts:
            if len(text) > 8 and text in source:
                pytest.fail(
                    f"{py_file.name} contém texto da obra hardcoded: {text[:60]!r}"
                )


def test_no_hardcoded_paths_in_connector_scripts():
    """Scripts do conector não devem ter caminhos absolutos hardcoded."""
    import re
    connector_dir = PROJECT_ROOT / "connector"
    # padrão: caminho absoluto Windows ou Unix
    abs_path_rx = re.compile(r'(?:[A-Za-z]:\\|/home/|/Users/|/root/)')
    for py_file in connector_dir.glob("*.py"):
        if py_file.name.startswith("test_"):  # os próprios testes podem ter regex com padrões de path
            continue
        source = py_file.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(source.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if abs_path_rx.search(line):
                pytest.fail(
                    f"{py_file.name}:{i} — caminho absoluto hardcoded: {line.strip()!r}"
                )
