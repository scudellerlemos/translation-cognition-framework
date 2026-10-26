# TABLE SCHEMA — Utawarerumono: Prelude to the Fallen (conector próprio)

Formato mapeado do zero (Fase 0) a partir do `DataBase2.sdat` da instalação Steam; nada reaproveitado de outro
projeto. Compartilhado por `extract.py` e `reinsert.py` (o parser mora no `extract.py`). Todos os inteiros são
`uint32` little-endian. O arquivo-fonte do texto é **`Data/DataBase2.sdat`** (fora do repo; gitignored).

---

## SEÇÃO 0 — CONTÊINER `.sdat`

```
0x00  "Filename    "  (12 bytes, tag com espaços)
0x0C  u32 end        fim do bloco de nomes menos 1 (informativo)
0x10  u32 name_off[]  tabela de offsets dos nomes (relativos a 0x10); o 1º valor marca onde ela termina
...   nomes ASCII terminados em NUL, um por membro, na ordem de `Pack`
      (a tabela de offsets NÃO cobre todos os nomes: os últimos vêm em sequência; separar o bloco por NUL)
pk    "Pack        "  (12 bytes)
pk+12 u32 section_size   = 20 + 8*count - 20 (informativo)
pk+16 u32 count
pk+20 (u32 offset, u32 size) * count   offsets ABSOLUTOS no arquivo; membros contíguos
      alinhamento: o 1º membro começa no próximo múltiplo de 16 depois da tabela
...   membros (bytes crus, sem compressão nem cifra)
...   cauda (bytes após o último membro; preservada byte a byte)
```

- Sem compressão, sem cifra, sem checksum observado. `binwalk` não reconhece assinatura (contêiner próprio).
- Reconstrução: cabeça (até o 1º membro) e cauda são copiadas; só `offset`/`size` de `Pack` são recalculados.

## SEÇÃO 1 — MEMBROS DE TEXTO (`ScriptTextData_<cap>_<sub>_<n>.bin`)

```
u32 n                       número de falas (linhas)
u32 ptr[n * cols]           offsets (relativos ao início do membro), linha a linha
pool                        strings UTF-8 terminadas em NUL, contíguas, na ordem dos ponteiros
```

- `cols = (ptr[0] - 4) / (4 * n)`. Padrão: `cols = 4`, na ordem fixa **JA, KO, ZH, EN**; a coluna `EN` (índice 3)
  é o texto-fonte da tradução.
- Layout "estrito" que o conector aceita: ponteiros estritamente crescentes, `ptr[0] = 4 + 4*cols*n`, cada
  string termina exatamente onde a próxima começa, o pool acaba no fim do membro, nenhum ponteiro repetido.
  Nesse layout, reconstruir o membro a partir das strings reproduz os bytes originais.
- Membros fora do padrão ficam **fora da extração** e são listados no `extraction_log.md` (não são trocados
  em silêncio): `ScriptTextData_10_84_00` (3 colunas, sem EN).
- `StageTextData` (nomes das fases de batalha, 50 linhas) entra na extração por um leitor próprio
  (`read_stage_member`). O pool traz JA, KO, ZH, EN em sequência, mas os ponteiros do jogo estão defeituosos
  (coluna 3 aponta o ZH; coluna 2 cai de -10 a +21 bytes em torno do EN; a linha 24 tem EN vazio). O leitor lê
  o pool, não os ponteiros; a reinserção (`build_stage_member`) aponta as colunas 2 e 3 para o EN/PT, e o pool
  não muda de ordem. Testes: `test_stage_member.py`.
- `NameTextData`, `SysMessageTextData`, `UnitTextData` têm o mesmo layout, mas são escopo de UI/nomes
  (decisão de escopo `dialogo` × `completo` pendente do usuário; ver ROADMAP).

## SEÇÃO 2 — CÓDIGOS DENTRO DO TEXTO EN

Texto puro UTF-8; os códigos viajam como caracteres ASCII (nada de byte de controle), então passam intactos
pelo CSV. Preservar verbatim na tradução (`project.json → formatting_token_patterns`):

| Código | Observado | Papel |
| --- | --- | --- |
| `\n` (barra + `n`, 2 caracteres) | quebra de linha | |
| `\R` | raro | tratado como token opaco |
| `{W<n>}` | espera/pausa de `n` quadros | |
| `{c<n>}`, `{c-1}` | cor | |
| `{i<n>}` | ícone | |
| `{g<n>}` | glifo de botão | |
| `[Título]` | rótulo de tutorial | texto, traduzível |

Nas colunas JA/KO/ZH aparece ruby `[kanji*furigana]`; **não existe na coluna EN** (a coluna EN não é lida pelo
parser de ruby). Linhas EN vazias (37) não entram no corpus e ficam como estão.

## SEÇÃO 3 — TERMINADORES E ESTRUTURA

- Terminador de string: `00`. Nenhum código leva `00` como parâmetro (os códigos são ASCII imprimível).
- Alinhamento: strings sem alinhamento (contíguas). Base de offset: relativa ao início do membro.
- `byte_budget` = bytes UTF-8 da string + 1 (terminador). **Não é limite duro**: o membro é reconstruído
  (`space_strategy: reconstrucao_secao`), então não há resíduo por espaço; o limite real é a largura da caixa
  na tela (skill 08c, a medir no jogo) e `length_constraints` do `project.json`.

## SEÇÃO 4 — PONTEIROS

Tabela de `u32` por membro, descrita na Seção 1. O `ScriptEvent.sdat` (bytecode `STSC`) referencia o texto por
índice e **não é alterado**.

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO (gate)

O texto EN (diálogo e menu) é desenhado com `Data/ENG/Texture/font.tex` (atlas RGBA 256x256, só o alpha desenha;
LZ77 do formato Steam) e uma tabela BMFont binária embutida no exe (fonte "KoreanPGDM", 121 entradas de 20 B:
`u32` código Unicode ordenado + `x,y,w,h,xoffset,yoffset,xadvance` + page + chnl; achada pela string
`KoreanPGDM_26_binary_0.tga`). `Data/Font.fnt` (fonte japonesa) NÃO é usado pelo texto EN. A tabela não tem
á à â ã é ê í ó ô õ ú ç (nem maiúsculas), aspas curvas, `…` nem `—`; caractere ausente cai em `@`.

Solução (`connector/font.py`, confirmada in-game): as 24 letras acentuadas são o glifo da letra-base copiado do
próprio atlas + acento feito dos traços da própria fonte (`` ` `` espelhado, `~`, `,`, `^` reduzidos), em área
livre do atlas (linha >= 178; 1 linha em branco no topo, senão a borda corta o acento). Cada glifo novo reaproveita
a entrada de um glifo que nenhum EN usa (`SACRIFICE`: `× ™ □ △ ◇ ○ ☆ ✖ ⑪–⑯ { } \ | ^ ` _ < # $`; o `~` NÃO entra: o EN o desenha (60 usos, nas cantigas `♪~♪~~`) e sem a entrada ele vira `@`), então a tabela e o
exe mantêm o tamanho; a tabela é reordenada por código. Sem patch global de fonte: o visual é o da fonte original.
`reinsert.py` normaliza o que a tabela não tem (`“ ” « »`→`"`, `‘ ’`→`'`, `–`→`-`, `—`→`―`, `…`→`...`).
Instalação (manual, jogo fechado): `python connector/font.py <exe original> <font.tex original> <dir>` e copiar
`game.exe`→exe do jogo e `font.tex`→`Data/ENG/Texture/`. Teste: `UTAP_BACKUP=<backup_original> pytest connector/test_font.py`.
Plano B: `connector.diacritic_strategy = "transliterate"`.
