# Conector — Utawarerumono
## Estado: ✅ validado in-game (1025 linhas; relocação intra-arquivo + Pack)

Este projeto usa o conector `hex_binary` (ver `framework/connectors/hex_binary.md`). O formato do
`ScriptEvent.sdat` foi mapeado por engenharia reversa — ver `table_schema.md`.

## Formato (resumo)

- Container: `Filename` (header) → tabela de nomes → `Pack` (count + (offset,size) por arquivo) →
  **353 scripts contíguos, alinhados a 16 bytes**. Cada script = `[bytecode STSC][bloco de texto]`.
- Texto: strings UTF-8 **null-terminated** e **contíguas**; control codes são tokens ASCII literais (`{W75}`…).
- Ponteiros: **inline no bytecode**, sem tabela central. Opcode `50 00` (uint16 LE) + **uint32 LE
  RELATIVO ao início do arquivo** (alvo_abs = file_start + uint32; **não é absoluto**). Continuações =
  strings sem ponteiro, lidas em sequência após o head. **Run** = head + continuações.

## O que está feito (Passo 00 + Passo 08)

- [x] Container `.sdat` totalmente mapeado (`parse_pack`, `rebuild_container`) — `table_schema.md`.
- [x] **Modelo de ponteiro FILE-RELATIVO** (correção crítica; ~42k sites confirmam vs ~63 absolutos) —
      `table_schema.md` SEÇÃO 4.
- [x] `reinsert.py`: round-trip byte-idêntico + cascata de encaixe (1025 linhas: T1=595, RELOC=430, **resíduo T4=0**).
- [x] **Relocação INTRA-ARQUIVO**: o run que estoura é anexado ao fim da região do próprio arquivo; o
      arquivo cresce e a tabela Pack é reescrita (`rebuild_container`, padding a 16 bytes); ponteiro =
      offset local. (EOF-append ao fim do container foi **reprovado in-game**.)
- [x] **Charset**: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração** na
      gravação. Evidência: `artifacts/evidence/char1.png`, `char2.png`.
- [x] **Validação in-game ✅**: pt-BR exibe (`artifacts/evidence/Fasea*.png`); linha relocada pelo Plano B
      exibe e o jogo avança sem travar (`artifacts/evidence/testeplanob.png`, `testeplanob_avanco.png`).
- [x] Patch IPS gerado em `output/ScriptEvent.sdat.ips`.

## Próximos passos

- [ ] Ordem offset × ordem narrativa para cenas distantes (ver `decision_log.md`).
- [ ] 2ª metade do jogo (~33k linhas no total) — extração por capítulo via `extract_chapter.py`;
      caps 11–13 já traduzidos/verificados pelo harness (`framework/runtime/`).

## Como rodar

```
python connector/extract.py  artifacts/ScriptEvent.sdat   # -> artifacts/dialogs.csv
python connector/reinsert.py artifacts/ScriptEvent.sdat   # -> output/ScriptEvent.sdat + .ips + reinsertion_report.md
pytest  connector/                                        # gate de regressão (round-trip + ponteiros + IPS)
```

O formato é parseado por `connector/sdat_format.py` (módulo único compartilhado por extract e
reinsert — garante o round-trip). O escopo extraído é controlado por capítulo via
`connector/extract_chapter.py` (prefixos de nome de script por capítulo, ex.: `13` → `ch_13_*`); caps
11–13 já extraídos e traduzidos.

O caminho do binário **nunca** é hardcoded: vem do argumento de CLI ou de
`connector.source_binary` no `project.json` (relativo à raiz do projeto).

## Testes (regressão)

`connector/test_roundtrip.py` (pytest, **16 testes**) trava os invariantes do conector: round-trip de
identidade byte-a-byte, binário-fonte intacto, modelo file-relativo, cada head relocado aponta para
**dentro do seu arquivo** com a string traduzida correta (`test_planob_within_file`), integridade do
Pack reconstruído (contíguo/alinhado/nomes/footer — `test_pack_rebuild_integrity`), patch IPS
aplicável, e o **guard de governança** (nenhum texto da obra hardcoded em `.py`). Rodar antes de entregar.
