# Fase 0 — capitulo 30 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 30 --check`.

- cenas do capitulo: 30_01, 30_02, 30_03, 30_04, 30_05, 30_06, 30_07, 30_08, 30_09, 30_10, 30_11
- research_log reconciliado: sim
- nao cobertos: **11 bloqueante(s)** (recorrem >=2 cenas) + 16 de baixa confianca | fracos (ruido): 243 | ja cobertos: 48

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Ngh | **SIM** | 8 | 30_04 | 30_04, 30_05, 30_09, 30_10 | …maybe? Quiet down. Oh, dear... Ngh. My apologies. They can move… |
| Hee | **SIM** | 6 | 30_04 | 30_04, 30_07, 30_08, 30_09, 30_10 | …we can all share together... Hee. That's my Rulie. Phew. Fina… |
| Speak | **SIM** | 4 | 30_01 | 30_01, 30_10 | …spired to a-- Hold your tongue. Speak not such accusations wit… |
| Yatanawarabe | **SIM** | 4 | 30_01 | 30_01 | …to find Woshis and one of his Yatanawarabe conversing. They… |
| Follow | **SIM** | 3 | 30_04 | 30_04, 30_10 | …ing...? A map of the waterways. Follow the path marked in red,… |
| Ohn Riyaak | **SIM** | 3 | 30_07 | 30_07, 30_09 | …f the imperial capital... the Ohn Riyaak. Ohn Riyaak... Is tha… |
| Open | **SIM** | 3 | 30_10 | 30_10 | …s, backing down. ...Understood. Open the gates. Y-Yes sir... Ope… |
| Osh | **SIM** | 3 | 30_01 | 30_01, 30_08 | …is? The herbal tea you sent me, Osh-- *cough*--the--*cough, co… |
| Goodbadguy | — | 2 | 30_04 | 30_04 | …ht, buddy, your name's gonna be Goodbadguy. Nice to meet you,… |
| Hahh | **SIM** | 2 | 30_05 | 30_05, 30_09 | …Her Highness--Nghh...! Gah...! Hahh... hahh... hahh... The mome… |
| Nrrgh | — | 2 | 30_09 | 30_09 | …olySurface24630 polySurface2330 Nrrgh... hah. Is this... blood..… |
| Someday | — | 2 | 30_04 | 30_04 | …l to me...eventually. I will. Someday. I promise. All right. I… |
| True | **SIM** | 2 | 30_04 | 30_04, 30_07 | …longer requires my protection. True. She's grown up into quite… |
| Wonder | **SIM** | 2 | 30_05 | 30_05, 30_09 | …en walking for quite a while. Wonder what's above us right now… |
| Anju Shit | — | 1 | 30_08 | 30_08 | …own throat. Nh... ah... hhh... Anju-- Shit, we barely made it i… |
| Follow Dekopompo | — | 1 | 30_10 | 30_10 | …open, we have little choice. Follow Dekopompo's soldiers insi… |
| Grab Nekone | — | 1 | 30_11 | 30_11 | …ld you stop flailing--Nosuri! Grab Nekone's legs! Yes, leave i… |
| Lounge Mode | — | 1 | 30_04 | 30_04 | …es as Atuy switches into full Lounge Mode. How can you relax?… |
| Mark Vurai | — | 1 | 30_09 | 30_09 | …is too early yet to give up. Mark Vurai closely. What? The fo… |
| O Osh | — | 1 | 30_03 | 30_03 | …Tell me... Where is Oshtor...? O-- Osh... tor... |
| Uzurushan Soldier Gghh | — | 1 | 30_06 | 30_06 | …ously, you can HAVE the name. Uzurushan Soldier Gghh... We los… |
| Wh Lord Oshtor | — | 1 | 30_01 | 30_01 | …! What is going on!? Excuse us! Wh-- Lord Oshtor. I must ask tha… |
| Wh Osh | — | 1 | 30_11 | 30_11 | …t, I might be able to save her! Wh-- Osh... tor... Dear... broth… |
| Wha Impossible | — | 1 | 30_09 | 30_09 | …... Is that... truly your best? Wha-- Impossible... After taking… |
| Yatanawarabe Liveruni | — | 1 | 30_01 | 30_01 | …Where is Lady Honoka right now? Yatanawarabe Liveruni W-Well...… |
| Yatanawarabe Ravieh Lord Woshis | — | 1 | 30_01 | 30_01 | …idence. M-My deepest apologies. Yatanawarabe Ravieh Lord Woshis.… |
| Yatanawarabe Shyasurika Lord Woshis | — | 1 | 30_01 | 30_01 | …e shoes of a pretender empress. Yatanawarabe Shyasurika Lord Wos… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Plane | 99 | …and harmony that knows no end. pPlane1 pCylinder21 pCylinder22 p… |
| Surface | 72 | …ering. Dear brothe-- lock04 polySurface731 polySurface27814 poly… |
| Cylinder | 38 | …ony that knows no end. pPlane1 pCylinder21 pCylinder22 pCylinder… |
| Stop | 7 | …nd to sort out right now. Hm? Stop the carriage. Aren't those… |
| Lady-in-waiting | 6 | …ng to hunt us down after all? Lady-in-waiting Please forgive t… |
| Impressive | 5 | …They just... ran up the walls. Impressive. You seem cautious. Y… |
| Nyeh | 5 | …ourns in silence and isolation. Nyeh!? This is preposterous! Wha… |
| Course | 4 | …good girl while I was gone? 'Course I was good! I'm ALWAYS go… |
| Sigh | 4 | …Everyone's mind is made up. *Sigh*... Yeah, I should have fig… |
| Courage | 3 | ….. I do not have the courage... Courage... Kiwru. What is courag… |
| Excuse | 3 | …Are you awake? Hm? Yes, enter. Excuse me. I've brought you tea.… |
| Finally | 3 | …m the Tiriryarai? Well... Hmph. Finally, some movement. NYEH!? B… |
| Ghh | 3 | …nt will not help your cause. ...Ghh! We serve a different genera… |
| Hmhm | 3 | …circumstances indeed. Still... Hmhm. This does intrigue me some… |
| Holy | 3 | …dn't think it'd work THAT well. Holy shit. A warning. Please do… |
| Suddenly | 3 | …o long as you reach the palace? Suddenly, a voice from behind me… |
| Tea | 3 | …xcuse me. I've brought you tea. Tea? I did not ask for tea. Lord… |
| Welcome | 3 | …e, and the door crashes open. Welcome back, Dad! Hey, Shinonon… |
| Actually | 2 | …oesn't even seem to notice her. Actually, the soldiers' bodies j… |
| Beside | 2 | …Finally, some movement. NYEH!? Beside the gates, a much smaller… |
| Better | 2 | …aces. It's more of a costume. Better than nothing, I suppose.… |
| Call | 2 | …ef truly driven you to madness? Call me a madman if you wish.… |
| Calm | 2 | …e!? Gah-- P-Please, Lord Vurai! Calm yourself! You mustn't use v… |
| Center | 2 | …lySurface24646 polySurface24647 Center_desk Center_desk1 polySur… |
| Eek | 2 | …than the very poison you hold. Eek!? Please, Lord Vurai, calm y… |
| Eep | 2 | …oman. Do you mean to insult me? Eep... Hm? I was just commenting… |
| Geez | 2 | …e by side. It's finally over... Geez, that was nearly it for m… |
| Glad | 2 | …cool this is! It's all sparkly! Glad you're happy with it, kid.… |
| Hmhmhm | 2 | …s actually pretty impressive. Hmhmhm. The pieces are in place.… |
| Jiggle | 2 | …Kurarin's all pumped up, too! *Jiggle, jiggle* This is my duty… |
| Mercifully | 2 | …attempt on the princess's life. Mercifully, Her Highness survive… |
| Mhm | 2 | …ow he can do this... I see... Mhm. You're right. Haha... Give… |
| Nghh | 2 | …Vurai! Are you--You dare to-- Her Highness--Nghh...! Gah...! H… |
| Nyargh | 2 | …my absence from the capital! Nyargh!? Soldiers Arrrrrrrgh!! T… |
| Oho | 2 | …And being his right hand man... Oho! What a promotion for me!… |
| Rrrgh | 2 | …and not just some pillar... ...Rrrgh! GYAGH!? Haku!? You need t… |
| Save | 2 | …ds. Wh--Hold on a second, here. Save the princess? I'm starting… |
| Shit | 2 | …lar and dashes toward Oshtor. Shit! What the--!? What was that… |
| Stand | 2 | …ping child. What are you doing? Stand up. Stand and rule. Comman… |
| Stay | 2 | …onsible for this transgression. Stay yourself, Lord Vurai! We ne… |
| … | … | (+203 mais) |

## Ja cobertos pela KB (conferencia)
Akuruka, Akuruturuka, Anju, Atuy, Bokoinante, Chains, Cocopo, Dekopompo, Divine Scion, Ennakamuy, Entua, Haku, Hakurokaku, Hakurokaku Inn, Honoka, Imperial Guard, Jachdwalt, Kamunagi, Karulau, Kiwru, Kuon, Kurarin, Maroro, Mikado, Mikazuchi, Munechika, Nekone, Nekone Kuon, Nosuri, Oshtor, Ougi, Pillar, Pillars, Raiko, Rulie, Rulutieh, Saraana, Shichirya, Shinonon, Touka, Tuskur, Uruuru, Uzurusha, Uzurushan, Vurai, Woshis, Yamatan, Yamato
