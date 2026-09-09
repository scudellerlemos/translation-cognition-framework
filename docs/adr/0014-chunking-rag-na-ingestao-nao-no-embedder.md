# ADR 0014 — Chunking de conteúdo não-atômico acontece na ingestão, não no embedder

**Status:** aceito · **Data:** 2026-09-08

## Contexto

`framework/db/embedder.py` (#105, generalizado sobre #109) indexa 1 vetor por linha de
`translations.source` ou `decisions.summary` — 1-linha-1-vetor, sem chunking, porque diálogo de
jogo e resumos de decisão já chegam pré-segmentados em unidades atômicas (1 fala = 1 linha, 1
decisão = 1 linha).

Isso não se generaliza sozinho pra conteúdo tipo documento: `universe_knowledge_base.md` é lore
extensa, hoje "chunkada" manualmente por seção markdown com curadoria humana (tag
`<!-- reveal: ... -->` por seção `##`/`###`). A pergunta do #169 era se o embedder devia ganhar um
`chunk_fn` por kind (parâmetro configurável de estratégia de chunking — por seção, por parágrafo,
por N tokens com overlap) pra cobrir esse caso e generalizar pra projeto futuro.

Investigando: essa quebra por seção **já existe e já roda antes do embedder ver o dado**.
`migrate_from_flat._migrate_kb` (`framework/db/migrate_from_flat.py`) parseia o markdown por
cabeçalho `##`/`###`, lê o `<!-- reveal: ... -->` de cada seção e grava **1 linha por seção** na
tabela `kb` (`section`, `content`, `reveal`) via `Store.upsert_kb`. Ou seja: pelo momento em que
qualquer indexador (léxico ou semântico) enxerga a tabela `kb`, o conteúdo **já é atômico** — o
mesmo shape que `translations`/`decisions` sempre tiveram.

## Decisão

**O embedder nunca chunka. Chunking de conteúdo não-atômico é responsabilidade da ingestão
(o parser que grava a tabela-fonte), não do `Embedder`.** `_KIND_CONFIG` ganha um kind novo
(`"kb"` → tabela `kb`, coluna `content`) reaproveitando a MESMA indexação genérica
1-linha-1-vetor de `translation`/`decision` — sem `chunk_fn`, sem parâmetro de estratégia:

```python
"kb": {"table": "kb", "text_col": "content",
       "vec_table": "kb_vectors", "emb_table": "kb_embeddings",
       "id_col": "kb_id", "filter_sql": ""},
```

Convenção pra projeto futuro com conteúdo tipo documento (glossário extenso, referência): a
quebra em unidades pesquisáveis acontece no **parser que ingere aquele conteúdo pra uma tabela**
(igual `_migrate_kb` faz pro markdown → tabela `kb`) — por seção, por parágrafo, ou por N tokens,
dependendo do que fizer sentido pra aquele formato de origem. O critério pra "unidade" é o mesmo em
qualquer nível do pipeline: **cada linha da tabela-fonte precisa ser pesquisável e citável sozinha**
(igual 1 fala de diálogo já é). Uma vez que a tabela existe com esse shape, indexar semanticamente é
sempre a mesma receita: 1 entrada em `_KIND_CONFIG` + 1 tabela `<kind>_embeddings` no `schema.sql`
(padrão `tm_embeddings`/`decision_embeddings`/`kb_embeddings`) + reuso de
`Embedder.index_project(kind=...)`.

## Consequências

- (+) Zero código novo de chunking no embedder — reusa a mesma função genérica que já existia pra
  `translation`/`decision`; `index_project(con, project_id, kind="kb")` funciona sem alteração de
  lógica, só de config.
- (+) A convenção fica testável no lugar certo: se a KB de um projeto está mal chunkada
  (seção grande demais, parágrafos misturados), o bug é no parser (`_migrate_kb` ou equivalente
  futuro), não em heurística escondida dentro do embedder.
- (+) Um `chunk_fn` genérico dentro do embedder teria custo de manutenção (parâmetros de overlap,
  tamanho, boundary-detection por formato) pra resolver algo que a ingestão já resolve de forma mais
  simples e específica ao formato de origem.
- (−) Quem escreve um parser de ingestão novo (formato de lore diferente de markdown por seção)
  precisa saber que a responsabilidade de "virar unidade pesquisável" é dele, não do embedder — sem
  isso documentado, a tentação óbvia é adicionar um `chunk_fn` ali. Este ADR é o registro dessa
  decisão pra próxima vez que a pergunta aparecer.
- Extensão feita na mesma issue: `Embedder.search_kb()` (retrieval semântico sobre `kb_vectors`,
  mesmo shape de `search_decisions()`) e `context_pack._load_kb_semantic()`, que injeta uma seção
  **"## 5d. Lore SEMELHANTE (semântica)"** no prompt, adicional a `select_kb()` (léxico, inalterado)
  — nunca substituindo, só suplementando, com dedupe por seção já mostrada e o mesmo gate de
  spoiler (`_reveal_allowed`) que `select_kb`/`_load_decisions_semantic` já usam. Fallback pra `[]`
  sem stack de ML, sem DB, ou em erro inesperado (mesmo padrão de `_load_tm_semantic`).
- Validado com dados reais (`projects/breath_of_fire_4`, 11 seções): queries de lore relevantes
  destacam a seção certa nas top-3 com score visivelmente maior que uma query fora de tópico
  ("receita de bolo de fubá" → scores ~0.14–0.21 vs. ~0.26–0.56 nas relevantes). Achado relevante:
  a KB do BoF4 não tem nenhuma tag `<!-- reveal: ... -->`, então toda seção fica com `reveal=NULL`
  — o gate default-deny bloqueia a seção semântica inteira até o projeto tagueá-la, ou seja, hoje
  esse caminho não muda o pacote de nenhum projeto real (só o léxico `select_kb` está ativo neles).
