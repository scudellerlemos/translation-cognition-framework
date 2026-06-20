# Table Schema — Breath of Fire IV (PC Port, Capcom 2000)

> Status: **MAPEADO** — análise do diretório english/DAT em 2026-06-20

---

## 1. Arquivos de diálogo

O jogo usa um container binário com TOC (Table of Contents). O mesmo formato
se aplica a todos os tipos:

| Família | Conteúdo | Exemplo |
|---|---|---|
| `AREAD*.DAT` | Diálogo principal de cenas (field events) | `AREAD001.DAT` |
| `AREAS*.DAT` | Scripts de área (cutscenes, NPCs avançados) | `AREAS001.DAT` |
| `AREAE*.DAT` | Eventos de área (encuentros, interações) | `AREAE001.DAT` |
| `AREAM*.DAT` | Mapas (NPC dialog de campo aberto) | `AREAM000.DAT` |
| `SHOP.DAT`, `CAMP.DAT`, `DEMO.DAT` | UI de loja, menu camp, demo/intro | — |

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
                            PTR_TABLE_SIZE variável para SHOP/CAMP/DEMO
[PTR_TABLE_SIZE:end]      = strings null-terminadas (\x00) em ASCII
```

Cada entrada da tabela de ponteiros é um uint16 = offset da string dentro desta seção.
Entradas duplicadas = aliases (dois slots apontam para a mesma string).

---

## 4. Encoding

**ASCII puro** para o PC port em inglês (bytes 0x20–0x7E são caracteres diretos).
Bytes fora desse range são tokens de controle — representados como `[XX]` no CSV.

---

## 5. Tokens de controle conhecidos

| Token (hex) | Representação CSV | Significado |
|---|---|---|
| `00` | fim de string | terminador null |
| `01` | `[01]` | newline dentro da caixa de diálogo |
| `02` | `[02]` | page break (aguarda input, abre nova caixa) |
| `04` | `[04]` | variável: nome de personagem (dinâmico) |
| `05` | `[05]` | variável: nome de item/magia (dinâmico) |
| `0A` | `[0A]` | efeito sonoro / voz |
| `0B` | `[0B]` | pausa breve (ellipsis beat) |
| `0C` | `[0C]` | comando de evento (seguido de bytes de parâmetro) |
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
