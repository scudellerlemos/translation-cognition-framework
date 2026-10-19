"""Lint de padroes ANTES da amostra de qualidade: a amostra e o ultimo passo, entao o que da pra achar por regra
(fala mais larga que a caixa, valor de parametro fora da tabela) se conserta antes, senao o humano gasta o sorteio com erro mecanico.

  python pattern_lint.py <projeto>     imprime a contagem por padrao; sai com 2 se houver padrao que bloqueia

`largura` e `parametro` (valor fora da tabela de opcodes) bloqueiam (mecanicos, consertaveis); `identico-fonte` so e contado (nome mantido e normal).
Largura pela tabela de opcodes do conector e pelo limite do box_width, so onde a fonte tem quebra do autor (linha unica = o motor quebra); pt-PT pela regex do quality_review.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifact_io  # noqa: E402
import box_width  # noqa: E402
import opcodes  # noqa: E402
import paths  # noqa: E402
import quality_review  # noqa: E402

BLOCKING = ("largura", "parametro")


def lint(root) -> dict:
    """Le as falas do plano (texto COM codigos: o limpo perderia as quebras) e mede pela tabela de opcodes."""
    root = Path(root)
    lim, tbl = box_width.configure(root), opcodes.table(root)
    counts: Counter = Counter()
    where: dict[str, list] = {f: [] for f in BLOCKING}
    for scene in artifact_io.scenes(root):
        for ln in artifact_io.plan_lines(root, scene):
            src, tgt = ln.get("text_source", ""), ln.get("base_translation", "")
            if not tgt:
                continue
            found = []
            # fonte em linha unica = texto corrido, o motor quebra: nao ha largura de caixa para estourar
            if len(box_width.widths(src, tbl)) > 1 and max(box_width.widths(tgt, tbl), default=0) > lim:
                found.append("largura")
            if quality_review._PTPT.search(tgt):
                found.append("pt-PT?")
            if opcodes.invalid_params(tgt, tbl):
                found.append("parametro")
            if src.strip() == tgt.strip():
                found.append("identico-fonte")
            for f in found:
                counts[f] += 1
                if f in where:
                    where[f].append((scene, ln.get("offset", "")))
    return {"counts": dict(counts), "blocking": {f: w for f, w in where.items() if w}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("project")
    a = ap.parse_args()
    r = lint(paths.require_project(a.project))
    print("padroes:", r["counts"] or "nenhum")
    for f, w in r["blocking"].items():
        print(f"  BLOQUEIA {f}: {len(w)} fala(s), ex.: {', '.join(f'{s}:{o}' for s, o in w[:3])}")
    sys.exit(2 if r["blocking"] else 0)


if __name__ == "__main__":
    main()
