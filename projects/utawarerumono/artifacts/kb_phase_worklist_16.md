# Fase 0 — capitulo 16 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 16 --check`.

- cenas do capitulo: 16_01, 16_02, 16_03, 16_04, 16_05
- research_log reconciliado: sim
- nao cobertos: **6 bloqueante(s)** (recorrem >=2 cenas) + 9 de baixa confianca | fracos (ruido): 186 | ja cobertos: 19

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Yuuri | **SIM** | 26 | 16_02 | 16_02, 16_03, 16_04, 16_05 | …s who you'll be escorting. I am Yuuri. I-It's a pleasure to meet… |
| Kurarin | **SIM** | 23 | 16_01 | 16_01 | …mon mistake. This little one is Kurarin. ...Kurarin? What's a… |
| Dear | **SIM** | 8 | 16_01 | 16_01, 16_02, 16_03, 16_05 | …this is where you got off to. Dear sister was-- *Stick* EEP!?… |
| Guess | **SIM** | 7 | 16_01 | 16_01, 16_02 | …might appreciate this place. Guess I'll let her know about it… |
| Ahaha | **SIM** | 4 | 16_01 | 16_01, 16_02 | …atch a cold around you, then. Ahaha. That's probably for the b… |
| Karulau | **SIM** | 3 | 16_01 | 16_01 | …oduce myself. You may call me Karulau, if it pleases you. Ka… |
| Getting | — | 2 | 16_01 | 16_01 | …lucky you're just my type. Eh? Getting on good terms with the l… |
| Nice | — | 2 | 16_02 | 16_02 | …ine. I-I'm R-Rulutieh, yes... Nice to meet you. Is that right?… |
| Rulie | — | 2 | 16_02 | 16_02 | …tuy. It's nice to meet you too, Rulie. Ru...lie? You aren't seri… |
| We'd | — | 2 | 16_01 | 16_01 | …lessly. You're... You're right. We'd best patrol the area we'r… |
| Agh Finally | — | 1 | 16_01 | 16_01 | …of scale around here. *WHUMP* Agh-- Finally freed from my desk… |
| Combat Tutorial | — | 1 | 16_04 | 16_04 | {c5}Combat Tutorial{c-1} added to th… |
| Ladykiller Kurarin | — | 1 | 16_01 | 16_01 | …ular with the girls this way. Ladykiller Kurarin. Two quick ci… |
| Tenant Wheh | — | 1 | 16_01 | 16_01 | …merge, giving off a shady vibe. Tenant Wheh? Who the--Oh! If it… |
| Yamatan Soldier Pweeaase | — | 1 | 16_04 | 16_04 | …You get it, ya... ya shithead! Yamatan Soldier Pweeaase, hewp m… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Nah | 5 | …alone? What if something...? Nah, I shouldn't worry. Kuon can… |
| Hee | 4 | …mysterious as, uh... as a hat. Hee hee. This little guy's no tr… |
| Urgh | 4 | Hm... Urgh. Toilet. Gotta go... ...Phe… |
| Wait | 4 | …r the kitchen's whole larder. Wait, wait, hold on. That's defi… |
| Ahh | 3 | …up to my lips and drink deeply. Ahh... That's the good stuff. Sm… |
| Ngh | 3 | …face(???) with a hand towel. Ngh, slippery. Hard to wipe--Gah… |
| Nhalai | 3 | …Did I... Did I take it too far? Nhalai... I'm... so sorry... No!… |
| Y'know | 3 | …drink... Let's find a place. ...Y'know what, never mind. Huh? Nn… |
| Anyway | 2 | …t lie about anything. You jerk. Anyway! To be straight with you,… |
| Babe | 2 | …be bad people. My, my. Ukon! Babe. Honey. I've missed you SO\… |
| Bwuh | 2 | …Well, now. Do I have a visitor? Bwuh!? In a corner of the room d… |
| Crap | 2 | …on my face? Oh... S-Sorry, no. Crap. I was staring, wasn't I? A… |
| Eep | 2 | …ediocre. Hey, love, you around? Eep! Ah, there you are. Thought… |
| Finally | 2 | …ing is... What's this place...? Finally, after a long ascent, I… |
| Geez | 2 | …t I'm not gonna let you say it. Geez, don't pop a vein making th… |
| Halfway | 2 | …'s cold out here. *CLATTER* Hm? Halfway back to my room from the… |
| Heard | 2 | …he contraband item actually is. Heard it was "live" and "fresh,"… |
| Hmhm | 2 | …fer it towards her empty cup. Hmhm... I was curious as to what… |
| Hrm | 2 | …terate. I glance to the side... Hrm... ah... Kuon sits beside me… |
| Judging | 2 | …but... just who is this person? Judging by the luxurious room, t… |
| Promise | 2 | …area, right? Yeah, that's all. Promise. Ukon gives his answer w… |
| Quit | 2 | …, love. Is THIS one your lover? Quit taking everything there. No… |
| Sleepy | 2 | …are of herself, anyway. Ah... Sleepy. Well, whatever. Maybe sh… |
| Sounds | 2 | …der arrest! ...What's all this? Sounds like bandits. It came fro… |
| This'll | 2 | …, no, I shouldn't bother her. This'll heal up on its own. If i… |
| Try | 2 | …'re earnest to a fault, y'know. Try saying that to the others,… |
| Understood | 2 | …t's no big deal. Come see me. U-Understood. I can't help but n… |
| Walking | 2 | …g workers cleaning the rooms. Walking around like this is givi… |
| Welp | 2 | …n, and my cup nearly overflows. Welp. Without further ado... I b… |
| Whence | 2 | …must be thrifty. GYAH!? Pain! Whence doth this pain come? Maro… |
| A'ight | 1 | …u to leave this one to me. Huh? A'ight, I guess. If you say so,… |
| Ack | 1 | …tents out and pastes them on. Ack...! Ow, ow, it stings--!! Wh… |
| Acquaintances | 1 | …ork with him is still secret. Acquaintances... Well, not quite… |
| Ahahaha | 1 | …ver since we first met. Huh? ...Ahahaha, I'm blushing. You flatt… |
| Alack | 1 | ….Yeah, let's finish our patrol. Alack, how the cold doth bore in… |
| Alas | 1 | …as to throw stones at him? ...Alas, no voice doth answer. But… |
| Alcohol | 1 | …ouuuu really think sho...? Urk. Alcohol's getting to me. I can… |
| Altered | 1 | …an to throw off her pursuers. Altered gender presentation is… |
| Apothecary | 1 | …they fester or get infected. Apothecary wisdom? That's right.… |
| Asleep | 1 | …rinking. Oh... right... Oh, my. Asleep already, are we? Hm hm. S… |
| … | … | (+146 mais) |

## Ja cobertos pela KB (conferencia)
Atuy, Capital, Haku, Hakurokaku, Hakurokaku Inn, Imperial Guard, Inn, Kiwru, Kuon, Maroro, Mikado, Nekone, Nosuri, Oshtor, Point, Rulutieh, Tatari, Twin Shields Oshtor, Ukon
