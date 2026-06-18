#!/usr/bin/env python3
"""
reinsert.py — conector hex_binary para Breath of Fire IV (PC port, Capcom, 2000)

Status: FASE 00 — MAPEAMENTO PENDENTE
Implementar encode_string e fit_string após mapeamento do Passo 00.

Contrato (ver framework/connectors/hex_binary.md):
    entrada : approved_translations.csv + dialogs.csv + table_schema + source_binary
    saída   : output/<nome-original> + patch + reinsertion_report.md

Regras:
- 100% determinístico. LLM NUNCA escreve bytes nem recalcula ponteiros.
- T4 (overflow irredutível) é reportado para reescrita LLM em lote no Passo 08.
- O binário-fonte nunca é sobrescrito; a saída vai para output/.
"""

import csv
import json
import sys
from pathlib import Path

from extract import load_table, resolve_source  # mesmo table_schema -> garante round-trip


# ---------------------------------------------------------------------------
# 1. ENCODE
# ---------------------------------------------------------------------------
def encode_string(text: str, table) -> bytes:
    """
    TBD — implementar após mapeamento do encoding de BoF4 PC.
    Inverso de decode_string em extract.py.
    """
    raise NotImplementedError(
        "encode_string não implementado. Mapear charset de BoF4 PC no Passo 00 "
        "antes de implementar."
    )


# ---------------------------------------------------------------------------
# 2. CASCATA DE ENCAIXE (T1–T3)
# ---------------------------------------------------------------------------
def fit_string(encoded: bytes, budget: int, conn: dict) -> tuple[bytes | None, str]:
    """
    T1: direto. T2: repoint (TBD). T3: trim mecânico. T4: resíduo.
    NUNCA chama LLM.
    """
    if len(encoded) <= budget:
        return encoded, "T1"
    # T2/T3 — adaptar à estratégia de espaço do BoF4 PC após mapeamento
    trimmed = encoded.replace(b"  ", b" ")
    if len(trimmed) <= budget:
        return trimmed, "T3"
    return None, "T4"


# ---------------------------------------------------------------------------
# 3. PATCH
# ---------------------------------------------------------------------------
def emit_patch(original: bytes, modified: bytes, fmt: str, out_path: Path):
    """TBD — implementar após definir patch_format para BoF4 PC."""
    raise NotImplementedError(f"emit_patch não implementado para formato '{fmt}'.")


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------
def main(project_json: Path, source_override: str | None = None):
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    conn = cfg["connector"]
    root = project_json.parent

    src_path, _ = resolve_source(root, conn, source_override)
    original = src_path.read_bytes()
    table = load_table(root / conn["table_schema"])
    buf = bytearray(original)

    id_col = cfg["source"]["id_column"]
    residue = []
    report = []

    budgets = {r[id_col]: int(r["byte_budget"])
               for r in csv.DictReader((root / "artifacts" / "dialogs.csv").open(encoding="utf-8"))}

    with (root / "artifacts" / "approved_translations.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            target = row.get("text_target", "")
            if not target:
                continue
            offset = int(row[id_col], 16)
            budget = budgets[row[id_col]]
            encoded = encode_string(target, table)
            to_write, tier = fit_string(encoded, budget, conn)
            if to_write is None:
                residue.append(row[id_col])
                report.append((row[id_col], "T4_overflow", len(encoded), budget))
                continue
            buf[offset:offset + len(to_write)] = to_write
            report.append((row[id_col], tier, len(to_write), budget))

    out_bin = root / "output" / src_path.name
    out_bin.parent.mkdir(parents=True, exist_ok=True)
    out_bin.write_bytes(buf)
    print(f"Saída gravada em: {out_bin}")

    patch_fmt = conn.get("patch_format", "ips")
    emit_patch(original, bytes(buf), patch_fmt,
               root / "output" / f"patch.{patch_fmt}")

    lines = "\n".join(f"- {i} [{t}] {n}/{b} bytes" for i, t, n, b in report)
    (root / "artifacts" / "reinsertion_report.md").write_text(
        f"# Reinsertion Report — Breath of Fire IV\n\n"
        f"Resíduo T4 (overflow — reescrever por LLM em lote): {len(residue)}\n\n"
        f"{lines}\n",
        encoding="utf-8",
    )
    if residue:
        print(f"ATENÇÃO: {len(residue)} strings em T4 -> reescrita LLM em lote (Passo 08)")
    print(f"Build gerado -> {out_bin}")


if __name__ == "__main__":
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
