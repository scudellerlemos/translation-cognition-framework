# Decision Log — Utawarerumono: Mask of Deception

Registro acumulativo de decisões não-óbvias. Nunca apagar entradas (ver `framework/skills/04b_decision_log.md`).

---

## space_strategy — in_place → repoint

**Data:** POC
**Passo do SDD:** 00 / 08
**Tipo:** revision

**Decisão tomada:**
Mudar `connector.space_strategy` de `in_place` para `repoint`.

**Alternativas consideradas:**
- Manter `in_place` — rejeitada: só 12/20 (60%) das traduções cabem no `byte_budget` original.
- Abreviar tudo para caber in_place — rejeitada: degrada qualidade/tom de quase metade das linhas.

**Razão da decisão final:**
pt-BR é mais longo que o inglês e seus acentos custam 2 bytes em UTF-8. Medição real da POC:
8/20 linhas estouram o orçamento de bytes. `repoint` (recalcular ponteiros) é o caminho viável.

**Impacto:**
Reinserção (Passo 08). Repoint completo exige mapear a tabela de ponteiros do `.sdat` (próximo passo).
A POC gravou apenas as 12 que cabem in_place como prova de conceito.

**Revisão necessária:** sim — implementar repoint real (pointer table) antes de traduzir o corpus completo.

---

## Gate de charset pt-BR — método e veredito

**Data:** POC
**Passo do SDD:** 00
**Tipo:** external

**Decisão tomada:**
Marcar `target_charset_supported: likely` e exigir confirmação in-game antes de produção.

**Alternativas consideradas:**
- Confirmar por presença no texto-fonte — **insuficiente**: o fonte é inglês e quase não usa acentos
  (só `õ` e `À` aparecem em texto real).
- Parsear o `Font.fnt` por suposição de layout (uint16 LE) — resultado inconsistente, não confiável.

**Razão da decisão final:**
`õ` (U+00F5) e `À` (U+00C0) já são renderizados pelo jogo; ambos do bloco Latin-1 Supplement, onde
vivem TODOS os acentos pt-BR. Suporte é altamente provável, mas não confirmado glifo-a-glifo.

**Impacto:**
Tradução pt-BR (acentos). Se algum glifo faltar, precisa expandir a fonte ou transliterar.

**Revisão necessária:** sim — teste in-game com pangrama pt-BR (`áéíóú âêô ãõ ç ÁÉÍ ÃÕ Ç`) ou parse correto do `Font.fnt`.

---

## Anomalia 0x33f9 — texto PT/EN corrompido na fonte

**Data:** POC
**Passo do SDD:** 00
**Tipo:** formatting

**Decisão tomada:**
Marcar a linha `0x33f9` como anomalia de fonte (não traduzir em cima do lixo; tratar como linha de sistema reescrita).

**Razão:**
A string original já vem misturada PT/EN e truncada ("...SISTEMAS AM . RESTARTING...") no próprio jogo.
Não é erro de extração. O conector deve sinalizar esse tipo de anomalia no `extraction_log.md`.

**Impacto:** linha 0x33f9. **Revisão necessária:** não (tratada como sistema na POC).

---

## Modelo de execução da tradução — arquivo aprovado + script

**Data:** POC (revisão de governança)
**Passo do SDD:** 06 / 08
**Tipo:** revision

**Decisão tomada:**
A IA **não escreve a tradução à mão** nos dados. Ela propõe no `translation_plan.json`
(`base_translation`); após aprovação, o conjunto vai para `approved_translations.csv`
(`offset`, `text_target`); o script `reinsert.py` aplica esse arquivo ao binário.

**Alternativas consideradas:**
- IA preenchendo `text_target` no `translated.csv` (source+target juntos) — rejeitada: mistura
  proposta com aplicação e arrisca contaminar o source.

**Razão da decisão final:**
Separar cognição (propor) → aprovação (usuário) → aplicação (script determinístico). O `translated.csv`
escrito à mão foi depreciado.

**Impacto:** Passos 06/08, schema dos artefatos, scripts da instância.
**Revisão necessária:** não.

---

## Saída em output/ + governança de scripts

**Data:** POC (revisão de governança)
**Passo do SDD:** 08
**Tipo:** formatting

**Decisão tomada:**
A saída final vai para `output/ScriptEvent.sdat` (mesmo nome e extensão do input), substituindo
`artifacts/build/`. Os scripts do conector são **executados, não refeitos**; criar script novo só com permissão.

**Impacto:** localização da entrega; fluxo de trabalho da IA.
**Revisão necessária:** não.

---

## Ordem de offset ≠ ordem de exibição

**Data:** POC
**Passo do SDD:** 00
**Tipo:** revision

**Decisão tomada:**
Usar ordem por offset como aproximação da ordem narrativa na POC.

**Razão:**
A ordem real de exibição é controlada pelo script (ponteiros). Interpretar o script é mais custoso e
fica como próximo passo; para a cena de abertura, a ordem por offset coincide com a narrativa.

**Impacto:** sequência das linhas. **Revisão necessária:** sim, se a continuidade/contexto exigir ordem exata.
