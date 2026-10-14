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


# --- ciclo instalar/desinstalar sobre pacote sintetico (bytes inventados, nada do jogo) ---
import hashlib
import subprocess as _sp
import sys
from pathlib import Path

import bsdiff4
import pytest

sha = lambda b: hashlib.sha256(b).hexdigest()
ORIG, TRAD = {"A.DAT": b"original-a" * 20, "B.DAT": b"original-b" * 20}, {"A.DAT": b"traduzido-a" * 20, "B.DAT": b"traduzido-b" * 20}


@pytest.fixture
def cenario(tmp_path, monkeypatch):
    jogo, pkg = tmp_path / "jogo", tmp_path / "pkg"
    (pkg / "deltas").mkdir(parents=True)
    jogo.mkdir()
    for n in ORIG:
        (jogo / n).write_bytes(ORIG[n])
        (pkg / "deltas" / (n + ".bsdiff")).write_bytes(bsdiff4.diff(ORIG[n], TRAD[n]))
    man = {"app": APP, "files": [{"name": n, "sha_original": sha(ORIG[n]), "sha_final": sha(TRAD[n])} for n in ORIG]}
    monkeypatch.setattr(patcher, "jogo_aberto", lambda app: False)
    return jogo, pkg, man


def _conteudo(jogo):
    return {n: (jogo / n).read_bytes() for n in ORIG}


def test_instalar_idempotente_e_desinstalar_volta_byte_a_byte(cenario):
    jogo, pkg, man = cenario
    assert not patcher.instalar(jogo, pkg, man)
    assert _conteudo(jogo) == TRAD
    assert not patcher.instalar(jogo, pkg, man)                    # de novo: nada a fazer
    assert _conteudo(jogo) == TRAD
    assert not patcher.desinstalar(jogo, man)
    assert _conteudo(jogo) == ORIG


def test_arquivo_modificado_recusa_sem_alterar_nada(cenario):
    jogo, pkg, man = cenario
    (jogo / "B.DAT").write_bytes(b"outra versao")
    assert patcher.instalar(jogo, pkg, man) == 1
    assert (jogo / "A.DAT").read_bytes() == ORIG["A.DAT"] and (jogo / "B.DAT").read_bytes() == b"outra versao"


def test_falha_no_meio_restaura_tudo(cenario):
    jogo, pkg, man = cenario
    (pkg / "deltas" / "B.DAT.bsdiff").write_bytes(bsdiff4.diff(ORIG["B.DAT"], b"hash errado"))
    assert patcher.instalar(jogo, pkg, man) == 1
    assert _conteudo(jogo) == ORIG


def test_jogo_aberto_bloqueia_instalar_e_desinstalar(cenario, monkeypatch):
    jogo, pkg, man = cenario
    monkeypatch.setattr(patcher, "jogo_aberto", lambda app: True)
    man["app"] = {**APP, "titulo": "Jogo"}
    assert patcher.instalar(jogo, pkg, man) == 1 and patcher.desinstalar(jogo, man) == 1
    assert _conteudo(jogo) == ORIG


def test_scripts_de_build_tem_help_e_exe_recusa_saida_em_dist(tmp_path):
    here = Path(__file__).parent
    for s in ("build_package.py", "build_exe.py", "patcher.py"):
        r = _sp.run([sys.executable, str(here / s), "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert "Uso" in (r.stdout + r.stderr), s
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "manifest.json").write_text('{"app": {"exe": "x"}}', encoding="utf-8")
    r = _sp.run([sys.executable, "-O", str(here / "build_exe.py"), str(dist), str(dist / "sub")], capture_output=True, text=True)
    assert r.returncode != 0 and "embutida" in r.stderr
