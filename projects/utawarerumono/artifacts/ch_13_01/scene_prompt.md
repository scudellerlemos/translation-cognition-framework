# Cena ch_13_01 — pacote de traducao (514 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Ozen | Personagem | Ozen | manter_original | none |
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
### Ozen — criticality: low
- Ozen — `voice_criticality: low`. General-Pilar, pai da Rulutieh; registro grave/nobre.
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Girl` -> `Garota` (sistema, root)
- `Oh...` -> `Ah...` (Kuon, root)
- `*THUD*` -> `*BAQUE*` (Kuon, root)
- `Gah!` -> `Ai!` (Man, root)
- `but...` -> `mas...` (Kuon, 12_16)
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Hello?` -> `Olá?` (Garota, 12_01)
- `N-No...` -> `N-Não..` (Protagonista, 12_01)
- `I think.` -> `acho.` (Kuon, 12_11)
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
| 0x56af3 | 14 | Nngh... Gah... |
| 0x56b02 | 50 | The room is already painfully bright by the time\n |
| 0x56b35 | 49 | I dare to open my eyes. I can hear voices, but... |
| 0x56b67 | 22 | I'm alone in the room. |
| 0x56b7e | 42 | Urgh, my head... Hi, hangover. How're you. |
| 0x56ba9 | 39 | Definitely drank too much last night... |
| 0x56bd1 | 5 | Ah... |
| 0x56bd7 | 53 | I manage to pour myself a jug of water and down the\n |
| 0x56c0d | 40 | whole thing in one go, clearing my head. |
| 0x56c36 | 43 | Just how late was I up partying last night? |
| 0x56c62 | 53 | They made me drink with them after I came back with\n |
| 0x56c98 | 43 | Ukon, and... Everything after that is hazy. |
| 0x56cc4 | 49 | Seems like I managed to make it to bed, at least. |
| 0x56cf6 | 51 | Halfway into my second jug of water, Kuon enters,\n |
| 0x56d2a | 22 | already fully dressed. |
| 0x56d41 | 47 | Morning, sleepyhead. Back in the world of the\n |
| 0x56d71 | 11 | living now? |
| 0x56d7d | 21 | Yeah, I just woke up. |
| 0x56d93 | 52 | You don't look like you're doing too well. I guess\n |
| 0x56dc8 | 49 | I shouldn't be surprised, considering last night. |
| 0x56dfa | 41 | Nnhh. Yeah. I've got a bit of a hangover. |
| 0x56e24 | 54 | Hmm. I thought that might be the case, so I prepared\n |
| 0x56e5b | 33 | a little something to help. Here. |
| 0x56e7d | 37 | Kuon holds out a bowl in her hands... |
| 0x56ea3 | 53 | ...filled to the brim with something dark green and\n |
| 0x56ed9 | 8 | viscous. |
| 0x56ee2 | 54 | It's medicine that'll help sober you up. Be careful,\n |
| 0x56f19 | 42 | though--it's got a bit of a strong flavor. |
| 0x56f44 | 14 | Ah, thank you. |
| 0x56f53 | 8 | PFFFEH!? |
| 0x56f5c | 33 | Aah! What'd you spit it out for!? |
| 0x56f7e | 23 | Guh... g-gah... ghhh... |
| 0x56f96 | 51 | Wh-What is... it's... What is this flavor? I-It's\n |
| 0x56fca | 53 | somehow bitter, hot, sweet, and s-sour all at once... |
| 0x57000 | 50 | The best medicine always has a bitter taste! You\n |
| 0x57033 | 49 | may not like it, but I can guarantee its effects. |
| 0x57065 | 37 | Why, you--Is this--? *Cough, cough--* |
| 0x5708b | 48 | *Cough, cough--* I-Is this just punishment for\n |
| 0x570bc | 21 | sleeping in too late? |
| 0x570d2 | 48 | Hmph! Nothing of the sort. This medicine is my\n |
| 0x57103 | 45 | SPECIALTY. It even earned my father's praise. |
| 0x57131 | 51 | Either he was biased because you're his child, or\n |
| 0x57165 | 44 | he couldn't bring himself to tell the truth. |
| 0x57192 | 53 | You get used to the flavor. It's almost addicting--\n |
| 0x571c8 | 49 | a mature, nuanced profile, for refined palates... |
| 0x571fa | 46 | Kuon puts her lips to the bowl in her hands... |
| 0x57229 | 51 | Mm. Delicious. The bitterness lends it a depth of\n |
| 0x5725d | 39 | complexity that's almost indescribable. |
| 0x57285 | 50 | Seeing her drinking the vile stuff down readily,\n |
| 0x572b8 | 13 | I nearly gag. |
| 0x572c6 | 6 | Hurk-- |
| 0x572cd | 39 | Guh. The inside of my mouth is still... |
| 0x572f5 | 52 | There's no doubt my hangover is receding, but that\n |
| 0x5732a | 42 | foul taste is still lingering in my mouth. |
| 0x57355 | 52 | If she was feeding this stuff to her father on the\n |
| 0x5738a | 49 | regular, she was definitely trying to murder him. |
| 0x573bc | 6 | ...Hm? |
| 0x573c3 | 46 | A rising noise in the distance interrupts my\n |
| 0x573f2 | 49 | thoughts. Some kind of commotion outside the inn? |
| 0x57424 | 54 | Poking my head out to find the source of the hubbub,\n |
| 0x5745b | 46 | I spy large carts parked in the central plaza. |
| 0x5748a | 52 | A number of new faces chat with the villagers--the\n |
| 0x574bf | 43 | people who came with the caravan, no doubt. |
| 0x574eb | 22 | Heya, kid. Sleep well? |
| 0x57502 | 47 | Well enough that I don't remember a damn thing. |
| 0x57532 | 48 | Bahahaha! I don't doubt it. Even our missy was\n |
| 0x57563 | 29 | having trouble waking you up. |
| 0x57581 | 53 | It was somethin' to see, her nursing you diligently\n |
| 0x575b7 | 30 | while you were dead-ass drunk. |
| 0x575d6 | 23 | Nngh... Don't say that. |
| 0x575ee | 52 | Ahahaha! It's fine, c'mon. I think some of the men\n |
| 0x57623 | 51 | wanted you dead from envy, seeing her taking care\n |
| 0x57657 | 7 | of you. |
| 0x5765f | 25 | That's not "fine" at all. |
| 0x57679 | 34 | Forget it. So what's in the carts? |
| 0x5769c | 53 | Examining one of the caravan's wagons more closely,\n |
| 0x576d2 | 51 | it looks larger than the ones around the village... |
| 0x57706 | 47 | Escorting this cargo to the capital is why we\n |
| 0x57736 | 46 | originally came out here. We got hired for it. |
| 0x57765 | 37 | Then you'll be on your way soon, huh? |
| 0x5778b | 52 | Yeah, we're in the middle of the handover. Soon as\n |
| 0x577c0 | 40 | everything's squared away, we'll be off. |
| 0x577e9 | 8 | I see... |
| 0x577f2 | 50 | Which means this is goodbye for now. Since we're\n |
| 0x57825 | 50 | all bound for the city, we'll no doubt meet again. |
| 0x57858 | 52 | I know I already asked, but are you sure you won't\n |
| 0x5788d | 48 | come with us? It really wouldn't be any trouble. |
| 0x578be | 54 | Ah, well--I wouldn't mind it, but Kuon's the one who\n |
| 0x578f5 | 29 | makes those decisions for us. |
| 0x57913 | 51 | Whatever you say. How 'bout it, missy? Considered\n |
| 0x57947 | 21 | my offer any further? |
| 0x5795d | 3 | Hm? |
| 0x57965 | 47 | Glancing over my shoulder, I notice Kuon, who\n |
| 0x57995 | 45 | hadn't been standing there just a moment ago. |
| 0x579c3 | 52 | Conspicuously silent, her eyes seem focused on the\n |
| 0x579f8 | 35 | caravan, quietly scrutinizing it... |
| 0x57a1c | 5 | Kuon? |
| 0x57a22 | 19 | Huh? Ah, what's up? |
| 0x57a36 | 50 | That's what I was gonna ask you. The offer to go\n |
| 0x57a69 | 39 | with them--are you sure about refusing? |
| 0x57a91 | 17 | Ah, about that... |
| 0x57aa3 | 47 | Kuon mumbles, seeming to nod and think for an\n |
| 0x57ad3 | 16 | extended moment. |
| 0x57ae4 | 51 | Considering her quick refusal last night, I doubt\n |
| 0x57b18 | 42 | she'll have changed her mind so quickly... |
| 0x57b43 | 45 | I believe... we'll take you up on your offer. |
| 0x57b71 | 4 | Huh? |
| 0x57b76 | 53 | I thought it over. Considering the danger yesterday\n |
| 0x57bac | 49 | presented, it'd be best if we all stuck together. |
| 0x57bde | 50 | Aha! Well then. Welcome aboard, you two. I doubt\n |
| 0x57c11 | 47 | there'll ever be a dull moment with you around. |
| 0x57c41 | 50 | If you're comin' along, then you oughta pack up.\n |
| 0x57c74 | 50 | We're out of here as soon as our business is done. |
| 0x57ca7 | 32 | OK. We'll see you shortly, then. |
| 0x57cc8 | 31 | Why the sudden change of heart? |
| 0x57ce8 | 24 | Whatever could you mean? |
| 0x57d01 | 48 | Feigning ignorance, Kuon spares another glance\n |
| 0x57d32 | 43 | toward the loaded caravan, smiling faintly. |
| 0x57d5e | 48 | Curiosity gets the better of me, and I turn to\n |
| 0x57d8f | 18 | follow her gaze... |
| 0x57da2 | 7 | *FOOMP* |
| 0x57daa | 4 | Wh-- |
| 0x57daf | 48 | And the moment I stop looking where I'm going,\n |
| 0x57de0 | 41 | I bump into a... really big, fluffy wall? |
| 0x57e0a | 14 | Oh, pardon me. |
| 0x57e19 | 41 | Then I hear a female voice from above me. |
| 0x57e43 | 5 | Bird? |
| 0x57e56 | 8 | Holy--!? |
| 0x57e5f | 51 | When I look back in front of me, an enormous bird\n |
| 0x57e93 | 48 | creature blocks my path, ridden by a young girl. |
| 0x57ec4 | 4 | Girl |
| 0x57ec9 | 25 | I'm... sorry about, um... |
| 0x57ee3 | 46 | It's, uh, OK. I'm the one who bumped into you. |
| 0x57f12 | 47 | That thing is HUGE. And that girl is RIDING it. |
| 0x57f42 | 51 | That's a relief... Come on, Cocopo. We'll just be\n |
| 0x57f76 | 36 | in everybody's way, standing here... |
| 0x57fa2 | 51 | "Cocopo"--probably the bird's name?--disobeys its\n |
| 0x57fd6 | 49 | master, edging closer to put its face up to mine. |
| 0x58008 | 26 | What's with this thing...? |
| 0x58023 | 8 | ♪...\n |
| 0x58034 | 17 | *Sshff, sshff*... |
| 0x58046 | 49 | And then it starts to rub its gigantic, fluffy-\n |
| 0x58078 | 31 | feathered body against my face. |
| 0x58098 | 8 | Gh--Wh-- |
| 0x580a1 | 34 | W-What's with it, all of a sudden? |
| 0x580c4 | 10 | Cocopo...? |
| 0x580cf | 36 | Is it... trying to snuggle up to me? |
| 0x580f4 | 46 | I've... never seen Cocopo become attached to\n |
| 0x58123 | 20 | someone like this... |
| 0x58138 | 50 | It'd be fine if it were, y'know, a SMALL animal.\n |
| 0x5816b | 47 | Not something that could accidentally crush me. |
| 0x5819b | 52 | This is just a pain in the neck. It's so big, it's\n |
| 0x581d0 | 45 | more gently shoving me around than snuggling. |
| 0x581fe | 51 | A woman's pet becomes attached to a man, and they\n |
| 0x58232 | 50 | grow closer for it... This is nothing like those\n |
| 0x58265 | 8 | stories. |
| 0x5826e | 19 | *Sshhff, sshhff*... |
| 0x58282 | 51 | And this thing is coming on to me WAY too strong.\n |
| 0x582b6 | 22 | Too close for comfort. |
| 0x582cd | 36 | W-Well, I'll just... be going, then. |
| 0x582f2 | 5 | Oh... |
| 0x582f8 | 50 | I'm starting to get a little creeped out by this\n |
| 0x5832b | 48 | thing, so I'll try to beat a hasty retreat and-- |
| 0x5835c | 17 | *Tmp-tmp-tmp-tmp* |
| 0x5836e | 21 | ...It's following me. |
| 0x58384 | 16 | *Tmp-tmp-tmp--!* |
| 0x58395 | 17 | *TUP-TUP-TUP-TUP* |
| 0x583a7 | 24 | Why is it FOLLOWING ME!? |
| 0x583c0 | 53 | Even as I quicken my pace, I can hear its footsteps\n |
| 0x583f6 | 16 | right behind me. |
| 0x58407 | 21 | *Tmp-tmp-tmp-tmp--!!* |
| 0x5841d | 19 | *TUPTUPTUPTUPTUP--* |
| 0x58431 | 23 | *TMP-TMP-TMP-TMP-TMP--* |
| 0x58449 | 29 | *TUKKATUKKATUKKATUKKATUKKA--* |
| 0x58467 | 13 | Hhnnnnggh--!! |
| 0x58475 | 25 | *TAKKA-TAKKA-TAKKA-TAK--* |
| 0x5848f | 44 | If I run as fast as I can, I doubt it'll--\n |
| 0x584bc | 5 | Gah!? |
| 0x584da | 27 | God DAMN it, it's too fast! |
| 0x584f6 | 31 | C-Cocopo, no. Stop... please... |
| 0x58516 | 54 | Try to stop it with a more assertive voice than that\n |
| 0x5854d | 30 | little mouse whisper, damn it! |
| 0x58581 | 17 | Wait, AAAAACK--!! |
| 0x58593 | 6 | *THUD* |
| 0x5859a | 4 | Gah! |
| 0x5859f | 52 | Even running as hard as I can, I can't outpace it.\n |
| 0x585d4 | 47 | It tackles me with enthusiasm, and I go flying. |
| 0x5860a | 7 | *WHUMF* |
| 0x58612 | 22 | G-Gurgh--It's heavy--! |
| 0x58629 | 50 | Then it sits its entire bulk happily on top of me. |
| 0x5865c | 22 | Nngh--I can't--move--! |
| 0x58673 | 28 | A-Are you all right, sir...? |
| 0x58690 | 48 | The young girl looks at me with worry from her\n |
| 0x586c1 | 20 | place in the saddle. |
| 0x586d6 | 41 | I'm sorry, I'm sorry... I'm v-very sorry! |
| 0x58700 | 48 | She dismounts and begins to apologize profusely. |
| 0x58731 | 39 | Y-You don't need to say sorry, just--\n |
| 0x58759 | 24 | Please get it off of me. |
| 0x58772 | 19 | Y-Yes, of course... |
| 0x5878d | 48 | Come on, Cocopo, stand up... You mustn't cause\n |
| 0x587be | 10 | trouble... |
| 0x587cf | 34 | Here, just step a little to the... |
| 0x587fd | 19 | *STOMP STOMP STOMP* |
| 0x58811 | 49 | N-No, I said step, not two-step! Come on, move,\n |
| 0x58843 | 10 | please...? |
| 0x5884e | 15 | *TUG-TUG-TUG--* |
| 0x5885e | 49 | She tries everything she can to get the bird to\n |
| 0x58890 | 49 | move, pushing, pulling, shoving--all to no avail. |
| 0x588c2 | 29 | I-I'm sorry... It's no use... |
| 0x588e0 | 52 | You're giving up too quickly! Try a little harder,\n |
| 0x58915 | 10 | please...! |
| 0x58920 | 35 | O-OK... Here we go...! T-Take this! |
| 0x58944 | 12 | *TUUUUUUG--* |
| 0x58951 | 41 | Is she really putting her all into it...? |
| 0x5897b | 52 | Guess it can't be helped. Just grab my hand, would\n |
| 0x589b0 | 4 | you? |
| 0x589b5 | 6 | H-Huh? |
| 0x589bc | 48 | For some reason, she goes red at that request,\n |
| 0x589ed | 19 | becoming flustered. |
| 0x58a01 | 6 | But... |
| 0x58a08 | 49 | Please. It's not gonna budge, that much is clear. |
| 0x58a3a | 7 | O-OK... |
| 0x58a42 | 47 | Red in the face, she uncertainly takes my hand. |
| 0x58a72 | 36 | Be sure to pull with all your might. |
| 0x58a97 | 45 | Y-Yes, of course... Here I go...!! Take this! |
| 0x58ac5 | 14 | *STREEEETCH--* |
| 0x58ad4 | 7 | GYAAAH! |
| 0x58adc | 10 | Nnnngh--!! |
| 0x58ae7 | 11 | *RRRRRIP--* |
| 0x58af3 | 37 | Ow ow OW OW THINGS ARE MAKING NOISE\n |
| 0x58b19 | 31 | THAT SHOULDN'T BE MAKING NOISE. |
| 0x58b39 | 13 | Hnnnnnnnngh!! |
| 0x58b47 | 41 | Wait, wait, stop, STOP, MY HAND'S GONNA\n |
| 0x58b71 | 10 | TEAR OFF-- |
| 0x58b7c | 6 | ...Eh? |
| 0x58b83 | 51 | O-Oh... I'm sorry... Y-You said to do it with all\n |
| 0x58bb7 | 15 | my might, so... |
| 0x58bc7 | 51 | Gah. That's some strength on her. So she's not so\n |
| 0x58bfb | 18 | weak after all...? |
| 0x58c0e | 37 | Hm? What're you doing over here, kid? |
| 0x58c34 | 27 | Can't you tell by looking!? |
| 0x58c50 | 53 | Well, it LOOKS like you're being crushed by a giant\n |
| 0x58c86 | 5 | bird. |
| 0x58c8c | 49 | I'm glad we got THAT cleared up! A little help,\n |
| 0x58cbe | 8 | please!? |
| 0x58cc7 | 49 | How 'bout we put it aside for the moment, yeah?\n |
| 0x58cf9 | 20 | Introductions first. |
| 0x58d0e | 50 | This is Princess Rulutieh. She's the daughter of\n |
| 0x58d41 | 49 | Lord Ozen, owlo of Kujyuri and one of the Eight\n |
| 0x58d73 | 8 | Pillars. |
| 0x58d7c | 53 | Don't "put it aside"! I kinda need a little help, h-- |
| 0x58db2 | 27 | Wait, what did he just say? |
| 0x58dce | 47 | As I glance back at the young bird rider, she\n |
| 0x58dfe | 24 | hurriedly bows her head. |
| 0x58e17 | 14 | A prin...cess? |
| 0x58e26 | 52 | Lady Rulutieh, this is Haku. He'll be comin' along\n |
| 0x58e5b | 41 | with us to the capital as our consultant. |
| 0x58e85 | 50 | Y-Yes... My name is Rulutieh. It's a pleasure to\n |
| 0x58eb8 | 23 | make your acquaintance. |
| 0x58ed0 | 7 | Y-Yeah. |
| 0x58ed8 | 13 | ...Hey, Ukon? |
| 0x58ee6 | 16 | Yeah? What's up? |
| 0x58ef7 | 23 | Did you say "princess"? |
| 0x58f0f | 14 | Yep. Sure did. |
| 0x58f1e | 45 | What's a princess doing in a place like this? |
| 0x58f4c | 51 | What do you mean, "a place like this"? Kujyuri is\n |
| 0x58f80 | 24 | Lady Rulutieh's country. |
| 0x58f99 | 50 | No, I don't mean it like that. I mean why is she\n |
| 0x58fcc | 36 | way out here in a backwater village? |
| 0x58ff1 | 43 | That's 'cause she's on her way to present\n |
| 0x5901d | 24 | offerings to the Mikado. |
| 0x59036 | 3 | Eh? |
| 0x5903a | 24 | Offerings to the Mikado? |
| 0x59053 | 49 | That's our cargo. It's proper for a princess to\n |
| 0x59085 | 46 | escort her country's offerings to the capital. |
| 0x590b4 | 23 | ...Yeah, but. "Mikado"? |
| 0x590cc | 34 | Eh? Oh, right. Your memories, huh. |
| 0x590ef | 46 | The Mikado's a great man who rules over most\n |
| 0x5911e | 28 | countries on this continent. |
| 0x5913b | 48 | The guy commands immense respect, deep wisdom,\n |
| 0x5916c | 21 | unparalleled power... |
| 0x59182 | 50 | The owlos of each country under his control only\n |
| 0x591b5 | 51 | rule because the Mikado allows them their autonomy. |
| 0x591e9 | 54 | So when a country sends tribute, someone of properly\n |
| 0x59220 | 48 | high station's gotta present it themselves, see? |
| 0x59251 | 39 | Which means this girl's coming with us. |
| 0x59279 | 36 | That's what I'm trying to say, yeah. |
| 0x5929e | 32 | The cargo's that valuable, then? |
| 0x592bf | 54 | Sure. Preserved meats, textiles, furs, incense, ore.\n |
| 0x592f6 | 28 | A whole bunch of good stuff. |
| 0x59313 | 45 | I see... But isn't that, uh, sort of a huge\n |
| 0x59341 | 15 | responsibility? |
| 0x59351 | 51 | I didn't sign up to see my head roll if something\n |
| 0x59385 | 25 | goes wrong with all this. |
| 0x5939f | 54 | Eh? I told you before, we'll be fine. Nobody's gonna\n |
| 0x593d6 | 44 | be stupid enough to try it with our numbers. |
| 0x59403 | 32 | No, I don't mean it like that... |
| 0x59424 | 54 | Don't worry so much! You and Missy just sit back and\n |
| 0x5945b | 31 | enjoy the trip, huh? Gwahahaha! |
| 0x5947b | 39 | Man, I just can't shake this feeling... |
| 0x594a3 | 53 | I look over to Rulutieh again, and she shrinks back\n |
| 0x594d9 | 6 | a bit. |
| 0x594e0 | 47 | She doesn't seem... frightened, exactly? More\n |
| 0x59510 | 50 | uncomfortable. She's probably just the timid type. |
| 0x59543 | 5 | Um... |
| 0x59549 | 31 | I'm, ah... s-sorry about, um... |
| 0x59569 | 51 | ...Oh, right. The princess's stupid bird is still\n |
| 0x5959d | 14 | sitting on me. |
| 0x595ac | 51 | Hey, hey, it's all right. Not like it's your fault. |
| 0x595e0 | 25 | But Cocopo is mine, so... |
| 0x595fa | 49 | Really. It's OK. You didn't exactly order it to\n |
| 0x5962c | 8 | do this. |
| 0x59635 | 23 | But a princess, huh...? |
| 0x59652 | 50 | She certainly seems like one. Now that I look at\n |
| 0x59685 | 52 | her, she's dressed much more finely than the others. |
| 0x596ba | 25 | Quite a nice girl, too... |
| 0x596d4 | 52 | And she definitely has that princess-like cuteness\n |
| 0x59709 | 10 | about her. |
| 0x59714 | 44 | Hey, are you hitting on her all of a sudden? |
| 0x59741 | 17 | What do you mean? |
| 0x59753 | 18 | ...Eh. Never mind. |
| 0x59766 | 17 | Um... uh... ah... |
| 0x59778 | 50 | ...And now the princess is fidgeting restlessly.\n |
| 0x597ab | 40 | Does she need the bathroom or something? |
| 0x597d4 | 35 | A-Ah, Sir Ukon... please take this. |
| 0x597f8 | 49 | Rulutieh abruptly thrusts a scroll toward Ukon,\n |
| 0x5982a | 44 | as if trying to change the subject forcibly. |
| 0x59857 | 44 | M-My father asked me to... give this to you. |
| 0x59884 | 13 | Oh, that's... |
| 0x59892 | 50 | Ukon accepts the scroll and unties it, beginning\n |
| 0x598c5 | 8 | to read. |
| 0x598ce | 52 | Hey, never mind that! Can I get a little help, here? |
| 0x59903 | 50 | Trying to get the princess' attention only seems\n |
| 0x59936 | 34 | to make her withdraw further. Why? |
| 0x59959 | 49 | And she's still fidgeting. Really, if she needs\n |
| 0x5998b | 45 | the bathroom, she should just excuse herself. |
| 0x599b9 | 16 | ...Hm. Princess. |
| 0x599ca | 6 | YEEK!? |
| 0x599d1 | 50 | ...Somethin' wrong? What was that noise you made\n |
| 0x59a04 | 9 | just now? |
| 0x59a0e | 23 | N-No... I-It's nothing. |
| 0x59a26 | 51 | If you say so. Did Lord Ozen say anything besides\n |
| 0x59a5a | 22 | what's in this letter? |
| 0x59a71 | 53 | He, ah... told me to follow any orders you gave me,\n |
| 0x59aa7 | 9 | Sir Ukon. |
| 0x59ab1 | 50 | I see. All right, then, princess! You just leave\n |
| 0x59ae4 | 17 | everything to us. |
| 0x59af6 | 42 | Rulutieh puts her hands to her chest and\n |
| 0x59b21 | 26 | breathes a sigh of relief. |
| 0x59b3c | 52 | Good. I'll go and get the men prepped for departure. |
| 0x59b71 | 23 | Very well... Thank you. |
| 0x59b89 | 47 | H-Hey, now. You aren't gonna help me out, here? |
| 0x59bb9 | 37 | Ukon leans down to whisper in my ear. |
| 0x59bdf | 46 | See, the thing is, the bird's got a bit of a\n |
| 0x59c0e | 19 | mischievous streak. |
| 0x59c22 | 54 | Seems it'll mess with anything it finds interesting,\n |
| 0x59c59 | 49 | and it's been a pain in the ass all the way here. |
| 0x59c8b | 30 | ...What are you trying to say? |
| 0x59caa | 53 | It finds YOU interesting. So play with it for a few\n |
| 0x59ce0 | 50 | hours and keep it out of everyone's way, will you? |
| 0x59d13 | 52 | Sorry. I'll owe you a drink when we hit the capital. |
| 0x59d48 | 10 | Hey, wait! |
| 0x59d53 | 45 | Thanks for volunteering! I'm counting on you. |
| 0x59d81 | 37 | Will you just w-- Damn it, he's gone. |
| 0x59da7 | 52 | *Sigh*... Don't worry about it, OK? I'm gonna keep\n |
| 0x59ddc | 39 | saying that until you stop apologizing. |
| 0x59e04 | 51 | I know the bird's not doing this because you want\n |
| 0x59e38 | 6 | it to. |
| 0x59e3f | 7 | ...Huh? |
| 0x59e47 | 9 | *Poke*... |
| 0x59e51 | 15 | *Poke, poke*... |
| 0x59e61 | 40 | Suddenly, something pokes into my cheek. |
| 0x59e8a | 21 | *Poke, poke, poke*... |
| 0x59ea0 | 51 | Above me stands an unfamiliar person wrapped from\n |
| 0x59ed4 | 43 | head to toe in thick cloth, poking my face. |
| 0x59f00 | 15 | ...And you are? |
| 0x59f10 | 52 | I can't even tell if they're male or female. Their\n |
| 0x59f45 | 43 | wrap-like robes totally obscure everything. |
| 0x59f71 | 45 | The stranger remains silent at my question,\n |
| 0x59f9f | 40 | continuing to prod my cheek inscrutably. |
| 0x59fc8 | 6 | Hello? |
| 0x59fcf | 9 | YEEEEEK!? |
| 0x59fd9 | 52 | O-Oh, um. I wasn't talking to you, but--is this an\n |
| 0x5a00e | 22 | acquaintance of yours? |
| 0x5a025 | 7 | N-No... |
| 0x5a02d | 19 | *Poke-poke-poke*... |
| 0x5a041 | 24 | What's up with this guy? |
| 0x5a05a | 8 | *Poke--* |
| 0x5a063 | 13 | *--squish*... |
| 0x5a071 | 52 | And then I feel a pressure against my other cheek.\n |
| 0x5a0a6 | 12 | More poking? |
| 0x5a0b3 | 54 | But this person isn't the one doing it. Someone else\n |
| 0x5a0ea | 38 | is prodding me from the opposite side. |
| 0x5a111 | 9 | Who the-- |
| 0x5a11b | 19 | *Squish, squish*... |
| 0x5a12f | 20 | *Poke-poke-poke--*\n |
| 0x5a144 | 24 | *Squish-squish-squish--* |
| 0x5a15d | 49 | On my other side, another figure dressed in the\n |
| 0x5a18f | 39 | same mysterious clothing pokes at me... |
| 0x5a1b7 | 52 | I am being poked in the cheeks by two identically-\n |
| 0x5a1ec | 52 | dressed people who don't care to explain themselves. |
| 0x5a221 | 26 | What the HELL is going on? |
| 0x5a23c | 54 | I have officially stopped understanding any of this.\n |
| 0x5a273 | 28 | Why is this happening to me? |
| 0x5a290 | 47 | Sorry to keep you waiting. We got into a long\n |
| 0x5a2c0 | 46 | conversation, and...{W210} What are you doing? |
| 0x5a2ef | 26 | By all means, you tell me. |
| 0x5a30a | 19 | Who were those two? |
| 0x5a31e | 46 | That's what I want to kn--Eh? ...And they're\n |
| 0x5a34d | 47 | gone. The robed cheek-pokers have straight-up\n |
| 0x5a37d | 9 | vanished. |
| 0x5a387 | 51 | Glancing around as best I'm able, I can't catch a\n |
| 0x5a3bb | 27 | glimpse of them anywhere... |
| 0x5a3d7 | 43 | I only looked away for a moment, and they\n |
| 0x5a403 | 36 | disappeared right out from under me. |
| 0x5a428 | 29 | What the hell was that about? |
| 0x5a446 | 33 | Hmm. You've made a friend, I see. |
| 0x5a477 | 18 | *Lick-lick-lick--* |
| 0x5a48a | 51 | No! No, don't lick my face, that beak is HUGE AND\n |
| 0x5a4be | 41 | YOU'RE GONNA CRUSH MY HEAD PLEASE DON'T-- |
| 0x5a4e8 | 52 | I-I'm sorry! I'm sorry--Cocopo, please, stand up...! |
| 0x5a52e | 50 | Rulutieh struggles to push Cocopo off of me, but\n |
| 0x5a561 | 45 | once again, she can't bring it to even budge. |
| 0x5a58f | 10 | Cocopo...! |
| 0x5a59a | 9 | ...May I? |
| 0x5a5a4 | 64 | Perhaps it's only because she can't bear to watch anymore, but\n |
| 0x5a5e5 | 32 | Kuon walks up beside Rulutieh... |
| 0x5a606 | 49 | You're a hopeless little thing, aren't you? You\n |
| 0x5a638 | 31 | mustn't be naughty, you know... |
| 0x5a658 | 49 | Kuon murmurs to the bird and gently strokes its\n |
| 0x5a68a | 35 | neck... And it nonchalantly stands. |
| 0x5a6ae | 50 | Aaahhh. That was... an experience. I can breathe\n |
| 0x5a6e1 | 23 | again. Thank you, Kuon. |
| 0x5a6f9 | 26 | Hmhm. You're very welcome. |
| 0x5a714 | 45 | Cocopo... When I asked, you didn't... Why...? |
| 0x5a742 | 38 | It's because you're so close, I think. |
| 0x5a769 | 47 | Cocopo thinks of you more as a friend than an\n |
| 0x5a799 | 8 | owner... |
| 0x5a7a2 | 55 | ...so your "commanding" was interpreted as "playing,"\n |
| 0x5a7da | 8 | I think. |
| 0x5a7e3 | 24 | ...Is that true, Cocopo? |
| 0x5a7fc | 48 | I'm Kuon, by the way. Pleased to meet you. You\n |
| 0x5a82d | 7 | are...? |
| 0x5a835 | 36 | Would you mind telling me your name? |
| 0x5a85a | 46 | Oh... Y-Yes, of course. It's Rulu... Rulutieh. |
| 0x5a889 | 50 | Miss Rulutieh, huh? It's a pleasure to make your\n |
| 0x5a8bc | 13 | acquaintance. |
| 0x5a8ca | 20 | Y-Yes, a pleasure... |
| 0x5a8df | 52 | Eh heh heh. She's cute. She's almost like a little\n |
| 0x5a914 | 9 | princess. |
| 0x5a91e | 52 | Kuon whispers into my ear, most likely so Rulutieh\n |
| 0x5a953 | 47 | can't hear, so I whisper my reply back in turn. |
| 0x5a983 | 52 | Not "almost." She actually is the princess of this\n |
| 0x5a9b8 | 20 | country, apparently. |
| 0x5a9cd | 44 | Oh, so she's really a princess? Go figure... |
| 0x5a9fa | 43 | Yeah. And you're right; she IS pretty cute. |
| 0x5aa26 | 47 | Oh, that's right. She's coming with us to the\n |
| 0x5aa56 | 49 | capital--or, well, WE'RE going with HER, I guess. |
| 0x5aa88 | 23 | Hmm hmm. Is that so...? |
| 0x5aaa0 | 49 | Hm. Well, Miss Rulutieh... Would you like to be\n |
| 0x5aad2 | 8 | friends? |
| 0x5aadb | 33 | Ah--If you don't want to, it's... |
| 0x5aafd | 17 | U-Uhm... No, I... |
| 0x5ab0f | 50 | Hey, is that OK, Kuon? Asking a princess that so\n |
| 0x5ab42 | 9 | casually? |
| 0x5ab4c | 54 | ...I think it'll be fine. I'm not from this country,\n |
| 0x5ab83 | 45 | so it's not like she's my liege or something. |
| 0x5abb1 | 49 | That's not what I meant. Like, wouldn't she mind? |
| 0x5abe3 | 53 | You say that, but you don't seem exactly flustered,\n |
| 0x5ac19 | 9 | yourself. |
| 0x5ac23 | 51 | What are you talking about? I've been showing her\n |
| 0x5ac57 | 20 | nothing but respect. |
| 0x5ac6c | 53 | I mean--Yeah, it's probably because of my memories,\n |
| 0x5aca2 | 49 | but social status stuff hasn't really... sunk in? |
| 0x5acd4 | 45 | So, you wouldn't rather be friends, princess? |
| 0x5ad02 | 50 | Rulutieh shakes her head rapidly, clearly anxious. |
| 0x5ad35 | 37 | I-I don't know... what to, um, do...? |
| 0x5ad5b | 48 | Nobody's ever... asked me that. I don't really\n |
| 0x5ad8c | 18 | have... friends... |
| 0x5ad9f | 53 | Ah, I get it. Because she's a princess, she doesn't\n |
| 0x5add5 | 41 | really have a group of peers to befriend. |
| 0x5adff | 51 | I suppose it'll be the first time for both of us,\n |
| 0x5ae33 | 5 | then. |
| 0x5ae39 | 49 | I don't really have anyone I can call a friend,\n |
| 0x5ae6b | 40 | either. So it'll be a first for us both! |
| 0x5ae94 | 39 | This IS Kuon we're talking about, so... |
| 0x5aebc | 50 | Forever alone because you're always on the road,\n |
| 0x5aeef | 37 | huh? Can't be tied down for too long? |
| 0x5af15 | 50 | I won't say I'm not surprised, but I guess I can\n |
| 0x5af48 | 24 | understaAARGH OW OW OW-- |
| 0x5af61 | 19 | *Crrraaaaackkk--!!* |
| 0x5af75 | 51 | Ow, ow, that HURTS--Why are you squeezing so damn\n |
| 0x5afa9 | 6 | HARD!? |
| 0x5afb0 | 37 | So. Will you be my very first friend? |
| 0x5afd6 | 48 | Saying that, Kuon offers her hand to Rulutieh,\n |
| 0x5b007 | 17 | smiling gently... |
| 0x5b019 | 52 | ...as her tail's deathgrip around my head tightens\n |
| 0x5b04e | 12 | dangerously. |
| 0x5b05b | 46 | Gah, my skull's gonna crack, it's gonna crack! |
| 0x5b08a | 26 | O-Of course I will, but... |
| 0x5b0a5 | 53 | I don't know... what friends are supposed to really\n |
| 0x5b0db | 22 | do with each other...? |
| 0x5b0f2 | 46 | Talking, playing... Anything is fine, I think. |
| 0x5b121 | 30 | I hope we can be good friends. |
| 0x5b140 | 43 | Kuon keeps her hand held out as she speaks. |
| 0x5b16c | 7 | ...Yes. |
| 0x5b174 | 51 | I... I would very much like to be friends with you. |
| 0x5b1a8 | 52 | Rulutieh bashfully reaches out and squeezes Kuon's\n |
| 0x5b1dd | 5 | hand. |
| 0x5b1e3 | 50 | It's a heartwarming sight. It WOULD be touching,\n |
| 0x5b216 | 7 | even... |
| 0x5b21e | 52 | ...if I weren't being crushed by a vice on the side. |
| 0x5b253 | 52 | I'm sure it's an emotional moment, but this REALLY\n |
| 0x5b288 | 6 | HURTS. |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_01.json` com a forma:
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
