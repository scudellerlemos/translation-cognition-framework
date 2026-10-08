# RAG_ARCHITECTURE.md — arquitetura do RAG semântico

Só o RAG, de ponta a ponta: de onde vem o dado, como vira vetor, como é consultado na hora de
traduzir e o que impede vazamento de spoiler. Visão de stack inteira (modelo, execução,
persistência) → [`STACK.md`](STACK.md). ROI medido → [ADR 0016](adr/0016-rag-roi-validado-reindex-obrigatorio.md).

**Em uma frase:** o `context_pack` já recupera contexto por match léxico (TM exata, glossário, voice
cards); o RAG semântico é um **suplemento rotulado e limitado** em cima disso — três retrievers
sobre o mesmo SQLite do projeto, todos opcionais, nenhum no caminho crítico.

---

## 1. Visão geral

```mermaid
%%{init: {'flowchart': {'wrappingWidth': 520}}}%%
flowchart TB
  subgraph src["FONTES (por projeto)"]
    f1["traduções aprovadas<br/>approved_*.csv"]
    f2["decision_log.md"]
    f3["universe_knowledge_base.md"]
  end
  subgraph ing["INGESTÃO — det."]
    i1["sync_translations_db + approve_scene_db<br/>(write-path de cada cena)"]
    i2["migrate_from_flat<br/>(mirror flat→DB)<br/>KB quebrada por seção ##/###"]
  end
  subgraph db["SQLite do projeto"]
    t1[("translations<br/>decisions · kb")]
    t2[("vec0<br/>tm_vectors · decision_vectors · kb_vectors")]
  end
  emb["Embedder<br/>MiniLM multilíngue · dim 384<br/>local, CPU/GPU"]
  ret["<b>RECUPERAÇÃO</b> — context_pack, det.<br/>nº1 TM semântica · nº2 KB / lore · decisões semelhantes"]
  prompt["scene_prompt.md<br/>seções rotuladas"]
  llm{{"translate<br/>IA"}}

  f1 --> i1
  f1 & f2 & f3 --> i2
  i1 & i2 --> t1
  t1 -->|"reindex_pending_embeddings"| emb
  emb -->|"1 linha = 1 vetor"| t2
  t2 --> ret
  emb -. "embeda a query" .-> ret
  ret --> prompt --> llm

  classDef ia fill:#f6d6e8,stroke:#c0397b,color:#000;
  classDef em fill:#fde6c4,stroke:#c97b1f,color:#000;
  classDef rg fill:#e8dff5,stroke:#6a3d9b,color:#000;
  classDef st fill:#d9f2d9,stroke:#2e7d32,color:#000;
  class llm ia;
  class emb em;
  class ret rg;
  class t1,t2 st;
```

| Peça | Onde | Papel |
|---|---|---|
| `Embedder` | `framework/db/embedder.py` | `encode` / `index_project` / `search` / `search_decisions` / `search_kb` |
| `Store` | `framework/db/store.py` | tabelas-fonte + `reindex_pending_embeddings()` |
| `context_pack` | `framework/runtime/context_pack.py` | `_load_tm_semantic` / `_load_kb_semantic` / `_load_decisions_semantic` + `_reveal_allowed` |
| write-path | `connector_io.sync_translations_db` → `state_index.approve_scene_db` | grava a cena (`approved=0`); ao fechar `verified`, aprova e dispara o reindex |

### Para que serve a TM semântica

Ela cobre o caso que o hash não pega: a fala **quase igual** a uma já traduzida. Uma vírgula ou
uma palavra de diferença muda a chave da TM exata, e a fala vai ao modelo como se fosse nova. Sem
referência, o modelo traduz do zero e pode escolher outro fraseado para o que, no jogo, é a mesma
frase com uma variação.

Jogos têm muito texto assim: a mesma pergunta de NPC com pontuação diferente, a mesma mensagem de
sistema com outro nome de item, a fala que um personagem repete com pequena mudança. Para o
jogador, traduções diferentes dessas falas parecem descuido.

A TM semântica acha essas falas vizinhas e as coloca no prompt, com a tradução que foi aprovada,
numa seção rotulada:

```
**Falas SIMILARES (nao identicas) — use p/ voz/fraseado, ADAPTE ao contexto:**
- (~0.87) `Where do you want to go?` -> `Para onde você quer ir?`
```

O par acima é ilustrativo. O número entre parênteses é o score de similaridade, que o modelo vê
junto com o par.

Três propriedades definem o papel dela:

- **É referência, não substituição.** A fala continua indo ao modelo. A instrução é adaptar, e não
  copiar, porque a diferença entre as duas falas pode importar. Quem substitui é só o caminho
  exato.
- **Não decide nada no pipeline.** Um vizinho ruim custa algumas linhas de prompt e pode ser
  ignorado pelo modelo. Por isso o limiar pode ser mais permissivo do que seria aceitável para
  reuso automático.
- **Só mostra tradução aprovada.** O que serve de referência já passou no round-trip.

Na calibração do `rag_min_score` (abaixo), as faixas úteis foram as de fala quase idêntica (score
de 0,83 a 0,89) e de paráfrase (0,71 a 0,89). É nelas que a referência ajuda.

O que está e o que não está medido: a medição do ADR 0016 mostrou que o ganho de **custo** veio do
reuso exato, e que ligar a busca semântica não piorou os lints de glossário e de naturalidade. O
ganho de **consistência** da TM semântica é a intenção do desenho e ainda não foi medido
isoladamente.

---

## 2. Modelo de dados

Mesma estrutura para os três tipos (`_KIND_CONFIG` em `embedder.py`): tabela-fonte já atômica →
tabela virtual `vec0` com o vetor → tabela de metadados que pina o modelo.

```mermaid
erDiagram
  translations ||--o| tm_vectors : "translation_id"
  translations ||--o| tm_embeddings : "translation_id"
  decisions ||--o| decision_vectors : "decision_id"
  decisions ||--o| decision_embeddings : "decision_id"
  kb ||--o| kb_vectors : "kb_id"
  kb ||--o| kb_embeddings : "kb_id"

  translations {
    text source "texto embedado"
    text target
    int approved "so approved=1 e indexado"
  }
  decisions {
    text summary "texto embedado"
    text reveal "gate de spoiler"
  }
  kb {
    text content "texto embedado"
    text reveal "gate de spoiler"
  }
  tm_vectors {
    float_384 embedding "vec0, unit-norm"
  }
  tm_embeddings {
    text model_name "modelo pinado"
    int dim
    real indexed_at
  }
```

- **O que é embedado**: a coluna-fonte passada por `strip_codes` (sem códigos de controle do jogo).
  Na TM é o `source` — a qualidade do `target` não entra no score.
- **Sem chunking no embedder** ([ADR 0014](adr/0014-chunking-rag-na-ingestao-nao-no-embedder.md)):
  conteúdo não-atômico (a KB em markdown) é quebrado **na ingestão**, por seção.
- **Linha editada sai da busca**: trigger em `decisions.summary` / `kb.content` apaga o metadado de
  embedding; `search_decisions` / `search_kb` fazem JOIN nele, então a linha some até o reindex.

---

## 3. Caminho de escrita — quando o vetor nasce

```mermaid
flowchart TB
  a["db index (CLI)<br/>manual, --force = do zero"]
  b["migrate_from_flat<br/>mirror flat→DB no início do run"]
  c["approve_scene_db<br/>cena fechou verified (#182, #216)"]
  r["Store.reindex_pending_embeddings"]
  q["linhas SEM vetor<br/>translations: só approved=1<br/>decisions · kb: todas"]
  e["Embedder.encode<br/>batch 64, normalizado"]
  w[("vec0 + *_embeddings")]
  x["retorna None<br/>escrita da TM segue"]

  a --> q
  b & c --> r --> q --> e --> w
  r -. "sem stack de ML<br/>ou falha no índice" .-> x

  classDef em fill:#fde6c4,stroke:#c97b1f,color:#000;
  classDef st fill:#d9f2d9,stroke:#2e7d32,color:#000;
  class e em;
  class w st;
```

- **Incremental**: pula o que já tem vetor. **Nunca derruba a escrita**: o dado já está em SQL
  antes da chamada; falha de embedding nunca derruba a escrita.
- **Custo é latência, não dinheiro**: ~9–12 s por cena para carregar o modelo (roda local); o
  encode de uma linha é ~0,06 s. Processo isolado por projeto, sem daemon
  ([ADR 0015](adr/0015-embedder-isolado-por-processo-nao-daemon-compartilhado.md)).
- **Reindex é na aprovação, não no `build_plan`**: no `build_plan` a cena ainda está `approved=0`
  e o embedder só embeda `approved=1`. Rodando depois do `approve_scene`, a cena N já é vizinha
  semântica da cena N+1 (coberto por `test_verified_scene_is_semantically_searchable_end_to_end`).

---

## 4. Caminho de leitura — os três retrievers

```mermaid
flowchart TB
  scene["cena: linhas-fonte"]

  subgraph tm["nº1 TM semântica — 1 query POR LINHA"]
    direction TB
    a1["SQL: projeto + approved=1<br/>GROUP BY source,target"]
    a2["exclui o exato<br/>score &lt; 0,999"]
    a3["top k=3 por distância L2"]
    a4["corte rag_min_score"]
    a5["dedup · ordena por score · máx. 8"]
    a1 --> a2 --> a3 --> a4 --> a5
  end

  subgraph kb["nº2 KB / lore — 1 query POR CENA"]
    direction TB
    b1["query = 2000 primeiros chars da cena"]
    b2["SQL: projeto, TODOS por distância"]
    b3{"gate de reveal"}
    b4["primeiros k=3 aprovados · máx. 5"]
    b5["dedupe contra o léxico"]
    b1 --> b2 --> b3 -->|"passa"| b4 --> b5
  end

  subgraph dec["decisões semelhantes — 1 query POR CENA"]
    direction TB
    c1["mesma query da KB"]
    c2["SQL: projeto, TODAS por distância"]
    c3{"gate de reveal"}
    c4["primeiras k=3 aprovadas · máx. 8"]
    c5["dedupe contra o léxico"]
    c1 --> c2 --> c3 -->|"passa"| c4 --> c5
  end

  scene --> a1
  scene --> b1
  scene --> c1
  a5 --> s1["falas SIMILARES (adapte)"]
  b5 --> s2["5d. Lore SEMELHANTE"]
  c5 --> s3["Decisões SEMELHANTES"]

  classDef rg fill:#e8dff5,stroke:#6a3d9b,color:#000;
  classDef out fill:#d6e8f6,stroke:#1f6f9b,color:#000;
  class a1,a2,a3,a4,a5,b1,b2,b4,b5,c1,c2,c4,c5 rg;
  class s1,s2,s3 out;
```

- **Filtro antes do top-k, sempre**: projeto, `approved` e exclusão do exato vão no SQL. Cortar
  depois devolvia menos de k hits (ou zero, em fala curta tipo "Yes." com muitos exatos).
- **Gate antes do corte, na KB e nas decisões**: a busca traz tudo em ordem de distância e o k é
  contado só entre o que passou no gate — senão os k mais próximos ainda não revelados zeravam a seção.
- **Busca exata, não aproximada**: scan linear sobre os vetores do projeto, pelo determinismo.
  Reavaliar ANN a partir de ~50–100 mil vetores por projeto.
- **Score** = `1 − L2²/2` sobre vetores unit-norm (idêntico 1,0 · ortogonal 0,0). `rag_min_score`
  é por projeto, em `project.json`; calibração → [abaixo](#rag_min_score--calibração-com-dado-real).
- **Sem reranker**: o pacote ordena por score (ordem estável). O FlashRank foi removido em
  2026-10-07 — medido, não mudava o que entrava no pacote e custava ~200 ms por linha.
- **Texto embedado sem códigos do jogo**: `strip_codes` remove os códigos de controle antes do
  encode, para a similaridade medir o sentido da fala e não a formatação.
- **Determinismo**: vetores pré-computados + ordenação estável → `context_pack` rodado 2× sai
  byte-idêntico.

### Implementação e parâmetros

A consulta da TM semântica, com os filtros antes do `LIMIT`. Com o operador `MATCH ... k` do
`vec0` o corte vinha primeiro, sobre a tabela inteira, e por isso a busca usa varredura com
`vec_distance_l2`:

```sql
SELECT ..., MIN(vec_distance_l2(v.embedding, :consulta)) AS l2
FROM tm_vectors v JOIN translations t ON t.id = v.translation_id
WHERE t.project_id = :projeto AND t.approved = 1
GROUP BY t.source, t.target          -- o mesmo par em N cenas ocupa 1 vaga, não N
HAVING l2 > :l2_do_match_exato       -- exclui o que o caminho léxico já trouxe
ORDER BY l2 LIMIT :k
```

**Parâmetros de recuperação** (em `context_pack.py`):

| Parâmetro | TM semântica | KB e decisões semânticas |
|---|---|---|
| Consulta | uma por fala da cena | uma por cena (os primeiros 2.000 caracteres do texto da cena) |
| `k` (vizinhos por consulta) | 3 | 3 |
| Teto por cena | 8 pares fonte→tradução | 3 decisões e 3 seções de KB |
| Score mínimo | `rag_min_score` (0,55; calibrado, ver abaixo) | sem limiar; o corte é o `k` |
| Score máximo | 0,999 (acima disso é match exato) | — |
| Filtro | só `approved=1`, só do projeto | marca `reveal` já ultrapassada (default-deny) |
| Deduplicação | por par (fonte, tradução), no SQL e no pacote | o que já entrou pelo caminho léxico não repete |
| Ordenação | score decrescente, desempate pelo texto (saída estável) | idem |

Sobre a calibração: o único parâmetro calibrado com dado real é o `rag_min_score`. O `k=3` e o
teto de 8 são valores fixos de projeto, escolhidos para limitar o tamanho da seção; não houve
experimento variando `k`. A medição de custo (ADR 0016) mostrou que o ganho não vinha dali, então
afinar `k` ficou sem prioridade.

### `rag_min_score` — calibração com dado real

`rag_min_score` é o score mínimo para um vizinho semântico entrar no prompt. O score é o cosseno
entre a fala consultada e a fala-fonte indexada: 1,0 é idêntico, 0,0 é sem relação. Só o texto na
língua de origem entra no cálculo; a tradução vai junto como metadado.

A calibração usou um índice real: 12 cenas do Breath of Fire IV traduzidas pelo pipeline e
aprovadas (323 falas, 323 vetores), e 40 consultas em 5 categorias.

| Categoria da consulta | Exemplo | Score do melhor hit |
|---|---|---|
| Texto idêntico ao do corpus | `"Monsters! They're everywhere!..."` | **1,0** (5 de 5) |
| Quase idêntico (pontuação ou aspas diferentes) | "Where do you want to go?" | 0,83–0,89 |
| Paráfrase (mesmo sentido, outras palavras) | "So what is the state of the sacrifice now?" | 0,71–0,89 (um caso em 0,57) |
| Mesmo tema, conteúdo diferente | "Take this sword, it was forged by ancient smiths" | 0,37–0,51 |
| Fora do domínio | "Preheat the oven to 200 degrees..." | 0,13–0,38 |

Leitura: acima de 0,71 os hits são paráfrases de verdade, úteis como referência. Abaixo de 0,57
eles casam só por vocabulário de tema (fantasia/RPG), sem relação de sentido. O maior score de
ruído observado foi **0,51**.

**Valor escolhido: `rag_min_score = 0.55`**, acima do teto de ruído (0,51) e abaixo do piso das
paráfrases (0,57). Fica em `projects/translation_software/project.json`; é configurável por
projeto, porque depende do par de idiomas.

Limite dessa medição: 323 falas são uma fração do corpus completo (6.046 falas). A amostra serve
para ver a **forma** da distribuição de scores, que depende só do texto, mas não mede cobertura em
produção. O modelo também só foi validado para inglês→português; para outro par de idiomas,
`tcf db validate-model` refaz a medição.

Fases e decisões de design do banco e do índice → [`DB_MIGRATION_ROADMAP.md`](DB_MIGRATION_ROADMAP.md).

---

## 5. Gate de spoiler (`_reveal_allowed`)

Vale para KB (léxico e semântico) e decisões semânticas. **Default-deny**: só entra o que é provadamente
seguro. Decisões léxicas usam gate opt-in (`_decision_reveal_ok`): sem tag `reveal`, a decisão entra.

```mermaid
flowchart TB
  h["hit com campo reveal"] --> q1{"reveal é<br/>safe / always / public?"}
  q1 -->|"sim"| ok["ENTRA no pacote"]
  q1 -->|"não"| q2{"vazio ou<br/>beyond_frontier?"}
  q2 -->|"sim"| no["BARRADO"]
  q2 -->|"não: é um scene_id"| q3{"scene_id ≤<br/>cena atual?"}
  q3 -->|"sim: já revelado"| ok
  q3 -->|"não: futuro ou incomparável"| no

  classDef good fill:#d9f2d9,stroke:#2e7d32,color:#000;
  classDef bad fill:#f6d6d6,stroke:#b03030,color:#000;
  class ok good;
  class no bad;
```

A garantia vem do dado explícito por item, não de casar texto. Consequência prática: seção de KB
sem `reveal` tagueado nunca aparece — projeto novo precisa taguear para o nº2 render algo. Hoje
nenhum projeto tem a KB marcada, então a KB semântica fica vazia em produção.

---

## 6. Degradação — o RAG nunca derruba o pacote

```mermaid
flowchart LR
  s{"projeto tem<br/>db configurado?"} -->|"não"| e1["[] silencioso<br/>modo flat files"]
  s -->|"sim"| o{"db.semantic<br/>= false?"}
  o -->|"sim"| e4["[] + aviso do kb_gate<br/>opt-out explícito"]
  o -->|"não"| m{"stack de ML<br/>instalada?"}
  m -->|"não"| e2["kb_gate BLOQUEIA<br/>(aviso com TCF_ALLOW_NO_ML, caso da CI)"]
  m -->|"sim"| f{"busca falhou?<br/>índice ausente, vec0, OOM"}
  f -->|"sim"| e3["[] + AVISO visível"]
  f -->|"não"| ok["seção semântica no pacote"]

  classDef good fill:#d9f2d9,stroke:#2e7d32,color:#000;
  classDef warn fill:#fde6c4,stroke:#c97b1f,color:#000;
  class ok good;
  class e3,e4 warn;
```

Nenhum caminho com `db` fica calado: sem a stack o `kb_gate` bloqueia antes de qualquer chamada de
modelo, o opt-out (`db.semantic: false`) aparece como aviso, e "stack presente e quebrou" avisa —
mascarar como "sem vizinhos" esconderia índice desatualizado.

---

## 7. Na execução

O laço completo de uma cena — consulta, reuso exato sem LLM, tradução, aprovação e volta para o
índice — está desenhado [abaixo](#fluxo-em-execução--o-laço-de-reuso).

Ponto que costuma confundir: **a economia medida (−24%, ADR 0016) vem do reuso exato**, que tira a
linha do LLM. Os retrievers semânticos desta página só enriquecem o prompt das linhas novas.

### Fluxo em execução — o laço de reuso

O que acontece com **uma cena** em projeto com `db`, e por onde a tradução aprovada volta para
alimentar a cena seguinte:

```mermaid
flowchart TB
  scene["cena N<br/>linhas-fonte"]
  subgraph pack["context_pack — det., só consulta (vetor pré-computado)"]
    direction LR
    ex["match EXATO<br/>tm_exact"]
    sem["TM semântica<br/>embedder.search · k=3/linha<br/>rag_min_score ≤ score &lt; 0,999<br/>máx. 8 hits"]
    kb["KB / decisões<br/>filtro de spoiler default-deny"]
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

- **Onde está a economia** (laranja): uma fala cuja fonte já foi traduzida em outra cena **não vai
  ao LLM** (`model._select_reuse`); a tradução aprovada é reusada. Uma cena 100% reaproveitada não
  faz chamada nenhuma. Foi esse caminho que rendeu a redução de 24% de custo medida em 10 cenas
  (ADR 0016). A busca semântica (roxo) só **informa** o prompt das falas novas; não corta tokens.
- **Só vira TM o que passou no round-trip.** O `build_plan` grava a tradução com `approved=0`; o
  `approve_scene` promove para `approved=1` depois do `verify`. As buscas exata e semântica só
  leem `approved=1`, então uma tradução reprovada nunca contamina as cenas seguintes.
- **O vetor nasce na aprovação.** `reindex_pending_embeddings` embeda as linhas aprovadas que ainda
  não têm vetor, logo depois do `approve_scene`. A cena N+1 já enxerga a cena N. É incremental e
  não derruba a escrita: o dado já está gravado em SQL antes da indexação.

---

## Decisões de desenho

| Decisão | Por quê | Onde |
|---|---|---|
| Vetor dentro do SQLite do projeto (`sqlite-vec`), embedding local | sem serviço externo nem 2º fornecedor pago; um arquivo por projeto | [`DB_MIGRATION_ROADMAP.md`](DB_MIGRATION_ROADMAP.md) · contexto: [ADR 0003](adr/0003-state-substrate-flatfiles-then-index.md) (vetor adiado até haver necessidade) |
| Chunking na ingestão, nunca no embedder | 1 linha = 1 vetor; kind novo é só config | [ADR 0014](adr/0014-chunking-rag-na-ingestao-nao-no-embedder.md) |
| Embedder por processo, sem daemon | isolamento entre projetos; reload aceito | [ADR 0015](adr/0015-embedder-isolado-por-processo-nao-daemon-compartilhado.md) |
| Reindex no write-path é obrigatório | índice defasado devolve vazio sem erro | [ADR 0016](adr/0016-rag-roi-validado-reindex-obrigatorio.md) |
| Semântico é suplemento rotulado | núcleo do pacote tem que ser determinístico | [`STACK.md`](STACK.md#rag-recuperação-semântica) |
| RAG **não** entra em glossário nem voice cards | match léxico é preciso; semântico traria falso-positivo | [`STACK.md`](STACK.md#rag-recuperação-semântica) |

## Linha do tempo

| Data | Marco |
|---|---|
| 2026-06-11 | precursor: retrieval por keyword reforçado no `context_pack` |
| 2026-06-29 | TM semântica (nº1) e KB com gate de spoiler (nº2) entram no pacote |
| 2026-07-05 | decisões semelhantes (#105) |
| 2026-09-09 | ROI medido (ADR 0016) e reindex no write-path (#182) |
| 2026-09-10 | `rag_min_score` calibrado com dado real (#184) |
| 2026-09-25 | leva de correções: filtro antes do top-k, gate antes do corte, linha editada fora da busca |
| 2026-10-07 | reindex movido para a aprovação da cena (fim do atraso de uma cena); FlashRank removido |
