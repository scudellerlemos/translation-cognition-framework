# ADR 0010 — Gate de schema (`risk_level`) via `validate.py`, obrigatório por capítulo

**Status:** aceito · **Data:** 2026-08-30

## Contexto

`validate.py` já validava `translation_plan.json` (esquema legado, POC antigo), mas não o esquema
real de produção — `translation_plan_<scene_id>.json` por cena (`artifacts/scenes/ch_*/`,
ver `paths.py`). Um `risk_level` inválido ou ausente, ou um `risk_notes` faltando numa linha
`medium`/`high`/`critical`, só era pego se alguém rodasse `validate.py` manualmente — nenhum gate
automático do pipeline conferia isso. A checagem de `risk_level`/`risk_notes` já existia duplicada
inline no bloco de `translation_plan.json`.

## Decisão

- `validate.py`: checagem de risco extraída para `_check_risk(label, lines)` (dedup) e estendida a um
  novo bloco que varre `artifacts/scenes/*/translation_plan_<scene_id>.json` (todas as cenas do
  projeto, esquema real), validando campos obrigatórios universais (`offset`, `text_source`,
  `speaker`, `risk_level`, `base_translation` — só o subconjunto comum a todos os conectores;
  `tone_register`/`intent`/`glossary_flags`/`entities_present` variam por conector e ficam de fora).
- Os 5 `build_plan_chapter.py` (`_skeleton`, `breath_of_fire_4`, `souldiers`, `trails_sky_sc`,
  `utawarerumono`) passam a validar `risk_level` contra o enum (`_RISK` frozenset) na hora de montar
  o plano, com fallback pra `"low"` + erro reportado (em vez de aceitar qualquer string do LLM sem
  checar).
- `run_chapter.py` ganha `_audit_schema(root)`, chamado sempre ao fim do capítulo (mesmo padrão
  report-only de `_audit_spoiler`/`_audit_quality` — nunca bloqueia, só avisa alto e claro).
- `GOVERNANCE.md`: nova linha "Schema" na tabela da pilha de gates (§3).

## Consequências

- (+) `risk_level` inválido/ausente ou `risk_notes` faltando em linha de risco ≥ medium agora aparece
  sempre ao fim do capítulo, sem depender de alguém lembrar de rodar `validate.py` à mão.
- (+) Dedup de `_check_risk` remove a duplicação que já existia entre o bloco legado e o novo bloco
  por-cena.
- (+) Mesma filosofia dos demais gates (§3 de `GOVERNANCE.md`): audita o projeto inteiro, não só o
  capítulo corrente — pega histórico também.
- (−) Mais uma auditoria obrigatória rodando a cada capítulo (custo de tempo, não de API — é
  determinístico/local); mitigado por ser report-only e best-effort (`try/except` em
  `_audit_schema`, não derruba o capítulo se `validate.py` falhar).
- Fora de escopo (dívida conhecida): nenhum teste novo cobre `_audit_schema` diretamente nem o novo
  bloco de `validate.py` sobre `translation_plan_<scene_id>.json` — candidato a próxima sessão.
