# Cena ch_13_06 — pacote de traducao (132 linhas)

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
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
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
- `Whoa!` -> `Uou!` (Haku, 11_11)
- `Wh--` -> `Q--` (Haku, 11_07)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `but...` -> `mas...` (Kuon, 12_16)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `What?` -> `Que?` (Haku, 12_02)
- `Head` -> `Head` (rotulo, 11_03)
- `Huh?` -> `Hein?` (Haku, 11_06)
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
- Moznu: `Ha! Well done, Nosuri. A right impressive show,\n` -> `Ha! Bom trabalho, Nosuri. Foi uma boa encenação,\n`
- Moznu: `this.` -> `essa.`
- Moznu: `Heh heh. Now, ain't this one a beauty? Lookers\n` -> `Heh heh. Ora, essa aqui é uma beldade. Cara\n`
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x73468 | 50 | Ukon leads his company deeper into the mountains\n |
| 0x7349b | 48 | to join up with the strike team waiting in the\n |
| 0x734cc | 6 | wings. |
| 0x734d3 | 34 | The journey takes maybe an hour... |
| 0x734f6 | 50 | ...and before long, the sounds of crashing metal\n |
| 0x73529 | 38 | and shouted battlecries fill our ears. |
| 0x73550 | 26 | So it's already started... |
| 0x7356b | 46 | Judging from how loud the noises are, it's a\n |
| 0x7359a | 26 | pretty large-scale battle. |
| 0x735b5 | 48 | I wouldn't stand a chance if I got involved in\n |
| 0x735e6 | 20 | something like that. |
| 0x735fb | 12 | ...Sir Haku? |
| 0x73608 | 5 | Whoa! |
| 0x73613 | 26 | N-No, it's nothing, sorry. |
| 0x7362e | 48 | That damn bird is still catching me off-guard... |
| 0x7365f | 23 | Did you need something? |
| 0x73677 | 52 | Oh... yes. I-I just... wanted to say I'm sorry for\n |
| 0x736ac | 25 | dragging you into this... |
| 0x736c6 | 52 | Dragging me into this? What, you mean guarding you\n |
| 0x736fb | 23 | while the others fight? |
| 0x73713 | 29 | Don't worry about it. Really. |
| 0x73731 | 44 | I'd rather be here than in that huge melee\n |
| 0x7375e | 37 | happening out there, that's for sure. |
| 0x73784 | 49 | Besides, this was a personal request from Ukon.\n |
| 0x737b6 | 49 | If he wants me here, then I'm not gonna complain. |
| 0x737e8 | 50 | You must have been scared, though, Rulutieh. You\n |
| 0x7381b | 14 | holding up OK? |
| 0x7382a | 51 | Even with Ukon's agents among the bandits, things\n |
| 0x7385e | 40 | could have gone pretty badly back there. |
| 0x73887 | 39 | If that Moznu guy hadn't backed down... |
| 0x738af | 16 | I-I'm all right. |
| 0x738c0 | 48 | Miss Kuon was there with me... A-And you, too,\n |
| 0x738f1 | 9 | Sir Haku. |
| 0x738fb | 50 | ...While I'm happy to hear her say that, I'm not\n |
| 0x7392e | 47 | sure there's much I would have been able to do. |
| 0x7395e | 50 | You really are noble at heart, Rulutieh. I guess\n |
| 0x73991 | 45 | I should expect nothing less from a princess. |
| 0x739bf | 39 | A-Ah--a princess--N-No, please don't... |
| 0x739e7 | 47 | Oh? Did I say something to embarrass her, or... |
| 0x73a17 | 51 | Still... I think it turned out to be a good thing\n |
| 0x73a4b | 23 | we joined up with Ukon. |
| 0x73a63 | 47 | Hmhm. Even with our terrible experience so far? |
| 0x73a93 | 49 | Yeah. I mean, say we HADN'T taken him up on his\n |
| 0x73ac5 | 48 | offer. We'd still have to take this road, right? |
| 0x73af6 | 47 | We could've gotten caught on our own by those\n |
| 0x73b26 | 8 | bandits. |
| 0x73b2f | 50 | If that happened... I dunno if we'd have made it\n |
| 0x73b62 | 30 | through unscathed like we did. |
| 0x73b81 | 52 | Even if Ukon has a mole in their ranks, there's no\n |
| 0x73bb6 | 48 | guarantee they'd risk their cover for strangers. |
| 0x73be7 | 51 | There's the distinct possibility that they'd just\n |
| 0x73c1b | 47 | as soon NOT help us to earn the bandits' trust. |
| 0x73c4b | 48 | So, yeah. I think it was the right decision to\n |
| 0x73c7c | 21 | come along with Ukon. |
| 0x73c96 | 17 | Just so! Just so. |
| 0x73ca8 | 4 | Wh-- |
| 0x73cad | 49 | Master Haku, thy fate and ours are entwine'd as\n |
| 0x73cdf | 26 | the vine is unto the stem! |
| 0x73cfa | 40 | M-Maroro? Didn't you go with the others? |
| 0x73d23 | 49 | Hardly! The prospect of abandoning thee wracked\n |
| 0x73d55 | 48 | my heart with worry. Ukon bade me stay, when I\n |
| 0x73d86 | 22 | asked the boon of him. |
| 0x73d9d | 8 | I see... |
| 0x73da6 | 46 | Maroro's magic is nothing if not a powerhouse. |
| 0x73dd5 | 48 | It's reassuring to have him with us, for sure,\n |
| 0x73e06 | 6 | but... |
| 0x73e0d | 43 | ...I can't honestly say I'm HAPPY about it? |
| 0x73e39 | 48 | But to speak truth--so afear'd was poor Maroro\n |
| 0x73e6a | 50 | that his heart did threaten to beat out his chest! |
| 0x73e9d | 52 | He'd been pale and trembling, true--but then, it's\n |
| 0x73ed2 | 37 | difficult to tell through the makeup. |
| 0x73ef8 | 45 | Is he really going to be all that helpful...? |
| 0x73f26 | 51 | Ah, but would that my companions told me of their\n |
| 0x73f5a | 42 | scheme! Is Maroro so undeserving of trust? |
| 0x73f85 | 46 | I don't think they had a choice. Any hint of\n |
| 0x73fb4 | 41 | suspicion might've ruined the whole ruse. |
| 0x73fde | 33 | That's the way it is, I'm afraid. |
| 0x74000 | 51 | All we have to do is wait for Ukon and the others\n |
| 0x74034 | 12 | to get back. |
| 0x74041 | 6 | ...Hm? |
| 0x74048 | 8 | ...Huh!? |
| 0x74051 | 52 | Useless fuckin' SHIT-ass sentries! How'd they even\n |
| 0x74086 | 32 | find the hideout to begin with!? |
| 0x740a7 | 6 | Bandit |
| 0x740ae | 47 | B-Boss, uh... Y'think maybe that Nosuri broad\n |
| 0x740de | 37 | ratted us out? Just think about it... |
| 0x74104 | 5 | What? |
| 0x7410a | 48 | Just 'cause you've gotta great pair of tits in\n |
| 0x7413b | 48 | your face, do you gotta believe everything she\n |
| 0x7416c | 5 | says? |
| 0x74172 | 52 | Shut it! You all saw 'em. A man's only got so much\n |
| 0x741a7 | 50 | willpower with those things right in front of him! |
| 0x741da | 20 | Yeah, fair enough... |
| 0x741ef | 19 | Boss's got a point. |
| 0x74203 | 52 | Heh... Too bad for The Chest, though. I'll bet she\n |
| 0x74238 | 46 | never woulda dreamed there's a secret passage. |
| 0x74267 | 52 | Now, let's scram. We'll regroup, figure out how to\n |
| 0x7429c | 23 | get revenge on that b-- |
| 0x742b4 | 4 | Head |
| 0x742b9 | 6 | WHUT!? |
| 0x742c0 | 15 | Wh-What is it!? |
| 0x742d0 | 42 | These guys--It's the bandits from earlier! |
| 0x742fb | 37 | Wh-What the hell are YOU doin' here!? |
| 0x74321 | 26 | B-Boss, what should we do? |
| 0x7433c | 48 | Hah! What're you, an idiot? We smash some heads! |
| 0x7436d | 48 | Ain't this a nice little surprise, you fallin'\n |
| 0x7439e | 45 | into my lap again? Like moths to the flame,\n |
| 0x743cc | 10 | aren'tcha? |
| 0x743d7 | 52 | Heh heh. I'll be sure to give you plenty of lovin'\n |
| 0x7440c | 24 | after we get outta here. |
| 0x74425 | 49 | All right, boys! Tie the women up, and give the\n |
| 0x74457 | 26 | guys what's comin' to 'em! |
| 0x74472 | 19 | Get back, Rulutieh! |
| 0x74486 | 5 | Eep-- |
| 0x74493 | 18 | A-Ah, no, Cocopo-- |
| 0x744b8 | 17 | Please, just run! |
| 0x744ca | 47 | What're you saying? I can't just leave you to\n |
| 0x744fa | 9 | this guy. |
| 0x74504 | 27 | No, you don't understand... |
| 0x74522 | 48 | Please, all of you--get away as fast as you can! |
| 0x74553 | 4 | Huh? |
| 0x74558 | 23 | Eh? What're you sayin'? |
| 0x74570 | 50 | This bird is a gentle soul, but... I-If you make\n |
| 0x745a3 | 35 | Cocopo angry... Y-You'll regret it! |
| 0x745c7 | 48 | Pfffft. You think threatening me with your big\n |
| 0x745f8 | 32 | bird is gonna work, little girl? |
| 0x74619 | 5 | Gyah! |
| 0x7461f | 9 | Hngaaah!! |
| 0x74629 | 4 | Eh!? |
| 0x7462e | 27 | So that's what she meant... |
| 0x74662 | 9 | RightFoot |
| 0x7466c | 8 | LeftFoot |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_06.json` com a forma:
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
