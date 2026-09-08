# ADR 0008 — Tier Ollama local para tradução: descontinuado

**Status:** aceito · **Data:** 2026-08-30

## Contexto

Uma auditoria de redução de custo (fork subagent, 2026-08-30) listou "tier Ollama local para tradução
barata" como estratégia de maior impacto ainda não explorada: `framework/runtime/ollama_client.py` +
`model.py::_ollama_translate` + `bench_local.py` já existem como caminho opt-in (`--backend ollama`),
nunca adotado como padrão nem roteado automaticamente por `risk_level` — só uma ferramenta de bench
pronta, parada. Faltava validar se valia a pena ativá-lo antes de investir em roteamento automático.

Validação feita nesta sessão, com dados reais (zero custo de API):
- **Integração:** `ollama serve` local respondendo, `qwen2.5:14b` carregado, pipeline
  extract→split_scenes→context_pack→`_ollama_translate` rodou fim-a-fim sem erro/timeout/truncamento.
- **Velocidade:** medido **2,2–3,5 tok/s** (2 amostras, modelo já aquecido, offload 57% GPU / 43% CPU
  confirmado via `ollama ps` — mesma config de hardware do ADR 0005). O próprio `ollama_client.py`
  documentava ~6,2 tok/s (medido 2026-08-24) e a expectativa original era ~10–15 tok/s. Regressão de
  2–4x não investigada (driver, throttling térmico, carga concorrente — causa não identificada).
- **Qualidade:** só havia baseline aprovado real disponível em `trails_sky_sc/manual_tests/`
  (4 linhas, aprovadas por humano). Amostra pequena demais pra veredito estatístico, mas já mostrou
  1 escolha de terminologia ruim: `"Airliner Linde"` → Ollama produziu `"Aeroliner Linde"` (não é
  palavra real em português) onde o baseline aprovado usa `"dirigível Linde"` (termo correto).

## Decisão

**NÃO adotar** o tier Ollama como caminho de tradução em produção — nem como padrão, nem como
rota automática por `risk_level` baixo. Nota inicial desta ADR (2026-08-30, mesma data) previa manter
o código intocado como ferramenta de reavaliação futura; ao escopar essa manutenção, descobriu-se que
existia um sub-projeto inteiro (`projects/translation_local/`, Fase 1 MVP) dedicado exatamente a esse
tier, não só um caminho opt-in isolado — o que mudou o cálculo de custo de manutenção de zero para
não-zero (projeto com README/roadmap/dívidas técnicas próprios a manter coerente). Decisão final,
mesmo dia: **remover o código do backend** do framework e marcar `translation_local` como
descontinuado, em vez de deixá-lo dormente.

Removido: `model.py::_ollama_translate` e os dois despachos `backend == "ollama"` (`translate()` e
`retranslate_offsets()`), `bench_local.py` (deletado), a opção `"ollama"` de `--backend` em
`run_scene.py`/`framework/cli.py`/`framework/skills/s06_translation.py`, e os testes específicos do
backend em `test_model.py`/`test_run_scene.py`. `projects/translation_local/README.md` marcado
DESCONTINUADO.

**Mantido intocado:** `framework/runtime/ollama_client.py` (client HTTP genérico) e
`framework/cli.py`'s `ollama status`/`ollama pull` (gerência de serviço) — dependências ativas de
`kb_build_ollama.py`, feature de extração de KB não relacionada a esta descontinuação.

## Consequências

- (+) Elimina um caminho de código (`--backend ollama`) que media 2–4x mais lento que o documentado e
  já mostrou 1 erro real de terminologia — não sobra tentação de reativá-lo por atalho.
- (+) `projects/translation_local/` para de exigir manutenção de roadmap/dívidas técnicas por um tier
  que não vinga; menos superfície pra manter coerente no repo.
- (+) `ollama_client.py` continua servindo `kb_build_ollama.py` (feature ativa, ver ROADMAP.md) —
  nenhuma regressão na extração de KB.
- (−) Redução de custo do tier Ollama (custo $0 de API) sai do roadmap; a economia real hoje vem só de
  batch mode (ver `run_chapter.py` "BATCH POR DEFAULT").
- (−) Reabrir essa via no futuro exige reescrever `_ollama_translate`/`bench_local.py` do zero (não é
  só "descomentar") — aceito porque o código morto tem custo de manutenção maior que o de reescrever
  se a decisão realmente reverter.

**Reabrir se:** (a) a causa da regressão de velocidade for identificada e corrigida (voltando a
~10–15 tok/s), ou (b) surgir necessidade real de tradução 100% offline/sem custo que justifique
investir em validação de qualidade com amostra maior (baseline pago de pelo menos 1 cena completa) —
nesse caso, reabrir como projeto novo, não recuperar `translation_local`.
