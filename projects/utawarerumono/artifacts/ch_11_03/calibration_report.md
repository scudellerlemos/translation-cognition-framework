# Relatório de Calibração — Cap. 11_03_000C (118 linhas)

> Data: 2026-06-08. Objetivo: rodar **1 capítulo do zero** em modo **padrão** (extração →
> discovery/glossário → tradução com a Carta → micro-QA + back-translation nas high → reinsert +
> round-trip) pra estabelecer (a) que o pipeline funciona incremental/resumível e (b) o **ritmo**
> e o **custo** da meia-maratona até o cap. 25.

## O que foi feito (end-to-end, padrão)

| Etapa | Resultado |
|---|---|
| Extração isolada | `ch_11_03/dialogs.csv` — 118 linhas, 4.025 bytes de texto (não tocou o build de 1025) |
| Discovery/glossário | 1 termo de mundo novo: **`toriuma`** (ave-montaria) → adicionado ao `glossary.csv` |
| Tradução (Carta) | 118 linhas; voz Haku (irônico/pânico cômico) + Kuon (fofa↔firme); interjeições localizadas |
| Risco cognitivo | **12 high / 29 medium / 77 low** (comédia, voz-crítica, 1ª menção de lore, rótulos ambíguos) |
| Back-translation | 10 high de fala → **1 revisão real** (`bom senso indo embora`→`evaporando`) |
| Linter naturalidade | limpo (4 achados, todos esperados: 2 gritos animais + 2 rótulos `needs_review`) |
| Reinsert + round-trip | **118/118 verificadas**, round-trip byte-idêntico, **resíduo T4=0**, 0 ponteiro fora-do-arquivo |
| pytest | 29/29 verde |
| Pendência sinalizada | rótulos internos `Head` / `Head_toriuma` → `needs_human_review` (verificar in-game se exibem) |

**A Carta pegou coisa real:** a back-translation revisou uma tirada-assinatura do Haku; o risco
cognitivo elevou 41 linhas (de comédia/voz/lore) que os sinais de dados não pegam; e o processo
**sinalizou** (não inventou) os 2 rótulos ambíguos — exatamente o comportamento contratado.

## Custo de PRODUÇÃO (API, caminho de chave própria — NÃO é o seu caminho de assinatura)

Tokens estimados (≈chars/3.8) sobre o conteúdo real do capítulo; preços via skill `claude-api`
(Opus 4.8 $5/$25 por Mtok), contexto estável (glossário+Carta+tone ≈6k tok) via prompt caching.

| Métrica | Cap. 11_03 | Projeção meia-maratona (~16.000 linhas ≈ 136× este cap.) |
|---|---|---|
| source | ~1.059 tok | — |
| plano+metadados (saída) | ~3.328 tok | — |
| **custo/capítulo** | **~$0,135** | — |
| **$/1k linhas** | **~$1,14** | — |
| **total** | — | **~$18** (R$ ~100, uma vez) |

> Bem **abaixo** do `cost_report.md` anterior ($/1k 1,75–3,12; ~33k → $58–103). Por quê: aqui o
> modelo conta **só** tradução + micro-QA + back-translation nas high (modo padrão), com caching do
> contexto; o report antigo era pessimista (lotes redundantes, sem assumir caching pleno). O número
> real do capítulo é a baseline mais confiável.

## Consumo de JANELA (caminho da assinatura — o SEU caminho)

No modo assinatura **não há conta de API**: o custo é a **janela de uso** do plano. 1 capítulo de
~118 linhas com o processo padrão completo (incluindo as 3 iterações de depuração da verificação,
que não se repetem) **coube com folga** numa fração da janela. Estimativa conservadora de ritmo:

- **~6–10 capítulos deste tamanho por janela** em regime (sem a depuração inicial de ferramenta).
- Meia-maratona ≈ **136 capítulos** deste tamanho → **~15–25 janelas**, feita incremental.
- O `translation_status.json` marca `next_offset`; cada janela retoma de onde parou, **sem refazer**.

> Observação honesta: não tenho telemetria exata da janela de dentro da sessão; o ritmo acima é
> estimativa pela massa de trabalho real deste capítulo. As 2 primeiras janelas reais vão calibrar
> o número fino — daí em diante o ritmo é previsível.

## Veredito

Pipeline **incremental e resumível validado**: 1 capítulo do zero, qualidade-Carta, round-trip
íntegro, 0 resíduo. Custo de produção ínfimo ($/1k ~$1,14); no caminho assinatura, o limite é só
ritmo (~15–25 janelas pra meia-maratona). **Pronto pra escalar** capítulo a capítulo.

## Artefatos deste capítulo
`ch_11_03/`: `dialogs.csv`, `translations_11_03.json` (curado), `translation_plan_11_03.json`,
`approved_11_03.csv`, `back_translation_11_03.json`, `calibration_report.md`.
Conector: `build_plan_11_03.py` (merge sem work-text), `verify_11_03.py` (round-trip dirigido por ponteiro).
