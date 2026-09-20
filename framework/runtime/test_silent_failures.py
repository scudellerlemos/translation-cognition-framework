"""test_silent_failures.py — falhas que antes eram engolidas em silencio (`except ...: pass`) e agora
avisam: ledger que nao grava, linha corrompida no ledger, run_state/plan ilegivel, glossario ilegivel."""
import sys
import warnings
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import cost  # noqa: E402
import cost_report  # noqa: E402
import paths  # noqa: E402
import scene_lifecycle  # noqa: E402
import state_index  # noqa: E402
import tm_correct  # noqa: E402


def test_log_api_call_warns_when_ledger_append_fails(tmp_path, monkeypatch):
    def boom(*_a, **_k):
        raise OSError("disco cheio")
    monkeypatch.setattr(cost, "_ledger_append", boom)
    with pytest.warns(RuntimeWarning, match="NAO foi contabilizada"):
        rec = cost.log_api_call(tmp_path, "S1", "translate", "claude-opus-4-8", {"in": 10, "out": 5})
    assert rec is not None                       # nunca derruba a traducao por falha de log


def test_read_ledger_warns_on_corrupt_line_and_keeps_good_ones(tmp_path, capsys):
    lp = paths.ledger(tmp_path)
    lp.parent.mkdir(parents=True)
    lp.write_text('{"scene": "a", "cost_usd": 1.0}\n{truncado\n{"scene": "b", "cost_usd": 2.0}\n',
                  encoding="utf-8")
    rows = cost_report.read_ledger(tmp_path)
    assert [r["scene"] for r in rows] == ["a", "b"]
    assert "1 linha(s) ilegivel(is)" in capsys.readouterr().err


def test_clean_failed_scene_warns_when_run_state_unreadable(tmp_path, capsys):
    rs = paths.run_state(tmp_path)
    rs.parent.mkdir(parents=True)
    rs.write_text("{nao e json", encoding="utf-8")
    scene_lifecycle.clean_failed_scene(tmp_path, "ch_01_01")
    assert "run_state.json ilegivel" in capsys.readouterr().out


def test_tm_correct_collect_warns_on_unreadable_json(tmp_path, capsys):
    bad = tmp_path / "translations_01.json"
    bad.write_text("{nao e json", encoding="utf-8")
    hits: list = []
    tm_correct._collect(hits, bad, "ch_01_01", "01", "translations", "t",
                        tm_correct._iter_translations, [])
    assert hits == [] and "NAO corrigido" in capsys.readouterr().out


def test_validate_kb_format_reports_unreadable_glossary(tmp_path):
    gp = paths.glossary(tmp_path)
    gp.parent.mkdir(parents=True)
    gp.write_bytes(b"term,\xff\xfe\xfa\n")       # bytes invalidos em UTF-8
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        issues = state_index._validate_kb_format(tmp_path)
    assert any("glossary.csv ilegivel" in i for i in issues)
