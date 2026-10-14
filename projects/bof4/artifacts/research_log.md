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
| T1 | Manual oficial do jogo (PC, 2003) — `english/manual.pdf` da instalação; texto em `research_cache/91074abab54433a8.md` | Premissa, descrição dos 7 personagens, sistema de jogo | Humano |
| T2 | Wiki de fãs — https://bof.fandom.com/wiki/Breath_of_Fire_IV (via `api.php`, wikitext em `research_cache/413185b2524bd869.md`) | Ambientação, enredo completo, notas de localização e censura | Humano |

**Atribuição e licença das fontes abertas:** o texto abaixo é síntese própria, sem cópia literal. A Wikipedia PT
(CC BY-SA 4.0) e a wiki de fãs do Fandom (em geral CC BY-SA 3.0) são citadas como fonte; qualquer trecho
reaproveitado delas mantém atribuição e a mesma licença. O manual oficial e o corpus do jogo são consultados só
para conferir grafia e uso, sem reproduzi-los.

**Reconciliação humana:** usuário forneceu Wikipedia PT como fonte principal (2026-06-20).
Novos termos confirmados pela Wikipedia: **Aliança do Leste** (Eastern Alliance), **Synesta** (cidade onde Elina desapareceu), **Sandflier** (veículos que navegam no oceano de areia), **Império Fou** (grafia PT confirmada).

---

### Entidades e fontes por categoria

#### Personagens — grupo principal
- **Ryu**: protagonista amnésico, metade do deus Yorae (luz); control code [04][01]; pode transformar em dragões. Fonte: training-knowledge-T2 + corpus (control code analysis).
- **Fou-lu**: imperador, metade do deus Yorae (sombra); acordou de 600 anos; grafia "Fou-lu" confirmada in-corpus via item desc. Fonte: training-knowledge-T2 + corpus (53x "Fou").
- **Nina**: princesa de Wyndia, asas; procura Elina. Fonte: training-knowledge-T2.
- **Cray**: jovem líder do povo Woren, procura Elina (amiga de infância). Fonte: manual oficial (T1); corrige o "noiva" do training-knowledge-T2 (no corpus Elina é "the prince's fiancee").
- **Scias**: mercenário Grassrunner, fala com gagueira. Fonte: training-knowledge-T2.
- **Ursula**: capitã imperial, junta-se ao grupo. Fonte: training-knowledge-T2.
- **Ershin**: armadura com Deis aprisionada, fala em 3ª pessoa. Fonte: training-knowledge-T2.

#### Personagens — NPCs e antagonistas
- **Elina**: irmã de Nina, desaparecida; confirmada 159x no corpus ((fala do corpus)). Fonte: corpus.
- **Yuna**: "Lord Yuna", antagonista científico imperial; 88x no corpus. Fonte: corpus + training-knowledge-T2.
- **Deis**: deusa serpente; 55x no corpus ("Says Deis"). Fonte: corpus.
- **Marlok**: mercador NPC; corpus: "I am Marlok" (auto-apresentação direta). Fonte: corpus.
- **Rasso**: "Captain Rasso"; 4x no corpus. Fonte: corpus.
- **Abbess**: líder religiosa; 37x no corpus ("the Abbess' home"). Fonte: corpus.
- **Chino**: criança NPC; 48x. Fonte: corpus.

#### Locais
- **Wyndia**: reino dos Wyndians; 143x no corpus. Fonte: corpus + training-knowledge-T2.
- **Astana**: cidade onde a Carronade foi construída, conforme o corpus. Fonte: corpus.
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
- **Endless**: deuses que estão desaparecendo, conforme o corpus. 72x. Fonte: corpus.
- **Yorae Dragon**: citado no corpus como alvo de captura. 71x. Fonte: corpus.
- **Kecak**: 264x no corpus — jogo de dados. Fonte: corpus.
- **Carronade**: corpus: (fala do corpus) 54x. Fonte: corpus.

#### Criaturas/Povos
- **Faeries**: 72x no corpus (mecânica de vila). Fonte: corpus.
- **Manillo**: corpus: (fala do corpus) 34x. Fonte: corpus.
- **Woren**: povo-tigre; corpus confirma "Worent" (aldeia). 78x. Fonte: corpus + training-knowledge-T2.
- **Wyndian**: corpus: "ancient Wyndian hero". 41x. Fonte: corpus.

#### Stats e UI (glossary)
- **Pwr/Def/Agl/Wis/Wgt**: abreviações de stat confirmadas in-corpus. Propostas: For./Def./Agi./Sab./Pes. Fonte: corpus + convenção JRPG PT-BR (training-T2).
- **HP** (Hit Points): pontos de vida; manter "HP". Fonte: corpus.
- **AP** (Action Points): pontos de ação/magia; manter "AP". Fonte: corpus.
- **Hit** (taxa de acerto): traduzir "Acerto". Fonte: corpus.
- **Dodge** (esquiva): traduzir "Esquiva". Fonte: corpus.
- **Princess**: título de Nina ("Princess [04][XX]"). Traduzir "Princesa". Fonte: corpus.
- **Hex**: corpus: (fala do corpus), (fala do corpus). 159x. Fonte: corpus.
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
- **Majesty**: tratamento real ((fala do corpus)). Fonte: corpus.
- **Ahtar**: NPC do corpus de diálogo. Fonte: corpus.
- **Mei**: NPC do corpus de diálogo. Fonte: corpus.

#### Locais adicionais (corpus)
- **Ludia**: região/localidade; dá nome ao povo "Ludians". 103x total, aparece em diálogo. Fonte: corpus.
- **Pabpab**: localidade — topônimo. 25x no corpus. Fonte: corpus.
- **Golden Plains**: local geográfico mencionado em diálogo. Fonte: corpus.
- **Tower**: refere-se à Torre do Vento (Pung'tap = (fala do corpus)) e a Torres Imperiais. Contexto de diálogo. Fonte: corpus.
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

### Decisões resolvidas (2026-06-21 — ratificação humana)

1. **Endless → "Eternos"** ✓ — ratificado pelo usuário. Usar "Eternos" em todo o texto narrativo e diálogo.
2. **Hex → "maldição"** ✓ — ratificado pelo usuário. Usar "maldição" em diálogos e narrativa.
3. **Abbess → manter "Abbess"** ✓ — ratificado pelo usuário. Personagem NPC não jogável; nome próprio não traduzido.
4. **Gênero de Elina e Deis** ✓ — feminino confirmado pelo corpus. Resolvido.
5. **Nome do protagonista → "Ryu" (padrão)** ✓ — ratificado pelo usuário. Nome personalizável pelo jogador; padrão canônico é "Ryu". Aparece via control code `[04][01]`, nunca como texto literal — não requer tradução.

---

#### Nomes adicionais (2026-10-11 — cruzamento wiki × corpus + worklist do kb_phase)

Síntese por IA. Fonte por item: wiki de fãs (wikitext em `research_cache/`) quando há página; senão só o corpus. Traduções marcadas como proposta estão pendentes de ratificação pelo usuário.

- **Oracle of Wind** (Personagem): Sacerdotisa que serve o Dragão do Vento P'ung Ryong; vive em Kasq Woods. 10x. Tradução: 'Oráculo do Vento' (ratificado pelo usuário em 2026-10-11). Fonte: wiki de fãs + corpus.
- **King of Wyndia** (Personagem): Pai de Nina e Elina, monarca de Wyndia (Aliança do Leste). 5x. Tradução: 'Rei de Wyndia' (ratificado pelo usuário em 2026-10-11). Fonte: wiki de fãs + corpus.
- **Bunyan** (Personagem): Lenhador solitário que cuida de Fou-lu ferido; também é mestre de habilidades. 4x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Tahb** (Personagem): Chefe do grupo que limpa Chamba dos efeitos da maldição (hex). 4x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Ilgor** (Personagem): Serve ao príncipe de Ludia; tratado por 'Master Ilgor'. 1x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Stoll** (Personagem): Mestre de habilidades; aparece como 'Stoll the Thief' no minijogo de pegar o ladrão. 1x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Ni Ryong** (Personagem): Dragão da Lama, um dos Eternos; feminino ('She' na wiki). Fala arcaica ('I watcheth o'er this world'). 1x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Mugul** (Personagem): Quinto Imperador do Império Fou; citado só em títulos de livros de história. 13x. Manter grafia. Fonte: corpus.
- **Shei** (Personagem): Nono Imperador do Império Fou; citado só em títulos de livros de história. 13x. Manter grafia. Fonte: corpus.
- **Sen** (Personagem): Um dos cinco apresentados por Beyd ((fala do corpus)). 2x. Manter grafia. Fonte: corpus.
- **Shami** (Personagem): Um dos cinco apresentados por Beyd. 2x. Manter grafia. Fonte: corpus.
- **Rinpo** (Personagem): Um dos cinco apresentados por Beyd. 2x. Manter grafia. Fonte: corpus.
- **Poske** (Personagem): Um dos cinco apresentados por Beyd. 2x. Manter grafia. Fonte: corpus.
- **Peso** (Personagem): Um dos cinco apresentados por Beyd. 2x. Manter grafia (nome próprio; não é a moeda). Fonte: corpus.
- **Marcy** (Personagem): 'Sister Marcy', citada junto de Chino (AREAS011/046). 2x. Manter grafia; 'Sister' = Irmã (religiosa). Fonte: corpus.
- **Modo** (Personagem): Criança do esconde-esconde ((fala do corpus), AREAS011/046). 2x. Manter grafia. Fonte: corpus.
- **Pabupabu** (Conceito): Palavra da língua de Pukapuka ((fala do corpus)); também título de faixa. 2x. Manter grafia. Fonte: corpus.
- **Mt. Glom** (Local): Monte vulcânico na região das Planícies Douradas, continente oriental. 6x. Manter 'Mt. Glom'. Fonte: wiki de fãs + corpus.
- **Zhinga Mts.** (Local): Região montanhosa do continente ocidental. 6x. Manter 'Zhinga'. Fonte: wiki de fãs + corpus.
- **Kyria** (Local): Vila do continente oriental cheia de armadilhas; o prefeito guarda a passagem para Synesta. 2x. Manter grafia. Fonte: wiki de fãs + corpus.
- **En Jhou** (Local): Ruínas na floresta da península de Paedra, a leste do rio Shan. 2x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Paedra** (Local): Península do continente ocidental (Shan River, En Jhou). 2x. Manter grafia. Fonte: wiki de fãs + corpus.
- **S. Hesperia** (Local): Região do continente ocidental; aparece na lista de áreas de pesca. 2x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Shan River** (Local): Rio grande da península de Paedra. 1x. Manter 'Shan'. Fonte: wiki de fãs + corpus.
- **Kwanso** (Local): Local com portão de passagem no continente ocidental. 1x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Sandflier Valley** (Local): Cemitério de sandfliers ao sul de Sarai, onde Ryu e Nina buscam peças. 2x (+2 em AREAS004). Tradução: 'Vale dos Sandfliers' (ratificado pelo usuário em 2026-10-11). Fonte: wiki de fãs + corpus.
- **Spell of Evocation** (Conceito): Técnica secreta de invocação que traz os Eternos ao mundo, guardada na vila de Chek. 2x. Tradução a definir — pendente de ratificação. Fonte: wiki de fãs + corpus.
- **They Who Pass** (Conceito): Como os Eternos chamam os humanos, por serem mortais. 2x. Tradução a definir — pendente de ratificação. Fonte: corpus.
- **Land of Dreams** (Conceito): Lugar para onde as fadas levam Ryu. 2x. Tradução a definir — pendente de ratificação. Fonte: corpus.
- **Wyd** (Criatura): Inimigo de Mt. Glom; vira Firewyd se atingido por fogo. 3x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Drake** (Criatura): Inimigo de Mt. Glom, citado junto de Wyd. 3x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Status** (Mecânica): tipo de ataque/condição ('Status attacks', 276x no corpus). Manter 'Status', termo usual em JRPG em pt-BR. Fonte: corpus.
- **Buy / Sell / Stop / Normal** (UI): rótulos de menu que vivem nos arquivos de cena (loja em AREAS021/041, modo do minijogo em AREAS041). Entraram no corpus com a correção do extrator (issue do backlog). Traduzir: Comprar / Vender / Parar / Normal. Fonte: corpus.
- **Sink** (Mecânica): movimento de isca na ajuda da pesca (AREAD075, (fala do corpus)). Verbo comum: afundar. Fonte: corpus.
- **Pilfer, Blitz, Spray, Clip, Egghead** (Mecânica): nomes de habilidade, listados como rótulo em AREAS015/016/020 e AREAS002/017/018/019, junto de 'Super Combo' (já no glossário, mantido). Manter em inglês: o menu de batalha, onde o jogador usa esses nomes, está fora do escopo e continua em inglês. Rever se a UI de batalha for traduzida. 'Oracle' na mesma lista é a habilidade homônima e segue a mesma regra nesse rótulo. Fonte: wiki de fãs (List of Breath of Fire IV Abilities) + corpus.

Descartados como ruído da worklist (não são nomes próprios de lore): títulos de faixas do teste de som ('Desert Town', 'Bastard Sword', 'Thousand Winds' etc.), nomes de iscas e varas de pesca, rótulos de menu/controle, listas de loja e de habilidades coladas pela extração, e 'Zee Empire' (sotaque de Marlok para 'the Empire').

#### Re-extração com AREAM/AREAE e falas completas (2026-10-11 — worklist do kb_phase)

Síntese por IA. O corpus passou de 6.417 para 19.234 linhas (famílias AREAM/AREAE incluídas; fala não é mais cortada em `0x00` de parâmetro). Entraram rótulos de menu e de minijogo (pesca, colônia de fadas) e alguns nomes. Traduções marcadas como proposta estão pendentes de ratificação.

- **Una** (Personagem): Moça Woren de Worent que ajuda na casa dos Anciões; mestra de habilidades ('Master Una'). 41x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Pokko** (Personagem): Moradora de Pabpab citada na língua local ((fala do corpus)). 29x. Manter grafia. Fonte: corpus.
- **Ch'o Ryong** (Personagem): Dragão da Grama, um dos Eternos. 13x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Sa Ryong** (Personagem): Dragão da Areia; danifica o sandflier de Nina e Cray na abertura. 12x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Su Ryong** (Personagem): Dragão da Árvore, a grande árvore sábia perto de Chamba. 4x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Hae Ryong** (Personagem): Dragão do Mar, no santuário de Fane. 6x. Manter grafia. Fonte: wiki de fãs + corpus.
- **Goete** (Personagem): Criança do esconde-esconde (fala do corpus). 4x. Manter grafia. Fonte: corpus.
- **Konoko** (Personagem): Criança do esconde-esconde. 4x. Manter grafia. Fonte: corpus.
- **Modo** (Personagem): Criança do esconde-esconde ((fala do corpus)). 2x. Manter grafia. Fonte: corpus.
- **Marcy** (Personagem): Irmã Marcy, do orfanato de Chek ('Sister Marcy'). 2x. Manter grafia. Fonte: corpus.
- **Kyria** (Local): Vila com prefeito ((fala do corpus)). Manter grafia. Fonte: wiki de fãs + corpus.
- **Rand** (Personagem): Nomes das fadas da colônia (lista do minijogo). Manter grafia. Fonte: corpus.
- **Purifiers** (Facção): 'Purificadores'. Grupo que vai de cidade em cidade purificando a maldição (hex). Proposta, pendente de ratificação. Fonte: corpus.
- **Elders** (Personagem): 'Anciões'. Anciões Woren de Worent ('the Elders'). Proposta, pendente de ratificação. Fonte: corpus.
- **Troops** (Facção): 'Tropas'. 'Imperial Troops' = Tropas Imperiais. Fonte: corpus.
- **Continent** (Local): 'Continente'. 'Western Continent' = Continente Ocidental. Fonte: corpus.
- **Region** (Local): 'Região'. 'Shikk Region' = Região de Shikk. Fonte: corpus.
- **Nameless** (Local): 'Sem Nome'. 'Nameless Island' = Ilha Sem Nome. Proposta, pendente de ratificação. Fonte: corpus.
- **Gateway** (Local): 'Portal'. Passagem entre os continentes ('This must be the Gateway'). Proposta, pendente de ratificação. Fonte: corpus.
- **Mighty** (Cultural): 'Poderosa'. Tratamento: 'Mighty Deis' = Poderosa Deis. Fonte: corpus.
- **Bah** (Cultural): 'Bah'. Interjeição; adaptar ao tom (Bah!/Ora!). Fonte: corpus.
- **Don** (Cultural): 'Não'. Não é nome: contração de sotaque ("Don' let..."). Fonte: corpus.
- **Rótulos de UI** (Add, Adjust, Age, Auto, Buttons, Camera, Choose, Compass, Controller, Data, Destroy, Difficulty, Easy, Fast, Hints, Info, Items, Key, Learn, Manual, Mode, Mono, Norm, Options, Pad, Pause, Play, Rank, Reset, Resolution, Reverse, Screen, Search, Slow, Sound, Stereo, SubScreen, Switch, Talk, Text, Tips, Toggle, Vib, Vibration, View, Dash, Beginners, Shop, Inn, Bar, Weapons, Arms, Museum, Arcade, Barracks, Conservatory, Music, Art, Games, Explorers, Bonds, Aurum, Mayor, Place): menus que vivem nos arquivos de cena. Traduzir. Fonte: corpus.
- **Termos de minijogo e descrição** (Abilities, Ability, Activity, Meter, Approval, Rating, Assigning, Assist, Atk, Attracts, Best, Birth, Building, Houses, Culture, Cut, Depth, Diligent, Ordinary, Lazy, Odd, Endurance, Style, Fancy, Farm, Fish, Fishing, Floats, Free, Handmade, Heavy, Hooking, Hunt, Hunting, Increases, Job, Jobs, Lifelike, Orders, Plow, Poison, Powerful, Range, Rarely, Reel, Relax, Rise, Rises, Shaped, Shiny, Spd, Tec, Terrain, Thief, Type, Types, Uses, Well-balanced, Work, Worm, Frogger, Minnow, Topper, Spinner, Winder, Devil, Drops, Bird, Meat, Rotten, Ice, Ring, Sun, Breath): pesca, colônia de fadas, efeitos. Traduzir. Fonte: corpus.
- **Golpes em lista de cena** (Megaphone, SpiritBlast, Cleave, Disembowel): manter em inglês, como no menu de batalha. Fonte: corpus.
- **Nomes de fadas e de crianças** (Chai, Fumi, Yuka, Vizy, Poff, Sila, Meyl, Biky, Apa, Phly, Hyat, Chik, Cyrl, Oban, Choi, Pema, Chmo, Beco, Yohn, Ramo, Parz, Ludy, Poke, Kayo, Wabu, Rass, Boko, Yuhi, Sasa, Lany, Aili, Jika, Yuma, Feyl, Kora, Sena, Rahn, Sino, Mamu, Kupi, Kiil, Dita, Bole, Pahn, Naeg, Guti, Maki, Ginz, Nyan, Kari, Sen, Shami, Rinpo, Poske, Peso): manter grafia. Fonte: corpus.

#### Cenas curtas e textos de sistema (2026-10-11 — worklist do kb_phase)

Síntese por IA. O corpus passou de 19.234 para 19.873 linhas: 62 cenas curtas que o detector de seção descartava (tabela fixa de 256 ponteiros e poucas falas) e as duas seções de texto do `INIT.DAT` (avisos de inventário e loja, nomes de região do mapa, menu). `AREAS056` passou a ler a seção certa. Traduções são proposta, pendentes de ratificação.

- **Personagem — manter grafia** (Rey, Yohm, Nahma, Fu, Chuman): Nome próprio; manter grafia. Fonte: corpus.
- **Local — manter grafia** (Ahm, Astan, Chiqua, Soma, Kurok, Wychwood, Giga, Pauk, Mukto, Sinchon, Ryft, Yogy): Nome de lugar do mapa-múndi / lista de regiões (INIT.DAT); manter grafia. Fonte: corpus.
- **Local — traduzir** (Village→Vila, City→Cidade, Town→Cidade, Kingdom→Reino, Highway→Estrada, Bridge→Ponte, Wharf→Cais, Dam→Represa, Aqueduct→Aqueduto, Hideout→Esconderijo, Beach→Praia, Cliff→Penhasco, Sanctum→Santuário, Hut→Cabana, Fen→Brejo, Peak→Pico, Cove→Enseada, Jungle→Selva, Residence→Residência, Highlands→Planalto, Hills→Colinas, Habitat→Hábitat, Preserve→Reserva, Area→Área, Storage→Depósito, Eastern→Leste, Northern→Norte, North→Norte, South→Sul, Crash→Queda, Gold→Ouro): Substantivo comum em nome de lugar ou placa; segue o nome próprio (ex.: Chiqua Village = Vila de Chiqua). Fonte: corpus.
- **Local — traduzir** (Rvr→Rio, Wds→Bosq., Chkpoint→Posto, WestGate→PortãoO, FishSpot→Pesqueiro, St→St.): Abreviação de rótulo do mapa (largura fixa); manter curta. Fonte: corpus.
- **UI — traduzir** (Rest→Descansar, Trade→Trocar, Enter, Main→Principal, Menu, Purchase→Comprar, Skill→Habilidade, Mstr→Mestre, Minigame→Minijogo, Instructions→Instruções, Secret→Secreto, Bonus→Bônus, Direction→Direção, Judging→Avaliar, Ship→Navio, Logs→Toras, Entry→Entrada, Permission→Permissão, Trapped→Armadilha, Repairs→Conserto, Control→Controle, Panel→Painel, Sluice→Comporta, Winch→Guincho, Barrel→Barril, Jar→Jarro, Anchor→Âncora, Endangered→Ameaçada, Species→Espécie, Wildlife→Vida Selvagem, Health→Vida, Retreat→Recuar): Rótulo de menu ou aviso de sistema (INIT.DAT e menus em cena). Fonte: corpus.
- **Item — traduzir** (Copper→Cobre, Bell→Sino, ElectrumBell→Sino de Electro, PlatinumBell→Sino de Platina, Charm→Amuleto, Dress→Social, Shoes→Sapatos, Multivitamin→Multivitamina, Vitamin→Vitamina, Midas, Stone→Pedra, Soul→Alma, Spanner→Chave Inglesa, Sausage→Salsicha, Beer→Cerveja, Steak→Bife, Wine→Vinho, Snake→Cobra): Nome de item/prêmio em lista de cena; conferir com o menu de itens quando ele for traduzido. Fonte: corpus.
- **Mecânica — manter grafia** (Supplication, Holy, Strike, Resist, Benediction, Monopolize, Roulette, Curse, Ride): Nome de golpe/magia em lista de cena: manter em inglês, como no menu de batalha. Fonte: corpus.
- **Criatura — manter grafia** (Mage, Goo): Nome de inimigo (Mage Goo); manter em inglês, como na lista de inimigos. Fonte: corpus.
- **Cultural — traduzir** (Bastard→Bastarda, Beginnings→Começos, Believing→Crer, Distant→Distante, Divine→Divino, Danger→Perigo, Blood→Sangue, Fall→Queda, Streams→Riachos, Mixed→Misturado, Money→Dinheiro, Neverending→Sem Fim, Rain→Chuva, Numbers→Números, Poisoned→Envenenado, Air→Ar, Pressure→Pressão, Rampant→Desenfreado, Round→Volta, Sailing→Navegando, Tension→Tensão, Song→Canção, Moon→Lua, Thousand→Mil, Traveling→Viajante, Merchant→Mercador, Spirits→Espíritos, Trouble→Problema, Ahead→Adiante, Truth→Verdade, Fiction→Ficção, Unwavering→Inabalável, Courage→Coragem, Watch→Cuidado, Step→Passo, Working→Trabalho): Título de faixa da sala de música (lista de títulos em inglês): palavra comum, traduzir no título. Fonte: corpus.
- **Cultural — traduzir** (Course→Claro, Zee→O, P-princess→P-princesa, Firing→Disparar, Stepping→Pisar, Watching→Ver, Near→Perto, June→junho): Não é nome próprio: palavra comum, sotaque ou gagueira capitalizada no meio da fala. Fonte: corpus.
- **Rey**, **Yohm**, **Nahma**, **Fu Chuman** (Personagem): nomes citados em fala; Yohm é o general do Império já listado na wiki de fãs (antes sem ocorrência no corpus). Fonte: wiki de fãs + corpus.
- **Soma**, **Chiqua** (Local): Floresta de Soma (continente do sul) e Vila de Chiqua. Fonte: wiki de fãs + corpus.

### Manual oficial — reconciliação (2026-10-10)

Fonte fornecida pelo usuário. Fatos extraídos (síntese por IA). Pendente de ratificação pelo usuário.

- Dois continentes separados por um pântano intransponível; o primeiro contato virou guerra entre o Império Fou (oeste) e uma aliança de países (leste).
- A guerra terminou em armistício por exaustão dos dois lados. Elina desapareceu **um ano depois**, numa cidade pequena perto da linha de frente, enquanto visitava campos de batalha e veteranos.
- A Aliança não pôde fazer uma busca em larga escala: mandar tropas à fronteira quebraria o armistício. Por isso Nina parte sozinha.
- Ryu: raça e terra natal desconhecidas; Nina o encontra inconsciente numa cidade do deserto, no continente leste. Tem o Olho do Dragão ("Dragon's Eye", 2× no corpus).
- Fou-lu: unificou sozinho o continente oeste, primeiro imperador, há várias centenas de anos; teria previsto a própria ressurreição ao morrer.
- Cray: jovem líder dos Woren, amigo de infância de Elina, age como líder do grupo. Corrige o "noiva" que vinha do training-knowledge-T2.
- Ershin: armadura totalmente selada, para proteger contra maldições; ninguém conhece seu rosto. O manual trata Ershin por "she".
- Scias: mercenário contratado pelo lado leste durante a guerra; vira o vigia do grupo; calado e distante.
- Ursula: "middle-class leader of the Fou Empire" (oficial de patente média) criada no meio militar; veio ao continente leste à procura de dragões; sabe pouco do mundo fora do quartel.

Divergências de nomenclatura — o manual é outra localização; **o corpus in-game prevalece**:

| Manual | Corpus (usar) | Ocorrências no corpus |
|---|---|---|
| Elena | Elina | 0 × 159 |
| Fae tribe (winged folk) | Wyndian | 0 × 41 |
| curse | hex → "maldição" | 2 × 159 |
| armistice | cease-fire | 0 × 6 |

Extração: o PDF tem duas colunas. As páginas de personagens (pp. 5–6 do manual) foram relidas em 2026-10-11 com `pdfplumber`, uma coluna por vez; os trechos de Scias e Ursula acima conferem com o texto e a patente de Ursula foi recuperada.

### Wiki de fãs (Fandom) — reconciliação (2026-10-10)

Fonte fornecida pelo usuário; a página está marcada `{{rewrite}}` na própria wiki. Síntese por IA. Pendente de ratificação pelo usuário. Só o arco inicial foi sintetizado; o resto do enredo (destino de Elina, final) fica no cache, fora da KB, para não vazar no context_pack.

- Abertura: Nina e Cray percorrem cidades à beira do grande deserto atrás de Elina, sumida numa missão diplomática. Elina é irmã mais velha de Nina e "love interest" de Cray (bate com o "amiga de infância" do manual; nenhuma fonte diz noiva).
- Nina vê um dragão virar um rapaz numa cratera; ele só lembra o nome, Ryu. Ela conclui que é amnésia e o convence a ajudar.
- Dois blocos culturais: Império Fou (oeste, inspirado na China feudal) e reinos do leste (Europa medieval e Arábia). Paz frágil depois de anos de guerra.
- Endless: seres imortais, divinos, em forma de dragão, que controlam os elementos.
- Hex: miasma maligno que empesteia uma cidade; Ershin guia o grupo pelo lado envenenado.
- Scias: mercenário alto, de aparência canina. Ursula: de família de alto oficial imperial; entra no grupo para vigiá-lo.
- Localização EN: feita às pressas (7 meses); nomes de magias e dragões foram postos em coreano de propósito, para soar estrangeiro → manter como estão (confirma P'ung Ryong). Linguagem dura foi suavizada em relação ao japonês.

Divergências de grafia — **o corpus in-game prevalece**:

| Wiki | Corpus (usar) | Ocorrências no corpus |
|---|---|---|
| Fou-Lu | Fou-lu | 0 × 13 linhas |
| Kyojin | Kyoin | 0 × 4 |
| sand-flier | Sandflier | 0 × 6 |
| Yohm | (não aparece com essa grafia) | 0 |

### Wiki de fãs — páginas individuais (2026-10-10)

500 páginas das categorias de BoF4 baixadas via `api.php` (20 arquivos em `research_cache/`, 25 páginas por arquivo). Ficaram de fora: música, imagens, mangá, novel e guias. Lidas e sintetizadas por IA só as do arco inicial (Sarai, Valley, Joh, Nina, Cray, Ryu, Elina, Woren, Kyria e vizinhas) → seção "Arco inicial — Sarai" da KB. Pendente de ratificação pelo usuário. O resto está no cache, não lido.

- Confirma: Elina é noiva do príncipe de Ludia (casamento arranjado), não de Cray. Fecha a inferência feita a partir do corpus.
- Cruzamento de títulos × corpus: 398 dos 501 títulos não aparecem em `dialogs.csv` (nomes de itens, habilidades e inimigos não estão nos diálogos AREAD/AREAS; personagens principais entram por control code). 32 aparecem no corpus e não estão em glossário, entidades nem KB: Oracle of Wind (10), Zhinga Mts. (6), Mt. Glom (6), King of Wyndia (5), Tahb (4), Bunyan (4), Kyria (2), Sarai (2), Joh (2), En Jhou (2), Paedra (2), S. Hesperia (2), Stoll, Shan River, Ni Ryong, Kwanso, Ilgor e outros de 1–3 ocorrências. Candidatos a entrar em `entities.csv`/`glossary.csv` no passo 01–04.
- Termos da wiki que não são grafia do jogo (0 no corpus): Information Broker, Black Market, King's Sword, Purifiers, Wing Clan, Sa Ryong, Morley. Usar só como descrição, nunca como termo.

### Human input

human_input: confirmed

> Contribuição humana recebida em 2026-06-20: Wikipedia PT como fonte T1 (personagens,
> locais, facções). Novos termos ratificados: Aliança do Leste, Synesta, Sandflier,
> Império Fou.
>
> Atualização 2026-06-21: todas as decisões pendentes ratificadas pelo usuário (ver seção acima).
