# SKILL 05b — SYNTHETIC TEST CORPUS
## Corpus de teste sintético para pontos críticos

> **Quando usar:** No final do passo 5 (TRANSLATION PLANNING), antes de traduzir qualquer segmento de mid ou late game que contenha personas de identidade dupla ou outros pontos críticos. Também deve ser executado ao início do projeto para calibrar a voz do protagonista.

---

## OBJETIVO

Testar a capacidade de manter vozes distintas e tratar spoilers corretamente **antes** de entrar no corpus real. Um erro no corpus sintético custa zero — o mesmo erro em 500 linhas de corpus real custa revisão completa.

---

## QUANDO EXECUTAR

| Gatilho | Corpus sintético a executar |
|---------|----------------------------|
| Início do projeto | Calibração de voz de Haku (narrador) |
| Antes dos primeiros segmentos de Ukon | Suite Ukon |
| Antes dos primeiros segmentos de Sakon | Suite Sakon |
| Antes dos primeiros segmentos de Mito | Suite Mito |
| Antes de qualquer segmento com Tatari nomeado | Suite Tatari |
| Antes dos segmentos de reveal (qualquer um) | Suite Reveal |

---

## ESTRUTURA DO ARQUIVO

`synthetic_test_corpus.json`

```json
{
  "test_suites": [
    {
      "suite_id": "SUITE-HAKU-CALIBRATION",
      "purpose": "Calibrar voz de Haku antes de traduzir corpus real",
      "execute_before": "primeiro segmento de narração de Haku",
      "cases": [...]
    }
  ]
}
```

Cada caso de teste:

```json
{
  "id": "TEST-001",
  "suite": "SUITE-HAKU-CALIBRATION",
  "purpose": "Verificar subreação de Haku — não deve soar melodramático",
  "speaker": "Haku",
  "context": "Haku acaba de ver algo impossível e reage internamente",
  "text_en": "An insect that size doesn't exist. I must be dreaming.",
  "expected_register": "casual_dry",
  "expected_characteristics": [
    "frase curta",
    "sem hipérbole",
    "subreação — o impossível comentado com calma"
  ],
  "red_flags": [
    "qualquer melodrama",
    "adjetivos excessivos",
    "exclamações desnecessárias"
  ],
  "pass_criteria": "A tradução soa como Haku pensando consigo mesmo, não como narrador literário",
  "fail_criteria": "A tradução infla o registro ou adiciona ênfase que o original não tem"
}
```

---

## SUITES OBRIGATÓRIAS

### SUITE-HAKU-CALIBRATION
Testa a voz base do protagonista — subreação, humor seco, nunca melodramático.

**Casos a incluir:**
- Haku vendo algo impossível e comentando com calma
- Haku reclamando de frio / fome / cansaço (subreação a desconforto físico)
- Haku em momento de competência silenciosa (sem piadas, sem drama)
- Haku fazendo piada por deflexão quando algo sério acontece

---

### SUITE-UKON (executar antes de qualquer segmento de Ukon)
Testa a distinção entre Ukon e Oshtor.

**Casos a incluir:**

```json
{
  "id": "TEST-UKON-01",
  "purpose": "Ukon deve soar relaxado e direto — sem ecos de linguagem de corte",
  "speaker": "Ukon",
  "text_en": "Could be worse. At least nobody's trying to kill us. Yet.",
  "expected_register": "casual_competent",
  "red_flags": ["formal court language", "excessive gravity", "vocabulary typical of Oshtor's court register"]
},
{
  "id": "TEST-UKON-02",
  "purpose": "Ukon com humor seco — não deve parecer Oshtor sendo casual",
  "speaker": "Ukon",
  "text_en": "You worry too much. Worrying doesn't change outcomes.",
  "expected_register": "dry_warm",
  "red_flags": ["cold delivery", "formal phrasing", "any echo of duty/responsibility vocabulary"]
},
{
  "id": "TEST-OSHTOR-01",
  "purpose": "Oshtor deve soar com peso de dever e linguagem de corte",
  "speaker": "Oshtor",
  "text_en": "This is my duty. I will not allow another outcome.",
  "expected_register": "formal_grave",
  "red_flags": ["casual phrasing", "any relaxed vocabulary typical of Ukon"]
}
```

**Critério de aprovação da suite:** as traduções de Ukon e Oshtor devem soar claramente como pessoas diferentes, mas reconhecidamente a mesma pessoa em retrospecto.

---

### SUITE-SAKON (executar antes de qualquer segmento de Sakon)
Testa a distinção entre Sakon e Mikazuchi — a maior do jogo.

**Casos a incluir:**

```json
{
  "id": "TEST-SAKON-01",
  "purpose": "Sakon genuinamente caloroso — não pode parecer performático",
  "speaker": "Sakon",
  "text_en": "Here, I made too many today. Take some home with you.",
  "expected_register": "warm_cheerful",
  "red_flags": ["any coldness", "flat affect", "minimal phrasing", "anything that would feel ironic in retrospect"]
},
{
  "id": "TEST-SAKON-02",
  "purpose": "Sakon com metáforas de doce — deve soar natural, não forçado",
  "speaker": "Sakon",
  "text_en": "Life is sweeter when shared, don't you think?",
  "expected_register": "warm_cheerful",
  "red_flags": ["irony", "coldness beneath the warmth", "any subtext of threat"]
},
{
  "id": "TEST-MIKAZUCHI-01",
  "purpose": "Mikazuchi gelado e econômico — contraste máximo com Sakon",
  "speaker": "Mikazuchi",
  "text_en": "They are dealt with.",
  "expected_register": "cold_minimal",
  "red_flags": ["warmth", "elaboration", "any Sakon-style phrasing"]
}
```

**Critério de aprovação da suite:** a leitura de uma linha de Sakon logo após uma linha de Mikazuchi deve criar dissonância imediata. O contraste é o ponto.

**Critério crítico:** reler todas as traduções de Sakon e perguntar — "isso soaria irônico se o leitor já soubesse que é Mikazuchi?" Se a resposta for sim, revisar.

---

### SUITE-MITO (executar antes de qualquer segmento de Mito)
Testa a voz de Mito — sem nenhum vazamento de autoridade imperial.

**Casos a incluir:**

```json
{
  "id": "TEST-MITO-01",
  "purpose": "Mito como velho cansado — nenhum traço de autoridade",
  "speaker": "Mito",
  "text_en": "Wine's better with company. Sit down.",
  "expected_register": "casual_weathered",
  "red_flags": ["imperial tone", "formal vocabulary", "any command that sounds like an order from authority"]
},
{
  "id": "TEST-MITO-02",
  "purpose": "Mito com humor autodepreciativo — leveza sem leveza excessiva",
  "speaker": "Mito",
  "text_en": "I've seen enough sunrises. One more won't change anything.",
  "expected_register": "wry_tired",
  "red_flags": ["wisdom that sounds imperial", "gravitas that reveals age/power", "any sentence that sounds like it carries centuries of weight"]
}
```

**Critério de aprovação:** a tradução de Mito deve poder passar despercebida como um velho comum que bebe bem. Nenhuma linha deve fazer o leitor perguntar "quem é esse cara realmente?"

---

### SUITE-TATARI (executar antes de qualquer segmento que nomeie Tatari)
Testa o tratamento pré-reveal — monstro, sem pathos.

```json
{
  "id": "TEST-TATARI-01",
  "purpose": "Tatari como monstro — sem nenhuma humanidade sugerida",
  "speaker": "narrador",
  "text_en": "The creature surged forward, engulfing everything in its path.",
  "expected_register": "action_neutral",
  "red_flags": ["any word that suggests pain or suffering of the creature", "pathos", "hesitation in describing it as threat"]
}
```

---

### SUITE-REVEAL (executar antes dos segmentos de qualquer reveal)
Testa que a transição de alias para nome real funciona narrativamente.

```json
{
  "id": "TEST-REVEAL-01",
  "purpose": "A linha do reveal de Ukon/Oshtor deve ter peso sem ser melodramática",
  "speaker": "narrador",
  "context": "O momento exato em que a identidade é revelada",
  "text_en": "The mercenary known as Ukon removed his hood. It was Oshtor.",
  "expected_register": "grave_restrained",
  "red_flags": ["melodrama", "excessive emphasis", "over-explanation"]
}
```

---

## PROCESSO DE EXECUÇÃO

1. Traduzir todos os casos da suite relevante
2. Revisar cada tradução contra os `red_flags` e `pass_criteria`
3. Se algum caso falhar: identificar a causa raiz antes de continuar
   - Causa raiz no prompt? → ajustar instrução de voz para o passo 6
   - Causa raiz na regra? → atualizar `translation_rules.md` + registrar no `decision_log.md`
   - Causa raiz pontual? → corrigir o caso e verificar se o padrão não se repete
4. Só avançar para o corpus real após aprovação completa da suite

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `synthetic_test_corpus.json` | Todos os casos de teste por suite |
| `synthetic_test_results.json` | Resultados de cada execução: passed / failed + notas |

### Estrutura do `synthetic_test_results.json`

```json
{
  "execution_date": "2025-06-07",
  "suite": "SUITE-SAKON",
  "results": [
    {
      "id": "TEST-SAKON-01",
      "status": "passed",
      "translation_produced": "Fiz demais hoje. Leva um pouco pra casa.",
      "notes": "Tom genuinamente caloroso, sem subtext de frieza."
    },
    {
      "id": "TEST-SAKON-02",
      "status": "failed",
      "translation_produced": "A vida fica mais doce quando compartilhada, não acha?",
      "failure_reason": "Soa levemente irônico em retrospecto — 'doce' com maiúscula implícita demais",
      "suggested_fix": "A vida é melhor em companhia, não é?",
      "notes": "Remover metáfora de doce explícita neste caso específico — o calor vem do gesto, não da palavra."
    }
  ],
  "suite_approved": false,
  "blocking_issues": 1,
  "action_required": "Corrigir TEST-SAKON-02 e re-executar antes de traduzir segmentos reais de Sakon."
}
```

---

## REGRAS CRÍTICAS

- **Nenhum segmento real de persona de identidade dupla deve ser traduzido antes da suite correspondente ser aprovada.** Isso é inegociável.
- Aprovação da suite não é automática — cada caso deve ser revisado explicitamente.
- Casos que falham por causa raiz sistêmica (instrução de prompt) bloqueiam **toda a suite**, não só o caso individual.
- Os resultados do corpus sintético alimentam o `decision_log.md` quando revelam necessidade de ajuste de regra.
