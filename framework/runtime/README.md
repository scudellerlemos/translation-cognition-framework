# framework/runtime — harness de execução (orquestração determinística + interface de modelo)

Torna **cada cena um job stateless e limitado**: o contexto por execução é O(cena), não O(histórico).
É a camada que tira a orquestração e a memória da janela da LLM. Ver `framework/docs/ARCHITECTURE.md`.

## Módulos

| Arquivo | Tipo | Função |
|---|---|---|
| `state_index.py` | determinístico | Materializa o estado externo: `translation_memory.jsonl`, `voice_cards.json`, `decision_index.json`. Idempotente, reconstruível. |
| `context_pack.py` | determinístico | Monta o pacote LIMITADO de 1 cena → `scene_prompt.md` + `pack.json`. A peça central. |
| `model.py` | interface (única parte de IA) | `translate` / `back_translate`; backends `in-session` (assinatura) e `api` (model-mix). |
| `run_scene.py` | orquestrador (det.) | Encadeia pack → translate → build_plan → back-translate → verify → checkpoint. Resumível. |
| `test_runtime.py` | pytest | Determinismo, boundedness, idempotência, guard de no-work-text. |

## Uso

```bash
# 1) materializa o estado consultável (idempotente)
python framework/runtime/state_index.py projects/<projeto> --rebuild

# 2) monta o contexto limitado de uma cena (determinístico)
python framework/runtime/context_pack.py projects/<projeto> <cena>

# 3) roda a cena ponta-a-ponta (assinatura: para em 'awaiting' se faltar tradução)
python framework/runtime/run_scene.py projects/<projeto> <cena> [--backend in-session|api] [--require-back] [--no-verify]
```

`<cena>` = subdir em `artifacts/` (ex.: `ch_12_01`). Genérico: nenhum dado de obra aqui; tudo vem de
`project.json` + artefatos. Sem rede no caminho `in-session`. Sem work-text nos `.py` (travado por teste).
