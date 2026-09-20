"""test_run_chapter_edges.py — ramos de borda do driver de capítulo (guards, KB-gate no batch, fallback,
teto no pós-passe, gates de conector, audits e custo best-effort). Complementa test_run_chapter.py.
"""
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import run_chapter as rc  # noqa: E402

_OK_KB = {"problems": [], "hard_problems": [], "warnings": [], "pending_decisions": []}


@pytest.mark.parametrize("chap,msg", [("", "vazio"), ("1/2", "separador"), ("1\\2", "separador")])
def test_validate_chapter_arg_rejects_empty_and_path_separators(tmp_path, chap, msg):
    with pytest.raises(ValueError, match=msg):
        rc._validate_chapter_arg(tmp_path, chap)


def test_batch_phase_skips_scenes_blocked_by_kb_gate(tmp_path, monkeypatch, capsys):
    gates = {"a": {**_OK_KB, "hard_problems": ["KB vazia"]}, "b": {**_OK_KB, "problems": ["sem fronteira"]}}
    monkeypatch.setattr(rc.kb_gate, "check", lambda r, s: gates[s])
    monkeypatch.setattr(rc.M, "batch_translate", lambda r, s: pytest.fail("nada a submeter"))
    st, failed = rc._batch_phase(tmp_path, ["a", "b"], skip_kb_gate=False, allow_interactive_fallback=False)
    out = capsys.readouterr().out
    assert (st, failed) == ({}, False)
    assert "KB-gate, hard" in out and "KB vazia" in out and "sem fronteira" in out


def test_batch_phase_skip_kb_gate_bypasses_soft_but_not_hard(tmp_path, monkeypatch):
    gates = {"a": {**_OK_KB, "hard_problems": ["KB vazia"]}, "b": {**_OK_KB, "problems": ["sem fronteira"]}}
    monkeypatch.setattr(rc.kb_gate, "check", lambda r, s: gates[s])
    sent = []
    monkeypatch.setattr(rc.M, "batch_translate", lambda r, s: sent.append(list(s)) or {x: "written" for x in s})
    st, failed = rc._batch_phase(tmp_path, ["a", "b"], skip_kb_gate=True, allow_interactive_fallback=False)
    assert sent == [["b"]] and st == {"b": "written"} and failed is False


def test_batch_phase_failure_with_fallback_flag_continues_interactive(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc.kb_gate, "check", lambda r, s: _OK_KB)

    def boom(r, s):
        raise RuntimeError("rede")
    monkeypatch.setattr(rc.M, "batch_translate", boom)
    st, failed = rc._batch_phase(tmp_path, ["a"], skip_kb_gate=False, allow_interactive_fallback=True)
    assert (st, failed) == ({}, False)
    assert "caindo p/ caminho interativo" in capsys.readouterr().out


def test_back_batch_phase_empty_and_failure_and_partial(tmp_path, monkeypatch, capsys):
    assert rc._back_batch_phase(tmp_path, []) == []

    def boom(r, s):
        raise RuntimeError("api fora")
    monkeypatch.setattr(rc.M, "batch_back_translate", boom)
    assert rc._back_batch_phase(tmp_path, ["a", "b"]) == ["a", "b"]           # tudo pendente, nao bloqueia
    assert "back-translation segue pendente" in capsys.readouterr().out

    monkeypatch.setattr(rc.M, "batch_back_translate", lambda r, s: {"a": "reviewed", "b": "parse_failed"})
    assert rc._back_batch_phase(tmp_path, ["a", "b"]) == ["b"]                 # so devolve as sem back concluido


def _post(root, **kw):
    args = {"no_back": False, "require_back": False, "max_usd": None}
    args.update(kw)
    return rc._post_pass(root, [], "12", **args)


def test_post_pass_no_back_is_skipped(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc, "_rebuild_index_phase", lambda root: None)
    assert _post(tmp_path, no_back=True) == []
    assert "pulado (--no-back)" in capsys.readouterr().out


def test_post_pass_budget_reached_skips_back_batch(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc, "_rebuild_index_phase", lambda root: None)
    monkeypatch.setattr(rc, "_chapter_cost", lambda root, chap: 5.0)
    monkeypatch.setattr(rc, "_back_batch_phase", lambda root, sc: pytest.fail("teto atingido"))
    assert _post(tmp_path, max_usd=1.0) == []
    assert "teto de gasto atingido" in capsys.readouterr().out


def test_post_pass_require_back_overrides_no_back(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc, "_rebuild_index_phase", lambda root: None)
    monkeypatch.setattr(rc, "_back_batch_phase", lambda root, sc: ["pendente"])
    assert _post(tmp_path, no_back=True, require_back=True) == ["pendente"]
    assert "--no-back ignorado" in capsys.readouterr().out


def test_connector_blocked_hard_problem_runs_audits_and_returns_status(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc.connector_gate, "check",
                        lambda r: {"hard_problems": ["sem build_plan"], "problems": ["sem round-trip"],
                                   "warnings": ["sem test_roundtrip"]})
    audited = []
    monkeypatch.setattr(rc, "_run_mandatory_audits", lambda root, chap: audited.append(chap))
    r = rc._connector_blocked(tmp_path, "12", None, skip_connector_gate=True)
    out = capsys.readouterr().out
    assert r == {"chapter": "12", "scenes": [], "status": "connector_incomplete"}
    assert audited == ["12"] and "sem build_plan" in out and "sem round-trip" not in out   # skip nao vale p/ hard
    assert "aviso: sem test_roundtrip" in out


def test_connector_blocked_soft_problem_suggests_skip_flag_and_glob_audits_whole_project(
        tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc.connector_gate, "check",
                        lambda r: {"hard_problems": [], "problems": ["sem round-trip"], "warnings": []})
    audited = []
    monkeypatch.setattr(rc, "_run_mandatory_audits", lambda root, chap: audited.append(chap))
    assert rc._connector_blocked(tmp_path, "rotulo", "ch_*", False)["status"] == "connector_incomplete"
    assert audited == [None] and "--skip-connector-gate" in capsys.readouterr().out


def test_connector_not_blocked_when_only_soft_and_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(rc.connector_gate, "check",
                        lambda r: {"hard_problems": [], "problems": ["sem round-trip"], "warnings": []})
    assert rc._connector_blocked(tmp_path, "12", None, True) is None


def test_chapter_cost_returns_total(tmp_path, monkeypatch):
    monkeypatch.setattr(rc.cost_report, "report", lambda r, chapter=None: {"total_usd": 1.25})
    assert rc._chapter_cost(tmp_path, "12") == 1.25


@pytest.mark.parametrize("rep,needle", [
    ({"revise": [1], "uncovered": []}, "ALERTA: 1 linha"),
    ({"revise": [], "uncovered": [1, 2]}, "2 linha(s) high/critical sem cobertura"),
    ({"revise": [], "uncovered": []}, "OK: nenhuma linha"),
])
def test_audit_quality_reports_each_outcome(tmp_path, monkeypatch, capsys, rep, needle):
    monkeypatch.setattr(rc.quality_gate, "check", lambda r, c: rep)
    rc._audit_quality(tmp_path, "12")
    assert needle in capsys.readouterr().out


def test_audit_quality_failure_only_warns(tmp_path, monkeypatch, capsys):
    def boom(r, c):
        raise RuntimeError("csv ruim")
    monkeypatch.setattr(rc.quality_gate, "check", boom)
    rc._audit_quality(tmp_path, None)
    assert "AVISO: falha ao auditar" in capsys.readouterr().out


def test_export_qa_failure_only_warns(tmp_path, monkeypatch, capsys):
    def boom(r, c):
        raise ImportError("openpyxl")
    monkeypatch.setattr(rc.quality_review, "export", boom)
    rc._export_qa(tmp_path, "12")
    out = capsys.readouterr().out
    assert "falha ao gerar o XLSX" in out and "quality_review.py export <projeto> 12" in out


def test_print_cost_prints_summary_only_when_there_are_calls(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rc.cost_report, "report", lambda r, chapter=None: {"n_calls": 0})
    rc._print_cost(tmp_path, "12")
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(rc.cost_report, "report", lambda r, chapter=None: {"n_calls": 2})
    monkeypatch.setattr(rc.cost_report, "_fmt", lambda rep, by_scene: "RESUMO-DE-GASTO")
    rc._print_cost(tmp_path, "12")
    assert "RESUMO-DE-GASTO" in capsys.readouterr().out
