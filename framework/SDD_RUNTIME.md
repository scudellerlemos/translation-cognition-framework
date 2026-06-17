# SDD ↔ Runtime — Como as Skills se Conectam ao Pipeline

Este documento mapeia cada skill do processo SDD (`framework/skills/`) aos módulos do harness
(`framework/runtime/`) e aos artefatos que fluem entre eles.

---

## Visão geral: dois sistemas, um processo

```
framework/skills/        ← O QUE fazer e POR QUÊ (processo, regras, qualidade)
framework/runtime/       ← COMO executar em escala (automação, IA, determinismo)
```

As skills definem o processo cognitivo (o tradutor raciocina via skills).
O runtime automatiza a execução em escala (o harness orquestra sem o chat).
**Ambos são obrigatórios**: as skills sem o runtime são manuais; o runtime sem as skills não tem processo.

---

## Mapa skill → runtime

### Skill 00 — Extração (`00_extraction.md`)

**Responsável**: conector do projeto (`<projeto>/connector/extract.py`)
**Runtime envolvido**: nenhum (etapa pré-pipeline, 100% determinística)

```
connector/extract.py  →  artifacts/<scene>/dialogs.csv
                          artifacts/extraction_log.md
```

- O `dialogs.csv` é a **entrada** do pipeline do runtime.
- O `byte_budget` por linha calculado aqui é consumido pelo `context_pack` e pelo `build_plan`.
- O round-trip oracle (`reextract == extract`) é validado aqui, antes de qualquer tradução.

---

### Skills 01–04 — Descoberta, Entidades, KB, Glossário

**Responsável**: humano + IA via chat (skills interativas)
**Runtime envolvido**: `state_index.py`, `kb_gate.py`

```
tone_analysis.md     →  state_index.build_voice_cards()  →  artifacts/state/voice_cards.json
decision_log.md      →  state_index.build_decision_index() →  artifacts/state/decision_index.json
glossary.csv         →  context_pack.write_pack()  →  parte do scene_prompt.md
research_log.md      →  kb_gate.check()  →  gate obrigatório antes da tradução
kb_ratified.csv      →  kb_gate.check()  →  valida cobertura por entidade da cena
```

**Gate crítico**: `kb_gate.check()` é executado por `run_scene()` antes de qualquer chamada de IA.
Se o KB não cobrir as entidades da cena com `status: reconciled`, a cena é **bloqueada**.
Override via `--skip-kb-gate` (não recomendado; rompe a doutrina de pesquisa reconciliada).

---

### Skill 05 — Planejamento de Tradução (`05_translation_planning.md`)

**Responsável**: `context_pack.py` + `model.py`
**Runtime envolvido**: `context_pack.write_pack()`, `model.translate()`

```
dialogs.csv + glossary.csv + voice_cards + decision_index + TM
    ↓  context_pack.write_pack()
artifacts/<scene>/pack.json         ← pacote O(cena): só o contexto relevante
artifacts/<scene>/scene_prompt.md   ← prompt auto-contido e limitado
    ↓  model.translate()
artifacts/<scene>/translations_<id>.json  ← tradução com risk_level, risk_notes, intent por linha
```

O **context_pack** implementa o princípio de memória O(cena): em vez de carregar o histórico inteiro
na janela do LLM, carrega só o subconjunto relevante (glossário filtrado por entidades da cena,
voice cards dos falantes presentes, decisões com tags que casam). Isso garante contexto sem
acúmulo de sessão.

---

### Skill 06 — Tradução (`06_translation.md`)

**Responsável**: `model.py` → `_api_translate()` / `batch_translate()`
**Runtime envolvido**: `run_scene._pack_and_translate()`, `run_chapter._batch_phase()`

```
translations_<id>.json
    ↓  connector/build_plan_chapter.py  (via run_scene._fitting_loop)
artifacts/<scene>/translation_plan_<id>.json   ← plano linha a linha com byte_budget
artifacts/<scene>/approved_<id>.csv            ← projeção (offset, text_target) p/ o conector
```

**Escalonamento de fitting**: se `verify_chapter.py` falhar por estouro de byte (exit 3),
`run_scene._fitting_loop()` re-traduz **só as linhas acima do budget** com tolerância mais apertada
(`BUDGET_ESCALATION: 1.40 → 1.15 → 1.0`), sem re-traduzir a cena inteira.

**Backends disponíveis**:
- `api` (escala headless): Anthropic SDK com tiering Haiku/Sonnet, batch -50%
- `in-session` (assinatura): sem chamada de rede, prompt auto-contido, 1 cena por sessão limpa

---

### Skill 06b — Micro-QA / 06c — Ciclo de Correção

**Responsável**: `back_translate.py`, `quality_fix.py`
**Runtime envolvido**: `run_scene._back_phase()` (back-translation), `quality_fix.apply()`

```
translation_plan_<id>.json  [linhas risk>=high]
    ↓  model.back_translate()
artifacts/<scene>/back_translation_<id>.json   ← EN→pt-BR→EN com verdict pass/fail
```

A back-translation é **report-only** por padrão: sinaliza mas não bloqueia (exceto `--require-back`).
O `quality_fix.py` permite aplicar correções da revisão humana cirurgicamente via
`model.retranslate_offsets()` — só as linhas marcadas, com feedback da back-translation no prompt.

---

### Skill 07 — QA Final (`07_qa.md`)

**Responsável**: `quality_review.py`, `run_chapter._export_qa()`
**Runtime envolvido**: gerado **obrigatoriamente** ao fim de cada capítulo

```
translation_plan_<id>.json  [todas as linhas do capítulo]
    ↓  quality_review.export()
artifacts/qa_revisao/para_revisar/review_cap_<N>.xlsx   ← XLSX para o revisor humano
    ↓  revisor humano preenche e devolve
artifacts/qa_revisao/devolvido/review_cap_<N>.xlsx
    ↓  quality_review.apply()
retranslate_offsets() das linhas com Correção/Nota preenchida
```

O **XLSX é gerado sempre** — mesmo que a IA não tenha marcado nada. O piso de qualidade é o
humano ler, não o modelo decidir. O ciclo completo é: joga o jogo → preenche `relato_tester.csv`
→ aplica via `quality_review.py apply`.

---

### Skill 08 — Reinserção (`08_reinsertion.md`)

**Responsável**: conector do projeto (`<projeto>/connector/verify_chapter.py` + scripts de reinserção)
**Runtime envolvido**: `run_scene._fitting_loop()` (via verify), `state_index.build()`

```
approved_<id>.csv
    ↓  connector/verify_chapter.py  (round-trip byte-a-byte)
exit 0 → verified = True  →  state_index.build()  →  TM cresce com esta cena
exit 1 → verify_failed     →  pipeline para, reporta
exit 3 → fitting_failure   →  _fitting_loop() escala tolerância e re-traduz
```

O **round-trip oracle** é a garantia final: `reextract(reinsert(approved)) == extract(original)`.
Se passar, a cena entra na TM e influencia todas as cenas futuras (dedup e consistência).

---

## Fluxo completo de dados

```
[Skills 00–04: humano + IA]
dialogs.csv + glossary.csv + tone_analysis.md + decision_log.md + research_log.md + kb_ratified.csv
                                    ↓
                          [run_scene() ou run_chapter()]
                                    ↓
                    state_index.build()  →  voice_cards + decision_index + TM
                                    ↓
                    kb_gate.check()  →  bloqueia se KB incompleto
                                    ↓
                    context_pack.write_pack()  →  pack.json + scene_prompt.md
                                    ↓
                    model.translate()  →  translations_<id>.json
                                    ↓
                    build_plan_chapter.py  →  translation_plan + approved.csv
                                    ↓
                    verify_chapter.py  →  round-trip (exit 0/1/3)
                                    ↓ (exit 0)
                    back_translate()  →  back_translation_<id>.json
                                    ↓
                    state_index.build()  →  TM atualizada com esta cena
                                    ↓
                    quality_review.export()  →  XLSX para revisão humana
```

---

## Artefatos: quem produz, quem consome

| Artefato | Produzido por | Consumido por |
|---|---|---|
| `dialogs.csv` | skill 00 / `extract.py` | `context_pack`, `build_plan`, `verify` |
| `glossary.csv` | skill 04 (humano) | `context_pack`, `state_index` |
| `tone_analysis.md` | skill 01 (IA) | `state_index.build_voice_cards()` |
| `decision_log.md` | skill 04b (acumulativo) | `state_index.build_decision_index()` |
| `research_log.md` | skill 03 (IA+humano) | `kb_gate.check()` |
| `kb_ratified.csv` | skill 03 (humano ratifica) | `kb_gate.check()` |
| `pack.json` | `context_pack.write_pack()` | `model.translate()` |
| `translations_<id>.json` | `model.translate()` | `build_plan_chapter.py` |
| `translation_plan_<id>.json` | `build_plan_chapter.py` | `verify`, `back_translate`, `quality_review` |
| `approved_<id>.csv` | `build_plan_chapter.py` | `verify_chapter.py` (conector) |
| `back_translation_<id>.json` | `model.back_translate()` | `quality_fix`, revisão humana |
| `translation_memory.jsonl` | `state_index.build()` | `context_pack` (dedup por TM) |
| `voice_cards.json` | `state_index.build()` | `context_pack` |
| `decision_index.json` | `state_index.build()` | `context_pack` |
| `run_state.json` | `run_scene._checkpoint()` | `run_chapter` (skip se verified) |
| `api_ledger.jsonl` | `cost.log_api_call()` | `cost_report`, `_ledger_scene_cost()` |
| `review_cap_<N>.xlsx` | `quality_review.export()` | revisor humano → `quality_review.apply()` |
