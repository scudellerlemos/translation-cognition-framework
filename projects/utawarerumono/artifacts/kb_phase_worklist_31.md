# Fase 0 — capitulo 31 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 31 --check`.

- cenas do capitulo: 31_01, 31_02
- research_log reconciliado: sim
- nao cobertos: **1 bloqueante(s)** (recorrem >=2 cenas) + 0 de baixa confianca | fracos (ruido): 42 | ja cobertos: 16

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Run | **SIM** | 6 | 31_02 | 31_02 | …he correct choice was to run. Run, and never stop running. The… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Answer | 3 | …t's... What's happened to Haku? Answer me! ...He is dead. Hm? ..… |
| Bosslady | 2 | …lly was... so much fun... Ah... Bosslady, you're going away? ...… |
| Impossible | 2 | …ld we be defeated so easily...? Impossible... Impossible... impo… |
| Kill | 2 | …able to regain their senses. K-Kill it! Kill that monster!! T… |
| Surface | 2 | …ates! OPEN THE GATES!! gate polySurface19404 polySurface19405 We… |
| Aaaaaaaaaahhhhh | 1 | …stronger. Ah... Ah... Ahh... Aaaaaaaaaahhhhh!! They roll on t… |
| Agghh | 1 | …it out! PUT IT OUT!! PLEASE!! Agghh... AAAAAAAAARRRGH!! They s… |
| Ahh | 1 | …growing stronger. Ah... Ah... Ahh... Aaaaaaaaaahhhhh!! They ro… |
| Beloved | 1 | …down now. Let us begin, then... Beloved people of Ennakamuy! I… |
| Citizen | 1 | …mmediately! Please step back! Citizen Oh, what a regal air he… |
| Citizens | 1 | …has occurred in Yamato of late. Citizens of Ennakamuy, I bring g… |
| Countless | 1 | Countless shadows dart and leap… |
| Crack | 1 | …fires still roaring nearby. *Crack... crack... crack* A sharp… |
| Explosions | 1 | …her body is blown to viscera. Explosions of flesh and blood pa… |
| Faces | 1 | …ls them. Frozen like statues. Faces locked in timeless agony… |
| Fool | 1 | …s intent on blocking his way. Fool... He can tell at a glance.… |
| Frozen | 1 | …nally fades, it reveals them. Frozen like statues. Faces locke… |
| Gasp | 1 | …ed! Passed... Does he mean...? *Gasp*... No... That can't be...!… |
| Gate | 1 | …ody face hair RightIndexFinger2 Gate guard Hey, look! Yes... the… |
| Goodbye | 1 | …Bosslady, you're going away? ...Goodbye. Bosslady? Don't go... I… |
| HhhYYAAAGH | 1 | …begins to swell. It was you... HhhYYAAAGH-- His own scream is c… |
| Holy | 1 | …course she would come to him! Holy crap! That's amazing! Tha… |
| Impressive | 1 | …e time being. *Whistle* Damn. Impressive. You actually defeate… |
| Instantly | 1 | …ck downward swing of his arm. Instantly, ropes fly from the tr… |
| Join | 1 | …ren! Now is our time to rise! Join me under Her Highness's b… |
| Lucky | 1 | …surging forward at the order. Lucky, perhaps. However, they ha… |
| Managing | 1 | …longer even stand. H...Help... Managing only that, he rots away… |
| Ngaah | 1 | …be a-- She has to be a... what? Ngaah!? A voice from nowhere. Be… |
| Ngh | 1 | …oing through the very ground. Ngh... The shadows are well trai… |
| Open | 1 | …wn to become such a fine man... Open the gates! OPEN THE GATES!!… |
| Others | 1 | …e the advantage and strike now. Others Sir! Take the woman away.… |
| Passed | 1 | …The god incarnate, has passed! Passed... Does he mean...? *Gasp… |
| Pull | 1 | …... Haku... Wha--Hey, Rulutieh! Pull yourself together-- ...How,… |
| RightArm | 1 | RightArm body face hair RightInd… |
| RightIndexFinger | 1 | RightArm body face hair RightIndexFinger2 Gate guard Hey… |
| Shadow | 1 | …ace with the portrait, nodding. Shadow It's her. One of Oshtor's… |
| Sweet | 1 | …A love like your mother's... Sweet, yet painful... A love tha… |
| Timanonna | 1 | …mile was warm and kind as the Timanonna, the sun's flower, but… |
| Welcome | 1 | …lySurface19404 polySurface19405 Welcome back! You took a bit lon… |
| Wha | 1 | …e rest... yet there she stands. Wha--!? The shadows stare, paral… |
| … | … | (+2 mais) |

## Ja cobertos pela KB (conferencia)
Akuruka, Ennakamuy, Haku, Imperial, Imperial Guard, Jachdwalt, Kuon, Mikado, Nekone, Nugwisomkami, Oshtor, Oshtor Yamato, Pillar, Rulutieh, Vurai, Yamato
