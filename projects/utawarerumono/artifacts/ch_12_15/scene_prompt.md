# Cena ch_12_15 — pacote de traducao (95 linhas)

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
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |

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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Hah... hah... phew...` -> `Hah... hah... ufa...` (Haku, 12_15)
- `I thought this whole thing was supposed to make me\n` -> `Achei que essa coisa toda era pra me deixar\n` (Haku, 12_15)
- `stronger while I sleep. So why am I so tired?` -> `mais forte dormindo. Por que estou tão cansado?` (Haku, 12_15)
- `Not to mention how realistic that was. I thought\n` -> `Sem falar como aquilo foi real. Achei que\n` (Haku, 12_15)
- `I was going to die there.` -> `ia morrer lá dentro.` (Haku, 12_15)
- `Amplified. Double the trouble.` -> `Amplificado. O dobro do problema.` (Homem, 12_15)
- `The amount of exertion required is increased.\n` -> `O esforço exigido é aumentado.\n` (Homem, 12_15)
- `Your fatigue should feel about three times more\n` -> `Sua fadiga deve parecer cerca de três vezes maior\n` (Homem, 12_15)
- `than normal.` -> `que o normal.` (Homem, 12_15)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `You will feel as fresh as a pile of mud.` -> `Vai se sentir fresco como um monte de lama.` (Homem, 12_15)
- `...When you awaken, I am sure you will feel equal\n` -> `...Ao despertar, tenho certeza que sentirá\n` (Homem, 12_15)
- `parts fatigue and intense accomplishment.` -> `partes iguais de fadiga e intensa realização.` (Homem, 12_15)
- `Wh--Hold on, what's that even supposed to mean?\n` -> `Es-- Calma, o que isso quer dizer afinal?\n` (Haku, 12_15)
- `I'm calling it here. Abort! Abort!` -> `Eu cancelo isso. Aborta! Aborta!` (Haku, 12_15)
- `Not possible.` -> `Impossível.` (Homem, 12_15)
- `I am afraid you will have to overcome all the\n` -> `Receio que você tenha que superar todos os\n` (Homem, 12_15)
- `trials before you can awaken.` -> `desafios para poder despertar.` (Homem, 12_15)
- `We forgot to mention, but the line between dream\n` -> `Esquecemos de mencionar, mas a linha entre sonho\n` (Homem, 12_15)
- `and reality can often blur. Please use caution.` -> `e realidade pode se misturar. Tome cuidado.` (Homem, 12_15)
- `Wh-What exactly do you mean by that?` -> `O-O que exatamente quer dizer com isso?` (Haku, 12_15)
- `If you believe that you die within your dream.` -> `Se acreditar que morreu dentro do seu sonho.` (Homem, 12_15)
- `You will kick the bucket in reality, as well.` -> `Você vai bater as botas na realidade também.` (Homem, 12_15)
- `The HELL!?` -> `Que MERDA!?` (Haku, 12_15)
- `gake_parts` -> `gake_parts` (SYSTEM, 12_14)
- `All right! Now we just wait for Kuon to get back,\n` -> `Certo! Agora é só esperar a Kuon voltar,\n` (Haku, 12_15)
- `and... {W230}Huh?` -> `e... {W230}Hein?` (Haku, 12_15)
- `Here's my grand entrance!\n` -> `Minha entrada triunfal!\n` (Kuon, 12_15)
- `Did I keep you waiting, Haku?` -> `Te fiz esperar, Haku?` (Kuon, 12_15)
- `...Well, how do I put it...` -> `...Bom, como eu diria...` (Haku, 12_15)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `We can talk later. Looks like naptime's over.` -> `Conversa depois. Parece que o cochilo acabou.` (Haku, 12_15)
- `Damn, it's persistent. Maroro, it's up to you!` -> `Droga, ele insiste. Maroro, depende de você!` (Ukon, 12_15)
- `Drop it straight down. Your guest is just\n` -> `Joga reto pra baixo. Seu convidado está\n` (Ukon, 12_15)
- `nearby.` -> `perto.` (Ukon, 12_15)
- `W-We shall not fail!` -> `N-Não falharemos!` (Maroro, 12_15)
- `NOW, Maroro!` -> `AGORA, Maroro!` (Ukon, 12_15)
- `We did it...` -> `Conseguimos...` (Ukon, 12_15)
- `Leg_2_B_L` -> `Leg_2_B_L` (SYSTEM, 12_15)
- `Leg_2_B_R` -> `Leg_2_B_R` (SYSTEM, 12_15)
- `The game is over, I think. Are you hurt, Haku?` -> `Acabou, acho. Está machucado, Haku?` (Ukon, 12_15)
- `No, but never mind me. Are you OK?` -> `Não, mas me deixa. Você está bem?` (Haku, 12_15)
- `I'm fine. I did say I was good at running,\n` -> `Estou bem. Eu disse que era boa em correr,\n` (Kuon, 12_15)
- `didn't I?` -> `não disse?` (Kuon, 12_15)
- `Good grief, missy. Teasing a beastie like that\n` -> `Puxa vida, moça. Provocar uma fera desse jeito\n` (Ukon, 12_15)
- `all the way out here... You really are somethin'.` -> `aqui fora... Você é demais mesmo.` (Ukon, 12_15)
- `It's over...` -> `Acabou...` (Haku, 12_15)
- `Yeah, it's over all right.` -> `É, acabou de vez.` (Ukon, 12_15)
- `...Gah, I need a nap.` -> `...Ah, preciso dormir.` (Haku, 12_15)
- `I sag to the ground in sheer relief.` -> `Afundo no chão de puro alívio.` (Haku, 12_15)
- `M-Master Haku, have we won the day?\n` -> `M-Mestre Haku, triunfamos neste dia?\n` (Maroro, 12_15)
- `O-Our lives are yet our own!?` -> `N-Nossas vidas ainda são nossas!?` (Maroro, 12_15)
- `Yeah, it's over now. So you can quit clinging\n` -> `É, acabou. Então para de ficar se\n` (Haku, 12_15)
- `to me so much!` -> `agarrando em mim!` (Haku, 12_15)
- `The day is ours! Oh, the day is OURS, Master Haku!` -> `A vitória é nossa! Oh, a vitória é NOSSA, Mestre Haku!` (Maroro, 12_15)
- `All right, I got it, so just... get off me...` -> `Tá bom, entendi, então... sai de cima de mim...` (Haku, 12_15)
- `Let's head back, Haku. There'll be a feast\n` -> `Vamos voltar, Haku. Vai ter uma festa\n` (Ukon, 12_15)
- `waiting... Fine drink, fine delicacies, and\n` -> `esperando... Boa bebida, boas iguarias e\n` (Ukon, 12_15)
- `a hot bath.` -> `banho quente.` (Kuon, 12_15)
- `Even with us all injured and battered, something\n` -> `Mesmo todos feridos e exaustos, algo\n` (Haku, 12_15)
- `joyful surges inside all of us at Kuon's words.` -> `jubiloso surge em nós todos com as palavras de Kuon.` (Haku, 12_15)
- `Joyous shouts fill the air, and resolve into\n` -> `Gritos de alegria enchem o ar e se transformam em\n` (Haku, 12_15)
- `roars of triumph.` -> `rugidos de triunfo.` (Haku, 12_15)
- `Eyes up, kid! We're not done yet!` -> `Atenção, garoto! Ainda não acabou!` (Ukon, 12_15)
- `O, what unhappy tenacity! ` -> `Ó, que infeliz tenacidade!` (Maroro, 12_15)
- `Sorry, but this is the end!` -> `Desculpe, mas é aqui que acaba!` (Kuon, 12_15)
- `...She's here!` -> `...Ela chegou!` (Ukon, 12_15)
- `I'm back. Haku, are you hurt or anything?` -> `Voltei. Haku, está machucado?` (Kuon, 12_15)
- `M-Master Haku, have we won the day? O-Our lives\n` -> `M-Mestre Haku, triunfamos neste dia? N-Nossas vidas\n` (Maroro, 12_15)
- `are yet our own!?` -> `ainda são nossas!?` (Maroro, 12_15)
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

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x4a4f3 | 21 | Hah... hah... phew... |
| 0x4a509 | 52 | I thought this whole thing was supposed to make me\n |
| 0x4a53e | 45 | stronger while I sleep. So why am I so tired? |
| 0x4a56c | 50 | Not to mention how realistic that was. I thought\n |
| 0x4a59f | 25 | I was going to die there. |
| 0x4a5b9 | 30 | Amplified. Double the trouble. |
| 0x4a5d8 | 47 | The amount of exertion required is increased.\n |
| 0x4a608 | 49 | Your fatigue should feel about three times more\n |
| 0x4a63a | 12 | than normal. |
| 0x4a647 | 6 | What!? |
| 0x4a64e | 40 | You will feel as fresh as a pile of mud. |
| 0x4a677 | 51 | ...When you awaken, I am sure you will feel equal\n |
| 0x4a6ab | 41 | parts fatigue and intense accomplishment. |
| 0x4a6d5 | 49 | Wh--Hold on, what's that even supposed to mean?\n |
| 0x4a707 | 34 | I'm calling it here. Abort! Abort! |
| 0x4a72a | 13 | Not possible. |
| 0x4a738 | 47 | I am afraid you will have to overcome all the\n |
| 0x4a768 | 29 | trials before you can awaken. |
| 0x4a786 | 50 | We forgot to mention, but the line between dream\n |
| 0x4a7b9 | 47 | and reality can often blur. Please use caution. |
| 0x4a7e9 | 36 | Wh-What exactly do you mean by that? |
| 0x4a80e | 46 | If you believe that you die within your dream. |
| 0x4a83d | 45 | You will kick the bucket in reality, as well. |
| 0x4a86b | 10 | The HELL!? |
| 0x4bef3 | 10 | gake_parts |
| 0x4beff | 51 | All right! Now we just wait for Kuon to get back,\n |
| 0x4bf33 | 17 | and... {W230}Huh? |
| 0x4bf45 | 27 | Here's my grand entrance!\n |
| 0x4bf61 | 29 | Did I keep you waiting, Haku? |
| 0x4bf7f | 27 | ...Well, how do I put it... |
| 0x4bf9b | 7 | ...Huh? |
| 0x4bfa3 | 45 | We can talk later. Looks like naptime's over. |
| 0x4bfd1 | 46 | Damn, it's persistent. Maroro, it's up to you! |
| 0x4c000 | 43 | Drop it straight down. Your guest is just\n |
| 0x4c02c | 7 | nearby. |
| 0x4c034 | 20 | W-We shall not fail! |
| 0x4c049 | 12 | NOW, Maroro! |
| 0x4c056 | 12 | We did it... |
| 0x4c063 | 9 | Leg_2_B_L |
| 0x4c06d | 9 | Leg_2_B_R |
| 0x4c077 | 46 | The game is over, I think. Are you hurt, Haku? |
| 0x4c0a6 | 34 | No, but never mind me. Are you OK? |
| 0x4c0c9 | 44 | I'm fine. I did say I was good at running,\n |
| 0x4c0f6 | 9 | didn't I? |
| 0x4c100 | 48 | Good grief, missy. Teasing a beastie like that\n |
| 0x4c131 | 49 | all the way out here... You really are somethin'. |
| 0x4c167 | 12 | It's over... |
| 0x4c174 | 26 | Yeah, it's over all right. |
| 0x4c18f | 21 | ...Gah, I need a nap. |
| 0x4c1a5 | 36 | I sag to the ground in sheer relief. |
| 0x4c1ca | 37 | M-Master Haku, have we won the day?\n |
| 0x4c1f0 | 29 | O-Our lives are yet our own!? |
| 0x4c20e | 47 | Yeah, it's over now. So you can quit clinging\n |
| 0x4c23e | 14 | to me so much! |
| 0x4c24d | 50 | The day is ours! Oh, the day is OURS, Master Haku! |
| 0x4c280 | 45 | All right, I got it, so just... get off me... |
| 0x4c2ae | 44 | Let's head back, Haku. There'll be a feast\n |
| 0x4c2db | 45 | waiting... Fine drink, fine delicacies, and\n |
| 0x4c309 | 11 | a hot bath. |
| 0x4c315 | 50 | Even with us all injured and battered, something\n |
| 0x4c348 | 47 | joyful surges inside all of us at Kuon's words. |
| 0x4c378 | 46 | Joyous shouts fill the air, and resolve into\n |
| 0x4c3a7 | 17 | roars of triumph. |
| 0x4da0e | 10 | gake_parts |
| 0x4da1a | 12 | NOW, Maroro! |
| 0x4da27 | 12 | We did it... |
| 0x4da34 | 33 | Eyes up, kid! We're not done yet! |
| 0x4da56 | 26 | O, what unhappy tenacity!  |
| 0x4da71 | 27 | Sorry, but this is the end! |
| 0x4da8d | 14 | ...She's here! |
| 0x4da9c | 9 | Leg_2_B_L |
| 0x4daa6 | 9 | Leg_2_B_R |
| 0x4dab0 | 41 | I'm back. Haku, are you hurt or anything? |
| 0x4dada | 34 | No, but never mind me. Are you OK? |
| 0x4dafd | 44 | I'm fine. I did say I was good at running,\n |
| 0x4db2a | 9 | didn't I? |
| 0x4db34 | 48 | Good grief, missy. Teasing a beastie like that\n |
| 0x4db65 | 49 | all the way out here... You really are somethin'. |
| 0x4db9b | 12 | It's over... |
| 0x4dba8 | 26 | Yeah, it's over all right. |
| 0x4dbc3 | 21 | ...Gah, I need a nap. |
| 0x4dbd9 | 36 | I sag to the ground in sheer relief. |
| 0x4dbfe | 49 | M-Master Haku, have we won the day? O-Our lives\n |
| 0x4dc30 | 17 | are yet our own!? |
| 0x4dc42 | 47 | Yeah, it's over now. So you can quit clinging\n |
| 0x4dc72 | 14 | to me so much! |
| 0x4dc81 | 50 | The day is ours! Oh, the day is OURS, Master Haku! |
| 0x4dcb4 | 45 | All right, I got it, so just... get off me... |
| 0x4dce2 | 44 | Let's head back, Haku. There'll be a feast\n |
| 0x4dd0f | 45 | waiting... Fine drink, fine delicacies, and\n |
| 0x4dd3d | 11 | a hot bath. |
| 0x4dd49 | 50 | Even with us all injured and battered, something\n |
| 0x4dd7c | 47 | joyful surges inside all of us at Kuon's words. |
| 0x4ddac | 46 | Joyous shouts fill the air, and resolve into\n |
| 0x4dddb | 17 | roars of triumph. |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_15.json` com a forma:
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
