#!/usr/bin/env python3
"""
wave.py — UMA ONDA NUM COMANDO SO (caminho de sessao): roda os passos mecanicos em sequencia, grava a saida
inteira em `artifacts/wave_last_<primeira-cena>[_+N].log` (um log por onda: ondas ou subagentes em paralelo nao
sobrescrevem o log um do outro; sem cena, `wave_last.log`) e devolve UMA linha por passo. Cada comando na janela da sessao rele o
contexto inteiro; juntar os passos e tirar a saida longa da conversa e o que barateia a orquestracao.

Nao pula nada: sao os mesmos comandos, na mesma ordem, com os mesmos gates. Passo que falha PARA a onda.

  run_scene (se houver cenas; cena de texto repetido espera a original) -> scene_dedup copy -> run_scene das copias
  -> glossary_lint -> quality_gate -> session_usage rebuild -> cost_report --summary (+ --by-scene no log)
  -> obs_report

Uso:
  python wave.py <projeto> [cena ...] [--backend in-session|api] [--require-back]
"""
from __future__ import annotations

import argparse
import contextlib
import subprocess
import sys
from pathlib import Path

import paths

_HERE = Path(__file__).resolve().parent
LOG = "wave_last.log"
STEP_TIMEOUT = 3600        # s por passo: passo travado para a onda com mensagem, em vez de prender a sessao


def _copies(project: str, scenes: list[str]) -> set[str]:
    """Cenas do pedido que repetem o texto de outra cena (scene_dedup): traduzidas por copia, nao por modelo."""
    import scene_dedup
    from paths import require_project
    return {d for ds in scene_dedup.groups(require_project(project)).values() for d in ds} & set(scenes)


def steps(project: str, scenes: list[str], backend: str, require_back: bool) -> list[tuple[str, list[str]]]:
    out = []
    own = [s for s in scenes if s not in _copies(project, scenes)] if scenes else []
    if own:
        out.append(("run_scene", ["run_scene.py", project, *own, "--backend", backend]
                    + (["--require-back"] if require_back else [])))
    if len(own) < len(scenes):                       # ha copias: o passo `scene_dedup` gera o run_scene delas
        out.append(("scene_dedup", ["scene_dedup.py", project, "copy", *scenes]))
    scope = ["--scenes", *scenes] if scenes else []   # o gate da onda e por cena; o global fica na entrada (entry_problems)
    return out + [("glossary_lint", ["glossary_lint.py", project, *scope]), ("quality_gate", ["quality_gate.py", project, *scope]),
                  # rebuild: o `sync` incremental perde o gasto dos subagentes; sem ele a onda mostra custo falso.
                  ("session_usage", ["session_usage.py", "rebuild", project]),
                  ("cost_report", ["cost_report.py", project, "--summary"]),
                  ("cost_detail", ["cost_report.py", project, "--by-scene"]), ("obs_report", ["obs_report.py", project])]


def phase_lines(name: str, text: str) -> list[str]:
    """Do run_scene: so as linhas que dizem em que fase a onda esta (AGUARDANDO traducao/back-translation) e
    quais cenas fecharam. Sao o contrato com o `session_usage` (fase e fechamento da cena na transcricao: sem
    elas o custo da onda nao se divide em traducao x governanca) e dizem ao usuario o que falta."""
    if not name.startswith("run_scene"):
        return []
    seen: list[str] = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ("AGUARDANDO" in ln or "status final =" in ln) and ln not in seen:
            seen.append(ln[:160])
    return seen


def log_name(scenes: list[str]) -> str:
    if not scenes:
        return LOG
    return f"wave_last_{scenes[0]}.log" if len(scenes) == 1 else f"wave_last_{scenes[0]}_+{len(scenes) - 1}.log"


def entry_problems(project: str, scenes: list[str]) -> list[str]:
    """Bloqueio global na ENTRADA da onda: escalonamento aberto de cena fora do pedido (onda anterior) impede
    abrir onda nova. O gate da onda e por cena; isto garante que nenhuma pendencia fique esquecida."""
    import hitl
    if not scenes or not hitl.enabled(project):
        return []
    if all(paths.pack(Path(project), s).is_file() for s in scenes):
        return []                                  # cenas ja em andamento (subagente em paralelo): nao e onda nova
    want = set(scenes)
    other = sorted({r["scene"] for r in hitl.open_items(project) if r["scene"] not in want})
    return [f"escalonamento aberto de outra onda ({', '.join(other)}): responda em {hitl.queue_path(Path(project))} "
            f"e rode hitl.py resolve antes de abrir esta onda"] if other else []


class _LogAnexo:
    """Log da onda: comeca vazio (troca atomica) e cada `write` anexa sob trava, para o log ir aparecendo
    durante a onda e uma queda no meio nao deixar arquivo truncado nem linhas misturadas."""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        paths.atomic_write(self.path, "")
        return self

    def __exit__(self, *_exc):
        return False

    def write(self, texto: str) -> None:
        paths.append_line(self.path, texto)


def run(project: str, scenes: list[str], backend: str = "in-session", require_back: bool = False,
        step_timeout: float = STEP_TIMEOUT) -> int:
    probs = entry_problems(project, scenes)
    if probs:
        print("BLOQUEADO na entrada da onda: " + " | ".join(probs))
        return 1
    log = Path(project) / "artifacts" / log_name(scenes)
    rc = 0
    todo = steps(project, scenes, backend, require_back)
    with _LogAnexo(log) as fh:
        while todo:
            name, cmd = todo.pop(0)
            try:
                p = subprocess.run([sys.executable, "-X", "utf8", str(_HERE / cmd[0]), *cmd[1:]], capture_output=True,
                                   text=True, encoding="utf-8", errors="replace", timeout=step_timeout)
            except subprocess.TimeoutExpired:
                fh.write(f"===== {name} (TIMEOUT apos {step_timeout:.0f} s) =====\n")
                print(f"PAROU em {name}: sem resposta em {step_timeout:.0f} s (--step-timeout); detalhe em {log}")
                return 124
            text = (p.stdout or "") + (p.stderr or "")
            fh.write(f"===== {name} (exit {p.returncode}) =====\n{text}\n")
            last = next((ln.strip() for ln in reversed(text.splitlines()) if ln.strip()), "")
            print(f"{name:14s} exit={p.returncode}  " + ("(por fase e por cena no log)" if name == "cost_detail" and not p.returncode
                                                         else last[:300]))
            for ln in phase_lines(name, text):
                print("               " + ln)
            if p.returncode:
                rc = p.returncode
                print(f"PAROU em {name}: resolva a causa e rode de novo (detalhe em {log})")
                break
            if name == "scene_dedup":                # as copias feitas passam pelos mesmos gates
                made = [x for x in last.split() if x in set(scenes)]
                if made:
                    todo.insert(0, ("run_scene_copias", ["run_scene.py", project, *made, "--backend", backend]
                                    + (["--require-back"] if require_back else [])))
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
    ap.add_argument("--step-timeout", type=float, default=STEP_TIMEOUT, help="segundos maximos por passo (padrao 3600)")
    a = ap.parse_args()
    sys.exit(run(a.project, a.scene, a.backend, a.require_back, a.step_timeout))


if __name__ == "__main__":
    main()
