# Fase 0 — capitulo 22 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 22 --check`.

- cenas do capitulo: 22_02, 22_03, 22_04, 22_05, 22_06, 22_07, 22_08
- research_log reconciliado: sim
- nao cobertos: **16 bloqueante(s)** (recorrem >=2 cenas) + 6 de baixa confianca | fracos (ruido): 348 | ja cobertos: 37

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Tuskur | **SIM** | 25 | 22_03 | 22_03, 22_04, 22_05, 22_06 | …o... Tuss...? Oh, right. It was Tuskur. Pffffft!! Kuon immediate… |
| Camyu | **SIM** | 19 | 22_04 | 22_04, 22_05, 22_06 | …ha! Say goodbye to the clueless Camyu of before. See, I can ca… |
| Aruruu | **SIM** | 14 | 22_04 | 22_04, 22_05, 22_06 | …way... I think. Cammie, hide. Aruruu dives into my bed, and Ca… |
| Aru | **SIM** | 11 | 22_04 | 22_04, 22_05, 22_06 | …rence-- She freezes. A... Ar... Aru...!? Aru? The worker quickly… |
| Young | **SIM** | 9 | 22_04 | 22_04 | …at the other side of my table. Young master, please. Over here.… |
| She'd | **SIM** | 6 | 22_04 | 22_04, 22_05, 22_07 | …ds for men were way too high. She'd ignore every single person… |
| Neko | **SIM** | 5 | 22_08 | 22_08 | …is anger or exasperation. Oh, Neko and Oshtor! What a lovely c… |
| Amaterasu | **SIM** | 4 | 22_08 | 22_08 | …to try to wipe them out using Amaterasu. Hold on. Wasn't Amate… |
| C'mon | **SIM** | 4 | 22_03 | 22_03, 22_08 | …like that excuse is gonna fly. C'mon... I struggle to pull Kuon… |
| Chii | **SIM** | 3 | 22_08 | 22_08 | …...? What about your wife and Chii...? A smile crosses the Mik… |
| Earth | **SIM** | 3 | 22_08 | 22_08 | …uld drop an artificial sun on Earth, or cause some kind of s… |
| Hmmm | **SIM** | 3 | 22_03 | 22_03, 22_08 | …in the imperial capital soon. Hmmm. I wonder what kind of peop… |
| Onkamiyamukai | **SIM** | 3 | 22_06 | 22_06 | …mean? Kid, you ever hear of the Onkamiyamukai? The twins freeze… |
| Hiroshi | — | 2 | 22_08 | 22_08 | …talked like this, hasn't it, Hiroshi...? ...Bro... ther...? T… |
| Hiroyuki | — | 2 | 22_08 | 22_08 | …"Hiroshi"? ...Hm? Or... was it Hiroyuki? What do you mean "or w… |
| Imperial Cloister | **SIM** | 2 | 22_04 | 22_04, 22_05 | …ur ambassadors arrived at the Imperial Cloister... Just as Uko… |
| Pretty | **SIM** | 2 | 22_03 | 22_03, 22_08 | …ery gentle, and so elegant... Pretty much the complete opposit… |
| Smells | **SIM** | 2 | 22_04 | 22_04, 22_06 | …here's a dish called kusayan. Smells a bit strange, I'll grant… |
| Yaana Mauna | — | 2 | 22_05 | 22_05 | …st. Sister... I don't think the Yaana Mauna should be partakin… |
| Aru Hm | — | 1 | 22_04 | 22_04 | …er"... Cammie, did you find Ku? Aru-- Hm? Wait, you're-- ...Wher… |
| C'mon Kuon | — | 1 | 22_08 | 22_08 | …run, like Kuon's doing now... C'mon Kuon, pretty please! I w… |
| Imperial Palace | — | 1 | 22_07 | 22_07 | …Yes. I've been summoned to the Imperial Palace on urgent noti… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Mhm | 16 | …ly peeking through her fingers. Mhm... Well, you seem fine now.\… |
| Sigh | 9 | …eet. ...Market street. Got it. *Sigh*... ...*Sigh*... Haku, is s… |
| Hee | 7 | …t, then clean up main street. Hee hee! And what'll we have for… |
| Whew | 7 | …flumps back down onto his seat. Whew. Feels a lot more natural t… |
| Wha | 6 | …crowd as the carriages pass. Wha--!? What are those steeds?… |
| Grind | 5 | …one important. A kamunagi...!? *Grind* *grind* *grind* *grind* K… |
| Mmf | 5 | …ile Kurarin keeps them bound. Mmf. Mmmf. Mmmf! Mmmmmf! You hav… |
| True | 5 | …ing it out is enough to help. True. Maybe telling someone abou… |
| Cammie | 4 | …old enough to be a "mister"... Cammie, did you find Ku? Aru-- H… |
| Excuse | 4 | …first place. I don't know any-- Excuse me. I must pass behind yo… |
| Hmhm | 4 | …t. I'm sure she still likes us! Hmhm. Although she was almost in… |
| Kid | 4 | …his expression turning grave. Kid, I think you'd better tell m… |
| Munch | 4 | …o eat what they've seasoned. *Munch, munch*... Hlgh... So so… |
| Course | 3 | …ways carry that thing around? Course I do. Why wouldn't I? I… |
| Far | 3 | …like nice people to be around. Far as I can tell, they seemed m… |
| Immediately | 3 | …pen to reveal a woman inside. Immediately, we hear gasps from… |
| Mmm | 3 | …at's very considerate of you. Mmm! I see you've chosen the per… |
| Stop | 3 | …sash. I can't!! P-Please, Ougi! Stop! G-Give it back! Please!… |
| Welcome | 3 | …open. Good. She's awake. *Yawn* Welcome back, Ku. Ku? This Ku pe… |
| Yawn | 3 | …lowly open. Good. She's awake. *Yawn* Welcome back, Ku. Ku? This… |
| Ahh | 2 | ….. *Rub* *rub* *rub*... Hnngh!? Ahh... I can't restrain a little… |
| Anyhow | 2 | …e something of a ladies' man. Anyhow, we all thought it might… |
| Anyway | 2 | …ybe it was fate more than luck. Anyway, thanks to that, I can… |
| Apparently | 2 | …my attention before. Rumors? Apparently, those two... Back in… |
| Awright | 2 | …le sortin' it out yourself... Awright, we can wait. I know y… |
| Beautiful | 2 | …er one of those two beauties. Beautiful woman *Snore*... zzz..… |
| Disappointing | 2 | …this is a little... you know. Disappointing. What do I do? Sho… |
| Eventually | 2 | …forward, letting them guide me. Eventually, another giant door a… |
| Gotcha | 2 | …something on the side to eat. Gotcha. One random plate coming… |
| Gulp | 2 | …d to be our snack for today! *Gulp* And with that, the final o… |
| Hnngh | 2 | …with work. Man, I'm tired... Hnngh!? M-My back... As I stretc… |
| Hrm | 2 | …of something being chewed. ...Hrm? Fnngh? The two figures, app… |
| Humans | 2 | …... So the Tatari really are... Humans... That is correct. Befor… |
| Jiggle | 2 | …on't let them go now, Kurarin. *Jiggle jiggle jiggle* Mmf... Mmm… |
| Mmmf | 2 | …urarin keeps them bound. Mmf. Mmmf. Mmmf! Mmmmmf! You have my… |
| Mmmmmf | 2 | …them bound. Mmf. Mmmf. Mmmf! Mmmmmf! You have my respect for… |
| Nnngh | 2 | …sitate, unsure of what to do. Nnngh... As I stand there dither… |
| Ohhh | 2 | …can sense Ku here so much is... Ohhh... Hold on, I'm getting the… |
| Oho | 2 | …liviously happy and carefree. Oho? Ah, thy praise is too kind!… |
| Oooh | 2 | …nd in a flurry of excitement. Oooh, Master Haku! Thy dance is… |
| … | … | (+308 mais) |

## Ja cobertos pela KB (conferencia)
Anju, Atuy, Chains, Cocopo, Ennakamuy, Free, Haku, Hakurokaku, Honoka, Imperial, Jachdwalt, Kamunagi, Kiwru, Kuon, Kurarin, Maroro, Mausoleum, Mikado, Mikazuchi, Mito, Mushroom, Nekone, Nosuri, Nugwisomkami, Onvitaikayan, Oshtor, Ougi, Rulutieh, Sakon, Saraana, Shinonon, Tatari, Twin, Ukon, Uruuru, Yamatan, Yamato
