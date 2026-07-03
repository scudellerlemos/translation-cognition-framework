#!/usr/bin/env python3
"""
test_roundtrip.py — Souldiers

Gate obrigatório: rebuild_table(translations={}) reproduz cada bundle de diálogo byte-a-byte.
Grão mínimo aqui é a TABELA (3 bundles), não a cena — reinsert.py reescreve bundles inteiros,
não arquivos por-cena isoláveis (diferente do BoF4).

Precisa do jogo instalado: SOULDIERS_DATA_DIR ou --data-dir.

Uso: pytest connector/test_roundtrip.py -v
     pytest connector/test_roundtrip.py -v --data-dir "<caminho>"
"""
import os
from pathlib import Path

import pytest

import reinsert as R

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def data_dir(request):
    d = request.config.getoption("--data-dir") or os.environ.get("SOULDIERS_DATA_DIR")
    if not d:
        pytest.skip("SOULDIERS_DATA_DIR não definido e --data-dir não passado")
    p = Path(d)
    if not p.is_dir():
        pytest.skip(f"data_dir não encontrado: {p}")
    return p


@pytest.mark.parametrize("table_name,bundle_file", sorted(R._DIALOGUE_TABLES.items()))
def test_roundtrip_identity(data_dir, table_name, bundle_file):
    bundle_path = data_dir / bundle_file
    if not bundle_path.is_file():
        pytest.skip(f"bundle não encontrado: {bundle_path}")

    original = bundle_path.read_bytes()
    rt_bytes, n_changed = R.rebuild_table(table_name, bundle_path, {})

    assert n_changed == 0, f"{table_name}: translations vazio não deveria alterar nenhuma linha"
    assert rt_bytes == original, f"{table_name}: round-trip não é byte-idêntico"


@pytest.mark.parametrize("table_name,bundle_file", sorted(R._DIALOGUE_TABLES.items()))
def test_apply_then_readback(data_dir, table_name, bundle_file):
    """Aplica 1 tradução sintética e confirma que ela — e SÓ ela — é lida de volta."""
    bundle_path = data_dir / bundle_file
    if not bundle_path.is_file():
        pytest.skip(f"bundle não encontrado: {bundle_path}")

    original_rows = R.read_table(table_name, bundle_path.read_bytes())
    if not original_rows:
        pytest.skip(f"{table_name}: nenhuma linha lida do bundle original")

    target_id = next(iter(original_rows))
    probe = "PROBE_ROUNDTRIP_ãção"
    new_bytes, n_changed = R.rebuild_table(table_name, bundle_path, {target_id: probe})

    assert n_changed == 1
    new_rows = R.read_table(table_name, new_bytes)
    assert new_rows[target_id] == probe

    # nenhuma outra linha deveria ter mudado
    for rid, val in original_rows.items():
        if rid == target_id:
            continue
        assert new_rows.get(rid) == val, f"{table_name}: {rid} mudou sem ser tocada"
