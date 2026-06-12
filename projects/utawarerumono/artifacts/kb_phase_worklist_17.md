# Fase 0 — capitulo 17 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 17 --check`.

- cenas do capitulo: 17_01, 17_02, 17_03, 17_04, 17_06
- research_log reconciliado: sim
- nao cobertos: **7 bloqueante(s)** (recorrem >=2 cenas) + 17 de baixa confianca | fracos (ruido): 288 | ja cobertos: 24

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Wait | **SIM** | 17 | 17_01 | 17_01, 17_04, 17_06 | …small amount to be this potent. Wait, is she OK!? She didn't fal… |
| Dekopompo | **SIM** | 16 | 17_03 | 17_03, 17_04 | …r this job is none other than Dekopompo, of the Eight Pillar G… |
| Touka | **SIM** | 13 | 17_01 | 17_01 | …eeper in her face. ...Mother... Touka!? Hyah!? N-No! I have no i… |
| Chalafun | **SIM** | 9 | 17_01 | 17_01 | …what joy you have given humble Chalafun! I have not felt such… |
| Cheers | **SIM** | 3 | 17_01 | 17_01 | …ne reaching a difficult age...! Cheers! *Yawn*...... That was qu… |
| Ooh | **SIM** | 3 | 17_01 | 17_01 | …not recognize true beauty... Ooh, my... That's far too much p… |
| Thou | **SIM** | 3 | 17_01 | 17_01 | …t is of the finest provision! Thou wilt not be disappointed, t… |
| Bokoinante | — | 2 | 17_04 | 17_04 | …Lord Dekopompo! What is it now, Bokoinante? I'm ensuring the i… |
| Damn | — | 2 | 17_04 | 17_04 | …I think that's check. Hnngh... Damn it, this isn't how this was… |
| Fate | — | 2 | 17_01 | 17_01 | …iny brought us to each other. Fate cannot be denied. Ah... Or… |
| Game | — | 2 | 17_01 | 17_01 | …tune circumstances for... the Game. Maroro swiftly pours the d… |
| Mmmmm | — | 2 | 17_01 | 17_01 | …into it. *Munch, munch, munch* Mmmmm, s' good! I also made thos… |
| Nugwisomkami | — | 2 | 17_01 | 17_01 | …h appear. Or were they called Nugwisomkami around here? Th-T… |
| Perfect | — | 2 | 17_01 | 17_01 | …just roll it up like this... Perfect. Satisfied, I look again… |
| Sisters | — | 2 | 17_01 | 17_01 | …. Sh-She's, ah... one of the m--Sisters!! Sisters, who raised… |
| Barkeep Welcome | — | 1 | 17_01 | 17_01 | …enjoy an evening hereabouts. Barkeep Welcome. What will it be… |
| Chalafun Halt | — | 1 | 17_01 | 17_01 | …use you're kinda cute!? Huh!? Chalafun Halt!! You scoundrels!… |
| Glad Kuon | — | 1 | 17_01 | 17_01 | …Gahahahaha! You got that right! Glad Kuon wasn't here this time.… |
| Hakurokaku Inn Owner | — | 1 | 17_01 | 17_01 | …ns... ...Yours sincerely, the Hakurokaku Inn Owner. The paper… |
| Mayhap Master Haku | — | 1 | 17_01 | 17_01 | …es into his usual seat. Ah... Mayhap Master Haku and his compa… |
| Methinks Master Haku | — | 1 | 17_01 | 17_01 | …st deserving of its prestige. Methinks Master Haku would take… |
| Thugs Geheheheheh | — | 1 | 17_01 | 17_01 | …ve just as much fun here too. Thugs Geheheheheh! ...You boys k… |
| Ukon Cheers | — | 1 | 17_01 | 17_01 | …it, but I'll toast it! Haku & Ukon Cheers!! Gahahah! We make a… |
| Wh Kuon | — | 1 | 17_01 | 17_01 | …ning from people like that, hm? Wh-- Kuon appears in front of me… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Hee | 7 | …Well, someone's in a good mood. Hee hee, well, I happened to hel… |
| Hmhm | 7 | …k Nekone would appreciate it. Hmhm. It is the kind of thing Ne… |
| Mhm | 6 | …'s finished. ...Whew. All done? Mhm, that should be good for now… |
| Urgh | 5 | …ssier. You're probably right... Urgh, I... I see. But could we n… |
| Ahahaha | 4 | …na make bath oil out of that? Ahahaha, not this one, but the v… |
| Gulp | 4 | …Well, let's give it a shot... *Gulp* Th-This is...! Oh man, thi… |
| Ngh | 4 | …d drink together as siblings. Ngh... I'm gettin' all misty.… |
| Sigh | 4 | …door and watch her leave. ...*Sigh* I still feel guilty about… |
| Wha | 4 | …ng strange fell in... *CRACK* Wha--!? A blinding light fills t… |
| Whew | 4 | ....Whew. That about does it for all… |
| Amazing | 3 | …be damned. You got it perfect. Amazing... A trifle, master! Thi… |
| Anyway | 3 | …t WHY these guys are after her. Anyway, I just think we should f… |
| Course | 3 | …een handling the dirty work. 'Course I won't. Once I'm married… |
| Eep | 3 | …Atuy looks into the man's face. Eep!? The man suddenly breaks fr… |
| Holy | 3 | …r beyond what I had expected. Holy crap, that stuff's powerful… |
| It'll | 3 | …only a word of caution for me. It'll be a walk in the park. All… |
| Kick | 3 | …ok nice out there in the yard? *Kick* Ow! What the-- H-Hey-- *… |
| Kind | 3 | …up gently. Whew... Thank you... Kind miss, may I have the hono… |
| Munch | 3 | …you go, one tripe stew. Yeah. *Munch, munch* Pfah, desh hoht...… |
| Prithee | 3 | …h one's which? Yes. Think so. Prithee, if I may... Maroro pick… |
| Stop | 3 | …bugs! *Crunch, crunch, crunch* S-Stop! Please, I'm begging you!… |
| What're | 3 | …ous. Thug Hey there, beautiful. What're you doin' in a place l… |
| Actually | 2 | …eful out there. What's wrong? Actually, it's already dark. The… |
| Ahh | 2 | …e supposed to USE gold bars!? Ahh, the wonderful shouts of joy… |
| Augh | 2 | …apping the guy across the face. Augh... Hrgghhh... Of course, th… |
| Bah | 2 | …ying a gentle, tipsy buzz. ...Bah. A lone cup ill satisfies th… |
| C'mon | 2 | …ch them pamper her like that. C'mon, Haku, you should try some… |
| Crunch | 2 | …to nimbly snatch up the bugs. *Crunch, munch, crunch* WHAAAAT!?… |
| Erm | 2 | …tentious guys like him? Uh... Erm, well, to each their own, as… |
| Excellent | 2 | …nything particularly special. Excellent. You have my gratitude… |
| Fish | 2 | …ar. They should be delicious. Fish, huh... Mm. That does sound… |
| Fwoop | 2 | …y for mercy now... *Wriggle* *Fwoop, fwoop, fwoop* Kurarin lea… |
| Geez | 2 | …something round, and I slip. Geez, that was close. Almost bro… |
| Goodness | 2 | …brother as an Imperial Guard. Goodness. I had no idea my papa… |
| Hic | 2 | …before we run into trouble. *Hic* A toast! L'ss make a toast.… |
| Hmmm | 2 | …e you somewhere real special. Hmmm...? Oh, sorry, but do you h… |
| Hyah | 2 | …That pattern... isn't that...? Hyah!? The worker's eyes fall on… |
| Items | 2 | …see around you are rarities! Items from my personal collectio… |
| Ohhh | 2 | …show you a reeeaaal good time. Ohhh, so that's what it was. Y… |
| Pardon | 2 | …iative with her, you know... ...Pardon? Never mind. Well, I gues… |
| … | … | (+248 mais) |

## Ja cobertos pela KB (conferencia)
Atuy, Cocopo, Haku, Hakurokaku, Hakurokaku Inn, Imperial Guard, Karulau, Kiwru, Kuon, Kurarin, Maro, Maroro, Mikado, Mikazuchi, Nekone, Nosuri, Oshtor, Ougi, Pillar, Rulie, Rulutieh, Twin Shields, Ukon, Yamato
