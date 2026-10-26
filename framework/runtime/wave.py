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
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import alerts
import cost_report
import events
import paths

_HERE = Path(__file__).resolve().parent
LOG = "wave_last.log"
STEP_TIMEOUT = 3600        # s por passo: passo travado para a onda com mensagem, em vez de prender a sessao
BUDGET_RC = 4              # a onda parou porque o gasto dela chegou ao teto
BUDGET_POLL = 1.0          # s entre leituras do ledger enquanto um passo roda


class _Teto(Exception):
    """O gasto da onda chegou ao teto enquanto o passo rodava (o passo ja foi morto)."""


def wave_budget(project: str, cli: float | None) -> float | None:
    """Teto da onda em USD: `--max-usd` vence; senao `budget.max_usd_per_wave` do project.json; senao sem teto."""
    if cli is not None:
        return cli
    p = paths.project_json(Path(project))
    cfg = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    v = (cfg.get("budget") or {}).get("max_usd_per_wave")
    return float(v) if v is not None else None


def spent_since(project: str, t0: float) -> float:
    """Gasto (API paga + equivalente de sessao) das linhas do ledger gravadas desde `t0`."""
    return sum(r.get("api_equiv_usd") or r.get("cost_usd", 0.0)
               for r in cost_report.read_ledger(Path(project)) if r.get("t", 0.0) >= t0)


def _matar(p: subprocess.Popen) -> None:
    """Mata o passo E os processos que ele abriu (run_scene --jobs abre um por cena)."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, check=False)
    else:
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(p.pid, signal.SIGKILL)  # type: ignore[attr-defined]
    with contextlib.suppress(OSError):
        p.kill()


def _executa(argv: list[str], timeout: float, estourou=None):
    """Roda um passo. Sem `estourou` (sem teto) e o subprocess.run de sempre. Com `estourou` (callable -> bool),
    confere o teto a cada BUDGET_POLL s e mata o passo (e os filhos) quando passar: parada dura, nao so aviso."""
    if estourou is None:
        return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=timeout)
    flags = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
                         errors="replace", **flags)    # type: ignore[call-overload]
    fim = time.monotonic() + timeout
    while True:
        try:
            out, err = p.communicate(timeout=BUDGET_POLL)
            return subprocess.CompletedProcess(argv, p.returncode, out, err)
        except subprocess.TimeoutExpired:
            if estourou():
                _matar(p)
                p.communicate()
                raise _Teto from None
            if time.monotonic() > fim:
                _matar(p)
                p.communicate()
                raise


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


_ESPERA_RUN_SCENE = ("AGUARDANDO traducao", "AGUARDANDO back-translation")
_ESPERA_GATE = ("SEM COBERTURA", "REVISAR", "ESCALONAMENTO")
_ERRO = ("Traceback", "ERRO", "BLOQUEADO", "SCHEMA")


CARENCIA_CORRECAO = 1800.0     # s: tempo que a sessao tem para corrigir uma traducao parada antes de virar alerta


def espera_esperada(name: str, text: str) -> bool:
    """O passo saiu com codigo != 0 so porque a sessao ainda tem de traduzir ou retrotraduzir (fluxo normal da
    onda), sem erro de verdade: nao vira alerta. Qualquer marca de erro no texto mantem o alerta."""
    if "Traceback" in text:
        return False
    if name.startswith("run_scene") and events.CORRECAO_MARCA in text:
        return True                                  # defeito da traducao que a sessao corrige: segue sendo a onda
    if any(m in text for m in _ERRO):
        return False
    marcas = _ESPERA_RUN_SCENE if name.startswith("run_scene") else _ESPERA_GATE if name == "quality_gate" else ()
    return any(m in text for m in marcas)


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
    if not scenes or not hitl.enabled(project) or hitl.diferida(project):
        return []                                  # fila diferida: o humano responde no fim do lote (quality_gate --fechar)
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
        step_timeout: float = STEP_TIMEOUT, max_usd: float | None = None) -> int:
    probs = entry_problems(project, scenes)
    if probs:
        print("BLOQUEADO na entrada da onda: " + " | ".join(probs))
        alerts.notify(project, "entrada", "blocked", scenes[0] if scenes else None, 1)
        return 1
    # parada por defeito da traducao que ficou para tras (onda manual, sem resumo de lote): alerta passada a carencia
    alerts.alertar_correcoes_pendentes(project, CARENCIA_CORRECAO, tuple(scenes))
    log = Path(project) / "artifacts" / log_name(scenes)
    rc = 0
    todo = steps(project, scenes, backend, require_back)
    teto = wave_budget(project, max_usd)
    t0 = time.time()
    estourou = (lambda: spent_since(project, t0) >= teto) if teto is not None else None
    sc0 = scenes[0] if scenes else None

    def parar_por_teto(name: str, fh) -> int:
        gasto = spent_since(project, t0)
        fh.write(f"===== {name} (TETO DA ONDA: gasto ${gasto:.2f} >= ${teto:.2f}) =====\n")
        print(f"PAROU em {name}: o gasto da onda (${gasto:.2f}) chegou ao teto de ${teto:.2f} "
              f"(--max-usd ou budget.max_usd_per_wave); detalhe em {log}")
        alerts.notify(project, name, "budget", sc0, BUDGET_RC)
        return BUDGET_RC

    with _LogAnexo(log) as fh:
        while todo:
            name, cmd = todo.pop(0)
            if estourou and estourou():
                return parar_por_teto(name, fh)
            try:
                p = _executa([sys.executable, "-X", "utf8", str(_HERE / cmd[0]), *cmd[1:]], step_timeout, estourou)
            except _Teto:
                return parar_por_teto(name, fh)
            except subprocess.TimeoutExpired:
                fh.write(f"===== {name} (TIMEOUT apos {step_timeout:.0f} s) =====\n")
                print(f"PAROU em {name}: sem resposta em {step_timeout:.0f} s (--step-timeout); detalhe em {log}")
                alerts.notify(project, name, "timeout", scenes[0] if scenes else None, 124)
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
                if espera_esperada(name, text):
                    print("               (espera da sessao: passo normal da onda, sem alerta)")
                else:
                    alerts.notify(project, name, "failed", scenes[0] if scenes else None, p.returncode)
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
    ap.add_argument("--max-usd", type=float, default=None,
                    help="teto de gasto da onda em USD (padrao: budget.max_usd_per_wave do project.json; sem ele, sem teto)")
    a = ap.parse_args()
    sys.exit(run(a.project, a.scene, a.backend, a.require_back, a.step_timeout, a.max_usd))


if __name__ == "__main__":
    main()
