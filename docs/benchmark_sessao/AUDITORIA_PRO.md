# Auditoria do framework para o Claude Pro (2026-10-19)

Base: inventário do repositório, o `RELATORIO.md` do benchmark (V0 a V16) e o `cost_report` do projeto real.
Tudo que é número vem do ledger ou do tamanho de arquivo; o que é estimativa está marcado **(est.)**.
Sem fala do jogo.

## 1. Resumo executivo

- O framework não é um sistema de coordenador com muitos especialistas. O fluxo é um pipeline determinista
  (`wave.py` → `run_scene.py` → gates) com **um** agente de tradução (`scene-translator`) e um de retrotradução
  (Opus), sob um orquestrador (a sessão principal, skill `rodar-onda`). Dois agentes de manutenção
  (`build-error-resolver`, `refactor-cleaner`) não participam do fluxo de tradução.
- O custo vive no **modelo escolhido e no número de subagentes**, não em contexto inflado: o prompt de cena já é
  recortado por cena (glossário 0,1 a 0,8 KB, vozes 1,3 a 1,5 KB).
- Medido no benchmark (6 cenas, 267 falas): base US$ 1,17 a 1,38 → agrupado em Sonnet US$ 0,88 a 1,01 (-26%) →
  agrupado em Haiku US$ 0,33 a 0,34. **Haiku agrupado é ~-73% contra a base**, qualidade cega sem diferença
  detectável (0 a 3 erros em n=120).
- A meta genérica de "60 a 80% menos contexto inicial" **não se aplica**: o contexto inicial já é por cena, e o
  único bloco grande e fixo (a Carta de governança) vale ≤5% do custo. A economia veio de trocar de modelo.
- Falta pouco: a Carta, a fila de escalonamento e o custo da conversa principal.

## 2. Mapa do AS IS

```
usuário ──► sessão principal (Sonnet) ── skill rodar-onda
              │  1 panorama.py → propõe cenas   2 kb_phase.py → lore/glossário (decisão humana)
              ▼
        N × scene-translator (Haiku desde 2026-10-19; antes Sonnet), paralelos, 1 por cena/grupo
              │  wave.py → run_scene.py → context_pack/pack_render → scene_prompt.md
              │  subagente lê o prompt, escreve translations_<cena>.json, repete até o gate fechar
              ▼
        gates deterministas: build_plan/verify, budget, glossary_lint, pattern_lint, quality_gate, connector_gate
              ▼
        sessão principal confere no disco: wave.py (sem cenas), cost_report, panorama, escalonamentos (hitl)
              ▼
        fala high/critical ──► retrotradução (Opus, 1 por cena) ──► pass|revise
```

| Componente | O que é |
| --- | --- |
| Agentes | `scene-translator` (tradução), retrotradutor Opus (sem arquivo, lançado pela skill), `build-error-resolver`, `refactor-cleaner` (dev, fora do fluxo) |
| Skills | `rodar-onda` (11 KB), `gaps-custo`, `levantar-melhorias`, `panorama-ondas` |
| Prompts fixos | `CLAUDE.md` 5,8 KB (carregado em toda requisição), `scene-translator.md` 4,2 KB, `SKILL.md` do `rodar-onda` 11 KB (só quando invocada) |
| Contexto de cena | `scene_prompt.md`: ~15 KB numa cena de 31 falas, `pack.json` ~10 KB |
| "RAG" | léxico: KB (`universe_knowledge_base.md`), TM (`translation_memory.jsonl`), glossário, decisões, controle de spoiler; sem vetor na rota de sessão |
| MCP | nenhum ligado no projeto (`disableClaudeAiConnectors`, `deniedMcpServers`) |
| Memória | `run_state.json`, `hitl_state.json`, `decision_log.md`, memória do Claude Code |
| Observabilidade | `events.jsonl`, `api_ledger.jsonl`, `metrics.jsonl`, `phase_marks.jsonl`, `obs_report`, `cost_report` |

## 3. Medição (onde o orçamento vai)

Projeto real hoje: 181 cenas `verified` (13.723 de 23.933 falas), equivalente API US$ 129,36 em 5.341 requisições
(fase 3: US$ 127,66). Restam 10.210 falas.

| Etapa | Tokens | Chamadas | Frequência | Impacto | Classe |
| --- | --- | --- | --- | --- | --- |
| Tradução (subagente) | ~30 a 37 mil de base por subagente + ~1,0 mil/fala | ~22 req/6 cenas (V13) | por cena/grupo | **~85 a 90% do custo** | crítico |
| Retrotradução (Opus) | ~15 s por 3 falas, só `high` | 1 por cena com `high` | pouco | baixo | importante |
| Conversa principal (orquestração) | cresce com a onda; `/usage` +2 a +20 pp por braço, inclui a conversa | 1 por passo | por onda | medido como teto, não separável | importante |
| Carta de governança no prompt | ~2 mil tokens por cena | embutida | por cena | ≤5% (V8) | importante |
| Script de conferência / gates | 0 token (Python) | 0 | por cena | 0 | crítico |
| Levantamento de lore (`kb_phase`) | pouco | 1 por onda | por onda | baixo | importante |
| Observabilidade | 0 token (grava arquivo) | 0 | contínua | 0 | importante |

Maiores consumidores: (1) tokens de subagente por cena, (2) modelo usado neles, (3) conversa principal, (4) Carta,
(5) rodadas de correção de `\n`/bytes (V10: 1 a 2 voltas por braço).

## 4. Gargalos principais (Top 10)

| # | Problema | Impacto | Mudança | Economia | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | Sonnet em fala de baixo risco | ~US$ 0,0044/fala | Haiku no tradutor; `high`/`critical` retraduzidas em Sonnet | **-65% (medido)** | feito, sem commit |
| 2 | Um subagente por cena curta (custo fixo US$ 0,076 a 0,13) | repete a base de 30 a 37 mil tokens | agrupar ≤4 cenas de ≤60 falas, soma ≤150 | **-26% (medido)** | feito, sem commit |
| 3 | Conversa principal acompanha cada subagente | parte do `/usage` | prompt de subagente curto; relatório curto; menos releitura | não separável (est. 5 a 10%) | parcial |
| 4 | Carta de governança em toda cena | ~2 mil tokens/cena (50% de cena curta) | trocar por contrato curto + ponteiro | ≤5% do total (V8) | não feito |
| 5 | Rodadas de correção `\n`/bytes | 1 a 2 voltas por braço | script de conferência antes do `wave` | ≤ ruído (V10) | não vale |
| 6 | Retrabalho por `escalate` de corte de bytes | fila humana | aceitar corte sinalizado (decidido) | pequeno | decidido |
| 7 | Sessão principal em Sonnet para orquestração | pouco, é fluxo mecânico | manter Sonnet; Haiku na sessão pioraria a decisão | n/d | manter |
| 8 | Retrotradução Opus | só `high` | manter; é o gate de qualidade | n/d | manter |
| 9 | Execução headless (V12) | sem ganho de cota (+15 pp) | não adotar | 0 | descartado |
| 10 | Pré-preenchimento por TM (V14) | reuso já cobre 20,3% | não implementar | ≤2,4% | descartado |

Descartados por medição: V7 roteiro enxuto, V8 prompt enxuto, V10 script de conferência, V12 headless, V13 um
subagente em sequência (indiferente), V14 TM, V15 campos de saída (8% dos tokens de saída, usados adiante).

## 5. Auditoria por área

**Arquitetura.** Monolítica no código (pipeline), fan-out por cena na tradução, fan-in no `wave.py`/disco.
Sem coordenador de LLM em cima de especialistas; a "coordenação" é Python e a skill. Chamada redundante: só a base
de cada subagente (tratada no agrupamento). Nenhum especialista é redundante no fluxo.

**Prompts.** `scene-translator.md` (4,2 KB): enxuto; já tem as regras de `lore_novo`/`escalate`. A skill `rodar-onda`
(11 KB) só carrega ao invocar. O `CLAUDE.md` (5,8 KB) vai em toda requisição: ~1,5 mil tokens × 5.341 req ≈ 8 M de
tokens lidos, quase todos de **cache** (barato). Não há ganho que justifique reescrever.

**Contexto.** Sempre necessário: Regras do conector, vozes e glossário da cena, linhas a traduzir, formato de saída.
Sob demanda (já é): glossário e vozes só da cena, spoiler só da cena. Melhor virar ponteiro: **a Carta** (~8 KB,
nove seções, repetida por cena). Melhor virar ferramenta: já são (gates).

**RAG.** Léxico, sem vetor na rota de sessão: pouco contexto, sem duplicação evidente (TM de 99 bytes numa cena
sem reuso). Sem reranking a propor: o conteúdo devolvido por cena é pequeno (decisões 0,75 KB, spoiler 0,37 KB).

**Especialistas.**

| Especialista | Manter | Fundir | Remover | Lazy load |
| --- | --- | --- | --- | --- |
| scene-translator | sim (Haiku) | não | não | já é (só na onda) |
| retrotradutor Opus | sim | não | não | já é (só se houver `high`) |
| build-error-resolver | sim | não | não | já é (só em CI quebrada) |
| refactor-cleaner | sim | não | não | já é |

**Ferramentas.** Nenhum MCP ligado. Chamadas repetidas: `panorama.py` a cada onda (barato, Python). Nada a cachear
que custe token. `kb_phase` roda uma vez por onda.

**Memória.** `run_state`/`hitl_state` em disco, reaproveitados entre sessões. A "Retomada" do ROADMAP limita a
releitura (offset 1, limit 21). Sem reenvio relevante.

**Observabilidade.** Já é barata: grava em arquivo, 0 token. O `cost_report` é o medidor confiável (ruído do
ledger ~20%; `/usage` é grosso demais para ganho <2x).

**Segurança.** Mantida. `content_guard` bloqueia conteúdo de jogo no git; gates não têm flag de bypass; conectores
do claude.ai desligados; subagente `scene-translator` só tem Read/Write/Edit/Bash. Risco novo do Haiku: nenhum de
permissão; o risco é de qualidade em fala dura, coberto pela escalada `high`→Sonnet e pela retrotradução.

## 6. Arquitetura proposta para o Pro

1. Tradutor em **Haiku** para tudo; **Sonnet** só nas falas `high`/`critical` (passo 5d da skill).
2. **Agrupamento** de cenas curtas por subagente (≤4 cenas, ≤60 falas cada, soma ≤150).
3. Retrotradução **Opus** só onde há `high`; triagem de risco barata antes.
4. Sessão principal em Sonnet, só para decisões (lore, escalonamento) e conferência; trabalho mecânico em Python.
5. Medir sempre pelo ledger (`cost_report`), nunca pelo `/usage`.

## 7. Fluxo otimizado

`panorama` → proposta de cenas (usuário diz sim) → `kb_phase onda` (decisões de lore) → **grupos** de cenas curtas
em subagentes Haiku, em paralelo → `wave` sem cenas → listar `high`/`critical` → Sonnet retraduz só esses offsets
→ `wave` → retrotradução Opus → escalonamentos em lote → panorama/custo/Retomada.

## 8. Quick wins / Roadmap

| Prazo | Ação | Economia |
| --- | --- | --- |
| Hoje (feito, falta commit) | Haiku no `scene-translator`; passo 5d; agrupamento ampliado | -65% e -26% medidos, combinado ~-73% |
| 1 dia | Rodar a próxima onda real em Haiku e conferir qualidade com `quality_sample` (n=120, `--seed 42`) | valida a economia no projeto real |
| 1 semana | Medir o passo 5d na prática (quantas `high` voltam a Sonnet; custo do retrabalho) | confirma ou ajusta a regra |
| 1 semana | Carta de governança por ponteiro (V8 lado código, numa cópia isolada; precisa de ok seu) | ≤5% |
| 1 mês | Reavaliar o V16 (parar no limite da janela e retomar), que não foi rodado | pode evitar perda de sessão; sem número |
| 1 mês | Projeção de término (abaixo) com o custo real de uma onda em Haiku | planejamento |

## 9. Estimativa de economia (restam 10.210 falas)

| Cenário | USD/fala | Total aprox. |
| --- | --- | --- |
| Base (V0b/V0c, Sonnet por cena) | 0,0044 a 0,0052 | US$ 45 a 53 |
| Agrupado em Sonnet (V6/V6b) | 0,0033 a 0,0038 | US$ 34 a 39 |
| Agrupado em Haiku (V9/V9b/V9c) | 0,0012 a 0,0017 | **US$ 12 a 17** **(est.)** |

Acrescentar o retrabalho `high`→Sonnet e a retrotradução Opus: **(est.)** +10 a 20%. A cena longa (V9c, 197 falas)
saiu a US$ 0,0017/fala, então o teto prático fica perto de US$ 17 a 20.

| Métrica | Antes | Depois | Ganho |
| --- | --- | --- | --- |
| USD equiv. por execução (6 cenas, 267 falas) | 1,17 a 1,38 | 0,33 a 0,34 | -73% |
| Chamadas ao modelo | 147 a 158 requisições | n/d no Haiku; subagentes 6 → 3 | menos subagentes, requisições não medidas |
| Contexto inicial por cena | ~15 KB (31 falas) | igual | 0% (Carta ≤5%) |
| `/usage` de sessão | +7 a +14 pp (base) | +2 a +3 pp (V9, V9b) | ~-75% |
| Especialistas carregados | 1 tradutor por cena | 1 por grupo | menos |
| RAG enviado por cena | ~1,7 KB | igual | 0% |
| Latência | n/d | Haiku usou 275 mil tokens de subagente (2x o Sonnet) | sem medição de tempo; não é ganho |

## 10. Checklist de validação pós-migração

- [ ] `scene-translator.md` com `model: haiku`; `CLAUDE.md` e skill coerentes (feito).
- [ ] Primeira onda real: `cost_report` por cena e USD/fala dentro de 0,0012 a 0,0020.
- [ ] `quality_sample export --n 120 --seed 42` pontuado às cegas: erro dentro do IC do Sonnet (≤ ~7%).
- [ ] Cenas `verified` subiram pelo número de cenas da onda; nenhum gate contornado.
- [ ] Contar `escalate` por onda: se passar de ~1 por 100 falas, revisar a regra de corte por byte.
- [ ] Passo 5d: registrar quantas falas `high`/`critical` voltaram a Sonnet e o custo delas.
- [ ] `/usage`: sessão +≤5 pp por onda de 6 cenas; se passar, medir a conversa principal.
- [ ] `content_guard` OK em todo commit; `/mcp` vazio.

## Riscos e limites desta auditoria

- Os números do Haiku vêm do recorte de 6 cenas e de uma cena longa; o jogo tem mais variedade (falas `critical`).
- Haiku usou o dobro dos tokens do Sonnet, mas a US$ ~65% menor; numa cota por tokens (e não por USD) o ganho em
  `/usage` pode ser menor que o do ledger. No benchmark o `/usage` confirmou (+2 pp), mas com n pequeno.
- Latência não foi medida.
