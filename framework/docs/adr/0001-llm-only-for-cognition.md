# ADR 0001 — A LLM é responsável apenas pela cognição (traduzir + verificar alto risco)

**Status:** aceito · **Data:** 2026-06-10

## Contexto

O framework usava a LLM, na prática, como compute + orquestrador + memória ao mesmo tempo. Revisão do
código real mostrou que conector e validadores **já** eram determinísticos; o que sobrava na LLM além
da tradução era acidental (orquestração no chat, memória de consistência na janela).

## Decisão

A LLM executa **só** dois papéis: **traduzir** e **back-translation de alto risco**. Tudo o mais
(parser, reinserção, controle de fluxo, montagem de contexto, memória, checkpoint, validação, métricas)
é código determinístico. A fronteira de IA fica isolada em `framework/runtime/model.py`.

## Consequências

- (+) Reprodutibilidade: tudo exceto a tradução é determinístico e testável.
- (+) Custo previsível: a IA só é chamada onde agrega; governança custa ~0 token (gates determinísticos).
- (+) Agnosticismo de modelo: trocar o modelo não afeta o resto do sistema.
- (−) Exige disciplina: qualquer "deixa a IA decidir o fluxo" é dívida — deve virar código.
