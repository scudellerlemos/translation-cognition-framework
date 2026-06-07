# Extraction Log — Utawarerumono: Mask of Deception (POC)

**Data:** POC
**Conector:** hex_binary (`connector/extract.py`)

## Fonte
- **Binário:** `Data/ENG/ScriptEvent.sdat` (Steam) — 3.274.096 bytes
- **Container:** header `"Filename    "` + tabela de offsets; strings UTF-8 **null-terminated contíguas**
- **Encoding:** UTF-8 (texto em claro, não comprimido/encriptado)

## Extração (POC)
- **Escopo:** 20 primeiras linhas a partir da 1ª fala (`0x3398`)
- **Faixa de offsets:** `0x3398` → `0x35ed`
- **id_column:** offset hex · **byte_budget:** bytes da string (sem `\0`)

## Control codes (confirmados no texto real)
- `{W75}`, `{W80}`, `{W10}` — timers (batem com `project.json → formatting_tokens`)
- `\n` — quebra de linha como token literal (backslash-n)
- Linhas de sistema em CAPS (bate com `system_line_convention: all_caps`)

## Gate de round-trip
- **PASSOU** — `extract.py` → `reinsert.py` (sem mudanças) reproduz o `.sdat` byte-a-byte idêntico.

## Gate de charset (pt-BR)
- **Método empírico falhou em confirmar** (fonte é inglês, que quase não usa acentos).
- Confirmados renderizados em texto real: `õ` (U+00F5), `À` (U+00C0).
- Demais acentos pt-BR vivem no mesmo bloco Latin-1 Supplement → **suporte provável**.
- **Ação:** confirmar in-game com pangrama pt-BR, ou parsear o `Font.fnt` (formato `"Table"`).
- `target_charset_supported: likely`

## Anomalias detectadas
- `0x33f9`: "INICIANDO PROCESSO DE DESPERTAR. SISTEMAS AM . RESTARTING IN 5 SECONDS." — **texto já vem misturado PT/EN e corrompido no próprio jogo** (não é erro da extração). Marcar como anomalia de fonte.

## Limitações
- **Ordem por offset ≠ ordem de exibição.** A ordem narrativa real é controlada pelo script (comandos que referenciam strings por ponteiro). A POC usa ordem por offset (aproximação válida para a cena de abertura).
