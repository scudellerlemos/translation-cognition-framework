"""events.py — log estruturado do pipeline: 1 linha JSON por acontecimento em artifacts/events.jsonl.

Cada linha: {"t": epoch, "run": id da execucao, "scene": cena|null, "stage": etapa, "result": resultado,
"dur_s": duracao (quando medida), ...campos da etapa}. E a fonte unica de: tempo por etapa, resultado
de gate (passou/bloqueou e quando), falha no meio de um lote e retrabalho. `obs_report.py` le daqui.

`run` identifica UMA execucao: o processo que comeca o lote exporta TCF_RUN_ID e os filhos herdam.

GOVERNANCA: so contagem, status e duracao. Nada de texto do jogo — de uma excecao entra o tipo e os
200 primeiros caracteres da mensagem, e o arquivo fica fora do git (.gitignore).
"""
from __future__ import annotations

import contextlib
import json
import os
import time
import uuid
from pathlib import Path

import paths

RUN = os.environ.setdefault("TCF_RUN_ID", uuid.uuid4().hex[:8])


def emit(root, stage: str, result: str, scene: str | None = None, **fields) -> None:
    """Anexa um evento. Nunca derruba o pipeline: observabilidade que falha so avisa."""
    rec = {"t": round(time.time(), 3), "run": RUN, "scene": scene, "stage": stage, "result": result, **fields}
    try:
        with paths.events(Path(root)).open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
    except FileNotFoundError:       # projeto sem artifacts/ ainda: nada a observar
        pass
    except OSError as e:
        print(f"[events] AVISO: evento {stage}/{result} nao gravado ({e!r}).")


@contextlib.contextmanager
def stage(root, name: str, scene: str | None = None):
    """Mede a etapa. O corpo preenche `ev` (ex.: ev["result"] = "fail", ev["over"] = 3); excecao vira
    result="error" com tipo e mensagem curta, e segue subindo."""
    ev: dict = {"result": "ok"}
    t0 = time.perf_counter()
    try:
        yield ev
    except BaseException as e:
        ev.update(result="error", error=type(e).__name__, msg=str(e)[:200])
        raise
    finally:
        emit(root, name, ev.pop("result"), scene, dur_s=round(time.perf_counter() - t0, 3), **ev)


def read(root) -> list[dict]:
    p = paths.events(Path(root))
    out = []
    for line in p.read_text(encoding="utf-8").splitlines() if p.is_file() else []:
        with contextlib.suppress(json.JSONDecodeError):
            out.append(json.loads(line))
    return out
