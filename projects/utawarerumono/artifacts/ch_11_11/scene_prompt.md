# Cena ch_11_11 — pacote de traducao (121 linhas)

> Pacote AUTO-CONTIDO e LIMITADO (so o que esta cena precisa). Traduza EN -> pt-BR
> seguindo a Carta abaixo. Saida exigida ao final. Nao precisa de contexto externo.

---

## 1. CARTA DE GOVERNANCA (contrato de qualidade)

# CARTA DE GOVERNANÇA DE TRADUÇÃO
## Contrato de qualidade que a IA SEGUE ao traduzir (transversal aos Passos 05–08)

> **Natureza:** não é um passo do pipeline — é o **contrato** que rege *como* traduzir em todos os
> passos cognitivos (05 planejamento, 06 tradução, 06b/06c QA, 07 QA final). Genérico: nenhum dado de
> obra vive aqui; tudo específico vem de `project.json` + artefatos.
>
> **Regra-mãe:** **a IA traduz conforme esta Carta — não improvisa fora dela.** Quando uma linha não
> puder satisfazer a Carta, a IA **sinaliza** (QA/`risk_notes`), não inventa.

---

## O QUE É "TRADUÇÃO DE QUALIDADE" AQUI

Localização de qualidade preserva **identidade, tom e sentido na situação** — não traduz palavra a
palavra. Toda linha é avaliada **no contexto do personagem, do mundo e da cena**, com uma âncora única:

> **"Uma pessoa nativa, lendo isto NESTA situação, entende com naturalidade e sente o que deveria sentir?"**
> Se não → revisar. Se não dá para satisfazer → sinalizar (não entregar às cegas).

---

## AS QUATRO DIRETRIZES

### 1. Contexto de PERSONAGEM (voz)
- Cada linha respeita o **perfil de voz** do falante em `tone_analysis.md` (registro, léxico,
  comprimento de frase, tiques). `voice_criticality: high` → verificação **em cada linha**.
- **Identidade dupla:** a persona pública nunca exibe traços/nomes da identidade revelada antes do
  `reveal_timing` (`aliases_map.json`). Voz consistente: o personagem soa como **a mesma pessoa** do
  começo ao fim do corpus.

### 2. Contexto de MUNDO (lore)
- Termos do `glossary.csv` seguem o `handling_rule` (`manter_original`/`traduzir`/`traduzir_parcial`);
  **formas exatas** sem variação não justificada.
- **Spoilers:** nenhum nome/revelação aparece antes do `reveal_timing`.
- Honoríficos, formalidade e tratamento conforme a **relação** dos personagens no mundo.

### 3. Contexto de SITUAÇÃO (cena/emoção)
- Traduzir pela **intenção/emoção** da cena (susto, dor, comédia, solenidade, ternura), não pela letra
  — usar `intent`/`tone_register` do `translation_plan.json`.
- **Interjeições/onomatopeias/exclamações são tradução**: localizar à convenção do idioma-alvo (curada
  em um artefato de referência do projeto), nunca copiar do source. (Ver `06_translation.md` e a
  referência de interjeições do projeto.)
- **Continuidade:** a junção de linhas quebradas (`\n`) soa natural; ritmo de comédia preservado.
- **Restrição do conector:** se há transliteração na gravação (fonte sem acentos), escolher formas que
  sobrevivam (não depender de acento/til).

### 4. PROCESSO (como a qualidade é garantida)
- **Metadados reais por linha** (`speaker`, situação/`tone_register`, `risk_level`) — **não
  auto-default**: são o que dirige a QA contextual.
- **Risco calibrado** (data-driven): identidade dupla, comédia, 1ª menção de lore, spoiler →
  `risk ≥ high` → **back-translation obrigatória** (06b/07).
- **Camadas de verificação:** linter determinístico de naturalidade (pega o sistemático barato) →
  revisão contextual por personagem × situação (06b/07) → **aprovação humana**.
- **Fluxo:** a IA **PROPÕE** no `translation_plan.json` (`base_translation`) → o usuário **APROVA**
  (`approved_translations.csv`) → o script **APLICA** (Passo 08). A IA nunca edita dados/binário à mão.
- **Decisões não-óbvias** vão para o `decision_log.md`.

---

## CHECKLIST (executar antes de aceitar/aprovar uma linha ou lote)

```
□ Voz: registro/léxico batem com o perfil do falante? (high → toda linha)
□ Identidade/spoiler: nada revelado antes do reveal_timing?
□ Lore: termos do glossário na forma certa?
□ Situação: traduzida pela emoção/intenção da cena? interjeição localizada?
□ Naturalidade: um nativo lê NESTA situação e entende fácil? (senão, revisa)
□ Conector: cabe/translitera sem virar outra coisa? tokens preservados?
□ Risco: se ≥ high, passou por back-translation?
□ Não satisfez algo acima? → sinalizar em QA/risk_notes (não entregar às cegas).
```

---

## ONDE A CARTA É APLICADA

| Passo | Como a Carta entra |
|-------|--------------------|
| 05 planejamento | metadados reais por linha (speaker/situação/risco) — base da QA |
| 06 tradução | traduzir conforme as 4 diretrizes + checklist por linha |
| 06b micro-QA | naturalidade contextual + interjeições + back-translation de alto risco |
| 06c correção | só toca o que a QA/linter reprovou; re-valida |
| 07 QA final | adequação contextual por arco de personagem; spoilers cross-segmento |
| 08 reinserção | respeita a restrição do conector (byte/translit.); LLM só no resíduo |

> Ferramentas de apoio: `framework/validation/validate.py` (schemas/invariantes) e
> `framework/validation/naturalness_lint.py` (smells de naturalidade). Ambas são Input Gates executáveis.

## 2. Regras do conector / projeto
- Token de quebra de linha: `\n` (literal; preservar EXATO, mesma posicao).
- Tokens de formatacao a preservar verbatim: ['{W75}', '{W80}', '{W10}', '{COLOR}', '{END}'] + padroes ['\\{c-?\\d*\\}'].
- Convencao de linha de sistema: all_caps.
- Restricao de comprimento: {'mode': 'byte_space', 'dialogue_max_pct': 140, 'ui_max_pct': 110} (orcamento em bytes por linha — ver coluna byte_budget).
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acento→ASCII) 
  -> escolha formas que sobrevivam a transliteracao (nao dependa de acento/til p/ sentido).

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |

## 4. Vozes presentes
### Garota — criticality: high
- Registro: cotidiano gentil; cuidadora.
- Características: acolhe sem pressionar ("Apenas relaxe..."); curiosa mas paciente; calor humano.
- Red flags: soar fria, clínica ou impaciente; formalidade excessiva.
### Haku — criticality: high
- Haku (protagonista, narração 1ª pessoa) — `voice_criticality: high`. Predomina nas 2 cenas:
### Homem — criticality: high
- Registro: enigmático, profético, frio.
- Características: sentenças curtas e definitivas; duplo sentido ("um mundo totalmente novo te espera"); ambiguidade ameaçadora.
- Red flags: soar caloroso/paternal; resolver a ambiguidade (a fala deve permanecer dúbia).
### Protagonista — criticality: high
- Registro: confuso, desorientado, semi-consciente.
- Características: frases quebradas por reticências; perguntas curtas ("Quem... é você...?"); pouca pontuação forte.
- Red flags: falas fluentes/articuladas demais; perder o tom de torpor; pontuação "limpa" que apaga a fragmentação.

## 5. Decisoes relevantes (do decision_log)
- **Opcode de RÓTULO DE FALANTE `53 00` + reconcile de speaker (data-driven)** [universal]: **Problema:** in-game, o rótulo de falante aparecia em **inglês** ("Girl") mesmo com a tradução ("Garota") aprovada e gravada. RE: o nome do falante usa um **2º opcode de ponteiro, `53 00`** (mesmo formato file-relativo do `50 00` de diálogo), que o conector ignorava. Resultado: "Girl"→"Garota"
- **Gate de charset pt-BR — método e veredito** [universal]: **Decisão tomada:** Marcar `target_charset_supported: likely` e exigir confirmação in-game antes de produção. **Alternativas consideradas:** - Confirmar por presença no texto-fonte — **insuficiente**: o fonte é inglês e quase não usa acentos (só `õ` e `À` aparecem em texto real).
- **Anomalia 0x33f9 — texto PT/EN corrompido na fonte** [universal]: **Decisão tomada:** Marcar a linha `0x33f9` como anomalia de fonte (não traduzir em cima do lixo; tratar como linha de sistema reescrita). **Razão:** A string original já vem misturada PT/EN e truncada ("...SISTEMAS AM . RESTARTING...") no próprio jogo. Não é erro de extração. O conector deve sinali
- **Charset — transliteração na gravação (gate FALHOU)** [universal]: **Decisão tomada:** Marcar `target_charset_supported: false` e **transliterar** (acento → ASCII) na gravação do binário. A tradução canônica (`approved_translations.csv`, `translation_plan.json`) **mantém os acentos** (correta para QA/revisão); apenas os bytes escritos no jogo são dobrados para ASCI
- **Escopo cognitivo — 75 → 1025 linhas (cenas 11_01 + 11_02); reveal de Haku in-corpus** [universal]: **Decisão tomada:** Re-rodar o pipeline completo em escala (cenas 11_01 + 11_02 = 1025 linhas). Novos termos canônicos: **Kuon** (nome revelado em 0x108db), **Haku** (nome dado ao protagonista em 0x12668 — reveal agora **dentro do corpus**), **Tatari** (criatura imortal), **aperyu** (vestimenta), **
- **CORREÇÃO CRÍTICA — ponteiros são FILE-RELATIVOS, não absolutos** [universal]: **Decisão tomada:** Ao investigar o "opcode de início de bloco", descobri que **`50 00`+uint32 é um offset RELATIVO ao início do arquivo (Pack)**, não absoluto. Endereço da string = `file_start_do_site + uint32`. Prova: dos ~47k sites, **42.101** só apontam para string como file-relativos vs **63** 

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Phew. I'm out of the bath.` -> `Ufa. Saí do banho.` (Haku, 11_11)
- `I return to the room, relaxed and refreshed, to find\n` -> `Volto pro quarto, relaxado e renovado, e encontro\n` (Haku, 11_11)
- `Kuon sitting in the corner with her back turned.` -> `a Kuon sentada no canto, de costas.` (Haku, 11_11)
- `Kuon, I'm out...?` -> `Kuon, eu já saí...?` (Haku, 11_11)
- `What's going on?` -> `O que tá acontecendo?` (Haku, 11_11)
- `No reply. She doesn't seem to even notice me.` -> `Sem resposta. Ela nem parece me notar.` (Haku, 11_11)
- `When I approach, I can faintly hear her muttering to\n` -> `Quando me aproximo, ouço fraquinho ela murmurando\n` (Haku, 11_11)
- `herself, gaze vacant...` -> `pra si mesma, o olhar vazio...` (Haku, 11_11)
- `It sounds like she's saying "thwap, thwap," but it's\n` -> `Parece que ela tá dizendo "pá, pá", mas é\n` (Haku, 11_11)
- `difficult to make out.` -> `difícil de entender.` (Haku, 11_11)
- `...Kuon?` -> `...Kuon?` (Haku, 11_11)
- `I put my hand on her shoulder.` -> `Ponho a mão no ombro dela.` (Haku, 11_11)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `Whoa!` -> `Uou!` (Haku, 11_11)
- `G-Geez, don't surprise me like that.` -> `C-Caramba, não me assusta desse jeito.` (Kuon, 11_11)
- `I-I'm the one who's surprised, here. Did something\n` -> `E-Eu é que me assustei, aqui. Aconteceu\n` (Haku, 11_11)
- `happen?` -> `alguma coisa?` (Haku, 11_11)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `You had a thousand-yard stare and you were mumbling\n` -> `Você tava com o olhar perdido e murmurando\n` (Haku, 11_11)
- `like you'd seen something awful. What happened?` -> `como se tivesse visto algo horrível. O que houve?` (Haku, 11_11)
- `Why are you averting your eyes?` -> `Por que você tá desviando o olhar?` (Haku, 11_11)
- `I-I'm not... averting them...` -> `N-Não tô... desviando...` (Kuon, 11_11)
- `Despite her words, Kuon is, in fact, looking entirely\n` -> `Apesar do que diz, a Kuon está, de fato, olhando\n` (Haku, 11_11)
- `to one side of me.` -> `totalmente pro lado de mim.` (Haku, 11_11)
- `No, you definitely are.` -> `Não, você tá sim.` (Haku, 11_11)
- `I round on her and place myself in front of her\n` -> `Me viro pra ela e me ponho na frente dos\n` (Haku, 11_11)
- `eyes, but she turns away again.` -> `olhos dela, mas ela desvia de novo.` (Haku, 11_11)
- `And your face is bright red. What's the deal?` -> `E sua cara tá vermelhíssima. Que que tá rolando?` (Haku, 11_11)
- `I lean down and put my face right in front of hers. She still\n` -> `Me abaixo e ponho meu rosto bem na frente do dela. Ela ainda\n` (Haku, 11_11)
- `refuses to make eye contact.` -> `se recusa a fazer contato visual.` (Haku, 11_11)
- `Instead, her cheeks turn even redder--and her eyes\n` -> `Em vez disso, as bochechas dela ficam mais vermelhas--e os olhos\n` (Haku, 11_11)
- `are bloodshot like she's been drinking.` -> `injetados como se ela tivesse bebido.` (Haku, 11_11)
- `Your eyes are red, too. Are you feeling...?` -> `Seus olhos também estão vermelhos. Você tá se sentindo...?` (Haku, 11_11)
- `*WHUMF--*` -> `*BAM--*` (Kuon, 11_11)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Out of the blue, Kuon grabs me and tosses me away\n` -> `Do nada, a Kuon me agarra e me arremessa\n` (Haku, 11_11)
- `like a ragdoll with that casual strength of hers.` -> `como um boneco de pano, com aquela força casual dela.` (Haku, 11_11)
- `*FLUMP*` -> `*PUF*` (Haku, 11_11)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `My body flies through the air, landing squarely\n` -> `Meu corpo voa pelo ar e cai bem\n` (Haku, 11_11)
- `on the bed.` -> `em cima da cama.` (Haku, 11_11)
- `Wh-What are you d--` -> `Q-Que que você tá faz--` (Haku, 11_11)
- `You needn't concern yourself with me. More\n` -> `Você não precisa se preocupar comigo. Mais\n` (Kuon, 11_11)
- `importantly, why didn't you tell me about THIS?` -> `importante: por que você não me contou sobre ISSO?` (Kuon, 11_11)
- `Kuon pulls my feet upward and inspects the soles.` -> `A Kuon levanta meus pés e inspeciona as solas.` (Haku, 11_11)
- `Tell you what?` -> `Te contar o quê?` (Haku, 11_11)
- `Was there something I needed to tell her...?` -> `Tinha algo que eu precisava contar pra ela...?` (Haku, 11_11)
- `Kuon ignores the question, frowning deeply at the\n` -> `A Kuon ignora a pergunta, franzindo a testa diante\n` (Haku, 11_11)
- `sight of my ruined soles.` -> `das minhas solas arruinadas.` (Haku, 11_11)
- `If you'd said something, I wouldn't have made you\n` -> `Se você tivesse falado algo, eu não teria te feito\n` (Kuon, 11_11)
- `strain yourself this much today.` -> `se esforçar tanto hoje.` (Kuon, 11_11)
- `...What!? I did tell you. Repeatedly.` -> `...Quê!? Eu te contei. Várias vezes.` (Haku, 11_11)
- `I run through the day's events in my mind...` -> `Repasso os acontecimentos do dia na cabeça...` (Haku, 11_11)
- `I did gripe and complain, several times... I...` -> `Eu reclamei e resmunguei, várias vezes... Eu...` (Haku, 11_11)
- `Actually, come to think of it, I never complained\n` -> `Na verdade, pensando bem, eu nunca reclamei\n` (Haku, 11_11)
- `aloud--I only ever muttered my gripes...` -> `em voz alta--só resmunguei as queixas...` (Haku, 11_11)
- `Hold still for a moment.` -> `Fica parado um instante.` (Kuon, 11_11)
- `Kuon takes several small pills from the pouch at\n` -> `A Kuon pega várias pílulas pequenas da bolsa na\n` (Haku, 11_11)
- `her waist and puts them into her mouth, chewing.` -> `cintura, põe na boca e mastiga.` (Haku, 11_11)
- `What's that?` -> `O que é isso?` (Haku, 11_08)
- `Kuon only smiles, taking the chewed-up glob from her\n` -> `A Kuon só sorri, tirando a pasta mastigada da\n` (Haku, 11_11)
- `mouth and smearing it on my feet.` -> `boca e passando nos meus pés.` (Haku, 11_11)
- `This will sting a bit.` -> `Isso vai arder um pouquinho.` (Kuon, 11_11)
- `I can't quite figure out why, but a chill rolls down\n` -> `Não sei bem por quê, mas um arrepio desce\n` (Haku, 11_11)
- `my spine at the sight of that cheerful smile.` -> `pela minha espinha ao ver aquele sorriso alegre.` (Haku, 11_11)
- `*Rub, slip, slather--*` -> `*Esfrega, escorrega, lambuza--*` (Haku, 11_11)
- `Kuon's fingers work the substance into my feet,\n` -> `Os dedos da Kuon trabalham a substância nos meus pés,\n` (Haku, 11_11)
- `paying special attention to where the skin peels.` -> `com atenção especial onde a pele descasca.` (Haku, 11_11)
- `Is she applying a salve, or something? It's\n` -> `Ela tá passando uma pomada, ou algo assim? Tá\n` (Haku, 11_11)
- `definitely stinging...` -> `ardendo, com certeza...` (Haku, 11_11)
- `Ow, hhhh--` -> `Ai, hhhh--` (Haku, 11_11)
- `Maybe stinging isn't quite the word. It itches and\n` -> `Talvez arder não seja bem a palavra. Coça e\n` (Haku, 11_11)
- `tingles more than it stings.` -> `formiga mais do que arde.` (Haku, 11_11)
- `It's probably the medicine, but suddenly, I can't\n` -> `Deve ser o remédio, mas de repente não\n` (Haku, 11_11)
- `contain the urge to scratch my itching feet--` -> `consigo conter a vontade de coçar os pés--` (Haku, 11_11)
- `But when I reach for them, Kuon bats my hand away.` -> `Mas quando vou neles, a Kuon dá um tapa na minha mão.` (Haku, 11_11)
- `Ah, ah, no touching. It'll be uncomfortable, but its\n` -> `Ah, ah, sem tocar. Vai ser incômodo, mas a\n` (Kuon, 11_11)
- `effectiveness is second to none!` -> `eficácia é imbatível!` (Kuon, 11_11)
- `Arrrgh, so THAT'S why she was smiling. God, it\n` -> `Arrrgh, então é por ISSO que ela tava sorrindo. Deus, como\n` (Haku, 11_11)
- `itches, it itches--` -> `coça, como coça--` (Haku, 11_11)
- `That should just about do it. It'll settle down\n` -> `Acho que é isso. Vai acalmar\n` (Kuon, 11_11)
- `after a while, so hang in there until then, OK?` -> `daqui a pouco, então aguenta firme até lá, tá?` (Kuon, 11_11)
- `Still smiling, Kuon expertly wraps my feet in tight\n` -> `Ainda sorrindo, a Kuon enfaixa meus pés com perícia,\n` (Haku, 11_11)
- `bandages, sealing in the salve.` -> `apertado, selando a pomada.` (Haku, 11_11)
- `And for good measure...` -> `E só por garantia...` (Kuon, 11_11)
- `Kuon sets an odd, legged jar next to my pillow.` -> `A Kuon põe um pote esquisito, com pés, ao lado do meu travesseiro.` (Haku, 11_11)
- `Hmhm. Just watch.` -> `Hmhm. Só observa.` (Kuon, 11_11)
- `She removes the jar's perforated lid. The inside\n` -> `Ela tira a tampa furada do pote. O interior\n` (Haku, 11_11)
- `looks to be packed with white ash.` -> `parece cheio de cinza branca.` (Haku, 11_11)
- `Then, nestling a small piece of charcoal in the ash,\n` -> `Então, acomodando um pedacinho de carvão na cinza,\n` (Haku, 11_11)
- `she lights it and waits for a moment...` -> `ela o acende e espera um instante...` (Haku, 11_11)
- `Finally, another small, black pill goes on top of\n` -> `Por fim, outra pílula pequena e preta vai em cima\n` (Haku, 11_11)
- `the lit charcoal.` -> `do carvão aceso.` (Haku, 11_11)
- `A moment passes, and sweet, fruity scents begin to\n` -> `Passa um instante, e aromas doces e frutados começam a\n` (Haku, 11_11)
- `waft from the jar, filling my nostrils.` -> `subir do pote, enchendo minhas narinas.` (Haku, 11_11)
- `An incense burner, huh...` -> `Um incensário, é...` (Haku, 11_11)
- `Exactly.` -> `Exato.` (Kuon, 11_11)
- `This particular incense is a blend of aromatic and\n` -> `Esse incenso é uma mistura de ervas aromáticas e\n` (Kuon, 11_11)
- `pain-relieving herbs.` -> `analgésicas.` (Kuon, 11_11)
- `It'll relieve your fatigue and pain, and it has\n` -> `Vai aliviar sua fadiga e dor, e tem\n` (Kuon, 11_11)
- `ancillary properties that facilitate sleep, I think?` -> `propriedades secundárias que facilitam o sono, eu acho?` (Kuon, 11_11)
- `Even as Kuon speaks, I can feel the fragrance\n` -> `Enquanto a Kuon fala, já sinto a fragrância\n` (Haku, 11_11)
- `soothing my mind and dulling my pain.\n` -> `acalmando minha mente e amenizando a dor.\n` (Haku, 11_11)
- `I feel... light.` -> `Me sinto... leve.` (Haku, 11_11)
- `Oh... oh, that's... blissful...` -> `Ah... ah, isso é... uma bênção...` (Haku, 11_11)
- `I think the concentration might be a little high.\n` -> `Acho que a concentração pode estar um pouco alta.\n` (Kuon, 11_11)
- `Are you feeling OK? You don't feel ill?` -> `Você está bem? Não tá passando mal?` (Kuon, 11_11)
- `No, I'm... I'm good... I'm really, REALLY good...` -> `Não, eu... tô bem... Tô muito, MUITO bem...` (Haku, 11_11)
- `Getting... sleepy... Eyelids... heavy...` -> `Ficando... com sono... Pálpebras... pesadas...` (Haku, 11_11)
- `Now, are you feeling pain anywhere else? ...Haku?\n` -> `E então, tá sentindo dor em mais algum lugar? ...Haku?\n` (Kuon, 11_11)
- `Haku, that's my bed, you can't sl--` -> `Haku, essa é a minha cama, você não pode dor--` (Kuon, 11_11)
- `I'm sinking...` -> `Tô afundando...` (Haku, 11_11)
- `My consciousness... swirling away into oblivion...` -> `Minha consciência... se esvaindo no esquecimento...` (Haku, 11_11)
- `Hey, Haku. Hey--\n` -> `Ei, Haku. Ei--\n` (Kuon, 11_11)
- `...Sheesh.` -> `...Aff.` (Kuon, 11_11)
- `I picked up quite a burden out there, didn't I...?` -> `Acabei pegando um belo de um fardo por aí, né...?` (Kuon, 11_11)
- `But I suppose that's... my...` -> `Mas suponho que isso seja... o meu...` (Kuon, 11_11)
- `What is... this music?` -> `Que... música é essa?` (Haku, 11_11)
- `It's... soft. And a little nostalgic...` -> `É... suave. E um pouco nostálgica...` (Haku, 11_11)
- `Where have I... heard it before? I feel like I've...` -> `Onde eu... já ouvi isso? Sinto que eu já...` (Haku, 11_11)
- `Some... where...` -> `Em algum... lugar...` (Haku, 11_11)
**Voz estabelecida dos falantes (amostra):**
- Haku: `Geez...! Too bright out here...` -> `Aff...! Claridade demais aqui fora...`
- Haku: `Well, guess the sun still rises no matter where\n` -> `Enfim, o sol nasce em qualquer lugar, pelo visto\n`
- Haku: `I am. Still... What am I supposed to do now...?` -> `Pois é. Mesmo assim... O que é que eu faço agora...?`
- Protagonista: `Ngh... ghh...` -> `Nnh... aagh...`
- Protagonista: `Nn...\n` -> `Nnh...\n`
- Protagonista: `It's... warm...?` -> `Está... quente...?`

## 7. Linhas a traduzir
| offset | byte_budget | source |
|---|---|---|
| 0x24a8f | 26 | Phew. I'm out of the bath. |
| 0x24aae | 54 | I return to the room, relaxed and refreshed, to find\n |
| 0x24ae5 | 48 | Kuon sitting in the corner with her back turned. |
| 0x24b16 | 17 | Kuon, I'm out...? |
| 0x24b28 | 16 | What's going on? |
| 0x24b39 | 45 | No reply. She doesn't seem to even notice me. |
| 0x24b67 | 54 | When I approach, I can faintly hear her muttering to\n |
| 0x24b9e | 23 | herself, gaze vacant... |
| 0x24bb6 | 54 | It sounds like she's saying "thwap, thwap," but it's\n |
| 0x24bed | 22 | difficult to make out. |
| 0x24c04 | 8 | ...Kuon? |
| 0x24c0d | 30 | I put my hand on her shoulder. |
| 0x24c2c | 4 | Eep! |
| 0x24c31 | 5 | Whoa! |
| 0x24c37 | 36 | G-Geez, don't surprise me like that. |
| 0x24c5c | 52 | I-I'm the one who's surprised, here. Did something\n |
| 0x24c91 | 7 | happen? |
| 0x24c99 | 4 | Huh? |
| 0x24c9e | 53 | You had a thousand-yard stare and you were mumbling\n |
| 0x24cd4 | 47 | like you'd seen something awful. What happened? |
| 0x24d04 | 31 | Why are you averting your eyes? |
| 0x24d24 | 29 | I-I'm not... averting them... |
| 0x24d42 | 55 | Despite her words, Kuon is, in fact, looking entirely\n |
| 0x24d7a | 18 | to one side of me. |
| 0x24d8d | 23 | No, you definitely are. |
| 0x24da5 | 49 | I round on her and place myself in front of her\n |
| 0x24dd7 | 31 | eyes, but she turns away again. |
| 0x24df7 | 45 | And your face is bright red. What's the deal? |
| 0x24e25 | 63 | I lean down and put my face right in front of hers. She still\n |
| 0x24e65 | 28 | refuses to make eye contact. |
| 0x24e82 | 52 | Instead, her cheeks turn even redder--and her eyes\n |
| 0x24eb7 | 39 | are bloodshot like she's been drinking. |
| 0x24edf | 43 | Your eyes are red, too. Are you feeling...? |
| 0x24f0b | 9 | *WHUMF--* |
| 0x24f15 | 4 | Wh-- |
| 0x24f1a | 51 | Out of the blue, Kuon grabs me and tosses me away\n |
| 0x24f4e | 49 | like a ragdoll with that casual strength of hers. |
| 0x24f80 | 7 | *FLUMP* |
| 0x24f88 | 7 | Urgh... |
| 0x24f90 | 49 | My body flies through the air, landing squarely\n |
| 0x24fc2 | 11 | on the bed. |
| 0x24fce | 19 | Wh-What are you d-- |
| 0x24fe2 | 44 | You needn't concern yourself with me. More\n |
| 0x2500f | 47 | importantly, why didn't you tell me about THIS? |
| 0x2503f | 49 | Kuon pulls my feet upward and inspects the soles. |
| 0x25071 | 14 | Tell you what? |
| 0x25080 | 44 | Was there something I needed to tell her...? |
| 0x250ad | 51 | Kuon ignores the question, frowning deeply at the\n |
| 0x250e1 | 25 | sight of my ruined soles. |
| 0x250fb | 51 | If you'd said something, I wouldn't have made you\n |
| 0x2512f | 32 | strain yourself this much today. |
| 0x25150 | 37 | ...What!? I did tell you. Repeatedly. |
| 0x25176 | 44 | I run through the day's events in my mind... |
| 0x251a3 | 47 | I did gripe and complain, several times... I... |
| 0x251d3 | 51 | Actually, come to think of it, I never complained\n |
| 0x25207 | 40 | aloud--I only ever muttered my gripes... |
| 0x25230 | 24 | Hold still for a moment. |
| 0x25249 | 50 | Kuon takes several small pills from the pouch at\n |
| 0x2527c | 48 | her waist and puts them into her mouth, chewing. |
| 0x252ad | 12 | What's that? |
| 0x252ba | 54 | Kuon only smiles, taking the chewed-up glob from her\n |
| 0x252f1 | 33 | mouth and smearing it on my feet. |
| 0x25313 | 22 | This will sting a bit. |
| 0x2532a | 54 | I can't quite figure out why, but a chill rolls down\n |
| 0x25361 | 45 | my spine at the sight of that cheerful smile. |
| 0x2538f | 22 | *Rub, slip, slather--* |
| 0x253a6 | 49 | Kuon's fingers work the substance into my feet,\n |
| 0x253d8 | 49 | paying special attention to where the skin peels. |
| 0x2540a | 45 | Is she applying a salve, or something? It's\n |
| 0x25438 | 22 | definitely stinging... |
| 0x2544f | 10 | Ow, hhhh-- |
| 0x2545a | 52 | Maybe stinging isn't quite the word. It itches and\n |
| 0x2548f | 28 | tingles more than it stings. |
| 0x254ac | 51 | It's probably the medicine, but suddenly, I can't\n |
| 0x254e0 | 45 | contain the urge to scratch my itching feet-- |
| 0x2550e | 50 | But when I reach for them, Kuon bats my hand away. |
| 0x25541 | 54 | Ah, ah, no touching. It'll be uncomfortable, but its\n |
| 0x25578 | 32 | effectiveness is second to none! |
| 0x25599 | 48 | Arrrgh, so THAT'S why she was smiling. God, it\n |
| 0x255ca | 19 | itches, it itches-- |
| 0x255de | 49 | That should just about do it. It'll settle down\n |
| 0x25610 | 47 | after a while, so hang in there until then, OK? |
| 0x25640 | 53 | Still smiling, Kuon expertly wraps my feet in tight\n |
| 0x25676 | 31 | bandages, sealing in the salve. |
| 0x25696 | 23 | And for good measure... |
| 0x256ae | 47 | Kuon sets an odd, legged jar next to my pillow. |
| 0x256de | 17 | Hmhm. Just watch. |
| 0x256f0 | 50 | She removes the jar's perforated lid. The inside\n |
| 0x25723 | 34 | looks to be packed with white ash. |
| 0x25746 | 54 | Then, nestling a small piece of charcoal in the ash,\n |
| 0x2577d | 39 | she lights it and waits for a moment... |
| 0x257a5 | 51 | Finally, another small, black pill goes on top of\n |
| 0x257d9 | 17 | the lit charcoal. |
| 0x257eb | 52 | A moment passes, and sweet, fruity scents begin to\n |
| 0x25820 | 39 | waft from the jar, filling my nostrils. |
| 0x25848 | 25 | An incense burner, huh... |
| 0x25862 | 8 | Exactly. |
| 0x2586b | 52 | This particular incense is a blend of aromatic and\n |
| 0x258a0 | 21 | pain-relieving herbs. |
| 0x258b6 | 49 | It'll relieve your fatigue and pain, and it has\n |
| 0x258e8 | 52 | ancillary properties that facilitate sleep, I think? |
| 0x2591d | 47 | Even as Kuon speaks, I can feel the fragrance\n |
| 0x2594d | 39 | soothing my mind and dulling my pain.\n |
| 0x25975 | 16 | I feel... light. |
| 0x25986 | 31 | Oh... oh, that's... blissful... |
| 0x259a6 | 51 | I think the concentration might be a little high.\n |
| 0x259da | 39 | Are you feeling OK? You don't feel ill? |
| 0x25a02 | 49 | No, I'm... I'm good... I'm really, REALLY good... |
| 0x25a34 | 40 | Getting... sleepy... Eyelids... heavy... |
| 0x25a5d | 51 | Now, are you feeling pain anywhere else? ...Haku?\n |
| 0x25a91 | 35 | Haku, that's my bed, you can't sl-- |
| 0x25ab5 | 14 | I'm sinking... |
| 0x25ac4 | 50 | My consciousness... swirling away into oblivion... |
| 0x25af7 | 18 | Hey, Haku. Hey--\n |
| 0x25b0a | 10 | ...Sheesh. |
| 0x25b15 | 50 | I picked up quite a burden out there, didn't I...? |
| 0x25b48 | 29 | But I suppose that's... my... |
| 0x25b66 | 22 | What is... this music? |
| 0x25b7d | 39 | It's... soft. And a little nostalgic... |
| 0x25ba5 | 52 | Where have I... heard it before? I feel like I've... |
| 0x25bda | 16 | Some... where... |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_11.json` com a forma:
```json
{ "lines": {
  "<offset>": {"speaker": "...", "tone_register": "...", "intent": "...",
    "risk_level": "low|medium|high|critical", "risk_notes": "(se >= medium)",
    "t": "<traducao pt-BR canonica, com acentos, com o token de quebra exato>"},
  ... 1 entrada por offset acima ...
} }
```
Regras: cobrir TODOS os offsets; preservar o token de quebra; risco >= medium exige
risk_notes; interjeicoes/onomatopeias = traducao (localizar, nao copiar). O build_plan
valida cobertura/tokens/risk_notes; linhas risco>=high passam por back-translation.
