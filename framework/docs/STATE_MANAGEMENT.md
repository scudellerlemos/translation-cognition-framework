# State Management — conhecimento permanente vs contexto temporário

O harness opera sem usar a janela da LLM como memória. Esta é a separação de estados.

## Conhecimento PERMANENTE (sobrevive entre cenas; é a "memória" do projeto)

| Estado | Arquivo | Quem escreve | Papel |
|---|---|---|---|
| Glossário | `artifacts/glossary.csv` | passo 04 (IA propõe, humano aprova) | termos + `handling_rule` + spoiler |
| Memória de tradução (TM) | `artifacts/state/translation_memory.jsonl` | `state_index.py` (det.) | toda fala já traduzida → reuso/consistência |
| Voice cards | `artifacts/state/voice_cards.json` | `state_index.py` (det.) | voz por personagem, destilada (~300 tok) |
| Índice de decisões | `artifacts/state/decision_index.json` | `state_index.py` (det.) | tag→regra; carrega só o relevante |
| Lore / universo | `artifacts/universe_knowledge_base.md` | passo 03 | mundo, spoilers, reveal_timing |
| Decisões (fonte) | `artifacts/decision_log.md` | passos 04b+ | auditoria acumulativa (nunca apagar) |
| Progresso narrativo | `artifacts/translation_status.json` | passo 06 | next_offset, needs_human_review |
| Checkpoint do harness | `artifacts/run_state.json` | `run_scene.py` (det.) | status por cena (resume) |

## Contexto TEMPORÁRIO (por cena; descartável e regenerável)

| Estado | Arquivo | Vida |
|---|---|---|
| Pacote de contexto | `artifacts/<cena>/pack.json` + `scene_prompt.md` | recomputável de `state/` + dialogs |
| Plano da cena | `artifacts/<cena>/translation_plan_<scene_id>.json` | derivado de translations + dialogs |
| Logs de QA | `micro_qa_log.json`, `back_translation_<scene_id>.json` | por lote/cena |

Regra: se um estado é **derivável** de outros, ele é temporário (regenerar > guardar). A TM, os voice
cards e o decision_index são derivados (de `translation_plan*`, `tone_analysis.md`, `decision_log.md`),
mas são **materializados** porque o `context_pack` os consulta a cada cena — materializar é a otimização
que tira a leitura desses fontes grandes da janela.

## Substrato: por que flat files + índice fino AGORA (e não banco/vetor)

Escolha: **arquivos estruturados (CSV/JSONL/JSON) + um índice materializado leve**, versionados em git.
Ver `adr/0003-state-substrate-flatfiles-then-index.md`.

| Abordagem | Quando | Veredito atual |
|---|---|---|
| Flat files + índice (atual) | sempre — o 80/20 | **adotado**. Portável, versionável, diff-ável, zero infra. |
| Banco relacional | múltiplos projetos + consultas transacionais | adiar (P2). |
| Banco vetorial / RAG | recuperação **semântica** sobre lore/decisões grandes | só quando a recuperação por tag/termo não bastar (P2). Hoje a TM é lookup por chave exata + voz por falante — não precisa de embeddings. |
| Knowledge Graph | relações densas entre entidades | overengineering. `entities.csv` + `aliases_map.json` bastam (P3). |

**Gatilho para evoluir** (documentar quando ocorrer): o `context_pack` passar a precisar de "decisões/lore
semanticamente parecidas" que a busca por tag não acha → aí entra RAG/vetor **só sobre** `decision_log`
+ `universe_knowledge_base`, mantendo o resto em flat files.

## Reconstrutibilidade

`state_index.py` é **idempotente**: apagar `artifacts/state/` e rodar `python state_index.py <projeto>`
reconstrói TM + voice cards + decision_index byte-idênticos a partir dos artefatos. Travado por
`test_state_index_idempotent`. Isso garante que o estado nunca é uma caixa-preta presa à sessão.
