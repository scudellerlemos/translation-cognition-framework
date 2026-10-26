#!/usr/bin/env python3
"""
lote_status.py — uma tela com a situacao do lote de ondas (substitui conferir lock, estado.json e logs a mao).

Mostra: execucao viva (PID do `logs/.lock` esta de pe?), `estado.json` contra o `run_state.json`
(defasado = onda fechada fora do `rodar_ondas.ps1`: numeracao errada), ultimo log de onda e a idade dele,
e o batimento do projeto (`estimar_lote.estado`).

Uso:  python lote_status.py projects/<nome> [pasta de logs, padrao framework/skills/operacao/rodar-onda/logs]
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import estimar_lote

LOGS_PADRAO = Path("framework/skills/operacao/rodar-onda/logs")
DEFASAGEM_MIN = 10          # mesma regra do rodar_ondas.ps1


def pid_do_lock(logs: Path) -> int | None:
    """PID gravado no `.lock` (o PowerShell grava em UTF-16 com BOM; aceita UTF-8 tambem)."""
    f = logs / ".lock"
    if not f.is_file():
        return None
    raw = f.read_bytes()
    for enc in ("utf-16", "utf-8-sig"):
        try:
            return int(raw.decode(enc).strip())
        except (UnicodeDecodeError, ValueError):
            continue
    return None


def pid_vivo(pid: int) -> bool:
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, check=False).stdout
    return str(pid) in out


def estado_json(logs: Path) -> dict:
    f = logs / "estado.json"
    return json.loads(f.read_text(encoding="utf-8-sig")) if f.is_file() else {}


def defasado(logs: Path, projeto: Path) -> bool:
    e, rs = logs / "estado.json", projeto / "artifacts" / "run_state.json"
    return e.is_file() and rs.is_file() and (rs.stat().st_mtime - e.stat().st_mtime) / 60 > DEFASAGEM_MIN


def fim_do_console(logs: Path, n: int = 8, agora: float | None = None) -> list[str]:
    """Ultimas linhas do transcript do console (`lote_<n>_console.log`): onde cai o texto de um erro do script."""
    fs = sorted(logs.glob("lote_*_console.log"), key=lambda p: p.stat().st_mtime)
    if not fs:
        return []
    f = fs[-1]
    idade = int(((agora or time.time()) - f.stat().st_mtime) / 60)
    linhas = [ln for ln in f.read_text(encoding="utf-8-sig", errors="replace").splitlines() if ln.strip()]
    return [f"console  : {f.name} (ha {idade} min), ultimas linhas:", *[f"    {ln[:160]}" for ln in linhas[-n:]]]


def ultimo_log(logs: Path, agora: float | None = None) -> str:
    logs_onda = sorted(logs.glob("onda_*.log"), key=lambda p: p.stat().st_mtime)
    if not logs_onda:
        return "nenhum log de onda"
    f = logs_onda[-1]
    idade = int(((agora or time.time()) - f.stat().st_mtime) / 60)
    linhas = [ln for ln in f.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    return f"{f.name} (ha {idade} min): {linhas[-1][:120] if linhas else 'vazio'}"


def tela(projeto: Path, logs: Path) -> list[str]:
    pid = pid_do_lock(logs)
    viva = False
    if pid is None:
        exec_ = "sem execucao (nao ha .lock)"
    elif pid_vivo(pid):
        viva = True
        exec_ = f"EM EXECUCAO (PID {pid})"
    else:
        exec_ = f"lock velho (PID {pid} morto; o proximo lote o sobrescreve)"
    est = estado_json(logs)
    # Com o lote rodando, o estado.json so e gravado no fim de cada onda: run_state mais novo e esperado, nao defasagem.
    aviso = "  <- DEFASADO: houve onda fora do script; rode com -OndaInicial" if not viva and defasado(logs, projeto) else ""
    return [f"execucao : {exec_}",
            f"estado   : proxima_onda={est.get('proxima_onda', '?')} lote={est.get('lote', '?')}{aviso}",
            f"ultimo   : {ultimo_log(logs)}",
            f"projeto  : {estimar_lote.estado(projeto)}",
            *([] if viva else fim_do_console(logs))]


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python lote_status.py projects/<nome> [pasta de logs]")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # console cp1252 do Windows nao imprime o texto do jogo
    print("\n".join(tela(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else LOGS_PADRAO)))


if __name__ == "__main__":
    main()
