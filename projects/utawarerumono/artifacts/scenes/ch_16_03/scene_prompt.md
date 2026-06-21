# Cena ch_16_03 — pacote de traducao (189 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Yuuri | Personagem | Yuuri | manter_original | none |

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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `at all.` -> `nada.` (Haku, 16_01)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `trouble.` -> `de verdade.` (Haku, 12_04)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `*Swish*...` -> `*Fiu*...` (Haku, 12_03)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `EEP!?` -> `EEEK!?` (Atuy, 16_01)
- `Are you OK?` -> `Está bem?` (Kuon, 13_09)
- `least.` -> `enfim.` (Ukon, 12_12)
- `Phew...` -> `Ufa...` (Haku, 12_16)
- `Head` -> `Head` (rotulo, 11_03)
- `Man` -> `Hom` (Sistema, 12_04)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
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
| 0xe2e25 | 27 | ...She really came with us. |
| 0xe2e41 | 48 | Don't you worry, Yuuri! I'm here to protect you. |
| 0xe2e72 | 21 | Ah... Th-Thank you... |
| 0xe2e88 | 41 | But, um, it's hard to walk when you're... |
| 0xe2eb2 | 36 | Oh, don't worry about that, silly.\n |
| 0xe2ed7 | 24 | I'm just supporting you! |
| 0xe2ef0 | 13 | No, I mean... |
| 0xe2efe | 45 | Man, what am I gonna do? Atuy still doesn't\n |
| 0xe2f2c | 47 | know about Yuuri's lover, let alone her gender. |
| 0xe2f5c | 47 | To make matters worse, I thought she was just\n |
| 0xe2f8c | 45 | forming a little crush, but she's head over\n |
| 0xe2fba | 6 | heels. |
| 0xe2fc1 | 45 | It... kinda feels too late to just tell her\n |
| 0xe2fef | 32 | the truth and hope for the best. |
| 0xe3014 | 44 | Yeah, all right. I haven't heard anything,\n |
| 0xe3041 | 47 | haven't seen anything. Nope. Nothing going on\n |
| 0xe3071 | 7 | at all. |
| 0xe3079 | 31 | Urgh... This smell is... rough. |
| 0xe3099 | 42 | We happen to be in a sewer, so yes. It is. |
| 0xe30c4 | 44 | Be that as it may, you don't have to be so\n |
| 0xe30f1 | 17 | blunt about it... |
| 0xe3103 | 43 | It cannot be helped. Egress via the sewer\n |
| 0xe312f | 40 | tunnels is the best method of escaping\n |
| 0xe3158 | 10 | detection. |
| 0xe3163 | 46 | Take comfort in the fact that we will not be\n |
| 0xe3192 | 47 | traversing the sewer canal proper, if nothing\n |
| 0xe31c2 | 5 | else. |
| 0xe31c8 | 41 | ...If I recall... The canal below us is\n |
| 0xe31f2 | 20 | expressly for waste. |
| 0xe3207 | 45 | Yeah, this is probably better than trudging\n |
| 0xe3235 | 23 | through that by a mile. |
| 0xe324d | 46 | Hey, Yuuri, are you hungry? I made bento, so\n |
| 0xe327c | 33 | we can eat together, if you like. |
| 0xe329e | 31 | Huh? N-No, thank you, that's... |
| 0xe32be | 45 | Whoa, there, take it down a notch or three.\n |
| 0xe32ec | 45 | A romantic bento lunch in the sewers is NOT\n |
| 0xe331a | 10 | happening. |
| 0xe3325 | 42 | Watch your step, you two. You don't want\n |
| 0xe3350 | 18 | to trip down here. |
| 0xe3363 | 6 | O-OK-- |
| 0xe336a | 11 | Understood. |
| 0xe3376 | 5 | Um... |
| 0xe337c | 49 | I understand why we're here, but maybe a little\n |
| 0xe33ae | 21 | warning next time...? |
| 0xe33c4 | 44 | I'm sorry for putting you through all this\n |
| 0xe33f1 | 8 | trouble. |
| 0xe33fa | 42 | Huh? Oh, no, I didn't mean it like that... |
| 0xe3425 | 42 | Sorry. If you really can't deal with it,\n |
| 0xe3450 | 41 | just tell me. I'm not forcing you to do\n |
| 0xe347a | 15 | anything, here. |
| 0xe348a | 4 | Huh? |
| 0xe348f | 26 | N-No, not at all, really-- |
| 0xe34aa | 48 | Really? If that's the case, then don't mind if\n |
| 0xe34db | 19 | I do. I'm outta h-- |
| 0xe34ef | 10 | *Swish*... |
| 0xe34fa | 48 | Kuon's tail slips efficiently around the crown\n |
| 0xe352b | 11 | of my head. |
| 0xe3537 | 21 | *KRRKKKKK KRKK KRK--* |
| 0xe354d | 32 | Ow ow OW OK IT WAS JUST A JOKE-- |
| 0xe356e | 44 | Dear sister, perhaps you SHOULD let him go\n |
| 0xe359b | 31 | back, if he desires it so much. |
| 0xe35bb | 45 | If you throw him into the channel ahead, he\n |
| 0xe35e9 | 45 | should be able to get out by riding the flow. |
| 0xe3617 | 37 | By way of the sewer canal, naturally. |
| 0xe363d | 28 | You're right. Let's do that. |
| 0xe365a | 36 | Now, hold on, that's not even funn-- |
| 0xe367f | 40 | I'm only kidding, but hopefully you've\n |
| 0xe36a8 | 20 | learned your lesson. |
| 0xe36bd | 32 | We aren't throwing him in, then? |
| 0xe36de | 5 | Huh!? |
| 0xe36e4 | 22 | Sh-She's not joking... |
| 0xe36fb | 30 | Nekone is scary. Really scary. |
| 0xe371a | 18 | *Squeak, squeak--* |
| 0xe372d | 5 | Eep!? |
| 0xe3733 | 13 | Whoa, there-- |
| 0xe3741 | 11 | Are you OK? |
| 0xe374d | 19 | Y-Yes, thank you... |
| 0xe3761 | 43 | It's dangerous there. Walk on this side a\n |
| 0xe378d | 12 | little more. |
| 0xe379a | 6 | ...OK. |
| 0xe37a1 | 21 | Eek, my foot slipped! |
| 0xe37b7 | 10 | Ah!? Hey-- |
| 0xe37c2 | 46 | It's so scaaary down here. Is it OK if I get\n |
| 0xe37f1 | 14 | closer to you? |
| 0xe3800 | 33 | It's like I'm watching a farce... |
| 0xe3822 | 42 | It should be this way. Oshtor's map says\n |
| 0xe384d | 39 | we should take the next left, then...\n |
| 0xe3875 | 20 | We're getting close. |
| 0xe388a | 44 | Thank God. We'll be free of this smell, at\n |
| 0xe38b7 | 6 | least. |
| 0xe38be | 7 | Phew... |
| 0xe38c6 | 48 | Hey Yuuri, what are you gonna do when all this\n |
| 0xe38f7 | 8 | is over? |
| 0xe3900 | 43 | After this? I'm leaving the capital behind. |
| 0xe392c | 11 | Eh? Really? |
| 0xe3938 | 46 | Yes. The plan is to meet with another escort\n |
| 0xe3967 | 41 | outside the walls, then go on from there. |
| 0xe3991 | 33 | Oh, crap, she's looking this way. |
| 0xe39b3 | 26 | Did I say something wrong? |
| 0xe39ce | 32 | Huh... That sounds, um... rough. |
| 0xe39ef | 24 | I know! Maybe together-- |
| 0xe3a08 | 45 | --we'll be able to make the handoff without\n |
| 0xe3a36 | 8 | a hitch. |
| 0xe3a3f | 46 | Sorry, Atuy, but I'm not gonna let you say it. |
| 0xe3a6e | 42 | Geez, don't pop a vein making that face.\n |
| 0xe3a99 | 24 | I said it for your sake! |
| 0xe3ab2 | 47 | I had my doubts, but she's really planning to\n |
| 0xe3ae2 | 15 | go with her...? |
| 0xe3af2 | 49 | Naturally, I have calculated the most efficient\n |
| 0xe3b24 | 43 | route to our goal while still considering\n |
| 0xe3b50 | 8 | stealth. |
| 0xe3b59 | 47 | Even if we are pursued, shaking off any tails\n |
| 0xe3b89 | 40 | or shadows should be a matter of course. |
| 0xe3bb2 | 44 | ...She says that all matter-of-factly, but\n |
| 0xe3bdf | 34 | she's still puffing out her chest. |
| 0xe3c02 | 46 | You really are great at devising these plans\n |
| 0xe3c31 | 15 | for us, Nekone. |
| 0xe3c41 | 33 | I-I... I am not so great as that. |
| 0xe3c63 | 42 | You needn't be so modest! You really are\n |
| 0xe3c8e | 44 | incredible, Neko. Give yourself some credit. |
| 0xe3cbb | 44 | So, uh, what are we gonna do if there's an\n |
| 0xe3ce8 | 44 | ambush at the exit? All our sneaking won't\n |
| 0xe3d15 | 10 | mean jack. |
| 0xe3d20 | 9 | ...I, uh. |
| 0xe3d2a | 47 | Say, for instance, if they came advancing out\n |
| 0xe3d5a | 7 | of th-- |
| 0xe3d62 | 4 | Head |
| 0xe3d67 | 5 | Head1 |
| 0xe3d6d | 17 | Ad... vancing...? |
| 0xe3d7f | 21 | Way to jinx it, love. |
| 0xe3d95 | 31 | Is it that fun bullying Nekone? |
| 0xe3db5 | 47 | N-Now wait a second, how did you get THAT out\n |
| 0xe3de5 | 45 | of what I said? Your logic doesn't make any\n |
| 0xe3e13 | 7 | sense-- |
| 0xe3e1b | 47 | Ahem. I don't know who you are, but I take it\n |
| 0xe3e4b | 42 | you have some business with us, gentlemen? |
| 0xe3e76 | 3 | Man |
| 0xe3e7a | 45 | Weeeell, seems we surprised you. Nah, we're\n |
| 0xe3ea8 | 26 | just lookin' for somebody. |
| 0xe3ec3 | 45 | Someone called... Yuuri. That ring any bells? |
| 0xe3ef1 | 6 | Ngh... |
| 0xe3ef8 | 24 | Nope, can't say it does. |
| 0xe3f11 | 44 | Huh. Then I guess it can't be helped. Shame. |
| 0xe3f3e | 44 | Why don't you keep us company for a little\n |
| 0xe3f6b | 11 | while, huh? |
| 0xe3f77 | 7 | Ruffian |
| 0xe3f7f | 13 | Eh heh heh... |
| 0xe3f8d | 45 | Lucky us. They're all lookers, every one of\n |
| 0xe3fbb | 4 | 'em. |
| 0xe3fc0 | 11 | Bastards... |
| 0xe3fcc | 23 | Wh-Who are you people-- |
| 0xe3fe4 | 37 | Weren't you busy looking for someone? |
| 0xe400a | 44 | Oh, don't get me wrong, we got that to do.\n |
| 0xe4037 | 45 | But I ain't gonna look a sexy gift horse in\n |
| 0xe4065 | 10 | the mouth. |
| 0xe4070 | 46 | Heh heh. So many beauties in such an obscure\n |
| 0xe409f | 46 | place... Can you blame a guy for takin' what\n |
| 0xe40ce | 11 | life gives? |
| 0xe40da | 22 | Nekone, get behind me! |
| 0xe40f1 | 47 | So... the group pursuing Yuuri finally showed\n |
| 0xe4121 | 44 | up, but they can't see through the disguise. |
| 0xe414e | 47 | ...But they're total lowlives, so we're gonna\n |
| 0xe417e | 18 | get jumped anyway. |
| 0xe4191 | 28 | What's this hazy feeling...? |
| 0xe41ae | 45 | Whoa, now, don't you move. Resist if that's\n |
| 0xe41dc | 44 | your thing, but you don't wanna be damaged\n |
| 0xe4209 | 16 | goods, now, huh? |
| 0xe421a | 45 | We'll show you a REAL good time if you play\n |
| 0xe4248 | 13 | along, heh... |
| 0xe4256 | 5 | Ngh-- |
| 0xe425c | 45 | Hey, now, didn't I just tell you not to move? |
| 0xe428a | 47 | We can sell the men to the right buyers, too.\n |
| 0xe42ba | 32 | Don't go givin' us trouble, now. |
| 0xe42db | 48 | We don't mind killin' one of you as a warning,\n |
| 0xe430c | 12 | if we hafta. |
| 0xe4319 | 47 | How interesting... So there are men like this\n |
| 0xe4349 | 35 | even in the Mikado's own holy city. |
| 0xe436d | 46 | The capital's become so dense that this kind\n |
| 0xe439c | 49 | of thing happens right under the Mikado's nose... |
| 0xe43ce | 11 | Sir Haku... |
| 0xe43da | 35 | Hm? Hey, it's gonna be all right.\n |
| 0xe43fe | 24 | You'll be safe. Promise. |
| 0xe4417 | 5 | Oh... |
| 0xe441d | 7 | O-OK... |
| 0xe4425 | 48 | Yee hee. Awful confident, aren't you, big guy?\n |
| 0xe4456 | 40 | Showing off in front of your ladyfriend? |
| 0xe447f | 40 | Just how are you gonna protect her, huh? |
| 0xe44a8 | 26 | What do you mean "how"...? |
| 0xe44c3 | 33 | Hah, all right. This one's mine-- |

## 8. Formato de saida EXIGIDO
Escreva `translations_16_03.json` com a forma:
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
