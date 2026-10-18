"""Integridade de estado: escrita atomica, append sob trava e tempo de vida da trava (paths.py).

Origem: auditoria de 2026-10-17. O `open('a')` do Python no Windows perde/mistura linhas com varios
processos, e `write_text` direto deixa o arquivo truncado se o processo cai no meio.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import paths
import pytest

HERE = Path(__file__).resolve().parent
_WORKER = """
import sys, json
sys.path.insert(0, {here!r})
import paths
for k in range({n}):
    paths.append_line({target!r}, json.dumps({{"w": {w}, "k": k, "x": "a" * 150}}) + "\\n")
"""


def test_atomic_write_grava_e_nao_deixa_temporario(tmp_path):
    p = tmp_path / "estado.json"
    paths.atomic_write(p, '{"a": 1}')
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 1}
    assert [x.name for x in tmp_path.iterdir()] == ["estado.json"]


def test_atomic_write_falha_no_meio_preserva_o_original(tmp_path, monkeypatch):
    p = tmp_path / "estado.json"
    paths.atomic_write(p, '{"a": 1}')

    def cai(*_a, **_k):
        raise OSError("queda simulada")

    monkeypatch.setattr(paths.os, "replace", cai)
    with pytest.raises(OSError):
        paths.atomic_write(p, '{"a": 2}')
    monkeypatch.undo()
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 1}      # original intacto, JSON valido
    assert [x.name for x in tmp_path.iterdir()] == ["estado.json"]    # temporario removido


def test_atomic_write_respeita_utf8_e_quebra_de_linha(tmp_path):
    p = tmp_path / "t.txt"
    paths.atomic_write(p, "a\nçã\n")
    assert p.read_bytes().decode("utf-8").replace("\r\n", "\n") == "a\nçã\n"


def test_append_line_com_processos_paralelos_nao_perde_nem_mistura_linha(tmp_path):
    target = tmp_path / "log.jsonl"
    target.write_text("", encoding="utf-8")
    workers, n = 5, 60
    procs = [subprocess.Popen([sys.executable, "-c", _WORKER.format(here=str(HERE), n=n, target=str(target), w=w)])
             for w in range(workers)]
    assert all(p.wait(timeout=120) == 0 for p in procs)
    rows = [json.loads(ln) for ln in target.read_text(encoding="utf-8").splitlines()]   # linha corrompida levanta aqui
    assert len(rows) == workers * n
    assert {(r["w"], r["k"]) for r in rows} == {(w, k) for w in range(workers) for k in range(n)}
    assert not (tmp_path / "log.jsonl.lock").exists()


def test_locked_trava_orfa_so_quebra_depois_de_stale(tmp_path):
    p = tmp_path / "x.json"
    lock = tmp_path / "x.json.lock"
    lock.write_text("", encoding="utf-8")
    # trava recente + stale longo: nao e quebrada, quem espera estoura o timeout
    with pytest.raises(TimeoutError), paths.locked(p, timeout=0.2, stale=60.0):
        pass
    assert lock.exists()
    # trava velha (acima de stale): e quebrada e a secao critica roda
    old = time.time() - 120
    os.utime(lock, (old, old))
    with paths.locked(p, timeout=1.0, stale=60.0):
        assert lock.exists()
    assert not lock.exists()


def test_locked_padrao_mantem_stale_igual_ao_timeout(tmp_path):
    p = tmp_path / "x.json"
    lock = tmp_path / "x.json.lock"
    lock.write_text("", encoding="utf-8")
    old = time.time() - 5
    os.utime(lock, (old, old))
    with paths.locked(p, timeout=1.0):          # comportamento antigo: trava com mais de `timeout` s e orfa
        pass
    assert not lock.exists()


def test_events_emit_nao_derruba_quando_nao_pega_a_trava(tmp_path, monkeypatch):
    import events
    (tmp_path / "artifacts").mkdir()

    def sem_trava(*_a, **_k):
        raise TimeoutError("trava ocupada")

    monkeypatch.setattr(events.paths, "append_line", sem_trava)
    events.emit(tmp_path, "etapa", "ok")        # observabilidade que falha so avisa
