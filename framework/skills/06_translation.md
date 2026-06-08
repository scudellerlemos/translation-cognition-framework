# SKILL 06 — TRANSLATION
## Execução da tradução com controle de progresso

> **Quando usar:** Após o TRANSLATION PLANNING. Opera em lotes de tamanho fixo com rastreamento de progresso e auto-revisão de voz inline.

---

## OBJETIVO

Traduzir o corpus em lotes controláveis, aplicando o plano do passo 5, com auto-revisão de voz inline a cada linha e rastreamento de progresso que permite retomada exata.

---

## INPUTS

- `translation_plan.json` (output obrigatório do passo 5)
- `project.json` (tokens, idiomas, formato, batch_size, length_constraints)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`
- `translation_status.json` (lido no início; criado se não existir)
- Corpus-fonte (`project.json → source.file`) — todas as linhas, incluindo não traduzidas

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `translation_plan.json` | Existe; `total_lines` bate com o número de linhas no corpus-fonte |
| `glossary.csv` | Existe; nenhuma entrada com `handling_rule` vazio |
| `translation_rules.md` | Existe |
| `tone_analysis.md` | Existe |
| `project.json` | Existe; `formatting_tokens` e `length_constraints` declarados |

**Verificação de cobertura do plano:**
- Contar linhas no corpus-fonte
- Contar entradas em `translation_plan.json`
- Se contagens diferem: o plano não cobre todo o corpus — **PARAR**

❌ **Se qualquer verificação falhar: PARAR. Traduzir sem plano completo viola o contrato do processo.**

---

## ONDE FICAM AS TRADUÇÕES PROPOSTAS

As traduções propostas vivem no `translation_plan.json` (campo `base_translation`), uma por linha.
O progresso e a retomada são rastreados pelo `translation_status.json` (`next_offset`).

```
translation_plan.json → base_translation (proposta)   →  approved_translations.csv (aprovado)
```

Após aprovação, o conjunto vai para `approved_translations.csv` (`id_column`, `text_target`). A IA
**não** mantém um CSV de dados com source+target preenchido à mão (ver `schemas/artifacts_schema.md`).

> Os nomes de coluna seguem o `project.json`: o ID usa `source.id_column`; o alvo recebe a tradução no `target_language`.

---

## CONTROLE DE PROGRESSO

### `translation_status.json`

Criado/atualizado ao final de cada lote:

```json
{
  "project": "[título]",
  "total_lines": 0,
  "translated_lines": 0,
  "completion_pct": 0.0,
  "last_offset": "[último id traduzido]",
  "next_offset": "[próximo id a traduzir]",
  "last_updated": "YYYY-MM-DD",
  "batch_size": 200,
  "batches_completed": 0,
  "length_warnings": [],
  "needs_human_review": [],
  "notes": ""
}
```

**Ao iniciar uma nova execução do passo 6:**
1. Ler `translation_status.json`
2. Localizar `next_offset` no corpus-fonte
3. Traduzir as próximas `batch_size` linhas a partir desse ponto
4. Atualizar `translation_status.json` com o novo `next_offset` e contagem

**Tamanho do lote:** `project.json → batch_size` (default 200).

---

## AUTO-REVISÃO DE VOZ INLINE

Para cada linha traduzida onde `speaker` é um personagem com perfil de voz no `tone_analysis.md`, executar a verificação antes de aceitar a tradução:

```
CHECKLIST DE VOZ (executar mentalmente antes de aceitar cada linha):
□ O registro está correto para este personagem neste contexto?
□ O comprimento da frase está dentro do padrão do personagem?
□ Alguma palavra ou construção soa errada para esta voz (ver red flags do perfil)?
□ Se for linha de comédia: a piada funciona? O ritmo está certo?
□ Se contém entidade do glossário: a entidade está tratada corretamente?
□ Se tem risk_level ≥ medium no plano: o risco foi endereçado?
□ ORÇAMENTO: a tradução cabe no byte_budget da linha (verificação em bytes, ver abaixo)?
```

**Personagens de atenção máxima:** todos com `voice_criticality: high` no `tone_analysis.md` —
verificação obrigatória em **cada linha**. As características e red flags de cada personagem vêm do
seu perfil. Não há lista hardcoded de personagens aqui; a lista é o conjunto de perfis `high` do projeto.

---

## SHIFT-LEFT: ORÇAMENTO DE BYTES COMO RESTRIÇÃO DE TRADUÇÃO

Esta é a maior alavanca de custo do framework. Em vez de deixar a tradução estourar e pagar LLM para
reescrever depois (Passo 08), traduzir **já dentro do orçamento** na 1ª passada — a custo marginal zero,
porque a chamada de tradução já acontece.

**1. Restrição no prompt de tradução.**
Para cada linha, incluir o `byte_budget` (do `translation_plan.json`) como restrição dura:
> "Traduza de modo que o resultado, codificado pela tabela do projeto, **caiba em N bytes**.
> Prioridade: tom > caber > literalidade."

**2. Verificação determinística (não-LLM) antes de aceitar.**
Medir os bytes que a tradução ocupará (encode com a `table_schema` do conector) e comparar com o
`byte_budget`. **Isto é aritmética — não consome LLM.**

- Cabe → aceitar.
- Não cabe → reformular preservando tom (ainda na mesma passada de tradução).
- Persistindo o estouro sem perder qualidade → marcar o ID em `length_warnings` no
  `translation_status.json`. Ele será resolvido pela cascata determinística no Passo 08, e só o
  resíduo irredutível irá para a reescrita LLM em lote (T4).

**Mídias sem byte-space** (ex: legendas): substituir a métrica por caracteres/linha ou CPS, conforme
o media-profile. O mecanismo (orçamento como restrição + check determinístico) é o mesmo.

- **Prioridade:** tom > caber no orçamento > literalidade. Nunca sacrificar voz para encurtar.

> Racional por tipo de mídia e detalhes de byte-space: ver `framework/media-profiles/<media_profile>.md`
> e `framework/connectors/<connector.type>.md`.

> Racional por tipo de mídia: ver `framework/media-profiles/<media_profile>.md`.

---

## REGRAS DE EXECUÇÃO

### Preservação de tokens
**Obrigatório:** preservar exatamente todos os tokens listados em `project.json → formatting_tokens`.

- Cada token mantém posição correspondente entre fonte e tradução
- Quebras de linha estruturais preservadas exatamente
- **Verificação:** se a linha-fonte tem N tokens, a tradução tem os mesmos N tokens nas posições correspondentes

> Ver `framework/media-profiles/<media_profile>.md` para o racional de preservação de tokens.

### Nomes e termos do glossário
- Verificar `glossary.csv` antes de traduzir qualquer nome próprio ou termo de lore
- `handling_rule: manter_original` → copiar exatamente do original
- `handling_rule: traduzir` → usar a `target_translation` do CSV
- `handling_rule: traduzir_parcial` → aplicar a regra específica da entrada

### Linhas de sistema
- Detectar conforme `project.json → system_line_convention` (ex: `all_caps`)
- Manter a convenção na tradução; registro frio, técnico, sem afeto
- Preferir estrutura `OBJETO: ESTADO` para logs de sistema

### Linhas incompletas (quebra de frase)
- Muitas linhas terminam com quebra e continuam no próximo ID
- Verificar sempre se a junção da linha atual + próxima soa natural no idioma-alvo

### Interjeições, onomatopeias e exclamações de emoção
Sons de **susto, dor, surpresa, esforço, riso, choro, hesitação** (ex.: `Ngh...`, `Nn...`, `Hm?`,
`Gah!`, `Ghh!`) **são tradução, não pontuação** — devem ser **LOCALIZADOS** às convenções do
idioma-alvo, nunca copiados do source. Copiar a interjeição do source é um erro de naturalidade tão
grave quanto deixar uma palavra sem traduzir.

- Traduzir pela **emoção/situação**, não pela letra: o som certo é o que um falante nativo emitiria
  *naquela* situação dramática (ver o `intent`/`tone_register` da linha no plano).
- Sinal de detecção: `tone_register` ~ `interjeicao_*` **ou** linha curta cujo conteúdo é só
  onomatopeia. **Atenção:** muitas interjeições ficam marcadas como `dialogo` genérico — detectar
  também por conteúdo (linha curta, sem palavras do idioma-alvo).
- **Coerência:** se o projeto adota uma convenção (ex.: gemido = `Nnh...`, dúvida = `Hein?`),
  aplicá-la a TODAS as ocorrências. Curar as formas num artefato de referência do projeto.
- **Restrição do conector:** se o conector transflitera na gravação (ex.: fonte sem acentos), escolher
  formas que sobrevivam à transliteração — ex.: `Hã?`→`Ha?` lê como riso; preferir `Hein?`/`Ai!`.

---

## ONDE A TRADUÇÃO É ESCRITA (proposta → aprovação → aplicação)

A IA **propõe** a tradução; ela **não** edita o binário nem um CSV de dados à mão. Fluxo:

1. **Propor (este passo, cognitivo):** a tradução de cada linha é registrada no
   `translation_plan.json`, campo `base_translation`. Reviewável e auditável.
2. **Aprovar (usuário):** após revisão (incluindo Micro-QA 06b), o conjunto aprovado é consolidado em
   **`approved_translations.csv`** (`id_column`, `text_target`) — a fonte de verdade da tradução.
3. **Aplicar (Passo 08, determinístico):** o script do conector lê `dialogs.csv` + `approved_translations.csv`
   e grava a saída. Nenhuma escrita à mão da IA nos dados/binário.

> ⚠️ A IA **não preenche `text_target` à mão** num arquivo que contém o source. Isso evita
> contaminar o source e mantém a separação cognição/mecânica. Ver `schemas/artifacts_schema.md`.

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `translation_plan.json` | Traduções **propostas** (`base_translation`) + metadados por linha |
| `approved_translations.csv` | Traduções **aprovadas** (`id_column`, `text_target`) — consolidado após aprovação |
| `translation_status.json` | Estado atual do progresso, `next_offset` para retomada |

---

## REGRAS CRÍTICAS

- **Nunca reiniciar do zero.** Sempre ler `translation_status.json` primeiro e continuar do `next_offset`.
- **A IA propõe; não edita dados à mão.** A tradução aprovada vive em `approved_translations.csv`; a aplicação é do script (Passo 08).
- **Nunca sobrescrever traduções já aprovadas** ao retomar — só completar as pendentes.
- Se o `translation_plan.json` existir para o lote atual, usar os `base_translation` como ponto de partida, não ignorar o plano.
- Linhas com `risk_level: critical` no plano → adicionar a `needs_human_review` no status antes de prosseguir.
