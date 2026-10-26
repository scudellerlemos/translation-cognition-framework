#!/usr/bin/env python3
"""
quality_sample.py — MEDIDA DE QUALIDADE: taxa de erro por amostra aleatoria julgada pelo humano, taxa da
triagem e acerto do juiz. $0, sem IA: so sorteia, monta a planilha e faz a conta.

  export  sorteia N pares unicos (fonte+traducao) do jogo inteiro (ou so das --scenes, para medir uma onda) e junta
          os que o juiz da triagem apontou
          (risk_triage). A planilha nao diz de onde veio cada fala — o humano julga as cegas.
  score   le a planilha com a coluna `veredito` preenchida (ok / erro) e calcula:
            - taxa de erro da amostra aleatoria, com intervalo de 95% (a medida de qualidade);
            - taxa da triagem: quanto do que o juiz leu ele apontou (indicador por onda);
            - acerto do juiz: precisao (apontou e era erro) e alcance (erro da amostra que ele pegou).
          Grava um registro em qa_effectiveness.jsonl (historico, sem texto de fala).

Juiz de modelo (indicador, nao substitui o humano): `judge-export` grava `amostra_juiz.tsv` (id, fonte, traducao —
sem cena, offset nem modelo) + prompt; o juiz devolve `veredito_juiz.tsv` (id<TAB>ok|erro<TAB>motivo curto);
`judge-apply` copia os vereditos para a planilha devolvida e o `score` grava o juiz como `llm-judge:<modelo>`.
`judge-compare` mede a concordancia do juiz com uma planilha ja julgada por humano (calibracao).

Uso:
  python quality_sample.py export <projeto> [--n 200] [--seed q1] [--scenes CENA ...]
  python quality_sample.py score  <projeto> --reviewer NOME [planilha.csv]
  python quality_sample.py judge-export  <projeto>
  python quality_sample.py judge-apply   <projeto> [veredito_juiz.tsv]
  python quality_sample.py judge-compare <projeto> [veredito_juiz.tsv]
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import paths  # noqa: E402
import pattern_lint  # noqa: E402
import risk_triage  # noqa: E402

NAME = "amostra_qualidade"
JUDGE_IN, JUDGE_OUT, JUDGE_PROMPT = "amostra_juiz.tsv", "veredito_juiz.tsv", "amostra_juiz_prompt.md"
JUDGE_TEXT = """# Juiz de qualidade de traducao (EN -> PT-BR)

Cada linha de `amostra_juiz.tsv` e: id, fala original (EN), traducao (PT-BR). Voce nao sabe quem traduziu.
Julgue cada linha sozinha: `erro` so se houver defeito claro (sentido trocado ou perdido, palavra de conteudo
omitida, termo mal traduzido, concordancia ou ortografia errada, tom claramente fora). Estilo diferente do seu,
mas correto e natural, e `ok`. Tokens como [0A] e quebras literais nao sao defeito. Na duvida, `ok`.
Grave, com Write, `veredito_juiz.tsv` na mesma pasta: uma linha por id, `id<TAB>ok` ou `id<TAB>erro<TAB>motivo curto`.
Nao edite outro arquivo e nao leia outra pasta do projeto.
"""
COLS = ["id", "scene", "offset", "source_en", "target_pt", "veredito", "nota"]


def _h(seed: str, pid: str) -> str:
    return hashlib.sha1(f"{seed}|{pid}".encode(), usedforsecurity=False).hexdigest()


def export(root, n: int = 200, seed: str = "q1", scenes=None) -> dict:
    root = Path(root)
    bl = pattern_lint.lint(root)["blocking"]
    if bl:   # a amostra e o ultimo passo: padrao mecanico se conserta antes (rode pattern_lint.py)
        raise SystemExit("ERRO: lint de padroes reprova antes da amostra: "
                         + "; ".join(f"{f} em {len(w)} fala(s)" for f, w in bl.items()))
    allp = risk_triage.pairs(root, everything=True)
    if scenes:   # populacao so das cenas pedidas (ex.: a onda traduzida por outro modelo)
        keep = set(scenes)
        allp = {pid: {**v, "where": [w for w in v["where"] if w[0] in keep]} for pid, v in allp.items()}
        allp = {pid: v for pid, v in allp.items() if v["where"]}
        if not allp:
            raise SystemExit(f"ERRO: nenhuma fala traduzida nas cenas {sorted(keep)}")
    seen, flagged = risk_triage.judged(root)
    sample = sorted(allp, key=lambda pid: _h(seed, pid))[:n]          # sorteio estavel: mesma seed, mesma amostra
    rows = sorted(set(sample) | (flagged & set(allp)), key=lambda pid: _h(seed + "|ordem", pid))   # embaralhado
    out = paths.qa_outbox(root)
    out.mkdir(parents=True, exist_ok=True)
    paths.atomic_write_csv(out / f"{NAME}.csv", COLS,
                           ([pid, *allp[pid]["where"][0], allp[pid]["source"], allp[pid]["target"], "", ""] for pid in rows),
                           encoding="utf-8-sig")
    paths.atomic_write(out / f"{NAME}.json", json.dumps({
        "seed": seed, "population": len(allp), "sample": sample, "flagged": sorted(flagged), "seen": len(seen),
        "weight": {pid: len(allp[pid]["where"]) for pid in rows}}))
    return {"rows": len(rows), "sample": len(sample), "flagged": len(flagged), "population": len(allp),
            "path": str(out / f"{NAME}.csv")}


def _rows(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(raw.splitlines(), delimiter=";" if raw.count(";") > raw.count(",") else ","))


def judge_export(root) -> dict:
    """Entrada do juiz: so id, fonte e traducao (a planilha ja esta embaralhada); sem cena, offset nem modelo."""
    root = Path(root)
    sheet = paths.qa_outbox(root) / f"{NAME}.csv"
    if not sheet.is_file():
        raise SystemExit(f"ERRO: sem {sheet}; rode `export` antes")
    rows = _rows(sheet)
    clean = lambda s: " ".join(s.replace("\t", " ").split())   # noqa: E731  (uma linha por id no TSV)
    out = paths.qa_outbox(root)
    paths.atomic_write(out / JUDGE_IN, "".join(
        f"{r['id']}\t{clean(r['source_en'])}\t{clean(r['target_pt'])}\n" for r in rows))
    paths.atomic_write(out / JUDGE_PROMPT, JUDGE_TEXT)
    return {"rows": len(rows), "dir": str(out)}


def _read_verdicts(path: Path) -> dict[str, str]:
    v = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        parts = ln.split("\t")
        if len(parts) >= 2 and parts[1].strip().lower() in ("ok", "erro"):
            v[parts[0].strip()] = parts[1].strip().lower()
    return v


def judge_apply(root, verdicts=None) -> dict:
    """Copia os vereditos do juiz para a planilha devolvida (o `score` le dali). Id sem veredito fica em branco."""
    root = Path(root)
    src = Path(verdicts) if verdicts else paths.qa_outbox(root) / JUDGE_OUT
    v = _read_verdicts(src)
    rows = _rows(paths.qa_outbox(root) / f"{NAME}.csv")
    for r in rows:
        r["veredito"] = v.get(r["id"], "")
    inbox = paths.qa_inbox(root)
    inbox.mkdir(parents=True, exist_ok=True)
    paths.atomic_write_csv(inbox / f"{NAME}.csv", COLS, ([r[c] for c in COLS] for r in rows), encoding="utf-8-sig")
    return {"judged": sum(1 for r in rows if r["veredito"]), "rows": len(rows), "path": str(inbox / f"{NAME}.csv")}


def judge_compare(root, verdicts=None) -> dict:
    """Concordancia do juiz com a planilha ja julgada por humano (a que esta em para_revisar ou devolvido)."""
    root = Path(root)
    src = Path(verdicts) if verdicts else paths.qa_outbox(root) / JUDGE_OUT
    v = _read_verdicts(src)
    human_sheet = paths.qa_inbox(root) / f"{NAME}.csv"
    human = {r["id"]: (r.get("veredito") or "").strip().lower().startswith("e")
             for r in _rows(human_sheet if human_sheet.is_file() else paths.qa_outbox(root) / f"{NAME}.csv")
             if (r.get("veredito") or "").strip()}
    both = [i for i in human if i in v]
    jerr = {i: v[i] == "erro" for i in both}
    h_err = [i for i in both if human[i]]
    j_err = [i for i in both if jerr[i]]
    return {"compared": len(both), "human_errors": len(h_err), "judge_errors": len(j_err),
            "both_error": sum(1 for i in h_err if jerr[i]),
            "judge_only": sum(1 for i in j_err if not human[i]),
            "agreement": round(sum(human[i] == jerr[i] for i in both) / len(both), 4) if both else None}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de 95% de uma proporcao (Wilson): honesto com amostra pequena e taxa perto de zero."""
    if not n:
        return 0.0, 1.0
    p, d = k / n, 1 + z * z / n
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    mid = (p + z * z / (2 * n)) / d
    return max(0.0, mid - half), min(1.0, mid + half)


def _sheet(root: Path, path) -> Path:
    if path:
        return Path(path)
    back = paths.qa_inbox(root) / f"{NAME}.csv"
    return back if back.is_file() else paths.qa_outbox(root) / f"{NAME}.csv"


def score(root, reviewer: str, path=None) -> dict:
    root = Path(root)
    meta = json.loads((paths.qa_outbox(root) / f"{NAME}.json").read_text(encoding="utf-8"))
    sheet = _sheet(root, path)
    raw = sheet.read_text(encoding="utf-8-sig")
    rows = csv.DictReader(raw.splitlines(), delimiter=";" if raw.count(";") > raw.count(",") else ",")
    verdict = {}
    for r in rows:
        v = (r.get("veredito") or "").strip().lower()
        if v:
            verdict[r["id"]] = v.startswith("e")              # erro / errado; qualquer outra coisa = ok
    sample, flagged, weight = set(meta["sample"]), set(meta["flagged"]), meta["weight"]
    s = [p for p in sample if p in verdict]
    s_err = [p for p in s if verdict[p]]
    f = [p for p in flagged if p in verdict]
    lo, hi = wilson(len(s_err), len(s))
    w_all, w_err = sum(weight[p] for p in s), sum(weight[p] for p in s_err)
    rec = {
        "t": round(time.time(), 3), "source": "quality_sample", "reviewer": reviewer, "seed": meta["seed"],
        "population": meta["population"], "judged": len(s), "errors": len(s_err),
        "error_rate": round(len(s_err) / len(s), 4) if s else None, "ci95": [round(lo, 4), round(hi, 4)],
        "error_rate_weighted": round(w_err / w_all, 4) if w_all else None,      # pesa fala repetida pelo nº de copias
        "triage_rate": round(len(flagged) / meta["seen"], 4) if meta["seen"] else None,
        "judge_precision": round(sum(verdict[p] for p in f) / len(f), 3) if f else None,
        "judge_flagged_judged": len(f),
        # alcance: so vale se o juiz ja leu o jogo todo — erro em lote ainda sem veredito conta como nao pego
        "judge_recall": round(sum(p in flagged for p in s_err) / len(s_err), 3) if s_err and meta["seen"] else None,
        "unjudged": len(sample - set(verdict)),
    }
    paths.append_line(paths.qa_effectiveness(root), json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main():
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    ap = argparse.ArgumentParser(description="Medida de qualidade por amostra julgada pelo humano.")
    ap.add_argument("cmd", choices=["export", "score", "judge-export", "judge-apply", "judge-compare"])
    ap.add_argument("project")
    ap.add_argument("sheet", nargs="?", default=None)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", default="q1")
    ap.add_argument("--reviewer", default=None)
    ap.add_argument("--scenes", nargs="+", default=None, help="export: sorteia so destas cenas")
    a = ap.parse_args()
    if a.cmd == "export":
        r = export(a.project, a.n, a.seed, a.scenes)
        print(f"amostra: {r['rows']} fala(s) para julgar ({r['sample']} sorteadas de {r['population']} pares unicos"
              f" + {r['flagged']} apontadas pelo juiz, misturadas) -> {r['path']}")
        print("  preencha a coluna `veredito` com ok ou erro; depois: quality_sample.py score <projeto> --reviewer NOME")
        return
    if a.cmd == "judge-export":
        r = judge_export(a.project)
        print(f"juiz: {r['rows']} fala(s) em {r['dir']} ({JUDGE_IN} + {JUDGE_PROMPT}); o juiz grava {JUDGE_OUT}")
        return
    if a.cmd == "judge-apply":
        r = judge_apply(a.project, a.sheet)
        print(f"juiz: {r['judged']}/{r['rows']} veredito(s) -> {r['path']}; depois: score --reviewer llm-judge:<modelo>")
        return
    if a.cmd == "judge-compare":
        r = judge_compare(a.project, a.sheet)
        print(f"concordancia juiz x humano: {r['compared']} fala(s) | erro humano {r['human_errors']}, erro do juiz "
              f"{r['judge_errors']} | pegou {r['both_error']} dos erros humanos | so o juiz apontou {r['judge_only']} "
              f"| concordancia {r['agreement']}")
        return
    if not a.reviewer:
        ap.error("--reviewer NOME e obrigatorio: o veredito e de um humano")
    r = score(a.project, a.reviewer, a.sheet)

    def pct(x):
        return "n/d" if x is None else f"{100 * x:.1f}%"
    print(f"taxa de erro : {pct(r['error_rate'])} ({r['errors']}/{r['judged']}; 95%: {pct(r['ci95'][0])} a "
          f"{pct(r['ci95'][1])}) | pesada por repeticao: {pct(r['error_rate_weighted'])}")
    print(f"triagem      : juiz apontou {pct(r['triage_rate'])} do que leu")
    print(f"juiz         : precisao {pct(r['judge_precision'])} ({r['judge_flagged_judged']} apontada(s) julgada(s))"
          f" | alcance {pct(r['judge_recall'])}")
    if r["unjudged"]:
        print(f"  AVISO: {r['unjudged']} fala(s) da amostra sem veredito — a taxa vale so para as julgadas.")


if __name__ == "__main__":
    main()
