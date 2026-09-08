# ADR 0004 — Interface fina de modelo + model-mix (Sonnet traduz, Opus verifica)

**Status:** aceito · **Data:** 2026-06-10

## Contexto

O processo "rodava confortável só no Opus". A causa não era a dificuldade intrínseca da tradução por
linha, e sim a dependência de segurar todo o contexto acumulado na cabeça. Com o `context_pack`
entregando contexto pequeno e curado, a tradução por linha cabe em modelos menores.

## Decisão

Isolar a chamada de IA atrás de `framework/runtime/model.py`, com dois backends (assinatura `in-session`
e `api`) e **model-mix** por papel: tradução em **Sonnet 4.6** (default), back-translation em **Opus 4.8**.
A doutrina (Carta) vai no `system` com `cache_control` (cobrada ~1×). Trocar de modelo é trocar uma string.

## Consequências

- (+) Sonnet vira o default de tradução; Opus fica reservado ao alto risco → custo cai (cost_model:
  `mix_cache` ≈ −44% vs tudo-Opus).
- (+) Agnosticismo: o resto do harness não sabe qual modelo rodou.
- (+) Caminho assinatura e caminho API compartilham o mesmo contrato e o mesmo pacote de contexto.
- (−) O caminho `api` precisa de endurecimento contra o SDK vivo antes de produção (P1; ver
  `MODEL_INTERFACE.md`).
