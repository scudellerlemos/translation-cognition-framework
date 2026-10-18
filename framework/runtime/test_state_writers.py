"""Onda 2 (integridade): os escritores de ESTADO real nao gravam direto no destino.

Estado = o que nao se regenera sozinho (traducao, aprovados, project.json, research_log, ledger, ratificacao).
Relatorio regeneravel (prompt, pack, csv de revisao) pode continuar com write_text. Quem entrar na lista abaixo
tem de usar atomic_write / os.replace / locked; esta lista so cresce.
"""
import ast
import csv
import json
import os
from pathlib import Path

import paths
import pytest
import tm_correct

RUNTIME = Path(__file__).resolve().parent
CONNECTORS = RUNTIME.parent / "connectors"

# (arquivo, funcao, o que prova que e seguro)
ESTADO = [
    (RUNTIME / "session_lot.py", "_save", "atomic_write"),
    (RUNTIME / "kb_phase.py", "apply_frontier", "atomic_write"),
    (RUNTIME / "kb_reconcile.py", "promote", "atomic_write"),
    (RUNTIME / "tm_correct.py", "_write_approved", "atomic_write_csv"),
    (RUNTIME / "session_usage.py", "rebuild", "locked"),
    (RUNTIME / "hitl.py", "_ratify_csv", "locked"),
    (CONNECTORS / "connector_io.py", "sync_translations_db", "replace"),
]


def _funcao(arquivo: Path, nome: str) -> ast.FunctionDef:
    for n in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    raise AssertionError(f"{nome} nao existe em {arquivo.name}")


@pytest.mark.parametrize(("arquivo", "nome", "prova"), ESTADO, ids=[f"{a.name}:{n}" for a, n, _ in ESTADO])
def test_escritor_de_estado_usa_gravacao_segura(arquivo, nome, prova):
    fn = _funcao(arquivo, nome)
    chamadas = {c.func.attr if isinstance(c.func, ast.Attribute) else getattr(c.func, "id", "")
                for c in ast.walk(fn) if isinstance(c, ast.Call)}
    assert prova in chamadas, f"{arquivo.name}:{nome} deve chamar {prova}"
    assert "write_text" not in chamadas, f"{arquivo.name}:{nome} grava estado com write_text direto"


def test_atomic_write_csv_preserva_aspas_quebra_de_linha_e_utf8(tmp_path):
    p = tmp_path / "a.csv"
    rows = [("0x1", 'ele disse "oi"\nsegunda linha'), ("0x2", "cafe, acucar")]
    paths.atomic_write_csv(p, ["offset", "text_target"], rows)
    with p.open(encoding="utf-8", newline="") as fh:
        assert [tuple(r) for r in csv.reader(fh)] == [("offset", "text_target"), *rows]
    assert [x.name for x in tmp_path.iterdir()] == ["a.csv"]


def test_csv_de_aprovados_nao_fica_truncado_se_a_troca_falha(tmp_path, monkeypatch):
    p = tmp_path / "approved_a.csv"
    tm_correct._write_approved(p, [{"offset": "0x1", "text_target": "bom"}])
    antes = p.read_bytes()

    def _boom(*_a, **_k):
        raise OSError("disco cheio")
    monkeypatch.setattr(os, "replace", _boom)
    with pytest.raises(OSError, match="disco cheio"):
        tm_correct._write_approved(p, [{"offset": "0x1", "text_target": "novo"}])
    assert p.read_bytes() == antes, "o arquivo bom anterior tem de sobreviver"
    assert [x.name for x in tmp_path.iterdir()] == ["approved_a.csv"], "sem temporario sobrando"


# --- leitura: estado corrompido nao e recriado em silencio -------------------------------------------
def test_read_json_ausente_devolve_default_e_valido_devolve_dado(tmp_path):
    assert paths.read_json(tmp_path / "nao_existe.json", {"x": 1}) == {"x": 1}
    (tmp_path / "ok.json").write_text('{"a": 2}', encoding="utf-8")
    assert paths.read_json(tmp_path / "ok.json") == {"a": 2}


def test_read_json_corrompido_levanta_com_arquivo_e_como_recuperar(tmp_path):
    p = tmp_path / "run_state.json"
    p.write_text('{"scenes": {"a": ', encoding="utf-8")
    with pytest.raises(paths.StateCorrupt) as ei:
        paths.read_json(p, {})
    msg = str(ei.value)
    assert "run_state.json" in msg and "linha 1" in msg and "git checkout" in msg


def test_checkpoint_com_run_state_corrompido_nao_sobrescreve_o_arquivo(tmp_path):
    import run_scene
    (tmp_path / "artifacts").mkdir()
    p = paths.run_state(tmp_path)
    p.write_text("{truncado", encoding="utf-8")
    with pytest.raises(paths.StateCorrupt):
        run_scene._checkpoint(tmp_path, "ch_01", {"status": "verified"})
    assert p.read_text(encoding="utf-8") == "{truncado", "o estado ruim fica como esta para ser recuperado"


def test_read_jsonl_ignora_linha_truncada_com_um_aviso(tmp_path, capsys):
    p = tmp_path / "ledger.jsonl"
    p.write_text('{"a": 1}\n\n{"a": 2}\n{"a": 3, "x', encoding="utf-8")        # ultima linha cortada por queda
    assert paths.read_jsonl(p) == [{"a": 1}, {"a": 2}]
    err = capsys.readouterr().err
    assert err.count("AVISO") == 1 and "1 linha(s)" in err
    assert paths.read_jsonl(tmp_path / "nao_existe.jsonl") == []


def test_ledger_de_sessao_com_linha_truncada_nao_derruba_marks(tmp_path):
    import session_usage
    (tmp_path / "artifacts").mkdir()
    p = tmp_path / "artifacts" / "phase_marks.jsonl"
    p.write_text('{"t": 2.0, "stage": "b"}\n{"t": 1.0, "stage": "a"}\n{"t": 3', encoding="utf-8")
    assert session_usage.marks(tmp_path) == [(1.0, "a"), (2.0, "b")]


def test_rebuild_do_ledger_nao_perde_linha_de_api_gravada_em_paralelo(tmp_path, monkeypatch):
    import subprocess
    import sys

    import session_usage
    monkeypatch.setattr(session_usage, "sync", lambda root, tdir=None: [])      # so o trecho que reescreve o ledger
    (tmp_path / "artifacts").mkdir()
    lp = paths.ledger(tmp_path)
    lp.write_text('{"source": "session", "k": "velha"}\n', encoding="utf-8")
    worker = ("import sys, json\nsys.path.insert(0, {here!r})\nimport paths\nfor k in range(40):\n"
              "    paths.append_line({lp!r}, json.dumps({{'source': 'api', 'w': {w}, 'k': k}}) + chr(10))\n")
    procs = [subprocess.Popen([sys.executable, "-c", worker.format(here=str(RUNTIME), lp=str(lp), w=w)])
             for w in range(3)]
    while any(p.poll() is None for p in procs):
        session_usage.rebuild(tmp_path)
    assert all(p.returncode == 0 for p in procs)
    session_usage.rebuild(tmp_path)
    rows = [json.loads(x) for x in lp.read_text(encoding="utf-8").splitlines()]
    assert {(r["w"], r["k"]) for r in rows} == {(w, k) for w in range(3) for k in range(40)}
    assert all(r["source"] == "api" for r in rows) and len(rows) == 120
