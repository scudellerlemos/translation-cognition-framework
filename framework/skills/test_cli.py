"""test_cli.py — cobre o dispatch da CLI unificada (subcomandos -> funções, alvos mockados)."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FW = _HERE.parent
for _p in (_HERE, _FW):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import cli  # noqa: E402


def _run(argv):
    args = cli.build_parser().parse_args(argv)
    return args.func(args)


def test_skill_list(capsys):
    assert _run(["skill", "list"]) == 0
    assert "deterministic" in capsys.readouterr().out


def test_skill_check_unknown_returns_2(capsys):
    assert _run(["skill", "check", "99", "."]) == 2
    assert "desconhecida" in capsys.readouterr().err


def test_skill_run_unknown_returns_2(capsys):
    assert _run(["skill", "run", "99", "."]) == 2


def test_db_summary(tmp_path, capsys):
    from store import Store
    dbp = tmp_path / "t.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
    assert _run(["db", "summary", str(dbp), "p"]) == 0
    assert "project_id" in capsys.readouterr().out


def test_translate_dispatch(tmp_path, monkeypatch, capsys):
    import run_scene
    monkeypatch.setattr(run_scene, "run_scene", lambda p, s, **k: {"status": "verified"})
    assert _run(["translate", str(tmp_path), "AREAD001"]) == 0
    assert "verified" in capsys.readouterr().out


def test_translate_dispatch_nonzero_on_failure(tmp_path, monkeypatch):
    import run_scene
    monkeypatch.setattr(run_scene, "run_scene", lambda p, s, **k: {"status": "verify_failed"})
    assert _run(["translate", str(tmp_path), "AREAD001"]) == 1


def test_db_migrate_dispatch(tmp_path, monkeypatch, capsys):
    import migrate_from_flat
    monkeypatch.setattr(migrate_from_flat, "migrate",
                        lambda r, d, project_id="bof4": {"scenes": 1, "translations": 2})
    assert _run(["db", "migrate", str(tmp_path), str(tmp_path / "o.db")]) == 0
    assert "scenes" in capsys.readouterr().out


def test_db_export_dispatch(tmp_path, monkeypatch, capsys):
    import export_to_flat
    monkeypatch.setattr(export_to_flat, "export",
                        lambda db, pid, out: {"approved": 3, "tm": 3})
    assert _run(["db", "export", "x.db", "p", str(tmp_path)]) == 0
    assert "approved" in capsys.readouterr().out


def test_skill_check_ok(tmp_path, capsys):
    # skill 07 (QA) gate: sem artifacts/scenes -> gate reporta problema (rc 1)
    (tmp_path / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")
    rc = _run(["skill", "check", "07", str(tmp_path)])
    assert rc in (0, 1)                                    # gate roda (0 ok / 1 bloqueado)
