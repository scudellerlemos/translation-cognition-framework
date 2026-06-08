# Conector — Utawarerumono
## Estado: ✅ POC validada (repoint + transliteração) — binário entregue

Este projeto usa o conector `hex_binary` (ver `framework/connectors/hex_binary.md`). O formato do
`ScriptEvent.sdat` foi mapeado por engenharia reversa — ver `table_schema.md`.

## Formato (resumo)

- Texto: strings UTF-8 **null-terminated** e **contíguas**; control codes são tokens ASCII literais
  (`{W75}`…). Bloco de texto começa em `0x3398`.
- Ponteiros: **inline no bytecode**, sem tabela central. Opcode de texto `50 00` (uint16 LE) +
  **ponteiro absoluto uint32 LE** para a string ("head"). Continuações = strings sem ponteiro,
  lidas em sequência após o head. **Run** = head + continuações.

## O que está feito (Passo 00 + Passo 08)

- [x] Binário entregue: `artifacts/ScriptEvent.sdat` (3,27 MB).
- [x] Mapa de caracteres / control codes (UTF-8 direto; tokens literais) — `table_schema.md`.
- [x] Tabela de ponteiros mapeada (opcode `50 00` + uint32 LE absoluto) — `table_schema.md` SEÇÃO 4.
- [x] `reinsert.py`: round-trip byte-idêntico + cascata de encaixe.
- [x] **Repoint por run** implementado (head + continuações relocados ao fim do arquivo; ponteiros
      reescritos). POC: T1=12, repoint=8 (7 runs), **resíduo T4=0**.
- [x] **Charset**: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração** na
      gravação. Evidência: `artifacts/char1.png`, `char2.png`.
- [x] Patch IPS gerado em `output/ScriptEvent.sdat.ips`.

## Próximos passos (fora desta POC)

- [ ] Confirmar in-game que as strings relocadas (apêndice ao fim do arquivo) exibem corretamente.
- [ ] Bloqueador 3: ordem offset × ordem narrativa (ver `decision_log.md`).
- [ ] Extrair o corpus completo (~33.000 linhas) e rodar o pipeline 01–08.

## Como rodar

```
python connector/extract.py  artifacts/ScriptEvent.sdat   # -> artifacts/dialogs.csv
python connector/reinsert.py artifacts/ScriptEvent.sdat   # -> output/ScriptEvent.sdat + .ips + reinsertion_report.md
pytest  connector/                                        # gate de regressão (round-trip + ponteiros + IPS)
```

O formato é parseado por `connector/sdat_format.py` (módulo único compartilhado por extract e
reinsert — garante o round-trip). O escopo extraído é controlado por `SCENES` em `extract.py`
(prefixos de nome de script; atual: `11_01` + `11_02`).

O caminho do binário **nunca** é hardcoded: vem do argumento de CLI ou de
`connector.source_binary` no `project.json` (relativo à raiz do projeto).

## Testes (regressão)

`connector/test_roundtrip.py` (pytest) trava os invariantes do conector:
round-trip de identidade byte-a-byte, binário-fonte intacto, cada tradução lida pela posição final
== transliteração do alvo, e patch IPS aplicável. Rodar antes de qualquer entrega.
