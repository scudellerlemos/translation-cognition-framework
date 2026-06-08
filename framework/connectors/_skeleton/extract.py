#!/usr/bin/env python3
"""
ESQUELETO — extract.py  (conector hex_binary)

Extrator DETERMINÍSTICO: binário -> dialogs.csv

A IA adapta este esqueleto ao formato do binário específico de cada projeto e o salva em
    projects/<título>/connector/extract.py

Contrato (ver framework/connectors/hex_binary.md):
    entrada : source_binary + table_schema
    saída   : dialogs.csv (id_column, text_source, byte_budget) + extraction_log.md

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
    Retorna:
      byte_to_char : dict[bytes, str]   mapa de caracteres
      control_map  : list[(bytes, str)] sequências de control code -> token
      terminator   : bytes
    Adaptar o parser ao formato real do table_schema do projeto.
    """
    # TODO: parsear table_schema.md / .tbl do projeto
    byte_to_char = {}
    control_map = []          # ordenar por comprimento decrescente p/ casar sequências longas 1º
    terminator = b"\x00"
    raise NotImplementedError("Adaptar load_table ao table_schema do projeto")


# ---------------------------------------------------------------------------
# 2. DECODIFICAR UMA STRING A PARTIR DE UM OFFSET
# ---------------------------------------------------------------------------
def decode_string(data: bytes, offset: int, table) -> tuple[str, int]:
    """
    Lê do offset até o terminador. Retorna (texto_com_tokens, n_bytes_consumidos).
    n_bytes_consumidos é o byte_budget da string (espaço ocupado no binário).
    """
    byte_to_char, control_map, terminator = table
    out = []
    i = offset
    while not data[i:].startswith(terminator):
        # 2a. tentar casar um control code (sequência -> token)
        matched = False
        for seq, token in control_map:          # control_map ordenado por len desc
            if data[i:i + len(seq)] == seq:
                out.append(token)
                i += len(seq)
                matched = True
                break
        if matched:
            continue
        # 2b. caractere normal
        # TODO: respeitar largura (fixed-1/fixed-2/variable) do encoding do projeto
        ch = byte_to_char.get(data[i:i + 1])
        if ch is None:
            ch = f"[{data[i]:02X}]"             # byte desconhecido -> marcar p/ revisão
        out.append(ch)
        i += 1
    byte_budget = (i + len(terminator)) - offset
    return "".join(out), byte_budget


# ---------------------------------------------------------------------------
# 3. LOCALIZAR AS STRINGS (via tabela de ponteiros ou varredura)
# ---------------------------------------------------------------------------
def iter_string_offsets(data: bytes, project_cfg: dict):
    """
    Produz os offsets de cada string. Duas estratégias comuns:
      - ler a pointer_table declarada no project.json
      - varrer sequencialmente entre terminadores
    Adaptar ao formato do projeto.
    """
    raise NotImplementedError("Adaptar iter_string_offsets (pointer_table ou varredura)")


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------
def resolve_source(root: Path, conn: dict, cli_override: str | None) -> tuple[Path, str]:
    """
    Resolve o binário-fonte ENTREGUE pelo usuário e devolve (caminho, proveniência).
    - cli_override (arg de CLI no runtime) tem prioridade — é uma das formas de entrega.
    - Senão, usa conn['source_binary'], resolvido RELATIVO à raiz do projeto.
    Governança: o caminho da config nunca deve ser absoluto/externo persistido.
    """
    if cli_override:
        src = Path(cli_override)
        return src, f"CLI: {cli_override}"
    declared = conn["source_binary"]
    if Path(declared).is_absolute():
        raise SystemExit(
            f"source_binary não pode ser absoluto na config ({declared}). "
            f"Copie o arquivo para artifacts/ (caminho relativo) ou passe por CLI."
        )
    return (root / declared), f"config: {declared}"


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
        rows.append({id_col: f"0x{offset:x}", "text_source": text, "byte_budget": budget})

    # dialogs.csv — output explícito do Passo 00
    out_csv = root / cfg["source"]["file"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[id_col, "text_source", "byte_budget"])
        w.writeheader()
        w.writerows(rows)

    # extraction_log.md — metadados auditáveis
    log = root / "artifacts" / "extraction_log.md"
    log.write_text(
        f"# Extraction Log\n\n"
        f"- Binário (entregue): {src_path.name}\n"
        f"- Proveniência: {provenance}\n"
        f"- Container: {conn.get('container_format', 'none')}"
        f"{(' / inner: ' + conn['inner_path']) if conn.get('inner_path') else ''}\n"
        f"- Tabela: {conn['table_schema']}\n"
        f"- Encoding: {conn.get('encoding')}\n"
        f"- Total de strings: {len(rows)}\n",
        encoding="utf-8",
    )
    print(f"Extraídas {len(rows)} strings -> {out_csv}")


if __name__ == "__main__":
    # Uso: python extract.py [project.json] [<caminho-do-binário-entregue>]
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
