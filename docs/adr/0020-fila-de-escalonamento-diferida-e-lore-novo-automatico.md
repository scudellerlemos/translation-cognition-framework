# ADR 0020 — Fila de escalonamento diferida e lore novo automático

**Status:** aceito · **Data:** 2026-10-18 · **Decisão do usuário** (pedido explícito, três itens)

## Contexto

No modo contínuo (`rodar_ondas.ps1`), cada escalonamento do tradutor parava o lote: o `quality_gate` e a entrada da
onda seguinte (ADR 0017) exigem a fila zerada. Nas ondas 11 e 12 do utawarerumono_prelude, os itens eram nomes
inventados (lugar, remédio, animal) cuja resposta foi sempre "manter o original". Uma parada por onda tira o sentido
de rodar em lote.

## Decisão

1. **Lore novo automático.** O tradutor que mantém no original um nome próprio, item, criatura ou lugar sem forma
   no glossário marca `"lore_novo"` na fala (não `escalate`). `hitl.after_batch` chama `adopt_new_lore`: o termo
   entra no `glossary.csv` como `manter_original` (categoria "Lore (auto)"), com registro no `hitl_log.jsonl`
   (`by: regra-permanente`). Trocadilho, duas leituras, termo que não cabe no orçamento e glossário em conflito
   continuam `escalate`.
2. **Levantar o lore antes do lote.** `rodar_ondas.ps1 -Lore` roda `kb_phase.py ... onda` para as próximas ondas do
   `panorama.py` e grava uma tabela única; as formas se decidem antes de lançar o lote.
3. **Fila diferida.** `"hitl_fila": "diferida"` no `project.json`: escalonamento aberto não bloqueia a entrada da
   onda seguinte, o `quality_gate --scenes` nem o `glossary_lint --scenes` (achado já enfileirado vira aviso). A
   fila é respondida no fim do lote.

## Salvaguarda

Não é bypass: o bloqueio muda de lugar. `quality_gate.py --fechar` e `glossary_lint.py --fechar` voltam a bloquear
com a fila aberta e valem no fim do lote e antes de instalar. Sem a chave `hitl_fila`, nada muda (padrão
bloqueante). Os gates de qualidade (`revise`, cobertura) não mudam.

## Consequências

- Risco: retrabalho se uma forma errada se propagar por várias cenas antes da resposta. Mitigação: o passo 2 e a
  regra do lore novo (o termo vira regra de glossário e o lint a aplica nas cenas seguintes).
- Reverter: remover `hitl_fila` do `project.json`.
- Testes: `test_hitl.py` (`test_new_lore_enters_glossary_as_keep_original_once`,
  `test_deferred_queue_does_not_block_entry_but_fechar_does`).
