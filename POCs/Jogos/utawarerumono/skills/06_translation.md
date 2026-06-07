# SKILL 06 — TRANSLATION
## Execução da tradução com controle de progresso

> **Quando usar:** Após o TRANSLATION PLANNING. Opera em lotes de tamanho fixo com rastreamento de progresso e auto-revisão de voz inline.

---

## OBJETIVO

Traduzir o corpus em lotes controláveis, aplicando o plano do passo 5, com auto-revisão de voz inline a cada linha e rastreamento de progresso que permite retomada exata.

---

## INPUTS

- `translation_plan.json` (output obrigatório do passo 5)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`
- `translation_status.json` (lido no início; criado se não existir)
- `dialogs.csv` (corpus completo — todas as linhas, incluindo não traduzidas)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `translation_plan.json` | Existe; `total_lines` bate com o número de linhas em `dialogs.csv` |
| `glossary.csv` | Existe; nenhuma entrada com `handling_rule` vazio |
| `translation_rules.md` | Existe |
| `tone_analysis.md` | Existe |

**Verificação de cobertura do plano:**
- Contar linhas em `dialogs.csv`
- Contar entradas em `translation_plan.json`
- Se contagens diferem: o plano não cobre todo o corpus — **PARAR**

❌ **Se qualquer verificação falhar: PARAR. Traduzir sem plano completo viola o contrato do processo.**

---

## ESTRUTURA DO TRANSLATED.CSV

**A partir desta versão: o `translated.csv` contém TODAS as linhas do `dialogs.csv`.**

Linhas não traduzidas têm `text_pt` vazio. Isso torna o progresso visível e permite retomada sem perda.

```csv
offset,text_en,text_pt
0x33cd,...calls... to me...?,...chama... para mim...?
0x998e,but this thing... defies all reason. And...,
0x99cb,"This enormous insect's shell, hard as metal,\n",
```

---

## CONTROLE DE PROGRESSO

### `translation_status.json`

Criado/atualizado ao final de cada lote:

```json
{
  "project": "utawarerumono_mod",
  "total_lines": 33014,
  "translated_lines": 150,
  "completion_pct": 0.45,
  "last_offset": "0x995f",
  "next_offset": "0x998e",
  "last_updated": "2025-06-07",
  "batch_size": 200,
  "batches_completed": 1,
  "notes": ""
}
```

**Ao iniciar uma nova execução do passo 6:**
1. Ler `translation_status.json`
2. Localizar `next_offset` no `dialogs.csv`
3. Traduzir as próximas `batch_size` linhas a partir desse ponto
4. Atualizar `translation_status.json` com o novo `next_offset` e contagem

**Tamanho padrão do lote:** 200 linhas por execução.

---

## AUTO-REVISÃO DE VOZ INLINE

Para cada linha traduzida onde `speaker` é um personagem com perfil de voz definido no `tone_analysis.md`, executar a verificação antes de aceitar a tradução:

```
CHECKLIST DE VOZ (executar mentalmente antes de aceitar cada linha):
□ O registro está correto para este personagem neste contexto?
□ O comprimento da frase está dentro do padrão do personagem?
□ Alguma palavra ou construção soa errada para esta voz?
□ Se for linha de comédia: a piada funciona? O ritmo está certo?
□ Se contém entidade do glossário: a entidade está tratada corretamente?
□ Se tem risk_level ≥ medium no plano: o risco foi endereçado?
□ COMPRIMENTO: cada segmento entre \n não excede 140% do EN? (UI/CAPS: ≤ 110%)
```

**Sobre a verificação de comprimento:**
PT-BR é ~20-30% mais longo que EN em média. Caixas de diálogo têm tamanho fixo.

- Medir cada segmento entre marcadores `\n` separadamente
- Se comprimento PT-BR > 140% do EN: tentar reformulação que preserve tom + sentido
- Se não for possível reformular sem perder qualidade: marcar `length_warning: true` no `translation_status.json` para revisão posterior
- Para UI (linhas em CAPS): limite mais estrito de 110% — boxes de UI são menores
- **Prioridade:** tom > comprimento > literalidade. Nunca sacrificar voz para encurtar.

**Personagens de atenção máxima** (verificação obrigatória em cada linha):
- **Haku:** casual, seco, nunca melodramático. Comédia por subreação.
- **Kuon:** calorosa e direta, não formal. Scolding afetivo, nunca hostil.
- **Nekone:** formal por escolha, não por frieza.
- **Ukon:** mais solto que Oshtor. Nunca ecos de linguagem de corte.
- **Sakon:** genuinamente caloroso. Nenhuma frieza vazando antes do reveal.
- **Mito:** velho cansado. Nenhuma autoridade imperial antes do reveal.
- **Maroro:** frases longas são caracterização, não simplificar.
- **Atuy:** nunca formal, nem com superiores.

---

## REGRAS DE EXECUÇÃO

### Preservação de tokens
**Obrigatório:** tokens de jogo devem ser preservados exatamente como estão.
- `{W75}`, `{W80}`, `{W10}` — timers de espera, preservar posição
- `\n` — quebras de linha, preservar exatamente
- `{COLOR}`, `{END}` — tags de formatação, preservar

**Verificação:** se a linha original tem N tokens, a tradução deve ter os mesmos N tokens nas posições correspondentes.

### Nomes e termos do glossário
- Verificar `glossary.csv` antes de traduzir qualquer nome próprio ou termo de lore
- `handling_rule: manter_original` → copiar exatamente do original
- `handling_rule: traduzir` → usar a `pt_br_translation` do CSV
- `handling_rule: traduzir_parcial` → aplicar a regra específica da entrada

### Linhas de sistema (CAPS)
- Linhas em CAPS são texto de sistema computacional
- Manter em CAPS na tradução
- Registro: frio, técnico, sem afeto
- Preferir estrutura `OBJETO: ESTADO` para logs de sistema

### Linhas incompletas (quebra de frase)
- Muitas linhas terminam com `\n` e continuam no próximo offset
- Verificar sempre se a junção da linha atual + próxima linha soa natural em português

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `translated.csv` | Todas as linhas do corpus; `text_pt` preenchido para as traduzidas, vazio para as pendentes |
| `translation_status.json` | Estado atual do progresso, `next_offset` para retomada |

---

## REGRAS CRÍTICAS

- **Nunca reiniciar do zero.** Sempre ler `translation_status.json` primeiro e continuar do `next_offset`.
- **Nunca sobrescrever traduções já existentes** ao retomar — só preencher linhas com `text_pt` vazio.
- Se o `translation_plan.json` existir para o lote atual, usar os `base_translation` como ponto de partida, não ignorar o plano.
- Linhas com `risk_level: critical` no plano → marcar no status como `needs_human_review` antes de prosseguir.
