# Fase 0 — capitulo 39 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 39 --check`.

- cenas do capitulo: 39_00, 39_01, 39_10, 39_17
- research_log reconciliado: sim
- nao cobertos: **0 bloqueante(s)** (recorrem >=2 cenas) + 1 de baixa confianca | fracos (ruido): 10 | ja cobertos: 1

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Dream Arena | — | 2 | 39_01 | 39_01 | {c5}Dream Arena{c-} has been added t… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Cannot | 1 | …I went through in my dreams!? Cannot comprehend. Perhaps the e… |
| Deilnidrah | 1 | …d close your eyes. L-Like this? Deilnidrah, deilnidrah... Suoluc… |
| Hooooooff | 1 | …er job well done today, Master. Hooooooff... Yeah, that's the sp… |
| Nnngh | 1 | …for you to wake up. *Yawn*... Nnngh... I feel like I had a rea… |
| Satisfaction | 1 | …t is certain to have an effect. Satisfaction guaranteed or you… |
| Shoulder | 1 | *Sigh*... Man, I'm beat... Shoulder massage. Another job we… |
| Sigh | 1 | *Sigh*... Man, I'm beat... Should… |
| Suolucidteews | 1 | …this? Deilnidrah, deilnidrah... Suolucidteews, suolucidteews... |
| Wonder | 1 | …and easy way to get stronger. Wonder if my brother has some ki… |
| Yawn | 1 | …is time for you to wake up. *Yawn*... Nnngh... I feel like I… |

## Ja cobertos pela KB (conferencia)
Mikado
