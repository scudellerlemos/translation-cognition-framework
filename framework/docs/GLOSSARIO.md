# Glossário — nomes dos itens de planejamento

> **Política:** os itens de risco/hardening/gap são identificados por **nome descritivo**, tanto no
> código quanto nos documentos. Não usamos mais códigos crípticos (`H2`, `R5`, `GAP D`…) — eles foram
> aposentados por serem mal desenhados (o mesmo `R3`, por exemplo, significava coisas diferentes em
> tabelas diferentes).
>
> Esta página existe por dois motivos: (1) listar os nomes canônicos em um lugar; (2) servir de
> **de-para** para quem encontrar um código antigo em **commits, PRs ou históricos** anteriores a
> 2026-06.

## Hardening — endurecimentos de arquitetura
Documentados em `framework/docs/ROADMAP.md` (seção P4). Código antigo → nome atual:

| Antigo | Nome atual | Conceito |
|---|---|---|
| H1 | **Saída estruturada do conector** | exit code + linha `VERIFY_STATUS:{json}`; o orquestrador não faz grep de prosa (`run_scene.py`, `verify_chapter.py`) |
| H2 | **Fonte única de paths** | contrato de caminhos de artefato consolidado em `paths.py` |
| H3 | **run_scene coeso** | `run_scene` não deve acretar responsabilidade sem limite (adiado) |
| H4 | **Repro: gate ≠ geração** | os *gates* reproduzem; a *geração* (saída do LLM) não (`ARCHITECTURE.md`) |
| H5 | **Profundidade da Fase 0** | até onde cabear a reconciliação de KB (adiado; `kb_review.py` é o digest leve) |
| H6 | **Spoiler observável** | verificação observável de não-vazamento pós-tradução (`spoiler_check.py`) |

## Riscos de cognição (levar o pipeline a produção)
Documentados em `framework/docs/ROADMAP.md` (seção P1.5).

| Antigo | Nome atual | Conceito |
|---|---|---|
| R1 | **API comprovada** | ligar e comprovar o caminho de API (`.env` + benchmark) |
| R2 | **API como default** | `api` como backend default de produção |
| R3 | **Fase 0 / cobertura de KB** | KB reconciliada + gate de cobertura (`kb_gate.py`) |
| R4 | **Controle de spoiler** | `spoiler_ledger.json` + filtro temporal + regra de gênero |
| R5 | **Bundle de custo** | Batch API −50% + model tiering + back-batch + guardrails de orçamento |
| R-CUSTO | **Re-tradução cara** | re-tradução era 58% do gasto (rótulo de engine traduzido → estouro de budget → retighten); resolvido por `model._label_passthrough` |

## Riscos de engenharia (mitigações offline)
Documentados em `framework/docs/ROADMAP.md` (seção P4).

| Antigo | Nome atual | Conceito |
|---|---|---|
| R#1 | **Mock↔API diverge** | bugs de batch passaram no fake e queimaram dinheiro → smoke vivo de contrato (`batch_smoke.py`) |
| R#2 | **Piso de qualidade** | verdict `revise` report-only + tier Haiku sem crivo → gate + amostragem + correção dirigida |
| R#3 | **TM append-only** | termo errado propagado sem ferramenta de correção (`tm_correct.py`) |
| R#2g | **Vazamento de gênero** | ele/ela onde o EN é neutro (`spoiler_check.check_gender`) |
| R#4 | **IA reconcilia a própria KB** | sem segundo par de olhos no delta → gate de fonte + ratificação humana |
| R#4g | **Gênero pt-BR inativo** | mecanismo pronto, marcação aguarda caso confirmado por fonte |

## GAPs do processo (Fase 0 → pessoa jogando)
Documentados no `QA_REVIEW.md`.

| Antigo | Nome atual | Quem cobre |
|---|---|---|
| GAP A | **Revisão literária** | papel humano REVISOR |
| GAP B | **Teste in-game** | papel humano TESTER |
| GAP C | **Zona cinza do balão** | TESTER confirma na tela (cresceu vs EN mas não estourou) |
| GAP D | **Consistência de glossário** | `glossary_lint.py` (determinístico) |

## Generic Connector System / Evolução do Motor (retirados 2026-07-03)
Documentados em `framework/docs/ROADMAP.md` (seção Fase D / Evolução do Motor).

| Antigo | Nome atual | Conceito |
|---|---|---|
| D1 | **Descoberta automática de engine** | `evidence_collector.py` + `tier_classifier.py` + `connector_registry.json` |
| D2 | **Validação de cobertura/consistência do candidato** | `coverage_gate.py` + `adversarial_validator.py` |
| D3 | **Manifesto e fingerprint de conector** | `fingerprint_monitor.py` |
| D4 | **TM por série** | `tm_lookup.py` + `tm_updater.py` |
| D5 | **Gates de autonomia** | `tier_classifier.existence_gate()` + `connector_gate.assert_fresh_read()` |
| D6 | **Gate de completude de conector** | `connector_gate.py` |
| B1 | **Validação leve** | `framework/validation/validate.py` |
| B2 | **Memória semântica** | `framework/db/embedder.py` + `store.py` (sqlite-vec) |
| B3 | **Fachada de orquestração** | `kernel.py` |
| B4 | **Skill DSL** | `framework/skills/skill_base.py` + `registry.py` |
| P1.7 | **Onboarding de baixo custo** | `scaffold_project.py`, `kb_fetch.py`/`kb_build_ollama.py`/`kb_reconcile.py` |
| P2.5 | **Driver ponta-a-ponta** | `run_game.py` + `progress_report.py` |

Os dois sistemas de **tier numerado** também foram retirados do código nesta data: o tier de
descoberta de engine (`T1`/`T2`/`T3`) virou `known_engine`/`unknown_engine`/`blocked`; a cascata de
encaixe de bytes na reinserção (`T1`–`T4`) virou nomes descritivos por conector — `direct`/
`repoint`/`trimmed`/`residue` no template (`framework/connectors/_skeleton/reinsert.py`), `in_place`/
`residuo` no Utawarerumono, `unchanged`/`shrunk`/`expanded`/`individual_overflow` no Breath of Fire IV.

## Abreviações de domínio aceitas
Estas **podem** aparecer em código — são jargão de domínio estabelecido, documentado em
[`NAMING.md`](NAMING.md) §3 (`KB`, `TM`, `QA`, `BIN`/`SDAT`, `scene_id`). `T4` foi retirado desta
lista (ver seção acima) — deixou de ser aceito como nome de domínio.
