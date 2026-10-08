"""test_batch_status.py — batch_status so REPORTA (nunca cancela) e avisa que 'succeeded' nao e tempo real."""
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import batch_status  # noqa: E402


def _batch(bid, status, age_min=135):
    return SimpleNamespace(id=bid, processing_status=status, request_counts="succeeded=0",
                           created_at=datetime.now(UTC) - timedelta(minutes=age_min))


class _FakeClient:
    """So expoe retrieve/list; qualquer cancel() estouraria AttributeError (garante 'nunca cancela')."""
    def __init__(self, batches):
        self._by_id = {b.id: b for b in batches}
        self.messages = SimpleNamespace(batches=SimpleNamespace(
            retrieve=lambda bid: self._by_id[bid], list=lambda limit: list(self._by_id.values())))


def test_age_formats_hours_and_minutes():
    assert batch_status._age(datetime.now(UTC) - timedelta(hours=2, minutes=5, seconds=10)) == "2h05m"


def test_report_one_in_progress_prints_the_warning(capsys):
    batch_status.report_one(_FakeClient([_batch("b1", "in_progress")]), "b1")
    out = capsys.readouterr().out
    assert "b1" in out and "status: in_progress" in out and "idade: 2h15m" in out
    assert "NAO cancelar por isso" in out


def test_report_one_ended_has_no_warning(capsys):
    batch_status.report_one(_FakeClient([_batch("b2", "ended")]), "b2")
    assert "AVISO" not in capsys.readouterr().out


def test_main_lists_only_in_progress(monkeypatch, capsys):
    client = _FakeClient([_batch("run1", "in_progress"), _batch("done1", "ended")])
    monkeypatch.setattr(batch_status, "_client", lambda: client)
    monkeypatch.setattr(sys, "argv", ["batch_status.py"])
    batch_status.main()
    out = capsys.readouterr().out
    assert "1 batch(es) in_progress" in out and "run1" in out and "done1" not in out


def test_main_without_in_progress(monkeypatch, capsys):
    monkeypatch.setattr(batch_status, "_client", lambda: _FakeClient([_batch("done1", "ended")]))
    monkeypatch.setattr(sys, "argv", ["batch_status.py"])
    batch_status.main()
    assert "Nenhum batch in_progress" in capsys.readouterr().out


def test_main_with_batch_id_reports_that_one(monkeypatch, capsys):
    monkeypatch.setattr(batch_status, "_client", lambda: _FakeClient([_batch("only", "ended")]))
    monkeypatch.setattr(sys, "argv", ["batch_status.py", "only"])
    batch_status.main()
    assert capsys.readouterr().out.startswith("only")
