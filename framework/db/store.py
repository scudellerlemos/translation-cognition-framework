"""store.py — Interface tipada sobre o banco SQLite do framework.

Substitui state_index.py (flat files → SQLite). Fonte única de verdade
para TM, glossário, voice cards, entidades e ledger de jobs.

Uso:
    db = Store("projects/translation_software/translation_software.db")
    db.upsert_translation(project_id="bof4", scene_id="AREAD001", offset="X:0:1",
                          source="Hello", target="Olá", speaker="Ryu")
    hits = db.search_tm_exact("Hello", project_id="bof4")
"""
from __future__ import annotations

import json
import re
import sqlite3
import time
from pathlib import Path

_SCHEMA = Path(__file__).with_name("schema.sql")

_CODE_RX = re.compile(r"\[[0-9A-Fa-f]{2}\]")


def strip_codes(text: str) -> str:
    """Forma LIMPA do texto: remove os códigos de controle do jogo (`[XX]`) e normaliza
    espaços. Para LEITURA e EMBEDDING semântico — o `target` FIEL (com códigos) continua
    intacto no banco (round-trip/conector dependem dele). Genérico (multi-game)."""
    if not text:
        return text or ""
    return re.sub(r"\s+", " ", _CODE_RX.sub(" ", text)).strip()


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
        self._migrate_schema()
        self._con.commit()

    def _migrate_schema(self):
        """#85: migrações ADITIVAS de coluna (ALTER TABLE) — CREATE TABLE IF NOT EXISTS não
        adiciona coluna nova a uma tabela já existente num banco criado antes dela existir."""
        cols = {r["name"] for r in self._con.execute("PRAGMA table_info(spoiler_entries)").fetchall()}
        if "forbidden_pre_reveal" not in cols:
            self._con.execute("ALTER TABLE spoiler_entries ADD COLUMN forbidden_pre_reveal TEXT")
        if "gender_quarantine" not in cols:
            self._con.execute("ALTER TABLE spoiler_entries ADD COLUMN gender_quarantine INTEGER DEFAULT 0")

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
                     n_lines: int | None = None, n_high: int | None = None, verified: bool = False,
                     cost_usd: float = 0.0, backend: str | None = None, model_id: str | None = None):
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
                           source: str, target: str | None = None, speaker: str | None = None,
                           tone_register: str | None = None, intent: str | None = None,
                           risk_level: str = "low", risk_notes: str = "",
                           approved: bool = False, backend: str | None = None,
                           model_id: str | None = None):
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

    def get_translations(self, project_id: str, approved_only: bool = True) -> list[dict]:
        """Traduções da TM (scene_id/offset/source/target/speaker), ordenadas — fonte da
        TM consumida pelo context_pack no modo DB. approved_only reflete a TM revisada."""
        if approved_only:
            rows = self._con.execute(
                "SELECT scene_id, offset, source, target, speaker FROM translations "
                "WHERE project_id=? AND approved=1 ORDER BY scene_id, offset",
                (project_id,),
            ).fetchall()
        else:
            rows = self._con.execute(
                "SELECT scene_id, offset, source, target, speaker FROM translations "
                "WHERE project_id=? ORDER BY scene_id, offset",
                (project_id,),
            ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            # forma limpa p/ leitura/semântica; o source/target fiel (com códigos) fica intacto
            d["source_clean"] = strip_codes(d.get("source") or "")
            d["target_clean"] = strip_codes(d.get("target") or "")
            out.append(d)
        return out

    # ── Linhas da cena (dialogs) ────────────────────────────────────────────────

    def upsert_scene_lines(self, project_id: str, scene_id: str, lines: list):
        """Insere/atualiza as linhas de uma cena em LOTE (1 commit) — dialogs.csv → DB."""
        self._con.executemany(
            """INSERT INTO scene_lines(project_id, scene_id, offset, source, byte_budget)
               VALUES(?,?,?,?,?)
               ON CONFLICT(project_id, scene_id, offset) DO UPDATE SET
                   source=excluded.source, byte_budget=excluded.byte_budget""",
            [(project_id, scene_id, ln.get("offset", ""), ln.get("source"),
              ln.get("byte_budget")) for ln in lines],
        )
        self._con.commit()

    def get_scene_lines(self, project_id: str, scene_id: str) -> list[dict]:
        """Linhas da cena na MESMA forma de context_pack.load_dialogs (offset/source/byte_budget)."""
        rows = self._con.execute(
            "SELECT offset, source, byte_budget FROM scene_lines "
            "WHERE project_id=? AND scene_id=? ORDER BY id",
            (project_id, scene_id),
        ).fetchall()
        return [{"offset": r["offset"], "source": r["source"],
                 "byte_budget": r["byte_budget"]} for r in rows]

    # ── Knowledge base (lore) ────────────────────────────────────────────────────

    def upsert_kb(self, project_id: str, entries: list):
        """Seções da KB em LOTE (1 commit). entries: [{section, content, reveal}]."""
        self._con.executemany(
            """INSERT INTO kb(project_id, section, content, reveal) VALUES(?,?,?,?)
               ON CONFLICT(project_id, section) DO UPDATE SET
                   content=excluded.content, reveal=excluded.reveal""",
            [(project_id, e.get("section", ""), e.get("content", ""), e.get("reveal"))
             for e in entries],
        )
        self._con.commit()

    def get_kb(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT section, content, reveal FROM kb WHERE project_id=? ORDER BY id",
            (project_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Back-translation ────────────────────────────────────────────────────────

    def upsert_back_translations(self, project_id: str, scene_id: str, entries: list):
        """Entradas de back-translation de uma cena em LOTE (1 commit)."""
        self._con.executemany(
            """INSERT INTO back_translations(project_id, scene_id, offset, back_en, verdict, note)
               VALUES(?,?,?,?,?,?)
               ON CONFLICT(project_id, scene_id, offset) DO UPDATE SET
                   back_en=excluded.back_en, verdict=excluded.verdict, note=excluded.note""",
            [(project_id, scene_id, e.get("offset", ""), e.get("back_en"),
              e.get("verdict"), e.get("note")) for e in entries],
        )
        self._con.commit()

    def get_back_translations(self, project_id: str, scene_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT offset, back_en, verdict, note FROM back_translations "
            "WHERE project_id=? AND scene_id=? ORDER BY id",
            (project_id, scene_id),
        ).fetchall()
        return [dict(r) for r in rows]

    def upsert_glossary(self, project_id: str, term: str, translation: str,
                        handling_rule: str | None = None, domain: str | None = None,
                        category: str | None = None, aliases: str | None = None,
                        spoiler_level: str | None = None, notes: str | None = None):
        self._con.execute(
            """INSERT INTO glossary(project_id, term, translation, handling_rule,
                                    domain, category, aliases, spoiler_level, notes, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, term) DO UPDATE SET
                   translation=excluded.translation,
                   handling_rule=COALESCE(excluded.handling_rule, handling_rule),
                   domain=COALESCE(excluded.domain, domain),
                   category=COALESCE(excluded.category, category),
                   aliases=COALESCE(excluded.aliases, aliases),
                   spoiler_level=COALESCE(excluded.spoiler_level, spoiler_level),
                   notes=COALESCE(excluded.notes, notes),
                   updated_at=excluded.updated_at""",
            (project_id, term, translation, handling_rule, domain, category,
             aliases, spoiler_level, notes, time.time()),
        )
        self._con.commit()

    def get_glossary(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM glossary WHERE project_id=? ORDER BY term", (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Entidades ────────────────────────────────────────────────────────────

    def upsert_entity(self, project_id: str, name: str, canonical_pt: str | None = None,
                      entity_type: str | None = None, first_scene: str | None = None,
                      spoiler_reveal_scene: str | None = None, notes: str | None = None):
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
                          register: str | None = None, quirks: list | None = None,
                          example_src: list | None = None, example_tgt: list | None = None,
                          criticality: str = "medium",
                          aliases: list | None = None, lines: list | None = None):
        self._con.execute(
            """INSERT INTO voice_cards(project_id, speaker, aliases, register, quirks,
                                       example_src, example_tgt, lines, criticality)
               VALUES(?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, speaker) DO UPDATE SET
                   aliases=COALESCE(excluded.aliases, aliases),
                   register=COALESCE(excluded.register, register),
                   quirks=COALESCE(excluded.quirks, quirks),
                   example_src=COALESCE(excluded.example_src, example_src),
                   example_tgt=COALESCE(excluded.example_tgt, example_tgt),
                   lines=COALESCE(excluded.lines, lines),
                   criticality=excluded.criticality""",
            (project_id, speaker,
             json.dumps(aliases or [], ensure_ascii=False),
             register,
             json.dumps(quirks or [], ensure_ascii=False),
             json.dumps(example_src or [], ensure_ascii=False),
             json.dumps(example_tgt or [], ensure_ascii=False),
             json.dumps(lines or [], ensure_ascii=False),
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
            d["aliases"] = json.loads(d.get("aliases") or "[]")
            d["quirks"] = json.loads(d.get("quirks") or "[]")
            d["example_src"] = json.loads(d.get("example_src") or "[]")
            d["example_tgt"] = json.loads(d.get("example_tgt") or "[]")
            d["lines"] = json.loads(d.get("lines") or "[]")
            result.append(d)
        return result

    # ── Decisões ───────────────────────────────────────────────────────────────

    def upsert_decision(self, project_id: str, title: str, summary: str | None = None,
                        universal: bool = False, tags: list | None = None):
        self._con.execute(
            """INSERT INTO decisions(project_id, title, summary, universal, tags)
               VALUES(?,?,?,?,?)
               ON CONFLICT(project_id, title) DO UPDATE SET
                   summary=COALESCE(excluded.summary, summary),
                   universal=excluded.universal,
                   tags=COALESCE(excluded.tags, tags)""",
            (project_id, title, summary, int(universal),
             json.dumps(tags or [], ensure_ascii=False)),
        )
        self._con.commit()

    def get_decisions(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM decisions WHERE project_id=? ORDER BY id", (project_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["universal"] = bool(d.get("universal"))
            d["tags"] = json.loads(d.get("tags") or "[]")
            out.append(d)
        return out

    # ── Spoiler ────────────────────────────────────────────────────────────────

    def upsert_spoiler_entry(self, project_id: str, entity: str, fact: str | None = None,
                             spoiler_level: str | None = None, reveal: str | None = None,
                             scenes: list | None = None, triggers: list | None = None,
                             pre_reveal: str | None = None, forbidden_pre_reveal: list | None = None,
                             gender_quarantine: bool = False):
        self._con.execute(
            """INSERT INTO spoiler_entries(project_id, entity, fact, spoiler_level,
                                           reveal, scenes, triggers, pre_reveal,
                                           forbidden_pre_reveal, gender_quarantine)
               VALUES(?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, entity, fact) DO UPDATE SET
                   spoiler_level=excluded.spoiler_level,
                   reveal=excluded.reveal,
                   scenes=excluded.scenes,
                   triggers=excluded.triggers,
                   pre_reveal=excluded.pre_reveal,
                   forbidden_pre_reveal=excluded.forbidden_pre_reveal,
                   gender_quarantine=excluded.gender_quarantine""",
            (project_id, entity, fact, spoiler_level, reveal,
             json.dumps(scenes or [], ensure_ascii=False),
             json.dumps(triggers or [], ensure_ascii=False),
             pre_reveal,
             json.dumps(forbidden_pre_reveal or [], ensure_ascii=False),
             int(bool(gender_quarantine))),
        )
        self._con.commit()

    def get_spoiler_entries(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM spoiler_entries WHERE project_id=? ORDER BY id", (project_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["scenes"] = json.loads(d.get("scenes") or "[]")
            d["triggers"] = json.loads(d.get("triggers") or "[]")
            d["forbidden_pre_reveal"] = json.loads(d.get("forbidden_pre_reveal") or "[]")
            d["gender_quarantine"] = bool(d.get("gender_quarantine"))
            out.append(d)
        return out

    # ── Jobs (ledger) ─────────────────────────────────────────────────────────

    def log_job(self, project_id: str, kind: str, scene_id: str | None = None,
                model_id: str | None = None, backend: str | None = None,
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

    def clear_jobs(self, project_id: str) -> None:
        """Apaga os jobs do projeto. `jobs` é o mirror do api_ledger.jsonl (append-log sem
        chave natural); o write-path reconstrói por clear+reload p/ não inflar o custo a cada
        re-index (ao contrário das outras tabelas, que são idempotentes via UNIQUE upsert)."""
        self._con.execute("DELETE FROM jobs WHERE project_id=?", (project_id,))
        self._con.commit()

    def get_cost_summary(self, project_id: str) -> dict:
        row = self._con.execute(
            """SELECT SUM(cost_usd) as total, SUM(tokens_in) as tin,
                      SUM(tokens_out) as tout, COUNT(*) as n_calls
               FROM jobs WHERE project_id=?""",
            (project_id,),
        ).fetchone()
        return dict(row) if row else {"total": 0, "tin": 0, "tout": 0, "n_calls": 0}

    # ── Observabilidade ──────────────────────────────────────────────────────

    def upsert_metrics(self, project_id: str, rows: list) -> None:
        """Métricas por cena em LOTE (1 commit). Snapshot 1-por-cena (upsert por scene_id).
        rows: [{scene_id, n_lines, n_high, verified, reused, back_pass_rate,
                cost_usd_last, cost_usd, raw}]. `raw` é a string JSON do registro completo."""
        self._con.executemany(
            """INSERT INTO metrics(project_id, scene_id, n_lines, n_high, verified,
                                   reused, back_pass_rate, cost_usd_last, cost_usd, raw)
               VALUES(?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, scene_id) DO UPDATE SET
                   n_lines=excluded.n_lines, n_high=excluded.n_high,
                   verified=excluded.verified, reused=excluded.reused,
                   back_pass_rate=excluded.back_pass_rate,
                   cost_usd_last=excluded.cost_usd_last, cost_usd=excluded.cost_usd,
                   raw=excluded.raw""",
            [(project_id, r.get("scene_id", ""), r.get("n_lines"), r.get("n_high"),
              int(bool(r.get("verified"))), r.get("reused"), r.get("back_pass_rate"),
              r.get("cost_usd_last"), r.get("cost_usd"), r.get("raw")) for r in rows],
        )
        self._con.commit()

    def get_metrics(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT * FROM metrics WHERE project_id=? ORDER BY scene_id", (project_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["verified"] = bool(d.get("verified"))
            d["raw"] = json.loads(d["raw"]) if d.get("raw") else None
            out.append(d)
        return out

    def upsert_warnings(self, project_id: str, rows: list) -> None:
        """Avisos do harness em LOTE (1 commit). rows: [{t, source, warnings:[str]}]."""
        self._con.executemany(
            """INSERT INTO warnings(project_id, t, source, warnings) VALUES(?,?,?,?)
               ON CONFLICT(project_id, t, source) DO UPDATE SET warnings=excluded.warnings""",
            [(project_id, r.get("t"), r.get("source"),
              json.dumps(r.get("warnings", []), ensure_ascii=False)) for r in rows],
        )
        self._con.commit()

    def get_warnings(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT t, source, warnings FROM warnings WHERE project_id=? ORDER BY t", (project_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["warnings"] = json.loads(d.get("warnings") or "[]")
            out.append(d)
        return out

    def upsert_qa_effectiveness(self, project_id: str, rows: list) -> None:
        """Efetividade do QA humano em LOTE (1 commit). Append-log idempotente por (t, source)."""
        self._con.executemany(
            """INSERT INTO qa_effectiveness(project_id, t, source, total_marked, applied,
                                            verbatim, ai, effectiveness_rate, cost_usd)
               VALUES(?,?,?,?,?,?,?,?,?)
               ON CONFLICT(project_id, t, source) DO UPDATE SET
                   total_marked=excluded.total_marked, applied=excluded.applied,
                   verbatim=excluded.verbatim, ai=excluded.ai,
                   effectiveness_rate=excluded.effectiveness_rate, cost_usd=excluded.cost_usd""",
            [(project_id, r.get("t"), r.get("source"), r.get("total_marked"),
              r.get("applied"), r.get("verbatim"), r.get("ai"),
              r.get("effectiveness_rate"), r.get("cost_usd")) for r in rows],
        )
        self._con.commit()

    def get_qa_effectiveness(self, project_id: str) -> list[dict]:
        rows = self._con.execute(
            "SELECT t, source, total_marked, applied, verbatim, ai, effectiveness_rate, "
            "cost_usd FROM qa_effectiveness WHERE project_id=? ORDER BY t", (project_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Stats ────────────────────────────────────────────────────────────────

    def summary(self, project_id: str) -> dict:
        scenes = self.get_scenes(project_id)
        cost = self.get_cost_summary(project_id)
        n_tm = self._con.execute(
            "SELECT COUNT(*) FROM translations WHERE project_id=? AND approved=1",
            (project_id,),
        ).fetchone()[0]
        n_tm_total = self._con.execute(
            "SELECT COUNT(*) FROM translations WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        # Contagens por tipo de artefato — expô-las torna o "silent-zero" da migração
        # visível (um 0 inesperado em glossary/entities salta no resumo).
        n_gloss = self._con.execute(
            "SELECT COUNT(*) FROM glossary WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_ent = self._con.execute(
            "SELECT COUNT(*) FROM entities WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_voice = self._con.execute(
            "SELECT COUNT(*) FROM voice_cards WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_dec = self._con.execute(
            "SELECT COUNT(*) FROM decisions WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_spoil = self._con.execute(
            "SELECT COUNT(*) FROM spoiler_entries WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_lines = self._con.execute(
            "SELECT COUNT(*) FROM scene_lines WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_kb = self._con.execute(
            "SELECT COUNT(*) FROM kb WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_metrics = self._con.execute(
            "SELECT COUNT(*) FROM metrics WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_warn = self._con.execute(
            "SELECT COUNT(*) FROM warnings WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        n_qa = self._con.execute(
            "SELECT COUNT(*) FROM qa_effectiveness WHERE project_id=?", (project_id,)
        ).fetchone()[0]
        return {
            "project_id": project_id,
            "scenes": len(scenes),
            "verified": sum(1 for s in scenes if s["verified"]),
            "scene_lines": n_lines,
            "translations": n_tm_total,
            "tm_approved": n_tm,
            "glossary": n_gloss,
            "entities": n_ent,
            "voice_cards": n_voice,
            "decisions": n_dec,
            "spoiler": n_spoil,
            "kb": n_kb,
            "metrics": n_metrics,
            "warnings": n_warn,
            "qa_effectiveness": n_qa,
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
