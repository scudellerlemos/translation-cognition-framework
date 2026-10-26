# ADR 0025 — Retrotradução cega em duas passagens (opt-in)

**Status:** rejeitado como padrão (medido em 2026-10-25; fica opt-in, desligado por padrão) · **Data:** 2026-10-25
**Decisão do usuário:** passagem A em Sonnet.

## Contexto

Hoje o juiz da retrotradução recebe `source` e `target` juntos e traduz de volta já tendo visto o original. O
`back_en` sai viciado pelo source e o `pass` fica mais fácil do que deveria.

## Decisão

Com `back_translation_cega: true` no `project.json`, o caminho de sessão grava dois prompts por cena:

- **A** (`back_prompt_<id>.md`): só `offset`, falante e `target`. Quem roda (Sonnet) não vê o source. Grava `back_a_<id>.json`.
- **B** (`back_prompt_juiz_<id>.md`): `source`, `target` e o `back_en` da A. O juiz julga `pass|revise` e grava o
  `back_translation_<id>.json` de sempre, sem mudar o formato que o `quality_gate` lê.

Sem a chave, nada muda.

## Medição A/B (2026-10-25)

Ferramenta: `framework/runtime/bench_retro_cega.py` (sorteio, montagem dos dois braços, placar). Verdade conhecida:
60 falas aprovadas do Prelude em 6 cenas, 30 intactas e 30 com um defeito rotulado injetado (`sentido_invertido` 8,
`omissao` 8, `tom` 6, `nome_errado` 4, `adicao` 4; defeitos gerados por Sonnet). Braço **padrão**: Opus vê o source.
Braço **cega**: A em Sonnet (só o target) e B em Opus (com source e `back_en`). Critério fixado antes: adotar a
cega só se recall ≥ padrão + 10 pp e falso alarme ≤ padrão + 10 pp.

| braço | recall | falso alarme |
|---|---|---|
| padrão | 24/30 (80%) | 2/30 (6,7%) |
| cega | 24/30 (80%) | 1/30 (3,3%) |

Empate em recall, diferença de 1 fala no falso alarme: **critério não atingido**, a cega não pega mais defeito
e custa duas passagens. Em ambos os braços `omissao` é o ponto fraco (4/8). Limites: n = 60, um modelo, defeitos
sintéticos, uma semente; a diferença de 1 fala não é distinguível de ruído.

## Decisão

Mantida a implementação opt-in, desligada por padrão; não vale ligar em projeto. Se quiserem insistir, o ganho a
buscar é em `omissao` (nenhum dos dois pega metade), não na cegueira.

## Reverter

Remover `_cega` e `_write_back_prompts_cegos` de `back_translate.py`. Sem a chave, o código não executa.
