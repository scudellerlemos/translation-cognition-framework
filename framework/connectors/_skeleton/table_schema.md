# TABLE SCHEMA — formato
## Schema de tabela compartilhado por extract.py e reinsert.py

> Este é o formato do arquivo de tabela que ambos os scripts consomem. Cada projeto cria o seu em
> `projects/<título>/connector/table_schema.md` (ou `.tbl`) a partir da análise do binário.
> Manter o schema **estável e único** é o que garante o round-trip.

---

## SEÇÃO 1 — MAPA DE CARACTERES (byte → caractere)

Estilo romhacking `.tbl`: uma entrada por linha, `HEX=char`.

```
41=A
42=B
61=a
62=b
20=(espaço)
...
```

A largura pode ser fixa (1 byte/char) ou variável (multi-byte). Documentar qual.

- **Encoding:** `custom` | `ascii` | `shift-jis` | `utf-8` | ...
- **Largura:** `fixed-1` | `fixed-2` | `variable`

---

## SEÇÃO 2 — CONTROL CODES (sequência de bytes → token)

Bytes que não são texto e viram tokens no `dialogs.csv`. Devem bater com `project.json → formatting_tokens`.

```
FF=  {END}
FE 4B=  {W75}
FE 50=  {W80}
FE 0A=  {W10}
FD=  \n
FC ??=  {COLOR}
```

`reinsert.py` faz o mapeamento inverso (token → bytes).

---

## SEÇÃO 3 — TERMINADORES E ESTRUTURA

- **Terminador de string:** byte(s) que encerram uma string (ex: `00` ou `FF`)
- **Alinhamento:** strings começam em offsets alinhados? (ex: múltiplos de 2/4)
- **Base de offset:** offset absoluto no arquivo, ou relativo a uma base?

---

## SEÇÃO 4 — PONTEIROS (se aplicável)

- **Localização da tabela de ponteiros:** offset onde começa
- **Formato:** endianness + largura (ex: `little-endian 16-bit`)
- **Cálculo:** ponteiro = offset absoluto? offset relativo a uma base? índice?

---

## SEÇÃO 5 — COBERTURA DE CHARSET DO ALVO

Listar caracteres do idioma-alvo **ausentes** na fonte/tabela (gate de charset):

```
ã -> AUSENTE  (precisa expandir fonte OU transliterar para 'a')
ç -> AUSENTE
õ -> AUSENTE
é -> presente (0x..)
```

Se houver ausências, registrar a decisão (expandir fonte vs transliterar) no `decision_log.md`.
