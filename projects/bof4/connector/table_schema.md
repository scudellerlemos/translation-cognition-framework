# Table Schema — Breath of Fire IV (PC Port, Capcom 2000)

> Status: **MAPEADO** — análise do diretório english/DAT em 2026-06-20

---

## 1. Arquivos de diálogo

O jogo usa um container binário com TOC (Table of Contents). O mesmo formato
se aplica a todos os tipos:

| Família | Conteúdo | Escopo Fase 0 |
|---|---|---|
| `AREAD*.DAT` | Diálogo principal de cenas (field events) | ✅ **incluído** |
| `AREAS*.DAT` | Scripts de área (cutscenes, NPCs com fala) | ✅ **incluído** |
| `AREAE*.DAT` | Eventos de área (narração de abertura, cutscenes, tutoriais) | ✅ **incluído** |
| `AREAM*.DAT` | Cidades e mapas (NPCs, lojas, minijogos — ex.: `AREAM000` = Sarai) | ✅ **incluído** |
| `SHOP.DAT`, `CAMP.DAT`, `DEMO.DAT`, `AB*.DAT`, `INIT.DAT` e demais de sistema | UI, loja, batalha, menu | ✅ **incluído depois** (`extraction_scope: completo` no `project.json`; eram "fase futura" na Fase 0) |

> **Regra do framework (Fase 0):** o extrator inclui SOMENTE famílias com diálogo
> de personagem identificado por falante. UI, itens e batalha são fases separadas
> (no bof4 o escopo foi ampliado para `completo`; ver `ROADMAP.md`).
> Ver `framework/media-profiles/games.md` — seção "Escopo de extração".

### Filtros de conteúdo aplicados dentro das famílias incluídas

| Filtro | Critério | Motivo |
|---|---|---|
| Família | `AREAD`, `AREAS`, `AREAM`, `AREAE` | escopo de diálogo |
| Sem letra | nenhum byte `A-Za-z` fora de parâmetro de control code | `--[81]`, `5`, `[14]A`, `[0C][05][14]A`: nada a traduzir |

`[05][03]…[06]` é cor de destaque (azul), não "descrição de item": aparece em fala comum e não filtra.
Label curto (`Beer`, `Food`) aparece na tela da cena e é extraído.

---

## 2. Formato do container DAT

```
[0:4]       = TOC size (little-endian uint32) — ex. 0xB0 = 176 bytes = 11 entradas × 16
[4:TOC_SZ]  = entradas do TOC, cada uma de 16 bytes:
    [0:4]   = offset da seção no arquivo (absoluto)
    [4:8]   = tamanho da seção em bytes
    [8:12]  = flags
    [12:16] = tipo
```

A entrada 0 do TOC é o header global (v[0]=TOC_SIZE, v[1]=main_data_size).
As entradas 1..N descrevem seções adicionais.

---

## 3. Seção de texto

Identificada pela heurística: primeira seção cuja tabela de ponteiros + conteúdo pós-tabela
apresenta ≥ 70% de bytes ASCII com palavras reais em inglês.

**Estrutura interna da seção de texto:**

```
[0:PTR_TABLE_SIZE]        = tabela de ponteiros 2-byte (little-endian uint16)
                            valor[0] = PTR_TABLE_SIZE (= tamanho da própria tabela em bytes)
                            PTR_TABLE_SIZE = 0x200 para AREAD/AREAS/AREAE/AREAM
                            (valor ímpar, ex. 0x201: o byte que sobra é preservado como está)
                            PTR_TABLE_SIZE variável para SHOP/CAMP/DEMO
[PTR_TABLE_SIZE:end]      = strings; cada uma vai do seu ponteiro até o PRÓXIMO ponteiro distinto
                            (não até o primeiro \x00 — ver `string_spans` em extract.py)
```

Cada entrada da tabela de ponteiros é um uint16 = offset da string dentro desta seção.
Entradas duplicadas = aliases (dois slots apontam para a mesma string).

**Cenas curtas:** a tabela tem sempre 256 ponteiros nas famílias `AREA*`; cena com poucas falas repete o último ponteiro até encher, e a tabela pode ser maior que o texto. O detector (`find_text_section`) não pode exigir proporção mínima de destinos únicos nem tabela menor que metade da seção — confere se cada destino começa logo depois de um `00`.

**Texto de sistema:** o `INIT.DAT` tem duas seções de texto, 5 (avisos de item, loja, salvar) e 6 (rótulos de tecla, menu e mapa), no mesmo formato. São as únicas com mais de uma seção por arquivo (`text_sections`).

---

## 4. Encoding

**ASCII puro** para o PC port em inglês (bytes 0x20–0x7E são caracteres diretos).
Bytes fora desse range são tokens de controle — representados como `[XX]` no CSV.
Exceção: `0x7F`–`0x84` são glifos de botão do controle (`[7F]: Confirm`, `[80]: Cancel`), desenhados como texto.
Nenhum outro byte ≥ `0x80` aparece como texto no jogo em inglês.

**Sonda in-game (2026-10-11, prints `dentro_bar_sarai_teste*.png`):** `0x85`–`0x87` são ícones de tecla
(`Tab`, `F1`, `Enter`). De `0x88` a `0xFF` o jogo não trava, mas desenha lixo e não avança o cursor (os 16
códigos de cada linha saem empilhados na mesma posição). A fonte não tem glifo acentuado nem largura
para esses códigos.

**Sonda 2 (2026-10-11, print `print_ascentp.png`):** o atlas da seção 9 pode crescer (o jogo abre e desenha os
glifos novos). Código ≥ `0x88` é desenhado na posição do cursor **sem avançar**, então funciona como acento
sobreposto: `á` = `[A0]a` (2 bytes). A célula do acento começa ~2 px antes da tinta da letra seguinte.
`connector/font.py` desenha os 12 acentos (`0xA0`–`0xAB`: agudo, grave, circunflexo, til e cedilha, em
minúscula e maiúscula, mais agudo de `i`/`I`), `encode_string` converte, e `reinsert.py` grava o `INIT.DAT`
estendido em `output/` (precisa do `INIT.DAT` original em `BOF4_DAT_DIR`). `0x88`–`0x9F` ficam em branco.
Só a fonte de 24 px foi tratada; pelos prints do jogo é ela que desenha diálogo, menus, caixa Info e faixa do mapa. A de 16 px (seção 8) segue sem acento e não apareceu em nenhuma tela conferida.
Run3 (2026-10-12): glifo próprio para `í` na vaga de `]` (`0x5D`) falhou — o jogo não desenha as colunas onde o `]` original tem tinta (só um fiapo do desenho apareceu) e avança ~14 px. A janela e o avanço de cada código vêm do executável; medir com sonda antes de reaproveitar uma vaga.
Sonda 3 (2026-10-12, print `run3/ascento2.png`, régua diagonal em cada vaga): cada código tem uma janela de
colunas da célula e um avanço; o jogo desenha a janela a partir do cursor.

| Código | Colunas desenhadas | Avanço (px) |
|---|---|---|
| `;` `0x3B` | 6–17 | ~11 |
| `<` `0x3C` | 13–23 | ~11 |
| `>` `0x3E` | 0–11 | ~11 |
| `[` `0x5B` | não medido (régua encostou no `l` seguinte) | 18 |
| `]` `0x5D` | 5–19 | 14 |
| `\|` `0x7C` | 0–23 | 24 |
| `l` (referência) | — | 8 |

O `í` é glifo próprio na vaga de `>` (`font.I_ACUTE`): `i` original sem o pingo, deslocado 6 colunas para a
esquerda, mais o agudo. `;` tem a mesma largura mas a tradução usa ponto e vírgula. Nenhuma vaga livre avança
8 px como o `i`, então o `í` fica ~3 px mais largo que o `i`.

**Atlas da fonte (2026-10-11):** as fontes ficam no `INIT.DAT`, seções com `flags == 5`, **sem compressão**;
o byte alto do 4º campo é o lado do glifo: seção 8 = 16 px, **seção 9 = 24 px (caixa de diálogo)**, 10 = 12 px,
11 = 64 px. Glifo = lado × lado pixels, 4bpp, nibble baixo primeiro (valor 1 = tinta cheia, maiores = borda
suavizada), índice = código − `0x20`. A seção 9 em inglês tem 104 glifos (`0x20`–`0x87`), por isso `0x88`+ lê
lixo depois do atlas; a japonesa tem 863 no mesmo layout de TOC. Largura/avanço por código fica no `BOF4.exe`
(não analisado). Símbolos ASCII nunca usados no texto do jogo: `$ * < >`.

Seções com `flags & 0xFFFF == 1` são imagem comprimida (`flags >> 16` × 256 = tamanho descomprimido, 4º campo =
destino na VRAM do PS1); codec na seção 9.

---

## 5. Tokens de controle conhecidos

| Token (hex) | Representação CSV | Significado |
|---|---|---|
| `00` | fim de string **ou** `[00]` | terminador só no último byte antes do próximo ponteiro; no meio da string é parâmetro de control code (`[14][00][00]`, `[0F][00]`, `[19][00]`, `[04][00]`) e o texto continua depois dele |
| `01` | `[01]` | newline dentro da caixa de diálogo |
| `02` | `[02]` | page break (aguarda input, abre nova caixa) |
| `04` | `[04]` | variável: nome de personagem (dinâmico) |
| `05` | `[05]` | no `project.json` chama-se `var_item_name` (1 parâmetro); `extract.py` e a nota abaixo da tabela de filtros (seção 1) descrevem `[05][03]…[06]` como **cor de destaque (azul)**, usada em fala comum. **Divergência não resolvida:** o nome do `project.json` e a leitura de cor de destaque não batem; não confirmado qual é o significado real |
| `07` | `[07]` | `var_value` no `project.json` (1 parâmetro, valores `00`–`08`); ex.: `[07][00]` é a tabela "um/todos" de cada cena |
| `09` | `[09]` | `unmapped` no `project.json` (1 parâmetro) |
| `0F` | `[0F]` | `unmapped` no `project.json` (1 parâmetro, valores `00`–`03`, `08`, `09`) |
| `16` | `[16]` | `unmapped` no `project.json` (1 parâmetro) |
| `0A` | `[0A]` | efeito sonoro / voz |
| `0B` | `[0B]` | pausa breve (ellipsis beat) |
| `0C` | `[0C]` | comando de evento (`event_cmd`, 1 parâmetro) |
| `12` | `[12]` | início de menu de escolha |
| `14` | `[14]` | ID de speaker (seguido de byte de personagem) |
| `8B` | `[8B]` | marcador de opção de menu |
| `93` | `[93]` | código de menu (pós-`[8B][0C]`) |
| outros | `[XX]` | tokens não mapeados — preservar sem alteração |

**Padrão de speaker ID:**
```
[14][C1]@ = Nina falando
[14][C2]@ = Cray falando
[14][80]@ = NPC/personagem genérico
[14][81]@ = variante de NPC
```
O byte após `[14]` identifica o personagem; o byte seguinte (ex. `@` = 0x40) pode ser
um parâmetro de posição ou estilo de caixa.

---

## 6. Restrições de tamanho

- **byte_budget por string**: comprimento em bytes do conteúdo original + 1 (terminador)
- **Estratégia de espaço (T1)**: substituição direta se `len(encoded) <= byte_budget`
- **Estratégia de espaço (T2)**: reconstrução da seção — se total da seção nova ≤ total original
- **Estratégia de espaço (T3)**: expansão da seção (atualiza TOC + offsets subsequentes)
- **Overflow irredutível (T4)**: quando nenhuma estratégia cabe; enviar para reescrita por LLM

---

## 7. Ponteiros

**Tabela central no início da seção de texto** (ver seção 3 acima).
Offsets são relativos ao início da seção.
Ponteiros duplicados (aliases) devem ser preservados.

---

## 8. Variantes de localização

O diretório `english/DAT/` contém a versão EN (corpus de extração).
O diretório `japanese/DAT/` contém a versão JP (para referência de lore/nomes).
Mesma estrutura de container e seções entre as duas versões.

---

## 9. Imagens comprimidas

Seção com `flags & 0xFFFF == 1`. `flags >> 16` × 256 = tamanho descomprimido; 4º campo = destino na VRAM
(byte 1 = blocos por linha). Implementação: `imgcodec.py`.

**Codec** — LZ77 + Huffman no molde do LHA `-lh1-`, bits LSB-first dentro de cada byte:

- literal/comprimento: Huffman dinâmico do LHA (`dhuf.c`) com 321 símbolos — 0–255 literal, 256–320 cópia de
  3 a 67 bytes; a cada bit lido, `nó = filho[nó − bit]`;
- depois de um comprimento vem a posição: prefixo estático do `-lh1-` (6 bits altos) + 6 bits baixos
  LSB-first; distância = posição + 1; janela de 4096 bytes pré-preenchida com zeros;
- fim: símbolo 256 + posição 4095, completado com zeros até fechar o byte.

**Limite conhecido** — quando a frequência da raiz chega a `0x8000` (32768 símbolos) o jogo reconstrói a
árvore. A reconstrução divide as folhas por 2 arredondando para cima, como o LHA, mas o desempate entre nós
de mesma frequência não é o do LHA e não foi decodificado (o `reconst` do LHA acerta ~82% dos códigos
seguintes). `imgcodec` levanta `NotImplementedError` nesse ponto: seções pequenas (cartões, ícones) abrem e
regravam; 424 fluxos grandes (fundos, retratos) ainda não.

**Layout** — a imagem descomprimida são blocos de 64×32 bytes em ordem de leitura. 4bpp: nibble baixo
primeiro; 8bpp: um byte por pixel. A paleta (15 bits, 2 bytes por cor) fica numa seção separada, sem compressão.

**Títulos de capítulo** — uma única imagem 4bpp de 256×256 com os quatro títulos ("I: …" a "IV: …"), repetida
em `AREAE023:10`, `AREAE029:13`, `AREAM013:13` e `AREAM052:7`. Cada título é uma faixa de 512×32 px cortada em
duas metades empilhadas (esquerda em cima). `cards.py` redesenha em português e o `reinsert` regrava os quatro.
