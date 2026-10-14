"""test_budget.py — a conta de bytes e uma so: model, tools locais e verify usam budget.py."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import budget as b  # noqa: E402
import model  # noqa: E402

TOK = re.compile(r"\[[0-9a-f]{2}\]")


def test_translit_vs_utf8_metric():
    assert b.budget_len("ação", {}) == 4                                    # transliterado: sem acento
    assert b.budget_len("ação", {"target_charset_supported": True}) == 6    # utf-8 real: ç e ã custam 2
    assert b.budget_len("ação", {"target_charset_supported": "sim"}) == 4  # so True estrito conta utf-8


def test_terminator_and_zero_budget():
    pc = {"budget_reserves_terminator": True}
    assert not b.over_budget("abcd", 5, pc) and b.over_budget("abcde", 5, pc)   # cabe em budget-1
    assert b.over_budget("a", 0) and not b.over_budget("a", None)


def test_token_counts_one_byte_when_rx_given():
    assert b.budget_len("[07][04]ok", {}) == 10 and b.budget_len("[07][04]ok", {}, TOK) == 4


def test_exception_overrides_budget():
    cfg = {"byte_budget_exceptions": {"0x10": 12}}
    assert b.effective_budget("0x10", 11, cfg) == 12 and b.effective_budget("0x20", 11, cfg) == 11


def test_model_delegates_to_budget():
    for t, pc, bud in (("ação!", {}, 5), ("ação!", {"target_charset_supported": True}, 5)):
        assert model._budget_len(t, pc) == b.budget_len(t, pc)
        assert model._over_budget(t, bud, pc, 1.0) == b.over_budget(t, bud, pc, 1.0)
