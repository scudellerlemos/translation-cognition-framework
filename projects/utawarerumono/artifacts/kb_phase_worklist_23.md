# Fase 0 — capitulo 23 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 23 --check`.

- cenas do capitulo: 23_01, 23_02, 23_03, 23_04, 23_05, 23_06, 23_07, 23_08, 23_09, 23_10, 23_11, 23_12, 23_13, 23_14, 23_15, 23_16, 23_17, 23_18, 23_20
- research_log reconciliado: sim
- nao cobertos: **0 bloqueante(s)** (recorrem >=2 cenas) + 7 de baixa confianca | fracos (ruido): 269 | ja cobertos: 63

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Dekopachi | — | 2 | 23_09 | 23_09 | …gain? Something like Deppa... Dekopachi, maybe, or Degarashi..… |
| Assassin Grh | — | 1 | 23_17 | 23_17 | …pain while they were fighting. Assassin Grh... Urgh... Grrrhhh.… |
| Center Blade | — | 1 | 23_13 | 23_13 | …ecting an attack from us? Blade_Center Blade_Dummy1 And fraterni… |
| Invade Tuskur | — | 1 | 23_01 | 23_01 | …all who stand in our way. ...Invade Tuskur? Wait, why!? Didn'… |
| Loincloth Force | — | 1 | 23_11 | 23_11 | …, we need more! To the skies, Loincloth Force One! Onward! Gah… |
| Merchant Step | — | 1 | 23_07 | 23_07 | …bring myself to say anything. Merchant Step right up, step rig… |
| Mononofu Warehouse | — | 1 | 23_07 | 23_07 | …ks to this one weird trick!" "Mononofu's Warehouse. You're gon… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Ahahaha | 7 | …That's not what the problem is. Ahahaha! You worried I've forgot… |
| You'd | 5 | …hough, are those huge fruits. You'd need both arms to carry on… |
| Aye | 4 | …You gotta keep your chin up. Aye, perhaps, but... in the heat… |
| Oho | 4 | …to depart. Oh! Here she comes! Oho? Well, she definitely looks… |
| Bah | 3 | …y anything to help right now. Bah, wasting our precious time..… |
| Clothes | 3 | …ugs with legs like tree trunks. Clothes or not, they'll never lo… |
| Nyargh | 3 | …h units one, three, and four! Nyargh!? We've also received rep… |
| Shit | 3 | …y! Sound the alar-- {W90}Eh!? Shit. It's the enemy! They're ov… |
| Sigh | 3 | …hem any closer to the truth. *Sigh*... Oh, it's not that bad.… |
| Amazing | 2 | Eep...! Amazing... Hee hee. Makes my ear… |
| Anyhow | 2 | …we withdraw into our shells! Anyhow, why don't we ask the opi… |
| Awww | 2 | …ow." And Anju... slightly nods. Awww, and there goes Munechika.… |
| Blue | 2 | …eady a bed immediately. ...Huh? Blue waters. Blue sky. Passion.\… |
| Bold | 2 | …ur liege with such audacity!? Bold of him. A bold move, indeed… |
| Crap | 2 | …e one who deceived us before! Crap... It's the guys we met on… |
| Crew | 2 | …ys, anchors aweigh! Cast off! Crew SIR! A raucous response fro… |
| Disappointing | 2 | …ady... What's wrong? Let's go. Disappointing. You are an incorr… |
| Eeeee | 2 | …big enough to ride, even. Eee! Eeeee! *click, click, click, c… |
| Egh | 2 | …u art too kind... *Pfflfflfflp* Egh, it's covered in snot now...… |
| Fighting | 2 | …e. It's worse than I thought. Fighting in a land where the ene… |
| Hard | 2 | …I see. It's... pretty big, huh. Hard to imagine something like t… |
| Hmhm | 2 | …ne. The delivery is a side gig. Hmhm... It's reassuring to hear… |
| Holy | 2 | …p but let out a sigh of relief. H-Holy shit... that was scary...… |
| Hup | 2 | …'m not too worried. Hm hm hm... Hup, hup, hup. I didn't expect y… |
| Judging | 2 | …elves as they close in on us. Judging by how relaxed they are,… |
| Konjac | 2 | …e... Could this be... konjac? Konjac? Konjac...hot air balloon… |
| Merely | 2 | …huses you so, do as you will. Merely remember what I said. Nye… |
| Mhm | 2 | …t... Could that be a yanmororo? Mhm. The roots are edible, if yo… |
| Nuzzle | 2 | …s worried sick about you, aye! *Nuzzle, nuzzle, nuzzle* Egh... U… |
| Nyegh | 2 | …is the case, then please let-- Nyegh!? As the pudgy man begins… |
| Nyeh | 2 | …owed your ego to-- Be silent. Nyeh! You dare...? Munechika gla… |
| Oooh | 2 | …looks damn snazzy with that. Oooh, damn snazzy! Hey, why don'… |
| Probably | 2 | …I-I'll help too, dear sister-- Probably better for Nekone and R… |
| Push | 2 | …ments. Let's book it! G-Got it! Push! Push! PUSH! Tuskur soldier… |
| Sound | 2 | …Tuskur soldier It's the enemy! Sound the alar-- {W90}Eh!? Shi… |
| Suddenly | 2 | …ou desire new clothing, Master? Suddenly, several of the girls i… |
| There'll | 2 | …It'll be like... a short nap. There'll be a whole new world wa… |
| Unfortunately | 2 | …y would react if they knew... Unfortunately for them, I can't… |
| Welp | 2 | …ashore. Oh... Very good, then. Welp, might as well leave the he… |
| Whew | 2 | …hat salty sea wind for so long. Whew, that hit the spot. Ahhh, i… |
| … | … | (+229 mais) |

## Ja cobertos pela KB (conferencia)
Akuruka, Akuruturuka, Anju, Aruruu, Atuy, Benawi, Blade, Bokoinante, Camyu, Cocopo, Dekopompo, Entua, Haku, Hakurokaku, Honoka, Imperial Guard, Jachdwalt, Jachdwalt Jachdwalt, Kiwru, Kujyuri, Kuon, Kurou, Major, Mariner, Maro, Maroro, Mikado, Mikazuchi, Mito, Munechika, Munechika Lord Haku, Munechika The Warmaster, Neko, Nekone, Nosuri, Onkamiyamukai, Oshtor, Ougi, Pillar, Pillars, Raiko, Rulie, Rulu, Rulutieh, Saraana, Shichirya, Shinonon, Shyahoro, Soyankekur, Tatari, Tuskur, Ukon, Uruuru, Uzurusha, Uzurushan, Uzurushans, Vurai, Warmaster, Woshis, Yamatan, Yamatans, Yamato, Yatanawarabe
