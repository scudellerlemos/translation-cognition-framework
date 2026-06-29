"""store.py — Interface tipada sobre o banco SQLite do framework.

Substitui state_index.py (flat files → SQLite). Fonte única de verdade
para TM, glossário, voice cards, entidades e ledger de jobs.

Uso:
    db = Store("projects/bof4_software/bof4_software.db")
    db.upsert_translation(project_id="bof4", scene_id="AREAD001", offset="X:0:1",
                          source="Hello", target="Olá", speaker="Ryu")
    hits = db.search_tm_exact("Hello", project_id="bof4")
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

_SCHEMA = Path(__file__).with_name("schema.sql")


class Store:
    """Interface sobre o banco SQLite. Thread-safe via WAL + check_same_thread=False."""

    def __init__(self, db_path: str | Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._con = sqlite3.connect(str(self.path), check_same_thread=False)
        self._con.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        sql = _SCHEMA.read_text(encoding="utf-8")
        self._con.executescript(sql)
        self._con.commit()

    def close(self):
        self._con.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    # ── Projetos ────────────────────────────────────────────────────────────

    def upsert_project(self, project_id: str, title: str,
                       source_lang: str = "en", target_lang: str = "pt-BR",
                       media_type: str = "game"):
        self._con.execute(
            """INSERT INTO projects(id, title, source_lang, target_lang, media_type, created_at)
               VALUES(?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET title=excluded.title""",
            (project_id, title, source_lang, target_lang, media_type, time.time()),
        )
        self._con.commit()

    # ── Cenas ────────────────────────────────────────────────────────────────

    def upsert_scene(self, project_id: str, scene_id: str, status: str,
                     n_lines: int = None, n_high: int = None, verified: bool = False,
                     cost_usd: float = 0.0, backend: str = None, model_id: str = None):
        now = time.time()
        self._con.execute(
            """INSERT INTO scenes(id, project_id, status, n_lines, n_high, verified,
                                  cost_usd, backend, model_id, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id, project_id) DO UPDATE SET
                   status=excluded.status, n_lines=COALESCE(excluded.n_lines, n_lines),
                   n_high=COALESCE(excluded.n_high, n_high),
                   verified=excluded.verified, cost_usd=excluded.cost_usd,
                   backend=excluded.backend, model_id=excluded.model_id,
                   updated_at=excluded.updated_at""",
            (scene_id, project_id, status, n_lines, n_high, int(verified),
             cost_usd, backend, model_id, now, now),
        )
        self._con.commit()

    def get_scenes(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM scenes WHERE project_id=? ORDER BY id", (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Traduções (TM) ───────────────────────────────────────────────────────

    def upsert_translation(self, project_id: str, scene_id: str, offset: str,
                           source: str, target: str = None, speaker: str = None,
                           tone_register: str = None, intent: str = None,
                           risk_level: str = "low", risk_notes: str = "",
                           approved: bool = False, backend: str = None,
                           model_id: str = None):
        self._con.execute(
            """INSERT INTO translations(project_id, scene_id, offset, source, target,
                   speaker, tone_register, intent, risk_level, risk_notes,
                   approved, backend, model_id, created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, scene_id, offset) DO UPDATE SET
                   target=excluded.target, speaker=excluded.speaker,
                   tone_register=excluded.tone_register, intent=excluded.intent,
                   risk_level=excluded.risk_level, risk_notes=excluded.risk_notes,
                   approved=excluded.approved, backend=excluded.backend,
                   model_id=excluded.model_id""",
            (project_id, scene_id, offset, source, target, speaker, tone_register,
             intent, risk_level, risk_notes, int(approved), backend, model_id, time.time()),
        )
        self._con.commit()

    def search_tm_exact(self, source: str, project_id: str,
                        approved_only: bool = True) -> list[dict]:
        """Busca exata na TM por texto fonte. Retorna lista de hits."""
        q = (
             "SELECT * FROM translations WHERE project_id=? AND source=?"  # nosec B608 - fragmento literal por bool; valores parametrizados
             + (" AND approved=1" if approved_only else "")
             + " ORDER BY approved DESC, created_at DESC LIMIT 10")
        rows = self._con.execute(q, (project_id, source)).fetchall()
        return [dict(r) for r in rows]

    def search_tm_semantic(self, source: str, project_id: str, k: int = 5) -> list[dict]:
        """Busca semântica na TM via embeddings (requer embedder.py + sqlite-vec).

        Fallback para busca exata se embeddings não disponíveis.
        """
        try:
            from embedder import Embedder  # type: ignore
            emb = Embedder()
            return emb.search(self._con, source, project_id=project_id, k=k)
        except ImportError:
            return self.search_tm_exact(source, project_id)

    def get_tm_approved(self, project_id: str, limit: int = 5000) -> list[dict]:
        rows = self._con.execute(
            """SELECT scene_id, offset, source, target, speaker
               FROM translations WHERE project_id=? AND approved=1
               ORDER BY created_at DESC LIMIT ?""",
            (project_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Glossário ────────────────────────────────────────────────────────────

    def upsert_glossary(self, project_id: str, term: str, translation: str,
                        handling_rule: str = None, domain: str = None, notes: str = None):
        self._con.execute(
            """INSERT INTO glossary(project_id, term, translation, handling_rule,
                                    domain, notes, updated_at)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(project_id, term) DO UPDATE SET
                   translation=excluded.translation,
                   handling_rule=COALESCE(excluded.handling_rule, handling_rule),
                   domain=COALESCE(excluded.domain, domain),
                   notes=COALESCE(excluded.notes, notes),
                   updated_at=excluded.updated_at""",
            (project_id, term, translation, handling_rule, domain, notes, time.time()),
        )
        self._con.commit()

    def get_glossary(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM glossary WHERE project_id=? ORDER BY term", (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Entidades ────────────────────────────────────────────────────────────

    def upsert_entity(self, project_id: str, name: str, canonical_pt: str = None,
                      entity_type: str = None, first_scene: str = None,
                      spoiler_reveal_scene: str = None, notes: str = None):
        self._con.execute(
            """INSERT INTO entities(project_id, name, canonical_pt, entity_type,
                                    first_scene, spoiler_reveal_scene, notes)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(project_id, name) DO UPDATE SET
                   canonical_pt=COALESCE(excluded.canonical_pt, canonical_pt),
                   entity_type=COALESCE(excluded.entity_type, entity_type),
                   spoiler_reveal_scene=COALESCE(excluded.spoiler_reveal_scene,
                                                  spoiler_reveal_scene)""",
            (project_id, name, canonical_pt, entity_type, first_scene,
             spoiler_reveal_scene, notes),
        )
        self._con.commit()

    def get_entities(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM entities WHERE project_id=? ORDER BY name", (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Voice cards ──────────────────────────────────────────────────────────

    def upsert_voice_card(self, project_id: str, speaker: str,
                          register: str = None, quirks: list = None,
                          example_src: list = None, example_tgt: list = None,
                          criticality: str = "medium"):
        self._con.execute(
            """INSERT INTO voice_cards(project_id, speaker, register, quirks,
                                       example_src, example_tgt, criticality)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(project_id, speaker) DO UPDATE SET
                   register=COALESCE(excluded.register, register),
                   quirks=COALESCE(excluded.quirks, quirks),
                   example_src=COALESCE(excluded.example_src, example_src),
                   example_tgt=COALESCE(excluded.example_tgt, example_tgt),
                   criticality=excluded.criticality""",
            (project_id, speaker, register,
             json.dumps(quirks or [], ensure_ascii=False),
             json.dumps(example_src or [], ensure_ascii=False),
             json.dumps(example_tgt or [], ensure_ascii=False),
             criticality),
        )
        self._con.commit()

    def get_voice_cards(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM voice_cards WHERE project_id=? ORDER BY speaker", (project_id,)
        ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["quirks"] = json.loads(d.get("quirks") or "[]")
            d["example_src"] = json.loads(d.get("example_src") or "[]")
            d["example_tgt"] = json.loads(d.get("example_tgt") or "[]")
            result.append(d)
        return result

    # ── Jobs (ledger) ─────────────────────────────────────────────────────────

    def log_job(self, project_id: str, kind: str, scene_id: str = None,
                model_id: str = None, backend: str = None,
                tokens_in: int = 0, tokens_out: int = 0,
                cost_usd: float = 0.0, batch: bool = False):
        self._con.execute(
            """INSERT INTO jobs(project_id, scene_id, kind, model_id, backend,
                                tokens_in, tokens_out, cost_usd, batch, created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (project_id, scene_id, kind, model_id, backend,
             tokens_in, tokens_out, cost_usd, int(batch), time.time()),
        )
        self._con.commit()

    def get_cost_summary(self, project_id: str) -> dict:
        row = self._con.execute(
            """SELECT SUM(cost_usd) as total, SUM(tokens_in) as tin,
                      SUM(tokens_out) as tout, COUNT(*) as n_calls
               FROM jobs WHERE project_id=?""",
            (project_id,),
        ).fetchone()
        return dict(row) if row else {"total": 0, "tin": 0, "tout": 0, "n_calls": 0}

    # ── Stats ────────────────────────────────────────────────────────────────

    def summary(self, project_id: str) -> dict:
        scenes = self.get_scenes(project_id)
        cost = self.get_cost_summary(project_id)
        n_tm = self._con.execute(
            "SELECT COUNT(*) FROM translations WHERE project_id=? AND approved=1",
            (project_id,),
        ).fetchone()[0]
        return {
            "project_id": project_id,
            "scenes": len(scenes),
            "verified": sum(1 for s in scenes if s["verified"]),
            "tm_approved": n_tm,
            "cost_usd": round(cost["total"] or 0, 4),
            "api_calls": cost["n_calls"],
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python store.py <db_path>")
        sys.exit(1)
    with Store(sys.argv[1]) as db:
        print(json.dumps(db.summary(sys.argv[2] if len(sys.argv) > 2 else ""), indent=2))
