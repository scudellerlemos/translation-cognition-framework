# Translation Software — Arquitetura limpa (piloto: BoF4)

> Status: **EM DESENVOLVIMENTO — Fase 1 MVP**
> Objetivo: pipeline end-to-end sem `.md` como fonte de dados em runtime; SQLite como fonte única de verdade.

---

## O que é este projeto

Redesign arquitetural do framework: elimina a dependência de flat files (`.jsonl`, `.csv`, `.json`, `.md`)
como fonte de dados em runtime e substitui por SQLite + módulos Python tipados.
Reutiliza o conector e os dados do BoF4 como base de migração e validação.

---

## Objetivos

### Done quando:
- [ ] TM, glossário e voice cards vivem em SQLite e são consultáveis via SQL
- [ ] Migração dos dados do BoF4 executada e validada (`migrate_from_flat.py`)
- [ ] Skill 00 (extraction) funciona como módulo Python com interface typed
- [ ] Context pack lê do banco em vez de flat files
- [ ] Busca semântica na TM operacional (sentence-transformers + sqlite-vec)
- [ ] CLI unificada: `python framework/cli.py <comando>` funciona end-to-end

---

## Stack completa

```
LLM (plugável)
  ├── Anthropic API     claude-sonnet-4-6  (pago, alta qualidade)
  └── Ollama local      qwen2.5:14b        (zero custo, AMD RX 6650 XT)

Embeddings (sempre local, sempre gratuito)
  ├── sentence-transformers  paraphrase-multilingual-MiniLM-L12-v2  (~470 MB)
  ├── sqlite-vec             extensão C — índice vetorial no SQLite
  └── flashrank              MiniLM-L-12 quantizado (~4 MB, reranker)

NER (extração de entidades)
  └── spaCy  xx_ent_wiki_sm  (~31 MB, EN+PT)

Store
  └── SQLite (WAL) — translations, glossary, entities, voice_cards, scenes, jobs

CLI
  └── framework/cli.py — ponto de entrada único
```

---

## Arquitetura das camadas

```
┌─────────────────────────────────────────┐
│  SKILLS  (00–08 como Python classes)     │  framework/skills/s00_*.py ...
│  interface: run(project) → artifacts     │  gate de entrada: check_inputs()
├─────────────────────────────────────────┤
│  RUNTIME  (orquestração)                 │  run_scene.py, context_pack.py
│  lê do banco, não de flat files          │  queries SQL em vez de csv.reader
├─────────────────────────────────────────┤
│  BACKENDS  (LLM plugável)                │  ollama_client.py, llm_client.py
│  interface única: translate(lines)       │  troca de modelo = troca de arquivo
├─────────────────────────────────────────┤
│  STORE  (SQLite + sqlite-vec)            │  framework/db/store.py
│  fonte única de verdade                  │  framework/db/schema.sql
└─────────────────────────────────────────┘
```

---

## Como rodar

### Migrar dados do BoF4 para SQLite
```bash
python framework/cli.py db migrate projects/breath_of_fire_4 projects/translation_software/translation_software.db
python framework/cli.py db summary projects/translation_software/translation_software.db bof4
```

### Indexar TM semântica
```bash
pip install sentence-transformers sqlite-vec flashrank
python framework/cli.py db index projects/translation_software/translation_software.db bof4
```

### Traduzir com backend local
```bash
python framework/cli.py translate projects/translation_software AREAD001 --backend ollama
```

---

## Estrutura

```
project.json              ← manifesto com stack declarada
translation_software.db          ← banco SQLite (gerado por migrate_from_flat.py)
artifacts/                ← traduções e artefatos gerados pelo pipeline novo
  scenes/

framework/db/
  schema.sql              ← schema versionado (fonte única do contrato)
  store.py                ← CRUD tipado (substitui state_index.py)
  embedder.py             ← sentence-transformers + sqlite-vec + flashrank
  migrate_from_flat.py    ← importa dados do BoF4 para SQLite

framework/skills/
  skill_base.py           ← base class Skill com gate de entrada formal
  s00_extraction.py       ← Skill 00 como módulo Python
  (s01..s08 — a implementar)

framework/cli.py          ← CLI unificada
```

---

## Próximos passos

### Fase 1 — MVP (em andamento)
1. **Executar migração** — `migrate_from_flat.py` e validar contagens no banco
2. **Indexar TM semântica** — instalar deps, rodar `db index`, medir hit rate
3. **Adaptar context_pack** — ler TM/glossário do SQLite em vez de flat files
4. **Implementar Skills 01–04** — discovery, entity resolution, KB, glossário como módulos Python
5. **Validar round-trip** — cena completa com store SQLite como fonte

### Fase 2 — Connector registry (depois)
6. **Connector registry** — `registry.detect(dir)` identifica engine automaticamente
7. **Famílias de engine** — binary/text/script/i18n (ver decisão de design abaixo)
8. **Síntese de conector** — loop LLM-propõe → round-trip → refina (oráculo automático)

---

## Decisões de design

| Decisão | Escolha | Motivo |
|---|---|---|
| Store | SQLite (WAL) | stdlib, consultável, versionável, zero ops |
| Embedding | paraphrase-multilingual-MiniLM-L12-v2 | melhor multilingual EN+PT no range <500MB |
| Vector index | sqlite-vec | extensão C, sem servidor separado, filtros SQL nativos |
| Reranker | flashrank MiniLM-L-12 | ~4 MB, gratuito, melhora precisão top-K |
| NER | spaCy xx_ent_wiki_sm | ~31 MB, EN+PT, detecta entidades para Skill 01 |
| LLM local | qwen2.5:14b via Ollama | melhor qualidade que cabe em 8 GB VRAM (partial offload) |
| CLI | argparse (stdlib) | consistente com o resto do codebase, zero deps extras |
| Connector registry | Fase 2 (defer) | depende da validação da arquitetura base primeiro |

---

## Dívidas técnicas

| Item | Prioridade |
|---|---|
| context_pack lendo do SQLite (hoje ainda lê flat files) | P1 |
| Skills 01–08 como módulos Python | P1 |
| Testes de integração para store.py + embedder.py | P1 |
| NER via spaCy integrado ao Skill 01 | P2 |
| Connector registry + famílias de engine | Fase 2 |
