"""test_espera_reset.py — a espera do limite de cota le o horario de liberacao nos formatos que o claude imprime."""
import sys
from datetime import datetime
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import espera_reset  # noqa: E402

AGORA = datetime(2026, 10, 19, 21, 0, 0)
M = espera_reset.MARGEM


def test_session_limit_same_day_and_next_day():
    assert espera_reset.segundos_ate_reset("You've hit your session limit · resets 11pm", AGORA) == 2 * 3600 + M
    assert espera_reset.segundos_ate_reset("You've hit your session limit · resets 2:30am", AGORA) == 5 * 3600 + 1800 + M


def test_weekly_limit_with_date():
    t = "You've hit your weekly limit · resets Oct 21, 9am"
    assert espera_reset.segundos_ate_reset(t, AGORA) == (36 * 3600) + M
    assert espera_reset.segundos_ate_reset("weekly limit reached, resets Oct 21 at 9am", AGORA) == 36 * 3600 + M


def test_legacy_epoch_format():
    ep = int(AGORA.timestamp()) + 600
    assert espera_reset.segundos_ate_reset(f"Claude AI usage limit reached|{ep}", AGORA) == 600 + M


def test_no_limit_message_returns_none():
    assert espera_reset.segundos_ate_reset("ONDA_OK: 6 cenas, 235 falas", AGORA) is None
    assert espera_reset.segundos_ate_reset("o roteiro diz resets 3pm", AGORA) is None      # sem a palavra limit
    assert espera_reset.segundos_ate_reset("hit your session limit", AGORA) is None        # limite sem horario
