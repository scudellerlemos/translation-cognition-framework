# Translation Cognition Framework
## Framework SDD para tradução baseada em cognição narrativa

Framework spec-driven para localização de obras narrativas complexas (jogos, filmes, séries).
Separa **entendimento, estrutura, regras, planejamento, execução e validação** para preservar
identidade, tom e consistência ao longo de corpora grandes.

---

## O MODELO DE 3 CAMADAS

```
┌─────────────────────────────────────────────────────────────┐
│  framework/skills/         O PROCESSO (como)                  │
│  Genérico. Os passos 00..08 do SDD. Nunca contém dados de obra│
├─────────────────────────────────────────────────────────────┤
│  framework/media-profiles/ A CATEGORIA (jogos/filmes/séries)  │
│  Formato de fonte, tokens, timing, restrições de comprimento. │
├─────────────────────────────────────────────────────────────┤
│  framework/connectors/     A I/O (código determinístico)      │
│  Extração (meio→corpus) e reinserção (corpus→meio).           │
├─────────────────────────────────────────────────────────────┤
│  framework/runtime/        O HARNESS (orquestração det.)      │
│  Cena = job stateless e limitado; interface de modelo.        │
├─────────────────────────────────────────────────────────────┤
│  projects/<título>/        A INSTÂNCIA (o quê)                │
│  project.json + profile/ + artifacts/ + connector/. Os dados. │
└─────────────────────────────────────────────────────────────┘
```

**Princípio central:** as skills genéricas resolvem tudo que é específico de uma obra lendo o
`project.json` e os artefatos gerados. Nenhum nome de personagem, termo de lore, token de engine
ou idioma vive dentro de `framework/`.

**Conector (camada de I/O):** para jogos antigos, o texto está dentro de um binário e precisa ser
extraído com hex editor + tabela de caracteres. O conector modela isso como **código Python
determinístico**: o usuário fornece o binário, a IA escreve `extract.py` (binário → `dialogs.csv`) e
`reinsert.py` (`approved_translations.csv` → binário traduzido em `output/`). Propriedade-chave:
**round-trip** — extrair e reinserir sem mudanças regenera o binário byte-a-byte. Ver `framework/connectors/`.

> **Convenções de conector (genéricas, travadas por teste):** os scripts **nunca contêm texto da obra**
> (leem dos artefatos) e o **round-trip** é um gate de regressão automatizado (`connector/test_roundtrip.py`,
> pytest) — incluindo um guard data-driven que falha se houver frase hardcoded em `.py`. Servem de
> referência para qualquer instância nova.

---

## ESTRUTURA

```
framework/
  skills/           ← 00..08 — o processo genérico (comece por skills/_index.md)
  schemas/          ← artifacts_schema.md (outputs) + project_schema.md (manifesto)
  media-profiles/   ← games.md (validado), films.md / series.md (stubs)
  connectors/       ← 00_index.md, hex_binary.md, _skeleton/ (extract.py, reinsert.py, table_schema.md)
  runtime/          ← context_pack, state_index, model, run_scene (harness; cena = job stateless)
  validation/       ← validate.py, naturalness_lint.py, cost_model.py (gates determinísticos)
  docs/             ← ARCHITECTURE, STATE_MANAGEMENT, MODEL_INTERFACE, TRANSLATION_PIPELINE, OBSERVABILITY, NAMING, ROADMAP, adr/
  templates/        ← project.template.json + profile/ para novos projetos
  README.md         ← este arquivo

projects/
  utawarerumono/    ← primeira instância de referência (jogo, EN→pt-BR)
    connector/      ← extract.py, reinsert.py, table_schema (adaptados ao binário)
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

- **Jogos** — ✅ validado **em produção** (Utawarerumono): harness de escala rodando, caps 11–13
  traduzidos e verificados, pt-BR renderizando in-game. Ver `media-profiles/games.md`.
- **Filmes** — 🚧 ponto de extensão. Ver `media-profiles/films.md`.
- **Séries** — 🚧 ponto de extensão. Ver `media-profiles/series.md`.

---

## RUNTIME (harness de escala)

Além das skills (o *processo*), `framework/runtime/` é o *harness* que torna a execução sustentável:
cada cena é um **job stateless e limitado** (contexto O(cena), não O(histórico)), o que elimina o
estouro de sessão e viabiliza Sonnet a custo previsível. A LLM faz só cognição (traduzir / verificar
alto risco); orquestração, estado, contexto e validação são determinísticos. Ver
[`runtime/README.md`](runtime/README.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) e a convenção
de nomes em [`docs/NAMING.md`](docs/NAMING.md).

---

## INSTÂNCIA DE REFERÊNCIA

`projects/utawarerumono/` é a prova viva de que o processo funciona em um título real e em escala:
visual novel, EN→pt-BR, com múltiplos pares de identidade dupla e gestão crítica de spoilers. **Caps
11–13 traduzidos e verificados ponta-a-ponta** pelo harness, com saída renderizando no jogo. Use-a como
exemplo de como preencher manifesto e perfil.
