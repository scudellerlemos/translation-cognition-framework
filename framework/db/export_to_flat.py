"""export_to_flat.py — Inverso do migrate: gera os flats de intercâmbio A PARTIR do DB.

Fase 6 (cutover, parte 6a): com o DB como fonte de verdade, os arquivos que vivem na borda do
sistema continuam existindo — mas DERIVADOS do banco, não autoritativos:

  approved_translations.csv  (offset,text_target)  → consumido pelo conector na reinserção (s08)
  translation_memory.jsonl   (1 linha/fala)        → índice de TM p/ inspeção e modo flat

NÃO faz parte daqui a inversão dos PRODUTORES (gravar DB-first, 6b) — essa exige run vivo e fica
deferida. Aqui só provamos que o DB regenera o que o conector precisa, sem perda (round-trip
DB→flat→DB idêntico é o oráculo, em test_export.py).

Uso:
  python export_to_flat.py <db_path> <project_id> <out_dir>
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
for _p in (_HERE, _RUNTIME):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from store import Store  # noqa: E402
from text_ids import tm_key as _src_key  # noqa: E402  (fonte única da chave de TM)


def export_approved(db: Store, project_id: str, out_csv: Path) -> int:
    """approved_translations.csv (offset,text_target) das traduções APROVADAS, ordenado.
    É o arquivo que o conector (reinsert.py) aplica no binário — a borda determinística."""
    rows = db.get_translations(project_id, approved_only=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["offset", "text_target"])
        w.writeheader()
        for r in rows:
            w.writerow({"offset": r.get("offset", ""), "text_target": r.get("target", "")})
    return len(rows)


def export_tm(db: Store, project_id: str, out_jsonl: Path) -> int:
    """translation_memory.jsonl (1 linha/fala) — schema do state_index.build_tm (sem
    doctrine_version, que é metadado de auditoria não persistido no DB)."""
    rows = db.get_translations(project_id, approved_only=False)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for r in rows:
        src = r.get("source", "")
        lines.append(json.dumps({
            "scene": r.get("scene_id", ""),
            "offset": r.get("offset", ""),
            "speaker": r.get("speaker", ""),
            "source": src,
            "target": r.get("target", ""),
            "src_key": _src_key(src),
        }, ensure_ascii=False, sort_keys=True))
    out_jsonl.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def export(db_path: Path, project_id: str, out_dir: Path) -> dict:
    out_dir = Path(out_dir)
    with Store(db_path) as db:
        approved = export_approved(db, project_id, out_dir / "approved_translations.csv")
        tm = export_tm(db, project_id, out_dir / "translation_memory.jsonl")
    return {"project_id": project_id, "approved": approved, "tm": tm, "out_dir": str(out_dir)}


def main():
    ap = argparse.ArgumentParser(description="Exporta os flats de intercâmbio a partir do DB (Fase 6).")
    ap.add_argument("db_path")
    ap.add_argument("project_id")
    ap.add_argument("out_dir", help="Diretório de saída (ex.: projects/<x>/artifacts)")
    a = ap.parse_args()
    result = export(Path(a.db_path), a.project_id, Path(a.out_dir))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
