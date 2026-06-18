#!/usr/bin/env python3
"""
extract.py — conector hex_binary para Breath of Fire IV (PC port, Capcom, 2000)

Status: FASE 00 — MAPEAMENTO PENDENTE
Este arquivo é um stub adaptado do _skeleton. Implementar load_table e
iter_string_offsets após análise do hex dump (ver connector/table_schema.md).

Contrato (ver framework/connectors/hex_binary.md):
    entrada : source_binary (arquivo de diálogo do jogo) + table_schema
    saída   : artifacts/dialogs.csv (offset, text_en, byte_budget) + extraction_log.md

Regras:
- 100% determinístico. NUNCA usar LLM aqui.
- Compartilhar o MESMO table_schema com reinsert.py (garante round-trip).
- Emitir byte_budget por string (shift-left — consumido no Passo 06).
- Não modificar o binário-fonte (somente leitura).
"""

import csv
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. CARREGAR O SCHEMA DE TABELA
# ---------------------------------------------------------------------------
def load_table(table_path: Path):
    """
    TBD — preencher após mapeamento do Passo 00.
    Retorna: (byte_to_char, control_map, terminator)
    """
    # TODO: parsear connector/table_schema.md após mapeamento
    byte_to_char = {}
    control_map = []
    terminator = b"\x00"
    raise NotImplementedError(
        "load_table não implementado. Mapear o charset de BoF4 PC no Passo 00 "
        "e preencher connector/table_schema.md antes de implementar."
    )


# ---------------------------------------------------------------------------
# 2. DECODIFICAR UMA STRING A PARTIR DE UM OFFSET
# ---------------------------------------------------------------------------
def decode_string(data: bytes, offset: int, table) -> tuple[str, int]:
    byte_to_char, control_map, terminator = table
    out = []
    i = offset
    while not data[i:].startswith(terminator):
        matched = False
        for seq, token in control_map:
            if data[i:i + len(seq)] == seq:
                out.append(token)
                i += len(seq)
                matched = True
                break
        if matched:
            continue
        ch = byte_to_char.get(data[i:i + 1])
        if ch is None:
            ch = f"[{data[i]:02X}]"
        out.append(ch)
        i += 1
    byte_budget = (i + len(terminator)) - offset
    return "".join(out), byte_budget


# ---------------------------------------------------------------------------
# 3. LOCALIZAR AS STRINGS
# ---------------------------------------------------------------------------
def iter_string_offsets(data: bytes, project_cfg: dict):
    """
    TBD — preencher após mapeamento da estrutura de ponteiros de BoF4 PC.
    Retorna iterável de offsets inteiros.
    """
    # TODO: implementar após mapeamento do Passo 00
    raise NotImplementedError(
        "iter_string_offsets não implementado. Determinar estratégia de ponteiros "
        "do engine Capcom BoF4 PC (tabela central? inline? varredura sequencial?) "
        "e documentar em connector/table_schema.md."
    )


# ---------------------------------------------------------------------------
# 4. RESOLVE SOURCE
# ---------------------------------------------------------------------------
def resolve_source(root: Path, conn: dict, cli_override: str | None) -> tuple[Path, str]:
    if cli_override:
        return Path(cli_override), f"CLI: {cli_override}"
    declared = conn["source_binary"]
    if Path(declared).is_absolute():
        raise SystemExit(
            f"source_binary não pode ser absoluto na config ({declared}). "
            f"Copie o arquivo para artifacts/ (caminho relativo) ou passe por CLI."
        )
    if "TBD" in declared:
        raise SystemExit(
            "source_binary ainda é 'TBD' em project.json. "
            "Copie o binário de diálogo para artifacts/ e atualize o campo."
        )
    return (root / declared), f"config: {declared}"


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
def main(project_json: Path, source_override: str | None = None):
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    conn = cfg["connector"]
    root = project_json.parent

    src_path, provenance = resolve_source(root, conn, source_override)
    data = src_path.read_bytes()
    table = load_table(root / conn["table_schema"])

    id_col = cfg["source"]["id_column"]
    rows = []
    for offset in iter_string_offsets(data, cfg):
        text, budget = decode_string(data, offset, table)
        rows.append({id_col: f"0x{offset:x}", "text_en": text, "byte_budget": budget})

    out_csv = root / cfg["source"]["file"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[id_col, "text_en", "byte_budget"])
        w.writeheader()
        w.writerows(rows)

    log = root / "artifacts" / "extraction_log.md"
    log.write_text(
        f"# Extraction Log — Breath of Fire IV\n\n"
        f"- Binário (entregue): {src_path.name}\n"
        f"- Proveniência: {provenance}\n"
        f"- Container: {conn.get('container_format', 'TBD')}\n"
        f"- Encoding: {conn.get('encoding', 'TBD')}\n"
        f"- Total de strings: {len(rows)}\n",
        encoding="utf-8",
    )
    print(f"Extraídas {len(rows)} strings -> {out_csv}")


if __name__ == "__main__":
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
