# TABLE SCHEMA — Trails in the Sky 2nd Chapter (remake Falcom, 2026)

> Fase 0 **concluída em 2026-08-23**. Duas camadas de formato: contêiner FPAC (mapeado, confirmado
> por bytes reais) e script interno `scena/*.dat` em formato `#scp` (header confirmado via
> desmontagem de `sora_2nd.exe` no Ghidra; mecanismo de nome→label e a cadeia de dispatch por
> vtable foram resolvidos e decompilados, mas confirmaram pertencer ao subsistema de batalha, sem
> relação com diálogo — ver "RETOMADA #3" na Camada 1). Critério de conclusão: os dois formatos
> necessários pro conector (contêiner FPAC + heurística de extração de string em `#scp`) estão
> mapeados, confirmados e em produção (Fase 1); a via de bytecode/VM foi investigada até o ponto
> de confirmar que não é necessária nem aplicável a diálogo — decisão final, não pausa.

Fonte usada para o mapeamento: `pac/steam/script_en.pac` da demo Steam
(`Trails in the Sky 2nd Chapter Demo`). Ainda não temos o jogo completo — apenas a demo.

---

## CAMADA 0 — Contêiner FPAC (mapeado e confirmado)

`discover.py` classificou como `unknown_engine` (não está no `connector_registry.json`), mas o
formato do contêiner já está publicamente documentado (projeto `FPACker`,
https://github.com/coinkillerl/FPACker — usado para Trails in the Sky 1st/2nd Chapter e Kuro no
Kiseki: Kyoto Xanadu) e **confirmado byte a byte** contra `script_en.pac`, `script.pac` e
`table_en.pac` nesta sessão.

### Header (16 bytes)

| Offset | Tamanho | Campo | Notas |
|---|---|---|---|
| 0x00 | 4 | magic | `"FPAC"` (`46 50 41 43`) |
| 0x04 | 4 (u32 LE) | file_count | ex: `script_en.pac` = 269, `table_en.pac` = 129 |
| 0x08 | 4 (u32 LE) | first_file_address | offset absoluto onde começam os DADOS do primeiro arquivo (depois da tabela de entradas + tabela de nomes) |
| 0x0c | 4 (u32 LE) | unknown_magic | sempre `1` nos 3 arquivos inspecionados |

### Tabela de entradas (32 bytes cada, começa em 0x10, `file_count` entradas)

| Offset (rel.) | Tamanho | Campo | Notas |
|---|---|---|---|
| 0x00 | 4 (u32 LE) | filename_crc32_xor | `crc32(nome_sem_null) XOR 0xFFFFFFFF` |
| 0x04 | 4 | padding | sempre `0` |
| 0x08 | 8 (u64 LE) | name_address | offset absoluto p/ string do nome, terminada em `\0` |
| 0x10 | 8 (u64 LE) | file_size | tamanho em bytes |
| 0x18 | 8 (u64 LE) | data_address | offset absoluto dos dados do arquivo |

- **Compressão:** nenhuma (confirmado — dados legíveis diretamente).
- **Ordenação:** por `filename_crc32` ascendente (não importa para extração, só para reempacotamento).
- Entradas relevantes em `script_en.pac`: subpastas `scena/` (script/diálogo — o alvo),
  `ani/`, `ai/`, `battle/` (dados de animação/IA/batalha — fora de escopo de tradução).

**Parser de referência (validado nesta sessão, stdlib puro — `struct`):**
```python
magic, count, first_addr, unk = struct.unpack_from("<4sIII", data, 0)  # magic == b"FPAC"
off = 16
for i in range(count):
    crc, pad, name_addr, size, data_addr = struct.unpack_from("<IIQQQ", data, off)
    off += 32
    name = data[name_addr:data.index(b"\x00", name_addr)].decode("ascii")
```

---

## CAMADA 1 — Script interno `scena/*.dat` (formato `#scp`) — NÃO MAPEADO

Cada arquivo relevante (ex: `script_en/scena/e2000.dat`, `mp2010_10.dat`, `mp0000_ev.dat`) começa
com o magic `#scp` (`23 73 63 70`) seguido de bytecode binário. Diálogo em inglês aparece como
**ASCII plano, sem compressão nem criptografia** misturado com o bytecode (confirmado via scan de
strings), incluindo ao menos um token de controle visível: `<C1>...`.

Exemplo real de string extraída de `e2000.dat` (offset dentro do blob, não mapeado ainda):
```
Our story begins in Rolent, in the kingdom of Liberl.
<C1>Obtained ... as a reward for Estelle's final level (100 or higher)!
sound.PlayBGM
OnMapReinit
```

### Header confirmado via Ghidra (2026-08-23) — desmontagem de `sora_2nd.exe`

Achamos a função que valida o magic `#scp` e inicializa a struct em runtime, via busca por
xref ao byte pattern `#scp` no executável (`sora_2nd.exe`, Ghidra headless + decompilador).
Único hit: `CMP dword ptr [RDX],0x70637323` em `FUN_1405dab70` (chamada por `FUN_1404c9cd0`).

Decompilado (assinatura): `FUN_1405dab70(struct *self, uint32_t *file_buf, uint32_t param_3, char *name)`

Layout do header confirmado (todos u32 LE), cruzado contra `e2000.dat` real:

| Offset | Campo | Valor em e2000.dat | Uso confirmado no código |
|---|---|---|---|
| 0x00 | magic | `0x70637323` ("#scp") | comparação direta |
| 0x04 | header[1] | `0x18` (24) | vira `self->field_0x38 = header[1] + file_base` — um cursor/offset armazenado na struct em runtime, ainda não confirmado se é lido de volta como offset de string |
| 0x08 | header[2] | `0x2a` (42) | **não referenciado nesta função** — candidato a contagem de um array de records de 32 bytes que começa em 0x20 (ver abaixo) |
| 0x0c | header[3] | `0x318c` (12684) | vira `self->field_0x40 = header[3] + file_base`; só é processado (malloc de tabela auxiliar) se header[4] != 0 |
| 0x10 | header[4] | `0` em e2000.dat | contagem de entradas de 8 bytes na tabela apontada por header[3]; zero neste arquivo então o bloco não roda — provavelmente tabela de flags de voice-over (0x40000000 = "sem voz" / 0xc0000000 = "com voz" por entrada, visto no bytecode do loop) |

**Hipótese forte, não 100% confirmada**: array de records de **32 bytes** começando em offset
`0x20` (logo após o header de 0x14 bytes + 4 bytes de padding em 0x18–0x1f), possivelmente
`header[2]` (=42) entradas. Campos observados por record (3 primeiras entradas de `e2000.dat`):

```
offset  u32[0] u32[1] u32[2]  u32[3](offset?)  u32[4](hash?)  u32[5](flag 0xC00077xx)  u32[6](offset, +12/record)  u32[7]
0x20    0x558  0x5e8  0x98    0x718            0x3e5f3851     0xc00077c3               0x5be0                      0
0x40    0x558  0x5e8  0x01    0xe38            0x009e93cc     0xc00077d2               0x4275                      0
0x60    0x558  0x5e8  0x00    0xe44            0x3585e0ee     0xc00077e9               0x4281                      0
```

- u32[0]/u32[1] constantes (`0x558`, `0x5e8`) em todas as entradas vistas — provável ID de
  cena/bloco fixo por arquivo, não por linha.
- u32[6] cresce em passos de **+12 bytes** entre records consecutivos (0x4275 → 0x4281 → header[1]=0x428d
  seguiria o mesmo passo) — indício de que aponta pra um sub-array de registros de 12 bytes cada
  (possível timing/lipsync ou metadata por linha), não confirmado o conteúdo desses 12 bytes ainda.
- u32[5] com padrão `0xC00077xx` em todas as entradas — parece HRESULT-like ou hash, não offset.

### Cadeia de loading confirmada (2026-08-23)

Decompilado também `FUN_1404c9cd0` (o único caller de `FUN_1405dab70`). É a função genérica de
carregar um script: monta o path `"script/<nome>.dat"`, busca no cache de recursos
(`FUN_14043e930(DAT_140c5f208, path)` → retorna um "resource entry" `lVar2`), e então chama:

```c
FUN_1405dab70(scena_obj, *(void**)(lVar2 + 0x10), *(uint32_t*)(lVar2 + 0x18), name);
//             ^self      ^ponteiro pros bytes crus do .dat (já em memória)  ^tamanho do arquivo
```

Confirma que `param_2` de `FUN_1405dab70` é mesmo o buffer bruto do `.dat` carregado (não um
handle indireto) — os offsets de header mapeados acima (0x00/0x04/0x08/0x0c/0x10) são relativos
ao início real do arquivo em memória, sem camada extra de indireção do loader.

**Isto é só o parser do header/constructor — ainda não achamos o interpretador de bytecode que
lê `self->field_0x38`/`self->field_0x40` depois de inicializados** (esses devem ser os ponteiros
que a VM usa pra buscar strings/records durante a execução da cena). Esse é o próximo alvo, mas
exige achar as funções que recebem esse objeto "scena" já carregado e dereferenciam esses campos
— não é mais uma busca de xref única e simples como o magic check foi.

### Achado: funções de scena são invocadas por nome via vtable (2026-08-23)

Rastreando o array de scena_objs pré-carregados (`ScriptManager+0x11600`, preenchido por
`FUN_1404c9800`, ordem fixa: `scena/system`=0, `scena/system2`=1, `scena/sound`=2,
`scena/npc_setting`=3, `scena/sys_event`=4, `scena/talk_common`=5, mais `ani/*`, `obj/*`,
`battle/btlsys`), achamos `FUN_14025ef60`, que lê o scena_obj do índice 0 (`scena/system`) e
chama:

```c
plVar2 = *(longlong **)(lVar3 + 0x11690);           // objeto "event manager" (outro singleton)
(**(code **)(*plVar2 + 0x10))(plVar2, uVar1, "OnEventFinalize", 0, 0);
//            ^vtable slot 2 (offset 0x10)            ^scena_obj  ^nome da função dentro da cena
```

Ou seja: **funções/labels dentro de um `#scp` são invocadas pelo motor por nome (string),
via dispatch virtual**, não por índice numérico direto. Isso é coerente com as strings de
identificador já vistas no dump de `e2000.dat` (`sound.PlayBGM`, `OnMapReinit`) — são nomes de
função/label referenciados por essa mesma via, não texto de diálogo.

**Ainda não resolvido**: qual é a classe concreta do "event manager" (`*(longlong*)(lVar3+0x11690)`)
e portanto qual função real está no slot 2 da vtable — isso exige achar o construtor que
inicializa esse objeto (grava seu ponteiro de vtable) pra resolver o dispatch virtual pra um
endereço concreto e decompilar a implementação de verdade (onde certamente está a lógica de
lookup de nome → e, por extensão, a de leitura de string de diálogo).

**Escopo em expansão**: o que era "achar 1 xref" virou "resolver uma cadeia de objetos com
dispatch virtual" — esforço bem maior que os passos anteriores. Ver decisão de estratégia com o
usuário antes de continuar essa linha.

### RETOMADA (2026-08-23, sessão seguinte) — mecanismo de nome→label RESOLVIDO

A pedido do usuário, RE de VM retomada. Progresso real, corrigindo/completando os achados acima:

**Correção**: `DAT_140c5f170` (referenciado pela nota anterior como offset `+0x11690` de "outro
singleton") é na verdade o singleton `sora::script::Manager` — confirmado por símbolo real no
binário (`sora::script::Manager::vftable`, atribuído no construtor `FUN_1400372e0`, que aloca
`0x11738` bytes). Não existe um segundo objeto "event manager" separado; offset `0x11690` dentro
desse singleton é um **pool de 11 slots de handler** (array de ponteiros, indexado por `id & 0xf`
em `FUN_1400ce0d0`/`FUN_1400ce1c0`), não um ponteiro único pra um objeto singular.

**`FUN_1400ce1c0`** (dispatcher de evento por nome, chamado por `FUN_14025ef60` pra invocar
`"OnEventFinalize"` — já mapeado na seção anterior) faz, nesta ordem:
1. `FUN_1405dad20(scena_obj, nome)` — resolve o nome dentro do `#scp` já carregado.
2. Se achou (retorno != 0): pega um slot livre do pool (`byte em slot+0x408 == 0`), grava o
   ponteiro/contexto do chamador nele, e invoca `(*slot->vtable[2])(slot, scena_obj_ptr, nome, ...)`
   — o mesmo slot vtable+0x10 já visto antes.

**`FUN_1405dad20(longlong *scena_obj, byte *nome)` — RESOLVIDA POR COMPLETO.** É a função de
lookup nome→label dentro de um `#scp` já carregado:

```c
longlong FUN_1405dad20(longlong *param_1, byte *param_2) {
    // param_1 = scena_obj (mesma struct inicializada por FUN_1405dab70)
    // param_2 = nome (C-string) a resolver, ex.: "OnEventFinalize"

    hash = nome vazio ? -1
           : FUN_14005b260(nome+1, TABELA_256[(byte)~nome[0]] ^ 0xffffff);
    // hash tipo CRC32 tabela-driven: 1º byte tratado à parte via tabela de 256 u32
    // (DAT_140a92940, endereço sugere tabela CRC32 padrão, NÃO extraída ainda),
    // resto do nome via função de continuação FUN_14005b260 (não decompilada ainda).

    count = *(uint*)(scena_obj_raw_buffer + 8);      // == header[2] (CONFIRMADO: é contagem, não "não referenciado" como a nota anterior registrava)
    base  = param_1[7];                               // == scena_obj+0x38 == header[1] + file_base (CONFIRMADO: é a base da tabela de records, não só um "cursor" genérico)

    for (i = 0; i < count; i++) {
        record = base + i*0x20;                        // CONFIRMA a hipótese de record de 32 bytes
        // record+0x1c: top 2 bits (0xC0000000/0x40000000, MESMO padrão de flag já visto na
        //   tabela de voice-over) = "tem nome embutido"; 30 bits baixos = offset (a partir do
        //   INÍCIO DO ARQUIVO, *param_1, não do header) até a C-string do nome deste record.
        // record+0x18: hash (mesmo algoritmo acima) do nome deste record.
        if (record.hash == hash) {
            if (strcmp(record.name_ptr, nome) == 0) return record;  // ponteiro pro record inteiro
        }
    }
    return 0;  // não encontrado
}
```

**Confirmações que substituem hipóteses antigas desta seção:**
- `header[2]` (42 em `e2000.dat`) É a contagem de records de 32 bytes — não "não referenciado",
  como a 1ª passada de RE havia registrado (só não é lido pelo *construtor*; é lido por esta
  função de lookup).
- `self->field_0x38` (`param_1[7]`) É a base da tabela de records de 32 bytes (`header[1] +
  file_base`) — CONFIRMADO como "lido de volta", resolvendo o "ainda não confirmado" do header.
- Padrão de flag `0xC0000000`/`0x40000000` é reusado em pelo menos 2 lugares (tabela de voz E
  offset de nome do record) — parece ser uma convenção geral do engine pra "ponteiro relativo
  válido vs. nulo", não algo específico de um subsistema.

**Ainda não resolvido** (próximo alvo, se continuar): os outros 24 bytes do record (offsets
`+0x00`..`+0x14`) não foram decodificados — candidato forte a conter o offset de entrada do
bytecode correspondente ao label (ou seja, o "onde pular quando o nome bate"), que é o dado que
efetivamente resolveria a extração de diálogo via bytecode em vez da heurística atual. `FUN_1405dad20`
tem 14 callers no binário total (só 1, `FUN_1400ce1c0`, investigado até aqui) — os outros 13 não
foram visitados, podem ser subsistemas não relacionados a diálogo (batalha, UI, etc.) ou podem
revelar outro consumidor do record que leia esses 24 bytes.

Ferramentas desta sessão: mesmo Ghidra project (`C:\re\ghidra_project\trails_sc`), scripts novos em
`C:\re\scripts\` (`DecompFull.java`, `FindOffset11690.java`, `Decomp11690.java`, `DecompLookup.java`).

### RETOMADA (2026-08-23, sessão seguinte #2) — `+0x10`/`+0x14` decodificados: tabela de parâmetros, NÃO offset de bytecode

Decompilados os 13 callers restantes de `FUN_1405dad20` (script `DecompCallers3.java`, mesma
convenção dos anteriores). Todos os 13 seguem o mesmo idioma já visto em `FUN_1400ce1c0`
(`"BattleStart"`, `"BattleEnd"`, `"BattleCommandBegin"`, `"BattleGameOver"`, `"NextBattle"`,
`"BattleDead"`, `"CheckAlgoUse"`, etc. — todos nomes de eventos de sistema de batalha, nenhum
relacionado a diálogo) e a maioria só testa `lVar = FUN_1405dad20(...); if (lVar != 0) { ... }`
sem tocar no conteúdo do record. **Duas exceções dereferenciam campos do record de verdade**:

- `FUN_14053abf0` (chamada por `FUN_1404ac480`, que por sua vez também chama `FUN_1405dad20`
  direto antes de delegar): `lVar7 = FUN_1405dad20(...)`, depois
  `uVar3 = *(uint *)(lVar7 + 0x10)` — usado como **contador**, e mais abaixo
  `puVar12 = (uint *)(*(uint *)(lVar7 + 0x14) + puVar11 * 0xc + *plVar4)` — ou seja `+0x14` é um
  **offset relativo ao buffer do arquivo** (mesma base `*plVar4`/`self->field_0x00` de sempre)
  pra um **array de registros de 12 bytes**, com `uVar3` entradas.
- Cada registro de 12 bytes desse array-de-parâmetros: `+0x04` (lido como `short`) é um
  **type tag** (comparado contra `3` no código visto); `+0x06` (`ushort`) é uma flag secundária
  que decide se o valor vem embutido ou de outro lugar; `+0x08` é um **valor com a mesma
  convenção de tag de 2 bits no topo** já vista em outros lugares do formato (`>>0x1e == 1` →
  inteiro de 30 bits com sign-extend via `(x*4)>>2`; `>>0x1e == 2` → float codificado via
  `(float)(x*4)`).

**Conclusão**: `+0x10` = **contagem de parâmetros** do label/evento, `+0x14` = **offset (relativo
ao buffer do arquivo) da tabela de descritores de parâmetro** (12 bytes cada: type tag + flag +
valor/offset tagueado). Isso resolve 8 dos 24 bytes que faltavam — mas **não é o offset de
bytecode** hipotetizado; é a assinatura/tipagem dos argumentos que o evento espera receber,
usada por quem invoca o handler (o slot 2 da vtable em `FUN_1400ce1c0`) para validar/converter
os argumentos antes de chamar.

**Ainda não resolvido**: os 16 bytes em `+0x00`..`+0x0c` continuam sem uso identificado — nenhum
dos 14 callers de `FUN_1405dad20` (o único, `FUN_1400ce1c0`, mais os 13 novos) os dereferencia.
Duas leituras possíveis: (a) são de fato o offset/ponteiro de entrada do bytecode, mas consumidos
por código que NÃO passa pelo lookup por nome (ex.: o motor pode resolver o label uma vez e
cachear o endereço, ou o slot de handler da vtable pode já receber o offset por outro caminho,
não pelo record); (b) são metadados não usados neste jogo específico (herdados de um formato
mais genérico de outro título Kiseki). Continuar essa linha exigiria decompilar a implementação
concreta do slot 2 da vtable (`FUN_1400ce1c0` só invoca `(**(code**)(*plVar+0x10))(...)` — chamada
virtual, não resolvida pra endereço concreto) pra ver se ELE lê `+0x00`..`+0x0c` do record.

Ferramentas desta sessão: mesmo Ghidra project, script novo `C:\re\scripts\DecompCallers3.java`
(decompila os 13 callers restantes em lote).

### RETOMADA (2026-08-23, sessão seguinte #3) — pool de 11 handlers é 100% sistema de batalha; linha encerrada

Investigado o pool de 11 slots em `ScriptManager+0x11690` (indexado por `id & 0xf`), tentando achar
o construtor concreto do objeto no slot pra resolver o vtable slot 2 chamado em `FUN_1400ce1c0`.

- Busca por xrefs ao offset literal `0x116d0` (= slot fixo `id=8`, o mais usado no binário — 62
  hits) mostrou **um único write site**: `MOVUPS xmmword ptr [RBX+0x116d0],XMM0` dentro do próprio
  `FUN_1400372e0` (construtor do `ScriptManager`) — é só zeragem de memória (`memset`-like), não
  um `new` de subobjeto com vtable própria. Todos os outros 61 hits são leituras.
- Decompilado `FUN_1400ce0d0` (rotina de limpeza de handlers, chamada no destructor/reset da
  scena): confirma o pool como array de **ponteiros** de 8 bytes em
  `DAT_140c5f170 + 0x11690 + (id & 0xf) * 8`, cada objeto apontado tendo campo `+0x74` (flag de
  "slot ocupado", compara contra o ponteiro de scena_obj em `+0x08`) e um método de vtable em
  `+0x30` ("release"), chamado quando a scena dona do handler é destruída.
  Confirma também: `FUN_1400ce1c0` (dispatcher genérico por nome) usa exatamente essa mesma
  indexação (`(param_2 & 0xf) * 8 + 0x11690`), com `+0x408` como flag de "handler livre" e
  `+0x10` como o método de vtable disparado (slot 2, o "invoke" do handler).
- **Todos os 14 callers de `FUN_1405dad20`, e todos os 62 usos de `+0x116d0`, pertencem
  exclusivamente ao subsistema de batalha** (`btlsys.*`, `BattleStart/End/Dead/GameOver/...`,
  `battle_ai.cpp`, `script_manager.cpp` linha 0x18c/0x2dd que é dentro do próprio dispatcher). Não
  apareceu nenhuma referência a diálogo, texto ou `scena/*.dat` de conversação nesse pool inteiro.
  O slot concreto (ex.: `id=8`) é populado em algum ponto de inicialização do sistema de batalha
  via offset computado em runtime (`reg*8 + 0x11690`, não um imediato literal), fora do escopo dos
  4 hits de `0x11690` já mapeados — encontrar esse `new` exigiria mais um salto de indireção sem
  relação alguma com extração de diálogo.

**Conclusão prática**: a cadeia de dispatch por nome via vtable (`sora::script::Manager` → pool de
11 handlers → slot vtable+0x10) é **inteiramente do sistema de batalha**, não de diálogo/texto.
Continuar essa linha não teria retorno pro objetivo real do conector (extração de texto de
`scena/*.dat`). **Linha de RE de VM encerrada de novo aqui** — a extração via heurística de string
scan (já em produção, ver seções anteriores) continua sendo a via prática confirmada; os 16 bytes
remanescentes do label record (`+0x00`..`+0x0c`) ficam como curiosidade não resolvida, sem
prioridade.

Ferramentas desta sessão: `C:\re\scripts\FindOffset116d0.java` (busca de xrefs por scalar).

### DECISÃO DE ESTRATÉGIA (2026-08-23) — pivô pra abordagem pragmática, RE de VM pausada

Depois do achado do dispatch por nome via vtable (acima), ficou claro que continuar resolvendo
a cadeia de objetos (`event manager` → vtable real → implementação → só então descobrir se essa
via toca texto de diálogo) tem **custo crescente e retorno incerto**: cada salto adicional exige
um novo ciclo de busca+decompilação no Ghidra, e o que já foi resolvido (dispatch de
função/label por nome) é um subsistema diferente de como a caixa de texto busca a linha de
diálogo pra exibir — não há garantia de que essa cadeia leve lá.

**Decisão tomada com o usuário**: pausar a RE de VM/bytecode aqui e seguir para a Camada 1 com
uma abordagem pragmática orientada a dados, que não depende de entender o mecanismo de referência
de string:

1. `extract.py` faz varredura heurística de sequências ASCII imprimíveis terminadas em `\0`
   dentro do `.dat` (mesmo princípio já usado pra achar as strings citadas neste doc).
2. `reinsert.py` grava a tradução **no mesmo offset, respeitando o mesmo tamanho em bytes**
   (padding/truncamento) — assim nenhuma outra estrutura do arquivo (o array de records de 32
   bytes, os campos de header, etc.) precisa mudar, porque nada que referencia essas strings é
   tocado.
3. Validar via round-trip byte-idêntico (`test_roundtrip_synthetic.py` / gate padrão do
   framework) antes de declarar a camada 1 mapeada.
4. Se essa abordagem quebrar (round-trip falhar, ou pt-BR precisar de mais espaço do que cabe no
   tamanho original), aí sim retomar a RE de VM — mas com uma pergunta concreta e estreita
   ("por que o offset X move quando essa string muda de tamanho"), em vez de exploração aberta.

RE de VM/vtable fica **pausada, não abandonada** — os achados até aqui (header do `#scp`,
cadeia de loading, dispatch por nome) ficam registrados acima como base caso seja retomada.

### O que falta mapear (bloqueia extract.py de verdade)

- [ ] Confirmar (ou refutar) a hipótese do array de records de 32 bytes em 0x20 contra outros
      arquivos `.dat` (idealmente um com `header[2]` pequeno, fácil de contar à mão) — só relevante
      se a abordagem pragmática esbarrar nisso durante o round-trip.
- [ ] Terminador de string (aparenta ser `\0`, não confirmado sistematicamente).
- [x] Codificação de token de controle: `<C1>` e variantes — **mapeado em 2026-08-23** via
      regex `<[^<>]{1,20}>` sobre as 41.834 strings de `dialogs.csv`: 57 tokens distintos / 1.170
      ocorrências em 9 categorias (cor `<C\d+>`/`</C>`, portrait `<P\d+>`, tecla/kanji `<[Kk]\d*>`,
      voz `<S\d+>`, pausa cronometrada `<[Ww]\d+>`, ícone de botão `<I\d+>`, emoção `<E\d+>`,
      código facial composto `<#E_x#M_y#B_z>`, literais raros `<R>`/`<T>`). Registrado em
      `project.json` (`formatting_tokens`/`formatting_token_patterns`). Cobertura é sobre o dado
      da demo — full game pode ter variantes novas.
- [ ] Se o offset de cada string de diálogo é estável o bastante para servir de `id` no
      `dialogs.csv` (padrão do framework é `offset` como id — ver `souldiers/project.json`).
- [x] Escrever `extract.py`/`reinsert.py` heurísticos (scan de strings + replace de mesmo tamanho)
      e validar round-trip — **feito em 2026-08-23** (sessão de continuação). Resultado:
      - `extract.py` rodado contra a demo real: **41.834 strings** extraídas de **78** arquivos
        `scena/*.dat`. Scan de ruído (heurístico) apontou **191/41.834 (~0,46%)** linhas
        potencialmente problemáticas; inspeção manual de amostra confirmou que a maioria são
        frases curtas legítimas, ruído real é uma fração ainda menor (ex: `'@&[ '`, `' x4.'`) —
        aceitável para esta camada heurística.
      - `reinsert.py` valida round-trip **byte-idêntico** contra o `.pac` real instalado
        (`test_roundtrip.py`) e contra fixture sintética em memória (`test_roundtrip_synthetic.py`,
        sempre roda em CI sem depender do jogo). 5 + 2 testes passando.
      - Bug real encontrado e corrigido durante a implementação: padding de string truncada
        estava usando espaço (`b" "`) antes do `\0` final — deixaria espaço visível no jogo.
        Corrigido pra padding com `\0` direto após o texto (traduzido/truncado).
      - Limitação documentada (não é bug do reinsert): o helper de teste `read_scena_strings`
        re-varre com a MESMA heurística do `extract.py` (min. 4 chars + espaço obrigatório), então
        traduções curtas/sem-espaço ficam invisíveis nesse re-scan mesmo gravadas corretamente —
        um futuro `verify_chapter.py` deve ler pelos offsets do `dialogs.csv`, não re-varrer.
      - Ainda não resolvido/fora de escopo: token `<C1>`/variantes ainda não mapeados
        sistematicamente (ver item acima); `build_plan_chapter.py`/`verify_chapter.py` não
        escritos (Fase D6b, fora do escopo deste passo).

### Estado da sessão em 2026-08-23 — pausada aqui a pedido do usuário

Sessão de RE pausada neste ponto (decisão explícita do usuário). Ferramentas/artefatos desta
sessão de RE, se for retomar a Camada 1 de verdade (bytecode/VM):

- Ghidra project em `C:\re\ghidra_project\trails_sc` (programa `sora_2nd.exe` já importado e
  analisado — reusar com `-process sora_2nd.exe -noanalysis`, nunca reimportar).
- Scripts Java usados ficam em `C:\re\scripts\` (`FindScp.java`, `DecompScp.java`,
  `DecompCaller.java`, `DecompCallers2.java`, `FindConst.java`, `DecompReader.java`).
- Cópia limpa do executável em `C:\re\sora_2nd.exe` (o original tem espaços/parênteses no path
  e quebra o `analyzeHeadless.bat`).
- Lembrete de shell: sempre usar paths estilo Unix (`/c/re/...`) sem aspas em comandos Bash pra
  chamar `analyzeHeadless.bat` — path Windows cru fora de aspas quebra por causa da interpretação
  de barra invertida do MSYS.

### Estado da pesquisa (2026-08-23)

Ferramentas públicas verificadas e **nenhuma cobre o `#scp` interno deste remake**:
- `FPACker` (coinkillerl) — só o contêiner FPAC, não entra no `.dat`.
- `Aureole`/Calmare (Kyuuhachi) e `EDDecompiler` (ZhenjianYang) — decompiladores de scena
  consolidados, mas para o formato **clássico ED6** (porte PC XSEED de Sora no Kiseki), não para
  este engine novo do remake 2025/2026. Bytecode provavelmente incompatível (magic diferente:
  `#scp` aqui vs. formato ED6 sem esse magic).
- `Trails-Research-Group/Doc` — index de ferramentas, sem doc de formato binário.
- Nenhuma menção pública encontrada a `#scp`/`FPAC` scena parsing especificamente para este remake
  no momento da pesquisa — é engine muito recente, comunidade provavelmente ainda não chegou lá.

**Ferramentas de RE do CLAUDE.md do projeto não estão instaladas neste ambiente** (binwalk,
Kaitai Struct, ImHex) — mapeamento até aqui foi feito com Python (`struct` + regex de strings ASCII)
como fallback. Recomendado instalar ImHex (padrão de pattern-matching visual acelera achar a
tabela de ponteiros) antes de continuar essa camada.

---

## SEÇÃO 5 — Cobertura de charset do alvo (pt-BR): UTF-8, confirmado (2026-08-23)

**Confirmado sem precisar testar no jogo**, comparando o mesmo arquivo `scena/e2000.dat` nos dois
pacotes já instalados (`pac/steam/script_en.pac` inglês vs `pac/steam/script.pac` japonês/base):
na região onde o inglês tem `"My name is Estelle Bright. And my dream has always..."`, o japonês
tem os bytes `e9 80 a3 e4 b8 ad e3 81 8c e5 bc 95 ...`, que decodificam **perfeitamente como
UTF-8 válido**:

```
連中が引き起こした『定期船失踪事件』だった。
以降、全ての...
```

Japonês (3 bytes/caractere em UTF-8) está codificado assim no mesmo arquivo/mesmo mecanismo que
o inglês ASCII (1 byte/caractere, também válido em UTF-8) — ou seja, o `#scp` usa **UTF-8** como
charset de texto, não ASCII-only nem Shift-JIS/CP932 (testado e descartado: bytes aleatórios do
bytecode "decodificam" como CP932 sem erro por acaso, dado o range amplo de lead-bytes do CP932 —
falso positivo; o teste decisivo foi achar JAPONÊS COERENTE decodificando como UTF-8, não CP932).

**Implicação prática**: `reinsert.py` foi corrigido em 2026-08-23 pra gravar `.encode("utf-8")`
em vez de `.encode("ascii")` (que rejeitava qualquer acento). Acentos de pt-BR (á, ç, ã, õ — 2
bytes em UTF-8) cabem no formato. Truncamento por `byte_budget` agora é UTF-8-safe (nunca corta
um caractere multibyte ao meio — decode/re-encode com `errors="ignore"` descarta bytes finais
incompletos). Coberto por `test_roundtrip_accented_translation_utf8_safe_truncation` em
`test_roundtrip_synthetic.py`.

**CONFIRMADO VISUALMENTE NO JOGO em 2026-08-23**: a fonte do jogo tem glifos pra caracteres
latinos acentuados de pt-BR (í, à, é testados) e renderiza sem clipping/glifo quebrado. Evidência:
`.pac` de teste com 2 diálogos reais (`scena/mp0000.dat:0x665d9`/`0x665c3`, NPC "Skyler",
"O dirigível Linde, rumo à capital, / vai pousar em seguida"; e `scena/mp0000.dat:0x66e62`/`0x66e45`,
NPC "Fabree", "Pelo que ouvi dizer, o Arseille / é uma verdadeira maravilha.") — screenshots em
`manual_tests/evidence/resultado_1.png` e `resultado_2.png` (pasta gitignored, local).

**Nota de processo**: a 1ª tentativa de teste visual usou strings de `scena/e2000.dat` (a
narração de abertura "Our story begins in Rolent...") que na verdade fazem parte da legenda
GRAVADA NO VÍDEO do recap "Summary of 1st Chapter" — o vídeo toca sozinho, sem esperar botão, e a
legenda é pixel do vídeo, não texto desenhado pelo motor. Editar o `.pac` não tinha como afetar
essa tela (confirmado: arquivo trocado corretamente, data de modificação atualizada, jogo
reiniciado, texto continuou em inglês). Lição: só testar strings de `scena/*.dat` que correspondem
a diálogo interativo real (caixa com nome de personagem, avança por botão) — não a narração de
cutscene/vídeo, mesmo que o texto esteja no mesmo arquivo/formato `#scp`.

## SEÇÃO 6 — Wrap de linha: automático, confirmado (2026-08-23)

Nenhuma das 41.834 strings extraídas (a maior tem 72 caracteres) contém `\n` embutido —
confirmado varrendo `dialogs.csv` inteiro. Ou seja, o motor faz **quebra de linha automática na
renderização**; não existe convenção de newline manual no dado-fonte que o tradutor precise
respeitar. `length_constraints.mode` no `project.json` registrado como `auto_wrap_no_manual_newline`.

Isso NÃO resolve sozinho a questão de "pt-BR mais longo estoura a caixa" — `reinsert.py` já
trunca pt-BR pro mesmo `byte_budget` do inglês (replace same-size), então nunca escrevemos mais
texto do que cabia no original; a pergunta real que sobra era só qualidade (o corte no meio da
palavra em orçamento apertado é aceitável?) e se a fonte tem os glifos acentuados — ambas
confirmadas visualmente no jogo em 2026-08-23 (ver SEÇÃO 5): glifo acentuado ok; teste de
truncamento no meio da palavra (`scena/e2000.dat:0x6040`, "juniores oficialmente!"→"juniores ofi")
foi feito na 1ª rodada mas caiu na cutscene de vídeo (não validado visualmente); o teste que
funcionou (`mp0000.dat`, NPCs Skyler/Fabree) coube dentro do orçamento sem truncar. Corte no meio
da palavra em diálogo interativo real segue como item de qualidade não verificado visualmente —
candidato a retestar com uma tradução propositalmente maior num diálogo de `mp*.dat` se virar
prioridade.

## SEÇÃO 7 — Fase D6b: divisão em cenas + build_plan_chapter.py/verify_chapter.py (2026-08-23)

Sessão de continuação, depois de extract.py/reinsert.py validados (Seções 5/6). Objetivo: destravar
o `connector_gate` (hard, não-bypassável) do runtime de tradução, que exige `build_plan_script` e
`verify_script` no `project.json` apontando pra arquivos existentes.

**1. Divisão em cenas — gap de framework achado e corrigido.** `run_scene`/`build_plan_chapter`
exigem `artifacts/scenes/<cena>/dialogs.csv` (`paths.py`, contrato congelado) — o `dialogs.csv`
FLAT que `extract.py` escreve não é lido pelo runtime de tradução. Não existia NENHUMA ferramenta
genérica no framework pra fazer essa ponte (BoF4/Souldiers/Utawarerumono resolveram isso ad hoc,
cada um diferente). Criado `framework/runtime/split_scenes.py` (melhoria de framework, não só
deste projeto — ver `ROADMAP.md` P1.7-F), cobrindo o caso "1 coluna do corpus = 1 cena" (`file`,
que é exatamente o padrão do Trails Sky SC). Rodado de verdade:
`python framework/runtime/split_scenes.py projects/trails_sky_sc` → **41.834 linhas → 71 cenas**
em `artifacts/scenes/<cena>/dialogs.csv`.

**2. `build_plan_chapter.py`** (adaptado do skeleton + padrão real do BoF4). Por cena: exige
cobertura total (todo offset do `dialogs.csv` da cena com tradução em `translations_*.json`) e
preservação dos tokens de formatação do engine — carrega `formatting_tokens`/
`formatting_token_patterns` do `project.json` (Seção "CAMADA 1", token de controle mapeado) em
runtime via `_structural_token_rx(root)`, compila 1 regex e compara `Counter` de ocorrências
src×tgt por linha. Linhas com `risk_level` medium/high/critical exigem `risk_notes`. Escreve
`translation_plan_<sfx>.json` + `approved_<sfx>.csv`.

**3. `verify_chapter.py`** — o ponto de maior adaptação: BoF4 opera sobre 1 arquivo binário
isolado por cena; aqui múltiplas cenas vivem no MESMO buffer `.pac` compartilhado (contêiner FPAC),
então toda verificação é escopada ao(s) entry(ies) `scena/*.dat` tocado(s) pela cena, dentro do
buffer inteiro (`[addr, addr+size)`). Oráculos, em ordem:
  1. round-trip vazio (`rebuild_pac(..., {}, ...)` == bytes originais — fast-path de identidade).
  2. round-trip significativo: reinserir o PRÓPRIO `text_en` de cada offset da cena (o `byte_budget`
     é exatamente `len(text_en)+1` por construção do `extract.py`, então não deveria truncar nada) —
     precisa reproduzir os bytes originais byte a byte; sem isso, um round-trip vazio sozinho
     provaria pouco (é literalmente um no-op no código).
  3. apply real (traduções aprovadas, com fallback pro `text_en` se algum offset ficar sem
     aprovação — defensivo, mesmo padrão do BoF4).
  4. overflow individual (`len(utf-8)+1 > byte_budget`) — falha classificada como `fitting_only`
     (exit 3, escalável — nunca hard fail, coerente com a decisão já registrada de que overflow
     trunca em vez de erro).
  5. readback por OFFSET conhecido (não re-scan) — decisão que já estava documentada na docstring
     de `reinsert.read_scena_strings` desde a Seção 6 ("um verify_chapter.py futuro deve ler pelos
     offsets do dialogs.csv, não re-varrer"): le `new_bytes[abs_off:abs_off+budget]`, tira o padding
     `\0`, compara contra `truncate_for_budget()` (função nova, extraída de dentro de
     `reinsert.rebuild_pac` pra `verify_chapter.py` reusar a MESMA lógica de truncamento em vez de
     reimplementar e arriscar divergência).
  6. sem corrupção fora da cena: bytes fora dos ranges `[addr, addr+size)` tocados == bytes
     originais.
  Classificação final: qualquer falha fora de `individual_overflow` é `hard_fail` (exit 1); só
  overflow(s) sozinho(s) é `fitting_only` (exit 3). Protocolo de saída padrão do framework
  (`VERIFY_STATUS: {json}` + exit 0/1/3) inalterado.

**4. Teste.** `connector/test_chapter_pipeline.py` (5 testes) reusa o fixture FPAC sintético já
existente em `test_roundtrip_synthetic.py` (não duplica setup) — cobre `_structural_token_rx`
(regex vazia vs. tokens reais) e `verify_chapter._rebuild` (OK/overflow-como-fitting-only/sem
corrupção fora da cena) via `TRAILS_SKY_SC_DATA_DIR` apontando pra um `.pac` sintético em
`tmp_path`, sem depender do jogo real. 11 passed + 2 skipped (os 2 skipped exigem o `.pac` real,
gitignored) na suíte inteira de `connector/`.

**5. Estado do gate após D6b.** `connector_gate` HARD (`build_plan_script`/`verify_script`
existem) confirmado verde. O soft-check ("nenhuma cena com round-trip verde registrado em
`run_state.json`") continua aberto — só fecha com 1 passada real de `run_scene` (tradução via
`model.py`), que por sua vez está bloqueada pelo `kb_gate`: **Fase 0 de KB do Trails Sky SC
(`artifacts/kb_phase_worklist.md`) ainda não foi iniciada.** Nenhuma tradução de verdade foi feita
ou testada contra o `.pac` real nesta seção — só contra fixture sintético.

### RETOMADA (2026-08-23, sessão seguinte #4) — pendência "tabela de nomes de Arts/Crafts" RESOLVIDA

Contexto: ao popular `artifacts/glossary.csv` (Fase 3, ver seção acima), só 3 nomes de Art apareciam
em `dialogs.csv` (Aqua Bleed, Air Strike, Tear — texto de tutorial em `scena/system.dat`). Hipótese
registrada: o catálogo completo de Arts/Crafts vive em outra tabela binária, ainda não mapeada pelo
conector. Usuário pediu pra resolver essa pendência de verdade, não só deixar anotada.

**Achado**: `pac/steam/table_en.pac` (mesmo `TRAILS_SKY_SC_DATA_DIR`, achado via busca em
`/c/Program Files (x86)/Steam/steamapps/common/Trails in the Sky 2nd Chapter Demo/`) é um contêiner
FPAC — mesmo formato de contêiner já suportado por `connector/fpac_unpack.py`, sem trabalho novo
de parsing de contêiner. Dentro dele, 129 entradas `table_en/t_*.tbl`. A relevante:
`table_en/t_skill.tbl` (96.935 bytes) contém, como texto ASCII puro (mesma heurística de
extração já usada pra `scena/*.dat` — scan de strings, sem VM/bytecode envolvido), o catálogo
completo confirmado nesta demo:
  - 72 Arts (magias por elemento — contagem final precisa, após correção do bug de truncamento
    UTF-8 descrito abaixo): Earth x13, Water x14, Fire x11, Wind x10, Time x11, Space x7,
    Mirage x6 — cada uma com nome + descrição em `<C9>...` (mesmo token de cor já catalogado em
    `formatting_token_patterns`).
  - 117 Crafts/S-Crafts por personagem (nome + descrição), agrupadas por bloco
    (`AniBtlCraft##` / `AniBtlSCraft##` como chave interna, não visível ao jogador). Excluídas
    15 entradas de QA/debug (`AniBtlCraftTest*` / `AniBtlSCraftTest*`, ex.: "Single, Move",
    "Circle, Location" — não são nomes de habilidade jogável).
  - 40 habilidades reativas ligadas a Support Ability, tag interna `BFS`, sem descrição própria
    na tabela (First Aid/EX/Supreme, Resurgence/EX/Supreme, Dauntless Courage/EX, Lightning
    Speed/EX, Wheel of Fortune/EX, Magnificent Harmony/EX, Unparalleled Focus/EX, Heat Up/II,
    Self Maintenance/II, Immovable Pranayama/EX, Gralsritter's Grace/EX, Energy Reload/EX,
    Fell Swoop/EX, Inner Calm/EX, Winds of Change/EX, Heavenly Herald/EX, Endure, Quick Repair,
    Indomitable Will, Auto Thelas, Flames of Carnage, Auto Athelas).
  - Confirma Aqua Bleed/Air Strike/Tear (+ variantes não vistas em `dialogs.csv`: Teara,
    Tearal, La Tear, La Teara, La Tearal, Tear-All).

**Bug encontrado e corrigido durante a extração**: regex ASCII-only (`[\x20-\x7e]{3,}` direto em
bytes) truncava silenciosamente nomes com caractere não-ASCII — ex.: "Kämpfer" virava "mpfer"
(o prefixo "Kä" é uma sequência UTF-8 de 2 bytes que quebra o range ASCII). Também achou variantes
com letras gregas reais como sufixo de tier ("Kämpfer β", "Kämpfer γ", "Vital Cannon Σ").
Corrigido decodificando o arquivo inteiro como UTF-8 primeiro (`errors='replace'`) e aplicando
regex Unicode-aware (`[\x20-\x7e -￿]{2,}`) sobre o texto decodificado, filtrando strings
com `�` (ruído binário genuíno) — validado via grep pontual em "Kämpfer" pós-correção.

**Conclusão**: a pendência de RE está fechada — não existe VM/bytecode escondendo esses nomes; é
outro arquivo `#TBL` dentro do mesmo tipo de contêiner FPAC já resolvido, com texto legível do mesmo
jeito. `t_orbment.tbl` (Quartz/Orbment/Arts parametrização, sem nomes) e `t_skill.tbl` (nomes +
descrições) são tabelas separadas — o parâmetro numérico e o texto de exibição não vivem juntos,
como já era o padrão observado em `scena/*.dat` (`#scp` vs. string pool).

**Escopo concluído em sessão seguinte (mesmo dia)**: os 72 Arts + 117 Crafts/S-Crafts + 40
habilidades reativas (229 termos, menos os 3 já cadastrados = 226 linhas novas) foram adicionados
a `glossary.csv` com `handling_rule: manter_original` (convenção já usada para Aqua Bleed/Air
Strike/Tear — nomes de magia/técnica ficam no original, como em toda a série Trails/Kiseki
já lançada em PT-BR não-oficial) e `notes` citando a descrição original traduzida para
referência do tradutor. `category: Mecânica`, mesma usada para os 3 termos-piloto.

Ferramenta usada: `connector/fpac_unpack.py` (já existente, sem alteração) + scan de strings
Unicode-aware ad hoc em Python sobre `table_en/t_skill.tbl` extraído. Nenhum arquivo novo criado
no conector.

### RETOMADA (2026-08-23, sessão seguinte #5) — pendência "cobertura de UI em jogo" RESOLVIDA

Contexto: roadmap listava como pendência aberta a cobertura de texto de UI/menu além dos 8 termos
piloto já cadastrados em `glossary.csv` (categoria UI). Usuário pediu pra resolver essa pendência
("item 1") com o mesmo rigor da RETOMADA #4.

**Achado**: dentro do mesmo contêiner `pac/steam/table_en.pac` (129 entradas `table_en/t_*.tbl`,
já mapeado na RETOMADA #4), `table_en/t_text.tbl` (107.452 bytes, nome interno `TextTableData`) é
a tabela mestra de texto de UI/sistema — mesmo formato genérico `#TBL` de `t_skill.tbl`, texto
ASCII/UTF-8 puro, sem VM/bytecode. Estrutura: chave `TXT_<NOME>` seguida de um ou mais valores em
inglês até a próxima chave `TXT_`. Total: **1603 pares chave/valor**, cobrindo ~40 subsistemas por
prefixo (CAMP=217 menu principal, OPT=187 opções, NOTE=125 caderno do Bracer, BTL=96 status/popup
de batalha, SHOP=81, MINIGAME=73 cassino, VIEWER=60 modo foto, ITEM=42, QUEST=41, TITLE=38, HUD=36,
MINIMAP=28, SAVE=18, MESLOG=18, STEAM=446 configurações gráficas/controle específicas do port Steam,
e outros menores).

**Heurística de curadoria**: nem todo par é um "termo de UI" (muitos são frases completas de
ajuda/tutorial, fora do escopo de glossário de termos). Filtro aplicado: valor único por chave,
sem pontuação de frase (`.?!%`), ≤28 caracteres, sem token de ícone (`<I...>`) — resultou em 738
candidatos "label-like". Removido o bloco `TXT_STEAM_*` (446 pares, configurações gráficas/input
específicas do port PC — fora do escopo "telas de menu do jogo" descrito na pendência; fica anotado
como possível Fase 3.5 futura, não bloqueia esta). Dos 572 candidatos restantes, deduplicados por
valor (várias chaves diferentes repetem o mesmo texto em telas diferentes, ex.: "Owned", "Total",
"Cancel") → 464 termos únicos. Removidos mais 15 por serem nomes de objeto interativo de campo ou
entradas de debug/QA (`TXT_DOOR`, `TXT_SMOKE_POT`, `TXT_MOSS`, `TXT_EV_*`, `TXT_QS2*_00`,
`TXT_AIUEO`, `TXT_TEST_*`) — não são texto de menu.

**Bug de extração corrigido**: o regex Unicode-aware com tamanho mínimo 2 (usado na RETOMADA #4)
capturava ruído binário de 2 bytes de uma região de tabela de offsets no início do arquivo (ex.:
`"'e"`, `'gf'`). Corrigido subindo o mínimo para 4 caracteres, o que isola de forma limpa o
conteúdo real a partir de `'#TBL'`/`'TextTableData'`/`'TXT_SAVEDATA_NEWDATA_TITLE'` em diante.

**Lacuna confirmada e não preenchida (sem fabricar)**: as legendas literais das abas principais do
menu CAMP (as strings realmente exibidas — "Equip", "Orbment", "Item", "Status", "Achievement",
"Costume", "System") foram buscadas diretamente (`TXT_CAMP_EQUIP`, `TXT_CAMP_ORBMENT`, variações
`*_TAB_TEXT`/`*_TAB`) e **não existem como string extraída isolada** em `t_text.tbl` — só a
variante `_HELP` (descrição da aba) existe, ex.: `TXT_CAMP_TOP_TAB_HELP_EQUIP` → `'Change
equipment.'`. Por via de regra do projeto (nunca cadastrar termo sem fonte extraída confirmada),
essas 7 legendas de aba **não foram adicionadas ao glossário** — provavelmente vivem em atlas de
imagem ou em outra tabela ainda não localizada. Fica como pendência residual, pequena e específica
(7 strings), registrada aqui em vez de inventada.

**Escopo concluído no mesmo dia**: os 464 termos únicos curados (menos 15 exclusões de
objeto/debug = 449) foram processados; 5 já existiam no glossário (Sepith, Quartz, Mira, Estelle
Bright, Joshua Bright — colisão de valor com termos já cadastrados em outras categorias) e foram
pulados automaticamente pelo script de importação. **439 linhas novas** adicionadas a
`glossary.csv` com `category: UI` e `handling_rule: traduzir` (ao contrário do `manter_original`
usado pra Arts/Crafts — texto de interface comum é traduzido, não é nome próprio de mecânica),
`target_translation` preenchido com tradução PT-BR, `notes` citando a chave `TXT_` de origem pra
rastreabilidade. Também adicionadas **5 abreviações de status** que apareciam em popups de batalha
mas ainda não tinham entrada própria (STR, DEF, ATS, ADF, SPD, MOV — na verdade 6, mas `MOV` novo;
seguem a convenção já usada para HP/EP/CP: `category: Mecânica`, `handling_rule: manter_original`).
`glossary.csv` foi de 333 para 772 linhas.

Ferramenta usada: `connector/fpac_unpack.py` (sem alteração) + scan de strings Unicode-aware ad hoc
em Python sobre `table_en/t_text.tbl` extraído. Nenhum arquivo novo criado no conector.
