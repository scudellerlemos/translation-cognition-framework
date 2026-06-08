# Validation leve (B1)

Validadores **executáveis** dos artefatos do pipeline — a contraparte de código dos schemas em prosa
(`framework/schemas/artifacts_schema.md`). Genéricos: descobrem tudo lendo o `project.json` da
instância; **não contêm dados de obra**.

## O que valida

`validate.py` → `validate_project(<dir>)` checa, para os artefatos que existirem:

- **`project.json`** — campos obrigatórios (title, idiomas, source, formatting_tokens).
- **`glossary.csv`** — `handling_rule` não-vazio e no enum; `target_translation` quando
  `traduzir`/`traduzir_parcial`; `spoiler_level` no enum.
- **`dialogs.csv`** — `id_column` único; `byte_budget` inteiro ≥ 0.
- **`approved_translations.csv`** — cada id casa com `dialogs.csv`; **tokens preservados** vs source.
- **`translation_plan.json`** — campos obrigatórios por linha; `risk_level` no enum; **`risk_notes`
  obrigatório quando `risk ≥ medium`**; `total_lines` e `critical_lines` coerentes.
- **`entities.csv`** — `canonical_name` único; enums de category/importance/confidence.
- **`aliases_map.json`** — campos obrigatórios; `reveal_timing` quando `spoiler_level ≠ none`.

Severidades: **ERROR** (viola schema/invariante → exit 1) e **WARN** (suspeita não-bloqueante).

## Uso

```
python framework/validation/validate.py projects/<título>     # relatório + exit code
pytest  framework/validation/                                 # gate de regressão (passa na ref + pega violações injetadas)
```

É um **Input Gate executável**: rodar antes de consumir os artefatos num passo do pipeline. Cresce
incrementalmente — novos invariantes viram novas checagens + testes.
