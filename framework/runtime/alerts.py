"""alerts.py — alerta de falha de onda sem ninguem olhar o log (Onda 3).

`notify` registra o alerta em tres lugares: evento `alert` (events.jsonl), `artifacts/alerts.jsonl` (o que o
`obs_report` mostra) e, se `TCF_ALERT_WEBHOOK` estiver definida, um POST JSON nesse endereco (Slack/Discord/
ntfy/qualquer receptor). O corpo leva so projeto, cena, passo, resultado e codigo de saida: nada de fala do jogo.

Nunca derruba o pipeline: webhook fora do ar so avisa em stderr (a falha ja esta em disco).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import events
import paths

WEBHOOK_ENV = "TCF_ALERT_WEBHOOK"
WEBHOOK_TIMEOUT = 5.0


def notify(root, step: str, result: str, scene: str | None = None, rc: int | None = None) -> dict:
    root = Path(root)
    rec = {"t": round(time.time(), 3), "project": root.name, "scene": scene, "step": step, "result": result,
           "rc": rc, "run": events.RUN}
    events.emit(root, "alert", "raised", scene, step=step, outcome=result, rc=rc)
    try:
        paths.append_line(paths.alerts(root), json.dumps(rec, ensure_ascii=False) + "\n", timeout=5.0)
    except OSError as e:
        print(f"[alerts] AVISO: alerta nao gravado em disco ({e!r}).", file=sys.stderr)
    url = os.environ.get(WEBHOOK_ENV, "").strip()
    if url:
        rec["webhook"] = _post(url, rec)
    return rec


def _post(url: str, rec: dict) -> bool:
    if not url.startswith(("https://", "http://")):
        print(f"[alerts] AVISO: {WEBHOOK_ENV} precisa ser http(s); alerta nao enviado.", file=sys.stderr)
        return False
    texto = f"[tcf] {rec['project']}: {rec['step']} {rec['result']}" + (f" (rc {rec['rc']})" if rec["rc"] is not None else "")
    body = json.dumps({"text": texto, **rec}).encode("utf-8")      # `text` serve a Slack/Discord/Mattermost
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=WEBHOOK_TIMEOUT):  # noqa: S310 (esquema validado acima)
            return True
    except (OSError, ValueError) as e:
        print(f"[alerts] AVISO: webhook falhou ({type(e).__name__}); o alerta continua em alerts.jsonl.", file=sys.stderr)
        return False


def read(root) -> list[dict]:
    p = paths.alerts(Path(root))
    out = []
    for line in p.read_text(encoding="utf-8").splitlines() if p.is_file() else []:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
