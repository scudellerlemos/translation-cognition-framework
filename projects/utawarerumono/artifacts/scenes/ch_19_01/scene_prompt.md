# Cena ch_19_01 — pacote de traducao (240 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `today.` -> `hoje.` (Atuy, 18_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Wh--` -> `Q--` (Haku, 11_07)
- `...Right. ` -> `...Tá.` (Haku, 14_10)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `anyway.` -> `de agora.` (Ougi, 13_08)
- `like this...` -> `assim...` (Rulutieh, 17_01)
- `nicely.` -> `direitinho.` (Haku, 11_09)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `sister.` -> `irmã.` (Ukon, 14_04)
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
| 0x16e944 | 20 | ...You have arrived. |
| 0x16e959 | 48 | Oshtor welcomes us, though his voice is stern.\n |
| 0x16e98a | 45 | Nekone had asked Kuon and me to come to the\n |
| 0x16e9b8 | 6 | manor. |
| 0x16e9bf | 52 | This time, we were told to leave Rulutieh and Atuy\n |
| 0x16e9f4 | 21 | back at headquarters. |
| 0x16ea0a | 50 | That alone told me this wasn't going to be about\n |
| 0x16ea3d | 45 | a job... It had to be some kind of emergency. |
| 0x16ea6b | 48 | Allow me to explain why I have called upon you\n |
| 0x16ea9c | 6 | today. |
| 0x16eaa3 | 46 | It concerns Her Highness's abduction several\n |
| 0x16ead2 | 47 | days ago, and the fate of the bandits involved. |
| 0x16eb02 | 46 | Regardless of her safe return, the abduction\n |
| 0x16eb31 | 36 | itself cannot be so easily forgiven. |
| 0x16eb56 | 48 | They have thus been charged with high treason,\n |
| 0x16eb87 | 43 | and will receive due punishment for their\n |
| 0x16ebb3 | 8 | actions. |
| 0x16ebbc | 51 | Yeah, I figured something like this might happen.\n |
| 0x16ebf0 | 19 | Wait, that means... |
| 0x16ec04 | 49 | If we'd taken any longer, it might have been us\n |
| 0x16ec36 | 39 | up against the wall. Geez... close one. |
| 0x16ec5e | 53 | Her Highness did make all efforts to proclaim their\n |
| 0x16ec94 | 43 | innocence, but her words fell on deaf ears. |
| 0x16ecc0 | 42 | Why can't they just admit that she lied?\n |
| 0x16eceb | 50 | A proper scolding would resolve the whole thing,\n |
| 0x16ed1e | 10 | I'd think. |
| 0x16ed29 | 52 | The holy imperial princess does not make mistakes.\n |
| 0x16ed5e | 47 | Rather... she cannot be seen to make a mistake. |
| 0x16ed8e | 49 | We were forced to mobilize the soldiers for her\n |
| 0x16edc0 | 45 | sake. It can no longer be passed off lightly. |
| 0x16edee | 50 | Her Highness WAS abducted. The offenders are now\n |
| 0x16ee21 | 47 | enemies of the throne, and must face judgement. |
| 0x16ee51 | 42 | ...I see now. So that's what's going on... |
| 0x16ee7c | 21 | Man, I hate politics. |
| 0x16ee92 | 49 | But if things have gotten this far out of hand,\n |
| 0x16eec4 | 15 | Anju must be... |
| 0x16eed4 | 40 | Yes. She has locked herself in her room. |
| 0x16eefd | 43 | The punishment for high treason is death.\n |
| 0x16ef29 | 48 | Her Highness's naivete has cost their lives...\n |
| 0x16ef5a | 13 | It pains her. |
| 0x16ef68 | 47 | Makes sense... The guilt must be eating her up. |
| 0x16ef98 | 33 | Quite unfair, wouldn't you say?\n |
| 0x16efba | 48 | We merely wished to help, and it seems this is\n |
| 0x16efeb | 11 | our reward. |
| 0x16eff7 | 35 | A calm voice speaks from behind us. |
| 0x16f01b | 52 | Surprised, we quickly turn to see Nosuri's brother\n |
| 0x16f050 | 23 | standing there... Ougi. |
| 0x16f068 | 16 | When did you...? |
| 0x16f079 | 37 | Shortly after you arrived, I believe. |
| 0x16f09f | 30 | Been here the whole time, huh? |
| 0x16f0be | 45 | Be at ease--I was the one who summoned him.\n |
| 0x16f0ec | 46 | He will be essential in resolving this matter. |
| 0x16f11b | 16 | Well, OK then... |
| 0x16f12c | 46 | But you knew the princess's identity, right?\n |
| 0x16f15b | 49 | Any reason you didn't stop your partner in crime? |
| 0x16f18d | 53 | I believe I have mentioned, but I generally refrain\n |
| 0x16f1c3 | 51 | from standing in the way of my dear sister's plans. |
| 0x16f1f7 | 48 | And now look what's happened. Do you want your\n |
| 0x16f228 | 37 | sister to ruin her life or something? |
| 0x16f24e | 49 | Haha... You underestimate her. A situation such\n |
| 0x16f280 | 47 | as this is a brief inconvenience; nothing more. |
| 0x16f2b0 | 39 | It's CLEARLY a little more than that.\n |
| 0x16f2d8 | 43 | Seems more like the two of you are screwed. |
| 0x16f304 | 48 | And my presence here, as one of the accused...\n |
| 0x16f335 | 50 | indicates that you would prefer our heads remain\n |
| 0x16f368 | 9 | attached? |
| 0x16f372 | 47 | Ougi smiles meaningfully in Oshtor's direction. |
| 0x16f3a2 | 52 | Ougi's attitude seems to elicit a dry chuckle from\n |
| 0x16f3d7 | 43 | Oshtor... and the general turns to face me. |
| 0x16f403 | 42 | And this, Lord Haku, is where you come in. |
| 0x16f42e | 3 | Hm? |
| 0x16f432 | 41 | I would have you help them in escaping,\n |
| 0x16f45c | 28 | with stealth and discretion. |
| 0x16f479 | 4 | Wh-- |
| 0x16f47e | 45 | Of course, I would not force this upon you.\n |
| 0x16f4ac | 44 | If you fear for your safety, simply forget\n |
| 0x16f4d9 | 12 | my proposal. |
| 0x16f4e6 | 40 | I will not judge you for your refusal.\n |
| 0x16f50f | 44 | Having asked you to serve as accomplice in\n |
| 0x16f53c | 38 | such a scheme, I am in no position to. |
| 0x16f563 | 47 | Whatever my reasons, I AM asking that you aid\n |
| 0x16f593 | 45 | Her Highness's abductors in escaping the law. |
| 0x16f5c1 | 49 | Should this reach the public ear, the crime and\n |
| 0x16f5f3 | 45 | consequence of high treason will fall to you. |
| 0x16f621 | 49 | I would not hesitate to disavow any association\n |
| 0x16f653 | 53 | with you. Or I may be forced to silence you myself,\n |
| 0x16f689 | 22 | to keep matters quiet. |
| 0x16f6a4 | 14 | Your thoughts? |
| 0x16f6b3 | 49 | Oshtor meets my eyes gravely, awaiting my answer. |
| 0x16f6e5 | 48 | I give it some thought, slap my knee, and give\n |
| 0x16f716 | 16 | him the verdict. |
| 0x16f727 | 14 | Sure! Why not. |
| 0x16f736 | 49 | Are you sure about this? If word ever gets out,\n |
| 0x16f768 | 41 | it'll be our heads on the chopping block. |
| 0x16f792 | 35 | There's no surprise in her voice.\n |
| 0x16f7b6 | 29 | Just asking for confirmation. |
| 0x16f7d4 | 44 | That's fine. It's partly our fault anyway.\n |
| 0x16f801 | 42 | I'd feel pretty lousy abandoning them now. |
| 0x16f82c | 52 | Haha... I knew you were something of an eccentric,\n |
| 0x16f861 | 46 | but you continue to surprise me. You have my\n |
| 0x16f890 | 15 | deepest thanks. |
| 0x16f8a0 | 20 | ...And my apologies. |
| 0x16f8b5 | 50 | Eh, I decided on my own. Even if you didn't ask,\n |
| 0x16f8e8 | 44 | I'd go help when I saw their wanted posters. |
| 0x16f915 | 51 | I suppose you're just too kindhearted... whatever\n |
| 0x16f949 | 34 | your usual attitude might suggest. |
| 0x16f96c | 43 | In that case, though, Kuon and the others\n |
| 0x16f998 | 11 | shouldn't-- |
| 0x16f9a4 | 14 | What about us? |
| 0x16f9b3 | 45 | Kuon asks with a broad smile, as if there's\n |
| 0x16f9e1 | 23 | nothing to worry about. |
| 0x16f9f9 | 51 | I can't finish my sentence after seeing that look\n |
| 0x16fa2d | 45 | on her face. I scratch my head, trailing off. |
| 0x16fa5b | 14 | Eh. Nevermind. |
| 0x16fa6a | 9 | ...Right. |
| 0x16fa74 | 52 | But even if we succeed, won't they be hunted down?\n |
| 0x16faa9 | 51 | They'd be on the run for the rest of their lives... |
| 0x16fadd | 48 | She's got a point. Even if we help them escape\n |
| 0x16fb0e | 42 | now, it's still just a temporary solution. |
| 0x16fb39 | 50 | Judging from Oshtor's face, none of this is news\n |
| 0x16fb6c | 23 | to him. He nods grimly. |
| 0x16fb84 | 47 | Indeed... Steps have already been taken for a\n |
| 0x16fbb4 | 15 | countermeasure. |
| 0x16fbc4 | 51 | This is the current wanted poster we have prepared. |
| 0x16fbf8 | 48 | Oshtor takes out a piece of paper and hands it\n |
| 0x16fc29 | 8 | forward. |
| 0x16fc32 | 10 | Th-This... |
| 0x16fc3d | 12 | ...Who the-- |
| 0x16fc4a | 53 | The person on the poster... is nothing like Nosuri.\n |
| 0x16fc80 | 42 | She's huge, muscular, and glaring daggers. |
| 0x16fcab | 53 | This... bears little resemblance to my dear sister,\n |
| 0x16fce1 | 7 | if any. |
| 0x16fce9 | 50 | The artist responsible is a subordinate of mine.\n |
| 0x16fd1c | 52 | I may have... embellished her description, somewhat. |
| 0x16fd51 | 51 | Doesn't this mean that you're at the highest risk\n |
| 0x16fd85 | 48 | of all this "high treason" business? Honestly... |
| 0x16fdb6 | 48 | Kuon is clearly exasperated, but Oshtor's only\n |
| 0x16fde7 | 25 | response is a calm smile. |
| 0x16fe01 | 52 | That'll only make her harder to find. She'll still\n |
| 0x16fe36 | 35 | have to live on the run, won't she? |
| 0x16fe5a | 50 | She'd have to get out of the country if she ever\n |
| 0x16fe8d | 17 | wanted any peace. |
| 0x16fe9f | 49 | I might be amenable to such an arrangement, but\n |
| 0x16fed1 | 43 | I'm afraid my dear sister may be less so... |
| 0x16fefd | 49 | Well, it'd make things a lot easier if we could\n |
| 0x16ff2f | 15 | convince her... |
| 0x16ff3f | 46 | For a bandit, she sure seems honest by nature. |
| 0x16ff6e | 51 | In any case, that rules out the option of running\n |
| 0x16ffa2 | 44 | off to somewhere they wouldn't be pursued... |
| 0x16ffcf | 50 | So the best solution wouldn't be running, but to\n |
| 0x170002 | 46 | think of a way to stop the pursuit altogether. |
| 0x170031 | 54 | Good thing the picture doesn't look much like her...\n |
| 0x170068 | 42 | It's almost a completely different person. |
| 0x170093 | 35 | You can barely tell it's a woman.\n |
| 0x1700b7 | 51 | It may as well be a picture of a man, and if they\n |
| 0x1700eb | 18 | arrest the wrong-- |
| 0x1700fe | 25 | ...Now there's a thought. |
| 0x170118 | 50 | It would appear a worthy idea has occurred to you. |
| 0x17014b | 45 | "Worthy" is probably pushing it a little...\n |
| 0x170179 | 34 | It might be more like "desperate"? |
| 0x17019c | 46 | Why don't we just frame someone else for the\n |
| 0x1701cb | 6 | crime? |
| 0x1701d2 | 6 | ...Hm? |
| 0x1701d9 | 51 | Frame...? But who? I hardly imagine we could find\n |
| 0x17020d | 45 | a woman mad enough to accept such punishment. |
| 0x17023b | 16 | No, not a woman. |
| 0x17024c | 6 | A man. |
| 0x170253 | 9 | A... man? |
| 0x17025d | 51 | I'm afraid that strikes me as... rather impossible. |
| 0x170291 | 49 | Under normal circumstances, sure. She's clearly\n |
| 0x1702c3 | 48 | a woman. But how many people actually know that? |
| 0x1702f4 | 11 | That--hm... |
| 0x170300 | 51 | And the portrait, too. Nobody's going to know for\n |
| 0x170334 | 37 | sure whether that's a man or a woman. |
| 0x17035a | 44 | So if we shift the blame, it can be a man.\n |
| 0x170387 | 46 | That would probably be a lot more convenient\n |
| 0x1703b6 | 7 | anyway. |
| 0x1703be | 53 | I see... And who would you have play our scapegoat?\n |
| 0x1703f4 | 45 | I presume you aren't volunteering yourself... |
| 0x170422 | 48 | 'Course not. Believe me, that's the last thing\n |
| 0x170453 | 40 | I want. But I do have someone in mind... |
| 0x170481 | 46 | There was that other group of bandits making\n |
| 0x1704b0 | 44 | trouble in the capital, right? Moznu's gang. |
| 0x1704dd | 22 | You would use them...? |
| 0x1704f4 | 42 | Yeah. They haven't been caught yet, right? |
| 0x17051f | 41 | They should be in prison to begin with.\n |
| 0x170549 | 46 | I kind of feel bad, but we can stick all the\n |
| 0x170578 | 14 | blame on them. |
| 0x170587 | 47 | Even if they deny the charges, who's going to\n |
| 0x1705b7 | 29 | believe a bunch of criminals? |
| 0x1705d5 | 45 | Both Oshtor and Ougi are silent as I finish\n |
| 0x170603 | 15 | my explanation. |
| 0x170613 | 46 | I mean, there's a ton that could go wrong...\n |
| 0x170642 | 49 | Sorry. I'll shut up--just forget I said anything. |
| 0x170674 | 50 | You... have quite the terrifying mind, you know.\n |
| 0x1706a7 | 50 | Framing a hapless third party for high treason...? |
| 0x1706da | 48 | This may well be the first time I've seen true\n |
| 0x17070b | 40 | evil devoid of malice. Marvelous indeed. |
| 0x170734 | 38 | To be honest, it's a little appalling. |
| 0x17075b | 48 | Look, I wasn't really serious. I mean, even if\n |
| 0x17078c | 44 | the picture looks like some buff guy, that\n |
| 0x1707b9 | 9 | doesn't-- |
| 0x1707c3 | 47 | Our good fortune, I suppose, that you did not\n |
| 0x1707f3 | 30 | end up as our enemy. Hmhmhm... |
| 0x170812 | 44 | Despite his words, Ougi's nonchalant smile\n |
| 0x17083f | 8 | remains. |
| 0x170848 | 8 | O-Osht-- |
| 0x170851 | 51 | There's no way Oshtor would agree to a crazy plan\n |
| 0x170885 | 12 | like this... |
| 0x170892 | 48 | I think this scheme of yours should work quite\n |
| 0x1708c3 | 7 | nicely. |
| 0x1708cb | 7 | Wha--!? |
| 0x1708d3 | 33 | I should have expected as much.\n |
| 0x1708f5 | 50 | Such ruthless strategy... It seems Moznu will be\n |
| 0x170928 | 20 | our sacrificed pawn. |
| 0x17093d | 48 | Oshtor's face is grim, but he sounds like he's\n |
| 0x17096e | 25 | already made up his mind. |
| 0x170988 | 21 | Look, that was just-- |
| 0x17099e | 46 | Are you serious? You're going to frame a guy\n |
| 0x1709cd | 43 | for high treason based on this dumb poster? |
| 0x1709f9 | 46 | I guess they ARE criminals, and they've been\n |
| 0x170a28 | 39 | causing trouble for a while now, but... |
| 0x170a50 | 40 | And then I have a wonderful, awful idea. |
| 0x170a79 | 30 | Wait... But that would mean... |
| 0x170a98 | 47 | Y-Yep. Gotta do it for Nosuri. It's kind of a\n |
| 0x170ac8 | 51 | shame, but someone has to take the fall. Ahahaha... |
| 0x170afc | 47 | Splendid. Now, as we appear to have a plan of\n |
| 0x170b2c | 48 | action, I shall report our progress to my dear\n |
| 0x170b5d | 7 | sister. |
| 0x170b65 | 50 | I will begin investigating Moznu and his group's\n |
| 0x170b98 | 18 | possible location. |
| 0x170bab | 44 | Oshtor and Ougi both rise from their seats\n |
| 0x170bd8 | 13 | and head out. |
| 0x170be6 | 50 | Hmhmhm... Looks like things are about to get busy. |
| 0x170c19 | 37 | Kuon eyes me suspiciously as I speak. |
| 0x170c3f | 44 | Haku... I suppose I should ask what you're\n |
| 0x170c6c | 22 | scheming now, exactly? |
| 0x170c83 | 46 | S-Scheming? You wound me! I'm doing all this\n |
| 0x170cb2 | 34 | out of the goodness of my heart.\n |
| 0x170cd5 | 18 | Hahahaha! Aha. Ha. |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_01.json` com a forma:
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
