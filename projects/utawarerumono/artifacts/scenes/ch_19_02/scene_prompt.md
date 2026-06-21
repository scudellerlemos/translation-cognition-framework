# Cena ch_19_02 — pacote de traducao (334 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Nosuri Bandits | Organizacao | Bandidos Nosuri | traduzir | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Head` -> `Head` (rotulo, 11_03)
- `Brigand` -> `Bandido` (SISTEMA, 13_05)
- `...Haku?` -> `...Haku?` (Garota, 16_01)
- `Are you... sure?` -> `Tem... certeza?` (Protagonista, 17_01)
- `terrifying...` -> `assustador...` (Haku, 18_01)
- `but...` -> `mas...` (Kuon, 12_16)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `crime?` -> `crime?` (Oshtor, 19_01)
- `Alone?` -> `Sozinho?` (Kuon, root)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `right?` -> `né?` (Haku, 12_03)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `...What do you mean?` -> `...O que você quer dizer?` (Garota, 16_01)
- `That's...` -> `Isso...` (Haku, 15_01)
- `I think.` -> `acho.` (Kuon, 12_11)
- `for it.` -> `por isto.` (Homem, 17_01)
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
- Moznu: `Ha! Well done, Nosuri. A right impressive show,\n` -> `Ha! Bom trabalho, Nosuri. Foi uma boa encenação,\n`
- Moznu: `this.` -> `essa.`
- Moznu: `Heh heh. Now, ain't this one a beauty? Lookers\n` -> `Heh heh. Ora, essa aqui é uma beldade. Cara\n`
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
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
| 0x1746a9 | 11 | EXI_B0535_A |
| 0x1746b6 | 11 | EXI_B0535_C |
| 0x1746c2 | 4 | Head |
| 0x1746c7 | 7 | Brigand |
| 0x1746cf | 13 | Zzz... zzz... |
| 0x1746dd | 29 | Momma... That's my... food... |
| 0x1746fb | 47 | ...Worked like a charm. That sleeping incense\n |
| 0x17472b | 25 | stuff is pretty powerful. |
| 0x174745 | 40 | They should be asleep for a while now.\n |
| 0x17476e | 50 | I'd say they probably won't wake up until morning. |
| 0x1747a1 | 22 | Plenty of time for us. |
| 0x1747b8 | 53 | Wait. I don't think it'd be good to go in just yet.\n |
| 0x1747ee | 51 | The smoke hasn't dispersed, so if you breathe in... |
| 0x174826 | 8 | ...Haku? |
| 0x17482f | 27 | Gah!? What? I'm wide awake. |
| 0x17484b | 16 | Are you... sure? |
| 0x17485c | 49 | That was close... It smells sweet, but I didn't\n |
| 0x17488e | 30 | expect it to be this potent... |
| 0x1748ad | 36 | ...It should be safe now, I think.\n |
| 0x1748d2 | 18 | Are you all ready? |
| 0x1748e5 | 12 | Yeah, ready. |
| 0x1748f2 | 28 | Haku, this area looks clear. |
| 0x17490f | 51 | Let's keep moving, then. We need to round them up\n |
| 0x174943 | 36 | before they realize what's going on. |
| 0x174968 | 47 | Hm... I'm not used to just casually strolling\n |
| 0x174998 | 34 | into my target location like this. |
| 0x1749bb | 51 | Indeed. Our modus operandi was typically to sneak\n |
| 0x1749ef | 47 | through in the dead of night, while they slept. |
| 0x174a1f | 48 | After seeing this, it makes me wonder what all\n |
| 0x174a50 | 22 | that effort was for... |
| 0x174a67 | 49 | You were a gentlewoman thief who acted with all\n |
| 0x174a99 | 50 | due tradition, nobility, and decorum, dear sister. |
| 0x174acc | 37 | Not really sure how much decorum is\n |
| 0x174af2 | 36 | involved in breaking and entering... |
| 0x174b17 | 42 | But tactics like these are almost taboo.\n |
| 0x174b42 | 50 | Just think--what if this gas was a lethal poison\n |
| 0x174b75 | 11 | instead...? |
| 0x174b81 | 47 | He must be well aware of this, yet he doesn't\n |
| 0x174bb1 | 41 | bat an eye at such unthinkable methods.\n |
| 0x174bdb | 13 | Terrifying... |
| 0x174be9 | 50 | Truly. All audacity and atrocity is met with the\n |
| 0x174c1c | 27 | same unruffled nonchalance. |
| 0x174c38 | 42 | ...Why do I get the feeling you guys are\n |
| 0x174c63 | 27 | bad-mouthing me over there? |
| 0x174c7f | 50 | Hardly. If anything, it is praise. Little wonder\n |
| 0x174cb2 | 42 | you drew Oshtor's eye, with such artifice. |
| 0x174cdd | 48 | Now that I think about it, I guess you do have\n |
| 0x174d0e | 45 | a knack for these jobs, Haku. It's a little\n |
| 0x174d3c | 6 | scary. |
| 0x174d43 | 49 | Scheming and underhanded tactics are just about\n |
| 0x174d75 | 32 | the only thing he's any good at. |
| 0x174d96 | 40 | Is this really how these guys see me...? |
| 0x174dbf | 44 | Um... Sir Haku, I... I think you're amazing! |
| 0x174dec | 16 | Uh... th-thanks. |
| 0x174dfd | 40 | Anyway, let's get this over with, quick. |
| 0x174e26 | 51 | All I do is try whatever pops into my mind first.\n |
| 0x174e5a | 43 | I don't think that's anything praiseworthy. |
| 0x174e86 | 6 | But... |
| 0x174e8d | 43 | To think he would dare hide behind my name! |
| 0x174eb9 | 3 | Hm? |
| 0x174ebd | 48 | And stealing from the poor and the helpless...\n |
| 0x174eee | 40 | I never imagined he could sink that low. |
| 0x174f17 | 20 | Mm? Oh, yeah. Right. |
| 0x174f2c | 45 | Keep it together... Gotta stick to the story. |
| 0x174f5a | 48 | I asked Ougi to arrange a meeting with Nosuri,\n |
| 0x174f8b | 30 | somewhere we wouldn't be seen. |
| 0x174faa | 27 | Seems like you're doing OK. |
| 0x174fc6 | 20 | ...What do you want? |
| 0x174fdb | 47 | What do you have to gain from chatting with a\n |
| 0x17500b | 48 | wanted criminal? Or have you come to capture me? |
| 0x17503c | 50 | I guess the whole princess abduction is weighing\n |
| 0x17506f | 15 | heavy on her... |
| 0x17507f | 44 | Well, let's see if I can turn things around. |
| 0x1750ac | 50 | About that--There's something I think you should\n |
| 0x1750df | 5 | know. |
| 0x1750e5 | 30 | You have something to tell me? |
| 0x175104 | 46 | Yeah. You're being accused of several crimes\n |
| 0x175133 | 49 | right now... but do you know what they actually\n |
| 0x175165 | 4 | are? |
| 0x17516a | 14 | Of course not. |
| 0x175179 | 48 | Hey, come on. This stuff specifically involves\n |
| 0x1751aa | 38 | you. How can you actually not know...? |
| 0x1751d1 | 45 | Tales of my exploits are often exaggerated.\n |
| 0x1751ff | 45 | I can't be expected to remember every detail. |
| 0x17522d | 46 | Wonder how true that is. Well, at least this\n |
| 0x17525c | 41 | makes it a little more convenient for me. |
| 0x175286 | 48 | ...What if I told you that you're being framed\n |
| 0x1752b7 | 41 | for most of the crimes you're accused of? |
| 0x1752e1 | 29 | What's that supposed to mean? |
| 0x1752ff | 25 | Well, just hear me out... |
| 0x175319 | 49 | So Moznu and his cronies are claiming to be the\n |
| 0x17534b | 48 | Nosuri Thieves whenever he commits a dastardly\n |
| 0x17537c | 6 | crime? |
| 0x175383 | 47 | Nosuri furrows her brow after hearing my story. |
| 0x1753b3 | 51 | That's right. We looked into it, and it turns out\n |
| 0x1753e7 | 49 | he was the one who set you up in the first place. |
| 0x175419 | 16 | I had no idea... |
| 0x17542a | 31 | So that's where we're at now.\n |
| 0x17544a | 44 | At this rate, you'll end up blamed for all\n |
| 0x175477 | 20 | Moznu's crimes, too. |
| 0x17548c | 13 | I understand. |
| 0x17549a | 49 | As head of the Nosuri bandits, I will take down\n |
| 0x1754cc | 46 | Moznu with my own hands, even if it costs me\n |
| 0x1754fb | 8 | my life. |
| 0x175504 | 38 | Hey, hold on. Let's not be hasty here. |
| 0x17552b | 45 | He may be a villain, but he even evaded the\n |
| 0x175559 | 48 | capital forces. Ougi and I will be risking our\n |
| 0x17558a | 6 | lives. |
| 0x175591 | 48 | And why exactly do you two have to take him on\n |
| 0x1755c2 | 6 | alone? |
| 0x1755c9 | 47 | That's the right and proper way to do things!\n |
| 0x1755f9 | 48 | This is a righteous battle to reclaim our honor. |
| 0x17562a | 44 | Look, hold on a second before you make any\n |
| 0x175657 | 34 | decisions. Just hear me out first. |
| 0x17567a | 49 | If you can find a way to capture Moznu instead,\n |
| 0x1756ac | 41 | then we have a way of clearing your name. |
| 0x1756d6 | 5 | Hm... |
| 0x1756dc | 50 | He's been using the Nosuri Thieves' name, but if\n |
| 0x17570f | 52 | YOU'RE the ones who catch him, they might give you\n |
| 0x175744 | 24 | a full pardon in return. |
| 0x17575d | 49 | And in order to do that, we need proof that you\n |
| 0x17578f | 30 | were the ones that caught him. |
| 0x1757ae | 49 | Had to lie a little more than I thought, but if\n |
| 0x1757e0 | 41 | that's what it'll take to convince her... |
| 0x17580a | 40 | Moznu's really getting screwed here...\n |
| 0x175833 | 42 | I kinda feel bad, but it's not like he's\n |
| 0x17585e | 18 | innocent, I guess. |
| 0x175871 | 52 | I see. You could be right... But how would I prove\n |
| 0x1758a6 | 34 | that I was the one who caught him? |
| 0x1758c9 | 45 | Killing Moznu won't do any good, but we can\n |
| 0x1758f7 | 42 | clear your name if we just turn him over\n |
| 0x175922 | 14 | to the guards. |
| 0x175931 | 41 | Hm...? I'm a wanted criminal, aren't I?\n |
| 0x17595b | 33 | How am I supposed to turn him in? |
| 0x17597d | 48 | We'll tag along as witnesses. That should keep\n |
| 0x1759ae | 29 | everyone safe from suspicion. |
| 0x1759cc | 50 | And as an added bonus, I can get my hands on all\n |
| 0x1759ff | 30 | the treasure Moznu's stolen... |
| 0x175a1e | 49 | I'm serving the public good! Who could blame me\n |
| 0x175a50 | 39 | for living like a king afterwards...?\n |
| 0x175a78 | 7 | NO ONE! |
| 0x175a80 | 19 | What? But that's... |
| 0x175a94 | 47 | Those are our conditions. Otherwise, we can't\n |
| 0x175ac4 | 26 | take you to their hideout. |
| 0x175adf | 45 | I suppose I'm not in a position to argue...\n |
| 0x175b0d | 22 | I appreciate the help. |
| 0x175b24 | 20 | You can count on us. |
| 0x175b39 | 46 | Nosuri gives me a nod, and gets up to leave.\n |
| 0x175b68 | 41 | After I'm sure she's gone, I also get up. |
| 0x175b92 | 52 | Looks like I got her mind off that whole mess with\n |
| 0x175bc7 | 52 | the princess. She still seemed to be feeling guilty. |
| 0x175bfc | 47 | Now, I should prepare as well. It IS a bandit\n |
| 0x175c2c | 49 | hideout... Gotta think of how to carry all that\n |
| 0x175c5e | 9 | treasure. |
| 0x175c68 | 49 | Let's see, a carriage, a steed or two, rope for\n |
| 0x175c9a | 41 | tying things down... Time to get busy...! |
| 0x175cc4 | 44 | I didn't expect this much help from you...\n |
| 0x175cf1 | 45 | I thought you would just put in a good word\n |
| 0x175d1f | 7 | for us. |
| 0x175d27 | 46 | Hey, don't worry about it. We're taking down\n |
| 0x175d56 | 42 | the bad guys here. Justice is on our side. |
| 0x175d81 | 40 | I... see... Yes, I suppose you're right. |
| 0x175daa | 46 | I... had no idea you had put so much thought\n |
| 0x175dd9 | 20 | into it, Sir Haku... |
| 0x175dee | 14 | Huh? Uh, yeah. |
| 0x175dfd | 51 | I mean, it's only natural as a citizen of Yamato,\n |
| 0x175e31 | 6 | right? |
| 0x175e38 | 35 | Yes! An admirable creed to live by. |
| 0x175e5c | 8 | ...What? |
| 0x175e65 | 55 | When you say such responsible and respectable things,\n |
| 0x175e9d | 46 | it just makes you seem even more suspicious... |
| 0x175ecc | 9 | Agreed... |
| 0x175ed6 | 42 | What kind of guy do you two think I am...? |
| 0x175f01 | 24 | Just don't go overboard. |
| 0x175f1a | 20 | ...What do you mean? |
| 0x175f2f | 48 | Wait, does she know I'm going for the bandits'\n |
| 0x175f60 | 44 | treasure...? Haha, nah... that's ridiculous. |
| 0x175f8d | 35 | There are only a few still awake.\n |
| 0x175fb1 | 33 | They seem to be having a drink... |
| 0x175fd3 | 23 | Think you can hit them? |
| 0x175feb | 47 | If I can find a clear shot, then yes, I'm sure. |
| 0x17601b | 47 | It would appear the gentlemen just over there\n |
| 0x17604b | 29 | are all still hale and alert. |
| 0x176069 | 50 | We didn't expect the smoke to reach the farthest\n |
| 0x17609c | 47 | part of the caves anyway. Now, our next move... |
| 0x1760cc | 48 | ...Let's wait and see what they're doing, first. |
| 0x1760fd | 46 | Gyahaha! Who'da thought I'd have a knack for\n |
| 0x17612c | 10 | this shit? |
| 0x176137 | 49 | We didn't expect it either, boss! Your textiles\n |
| 0x176169 | 44 | are sellin' like hotcakes! You're a natural! |
| 0x176196 | 49 | Hey, I'm a bandit! I've seen some quality shit.\n |
| 0x1761c8 | 47 | I can tell the best stuff just as good as any\n |
| 0x1761f8 | 9 | merchant. |
| 0x176202 | 50 | Who knows, us bandits might even be better at it\n |
| 0x176235 | 15 | than them! Har! |
| 0x176245 | 46 | But, Boss, we didn't even know how to handle\n |
| 0x176274 | 9 | yer idea! |
| 0x17627e | 51 | Nobody else woulda thought to use the stolen cash\n |
| 0x1762b2 | 40 | to start a business! Boss, yer a genius! |
| 0x1762db | 45 | Gah hah hyah! That's it, boys, tell me more\n |
| 0x176309 | 48 | 'bout how great I am. And let's get more booze\n |
| 0x17633a | 9 | out here! |
| 0x176344 | 13 | Got it, Boss. |
| 0x176352 | 50 | ...Boys, I been thinkin'. Maybe... This could be\n |
| 0x176385 | 40 | our time to give up the ol' bandit life. |
| 0x1763ae | 17 | Eh? Y-Yeh mean... |
| 0x1763c0 | 49 | Been doin' this shit for ages now, but it ain't\n |
| 0x1763f2 | 52 | any stable kinda life. 'Bout time I straightened up. |
| 0x176427 | 30 | B-But... what about us, Boss!? |
| 0x176446 | 50 | Quit yer whinin'! I ain't gonna leave yeh out in\n |
| 0x176479 | 45 | the cold. We're practically family, ain't we? |
| 0x1764a7 | 12 | All brigands |
| 0x1764b4 | 8 | Ohhhhhh! |
| 0x1764bd | 48 | That's great, Boss! I can finally go back home\n |
| 0x1764ee | 23 | with my head held high! |
| 0x176506 | 51 | There's... a girl I was sweet on for a long time!\n |
| 0x17653a | 45 | I gave up on her, but... I could try askin'\n |
| 0x176568 | 8 | her out! |
| 0x176571 | 53 | Maybe now I can finally send some money home to Ma,\n |
| 0x1765a7 | 28 | fer all she's done fer me... |
| 0x1765c4 | 51 | Damn right yeh can! I'm gonna make all yer wishes\n |
| 0x1765f8 | 10 | come true! |
| 0x176603 | 28 | Three cheers for the Boss!\n |
| 0x176620 | 33 | Hip hip hooray! Hip hip hooray!\n |
| 0x176642 | 15 | Hip hip hooray! |
| 0x176652 | 47 | They certainly seem to be having a lovely time. |
| 0x176682 | 50 | ...Ah... Are we really going through with this...? |
| 0x1766b5 | 42 | ...We don't have much of a choice anymore. |
| 0x1766e0 | 51 | But... they're saying they're giving up banditry... |
| 0x176714 | 32 | That may be, but think about it. |
| 0x176735 | 51 | That money they're using is all thanks to someone\n |
| 0x176769 | 31 | else's sweat, blood, and tears. |
| 0x176789 | 9 | That's... |
| 0x176793 | 48 | And I don't see any remorse about stealing it.\n |
| 0x1767c4 | 47 | You think people will be safe with these guys\n |
| 0x1767f4 | 7 | around? |
| 0x1767fc | 45 | I... suppose you're right. All of that does\n |
| 0x17682a | 18 | make sense, but... |
| 0x17683d | 48 | I'm actually starting to wonder if we're doing\n |
| 0x17686e | 49 | the right thing... Is justice really on our side? |
| 0x1768a0 | 53 | But if we stop here, I'll never get enough treasure\n |
| 0x1768d6 | 40 | to live a life of sweet, sweet hedonism. |
| 0x1768ff | 34 | Shall we carry out the plan, then? |
| 0x176922 | 37 | I see. Yes, it seems sound in theory. |
| 0x176948 | 48 | But how to capture him? The man has struck and\n |
| 0x176979 | 52 | eluded capture many times... He is prey not easily\n |
| 0x1769ae | 9 | cornered. |
| 0x1769b8 | 45 | True. They do have a tendency to get out of\n |
| 0x1769e6 | 44 | sticky situations... So we're going to set\n |
| 0x176a13 | 7 | a trap. |
| 0x176a1b | 34 | I see. A reasonable enough course. |
| 0x176a3e | 46 | First, we make all the lookouts fall asleep.\n |
| 0x176a6d | 44 | We can use Kuon's sleeping incense for that. |
| 0x176a9a | 20 | A soporific incense? |
| 0x176aaf | 47 | One whiff, and even the toughest thug will be\n |
| 0x176adf | 30 | sleeping like a baby... right? |
| 0x176afe | 33 | That's the general idea, I guess. |
| 0x176b20 | 51 | Of course, it's an incense, so I think we'll have\n |
| 0x176b54 | 42 | to keep in mind the wind, the geography... |
| 0x176b7f | 48 | I'll leave all that to you. An amateur like me\n |
| 0x176bb0 | 30 | would only mess that stuff up. |
| 0x176bcf | 51 | After that, we can catch the rest by surprise and\n |
| 0x176c03 | 50 | force them out. Better than fighting them head-on. |
| 0x176c36 | 40 | Elegant in its simplicity, to be sure.\n |
| 0x176c5f | 43 | However, how do you propose we force them\n |
| 0x176c8b | 16 | from their base? |
| 0x176c9c | 40 | Kuon, did those smoke bombs come out OK? |
| 0x176cc5 | 53 | Mhm. I've never made one before, so I'm not sure...\n |
| 0x176cfb | 47 | But it can at least make a thick smokescreen,\n |
| 0x176d2b | 8 | I think. |
| 0x176d34 | 29 | That should be perfect, then. |
| 0x176d52 | 47 | Anyone will believe there's a fire if there's\n |
| 0x176d82 | 46 | smoke. I'm sure they'll panic and make a run\n |
| 0x176db1 | 7 | for it. |
| 0x176db9 | 49 | When people stop thinking rationally, they tend\n |
| 0x176deb | 29 | to react in predictable ways. |
| 0x176e09 | 49 | And if all goes according to plan, that's where\n |
| 0x176e3b | 18 | we take them down. |
| 0x176e4e | 13 | Yep, exactly. |
| 0x176e5c | 44 | Couldn't we just put the whole lot of them\n |
| 0x176e89 | 9 | to sleep? |
| 0x176e93 | 40 | ...Well, it'd be nice if we could, but-- |
| 0x176ebc | 41 | Soporific incense is a little tricky...\n |
| 0x176ee6 | 45 | In a closed space, the smoke won't disperse\n |
| 0x176f14 | 9 | properly. |
| 0x176f1e | 43 | And you probably don't want to take a nap\n |
| 0x176f4a | 28 | with a pack of bandits, huh? |
| 0x176f67 | 52 | ...So we smoke them out of the cave, and eliminate\n |
| 0x176f9c | 34 | them while they remain in a panic. |
| 0x176fbf | 49 | That's the idea. We can make changes on the fly\n |
| 0x176ff1 | 14 | if we need to. |
| 0x177000 | 22 | ...By the way, Ougi... |
| 0x177017 | 16 | How may I serve? |
| 0x177028 | 52 | I know it's to save your sister, but you ARE lying\n |
| 0x17705d | 37 | to her. You sure you're OK with that? |
| 0x177083 | 28 | Me? Lie to my dear sister?\n |
| 0x1770a0 | 42 | I have never done such a thing in my life. |
| 0x1770cb | 50 | ...Kinda contradicting yourself there, aren't you? |
| 0x1770fe | 11 | Not at all. |
| 0x17710a | 51 | My dear sister has little choice but to cooperate\n |
| 0x17713e | 32 | with this plan for her own good. |
| 0x17715f | 48 | Naturally, it is my duty to ensure the process\n |
| 0x177190 | 46 | is as simple and painless for her as possible. |
| 0x1771bf | 50 | Moreover... if you carry a secret to the pits of\n |
| 0x1771f2 | 36 | Denebokshiri, it ceases to be a lie. |
| 0x177217 | 47 | I was wondering why this guy would be OK with\n |
| 0x177247 | 48 | the plan when he's so dedicated to his sister... |
| 0x177278 | 50 | But I didn't expect him to be this devious about\n |
| 0x1772ab | 51 | it... Note to self: never insult Nosuri around him. |
| 0x1772df | 34 | Haku. I believe it's about time... |
| 0x177302 | 32 | Guess so. Let's get going, then. |
| 0x177323 | 41 | *Cough, hack* D-Dammit, what's goin' on!? |
| 0x17734d | 22 | B-Boss, it's smoke...! |
| 0x177364 | 52 | W-Wasn't someone s'posed to be watchin' the fire!?\n |
| 0x177399 | 7 | *Cough* |
| 0x1773a1 | 48 | Hold it right there. I suggest you come quietly. |
| 0x1773d2 | 47 | *Cough, cough* Y-YOU...! So all this shit was\n |
| 0x177402 | 36 | your idea, huh!? Outta the damn way! |
| 0x177427 | 36 | I'm afraid we cannot let you escape. |
| 0x17744c | 47 | I'll make you pay... How dare you tarnish the\n |
| 0x17747c | 46 | noble Nosuri Thieves' name with such heinous\n |
| 0x1774ab | 7 | crimes! |
| 0x1774b3 | 46 | Shit! I dunno what you're talking about, but\n |
| 0x1774e2 | 48 | you're dead meat now! You can't win up against\n |
| 0x177513 | 10 | ALL of us! |
| 0x17751e | 46 | All right, boys! Time to put an end to this,\n |
| 0x17754d | 17 | once and for all! |
| 0x17755f | 13 | U-Uh, Boss... |
| 0x17756d | 43 | WHAT!? Eh...? Where's the rest of the boys? |
| 0x177599 | 46 | Sorry, but the guys you had posted out there\n |
| 0x1775c8 | 38 | are taking a little nap at the moment. |
| 0x1775ef | 52 | DAMMIT! Well, we can still beat the shit outta you\n |
| 0x177624 | 43 | just fine on our own! Tear 'em apart, boys! |
| 0x177650 | 12 | On it, Boss! |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_02.json` com a forma:
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
