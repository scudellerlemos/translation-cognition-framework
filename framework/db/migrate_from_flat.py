"""migrate_from_flat.py — Importa dados do BoF4 (flat files) para SQLite.

Lê os artefatos existentes do BoF4:
  artifacts/scenes/*/approved_*.csv → translations (approved=1)
  artifacts/glossary.csv            → glossary
  state/voice_cards.json            → voice_cards (se existir)
  artifacts/entities.csv            → entities
  artifacts/api_ledger.jsonl        → jobs
  artifacts/run_state.json          → scenes (status)
  artifacts/metrics.jsonl           → metrics (observabilidade)
  artifacts/warnings.jsonl          → warnings
  artifacts/qa_effectiveness.jsonl  → qa_effectiveness

Grava em: <dest_db> (cria se não existir)

Uso:
  python migrate_from_flat.py <bof4_root> <dest_db> [--project-id bof4]
  python migrate_from_flat.py projects/breath_of_fire_4 projects/translation_software/translation_software.db
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))
sys.path.insert(0, str(_HERE))

from store import Store  # noqa: E402


def _sid(name: str) -> str:
    """scene_id canônico — igual a context_pack.scene_id_of (tira o prefixo 'ch_'). Usado em
    TODA migração p/ chavear scene_id de forma consistente entre as tabelas (senão projetos
    com prefixo 'ch_' divergiriam entre scene_lines e translations/back_translations/scenes)."""
    return name[3:] if name.startswith("ch_") else name


def _migrate_scenes(db: Store, project_id: str, root: Path) -> int:
    rs_path = root / "artifacts" / "run_state.json"
    if not rs_path.is_file():
        return 0
    state = json.loads(rs_path.read_text(encoding="utf-8"))
    n = 0
    for scene_id, data in state.get("scenes", {}).items():
        db.upsert_scene(
            project_id=project_id,
            scene_id=_sid(scene_id),
            status=data.get("status", "pending"),
            n_lines=data.get("n_lines"),
            n_high=data.get("high"),
            verified=data.get("verified", False),
        )
        n += 1
    return n


def _migrate_scene_lines(db: Store, project_id: str, root: Path) -> int:
    scenes_dir = root / "artifacts" / "scenes"
    if not scenes_dir.is_dir():
        return 0
    n = 0
    for scene_dir in sorted(scenes_dir.iterdir()):
        if not scene_dir.is_dir():
            continue
        dcsv = scene_dir / "dialogs.csv"
        if not dcsv.is_file():
            continue
        sid = _sid(scene_dir.name)
        lines = []
        with dcsv.open(encoding="utf-8", newline="") as f:
            rdr = csv.DictReader(f)
            cols = rdr.fieldnames or []
            textcol = "text_source" if "text_source" in cols else "text_en"
            for r in rdr:
                bb = (r.get("byte_budget") or "").strip()
                lines.append({
                    "offset": r.get("offset", ""),
                    "source": r.get(textcol, ""),
                    "byte_budget": int(bb) if bb.lstrip("-").isdigit() else None,
                })
        if lines:
            db.upsert_scene_lines(project_id, sid, lines)
            n += len(lines)
    return n


def _migrate_translations(db: Store, project_id: str, root: Path) -> tuple[int, int]:
    """TM = traduções APROVADAS, completas e fiéis. `target` vem do approved_*.csv (a forma
    FINAL que o jogo mostra — preserva os segmentos após [02] e os códigos de controle);
    `source` (EN) vem do dialogs.csv; speaker/metadata do translation_plan. NÃO usa
    base_translation/t: são rascunhos legíveis porém INCOMPLETOS em linhas multi-segmento
    (largam o trecho após [02], ex.: "Certo, Poko?"). Retorna (total, aprovadas)."""
    scenes_dir = root / "artifacts" / "scenes"
    if not scenes_dir.is_dir():
        return 0, 0
    total = approved_n = 0
    for scene_dir in sorted(scenes_dir.iterdir()):
        if not scene_dir.is_dir():
            continue
        scene_id = _sid(scene_dir.name)
        # source (EN) por offset — do dialogs.csv (extração completa da cena)
        src_by = {}
        dcsv = scene_dir / "dialogs.csv"
        if dcsv.is_file():
            with dcsv.open(encoding="utf-8", newline="") as f:
                rdr = csv.DictReader(f)
                cols = rdr.fieldnames or []
                tc = "text_source" if "text_source" in cols else "text_en"
                for r in rdr:
                    if r.get("offset"):
                        src_by[r["offset"]] = r.get(tc, "")
        # metadata (speaker/tom/risco) por offset — do translation_plan
        meta_by = {}
        for plan_path in sorted(scene_dir.glob("translation_plan_*.json")):
            try:
                data = json.loads(plan_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            lines = data.get("lines", [])
            if isinstance(lines, dict):
                lines = [{"offset": k, **v} for k, v in lines.items()]
            for ln in lines:
                if ln.get("offset"):
                    meta_by[ln["offset"]] = ln
        # target (completo/fiel) — do approved_*.csv
        for csv_path in sorted(scene_dir.glob("approved_*.csv")):
            with csv_path.open(encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    off = row.get("offset", "")
                    tgt = row.get("text_target", "")
                    if not off or not tgt:
                        continue
                    m = meta_by.get(off, {})
                    db.upsert_translation(
                        project_id=project_id,
                        scene_id=scene_id,
                        offset=off,
                        source=src_by.get(off, ""),
                        target=tgt,
                        speaker=m.get("speaker", ""),
                        tone_register=m.get("tone_register", ""),
                        intent=m.get("intent", ""),
                        risk_level=m.get("risk_level", "low"),
                        risk_notes=m.get("risk_notes", ""),
                        approved=True,
                    )
                    total += 1
                    approved_n += 1
    return total, approved_n


_KB_REVEAL_RX = re.compile(r"<!--\s*reveal:\s*([^\s>]+)\s*-->", re.IGNORECASE)


def _migrate_kb(db: Store, project_id: str, root: Path) -> int:
    """universe_knowledge_base.md → tabela kb, uma entrada por seção (## / ###). Lê o
    reveal explícito da seção via `<!-- reveal: <scene>|beyond_frontier|safe -->` no cabeçalho;
    sem tag → reveal=NULL (default-deny no context_pack: não injeta)."""
    p = root / "artifacts" / "universe_knowledge_base.md"
    if not p.is_file():
        return 0
    entries: list[dict] = []
    section: str | None = None
    reveal: str | None = None
    buf: list[str] = []

    def _flush():
        if section and "\n".join(buf).strip():
            entries.append({"section": section, "content": "\n".join(buf).strip(), "reveal": reveal})

    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith(("## ", "### ")):
            _flush()
            m = _KB_REVEAL_RX.search(line)
            reveal = m.group(1) if m else None
            section = _KB_REVEAL_RX.sub("", line).lstrip("# ").strip()
            buf = []
        elif section is not None:
            buf.append(line)
    _flush()
    if entries:
        db.upsert_kb(project_id, entries)
    return len(entries)


def _migrate_back_translations(db: Store, project_id: str, root: Path) -> int:
    scenes_dir = root / "artifacts" / "scenes"
    if not scenes_dir.is_dir():
        return 0
    n = 0
    for scene_dir in sorted(scenes_dir.iterdir()):
        if not scene_dir.is_dir():
            continue
        scene_id = _sid(scene_dir.name)
        for bt_path in sorted(scene_dir.glob("back_translation_*.json")):
            try:
                data = json.loads(bt_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            entries = [e for e in data.get("entries", []) if e.get("offset")]
            if entries:
                db.upsert_back_translations(project_id, scene_id, entries)
                n += len(entries)
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
            translation = (row.get("translation") or row.get("target_translation")
                           or row.get("target_term", ""))
            if not term or not translation:
                continue
            db.upsert_glossary(
                project_id=project_id,
                term=term,
                translation=translation,
                handling_rule=row.get("handling_rule"),
                domain=row.get("domain") or row.get("category"),
                category=row.get("category"),
                aliases=row.get("aliases"),
                spoiler_level=row.get("spoiler_level"),
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
            name = row.get("name") or row.get("entity") or row.get("canonical_name", "")
            if not name:
                continue
            db.upsert_entity(
                project_id=project_id,
                name=name,
                canonical_pt=row.get("canonical_pt") or row.get("translation"),
                entity_type=row.get("type") or row.get("entity_type") or row.get("category"),
                first_scene=row.get("first_scene"),
                spoiler_reveal_scene=row.get("spoiler_reveal_scene"),
                notes=row.get("notes"),
            )
            n += 1
    return n


def _migrate_voice_cards(db: Store, project_id: str, root: Path) -> int:
    # O context_pack lê voice_cards.json de artifacts/state/ (paths.state_dir); aceita também
    # os locais legados. Formato canônico: {nome: {aliases, criticality, lines}}.
    for cand in (root / "artifacts" / "state" / "voice_cards.json",
                 root / "state" / "voice_cards.json",
                 root / "artifacts" / "voice_cards.json"):
        if cand.is_file():
            vc_path = cand
            break
    else:
        return 0
    data = json.loads(vc_path.read_text(encoding="utf-8"))
    n = 0
    # Formato dict {nome: {...}} (context_pack) — chave é o falante.
    if isinstance(data, dict) and "cards" not in data:
        for name, card in data.items():
            db.upsert_voice_card(
                project_id=project_id,
                speaker=name,
                aliases=card.get("aliases", []),
                lines=card.get("lines", []),
                register=card.get("register"),
                quirks=card.get("quirks", []),
                example_src=card.get("example_src", card.get("examples_en", [])),
                example_tgt=card.get("example_tgt", card.get("examples_pt", [])),
                criticality=card.get("criticality", "medium"),
            )
            n += 1
        return n
    # Formato legado: lista ou {"cards": [...]}.
    cards = data if isinstance(data, list) else data.get("cards", [])
    for card in cards:
        speaker = card.get("speaker") or card.get("name", "")
        if not speaker:
            continue
        db.upsert_voice_card(
            project_id=project_id,
            speaker=speaker,
            aliases=card.get("aliases", []),
            lines=card.get("lines", []),
            register=card.get("register"),
            quirks=card.get("quirks", []),
            example_src=card.get("example_src", card.get("examples_en", [])),
            example_tgt=card.get("example_tgt", card.get("examples_pt", [])),
            criticality=card.get("criticality", "medium"),
        )
        n += 1
    return n


def _migrate_decisions(db: Store, project_id: str, root: Path) -> int:
    p = root / "artifacts" / "state" / "decision_index.json"
    if not p.is_file():
        return 0
    data = json.loads(p.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("decisions", [])
    n = 0
    for d in items:
        title = d.get("title")
        if not title:
            continue
        db.upsert_decision(
            project_id=project_id,
            title=title,
            summary=d.get("summary"),
            universal=bool(d.get("universal", False)),
            tags=d.get("tags", []),
        )
        n += 1
    return n


def _migrate_spoiler(db: Store, project_id: str, root: Path) -> int:
    p = root / "artifacts" / "spoiler_ledger.json"
    if not p.is_file():
        return 0
    data = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for e in data.get("entries", []):
        entity = e.get("entity")
        if not entity:
            continue
        db.upsert_spoiler_entry(
            project_id=project_id,
            entity=entity,
            fact=e.get("fact"),
            spoiler_level=e.get("spoiler_level"),
            reveal=e.get("reveal"),
            scenes=e.get("scenes", []),
            triggers=e.get("triggers", []),
            pre_reveal=e.get("pre_reveal"),
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


def _read_jsonl(path: Path) -> list[dict]:
    """Lê um .jsonl tolerante a linhas em branco/corrompidas (mesma postura do ledger)."""
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _migrate_metrics(db: Store, project_id: str, root: Path) -> int:
    """metrics.jsonl → tabela metrics. Snapshot 1-por-cena; escalares em colunas e o
    registro completo (translate/back aninhados) preservado em `raw` (JSON)."""
    recs = _read_jsonl(root / "artifacts" / "metrics.jsonl")
    rows = []
    for r in recs:
        scene = r.get("scene")
        if not scene:
            continue
        rows.append({
            "scene_id": _sid(scene),
            "n_lines": r.get("n_lines"),
            "n_high": r.get("n_high"),
            "verified": r.get("verified", False),
            "reused": r.get("reused"),
            "back_pass_rate": r.get("back_pass_rate"),
            "cost_usd_last": r.get("cost_usd_last"),
            "cost_usd": r.get("cost_usd"),
            "raw": json.dumps(r, ensure_ascii=False),
        })
    if rows:
        db.upsert_metrics(project_id, rows)
    return len(rows)


def _migrate_warnings(db: Store, project_id: str, root: Path) -> int:
    """warnings.jsonl → tabela warnings (append-log; lista de strings em JSON)."""
    recs = _read_jsonl(root / "artifacts" / "warnings.jsonl")
    rows = [{"t": r.get("t"), "source": r.get("source"), "warnings": r.get("warnings", [])}
            for r in recs if r.get("t") is not None]
    if rows:
        db.upsert_warnings(project_id, rows)
    return len(rows)


def _migrate_qa_effectiveness(db: Store, project_id: str, root: Path) -> int:
    """qa_effectiveness.jsonl → tabela qa_effectiveness (append-log do QA humano)."""
    recs = _read_jsonl(root / "artifacts" / "qa_effectiveness.jsonl")
    rows = [r for r in recs if r.get("t") is not None]
    if rows:
        db.upsert_qa_effectiveness(project_id, rows)
    return len(rows)


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
        scene_lines = _migrate_scene_lines(db, project_id, bof4_root)
        translations, approved = _migrate_translations(db, project_id, bof4_root)
        glossary = _migrate_glossary(db, project_id, bof4_root)
        entities = _migrate_entities(db, project_id, bof4_root)
        voice_cards = _migrate_voice_cards(db, project_id, bof4_root)
        decisions = _migrate_decisions(db, project_id, bof4_root)
        spoiler = _migrate_spoiler(db, project_id, bof4_root)
        back_translations = _migrate_back_translations(db, project_id, bof4_root)
        kb = _migrate_kb(db, project_id, bof4_root)
        jobs = _migrate_jobs(db, project_id, bof4_root)
        metrics = _migrate_metrics(db, project_id, bof4_root)
        warnings = _migrate_warnings(db, project_id, bof4_root)
        qa_effectiveness = _migrate_qa_effectiveness(db, project_id, bof4_root)
        return {
            "project_id": project_id,
            "scenes": scenes,
            "scene_lines": scene_lines,
            "translations": translations,
            "approved": approved,
            "glossary": glossary,
            "entities": entities,
            "voice_cards": voice_cards,
            "decisions": decisions,
            "spoiler": spoiler,
            "back_translations": back_translations,
            "kb": kb,
            "jobs": jobs,
            "metrics": metrics,
            "warnings": warnings,
            "qa_effectiveness": qa_effectiveness,
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
