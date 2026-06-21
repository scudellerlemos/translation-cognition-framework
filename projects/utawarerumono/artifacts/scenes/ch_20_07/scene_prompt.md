# Cena ch_20_07 — pacote de traducao (335 linhas)

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
- **pt-BR MODERNO (registro do jogador de hoje):** preferir a forma que um jogador BR atual usaria, não
  a "correta-mas-arcaica/truncada". Dois erros recorrentes pegos em QA in-game:
  - **Resposta de NOME** (`I'm…`/`My name's…`/`I am…` quando responde "qual seu nome?") → **"Meu nome é…"
    / "Eu me chamo…" / "Sou o(a)…"** conforme a voz. NUNCA "Eu sou" seco — refere-se a estado, soa
    truncado para apresentação.
  - **Léxico arcaico/erudito** (ex.: "ruminar"/"Rumino" por "pensar/refletir") só quando a VOZ do
    personagem pede; senão, a palavra que o público entende **de imediato**.
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
□ pt-BR moderno: forma que um jogador de HOJE usaria? (nome → "Meu nome é/Eu me chamo", não "Eu sou"; sem arcaísmo gratuito)
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
| Cocopo | Criatura | Cocopo | manter_original | none |
| Entua | Personagem | Entua | manter_original | major |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Nakwan | Termo | Nakwan | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `yeah?` -> `tá?` (Ukon, 14_02)
- `after all.` -> `afinal.` (Haku, 11_07)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `U-Understood.` -> `E-Entendi.` (Haku, 16_01)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `No.` -> `Não.` (Protagonista (narração), 18_01)
- `easily.` -> `facilmente.` (Haku, 18_01)
- `Y-Yes...` -> `S-Sim...` (Rulutieh, 15_01)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `Now...` -> `agora...` (Haku, 11_02)
- `behind.` -> `para trás.` (Garota, 13_05)
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Girl` -> `Garota` (sistema, 11_01)
- `Open wide.` -> `Abra bem.` (Garota, 18_01)
- `here...` -> `o fim...` (Haku, 12_03)
- `Yes, ma'am!` -> `Sim!` (Bandido, 13_05)
- `What are you--` -> `O que você está--` (Haku, 20_03)
- `Who exactly are you?` -> `Quem exatamente é você?` (Haku, 19_07)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `for a moment.` -> `por um instante.` (Kuon, 11_02)
- `you...` -> `você...` (Haku, 12_11)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `us.` -> `nós.` (Haku, 15_03)
- `Nakwan` -> `Nakwan` (Personagem-Sistema, 20_06)
- `Uzurushan soldiers` -> `soldados Uzurushan` ([SYSTEM], 20_04)
- `a little more.` -> `um pouco mais.` (Garota, 18_01)
- `OK!` -> `OK!` (Rulutieh, 13_02)
- `That's...` -> `Isso...` (Haku, 15_01)
**Voz estabelecida dos falantes (amostra):**
- Protagonista: `Ngh... ghh...` -> `Nnh... aagh...`
- Protagonista: `Nn...\n` -> `Nnh...\n`
- Protagonista: `It's... warm...?` -> `Está... quente...?`
- Haku: `Urgh...` -> `Argh...`
- Haku: `Right?` -> `né?`
- Haku: `Nn...` -> `Nnh...`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
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
| 0x1c60f5 | 12 | door_01_open |
| 0x1c6103 | 13 | door_01_close |
| 0x1c6111 | 12 | door_02_open |
| 0x1c611e | 13 | door_02_close |
| 0x1c612c | 12 | door_03_open |
| 0x1c6139 | 13 | door_03_close |
| 0x1c6147 | 47 | We close in on the Uzurushan encampment under\n |
| 0x1c6177 | 25 | cover of the morning fog. |
| 0x1c6191 | 45 | Well, it looks like they're all celebrating\n |
| 0x1c61bf | 12 | with drinks. |
| 0x1c61cc | 49 | Probably been tipping it back the entire night,\n |
| 0x1c61fe | 5 | yeah? |
| 0x1c6204 | 48 | The whole night... They're not even pretending\n |
| 0x1c6235 | 23 | to take us seriously... |
| 0x1c624d | 42 | Well, it's far from the front lines, and\n |
| 0x1c6278 | 44 | Uzurusha has the upper hand. They probably\n |
| 0x1c62a5 | 18 | think they've won. |
| 0x1c62b8 | 50 | Looks like the lookouts are enjoying a bottle or\n |
| 0x1c62eb | 42 | two as well. That makes our jobs easier... |
| 0x1c6316 | 30 | So, where are the hostages...? |
| 0x1c6335 | 46 | Over there. They should all be imprisoned in\n |
| 0x1c6364 | 14 | that carriage. |
| 0x1c6373 | 47 | I follow Jachdwalt's pointed finger, seeing a\n |
| 0x1c63a3 | 39 | large boxlike carriage with bars on it. |
| 0x1c63cb | 46 | They've locked all the women and children in\n |
| 0x1c63fa | 20 | there...? How cruel. |
| 0x1c640f | 45 | OK... Now we just stick to the plan. Nosuri\n |
| 0x1c643d | 45 | and Ougi will set fire to their supplies to\n |
| 0x1c646b | 15 | sow some chaos. |
| 0x1c647b | 49 | I'm pretty sure you two can sneak in unnoticed.\n |
| 0x1c64ad | 13 | You got this? |
| 0x1c64bb | 40 | Hm. As a good woman, I am dutybound to\n |
| 0x1c64e4 | 29 | exceed all your expectations. |
| 0x1c6502 | 50 | Such work fits neatly into our usual repertoire,\n |
| 0x1c6535 | 10 | after all. |
| 0x1c6540 | 44 | Me and the other guys use the chaos to our\n |
| 0x1c656d | 45 | advantage and free everyone, taking out any\n |
| 0x1c659b | 18 | guards in the way. |
| 0x1c65ae | 50 | Don't forget that the enemies are all around us.\n |
| 0x1c65e1 | 49 | Confused or not, if we slip up, they'll kill us\n |
| 0x1c6613 | 4 | all. |
| 0x1c6618 | 13 | U-Understood. |
| 0x1c6626 | 47 | Uruuru, Saraana, and Atuy will cut the saddle\n |
| 0x1c6656 | 46 | straps to slow them down in case they try to\n |
| 0x1c6685 | 9 | chase us. |
| 0x1c668f | 11 | Understood. |
| 0x1c669b | 44 | Oh, love? I'd much rather be where all the\n |
| 0x1c66c8 | 12 | action is... |
| 0x1c66d5 | 3 | No. |
| 0x1c66d9 | 9 | Please... |
| 0x1c66e3 | 13 | Pleeeaaase... |
| 0x1c66f1 | 10 | I said no! |
| 0x1c66fc | 45 | An utter, terrible, beastly spoilsport, love. |
| 0x1c672a | 49 | Yeah, and you rampaging around is just going to\n |
| 0x1c675c | 18 | make things worse. |
| 0x1c676f | 46 | Uruuru and Saraana, go with Atuy, and if you\n |
| 0x1c679e | 44 | encounter the enemy, take them out silently. |
| 0x1c67cb | 14 | Can you do it? |
| 0x1c67da | 7 | Easily. |
| 0x1c67e2 | 26 | Simplicity itself, Master. |
| 0x1c67fd | 44 | Kuon, Nekone, and Rulutieh will stay here.\n |
| 0x1c682a | 46 | Wait for the chaos, then have Cocopo tow the\n |
| 0x1c6859 | 14 | carriage away. |
| 0x1c6868 | 8 | Y-Yes... |
| 0x1c6871 | 29 | ...I'm counting on you, Kuon. |
| 0x1c688f | 48 | Mhm. You have nothing to worry about, I think.\n |
| 0x1c68c0 | 17 | Be careful, Haku. |
| 0x1c68d2 | 13 | Can I go now? |
| 0x1c68e0 | 8 | Not yet. |
| 0x1c68e9 | 44 | Nosuri and Ougi are infiltrating the base.\n |
| 0x1c6916 | 40 | Like it or not, it'll begin soon enough. |
| 0x1c693f | 46 | And Atuy, your job is just to cut the saddle\n |
| 0x1c696e | 47 | straps to slow down their pursuit. You hear me? |
| 0x1c699e | 47 | No problem! I won't be a moment. And it'll be\n |
| 0x1c69ce | 50 | all right if just ONE guard ends up accidentally\n |
| 0x1c6a01 | 8 | stabbed. |
| 0x1c6a0a | 29 | No accidental stabbing. Ever. |
| 0x1c6a28 | 26 | Wait... Where is she...?\n |
| 0x1c6a43 | 22 | Why isn't she here...? |
| 0x1c6a5a | 39 | What's the matter? It's about to start. |
| 0x1c6a82 | 43 | My girl... I don't see her in the carriage. |
| 0x1c6aae | 8 | ...What? |
| 0x1c6ab7 | 40 | Just... can't see her anywhere, yeah...? |
| 0x1c6ae0 | 47 | What do we do...? We can't stop the operation\n |
| 0x1c6b10 | 6 | now... |
| 0x1c6b17 | 46 | ...Sorry, boss, but I'm gonna have to leave.\n |
| 0x1c6b46 | 21 | I gotta find my girl. |
| 0x1c6b5c | 49 | Hey, wait! You're going to ruin the plan if you\n |
| 0x1c6b8e | 19 | go off on your own! |
| 0x1c6ba2 | 48 | Look, I'm real sorry, but if I can't save her,\n |
| 0x1c6bd3 | 48 | none of this means a damn thing. Just leave me\n |
| 0x1c6c04 | 7 | behind. |
| 0x1c6c0c | 45 | Jachdwalt dashes off, his expression frantic. |
| 0x1c6c3a | 34 | Argh... What am I supposed to...\n |
| 0x1c6c5d | 29 | No, there's no time to think. |
| 0x1c6c7b | 35 | Kiwru, I'm going after Jachdwalt.\n |
| 0x1c6c9f | 40 | You're in charge now. Stick to the plan. |
| 0x1c6cc8 | 24 | Wh-What!? Wait, that's-- |
| 0x1c6ce1 | 47 | I stay low to the ground as I stealthily tail\n |
| 0x1c6d11 | 10 | Jachdwalt. |
| 0x1c6d1c | 48 | Hold it, Jachdwalt! Do you even know where she\n |
| 0x1c6d4d | 45 | might be? You're not just gonna ransack the\n |
| 0x1c6d7b | 8 | camp...? |
| 0x1c6d84 | 39 | There's one place she might be, yeah?\n |
| 0x1c6dac | 34 | I just gotta check that one place. |
| 0x1c6dcf | 47 | Jachdwalt dashes towards a tent with a unique\n |
| 0x1c6dff | 45 | crest, a little ways from the center of the\n |
| 0x1c6e2d | 11 | encampment. |
| 0x1c6e39 | 46 | You've gotta be kidding me. That's clearly a\n |
| 0x1c6e68 | 29 | tent for someone in charge... |
| 0x1c6e86 | 47 | Why would she be here? Or is she being forced\n |
| 0x1c6eb6 | 44 | to...? No, can't jump to conclusions. More\n |
| 0x1c6ee3 | 14 | importantly... |
| 0x1c6ef2 | 17 | Uzurushan soldier |
| 0x1c6f04 | 4 | Wh-- |
| 0x1c6f09 | 7 | Hah...! |
| 0x1c6f11 | 45 | Jachdwalt cuts the guard down with a single\n |
| 0x1c6f3f | 35 | strike, and rushes toward the tent. |
| 0x1c6f63 | 46 | What kind of girl would make a guy like this\n |
| 0x1c6f92 | 18 | so crazy over her? |
| 0x1c6fa5 | 48 | Jachdwalt's peering inside through the gaps of\n |
| 0x1c6fd6 | 45 | the tent's canvas. I follow suit and peer in. |
| 0x1c7004 | 4 | Girl |
| 0x1c7009 | 10 | Open wide. |
| 0x1c7014 | 11 | Small child |
| 0x1c7020 | 23 | Ahhhh... *homf* *munch* |
| 0x1c7038 | 15 | Do you like it? |
| 0x1c7048 | 18 | Yeah, it's delish! |
| 0x1c705b | 50 | Really? Haha, I'm glad to hear it. Eat up now...\n |
| 0x1c708e | 35 | You need to eat a hearty breakfast. |
| 0x1c70b2 | 49 | I see a girl and a small child having breakfast\n |
| 0x1c70e4 | 7 | inside. |
| 0x1c70ec | 42 | ...Uhh...? Not quite what I was expecting. |
| 0x1c7117 | 47 | Jachdwalt, is that the girl you're looking for? |
| 0x1c7147 | 30 | Yeah. Looks like she's safe.\n |
| 0x1c7166 | 17 | But why is she... |
| 0x1c7178 | 48 | Jachdwalt gives a sigh of relief, but he looks\n |
| 0x1c71a9 | 26 | almost as baffled as I am. |
| 0x1c71c4 | 28 | Here we go again. Open wide. |
| 0x1c71e1 | 32 | Ahhhh, *munch* *munch* *munch*\n |
| 0x1c7202 | 10 | ...Delish! |
| 0x1c720d | 7 | Haha... |
| 0x1c7215 | 46 | But it would've been more delish if Dad were\n |
| 0x1c7244 | 7 | here... |
| 0x1c724c | 50 | Oh... He will be back soon, so be sure to behave\n |
| 0x1c727f | 24 | yourself until then. OK? |
| 0x1c7298 | 26 | OK. I'll be good and wait. |
| 0x1c72b3 | 48 | The girl wipes the child's face with a napkin,\n |
| 0x1c72e4 | 46 | gently removing errant food. They seem happy\n |
| 0x1c7313 | 9 | together. |
| 0x1c731d | 49 | ...Oh crap. Jachdwalt, we're running out of time. |
| 0x1c734f | 45 | Right, almost forgot. We need to hurry, yeah? |
| 0x1c737d | 25 | Hey, something's on fire. |
| 0x1c7397 | 15 | Fire...! Fire!! |
| 0x1c73a7 | 24 | Dammit, there it goes... |
| 0x1c73c0 | 23 | Is it an enemy attack!? |
| 0x1c73d8 | 42 | I don't know, but we have to put it out!\n |
| 0x1c7403 | 12 | Bring water! |
| 0x1c7410 | 50 | Plumes of smoke begin to rise, and chaos spreads\n |
| 0x1c7443 | 28 | across the camp, bit by bit. |
| 0x1c7460 | 30 | A fire? Is it an enemy attack? |
| 0x1c747f | 47 | The girl notices the ruckus going on, and she\n |
| 0x1c74af | 41 | holds the child close as she looks about. |
| 0x1c74d9 | 51 | Shinonon, I am going to go see what has happened.\n |
| 0x1c750d | 22 | Be good and stay here. |
| 0x1c7524 | 21 | Got it. I'll be good. |
| 0x1c753a | 19 | That's a good girl. |
| 0x1c754e | 48 | The girl peeks through the tent's entryway and\n |
| 0x1c757f | 33 | looks hesitantly around the area. |
| 0x1c75a1 | 50 | She seems to notice that the guards are missing,\n |
| 0x1c75d4 | 37 | and begins to hurry towards the fire. |
| 0x1c75fa | 19 | Hey, she's leaving. |
| 0x1c760e | 23 | Yeah, now's our chance! |
| 0x1c7626 | 45 | Jachdwalt hurries into the tent and runs to\n |
| 0x1c7654 | 17 | the child's side. |
| 0x1c7666 | 21 | Oh, Dad! You're back. |
| 0x1c767c | 28 | That's right. You been good? |
| 0x1c7699 | 20 | 'Course I been good! |
| 0x1c76ae | 47 | The child's speech patterns are oddly similar\n |
| 0x1c76de | 39 | to his. She seems to be in a good mood. |
| 0x1c7706 | 32 | We're gonna make a run for it.\n |
| 0x1c7727 | 16 | Hold tight, now. |
| 0x1c7738 | 27 | Got it! I ain't letting go! |
| 0x1c7754 | 46 | The child clambers onto Jachdwalt and clings\n |
| 0x1c7783 | 24 | to his clothes, beaming. |
| 0x1c779c | 26 | Time to make tracks, boss. |
| 0x1c77b7 | 35 | Huh? W-Wait, what about your girl-- |
| 0x1c77db | 32 | Fine, I guess I'll go get her... |
| 0x1c77fc | 49 | I exit the tent and look around, ducking behind\n |
| 0x1c782e | 25 | whatever I can for cover. |
| 0x1c7848 | 43 | Extinguish the fire! All others, move the\n |
| 0x1c7874 | 46 | supplies away! We cannot lose a single grain\n |
| 0x1c78a3 | 8 | of amam! |
| 0x1c78ac | 11 | Yes, ma'am! |
| 0x1c78b8 | 48 | That's her voice... It's coming from over there. |
| 0x1c78e9 | 42 | How could this happen...? I cannot be so\n |
| 0x1c7914 | 34 | careless. A change must be made... |
| 0x1c7937 | 37 | I will have to be more strict about-- |
| 0x1c795d | 40 | There she is...! And... nobody around.\n |
| 0x1c7986 | 16 | Now's my chance! |
| 0x1c7997 | 43 | I check to make sure nobody's around, and\n |
| 0x1c79c3 | 40 | grab the girl's hand as I lead her away. |
| 0x1c79ec | 26 | Wha--!? Wh-Who are you!?\n |
| 0x1c7a07 | 14 | What are you-- |
| 0x1c7a16 | 33 | We're here to help. Keep running! |
| 0x1c7a38 | 30 | Come to help? What do you...\n |
| 0x1c7a57 | 20 | Who exactly are you? |
| 0x1c7a6c | 45 | I'll explain later. Anyway, we need to hurry! |
| 0x1c7a9a | 48 | A-All right, but could you please stop pulling\n |
| 0x1c7acb | 14 | me so hard...? |
| 0x1c7ada | 48 | With those words, the girl's wariness seems to\n |
| 0x1c7b0b | 35 | fade, and she follows close behind. |
| 0x1c7b2f | 50 | Luckily, none of the barbarian soldiers spot us.\n |
| 0x1c7b62 | 46 | I manage to catch up with Kiwru and Jachdwalt. |
| 0x1c7b91 | 25 | Haku! Are you all right!? |
| 0x1c7bab | 24 | Yeah, I managed somehow. |
| 0x1c7bc4 | 50 | Hey, Jachdwalt. What's wrong with you!? I wasn't\n |
| 0x1c7bf7 | 40 | expecting you to leave your girl behind! |
| 0x1c7c20 | 49 | What are you talkin...What the--Boss, why'd you\n |
| 0x1c7c52 | 20 | bring HER with you!? |
| 0x1c7c67 | 4 | Huh? |
| 0x1c7c6c | 43 | You're... Jachdwalt!? Then that must mean-- |
| 0x1c7c98 | 49 | The girl glares at me and slaps my hand off hers. |
| 0x1c7cca | 20 | Gah!? What are you-- |
| 0x1c7cdf | 46 | She's THEIR boss! Dammit, I went through all\n |
| 0x1c7d0e | 46 | that to grab Shinonon without bein' noticed.\n |
| 0x1c7d3d | 26 | Why'd you bring her here!? |
| 0x1c7d58 | 42 | Hold on a sec. When you say your girl...\n |
| 0x1c7d83 | 22 | do you mean that kid!? |
| 0x1c7d9a | 41 | Best little girl in the whole wide world. |
| 0x1c7dc4 | 49 | Could we PLEASE clarify these things beforehand!? |
| 0x1c7df6 | 47 | Wh-What are we going to do!? If she calls for\n |
| 0x1c7e26 | 38 | help, we'll be completely outnumbered! |
| 0x1c7e4d | 47 | Kiwru doesn't really handle sudden changes of\n |
| 0x1c7e7d | 15 | plan well, huh? |
| 0x1c7e8d | 29 | But he does have a point...\n |
| 0x1c7eab | 24 | If she calls for help... |
| 0x1c7ec8 | 7 | ...Huh? |
| 0x1c7ed0 | 37 | However, the girl doesn't call out.\n |
| 0x1c7ef6 | 47 | She just gazes sadly at Jachdwalt and the kid\n |
| 0x1c7f26 | 13 | for a moment. |
| 0x1c7f34 | 17 | ...You should go. |
| 0x1c7f46 | 6 | You... |
| 0x1c7f4d | 22 | Be good now, Shinonon. |
| 0x1c7f64 | 9 | ...Entua? |
| 0x1c7f6e | 26 | You're going to let us go? |
| 0x1c7f89 | 23 | *Stomp* *stomp* *stomp* |
| 0x1c7fa1 | 27 | Lady Entua! Where are you!? |
| 0x1c7fbd | 46 | Hm!? Is that the enemy!? Lady Entua, are you\n |
| 0x1c7fec | 10 | unharmed!? |
| 0x1c7ff7 | 44 | It seems these men were searching for her.\n |
| 0x1c8024 | 46 | Multiple Uzurushan soldiers appear behind her. |
| 0x1c8053 | 22 | Nngh...! Draw steel!\n |
| 0x1c806a | 28 | Our enemy stands before you! |
| 0x1c8087 | 49 | The girl Shinonon called Entua has a conflicted\n |
| 0x1c80b9 | 49 | expression for a moment, but her command is firm. |
| 0x1c80eb | 33 | So this fire was their doing...\n |
| 0x1c810d | 34 | It's the enemy! The enemy is here! |
| 0x1c8130 | 51 | The barbarians handling the fire begin gathering,\n |
| 0x1c8164 | 44 | too. We have to buy time for the others to\n |
| 0x1c8191 | 9 | escape... |
| 0x1c819b | 22 | Entua, fighting's bad. |
| 0x1c81b2 | 41 | ...Surround them. Do not let them escape. |
| 0x1c81dc | 51 | Understood...! How dare you make a mockery of us!\n |
| 0x1c8210 | 29 | I'll gut you where you stand! |
| 0x1c822e | 31 | No. There will be no killing.\n |
| 0x1c824e | 27 | They are to be taken alive. |
| 0x1c826a | 7 | Wha--!? |
| 0x1c8272 | 44 | We must question them for information first! |
| 0x1c829f | 16 | ...U-Understood. |
| 0x1c82b0 | 50 | The barbarians take action, circling to surround\n |
| 0x1c82e3 | 3 | us. |
| 0x1c82e7 | 48 | Just then, the nakwans appear, keeping us from\n |
| 0x1c8318 | 23 | being fully surrounded. |
| 0x1c8330 | 6 | Nakwan |
| 0x1c8337 | 19 | You shall not pass! |
| 0x1c834b | 48 | We will not let you lay a single finger on our\n |
| 0x1c837c | 8 | saviors! |
| 0x1c8385 | 32 | Haku, we shall keep them at bay! |
| 0x1c83a6 | 29 | We leave the rest to you...\n |
| 0x1c83c4 | 31 | Please, save my wife and child! |
| 0x1c83e4 | 43 | Don't be stupid! We need to run, not fight! |
| 0x1c8410 | 47 | Haku, we're not going to last much longer here! |
| 0x1c8440 | 35 | Not good. I messed up big time...\n |
| 0x1c8464 | 24 | This could get real bad. |
| 0x1c847d | 18 | Uzurushan soldiers |
| 0x1c8490 | 13 | Gwaaaaaaghh!! |
| 0x1c849e | 21 | Wh-What is going on!? |
| 0x1c84b4 | 14 | A little more. |
| 0x1c84c3 | 35 | We apologize for the delay, Master. |
| 0x1c84e7 | 12 | You're here! |
| 0x1c84f4 | 5 | Guh!? |
| 0x1c84fa | 12 | Ahahahahaha! |
| 0x1c8507 | 47 | Oh, love, that's just no fair! You went ahead\n |
| 0x1c8537 | 35 | and started all the fun without me. |
| 0x1c855b | 44 | Atuy...! For once, you're not just here to\n |
| 0x1c8588 | 38 | complicate things. You're a lifesaver! |
| 0x1c85af | 9 | Obj_Arrow |
| 0x1c85b9 | 50 | Hmph! Kept you waiting? It seems you're hopeless\n |
| 0x1c85ec | 28 | without me around, as usual. |
| 0x1c8609 | 45 | Truly, there is never a dull moment in your\n |
| 0x1c8637 | 7 | employ. |
| 0x1c8659 | 12 | Sir Haku...! |
| 0x1c8666 | 24 | Did we keep you waiting? |
| 0x1c867f | 23 | Everything is in place. |
| 0x1c8697 | 31 | Damn right you kept me waiting! |
| 0x1c86b7 | 21 | Enemy reinforcements! |
| 0x1c86cd | 15 | L-Lady Entua... |
| 0x1c86dd | 44 | D-Do not falter! Their numbers have barely\n |
| 0x1c870a | 49 | increased! Show your pride as Uzurushan mononofu! |
| 0x1c873c | 12 | Y-Yes ma'am! |
| 0x1c8749 | 28 | Hold on tight now, Shinonon. |
| 0x1c8766 | 48 | Dad... are you going to go away like Father did? |
| 0x1c8797 | 45 | Don't you worry, now. I ain't goin' anywhere. |
| 0x1c87c5 | 3 | OK! |
| 0x1c87c9 | 23 | All right, let's do it! |
| 0x1c89df | 77 | A {c5}Combat Tutorial{c-1} has been added to the Glossary in the system menu. |
| 0x1c8c78 | 12 | H-Heeeeelp!! |
| 0x1c8c85 | 9 | That's... |
| 0x1c8c8f | 40 | We asked her to act the part of hostage. |
| 0x1c8cb8 | 50 | The idea behind this trial is to save the damsel\n |
| 0x1c8ceb | 48 | in distress, and become more dashing and heroic. |
| 0x1c8d1c | 49 | At least this one seems normal, compared to the\n |
| 0x1c8d4e | 5 | rest. |
| 0x1c8d54 | 51 | Then again, something tells me this might be more\n |
| 0x1c8d88 | 45 | than it appears... Eh, maybe I'm just being\n |
| 0x1c8db6 | 12 | pessimistic. |
| 0x1c8fe1 | 48 | Thank you for saving me. I shall remember your\n |
| 0x1c9012 | 29 | kindness and bravery forever. |
| 0x1c9030 | 44 | Hey, don't worry about it. I really didn't\n |
| 0x1c905d | 25 | do much anyways, ahaha... |
| 0x1c9077 | 32 | ...Um, was that suitable enough? |
| 0x1c9098 | 42 | Well done. Thank you for your cooperation. |
| 0x1c90c3 | 42 | This will be your reward for today's work. |
| 0x1c90ee | 28 | W-Wow, this much? Thank you! |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_07.json` com a forma:
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
