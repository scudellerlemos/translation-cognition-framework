# Fase 0 — capitulo 18 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 18 --check`.

- cenas do capitulo: 18_01, 18_02, 18_03, 18_04, 18_05
- research_log reconciliado: sim
- nao cobertos: **16 bloqueante(s)** (recorrem >=2 cenas) + 19 de baixa confianca | fracos (ruido): 368 | ja cobertos: 38

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Munechika | **SIM** | 60 | 18_01 | 18_01, 18_02 | …e's up there, but her name is Munechika the Guardian. Her sp… |
| Highness | **SIM** | 49 | 18_01 | 18_01, 18_02, 18_05 | …side and steps forward. Please, Your Highness. I humbly request… |
| Rulu | **SIM** | 18 | 18_01 | 18_01 | …me instead? Something like... Rulu, for example. ...Huh?! Afte… |
| Urgh | **SIM** | 15 | 18_01 | 18_01, 18_02, 18_03 | …s utmost trust. ...Dekopompo. Urgh, right. He's one of the Eig… |
| Guardian | **SIM** | 4 | 18_01 | 18_01, 18_02 | …but her name is Munechika the Guardian. Her specialty is defen… |
| It'll | **SIM** | 4 | 18_01 | 18_01, 18_02 | …but the parade travels slowly. It'll take a while for it to g… |
| Unhand | **SIM** | 4 | 18_01 | 18_01 | …! You're not going anywhere-- Unhand me! H-How dare you touch… |
| What're | **SIM** | 4 | 18_01 | 18_01, 18_03, 18_04 | …t more than shopping, really. What're you two up to? Rulie tip… |
| Honoka | **SIM** | 3 | 18_01 | 18_01 | …est has arrived. Most timely. Honoka, some tea, if you would?… |
| Miruhj | **SIM** | 3 | 18_01 | 18_01 | …ting in CHAIRS, for God's sake. Miruhj, tea. By your will, my lo… |
| Nah | **SIM** | 3 | 18_01 | 18_01 | …in such a mood... Or maybe... Nah, couldn't be. Could it? Spea… |
| Raurau | **SIM** | 3 | 18_01 | 18_01 | …ld you... possibly be, uhm... Sir Raurau? Raurau Oh, dear, hav… |
| Regardless | **SIM** | 3 | 18_01 | 18_01, 18_05 | …her clothes, more accurately. Regardless, I feel kinda bad for… |
| Soyankekur | **SIM** | 3 | 18_01 | 18_01 | …chi. A family of bigwigs, eh... Soyankekur the Mariner... He's S… |
| Understood | **SIM** | 3 | 18_01 | 18_01 | …s always an option. Just relax. U-Understood... Rulutieh stirs t… |
| Failure | — | 2 | 18_01 | 18_01 | …t worry about messing up, OK? Failure is always an option. Jus… |
| Mito | — | 2 | 18_01 | 18_01 | …n but I'm long retired. Call me Mito, if it please you. Uh, al… |
| Oohh | — | 2 | 18_01 | 18_01 | …ye. What the hell is she do-- Oohh. I get it. Now, I suddenly… |
| Pardon | **SIM** | 2 | 18_01 | 18_01, 18_05 | …s as she stares vacantly ahead. Pardon me. Hm? Oh, hullo. One af… |
| Pay | — | 2 | 18_01 | 18_01 | …you pay for what you ate. ...Pay? Aaaargh! Would somebody ple… |
| Preposterous | — | 2 | 18_01 | 18_01 | …I've never tasted their ilk? Preposterous. I DEMAND seconds.… |
| Puffs | — | 2 | 18_01 | 18_01 | …we're calling them... Well, "Puffs." Puffs? That's a strange… |
| Raiko | — | 2 | 18_01 | 18_01 | …less warrior, first. I see... Raiko the Sage... Word is he's n… |
| Remember | — | 2 | 18_01 | 18_01 | …ly empty. I can't pay for it. Remember my explanation about pa… |
| Cocky General Seeks | — | 1 | 18_01 | 18_01 | …n for her. "Clandestine Love! ~ The Cocky General Seeks the Pr… |
| Expecting Oshtor | — | 1 | 18_03 | 18_03 | …, Oshtor. Your Anju awaits you. Expecting Oshtor? Yeah, sorry to… |
| Hhhhgh Stop | — | 1 | 18_01 | 18_01 | …ooord? *Grind, grind, grind*... Hhhhgh-- Stop, stop, stop! That'… |
| Imperial Theater | — | 1 | 18_01 | 18_01 | …perform. I see. Similar to the Imperial Theater. They do occasi… |
| Inform Oshtor | — | 1 | 18_01 | 18_01 | …tionship wasn't especially bad. Inform Oshtor that all will be a… |
| Mystery Twins | — | 1 | 18_01 | 18_01 | …ook around, but--of course--the Mystery Twins have disappeared… |
| Nosuri Thieves | — | 1 | 18_01 | 18_01 | …e one and only Nosuri, of the Nosuri Thieves! Despite struggli… |
| Poor Kiwru | — | 1 | 18_01 | 18_01 | …... my... My stomach... unhh... Poor Kiwru has been doubled over… |
| RightFoot LeftFoot | — | 1 | 18_05 | 18_05 | …hen cover our ears in unison. RightFoot LeftFoot |
| Secret Sword | — | 1 | 18_01 | 18_01 | …~ The Cocky General Seeks the Prince's Secret Sword!" That's..… |
| Worker Pardon | — | 1 | 18_01 | 18_01 | …rning for this much racket... Worker Pardon me! Excuse me, sir… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Hee | 14 | …nitely been our focus lately. Hee hee... Hm? You're amazing, S… |
| Uhm | 8 | …entertaining. So? What say you? U-Uhm, I don't know. This is...… |
| Bah | 7 | …m not the one who made her cry. Bah. That she's saddened in your… |
| Urk | 7 | …rd me. Oh... Um... no, I can... Urk. Yeah, all right. I decide t… |
| Hromf | 5 | …do it! Now, to sample our work. Hromf... *Smack... smack*... Ahh… |
| Stop | 5 | …y more than you already have! Stop using me as a shield and--\… |
| Suddenly | 5 | …e to dethrone this foul tyrant! Suddenly, Atuy produces her spea… |
| Ahahaha | 4 | …aid I have to modestly decline. Ahahaha! There's no need for mod… |
| Bweh | 4 | …reading on the couch as always. Bweh heh--eh heh heh... And I re… |
| He'll | 4 | …enging the general himself... He'll utterly destroy her! Th-Th… |
| Krrkk | 4 | …for leverage over others... *Krrkk*... *KRRRKKKK*... Nnngh...… |
| Mmf | 4 | …we walk, savoring the taste. Mmf. Looks like I made the right… |
| Sigh | 4 | …dy try to feed me like this? *Sigh*... Reluctantly, I eat the… |
| Actually | 3 | …to be interested in that stuff. Actually, I've never read the on… |
| Ahh | 3 | …k. Hromf... *Smack... smack*... Ahh, delicious! Yes, it is! Such… |
| Eep | 3 | …offense at Nekone's rudeness. Eep! God, this guy is scary as h… |
| Erm | 3 | …sing. Please prepare to depart. Erm... Anju seems to notice for… |
| Grind | 3 | …on either side of Anju's head. *Grind, grind--* Gaaahh!! Whaaat'… |
| Grrr | 3 | …tually have curves. Sorry, kid. Grrr... Hnnngh... Nekone and I l… |
| Hard | 3 | …'s strange, but... very good... Hard to believe something this g… |
| Interesting | 3 | …t a secret... Very interesting. Interesting indeed... Huh? Oshto… |
| Open | 3 | …cess, isn't it? Here now, love. Open wide. She stabs one of the… |
| Osh | 3 | …ing in front of his princess. O-Osh... Oshtor! How may I be of… |
| Pretty | 3 | …Eight Pillars too, isn't he? Pretty sure you already know all… |
| Quit | 3 | …H {W35}FWOOSH {W35}WH--* Wh--!? Quit flailing, or I'm gonna fall… |
| Shit | 3 | …ggers at me than ever before. Shit. That little display just n… |
| Shove | 3 | …to get killed at this rate! *Shove, shove--* Would you PLEASE… |
| Somehow | 3 | …d-- Damn it, she won't budge. Somehow, I manage to turn myself… |
| Surely | 3 | …a random city girl, aren't you? Surely the honorable princess of… |
| True | 3 | …E were working as well, Haku. True, but think about it. Who'd… |
| Tug | 3 | …and they've disappeared. Who-- *Tug, tug*... Wh-- The approachin… |
| Ungh | 3 | …nts, letting go of Anju's head. Ungh... Anju crumbles, holding h… |
| Whew | 3 | …nds like a great idea, I think. Whew... Man, I'm full. It's gett… |
| ACHOO | 2 | …goal for the night, I think? Th-Then--ACHOO!!--let's get the… |
| Aheh | 2 | …s from Mikazuchi's. Mnnhh. Heh. Aheh heh heh. Mikazuchi's lips c… |
| Ahhh | 2 | …his sort of debauched behavior? Ahhh... S-Someone! Assassin! A b… |
| Astounding | 2 | …Ah, I'm glad you all like it... Astounding. The puffed dough cre… |
| Beside | 2 | …r. Then this wouldn't have... Beside me, Kiwru hunches over in… |
| Bwuh | 2 | …, Haku. Until we meet again. ...Bwuh!? The next moment, I snap u… |
| C'mon | 2 | …nd mine before I can protest. C'mon, Rulie, let's go. Um... An… |
| … | … | (+328 mais) |

## Ja cobertos pela KB (conferencia)
Akuruka, Amam, Anju, Atuy, Capital, Dekopompo, Divine Scion, Divine Scion Anju, Gigiri, Guard, Guards, Haku, Hakurokaku, Hakurokaku Inn, Imperial, Imperial Guard, Kiwru, Kujyuri, Kuon, Kurarin, Mausoleum, Mikado, Mikazuchi, Nekone, Nosuri, Oshtor, Ougi, Ozen, Pillar, Pillars, Points, Rulie, Rulutieh, Shyahoro, Twin Shields, Twins, Ukon, Yamato
