# Cena ch_12_04 — pacote de traducao (506 linhas)

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
| Cohort | Organizacao | Coorte | traduzir | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Tatari | Criatura | Tatari | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Innkeeper` -> `Estalajadeira` (rotulo, 11_06)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Man` -> `Homem` (sistema, root)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Ngh...` -> `Nnh...` (Man, root)
- `Unh... urgh...` -> `Nnh... argh...` (Protagonista, 12_01)
- `this...` -> `isto...` (Kuon, 11_08)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `I see...` -> `Entendo...` (Kuon, root)
- `trouble. ` -> `trabalho. ` (Kuon, root)
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
- Homem: `Inside your dream.` -> `No seu sonho.`
- Homem: `We have enchanted you with a spell that will help\n` -> `Lançamos sobre você um feitiço que irá ajudá-lo\n`
- Homem: `you become stronger in sleep, as requested, Master.` -> `a ficar mais forte enquanto dorme, como pedido, Mestre.`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x3163e | 51 | Gah. I thought for sure my skull was gonna crack... |
| 0x31672 | 53 | Once Kuon finally releases me, I return to the inn,\n |
| 0x316a8 | 38 | where a commotion seems to be brewing. |
| 0x316cf | 28 | Huh? What's with this crowd? |
| 0x316ec | 45 | Doesn't seem like they're from around here... |
| 0x3171a | 54 | They look like they've been on the road for a while.\n |
| 0x31751 | 35 | Most of them are well-armed, too... |
| 0x31775 | 9 | Innkeeper |
| 0x3177f | 51 | So he... Explain again? He switched the, ah. Gears? |
| 0x317b3 | 50 | Right. You'll only be able to use one of them at\n |
| 0x317e6 | 50 | a time, but the machinery is in working order now. |
| 0x31819 | 54 | I work my way through the crowd of newcomers to find\n |
| 0x31850 | 29 | Kuon at the innkeeper's desk. |
| 0x3186e | 55 | She left me behind to suffer her "little punishment,"\n |
| 0x318a6 | 51 | and seems to have struck up a conversation in the\n |
| 0x318da | 9 | meantime. |
| 0x318e4 | 52 | I'm not too sure I understand, but I guess as long\n |
| 0x31919 | 24 | as the mill's working... |
| 0x31932 | 51 | Everyone'll be glad to hear we don't have to hand\n |
| 0x31966 | 35 | mill everything anymore. Thank you. |
| 0x3198a | 50 | That mill was a gift to us from the great Mikado\n |
| 0x319bd | 19 | himself, you see... |
| 0x319d1 | 51 | It would have been heartbreaking if we were never\n |
| 0x31a05 | 21 | able to use it again. |
| 0x31a1b | 17 | The great Mikado? |
| 0x31a2d | 52 | Now, as for today's pay--I'll throw in a bonus for\n |
| 0x31a62 | 28 | fixing up the mill, shall I? |
| 0x31a7f | 53 | Yes! Talk about payoff. I guess I'm finally getting\n |
| 0x31ab5 | 27 | a reward for good behavior. |
| 0x31ad1 | 54 | There's no telling what we might need the extra cash\n |
| 0x31b08 | 48 | for down the line. No point in refusing, either. |
| 0x31b39 | 51 | Oh, please, that's not necessary! Our fix is just\n |
| 0x31b6d | 50 | temporary. Save that money for a proper repairman. |
| 0x31ba0 | 15 | Wh--Wait, what? |
| 0x31bb0 | 53 | Oh, but that doesn't feel right... Please, take it.\n |
| 0x31be6 | 9 | I insist. |
| 0x31bf0 | 42 | Really, it's fine. Isn't that right, Haku? |
| 0x31c1b | 53 | Kuon seems to have noticed me, and turns to me with\n |
| 0x31c51 | 17 | a pleasant smile. |
| 0x31c63 | 30 | W-Well, I don't really think-- |
| 0x31c82 | 51 | See? Haku agrees. He doesn't really think a bonus\n |
| 0x31cb6 | 13 | is necessary. |
| 0x31cc4 | 42 | What the hell? You've gotta be kidding me! |
| 0x31cef | 53 | Is that so? Well, aren't you two just the sweetest.\n |
| 0x31d25 | 27 | All right, if you say so... |
| 0x31d41 | 6 | What!? |
| 0x31d48 | 50 | It's not as much as a bonus, but at least let me\n |
| 0x31d7b | 43 | make the best supper I can for you tonight. |
| 0x31da7 | 50 | Really? Thank you, ma'am! Your cooking is always\n |
| 0x31dda | 9 | the best. |
| 0x31de4 | 50 | Oh, stop, you're making me blush! I just hope my\n |
| 0x31e17 | 35 | best lives up to your expectations. |
| 0x31e3b | 51 | And of course she's going to eat a hellish amount\n |
| 0x31e6f | 24 | of food again. *Sigh*... |
| 0x31e88 | 10 | Rugged Man |
| 0x31e93 | 26 | Sorry to keep you waiting. |
| 0x31eae | 51 | As we continue speaking with the innkeeper, a man\n |
| 0x31ee2 | 31 | suddenly enters and interrupts. |
| 0x31f02 | 51 | Ah, him. He looked to be the one in charge of the\n |
| 0x31f36 | 38 | group outside, as far as I could tell. |
| 0x31f5d | 51 | I sent a message ahead, but I just wanted to make\n |
| 0x31f91 | 33 | sure you've got rooms for us all. |
| 0x31fb3 | 54 | Ah, yes! I've been expecting your group. You've come\n |
| 0x31fea | 27 | from far away, haven't you? |
| 0x32006 | 51 | We'll be here a few days. My men'll need food and\n |
| 0x3203a | 46 | drink--ESPECIALLY drink. We'll pay, of course. |
| 0x32069 | 48 | Even at a glance, I can tell this guy has some\n |
| 0x3209a | 50 | serious muscles. A pretty impressive beard, too,\n |
| 0x320cd | 33 | but he looks young underneath it. |
| 0x320ef | 50 | Feels like the rough-and-brazen type. He doesn't\n |
| 0x32122 | 46 | seem to give much thought to his appearance... |
| 0x32151 | 47 | Huh. I'm guessing you two are guests here, too? |
| 0x32181 | 38 | That's correct. Nice to meet you, sir. |
| 0x321a8 | 53 | Same. Sorry if things get, uh, a little rowdy while\n |
| 0x321de | 11 | we're here. |
| 0x321ea | 49 | The stranger smiles and nods apologetically. He\n |
| 0x3221c | 46 | seems like an honest, friendly sort, actually. |
| 0x3224b | 13 | Here you are. |
| 0x32259 | 52 | The innkeeper hands him a stack of wooden room keys. |
| 0x3228e | 43 | That looks to be all of 'em. Thanks, ma'am. |
| 0x322ba | 3 | Man |
| 0x322be | 48 | Master Ukon! It pleaseth my heart to report my\n |
| 0x322ef | 48 | belongings lay duly unpack'd, and await porters. |
| 0x32320 | 29 | Another man enters the inn... |
| 0x3233e | 7 | Snrrk-- |
| 0x32346 | 52 | I can't help but stifle a laugh, and I don't think\n |
| 0x3237b | 38 | anyone else here will blame me for it. |
| 0x323a2 | 38 | Not after catching a look at this guy. |
| 0x323c9 | 49 | His lanky figure, his ridiculously flashy robe,\n |
| 0x323fb | 49 | those are both fine. The makeup I can't get over. |
| 0x3242d | 14 | Ah. Well done. |
| 0x3243c | 51 | I am VERY tired, sir. Naught more now do I desire\n |
| 0x32470 | 38 | than to nap erelong in restful repose! |
| 0x32497 | 12 | "Naught"...? |
| 0x324a4 | 51 | Somehow, I manage to keep myself from laughing in\n |
| 0x324d8 | 28 | his ludicrous, painted face. |
| 0x324f5 | 42 | God, I've never seen someone whose voice\n |
| 0x32520 | 42 | matches his face so well. I can't BREATHE. |
| 0x3254b | 52 | I'm calling it now, his name is gonna be something\n |
| 0x32580 | 37 | stupidly old-fashioned, like "Maro--" |
| 0x325a6 | 50 | Really, Maroro? Seems like you get tired quicker\n |
| 0x325d9 | 25 | and quicker these days... |
| 0x325f3 | 8 | Pffffft! |
| 0x325fc | 47 | Maroro. His name is actually Maroro. Oh my God. |
| 0x3262c | 49 | Get some exercise every now and then, huh? Stop\n |
| 0x3265e | 38 | sitting behind your damn desk all day. |
| 0x32685 | 51 | Prithee, time runneth but finite and my tasks are\n |
| 0x326b9 | 40 | legion. {W360}But soft! I behold a muse! |
| 0x326e2 | 51 | Maroro's face brightens as soon as he notices Kuon. |
| 0x32716 | 7 | ...Huh? |
| 0x3271e | 52 | Fair, thy visage doth seem a bud on spring's cusp.\n |
| 0x32753 | 51 | Would that all could witness its blooming ere the\n |
| 0x32787 | 13 | day arriveth! |
| 0x32795 | 49 | Wow. Ain't often I see you get worked up over a\n |
| 0x327c7 | 13 | girl, Maroro. |
| 0x327d5 | 52 | Hast thee no eyes to see, friend? Rare even amidst\n |
| 0x3280a | 49 | the imperial capital's myriad beauties are such\n |
| 0x3283c | 20 | visions of radiance. |
| 0x32851 | 43 | Is this some kind of stunt to win my heart? |
| 0x3287d | 54 | Alack, sweet lady! Prithee, I meant no such advance!\n |
| 0x328b4 | 37 | Thy beauty hath simply captivated me. |
| 0x328da | 44 | Th-That is to say--ah, ahem! Pray ease thy\n |
| 0x32907 | 49 | suspicions and grant me thy pardon. Maroro thou\n |
| 0x32939 | 14 | mayst call me. |
| 0x32948 | 48 | If mine own eyes deceive me not as dear Master\n |
| 0x32979 | 48 | Ukon's do him, th'art our fellow guest in this\n |
| 0x329aa | 21 | place of hospitality? |
| 0x329c0 | 49 | On our company's behalf, I beg thee forgive our\n |
| 0x329f2 | 44 | unruliness anon. We seek benign revels only. |
| 0x32a1f | 52 | It's fine, really. I wouldn't be so rude as to put\n |
| 0x32a54 | 22 | a stop to a good time. |
| 0x32a6b | 30 | Heh. That so? Glad to hear it. |
| 0x32a8a | 48 | We aren't here to cause trouble. You'll barely\n |
| 0x32abb | 18 | notice we're here. |
| 0x32ace | 52 | We oughta get back to unpacking the carts, though.\n |
| 0x32b03 | 38 | No better way to work up a thirst, eh? |
| 0x32b2a | 32 | We beg your leave, sir and lady. |
| 0x32b4b | 40 | With that, the two of them head outside. |
| 0x32b74 | 46 | All right, you layabouts! Back to unloading.\n |
| 0x32ba3 | 14 | Then we feast! |
| 0x32bb2 | 14 | Ukon's Cohorts |
| 0x32bc1 | 7 | Yessir! |
| 0x32bc9 | 49 | Ukon's men respond to his rallying cry in unison. |
| 0x32bfb | 52 | And don't go causing trouble for the people around\n |
| 0x32c30 | 25 | here, you louts got that? |
| 0x32c4a | 13 | Ukon's Cohort |
| 0x32c58 | 29 | Sounds like a spirited bunch. |
| 0x32c7a | 47 | I turn to Kuon, but she's fallen silent, eyes\n |
| 0x32caa | 25 | lingering on the doorway. |
| 0x32cc4 | 5 | Kuon? |
| 0x32cca | 51 | Hm? Yes, they do seem... interesting. I'm curious\n |
| 0x32cfe | 34 | as to where they're from, I think. |
| 0x32d21 | 52 | The guy who dresses like a clown and talks like an\n |
| 0x32d56 | 34 | old play would make anyone wonder. |
| 0x32d79 | 53 | Definitely. The way he talks and carries himself...\n |
| 0x32daf | 31 | He's no ordinary person, is he? |
| 0x32dcf | 53 | The makeup, the voice, the shamoji he's carrying...\n |
| 0x32e05 | 42 | I don't even know where to start with him. |
| 0x32e30 | 49 | Oh, you noticed too, huh? I'm actually a little\n |
| 0x32e62 | 16 | impressed, Haku. |
| 0x32e73 | 40 | What're you talking about? Who wouldn't? |
| 0x32e9c | 52 | Ah, this is why I love to travel. I never would've\n |
| 0x32ed1 | 49 | expected to meet someone like that on the road... |
| 0x32f03 | 39 | So you're, uhm. Into guys like... that? |
| 0x32f2b | 35 | Seriously? Guys who look like that? |
| 0x32f4f | 52 | I didn't mean it that way, but... I suppose I like\n |
| 0x32f84 | 26 | my men more like him, yes. |
| 0x32f9f | 13 | I... I see... |
| 0x32fad | 49 | I don't believe it. She really goes in for guys\n |
| 0x32fdf | 13 | like THAT...? |
| 0x32fed | 52 | Eh, to each their own, I guess. Hardly my place to\n |
| 0x33022 | 25 | judge her for her tastes. |
| 0x3303c | 52 | But... Maybe I can use this to get on her good side. |
| 0x33071 | 50 | I see... thou preferest thine menfolk to talketh\n |
| 0x330a4 | 36 | liketh this... eth? Prithee! Verily! |
| 0x330c9 | 47 | ...Why exactly are you talking like that, Haku? |
| 0x330f9 | 44 | Methought thou enjoyest men who speaketh so. |
| 0x33126 | 15 | What ails thee? |
| 0x33136 | 32 | Kuon just gives me a cold smile. |
| 0x33157 | 51 | My heart drops into my stomach, and I try to make\n |
| 0x3318b | 48 | an escape--but her tail catches me like a lasso. |
| 0x331bc | 15 | W-Wait! Why--!? |
| 0x331cc | 9 | *Krkkk--* |
| 0x331d6 | 12 | GaaaAAAHHH!! |
| 0x331e3 | 38 | Hey, you've barely touched your cup.\n |
| 0x3320a | 15 | Come on, drink! |
| 0x3321a | 54 | Hey, we're all out over here! Could you get us three\n |
| 0x33251 | 13 | more bottles? |
| 0x3325f | 53 | The inn's tavern-like dining hall is a lot livelier\n |
| 0x33295 | 24 | than it was yesterday... |
| 0x332ae | 36 | They're quite a spirited bunch, huh? |
| 0x332d3 | 49 | So it seems. I can't say I mind the atmosphere,\n |
| 0x33305 | 7 | though. |
| 0x3330d | 54 | Kuon pours herself a cup of sake, looking faintly...\n |
| 0x33344 | 31 | nostalgic? It's hard to tell... |
| 0x33364 | 51 | So, Haku. I've been thinking about moving on from\n |
| 0x33398 | 48 | here to the imperial capital. What do you think? |
| 0x333c9 | 21 | The imperial capital? |
| 0x333df | 54 | Mhm. The only jobs we're likely to find for you here\n |
| 0x33416 | 47 | are all manual labor, which you aren't fit for. |
| 0x33446 | 53 | Suffice it to say, I don't think someone as weak as\n |
| 0x3347c | 40 | you will survive out here for very long. |
| 0x334a5 | 6 | Ngh... |
| 0x334ac | 52 | You're a lost cause in brawn, but I think you have\n |
| 0x334e1 | 29 | the brains to make up for it! |
| 0x334ff | 54 | The imperial capital would be just the place to find\n |
| 0x33536 | 34 | work for someone with your skills. |
| 0x33559 | 47 | Are you really doing all this just for my sake? |
| 0x33589 | 52 | Don't worry about it. I was planning on making for\n |
| 0x335be | 36 | the capital sooner or later, anyway. |
| 0x335e3 | 50 | If you say so. I didn't even know this place HAD\n |
| 0x33616 | 12 | a capital... |
| 0x33623 | 50 | Well, Yamato's made up of a lot of provinces, so\n |
| 0x33656 | 34 | there are actually a few capitals. |
| 0x33679 | 49 | I'm not surprised it's hard for you to picture,\n |
| 0x336ab | 49 | since all you've seen is this one little village. |
| 0x336dd | 52 | "Yamato," eh...? I can't put my finger on why, but\n |
| 0x33712 | 29 | the name does sound familiar. |
| 0x33730 | 53 | At any rate, my point is this; if we go to a proper\n |
| 0x33766 | 53 | city, it might as well be the big one. The imperial\n |
| 0x3379c | 8 | capital. |
| 0x337a5 | 49 | It's the seat of power for the Mikado, Yamato's\n |
| 0x337d7 | 27 | divine ruler. It's really-- |
| 0x337f3 | 51 | Eh, what's this? You kids planning on heading for\n |
| 0x33827 | 12 | the capital? |
| 0x33834 | 49 | One of the men at the next table suddenly turns\n |
| 0x33866 | 21 | around to address us. |
| 0x3387c | 28 | It's the guy from earlier... |
| 0x33899 | 24 | Hey, sorry to interrupt. |
| 0x338b2 | 50 | Couldn't help but overhear you two talking about\n |
| 0x338e5 | 24 | my old stomping grounds. |
| 0x338fe | 38 | You're from the imperial capital, sir? |
| 0x33925 | 51 | Yeah. I'm out on a little errand right now, though. |
| 0x33959 | 54 | But hey, I haven't even introduced myself. I'm Ukon,\n |
| 0x33990 | 23 | leader of this company. |
| 0x339a8 | 52 | My name is Kuon. This is... I suppose you can call\n |
| 0x339dd | 9 | him Haku. |
| 0x339e7 | 46 | Haku. We've been traveling together for a bit. |
| 0x33a16 | 51 | Kuon prompts me, and I keep my introduction simple. |
| 0x33a4a | 51 | Kuon and Haku, eh? Must be fate that we're all in\n |
| 0x33a7e | 39 | this inn together. Pleased to meet you. |
| 0x33aa6 | 9 | Likewise. |
| 0x33ab0 | 49 | Mmmashter Ukon, to whoooom dosht thou shpeak--?\n |
| 0x33ae2 | 35 | Ohoho, 'tish mmmmy LADY once again! |
| 0x33b06 | 49 | Drunk already, Maroro? I don't mind you getting\n |
| 0x33b38 | 48 | sauced, but keep your nose out of trouble, yeah? |
| 0x33b69 | 47 | Whaaaaat? Prithee, MASHTER Ukon. I am but the\n |
| 0x33b99 | 37 | PICture of--hic!--stone sssshobriety. |
| 0x33bbf | 51 | Ha! Sorry, Maroro, but you're not fooling anyone.\n |
| 0x33bf3 | 40 | You're as much of a lightweight as ever. |
| 0x33c1c | 52 | Bah! Mine is sssho keen a mind the Mikado HIMSHELF\n |
| 0x33c51 | 52 | doth recognizshe itsh luminance. A ssscholar am I,\n |
| 0x33c86 | 18 | lesht thou forget! |
| 0x33c99 | 23 | Snnrrkk--*cough, cough* |
| 0x33cb1 | 49 | I try to hold in my laughter as Maroro appears,\n |
| 0x33ce3 | 16 | but it's no use. |
| 0x33cf4 | 54 | I really should be prepared by now, but I can't help\n |
| 0x33d2b | 36 | it. This guy is just too damn funny. |
| 0x33d50 | 10 | Amazing... |
| 0x33d5b | 51 | If the Mikado appointed him, that means he passed\n |
| 0x33d8f | 30 | the harrowing Imperial Exam... |
| 0x33dae | 52 | I don't get it. He passed a test? A really hard one? |
| 0x33de3 | 50 | Hard enough that only one person every few years\n |
| 0x33e16 | 51 | does well enough to earn the imperial scholar rank. |
| 0x33e4a | 49 | Nyo ho ho ho ho HO! Thy wordsh do warm the very\n |
| 0x33e7c | 52 | COCKLESH of my heart. Oh, go on, shweet paragon of\n |
| 0x33eb1 | 15 | earthly beauty. |
| 0x33ec1 | 51 | If his rank is so lofty and impressive, then what\n |
| 0x33ef5 | 40 | is he doing way out here in the boonies? |
| 0x33f1e | 54 | Ho ho! Master Ukon himshelf SHEEKETH mine aid, shir,\n |
| 0x33f55 | 44 | worth fffivescore hands on shwords and more. |
| 0x33f82 | 52 | What Maroro's trying to say is I brought him along\n |
| 0x33fb7 | 50 | because he's a spellslinger. A damn good one, too. |
| 0x33fea | 53 | It seems like you've placed your confidence in him.\n |
| 0x34020 | 48 | I suppose one can expect as much from a scholar. |
| 0x34051 | 52 | Ho ho HO, forSHOOTH, such shtation cometh not from\n |
| 0x34086 | 15 | idle lazinessh! |
| 0x34096 | 37 | Nyo ho ho ho ho ho! Ha ha. Ha. Hoo... |
| 0x340bc | 36 | Maroro begins to laugh with pride... |
| 0x340e1 | 50 | ...but ultimately hangs his head and sighs deeply. |
| 0x34114 | 45 | Forsooth, Maroro is naught but a foul sham.\n |
| 0x34142 | 47 | A worthless fraud, unfit even to draw breath... |
| 0x34172 | 54 | He begins to mutter and mumble something, then takes\n |
| 0x341a9 | 33 | an enormous draught from his cup. |
| 0x341cb | 42 | H-Huh? Why's he depressed all of a sudden? |
| 0x341f6 | 54 | *Sigh* This again. Maroro has some... problems. Best\n |
| 0x3422d | 49 | if we leave him alone for now. He'll come around. |
| 0x3425f | 53 | So bizarre, for an imperial scholar to accompany an\n |
| 0x34295 | 51 | armed group so far outside the walls. What exactl-- |
| 0x342c9 | 45 | A-Ah, uhm, never mind! Please forget I said\n |
| 0x342f7 | 14 | anything, sir. |
| 0x34306 | 50 | ...If you say so. It's not really anything we've\n |
| 0x34339 | 33 | gotta keep deadly secret, y'know. |
| 0x3435b | 51 | So, you two from overseas? I haven't seen clothes\n |
| 0x3438f | 29 | like that around here before. |
| 0x343ad | 43 | Yes, sir. You could say I'm a... tourist?\n |
| 0x343d9 | 34 | Just here for sightseeing, really. |
| 0x343fc | 53 | Yeah, you don't look the "traveling merchant" type.\n |
| 0x34432 | 41 | Tourist, eh? Wish I had time to sightsee. |
| 0x3445c | 53 | Yamato's a peaceful empire, but it can be dangerous\n |
| 0x34492 | 31 | for a noble lady like yourself. |
| 0x344b2 | 53 | Especially with only one bodyguard. You've got some\n |
| 0x344e8 | 40 | serious guts, I'll give you that, missy. |
| 0x34511 | 51 | Ah, I'm sorry--I'm afraid you're mistaken. I'm no\n |
| 0x34545 | 11 | noble, sir. |
| 0x34551 | 51 | Eh? Oh, were you keeping it a secret? I should be\n |
| 0x34585 | 26 | the one apologizin', then. |
| 0x345a0 | 34 | A secret? What makes you say that? |
| 0x345c3 | 51 | Aw, come on, now. You talk and act like us common\n |
| 0x345f7 | 13 | folk, sure... |
| 0x34605 | 53 | But anyone with eyes can see you've got blue blood.\n |
| 0x3463b | 32 | And the education to match, too. |
| 0x3465c | 51 | I bet you're from some high family, maybe a minor\n |
| 0x34690 | 21 | princess. Am I close? |
| 0x346a6 | 50 | A princess? You flatter me. Or are YOU trying to\n |
| 0x346d9 | 21 | win me over now, too? |
| 0x346ef | 51 | Ha! 'Course not. Just thinking out loud. I do that. |
| 0x34723 | 49 | Well, then. I'll gladly take the compliment, sir. |
| 0x34755 | 50 | I suppose it's a lot like how you're not just an\n |
| 0x34788 | 26 | ordinary sellsword, right? |
| 0x347a3 | 15 | Ha! Bwahahaha!! |
| 0x347b3 | 14 | Ahahahahaha... |
| 0x347c2 | 47 | ...Why do I feel so uncomfortable right now...? |
| 0x347f2 | 5 | Hey-- |
| 0x347f8 | 50 | Unable to bear the uncomfortable tension between\n |
| 0x3482b | 53 | Ukon and Kuon any longer, I begin to speak up, when-- |
| 0x34861 | 27 | Ma'am! We've got a problem! |
| 0x3487d | 50 | The doors to the dining hall fly open, admitting\n |
| 0x348b0 | 23 | a panicked-looking man. |
| 0x348c8 | 50 | The talk in the hall dies quickly as he stumbles\n |
| 0x348fb | 40 | in--and soon it's as quiet as the grave. |
| 0x34924 | 52 | What are you up in such a bluster about? We've got\n |
| 0x34959 | 38 | guests from out of town to mind, here. |
| 0x34980 | 48 | That's not important right now, ma'am, please--! |
| 0x349b1 | 49 | The man runs up to the innkeeper and leans into\n |
| 0x349e3 | 20 | her ear, whispering. |
| 0x349f8 | 53 | At first, the innkeeper had been smiling patiently,\n |
| 0x34a2e | 44 | but she pales as he speaks, expression hard. |
| 0x34a5b | 44 | They both seem pretty upset. Did something\n |
| 0x34a88 | 9 | go wrong? |
| 0x34a92 | 54 | Kuon and Ukon have both gone dead silent, fixated on\n |
| 0x34ac9 | 31 | the innkeeper and the newcomer. |
| 0x34ae9 | 46 | Oh... What should we do...? We don't have an\n |
| 0x34b18 | 31 | apothecary in town right now... |
| 0x34b38 | 52 | Hey, miss. Is something the matter? Tell me what's\n |
| 0x34b6d | 31 | up and I might be able to help. |
| 0x34b8d | 14 | Man lying down |
| 0x34b9c | 14 | Unh... urgh... |
| 0x34bab | 7 | This... |
| 0x34bb3 | 50 | A man writhes on the floor, his skin bloated and\n |
| 0x34be6 | 40 | purplish in splotches, groaning in pain. |
| 0x34c0f | 51 | Another man struggles nearby, but he doesn't seem\n |
| 0x34c43 | 52 | to be in as bad a condition--only his arm is purple. |
| 0x34c78 | 50 | So you were attacked by a group of gigiri on the\n |
| 0x34cab | 6 | trail. |
| 0x34cb2 | 11 | Injured man |
| 0x34cbe | 47 | N-Nngh... Yeah. The same road we always take.\n |
| 0x34cee | 35 | A swarm of them just... appeared... |
| 0x34d12 | 50 | This guy tried to save the woptor that was being\n |
| 0x34d45 | 50 | attacked, and they turned on him. And now, well... |
| 0x34d78 | 52 | I... I-I couldn't do anything, and more than that... |
| 0x34dad | 49 | Hey. If you hadn't run, they wouldn't have been\n |
| 0x34ddf | 44 | able to find him and bring him here in time. |
| 0x34e0c | 52 | Don't guilt yourself. If anything, praise yourself\n |
| 0x34e41 | 32 | for making it back in one piece. |
| 0x34e62 | 12 | I... ghhk... |
| 0x34e6f | 31 | Hey, uh, Kuon? What's a gigiri? |
| 0x34e8f | 50 | It's a carnivorous insect with a segmented body.\n |
| 0x34ec2 | 52 | Lots of legs, hard carapace. Big, scissor-like jaws. |
| 0x34ef7 | 51 | But... while they might bite, I've never heard of\n |
| 0x34f2b | 35 | them attacking people unprovoked... |
| 0x34f4f | 54 | A... big insect... with a hard carapace and enormous\n |
| 0x34f86 | 8 | jaws...? |
| 0x34f8f | 15 | Could it be...? |
| 0x34f9f | 13 | What's wrong? |
| 0x34fad | 48 | I was... probably also attacked by one of those. |
| 0x34fde | 49 | You? But I didn't see a gigiri where I found you. |
| 0x35010 | 47 | Ah, right. When Kuon saved me, the Tatari had\n |
| 0x35040 | 20 | already absorbed it. |
| 0x35055 | 53 | I was attacked by one of those gigiri things before\n |
| 0x3508b | 22 | you came to my rescue. |
| 0x350a2 | 50 | I almost bit it, but the Tatari swallowed it and\n |
| 0x350d5 | 29 | saved me in the nick of time. |
| 0x350f3 | 51 | Are you talking about the same one that was about\n |
| 0x35127 | 15 | to swallow YOU? |
| 0x35137 | 51 | That's just like you, stumbling out of the frying\n |
| 0x3516b | 53 | pan and into the fire. You're either REALLY unlucky\n |
| 0x351a1 | 14 | or just lucky? |
| 0x351b0 | 28 | Wait, why is that "like me"? |
| 0x351cd | 4 | Huh? |
| 0x351d2 | 22 | What's with that look? |
| 0x351e9 | 51 | I mean, you're lucky in that you weren't bitten--\n |
| 0x3521d | 27 | Gigiri are highly venomous. |
| 0x35239 | 34 | That's not what I--wait, venomous? |
| 0x3525c | 41 | Venom? Are these guys gonna be all right? |
| 0x35286 | 48 | They'll probably pull through. The venom isn't\n |
| 0x352b7 | 48 | that potent, and highlanders like them tend to\n |
| 0x352e8 | 26 | have a solid constitution. |
| 0x35303 | 48 | It's only the type that paralyzes the infected\n |
| 0x35334 | 46 | host, anyway, so they're not in mortal danger. |
| 0x35363 | 24 | That's good, at least... |
| 0x3537c | 51 | So, yeah, you were definitely lucky. You wouldn't\n |
| 0x353b0 | 49 | have been able to escape if you'd been paralyzed. |
| 0x353e2 | 50 | ...I'm pretty sure it would have split me in two\n |
| 0x35415 | 46 | before the venom could have any effect anyway. |
| 0x35444 | 50 | Why aren't these guys being treated, though? You\n |
| 0x35477 | 42 | shouldn't just leave patients like that... |
| 0x354a2 | 53 | It may not be life-threatening, but I can't imagine\n |
| 0x354d8 | 40 | being bitten up like that isn't painful. |
| 0x35501 | 53 | Without a doubt, the swollen, purplish flesh around\n |
| 0x35537 | 37 | their wounds looks EXTREMELY painful. |
| 0x3555d | 50 | They sucked out the venom, looks like, but their\n |
| 0x35590 | 51 | medicine ran out. The innkeeper lady's making more. |
| 0x355c4 | 8 | I see... |
| 0x355cd | 48 | It's a rotten situation. The townsfolk say the\n |
| 0x355fe | 49 | attacks are so frequent, their stock is depleted. |
| 0x35630 | 45 | Seems they had a stroke of luck and got the\n |
| 0x3565e | 50 | ingredients for a new batch in just the other day. |
| 0x35691 | 47 | I was gonna get advice from that big brain of\n |
| 0x356c1 | 51 | Maroro's, but he's gone and drunk himself out cold. |
| 0x356f5 | 51 | Hhghk. Wh-Why...? We even burned insect-repelling\n |
| 0x35729 | 40 | incense, and they still came swarming... |
| 0x35752 | 47 | I heard there'd been more injuries from these\n |
| 0x35782 | 49 | attacks, but geez. Entire swarms? Is it that bad? |
| 0x357b4 | 43 | They've b-been... happening more and more\n |
| 0x357e0 | 39 | for... th-the last half a year or so... |
| 0x35808 | 50 | B-But they've never attacked in swarms like they\n |
| 0x3583b | 12 | did today... |
| 0x35848 | 53 | I've never heard of gigiri attacking people at all,\n |
| 0x3587e | 30 | let alone in organized groups. |
| 0x3589d | 54 | Maybe some kind of outbreak...? Could be a real pain\n |
| 0x358d4 | 39 | in the ass if we just leave them alone. |
| 0x358fc | 31 | Urgh... g-gurgh--*cough, cough* |
| 0x3591c | 54 | Hey, hang in there, all right? Is that damn medicine\n |
| 0x35953 | 10 | ready yet? |
| 0x3595e | 28 | Can't you do anything, Kuon? |
| 0x3597b | 51 | My medicines are more general-purpose. If there's\n |
| 0x359af | 43 | a specific antivenom, it'll be much better. |
| 0x359db | 50 | And treating the swelling won't dispel the pain.\n |
| 0x35a0e | 24 | Not immediately, anyway. |
| 0x35a27 | 9 | Nngghh... |
| 0x35a31 | 49 | ...But it looks like I have no choice. I didn't\n |
| 0x35a63 | 24 | want to use this, but... |
| 0x35a7c | 49 | Muttering that to herself, Kuon pulls a pair of\n |
| 0x35aae | 45 | small, round pills from her medicine pouch... |
| 0x35adc | 52 | Now put this in your mouth, but don't swallow, OK?\n |
| 0x35b11 | 28 | Just let it dissolve slowly. |
| 0x35b2e | 17 | Wh-What... is...? |
| 0x35b40 | 51 | It's an analgesic. It'll relieve your pain if you\n |
| 0x35b74 | 11 | suck on it. |
| 0x35b80 | 15 | Th-Thank you... |
| 0x35b90 | 52 | If you had something like that up your sleeve, why\n |
| 0x35bc5 | 42 | didn't you bust it out from the beginning? |
| 0x35bf0 | 55 | It's for emergencies only. And just to warn you, it's\n |
| 0x35c28 | 31 | not the greatest-tasting stuff. |
| 0x35c48 | 51 | The wounded man regards the pill with trepidation\n |
| 0x35c7c | 45 | at that, but boldly throws it into his mouth. |
| 0x35caa | 25 | Did you hear what I said? |
| 0x35cc4 | 52 | Kuon brings the second pill to the man lying down,\n |
| 0x35cf9 | 22 | holding it out to him. |
| 0x35d10 | 13 | Ah... nnhh... |
| 0x35d1e | 51 | Despite his pain, he seems to be conscious of his\n |
| 0x35d52 | 52 | surroundings, for he also takes the pill obediently. |
| 0x35d87 | 54 | There. Those should help you feel better. You'll get\n |
| 0x35dbe | 43 | some dizziness, but at least it's not pain. |
| 0x35dea | 50 | Tense moments pass, and after a while, the men's\n |
| 0x35e1d | 49 | faces lapse into peacefulness--just as Kuon said. |
| 0x35e4f | 53 | Their expressions, only just now wracked with pain,\n |
| 0x35e85 | 47 | have softened significantly. Effective stuff... |
| 0x35eb5 | 11 | Chyaaahhh!? |
| 0x35ec1 | 52 | Within moments of me letting out a sigh of relief,\n |
| 0x35ef6 | 47 | the wounded man bolts upright, grinning widely. |
| 0x35f26 | 18 | Kyeh HEH? Hyaaah!? |
| 0x35f39 | 15 | Whoa, what th-- |
| 0x35f49 | 37 | Wh-What's going on? What's happening? |
| 0x35f6f | 53 | He laughs, head swiveling wildly, then falls to the\n |
| 0x35fa5 | 46 | ground as if something inside him has snapped. |
| 0x35fd4 | 34 | Ah... ahaha, any--anyohoHOHEE HEE! |
| 0x35ff7 | 53 | The man already lying down begins drooling from his\n |
| 0x3602d | 20 | wide, dopey smile... |
| 0x36042 | 48 | Then, he leaps to his feet and begins to dance\n |
| 0x36073 | 11 | listlessly. |
| 0x3607f | 19 | Heavily injured man |
| 0x36093 | 32 | Hooohh... hoo! Hmm, hmm, hmhmhm! |
| 0x360b4 | 52 | This... isn't normal, right? This could be serious\n |
| 0x360e9 | 8 | trouble. |
| 0x360f2 | 51 | Oh, it's all right. The analgesic's concentration\n |
| 0x36126 | 52 | is pretty strong, so it's just affecting them a bit. |
| 0x3615b | 16 | This is "a bit"? |
| 0x3616c | 24 | Ukon and I share a look. |
| 0x36185 | 50 | Silently, we each confirm the other's thoughts--\n |
| 0x361b8 | 29 | This is nowhere near "a bit." |
| 0x361d6 | 48 | Isn't it, uh... maybe working a little TOO well? |
| 0x36207 | 47 | Mm. Like I said, it's for emergencies, so its\n |
| 0x36237 | 36 | effects are supposed to be powerful. |
| 0x3625c | 49 | It was originally formulated to help grievously\n |
| 0x3628e | 50 | wounded soldiers fight through the pain in battle. |
| 0x362c1 | 48 | It has some addictive qualities, too, but it's\n |
| 0x362f2 | 41 | OK as long as it's not used frequently.\n |
| 0x3631c | 10 | Besides... |
| 0x36327 | 53 | Look at them. Their pain is the last thing on their\n |
| 0x3635d | 6 | minds. |
| 0x36364 | 48 | Kuon indicates the frantically dancing man and\n |
| 0x36395 | 7 | smiles. |
| 0x3639d | 13 | I... suppose. |
| 0x363ab | 35 | Kuon's medicines are scary stuff... |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_04.json` com a forma:
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
