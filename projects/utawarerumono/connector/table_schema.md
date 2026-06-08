# Table Schema — Utawarerumono: Mask of Deception (ENG/Steam)
## ScriptEvent.sdat — formato descoberto por engenharia reversa (POC)

> Formato definido em `framework/connectors/_skeleton/table_schema.md`. Este arquivo é consumido
> por `extract.py` E `reinsert.py` — mantê-lo único e estável garante o round-trip.

---

## SEÇÃO 1 — MAPA DE CARACTERES (byte → caractere)

- **Encoding:** UTF-8 (texto armazenado diretamente como UTF-8; não há tabela byte→glifo custom).
- **Largura:** variável (UTF-8).
- O texto exibível é ASCII/UTF-8 legível; nenhum remapeamento é necessário na extração.

## SEÇÃO 2 — CONTROL CODES (bytes → token)

Os control codes são armazenados como **tokens ASCII literais** dentro da própria string
(ex.: os bytes `{`, `W`, `7`, `5`, `}`). Não há bytes de controle binários a mapear.

```
{W75}  -> literal "{W75}"   (5 bytes ASCII)
{W80}  -> literal "{W80}"
{W10}  -> literal "{W10}"
{COLOR}-> literal "{COLOR}"
{END}  -> literal "{END}"
\n     -> literal "\n"       (2 bytes ASCII: 0x5C 0x6E)
```

## SEÇÃO 3 — TERMINADORES E ESTRUTURA

- **Terminador de string:** `0x00` (null). Strings são **contíguas** no bloco de texto.
- **Cabeçalho do container:** `"Filename    "` (12 bytes) + índice de arquivos de script
  (`NN_NN_NNNS.BIN`, registros de 15 bytes). Esse índice **não** referencia falas de diálogo.
- **Bloco de texto:** inicia em `0x3398` (primeira fala da cena de abertura).
- **Base de offset:** absoluta (offset do arquivo). O `id_column` (`offset` hex) é o endereço real.

## SEÇÃO 4 — PONTEIROS

- **Modelo:** **não há tabela central de ponteiros.** As falas são referenciadas inline no bytecode
  de script pelo **opcode de texto `50 00`** (uint16 LE = 0x0050) **seguido de um ponteiro absoluto
  uint32 LE** para o início da string.
  - Ex.: `50 00 | 98 33 00 00` → exibe a string em `0x3398`.
- **Localização:** espalhada por todo o arquivo (múltiplos script files referenciam a mesma string).
- **Formato:** `uint32 LE`, offset **absoluto** no arquivo, precedido por `50 00`.
- **Heads vs. continuações:**
  - *Head* = string com ≥1 referência `50 00`+ptr.
  - *Continuação* = string sem ponteiro próprio, lida em sequência logo após o head (mesma "página"
    de texto). Um **run** = head + suas continuações, até o próximo head.
- **Filtro anti-falso-positivo:** localizar ponteiros como `50 00`+`uint32(offset)` (não o uint32
  cru), o que descarta sequências de 4 bytes que casam o valor por acaso.

### Estratégia de reinserção (cascata determinística)

- **T1 in_place:** `len(bytes) ≤ byte_budget` → grava no slot original.
- **Repoint (run):** se qualquer membro de um run estoura → **reloca o run inteiro** (head +
  continuações) para o **fim do arquivo** e reescreve **todos** os ponteiros `50 00`+ptr do head para
  o novo endereço. As continuações viajam contíguas → a leitura sequencial é preservada.
- **T4 resíduo:** caso irredutível (sem ponteiro e sem como caber) → issue para o Passo 06c.

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO (pt-BR)

**Veredito: a fonte do jogo NÃO renderiza diacríticos** (evidência in-game: `artifacts/char1.png`,
`char2.png` — pangrama pt-BR sai como `@`).

```
á é í ó ú  â ê ô  ã õ  ç  (e maiúsculas)  -> AUSENTES na fonte (renderizam como '@')
```

**Decisão:** **transliteração na gravação** (NFKD + descarte de combining marks; `ç→c`). A tradução
canônica (`approved_translations.csv`) permanece com acento (correta para QA); só os bytes gravados
no jogo são dobrados para ASCII. Registrado no `decision_log.md`.
