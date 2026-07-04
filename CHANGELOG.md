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
