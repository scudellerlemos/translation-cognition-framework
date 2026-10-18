#!/usr/bin/env python3
"""reinsert.py — conector Utawarerumono: Prelude to the Fallen (escrito do zero; formato em table_schema.md).

Reinseridor DETERMINISTICO: approved_translations.csv -> output/DataBase2.sdat. Cada membro ScriptTextData
tocado e reconstruido (ponteiros recalculados, colunas JA/KO/ZH byte-identicas, so a coluna EN muda) e a
tabela Pack do contêiner e atualizada. Sem traducao nenhuma, a saida e byte-identica ao original.

Uso: python reinsert.py [project.json|raiz] [<DataBase2.sdat | pasta Data>]
"""
import contextlib
import json
import sys
from pathlib import Path

from extract import (
    EN_COL,
    LANGS,
    build_text_member,
    connector_io,
    read_sdat,
    resolve_sdat,
    text_members,
    write_sdat,
)
from font import fit


def rebuild(data: bytes, approved: dict[str, str], transliterate: bool = False) -> tuple[bytes, list[str]]:
    """(novo contêiner, ids de `approved` sem destino). Ids vazios/ausentes mantem o EN original."""
    sd = read_sdat(data)
    members = list(sd.members)
    used: set[str] = set()
    for scene, i, n, cols, strings, why in text_members(sd):
        if why:
            continue
        changed = False
        for idx in range(n):
            key = f"{scene}:{idx}"
            if key in approved:
                used.add(key)
                text = connector_io.transliterate(approved[key]) if transliterate else fit(approved[key])
                strings[idx * len(LANGS) + EN_COL] = text.encode("utf-8")
                changed = True
        if changed:
            members[i] = build_text_member(n, cols, strings)
    return write_sdat(sd, members), sorted(set(approved) - used)


def main(project_json: Path, source_override: str | None = None):
    with contextlib.suppress(AttributeError, ValueError, OSError):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.loads(project_json.read_text(encoding="utf-8"))
    conn, root = cfg["connector"], project_json.parent
    src = resolve_sdat(conn, source_override)
    data = src.read_bytes()

    appr_path = root / "artifacts" / "approved_translations.csv"
    approved = connector_io.load_approved(appr_path, "reinserir assim e no-op silencioso") if appr_path.is_file() else {}
    out, orphans = rebuild(data, approved, conn.get("diacritic_strategy") == "transliterate")
    if orphans:
        sys.exit(f"ERRO: {len(orphans)} id(s) aprovado(s) sem destino no binario: {orphans[:5]}")

    out_bin = root / "output" / src.name
    out_bin.parent.mkdir(parents=True, exist_ok=True)
    out_bin.write_bytes(out)
    (root / "artifacts" / "reinsertion_report.md").write_text(
        f"# Reinsertion Report\n\nStrings reinseridas: {len(approved)}\n"
        f"Tamanho: {len(data)} -> {len(out)} bytes (membros reconstruídos; sem resíduo de espaço)\n",
        encoding="utf-8")
    print(f"Build gerado -> {out_bin} ({len(approved)} strings)")


if __name__ == "__main__":
    proj = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("project.json")
    if proj.is_dir():
        proj = proj / "project.json"
    main(proj, sys.argv[2] if len(sys.argv) > 2 else None)
