# Cena ch_13_05 — pacote de traducao (452 linhas)

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
| Cocopo | Criatura | Cocopo | manter_original | none |
| Cohort | Organizacao | Coorte | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
| Woman | UI | Mulher | traduzir | none |

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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
### Oshtor — criticality: high
- Oshtor — `voice_criticality: high`. = Ukon até 13_08 (ver spoiler_ledger). Registro formal, nobre, comedido; General da Direita. Antes do reveal, traduzir como o mercenário "Ukon" (espirituoso, informal) — NÃO antecipar a pompa de general
### Ougi — criticality: low
- Ougi — `voice_criticality: low`. Irmão da Nosuri; pragmático, parceria com a irmã.
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Mysterious duo right` -> `Dupla misteriosa dir.` (sistema, 13_02)
- `Mysterious duo left` -> `Dupla misteriosa esq.` (sistema, 13_02)
- `*Poke-poke-poke*...` -> `*Cutuca-cutuca-cutuca*...` (sistema, 13_01)
- `*Squish-squish-squish*...` -> `*Amassa-amassa-amassa*...` (sistema, 13_02)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Girl` -> `Garota` (sistema, 13_01)
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Sir!` -> `Sim!` (Maroro, 12_09)
- `...Eh?` -> `...Hein?` (Rulutieh, 13_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Sir Haku?` -> `Sir Haku?` (Rulutieh, 13_02)
- `little.` -> `acorda.` (Garota, 12_01)
- `Wh--?` -> `Qu--?` (Haku, 12_03)
- `Hm.` -> `Hm.` (Ukon, 12_12)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `Hey!` -> `Ei!` (Haku, 12_12)
- `I... see...` -> `Eu... entendo...` (Kuon, root)
- `Urgh--` -> `Argh--` (Man, root)
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
| 0x6d387 | 52 | The caravan continues on its slow, inexorable roll\n |
| 0x6d3bc | 23 | up the mountain path... |
| 0x6d3d4 | 51 | I can tell the road here was paved at SOME point,\n |
| 0x6d408 | 49 | but now, only a scattered few flat stones remain. |
| 0x6d43a | 48 | Trees have taken root in the days since, roots\n |
| 0x6d46b | 47 | snaking under the surface and breaking up the\n |
| 0x6d49b | 5 | path. |
| 0x6d4a1 | 50 | So this is what Ukon meant when he said the road\n |
| 0x6d4d4 | 17 | would be rough... |
| 0x6d4e6 | 45 | The snowmelt has sunken into the dirt, too,\n |
| 0x6d514 | 49 | forcing everyone to trudge through the thick mud. |
| 0x6d546 | 20 | Mysterious duo right |
| 0x6d55f | 19 | Mysterious duo left |
| 0x6d573 | 19 | *Poke-poke-poke*... |
| 0x6d587 | 25 | *Squish-squish-squish*... |
| 0x6d5a1 | 46 | As usual, the Mystery Twins are close at hand. |
| 0x6d5d0 | 25 | This is... Ah, forget it. |
| 0x6d5ea | 51 | No matter what I say, it's not like they're gonna\n |
| 0x6d61e | 45 | reply. It's pointless to even worry about it. |
| 0x6d64c | 34 | ...Man, though. It's getting dark. |
| 0x6d66f | 47 | The sun SHOULD be at high noon, but the thick\n |
| 0x6d69f | 43 | canopy growth above us is blocking it out\n |
| 0x6d6cb | 12 | effectively. |
| 0x6d6d8 | 52 | Ne'ertofore have I breathed so foul an air as that\n |
| 0x6d70d | 45 | which chilleth my very bones in this place... |
| 0x6d73b | 46 | Maroro mutters uneasily as he shoots furtive\n |
| 0x6d76a | 38 | glances about, peering into the trees. |
| 0x6d791 | 49 | It calleth forward a memory most unseemly, of a\n |
| 0x6d7c3 | 41 | darkling scroll that fearful once I read. |
| 0x6d7ed | 50 | 'Twas a tale of a man a-wandering in a wood like\n |
| 0x6d820 | 49 | this one, whence he met a woman of beauty quite\n |
| 0x6d852 | 10 | unmatch'd. |
| 0x6d85d | 51 | But lo, 'neath this woman's mask of deception lay\n |
| 0x6d891 | 52 | a nugwisomkami! That which feasteth upon the flesh\n |
| 0x6d8c6 | 13 | of wayfarers. |
| 0x6d8d4 | 45 | "Nugwisomkami?" So, what, it's some kind of\n |
| 0x6d902 | 33 | phantom or ghost or something...? |
| 0x6d924 | 45 | Doth the tale frighten thee not, Master Haku? |
| 0x6d952 | 18 | Not... really, no. |
| 0x6d965 | 10 | I-I see... |
| 0x6d970 | 47 | Not only is it kind of a generic story, but a\n |
| 0x6d9a0 | 47 | short summary isn't exactly gonna strike fear\n |
| 0x6d9d0 | 14 | into my heart. |
| 0x6d9df | 3 | Hm? |
| 0x6d9e3 | 45 | A figure on the road ahead catches my gaze... |
| 0x6da11 | 52 | Someone unfamiliar stands at the side of the road,\n |
| 0x6da46 | 46 | waving both arms in an effort to flag us down. |
| 0x6da75 | 52 | Next to them, a wagon much like one of our own has\n |
| 0x6daaa | 37 | tilted and fallen, blocking the road. |
| 0x6dad0 | 55 | Ukon calls a halt, and a nervous vibe ripples through\n |
| 0x6db08 | 47 | the caravan, the prospect of bandits very real. |
| 0x6db38 | 4 | Girl |
| 0x6db3d | 40 | I'm so sorry, but could you help me out? |
| 0x6db66 | 48 | The young girl next to the wagon approaches us\n |
| 0x6db97 | 25 | with an apologetic smile. |
| 0x6dbb1 | 29 | What can we do for you, miss? |
| 0x6dbcf | 52 | My cart's wheels are stuck in a ditch, and I can't\n |
| 0x6dc04 | 21 | get it out on my own. |
| 0x6dc1a | 52 | My companions went for help, but at this rate, the\n |
| 0x6dc4f | 43 | sun's going to set before they come back... |
| 0x6dc7b | 46 | I'm awfully sorry, but could I get your help\n |
| 0x6dcaa | 22 | pushing the cart free? |
| 0x6dcc1 | 52 | Quite a bind you're in, huh. All right, men, let's\n |
| 0x6dcf6 | 13 | help her out! |
| 0x6dd04 | 13 | Ukon's Cohort |
| 0x6dd12 | 4 | Sir! |
| 0x6dd17 | 15 | Leave it to us! |
| 0x6dd27 | 42 | Several men quickly gather at Ukon's call. |
| 0x6dd52 | 51 | They seem a little eager to please because it's a\n |
| 0x6dd86 | 50 | woman--especially one with a pretty face. Figures. |
| 0x6ddb9 | 39 | Hey, Maroro. Is that your nugwisomkami? |
| 0x6dde1 | 8 | How now? |
| 0x6ddea | 49 | The story you just told me. She gonna eat us up\n |
| 0x6de1c | 24 | while our guard is down? |
| 0x6de35 | 47 | G-Gadzooks, Master Haku, make not such jests!\n |
| 0x6de65 | 24 | 'Tis no laughing matter! |
| 0x6de7e | 50 | Oh, come on, I'm not being serious. I just asked\n |
| 0x6deb1 | 21 | if it looks like her. |
| 0x6dec7 | 47 | I mean--she's cute, but I wouldn't call her a\n |
| 0x6def7 | 49 | woman of "beauty unmatch'd" or whatever you said. |
| 0x6df29 | 26 | O-One supposeth as much... |
| 0x6df44 | 50 | She possesseth some charm, but no. Milady is not\n |
| 0x6df77 | 43 | such a beauty as the fell creatures might\n |
| 0x6dfa3 | 12 | impersonate. |
| 0x6dfb0 | 50 | Forsooth, let us be thankful for thy homeliness... |
| 0x6dfe3 | 26 | Hm? Something wrong, miss? |
| 0x6dffe | 17 | No, not really... |
| 0x6e010 | 49 | You're very kind. If I may, can I make one more\n |
| 0x6e042 | 15 | request of you? |
| 0x6e052 | 20 | Sure, let's hear it. |
| 0x6e067 | 46 | Mm, put down your weapons and leave all your\n |
| 0x6e096 | 24 | other belongings behind. |
| 0x6e0af | 6 | ...Eh? |
| 0x6e0b6 | 4 | Huh? |
| 0x6e0bb | 50 | Put down your weapons, and leave your belongings\n |
| 0x6e0ee | 7 | behind. |
| 0x6e0f6 | 8 | *FWOOSH* |
| 0x6e0ff | 52 | In the blink of an eye, the dropcloth covering her\n |
| 0x6e134 | 44 | cart's cargo rips away, revealing armed men. |
| 0x6e161 | 51 | Ukon's men who had approached the caravan to help\n |
| 0x6e195 | 46 | lift it are quickly subdued and pinned down... |
| 0x6e1c4 | 5 | Ah--! |
| 0x6e1ca | 5 | Wh--! |
| 0x6e1d0 | 11 | Don't move. |
| 0x6e1dc | 52 | Faster than Ukon can reach for his blade, the girl\n |
| 0x6e211 | 18 | raises her hand... |
| 0x6e224 | 46 | At her signal, more men with bows and nocked\n |
| 0x6e253 | 48 | arrows materialize from the trees, aimed right\n |
| 0x6e284 | 6 | at us. |
| 0x6e28b | 28 | Yeek! Wh-Wh-What manner of-- |
| 0x6e2a8 | 17 | We're surrounded! |
| 0x6e2ba | 52 | Their numbers are only half ours, but every one of\n |
| 0x6e2ef | 41 | them has his bowstring drawn and readied. |
| 0x6e319 | 45 | We'll have to play this very, very carefully. |
| 0x6e347 | 17 | M-Master Haku...! |
| 0x6e359 | 47 | Maroro begins visibly trembling at the sudden\n |
| 0x6e389 | 12 | development. |
| 0x6e396 | 49 | Both he and the twins are-- Wait, where did the\n |
| 0x6e3c8 | 9 | twins go? |
| 0x6e3d2 | 29 | ...Vanished again, of course. |
| 0x6e3f0 | 12 | Hm. Not bad. |
| 0x6e3fd | 52 | Ukon remains straight-backed and fearless, but his\n |
| 0x6e432 | 23 | voice is audibly stiff. |
| 0x6e44a | 48 | Worry not. We're merely after your cargo. Your\n |
| 0x6e47b | 46 | lives are only in danger if you decide to be\n |
| 0x6e4aa | 7 | idiots. |
| 0x6e4b2 | 51 | Or... perhaps you'll resist, and put those two on\n |
| 0x6e4e6 | 17 | the bird at risk? |
| 0x6e4f8 | 42 | Is she talking about... Rulutieh and Kuon? |
| 0x6e523 | 48 | If they loose those arrows, the girls would be\n |
| 0x6e554 | 45 | first to fall. There's nowhere to take cover. |
| 0x6e582 | 14 | A-Ah... Uhm... |
| 0x6e591 | 51 | I look over to see Kuon protectively wrapping her\n |
| 0x6e5c5 | 48 | arms around Rulutieh, who's gone pale with fear. |
| 0x6e5f6 | 33 | ...Guess there's no choice, then. |
| 0x6e618 | 52 | Ukon takes his katana from his waist and tosses it\n |
| 0x6e64d | 20 | at the woman's feet. |
| 0x6e662 | 45 | You guys do the same. Don't do anything rash. |
| 0x6e690 | 51 | I'm taking her at her word that she won't hurt us\n |
| 0x6e6c4 | 17 | if we stay quiet. |
| 0x6e6d6 | 47 | The ankuam all share looks, murmuring to each\n |
| 0x6e706 | 8 | other... |
| 0x6e70f | 50 | The reality of their situation sinks in, and one\n |
| 0x6e742 | 33 | by one, they lay down their arms. |
| 0x6e764 | 19 | You there. You too. |
| 0x6e778 | 50 | Maroro and I are the only ones not moving to put\n |
| 0x6e7ab | 50 | down our weapons... We're drawing undue attention. |
| 0x6e7de | 30 | Looks like I have no choice... |
| 0x6e7fd | 52 | I guess I can only ride out the storm and see what\n |
| 0x6e832 | 23 | happens, at this point. |
| 0x6e84a | 50 | I pull the fan from my sash and gently lay it on\n |
| 0x6e87d | 11 | the ground. |
| 0x6e889 | 18 | And the other one. |
| 0x6e89c | 14 | I-I... I-I-I-- |
| 0x6e8ab | 32 | He doesn't have anything on him. |
| 0x6e8cc | 49 | As Maroro dissolves into a panic, I step in and\n |
| 0x6e8fe | 14 | speak for him. |
| 0x6e90d | 21 | O-Oh, Master Haku...! |
| 0x6e923 | 51 | Maroro takes my words as sticking up for him, and\n |
| 0x6e957 | 27 | he quivers, moved to tears. |
| 0x6e973 | 51 | ...Really, I only did it so his flailing wouldn't\n |
| 0x6e9a7 | 27 | unnecessarily provoke them. |
| 0x6e9c3 | 15 | Very well. Men! |
| 0x6e9d3 | 7 | Brigand |
| 0x6e9db | 11 | Yes, ma'am! |
| 0x6e9e7 | 47 | At the woman's call, some of her bandits step\n |
| 0x6ea17 | 19 | forward with ropes. |
| 0x6ea2b | 44 | Hands behind your backs. Nice and slow-like. |
| 0x6ea58 | 45 | There's no real point in resisting. I do as\n |
| 0x6ea86 | 11 | instructed. |
| 0x6ea92 | 48 | Didn't Ukon say no bandit would dare attack us\n |
| 0x6eac3 | 13 | like this...? |
| 0x6ead1 | 44 | And here we are. Being attacked. By bandits. |
| 0x6eafe | 49 | Glancing up the line to Ukon, I can see they've\n |
| 0x6eb30 | 39 | also tied him up and forced him to sit. |
| 0x6eb58 | 50 | At least these guys don't seem like the types to\n |
| 0x6eb8b | 24 | do anything too rough... |
| 0x6eba4 | 49 | Ha! Well done, Nosuri. A right impressive show,\n |
| 0x6ebd6 | 5 | this. |
| 0x6ebdc | 48 | The sound of slow clapping fills the clearing... |
| 0x6ec0d | 50 | A broad-shouldered, rugged man appears and gives\n |
| 0x6ec40 | 47 | a vulgar smile, clapping as he approaches the\n |
| 0x6ec70 | 5 | girl. |
| 0x6ec76 | 50 | Despite his dramatic entrance, Nosuri only gives\n |
| 0x6eca9 | 47 | him a sidelong glance, hardly paying attention. |
| 0x6ecd9 | 49 | The newcomer shrugs it off, looking over to me... |
| 0x6ed0b | 53 | Or past me, more accurately, to Kuon and Rulutieh--\n |
| 0x6ed41 | 49 | now dismounted and tied up. His smile widens by\n |
| 0x6ed73 | 14 | several teeth. |
| 0x6ed82 | 48 | Heh heh. Now, ain't this one a beauty? Lookers\n |
| 0x6edb3 | 48 | like this are hard to come by, even in the city. |
| 0x6ede4 | 43 | Yeah, that settles that. This girl is mine. |
| 0x6ee10 | 10 | Bastard... |
| 0x6ee1b | 52 | The woman--Nosuri, apparently--had promised they'd\n |
| 0x6ee50 | 49 | only touch the cargo, but I guess that was a lie. |
| 0x6ee82 | 48 | Hey, boys. Don't forget to search these idiots\n |
| 0x6eeb3 | 48 | while we've got 'em tied up. Take whatever you\n |
| 0x6eee4 | 13 | come up with. |
| 0x6eef2 | 7 | Bandits |
| 0x6eefa | 5 | Yeah! |
| 0x6ef00 | 48 | At the broad-shouldered man's call, a bunch of\n |
| 0x6ef31 | 50 | ragged ruffians--a new, separate group--approach\n |
| 0x6ef64 | 5 | us... |
| 0x6ef6a | 51 | This isn't good. How are we gonna get out of this\n |
| 0x6ef9e | 7 | one...? |
| 0x6efa6 | 41 | Sorry, but I'll pass. You aren't my type. |
| 0x6efd0 | 5 | Hm... |
| 0x6efd6 | 5 | Hmhm. |
| 0x6efdc | 51 | Oh, you're good. You've got spunk. I'm likin' you\n |
| 0x6f010 | 15 | even more, now! |
| 0x6f020 | 49 | Heh heh. You girls are mine, now, y'understand?\n |
| 0x6f052 | 48 | I'll be sure to give you plenty of "attention"\n |
| 0x6f083 | 6 | later. |
| 0x6f08a | 30 | Hey, boss, you'd better share! |
| 0x6f0a9 | 48 | You wish! I ain't sharing one little finger of\n |
| 0x6f0da | 15 | these lovelies. |
| 0x6f0ea | 12 | Miss Kuon... |
| 0x6f0f7 | 48 | Pale with fear, Rulutieh huddles against Kuon,\n |
| 0x6f128 | 8 | shaking. |
| 0x6f131 | 49 | Hey, hey. Everything's going to be OK. We'll be\n |
| 0x6f163 | 21 | all right. I promise. |
| 0x6f179 | 37 | Well, someone's incredibly confident. |
| 0x6f19f | 48 | The situation's looking bleaker by the moment.\n |
| 0x6f1d0 | 48 | Does Kuon have some kind of secret plan up her\n |
| 0x6f201 | 7 | sleeve? |
| 0x6f209 | 37 | I'm sure Haku will find us a way out. |
| 0x6f22f | 9 | Sir Haku? |
| 0x6f239 | 4 | Me!? |
| 0x6f23e | 49 | Rulutieh follows Kuon's eyes, looking to me for\n |
| 0x6f270 | 5 | help. |
| 0x6f276 | 34 | Wh-What does she expect ME to do!? |
| 0x6f299 | 49 | Please stop looking at me like that. Those eyes\n |
| 0x6f2cb | 29 | are plaguing me with guilt... |
| 0x6f2e9 | 51 | Moznu, enough. If you're going to be working with\n |
| 0x6f31d | 50 | the Nosuri Thieves from now on, you abide by our\n |
| 0x6f350 | 17 | rules, not yours. |
| 0x6f362 | 51 | The girl gives the man called Moznu a sharp look,\n |
| 0x6f396 | 16 | admonishing him. |
| 0x6f3a7 | 49 | We only take the cargo. Everything and everyONE\n |
| 0x6f3d9 | 27 | else is to remain unharmed. |
| 0x6f3f5 | 50 | I told you this before. You can't just do as you\n |
| 0x6f428 | 7 | please. |
| 0x6f430 | 49 | Ah, come on, don't be such a spoilsport! Live a\n |
| 0x6f462 | 7 | little. |
| 0x6f46a | 49 | You know you can just leave it aaall to me, babe. |
| 0x6f49c | 49 | Moznu swaggers over to Nosuri and throws an arm\n |
| 0x6f4ce | 49 | around her shoulder, getting a little too close\n |
| 0x6f500 | 12 | for comfort. |
| 0x6f50d | 52 | I know you're just jealous 'cause I'm giving those\n |
| 0x6f542 | 49 | two attention. Why don't you come clean, already? |
| 0x6f574 | 51 | Be my sweetheart, yeah? It'd be an awful shame if\n |
| 0x6f5a8 | 48 | those great tits of yours never got the lovin'\n |
| 0x6f5d9 | 13 | they deserve. |
| 0x6f5e7 | 49 | As Moznu points meaningfully at Nosuri's chest,\n |
| 0x6f619 | 48 | she calmly seizes his finger and twists sharply. |
| 0x6f64a | 6 | *KRAK* |
| 0x6f651 | 9 | HRAAAGH!! |
| 0x6f65b | 52 | Moznu drops to the ground, clutching the offending\n |
| 0x6f690 | 28 | finger and writhing in pain. |
| 0x6f6ad | 47 | D-Did she just--Fingers aren't... supposed to\n |
| 0x6f6dd | 16 | bend that way... |
| 0x6f6ee | 24 | Heh. Behave, little boy. |
| 0x6f707 | 50 | Nosuri says that line as though reciting it from\n |
| 0x6f73a | 31 | a script, then winks awkwardly. |
| 0x6f75a | 50 | How was that, Ougi? Did I act with all the style\n |
| 0x6f78d | 29 | and strength of a good woman? |
| 0x6f7ab | 45 | Truly most impressive, dearest sister. Your\n |
| 0x6f7d9 | 32 | feminine charms dazzle, as ever. |
| 0x6f7fa | 5 | Wh--? |
| 0x6f800 | 33 | A slender man appears next to me. |
| 0x6f822 | 51 | How was he hiding in plain sight? I didn't notice\n |
| 0x6f856 | 11 | him at all. |
| 0x6f862 | 49 | That's right. With this, I'm one step closer to\n |
| 0x6f894 | 37 | being the very model of a good woman! |
| 0x6f8ba | 46 | Gh... guh... g-gah... What'd you do that for!? |
| 0x6f8e9 | 47 | He looks like he's in serious pain, thrashing\n |
| 0x6f919 | 28 | about as he howls at Nosuri. |
| 0x6f936 | 43 | How positively boorish. A good MAN simply\n |
| 0x6f962 | 38 | laughs and shrugs off a woman's jests. |
| 0x6f989 | 48 | How'm I supposed to shrug this off!? This shit\n |
| 0x6f9ba | 6 | HURTS! |
| 0x6f9c1 | 44 | Oh, dear. This is exactly why you'll never\n |
| 0x6f9ee | 31 | aspire to be a good man, Moznu. |
| 0x6fa0e | 50 | There was once a foreign owlo who was thought to\n |
| 0x6fa41 | 24 | be such a man, you know. |
| 0x6fa5a | 51 | No matter how his jealous wife hit him or stabbed\n |
| 0x6fa8e | 48 | him with her chopsticks, he grinned and bore it. |
| 0x6fabf | 44 | To weather such treatment with a smile and\n |
| 0x6faec | 43 | acceptance--such is the duty of a good man! |
| 0x6fb18 | 50 | ...I'm finding a couple of things wrong with her\n |
| 0x6fb4b | 14 | logic, here... |
| 0x6fb5a | 45 | You, on the other hand, are a boor and a pig. |
| 0x6fb88 | 14 | H-How dare--!? |
| 0x6fb97 | 47 | The man grimaces, but just as he moves toward\n |
| 0x6fbc7 | 39 | Nosuri menacingly, he freezes in place. |
| 0x6fbef | 49 | Why, my good man. Whatever is the matter? Can't\n |
| 0x6fc21 | 9 | you move? |
| 0x6fc2b | 9 | U-Urgh... |
| 0x6fc35 | 53 | The man called Ougi--at my side just a moment ago--\n |
| 0x6fc6b | 49 | reappears behind Moznu, holding a thin blade to\n |
| 0x6fc9d | 9 | his neck. |
| 0x6fca7 | 51 | What's with this guy? I didn't even see him move... |
| 0x6fcdb | 49 | H-Hey now, I'm just joking, yeah? All in g-good\n |
| 0x6fd0d | 18 | fun. Take it easy. |
| 0x6fd20 | 47 | It's all right, Ougi. Forgiving a man for his\n |
| 0x6fd50 | 46 | rudeness is what a good woman does, after all. |
| 0x6fd7f | 48 | If you insist, dearest sister, then I defer to\n |
| 0x6fdb0 | 15 | your judgement. |
| 0x6fdc0 | 47 | And just like that, Ougi slips his blade back\n |
| 0x6fdf0 | 46 | into his sleeve and walks away as if nothing\n |
| 0x6fe1f | 16 | happened at all. |
| 0x6fe30 | 45 | Ghh... Guh. Geh heh. Heh! Whatever. I never\n |
| 0x6fe5e | 23 | liked huge tits anyway! |
| 0x6fe76 | 48 | Spitting a weak parting shot over his shoulder\n |
| 0x6fea7 | 42 | like a sore loser, Moznu turns and runs... |
| 0x6fed2 | 51 | They're gonna shrivel up and droop when you're an\n |
| 0x6ff06 | 16 | old hag, y'know! |
| 0x6ff17 | 50 | --and gives a final insult as he disappears into\n |
| 0x6ff4a | 12 | the thicket. |
| 0x6ff57 | 32 | Is something the matter, sister? |
| 0x6ff78 | 3 | Ah? |
| 0x6ff7c | 26 | ...It's nothing. Carry on. |
| 0x6ff97 | 49 | Ougi waves to the remaining men at her command,\n |
| 0x6ffc9 | 50 | who gather around the caravan's unmanned wagons... |
| 0x6fffc | 48 | Anything loaded with cargo--even that strange,\n |
| 0x7002d | 42 | covered one--is hauled off in short order. |
| 0x70058 | 51 | Please forgive the inconvenience. We'll be taking\n |
| 0x7008c | 15 | this. Farewell! |
| 0x7009c | 50 | Do take care on the road, friends. Until we meet\n |
| 0x700cf | 6 | again. |
| 0x700d6 | 47 | With bizarrely polite farewells, both of them\n |
| 0x70106 | 49 | disappear with the last of the bandits into the\n |
| 0x70138 | 6 | woods. |
| 0x7013f | 44 | ...Good grief. Well, at least we survived... |
| 0x7016c | 52 | I mean. We're tied up deep in the mountains, sure,\n |
| 0x701a1 | 51 | but we survived. Now how are we supposed to break\n |
| 0x701d5 | 13 | out of this!? |
| 0x701e3 | 20 | *Wriggle, wriggle--* |
| 0x701f8 | 45 | No sooner than the thought crosses my mind,\n |
| 0x70226 | 49 | I notice Kuon, wiggling her body oddly behind me. |
| 0x70258 | 6 | There. |
| 0x7025f | 11 | *Flumph*... |
| 0x7026b | 47 | The ropes tightly wrapped around her suddenly\n |
| 0x7029b | 19 | fall to the ground. |
| 0x702af | 51 | A rope escape, huh? You're gonna have to teach me\n |
| 0x702e3 | 40 | that if this turns into a regular thing. |
| 0x7030c | 51 | Mm, there's a little trick to it, that's all. You\n |
| 0x70340 | 28 | just dislocate your fingers. |
| 0x7035d | 51 | I'm, uh, reasonably sure that's a pretty big leap\n |
| 0x70391 | 22 | from a "little trick." |
| 0x703a8 | 49 | Sure it is. Just hold still and let me untie you. |
| 0x703da | 49 | Kuon makes her way down the line, starting with\n |
| 0x7040c | 46 | me, then untying everyone in quick succession. |
| 0x7043b | 18 | A-Ah, thank you... |
| 0x7044e | 36 | Hey, missy. Do mine, too, won't you? |
| 0x70473 | 40 | Oh? I don't think I need to untie yours. |
| 0x7049c | 26 | What're you talking about? |
| 0x704b7 | 49 | You're a pretty good actor, Ukon, but enough of\n |
| 0x704e9 | 44 | the charade. I could tell something was off. |
| 0x70516 | 48 | You weren't being cautious at all, what with a\n |
| 0x70547 | 44 | suspicious woman approaching us unsolicited. |
| 0x70574 | 3 | Hm. |
| 0x70578 | 48 | It's not like you at all. A mercenary captain,\n |
| 0x705a9 | 42 | letting his guard down? I hardly think so. |
| 0x705d4 | 41 | You're overestimating me, I think, missy. |
| 0x705fe | 50 | And the way you took her story at face value was\n |
| 0x70631 | 48 | unlike you, too. You would've asked for details. |
| 0x70662 | 6 | Ngh... |
| 0x70669 | 51 | Moreover, after they surrounded us, only Rulutieh\n |
| 0x7069d | 49 | and Maroro were upset. Everyone else stayed calm. |
| 0x706cf | 46 | With all of that in mind, that was a strange\n |
| 0x706fe | 42 | encounter we just had, wouldn't you agree? |
| 0x70729 | 47 | ...So that's why Kuon was so unflappable. She\n |
| 0x70759 | 25 | noticed something was up. |
| 0x70773 | 49 | Had it been one or two "off" notes I might have\n |
| 0x707a5 | 45 | let it slide, but the whole thing feels too\n |
| 0x707d3 | 11 | suspicious. |
| 0x707df | 48 | Cripes. All right, already. I give. You've got\n |
| 0x70810 | 44 | some scary deductive abilities, y'know that? |
| 0x7083d | 27 | You'll explain, won't you?  |
| 0x70859 | 45 | Ukon smiles wryly, then stands without issue. |
| 0x70887 | 45 | The ropes supposedly "tying him up" flutter\n |
| 0x708b5 | 36 | uselessly to the ground at his feet. |
| 0x708da | 30 | Wh-What bewitcheth yon ropes!? |
| 0x708f9 | 36 | Ah, but first--How'd it go, you two? |
| 0x7091e | 50 | The twins nod, both silently pointing off in the\n |
| 0x70951 | 15 | same direction. |
| 0x70961 | 19 | Hm? When did they-- |
| 0x70975 | 47 | All right, then. Looks like everything's ready. |
| 0x709a5 | 45 | I guess I should make the big reveal, then... |
| 0x709d3 | 51 | Ukon scratches the back of his head, turning back\n |
| 0x70a07 | 10 | toward us. |
| 0x70a12 | 50 | Well, first. Remember how I said no bandit would\n |
| 0x70a45 | 50 | dare attack us? I, uh, might've lied a little bit. |
| 0x70a78 | 4 | Hey! |
| 0x70a7d | 48 | See, this area's been plagued by more and more\n |
| 0x70aae | 49 | bandits and highway robberies like this recently. |
| 0x70ae0 | 52 | Even way out here in Kujyuri, efforts to bring 'em\n |
| 0x70b15 | 29 | in haven't exactly gone well. |
| 0x70b33 | 48 | Seems the bandits in question have been moving\n |
| 0x70b64 | 50 | their stronghold regularly, throwing off the hunt. |
| 0x70b97 | 45 | And all the while, they've been raiding and\n |
| 0x70bc5 | 46 | robbing, scaling up, recruiting new members... |
| 0x70bf4 | 50 | They can't just be left to their own devices, at\n |
| 0x70c27 | 46 | this point. We were asked to take care of 'em. |
| 0x70c56 | 43 | Ukon looks over to Rulutieh apologetically. |
| 0x70c82 | 5 | E-Eh? |
| 0x70c88 | 52 | Sorry for putting you through this mess, princess.\n |
| 0x70cbd | 45 | We thought it'd be better if you didn't know. |
| 0x70ceb | 30 | I-I see... So... that's why... |
| 0x70d0a | 52 | M-Master Ukon! Prithee, speak truth! I knew naught\n |
| 0x70d3f | 15 | of these plans. |
| 0x70d4f | 52 | Yyyeah, about that. Maroro, you're not exactly the\n |
| 0x70d84 | 47 | best actor in the world. Had to minimize risks. |
| 0x70db4 | 11 | I... see... |
| 0x70dc0 | 47 | C'mon, man, it's not like I made the decision\n |
| 0x70df0 | 47 | myself. It was a group thing, we a--men? Men,\n |
| 0x70e20 | 11 | look at me! |
| 0x70e2c | 49 | Well, Maroro's kinda... Yeah. I guess I can see\n |
| 0x70e5e | 48 | that. But hey, doesn't that mean this was a tr-- |
| 0x70e8f | 6 | Urgh-- |
| 0x70e96 | 48 | Wow, kid. Rude. But yes, this was a purposeful\n |
| 0x70ec7 | 49 | trap. Faster to track 'em to their base this way. |
| 0x70ef9 | 50 | Hold on, hold on. I get that, but what would you\n |
| 0x70f2c | 41 | have done if they'd actually ATTACKED us? |
| 0x70f56 | 47 | Thankfully nothing happened, but for a second\n |
| 0x70f86 | 44 | there, things were about to get pretty ugly. |
| 0x70fb3 | 50 | The way that Moznu guy was leering at those two... |
| 0x70fe6 | 52 | Rulutieh must've been scared out of her mind, with\n |
| 0x7101b | 44 | her face buried in Cocopo's fluff like that. |
| 0x71048 | 25 | Hm? Ah, yeah. About that. |
| 0x71062 | 30 | So that's what was going on... |
| 0x71081 | 52 | As Ukon tries to talk around her, Kuon cuts to the\n |
| 0x710b6 | 16 | heart of things. |
| 0x710c7 | 52 | Either there's a traitor in their ranks, or one of\n |
| 0x710fc | 34 | ours infiltrated them. Am I right? |
| 0x7111f | 35 | No wonder things seemed suspicious. |
| 0x71143 | 51 | That's about the shape of it. We'll be joining up\n |
| 0x71177 | 47 | with a company waiting nearby, then attacking\n |
| 0x711a7 | 11 | their base. |
| 0x711b3 | 51 | I know you've got more questions, and you deserve\n |
| 0x711e7 | 48 | answers, but save 'em. Every minute counts, now. |
| 0x71218 | 47 | Oh, no you don't. How can you suggest that so\n |
| 0x71248 | 7 | calmly? |
| 0x71250 | 48 | Escorting cargo I signed on for, but launching\n |
| 0x71281 | 47 | surprise attacks on bandit fortresses? C'mon,\n |
| 0x712b1 | 16 | give me a break. |
| 0x712c2 | 48 | Yeah, I know. I'm not planning on bringing you\n |
| 0x712f3 | 22 | along for this. Relax. |
| 0x7130a | 25 | Saying that, Ukon smiles. |
| 0x71324 | 50 | Instead... I hate to ask this of you, but I need\n |
| 0x71357 | 13 | a tiny favor. |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_05.json` com a forma:
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
