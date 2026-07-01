# Translation Cognition Framework — guia do framework

> O processo + o motor para localizar obras narrativas longas: IA cercada na cognição, estado externalizado, gates determinísticos.
> **Validado em produção:** 16 capítulos, 146 cenas, ~45.100 linhas, R$ 0 desperdiçado.

Esta página mostra a **organização do código** e como **instanciar um projeto novo**.
Conceitos, arquitetura e o "porquê" das decisões → [README raiz](../README.md).

---

## Estrutura de pastas

| Pasta | Papel | Camadas |
|---|---|---|
| `framework/skills/` | Passos 00..08 do SDD — o processo, em prosa | Cognition + Validation |
| `framework/media-profiles/` | Preocupações por tipo de mídia (jogos/filmes/séries) | — |
| `framework/connectors/` | I/O binário ↔ corpus (extração + reinserção, round-trip) | Execution + Validation |
| `framework/runtime/` | Harness executável — cena = job stateless | State + Execution + Cognition |
| `projects/<título>/` | A instância: `project.json` + artefatos + conector | — |

> **Princípio:** as skills genéricas resolvem tudo que é específico de uma obra lendo o `project.json`.
> Nenhum nome de personagem, termo de lore ou idioma vive dentro de `framework/`.

---

## Arquivos

```
framework/
  skills/           ← 00..08 — o processo genérico (comece por skills/_index.md)
  schemas/          ← artifacts_schema.md (outputs) + project_schema.md (manifesto)
  media-profiles/   ← games.md (validado), films.md / series.md (stubs)
  connectors/       ← 00_index.md, hex_binary.md, _skeleton/ (extract.py, reinsert.py, table_schema.md)
  SDD_RUNTIME.md    ← mapa skill→runtime: qual módulo executa cada etapa do SDD (00–08) + quem produz/consome cada artefato
  runtime/          ← harness (cena = job stateless): orquestração (run_scene/run_chapter), contexto
                       (context_pack), estado (state_index), IA (model + back_translate), KB/spoiler
                       (kb_review, kb_phase, spoiler_check), qualidade (quality_review/gate/fix,
                       tm_correct), custo (cost, cost_report) — ~23 módulos. Ver runtime/README.md
  validation/       ← validate.py, naturalness_lint.py, cost_model.py (gates determinísticos)
  docs/             ← ARCHITECTURE, GOVERNANCE, STATE_MANAGEMENT, MODEL_INTERFACE, TRANSLATION_PIPELINE, OBSERVABILITY, NAMING, ROADMAP, adr/
  templates/        ← project.template.json + profile/ para novos projetos
  README.md         ← este arquivo

projects/
  utawarerumono/    ← primeira instância de referência (jogo, EN→pt-BR) — completa
    connector/      ← extract.py, reinsert.py, table_schema (adaptados ao binário)
  breath_of_fire_4/ ← segunda instância — piloto de portabilidade para engine Capcom
    connector/      ← implementado (Fase 0 concluída, round-trip green)
```

---

## COMO INSTANCIAR UM PROJETO NOVO

### 1. Criar a pasta do projeto
```
projects/<seu-título>/
  artifacts/      ← onde os outputs do pipeline vão viver (e o binário-fonte, para jogos)
  connector/      ← scripts do conector (para jogos antigos)
  profile/        ← dados curados de referência (opcional, mas recomendado)
```

### 2. Preencher o manifesto
Copiar `framework/templates/project.template.json` para `projects/<seu-título>/project.json` e
preencher. Campos essenciais (schema completo em `framework/schemas/project_schema.md`):

- `title`, `media_type`, `media_profile`
- `source_language`, `target_language` (códigos BCP-47 — ex: `en`, `ja`, `pt-BR`)
- `source` — caminho e formato do corpus + colunas de ID/texto
- `connector` — para jogos: tipo, binário-fonte, tabela, scripts, estratégia de espaço, formato de patch
- `formatting_tokens` — tokens de engine a preservar (para jogos)
- `system_line_convention`, `length_constraints`, `batch_size`

### 3. Fornecer o binário e escrever o conector (jogos antigos)
O usuário coloca o binário em `artifacts/` e declara o `connector` no manifesto. A IA escreve
`connector/extract.py` e `reinsert.py` a partir de `framework/connectors/_skeleton/`, guiada por
`framework/connectors/hex_binary.md`. **O Passo 00 só avança se o round-trip passar** (extrair →
reinserir sem mudanças === binário original).

### 4. (Opcional) Curar o perfil
Copiar os templates de `framework/templates/profile/` e preencher com o que já se sabe da obra.
No pipeline real, o conteúdo equivalente é **gerado** pelos passos 1–4; o perfil curado serve de
semente e referência.

### 5. Rodar o pipeline
Executar as skills em ordem (`framework/skills/_index.md` tem o fluxo `00..08`). Cada skill:
- Lê `project.json` + os artefatos do passo anterior
- Tem um **Input Gate** que bloqueia execução fora de ordem
- Produz artefatos em `projects/<seu-título>/artifacts/`

A entrega final (Passo 08) é o **binário traduzido + um patch** (ips/bps/xdelta).

---

## O QUE É GENÉRICO vs. O QUE O PROJETO FORNECE

| Genérico (framework) | Específico (projeto) |
|----------------------|----------------------|
| Os passos 00..08 e seus gates | Título, idiomas, tipo de mídia |
| Schemas de artefatos | Corpus-fonte e seu formato |
| Regra de geração de suites de teste | Tokens de engine deste jogo |
| Categorias de `handling_rule` | Quais termos caem em cada categoria |
| Verificação de voz por `voice_criticality` | Os perfis de voz reais (gerados/curados) |
| Verificação de identidade dupla | Os pares de identidade reais |
| Verificação de tom por fase | As fases narrativas reais |

---

## MÍDIA SUPORTADA

- **Jogos** — ✅ validado em dois engines distintos:
  - *Utawarerumono* (Aquaplus): **CONCLUÍDO** — 16 capítulos, 146 cenas, ~45.100 linhas, pt-BR in-game.
  - *Breath of Fire IV* (Capcom DAT): **CONCLUÍDO** — 125 cenas, pipeline completo 00–08, QA + output gerados.
  - Ver `media-profiles/games.md`.
- **Filmes** — 🚧 ponto de extensão. Ver `media-profiles/films.md`.
- **Séries** — 🚧 ponto de extensão. Ver `media-profiles/series.md`.

---

## RUNTIME (harness de escala)

Além das skills (o *processo*), `framework/runtime/` é o *harness* que torna a execução sustentável:
cada cena é um **job stateless e limitado** (contexto O(cena), não O(histórico)), o que elimina o
estouro de sessão e viabiliza Sonnet a custo previsível. A LLM faz só cognição (traduzir / verificar
alto risco); orquestração, estado, contexto e validação são determinísticos. Ver
[`runtime/README.md`](runtime/README.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), a governança
com desenhos em [`docs/GOVERNANCE.md`](docs/GOVERNANCE.md) e a convenção de nomes em
[`docs/NAMING.md`](docs/NAMING.md).

---

## INSTÂNCIAS

**`projects/utawarerumono/`** — primeira instância de referência. Visual novel, EN→pt-BR, com múltiplos
pares de identidade dupla e gestão crítica de spoilers. **CONCLUÍDO:** 16 capítulos, 146 cenas,
~45.100 linhas, round-trip byte-idêntico, custo ~R$ 338,46, pt-BR in-game. Use como
exemplo de manifesto, perfil e artefatos do pipeline.

**`projects/breath_of_fire_4/`** — segunda instância. Valida a portabilidade para engine Capcom. **CONCLUÍDO:**
125 cenas, pipeline 00–08 completo, QA humana + output (125 DAT files) gerados, custo ~$11 USD.
Débitos técnicos em aberto: glossary coluna, NPC voice cards, TM semântica (B2), release.

---

## STATUS DO FRAMEWORK — junho 2026

### Objetivos alcançados

- Harness stateless (cena = job isolado, contexto O(cena)): sem estouro de sessão ✅
- Batch API (−50%) + tiering Haiku/Sonnet/Opus: validado em escala ✅
- Gates de cognição: KB-gate, controle de spoiler, controle de gênero ✅
- Revisão humana via XLSX → verbatim (R$ 0) ou nota cirúrgica ✅
- Ledger auditável: toda chamada cobrada registrada, inclusive falhas ✅
- Generic Connector System: dois engines (Aquaplus + Capcom) com round-trip byte-idêntico ✅
- 145 testes passando (116 runtime + 29 validação)

### Dívidas técnicas do framework

| Dívida | Prioridade |
|---|---|
| `run_game` — driver ponta-a-ponta (todos os capítulos + Fase 0 gating automático) | P2.5 — agora |
| Observabilidade de progresso (linhas/min, % do jogo, ETA) | P2.5 — agora |
| `state_index` rebuild 1×/capítulo no batch (hoje por cena, redundante) | P2.5 — agora |
| TM busca semântica (B2: `sentence-transformers` local) | pós-produção |
| Evolução do conector: registry de detecção + síntese governada | P4 (pós-produção) |
| Filmes / séries: pontos de extensão sem validação em produção | futuro |

### Próximos passos

1. `run_game` + observabilidade (P2.5 — barato, não requer novo modelo)
2. TM semântica (B2) — implementação
3. Piloto multi-game: questões abertas respondidas progressivamente (BoF4 como referência)
