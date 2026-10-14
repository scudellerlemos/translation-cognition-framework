# framework/runtime — harness de execução (orquestração determinística + interface de modelo)

Torna **cada cena um job stateless e limitado**: o contexto por execução é O(cena), não O(histórico).
É a camada que tira a orquestração e a memória da janela da LLM. Ver `docs/ARCHITECTURE.md`.

## Módulos

Agrupados por concern (a fronteira com o LLM pago é só `model.py` + `back_translate.py`):

**Orquestração & contexto (det.)**

| Arquivo | Função |
|---|---|
| `run_scene.py` | Orquestrador de 1 cena: `connector_gate` (completude de conector) → `kb_gate` → `_pack_and_translate` → `_fitting_loop` (build_plan + verify, com escalonamento de budget) → `_back_phase` → `state_index.build` → checkpoint. Grava `connector_hash` + `_ts` junto com `verified=True`. Resumível. Cena `verified` sem fala tocada (mesmo conector e doutrina, ver `touched.py`) é pulada; `--full` força a reconferência. Flags: `--backend`, `--require-back`, `--no-verify`, `--no-back`, `--jobs N`, `--full`, `--clean`, `--check-stale`, `--purge-discontinued DAYS`, `--skip-kb-gate`. |
| `touched.py` | Reconferência só do que mudou: impressão digital (sha1 curto) por fala da tradução, gravada no `run_state` (`t_hashes`) quando a cena fecha `verified`. `touched()` → offsets novos/alterados; `unchanged()` → verified, sem fala tocada, mesma doutrina e mesmo conector. |
| `wave.py` | Uma onda num comando só (caminho de sessão): `run_scene` → `scene_dedup copy` (+ `run_scene` das cópias) → `glossary_lint` → `quality_gate` → `cost_report --summary` → `obs_report`. Mesmos comandos, ordem e gates; passo que falha PARA a onda. Saída inteira em `artifacts/wave_last.log`, 1 linha por passo no terminal. As cenas pedidas escopam só `run_scene`/`scene_dedup`; os demais passos olham o projeto. Uso: `wave.py <projeto> [cena ...] [--backend in-session\|api] [--require-back]`. |
| `scene_dedup.py` | Texto repetido entre cenas é traduzido UMA vez: agrupa cenas pela mesma sequência de `text_source` (ou `text_en`, como `context_pack.load_dialogs`); `plan` lista os grupos, `copy [CENA ...]` leva tradução e retrotradução do representante verified para as cópias não verified, remapeando os offsets por posição no JSON já parseado. A cópia não pula gate: o `run_scene` passa cada uma pelos gates. |
| `session_lot.py` / `session_part.py` | Caminho da sessão em lote (a IA da sessão traduz; nada vai à API): `plan` (lotes de até N falas, 150 por padrão), `prompt` (junta os `scene_prompt.md` num prompt de lote), `check` (tokens, orçamento de bytes via `budget.py`, cobertura), `go` (confere e, se limpo, roda `run_scene --backend in-session --require-back`), `split`/`join` (por seção; `session_part.py`), `install` (copia os `.DAT` remontados para o jogo). Arquivos de trabalho em `projects/<p>/tools_local/` (gitignored: trazem fala do jogo). |
| `risk_triage.py` / `risk_triage_run.py` | Triagem de risco (passo 4.4a, caminho de sessão): `export` grava lotes `lote_NNN.tsv` + `triagem_prompt.md`, `apply` sobe para `high` o risco das falas apontadas em `veredito_NNN.tsv`. `risk_triage_run.py` faz o miolo num comando só (juiz barato via CLI `claude -p`, `--model haiku`, `--jobs 6`): sem `--go` só LISTA os lotes; `--go` chama o modelo (pago). |
| `scene_lifecycle.py` | Housekeeping/diagnóstico extraído de `run_scene.py` (P4 hardening): `clean_failed_scene`, `prune_discontinued`, `_check_stale`. Reimportado em `run_scene.py` (mesmo nome, zero mudança de caller). |
| `connector_mgr.py` | Interface do conector (A1): `_run`, `_verify_status`, `_connector_script`, `_connector_hash`, `_warn_if_connector_stale`. Detecta conector stale via `run_state.json` antes de executar (S3). |
| `connector_gate.py` | Gate de completude de conector (D6, espelha `kb_gate.py`): hard-block se scripts ausentes; soft-block se nunca houve round-trip verde. `assert_fresh_read()` (D5): prova de leitura completa antes de editar um conector (hash do conteúdo alegado vs. disco). |
| `run_chapter.py` | Driver de capítulo: loop de cenas via `run_scene`; modo batch por padrão (−50%; `--no-batch` desliga); resumível; `--max-usd`; ao fim, sempre: export de QA, auditoria de spoiler/gênero, piso de qualidade e validação de schema; rebuild de `state_index` 1×/capítulo em modo batch. |
| `run_game.py` | Driver ponta-a-ponta: descobre capítulos (ou modo flat via `--scenes-glob`) e roda todos em sequência; `--max-usd` GLOBAL (encolhe entre capítulos); retomada automática de graça. |
| `progress_report.py` | Observabilidade de progresso do jogo inteiro: % concluído, linhas/min, ETA, taxa de falha — puro (elapsed_s externo, sem `time.time()` interno). |
| `kernel.py` | Fachada fina (B3): consolida `run_scene`/`run_chapter`/`run_game`/`validate_project`/`write_pack` sob um import único. Zero lógica nova — reexport testado por identidade de objeto. |
| `context_pack.py` | Monta o pacote LIMITADO de 1 cena → `scene_prompt.md` + `pack.json`. A peça central. Inclui `validate_dialogs_csv()` — schema guard antes de `load_dialogs` (A4). TM por série (`tm_series`) consultada na entrada via `tm_lookup.py`. |
| `budget.py` | FONTE ÚNICA da conta de orçamento de bytes (modelo, ferramentas locais e conferências): bytes UTF-8 reais se o conector não translitera (`target_charset_supported` True), senão a forma transliterada; `budget_reserves_terminator` reserva 1 byte; exceção pontual por `byte_budget_exceptions` (`effective_budget`). |
| `box_width.py` | Largura de linha por caixa derivada do inglês do próprio jogo: `project.json` `"line_width": "derive"` (maior segmento visível entre quebras), `line_width_max` fixo (vence), ou 62 sem nenhum dos dois; `rewrap()` requebra nos espaços. |
| `opcodes.py` | Tabela de opcodes do conector (`connector.control_codes`: nome ou `{name, params, width, values}`); `segments()` mede a largura visível entre quebras de caixa — `newline`, `page_break` e `choice_start` quebram; token de parâmetro (`params`) não é código. |
| `pattern_lint.py` | Lint de padrões ANTES da amostra de qualidade: `largura` e `parametro` bloqueiam (exit 2), `identico-fonte` só é contado. |
| `artifact_io.py` | Camada única de leitura de artefatos (scenes, plan_lines, translations_map, back_entries). |
| `paths.py` | Fonte única de caminhos de artefato. |
| `scaffold_project.py` | Inicializa os artefatos KB de um projeto novo com o schema correto desde o início (elimina "schema errado descoberto tarde"); gera `project.json` do template, KB-stub/research_log/kb_ratified/spoiler_ledger, `profile/` (4 arquivos de referência) e `connector/` (cópia do `_skeleton`) — nenhum placeholder passa gate — e reporta status do `kb_gate`/`connector_gate`. Skip seguro — nunca sobrescreve arquivo existente. |
| `split_scenes.py` | Materializa `artifacts/scenes/<cena>/dialogs.csv` a partir do `dialogs.csv` FLAT do `extract.py`, agrupando por 1 coluna do corpus (`--by`, default `file`). Escopo deliberado: só cobre o caso 1-coluna-identifica-a-cena (BoF4/Trails Sky SC); Souldiers/Utawarerumono ficam fora, não força um contrato que os 3 não compartilham. |

**Modelo — IA + suporte determinístico**

A fronteira não-determinística é **só** `model.py` + `back_translate.py` (as chamadas ao LLM pago; fora dela, só `kb_build_ollama.py` chama um LLM, local e sempre como rascunho). Todo o
resto deste grupo é plumbing **determinístico** em volta da IA:

```mermaid
flowchart LR
  subgraph ia["IA — a fronteira não-determinística"]
    tr["model.py<br/>translate · batch_*"]:::a
    bt["back_translate.py<br/>revisão de alto risco"]:::a
  end
  subgraph det["suporte ao modelo — determinístico"]
    client["llm_client.py<br/>cliente · backoff · batch"]:::d
    cost["cost.py<br/>pricing · ledger"]:::d
    cfg["config.py<br/>tiers · custo · status"]:::d
    bench["bench_translate.py<br/>aprovação de modelo"]:::d
  end
  det --> ia
  classDef a fill:#f6d6e8,stroke:#c0397b,color:#000;
  classDef d fill:#d6e8f6,stroke:#1f6f9b,color:#000;
```

| Arquivo | IA? | Função |
|---|---|---|
| `model.py` | 🩷 IA | `translate` / `batch_*`; backends `in-session` (assinatura) e `api` (model-mix); guard anti-blow-up. |
| `back_translate.py` | 🩷 IA | Back-translation de alto risco (Opus) + amostragem ~5% das low/medium; invalidação de stale. |
| `llm_client.py` | det. | Cliente + backoff/retry, await de batch, dotenv. |
| `ollama_client.py` | det. | REST client pro Ollama local (zero custo de API) — usado só pelo pipeline de KB (`kb_fetch`/`kb_build_ollama`) e por `tcf ollama`, não é backend de tradução (ADR 0008); configuração via `OLLAMA_HOST`/`OLLAMA_MODEL`/`OLLAMA_NUM_CTX`. |
| `config.py` | det. | Constantes de tier/modelo/custo/status (sem lógica). |
| `cost.py` | det. | Pricing real + `log_api_call` (escreve o ledger). |
| `bench_translate.py` | det. | Benchmark Sonnet vs Opus-à-mão (gate de aprovação de modelo). |

**Estado & memória (det.)**

| Arquivo | Função |
|---|---|
| `state_index.py` | Materializa `translation_memory.jsonl`, `voice_cards.json`, `decision_index.json`. Idempotente. |
| `tm_correct.py` | Find→replace governado em translations + plan (dado propõe, script aplica; dry-run/`--apply`). |
| `tm_lookup.py` | TM por SÉRIE (D4): `tm/<série>.json` na raiz do repo (versionado quando existir; ainda não há nenhum), isolamento estrutural entre franquias. Série declarada em `project.json["series"]` (fallback: slug do título). |
| `tm_updater.py` | `sync_scenes()` — upsert na TM da série a partir de `translation_plan_*.json` das cenas VERIFIED tocadas pelo QA; `reset_game()` — remove entradas de 1 jogo (retradução), avisa antes. |
| `fingerprint_monitor.py` | Manifesto de conector por projeto (D3): `connector_manifest.json` (tier/engine/versão/fingerprints). Fingerprint de ARQUIVOS-FONTE do jogo (detecta patch); reusa `_connector_hash` p/ drift de scripts. |

**Gates de cognição (det.)**

| Arquivo | Função |
|---|---|
| `kb_gate.py` | Cobertura de KB por cena (research reconciliada + `kb_frontier`) ANTES de traduzir. Avisa quando `status: reconciled` e `human_input: pending` co-existem (G1). Exige ratificação humana por entidade (`kb_ratified.csv`) pra qualquer research_log `reconciled`, não só o caminho `draft_ollama`. |
| `kb_phase.py` | Driver de Fase 0: descobre o gap de KB do capítulo; `--check` falha sem fonte; `--strict` exige ratificação. |
| `kb_review.py` | Digest + **gate de fonte** do delta de KB (`--gate`/`--strict`; lê `kb_ratified.csv`). |
| `kb_fetch.py` | P1.7-E: busca/normaliza fontes de KB (URL/PDF/.docx/.xlsx/local) pra `artifacts/research_cache/`, zero LLM. `--found-por {ia,usuario}` preserva proveniência. |
| `kb_build_ollama.py` | P1.7-E: extração factual por entidade via Ollama LOCAL a partir do cache — sempre `status: draft_ollama`, nunca `reconciled` sozinho. |
| `kb_reconcile.py` | Promove `draft_ollama` → `reconciled` SÓ após ratificação humana por entidade (`kb_ratified.csv`) + revisão real da seção "Conflitos Resolvidos". |
| `kb_concordance.py` | Sinaliza concordância entre o rascunho `draft_ollama` e a pesquisa humana já registrada — triagem read-only pra Fase 1B (skill 03), nunca bloqueia nem decide sozinho; o gate de promoção continua em `kb_reconcile.py`. |
| `spoiler_check.py` | `check` (nomes) + `check_gender` (gênero) — não vaza reveal antes do `reveal_timing`. `audit_and_persist()` roda OBRIGATORIAMENTE ao fim de todo capítulo (`run_chapter.py`), grava `spoiler_audit.json`. |

**Qualidade & custo (det.)**

| Arquivo | Função |
|---|---|
| `quality_gate.py` | Cruza veredito de back-translation + cobertura; `--export` da worklist `revise`. |
| `quality_review.py` | Relatório humano **XLSX** amigável; aplica verbatim (R$ 0) ou nota cirúrgica; `--max-usd`. Persiste `qa_effectiveness.jsonl` (`total_marked` vs `applied`) a cada ciclo. |
| `quality_fix.py` | Re-traduz dirigido só os offsets `revise` da worklist; `--max-usd`. |
| `glossary_lint.py` | Consistência de glossário cross-capítulo: termo do EN sem a forma canônica no pt-BR → candidatos p/ revisão. |
| `cost_report.py` | Agrega `api_ledger.jsonl` (custo real por modelo/tipo/cena; gasto desperdiçado). `--summary`: linha única p/ embeber em docs (G5); `--json`: saída estruturada. |
| `review_page.py` (+ `review_page_tpl.py`) | Página local de revisão humana das planilhas de `qa_revisao/para_revisar` (HTML, fora do git): só lê os CSVs e devolve o mesmo CSV; `--serve [--port 8765]` grava direto na pasta. |
| `obs_report.py` | Observabilidade do projeto numa visão: 1 linha por cena + gates + falhas (`run_state`, `metrics.jsonl`, `events.jsonl`, ledger); só lê. `--json`, `--scene`. |
| `events.py` | Log estruturado `artifacts/events.jsonl` (1 JSON por acontecimento; só contagem, status e duração, sem texto do jogo; fora do git). Fonte do `obs_report`. |
| `session_usage.py` | Tokens REAIS das sessões do Claude Code (backend in-session): `sync` anexa ao `api_ledger.jsonl` linhas `source: "session"` (`cost_usd` 0.0; `api_equiv_usd` = custo na API); `mark <projeto> <fase>` grava a virada de fase em `artifacts/phase_marks.jsonl`. Só contador de token, modelo e id de cena. |
| `hitl.py` | Humano no laço (liga com `"hitl": true`): `accept-scope`, `choose-path`, `ratify`, `ack`, `resolve`, `status`; escopo, caminho e fila de ambiguidade bloqueiam, glossário frequente e onda só avisam. Decisões em `artifacts/hitl_log.jsonl`. |
| `translate_checkpoint.py` | Não perde as linhas já pagas quando os retries esgotam: `save`/`load`/`clear` de `partial_translations_<id>.json` (vale só com mesmo source e `doctrine_hash`) e `log_exhausted`. |
| `batch_status.py` | Checagem honesta de batches em andamento (só reporta; nunca cancela). |
| `batch_smoke.py` | Smoke vivo do contrato da Batch API antes de pagar um capítulo inteiro (E5). Validado ao vivo (~$0,0018 por run, 2 linhas Haiku+Sonnet). |

**Testes**

| Arquivo | Função |
|---|---|
| `test_runtime.py` | determinismo, boundedness, idempotência, recuperação por-linha, teto/estimativa de custo, guard de no-work-text, contrato do conector (hash determinístico, sandbox, protocolo VERIFY_STATUS), round-trip de integração, kb_gate human_input, validate_dialogs_csv, prune_discontinued, summary_line, TM por série via `apply()`. Fixture `fake_pack_ctx` (conftest.py) elimina monkeypatches repetidos em testes de batch. Módulos novos (`touched`, `wave`, `scene_dedup`, `risk_triage_run`, `session_lot`, `budget`, `box_width`, `review_page`, `session_usage`, `kb_reconcile`, `connector_gate`, `run_game`, `progress_report`, `tm_lookup`, `tm_updater`, `fingerprint_monitor`, `kernel`, `kb_fetch`, `kb_build_ollama`) têm `test_<módulo>.py` dedicado. |
| `conftest.py` | Fixture `fake_pack_ctx`: patcha `write_pack`, `render_prompt`, `_carta_text` em 3 linhas (E6). |

> Mapa skill↔runtime (qual módulo executa cada etapa do SDD, quem produz/consome cada artefato):
> [`../SDD_RUNTIME.md`](../SDD_RUNTIME.md).

> Governança (quem propõe, quem aprova, quem aplica, o que é imutável) com desenhos:
> [`../docs/GOVERNANCE.md`](../../docs/GOVERNANCE.md).

> Convenção de nomes (identificadores em inglês, glossário de abreviações aceitas — KB/TM/scene_id… — e o
> **contrato congelado** de nomes de artefato/CLI/`project.json`): ver [`../docs/NAMING.md`](../../docs/NAMING.md).

## Uso

```bash
# 1) materializa o estado consultável (idempotente)
python framework/runtime/state_index.py projects/<projeto>

# 2) monta o contexto limitado de uma cena (determinístico)
python framework/runtime/context_pack.py projects/<projeto> <cena>

# 3) roda a cena ponta-a-ponta (assinatura: para em 'awaiting' se faltar tradução)
python framework/runtime/run_scene.py projects/<projeto> <cena> [--backend in-session|api] [--require-back] [--no-verify]
```

`<cena>` = subdir em `artifacts/scenes/` (ex.: `ch_12_01`). Genérico: nenhum dado de obra aqui; tudo vem de
`project.json` + artefatos. Sem rede no caminho `in-session`. Sem work-text nos `.py` (travado por teste).
