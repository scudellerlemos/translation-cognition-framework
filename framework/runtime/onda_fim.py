#!/usr/bin/env python3
"""
onda_fim.py — a linha final de uma onda (usado pelo rodar_ondas.ps1).

O contrato da onda e terminar com uma linha `ONDA_OK: <n> cenas, <x> falas`, `PARADA: <motivo>` ou `FIM`. O modelo
as vezes escreve algo depois dela (um "pronto", um resumo, uma linha de erro do shell); olhar so a ultima linha do
log transformava onda boa em "fora do contrato". Aqui vale a ULTIMA linha que tem a forma do contrato, em qualquer
posicao. Linha entre aspas ou citada (`> ONDA_OK`, `` `ONDA_OK` ``) nao conta: so a que COMECA com a palavra.

Uso:  python onda_fim.py [arquivo]      (sem arquivo le o stdin)
Imprime a linha do contrato e sai com 0; sem linha de contrato imprime nada e sai com 1.
"""
from __future__ import annotations

import re
import sys

_CONTRATO = re.compile(r"^\s*(ONDA_OK\b.*|PARADA\b.*|FIM\s*)$")


def linha_final(texto: str) -> str | None:
    achou = None
    for ln in texto.splitlines():
        if _CONTRATO.match(ln):
            achou = ln.strip()
    return achou


def main() -> None:
    texto = open(sys.argv[1], encoding="utf-8", errors="replace").read() if len(sys.argv) > 1 else sys.stdin.read()
    ln = linha_final(texto)
    if ln is None:
        sys.exit(1)
    print(ln)


if __name__ == "__main__":
    main()
