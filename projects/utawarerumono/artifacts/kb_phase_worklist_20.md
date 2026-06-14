# Fase 0 — capitulo 20 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 20 --check`.

- cenas do capitulo: 20_01, 20_02, 20_03, 20_04, 20_05, 20_06, 20_07, 20_08, 20_10, 20_11, 20_12, 20_13, 20_14, 20_17, 20_18, 20_19, 20_20, 20_21, 20_22
- research_log reconciliado: sim
- nao cobertos: **21 bloqueante(s)** (recorrem >=2 cenas) + 15 de baixa confianca | fracos (ruido): 248 | ja cobertos: 30

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Jachdwalt | **SIM** | 39 | 20_06 | 20_06, 20_07, 20_21 | …d... telling me your name? ...It's Jachdwalt. I see. Figures.… |
| Uzurushan | **SIM** | 33 | 20_01 | 20_01, 20_03, 20_04, 20_05, 20_06, 20_07, 20_08, 20_10, 20_11, 20_12, 20_13, 20_14, 20_17, 20_18, 20_20, 20_21 | …ou, duly noted. Ha... Hahaha. The Uzurushan army is showing si… |
| Gundhurua | **SIM** | 27 | 20_01 | 20_01, 20_02, 20_11, 20_17, 20_18, 20_20, 20_21 | …e situation changed completely. Gundhurua... a man who united ov… |
| Uzurusha | **SIM** | 22 | 20_01 | 20_01, 20_02, 20_03, 20_05, 20_07, 20_10, 20_12, 20_14, 20_18, 20_20, 20_21 | …m. So... Maruruha has fallen to Uzurusha. If all proceeds as pre… |
| Entua | **SIM** | 21 | 20_07 | 20_07, 20_08, 20_20, 20_21 | …ou... Be good now, Shinonon. ...Entua? You're going to let us go… |
| Zeguni | **SIM** | 21 | 20_20 | 20_20 | …nd! You DARE!! My owlo!! Hmh... Commander Zeguni stares into Gun… |
| Yamatan | **SIM** | 18 | 20_02 | 20_02, 20_03, 20_10, 20_11, 20_12, 20_13, 20_14, 20_17, 20_18, 20_20, 20_21 | …n his face as he looks upon the Yamatan messenger. His retaine… |
| Uzurushans | **SIM** | 12 | 20_01 | 20_01, 20_03, 20_06, 20_20 | …ry few instances in which the Uzurushans clashed with Yamato's… |
| Woshis | **SIM** | 9 | 20_18 | 20_18 | …emember, anticipation is key. Woshis sketches on his drawing b… |
| Shinonon | **SIM** | 8 | 20_07 | 20_07, 20_08, 20_21 | …child close as she looks about. Shinonon, I am going to go see w… |
| Akuruturuka | **SIM** | 5 | 20_13 | 20_13, 20_17, 20_21 | …supposed to call that thing!? Akuruturuka. ...An Akuruturuka?… |
| Vurai | **SIM** | 5 | 20_13 | 20_13 | …at's the matter? It can't be... Vurai, the Vanguard... Wha... Wh… |
| Hahaha | **SIM** | 4 | 20_01 | 20_01, 20_02, 20_13 | …assure you, duly noted. Ha... Hahaha. The Uzurushan army is sh… |
| Hurry | **SIM** | 4 | 20_05 | 20_05, 20_06, 20_08 | …you just standing there for!? Hurry up and kill them all! What… |
| Yamatans | **SIM** | 4 | 20_01 | 20_01, 20_18, 20_20, 20_21 | …raid storehouses, or take the Yamatans' harvested crops. The U… |
| Ahhhh | **SIM** | 3 | 20_07 | 20_07, 20_14 | …in. Girl Open wide. Small child Ahhhh... *homf* *munch* Do you l… |
| Hyahahahahaha | **SIM** | 3 | 20_14 | 20_14, 20_17 | …, help me...! Uzurushan soldier Hyahahahahaha! Look at these guy… |
| Combat Tutorial | **SIM** | 2 | 20_05 | 20_05, 20_07 | …ave to ask you to die here. {c5}Combat Tutorial{c-1} added to th… |
| Glossary | **SIM** | 2 | 20_05 | 20_05, 20_07 | …mbat Tutorial{c-1} added to the Glossary. Maroro? You're up next… |
| Khakakakakakaka | — | 2 | 20_02 | 20_02 | …hakakakakaka! Hh... hh... hh... Khakakakakakaka! Khakakakakaka… |
| LeftLeg | **SIM** | 2 | 20_11 | 20_11, 20_20 | …H! ch400_00_base ch400_00_wheel LeftLeg target kamen billboard G… |
| Maruruha | — | 2 | 20_01 | 20_01 | …it may be safe to assume that Maruruha has fallen... Most re… |
| Open | — | 2 | 20_07 | 20_07 | …vas. I follow suit and peer in. Girl Open wide. Small child Ahhh… |
| Reporting | — | 2 | 20_14 | 20_14 | …kirmishing while scattered... Reporting! Our soldiers have def… |
| Vanguard | — | 2 | 20_13 | 20_13 | …tter? It can't be... Vurai, the Vanguard... Wha... What is one o… |
| Yamatan Soldier | **SIM** | 2 | 20_14 | 20_14, 20_19 | …Y-Your head...! AAAAAAAGHHH! Yamatan Soldier Lord... Mikazuch… |
| Yatanawarabe | — | 2 | 20_18 | 20_18 | …in to kiss. Before him are his Yatanawarabe, faces red with e… |
| Adviser The Yamatan | — | 1 | 20_17 | 20_17 | …d charge! Damn. At this rate... Adviser The Yamatan army has beg… |
| Advisers Gundhurua | — | 1 | 20_18 | 20_18 | …y's defeats come in. Silence! Advisers Gundhurua roars at his… |
| Beside Woshis | — | 1 | 20_18 | 20_18 | …ares up at Woshis, eyes wide. Beside Woshis, countless other s… |
| Damned Yamatan | — | 1 | 20_17 | 20_17 | …What is this? A smokescreen...? Damned Yamatan cowards! They'r… |
| Messenger Reporting | — | 1 | 20_18 | 20_18 | Messenger R-Reporting! Our force… |
| Mirage Blade | — | 1 | 20_06 | 20_06 | …y they call him Jachdwalt the Mirage Blade... ...Huh? W-Wait..… |
| Multiple Uzurushan | — | 1 | 20_07 | 20_07 | …e men were searching for her. Multiple Uzurushan soldiers appe… |
| Soldier Reporting | — | 1 | 20_01 | 20_01 | …o such emotion. Such shame... Soldier Reporting! What is the m… |
| Spine Winds | — | 1 | 20_08 | 20_08 | …way. And you... are in the way. Spine Winds take you! Now, Cocop… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Wha | 8 | …will take your hisha instead. Wha--!? I am glad indeed to see… |
| Impossible | 6 | …...? Can this be possible...? Impossible... We need to regroup… |
| Soldiers | 5 | …s this? Is this magecraft...? Rrgh--Soldiers! Cease the attack… |
| Hee | 4 | …behind. Get off. You're heavy. Hee hee, you shouldn't ever joke… |
| Nyeh | 4 | …my genius and might. Be silent. Nyeh...? Wha--Wh--Wh--Wh... How… |
| Ahhh | 3 | …eegh! You won't escape! Arrrgh! Ahhh!? You guys are genuinely te… |
| Hmhmhm | 3 | …er from playing with them. ...Hmhmhm. I would expect no less f… |
| Laugh | 3 | …t amusing? Ah... A-Ahah... Yes. Laugh, laugh! Ahahahaha... Hahah… |
| Nakwan | 3 | …You WERE holding back on us. Nakwan What have you done, Jachd… |
| Show | 3 | …ommence our invasion of Yamato! Show mercy to none. Man, woman,… |
| Silence | 3 | …ution, we act in grave error! Silence! I have heard enough fro… |
| Adviser | 2 | …h a vicious blow to the face. Adviser One must remember to rel… |
| Ahahahaha | 2 | ….. A-Ahah... Yes. Laugh, laugh! Ahahahaha... Hahaha... Very good… |
| Arrrgh | 2 | …back on her word, I'd think? Arrrgh! How!? How could I have l… |
| Course | 2 | …. That's right. You been good? 'Course I been good! The child's… |
| Crush | 2 | …beauty in an honorable death! Crush them, like the worms they… |
| Eep | 2 | …. So we don't need him anymore? Eep... Well... I guess this is g… |
| Ghaaah | 2 | …ming! Huh...? RAAAAAAAAAAAAAAH! Ghaaah! Our pursuing unit was sc… |
| Haaaaaaaaaah | 2 | …escape... I commend your valor. Haaaaaaaaaah!! Then I shall hono… |
| Hahahahahaha | 2 | …re! Laugh HARDER! Ahahahahahah! Hahahahahaha! DO YOU FIND THIS F… |
| Hmhm | 2 | …n, but it will not be denied. Hmhm. That was quite the yawn. Y… |
| Hmmm | 2 | …be late. Right you are. Ohhh... Hmmm... What to do? I can't just… |
| Kill | 2 | …'s going to be... That's right. Kill them! My name is Kuon. Do y… |
| Mere | 2 | …l pay with your life! Kill him! Mere child's play... What...!? Y… |
| Mhm | 2 | …me... to accompany you...? ...Mhm, of course. I'm sure Haku wi… |
| Nakwans | 2 | …ans, and fight in their wars. Nakwans? Expendable slave soldie… |
| Ngh | 2 | …. So... why do you not laugh? Ngh... ...Or do you not find it… |
| Oooh | 2 | …expectations. Here they come... Oooh, he looks like a tough one.… |
| Rugged | 2 | …is goodbye, then. Hm? You're... Rugged man Sorry about that, lad… |
| Sigh | 2 | …g? That's not who we're after. *Sigh* Love, you really are a spo… |
| Stomp | 2 | …ua? You're going to let us go? *Stomp* *stomp* *stomp* Lady Entu… |
| Stop | 2 | …you no mercy. Gah... W-Wait...! S-Stop pushing forward! Wh-What… |
| Surround | 2 | …pe... Entua, fighting's bad. ...Surround them. Do not let them e… |
| Aaaaaarrrgh | 1 | …n my way will be crushed. Ah... Aaaaaarrrgh! Erupt. Hm...? Wha--… |
| Aah | 1 | …enough to make a scratch on me. Aah!! Oshtor grabs the blade of… |
| Across | 1 | …at makes us doubt our own eyes. Across the canyon, a lone man--m… |
| Ahah | 1 | …you not find it amusing? Ah... A-Ahah... Yes. Laugh, laugh! Aha… |
| Ahahaha | 1 | …, still vibrating with force. Ahahaha! Looks like they've star… |
| Ahahahahah | 1 | …down the soldiers in the back! Ahahahahah! I've been waiting SO… |
| Ahahahahaha | 1 | …lay, Master. You're here! Guh!? Ahahahahaha! Oh, love, that's ju… |
| … | … | (+208 mais) |

## Ja cobertos pela KB (conferencia)
Akuruka, Akurukas, Atuy, Bokoinante, Cocopo, Dekopompo, Haku, Honoka, Imperial, Imperial Capital, Imperial Guard, Kiwru, Kuon, Maro, Maroro, Mikado, Mikazuchi, Munechika, Nekone, Nosuri, Nugwisomkami, Oshtor, Ougi, Pillar, Pillars, Raiko, Rulutieh, Saraana, Uruuru, Yamato
