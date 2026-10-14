# TABLE SCHEMA — Trails in the Sky 2nd Chapter (remake Falcom, 2026)

> Fase 0 **concluída em 2026-08-23**. Duas camadas de formato: contêiner FPAC (mapeado, confirmado
> por bytes reais) e script interno `scena/*.dat` em formato `#scp` (header e tabela de records
> mapeados; bytecode não mapeado). Critério de conclusão: os dois formatos necessários pro conector
> (contêiner FPAC + heurística de extração de string em `#scp`) estão mapeados, confirmados e em
> produção (Fase 1); a via de bytecode/VM foi avaliada e não é necessária nem aplicável a diálogo —
> decisão final, não pausa.

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

### Header do `#scp` (todos u32 LE), cruzado contra `e2000.dat`

| Offset | Campo | Valor em e2000.dat | Significado |
|---|---|---|---|
| 0x00 | magic | `0x70637323` ("#scp") | identificação do formato |
| 0x04 | header[1] | `0x18` (24) | offset, a partir do início do arquivo, da tabela de records de 32 bytes |
| 0x08 | header[2] | `0x2a` (42) | contagem de records de 32 bytes |
| 0x0c | header[3] | `0x318c` (12684) | offset de uma tabela auxiliar de entradas de 8 bytes; só vale se header[4] != 0 |
| 0x10 | header[4] | `0` em e2000.dat | contagem de entradas da tabela auxiliar — provavelmente flags de voice-over (`0x40000000` = "sem voz" / `0xc0000000` = "com voz" por entrada) |

### Tabela de records (32 bytes cada)

Dump das 3 primeiras linhas de 32 bytes de `e2000.dat` a partir de `0x20`. A tabela começa em
`header[1]` (= `0x18`), então este dump está deslocado 8 bytes em relação ao início de cada record:

```
offset  u32[0] u32[1] u32[2]  u32[3]  u32[4]      u32[5]      u32[6]  u32[7]
0x20    0x558  0x5e8  0x98    0x718   0x3e5f3851  0xc00077c3  0x5be0  0
0x40    0x558  0x5e8  0x01    0xe38   0x009e93cc  0xc00077d2  0x4275  0
0x60    0x558  0x5e8  0x00    0xe44   0x3585e0ee  0xc00077e9  0x4281  0
```

Campos, relativos ao início do record:

| Offset | Campo | Notas |
|---|---|---|
| +0x00..+0x0c | não identificado | 16 bytes sem uso conhecido |
| +0x10 | contagem de parâmetros | do label/evento |
| +0x14 | offset da tabela de descritores de parâmetro | relativo ao início do arquivo; 12 bytes por descritor: `+0x04` type tag (i16), `+0x06` flag (u16), `+0x08` valor com tag nos 2 bits altos (`1` = inteiro de 30 bits com sinal, `2` = float) |
| +0x18 | hash do nome | tipo CRC32 |
| +0x1c | offset do nome | 2 bits altos = flag (`0xC0000000`/`0x40000000`), 30 bits baixos = offset, a partir do início do arquivo, da C-string do nome |

- Cada record é um **label/evento nomeado** (ex.: `OnEventFinalize`, `OnMapReinit`, `BattleStart`),
  invocado pelo motor por nome. Os nomes vistos são de sistema de eventos e de batalha, não de
  diálogo — coerente com as strings de identificador do dump de `e2000.dat` (`sound.PlayBGM`,
  `OnMapReinit`), que não são texto de fala.
- O padrão de flag `0xC0000000`/`0x40000000` aparece tanto na tabela de voz quanto no offset de
  nome do record — parece convenção geral do formato para "offset válido vs. nulo".
- Esta tabela **não** contém o offset das strings de diálogo: o mecanismo que liga o bytecode a
  cada fala segue não mapeado.

### DECISÃO DE ESTRATÉGIA (2026-08-23) — abordagem pragmática orientada a dados

Mapear o bytecode do `#scp` tem **custo crescente e retorno incerto**: a tabela de records acima é
de labels/eventos, um subsistema diferente de como a caixa de texto busca a linha de diálogo — não
há garantia de que esse caminho leve lá.

**Decisão tomada com o usuário**: seguir para a Camada 1 com uma abordagem pragmática orientada a
dados, que não depende de entender o mecanismo de referência de string:

1. `extract.py` faz varredura heurística de sequências ASCII imprimíveis terminadas em `\0`
   dentro do `.dat` (mesmo princípio já usado pra achar as strings citadas neste doc).
2. `reinsert.py` grava a tradução **no mesmo offset, respeitando o mesmo tamanho em bytes**
   (padding/truncamento) — assim nenhuma outra estrutura do arquivo (o array de records de 32
   bytes, os campos de header, etc.) precisa mudar, porque nada que referencia essas strings é
   tocado.
3. Validar via round-trip byte-idêntico (`test_roundtrip_synthetic.py` / gate padrão do
   framework) antes de declarar a camada 1 mapeada.
4. Se essa abordagem quebrar (round-trip falhar, ou pt-BR precisar de mais espaço do que cabe no
   tamanho original), aí sim mapear o formato mais a fundo — mas com uma pergunta concreta e
   estreita ("por que o offset X move quando essa string muda de tamanho"), em vez de exploração
   aberta.

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

> Atualização 2026-10-14: o item 5 acima (e os números "41.834 strings" das seções anteriores) descreve o estado de 2026-08-23.
> Depois disso: a Fase 0 de KB foi fechada (`artifacts/kb_phase_worklist.md`), um patch do Steam subiu o corpus flat para
> 41.890 linhas (2026-08-26) e a cena-piloto `mp0010_01` consta `verified` no `run_state.json` (round-trip real contra o `.pac`).
> As demais cenas seguem sem tradução. Ver `artifacts/decision_log.md`.

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
