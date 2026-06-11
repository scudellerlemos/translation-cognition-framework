# Observability — métricas do harness

Estado: **especificação (P1)**. O `run_scene` já é o ponto natural de instrumentação; este doc define
o que coletar e onde, para validar o diagnóstico (custo está na tradução ou na governança?) com número.

## Onde instrumentar

`framework/runtime/run_scene.py`, emitindo `artifacts/metrics.jsonl` (1 linha por cena). A chamada de
IA passa por `model.py` — é lá que tokens in/out são conhecidos (backend `api`) ou estimados
(backend `in-session`, via `cost_model._toks`).

## Métricas por cena (consumo)

| Métrica | Como | Uso |
|---|---|---|
| tokens_in / tokens_out | resposta da API (`usage`) ou estimativa `cost_model` | custo |
| **segmentação**: tradução / governança / revisão | por etapa ([2] vs [3-5] vs [4]) | responde "tradução vs governança" |
| custo_cena / custo_capítulo | tokens × pricing (`cost_model.PRICE`) | $/1k linhas real |
| cache_hits (doutrina) | `usage.cache_read_input_tokens` | prova o ganho do caching |

A proporção a mirar é **tradução : governança ≈ 70:30 ou melhor** (governança é a doutrina cacheada
~4K tok + as gates determinísticas, que custam ~0 em tokens de IA).

## Métricas por cena (qualidade)

| Métrica | Fonte | Uso |
|---|---|---|
| cobertura | build_plan (linhas traduzidas / total) | completude |
| preservação de tokens/tags | `validate.py` | regressão de formatação |
| consistência terminológica | TM/glossário hits vs divergências no pack | drift de termo |
| **taxa de retrabalho** | linhas reprovadas no QA / total | qualidade do 1º passe |
| back-translation pass-rate | `back_translation_<scene_id>.json` (pass/revise) | risco real pego |
| resíduo T4 | `verify_chapter` | overflow não resolvido (deve ser 0) |

## Sinais de saúde da arquitetura (o que validar)

- **Contexto por execução constante** (não cresce com o nº de capítulos) — medir tokens_in do pack por
  cena ao longo do jogo; a curva deve ser plana, não crescente. É a prova de que o estouro morreu.
- **Reprodutibilidade** — qualquer cena reexecutável a partir dos artefatos sem o chat.
- **Custo previsível** — `$/1k linhas` medido bate (ordem de grandeza) com `cost_model` cenário `mix_cache`.

## Benchmark de modelos (P1)

Suite fixa de cenas-gold (com tradução de referência aprovada). Para cada modelo (Opus 4.8 / Sonnet 4.6
/ Haiku 4.5) rodar o mesmo `context_pack` e comparar: back-translation pass-rate (fidelidade),
naturalness_lint hits (naturalidade), preservação de tokens, taxa de retrabalho, custo/1k. Saída:
`artifacts/model_benchmark.md`. Decide o default por papel (tradução vs back-translation).
