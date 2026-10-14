#!/usr/bin/env python3
"""
residual_text.py — texto legivel que ficou no binario de origem FORA do que o extract.py extraiu.

Contexto (BoF4, issue do backlog): o conector cortava cada string no primeiro 0x00, mas 0x00 tambem era
parametro de control code -- ~25% das falas saiam truncadas. O round-trip sem traducao passava byte
a byte (extract e reinsert cortavam no mesmo lugar), entao o connector_gate ficou verde e o defeito
so apareceu in-game. Round-trip identico prova que nada foi CORROMPIDO, nao que tudo foi EXTRAIDO.

Check: varre cada arquivo de origem atras de trechos ASCII com cara de frase e confere se cada um
esta contido em alguma string extraida daquele arquivo. Fracao de trechos sem dono acima do teto =
extracao incompleta. Deterministico, sem rede, nao depende do formato do container.

Uso: python residual_text.py <dialogs.csv> <source_dir> [--ceiling 0.05]
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

_CEILING = 0.05     # BoF4: 0.2% com o conector certo, 25% com o corte no primeiro 0x00
_RUN_RE = re.compile(rb"[ -~]{12,}")
_TOKEN_RE = re.compile(r"\[[0-9A-Fa-f]{2}\]")   # ponytail: so token [XX]; ler formatting_token_patterns se outro formato precisar


def _wordy(s: str) -> bool:
    """Frase, nao lixo binario que por acaso e imprimivel: tem espacos e e quase toda letra."""
    return s.count(" ") >= 2 and sum(c.isalpha() for c in s) >= 0.6 * len(s)


def file_residual(data: bytes, texts: list[str]) -> tuple[int, list[str]]:
    """(n. de trechos com cara de frase no binario, os que nao estao em nenhuma string extraida)."""
    hay = "\n".join(_TOKEN_RE.sub("\n", t) for t in texts)
    runs = [r for r in (m.group().decode("ascii") for m in _RUN_RE.finditer(data)) if _wordy(r)]
    return len(runs), [r for r in runs if r.strip() not in hay]


def check(dialogs_csv, source_dir, *, ceiling: float = _CEILING, text_column: str = "text_en") -> dict:
    """Retorna {passed, ratio, n_runs, n_residual, per_file: [(arquivo, residuais, trechos)], examples}.
    Texto que nao e ASCII no binario (tabela de caracteres propria) nao gera trecho: n_runs=0, passa."""
    by_file: dict[str, list[str]] = defaultdict(list)
    with open(dialogs_csv, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            by_file[Path(row["file"]).name].append(row[text_column])
    n_runs = n_res = 0
    per_file, examples = [], []
    for name, texts in sorted(by_file.items()):
        path = Path(source_dir) / name
        if not path.is_file():
            continue
        n, miss = file_residual(path.read_bytes(), texts)
        n_runs += n
        n_res += len(miss)
        if miss:
            per_file.append((name, len(miss), n))
            examples += miss[:1]
    ratio = n_res / n_runs if n_runs else 0.0
    per_file.sort(key=lambda x: x[1] / x[2], reverse=True)
    return {"passed": ratio <= ceiling, "ratio": round(ratio, 4), "n_runs": n_runs, "n_residual": n_res,
            "per_file": per_file, "examples": examples[:5]}


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Texto legivel no binario que o extract nao extraiu.")
    ap.add_argument("dialogs_csv")
    ap.add_argument("source_dir")
    ap.add_argument("--ceiling", type=float, default=_CEILING)
    a = ap.parse_args()
    r = check(a.dialogs_csv, a.source_dir, ceiling=a.ceiling)
    print(f"residual_text: {'OK' if r['passed'] else 'BLOQUEADO'} — {r['n_residual']}/{r['n_runs']} "
          f"trecho(s) fora da extracao ({r['ratio']:.1%}, teto {a.ceiling:.0%})")
    for name, miss, n in r["per_file"][:10]:
        print(f"    {name}: {miss}/{n}")
    for e in r["examples"]:
        print(f"    ex.: {e!r}")
    sys.exit(0 if r["passed"] else 1)


if __name__ == "__main__":
    main()
