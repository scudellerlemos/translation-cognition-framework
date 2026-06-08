# Conector — Utawarerumono
## Estado: ⏳ aguardando o binário

Este projeto usa o conector `hex_binary` (ver `framework/connectors/hex_binary.md`). Os scripts
`extract.py` e `reinsert.py` serão escritos a partir dos esqueletos em
`framework/connectors/_skeleton/` **quando o binário do jogo for fornecido** e analisado no HxD.

## O que falta para o Passo 00 rodar

- [ ] Usuário **entrega** o `.sdat`: copia para `artifacts/` (aponta `connector.source_binary` relativo) **ou** passa o caminho por CLI. A pasta da Steam (`Data/ENG/ScriptEvent.sdat`) é só a **localização de origem** — nunca um caminho absoluto na config.
- [ ] Mapear a tabela de caracteres (byte→glifo) em `table_schema.md`
- [ ] Mapear os control codes para os bytes reais (`{W75}`, `{W80}`, `{W10}`, `{COLOR}`, `{END}`)
- [ ] Localizar a tabela de ponteiros (`pointer_table.location` / `format`)
- [ ] Avaliar o gate de charset: a fonte do jogo tem os diacríticos do pt-BR (ã, ç, õ, á, ê...)?
- [ ] IA escreve `extract.py` e `reinsert.py` a partir dos esqueletos
- [ ] Rodar o gate de round-trip: extract → reinsert(idêntico) === binário original

## Observações conhecidas

- Os offsets do corpus são hex (ex: `0x33cd`, `0x998e`), confirmando endereçamento direto no binário.
- `space_strategy: in_place` + `length_constraints.mode: byte_space` — a tradução pt-BR deve caber
  no orçamento de bytes de cada string (shift-left no Passo 06).
- `patch_format: ips` — a entrega final é um patch IPS.
