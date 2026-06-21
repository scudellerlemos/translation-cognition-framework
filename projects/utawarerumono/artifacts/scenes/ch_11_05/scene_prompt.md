# Cena ch_11_05 — pacote de traducao (52 linhas)

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
- **pt-BR MODERNO (registro do jogador de hoje):** preferir a forma que um jogador BR atual usaria, não
  a "correta-mas-arcaica/truncada". Dois erros recorrentes pegos em QA in-game:
  - **Resposta de NOME** (`I'm…`/`My name's…`/`I am…` quando responde "qual seu nome?") → **"Meu nome é…"
    / "Eu me chamo…" / "Sou o(a)…"** conforme a voz. NUNCA "Eu sou" seco — refere-se a estado, soa
    truncado para apresentação.
  - **Léxico arcaico/erudito** (ex.: "ruminar"/"Rumino" por "pensar/refletir") só quando a VOZ do
    personagem pede; senão, a palavra que o público entende **de imediato**.
- **Restrição do conector:** se há transliteração na gravação (fonte sem acentos), escolher formas que
  sobrevivam (não depender de acento/til).
- **Preservar ambiguidade (anti-spoiler por construção):** quando o pacote da cena traz um *controle de
  spoiler* (fato ainda não revelado), a tradução **não pode resolver** o que o original deixa em aberto.
  Atenção especial ao **gênero em pt-BR**: o EN/JP esconde gênero/identidade que o pt-BR forçaria a
  concordância (`cansad{o/a}`, `el{e/a}`, `um{/a}`). Se o falante/referente é de identidade oculta,
  **escolher construção neutra** (reformular; evitar adjetivo/artigo de gênero) e marcar `risk ≥ high`.
  Nunca antecipar nome, relação ou identidade futura.

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
□ pt-BR moderno: forma que um jogador de HOJE usaria? (nome → "Meu nome é/Eu me chamo", não "Eu sou"; sem arcaísmo gratuito)
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
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/evidence/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acent
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

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
### Maroro — criticality: high
- Registro: erudito cômico, pomposo e arcaico; bajulador do Ukon; alívio cômico.
- Características: fala arcaica/empolada (equivalente a "vós/peço-vos/meus olhos não me enganam") + gag de cicio (s→sh, ex.: "SHEEKETH"/"shir"); melodramático; gruda no Haku como "benfeitor".
- Red flags: perder o arcaísmo ou o cicio (são a piada); soar moderno/neutro; explicar a comédia. Manter o contraste entre a pompa do vocabulário e a fragilidade do personagem.
### Oshtor — criticality: high
- Oshtor — `voice_criticality: high`. = Ukon até 13_08 (ver spoiler_ledger). Registro formal, nobre, comedido; General da Direita. Antes do reveal, traduzir como o mercenário "Ukon" (espirituoso, informal) — NÃO antecipar a pompa de general
### Protagonista — criticality: high
- Registro: confuso, desorientado, semi-consciente.
- Características: frases quebradas por reticências; perguntas curtas ("Quem... é você...?"); pouca pontuação forte.
- Red flags: falas fluentes/articuladas demais; perder o tom de torpor; pontuação "limpa" que apaga a fragmentação.
### Ukon — criticality: high
- Registro: guerreiro carismático, espirituoso, caloroso e informal; líder nato que trata Haku como um irmão mais novo.
- Características: desembaraçado, brincalhão, generoso; fala direta e cativante; autoridade leve (lidera a Coorte) sem arrogância.
- Red flags: soar rígido/formal/militar demais (a graça é justamente o contraste com a patente); frieza. SPOILER: não deixar a tradução insinuar a identidade verdadeira — no cap.12 ele é só "Ukon".

## 5. Decisoes relevantes (do decision_log)
- **Opcode de RÓTULO DE FALANTE `53 00` + reconcile de speaker (data-driven)** [universal]: **Problema:** in-game, o rótulo de falante aparecia em **inglês** ("Girl") mesmo com a tradução ("Garota") aprovada e gravada. RE: o nome do falante usa um **2º opcode de ponteiro, `53 00`** (mesmo formato file-relativo do `50 00` de diálogo), que o conector ignorava. Resultado: "Girl"→"Garota"
- **Gate de charset pt-BR — método e veredito** [universal]: **Decisão tomada:** Marcar `target_charset_supported: likely` e exigir confirmação in-game antes de produção. **Alternativas consideradas:** - Confirmar por presença no texto-fonte — **insuficiente**: o fonte é inglês e quase não usa acentos (só `õ` e `À` aparecem em texto real).
- **Anomalia 0x33f9 — texto PT/EN corrompido na fonte** [universal]: **Decisão tomada:** Marcar a linha `0x33f9` como anomalia de fonte (não traduzir em cima do lixo; tratar como linha de sistema reescrita). **Razão:** A string original já vem misturada PT/EN e truncada ("...SISTEMAS AM . RESTARTING...") no próprio jogo. Não é erro de extração. O conector deve sinali
- **Charset — transliteração na gravação (gate FALHOU)** [universal]: **Decisão tomada:** Marcar `target_charset_supported: false` e **transliterar** (acento → ASCII) na gravação do binário. A tradução canônica (`approved_translations.csv`, `translation_plan.json`) **mantém os acentos** (correta para QA/revisão); apenas os bytes escritos no jogo são dobrados para ASCI
- **Escopo cognitivo — 75 → 1025 linhas (cenas 11_01 + 11_02); reveal de Haku in-corpus** [universal]: **Decisão tomada:** Re-rodar o pipeline completo em escala (cenas 11_01 + 11_02 = 1025 linhas). Novos termos canônicos: **Kuon** (nome revelado em 0x108db), **Haku** (nome dado ao protagonista em 0x12668 — reveal agora **dentro do corpus**), **Tatari** (criatura imortal), **aperyu** (vestimenta), **
- **CORREÇÃO CRÍTICA — ponteiros são FILE-RELATIVOS, não absolutos** [universal]: **Decisão tomada:** Ao investigar o "opcode de início de bloco", descobri que **`50 00`+uint32 é um offset RELATIVO ao início do arquivo (Pack)**, não absoluto. Endereço da string = `file_start_do_site + uint32`. Prova: dos ~47k sites, **42.101** só apontam para string como file-relativos vs **63** 
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Hahh... hah... phew...` -> `Haah... haah... ufa...` (Haku, 11_05)
- `I-Is that... all of them?` -> `E-Esses... eram todos?` (Haku, 11_05)
- `Kuon closes her eyes, straining her big ears as she\n` -> `A Kuon fecha os olhos, aguçando as orelhas grandes enquanto\n` (Haku, 11_05)
- `listens.` -> `escuta.` (Haku, 11_05)
- `...Yes... I don't think there are any more nearby.` -> `...Sim... acho que não tem mais nenhum por perto.` (Kuon, 11_05)
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
- `I sag to the ground. ` -> `Eu desabo no chão. ` (Haku, 11_05)
- `Thought... I was gonna die there...` -> `Achei... que ia morrer ali...` (Haku, 11_05)
- `Er... well done...?` -> `Ahn... mandou bem...?` (Kuon, 11_05)
- `Kuon offers me some kind of flask, seeing me\n` -> `A Kuon me oferece uma espécie de cantil, me vendo\n` (Haku, 11_05)
- `seated and trying to catch my breath.` -> `sentado tentando recuperar o fôlego.` (Haku, 11_05)
- `I take it with a grumble. Maybe I'm sulking\n` -> `Pego resmungando. Talvez eu esteja de bico\n` (Haku, 11_05)
- `a little.` -> `um pouco.` (Haku, 11_05)
- `It wasn't anything like you said!` -> `Não foi nada do que você disse!` (Haku, 11_05)
- `What I said?` -> `O que eu disse?` (Kuon, 11_05)
- `Just a second ago! All that "oh, just wave a\n` -> `Agora há pouco! Aquele "ah, é só balançar um\n` (Haku, 11_05)
- `stick around, they'll scatter."` -> `graveto que eles se espalham."` (Haku, 11_05)
- `So much for scattering! They tried to maul me!\n` -> `Espalharam que nada! Eles tentaram me despedaçar!\n` (Haku, 11_05)
- `They didn't care about the damn stick--I could've\n` -> `Eles nem ligaram pro maldito graveto--eu podia ter\n` (Haku, 11_05)
- `died!` -> `morrido!` (Haku, 11_05)
- `But... I was telling the truth. ` -> `Mas... eu falei a verdade. ` (Kuon, 11_05)
- `They try to ambush people, and they attack in\n` -> `Eles tentam emboscar as pessoas e atacam em\n` (Kuon, 11_05)
- `packs, but they're really not that big of a deal.` -> `bando, mas eles não são grande coisa de verdade.` (Kuon, 11_05)
- `That... wasn't a big deal?` -> `Aquilo... não foi grande coisa?` (Haku, 11_05)
- `Kuon glances at me dubiously.` -> `A Kuon me lança um olhar de dúvida.` (Haku, 11_05)
- `Haku, maybe you're a bit, ah...` -> `Haku, talvez você seja um pouquinho, ahn...` (Kuon, 11_05)
- `Ah, no, never mind. I think.` -> `Ah, não, deixa pra lá. Acho eu.` (Kuon, 11_05)
- `Not sure what she was about to say, but I'll act\n` -> `Não sei o que ela ia dizer, mas vou fingir\n` (Haku, 11_05)
- `like I didn't hear. I've got a good guess, anyway...` -> `que não ouvi. Mas dá pra imaginar, de todo jeito...` (Haku, 11_05)
- `You're still recovering, after all... Not quite\n` -> `Você ainda está se recuperando, afinal... Não\n` (Kuon, 11_05)
- `back to normal. And you seemed unused to all this.` -> `totalmente recuperado. E parecia sem prática nisso tudo.` (Kuon, 11_05)
- `Well, perhaps all you need is a bit of practice,\n` -> `Bom, talvez você só precise de um pouco de prática,\n` (Kuon, 11_05)
- `and you'll be driving them off easily.` -> `e vai enxotá-los fácil.` (Kuon, 11_05)
- `Like I'd ever want to go through that again.` -> `Como se eu fosse querer passar por isso de novo.` (Haku, 11_05)
- `All right, we should get back on the road soon.` -> `Certo, a gente devia voltar pra estrada logo.` (Kuon, 11_05)
- `What, already!? Can't we just rest a little\n` -> `Quê, já!? A gente não pode descansar um pouco\n` (Haku, 11_05)
- `longer...?` -> `mais...?` (Haku, 11_05)
- `My legs are weak, and they're shaking slightly.` -> `Minhas pernas estão bambas, tremendo de leve.` (Haku, 11_05)
- `I wouldn't mind, but if we take much longer, the\n` -> `Por mim tudo bem, mas se a gente demorar muito, o\n` (Kuon, 11_05)
- `sun will set. Are you OK with that?` -> `sol vai se pôr. Você topa isso?` (Kuon, 11_05)
- `It'd mean we'd be traveling in darkness, and\n` -> `Ia significar viajar no escuro, e\n` (Kuon, 11_05)
- `there's a good chance we'd run into more of\n` -> `tem boa chance da gente esbarrar em mais\n` (Kuon, 11_05)
- `them.` -> `deles.` (Kuon, 11_05)
- `I peer skyward, but... the sun is nowhere near\n` -> `Olho pro céu, mas... o sol não está nem perto\n` (Haku, 11_05)
- `the horizon.` -> `do horizonte.` (Haku, 11_05)
- `And this village is... pretty close by,\n` -> `E essa vila está... bem pertinho,\n` (Haku, 11_05)
- `you said?` -> `você disse?` (Haku, 11_05)
- `Right. Not much farther now, I think.` -> `Isso. Não falta muito agora, acho.` (Kuon, 11_05)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Kuon meets my eyes with a look of polite confusion.` -> `A Kuon encontra meu olhar com uma confusão educada.` (Haku, 11_05)
- `She seems... honest enough... It'll be fine.\n` -> `Ela parece... bastante sincera... Vai dar certo.\n` (Haku, 11_05)
- `Just a little farther... that's all...` -> `Só mais um pouquinho... é só isso...` (Haku, 11_05)
**Voz estabelecida dos falantes (amostra):**
- Protagonista: `Ngh... ghh...` -> `Nnh... aagh...`
- Protagonista: `Nn...\n` -> `Nnh...\n`
- Protagonista: `It's... warm...?` -> `Está... quente...?`
- Haku: `Urgh...` -> `Argh...`
- Haku: `Right?` -> `né?`
- Haku: `Nn...` -> `Nnh...`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
- Maroro: `Master Ukon! It pleaseth my heart to report my\n` -> `Mestre Ukon! É com grande satisfação que reporto que meus\n`
- Maroro: `belongings lay duly unpack'd, and await porters.` -> `meus pertences estão desfeitos e aguardam os carregadores.`
- Ukon: `Ah. Well done.` -> `Ah. Bom trabalho.`
- Maroro: `I am VERY tired, sir. Naught more now do I desire\n` -> `Estou MUITO cansado, senhor. Nada mais desejo agora\n`
- Ukon: `Really, Maroro? Seems like you get tired quicker\n` -> `É sério, Maroro? Parece que você se cansa mais rápido\n`
- Ukon: `and quicker these days...` -> `a cada dia que passa...`
- Homem: `The way you were carrying on, you got us all\n` -> `Do jeito que você estava, nos deixou todos\n`
- Homem: `anxious, too!` -> `ansiosos também!`
- Homem: `Wahahahaha!!` -> `Wahahahaha!!`
- Oshtor: `Enter.` -> `Entre.`
- Oshtor: `How good of you to come.` -> `Que bom que vieram.`
- Oshtor: `Lord Haku. Lady Kuon. Thank you for your aid\n` -> `Senhor Haku. Senhora Kuon. Obrigado pela ajuda\n`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x16e45 | 22 | Hahh... hah... phew... |
| 0x16e5c | 25 | I-Is that... all of them? |
| 0x16e76 | 53 | Kuon closes her eyes, straining her big ears as she\n |
| 0x16eac | 8 | listens. |
| 0x16eb5 | 50 | ...Yes... I don't think there are any more nearby. |
| 0x16ee8 | 7 | O-OK... |
| 0x16ef0 | 21 | I sag to the ground.  |
| 0x16f06 | 35 | Thought... I was gonna die there... |
| 0x16f2a | 19 | Er... well done...? |
| 0x16f3e | 46 | Kuon offers me some kind of flask, seeing me\n |
| 0x16f6d | 37 | seated and trying to catch my breath. |
| 0x16f93 | 45 | I take it with a grumble. Maybe I'm sulking\n |
| 0x16fc1 | 9 | a little. |
| 0x16fcb | 33 | It wasn't anything like you said! |
| 0x16fed | 12 | What I said? |
| 0x16ffa | 46 | Just a second ago! All that "oh, just wave a\n |
| 0x17029 | 31 | stick around, they'll scatter." |
| 0x17049 | 48 | So much for scattering! They tried to maul me!\n |
| 0x1707a | 51 | They didn't care about the damn stick--I could've\n |
| 0x170ae | 5 | died! |
| 0x170b4 | 32 | But... I was telling the truth.  |
| 0x170d5 | 47 | They try to ambush people, and they attack in\n |
| 0x17105 | 49 | packs, but they're really not that big of a deal. |
| 0x17137 | 26 | That... wasn't a big deal? |
| 0x17152 | 29 | Kuon glances at me dubiously. |
| 0x17170 | 31 | Haku, maybe you're a bit, ah... |
| 0x17190 | 28 | Ah, no, never mind. I think. |
| 0x171ad | 50 | Not sure what she was about to say, but I'll act\n |
| 0x171e0 | 52 | like I didn't hear. I've got a good guess, anyway... |
| 0x17215 | 49 | You're still recovering, after all... Not quite\n |
| 0x17247 | 50 | back to normal. And you seemed unused to all this. |
| 0x1727a | 50 | Well, perhaps all you need is a bit of practice,\n |
| 0x172ad | 38 | and you'll be driving them off easily. |
| 0x172d4 | 44 | Like I'd ever want to go through that again. |
| 0x17301 | 47 | All right, we should get back on the road soon. |
| 0x17331 | 45 | What, already!? Can't we just rest a little\n |
| 0x1735f | 10 | longer...? |
| 0x1736a | 47 | My legs are weak, and they're shaking slightly. |
| 0x1739a | 50 | I wouldn't mind, but if we take much longer, the\n |
| 0x173cd | 35 | sun will set. Are you OK with that? |
| 0x173f1 | 46 | It'd mean we'd be traveling in darkness, and\n |
| 0x17420 | 45 | there's a good chance we'd run into more of\n |
| 0x1744e | 5 | them. |
| 0x17454 | 48 | I peer skyward, but... the sun is nowhere near\n |
| 0x17485 | 12 | the horizon. |
| 0x17492 | 41 | And this village is... pretty close by,\n |
| 0x174bc | 9 | you said? |
| 0x174c6 | 37 | Right. Not much farther now, I think. |
| 0x174f0 | 6 | ...Hm? |
| 0x174f7 | 51 | Kuon meets my eyes with a look of polite confusion. |
| 0x1752b | 46 | She seems... honest enough... It'll be fine.\n |
| 0x1755a | 38 | Just a little farther... that's all... |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_05.json` com a forma:
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
