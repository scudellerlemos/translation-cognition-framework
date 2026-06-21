# Fase 0 — capitulo all — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> all --check`.

- cenas do capitulo: all
- research_log reconciliado: sim
- nao cobertos: **56 bloqueante(s)** (recorrem >=2 cenas) + 119 de baixa confianca | fracos (ruido): 411 | ja cobertos: 85

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Ludia | **SIM** | 57 | all | all | …uite a fix!" [14][83]C"How dare Ludia treat[01]you like that![02… |
| Try | **SIM** | 28 | all | all | …[07][07]"What's the matter!?[02]Try moving the lever[01]some mor… |
| Using Silverware | **SIM** | 28 | all | all | …ate!" There's a book titled[01]"Using Silverware." There's a boo… |
| Change | **SIM** | 24 | all | all | …e to go[01]now?"[12][82][0C][93]Change destination[01]Cancel sea… |
| Tower | **SIM** | 21 | all | all | …y relic, needed[01]to enter the Tower of Wind,[02]which is sacre… |
| Move | **SIM** | 19 | all | all | …you want to go?[12][02][0C][93]Move ahead[01]Go up[01]Never min… |
| Army | **SIM** | 17 | all | all | …quarters[02]for the Imperial[01]Army, does it?...[01]Wait!" [0C]… |
| Insurance Contract | **SIM** | 16 | all | all | …from zenny earned. You got:[01]Insurance Contract 1! You got:[0… |
| Thirteenth | **SIM** | 14 | all | all | …e[02]during the reign of the[01]Thirteenth and current[01]Empero… |
| Ahtar | **SIM** | 13 | all | all | …peror[01]Shei to the Twelfth[01]Emperor Ahtar. This book details… |
| Causeway | **SIM** | 13 | all | all | …rs[02]who guard the Imperial[01]Causeway.[02]Kyoin means 'people… |
| Eighth | **SIM** | 13 | all | all | …e Fifth Emperor[01]Mugul to the Eighth[01]Emperor Mei. This book… |
| Fifth | **SIM** | 13 | all | all | …story of the Empire[02]from the Fifth Emperor[01]Mugul to the Ei… |
| Fourth | **SIM** | 13 | all | all | …First Emperor[01]Fou-lu to the Fourth[01]Emperor Temul. This bo… |
| Mei | **SIM** | 13 | all | all | …peror[01]Mugul to the Eighth[01]Emperor Mei. This book details t… |
| Ninth | **SIM** | 13 | all | all | …story of the Empire[02]from the Ninth Emperor[01]Shei to the Twe… |
| Temul | **SIM** | 13 | all | all | …eror[01]Fou-lu to the Fourth[01]Emperor Temul. This book details… |
| Twelfth | **SIM** | 13 | all | all | …he Ninth Emperor[01]Shei to the Twelfth[01]Emperor Ahtar. This b… |
| Pukapuka | **SIM** | 12 | all | all | …B]...[0B]..." [0C][03][14][C3]@"Pukapuka..." [0C][03][14][86]E"R… |
| Poko | **SIM** | 11 | all | all | …he mainland?[02][14][81]ARight, Poko?" [14][02][02]"Heh heh...[0… |
| Standing | **SIM** | 9 | all | all | …Under Repairs[06][01] Caution: Standing on the[01] anchor will… |
| Zig | **SIM** | 9 | all | all | …e other day?[02]Their names are Zig, Kryrik,[01]and Iggy. They'r… |
| Chedo | **SIM** | 8 | all | all | …oops[01]and make mine way[01]to Chedo...[02]And yet..." [14][06]… |
| West | **SIM** | 8 | all | all | …ts?" "Lot o' people from[01]the West who want to[02]sell things… |
| P'ung Ryong | **SIM** | 7 | all | all | …5][02]beneath the castle[06]." "P'ung Ryong, the Wind[01]Dragon,… |
| Quit | **SIM** | 7 | all | all | …[0C][93]Begin apprenticeship[01]Quit apprenticeship[01]Never min… |
| Beyd | **SIM** | 6 | all | all | …myself! How rude![02]My name is Beyd, and[01]this is Sen, Shami,… |
| Desert Dif | **SIM** | 6 | all | all | …t, then, I won't[01]go!" Dif.5 Desert Dif.5 Desert Dif.5 Dese… |
| Grass Dragon | **SIM** | 6 | all | all | …01]dragon in the plains,[01]the Grass Dragon." [14][03][03]"Drag… |
| Island | **SIM** | 6 | all | all | …sland ahead!" [0C][06][14][80]@"Island? You[01]mean...?" [14][02… |
| Lyta | **SIM** | 6 | all | all | …mmies or[01]daddies anymore.[02]Sister Lyta takes[01]care of us… |
| Gramps | **SIM** | 5 | all | all | …ere who's[01]ever been there is Gramps.[02]That's what everyone[… |
| Kasq Woods | **SIM** | 5 | all | all | …cle of Wind has[01]lived in the Kasq Woods[02]for as long as any… |
| Kyoin | **SIM** | 5 | all | all | …e of the[01]guards stationed at Kyoin.[02]I hope he gets rotated… |
| Mud | **SIM** | 5 | all | all | …You can't fish in the Sea[01]of Mud, but you can fish[01]here, y… |
| Close | **SIM** | 4 | all | all | …...a god?" "Very well, then.[01]Close your eyes." "Tell me when… |
| Diet Hard | **SIM** | 4 | all | all | …ren." There's a book titled[01]"Diet Hard 3." "Looking for my wi… |
| Dif | **SIM** | 4 | all | all | …ll right, then, I won't[01]go!" Dif.5 Desert Dif.5 Desert Dif.… |
| Fane | **SIM** | 4 | all | all | …d there leads[01]to the [05][02]Fane of the[01]Sea God[06]." [14… |
| Imperial Army | **SIM** | 4 | all | all | …2] "We are a supplier to the[01]Imperial Army! We carry[01]only… |
| Kryrik | **SIM** | 4 | all | all | …er day?[02]Their names are Zig, Kryrik,[01]and Iggy. They're bro… |
| Material | **SIM** | 4 | all | all | …more[01]than once." [05][02]1st Material[06] [05][02]1st Materia… |
| Quit Kecak | **SIM** | 4 | all | all | …]Try for a prize[01]Practice[01]Quit Kecak "Which lesson do you… |
| Rhem | **SIM** | 4 | all | all | …response... [14][01][01]"I saw Rhem go by[01]earlier wearing he… |
| Rudd | **SIM** | 4 | all | all | …ll[01]tell you where to[01]find Rudd.[02]He said he'd hide[01]un… |
| Table Manners | **SIM** | 4 | all | all | …are." There's a book titled[01]"Table Manners for[01]Children."… |
| Tak | **SIM** | 4 | all | all | …e while ago, his pet[01]chicken Tak ran off, and[01]ever since t… |
| Capital | **SIM** | 3 | all | all | …e [05][02]Sonne Village[06].[01]Capital? Oh, that be far[01]off… |
| Catch | **SIM** | 3 | all | all | …un And The Moon" "1-2-3 1-2-3" "Today's Catch" "A Whopper Of A T… |
| Directional | **SIM** | 3 | all | all | …e will be?" Select a character. Directional buttons: Move[01]… |
| Equip | **SIM** | 3 | all | all | …oose a rod and[01]lure to use. NO DATA Equip a rod and lure. Vi… |
| Kahn | **SIM** | 3 | all | all | …e." [0C][06][14][80]@"When that Kahn[01]fellow showed up,[02]we… |
| Rhoppe | **SIM** | 3 | all | all | …." [0C][05][14][04][04]"[05][02]Rhoppe[06]'s got the key[01]to t… |
| Super Combo | **SIM** | 3 | all | all | …[01]zat it is 'arder to[02][19] Super Combo [14][06][06]"Well, h… |
| Ultimate | **SIM** | 3 | all | all | …good balance.[01]Power Level: 3 Ultimate rod Can be used to[01]c… |
| Western | **SIM** | 3 | all | all | …...[02]If you go to the [05][02]Western[01]Plains[06], you can p… |
| Astan Dif | — | 2 | all | all | …f.1 Wyndia Dif.2 Ludia Dif.2 Astan Dif.5 Zhinga Mts. Dif.1… |
| Bastard Sword | — | 2 | all | all | …nd And Round" "Under Pressure" "Bastard Sword" "Another Working… |
| Beginnings | — | 2 | all | all | …in" "Slow Tension" "Endings and Beginnings" "Trouble Ahead" "Eph… |
| Believing | — | 2 | all | all | …f The Plains" "Thousand Winds" "Seeing Is Believing" "A Distant… |
| Cancel Diligent Ordinary | — | 2 | all | all | …r[01][7F]: Confirm [80]: Cancel Diligent Ordinary "We pla… |
| Combo Attacks | — | 2 | all | all | …ut ranks[01]About "learning"[01]About Combo Attacks[01]Never min… |
| Copper Bell ElectrumBell PlatinumBell Monopolize Roulette | — | 2 | all | all | …ny[01]bodyguards right[01]now." Copper Bell ElectrumBell Platinu… |
| Curse | — | 2 | all | all | …"Prayer" "Unwavering Courage" "The Curse" "Turismo" "Replay" "S… |
| Desert Town | — | 2 | all | all | …Money And Run" "Battling Gods" "Desert Town" "Round And Round" "… |
| Distant Land | — | 2 | all | all | …Winds" "Seeing Is Believing" "A Distant Land" "Hills And Streams… |
| Divine Danger | — | 2 | all | all | …, Pukapuka" "For The Princess" "Divine Danger" "Emperor Rampant"… |
| Dragon Blood | — | 2 | all | all | …vine Danger" "Emperor Rampant" "Dragon's Blood" "Whirlpool" "Whi… |
| Dream | — | 2 | all | all | …here" "Floating" "The Endless" "After The Dream" "I've been stud… |
| Dreams | — | 2 | all | all | …01]want to go to the[01]Land of Dreams?"[12] [14][83]C"All right… |
| Dress Shoes Multivitamin | — | 2 | all | all | …0 zenny Midas Stone 1,000 zenny Dress Shoes Multivitamin [0C]D"H… |
| Evocation | — | 2 | all | all | …e secrets[02]of the Spell of[01]Evocation, the[02]knowledge of h… |
| Free Fall | — | 2 | all | all | …ve Heart" "Requiem" "Shepards" "Free Fall" "Neverending Rain" "T… |
| Gold Plains Dif | — | 2 | all | all | …Astan Dif.5 Zhinga Mts. Dif.1 Gold Plains Dif.5 Highlands Dif… |
| Hesperia Dif | — | 2 | all | all | …ains Dif.5 Highlands Dif.3 S. Hesperia Dif.2 Shikk Dif.4 Sal… |
| Highlands Dif | — | 2 | all | all | …Mts. Dif.1 Gold Plains Dif.5 Highlands Dif.3 S. Hesperia Dif… |
| Hills And Streams | — | 2 | all | all | …Is Believing" "A Distant Land" "Hills And Streams" "The Sun And… |
| Imperial Capital | — | 2 | all | all | …]... [0C][81][05][08]Chedo, the Imperial Capital[06][13][90][0C]… |
| Imperial Causeway | — | 2 | all | all | …the entrance to[01]the [05][02]Imperial Causeway[06],[02]which… |
| Islands Dif | — | 2 | all | all | …Shikk Dif.4 Salt Sea Dif.4 N. Islands Dif.3 Paedra Dif.3 C.… |
| Kyria | — | 2 | all | all | …em..." "I mean, the mayor[01]of Kyria is in[01]here...[02]But he… |
| Land | — | 2 | all | all | …Do you[01]want to go to the[01]Land of Dreams?"[12] [14][83]C"A… |
| Ludia Dif | — | 2 | all | all | ….5 Desert Dif.1 Wyndia Dif.2 Ludia Dif.2 Astan Dif.5 Zhinga… |
| Marcy | — | 2 | all | all | …4][04]"That's how Chino[01]gets Sister Marcy[02]and other people… |
| Megaphone Megaphone SpiritBlast Disembowel | — | 2 | all | all | …ck on[01][04][01] and [04][04]! Megaphone Megaphone SpiritBlast… |
| Midas Stone | — | 2 | all | all | …st you!" Soul Ring 10,000 zenny Midas Stone 1,000 zenny Dress Sh… |
| Minigame Instructions | — | 2 | all | all | …ged or[01]anything, though." Minigame Instructions[14][02][02… |
| Mixed | — | 2 | all | all | …d Sword" "Another Working Day" "All Mixed Up" "Poisoned Air" "Tr… |
| Modo | — | 2 | all | all | …yet?" [14][06][06]"Did you see Modo?[02]Try looking north[01]fr… |
| Money | — | 2 | all | all | …"The First Emperor" "Fighters" "Take The Money And Run" "Battlin… |
| Neverending Rain | — | 2 | all | all | …equiem" "Shepards" "Free Fall" "Neverending Rain" "Tree Spirits"… |
| Numbers | — | 2 | all | all | …8! "Starlight Run" "Walkabout" "By The Numbers" "Bringing Home A… |
| Paedra Dif | — | 2 | all | all | …alt Sea Dif.4 N. Islands Dif.3 Paedra Dif.3 C. Hesperia "I alm… |
| Pass | — | 2 | all | all | …][01][03]"Humans are called[01]"They Who Pass,"[02]because they… |
| Peso | — | 2 | all | all | …en, Shami,[01]Rinpo, Poske, and Peso.[02]They wanted to see[01]y… |
| Poisoned Air | — | 2 | all | all | …er Working Day" "All Mixed Up" "Poisoned Air" "Truth And Fiction… |
| Poske | — | 2 | all | all | …1]this is Sen, Shami,[01]Rinpo, Poske, and Peso.[02]They wanted… |
| Pressure | — | 2 | all | all | …Desert Town" "Round And Round" "Under Pressure" "Bastard Sword"… |
| Rampant | — | 2 | all | all | …The Princess" "Divine Danger" "Emperor Rampant" "Dragon's Blood… |
| Retreat | — | 2 | all | all | …rned. Recover and automatically Retreat.[01][05][02]2%[06] is de… |
| Round And Round | — | 2 | all | all | …"Battling Gods" "Desert Town" "Round And Round" "Under Pressure… |
| Ryong | — | 2 | all | all | …elationship." [0C][06][14][80]@"Ryong..." [0C][06][14][80]@"Don'… |
| Sailing The Seven Seas | — | 2 | all | all | …"Turismo" "Replay" "Seagulls" "Sailing The Seven Seas" "Pabupab… |
| Salt Sea Dif | — | 2 | all | all | …S. Hesperia Dif.2 Shikk Dif.4 Salt Sea Dif.4 N. Islands Dif.3… |
| Sandflier Valley | — | 2 | all | all | …[01]we'll go to this[02][05][02]Sandflier Valley[06],[01]and get… |
| Sarai | — | 2 | all | all | ….[01]This your first time[01]to Sarai?" [14][02][02]"munch munch… |
| Sen | — | 2 | all | all | …My name is Beyd, and[01]this is Sen, Shami,[01]Rinpo, Poske, and… |
| Shami | — | 2 | all | all | …me is Beyd, and[01]this is Sen, Shami,[01]Rinpo, Poske, and Peso… |
| Shikk Dif | — | 2 | all | all | …lands Dif.3 S. Hesperia Dif.2 Shikk Dif.4 Salt Sea Dif.4 N. I… |
| Slow Tension | — | 2 | all | all | …Numbers" "Bringing Home A Win" "Slow Tension" "Endings and Begin… |
| Sluice Control Panel | — | 2 | all | all | …01]leave us alone!" [05][02]Sluice Control Panel[06][01]… |
| Song Of The Plains | — | 2 | all | all | …verending Rain" "Tree Spirits" "Song Of The Plains" "Thousand Wi… |
| Sonne Village | — | 2 | all | all | …t' ask.[02]This here be [05][02]Sonne Village[06].[01]Capital? O… |
| Soul Ring | — | 2 | all | all | …seemed to[01]work against you!" Soul Ring 10,000 zenny Midas Sto… |
| Sound Of Money | — | 2 | all | all | …raveling Merchant" "Macho Man" "The Sound Of Money" "Brave Heart… |
| Spell | — | 2 | all | all | …preserved the secrets[02]of the Spell of[01]Evocation, the[02]kn… |
| Sun And The Moon | — | 2 | all | all | …tant Land" "Hills And Streams" "The Sun And The Moon" "1-2-3 1-2… |
| Supplication Supplication Holy Strike Benediction | — | 2 | all | all | …ou're a little[01]short there." Supplication Supplication Holy S… |
| Thief | — | 2 | all | all | …ns?[12] [0C]![01] Catch the Thief![02]To catch the thief, ge… |
| Thousand Winds | — | 2 | all | all | …Spirits" "Song Of The Plains" "Thousand Winds" "Seeing Is Belie… |
| Traveling Merchant | — | 2 | all | all | …" "Watch Your Step" "Darkness" "Traveling Merchant" "Macho Man"… |
| Tree Spirits | — | 2 | all | all | …"Free Fall" "Neverending Rain" "Tree Spirits" "Song Of The Plain… |
| Trouble Ahead | — | 2 | all | all | …sion" "Endings and Beginnings" "Trouble Ahead" "Ephemeral" "The… |
| Truth And Fiction | — | 2 | all | all | …"All Mixed Up" "Poisoned Air" "Truth And Fiction" "Watch Your S… |
| Unwavering Courage | — | 2 | all | all | …"Faeries" "Game Over" "Prayer" "Unwavering Courage" "The Curse"… |
| Valley | — | 2 | all | all | …ey[01]call [05][02]Sandflier[01]Valley[06] near here.[02]It's a… |
| View | — | 2 | all | all | …NO DATA Equip a rod and lure. View fish data. Learn how to fis… |
| Vitamin | — | 2 | all | all | …xt work to you!" Recover with a Vitamin.[01][05][02]1%[06] is de… |
| Watch Your Step | — | 2 | all | all | …soned Air" "Truth And Fiction" "Watch Your Step" "Darkness" "Tra… |
| Working | — | 2 | all | all | …nder Pressure" "Bastard Sword" "Another Working Day" "All Mixed… |
| Wyndia Dif | — | 2 | all | all | ….5 Desert Dif.5 Desert Dif.1 Wyndia Dif.2 Ludia Dif.2 Astan… |
| Zee Empire | — | 2 | all | all | …A"Zere is nozing to[01]tell![02]Zee Empire asked zee[01]Princess… |
| Camera Turn Right Talk | — | 1 | all | all | …line got caught on the bottom! Camera Turn Right Talk/Confirm R… |
| Cancel Camera | — | 1 | all | all | …s. Change Rank SubScreen Action/Cancel Camera Turn Left START bu… |
| Cancel Directional | — | 1 | all | all | …down[02]~: Confirm [7F]: Cancel Directional buttons: Chan… |
| Cancel Quit | — | 1 | all | all | …down[02]~: Confirm [7F]: Cancel Quit fishing? Quit fishin… |
| Change Controller | — | 1 | all | all | …fishing. Change game settings. Change Controller settings. Adju… |
| Change Rank SubScreen Action | — | 1 | all | all | …eturned to default[01]settings. Change Rank SubScreen Action/Can… |
| Confirm Resolution Screen | — | 1 | all | all | …bottom! Camera Turn Right Talk/Confirm Resolution Screen adjust… |
| Depth Meter | — | 1 | all | all | …'s[01]current depth with the[01]Depth Meter. [0C][02]Some lures… |
| Devil Fish | — | 1 | all | all | …ng[01]fish. Also called the[01]"Devil Fish."[01]No one has yet[0… |
| En Jhou | — | 1 | all | all | …say?[02]If you mean the [05][02]En Jhou[06][01]ruins, they're to… |
| Exit For Beginners Easy | — | 1 | all | all | …ion[01][01]~: Confirm [7F]: Exit For Beginners Easy to use b… |
| Frogger Best | — | 1 | all | all | …]Has a cute pink[01]color. LV 3 Frogger Best frogger;[01]has an… |
| Frogger Lure | — | 1 | all | all | …getting[01]bottomdwellers. LV 1 Frogger Lure shaped like[01]a fr… |
| Frogger Sinks | — | 1 | all | all | …[01]sink even if[01]moved. LV 2 Frogger Sinks slowly but[01]rise… |
| Imperial Troops | — | 1 | all | all | …ow the horses and[01]whelks the Imperial Troops[01]ride into bat… |
| Learn How To Fish | — | 1 | all | all | …]Handle with care! [0C][02] Learn How To Fish[01] Sele… |
| Levant Uses | — | 1 | all | all | …d[01]only in deep[01]waters. S. Levant Uses its horns[01]to cut… |
| Ludian Kingdom | — | 1 | all | all | …s him![02]He's wanted by the[01]Ludian Kingdom![02]If we let him… |
| Manillo Shop | — | 1 | all | all | …ems,[02]or trade them at the[01]Manillo Shop for rare and[01]har… |
| Mighty Deis | — | 1 | all | all | …[01]us with time." [14][0B][0A]"Mighty Deis...[02]I see you have… |
| Minnow Floats | — | 1 | all | all | …mall fish; easy[01]to use. LV 2 Minnow Floats when[01]wound; sin… |
| Minnow Shaped | — | 1 | all | all | …churns up[01]the surface. LV 1 Minnow Shaped like a[01]small fi… |
| Minnow Sinks | — | 1 | all | all | …d; sinks if[01]left alone. LV 3 Minnow Sinks quickly;[01]rises s… |
| Mud Dragon | — | 1 | all | all | …re now able to draw[01]upon the Mud Dragon's[01]power![02]You le… |
| Ni Ryong | — | 1 | all | all | …f[01]to all [14][04][03]"I...am Ni Ryong.[02]From the bottom of[… |
| Power Bar | — | 1 | all | all | …02]Then, press the ~ button.[01]The Power Bar will begin[01]movi… |
| Salt Sea Fish | — | 1 | all | all | …01]it is the[01]ultimate catch. Salt Sea Fish mutated by[01]expo… |
| Salt Sea Swimes | — | 1 | all | all | …good[01]fish for[01]beginners. Salt Sea Swimes close to[01]the… |
| Shan River | — | 1 | all | all | …, they're to the east[01]of the Shan River." "You're going to go… |
| Shikk Region | — | 1 | all | all | …n the sandflier?[12][09][0C][94]Shikk Region[01]Shyde[01]Outside… |
| Spinner Lures | — | 1 | all | all | …emptation of[01]this lure. LV 1 Spinner Lures fish with[01]its s… |
| Spinner Sinks | — | 1 | all | all | …nks quickly[01]when wound. LV 2 Spinner Sinks fast and[01]floats… |
| Tak Tak | — | 1 | all | all | …you, my[01]little Tak? Here[01]Tak Tak!" [14][03][02]"Thank you… |
| Toggle Vibration | — | 1 | all | all | …all settings to default values? Toggle Vibration mode ON/OFF.[01… |
| Topper Attracts | — | 1 | all | all | …[01]shallow-water[01]fish. LV 3 Topper Attracts fish[01]with a p… |
| Topper Moves | — | 1 | all | all | …not sink even if[01]moved. LV 2 Topper Moves like a[01]shallow-w… |
| Winch Under Repairs | — | 1 | all | all | …1][0C][82]Yes[01]No [05][02]Winch Under Repairs[06][01] Caut… |
| Winder Heavy | — | 1 | all | all | …th its[01]floating motion. LV 3 Winder Heavy and sinks[01]fast.… |
| Winder Rarely | — | 1 | all | all | …humans as well[01]as fish. LV 1 Winder Rarely gets[01]caught, so… |
| Winder Well-balanced | — | 1 | all | all | …g after[01]bottomdwellers. LV 2 Winder Well-balanced;[01]attract… |
| Worm Lure | — | 1 | all | all | …deful look[01]on its face. LV 1 Worm Lure shaped like[01]a worm.… |
| Worm Rises | — | 1 | all | all | …[01]and is easy to[01]use. LV 3 Worm Rises slightly[01]when woun… |
| Yorae Shrine | — | 1 | all | all | …01]be getting to the[01][05][02]Yorae Shrine[06]." [14][8C]K"I d… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Rest | 82 | …u can rest here.[12][8B][0C][93]Rest[01]Diary[01]Never mind "You… |
| Diary | 75 | …st here.[12][8B][0C][93]Rest[01]Diary[01]Never mind "You hear al… |
| Yawn | 30 | …g[01]at all!" [0A][01]"squeak" "Yawn...[01]I want to eat--now!"… |
| Press | 22 | …ar it[01]is following us." [0C]!Press the ~ button rapidly[01]to… |
| Whew | 20 | …mes the mud!" [0C][06][14][8A]F"Whew...![01]We made it!" [0C][06… |
| Bwah | 19 | …2]You bet![01]Are you kidding? "Bwah ha ha ha ha ha![01]You'll g… |
| Arrrgggghh | 18 | ….[02][14]A [0C][05][14][0A][08]"Arrrgggghh!"[13]0[14][04][04]"My… |
| Anyway | 17 | …business." [0C][05][14][84][04]"Anyway, you want to[01]get to th… |
| Use | 16 | …d the[01]instructions?[12] [0C]!Use the directional buttons[01]t… |
| Interested | 14 | …ow when it'll[01]come in handy! Interested?"[12][82][0C][82]Yes[… |
| Trade | 14 | …"[12][84][0C][94]Buy[01]Sell[01]Trade[01]Never mind "We are a su… |
| Mugul | 13 | …re[02]from the Fifth Emperor[01]Mugul to the Eighth[01]Emperor M… |
| Shei | 13 | …re[02]from the Ninth Emperor[01]Shei to the Twelfth[01]Emperor A… |
| Humph | 12 | …take[01]you through the hex?[02]Humph! You don't know[01]it like… |
| Whirlpool | 12 | …eror Rampant" "Dragon's Blood" "Whirlpool" "Whirlpool" "Whirlpoo… |
| Buy | 11 | …e best weapons!"[12][84][0C][94]Buy[01]Sell[01]Trade[01]Never mi… |
| Sell | 11 | …weapons!"[12][84][0C][94]Buy[01]Sell[01]Trade[01]Never mind "We… |
| AMarlok | 10 | …Holy Strike Benediction [14][81]AMarlok[01]"...[0B]You again.[02… |
| Monsters | 10 | …oing in[01]a place like this?" "Monsters...Too many of[01]them..… |
| Stage | 10 | …want[01]to try?"[12][82][0C][15]Stage 1[01]Stage 2[01]Stage 3[01… |
| You'd | 9 | …4]"The lift's over[01]there![02]You'd better hurry[01]before the… |
| Purechi | 8 | …hen is that?" [0C][06][14][80]@"Purechi, suru ko![02]Taan, kalu.… |
| Sigh | 8 | …, y'know." [14][02][02][0A][06]"Sigh." "If'n you got nuthin'[01]… |
| Zis | 8 | …1]letting him go." [14][01][01]"Zis time, I 'ave you[01]do work… |
| Beware | 7 | …e color up to create[01]a path. Beware the [05][02]Red Eye[06]..… |
| Drat | 7 | …et[01]today." [0C][02][14][C2]@"Drat! It's too dark[01]to even s… |
| Line | 7 | …01]pressing the [7F] button.[02]Line three blocks of the[01]same… |
| Wha | 7 | …town..." [0C][06][14][81]A"[0D]Wha-[0E][0F] [0C][03][14][07][07… |
| Calm | 6 | ….[0B]I..." [0C][05][14][04][03]"Calm down![02]Get a hold of[01]y… |
| Figures | 6 | …w you[01]were a funny one...[02]Figures you'd take[01]this job!"… |
| Glom | 6 | …][02][02]"To get to [05][02]Mt. Glom[06],[01]you first have to[0… |
| Greed | 6 | …ks, I will[01]teach you [05][04]Greed[06].[02]If you want to be[… |
| If'n | 6 | …[01]shovel t'dig 'em[01]out.[02]If'n ya have a dog[01]that can s… |
| Insects | 6 | …01]there! They're like ants![01]Insects! Bwah ha ha ha ha!" "We… |
| Normal | 6 | …[01]to play in?"[12][82][0C][02]Normal[01]Random [0C]F"Are you s… |
| Show | 6 | …secrets,[01]eh?"[12][82][0C][92]Show treasure[01]Never mind [14]… |
| Tis | 6 | …hou[01]fight a god?" [14][83]C"'Tis as I thought...[02]It is not… |
| Twin | 6 | …the Grass Dragon." [14][04][04]"Twin gods? Yorae[01]Dragon?[02]I… |
| Yer | 6 | …ost you[01]50 zenny." [14][81]A"Yer shovel broke,[01]did it? Wel… |
| Zat | 6 | …like[01]me in other places?[02]Zat is because we[01]Manillo pla… |
| … | … | (+371 mais) |

## Ja cobertos pela KB (conferencia)
Abbess, Alliance, Astana, Cancel, Cancel Select, Carronade, Castle, Chamba, Chamba Spot, Chamba Spot Saldine Spot Ocean Spot, Chek, Chino, Confirm, Deis, Dodge Iggy, Dragon, Dragons, Earth, Eastern, Elina, Empire, Endless, Exit, Faeries, Fou, Fou Empire, Fou-lu, Golden Plains, Guards, Hesperia, Iggy, Imperial, Imperial Castle, Kecak, Koshka, Lake Spot, Levant, Ludian, Ludians, Lure Actions, Lures, Lyp, Majesty, Mami, Manillo, Marlok, Ocean Spot, Oracle, Pabpab, Pabpabs, Plains, Points, Power Level, Raise, Rasso, Recover, Red, Red Seal, Rhun, River Spot, Rods, Saldine Spot, Salt Sea, Sandflier, Scroll, Sea, Select, Shikk, Soniel, Synesta, Tarhn, Tomb, Wind, Wind Dragon, Wisdom, Woren, Worens, Wyndia, Wyndian, Wyndians, Yellow Seal, Yorae, Yorae Dragon, Yuna, Zhinga Mts
