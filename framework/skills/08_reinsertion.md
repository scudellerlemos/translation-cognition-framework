# SKILL 08 — REINSERTION
## Devolver a tradução ao meio (via conector) — patch de custo ótimo

> **Quando usar:** Após o QA Final (Passo 07) aprovar. Fecha o ciclo: grava o `translated.csv` de
> volta no binário, sobrescrevendo o idioma-fonte pelo idioma-alvo, e emite o patch.

---

## OBJETIVO

Gerar o binário traduzido e um patch distribuível, de forma **determinística**, gastando LLM apenas
no resíduo irredutível de overflow. A IA **escreve o `reinsert.py`** do projeto (a partir de
`framework/connectors/_skeleton/reinsert.py`).

---

## PRINCÍPIO DE CUSTO

| Operação | Método | Custo LLM |
|----------|--------|-----------|
| Detectar se cabe | encode + contar bytes vs `byte_budget` | zero |
| Escrever bytes, mapear tokens, ponteiros, patch | `reinsert.py` | zero |
| Fazer caber (cascata T1–T3) | determinístico | zero |
| Reescrever resíduo T4 | 1 chamada LLM **em lote** | mínimo |

O grosso do encaixe já foi resolvido no **shift-left** (Passo 06 traduziu dentro do `byte_budget`),
então o resíduo T4 tende a ser pequeno.

---

## INPUTS

- `translated.csv` (100% preenchido)
- `project.json` (bloco `connector`: `space_strategy`, `patch_format`, `pointer_table`)
- `table_schema` + binário-fonte
- `qa_report.md` (aprovado)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `translated.csv` | Todas as linhas com `text_target` preenchido |
| `qa_report.md` | Status: aprovado (0 issues críticos) |
| Gate de round-trip (Passo 00) | Passou (byte-idêntico) |
| `connector` | `space_strategy` e `patch_format` declarados |

❌ **Se o QA não aprovou ou o round-trip não passou: PARAR. Não reinserir tradução não-validada.**

---

## CASCATA DE ENCAIXE (determinística primeiro — só sobe quem falha)

Para cada string traduzida, `reinsert.py` aplica:

- **T1 — Escrita direta:** `len(encoded) ≤ byte_budget` → grava. Zero LLM. *(maioria absoluta)*
- **T2 — Recuperação de espaço:** repointing (se `space_strategy: repoint`); reuso de espaço de
  strings que encolheram; tabela de abreviações seguras. Zero LLM.
- **T3 — Trim mecânico:** colapsar espaços duplos, reticência tipográfica (…), abreviações do
  glossário do projeto. Zero LLM.
- **T4 — Reescrita por LLM (resíduo):** as strings que ainda estouram são coletadas e enviadas em
  **uma única chamada em lote** ("reescreva estas K strings para caber em seus `byte_budget`,
  preservando tom e entidades"). O resultado **volta pelo Micro-QA (06b)** e é re-gravado por T1.

> Nunca uma chamada de LLM por string. Nunca LLM escrevendo bytes ou recalculando ponteiros.

---

## TAREFAS

1. **Escrever / adaptar `reinsert.py`** (encode, cascata T1–T3, emissão de patch).
2. **Recodificar** cada `text_target` via tabela; tokens → control codes.
3. **Aplicar a cascata**; coletar o resíduo T4.
4. **Resolver o resíduo T4** em chamada LLM única; re-validar no 06b; re-gravar.
5. **Gravar** o binário traduzido (cópia/patch — nunca sobre o original-fonte).
6. **Emitir o patch** no `patch_format` declarado (ips / bps / xdelta).
7. **Verificar:** byte-space respeitado por string? ponteiros consistentes? build abre e renderiza?

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `connector/reinsert.py` (na instância) | Reinseridor determinístico do projeto |
| `translated_build.bin` (ou equivalente) | Binário com a tradução gravada |
| `patch.<fmt>` | Patch padrão (ips/bps/xdelta) para distribuição |
| `reinsertion_report.md` | Tier por string, overflows, repoints, falhas |

---

## REGRAS CRÍTICAS

- **Reinserção é determinística.** LLM só na cascata T4, em lote, e o resultado passa pelo 06b.
- **Nunca sobrescrever o binário-fonte em disco** — gerar cópia + patch.
- Strings que falham mesmo após T4 → issues no `reinsertion_report.md`, voltam para o ciclo 06c/07.
- O patch é a entrega: não exige redistribuir o jogo original.
- Reinserção sem QA aprovado e sem round-trip é proibida.
