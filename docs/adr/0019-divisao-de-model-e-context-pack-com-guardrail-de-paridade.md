# ADR 0019 — Divisão de `model.py` e `context_pack.py` com guardrail de paridade entre os caminhos

**Status:** proposto · **Data:** 2026-10-18

## Contexto

`model.py` (997 linhas, 37 funções) mistura o caminho de sessão (`translate` in-session, `saved_pack`,
`read_translation`), o caminho de API (`_api_translate`, `batch_translate`, `_translate_params`) e as regras de
tradução que os dois usam (paridade de quebra, orçamento de bytes, blowup, tokens de formatação, dedup por TM).
`context_pack.py` (950 linhas) concentra a montagem do pacote e `render_prompt` (complexidade 30), usados pelos dois
caminhos. Medido em 2026-10-18 (dados sintéticos, mediana de 7 rodadas): `build_pack` 13/31 ms (100/500 linhas),
`session translate` 28/47 ms, overhead mecânico de `_api_translate` 1,7/7,6 ms, import de `model` 45 ms e de
`context_pack` 40 ms.

## Decisão

Dividir os dois arquivos em módulos coesos, mantendo `model.py` e `context_pack.py` como fachada que re-exporta os
mesmos nomes (os testes e os chamadores usam `model._client`, `model.time` etc.). Ordem: primeiro o que os dois
caminhos compartilham, depois o específico de cada um.

### Guardrail: nenhum caminho é beneficiado à custa do outro

1. **API byte a byte:** teste golden do que `_api_translate` envia ao cliente (system, mensagens, `thinking`,
   `output_config`) e da nota de retry. Idêntico antes e depois.
2. **Sessão byte a byte:** teste golden do `scene_prompt.md` e do retorno de `translate(backend="in-session")`.
3. **Testes existentes intocados:** só se acrescenta; se um teste antigo precisar mudar, o passo para e pergunta.
4. **Benchmark dos dois lados:** `perf_bench` ganha as operações de sessão e de API (overhead mecânico),
   `render_prompt` com pacote realista e o tempo de import. Antes e depois, na mesma máquina; nenhuma pode piorar
   mais de 10%.
5. **Sem desequilíbrio:** o saldo dos dois caminhos tem o mesmo sinal. Um ganha e o outro piora = o passo é revertido,
   mesmo dentro dos 10%.
6. **Camadas:** o módulo da sessão não importa nada específico da API (`llm_client`, `anthropic`) e vice-versa; os dois
   dependem só do núcleo compartilhado. Teste de contrato.

Benefício estrutural (menos complexidade, import mais leve) vale como ganho de um caminho desde que o outro não piore
(checks 4 e 5).

## Consequências

- Mais arquivos, cada um menor; a fachada mantém a compatibilidade.
- O custo do guardrail são os goldens e as operações novas no benchmark, feitos antes de mover qualquer código.
- Reverter = voltar o commit do passo (cada módulo sai num commit próprio).
