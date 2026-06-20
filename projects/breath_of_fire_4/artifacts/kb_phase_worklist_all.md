# Fase 0 — capitulo all — worklist de cobertura de KB

> Gerado por `kb_phase.py` (deterministico). A IA descobriu candidatos de lore/nome que aparecem
> no capitulo e que a KB reconciliada (glossary + entities) NAO cobre. **Governanca:** pesquise
> + reconcilie cada item (skill 03 — IA+humano, por tier de fonte); se NAO for fornecer pesquisa
> p/ um item, registre o declinio explicito. Depois rode `kb_phase.py <projeto> all --check`.

- cenas do capitulo: all
- research_log reconciliado: NAO — bloqueia o avanco
- nao cobertos: **456 bloqueante(s)** (recorrem >=2 cenas) + 138 de baixa confianca | fracos (ruido): 690 | ja cobertos: 0

## Candidatos NAO cobertos — PESQUISAR (cobranca)
> `bloq` = recorre em >=2 cenas (alta confianca; BLOQUEIA o avanco da fronteira ate ser pesquisado/registrado). Os demais sao baixa confianca (citados 1x) — confira, nao bloqueiam.
| candidato | bloq | ocorr. | 1a cena | cenas | exemplo |
|---|---|---|---|---|---|
| Def | **SIM** | 984 | all | all | …gt[07][02] Ranged instant kill. Def[07][01] Wgt[07][02] Blessed… |
| Pwr | **SIM** | 810 | all | all | …7] Restores [07][03] HP to [07] Pwr[07][01] Wgt[07][02] Pwr[07][… |
| Restores | **SIM** | 390 | all | all | …1]the drums in the BGM. [05][03]Restores HP[06] [05][03]Restores… |
| Wis | **SIM** | 294 | all | all | …[01][16]%@User's Pwr, Def, Agl, Wis double;[01]Use: once/3 hours… |
| Select | **SIM** | 284 | all | all | …Help Key/PadSetting Up/Down:Select type[01]Enter:OK Esc… |
| Wind | **SIM** | 284 | all | all | …]Then, another person[01]uses a Wind spell.[02]Those two spells… |
| Status | **SIM** | 276 | all | all | …][01] Wgt[07][02] Resists Mind, Status[01]& Death attacks but we… |
| Confirm | **SIM** | 267 | all | all | …om! Dash Camera Turn Right Talk/Confirm ~ L R Resolution Mode Sc… |
| Kecak | **SIM** | 260 | all | all | …ometime, OK?" "You want to play Kecak[01]with us?"[12][82][0C][8… |
| Empire | **SIM** | 252 | all | all | …ehind the tavern." [14][0A][07]"The Empire could[01]come back at… |
| Agl | **SIM** | 240 | all | all | …ef=0.[01][16]%@User's Pwr, Def, Agl, Wis double;[01]Use: once/3… |
| Change | **SIM** | 224 | all | all | …Hints to help you fish better. Change game options. Stop fishin… |
| Mind | **SIM** | 218 | all | all | …eases wearer's resistance to[01]Mind attacks. Protects wearer ag… |
| ARaises Pwr | **SIM** | 210 | all | all | …ance to Mind/Status.[01][16][BF]ARaises Pwr/Def/Agl/Wis.[01][16]… |
| Ranged | **SIM** | 199 | all | all | …y kill. Pwr[07][01] Wgt[07][02] Ranged instant kill. Def[07][01]… |
| Earth | **SIM** | 187 | all | all | …[03]Water[06] Category: [05][03]Earth[06] Category: [05][03]Holy… |
| Melee | **SIM** | 180 | all | all | …Category: [05][03]Death/Melee[06] Critical hit--if it hi… |
| ARaises Dodge | **SIM** | 174 | all | all | …][BF]ARaises To-Hit.[01][16][BF]ARaises Dodge.[01][16][BF]ARaise… |
| Breath | **SIM** | 164 | all | all | …atch[01]Exit [0C][02]Fishing in Breath of Fire `[01]is done on a… |
| Hit | **SIM** | 162 | all | all | …07][02] +25% to wearer's[01]To-Hit. Def[07][01] Wgt[07][02]… |
| Elina | **SIM** | 159 | all | all | …[C2]@"Yeah...It's[01]also where Elina[01]disappeared." [0C][05][… |
| Try | **SIM** | 142 | all | all | …and[01]hard-to-find items.[11] Try matching the movement[01]of… |
| Exit | **SIM** | 133 | all | all | …adjust[01]~: Confirm [7F]: Exit [0C][8A][12][82][0C][82]Yes… |
| Use | **SIM** | 129 | all | all | …ange camera rotation direction. Use Up/Down and Right/Left butto… |
| Attack | **SIM** | 123 | all | all | …-rich food bar. +1 to[01]user's Attack. Contains many kinds of n… |
| Cancel | **SIM** | 108 | all | all | …ht/Left: Change option[01][80]: Cancel Up/Down: Select option[01… |
| Ludia | **SIM** | 103 | all | all | …[01]agile and hard[01]to catch. Ludia [05][03]Cures poison[06] P… |
| Lures | **SIM** | 96 | all | all | …matically replaced![11] [10][02]Lures have two qualities:[01]"ta… |
| River Spot | **SIM** | 96 | all | all | …irectional buttons: Change page River Spot 1 River Spot 1 River… |
| Extra | **SIM** | 90 | all | all | …7][01] Wgt[07][02] [01]Extra damage to Dragons. Pwr[07]… |
| Wyndia | **SIM** | 89 | all | all | …01]changes with its[01]habitat. Wyndia [05][03]Restores HP[06] N… |
| Yuna | **SIM** | 88 | all | all | …[01]building on the hill?" "Hm? Lord Yuna?[02]He was scheduled t… |
| Dragon | **SIM** | 85 | all | all | …s, like[01]worms?" [14][05][05]"Dragon?[02]Heh![0B] I ain't scar… |
| Lake Spot | **SIM** | 84 | all | all | …pot 3 Ocean Spot 1 Ocean Spot 3 Lake Spot 1 Lake Spot 1 Lake Spo… |
| Magic | **SIM** | 80 | all | all | …ack vs. [07][04] Lvl 1 [07][06] Magic vs [07] Lvl 2 [07][06] Mag… |
| Dodge | **SIM** | 78 | all | all | …rds.[01]Def[07][01] Wgt[07][02] Dodge+5%; vs. Wind Robe worn by… |
| Scroll | **SIM** | 74 | all | all | …2]Up/Down: Select lure[01][82]: Scroll page up[01][83]: Scroll p… |
| Demons | **SIM** | 72 | all | all | …anged attack[01]Extra damage to Demons. Pwr[07][01] Wgt[07][02]… |
| Endless | **SIM** | 72 | all | all | …ry mortals. Well! What is this? The Endless are fading away. It… |
| Faeries | **SIM** | 72 | all | all | …lly placed[01]in this category. Faeries assigned to[01]this job… |
| Hits | **SIM** | 72 | all | all | …02] [07][06] attack[01]+1 Hits. Straightbladed knife.[01][… |
| Ocean Spot | **SIM** | 72 | all | all | …pot 1 River Spot 2 River Spot 3 Ocean Spot 1 Ocean Spot 3 Lake S… |
| Power Level | **SIM** | 72 | all | all | …ut[01]line breaks[01]easily.[01]Power Level: 1 A bamboo rod Good… |
| Wisdom | **SIM** | 72 | all | all | …her brain[01]food. +1 to user's Wisdom. Food of the gods. Restor… |
| Defense | **SIM** | 66 | all | all | …ional[01]elements. +1 to user's Defense. Increases reaction time… |
| Move | **SIM** | 61 | all | all | …Reel in the lure [0C][02]Right: Move the lure to the[01] ri… |
| Salt Sea | **SIM** | 60 | all | all | …good[01]fish for[01]beginners. Salt Sea [05][03]Restores status… |
| Marlok | **SIM** | 58 | all | all | …rwell room. Check received from Marlok.[01]Needed to buy sandfli… |
| ARaises Hit | **SIM** | 54 | all | all | …critical hit chance.[01][16][BF]ARaises To-Hit.[01][16][BF]ARais… |
| Armor | **SIM** | 54 | all | all | …supple cloth armor.[01][16][16]@Armor made of linked chains.[01]… |
| Carronade | **SIM** | 54 | all | all | …e uses[01]something called a[01]Carronade to put a[02]hex on its… |
| Guard Focus Counter | **SIM** | 54 | all | all | …ures back.[01][16]6BPwr Up;Rear/Guard Focus Counter Up[01][16]%@… |
| Healing | **SIM** | 54 | all | all | …]attacks. Holy stone; increases Healing[01]magic to maximum leve… |
| Majesty | **SIM** | 54 | all | all | …as been worried[01]about you." "His Majesty the King, as[01]well… |
| Rod | **SIM** | 54 | all | all | …f used by horsemen.[01][16][12]@Rod with two balls chained to it… |
| Sword | **SIM** | 54 | all | all | …ten used by guards.[01][16][12]@Sword with a curved blade.[01][1… |
| Castle | **SIM** | 51 | all | all | …Do you want to return to[01]the Castle?[12] Do you want to retur… |
| Deis | **SIM** | 51 | all | all | …hink it[01]is."[02][14][09][07]"Says Deis." [0C][05][14]A [0C][0… |
| Desert | **SIM** | 51 | all | all | …1]Lives in schools[01]in lakes. Desert [05][03]Restores HP[06] O… |
| Zhinga Mts | **SIM** | 50 | all | all | …s.[01]Popular with[01]children. Zhinga Mts. [05][03]Restores AP[… |
| Tomb | **SIM** | 49 | all | all | …staff.[01][16][14]@Final key of Emperor's Tomb. Used[01]in the s… |
| Imperial | **SIM** | 48 | all | all | …01]about how there's[02]lots of Imperial[01]troops hanging aroun… |
| Rods | **SIM** | 48 | all | all | …or below[01]the target area. 1: Rods and Lures 1: Rods and Lures… |
| Sea | **SIM** | 47 | all | all | …ght...?" "You can't fish in the Sea[01]of Mud, but you can fish[… |
| Chino | **SIM** | 46 | all | all | …[01]you can!" [0C][04][14][84]D"Chino! You come back[01]here rig… |
| Mami | **SIM** | 46 | all | all | …shell.[01][16][16]@Handmade by Mami.[01][16][0D]@Strong armor..… |
| ARaises Wisdom | **SIM** | 42 | all | all | …[BF]ARaises Agility.[01][16][BF]ARaises Wisdom.[01][16][BF]ARais… |
| Recover | **SIM** | 42 | all | all | …1]nutrition. N. Islands [05][03]Recover from KO[06] Only found i… |
| Chamba | **SIM** | 40 | all | all | …ex energy.[01]Handle with care! Chamba ? ? ? ? ? ? ? ? ? ?… |
| Choose | **SIM** | 40 | all | all | …[01]No Equip a rod. Equip lure. Choose a rod to equip. Choose a… |
| Tower | **SIM** | 40 | all | all | …9][DF][04][06]. Needed to enter Tower of Wind. Needed to enter T… |
| View | **SIM** | 40 | all | all | …ions Exit Equip a rod and lure. View fish data. Learn how to fis… |
| Yorae Dragon | **SIM** | 40 | all | all | …2][02]"Hmmm...Gods, you[01]say? Yorae Dragon?[02]You're on your… |
| Woren | **SIM** | 39 | all | all | …he[01]previous leader of the[01]Woren in battle." "All my boy do… |
| Saldine | **SIM** | 38 | all | all | …ke it's flying[01]in the water. Saldine [05][03]Restores HP[06]… |
| Abbess | **SIM** | 36 | all | all | …gods." [14][01][01]"This is the Abbess'[01]home." [14][02][02]"W… |
| ARaises Agility | **SIM** | 36 | all | all | …[BF]ARaises Defense.[01][16][BF]ARaises Agility.[01][16][BF]ARai… |
| Heavy | **SIM** | 36 | all | all | …b with steel nails.[01][16][12]@Heavy, blunt weapon.[01][16][12]… |
| Large | **SIM** | 36 | all | all | …e warrior's weapon.[01][16][12]@Large, two-handed sword.[01][16]… |
| Powerful | **SIM** | 36 | all | all | …e.[01]Power Level: 2 Good range Powerful rod[01]with long range.… |
| Sink | **SIM** | 36 | all | all | …rs: Rise when wound[01]Winders: Sink quickly[02][05][03]Lures sh… |
| Tarhn | **SIM** | 36 | all | all | …ou still haven't talked[01]with Tarhn... [14]B [14][80]@"[04][02… |
| Ultimate | **SIM** | 36 | all | all | …good balance.[01]Power Level: 3 Ultimate rod Can be used to[01]c… |
| Culture | **SIM** | 35 | all | all | …rders[01]Types and Abilities[01]Culture and Work[01]Assigning Jo… |
| Plow | **SIM** | 35 | all | all | …e and Work[01]Assigning Jobs[01]Plow[01]Building Houses[01]Exit… |
| Red Seal | **SIM** | 35 | all | all | …Seal's[06][01][16][A6]A[05][02]Red Seal's[06][01][16][A6]ANorma… |
| Synesta | **SIM** | 35 | all | all | …ike they did with[01]Chamba and Synesta.[02]Just the thought of[… |
| Wind Dragon | **SIM** | 35 | all | all | …ucky, you might[01]even see the Wind Dragon[01]flying from here.… |
| Cancel Select | **SIM** | 34 | all | all | …item[01]~: Confirm [7F]: Cancel Select a rod to equip.[01… |
| Alliance | **SIM** | 33 | all | all | …r lands[01]controlled by the[02]Alliance whenever[01]they want,… |
| Army | **SIM** | 32 | all | all | …mind "You're not part of the[01]Army, are you? Can I help[01]you… |
| Levant | **SIM** | 32 | all | all | …tch one is a[01]distinction. S. Levant [05][03]Restores AP[06] A… |
| Wyndian | **SIM** | 32 | all | all | …ss.[01][16]^@Worn by an ancient Wyndian hero.[01]Def[07][01] Wgt… |
| Rhun | **SIM** | 31 | all | all | …[14]A "If you're looking for[01]General Rhun, he's this[01]way."… |
| ARaises Defense | **SIM** | 30 | all | all | …6][BF]ARaises Power.[01][16][BF]ARaises Defense.[01][16][BF]ARai… |
| Club | **SIM** | 30 | all | all | …3]@Large steel rod.[01][16][12]@Club with steel nails.[01][16][1… |
| Egg Magic | **SIM** | 30 | all | all | …om one enemy.[01][16][1C]@Lvl 1 Egg Magic. Deals damage[01]equal… |
| Final | **SIM** | 30 | all | all | …ate.Fighting staff.[01][16][14]@Final key of Emperor's Tomb. Use… |
| Heals | **SIM** | 30 | all | all | …1][16]+@Cures blindness in [07] Heals 6 people simultaneously.[0… |
| Trade | **SIM** | 30 | all | all | …can I 'elp you?"[12][85][0C][93]Trade for items[01]Cash in stamp… |
| Fish | **SIM** | 29 | all | all | …t Sea [05][03]Causes poison[06] Fish mutated by[01]exposure to[0… |
| Yellow Seal | **SIM** | 29 | all | all | …Seal's[06][01][16][A6]A[05][06]Yellow Seal's[06][01][16][A6]A[0… |
| Using Silverware | **SIM** | 28 | all | all | …ate!" There's a book titled[01]"Using Silverware." There's a boo… |
| Buy | **SIM** | 27 | all | all | …[01]some items?"[12][85][0C][93]Buy[01]Sell[01]Never mind [14][0… |
| Equip | **SIM** | 27 | all | all | …[0C][88][12][82][0C][82]Yes[01]No Equip a rod. Equip lure. Choo… |
| Return | **SIM** | 27 | all | all | …ings. Adjust screen resolution. Return all settings to their[01]… |
| Astana | **SIM** | 26 | all | all | …01]enemy towns! BOOM!" "This is Astana, where the[01]Carronade w… |
| Yorae | **SIM** | 26 | all | all | …ragon." [14][04][04]"Twin gods? Yorae[01]Dragon?[02]I don't know… |
| Hard | **SIM** | 25 | all | all | …06] Lives in shallow[01]waters. Hard to[01]catch as it is[01]ver… |
| Pabpab | **SIM** | 25 | all | all | …][14][86]E"Remember what the[01]Pabpab said?[02]Pukapuka...What… |
| Agility | **SIM** | 24 | all | all | …reaction time. +1 to[01]user's Agility. Contains Vitamin B and… |
| ARaises Power | **SIM** | 24 | all | all | …ct of healing magic.[01][16][BF]ARaises Power.[01][16][BF]ARaise… |
| Causeway | **SIM** | 24 | all | all | …rs[02]who guard the Imperial[01]Causeway.[02]Kyoin means 'people… |
| Close | **SIM** | 24 | all | all | …command[01]~: Confirm[01][7F]: Close screen Up/Down: Select opt… |
| Ear | **SIM** | 24 | all | all | …[01]swims. Anywhere [05][03]Fir+Ear attack[06] Bottomdweller[01]… |
| Fishing | **SIM** | 24 | all | all | …irm [7F]: Cancel [10][02]Fishing equipment can be[01]boug… |
| Handmade | **SIM** | 24 | all | all | ….[01]Power Level: MAX Super rod Handmade rod;[01]good balance.[0… |
| Iggy | **SIM** | 24 | all | all | …r names are Zig, Kryrik,[01]and Iggy. They're brothers,[01]and t… |
| Key | **SIM** | 24 | all | all | …ton Pause SELECT button Help Key/PadSetting Up/Down:S… |
| Land | **SIM** | 24 | all | all | …] "To build a house,[01]select "Land" from[01]the "Plow" menu.[0… |
| Normal | **SIM** | 24 | all | all | …]ANormal property. HP[07] Normal property. HP[07] Su… |
| Oracle | **SIM** | 24 | all | all | …e, you will find[01]the [05][02]Oracle of Wind[06],[02]a prieste… |
| Raises Defense | **SIM** | 24 | all | all | …maining HP Raises Power of [07] Raises Defense of [07] Raises Ag… |
| Simple | **SIM** | 24 | all | all | …ct as [05][02][09][07][04][06]. Simple dagger.[01][16]\@Branch w… |
| User | **SIM** | 24 | all | all | ….[01][16]6BUser becomes an egg. User is KOed; damage=remaining H… |
| Uses | **SIM** | 24 | all | all | …Levant [05][03]Restores HP[06] Uses its horns[01]to cut through… |
| Worm | **SIM** | 24 | all | all | …to catch[01]various fish. LV 2 Worm Good balance;[01]has a long… |
| Blue Seal | **SIM** | 23 | all | all | …all enemies' attention. [05][03]Blue Seal's[06][01][16][A6]A[05]… |
| Golden Plains | **SIM** | 23 | all | all | …"Um...[0B]Well...[02]Maybe..." "The Golden Plains is the[01]name… |
| Ludians | **SIM** | 23 | all | all | …"Don't worry--if we see any[01]Ludians, we'll take care of[01]t… |
| Sell | **SIM** | 23 | all | all | …e items?"[12][85][0C][93]Buy[01]Sell[01]Never mind [14][07][04]"… |
| Soniel | **SIM** | 23 | all | all | …rteenth and current[01]Emperor, Soniel. There are various kinds… |
| Types | **SIM** | 22 | all | all | …and Lures 1: Rods and Lures 2: Types of Lures 3: Terrain and Ra… |
| Add | **SIM** | 20 | all | all | …re are no faeries under "Plow." Add a fertilizer?[12][82][0C][82… |
| Hesperia | **SIM** | 20 | all | all | …nt of Levant to[01]western one, Hesperia.[02]But do you know wha… |
| Work | **SIM** | 20 | all | all | …es and Abilities[01]Culture and Work[01]Assigning Jobs[01]Plow[0… |
| Chedo | **SIM** | 19 | all | all | …oops[01]and make mine way[01]to Chedo...[02]And yet..." [14][06]… |
| Quit | **SIM** | 19 | all | all | …[7F]: Cancel Quit fishing? Quit fishing? Up/Down: Select co… |
| Attracts | **SIM** | 18 | all | all | …1]bottomdwellers. Ultimate lure Attracts any and[01]all kinds of… |
| Critical | **SIM** | 18 | all | all | …-tech Rocket Punch.[01][16][14]@Critical +20% if enemy HP at 25%… |
| Current Level | **SIM** | 18 | all | all | …attack; lowers enemy Status[01]Current Level: [05][04][07][08][… |
| Dragons | **SIM** | 18 | all | all | …2] [01]Extra damage to Dragons. Pwr[07][01] Wgt[07][02]… |
| Enter | **SIM** | 18 | all | all | …tting Up/Down:Select type[01]Enter:OK Esc:Cancel Dash Da… |
| High-grade Vitamin | **SIM** | 18 | all | all | …ious healing herbs.[01][16][0D]@High-grade Vitamin.[01][16][0D]@… |
| Item | **SIM** | 18 | all | all | …[01]for items at Manillo Shops. Item that can be traded with[01]… |
| KOs | **SIM** | 18 | all | all | …s damage[01]equal to user's HP; KOs user. Absorbs AP from one en… |
| Raises Agility | **SIM** | 18 | all | all | …of [07] Raises Defense of [07] Raises Agility of [07] Raises Wi… |
| Raises Power | **SIM** | 18 | all | all | …] Damage changes with remaining HP Raises Power of [07] Raises D… |
| Raises Wisdom | **SIM** | 18 | all | all | …of [07] Raises Agility of [07] Raises Wisdom of [07] Category:… |
| Retreats | **SIM** | 18 | all | all | …][16]6BDamage increased by # of Retreats.[01][16]6BCan be used t… |
| Shikk | **SIM** | 18 | all | all | …as that place north-[01]west of Shikk,[02]where it gets really[0… |
| Tak | **SIM** | 18 | all | all | …e while ago, his pet[01]chicken Tak ran off, and[01]ever since t… |
| Worent | **SIM** | 18 | all | all | …e you could get[01]one would be Worent." [0C][06][14][80]@"Did y… |
| Adjust | **SIM** | 17 | all | all | …gs. Change Controller settings. Adjust screen resolution. Return… |
| Auto | **SIM** | 17 | all | all | …FeedBack PAD only.) Manual=Run, Auto=Walk when dash[01]button is… |
| Cancel Camera | **SIM** | 17 | all | all | …s. Change Rank SubScreen Action/Cancel Camera Turn Left START bu… |
| Change Controller | **SIM** | 17 | all | all | …ereo Mono Change game settings. Change Controller settings. Adju… |
| Depth Meter | **SIM** | 17 | all | all | …'s[01]current depth with the[01]Depth Meter. [0C][02]Some lures… |
| Manual | **SIM** | 17 | all | all | ….[01](Force-FeedBack PAD only.) Manual=Run, Auto=Walk when dash[… |
| Pause | **SIM** | 17 | all | all | …mera Turn Left START button Pause SELECT button Help Key… |
| Slow Norm Fast Stereo Mono Change | **SIM** | 17 | all | all | …o Normal Reverse 0\| R 45\| L 45\| Slow Norm Fast Stereo Mono Chang… |
| Thirteenth | **SIM** | 17 | all | all | …e[02]during the reign of the[01]Thirteenth and current[01]Empero… |
| Toggle Vibration | **SIM** | 17 | all | all | …all settings to default values? Toggle Vibration mode ON/OFF.[01… |
| Charge | **SIM** | 16 | all | all | …ls![01][16][0C] [0C][02][05][04]Charge[06]: All characters in[01… |
| Esc | **SIM** | 16 | all | all | …Up/Down:Select type[01]Enter:OK Esc:Cancel Dash Dash Das… |
| Escape | **SIM** | 16 | all | all | …01]equipped weapons.[02][05][04]Escape[06]: All characters[01]re… |
| Faerie | **SIM** | 16 | all | all | …6BNon-elemental magical attack. Faerie attack (6+ faeries needed… |
| Insurance Contract | **SIM** | 16 | all | all | …from zenny earned. You got:[01]Insurance Contract 1! You got:[0… |
| Ludian | **SIM** | 16 | all | all | …gone anywhere!" "I've seen some Ludian[01]troops moving around h… |
| Poison | **SIM** | 16 | all | all | …tely protects wearer against[01]Poison and Poison attacks. Weare… |
| Poko | **SIM** | 16 | all | all | …he mainland?[02][14][81]ARight, Poko?" [14]A [14]C [14][02][02]"… |
| Pukapuka | **SIM** | 16 | all | all | …B]...[0B]..." [0C][03][14][C3]@"Pukapuka..." [0C][03][14][86]E"R… |
| Rhem | **SIM** | 16 | all | all | …response... [14][01][01]"I saw Rhem go by[01]earlier wearing he… |
| Slot | **SIM** | 16 | all | all | …reen No MEMORY CARD found in[01]Slot 1. A MEMORY CARD is[01]need… |
| Stop | **SIM** | 16 | all | all | …sh better. Change game options. Stop fishing. Options Buttons Sc… |
| Directional | **SIM** | 15 | all | all | …Select [7F]: View data on [07] Directional buttons: Change page… |
| Fou Empire | **SIM** | 15 | all | all | …This building belongs[01]to the Fou Empire.[02]And you are[01]Ea… |
| Gramps | **SIM** | 15 | all | all | …ere who's[01]ever been there is Gramps.[02]That's what everyone[… |
| Orders | **SIM** | 15 | all | all | …e to do?[01]Food and Hunting[01]Orders[01]Types and Abilities[01… |
| P'ung Ryong | **SIM** | 15 | all | all | …5][02]beneath the castle[06]." "P'ung Ryong, the Wind[01]Dragon,… |
| Points | **SIM** | 15 | all | all | …eases wearer's Concentration[01]Points by 50%. Doubles wearer's… |
| Reduces | **SIM** | 15 | all | all | …arer against[01]Status changes. Reduces wearer's AP costs by 25%… |
| Worens | **SIM** | 15 | all | all | …"This is Worent, home of[01]the Worens." "This is Worent, home o… |
| Grass Dragon | **SIM** | 14 | all | all | …01]dragon in the plains,[01]the Grass Dragon." [14][03][03]"Drag… |
| Insects | **SIM** | 14 | all | all | …Def as Pwr. Extra[01]damage to Insects. Category: [05][03]Melee… |
| Manillo | **SIM** | 14 | all | all | …t[01]to show me?[02]I am a busy Manillo,[01]but I can give you a… |
| Manillo Shop | **SIM** | 14 | all | all | …ems,[02]or trade them at the[01]Manillo Shop for rare and[01]har… |
| Ahtar | **SIM** | 13 | all | all | …peror[01]Shei to the Twelfth[01]Emperor Ahtar. This book details… |
| Assist | **SIM** | 13 | all | all | …batants.[01][16]"@Nullifies all Assist magic[01]effects. Nullifi… |
| Eighth | **SIM** | 13 | all | all | …e Fifth Emperor[01]Mugul to the Eighth[01]Emperor Mei. This book… |
| Fifth | **SIM** | 13 | all | all | …story of the Empire[02]from the Fifth Emperor[01]Mugul to the Ei… |
| Fourth | **SIM** | 13 | all | all | …First Emperor[01]Fou-lu to the Fourth[01]Emperor Temul. This bo… |
| Kyoin | **SIM** | 13 | all | all | …e of the[01]guards stationed at Kyoin.[02]I hope he gets rotated… |
| Lyp | **SIM** | 13 | all | all | …you'll need[01]to go to [05][02]Lyp[06]." [14][01][01]"The herbs… |
| Mei | **SIM** | 13 | all | all | …peror[01]Mugul to the Eighth[01]Emperor Mei. This book details t… |
| Ninth | **SIM** | 13 | all | all | …story of the Empire[02]from the Ninth Emperor[01]Shei to the Twe… |
| Plains | **SIM** | 13 | all | all | …orse?" "Headed to the Golden[01]Plains, are you?[02]Wait there j… |
| Resolution Mode Screen | **SIM** | 13 | all | all | …a Turn Right Talk/Confirm ~ L R Resolution Mode Screen adjust[01… |
| Switch | **SIM** | 13 | all | all | …4]E [0C][0B][14]E [0C][03][14]E Switch between groups[01]using t… |
| Temul | **SIM** | 13 | all | all | …eror[01]Fou-lu to the Fourth[01]Emperor Temul. This book details… |
| Twelfth | **SIM** | 13 | all | all | …he Ninth Emperor[01]Shei to the Twelfth[01]Emperor Ahtar. This b… |
| Broken Ludian King Sword | **SIM** | 12 | all | all | …raightbladed knife.[01][16][12]@Broken Ludian King's Sword.[01][… |
| Cancel Dash Dash Dash | **SIM** | 12 | all | all | …elect type[01]Enter:OK Esc:Cancel Dash Dash Dash The line g… |
| Cancel Directional | **SIM** | 12 | all | all | …down[02]~: Confirm [7F]: Cancel Directional buttons: Chan… |
| Cancel Quit | **SIM** | 12 | all | all | …down[02]~: Confirm [7F]: Cancel Quit fishing? Quit fishin… |
| Cancel Save | **SIM** | 12 | all | all | …ORY CARD[01]~: Confirm[01][7F]: Cancel Save/Load Up/Down: Select… |
| Cancels Assist | **SIM** | 12 | all | all | …namite[06]. Zhinga Mts. [05][03]Cancels Assist[06] Lives in shal… |
| Chamba Spot | **SIM** | 12 | all | all | …][02]TARGET FISH[06][01] Chamba Spot[02][07] [05]… |
| Chamba Spot Saldine Spot Ocean Spot | **SIM** | 12 | all | all | …Spot 1 Lake Spot 2 Lake Spot 3 Chamba Spot Saldine Spot Ocean S… |
| Change Rank SubScreen Action | **SIM** | 12 | all | all | …eturned to default[01]settings. Change Rank SubScreen Action/Can… |
| Checking | **SIM** | 12 | all | all | …[0C][88][12][82][0C][82]Yes[01]No Checking MEMORY CARD... Check… |
| Concentration | **SIM** | 12 | all | all | …osts by 25%. Increases wearer's Concentration[01]Points by 50%.… |
| Dash Camera Turn Right Talk | **SIM** | 12 | all | all | …line got caught on the bottom! Dash Camera Turn Right Talk/Conf… |
| Delete | **SIM** | 12 | all | all | …Confirm [7F]: Exit :Input :Delete :Next :Back :Start Do you… |
| Devil Fish | **SIM** | 12 | all | all | …enemies[06] Also called the[01]"Devil Fish."[01]No one has yet[0… |
| Equip Data Help Hints Options Exit Equip | **SIM** | 12 | all | all | …oose a rod and[01]lure to use. NO DATA Equip Data Help Hints Op… |
| Exit For Beginners Easy | **SIM** | 12 | all | all | …ion[01][01]~: Confirm [7F]: Exit For Beginners Easy to use b… |
| Fancy | **SIM** | 12 | all | all | …rd to handle.[01]Power Level: 2 Fancy rod Good balance,[01]easy… |
| Fir | **SIM** | 12 | all | all | …s it[01]swims. Anywhere [05][03]Fir+Ear attack[06] Bottomdweller… |
| Frogger Best | **SIM** | 12 | all | all | …]Has a cute pink[01]color. LV 3 Frogger Best frogger;[01]has an… |
| Frogger Lure | **SIM** | 12 | all | all | …getting[01]bottomdwellers. LV 1 Frogger Lure shaped like[01]a fr… |
| Frogger Sinks | **SIM** | 12 | all | all | …[01]sink even if[01]moved. LV 2 Frogger Sinks slowly but[01]rise… |
| Hints | **SIM** | 12 | all | all | …w fish data. Learn how to fish. Hints to help you fish better. C… |
| Hits Pwr | **SIM** | 12 | all | all | …r[07][01] Wgt[07][02] +1 Hits Pwr[07][01] Wgt[07][02]… |
| Hooking | **SIM** | 12 | all | all | …f Lures 3: Terrain and Range 4: Hooking 5: Uses of Fish 6: Lure… |
| Imperial Castle | **SIM** | 12 | all | all | …[80]@"Hey there! This is[01]the Imperial Castle![02]It's not a p… |
| Increases Atk | **SIM** | 12 | all | all | …otect[01]itself. Desert [05][03]Increases Atk[06] Beautiful to[0… |
| Increases Def | **SIM** | 12 | all | all | …of the[01]world. Desert [05][03]Increases Def[06] Shape and colo… |
| Instant | **SIM** | 12 | all | all | …7] Lvl 3 [07][06] Magic vs [07] Instant kill vs. [07] Instant ki… |
| KOed | **SIM** | 12 | all | all | …bduing attack.[01][16]6BUser is KOed; damage=remaining HP[01][16… |
| Learn How To Fish | **SIM** | 12 | all | all | …? ? ? ? ? ? ? [0C][02] Learn How To Fish[01] Sele… |
| Lifelike Lures | **SIM** | 12 | all | all | …now: Sink when wound[02][05][04]Lifelike Lures:[06][01]Froggers:… |
| Lure Actions | **SIM** | 12 | all | all | …e 4: Hooking 5: Uses of Fish 6: Lure Actions Where to find rods… |
| Medium | **SIM** | 12 | all | all | …g of [07] Light healing of [07] Medium healing of [07] Major hea… |
| Minnow | **SIM** | 12 | all | all | …[01]Toppers: Don't sink much[01]Minnow: Sink when wound[02][05][… |
| Minnow Floats | **SIM** | 12 | all | all | …mall fish; easy[01]to use. LV 2 Minnow Floats when[01]wound; sin… |
| Minnow Shaped | **SIM** | 12 | all | all | …churns up[01]the surface. LV 1 Minnow Shaped like a[01]small fi… |
| Minnow Sinks | **SIM** | 12 | all | all | …d; sinks if[01]left alone. LV 3 Minnow Sinks quickly;[01]rises s… |
| Options Buttons Screen Reset Vib Dash Camera Pad Text Sound Compass Manual Auto Normal Reverse | **SIM** | 12 | all | all | …nge game options. Stop fishing. Options Buttons Screen Reset Vib… |
| Power Bar | **SIM** | 12 | all | all | …Then, press the [7F] button.[01]The Power Bar will begin[01]movi… |
| Raise | **SIM** | 12 | all | all | …the[01] left [0C][02]Down: Raise your rod [0C][02]You can r… |
| Raises Dodge | **SIM** | 12 | all | all | …ring one. If 6 people wear one? Raises Dodge.[01][16][BF]ARaises… |
| Raises Pwr | **SIM** | 12 | all | all | …ring one. If 6 people wear one? Raises Pwr/Def/Agl/Wis.[01][16][… |
| Range | **SIM** | 12 | all | all | …: Types of Lures 3: Terrain and Range 4: Hooking 5: Uses of Fish… |
| Ranged Pwr | **SIM** | 12 | all | all | …attack Pwr[07][01] Wgt[07][02] Ranged Pwr[07][01] Wgt[07][02]… |
| Reel | **SIM** | 12 | all | all | …]follows: [0C][02][01]~ button: Reel in the lure [0C][02]Right:… |
| Resists Mind | **SIM** | 12 | all | all | …1][16]^@Def[07][01] Wgt[07][02] Resists Mind, Status[01]& Death… |
| Rise | **SIM** | 12 | all | all | …2]Shiny Lures:[06][01]Spinners: Rise when wound[01]Winders: Sink… |
| Robe | **SIM** | 12 | all | all | …ant cocktail dress.[01][16][16]@Robe worn by wind wizards.[01]De… |
| Saldine Spot | **SIM** | 12 | all | all | …5][02]TARGET FISH[06][01] Saldine Spot[02][07] [05… |
| Shiny Lures | **SIM** | 12 | all | all | …]changing your lure.[02][05][02]Shiny Lures:[06][01]Spinners: Ri… |
| Sinks | **SIM** | 12 | all | all | …ish with[01]its silver skin.[01]Sinks quickly[01]when wound. LV… |
| Spinner | **SIM** | 12 | all | all | …old skin[01]attracts fish. LV 3 Spinner Its shiny metal[01]surfa… |
| Spinner Lures | **SIM** | 12 | all | all | …emptation of[01]this lure. LV 1 Spinner Lures fish with[01]its s… |
| Spinner Sinks | **SIM** | 12 | all | all | …nks quickly[01]when wound. LV 2 Spinner Sinks fast and[01]floats… |
| Super | **SIM** | 12 | all | all | …ith long range.[01]Power Level: MAX Super rod Handmade rod;[01]g… |
| Tec | **SIM** | 12 | all | all | …you've caught one Try to get to Tec. 4! [0C][02]The distance you… |
| Terrain | **SIM** | 12 | all | all | …and Lures 2: Types of Lures 3: Terrain and Range 4: Hooking 5:… |
| Tips | **SIM** | 12 | all | all | …Finding the best places to fish Tips and tricks on hooking fish… |
| Topper | **SIM** | 12 | all | all | …a[01]rhythmic[01]movement. LV 1 Topper Makes a noise[01]when wou… |
| Topper Attracts | **SIM** | 12 | all | all | …[01]shallow-water[01]fish. LV 3 Topper Attracts fish[01]with a p… |
| Topper Moves | **SIM** | 12 | all | all | …not sink even if[01]moved. LV 2 Topper Moves like a[01]shallow-w… |
| User Pwr | **SIM** | 12 | all | all | …rts Def to Pwr; Def=0.[01][16]%@User's Pwr, Def, Agl, Wis double… |
| Wat | **SIM** | 12 | all | all | …[01]the effort. Saldine [05][03]Wat+Ear attack[06] A rare fish[0… |
| Winder Heavy | **SIM** | 12 | all | all | …th its[01]floating motion. LV 3 Winder Heavy and sinks[01]fast.… |
| Winder Rarely | **SIM** | 12 | all | all | …humans as well[01]as fish. LV 1 Winder Rarely gets[01]caught, so… |
| Winder Well-balanced | **SIM** | 12 | all | all | …g after[01]bottomdwellers. LV 2 Winder Well-balanced;[01]attract… |
| Worm Lure | **SIM** | 12 | all | all | …deful look[01]on its face. LV 1 Worm Lure shaped like[01]a worm.… |
| Worm Rises | **SIM** | 12 | all | all | …[01]and is easy to[01]use. LV 3 Worm Rises slightly[01]when woun… |
| Zig | **SIM** | 12 | all | all | …e other day?[02]Their names are Zig, Kryrik,[01]and Iggy. They'r… |
| Chek | **SIM** | 11 | all | all | …][02]"This village is[01]called Chek.[02]That means "Holy[01]Pla… |
| Free | **SIM** | 11 | all | all | …]how hard it works.[01]"[05][02]Free[06]" faeries don't[01]do mu… |
| Island | **SIM** | 11 | all | all | …that on the [05][02]Nameless[01]Island[06],[02]to the east of he… |
| Sarai | **SIM** | 11 | all | all | ….[01]This your first time[01]to Sarai?" [14][02][02]"munch munch… |
| Abilities | **SIM** | 10 | all | all | …Hunting[01]Orders[01]Types and Abilities[01]Culture and Work[01… |
| Activity Meter | **SIM** | 10 | all | all | …uses we[01]build?[02]That's the Activity Meter.[01]The longer th… |
| Assigning Jobs | **SIM** | 10 | all | all | …bilities[01]Culture and Work[01]Assigning Jobs[01]Plow[01]Buildi… |
| Building Houses | **SIM** | 10 | all | all | …rk[01]Assigning Jobs[01]Plow[01]Building Houses[01]Exit "What do… |
| Front Rank | **SIM** | 10 | all | all | …nd are placed[01]in the [05][03]Front Rank[06],[02]while those w… |
| Hunt | **SIM** | 10 | all | all | …]jobs we know how to[01]do are "Hunt" and[02]"Plow," but as[01]o… |
| Hunting | **SIM** | 10 | all | all | …at do I have to do?[01]Food and Hunting[01]Orders[01]Types and A… |
| Save | **SIM** | 10 | all | all | …Fire file. Unable to load file! SAVE SAVE Save to which MEMORY C… |
| Type | **SIM** | 10 | all | all | …good at[01]physical labor.[02]"Type" refers to[01]our personali… |
| Beyd | **SIM** | 9 | all | all | …myself! How rude![02]My name is Beyd, and[01]this is Sen, Shami,… |
| Combo Attack | **SIM** | 9 | all | all | …ey have a chance of[01]making a Combo Attack.[02]Characters in t… |
| Place | **SIM** | 9 | all | all | …ed Chek.[02]That means "Holy[01]Place" in the ancient[01]tongue.… |
| Play | **SIM** | 9 | all | all | …ew game art. Buy or sell aurum. Play various minigames. Buy batt… |
| Set | **SIM** | 9 | all | all | …ou, Majesty?" [0C][06][14][80]@"Set fire to the[01]trees.[02]We… |
| Skill Scroll | **SIM** | 9 | all | all | …in camp[01]to learn skills from Skill Scroll. [16][F1]ASpecially… |
| Standing | **SIM** | 9 | all | all | …Under Repairs[06][01] Caution: Standing on the[01] anchor will… |
| Evocation | **SIM** | 8 | all | all | …e secrets[02]of the Spell of[01]Evocation, the[02]knowledge of h… |
| Map | **SIM** | 8 | all | all | …01]SELECT button on the [05][04]World Map[06]. Raises resistance… |
| Mud | **SIM** | 8 | all | all | …You can't fish in the Sea[01]of Mud, but you can fish[01]here, y… |
| Pass | **SIM** | 8 | all | all | …][01][03]"Humans are called[01]"They Who Pass,"[02]because they… |
| Relax | **SIM** | 8 | all | all | …he[01]Elders, they're inside." "Relax...Take it easy...[02]We'll… |
| Silence | **SIM** | 8 | all | all | …going to..." [0C][06][14][80]@"Silence![02]This is no longer a[… |
| Spell | **SIM** | 8 | all | all | …preserved the secrets[02]of the Spell of[01]Evocation, the[02]kn… |
| West | **SIM** | 8 | all | all | …..." "Lot o' people from[01]the West who want to[02]sell things… |
| Working | **SIM** | 8 | all | all | …04]; To-Hit +20%, critical +5%. Working gloves.[01][16][14]@Pwr[… |
| Combo Attacks | **SIM** | 7 | all | all | …t combat[01]About "learning"[01]About Combo Attacks[01]Never min… |
| Confused | **SIM** | 7 | all | all | …mand against[01]enemy; works on Confused allies. Restores some H… |
| Dragon Crystal | **SIM** | 7 | all | all | …the [05][03][09][05][05][06][01]Dragon Crystal![02]You gained th… |
| Eastern | **SIM** | 7 | all | all | …ime you were on your[02]way, my Eastern[01]friends." [0C][06][14… |
| Excellent | **SIM** | 7 | all | all | …]grow, Lord Yuna." [14][02][02]"Excellent.[0B] I am[01]greatly p… |
| Kahn | **SIM** | 7 | all | all | …g to you!" [0C][02][14][05][05]"Kahn? [0C][01][14][86]C"That voi… |
| Magical | **SIM** | 7 | all | all | …burnt and blackened rice ball. Magical metal; can be used in ca… |
| Sandflier | **SIM** | 7 | all | all | …sk? Well, that's[01]a secret." "Sandflier parts?[02]Oh, yeah, I… |
| Shyde | **SIM** | 7 | all | all | …ant them all!" "This is [05][02]Shyde[06].[02]Since we're right… |
| Bell | **SIM** | 6 | all | all | …] Reduces all enemies' HP to 1. Bell used as a hair ornament. Ca… |
| Charon | **SIM** | 6 | all | all | …[06]. Said to have been used by Charon.[01][16]]@Can be used to… |
| Contains Vitamin | **SIM** | 6 | all | all | …time. +1 to[01]user's Agility. Contains Vitamin B and other bra… |
| Converts Def | **SIM** | 6 | all | all | …tegory: [05][03]ST Up/LV Up[06] Converts Def to Pwr; Def=0.[01][… |
| Danger | **SIM** | 6 | all | all | …mor Attack vs. [07] Enemy only! Danger! Lightweight, supple clot… |
| Def Instantly | **SIM** | 6 | all | all | …Damage changes w/ remaining HP&Def Instantly kills [07] Pwr[07]… |
| Desert Dif | **SIM** | 6 | all | all | …t, then, I won't[01]go!" Dif.5 Desert Dif.5 Desert Dif.5 Dese… |
| Ear Ear | **SIM** | 6 | all | all | …oly Fir+Win Fir+Win Win+Wat Wat+Ear Ear+Fir Restores [07][03] HP… |
| Fane | **SIM** | 6 | all | all | …d there leads[01]to the [05][02]Fane of the[01]Sea God[06]." [14… |
| Fir Restores | **SIM** | 6 | all | all | …Win Fir+Win Win+Wat Wat+Ear Ear+Fir Restores [07][03] HP to [07]… |
| Flexible | **SIM** | 6 | all | all | …gt[07][02] Can stun enemy Flexible, jointed staff.[01][16]… |
| Goo | **SIM** | 6 | all | all | …09]5[04][06]. Sword used by the Goo King.[01][16][12]@Pwr[07][01… |
| Greed | **SIM** | 6 | all | all | …ks, I will[01]teach you [05][04]Greed[06].[02]If you want to be[… |
| Health Retreat Dragon Hard | **SIM** | 6 | all | all | …this time![01]Premium: [07][07] None Health Retreat AP Dragon Ha… |
| Hi-tech Rocket Punch | **SIM** | 6 | all | all | …tack[01]Extra damage to Demons. Hi-tech Rocket Punch.[01][16][14… |
| Hits Critical | **SIM** | 6 | all | all | …r[07][01] Wgt[07][02] +1 Hits Critical +20% if enemy HP a… |
| Imperial Army | **SIM** | 6 | all | all | …?" "We are a supplier to the[01]Imperial Army! We carry[01]only… |
| Imperial Capital | **SIM** | 6 | all | all | …ou." [0C][81][05][08]Chedo, the Imperial Capital[06][13][90][0C]… |
| Improved Rocket Punch | **SIM** | 6 | all | all | …anged attack[01]Confuses enemy. Improved Rocket Punch.[01][16][1… |
| Kasq Woods | **SIM** | 6 | all | all | …cle of Wind has[01]lived in the Kasq Woods[02]for as long as any… |
| Kryrik | **SIM** | 6 | all | all | …er day?[02]Their names are Zig, Kryrik,[01]and Iggy. They're bro… |
| Lowers Agility | **SIM** | 6 | all | all | …of [07] Lowers Defense of [07] Lowers Agility of [07] Lowers Wi… |
| Lowers Defense | **SIM** | 6 | all | all | …Mutes [07] Lowers Power of [07] Lowers Defense of [07] Lowers Ag… |
| Lowers Power | **SIM** | 6 | all | all | …n [07] Confuses [07] Mutes [07] Lowers Power of [07] Lowers Defe… |
| Lowers Wisdom | **SIM** | 6 | all | all | …of [07] Lowers Agility of [07] Lowers Wisdom of [07] Raises Pow… |
| Lyta | **SIM** | 6 | all | all | …mmies or[01]daddies anymore.[02]Sister Lyta takes[01]care of us… |
| Manillo Shops | **SIM** | 6 | all | all | …t can be traded[01]for items at Manillo Shops. Item that can be… |
| Modo | **SIM** | 6 | all | all | …bly[01]won't be able to find[01]Modo so easy though![02]You prob… |
| Nameless | **SIM** | 6 | all | all | …ing[01]like that on the [05][02]Nameless[01]Island[06],[02]to th… |
| Plants | **SIM** | 6 | all | all | …Agl as Pwr. Extra[01]damage to Plants. Category: [05][03]Melee… |
| Raises Hit | **SIM** | 6 | all | all | …ring one. If 6 people wear one? Raises To-Hit.[01][16][BF]ARaise… |
| Ranged Def | **SIM** | 6 | all | all | …r[07][01] Wgt[07][02] [07][06] Ranged Def[07][01] Wgt[07][02] C… |
| Rear Rank | **SIM** | 6 | all | all | …mmand are[01]put in the [05][03]Rear Rank[06].[02]The [05][03]Fr… |
| Resists Earth | **SIM** | 6 | all | all | …. Def[07][01] Wgt[07][02] Resists Earth. Confuses [07] Red… |
| Resists Wind | **SIM** | 6 | all | all | …Def[07][01] Wgt[07][02] Resists Wind. Def[07][01] Wgt[07… |
| Sand Dragon | **SIM** | 6 | all | all | …gone out to see[01]the [05][02]Sand Dragon[06] then?"[12][03][0… |
| Southern | **SIM** | 6 | all | all | …][09]#[04][06]. Curved sword of Southern origin.[01][16][11]ALig… |
| Tarhn Shrine | **SIM** | 6 | all | all | …Tower of Wind. Needed to enter Tarhn's Shrine. Needed to activa… |
| Tree | **SIM** | 6 | all | all | …"Have you ever heard of the[01]Tree of Wisdom?"[12] "I came all… |
| Troops | **SIM** | 6 | all | all | …ble! Crops ready[01]to harvest! Troops' level[01]went up! New mi… |
| Wat Wat | **SIM** | 6 | all | all | …Earth Holy Fir+Win Fir+Win Win+Wat Wat+Ear Ear+Fir Restores [07… |
| Western | **SIM** | 6 | all | all | …...[02]If you go to the [05][02]Western[01]Plains[06], you can p… |
| Win Fir | **SIM** | 6 | all | all | …Fire Wind Water Earth Holy Fir+Win Fir+Win Win+Wat Wat+Ear Ear+… |
| Win Win | **SIM** | 6 | all | all | …nd Water Earth Holy Fir+Win Fir+Win Win+Wat Wat+Ear Ear+Fir Rest… |
| Wind Def | **SIM** | 6 | all | all | …][01] Wgt[07][02] Dodge+5%; vs. Wind Def[07][01] Wgt[07][02]… |
| Wind Robe | **SIM** | 6 | all | all | …][01] Wgt[07][02] Dodge+5%; vs. Wind Robe worn by wind wizards.[… |
| Wind Water Earth Holy Fir | **SIM** | 6 | all | all | …o Attacks[01]Never mind one all Fire Wind Water Earth Holy Fir+W… |
| Wyndians | **SIM** | 6 | all | all | …scared[01]living so high up?" "We Wyndians are not afraid[01]of… |
| Age Job Choose | **SIM** | 5 | all | all | …s job is currently unavailable. EN KN SL Age Job Choose a sort m… |
| Approval Rating | **SIM** | 5 | all | all | …ic?" "Did you know that your[01]Approval Rating won't go[02]down… |
| Bird Drops | **SIM** | 5 | all | all | …corchedRice[06],[01]and [05][02]Bird Drops[06] work really[01]go… |
| Birth Job | **SIM** | 5 | all | all | …! I'm tired of[01]all this work Death Birth Job From [07][01] Yo… |
| Cancel Dash Dash Dash Dash Camera Turn Right Talk | **SIM** | 5 | all | all | …elect type[01]Enter:OK Esc:Cancel Dash Dash Dash Dash Camer… |
| Catch | **SIM** | 5 | all | all | …off[01]to?" [14][05][05]"Zoom! Catch me if[01]you can!" [0C][04… |
| Destroy | **SIM** | 5 | all | all | …ommands. Change a faerie's job. Destroy a house. Set ratio of cr… |
| Difficulty | **SIM** | 5 | all | all | …want parts, your best[01]bet is Difficulty 2...[02]Do you have a… |
| Diligent Ordinary Lazy Odd | **SIM** | 5 | all | all | …destroy a house. Are you sure? Diligent Ordinary Lazy Odd This… |
| Elders | **SIM** | 5 | all | all | …t now...[01]You can talk to the Elders[01]instead, if you want."… |
| Endurance | **SIM** | 5 | all | all | …bilities, you know![02]They are Endurance[01](EN),[02]Knowledge… |
| Hard Normal Easy Relax Work | **SIM** | 5 | all | all | …l faeries what pace to work at. Hard Normal Easy Relax Work with… |
| Hesperia Zhinga Mts | **SIM** | 5 | all | all | …ert Paedra C. Hesperia Zhinga Mts.… |
| Islands Salt Sea Gold Plains | **SIM** | 5 | all | all | …a Zhinga Mts. N. Islands Salt Sea… |
| Items Items Items Arms Inn Search Troops Music Art Aurum Games Bonds Shop | **SIM** | 5 | all | all | …arn more about orders and work. Items Items Items Arms Inn Searc… |
| Items Shop Weapons Shop Inn Explorers Barracks Conservatory Museum Aurum Shop Arcade Insurance Shop | **SIM** | 5 | all | all | …give it[01]lots of fertilizer! Items Shop Weapons Shop Inn Expl… |
| Job | **SIM** | 5 | all | all | …the[01]Confirm button in the[01]Job window,[02]a menu pops up. F… |
| Jobs | **SIM** | 5 | all | all | …C][82]Yes[01]No [12][03][0C][94]Jobs and Orders[01]Look at Land[… |
| Material | **SIM** | 5 | all | all | …ot:[01][05][03][07] [05][02]1st Material[06] [05][02]1st Materia… |
| Odd | **SIM** | 5 | all | all | …ier everyone is,[01]you know." "Odd faeries aren't born[01]very… |
| Orders Help Adjust | **SIM** | 5 | all | all | …Faerie determines its own pace. Orders Help Adjust a faerie's wo… |
| Pabpabs | **SIM** | 5 | all | all | …om[01]over there.[02]One of the Pabpabs[01]was crouched over[01]… |
| Plow Hunt Farm Free Cut | **SIM** | 5 | all | all | …battle insurance. Select a job: Plow Hunt Farm Free Cut down tre… |
| Rand Chai Fumi Yuka Vizy Poff Sila Meyl Biky Apa Phly Hyat Chik Cyrl Oban Choi Pema Chmo Beco Yohn Ramo Parz Ludy Poke Kayo Wabu Rass Boko Yuhi Sasa Lany Aili Jika Yuma Feyl Kora Sena Rahn Sino Mamu Kupi Kiil Dita Bole Pahn Naeg Guti Maki Ginz Nyan Kari | **SIM** | 5 | all | all | …Empty plots can't be selected. Rand Chai Fumi Yuka Vizy Poff Si… |
| Rotation System | **SIM** | 5 | all | all | …01][16][0C] [0C][02]The [05][02]Rotation System[06] allows[01]yo… |
| Rotten Meat | **SIM** | 5 | all | all | …01]work really well.[02][05][02]Rotten Meat[06], [05][02]Scorche… |
| Select All Info Help Switch Destroy Place Land Select | **SIM** | 5 | all | all | …der construction. Select a job. Select All Info Help Switch Dest… |
| Shop | **SIM** | 5 | all | all | …nds Shop selling various items. Shop selling various weapons. Pl… |
| Style | **SIM** | 5 | all | all | …(EN),[02]Knowledge (KN),[02]and Style (SL).[02]Each one of us is… |
| Super Combo | **SIM** | 5 | all | all | …you're going to use[01][05][03]Super Combo[06], it's best if[01… |
| Tree Lake None Add | **SIM** | 5 | all | all | …rsed area." St. St. St. St. Sq. Tree Lake None Add another kind… |
| Yorae Shrine | **SIM** | 5 | all | all | …01]be getting to the[01][05][02]Yorae Shrine[06]." [14][8C]K"I d… |
| Art | **SIM** | 4 | all | all | …4][05][04]"Haaaaaa!!" [14][C6]@"Art thou finished?" [0C][05][14]… |
| Broken Sword | **SIM** | 4 | all | all | …sociations 3-Missing Princess 4-The Broken Sword 5-The Wind Drag… |
| Bunyan | **SIM** | 4 | all | all | …Then w...I am in[01]your debt...Bunyan,[01]yes?" [0C][04][14]F [… |
| Buy Buy Buy Buy Sell Trade Quit Purchase | **SIM** | 4 | all | all | …ou found:[01]Item: [05][03][07] Buy Buy Buy Buy Sell Trade Quit… |
| Capital | **SIM** | 4 | all | all | …e [05][02]Sonne Village[06].[01]Capital? Oh, that be far[01]off… |
| Chedo Dreamland South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert South Desert Ludia Region Wyndia Region Highlands Shikk Region Astan Region North Desert Paedra | **SIM** | 4 | all | all | …fl Castle, 1 fl Chedo Dreamland… |
| Diet Hard | **SIM** | 4 | all | all | …ren." There's a book titled[01]"Diet Hard 3." "Looking for my wi… |
| Dif | **SIM** | 4 | all | all | …ll right, then, I won't[01]go!" Dif.5 Desert Dif.5 Desert Dif.… |
| Dreams | **SIM** | 4 | all | all | …here, in the[01][05][05]Land of Dreams[06]!" [14][80]B"But then,… |
| Exit Change Rank SubScreen Action | **SIM** | 4 | all | all | …ion[01][01]~: Confirm [7F]: Exit Change Rank SubScreen Actio… |
| Fish Head Beach | **SIM** | 4 | all | all | …4][09][9D][04][09][9E][04] Fish Head Beach [09]i[04][09]p[0… |
| Fou | **SIM** | 4 | all | all | …he Thirteenth[01]Emperor of the Fou[01]Empire,[02]His Majesty[01… |
| Goete | **SIM** | 4 | all | all | …l right, I'll[01]tell you where Goete[01]is.[02]I saw him go off… |
| Guard | **SIM** | 4 | all | all | …01]change equipment.[02][05][04]Guard[06]: Reduces damage and[01… |
| Hesperia Options Buttons Screen Default Vib Dash Camera Pad Message Sound Compass Manual Auto Normal Reverse | **SIM** | 4 | all | all | …a Gold Plains S. Hesperia Options Buttons Scr… |
| Ice Ring | **SIM** | 4 | all | all | …ike." 4,000 6,000 9,500 Ring of Ice Ring of Ice Ring of Ice Span… |
| Imperial Causeway | **SIM** | 4 | all | all | …the entrance to[01]the [05][02]Imperial Causeway[06],[02]which… |
| Items | **SIM** | 4 | all | all | …r the[01][80] button to cancel. Items cannot be used to[01]make… |
| Journey End | **SIM** | 4 | all | all | …10-Levant 11-The Path Ahead 12-Journey's End 13-Of Gods and Men… |
| Konoko | **SIM** | 4 | all | all | …![01]OK, I'll tell you[01]where Konoko is.[02]From here, walk 6[… |
| Load Directional | **SIM** | 4 | all | all | …~: Confirm[01][7F]: Cancel Save/Load Directional button: Move[01… |
| Mighty Deis | **SIM** | 4 | all | all | …[01]us with time." [14][0B][0A]"Mighty Deis...[02]I see you have… |
| Path Ahead | **SIM** | 4 | all | all | …gs 9-Fools and Men 10-Levant 11-The Path Ahead 12-Journey's End… |
| Purchase | **SIM** | 4 | all | all | …ell Trade Quit Purchase an item Purchase weapons, armor, and oth… |
| Purifiers | **SIM** | 4 | all | all | …come back are[02]a group of[01]Purifiers.[02]They go from town[… |
| Quit Kecak | **SIM** | 4 | all | all | …]Try for a prize[01]Practice[01]Quit Kecak "Which lesson do you… |
| Rasso | **SIM** | 4 | all | all | …4]@"What are you doing[01]here, Captain Rasso?" [0C][04][14][C4]… |
| Resolution Resolution Mode Screen | **SIM** | 4 | all | all | …a Turn Right Talk/Confirm ~ L R Resolution Resolution Mode Scree… |
| Rhoppe | **SIM** | 4 | all | all | …." [0C][05][14][04][04]"[05][02]Rhoppe[06]'s got the key[01]to t… |
| Rock Dragon | **SIM** | 4 | all | all | …re now able to draw[01]upon the Rock Dragon's[01]power![02]You l… |
| Rudd | **SIM** | 4 | all | all | …ll[01]tell you where to[01]find Rudd.[02]He said he'd hide[01]un… |
| Sa Ryong | **SIM** | 4 | all | all | …]E[04][06]! [14][01][01]"I...am Sa Ryong.[02]I watcheth o'er thi… |
| Sarai Chamba Astana Base Kyria Mountain Hut Synesta Kyoin Astana Ludia Shyde Worent Wyndia Chek Sonne Faerie Village Checkpoint Shikk Lyp Saldine Island Koshka Chiqua Pauk Castle | **SIM** | 4 | all | all | …itle screen.[12][8C][0C]BYes[01]No Anywhere Anywh… |
| Spd | **SIM** | 4 | all | all | …d SW Wind W Wind NW Wind Spd 1 Spd 2 Spd 3 Spd 4 Spd 5 Looks li… |
| Spray Spray Clip Oracle Egghead | **SIM** | 4 | all | all | …k, he[01]was gone!" 25 30 40 50 Spray Spray Clip Oracle Egghead… |
| Su Ryong | **SIM** | 4 | all | all | …]H[04][06]! [14][03][03]"I...am Su Ryong.[02]I watcheth o'er thi… |
| Table Manners | **SIM** | 4 | all | all | …are." There's a book titled[01]"Table Manners for[01]Children."… |
| Tree Dragon | **SIM** | 4 | all | all | …re now able to draw[01]upon the Tree Dragon's[01]power![02]You l… |
| Ability | **SIM** | 3 | all | all | …ople in the[01]back rank regain Ability[01]Points[02]based on th… |
| Cancel Move | **SIM** | 3 | all | all | …st down.[01]~: Confirm [7F]: Cancel Move the cursor using the… |
| Character Commands | **SIM** | 3 | all | all | …[05][02]Rotation System[06][01]Character Commands[01][05][04]Ch… |
| Checkpoint | **SIM** | 3 | all | all | …the pub." "I heard that the[01]Checkpoint's been closed[02]and… |
| Combo | **SIM** | 3 | all | all | …][05][02]magic[06] can create a Combo.)[02][05][04]Use Item[06]:… |
| Continent | **SIM** | 3 | all | all | …][14]B [14][82]B"The Western[01]Continent, eh?[02]Well, we can't… |
| Dodge Iggy | **SIM** | 3 | all | all | …you want to!" [14]A [14]A [0C]!Dodge Iggy's attacks by[01]press… |
| Don | **SIM** | 3 | all | all | …0]@"Ryong..." [0C][06][14][80]@"Don' let what th'[01]landlord sa… |
| Entering Commands | **SIM** | 3 | all | all | …e[06] and [05][04]Escape[06][01]Entering Commands[01]Close Help… |
| Grass | **SIM** | 3 | all | all | …priestess of[02]Ch'o Ryong, the Grass[01]Dragon." "Welcome back.… |
| Imperial Troops | **SIM** | 3 | all | all | …ow the horses and[01]whelks the Imperial Troops[01]ride into bat… |
| Koshka | **SIM** | 3 | all | all | …you should ask the[01]folks in Koshka.[02]They're the ones that… |
| Kwanso | **SIM** | 3 | all | all | …]through the gate at[01][05][02]Kwanso[06]...[02]You might not b… |
| Kyria | **SIM** | 3 | all | all | …em..." "I mean, the mayor[01]of Kyria is in[01]here...[02]But he… |
| Mayor | **SIM** | 3 | all | all | …hout Permission[01] of the Mayor is[01] Prohibited![… |
| Megaphone Megaphone SpiritBlast Cleave Disembowel | **SIM** | 3 | all | all | …][01] and [04][04]! 30 40 50 70 Megaphone Megaphone SpiritBlast… |
| Mud Dragon | **SIM** | 3 | all | all | …like the Wind Dragon[01]and the Mud Dragon?[02]They were all[01]… |
| Peso | **SIM** | 3 | all | all | …en, Shami,[01]Rinpo, Poske, and Peso.[02]They wanted to see[01]y… |
| Pilfer Pilfer Pilfer Super Combo Blitz | **SIM** | 3 | all | all | …r to[02][19] 1,500 3,000 10,000 Pilfer Pilfer Pilfer Super Combo… |
| Poske | **SIM** | 3 | all | all | …1]this is Sen, Shami,[01]Rinpo, Poske, and Peso.[02]They wanted… |
| Remove | **SIM** | 3 | all | all | …items; ignores special effects. Remove equipment from a characte… |
| Ryong | **SIM** | 3 | all | all | …elationship." [0C][06][14][80]@"Ryong..." [0C][06][14][80]@"Don'… |
| Sen | **SIM** | 3 | all | all | …My name is Beyd, and[01]this is Sen, Shami,[01]Rinpo, Poske, and… |
| Shami | **SIM** | 3 | all | all | …me is Beyd, and[01]this is Sen, Shami,[01]Rinpo, Poske, and Peso… |
| Shikk Region | **SIM** | 3 | all | all | …dflier?[12][02][0C][93]Kyoin[01]Shikk Region[01]Never mind "I se… |
| Sonne Village | **SIM** | 3 | all | all | …t' ask.[02]This here be [05][02]Sonne Village[06].[01]Capital? O… |
| Special | **SIM** | 3 | all | all | …ck with a[01]weapon.[02][05][04]Special[06]: Attack using magic[… |
| Tak Tak | **SIM** | 3 | all | all | …you, my[01]little Tak? Here[01]Tak Tak!" [14][03][02]"Thank you… |
| Use Item | **SIM** | 3 | all | all | …can create a Combo.)[02][05][04]Use Item[06]: Use an item or[01]… |
| Wind Wind | **SIM** | 3 | all | all | …ou[01]don't go back there... N Wind NE Wind E Wind SE Wind S… |
| Ability Points | — | 2 | all | all | …annot be attacked, and [01]heal Ability Points (AP)[02]based on… |
| Astan Dif | — | 2 | all | all | …f.1 Wyndia Dif.2 Ludia Dif.2 Astan Dif.5 Zhinga Mts. Dif.1… |
| Attacks | — | 2 | all | all | …its[01][05][03]Weakness[06].[02]Attacks can be classified[01]int… |
| Bah | — | 2 | all | all | …hinking is not[01] required...' Bah!" [0C][05][14]B [0C][06][14]… |
| Bastard Sword | — | 2 | all | all | …nd And Round" "Under Pressure" "Bastard Sword" "Another Working… |
| Beginnings | — | 2 | all | all | …in" "Slow Tension" "Endings and Beginnings" "Trouble Ahead" "Eph… |
| Believing | — | 2 | all | all | …f The Plains" "Thousand Winds" "Seeing Is Believing" "A Distant… |
| Bridge | — | 2 | all | all | …]lots of monsters inside[01]the Bridge." [14][02][02]"Hail, trav… |
| Buy Sell Stop Buy | — | 2 | all | all | …[09]# "You don't have any [09]# Buy Sell Stop Buy [09]# Sell [09… |
| Cancel Diligent Ordinary Lazy Odd St | — | 2 | all | all | …r[01][7F]: Confirm [80]: Cancel Diligent Ordinary Lazy Od… |
| Catch Chino | — | 2 | all | all | …ne can[01]catch me!" [0C]! Help Catch Chino[02]You can catc… |
| Chiqua Village | — | 2 | all | all | …Arcade Insurance Shop "This is Chiqua Village.[01]It's not big… |
| Combos | — | 2 | all | all | …Items cannot be used to[01]make Combos, but they can[01]be used… |
| Concentration Points | — | 2 | all | all | …s (AP)[02]based on their CP[01](Concentration Points).[02](Howev… |
| Copper Bell ElectrumBell PlatinumBell Charm Charm Charm Monopolize Roulette | — | 2 | all | all | …ny[01]bodyguards right[01]now." Copper Bell ElectrumBell Platinu… |
| Curse | — | 2 | all | all | …"Prayer" "Unwavering Courage" "The Curse" "Turismo" "Replay" "S… |
| Desert City | — | 2 | all | all | …2]some people call this the[01]'Desert City'." "We get a lot of… |
| Desert Town | — | 2 | all | all | …Money And Run" "Battling Gods" "Desert Town" "Round And Round" "… |
| Distant Land | — | 2 | all | all | …Winds" "Seeing Is Believing" "A Distant Land" "Hills And Streams… |
| Divine Danger | — | 2 | all | all | …, Pukapuka" "For The Princess" "Divine Danger" "Emperor Rampant"… |
| Dragon Blood | — | 2 | all | all | …vine Danger" "Emperor Rampant" "Dragon's Blood" "Whirlpool" "Whi… |
| Dream | — | 2 | all | all | …here" "Floating" "The Endless" "After The Dream" "I've been stud… |
| Dress Shoes Multivitamin | — | 2 | all | all | …0 zenny Midas Stone 1,000 zenny Dress Shoes Multivitamin [0C]D"H… |
| Eastern Highway | — | 2 | all | all | …ut[02]of town on the[01][05][02]Eastern Highway[06]." "There's b… |
| En Jhou | — | 2 | all | all | …say?[02]If you mean the [05][02]En Jhou[06][01]ruins, they're to… |
| Free Fall | — | 2 | all | all | …ve Heart" "Requiem" "Shepards" "Free Fall" "Neverending Rain" "T… |
| Gold Plains Dif | — | 2 | all | all | …Astan Dif.5 Zhinga Mts. Dif.1 Gold Plains Dif.5 Highlands Dif… |
| Health Retreat Dragon Recover | — | 2 | all | all | …cating my[01]next work to you!" None None None None None Health… |
| Hesperia Dif | — | 2 | all | all | …ains Dif.5 Highlands Dif.3 S. Hesperia Dif.2 Shikk Dif.4 Sal… |
| Hex | — | 2 | all | all | …1]used." [0C]D[14][C1]@"[05][02]Hex[06]?" [14][02][02]"You've he… |
| Highlands Dif | — | 2 | all | all | …Mts. Dif.1 Gold Plains Dif.5 Highlands Dif.3 S. Hesperia Dif… |
| Highway | — | 2 | all | all | …2]Try looking on the[01][05][02]Highway[06] outside[01]town." [0… |
| Hills And Streams | — | 2 | all | all | …Is Believing" "A Distant Land" "Hills And Streams" "The Sun And… |
| Ice Spanner Master Rod | — | 2 | all | all | …Ring of Ice Ring of Ice Ring of Ice Spanner Master's Rod "I saw… |
| Islands Dif | — | 2 | all | all | …Shikk Dif.4 Salt Sea Dif.4 N. Islands Dif.3 Paedra Dif.3 C.… |
| Jhou | — | 2 | all | all | …02]I bet if I went to the En[01]Jhou ruins I could find[01]somet… |
| June | — | 2 | all | all | …d of hay;[01]A swarm of bees in June[01]Is worth a silver spoon;… |
| List | — | 2 | all | all | …Menu : Map : Search : Speed+ : List : Back : Cast : Help : Row… |
| Ludia Dif | — | 2 | all | all | ….5 Desert Dif.1 Wyndia Dif.2 Ludia Dif.2 Astan Dif.5 Zhinga… |
| Ludian Kingdom | — | 2 | all | all | …s him![02]He's wanted by the[01]Ludian Kingdom![02]If we let him… |
| Mage Goo | — | 2 | all | all | …][98][04][06] from[01]a [05][03]Mage Goo[06]! "There are many di… |
| Main Menu | — | 2 | all | all | …A [0C]C[14]A [0C]C[14]A Quit to Main Menu : F9[01][01]Cancel : O… |
| Marcy | — | 2 | all | all | …4][04]"That's how Chino[01]gets Sister Marcy[02]and other people… |
| Midas Stone | — | 2 | all | all | …st you!" Soul Ring 10,000 zenny Midas Stone 1,000 zenny Dress Sh… |
| Minigame Instructions | — | 2 | all | all | …ns again?[12][02][0C][82]Yes[01]No Minigame Instructions[14][… |
| Mixed | — | 2 | all | all | …d Sword" "Another Working Day" "All Mixed Up" "Poisoned Air" "Tr… |
| Money | — | 2 | all | all | …"The First Emperor" "Fighters" "Take The Money And Run" "Battlin… |
| Nahma | — | 2 | all | all | …...[02]If you're looking[01]for Nahma, she told[01]me she was go… |
| Neverending Rain | — | 2 | all | all | …equiem" "Shepards" "Free Fall" "Neverending Rain" "Tree Spirits"… |
| Ni Ryong | — | 2 | all | all | …f[01]to all [14][04][03]"I...am Ni Ryong.[02]From the bottom of[… |
| Numbers | — | 2 | all | all | …8! "Starlight Run" "Walkabout" "By The Numbers" "Bringing Home A… |
| Paedra Dif | — | 2 | all | all | …alt Sea Dif.4 N. Islands Dif.3 Paedra Dif.3 C. Hesperia "I alm… |
| Poisoned Air | — | 2 | all | all | …er Working Day" "All Mixed Up" "Poisoned Air" "Truth And Fiction… |
| Pressure | — | 2 | all | all | …Desert Town" "Round And Round" "Under Pressure" "Bastard Sword"… |
| Rampant | — | 2 | all | all | …The Princess" "Divine Danger" "Emperor Rampant" "Dragon's Blood… |
| Retreat | — | 2 | all | all | …rned. Recover and automatically Retreat.[01][05][02]2%[06] is de… |
| Ring | — | 2 | all | all | …you'd like." 4,000 6,000 9,500 Ring of Ice Ring of Ice Ring of… |
| Round And Round | — | 2 | all | all | …"Battling Gods" "Desert Town" "Round And Round" "Under Pressure… |
| Sailing The Seven Seas | — | 2 | all | all | …"Turismo" "Replay" "Seagulls" "Sailing The Seven Seas" "Pabupab… |
| Salt Sea Dif | — | 2 | all | all | …S. Hesperia Dif.2 Shikk Dif.4 Salt Sea Dif.4 N. Islands Dif.3… |
| Sandflier Valley | — | 2 | all | all | …[01]we'll go to this[02][05][02]Sandflier Valley[06],[01]and get… |
| Sausage Beer Steak Wine | — | 2 | all | all | …[02]Happy[06] [05][03]Drink[06] Sausage Beer Steak Wine --[81] -… |
| Shan River | — | 2 | all | all | …, they're to the east[01]of the Shan River." "You're going to go… |
| Shikk Dif | — | 2 | all | all | …lands Dif.3 S. Hesperia Dif.2 Shikk Dif.4 Salt Sea Dif.4 N. I… |
| Slow Tension | — | 2 | all | all | …Numbers" "Bringing Home A Win" "Slow Tension" "Endings and Begin… |
| Sluice Control Panel | — | 2 | all | all | …so bad after all... [05][02]Sluice Control Panel[06][01]… |
| Song Of The Plains | — | 2 | all | all | …verending Rain" "Tree Spirits" "Song Of The Plains" "Thousand Wi… |
| Sort | — | 2 | all | all | …aracter's special[01]abilities. Sort a character's special[01]ab… |
| Soul Ring | — | 2 | all | all | …seemed to[01]work against you!" Soul Ring 10,000 zenny Midas Sto… |
| Sound Of Money | — | 2 | all | all | …raveling Merchant" "Macho Man" "The Sound Of Money" "Brave Heart… |
| South | — | 2 | all | all | …01]you one more time,[01]OK?[02]South 6, west 16,[01]north 1, we… |
| Sun And The Moon | — | 2 | all | all | …tant Land" "Hills And Streams" "The Sun And The Moon" "1-2-3 1-2… |
| Supplication Supplication Holy Strike Resist Benediction | — | 2 | all | all | …le[01]short there." 20 25 30 35 Supplication Supplication Holy S… |
| Thief | — | 2 | all | all | …ns?[12] [0C]![01] Catch the Thief![02]To catch the thief, ge… |
| Thousand Winds | — | 2 | all | all | …Spirits" "Song Of The Plains" "Thousand Winds" "Seeing Is Belie… |
| Traveling Merchant | — | 2 | all | all | …" "Watch Your Step" "Darkness" "Traveling Merchant" "Macho Man"… |
| Tree Lake | — | 2 | all | all | …igent Ordinary Lazy Odd St. Sq. Tree Lake None "We play rock-pap… |
| Tree Spirits | — | 2 | all | all | …"Free Fall" "Neverending Rain" "Tree Spirits" "Song Of The Plain… |
| Trouble Ahead | — | 2 | all | all | …sion" "Endings and Beginnings" "Trouble Ahead" "Ephemeral" "The… |
| Truth And Fiction | — | 2 | all | all | …"All Mixed Up" "Poisoned Air" "Truth And Fiction" "Watch Your S… |
| Una | — | 2 | all | all | …][01][14][86]C"That voice...[01]Master Una![02]Forgive me,[01]Ma… |
| Unwavering Courage | — | 2 | all | all | …"Faeries" "Game Over" "Prayer" "Unwavering Courage" "The Curse"… |
| Valley | — | 2 | all | all | …ey[01]call [05][02]Sandflier[01]Valley[06] near here.[02]It's a… |
| Vitamin | — | 2 | all | all | …etreat AP Dragon Recover with a Vitamin.[01][05][02]1%[06] is de… |
| Watch Your Step | — | 2 | all | all | …soned Air" "Truth And Fiction" "Watch Your Step" "Darkness" "Tra… |
| Western Continent | — | 2 | all | all | …ds." "You want to get to the[01]Western Continent?[02]Hmmm...I'v… |
| Win | — | 2 | all | all | …y The Numbers" "Bringing Home A Win" "Slow Tension" "Endings and… |
| Wyndia Dif | — | 2 | all | all | ….5 Desert Dif.5 Desert Dif.1 Wyndia Dif.2 Ludia Dif.2 Astan… |
| Zee Empire | — | 2 | all | all | …A"Zere is nozing to[01]tell![02]Zee Empire asked zee[01]Princess… |
| Anchor Free Free Free Free Free Free Free Free Free Free Free Free Free Free Free Hunt Plow Farm Item Arms Inn Search Troops Music Art Aurum Games Bonds South Desert South Desert South Desert Ludia Region Wyndia Region Highlands Shikk Region Astan Region North Desert Paedra | — | 1 | all | all | …w : Sail : DropSail : Explore : Anchor Free Free Free Free Free… |
| Area Is Trapped | — | 1 | all | all | …[05][02]Caution![06][01] This Area Is Trapped[11] "You bo… |
| Cancel Choose | — | 1 | all | all | …st down.[01]~: Confirm [7F]: Cancel Choose a character using[… |
| Cancel Nothing Pool Pool | — | 1 | all | all | …buttons.[02]~: Confirm [7F]: Cancel Nothing Pool Pool Are you… |
| Cancel Switch | — | 1 | all | all | …button.[01]~: Confirm [7F]: Cancel Switch characters using t… |
| Cancel Use | — | 1 | all | all | …buttons.[02]~: Confirm [7F]: Cancel Use the directional butto… |
| Castle Ludia | — | 1 | all | all | …"I heard you all snuck into[01]Castle Ludia...[02]Didn't anybod… |
| Ch'o Ryong | — | 1 | all | all | …01]she's also a priestess of[02]Ch'o Ryong, the Grass[01]Dragon.… |
| Chamba Hideout Mt | — | 1 | all | all | …y Kyoin Astana Aqueduct Kurok N.Chamba Hideout Mt. Yogy Ludia Wy… |
| Chamba Kurok Dam Kyria Woods Synesta Wharf Causeway Kyoin Ludia Plains Wychwood Worent Mt | — | 1 | all | all | …ash Cliff Sarai Valley Chamba N.Chamba Kurok Dam Kyria Woods Syn… |
| Change Rank Change Rank Change Rank SubScreen Action | — | 1 | all | all | …he rear if [05][06]Confused[06] Change Rank Change Rank Change R… |
| Charge Attack Guard Critical Hit Lucky Strike Instant Kill Counter Escape | — | 1 | all | all | …t treasure[01]Close Help window Charge Attack Guard Critical Hit… |
| Confirm Esc | — | 1 | all | all | …Up/Down:Select type[01]Enter:Confirm Esc:Cancel Dash Das… |
| Elemental Change | — | 1 | all | all | …ou killed him! How could you!?" Elemental Change You need the dr… |
| Entry Without Permission | — | 1 | all | all | …The Pet[11] [10][02] Entry Without Permission[01]… |
| Equip Best Pool Pwr Def Agl Wis Equip | — | 1 | all | all | …1]directional buttons. Use [07] Equip Best Pool Pwr Def Agl Wis… |
| Fish Head Beach Fish Head Beach Fish Head Beach | — | 1 | all | all | …sh Head Beach [09][9E][04] Fish Head Beach Fish Head… |
| FishSpot Crash Cliff Sarai Valley Chamba | — | 1 | all | all | …'t be[01]entered. ? ? ? ? ? ? ? FishSpot Crash Cliff Sarai Valle… |
| Free To Play | — | 1 | all | all | …ayor's Residence[11] [10][02] Feel Free To Play With[01]… |
| Giga Fane Hideout Astana Astana Astana Astana Astana Aqueduct Castle Koshka En Jhou Shan Rvr Chiqua River Pauk Tomb Mukto Kwanso Highway Sonne Sanctum Soma Chedo Hut WestGate WestGate Mt | — | 1 | all | all | …yde Chkpoint Shikk Mt. Ryft Mt. Giga Fane Hideout Astana Astana… |
| Giga Plains | — | 1 | all | all | …onne Sanctum Soma Chedo Hut Mt. Giga Plains one all Fire Wind Wa… |
| Glom Shrine Ahm Fen Kasq Wds Wyndia Pung'tap Ice Peak Chek Sinchon Shyde Chkpoint Shikk Mt | — | 1 | all | all | …udia Plains Wychwood Worent Mt. Glom Shrine Ahm Fen Kasq Wds Wyn… |
| Glom Shrine Kasq Wds Castle Wyndia Ahm Fen Pung'tap Ice Peak Chek Sinchon Mt | — | 1 | all | all | …Ludia Wychwood Worent Fane Mt. Glom Shrine Kasq Wds Castle Wynd… |
| Health Retreat Dragon Slash Ranged Magic Dragon | — | 1 | all | all | …] [09][0A][05]:[07] No contract AP Health Retreat Dragon Slash R… |
| Hesperia Crash Crash Crash Cliff Sarai Valley Chamba Dam Kyria Woods Synesta FishSpot | — | 1 | all | all | …Islands Salt Sea Gold Plains S. Hesperia Crash Crash Crash Cliff… |
| Item Special Equip Status Change Setting Save Use | — | 1 | all | all | …[0C][8A][12][82][0C][82]Yes[01]No Item Special Equip Status Cha… |
| Judging Wind Direction | — | 1 | all | all | …2][01][0C][15]Wind Direction[01]Judging Wind Direction[01]Suppli… |
| Key Exit | — | 1 | all | all | …Main Menu : F9[01][01]Cancel : Other Key Exit Game : F9[01][01]… |
| Key Quit | — | 1 | all | all | …Main Menu : F9[01][01]Cancel : Other Key Quit to Main Menu : F9… |
| Manly Clothes | — | 1 | all | all | …[03][06] shattered! The [05][02]Manly Clothes[06] were destroyed… |
| Manual Normal Battle Fish Type MagicWepn Power MagicArmr Defense Accessory Armor Fishing Healing Combat Melee Melee Hex View | — | 1 | all | all | …eturned to default[01]settings. Manual Normal Battle Fish Type M… |
| Mayor Residence | — | 1 | all | all | …[05][03][09]! [10][02] [01] Mayor's Residence[11] [10][02]… |
| Move The Ship | — | 1 | all | all | …nued without incident. [0C]" How To Move The Ship[12][01][0C]… |
| Options Buttons Screen Reset Vib Dash Camera Pad Text Sound Manual Auto Normal Reverse | — | 1 | all | all | …sure you want to equip[01][07] Options Buttons Screen Reset Vib… |
| Pwr Def Agl Wis | — | 1 | all | all | …[05][01]NOTHING[06] Pwr Def Agl Wis _ [05][01]Nothin… |
| Rwolf Momo Kryrik Abbess Njomo Gyosil Stoll Una Bunyan Lyta Khan Marlok Haste Drowse Finale Reck Pique Ward Filch Wild Vision Guard Valor Greed Normal Battle Set | — | 1 | all | all | …[7F]: Cancel [05][01]Free[06] Rwolf Momo Kryrik Abbess Njomo G… |
| Ryft Mt | — | 1 | all | all | …inchon Shyde Chkpoint Shikk Mt. Ryft Mt. Giga Fane Hideout Astan… |
| Ryft Shyde Chkpoint Shikk Lyp Cove Jungle Pabpab Saldine Koshka En Jhou Shan Rvr Chiqua River Pauk Tomb Mukto Kwanso Highway Sonne Sanctum Soma Chedo Hut Mt | — | 1 | all | all | …g'tap Ice Peak Chek Sinchon Mt. Ryft Shyde Chkpoint Shikk Lyp Co… |
| Super God Grand Royal Mach End Fast Mega Flash Cancel Great Final Small Medium Large Reverse Galactic Atomic Excellent Giant Attack Drive Magnum Break Zzzzt | — | 1 | all | all | …en erased! Miss! HI EX RAD X Super God Grand Royal Mach End F… |
| Use Combo Attacks | — | 1 | all | all | …mbo Attack on[01]it first turn! Use Combo Attacks to knock[01]yo… |
| Use Equip | — | 1 | all | all | …e enemy caught you by surprise! Use Equip [12][81][0C][93]Findin… |
| Use Sort Drop Key Select | — | 1 | all | all | …ap[06] only) [05][01]EMPTY[06] Use Sort Drop Key Select and use… |
| Wharf Causeway Kyoin Astana Aqueduct Kurok | — | 1 | all | all | …Kyria Woods Synesta FishSpot ? Wharf Causeway Kyoin Astana Aque… |
| Winch Under Repairs | — | 1 | all | all | …1][0C][82]Yes[01]No [05][02]Winch Under Repairs[06][01] Caut… |
| Wind Direction | — | 1 | all | all | …To Move The Ship[12][01][0C][15]Wind Direction[01]Judging Wind D… |
| Wind Water Earth Holy Mind Stat | — | 1 | all | all | …f Agl Wis _ [05][01]Nothing[06] Fire Wind Water Earth Holy Mind… |
| Wind Wind Spd | — | 1 | all | all | …Wind SE Wind S Wind SW Wind W Wind NW Wind Spd 1 Spd 2 Spd 3 S… |
| Yogy Ludia Wychwood Worent Fane Mt | — | 1 | all | all | …duct Kurok N.Chamba Hideout Mt. Yogy Ludia Wychwood Worent Fane… |
| Yogy Lyp Lyp Lyp Lyp Lyp Lyp Lyp Cove Jungle Pabpab Saldine | — | 1 | all | all | …Chedo Hut WestGate WestGate Mt. Yogy Lyp Lyp Lyp Lyp Lyp Lyp Lyp… |

## Candidatos FRACOS (capitalizacao de inicio de frase — provavel ruido, conferir)
| candidato | ocorr. | exemplo |
|---|---|---|
| Wgt | 1176 | …[07][03] HP to [07] Pwr[07][01] Wgt[07][02] Pwr[07][01] Wgt[07][… |
| ARaises | 570 | …nce to Mind attacks.[01][16][BF]ARaises resistance to Status att… |
| Category | 450 | …Ranged Def[07][01] Wgt[07][02] Category: [05][03]Fire[06] Categ… |
| BEvolved | 294 | …. Basic dragon form.[01][16][09]BEvolved dragon form.[01][16][0A… |
| BBasic | 252 | …Evolved dragon form.[01][16][0A]BBasic dragon form.[01][16][09]B… |
| Protects | 240 | …Ludia [05][03]Cures poison[06] Protects itself[01]with very sha… |
| Press | 223 | …01]find a fishing spot. [0C][02]Press the [7F] button near the[0… |
| Cures | 174 | …hard[01]to catch. Ludia [05][03]Cures poison[06] Protects itself… |
| Increases | 132 | …elements. +1 to user's Defense. Increases reaction time. +1 to[0… |
| Rest | 125 | …u can rest here.[12][8B][0C][93]Rest[01]Diary[01]Never mind "You… |
| Diary | 121 | …st here.[12][8B][0C][93]Rest[01]Diary[01]Never mind "You hear al… |
| ATypical | 120 | …To-Hit, other stats.[01][16][BF]ATypical shield; usable by anyon… |
| Strong | 120 | …6][16]@Def[07][01] Wgt[07][02] Strong vs. Fire and[01]Earth; we… |
| Resists | 114 | …. Def[07][01] Wgt[07][02] Resists breath[01]attacks. Resis… |
| Lvl | 102 | …] [07][06] attack vs. [07][04] Lvl 1 [07][06] Magic vs [07] Lvl… |
| Raises | 102 | …on. Def[07][01] Wgt[07][02] Raises chance of[01]encountering… |
| BAttack | 96 | …ake 2 attacks in a row.[01][16]6BAttack 1-3 times (random).[01][… |
| BMake | 84 | …chance of finding item.[01][16]:BMake 2 attacks in a row.[01][16… |
| BRestores | 84 | …mutant dragon form.[01][16][0F]BRestores [07] Evolved dragon fo… |
| Deals | 78 | …res all[01]dragons' HP to full. Deals minor Wind damage to [07]… |
| Needed | 72 | …. Non-elemental magical attack. Needed to enter sluice control[0… |
| Contains | 66 | …favorite of boars.[01][16][0D]@Contains magical energy.[01][16]… |
| Basic | 60 | …udian King's Sword.[01][16][12]@Basic sword; often used by guard… |
| Poisons | 60 | …[07] Blinds [07] Confuses [07] Poisons [07] Mutes [07] Cures po… |
| Steel | 60 | …e of linked chains.[01][16][16]@Steel breastplate.[01][16][16]@M… |
| ACan | 54 | …balls chained to it.[01][16][11]ACan smash bones through armor.[… |
| Allows | 54 | …with sharp thorns.[01][16][14]@Allows [04][01] to fire energy b… |
| Damage | 54 | …06] Category: [05][03]Death[06] Damage changes with remaining HP… |
| Rear | 54 | …6BInjures back.[01][16]6BPwr Up;Rear/Guard Focus Counter Up[01][… |
| Shiny | 54 | …tection, but heavy.[01][16][16]@Shiny plate armor with high Def.… |
| Causes | 48 | …ltimate catch. Salt Sea [05][03]Causes poison[06] Fish mutated b… |
| Non-elemental | 48 | …ent Level: [05][04][07][08][06] Non-elemental. Category: [05]… |
| Offers | 48 | …bound with straps.[01][16][16]@Offers full protection, but heav… |
| Pick | 48 | …nding[01]on the rod you use.[02]Pick your rod carefully and[01]c… |
| Premium | 48 | …[07] You get another chance![01]Premium: [07][07] Get up--you ca… |
| Holy | 47 | …[03]Earth[06] Category: [05][03]Holy[06] Category: [05][03]Death… |
| APwr | 42 | …, lightweight sword.[01][16][11]APwr[07][01] Wgt[07][02]… |
| Auto-counter | 42 | …attacks for one turn.[01][16]%@Auto-counter vs attacks for 1 tu… |
| Evolved | 42 | …form.[01][16][0F]BRestores [07] Evolved dragon form.[01][16][0A]… |
| Helmet | 42 | …m-fitting leggings.[01][16][16]@Helmet made from blended steel.[… |
| … | … | (+650 mais) |

## Ja cobertos pela KB (conferencia)
_(nenhum)_
