# Cena ch_22_05 — pacote de traducao (589 linhas)

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
| Aruruu | Personagem | Aruruu | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Camyu | Personagem | Camyu | manter_original | moderate |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Cloister | Local | Claustro Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `asleep.` -> `adormecido.` (Narrador (Haku - 1ª pessoa), 19_08)
- `I think.` -> `acho.` (Kuon, 12_11)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Mhm.` -> `Hum.` (Protagonista, 22_04)
- `the capital?` -> `a capital?` (Ukon, 12_04)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `well.` -> `bem.` (Kuon, 11_02)
- `Hmhm.` -> `Hmhm.` (Moznu, 13_05)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `*THUD*` -> `*BAQUE*` (Kuon, 11_02)
- `inside.` -> `café.` (Haku, 20_07)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `of me.` -> `de mim.` (Nosuri, 18_01)
- `That's...` -> `Isso...` (Haku, 15_01)
- `you know?` -> `sabe?` (Haku, 14_08)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `then.` -> `então.` (Kuon, 13_01)
- `this...?` -> `isto...?` (Haku, 18_01)
- `her...` -> `dela...` (Nekone, 18_01)
- `same.` -> `igual.` (Haku, 15_05)
- `for her.` -> `pra ela.` (Haku, 15_03)
- `it...` -> `isso...` (Haku, 18_01)
- `the imperial capital.` -> `a capital imperial.` (Haku, 17_01)
- `doing.` -> `fazendo.` (Jachdwalt, 21_05)
- `me.` -> `mim.` (Garota, 17_01)
- `entertainment.` -> `entretenimento.` (Raiko, 20_17)
- `back...` -> `de lá...` (Haku, 14_04)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `I... see.` -> `Eu... entendo.` (Haku, 19_08)
- `M-Miss Atuy...` -> `S-Senhora Atuy...` (Rulutieh, 19_08)
- `ruins.` -> `ruínas.` (Haku, 21_01)
- `too.` -> `também.` (Garota, 17_01)
- `again.` -> `vez.` (Ougi, 13_05)
- `stuff.` -> `isso.` (Haku, 14_04)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `Haku...` -> `Haku...` (Kuon, 11_02)
- `head.` -> `cabeça.` (Haku, 18_01)
- `dear sister.` -> `querida irmã.` (Nekone, 14_10)
- `Haku!` -> `Haku!` (Kuon, 12_11)
- `them.` -> `deles.` (Kuon, 11_05)
- `Really...?` -> `Sério...?` (Rulutieh, 14_10)
- `anymore.` -> `mais.` (Man, 11_01)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `Me...?` -> `Eu...?` (Protagonista, 11_01)
- `more...` -> `mais...` (Haku, 22_04)
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
| 0x246d13 | 9 | *Yawn*... |
| 0x246d1d | 44 | I try to stifle a yawn as I scratch my side. |
| 0x246d4a | 46 | Huh... I was just planning on lying down for\n |
| 0x246d79 | 45 | a bit after eating, but I guess I just fell\n |
| 0x246da7 | 7 | asleep. |
| 0x246daf | 45 | Guess I've been pretty busy with keeping an\n |
| 0x246ddd | 43 | eye on those Tuskur ambassadors for Oshtor. |
| 0x246e09 | 47 | This morning seems more peaceful than most...\n |
| 0x246e39 | 48 | Well, judging by the sun's height, it's almost\n |
| 0x246e6a | 5 | noon. |
| 0x246e70 | 49 | If I remember right, the Tuskur folks have some\n |
| 0x246ea2 | 43 | meeting with court officials, and then an\n |
| 0x246ece | 11 | inspection? |
| 0x246eda | 42 | Sounded like Uruuru and Saraana had some\n |
| 0x246f05 | 45 | related business, so I have some alone time\n |
| 0x246f33 | 13 | for a change. |
| 0x246f41 | 48 | Thanks to that, for once, I have nothing to do\n |
| 0x246f72 | 17 | but take it easy. |
| 0x246f84 | 46 | Yamato seems pretty anxious about this whole\n |
| 0x246fb3 | 42 | thing, but the Tuskur guests are totally\n |
| 0x246fde | 10 | unruffled. |
| 0x246fe9 | 45 | My mind drifts to the Tuskur ambassadors...\n |
| 0x247017 | 45 | to the two gorgeous women as I leave my room. |
| 0x247045 | 47 | Felt like they came more for sightseeing than\n |
| 0x247075 | 10 | diplomacy. |
| 0x247080 | 46 | They say neighboring countries are your most\n |
| 0x2470af | 43 | likely enemies, but if they have ulterior\n |
| 0x2470db | 22 | motives, I can't tell. |
| 0x2470f2 | 46 | Of course, worrying about that kind of stuff\n |
| 0x247121 | 33 | is up to the bigwigs. Not my job. |
| 0x247143 | 46 | More importantly, I should figure out how to\n |
| 0x247172 | 17 | spend my day off. |
| 0x247184 | 44 | Guess I'll take a bath first, maybe have a\n |
| 0x2471b1 | 19 | drink with lunch... |
| 0x2471c5 | 45 | Or maybe it'd be better to meet up with the\n |
| 0x2471f3 | 20 | owner of this place. |
| 0x247208 | 46 | I start making my way towards the bath while\n |
| 0x247237 | 8 | I think. |
| 0x247240 | 11 | Excuse me!! |
| 0x24724c | 6 | Scuse. |
| 0x247253 | 7 | ...Huh? |
| 0x24725b | 44 | Just as I walk past the front door, a very\n |
| 0x247288 | 40 | energetic voice echoes through the hall. |
| 0x2472b1 | 48 | I turn around to find those two beautiful-yet-\n |
| 0x2472e2 | 41 | disappointing... I mean, the two Tuskur\n |
| 0x24730c | 12 | ambassadors. |
| 0x247319 | 34 | Good morning, Haku! We meet again. |
| 0x24733c | 32 | Hey you. We've come to hang out. |
| 0x24735d | 40 | ...What the hell are you two doing here? |
| 0x247386 | 38 | Well, we came to have some fun, silly! |
| 0x2473ad | 4 | Mhm. |
| 0x2473b2 | 48 | ...Aren't you supposed to be in some important\n |
| 0x2473e3 | 24 | meeting with our people? |
| 0x2473fc | 45 | Well, it seemed kinda boring, so we decided\n |
| 0x24742a | 21 | to come here instead! |
| 0x247440 | 39 | Their nonchalance leaves me speechless. |
| 0x247468 | 43 | You ditched the meeting because of that...? |
| 0x247494 | 46 | It should be fine, right? I mean, we came in\n |
| 0x2474c3 | 42 | the first place so we could all get along. |
| 0x2474ee | 48 | Don't you think skipping that meeting would be\n |
| 0x24751f | 47 | counterproductive for what you came here to do? |
| 0x24754f | 37 | How the hell are they ambassadors!?\n |
| 0x247575 | 47 | Is this a joke? How does Tuskur function with\n |
| 0x2475a5 | 26 | people like this in power? |
| 0x2475c0 | 40 | It's fine! We left doubles in our place. |
| 0x2475e9 | 43 | Cammie's ability to leave body doubles is\n |
| 0x247615 | 20 | unmatched in Tuskur. |
| 0x24762a | 18 | Mhm! That's right! |
| 0x24763d | 48 | It's an amazing doll. It responds to questions\n |
| 0x24766e | 37 | and can even do lots of little tasks. |
| 0x247694 | 45 | Even Munto would say "If we have this, then\n |
| 0x2476c2 | 44 | there's no need to keep you here, princess." |
| 0x2476ef | 45 | He even praised me! He said, "You must have\n |
| 0x24771d | 46 | gone through quite the effort to manage this." |
| 0x24774c | 43 | I'm pretty damn sure that would come from\n |
| 0x247778 | 24 | exasperation, not pride. |
| 0x247791 | 48 | And besides, I'd rather see the people of this\n |
| 0x2477c2 | 44 | nation with my own eyes than sit around in\n |
| 0x2477ef | 9 | meetings. |
| 0x2477f9 | 45 | ...So am I going to have to show you around\n |
| 0x247827 | 12 | the capital? |
| 0x247834 | 31 | No wonder you're Ku's favorite! |
| 0x247854 | 48 | So they'd rather see the people than get stuck\n |
| 0x247885 | 30 | in talks with the officials... |
| 0x2478a4 | 47 | I should probably report this to Oshtor, just\n |
| 0x2478d4 | 8 | in case. |
| 0x2478dd | 31 | So could you go find Ku for us? |
| 0x2478fd | 46 | Oh well. I guess I'm not the one that has to\n |
| 0x24792c | 20 | be their tour guide. |
| 0x247941 | 20 | Sure. Hold on a bit. |
| 0x247956 | 39 | Oh... um. Could you wait just a moment? |
| 0x24797e | 3 | Hm? |
| 0x247982 | 44 | Do you think it's OK? Ku didn't look happy\n |
| 0x2479af | 48 | to see us. She looked pretty grumpy last time... |
| 0x2479e0 | 19 | Oh, so you noticed. |
| 0x2479f4 | 36 | She's been so cold to us recently.\n |
| 0x247a19 | 36 | Do you think she doesn't like us...? |
| 0x247a3e | 47 | Do you think she's annoyed with us for trying\n |
| 0x247a6e | 46 | to follow her around when she doesn't like us? |
| 0x247a9d | 50 | I wouldn't say she doesn't like you... More like\n |
| 0x247ad0 | 44 | she doesn't know how to act in front of you. |
| 0x247afd | 46 | At a certain age, it's awkward for anyone to\n |
| 0x247b2c | 43 | talk to an older sibling who knows you so\n |
| 0x247b58 | 5 | well. |
| 0x247b62 | 49 | And if she really didn't like you, she wouldn't\n |
| 0x247b94 | 49 | have been doing the happy tail wag thing, would\n |
| 0x247bc6 | 4 | she? |
| 0x247bcb | 50 | Y-Yeah. You're right. I'm sure she still likes us! |
| 0x247bfe | 5 | Hmhm. |
| 0x247c04 | 48 | Although she was almost in tears by the end of\n |
| 0x247c35 | 42 | last time. I'd say she's pretty close to\n |
| 0x247c60 | 11 | hating you. |
| 0x247c6c | 7 | Wha--!? |
| 0x247c74 | 31 | Huh!? Aru, this guy's so mean!! |
| 0x247c94 | 15 | Kuon, you here? |
| 0x247ca4 | 43 | You've got guests. Are you really not here? |
| 0x247cd0 | 5 | Kuon? |
| 0x247cd6 | 10 | No answer. |
| 0x247ce1 | 6 | *Thud* |
| 0x247ce8 | 36 | But it sounds like someone's inside. |
| 0x247d0d | 17 | ...I'm coming in. |
| 0x247d1f | 50 | When I enter the room, I see a mound of blankets\n |
| 0x247d52 | 11 | on her bed. |
| 0x247d5e | 24 | Kuon, you've got guests. |
| 0x247d77 | 44 | I speak to the clump of linens. There's no\n |
| 0x247da4 | 47 | reply at first, but I hear a tired voice from\n |
| 0x247dd4 | 7 | inside. |
| 0x247ddc | 46 | ...Tell them that I am running some errands,\n |
| 0x247e0b | 26 | and am not currently here. |
| 0x247e26 | 42 | So you want me to tell them you said that? |
| 0x247e51 | 44 | I crouch down near the lump, and peer into\n |
| 0x247e7e | 17 | the blanket nest. |
| 0x247e90 | 48 | Kuon looks like a turtle in its shell, but she\n |
| 0x247ec1 | 47 | finally gives up and peeks out of the blankets. |
| 0x247ef1 | 26 | It's my sisters, isn't it? |
| 0x247f0c | 21 | Yep. The dynamic duo. |
| 0x247f22 | 46 | Why would they come NOW? I thought they were\n |
| 0x247f51 | 28 | supposed to be at a meeting. |
| 0x247f6e | 47 | I'm sure you would understand the reason much\n |
| 0x247f9e | 27 | better than I would, right? |
| 0x247fba | 7 | Urgh... |
| 0x247fc2 | 43 | Kuon slowly disentangles herself from the\n |
| 0x247fee | 8 | bedding. |
| 0x247ff7 | 39 | Those two never consider my feelings... |
| 0x24801f | 31 | You angry at them or something? |
| 0x24803f | 45 | I-I suppose I wouldn't say I'm angry at them. |
| 0x24806d | 45 | I just... don't know how to act in front of\n |
| 0x24809b | 7 | them... |
| 0x2480a3 | 46 | You were on the verge of tears last time you\n |
| 0x2480d2 | 18 | were all together. |
| 0x2480e5 | 50 | She seems a little grumpy, but at the same time,\n |
| 0x248118 | 38 | there's a hint of bashfulness as well. |
| 0x24813f | 45 | If you really don't want to see them, I can\n |
| 0x24816d | 44 | come up with some kind of excuse for them.\n |
| 0x24819a | 14 | What'll it be? |
| 0x2481a9 | 52 | I-I'm not saying... I... don't want to see them...\n |
| 0x2481de | 12 | It's just... |
| 0x2481eb | 13 | It's just...? |
| 0x2481f9 | 30 | Kuon blushes as she continues. |
| 0x248218 | 42 | I just don't know what to do about them.\n |
| 0x248243 | 26 | They're... overprotective. |
| 0x24825e | 20 | Overprotective, huh. |
| 0x248273 | 49 | Yes. My sisters are just far too overprotective\n |
| 0x2482a5 | 6 | of me. |
| 0x2482ac | 44 | Kuon shuffles closer, as though she's been\n |
| 0x2482d9 | 41 | waiting for a chance to let all this out. |
| 0x248303 | 49 | They have opinions on everything I do, they ask\n |
| 0x248335 | 46 | if I need to use the restroom before bed--at\n |
| 0x248364 | 11 | THIS age... |
| 0x248370 | 51 | They tell me I have to study, or that I shouldn't\n |
| 0x2483a4 | 39 | explore ruins because it's "dangerous." |
| 0x2483cc | 46 | Of course, I'm not ungrateful to my sisters.\n |
| 0x2483fb | 49 | They've treated me like family ever since I was\n |
| 0x24842d | 6 | young. |
| 0x248434 | 28 | But I'm not a child anymore. |
| 0x248451 | 41 | So does that mean you want them to leave? |
| 0x24847b | 9 | That's... |
| 0x248485 | 46 | For a moment, Kuon seems to be at a loss for\n |
| 0x2484b4 | 6 | words. |
| 0x2484bb | 49 | But as soon as she notices my gaze, she quickly\n |
| 0x2484ed | 11 | turns away. |
| 0x2484f9 | 44 | Y-Yes. Have them leave. Tell them I'm away\n |
| 0x248526 | 10 | right now. |
| 0x248531 | 46 | You sure? They came all this way to see you,\n |
| 0x248560 | 9 | you know? |
| 0x24856a | 47 | Yes, it's fine! Go on and tell them my message. |
| 0x24859a | 47 | Well, as long as you're OK with that, I'll go\n |
| 0x2485ca | 10 | tell them. |
| 0x2485d5 | 6 | ...Hm? |
| 0x2485dc | 26 | Where'd those two go...?\n |
| 0x2485f7 | 15 | Did they leave? |
| 0x248607 | 16 | Is that... true? |
| 0x248618 | 49 | It's hard to believe Kuon was such a cutie back\n |
| 0x24864a | 5 | then. |
| 0x248650 | 50 | I wasn't expecting that. I saw Kuon as a prodigy\n |
| 0x248683 | 48 | who'd master anything. But she has a side like\n |
| 0x2486b4 | 8 | this...? |
| 0x2486bd | 29 | Yep, Ku's a real hard worker. |
| 0x2486db | 48 | She'd cry when her lessons didn't go well, but\n |
| 0x24870c | 49 | each time it made her try harder. It was so cute! |
| 0x24873e | 48 | I never knew my dear sister had such a side to\n |
| 0x24876f | 6 | her... |
| 0x248776 | 47 | Oh, I'm not shattering your image of her, am I? |
| 0x2487a6 | 47 | Not at all. Quite the opposite--I respect her\n |
| 0x2487d6 | 14 | even more now. |
| 0x2487e5 | 46 | Hee hee! Looks like you understand Ku's many\n |
| 0x248814 | 7 | charms. |
| 0x24881c | 15 | Fellow comrade. |
| 0x24882c | 25 | Oh, can I have some more? |
| 0x248846 | 5 | Same. |
| 0x24884c | 16 | Oh, of course... |
| 0x24885d | 45 | I hear voices from our headquarters. I look\n |
| 0x24888b | 44 | inside to find everyone taking care of our\n |
| 0x2488b8 | 7 | guests. |
| 0x2488c0 | 45 | I would never have pictured Kuon begging to\n |
| 0x2488ee | 46 | sleep in her siblings' bed from being afraid\n |
| 0x24891d | 12 | of the dark. |
| 0x24892a | 45 | It is true that in one's younger years, the\n |
| 0x248958 | 47 | slightest ambiguities become beacons of terror. |
| 0x248988 | 49 | Now that I recall, you were always apprehensive\n |
| 0x2489ba | 42 | about the central pillar within our house. |
| 0x2489e5 | 34 | Th-That was perfectly justified!\n |
| 0x248a08 | 48 | I keep telling you, that pattern shaped like a\n |
| 0x248a39 | 16 | face could TALK! |
| 0x248a4a | 48 | I-It would speak to me, and say things in this\n |
| 0x248a7b | 40 | evil voice, like "I'll eat you up"...!\n |
| 0x248aa4 | 19 | I swear it's true!! |
| 0x248ab8 | 44 | Dear sister, I do look up to and trust you\n |
| 0x248ae5 | 43 | implicitly, but a talking pillar is a bit\n |
| 0x248b11 | 16 | far-fetched, no? |
| 0x248b22 | 29 | I'm telling you, it's true!\n |
| 0x248b40 | 23 | That thing SPOKE to me! |
| 0x248b58 | 47 | I see. Well, I suppose there are phenomena in\n |
| 0x248b88 | 27 | this world yet unexplained. |
| 0x248ba4 | 41 | You don't even believe me, do you, Ougi!? |
| 0x248bce | 51 | Ougi sits there with an extremely satisfied grin.\n |
| 0x248c02 | 43 | I think the story behind this one is clear. |
| 0x248c2e | 42 | Oh I know. I'll share my favorite story!\n |
| 0x248c59 | 37 | It's about Ku having a big adventure. |
| 0x248c7f | 45 | We've yet to share even a third of how cute\n |
| 0x248cad | 6 | Ku is. |
| 0x248cb4 | 19 | A... big adventure? |
| 0x248cc8 | 36 | Mhm! I call it "Ku's mushroom hunt." |
| 0x248ced | 14 | Mushroom hunt? |
| 0x248cfc | 49 | It happened a while ago, back when Ku was still\n |
| 0x248d2e | 13 | really small. |
| 0x248d3c | 18 | So small. So cute. |
| 0x248d4f | 45 | At the time, Ku was a troubled little maiden. |
| 0x248d7d | 9 | Troubled? |
| 0x248d87 | 7 | Maiden? |
| 0x248d8f | 48 | Yep... There was something deeply troubling Ku\n |
| 0x248dc0 | 14 | in those days. |
| 0x248dcf | 51 | Oh? Something that distressed Kuon as a child...?\n |
| 0x248e03 | 21 | By all means, say on. |
| 0x248e19 | 50 | Hee hee, I know. There's only one thing that can\n |
| 0x248e4c | 44 | trouble a maiden's heart... A little thing\n |
| 0x248e79 | 12 | called love. |
| 0x248e86 | 5 | Nope. |
| 0x248e8c | 41 | Hmm, that's not a bad guess, but it was\n |
| 0x248eb6 | 20 | something different. |
| 0x248ecb | 34 | Something that troubled Kuon, huh? |
| 0x248eee | 44 | I don't usually go poking my nose in other\n |
| 0x248f1b | 45 | folks' business, but I'd be lying if I said\n |
| 0x248f49 | 17 | I wasn't curious. |
| 0x248f5b | 42 | I feel a little guilty, but I can't help\n |
| 0x248f86 | 35 | listening in a little more closely. |
| 0x248faa | 48 | Camyu's gaze grows a bit distant, as though in\n |
| 0x248fdb | 18 | fond recollection. |
| 0x248fee | 46 | At the time, Ku still had a habit of wetting\n |
| 0x24901d | 8 | her bed. |
| 0x249026 | 44 | So that's why Ku decided to search for the\n |
| 0x249053 | 38 | legendary mushroom that would cure it. |
| 0x24907a | 34 | Specifically, the samanyafusube.\n |
| 0x24909d | 27 | Supposed to help with that. |
| 0x2490b9 | 45 | I look around to see everyone unsure of how\n |
| 0x2490e7 | 28 | to react to this revelation. |
| 0x249104 | 48 | I think I see why Kuon has a hard time dealing\n |
| 0x249135 | 45 | with these two. I'm actually a little sorry\n |
| 0x249163 | 8 | for her. |
| 0x24916c | 45 | The worst part is that they don't even mean\n |
| 0x24919a | 45 | any harm by it. I can imagine that makes it\n |
| 0x2491c8 | 11 | unbearable. |
| 0x2491d4 | 36 | Dear sister would... wet her bed...? |
| 0x2491f9 | 48 | There's shock in her voice, but is that a hint\n |
| 0x24922a | 33 | of relief...? Maybe it's just me. |
| 0x24924c | 49 | There is likely some variance in frequency, but\n |
| 0x24927e | 49 | surely all children experience similar mishaps,\n |
| 0x2492b0 | 3 | no? |
| 0x2492b4 | 29 | Don't you agree, dear sister? |
| 0x2492d2 | 50 | Huh!? O-Of course! Everybody makes mistakes when\n |
| 0x249305 | 15 | they are young. |
| 0x249315 | 48 | Th-That's right... There's nothing wrong about\n |
| 0x249346 | 5 | it... |
| 0x24934c | 47 | True, but as her rite of adolescence ceremony\n |
| 0x24937c | 41 | was coming up, it was a bit of a problem. |
| 0x2493a6 | 43 | That's why Ku was so deeply troubled by it. |
| 0x2493d2 | 37 | I suddenly feel a presence behind me. |
| 0x2493f8 | 41 | I look around to find Kuon shaking with\n |
| 0x249422 | 41 | embarrassment, tears welling in her eyes. |
| 0x24944c | 42 | I thought I told you to make them leave... |
| 0x249477 | 44 | Gah!? Well, they kinda let themselves in--\n |
| 0x2494a4 | 26 | what was I supposed to do? |
| 0x2494bf | 9 | Urrrgh... |
| 0x2494c9 | 41 | The door is opened with a slam, drawing\n |
| 0x2494f3 | 21 | everyone's attention. |
| 0x249509 | 44 | H-Hello, sisters... I had no idea you were\n |
| 0x249536 | 33 | both here. Good to see you again. |
| 0x249558 | 48 | She tries to act like nothing's wrong, but her\n |
| 0x249589 | 45 | face is stiff, and she's still on the verge\n |
| 0x2495b7 | 9 | of tears. |
| 0x2495c1 | 21 | Oh, welcome back, Ku. |
| 0x2495d7 | 20 | We were waiting, Ku. |
| 0x2495ec | 35 | We were all just talking about you. |
| 0x249610 | 22 | Sharing your cuteness. |
| 0x249627 | 33 | Come over here, Ku. Here, here!\n |
| 0x249649 | 15 | Sit right here. |
| 0x249659 | 49 | Camyu happily tugs at the sleeve of her story's\n |
| 0x24968b | 20 | beloved protagonist. |
| 0x2496a0 | 46 | Kuon looks around to see everyone looking at\n |
| 0x2496cf | 24 | her with awkward smiles. |
| 0x2496e8 | 22 | Sorry. I was too late. |
| 0x2496ff | 49 | And so we end up guiding the two of them around\n |
| 0x249731 | 21 | the imperial capital. |
| 0x249747 | 46 | I look back to see what Camyu and Aruruu are\n |
| 0x249776 | 6 | doing. |
| 0x24977d | 47 | The two look around the city in awe, munching\n |
| 0x2497ad | 37 | on the candy we bought along the way. |
| 0x2497d3 | 47 | I casually keep pace with Kuon and whisper to\n |
| 0x249803 | 29 | You sure you're OK with this? |
| 0x249821 | 10 | With what? |
| 0x24982c | 50 | With these two walking around in broad daylight.\n |
| 0x24985f | 39 | Wouldn't it be bad if someone saw them? |
| 0x249887 | 44 | I think it's fine. I'm pretty sure they're\n |
| 0x2498b4 | 45 | hiding their presence with some perception-\n |
| 0x2498e2 | 20 | distorting illusion. |
| 0x2498f7 | 46 | She is one of the most powerful thaumaturges\n |
| 0x249926 | 43 | of Tuskur... even if she doesn't look it... |
| 0x249952 | 35 | Well, this was all pretty sudden.\n |
| 0x249976 | 37 | You have plans on where to take them? |
| 0x24999c | 40 | At that, Kuon only smiles confidently,\n |
| 0x2499c5 | 19 | continuing forward. |
| 0x2499d9 | 45 | I've already prepared a selective itinerary\n |
| 0x249a07 | 26 | for just such an occasion. |
| 0x249a22 | 48 | I'll take the two of them to all those places.\n |
| 0x249a53 | 45 | I want to see them filled with shock and awe. |
| 0x249a81 | 19 | Shock and awe, huh. |
| 0x249a95 | 49 | So she's planned ahead for them visiting. Guess\n |
| 0x249ac7 | 49 | she really likes them, no matter what she says... |
| 0x249af9 | 45 | I mutter, making sure Kuon (who seems oddly\n |
| 0x249b27 | 49 | determined) can't hear. She'd probably strangle\n |
| 0x249b59 | 3 | me. |
| 0x249b5d | 50 | I imagine Kuon staying up all night plotting out\n |
| 0x249b90 | 45 | a tour... I don't know what to think anymore. |
| 0x249bbe | 39 | So Ku, you said you'd give us a tour.\n |
| 0x249be6 | 25 | Where are we going to go? |
| 0x249c00 | 43 | I suppose we can first go to the imperial\n |
| 0x249c2c | 49 | theater. It's the public's most famous spot for\n |
| 0x249c5e | 14 | entertainment. |
| 0x249c6d | 33 | Oh my... The lines are so long.\n |
| 0x249c8f | 32 | I don't know if we can get in... |
| 0x249cb0 | 18 | Um... Miss Kuon... |
| 0x249cc3 | 49 | The... The program there has just changed, so I\n |
| 0x249cf5 | 50 | believe the seats will be very full for a while... |
| 0x249d28 | 50 | All reserved seating is sold out... and you have\n |
| 0x249d5b | 41 | to line up in early morning for general\n |
| 0x249d85 | 12 | admission... |
| 0x249d92 | 46 | If we join the line now, I'm afraid we could\n |
| 0x249dc1 | 43 | only get tickets for standing room in the\n |
| 0x249ded | 7 | back... |
| 0x249df5 | 18 | I-I had no idea... |
| 0x249e08 | 28 | Ku, we've already been here. |
| 0x249e25 | 49 | Mhm. We were invited as national guests and got\n |
| 0x249e57 | 37 | to use the fancy suite room... Sorry. |
| 0x249e7d | 49 | I... suppose there's no point being here, then.\n |
| 0x249eaf | 50 | Well, it's a bit far, but how about the Imperial\n |
| 0x249ee2 | 7 | Garden? |
| 0x249eea | 51 | They've collected all the plants in Yamato there.\n |
| 0x249f1e | 43 | You can see the nation's botanical variety. |
| 0x249f4a | 49 | They have a greenhouse in the back, and you can\n |
| 0x249f7c | 48 | even see the rare plants of the south there too. |
| 0x249fad | 45 | Huh... I had no idea there was a place like\n |
| 0x249fdb | 5 | that. |
| 0x249fe1 | 47 | Um, actually, Ku... That was one of the first\n |
| 0x24a011 | 46 | places they guided us around when we got here. |
| 0x24a040 | 3 | Mm. |
| 0x24a044 | 5 | Huh!? |
| 0x24a04a | 49 | All they did was walk around and brag about it.\n |
| 0x24a07c | 7 | Boring. |
| 0x24a084 | 49 | Yeah. I would've preferred to hear explanations\n |
| 0x24a0b6 | 28 | about the plants themselves. |
| 0x24a0d3 | 9 | Nrrrgh... |
| 0x24a0dd | 23 | What about the library? |
| 0x24a0f5 | 50 | In the Imperial Cloister, there's a huge library\n |
| 0x24a128 | 46 | with public access. You can see how advanced\n |
| 0x24a157 | 10 | Yamato is. |
| 0x24a162 | 45 | Oh... That might not work out. The Imperial\n |
| 0x24a190 | 46 | Cloister's barrier is strong, so my illusion\n |
| 0x24a1bf | 11 | might fail. |
| 0x24a1cb | 9 | I... see. |
| 0x24a1d5 | 24 | Then, ah... that statue? |
| 0x24a1ee | 47 | Kuon points at a statue of a middle-aged man,\n |
| 0x24a21e | 43 | standing in the center of the thoroughfare. |
| 0x24a24a | 25 | The statue of the Mikado. |
| 0x24a264 | 49 | I'd say he's an important figure where Yamato's\n |
| 0x24a296 | 47 | concerned, but it's not that exciting to look\n |
| 0x24a2c6 | 5 | at... |
| 0x24a2cc | 47 | He must have been quite a dashing fellow when\n |
| 0x24a2fc | 45 | he was young. Still, a bit grandiose for my\n |
| 0x24a32a | 7 | tastes. |
| 0x24a332 | 14 | M-Miss Atuy... |
| 0x24a341 | 49 | Rulutieh gives Atuy an admonishing look, though\n |
| 0x24a373 | 48 | she seems baffled as to Atuy's unique taste in\n |
| 0x24a3a4 | 4 | men. |
| 0x24a3a9 | 50 | The Mikado... Oh, you mean that old grandpa that\n |
| 0x24a3dc | 40 | we met at the evening banquet last time. |
| 0x24a405 | 36 | He looked like a really kind person! |
| 0x24a42a | 32 | Mhm. Gave us lots of presents.\n |
| 0x24a44b | 14 | Very generous. |
| 0x24a45a | 36 | The Mikado as a young man, huh...?\n |
| 0x24a47f | 35 | He looks exactly like that old guy. |
| 0x24a4a3 | 47 | ...Now that I think about it, I still need to\n |
| 0x24a4d3 | 47 | report back to him about what we found in the\n |
| 0x24a503 | 6 | ruins. |
| 0x24a50a | 45 | But... at the same time, he was kinda scary\n |
| 0x24a538 | 4 | too. |
| 0x24a53d | 49 | Like a beast. He may be old, but he still hides\n |
| 0x24a56f | 12 | sharp fangs. |
| 0x24a57c | 8 | Urrgh... |
| 0x24a585 | 48 | I'm sure Camyu and Aruruu don't mean any harm,\n |
| 0x24a5b6 | 49 | but Kuon looks like she's on the verge of tears\n |
| 0x24a5e8 | 6 | again. |
| 0x24a5ef | 43 | Camyu and Aruruu seem to notice this, and\n |
| 0x24a61b | 44 | quickly cover their mouths with their hands. |
| 0x24a648 | 44 | Oh... I-I know, Ku. We've seen the obvious\n |
| 0x24a675 | 39 | tourist spots, so how about something\n |
| 0x24a69d | 15 | out-of-the-way? |
| 0x24a6ad | 18 | Out... of the way? |
| 0x24a6c0 | 46 | Mhm! Do you know someplace that would be fun\n |
| 0x24a6ef | 6 | to go? |
| 0x24a6f6 | 48 | I-It's not as if I don't, but... I can't think\n |
| 0x24a727 | 34 | of anywhere on the spot like this. |
| 0x24a74a | 46 | Cammie, Ku's not really good at this kind of\n |
| 0x24a779 | 6 | stuff. |
| 0x24a780 | 49 | She doesn't have friends, so she doesn't really\n |
| 0x24a7b2 | 30 | know how or where to hang out. |
| 0x24a7d1 | 5 | Oh... |
| 0x24a7d7 | 24 | I-I do too have friends! |
| 0x24a7f0 | 34 | D-Don't worry about it too much.\n |
| 0x24a813 | 44 | Um, I didn't have friends when I was young\n |
| 0x24a840 | 19 | either... you know? |
| 0x24a854 | 45 | And besides, it should be a gentleman's job\n |
| 0x24a882 | 17 | to escort a lady! |
| 0x24a894 | 33 | So that's why I'll ask you, Haku. |
| 0x24a8b6 | 48 | Huh? Ask me...? What, I'm supposed to take you\n |
| 0x24a8e7 | 29 | to some kind of hangout spot? |
| 0x24a905 | 37 | Mhm. Somewhere we can all have fun.\n |
| 0x24a92b | 26 | Can you think of anything? |
| 0x24a946 | 33 | Well, I guess I have some idea... |
| 0x24a968 | 10 | Is it fun? |
| 0x24a973 | 20 | Probably... I think. |
| 0x24a988 | 40 | Really? I want to see it. Take us there! |
| 0x24a9b1 | 46 | Haku... you'd better not take them someplace\n |
| 0x24a9e0 | 8 | weird... |
| 0x24a9e9 | 18 | Well, yeah, but... |
| 0x24a9fc | 47 | ...Why do I get the feeling you're taking out\n |
| 0x24aa2c | 17 | your anger on me? |
| 0x24aa3e | 15 | I-Isn't this... |
| 0x24aa4e | 44 | Ooh, I can just FEEL the thrills in the air. |
| 0x24aa7b | 32 | Everyone feels a bit... scary... |
| 0x24aa9c | 47 | Well, the people here are putting their lives\n |
| 0x24aacc | 23 | on the line, after all. |
| 0x24aae4 | 28 | Is this... a dog race track? |
| 0x24ab01 | 13 | A race track? |
| 0x24ab0f | 49 | Allow me! Here, orkes will race each other, and\n |
| 0x24ab41 | 47 | spectators wager on the results. It's related\n |
| 0x24ab71 | 45 | to coursing, and was once called "inukurabe"! |
| 0x24ab9f | 28 | So basically, it's gambling. |
| 0x24abbc | 50 | Atuy, Nosuri, and Ougi seem fine with this fact,\n |
| 0x24abef | 48 | but Rulutieh and Nekone are a bit out of their\n |
| 0x24ac20 | 6 | depth. |
| 0x24ac27 | 48 | Kuon gives an exasperated sigh as she rubs her\n |
| 0x24ac58 | 34 | palm wearily against her forehead. |
| 0x24ac7b | 50 | I suppose I'd like to know what exactly you were\n |
| 0x24acae | 27 | thinking, bringing us here. |
| 0x24acca | 48 | Well, I mean, they asked to see a hangout spot\n |
| 0x24acfb | 50 | that national guests usually wouldn't be brought\n |
| 0x24ad2e | 9 | to, so... |
| 0x24ad38 | 21 | Yes, we did say that. |
| 0x24ad4e | 45 | Kuon suddenly freezes as she says this, and\n |
| 0x24ad7c | 23 | levels her glare at me. |
| 0x24ad94 | 43 | You seem rather familiar with this place.\n |
| 0x24adc0 | 15 | Have you been-- |
| 0x24add0 | 11 | Ah, crap... |
| 0x24addc | 7 | Haku... |
| 0x24ade4 | 47 | Kuon's tail stretches out and wraps around my\n |
| 0x24ae14 | 5 | head. |
| 0x24ae1a | 41 | W-Wait, this place is run by the state!\n |
| 0x24ae44 | 41 | It's a glimpse at national policy! It's\n |
| 0x24ae6e | 22 | completely legitimate! |
| 0x24ae85 | 50 | And hey, I'm pretty much donating to the country\n |
| 0x24aeb8 | 33 | itself! I'm a model patriot here! |
| 0x24aeda | 42 | Which I assume means you've been losing.\n |
| 0x24af05 | 49 | There you go, squandering all your money again... |
| 0x24af37 | 50 | B-But my money is eventually used for the city's\n |
| 0x24af6a | 47 | bridges and roads, so I'm making it safer for\n |
| 0x24af9a | 8 | childr-- |
| 0x24afa3 | 20 | Stop making excuses. |
| 0x24afb8 | 15 | Owowowowowowow! |
| 0x24afc8 | 43 | Kuon's tail tightens around me like a vice. |
| 0x24aff4 | 47 | Hold on a moment, Kuon. Haku speaks pure truth! |
| 0x24b024 | 46 | Indeed, gambling can be considered a type of\n |
| 0x24b053 | 43 | charity! Therefore, enjoying it is hardly-- |
| 0x24b07f | 12 | Dear sister. |
| 0x24b08c | 49 | Wait a minute. Where did the guests from Tuskur\n |
| 0x24b0be | 3 | go? |
| 0x24b0c2 | 49 | Nekone exclaims, as though she's just remembered. |
| 0x24b0f4 | 35 | Huh...? But they were right here... |
| 0x24b118 | 48 | Then we hear a voice calling to us from far off. |
| 0x24b149 | 5 | Haku! |
| 0x24b14f | 46 | We look over to see Camyu and Aruruu running\n |
| 0x24b17e | 44 | towards us, hands full of small paper slips. |
| 0x24b1ab | 43 | Look! I won. The odds were fifteen to one\n |
| 0x24b1d7 | 8 | against! |
| 0x24b1e0 | 12 | ...Wh-What!? |
| 0x24b1ed | 38 | I won too. Odds thirty to one against. |
| 0x24b214 | 13 | Impossible... |
| 0x24b222 | 19 | Oh wow! How lovely! |
| 0x24b236 | 48 | Are you two veterans in these sorts of games...? |
| 0x24b267 | 35 | Aruruu shakes her head in response. |
| 0x24b28b | 47 | First time. But I can tell which one wants to\n |
| 0x24b2bb | 26 | win, and which one's fast. |
| 0x24b2d6 | 48 | Sister... I don't think the Yaana Mauna should\n |
| 0x24b307 | 42 | be partaking in these kinds of activities. |
| 0x24b332 | 41 | A Yaana Mauna? So they really do exist... |
| 0x24b35c | 21 | A Yaana... what, now? |
| 0x24b372 | 46 | A person that can understand the thoughts of\n |
| 0x24b3a1 | 47 | animals. Some say they can even converse with\n |
| 0x24b3d1 | 5 | them. |
| 0x24b3d7 | 25 | So kind of like Rulutieh? |
| 0x24b3f1 | 42 | Oh, uh... No... I can't really tell what\n |
| 0x24b41c | 20 | Cocopo's thinking... |
| 0x24b431 | 10 | Really...? |
| 0x24b43c | 31 | I can tell what they're saying. |
| 0x24b45c | 51 | Speaking with animals...? I've met too many weird\n |
| 0x24b490 | 43 | people already. This doesn't even faze me\n |
| 0x24b4bc | 8 | anymore. |
| 0x24b4c5 | 15 | She's the same. |
| 0x24b4d5 | 7 | Huh...? |
| 0x24b4dd | 32 | I can tell. You're just like me. |
| 0x24b4fe | 6 | Me...? |
| 0x24b505 | 27 | Understanding animals, huh? |
| 0x24b521 | 48 | If I can exploit an ability like that, I might\n |
| 0x24b552 | 46 | not win all the time, but I'd definitely win\n |
| 0x24b581 | 7 | MORE... |
| 0x24b589 | 51 | Hmm, I could use an ability like that... But what\n |
| 0x24b5bd | 41 | of my pride as a sportswoman and gambler? |
| 0x24b5e7 | 48 | ...By the way, who do you think's going to win\n |
| 0x24b618 | 5 | next? |
| 0x24b61e | 30 | W-Wait, Haku! That's not fair! |
| 0x24b63d | 50 | The one with black spots. He's telling me to bet\n |
| 0x24b670 | 7 | on him. |
| 0x24b678 | 24 | He seems really excited. |
| 0x24b691 | 8 | ...Haku. |
| 0x24b69a | 46 | Kuon's smile is giving me chills down my back. |
| 0x24b6c9 | 45 | H-Hold it! I just want to see if what she's\n |
| 0x24b6f7 | 15 | saying is true. |
| 0x24b707 | 42 | I mean, you gotta admit this is at least\n |
| 0x24b732 | 44 | interesting. I just want to try it out once. |
| 0x24b75f | 29 | Guess that's not gonna fly... |
| 0x24b77d | 48 | Ahem! I think Haku's right. It would not do to\n |
| 0x24b7ae | 39 | abuse such an ability, but why not see? |
| 0x24b7d6 | 32 | *Sigh*... Fine. I guess you can. |
| 0x24b7f7 | 12 | Huh? Really? |
| 0x24b804 | 43 | But I'm only going to allow it this once.\n |
| 0x24b830 | 7 | Got it? |
| 0x24b838 | 29 | All right! That's all I need. |
| 0x24b856 | 47 | I'm gonna put everything I've got on that one\n |
| 0x24b886 | 17 | with black spots. |
| 0x24b898 | 49 | Hmm... my instinct as a gambler tells me to bet\n |
| 0x24b8ca | 32 | on the one with the black spots. |
| 0x24b8eb | 46 | It has nothing to do with whatever she said.\n |
| 0x24b91a | 44 | It's just... my own personal hunch, you see! |
| 0x24b947 | 48 | Sister, do you really think the one with black\n |
| 0x24b978 | 15 | spots will win? |
| 0x24b988 | 48 | I don't lie. That one with black spots will win. |
| 0x24b9b9 | 43 | But Aru, that one's not in the next race,\n |
| 0x24b9e5 | 6 | is he? |
| 0x24b9ec | 43 | Oh... OK. Yeah, I had a feeling something\n |
| 0x24ba18 | 23 | like this would happen. |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_05.json` com a forma:
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
