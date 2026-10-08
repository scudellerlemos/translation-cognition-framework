# CONNECTORS.md — conector e round-trip

A parte determinística que devolve o texto traduzido ao binário do jogo, e a verificação que
garante que o jogo não quebra. Visão da stack inteira → [`STACK.md`](STACK.md).

Traduzir o texto é metade do problema. A outra metade é devolver esse texto a um arquivo binário
que o jogo consiga ler. Essa parte é **determinística**, específica de cada jogo, e é o que o
conector resolve.

## O que é um conector

É um conjunto de scripts Python em `projects/<jogo>/connector/`, com um contrato fixo:

| Script | O que faz |
|---|---|
| `extract.py` | lê o binário do jogo e gera `dialogs.csv`: uma linha por fala, com `offset` (onde ela está no arquivo), o texto-fonte e `byte_budget` (quantos bytes ela ocupa) |
| `build_plan_chapter.py` | junta a tradução do modelo com o `dialogs.csv`: valida cobertura e tokens de formatação, e grava o plano de reinserção |
| `reinsert.py` | codifica a tradução no formato do jogo e reconstrói o arquivo |
| `verify_chapter.py` | executa o round-trip e devolve o veredito |
| `test_roundtrip.py`, `test_roundtrip_synthetic.py` | testes do próprio conector |

O que é comum a todos os jogos (linha de comando, validação de cobertura, protocolo de saída) vem
de um esqueleto em `framework/connectors/_skeleton/`. O que não dá para generalizar é a
reconstrução byte a byte do formato: tabela de caracteres, códigos de controle, ponteiros,
contêiner. Isso é escrito por jogo.

Quatro jogos têm conector, cada um com uma restrição de espaço diferente (o estágio de cada um
está em [`STACK.md`](STACK.md#onde-cada-projeto-está-hoje)):

| Projeto | Engine / formato | Restrição de espaço |
|---|---|---|
| `utawarerumono` | Aquaplus (SDAT) | orçamento em bytes por fala; reinserção no lugar, com realocação dentro do arquivo |
| `breath_of_fire_4` | Capcom (PS1/PC), tabela de ponteiros por seção | orçamento em bytes por fala; a seção é reconstruída |
| `souldiers` | Unity 2021 (Addressables) | sem limite de bytes; a engine quebra a linha sozinha |
| `trails_sky_sc` | engine própria da Falcom | quebra automática, sem quebra manual |

## O round-trip

O `verify_chapter.py` faz três verificações, nesta ordem:

1. **Round-trip.** Reconstrói o arquivo **sem aplicar tradução nenhuma** e compara com o original,
   byte a byte. Se não bate, o conector não entende o formato, e nada que ele escrever é
   confiável. É o teste que não admite exceção.
2. **Aplicação.** Reconstrói o arquivo com a tradução da cena.
3. **Releitura.** Extrai o texto do arquivo reconstruído e confere que é a tradução aplicada.

O resultado segue um protocolo único, que o orquestrador lê:

| Código de saída | Significado | O que o run faz |
|---|---|---|
| `0` | as três verificações passaram | a cena vira `verified` e a tradução é aprovada |
| `3` | a única falha foi falta de espaço | re-traduz mais curto (ver abaixo) |
| `1` | falha dura (round-trip, leitura ou outra) | para; é defeito de conector, não de tradução |

## Quando a tradução não cabe

Em jogos com orçamento de bytes, o português costuma sair maior que o inglês. O tratamento é
gradual:

- **Tolerância inicial de 1,40.** A tradução pode passar do orçamento da fala em até 40%, porque
  os conectores conseguem absorver crescimento (realocando ou reconstruindo a seção). Traduzir sem
  aperto dá texto mais natural e menos re-tentativas.
- **O `verify` é o juiz.** Se o arquivo reconstruído não fecha, ele devolve código `3`.
- **Aperto progressivo.** O run re-traduz só as falas acima do orçamento, com tolerância 1,15 no
  Haiku; o que ainda não couber vai a 1,0 no Opus (`BUDGET_ESCALATION` e `MODEL_ESCALATION`). O
  modelo caro só vê o resíduo que provou ser difícil. Vale só no backend de API, que roda sem
  intervenção humana.
- **O orçamento é medido nos bytes que serão gravados.** Se o conector translitera os acentos na
  reinserção, conta o texto transliterado; se grava UTF-8, contam os bytes UTF-8.

Como criar um conector para um jogo novo → [`NEW_PROJECT_ONBOARDING.md`](NEW_PROJECT_ONBOARDING.md).
