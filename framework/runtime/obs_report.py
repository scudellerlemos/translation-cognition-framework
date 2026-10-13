"""obs_report.py — visao unica de observabilidade do projeto: 1 linha por cena + gates + falhas.

Junta o que estava espalhado: estado (run_state.json), qualidade (metrics.jsonl + evento `verify`),
tempo por etapa e retrabalho (events.jsonl) e gasto (api_ledger.jsonl, via cost_report). So le.

Uso: python obs_report.py <projeto> [--json] [--scene CENA]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import cost_report  # noqa: E402
import events  # noqa: E402
import paths  # noqa: E402

STAGES = ("pack", "translate", "build_plan", "verify", "back_translate", "state_index")
_BAD = ("error", "fail", "block")


def _jsonl(p: Path) -> list[dict]:
    out = []
    for line in p.read_text(encoding="utf-8").splitlines() if p.is_file() else []:
        with contextlib.suppress(json.JSONDecodeError):
            out.append(json.loads(line))
    return out


def report(root) -> dict:
    root = Path(root)
    evs = events.read(root)
    rs = paths.run_state(root)
    state = json.loads(rs.read_text(encoding="utf-8")).get("scenes", {}) if rs.is_file() else {}
    last_metric = {m.get("scene"): m for m in _jsonl(paths.metrics(root))}
    cost = cost_report.report(root)

    scenes: dict[str, dict] = {}
    for name, st in state.items():
        m = last_metric.get(name, {})
        c = cost["by_scene"].get(name, {})
        scenes[name] = {"status": st.get("status"), "n_lines": st.get("n_lines"), "high": st.get("high"),
                        "back_pass_rate": m.get("back_pass_rate"), "overflow": None, "runs": 0, "verify_fails": 0,
                        "wait_s": 0.0, "dur_s": dict.fromkeys(STAGES, 0.0), "total_s": 0.0,
                        "cost_usd": c.get("cost_usd", 0.0), "session_equiv_usd": c.get("session_equiv_usd", 0.0),
                        "session_tokens": c.get("session_tokens", 0), "attribution": c.get("attribution", "")}
    awaiting: dict[str, float] = {}     # cena -> fim da execucao que parou AGUARDANDO (in-session)
    packs: dict[str, list] = {}         # cena -> eventos `pack` ainda nao descontados da etapa que os contem
    gates: dict[str, dict] = {}
    failures = []
    for e in evs:
        stg, res, sc = e.get("stage", ""), e.get("result", ""), scenes.get(e.get("scene"))
        if stg.startswith(("gate.", "audit.")):
            g = gates.setdefault(stg, {"pass": 0, "block": 0, "last": None, "last_t": None})
            g["pass" if res in ("pass", "ok") else "block"] += 1
            g["last"], g["last_t"] = res, e.get("t")
        if res in _BAD or (stg == "scene" and res.endswith("_failed")):
            failures.append({k: e.get(k) for k in ("t", "run", "scene", "stage", "result", "error", "problems")})
        if sc is None:
            continue
        if stg in STAGES:
            dur = e.get("dur_s", 0.0)
            if stg == "pack":
                packs.setdefault(e["scene"], []).append(e)
            else:       # o pack roda DENTRO da etapa que o pediu: desconta, para `translate` ser so a chamada
                start = e["t"] - dur
                inside = [p for p in packs.get(e["scene"], []) if start - 0.01 <= p["t"] <= e["t"] + 0.01]
                dur = max(0.0, dur - sum(p.get("dur_s", 0.0) for p in inside))
                packs[e["scene"]] = [p for p in packs.get(e["scene"], []) if p not in inside]
            sc["dur_s"][stg] = round(sc["dur_s"][stg] + dur, 3)
        if stg == "verify":
            sc["verify_fails"] += res != "ok"
            sc["overflow"] = e.get("individual_overflow", sc["overflow"])
        if stg == "scene":
            sc["runs"] += 1
            sc["total_s"] = round(sc["total_s"] + e.get("dur_s", 0.0), 3)
            start = e["t"] - e.get("dur_s", 0.0)
            if e["scene"] in awaiting:      # tempo que a traducao/back levou fora do processo (sessao)
                sc["wait_s"] = round(sc["wait_s"] + max(0.0, start - awaiting.pop(e["scene"])), 3)
            if res.startswith("awaiting"):
                awaiting[e["scene"]] = e["t"]
    return {"scenes": scenes, "gates": gates, "failures": failures, "n_events": len(evs),
            "runs": len({e.get("run") for e in evs}), "split": cost["split"], "by_activity": cost["by_activity"]}


def _when(t) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(t)) if t else "-"


TOP = 10      # visao enxuta: a tabela inteira na janela da sessao e contexto relido a cada comando seguinte


def _fmt(rep: dict, only: str | None = None, full: bool = False) -> str:
    L = [f"OBSERVABILIDADE — {len(rep['scenes'])} cena(s), {rep['n_events']} evento(s) em {rep['runs']} execucao(oes)",
         "  cena           status     linhas high back  overfl exec vfail | pack  trad  plano verif back  espera | sessao tok  equiv $"]
    rows = sorted(rep["scenes"].items())
    if not full and not only and len(rows) > TOP:
        bad = [r for r in rows if r[1]["status"] != "verified" or r[1]["verify_fails"] or r[1]["overflow"]]
        dear = sorted(rows, key=lambda r: -(r[1]["session_equiv_usd"] + r[1]["cost_usd"]))[:TOP]
        shown = sorted(dict(bad[:TOP] + dear).items())
        L.append(f"  (enxuto: {len(shown)} de {len(rows)} cenas — nao verificadas/com falha e as {TOP} mais caras;"
                 f" {len(bad)} com problema; --all mostra todas)")
        rows = shown
    for name, s in rows:
        if only and name != only:
            continue
        d = s["dur_s"]
        bp = f"{100 * s['back_pass_rate']:.0f}%" if s["back_pass_rate"] is not None else "-"
        L.append(f"  {name:14s} {str(s['status'])[:10]:10s} {s['n_lines'] or 0:6d} {s['high'] or 0:4d} {bp:>5s} "
                 f"{'-' if s['overflow'] is None else s['overflow']:>6} {s['runs']:4d} {s['verify_fails']:5d} | "
                 f"{d['pack']:5.1f} {d['translate']:5.1f} {d['build_plan']:5.1f} {d['verify']:5.1f} {d['back_translate']:5.1f} "
                 f"{s['wait_s']:6.0f} | {s['session_tokens']:10,} {s['session_equiv_usd'] + s['cost_usd']:8.4f}")
    L.append("  (tempos em segundos; `espera` = intervalo em que a cena ficou AGUARDANDO a sessao traduzir/revisar;"
             " `-` = sem evento ainda)")
    sp = rep["split"]
    tg = sp["translate"] + sp["governance"]
    if tg:
        L.append(f"  traducao:governanca = {100 * sp['translate'] / tg:.0f}:{100 * sp['governance'] / tg:.0f} "
                 f"(resto, fora da conta: ${sp['other']:.2f})")
    if rep["by_activity"]:
        L.append("  resto por atividade (heuristico): " + ", ".join(
            f"{k} ${v['usd']:.2f}" for k, v in rep["by_activity"].items()))
    L.append("  gates e auditorias:")
    for g, v in sorted(rep["gates"].items()):
        L.append(f"    {g:16s} ultimo={v['last']:6s} em {_when(v['last_t'])} | passou {v['pass']}x, bloqueou {v['block']}x")
    L.append(f"  falhas e bloqueios: {len(rep['failures'])}")
    for f in rep["failures"][-10:]:
        L.append(f"    {_when(f['t'])} run={f['run']} {f['scene'] or '-':12s} {f['stage']}/{f['result']} "
                 + (str(f.get('error') or '')))
    return "\n".join(L)


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Visao unica de observabilidade (cenas, gates, falhas).")
    ap.add_argument("project")
    ap.add_argument("--scene")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--all", action="store_true", help="tabela com todas as cenas (padrao: enxuto)")
    a = ap.parse_args()
    rep = report(a.project)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else _fmt(rep, a.scene, a.all))


if __name__ == "__main__":
    main()
