#!/usr/bin/env python3
"""
test_roundtrip.py — TCF Demo

Oraculo do conector sintetico: reconstruir sem nenhuma traducao (approved={}) reproduz
connector/source.txt byte-a-byte. E o unico round-trip que este conector (formato de
demonstracao, sem binario real) precisa provar.

Uso: pytest projects/demo/connector/test_roundtrip.py -v
"""
import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import verify_chapter as V  # noqa: E402

ROOT = _HERE.parent
SCENE = "demo01"


def _load_dialogs() -> dict:
    dialogs = {}
    with (ROOT / "artifacts" / "scenes" / SCENE / "dialogs.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dialogs[row["offset"]] = row["text_en"]
    return dialogs


def test_roundtrip_sem_traducao_bate_com_source():
    dialogs = _load_dialogs()
    round_trip_ok, fitting_failure, fails = V._rebuild(SCENE, dialogs, {})
    assert round_trip_ok, "reconstrucao sem traducao deveria bater byte-a-byte com source.txt"
    assert fitting_failure is False
    assert any("sem traducao aprovada" in f for f in fails)  # approved={} -> todo offset falta


def test_cobertura_completa_nao_reporta_falha():
    dialogs = _load_dialogs()
    approved_completa = dict.fromkeys(dialogs, "traducao de teste")
    round_trip_ok, _, fails = V._rebuild(SCENE, dialogs, approved_completa)
    assert round_trip_ok
    assert fails == []


if __name__ == "__main__":
    test_roundtrip_sem_traducao_bate_com_source()
    test_cobertura_completa_nao_reporta_falha()
    print("OK: test_roundtrip.py (demo) passou.")
