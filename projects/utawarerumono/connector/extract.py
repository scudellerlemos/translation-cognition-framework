#!/usr/bin/env python3
"""
extract.py — conector hex_binary para Utawarerumono: Mask of Deception (versão ENG/Steam)

Formato do container ScriptEvent.sdat (descoberto na POC):
- Cabeçalho "Filename    " + tabela de offsets (índice do script)
- Bloco de texto: strings UTF-8 **null-terminated** e **contíguas**
- Control codes embutidos como tokens legíveis: {W75}, {W80}, {W10}, {COLOR}, {END}
- Linhas de sistema em CAPS

Contrato (framework/connectors/hex_binary.md):
  entrada : .sdat
  saída   : dialogs.csv (offset, text_source, byte_budget)

Determinístico. O offset (hex) é o id_column — âncora para reinserção.
byte_budget = nº de bytes UTF-8 da string (sem o terminador \\0) — orçamento para reinserção in_place.

POC: extrai N strings de texto a partir da primeira fala (FIRST_DIALOGUE_OFFSET).

Caminho do binário (NUNCA hardcoded): o usuário fornece o arquivo a traduzir.
Resolução: (1) argumento de linha de comando; senão (2) connector.source_binary do project.json.
Se nenhum resolver para um arquivo existente, falha com mensagem clara.
"""

import csv
import json
import sys
from pathlib import Path

# --- config da POC ---
FIRST_DIALOGUE_OFFSET = 0x3398   # "Ngh... ghh..." — início da cena de abertura
N_LINES = 20
ROOT = Path(__file__).resolve().parent.parent          # raiz do projeto
OUT = ROOT / "artifacts" / "dialogs.csv"


def resolve_source() -> Path:
    """Caminho do binário a traduzir: CLI > connector.source_binary do project.json.
    Sem hardcode. O usuário deve fornecer o arquivo."""
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
    else:
        cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
        sb = cfg.get("connector", {}).get("source_binary", "")
        if not sb:
            sys.exit("ERRO: forneça o binário a traduzir via argumento "
                     "(`python extract.py <caminho>`) ou preencha "
                     "`connector.source_binary` no project.json.")
        p = Path(sb)
        if not p.is_absolute():
            p = ROOT / p                                # relativo à raiz do projeto
    if not p.is_file():
        sys.exit(f"ERRO: binário não encontrado: {p}\n"
                 "Aponte `connector.source_binary` (no project.json) ou o argumento de CLI "
                 "para o arquivo do jogo a traduzir.")
    return p


def is_displayable(text: str) -> bool:
    """String de texto exibível: tem ao menos um caractere alfanumérico."""
    return any(c.isalnum() for c in text)


def extract(data: bytes, start: int, n: int):
    rows = []
    i = start
    while len(rows) < n and i < len(data):
        # lê até o próximo \0
        end = data.find(b"\x00", i)
        if end == -1:
            break
        raw = data[i:end]
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("utf-8", errors="replace")
        if raw and is_displayable(text):
            rows.append({
                "offset": f"0x{i:x}",
                "text_source": text,
                "byte_budget": len(raw),   # bytes sem o \0
            })
        i = end + 1
    return rows


def main():
    src = resolve_source()
    data = src.read_bytes()
    rows = extract(data, FIRST_DIALOGUE_OFFSET, N_LINES)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["offset", "text_source", "byte_budget"])
        w.writeheader()
        w.writerows(rows)
    print(f"Extraídas {len(rows)} linhas -> {OUT}")
    for r in rows:
        print(f'  {r["offset"]:>8}  [{r["byte_budget"]:>3}b]  {r["text_source"]}')


if __name__ == "__main__":
    main()
