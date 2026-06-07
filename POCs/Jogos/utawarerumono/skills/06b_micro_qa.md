# SKILL 06b — MICRO-QA
## QA por lote — executar após cada bloco de tradução

> **Quando usar:** Automaticamente após cada lote de 200 linhas traduzidas no passo 6. Antes de prosseguir para o próximo lote.

---

## OBJETIVO

Detectar drift de tom, erros de entidade e quebras de registro enquanto o corpus ainda é pequeno o suficiente para corrigir sem custo alto. O micro-QA não substitui o QA final do passo 7 — ele previne que problemas se acumulem.

---

## INPUTS

- O lote recém-traduzido (200 linhas do `translated.csv`)
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

**Sinais de alerta:**
- Haku soando melodramático ou formal
- Kuon soando fria ou hostil
- Ukon soando com vocabulário de corte (eco de Oshtor)
- Sakon soando seco ou frio (eco de Mikazuchi)
- Mito soando com autoridade (eco do Mikado)
- Nekone soando casual ou emocional sem contexto
- Maroro com frases simplificadas
- Atuy com qualquer registro formal

### 2. Verificação de entidades
Para cada termo do `glossary.csv` presente no lote:
- Verificar que `handling_rule: manter_original` → termo não foi traduzido
- Verificar que `handling_rule: traduzir` → termo usa exatamente a `pt_br_translation`
- Verificar que nomes de personagens estão na forma canônica

### 3. Verificação de tokens
- Contar tokens `{W}` e `\n` no original e na tradução de cada linha
- Sinalizar qualquer linha onde a contagem não bate

### 4. Verificação de spoilers
Se o lote contém alguma linha com `spoiler_flags` no plano:
- Verificar que aliases de spoiler não foram usados antes do reveal
- Verificar que os dois nomes de um par de identidade dupla não aparecem no mesmo segmento

### 5. Verificação de naturalidade (amostra)
Selecionar aleatoriamente 10% das linhas do lote e verificar:
- A linha soa como português nativo ou como tradução?
- Há calques de inglês ("de qualquer forma" onde seria "de qualquer jeito")?
- A pontuação e as reticências estão sendo usadas corretamente?

---

## BACK-TRANSLATION PARA ALTO RISCO

Para linhas com `risk_level: high` ou `critical` no plano:
1. Traduzir a linha pt-BR de volta para inglês (mentalmente ou explicitamente)
2. Comparar com o `text_en` original
3. Se o sentido ou tom diferirem significativamente → revisar

**Casos que sempre exigem back-translation:**
- Linhas de comédia com timing específico
- Linhas que contêm a primeira menção de um termo de lore importante
- Qualquer linha de Sakon (antes do reveal) que possa parecer fria em retrospecto
- Linhas de Mito que possam insinuar poder ou autoridade

---

## OUTPUTS OBRIGATÓRIOS

### `micro_qa_log.json`

Append a cada lote (não sobrescrever — acumular):

```json
{
  "batch": 1,
  "offsets": "0x33cd–0x995f",
  "lines_reviewed": 150,
  "issues_found": [
    {
      "offset": "0x36fa",
      "type": "tone_drift",
      "speaker": "Kuon",
      "issue": "Registro formal ('suponho que você ainda possa') inadequado para Kuon",
      "current_pt": "...Suponho que você ainda possa estar delirando...?",
      "suggested_pt": "...Deve ser o delírio ainda...?",
      "severity": "high"
    }
  ],
  "token_errors": [],
  "spoiler_flags": [],
  "back_translation_flags": [],
  "batch_approved": false,
  "notes": "5 issues de tom identificados. Aguardando correção antes de próximo lote."
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
- Quando `batch_approved: false`: executar o Passo 06c (Correction Cycle) antes de avançar. Não tentar corrigir inline no mesmo passo — o 06c tem o protocolo de escopo cirúrgico.
- Issues de tom que aparecem em ≥ 3 linhas do mesmo personagem no mesmo lote são **problemas sistêmicos**, não pontuais. Revisar o perfil de voz no prompt do passo 6 antes de continuar.
- O `micro_qa_log.json` é a memória do processo — não apagar entre lotes.
- Issues com `escalated: true` no log (segundo failure no mesmo offset) devem ser resolvidos por humano antes da entrega — não podem ser fechados automaticamente.
