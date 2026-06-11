# framework/runtime — harness de execução (orquestração determinística + interface de modelo)

Torna **cada cena um job stateless e limitado**: o contexto por execução é O(cena), não O(histórico).
É a camada que tira a orquestração e a memória da janela da LLM. Ver `framework/docs/ARCHITECTURE.md`.

## Módulos

| Arquivo | Tipo | Função |
|---|---|---|
| `state_index.py` | determinístico | Materializa o estado externo: `translation_memory.jsonl`, `voice_cards.json`, `decision_index.json`. Idempotente, reconstruível. |
| `context_pack.py` | determinístico | Monta o pacote LIMITADO de 1 cena → `scene_prompt.md` + `pack.json`. A peça central. |
| `model.py` | interface (única parte de IA) | `translate` / `back_translate` / `batch_*`; backends `in-session` (assinatura) e `api` (model-mix). |
| `run_scene.py` | orquestrador (det.) | Encadeia pack → translate → build_plan → back-translate → verify → checkpoint. Resumível. |
| `run_chapter.py` | driver (det.) | Loop de cenas de um capítulo via `run_scene`; modo `--batch` (−50%); resumível. |
| `kb_gate.py` | gate (det.) | Cobertura de KB por cena (research reconciliada + `kb_frontier`) ANTES de traduzir. |
| `kb_phase.py` | driver de Fase 0 (det.) | Descobre o gap de KB de um capítulo (cobrança) e valida/avança a fronteira. |
| `cost_report.py` | observabilidade (det.) | Agrega `api_ledger.jsonl` (custo real por modelo/tipo/cena; gasto desperdiçado). |
| `test_runtime.py` | pytest | Determinismo, boundedness, idempotência, guard de no-work-text. |

> Convenção de nomes (identificadores em inglês, glossário de abreviações aceitas — KB/TM/scene_id… — e o
> **contrato congelado** de nomes de artefato/CLI/`project.json`): ver [`../docs/NAMING.md`](../docs/NAMING.md).

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
