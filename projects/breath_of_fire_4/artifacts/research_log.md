# Research Log — Breath of Fire IV PT-BR

status: reconciled

---

## cap.all — pesquisa global (corpus flat)

> Seção única para o modelo flat-CSV. Todas as entidades marcadas `(cap.all)` em
> `entities.csv` e `glossary.csv` têm suas fontes declaradas abaixo.

### Fontes utilizadas

| Tier | Fonte | Cobertura | Origem |
|------|-------|-----------|--------|
| T1 | Wikipedia PT — https://pt.wikipedia.org/wiki/Breath_of_Fire_IV | Personagens, locais, facções, lore geral | Humano |
| T2 | Corpus `artifacts/dialogs.csv` (22987 strings, extração direta do binário) | Frequências, definições in-game, grafias oficiais | IA |
| T2 | Conhecimento de treinamento — BoF4 (PC/PS1, Capcom 2000) | Lore, personagens, estrutura narrativa | IA |

**Reconciliação humana:** usuário forneceu Wikipedia PT como fonte principal (2026-06-20).
Novos termos confirmados pela Wikipedia: **Aliança do Leste** (Eastern Alliance), **Synesta** (cidade onde Elina desapareceu), **Sandflier** (veículos que navegam no oceano de areia), **Império Fou** (grafia PT confirmada).

---

### Entidades e fontes por categoria

#### Personagens — grupo principal
- **Ryu**: protagonista amnésico, metade do deus Yorae (luz); control code [04][01]; pode transformar em dragões. Fonte: training-knowledge-T2 + corpus (control code analysis).
- **Fou-lu**: imperador, metade do deus Yorae (sombra); acordou de 600 anos; grafia "Fou-lu" confirmada in-corpus via item desc. Fonte: training-knowledge-T2 + corpus (53x "Fou").
- **Nina**: princesa de Wyndia, asas; procura Elina. Fonte: training-knowledge-T2.
- **Cray**: guerreiro Woren, procura Elina (noiva). Fonte: training-knowledge-T2.
- **Scias**: mercenário Grassrunner, fala com gagueira. Fonte: training-knowledge-T2.
- **Ursula**: capitã imperial, junta-se ao grupo. Fonte: training-knowledge-T2.
- **Ershin**: armadura com Deis aprisionada, fala em 3ª pessoa. Fonte: training-knowledge-T2.

#### Personagens — NPCs e antagonistas
- **Elina**: irmã de Nina, desaparecida; confirmada 159x no corpus ("also where Elina disappeared"). Fonte: corpus.
- **Yuna**: "Lord Yuna", antagonista científico imperial; 88x no corpus. Fonte: corpus + training-knowledge-T2.
- **Deis**: deusa serpente; 55x no corpus ("Says Deis"). Fonte: corpus.
- **Marlok**: mercador NPC; corpus: "I am Marlok" (auto-apresentação direta). Fonte: corpus.
- **Rasso**: "Captain Rasso"; 4x no corpus. Fonte: corpus.
- **Abbess**: líder religiosa; 37x no corpus ("the Abbess' home"). Fonte: corpus.
- **Chino**: criança NPC; 48x ("Zoom! Catch me if you can!"). Fonte: corpus.

#### Locais
- **Wyndia**: reino dos Wyndians; 143x no corpus. Fonte: corpus + training-knowledge-T2.
- **Astana**: corpus define "This is Astana, where the Carronade was built." Fonte: corpus.
- **Shikk**: 34x no corpus (lista de locais). Fonte: corpus.
- **Lyp**: 25x no corpus. Fonte: corpus.
- **Worent**: aldeia Woren; 24x. Fonte: corpus.
- **Chek**: corpus define "Chek. That means Holy Place". Fonte: corpus (definição direta).
- **Pung'tap**: corpus define "Pung'tap, which means The Tower of Wind". Fonte: corpus (definição direta).
- **Zhinga Mts**: 55x no corpus. Fonte: corpus.
- **Koshka**: 9x (lista de locais). Fonte: corpus.

#### Facção
- **Fou Empire**: "The Empire"; 269x no corpus. Fonte: corpus + training-knowledge-T2.

#### Conceitos/Lore
- **Endless**: corpus define "The Endless are fading away. It would seem the gods are dead." 72x. Fonte: corpus.
- **Yorae Dragon**: corpus: "Gods, you say? Yorae Dragon?" e "Resistance is futile. Hand over the Yorae Dragon." 71x. Fonte: corpus.
- **Kecak**: corpus: "You want to play Kecak with us?" 264x — jogo de dados. Fonte: corpus.
- **Carronade**: corpus: "something called a Carronade to put a hex on its enemies." 54x. Fonte: corpus.

#### Criaturas/Povos
- **Faeries**: 72x no corpus (mecânica de vila). Fonte: corpus.
- **Manillo**: corpus: "Manillo Shop for rare and hard-to-find items." 34x. Fonte: corpus.
- **Woren**: povo-tigre; corpus confirma "Worent" (aldeia). 78x. Fonte: corpus + training-knowledge-T2.
- **Wyndian**: corpus: "ancient Wyndian hero". 41x. Fonte: corpus.

#### Stats e UI (glossary)
- **Pwr/Def/Agl/Wis/Wgt**: abreviações de stat confirmadas in-corpus (ex: "User's Pwr, Def, Agl, Wis double"). Propostas: For./Def./Agi./Sab./Pes. Fonte: corpus + convenção JRPG PT-BR (training-T2).
- **HP** (Hit Points): pontos de vida; manter "HP". Fonte: corpus.
- **AP** (Action Points): pontos de ação/magia; manter "AP". Fonte: corpus.
- **Hit** (taxa de acerto): traduzir "Acerto". Fonte: corpus.
- **Dodge** (esquiva): traduzir "Esquiva". Fonte: corpus.
- **Princess**: título de Nina ("Princess [04][XX]"). Traduzir "Princesa". Fonte: corpus.
- **Hex**: corpus: "exposure to hex energy", "to put a hex on its enemies". 159x. Fonte: corpus.
- Restores, Select, Confirm, Cancel, Exit, Scroll, Save: UI padrão; traduzir conforme PT-BR standard. Fonte: corpus (frequência alta).

#### Facções (novo — fonte T1 Wikipedia)
- **Aliança do Leste** (Eastern Alliance): facção oposta ao Império Fou, no continente oriental. Wikipedia PT: "Aliança do Leste". Fonte: Wikipedia-T1 (humano).

#### Locais adicionais (fonte T1 Wikipedia + corpus)
- **Synesta**: cidade onde Elina desapareceu. Wikipedia PT confirma. 35x no corpus. Fonte: Wikipedia-T1 + corpus.
- **Chamba**: aldeia/local. 40x no corpus. Fonte: corpus.
- **Saldine**: localidade. 38x no corpus. Fonte: corpus.
- **Sandflier**: veículo que navega no oceano de areia entre os continentes. Wikipedia PT: "barcos que navegam pela areia". Fonte: Wikipedia-T1 (humano).
- **Wind Dragon**: o Dragão do Vento — divindade/guardião referenciada pela tribo Fae/Wyndian. 35x no corpus. Fonte: corpus + training-T2.

#### Mecânicas de combate e magia (corpus)
- **Wind, Earth, Mind**: elementos/tipos de ataque mágico. "Wind spell", "Earth [category]", "Mind attacks". Fonte: corpus.
- **Ranged, Melee**: tipos de dano físico ("Ranged instant kill", "Death/Melee"). Fonte: corpus.
- **Attack, Healing, Recover**: termos de sistema de batalha. Fonte: corpus.
- **ARaises Pwr, ARaises Dodge, ARaises Hit, ARaises Defense, ARaises Wisdom, ARaises Agility, Guard Focus Counter**: strings de efeito de habilidade geradas por control codes ([BF] + "Raises" + stat). São mechanic shorthand do sistema de batalha. Fonte: corpus.

#### Itens e pesca (corpus)
- **Lures, Rod, Rods**: equipamentos de pesca. Fonte: corpus.
- **River Spot, Lake Spot, Ocean Spot, Salt Sea**: locais/categorias de pesca. Fonte: corpus.
- **Armor, Sword**: categorias de equipamento. Fonte: corpus.
- **Red Seal, Yellow Seal, Blue Seal**: selos/modificadores de item. Fonte: corpus.

#### Personagens/NPCs adicionais (corpus)
- **Mami, Tarhn, Iggy, Levant, Rhun, Soniel, Synesta**: NPCs mencionados no corpus. Fonte: corpus.
- **Oracle**: título de personagem religioso. Fonte: corpus.
- **Majesty**: tratamento real ("His Majesty the King"). Fonte: corpus.
- **Ahtar**: NPC do corpus de diálogo. Fonte: corpus.
- **Mei**: NPC do corpus de diálogo. Fonte: corpus.

#### Locais adicionais (corpus)
- **Ludia**: região/localidade; dá nome ao povo "Ludians". 103x total, aparece em diálogo. Fonte: corpus.
- **Pabpab**: localidade — topônimo. 25x no corpus. Fonte: corpus.
- **Golden Plains**: local geográfico mencionado em diálogo. Fonte: corpus.
- **Tower**: refere-se à Torre do Vento (Pung'tap = "The Tower of Wind") e a Torres Imperiais. Contexto de diálogo. Fonte: corpus.
- **Causeway**: "Imperial Causeway" — via mencionada em diálogo de contexto de guerra. Fonte: corpus.
- **Fane**: templo/santuário — topônimo em diálogo. Fonte: corpus.
- **Imperial Capital**: capital do Império Fou. Fonte: corpus.
- **Kasq Woods, Yorae Shrine, Sonne, Shyde, Kyoin**: localidades adicionais mencionadas no corpus. Fonte: corpus.

#### Ações e mecânicas em diálogo (corpus)
Termos comuns que aparecem no corpus de DIÁLOGO (AREAD+AREAS) como instrução ou referência narrativa:
- **Change**: instrução de mudança de forma/transformação em diálogo. Fonte: corpus.
- **Try**: instrução em diálogo ("Try this"). Fonte: corpus.
- **Move**: ação de movimento em diálogo. Fonte: corpus.
- **Army**: referência a exércitos em diálogo de guerra. Fonte: corpus.
- **Using Silverware**: habilidade mencionada em diálogo. Fonte: corpus.
- **Insurance Contract**: mecânica Manillo mencionada em diálogo. Fonte: corpus.
- **Thirteenth, Eighth, Fifth, Fourth**: ordinais referentes a cargos/gerais em diálogo ("Thirteenth General"). Fonte: corpus.

#### Criaturas, magia e mecânicas adicionais (corpus)
- **Demons**: categoria de inimigos em diálogo. Fonte: corpus.
- **Egg Magic**: habilidade especial em diálogo. Fonte: corpus.
- **Magic**: referência a magia em geral em diálogo. Fonte: corpus.
- **Power Level**: nível de poder em diálogo (vara de pesca ou progressão). Fonte: corpus.
- **Tomb**: "Emperor's Tomb" — local referenciado em diálogo. Fonte: corpus.
- **Grass Dragon, Sand Dragon, Rock Dragon, Tree Dragon, Mud Dragon**: formas dragão de Ryu mencionadas em diálogo. Fonte: corpus + training-T2.
- **Dragon Crystal**: item mencionado em diálogo. Fonte: corpus.
- **P'ung Ryong**: nome coreano do Dragão do Vento (15x em diálogo). Fonte: corpus.
- **Ludians**: povo de Ludia mencionado em diálogo. Fonte: corpus.
- **ARaises Power**: efeito de habilidade em diálogo. Fonte: corpus.

#### Tratamentos informais e locais menores (corpus)
- **Gramps**: honorífico informal usado em diálogo para ancião. Fonte: corpus.
- **Hesperia**: localidade mencionada em diálogo. 20x. Fonte: corpus.
- **Ninth**: ordinal — título/cargo militar em diálogo. Fonte: corpus.
- **Twelfth**: ordinal — título/cargo em diálogo. Fonte: corpus.
- **Temul, Pukapuka, Poko, Zig, Chedo, Beyd, Lyta, Kryrik, Rhem, Rudd, Tak, Kahn, Rhoppe**: NPCs/localidades mencionados no corpus de diálogo. Fonte: corpus.
- **Standing**: referência a posição/cargo em diálogo. Fonte: corpus.
- **West**: referência geográfica em diálogo. Fonte: corpus.
- **Quit**: ação/instrução em diálogo. Fonte: corpus.
- **Desert Dif**: localidade — variante de Astan Dif na região de deserto. Fonte: corpus.
- **Island**: local geográfico em diálogo. Fonte: corpus.
- **Close**: ação em diálogo. Fonte: corpus.
- **Diet Hard**: habilidade de batalha (trocadilho com "Die Hard"). Fonte: corpus.
- **Material**: categoria de item em diálogo. Fonte: corpus.
- **Table Manners**: habilidade de batalha (nome humorístico). Fonte: corpus.
- **Catch**: ação de captura em diálogo (pesca). Fonte: corpus.
- **Directional**: instrução de controle em diálogo. Fonte: corpus.
- **Equip**: ação de equipar em diálogo. Fonte: corpus.
- **Super Combo**: técnica de batalha em diálogo. Fonte: corpus.
- **Ultimate**: nível/tipo de habilidade em diálogo. Fonte: corpus.
- **Western**: referência geográfica (Western Continent) em diálogo. Fonte: corpus.

#### Declined — termos rejeitados como não-próprios (UI pura, sem diálogo)
Os seguintes candidatos foram classificados como false positives de UI/menu pura (não aparecem no corpus de diálogo AREAD+AREAS):
Use, Buy, Add, Return, Choose, Equip, Sell, Close, Hard, Land, Simple, Normal, Large, Powerful, View, Castle (quando genérico), Trade, Final, Key, User, Uses, Types, Fish, Fishing, Worm, Extra, Heavy, Sink, Plow, Culture, Ear, Handmade, Buy Sell Stop, Ultimate

---

### Decisões pendentes (aguardam revisão humana)

1. **Endless → "Eternos" ou manter "Endless"?** — termo central da cosmologia. Proposta IA: "Eternos". Precisa de ratificação humana.
2. **Hex → "maldição" ou manter "hex"?** — mecanismo de sistema (hex energy, hex attacks). Proposta IA: "maldição" para texto narrativo; considerar manter "hex" em menus de status. Precisa de ratificação.
3. **Abbess → "Abadessa" ou manter "Abbess"?** — título religioso. Proposta IA: "Abadessa".
4. **Gênero de Elina e Deis** — feminino confirmado pelo contexto corpus. Sem incerteza.
5. **Nome do protagonista** — renomeável; "Ryu" é o nome padrão/canônico. A confirmar se manter "Ryu" como padrão PT-BR.

---

### Human input

human_input: pending

> Contribuição humana ainda não recebida. O gate de cobertura (`kb_phase all --check`)
> vai BLOQUEAR até que o status mude para `reconciled` (requer contribuição humana
> OU declínio explícito: `human_input: declined`).
>
> Para reconciliar: envie suas fontes (wiki, guias, material oficial de BoF4),
> corrija/complemente as entidades acima, e altere a linha de status para:
> `status: reconciled`
