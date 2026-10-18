"""Onda 3 (observabilidade): schema dos eventos validado, indicadores definidos e alerta de falha de onda."""
import ast
import http.server
import json
import threading
import wave
from pathlib import Path

import alerts
import events
import obs_report
import paths
import pytest

RUNTIME = Path(__file__).resolve().parent


def _ok(**kw):
    return {"t": 1.0, "run": "r", "scene": None, "stage": "scene", "result": "verified", **kw}


# ---- schema -----------------------------------------------------------------------------------------------
def test_evento_valido_e_invalidos():
    assert events.validate(_ok()) == []
    assert events.validate(_ok(stage="gate.novo")) == []                       # familia aberta
    assert events.validate({k: v for k, v in _ok().items() if k != "run"})
    assert any("desconhecida" in p for p in events.validate(_ok(stage="inventada")))
    assert any("escalar" in p for p in events.validate(_ok(lista=[1, 2])))
    assert any("nao carrega texto" in p for p in events.validate(_ok(msg="x" * 201)))
    assert events.validate(_ok(t=True))                                        # bool nao e numero
    assert any("scene" in p for p in events.validate({k: v for k, v in _ok().items() if k != "scene"}))


def test_emit_fora_do_schema_avisa_mas_nao_perde_o_evento(tmp_path, capsys):
    (tmp_path / "artifacts").mkdir()
    events.emit(tmp_path, "inventada", "ok")
    assert "fora do schema" in capsys.readouterr().out
    assert len(events.read(tmp_path)) == 1


def _chamadas_de_evento():
    for p in sorted(RUNTIME.glob("*.py")):
        if p.name.startswith("test_"):
            continue
        for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("emit", "stage") \
                    and isinstance(n.func.value, ast.Name) and n.func.value.id == "events" and len(n.args) >= 2:
                a = n.args[1]
                yield p.name, a.value if isinstance(a, ast.Constant) else None


def test_toda_etapa_emitida_no_codigo_esta_no_schema():
    """Etapa nova no codigo sem entrar em events.ETAPAS (ou numa familia gate./audit.) falha aqui."""
    achadas = list(_chamadas_de_evento())
    assert len(achadas) >= 10, "o scanner nao achou as chamadas de events.emit/stage"
    fora = sorted({(f, s) for f, s in achadas if isinstance(s, str) and s not in events.ETAPAS
                   and not s.startswith(events.FAMILIAS)})
    assert not fora, f"etapa fora do schema: {fora}"


# ---- indicadores -------------------------------------------------------------------------------------------
def test_indicadores_taxa_de_sucesso_e_custo_por_cena():
    evs = [_ok(scene="a", result="verified"), _ok(scene="b", result="build_plan_failed"),
           _ok(scene="c", result="awaiting_translation"), _ok(scene="d", result="verified")]
    scenes = {n: {"status": s, "cost_usd": c, "session_equiv_usd": e} for n, s, c, e in
              (("a", "verified", 0.1, 0.0), ("b", "failed", 0.2, 0.0), ("d", "verified", 0.0, 0.3))}
    ind = obs_report.indicators(evs, scenes)
    assert ind["wave_success_rate"] == pytest.approx(2 / 3, abs=1e-3)      # awaiting fica fora da conta
    assert ind["cost_per_scene_usd"] == pytest.approx(0.3, abs=1e-4)       # (0,1+0,2+0,3) / 2 verified
    vazio = obs_report.indicators([], {})
    assert vazio["wave_success_rate"] is None and vazio["cost_per_scene_usd"] is None


# ---- alerta ------------------------------------------------------------------------------------------------
def _projeto(tmp_path):
    (tmp_path / "artifacts").mkdir()
    return tmp_path


def test_notify_grava_evento_e_alerts_jsonl(tmp_path, monkeypatch):
    monkeypatch.delenv(alerts.WEBHOOK_ENV, raising=False)
    root = _projeto(tmp_path)
    alerts.notify(root, "quality_gate", "failed", "s1", 1)
    (rec,) = alerts.read(root)
    assert (rec["step"], rec["result"], rec["scene"], rec["rc"]) == ("quality_gate", "failed", "s1", 1)
    assert any(e["stage"] == "alert" and e["scene"] == "s1" for e in events.read(root))
    assert all(events.validate(e) == [] for e in events.read(root))


def test_notify_posta_no_webhook_sem_texto_de_jogo(tmp_path, monkeypatch):
    recebido = []

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            recebido.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            self.send_response(200)
            self.end_headers()

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    monkeypatch.setenv(alerts.WEBHOOK_ENV, f"http://127.0.0.1:{srv.server_port}/hook")
    try:
        rec = alerts.notify(_projeto(tmp_path), "run_scene", "timeout", "s1", 124)
    finally:
        srv.shutdown()
    assert rec["webhook"] is True
    assert recebido[0]["step"] == "run_scene" and recebido[0]["rc"] == 124 and "run_scene timeout" in recebido[0]["text"]
    assert set(recebido[0]) == {"text", "t", "project", "scene", "step", "result", "rc", "run"}


def test_webhook_fora_do_ar_ou_invalido_nao_derruba(tmp_path, monkeypatch, capsys):
    root = _projeto(tmp_path)
    monkeypatch.setenv(alerts.WEBHOOK_ENV, "http://127.0.0.1:9/nada")      # porta fechada
    assert alerts.notify(root, "x", "failed")["webhook"] is False
    monkeypatch.setenv(alerts.WEBHOOK_ENV, "ftp://exemplo")
    assert alerts.notify(root, "x", "failed")["webhook"] is False
    assert len(alerts.read(root)) == 2                                     # o alerta ficou em disco nas duas
    assert "AVISO" in capsys.readouterr().err


def test_onda_que_falha_gera_alerta_sem_ninguem_olhar_o_log(tmp_path, monkeypatch):
    """Criterio da nota 4: passo da onda que falha (rc != 0), trava (timeout) ou bloqueia na entrada alerta sozinho."""
    monkeypatch.delenv(alerts.WEBHOOK_ENV, raising=False)
    root = _projeto(tmp_path)
    monkeypatch.setattr(wave, "steps", lambda *a, **k: [("quality_gate", ["quality_gate.py", str(root)])])
    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: [])

    class P:
        returncode, stdout, stderr = 3, "ruim", ""

    monkeypatch.setattr(wave.subprocess, "run", lambda *a, **k: P())
    assert wave.run(str(root), ["s1"]) == 3
    assert [(a["step"], a["result"], a["rc"]) for a in alerts.read(root)] == [("quality_gate", "failed", 3)]

    def trava(*a, **k):
        raise wave.subprocess.TimeoutExpired("x", 1)

    monkeypatch.setattr(wave.subprocess, "run", trava)
    assert wave.run(str(root), ["s1"], step_timeout=1) == 124
    assert alerts.read(root)[-1]["result"] == "timeout"

    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: ["escalonamento aberto"])
    assert wave.run(str(root), ["s1"]) == 1
    assert alerts.read(root)[-1]["result"] == "blocked"


def test_onda_que_passa_nao_alerta(tmp_path, monkeypatch):
    root = _projeto(tmp_path)
    monkeypatch.setattr(wave, "steps", lambda *a, **k: [("glossary_lint", ["glossary_lint.py", str(root)])])
    monkeypatch.setattr(wave, "entry_problems", lambda *a, **k: [])

    class P:
        returncode, stdout, stderr = 0, "ok", ""

    monkeypatch.setattr(wave.subprocess, "run", lambda *a, **k: P())
    assert wave.run(str(root), ["s1"]) == 0
    assert alerts.read(root) == []


def test_obs_report_mostra_indicadores_e_alertas(tmp_path):
    root = _projeto(tmp_path)
    paths.run_state(root).write_text(json.dumps({"scenes": {"s1": {"status": "verified", "n_lines": 3}}}), encoding="utf-8")
    with events.stage(root, "scene", "s1") as ev:
        ev["result"] = "verified"
    alerts.notify(root, "cost_report", "failed", "s1", 2)
    txt = obs_report._fmt(obs_report.report(root))
    assert "indicadores: taxa de sucesso da onda 100%" in txt
    assert "alertas de onda: 1" in txt and "cost_report/failed rc=2" in txt
