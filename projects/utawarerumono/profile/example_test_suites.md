# Suites de Teste Sintético — Utawarerumono: Mask of Deception
## Exemplo de referência do projeto (instancia o Passo 5b genérico)

> O Passo 5b genérico descreve **como gerar** suites a partir dos pares de identidade
> e perfis de voz `voice_criticality: high`. Este arquivo é a instância concreta para
> este título — serve de exemplo de como as regras de geração se materializam.
>
> No pipeline real, estas suites viram `synthetic_test_corpus.json`.

---

## SUITE-HAKU-CALIBRATION (protagonista/narrador)
Calibra a voz base — subreação, humor seco, nunca melodramático.

Casos a incluir:
- Vendo algo impossível e comentando com calma
- Reclamando de frio/fome/cansaço (subreação a desconforto físico)
- Momento de competência silenciosa (sem piadas, sem drama)
- Piada por deflexão quando algo sério acontece

Exemplo:
```json
{
  "id": "TEST-001",
  "suite": "SUITE-HAKU-CALIBRATION",
  "purpose": "Verificar subreação de Haku — não deve soar melodramático",
  "speaker": "Haku",
  "context": "Haku acaba de ver algo impossível e reage internamente",
  "text_en": "An insect that size doesn't exist. I must be dreaming.",
  "expected_register": "casual_dry",
  "expected_characteristics": ["frase curta", "sem hipérbole", "subreação"],
  "red_flags": ["qualquer melodrama", "adjetivos excessivos", "exclamações desnecessárias"],
  "pass_criteria": "Soa como Haku pensando consigo mesmo, não como narrador literário",
  "fail_criteria": "Infla o registro ou adiciona ênfase que o original não tem"
}
```

---

## SUITE-UKON (par Ukon/Oshtor — executar antes de qualquer segmento de Ukon)

```json
{
  "id": "TEST-UKON-01",
  "purpose": "Ukon relaxado e direto — sem ecos de linguagem de corte",
  "speaker": "Ukon",
  "text_en": "Could be worse. At least nobody's trying to kill us. Yet.",
  "expected_register": "casual_competent",
  "red_flags": ["formal court language", "excessive gravity", "Oshtor's court register"]
},
{
  "id": "TEST-OSHTOR-01",
  "purpose": "Oshtor com peso de dever e linguagem de corte",
  "speaker": "Oshtor",
  "text_en": "This is my duty. I will not allow another outcome.",
  "expected_register": "formal_grave",
  "red_flags": ["casual phrasing", "vocabulário relaxado típico de Ukon"]
}
```
**Critério da suite:** Ukon e Oshtor devem soar como pessoas diferentes, mas reconhecíveis como a mesma em retrospecto.

---

## SUITE-SAKON (par Sakon/Mikazuchi — o maior contraste do jogo)

```json
{
  "id": "TEST-SAKON-01",
  "purpose": "Sakon genuinamente caloroso — não pode parecer performático",
  "speaker": "Sakon",
  "text_en": "Here, I made too many today. Take some home with you.",
  "expected_register": "warm_cheerful",
  "red_flags": ["any coldness", "flat affect", "anything ironic in retrospect"]
},
{
  "id": "TEST-MIKAZUCHI-01",
  "purpose": "Mikazuchi gelado e econômico — contraste máximo",
  "speaker": "Mikazuchi",
  "text_en": "They are dealt with.",
  "expected_register": "cold_minimal",
  "red_flags": ["warmth", "elaboration", "qualquer phrasing tipo Sakon"]
}
```
**Critério da suite:** ler uma linha de Sakon logo após uma de Mikazuchi deve criar dissonância imediata.
**Critério crítico:** reler Sakon e perguntar — "soaria irônico se o leitor já soubesse que é Mikazuchi?"

---

## SUITE-MITO (par Mito/Mikado)

```json
{
  "id": "TEST-MITO-01",
  "purpose": "Mito como velho cansado — nenhum traço de autoridade",
  "speaker": "Mito",
  "text_en": "Wine's better with company. Sit down.",
  "expected_register": "casual_weathered",
  "red_flags": ["imperial tone", "formal vocabulary", "comando que soa como ordem de autoridade"]
}
```
**Critério:** Mito deve passar despercebido como um velho comum que bebe bem.

---

## SUITE-TATARI (entidade pré-reveal — monstro sem pathos)

```json
{
  "id": "TEST-TATARI-01",
  "purpose": "Tatari como monstro — sem humanidade sugerida",
  "speaker": "narrador",
  "text_en": "The creature surged forward, engulfing everything in its path.",
  "expected_register": "action_neutral",
  "red_flags": ["palavra que sugira dor/sofrimento da criatura", "pathos", "hesitação em descrevê-la como ameaça"]
}
```

---

## SUITE-REVEAL (impacto de reveal — transição alias→nome real)

```json
{
  "id": "TEST-REVEAL-01",
  "purpose": "Linha de reveal de Ukon/Oshtor deve ter peso sem melodrama",
  "speaker": "narrador",
  "context": "O momento exato em que a identidade é revelada",
  "text_en": "The mercenary known as Ukon removed his hood. It was Oshtor.",
  "expected_register": "grave_restrained",
  "red_flags": ["melodrama", "ênfase excessiva", "over-explanation"]
}
```
