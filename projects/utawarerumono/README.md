# Projeto: Utawarerumono: Mask of Deception
## Primeira instância de referência do framework SDD

Este é o projeto de localização que originou o framework. Serve como **referência viva**: prova de que o processo genérico em `/framework/` funciona em um título real, e exemplo de como preencher uma instância nova.

---

## Configuração

Toda a config deste título vive em [`project.json`](project.json):

- **Mídia:** jogo (visual novel) — usa o perfil `games`
- **Idiomas:** EN → pt-BR
- **Fonte:** `artifacts/dialogs.csv` (formato CSV com offset hex)
- **Tokens de engine:** `{W75}`, `{W80}`, `{W10}`, `{COLOR}`, `{END}`
- **Convenção de sistema:** linhas em CAPS = texto de sistema
- **Lote:** 200 linhas

---

## Dados curados (`profile/`)

| Arquivo | Conteúdo | Equivalente no pipeline |
|---------|----------|-------------------------|
| [`voice_profiles_reference.md`](profile/voice_profiles_reference.md) | Perfis de voz dos personagens + `voice_criticality` | `tone_analysis.md` (Passo 1) |
| [`identity_pairs_reference.md`](profile/identity_pairs_reference.md) | Pares de identidade dupla + regras de separação | `aliases_map.json` / `entities.csv` (Passos 1–2) |
| [`terminology_seeds.md`](profile/terminology_seeds.md) | Decisões terminológicas + formas exatas + fases narrativas | `glossary.csv` (Passo 4) |
| [`example_test_suites.md`](profile/example_test_suites.md) | Suites de teste sintético concretas | `synthetic_test_corpus.json` (Passo 5b) |

> Estes arquivos são **referência/exemplo**. No pipeline real, o conteúdo equivalente
> é produzido como artefato gerado. Eles registram o conhecimento deste título e
> servem de modelo de preenchimento para projetos novos.

---

## Artefatos gerados (`artifacts/`)

Onde os outputs do pipeline vivem: `dialogs.csv` (output do Passo 00, depois imutável), `entities.csv`,
`glossary.csv`, `translated.csv`, `research_log.md`, `translation_status.json`,
`micro_qa_log.json`, `qa_report.md`, o binário traduzido + patch (Passo 08), etc.
Ver `framework/schemas/artifacts_schema.md`.

---

## Conector (`connector/`)

Jogo antigo: o texto vive num binário e é extraído/reinserido por código determinístico
(conector `hex_binary`). Ver [`connector/README.md`](connector/README.md) para o estado atual —
**aguardando o binário** para escrever `extract.py`/`reinsert.py` e mapear a tabela. O bloco
`connector` do `project.json` declara a config; a entrega final é um patch IPS.

---

## Como rodar

O processo é definido em [`/framework/skills/`](../../framework/skills/_index.md).
Executar as skills na ordem do pipeline (00 → 08), cada uma lendo `project.json` +
os artefatos do passo anterior. Os Input Gates de cada skill bloqueiam execução fora de ordem.
O Passo 00 (extração) só avança se o gate de round-trip passar.

---

## Características críticas deste título

- **Múltiplos pares de identidade dupla** com spoilers críticos (Ukon/Oshtor, Sakon/Mikazuchi, Mito/Mikado)
- **Gestão de spoiler** rigorosa: nomes revelados nunca aparecem antes do `reveal_timing`
- **Comédia com timing** sensível (Haku, Nosuri)
- **Corpus extenso** (~33.000 linhas estimadas)
