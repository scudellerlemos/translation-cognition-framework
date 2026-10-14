# SKILL 05 — TRANSLATION PLANNING
## Planejar antes de traduzir

> **Quando usar:** Após o GLOSSARY CREATION, antes de qualquer execução de tradução. Este passo é **obrigatório** — não pular para o passo 6 sem o plano.

---

## OBJETIVO

Para cada linha do corpus, definir intenção, identificar entidades presentes, aplicar regras do glossário, esboçar uma tradução base, e marcar riscos. O plano é o contrato entre planejamento e execução — o passo 6 não inventa, executa o plano.

---

## INPUTS

- Corpus-fonte (`project.json → source.file`) — inclui o `byte_budget` por linha (do Passo 00)
- `glossary.csv`
- `translation_rules.md`
- `entities.csv`
- `aliases_map.json`
- `tone_analysis.md`

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

> Ver também `framework/skills/_pre_task.md` — decisões fechadas do projeto que antecedem este skill.

| Artefato | Critério |
|----------|---------|
| `glossary.csv` | Existe; verificação de cobertura do Passo 4 aprovada |
| `translation_rules.md` | Existe; seções obrigatórias aplicáveis presentes |
| `entities.csv` | Existe |
| `tone_analysis.md` | Existe; perfis de voz dos personagens principais documentados |
| Corpus-fonte | Existe; não-vazio |

❌ **Se qualquer verificação falhar: PARAR. O plano sem glossário ou regras completas é inútil como contrato.**

---

## OUTPUTS OBRIGATÓRIOS

### `translation_plan.json`

Estrutura por linha:

```json
{
  "offset": "[id_column da linha]",
  "text_en": "[texto no idioma-fonte]",
  "speaker": "[personagem / narrador / sistema]",
  "entities_present": [],
  "tone_register": "[registro esperado]",
  "intent": "[o que a linha faz narrativamente, 1 frase]",
  "risk_level": "low",
  "risk_notes": "",
  "base_translation": "[rascunho para o passo 6 partir]",
  "byte_budget": 0,
  "glossary_flags": [],
  "spoiler_flags": []
}
```

> O campo de ID usa o nome declarado em `project.json → source.id_column`. O campo de texto-fonte
> espelha `source.text_column`.

> **SHIFT-LEFT (`byte_budget`):** copiado do `dialogs.csv` (output do Passo 00). É o nº de bytes que
> a string ocupa no meio. O Passo 6 traduz **dentro** desse orçamento, evitando overflow na
> reinserção (Passo 08) — e portanto eliminando custo de LLM no patch-back. Para mídias sem
> restrição de bytes (ex: legendas), pode ser nulo ou substituído por limite de caracteres/CPS.

### Campos obrigatórios

| Campo | Descrição |
|-------|-----------|
| `offset` (ou `id_column`) | Identificador da linha no corpus original |
| `text_en` (ou `text_<source>`) | Texto no idioma-fonte |
| `speaker` | Personagem que fala (ou "narrador" / "sistema") |
| `entities_present` | Lista de entidades do glossário presentes na linha |
| `tone_register` | Registro de voz esperado para este falante neste contexto |
| `intent` | O que a linha faz narrativamente (1 frase) |
| `risk_level` | `low` / `medium` / `high` / `critical` |
| `risk_notes` | Descrição do risco se `risk_level` ≥ `medium` |
| `base_translation` | Rascunho de tradução para o passo 6 partir |
| `byte_budget` | Orçamento de bytes da string no meio (do Passo 00) — restrição dura no Passo 6 |
| `glossary_flags` | Termos do glossário presentes que exigem atenção |
| `spoiler_flags` | Aliases ou termos de spoiler presentes |

### Campos de controle (cabeçalho do arquivo)

| Campo | Descrição |
|-------|-----------|
| `total_lines` | Deve ser igual ao número de linhas no corpus-fonte |
| `critical_lines` | Contagem de linhas com `risk_level: critical` |
| `plan_version` | Data de criação "YYYY-MM-DD" |

### Como o plano nasce na implementação (conector `hex_binary`, ex.: bof4)

O plano é **por cena**, não um `translation_plan.json` único: `artifacts/scenes/<cena>/translation_plan_<sufixo>.json`
(`paths.translation_plan`). Quem o monta é o `build_plan_chapter.py <cena>` do conector (esqueleto em
`connectors/_skeleton/`), a partir do `dialogs.csv` da cena + o `translations_<sufixo>.json` que o tradutor devolve — cada
linha dele traz a tradução `t` **e** os metadados do plano (`speaker`, `tone_register`, `intent`, `risk_level`, `risk_notes`,
`glossary_flags`, `spoiler_flags`). Ou seja, o `base_translation` é a própria tradução da cena e o plano é o registro auditável
dela (`run_scene` o chama; ver `06_translation.md`). Diferenças em relação ao formato acima, verificadas no código:

- cabeçalho: `scene`, `scene_group`, `lines`, `total_lines`, `high_lines` (high+critical), `medium_lines`, `needs_review`
  (offsets), `plan_version` (`bof4-<sufixo>-v1` no bof4) — não há `critical_lines`;
- linha: `text_source` (não `text_en`), sem `entities_present`; `needs_human_review: true` quando o tradutor marcou;
  `risk_notes` obrigatório a partir de `medium`;
- `speaker` (bof4): o `speaker_code` determinístico do binário (`artifacts/state/portrait_codes.json`) tem precedência sobre o palpite
  do modelo;
- o build **falha** (exit 1) se faltar tradução de algum offset, sobrar offset, `risk_level` inválido (`low|medium|high|critical`),
  token estrutural divergente (esqueleto: `formatting_tokens`/`formatting_token_patterns` do `project.json`; bof4: só `[02]`) ou `risk_notes` ausente; também sincroniza o DB (`connector_io.sync_translations_db`) ou grava o
  `approved_<sufixo>.csv` (`offset,text_target`).

**Triagem de risco (passo 4.4a).** O tradutor marca pouco risco alto, e só `high`/`critical` passa pela retrotradução.
`python framework/runtime/risk_triage.py export <projeto> [--batch 400]` grava lotes (fala repetida entra uma vez) para um juiz
barato; `risk_triage_run.py <projeto> [--go] [--model haiku] [--jobs 6] [N ...]` orquestra o juiz — **sem `--go` só lista os
lotes; `--go` chama o modelo (pago)**; `risk_triage.py apply <projeto>` sobe para `high` as falas apontadas.

### Critérios de risk_level

| Nível | Quando usar |
|-------|-------------|
| `critical` | Linha contém alias de spoiler major/critical; qualquer erro aqui é irreparável |
| `high` | Cena de comédia com timing sensível; ou personagem com `voice_criticality: high` no `tone_analysis.md` |
| `medium` | Ambiguidade de registro ou entidade com regra especial |
| `low` | Narrativa/descritiva sem riscos identificados |

---

## CORPUS DE TESTE SINTÉTICO

Ver `05b_synthetic_test_corpus.md` para o protocolo completo. Em resumo: antes de traduzir
segmentos reais que envolvam pares de identidade dupla ou personagens de voz crítica, criar e
aprovar um conjunto de linhas sintéticas que testam esses pontos. O artefato é o
`synthetic_test_corpus.json`.

---

## REVISÃO HUMANA DE LINHAS CRÍTICAS

Linhas com `risk_level: critical` no plano **não entram no corpus final sem aprovação explícita**.

Checklist obrigatório para cada linha crítica:

| # | Verificação | Critério de aprovação |
|---|------------|----------------------|
| 1 | Identidade correta | A persona usada é a correta para este momento narrativo (não o alias de spoiler)? |
| 2 | Sem vazamento | Nenhuma informação do alias de spoiler vaza no tom, vocabulário ou phrasing? |
| 3 | Back-translation | Idioma-alvo → idioma-fonte preserva sentido e tom sem distorção? |
| 4 | Leitura sem spoiler | A linha funciona para um leitor que ainda não sabe o spoiler? |
| 5 | Registro no decision_log | A decisão está documentada com tipo, razão e impacto? |

**Aprovação:** todas as 5 verificações devem passar.
**Se reprovada:** bloquear inclusão + registrar no `decision_log.md` (tipo `revision`) + marcar a linha com `needs_human_review` (no plano da cena vira `needs_review` no cabeçalho; a fila humana é do `hitl.py`). `translation_status.json` não é gerado por nenhum script — o progresso real está em `artifacts/run_state.json`.

---

## REGRAS CRÍTICAS

- **Este passo é obrigatório.** Ir direto do passo 4 para o passo 6 sem o plano é o erro estrutural mais comum do processo.
- O `base_translation` no plano não é a tradução final — é o ponto de partida. O passo 6 pode melhorar, mas não deve contradizer a intenção documentada.
- Linhas com `risk_level: critical` devem passar pelo checklist de revisão humana acima antes de entrar no corpus final.
- O corpus de teste sintético deve cobrir **todos** os pares de identidade dupla (de `aliases_map.json`) antes de traduzir os segmentos reais dessas personas.
- O `translation_plan.json` deve incluir `total_lines` igual ao total de linhas no corpus-fonte. Um plano incompleto não é um contrato válido.
