"""Auditoria F1 (rastreabilidade): uma execucao tem UM id, gravado no ledger de custo, nos eventos e nas metricas."""
import json

import cost
import events
import paths

USO = {"in": 10, "out": 5, "cache_read": 0, "cache_write": 0}


def _linhas(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()]


def test_ledger_eventos_e_metricas_compartilham_o_run_id(tmp_path):
    (tmp_path / "artifacts").mkdir()
    cost.log_api_call(tmp_path, "S1", "translate", "claude-sonnet-5-5", USO)
    events.emit(tmp_path, "pack", "ok", "S1")
    paths.append_line(paths.metrics(tmp_path), json.dumps({"scene": "S1", "run": events.RUN}) + "\n")
    ids = {_linhas(paths.ledger(tmp_path))[0]["run"], _linhas(paths.events(tmp_path))[0]["run"],
           _linhas(paths.metrics(tmp_path))[0]["run"]}
    assert ids == {events.RUN} and events.RUN


def test_chamada_sem_uso_nao_grava_linha_e_nao_exige_run(tmp_path):
    (tmp_path / "artifacts").mkdir()
    assert cost.log_api_call(tmp_path, "S1", "translate", "claude-sonnet-5-5", {}) is None
    assert not paths.ledger(tmp_path).exists()
