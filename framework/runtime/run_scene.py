#!/usr/bin/env python3
"""
run_scene.py — ORQUESTRADOR DETERMINISTA de UMA cena (tira a orquestracao do chat).

Encadeia o pipeline de 1 cena como um job limitado e resumivel:
  1. context_pack  -> scene_prompt.md + pack.json (contexto O(cena), nao O(historico))
  2. translate     -> model.translate (in-session: espera o translations_<sfx>.json; api: gera)
  3. build_plan    -> connector/build_plan_chapter.py (valida cobertura/tokens/risk_notes; gera approved)
  4. back-translate-> linhas risco>=high (model.back_translate; REPORTA por padrao, --require-back exige)
  5. verify        -> connector/verify_chapter.py (round-trip byte-identico + ponteiros within-file)
  6. checkpoint    -> artifacts/run_state.json (status por cena) + reconstroi o state_index (TM cresce)

O chat deixa de ser runtime/memoria: o estado vive em run_state.json + artifacts. Crash/parada ->
rode de novo; cada etapa e idempotente e o checkpoint diz onde retomar.

GOVERNANCA: sem work-text. Os scripts do conector sao por-projeto (convencao <projeto>/connector/,
override em project.json connector.{build_plan_script,verify_script}). A unica parte nao-determinista
e a chamada de IA (isolada em model.py). Sob CONGELAMENTO de traducao: nao gera traducao nova; roda
as gates sobre cenas ja traduzidas (dry-run/dogfood).

Uso:  python run_scene.py <dir-do-projeto> <scene> [--backend in-session|api] [--require-back] [--no-verify]
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack   # noqa: E402
import model as M      # noqa: E402
import state_index     # noqa: E402
import kb_gate         # noqa: E402


def _connector_script(root: Path, cfg: dict, key: str, default: str) -> Path:
    override = cfg.get("connector", {}).get(key)
    p = (root / override) if override else (root / "connector" / default)
    return p


def _run(cmd) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _checkpoint(root: Path, scene: str, patch: dict):
    p = root / "artifacts" / "run_state.json"
    state = {}
    if p.is_file():
        state = json.loads(p.read_text(encoding="utf-8"))
    scenes = state.setdefault("scenes", {})
    scenes[scene] = {**scenes.get(scene, {}), **patch}
    state["scenes"] = dict(sorted(scenes.items()))
    state["managed_by"] = "framework/runtime/run_scene.py"
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _ledger_scene_cost(root: Path, scene: str) -> float:
    """Custo-VERDADE da cena = soma de TODAS as chamadas no api_ledger.jsonl (cada retry de cobertura e
    cada escalonamento de fitting), nao so a ultima translate/back. E o numero que casa com o saldo."""
    p = root / "artifacts" / "api_ledger.jsonl"
    if not p.is_file():
        return 0.0
    tot = 0.0
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("scene") == scene:
            tot += r.get("cost_usd", 0.0)
    return round(tot, 5)


def _metrics(root: Path, scene: str, sfx: str, *, n_lines, tr, bt, n_high, verified):
    """Anexa 1 linha a artifacts/metrics.jsonl: RESUMO por cena (tokens/custo segmentados da ultima
    translate/back, pass-rate). O custo-verdade (`cost_usd`) vem do api_ledger.jsonl — soma TODAS as
    chamadas cobradas da cena (retries + escalonamento), nao so a ultima. O metrics.jsonl segue sendo
    resumo so-de-sucesso; a contabilidade completa (inclusive cenas que falharam) e o ledger."""
    tu = tr.get("usage") if isinstance(tr, dict) else None
    bu = bt.get("usage") if isinstance(bt, dict) else None
    tmodel = tr.get("model", "") if isinstance(tr, dict) else ""
    bmodel = bt.get("model", "") if isinstance(bt, dict) else ""
    # back-translation pass-rate (se houve saida)
    bt_pass = None
    bpath = root / "artifacts" / scene / f"back_translation_{sfx}.json"
    if bpath.is_file():
        try:
            ents = json.loads(bpath.read_text(encoding="utf-8")).get("entries", [])
            if ents:
                bt_pass = sum(1 for e in ents if e.get("verdict") == "pass") / len(ents)
        except Exception:
            pass
    rec = {"scene": scene, "n_lines": n_lines, "n_high": n_high, "verified": verified,
           "translate": {"model": tmodel, "usage": tu, "cost_usd": round(M.cost_of(tmodel, tu or {}), 5)},
           "back": {"model": bmodel, "usage": bu, "cost_usd": round(M.cost_of(bmodel, bu or {}), 5)},
           "back_pass_rate": bt_pass,
           "cost_usd_last": round(M.cost_of(tmodel, tu or {}) + M.cost_of(bmodel, bu or {}), 5)}
    rec["cost_usd"] = _ledger_scene_cost(root, scene)   # VERDADE: soma o ledger (retries + escalonamento)
    p = root / "artifacts" / "metrics.jsonl"
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def _high_lines(root: Path, scene: str, sfx: str):
    plan = root / "artifacts" / scene / f"translation_plan_{sfx}.json"
    if not plan.is_file():
        return []
    lines = json.loads(plan.read_text(encoding="utf-8")).get("lines", [])
    out = []
    for ln in lines:
        if ln.get("risk_level") in ("high", "critical"):
            out.append({"offset": ln.get("offset", ""), "source": ln.get("text_source", ""),
                        "target": ln.get("base_translation", ""), "speaker": ln.get("speaker", ""),
                        "risk_notes": ln.get("risk_notes", "")})
    return out


def run_scene(root, scene, *, backend="api", require_back=False, do_verify=True, skip_kb_gate=False):
    root = Path(root)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    sfx = context_pack.sfx_of(scene)

    # GATE DE COBERTURA DE KB (cabeia a doutrina: pesquisa reconciliada ANTES de traduzir)
    kb = kb_gate.check(root, scene)
    for w in kb["warnings"]:
        print(f"[kb] aviso: {w}")
    if kb["problems"] and not skip_kb_gate:
        print(f"[0/6] BLOQUEADO por cobertura de KB ({len(kb['problems'])}):")
        for p in kb["problems"]:
            print(f"      - {p}")
        print("      -> rode a Fase 0 (skill 03) ou use --skip-kb-gate p/ ignorar (nao recomendado).")
        _checkpoint(root, scene, {"sfx": sfx, "status": "kb_coverage_failed"})
        return {"status": "kb_coverage_failed", "scene": scene, "problems": kb["problems"]}

    print(f"[1/6] context_pack {scene} ...")
    try:
        tr = M.translate(root, scene, backend=backend)
    except Exception as e:                                  # backend api: erro de rede/saida invalida
        print(f"      ERRO na traducao ({backend}): {e}")
        _checkpoint(root, scene, {"sfx": sfx, "status": "api_translate_failed"})
        return {"status": "api_translate_failed", "scene": scene, "error": str(e)}
    print(f"      glossario/vozes/decisoes/TM montados; status traducao = {tr['status']}")
    _checkpoint(root, scene, {"sfx": sfx, "n_lines": tr["n_lines"], "status": "packed"})

    if tr["status"] == M.AWAITING:
        print(f"[2/6] AGUARDANDO traducao (caminho assinatura): responda o prompt limitado")
        print(f"      prompt : {tr['prompt']}")
        print(f"      saida  : {tr['expected_output']}")
        print("      -> rode novamente apos o arquivo aparecer. (checkpoint: 'packed')")
        return {"status": "awaiting_translation", "scene": scene}
    print(f"[2/6] traducao presente ({tr['status']}).")

    # [3+5] build_plan + verify com ESCALONAMENTO DE FITTING: budget 1.40 (natural) por padrao; se a
    # verify falha por fitting (out-of-file/residuo) e ha API, re-traduz mais apertado (BUDGET_ESCALATION)
    # e repete. Cenas normais passam de primeira (sem custo extra); so as apertadas escalam.
    bp = _connector_script(root, cfg, "build_plan_script", "build_plan_chapter.py")
    vf = _connector_script(root, cfg, "verify_script", "verify_chapter.py")
    tolerances = [None] + (list(M.BUDGET_ESCALATION) if backend == "api" else [])
    verified = None
    for ti, tol in enumerate(tolerances):
        if ti > 0:
            print(f"[retighten] verify falhou por fitting -> re-traduzindo budget_tolerance={tol} ...")
            try:
                tr = M.translate(root, scene, backend=backend, budget_tolerance=tol)
            except Exception as e:
                print(f"      ERRO na re-traducao ({backend}): {e}")
                _checkpoint(root, scene, {"status": "api_translate_failed"})
                return {"status": "api_translate_failed", "scene": scene, "error": str(e)}

        print(f"[3/6] build_plan_chapter {scene} ...")
        code, out = _run([sys.executable, str(bp), scene])
        print(_indent(out))
        if code != 0:
            _checkpoint(root, scene, {"status": "build_plan_failed"})
            return {"status": "build_plan_failed", "scene": scene}
        _checkpoint(root, scene, {"status": "planned"})

        if not do_verify:
            print("[5/6] verify pulado (--no-verify).")
            break
        print(f"[5/6] verify_chapter {scene} (round-trip) ...")
        code, out = _run([sys.executable, str(vf), scene])
        print(_indent(out))
        if code == 0:
            verified = True
            _checkpoint(root, scene, {"status": "verified", "verified": True})
            break
        low = out.lower()
        fitting = ("fora do arquivo" in low) or ("residuo t4" in low and "esperado 0" in low)
        if fitting and ti < len(tolerances) - 1:
            print("      verify falhou por FITTING (cena apertada); escalando aperto de budget ...")
            continue
        _checkpoint(root, scene, {"status": "verify_failed", "verified": False})
        return {"status": "verify_failed", "scene": scene}

    # [4/6] back-translation (apos fitting OK; report-only; roda 1x — nao re-roda no escalonamento)
    highs = _high_lines(root, scene, sfx)
    print(f"[4/6] back-translation: {len(highs)} linha(s) risco>=high")
    try:
        bt = M.back_translate(root, scene, highs, backend=backend)
    except Exception as e:                                  # nao-bloqueante: reporta e segue
        print(f"      AVISO: back-translation falhou ({backend}): {e} — seguindo (report-only).")
        bt = {"status": M.DONE, "reviewed": 0, "path": None}
        if require_back:                                    # so bloqueia se exigida explicitamente
            _checkpoint(root, scene, {"status": "back_translation_failed", "high": len(highs)})
            return {"status": "back_translation_failed", "scene": scene, "error": str(e)}
    if bt["status"] == M.AWAITING:
        msg = f"      AGUARDANDO back-translation: {bt['prompt']}"
        if require_back:
            print(msg + "  (--require-back: bloqueia)")
            _checkpoint(root, scene, {"status": "awaiting_back_translation", "high": len(highs)})
            return {"status": "awaiting_back_translation", "scene": scene}
        print(msg + "  (apenas reportado; use --require-back p/ bloquear)")
    elif bt["status"] == M.READY:
        print(f"      back-translation presente: {bt['path']}")
    else:
        print(f"      back-translation: {bt.get('reviewed',0)} revisada(s)")
    _checkpoint(root, scene, {"high": len(highs)})

    print("[6/6] reconstruindo state_index (TM cresce com esta cena) ...")
    si = state_index.build(root)
    print(f"      TM: {si['tm']} entradas | cards: {si['cards']} | decisoes: {si['decisions']}")
    _checkpoint(root, scene, {"status": "verified" if verified else "planned"})
    mr = _metrics(root, scene, sfx, n_lines=tr.get("n_lines"), tr=tr, bt=bt,
                  n_high=len(highs), verified=bool(verified))
    print(f"      metrics: custo ~${mr['cost_usd']:.4f} | back_pass_rate={mr['back_pass_rate']}")
    print(f"OK run_scene {scene}: status final = {'verified' if verified else 'planned'}")
    return {"status": "verified" if verified else "planned", "scene": scene,
            "high": len(highs), "verified": verified}


def _indent(s: str) -> str:
    return "\n".join("      " + ln for ln in s.strip().splitlines() if ln.strip())


def main():
    ap = argparse.ArgumentParser(description="Orquestrador determinista de 1 cena.")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true",
                    help="bloqueia se a back-translation de alto risco faltar")
    ap.add_argument("--no-verify", action="store_true", help="pula o round-trip (verify_chapter)")
    ap.add_argument("--skip-kb-gate", action="store_true",
                    help="ignora o gate de cobertura de KB (nao recomendado)")
    a = ap.parse_args()
    r = run_scene(a.project, a.scene, backend=a.backend, require_back=a.require_back,
                  do_verify=not a.no_verify, skip_kb_gate=a.skip_kb_gate)
    sys.exit(0 if r["status"] in ("verified", "planned", "awaiting_translation",
                                  "awaiting_back_translation") else 1)


if __name__ == "__main__":
    main()
