# Cena ch_21_05 — pacote de traducao (273 linhas)

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
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Onvitaikayan | Termo | Onvitaikayan | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Utawarerumono | Título | Utawarerumono | manter_original | none |
| Yamato | Local | Yamato | manter_original | none |

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
### Ougi — criticality: low
- Ougi — `voice_criticality: low`. Irmão da Nosuri; pragmático, parceria com a irmã.
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
- `Guard` -> `Guarda` (Mikazuchi, 18_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `As you wish.` -> `Como desejar.` (Nekone, 14_04)
- `heads.` -> `balançam a cabeça.` (Haku, 13_02)
- `rest.` -> `resto.` (Haku, 20_07)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `otherwise...` -> `senão...` (Haku, 18_01)
- `first.` -> `primeiro.` (Haku, 13_02)
- `dear sister?` -> `cara irmã?` (Nekone, 15_01)
- `like that?` -> `assim?` (Haku, 15_01)
- `now.` -> `já.` (Kuon, 14_04)
- `That is...` -> `Isso é...` (Mulher, 17_01)
- `as well.` -> `também.` (Haku, 17_01)
- `But...` -> `mas...` (Kuon, 11_01)
- `That is all.` -> `É tudo.` (Oshtor, 20_02)
- `this.` -> `essa.` (Moznu, 13_05)
- `Sir Haku?` -> `Sir Haku?` (Rulutieh, 13_02)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `love.` -> `amor.` (Atuy, 15_04)
- `...Haku?` -> `...Haku?` (Garota, 16_01)
- `EEP!?` -> `EEEK!?` (Atuy, 16_01)
- `happening?` -> `acontecendo?` (Garota, 17_01)
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
- Ougi: `Truly most impressive, dearest sister. Your\n` -> `Muito impressionante, querida irmã. Seu charme\n`
- Ougi: `feminine charms dazzle, as ever.` -> `feminino encanta, como sempre.`
- Ougi: `How positively boorish. A good MAN simply\n` -> `Que grosseria. Um bom HOMEM simplesmente\n`
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
| 0x22661d | 20 | Hah... hh... hahh... |
| 0x226632 | 26 | I... I can't... breathe... |
| 0x22664d | 29 | I can... run... no farther... |
| 0x22666b | 5 | Guard |
| 0x226671 | 46 | What happened? Why are you all in such a rush? |
| 0x2266a0 | 44 | As we all scramble out of the ruins, we're\n |
| 0x2266cd | 43 | greeted by the carefree voice of the guard. |
| 0x2266f9 | 50 | I shout to the guard, as loud as my raspy throat\n |
| 0x22672c | 11 | can manage. |
| 0x226738 | 48 | We need to bury this thing and close the place\n |
| 0x226769 | 4 | off! |
| 0x22676e | 38 | Wha--!? What are you talking about...? |
| 0x226795 | 36 | Hurry! Maro, don't just stand there! |
| 0x2267ba | 16 | Bwuh!? R-Right!! |
| 0x2267cb | 34 | Summon all able hands! O, haste!\n |
| 0x2267ee | 45 | We must seal off this accursed tomb without\n |
| 0x22681c | 7 | delay!! |
| 0x226824 | 30 | B-But this is all so sudden.\n |
| 0x226843 | 22 | I don't think we can-- |
| 0x22685a | 49 | This thing's full of Tatari! If we don't hurry,\n |
| 0x22688c | 37 | they're going to start flooding out!! |
| 0x2268b2 | 7 | ...Huh? |
| 0x2268ba | 50 | The guard stands dumbfounded, as though he can't\n |
| 0x2268ed | 27 | comprehend what I'm saying. |
| 0x226909 | 17 | Uruuru! Saraana!! |
| 0x22691b | 12 | As you wish. |
| 0x226928 | 47 | The twins seem to catch my drift, and quickly\n |
| 0x226958 | 49 | pull out the crested box, holding it over their\n |
| 0x22698a | 6 | heads. |
| 0x226991 | 12 | Th-That is-- |
| 0x22699e | 16 | Know your place. |
| 0x2269af | 46 | Cease your impertinence. Do you not see this\n |
| 0x2269de | 7 | emblem? |
| 0x2269e6 | 23 | M-My utmost apologies!! |
| 0x2269fe | 44 | All the guards and scholars who can see us\n |
| 0x226a2b | 40 | quickly get on their knees and bow down. |
| 0x226a54 | 41 | We've got bigger things to worry about!\n |
| 0x226a7e | 49 | Bring all your picks and shovels! We're closing\n |
| 0x226ab0 | 16 | this thing off!! |
| 0x226ac1 | 11 | Y-Yes, sir! |
| 0x226acd | 7 | Hurry!! |
| 0x226ad5 | 47 | The guards and scholars immediately rise, and\n |
| 0x226b05 | 35 | hurriedly help us rebury the ruins. |
| 0x226b29 | 51 | When we have the main entrance sealed off, we all\n |
| 0x226b5d | 51 | crumple to the ground, like puppets whose strings\n |
| 0x226b91 | 8 | are cut. |
| 0x226b9a | 45 | Man oh man... But at least this means we're\n |
| 0x226bc8 | 19 | safe for now, yeah? |
| 0x226bdc | 44 | Yes... For a moment there, I thought I was\n |
| 0x226c09 | 10 | a goner... |
| 0x226c14 | 46 | O me... Verily, I was not expecting a Tatari\n |
| 0x226c43 | 26 | of such vast proportion... |
| 0x226c5e | 42 | I confess I was rather surprised myself.\n |
| 0x226c89 | 45 | It seems your company allows one no time to\n |
| 0x226cb7 | 5 | rest. |
| 0x226cc1 | 36 | A person... changed into a Tatari... |
| 0x226ce6 | 46 | No that's impossible... He was probably just\n |
| 0x226d15 | 25 | eaten by a Tatari, and... |
| 0x226d2f | 48 | No, that can't be. He was definitely a person... |
| 0x226d60 | 16 | A human being... |
| 0x226d71 | 48 | Kuon looks over at me from a little ways away,\n |
| 0x226da2 | 33 | a worried expression on her face. |
| 0x226dc4 | 12 | Hey, Haku... |
| 0x226dd1 | 22 | What exactly was that? |
| 0x226de8 | 45 | I've never heard of a person turning into a\n |
| 0x226e16 | 46 | Tatari... Kuon, do you know anything about it? |
| 0x226e45 | 5 | Huh!? |
| 0x226e4b | 42 | Y-Yea, verily! Milady Kuon, thy grimlike\n |
| 0x226e76 | 45 | reactions bespoke some study of these Tatari. |
| 0x226ea4 | 51 | Of those monsters curse'd we know blessed little.\n |
| 0x226ed8 | 48 | If you've aught to share, speak--'tis surely a\n |
| 0x226f09 | 5 | boon. |
| 0x226f0f | 12 | Milady Kuon? |
| 0x226f1c | 31 | That's... something I can't do. |
| 0x226f3c | 17 | ...M-Milady Kuon? |
| 0x226f4e | 40 | When Kuon finally speaks, her voice is\n |
| 0x226f77 | 49 | uncharacteristically cold. We all stare at her,\n |
| 0x226fa9 | 15 | shocked silent. |
| 0x226fb9 | 49 | ...Uh, I-I just... I can't do it. Talking about\n |
| 0x226feb | 47 | the Tatari is taboo, so... I'm not allowed to\n |
| 0x22701b | 9 | tell you. |
| 0x227025 | 47 | Kuon quickly tries to explain herself, seeing\n |
| 0x227055 | 44 | the bewildered gazes of everyone around her. |
| 0x227082 | 48 | Taboo? Um, dear sister... I know that not many\n |
| 0x2270b3 | 50 | people wish to study them, but I know of no such\n |
| 0x2270e6 | 8 | taboo... |
| 0x2270ef | 50 | Aye, 'tis so. Few would brave the ominous depths\n |
| 0x227122 | 38 | where such direful malignity dwelleth. |
| 0x227149 | 45 | Thus, those who aim to study the fiends are\n |
| 0x227177 | 22 | few and far between... |
| 0x22718e | 30 | Yet this is most intriguing.\n |
| 0x2271ad | 21 | I yearn to know more. |
| 0x2271c3 | 47 | Please, dear sister. Is there some reason why\n |
| 0x2271f3 | 21 | you will not tell us? |
| 0x227209 | 48 | It's just that... maybe we witnessed something\n |
| 0x22723a | 28 | that we shouldn't have seen. |
| 0x227257 | 36 | Something we... shouldn't have seen? |
| 0x22727c | 40 | I think you shouldn't pry any further.\n |
| 0x2272a5 | 12 | Otherwise... |
| 0x2272b2 | 13 | Otherwise...? |
| 0x2272c0 | 28 | You may have to "disappear." |
| 0x2272dd | 23 | Eep!? D-Dear sister...? |
| 0x2272f5 | 31 | Well, that sure sounds ominous. |
| 0x227315 | 41 | You do not appear to be speaking in jest. |
| 0x22733f | 28 | Hmm? What couldst thou mean? |
| 0x22735c | 48 | The way it sounds, I'm guessin' one day you'll\n |
| 0x22738d | 49 | just never be seen again, and nobody'll notice... |
| 0x2273bf | 8 | Zounds!! |
| 0x2273c8 | 45 | Hmm... You mentioned it being taboo before.\n |
| 0x2273f6 | 39 | Does that have something to do with it? |
| 0x22741e | 26 | So you still want to know? |
| 0x227439 | 47 | It's all very enigmatic, but your words don't\n |
| 0x227469 | 50 | make sense to me. I'd like to know all the facts\n |
| 0x22749c | 6 | first. |
| 0x2274a3 | 51 | Ah, the reason she cannot explain it is precisely\n |
| 0x2274d7 | 22 | because it IS taboo... |
| 0x2274ee | 30 | ...I suppose you have a point. |
| 0x22750d | 12 | Dear sister? |
| 0x22751a | 48 | About what we saw today... Have you ever heard\n |
| 0x22754b | 48 | of a person melting and changing into a Tatari\n |
| 0x22757c | 10 | like that? |
| 0x227587 | 40 | No, I have never heard of such things... |
| 0x2275b0 | 47 | I suppose most people would never encounter a\n |
| 0x2275e0 | 45 | Tatari, since they live in cavernous lairs... |
| 0x22760e | 46 | But there have been more and more reports of\n |
| 0x22763d | 19 | sightings in ruins. |
| 0x227651 | 46 | I mean, I've encountered them numerous times\n |
| 0x227680 | 4 | now. |
| 0x227685 | 47 | But there have never been reports of a person\n |
| 0x2276b5 | 23 | changing into a Tatari. |
| 0x2276cd | 49 | Maybe it's just never been seen, but it's still\n |
| 0x2276ff | 43 | odd how little information we have on them. |
| 0x22772b | 16 | And why is that? |
| 0x22773c | 45 | Why haven't the scholars of Yamato tried to\n |
| 0x22776a | 45 | study the ecology, the biology of the Tatari? |
| 0x227798 | 10 | That is... |
| 0x2277a3 | 50 | In my homeland, all things Tatari are considered\n |
| 0x2277d6 | 6 | taboo. |
| 0x2277dd | 50 | We have folktales that those who come in contact\n |
| 0x227810 | 38 | with them will fall ill, or be cursed. |
| 0x227837 | 47 | It felt almost as if everyone wanted to avert\n |
| 0x227867 | 43 | their eyes from the very existence of the\n |
| 0x227893 | 7 | Tatari. |
| 0x22789b | 44 | This is just conjecture, but I believe the\n |
| 0x2278c8 | 47 | people of Yamato avoid Tatari-related matters\n |
| 0x2278f8 | 8 | as well. |
| 0x227901 | 47 | And if there are those who try to find out...\n |
| 0x227931 | 45 | or happen to find out something about them... |
| 0x22795f | 40 | So is that what you mean by "disappear"? |
| 0x227988 | 46 | That's impossible. Why would they go to such\n |
| 0x2279b7 | 11 | lengths...? |
| 0x2279c3 | 46 | I would agree, but what if there's something\n |
| 0x2279f2 | 43 | that we aren't supposed to know about them? |
| 0x227a1e | 35 | Aren't they only slime creatures?\n |
| 0x227a42 | 34 | What about them shouldn't we know? |
| 0x227a65 | 48 | Just what we saw. The truth about the identity\n |
| 0x227a96 | 25 | of the Tatari, I suppose. |
| 0x227ab0 | 50 | Identity...? You suppose that the Tatari did not\n |
| 0x227ae3 | 47 | assume that form unnaturally, but that it was\n |
| 0x227b13 | 14 | once a person? |
| 0x227b22 | 42 | If that is the case, then it does change\n |
| 0x227b4d | 47 | matters. However, that still wouldn't warrant\n |
| 0x227b7d | 11 | all this... |
| 0x227b89 | 47 | Hm. I still don't understand. It's a chilling\n |
| 0x227bb9 | 46 | idea, but what's so bad about it? Can you be\n |
| 0x227be8 | 12 | any clearer? |
| 0x227bf5 | 46 | ...Who exactly do you think that person was?\n |
| 0x227c24 | 37 | The one that came out of that casket? |
| 0x227c4a | 47 | Someone who had been frozen in sleep all this\n |
| 0x227c7a | 50 | time inside a ruin that had remained unexplored... |
| 0x227cad | 48 | What are you talking about? Isn't that exactly\n |
| 0x227cde | 23 | what we'd like to know? |
| 0x227cf6 | 45 | Ah!? Dear sister... you can't be suggesting-- |
| 0x227d24 | 47 | This is just my conjecture, but I don't think\n |
| 0x227d54 | 44 | I'm wrong. That person that changed into a\n |
| 0x227d81 | 9 | Tatari... |
| 0x227d8b | 41 | I believe... he was one from our myths.\n |
| 0x227db5 | 45 | From the ancient advanced civilization that\n |
| 0x227de3 | 16 | ruled our world. |
| 0x227df4 | 49 | The beings that suddenly vanished from history.\n |
| 0x227e26 | 29 | The Utawarerumono themselves. |
| 0x227e44 | 19 | The Onvitaikayan... |
| 0x227e58 | 7 | Gh...!? |
| 0x227e60 | 20 | The Onvitaikayan...? |
| 0x227e75 | 33 | Disappeared... ancient times...\n |
| 0x227e97 | 38 | Then this ruin... Wait, disappeared?\n |
| 0x227ebe | 22 | What does she mean...? |
| 0x227ed5 | 7 | Wait... |
| 0x227edd | 30 | Hold on a second... are you... |
| 0x227efc | 46 | Are you telling me that... that thing was...\n |
| 0x227f2b | 22 | once a human being...? |
| 0x227f42 | 27 | You're... joking... Why...? |
| 0x227f5e | 37 | Guh...!? Urgh... dammit... my head... |
| 0x227f84 | 46 | Countless images blur through my mind. I can\n |
| 0x227fb3 | 46 | feel myself slipping away. Everyone suddenly\n |
| 0x227fe2 | 18 | sounds so distant. |
| 0x227ff5 | 43 | Onvitaikayan... I've heard of them in old\n |
| 0x228021 | 23 | stories, but that is... |
| 0x228039 | 45 | I don't know what exactly caused it, but if\n |
| 0x228067 | 42 | it's true, a lot of this would make sense. |
| 0x228092 | 6 | But... |
| 0x228099 | 47 | If the truth that... the ones we worship, the\n |
| 0x2280c9 | 46 | Onvitaikayan, are what the Tatari truly are... |
| 0x2280f8 | 45 | And that's why I want you all to keep quiet\n |
| 0x228126 | 32 | about it. Do you understand now? |
| 0x228147 | 48 | My, my... Yes, this all seems a bit more heavy\n |
| 0x228178 | 21 | than I was expecting. |
| 0x22818e | 43 | ...We saw nothing here, and we don't know\n |
| 0x2281ba | 18 | anything about it. |
| 0x2281cd | 13 | Are we clear? |
| 0x2281db | 46 | Yes. What you say is... most likely correct,\n |
| 0x22820a | 44 | dear sister. If word of this ever got out... |
| 0x228237 | 50 | Hmm. Well, if that's how it is, I'll keep quiet.\n |
| 0x22826a | 17 | Sound good, Ougi? |
| 0x22827c | 47 | Are you sure about this? Such information may\n |
| 0x2282ac | 35 | prove to be valuable in the future. |
| 0x2282d0 | 26 | I am above such methods.\n |
| 0x2282eb | 12 | That is all. |
| 0x2282f8 | 43 | Very well. If that is your decision, dear\n |
| 0x228324 | 26 | sister, I can only follow. |
| 0x22833f | 43 | O lamentable, that I must forgo such rare\n |
| 0x22836b | 45 | knowledge in the name of self-preservation... |
| 0x228399 | 42 | But o'conscience, I promise thee I shall\n |
| 0x2283c4 | 19 | breathe not a word. |
| 0x2283d8 | 44 | You know, they say that tellin' someone to\n |
| 0x228405 | 48 | keep a secret just makes 'em want to spill it... |
| 0x228436 | 16 | Sir Jachdwalt... |
| 0x228447 | 47 | Relax. Kidding. Thinkin' ain't my job anyway.\n |
| 0x228477 | 44 | I'll stick to whatever the boss decides on\n |
| 0x2284a4 | 6 | doing. |
| 0x2284ab | 23 | Well, that's how it is. |
| 0x2284c3 | 46 | Kuon turns to Uruuru and Saraana as she says\n |
| 0x2284f2 | 5 | this. |
| 0x2284f8 | 46 | Uruuru and Saraana stay completely silent as\n |
| 0x228527 | 48 | they stare at Kuon with blank, emotionless eyes. |
| 0x228558 | 18 | Um... Sir Haku...? |
| 0x22856b | 48 | ...Oh right. Haku. Can I... ask you something,\n |
| 0x22859c | 10 | I suppose? |
| 0x2285a7 | 39 | It's about when we entered that room... |
| 0x2285cf | 47 | Oh, yes! The lights turned on, and everything\n |
| 0x2285ff | 44 | began to move on its own. What happened in\n |
| 0x22862c | 6 | there? |
| 0x228633 | 46 | Sir Haku...? You're looking somewhat pale...\n |
| 0x228662 | 9 | Sir Haku? |
| 0x22866c | 13 | Huh...? Haku? |
| 0x22867a | 5 | Haku? |
| 0x228680 | 50 | Oh dear. You're looking a bit under the weather,\n |
| 0x2286b3 | 5 | love. |
| 0x2286b9 | 29 | Haku, are you hurt somewhere? |
| 0x2286d7 | 24 | Is it something you ate? |
| 0x2286f0 | 35 | M-Master Haku, is aught amiss...?\n |
| 0x228714 | 12 | Master Haku? |
| 0x228721 | 34 | Boss, what's wrong...!? Hey, boss! |
| 0x228744 | 8 | ...Haku? |
| 0x22874d | 22 | Gh... AAAGGGHHHHHHHH!! |
| 0x228764 | 5 | Eep!? |
| 0x22876a | 8 | Master!! |
| 0x228773 | 26 | Boss! What's wrong, boss!? |
| 0x22878e | 30 | Is this the Tatari's curse...? |
| 0x2287ad | 42 | I-It can't be... Maroro, what exactly is\n |
| 0x2287d8 | 10 | happening? |
| 0x2287e3 | 32 | I-I-I am true incertain, myself! |
| 0x228804 | 45 | Everyone, remain calm. We must find a place\n |
| 0x228832 | 18 | where he can rest. |
| 0x228845 | 8 | R-Right! |
| 0x22884e | 32 | Kiwi! You hold him on that side. |
| 0x22886f | 23 | Um... I... What do I... |
| 0x228887 | 32 | Tch. I'll do it. Out of the way. |
| 0x2288a8 | 10 | S-Sorry... |
| 0x2288b3 | 27 | Oh... Oh no... Sir Haku!?\n |
| 0x2288cf | 10 | Sir Haku!? |
| 0x2288da | 13 | Master Haku!! |
| 0x2288e8 | 12 | Ha... ku...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_21_05.json` com a forma:
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
