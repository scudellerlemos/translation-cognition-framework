#!/usr/bin/env python3
"""
reinsert.py — conector hex_binary para Utawarerumono (versão ENG/Steam)

Reinseridor DETERMINÍSTICO: approved_translations.csv -> output/ScriptEvent.sdat

Contrato (framework/connectors/hex_binary.md):
  entrada : approved_translations.csv (id, text_target) + dialogs.csv (byte_budget) + .sdat original (read-only)
  saída   : output/ScriptEvent.sdat (mesma extensão do input) + reinsertion_report.md

Regras:
- NUNCA escreve no binário-fonte. Lê o original (read-only) e grava em output/ no projeto.
- 100% determinístico. A IA não escreve a tradução à mão — este script aplica o arquivo APROVADO.
- Gate de round-trip: reinserir o text_source (idêntico) reproduz o original byte-a-byte.
- POC: grava só as linhas que cabem no byte_budget; as que estouram entram no resíduo (repoint = próximo passo).

Caminho do binário (NUNCA hardcoded): o usuário fornece o arquivo a traduzir.
Resolução: (1) argumento de linha de comando; senão (2) connector.source_binary do project.json.
A saída em output/ preserva o NOME e a EXTENSÃO do input.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # raiz do projeto
ART = ROOT / "artifacts"
REPORT = ART / "reinsertion_report.md"


def resolve_source() -> Path:
    """Caminho do binário-fonte: CLI > connector.source_binary do project.json. Sem hardcode."""
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
    else:
        cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
        sb = cfg.get("connector", {}).get("source_binary", "")
        if not sb:
            sys.exit("ERRO: forneça o binário-fonte via argumento "
                     "(`python reinsert.py <caminho>`) ou preencha "
                     "`connector.source_binary` no project.json.")
        p = Path(sb)
        if not p.is_absolute():
            p = ROOT / p
    if not p.is_file():
        sys.exit(f"ERRO: binário não encontrado: {p}\n"
                 "Aponte `connector.source_binary` (no project.json) ou o argumento de CLI "
                 "para o arquivo do jogo a traduzir.")
    return p


def write_slot(buf: bytearray, offset: int, budget: int, text: str) -> bool:
    """Grava 'text' (UTF-8) no slot [offset, offset+budget], mantendo o \\0 terminador.
    Retorna True se coube (len <= budget)."""
    data = text.encode("utf-8")
    if len(data) > budget:
        return False
    buf[offset:offset + len(data)] = data
    for i in range(offset + len(data), offset + budget + 1):
        buf[i] = 0x00
    return True


def load_budgets():
    return {r["offset"]: (r["text_source"], int(r["byte_budget"]))
            for r in csv.DictReader((ART / "dialogs.csv").open(encoding="utf-8"))}


def round_trip_selftest(original: bytes, budgets) -> bool:
    """Reinsere o text_source (idêntico) nos mesmos offsets -> deve reproduzir o original."""
    buf = bytearray(original)
    for off, (src, budget) in budgets.items():
        write_slot(buf, int(off, 16), budget, src)
    return bytes(buf) == original


def main():
    src = resolve_source()
    OUT = ROOT / "output" / src.name          # mesmo nome e extensão do input
    original = src.read_bytes()
    budgets = load_budgets()
    approved = list(csv.DictReader((ART / "approved_translations.csv").open(encoding="utf-8")))

    # 1) GATE DE ROUND-TRIP
    rt = round_trip_selftest(original, budgets)
    print(f"Round-trip self-test: {'OK (byte-identico)' if rt else 'FALHOU'}")

    # 2) aplicar o APROVADO (só as que cabem)
    buf = bytearray(original)
    report, fit = [], 0
    for row in approved:
        off = row["offset"]
        tgt = row["text_target"]
        _src, budget = budgets[off]
        ok = write_slot(buf, int(off, 16), budget, tgt)
        tb = len(tgt.encode("utf-8"))
        report.append((off, "T1_in_place" if ok else "T4_residuo", tb, budget, tgt))
        if ok:
            fit += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(buf)

    # 3) relatório
    lines = ["# Reinsertion Report — Utawarerumono (POC 20 linhas)", "",
             f"- Round-trip self-test: {'OK' if rt else 'FALHOU'}",
             f"- Saída: output/{OUT.name} (mesmo nome e extensão do input)",
             f"- Aplicadas in_place (cabem): {fit}/{len(approved)}",
             f"- Resíduo T4 (estouram byte_budget): {len(approved)-fit}/{len(approved)} — exigem repoint ou abreviação",
             "", "| offset | tier | pt_bytes | budget | texto |", "|---|---|---|---|---|"]
    for off, tier, tb, budget, tgt in report:
        safe = tgt.replace("|", "\\|")
        lines.append(f"| {off} | {tier} | {tb} | {budget} | {safe} |")
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Aplicadas in_place: {fit}/{len(approved)}  |  resíduo: {len(approved)-fit}")
    print(f"SAÍDA -> {OUT}")
    print(f"Relatório -> {REPORT}")


if __name__ == "__main__":
    main()
