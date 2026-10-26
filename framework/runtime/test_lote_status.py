import os

import lote_status as L


def test_pid_do_lock_le_utf16_do_powershell_e_utf8(tmp_path):
    assert L.pid_do_lock(tmp_path) is None
    (tmp_path / ".lock").write_bytes("123\r\n".encode("utf-16"))
    assert L.pid_do_lock(tmp_path) == 123
    (tmp_path / ".lock").write_bytes(b"456\n")
    assert L.pid_do_lock(tmp_path) == 456


def test_defasado_so_se_run_state_for_mais_novo_que_10_min(tmp_path):
    logs, proj = tmp_path / "logs", tmp_path / "p"
    (proj / "artifacts").mkdir(parents=True)
    logs.mkdir()
    e, rs = logs / "estado.json", proj / "artifacts" / "run_state.json"
    e.write_text("{}", encoding="utf-8")
    rs.write_text("{}", encoding="utf-8")
    os.utime(e, (1000, 1000))
    os.utime(rs, (1000 + 5 * 60, 1000 + 5 * 60))
    assert not L.defasado(logs, proj)
    os.utime(rs, (1000 + 11 * 60, 1000 + 11 * 60))
    assert L.defasado(logs, proj)


def test_tela_com_lock_morto_e_sem_log(tmp_path, monkeypatch):
    logs, proj = tmp_path / "logs", tmp_path / "p"
    logs.mkdir()
    (logs / ".lock").write_bytes(b"999\n")
    (logs / "estado.json").write_text('{"proxima_onda": 7, "lote": 2}', encoding="utf-8")
    monkeypatch.setattr(L, "pid_vivo", lambda pid: False)
    t = "\n".join(L.tela(proj, logs))
    assert "lock velho (PID 999 morto" in t and "proxima_onda=7 lote=2" in t and "nenhum log de onda" in t


def test_defasado_nao_vale_com_lote_vivo(tmp_path, monkeypatch):
    logs, proj = tmp_path / "logs", tmp_path / "p"
    (proj / "artifacts").mkdir(parents=True)
    logs.mkdir()
    (logs / ".lock").write_bytes(b"999\n")
    e, rs = logs / "estado.json", proj / "artifacts" / "run_state.json"
    e.write_text("{}", encoding="utf-8")
    rs.write_text("{}", encoding="utf-8")
    os.utime(e, (1000, 1000))
    os.utime(rs, (1000 + 30 * 60, 1000 + 30 * 60))
    monkeypatch.setattr(L, "pid_vivo", lambda pid: True)
    assert "DEFASADO" not in "\n".join(L.tela(proj, logs))
    monkeypatch.setattr(L, "pid_vivo", lambda pid: False)
    assert "DEFASADO" in "\n".join(L.tela(proj, logs))


def test_fim_do_console_mostra_o_erro_do_script(tmp_path):
    assert L.fim_do_console(tmp_path) == []
    (tmp_path / "lote_8_console.log").write_text("﻿inicio\nErro: algo ⑧ quebrou\n", encoding="utf-8")
    t = "\n".join(L.fim_do_console(tmp_path))
    assert "lote_8_console.log" in t and "algo ⑧ quebrou" in t
