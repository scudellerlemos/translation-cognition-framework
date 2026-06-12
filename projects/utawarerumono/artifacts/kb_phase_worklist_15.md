# Fase 0 — capitulo 15 — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> 15 --check`.

- cenas do capitulo: 15_01, 15_02, 15_03, 15_04, 15_05, 15_06, 15_07, 15_08, 15_09
- research_log reconciliado: sim
- nao cobertos: **0 bloqueante(s)** (recorrem >=2 cenas) + 5 de baixa confianca | fracos (ruido): 223 | ja cobertos: 27

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Ahahahaha | — | 2 | 15_02 | 15_02 | ….. is... nyaa... the calico." Ahahahaha! Come on, now. This is… |
| Yargh | — | 2 | 15_01 | 15_01 | …? Oh, thanks. Bleaghaaaah!! Yargh, that's HOT-- Wh-Why, that… |
| Combat Tutorial | — | 1 | 15_08 | 15_08 | {c5}Combat Tutorial{c-1} added to th… |
| Empire Top | — | 1 | 15_04 | 15_04 | …e Hakurokaku? It's listed in "The Empire's Top 100 Inns." The… |
| Highness Princess Anju | — | 1 | 15_03 | 15_03 | …f my dear br--of Lord Oshtor. Her Highness Princess Anju is th… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Dear | 13 | …I allowed to get angry at that? Dear sister. I did not want to t… |
| Wait | 11 | …ial Guard of the Right himself. Wait a second, why is he...? Wel… |
| Urgh | 9 | …ot, if you can't even read... Urgh, my negligence is inexcusab… |
| Hrm | 5 | …g at the far end of the room... Hrm...! How good of you to come.… |
| Ack | 4 | …, in fact, a country bumpkin. Ack. Kiwru deflates at Nekone's… |
| Ahaha | 4 | …rily difficult for ourselves? Ahaha, well, um. We don't exactl… |
| Wha | 4 | …tension of your desire! Wh... Wh-Wha... Wait, what? Oshtor and… |
| C'mon | 3 | …. There. Is that good? For now. C'mon, let's do the next line. "… |
| Cripes | 3 | …think that made it all clear. Cripes. You really are a sharp o… |
| Especially | 3 | …way, then... It is no trouble. Especially since this concerns… |
| Honestly | 3 | …a care as she smiles. Though... Honestly, I figure I woulda done… |
| It'd | 3 | …strangers into your retinue. It'd be weird if we WEREN'T su… |
| Mhm | 3 | …with you. Rulutieh bows to us. Mhm. I look forward to it. Kuon… |
| Nice | 3 | …lf. I am Kiwru, of Ennakamuy. Nice to meet you. You can call m… |
| Actually | 2 | …but... Well, I can't read it... Actually, what language is thi… |
| Ahh | 2 | …really it? That's all there is? Ahh, that was really funny. That… |
| Charmed | 2 | …iption of his duties. I'm Haku. Charmed. Oh, yes, it's a pleasur… |
| Damn | 2 | …live it large. Large, damn it! Damn straight! Nothing better'n.… |
| Eep | 2 | …n while the law seeks his head? Eep! Man Whup! Sorry, miss. Wasn… |
| Henchman | 2 | …'bout it. See ya later, cutie. Henchman Ah! Hey, boss, come che… |
| Pleased | 2 | …uld you be... Ah, n-never mind. Pleased to make your acquainta… |
| Regular | 2 | …it very ferocious, or...? Nope. Regular old fish. It's pretty go… |
| Wwwh | 2 | …ying. That's kind of messed up. Wwwh... Wwwh? Wwhhaa...!! Grhaaa… |
| Yeesh | 2 | …, making it nigh-untraversable. Yeesh. Isn't this a bigger crowd… |
| Acquaintance | 1 | …she an acquaintance of yours? Acquaintance... Well, she live… |
| Ahahah | 1 | …What, something wrong with me? Ahahah... I believe it means tha… |
| Ahahaha | 1 | …for the rest of my life. Huh... Ahahaha! We'd all had a little b… |
| Ahahahah | 1 | …d of the Right. Heheheh...... Ahahahah! I can hear Kuon's laug… |
| Alack | 1 | …airly is prohibitive at best. Alack... Maroro withers in disap… |
| Amazing | 1 | …n capital. Is that all true...? Amazing... Um... You, ah. You ar… |
| Art | 1 | …s in on that. Speak now, speak! Art thou perhaps in need of co… |
| Awful | 1 | …ming to the capital for that... Awful lot of trouble to go throu… |
| Bah | 1 | …hy so quiet all of a sudden? ...Bah. You really are disappointin… |
| Bahahaha | 1 | …y honorable brother...? Ah... Bahahaha! Yeah, I guess the cat'… |
| Bandits | 1 | …e bandits we captured before? Bandits... You mean the ones tha… |
| Based | 1 | …tractors to begin with. ...Why? Based on what Ukon told us, a sm… |
| Basically | 1 | …Osh--geez, this is confusing. Basically, he sent her to keep u… |
| Bleaghaaaah | 1 | …r cup of tea. Hm? Oh, thanks. Bleaghaaaah!! Yargh, that's HO… |
| Bleeerghaaaargh | 1 | …? By all means. Here you are. Bleeerghaaaargh!! It serves you… |
| Blurghaaah | 1 | …e dark. Tch, he's getting awa-- Blurghaaah!! From the shadow of… |
| … | … | (+183 mais) |

## Ja cobertos pela KB (conferencia)
Atuy, Cocopo, Divine Scion, Ennakamuy, Guard, Haku, Hakurokaku, Hakurokaku Inn, Hororon, Imperial, Imperial Guard, Inns, Kiwru, Kujyuri, Kuon, Maro, Maroro, Mikado, Moznu, Nekone, Oshtor, Ozen, Rulutieh, Shields, Twin, Ukon, Yamato
