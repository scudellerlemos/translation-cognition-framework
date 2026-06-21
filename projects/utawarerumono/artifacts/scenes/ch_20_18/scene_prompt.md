# Cena ch_20_18 — pacote de traducao (125 linhas)

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
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Man | UI | Homem | traduzir | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Woshis | Personagem | Woshis | manter_original | major |
| Yamatan | Etnia | de Yamato | traduzir | none |
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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Messenger` -> `MENSAGEIRO` (MESSENGER, 20_01)
- `Adviser` -> `Conselheiro` (Yamatan adviser, 20_17)
- `Come in.` -> `Entre.` (Oshtor, 16_02)
- `Silence!` -> `Silêncio!` (Maroro, 19_05)
- `the room.` -> `do aposento.` (Haku, 15_01)
- `sight.` -> `cena estranha.` (Haku, 13_04)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Brigand` -> `Bandido` (SISTEMA, 13_05)
- `the ground.` -> `no chão.` (Haku, 13_05)
- `Hurgh--` -> `Hurgh--` (Maroro, 18_01)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `after all.` -> `afinal.` (Haku, 11_07)
- `Now then...` -> `Bom, então...` (Kuon, 11_02)
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
| 0x208ad5 | 9 | Messenger |
| 0x208adf | 42 | R-Reporting! Our forces in the south are-- |
| 0x208b0e | 7 | Ngh...! |
| 0x208b16 | 35 | What... of our forces in the south? |
| 0x208b3a | 44 | S-Sir... O-Our forces in the south... have\n |
| 0x208b67 | 33 | begun their retreat to regroup... |
| 0x208b89 | 48 | Oh...? Was I not recently told that our forces\n |
| 0x208bba | 42 | had the upper hand just a short while ago? |
| 0x208be5 | 28 | Or did I perhaps mishear...? |
| 0x208c02 | 46 | M-Moments after the report, an army led by a\n |
| 0x208c31 | 45 | masked commander appeared, and our soldiers\n |
| 0x208c5f | 15 | were--Gyaaaakh! |
| 0x208c6f | 41 | The messenger cannot finish his report.\n |
| 0x208c99 | 47 | Gundhurua knocks him down with a vicious blow\n |
| 0x208cc9 | 12 | to the face. |
| 0x208cd6 | 7 | Adviser |
| 0x208cde | 47 | One must remember to relay reports correctly.\n |
| 0x208d0e | 40 | So then, how is the eastern front doing? |
| 0x208d37 | 35 | E-Eastern forces are decimated...\n |
| 0x208d5b | 49 | We lost contact with the capital force, and the\n |
| 0x208d8d | 17 | reinforcements... |
| 0x208d9f | 46 | Th-Then that means the only soldiers we have\n |
| 0x208dce | 34 | left are the ones stationed here!? |
| 0x208df1 | 45 | Gundhurua's men cannot hide their terror as\n |
| 0x208e1f | 45 | report after report of their army's defeats\n |
| 0x208e4d | 8 | come in. |
| 0x208e56 | 8 | Silence! |
| 0x208e5f | 8 | Advisers |
| 0x208e6b | 34 | Gundhurua roars at his shaken men. |
| 0x208e8e | 45 | B-But, my owlo, it is only a matter of time\n |
| 0x208ebc | 43 | before the Yamatan forces will reach this\n |
| 0x208ee8 | 8 | place... |
| 0x208ef1 | 46 | I smell something foul coming from your mouth. |
| 0x208f20 | 46 | Gundhurua grasps his subordinate by his jaw,\n |
| 0x208f4f | 47 | and a sickening cracking noise echoes through\n |
| 0x208f7f | 9 | the room. |
| 0x208f89 | 14 | Agh... Argh... |
| 0x208f98 | 45 | The pitiful retainer lying on the ground is\n |
| 0x208fc6 | 32 | hastily dragged out by soldiers. |
| 0x208fe7 | 33 | Hmph... This war is not over yet. |
| 0x209009 | 26 | If I may speak, my owlo... |
| 0x209024 | 8 | You may. |
| 0x20902d | 47 | We have confirmed that they have successfully\n |
| 0x20905d | 38 | infiltrated Yamato's imperial capital. |
| 0x209084 | 44 | So those dirty little flies have settled...? |
| 0x2090b1 | 49 | The Yamatans will soon know that not all of our\n |
| 0x2090e3 | 32 | battles take place on the field. |
| 0x209104 | 39 | Very well. I hope you can supply some\n |
| 0x20912c | 21 | entertainment for me. |
| 0x209142 | 36 | There is nothing so offensive as a\n |
| 0x209167 | 26 | disappointing performance. |
| 0x209182 | 13 | Yes, my owlo. |
| 0x209190 | 18 | Khahahahahahaha... |
| 0x2091a3 | 36 | A shadow flits across the rooftop.\n |
| 0x2091c8 | 47 | It raises a hand in signal, and other shadows\n |
| 0x2091f8 | 25 | rise all across the city. |
| 0x209212 | 44 | The veiled figures all look to the palace,\n |
| 0x20923f | 48 | dim and dark in the night air, and vanish from\n |
| 0x209270 | 6 | sight. |
| 0x209277 | 5 | Hm... |
| 0x20927d | 45 | Eye contact, please. Yes, good, good... And\n |
| 0x2092ab | 40 | lips should not be touching. Remember,\n |
| 0x2092d4 | 20 | anticipation is key. |
| 0x2092e9 | 39 | Woshis sketches on his drawing board,\n |
| 0x209311 | 45 | illustrating two nude men embracing as they\n |
| 0x20933f | 17 | close in to kiss. |
| 0x209351 | 49 | Before him are his Yatanawarabe, faces red with\n |
| 0x209383 | 47 | embarrassment as they model by his instruction. |
| 0x2093b3 | 50 | Good, good... Hmhmhm. Now I want you to push him\n |
| 0x2093e6 | 45 | down, as though to say "Give up, and you're\n |
| 0x209414 | 6 | mine!" |
| 0x20941b | 46 | The Yatanawarabe look at him with what seems\n |
| 0x20944a | 47 | like disapproval, and Woshis responds with an\n |
| 0x20947a | 7 | excuse. |
| 0x209482 | 50 | Work...? Oh, come now. Ever since the war began,\n |
| 0x2094b5 | 49 | I have dealt with paperwork day after day after\n |
| 0x2094e7 | 4 | day. |
| 0x2094ec | 46 | Truly, what good does all this paperwork do?\n |
| 0x20951b | 48 | We cannot sustain soldiers on documents alone... |
| 0x20954c | 44 | At least let me do as I please after night\n |
| 0x209579 | 46 | falls. I am not causing anyone any harm, am I? |
| 0x2095a8 | 12 | Now, next... |
| 0x2095b5 | 45 | As Woshis places a new sheet on his drawing\n |
| 0x2095e3 | 43 | board, a shadow glides silently behind him. |
| 0x20960f | 48 | A long, thin wire slides out from the shadow's\n |
| 0x209640 | 47 | wrist, and he tries to slip it around Woshis'\n |
| 0x209670 | 6 | neck-- |
| 0x209677 | 7 | Brigand |
| 0x20967f | 45 | Just as he places it around the man's neck,\n |
| 0x2096ad | 29 | the assassin's body stiffens. |
| 0x2096cb | 50 | His body zips upward, as if pulled by something,\n |
| 0x2096fe | 49 | and he is slammed to the ceiling... and then to\n |
| 0x209730 | 11 | the ground. |
| 0x20973c | 7 | Hurgh-- |
| 0x209744 | 46 | The assassin cannot understand what has just\n |
| 0x209773 | 16 | happened to him. |
| 0x209784 | 43 | He is restrained by some invisible force.\n |
| 0x2097b0 | 46 | Unable to move, he stares up at Woshis, eyes\n |
| 0x2097df | 5 | wide. |
| 0x2097e5 | 42 | Beside Woshis, countless other shadows--\n |
| 0x209810 | 47 | different from the assassins--gradually appear. |
| 0x209840 | 32 | An Uzurushan agent... I presume? |
| 0x209861 | 45 | Woshis sighs, as though faintly troubled by\n |
| 0x20988f | 10 | something. |
| 0x20989a | 50 | I do pity your plight... Uzurusha's owlo prefers\n |
| 0x2098cd | 45 | glory in combat, yes? You must be otherwise\n |
| 0x2098fb | 9 | employed. |
| 0x209905 | 45 | If you wish to covertly sway the war, there\n |
| 0x209933 | 35 | are more peaceful ways of doing so. |
| 0x209957 | 47 | Woshis sighs again, deeper and more despondent. |
| 0x209987 | 44 | But this kind of tactic changes nothing...\n |
| 0x2099b4 | 39 | Unfortunate for the both of us, really. |
| 0x2099dc | 44 | As Woshis mutters this, one of the shadows\n |
| 0x209a09 | 30 | quickly whispers into his ear. |
| 0x209a28 | 46 | It seems the other intruders have been dealt\n |
| 0x209a57 | 45 | with. My liege is kept safe by Lady Honoka,\n |
| 0x209a85 | 10 | after all. |
| 0x209a90 | 11 | Now then... |
| 0x209a9c | 46 | Woshis slowly rises from his seat, and looks\n |
| 0x209acb | 48 | into the face of the assassin pinned before him. |
| 0x209afc | 46 | I really am sorry, but I think we have quite\n |
| 0x209b2b | 17 | a lot to discuss. |
| 0x209b3d | 50 | Oh, you needn't worry. I have no intent to cause\n |
| 0x209b70 | 13 | you any pain. |
| 0x209b7e | 23 | Now... Let us commence. |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_18.json` com a forma:
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
