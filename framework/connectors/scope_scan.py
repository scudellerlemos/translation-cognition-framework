#!/usr/bin/env python3
"""scope_scan.py — varredura de escopo da Fase 0: o que da pasta do jogo o dialogs.csv NAO cobre.

Agrupa os arquivos da pasta por extensao e marca, por arquivo, se o nome aparece em algum `offset` do
dialogs.csv (offset = "<cena>:<arquivo>:<...>"). Extensao sem nenhum arquivo coberto e candidata a escopo
esquecido (folha de imagem com rotulo, menu, texto de sistema) — decisao entre `dialogo` e `completo`.

Uso: python scope_scan.py <dialogs.csv | pasta_do_projeto> <pasta_do_jogo>
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


def scan(dialogs: Path, game_dir: Path) -> dict[str, dict]:
    """{extensao: {files, covered, bytes, uncovered_bytes}}"""
    dialogs = Path(dialogs)   # um dialogs.csv, ou uma pasta (o projeto: junta todos os dialogs.csv dela)
    owned = set()
    for csv_path in [dialogs] if dialogs.is_file() else sorted(dialogs.rglob("dialogs.csv")):
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            owned |= {part.lower() for r in csv.DictReader(fh) for part in r.get("offset", "").split(":")}
    out: dict[str, dict] = defaultdict(lambda: {"files": 0, "covered": 0, "bytes": 0, "uncovered_bytes": 0})
    for f in sorted(Path(game_dir).rglob("*")):
        if f.is_file():
            e, size = out[f.suffix.lower() or "(sem ext)"], f.stat().st_size
            e["files"] += 1
            e["bytes"] += size
            if f.name.lower() in owned:
                e["covered"] += 1
            else:
                e["uncovered_bytes"] += size
    return dict(out)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    rep = scan(Path(sys.argv[1]), Path(sys.argv[2]))
    print(f"{'ext':10} {'arquivos':>8} {'cobertos':>8} {'bytes_sem_dono':>15}")
    for ext, v in sorted(rep.items(), key=lambda kv: -kv[1]["uncovered_bytes"]):
        flag = "  <- nenhum coberto: escopo?" if v["covered"] == 0 else ""
        print(f"{ext:10} {v['files']:>8} {v['covered']:>8} {v['uncovered_bytes']:>15}{flag}")


if __name__ == "__main__":
    main()
