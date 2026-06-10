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

## Status do caminho API (COMPROVADO em produção — 2026-06)

Endurecido contra o SDK vivo `anthropic` 0.109.x e **rodado de verdade**. A 1ª rodada expôs 4 problemas
que só aparecem em produção (o motivo de "comprovar" ser uma etapa própria) — todos corrigidos:

| # | Achado empírico | Correção |
|---|---|---|
| 1 | structured output ESTRITO exige `additionalProperties:false` em todo objeto → mapa `{offset:{}}` (chaves dinâmicas) é rejeitado | schema virou **array de entradas** com `offset` por item; conversão array→mapa pós-parse (`_to_map`) |
| 2 | `effort:high` + adaptive thinking **estourou o custo ~5×** (thinking conta como saída a $15/M): 37 linhas → 20k tokens out | defaults **`EFFORT_TRANSLATE="low"` + `THINK_TRANSLATE=False`**; back-translation mantém thinking |
| 3 | em cena nova, o modelo colapsa o token `\n` numa **quebra de linha REAL** (3 retries não corrigem) | normalização **determinística** (`_norm_t`): newline real → token literal `\n` (este jogo só quebra via token) |
| 4 | o aviso de charset fazia o modelo **remover acentos** do `t` canônico | prompt clarificado: escreva `t` COM acentos; a transliteração ASCII é do `reinsert` |

### Veredito do benchmark — **Sonnet APROVADO** como `MODEL_TRANSLATE`
Teste limpo em cena de comédia fora da TM (ch_12_03, 408 linhas): registro/humor no nível da versão
feita à mão a Opus — ex.: *"Cérebro, meu camarada, você tá arrasando hoje."*, escalada cômica
*"Rejeito, renuncio, RECUSO esse 'trabalho'..."*. Em cena coberta por TM (ch_12_01): 37/37 `t`
**idêntico** ao gold (reuso de TM perfeito). Cobertura 100%, 0 quebras reais residuais. **Mantém
Sonnet**; Opus reservado à back-translation.

### Custo real medido (Sonnet, effort:low, sem thinking)
| cena | linhas | out tok | tempo | ~custo |
|---|---|---|---|---|
| ch_12_01 (TM) | 37 | 2.529 | 43s | ~$0.06 |
| ch_12_03 (nova) | 408 | 27.000 | 432s | ~$0.45 |
~**66 tok/linha** (bate o `cost_model`) → **~$1.1/1k linhas → jogo ~$36** (antes do bundle de custo R5).
Compare: com effort:high+thinking seria ~5× (jogo ~$285). Ver `OBSERVABILITY.md`.

## Por que isto viabiliza Sonnet

Sonnet não precisava de mais "inteligência" — precisava de **contexto pequeno e certo**. Com o
`context_pack` entregando só o relevante e a doutrina cacheada, a tradução por linha cabe em Sonnet;
Opus fica reservado à verificação de alto risco. Ver `adr/0004-model-agnostic-interface.md`.
