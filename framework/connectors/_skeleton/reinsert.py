#!/usr/bin/env python3
"""
ESQUELETO — reinsert.py  (conector hex_binary)

Reinseridor DETERMINÍSTICO: approved_translations.csv -> output/<nome-original> + patch

A IA adapta este esqueleto ao formato do binário específico de cada projeto e o salva em
    projects/<título>/connector/reinsert.py
Criar SÓ com permissão (governança de scripts); se já existir, apenas EXECUTAR.

Contrato (ver framework/connectors/hex_binary.md):
    entrada : approved_translations.csv + dialogs.csv + table_schema + source_binary
    saída   : output/<nome-original> (mesma extensão do input) + patch + reinsertion_report.md

Regras:
- 100% determinístico no caminho mecânico. LLM NUNCA escreve bytes nem recalcula ponteiros.
- A cascata de encaixe (direct/repoint/trimmed) é determinística; o resíduo (residue) é tratado
  FORA daqui, por uma chamada LLM em lote no Passo 08 — este script apenas REPORTA o resíduo.
- O original-fonte nunca é sobrescrito em disco: gera-se cópia + patch.
- Sobrescreve o idioma-fonte pelo idioma-alvo (ex: EN -> pt-BR).
"""

import csv
import json
import sys
from pathlib import Path

from extract import load_table, resolve_source  # mesmo table_schema -> garante round-trip


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
# 2. CASCATA DE ENCAIXE (determinística — direct/repoint/trimmed)
# ---------------------------------------------------------------------------
def fit_string(encoded: bytes, budget: int, ctx) -> tuple[bytes | None, str]:
    """
    Retorna (bytes_para_gravar, tier) ou (None, "residue") se nem "trimmed" resolver.
    NUNCA chama LLM. O resíduo é resolvido fora, em lote, no Passo 08.
    """
    # direct — escrita direta
    if len(encoded) <= budget:
        return encoded, "direct"
    # repoint — recuperação de espaço (repoint / reuso) — adaptar ao formato
    #   if ctx.space_strategy == "repoint": return encoded, "repoint"
    # trimmed — trim mecânico determinístico
    trimmed = (encoded
               .replace(b"  ", b" "))          # colapsar espaços duplos (exemplo)
    # TODO: reticência tipográfica, abreviações do glossário do projeto
    if len(trimmed) <= budget:
        return trimmed, "trimmed"
    # residue: reportar p/ reescrita por LLM em lote (fora deste script)
    return None, "residue"


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
def main(project_json: Path, source_override: str | None = None):
    try:                                              # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    conn = cfg["connector"]
    root = project_json.parent

    src_path, _ = resolve_source(root, conn, source_override)  # mesma fonte entregue na extração
    original = src_path.read_bytes()
    table = load_table(root / conn["table_schema"])
    buf = bytearray(original)

    id_col = cfg["source"]["id_column"]
    residue = []   # strings em residue — vão para reescrita LLM em lote (Passo 08)
    report = []

    # byte_budget vem do dialogs.csv (source); a tradução aprovada vem do approved_translations.csv
    budgets = {r[id_col]: int(r["byte_budget"])
               for r in csv.DictReader((root / "artifacts" / "dialogs.csv").open(encoding="utf-8"))}

    with (root / "artifacts" / "approved_translations.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            target = row.get("text_target", "")
            if not target:
                continue                                   # pendente — pula
            offset = int(row[id_col], 16)
            budget = budgets[row[id_col]]
            encoded = encode_string(target, table)
            to_write, tier = fit_string(encoded, budget, conn)
            if to_write is None:
                residue.append(row[id_col])
                report.append((row[id_col], "residue_overflow", len(encoded), budget))
                continue
            buf[offset:offset + len(to_write)] = to_write  # sobrescreve fonte->alvo
            report.append((row[id_col], tier, len(to_write), budget))

    # saída em output/ com o MESMO nome e extensão do input (nunca sobre o original)
    out_bin = root / "output" / src_path.name
    out_bin.parent.mkdir(parents=True, exist_ok=True)
    out_bin.write_bytes(buf)
    print(f"Saída gravada em: {out_bin}")            # informar o usuário o diretório de saída

    # patch padrão
    emit_patch(original, bytes(buf), conn.get("patch_format", "ips"),
               root / "output" / f"patch.{conn.get('patch_format', 'ips')}")

    # reinsertion_report.md — overflows/repoints/falhas viram issues p/ 06c/07
    lines = "\n".join(f"- {i} [{t}] {n}/{b} bytes" for i, t, n, b in report)
    (root / "artifacts" / "reinsertion_report.md").write_text(
        f"# Reinsertion Report\n\n"
        f"Strings em resíduo (overflow — reescrever por LLM em lote): {len(residue)}\n\n"
        f"{lines}\n",
        encoding="utf-8",
    )
    if residue:
        print(f"ATENÇÃO: {len(residue)} strings em overflow -> reescrita LLM em lote (Passo 08)")
    print(f"Build gerado -> {out_bin}")


if __name__ == "__main__":
    # Uso: python reinsert.py [project.json] [<caminho-do-binário-entregue>]
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    override = sys.argv[2] if len(sys.argv) > 2 else None
    main(proj, override)
