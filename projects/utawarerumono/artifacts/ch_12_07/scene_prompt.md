# Cena ch_12_07 — pacote de traducao (124 linhas)

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
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| Cohort | Organizacao | Coorte | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Ukon | Personagem | Ukon | manter_original | major |

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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Ukon** (major): Traduza as falas de/sobre Ukon como o personagem 'Ukon' por si so. NAO insinue outra identidade, patente oculta ou disfarce. Mantenha qualquer ambiguidade do original.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
**Voz estabelecida dos falantes (amostra):**
- Haku: `Geez...! Too bright out here...` -> `Aff...! Claridade demais aqui fora...`
- Haku: `Well, guess the sun still rises no matter where\n` -> `Enfim, o sol nasce em qualquer lugar, pelo visto\n`
- Haku: `I am. Still... What am I supposed to do now...?` -> `Pois é. Mesmo assim... O que é que eu faço agora...?`
- Protagonista: `Where... am I?` -> `Onde... estou?`
- Protagonista: `No one else around, or...?` -> `Não tem ninguém... ou...?`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
- Protagonista: `Unh... urgh...` -> `Nnh... argh...`
- Maroro: `Master Ukon! It pleaseth my heart to report my\n` -> `Mestre Ukon! É com grande satisfação que reporto que meus\n`
- Maroro: `belongings lay duly unpack'd, and await porters.` -> `meus pertences estão desfeitos e aguardam os carregadores.`
- Ukon: `Ah. Well done.` -> `Ah. Bom trabalho.`
- Maroro: `I am VERY tired, sir. Naught more now do I desire\n` -> `Estou MUITO cansado, senhor. Nada mais desejo agora\n`
- Ukon: `Really, Maroro? Seems like you get tired quicker\n` -> `É sério, Maroro? Parece que você se cansa mais rápido\n`
- Ukon: `and quicker these days...` -> `a cada dia que passa...`
- Homem: `Inside your dream.` -> `No seu sonho.`
- Homem: `We have enchanted you with a spell that will help\n` -> `Lançamos sobre você um feitiço que irá ajudá-lo\n`
- Homem: `you become stronger in sleep, as requested, Master.` -> `a ficar mais forte enquanto dorme, como pedido, Mestre.`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x38bfe | 50 | We make good time cutting through the mountains,\n |
| 0x38c31 | 41 | following the path up from the village... |
| 0x38c5b | 47 | As we forge deeper in, the light from the sun\n |
| 0x38c8b | 47 | overhead dims, filtered by dense canopy growth. |
| 0x38cbb | 50 | One of the men Kuon had treated the night before\n |
| 0x38cee | 50 | walks at the head of the company, leading the way. |
| 0x38d21 | 49 | He still has his wounded arm in a sling, but he\n |
| 0x38d53 | 39 | seems to have recovered enough to walk. |
| 0x38d7b | 51 | Ukon walks right behind him, whistling to himself\n |
| 0x38daf | 11 | cheerfully. |
| 0x38dbb | 54 | Several villagers armed with farm tools follow after\n |
| 0x38df2 | 50 | them, joined by Ukon's more properly equipped men. |
| 0x38e25 | 53 | The whole assembled group chats idly as we push on,\n |
| 0x38e5b | 45 | hardly anyone showing even a hint of fatigue. |
| 0x38e89 | 46 | Hhngh. Where do these people get their energy? |
| 0x38eb8 | 52 | Kuon's even been stopping to gather herbs and fruit. |
| 0x38eed | 53 | Keeping an eye out for ingredients for her medicine\n |
| 0x38f23 | 49 | on top of hiking doesn't seem to faze her at all. |
| 0x38f55 | 52 | Meanwhile, my feet feel like they're about to fall\n |
| 0x38f8a | 41 | off. I'm gonna collapse if this keeps up. |
| 0x38fb4 | 48 | You all right, kid? You're breathing awful hard. |
| 0x38fe5 | 46 | Anyone would be, after walking all this way... |
| 0x39014 | 24 | Really? This is nothing. |
| 0x3902d | 13 | Ukon's Cohort |
| 0x3903b | 51 | Hey, kid, that cutie's gonna be disappointed with\n |
| 0x3906f | 26 | you if you talk like that. |
| 0x3908a | 51 | That's right! A real man sucks it up and goes for\n |
| 0x390be | 6 | broke! |
| 0x390c5 | 7 | Urgh... |
| 0x390cd | 51 | I can't even work up the energy for a comeback as\n |
| 0x39101 | 42 | the members of the hunting party tease me. |
| 0x3912c | 53 | Well, this place is practically a backyard to folks\n |
| 0x39162 | 49 | who live here. You're prolly just not used to it. |
| 0x39194 | 50 | Guess it can't be helped. Go hitch a ride on the\n |
| 0x391c7 | 50 | back of the cart. Can't have you collapsing on us. |
| 0x391fa | 52 | He's trying to be subtle about looking out for me,\n |
| 0x3922f | 48 | but honestly, I don't care about my dignity now. |
| 0x39260 | 21 | Thanks. I'll do that. |
| 0x39276 | 37 | I hop on the cart without hesitation. |
| 0x3929c | 7 | GAHOO!? |
| 0x392a4 | 9 | What th-- |
| 0x392ae | 48 | As I climb into the cart, my foot presses into\n |
| 0x392df | 27 | something... gross-feeling. |
| 0x392fb | 27 | Wh-What did I just step on? |
| 0x39317 | 52 | I look down to find Maroro, pale in the face, in a\n |
| 0x3934c | 15 | miserable heap. |
| 0x3935c | 49 | He looks so sickly, I can even tell through his\n |
| 0x3938e | 43 | thick makeup he's not holding up very well. |
| 0x393ba | 28 | M-Maroro? Hey, what's wrong? |
| 0x393d7 | 29 | I hurriedly pull him upright. |
| 0x393f5 | 16 | U-Urk... hurk... |
| 0x39406 | 26 | Are you OK? What happened? |
| 0x39421 | 51 | Oh, alack! Oh, by every god, m-my stomach. How it\n |
| 0x39455 | 48 | yearns to shatter its f-fetters... Woe! Oh, woe! |
| 0x3948a | 25 | I let go of him promptly. |
| 0x394a4 | 6 | Gyeh!? |
| 0x394ab | 33 | Hwup--aahh. I can finally rest... |
| 0x394cd | 52 | Wh-What ill consideration, to so brusquely release\n |
| 0x39502 | 50 | me! Maroro 'tis a man besieged, so sayeth--heURGH? |
| 0x39535 | 51 | Ye gods, b-but how these backwood trails do chafe\n |
| 0x39569 | 53 | the spirit and vex the bowels! Pity this poor soul... |
| 0x3959f | 49 | This is why I told you to go easy on the booze.\n |
| 0x395d1 | 50 | You'd feel better if you walked instead of rode,\n |
| 0x39604 | 7 | y'know. |
| 0x3960c | 45 | Ukon's tone is exasperated, to say the least. |
| 0x3963a | 51 | Mayhaps, friend Ukon, mayhaps--but to debase mine\n |
| 0x3966e | 42 | own self so ignobly? U-Unthinkable 'tis... |
| 0x39699 | 49 | Oh, for the love of--is this your damn nobleman\n |
| 0x396cb | 12 | thing again? |
| 0x396d8 | 53 | Just so! No man of highest birth should fall so low\n |
| 0x3970e | 50 | as to walk upon the dirt, like a vagrant baseborn. |
| 0x39741 | 52 | I-It matters--hURGgh--m-matters not the cost! Even\n |
| 0x39776 | 52 | fallen from it; grace, we musn't f-forget gra--HURG? |
| 0x397ab | 51 | ...Yeah, I'm gonna go ahead and say nobody really\n |
| 0x397df | 44 | thinks you're all that "graceful" right now. |
| 0x3980c | 54 | To s-sully my very name with such v-vulgar behavior,\n |
| 0x39843 | 28 | perish the thoAURGH--HRF--!! |
| 0x39860 | 13 | *Splatter*... |
| 0x3986e | 43 | Sorry, kid, but could you take care of him? |
| 0x3989a | 47 | What, take care of THIS? How am I supposed to-- |
| 0x398ca | 51 | As long as you're taking it easy in the cart, the\n |
| 0x398fe | 53 | least you could do is look after the poor guy, right? |
| 0x39934 | 7 | Nngh... |
| 0x3993c | 54 | With that, Ukon moves up to the front of the company\n |
| 0x39973 | 34 | again, leaving Maroro in my hands. |
| 0x39996 | 13 | Bleeuurrgh... |
| 0x399a4 | 50 | I thought I'd finally be able to relax, but now... |
| 0x399d7 | 52 | If I abandon Maroro to his fate, everyone will see\n |
| 0x39a0c | 26 | me as heartless, no doubt. |
| 0x39a27 | 52 | Reluctantly, I sit down behind the hungover Maroro\n |
| 0x39a5c | 17 | and rub his back. |
| 0x39a6e | 52 | All right. Since it's come to this, just... get it\n |
| 0x39aa3 | 45 | all out of your system. Do what you gotta do. |
| 0x39ad1 | 29 | I thank thee, dear freEURGH-- |
| 0x39aef | 10 | Why me...? |
| 0x39afa | 45 | He looks terrible. Here, Haku--give him this. |
| 0x39b28 | 52 | Kuon approaches with pills in one hand and a flask\n |
| 0x39b5d | 13 | in the other. |
| 0x39b6b | 54 | This one is for hangovers, and this one's for motion\n |
| 0x39ba2 | 41 | sickness. And there's water in the flask. |
| 0x39bcc | 32 | Thanks. You gonna stay and help? |
| 0x39bed | 54 | Kuon smiles and steps sharply away without answering\n |
| 0x39c24 | 13 | the question. |
| 0x39c32 | 45 | Oh, I don't want the flask b--I mean, um...\n |
| 0x39c60 | 21 | You can hold onto it. |
| 0x39c76 | 25 | ...I should have figured. |
| 0x39c90 | 51 | I glance around for help, but everyone looks away\n |
| 0x39cc4 | 10 | in unison. |
| 0x39ccf | 50 | Urk... M-Master... Haku, was it? Truly, thou art\n |
| 0x39d02 | 47 | a{W370}--HEURGH--man of g-great kindness, and\n |
| 0x39d32 | 13 | untold HURK-- |
| 0x39d40 | 50 | Maroro tightly clasps my hands, tears in his eyes. |
| 0x39d73 | 48 | You, uh... You don't have to thank me, just...\n |
| 0x39da4 | 39 | point your mouth the other way. Please. |
| 0x39dcc | 50 | Pray dispense--HURP--with thy humility, O master\n |
| 0x39dff | 56 | H-Haku! Ne'er deep enough shall my gr--{W360}AGHtitude-- |
| 0x39e38 | 49 | Th-That's nice, but will you listen to what I'm\n |
| 0x39e6a | 7 | saying? |
| 0x39e72 | 51 | Without a thought unto thyself dost thou stoop to\n |
| 0x39ea6 | 52 | aid poor Maroro! Truly, thou art a bosom frienNGH--! |
| 0x39edb | 51 | What did I do to deserve this...? How did it come\n |
| 0x39f0f | 8 | to this? |
| 0x39f18 | 54 | I groan at the absurdity of the world, rocked by the\n |
| 0x39f4f | 21 | rumbling of the cart. |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_07.json` com a forma:
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
