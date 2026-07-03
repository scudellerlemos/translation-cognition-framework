"""test_progress_report.py — cobre a observabilidade de progresso do jogo inteiro (P2.5).

Puro/determinista: elapsed_s e passado explicitamente (nunca time.time() interno), entao os
testes nao precisam de monkeypatch de tempo.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import progress_report as pr  # noqa: E402


def _scene(root: Path, name: str, n_lines: int):
    d = root / "artifacts" / "scenes" / name
    d.mkdir(parents=True)
    rows = "\n".join(f"X:0:{i},linha {i}" for i in range(n_lines))
    (d / "dialogs.csv").write_text("offset,text_source\n" + rows + "\n", encoding="utf-8")


def _mark(root: Path, scene: str, status="verified", verified=True):
    p = paths.run_state(root)
    st = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"scenes": {}}
    st.setdefault("scenes", {})[scene] = {"status": status, "verified": verified}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st), encoding="utf-8")


def test_progress_pct_done_and_lines(tmp_path):
    _scene(tmp_path, "s1", 4)
    _scene(tmp_path, "s2", 6)
    _mark(tmp_path, "s1")
    rep = pr.report(tmp_path, ["s1", "s2"])
    assert rep["lines_total"] == 10 and rep["lines_verified"] == 4
    assert rep["pct_done"] == 40.0
    assert rep["scenes_verified"] == 1 and rep["scenes_total"] == 2


def test_progress_lines_per_min_from_elapsed(tmp_path):
    _scene(tmp_path, "s1", 60)
    _mark(tmp_path, "s1")
    rep = pr.report(tmp_path, ["s1"], elapsed_s=60.0)   # 60 linhas em 60s = 60 linhas/min
    assert rep["lines_per_min"] == 60.0
    assert rep["eta_s"] == 0.0   # tudo ja verified -> nada restando


def test_progress_failure_rate(tmp_path):
    _scene(tmp_path, "s1", 2)
    _scene(tmp_path, "s2", 2)
    _mark(tmp_path, "s1", status="verify_failed", verified=False)
    rep = pr.report(tmp_path, ["s1", "s2"])
    assert rep["failure_rate"] == 1.0   # 1 tentada (s1), 1 falhou; s2 nem tentada ainda


def test_progress_no_run_state_is_zero(tmp_path):
    _scene(tmp_path, "s1", 5)
    rep = pr.report(tmp_path, ["s1"])
    assert rep["pct_done"] == 0.0 and rep["scenes_verified"] == 0
    assert "lines_per_min" not in rep   # sem elapsed_s, nao calcula


def test_format_line_includes_eta_when_present():
    rep = {"scenes_verified": 1, "scenes_total": 2, "pct_done": 50.0, "lines_verified": 5,
           "lines_total": 10, "failure_rate": 0.0, "lines_per_min": 2.5, "eta_s": 120.0}
    line = pr.format_line(rep)
    assert "50.0%" in line and "2.5 linhas/min" in line and "ETA" in line
