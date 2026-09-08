# Roadmap — Migração dos flat files → SQLite (com RAG encaixado)

> Objetivo: SQLite como fonte única de verdade do runtime, **sem regressão** e **sem perder
> determinismo**. O RAG (recuperação semântica) entra como *upgrade cirúrgico* de retrievers
> específicos — não como reescrita. Cada oportunidade de RAG está encaixada na fase de
> migração que a habilita (o corpus precisa estar no DB primeiro).

## Princípios (valem em todas as fases)

1. **Gated por projeto** — `project.json` com `db` populado → DB; senão flat. BoF4/Uta intactos até optarem.
2. **Paridade como oráculo** — cada migração só "liga" quando um teste prova DB == flat (ou, na TM, não-degradação justificada).
3. **Determinismo é inegociável** — o `context_pack` roda 2× → byte-idêntico. RAG semântico só entra como **suplemento rotulado e bounded**, nunca no núcleo determinístico (ver Guardrails).
4. **Já fazemos RAG** — o `context_pack` é retrieval-augmented; a recuperação hoje é léxica. O trabalho é trocar léxico→semântico **só onde paráfrase/corpus-grande importa**.

## Onde RAG NÃO entra (decidido)

- **Glossário** — match léxico (`_present`) é preciso; semântico traria falso-positivo/bloat. Fica léxico.
- **Voice cards** — match por **nome do falante** (identidade, não similaridade). Fica determinístico.
- **Núcleo do pacote** — match exato de TM, contagens, hashes. Fica determinístico.

## Fases (migração + RAG)

| Fase | Migração (write/read path) | RAG encaixado | Status |
|---|---|---|---|
| **1** | `dialogs.csv` → `scene_lines`; pacote 100% do DB no modo DB | — | ✅ feito (205b8be) |
| **2** | **write path** (consolidado): espelho gated no `state_index.build()` reusa `migrate` → DB vira mirror fiel do estado flat após cada re-index. *(em vez de upsert inline por produtor)* | *(enche o corpus que o RAG usa)* | ✅ |
| **2.5** | — | 🟢 **nº1 TM semântica**: plugar `embedder.search` no `context_pack` como seção rotulada "falas SIMILARES (adapte)" | ✅ |
| **3** | derivados de `.md` gravam no DB (`decisions`/`voice_cards`/`spoiler`/`kb`) — cobertos pelo mesmo espelho gated da Fase 2 | 🟢 **nº2 KB/lore RAG**: retrieval semântico sobre a KB, **gated pela trava temporal de spoiler** | ✅ |
| **4** | observabilidade: `metrics`/`warnings`/`qa_effectiveness` → tabelas — cobertos pelo mesmo espelho gated | — | ✅ |
| **5** | skills como módulos + CLI e2e — registry SÓ com skills de código (det.: 00/07/08; orquestração: 06); cognitivas (01–04b/05b/06b/06c) ficam playbooks `.md`. `Skill.kind` torna a fronteira estrutural | retrieval disponível às skills (reuso da infra) | ✅ |
| **6** | cutover: **6a** ✅ export DB→flat (`approved_translations.csv`/`translation_memory.jsonl`) + oráculo round-trip lossless; remoção de leitura flat já feita pelo switch gated (Fases 1–3). **6b** ✅ `build_plan_chapter` (translations) DB-first via `connector_io.sync_translations_db` — ver [[db-first-6b-escopo]] e [issue #109](https://github.com/scudellerlemos/translation-cognition-framework/issues/109) | — | ✅ 6a+6b feito (escopo: translations) |
| **7** | — (multi-game) | 🟢 **nº3 RAG cross-game/franquia**: corpus compartilhado por série, retrieval por cena | 🔮 futuro |

## Gates de governança sob o switch DB-gated (#85)

Os módulos de gate (`kb_gate`/`kb_phase`/`kb_review`/`glossary_lint`/`spoiler_check`) foram
auditados quanto ao mesmo switch DB-gated do `context_pack`. Achado: **liam sempre o flat**,
mesmo em projeto com `db` populado — divergência silenciosa (o gate validava uma fonte que
podia não ser mais a de verdade). Corrigido em duas frentes:

- **`spoiler_check.py`** (check/check_gender/list_guards) e **`glossary_lint.py`** (lint):
  agora DB-gated via `context_pack.load_spoiler_ledger()`/`load_translated_scenes()` — leem
  SQLite quando o projeto tem `db`, senão flat (comportamento original intacto). Exigiu
  estender `spoiler_entries` com as colunas `forbidden_pre_reveal`/`gender_quarantine`
  (ausentes no schema original; migração ADITIVA via `Store._migrate_schema`, idempotente
  para bancos já existentes).
- **`kb_gate.py`**: só o check de `glossary` (coluna `updated_date`) virou DB-aware (lê
  `updated_at` do banco). Os demais hard/soft-checks deste módulo (`research_log.md`
  reconciliado, `kb_ratified.csv`) permanecem **flat-only por decisão** — ver limite abaixo.

**Limite conhecido (não fechado por #85):** `kb_phase.py` e `kb_review.py` dependem de
`research_log.md` (status de reconciliação por capítulo) e `kb_ratified.csv` (ratificação
humana) — nenhum dos dois tem tabela equivalente no schema.sql hoje. Não é "rotear pelo
switch existente": é desenhar 2 tabelas novas (schema + migração dos dados flat existentes),
decisão de design maior que o escopo de #85. Rastreado em issue separada — antes de tratar
esses 2 módulos como DB-first, decidir se `research_log`/`kb_ratified` viram tabelas ou se
continuam sendo, por design, a única fonte de verdade (mesmo sob projeto DB-gated) — nesse
caso documentar isso como decisão explícita, não como lacuna. Rastreado na
[issue #94](https://github.com/scudellerlemos/translation-cognition-framework/issues/94).

## Write-path consolidado (Fases 2/3/4) — decisão de design

**Decisão (jun/2026):** o write-path NÃO é upsert inline espalhado por
`build_plan`/`run_scene`/`back_translate`/`cost`/`quality_review`. Em vez disso, há **um
único hook gated** no `state_index.build()` — o passo determinístico/idempotente que já
reconstrói o estado consolidado a partir dos artefatos por-cena (ADR 0003). Após gravar os
flats, `state_index._sync_db()` chama `migrate_from_flat.migrate()` (idempotente, upsert) e
o **DB vira mirror fiel** do estado flat completo (scenes, scene_lines, translations,
glossary, entities, voice_cards, decisions, spoiler, back_translations, kb, jobs, metrics,
warnings, qa_effectiveness). Por quê:

- **Offline-testável** — o mirror lê flats → DB; não exige run vivo de API p/ validar (o
  inline exigiria). Testes em `test_runtime.py` (gate-off no-op / gate-on popula).
- **Risco zero ungated** — `project.json:db` ausente (BoF4/Uta hoje) → no-op total.
- **DRY** — reusa o `migrate` já testado; idempotente (re-index não duplica).
- **Determinismo intacto** — não toca o núcleo do `context_pack`.

`migrate()` passou a ler `title`/`media_type`/langs do `project.json` (era hardcoded
"Breath of Fire IV") — pré-requisito p/ o write-path ser multi-projeto.

## Fase 6b — produtores DB-first (#109) — decisão de escopo

**Decisão (set/2026):** o critério de pronto original da issue ("1 projeto rodando end-to-end
com produtores DB-first") não é atingível hoje sem run vivo — **nenhum projeto ativo tem
`db` populado** (`translation_software` é um shell DB-only, corpus BoF4 migrado uma vez, sem
connector/artifacts próprios; BoF4/Uta/Souldiers/Trails/Demo seguem flat). Em vez de esperar
esse pré-requisito (fora do controle desta issue), o escopo foi reduzido ao que o oráculo de
paridade da Fase 6a realmente mede: **translations**, via o produtor `build_plan_chapter.py`.

- **`connector_io.sync_translations_db(root, scene_id, sfx, approved, plan_lines)`** — novo,
  único ponto compartilhado pelas 6 cópias de `build_plan_chapter.py` (mesmo gate-shape de
  `state_index._db_target`, extraído aqui pra nunca divergir entre conectores, espírito do
  #86). Se `project.json:db` não populado → no-op, `False`, caller escreve o CSV como sempre
  (BoF4/Uta/Souldiers/Trails/Demo hoje: comportamento intacto, zero risco).
- Se gated: grava cada offset aprovado direto no `Store` (fonte de verdade) e regenera
  `approved_<sfx>.csv` a **partir do DB** — o flat vira export derivado, não mais o dado
  gravado pelo produtor (o mirror da Fase 2 some para este produtor especificamente).
- **Não migrado para DB-first:** `run_scene.py`, `back_translate.py`, `cost.py`,
  `quality_review.py`, `tm_updater.py` — continuam gravando flat direto (espelhados pelo
  mirror da Fase 2, `state_index._sync_db`). Fora do escopo: nenhum desses tem oráculo de
  paridade equivalente ao de translations hoje; converter sem oráculo seria mudança de fonte
  de verdade sem prova de não-regressão.
- **Validação:** sem projeto DB-gated ativo, não há run vivo possível. Oráculo sintético
  **invertido** de `test_export_roundtrip_lossless` (mesma convenção de toda fase desta
  migração — dado sintético, sem chamada de API): `sync_translations_db` gravando direto no
  Store deve produzir os mesmos registros que o caminho legado (produtor grava flat →
  `migrate_from_flat.migrate()` espelha pro Store), para a mesma entrada — ver
  `framework/connectors/test_connector_io.py::test_sync_translations_db_matches_legacy_flat_then_migrate_oracle`.
- **Em aberto:** validar com run vivo assim que algum projeto ativo adotar `db` (fora do
  controle desta issue — depende de decisão de produto, não técnica).

## Detalhe das oportunidades de RAG

**🟢 nº1 — TM semântica (Fase 2.5, maior ROI).** Hoje uma fala só reusa tradução se for *idêntica*
(`src_key`). A infra (`embedder.py` + `sqlite-vec` + reranker + `store.search_tm_semantic`) **já existe
mas não está plugada** no pipeline (só via `cli db index`). Plugar no `context_pack` (modo DB) como
seção separada e rotulada ataca o custo (re-tradução = 58% do gasto) e a consistência de voz.
Depende da Fase 2 (corpus no DB), mas dá pra começar já com a TM aprovada que está migrada.

**🟢 nº2 — KB/lore (Fase 3).** `universe_knowledge_base.md` agora está no DB (tabela `kb`, por seção).
Retrieval da KB por cena injetaria lore relevante. **Trava obrigatória:** filtro temporal de spoiler.

**Status (jun/2026): migração feita; injeção LIGADA com gate DEFAULT-DENY (seguro por construção).**
A validação com dado real do Utawarerumono mostrou que um gate por **texto** não garante zero-leak
(triggers do ledger em EN vs KB pt-BR com acento; seção spoiler sem marcador, ex.: "Mulher (figura de
memória)", vazava). **Conserto:** a segurança deixou de depender de matching e passou a ser **fail-safe**:
- a tabela `kb` tem coluna **`reveal`** (lida de `<!-- reveal: <scene>|beyond_frontier|safe -->` por seção);
- `context_pack.select_kb` é **default-deny**: injeta uma seção SÓ se `reveal`='safe' ou `reveal` ≤ cena
  atual; **sem tag / beyond_frontier / futuro → excluída**. Dado não-anotado nunca vaza.

**Pré-requisito de UTILIDADE (não de segurança):** anotar as seções da KB com `<!-- reveal: ... -->`
(curadoria humana, como o `spoiler_ledger`). Enquanto não anotar, o gate não injeta nada (seguro).

**🟢 nº3 — Cross-game/franquia (Fase 7).** Quando houver 2+ jogos da mesma série: corpus de
lore/terminologia compartilhado, recuperado por cena. É o caso onde RAG escala (corpus grande,
não indexável por regra). Pós-cutover.

## Guardrails de determinismo (transversal — onde houver semântico)

1. **Vetores pré-computados no DB** (`tm_embeddings` já existe) — build do pacote só consulta, não reinfere.
2. **NN exato** (cosine sobre os vetores), não ANN aproximado, no corpus pequeno; **tie-break por id** (ordem estável).
3. **Modelo pinado** — nome+versão gravados (`tm_embeddings.model_name`); trocar modelo = reindex explícito.
4. **Seção semântica SEPARADA e rotulada** no pacote — nunca misturar no bloco de match exato. Núcleo determinístico intocado; RAG é suplemento auditável.

## Limpeza de texto (códigos do jogo) — decisão

O `target` da TM é **fiel** (com os códigos `[XX]` do engine; o round-trip/conector dependem disso).
Para leitura e embedding semântico existe uma forma **limpa** derivada: `store.strip_codes()` —
**genérico**, remove os `[XX]` (não-ASCII) e normaliza espaços. Cobre ~95% do ruído.

Sobram artefatos **ASCII-controle** específicos do engine (ex.: `@` = 0x40, o `A` = 0x41 após
`[14][XX]`) — o `decode_string` os renderiza como letra porque são ASCII, e não dá pra distinguir
controle de texto **por valor** (`A` é letra normal no meio de palavra). Limpá-los exige a
**gramática dos opcodes**, que é **conhecimento do conector**, não do framework.

**Decisão (jun/2026):** o `strip_codes` genérico fica como está; a limpeza connector-aware
(`to_plain()` por engine, mapeando a gramática completa de opcodes) é item da **evolução do
conector** (pós-produção) — ver [[connector-evolution-vision]]. NÃO tentar remover `@`/`A` no
helper genérico (risco de comer texto real).

## Pré-requisito atravessador

A migração É o que viabiliza o RAG: o **DB com vetores é o store de RAG**. Quanto mais corpus migrado
(Fases 2–3), mais rico o retrieval. Por isso a ordem: encher o DB primeiro, ativar semântica em cima.

## Como LIGAR a TM semântica (stack de ML) — projeto `translation_software`

A migração de DADO está completa; ligar a busca semântica é **operacional**, não migração. O projeto
alvo é **`translation_software`** (único com `db` declarado; corpus do BoF4 já migrado pra dentro dele:
125 cenas / 6046 linhas). BoF4/Uta seguem flat (`db=null`); `translation_local` está **descontinuado**
(ADR 0008 — POC de tier Ollama local pra tradução, não embeddings).

1. **Instalar a stack** (fora da CI, pesada): `pip install -r requirements-ml.txt`
   (`sentence-transformers` + `sqlite-vec` + `flashrank`; ~700 MB–1,5 GB com torch + modelo MiniLM).
2. **Construir os vetores** (compute único, ~minutos em CPU):
   `python framework/cli.py db index projects/translation_software/translation_software.db bof4`
   → popula `tm_embeddings` + a virtual table `vec0` na própria `.db`.
3. **Pronto**: o `context_pack` em modo DB injeta a seção "falas SIMILARES (adapte)" sozinho
   (o `_get_embedder` carrega o modelo 1×/processo). Sem a stack, cai p/ `[]` (fallback testado).

**Validação (correção — este parágrafo estava desatualizado):** `embedder.index_project`/`search` JÁ
rodaram com as deps reais (a CI usa o fallback de propósito, mas fora dela a stack real foi validada):
6046 vetores no `translation_software`, busca exata → score 1.0, variação de vocabulário → 0.944. Ver
memória `semantic-stack-validated` e `docs/ROADMAP.md` (seção B2, Histórico detalhado).
