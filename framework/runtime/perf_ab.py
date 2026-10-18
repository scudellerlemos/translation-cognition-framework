"""perf_ab.py — guardrail A/B do ADR 0019: o mesmo benchmark em DOIS codigos, na mesma maquina e na mesma sessao.

"Antes" e um commit (worktree temporario, fora do repo); "depois" e a arvore de trabalho atual. As rodadas
alternam antes/depois (a deriva da maquina — termica, carga — pega os dois lados) e cada operacao fica com o MENOR
tempo de cada lado (o ruido so atrasa). O veredito e o de `perf_bench.guardrail`: piora acima de 10% em qualquer
operacao, ou um caminho (sessao/API) ganhando enquanto o outro perde, reprova (saida 1).

Uso: python perf_ab.py [--ref HEAD] [--rodadas 3]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import perf_bench  # noqa: E402


def agregar(medidas: list[dict[str, float]]) -> dict[str, float]:
    """Menor razao de cada operacao entre as rodadas (o ruido so atrasa, nunca adianta)."""
    return {n: min(m[n] for m in medidas if n in m) for n in {n for m in medidas for n in m}}


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def _medir(codigo: Path, saida: Path) -> dict[str, float]:
    subprocess.run([sys.executable, str(codigo / "framework" / "runtime" / "perf_bench.py"), "--salvar", str(saida)],
                   check=True, capture_output=True)
    return json.loads(saida.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default="HEAD", help="commit do 'antes' (padrao HEAD: o ultimo commit)")
    ap.add_argument("--rodadas", type=int, default=3)
    a = ap.parse_args()
    raiz = Path(_git("rev-parse", "--show-toplevel", cwd=_HERE))
    with tempfile.TemporaryDirectory() as d:
        antes_dir = Path(d) / "antes"
        _git("worktree", "add", "--detach", str(antes_dir), a.ref, cwd=raiz)
        try:
            antes, depois = [], []
            for i in range(a.rodadas):
                antes.append(_medir(antes_dir, Path(d) / f"a{i}.json"))
                depois.append(_medir(raiz, Path(d) / f"d{i}.json"))
                print(f"rodada {i + 1}/{a.rodadas} feita", flush=True)
        finally:
            _git("worktree", "remove", "--force", str(antes_dir), cwd=raiz)
    ma, md = agregar(antes), agregar(depois)
    print(f"{'operacao':20s} {'antes':>8s} {'depois':>8s} {'delta':>8s}")
    for n in perf_bench.OPS:
        if n in ma and n in md:
            print(f"{n:20s} {ma[n]:8.2f} {md[n]:8.2f} {md[n] / ma[n] - 1:+8.1%}")
    probs = perf_bench.guardrail(ma, md)
    for p in probs:
        print(f"GUARDRAIL: {p}")
    print("GUARDRAIL: ok" if not probs else "GUARDRAIL: REPROVADO")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
