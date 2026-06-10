# ADR 0003 — Substrato de estado: flat files + índice materializado leve (vetor/banco só depois)

**Status:** aceito · **Data:** 2026-06-10

## Contexto

O harness precisa de memória externa consultável (consistência sem usar a janela). Opções: flat files,
banco relacional, banco vetorial/RAG, knowledge graph. A pergunta é qual cabe num framework de tradução
**neste estágio** (prioridade: traduzir o jogo de forma sustentável, não construir a arquitetura perfeita).

## Decisão

Usar **arquivos estruturados** (CSV/JSONL/JSON) versionados em git + um **índice materializado leve**
(`framework/runtime/state_index.py`) que deriva, de forma idempotente: `translation_memory.jsonl`
(lookup por chave exata de source + voz por falante), `voice_cards.json`, `decision_index.json`
(tag→regra). Sem banco, sem embeddings, sem infra.

## Alternativas e gatilhos

- **Banco relacional** — adiar (P2): justifica-se com múltiplos projetos + consultas transacionais.
- **Vetorial / RAG** — adiar (P2): justifica-se **só** quando o `context_pack` precisar de "decisões/lore
  semanticamente parecidas" que a busca por tag/termo não acha — e mesmo aí, só sobre `decision_log` +
  `universe_knowledge_base`. Hoje a recuperação é por chave/tag, que não precisa de embeddings.
- **Knowledge graph** — não fazer (P3): `entities.csv` + `aliases_map.json` cobrem as relações.

## Consequências

- (+) Zero infra, portável, diff-ável, reconstruível (travado por `test_state_index_idempotent`).
- (+) Migração futura é localizada: só `state_index.py` + `context_pack.py` consomem o estado.
- (−) Busca semântica não existe até o gatilho de RAG ser atingido (aceitável agora).
