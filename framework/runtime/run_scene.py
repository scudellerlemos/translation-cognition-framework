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


def run_scene(root, scene, *, backend="in-session", require_back=False, do_verify=True):
    root = Path(root)
    cfg = json.loads((root / "project.json").read_text(encoding="utf-8"))
    sfx = context_pack.sfx_of(scene)
    print(f"[1/6] context_pack {scene} ...")
    tr = M.translate(root, scene, backend=backend)
    print(f"      glossario/vozes/decisoes/TM montados; status traducao = {tr['status']}")
    _checkpoint(root, scene, {"sfx": sfx, "n_lines": tr["n_lines"], "status": "packed"})

    if tr["status"] == M.AWAITING:
        print(f"[2/6] AGUARDANDO traducao (caminho assinatura): responda o prompt limitado")
        print(f"      prompt : {tr['prompt']}")
        print(f"      saida  : {tr['expected_output']}")
        print("      -> rode novamente apos o arquivo aparecer. (checkpoint: 'packed')")
        return {"status": "awaiting_translation", "scene": scene}
    print(f"[2/6] traducao presente ({tr['status']}).")

    print(f"[3/6] build_plan_chapter {scene} ...")
    bp = _connector_script(root, cfg, "build_plan_script", "build_plan_chapter.py")
    code, out = _run([sys.executable, str(bp), scene])
    print(_indent(out))
    if code != 0:
        _checkpoint(root, scene, {"status": "build_plan_failed"})
        return {"status": "build_plan_failed", "scene": scene}
    _checkpoint(root, scene, {"status": "planned"})

    highs = _high_lines(root, scene, sfx)
    print(f"[4/6] back-translation: {len(highs)} linha(s) risco>=high")
    bt = M.back_translate(root, scene, highs, backend=backend)
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

    verified = None
    if do_verify:
        print(f"[5/6] verify_chapter {scene} (round-trip) ...")
        vf = _connector_script(root, cfg, "verify_script", "verify_chapter.py")
        code, out = _run([sys.executable, str(vf), scene])
        print(_indent(out))
        verified = (code == 0)
        if not verified:
            _checkpoint(root, scene, {"status": "verify_failed", "verified": False})
            return {"status": "verify_failed", "scene": scene}
        _checkpoint(root, scene, {"status": "verified", "verified": True})
    else:
        print("[5/6] verify pulado (--no-verify).")

    print("[6/6] reconstruindo state_index (TM cresce com esta cena) ...")
    si = state_index.build(root)
    print(f"      TM: {si['tm']} entradas | cards: {si['cards']} | decisoes: {si['decisions']}")
    _checkpoint(root, scene, {"status": "verified" if verified else "planned"})
    print(f"OK run_scene {scene}: status final = {'verified' if verified else 'planned'}")
    return {"status": "verified" if verified else "planned", "scene": scene,
            "high": len(highs), "verified": verified}


def _indent(s: str) -> str:
    return "\n".join("      " + ln for ln in s.strip().splitlines() if ln.strip())


def main():
    ap = argparse.ArgumentParser(description="Orquestrador determinista de 1 cena.")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="in-session", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true",
                    help="bloqueia se a back-translation de alto risco faltar")
    ap.add_argument("--no-verify", action="store_true", help="pula o round-trip (verify_chapter)")
    a = ap.parse_args()
    r = run_scene(a.project, a.scene, backend=a.backend,
                  require_back=a.require_back, do_verify=not a.no_verify)
    sys.exit(0 if r["status"] in ("verified", "planned", "awaiting_translation",
                                  "awaiting_back_translation") else 1)


if __name__ == "__main__":
    main()
