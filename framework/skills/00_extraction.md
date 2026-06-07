# SKILL 00 — EXTRACTION
## Extrair o corpus do meio de armazenamento (via conector)

> **Quando usar:** No começo absoluto do projeto, **antes do Discovery**. Transforma o binário da
> obra (fornecido pelo humano) no corpus canônico (`dialogs.csv`) que todo o resto do pipeline consome.

---

## OBJETIVO

Produzir o `dialogs.csv` de forma **determinística e auditável** a partir do meio de armazenamento,
usando o conector declarado em `project.json → connector`. Nenhuma tradução nem análise cognitiva
acontece aqui — é extração mecânica.

> A IA **escreve o `extract.py`** do projeto (a partir de `framework/connectors/_skeleton/extract.py`),
> guiada pelo contrato em `framework/connectors/<connector.type>.md`. O humano fornece o binário.

---

## INPUTS

- `project.json` (com bloco `connector` válido)
- O binário-fonte (`connector.source_binary`) — fornecido pelo humano
- O schema de tabela (`connector.table_schema`)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `project.json` | Existe; bloco `connector` presente e válido (ver `schemas/project_schema.md`) |
| Binário-fonte | Arquivo presente em `connector.source_binary` |
| `table_schema` | Existe; mapa de caracteres + control codes definidos |

❌ **Se faltar binário ou tabela: PARAR. Sem o meio e a tabela não há extração.**

---

## TAREFAS

### 1. Escrever / adaptar o `extract.py`
A partir do esqueleto, implementar para o formato real do binário: parser da tabela, decodificação
de string, localização por ponteiro/varredura. Determinístico — nunca LLM.

### 2. Extrair o corpus
Rodar `extract.py`. Para cada string: decodificar via tabela, mapear control codes → tokens, registrar
o offset como `id_column`.

### 3. Registrar o byte budget (SHIFT-LEFT)
Para cada string, gravar `byte_budget` = nº de bytes que ela ocupa no binário. **Este campo é o que
permite a tradução caber na 1ª passada (Passo 06) e evita custo de LLM na reinserção.** Não omitir.

### 4. Gate de charset do idioma-alvo
Verificar se a fonte/tabela do jogo representa os caracteres do `target_language` (ex: ã, ç, õ).
- Todos representáveis → seguir.
- Faltam glifos → registrar `target_charset_supported: false` e decidir (expandir fonte vs transliterar)
  no `decision_log.md`. **Bloquear** tradução fiel até resolver.

### 5. Gate de round-trip (prova de correção)
Rodar `extract.py` → `reinsert.py` (sem traduzir nada) → comparar com o binário original.

```
extract(binário) → dialogs.csv → reinsert(dialogs.csv) → binário'
binário' === binário  (byte-a-byte)
```

❌ **Se não for byte-idêntico: o conector perde informação. BLOQUEAR o pipeline até corrigir os scripts.**

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `connector/extract.py` (na instância) | Extrator determinístico do projeto |
| `dialogs.csv` | Corpus canônico: `id_column`, `text_source`, `byte_budget` |
| `extraction_log.md` | Tabela usada, encoding, mapa de control codes, total de strings, offsets cobertos |

---

## REGRAS CRÍTICAS

- **Determinístico, sempre.** Nenhum LLM no caminho de extração.
- **`byte_budget` é obrigatório** em cada linha — é a base do shift-left.
- **Round-trip é gate**: sem round-trip byte-idêntico, o pipeline não avança.
- O binário-fonte é **somente leitura** — nunca modificado por este passo.
- `dialogs.csv` é um **output deste passo**, não um dado pré-existente. O Discovery (Passo 01) o consome.
