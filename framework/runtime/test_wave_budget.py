"""Onda 3 (custo): teto de gasto por onda com parada dura, vindo de --max-usd ou de budget.max_usd_per_wave."""
import json
import sys
import time
import wave

import alerts
import paths
import pytest


def _projeto(tmp_path, budget=None):
    (tmp_path / "artifacts").mkdir()
    cfg = {"budget": {"max_usd_per_wave": budget}} if budget is not None else {}
    paths.project_json(tmp_path).write_text(json.dumps(cfg), encoding="utf-8")
    return tmp_path


def _gasta(root, usd, t=None):
    with open(paths.ledger(root), "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": t if t is not None else time.time() + 1, "scene": "s1", "kind": "x",
                             "model": "m", "usage": {}, "cost_usd": usd}) + "\n")


def test_teto_vem_do_cli_ou_do_project_json(tmp_path):
    root = _projeto(tmp_path, budget=5)
    assert wave.wave_budget(str(root), None) == 5.0
    assert wave.wave_budget(str(root), 2.0) == 2.0                # --max-usd vence
    sem = tmp_path / "sem"
    (sem / "artifacts").mkdir(parents=True)
    assert wave.wave_budget(str(sem), None) is None


def test_gasto_anterior_a_onda_nao_conta(tmp_path):
    root = _projeto(tmp_path)
    _gasta(root, 9.0, t=1.0)
    _gasta(root, 0.5, t=100.0)
    assert wave.spent_since(str(root), 50.0) == pytest.approx(0.5)


def test_onda_ja_acima_do_teto_nao_roda_o_proximo_passo(tmp_path, monkeypatch):
    root = _projeto(tmp_path)
    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: [])
    monkeypatch.setattr(wave, "steps", lambda *a, **k: [("glossary_lint", ["x.py"]), ("quality_gate", ["y.py"])])
    chamados = []

    def fake(argv, timeout, estourou=None):
        chamados.append(argv[-1])
        _gasta(root, 3.0)                                          # o 1o passo gasta acima do teto
        return wave.subprocess.CompletedProcess(argv, 0, "ok", "")

    monkeypatch.setattr(wave, "_executa", fake)
    assert wave.run(str(root), ["s1"], max_usd=1.0) == wave.BUDGET_RC
    assert len(chamados) == 1                                      # o 2o nem comecou
    (al,) = alerts.read(root)
    assert (al["step"], al["result"], al["rc"]) == ("quality_gate", "budget", wave.BUDGET_RC)


def test_passo_longo_e_morto_quando_o_gasto_passa_do_teto(tmp_path, monkeypatch):
    """Parada dura: o passo roda e gasta no meio; a onda mata o processo sem esperar ele terminar."""
    root = _projeto(tmp_path)
    monkeypatch.setattr(wave, "BUDGET_POLL", 0.2)
    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: [])
    script = tmp_path / "lento.py"
    script.write_text("import time\ntime.sleep(60)\n", encoding="utf-8")
    monkeypatch.setattr(wave, "steps", lambda *a, **k: [("run_scene", [str(script)])])
    monkeypatch.setattr(wave, "_HERE", tmp_path)
    monkeypatch.setattr(wave.sys, "executable", sys.executable)
    _gasta(root, 4.0, t=time.time() + 0.5)                         # aparece no ledger logo depois do inicio
    t0 = time.monotonic()
    assert wave.run(str(root), ["s1"], max_usd=1.0) == wave.BUDGET_RC
    assert time.monotonic() - t0 < 30                              # nao esperou os 60 s do passo
    assert alerts.read(root)[-1]["result"] == "budget"


def test_sem_teto_o_comportamento_e_o_de_sempre(tmp_path, monkeypatch):
    root = _projeto(tmp_path)
    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: [])
    monkeypatch.setattr(wave, "steps", lambda *a, **k: [("glossary_lint", ["x.py"])])
    visto = {}

    def fake(argv, timeout, estourou=None):
        visto["estourou"] = estourou
        return wave.subprocess.CompletedProcess(argv, 0, "ok", "")

    monkeypatch.setattr(wave, "_executa", fake)
    assert wave.run(str(root), ["s1"]) == 0
    assert visto["estourou"] is None
    assert alerts.read(root) == []
