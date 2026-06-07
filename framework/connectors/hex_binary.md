# CONECTOR — hex_binary
## Conector para jogos antigos (texto embutido em binário, estilo HxD)

> **Status:** definido. Instância de referência: Utawarerumono.
> Este documento é o **contrato** dos scripts `extract.py` / `reinsert.py`. Não contém código
> específico de jogo — esse código é escrito pela IA por projeto, a partir do esqueleto em
> `_skeleton/`, e vive em `projects/<título>/connector/`.

---

## QUANDO USAR

O texto da obra está embutido em um **arquivo binário** e só é legível com um **hex editor** (HxD)
mais uma **tabela de caracteres** (byte→glifo). Cada string é endereçada por **offset** e
referenciada por **ponteiros**. É o caso clássico de jogos de console antigos / ROMs.

---

## O SCHEMA DE TABELA (coração do conector)

Um único `table_schema` (ver `_skeleton/table_schema.md`) é compartilhado por extração e reinserção.
Ele define:
- **Mapa byte→caractere** (e o inverso caractere→byte)
- **Control codes:** sequências de bytes que viram tokens (`{W75}`, `{END}`, quebra de linha, cor)
- **Terminadores** de string
- **Encoding** (largura fixa, variável, custom)

Manter o schema estável é o que garante o round-trip. Extração e reinserção **nunca** divergem na tabela.

---

## CONTRATO: `extract.py`

```
extract.py(source_binary, table_schema) → dialogs.csv + extraction_log.md
```

**Determinístico.** Para cada string localizada no binário:
1. Ler bytes a partir do offset até o terminador
2. Decodificar via tabela (byte→caractere)
3. Substituir sequências de control code pelos tokens correspondentes
4. Registrar a linha em `dialogs.csv` com:
   - `<id_column>` = offset (hex)
   - `text_source` = texto decodificado
   - `byte_budget` = nº de bytes que a string ocupa no binário (**shift-left** — ver Passo 06)
5. Acumular metadados em `extraction_log.md` (tabela usada, encoding, mapa de control codes, total de strings, offsets cobertos)

---

## CONTRATO: `reinsert.py`

```
reinsert.py(translated.csv, table_schema, source_binary) → binário traduzido + patch + reinsertion_report.md
```

**Determinístico.** Para cada string traduzida:
1. Recodificar `text_target` via tabela (caractere→byte)
2. Substituir tokens pelas sequências de control code
3. Aplicar a **cascata de encaixe** (abaixo)
4. **Sobrescrever** os bytes do idioma-fonte pelos do idioma-alvo, conforme `space_strategy`
5. Emitir o binário traduzido **e** um patch (`patch_format`: ips / bps / xdelta)
6. Registrar overflows, repoints e falhas em `reinsertion_report.md`

> O original-fonte nunca é sobrescrito em disco: gera-se cópia/patch.

---

## CASCATA DE ENCAIXE (custo crescente — só sobe quem falha)

A reinserção precisa caber a tradução no espaço disponível. Resolver do mais barato ao mais caro:

| Tier | Método | Custo LLM |
|------|--------|-----------|
| **T1** | **Escrita direta** — cabe no byte-space → grava | zero *(maioria)* |
| **T2** | **Recuperação de espaço** — repointing (se permitido); reuso de espaço de strings que encolheram; tabela de abreviações seguras | zero |
| **T3** | **Trim mecânico** — colapsar espaços duplos, reticência tipográfica (…), abreviações do glossário do projeto | zero |
| **T4** | **Reescrita por LLM** — só o resíduo, numa **única chamada em lote**; volta pelo Micro-QA (06b) | mínimo |

A maior parte do custo já foi eliminada no **shift-left** (orçamento de bytes na tradução, Passo 06),
então T4 tende a processar pouquíssimas strings.

---

## ESTRATÉGIA DE ESPAÇO (`space_strategy`)

| Valor | Significado | Restrição de comprimento |
|-------|-------------|--------------------------|
| `in_place` | A tradução é gravada no mesmo slot de bytes da original | Limite **em bytes** (`byte_budget`) — não % de caracteres |
| `repoint` | Ponteiros são recalculados; a tradução pode crescer | Limitada pelo espaço total realocável |

Quando `in_place`, o `length_constraints` do `project.json` opera em **modo byte-space**.

---

## FONTE / GLIFOS DO IDIOMA-ALVO (gate de charset)

A fonte do jogo pode não ter os glifos do idioma-alvo (pt-BR: ã, ç, õ, á, ê...). Antes de traduzir:

- `extract.py` (ou um self-check do conector) verifica se cada caractere do alvo é representável pela tabela/fonte.
- Se **não**: `target_charset_supported: false` → **AVISO/BLOQUEIO** documentado. Opções: expandir a
  fonte/tabela (adicionar glifos) ou definir transliteração determinística de fallback (ã→a, ç→c...).
- A escolha vira entrada no `decision_log.md`.

---

## PONTEIROS

- `pointer_table` no `project.json` declara onde está e o formato (ex: little-endian 16-bit relativo à base).
- Em `space_strategy: repoint`, `reinsert.py` recalcula cada ponteiro deterministicamente após gravar as strings.
- Recalcular ponteiros é **aritmética** — nunca usar LLM para isso.

---

## CHECKLIST DE CONFORMIDADE DO CONECTOR

```
□ extract.py e reinsert.py consomem o MESMO table_schema?
□ extract.py emite byte_budget por string?
□ Round-trip (extract → reinsert idêntico === original) passa byte-a-byte?
□ Control codes mapeiam para os formatting_tokens do project.json?
□ space_strategy declarada e length_constraints em modo byte-space se in_place?
□ Gate de charset avaliado (target_charset_supported)?
□ Saída inclui o patch no patch_format declarado?
```
