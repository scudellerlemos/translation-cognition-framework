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
- Adaptive thinking; saída estruturada por schema (ver nota de endurecimento P1).

## Matriz de modelos (defaults; ver skill `claude-api`)

| Papel | Modelo default | Constante | Razão |
|---|---|---|---|
| Tradução | `claude-sonnet-4-6` | `MODEL_TRANSLATE` | barato, suficiente com contexto curado |
| Back-translation | `claude-opus-4-8` | `MODEL_BACK` | raciocínio p/ ambiguidade/duplo-sentido |
| (linhas low mecânicas) | `claude-haiku-4-5` | — | opção futura p/ lotes triviais |

Trocar de modelo = trocar a string. Nenhuma outra parte do harness sabe qual modelo rodou.

## Endurecimento P1 (não bloqueia o caminho assinatura)

O caminho `api` está implementado fielmente ao skill `claude-api`, mas **não roda sob o congelamento**
atual. Antes de produção via API (P1):
- validar a forma de saída estruturada contra o SDK vivo (`client.messages.parse()` é o recomendado;
  o código atual usa `output_config.format` + parse de texto como fallback);
- bater o custo real contra `validation/cost_model.py` (cenário `mix_cache`);
- afinar `max_tokens`/`effort` por tamanho de cena.

## Por que isto viabiliza Sonnet

Sonnet não precisava de mais "inteligência" — precisava de **contexto pequeno e certo**. Com o
`context_pack` entregando só o relevante e a doutrina cacheada, a tradução por linha cabe em Sonnet;
Opus fica reservado à verificação de alto risco. Ver `adr/0004-model-agnostic-interface.md`.
