# Fase 0 — capitulo 14 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 14 --check`.

- cenas do capitulo: 14_01, 14_02, 14_03, 14_04, 14_06, 14_07, 14_08, 14_09, 14_10
- research_log reconciliado: sim
- nao cobertos: **5 bloqueante(s)** (recorrem >=2 cenas) + 14 de baixa confianca | fracos (ruido): 196 | ja cobertos: 13

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Nekone | **SIM** | 94 | 14_04 | 14_04, 14_08, 14_09, 14_10 | …Hey, we've been waitin' on ya! Nekone! Adoring cheers--well, mo… |
| Mikazuchi | **SIM** | 8 | 14_10 | 14_10 | …. Ahem! He is the very equal of Lord Mikazuchi, Imperial Guard… |
| Imperial Guard | **SIM** | 5 | 14_10 | 14_10 | …rectly, his name was... Oshtor, Imperial Guard of the Right... T… |
| Hoo | **SIM** | 3 | 14_10 | 14_10 | …iful treats before... Old man Hoo hoo! I'm flattered, so I am.… |
| Mausoleum | **SIM** | 3 | 14_02 | 14_02, 14_09 | …in the capital. Ah, that's the Mausoleum. Mausoleum? It's like.… |
| Akuruturuka | — | 2 | 14_09 | 14_09 | …he people and the city... the Akuruturuka. Akuruturuka... I ha… |
| Glad | — | 2 | 14_04 | 14_04 | …but she acts like an old man... Glad she's in a good mood, anywa… |
| Mmf | — | 2 | 14_04 | 14_04 | …a bath always hits the spot. Mmf. Kuon drains her cup as quic… |
| Nuko | — | 2 | 14_10 | 14_10 | …s. Is this... the divine beast, Nuko? Nuko? The creature from...… |
| Twin Shields | — | 2 | 14_10 | 14_10 | …rd of the Left and one of the Twin Shields of Yamato... Lord O… |
| Hakurokaku Inn | — | 1 | 14_03 | 14_03 | …of greenery. Here we are--the Hakurokaku Inn. It's a renowned\… |
| Imperial Capital | — | 1 | 14_09 | 14_09 | …d. I've seen it before, but the Imperial Capital really is an… |
| Noticing Nekone | — | 1 | 14_04 | 14_04 | …s at Kuon, stunned. Right? I... Noticing Nekone's eyes on her, K… |
| Omuchakko River | — | 1 | 14_09 | 14_09 | …across the city. This is the Omuchakko River. Boats of all si… |
| Onvitaikayan--the Great Fathers | — | 1 | 14_04 | 14_04 | …e ancients, too. Especially the Onvitaikayan--the Great Fathers.… |
| Urghbwa Ahhh | — | 1 | 14_03 | 14_03 | …everyone in the splash zone. Urghbwa-- Ahhh. Ah ha! Ahahaha,… |
| Wh Wha | — | 1 | 14_04 | 14_04 | …scene. Won't you notice her? Wh-- Wha... I... Ah... That's wh… |
| Wild Chrysanthemum | — | 1 | 14_03 | 14_03 | …s are already gathered in the Wild Chrysanthemum Room. Gotcha.… |
| Worker Hm | — | 1 | 14_03 | 14_03 | …be a group here ahead of me? Worker Hm? Ah, yes... Your frien… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Wait | 9 | …est to you guys. Yes, s... Sir? W-Wait a minute! Ukon wearily ru… |
| Dear | 7 | …her. Just what are you doing? D-Dear... brother? Wait, she's n… |
| C'mon | 6 | …ignore me over here. Bahahaha! C'mon, what's the fuss? You got… |
| Urgh | 6 | …just want to get to the food. Urgh... Rulutieh shyly bows in f… |
| Cheers | 5 | …capital, and to new comrades! Cheers! Cheers! Cheers. Ch-Cheer… |
| Ahahaha | 4 | …t brows twitch for some reason. Ahahaha... No, nothing's wrong.\… |
| Mhm | 4 | …. It's probably delicious. ...Mhm. I think it's very nice. Yes… |
| Ngh | 4 | …how her you're safe, I think. Ngh... It's not like this was an… |
| Ahaha | 3 | …g that's the real reason, then. Ahaha, I see. If that's the case… |
| Bah | 3 | …equires your personal presence. Bah! Don't say stuff like that.… |
| Finally | 3 | …r standing out from the rest. Finally. This city is way too bi… |
| Like | 3 | …nd of special occasion today? Like a festival or something? Hm… |
| Ahahah | 2 | …l candy suits you finely, eh? Ahahah, you certainly have a way… |
| Ahahahaha | 2 | …it run down her arms, giddy. Ahahahaha!! Kuon flops her whole… |
| Ahh | 2 | …Cheers. Ch-Cheers... *Gulp*... Ahh. At Ukon's toast, Kuon drain… |
| Alas | 2 | …big a deal if HE passed it? ...Alas, Maroro is an underscholar… |
| Anyway | 2 | …Y-You must be imagining things. Anyway, we're gonna be having th… |
| Bahahaha | 2 | …Hey, don't ignore me over here. Bahahaha! C'mon, what's the fuss… |
| Beyond | 2 | …at difficult? The exam, I mean. Beyond compare. But one or two a… |
| Eep | 2 | …d, and her eyes meet mine. ...Eep. Rulutieh gasps, going stiff… |
| Especially | 2 | …ll be happy to see you there. Especially since the kid's footi… |
| Forsooth | 2 | …nt kinds of scholars, then... Forsooth, would such things tran… |
| Geez | 2 | …re like you outright SHOWED me. Geez-- Did you say something? N-… |
| Hearing | 2 | …h, too. Sexy and strong, huh... Hearing that, I glance over my s… |
| Hee | 2 | …fruit and herbs... I believe. Hee hee, it looks like the gold… |
| Hmhm | 2 | …re so close to the capital... Hmhm. In other words, you're giv… |
| Hrm | 2 | …ekone's face instantly reddens. Hrm. Ukon tilts his head, puzzle… |
| Nice | 2 | …and the cute one's Rulutieh. Nice to meet y--Hey, "hapless"?… |
| Sigh | 2 | …just sort of... in the open. *Sigh* Under typical circumstance… |
| Somehow | 2 | …st... cover yourself... please. Somehow, I can't bring myself to… |
| Surely | 2 | …long I've waited for this day! Surely, it must be providence th… |
| Thud | 2 | …t'd make him more relatable. *Thud, thud, thud--* Without sayi… |
| Welcome | 2 | …Sorry, my bad. ...Dear brother. Welcome home. Yeah. 's good to b… |
| Yorkur | 2 | …call it a staple dessert. Oh... Yorkur... Yorkur? It's fermented… |
| Accompanying | 1 | …Oh, I've been in there before. Accompanying Rulutieh, anyway.… |
| Across | 1 | …turns to look at the open door. Girl Across the threshold stands… |
| Adoring | 1 | …'ve been waitin' on ya! Nekone! Adoring cheers--well, more like… |
| Ahahaaaa | 1 | …there, stuck at Kuon's mercy. Ahahaaaa... You've got really ni… |
| Ahhh | 1 | …ew. Here, your turn. All right. Ahhh. After a job well done, tha… |
| Allies | 1 | …three cups. That's the rule. ...Allies, huh. Phew. Here, your tu… |
| … | … | (+156 mais) |

## Ja cobertos pela KB (conferencia)
Cocopo, Haku, Kujyuri, Kuon, Maroro, Mikado, Oshtor, Ozen, Pillar, Rulutieh, Ukon, Ukon Cohort, Yamato
