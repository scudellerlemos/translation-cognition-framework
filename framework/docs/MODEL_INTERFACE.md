# Model Interface — agnosticismo de modelo

`framework/runtime/model.py` é a **única** fronteira não-determinística do harness. Isola "como a IA é
chamada" do "o que o pipeline faz", para que o mesmo `run_scene` rode com qualquer modelo/caminho.

## Contrato

```
translate(root, scene, *, backend, model)        -> {status, path|prompt, sfx, n_lines}
back_translate(root, scene, high_lines, *, backend, model) -> {status, path|prompt, reviewed}
```

Dois papéis de IA, e **apenas** estes:
- **translate** — traduz a cena a partir do pacote limitado (`context_pack`).
- **back_translate** — verifica linhas `risk >= high` (pt-BR → EN → confere sentido/voz/ambiguidade).

## Dois backends, mesmo contrato

### (a) `in-session` — caminho ASSINATURA (default)
Não chama rede. Garante o `scene_prompt.md` (auto-contido e **limitado**) e checa se o modelo do chat
já produziu `translations_<sfx>.json`:
- ausente → `status: awaiting` (o operador responde o prompt numa **sessão limpa**; como o prompt é
  pequeno, o contexto nunca acumula → sem estouro, sem conta de API).
- presente → `status: ready` (segue para as gates determinísticas).

Resumível: rode `run_scene` de novo após o arquivo aparecer; o checkpoint diz onde retomar.

### (b) `api` — caminho ESCALA HEADLESS
Anthropic SDK (import preguiçoso; erro claro se faltar `anthropic`/`ANTHROPIC_API_KEY`):
- **Doutrina (Carta) no `system` com `cache_control`** → cobrada ~1× via prompt-caching, não a cada cena.
- **Model-mix** (cenário `mix` do `cost_model.py`): tradução em **Sonnet**, back-translation em **Opus**.
- **Streaming** (`messages.stream` + `get_final_message`) p/ saídas longas; `output_config` com
  `json_schema` + `effort: high`; adaptive thinking.
- **`max_tokens = 64000`** (cobre a maior cena do corpus; o valor antigo de 16k truncava cenas grandes).
- **Guard do token de quebra + cobertura** com retry corretivo (até 3 tentativas): se o modelo emitir
  quebra de linha REAL no campo `t` (em vez do literal `\n`) ou faltar offsets, regenera — mata o bug
  recorrente *na borda da API*, antes de gravar.
- **Backoff** exponencial em 429/500/timeout; falha de tradução vira checkpoint `api_translate_failed`
  em `run_scene` (retomável).

**Como ligar:** `pip install anthropic` + `ANTHROPIC_API_KEY` no ambiente **ou** num `.env` na raiz do
framework (carregado por `model._load_dotenv`; `.env` está no `.gitignore`, ver `.env.example`).
Driver de capítulo: `run_chapter.py <projeto> <cap> --backend api` (loop de cenas fora do chat,
resumível, para na 1ª falha). Métricas por cena em `artifacts/metrics.jsonl` (ver `OBSERVABILITY.md`).
Benchmark de modelo: `bench_translate.py` grava saída paralela `translations_<sfx>.<tag>.json` sem
tocar nas aprovadas.

## Matriz de modelos (defaults; ver skill `claude-api`)

| Papel | Modelo default | Constante | Razão |
|---|---|---|---|
| Tradução | `claude-sonnet-4-6` | `MODEL_TRANSLATE` | barato, suficiente com contexto curado |
| Back-translation | `claude-opus-4-8` | `MODEL_BACK` | raciocínio p/ ambiguidade/duplo-sentido |
| (linhas low mecânicas) | `claude-haiku-4-5` | — | opção futura p/ lotes triviais |

Trocar de modelo = trocar a string. Nenhuma outra parte do harness sabe qual modelo rodou.

## Status do caminho API (endurecido — pronto p/ produção)

Endurecido contra o SDK vivo `anthropic` 0.109.x (streaming, `output_config` json_schema, backoff,
guard de `\n`/cobertura). Pendências de validação **em produção real** (requerem a chave):
- **Benchmark Sonnet×Opus** nas cenas-gold (ch_12_01/02, feitas à mão a Opus) — veredito do modelo de
  tradução default. _(pendente da chave; rodar `bench_translate.py … --model claude-sonnet-4-6`)._
- Bater o custo real (`metrics.jsonl`) contra `validation/cost_model.py` (cenário `mix`/`mix_cache`).

### Veredito do benchmark
_(a preencher após a primeira rodada via API: Sonnet preserva voz/registro cômico? passa
`build_plan_chapter` + `naturalness_lint`? Se não, `MODEL_TRANSLATE` → `claude-opus-4-8`.)_

## Por que isto viabiliza Sonnet

Sonnet não precisava de mais "inteligência" — precisava de **contexto pequeno e certo**. Com o
`context_pack` entregando só o relevante e a doutrina cacheada, a tradução por linha cabe em Sonnet;
Opus fica reservado à verificação de alto risco. Ver `adr/0004-model-agnostic-interface.md`.
