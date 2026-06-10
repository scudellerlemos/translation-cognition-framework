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
| 8 | endurecer caminho `api` (streaming, schema, guard `\n`+retry, backoff) | ✅ codado, ⚠️ **não comprovado** (falta `.env`) |
| 8b | `run_chapter.py` — driver de capítulo (loop de cenas, resumível) | ✅ |
| 9 | benchmark de modelos (Sonnet vs Opus em cenas-gold) | ⏳ pendente da chave |

### P1.5 — cabear cognição no runtime (gaps da Architecture Review #2)
> Doutrina existe nas skills, mas o harness de escala não a aplica. Ver `ARCHITECTURE_REVIEW_2.md`.

| # | Item | Severidade | Status |
|---|---|---|---|
| R1 | ligar e **comprovar** o caminho API (`.env` + benchmark) | 🔴 | ✅ **feito** — Sonnet aprovado; 4 bugs de produção corrigidos; custo real ~$36/jogo (ver `MODEL_INTERFACE`) |
| R2 | `api` como default de produção (`run_chapter --backend api` é o entrypoint) | 🔴 | 🟡 `run_chapter` já default `api`; falta flip do default de `run_scene`/`translate` |
| R3 | **Fase 0**: KB reconciliada (IA+humano) global + **gate de cobertura** no `context_pack`/`translate` | 🟠 | pendente (skills 01–04) |
| R4 | **spoiler**: `spoiler_ledger.json` + **filtro temporal** no `context_pack` + regra de gênero pt-BR na Carta | 🟠 | pendente (depende R3) |
| R5 | bundle de custo (dedup TM/intra-corpus, slim de schema low-risk, batch API) → jogo ~$36→~$15 | 🟡 | **parcial**: tuning de effort/thinking já cortou ~5× (o maior); falta dedup/slim/batch |

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
- **Fase 2 — reduzir custo operacional:** P1 (entregue: métricas + API endurecida + `run_chapter`).
  Falta **comprovar em produção** (benchmark/`metrics.jsonl` reais — pendente da chave).
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
