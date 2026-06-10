# Arquitetura — Translation-Cognition Framework

Framework spec-driven (SDD) para localização baseada em cognição narrativa. Separa **entender →
estruturar → reger → planejar → executar → validar** para preservar identidade, tom e consistência
em obras longas (jogos, filmes, séries). Este documento descreve a arquitetura **alvo** e o estado atual.

## Princípio central

> A LLM faz **só** o que exige IA: **traduzir** e **verificar alto risco**. Todo o resto — estado,
> memória, governança, checkpoints, métricas, controle de fluxo, montagem de contexto — é
> **determinístico e externo** à janela do modelo.

A regra existe por uma razão medida: o que estourava a sessão **não** era a tradução nem a governança,
e sim o **modo de execução** — a tradução cognitiva sendo feita inline, turno-a-turno, numa sessão de
vida-longa que acumulava todo o histórico (ver `adr/0002-stateless-scene-jobs.md`).

## As 3 camadas (genéricas) + a instância

```
framework/skills/          ← O PROCESSO (como). Genérico. Nunca contém dados de obra.
framework/media-profiles/  ← A CATEGORIA (jogos/filmes/séries). Formato, tokens, timing.
framework/connectors/      ← A I/O (código det.). Extração/reinserção meio↔corpus.
framework/runtime/         ← O HARNESS (orquestração det. + interface de modelo).  [NOVO]
framework/validation/      ← OS GATES (código det.). Schemas, naturalidade, custo.
framework/docs/            ← ARQUITETURA + ADRs + ROADMAP.                          [NOVO]
        +
projects/<título>/         ← A INSTÂNCIA (o quê). Manifesto + perfil + artefatos + conector do título.
```

## O alvo: "uma cena = um job stateless e limitado"

Cada cena é um **job resumível** cujo contexto é **O(cena)**, não O(histórico). O orquestrador
determinístico (`framework/runtime/run_scene.py`) encadeia:

```
run_scene(cena)
  1. context_pack  → pacote LIMITADO (doutrina cacheável + glossário-subset + voice cards dos
                     falantes + decisões relevantes + hits de TM + linhas+budgets) → scene_prompt.md
  2. translate ............................► [IA: Sonnet]   (única parte não-determinística)
  3. build_plan_chapter (valida cobertura/tokens/risk_notes) → approved_<sfx>.csv
  4. high? back_translate .................► [IA: Opus]     (verificação de alto risco)
  5. verify_chapter (round-trip byte-idêntico + ponteiros within-file)
  6. checkpoint (run_state.json) + state_index (TM cresce)
```

**Estado externo consultável** (não na janela): `glossary.csv`, `state/translation_memory.jsonl`,
`state/voice_cards.json`, `state/decision_index.json`, `translation_status.json`, `run_state.json`.

## Determinismo vs IA (mapa)

| Responsabilidade | Veredito | Onde |
|---|---|---|
| Parser / extração / reinserção | Determinístico | `connector/` |
| Orquestração / controle de fluxo | Determinístico | `runtime/run_scene.py` |
| Montagem de contexto | Determinístico | `runtime/context_pack.py` |
| Memória / consistência (TM, vozes, decisões) | Determinístico | `runtime/state_index.py` |
| Checkpoints | Determinístico | `run_state.json` |
| Validação (schemas/tokens/naturalidade/custo) | Determinístico | `validation/` |
| **Tradução** | **IA** | `runtime/model.py` |
| **Back-translation (alto risco)** | **IA** | `runtime/model.py` |

A única fronteira não-determinística é `model.py` — por isso ela é fina e isolada. Ver
`MODEL_INTERFACE.md`.

## Por que isto escala e roda em Sonnet

- **Contexto constante por execução** → a janela não cresce com o nº de capítulos (mata o estouro).
- **Doutrina cacheável (~4K tok)** cobrada ~1× via prompt-caching, não a cada cena.
- **Consistência vem do store** (TM/glossário/voice cards), não da memória do chat.
- **Model-mix**: Sonnet traduz, Opus só verifica alto risco (ver `validation/cost_model.py`).

Resultado: Sonnet passa a ser o default de tradução com contexto pequeno e curado. Ver
`adr/0004-model-agnostic-interface.md` e a seção *Sonnet Readiness* do `ROADMAP.md`.

## Documentos relacionados

- `STATE_MANAGEMENT.md` — conhecimento permanente vs temporário; substrato de estado.
- `MODEL_INTERFACE.md` — contrato `translate`/`back_translate`; caminhos assinatura vs API.
- `TRANSLATION_PIPELINE.md` — o fluxo de 1 cena ponta-a-ponta; checkpoint/resume.
- `OBSERVABILITY.md` — métricas a coletar.
- `ROADMAP.md` — backlog priorizado (P0–P3) + fases.
- `adr/` — decisões arquiteturais registradas.
