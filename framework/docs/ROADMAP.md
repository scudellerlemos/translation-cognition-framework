# ROADMAP — evolução do framework

Prioridade declarada: (1) traduzir o jogo de forma **sustentável**, (2) eliminar o estouro de sessão,
(3) reduzir contexto/tokens, (4) viabilizar Sonnet, (5) fundações mínimas p/ evoluir. Não é "construir
a arquitetura perfeita".

## O que estava bloqueando a tradução completa

A sessão crescia linearmente com o nº de capítulos porque a tradução era feita inline e a consistência
vinha da janela (ver `adr/0002`). **Menor conjunto de mudanças** que destrava: cena como job stateless
+ context_pack limitado + estado externalizado. Isso é o **P0 (entregue)**.

## Backlog priorizado

### P0 — MVP do harness (ENTREGUE)
| # | Item | Status |
|---|---|---|
| 1 | `context_pack.py` — contexto O(cena) | ✅ |
| 2 | `state_index.py` — TM + voice cards + decision_index | ✅ |
| 3 | `model.py` — interface (Sonnet traduz / Opus verifica; in-session + api) | ✅ |
| 4 | `run_scene.py` — orquestrador determinístico + checkpoint | ✅ |
| 5 | docs/ + ADRs 0001–0004 | ✅ |
| 6 | `test_runtime.py` (determinismo, boundedness, idempotência, guard) | ✅ |

### P1 — antes de escalar (custo/observabilidade)
| # | Item | Status |
|---|---|---|
| 7 | métricas no runner (`metrics.jsonl`: tokens trad/revisão, custo/cena, back-pass-rate) | ✅ |
| 8 | endurecer caminho `api` (streaming, schema, guard `\n`+retry, backoff) | ✅ **comprovado em produção** (cap.12 16/16) |
| 8b | `run_chapter.py` — driver de capítulo (loop de cenas, resumível) | ✅ |
| 9 | benchmark de modelos (Sonnet vs Opus em cenas-gold) | ✅ **Sonnet aprovado** (ch_12_03, nível Opus-à-mão) |
| 9b | **telemetria de gasto REAL** (`api_ledger.jsonl` por chamada + `cost_report.py`) | ✅ **feito** — toda chamada cobrada conta, inclusive cenas que falham/escalam |

### P1.5 — cabear cognição no runtime (gaps da Architecture Review #2)
> Doutrina existe nas skills, mas o harness de escala não a aplica. Ver `ARCHITECTURE_REVIEW_2026-06.md`.

| # | Item | Severidade | Status |
|---|---|---|---|
| API comprovada | ligar e **comprovar** o caminho API (`.env` + benchmark) | 🔴 | ✅ **feito** — Sonnet aprovado; bugs de produção corrigidos; custo real ~$36/jogo |
| API como default | `api` como default de produção | 🔴 | ✅ **feito** — default `api` em translate/run_scene/run_chapter |
| Fase 0 / cobertura de KB | **Fase 0**: KB reconciliada + **gate de cobertura** | 🟠 | ✅ **feito** — `kb_gate.py`; Fase 0 do cap.12; `kb_frontier=12_17`. **Driver de Fase 0 ✅** (`kb_phase.py`): automatiza a parte determinista do gargalo — DESCOBRE o gap (candidatos de lore/nome que aparecem no cap. e a KB não cobre, via a MESMA primitiva `_present` do tradutor → o gap é exatamente o que o `context_pack` falharia em surfar) e escreve a worklist (**cobrança** do humano); `--check` valida cobertura (gap recorrente cross-cena fechado + `reconciled`); `--apply-frontier` avança `kb_frontier`. Governança preservada: IA **propõe** → humano **reconcilia** (skill 03) → script **valida/aplica**; NÃO pesquisa sozinho. Auditou o cap.13 e achou 3 termos recorrentes fora do glossário (Mystery Twins / Imperial Guard / Twin Shields). |
| Controle de spoiler | **spoiler**: `spoiler_ledger.json` + **filtro temporal** + regra de gênero | 🟠 | ✅ **feito** — ledger + filtro no `context_pack`; Carta atualizada |
| Bundle de custo | bundle de custo (dedup TM/intra-corpus, ~~slim de schema~~, batch API) → ~$36→~$15 | 🟡 | **parcial**: effort/thinking já cortou ~5×; **dedup por TM ✅** (linhas com fonte já traduzida em outra cena não vão ao modelo — corta tokens de saída; medido 2,8% no cap.12 sobre TM cap.11+12, **cresce com o corpus**; guard de paridade + nunca reusa a própria cena; desligado no escalonamento). **slim de schema: REJEITADO por qualidade** (ver abaixo). **cache da Carta: observável, BECO SEM SAÍDA** ✅ (medido cap.13: Carta ~1.3k tok, custa $0,14 vs output $3,41; com cache_control fica até levemente net-negativo pois o batch paraleliza e re-escreve ~27×; cache perfeito é impossível no batch e economizaria só $0,12/cap). **batch API ✅ comprovado vivo** (cap.13 9/9; −50% real; resume idempotente; re-batch acumulativo entre rodadas). **tiering por complexidade ✅ codado** (linhas SEM `\n` → Haiku −67%/linha; COM `\n` → Sonnet; benchmark: voz do Haiku no nível do Sonnet inclusive registro arcaico, mas Haiku derrapa na paridade de `\n` em escala → o split dribla a fraqueza; só no batch; falta run viva tiered p/ medir). **back-translation em BATCH ✅ codado** (Tier 1: a back-translation Opus — passo mais caro/linha, $25/M de saída — vira PÓS-PASSE do capítulo; `batch_back_translate` coleta as linhas high/critical de todas as cenas verificadas e roda 1 batch −50%; `run_chapter --batch` difere a back-translation por cena e batcheia ao fim; resume idempotente; report-only, não bloqueia; ledger marca `batch=True`. Falta run viva p/ medir). |

> **slim de schema — REJEITADO (não tentar de novo).** Decisão registrada e fechada como "not planned"
> em [issue #111](https://github.com/scudellerlemos/translation-cognition-framework/issues/111)
> (cortar `tone_register`/`intent` do schema quebraria o gate de qualidade e a única cognição
> estruturada por linha com o thinking desligado).

**Validação Etapa 6 (cap.12 headless):** **16/16** cenas `verified` ponta-a-ponta (round-trip byte-idêntico,
back-translation via API). Pipeline endurecido em ~2300 linhas reais (schema-array, custo, `\n`,
paridade, cobertura-merge, retry de conexão, budget best-effort).

**Telemetria de gasto (gap revelado pela produção — RESOLVIDO):** o `metrics.jsonl` era resumo
SO-DE-SUCESSO (1 linha por cena que fechou no verify) → perdia o que **falhou depois de já cobrar a API**
(cobertura estourou → exceção; verify reprovou), cada **re-tradução do escalonamento** (1.40→1.15→1.0) e
**back-translations que quebraram no parse**. Por isso a estimativa (~$9–10) ficou abaixo do real (~$15).
**Conserto:** `model.log_api_call` grava `api_ledger.jsonl` (1 linha por chamada CONCLUÍDA, **antes** de
qualquer parse/gate) → captura TODA chamada cobrada. `cost_report.py` agrega (total, por modelo/tipo/cena)
e cruza com `run_state.json` p/ marcar gasto **desperdiçado** (cenas que não fecharam `verified`).
`run_chapter` imprime o resumo de gasto ao fim **e na parada por falha**. O `cost_usd` do `metrics.jsonl`
agora vem do ledger (soma retries+escalonamento). _O ledger começa do zero nesta instrumentação — runs
anteriores do cap.12 não estão nele (não há como recuperar honestamente do resumo subcontado)._

**Run viva do cap.14 (1ª medição real de batch/tiering/back-batch — "codado ≠ medido"):**
- 🐛 **bug do tiering (corrigido):** `custom_id = scene@@tier` é inválido na Batch API
  (`^[a-zA-Z0-9_-]{1,64}$`) → o batch dava **400** e caía 100% pro interativo **full-price**. Os unit
  tests não pegavam (o fake aceitava qualquer id). Fix: `@@`→`__`; o fake agora **valida o padrão**.
- ✅ **back-batch −50% Opus comprovado VIVO** (cap.14, 9 cenas, 5 revisadas num batch). Funciona.
- 🐛🐛🐛 **batch −50% no translate NÃO convergia — CAUSA-RAIZ REAL = 400 do Haiku no tier cheap (cap.15):**
  as **9/9 cenas** deram `coverage_failed` → 100% interativo **full-price** ($22 Sonnet). Caça em camadas
  (ledger por timestamp → repro offline → diagnóstico vivo de 1 cena → **composição do pack**): o
  `_translate_params` (usado pelo batch) **sempre incluía `output_config.effort`** — mas **Haiku 4.5 dá 400
  com `effort`** → **todo request do tier cheap (single-line → Haiku) falhava** (não logado) → as linhas
  single-line nunca voltavam. Pista decisiva: no 15_06, `MISSING=120/221` = **exatamente as 120 linhas do
  tier cheap** (o tier main/Sonnet cobriu suas 101 sem problema). O `_api_translate` (interativo) **checa
  `_no_effort_model` e omite o effort** p/ Haiku; o batch não checava. **Fix** (`model.py`): `_translate_params`
  omite `effort` p/ Haiku/Sonnet-4.5 (espelha o interativo). **Validado OFFLINE**: o fake do batch agora
  **rejeita `effort` em request Haiku** (mimetiza o 400) — `test_batch_tiering_routes_models` **falha no
  código antigo** e passa no novo; 45 testes verdes. **Defesa extra mantida** (`_BATCH_CHUNK`=60 + merge
  best-parity): protege contra truncação real de resposta longa em cenas grandes. ✅ **CONFIRMADO VIVO
  (15_06, run de 1 cena):** convergiu `written` com **5 requests batch=True** (3× Haiku tier cheap + 2×
  Sonnet tier main), custo **$0,1484** — pela 1ª vez o translate fecha NO batch (−50%) **e o tiering Haiku
  engata** (as 120 single-line que antes davam 400). Mesma cena no interativo full-price custava ~$0,40–0,64
  → ~65% mais barato.
- ✅✅ **CONFIRMADO EM ESCALA DE CAPÍTULO (cap.16, 1ª run de cap. com tudo consertado):** **5/5 cenas
  `written` no batch → verified** (round-trip idêntico), **ZERO fallback interativo** (46/46 translate em
  batch=True: 26 Haiku + 20 Sonnet), chunking segurou a cena de **1.334 linhas** (16_01). **Custo: $1,4154**
  (delta do cap.; teto `--max-usd 3` não chegou perto) — vs ~$6,5 se rodasse com o bug (≈78% mais barato).
  **Tiering MEDIDO:** Haiku $0,32 **ativo** (estava congelado $0,71 por 2 caps). Previsão ($0,0007/linha →
  ~$1,46) cravada no real ($1,42). **Bundle de custo fechado: batch −50% + tiering + back-batch + guardrails de custo
  todos vivos e medidos.** > **NB metodológico (3 diagnósticos até
  acertar):** (1º) "faltava nota corretiva", (2º) "re-mandar fragmento vs cena inteira", (3º) "truncação" —
  todos passavam no fake mas o **run de 1 cena (~$0,30) reprovava ao vivo**. Só a composição do pack
  (`MISSING == nº de single-line`) fechou o caso. **Lição forte: validar a mecânica de batch num run de 1
  cena ANTES de pagar capítulo — e o fake deve VALIDAR as restrições reais da API (custom_id, effort-por-modelo).**
- ✅ **mitigação do risco "mock↔API diverge" (`batch_smoke.py`):** a lição acima virou ferramenta — smoke
  vivo (~$0,02, ~min) de 1 cena de 2 linhas (1 Haiku + 1 Sonnet) pela API REAL; afirma os 4 invariantes
  (submete sem 400, converge `written`, AMBOS os tiers ao vivo, zero fallback). **Rodar ANTES de cada
  capítulo pago** (`python framework/runtime/batch_smoke.py`). A lógica de avaliação (`evaluate`) é testada
  offline (pega os 4 modos de divergência que já custaram dinheiro). É o teste de contrato que faltava
  entre o mock e a API real.
- ✅ **tiering: causa do "$0,71 inalterado" ERA O BUG DO HAIKU, não falta de single-line.** A hipótese
  antiga ("o jogo pode não ter single-line suficiente → desligar `MODEL_TRANSLATE_CHEAP`") estava **errada
  e invertida**. Medição em **44.116 linhas** (`_tier_of` sobre todos os dialogs): **59% são single-line
  (Haiku-elegíveis)** — 26.004 cheap vs 18.112 main, consistente em TODOS os caps (56–67%). O Haiku ficava
  em $0,71 porque **todo request Haiku dava 400** (effort, corrigido hoje), não por falta de conteúdo.
  **Confirmado vivo (15_06):** 132 linhas single-line foram pro Haiku (3 requests). **Disposição: MANTER o
  tiering** (cobre 59% do jogo; Haiku = 1/3 da saída do Sonnet). ⚠️ **Falta só** o número AGREGADO de
  economia num capítulo inteiro (o 15_06 prova o roteamento; o $ total sai na próxima run de capítulo).
- 🐛 **falso-positivo no KB-gate (corrigido):** "Like/Hold/Papa" (palavras comuns no início de frase)
  bloqueavam a Fase 0 do cap.15 por escaparem da stoplist do `kb_phase`. Adicionadas ao `_STOP`.
- 💰 **custo real medido (2 caps):** cap.14 ≈ $8,5; cap.15 ≈ **$23** (2525 linhas, **full-price** pelo bug
  acima) → ~$117/33k **sem** o desconto. O **$36/jogo era otimista**; só o fix do batch (a validar vivo)
  reaproxima disso.

### P1.6 — robustez de conector p/ cenas de binário apertado (BACKLOG pós-produção)
> Disparado pela ch_12_15: binário multi-BIN com pouco espaço de realocação → 2 linhas (+4/+5 bytes)
> caem em RELOC_cont → ponteiros fora-do-arquivo. As traduções estão boas; o conector é que não cabe.
> **Decisão: backlog pós-produção** (não overengineer; a Fase D / QA in-game cobre casos isolados).

| Parte | Item | Esforço | Risco | Status |
|---|---|---|---|---|
| **3A** | self-heal por aperto de budget: `run_scene` escala `BUDGET_TOLERANCE` 1.40→1.15→1.0 e re-traduz só na falha de fitting | ~1 dia | baixo | ✅ **feito** (escalonamento de fitting) |
| **3B-fix** | verify: out-of-file era **FALSO-POSITIVO** (coincidências `50 00` no bytecode apontando cross-file, ex.: p/ 31_02_000S.BIN) — agora compara com baseline do ORIGINAL (só conta o que o reinsert INTRODUZIU) | ~2h | baixo | ✅ **feito** (`verify_chapter.py`) |

**Resolução 12_15 (CONFIRMADO):** o reinsert sempre esteve correto (95/95 linhas, round-trip idêntico,
+32 bytes). Os 2 "ponteiros fora-do-arquivo" **existem no binário ORIGINAL intocado** e apontam p/ um
arquivo de OUTRO capítulo (cap.31) — coincidências de bytes `50 00` no bytecode, não ponteiros de texto.
A verify agora subtrai o baseline → **12_15 verified (16/16 do cap.12)**. Não foi preciso 3B real
(realocação de conector). Caveat: a tradução da 12_15 ficou na tolerância 1.0 (mais justa que o normal)
porque a escalada rodou antes do fix — re-traduzir a 1.40 (~$0.15) recupera naturalidade, opcional.

### P1.7 — custo de onboarding de novo jogo (BACKLOG — pós-piloto Souldiers)

> Observação medida no onboarding do Souldiers (jul/2026): ~40k tokens gastos só na Fase 0 —
> investigação de arquivos, iterações no conector, correção de schema KB, debug do context_pack.
> Nenhum token gerou tradução. O gasto é evitável com scaffolding + validação precoce.

| # | Item | Impacto estimado | Status |
|---|---|---|---|
| A | **`scaffold_project.py`** — gera skeleton com schema correto (glossary.csv com colunas certas, tone_analysis.md com `### Speaker — voice_criticality:` placeholder, decision_log.md template). Zero iteração de "schema errado". | ~10k tok/jogo | ✅ |
| B | **Validação early em `state_index.build()`** — se glossary/tone_analysis não tiverem o formato esperado, falhar com mensagem clara em vez de retornar silenciosamente 0 cards/0 decisões. | ~3k tok/jogo | ✅ |
| C | **Connector template por família de engine** — Unity Addressables é engine conhecida. Novo jogo Unity = template configurável (bundle paths, CSV columns), não reescrita. Para engine desconhecida: `connector_smoke.py` (smoke test round-trip por iteração) + `script_generator.py` com 3 padrões de stub pré-preenchidos (linear_scan/token_table/pointer_table) baseados nas evidências do `discover.py`. | ~15k tok/jogo | ✅ |
| D | **KB research como skill estruturada** — skill que recebe título do jogo + URL wiki e produz artefatos já no formato correto (glossary.csv + tone_analysis.md com `###` voice cards), em vez de fork ad-hoc + iterações de correção de formato. | ~8k tok/jogo | ✅ (skill 04 atualizada) |
| E | **`kb_fetch.py` + `kb_build_ollama.py` + `kb_reconcile.py`** — pipeline híbrido para KB sem custo de API: `kb_fetch.py` baixa fontes e `kb_build_ollama.py` usa Ollama local para extração factual por entidade (rascunho `draft_ollama`); `kb_reconcile.py` promove pra `reconciled` só após ratificação humana (`kb_ratified.csv`). Elimina a leitura/extração de texto bruto da sessão Claude, sem abrir mão da reconciliação humana obrigatória. Ver nota abaixo. | ~30k tok/jogo | ✅ |
| F | **`split_scenes.py`** — gap achado no onboarding do Trails Sky SC (2026-08-23): `run_scene`/`build_plan_chapter` exigem `artifacts/scenes/<cena>/dialogs.csv` (contrato congelado, `paths.py`), mas `extract.py` de todo conector só escreve o `dialogs.csv` FLAT — não havia nenhuma ferramenta genérica no framework pra fazer essa ponte; BoF4/Souldiers/Utawarerumono resolveram isso ad hoc, fora do framework versionado. Escopo deliberado: só cobre o caso em que 1 coluna do corpus já identifica a cena 1:1 (`--by file`, padrão do BoF4/Trails Sky SC) — Souldiers (prefixo no offset) e Utawarerumono (`extract.py` já roda 1×/cena) continuam fora do escopo, não força um contrato que os 3 não compartilham. `framework/runtime/split_scenes.py` + `test_split_scenes.py` (4 testes); documentado em `NEW_PROJECT_ONBOARDING.md` (passo 2b). | — | ✅ |

> **Nota E — fontes de KB aceitas pelo `kb_fetch.py`:**
> O humano pode passar qualquer tipo de fonte — o fetch tool deve normalizar tudo para texto
> plano antes de entregar ao Ollama:
> - **URL de site/wiki** — urllib/requests + extração de texto (strip HTML)
> - **PDF** — pdfplumber ou PyMuPDF → texto plano
> - **Word (.docx)** — python-docx → texto plano
> - **Excel (.xlsx)** — openpyxl → tabela CSV/texto plano
> - **Arquivo local qualquer** — leitura direta se já for .txt/.md; conversão nos demais
>
> Interface: `python kb_fetch.py <fonte_1> [fonte_2] ...` onde `<fonte>` é URL ou caminho local.
> Saída: `artifacts/research_cache/<hash_fonte>.md` (texto normalizado, um arquivo por fonte).
> O `kb_build_ollama.py` lê o cache sem saber se a origem era web ou arquivo local.
>
> ✅ **Implementado (2026-07-03).** `kb_fetch.py`: URL (stdlib `urllib` + `html.parser`, zero dep
> nova), PDF/.docx (lazy-import `pdfplumber`/`python-docx`, `requirements-kb.txt` opcional/fora da
> CI, `RuntimeError` claro se faltar), .xlsx (`openpyxl`, já em `requirements-dev.txt`), teto de
> 10 MB/fonte. `kb_build_ollama.py`: 1 chamada Ollama por entidade de `entities.csv`
> (`importance: main/secondary` — não extrai entidade nova, doutrina "não inventar"), JSON schema
> estrito via `ollama_client._chat(fmt=...)`.
>
> ⚠️ **Ressalva de governança (não é opcional, é o design):** `kb_build_ollama.py` escreve
> `research_log.md`/`universe_knowledge_base.md` sempre com **`status: draft_ollama`** — NUNCA
> `reconciled`. `kb_gate.py` já bloqueia rascunho não-reconciliado sem nenhuma mudança (a regex de
> status não casa `draft_ollama`). A Fase 1B (reconciliação IA+humano) da skill 03 continua
> obrigatória e manual — o Ollama só substitui a leitura/extração bruta de texto das fontes, nunca
> a decisão de tier/confiança/reconciliação (mesmo princípio de [[kb-reconciliation-mandatory]] e do
> gate de `kb_review.py --strict`: a IA nunca propõe E aprova a própria KB sozinha). `confiança` do
> Ollama é travada por schema em `low|medium` — `high` é estruturalmente impossível antes de
> reconciliação humana (mesmo se o modelo "alucinar" o valor, `_clamp_confidence` rebaixa p/ `low`).
> Testes: `test_kb_fetch.py` (8), `test_kb_build_ollama.py` (9).
>
> ✅ **Fechamento do loop (2026-07-03) — `kb_reconcile.py`.** A ressalva acima deixava a promoção
> `draft_ollama → reconciled` só "manual/via sessão Claude", sem mecanismo formal. `kb_reconcile.py`
> fecha isso reusando `kb_ratified.csv` (mesmo arquivo/coluna que `kb_review.py --strict` já usa —
> nenhum formato novo): `check()` lista as entidades do rascunho com conteúdo afirmado (`found=true`,
> ≠ UNSOURCED) ainda sem linha em `kb_ratified.csv`, e avisa se a seção "Conflitos Resolvidos" do
> `research_log.md` ainda está no placeholder literal do rascunho (tripwire barato contra promover
> sem revisar nada). `promote()` só flipa `status: draft_ollama → reconciled` +
> `human_input: pending → confirmed` se `check()` estiver limpo; caso contrário recusa (`exit 1`),
> sem alterar nada. UNSOURCED nunca bloqueia (nada foi afirmado, nada a ratificar). `kb_gate.py` **não
> mudou** — a regex de status já bloqueia qualquer coisa ≠ `reconciled`, incluindo `draft_ollama`,
> sem necessidade de alteração. `kb_fetch.py` ganhou `--found-por {ia,usuario}` (default `ia`),
> gravado como `encontrada_por:` no front-matter do cache e refletido na coluna "Encontrada por" do
> `research_log.md` — restaura a distinção que a skill 03 (Fase 1A/1B) precisa pra tiering de fonte,
> sem reconstruir a comparação de conteúdo IA×humano da Fase 1B (deliberadamente fora de escopo).
>
> **Hardening pós-revisão adversarial (2026-07-03):** 2 achados reais corrigidos. (1) `_STATUS_RE`
> era frouxa (`status[:*\s]+valor` casava em qualquer lugar do texto, ex.: "o status social do
> personagem" também batia) — agora ancorada em início de linha + negrito exato
> (`^\*\*Status:\*\*`), igual ao formato que `promote()` escreve; `promote()` também confere que a
> substituição realmente mudou o arquivo antes de reportar `promoted: True` (nunca mais sucesso
> falso). (2) o tripwire de "Conflitos Resolvidos" só checava a AUSÊNCIA do placeholder — um "xxx"
> qualquer passava; agora exige um mínimo de conteúdo substantivo (`_MIN_CONFLICTS_CHARS`), não
> valida qualidade semântica (exigiria modelo, fora de escopo) mas mata o caso mais preguiçoso.
> Testes: `test_kb_reconcile.py` (11, inclui `--found-por`, decoy de status, tripwire trivial e
> chamada dupla de `promote()`).

> **Lição do Souldiers:** o maior gasto individual foi C (investigação de engine + iterações do conector).
> D1 (`discover.py`) resolve a classificação; falta o template que usa o resultado.
> O segundo maior foi A+B juntos (schema errado descoberto tarde = re-fazer o que deveria estar certo desde o início).

### P2 — quando amadurecer (reuso/escala 40–100k)

→ ver [Project #4](https://github.com/users/scudellerlemos/projects/4), issues
[#104](https://github.com/scudellerlemos/translation-cognition-framework/issues/104) (multi-projeto/paralelismo)
e [#105](https://github.com/scudellerlemos/translation-cognition-framework/issues/105) (RAG sobre `decision_log`
— KB/lore já ativo, ver Fase 3 do `DB_MIGRATION_ROADMAP.md`).

### P2.5 — Maturidade de execução (paralelismo, orquestração, observabilidade)
> Gap reconhecido: o roadmap tratava "paralelizar cenas" como uma linha vaga. Esta seção torna explícito
> o que é maturidade de processo aqui — e, principalmente, o **constraint** que limita o paralelismo.

**Nuance que muda a prioridade:** o paralelismo que custa **dinheiro** (chamadas de LLM) **já existe** —
`run_chapter --batch` submete todas as cenas do capítulo num **batch único** (Batch API processa
concorrente). O resto (`build_plan`, `verify`, rebuild de `state_index`) é Python local e barato.
Logo "paralelizar execução" é alavanca de **latência/throughput e operabilidade**, NÃO de custo.

**O constraint (a espinha sequencial):** a **consistência vem da TM acumulando em sequência** — cena N
entra na TM, cena N+1 faz dedup e herda voz/termos. Paralelizar cegamente perde dedup + propagação de
consistência. **Mas** o batch já abre mão disso DENTRO do capítulo (traduz com a TM do início do cap.; a
consistência intra-cap. vem do glossário/KB da Fase 0 + Carta). Portanto a espinha sequencial é **por
capítulo, não por cena** — a TM só importa cross-capítulo.

| Dimensão | Estado | Gap | Quando |
|---|---|---|---|
| paralelismo de LLM | ✅ via batch | nenhum (é o que importa em $) | — |
| **orquestração ponta-a-ponta** | ✅ **feito (2026-07-03)** | `run_game.py`: descobre capítulos (`ch_<N>_*`) ou modo flat (`--scenes-glob`, rótulo `"full"`); `--max-usd` GLOBAL encolhe entre capítulos; resumível de graça | — |
| observabilidade de progresso | ✅ **feito** | `progress_report.py`: % do jogo, linhas/min, ETA, taxa de falha — puro (elapsed_s externo) | — |
| rebuild de `state_index` | ✅ **feito** | `run_scene.rebuild_index` (default True); `run_chapter` passa `False` em batch + 1 rebuild pós-capítulo (`_rebuild_index_phase`) | — |
| fault-tolerance/resumo | ✅ decente (`run_state` + batch idempotente) | — (já maduro) | — |
| pipelining (overlap do wait async) | ❌ | enquanto o batch do cap N processa (~min), fazer o local do cap N-1 / submeter cap N+1 | plataforma (P4) |
| paralelismo cross-capítulo | ❌ | trade-off de TM documentado (perde dedup/consistência por throughput) | plataforma (P4) |
| multi-projeto | ❌ | generalizar `state_index`/paths por projeto | plataforma (P4) |

**Decisão (anti-overengineering):** p/ ESTE jogo (~33k linhas, ~3–4h wall-clock total), fila/pipelining é
overengineering. **Feito (2026-07-03):** `run_game` driver + `progress_report` + rebuild 1×/capítulo —
tudo offline (orquestração sobre o `run_chapter` que já existe), tira o humano do "invocar cap. a cap.".
Testes: `test_run_game.py` (5), `test_progress_report.py` (5), `test_batch_mode_rebuilds_state_index_once_per_chapter`
+ 2 em `test_run_scene.py`. **Fica p/ P4 (plataforma, vários jogos):** pipelining, paralelismo cross-capítulo,
multi-projeto — ver [issue #104](https://github.com/scudellerlemos/translation-cognition-framework/issues/104).

### P3 — não fazer agora (overengineering)
Decisão registrada e fechada como "not planned" em
[issue #110](https://github.com/scudellerlemos/translation-cognition-framework/issues/110)
(banco relacional pesado, knowledge graph, fila/broker, multi-agente "de serviços").

### P4 — Pós-produção & hardening (PRIORIDADE, **depois** de entregar o jogo)
> Decisão: **entregar primeiro** (traduzir tudo → build → QA → release); só então o hardening. A maioria
> destas dívidas só "morde" quando algo **muda** (conector novo, rename) — por isso ficam após produção.
> **Exceção:** o item de spoiler (Spoiler observável) tem risco **durante** a produção (a mitigação por-linha segue ativa;
> o que fica pra cá é o teste sistemático de não-vazamento).

**Entrega do jogo (fases C–F):**
| Fase | Item |
|---|---|
| C | **build jogável** — reinserir o jogo INTEIRO traduzido + patch final (não só caps isolados) |
| D | **QA in-game** humano — overflow / quebra / spoiler vazado |
| E | **revisão holística de consistência** — cross-capítulo (voz/lore/termos) sobre o corpus inteiro |
| F | **release** — patch + docs de instalação |

**Hardening arquitetural (dívidas conhecidas — ordem de ataque sugerida):**
| # | Dívida | Fix | Status |
|---|---|---|---|
| Saída estruturada do conector | fronteira do conector **stringly-typed** (`run_scene` dá grep no stdout do conector p/ decidir escalonamento) | **protocolo de saída estruturado** (exit codes + JSON de status) | ✅ **feito** — `verify_chapter` emite exit 0/1/3 + linha `VERIFY_STATUS:{json}`; `run_scene` usa o exit-code (grep morto). Bug latente corrigido: o grep procurava `"fora do arquivo"` (espaços) vs `"fora-do-arquivo"` (hifens) → out-of-file nunca escalonava |
| Fonte única de paths | contrato de nomes de artefato espalhado por ~18 arquivos | **módulo único de paths/contrato** | ✅ **feito** — `paths.py` (módulo leaf, fonte única); 42 call sites migrados em 8 módulos; `test_paths_contract` fixa as strings; NAMING.md aponta |
| run_scene coeso | `run_scene` acretando responsabilidade (hoje 492 linhas, era ~300 quando documentado) | extrair **quando cruzar o limiar de leitura** (não o split-em-6 do GPT) | ✅ **feito (2026-07-03)** — extraídas as 3 funções de housekeeping/diagnóstico (`clean_failed_scene`/`prune_discontinued`/`_check_stale`, todas pós-`run_scene()`, sem relação com o fluxo de tradução) para `scene_lifecycle.py` novo; `run_scene.py` caiu de ~510 → 442 linhas e reimporta os nomes (mesmo padrão de re-export de `model.py`/`back_translate.py`) — nenhum caller mudou, os 26 testes de `test_run_scene.py` passam sem alteração |
| Repro: gate ≠ geração | "reprodutível" com asterisco | doc: *gates* reprodutíveis ≠ *tradução* reprodutível | ✅ **feito** — ARCHITECTURE.md: "o veredito reproduz; a geração não" |
| Profundidade da Fase 0 | Fase 0 meio-cabeada ("reconciled" = marcador, não garantia de qualidade) | cabear a **profundidade** da reconciliação no runtime | ✅ **feito (2026-07-03)** — `kb_gate.py` generalizou a exigência de ratificação humana por entidade (`kb_ratified.csv`) para QUALQUER `research_log.md` com `status: reconciled`, não só o caminho `draft_ollama` do `kb_reconcile.py`. Toda entidade com conteúdo afirmado (≠ UNSOURCED) no `universe_knowledge_base.md` agora exige uma linha em `kb_ratified.csv`; bypassável via `--skip-kb-gate` como qualquer `problem` (soft, não quebra continuidade de projetos já em produção). **Escopo deliberadamente reduzido**: o tripwire de conteúdo mínimo em "Conflitos Resolvidos" do `kb_reconcile.py` NÃO foi generalizado — um projeto sem nenhum conflito de verdade (fonte única) é um caso legítimo que só o placeholder EXATO do `kb_build_ollama.py` consegue distinguir de "não revisado"; não generaliza sem uma âncora textual conhecida. **Custo aceito**: Utawarerumono/BoF4/Souldiers (as 3 KBs já reconciliadas) agora mostram esse `problem` novo até serem ratificadas por entidade — não bloqueia trabalho já feito, só torna visível o que faltava. Testes: 3 novos em `test_kb_gate.py` |
| Spoiler observável | spoiler pouco observável (ledger incompleto = vazamento silencioso de gênero pt-BR) | **teste sistemático de não-vazamento** | ✅ **feito (parcial)** — `spoiler_check.py`: contraparte OBSERVÁVEL do guard preventivo; flagra nome/título pós-reveal vazando pré-reveal (`forbidden_pre_reveal` no ledger); auditoria dos caps 11–18 LIMPA; teste de regressão sobre as traduções commitadas. ⚠️ extensão de gênero rastreada em [issue #106](https://github.com/scudellerlemos/translation-cognition-framework/issues/106) |

**Riscos de engenharia (avaliação crítica — mitigações offline):**
| # | Risco | Mitigação | Status |
|---|---|---|---|
| Mock↔API diverge | **mock↔API diverge** (3 bugs de batch passaram no fake e queimaram dinheiro) | smoke vivo de contrato | ✅ **feito** — `batch_smoke.py` (ver Bundle de custo acima) |
| Piso de qualidade | **sem piso de qualidade** — verdict `revise` report-only + 59% (tier Haiku) sem crivo nenhum | gate observável + amostragem + correção dirigida | ✅ **feito (3 camadas)** — (a) `quality_gate.py` lê os `verdict: revise` + flagra high/critical sem cobertura + **métrica de cobertura** (% das linhas com crivo); (b) `model.sample_low_risk_lines` ~5% determinístico das low/medium entra na back-batch → piso medido p/ o Haiku (liga dos próximos caps); (c) `quality_fix.py` re-traduz dirigido os `revise` (worklist do `--export` = dado; reusa `retranslate_offsets`+merge; corrige translations+plan). 1ª execução: **134 `revise`** nos caps 11–19 (incl. corrupção crua de 5872 chars em ch_19_04) |
| TM append-only | **TM append-only** — termo errado propagado por N capítulos sem ferramenta de correção | correção governada cross-capítulo | ✅ **feito** — `tm_correct.py`: find→replace a partir de CSV de **dados**, match por limite de palavra, corrige translations+plan, dry-run por padrão. Dry-run real achou "paragon" em ch_12_04 **e** ch_14_10 |
| Vazamento de gênero | **vazamento de GÊNERO pt-BR** (ele/ela onde o EN é neutro) — o que o `spoiler_check` de nomes NÃO pegava | contraparte observável de gênero | ✅ **feito** — `spoiler_check.check_gender`: campo `gender_quarantine` no ledger + heurística de co-ocorrência (marcador de gênero pt-BR junto a entidade pré-reveal). Mecanismo ativo; marcação real aguarda caso confirmado por fonte (não fabricar spoiler = não recair em "IA reconcilia a própria KB") |
| IA reconcilia a própria KB | **a IA reconcilia a própria KB** (sem segundo par de olhos no delta) | gate de fonte (hard) + ratificação humana | ✅ **feito (gate)** — `kb_review.py` + `kb_phase --check`: FALHA (hard) se entidade nova não citar **fonte** no research_log (âncora externa checável = mata "IA propõe E aprova"). `--strict` exige **ratificação humana** (`kb_ratified.csv`, só o humano edita) + gênero confirmado. Evoluiu de digest → gate |
| Gênero pt-BR inativo | **gênero pt-BR inativo** (mecanismo pronto, zero entidades marcadas) | pesquisa + resolução com fonte | ✅ **feito** — faixa 11-19 auditada (wiki): NENHUM gender-spoiler (o twist é Haku→Oshtor = identidade, já no ledger) → `gender_quarantine` dormente por estar CORRETO, documentado. Shichirya→MASCULINO, Honoka→FEMININO (com fonte); restantes flagrados no `--strict` p/ ratificação (não-fabricado) |
| Auditoria de gênero dependia de lembrar rodar | **`spoiler_check.check_gender` só existia como CLI manual** (`python spoiler_check.py <projeto>`) — foi assim que Uta foi auditado (caps 11-19), mas o Souldiers nunca chegou a ser, porque depende de alguém lembrar de rodar. Mesma classe do gap de `onboarding-scaffold-kb-gate-drift` (fase "pronta" sem gate automático) | cabear como passo OBRIGATÓRIO e automático do pipeline, sempre, com resultado persistido | ✅ **feito** (2026-07-03) — `spoiler_check.audit_and_persist(root)` roda `check()` (vazamento de nome/título, alta confiança) + `check_gender()` (heurística, pode ter falso-positivo) sobre o **projeto inteiro** e grava `artifacts/spoiler_audit.json`. `run_chapter._audit_spoiler` chama isso **incondicionalmente** ao fim de todo capítulo (ao lado do `_export_qa`), report-only (nunca bloqueia), com aviso alto/baixo diferenciado por confiança. Não depende mais de ninguém lembrar de rodar o CLI. Teste: `test_complete_persists_spoiler_audit` |
| Contador de batch engana | **`request_counts.succeeded` não reflete progresso real durante `in_progress`** (batch de 146 requests ficou 0/146 por 111min; cancelar por achar travado matou 12 já quase prontas — 134/146 tinham sucedido de verdade) | ferramenta de checagem honesta, nunca cancela sozinha; polling loga status periódico | ✅ **feito** — `batch_status.py`: reporta status/idade/counts de qualquer batch in_progress com o aviso embutido na própria saída ("não cancelar por contador zerado"); cancelamento continua manual e deliberado (`client.messages.batches.cancel`). `_await_batch` (llm_client.py) agora loga a cada ~5min em vez de silêncio total. Ver `anthropic-batch-progress-unreliable` (memory) |
| Batch gigante = risco concentrado | **1 batch de back-translation com 146 requests** ficou lento (motivo real não identificável do nosso lado — conteúdo de cada request era pequeno, nada anômalo); esperar/cancelar um batch gigante é tudo-ou-nada | segmentar em vários batches menores + timeout curto (report-only não é crítico) | ✅ **feito (as 2 pontas)** — `batch_back_translate` (back_translate.py) divide requests em chunks de `chunk_size=40`, cada 1 um batch **separado**; `max_wait_seconds` default caiu de 24h → **2h** (report-only, não vale esperar o SLA inteiro). Teste: `test_batch_back_translate_segments_large_batches`. **`batch_translate` (tradução, a op CRÍTICA) também segmentada agora** (2026-07-03): `_TRANSLATE_SUBMIT_CHUNK=40` (config.py) fatia as requisições de cada rodada em batches separados via `_submit_translate_chunk`; um chunk que trava/estoura o timeout só fica sem cobertura DELE — a rodada seguinte re-tenta o que faltou (não aborta mais o batch inteiro no 1º timeout, como fazia antes). Teste: `test_batch_translate_segments_large_submissions`. |

**Piso de qualidade HUMANO (supera a auto-avaliação por IA — `quality_review.py`):**
A back-translation (Opus julgando Sonnet/Haiku) custa e não substitui um humano lendo o pt-BR. O fluxo
human-in-the-loop fecha o nº 2 na raiz, governança *humano propõe → gate aprova → script aplica*:
`export <cap>` gera **1 CSV com o capítulo inteiro**, cada linha **marcada deterministicamente** (sem IA)
na coluna `revisar` — `risco:high/critical`, `amostra` (5% do Haiku), `identico-fonte` (provável
não-traduzido), `tamanho` (outlier), `pt-PT?`. O humano preenche `correcao` (texto certo → aplicado
**verbatim, 0 IA**: só charset/paridade/round-trip) ou `nota` (instrução → IA re-traduz **só aquela
linha**). `apply` processa exatamente o devolvido. Mede no cap.19: 4196 linhas, 691 marcadas (391 high +
199 amostra + 77 idêntico-fonte + 37 critical). Custo de aplicar uma revisão verbatim = **$0**.

**Evolução da camada de conector (norte de "plataforma" — PRIORIDADE pós-produção):**

→ ver [Project #4](https://github.com/users/scudellerlemos/projects/4), issues
[#107](https://github.com/scudellerlemos/translation-cognition-framework/issues/107) (registry por
família de engine — gatilho de 2-3 conectores já atingido: BoF4+Uta+Souldiers) e
[#108](https://github.com/scudellerlemos/translation-cognition-framework/issues/108) (síntese agêntica
de conector novo via round-trip como oráculo).

## Fases

- **Fase 1 — resolver estouro de sessão:** P0 (entregue). Cena stateless + contexto limitado.
- **Fase 2 — reduzir custo operacional:** P1 (entregue e **comprovado em produção**: métricas + API
  endurecida + `run_chapter` + benchmark Sonnet aprovado + telemetria de gasto real via `api_ledger.jsonl`).
- **Fase 2.5 — cabear cognição no runtime:** P1.5 (riscos de cognição). Ligar/comprovar API, KB-gate, spoiler-filter,
  bundle de custo. **É aqui que estamos.**
- **Fase 2.7 — maturidade de execução:** P2.5. Orquestração ponta-a-ponta (`run_game`) + observabilidade
  de progresso + rebuild de state_index 1×/capítulo (barato, agora). Paralelismo de LLM já resolvido (batch);
  pipelining/cross-capítulo ficam p/ plataforma.
- **Fase 3 — escalar p/ 40–100k linhas:** P2. Paralelização + (se preciso) RAG sobre lore/decisões.
- **Fase 4 — pós-produção & plataforma:** P4. Entregar o jogo (build → QA in-game → consistência →
  release), depois o hardening arquitetural e a evolução da camada de conector (detecção + síntese governada).

## Sonnet Readiness

**4/10 (antes do harness) → arquitetura 9/10 → empírica ✅ COMPROVADA (API comprovada, 2026-06): Sonnet aprovado.**
Teste limpo de comédia (ch_12_03, fora da TM) no nível da versão à mão a Opus; custo ~$36/jogo no
setting econômico (effort:low, sem thinking). O que exigia Opus era segurar o contexto acumulado, não
a tradução por linha — confirmado. As 5 mudanças de maior impacto (todas em P0):
1. job stateless por cena (`run_scene`); 2. `context_pack` limitado; 3. caching da doutrina;
4. memória externalizada (TM/voice cards/decisões); 5. saída por schema. Com (1)+(2)+(4) o contexto
por execução para de crescer e cai bem abaixo de 30% do atual → Sonnet vira o default de tradução.

## MVP arquitetural recomendado (entregue neste ciclo)

`framework/runtime/` (context_pack + state_index + model + run_scene + testes) + `framework/docs/`.
É o mínimo que torna a tradução sustentável e model-agnostic **sem** interromper a entrega: as próximas
cenas rodam pelo harness, uma sessão limpa por cena.
