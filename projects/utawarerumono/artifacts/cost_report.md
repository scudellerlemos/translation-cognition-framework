# Cost Report — modelo de custo de PRODUÇÃO (via API)

> Estima o custo de produção (API, lotes + caching), **não** o desta sessão.
> Tokens ≈chars/3.8 (refinar com `messages.count_tokens`). Preços: skill claude-api 2026-05-26.

```
Arco: 1025 linhas | lotes de 200 (6) | alto risco: 9 | risco {'low': 1007, 'medium': 9, 'high': 9}
Contexto cacheável ~3840 tok | source ~9081 tok | alvo ~9032 tok

cenário         $ arco   $/1k linhas    $ ~33k (proj.)
forte            3.196         3.118            102.91
mix              1.929         1.882             62.11
mix_cache        1.790         1.747             57.64

Economia mix+cache vs forte: -44%
(estimativa por heurística de tokens ≈chars/3.8 + caching; refinar com count_tokens)
```
