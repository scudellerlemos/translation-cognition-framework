#!/usr/bin/env python3
"""
quality_fix.py — PASSE DIRIGIDO de re-traducao das linhas 'revise' (risco #1, lado corretivo).

O `quality_gate --export` produz uma worklist (CSV) das linhas high/critical que a back-translation
marcou `revise` (divergencia de sentido/voz/ambiguidade) — e ate corrupcao crua (ex.: um grito que o
batch transformou em 5872 chars de lixo). Este script LE essa worklist (dados) e re-traduz APENAS
aqueles offsets, anexando ao prompt o feedback da back-translation, e MESCLA de volta — sem tocar nas
outras linhas.

Reusa a maquinaria cirurgica que ja existe (`model.retranslate_offsets`, usada no escalonamento de
fitting): re-traduz um subconjunto FRESCO (dedup-TM off), apertado por `budget_tolerance=1.0` (o fitting
forca o caso patologico a caber). Atualiza `translations_<id>.json` (o que o reinsert usa) E o
`base_translation` no `translation_plan_<id>.json` (coerencia da TM no proximo rebuild).

GOVERNANCA: a worklist e DADO (IA propoe via quality_gate; humano revisa o CSV; este script aplica).
Sem work-text no .py — as notas corretivas vem do back_translation. Dry-run por padrao; `--apply` grava.

DEPOIS de --apply (loop governado): `verify_chapter` de cada cap. afetado (re-traducao pode crescer e
estourar o byte_budget -> round-trip/charset/fitting tem que seguir verde) e `state_index --rebuild`.

Uso:  python quality_fix.py <projeto> <worklist.csv> [--apply] [--model M] [--json]
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import model          # noqa: E402
import paths          # noqa: E402


def load_worklist(csv_path) -> dict:
    """Le o CSV do quality_gate --export -> {scene: [{offset, note, back_en, source, target}]}.
    Ignora linhas sem scene/offset."""
    p = Path(csv_path)
    if not p.is_file():
        raise FileNotFoundError(f"worklist nao encontrada: {csv_path}")
    by_scene = {}
    with p.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            scene, off = (r.get("scene") or "").strip(), (r.get("offset") or "").strip()
            if not scene or not off:
                continue
            by_scene.setdefault(scene, []).append({
                "offset": off, "note": (r.get("note") or "").strip(),
                "back_en": (r.get("back_en") or "").strip(),
                "source": (r.get("source") or "").strip(), "target": (r.get("target") or "").strip()})
    return by_scene


def _quality_note(items) -> str:
    """Bloco corretivo p/ o prompt a partir das observacoes da back-translation (dados, nao work-text)."""
    L = ["\n\n## REVISAO DE QUALIDADE (a back-translation apontou divergencia nestes offsets)",
         "Reescreva CADA um preservando sentido EXATO, voz do falante e ambiguidade do original; "
         "mantenha o nº e a posicao do token de quebra. Observacoes:"]
    for it in items:
        obs = it["note"] or "divergencia apontada"
        L.append(f"- {it['offset']}: {obs}")
    return "\n".join(L)


def plan(root, worklist) -> list[dict]:
    """DRY-RUN: o que seria re-traduzido. [{scene, offsets, notes}]. Sem rede."""
    out = []
    for scene in sorted(worklist):
        items = worklist[scene]
        out.append({"scene": scene, "offsets": [i["offset"] for i in items],
                    "notes": [f"{i['offset']}: {i['note']}" for i in items]})
    return out


def _update_plan_base(root, scene, offsets):
    """Apos o merge em translations, espelha o novo `t` no `base_translation` do translation_plan
    (coerencia da TM). Le translations + plan; atualiza so os offsets tocados."""
    sid = context_pack.scene_id_of(scene)
    tf, pf = paths.translations(root, scene, sid), paths.translation_plan(root, scene, sid)
    if not tf.is_file() or not pf.is_file():
        return 0
    tmap = json.loads(tf.read_text(encoding="utf-8")).get("lines", {})
    pdata = json.loads(pf.read_text(encoding="utf-8"))
    n = 0
    for ln in pdata.get("lines", []):
        off = ln.get("offset", "")
        if off in offsets and off in tmap:
            new_t = (tmap[off] or {}).get("t", "")
            if new_t and ln.get("base_translation") != new_t:
                ln["base_translation"] = new_t
                n += 1
    if n:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding="utf-8")
    return n


def apply(root, worklist, *, model_name=None, max_usd=None) -> dict:
    """Re-traduz dirigido cada cena da worklist (PAGO) e mescla. `max_usd` = teto de gasto: antes de cada
    cena, se o custo acumulado ja atingiu o teto, PARA (stopped_budget=True). Retorna
    {scenes, offsets, cost_usd, stopped_budget, scenes_left}."""
    root = Path(root)
    m = model_name or model.MODEL_TRANSLATE
    scenes_done, offs_done, cost = 0, 0, 0.0
    order = sorted(worklist)
    stopped = False
    for i, scene in enumerate(order):
        if max_usd is not None and cost >= max_usd:
            stopped = True
            return {"scenes": scenes_done, "offsets": offs_done, "cost_usd": round(cost, 4),
                    "stopped_budget": True, "scenes_left": len(order) - i}
        items = worklist[scene]
        offsets = [i2["offset"] for i2 in items]
        note = _quality_note(items)
        res = model.retranslate_offsets(root, scene, offsets, model=m,
                                        budget_tolerance=1.0, quality_note=note)
        if res.get("usage"):
            cost += model.cost_of(m, res["usage"])
        _update_plan_base(root, scene, set(offsets))
        scenes_done += 1
        offs_done += len(offsets)
    return {"scenes": scenes_done, "offsets": offs_done, "cost_usd": round(cost, 4),
            "stopped_budget": stopped, "scenes_left": 0}


def main():
    ap = argparse.ArgumentParser(description="Re-traducao dirigida das linhas 'revise' (dados propoem; script aplica).")
    ap.add_argument("project")
    ap.add_argument("worklist", help="CSV do quality_gate --export")
    ap.add_argument("--apply", action="store_true", help="grava (PAGO; default: dry-run)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--max-usd", type=float, default=None, help="teto de gasto (PARA ao atingir)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    wl = load_worklist(a.worklist)
    if not wl:
        print("worklist vazia (nada a re-traduzir).")
        sys.exit(0)
    total = sum(len(v) for v in wl.values())
    if not a.apply:
        pl = plan(a.project, wl)
        if a.json:
            print(json.dumps(pl, ensure_ascii=False, indent=2))
        else:
            print(f"DRY-RUN: {total} linha(s) em {len(wl)} cena(s) seriam re-traduzidas. Nada gravado.")
            for p in pl:
                print(f"  {p['scene']}: {len(p['offsets'])} offset(s) -> {p['offsets']}")
        sys.exit(0)
    cap = f" | teto ${a.max_usd:.2f}" if a.max_usd is not None else ""
    print(f"[quality_fix] re-traduzindo {total} linha(s) em {len(wl)} cena(s) (PAGO){cap} ...")
    r = apply(a.project, wl, model_name=a.model, max_usd=a.max_usd)
    print(f"[quality_fix] OK: {r['offsets']} offset(s) em {r['scenes']} cena(s) | custo ~${r['cost_usd']:.4f}")
    if r.get("stopped_budget"):
        print(f"[quality_fix] PAROU no teto de ${a.max_usd:.2f} — {r['scenes_left']} cena(s) nao processadas. "
              "Re-rode (resume) com mais orcamento p/ continuar.")
    print("Proximos passos (loop governado):")
    print("  1) verify_chapter de cada cap. afetado  # round-trip/charset/fitting tem que seguir verde")
    print(f"  2) python {Path(__file__).with_name('state_index.py').name} {a.project} --rebuild  # TM reflete")
    print(f"  3) python {Path(__file__).with_name('quality_gate.py').name} {a.project}  # confere 'revise' reduzido")
    sys.exit(0)


if __name__ == "__main__":
    main()
