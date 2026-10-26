# Changelog

Todas as mudanças significativas do framework são documentadas aqui, em ordem cronológica
(mais recente primeiro). Numeração de versão via `VERSION` + tag `vX.Y.Z` desde a v1.0.0
(ver `docs/adr/0013-versionamento-semver-manual.md`); as seções abaixo continuam
organizadas por período, não por versão.

---

## 2026-10-23 — `spoiler_check`: termo em tabela de sistema não é vazamento

- Causa raiz dos 2 alertas permanentes do Prelude (`NameTextData:7`, `UnitTextData:218`): o `check()` varria toda unidade traduzida, inclusive as tabelas de nomes/unidades do jogo, onde o dado de origem já traz o termo proibido (e o ledger marca `beyond_frontier`, "sempre futuro"). Nenhuma cena da história cita o termo.
- Agora unidade fora de `artifacts/ordem_cenas.txt` vai para `check_tabelas()` (informativo, sem a fala) e para `tabelas_com_termo` no `spoiler_audit.json`; só cena da história entra em `name_leaks`/`clean`. Sem `ordem_cenas.txt`, nada muda (toda unidade conta como cena).
- Testes: tabela fora do vazamento, só-tabela deixa o audit limpo, sem `ordem_cenas.txt` mantém o comportamento antigo.

## 2026-10-21 — janela do lote em Haiku e benchmark A × B

- `rodar_ondas.ps1`: `-Modelo` passa a `haiku` por padrão (decisão do usuário). Medido em 8 ondas intercaladas (lotes 12–19, mesmo teto de 380 falas): o overhead da janela é ~US$ 0,03 por onda; `-Esforco low` e `-PrefixoEstavel` só atuam nela (ganho possível < 3% do custo) e ficam opcionais. A diferença aparente de ~20% entre os braços era ruído de cena (o Sonnet 5d varia de US$ 0,25 a 0,62 por onda).
- `resumo_lote.py`: tabela por onda (falas, US$/fala, janela, 1º turno de cache, tradutor, 5c/5d). Novos: `ab_benchmark.ps1` (driver A/B intercalado com teto de cota), `ab_resumo.py` (tabela A × B), `framework/runtime/cota_uso.py` (lê a cota 5h/7d), e o `vigia_lote.sh` avisa a cota e não acusa mais "PARADO?" falso no início do lote.
- Passo 5d (skill `rodar-onda`) só retraduz `critical`; as `high` ficam com o Haiku (ADR 0023, decisão do usuário). Revisão cega de 56 falas `high`: Haiku aceitável em 91,1%, Sonnet vence 50% dos pares com vencedor. Salvaguarda: reprovação > 10% na amostra de revisão devolve o Sonnet às `high`.
- `run_scene`: trava de rebaixamento de risco (`risk_piso_<cena>.json`, no `.gitignore`): o `risk_level` de uma fala só sobe entre rodadas da mesma cena; a rodada que rebaixar é barrada com `risco rebaixado`. Disparou em lote real (1 vez, 47 falas) e a cena fechou `verified` na rodada seguinte.

---

## 2026-10-21 — tabelas de sistema na descoberta e triagem de termo

- `connectors/scene_scope.py`: strings e `byte_budget` por categoria, separando tabelas de sistema (id fora da forma das cenas da história) das cenas; avisa quando falta `ordem_cenas.txt`. `panorama.py` passa a mandar as tabelas para o fim por classificação, no grupo `tab`. Entra na Fase 0 (`00_extraction.md` 2b, onboarding).
- Glossário privado (`artifacts/glossary.local.csv`, mesmas colunas do `glossary.csv`): nome de spoiler e afins que o repo público não pode carregar. Soma ao glossário em `context_pack.load_glossary` (prompt da cena), `glossary_lint` (inclusive com DB) e `kb_phase._kb_blob` (termo coberto não volta como candidato a nome). `*.local.csv` entra no `.gitignore` e no `content_guard` (bloqueado em qualquer pasta). O `kb_gate` também exige `updated_date` no arquivo privado (coluna e data em cada linha), com ou sem DB.
- `spoiler_audit.json` saiu da allowlist do guard e entrou no `.gitignore`: o relatório traz o par personagem ↔ nome verdadeiro ainda não revelado. Continua sendo gerado e lido localmente (`spoiler_check`, `run_chapter`); só deixa de ser versionado.
- `content_guard`: extensão `.sh` liberada, só para o vigia do lote (`vigia_lote.sh`, roda sob o Monitor do Claude Code; não cita conteúdo de jogo).
- Alertas de correção pendente: `alerts.correcoes_pendentes` / `alertar_correcoes_pendentes` listam as cenas paradas por defeito da tradução que ninguém corrigiu (resultado `correcao_pendente`, uma vez por parada, via `_ts`). Chamado pelo `resumo_lote.py` ao fim do lote (sem carência) e pelo `wave.run` na entrada da onda seguinte, passada a `CARENCIA_CORRECAO` (30 min) e sem contar as cenas que a própria execução está refazendo.
- `kb_gate`: exige `updated_date` no `glossary.local.csv` (coluna e data em cada linha), com ou sem DB (`_check_dated_header`).
- `projects/utawarerumono_prelude/connector/extract.py`: grava `ordem_cenas.txt` sozinho a partir do `EventManagerData.bin` do `DataBase.sdat` ao lado da fonte (`story_order`, `write_story_order`; sem o arquivo mantém a ordem anterior ou avisa "ordem NAO confirmada"). Reproduz as 275 cenas da ordem anterior; `test_story_order.py`.
- Runner de lote (`rodar_ondas.ps1`, `lancar_lote.ps1`, `vigia_lote.sh`, `resumo_lote.py`, skill `rodar-onda`): transcrição do console por lote, vigia que lê `-Lote`/`-Ondas`, `lancar_lote.ps1` abre a janela fora da sessão, aviso no resumo quando as requisições por fala passam de `MAX_REQ_FALA`, prompt da onda proíbe `Monitor`/`run_in_background` e `scene-translator.md` ajustado. `onda_fim.py`: o `rodar_ondas.ps1` usa a última linha com a forma do contrato (`ONDA_OK`/`PARADA`/`FIM`), mesmo com texto solto depois dela; antes só valia a última linha do log e onda boa virava "fora do contrato" (exit 3). Não feito: encerrar o `claude -p` à força quando ele escreve `ONDA_OK` e não sai (precisaria de `--output-format stream-json`).
- `hitl.py`: `ratify` lê também o `glossary.csv` quando o banco está atrás; aviso de voice card ignora `npc`/`system`/`unknown`.
- Limites do dia fechados: `alerts.py correcoes <projeto> [--carencia S]` (CLI) e `vigia_lote.sh` chama a cada passo, entao a correcao pendente alerta mesmo sem `resumo_lote.py` e sem onda seguinte; `kb_phase onda` avisa quando roda sem `wordfreq` (triagem so pelo vocabulario do jogo); `kb_gate` confere o `glossary.local.csv` alem da data (regra de tratamento valida, traducao onde a regra pede, termo repetido, termo que tambem esta no glossario publico).
- `resumo_lote.py`: o custo do lote conta só as sessões que nasceram depois do disparo; a sessão principal (que lançou o lote e seguia trabalhando) saía somada e inflava custo e overhead (lote 9: $7,16 / 80% → $3,80 / 62%). Mostra a linha "Fora da conta". `vigia_lote.sh` reconhece `ONDA_OK` em log que começa com BOM.
- `session_usage.py`: requisição de subagente sem cena (retradução do passo 5d, retrotradução; subagente de várias cenas) deixa de ser `overhead` e vira `agent` na cena `_session`, com `agent_type` lido do `.meta.json`. Overhead do lote 9: 62% → 33% (US$ 1,26 de US$ 3,84, a orquestração de fato); o custo total não mudou. `resumo_lote.py` mostra os subagentes por tipo. Ledger do Prelude refeito com `rebuild`. Teste em `test_session_usage.py`.
- Alerta falso de `run_scene` rc=1: as paradas por defeito da tradução (`build_plan_failed`, `verify_failed`, `schema_failed`) agora imprimem `CORRECAO DA TRADUCAO` (`events.CORRECAO_MARCA`) e o `wave` não as alerta; só `Traceback` ou erro de infraestrutura alertam. O que ficar parado sem correção é alertado uma vez por parada (`alerts.alertar_correcoes_pendentes`, resultado `correcao_pendente`): ao fim do lote pelo `resumo_lote.py` e, em onda manual, na entrada do próximo `wave.run` depois de `CARENCIA_CORRECAO` (30 min), sem contar as cenas que essa execução está refazendo.
- `kb_phase onda`: candidatos em dois grupos (provável nome × palavra comum/rótulo de interface) por frequência da palavra na `source_language` (`wordfreq`, opcional) e vocabulário do jogo, sem lista escrita à mão.

---

## 2026-10-20 — retrotradução por nível de risco configurável

- `back_translation_risk` no `project.json` (padrão `["high","critical"]`, sem mudança para quem não declara): `artifact_io.back_risk_levels` alimenta `back_translate` e `quality_gate` (ADR 0022). Prelude: só `critical`.

---

## 2026-10-17 — v2.1.0: conserto de atrito da onda

MINOR (ADR 0013): parâmetros e campos novos (`--scenes` em `glossary_lint`/`quality_gate`, `code` nos eventos, `entry_problems` no `wave`) com default que preserva o uso anterior; nenhuma flag removida nem schema quebrado.

- Estado gravado com segurança (ADR 0018): `paths.atomic_write` (temporário + `os.replace`) para `run_state.json`,
  `translations_*.json`, estado do `hitl` e `state/`; `paths.append_line` (append sob trava) para `events.jsonl`,
  `metrics.jsonl`, `hitl_log.jsonl`, `warnings.jsonl`, ledger e demais logs `.jsonl`. No Windows o `open('a')` com
  vários processos perdeu/misturou linhas em medição (27 de 1800 corrompidas); sem trava, queda no meio deixava JSON
  truncado. `cost._ledger_append` perde o fallback sem trava. `locked` ganha o parâmetro `stale` (padrão = `timeout`).
- CI: `ml-coverage-optional.yml` roda também em PR e push na `main` (antes só semanal); issue de falha só no agendado.
- Auditoria ciclo 2: gravação atômica também em `scene_lifecycle` (`run_state` ao descontinuar), `quality_review`,
  `back_translate`, `scene_dedup`, `tm_updater`, `tm_correct`, `risk_triage`, `quality_fix` e `translate_checkpoint`
  (relatórios regeneráveis ficam com `write_text`). `wave.py` ganha `--step-timeout` (padrão 3600 s; passo travado
  para a onda com exit 124); `risk_triage_run` (900 s) e `session_lot check` (3600 s) também têm timeout.
  Tipos: mypy passa sem `--follow-imports=silent` (anotações em `opcodes`, `hitl`, `session_usage`).
- `db/store.py`: espera de até 30 s por escrita concorrente (`timeout`), docstring deixa de dizer WAL (não é usado).
- `wave.py`: onda de várias cenas grava `wave_last_<primeira>_+N.log` (antes sobrescrevia `wave_last.log`).
- `risk_triage_run.py`: `claude` fora do PATH vira mensagem clara; `cli ollama-pull` recusa nome começando com `-`.
- `session_part.py`: erro claro quando o lote não tem as seções 7 e 8; testes novos (`session_part`, `session_lot`).
- Gate da onda por cena (ADR 0017): `quality_gate.py --scenes` bloqueia só item das cenas do pedido (resto vira aviso);
  `wave.py` passa as cenas aos dois gates e, para não perder pendência, recusa abrir onda nova (cena sem pack) com
  escalonamento aberto de outra cena (`wave.entry_problems`).
- `run_scene`: os eventos `build_plan`/`verify` com `result=fail` ganham `code` (token, newline, byte_budget, tabela,
  risk, round_trip, outro) e `reason` passa a ser a 1ª linha de erro depois do cabeçalho `ERROS:`/`FALHAS:`.
- `model.read_translation`: `translations_<cena>.json` do subagente em cp1252, JSON quebrado ou sem `lines` vira
  `invalid_translation_file` (evento `translate` com `result=invalid_output` e `backend`), com a instrução de regravar em
  UTF-8; antes saía `api_translate_failed` sem causa. A outra codificação nunca é aceita.
- `hitl.py resolve`: aceite de escalonamento do tradutor (sem `term`) passa a ser contado à parte ("N aceite(s) do
  tradutor"); "alias no glossário" e o aviso de `state_index.py` só aparecem quando o glossário mudou de fato.
- `glossary_lint.py --scenes` (o `wave.py` passa as cenas do pedido): só achado dessas cenas bloqueia; achado de outra
  cena vira aviso (exit 0, lista em `outside` no JSON). Antes um achado de cena fora da onda parava o `wave`.
- `hitl.py resolve`: escalonamento do tradutor (`kind=tradutor`) sem `term` e com `alias` preenchido é aceito
  como está (limpa `escalate`, entra no `hitl_log`); antes ficava em aberto para sempre (17 de 23 no utawarerumono_prelude).
- `run_scene`: os eventos `build_plan`/`verify` com `result=fail` ganham `reason` (1ª linha de erro da saída, até 160
  caracteres) no `events.jsonl`; antes só o `exit`.
- `connector.data_dir_default` (caminho relativo ao projeto, nunca absoluto) em `project.json`: o `run_scene` usa
  quando a env de `data_dir_env` não está setada (a env setada sempre vence); subagente deixa de exportar a variável.
- `phase_marks.jsonl` do utawarerumono_prelude: rótulos soltos `translate` e `3.` fundidos na fase `3` (dado local).
- `content_guard.py`: `.ps1` entra na allowlist de extensões (e na CI, que usa o mesmo guard), para versionar o
  lançador `.claude/skills/rodar-onda/rodar_ondas.ps1` (modo contínuo da skill `rodar-onda`: uma sessão
  `claude -p` por onda, para na primeira `PARADA`/`FIM`/erro; Windows/PowerShell). Teste em `test_content_guard.py`.
  O lançador passou a ser versionado depois que a allowlist com `.ps1` chegou à `main` (Onda 1).
- Camada de controle `.claude/` (modo contínuo, sem mudança no runtime): `rodar_ondas.ps1` ganha `-Lote N`,
  `logs/estado.json` (próxima onda e nº do lote), espera do limite de sessão da assinatura (refaz a onda após o
  horário de liberação, até 3 vezes) e chama `resumo_lote.py` na saída (cenas e falas do lote, custo, overhead, fim
  de cada onda; lê só `api_ledger.jsonl` e `run_state.json`). Skill `rodar-onda`: passo 5c (retrotradução Opus das
  falas `high` quando o `quality_gate` acusa `SEM COBERTURA`) e escalonamento que **para** a onda com tabela, em vez
  de ser adiado (o gate bloqueia a onda seguinte com escalonamento aberto). `scene-translator.md`: nunca cortar termo
  `manter_original` ao abreviar para o `byte_budget` e conferir o `glossary_lint` das próprias cenas antes de
  encerrar (as paradas das ondas 6 e 8 vinham disso). Ainda sem teste de ponta a ponta.

- `run_scene`: antes do `build_plan` imprime `[pre]` com as falas que já se sabe que vão falhar (quebra de linha
  real no JSON; contagem do token de quebra diferente da fonte; `model.precheck`) e conserta o mecânico
  (`model.fix_newlines`: quebra real → token, token a mais que a fonte não tem sai; o que o caminho api já fazia).
  Estouro de `byte_budget` fica de fora de propósito: no utawarerumono 7 de 26 cenas verified têm fala acima do
  budget por linha (o conector não o impõe por fala), então seria falso positivo; o `_fitting_loop` segue
  reagindo ao exit 3 do verify. Antes cada erro custava uma rodada.
- `hitl.py resolve` tira o `escalate` da fala decidida; antes o `collect` da onda seguinte a recolhia de novo.
- `wave.py` com uma cena só grava `artifacts/wave_last_<cena>.log` (subagentes em paralelo não se sobrescrevem);
  o `scene-translator` passa a usar `scratch/<CENA>/` para temporários.
- `kb_phase.py <projeto> onda --scenes <cenas> [--max N]`: lista os candidatos de lore/nome sem forma na KB só
  nas cenas da onda (vizinhança com teto, como o RAG da API), inclusive os que aparecem 1x; filtra gemidos
  (`Mmm`, `Uhhh`). Roda antes de traduzir, para a decisão vir uma vez só em vez de virar escalonamento por cena.
  Não bloqueia. Limite medido: só enxerga nome com inicial maiúscula (ver benchmark no ROADMAP do projeto).
- `kb_phase._scan`: o token literal de quebra (barra-n) vira espaço (antes grudava na palavra seguinte: "nbecause") e
  nome composto não cruza mais o fim de uma fala com o início da próxima (`_CAP_RUN` só junta espaço/tab).
- `kb_phase.discover`, causa raiz do ruído: maiúscula de início de fala não prova nome. Nome composto só é forte
  com ocorrência em meio de frase (antes bastava ser composto: "Battle Results", "Guide X", "Including X"); palavra
  cortada por `--` ("Wha--") deixa de ser candidata; 's/'ll/'d/'re/'ve/'m colados saem do candidato. No jogo todo,
  `gap` 91 → 65 e `onda` 128 → 100, só removendo composto de verbo/título + nome , interjeição e título de interface entre colchetes (`[About ...]`).
- `kb_phase onda`, truecasing: vocabulário em minúscula do jogo todo (`_lower_vocab`). Palavra comum no início de um
  composto é aparada quando o resto nunca aparece em minúscula ("Guide X" → "X"); candidato que nunca aparece em
  minúscula e recorre em 2 frases com companhia (`_company`; som solto como "Plop!" fica de fora) entra na lista da
  onda mesmo só em início de fala; risada (`Nyahaha`, `Hohoho`) é interjeição.
- Testes em `test_model.py`, `test_hitl.py`, `test_wave.py`, `test_kb_phase.py`; suíte 626 passed.

## Não lançado — fila diferida de `revise` e espera do reset (MINOR, sem bump ainda)

- `wave.espera_esperada`: passo que sai com código ≠ 0 só porque a sessão ainda tem de traduzir ou retrotraduzir (`AGUARDANDO …`, `SEM COBERTURA`, `REVISAR`, `ESCALONAMENTO`, sem marca de erro) não gera mais o evento `alert`.
- `estimar_lote.py` (ritmo = mediana de min/fala dos logs de onda × plano do `panorama.py`; `--estado` = cenas `verified` e idade do último evento).
- `rodar_ondas.ps1`: estimativa no início, onda num job com batimento a cada 3 min, contagem regressiva na espera de cota, `-Teste` sem log de onda nem resumo de lote, aviso de `estado.json` mais velho que o `run_state.json`; `lancar_lote.ps1` (janela fora do Claude Code) e `vigia_lote.sh`.
- O fim do lote não para mais por causa da fila de escalonamento: o `--fechar` e a tabela de pendências ficam para o `FIM`.

ADR 0021. Com `"hitl_fila": "diferida"`, `quality_gate --scenes` só avisa de `revise` (bloqueia no `--fechar`; cobertura
continua bloqueando); sem a chave nada muda. `framework/runtime/espera_reset.py` lê o aviso de limite de sessão ou de
semana e o `rodar_ondas.ps1` espera o reset e refaz a onda (até 8 vezes). `obs_report` deixa de repetir falha de cena que
depois fechou `verified`. Skill `rodar-onda`: passo 5e (Sonnet reescreve `revise`, até 2 tentativas) e formato do `offset` no 5c.

## Não lançado — Onda 3: medição (PATCH, sem bump ainda)

- Performance: `runtime/perf_bench.py` mede `append_line`, `build_pack` (sem busca semântica) e `state_index_tm` sobre dados sintéticos, como razão contra uma carga de calibração da própria máquina; `perf_baseline.json` guarda o baseline e regressão acima de 2× vira `::warning::` (`--strict` sai com 1). Workflow `perf.yml` registra a tendência a cada PR/push sem bloquear. `test_perf_bench.py` falha se o baseline não cobrir uma operação ou a detecção de regressão quebrar.
- Observabilidade: `events.validate` define o schema dos eventos (campos, etapas conhecidas, só escalares, texto ≤ 200) e um teste falha se o código emitir etapa fora dele; `obs_report` ganha os indicadores taxa de sucesso da onda e custo por cena; `alerts.py` + `wave.py`: falha, timeout ou bloqueio de entrada geram evento `alert`, `alerts.jsonl` e webhook opcional (`TCF_ALERT_WEBHOOK`). `alerts.py` e `perf_bench.py` entram no mypy.
- Custo: teto de gasto por onda com parada dura. `wave.py --max-usd N` (ou `budget.max_usd_per_wave` no project.json) soma o ledger desde o início da onda, confere a cada segundo enquanto um passo roda e mata o passo (e os processos filhos) quando passa do teto; não abre o passo seguinte acima dele. Sai com código 4 e gera alerta `budget`.
- Contexto/RAG: `framework/db/rag_eval.py` mede recall@1/3/5 e MRR da busca semântica com o modelo real num corpus sintético de 40 casos (frase indexada × consulta parafraseada); `test_rag_eval.py` roda no job `ml-coverage` (que alimenta o `All checks`) e falha se o recall cair abaixo do piso (0,85/0,95/0,95) ou mais de 0,05 abaixo do `rag_eval_baseline.json` (medido: 0,95/1,0/1,0). Para regravar o baseline após mudança deliberada de modelo: `python framework/db/rag_eval.py --write-baseline`.
- Custo: `cost_reconcile.py <projeto> --invoice AAAA-MM=USD [...]` concilia o gasto da API paga do ledger com a fatura do provedor, mês a mês; sai 1 se a diferença passar de 5% da fatura (`--tolerance`) ou se houver fatura sem gasto no ledger. Os valores da fatura são digitados pelo usuário: o framework não tem acesso ao faturamento.
- Custo: `cost_integrity.py` confere o ledger linha a linha (campos obrigatórios, nenhum contador de uso negativo, `cost_usd` da API paga igual ao recalculado pela tabela de preços, linha de sessão com `cost_usd` 0) e `test_cost_integrity.py` roda a regra em todo `api_ledger.jsonl` do repo. Achou e corrigiu um bug real: `session_usage._usage` gravava `cache_write` negativo quando o transcript trazia `ephemeral_1h` maior que o total de cache criado (8 linhas no bof4 e no utawarerumono); agora o 1h é limitado ao total. Ledger do bof4 refeito (`session_usage rebuild`).

## Não lançado — Onda 2, fechamento para a nota 4 (PATCH, sem bump ainda)

- Varredura em `test_state_writers.py` sem lista de excecoes: todo `write_text`/`write_bytes`/`open("w"|"a")` do framework tem de estar numa funcao que usa `atomic_write`/`atomic_write_csv`, `append_line`, `locked` ou tmp + `replace`. Nao ha classificacao manual de "estado" x "regeneravel": os ~38 pontos que gravavam direto (prompts, packs, CSVs de revisao, relatorios, lotes temporarios, log da onda, scripts de `distribution/`) foram migrados. Escritor novo, ou escrita fora de funcao, falha o teste.
- Quatro escritores de estado que a lista antiga nao enxergava foram migrados para `paths.atomic_write`: fila de revisao (`hitl._write_queue`), alias no glossario (`hitl._add_alias`, agora sob `paths.locked`, preserva BOM e CRLF), planilha do revisor (`review_page.save`) e `connector_manifest.json` (`fingerprint_monitor.write_manifest`). `atomic_write` passa a aceitar bytes.
- `run_scene --jobs` ganha `--scene-timeout` (padrao 3600 s): cena travada vira rc 124 e nao trava o lote. Com isso todo subprocesso do pipeline tem timeout; `claude -p` ja tinha (900 s, ate 3 tentativas).

## Não lançado — ML obrigatório e lock com hash

- `requirements-dev.txt` passa a ser lock com hashes (`requirements-dev-src.txt` é a fonte; `uv pip compile --universal --generate-hashes`). Instalação verificada com `--require-hashes` em Python 3.11 e 3.12, hash adulterado recusado, `pip-audit` limpo sobre o lock. Teste novo em `test_docs_integrity.py`.
- Cobertura real do ML virou obrigatória: `ml-coverage-optional.yml` é workflow reutilizável chamado pelo job `ml-coverage` de `test.yml`, que entra no `needs` de `all-checks` e `mark-staging` (a branch protection não muda). Teste impede remover do agregador.
- "Require review from Code Owners" fica desligado de propósito: com um único autor, travaria os PRs dele mesmo.

## Não lançado — Onda 2: integridade e concorrência do estado (PATCH, sem bump ainda)

- Escrita segura de estado que ainda gravava direto: `project.json` (`kb_phase.apply_frontier`, uma queda no meio
  destruía o manifesto), tradução (`session_lot._save`), `research_log.md` (`kb_reconcile.promote`), CSV de aprovados
  (`tm_correct`, `connector_io.sync_translations_db`). Novo `paths.atomic_write_csv`.
- Concorrência: `session_usage.rebuild` reescrevia o ledger sem trava e perdia linhas de API anexadas ao mesmo
  tempo (teste com processos paralelos falha 3 de 3 no código antigo); `hitl._ratify_csv` passa a gravar sob trava.
- Leitura: `paths.read_json` (arquivo corrompido levanta `StateCorrupt` com arquivo, posição e como recuperar, sem
  recriar o estado em silêncio) e `paths.read_jsonl` (linha truncada de ledger/log é ignorada com um aviso, em vez
  de derrubar a leitura). Adotados em `run_scene._checkpoint`, `cost_report`, `session_usage.marks`, `hitl`,
  `state_index`.
- `test_state_writers.py`: lista de escritores de estado que não podem usar `write_text` direto (só cresce) e testes
  de queda no meio da troca, corrupção e concorrência.

## Não lançado — Onda 1: CI, segurança, configuração e docs (PATCH, sem bump ainda)

- `validate.py`: `project.json` com campo de tipo errado (ex.: `"hitl": "true"`, `"batch_size": "30"`) agora é
  ERROR na validação, em vez de falhar sem aviso no runtime. Campo ausente continua válido. Teste confere também
  todos os `projects/*/project.json`.
- `test_docs_integrity.py`: ADRs sequenciais, com título e status válidos; `VERSION` igual à última versão do
  CHANGELOG; todo teste do embedder listado no workflow de cobertura de ML (a falha de cobertura do PR #86 teria
  sido pega aqui).
- `.github/CODEOWNERS` (dono em todo o repo); `content_guard.py` aceita o nome `CODEOWNERS` (o GitHub exige esse nome exato, sem extensão).
- `SECURITY.md`: seção "Texto do jogo como dado não confiável" e runbook de rotação de chave;
  `test_untrusted_text_boundary.py` falha se uma chamada de LLM ganhar `tools`/`tool_choice`, se a triagem perder
  `--allowedTools ''` ou se as ferramentas do `scene-translator` forem alargadas.
- CI: job `windows` (suíte completa em `windows-latest`) entra no agregador `all-checks`.
- `rodar_ondas.ps1` versionado (linha do `.gitignore` removida).

## Não lançado — correção de medição (PATCH, sem bump ainda)

`session_usage.py`: o custo de sessão sumia do ledger quando a sessão só chamava `wave.py`, porque a cena só
era aberta por `run_scene.py` na linha de comando e `wave.py` chama o `run_scene` por dentro. Agora os dois
abrem a cena (`_RUNNER`); teste de regressão em `test_session_usage.py`. O `rebuild` recupera o custo perdido.
`wave.py` agora ecoa (`phase_lines`) as linhas `AGUARDANDO traducao|back-translation` e `status final =` do
`run_scene`, que são o que o `session_usage` lê para separar tradução de governança e fechar a cena na janela;
teste em `test_wave.py`. Sessões gravadas antes disso ficam sem a divisão por fase (a transcrição não tem o sinal).

## 2026-10-14 — v2.0.0: pós-bof4, o que subiu do projeto para o framework

MAJOR (ADR 0013): a flag `--skip-connector-gate` foi removida (o gate não tem mais bypass), projeto com `db` passa a exigir `requirements-ml.txt` e a cópia intocada do `_skeleton` é bloqueada pelo `connector_gate`. Além disso, só adições (caminho de sessão em lote, patcher, `touched`, `scene_dedup`, `budget`, skills `08b`/`08c`). Lições do bof4 levadas ao framework (tag `v2.0.0` depois do merge da PR). Só framework;
os dados do projeto ficam em `projects/`.

- **Distribuição** (fee19ba, e5821a3, 33100ca): `framework/distribution/` com patcher genérico de
  um clique (delta binário, sem conteúdo do jogo) e a skill `09_distribution`. O patcher não estoura
  quando o `tasklist` devolve saída fora do UTF-8; `build_exe` grava em `<projeto>/output/` por padrão,
  recusa saída dentro de `dist/` e deixa `work/` numa pasta temporária.
- **Reconferência só do que mudou** (19452bb, 6084b1e): `touched.py` + `run_scene` pulam cena `verified`
  sem fala tocada (`--full` força); `run_scene --jobs N` reconfere cenas em paralelo (processo por cena,
  `run_state` sob trava); a retrotradução é re-julgada por fala (só as stale), não por cena (3d289d5).
- **Texto repetido e lote** (e93d4c2, 47530b3, b39a4de): `scene_dedup.py` (traduz uma vez o texto repetido
  entre cenas; agrupa pela coluna de texto-fonte e remapeia offsets no JSON parseado), ligado ao
  `wave.py`; `session_lot.py` (`plan/prompt/check/go/split/join/install`).
- **Triagem de risco e onda** (ae11e96, 8ab904c): `risk_triage_run.py` só lista e só chama o modelo
  (pago) com `--go`; `wave.py` copia só as cenas pedidas.
- **Bytes e largura de caixa** (d0c1e30, 5c7827a, 80f55da): `budget.py` vira fonte única da conta de
  bytes (+ `byte_budget_exceptions` no `project.json`), usada também pelo `session_lot`; largura de caixa
  derivada do inglês (`box_width.py`), tabela de opcodes com parâmetros (`choice_start` quebra caixa) e
  lint de largura antes da amostra; a regex `_PTPT` do `quality_review` ficou mais estreita.
- **Revisão e correção** (00fa261, 29a7578): `review_page.py` (página de revisão local, `--serve`);
  `tm_correct` com escopo por linha e medida de bytes no dry-run.
- **Fase 0 e portões** (300509e, 81029a9, 4b6027e): `connectors/scope_scan.py` (o que o `dialogs.csv`
  não cobre); `run_chapter`/`run_game` passam pelo portão de caminho (HITL + chave + cena de sistema);
  gates e relatórios saem com código != 0 em pasta que não é projeto.
- **Medição** (77dbe7f): o medidor de tokens ganha o ajuste do sonnet-5 e o erro da estimativa entra no relatório.
- **Skills** (280a7b6, ce51986): a 06c foi incorporada à 06b; entram `08b` (texto de sistema/rótulos) e
  `08c` (teste no jogo); a 06 ganha os dois caminhos de tradução; glossário, QA final e decisões de voz
  detalhados. As skills numeradas vão de 00 a 09.

---

## 2026-10 — entre v1.1.0 e v2.0.0

- **Modo DB vira default de projeto novo** (e3b6921): o template de `project.json` declara `db`; o
  banco nasce sozinho no 1º `run_scene`/`run_chapter` (mirror flat→DB no início do run). Projetos
  existentes sem `db` seguem em flat files, sem mudança.
- **Busca semântica vira default de projeto com `db`**: `sentence-transformers` e `sqlite-vec` entram
  nas dependências do pacote (o `pyproject.toml` passa a ler os pins de `requirements.txt` +
  `requirements-ml.txt`, fonte única); projeto com `db` e sem a stack instalada é hard-block no
  `kb_gate` (antes o RAG caía para vazio sem aviso). Opt-out explícito: `"db": {..., "semantic": false}` no
  `project.json` (o `demo` usa). `TCF_ALLOW_NO_ML=1` rebaixa o bloqueio a aviso (CI de push/PR).
  **Atenção ao atualizar**: projeto com `db` passa a exigir `pip install -r requirements-ml.txt`.
- **Scaffold completo** (e0869d1, 6f722fe, ad8c847): `scaffold_project` gera `project.json`, os
  artefatos de KB e um `connector/` copiado do `_skeleton` (com `test_roundtrip.py`,
  `test_roundtrip_synthetic.py` e `conftest.py`). A cópia intocada do `_skeleton` é hard-block no
  `connector_gate` — nenhum placeholder passa.
- **TM do DB só aprova cena `verified`** (de68c36, 3251bae): `build_plan` grava `approved=0`; a cena
  vira TM (`approved=1`) ao fechar o verify, em `state_index.approve_scene_db`, que já reindexa os
  embeddings na hora. A TM flat também passa a ler só cenas `verified` (df6bc41).
- **FlashRank removido** (3251bae): o ranking da busca semântica é só o cosine do bi-encoder.
- **`connector_hash` normaliza CRLF** (5745ec8): `run_state.json` versionado não acusa mais
  "conector mudou" ao trocar de plataforma.
- **Registros retroativos** (mudanças anteriores que ficaram sem entrada): o backend `ollama` de
  tradução foi removido (ADR 0008) — `--backend` aceita só `in-session`/`api`; `ollama_client.py` e
  `tcf ollama` ficam para o pipeline de KB. A issue do console cp1252 no Windows foi fechada: os
  CLIs principais forçam stdout UTF-8.

---

## 2026-09 — versionamento SemVer + CI hardening

- **v1.1.0 — loop de code review + RAG semântico + DB-first**. MINOR (ADR 0013):
  só adições (`tcf db validate-model`, `rag_min_score`, retrieval semântico da KB, produtores
  DB-first, tabelas novas no schema via `CREATE TABLE IF NOT EXISTS`). Correções de integridade
  que **passam a falhar alto onde antes corrompiam em silêncio** — se um pipeline seu depende do
  comportamento antigo, veja aqui: `--require-back` em modo batch agora bloqueia (`back_incomplete`)
  se a back-translation não fechar; BoF4 `extract`/`reinsert` com encode estrito; Utawarerumono
  `load_game` recusa traduções conflitantes pro mesmo offset; `split_scenes` aborta em colisão de
  id de cena. `connector.target_charset_supported` do BoF4 era a string `"ascii_only"` (o schema
  declara `bool`), agora `false`: o aviso de charset passa a entrar no prompt do BoF4. O wheel de
  `pip install .` agora inclui `schema.sql`, a carta de governança, templates e media-profiles
  (o da v1.0.3 saía só com `.py`). `--project-id` de `tcf db migrate` passa a defaultar em
  `project.json:db.project_id` (fallback `bof4`, sem mudança pros projetos atuais). `release.yml`
  agora exige `test.yml` verde no commit taggeado.
- **Chunking do RAG semântico documentado, `kb` vira kind indexável** (ADR 0014): o embedder
  nunca chunka — `_KIND_CONFIG` ganhou o kind `"kb"` (tabela `kb`, coluna `content`, nova tabela
  `kb_embeddings` no schema) reaproveitando a mesma indexação genérica 1-linha-1-vetor de
  `translation`/`decision`, porque a KB já chega pré-chunkada por seção markdown na ingestão
  (`migrate_from_flat._migrate_kb`). Convenção pra conteúdo tipo documento em projeto futuro:
  chunking é responsabilidade do parser que grava a tabela-fonte, nunca do embedder. Escopo
  ampliado na mesma issue: `Embedder.search_kb()` + `context_pack._load_kb_semantic()` injetam
  uma seção "5d. Lore SEMELHANTE (semântica)" suplementar (nunca substitui `select_kb` léxico),
  com o mesmo gate de spoiler e dedupe contra o resultado léxico. Validado com Embedder/sqlite-vec
  reais (não só skip de CI) e com a KB real do BoF4 (11 seções) — retrieval discrimina bem
  (query fora de tópico cai pra ~0.15–0.21 vs. ~0.26–0.56 nas relevantes), mas como nenhum projeto
  hoje tagueia `reveal` na KB, o gate default-deny mantém esse caminho invisível em produção até
  a KB de algum projeto ganhar essas tags.
- **Versionamento SemVer manual adotado** (ADR 0013): `VERSION` + tag `vX.Y.Z`, decisão de
  patch/minor/major é julgamento humano no momento de taguear, sem ferramenta nem enforcement de
  formato de commit. Primeiras tags reais: `v1.0.0`, `v1.0.1`.
- `release.yml` passou a subir `pip-freeze` (`pip freeze` da instalação usada na Release) como
  artifact — auditoria de que exatamente foi publicado; `.github/workflows/README.md` documenta
  procedimento de hotfix/rollback (yank via `gh release delete`, branch de hotfix a partir da tag).
- `dep-audit-optional.yml` (novo workflow): `pip-audit` de `requirements-kb.txt`/`requirements-ml.txt`
  (torch + sentence-transformers) saiu do job `deps` de `quality.yml` — instalar essas stacks opcionais
  do zero custava ~1min a cada push/PR pra auditar código que a maioria das mudanças nem toca — e virou
  checagem semanal (cron + `workflow_dispatch`, mesmo padrão do `api-smoke.yml`), com issue automática
  em falha (corrigido logo em seguida: o job novo não instalava o próprio `pip-audit` nem tinha
  `permissions: issues: write`, então falhava sempre que rodava).

---

## 2026-08/09 — pós-harness estável

Trabalho incremental sobre o harness estável abaixo: cobertura de testes, reestruturação
da CI, onboarding de baixo custo, Generic Connector System completo e terceiro jogo concluído.

- **`connector_gate` liberado para `trails_sky_sc` com verificação real**: cena piloto `mp0010_01`
  fechou o round-trip real contra o `.pac` instalado (`verify_chapter.py`: `{"ok": true,
  "fitting_failure": false, "n_fails": 0}`), após resolver 65 linhas em overflow (56 causadas pelo
  bug de off-by-one abaixo, 9 de overflow genuíno corrigidas manualmente) e sobreviver a um patch do
  Steam no meio do processo (jogo mudou de build entre a extração original e a verificação; corpus
  re-extraído, 414/448 linhas remapeadas automaticamente por diff de offset, 34 linhas órfãs
  retraduzidas). Checkpoint gravado em `run_state.json` via o mesmo caminho de sucesso de
  `run_scene.py`. Detalhe da investigação e da metodologia de remap em
  `projects/trails_sky_sc/artifacts/decision_log.md`.
- **Off-by-one do terminador corrigido por conector** (ver
  `docs/adr/0006-budget-reserves-terminator-per-connector.md`):
  `byte_budget` de `bof4`/`trails_sky_sc`/`translation_local`/`translation_software` já reservava 1
  byte pro terminador `\0` fisicamente no CSV, mas `model.py`/`context_pack.py` nunca descontavam
  esse byte do limiar usado pra decidir se uma tradução cabe — causa raiz de 56/65 linhas do
  overflow acima. Novo campo `budget_reserves_terminator` (mesmo padrão de
  `target_charset_supported`, default `False`); `utawarerumono`/`souldiers` inalterados.
- Cobertura elevada a 90.17% (core: runtime+db+skills+validation) com gate `--cov-fail-under=90`;
  438 testes coletados (435 passed / 3 skipped) na suite `framework/`
- CI reestruturada para paralelismo total: `test.yml` dividido em 6 jobs independentes (era 1 job de
  5 passos sequenciais: guard → mypy → coverage → 3 conectores); zero `needs:` nos 3 workflows
  (`quality.yml`, `test.yml`, `api-smoke.yml`)
- **Onboarding de baixo custo**: `scaffold_project.py` + self-check de `kb_gate.py` reduzem o custo
  de dar início a um projeto novo de ~40k para ~5k tokens; KB híbrida via Ollama local
  (`kb_fetch.py`/`kb_build_ollama.py`) gera rascunho sem custo de API, sempre sujeito a ratificação
  humana obrigatória antes de reconciliar (`kb_reconcile.py`)
- **Driver ponta-a-ponta**: `run_game.py` roda todos os capítulos/cenas de um projeto em sequência
  com teto de gasto global e retomada automática; `progress_report.py` cobre observabilidade de
  progresso do jogo inteiro (% concluído, linhas/min, ETA, taxa de falha)
- **Gate de completude de conector**: `connector_gate.py` bloqueia tradução sem conector completo
  (scripts presentes + ao menos 1 round-trip verde já registrado)
- **Generic Connector System completo**: descoberta automática de engine (`evidence_collector.py` +
  `tier_classifier.py`) evoluiu para um pipeline completo — validação de cobertura/consistência do
  candidato (`coverage_gate.py` + `adversarial_validator.py`), manifesto + fingerprint de conector
  (`fingerprint_monitor.py`), TM por série entre jogos da mesma franquia (`tm_lookup.py` +
  `tm_updater.py`), e gates de autonomia AI-agnostic (`existence_gate()` + `assert_fresh_read()`).
  Validado em três engines distintos: Aquaplus (Utawarerumono), Capcom DAT (Breath of Fire IV) e
  Unity Addressables (Souldiers)
- `kernel.py`: fachada fina consolidando `run_scene`/`run_chapter`/`run_game`/`validate_project`/
  `write_pack` sob um import único
- **Souldiers (terceiro jogo, terceiro engine) concluído**: 470/470 cenas verified, round-trip
  byte-idêntico 100%, back-translation 100% de cobertura, custo ~$3,06 USD
- Limpeza: `tm_search.py` (protótipo de busca semântica em `.npy` flat, órfão — superado pela busca
  via sqlite-vec já em produção em `framework/db/`) removido
- Nenhuma sigla de roadmap/débito técnico (`D1`–`D6`, `B1`–`B4`, `P1.7`, `P2.5`) nem os dois sistemas
  de tier numerado (`T1`/`T2`/`T3` de descoberta de engine; `T1`–`T4` da cascata de encaixe de bytes
  na reinserção) sobrevivem em código `.py` — renomeados para nomes descritivos em todo o repo
- **`split_scenes.py`**: gap achado no onboarding do `trails_sky_sc` (2026-08-23) —
  `run_scene`/`build_plan_chapter` exigem `artifacts/scenes/<cena>/dialogs.csv` (contrato congelado
  em `paths.py`), mas o `extract.py` de todo conector só escreve o `dialogs.csv` FLAT — não havia
  nenhuma ferramenta genérica no framework pra fazer essa ponte; BoF4/Souldiers/Utawarerumono tinham
  resolvido isso ad hoc, fora do framework versionado. Escopo deliberado: só cobre o caso em que 1
  coluna do corpus já identifica a cena 1:1 (`--by file`, padrão do BoF4/Trails Sky SC) — Souldiers
  (prefixo no offset) e Utawarerumono (`extract.py` já roda 1×/cena) ficam fora, não força um
  contrato que os 3 não compartilham. `test_split_scenes.py` (4 testes); documentado em
  `NEW_PROJECT_ONBOARDING.md` (passo 2b) e `ROADMAP.md` (item F)
- **Gap do `scaffold_project.py` corrigido**: o onboarding doc afirmava que o scaffold cria
  `profile/` (referência humana de vozes/terminologia exigida pelo checklist de gate), mas o código
  nunca criava — `profile/` ficava vazio até o Passo 5 do checklist notar, tarde. Descoberto no
  mesmo onboarding do `trails_sky_sc`. `scaffold()` agora materializa os 4 arquivos de referência
  (`voice_profiles_reference.md`, `terminology_seeds.md`, `identity_pairs_reference.md`,
  `example_test_suites.md`); trava de regressão em `test_scaffold_creates_profile_reference_files`
- **Doutrina de spoiler documentada na skill 03**: `spoiler_ledger.json` +
  `context_pack.select_spoiler_guards()` + `spoiler_check.py` já existiam no runtime (usados em
  `utawarerumono`), mas `framework/skills/03_knowledge_building.md` nunca os mencionava — a doutrina
  escrita mandava "não avançar para seções que revelam plot posterior" durante a pesquisa, o oposto
  do mecanismo real (pesquisar por completo, quarentenar o reveal no ledger, não na prosa do KB).
  Corrigido após o gap se repetir no onboarding do `trails_sky_sc`: nova seção "SPOILER LEDGER" na
  skill 03 com o schema completo da entrada, quando criar uma, e como o KB visível fica
  espoiler-safe; `spoiler_ledger.json` adicionado como artefato condicional aos OUTPUTS OBRIGATÓRIOS
- **Causa raiz do estouro de budget em `trails_sky_sc` corrigida (ADR 0005)**: `mp0010_01` tinha
  308/447 linhas `soft_failed`; não era o modelo traduzindo longo demais, era a métrica de orçamento
  errada. `_translit_len()` (comprimento sem acentos) era usado incondicionalmente em todo o
  pipeline (prompt, retry, escalonamento) — correto pra `bof4`/`utawarerumono` (cujo `reinsert.py`
  translitera de fato na gravação), errado pra `trails_sky_sc` (grava UTF-8 real: `"coração"` = 9
  bytes, não os 7 de `"coracao"`). O veredito `connector.target_charset_supported` já existia (Passo
  4 da skill 00) mas só controlava o texto do prompt, nunca a métrica de contagem. Agora
  `target_charset_supported is True` (checagem estrita de booleano) seleciona a métrica em toda a
  fonte única `model.py::_budget_len` (usada por `_over_budget`/`_budget_note`/`_over_offsets`/
  `over_budget_offsets`/`_api_translate`/`_ollama_translate`/`context_pack.render_prompt`) — bytes
  UTF-8 reais quando `True`, forma transliterada legada caso contrário. `bof4`/`utawarerumono` não
  regridem (cobertos por `test_budget_len_charset_false_or_missing_uses_translit`). Skill 00 e
  `NEW_PROJECT_ONBOARDING.md` atualizadas: `likely`/`unknown` devem resolver para `false` antes de
  ir pro `project.json`, porque agora o veredito tem dois efeitos (prompt + métrica), não só um
- **Paridade de retry por orçamento entre backends `api` e `ollama`**: `ollama` era "cidadão de
  segunda classe" no escalonamento de fitting — não tinha o retry por estouro de budget que `api` já
  tinha. `_ollama_translate` ganhou o mesmo mecanismo (`_over_budget`/`_budget_note`,
  `test_ollama_translate_retries_over_budget`) e passou a traduzir em **lotes** de
  `OLLAMA_BATCH_LINES` (novo, default 40; `test_ollama_translate_batches_across_multiple_calls`) em
  vez da cena inteira numa chamada só — a janela de contexto local (`OLLAMA_NUM_CTX`, novo, default
  12288) é pequena pra caber numa GPU de consumidor, e mandar a cena toda de uma vez trunca em
  silêncio sem erro (virava linha "sem tradução" no build_plan). Timeout por chamada subiu de 600s
  para 1800s, medido na RX 6650 XT (~6,2 tok/s com ~57% offload GPU, 14B). `_fitting_loop` em
  `run_scene.py` passou a escalonar tolerância também no backend `ollama` (antes só `api`) — escolha
  de backend fica só com o humano (`--backend`), nenhuma opção é uma armadilha sem retry de budget
- **Retry de token de formatação do engine perdido/corrompido**: bug real medido em `mp0010_01`
  (2026-08-24): 7/447 linhas o LLM derrubava ou trocava tokens de formatação do engine (`<C1>`,
  `<P2>` etc.) e o retry existente só checava paridade de quebra de linha (`\n`), não esses tokens —
  passava paridade e ia pro build_plan quebrado. `model.py::_struct_ok`/`_structural_rx` (mesma
  checagem de regex que `build_plan_chapter.py` do conector já fazia depois, agora também DENTRO do
  retry de tradução, antes de persistir) comparam o multiset de tokens da fonte vs. tradução em
  ambos os backends (`api`/`ollama`); `test_ollama_translate_retries_on_dropped_structural_token`
- **Diagnóstico de fitting persistido**: `run_scene.py::_persist_fitting_diagnostics` — quando o
  fitting esgota o escalonamento (ou falha dura), grava as linhas ainda acima do budget em
  `verify_diagnostics_<scene_id>.json` (`paths.verify_diagnostics`, novo), passivo (só lê o que já
  foi gravado, não gera trabalho extra de modelo). `model.py::over_budget_offsets` ganhou
  `detail=True` pra devolver offset/budget/atual/source/tradução em vez da lista nua de offsets
- **Bug pré-existente documentado (não corrigido)**: `PYTHONIOENCODING`/console cp1252 no Windows
  quebra `print()` com acento/seta com `UnicodeEncodeError` — reproduzido de novo
  23/08/2026 no bring-up do `trails_sky_sc`. `NEW_PROJECT_ONBOARDING.md` agora exige setar
  `PYTHONIOENCODING=utf-8` (ou `chcp 65001`) antes de rodar qualquer CLI do framework em ambiente
  novo — nenhum projeto até hoje foi bloqueado porque o texto-fonte é ASCII, mas é verificação
  obrigatória daqui pra frente
- **Escalonamento de modelo no retighten de fitting (`MODEL_ESCALATION`)**: o loop de aperto de
  budget (`_fitting_loop` em `run_scene.py`) já escalava a *tolerância* de bytes em tiers
  (`BUDGET_ESCALATION = (1.15, 1.0)`); agora escala também o *modelo* no backend `api`, pareado por
  índice com a tolerância — tier tol=1.15 (folga maior, resolve a maioria) usa `claude-haiku-4-5`
  (barato); só o resíduo que nem 1.15 resolveu (tol=1.0 — sinal real de dificuldade medido, não
  suposição a priori de quais linhas são "difíceis") escala para `claude-opus-4-8`. Backend `ollama`
  fica de fora (modelo local único, sem tiering — `model=None` sempre). Evita a pegadinha de
  atribuir haiku/opus por linha antes de saber quais linhas de fato precisam do modelo caro.
  `config.py`: `MODEL_ESCALATION = (MODEL_TRANSLATE_CHEAP, MODEL_BACK)`; `test_run_scene.py`: 2
  testes novos cobrindo escalação no backend `api` e não-escalação no `ollama` (31/31 em
  `test_run_scene.py`, 375 passed/7 skipped na suite `framework/runtime` inteira)
- **Investigação `mp0010_01` (trails_sky_sc)**: retighten via Ollama travou após ~2h15m
  (`Remote end closed connection without response`, sem corromper dado — checkpoint limpo); rodado
  via API Anthropic (`claude-haiku-4-5`) em chunks de 40 linhas com teto de gasto por ledger,
  276/276 linhas acima do budget (tolerância 1.15) retraduzidas por US$0,2468. Resultado real
  (`verify_chapter.py mp0010_01`, contra o `.pac` real do jogo): fitting-failure caiu de 301 para
  145 das 447 linhas da cena, round-trip OK
- **Tier opus validado com dado real** (fecha o ciclo do `MODEL_ESCALATION` acima): resíduo de 101
  linhas ainda acima do budget em tolerância 1.0 retraduzido com `claude-opus-4-8` em chunks de 20,
  US$0,8598. `verify_chapter.py` real: **145 → 65** linhas com overflow (exit 3, só fitting,
  round-trip OK) — queda de 55%, confirmando que a escalação de modelo (não só de tolerância) ajuda
  de fato, não só em teste com mock. Achado colateral: `model.over_budget_offsets()` (heurística
  interna) reportou só 9 residuais pós-opus contra os 65 reais do `verify_chapter.py` — a heurística
  de budget do `model.py` diverge do budget real do engine nessa cena; não investigado a fundo nesta
  sessão, fica como próximo passo se o resíduo de 65 for revisitado
- **`trails_sky_sc` (quarto jogo, engine novo) onboarding iniciado**: Falcom remake engine (Sora no
  Kiseki 2nd Chapter, 2026) — sem entrada no `connector_registry.json`, conector escrito do zero.
  `target_charset_supported: true` (grava UTF-8 real, motivou a ADR 0005 acima). Estado atual:
  extração + split de 67 cenas completos, `mp0010_01` (447 linhas) é a cena-piloto do escalonamento
  de fitting — ainda com resíduo de overflow (65/447, ver acima), demais cenas não traduzidas ainda

---

## 2026-06-16 — harness estável

Framework em produção com Utawarerumono (cap. 11–20+).

### Runtime (`framework/runtime/`)

**Pipeline de tradução**
- `run_scene.py` — orquestrador determinístico de 1 cena: context_pack → translate → build_plan → back-translate → verify → state_index
- `run_chapter.py` — driver de capítulo: loop resumível de cenas, stop-na-1ª-falha, `--max-usd` para teto duro de gasto
- Escalonamento cirúrgico de fitting: re-traduz só linhas above-budget (não a cena inteira) ao falhar verify por fitting
- Fases isoladas: `_pack_and_translate()` e `_fitting_loop()` extraídas de `run_scene()` para facilitar testes e leitura

**Backends de tradução**
- Backend `api`: Anthropic SDK com streaming, backoff em transient errors, retry por linha (não por cena)
- Backend `in-session`: caminho de assinatura sem chamada de rede (contexto O(cena))
- Batch API com 50% de desconto: tiering Haiku/Sonnet por complexidade de linha, chunking de 60 linhas, múltiplas rodadas para convergência de cobertura
- Back-translation em batch pós-capítulo (`_back_batch_phase`): 1 batch -50% Opus para todas as cenas verificadas

**Custo e observabilidade**
- `api_ledger.jsonl`: toda chamada cobrada registrada (inclusive retries e falhas) — fonte de verdade de gasto
- `metrics.jsonl`: resumo por cena de sucesso com custo-verdade via ledger
- `cost_report.py`: delta de gasto por capítulo (filtra só cenas `ch_<cap>_*`)
- `_warn_ledger_size()`: RuntimeWarning quando ledger passa de 100 MB
- `warnings.jsonl`: avisos de governança persistidos (não só stdout)

**Estado e memória**
- `run_state.json`: checkpoint por cena (status, verified, high, scene_id) — resumo idempotente
- `state_index.py`: TM (`translation_memory.jsonl`) + voice cards + decision index reconstruídos após cada cena
- `context_pack.py`: pacote O(cena) — subconjunto de glossário/vozes/TM relevante, não o estado inteiro

**Qualidade**
- `kb_gate.py`: gate de cobertura de KB antes de traduzir (pesquisa reconciliada obrigatória)
- Back-translation de linhas `risk>=high` com amostragem de low/medium (`BACK_SAMPLE_RATE=0.05`)
- `quality_review.py`: XLSX de revisão humana gerado obrigatoriamente ao fim de cada capítulo
- `quality_fix.py`: aplicação cirúrgica de correções da revisão humana via `retranslate_offsets()`

**Segurança**
- Path traversal guard: `_validate_scene_arg()` e `_validate_chapter_arg()` bloqueiam separadores de path
- Conector sandboxado: `_connector_script()` verifica que o script está dentro de `root.resolve()`
- Blowup guard: traduções >8× a fonte descartadas antes de gravar
- Engine labels allowlist: identificadores de rig/asset nunca vão ao LLM (`_ENGINE_LABELS` + `_ENGINE_LABEL_RX`)
- Lock cross-platform atômico no ledger (`O_CREAT|O_EXCL`)
- Timeout de 300s no conector

**Módulos leaf (sem dependências de runtime)**
- `config.py`: constantes de tier/custo/status, TypedDicts de contrato, `CONNECTOR_REGISTRY`, `RunSceneOptions`
- `paths.py`: fonte única de todos os caminhos de artefato — zero f-strings espalhadas
- `cost.py`: tabela de preços, `cost_of()`, `log_api_call()`, lock de ledger

**CI**
- GitHub Actions: Python 3.11 + 3.12, mypy (config/paths/cost), pytest (102 testes)

### SDD (`framework/skills/`)

- 9 skills (00–08) + governance: processo completo de localização baseado em cognição narrativa
- `translation_governance.md`: Carta de Governança — contrato de qualidade (voz/lore/situação/processo)
- `_index.md`: índice com fluxo, invariantes e critérios de aceitação do projeto

### Conector (`framework/connectors/`)

- Skeleton `extract.py` + `reinsert.py`: ponto de partida para novos conectores
- Contrato: exit codes 0/1/3 + linha `VERIFY_STATUS: {json}` (protocolo estruturado)
- Round-trip oracle: `reextract(reinsert(translate(extract(bin)))) == extract(bin)` byte a byte

---

## Antes de 2026-06-16 — histórico inicial

Desenvolvimento iterativo durante produção do cap. 11–20 do Utawarerumono. Marcos relevantes:

- God-module `model.py` decomposto em `config.py`, `cost.py`, `llm_client.py`, `back_translate.py`
- Escalonamento de fitting com `BUDGET_ESCALATION` (1.40 → 1.15 → 1.0)
- Dedup por TM com guards de paridade de quebra (`\n`)
- Tiering Haiku/Sonnet com guard de modelo para linhas multi-linha
- Staleness check do glossário (`GLOSSARY_STALENESS_DAYS=180`)
- `clean_failed_scene()`: move artefatos de cena falha para `discontinued/` (não apaga)
