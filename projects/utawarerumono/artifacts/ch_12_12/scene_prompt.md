# Cena ch_12_12 — pacote de traducao (198 linhas)

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
| Boro-Gigiri | Criatura | Boro-Gigiri | manter_original | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
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
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `Villager` -> `Aldeão` (SISTEMA, 12_08)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
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
| 0x46330 | 27 | Hhah--h-hah--hah, wheeze... |
| 0x4634c | 50 | Seems like we were able to get away for the time\n |
| 0x4637f | 40 | being, thanks to Kuon's flash grenade... |
| 0x463a8 | 46 | Ukon and the other survivors grind to a stop\n |
| 0x463d7 | 44 | around me, looking as out-of-breath as I am. |
| 0x46404 | 27 | D-Doth fate preserve us...? |
| 0x46420 | 50 | Hey, how long are you gonna keep clinging to me?\n |
| 0x46453 | 17 | Get off, already. |
| 0x46465 | 5 | Gyeh! |
| 0x4646b | 53 | I disentangle myself from Maroro's vice grip around\n |
| 0x464a1 | 8 | my legs. |
| 0x464aa | 49 | I'm exhausted. With Maroro weighing me down the\n |
| 0x464dc | 44 | whole way, my body's already at its limit... |
| 0x46509 | 24 | Hey, kid. You all right? |
| 0x46522 | 52 | Ukon looks over at me, carrying several men on his\n |
| 0x46557 | 49 | shoulders--even dragging some others with a rope. |
| 0x46589 | 51 | He managed to rescue all those people despite the\n |
| 0x465bd | 9 | danger... |
| 0x465c7 | 46 | Damn it, there's a lot of guys missing. Hope\n |
| 0x465f6 | 11 | they're OK. |
| 0x46602 | 53 | A quick headcount reveals only about half the group\n |
| 0x46638 | 20 | made it out with us. |
| 0x4664d | 47 | Most of them probably just got separated, but\n |
| 0x4667d | 47 | undoubtedly some wounded had to be left behind. |
| 0x466ad | 50 | Man. And to think that you were on the mark this\n |
| 0x466e0 | 42 | whole time, anxious about a Boro-Gigiri... |
| 0x4670b | 35 | Boro-Gigiri? You mean the huge one? |
| 0x4672f | 53 | Yeah. My parents used to warn me when I was a kid--\n |
| 0x46765 | 50 | Don't go into the woods alone or you'll get eaten. |
| 0x46798 | 50 | I thought it was just a bogeyman. Never actually\n |
| 0x467cb | 51 | seen one in the flesh. Didn't think they were real. |
| 0x467ff | 53 | Never expected to see one pop up now, of all times... |
| 0x46835 | 53 | It's just like you've been saying. Going up against\n |
| 0x4686b | 40 | that thing is a fool's errand, for sure. |
| 0x46894 | 41 | Sorry. I should have made myself clearer. |
| 0x468be | 50 | If I had, this wouldn't have... No. Too late for\n |
| 0x468f1 | 9 | that now. |
| 0x468fb | 52 | Hey, no. I'm not gonna have you getting all guilty\n |
| 0x46930 | 44 | over this. It's my fault for being careless. |
| 0x4695d | 6 | *WHAP* |
| 0x46964 | 52 | Ukon pounds his fist into his palm in frustration.\n |
| 0x46999 | 51 | It seems like he's taking his anger out on himself. |
| 0x469cd | 29 | So, what are we gonna do now? |
| 0x469eb | 48 | Maroro. You know anything about the Boro-Gigiri? |
| 0x46a1c | 50 | Ho? Erst I read of the beast in some old tome or\n |
| 0x46a4f | 17 | other, mayhaps... |
| 0x46a61 | 51 | Whatever you can tell us. Anything is more useful\n |
| 0x46a95 | 13 | than nothing. |
| 0x46aa3 | 53 | Hmm. Hmmmm, and hmmmm again. 'Tis a likelihood that\n |
| 0x46ad9 | 49 | the swarm is but her brood, and she their mother. |
| 0x46b0b | 52 | Ere the spawning-season beginneth, one amongst the\n |
| 0x46b40 | 51 | gigiri doth grow as unto a titan, and giveth birth! |
| 0x46b74 | 53 | So engorge'd, under her bulk do her children swarm,\n |
| 0x46baa | 44 | seeking as one horde what prey fate sendeth. |
| 0x46bd7 | 36 | So it attacked us to feed its young. |
| 0x46bfc | 51 | Indubitably. I'faith, the breeding months are not\n |
| 0x46c30 | 50 | yet upon us, and the gigiri oft favor far warmer\n |
| 0x46c63 | 20 | climes than these... |
| 0x46c78 | 50 | But upon rare occasion, fate conspireth to bring\n |
| 0x46cab | 50 | about such monstrosities in circumstance aberrant. |
| 0x46cde | 44 | And there, I fear, lies the boundary of my\n |
| 0x46d0b | 10 | knowledge. |
| 0x46d16 | 51 | Huh. I guess that stuff about him being a scholar\n |
| 0x46d4a | 24 | wasn't a joke after all. |
| 0x46d63 | 50 | So if the Boro-Gigiri are the parents, does that\n |
| 0x46d96 | 24 | mean they come in pairs? |
| 0x46daf | 52 | One can but assume. Alas, the fine details are but\n |
| 0x46de4 | 30 | esoteric, and unknown to me... |
| 0x46e03 | 3 | Hm. |
| 0x46e07 | 29 | Ukon looks lost in thought... |
| 0x46e25 | 16 | Something wrong? |
| 0x46e36 | 27 | Eh... No. I don't think so. |
| 0x46e52 | 9 | I'm back. |
| 0x46e5c | 38 | Ah, welcome back. How is it out there? |
| 0x46e83 | 29 | It was just as you predicted. |
| 0x46ea1 | 12 | I knew it... |
| 0x46eae | 33 | Prithee, of what dost thou speak? |
| 0x46ed0 | 31 | Oh, they're chasing us, is all. |
| 0x46ef0 | 11 | *Mutter*... |
| 0x46efc | 24 | Sshh. They'll notice us. |
| 0x46f15 | 47 | Kuon tries to quiet everyone down as a murmur\n |
| 0x46f45 | 28 | spreads through the group... |
| 0x46f62 | 5 | Kuon? |
| 0x46f68 | 19 | Kuon's ears twitch. |
| 0x46f7c | 12 | *Krrkkkk*... |
| 0x46f89 | 53 | Barely a sound disturbs the clearing except for the\n |
| 0x46fbf | 27 | distant rustling of bushes. |
| 0x46fdb | 27 | They're heading this way... |
| 0x46ff7 | 9 | Villagers |
| 0x47001 | 8 | Gasp--!! |
| 0x4700a | 19 | It'll be all right. |
| 0x47022 | 49 | They're still off at quite a distance. We'll be\n |
| 0x47054 | 12 | OK, I think. |
| 0x47061 | 49 | At Kuon's words, everyone seems to calm a little. |
| 0x47093 | 51 | Speak plain. Dost thou believe the scent of blood\n |
| 0x470c7 | 20 | draweth them nearer? |
| 0x470dc | 28 | The scent... That's right... |
| 0x470f9 | 51 | This isn't good. We can't exactly erase the smell\n |
| 0x4712d | 39 | so long as we have the injured with us. |
| 0x47155 | 34 | Looks like we'll have to fight it. |
| 0x47178 | 8 | ...What? |
| 0x47181 | 8 | Villager |
| 0x4718a | 52 | Th-That's impossible! There's no way we'll stand a\n |
| 0x471bf | 28 | chance against that monster! |
| 0x471dc | 49 | A villager cries out his protest, clutching his\n |
| 0x4720e | 12 | wounded arm. |
| 0x4721b | 49 | I won't lie to you. It's reckless, and with our\n |
| 0x4724d | 50 | forces in this shape, we can't really execute on\n |
| 0x47280 | 17 | any kind of plan. |
| 0x47292 | 30 | ...So it really is impossible. |
| 0x472b1 | 50 | Even if I was right in the end, it's not exactly\n |
| 0x472e4 | 12 | vindicating. |
| 0x472f1 | 52 | In an ideal situation, I'd like to be able to fall\n |
| 0x47326 | 48 | back and regroup so we can organize ourselves... |
| 0x47357 | 48 | But doing that now risks luring it back to the\n |
| 0x47388 | 40 | village. We have to make our stand here. |
| 0x473b1 | 38 | Everyone falls silent at Ukon's words. |
| 0x473d8 | 26 | Come to think of it, Haku? |
| 0x473f3 | 3 | Hm? |
| 0x473f7 | 49 | I'm surprised you came out of being attacked by\n |
| 0x47429 | 30 | one of those things all right. |
| 0x47448 | 46 | I was not "all right." It was about to eat me! |
| 0x47477 | 49 | I only survived because that other Tatari thing\n |
| 0x474a9 | 44 | showed up and ate it before IT could eat ME. |
| 0x474d6 | 24 | I see. And that's why... |
| 0x474ef | 52 | Ahahaha, and that's why you were about to be eaten\n |
| 0x47524 | 53 | by a Tatari? You have either the worst or best luck\n |
| 0x4755a | 22 | in the world, I think. |
| 0x47571 | 47 | It's nothing to laugh about! I was in serious\n |
| 0x475a1 | 8 | trouble! |
| 0x475aa | 51 | But you survived, so it made for a good story, at\n |
| 0x475de | 6 | least. |
| 0x475e5 | 52 | The way things are going, I'm gonna be making more\n |
| 0x4761a | 49 | of those great "I almost died" stories right now. |
| 0x4764c | 47 | Geez... If only a Tatari could come along and\n |
| 0x4767c | 27 | swallow this one up, too... |
| 0x47698 | 7 | ...Huh? |
| 0x476a0 | 22 | What did you just say? |
| 0x476b7 | 49 | I'm about to make more of those "I almost died"\n |
| 0x476e9 | 8 | stories? |
| 0x476f2 | 15 | No, after that. |
| 0x47702 | 52 | If only a Tatari could come along and swallow this\n |
| 0x47737 | 11 | one up too? |
| 0x47743 | 52 | That's it! That's it. We'll just have this one get\n |
| 0x47778 | 18 | eaten by a Tatari. |
| 0x4778b | 41 | Huh? Eaten up by... What? There's no way. |
| 0x477b5 | 53 | Haku, look around. Doesn't this place look familiar\n |
| 0x477eb | 7 | to you? |
| 0x477f3 | 52 | At Kuon's prompting, I take a quick glance around... |
| 0x47828 | 33 | Hm? This place... Could it be...? |
| 0x4784a | 54 | Then it's decided. I'll go bait the Tatari and bring\n |
| 0x47881 | 8 | it here. |
| 0x4788a | 51 | I'll need you to... push the Boro-Gigiri off that\n |
| 0x478be | 26 | cliff over there. Somehow. |
| 0x478d9 | 52 | H-How can you ask--how are we supposed to actually\n |
| 0x4790e | 8 | DO that? |
| 0x47917 | 22 | Well... Try your best? |
| 0x4792e | 46 | Try our b--You're just leaving it to us, then. |
| 0x4795d | 48 | We're running out of time and this is our best\n |
| 0x4798e | 28 | shot. We're lost, otherwise. |
| 0x479ab | 22 | Now, hold on a second. |
| 0x479c2 | 38 | Ukon, PLEASE talk some sense into her. |
| 0x479e9 | 36 | Missy... You're really OK with this? |
| 0x47a0e | 52 | Eh heh heh. I may not look it, but I'm pretty good\n |
| 0x47a43 | 45 | at running. You won't have to worry about me. |
| 0x47a71 | 4 | Hey! |
| 0x47a76 | 21 | Ahahaha... Hey, Haku. |
| 0x47a8c | 47 | You know, you really are an interesting person. |
| 0x47abc | 43 | With that, Kuon dashes off into the forest. |
| 0x47ae8 | 30 | ...So, what should we do, kid? |
| 0x47b07 | 34 | You're leaving it to me, too, huh? |
| 0x47b2a | 50 | Well, you and her came up with this plan, so I'm\n |
| 0x47b5d | 31 | assuming you can execute on it. |
| 0x47b7d | 25 | What am I supposed to do? |
| 0x47b97 | 51 | They follow the scent of blood, so... If we could\n |
| 0x47bcb | 44 | distract them with an even stronger scent... |
| 0x47bf8 | 38 | Is there any of that rotten stew left? |
| 0x47c1f | 35 | This stuff? Yeah, there's a little. |
| 0x47c43 | 48 | OK. We're gonna need anyone who can still move\n |
| 0x47c74 | 46 | to act as decoys and peel the little ones off. |
| 0x47ca3 | 45 | The less severely injured who can carry the\n |
| 0x47cd1 | 49 | incapacitated will get them out of here in that\n |
| 0x47d03 | 7 | window. |
| 0x47d0b | 49 | And the rest of us will lure the Boro-Gigiri to\n |
| 0x47d3d | 47 | this cliff once the swarm has been baited away. |
| 0x47d6d | 52 | ...That's about as good of a plan as I can come up\n |
| 0x47da2 | 15 | with right now. |
| 0x47db2 | 45 | ...Fast thinking, in a situation like this... |
| 0x47de0 | 26 | Hm? Did you say something? |
| 0x47dfb | 45 | No, nothing. It's a good plan. It could work. |
| 0x47e29 | 42 | You heard him, men. Everyone OK with that? |
| 0x47e54 | 29 | The men around us slowly nod. |
| 0x47e72 | 48 | Hey, you're sure, right? I was just running my\n |
| 0x47ea3 | 39 | mouth with whatever came to mind, so... |
| 0x47ecb | 50 | Considering we're improvising here, it's all good. |
| 0x47efe | 46 | OK. If you're fine with it, then I've got no\n |
| 0x47f2d | 11 | objections. |
| 0x47f39 | 42 | All right. Kid! Maroro! Let's get to work! |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_12.json` com a forma:
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
