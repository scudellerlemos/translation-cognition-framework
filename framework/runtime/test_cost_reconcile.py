"""Onda 3 (custo): conciliacao ledger x fatura do provedor."""
import json
import time

import cost_reconcile
import paths


def _ts(mes: str) -> float:
    return time.mktime(time.strptime(mes + "-15 12:00", "%Y-%m-%d %H:%M"))


def _projeto(tmp_path, linhas):
    (tmp_path / "artifacts").mkdir()
    paths.project_json(tmp_path).write_text("{}", encoding="utf-8")
    paths.ledger(tmp_path).write_text("".join(json.dumps(
        {"t": _ts(m), "scene": "s", "kind": "x", "model": "m", "usage": {}, "cost_usd": c}) + "\n" for m, c in linhas),
        encoding="utf-8")
    return tmp_path


def test_por_mes_soma_so_o_mes_certo(tmp_path):
    root = _projeto(tmp_path, [("2026-09", 1.0), ("2026-10", 2.0), ("2026-10", 0.5)])
    assert cost_reconcile.por_mes(root) == {"2026-09": 1.0, "2026-10": 2.5}


def test_conciliar_dentro_e_fora_da_tolerancia():
    r = cost_reconcile.conciliar({"2026-10": 10.2, "2026-09": 5.0}, {"2026-10": 10.0, "2026-09": 8.0})
    assert [(x["mes"], x["ok"]) for x in r] == [("2026-09", False), ("2026-10", True)]
    assert r[0]["dif_usd"] == -3.0


def test_mes_com_fatura_e_sem_ledger_diverge():
    (r,) = cost_reconcile.conciliar({}, {"2026-08": 4.0})
    assert not r["ok"] and r["ledger_usd"] == 0.0


def test_main_codigo_de_saida(tmp_path, monkeypatch, capsys):
    root = _projeto(tmp_path, [("2026-10", 10.0)])

    def roda(*args):
        monkeypatch.setattr(cost_reconcile.sys, "argv", ["cost_reconcile.py", str(root), *args])
        return cost_reconcile.main()

    assert roda("--invoice", "2026-10=10.1") == 0
    assert roda("--invoice", "2026-10=20") == 1
    assert "DIVERGE" in capsys.readouterr().out
    assert roda("--invoice", "outubro=20") == 2
