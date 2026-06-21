# Cena ch_30_06 — pacote de traducao (180 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Saraana | Personagem | Saraana | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |

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
- `RightArm` -> `RightArm` (, 31_01)
- `mask` -> `mask` (SYSTEM, 20_14)
- `of course.` -> `claro.` (Haku, 18_01)
- `Ah...!` -> `Ah...!` (Man, 11_01)
- `Thank goodness...` -> `Que alívio...` (Haku, 23_10)
- `Dear brother...` -> `Querido irmão...` (Nekone, 14_04)
- `Lady-in-waiting` -> `Dama de companhia` (Ukon, 30_04)
- `...As you wish.` -> `...Como desejar.` (Oshtor, 23_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `for a moment.` -> `por um instante.` (Kuon, 11_02)
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `warriors.` -> `guerreiras.` (Haku, 23_11)
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
| 0x2dd7c9 | 8 | RightArm |
| 0x2dd7d2 | 4 | mask |
| 0x2dd7d8 | 9 | door_open |
| 0x2dd7e2 | 40 | Dear brother... Are you... all right...? |
| 0x2dd80b | 33 | Nekone asks, her voice quavering. |
| 0x2dd82d | 13 | Dear brothe-- |
| 0x2dd83b | 6 | lock04 |
| 0x2dd842 | 14 | polySurface731 |
| 0x2dd851 | 16 | polySurface27814 |
| 0x2dd862 | 15 | polySurface1005 |
| 0x2dd872 | 15 | polySurface1006 |
| 0x2dd882 | 15 | polySurface1007 |
| 0x2dd892 | 9 | jail_roof |
| 0x2dd8a0 | 13 | B-Brother...? |
| 0x2dd8ae | 20 | Don't tell me he's-- |
| 0x2dd8c3 | 16 | ...Kuon, please. |
| 0x2dd8d4 | 10 | Of course. |
| 0x2dd8df | 49 | After entering the cell, Kuon silently examines\n |
| 0x2dd911 | 40 | Oshtor for a moment... and sighs softly. |
| 0x2dd93a | 38 | It's all right. He's just unconscious. |
| 0x2dd961 | 6 | Ah...! |
| 0x2dd968 | 17 | Thank goodness... |
| 0x2dd97a | 16 | ...Ah... Nekone. |
| 0x2dd98b | 43 | Oshtor stirs, managing only a raspy murmur. |
| 0x2dd9b7 | 16 | Dear brother...! |
| 0x2dd9c8 | 48 | Nekone pulls Oshtor in a tight embrace without\n |
| 0x2dd9f9 | 33 | even bothering to wipe her tears. |
| 0x2dda1b | 27 | Haku, everyone... You came. |
| 0x2dda37 | 33 | Yeah, we sure did. Can you stand? |
| 0x2dda59 | 29 | Yes... We must... make haste. |
| 0x2dda77 | 10 | door_close |
| 0x2dda82 | 45 | We unbind him from the chains, and lend him\n |
| 0x2ddab0 | 26 | a hand as he slowly rises. |
| 0x2ddacb | 55 | Below his ragged clothes, we can see reddened stripes\n |
| 0x2ddb03 | 45 | and wounds from the lashes covering his body. |
| 0x2ddb31 | 40 | He... withstood all that pain up to now? |
| 0x2ddb5a | 47 | Nekone hastens to Oshtor's side in an attempt\n |
| 0x2ddb8a | 22 | to support his weight. |
| 0x2ddba1 | 47 | Oshtor looks down at her, his eyes softening,\n |
| 0x2ddbd1 | 27 | and gently holds her close. |
| 0x2ddbed | 15 | Dear brother... |
| 0x2ddbfd | 48 | At that, Nekone finally relaxes, the terrified\n |
| 0x2ddc2e | 46 | tension draining from her expression and body. |
| 0x2ddc5d | 48 | Drink this. It'll only be a temporary fix, but\n |
| 0x2ddc8e | 29 | it should help with the pain. |
| 0x2ddcac | 49 | Kuon takes out a pouch of medicine and hands it\n |
| 0x2ddcde | 10 | to Oshtor. |
| 0x2ddce9 | 16 | Ah... My thanks. |
| 0x2ddcfa | 50 | If we had the time, I would've preferred to give\n |
| 0x2ddd2d | 23 | you proper treatment... |
| 0x2ddd45 | 51 | No need. I can already feel the medicine working.\n |
| 0x2ddd79 | 46 | But we must move swiftly--Her Highness is in\n |
| 0x2ddda8 | 13 | grave danger. |
| 0x2dddb6 | 49 | We know. Oshtor, do you have any idea where the\n |
| 0x2ddde8 | 18 | princess would be? |
| 0x2dddfb | 47 | It's only a matter of time until they realize\n |
| 0x2dde2b | 50 | we're here. We don't have the luxury of searching. |
| 0x2dde5e | 50 | Her Highness's sleeping quarters are at the apex\n |
| 0x2dde91 | 52 | of the innermost building. I know... she is there... |
| 0x2ddec6 | 50 | At my nod, Oshtor puts all his weight on his own\n |
| 0x2ddef9 | 32 | legs, and tries to walk forward. |
| 0x2ddf1a | 53 | Dear brother! You must not push yourself like that... |
| 0x2ddf50 | 42 | She's right. You can leave the rescue of\n |
| 0x2ddf7b | 19 | Her Highness to us. |
| 0x2ddf8f | 52 | That's right. You need to escape quickly, brother... |
| 0x2ddfc4 | 29 | I am sorry, but... I must go. |
| 0x2ddfe2 | 53 | Whether or not my limbs can move, I will go to her.\n |
| 0x2de018 | 41 | Even if I must crawl, I will go to her... |
| 0x2de042 | 45 | Even Oshtor--stoic, calm, composed Oshtor--\n |
| 0x2de070 | 28 | has totally lost his cool... |
| 0x2de08d | 47 | Guess that just shows how bad the situation's\n |
| 0x2de0bd | 7 | gotten. |
| 0x2de0c5 | 15 | Lady-in-waiting |
| 0x2de0d5 | 50 | Um... If that is the case, I do not mind helping\n |
| 0x2de108 | 9 | you walk. |
| 0x2de112 | 21 | Please, take my hand. |
| 0x2de128 | 11 | You are...? |
| 0x2de134 | 44 | My apologies for the belated introduction.\n |
| 0x2de161 | 42 | I am the one in charge of Her Highness's\n |
| 0x2de18c | 11 | well-being. |
| 0x2de198 | 47 | She's the one who told us you were being held\n |
| 0x2de1c8 | 15 | in this prison. |
| 0x2de1d8 | 47 | I am truly sorry, Lord Oshtor. This is all my\n |
| 0x2de208 | 8 | fault... |
| 0x2de211 | 52 | Sorry, but I'll have to ask you to save that stuff\n |
| 0x2de246 | 47 | for later. We don't have time to stand around\n |
| 0x2de276 | 12 | apologizing. |
| 0x2de283 | 46 | Uruuru, Saraana, could you do your... thing?\n |
| 0x2de2b2 | 14 | One more time? |
| 0x2de2c1 | 15 | ...As you wish. |
| 0x2de2d1 | 27 | Oshtor, are you OK walking? |
| 0x2de2ed | 45 | If you slow us down, I swear I'm just gonna\n |
| 0x2de31b | 31 | leave you in a ditch somewhere. |
| 0x2de33b | 29 | I would have it no other way. |
| 0x2de359 | 50 | This is how it must be, Nekone. We have no time.\n |
| 0x2de38c | 47 | I would rather fall behind than hinder you all. |
| 0x2de3bc | 24 | ...I will help you walk. |
| 0x2de3d5 | 8 | Nekone-- |
| 0x2de3de | 21 | I WILL help you walk. |
| 0x2de3f4 | 45 | Anju's caretaker also stands beside Oshtor,\n |
| 0x2de422 | 15 | supporting him. |
| 0x2de432 | 40 | I cannot fight like the rest of you...\n |
| 0x2de45b | 46 | So please, allow me to help in this small way. |
| 0x2de48a | 34 | Just let them handle it, Oshtor.\n |
| 0x2de4ad | 46 | Otherwise we'll be wasting all our time here\n |
| 0x2de4dc | 17 | arguing about it. |
| 0x2de4ee | 35 | I suppose so... Thank you, you two. |
| 0x2de512 | 18 | I-It is nothing... |
| 0x2de525 | 23 | You good to go, Oshtor? |
| 0x2de53d | 27 | Yes. Sorry for keeping you. |
| 0x2de559 | 21 | Don't worry about it. |
| 0x2dea1b | 48 | We continue onward to the top of the building,\n |
| 0x2dea4c | 22 | through the dense fog. |
| 0x2dea63 | 51 | We pass by several patrols on the way, but thanks\n |
| 0x2dea97 | 32 | to the barrier, nobody spots us. |
| 0x2deabc | 47 | I sneak a look at Oshtor, walking alongside me. |
| 0x2deaec | 35 | He's definitely not looking good... |
| 0x2deb10 | 37 | His footsteps are heavy and slow...\n |
| 0x2deb36 | 51 | It's like looking at a completely different person. |
| 0x2deb6a | 44 | Oshtor's wounds must be a lot more serious\n |
| 0x2deb97 | 21 | than he's letting on. |
| 0x2debad | 15 | ...Hey, Oshtor. |
| 0x2debbd | 3 | Hm? |
| 0x2debc1 | 38 | Maybe this isn't the best time, but... |
| 0x2debe8 | 46 | It is unlike you to dance around a subject so. |
| 0x2dec17 | 37 | Well, I guess I'll just be blunt...\n |
| 0x2dec3d | 26 | Is the Mikado really dead? |
| 0x2dec58 | 22 | ...Yes. Without doubt. |
| 0x2dec6f | 45 | I have seen my liege's body with my own eyes. |
| 0x2dec9d | 45 | I hear Kiwru and the others' breathing skip\n |
| 0x2deccb | 13 | for a moment. |
| 0x2decd9 | 46 | I'm sure there was a part of them that hoped\n |
| 0x2ded08 | 29 | it wasn't true, like I did... |
| 0x2ded26 | 50 | It is believed that the ones responsible for his\n |
| 0x2ded59 | 33 | death are Lady Honoka and myself. |
| 0x2ded7b | 47 | Yeah. I heard the Mikado's meal was poisoned... |
| 0x2dedab | 46 | So the real culprit is still in the imperial\n |
| 0x2dedda | 50 | capital somewhere, waiting for a chance to strike? |
| 0x2dee0d | 13 | Regardless... |
| 0x2dee1b | 31 | I see. So... he really is gone. |
| 0x2dee3b | 50 | The keeper of lost technology, the man who lived\n |
| 0x2dee6e | 18 | for centuries...\n |
| 0x2dee81 | 22 | My brother... is dead. |
| 0x2dee98 | 33 | And it happened just like that... |
| 0x2deeba | 47 | He just appeared before me as the Mikado, and\n |
| 0x2deeea | 44 | without any warning, he disappeared from me. |
| 0x2def17 | 48 | It's so sudden. I know I should be sad, but...\n |
| 0x2def48 | 35 | why can't I shed any tears for him? |
| 0x2def6c | 50 | I'm sure if he could see me now, he'd just laugh\n |
| 0x2def9f | 42 | and tell me what a heartless brother I am. |
| 0x2defca | 42 | What's certain, at least, is that now...\n |
| 0x2deff5 | 44 | there's no one left who knows about my past. |
| 0x2df022 | 33 | ...The top floor is just ahead.\n |
| 0x2df044 | 22 | We should hurry, Haku. |
| 0x2df05b | 14 | Sure... Right. |
| 0x2df223 | 17 | Uzurushan Soldier |
| 0x2df235 | 43 | The bravest warrior of Uzurusha is eternal! |
| 0x2df261 | 24 | Dammit. Not you again... |
| 0x2df27a | 35 | Almighty overlord, I have returned! |
| 0x2df29e | 50 | And I have come to prove that the brave warriors\n |
| 0x2df2d1 | 46 | of Uzurusha are the bravest of brave warriors! |
| 0x2df300 | 46 | We shall take the title of almighty overlord\n |
| 0x2df32f | 14 | for ourselves! |
| 0x2df33e | 20 | Now then! To battle! |
| 0x2df353 | 51 | I genuinely could not care less. Look, seriously,\n |
| 0x2df387 | 22 | you can HAVE the name. |
| 0x2df548 | 17 | Uzurushan Soldier |
| 0x2df55a | 16 | Gghh... We lost. |
| 0x2df56b | 48 | But I shall not give up! One day I shall prove\n |
| 0x2df59c | 46 | that the warriors of Uzurusha are true brave\n |
| 0x2df5cb | 9 | warriors. |
| 0x2df5d5 | 44 | Until then, you may uphold the name of the\n |
| 0x2df602 | 29 | almighty overlord with pride! |
| 0x2df620 | 34 | Please, take the name. Honestly.\n |
| 0x2df643 | 14 | I do NOT care. |
| 0x2df652 | 21 | Very fitting for you. |
| 0x2df668 | 45 | The almighty bonerlord. Very distinguished.\n |
| 0x2df696 | 39 | It truly embodies the essence of your\n |
| 0x2df6be | 18 | character, master. |
| 0x2df6d1 | 26 | And THAT'S not any better! |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_06.json` com a forma:
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
