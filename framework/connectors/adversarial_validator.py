#!/usr/bin/env python3
"""
adversarial_validator.py — 3 checagens de consistencia sobre os resultados por-arquivo do
coverage_gate.py. Roda DEPOIS do coverage_gate (recebe `per_file` ja computado -- nao reimporta o
candidato nem re-le os arquivos). Nao substitui o round-trip (connector_smoke.py/
test_roundtrip.py), que continua sendo o portao FINAL e inegociavel de aceitacao.

3 checagens concretas (nao vagas):
  1. Arquivo com ZERO strings entre arquivos populados -- candidato nao generaliza pro formato
     desse arquivo especifico (overfitting a outra amostra).
  2. Variancia alta entre arquivos (coeficiente de variacao > 1.5) -- cobertura inconsistente
     entre amostras do mesmo formato, sinal de bug dependente de layout especifico.
  3. Offsets sobrepostos dentro de 1 arquivo -- bug real de geracao/duplicacao no candidato.

Interface de escape (engine bloqueada, humano implementa extract/reinsert/validate manualmente):
reusa este modulo SEM NENHUMA adaptacao -- as checagens dependem so do shape de `per_file`
(produzido por coverage_gate.check()), nao de quem escreveu o candidato.

Uso: chamado por coverage_gate.py main() apos check(); standalone via main() so pra depuracao.
"""
from __future__ import annotations

import statistics

_VARIANCE_CV_MAX = 1.5


def check(per_file: list[dict]) -> dict:
    """Recebe a lista `per_file` que coverage_gate.check() ja computou (nao chama nada de novo).
    Retorna {passed, problems}."""
    problems: list[str] = []
    valid = [f for f in per_file if not f.get("error")]
    counts = [f["n_strings"] for f in valid]

    if counts and max(counts) > 10 and min(counts) == 0:
        zeroed = [f["path"] for f in valid if f["n_strings"] == 0]
        problems.append(
            f"arquivo(s) com ZERO strings extraidas entre arquivos populados (candidato nao "
            f"generaliza pro formato desse arquivo): {zeroed}"
        )

    if len(counts) >= 2 and statistics.mean(counts) > 0:
        cv = statistics.stdev(counts) / statistics.mean(counts)
        if cv > _VARIANCE_CV_MAX:
            problems.append(
                f"variancia alta entre arquivos (coeficiente de variacao {cv:.2f} > "
                f"{_VARIANCE_CV_MAX}) — cobertura inconsistente entre amostras"
            )

    for f in per_file:
        offs = sorted(f.get("offsets", []))
        for (o1, b1), (o2, _b2) in zip(offs, offs[1:], strict=False):   # janela deslizante, tamanhos diferentes de proposito
            if o1 + b1 > o2:
                problems.append(f"{f['path']}: offsets sobrepostos ({o1}+{b1} > {o2})")
                break

    return {"passed": not problems, "problems": problems}


def main():
    import json
    import sys
    from pathlib import Path
    if len(sys.argv) < 2:
        sys.exit("uso: python adversarial_validator.py <per_file.json> "
                 "(lista 'per_file' de uma saida de coverage_gate.check())")
    per_file = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    r = check(per_file)
    print("OK" if r["passed"] else "BLOQUEADO")
    for p in r["problems"]:
        print(f"  - {p}")
    sys.exit(0 if r["passed"] else 1)


if __name__ == "__main__":
    main()
