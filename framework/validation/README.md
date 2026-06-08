# Validação executável

Camada de **gates executáveis** do pipeline — a contraparte de código dos schemas/regras em prosa.
Genéricos: descobrem tudo lendo o `project.json` da instância; **não contêm dados de obra**.

- **`validate.py`** — schemas + invariantes estruturais (B1).
- **`naturalness_lint.py`** — smells de naturalidade/tradução (apoio à Carta de Governança).

---

## `validate.py` — Validation leve (B1)

Validadores **executáveis** dos artefatos do pipeline — a contraparte de código dos schemas em prosa
(`framework/schemas/artifacts_schema.md`).

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

Severidades: **ERROR** (viola schema/invariante → exit 1) e **WARN**. É um **Input Gate executável**:
rodar antes de consumir os artefatos. Cresce incrementalmente (novos invariantes → novas checagens + testes).

---

## `naturalness_lint.py` — Linter de naturalidade

Heurístico, complementa a **Carta de Governança** (`framework/skills/translation_governance.md`).
Sinaliza **candidatos** para revisão (06c) — não auto-fix. Checagens de alta precisão:

- **`copia_crua`** — alvo idêntico ao source, fora da whitelist (nomes do glossário `manter_original`
  por conteúdo alfabético; gritos puros tipo `Aaaah!`/`Aaagh--`; linhas só de número/token).
- **`fragmento_residual`** — hesitação de 1 letra + reticências idêntica nos dois lados (ex.: `U...` em
  `U... Argh...`), com o resto traduzido. Ignora palavras curtas reais (`a short` → `a pouca`).
- **`rotulo_cru`** — rótulo de falante (alias/UI) idêntico ao source.

Saída: imprime os achados + grava `<projeto>/artifacts/naturalness_lint.json` (`offset`, `check`,
`source`, `target`, `note`) — input do 06c.

## Uso

```
python framework/validation/validate.py         projects/<título>   # schemas/invariantes (exit code)
python framework/validation/naturalness_lint.py projects/<título>   # smells -> naturalness_lint.json
pytest  framework/validation/                                        # gate (passa na ref + pega violações injetadas)
```
