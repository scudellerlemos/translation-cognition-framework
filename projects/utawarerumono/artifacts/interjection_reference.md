# Referência de interjeições — Utawarerumono (EN → pt-BR)

> Artefato de **dados curados** (convenção do projeto), não código. Consumido na revisão de
> naturalidade (Passos 06/06b/07). Princípio: interjeição/onomatopeia é **tradução** — localizar à
> convenção do pt-BR, com **coerência** em todo o corpus.
>
> ⚠️ **Restrição do conector:** o `reinsert.py` **translitera** na gravação (a fonte do jogo não tem
> acentos — ver `decision_log.md`). Logo, evitar formas que dependem de acento/til, que viram outra
> coisa no jogo: `Hã?`→`Ha?` (lê como riso), `Ué?`→`Ue?`. As formas abaixo são **robustas a ASCII**.

## Convenção por emoção/situação

| Emoção / situação | Source (EN) típico | pt-BR (convenção do projeto) | Observação |
|---|---|---|---|
| Dúvida / "o quê?" / notar algo | `Hm?`, `Nh?`, `...Hm?`, `Hm...?` | `Hein?`, `...Hum?`, `Hum...?` | `Hum?` = reflexivo; `Hein?` = não entendeu |
| Gemido baixo / despertar dolorido | `Ngh...`, `Nn...`, `Ngh... ghh...` | `Nnh...`, `Mn...`, `Nnh... aagh...` | esforço/dor surda |
| Dor súbita / pancada | `Gah!`, `Guh--`, `Ghh!` | `Ai!`, `Agh--`, `Agh!` | `Ai!` = dor/susto súbito, muito pt-BR |
| Agonia contínua | `Urgh...`, `Ghh...`, `Agh...` | `Argh...`, `Argh...`, `Argh...` | já usado no corpus; padronizar |
| Esforço (segurar/puxar) | `H-Hgh!`, `Hngh!` | `Hngh!`, `Nngh!` | tensão muscular |
| Engasgo / susto que prende o ar | `Hk--`, `Hgh--` | `Hgh--`, `Kh--` | corte seco |
| Grito puro (vogais) | `Aaaaah!`, `Waaaah!`, `EEEYAAAGH!` | manter/espelhar (`Aaaaah!`, `IIIAAAH!`) | só vogais → já universal |
| Reação leve / alívio / "ah" | `Ah...!`, `...Ah!`, `...Ah.` | manter `Ah...!`, `...Ah!`, `...Ah.` | já natural em pt-BR |
| Riso | `Hah`, `Heh`, `Fufu` | `Há`→`Haha`, `Hehe`, `Fufu` | sem depender de acento isolado |

## Regras

1. **Nunca** deixar `base_translation == text_source` numa interjeição, salvo: grito só de vogais, ou
   nome próprio sendo soletrado (`Ha... ku...` = "Haku").
2. **Coerência:** a mesma situação usa a mesma forma em todo o corpus (ex.: todo gemido de dor = `Nnh...`).
3. **byte_budget:** não é mais trava dura (o conector reloca overflow — Plano B); ainda assim preferir
   a forma natural mais curta.
4. Tradução pela **emoção/situação** (campo `intent`/`tone_register` do plano), não pela letra do source.
