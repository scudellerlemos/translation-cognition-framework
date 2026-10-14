"""`--help` dos scripts de linha de comando imprime o docstring e sai 0 (não trata como argumento)."""
import subprocess
import sys
from pathlib import Path

import pytest

_FW = Path(__file__).resolve().parents[1]
_SCRIPTS = [
    "runtime/connector_gate.py",
    "runtime/state_index.py",
    "runtime/box_width.py",
    "connectors/adversarial_validator.py",
    "connectors/_skeleton/verify_chapter.py",
]


@pytest.mark.parametrize("rel", _SCRIPTS)
def test_help_imprime_docstring(rel):
    r = subprocess.run([sys.executable, "-X", "utf8", str(_FW / rel), "--help"],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert r.returncode == 0, r.stderr
    assert Path(rel).name in r.stdout
