# Cena ch_13_08 — pacote de traducao (114 linhas)

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
| Kujyuri | Local | Kujyuri | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| woptor | Criatura | woptor | manter_original | none |
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
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Rulutieh.` -> `Rulutieh.` (Haku, 13_02)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `yourself.` -> `abalado.` (Kuon, 13_01)
- `bandits.` -> `bandidos.` (Haku, 13_06)
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
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
- Ougi: `Truly most impressive, dearest sister. Your\n` -> `Muito impressionante, querida irmã. Seu charme\n`
- Ougi: `feminine charms dazzle, as ever.` -> `feminino encanta, como sempre.`
- Ougi: `How positively boorish. A good MAN simply\n` -> `Que grosseria. Um bom HOMEM simplesmente\n`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x7778e | 12 | Hips_toriuma |
| 0x7779b | 11 | Gwaaaaghh!! |
| 0x777a7 | 46 | Gah! GEH! I'm sorry! I'm sorry, make it st--!! |
| 0x777d6 | 30 | Erm... P-Princess... Rulutieh? |
| 0x777f5 | 50 | Just a suggestion, but maybe he's, um, had enough? |
| 0x77828 | 50 | Huh? N-No, you don't understand-- I'm not making\n |
| 0x7785b | 17 | Cocopo do this... |
| 0x7786d | 42 | Cocopo, you can stop now. It's all over... |
| 0x778ae | 16 | GYEH!! GAAAH--!! |
| 0x778bf | 50 | The usual response to her asking nicely, then...\n |
| 0x778f2 | 42 | This is just cruel and unusual punishment. |
| 0x7791d | 38 | M-My life! Just spare my life, please! |
| 0x77944 | 50 | This guy might be a scumbag, but I'm starting to\n |
| 0x77977 | 43 | feel sorry for him--not that I forgive him. |
| 0x779a3 | 46 | Do whatever you like with him, I guess--have\n |
| 0x779d2 | 45 | Cocopo kill him, for all I care. Your call,\n |
| 0x77a00 | 9 | Rulutieh. |
| 0x77a0a | 31 | No... Y-You don't understand... |
| 0x77a2a | 37 | Oh, my. Now isn't THIS a grand scene? |
| 0x77a50 | 12 | Who's there? |
| 0x77a5d | 31 | You're that guy from earlier... |
| 0x77a7d | 51 | My apologies for the tribulations you've been put\n |
| 0x77ab1 | 50 | through thus far. It gave me no pleasure to play\n |
| 0x77ae4 | 22 | my role, I assure you. |
| 0x77afb | 24 | Then you guys are the... |
| 0x77b14 | 30 | Wh-Why you--Ougi, you traitor! |
| 0x77b33 | 51 | I resent that accusation. I was never one of your\n |
| 0x77b67 | 19 | dogs to begin with. |
| 0x77b7b | 51 | What happened to honor among thieves? You sold us\n |
| 0x77baf | 40 | out to the imperials, you damn turncoat! |
| 0x77bd8 | 49 | Honor among thieves? You mean thieves who don't\n |
| 0x77c0a | 48 | kill, violate women, or pillage from the poor,\n |
| 0x77c3b | 7 | surely. |
| 0x77c43 | 46 | I find it offensive that you'd liken me to a\n |
| 0x77c72 | 44 | murderous, philandering brute like yourself. |
| 0x77c9f | 50 | Hah! Pretty it up all you like, but you're still\n |
| 0x77cd2 | 31 | stealin' at the end of the day! |
| 0x77cf2 | 50 | Think however you like, sir. I did not come here\n |
| 0x77d25 | 34 | to exchange verbal spurs with you. |
| 0x77d48 | 52 | You won't be running your mouth a great deal more,\n |
| 0x77d7d | 7 | anyway. |
| 0x77d85 | 47 | Wh--You aren't gonna-- Q-Quit joking around...! |
| 0x77db5 | 51 | You befouled my sister with your lecherous hands,\n |
| 0x77de9 | 27 | insulted her aspirations... |
| 0x77e05 | 29 | Have you any last words, sir? |
| 0x77e23 | 39 | Ougi's cold smile remains as he speaks. |
| 0x77e4b | 44 | Stop that! Like hell I'm gonna die here, y-- |
| 0x77e78 | 6 | Ngh... |
| 0x77e7f | 48 | You realize this is a pointless endeavor, yes?\n |
| 0x77eb0 | 46 | Honestly, the flailings of the shortsighted... |
| 0x77edf | 12 | Hraaaaaagh!! |
| 0x77eec | 12 | That mask... |
| 0x77ef9 | 43 | Th-That man... Could that be... Sir Oshtor? |
| 0x77f25 | 29 | Damn it... Ougi, you bastard! |
| 0x77f43 | 34 | As I said, my good man. Pointless. |
| 0x77f66 | 26 | Is this your doing, Ougi!? |
| 0x77f81 | 12 | He's fast... |
| 0x77f8e | 47 | I couldn't follow that. What did he just do...? |
| 0x77fc2 | 50 | Fret not, princess. I merely struck him with the\n |
| 0x77ff5 | 17 | flat of my blade. |
| 0x78007 | 46 | This one isn't worth sullying good steel upon. |
| 0x78036 | 48 | I believe that resolves matters, Lord Oshtor...? |
| 0x78067 | 49 | You have my gratitude. Convey my thanks to Lady\n |
| 0x78099 | 28 | Nosuri for her aid, as well. |
| 0x780b6 | 52 | As you wish. The cargo we "stole" has already been\n |
| 0x780eb | 46 | moved to the designated location, so do help\n |
| 0x7811a | 9 | yourself. |
| 0x78124 | 11 | Understood. |
| 0x78130 | 49 | Ah, and I have a message from my dearest sister\n |
| 0x78162 | 8 | for you. |
| 0x7816b | 20 | Let's have it, then. |
| 0x78180 | 48 | "We only cooperated with you to put down these\n |
| 0x781b1 | 49 | brutes. There will be no future ties between us." |
| 0x781e3 | 50 | Heh... That certainly sounds like something Lady\n |
| 0x78216 | 17 | Nosuri would say. |
| 0x78228 | 47 | I'll be off, then. Until our paths cross again. |
| 0x78258 | 41 | I never imagined... Sir Oshtor himself... |
| 0x78282 | 20 | The one in the mask? |
| 0x78297 | 52 | Yes! That man... Sir Oshtor, Imperial Guard of the\n |
| 0x782cc | 44 | Right, one of the Twin Shields of Yamato...! |
| 0x782f9 | 14 | That guy, huh? |
| 0x78308 | 47 | So you've apprehended the ringleader of these\n |
| 0x78338 | 8 | bandits. |
| 0x78341 | 13 | Yeah, well... |
| 0x7834f | 48 | Had he escaped, this operation would have been\n |
| 0x78380 | 17 | deemed a failure. |
| 0x78392 | 28 | You, too, have my gratitude. |
| 0x783af | 9 | S-Sure... |
| 0x783b9 | 52 | I cannot properly reward you in a place like this,\n |
| 0x783ee | 43 | however. Expect a formal commendation soon. |
| 0x7841a | 14 | Lady Rulutieh. |
| 0x78429 | 9 | Y-Yes...? |
| 0x78433 | 51 | Shall I report that Kujyuri's plea for assistance\n |
| 0x78467 | 18 | has been answered? |
| 0x7847a | 48 | The details have been recorded in this letter.\n |
| 0x784ab | 43 | Please see that your lord father the owlo\n |
| 0x784d7 | 12 | receives it. |
| 0x784e4 | 45 | Y-Yes. I'll... pass the message along to him. |
| 0x78512 | 48 | She's gone all tense. This guy must be someone\n |
| 0x78543 | 45 | important, to make a princess like Rulutieh\n |
| 0x78571 | 8 | nervous. |
| 0x7857a | 51 | There are other matters of state that require our\n |
| 0x785ae | 44 | presence, so we'll be taking our leave, now. |
| 0x785db | 45 | Your escorts are en route to this location.\n |
| 0x78609 | 48 | Please, enjoy the remainder of your journey in\n |
| 0x7863a | 25 | their protection, milady. |
| 0x78654 | 33 | Y-Yes... Thank you for your help. |
| 0x78676 | 50 | I will pray that your travels take you down safe\n |
| 0x786a9 | 44 | roads only. For now... All forces, withdraw! |
| 0x786d6 | 22 | We'll meet again. Hup! |
| 0x786ed | 52 | Oshtor gallops away astride his woptor, the strike\n |
| 0x78722 | 30 | team following closely behind. |
| 0x78741 | 51 | They all march in perfect formation, showing just\n |
| 0x78775 | 38 | as much discipline as their commander. |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_08.json` com a forma:
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
