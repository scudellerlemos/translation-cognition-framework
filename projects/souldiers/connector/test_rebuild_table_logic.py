#!/usr/bin/env python3
"""
test_rebuild_table_logic.py — Souldiers

Cobre `reinsert._rewrite_csv_text` (a lógica de aplicar traduções na coluna PT/BR de um CSV
~-delimitado) SEM UnityPy nem bundle real — roda SEMPRE na CI, com ou sem o jogo instalado.

Escopo (honesto): isto NÃO é o oráculo de round-trip byte-idêntico do container Unity (esse
continua em test_roundtrip.py, que exige SOULDIERS_DATA_DIR e o bundle comercial — UnityPy só lê
bundles reais, `BundleFile.__init__` exige um `EndianBinaryReader` de bytes já existentes; não há
API para criar um bundle do zero, então uma fixture sintética completa como a do BoF4
(test_roundtrip_synthetic.py) não é viável aqui sem reimplementar o formato binário UnityFS à mão).
O que ESTE teste garante sempre na CI: a reescrita da tabela CSV interna — que é onde bugs reais de
tradução aconteceriam (coluna errada, linha trocada, quoting quebrado) — está correta.

Uso: pytest connector/test_rebuild_table_logic.py -v
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import reinsert as R  # noqa: E402

_HEADER = '::ID::~::EN::~::PT::~::BR::\n'
_SAMPLE_CSV = (
    _HEADER +
    'STR_DIALOGS_CAVE_23_D1_BALOF_1~"Hello there."~"Hello there."~""\n'
    'STR_DIALOGS_CAVE_23_D1_BALOF_2~"Goodbye."~"Goodbye."~""\n'
)


def test_rewrite_applies_only_targeted_row():
    new_text, changed = R._rewrite_csv_text(
        _SAMPLE_CSV, "::PT::", {"STR_DIALOGS_CAVE_23_D1_BALOF_1": "Olá."})
    assert changed == 1
    assert '"Olá."' in new_text
    assert '"Goodbye."' in new_text            # linha 2 preservada
    assert new_text.count("Hello there.") == 1  # só na coluna EN original, não sobrescreveu


def test_rewrite_preserves_untouched_rows_verbatim():
    new_text, changed = R._rewrite_csv_text(_SAMPLE_CSV, "::PT::", {})
    assert changed == 0
    # reconstrói e relê pra comparar por conteudo (nao por bytes -- csv.QUOTE_ALL pode re-quotar
    # diferente do original; a garantia de round-trip byte-a-byte fica com o fast-path de
    # `rebuild_table` (translations={} -> read_bytes() cru), nao com esta funcao pura)
    import csv
    import io
    before = list(csv.DictReader(io.StringIO(_SAMPLE_CSV), delimiter="~"))
    after = list(csv.DictReader(io.StringIO(new_text), delimiter="~"))
    assert before == after


def test_rewrite_respects_per_table_pt_vs_br_column():
    # SIDE_DIALOGS usa ::BR::, nao ::PT:: (ver reinsert._PT_COL_BY_TABLE) -- escrever na coluna
    # errada e um bug real e silencioso (traducao "aplicada" mas nunca lida pelo jogo).
    pt_col = R._PT_COL_BY_TABLE["texts_SIDE_DIALOGS"]
    assert pt_col == "::BR::"
    new_text, changed = R._rewrite_csv_text(
        _SAMPLE_CSV, pt_col, {"STR_DIALOGS_CAVE_23_D1_BALOF_1": "Fala lida"})
    assert changed == 1
    import csv
    import io
    rows = list(csv.DictReader(io.StringIO(new_text), delimiter="~"))
    assert rows[0]["::BR::"] == "Fala lida"
    assert rows[0]["::PT::"] == "Hello there."   # coluna PT intocada


def test_rewrite_ignores_unknown_row_id():
    new_text, changed = R._rewrite_csv_text(_SAMPLE_CSV, "::PT::", {"ID_INEXISTENTE": "x"})
    assert changed == 0
    assert "x" not in new_text
