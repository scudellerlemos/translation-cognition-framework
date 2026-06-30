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
| **2.5** | — | 🟢 **nº1 TM semântica**: plugar `embedder.search` no `context_pack` como seção rotulada "falas SIMILARES (adapte)" | ⏳ |
| **3** | derivados de `.md` gravam no DB (`decisions`/`voice_cards`/`spoiler`/`kb`) — cobertos pelo mesmo espelho gated da Fase 2 | 🟢 **nº2 KB/lore RAG**: retrieval semântico sobre a KB, **gated pela trava temporal de spoiler** | ✅ |
| **4** | observabilidade: `metrics`/`warnings`/`qa_effectiveness` → tabelas — cobertos pelo mesmo espelho gated | — | ✅ |
| **5** | skills como módulos + CLI e2e — registry SÓ com skills de código (det.: 00/07/08; orquestração: 06); cognitivas (01–04b/05b/06b/06c) ficam playbooks `.md`. `Skill.kind` torna a fronteira estrutural | retrieval disponível às skills (reuso da infra) | ✅ |
| **6** | cutover: **6a** ✅ export DB→flat (`approved_translations.csv`/`translation_memory.jsonl`) + oráculo round-trip lossless; remoção de leitura flat já feita pelo switch gated (Fases 1–3). **6b** ⏳ produtores DB-first (flat vira só export, remove o mirror) — **deferida (precisa de run vivo)** | — | 🟡 6a feito / 6b deferido |
| **7** | — (multi-game) | 🟢 **nº3 RAG cross-game/franquia**: corpus compartilhado por série, retrieval por cena | 🔮 futuro |

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
125 cenas / 6046 linhas). BoF4/Uta seguem flat (`db=null`); `translation_local` é o POC de Ollama (LLM
local), não embeddings.

1. **Instalar a stack** (fora da CI, pesada): `pip install -r requirements-ml.txt`
   (`sentence-transformers` + `sqlite-vec` + `flashrank`; ~700 MB–1,5 GB com torch + modelo MiniLM).
2. **Construir os vetores** (compute único, ~minutos em CPU):
   `python framework/cli.py db index projects/translation_software/translation_software.db bof4`
   → popula `tm_embeddings` + a virtual table `vec0` na própria `.db`.
3. **Pronto**: o `context_pack` em modo DB injeta a seção "falas SIMILARES (adapte)" sozinho
   (o `_get_embedder` carrega o modelo 1×/processo). Sem a stack, cai p/ `[]` (fallback testado).

**Validação ainda pendente:** `embedder.index_project`/`search` nunca rodaram com as deps reais (a CI
usa o fallback de propósito). Ligar pela 1ª vez = confirmar que index+search produzem vizinhos de fato.
