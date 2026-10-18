"""perf_bench.py — benchmarks de performance com baseline e limite por operacao (Onda 3).

Mede tres operacoes que dominam o custo mecanico do pipeline, sobre dados 100% SINTETICOS (nenhum texto de
jogo): `append_line` (ledger/eventos sob trava), `build_pack` (montagem do context_pack a partir do DB, sem busca semantica: o custo de modelo de ML e outra
medida e variaria entre CI e PC) e
`state_index_tm` (reconstrucao da TM a partir de planos de cena).

Para o numero valer em maquinas diferentes (CI x PC), cada tempo e dividido pelo de uma carga de calibracao fixa
rodada na MESMA maquina; o baseline (`perf_baseline.json`) guarda essa razao. Uma operacao REGRIDE quando a razao
passa de `LIMITE` (2x) do baseline. Sem `--strict` o resultado so avisa (tendencia, nao bloqueia); com `--strict` o
codigo de saida e 1.

Uso: python perf_bench.py [--json] [--out arq.json] [--strict] [--update-baseline]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _p in (_HERE, _HERE.parent / "db"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import paths  # noqa: E402

BASELINE = _HERE / "perf_baseline.json"
LIMITE = 2.0          # regressao: razao atual > LIMITE x razao do baseline
REPETICOES = 5


def _calibracao() -> None:
    """Carga fixa de CPU + disco pequena: a unidade de medida das demais operacoes nesta maquina."""
    acc = 0
    for i in range(200_000):
        acc += i * i % 7
    with tempfile.TemporaryDirectory() as d:
        paths.atomic_write(Path(d) / "c.txt", "x" * 1000)


def _op_append_line(tmp: Path) -> None:
    p = tmp / "ledger.jsonl"
    for i in range(100):
        paths.append_line(p, f'{{"i": {i}}}\n')


def _op_state_index_tm(tmp: Path) -> None:
    import state_index
    for n in range(20):
        pf = paths.translation_plan(tmp, f"s{n}", f"s{n}")
        pf.parent.mkdir(parents=True, exist_ok=True)
        pf.write_text(json.dumps({"lines": [
            {"offset": f"{n}:{k}", "text_source": f"fonte {n} {k}", "base_translation": f"alvo {n} {k}"}
            for k in range(50)]}), encoding="utf-8")
    state_index.build_tm(paths.artifacts(tmp))


def _op_build_pack(tmp: Path) -> None:
    import context_pack
    from store import Store
    with Store(tmp / "p.db") as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", "S1", [{"offset": f"X:0:{k}", "source": f"Linha sintetica {k}.",
                                           "byte_budget": 60} for k in range(100)])
        db.upsert_glossary("p", "termo", "alvo")
        db.upsert_voice_card("p", "Ana", lines=["fala"])
        db.upsert_decision("p", "Regra", summary="resumo", tags=["termo"])
    (tmp / "project.json").write_text(json.dumps(
        {"title": "T", "media_type": "game", "db": {"path": "p.db", "project_id": "p", "semantic": False}, "connector": {}}),
        encoding="utf-8")
    context_pack.build_pack(tmp, "S1")


OPS: dict[str, Callable[[Path], None]] = {
    "append_line": _op_append_line,
    "build_pack": _op_build_pack,
    "state_index_tm": _op_state_index_tm,
}


def _tempo(fn: Callable[[], None]) -> float:
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def medir(repeticoes: int = REPETICOES) -> dict[str, float]:
    """Razao tempo(op) / tempo(calibracao), pela mediana de `repeticoes` rodadas (cada op em pasta nova)."""
    cal = statistics.median(_tempo(_calibracao) for _ in range(repeticoes))
    out = {}
    for nome, op in OPS.items():
        tempos = []
        for _ in range(repeticoes):
            with tempfile.TemporaryDirectory() as d:
                t0 = time.perf_counter()
                op(Path(d))
                tempos.append(time.perf_counter() - t0)
        out[nome] = round(statistics.median(tempos) / cal, 3)
    return out


def regressoes(atual: dict[str, float], base: dict[str, float], limite: float = LIMITE) -> list[str]:
    """Operacoes cuja razao passou de `limite` x o baseline; operacao sem baseline tambem conta (baseline
    desatualizado nao pode esconder regressao)."""
    out = []
    for nome, v in atual.items():
        b = base.get(nome)
        if b is None:
            out.append(f"{nome}: sem baseline (rode --update-baseline)")
        elif v > b * limite:
            out.append(f"{nome}: {v:.2f} > {limite:g}x o baseline {b:.2f}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="saida 1 se alguma operacao regredir")
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--out", help="grava o JSON (atual, baseline, regressoes) neste arquivo")
    a = ap.parse_args()
    atual = medir()
    if a.update_baseline:
        paths.atomic_write(BASELINE, json.dumps(atual, indent=2, sort_keys=True) + "\n")
        print(f"baseline gravado em {BASELINE}")
        return
    base = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.is_file() else {}
    regs = regressoes(atual, base)
    if a.out:
        paths.atomic_write(a.out, json.dumps({"atual": atual, "baseline": base, "regressoes": regs}, indent=2))
    if a.json:
        print(json.dumps({"atual": atual, "baseline": base, "regressoes": regs}, indent=2))
    else:
        for nome, v in atual.items():
            print(f"{nome:16s} {v:8.2f}  (baseline {base.get(nome, '-')})")
    for r in regs:
        print(f"::warning::performance: {r}")
    if regs and a.strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
