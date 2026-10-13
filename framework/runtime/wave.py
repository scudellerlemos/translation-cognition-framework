#!/usr/bin/env python3
"""
wave.py — UMA ONDA NUM COMANDO SO (caminho de sessao): roda os passos mecanicos em sequencia, grava a saida
inteira em `artifacts/wave_last.log` e devolve UMA linha por passo. Cada comando na janela da sessao rele o
contexto inteiro; juntar os passos e tirar a saida longa da conversa e o que barateia a orquestracao.

Nao pula nada: sao os mesmos comandos, na mesma ordem, com os mesmos gates. Passo que falha PARA a onda.

  run_scene (se houver cenas) -> glossary_lint -> quality_gate -> cost_report --summary -> obs_report

Uso:
  python wave.py <projeto> [cena ...] [--backend in-session|api] [--require-back]
"""
from __future__ import annotations

import argparse
import contextlib
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
LOG = "wave_last.log"


def steps(project: str, scenes: list[str], backend: str, require_back: bool) -> list[tuple[str, list[str]]]:
    out = []
    if scenes:
        out.append(("run_scene", ["run_scene.py", project, *scenes, "--backend", backend]
                    + (["--require-back"] if require_back else [])))
    return out + [("glossary_lint", ["glossary_lint.py", project]), ("quality_gate", ["quality_gate.py", project]),
                  ("cost_report", ["cost_report.py", project, "--summary"]), ("obs_report", ["obs_report.py", project])]


def run(project: str, scenes: list[str], backend: str = "in-session", require_back: bool = False) -> int:
    log = Path(project) / "artifacts" / LOG
    rc = 0
    with log.open("w", encoding="utf-8") as fh:
        for name, cmd in steps(project, scenes, backend, require_back):
            p = subprocess.run([sys.executable, "-X", "utf8", str(_HERE / cmd[0]), *cmd[1:]], capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            text = (p.stdout or "") + (p.stderr or "")
            fh.write(f"===== {name} (exit {p.returncode}) =====\n{text}\n")
            last = next((ln.strip() for ln in reversed(text.splitlines()) if ln.strip()), "")
            print(f"{name:14s} exit={p.returncode}  {last[:150]}")
            if p.returncode:
                rc = p.returncode
                print(f"PAROU em {name}: resolva a causa e rode de novo (detalhe em {log})")
                break
    print(f"saida completa: {log}")
    return rc


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Passos mecanicos de uma onda num comando so; saida longa em arquivo.")
    ap.add_argument("project")
    ap.add_argument("scene", nargs="*")
    ap.add_argument("--backend", default="in-session", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true")
    a = ap.parse_args()
    sys.exit(run(a.project, a.scene, a.backend, a.require_back))


if __name__ == "__main__":
    main()
