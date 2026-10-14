# SKILL 06b — MICRO-QA E CICLO DE CORREÇÃO
## QA por lote e correção cirúrgica do que ele reprova

> **Quando usar:** Automaticamente após cada lote traduzido no passo 6. Antes de prosseguir para o próximo lote. A Parte 2 roda quando o micro-QA reprova ou o passo 07 gera `fix_suggestions.json`.

---

## OBJETIVO

Detectar drift de tom, erros de entidade e quebras de registro enquanto o corpus ainda é pequeno o suficiente para corrigir sem custo alto. O micro-QA não substitui o QA final do passo 7 — ele previne que problemas se acumulem.

> **Referência normativa:** este QA verifica o cumprimento da **Carta de Governança**
> (`translation_governance.md`) — voz, lore, situação e o checklist por linha/lote. Apoio executável:
> `framework/validation/naturalness_lint.py` (smells de naturalidade) roda antes da revisão contextual.

---

## INPUTS

- O lote recém-proposto (plano da cena `translation_plan_<cena>.json → base_translation`, consolidado em `approved_<cena>.csv`) confrontado com o `dialogs.csv` (source)
- `project.json` (tokens, convenção de sistema)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`
- plano da cena (para comparar `base_translation` com o resultado final)

---

## VERIFICAÇÕES OBRIGATÓRIAS

### 1. Verificação de tom por personagem
Para cada personagem com ≥ 3 linhas no lote:
- Ler as linhas em sequência
- Verificar se o registro está consistente com o perfil do `tone_analysis.md`
- Sinalizar qualquer linha que soe "fora de voz"

**Sinais de alerta:** cada personagem tem seus próprios red flags definidos no perfil de voz
(`tone_analysis.md`). Verificar cada linha contra os red flags do falante. Não há lista hardcoded —
a fonte de verdade é o perfil de voz do projeto.

> Para pares de identidade dupla, atenção especial ao **vazamento de voz**: a persona pública não
> pode exibir traços da identidade revelada (ver `aliases_map.json` e o perfil de pares do projeto).

### 2. Verificação de entidades
Para cada termo do `glossary.csv` presente no lote:
- `handling_rule: manter_original` → termo não foi traduzido
- `handling_rule: traduzir` → termo usa exatamente a `target_translation`
- Nomes de personagens na forma canônica

### 3. Verificação de tokens
- Contar tokens (`project.json → formatting_tokens`) e quebras de linha no original e na tradução de cada linha
- Sinalizar qualquer linha onde a contagem não bate

### 4. Verificação de spoilers
Se o lote contém alguma linha com `spoiler_flags` no plano:
- Verificar que aliases de spoiler não foram usados antes do reveal
- Verificar que os dois nomes de um par de identidade dupla não aparecem no mesmo segmento

### 5. Verificação de naturalidade CONTEXTUAL (não-amostral)
Ler as falas **agrupadas por personagem × situação dramática** (não linha isolada): pegar a sequência
de falas do personagem naquele momento da história e perguntar, sobre o conjunto:
- **"Isso lê natural no idioma-alvo? Uma pessoa entende com facilidade?"** Se não → revisar.
- A fala soa como falante nativo *naquela situação*, ou como tradução literal?
- Há calques do idioma-fonte? Pontuação/reticências corretas?

### 5b. Localização de interjeições (OBRIGATÓRIO — não amostral)
Interjeições/onomatopeias/exclamações de emoção (susto, dor, surpresa, esforço, riso, choro) **não
podem ser cópia do source.** Verificar **todas** as linhas curtas / `tone_register: interjeicao_*`:
- A interjeição foi **localizada** à convenção do alvo? (`Hm?`→`Hein?`, `Ngh...`→`Nnh...`, `Gah!`→`Ai!`)
- É **coerente** com as outras ocorrências (mesma convenção em todo o corpus)?
- Sobrevive à transliteração do conector, se houver (não vira outra coisa sem o acento)?
- Qualquer interjeição idêntica ao source (`base_translation == text_source`) é um **issue**, salvo
  justificativa (ex.: grito puro de vogais `Aaaah!`, ou nome próprio sendo soletrado).

---

> **No runtime:** o micro-QA por lote é, na prática, o `run_scene` (gates de cobertura, tokens, fitting, round-trip e
> `spoiler_check`) mais o `naturalness_lint.py`; `micro_qa_log.json` e `fix_suggestions.json` descritos abaixo são o
> formato do **playbook cognitivo** — nenhum script os grava hoje (o `quality_gate`/`quality_review` usam
> `back_translation_<cena>.json` e as planilhas de `qa_revisao/`). A Parte 2 em produção é `quality_fix.py`
> (retradução dirigida, pago com `--apply`), `quality_review.py apply` (correção humana verbatim) e `tm_correct.py`
> (find→replace por cena/offset nos três artefatos) — ver `07_qa.md`.

---

## BACK-TRANSLATION PARA ALTO RISCO

Para linhas com `risk_level: high` ou `critical` no plano:
1. Traduzir a linha do idioma-alvo de volta para o idioma-fonte (mentalmente ou explicitamente)
2. Comparar com o texto-fonte original
3. Se o sentido ou tom diferirem significativamente → revisar

**Casos que sempre exigem back-translation:**
- Linhas de comédia com timing específico
- Linhas que contêm a primeira menção de um termo de lore importante
- Qualquer linha de uma persona de identidade dupla que possa vazar a identidade revelada em retrospecto
- Linhas que possam insinuar informação de spoiler

---

## OUTPUTS OBRIGATÓRIOS

### `micro_qa_log.json`

Append a cada lote (não sobrescrever — acumular):

```json
{
  "batch": 1,
  "offsets": "[range de ids do lote]",
  "lines_reviewed": 0,
  "issues_found": [
    {
      "offset": "[id]",
      "type": "tone_drift",
      "speaker": "[personagem]",
      "issue": "[descrição do problema]",
      "current_pt": "[tradução atual]",
      "suggested_pt": "[correção sugerida]",
      "severity": "high"
    }
  ],
  "token_errors": [],
  "spoiler_flags": [],
  "back_translation_flags": [],
  "batch_approved": false,
  "notes": ""
}
```

---

## POLÍTICA DE APROVAÇÃO DE LOTE

- **0 issues críticos + ≤ 3 issues altos:** lote aprovado, prosseguir
- **1+ issues críticos:** lote bloqueado, corrigir antes de avançar
- **> 3 issues altos:** revisar padrão — pode indicar problema sistêmico que precisa ser corrigido nas regras, não nas linhas individuais

---

## REGRAS CRÍTICAS

- **O micro-QA é executado antes do próximo lote, não depois.** A ordem é: traduzir lote → micro-QA → **Parte 2 (correção) se reprovado** → aprovar → traduzir próximo lote.
- Quando `batch_approved: false`: executar a **Parte 2 — Ciclo de correção** (abaixo) antes de avançar. Não corrigir inline — a Parte 2 tem o protocolo de escopo cirúrgico.
- Issues de tom que aparecem em ≥ 3 linhas do mesmo personagem no mesmo lote são **problemas sistêmicos**, não pontuais. Revisar o perfil de voz no prompt do passo 6 antes de continuar.
- O `micro_qa_log.json` é a memória do processo — não apagar entre lotes.
- Issues com `escalated: true` (segundo failure no mesmo id) devem ser resolvidos pelo usuário antes da entrega.

---

# PARTE 2 — CICLO DE CORREÇÃO
## Aplicar correções ao corpus sem corromper traduções existentes

> **Quando usar:** após a Parte 1 emitir `batch_approved: false`, ou após o passo 07 produzir `fix_suggestions.json`. Fecha o loop detectar → corrigir → re-validar.

---

## OBJETIVO (Parte 2)

Aplicar correções identificadas pelo Micro-QA ou pelo QA Final ao `approved_translations.csv` (a tradução aprovada), com escopo cirúrgico (apenas os IDs identificados), verificação inline de cada correção, e registro auditável do que foi alterado.

---

## INPUTS (Parte 2)

- `micro_qa_log.json` (se vindo do Parte 1) **ou** `fix_suggestions.json` (se vindo do passo 07)
- `approved_translations.csv` (traduções aprovadas — alvo das correções)
- `project.json` (tokens, length_constraints)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`

---

## PROTOCOLO DE EXECUÇÃO

### Passo 1 — Separar issues por severidade

| Severidade | Ação neste ciclo |
|------------|-----------------|
| Crítica | Corrigir obrigatoriamente |
| Alta | Corrigir obrigatoriamente |
| Média | Corrigir se possível; marcar como `deferred` caso contrário |
| Baixa | Opcional |

### Passo 2 — Definir o escopo cirúrgico

Montar a lista de IDs (`id_column`) a corrigir. **Esta lista é o único escopo do ciclo.** Nenhuma linha fora desses IDs deve ser tocada — qualquer edição fora do escopo é uma regressão potencial.

### Passo 3 — Aplicar correções

Para cada ID na lista:
1. Localizar a linha em `approved_translations.csv`
2. Aplicar a `suggested` do log, ou uma nova tradução fundamentada na análise
3. Antes de aceitar, verificar checklist obrigatório:

```
CHECKLIST DE CORREÇÃO:
□ O registro está correto para o personagem (ver perfil em tone_analysis.md)?
□ A entidade está tratada conforme glossary.csv?
□ Os tokens (project.json → formatting_tokens) e quebras de linha estão preservados (mesma contagem)?
□ O comprimento respeita project.json → length_constraints?
□ Se risk_level: high ou critical: back-translation confirma sentido?
```

### Passo 4 — Mini-QA pós-correção

Após aplicar todas as correções, executar verificação reduzida **somente nas linhas corrigidas**:
- Re-verificar voz para cada linha alterada
- Re-verificar tokens de cada linha alterada
- Re-verificar entidades de cada linha alterada
- Se a linha é `risk_level: high` ou `critical`: back-translation obrigatória

Se uma linha falhar no mini-QA:
- Registrar novo issue no log
- Se for a segunda tentativa no mesmo ID: escalar para revisão humana com `escalated: true`

### Passo 5 — Atualizar os logs

**Se vindo da Parte 1** — adicionar entrada ao `micro_qa_log.json` (append):

```json
{
  "batch": "1_correction",
  "offsets": "[ids corrigidos]",
  "lines_reviewed": 0,
  "issues_found": [],
  "corrections_applied": [
    {
      "offset": "[id]",
      "original_issue": "[descrição]",
      "previous_pt": "[tradução anterior]",
      "corrected_pt": "[tradução corrigida]",
      "mini_qa_passed": true
    }
  ],
  "batch_approved": true,
  "notes": "Todas as correções aplicadas e verificadas. Lote liberado."
}
```

**Se vindo do 07** — marcar cada issue resolvido no `fix_suggestions.json`:
```json
{
  "id": "FIX-001",
  "status": "applied",
  "applied_pt": "[tradução aplicada]",
  "verified": true
}
```

---

## OUTPUTS OBRIGATÓRIOS (Parte 2)

| Arquivo | Modificação |
|---------|-------------|
| `approved_translations.csv` | Linhas corrigidas atualizadas (somente os IDs do escopo) |
| `micro_qa_log.json` | Nova entrada de correção adicionada (append) |
| `fix_suggestions.json` | Issues resolvidos marcados com `"status": "applied"` |

---

## REGRAS CRÍTICAS (Parte 2)

- **Escopo cirúrgico é inviolável.** Nunca modificar linhas fora da lista de IDs do ciclo.
- **Nunca aceitar uma correção sem passar pelo checklist.** A correção pode introduzir um novo issue.
- Após o ciclo: se `micro_qa_log.json` ainda contém issues críticos não resolvidos → **o bloqueio de avanço para o próximo lote permanece ativo**.
- Issues escalados (`escalated: true`) devem ser resolvidos pelo usuário antes da entrega.
- Este passo é **sempre sequencial** — não aplicar correções em paralelo no mesmo arquivo.
