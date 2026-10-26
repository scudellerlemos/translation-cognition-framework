# ADR 0023 — Passo 5d só retraduz `critical`; as `high` ficam com o Haiku

**Status:** aceito · **Data:** 2026-10-21 · **Decisão do usuário** (Prelude, após o benchmark pareado)

## Contexto

O passo 5d (Sonnet retraduz as falas `high`/`critical` que o Haiku traduziu) era a maior parcela do custo da
onda: US$ 2,46 de US$ 4,46 nas 8 ondas do benchmark A x B (~55%). Quase todas as cenas com 5d tinham só `high`
(19 de 21). O ADR 0022 já tirou as `high` da retrotradução do Opus.

## Evidência

Experimento pareado e cego: 56 falas `high` de 14 cenas, primeira passada do Haiku x versão final do Sonnet,
revisão cega do usuário, critérios fixados antes. Haiku aceitável em 51/56 (91,1%; meta >= 90%). Sonnet venceu
7 de 14 pares com vencedor (50%; meta <= 60%). 31 empates. `glossary_lint` 0 x 0. As 5 reprovações do Haiku
foram deslizes de nuance/tom, sem erro de sentido. Limites: n pequeno (IC inferior ~81%); a passada do Haiku
não passou pelos gates de produção.

## Decisão

O passo 5d da skill `rodar-onda` retraduz só `risk_level` `critical`. As `high` ficam com a tradução do Haiku.

## Salvaguarda

O usuário continua conferindo a amostra de revisão de cada onda. Se a reprovação das `high` passar de 10%,
o 5d volta a cobrir `high`. A medição segue com o mesmo desenho pareado.

## Reverter

Restaurar `high`/`critical` no passo 5d do `SKILL.md`. Não há código: o passo é orquestrado pela skill.
