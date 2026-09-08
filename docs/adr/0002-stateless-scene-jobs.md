# ADR 0002 — Cena = job stateless e limitado (o chat deixa de ser runtime/memória)

**Status:** aceito · **Data:** 2026-06-10

## Contexto

O estouro de sessão acontecia porque a tradução era feita inline, turno-a-turno, numa única sessão de
vida-longa que atravessava 9+ capítulos e recarregava artefatos anteriores (decision_log ~30KB, planos
de capítulos ~250KB) "por consistência". Contexto crescia **linearmente** com o nº de capítulos. O
gargalo era o **modo de execução**, não a tradução nem a governança (esta ≈ 4K tokens cacheáveis).

## Decisão

A unidade de trabalho é a **cena**, executada como job determinístico e resumível por
`framework/runtime/run_scene.py`. O contexto de cada execução é montado por `context_pack` e é **O(cena)**,
não O(histórico): só glossário-subset + voice cards dos falantes + decisões relevantes + hits de TM +
as linhas da cena. O estado vive em arquivos (`run_state.json`, `artifacts/state/`), não na janela.

## Consequências

- (+) Contexto por execução constante → estouro de sessão eliminado.
- (+) Resumível: crash/parada entre cenas não perde nada; retoma pelo checkpoint.
- (+) Caminho assinatura: uma cena por sessão limpa (`/clear` entre cenas) — sem conta de API.
- (+) Paralelizável no futuro (cenas são jobs independentes).
- (−) Consistência precisa ser **materializada** (TM/voice cards/decision_index) em vez de "lembrada".
