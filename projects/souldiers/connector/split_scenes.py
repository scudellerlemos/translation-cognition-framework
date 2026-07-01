#!/usr/bin/env python3
"""
split_scenes.py — Souldiers: agrupa dialogs.csv por cena e cria artifacts/scenes/<cena>/

Lógica de agrupamento por tabela:

  texts_DIALOGS       → STR_DIALOGS<opt_num>_<LOC>_D<n>_<SPEAKER>_<line>
                        cena = LOC  (captura tudo entre STR_DIALOGS*_ e _D\d+_)
                        fallback para IDs sem _D\d+_: strip prefixo + 2x trailing _\d+

  texts_INGAME_DIALOGS→ STR_INGAME_DIALOGS_<SPEAKER>_<LOC>_<opt_n>
                        cena = INGAME_<SPEAKER>_<LOC> sem sufixo numérico final

  texts_SIDE_DIALOGS  → SIDE_DIALOG_<CATEGORY>_<n>
                        cena = SIDE_<CATEGORY> sem sufixo numérico final

Cria:
  artifacts/scenes/<cena>/dialogs.csv  — offset,text_en,byte_budget  (para context_pack)
  artifacts/scenes/<cena>/pack.json    — linhas da cena com metadados extras
  artifacts/scenes_index.json          — mapa cena → [offsets]

Uso:
  python split_scenes.py <project_root>
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# Extratores de cena por tabela
# --------------------------------------------------------------------------

# Captura tudo entre STR_DIALOGS<opt_num>_ e _D\d+_ (greedy para o último _D\d+_)
_DIALOG_SCENE_RE = re.compile(r"^STR_DIALOGS(.*)_D\d+_", re.IGNORECASE)
_TRAILING_NUM_RE = re.compile(r"_\d+$")
_TRAILING_SMALL_RE = re.compile(r"_(\d+)$")


def _strip_small(s: str, threshold: int = 20) -> str:
    """Strip trailing _N se N < threshold (número de linha/encontro, não parte do nome de área)."""
    m = _TRAILING_SMALL_RE.search(s)
    if m and int(m.group(1)) < threshold:
        return s[:m.start()]
    return s


def _scene_dialogs(offset: str) -> str:
    """STR_DIALOGS_CAVE_23_D1_BALOF_1 → CAVE_23
       STR_DIALOGS1_5_D1_ADAMONT_1   → 1_5"""
    m = _DIALOG_SCENE_RE.match(offset)
    if m:
        return m.group(1).strip("_").upper() or "UNKNOWN"
    # fallback: strip STR_DIALOGS<digits>_ e 2x trailing _\d+
    stripped = re.sub(r"^STR_DIALOGS\d*_", "", offset, flags=re.IGNORECASE)
    stripped = _TRAILING_NUM_RE.sub("", stripped)
    stripped = _TRAILING_NUM_RE.sub("", stripped)
    return stripped.upper() or "MISC"


def _scene_ingame(offset: str) -> str:
    """Agrupa INGAME dialogs por área geográfica.

    STR_INGAME_DIALOGS_PIG_CAVE_23_4  → INGAME_CAVE_23  (strip speaker + linha)
    STR_INGAME_DIALOGS_FREE_SOLDIER_1 → INGAME_SOLDIER   (sem localização)
    STR_INGAME_NOTE_SINKA             → INGAME_NOTE_SINKA
    """
    if re.match(r"^STR_INGAME_NOTE_", offset, re.IGNORECASE):
        body = re.sub(r"^STR_INGAME_NOTE_", "", offset, flags=re.IGNORECASE)
        body = _strip_small(body)
        return f"INGAME_NOTE_{body.upper()}"
    stripped = re.sub(r"^STR_INGAME_DIALOGS_", "", offset, flags=re.IGNORECASE)
    stripped = _strip_small(stripped)          # strip número de linha
    parts = stripped.split("_")
    if len(parts) > 1:
        loc = "_".join(parts[1:])             # descarta primeiro segmento (speaker)
        loc = _strip_small(loc)               # strip número de encontro/sub-área
        return f"INGAME_{loc.upper()}" if loc else f"INGAME_{stripped.upper()}"
    return f"INGAME_{stripped.upper()}"


def _scene_side(offset: str) -> str:
    """SIDE_DIALOG_UPGRADE_BEDS_1 → SIDE_UPGRADE_BEDS"""
    stripped = re.sub(r"^SIDE_DIALOG_", "", offset, flags=re.IGNORECASE)
    stripped = _TRAILING_NUM_RE.sub("", stripped)
    return f"SIDE_{stripped}"


_SCENE_FN: dict[str, object] = {
    "texts_DIALOGS":        _scene_dialogs,
    "texts_INGAME_DIALOGS": _scene_ingame,
    "texts_SIDE_DIALOGS":   _scene_side,
}


def _scene_of(row: dict) -> str:
    fn = _SCENE_FN.get(row["table"])
    if fn:
        return fn(row["offset"])
    return row["offset"].upper()


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def split(project_root: Path) -> dict[str, list[str]]:
    """Lê dialogs.csv, agrupa por cena, cria artifacts/scenes/<cena>/."""
    src = project_root / "artifacts" / "dialogs.csv"
    if not src.is_file():
        raise FileNotFoundError(f"dialogs.csv nao encontrado: {src}")

    scenes: dict[str, list[dict]] = defaultdict(list)
    with src.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            scenes[_scene_of(row)].append(row)

    scenes_dir = project_root / "artifacts" / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)

    scene_index: dict[str, list[str]] = {}
    for scene, rows in sorted(scenes.items()):
        scene_dir = scenes_dir / scene
        scene_dir.mkdir(exist_ok=True)

        # dialogs.csv — formato que context_pack espera
        dlg_path = scene_dir / "dialogs.csv"
        with dlg_path.open("w", encoding="utf-8", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["offset", "text_en", "byte_budget"])
            for r in rows:
                budget = len(r["text_en"].encode("utf-8"))
                wr.writerow([r["offset"], r["text_en"], budget])

        # pack.json — metadados extras para scripts auxiliares
        pack = {
            "scene": scene,
            "source_rows": [
                {
                    "offset":  r["offset"],
                    "text_en": r["text_en"],
                    "speaker": r["speaker"],
                    "table":   r["table"],
                }
                for r in rows
            ],
            "tm_exact":    [],
            "tm_semantic": [],
            "kb":          [],
        }
        (scene_dir / "pack.json").write_text(
            json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        scene_index[scene] = [r["offset"] for r in rows]

    index_path = project_root / "artifacts" / "scenes_index.json"
    index_path.write_text(
        json.dumps(scene_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    by_size = sorted(scene_index.items(), key=lambda x: -len(x[1]))
    print(f"Cenas criadas: {len(scenes)}")
    print("Top 15 cenas por tamanho:")
    for scene, offsets in by_size[:15]:
        print(f"  {scene}: {len(offsets)} linhas")
    print(f"Menor cena: {by_size[-1][0]} ({len(by_size[-1][1])} linha)")
    return dict(scene_index)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    split(root)


if __name__ == "__main__":
    main()
