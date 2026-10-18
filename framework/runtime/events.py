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

# Schema (Onda 3): campos obrigatorios e etapas conhecidas. `gate.*` e `audit.*` sao familias abertas.
OBRIGATORIOS = {"t": (int, float), "run": (str,), "stage": (str,), "result": (str,)}
ETAPAS = frozenset({"pack", "translate", "build_plan", "verify", "back_translate", "state_index", "scene",
                    "quality", "alert"})
FAMILIAS = ("gate.", "audit.")
MAX_TEXTO = 200


def validate(rec: dict) -> list[str]:
    """Problemas de um evento (lista vazia = valido): campo obrigatorio ausente/de tipo errado, etapa fora do
    conjunto conhecido, valor nao escalar ou texto longo (evento so leva contagem, status e duracao; nada de fala)."""
    out = []
    for k, tipos in OBRIGATORIOS.items():
        v = rec.get(k)
        if v is None or isinstance(v, bool) or not isinstance(v, tipos):
            out.append(f"campo `{k}` ausente ou de tipo errado")
    if "scene" not in rec or not (rec["scene"] is None or isinstance(rec["scene"], str)):
        out.append("campo `scene` deve existir (str ou null)")
    stg = rec.get("stage")
    if isinstance(stg, str) and stg not in ETAPAS and not stg.startswith(FAMILIAS):
        out.append(f"etapa desconhecida `{stg}`")
    for k, v in rec.items():
        if isinstance(v, str) and len(v) > MAX_TEXTO:
            out.append(f"`{k}` com {len(v)} caracteres (maximo {MAX_TEXTO}): evento nao carrega texto")
        elif not (v is None or isinstance(v, str | int | float | bool)):
            out.append(f"`{k}` nao e escalar ({type(v).__name__})")
    return out


def emit(root, stage: str, result: str, scene: str | None = None, **fields) -> None:
    """Anexa um evento. Nunca derruba o pipeline: observabilidade que falha so avisa."""
    rec = {"t": round(time.time(), 3), "run": RUN, "scene": scene, "stage": stage, "result": result, **fields}
    if (probs := validate(rec)):
        print(f"[events] AVISO: evento {stage}/{result} fora do schema: {'; '.join(probs)}.")
    try:
        paths.append_line(paths.events(Path(root)), json.dumps(rec, ensure_ascii=False, default=str) + "\n",
                          timeout=5.0)
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
