#!/usr/bin/env python3
"""
quality_review.py — REVISAO HUMANA por capitulo, sem IA-julga-IA (piso de qualidade de verdade).

A back-translation (Opus julgando Sonnet/Haiku) custa e nao substitui um humano lendo o pt-BR. Aqui o
humano E o juiz: o `export` gera UM CSV com o CAPITULO INTEIRO (todas as linhas, p/ leitura integral),
mas cada linha vem MARCADA de forma 100% DETERMINISTICA (sem IA) com uma tag dizendo ONDE avaliar —
risco alto, amostra do tier barato, ou flags baratas (identico-a-fonte=provavel nao-traduzido, outlier
de tamanho, `largura`=segmento estoura o balao no jogo, marcador pt-PT). Linha sem tag = passa o olho;
tag preenchida = "avalie aqui".

O humano devolve o MESMO CSV preenchendo, por linha:
  - coluna `correcao` = o texto certo  -> aplico VERBATIM (zero IA: so gate de charset/round-trip + merge);
  - coluna `nota` (sem correcao) = instrucao (ex.: "encurtar", "tom formal") -> IA re-traduz SO aquela
    linha seguindo a nota (cirurgico, nunca a cena inteira);
  - ambas vazias = aprovado, nao toco.

O `apply` processa EXATAMENTE o que foi marcado e re-verifica round-trip dos capitulos tocados. Governanca:
HUMANO propoe -> gate (charset/paridade/round-trip) aprova -> script aplica. Sem work-text no .py.

Uso:
  python quality_review.py export <projeto> <cap> [--out CSV]
  python quality_review.py apply  <projeto> <CSV-devolvido> [--model M]
"""
from __future__ import annotations
import argparse
import csv
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import artifact_io   # noqa: E402  (leitura compartilhada: scenes/translations_map)
import context_pack  # noqa: E402
import model          # noqa: E402
import paths          # noqa: E402

COLS = ["scene", "offset", "speaker", "risk", "revisar", "source_en", "target_pt", "correcao", "nota"]

# Marcadores pt-PT de ALTA precisao (raros no pt-BR falado) — heuristica, por isso a tag leva '?'.
_PTPT = re.compile(r"\b(tens|estás|fazes|podes|queres|deves|vês|hás)\b|\btem de\b|\bhás de\b", re.IGNORECASE)

# Largura do BALAO: o byte_budget garante que cabe no ARQUIVO (reinsercao), NAO que cabe na largura
# VISUAL do balao. Cada segmento entre tokens de quebra (`\n`) e UMA linha exibida; o pt-BR (~+25% vs
# EN) estoura linhas que no EN estavam no limite. Calibrado por QA in-game: o maior segmento EN que
# COUBE no corpus tem 62 chars transliterados -> usamos 60 (margem). Segmento pt-BR > isso = risco de
# sair do balao (o round-trip de bytes NAO pega isto).
WIDTH_MAX = 60


def _norm_cmp(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\\n", " ")).strip().lower()


def _flags(source: str, target: str, risk: str, sampled: bool) -> str:
    """Tags DETERMINISTICAS de 'onde avaliar' (sem IA). '' = linha sem sinal (passa o olho)."""
    fl = []
    if risk in ("high", "critical"):
        fl.append(f"risco:{risk}")
    if sampled:
        fl.append("amostra")
    if target and _norm_cmp(source) == _norm_cmp(target):
        fl.append("identico-fonte")                       # provavel nao-traduzido
    slen, tlen = model._translit_len(source), model._translit_len(target)
    if slen and (tlen > slen * 3 or (slen > 8 and tlen < slen * 0.4)):
        fl.append("tamanho")                              # outlier de comprimento
    if any(model._translit_len(seg) > WIDTH_MAX for seg in (target or "").split(context_pack.TOKEN)):
        fl.append("largura")                              # segmento estoura a largura do balao (in-game)
    if _PTPT.search(target or ""):
        fl.append("pt-PT?")
    return ";".join(fl)


def export(root, chapter) -> list[dict]:
    """CSV-rows do capitulo inteiro, cada linha marcada. Determinista (sem rede)."""
    root = Path(root)
    rows = []
    for scene in artifact_io.scenes(root, chapter):
        plan_lines = model._plan_lines(root, scene)
        if not plan_lines:
            continue
        tmap = artifact_io.translations_map(root, scene)
        sampled = {x["offset"] for x in model.sample_low_risk_lines(root, scene)}
        for ln in plan_lines:
            off = ln.get("offset", "")
            src = ln.get("text_source", "")
            tgt = (tmap.get(off) or {}).get("t", "") if isinstance(tmap.get(off), dict) \
                else ln.get("base_translation", "")
            risk = ln.get("risk_level", "")
            rows.append({"scene": scene, "offset": off, "speaker": ln.get("speaker", ""),
                         "risk": risk, "revisar": _flags(src, tgt, risk, off in sampled),
                         "source_en": src, "target_pt": tgt, "correcao": "", "nota": ""})
    return rows


def write_csv(rows, out_path):
    with Path(out_path).open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


def read_returned(csv_path) -> dict:
    """Le o CSV devolvido -> {scene: {'verbatim': [(offset, texto)], 'nota': [(offset, instrucao)]}}.
    So linhas com correcao OU nota preenchida entram."""
    by_scene = {}
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            scene, off = (r.get("scene") or "").strip(), (r.get("offset") or "").strip()
            cor, nota = (r.get("correcao") or "").strip(), (r.get("nota") or "").strip()
            if not scene or not off or (not cor and not nota):
                continue
            slot = by_scene.setdefault(scene, {"verbatim": [], "nota": []})
            if cor:
                slot["verbatim"].append((off, cor))       # correcao verbatim vence a nota
            else:
                slot["nota"].append((off, nota))
    return by_scene


def _apply_verbatim(root, scene, pairs) -> int:
    """Grava o texto do humano em translations + plan (parity-fit; SEM IA). Retorna nº de linhas."""
    import json
    sid = context_pack.scene_id_of(scene)
    tf, pf = paths.translations(root, scene, sid), paths.translation_plan(root, scene, sid)
    if not tf.is_file() or not pf.is_file():
        return 0
    tdata = json.loads(tf.read_text(encoding="utf-8"))
    pdata = json.loads(pf.read_text(encoding="utf-8"))
    srcmap = {ln.get("offset", ""): ln.get("text_source", "") for ln in pdata.get("lines", [])}
    n = 0
    for off, txt in pairs:
        fitted = model._parity_fit(srcmap.get(off, ""), model._norm_t(txt))
        tdata.setdefault("lines", {}).setdefault(off, {})["t"] = fitted
        for ln in pdata.get("lines", []):
            if ln.get("offset") == off:
                ln["base_translation"] = fitted
        n += 1
    tf.write_text(json.dumps(tdata, ensure_ascii=False, indent=2), encoding="utf-8")
    pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2), encoding="utf-8")
    model.invalidate_back_translation(root, scene, [o for o, _ in pairs])  # crivo antigo nao vale mais
    return n


def apply(root, csv_path, *, model_name=None, max_usd=None) -> dict:
    """Processa EXATAMENTE o devolvido: verbatim (0 IA) + nota (IA cirurgica por linha). `max_usd` so
    limita o caminho de IA (verbatim e sempre $0). Retorna {verbatim, ai, scenes, cost_usd,
    scenes_touched[], stopped_budget}."""
    root = Path(root)
    returned = read_returned(csv_path)
    m = model_name or model.MODEL_TRANSLATE
    verbatim_n, ai_n, cost = 0, 0, 0.0
    touched, stopped = [], False
    for scene in sorted(returned):
        slot = returned[scene]
        touched.append(scene)
        if slot["verbatim"]:
            verbatim_n += _apply_verbatim(root, scene, slot["verbatim"])   # sempre $0
        if slot["nota"]:
            if max_usd is not None and cost >= max_usd:
                stopped = True
                continue                                  # teto: pula o caminho PAGO (verbatim ja entrou)
            note = "\n\n## REVISAO DO HUMANO (reescreva SO estes offsets seguindo a instrucao)\n" + \
                   "\n".join(f"- {off}: {ins}" for off, ins in slot["nota"])
            res = model.retranslate_offsets(root, scene, [o for o, _ in slot["nota"]],
                                            model=m, budget_tolerance=1.0, quality_note=note)
            if res.get("usage"):
                cost += model.cost_of(m, res["usage"])
            ai_n += len(slot["nota"])
    return {"verbatim": verbatim_n, "ai": ai_n, "scenes": len(touched),
            "cost_usd": round(cost, 4), "scenes_touched": touched, "stopped_budget": stopped}


def main():
    ap = argparse.ArgumentParser(description="Revisao humana por capitulo (export CSV marcado / apply do devolvido).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("export", help="gera o CSV do capitulo inteiro, marcado p/ revisao")
    pe.add_argument("project"); pe.add_argument("chapter")
    pe.add_argument("--out", default=None)
    pa = sub.add_parser("apply", help="aplica o CSV devolvido (verbatim + notas)")
    pa.add_argument("project"); pa.add_argument("csv")
    pa.add_argument("--model", default=None)
    pa.add_argument("--max-usd", type=float, default=None, help="teto p/ o caminho de IA (notas); verbatim e $0")
    a = ap.parse_args()
    if a.cmd == "export":
        rows = export(a.project, a.chapter)
        out = a.out or str(paths.artifacts(Path(a.project)) / f"review_cap_{a.chapter}.csv")
        write_csv(rows, out)
        marked = sum(1 for r in rows if r["revisar"])
        print(f"[export] cap.{a.chapter}: {len(rows)} linha(s) -> {out}")
        print(f"         {marked} marcada(s) p/ avaliar (coluna 'revisar' preenchida); preencha "
              f"'correcao' (texto certo) ou 'nota' (instrucao) e devolva.")
        sys.exit(0)
    print(f"[apply] processando revisao devolvida: {a.csv}")
    r = apply(a.project, a.csv, model_name=a.model, max_usd=a.max_usd)
    print(f"[apply] verbatim={r['verbatim']} (0 IA) | nota+IA={r['ai']} (~${r['cost_usd']:.4f}) "
          f"| cenas tocadas={r['scenes']}")
    if r.get("stopped_budget"):
        print(f"[apply] teto de ${a.max_usd:.2f} atingido — algumas notas (IA) nao foram processadas; "
              "verbatim entrou tudo. Re-rode com mais orcamento p/ as notas restantes.")
    print("Proximos passos: verify_chapter de cada cap. tocado (round-trip/charset) + state_index --rebuild.")
    print(f"  cenas: {', '.join(r['scenes_touched'])}")
    sys.exit(0)


if __name__ == "__main__":
    main()
