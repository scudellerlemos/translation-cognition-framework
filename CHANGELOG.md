# Changelog

Todas as mudanças significativas do framework são documentadas aqui.
Formato: [Semântico](https://semver.org/) — `[versão] — data`.

---

## [Não versionado] — pós-1.0.0

Trabalho incremental sobre a 1.0.0 (sem novo marco de release): cobertura de testes, reestruturação
da CI, onboarding de baixo custo, Generic Connector System completo e terceiro jogo concluído.

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
  quebra `print()` com acento/seta com `UnicodeEncodeError` — issue #119, reproduzido de novo
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

---

## [1.0.0] — 2026-06-16

Primeira versão estável do harness. Framework em produção com Utawarerumono (cap. 11–20+).

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

## [Não versionado] — pré-1.0.0

Desenvolvimento iterativo durante produção do cap. 11–20 do Utawarerumono. Marcos relevantes:

- God-module `model.py` decomposto em `config.py`, `cost.py`, `llm_client.py`, `back_translate.py`
- Escalonamento de fitting com `BUDGET_ESCALATION` (1.40 → 1.15 → 1.0)
- Dedup por TM com guards de paridade de quebra (`\n`)
- Tiering Haiku/Sonnet com guard de modelo para linhas multi-linha
- Staleness check do glossário (`GLOSSARY_STALENESS_DAYS=180`)
- `clean_failed_scene()`: move artefatos de cena falha para `discontinued/` (não apaga)
