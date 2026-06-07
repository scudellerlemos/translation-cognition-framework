# SKILL 05 — TRANSLATION PLANNING
## Planejar antes de traduzir

> **Quando usar:** Após o GLOSSARY CREATION, antes de qualquer execução de tradução. Este passo é **obrigatório** — não pular para o passo 6 sem o plano.

---

## OBJETIVO

Para cada linha do corpus, definir intenção, identificar entidades presentes, aplicar regras do glossário, esboçar uma tradução base, e marcar riscos. O plano é o contrato entre planejamento e execução — o passo 6 não inventa, executa o plano.

---

## INPUTS

- `dialogs.csv` (corpus completo)
- `glossary.csv`
- `translation_rules.md`
- `entities.csv`
- `tone_analysis.md`

---

## OUTPUTS OBRIGATÓRIOS

### `translation_plan.json`

Estrutura por linha:

```json
{
  "offset": "0x36fa",
  "text_en": "...I suppose you might still be delirious...?",
  "speaker": "Kuon",
  "entities_present": [],
  "tone_register": "warm_direct",
  "intent": "Kuon especula sobre o estado de Haku de forma calorosa, não clínica",
  "risk_level": "low",
  "risk_notes": "",
  "base_translation": "...Deve ser o delírio ainda...?",
  "glossary_flags": [],
  "spoiler_flags": []
}
```

### Campos obrigatórios

| Campo | Descrição |
|-------|-----------|
| `offset` | Offset da linha no arquivo original |
| `text_en` | Texto em inglês |
| `speaker` | Personagem que fala (ou "narrador" / "sistema") |
| `entities_present` | Lista de entidades do glossário presentes na linha |
| `tone_register` | Registro de voz esperado para este falante neste contexto |
| `intent` | O que a linha faz narrativamente (1 frase) |
| `risk_level` | `low` / `medium` / `high` / `critical` |
| `risk_notes` | Descrição do risco se `risk_level` ≥ `medium` |
| `base_translation` | Rascunho de tradução para o passo 6 partir |
| `glossary_flags` | Termos do glossário presentes que exigem atenção |
| `spoiler_flags` | Aliases ou termos de spoiler presentes |

### Critérios de risk_level

| Nível | Quando usar |
|-------|-------------|
| `critical` | Linha contém alias de spoiler major/critical; qualquer erro aqui é irreparável |
| `high` | Linha é cena de comédia com timing sensível; ou personagem com voz muito específica (Haku, Maroro, Nosuri) |
| `medium` | Linha tem ambiguidade de registro ou entidade com regra especial |
| `low` | Linha é narrativa/descritiva sem riscos identificados |

---

## CORPUS DE TESTE SINTÉTICO

**Novo artefato obrigatório a partir desta versão do processo.**

Arquivo: `synthetic_test_corpus.json`

Antes de traduzir os segmentos reais de mid/late game, criar um conjunto de 20-30 linhas sintéticas que testam os pontos críticos do jogo:

```json
{
  "test_cases": [
    {
      "id": "TEST-001",
      "purpose": "Verificar voz de Ukon — deve soar relaxado, humor seco, sem ecos da linguagem de corte de Oshtor",
      "speaker": "Ukon",
      "text_en": "Could be worse. At least nobody's trying to kill us today.",
      "expected_register": "casual_warm",
      "red_flags": ["formal court language", "excessive gravity", "any Oshtor-style vocabulary"]
    },
    {
      "id": "TEST-002",
      "purpose": "Verificar voz de Sakon — genuinamente caloroso, sem vazar frieza de Mikazuchi",
      "speaker": "Sakon",
      "text_en": "Here, I made too many today. Take some sweets home with you.",
      "expected_register": "warm_cheerful",
      "red_flags": ["any coldness", "flat affect", "minimal phrasing"]
    },
    {
      "id": "TEST-003",
      "purpose": "Verificar voz de Mito — velho cansado, sem autoridade imperial",
      "speaker": "Mito",
      "text_en": "Wine's better when there's company. Sit down.",
      "expected_register": "casual_weathered",
      "red_flags": ["imperial tone", "formal vocabulary", "any hint of authority"]
    }
  ]
}
```

O corpus sintético deve ser traduzido e revisado **antes** de traduzir os segmentos reais correspondentes. Se a tradução do corpus sintético falhar, o processo para para diagnóstico.

---

## REGRAS CRÍTICAS

- **Este passo é obrigatório.** Ir direto do passo 4 para o passo 6 sem o plano é o erro estrutural mais comum do processo.
- O `base_translation` no plano não é a tradução final — é o ponto de partida. O passo 6 pode melhorar, mas não deve contradizer a intenção documentada.
- Linhas com `risk_level: critical` devem ser revisadas por humano antes de entrar no corpus final, independente da qualidade da tradução automática.
- O corpus de teste sintético deve cobrir **todos** os pares de identidade dupla (Ukon/Oshtor, Sakon/Mikazuchi, Mito/Mikado) antes de traduzir os segmentos reais dessas personas.
