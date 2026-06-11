#!/usr/bin/env python3
"""
extract_chapter.py — extrai UM capitulo inteiro do container, UMA cena por diretorio.

O extract.py extrai um arco para um dialogs.csv unico (modelo antigo de arco). O harness de escala
(`framework/runtime/`) consome UMA cena por diretorio: `artifacts/ch_<CC_SS>/dialogs.csv`. Este script
faz a ponte: dado um capitulo (prefixo CC), descobre as cenas (agrupando os scripts por prefixo CC_SS,
ex.: todos os `13_02_*` -> cena `ch_13_02`) e escreve um dialogs.csv por cena, na MESMA convencao do
extract.py (offset hex = id; byte_budget = nº de bytes UTF-8 da string sem o terminador; ordem de
exibicao = ordem de armazenamento). Reusa sdat_format -> offsets/budgets identicos aos do cap.12.

GOVERNANCA: determinista, binario READ-ONLY, sem work-text hardcoded (o texto vem do binario). Idempotente.

Uso:  python extract_chapter.py <capitulo> [<caminho-do-binario>]
      ex.: python extract_chapter.py 13           (binario via connector.source_binary do project.json)
           python extract_chapter.py 13 /caminho/ScriptEvent.sdat
"""
import csv
import json
import sys
from pathlib import Path

import sdat_format as S

ROOT = Path(__file__).resolve().parent.parent


def resolve_source(arg: str | None) -> Path:
    """Binario a traduzir: CLI > connector.source_binary do project.json. Sem hardcode."""
    if arg:
        p = Path(arg)
    else:
        cfg = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
        sb = cfg.get("connector", {}).get("source_binary", "")
        if not sb:
            sys.exit("ERRO: forneca o binario via argumento ou connector.source_binary no project.json.")
        p = Path(sb)
        if not p.is_absolute():
            p = ROOT / p
    if not p.is_file():
        sys.exit(f"ERRO: binario nao encontrado: {p}")
    return p


def scene_of(name: str) -> str:
    """Prefixo CC_SS do nome do script (CC_SS_NNNT.BIN) -> agrupa scripts na mesma cena. Ex.:
    '13_02_500S.BIN' -> '13_02'."""
    parts = name.split("_")
    return "_".join(parts[:2]) if len(parts) >= 2 else name


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python extract_chapter.py <capitulo>  (ex.: 13)")
    chap = sys.argv[1].rstrip("_")
    src = resolve_source(sys.argv[2] if len(sys.argv) > 2 else None)
    data = src.read_bytes()

    files = S.parse_pack(data)
    chap_files = [f for f in files if f.name.startswith(f"{chap}_")]
    if not chap_files:
        sys.exit(f"ERRO: nenhum script do capitulo {chap} (ex. de nomes: {[f.name for f in files[:5]]})")

    # agrupa por cena (CC_SS), preservando a ordem do Pack dentro de cada cena
    scenes: dict[str, list] = {}
    for f in chap_files:
        scenes.setdefault(scene_of(f.name), []).append(f)

    total = 0
    summary = []
    for sc in sorted(scenes):
        rows = []
        for f in scenes[sc]:                                  # ordem do Pack (= ordem de exibicao)
            for off, text, budget in S.extract_text_block(data, f):
                rows.append({"offset": f"0x{off:x}", "text_source": text, "byte_budget": budget})
        if not rows:                                          # cena sem texto (ex.: so bytecode) -> pula
            summary.append((sc, 0, len(scenes[sc]), "sem texto"))
            continue
        out_dir = ROOT / "artifacts" / f"ch_{sc}"
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / "dialogs.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["offset", "text_source", "byte_budget"])
            w.writeheader()
            w.writerows(rows)
        total += len(rows)
        summary.append((sc, len(rows), len(scenes[sc]), "ok"))

    print(f"Capitulo {chap}: {len(chap_files)} script(s) em {len(scenes)} cena(s).")
    for sc, n, nf, tag in summary:
        print(f"  ch_{sc}: {n} linhas ({nf} script(s)) {tag}")
    print(f"TOTAL: {total} linhas -> artifacts/ch_{chap}_*/dialogs.csv")


if __name__ == "__main__":
    main()
