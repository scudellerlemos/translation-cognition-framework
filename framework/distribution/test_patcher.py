import subprocess
from types import SimpleNamespace

import patcher

APP = {"processos": ["BOF4.exe", "4249150_Launcher.exe"]}


def _tasklist(monkeypatch, out):
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=out))


def test_jogo_aberto_detects_process_and_survives_missing_output(monkeypatch):
    _tasklist(monkeypatch, "BOF4.exe    1234 Console")
    assert patcher.jogo_aberto(APP)
    _tasklist(monkeypatch, "INFORMACAO: nenhuma tarefa")
    assert not patcher.jogo_aberto(APP)
    _tasklist(monkeypatch, None)                       # decode falhou na thread de leitura: nao pode estourar
    assert not patcher.jogo_aberto(APP)
