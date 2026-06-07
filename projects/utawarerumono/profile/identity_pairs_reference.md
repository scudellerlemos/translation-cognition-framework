# Pares de Identidade Dupla — Utawarerumono: Mask of Deception
## Dados de referência do projeto (consumido pelas skills genéricas)

> No pipeline real, os pares de identidade são capturados pelo Passo 1/2 no
> `aliases_map.json` e `entities.csv` (alias com `spoiler_level` + `reveal_timing`).
> Este arquivo registra os pares deste título como referência e exemplo.
>
> **Por que importa:** cada par exige (a) uma suite de teste de distinção no Passo 5b,
> (b) verificação cross-segmento no QA Final (Passo 7), e (c) gestão de spoiler que
> impede o nome revelado de aparecer antes do `reveal_timing`.

---

## Pares

| Persona pública | Identidade revelada | Spoiler level | Contraste de voz |
|-----------------|---------------------|---------------|------------------|
| Ukon | Oshtor | critical | Relaxado/seco ⟷ formal/grave, linguagem de corte |
| Sakon | Mikazuchi | critical | Caloroso/alegre ⟷ gelado/econômico (o maior contraste do jogo) |
| Mito | Mikado | critical | Velho cansado ⟷ autoridade imperial |

---

## Regras de separação (por par)

- **Nunca** usar o nome da identidade revelada em segmentos anteriores ao `reveal_timing`.
- **Nunca** deixar a voz da identidade revelada vazar na persona pública (ex: frieza de Mikazuchi nas falas de Sakon).
- Os dois nomes de um par **não podem aparecer juntos** no mesmo segmento em contexto de spoiler.
- Teste de retrospecto para Sakon: "isso soaria irônico se o leitor já soubesse que é Mikazuchi?" Se sim → revisar.

---

## Entidades pré-reveal especiais (não-personagem)

| Entidade | Tratamento pré-reveal |
|----------|----------------------|
| Tatari | Monstro puro, sem pathos, sem humanidade sugerida — antes do reveal de sua natureza |
