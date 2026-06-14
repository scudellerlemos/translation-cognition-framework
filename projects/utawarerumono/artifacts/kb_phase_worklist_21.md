# Fase 0 — capitulo 21 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 21 --check`.

- cenas do capitulo: 21_01, 21_03, 21_04, 21_05, 21_06, 21_07, 21_08
- research_log reconciliado: sim
- nao cobertos: **2 bloqueante(s)** (recorrem >=2 cenas) + 11 de baixa confianca | fracos (ruido): 84 | ja cobertos: 19

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Jachdwalt | **SIM** | 4 | 21_03 | 21_03, 21_04, 21_05 | …crack at it. Stand back, now. Jachdwalt? ...HRAH!! There you g… |
| Uzurushan | **SIM** | 3 | 21_01 | 21_01, 21_03 | …ded and we surveyed uncharted Uzurushan lands, we were able to… |
| Eep | — | 2 | 21_05 | 21_05 | ….? You may have to "disappear." Eep!? D-Dear sister...? Well, th… |
| Shinonon | — | 2 | 21_01 | 21_01 | …te exciting. Hey, hey, whassat? Shinonon, it's dangerous to lean… |
| Uzurusha | — | 2 | 21_01 | 21_01 | …room after getting back from Uzurusha, taking a rest, when th… |
| Fake Jachdwalt Not-bad-yeah | — | 1 | 21_04 | 21_04 | …a. So-you-have-finally-made-it. Fake Jachdwalt Not-bad-yeah. Hm?… |
| Fake Nosuri Ha-ha-ha | — | 1 | 21_04 | 21_04 | …ut of the way so we can escape! Fake Nosuri Ha-ha-ha. So-you-hav… |
| Guard Mm | — | 1 | 21_03 | 21_03 | …he guards first. Uh, excuse me. Guard Mm? Who are you lot? Uruur… |
| Haku Eek | — | 1 | 21_03 | 21_03 | …u, what's wrong? ...Haku? Wait! Haku-- Eek!? Rulutieh, get back!… |
| Hamyana Island | — | 1 | 21_03 | 21_03 | …he same symbology used by the Hamyana Island civilization? Pre… |
| Iceman Project | — | 1 | 21_06 | 21_06 | …u take a look. This is... This "Iceman Project" seems like an ex… |
| True Humanity Project | — | 1 | 21_06 | 21_06 | …ke an expanded version of the True Humanity Project, but... It… |
| Uzurusha Conquest | — | 1 | 21_01 | 21_01 | …ter what became known as the "Uzurusha Conquest"... I'm loungi… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Wha | 5 | …ward us, hair whipping askew. Wha--!? The Nugwisomkami bounds… |
| Hee | 3 | …erous to lean so far outside. Hee hee! You seem pretty excited… |
| Bwuh | 2 | …you certainly came back early. Bwuh!? K-Kuon!? What is she doin… |
| Guh | 2 | …e shadow of the collapsed wall. Guh...! Again... What's this str… |
| Hurry | 2 | …What are you talking about...? Hurry! Maro, don't just stand th… |
| Precisely | 2 | …t the place in your stead...? Precisely. Of course, I wouldn't… |
| Run | 2 | …timing! Three, two, one... Now! Run! Dammit! They've blocked our… |
| Several | 2 | Several days after what became k… |
| Stop | 2 | …crest engraved in it. That is-- Stop right there. Probably best… |
| AaaaAUUuUUgghHH | 1 | …Aghhh... You're... Ah... Ah... AaaaAUUuUUgghHH...! Wha--!? Eeee… |
| Aghhh | 1 | ….. Hhhhhh... Hey... Uh... Ah... Aghhh... You're... Ah... Ah... A… |
| Ahahaha | 1 | …t it into more of 'em, yeah...? Ahahaha! Look at them. There's s… |
| Ahhh | 1 | …tain he was dead... Ah... Ah... Ahhh... Ghhh... Hhhhh... Hhhhhh.… |
| Aye | 1 | …ut I know of no such taboo... Aye, 'tis so. Few would brave th… |
| Bhwurff | 1 | …re our Master to form a wall. Bhwurff--!? The pale figure cras… |
| Bring | 1 | …bigger things to worry about! Bring all your picks and shovels… |
| Bwaaaah | 1 | …ot! You shouldn't get too clo-- Bwaaaah!? Looks like it's imposs… |
| C'mon | 1 | …that? What's the holdup, love? C'mon, we're going to leave yo… |
| Cease | 1 | …. Th-That is-- Know your place. Cease your impertinence. Do you… |
| Close | 1 | …wall, then sinks to the ground. Close one. Master, are you unhur… |
| Cold | 1 | …'re all going to be... Hm? ...Cold...? Hold on, those people i… |
| Concentrate | 1 | …let yourself think like that! Concentrate on getting out of he… |
| Consider | 1 | …ange between the two regions. Consider the area of distributio… |
| Countless | 1 | …!? Urgh... dammit... my head... Countless images blur through my… |
| Details | 1 | …Who knows how old they are. ...Details, please. Yesss. She took… |
| Disappeared | 1 | ….. Gh...!? The Onvitaikayan...? Disappeared... ancient times...\… |
| Eeeeeek | 1 | …... AaaaAUUuUUgghHH...! Wha--!? Eeeeeek! What in the--!? What IS… |
| Eeeeek | 1 | …are we going to do about this!? Eeeeek! We are undone! We are tr… |
| Ghhh | 1 | …was dead... Ah... Ah... Ahhh... Ghhh... Hhhhh... Hhhhhh... Hey..… |
| Hamyana | 1 | …self settled by migrants from Hamyana? ...I have absolutely no… |
| Hhhhh | 1 | …... Ah... Ah... Ahhh... Ghhh... Hhhhh... Hhhhhh... Hey... Uh...… |
| Hhhhhh | 1 | …Ah... Ahhh... Ghhh... Hhhhh... Hhhhhh... Hey... Uh... Ah... Agh… |
| Hic | 1 | …t. Mmm, hmhmhm hmmm hmmm...♪ *Hic* Whew, what a feast. The foo… |
| Hmhm | 1 | …you need mor-- I'm on the case. Hmhm... Thank you, Lord Haku. Go… |
| Holy | 1 | Holy crap, this is... I figured… |
| Honeeey | 1 | …back, it's already light out. Honeeey, I'm hoooooome. Welcome… |
| Hrm | 1 | …the precious ruins, after all. Hrm. I thought you said it was u… |
| I'faith | 1 | …at out without a good reason. I'faith, such pursuits doth suit… |
| Identity | 1 | …ity of the Tatari, I suppose. Identity...? You suppose that th… |
| Impossible | 1 | …ar. Risen from the dead, is he? Impossible. I was certain he was… |
| … | … | (+44 mais) |

## Ja cobertos pela KB (conferencia)
Guard, Haku, Honoka, Kuon, Maro, Maroro, Mikado, Nekone, Nosuri, Nugwisomkami, Onvitaikayan, Oshtor, Ougi, Rulutieh, Saraana, Tatari, Uruuru, Utawarerumono, Yamato
