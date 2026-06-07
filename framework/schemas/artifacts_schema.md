# SCHEMAS DOS ARTEFATOS — Referência Formal
## Definição de campos obrigatórios, tipos e valores aceitos

> **Propósito:** Este documento é a fonte de verdade sobre o formato de cada artefato gerado pelo pipeline. Quando um passo recebe um artefato como input, valida-o contra este schema antes de executar.
>
> **Convenção de nomes de coluna/campo dependentes de idioma:** onde aparece `text_source` /
> `text_target` / `target_translation`, o nome concreto pode espelhar os idiomas do projeto
> (ex: `text_en` / `text_pt`). O ID da linha usa `project.json → source.id_column`. O schema do
> manifesto está em `project_schema.md`.

---

## SCHEMAS DE ARQUIVOS CSV

### `entities.csv`

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `canonical_name` | string | ✅ | Qualquer — deve ser único no arquivo |
| `category` | enum | ✅ | Personagem / Local / Facção / Item / Conceito / Título / Criatura / Alimento / Cultural / Mecânica / UI |
| `aliases` | string | ✅ | Lista separada por `;` com nível entre `()`: `<alias>(critical);<alias>(none)` |
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
| `term` | string | ✅ | Termo no idioma-fonte — único no arquivo |
| `category` | enum | ✅ | Mesmas categorias do entities.csv |
| `target_translation` | string | ✅ se `traduzir` / `traduzir_parcial` | Forma final no idioma-alvo |
| `handling_rule` | enum | ✅ | manter_original / traduzir / traduzir_parcial |
| `spoiler_level` | enum | ✅ | none / moderate / major / critical |
| `aliases` | string | — | Mesmo formato do entities.csv |
| `notes` | string | — | Instruções específicas de uso |

**Invariantes:**
- Nenhuma linha tem `handling_rule` vazio
- `target_translation` obrigatório quando `handling_rule ∈ {traduzir, traduzir_parcial}`
- Para `manter_original`: `target_translation` deve ser idêntico ao `term` ou vazio

---

### `dialogs.csv` (output do Passo 00 — extração)

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `<id_column>` | string | ✅ | Identificador da linha (`project.json → source.id_column`); único; ex: offset hex |
| `text_source` | string | ✅ | Texto no idioma-fonte, com control codes já mapeados em tokens |
| `byte_budget` | int | ✅ p/ meios binários | Nº de bytes que a string ocupa no meio (shift-left; consumido nos Passos 05/06) |

**Invariantes:**
- `dialogs.csv` é **gerado pelo Passo 00** (não é dado pré-existente) quando há `connector`
- É **somente leitura** a partir do Passo 01
- `byte_budget` ≥ 0; presente em todas as linhas quando o meio tem restrição de bytes

---

### `translated.csv`

| Campo | Tipo | Obrigatório | Valores aceitos |
|-------|------|-------------|-----------------|
| `<id_column>` | string | ✅ | Identificador da linha (`project.json → source.id_column`); único no arquivo |
| `text_source` | string | ✅ | Texto no idioma-fonte |
| `text_target` | string | — | Tradução no idioma-alvo; vazio = pendente |
| `byte_budget` | int | — | Herdado do `dialogs.csv`; usado pelo Passo 08 (reinserção) |

**Invariantes:**
- Cada ID aparece exatamente uma vez (mesma contagem do corpus-fonte)
- Tokens de `project.json → formatting_tokens` preservados exatamente
- Contagem de quebras de linha igual entre fonte e alvo nas linhas traduzidas
- Linhas de sistema (`system_line_convention`) mantêm a convenção na tradução

---

## SCHEMAS DE ARQUIVOS MARKDOWN ESTRUTURADO

### `extraction_log.md` (output do Passo 00)

Metadados auditáveis da extração. Seções obrigatórias:

| Campo / Seção | Obrigatório | Conteúdo |
|---------------|-------------|----------|
| Binário | ✅ | Caminho do `source_binary` extraído |
| Tabela | ✅ | Caminho do `table_schema` usado |
| Encoding | ✅ | Encoding declarado |
| Total de strings | ✅ | Quantidade de strings extraídas |
| Offsets cobertos | ✅ | Faixa/lista de offsets |
| Mapa de control codes | ✅ | token ↔ bytes |
| Gate de round-trip | ✅ | passou / falhou (byte-idêntico?) |
| Gate de charset | ✅ | `target_charset_supported` + caracteres ausentes |

---

### `reinsertion_report.md` (output do Passo 08)

Resultado da reinserção. Seções obrigatórias:

| Campo / Seção | Obrigatório | Conteúdo |
|---------------|-------------|----------|
| Strings gravadas | ✅ | Total + distribuição por tier (T1/T2/T3/T4) |
| Resíduo T4 | ✅ | IDs que precisaram de reescrita LLM em lote |
| Overflows não resolvidos | ✅ | IDs que falharam mesmo após T4 → viram issues p/ 06c/07 |
| Repoints | ✅ se `repoint` | Ponteiros recalculados |
| Patch | ✅ | Formato emitido (ips/bps/xdelta) + caminho |

---

### `research_log.md`

Arquivo markdown com seções obrigatórias. Campos de cabeçalho:

| Campo | Obrigatório | Valores aceitos |
|-------|-------------|-----------------|
| `Status` | ✅ | `pending` / `reconciled` |
| `Data de reconciliação` | ✅ se `reconciled` | `YYYY-MM-DD` |
| `Fronteira de spoiler` | ✅ | Descrição textual (ex: "Caps. 1–5, pré-reveal de <persona>") |
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
      "context": string,        // OBRIGATÓRIO — frase ou id de linha onde aparece
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
      "offset": string,           // OBRIGATÓRIO — id da linha (source.id_column)
      "text_source": string,      // OBRIGATÓRIO — texto no idioma-fonte
      "speaker": string,          // OBRIGATÓRIO — canonical_name ou "narrador" / "sistema"
      "entities_present": [str],  // OBRIGATÓRIO — lista vazia se nenhuma
      "tone_register": string,    // OBRIGATÓRIO
      "intent": string,           // OBRIGATÓRIO — 1 frase
      "risk_level": enum,         // OBRIGATÓRIO — low / medium / high / critical
      "risk_notes": string,       // OBRIGATÓRIO se risk_level ≥ medium
      "base_translation": string, // OBRIGATÓRIO
      "byte_budget": int,         // OBRIGATÓRIO p/ meios binários — orçamento de bytes (shift-left)
      "glossary_flags": [str],    // OBRIGATÓRIO — lista vazia se nenhum
      "spoiler_flags": [str]      // OBRIGATÓRIO — lista vazia se nenhum
    }
  ],
  "total_lines": int,             // OBRIGATÓRIO — deve bater com total do corpus-fonte
  "critical_lines": int,          // OBRIGATÓRIO — contagem de risk_level: critical
  "plan_version": string          // OBRIGATÓRIO — data de criação "YYYY-MM-DD"
}
```

**Invariante:** `total_lines` deve ser igual ao número de linhas no corpus-fonte.

---

### `translation_status.json`

```
{
  "project": string,            // OBRIGATÓRIO
  "total_lines": int,           // OBRIGATÓRIO — imutável após criação
  "translated_lines": int,      // OBRIGATÓRIO — atualizado a cada lote
  "completion_pct": float,      // OBRIGATÓRIO — translated_lines / total_lines
  "last_offset": string,        // OBRIGATÓRIO — último id traduzido no lote
  "next_offset": string,        // OBRIGATÓRIO — próximo id a traduzir
  "last_updated": string,       // OBRIGATÓRIO — "YYYY-MM-DD"
  "batch_size": int,            // OBRIGATÓRIO — de project.json (default 200)
  "batches_completed": int,     // OBRIGATÓRIO
  "length_warnings": [string],  // OBRIGATÓRIO — ids que excedem length_constraints
  "needs_human_review": [string], // OBRIGATÓRIO — ids com risk_level: critical
  "notes": string               // opcional
}
```

---

### `synthetic_test_corpus.json`

```
{
  "test_suites": [
    {
      "suite_id": string,         // OBRIGATÓRIO — ex: "SUITE-<NOME>"
      "purpose": string,          // OBRIGATÓRIO
      "execute_before": string,   // OBRIGATÓRIO — gatilho de execução
      "cases": [
        {
          "id": string,                       // OBRIGATÓRIO — único no arquivo
          "suite": string,                    // OBRIGATÓRIO — referência ao suite_id
          "purpose": string,                  // OBRIGATÓRIO
          "speaker": string,                  // OBRIGATÓRIO
          "context": string,                  // OBRIGATÓRIO
          "text_source": string,              // OBRIGATÓRIO — linha sintética no idioma-fonte
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
      "offsets": string,            // OBRIGATÓRIO — range de ids ou lista
      "lines_reviewed": int,        // OBRIGATÓRIO
      "issues_found": [
        {
          "offset": string,         // OBRIGATÓRIO — id da linha
          "type": enum,             // OBRIGATÓRIO — tone_drift / entity_error / token_error / spoiler_violation / naturalness / back_translation
          "speaker": string,        // OBRIGATÓRIO se type: tone_drift
          "issue": string,          // OBRIGATÓRIO
          "current_pt": string,     // OBRIGATÓRIO — tradução atual
          "suggested_pt": string,   // OBRIGATÓRIO — correção sugerida
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
      "offset": string,         // OBRIGATÓRIO — id da linha
      "category": enum,         // OBRIGATÓRIO — semantic_error / tone_drift / entity_error / token_error / spoiler_violation / naturalness / length_warning
      "original_en": string,    // OBRIGATÓRIO — texto-fonte
      "current_pt": string,     // OBRIGATÓRIO — tradução atual
      "issue": string,          // OBRIGATÓRIO
      "fix_pt": string,         // OBRIGATÓRIO — correção sugerida
      "status": enum,           // OBRIGATÓRIO — open / applied / deferred / escalated
      "applied_pt": string,     // presente quando status: applied
      "verified": bool,         // presente quando status: applied
      "notes": string           // opcional
    }
  ]
}
```

> Os sufixos `_en` / `_pt` nos campos acima são herança histórica e podem espelhar os idiomas
> reais do projeto; o que importa é a função (texto-fonte / texto-alvo).

---

## VERIFICAÇÃO DE SCHEMA — CHECKLIST RÁPIDO

Antes de consumir um artefato em qualquer passo, verificar:

```
□ O arquivo existe no diretório do projeto?
□ Todos os campos OBRIGATÓRIOS estão presentes em cada entrada?
□ Os enums estão dentro dos valores aceitos?
□ Os invariantes do schema são respeitados?
□ O total_lines (quando aplicável) bate com o corpus-fonte?
```

Se qualquer verificação falhar → **PARAR e reportar o campo inválido antes de continuar.**
