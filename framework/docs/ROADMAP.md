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
> Doutrina existe nas skills, mas o harness de escala não a aplica. Ver `ARCHITECTURE_REVIEW_2.md`.

| # | Item | Severidade | Status |
|---|---|---|---|
| R1 | ligar e **comprovar** o caminho API (`.env` + benchmark) | 🔴 | ✅ **feito** — Sonnet aprovado; bugs de produção corrigidos; custo real ~$36/jogo |
| R2 | `api` como default de produção | 🔴 | ✅ **feito** — default `api` em translate/run_scene/run_chapter |
| R3 | **Fase 0**: KB reconciliada + **gate de cobertura** | 🟠 | ✅ **feito** — `kb_gate.py`; Fase 0 do cap.12; `kb_frontier=12_17`. **Driver de Fase 0 ✅** (`fase0.py`): automatiza a parte determinista do gargalo — DESCOBRE o gap (candidatos de lore/nome que aparecem no cap. e a KB não cobre, via a MESMA primitiva `_present` do tradutor → o gap é exatamente o que o `context_pack` falharia em surfar) e escreve a worklist (**cobrança** do humano); `--check` valida cobertura (gap recorrente cross-cena fechado + `reconciled`); `--apply-frontier` avança `kb_frontier`. Governança preservada: IA **propõe** → humano **reconcilia** (skill 03) → script **valida/aplica**; NÃO pesquisa sozinho. Auditou o cap.13 e achou 3 termos recorrentes fora do glossário (Mystery Twins / Imperial Guard / Twin Shields). |
| R4 | **spoiler**: `spoiler_ledger.json` + **filtro temporal** + regra de gênero | 🟠 | ✅ **feito** — ledger + filtro no `context_pack`; Carta atualizada |
| R5 | bundle de custo (dedup TM/intra-corpus, ~~slim de schema~~, batch API) → ~$36→~$15 | 🟡 | **parcial**: effort/thinking já cortou ~5×; **dedup por TM ✅** (linhas com fonte já traduzida em outra cena não vão ao modelo — corta tokens de saída; medido 2,8% no cap.12 sobre TM cap.11+12, **cresce com o corpus**; guard de paridade + nunca reusa a própria cena; desligado no escalonamento). **slim de schema: REJEITADO por qualidade** (ver abaixo). **cache da Carta: observável, BECO SEM SAÍDA** ✅ (medido cap.13: Carta ~1.3k tok, custa $0,14 vs output $3,41; com cache_control fica até levemente net-negativo pois o batch paraleliza e re-escreve ~27×; cache perfeito é impossível no batch e economizaria só $0,12/cap). **batch API ✅ comprovado vivo** (cap.13 9/9; −50% real; resume idempotente; re-batch acumulativo entre rodadas). **tiering por complexidade ✅ codado** (linhas SEM `\n` → Haiku −67%/linha; COM `\n` → Sonnet; benchmark: voz do Haiku no nível do Sonnet inclusive registro arcaico, mas Haiku derrapa na paridade de `\n` em escala → o split dribla a fraqueza; só no batch; falta run viva tiered p/ medir). **back-translation em BATCH ✅ codado** (Tier 1: a back-translation Opus — passo mais caro/linha, $25/M de saída — vira PÓS-PASSE do capítulo; `batch_back_translate` coleta as linhas high/critical de todas as cenas verificadas e roda 1 batch −50%; `run_chapter --batch` difere a back-translation por cena e batcheia ao fim; resume idempotente; report-only, não bloqueia; ledger marca `batch=True`. Falta run viva p/ medir). |

> **slim de schema — REJEITADO (não tentar de novo).** A ideia era cortar `tone_register`/`intent`
> da saída p/ economizar ~15% de tokens. **Não fazer:** (1) `tone_register` GATEIA qualidade no
> `build_plan_chapter.py` (flag de interjeição copiada do source em vez de localizada); cortá-lo mata o
> gate. (2) Com o thinking DESLIGADO (corte de custo), esses campos são a **única cognição estruturada
> por linha** — e a ordem do schema põe `t` por ÚLTIMO, então o modelo articula registro+intenção ANTES
> de traduzir. É raciocínio barato que ancora voz/registro (comédia, voz por personagem = o valor central
> do projeto). Economizar saída sacrificando isso é a alavanca errada. `intent` é write-only hoje mas é o
> par natural do `tone_register` no prefixo de raciocínio — fica.

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

### P2 — quando amadurecer (reuso/escala 40–100k)
| # | Item | Nota |
|---|---|---|
| 10 | generalizar `state_index` p/ múltiplos projetos; paralelizar cenas | escala horizontal |
| 11 | RAG/vetor **só** sobre `decision_log` + `universe_knowledge_base` | só ao atingir o gatilho do `adr/0003` |

### P3 — não fazer agora (overengineering)
Banco relacional pesado, knowledge graph, fila/broker, multi-agente "de serviços". O orquestrador
determinístico + 2 papéis de IA já é a granularidade certa.

## Fases

- **Fase 1 — resolver estouro de sessão:** P0 (entregue). Cena stateless + contexto limitado.
- **Fase 2 — reduzir custo operacional:** P1 (entregue e **comprovado em produção**: métricas + API
  endurecida + `run_chapter` + benchmark Sonnet aprovado + telemetria de gasto real via `api_ledger.jsonl`).
- **Fase 2.5 — cabear cognição no runtime:** P1.5 (R1–R5). Ligar/comprovar API, KB-gate, spoiler-filter,
  bundle de custo. **É aqui que estamos.**
- **Fase 3 — escalar p/ 40–100k linhas:** P2. Paralelização + (se preciso) RAG sobre lore/decisões.

## Sonnet Readiness

**4/10 (antes do harness) → arquitetura 9/10 → empírica ✅ COMPROVADA (R1, 2026-06): Sonnet aprovado.**
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
