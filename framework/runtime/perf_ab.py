"""perf_ab.py — guardrail A/B do ADR 0019: o mesmo benchmark em DOIS codigos, na mesma maquina e na mesma sessao.

"Antes" e um commit (`git archive`); "depois" e a arvore de trabalho atual (copia, com o que ainda nao foi commitado).
Os DOIS sao extraidos para pastas de Temp: rodar um dentro do repo e o outro fora media o local (antivirus, disco), nao o
codigo (A/A com codigo identico deu +10% a +26% antes disso). Cada
operacao e medida alternando antes/depois em sequencia (a deriva da maquina pega os dois lados no mesmo segundo) e
fica com o MENOR tempo de cada lado (o ruido so atrasa). O veredito e o de `perf_bench.guardrail`: piora acima de 10% em qualquer
operacao, ou um caminho (sessao/API) ganhando enquanto o outro perde, reprova (saida 1).

Uso: python perf_ab.py [--ref HEAD] [--rodadas 7]
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import perf_bench  # noqa: E402


def agregar(medidas: list[dict[str, float]]) -> dict[str, float]:
    """Menor razao de cada operacao entre as rodadas (o ruido so atrasa, nunca adianta)."""
    return {n: min(m[n] for m in medidas if n in m) for n in {n for m in medidas for n in m}}


def _git(*args: str, cwd: Path) -> bytes:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True).stdout


def _extrair_commit(raiz: Path, ref: str, destino: Path) -> None:
    tarfile.open(fileobj=io.BytesIO(_git("archive", "--format=tar", ref, "framework", cwd=raiz))).extractall(
        destino, filter="data")


def _copiar_arvore(raiz: Path, destino: Path) -> None:
    shutil.copytree(raiz / "framework", destino / "framework", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def _medir(codigo: Path, saida: Path, op: str) -> float:
    """Razao de UMA operacao (1 repeticao) no codigo de `codigo`, num processo novo."""
    subprocess.run([sys.executable, str(codigo / "framework" / "runtime" / "perf_bench.py"), "--op", op,
                    "--repeticoes", "1", "--salvar", str(saida)], check=True, capture_output=True)
    return float(json.loads(saida.read_text(encoding="utf-8"))[op])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default="HEAD", help="commit do 'antes' (padrao HEAD: o ultimo commit)")
    ap.add_argument("--rodadas", type=int, default=7)
    a = ap.parse_args()
    raiz = Path(_git("rev-parse", "--show-toplevel", cwd=_HERE).decode().strip())
    with tempfile.TemporaryDirectory() as d:
        lados = {"antes": Path(d) / "antes", "depois": Path(d) / "depois"}
        _extrair_commit(raiz, a.ref, lados["antes"])
        _copiar_arvore(raiz, lados["depois"])
        res: dict[str, dict[str, list[float]]] = {"antes": {}, "depois": {}}
        for r in range(a.rodadas):
            for i, op in enumerate(perf_bench.OPS):
                # intercalado POR OPERACAO (a deriva da maquina pega os dois lados no mesmo segundo) e com a
                # ordem alternando: nem antes nem depois leva sempre o primeiro ou o segundo lugar
                ordem = ("antes", "depois") if (r + i) % 2 == 0 else ("depois", "antes")
                for lado in ordem:
                    res[lado].setdefault(op, []).append(_medir(lados[lado], Path(d) / "m.json", op))
            print(f"rodada {r + 1}/{a.rodadas} feita", flush=True)
    ma = agregar([{n: v[k] for n, v in res["antes"].items()} for k in range(a.rodadas)])
    md = agregar([{n: v[k] for n, v in res["depois"].items()} for k in range(a.rodadas)])
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
