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


# --- S110 residuais: leituras de config/estado que engoliam tudo e agora estreitam + avisam -----------
def test_stale_connector_check_warns_when_run_state_unreadable(tmp_path, capsys):
    import connector_mgr
    rs = paths.run_state(tmp_path)
    rs.parent.mkdir(parents=True)
    rs.write_text("{nao e json", encoding="utf-8")
    connector_mgr._warn_if_connector_stale(tmp_path, "ch_01_01", {})
    assert "não consegui checar o hash" in capsys.readouterr().out


def test_print_cost_warns_instead_of_hiding_a_broken_report(tmp_path, monkeypatch, capsys):
    import run_chapter

    def boom(*_a, **_k):
        raise ValueError("ledger torto")
    monkeypatch.setattr(cost_report, "report", boom)
    run_chapter._print_cost(tmp_path, "01")            # nao pode derrubar o capitulo
    assert "resumo de gasto indisponivel" in capsys.readouterr().err


def test_metrics_warns_when_back_translation_unreadable(tmp_path, capsys):
    import run_scene
    bp = paths.back_translation(tmp_path, "ch_01_01", "01_01")
    bp.parent.mkdir(parents=True)
    bp.write_text("{nao e json", encoding="utf-8")
    paths.metrics(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    rec = run_scene._metrics(tmp_path, "ch_01_01", "01_01", n_lines=1, tr={}, bt={}, n_high=0, verified=True)
    assert rec["back_pass_rate"] is None
    assert "back_translation de ch_01_01 ilegivel" in capsys.readouterr().out


def test_build_tm_warns_when_scene_pack_unreadable(tmp_path, capsys):
    scene = tmp_path / "scenes" / "ch_01_01"
    scene.mkdir(parents=True)
    (scene / "translation_plan_01_01.json").write_text('{"lines": []}', encoding="utf-8")
    (scene / "pack.json").write_text("{nao e json", encoding="utf-8")
    assert state_index.build_tm(tmp_path) == []
    assert "doctrine_version vazio" in capsys.readouterr().out


# --- BLE001 que escondiam degradacao real ---------------------------------------------------------
def test_chapter_cost_warns_that_the_spend_cap_is_blind(tmp_path, monkeypatch, capsys):
    import run_chapter

    def boom(*_a, **_k):
        raise ValueError("run_state torto")
    monkeypatch.setattr(cost_report, "report", boom)
    assert run_chapter._chapter_cost(tmp_path, "01") == 0.0     # comportamento mantido (nao aborta)
    assert "--max-usd NAO esta sendo aplicado" in capsys.readouterr().err


def test_load_kb_warns_when_db_is_unreadable(tmp_path, capsys):
    import context_pack
    bad = tmp_path / "state.db"
    bad.write_bytes(b"isto nao e um sqlite")
    assert context_pack._load_kb(str(bad), "p") == []
    assert "KB indisponivel" in capsys.readouterr().out


def test_load_kb_without_db_is_silent(capsys):
    import context_pack
    assert context_pack._load_kb(None, "p") == []
    assert capsys.readouterr().out == ""


def test_verify_status_bad_json_is_empty_dict():
    import connector_mgr
    assert connector_mgr._verify_status("ok\nVERIFY_STATUS: {torto") == {}
    assert connector_mgr._verify_status('VERIFY_STATUS: {"a": 1}') == {"a": 1}
