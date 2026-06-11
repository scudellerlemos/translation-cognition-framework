#!/usr/bin/env python3
"""
run_chapter.py — DRIVER de capitulo (tira o loop de cenas do chat).

Roda todas as cenas de um capitulo como jobs stateless, em sequencia, via run_scene. Cada cena e uma
requisicao isolada (backend api -> 1 chamada HTTP por cena); o chat so LANCA este driver e LE o resumo,
entao o footprint de sessao e constante, independente do nº de cenas/capitulos.

Propriedades:
  - RESUMIVEL: pula cenas ja `verified` em run_state.json (a menos de --redo).
  - PARA NA 1ª FALHA: build_plan/verify/api falhou -> interrompe e reporta (nao mascara erro).
  - Determinista: descobre as cenas por glob de artifacts/ch_<cap>_*/dialogs.csv (ordem por scene_id).
  - Reusa run_scene + state_index; nada de logica de IA aqui.

Uso:  python run_chapter.py <projeto> <cap> [--backend api|in-session] [--require-back] [--redo] [--no-verify]
      <cap> = "12" roda ch_12_01, ch_12_02, ... na ordem.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack   # noqa: E402
import run_scene as RS  # noqa: E402
import cost_report     # noqa: E402
import model as M      # noqa: E402
import kb_gate         # noqa: E402

_OK = ("verified", "planned")          # estados que permitem seguir p/ a proxima cena
_DONE = ("verified",)                  # estados que contam como "ja feito" (skip em modo resumivel)


def _scenes_of(root: Path, chap: str) -> list[str]:
    art = root / "artifacts"
    names = [p.parent.name for p in art.glob(f"ch_{chap}_*/dialogs.csv")]
    return sorted(set(names), key=context_pack.scene_id_of)


def _verified(root: Path, scene: str) -> bool:
    p = root / "artifacts" / "run_state.json"
    if not p.is_file():
        return False
    st = json.loads(p.read_text(encoding="utf-8")).get("scenes", {}).get(scene, {})
    return st.get("status") in _DONE and st.get("verified") is True


def _batch_phase(root, pending, *, skip_kb_gate):
    """FASE 1 do modo batch: submete as cenas pendentes (que passam o KB-gate) num unico batch (50% off,
    Carta cacheada compartilhada). Retorna {scene: status} do batch_translate. Cenas KB-bloqueadas ou
    que falham cobertura caem p/ o caminho interativo na fase 2 (run_scene normal). Best-effort: se o
    batch em si falhar (rede), retorna {} e tudo vira caminho interativo."""
    submit = []
    for s in pending:
        kb = kb_gate.check(root, s)
        if kb["problems"] and not skip_kb_gate:
            print(f"[batch] {s} pulado do batch (KB-gate): {kb['problems'][0]}")
            continue
        submit.append(s)
    if not submit:
        return {}
    print(f"[batch] submetendo {len(submit)} cena(s) em 1 batch (50% off; pode levar minutos) ...")
    try:
        st = M.batch_translate(root, submit)
    except Exception as e:
        print(f"[batch] falhou ({e}) -> caindo p/ caminho interativo em todas as cenas.")
        return {}
    for s in submit:
        print(f"[batch] {s}: {st.get(s, '?')}")
    return st


def _back_batch_phase(root, scenes):
    """POS-PASSE do modo batch: back-translation de todas as cenas verificadas num UNICO batch (-50%
    Opus). Roda DEPOIS do loop (cada cena ja produziu seu translation_plan); report-only (nao bloqueia).
    Resume idempotente dentro do batch_back_translate (cena ja revisada nao re-cobra)."""
    if not scenes:
        return
    print(f"\n[back-batch] back-translation de {len(scenes)} cena(s) em 1 batch (50% off, Opus) ...")
    try:
        st = M.batch_back_translate(root, scenes)
    except Exception as e:
        print(f"[back-batch] falhou ({e}) — back-translation segue pendente (report-only, nao bloqueia).")
        return
    rev = sum(1 for v in st.values() if v == "reviewed")
    noh = sum(1 for v in st.values() if v == "no_high")
    print(f"[back-batch] {rev} revisada(s), {noh} sem alto risco; detalhe: "
          f"{ {s: v for s, v in st.items() if v not in ('no_high',)} }")


def run_chapter(root, chap, *, backend="api", require_back=False, redo=False, do_verify=True,
                skip_kb_gate=False, batch=False):
    root = Path(root)
    scenes = _scenes_of(root, chap)
    if not scenes:
        print(f"nenhuma cena encontrada p/ cap {chap} (esperado artifacts/ch_{chap}_*/dialogs.csv)")
        return {"chapter": chap, "scenes": [], "status": "empty"}
    print(f"capitulo {chap}: {len(scenes)} cena(s) -> {', '.join(scenes)}")

    # MODO BATCH: traduz todas as pendentes num batch (fase 1); a fase 2 so finaliza (build_plan/verify).
    batch_status = {}
    if batch and backend == "api":
        pending = [s for s in scenes if redo or not _verified(root, s)]
        if pending:
            batch_status = _batch_phase(root, pending, skip_kb_gate=skip_kb_gate)

    results = []
    for scene in scenes:
        if not redo and _verified(root, scene):
            print(f"[skip] {scene} ja verified")
            results.append({"scene": scene, "status": "skipped"})
            continue
        pre = batch_status.get(scene) in ("written", "all_reused")
        # MODO BATCH: difere a back-translation p/ o pos-passe (1 batch -50% Opus ao fim do capitulo).
        defer_back = bool(batch and backend == "api")
        print(f"\n=== {scene} ({backend}{', batch' if pre else ''}) ===")
        r = RS.run_scene(root, scene, backend=backend, require_back=require_back,
                         do_verify=do_verify, skip_kb_gate=skip_kb_gate, pretranslated=pre,
                         defer_back=defer_back)
        results.append({"scene": scene, "status": r["status"]})
        if r["status"] not in _OK:
            print(f"\nPAROU em {scene}: status = {r['status']} "
                  f"(corrija e rode de novo; cenas verified serao puladas)")
            _print_cost(root)
            return {"chapter": chap, "scenes": results, "status": "stopped", "stopped_at": scene}
    # POS-PASSE: back-translation em batch (-50% Opus) das cenas verificadas, se modo batch.
    if batch and backend == "api":
        _back_batch_phase(root, [s for s in scenes if _verified(root, s)])
    done = sum(1 for x in results if x["status"] in ("verified", "skipped"))
    print(f"\nOK capitulo {chap}: {done}/{len(scenes)} cena(s) prontas.")
    _print_cost(root)
    return {"chapter": chap, "scenes": results, "status": "complete"}


def _print_cost(root: Path):
    """Resumo de gasto REAL (api_ledger.jsonl) ao fim do capitulo — protege o saldo (toda chamada
    cobrada conta, inclusive cenas que falharam/escalaram, nao so as que o metrics.jsonl registrou)."""
    try:
        rep = cost_report.report(root)
        if rep["n_calls"]:
            print(f"\n{cost_report._fmt(rep, by_scene=False)}")
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="Driver determinista de capitulo (loop de cenas).")
    ap.add_argument("project")
    ap.add_argument("chapter", help='prefixo do capitulo, ex.: "12"')
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--require-back", action="store_true")
    ap.add_argument("--redo", action="store_true", help="reprocessa mesmo cenas ja verified")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--skip-kb-gate", action="store_true", help="ignora o gate de cobertura de KB")
    ap.add_argument("--batch", action="store_true",
                    help="traduz todas as cenas pendentes num unico batch (50%% off, assincrono)")
    a = ap.parse_args()
    r = run_chapter(a.project, a.chapter, backend=a.backend, require_back=a.require_back,
                    redo=a.redo, do_verify=not a.no_verify, skip_kb_gate=a.skip_kb_gate, batch=a.batch)
    sys.exit(0 if r["status"] in ("complete", "empty") else 1)


if __name__ == "__main__":
    main()
