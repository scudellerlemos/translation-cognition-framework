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
| **2** | **write path**: `plan_lines`, `back_translations`, `translations(approved=0)`; rewire `build_plan`/`run_scene`/`back_translate`; export `approved_*.csv` | *(enche o corpus que o RAG usa)* | ⏳ |
| **2.5** | — | 🟢 **nº1 TM semântica**: plugar `embedder.search` no `context_pack` como seção rotulada "falas SIMILARES (adapte)" | ⏳ |
| **3** | derivados de `.md` gravam no DB (`state_index` → tabelas `decisions`/`voice_cards`); `kb_ratified.csv` → tabela; **tabela `kb`** p/ `universe_knowledge_base.md` | 🟢 **nº2 KB/lore RAG**: retrieval semântico sobre a KB, **gated pela trava temporal de spoiler** | ⏳ |
| **4** | observabilidade: `metrics`/`warnings`/`qa_effectiveness` → tabelas | — | ✅ migração (read-path); write-path dos produtores deferido |
| **5** | skills `s00–s08` como módulos lendo/gravando DB; CLI e2e | retrieval disponível às skills (reuso da infra) | ⏳ |
| **6** | cutover: `approved_*.csv` e `translation_memory.jsonl` viram **export** do DB; remove leitura flat dos paths migrados | — | ⏳ |
| **7** | — (multi-game) | 🟢 **nº3 RAG cross-game/franquia**: corpus compartilhado por série, retrieval por cena | 🔮 futuro |

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
