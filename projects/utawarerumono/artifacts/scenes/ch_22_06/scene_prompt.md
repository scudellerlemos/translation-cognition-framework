# Cena ch_22_06 — pacote de traducao (430 linhas)

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
| Camyu | Personagem | Camyu | manter_original | moderate |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| Onkamiyamukai | Local | Onkamiyamukai | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Ukon | Personagem | Ukon | manter_original | major |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Yamatan | Etnia | de Yamato | traduzir | none |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `...Hey, Ukon.` -> `...Oi, Ukon.` (Haku, 22_02)
- `What're you talking about?` -> `Como assim?` (Ukon, 13_05)
- `Take a seat.` -> `Sente-se.` (Kuon, 18_01)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `There we go...` -> `Pronto...` (Kuon, 11_02)
- `For you, Master.` -> `Para você, Mestre.` (Maroro, 19_06)
- `Haku & Ukon` -> `Haku & Ukon` (SISTEMA, 17_01)
- `Cheers!` -> `Saúde!` (Homens, 14_04)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `Heh...` -> `Heh...` (Ougi, 17_04)
- `around them.` -> `ao redor delas.` (Haku, 20_03)
- `Oh...?` -> `Oh...?` (Homem, 14_09)
- `this.` -> `essa.` (Moznu, 13_05)
- `command.` -> `ordem.` (Maroro, 18_01)
- `What do you mean?` -> `O que você quer dizer?` (Haku, 13_01)
- `Right?` -> `né?` (Haku, 11_01)
- `them.` -> `deles.` (Kuon, 11_05)
- `whole thing.` -> `coisa toda.` (Garota, 17_01)
- `me.` -> `mim.` (Garota, 17_01)
- `explaining.` -> `explicando.` (Rulutieh, 18_01)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `a little.` -> `um pouco.` (Haku, 11_05)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `bewildered.` -> `confusa.` (Haku, 19_08)
- `kitchen.` -> `cozinha.` (Garota, 22_04)
- `Mm.` -> `Ã©.` (Protagonista, 22_05)
- `to do.` -> `fazer.` (Haku, 22_04)
- `Kuon.` -> `Kuon.` (Kuon, 11_02)
- `What's the matter?` -> `O que foi?` (Haku, 15_02)
- `can.` -> `consigo.` (Haku, 19_08)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `HYAH!` -> `HYAH!` (Haku, 18_01)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `as well.` -> `também.` (Haku, 17_01)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Uh...` -> `Ahn...` (Haku, 14_03)
- `then.` -> `então.` (Kuon, 13_01)
- `Urk...` -> `Argh...` (Haku, 12_06)
- `though.` -> `porém.` (Kuon, 12_04)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `back.` -> `voltei.` (Haku, 18_01)
- `sister...` -> `do Ukon...` (Haku, 14_04)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `mind.` -> `mente.` (NARRAÇÃO, 12_08)
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
| 0x24e6fa | 3 | Yo. |
| 0x24e700 | 43 | As an energetic voice breaks the silence,\n |
| 0x24e72c | 38 | I snap out of my slee--uh, meditation. |
| 0x24e753 | 23 | How's everything going? |
| 0x24e76b | 13 | ...Hey, Ukon. |
| 0x24e779 | 48 | Kid, I knew you had a lotta hidden skills, but\n |
| 0x24e7aa | 45 | I didn't know y'could fall asleep with your\n |
| 0x24e7d8 | 10 | eyes open. |
| 0x24e7e3 | 26 | What're you talking about? |
| 0x24e7fe | 44 | Gahahahaha! Well, in any case, I brought a\n |
| 0x24e82b | 37 | little present with me. Care to join? |
| 0x24e851 | 27 | Ukon hoists a small bottle. |
| 0x24e86d | 31 | Oho... You have my attention.\n |
| 0x24e88d | 12 | Take a seat. |
| 0x24e89a | 51 | Somehow, the twins manage to produce a huge array\n |
| 0x24e8ce | 43 | of pickles, salted fish, jerky, and cheese. |
| 0x24e8fa | 32 | Allow us to pour your first cup. |
| 0x24e91b | 34 | Please enjoy as well, Master Ukon. |
| 0x24e93e | 11 | Oh, thanks. |
| 0x24e94a | 14 | There we go... |
| 0x24e959 | 48 | Saraana tips the bottle and begins to pour the\n |
| 0x24e98a | 21 | sake into Ukon's cup. |
| 0x24e9a0 | 16 | For you, master. |
| 0x24e9b1 | 21 | Oop, that's enough... |
| 0x24e9c7 | 29 | Well, a toast to free booze-- |
| 0x24e9e5 | 32 | A toast to a pair of lazy bums-- |
| 0x24ea06 | 11 | Haku & Ukon |
| 0x24ea12 | 7 | Cheers! |
| 0x24ea1a | 41 | We lift our cups and clink them together. |
| 0x24ea44 | 49 | Whew, that stuff's amazing! A hard drink tastes\n |
| 0x24ea76 | 46 | so good in the afternoon... Even better when\n |
| 0x24eaa5 | 10 | it's free. |
| 0x24eab0 | 48 | Makes me glad I brought it, seein' you in such\n |
| 0x24eae1 | 12 | a good mood. |
| 0x24eaee | 5 | Here. |
| 0x24eaf4 | 45 | OK, OK. So what did you come here to tell me? |
| 0x24eb22 | 48 | I waggle a piece of fish as questioningly as I\n |
| 0x24eb53 | 24 | can, as I speak to Ukon. |
| 0x24eb6c | 47 | That was some damn good booze you brought me.\n |
| 0x24eb9c | 35 | I'm sure it's not gonna come cheap. |
| 0x24ebc0 | 48 | Or are you gonna tell me you came all this way\n |
| 0x24ebf1 | 44 | just to drink with me in the middle of the\n |
| 0x24ec1e | 10 | afternoon? |
| 0x24ec29 | 48 | Judging by the taste, this is top-drawer stuff\n |
| 0x24ec5a | 46 | for special occasions. It literally COULDN'T\n |
| 0x24ec89 | 11 | come cheap. |
| 0x24ec95 | 6 | Heh... |
| 0x24ec9c | 48 | Ukon doesn't reply at first, just swishing the\n |
| 0x24eccd | 23 | sake around in his cup. |
| 0x24ece5 | 48 | After he finishes his cup, he gives a huge grin. |
| 0x24ed16 | 51 | You probably already heard the Tuskur ambassadors\n |
| 0x24ed4a | 47 | will be heading back to their country tomorrow. |
| 0x24ed7a | 44 | The plan is, we're gonna do a short little\n |
| 0x24eda7 | 47 | ceremony and then they'll head out immediately. |
| 0x24edd7 | 46 | Which would mean that the mission I gave you\n |
| 0x24ee06 | 20 | will come to an end. |
| 0x24ee1b | 21 | So it's finally over. |
| 0x24ee31 | 51 | I thought watching them would be an easy mission,\n |
| 0x24ee65 | 42 | but it was harder than any physical labor. |
| 0x24ee90 | 37 | And thanks to that, I'm all worn out. |
| 0x24eeb6 | 48 | What's wrong with that? Got some good exercise\n |
| 0x24eee7 | 15 | in, didn't you? |
| 0x24eef7 | 47 | Well. In any case, kid, I want you to tell me\n |
| 0x24ef27 | 20 | everything you know. |
| 0x24ef3c | 14 | ...About them? |
| 0x24ef4b | 23 | Yeah. What's your take? |
| 0x24ef63 | 45 | Ukon's eyes narrow as his gaze focuses on me. |
| 0x24ef91 | 41 | Well... I dunno how I should answer that. |
| 0x24efbb | 47 | I take a small sip from my cup before I start\n |
| 0x24efeb | 8 | talking. |
| 0x24eff4 | 42 | In the end, they're just like they seem... |
| 0x24f01f | 49 | I spin my cup in my hands as I answer, watching\n |
| 0x24f051 | 38 | ripples spread across the sake within. |
| 0x24f078 | 45 | Good-natured, no apparent ulterior motives.\n |
| 0x24f0a6 | 45 | They just seem like nice people to be around. |
| 0x24f0d4 | 42 | Far as I can tell, they seemed more like\n |
| 0x24f0ff | 42 | tourists. I didn't get a sense of danger\n |
| 0x24f12a | 12 | around them. |
| 0x24f137 | 47 | They were so carefree... Didn't seem the type\n |
| 0x24f167 | 45 | to do anything underhanded for their country. |
| 0x24f195 | 47 | 'Course, I guess that's not how diplomats are\n |
| 0x24f1c5 | 38 | supposed to be... but I kinda like it. |
| 0x24f1ec | 46 | Tuskur must be a real nice place. She didn't\n |
| 0x24f21b | 42 | admit it, but it sounds like it's Kuon's\n |
| 0x24f246 | 13 | homeland too. |
| 0x24f258 | 48 | But... at the same time, I don't think they're\n |
| 0x24f289 | 14 | all they seem. |
| 0x24f298 | 6 | Oh...? |
| 0x24f29f | 46 | Ukon's eyebrows twitch at those words, but I\n |
| 0x24f2ce | 38 | continue on, pretending not to notice. |
| 0x24f2f5 | 49 | It's not like I saw what they can do firsthand,\n |
| 0x24f327 | 30 | but... ah, how do I put it...? |
| 0x24f346 | 45 | They might seem like defenseless girls, but\n |
| 0x24f374 | 47 | there's a presence to them. Like a chill down\n |
| 0x24f3a4 | 13 | your spine... |
| 0x24f3b2 | 47 | ...Ah, I don't even know where I'm going with\n |
| 0x24f3e2 | 5 | this. |
| 0x24f3e8 | 43 | Still, makes me wonder who they really are. |
| 0x24f414 | 48 | About that. I've heard some rumors that caught\n |
| 0x24f445 | 20 | my attention before. |
| 0x24f45a | 7 | Rumors? |
| 0x24f462 | 44 | Apparently, those two... Back in their own\n |
| 0x24f48f | 42 | country, they're high up in the chain of\n |
| 0x24f4ba | 8 | command. |
| 0x24f4c3 | 47 | I remember they said they were ambassadors in\n |
| 0x24f4f3 | 42 | name only. Got the job because of family\n |
| 0x24f51e | 27 | influence, or something...? |
| 0x24f53a | 46 | The impression I got was that they were just\n |
| 0x24f569 | 33 | figureheads for this little trip. |
| 0x24f58b | 50 | Family influence... huh. Wonder how much of that\n |
| 0x24f5be | 17 | is actually true. |
| 0x24f5d0 | 50 | ...You think Tuskur's plotting something against\n |
| 0x24f603 | 7 | Yamato? |
| 0x24f60b | 49 | To be honest, that'd make this all a lot easier\n |
| 0x24f63d | 13 | to deal with. |
| 0x24f64b | 17 | What do you mean? |
| 0x24f65d | 40 | Kid, you ever hear of the Onkamiyamukai? |
| 0x24f686 | 49 | The twins freeze for the briefest of moments at\n |
| 0x24f6b8 | 25 | the mention of that name. |
| 0x24f6d2 | 16 | No. What's that? |
| 0x24f6e3 | 46 | Well, they worship a certain god over there.\n |
| 0x24f712 | 48 | The Onkamiyamukai's basically the headquarters\n |
| 0x24f743 | 9 | for that. |
| 0x24f74d | 15 | Uitsualnemetia. |
| 0x24f75d | 50 | The Nugwisomkami that expelled man from paradise\n |
| 0x24f790 | 43 | and brought famine and suffering upon them. |
| 0x24f7bc | 14 | Uitsu... What? |
| 0x24f7cb | 48 | That's their god. Us Yamatan folks who worship\n |
| 0x24f7fc | 46 | the god incarnate, the Mikado, that's how we\n |
| 0x24f82b | 7 | see it. |
| 0x24f833 | 44 | So... is that going to cause any problems?\n |
| 0x24f860 | 47 | Religious differences usually don't end well,\n |
| 0x24f890 | 6 | right? |
| 0x24f897 | 46 | Don't worry. The people of Yamato tend to be\n |
| 0x24f8c6 | 48 | relatively accepting with these kinds of things. |
| 0x24f8f7 | 50 | As long as they don't push their religion on us,\n |
| 0x24f92a | 45 | we're not so brash that we'd do anything to\n |
| 0x24f958 | 5 | them. |
| 0x24f95e | 47 | So this rumor. Seems Lady Camyu is the little\n |
| 0x24f98e | 50 | sister of the Oruyankuru of the Onkamiyamukai...\n |
| 0x24f9c1 | 13 | Their leader. |
| 0x24f9cf | 51 | And they say she's some special kamunagi as well.\n |
| 0x24fa03 | 45 | You know... like these two, the Kamunagi of\n |
| 0x24fa31 | 7 | Chains. |
| 0x24fa39 | 52 | You felt something, eh? Yeah... I can't get a read\n |
| 0x24fa6e | 50 | on them. It's like I'll fall in if I dig too deep. |
| 0x24faa1 | 47 | I dunno what to do about it. It's those eyes.\n |
| 0x24fad1 | 49 | Like a bottomless bog filled with crystal-clear\n |
| 0x24fb03 | 8 | water... |
| 0x24fb0c | 51 | I only know one other person with eyes like that,\n |
| 0x24fb40 | 43 | and that's the high priestess, Lady Honoka. |
| 0x24fb6c | 36 | As for the other one, Lady Aruruu... |
| 0x24fb91 | 50 | I hear she's part of Tuskur's royalty, and she's\n |
| 0x24fbc4 | 44 | apparently pretty high up the chain herself. |
| 0x24fbf1 | 48 | But she's got the eyes of someone who's walked\n |
| 0x24fc22 | 30 | across countless battlefields. |
| 0x24fc41 | 36 | You saw that beast she was riding?\n |
| 0x24fc66 | 42 | Hard to think anyone could control that.\n |
| 0x24fc91 | 25 | Guess it's nature's gift. |
| 0x24fcab | 49 | Maybe they brought it because... they wanted to\n |
| 0x24fcdd | 30 | show proper respect to Yamato? |
| 0x24fcfc | 18 | ...I sure hope so. |
| 0x24fd0f | 47 | Ukon gulps down the remainder of the drink in\n |
| 0x24fd3f | 8 | his cup. |
| 0x24fd48 | 48 | To be honest, I hope I'm just overthinking the\n |
| 0x24fd79 | 12 | whole thing. |
| 0x24fd86 | 48 | He holds out his cup and Saraana moves to pour\n |
| 0x24fdb7 | 47 | him some more, but only a trickle escapes the\n |
| 0x24fde7 | 7 | bottle. |
| 0x24fdef | 21 | Please wait a moment. |
| 0x24fe05 | 44 | We shall prepare another bottle immediately. |
| 0x24fe32 | 34 | Nah, I think I'm good for today.\n |
| 0x24fe55 | 44 | Got a lot on my plate for tomorrow, anyways. |
| 0x24fe82 | 20 | Oh, but before that. |
| 0x24fe97 | 50 | Ukon takes out a small package wrapped in cloth,\n |
| 0x24feca | 49 | sets it down on the floor, and pushes it toward\n |
| 0x24fefc | 3 | me. |
| 0x24ff00 | 47 | Maybe a little early, but you've got my thanks. |
| 0x24ff30 | 28 | Well, I'll gladly accept it. |
| 0x24ff4d | 51 | I pick it up, and find that it's a little heavier\n |
| 0x24ff81 | 16 | than I expected. |
| 0x24ff92 | 43 | Ukon seems to pick up on my puzzled look,\n |
| 0x24ffbe | 11 | explaining. |
| 0x24ffca | 34 | Gave you a little extra this time. |
| 0x24ffed | 45 | Sorry I made you work with barely any info.\n |
| 0x25001b | 50 | Take it as an apology, as well as me buying your\n |
| 0x25004e | 8 | silence. |
| 0x250057 | 43 | Remember, if you mention anything to some\n |
| 0x250083 | 46 | civilian, you might never see another sunrise. |
| 0x2500b2 | 16 | ...Mention what? |
| 0x2500c3 | 37 | I shrug nonchalantly at Ukon's words. |
| 0x2500e9 | 43 | Heh... Guess you don't need me to tell you. |
| 0x250115 | 23 | With that, Ukon stands. |
| 0x25012d | 22 | We shall see you back. |
| 0x250144 | 48 | I begin to rise, intending to see him off, but\n |
| 0x250175 | 34 | Ukon puts his hand out to stop me. |
| 0x250198 | 48 | No need. I got some thinking to do on my own--\n |
| 0x2501c9 | 45 | I'll take a walk. See you. Glad you enjoyed\n |
| 0x2501f7 | 10 | the drink. |
| 0x250202 | 19 | I'll see you later. |
| 0x250216 | 42 | I say my goodbyes to Ukon, still seated.\n |
| 0x250241 | 46 | My gaze drifts out the window as I sit there\n |
| 0x250270 | 27 | vaguely thinking to myself. |
| 0x25028c | 47 | So those Tuskur folks are going back to their\n |
| 0x2502bc | 14 | own country... |
| 0x2502cb | 7 | Master. |
| 0x2502d3 | 29 | Would you like another drink? |
| 0x2502f1 | 24 | ...Yeah, would you mind? |
| 0x25030a | 37 | ...I wonder if Kuon knows about this. |
| 0x250330 | 8 | ...Mmnh? |
| 0x250339 | 43 | I wake up to find the room completely dark. |
| 0x250365 | 16 | Have you awoken? |
| 0x250376 | 47 | I feel a soft sensation behind my head. I can\n |
| 0x2503a6 | 47 | see Uruuru and Saraana looking down at my face. |
| 0x2503d6 | 46 | Guess I've been resting my head on their legs. |
| 0x250405 | 24 | Must've fallen asleep... |
| 0x25041e | 50 | My body feels a little heavy... probably because\n |
| 0x250451 | 21 | of all that drinking. |
| 0x250467 | 46 | *Yawn*... Think I'll take a bath, freshen up\n |
| 0x250496 | 9 | a little. |
| 0x2504a0 | 49 | I wake myself up, keep the twins from following\n |
| 0x2504d2 | 27 | me, then head to the baths. |
| 0x2504ee | 48 | It's getting cold. Should hurry and warm up in\n |
| 0x25051f | 11 | the bath... |
| 0x25052b | 3 | Hm? |
| 0x25052f | 47 | As I pass the kitchen on my way to the baths,\n |
| 0x25055f | 32 | I hear something shatter inside. |
| 0x250580 | 17 | ...Someone there? |
| 0x250592 | 49 | I poke my head inside the kitchen to see a tail\n |
| 0x2505c4 | 33 | vigorously wagging in the back... |
| 0x2505e6 | 44 | ...and I hear the sound of something being\n |
| 0x250613 | 7 | chewed. |
| 0x25061b | 7 | ...Hrm? |
| 0x250623 | 6 | Fnngh? |
| 0x25062a | 50 | The two figures, apparently fixated on something\n |
| 0x25065d | 39 | in the back, look over to me--clearly\n |
| 0x250685 | 11 | bewildered. |
| 0x250691 | 33 | Are you serious!? You two again!? |
| 0x2506b3 | 51 | These are ambassadors representing their country,\n |
| 0x2506e7 | 44 | and here they are stealing snacks from the\n |
| 0x250714 | 8 | kitchen. |
| 0x25071d | 35 | *Munch* *munch* *munch*... *gulp*\n |
| 0x250741 | 43 | I-I don't know what you're talking about... |
| 0x25076d | 47 | You're national guests, aren't you? You could\n |
| 0x25079d | 48 | probably get all the expensive stuff you want... |
| 0x2507ce | 29 | Expensive doesn't equal good. |
| 0x2507ec | 50 | Mm, well, the food here's so nostalgic, or stuff\n |
| 0x25081f | 42 | I've never eaten before. We can't help it. |
| 0x25084a | 3 | Mm. |
| 0x25084e | 48 | With that, she graciously offers me one of the\n |
| 0x25087f | 47 | dried fruits piled in her arms, like she owns\n |
| 0x2508af | 14 | Hey, that's... |
| 0x2508be | 16 | Do you want two? |
| 0x2508cf | 31 | That's the stuff that was here. |
| 0x2508ef | 47 | Aruruu then quickly begins to stuff the dried\n |
| 0x25091f | 17 | fruit into a bag. |
| 0x250931 | 41 | She's just gonna take the lot with her... |
| 0x25095b | 48 | So what exactly are you doing here? Aren't you\n |
| 0x25098c | 49 | supposed to be heading back to your own country\n |
| 0x2509be | 9 | tomorrow? |
| 0x2509c8 | 50 | Oh, yeah. That's why there were things we wanted\n |
| 0x2509fb | 6 | to do. |
| 0x250a02 | 10 | Souvenirs. |
| 0x250a0d | 38 | Oh, they brought souvenirs for Kuon... |
| 0x250a34 | 46 | Guess no matter how they act, they still are\n |
| 0x250a63 | 20 | good sisters to her. |
| 0x250a78 | 49 | And so Aruruu takes an urn full of kondens from\n |
| 0x250aaa | 38 | the shelf, and carries it in her arms. |
| 0x250ad1 | 43 | Wait you're the ones TAKING the souvenirs!? |
| 0x250afd | 22 | Also came to see Kuon. |
| 0x250b14 | 46 | I intended on just leaving them to their own\n |
| 0x250b43 | 44 | devices, but Camyu pulls me all the way to\n |
| 0x250b70 | 12 | Kuon's room. |
| 0x250b7d | 16 | Kuon, you there? |
| 0x250b8e | 42 | I knock on the door, egged on by the two\n |
| 0x250bb9 | 49 | giggling and hiding behind a pillar to surprise\n |
| 0x250beb | 5 | Kuon. |
| 0x250bf1 | 47 | After a little while, Kuon pokes her head out\n |
| 0x250c21 | 25 | and looks left and right. |
| 0x250c3b | 26 | Oh, it's just you, Haku.\n |
| 0x250c56 | 18 | What's the matter? |
| 0x250c69 | 29 | She sounds somewhat relieved. |
| 0x250c87 | 32 | Were you expecting other people? |
| 0x250ca8 | 44 | Hm? Well... I just had a feeling, I suppose. |
| 0x250cd5 | 37 | Whoa, she's got pretty keen senses.\n |
| 0x250cfb | 27 | She was right on the money. |
| 0x250d17 | 46 | The two tiptoe over to us as quietly as they\n |
| 0x250d46 | 4 | can. |
| 0x250d4b | 50 | What the hell are they doing? She can completely\n |
| 0x250d7e | 25 | see you like that... Huh? |
| 0x250d98 | 43 | Somehow, Kuon doesn't seem to notice them\n |
| 0x250dc4 | 11 | sidling up. |
| 0x250dd0 | 48 | Even as the two of them pass right in front of\n |
| 0x250e01 | 46 | her, she doesn't react at all, as if they're\n |
| 0x250e30 | 10 | invisible. |
| 0x250e3b | 5 | Kuon? |
| 0x250e41 | 25 | Hm? Something the matter? |
| 0x250e5b | 47 | She really hasn't noticed... What's going on?\n |
| 0x250e8b | 28 | Can she really not see them? |
| 0x250ea8 | 12 | Now! Charge! |
| 0x250eb5 | 5 | Hyah! |
| 0x250ebb | 7 | Wha--!? |
| 0x250ec3 | 48 | The two slip right past Kuon and into her room\n |
| 0x250ef4 | 12 | with a yell. |
| 0x250f01 | 10 | Alley-oop! |
| 0x250f0c | 38 | Camyu jumps headfirst into Kuon's bed. |
| 0x250f33 | 49 | Aruruu follows, and begins rolling around in it\n |
| 0x250f65 | 8 | as well. |
| 0x250f6e | 21 | Hmhm. Smells like Ku. |
| 0x250f84 | 18 | Hey, no fair, Aru! |
| 0x250f97 | 42 | Camyu and Aruruu begin tussling over the\n |
| 0x250fc2 | 40 | blankets, like kittens playing together. |
| 0x250feb | 32 | Wh-What are you two doing here!? |
| 0x25100c | 29 | Ahaha, we couldn't help it!\n |
| 0x25102a | 26 | We could smell your scent. |
| 0x251045 | 42 | You have a very rich and smooth scent, Ku. |
| 0x251070 | 43 | W-Would you stop talking as if I stink of\n |
| 0x25109c | 11 | something!? |
| 0x2510a8 | 33 | ...I don't smell that much, do I? |
| 0x2510ca | 24 | Kuon sniffs her sleeves. |
| 0x2510e3 | 48 | Didn't you two have something you came here for? |
| 0x251114 | 5 | Oh... |
| 0x25111a | 49 | The two seem to finally remember what they came\n |
| 0x25114c | 48 | here for, and get out of bed to sit up straight. |
| 0x25117d | 47 | I can sense Kuon getting anxious at the sight\n |
| 0x2511ad | 36 | of the two of them suddenly serious. |
| 0x2511d2 | 26 | We're going home tomorrow. |
| 0x2511ed | 15 | Oh, I... I see. |
| 0x2511fd | 38 | Which is why we wanted to talk to you. |
| 0x251224 | 45 | What's with this uncomfortable atmosphere...? |
| 0x251252 | 27 | Ku. Let's go back together. |
| 0x25126e | 7 | ...Huh? |
| 0x251276 | 19 | But... I haven't... |
| 0x25128a | 40 | The period we decided on already passed. |
| 0x2512b3 | 44 | You did promise you'd come home, didn't you? |
| 0x2512e0 | 15 | But, I still... |
| 0x2512f0 | 42 | I think we've already fulfilled all your\n |
| 0x25131b | 21 | requests. Haven't we? |
| 0x251331 | 5 | Uh... |
| 0x251337 | 21 | Kuon's... leaving...? |
| 0x25134d | 48 | Kuon looks down at her two sisters' words, but\n |
| 0x25137e | 45 | darts uncertain glances at me every now and\n |
| 0x2513ac | 5 | then. |
| 0x2513b2 | 39 | B-But I still have a duty to fulfill.\n |
| 0x2513da | 16 | I promised I'd-- |
| 0x2513eb | 34 | Don't use other people as excuses. |
| 0x25140e | 6 | Urk... |
| 0x251415 | 48 | Kuon seems to be at a loss, caught between the\n |
| 0x251446 | 32 | gentle gazes of her two sisters. |
| 0x251467 | 45 | ...*Sigh* Well, I guess it can't be helped.\n |
| 0x251495 | 49 | It'll be lonely after finally seeing you again,\n |
| 0x2514c7 | 7 | though. |
| 0x2514cf | 4 | Huh? |
| 0x2514d4 | 46 | But only for a little bit more. You hear me?\n |
| 0x251503 | 39 | I'll only let it slide a biiiit longer. |
| 0x25152b | 16 | ...Are you sure? |
| 0x25153c | 16 | So stubborn, Ku. |
| 0x25154d | 49 | There's not much we can do. Even if we tell her\n |
| 0x25157f | 43 | to come home, Ku's not one to listen to us. |
| 0x2515ab | 48 | But don't forget that everyone's worried about\n |
| 0x2515dc | 46 | you, OK? We're all waiting for when you come\n |
| 0x25160b | 5 | back. |
| 0x251611 | 45 | Kuon's body seems to be shaking slightly at\n |
| 0x25163f | 14 | Camyu's words. |
| 0x25164e | 35 | It's boring without you around, Ku. |
| 0x251672 | 9 | Sister... |
| 0x25167c | 48 | Kuon pulls her two sisters in a close, tearful\n |
| 0x2516ad | 8 | embrace. |
| 0x2516b6 | 30 | You're still such a child, Ku. |
| 0x2516d5 | 48 | Camyu warmly embraces her, burying Kuon's face\n |
| 0x251706 | 13 | in her chest. |
| 0x251714 | 30 | Make sure to stay healthy, OK? |
| 0x251733 | 7 | ...Mhm. |
| 0x25173b | 37 | And don't drink any unfiltered water. |
| 0x251761 | 34 | I'm not a child anymore, sister... |
| 0x251784 | 34 | You're not a child, but you're Ku. |
| 0x2517a7 | 26 | And I'm still Ku's sister. |
| 0x2517c2 | 44 | As I watch the two of them, I feel someone\n |
| 0x2517ef | 21 | tugging at my sleeve. |
| 0x251805 | 37 | I look over to see Aruruu at my side. |
| 0x25182b | 21 | Look after Ku for us. |
| 0x251841 | 32 | She softly whispers into my ear. |
| 0x251862 | 49 | As her eyes focus on mine, I almost feel myself\n |
| 0x251894 | 21 | getting lost in them. |
| 0x2518aa | 46 | A small smile flickers across the calm face,\n |
| 0x2518d9 | 27 | normally devoid of emotion. |
| 0x2518f5 | 47 | It was a beautiful smile... somehow like both\n |
| 0x251925 | 39 | an innocent child, and a gentle mother. |
| 0x25194d | 48 | A little after noon, people begin gathering on\n |
| 0x25197e | 48 | the main road to send off the Tuskur delegation. |
| 0x2519af | 15 | Here they come. |
| 0x2519d2 | 47 | Yes. I do hope we can see them again one day... |
| 0x251a02 | 49 | Bet a piece of tonight's dinner on the color of\n |
| 0x251a34 | 23 | the front rider's sash? |
| 0x251a4c | 35 | Hee hee, you're on. I'm all on red. |
| 0x251a70 | 31 | Hmhm! Then I shall choose blue. |
| 0x251a90 | 45 | I take a quick look at the person at my side. |
| 0x251abe | 11 | What is it? |
| 0x251aca | 8 | Nothing. |
| 0x251ad3 | 34 | Kuon's smile is softer than usual. |
| 0x251af6 | 44 | It feels almost like a heavy burden's been\n |
| 0x251b23 | 45 | lifted from her shoulders... I'd say, anyway. |
| 0x251b51 | 44 | Kuon looks away, her eyes on the procession. |
| 0x251b7e | 47 | I guess... I was being a spoiled child again... |
| 0x251bae | 46 | What's wrong about that? You should let them\n |
| 0x251bdd | 46 | pamper you while you can. It clearly doesn't\n |
| 0x251c0c | 12 | bother them. |
| 0x251c19 | 47 | Under normal circumstances, I'd be giving you\n |
| 0x251c49 | 29 | a lecture right now, I think. |
| 0x251c67 | 43 | But... I guess that answer suits you, Haku. |
| 0x251c93 | 37 | Here they come! Red, red, red, red... |
| 0x251cb9 | 25 | Blue, blue, blue, blue... |
| 0x251cd3 | 23 | This is awfully rude... |
| 0x251ceb | 43 | I see the carriage with Camyu passing by.\n |
| 0x251d17 | 43 | Next to it walks the giant beast carrying\n |
| 0x251d43 | 7 | Aruruu. |
| 0x251d4b | 48 | Aruruu lazily looks around at the crowd, while\n |
| 0x251d7c | 49 | Camyu waves happily in response to the cheering\n |
| 0x251dae | 6 | crowd. |
| 0x251db5 | 48 | And just as they pass, my eyes meet with theirs. |
| 0x251de6 | 43 | And they leave me with one last inaudible\n |
| 0x251e12 | 8 | message. |
| 0x251e1b | 23 | "See you again"... huh. |
| 0x251e33 | 45 | For some reason, Ukon's words surface in my\n |
| 0x251e61 | 5 | mind. |
| 0x251e67 | 45 | Guess I never asked them... who they really\n |
| 0x251e95 | 17 | were, in the end. |
| 0x251ea7 | 38 | Ah, well. Not like it matters, anyway. |
| 0x251ece | 49 | Kuon remains watching them as they continue on,\n |
| 0x251f00 | 34 | slowly disappearing down the road. |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_06.json` com a forma:
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
