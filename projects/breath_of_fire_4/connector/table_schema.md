# Table Schema — Breath of Fire IV

> Status: **FASE 00 — MAPEAMENTO PENDENTE**
>
> Este arquivo deve ser preenchido durante o Passo 00 (Extração) com base na
> análise do hex dump dos arquivos de diálogo do jogo.
>
> Referência: `framework/connectors/hex_binary.md` e
> `projects/utawarerumono/connector/table_schema.md`.

---

## O que precisa ser mapeado

### 1. Localizar os arquivos de diálogo

- Identificar quais arquivos no diretório de instalação contêm strings de diálogo legíveis.
- Candidatos típicos em jogos Capcom PS1/PC: arquivos `.BIN`, `.DAT`, `.ARC`.
- Método: abrir no HxD e buscar strings reconhecíveis do jogo ("Ryu", "Cray", "Nina").

### 2. Encoding / charset

- [ ] ASCII puro?
- [ ] Shift-JIS com tabela de substituição?
- [ ] Encoding customizado com tabela própria?
- [ ] Suporte a diacríticos? (validar com pangrama pt-BR in-game)

### 3. Estrutura de cada string

- [ ] Terminador: `\x00`? comprimento prefixado? outro?
- [ ] Tokens de controle (quebra de linha, pausa, cor, nome do personagem)?

### 4. Estrutura de ponteiros

- [ ] Inline (no bytecode, como SDAT)?
- [ ] Tabela central (offsets de todas as strings num header)?
- [ ] Sem ponteiro (strings contíguas, tamanho fixo)?

### 5. Restrições de tamanho

- [ ] Byte budget por string?
- [ ] Limite de caracteres por linha de diálogo?
- [ ] Limite de linhas por caixa de diálogo?

---

## Tabela de caracteres

> Preencher após análise do hex dump.

| Byte(s) hex | Char / Token | Notas |
|---|---|---|
| TBD | TBD | TBD |

---

## Tokens de controle

> Preencher após análise.

| Token | Byte(s) hex | Significado |
|---|---|---|
| TBD | TBD | TBD |

---

## Notas de mapeamento

> Registrar descobertas incrementais durante o Passo 00.

*(vazio — preencher durante a análise)*
