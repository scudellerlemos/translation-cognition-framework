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
**Se reprovada:** bloquear inclusão + registrar no `decision_log.md` (tipo `revision`) + marcar no `translation_status.json` com `needs_human_review`.

---

## REGRAS CRÍTICAS

- **Este passo é obrigatório.** Ir direto do passo 4 para o passo 6 sem o plano é o erro estrutural mais comum do processo.
- O `base_translation` no plano não é a tradução final — é o ponto de partida. O passo 6 pode melhorar, mas não deve contradizer a intenção documentada.
- Linhas com `risk_level: critical` devem passar pelo checklist de revisão humana acima antes de entrar no corpus final.
- O corpus de teste sintético deve cobrir **todos** os pares de identidade dupla (de `aliases_map.json`) antes de traduzir os segmentos reais dessas personas.
- O `translation_plan.json` deve incluir `total_lines` igual ao total de linhas no corpus-fonte. Um plano incompleto não é um contrato válido.
