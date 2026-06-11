# Cena ch_13_03 — pacote de traducao (166 linhas)

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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Ukon** (major): ANTES de 13_08: trate Ukon como mercenario espirituoso por si so. NAO insinue patente, nobreza, vinculo imperial nem o nome 'Oshtor'. Preserve a ambiguidade do original (que usa 'Ukon').

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `What are you doing?` -> `O que você tá fazendo?` (Haku, 11_10)
- `Guh--` -> `Agh--` (Man, root)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Haku?` -> `Haku?` (Kuon, 11_07)
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
| 0x68441 | 13 | Hmm, hm hm... |
| 0x6844f | 47 | Kuon boils the water I'd fetched for her in a\n |
| 0x6847f | 40 | large, metallic tub, humming to herself. |
| 0x684a8 | 47 | I lost count of how many trips it took to get\n |
| 0x684d8 | 37 | enough water to fill that thing up... |
| 0x684fe | 47 | What is she boiling all this water for, anyway? |
| 0x6852e | 52 | It's not like she's cooking a hotpot or something.\n |
| 0x68563 | 47 | We just ate, and there's way too much for that. |
| 0x68593 | 48 | Not that I doubt she'd be able to eat that much. |
| 0x685c4 | 46 | Hmm, hm hm... The water's juuuust about right. |
| 0x685f3 | 53 | She tests the water with her hand, then--apparently\n |
| 0x68629 | 41 | satisfied--pours it into a different tub. |
| 0x68653 | 51 | The remaining water goes back on top of the fire,\n |
| 0x68687 | 47 | and she adds more from the buckets I'd fetched. |
| 0x686b7 | 50 | She's going through water like it's going out of\n |
| 0x686ea | 12 | style, here. |
| 0x686f7 | 51 | I'm probably going to feel stupid for asking, but\n |
| 0x6872b | 19 | what are you doing? |
| 0x6873f | 28 | Preparing a bath, obviously. |
| 0x6875c | 48 | Yeah, I had a feeling. I didn't think she'd go\n |
| 0x6878d | 33 | through all this trouble, though. |
| 0x687af | 47 | You're going out of your way to boil all that\n |
| 0x687df | 39 | water in the middle of a campground...? |
| 0x68807 | 48 | Sure. A bath feels great after proper hard work. |
| 0x68838 | 46 | "Proper hard work." But I'm the one who went\n |
| 0x68867 | 26 | through all the trouble... |
| 0x68882 | 33 | Step back a bit, would you, Haku? |
| 0x688a4 | 48 | My griping falls on deaf ears as Kuon drapes a\n |
| 0x688d5 | 46 | large sheet over a string to make a partition. |
| 0x68909 | 47 | The telltale rustling of clothes is perfectly\n |
| 0x68939 | 30 | audible through the partition. |
| 0x68958 | 28 | She's as brazen as always... |
| 0x68975 | 50 | But to think she'd go to such lengths just for a\n |
| 0x689a8 | 33 | bath. She must REALLY enjoy them. |
| 0x689ca | 11 | *Splish*... |
| 0x689d6 | 34 | Ahh... This is just what I needed. |
| 0x689f9 | 51 | She must have lowered herself into the water, for\n |
| 0x68a2d | 46 | a soft exclamation of comfort wafts over the\n |
| 0x68a5c | 8 | barrier. |
| 0x68a65 | 30 | You like baths that much, huh? |
| 0x68a84 | 15 | Mhm. Very much. |
| 0x68a94 | 49 | Washing away a hard day's sweat with a hot bath\n |
| 0x68ac6 | 29 | is the best feeling there is. |
| 0x68ae4 | 51 | Honestly, if I had my way I'd take two a day, but\n |
| 0x68b18 | 36 | I suppose beggars can't be choosers. |
| 0x68b3d | 51 | ...What, is she waiting for some kind of quip for\n |
| 0x68b71 | 15 | that? A retort? |
| 0x68b81 | 45 | Do you do this all the time when you're out\n |
| 0x68baf | 20 | traveling like this? |
| 0x68bc4 | 51 | Mm. I know it's a bit extravagant, but as long as\n |
| 0x68bf8 | 50 | I prepare it myself, it's not like I'm bothering\n |
| 0x68c2b | 7 | anyone. |
| 0x68c33 | 44 | I'm the one who did all the heavy lifting,\n |
| 0x68c60 | 9 | though... |
| 0x68c6a | 48 | So, thanks. I'm grateful for you helping me out. |
| 0x68c9b | 22 | Nngh. Sharp as always. |
| 0x68cb2 | 42 | I lean back and lounge against our piled\n |
| 0x68cdd | 22 | belongings, exhausted. |
| 0x68cf4 | 11 | *Sssslip--* |
| 0x68d00 | 49 | Then, shifting in a chain reaction, the part of\n |
| 0x68d32 | 39 | the string held up by our bags shifts-- |
| 0x68d5a | 12 | *Flutter*... |
| 0x68d67 | 5 | Guh-- |
| 0x68d6d | 4 | Hmm~ |
| 0x68d72 | 17 | W-Wait, why did-- |
| 0x68d84 | 51 | Over the fallen partition, I see Kuon has covered\n |
| 0x68db8 | 37 | her eyes with a washcloth, oblivious. |
| 0x68dde | 51 | She keeps humming to herself, kicking her legs in\n |
| 0x68e12 | 10 | the water. |
| 0x68e1d | 52 | ...I admit it's a pleasant sight, but I can't ogle\n |
| 0x68e52 | 14 | her like this. |
| 0x68e61 | 51 | Kuon's tail gracefully flicking back and forth is\n |
| 0x68e95 | 19 | almost hypnotizing. |
| 0x68ea9 | 28 | N-Not good. Not good at all. |
| 0x68ec6 | 52 | No, no, calm down. It was an accident, and knowing\n |
| 0x68efb | 39 | Kuon, she'll just smile and forgive me. |
| 0x68f23 | 18 | She'll... smile... |
| 0x68f36 | 52 | ...She might smile, but her eyes won't be smiling.\n |
| 0x68f6b | 41 | And that dangerous tail will be swinging. |
| 0x68f95 | 50 | B-But if I put the partition back the way it was\n |
| 0x68fc8 | 22 | before it's too late-- |
| 0x68fdf | 51 | Taking extreme care not to make any noise or draw\n |
| 0x69013 | 45 | attention, I try to pull the sheet back up... |
| 0x69041 | 9 | Hm, hm... |
| 0x6904b | 52 | Good... Slide that back into place like that, then\n |
| 0x69080 | 43 | all I have to do is tie off the edges and-- |
| 0x690ac | 9 | *Slip*... |
| 0x690b6 | 7 | ...Huh? |
| 0x690be | 49 | My hand slips right as I finish, and instead of\n |
| 0x690f0 | 50 | tightening the knot properly, it all comes undone. |
| 0x69127 | 50 | No, what are you doing!? Stop! Just stop! You're\n |
| 0x6915a | 16 | making it worse! |
| 0x6916b | 10 | Ah, right. |
| 0x69176 | 52 | Kuon pulls the washcloth off of her eyes as though\n |
| 0x691ab | 31 | suddenly remembering something. |
| 0x691cb | 5 | Ack-- |
| 0x691d1 | 47 | But without turning around, she reaches for a\n |
| 0x69201 | 46 | small bottle and dumps its contents into the\n |
| 0x69230 | 6 | water. |
| 0x69237 | 23 | Ah, that smells nice... |
| 0x6924f | 51 | Then--still oblivious--she re-soaks the washcloth\n |
| 0x69283 | 40 | and replaces it over her eyes once more. |
| 0x692ac | 50 | Th-That was close. If she'd turned her head even\n |
| 0x692df | 40 | a few degrees, it would've been the end. |
| 0x69308 | 7 | Hm, hm~ |
| 0x69310 | 49 | Kuon happily swings her legs and hums a tune, a\n |
| 0x69342 | 47 | stark contrast with what I'm feeling right now. |
| 0x69372 | 48 | Haku, you've gone all quiet. Is something wrong? |
| 0x693a3 | 52 | No, I just dunno what to say. No one else is here,\n |
| 0x693d8 | 49 | so it's gonna be quiet if I'm not talking to you. |
| 0x6940a | 51 | I suppose. You just got awfully quiet in a hurry,\n |
| 0x6943e | 38 | and I was worried something was wrong. |
| 0x69465 | 48 | Hmhm. You weren't thinking about peeking, were\n |
| 0x69496 | 17 | you, naughty boy? |
| 0x694a8 | 5 | Geh-- |
| 0x694ae | 47 | D-D-Don't be ridiculous. Who'd ever do such a\n |
| 0x694de | 6 | thing? |
| 0x694e5 | 50 | Ahahaha, calm down. I'm just kidding. I know you\n |
| 0x69518 | 9 | wouldn't. |
| 0x69522 | 39 | W-Well, as long as we're clear on that. |
| 0x6954a | 51 | Nngh, this isn't weighing well on my conscience--\n |
| 0x6957e | 50 | But I'm NOT peeking! Absolutely not! Not my fault! |
| 0x695b1 | 44 | ...Looks like I've got nothing left but my\n |
| 0x695de | 17 | contingency plan. |
| 0x695f0 | 39 | I stealthily tiptoe to the tent's flap. |
| 0x69618 | 27 | Yep. No choice but to bail! |
| 0x69634 | 49 | Even if she realizes what happened here, she'll\n |
| 0x69666 | 45 | probably let it drop by tomorrow. Probably... |
| 0x69694 | 45 | ...Maybe Ukon will let me sleep in his tent\n |
| 0x696c2 | 18 | instead of Kuon's. |
| 0x696d5 | 50 | I creep ever closer toward the exit, and spare a\n |
| 0x69708 | 36 | glance over my shoulder toward Kuon. |
| 0x6972d | 44 | Her skin is flawless, free of any scars or\n |
| 0x6975a | 50 | blemishes, her figure is tight and fit, her face\n |
| 0x6978d | 11 | pleasant... |
| 0x69799 | 50 | "Exquisite" is a good word for her kind of beauty. |
| 0x697cc | 50 | ...Now, personally, I prefer women with a little\n |
| 0x697ff | 35 | more, uh... endowment than she has. |
| 0x69823 | 51 | With everything else Kuon has going for her, it's\n |
| 0x69857 | 33 | actually almost... disappointing? |
| 0x69879 | 5 | Haku? |
| 0x6987f | 46 | Kuon raises her head from the water, and the\n |
| 0x698ae | 47 | washcloth slides off her eyes with an ominous\n |
| 0x698de | 5 | plop. |
| 0x698e4 | 11 | She smiles. |
| 0x698f0 | 36 | And just as I thought, those eyes... |
| 0x69915 | 46 | The smile doesn't quite... extend to her eyes. |
| 0x69944 | 28 | Her tail uncurls sinuously-- |
| 0x69961 | 49 | No, wait--Wait, it wasn't on purpose! The cloth\n |
| 0x69993 | 22 | came apart on its own! |
| 0x699aa | 50 | Never mind that. I'd like you to tell me what it\n |
| 0x699dd | 40 | was, exactly, you found "disappointing?" |
| 0x69a06 | 45 | Wh-What are you talking about? I didn't say\n |
| 0x69a34 | 20 | anything like that-- |
| 0x69a49 | 49 | I only thought it was a bit of a disappointment\n |
| 0x69a7b | 49 | that she isn't a little bigger through the ch--\n |
| 0x69aad | 6 | ...Oh. |
| 0x69ab4 | 46 | You sighed all disappointedly. What was that\n |
| 0x69ae3 | 6 | about? |
| 0x69aea | 12 | I sighed...? |
| 0x69af7 | 51 | Kuon's prehensile tail curls around the handle of\n |
| 0x69b2b | 34 | a bubbling, boiling pot and lifts. |
| 0x69b4e | 38 | N-No--Wait, I promise, this is all a\n |
| 0x69b75 | 17 | misunderstanding! |
| 0x69b87 | 32 | You've got it all wrong, liste-- |
| 0x69ba8 | 10 | AIIEEEEE!! |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_03.json` com a forma:
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
