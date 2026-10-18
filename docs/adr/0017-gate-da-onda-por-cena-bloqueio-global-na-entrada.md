# ADR 0017 — Gate da onda por cena; bloqueio global na entrada da onda seguinte

**Status:** aceito · **Data:** 2026-10-17

## Contexto

No `wave.py`, `glossary_lint` e `quality_gate` varriam o projeto inteiro. Um achado de lint ou um escalonamento
aberto numa cena fora do pedido parava a onda inteira, mesmo com as cenas do pedido limpas (visto no
utawarerumono_prelude: o achado de uma cena derrubava o `wave` das demais, e escalonamentos abertos de uma onda
travavam o fechamento da seguinte). O custo era retrabalho de sessão e uma tentação de contornar o gate.

## Decisão

1. `glossary_lint.py` e `quality_gate.py` ganham `--scenes`; o `wave.py` passa as cenas do pedido.
   Só achado dessas cenas bloqueia (exit 1). Achado de outra cena sai como **aviso** (exit 0) e fica no JSON.
2. O bloqueio global **não some, muda de lugar**: `wave.entry_problems` recusa abrir onda nova (cena sem pack)
   enquanto houver escalonamento aberto de cena fora do pedido. Cena já em andamento (subagente em paralelo)
   não é bloqueada por escalonamento de cena irmã.
3. Sem `--scenes` (uso direto, `run_chapter`), nada muda: o gate continua global.
4. O `glossary_lint` de cena fora do pedido só avisa, sem bloqueio na entrada (decisão do usuário).

## Consequências

- Nenhuma pendência deixa de existir: ela deixa de travar a cena que não tem culpa e trava a próxima onda.
- Não é bypass: não há flag que desligue o gate; o escopo é derivado das cenas do pedido.
- Teste: `test_wave.py`, `test_gates_edges.py`. Reverter = tirar `scope`/`--scenes` do `wave.steps`.
