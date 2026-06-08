#!/usr/bin/env python3
"""
charset_check.py — Gate de charset do conector (Passo 00).

Verifica se os glifos do idioma-alvo (pt-BR) são suportados pela fonte do jogo.
Método empírico robusto: se um code point JÁ aparece no texto que o jogo renderiza,
então a fonte tem o glifo. Para os que não aparecem no texto, reporta como "a confirmar".

Code points definidos por valor (sem acentos no código → imune a problemas de encoding).
"""
import os
import sys

# O caminho do .sdat é ENTREGUE pelo usuário no runtime (governança: nunca hardcoded).
# Uso: python charset_check.py <caminho-do-ScriptEvent.sdat>
# A localização de origem (pasta da Steam, Data/ENG/ScriptEvent.sdat) é só ONDE achar.

# acentos pt-BR por code point Unicode (Latin-1 Supplement)
PTBR = {
    "a_agudo": 0xE1, "e_agudo": 0xE9, "i_agudo": 0xED, "o_agudo": 0xF3, "u_agudo": 0xFA,
    "a_circ": 0xE2, "e_circ": 0xEA, "o_circ": 0xF4, "a_grave": 0xE0,
    "a_til": 0xE3, "o_til": 0xF5, "c_ced": 0xE7,
    "A_agudo": 0xC1, "E_agudo": 0xC9, "I_agudo": 0xCD, "O_agudo": 0xD3, "U_agudo": 0xDA,
    "A_circ": 0xC2, "E_circ": 0xCA, "O_circ": 0xD4, "A_grave": 0xC0,
    "A_til": 0xC3, "O_til": 0xD5, "C_ced": 0xC7,
}

import re

def textual_count(blob, ch):
    """Conta ocorrencias do acento DENTRO de palavra real (ladeado por letra ASCII),
    filtrando falsos positivos de bytes binarios decodificados como UTF-8."""
    pat = re.compile(r"(?:(?<=[A-Za-z])" + re.escape(ch) + r"|" + re.escape(ch) + r"(?=[A-Za-z]))")
    return len(pat.findall(blob))

def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python charset_check.py <caminho-do-ScriptEvent.sdat>  "
                 "(o usuário entrega o arquivo; nunca hardcoded na config)")
    sdat = sys.argv[1]
    blob = open(sdat, "rb").read().decode("utf-8", errors="ignore")
    print("=== Gate de charset pt-BR (acento em palavra real; filtra ruido binario) ===")
    present, absent = [], []
    for name, cp in PTBR.items():
        ch = chr(cp)
        n = textual_count(blob, ch)
        glyph = name.replace("_", " ")
        if n > 0:
            present.append((name, cp, n))
            print(f"  {glyph:<10} U+{cp:04X}  PRESENTE em texto (x{n})")
        else:
            absent.append((name, cp))
            print(f"  {glyph:<10} U+{cp:04X}  nao visto em texto EN")
    print(f"\nConfirmados em texto real: {len(present)}/{len(PTBR)}")
    if absent:
        print("Nao vistos (ingles quase nao usa; mesmo bloco Latin-1 dos confirmados): " +
              ", ".join(f"U+{cp:04X}" for _, cp in absent))
    block_ok = len(present) >= 3
    print("\nVEREDITO: " + (
        "varios acentos do Latin-1 Supplement ja sao renderizados em texto real -> "
        "a fonte cobre esse bloco contiguo, onde vivem TODOS os acentos pt-BR. "
        "Suporte ALTAMENTE PROVAVEL; confirmar 'a-til/o-til' in-game antes de producao." if block_ok else
        "evidencia fraca — inspecionar fonte / testar in-game."))

if __name__ == "__main__":
    main()
