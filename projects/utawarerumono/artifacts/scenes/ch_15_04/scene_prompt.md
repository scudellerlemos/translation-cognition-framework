# Cena ch_15_04 — pacote de traducao (224 linhas)

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
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/evidence/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acent
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| amam | Item | amam | manter_original | none |
| Atuy | Personagem | Atuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `but...` -> `mas...` (Kuon, 12_16)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `Wh--?` -> `Qu--?` (Haku, 12_03)
- `Girl` -> `Garota` (sistema, 13_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `R-Really?` -> `S-Sério?` (Haku, 11_06)
- `are you?` -> `coisa assim, vai?` (Haku, 13_02)
- `That's...` -> `Isso...` (Haku, 15_01)
- `trouble.` -> `de verdade.` (Haku, 12_04)
- `acquaintance of yours?` -> `essa pessoa?` (Rulutieh, 13_01)
- `acquaintance.` -> `conhecer você.` (Kuon, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `...What.` -> `...Que isso.` (Kuon, 11_04)
- `I-I see.` -> `A-Entendo.` (Nekone, 14_04)
- `S-Sure...` -> `P-Pode deixar...` (Haku, 13_08)
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
| 0xb785c | 44 | I find myself wandering the market streets\n |
| 0xb7889 | 10 | aimlessly. |
| 0xb7894 | 40 | I'm supposed to be gathering potential\n |
| 0xb78bd | 46 | collaborators for that thing Ukon mentioned,\n |
| 0xb78ec | 6 | but... |
| 0xb78f3 | 43 | Eh. No point in unnecessarily rushing the\n |
| 0xb791f | 47 | process. I'll find good talent sooner or later. |
| 0xb794f | 46 | As I walk, I munch thoughtfully on the snack\n |
| 0xb797e | 32 | I'd bought from a street vendor. |
| 0xb799f | 16 | *Hromf, nomf*... |
| 0xb79b0 | 44 | Hm. Fermented and steamed amam dough, huh... |
| 0xb79dd | 49 | It's fluffy, subtly sweet, just chewy enough...\n |
| 0xb7a0f | 47 | I'm doing better at finding food than talent,\n |
| 0xb7a3f | 5 | here. |
| 0xb7a45 | 16 | Hullo, handsome. |
| 0xb7a56 | 47 | As I reach into the bag for my second hunk of\n |
| 0xb7a86 | 48 | steamed dough, a voice whispers right by my ear. |
| 0xb7ab7 | 5 | Wh--? |
| 0xb7abd | 45 | I whirl on the spot, and behind me I find a\n |
| 0xb7aeb | 44 | young, gentle-looking woman staring me down. |
| 0xb7b18 | 48 | Oh, dear. You looked handsome from behind, but\n |
| 0xb7b49 | 44 | that face is a bit of a consolation prize,\n |
| 0xb7b76 | 12 | isn't it...? |
| 0xb7b83 | 38 | ...A-And she's the type to just make\n |
| 0xb7baa | 44 | observations like that out loud, apparently. |
| 0xb7bd7 | 49 | I can FEEL her radiating disappointment just by\n |
| 0xb7c09 | 25 | standing near her. Yikes. |
| 0xb7c23 | 4 | Girl |
| 0xb7c28 | 47 | Ah, well. Hey, love, could I ask you for some\n |
| 0xb7c58 | 29 | directions while you're here? |
| 0xb7c76 | 48 | And then she just talks to me as if she'd said\n |
| 0xb7ca7 | 47 | nothing at all. Does she just have zero filter? |
| 0xb7cd7 | 47 | I'm looking for an inn called the Hakurokaku?\n |
| 0xb7d07 | 43 | It's listed in "The Empire's Top 100 Inns." |
| 0xb7d33 | 19 | The Hakurokaku Inn? |
| 0xb7d47 | 51 | Asking about a "Hakurokaku Inn" in the capital...\n |
| 0xb7d7b | 33 | Well, she can only mean THAT one. |
| 0xb7d9d | 30 | Yeah, you could say I know it. |
| 0xb7dbc | 48 | Really? Hey, would you mind telling a girl how\n |
| 0xb7ded | 13 | to get there? |
| 0xb7dfb | 32 | Yeah, you take this street and-- |
| 0xb7e1c | 45 | ...You know what? I was about to head back,\n |
| 0xb7e4a | 35 | anyway. I'll just show her the way. |
| 0xb7e6e | 35 | Hmm. D'you live at the inn, then?\n |
| 0xb7e92 | 30 | That means we'll be neighbors! |
| 0xb7eb1 | 10 | Neighbors? |
| 0xb7ebc | 48 | That's right! Starting today, I'm staying there. |
| 0xb7eed | 5 | Hm... |
| 0xb7ef7 | 47 | Her gaze on me is... no, her gaze on what I'm\n |
| 0xb7f27 | 38 | eating is really distracting me, here. |
| 0xb7f4e | 47 | Ngh. Hard to eat with you just staring at me,\n |
| 0xb7f7e | 5 | lady. |
| 0xb7f84 | 16 | That looks good. |
| 0xb7f95 | 17 | ...You want some? |
| 0xb7fa7 | 49 | Left with no real choice in the matter, I break\n |
| 0xb7fd9 | 32 | off a piece and offer it to her. |
| 0xb7ffa | 35 | Really? You didn't have to, love.\n |
| 0xb801e | 10 | Thank you! |
| 0xb8029 | 44 | No, you were pretty clearly asking me with\n |
| 0xb8056 | 17 | your eyes, there. |
| 0xb8068 | 39 | You're a good person, love. I'm Atuy!\n |
| 0xb8090 | 17 | What's your name? |
| 0xb80a2 | 4 | Huh? |
| 0xb80a7 | 22 | Name. Your name, love. |
| 0xb80be | 29 | Oh, uh. Haku. My name's Haku. |
| 0xb80dc | 29 | Haku, eh? That's a nice name. |
| 0xb80fa | 9 | R-Really? |
| 0xb8104 | 46 | Come to think of it, no one has complimented\n |
| 0xb8133 | 46 | my name before. Kuon, maybe, but she came up\n |
| 0xb8162 | 10 | with it... |
| 0xb816d | 26 | I guess it IS a nice name. |
| 0xb8188 | 48 | Even if it's not my "real" name, I find myself\n |
| 0xb81b9 | 48 | blushing at the remark. I'm genuinely flattered. |
| 0xb81ea | 37 | ...Hey, why so quiet all of a sudden? |
| 0xb8210 | 43 | ...Bah. You really are disappointing, love. |
| 0xb823c | 40 | Not only ignoring me, but calling me a\n |
| 0xb8265 | 30 | disappointment. What the hell? |
| 0xb8284 | 46 | From behind, you're so attractive, I thought\n |
| 0xb82b3 | 39 | I'd met my soulmate right here and now. |
| 0xb82db | 48 | But to think, when you turned around... I want\n |
| 0xb830c | 47 | that spark of love at first sight back, please. |
| 0xb833c | 49 | Spark, my ass. How about giving me my shattered\n |
| 0xb836e | 49 | heart back? Buttering me up and then letting me\n |
| 0xb83a0 | 7 | drop... |
| 0xb83a8 | 47 | What are you even trying to say? I can't tell\n |
| 0xb83d8 | 43 | if you're insulting me or complimenting me. |
| 0xb8404 | 27 | Huh? I'm complimenting you. |
| 0xb8420 | 14 | ...Is that so. |
| 0xb842f | 46 | Hey, hey, so what's the Hakurokaku Inn like?\n |
| 0xb845e | 46 | This is my first time in the imperial capital. |
| 0xb848d | 49 | I don't really know what to tell you, honestly.\n |
| 0xb84bf | 33 | It's... got a huge bath, I guess? |
| 0xb84e1 | 44 | The lodgings are comfortable, the beds are\n |
| 0xb850e | 47 | spacious, the food's pretty good... and yeah,\n |
| 0xb853e | 9 | the bath. |
| 0xb8548 | 43 | From what I was told, there isn't another\n |
| 0xb8574 | 45 | communal bath that big in the entire capital. |
| 0xb85a2 | 50 | Wow. I'll look forward to that, then. Looks like\n |
| 0xb85d5 | 46 | I made the right decision to leave home, eh,\n |
| 0xb8604 | 5 | love? |
| 0xb860a | 49 | ...Leave home? You're not some kind of runaway,\n |
| 0xb863c | 8 | are you? |
| 0xb8645 | 44 | Eh? No, I left home because Papa told me to. |
| 0xb8672 | 50 | It's a big tradition, see--coming to the capital\n |
| 0xb86a5 | 42 | for Her Highness' nativity festival, yeah? |
| 0xb86d0 | 51 | So here I am, stranger in a strange city, arrived\n |
| 0xb8704 | 48 | from distant lands just in time for the big day. |
| 0xb8735 | 9 | That's... |
| 0xb873f | 39 | Is she like Rulutieh and Kiwru, then?\n |
| 0xb8767 | 23 | A noble family's child? |
| 0xb877f | 49 | Come to think of it, she does have a sort of...\n |
| 0xb87b1 | 44 | otherworldliness to her. A foreign kind of\n |
| 0xb87de | 11 | refinement. |
| 0xb87ea | 47 | But I guess a proper noble lady would have an\n |
| 0xb881a | 45 | attendant of some kind. Am I overthinking it? |
| 0xb8848 | 34 | Hey, so what about the procession? |
| 0xb886b | 46 | I'm not trying to trick the truth out of her\n |
| 0xb889a | 42 | or anything, but... It's worth it to ask\n |
| 0xb88c5 | 9 | politely. |
| 0xb88cf | 47 | Hm? Ah, all that. It was all a bit boring and\n |
| 0xb88ff | 38 | sort of a nuisance, so I slipped away. |
| 0xb8926 | 46 | I figured as much. Good thing I went with my\n |
| 0xb8955 | 6 | hunch. |
| 0xb895c | 48 | Besides, this is my first time in the capital!\n |
| 0xb898d | 25 | I want to live as I like. |
| 0xb89a7 | 43 | Papa arranged a manor for me, but really,\n |
| 0xb89d3 | 44 | I just want to keep to myself. No big fuss\n |
| 0xb8a00 | 13 | or pomp, see. |
| 0xb8a0e | 29 | Provided a manor? That's...\n |
| 0xb8a2c | 24 | He went pretty far, huh. |
| 0xb8a45 | 47 | And she broke away without telling anyone and\n |
| 0xb8a75 | 48 | wants to hide out at the inn. This smells like\n |
| 0xb8aa6 | 8 | trouble. |
| 0xb8aaf | 36 | ...Eh. Not gonna let it ruin my day. |
| 0xb8ad4 | 49 | Atuy keeps stopping every five feet, new stalls\n |
| 0xb8b06 | 35 | and displays catching her interest. |
| 0xb8b2a | 47 | Accompanying her to inspect each soaks up way\n |
| 0xb8b5a | 45 | too much time, but ultimately, we arrive at\n |
| 0xb8b88 | 8 | the inn. |
| 0xb8b91 | 47 | Oh, wow. It's lovely. I've never seen a place\n |
| 0xb8bc1 | 42 | that radiates such an exotic atmosphere... |
| 0xb8bec | 42 | Yes, I definitely made the right choice.\n |
| 0xb8c17 | 42 | This'll be loads more fun than the manor\n |
| 0xb8c42 | 15 | Papa had ready. |
| 0xb8c52 | 25 | Oh, welcome back, Haku.\n |
| 0xb8c6c | 12 | How'd it go? |
| 0xb8c79 | 49 | As we approach the gate, Kuon meets us halfway,\n |
| 0xb8cab | 44 | ostensibly leaving for some errand or other. |
| 0xb8cd8 | 50 | Huh? O-Oh. Uh, nothing really notable to report,\n |
| 0xb8d0b | 14 | I'm afraid...? |
| 0xb8d1a | 40 | I see. Ah, I guess it can't be helped.\n |
| 0xb8d43 | 43 | We shouldn't force it--we'll find someone\n |
| 0xb8d6f | 11 | eventually. |
| 0xb8d7b | 5 | Yeah. |
| 0xb8d81 | 44 | Crap, I completely forgot about the talent\n |
| 0xb8dae | 9 | search... |
| 0xb8db8 | 49 | Oh, what a beauty YOU are. Hey, love, is she an\n |
| 0xb8dea | 22 | acquaintance of yours? |
| 0xb8e01 | 17 | Acquaintance...\n |
| 0xb8e13 | 33 | Well, she lives here with me, so. |
| 0xb8e35 | 17 | Who's this, Haku? |
| 0xb8e47 | 47 | Oh, another guest of the inn, starting today.\n |
| 0xb8e77 | 36 | I was just showing her the way here. |
| 0xb8e9c | 48 | Atuy! I'll be staying here for a while. Charmed. |
| 0xb8ecd | 41 | I see... I'm Kuon. Pleased to make your\n |
| 0xb8ef7 | 13 | acquaintance. |
| 0xb8f05 | 46 | We've made this our temporary residence just\n |
| 0xb8f34 | 46 | like you, so if you ever need anything, come\n |
| 0xb8f63 | 8 | find us. |
| 0xb8f6c | 22 | Eh hee hee. Hey, love? |
| 0xb8f83 | 3 | Hm? |
| 0xb8f87 | 46 | Are you, by any chance...? You know, you and\n |
| 0xb8fb6 | 27 | Kuon. Are you two an item~? |
| 0xb8fd2 | 8 | ...What. |
| 0xb8fdb | 11 | You're not? |
| 0xb8fe7 | 17 | Nope. Not at all. |
| 0xb8ff9 | 48 | Really? You're telling me you two aren't MADLY\n |
| 0xb902a | 24 | in love with each other? |
| 0xb9043 | 44 | Not even a bit. If anything, she's like...\n |
| 0xb9070 | 14 | my benefactor. |
| 0xb907f | 43 | Me, lovers with Kuon? The thought's never\n |
| 0xb90ab | 21 | even crossed my mind. |
| 0xb90c1 | 45 | Ahaha. Sorry to burst your bubble, but Haku\n |
| 0xb90ef | 40 | and I aren't like that in the slightest. |
| 0xb9118 | 27 | Aw, so you really aren't... |
| 0xb9134 | 26 | Why is THAT disappointing? |
| 0xb914f | 47 | Hm? Oh! See, if you were, I was gonna ask you\n |
| 0xb917f | 42 | all sorts of questions for, um. Reference. |
| 0xb91aa | 51 | If you were lovers, I figured you'd be doing this\n |
| 0xb91de | 45 | and that, and I could pick up some tips, see. |
| 0xb920c | 22 | "Th-This... and that?" |
| 0xb9223 | 48 | I'm in the capital, after all! I'm not blowing\n |
| 0xb9254 | 48 | my chance to have a full-blown passionate love\n |
| 0xb9285 | 7 | affair. |
| 0xb928d | 48 | Eh hee hee. It's a little embarrassing, I guess. |
| 0xb92be | 48 | You came to the heart of the empire for... love. |
| 0xb92ef | 26 | You know! FALLING in love. |
| 0xb930a | 8 | I-I see. |
| 0xb9313 | 43 | At least she's open about what she wants... |
| 0xb933f | 18 | Love... Love, huh. |
| 0xb9352 | 50 | Well, then! I think I'm off for a nap. Papa sent\n |
| 0xb9385 | 46 | his four strongest to escort me home, so I'm\n |
| 0xb93b4 | 7 | winded. |
| 0xb93bc | 47 | Hee. I crushed them easily enough, of course,\n |
| 0xb93ec | 46 | but it's tiring work looking out for yourself! |
| 0xb941b | 43 | ...And she definitely just said something\n |
| 0xb9447 | 45 | unbelievable with utter nonchalance. Right,\n |
| 0xb9475 | 3 | OK. |
| 0xb9479 | 44 | Oh, if you're tired, go try out the baths.\n |
| 0xb94a6 | 23 | They're wonderful here. |
| 0xb94be | 44 | I'll do that! I've been looking forward to\n |
| 0xb94eb | 11 | using them. |
| 0xb94f7 | 48 | All right. Thanks for showing me the way here,\n |
| 0xb9528 | 5 | love. |
| 0xb952e | 9 | S-Sure... |
| 0xb9538 | 42 | Atuy heads into the inn proper, giving a\n |
| 0xb9563 | 31 | parting wave over her shoulder. |
| 0xb9583 | 40 | Whew. I'm... oddly tired after all that. |
| 0xb95ac | 17 | What an odd girl. |
| 0xb95be | 11 | No kidding. |
| 0xb95ca | 36 | ...Not that you should be talking.\n |
| 0xb95ef | 26 | You're not far behind her. |
| 0xb960a | 47 | From a distance, I watch the girl slip inside\n |
| 0xb963a | 37 | the inn, leaving me with my thoughts. |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_04.json` com a forma:
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
