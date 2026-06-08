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
- **Cabeçalho do container:** `"Filename    "` (12 bytes) + u32 (ptr p/ seção Pack) + array de u32
  (offsets dos nomes) + tabela de **nomes** (registros de 15 bytes `CC_SS_NNNT.BIN`).
- **Seção Pack:** `"Pack        "` (12 bytes) + u32 (tamanho) + u32 `count` + `count`×(u32 offset,
  u32 size) **interleaved**. Offsets contíguos do início ao fim do arquivo. **353 scripts** (caps. 11–39).
- **Layout por script:** `[bytecode 'STSC' + opcodes][bloco de texto: strings null-terminated]`. O
  bloco de texto de cada script está em **ordem de armazenamento = ordem narrativa** (verificado na abertura).
- **Pool de texto reusado:** a mesma string pode ser referenciada por vários scripts (ponteiros `50 00`).
- **Base de offset:** absoluta (offset do arquivo). O `id_column` (`offset` hex) é o endereço real.
- **Parsing canônico:** ver `connector/sdat_format.py` (`parse_pack`, `extract_text_block`) — módulo
  único compartilhado por `extract.py` e `reinsert.py`.

## SEÇÃO 4 — PONTEIROS

- **Modelo:** **não há tabela central de ponteiros.** As falas são referenciadas inline no bytecode
  pelo **opcode de texto `50 00`** (uint16 LE = 0x0050) **seguido de um uint32 LE que é um offset
  RELATIVO ao início do ARQUIVO (Pack) que contém o ponteiro.**
  - Endereço absoluto da string = `file_start_do_site + uint32`.
  - Ex. (file0 começa em `0x2568`): `50 00 | 30 0e 00 00` → `0x2568 + 0xe30 = 0x3398` ("Ngh... ghh...").
- ⚠️ **NÃO é absoluto.** Verificado empiricamente: dos ~47k sites `50 00`, **~42.101** só apontam para
  uma string quando lidos como file-relativos vs **~63** como absolutos (coincidência). Tratar como
  absoluto faz o jogo ler o endereço errado. (Travado pelo teste `test_pointer_model_is_file_relative`.)
- **Strings não cruzam arquivos:** um ponteiro file-relativo só endereça dentro do próprio script.
- **Entrada de bloco:** o 1º `50 00`+rel32 de um script aponta a 1ª string do seu bloco de texto.
- **Heads vs. continuações:**
  - *Head* = string com ≥1 referência `50 00`+rel32. (No corpus testado, quase toda linha é head.)
  - *Continuação* = string sem ponteiro próprio, lida em sequência após o head. **run** = head +
    continuações, até o próximo head.
- **Filtro anti-falso-positivo:** indexar `target_abs = file_start + uint32` e validar que aponta para
  um início de string real (descarta `50 00` aleatórios no bytecode).

### Estratégia de reinserção (cascata determinística)

- **T1 in_place:** `len(bytes) ≤ byte_budget` → grava no slot original.
- **Repoint (run):** se qualquer membro de um run estoura → **reloca o run inteiro** (head +
  continuações) para o **fim do arquivo** e reescreve cada ponteiro `50 00`+rel32 do head com o valor
  **`novo_offset − file_start_do_site`** (mantém a semântica file-relativa). Continuações viajam contíguas.
- **T4 resíduo:** caso irredutível → issue para o Passo 06c. (Com o modelo file-relativo, tudo é
  repointável → resíduo = 0 no corpus testado.)

> ⚠️ **Pendente de validação in-game:** a relocação grava no fim do arquivo (offset file-relativo grande).
> Se o engine limitar a leitura ao `size` declarado do arquivo no Pack, strings relocadas além desse
> tamanho podem não exibir. Confirmar com um patch de 1 linha relocada antes de produção.

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO (pt-BR)

**Veredito: a fonte do jogo NÃO renderiza diacríticos** (evidência in-game: `artifacts/char1.png`,
`char2.png` — pangrama pt-BR sai como `@`).

```
á é í ó ú  â ê ô  ã õ  ç  (e maiúsculas)  -> AUSENTES na fonte (renderizam como '@')
```

**Decisão:** **transliteração na gravação** (NFKD + descarte de combining marks; `ç→c`). A tradução
canônica (`approved_translations.csv`) permanece com acento (correta para QA); só os bytes gravados
no jogo são dobrados para ASCII. Registrado no `decision_log.md`.
