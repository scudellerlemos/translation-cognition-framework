#!/usr/bin/env python3
"""
quality_gate.py — PISO DE QUALIDADE observavel (risco #2: ate aqui nao havia piso).

O round-trip byte-identico prova que os BYTES voltam — prova plumbing, NAO traducao. O unico sinal
de QUALIDADE que o pipeline ja produz e a back-translation: nas linhas high/critical, um modelo forte
(Opus) traduz o pt-BR de volta p/ EN, compara com o source e emite `verdict: pass|revise` + `note`.
Mas esse sinal era REPORT-ONLY: ficava no `back_translation_<id>.json` em disco e ninguem lia de volta.
Um `verdict: revise` (o proprio modelo dizendo "sentido/voz/ambiguidade divergiu") passava silencioso.

Este gate torna o sinal OBSERVAVEL e BLOQUEANTE (mesma logica observavel do spoiler_check.py). Varre as
back_translation ja gravadas e o translation_plan de cada cena e levanta DOIS problemas:

  (R) REVISE  — linha high/critical onde o verdict do back-translate foi 'revise' (divergencia real
                apontada pelo modelo). E o coracao do piso: a traducao precisa de revisao humana.
  (U) UNCOVERED — linha high/critical SEM entry de back-translation (buraco silencioso na rede: o
                  back-batch pulou, deu parse_failed, ou a cena nunca foi revisada). Risco = a linha
                  mais critica passou sem o unico crivo de qualidade que temos.

ESCOPO HONESTO: cobre as linhas high/critical (as que sao back-translatadas). As linhas low/medium —
inclusive boa parte das single-line roteadas p/ o tier Haiku barato — NAO tem back-translation e logo
nao tem piso aqui; o crivo delas e o risco_level atribuido no plano + o round-trip. Elevar a cobertura
(amostragem das low, ou um juiz barato) e extensao futura (ver ROADMAP). Governanca: read-only, sem
rede, sem work-text — le artefato ja pago.

Uso:  python quality_gate.py <projeto> [<capitulo>] [--scenes C1 C2 ...] [--json]   (exit 1 se houver revise/uncovered)
Com `--scenes` (o `wave.py` passa as cenas da onda) so bloqueia o que e dessas cenas; o resto sai como AVISO.
O bloqueio global nao some: o `wave.py` recusa abrir onda nova com escalonamento aberto de outra cena.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io  # noqa: E402  (leitura compartilhada: scenes/plan_lines/back_entries)
import context_pack  # noqa: E402
import model  # noqa: E402
import paths  # noqa: E402


def check(root, chapter=None) -> dict:
    """Retorna {'revise', 'uncovered', 'coverage'} cruzando back_translation x high/critical do plano.
    So considera cenas com translation_plan em disco (ja planejadas). chapter=None varre tudo.

    Cada item de 'revise':   {scene, scene_id, offset, speaker, source, target, back_en, note}
    Cada item de 'uncovered': {scene, scene_id, offset, speaker, source, target, risk, reason}
    'coverage': {lines, high, with_back, sampled_low, pct} — torna o ponto cego do tier barato MEDIDO.
    """
    root = Path(root)
    revise, uncovered = [], []
    cov: dict[str, float] = {"lines": 0, "high": 0, "with_back": 0, "sampled_low": 0}
    for scene in artifact_io.scenes(root, chapter):
        plan_lines = model._plan_lines(root, scene)       # le translation_plan; [] se sem plano
        if not plan_lines:
            continue
        sid = context_pack.scene_id_of(scene)
        highs = [model._ln_entry(ln) for ln in plan_lines
                 if ln.get("risk_level") in ("high", "critical")]
        high_offsets = {h["offset"] for h in highs}
        entries = artifact_io.back_entries(root, scene)
        bt_missing = not paths.back_translation(root, scene, sid).is_file()
        valid = {off: e for off, e in entries.items() if not e.get("stale")}  # stale = julgou texto antigo
        cov["lines"] += len(plan_lines)
        cov["high"] += len(highs)
        cov["with_back"] += len(valid)
        cov["sampled_low"] += sum(1 for off in valid if off not in high_offsets)  # amostra das low/medium
        for h in highs:
            off = h["offset"]
            e = entries.get(off)
            if e is None or e.get("stale"):
                uncovered.append({
                    "scene": scene, "scene_id": sid, "offset": off, "speaker": h.get("speaker", ""),
                    "source": h.get("source", ""), "target": h.get("target", ""),
                    "risk": h.get("risk_notes", ""),
                    "reason": "back_translation STALE (cena re-traduzida; re-julgar)" if (e and e.get("stale"))
                    else ("sem back_translation (back-batch pulou/parse_failed)" if bt_missing
                          else "offset ausente nas entries do back_translation")})
            elif e.get("verdict") == "revise":
                revise.append({
                    "scene": scene, "scene_id": sid, "offset": off, "speaker": h.get("speaker", ""),
                    "source": h.get("source", ""), "target": h.get("target", ""),
                    "back_en": e.get("back_en", ""), "note": e.get("note", "")})
    cov["pct"] = round(100.0 * cov["with_back"] / cov["lines"], 1) if cov["lines"] else 0.0
    return {"revise": revise, "uncovered": uncovered, "coverage": cov}


def split_scope(items: list[dict], scenes: list[str] | None) -> tuple[list[dict], list[dict]]:
    """(bloqueia, avisa): sem `scenes` tudo bloqueia; com `scenes`, so o item das cenas do pedido."""
    if not scenes:
        return items, []
    want = set(scenes)
    return [i for i in items if i.get("scene") in want], [i for i in items if i.get("scene") not in want]


def export_revise(revise, csv_path):
    """Grava a worklist 'revise' como DADOS (entrada do quality_fix). Colunas estaveis."""
    import csv
    cols = ["scene", "scene_id", "offset", "speaker", "source", "target", "back_en", "note"]
    with Path(csv_path).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in revise:
            w.writerow({c: r.get(c, "") for c in cols})
    return len(revise)


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):  # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Piso de qualidade observavel (verdicts de back-translation).")
    ap.add_argument("project")
    ap.add_argument("chapter", nargs="?", default=None, help="filtra por capitulo (ex.: 19); default: tudo")
    ap.add_argument("--scenes", nargs="+", help="so bloqueia item destas cenas; o resto vira aviso")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--export", metavar="CSV", default=None,
                    help="grava a worklist 'revise' nesse CSV (entrada do quality_fix)")
    a = ap.parse_args()
    paths.require_project(a.project)
    r = check(a.project, a.chapter)
    cov = r["coverage"]
    rev, rev_out = split_scope(r["revise"], a.scenes)
    unc, unc_out = split_scope(r["uncovered"], a.scenes)
    import hitl  # fila de escalonamento aberta = decisao humana pendente -> bloqueia (projeto com "hitl")
    esc, esc_out = split_scope(hitl.open_items(a.project) if hitl.enabled(a.project) else [], a.scenes)
    r["escalations"] = len(esc)
    outside = len(rev_out) + len(unc_out) + len(esc_out)
    if outside:
        r["outside"] = {"revise": len(rev_out), "uncovered": len(unc_out), "escalations": len(esc_out)}
        where = sorted({i["scene"] for i in rev_out + unc_out + esc_out})
        print(f"AVISO: {outside} pendencia(s) fora das cenas do pedido (nao bloqueiam esta onda, "
              f"bloqueiam a proxima): {', '.join(where)}")
    if a.export:
        n = export_revise(r["revise"], a.export)
        print(f"[export] {n} linha(s) 'revise' -> {a.export}")
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(1 if (rev or unc or esc) else 0)
    print(f"[cobertura] {cov['with_back']}/{cov['lines']} linha(s) com crivo de qualidade "
          f"({cov['pct']}%) | high/critical={cov['high']} + amostra low/medium={cov['sampled_low']}")
    if not rev and not unc and not esc:
        scope = f"cap.{a.chapter}" if a.chapter else "todos os capitulos"
        print(f"OK: nenhuma linha high/critical com verdict 'revise' nem sem cobertura ({scope}).")
        sys.exit(0)
    if rev:
        print(f"REVISAR — {len(rev)} linha(s) high/critical com verdict 'revise' (o modelo apontou divergencia):")
        for k in rev:
            print(f"  {k['scene']} {k['offset']} ({k['speaker']}): {k['note'][:100]}")
            print(f"      src : {k['source'][:90]}")
            print(f"      pt  : {k['target'][:90]}")
            print(f"      back: {k['back_en'][:90]}")
    if unc:
        print(f"SEM COBERTURA — {len(unc)} linha(s) high/critical sem back-translation:")
        for k in unc:
            print(f"  {k['scene']} {k['offset']} ({k['speaker']}): {k['reason']}")
            print(f"      pt  : {k['target'][:90]}")
    if esc:
        print(f"ESCALONAMENTO — {len(esc)} fala(s) esperando decisao humana em {hitl.queue_path(Path(a.project))} "
              f"(preencha alias ou correcao e rode hitl.py resolve).")
    sys.exit(1)


if __name__ == "__main__":
    main()
