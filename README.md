# Translation Cognition Framework

Framework **spec-driven** para tradução baseada em **cognição narrativa**. Separa entendimento,
estrutura, regras, planejamento, execução e validação para preservar **identidade, tom e
consistência** em textos complexos como jogos, filmes e séries.

A ideia central: localização de qualidade não é traduzir linha a linha — é entender o universo,
fixar regras auditáveis e executá-las com verificação contínua. O framework torna cada uma dessas
etapas explícita, com gates que impedem avançar sobre uma base incompleta.

---

## Estrutura do repositório

```
framework/     → O PROCESSO (genérico, reutilizável). Não contém dados de obra nenhuma.
projects/      → AS INSTÂNCIAS. Cada obra traduzida vive em projects/<título>/.
```

- **`framework/`** — os passos do SDD (`00..08`), schemas, perfis de mídia (jogos/filmes/séries) e
  conectores (extração/reinserção). Comece por [`framework/README.md`](framework/README.md).
- **`projects/`** — cada projeto traz seu `project.json` (manifesto), `profile/` (dados curados) e
  `artifacts/` (outputs gerados). O `media_type` vive no manifesto — sem hierarquia de pastas por mídia.

---

## O modelo em camadas

| Camada | Onde | O que é |
|--------|------|---------|
| Processo | `framework/skills/` | Os passos do SDD — genéricos, sem dados de obra |
| Categoria | `framework/media-profiles/` | Preocupações por tipo de mídia (jogos ✅, filmes/séries 🚧) |
| I/O | `framework/connectors/` | Código determinístico que extrai/reinsere texto no meio (binário, etc.) |
| Instância | `projects/<título>/` | Manifesto + perfil + artefatos + scripts do conector |

As skills resolvem tudo que é específico de uma obra lendo o `project.json` e os artefatos gerados.

---

## O pipeline (00 → 08)

```
00 extração      → conector: binário → corpus canônico (+ orçamento de bytes); gate de round-trip
01 discovery     → entidades, tom, aliases, spoilers
02 entidades     → registro canônico
03 conhecimento  → pesquisa colaborativa (IA + usuário) → base de conhecimento
04 glossário     → regras normativas de tradução (+ decision log)
05 planejamento  → plano linha a linha (+ corpus de teste sintético)
06 tradução      → execução em lotes, auto-revisão de voz, orçamento de bytes (shift-left)
06b/06c QA       → micro-QA por lote + ciclo de correção cirúrgica
07 QA final      → consistência global, spoilers cross-segmento
08 reinserção    → conector: tradução → binário + patch (determinístico; LLM só no resíduo)
```

---

## Começar

1. Leia [`framework/README.md`](framework/README.md) — modelo de camadas e como instanciar um projeto.
2. Veja a instância de referência em [`projects/utawarerumono/`](projects/utawarerumono/README.md) —
   um jogo (visual novel), EN→pt-BR, com identidades duplas e gestão crítica de spoilers.
3. Para um projeto novo: copie `framework/templates/project.template.json`, preencha o manifesto e
   rode o pipeline na ordem `00..08`.

---

## Status

- **Processo (skills 00–08):** maduro.
- **Jogos:** validado na instância de referência (Utawarerumono). Pipeline 00→08 rodado de ponta a
  ponta em **2 cenas / 1025 linhas** (EN→pt-BR): extração por arco, tradução, repoint e patch IPS.
  Conector `hex_binary` com **modelo de ponteiro file-relativo** e **gate de regressão automatizado**
  (`pytest`, incl. um guard de governança que barra texto da obra hardcoded em `.py`).
- **Pendente para produção:** validação in-game das strings relocadas; run do jogo inteiro
  (estratégia incremental por capítulo em [`ROADMAP.md`](ROADMAP.md)).
- **Filmes / séries:** pontos de extensão documentados (`framework/media-profiles/`), ainda não validados.
