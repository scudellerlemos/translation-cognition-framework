# Cena ch_18_03 — pacote de traducao (168 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
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
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `after all.` -> `afinal.` (Haku, 11_07)
- `Yes, ma'am!` -> `Sim!` (Bandido, 13_05)
- `way.` -> `jeito.` (Atuy, 18_01)
- `...Uh.` -> `...Ahn.` (Haku, 14_04)
- `worry...` -> `se preocupe...` (Maroro, 18_01)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `before...?` -> `antes...?` (Haku, 18_01)
- `Head` -> `Head` (rotulo, 11_03)
- `me?` -> `mim?` (Maroro, 12_13)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `Gah!?` -> `Gah!?` (Haku, 13_01)
- `to this?` -> `a isso?` (Haku, 12_07)
- `Urgh...` -> `Argh...` (Haku, 11_06)
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
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
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
| 0x167112 | 21 | And that is the plan! |
| 0x167128 | 43 | The man Anju loves should be arriving any\n |
| 0x167154 | 14 | moment, now... |
| 0x167163 | 45 | Be sure not to hurt him. Don't go all-out--\n |
| 0x167191 | 42 | we need HIM to be the one to shine here,\n |
| 0x1671bc | 10 | after all. |
| 0x1671c7 | 49 | Just pretend to lose, go down, and let him rush\n |
| 0x1671f9 | 36 | in to rescue Anju. You all got that? |
| 0x16721e | 7 | Thieves |
| 0x167226 | 11 | Yes, ma'am! |
| 0x167232 | 48 | That's what I like to hear! Good luck, everyone. |
| 0x167263 | 5 | Thief |
| 0x167269 | 48 | A fake kidnapping, huh...? Boss sure gets some\n |
| 0x16729a | 25 | weird ideas, sometimes... |
| 0x1672b4 | 47 | Yeah, she's gettin' to be quite the busy bee.\n |
| 0x1672e4 | 39 | This is elaborate even for her, though. |
| 0x16730c | 50 | Bah, it'll be fine. What're you complaining for?\n |
| 0x16733f | 46 | It's not like we've had a ton of work, lately. |
| 0x16736e | 50 | True. And this job actually sounds like it could\n |
| 0x1673a1 | 7 | be fun. |
| 0x1673a9 | 20 | You. Nosuri, was it? |
| 0x1673be | 15 | Hm? What is it? |
| 0x1673ce | 45 | Your men's lack of passion for this mission\n |
| 0x1673fc | 46 | concerns me. Their spirit seems... lukewarm,\n |
| 0x16742b | 8 | at best. |
| 0x167434 | 44 | Ahahaha! Nothing could be further from the\n |
| 0x167461 | 6 | truth. |
| 0x167468 | 41 | Fear not! My men are hardly "lukewarm."\n |
| 0x167492 | 30 | Each possesses a fiery spirit! |
| 0x1674b1 | 48 | A fire burns in the heart of every last one of\n |
| 0x1674e2 | 49 | them, blazing brightly to aid in your quest for\n |
| 0x167514 | 5 | love! |
| 0x16751a | 46 | Astounding. I suppose I should have expected\n |
| 0x167549 | 43 | no less from the followers of a good woman. |
| 0x167575 | 27 | Ahahaha! Indeed you should. |
| 0x167591 | 48 | Boss, we just got word from the lookout. Looks\n |
| 0x1675c2 | 47 | like the guy we've been waiting for is on his\n |
| 0x1675f2 | 4 | way. |
| 0x1675f7 | 23 | Then he's finally come. |
| 0x16760f | 47 | He said to me long ago that he'd fly to me if\n |
| 0x16763f | 46 | ever I was in need... Truly, this is the man\n |
| 0x16766e | 7 | I love. |
| 0x167676 | 42 | He's here sooner than I expected, but it\n |
| 0x1676a1 | 29 | shouldn't affect the plans... |
| 0x1676bf | 48 | Well, uh. Boss. About that. It looks like he's\n |
| 0x1676f0 | 44 | got... other people with him. Like, a bunch. |
| 0x16771d | 45 | Wh-What!? But I t--I told him to... come...\n |
| 0x16774b | 29 | alone...? In my... message... |
| 0x167769 | 6 | ...Uh. |
| 0x167770 | 19 | Is something amiss? |
| 0x167784 | 45 | I-It's nothing. Nothing at all! This is all\n |
| 0x1677b2 | 45 | still w-well within my expectations. Not to\n |
| 0x1677e0 | 8 | worry... |
| 0x1677e9 | 40 | Hurry now, Oshtor. Your Anju awaits you. |
| 0x167812 | 44 | Expecting Oshtor? Yeah, sorry to disappoint. |
| 0x16783f | 6 | What!? |
| 0x167846 | 34 | H-Haku!? What are YOU doing here!? |
| 0x167869 | 50 | ...I can't believe it. She actually went through\n |
| 0x16789c | 8 | with it. |
| 0x1678a5 | 44 | I believe it is reasonable to conclude she\n |
| 0x1678d2 | 38 | possesses absolutely no capacity for\n |
| 0x1678f9 | 12 | forethought. |
| 0x167906 | 46 | I can feel that dark aura coming from Nekone\n |
| 0x167935 | 21 | even stronger, now... |
| 0x16794b | 48 | A-Ah... I don't think we should be saying that\n |
| 0x16797c | 32 | sort of thing to the princess... |
| 0x16799d | 13 | My stomach... |
| 0x1679ab | 44 | It can't be helped. A girl in love's got a\n |
| 0x1679d8 | 47 | one-track mind! I'd do the same in her shoes,\n |
| 0x167a08 | 6 | I bet. |
| 0x167a0f | 48 | For the sake of not making all our lives hell,\n |
| 0x167a40 | 19 | please don't. Ever. |
| 0x167a54 | 41 | Hm? That man... I've seen him somewhere\n |
| 0x167a7e | 10 | before...? |
| 0x167a89 | 4 | Head |
| 0x167a8e | 11 | Wh--!? YOU? |
| 0x167a9a | 48 | THIS is the man Anju has such strong affection\n |
| 0x167acb | 29 | for? That's some odd taste... |
| 0x167ae9 | 46 | A-A-Absolutely not! HAKU! What are you doing\n |
| 0x167b18 | 6 | here!? |
| 0x167b1f | 29 | OSHTOR!! Where is my Oshtor!? |
| 0x167b3d | 48 | Well, for one thing, I haven't told him a word\n |
| 0x167b6e | 40 | of what's happening, so he's not coming. |
| 0x167b97 | 48 | WHAT!? Why would you withhold information from\n |
| 0x167bc8 | 46 | him? There's no POINT if he knows nothing of\n |
| 0x167bf7 | 5 | this! |
| 0x167bfd | 47 | Well, the "ransom letter" said not to contact\n |
| 0x167c2d | 17 | the guard, right? |
| 0x167c3f | 48 | He's pretty much the head of the ENTIRE guard.\n |
| 0x167c70 | 49 | I was just following your orders. Can you blame\n |
| 0x167ca2 | 3 | me? |
| 0x167ca6 | 16 | W-Wait... truly? |
| 0x167cb7 | 50 | N-Now, uhm. Now that you mention it, I do recall\n |
| 0x167cea | 46 | putting something like that into the letter... |
| 0x167d19 | 21 | How could this be...? |
| 0x167d2f | 45 | At any rate, let's put an end to this whole\n |
| 0x167d5d | 47 | farce. Quit goofing off and let's get you home. |
| 0x167d8d | 45 | There is no "goofing off!" This is a deadly\n |
| 0x167dbb | 21 | serious matter, Haku. |
| 0x167dd1 | 41 | That attitude just makes it even worse.\n |
| 0x167dfb | 47 | Would you stop and consider your position for\n |
| 0x167e2b | 14 | just a moment? |
| 0x167e3a | 49 | You go off and do as you please, never stopping\n |
| 0x167e6c | 47 | to think of how many people you cause trouble\n |
| 0x167e9c | 4 | for! |
| 0x167ea1 | 47 | What false accusations! I have caused trouble\n |
| 0x167ed1 | 11 | for no one. |
| 0x167edd | 50 | Yeah, I'm gonna go ahead and say you're the only\n |
| 0x167f10 | 20 | one who thinks that. |
| 0x167f25 | 49 | A single sneeze from you can have repercussions\n |
| 0x167f57 | 45 | as deep as forcing a family onto the streets. |
| 0x167f85 | 48 | Don't you understand the responsibilities of a\n |
| 0x167fb6 | 42 | princess, let alone the IMPERIAL princess? |
| 0x167fe1 | 41 | What nonsense is this? A sneeze forcing\n |
| 0x16800b | 42 | homelessness upon a family? You speak in\n |
| 0x168036 | 10 | gibberish. |
| 0x168045 | 49 | D-Dear sister, is something the matter? Are you\n |
| 0x168077 | 43 | hurt? Why are your hands over your ears...? |
| 0x1680a3 | 47 | ...A-Ahaha. What... nice weather we're having\n |
| 0x1680d3 | 9 | lately... |
| 0x1680dd | 18 | I-I... suppose so? |
| 0x1680f0 | 46 | I'm getting a little, um, bored? Yeah, bored\n |
| 0x16811f | 43 | of this place. Why don't we go hit the...\n |
| 0x16814b | 11 | th-theatre? |
| 0x168157 | 29 | Ah... I don't think that's... |
| 0x168175 | 48 | Let's get you home before this g--Well, it HAS\n |
| 0x1681a6 | 41 | gotten out of hand, but it can still be\n |
| 0x1681d0 | 9 | salvaged. |
| 0x1681da | 46 | Tch. I understand your intent, now. You make\n |
| 0x168209 | 34 | these claims merely to confuse me! |
| 0x16822c | 45 | But I will not succumb! Not until my Oshtor\n |
| 0x16825a | 48 | arrives, that I may declare my truest feelings\n |
| 0x16828b | 7 | to him! |
| 0x168293 | 6 | ...Hm? |
| 0x16829a | 11 | Osh... tor? |
| 0x1682a6 | 42 | Oshtor... Where have I heard that name...? |
| 0x1682d1 | 47 | Nosuri! This man and his company seek to tear\n |
| 0x168301 | 23 | my Oshtor away from me! |
| 0x168319 | 3 | Eh? |
| 0x16831d | 48 | Please, you MUST help me! I can only rely upon\n |
| 0x16834e | 9 | you, now! |
| 0x168358 | 38 | What the hell are you talking about?\n |
| 0x16837f | 23 | Come on. Let's go home. |
| 0x168397 | 14 | I. WILL. NOT!! |
| 0x1683a6 | 8 | Hold it! |
| 0x1683af | 5 | Gah!? |
| 0x1683b5 | 42 | Not only do you dare to interfere with a\n |
| 0x1683e0 | 45 | maiden's love, but you seek to separate her\n |
| 0x16840e | 18 | from her intended? |
| 0x168421 | 44 | I'll put a stop to your meddling for good.\n |
| 0x16844e | 39 | For that is what a good woman would do! |
| 0x168476 | 40 | Great. You've gone completely nuts, too. |
| 0x16849f | 46 | Change of plans, men! We show these brigands\n |
| 0x1684ce | 37 | no mercy! Grind them into the ground! |
| 0x1684f4 | 25 | Heh, that's more like it! |
| 0x16850e | 50 | Sorry, man. Nothing against you, but if the boss\n |
| 0x168541 | 45 | wants you to take a nap, time to put you to\n |
| 0x16856f | 6 | sleep! |
| 0x168576 | 48 | Wh--? Damn it, why does it always have to come\n |
| 0x1685a7 | 8 | to this? |
| 0x1685b0 | 46 | Fine! You wanna play rough? Then let's play!\n |
| 0x1685df | 43 | We'll DRAG the princess back if we have to! |
| 0x16860b | 18 | Wh--Drag!? B-But-- |
| 0x16861e | 45 | That's right! We won't tolerate any more of\n |
| 0x16864c | 17 | your selfishness! |
| 0x16865e | 29 | Yeah! Time to give it my all! |
| 0x168681 | 6 | weapon |
| 0x168689 | 7 | Urgh... |

## 8. Formato de saida EXIGIDO
Escreva `translations_18_03.json` com a forma:
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
