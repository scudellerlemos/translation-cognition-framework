"""migrate_from_flat.py — Importa dados do BoF4 (flat files) para SQLite.

Lê os artefatos existentes do BoF4:
  artifacts/scenes/*/approved_*.csv → translations (approved=1)
  artifacts/glossary.csv            → glossary
  state/voice_cards.json            → voice_cards (se existir)
  artifacts/entities.csv            → entities
  artifacts/api_ledger.jsonl        → jobs
  artifacts/run_state.json          → scenes (status)

Grava em: <dest_db> (cria se não existir)

Uso:
  python migrate_from_flat.py <bof4_root> <dest_db> [--project-id bof4]
  python migrate_from_flat.py projects/breath_of_fire_4 projects/bof4_software/bof4.db
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))
sys.path.insert(0, str(_HERE))

from store import Store  # noqa: E402


def _migrate_scenes(db: Store, project_id: str, root: Path) -> int:
    rs_path = root / "artifacts" / "run_state.json"
    if not rs_path.is_file():
        return 0
    state = json.loads(rs_path.read_text(encoding="utf-8"))
    n = 0
    for scene_id, data in state.get("scenes", {}).items():
        db.upsert_scene(
            project_id=project_id,
            scene_id=scene_id,
            status=data.get("status", "pending"),
            n_lines=data.get("n_lines"),
            n_high=data.get("high"),
            verified=data.get("verified", False),
        )
        n += 1
    return n


def _migrate_translations(db: Store, project_id: str, root: Path) -> int:
    scenes_dir = root / "artifacts" / "scenes"
    if not scenes_dir.is_dir():
        return 0
    n = 0
    for scene_dir in sorted(scenes_dir.iterdir()):
        if not scene_dir.is_dir():
            continue
        scene_id = scene_dir.name
        for csv_path in sorted(scene_dir.glob("approved_*.csv")):
            with csv_path.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    db.upsert_translation(
                        project_id=project_id,
                        scene_id=scene_id,
                        offset=row.get("offset", ""),
                        source=row.get("source", row.get("text_en", "")),
                        target=row.get("target", row.get("text_pt", "")),
                        speaker=row.get("speaker", ""),
                        tone_register=row.get("tone_register", ""),
                        intent=row.get("intent", ""),
                        risk_level=row.get("risk_level", "low"),
                        risk_notes=row.get("risk_notes", ""),
                        approved=True,
                    )
                    n += 1
    return n


def _migrate_glossary(db: Store, project_id: str, root: Path) -> int:
    g_path = root / "artifacts" / "glossary.csv"
    if not g_path.is_file():
        return 0
    n = 0
    with g_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            term = row.get("term") or row.get("source_term", "")
            translation = row.get("translation") or row.get("target_term", "")
            if not term or not translation:
                continue
            db.upsert_glossary(
                project_id=project_id,
                term=term,
                translation=translation,
                handling_rule=row.get("handling_rule"),
                domain=row.get("domain"),
                notes=row.get("notes"),
            )
            n += 1
    return n


def _migrate_entities(db: Store, project_id: str, root: Path) -> int:
    e_path = root / "artifacts" / "entities.csv"
    if not e_path.is_file():
        return 0
    n = 0
    with e_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name") or row.get("entity", "")
            if not name:
                continue
            db.upsert_entity(
                project_id=project_id,
                name=name,
                canonical_pt=row.get("canonical_pt") or row.get("translation"),
                entity_type=row.get("type") or row.get("entity_type"),
                first_scene=row.get("first_scene"),
                spoiler_reveal_scene=row.get("spoiler_reveal_scene"),
                notes=row.get("notes"),
            )
            n += 1
    return n


def _migrate_voice_cards(db: Store, project_id: str, root: Path) -> int:
    # Tenta state/voice_cards.json primeiro, depois artifacts/tone_analysis.md (heurístico)
    vc_path = root / "state" / "voice_cards.json"
    if not vc_path.is_file():
        vc_path = root / "artifacts" / "voice_cards.json"
    if not vc_path.is_file():
        return 0
    data = json.loads(vc_path.read_text(encoding="utf-8"))
    cards = data if isinstance(data, list) else data.get("cards", [])
    n = 0
    for card in cards:
        speaker = card.get("speaker") or card.get("name", "")
        if not speaker:
            continue
        db.upsert_voice_card(
            project_id=project_id,
            speaker=speaker,
            register=card.get("register"),
            quirks=card.get("quirks", []),
            example_src=card.get("example_src", card.get("examples_en", [])),
            example_tgt=card.get("example_tgt", card.get("examples_pt", [])),
            criticality=card.get("criticality", "medium"),
        )
        n += 1
    return n


def _migrate_jobs(db: Store, project_id: str, root: Path) -> int:
    ledger = root / "artifacts" / "api_ledger.jsonl"
    if not ledger.is_file():
        return 0
    n = 0
    for line in ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        u = rec.get("usage", {})
        db.log_job(
            project_id=project_id,
            scene_id=rec.get("scene"),
            kind=rec.get("kind", "translate"),
            model_id=rec.get("model"),
            backend="api",
            tokens_in=u.get("in", 0) + u.get("cache_read", 0),
            tokens_out=u.get("out", 0),
            cost_usd=rec.get("cost_usd", 0.0),
            batch=rec.get("batch", False),
        )
        n += 1
    return n


def migrate(bof4_root: Path, dest_db: Path, project_id: str = "bof4") -> dict:
    with Store(dest_db) as db:
        db.upsert_project(
            project_id=project_id,
            title="Breath of Fire IV",
            source_lang="en",
            target_lang="pt-BR",
            media_type="game",
        )
        scenes = _migrate_scenes(db, project_id, bof4_root)
        translations = _migrate_translations(db, project_id, bof4_root)
        glossary = _migrate_glossary(db, project_id, bof4_root)
        entities = _migrate_entities(db, project_id, bof4_root)
        voice_cards = _migrate_voice_cards(db, project_id, bof4_root)
        jobs = _migrate_jobs(db, project_id, bof4_root)
        return {
            "project_id": project_id,
            "scenes": scenes,
            "translations": translations,
            "glossary": glossary,
            "entities": entities,
            "voice_cards": voice_cards,
            "jobs": jobs,
            "db": str(dest_db),
        }


def main():
    ap = argparse.ArgumentParser(description="Migra flat files do BoF4 para SQLite.")
    ap.add_argument("bof4_root", help="Diretório raiz do projeto BoF4")
    ap.add_argument("dest_db", help="Caminho do banco SQLite de destino")
    ap.add_argument("--project-id", default="bof4", help="ID do projeto no banco (default: bof4)")
    a = ap.parse_args()
    result = migrate(Path(a.bof4_root), Path(a.dest_db), a.project_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
