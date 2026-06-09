# QA Report — Deep pass do arco (1025 linhas) exercendo a Carta de Governança

> Data: 2026-06-08. Objetivo: rodar o processo da Carta **de verdade** (risco real, back-translation,
> voz) e provar que a qualidade sobe. Complementa o `micro_qa_log.json` e o `back_translation_log.json`.

## Sumário executivo

**Status: aprovado** — 0 issues críticos. O deep pass elevou a profundidade que estava rasa (a
avaliação apontava metadados defaultados, back-translation nunca rodada, voz não verificada).

| Camada | Resultado |
|---|---|
| **Back-translation** (linhas high) | 9 revisadas → **2 revisões reais** (ambiguidade/voz) |
| **Consistência de voz** (spot-check) | 3 vozes × 7 linhas → **consistente, 0 drift** |
| **Risco cognitivo** (A1) | +4 linhas de **reveal de identidade/lore** elevadas (low→medium) |
| **Gate de validação** | pegou 1 erro de token **meu** no deep pass → corrigido (processo funcionando) |
| **Custo de produção** | medido (`cost_report.md`): $/1k 3.12→1.75; ~33k $103→$58 |

## A2 — Back-translation (a verificação que nunca tinha rodado)

Método: pt-BR → EN, comparar com o source, confirmar sentido + **ambiguidade proposital** + tom.
Detalhe completo em `back_translation_log.json`. As 2 divergências corrigidas (delta antes→depois):

| offset | source | antes | depois | por quê |
|---|---|---|---|---|
| `0x3b3b` | "I'm not gonna **make it** for you anymore." | "...fazer isso por você." | "...**poder** fazer isso por você." | `make it` é dúbio (fazer / **conseguir/dar conta**); o "poder" restaura o tom de inabilidade/despedida que se perdeu. |
| `0x3ac3` | "There'll be a whole new world **waiting for you**" | "...vai te **esperar**" | "...te **aguarda**" | voz do Homem é profética/solene (red flag: soar casual); "aguarda" devolve o peso ominoso. |

As outras 7 passaram (ambiguidade e tom preservados — ex.: "primeiro... e o último", "tomou o remédio").

## A3 — Consistência de voz (spot-check por personagem × situação)

Lidas amostras das 3 vozes principais contra os red flags do `tone_analysis.md`:
- **Kuon** (618 linhas): contraste **fofa↔firme** presente ("Não vi ferimentos" / "O bom senso diz que isso é ridículo"). ✔
- **Homem/narração da morte** (343): tensão em 1ª pessoa, observação seca. ✔
- **Protagonista** (despertar): fragmentado/semiconsciente ("Está... quente...?"). ✔

**Nenhum drift no sample.** A tradução de voz já estava sólida — registrado honestamente, sem fix forçado.

## A1 — Risco cognitivo (além dos sinais de dados)

Elevadas para **medium** 4 linhas de **reveal** que os sinais de dados não pegam (o nome é a forma
canônica, sem flag): nome da Kuon dito (`0x108db`), protagonista nomeado **Haku** (`0x12668`/`0x12702`),
1ª menção do lore **Tatari** (`0x11224`). São momentos de identidade/spoiler que merecem vigilância de
consistência. Risco do arco: **0 high → 9 high / 13 medium**.

## Limitação assumida (deferida)

O `tone_register` **fino por situação** das ~948 linhas `dialogo` **não** foi re-tagueado linha a linha
aqui — é o passe contextual de escala (meia-maratona). Este deep pass cobriu o de **maior valor**: a
verificação de alto risco (back-translation), a voz, e o reveal de identidade. Ver `decision_log.md`.

## Verificação

`pytest` conector + validação verde; `validate.py` 0 ERRO/0 aviso; `naturalness_lint.py` limpo;
round-trip byte-idêntico; resíduo T4=0. Build reflete as 2 revisões.
