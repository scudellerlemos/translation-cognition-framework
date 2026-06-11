# Cena ch_13_02 — pacote de traducao (800 linhas)

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
| amam | Item | amam | manter_original | none |
| aperyu | Item | aperyu | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Cohort | Organizacao | Coorte | traduzir | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
| woptor | Criatura | woptor | manter_original | none |

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
### Rulutieh — criticality: medium
- Rulutieh — `voice_criticality: medium`. Princesa tímida e gentil; hesitante (gagueja quando nervosa: "P-Princesa..."), educada, se anima ao falar de arte/BL. Não soar arrogante apesar de princesa.
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
- **Ukon** (major): ANTES de 13_08: trate Ukon como mercenario espirituoso por si so. NAO insinue patente, nobreza, vinculo imperial nem o nome 'Oshtor'. Preserve a ambiguidade do original (que usa 'Ukon').

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `*Poke-poke-poke*...` -> `*Cutuca-cutuca-cutuca*...` (sistema, 13_01)
- `*Squish-squish-squish--*` -> `*Amassa-amassa-amassa--*` (sistema, 13_01)
- `*Poke-poke-poke--*\n` -> `*Cutuca-cutuca-cutuca--*\n` (sistema, 13_01)
- `thing.` -> `coisa.` (Haku, 12_03)
- `*Squish, squish*...` -> `*Amassa, amassa*...` (sistema, 13_01)
- `*Poke, poke*...` -> `*Cutuca, cutuca*...` (sistema, 13_01)
- `Kuon...` -> `Kuon...` (Kuon, root)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `Wh--` -> `Q--` (Haku, 11_07)
- `What the HELL is going on?` -> `O que DIABOS está acontecendo?` (Haku, 13_01)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `*WHUMP*` -> `*BAM*` (Haku, 11_07)
- `Why me...?` -> `Por que eu...?` (Haku, 12_07)
- `*TUG-TUG-TUG--*` -> `*PUXA-PUXA-PUXA--*` (sistema, 13_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Whoa!` -> `Uou!` (Haku, 11_11)
- `yourself.` -> `abalado.` (Kuon, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `What's this?` -> `O que é isso?` (Haku, 12_08)
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Ukon's Cohorts` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Yessir!` -> `Sim!` (Coorte de Ukon, 12_04)
- `Hm...?` -> `Hum...?` (Kuon, root)
- `but...` -> `mas...` (Kuon, 12_16)
- `Ah, thank you.` -> `Ah, obrigado.` (Haku, 13_01)
- `here...` -> `o fim...` (Haku, 12_03)
- `about her.` -> `nela.` (Haku, 13_01)
- `A joke?` -> `Piada?` (Kuon, 11_09)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
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
- Homem: `The way you were carrying on, you got us all\n` -> `Do jeito que você estava, nos deixou todos\n`
- Homem: `anxious, too!` -> `ansiosos também!`
- Homem: `Wahahahaha!!` -> `Wahahahaha!!`
- Rulutieh: `Oh, pardon me.` -> `Ah, com licença.`
- Rulutieh: `I'm... sorry about, um...` -> `Eu... desculpe, é que...`
- Rulutieh: `That's a relief... Come on, Cocopo. We'll just be\n` -> `Ainda bem... Vamos, Cocopo. Só estamos\n`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x5c47b | 51 | The caravan rolls lazily along the mountain path... |
| 0x5c4af | 24 | Mm. It's a nice day out. |
| 0x5c4c8 | 52 | The wagon is jostling and my butt hurts from every\n |
| 0x5c4fd | 45 | bump in the road, but I'm getting used to it. |
| 0x5c52b | 51 | I've got time to just lay back and leisurely gaze\n |
| 0x5c55f | 11 | at the sky. |
| 0x5c56b | 45 | The wind's calm, too. It really is peaceful\n |
| 0x5c599 | 10 | weather... |
| 0x5c5a4 | 54 | If only we weren't traveling with extremely valuable\n |
| 0x5c5db | 20 | bandit-magnet cargo. |
| 0x5c5f0 | 5 | Hurk. |
| 0x5c5f6 | 54 | Or this guy lying in the corner of the wagon reeking\n |
| 0x5c62d | 32 | to high heaven, for that matter. |
| 0x5c64e | 14 | *Poke-poke*... |
| 0x5c65d | 19 | *Poke-poke-poke*... |
| 0x5c671 | 25 | *Squish-squish-squish*... |
| 0x5c68f | 24 | *Squish-squish-squish--* |
| 0x5c6a8 | 18 | *Poke-poke-poke--* |
| 0x5c6bb | 20 | Mysterious duo right |
| 0x5c6d0 | 19 | Mysterious duo left |
| 0x5c6e4 | 34 | *Squish-poke-squish-poke-squish--* |
| 0x5c707 | 47 | Meanwhile, I've been unsuccessfully trying to\n |
| 0x5c737 | 46 | ignore my more, uh... immediate circumstances. |
| 0x5c766 | 49 | What exactly are you guys trying to accomplish,\n |
| 0x5c798 | 5 | here? |
| 0x5c79e | 52 | The Mystery Twins have me sandwiched between them,\n |
| 0x5c7d3 | 38 | and have yet to stop poking my cheeks. |
| 0x5c7fa | 49 | I've tried talking to them a few times now, but\n |
| 0x5c82c | 49 | never to any avail. They're just gonna do their\n |
| 0x5c85e | 6 | thing. |
| 0x5c865 | 48 | I've given up on getting anything out of them.\n |
| 0x5c896 | 26 | This is downright bizarre. |
| 0x5c8b1 | 21 | *Squish, squish*...\n |
| 0x5c8c7 | 15 | *Poke, poke*... |
| 0x5c8d7 | 51 | Really, I could probably just drive them off, but\n |
| 0x5c90b | 33 | I can't... quite bring myself to? |
| 0x5c92d | 53 | I don't wanna scare them, or make them timid around\n |
| 0x5c963 | 16 | me or something. |
| 0x5c974 | 48 | With my discomfort rising, I glance around the\n |
| 0x5c9a5 | 30 | caravan for some kind of help. |
| 0x5c9c4 | 53 | Maroro's... not gonna be of much use. Not that he'd\n |
| 0x5c9fa | 36 | be helpful if he were awake, anyway. |
| 0x5ca1f | 50 | And Ukon's... riding at the head of the caravan.\n |
| 0x5ca52 | 32 | Probably best not to bother him. |
| 0x5ca73 | 7 | Kuon... |
| 0x5ca7b | 36 | I quickly scan the caravan for Kuon. |
| 0x5caa0 | 6 | ♪~\n |
| 0x5cab2 | 48 | That ridiculously huge bird is trundling along\n |
| 0x5cae3 | 26 | right next to the caravan. |
| 0x5cafe | 52 | On its back, Kuon and Rulutieh chat happily. Seems\n |
| 0x5cb33 | 46 | they're having fun opening up to each other... |
| 0x5cb62 | 50 | That's nice to see, but they're so wrapped up in\n |
| 0x5cb95 | 50 | their conversation, they probably won't notice m-- |
| 0x5cbc8 | 32 | Kuon suddenly glances toward me. |
| 0x5cbe9 | 41 | As she notices my gaze, she smiles at me. |
| 0x5cc13 | 4 | Ku-- |
| 0x5cc18 | 52 | --and then she immediately turns back to Rulutieh,\n |
| 0x5cc4d | 21 | and resumes chatting. |
| 0x5cc6a | 51 | The enormous bird, however, croons at me in a bid\n |
| 0x5cc9e | 14 | for attention. |
| 0x5ccad | 33 | ...Gonna pretend I didn't see it. |
| 0x5cccf | 53 | ...Hold on. Is everyone else just pretending not to\n |
| 0x5cd05 | 45 | notice what's happening to me with these two? |
| 0x5cd33 | 52 | There are ankuam walking alongside the caravan, of\n |
| 0x5cd68 | 48 | course, but not one of them is looking this way. |
| 0x5cd99 | 49 | In fact, it seems like they're doing everything\n |
| 0x5cdcb | 40 | they can to KEEP from looking over here. |
| 0x5cdf4 | 50 | Some are cracking lame, forced jokes, or talking\n |
| 0x5ce27 | 44 | about love affairs, or just staring ahead... |
| 0x5ce54 | 47 | They seem to be keeping a watchful eye on our\n |
| 0x5ce84 | 48 | surroundings, rather than on the caravan itself. |
| 0x5ceb5 | 48 | Why exactly do these two get left to their own\n |
| 0x5cee6 | 8 | devices? |
| 0x5ceef | 28 | *Squish, squish, squish--*\n |
| 0x5cf0c | 14 | *Poke, poke--* |
| 0x5cf1b | 47 | Now that I pay attention to it, it seems like\n |
| 0x5cf4b | 47 | everyone's keeping their eyes off them pretty\n |
| 0x5cf7b | 13 | deliberately. |
| 0x5cf89 | 10 | I give up. |
| 0x5cf94 | 49 | I give up, already. It's not like they're doing\n |
| 0x5cfc6 | 51 | any harm, and if nobody is gonna call them on it... |
| 0x5cffa | 50 | I guess the company doesn't really consider them\n |
| 0x5d02d | 42 | a problem? Doesn't seem like it, anyway... |
| 0x5d058 | 50 | I bet they pull mischief like this all the time,\n |
| 0x5d08b | 38 | and I'm the only one who doesn't--Huh? |
| 0x5d0b2 | 20 | Hurk... Gh--G-Guh... |
| 0x5d0c7 | 51 | As Maroro thrashes in his agonized sleep, he tugs\n |
| 0x5d0fb | 43 | on the cloth that covers the wagon's cargo. |
| 0x5d127 | 52 | The corner of a bizarre object peeks out, catching\n |
| 0x5d15c | 9 | my eye... |
| 0x5d166 | 28 | Pottery? No... Not quite...? |
| 0x5d183 | 52 | It has a smooth surface like fine china, decorated\n |
| 0x5d1b8 | 24 | with intricate patterns. |
| 0x5d1d1 | 51 | Awkward, forced-together boxes and cylinders make\n |
| 0x5d205 | 36 | up its shape, strange and irregular. |
| 0x5d22a | 27 | No, definitely not pottery. |
| 0x5d246 | 32 | It's almost like some kind of... |
| 0x5d267 | 14 | Mysterious duo |
| 0x5d276 | 40 | Suddenly, the poking at my cheeks stops. |
| 0x5d29f | 50 | Momentarily free and curious to know the cargo's\n |
| 0x5d2d2 | 50 | contents, I reach for the barely-clinging cloth... |
| 0x5d305 | 11 | *Tug-tug--* |
| 0x5d311 | 4 | Huh? |
| 0x5d316 | 44 | Something pulls my sleeve back, stopping me. |
| 0x5d343 | 51 | The mysterious duo have each stopped poking me to\n |
| 0x5d377 | 26 | grab hold of my sleeves... |
| 0x5d392 | 8 | Wh-What? |
| 0x5d39b | 53 | They're not pulling too hard, but it's pretty clear\n |
| 0x5d3d1 | 46 | they're trying to yank me back from the cargo. |
| 0x5d400 | 42 | Are you trying to tell me not to touch it? |
| 0x5d42b | 50 | They seem to give me a subtle nod in quiet unison. |
| 0x5d45e | 19 | ...All right, then. |
| 0x5d472 | 51 | I'm not sure what the issue is, but if they don't\n |
| 0x5d4a6 | 47 | want me to see it, I guess it's not a big deal. |
| 0x5d4d6 | 19 | *Stroke, stroke*... |
| 0x5d4ea | 4 | Wh-- |
| 0x5d4ef | 52 | Instead of poking, now they've started stroking my\n |
| 0x5d524 | 43 | head as if to tell me I'm being a good boy. |
| 0x5d550 | 26 | What the hell is going on? |
| 0x5d56b | 51 | At least we were able to actually communicate for\n |
| 0x5d59f | 47 | once. Oh, well. Not gonna dwell on it any more. |
| 0x5d5cf | 53 | All right, everyone. This is as far as we go today.\n |
| 0x5d605 | 51 | Sentry squad, set up the watch and prepare to camp. |
| 0x5d639 | 6 | Ngh... |
| 0x5d640 | 21 | I sit up and stretch. |
| 0x5d656 | 22 | Must've drifted off... |
| 0x5d66d | 51 | I rouse myself and have a look around, getting my\n |
| 0x5d6a1 | 9 | bearings. |
| 0x5d6ab | 52 | Those two... aren't here. I guess they wandered off. |
| 0x5d6e0 | 53 | The caravan is parked in an open space off the side\n |
| 0x5d716 | 46 | of the road, fenced-off and protected. A camp? |
| 0x5d745 | 49 | Yeah, looks like we're here for the night. What\n |
| 0x5d777 | 15 | should I do...? |
| 0x5d787 | 50 | ...I guess I should just lie low until it's time\n |
| 0x5d7ba | 7 | to eat. |
| 0x5d7c2 | 51 | An unskilled, unseasoned person would just get in\n |
| 0x5d7f6 | 43 | everyone's way with chores, after all. Yep. |
| 0x5d822 | 50 | Here, Haku. As long as you're up, would you mind\n |
| 0x5d855 | 20 | taking care of this? |
| 0x5d86a | 50 | Kuon descends on me before I can see her coming,\n |
| 0x5d89d | 41 | smiling sweetly and holding out a bucket. |
| 0x5d8c7 | 54 | There's a well over there, so get the cookpot filled\n |
| 0x5d8fe | 14 | up, would you? |
| 0x5d90d | 52 | Then the washtub after that, and THEN all the jars\n |
| 0x5d942 | 24 | we've collected. Got it? |
| 0x5d95b | 49 | Remember, he who doesn't work doesn't eat. Good\n |
| 0x5d98d | 5 | luck! |
| 0x5d993 | 7 | ...Urk. |
| 0x5e9fc | 47 | Ukon calls out to me as I emerge from the tent. |
| 0x5ea2c | 49 | Hey, kid. If you're free, d'you mind tending to\n |
| 0x5ea5e | 21 | the steeds for a bit? |
| 0x5ea74 | 47 | Tend to the steeds? I don't mind, but... What\n |
| 0x5eaa4 | 31 | exactly does that, um, involve? |
| 0x5eac4 | 49 | Nothing big. Just give 'em some feed, groom 'em\n |
| 0x5eaf6 | 10 | for a bit. |
| 0x5eb01 | 6 | Groom? |
| 0x5eb08 | 49 | Yeah, you give their skin a good scrubbing with\n |
| 0x5eb3a | 38 | this brush. It's not real complicated. |
| 0x5eb61 | 53 | Ukon holds up a large scrubbing brush, wiggling the\n |
| 0x5eb97 | 25 | bristles in my direction. |
| 0x5ebb1 | 50 | It feels good to them, when you brush with this.\n |
| 0x5ebe4 | 16 | Keeps 'em happy. |
| 0x5ebf5 | 50 | They're critical to the caravan. If we treat 'em\n |
| 0x5ec28 | 44 | well, they'll respond in kind and work hard. |
| 0x5ec55 | 39 | Just in exchange for a good scrub, huh. |
| 0x5ec7d | 53 | You'll understand a little better if you ever start\n |
| 0x5ecb3 | 49 | riding steeds, kid. They're special, woptors are. |
| 0x5ece5 | 48 | Yeah, all right. If that's all, then I'll help\n |
| 0x5ed16 | 35 | out. I don't wanna be a freeloader. |
| 0x5ed3a | 46 | I appreciate it, kid. The steeds are hitched\n |
| 0x5ed69 | 49 | outside of camp over there. I'll leave the rest\n |
| 0x5ed9b | 7 | to you. |
| 0x5eda3 | 50 | Ukon hands me the brush, waves his hand as if to\n |
| 0x5edd6 | 49 | formally confer the duty on me, then turns to go. |
| 0x5ee08 | 50 | No matter how I look at it, these guys look more\n |
| 0x5ee3b | 52 | like ostriches than what the word "steed" conjures\n |
| 0x5ee70 | 11 | in my head. |
| 0x5ee7c | 49 | As I approach the woptors hitched to the fence,\n |
| 0x5eeae | 32 | they begin to stir, noticing me. |
| 0x5eecf | 50 | Easy, there. I'll feed you in a sec, so hold it,\n |
| 0x5ef02 | 9 | will you? |
| 0x5ef0c | 14 | Mysterious duo |
| 0x5ef1f | 4 | Wh-- |
| 0x5ef24 | 48 | As if from nowhere, those two wrapped in their\n |
| 0x5ef55 | 45 | aperyu appear crouching next to the feed bin. |
| 0x5ef83 | 44 | Wh--Geez, you two. Don't scare me like that. |
| 0x5efb0 | 49 | They both look up at me and tilt their heads in\n |
| 0x5efe2 | 40 | unison, as if to ask "Did we scare you?" |
| 0x5f00b | 53 | They must understand what I've been saying to them,\n |
| 0x5f041 | 28 | to react like that... right? |
| 0x5f05e | 51 | Anybody'd be surprised if you just appear without\n |
| 0x5f092 | 25 | a word and stare at them. |
| 0x5f0ac | 49 | They look at each other, then back to me, their\n |
| 0x5f0de | 36 | heads tilting as if to ask "really?" |
| 0x5f103 | 51 | They're totally synced. That's some coordination... |
| 0x5f137 | 51 | Their precise, perfectly-matched movements almost\n |
| 0x5f16b | 49 | make me want to ask if they're street performers. |
| 0x5f19d | 21 | So, what do you want? |
| 0x5f1b3 | 50 | They share another look, then turn back to stare\n |
| 0x5f1e6 | 18 | inscrutably at me. |
| 0x5f1f9 | 48 | If you want to watch, do as you please, I guess. |
| 0x5f22a | 49 | Not gonna ruin my day. If I stand here figuring\n |
| 0x5f25c | 50 | out what they want, the steeds will never get fed. |
| 0x5f28f | 52 | I fish what looks like some kind of vegetable from\n |
| 0x5f2c4 | 48 | the feed tub, offering it to the nearest woptor. |
| 0x5f2f5 | 5 | Steed |
| 0x5f2fb | 32 | *KROMPCH* *KRUNCH-MUNCH-MUNCH--* |
| 0x5f31c | 20 | Whoa, geez. Scary... |
| 0x5f331 | 50 | Maybe it's because they're just hungry, but man,\n |
| 0x5f364 | 49 | they're really going for it. I could've lost my\n |
| 0x5f396 | 17 | fingers just now. |
| 0x5f3a8 | 51 | Not really something I'm eager to have happen, so\n |
| 0x5f3dc | 42 | maybe if I just toss their food to them... |
| 0x5f407 | 26 | *KRUMPCH, KRONCH, MUNCH--* |
| 0x5f422 | 7 | *CRASH* |
| 0x5f42a | 15 | KWEH! KWEEEHHH! |
| 0x5f43a | 49 | Settle down, guys, there's plenty to go around... |
| 0x5f46c | 21 | KWEEEHHH! KWEEEHHH!!! |
| 0x5f482 | 23 | *CRASH--THUNK--WHUMP--* |
| 0x5f49a | 46 | It's hopeless. Their eyes are bloodshot with\n |
| 0x5f4c9 | 48 | excitement at being fed. This could get out of\n |
| 0x5f4fa | 13 | hand quickly. |
| 0x5f508 | 48 | I glance down at the twins, still crouching by\n |
| 0x5f539 | 16 | the tub of feed. |
| 0x5f54a | 27 | I guess I have no choice... |
| 0x5f566 | 31 | Hey, you two ever fed a woptor? |
| 0x5f586 | 51 | They slowly turn to stare at me, then shake their\n |
| 0x5f5ba | 6 | heads. |
| 0x5f5c1 | 45 | Nngh... That's OK, I guess. Care to help me\n |
| 0x5f5ef | 44 | feed these guys? Just try not to get bitten. |
| 0x5f61c | 46 | They each nod, then reach into the feed bin,\n |
| 0x5f64b | 44 | holding their offerings out for the woptors. |
| 0x5f678 | 49 | Urk, they're gonna lose their fingers like that-- |
| 0x5f6aa | 27 | *Crunch, crunch, crunch*... |
| 0x5f6c6 | 50 | ...Or so I thought, but the woptors calm down in\n |
| 0x5f6f9 | 48 | short order, eating peacefully from their hands. |
| 0x5f72a | 47 | As the woptors eat, the duo gently stroke the\n |
| 0x5f75a | 44 | sides of the steeds' heads, soothing them... |
| 0x5f787 | 52 | They said they've never fed woptors, but they seem\n |
| 0x5f7bc | 40 | awfully familiar with--Yikes! Close one. |
| 0x5f7e5 | 51 | With me, they're devouring their food with enough\n |
| 0x5f819 | 49 | force to pull my fingers off with it. What gives? |
| 0x5f84b | 52 | It doesn't seem like they hate me, they're just...\n |
| 0x5f880 | 12 | oddly eager? |
| 0x5f88d | 52 | That stupid fat bird gets all worked up around me,\n |
| 0x5f8c2 | 41 | too. All the animals around here seem to. |
| 0x5f8ec | 50 | Ah, I know. If you'd like, do you two wanna help\n |
| 0x5f91f | 25 | me scrub these guys down? |
| 0x5f939 | 52 | It'd be hard to do on my own, with the woptors all\n |
| 0x5f96e | 45 | antsy like this. They'd probably just mob me. |
| 0x5f99c | 26 | The cloaked figures nod... |
| 0x5f9b7 | 48 | With short-bristled scrubbing brushes in hand,\n |
| 0x5f9e8 | 40 | they begin to brush the woptors' bodies. |
| 0x5fa11 | 21 | Kweh...? Kwuuurrrh... |
| 0x5fa27 | 45 | As the bristles pull across their skin, the\n |
| 0x5fa55 | 37 | woptors let out low, contented cries. |
| 0x5fa7b | 36 | I see. That's how you do it, huh...? |
| 0x5faa0 | 7 | *WHUMP* |
| 0x5faa8 | 5 | Bwah! |
| 0x5faae | 49 | Suddenly and abruptly, the woptor nearest to me\n |
| 0x5fae0 | 31 | slams my chest with a headbutt. |
| 0x5fb00 | 47 | Wh-What was THAT for? My whole ribcage almost\n |
| 0x5fb30 | 10 | collapsed! |
| 0x5fb3b | 25 | KWEH! Kwur-kwur-kwurrr... |
| 0x5fb55 | 51 | The woptor ignores my complaints, nudging me with\n |
| 0x5fb89 | 47 | a brush clamped in its beak, demanding a scrub. |
| 0x5fbb9 | 40 | What? You want me to hurry up and do it? |
| 0x5fbe2 | 8 | Kwurrrr! |
| 0x5fbeb | 50 | Ow, OW--All right, already! Stop pushing it into\n |
| 0x5fc1e | 8 | my face! |
| 0x5fc27 | 24 | *Scrub, scrub, scrub*... |
| 0x5fc40 | 19 | Kwurh... Kwurrrh... |
| 0x5fc54 | 41 | Here? Is this the spot you like, big guy? |
| 0x5fc7e | 49 | As I pull the brush over its body, it starts to\n |
| 0x5fcb0 | 48 | breathe harder and stamp its feet in excitement. |
| 0x5fce1 | 50 | Gah! I get that it feels good, but calm down! If\n |
| 0x5fd14 | 51 | you kick me to death, nobody's gonna scrub you at\n |
| 0x5fd48 | 4 | all. |
| 0x5fd4d | 50 | With those thick, muscled legs, it wouldn't take\n |
| 0x5fd80 | 42 | much for a creature like this to do me in. |
| 0x5fdab | 52 | Man, why did I get stuck with this guy and not the\n |
| 0x5fde0 | 27 | gentle ones the twins have? |
| 0x5fdfc | 11 | *THUMP--*\n |
| 0x5fe08 | 9 | *WHUMP--* |
| 0x5fe12 | 16 | Hrrngh--Bwuh--!! |
| 0x5fe23 | 49 | No sooner than the thought crosses my mind, two\n |
| 0x5fe55 | 39 | massive, feathered shapes slam into me. |
| 0x5fe7d | 11 | KWEH-KWEH!! |
| 0x5fe89 | 20 | Wh--Y-You guys, too? |
| 0x5fe9e | 51 | The two woptors the robed pair had been in charge\n |
| 0x5fed2 | 47 | of nudge me with their brushes, just like the\n |
| 0x5ff02 | 6 | first. |
| 0x5ff09 | 42 | Why are y--Where did those two get off to? |
| 0x5ff34 | 52 | The Mystery Twins have disappeared without so much\n |
| 0x5ff69 | 20 | as a word, as usual. |
| 0x5ff7e | 7 | KWEH!\n |
| 0x5ff86 | 11 | KWEEEEEH!\n |
| 0x5ff92 | 12 | KWEEEEEEEEH! |
| 0x5ff9f | 51 | The woptors stomp and strut, worked into a tizzy,\n |
| 0x5ffd3 | 40 | thrusting the brushes at me insistently. |
| 0x5fffc | 45 | A-Aren't you supposed to be the gentle ones!? |
| 0x6002a | 21 | *Grnngkk, grngkkkk--* |
| 0x60040 | 45 | Ow! Owowow, quit jabbing me with the brush!\n |
| 0x6006e | 15 | I'll do it, OK? |
| 0x6007e | 10 | Why me...? |
| 0x60089 | 12 | *Tug, tug*-- |
| 0x60096 | 33 | Will you WAIT just a goddamn--Oh. |
| 0x600b8 | 48 | Where have you guys b--You know what? It's not\n |
| 0x600e9 | 48 | like you're gonna answer. Can I get some help,\n |
| 0x6011a | 5 | here? |
| 0x60120 | 15 | *Tug-tug-tug--* |
| 0x60130 | 51 | The pair both tug on my sleeve, ignoring what I'm\n |
| 0x60164 | 45 | saying as they point at an approaching shape. |
| 0x60192 | 7 | ...Huh? |
| 0x6019a | 19 | *TUP-TUP-TUP-TUP--* |
| 0x601ae | 49 | The sound of footsteps that are somehow at once\n |
| 0x601e0 | 38 | both heavy and bouncy fills my ears... |
| 0x60218 | 35 | And then that distinctive birdsong. |
| 0x6023c | 20 | No, don't tell me... |
| 0x60269 | 48 | That troublesome bird bounds into the paddock,\n |
| 0x6029a | 34 | chirping with bubbly enthusiasm... |
| 0x602bd | 45 | ...and holding a scrubbing brush in its beak. |
| 0x602eb | 17 | Et tu, Cocopo...? |
| 0x610b1 | 27 | Hey, kid. You got a moment? |
| 0x610cd | 47 | As I wrap up the tasks Kuon assigned me, Ukon\n |
| 0x610fd | 14 | flags me down. |
| 0x6110c | 51 | I'm free, but if you need my help, I'm gonna have\n |
| 0x61140 | 46 | to decline. I've been busting my butt all day. |
| 0x6116f | 52 | Bwahahaha! Missy's really got you under her thumb,\n |
| 0x611a4 | 4 | huh? |
| 0x611a9 | 6 | Guh... |
| 0x611b0 | 45 | He's right, of course. I can't exactly argue. |
| 0x611de | 20 | Well, in any case... |
| 0x611f3 | 52 | You're not used to this rough-and-tumble mercenary\n |
| 0x61228 | 50 | stuff, right? You been taking care of your weapon? |
| 0x6125b | 5 | Care? |
| 0x61261 | 49 | Bah, I figured as much. Guess it can't be helped. |
| 0x61293 | 49 | Ukon draws his sword, muttering under his breath. |
| 0x612c5 | 49 | You haven't maintained your weapon at all since\n |
| 0x612f7 | 49 | we've been in combat, huh? Let me show you what\n |
| 0x61329 | 7 | I mean. |
| 0x61331 | 51 | If you don't care for the blade when you have the\n |
| 0x61365 | 48 | time, you can wind up paying for it in a crisis. |
| 0x61396 | 48 | Ukon sits and pulls a cloth and what look like\n |
| 0x613c7 | 49 | whetstones from his bag, laying them across his\n |
| 0x613f9 | 6 | knees. |
| 0x61400 | 26 | Now that he mentions it... |
| 0x6141b | 50 | I withdraw Kuon's fan from my sash and look over\n |
| 0x6144e | 11 | it closely. |
| 0x6145a | 52 | It has a heft to it, heavy in my fingers and thick\n |
| 0x6148f | 40 | when its blades are folded up like this. |
| 0x614b8 | 50 | When I actually used it, I could tell right away\n |
| 0x614eb | 41 | it was forged solely for inflicting pain. |
| 0x61515 | 48 | I handled it pretty roughly, honestly--without\n |
| 0x61546 | 45 | much care for the state of the weapon itself. |
| 0x61574 | 50 | I guess it's bad that I've just kinda... left it\n |
| 0x615a7 | 17 | alone since then? |
| 0x615b9 | 47 | Ukon smiles wryly, setting a whetstone to the\n |
| 0x615e9 | 20 | steel of his katana. |
| 0x615fe | 51 | When you take up the blade, you entrust your life\n |
| 0x61632 | 49 | to it. Treat it like you would a lover or spouse. |
| 0x61664 | 50 | Be that as it may, how do I care for... whatever\n |
| 0x61697 | 18 | this fan thing is? |
| 0x616aa | 52 | If I were maintaining a sword, I could just follow\n |
| 0x616df | 49 | someone else's example, but this is... different. |
| 0x61711 | 19 | Here, lemme see it. |
| 0x61725 | 28 | You know how to maintain it? |
| 0x61742 | 47 | In my line of work, you learn to care for any\n |
| 0x61772 | 51 | kind of blade. This fan's a rare thing, sure, but\n |
| 0x617a6 | 23 | the basics still apply. |
| 0x617be | 52 | As Ukon takes the fan, he holds it up to the light\n |
| 0x617f3 | 38 | and squints at it from various angles. |
| 0x6181a | 18 | Oh, look at YOU... |
| 0x6182d | 41 | Ukon suddenly smiles in what looks like\n |
| 0x61857 | 11 | admiration. |
| 0x61863 | 52 | Now, THIS--I knew it was a special piece, but this\n |
| 0x61898 | 18 | is somethin' else. |
| 0x618ab | 22 | It's... what, exactly? |
| 0x618c2 | 49 | There's a lot to take in. Any good weapon has a\n |
| 0x618f4 | 49 | story behind it, and this guy's definitely been\n |
| 0x61926 | 7 | places. |
| 0x6192e | 52 | Wh--You're not gonna say it's cursed or something,\n |
| 0x61963 | 8 | are you? |
| 0x6196c | 50 | Ha, I don't mean it like that. Wouldn't surprise\n |
| 0x6199f | 11 | me, though. |
| 0x619ab | 51 | Oh, it wouldn't surprise you. Great. That's good.\n |
| 0x619df | 5 | Cool. |
| 0x619e5 | 49 | Well, first, there's whatever it's forged from... |
| 0x61a17 | 48 | As Ukon taps the metal with his fingernail, it\n |
| 0x61a48 | 39 | emits a high-pitched, resonant ringing. |
| 0x61a70 | 49 | It's not steel, that's for sure. Something much\n |
| 0x61aa2 | 40 | harder, though I can't say exactly what. |
| 0x61acb | 48 | You've been handling it roughly, but it hasn't\n |
| 0x61afc | 28 | chipped or even bent at all. |
| 0x61b19 | 50 | And then there's the question of this... I guess\n |
| 0x61b4c | 24 | you could say mechanism. |
| 0x61b65 | 34 | Mechanism? What sort of mechanism? |
| 0x61b88 | 50 | You didn't notice it? Watch, when you spread the\n |
| 0x61bbb | 21 | fan all the way out-- |
| 0x61bd1 | 44 | There. And if you try to spread the blades\n |
| 0x61bfe | 42 | further... Well, it's pretty nasty. Watch. |
| 0x61c29 | 7 | *CLICK* |
| 0x61c31 | 7 | *SHING* |
| 0x61c39 | 5 | Whoa! |
| 0x61c3f | 52 | At a flick of Ukon's wrist, blades abruptly spring\n |
| 0x61c74 | 23 | from the fan's surface. |
| 0x61c8c | 45 | Hidden blades pop out. It's a clever little\n |
| 0x61cba | 27 | contrivance, I gotta admit. |
| 0x61cd6 | 47 | It had this hidden function all along, huh...\n |
| 0x61d06 | 31 | And this is considered "nasty?" |
| 0x61d26 | 47 | I mean, it took me by surprise, but I'd think\n |
| 0x61d56 | 43 | hidden blades are a pretty standard tactic. |
| 0x61d82 | 47 | Well, look here. See the little grooves along\n |
| 0x61db2 | 19 | each blade segment? |
| 0x61dc6 | 10 | Ah, these? |
| 0x61dd1 | 50 | They're difficult to see at first, but each fold\n |
| 0x61e04 | 46 | of the fan has a thin, deep groove through it. |
| 0x61e33 | 16 | What about them? |
| 0x61e44 | 44 | Ukon produces a waterskin, upending it and\n |
| 0x61e71 | 51 | allowing a few drops to dribble into a dip in the\n |
| 0x61ea5 | 6 | fan... |
| 0x61eac | 45 | As the droplets disappear into the grooves,\n |
| 0x61eda | 50 | moisture spreads across the whole weapon in bare\n |
| 0x61f0d | 8 | moments. |
| 0x61f16 | 6 | Ugh... |
| 0x61f1d | 51 | As water condenses in droplets on the tips of the\n |
| 0x61f51 | 50 | hidden blades, I can't help but groan as I grasp\n |
| 0x61f84 | 17 | the implications. |
| 0x61f96 | 52 | Anyone who suffers even a little nick or a scratch\n |
| 0x61fcb | 27 | from something like that... |
| 0x61fe7 | 41 | Yeah, OK. "Nasty" is definitely the word. |
| 0x62011 | 51 | The broad surfaces may be polished and clean, but\n |
| 0x62045 | 48 | see these little patterns? Blood in the grooves. |
| 0x62076 | 49 | A weapon like this... You gotta wonder how many\n |
| 0x620a8 | 45 | lives it's claimed, to accumulate such deep\n |
| 0x620d6 | 7 | stains. |
| 0x620de | 48 | Who knows? Could be cursed after all, like you\n |
| 0x6210f | 5 | said! |
| 0x62115 | 52 | Urk. I know you meant it as a joke, but that's not\n |
| 0x6214a | 11 | funny, man. |
| 0x62156 | 26 | Yeah, you're right. Sorry. |
| 0x62171 | 17 | Hey, what's he... |
| 0x62183 | 49 | Ukon unfastens the pivot holding the individual\n |
| 0x621b5 | 43 | pieces of the fan together, painstakingly\n |
| 0x621e1 | 17 | disassembling it. |
| 0x621f3 | 49 | Hm. No warping or chipping. If that's the case,\n |
| 0x62225 | 49 | doesn't look like it'll need repairs or anything. |
| 0x6225b | 45 | Why would Kuon be carrying such a dangerous\n |
| 0x62289 | 8 | tool...? |
| 0x62292 | 52 | Seems our Missy thinks highly of you, to trust you\n |
| 0x622c7 | 25 | with something like this. |
| 0x622e1 | 28 | Kuon... thinks highly of me? |
| 0x622fe | 24 | What makes you say that? |
| 0x62317 | 48 | I can tell just by looking she's put her heart\n |
| 0x62348 | 50 | into maintaining this. It's got sentimental value. |
| 0x6237b | 51 | I doubt she'd entrust someone she didn't at least\n |
| 0x623af | 41 | respect with something so special to her. |
| 0x623d9 | 36 | All right. That should do the trick. |
| 0x623fe | 49 | Ukon wipes down each component of the fan, then\n |
| 0x62430 | 37 | puts it back together in short order. |
| 0x62456 | 50 | Here. All done. You oughta have her show you how\n |
| 0x62489 | 45 | she maintains it, so you can start doing it\n |
| 0x624b7 | 9 | yourself. |
| 0x624c1 | 17 | Ah, good point... |
| 0x624d3 | 28 | With that, Ukon turns to go. |
| 0x624f0 | 49 | I ought to thank him, but it slips my mind as I\n |
| 0x62522 | 47 | stand transfixed, staring dumbly at the weapon. |
| 0x62552 | 31 | Ukon's words echo in my mind... |
| 0x62572 | 23 | Sentimental value, huh. |
| 0x6258a | 50 | Why would Kuon give me something so important to\n |
| 0x625bd | 4 | her? |
| 0x625c2 | 50 | I spread and close the fan repeatedly, fidgeting\n |
| 0x625f5 | 27 | with it for no real reason. |
| 0x62611 | 46 | What sentiment has she poured into you, huh?\n |
| 0x62640 | 18 | What's your story? |
| 0x62653 | 48 | The fan remains silent, only glimmering in the\n |
| 0x62684 | 34 | light in lieu of giving an answer. |
| 0x6345a | 29 | Now, that--that is a big pot. |
| 0x63478 | 47 | An enormous cookpot hangs over a stove in the\n |
| 0x634a8 | 48 | corner of the campground, sizzling happily away. |
| 0x634d9 | 47 | Not too far away, amam is being baked, a tall\n |
| 0x63509 | 47 | pile of the doughy skins already stacked on a\n |
| 0x63539 | 6 | table. |
| 0x63540 | 43 | Ho, Master Haku. What seek thee hereabouts? |
| 0x6356c | 50 | Maroro takes note of me and swaggers over, a bag\n |
| 0x6359f | 12 | in his arms. |
| 0x635ac | 47 | Ah, just watching the preparations. I'd never\n |
| 0x635dc | 47 | considered how much work goes into feeding so\n |
| 0x6360c | 12 | many people. |
| 0x63619 | 47 | Verily. 'Tis mine own first sojourn amongst a\n |
| 0x63649 | 41 | company of such great number, to be sure! |
| 0x63673 | 23 | And what are you doing? |
| 0x6368b | 50 | What, I? Ah, gadzooks! Duty compelleth steadfast\n |
| 0x636be | 45 | Maroro to assist the sweetling Lady Rulutieh. |
| 0x636ec | 17 | Helping out, huh? |
| 0x636fe | 47 | Maroro frantically looks around for Rulutieh,\n |
| 0x6372e | 38 | hurrying over as soon as he spots her. |
| 0x63755 | 50 | Mistress Rulutieh, look thee not a moment longer\n |
| 0x63788 | 50 | for thy table-salt! I have found the thing itself. |
| 0x637bb | 47 | Proudly, he holds out the bag in his hands to\n |
| 0x637eb | 9 | Rulutieh. |
| 0x637f5 | 16 | Ah, thank you... |
| 0x63806 | 49 | A simple kitchen area has been set up beneath a\n |
| 0x63838 | 48 | tent, chopped fruits and veggies arranged on a\n |
| 0x63869 | 48 | Rulutieh stands at the table and pulls a solid\n |
| 0x6389a | 49 | chunk from Maroro's bag, crushing it into powder. |
| 0x638cc | 13 | Ah, Sir Haku? |
| 0x638da | 25 | You're cooking, Rulutieh? |
| 0x638f4 | 12 | A-Ah, uhm... |
| 0x63901 | 50 | Th-This is all I can really do to help everyone,\n |
| 0x63934 | 5 | so... |
| 0x6393a | 50 | Isn't it hard, preparing food for so many people\n |
| 0x6396d | 16 | at once, though? |
| 0x6397e | 19 | No, n-not really... |
| 0x63992 | 49 | I... used to manage the kitchens at the castle,\n |
| 0x639c4 | 50 | Huh. I wouldn't have thought a princess would be\n |
| 0x639f7 | 32 | doing that kind of manual labor. |
| 0x63a18 | 52 | I'd figured you would be a little more... I dunno,\n |
| 0x63a4d | 23 | detached from all that? |
| 0x63a65 | 50 | A-Ah, well... My family only rules the outlands,\n |
| 0x63a98 | 45 | so we're... not very powerful as nobles go... |
| 0x63ac6 | 41 | And M-Miss Kuon is helping me, of course! |
| 0x63af0 | 14 | Kuon too, huh? |
| 0x63aff | 37 | What, surprised that I'm helping out? |
| 0x63b25 | 5 | Bwuh! |
| 0x63b2b | 52 | Kuon's voice suddenly speaks from right behind me,\n |
| 0x63b60 | 43 | and I jump almost a full foot into the air. |
| 0x63b8c | 50 | I turn to find her smiling, but it doesn't quite\n |
| 0x63bbf | 19 | extend to her eyes. |
| 0x63bd3 | 47 | You may recall I was traveling alone before I\n |
| 0x63c03 | 45 | picked you up. I had to do everything myself. |
| 0x63c31 | 50 | N-No, I wasn't trying to imply that you can't...\n |
| 0x63c64 | 4 | Ugh. |
| 0x63c69 | 52 | You just watch and witness my skills for yourself,\n |
| 0x63c9e | 12 | nonbeliever. |
| 0x63cab | 51 | Kuon deftly twirls a kitchen knife in her hand as\n |
| 0x63cdf | 47 | she makes this proclamation, pointing it at me. |
| 0x63d0f | 51 | ...Does she have bad memories of being told she's\n |
| 0x63d43 | 26 | a poor chef, or something? |
| 0x63d5e | 49 | Rulutieh, are you sure that much salt will be OK? |
| 0x63d90 | 52 | Ah, I thought it might be better if the flavor was\n |
| 0x63dc5 | 20 | a little stronger... |
| 0x63dda | 51 | Everyone's working so hard... I figured more salt\n |
| 0x63e0e | 45 | would help replace what they're sweating out. |
| 0x63e3c | 33 | Oh, that makes sense. Good point. |
| 0x63e62 | 51 | I can tell I'm not really gonna be any help, so I\n |
| 0x63e96 | 51 | retreat to the edge of the tent to watch from the\n |
| 0x63eca | 5 | side. |
| 0x63ed0 | 52 | Ah, but to sup upon such victuals as those wrought\n |
| 0x63f05 | 46 | by the Lady Rulutieh's own hand! How I hunger! |
| 0x63f34 | 51 | He's right. I've gotta admit, I'm looking forward\n |
| 0x63f68 | 48 | to seeing what handmade dishes come out of this. |
| 0x63f99 | 8 | U-Uhm... |
| 0x63fa2 | 3 | Hm? |
| 0x63fa6 | 44 | Rulutieh approaches me with a small plate,\n |
| 0x63fd3 | 19 | offering it meekly. |
| 0x63fe7 | 46 | H...Here, p-please taste-test this, if y-you\n |
| 0x64016 | 16 | wouldn't mind... |
| 0x64027 | 12 | What's this? |
| 0x64034 | 51 | Simmered food sits lovingly arranged on the plate\n |
| 0x64068 | 34 | in her hands, steaming enticingly. |
| 0x6408b | 31 | I-I hope it's to your liking... |
| 0x640ab | 24 | Wow. It looks delicious. |
| 0x640c4 | 50 | I take a simmered skewer from the plate, eagerly\n |
| 0x640f7 | 32 | sampling the food impaled on it. |
| 0x64118 | 49 | It's cooked thoroughly, seasoned with a perfect\n |
| 0x6414a | 49 | amount of salt that doesn't overwhelm--a homey,\n |
| 0x6417c | 14 | rustic flavor. |
| 0x6418b | 44 | This is amazing! You're an excellent cook,\n |
| 0x641b8 | 49 | Oh, sorry--I'm supposed to call you "princess,"\n |
| 0x641ea | 38 | right? That was probably rude of me... |
| 0x64211 | 33 | N-No, please... call me Rulutieh. |
| 0x64233 | 20 | Here, try mine next. |
| 0x64248 | 38 | You made some too? Don't mind if I d-- |
| 0x6426f | 46 | My hand freezes halfway to the plate Kuon is\n |
| 0x6429e | 11 | proffering. |
| 0x642aa | 9 | Uh, Kuon? |
| 0x642b4 | 11 | What is it? |
| 0x642c0 | 21 | What exactly is this? |
| 0x642d6 | 48 | Simmered skewers? Same thing Rulutieh is making. |
| 0x64307 | 46 | It's, uh, definitely... simmered, all right... |
| 0x64336 | 49 | Isn't it a little, um, big? It's five times the\n |
| 0x64368 | 27 | size of the one Rulutieh... |
| 0x64384 | 18 | Now, have a taste. |
| 0x64397 | 33 | Th-This is a meal, not a "taste!" |
| 0x643b9 | 47 | It's generous to even call this a skewer. The\n |
| 0x643e9 | 50 | wooden rod itself is bending under the strain of\n |
| 0x6441c | 18 | the meat's weight. |
| 0x6442f | 49 | I carefully take the behemoth in my hands, then\n |
| 0x64461 | 46 | bite into it with what reluctant vigor I can\n |
| 0x64490 | 8 | muster-- |
| 0x64499 | 22 | H-Hot! Hot-hot-hot--!! |
| 0x644b0 | 49 | C'mon, don't nibble on it little by little like\n |
| 0x644e2 | 43 | that! Take the whole thing in one mouthful. |
| 0x6450e | 42 | H-Hot--! Come on, Kuon, b-be reasonable... |
| 0x64539 | 51 | It's not BAD, per se, but the flavor's all on the\n |
| 0x6456d | 46 | outside. The meat hasn't absorbed a bit of it. |
| 0x6459c | 49 | I suppose if I take it all in one bite like she\n |
| 0x645ce | 44 | wants me to, it'd be more spread out, but... |
| 0x645fb | 16 | Hmhm. How is it? |
| 0x6460c | 39 | Kuon has a very proud look on her face. |
| 0x64634 | 50 | It's probably exactly to her tastes, but I don't\n |
| 0x64667 | 30 | know how to break this to her. |
| 0x64686 | 22 | It's... good, I guess? |
| 0x6469d | 50 | I thought so. The full batch is almost ready, so\n |
| 0x646d0 | 38 | there'll be more where that came from. |
| 0x646f7 | 48 | I'm using "good" liberally, of course. It's...\n |
| 0x64728 | 27 | FAIRLY good? Good-adjacent. |
| 0x64744 | 46 | Rulutieh gives a small chuckle from beside me. |
| 0x64773 | 49 | When I look over to her, she quickly averts her\n |
| 0x647a5 | 16 | eyes, bashful... |
| 0x647b6 | 43 | She's awfully down-to-earth for a princess. |
| 0x647e2 | 48 | She doesn't have that haughtiness I would have\n |
| 0x64813 | 44 | expected, not to mention she's approachable. |
| 0x64840 | 52 | Ah, anyway. At this rate, I'm gonna be full before\n |
| 0x64875 | 23 | dinner is even ready... |
| 0x64e33 | 50 | Some time after the sun sets, everyone sits down\n |
| 0x64e66 | 30 | to dinner around the campfire. |
| 0x64e85 | 49 | There's amam skins stuffed full of ingredients,\n |
| 0x64eb7 | 47 | and a meat stew that warms me up from the core. |
| 0x64ee7 | 47 | Even though it's reheated campfire food, it's\n |
| 0x64f17 | 46 | easily as hearty as the innkeeper's cooking... |
| 0x64f46 | 13 | Ukon's Cohort |
| 0x64f54 | 22 | Oh, this is delicious! |
| 0x64f6b | 48 | Just like my ma's. Wonder if she's doing well... |
| 0x64f9c | 51 | High praise for the food comes from all over, and\n |
| 0x64fd0 | 48 | though she blushes bashfully, Rulutieh's smile\n |
| 0x65001 | 28 | cuts through her inhibition. |
| 0x6501e | 52 | Next to her stands Kuon, looking pleased and proud\n |
| 0x65053 | 24 | at the universal praise. |
| 0x6506c | 11 | But I know. |
| 0x65078 | 51 | I know the truth about the dish she's enjoying so\n |
| 0x650ac | 22 | many compliments over. |
| 0x650c3 | 45 | Originally, she'd made it far too dense and\n |
| 0x650f1 | 43 | filling, only becoming a proper dish with\n |
| 0x6511d | 16 | Rulutieh's help. |
| 0x6512e | 50 | Actually, "help" is pushing it. I'd say Rulutieh\n |
| 0x65161 | 40 | did about 80% of the work to Kuon's 20%. |
| 0x6518a | 49 | She was more of a hindrance than anything else... |
| 0x651bc | 48 | All right, everybody. You can keep eating, but\n |
| 0x651ed | 10 | listen up. |
| 0x651f8 | 52 | Ukon claps his hands to get the group's attention,\n |
| 0x6522d | 33 | standing in front of the bonfire. |
| 0x6524f | 52 | Everything's been going well so far. We made it to\n |
| 0x65284 | 43 | camp before sunset, just like we'd planned. |
| 0x652b0 | 52 | How things play out from here is a bit tricky. You\n |
| 0x652e5 | 48 | all know from here to the border is covered in\n |
| 0x65316 | 9 | woodland. |
| 0x65320 | 52 | We'll have the old road, but nobody stray too far,\n |
| 0x65355 | 50 | yeah? And take care to keep the carts out of the\n |
| 0x65388 | 4 | mud. |
| 0x6538d | 14 | Ukon's Cohorts |
| 0x6539c | 7 | Yessir. |
| 0x653a4 | 48 | And one more thing--the area up ahead has been\n |
| 0x653d5 | 42 | known for bandit attacks in recent months. |
| 0x65400 | 45 | Judging by the reports, they don't have the\n |
| 0x6542e | 48 | numbers to be a threat, but stay on your guard\n |
| 0x6545f | 11 | regardless. |
| 0x6546b | 48 | Remain vigilant, keep your wits about you, and\n |
| 0x6549c | 32 | we'll make it through just fine. |
| 0x654bd | 52 | And I won't tell you louts not to drink, but don't\n |
| 0x654f2 | 50 | go so hard that it impacts your work tomorrow, hm? |
| 0x65525 | 11 | That's all. |
| 0x65531 | 7 | Yessir! |
| 0x65539 | 48 | A rough forest road, huh... My butt's gonna be\n |
| 0x6556a | 49 | sore again. Still, it's better than walking the\n |
| 0x6559c | 10 | whole way. |
| 0x655a7 | 45 | I should find something I can set down as a\n |
| 0x655d5 | 38 | cushion before we head out tomorrow... |
| 0x655fc | 34 | But there really are bandits, huh? |
| 0x6561f | 51 | I guess there's no need to worry. Everyone in the\n |
| 0x65653 | 30 | company is strong and armed... |
| 0x65672 | 13 | Then again... |
| 0x65680 | 52 | "There's nothing to worry about" is what they told\n |
| 0x656b5 | 42 | me just before the disastrous gigiri hunt. |
| 0x663cc | 46 | After dinner, right as I get up to return to\n |
| 0x663fb | 10 | my tent... |
| 0x66406 | 5 | Yeep! |
| 0x6640c | 6 | Hm...? |
| 0x66413 | 51 | At the sound of someone crying out, I turn around\n |
| 0x66447 | 40 | to find Rulutieh kneeling on the ground. |
| 0x66470 | 33 | What happened? Are you all right? |
| 0x66492 | 44 | O-Oh, I'm... I'm OK. It's nothing, really... |
| 0x664bf | 50 | Nearby, a hempen sack lies in a crumpled heap on\n |
| 0x664f2 | 48 | the ground. She tripped holding it, most likely. |
| 0x66523 | 18 | Here, let me help. |
| 0x66536 | 42 | N-No, I--I can... carry it... by myself... |
| 0x66561 | 50 | You sure? You did trip. Any girl your size would\n |
| 0x66594 | 33 | have trouble with a bag this big. |
| 0x665b6 | 6 | But... |
| 0x665bd | 45 | Heavy lifting's typically a man's job, right? |
| 0x665eb | 4 | Ah-- |
| 0x665f0 | 43 | I crouch down to lift the bag as Rulutieh\n |
| 0x6661c | 48 | continues to hesitate, at a loss for what to do. |
| 0x6664d | 24 | All right. Up we GUH--!! |
| 0x66666 | 15 | Wh--H-Heavy--!! |
| 0x66676 | 9 | Sir Haku? |
| 0x66680 | 34 | Gah! She was trying to CARRY this? |
| 0x666a3 | 50 | My poor, aching back...! But I can't back out of\n |
| 0x666d6 | 10 | this now!! |
| 0x666e1 | 20 | Hnnngh... hrngh...!! |
| 0x666f6 | 51 | Somehow, I manage to lift the bag and get back on\n |
| 0x6672a | 8 | my feet. |
| 0x66733 | 34 | Ah, i-is... is something wrong...? |
| 0x66756 | 41 | No, I--hah!--I got this, you just watch-- |
| 0x66780 | 38 | Thank you... I feel as though I'm...\n |
| 0x667a7 | 26 | inconveniencing you, so... |
| 0x667c2 | 23 | Rulutieh bows politely. |
| 0x667da | 51 | I don't need thanks! J-Just hurry up and point me\n |
| 0x6680e | 32 | somewhere before my spine snaps! |
| 0x6682f | 28 | So where d-do you need this? |
| 0x6684c | 28 | Ah, just... over to my tent. |
| 0x66869 | 26 | All right. L-Lead the way. |
| 0x66884 | 6 | OK...! |
| 0x6688b | 7 | *FWUMP* |
| 0x66893 | 28 | Gasp... gasp... f-finally... |
| 0x668b0 | 24 | Ah, thank you very much. |
| 0x668c9 | 49 | No, it was--h-hah--no... haaaaahh. No big deal... |
| 0x668fb | 50 | I manage to smile, though I can't quite still my\n |
| 0x6692e | 13 | shaking legs. |
| 0x6693c | 27 | Oh, but you're sweating...! |
| 0x66958 | 52 | Rulutieh produces a handkerchief, carefully wiping\n |
| 0x6698d | 48 | away the sweat on my brow, my cheeks, my neck... |
| 0x669be | 51 | She stands on tiptoe, stretching around to reach,\n |
| 0x669f2 | 39 | nearly pressing her front against mine. |
| 0x66a1a | 49 | ...She smells nice. Is she wearing some kind of\n |
| 0x66a4c | 27 | perfume, or incense, or...? |
| 0x66a68 | 52 | Is it that strange, enchanting fragrance all women\n |
| 0x66a9d | 17 | seem to give off? |
| 0x66aaf | 19 | ...There. Finished. |
| 0x66ac3 | 49 | Rulutieh's voice pulls my head back down out of\n |
| 0x66af5 | 40 | the clouds, snapping me back to reality. |
| 0x66b1e | 14 | Ah, thank you. |
| 0x66b2d | 38 | O-Oh, it's the least I could do, so... |
| 0x66b54 | 24 | Well, I'll be off, then. |
| 0x66b6d | 31 | A-Ah, hold on. If you'd like... |
| 0x66b8d | 49 | I'll make some tea. Please, stay and rest for a\n |
| 0x66bbf | 8 | while... |
| 0x66bc8 | 42 | Rulutieh brews up a cup of tea skillfully. |
| 0x66bf3 | 21 | Here... Please enjoy. |
| 0x66c09 | 51 | Sweet, arresting scents steal across my nose from\n |
| 0x66c3d | 37 | the cup-- milk, wildflowers, honey... |
| 0x66c63 | 27 | You're pretty good at that. |
| 0x66c7f | 51 | Oh, um, thank you. Back home, I liked serving tea\n |
| 0x66cb3 | 15 | to my family... |
| 0x66cc3 | 48 | Rulutieh reminisces, a gentle smile on her face. |
| 0x66cf4 | 51 | This country, Kujyuri, used to be a wasteland. My\n |
| 0x66d28 | 47 | father, the owlo-- he cultivated great growth\n |
| 0x66d58 | 7 | here... |
| 0x66d60 | 50 | He, my older sisters, and my brothers all worked\n |
| 0x66d93 | 48 | the land with their own hands, tilling the soil. |
| 0x66dc4 | 37 | But I have a weak constitution, so... |
| 0x66dea | 51 | That's why I'm content to make tea for them, cook\n |
| 0x66e1e | 38 | for them... I help them in my own way. |
| 0x66e45 | 48 | I see. So that's why she has that domestic air\n |
| 0x66e76 | 10 | about her. |
| 0x66e81 | 49 | But how can she say she has a weak constitution\n |
| 0x66eb3 | 50 | when she was carrying a bag that heavy? Was that\n |
| 0x66ee6 | 7 | a joke? |
| 0x66eee | 52 | As I consider, I raise the cup to my lips and take\n |
| 0x66f23 | 16 | a careful sip... |
| 0x66f34 | 22 | Oh, this is delicious. |
| 0x66f4b | 21 | I'm glad you like it! |
| 0x66f61 | 48 | The bitterness and sweetness are balanced just\n |
| 0x66f92 | 29 | right. It's nice and calming. |
| 0x66fb0 | 34 | It's my eldest brother's favorite. |
| 0x66fd3 | 51 | It's said to relieve fatigue, so... I'm glad it's\n |
| 0x67007 | 16 | working for you. |
| 0x67018 | 44 | She really is a sweet, kind girl, isn't she? |
| 0x67045 | 52 | As she walks through her explanation, I indulge in\n |
| 0x6707a | 43 | another two, three sips of the calming tea. |
| 0x670a6 | 27 | Would you like another cup? |
| 0x670c2 | 11 | Ah, please. |
| 0x670ce | 3 | OK! |
| 0x670d2 | 46 | Rulutieh quickly sets about making more tea.\n |
| 0x67101 | 33 | I can tell she's done this a lot. |
| 0x67123 | 45 | As I watch her produce various kinds of tea\n |
| 0x67151 | 34 | leaves, a realization dawns on me. |
| 0x67174 | 45 | Hey, is that... entire shelf just tea leaves? |
| 0x671a2 | 22 | Ah, yes! Yes, it is... |
| 0x671b9 | 50 | Easily more than ten small drawers of tea leaves\n |
| 0x671ec | 31 | line the shelf from end to end. |
| 0x6720c | 43 | Aren't teas expensive here, if I recall...? |
| 0x67238 | 52 | Curiosity piqued, I take in my surroundings inside\n |
| 0x6726d | 9 | the tent. |
| 0x67277 | 48 | It's large for a single-person tent, the extra\n |
| 0x672a8 | 46 | space taken up mostly by shelving and drawers. |
| 0x672d7 | 29 | Can I ask what's in that one? |
| 0x672f5 | 50 | Ah, that shelf? That's... my wardrobe, my makeup\n |
| 0x67328 | 6 | box... |
| 0x6732f | 13 | And that one? |
| 0x6733d | 52 | That's for my cooking utensils... My sewing set...\n |
| 0x67372 | 40 | Ah, and that one just has knickknacks... |
| 0x6739b | 35 | What about that big one back there? |
| 0x673bf | 52 | Um, ah--Th-That's, ah... You'll laugh, but it's...\n |
| 0x673f4 | 48 | my bedding. I can't sleep with another pillow... |
| 0x67425 | 51 | Rulutieh grows quieter and quieter toward the end\n |
| 0x67459 | 37 | of her sentence, fidgeting bashfully. |
| 0x6747f | 10 | I-I see... |
| 0x6748a | 30 | She really is a princess, huh? |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_02.json` com a forma:
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
