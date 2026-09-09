# ADR 0015 — Embedder isolado por processo, sem daemon compartilhado entre projetos

**Status:** aceito · **Data:** 2026-09-08

## Contexto

Issue [#173](https://github.com/scudellerlemos/translation-cognition-framework/issues/173), aberta na
esteira do #109: `framework/db/embedder.py` carrega `sentence-transformers` (~470 MB de modelo,
stack ~700 MB–1,5 GB com torch) via `python embedder.py <db> <project_id>`, um processo por projeto.
A pergunta era se, quando **mais de 1 projeto** rodar RAG semântico ao mesmo tempo, vale a pena um
processo compartilhado carregando o modelo 1× pra indexar N projetos, versus manter isolado por
processo (custo de recarregar, mas simples).

Levantamento do estado real antes de decidir:

- **Hoje só 1 projeto tem RAG ligado**: `translation_software` (SQLite + `sqlite-vec`, 6.046 vetores
  indexados). Os outros quatro (`utawarerumono`, `breath_of_fire_4`, `souldiers`, `trails_sky_sc`)
  seguem em flat files — RAG nem se aplica (ver `STACK.md`, tabela "Onde cada projeto está hoje").
  **N projetos rodando RAG simultaneamente é cenário hipotético, não observado.**
- **Multi-projeto/paralelismo já é low-priority reconhecido**: `ROADMAP.md` P2.5 lista "multi-projeto:
  generalizar `state_index`/paths por projeto" como ❌, empurrado explicitamente pra P4 (plataforma,
  vários jogos) via [issue #104](https://github.com/scudellerlemos/translation-cognition-framework/issues/104).
  Não existe hoje nenhum orquestrador que rode 2 projetos no mesmo processo — construir um servidor de
  embedding compartilhado adiantaria uma peça de infra pra um orquestrador que ainda nem existe.
- **O recarregamento repetido dentro de 1 execução já não acontece**: `context_pack.py::_get_embedder()`
  memoiza `Embedder()` num global de módulo (`_EMBEDDER`) — o modelo carrega 1× por processo, não 1×
  por chamada. O custo de reload só existe **entre** invocações de processo (`db index` por projeto),
  não dentro de uma.
- **O cache de download (~470 MB) já é compartilhado, sem código nenhum**: `SentenceTransformer(model_name)`
  em `embedder.py:82` não passa `cache_dir` — cai no default do Hugging Face Hub
  (`~/.cache/huggingface/hub` ou `%USERPROFILE%\.cache\huggingface\hub` no Windows), que é por-máquina,
  não por-projeto. N projetos na mesma máquina já baixam o modelo 1× hoje.

## Decisão

**Manter isolado por projeto/processo — não construir processo/daemon compartilhado.** A segunda
metade da pergunta (cache de download) já está resolvida a favor de "compartilhado" pelo comportamento
default do Hugging Face Hub, sem precisar de decisão nem código.

Razão: nenhum dos dois pré-requisitos que justificariam um daemon existe ainda —
(a) mais de um projeto com RAG ativo ao mesmo tempo, e (b) um orquestrador que efetivamente dispare N
projetos no mesmo processo. Construir um servidor de embedding compartilhado agora seria infra pra um
cenário não observado, adiantando uma peça de um problema (#104, multi-projeto) que o próprio roadmap
já decidiu adiar pra P4.

## Consequências

- (+) Zero código novo. `embedder.py` continua um processo simples por invocação, sem IPC, fila, nem
  gestão de ciclo de vida de um daemon.
- (+) O cache de peso do modelo já é compartilhado (default do HF Hub) — nenhum download duplicado
  entre projetos na mesma máquina, sem esforço.
- (+) Sem contenção de memória de GPU entre projetos concorrentes pra debugar — cada processo é dono
  exclusivo do que aloca.
- (−) Se dois projetos indexarem ao mesmo tempo (hoje: manual, dois terminais), cada um paga o custo de
  carregar o modelo (segundos a ~1 min em CPU) — aceito, é custo one-time por processo, não por linha
  indexada.
- Fora de escopo: reavaliar quando existir orquestrador multi-projeto real (#104) **e** medição mostrar
  que o reload por processo é gargalo — nesse ponto, considerar processo compartilhado como parte do
  design do orquestrador, não isolado.

**Reabrir se:** #104 (orquestração multi-projeto) sair de "não planejado" E houver medição real de N
projetos rodando RAG ao mesmo tempo com custo de reload de modelo dominando o tempo total.
