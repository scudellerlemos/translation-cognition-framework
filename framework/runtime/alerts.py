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


CORRECAO_STATUS = ("build_plan_failed", "verify_failed", "schema_failed")


def correcoes_pendentes(root, min_idade_s: float = 0.0, fora: tuple[str, ...] = ()) -> list[str]:
    """Cenas paradas no run_state por defeito da traducao (token, glifo, schema) que ninguem corrigiu. O `wave` nao
    alerta essa parada na hora (a sessao corrige e roda de novo); quem a revisita depois alerta o que sobrou.
    `min_idade_s`: so conta a parada com mais de tanto tempo (carencia para a correcao em andamento);
    `fora`: cenas que a execucao atual esta refazendo. Parada ja alertada (mesmo `_ts`) nao entra de novo."""
    p = paths.run_state(Path(root))
    try:
        scenes = json.loads(p.read_text(encoding="utf-8")).get("scenes", {}) if p.is_file() else {}
    except (OSError, ValueError):
        return []
    visto = {r["scene"]: r["t"] for r in read(root) if r.get("result") == "correcao_pendente"}
    agora = time.time()
    return sorted(s for s, v in scenes.items()
                  if v.get("status") in CORRECAO_STATUS and s not in fora
                  and agora - v.get("_ts", 0) >= min_idade_s and visto.get(s, 0) < v.get("_ts", 0))


def alertar_correcoes_pendentes(root, min_idade_s: float = 0.0, fora: tuple[str, ...] = ()) -> list[str]:
    cenas = correcoes_pendentes(root, min_idade_s, fora)
    for s in cenas:
        notify(root, "run_scene", "correcao_pendente", s)
    return cenas


def _post(url: str, rec: dict) -> bool:
    if not url.startswith(("https://", "http://")):
        print(f"[alerts] AVISO: {WEBHOOK_ENV} precisa ser http(s); alerta nao enviado.", file=sys.stderr)
        return False
    texto = f"[tcf] {rec['project']}: {rec['step']} {rec['result']}" + (f" (rc {rec['rc']})" if rec["rc"] is not None else "")
    body = json.dumps({"text": texto, **rec}).encode("utf-8")      # `text` serve a Slack/Discord/Mattermost
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=WEBHOOK_TIMEOUT):  # nosec B310 - esquema restrito a http(s) acima; URL vem do ambiente do operador
            return True
    except (OSError, ValueError) as e:
        print(f"[alerts] AVISO: webhook falhou ({type(e).__name__}); o alerta continua em alerts.jsonl.", file=sys.stderr)
        return False


def main() -> None:
    """`python alerts.py correcoes <projeto> [--carencia S]`: alerta as cenas paradas por defeito da traducao. O vigia
    do lote chama a cada passo, entao o alerta sai mesmo sem `resumo_lote.py` e sem onda seguinte."""
    import argparse
    ap = argparse.ArgumentParser(description=main.__doc__)
    ap.add_argument("acao", choices=["correcoes"])
    ap.add_argument("project")
    ap.add_argument("--carencia", type=float, default=0.0, help="so conta parada com mais de tantos segundos")
    a = ap.parse_args()
    for s in alertar_correcoes_pendentes(a.project, a.carencia):
        print(f"CORRECAO PENDENTE (alertada): {s}")


def read(root) -> list[dict]:
    p = paths.alerts(Path(root))
    out = []
    for line in p.read_text(encoding="utf-8").splitlines() if p.is_file() else []:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


if __name__ == "__main__":
    main()
