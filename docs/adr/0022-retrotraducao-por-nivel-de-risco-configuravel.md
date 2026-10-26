# ADR 0022 — Níveis de risco que exigem retrotradução passam a ser configuráveis por projeto

**Status:** aceito · **Data:** 2026-10-20 · **Decisão do usuário** ("só critical", Prelude)

## Contexto

A retrotradução (Opus, passo 5c) era exigida para toda fala `high` ou `critical`, fixa no código
(`back_translate.high_risk_lines`, `quality_gate.check`). No Prelude, com o plano Pro, o Opus é a parte mais cara
do que sobra da onda; as `high` já são retraduzidas pelo Sonnet (passo 5d) e a amostra humana de 40 falas
(38 ok) não mostrou erro de sentido nelas.

## Decisão

1. Chave opcional `back_translation_risk` no `project.json`: lista de níveis (`low|medium|high|critical`) que
   exigem retrotradução. Sem a chave, ou com valor inválido, vale o padrão `["high","critical"]`: nada muda para
   os outros projetos.
2. Fonte única: `artifact_io.back_risk_levels(root)`, lida por `back_translate.high_risk_lines`,
   `sample_low_risk_lines` e `quality_gate.check` (cobertura `SEM COBERTURA` e veredito `revise` só valem para
   esses níveis).
3. Prelude: `["critical"]`. O Sonnet do passo 5d para `high`/`critical` continua.

## Salvaguarda

Não é bypass: o gate segue bloqueando `critical` sem retrotradução. Risco: erro de sentido em fala `high` passa
sem o juiz forte; mitigação: Sonnet no 5d, amostra humana a cada lote e conferência no jogo entre os lotes de
4 a 6 ondas. Falas `high` já retrotraduzidas e gravadas continuam no disco e seguem valendo.

## Reverter

Remover `back_translation_risk` do `project.json`. Cenas fechadas depois da mudança terão `high` sem
retrotradução e o gate passa a cobrar delas.

## Testes

`test_back_translate.py`: `test_back_risk_default_cobre_high_e_critical`,
`test_back_risk_do_project_json_restringe_a_critical`, `test_back_risk_valor_invalido_volta_ao_padrao`,
`test_quality_gate_so_exige_cobertura_dos_niveis_configurados`.
