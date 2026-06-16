# Extraction Log — Utawarerumono: Mask of Deception

**Data:** 2026-06-08
**Conector:** hex_binary (`connector/extract.py` + `connector/sdat_format.py`)

## Fonte
- **Binário:** `artifacts/ScriptEvent.sdat` (origem: Steam, `Data/ENG/ScriptEvent.sdat`) — 3.274.096 bytes
- **Container:** header `"Filename    "` + tabela de nomes (registros de 15 bytes `CC_SS_NNNT.BIN`)
  + seção `"Pack        "` (count + count×(offset,size) interleaved). **353 scripts**, capítulos 11–39.
- **Cada script:** `[bytecode 'STSC' + opcodes][bloco de texto: strings UTF-8 null-terminated contíguas]`.
- **Encoding:** UTF-8 (texto em claro, não comprimido/encriptado).

## Escopo extraído (corpus de teste em escala)
- **Cenas:** `11_01` (sub-scripts `000S`/`100C`/`150S`) + `11_02` (`000S`) — `SCENES=("11_01","11_02")`.
- **Total de strings:** **1025 linhas** (despertar → fuga na caverna [inseto gigante → Tatari] →
  resgate por Kuon → cena de vestir → nome **Haku**), em **ordem de armazenamento = narrativa**.
- **id_column:** offset hex · **byte_budget:** bytes da string (sem `\0`).
- **Limpeza de extração:** `extract_text_block` apara ruído de bytecode nas bordas (denylist `STSC`/
  `Head`/`head` + trim) e rejeita nomes de script (`.BIN`). `11_01_150S` ficou com 0 linhas (script vazio).
- Para mais cenas, ajustar `SCENES`. Tamanhos: 11_01≈470, 11_02≈557, 11_03≈119; caps. 11+12 ≈4519.

## Control codes (confirmados no texto real)
- `{W75}`, `{W80}`, `{W10}` — timers (batem com `project.json → formatting_tokens`).
- `\n` — quebra de linha como token literal (backslash-n, 2 bytes ASCII).
- Linhas de sistema em CAPS (bate com `system_line_convention: all_caps`).

## Ponteiros
- **Sem tabela central.** Falas referenciadas inline pelo opcode `50 00` (uint16 LE 0x0050) + ponteiro
  absoluto uint32 LE. Strings são um **pool reusado** (a mesma fala é referenciada de vários scripts).

## Gate de round-trip
- **PASSOU** — `extract.py` → `reinsert.py` (sem traduzir) reproduz o `.sdat` byte-a-byte idêntico.
  Travado por teste automatizado `connector/test_roundtrip.py` (pytest, 4 testes).
- Aplicação real (1025 traduções, modelo FILE-RELATIVO): T1=595, REPOINT_head=425, REPOINT_cont=5,
  **resíduo T4=0**; verificação do valor do ponteiro 100% (file_start+valor).

## Gate de charset (pt-BR)
- **FALHOU (confirmado in-game).** Pangrama pt-BR (`áéíóú âêô ãõ ç ÁÉÍ ÃÕ`) renderiza os acentos como
  `@` — evidência: `artifacts/evidence/char1.png`, `artifacts/evidence/char2.png`. A fonte do jogo não tem os glifos.
- **Decisão:** `target_charset_supported: false` → **transliteração na gravação** (acento→ASCII no
  `reinsert.py`); a tradução canônica mantém os acentos. Ver `decision_log.md`.

## Notas
- `0x33f9` **não é anomalia**: o binário-fonte está íntegro ("INITIALIZING AWAKENING PROCESS." em
  `0x33f9`, "SYSTEMS YELLOW. RESTARTING IN 5 SECONDS." em `0x3419`). O "corrompido PT/EN" anterior era
  artefato de uma extração sobre um `.sdat` já modificado pela POC. Ver `decision_log.md`.
- `0x3937` "I'm gonna cook you your favorite      !" tem 6 espaços (lacuna proposital) — preservar.
