# ADR 0024 — Coluna opcional `forma_curta` no glossário

**Status:** aceito · **Data:** 2026-10-25 · **Decisão do usuário** (levantamento de lições do Prelude)

## Contexto

Termo com tradução canônica longa estoura o `byte_budget` de rótulos e menus. O tradutor encurtava por conta
própria e o `glossary_lint` acusava a forma curta como inconsistência, indo para a fila do humano. O mesmo
termo reaparecia em dezenas de cenas.

## Decisão

O `glossary.csv` (e o `glossary.local.csv`) aceita a coluna opcional `forma_curta` (várias formas separadas por
`;` ou `|`).

- `glossary_lint` trata a forma curta como forma válida do termo (igual a um alias).
- O prompt da cena (`pack_render`) mostra a coluna "forma curta" só quando algum termo da cena a usa; sem a
  coluna, o prompt não muda.

## Limite

Projeto com banco (`db`) ainda não carrega a coluna: o `store.get_glossary` não a devolve, então nesses
projetos a forma curta continua como alias. Levar a coluna ao banco é migração de schema, fica para quando
um projeto com banco precisar.

## Reverter

Remover a coluna dos CSVs e as duas leituras de `forma_curta` (`glossary_lint._load_glossary`,
`pack_render._glossario`). Sem a coluna, nada muda.
