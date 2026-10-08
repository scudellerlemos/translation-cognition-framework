# Stack técnica — modelo, embedding, RAG, execução

Visão consolidada da tecnologia por trás do harness: qual LLM roda onde, qual stack de embedding
alimenta a busca semântica, onde entra RAG e como a execução escala. Cada seção linka pro doc
profundo correspondente — este arquivo é o mapa, não o detalhe.

```mermaid
%%{init: {'flowchart': {'wrappingWidth': 520}}}%%
flowchart TB
  model["<b>MODELO</b> — Anthropic Claude (única parte não-determinística)<br/>translate: Sonnet 4.6 (Haiku 4.5 no tier barato)<br/>back_translate: Opus 4.8 (só alto risco)"]:::mod
  embed["<b>EMBEDDING</b> — default em projeto com db<br/>sentence-transformers · paraphrase-multilingual-MiniLM-L12-v2 (dim 384)"]:::emb
  rag["<b>RAG</b> — 3 retrievers semânticos ativos + 1 futuro<br/>TM semântica — sqlite-vec (vec0)<br/>KB/lore e decisões — gated por spoiler"]:::rg
  exec["<b>EXECUÇÃO</b> — cena = job stateless<br/>run_scene / run_chapter<br/>backend in-session (assinatura) ou api (Batch −50%)"]:::ex
  store["<b>PERSISTÊNCIA</b> — SQLite (opt-in) ou flat files<br/>Store (framework/db/) · TM · glossário · voice cards · ledger"]:::st
  model --> exec
  embed --> rag
  rag --> exec
  exec --> store
  classDef mod fill:#f6d6e8,stroke:#c0397b,color:#000;
  classDef emb fill:#fde6c4,stroke:#c97b1f,color:#000;
  classDef rg fill:#e8dff5,stroke:#6a3d9b,color:#000;
  classDef ex fill:#d6e8f6,stroke:#1f6f9b,color:#000;
  classDef st fill:#d9f2d9,stroke:#2e7d32,color:#000;
```

---

## Modelo (LLM)

**Anthropic Claude**, via SDK oficial (`anthropic`), com tiering por complexidade de linha — trocar
modelo é trocar uma string em `framework/runtime/config.py`, nada mais no harness sabe qual modelo rodou:

| Papel | Modelo | Constante | Quando |
|---|---|---|---|
| Tradução (padrão) | `claude-sonnet-4-6` | `MODEL_TRANSLATE` | maioria das linhas; contexto curado dispensa Opus |
| Tradução (tier barato) | `claude-haiku-4-5` | `MODEL_TRANSLATE_CHEAP` | só linhas single-line no caminho batch (−67%/linha) |
| Verificação | `claude-opus-4-8` | `MODEL_BACK` | back-translation das linhas `risk >= high` (+ amostra de 5% das demais em cenas do batch); último degrau do re-aperto de fitting |

**Duas chamadas de IA, e só estas** (`translate`, `back_translate`) — o resto do harness é
determinístico. Dois backends por trás do mesmo contrato: `in-session` (assinatura, sem chamada de
rede, contexto O(cena)) e `api` (SDK Anthropic — streaming, prompt-caching da doutrina, Batch API
−50%, backoff exponencial em 429/500/timeout). `effort:low` sem thinking na tradução (thinking
custaria ~5× — medido); back-translation mantém thinking (raciocínio importa em ambiguidade).

Detalhe do contrato, backends e benchmarks reais → [`MODEL_INTERFACE.md`](MODEL_INTERFACE.md).
Plumbing HTTP/streaming/backoff → `framework/runtime/llm_client.py`.

---

## Embedding

**Default de todo projeto com `db`** — a stack entra no `pip install .` (dependência do
`pyproject.toml`). Projeto com `db` e sem a stack instalada é **hard-block no `kb_gate`** (antes o
retriever semântico caía para `[]` calado e o projeto parecia usar RAG sem usar). Para rodar sem
busca semântica de propósito: `"db": {..., "semantic": false}` no `project.json` (o gate vira aviso e o pacote usa só o RAG
léxico). Projeto sem `db` (flat files) não é afetado. A CI de push/PR (`test.yml`) não instala
torch: os testes rodam com `TCF_ALLOW_NO_ML=1` (setado no `conftest.py` da raiz), que rebaixa o
bloqueio a aviso. Testada de verdade
(sem mock) semanalmente por `ml-coverage-optional.yml` (#181), piso de 85% em `embedder.py`/
`validate_model.py` — mesma cadência do audit de CVE (`dep-audit-optional.yml`, #89), fora do
push/PR pelo mesmo motivo de custo (torch do zero). Stack (`requirements-ml.txt`):

- **`sentence-transformers`** — modelo `paraphrase-multilingual-MiniLM-L12-v2`, vetores de
  dimensão **384**, normalizados (`normalize_embeddings=True`) para o cosseno virar `1 - L2²/2`.
- **Hardware**: CPU por padrão; roda em GPU automaticamente se torch+ROCm detectado (alvo:
  AMD RX 6650 XT). No Windows fica CPU (ok para corpus de milhares de linhas, poucos minutos).
- **Onde mora**: `framework/db/embedder.py` (`Embedder.encode`/`index_project`/`search`).
- **Como instalar**: `pip install .` já traz; num checkout de dev, `pip install -r requirements-ml.txt`
  (pesado: ~700 MB–1,5 GB, puxa torch). Índice inicial de corpus já existente:
  `python framework/cli.py db index <projeto>.db <project_id>`.
- **Multi-projeto**: processo isolado por projeto, sem daemon compartilhado — cache de download do
  modelo já é por-máquina (default do Hugging Face Hub), reload por processo aceito (ver ADR 0015).

---

## RAG (recuperação semântica)

O `context_pack` já é retrieval-augmented por natureza — a recuperação **padrão é léxica** (match
exato de TM, glossário por termo, voice card por nome de falante). RAG **semântico** entra só como
**suplemento rotulado e bounded** em cima disso, nunca substituindo o núcleo determinístico
(o `context_pack` roda 2× → tem que sair byte-idêntico). Arquitetura só do RAG (dados, indexação,
recuperação, gate de spoiler, degradação) → [`RAG_ARCHITECTURE.md`](RAG_ARCHITECTURE.md).

| RAG | Onde | Mecanismo | Status |
|---|---|---|---|
| **nº1 — TM semântica** | `embedder.search()` → seção "falas SIMILARES (adapte)" no pacote | `sqlite-vec` (tabela virtual `vec0`) para o índice vetorial dentro do próprio SQLite do projeto | ✅ **validado tecnicamente e por ROI real**. ROI medido em produção (10 cenas reais, #175): -24% custo, +2 sucessos/10. Ver [ADR 0016](adr/0016-rag-roi-validado-reindex-obrigatorio.md) — manter índice atualizado é **requisito obrigatório**. Desde #182, isso é automático: `reindex_pending_embeddings()` roda no próprio write-path de tradução (`state_index.approve_scene_db`, chamado por `run_scene`/`run_chapter` quando a cena fecha `verified`), não só em `db migrate` manual. Calibração de `rag_min_score` com dado real (#184) → ver subseção abaixo |
| **nº2 — KB/lore** | `context_pack.select_kb()` (léxico) + `_load_kb_semantic()` (semântico, #169) → seções "5c." e "5d." do pacote | **léxico**: token do título da seção citado na cena. **semântico** (suplemento, nunca substitui): `embedder.search_kb()` sobre `kb_vectors`, dedupe contra o léxico. Ambos **gated pela mesma trava temporal de spoiler** (default-deny por reveal-por-seção) | ✅ ligado (léxico sempre; semântico se a stack de ML estiver instalada E o projeto tiver `kb` indexada — validado com o KB real do BoF4, mas nenhum projeto hoje tem `reveal` tagueado, então o gate barra a seção semântica em produção até isso mudar) |
| **decisões (semântico)** | `context_pack._load_decisions_semantic()` | `embedder` sobre `decision_embeddings`, suplemento ao índice léxico de decisões | ✅ ligado — ver [`RAG_ARCHITECTURE.md`](RAG_ARCHITECTURE.md) |
| **nº3 — cross-game/franquia** | corpus compartilhado por série, retrieval por cena | reusa a mesma infra | 🔮 futuro (multi-game) |

### Fluxo em execução — o laço de reuso

O que acontece com **uma cena** em projeto com `db` ligado, e por onde a tradução aprovada volta
para alimentar a próxima:

```mermaid
flowchart TB
  scene["cena N<br/>linhas-fonte"]
  subgraph pack["context_pack — det., só consulta (vetor pré-computado)"]
    direction LR
    ex["match EXATO<br/>tm_exact"]
    sem["nº1 TM semântica<br/>embedder.search · k=3/linha<br/>rag_min_score ≤ score &lt; 0,999<br/>máx. 8 hits"]
    kb["nº2 KB / decisões<br/>gate de reveal default-deny"]
  end
  split{"_prefilled<br/>fonte já traduzida em OUTRA cena<br/>+ paridade de tokens/quebras?"}
  reuse["reuso de TM<br/>0 token"]
  llm{{"translate<br/>IA · Sonnet / Haiku"}}
  plan["build_plan<br/>grava approved=0"]
  vf["verify round-trip"]
  ok["approve_scene<br/>approved=1"]
  idx["reindex_pending_embeddings<br/>embeda aprovadas ainda sem vetor"]
  db[("SQLite do projeto<br/>translations + tm_vectors (vec0)")]

  scene --> ex & sem & kb
  ex --> split
  split -->|"sim"| reuse
  split -->|"não: linha nova"| llm
  sem -. "falas SIMILARES (adapte)" .-> llm
  kb -. "lore já revelada" .-> llm
  reuse --> plan
  llm --> plan
  plan --> vf --> ok --> idx --> db
  db -. "cena N+1" .-> ex
  db -. "cena N+1" .-> sem

  classDef ia fill:#f6d6e8,stroke:#c0397b,color:#000;
  classDef rg fill:#e8dff5,stroke:#6a3d9b,color:#000;
  classDef st fill:#d9f2d9,stroke:#2e7d32,color:#000;
  classDef save fill:#fde6c4,stroke:#c97b1f,color:#000;
  class llm ia;
  class sem,kb rg;
  class db,idx,ok st;
  class reuse save;
```

- **Onde está a economia** (laranja): linha com match exato de outra cena **não vai ao LLM**
  (`model._select_reuse`); cena 100% reaproveitada não faz chamada nenhuma. É o caminho que rendeu
  o −24% do ADR 0016 — o semântico (roxo) só **informa** o prompt das linhas novas, não corta tokens.
- **Só vira TM o que fechou `verified`**: `build_plan` grava `approved=0`; `approve_scene` promove
  depois do round-trip (#216). Busca exata e semântica filtram `approved=1`.
- **O vetor nasce na aprovação**: `reindex_pending_embeddings` só embeda linha aprovada e roda logo
  depois do `approve_scene` (`state_index.approve_scene_db`) — a cena N+1 já enxerga a cena N nas
  duas buscas, exata e semântica.

### `rag_min_score` — calibração com dado real (#184)

`Embedder.search()` casa só a coluna `source` (texto em inglês) — a qualidade da tradução em
`target` **não** entra no score, só aparece como metadado na sugestão "falas SIMILARES (adapte)".
Score = `1.0 - distancia_L2² / 2` sobre vetores unit-norm (`paraphrase-multilingual-MiniLM-L12-v2`,
dim 384): idêntico → 1.0, ortogonal → 0.0, oposto → -1.0.

**Amostra real usada** (não sintética): 12 cenas do BoF4 recém-traduzidas via backend `api`
(pipeline real, custo real) e aprovadas em `build_plan_chapter` — 323 linhas, 323 vetores
indexados em `projects/translation_software/translation_software.db`. **Caveat de tamanho**: é
uma fração pequena do corpus completo (125 cenas / 6.046 linhas) — o corpus original de 6.046
vetores citado em versões antigas desta página foi apagado como efeito colateral da investigação
do #175, e regenerá-lo integralmente custaria a mais que o orçamento aprovado para esta calibração
($3,5 reais em chamadas de API); a chave usada esgotou o crédito (`credit balance too low`) em
$3,445 gastos, no meio do lote de regeneração. A amostra é real e suficiente para calibrar a
**forma da distribuição** (que é o que importa aqui — o score depende só do texto-fonte, não da
cobertura do corpus), mas não é representativa de recall/cobertura em produção.

40 queries de teste em 5 categorias, rodadas contra o índice real (`sample_queries.py`, não
versionado — script de calibração pontual):

| Categoria | Exemplo | Score (top hit) |
|---|---|---|
| Verbatim normalizado (texto do corpus após `strip_codes`, sem alteração) | `"Monsters! They're everywhere!..."` | **1,0** (5/5 queries) |
| Quase-verbatim (mesma frase digitada à mão, pequena diferença de pontuação/aspas) | "Where do you want to go?" | 0,83–0,89 |
| Paráfrase genuína (mesmo sentido, palavras diferentes) | "So what is the state of the sacrifice now?" | 0,71–0,89 (uma cauda em 0,57) |
| Mesmo domínio temático, conteúdo específico diferente (ruído plausível) | "Take this sword, it was forged by ancient smiths" → hit sobre uma lâmina que não corta | 0,37–0,51 |
| Fora de domínio (não relacionado ao jogo) | "Preheat the oven to 200 degrees..." | 0,13–0,38 |

**Onde a qualidade cai**: inspecionando os hits manualmente, a partir de ~0,57 pra baixo os
resultados retornados já não são genuinamente reaproveitáveis — casam só por vocabulário temático
comum (fantasia/RPG), não por conteúdo real da fala (ex.: query sobre "espada forjada por ferreiros
antigos" retorna, com score 0,51, uma fala sobre "esta lâmina não corta", sem relação de sentido
real). Acima de ~0,71 os hits são paráfrases genuínas, direto reaproveitáveis como referência de
adaptação. O teto de ruído observado (falas de domínio-mas-não-relacionadas + fora de domínio) foi
**0,51**.

**Valor escolhido: `rag_min_score = 0.55`** — acima do teto de ruído medido (0,51) com margem de
segurança, abaixo do piso da paráfrase genuína (0,57+). Corta o lixo temático e o fora-de-domínio
sem descartar paráfrases úteis. Configurado em `projects/translation_software/project.json`.

**Onde RAG deliberadamente NÃO entra** (decidido, não esquecido): glossário (match léxico é
preciso; semântico traria falso-positivo), voice cards (identidade por nome, não similaridade),
núcleo do pacote (match exato/contagens/hashes — determinismo é inegociável ali).

Vetores são **pré-computados** (build do pacote só consulta, não reinfere) e o **modelo é pinado**
(`tm_embeddings.model_name` grava o nome; trocar modelo = reindex explícito). Reindex incremental
(`Store.reindex_pending_embeddings()`, pula o que já tem vetor, nunca levanta sem deps de ML) roda
tanto em `db migrate` (#171) quanto no write-path real de tradução (#182) — uma linha aprovada via
`run_scene` fica pesquisável sem passo manual. Detalhe de fases e decisões de design →
[`DB_MIGRATION_ROADMAP.md`](DB_MIGRATION_ROADMAP.md).

---

## Execução

Cada cena roda como **job stateless e limitado** — contexto O(cena), não O(histórico):

```
run_scene(cena): context_pack → translate[IA] → build_plan → verify (round-trip)
                 → back_translate[IA, só alto risco] → checkpoint + state_index
```

- **`run_scene.py`** — orquestrador de 1 cena; **`run_chapter.py`** — driver de capítulo, loop
  resumível, `--max-usd` como teto duro de gasto (estimativa pré-voo antes de comprometer).
- **Escala**: Batch API (−50%, paralelo pela Anthropic, ~1h/corpus) é o default do `run_chapter`
  no backend `api`; tempo real só com `--no-batch` ou via `run_scene` (piloto/debug individual).
- **Checkpoints**: `run_state.json` por cena — cair na cena 40 não perde as 39 anteriores.
- **Custo auditável**: `api_ledger.jsonl` registra toda chamada cobrada (inclusive falhas);
  recuperação por-linha (não por-cena) mantém o retry ∝ linhas quebradas.

Detalhe medido (custo, recuperação por-linha, benchmarks) → [`ARCHITECTURE.md`](ARCHITECTURE.md)
e [`TRANSLATION_PIPELINE.md`](TRANSLATION_PIPELINE.md).

---

## Persistência

Dois modos, **gated por projeto** (`project.json` com `db` populado → SQLite; senão, flat files):

- **SQLite** (`framework/db/store.py`, classe `Store`) — WAL + thread-safe, schema único
  (`projects`, `scenes`, `translations`, `scene_lines`, `kb`, `glossary`, `entities`,
  `voice_cards`, `decisions`, `spoiler_entries`, `research_log`, `kb_ratified`, `back_translations`, `jobs`, `metrics`, `warnings`,
  `qa_effectiveness`). É o modo que habilita RAG (o vetor precisa de um lugar pra morar).
- **Flat files** (legado) — `translation_memory.jsonl`, `glossary.csv`, `state/*.json`. BoF4 e
  Utawarerumono seguem flat; `translation_software` e `demo` são os projetos com `db` declarado hoje.
- **Ponte**: `migrate_from_flat.py` / `export_to_flat.py` — paridade DB==flat é o oráculo; o
  write-path por cena é `sync_translations_db` + `state_index.approve_scene_db`; o espelho do corpus
  inteiro fica no `state_index.build()` deliberado (CLI), não no checkpoint por cena.

Detalhe → [`STATE_MANAGEMENT.md`](STATE_MANAGEMENT.md).

---

## Onde cada projeto está hoje

| Projeto | DB/RAG | Modelo | Execução |
|---|---|---|---|
| `utawarerumono` | flat files | Sonnet/Opus (API) | concluído — 16 capítulos, Batch API |
| `breath_of_fire_4` | flat files (corpus migrado *para dentro* de `translation_software`) | Haiku/Sonnet/Opus | concluído — 125 cenas |
| `souldiers` | flat files | Haiku/Sonnet/Opus (Batch API) | concluído — 470 cenas, terceiro engine (Unity Addressables) |
| `trails_sky_sc` | flat files | — (ainda não traduzido via harness) | em andamento — quarto engine (Falcom); 67 cenas extraídas, cena-piloto com round-trip fechado |
| `translation_software` | **SQLite + RAG nº1/nº2 ativos** | — | referência de arquitetura DB, não um projeto de tradução em progresso |
| `translation_local` | — | — | **DESCONTINUADO** (ADR 0008) — POC de tier Ollama local p/ tradução, regressão de velocidade + erro de terminologia na validação |
