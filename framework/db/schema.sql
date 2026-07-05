-- schema.sql — schema SQLite do Translation Cognition Framework (translation_software)
-- Versão 1.0 — junho 2026
--
-- Substitui os flat files dispersos (jsonl, csv, json) por uma fonte única
-- versionada e consultável. Cada tabela tem FOREIGN KEY implícita via scene_id.
--
-- Extensões opcionais (carregadas em runtime):
--   sqlite-vec  → habilita busca semântica na TM via embeddings

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ── Projetos ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id          TEXT PRIMARY KEY,          -- ex: translation_software
    title       TEXT NOT NULL,
    source_lang TEXT NOT NULL DEFAULT 'en',
    target_lang TEXT NOT NULL DEFAULT 'pt-BR',
    media_type  TEXT,                      -- game | film | series
    created_at  REAL NOT NULL
);

-- ── Cenas ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scenes (
    id          TEXT NOT NULL,             -- ex: AREAD001
    project_id  TEXT NOT NULL REFERENCES projects(id),
    status      TEXT NOT NULL DEFAULT 'pending',
                                           -- pending | extracted | planned |
                                           -- translated | verified | approved
    n_lines     INTEGER,
    n_high      INTEGER,
    verified    INTEGER DEFAULT 0,         -- 0/1 bool
    cost_usd    REAL DEFAULT 0.0,
    backend     TEXT,                      -- api | ollama
    model_id    TEXT,
    created_at  REAL,
    updated_at  REAL,
    PRIMARY KEY (id, project_id)
);

-- ── Traduções (TM) ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS translations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id    TEXT NOT NULL REFERENCES projects(id),
    scene_id      TEXT NOT NULL,
    offset        TEXT NOT NULL,           -- ex: AREAD001.DAT:0:3
    source        TEXT NOT NULL,
    target        TEXT,
    speaker       TEXT,
    tone_register TEXT,
    intent        TEXT,
    risk_level    TEXT,                    -- low | medium | high | critical
    risk_notes    TEXT,
    approved      INTEGER DEFAULT 0,       -- 0/1 revisão humana
    backend       TEXT,
    model_id      TEXT,
    created_at    REAL,
    UNIQUE(project_id, scene_id, offset)
);

CREATE INDEX IF NOT EXISTS idx_translations_source
    ON translations(source);
CREATE INDEX IF NOT EXISTS idx_translations_scene
    ON translations(project_id, scene_id);
CREATE INDEX IF NOT EXISTS idx_translations_approved
    ON translations(project_id, approved);

-- ── Linhas da cena (dialogs.csv — extração pré-tradução) ──────────────────────
-- Fonte das "lines" que o context_pack monta no pacote (offset/source/byte_budget).
CREATE TABLE IF NOT EXISTS scene_lines (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    scene_id    TEXT NOT NULL,
    offset      TEXT NOT NULL,
    source      TEXT,
    byte_budget INTEGER,
    UNIQUE(project_id, scene_id, offset)
);

CREATE INDEX IF NOT EXISTS idx_scene_lines_scene
    ON scene_lines(project_id, scene_id);

-- ── Glossário ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS glossary (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id     TEXT NOT NULL REFERENCES projects(id),
    term           TEXT NOT NULL,
    translation    TEXT NOT NULL,
    handling_rule  TEXT,                   -- preserve | translate | adapt | ...
    domain         TEXT,
    category       TEXT,                   -- compat flat: coluna 'category' do glossary.csv
    aliases        TEXT,                   -- ";"-separado (compat context_pack.select_glossary)
    spoiler_level  TEXT,                   -- compat flat: 'spoiler_level' (renderizado no prompt)
    notes          TEXT,
    updated_at     REAL,
    UNIQUE(project_id, term)
);

-- ── Entidades ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS entities (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id           TEXT NOT NULL REFERENCES projects(id),
    name                 TEXT NOT NULL,
    canonical_pt         TEXT,
    entity_type          TEXT,             -- character | place | item | concept | faction
    first_scene          TEXT,
    spoiler_reveal_scene TEXT,
    notes                TEXT,
    UNIQUE(project_id, name)
);

-- ── Perfis de voz (voice cards) ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS voice_cards (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   TEXT NOT NULL REFERENCES projects(id),
    speaker      TEXT NOT NULL,
    aliases      TEXT,                     -- JSON array (compat context_pack.select_voices)
    register     TEXT,                     -- formal | informal | archaic | child | ...
    quirks       TEXT,                     -- JSON array de características de voz
    example_src  TEXT,                     -- JSON array de exemplos em inglês
    example_tgt  TEXT,                     -- JSON array de exemplos em pt-BR
    lines        TEXT,                     -- JSON array de bullets de voz (formato context_pack)
    criticality  TEXT DEFAULT 'medium',    -- high | medium | low
    UNIQUE(project_id, speaker)
);

-- ── Decisões (decision_index — regras de tradução por tag/universal) ───────────
CREATE TABLE IF NOT EXISTS decisions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    title       TEXT NOT NULL,
    summary     TEXT,
    universal   INTEGER DEFAULT 0,         -- 0/1 — regra do conector aplicável sempre
    tags        TEXT,                      -- JSON array
    UNIQUE(project_id, title)
);

-- ── Spoiler ledger (filtro temporal de revelação) ─────────────────────────────
CREATE TABLE IF NOT EXISTS spoiler_entries (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id           TEXT NOT NULL REFERENCES projects(id),
    entity               TEXT,
    fact                 TEXT,
    spoiler_level        TEXT,
    reveal               TEXT,                    -- beyond_frontier | <scene_id>
    scenes               TEXT,                    -- JSON array
    triggers             TEXT,                    -- JSON array
    pre_reveal           TEXT,                    -- guard de ambiguidade pré-revelação
    forbidden_pre_reveal TEXT,                    -- JSON array — strings proibidas antes do reveal (spoiler_check)
    gender_quarantine    INTEGER DEFAULT 0,        -- 0/1 — genero da entidade em segredo (spoiler_check.check_gender)
    UNIQUE(project_id, entity, fact)
);

-- ── Knowledge base (lore/terminologia — universe_knowledge_base.md por seção) ──
-- Corpus de lore p/ retrieval semântico por cena (RAG nº2), gated por spoiler.
CREATE TABLE IF NOT EXISTS kb (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    section     TEXT NOT NULL,
    content     TEXT,
    reveal      TEXT,                      -- <scene> | beyond_frontier | safe (default-deny: NULL = não injeta)
    UNIQUE(project_id, section)
);

-- ── Back-translation (verificação pt-BR → EN de linhas de alto risco) ─────────
CREATE TABLE IF NOT EXISTS back_translations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    scene_id    TEXT NOT NULL,
    offset      TEXT NOT NULL,
    back_en     TEXT,
    verdict     TEXT,                      -- pass | fail | ...
    note        TEXT,
    UNIQUE(project_id, scene_id, offset)
);

-- ── Jobs (ledger auditável) ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    scene_id    TEXT,
    kind        TEXT NOT NULL,             -- translate | back_translate | verify | embed
    model_id    TEXT,
    backend     TEXT,                      -- api | ollama | local
    tokens_in   INTEGER DEFAULT 0,
    tokens_out  INTEGER DEFAULT 0,
    cost_usd    REAL DEFAULT 0.0,
    batch       INTEGER DEFAULT 0,         -- 0/1
    created_at  REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_jobs_project ON jobs(project_id);
CREATE INDEX IF NOT EXISTS idx_jobs_scene ON jobs(project_id, scene_id);

-- ── Observabilidade ───────────────────────────────────────────────────────────
-- Métricas por cena (snapshot reescrito a cada run — 1 linha por cena). Os blocos
-- aninhados translate/back ficam preservados em `raw` (JSON) p/ não perder nada;
-- os escalares ficam em colunas próprias p/ consulta direta.
CREATE TABLE IF NOT EXISTS metrics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    scene_id        TEXT NOT NULL,
    n_lines         INTEGER,
    n_high          INTEGER,
    verified        INTEGER DEFAULT 0,         -- 0/1 bool
    reused          INTEGER,
    back_pass_rate  REAL,
    cost_usd_last   REAL,
    cost_usd        REAL,
    raw             TEXT,                       -- JSON do registro completo (translate/back)
    UNIQUE(project_id, scene_id)
);

CREATE INDEX IF NOT EXISTS idx_metrics_scene ON metrics(project_id, scene_id);

-- Avisos do harness (append-log: state_index, validações). Chave (t, source) torna a
-- re-migração idempotente sem perder histórico realista.
CREATE TABLE IF NOT EXISTS warnings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id  TEXT NOT NULL REFERENCES projects(id),
    t           REAL,
    source      TEXT,
    warnings    TEXT,                           -- JSON array de strings
    UNIQUE(project_id, t, source)
);

-- Efetividade do QA humano (quality_review apply): quanto do que foi marcado virou
-- aplicação e a que custo. Append-log idempotente por (t, source).
CREATE TABLE IF NOT EXISTS qa_effectiveness (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id         TEXT NOT NULL REFERENCES projects(id),
    t                  REAL,
    source             TEXT,
    total_marked       INTEGER,
    applied            INTEGER,
    verbatim           INTEGER,
    ai                 INTEGER,
    effectiveness_rate REAL,
    cost_usd           REAL,
    UNIQUE(project_id, t, source)
);

-- ── Embeddings (TM semântica) ─────────────────────────────────────────────────
-- Criada via sqlite-vec se extensão disponível (embedder.py cria em runtime).
-- Guardamos aqui só os metadados; os vetores ficam na tabela virtual vec0.
CREATE TABLE IF NOT EXISTS tm_embeddings (
    translation_id  INTEGER PRIMARY KEY REFERENCES translations(id),
    model_name      TEXT NOT NULL,         -- paraphrase-multilingual-MiniLM-L12-v2
    dim             INTEGER NOT NULL,      -- 384
    indexed_at      REAL
);
