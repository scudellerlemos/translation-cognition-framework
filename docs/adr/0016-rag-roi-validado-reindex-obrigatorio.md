# ADR 0016 — RAG semântico: ROI validado por medição real; reindex incremental vira obrigatório

**Status:** aceito · **Data:** 2026-09-09

## Contexto

Issue [#175](https://github.com/scudellerlemos/translation-cognition-framework/issues/175) exigia
medir ROI real do RAG semântico (`framework/db/embedder.py`) antes de generalizar mais infra
(chunking #169, threshold #172, onboarding #174) — até então a decisão era só teórica/técnica
("está ligado e funciona"), nunca medida em custo/qualidade real.

Experimento: as mesmas 10 cenas reais de produção do `breath_of_fire_4` traduzidas duas vezes —
uma cópia com RAG desligado (sem `db`), outra com RAG ligado (`db index --force` reindexado após
cada cena, retrieval acumulando dentro do próprio lote). Orçamento aprovado: R$20 (~$3,77);
gasto real: $2,25.

**Resultado:**

| | RAG-off | RAG-on | Delta |
|---|---:|---:|---:|
| Custo total (10 cenas) | $1,2797 | $0,9714 | **-24%** |
| Cenas com sucesso | 5/10 | 7/10 | **+2** |
| Custo por cena traduzida com sucesso | $0,138 | $0,086 | **-38%** |

O ganho não veio de "achar contexto semanticamente parecido" — veio de **reuso exato de linhas
repetidas** (texto de sistema/menu comum entre áreas do jogo) assim que o índice tinha a linha
gêmea indexada: 2 das 10 cenas saíram a **$0,00** (reuso 100% via TM, zero tokens) contra
$0,066–$0,155 na mesma cena sem RAG. `glossary_lint`/`naturalness_lint` não mostraram regressão de
qualidade em nenhuma das duas condições. Detalhe completo:
[comentário no #175](https://github.com/scudellerlemos/translation-cognition-framework/issues/175#issuecomment-5608095339).

Achado colateral do próprio experimento: a issue [#182](https://github.com/scudellerlemos/translation-cognition-framework/issues/182)
(ligar reindex ao write-path real — `upsert_translation`/`run_scene` —, não só à migração manual)
já estava aberta e **explicitamente bloqueada** por este ADR: _"Depende de #175 fechar com ROI
positivo — não vale automatizar o reindex de uma feature cujo valor ainda não foi medido."_

## Decisão

**ROI é positivo e mensurado — RAG semântico (nº1, TM) está validado para uso em produção.**
O alavancador observado é reuso exato via índice atualizado, não afinamento de threshold semântico
nem chunking de conteúdo não-atômico (#169/#172 já fechados sem essas frentes se provarem
necessárias no caso medido).

Consequência direta: **manter o índice sempre atualizado deixa de ser boa prática opcional e vira
requisito obrigatório** para qualquer projeto com `db.path`/`project_id` configurado. Concretamente:

1. **#182 está desbloqueada** — reindexação incremental deve ser ligada ao write-path real
   (`upsert_translation`/`run_scene`), não depender de `db migrate` manual. Prioridade imediata
   sobre chunking/threshold (que não têm evidência de ROI neste momento).
2. Enquanto #182 não for implementada, qualquer projeto com RAG ligado **deve** rodar
   `db index --force` após cada lote de cenas aprovadas — trata-se de requisito de operação, não
   de otimização opcional. Um índice desatualizado silenciosamente devolve retrieval vazio/estale
   sem erro visível (nenhum teste ou aviso captura o gap hoje — parte do critério de pronto do #182).
3. #174 (onboarding de projeto novo com RAG) deve incluir este requisito explicitamente no fluxo,
   não como nota de rodapé.

## Consequências

- (+) Decisão de investir mais em RAG deixa de ser uma aposta — está ancorada em número real,
  medido em produção, sob orçamento controlado.
- (+) Escopo do próximo trabalho fica mais estreito: reindex freshness (#182) é a alavanca real;
  chunking/threshold deixam de ser prioridade sem evidência própria de que movem o resultado.
- (+) Amostra pequena (10 cenas) e conservadora — TM histórica das 125 cenas originais do BoF4
  havia sido apagada antes do experimento, então o índice foi populado sequencialmente dentro do
  próprio lote de teste. Produção real acumula bem mais histórico pra puxar — o ROI medido é
  provavelmente um piso, não o teto.
- (−) Até #182 ser implementado, "manter índice atualizado" depende de disciplina manual
  (`db index --force` no fluxo de cada lote) — risco de esquecimento sem enforcement automático.
- Fora de escopo deste ADR: nº2 (KB/lore semântico) e nº3 (cross-game) não foram medidos aqui —
  a validação de ROI é específica de nº1 (TM semântica); ver `docs/STACK.md` para o status de cada
  retriever.

**Reabrir se:** medição em corpus maior/produção real mostrar que o ganho medido aqui não se
sustenta (ex.: reuso exato cai a zero fora do caso "texto de sistema repetido entre áreas"), ou se
#182 revelar que reindex por cena tem custo de latência/infra que muda o cálculo.
