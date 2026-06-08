# SKILL 06b — MICRO-QA
## QA por lote — executar após cada bloco de tradução

> **Quando usar:** Automaticamente após cada lote traduzido no passo 6. Antes de prosseguir para o próximo lote.

---

## OBJETIVO

Detectar drift de tom, erros de entidade e quebras de registro enquanto o corpus ainda é pequeno o suficiente para corrigir sem custo alto. O micro-QA não substitui o QA final do passo 7 — ele previne que problemas se acumulem.

> **Referência normativa:** este QA verifica o cumprimento da **Carta de Governança**
> (`translation_governance.md`) — voz, lore, situação e o checklist por linha/lote. Apoio executável:
> `framework/validation/naturalness_lint.py` (smells de naturalidade) roda antes da revisão contextual.

---

## INPUTS

- O lote recém-proposto (`translation_plan.json → base_translation`, consolidado em `approved_translations.csv`) confrontado com o `dialogs.csv` (source)
- `project.json` (tokens, convenção de sistema)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`
- `translation_plan.json` (para comparar `base_translation` com o resultado final)

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

- **O micro-QA é executado antes do próximo lote, não depois.** A ordem é: traduzir lote → micro-QA → **06c se reprovado** → aprovar → traduzir próximo lote.
- Quando `batch_approved: false`: executar o Passo 06c (Correction Cycle) antes de avançar. Não corrigir inline no mesmo passo — o 06c tem o protocolo de escopo cirúrgico.
- Issues de tom que aparecem em ≥ 3 linhas do mesmo personagem no mesmo lote são **problemas sistêmicos**, não pontuais. Revisar o perfil de voz no prompt do passo 6 antes de continuar.
- O `micro_qa_log.json` é a memória do processo — não apagar entre lotes.
- Issues com `escalated: true` (segundo failure no mesmo id) devem ser resolvidos pelo usuário antes da entrega.
