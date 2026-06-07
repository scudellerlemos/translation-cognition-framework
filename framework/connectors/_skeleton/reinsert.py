#!/usr/bin/env python3
"""
ESQUELETO — reinsert.py  (conector hex_binary)

Reinseridor DETERMINÍSTICO: translated.csv -> binário traduzido + patch

A IA adapta este esqueleto ao formato do binário específico de cada projeto e o salva em
    projects/<título>/connector/reinsert.py

Contrato (ver framework/connectors/hex_binary.md):
    entrada : translated.csv + table_schema + source_binary
    saída   : binário traduzido + patch (ips/bps/xdelta) + reinsertion_report.md

Regras:
- 100% determinístico no caminho mecânico. LLM NUNCA escreve bytes nem recalcula ponteiros.
- A cascata de encaixe (T1–T3) é determinística; T4 (resíduo) é tratado FORA daqui,
  por uma chamada LLM em lote no Passo 08 — este script apenas REPORTA o resíduo.
- O original-fonte nunca é sobrescrito em disco: gera-se cópia + patch.
- Sobrescreve o idioma-fonte pelo idioma-alvo (ex: EN -> pt-BR).
"""

import csv
import json
import sys
from pathlib import Path

from extract import load_table  # mesmo table_schema -> garante round-trip


# ---------------------------------------------------------------------------
# 1. ENCODE: texto (com tokens) -> bytes
# ---------------------------------------------------------------------------
def encode_string(text: str, table) -> bytes:
    """Inverso de decode_string. token->control bytes, char->byte, + terminador."""
    byte_to_char, control_map, terminator = table
    char_to_byte = {v: k for k, v in byte_to_char.items()}
    token_to_bytes = {tok: seq for seq, tok in control_map}
    # TODO: tokenizar 'text' separando tokens ({...}, \n) de caracteres normais
    raise NotImplementedError("Adaptar encode_string ao encoding do projeto")


# ---------------------------------------------------------------------------
# 2. CASCATA DE ENCAIXE (determinística — T1..T3)
# ---------------------------------------------------------------------------
def fit_string(encoded: bytes, budget: int, ctx) -> tuple[bytes | None, str]:
    """
    Retorna (bytes_para_gravar, tier) ou (None, "T4") se nem T3 resolver.
    NUNCA chama LLM. O resíduo T4 é resolvido fora, em lote, no Passo 08.
    """
    # T1 — escrita direta
    if len(encoded) <= budget:
        return encoded, "T1"
    # T2 — recuperação de espaço (repoint / reuso) — adaptar ao formato
    #   if ctx.space_strategy == "repoint": return encoded, "T2"
    # T3 — trim mecânico determinístico
    trimmed = (encoded
               .replace(b"  ", b" "))          # colapsar espaços duplos (exemplo)
    # TODO: reticência tipográfica, abreviações do glossário do projeto
    if len(trimmed) <= budget:
        return trimmed, "T3"
    # T4 — resíduo: reportar p/ reescrita por LLM em lote (fora deste script)
    return None, "T4"


# ---------------------------------------------------------------------------
# 3. EMITIR PATCH (determinístico)
# ---------------------------------------------------------------------------
def emit_patch(original: bytes, modified: bytes, fmt: str, out_path: Path):
    """fmt: ips | bps | xdelta. Gera patch a partir do diff dos dois binários."""
    # TODO: implementar/charmar lib do formato escolhido (ex: ips simples é trivial de gerar)
    raise NotImplementedError(f"Adaptar emit_patch para {fmt}")


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------
def main(project_json: Path):
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    conn = cfg["connector"]
    root = project_json.parent

    original = (root / conn["source_binary"]).read_bytes()
    table = load_table(root / conn["table_schema"])
    buf = bytearray(original)

    id_col = cfg["source"]["id_column"]
    residue = []   # strings T4 — vão para reescrita LLM em lote (Passo 08)
    report = []

    with (root / "artifacts" / "translated.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            target = row.get("text_target", "")
            if not target:
                continue                                   # pendente — pula
            offset = int(row[id_col], 16)
            budget = int(row["byte_budget"])
            encoded = encode_string(target, table)
            to_write, tier = fit_string(encoded, budget, conn)
            if to_write is None:
                residue.append(row[id_col])
                report.append((row[id_col], "T4_overflow", len(encoded), budget))
                continue
            buf[offset:offset + len(to_write)] = to_write  # sobrescreve fonte->alvo
            report.append((row[id_col], tier, len(to_write), budget))

    # binário traduzido (cópia, nunca sobre o original)
    out_bin = root / "artifacts" / "translated_build.bin"
    out_bin.write_bytes(buf)

    # patch padrão
    emit_patch(original, bytes(buf), conn.get("patch_format", "ips"),
               root / "artifacts" / f"patch.{conn.get('patch_format', 'ips')}")

    # reinsertion_report.md — overflows/repoints/falhas viram issues p/ 06c/07
    lines = "\n".join(f"- {i} [{t}] {n}/{b} bytes" for i, t, n, b in report)
    (root / "artifacts" / "reinsertion_report.md").write_text(
        f"# Reinsertion Report\n\n"
        f"Strings em resíduo T4 (overflow — reescrever por LLM em lote): {len(residue)}\n\n"
        f"{lines}\n",
        encoding="utf-8",
    )
    if residue:
        print(f"ATENÇÃO: {len(residue)} strings em overflow T4 -> reescrita LLM em lote (Passo 08)")
    print(f"Build gerado -> {out_bin}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "project.json"))
