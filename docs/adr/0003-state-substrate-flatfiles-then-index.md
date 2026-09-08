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

## Atualização 2026-06 — RAG-parcial de graça (keyword reforçado)

Medido (cap.13): RAG **não baixaria custo** (dominado por output ~$5,53 vs ~$0,77 de TODO o input;
retrieval é fração disso) e **quebraria "só API Anthropic"** (embeddings = Voyage AI, 2º serviço pago) +
infra de vetor. Logo, capturamos **parte** do ganho semântico melhorando o keyword do `context_pack` —
**sem serviço novo**:
- `_present`: tolerância de plural/inflexão inglesa (`\b<termo>(?:e?s)?\b`) — pega "Cohorts"/"generals"
  que o match estrito perdia (medido: 7 "Cohorts" no corpus antes invisíveis).
- `select_decisions`: também casa pelo **conteúdo do `summary`**, não só pela tag do título.
- aliases distintivos no glossário: revisados — mas as formas alternativas seguras (war fan, Eight
  Pillars, Emperor…) **não aparecem no corpus**, então nada a adicionar (honestidade > recall; não
  inventar). Confirma o **teto**: sinônimos DESCRITIVOS de palavra comum ("o general mascarado")
  over-matcheiam no keyword — **isso** é o que exige RAG.

**Gatilho de RAG (inalterado, agora mais preciso):** adotar vetorial só quando o keyword reforçado
**ainda** errar — i.e., precisar de sinônimo descritivo/semântico ou a busca degradar em escala. Não é
custo; é qualidade/escala de retrieval.
