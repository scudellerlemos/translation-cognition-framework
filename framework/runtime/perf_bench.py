"""perf_bench.py — benchmarks de performance com baseline e limite por operacao (Onda 3 e 4).

Mede as operacoes que dominam o custo mecanico do pipeline, sobre dados 100% SINTETICOS (nenhum texto de
jogo): `append_line` (ledger/eventos sob trava), `build_pack` (montagem do context_pack a partir do DB, sem busca
semantica: o custo de modelo de ML e outra medida e variaria entre CI e PC), `state_index_tm` (reconstrucao da TM a
partir de planos de cena) e, para o ADR 0019, os DOIS caminhos de traducao: `session_translate` (caminho de sessao)
e `api_overhead` (so o overhead mecanico do caminho de API, com cliente falso), mais `render_prompt` (compartilhado,
com pacote completo) e o tempo de import de `model` e `context_pack`.

Para o numero valer em maquinas diferentes (CI x PC), cada tempo e dividido pelo de uma carga de calibracao fixa
rodada na MESMA maquina; o baseline (`perf_baseline.json`) guarda essa razao. Uma operacao REGRIDE quando a razao
passa de `LIMITE` (2x) do baseline. Sem `--strict` o resultado so avisa (tendencia, nao bloqueia); com `--strict` o
codigo de saida e 1.

Guardrail do ADR 0019 (`--salvar` e `--antes`, ou `perf_ab.py`): A/B na mesma maquina, limite de 10% por operacao e
sem desequilibrio entre sessao e API.

Uso: python perf_bench.py [--json] [--out arq.json] [--strict] [--update-baseline] [--salvar arq] [--antes arq]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import statistics
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

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
        paths.atomic_write(pf, json.dumps({"lines": [
            {"offset": f"{n}:{k}", "text_source": f"fonte {n} {k}", "base_translation": f"alvo {n} {k}"}
            for k in range(50)]}))
    state_index.build_tm(paths.artifacts(tmp))


def _projeto(tmp: Path, n_linhas: int = 100) -> None:
    """Projeto sintetico de uma cena `S1` (DB-only, sem busca semantica)."""
    from store import Store
    with Store(tmp / "p.db") as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", "S1", [{"offset": f"X:0:{k}", "source": f"Linha sintetica {k}.",
                                           "byte_budget": 60} for k in range(n_linhas)])
        db.upsert_glossary("p", "termo", "alvo")
        db.upsert_voice_card("p", "Ana", lines=["fala"])
        db.upsert_decision("p", "Regra", summary="resumo", tags=["termo"])
    paths.atomic_write(tmp / "project.json", json.dumps(
        {"title": "T", "media_type": "game", "db": {"path": "p.db", "project_id": "p", "semantic": False}, "connector": {}}))


def _op_build_pack(tmp: Path) -> None:
    import context_pack
    _projeto(tmp)
    context_pack.build_pack(tmp, "S1")


def _pack_completo(n: int = 500) -> dict:
    """Pacote com TODAS as secoes opcionais preenchidas: o render_prompt passa por todos os ramos."""
    return {
        "scene": "S1", "scene_id": "S1", "n_lines": n,
        "project_constraints": {"newline_token": "[01]", "formatting_tokens": ["<C1>"], "formatting_token_patterns": [],
                                "system_line_convention": "x", "length_constraints": {"max": 60},
                                "target_charset_supported": False, "charset_note": "ascii",
                                "budget_reserves_terminator": True},
        "glossary_subset": [{"term": f"t{i}", "category": "c", "target_translation": "a", "handling_rule": "r",
                             "spoiler_level": 0} for i in range(40)],
        "voice_cards": {f"V{i}": {"criticality": "high", "aliases": ["a"], "lines": ["l1", "l2"]} for i in range(8)},
        "decisions": [{"title": f"d{i}", "summary": "s", "universal": i % 2 == 0} for i in range(20)],
        "decisions_semantic": [{"title": f"s{i}", "summary": "s", "score": 0.5} for i in range(10)],
        "spoiler_guards": [{"entity": f"e{i}", "spoiler_level": 1, "guard": "g"} for i in range(5)],
        "kb": [{"section": f"k{i}", "content": "texto " * 30} for i in range(5)],
        "kb_semantic": [{"section": f"q{i}", "content": "texto " * 30, "score": 0.4} for i in range(5)],
        "tm_exact": [{"source": f"s{i}", "target": f"t{i}", "speaker": "A", "from_scene": "S0"} for i in range(30)],
        "tm_voice": [{"speaker": "A", "source": f"s{i}", "target": f"t{i}"} for i in range(30)],
        "tm_semantic": [{"score": 0.5, "source": f"s{i}", "target": f"t{i}"} for i in range(20)],
        "tm_series": [{"source": f"s{i}", "target": f"t{i}", "from_game": "G"} for i in range(10)],
        "lines": [{"offset": f"X:0:{k}", "byte_budget": 60, "source": f"Linha | sintetica {k}."} for k in range(n)],
    }


def _op_render_prompt(tmp: Path) -> None:
    import context_pack
    pack = _pack_completo()
    for _ in range(50):          # a funcao e rapida: repete p/ a medida passar do ruido do relogio
        context_pack.render_prompt(pack, "carta " * 200)


def _op_session_translate(tmp: Path) -> None:
    """Caminho de SESSAO: gera pacote+prompt e devolve o estado (AGUARDANDO). Sem rede."""
    import model
    _projeto(tmp)
    model.translate(tmp, "S1", backend="in-session")


@contextlib.contextmanager
def _api_falsa(model: Any):
    """Troca o cliente da API por um que responde na hora: so o overhead MECANICO do caminho de API entra na medida."""
    nomes = ("_client", "_carta_text", "_stream_final", "_text_of", "_usage_of", "log_api_call")
    antes = {n: getattr(model, n) for n in nomes}
    zero = {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    resp: dict = {}
    model._client = lambda: object()
    model._carta_text = lambda: "CARTA"
    model._stream_final = lambda client, **kw: resp
    model._text_of = lambda msg: json.dumps(msg)
    model._usage_of = lambda msg: dict(zero)
    model.log_api_call = lambda *a, **k: None
    try:
        yield resp
    finally:
        for n, v in antes.items():
            setattr(model, n, v)


def _op_api_overhead(tmp: Path) -> None:
    import context_pack
    import model
    _projeto(tmp)
    pack = context_pack.build_pack(tmp, "S1")
    paths.scene_dir(tmp, "S1").mkdir(parents=True, exist_ok=True)
    with _api_falsa(model) as resp:
        resp["lines"] = [{"offset": r["offset"], "speaker": "X", "tone_register": "n", "intent": "i",
                          "risk_level": "low", "risk_notes": "", "t": "ok"} for r in pack["lines"]]
        model._api_translate(tmp, "S1", pack, model.MODEL_TRANSLATE)


def _import_us(modulo: str) -> float:
    """Tempo (us) de importar `modulo` num processo novo, pelo `-X importtime` (cumulativo do proprio modulo)."""
    r = subprocess.run([sys.executable, "-X", "importtime", "-c", f"import {modulo}"], capture_output=True,
                       text=True, cwd=_HERE, check=True)
    linha = [ln for ln in r.stderr.splitlines() if ln.rstrip().endswith(f"| {modulo}")][-1]
    return float(linha.split("|")[1])


def _op_import_model(tmp: Path) -> None:
    _import_us("model")


def _op_import_context_pack(tmp: Path) -> None:
    _import_us("context_pack")


OPS: dict[str, Callable[[Path], None]] = {
    "append_line": _op_append_line,
    "build_pack": _op_build_pack,
    "state_index_tm": _op_state_index_tm,
    "render_prompt": _op_render_prompt,
    "session_translate": _op_session_translate,
    "api_overhead": _op_api_overhead,
    "import_model": _op_import_model,
    "import_context_pack": _op_import_context_pack,
}

# ADR 0019: a divisao de model/context_pack nao pode favorecer um caminho a custa do outro.
GRUPOS: dict[str, tuple[str, ...]] = {
    "sessao": ("session_translate",),
    "api": ("api_overhead",),
    "compartilhado": ("build_pack", "render_prompt", "import_model", "import_context_pack"),
}


def _tempo(fn: Callable[[], None]) -> float:
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def medir(repeticoes: int = REPETICOES, ops: list[str] | None = None) -> dict[str, float]:
    """Razao tempo(op) / tempo(calibracao), pela mediana de `repeticoes` rodadas (cada op em pasta nova).
    `ops` restringe a medida a algumas operacoes (o A/B intercalado mede uma por vez)."""
    cal = statistics.median(_tempo(_calibracao) for _ in range(max(repeticoes, 3)))
    out = {}
    for nome, op in OPS.items():
        if ops is not None and nome not in ops:
            continue
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


def guardrail(antes: dict[str, float], depois: dict[str, float], limite: float = 1.10,
              ruido: float = 0.03) -> list[str]:
    """Guardrail do ADR 0019 (A/B na mesma maquina). Problemas: (1) operacao que piorou mais de `limite`;
    (2) desequilibrio: um caminho (sessao/api) melhorou alem do `ruido` e o outro piorou alem dele."""
    out = [f"{n}: {depois[n]:.2f} > {limite:g}x o de antes ({antes[n]:.2f})"
           for n in depois if n in antes and depois[n] > antes[n] * limite]
    delta: dict[str, float] = {}
    for g in ("sessao", "api"):
        ds = [depois[n] / antes[n] - 1 for n in GRUPOS[g] if n in antes and n in depois and antes[n] > 0]
        if ds:
            delta[g] = statistics.mean(ds)
    if len(delta) == 2 and ((delta["sessao"] > ruido and delta["api"] < -ruido)
                            or (delta["api"] > ruido and delta["sessao"] < -ruido)):
        out.append(f"desequilibrio: sessao {delta['sessao']:+.1%} x api {delta['api']:+.1%} (um ganha, o outro perde)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="saida 1 se alguma operacao regredir")
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--salvar", help="grava as razoes medidas (serve de 'antes' no --antes)")
    ap.add_argument("--antes", help="guardrail do ADR 0019: compara a medida atual com este JSON (limite 10%%, sem desequilibrio)")
    ap.add_argument("--op", action="append", help="mede so esta operacao (repetivel)")
    ap.add_argument("--repeticoes", type=int, default=REPETICOES)
    ap.add_argument("--out", help="grava o JSON (atual, baseline, regressoes) neste arquivo")
    a = ap.parse_args()
    atual = medir(a.repeticoes, a.op)
    if a.salvar:
        paths.atomic_write(a.salvar, json.dumps(atual, indent=2, sort_keys=True) + "\n")
        print(f"medida gravada em {a.salvar}")
        return
    if a.antes:
        probs = guardrail(json.loads(Path(a.antes).read_text(encoding="utf-8")), atual)
        for nome, v in atual.items():
            print(f"{nome:20s} {v:8.2f}")
        for pr in probs:
            print(f"GUARDRAIL: {pr}")
        sys.exit(1 if probs else 0)
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
