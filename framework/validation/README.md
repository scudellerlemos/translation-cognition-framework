# Validação executável

Camada de **gates executáveis** do pipeline — a contraparte de código dos schemas/regras em prosa.
Genéricos: descobrem tudo lendo o `project.json` da instância; **não contêm dados de obra**.

- **`validate.py`** — schemas + invariantes estruturais.
- **`naturalness_lint.py`** — smells de naturalidade/tradução (apoio à Carta de Governança).
- **`cost_model.py`** — custo de produção via API em 3 cenários (`python cost_model.py <projeto> [--report]` grava `artifacts/cost_report.md`); tokens estimados (~chars/3,8), ordem de grandeza.

---

## `validate.py`

Validadores **executáveis** dos artefatos do pipeline — a contraparte de código dos schemas em prosa
(`framework/schemas/artifacts_schema.md`).

## O que valida

`validate.py` → `validate_project(<dir>)` checa, para os artefatos que existirem:

- **`project.json`** — campos obrigatórios (title, source_language, target_language, source, formatting_tokens); `formatting_tokens`/`formatting_token_patterns` válidos (regra única de `connector_io`).
- **`glossary.csv`** — `handling_rule` não-vazio e no enum; `target_translation` quando
  `traduzir`/`traduzir_parcial`; `spoiler_level` no enum (WARN).
- **`dialogs.csv`** — `id_column` único; `byte_budget` inteiro ≥ 0 (coluna de texto: `text_source`, ou `source.text_column` em projetos antigos).
- **`approved_translations.csv`** (flat) e **`scenes/<cena>/approved_*.csv`** (layout por cena, o dos projetos atuais, contra o `dialogs.csv` da cena) — cada id casa com o source; **tokens preservados** vs source (literais por contagem; padrões parametrizados por multiset verbatim); nº de `
` divergente é WARN.
- **`scenes/<cena>/translation_plan_*.json`** (plano por cena, o de produção) — campos obrigatórios por linha (`offset`, `text_source`, `speaker`, `risk_level`, `base_translation`); `risk_level` no enum; **`risk_notes`
  obrigatório quando `risk ≥ medium`**; `total_lines` coerente. O `translation_plan.json` global (legado do poc) ainda é aceito e exige também `entities_present`, `tone_register`, `intent`, `glossary_flags`, `spoiler_flags` e `critical_lines` coerente.
- **`entities.csv`** — `canonical_name` único; enums de category/importance/confidence.
- **`aliases_map.json`** — campos obrigatórios; `reveal_timing` quando `spoiler_level ≠ none`.

Severidades: **ERROR** (viola schema/invariante → exit 1) e **WARN**. É um **Input Gate executável**:
rodar antes de consumir os artefatos. Cresce incrementalmente (novos invariantes → novas checagens + testes).

---

## `naturalness_lint.py` — Linter de naturalidade

Heurístico, complementa a **Carta de Governança** (`framework/skills/translation_governance.md`).
Sinaliza **candidatos** para revisão (06b) — não auto-fix. Checagens de alta precisão:

- **`copia_crua`** — alvo idêntico ao source, fora da whitelist (nomes do glossário `manter_original`
  por conteúdo alfabético; gritos puros tipo `Aaaah!`/`Aaagh--`; linhas só de número/token).
- **`fragmento_residual`** — hesitação de 1 letra + reticências idêntica nos dois lados (ex.: `U...` em
  `U... Argh...`), com o resto traduzido. Ignora palavras curtas reais (`a short` → `a pouca`).
- **`rotulo_cru`** — rótulo de falante (alias/UI) idêntico ao source.

Entrada: planos por cena (ou `translation_plan.json`), senão `dialogs.csv` + `approved_translations.csv`; whitelist do `glossary.csv`/`aliases_map.json`. O lint de 1 letra respeita iniciais legítimas em pt-BR (`a`, `e`, `o`, `é`).

Saída: imprime os achados + grava `<projeto>/artifacts/naturalness_lint.json` (`offset`, `check`, `speaker`,
`source`, `target`, `note`) — input do 06b.

## Uso

```
python framework/validation/validate.py         projects/<título>   # schemas/invariantes (exit code)
python framework/validation/naturalness_lint.py projects/<título>   # smells -> naturalness_lint.json
pytest  framework/validation/                                        # gate (passa na ref + pega violações injetadas)
```
