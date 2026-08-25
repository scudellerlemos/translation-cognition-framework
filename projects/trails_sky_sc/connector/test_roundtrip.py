#!/usr/bin/env python3
"""
test_roundtrip.py — Trails in the Sky 2nd Chapter

Gate obrigatório: rebuild_pac(translations={}) reproduz script_en.pac byte-a-byte contra a
instalação real do jogo. Grão mínimo aqui é o CONTÊINER INTEIRO (script_en.pac), não um .dat
isolado — reinsert.py reescreve o .pac inteiro (replace same-size dentro do buffer completo,
sem reempacotamento por-arquivo).

Precisa do jogo instalado: TRAILS_SKY_SC_DATA_DIR ou --data-dir.

Uso: pytest connector/test_roundtrip.py -v
     pytest connector/test_roundtrip.py -v --data-dir "<caminho>"
"""
import os
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import reinsert as R  # noqa: E402
from fpac_unpack import read_index  # noqa: E402

_SCRIPT_PAC = Path("pac") / "steam" / "script_en.pac"


@pytest.fixture(scope="module")
def data_dir(request):
    d = request.config.getoption("--data-dir") or os.environ.get("TRAILS_SKY_SC_DATA_DIR")
    if not d:
        pytest.skip("TRAILS_SKY_SC_DATA_DIR não definido e --data-dir não passado")
    p = Path(d)
    if not p.is_dir():
        pytest.skip(f"data_dir não encontrado: {p}")
    return p


@pytest.fixture(scope="module")
def pac_path(data_dir):
    p = data_dir / _SCRIPT_PAC
    if not p.is_file():
        pytest.skip(f"script_en.pac não encontrado: {p}")
    return p


def test_roundtrip_identity(pac_path):
    data, entries = read_index(pac_path)
    new_bytes, changed = R.rebuild_pac(data, entries, {}, {})
    assert changed == 0, "translations vazio não deveria alterar nenhuma string"
    assert new_bytes == data, "round-trip não é byte-idêntico"


def test_apply_then_readback(pac_path):
    """Aplica 1 tradução sintética e confirma que ela — e SÓ ela — é lida de volta."""
    data, entries = read_index(pac_path)
    original = R.read_scena_strings(data, entries)
    if not original:
        pytest.skip("nenhuma string extraída do .pac real")

    # probe >= _MIN_LEN e com espaco -- read_scena_strings re-varre com a heuristica de
    # extract.py; um probe curto/sem-espaco ficaria invisivel no re-scan (falso negativo do
    # helper de teste, nao do reinsert -- ver docstring de read_scena_strings).
    target_key = next(iter(original))
    budgets = {k: len(v) + 1 for k, v in original.items()}
    probe = "PROBE TEXT"

    new_bytes, changed = R.rebuild_pac(data, entries, {target_key: probe}, budgets)
    assert changed == 1

    new_strings = R.read_scena_strings(new_bytes, entries)
    assert new_strings[target_key] == probe

    for key, text in original.items():
        if key == target_key:
            continue
        assert new_strings.get(key) == text, f"{key} mudou sem ser tocada"
