# Pares de Identidade Dupla — [TÍTULO]
## Template (consumido pelas skills genéricas)

> No pipeline real, os pares são capturados no `aliases_map.json` / `entities.csv` (alias com
> `spoiler_level` + `reveal_timing`). Preencha aqui o que já se sabe como referência.
>
> Cada par exige: (a) suite de teste de distinção no Passo 5b, (b) verificação cross-segmento no
> QA Final, (c) gestão de spoiler que impede o nome revelado de aparecer antes do `reveal_timing`.

---

## Pares

| Persona pública | Identidade revelada | Spoiler level | Contraste de voz |
|-----------------|---------------------|---------------|------------------|
| [persona A] | [identidade A] | critical | [traço público] ⟷ [traço revelado] |

---

## Regras de separação (por par)

- Nunca usar o nome da identidade revelada antes do `reveal_timing`.
- Nunca deixar a voz da identidade revelada vazar na persona pública.
- Os dois nomes de um par não podem aparecer juntos em contexto de spoiler.

---

## Entidades pré-reveal especiais (não-personagem)

| Entidade | Tratamento pré-reveal |
|----------|----------------------|
| [entidade] | [como tratar antes do reveal de sua natureza] |
