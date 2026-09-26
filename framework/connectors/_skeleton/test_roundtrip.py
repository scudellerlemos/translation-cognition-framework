"""
test_roundtrip.py — testes de contrato do conector (genérico, data-driven)

Copiado para projects/<título>/connector/ pelo scaffold_project.py (o connector_gate avisa se
este arquivo faltar). Verifica, antes de qualquer tradução:
  1. Round-trip byte-idêntico contra o binário REAL (extract → reinsert com alvo = fonte = original)
  2. Nenhum texto da obra hardcoded nos .py do conector
  3. Nenhum caminho absoluto hardcoded nos .py do conector

O round-trip roda numa CÓPIA do projeto em tmp_path — nunca sobrescreve artifacts/ nem output/
reais (approved_translations.csv do projeto não é tocado). O oráculo sempre ativo em CI, sem o
binário real, é o test_roundtrip_synthetic.py.

Rodar: pytest connector/ -v [--source-binary <caminho>]
"""
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CONNECTOR = Path(__file__).resolve().parent
PROJECT_ROOT = CONNECTOR.parent                      # projects/<título>/


def _cfg() -> dict:
    pj = PROJECT_ROOT / "project.json"
    return json.loads(pj.read_text(encoding="utf-8")) if pj.is_file() else {}


def _extracted_csv() -> Path | None:
    cfg = _cfg()
    p = PROJECT_ROOT / cfg["source"]["file"] if cfg.get("source") else None
    return p if p and p.is_file() else None


@pytest.fixture
def source_binary(request) -> Path:
    cli = request.config.getoption("--source-binary", default=None)
    declared = (_cfg().get("connector") or {}).get("source_binary", "")
    src = Path(cli) if cli else (PROJECT_ROOT / declared if declared else None)
    if src is None or not src.is_file():
        pytest.skip("binário-fonte ausente — passe --source-binary ou declare connector.source_binary")
    return src


def _run(script: str, root: Path, src: Path) -> None:
    r = subprocess.run(
        [sys.executable, str(root / "connector" / script), str(root / "project.json"), str(src)],
        capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, f"{script} falhou:\n{r.stdout}\n{r.stderr}"


def test_round_trip_byte_identical(source_binary, tmp_path):
    """extract → reinsert (alvo = texto-fonte) deve reproduzir o binário original byte a byte."""
    cfg = _cfg()
    root = tmp_path / "proj"
    shutil.copytree(CONNECTOR, root / "connector", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(PROJECT_ROOT / "project.json", root / "project.json")
    (root / "artifacts").mkdir()

    _run("extract.py", root, source_binary)
    dialogs = root / cfg["source"]["file"]
    assert dialogs.is_file(), "extract.py não gerou o CSV declarado em source.file"
    rows = list(csv.DictReader(dialogs.open(encoding="utf-8")))
    assert rows, "extract.py não extraiu nenhuma string"

    id_col = cfg["source"]["id_column"]
    with (root / "artifacts" / "approved_translations.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[id_col, "text_target"])
        w.writeheader()
        w.writerows({id_col: r[id_col], "text_target": r["text_source"]} for r in rows)

    _run("reinsert.py", root, source_binary)
    out = root / "output" / source_binary.name
    assert out.is_file(), "reinsert.py não gerou output/<nome-original>"
    assert out.read_bytes() == source_binary.read_bytes(), (
        "Round-trip FALHOU — o conector está perdendo informação. Rodar vbindiff original x saída "
        "antes de debugar no código; corrigir antes de traduzir qualquer linha.")


def test_dialogs_csv_has_required_columns():
    """O CSV extraído deve ter id_column, text_source e byte_budget."""
    extracted = _extracted_csv()
    if extracted is None:
        pytest.skip("CSV de extração ainda não existe — rode extract.py primeiro")
    with extracted.open(newline="", encoding="utf-8") as f:
        cols = csv.DictReader(f).fieldnames or []
    for c in (_cfg()["source"]["id_column"], "text_source", "byte_budget"):
        assert c in cols, f"CSV extraído falta coluna {c!r}; tem: {cols}"


def test_no_hardcoded_work_text_in_connector_scripts():
    """Scripts são determinísticos e leem frases de artefatos (CSV/JSON): falha se qualquer
    string extraída aparecer num .py do conector."""
    extracted = _extracted_csv()
    if extracted is None:
        pytest.skip("CSV de extração ainda não existe — rode extract.py primeiro")
    with extracted.open(newline="", encoding="utf-8") as f:
        texts = {r["text_source"].strip().lower() for r in csv.DictReader(f)
                 if (r.get("text_source") or "").strip()}
    for py_file in CONNECTOR.glob("*.py"):
        source = py_file.read_text(encoding="utf-8", errors="replace").lower()
        for text in texts:
            if len(text) > 8 and text in source:
                pytest.fail(f"{py_file.name} contém texto da obra hardcoded: {text[:60]!r}")


def test_no_hardcoded_paths_in_connector_scripts():
    """Scripts do conector não devem ter caminhos absolutos hardcoded."""
    abs_path_rx = re.compile(r'(?<![A-Za-z])[A-Za-z]:\\|/home/|/Users/|/root/')
    for py_file in CONNECTOR.glob("*.py"):
        if py_file.name.startswith(("test_", "conftest")):  # testes podem ter regex com padrões de path
            continue
        for i, line in enumerate(py_file.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not line.strip().startswith("#") and abs_path_rx.search(line):
                pytest.fail(f"{py_file.name}:{i} — caminho absoluto hardcoded: {line.strip()!r}")
