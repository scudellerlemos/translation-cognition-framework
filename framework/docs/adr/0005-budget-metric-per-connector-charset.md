# ADR 0005 — Métrica de byte_budget por charset do conector (transliterado vs. UTF-8 real)

**Status:** aceito · **Data:** 2026-08-24

## Contexto

`trails_sky_sc` cena `mp0010_01`: 308/447 linhas `soft_failed` por estouro de `byte_budget`. Causa raiz
não era "o modelo traduz longo demais" — `_translit_len()` (comprimento NFKD, sem acentos) era usado como
métrica de orçamento **incondicionalmente**, em todo o pipeline (prompt, retry, escalonamento). Isso é
correto para `bof4`/`utawarerumono`, cujo `reinsert.py` translitera para ASCII na gravação (acento
realmente some, então o budget certo é o do texto sem acento). É **errado** para `trails_sky_sc`, cujo
`reinsert.py` grava bytes UTF-8 reais (`"coração"` grava 9 bytes, não os 7 de `"coracao"`) — o pipeline
promovia traduções que cabiam na métrica errada e estouravam no binário de verdade.

O projeto já carrega o veredito `connector.target_charset_supported` (Passo 4 de
`framework/skills/00_extraction.md`), mas até aqui ele só controlava o texto do prompt (instrução de
escrever com/sem acento) — nunca a métrica de contagem de bytes usada para decidir se uma tradução cabe.

## Decisão

`target_charset_supported is True` (checagem **estrita** de booleano — preserva compatibilidade com o
`"ascii_only"` não-booleano do bof4 e o `False` do uta) seleciona a métrica de orçamento em toda a fonte
única (`model.py::_budget_len`, usada por `_over_budget`/`_budget_note`/`_over_offsets`/
`over_budget_offsets`/`_api_translate`/`_ollama_translate`/`context_pack.render_prompt`):
- `True` → bytes UTF-8 reais (`len(t.encode("utf-8"))`).
- caso contrário → forma transliterada legada (`_translit_len`, NFKD sem combining marks).

Junto, paridade de retry por orçamento entre os dois backends **automatizáveis** (`api` e `ollama`) —
ambos chamam modelo real sem intervenção manual, ao contrário de `in-session` (humano+Claude no chat,
fora de escopo de automação nova). `run_scene.py`'s escalonamento de tolerância (`BUDGET_ESCALATION`) e o
retighten cirúrgico (`retranslate_offsets`) agora tratam `api`/`ollama` de forma idêntica — a escolha de
backend fica com o humano (`--backend`), sem que uma opção seja uma "armadilha" sem retry de orçamento.

## Consequências

- (+) `trails_sky_sc` (e qualquer conector futuro com `target_charset_supported: true`) para de estourar
  budget silenciosamente na reinserção — a métrica de decisão passa a espelhar o que `verify_chapter.py`
  realmente confere.
- (+) `bof4`/`utawarerumono` (charset não suportado) mantêm o comportamento anterior byte-a-byte (nenhuma
  regressão — coberto por `test_budget_len_charset_false_or_missing_uses_translit`).
- (+) `ollama` deixa de ser um backend "de segunda classe" no escalonamento de fitting — ganha o mesmo
  retry por orçamento que `api` já tinha (`test_ollama_translate_retries_over_budget`).
- (−) `target_charset_supported` vira um campo com **dois** efeitos (texto do prompt + métrica de
  contagem) — um veredito errado agora tem consequência maior. Mitigado exigindo o método mais confiável
  (inspeção de fonte/atlas ou teste in-game) antes de gravar `true`, e documentando em
  `framework/skills/00_extraction.md` que `likely`/`unknown` devem resolver para `false`.
