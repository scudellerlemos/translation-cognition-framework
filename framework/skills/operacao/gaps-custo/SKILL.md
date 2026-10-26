---
name: gaps-custo
description: Identifica gaps de custo e de performance das respostas do framework, do ponto de vista de um AI engineer com a visao do projeto inteiro: qual parafuso apertar e que metrica justifica a otimizacao. Rodar no fim de uma onda ou antes de decidir mudanca de arquitetura.
---

# Gaps de custo e performance

Roda `python framework/skills/operacao/gaps-custo/gaps.py projects/<nome>` (raiz do repo). Filtros: `--sessao <prefixo do id>` (overhead de uma sessao/onda) e `--cenas <cena>...` (custo e falhas das cenas; sem overhead, que nao tem cena). Traz tambem falhas por causa (`code`) e cache por requisicao. Le `artifacts/` (`api_ledger.jsonl`,
`events.jsonl`, `metrics.jsonl`, `run_state.json`) e imprime 6 blocos (o 1b abre o custo por modelo e por fase, incluindo a retrotraducao `phase=back`). Depois interpreta com a tabela abaixo.
So le e relata: nao altera runtime nem ROADMAP; registrar no ROADMAP do projeto e decisao separada (skill `levantar-melhorias`).

## Parafusos (do maior para o menor retorno esperado) e a metrica que justifica cada um

| Parafuso | Metrica (bloco) | Sinal de gap | Otimizacao candidata |
|---|---|---|---|
| Overhead fora da traducao | % do custo em `overhead` (1) | >30% do total | menos conversa de sessao, skills enxutas, `--no-chrome`, medir por `activity` |
| Retrabalho (falha e nova traducao) | falhas por cena verified (4) | >0,5 | precheck, conserto mecanico, gate cedo; custo = falhas x $/cena |
| Cena outlier | $/fala > 2x mediana (3) | cena de poucas falas e cara | tamanho minimo de cena, agrupar cenas curtas, `scene_dedup` |
| Tokens de saida | saida tok/fala (3) | >2x o texto traduzido | JSON enxuto, sem eco do prompt, sem reescrever o que a memoria de traducao ja tem |
| Cache | cache_read/entrada (2) | <90% ou escrita de cache alta | prefixo estavel no prompt (glossario e doutrina antes, cena depois) |
| Requisicoes por fala | req/fala (3) | subindo entre ondas | menos idas e voltas do subagente, lote maior |
| Modelo | $ e % por modelo/fase (1b) | modelo caro em fala de risco baixo | roteamento por risco (Sonnet no padrao, Opus so no `risk>=high`/retrotraducao) |
| Gate que roda sem valor | contagem por `stage` (4) | muitos `block` sem efeito | corrigir o registro antes de otimizar (ex.: `gate.connector`) |

## Regras de interpretacao

- Custo "equivalente API" e a unidade: no caminho de sessao o gasto real e $0, mas o equivalente e o que a API cobraria.
- Otimizacao so entra no ROADMAP com a metrica **antes** e a meta **depois** (ex.: "falhas por cena 1,5 -> 0,5").
  Sem baseline medido, e hipotese, nao melhoria.
- Mostrar a projecao do jogo todo (5) junto: ganho por fala x falas restantes = economia total.
- Comparar sempre onda contra onda: rodar antes e depois de um conserto de runtime e anotar os dois numeros.
- Atribuicao por janela de tempo e o metodo adotado (o transcript nao traz a cena por requisicao); a separacao
  por cena e por fase e aproximada por desenho, nao um defeito a corrigir. Retrotraducao so tem custo medido
  quando a sessao ecoa `AGUARDANDO back-translation` (`phase=back`).
- Limites conhecidos: o evento `gate.connector` registra `block` em toda rodada (nao e bloqueio real).
- Texto no ROADMAP: sem fala do jogo.
