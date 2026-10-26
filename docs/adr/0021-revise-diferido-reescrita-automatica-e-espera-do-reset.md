# ADR 0021 — `revise` na fila diferida, reescrita automática pelo Sonnet e espera do reset da cota

**Status:** aceito · **Data:** 2026-10-19 · **Decisão do usuário** (três itens, resposta "sim" a cada um)

## Contexto

O objetivo é traduzir o jogo inteiro dentro do plano Pro sem o usuário pedir cada onda. Duas coisas ainda o
obrigavam a aparecer: o `revise` da retrotradução (bloqueia o `quality_gate` da onda; a marca `escalate` não
isenta a fala, e aceitar o `revise` só falsificando o veredito, o que o processo proíbe) e o limite de cota
(o `rodar_ondas.ps1` só entendia o aviso de sessão com horário, no máximo 3 vezes por onda). Na onda 33, uma
única fala travou a onda por três rodadas de retrotradução (conflito entre tom e orçamento de bytes).

## Decisão

1. **`revise` na fila diferida.** Com `"hitl_fila": "diferida"` no `project.json`, linha `revise` das cenas da
   onda vira aviso no `quality_gate --scenes` (mesma regra do escalonamento, ADR 0020). `--fechar` volta a
   bloquear. Cobertura (`SEM COBERTURA`) **continua bloqueando**: é buraco na rede, não julgamento. Sem a
   chave, nada muda.
2. **Reescrita automática, no máximo 2 tentativas.** Antes de adiar, o orquestrador lança o Sonnet para
   reescrever a fala dentro do `byte_budget` e o Opus re-julga só aquela fala; passou ou esgotou as 2
   tentativas, a onda segue. A fala que continua `revise` entra na tabela única do fim do lote (cena, fala,
   nota do juiz, sem texto do jogo no texto público); o usuário decide e o gate fecha só depois.
3. **Espera do reset.** `framework/runtime/espera_reset.py` lê o aviso de limite (sessão ou semana, com
   horário, data ou epoch) e o `rodar_ondas.ps1` dorme até lá (+2 min) e refaz a onda, até 8 vezes.

## Salvaguarda

Não é bypass: o veredito nunca é editado e o `--fechar` (fim de lote e antes de instalar) bloqueia com
`revise` aberto. O Sonnet não decide o que fica: quem aceita uma fala `revise` é o usuário, na tabela final.
Risco: uma fala pior que o juiz apontou segue para as cenas seguintes até o fim do lote; mitigação: o teto de
2 tentativas e a tabela final.

## Consequências

- Reverter: remover `hitl_fila` do `project.json` (volta a parada na onda).
- Custo: cada tentativa extra é ~US$ 0,15 (Sonnet + Opus de uma fala); o teto de 2 limita o gasto por fala.
- Testes: `test_gates_edges.py` (`test_quality_gate_defer_only_with_diferida_and_not_fechar`,
  `test_quality_gate_revise_is_deferred_in_diferida_and_blocks_on_fechar`), `test_espera_reset.py`.
