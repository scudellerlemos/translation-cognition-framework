# ADR 0009 — Modo batch como default de custo, com abort seguro em falha

**Status:** aceito · **Data:** 2026-08-30

## Contexto

`run_chapter.py` já suportava `--batch` (submete as cenas pendentes do capítulo num único batch da
API, 50% off) desde antes desta ADR, mas com default `batch=False` — era preciso lembrar de passar a
flag toda vez pra pagar metade do preço. Pior: quando o batch em si falhava (não a cena, o batch como
um todo — ex.: erro de rede, ou um modelo rejeitando um parâmetro do request), `_batch_phase` capturava
a exceção e caía **silenciosamente** no caminho interativo full-price para todas as cenas pendentes.
Aconteceu na prática: Haiku rejeitando `effort` no corpo do batch derrubou 9/9 cenas pro caminho caro,
e ninguém percebeu até investigação manual do ledger de custo — o mesmo tipo de "gasto surpresa" que
o teto `--max-usd` existe pra evitar (ver `_chapter_cost`/`max_usd` em `run_chapter.py`).

## Decisão

- `run_chapter()` e o CLI (`run_chapter.py main()`) invertem o default: `batch=True` (era `False`).
  Novo flag `--no-batch` desliga (era `--batch` pra ligar) — cobre o caso de debug interativo com
  feedback imediato por cena.
- `_batch_phase` passa a retornar `(status_dict, failed)` em vez de só `status_dict`. Se o batch em SI
  falhar (exceção em `M.batch_translate`), o novo default é **abortar** o capítulo inteiro
  (`status: "batch_failed"`) em vez de cair no caminho interativo sem avisar.
- Novo flag `--allow-interactive-fallback` (`allow_interactive_fallback=False` por padrão) destrava o
  comportamento antigo de propósito, para quem prefere pagar full-price a esperar corrigir o batch.

## Consequências

- (+) Custo 50% menor é o caminho padrão sem precisar lembrar de uma flag — alinhado com a filosofia
  de nunca gastar caro por omissão (mesmo racional do `--max-usd`).
- (+) Falha do batch em si vira parada visível (`batch_failed`) em vez de virar um capítulo inteiro
  traduzido a preço cheio sem ninguém saber — fecha exatamente o incidente relatado acima.
- (−) Quebra o default de scripts/CI existentes que chamavam `run_chapter(..., batch=False)`
  implicitamente (dependiam do default antigo); `test_runtime.py` precisou de `batch=False` explícito
  em 4 testes pré-existentes que mockam `run_scene`/`_chapter_cost` (não testam batch em si).
- Fora de escopo (dívida conhecida): nenhum teste novo cobre `_batch_phase`'s aborto/fallback nem
  `--allow-interactive-fallback` diretamente — só os 4 testes ajustados pra manter o comportamento
  anterior. Candidato a próxima sessão.
