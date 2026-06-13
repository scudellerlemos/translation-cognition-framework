# Fase 0 — capitulo 19 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 19 --check`.

- cenas do capitulo: 19_01, 19_02, 19_03, 19_04, 19_05, 19_06, 19_07, 19_08
- research_log reconciliado: sim
- nao cobertos: **0 bloqueante(s)** (recorrem >=2 cenas) + 11 de baixa confianca | fracos (ruido): 321 | ja cobertos: 45

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Forgot | — | 2 | 19_03 | 19_03 | …ough, cough*... Gah, my eyes! Forgot about all the damn smoke!… |
| Hear | — | 2 | 19_08 | 19_08 | …could not agree more, Oshtor. Hear! Hear! Free drinks aside, w… |
| Kind | — | 2 | 19_08 | 19_08 | …I head out to meet up with him. Kind of a lonely place for a bar… |
| Brigand Zzz | — | 1 | 19_02 | 19_02 | EXI_B0535_A EXI_B0535_C Head Brigand Zzz... zzz... Momma… |
| Caretaker Ey | — | 1 | 19_08 | 19_08 | …joy your life while it lasts. Caretaker Ey, those bugs still a… |
| Combat Tutorial | — | 1 | 19_03 | 19_03 | …ctually kind of impressive. {c5}Combat Tutorial{c-1} added to th… |
| Dessert Mountain | — | 1 | 19_07 | 19_07 | …, her eyes keep flickering to Dessert Mountain. Ah well. Guess… |
| Guests Huzzah | — | 1 | 19_08 | 19_08 | …I thank you all for joining me! Guests Huzzah! Splendidly honore… |
| Ignoring Moznu | — | 1 | 19_04 | 19_04 | …asquerading as... uh, Nosuri? Ignoring Moznu's yells, I glance… |
| Killing Moznu | — | 1 | 19_02 | 19_02 | …t I was the one who caught him? Killing Moznu won't do any good,… |
| Priestess Lady Honoka--her | — | 1 | 19_05 | 19_05 | …i of Chains, and daughters of High Priestess Lady Honoka--her… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Wha | 10 | …urs should work quite nicely. Wha--!? I should have expected a… |
| Cough | 6 | …ess so. Let's get going, then. *Cough, hack* D-Dammit, what's go… |
| Course | 6 | …ren't volunteering yourself... 'Course not. Believe me, that's t… |
| Whew | 6 | …brother's ranks, do you not!? Whew... That was close. I almost… |
| Eep | 5 | …y words I was told to convey. E-Eep... I must apologize, but a… |
| Excuse | 5 | …- Gah, now wait a damn minute-- Excuse me! Uh, wh-what's the mat… |
| Fwap | 5 | …s own bald scalp, and-- *Fwip* *Fwap* ...Huh? ...Understand? U-U… |
| Hee | 5 | …has to be something special... Hee hee, what IS it? Kuon dash… |
| Eat | 4 | …er trapped in Mikazuchi's gaze. Eat. What's wrong? You don't wan… |
| Fwip | 4 | …asps his own bald scalp, and-- *Fwip* *Fwap* ...Huh? ...Understa… |
| Hahaha | 4 | …er saying anything like that. Hahaha! You card, you! By the wa… |
| Holy | 4 | …filled with tray after tray. Holy crap, that's a lot... I've… |
| Shit | 4 | …ame with such heinous crimes! Shit! I dunno what you're talkin… |
| Smirk | 4 | …can do is stare at the food. *Smirk*... Guh...!? Ah... urgh...… |
| Tea | 4 | …much, I'm all thirsty now... Tea. We shall prepare you a cup… |
| Crap | 3 | …picious of us now, as a result. Crap. If that's true, this could… |
| Enjoy | 3 | …. Huh? Well, I've already got-- Enjoy. Uh... Great. Thanks. Um,… |
| Geez | 3 | …been us up against the wall. Geez... close one. Her Highness… |
| Guh | 3 | …stare at the food. *Smirk*... Guh...!? Ah... urgh... This guy'… |
| Hmhmhm | 3 | …did not end up as our enemy. Hmhmhm... Despite his words, Oug… |
| Hmmm | 3 | …wouldn't mind at all, you know. Hmmm... Then if you still aren't… |
| Judging | 3 | …till just a temporary solution. Judging from Oshtor's face, none… |
| Orders | 3 | …existing is your satisfaction. Orders are absolute. Following y… |
| Press | 3 | …learn. THIS is how you do it! *Press* Wh-- I put all my strengt… |
| Suddenly | 3 | …top... STOOOOOOOOOOOOOOOOP!!! Suddenly, Ougi and the Nosuri Ba… |
| Actually | 2 | …o they're that big a deal...? Actually, you know what? Don't t… |
| Anyway | 2 | …ou're amazing! Uh... th-thanks. Anyway, let's get this over with… |
| Believe | 2 | …eering yourself... 'Course not. Believe me, that's the last thin… |
| Better | 2 | …surprise and force them out. Better than fighting them head-o… |
| Bug | 2 | …ke a peek inside the cages... Bug SSSSSSSSSSSSSS!! Gah! Rgh, t… |
| Completely | 2 | …cided to keep you warm like so. C-Completely naked...? These two… |
| Cross | 2 | …. You better come. Pinky swear! Cross your heart and hope to d… |
| Food | 2 | …What's with all these steps...? Food pyramid. You must ascend th… |
| Gasp | 2 | …bout to pat Nekone's head-- ...*Gasp* *Skitter* Hrrngh... So clo… |
| Glad | 2 | …ssigning them to you. ...Mm? ...Glad that they are of use? Ass… |
| Goddammit | 2 | …own would've been real rough. Goddammit. I knew I should have… |
| Gulp | 2 | …and sweeter than any other. *Gulp*... Sounds like somebody's… |
| Hmhm | 2 | …pretend I'm still in the dark. Hmhm... Ho ho ho... With a cheer… |
| Homf | 2 | …be it's just my imagination? *Homf*... *nomf*... *munch* *mu… |
| Honestly | 2 | …l this "high treason" business? Honestly... Kuon is clearly exas… |
| … | … | (+281 mais) |

## Ja cobertos pela KB (conferencia)
Anju, Atuy, Bandits, Boro, Chains, Dekopompo, Ennakamuy, Free, Gigiri, Haku, Hakurokaku, Hakurokaku Inn, Honoka, Imperial, Imperial Guard, Kamunagi, Kiwru, Kujyuri, Kuon, Magecraft, Maro, Maroro, Mikado, Mikazuchi, Miruhj, Mito, Moznu, Nekone, Nosuri, Nosuri Bandits, Nosuri Thieves, Oshtor, Ougi, Pillar, Raiko, Rulutieh, Sakon, Saraana, Shichirya, Shyahoro, Twin Shields, Ukon, Uncle, Uruuru, Yamato
