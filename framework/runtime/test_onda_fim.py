"""test_onda_fim.py — a linha final da onda vale mesmo com texto solto depois dela."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import onda_fim  # noqa: E402


def test_last_line_is_the_contract_line():
    assert onda_fim.linha_final("trabalho\nONDA_OK: 5 cenas, 375 falas") == "ONDA_OK: 5 cenas, 375 falas"


def test_text_after_the_contract_line_does_not_hide_it():
    out = "x\nONDA_OK: 2 cenas, 90 falas\n\nPronto! Resumo da onda...\nwarning: LF will be replaced by CRLF"
    assert onda_fim.linha_final(out) == "ONDA_OK: 2 cenas, 90 falas"


def test_parada_and_fim_are_recognised_and_the_last_one_wins():
    assert onda_fim.linha_final("ONDA_OK: 1 cenas, 5 falas\nPARADA: gate vermelho") == "PARADA: gate vermelho"
    assert onda_fim.linha_final("a\nFIM\n") == "FIM"


def test_quoted_or_embedded_mentions_do_not_count():
    assert onda_fim.linha_final("termino com `ONDA_OK: n`\n> ONDA_OK: 1\nver ONDA_OK acima") is None
    assert onda_fim.linha_final("FIMDA onda\nPARADAS demais") is None


def test_no_contract_line():
    assert onda_fim.linha_final("") is None
    assert onda_fim.linha_final("so texto\noutro") is None
