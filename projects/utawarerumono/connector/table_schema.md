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
- **DOIS opcodes de ponteiro (mesmo formato file-relativo):**
  - **`50 00`** = exibição de **DIÁLOGO** (a fala).
  - **`53 00`** = **RÓTULO DE FALANTE** (o nome exibido na caixa, ex.: `Girl`, `Woman`, `Man`). É
    file-relativo igual ao `50 00`; um rótulo é referenciado por vários sites `53 00` (um por fala
    daquele falante). Os rótulos são strings curtas e **só** têm ponteiros `53 00` (sem `50 00`).
  - O conector indexa e **repointa AMBOS** (`POINTER_OPCODES` em `sdat_format.py`): senão um rótulo que
    cresce na tradução (`Girl`→`Garota`) reloca mas o nome segue em inglês. (Travado por `test_label_pointers_53`.)
- **Strings não cruzam arquivos:** um ponteiro file-relativo só endereça dentro do próprio script.
- **Entrada de bloco:** o 1º `50 00`+rel32 de um script aponta a 1ª string do seu bloco de texto.
- **Derivação de speaker:** o falante de cada fala = o rótulo do `53 00` mais próximo antes do seu
  `50 00` (usado para reconciliar a metadata `speaker` com o que o jogo exibe).
- **Heads vs. continuações:**
  - *Head* = string com ≥1 referência `50 00` **ou** `53 00`. (No corpus testado, quase toda linha é head.)
  - *Continuação* = string sem ponteiro próprio, lida em sequência após o head. **run** = head +
    continuações, até o próximo head.
- **Filtro anti-falso-positivo:** indexar `target_abs = file_start + uint32` e validar que aponta para
  um início de string real (descarta `50 00` aleatórios no bytecode).

### Estratégia de reinserção (cascata determinística) — Plano B (relocação INTRA-ARQUIVO)

- **T1 in_place:** `len(bytes) ≤ byte_budget` → grava no slot original.
- **RELOC intra-arquivo (run):** se qualquer membro de um run estoura → **reloca o run inteiro** (head +
  continuações) para o **FIM da região do PRÓPRIO arquivo**; o arquivo **cresce** (e o `size` na tabela
  Pack é reescrito por `sdat_format.rebuild_container`, com todos os offsets recalculados e padding a 16
  bytes). Cada ponteiro `50 00`+rel32 do head é reescrito com o valor **`offset_local_no_arquivo`**
  (= `novo_offset − file_start`). Continuações viajam contíguas → ordem preservada.
- **T4 resíduo:** caso irredutível (overflow sem head) → issue para o Passo 06c. (Com o modelo
  file-relativo, tudo é repointável → resíduo = 0 no corpus testado.)

> ⚠️ **EOF-append (fim do CONTAINER) foi REPROVADO in-game** (`artifacts/Fasea*.png`): o engine carrega
> cada arquivo do `.sdat` num buffer próprio dimensionado pelo `size` do Pack, então texto além do `size`
> vira `@@@@` e trava o jogo. Por isso a relocação é **dentro do arquivo** + **reescrita do Pack** (o
> texto fica dentro do `size` declarado). Ver `decision_log.md` → "GATE IN-GAME". Travado pelos testes
> `test_planob_within_file` e `test_pack_rebuild_integrity`.

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO (pt-BR)

**Veredito: a fonte do jogo NÃO renderiza diacríticos** (evidência in-game: `artifacts/char1.png`,
`char2.png` — pangrama pt-BR sai como `@`).

```
á é í ó ú  â ê ô  ã õ  ç  (e maiúsculas)  -> AUSENTES na fonte (renderizam como '@')
```

**Decisão:** **transliteração na gravação** (NFKD + descarte de combining marks; `ç→c`). A tradução
canônica (`approved_translations.csv`) permanece com acento (correta para QA); só os bytes gravados
no jogo são dobrados para ASCII. Registrado no `decision_log.md`.
