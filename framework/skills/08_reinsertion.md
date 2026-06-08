# SKILL 08 — REINSERTION
## Devolver a tradução ao meio (via conector) — patch de custo ótimo

> **Quando usar:** Após o QA Final (Passo 07) aprovar. Fecha o ciclo: aplica o
> `approved_translations.csv` ao binário e grava a saída em `output/`, preservando nome e extensão do input.

---

## OBJETIVO

Gerar o binário traduzido (e um patch distribuível) de forma **determinística**, gastando LLM apenas
no resíduo irredutível de overflow. O `reinsert.py` é **executado como ferramenta** — não refeito a
cada vez.

> **Governança de script (vale p/ todo script do conector):** se `reinsert.py` **não existir**, a IA
> **alerta** ("o script de reinserção ainda não existe") e **só o cria com permissão** do usuário
> (a partir de `framework/connectors/_skeleton/reinsert.py`). Se **existir**, a IA **apenas o executa** —
> nunca grava bytes à mão. Só reescrever o script se o formato do binário mudar.

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

- `approved_translations.csv` (traduções aprovadas: `id_column`, `text_target`)
- `dialogs.csv` (source) + binário-fonte (read-only) + `table_schema`
- `project.json` (bloco `connector`: `space_strategy`, `patch_format`, `pointer_table`)
- `qa_report.md` (aprovado)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `approved_translations.csv` | Existe; traduções aprovadas; cada `id_column` casa com `dialogs.csv` |
| `qa_report.md` | Status: aprovado (0 issues críticos) |
| Gate de round-trip (Passo 00) | Passou (byte-idêntico) |
| `connector` | `space_strategy` e `patch_format` declarados |
| `reinsert.py` | Existe — ou pedir permissão para criar (ver governança acima) |

❌ **Se o QA não aprovou ou o round-trip não passou: PARAR. Não reinserir tradução não-validada.**

---

## CASCATA DE ENCAIXE (determinística primeiro — só sobe quem falha)

Para cada string traduzida, `reinsert.py` aplica:

- **T1 — Escrita direta:** `len(encoded) ≤ byte_budget` → grava. Zero LLM. *(maioria absoluta)*
- **T2 — Recuperação de espaço:** repointing (se `space_strategy: repoint`); reuso de espaço de
  strings que encolheram; tabela de abreviações seguras. Zero LLM.
- **T3 — Trim mecânico:** colapsar espaços duplos, reticência tipográfica (…), abreviações do
  glossário do projeto. Zero LLM.
- **T4 — Reescrita por LLM (resíduo):** as strings que ainda estouram são **exportadas em lote** pelo
  `reinsert.py` para `artifacts/t4_residue.json` (`offset`, `text_source`, `current_target`,
  `byte_budget`, `over_by`). A IA reescreve as K strings em **uma única passada** para caber, devolve
  no `translation_plan.json` (`base_translation`), o conjunto é aprovado e **reaplicado pelo fluxo
  normal** (`poc_pipeline → approved → reinsert`). O resultado **volta pelo Micro-QA (06b)**.
  *(Quando a estratégia de espaço reloca o overflow — ex.: relocação intra-arquivo — o resíduo tende a
  0 e o lote sai vazio.)*

> Nunca uma chamada de LLM por string. Nunca LLM escrevendo bytes ou recalculando ponteiros.

---

## TAREFAS

1. **Escrever / adaptar `reinsert.py`** (encode, cascata T1–T3, emissão de patch).
2. **Recodificar** cada `text_target` via tabela; tokens → control codes.
3. **Aplicar a cascata**; coletar o resíduo T4.
4. **Resolver o resíduo T4** em chamada LLM única; re-validar no 06b; re-gravar.
5. **Gravar** o binário traduzido em `output/<nome-original>` — **mesmo nome e extensão do input**
   (ex: `<nome>.sdat` → `output/<nome>.sdat`). Nunca sobre o original-fonte.
6. **Emitir o patch** no `patch_format` declarado (ips / bps / xdelta).
7. **Verificar:** byte-space respeitado por string? ponteiros consistentes? build abre e renderiza?
8. **Informar o usuário** o diretório de saída ao final (caminho do arquivo gerado).

---

## SAÍDA — pasta `output/`

O arquivo final fica em **`projects/<título>/output/<nome-original>`**, com **nome e extensão do
input preservados** (`.sdat` de entrada → `.sdat` de saída). É o que o usuário pega para repatchar o
jogo. O script **informa o caminho** ao concluir.

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `connector/reinsert.py` (na instância) | Reinseridor determinístico do projeto |
| `output/<nome-original>` | Binário traduzido (mesma extensão do input), pronto para repatch |
| `output/patch.<fmt>` | Patch padrão (ips/bps/xdelta) para distribuição |
| `reinsertion_report.md` | Tier por string, overflows, repoints, falhas |

---

## REGRAS CRÍTICAS

- **Reinserção é determinística.** LLM só na cascata T4, em lote, e o resultado passa pelo 06b.
- **A IA executa o `reinsert.py`; não grava bytes à mão.** Criar o script só com permissão (governança acima).
- **Nunca sobrescrever o binário-fonte em disco** — saída em `output/`, nome e extensão preservados.
- **Informar o diretório de saída** ao usuário ao final.
- Strings que falham mesmo após T4 → issues no `reinsertion_report.md`, voltam para o ciclo 06c/07.
- Reinserção sem QA aprovado e sem round-trip é proibida.
