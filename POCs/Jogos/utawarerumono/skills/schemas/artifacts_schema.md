# SCHEMAS DOS ARTEFATOS — Referência Formal
## Definição de campos obrigatórios, tipos e valores aceitos

> **Propósito:** Este documento é a fonte de verdade sobre o formato de cada artefato do pipeline. Quando um passo recebe um artefato como input, valida-o contra este schema antes de executar.

---

## SCHEMAS DE ARQUIVOS CSV

### `entities.csv`

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `canonical_name` | string | ✅ | Qualquer — deve ser único no arquivo |
| `category` | enum | ✅ | Personagem / Local / Facção / Item / Conceito / Título / Criatura / Alimento / Cultural / Mecânica / UI |
| `aliases` | string | ✅ | Lista separada por `;` com nível entre `()`: `Oshtor(critical);Aruruu(none)` |
| `importance` | enum | ✅ | main / secondary / background |
| `confidence` | enum | ✅ | high / medium / low |
| `notes` | string | — | Texto livre; obrigatório se `confidence: low` |

**Invariantes:**
- `canonical_name` é único por linha
- Aliases de spoiler `major` ou `critical` nunca são o `canonical_name`
- Entidades UI sempre têm `importance: background`

---

### `glossary.csv`

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `term` | string | ✅ | Qualquer — deve ser único no arquivo |
| `category` | enum | ✅ | Mesmas categorias do entities.csv |
| `pt_br_translation` | string | ✅ se `traduzir` / `traduzir_parcial` | Forma final em PT-BR |
| `handling_rule` | enum | ✅ | manter_original / traduzir / traduzir_parcial |
| `spoiler_level` | enum | ✅ | none / moderate / major / critical |
| `aliases` | string | — | Mesmo formato do entities.csv |
| `notes` | string | — | Instruções específicas de uso |

**Invariantes:**
- Nenhuma linha tem `handling_rule` vazio
- `pt_br_translation` obrigatório quando `handling_rule ∈ {traduzir, traduzir_parcial}`
- Para `manter_original`: `pt_br_translation` deve ser idêntico ao `term` ou vazio

---

### `translated.csv`

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `offset` | string | ✅ | Hex com prefixo `0x`; deve ser único no arquivo |
| `text_en` | string | ✅ | Texto original em inglês |
| `text_pt` | string | — | Tradução em PT-BR; vazio = pendente |

**Invariantes:**
- Cada `offset` aparece exatamente uma vez (mesma contagem do `dialogs.csv`)
- Tokens `{W75}`, `{W80}`, `{W10}` preservados exatamente
- Contagem de `\n` igual entre `text_en` e `text_pt` para linhas traduzidas
- Linhas em CAPS no EN permanecem em CAPS no PT

---

## SCHEMAS DE ARQUIVOS MARKDOWN ESTRUTURADO

### `research_log.md`

Arquivo markdown com seções obrigatórias. Campos de cabeçalho:

| Campo | Obrigatório | Valores aceitos |
|-------|-------------|-----------------|
| `Status` | ✅ | `pending` / `reconciled` |
| `Data de reconciliação` | ✅ se `reconciled` | `YYYY-MM-DD` |
| `Fronteira de spoiler` | ✅ | Descrição textual (ex: "Caps. 1–5, pré-reveal de Ukon") |
| `Seções ignoradas intencionalmente` | ✅ | Lista de seções não lidas ou "nenhuma" |

Tabela **Fontes Avaliadas** — colunas obrigatórias:

| Coluna | Obrigatório | Valores aceitos |
|--------|-------------|-----------------|
| `ID` | ✅ | `SRC-NNN` único no arquivo |
| `Fonte` | ✅ | Nome da fonte |
| `Tipo` | ✅ | Wiki / Corpus / Guia / Site oficial / Outro |
| `Tier` | ✅ | 1 / 2 / 3 |
| `Cobertura de Spoiler` | ✅ | Descrição textual |
| `URL/Caminho` | ✅ | URL ou caminho local |
| `Encontrada por` | ✅ | IA / Humano / IA + Humano |
| `Usada` | ✅ | Sim / Não |
| `Notas` | — | Texto livre |

Tabela **Conflitos Resolvidos** — presente sempre (vazia se não houve conflito):

| Coluna | Obrigatório |
|--------|-------------|
| `Termo` | ✅ |
| `Versão IA` | ✅ |
| `Versão Humano` | ✅ |
| `Decisão` | ✅ |
| `Razão` | ✅ |

Seção **Gaps de Pesquisa** — presente sempre (vazia se não houve gap).

**Invariantes:**
- `status: reconciled` só pode ser definido após comparação entre achados da IA e do humano
- Cada fonte com `Usada: Sim` deve ter ao menos uma citação em `universe_knowledge_base.md`
- IDs de fonte (`SRC-NNN`) devem ser únicos no arquivo e sequenciais

---

## SCHEMAS DE ARQUIVOS JSON

### `entities_candidates.json`

```
{
  "entities": [
    {
      "name": string,           // OBRIGATÓRIO
      "category": enum,         // OBRIGATÓRIO — categorias do entities.csv
      "context": string,        // OBRIGATÓRIO — frase ou offset onde aparece
      "confidence": enum,       // OBRIGATÓRIO — high / medium / low
      "spoiler_level": enum,    // OBRIGATÓRIO — none / moderate / major / critical
      "notes": string           // opcional
    }
  ]
}
```

---

### `aliases_map.json`

```
{
  "aliases": [
    {
      "alias": string,              // OBRIGATÓRIO — forma do alias
      "canonical_name": string,     // OBRIGATÓRIO — a quem se refere
      "spoiler_level": enum,        // OBRIGATÓRIO — none / moderate / major / critical
      "reveal_timing": string,      // OBRIGATÓRIO se spoiler_level ≠ none
      "notes": string               // opcional
    }
  ]
}
```

---

### `translation_plan.json`

```
{
  "lines": [
    {
      "offset": string,           // OBRIGATÓRIO — hex com 0x
      "text_en": string,          // OBRIGATÓRIO
      "speaker": string,          // OBRIGATÓRIO — canonical_name ou "narrador" / "sistema"
      "entities_present": [str],  // OBRIGATÓRIO — lista vazia se nenhuma
      "tone_register": string,    // OBRIGATÓRIO
      "intent": string,           // OBRIGATÓRIO — 1 frase
      "risk_level": enum,         // OBRIGATÓRIO — low / medium / high / critical
      "risk_notes": string,       // OBRIGATÓRIO se risk_level ≥ medium
      "base_translation": string, // OBRIGATÓRIO
      "glossary_flags": [str],    // OBRIGATÓRIO — lista vazia se nenhum
      "spoiler_flags": [str]      // OBRIGATÓRIO — lista vazia se nenhum
    }
  ],
  "total_lines": int,             // OBRIGATÓRIO — deve bater com total de dialogs.csv
  "critical_lines": int,          // OBRIGATÓRIO — contagem de risk_level: critical
  "plan_version": string          // OBRIGATÓRIO — data de criação "YYYY-MM-DD"
}
```

**Invariante:** `total_lines` deve ser igual ao número de linhas em `dialogs.csv`.

---

### `translation_status.json`

```
{
  "project": string,            // OBRIGATÓRIO
  "total_lines": int,           // OBRIGATÓRIO — imutável após criação
  "translated_lines": int,      // OBRIGATÓRIO — atualizado a cada lote
  "completion_pct": float,      // OBRIGATÓRIO — translated_lines / total_lines
  "last_offset": string,        // OBRIGATÓRIO — último offset traduzido no lote
  "next_offset": string,        // OBRIGATÓRIO — próximo offset a traduzir
  "last_updated": string,       // OBRIGATÓRIO — "YYYY-MM-DD"
  "batch_size": int,            // OBRIGATÓRIO — padrão 200
  "batches_completed": int,     // OBRIGATÓRIO
  "length_warnings": [string],  // OBRIGATÓRIO — offsets com comprimento > 140% do EN
  "needs_human_review": [string], // OBRIGATÓRIO — offsets com risk_level: critical
  "notes": string               // opcional
}
```

---

### `synthetic_test_corpus.json`

```
{
  "test_suites": [
    {
      "suite_id": string,         // OBRIGATÓRIO — ex: "SUITE-HAKU-CALIBRATION"
      "purpose": string,          // OBRIGATÓRIO
      "execute_before": string,   // OBRIGATÓRIO — gatilho de execução
      "cases": [
        {
          "id": string,                       // OBRIGATÓRIO — único no arquivo
          "suite": string,                    // OBRIGATÓRIO — referência ao suite_id
          "purpose": string,                  // OBRIGATÓRIO
          "speaker": string,                  // OBRIGATÓRIO
          "context": string,                  // OBRIGATÓRIO
          "text_en": string,                  // OBRIGATÓRIO
          "expected_register": string,        // OBRIGATÓRIO
          "expected_characteristics": [str],  // OBRIGATÓRIO — lista não-vazia
          "red_flags": [str],                 // OBRIGATÓRIO — lista não-vazia
          "pass_criteria": string,            // OBRIGATÓRIO
          "fail_criteria": string             // OBRIGATÓRIO
        }
      ]
    }
  ]
}
```

---

### `synthetic_test_results.json`

```
{
  "execution_date": string,   // OBRIGATÓRIO — "YYYY-MM-DD"
  "suite": string,            // OBRIGATÓRIO — suite_id executada
  "results": [
    {
      "id": string,                   // OBRIGATÓRIO — referência ao caso
      "status": enum,                 // OBRIGATÓRIO — passed / failed
      "translation_produced": string, // OBRIGATÓRIO
      "failure_reason": string,       // OBRIGATÓRIO se status: failed
      "suggested_fix": string,        // opcional se status: failed
      "notes": string                 // opcional
    }
  ],
  "suite_approved": bool,     // OBRIGATÓRIO
  "blocking_issues": int,     // OBRIGATÓRIO — falhas que bloqueiam avanço
  "action_required": string   // OBRIGATÓRIO se suite_approved: false
}
```

**Critério de aprovação da suite:**
- `suite_approved: true` somente se `blocking_issues: 0`
- Um caso com `status: failed` que tenha `suggested_fix` aceito **não** conta como blocking se o fix foi aplicado às regras e re-testado

---

### `micro_qa_log.json`

```
{
  "entries": [
    {
      "batch": string,              // OBRIGATÓRIO — número ou "N_correction"
      "offsets": string,            // OBRIGATÓRIO — range "0xAAAA–0xBBBB" ou lista
      "lines_reviewed": int,        // OBRIGATÓRIO
      "issues_found": [
        {
          "offset": string,         // OBRIGATÓRIO
          "type": enum,             // OBRIGATÓRIO — tone_drift / entity_error / token_error / spoiler_violation / naturalness / back_translation
          "speaker": string,        // OBRIGATÓRIO se type: tone_drift
          "issue": string,          // OBRIGATÓRIO
          "current_pt": string,     // OBRIGATÓRIO
          "suggested_pt": string,   // OBRIGATÓRIO
          "severity": enum,         // OBRIGATÓRIO — critical / high / medium / low
          "escalated": bool         // opcional — true se segunda tentativa falhou
        }
      ],
      "corrections_applied": [],    // presente apenas em entradas de correção (06c)
      "token_errors": [str],        // OBRIGATÓRIO — lista vazia se nenhum
      "spoiler_flags": [str],       // OBRIGATÓRIO — lista vazia se nenhum
      "back_translation_flags": [str], // OBRIGATÓRIO — lista vazia se nenhum
      "batch_approved": bool,       // OBRIGATÓRIO
      "notes": string               // opcional
    }
  ]
}
```

**Invariante:** o arquivo é append-only. Nunca remover entradas existentes.

---

### `fix_suggestions.json`

```
{
  "suggestions": [
    {
      "id": string,             // OBRIGATÓRIO — "FIX-NNN" único
      "priority": enum,         // OBRIGATÓRIO — critical / high / medium / low
      "offset": string,         // OBRIGATÓRIO
      "category": enum,         // OBRIGATÓRIO — semantic_error / tone_drift / entity_error / token_error / spoiler_violation / naturalness / length_warning
      "original_en": string,    // OBRIGATÓRIO
      "current_pt": string,     // OBRIGATÓRIO
      "issue": string,          // OBRIGATÓRIO
      "fix_pt": string,         // OBRIGATÓRIO
      "status": enum,           // OBRIGATÓRIO — open / applied / deferred / escalated
      "applied_pt": string,     // presente quando status: applied
      "verified": bool,         // presente quando status: applied
      "notes": string           // opcional
    }
  ]
}
```

---

## VERIFICAÇÃO DE SCHEMA — CHECKLIST RÁPIDO

Antes de consumir um artefato em qualquer passo, verificar:

```
□ O arquivo existe no diretório do projeto?
□ Todos os campos OBRIGATÓRIOS estão presentes em cada entrada?
□ Os enums estão dentro dos valores aceitos?
□ Os invariantes do schema são respeitados?
□ O total_lines (quando aplicável) bate com dialogs.csv?
```

Se qualquer verificação falhar → **PARAR e reportar o campo inválido antes de continuar.**
