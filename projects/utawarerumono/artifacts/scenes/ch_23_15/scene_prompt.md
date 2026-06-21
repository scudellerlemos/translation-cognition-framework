# Cena ch_23_15 — pacote de traducao (153 linhas)

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
| Benawi | Personagem | Benawi | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurou | Personagem | Kurou | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
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
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Zzz... zzz...` -> `Zzz... zzz...` (Protagonista, 19_02)
- `What?` -> `Que?` (Haku, 12_02)
- `safe.` -> `seguro.` (Haku, 17_04)
- `you.` -> `isso.` (Nekone, 15_03)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `I...` -> `Eu...` (Nekone, 14_04)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `I... see...` -> `Eu... entendo...` (Kuon, 11_02)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `...Thank you.` -> `...Obrigado.` (Haku, 23_11)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `now.` -> `já.` (Kuon, 14_04)
- `them.` -> `deles.` (Kuon, 11_05)
- `Miss Munechika...` -> `Senhorita Munechika...` (Haku(?) ou Nosuri, 23_02)
- `return.` -> `retirada.` (Zeguni, 20_20)
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
| 0x2b9726 | 13 | Zzz... zzz... |
| 0x2b9734 | 34 | Look at Nekone. She must be tired. |
| 0x2b9757 | 47 | Thanks for letting her ride with you, Rulutieh. |
| 0x2b9787 | 44 | Oh, it's no problem at all... Cocopo seems\n |
| 0x2b97b4 | 24 | happy to have her along. |
| 0x2b97d2 | 48 | We should be there soon. The fortress is right\n |
| 0x2b9803 | 16 | over this ridge. |
| 0x2b9814 | 47 | Hee. Nekone's a real cutie when she's asleep,\n |
| 0x2b9844 | 46 | huh, Kiwru? You keep stealing little glances\n |
| 0x2b9873 | 7 | at her. |
| 0x2b987b | 18 | Huh!? A-Ah, well-- |
| 0x2b988e | 6 | Zzz... |
| 0x2b9895 | 32 | The sun's getting awfully low... |
| 0x2b98b6 | 44 | Yeah. Hope Munechika made it back all right. |
| 0x2b98e3 | 44 | That man--Kurou, was it? His parting words\n |
| 0x2b9910 | 39 | were... perturbing, wouldn't you agree? |
| 0x2b9938 | 42 | Yeah. He mentioned something about being\n |
| 0x2b9963 | 25 | "too late" for something. |
| 0x2b997d | 10 | ...He did. |
| 0x2b9988 | 11 | Kurou, huh. |
| 0x2b9994 | 43 | He was calling Kuon "my lady" like he was\n |
| 0x2b99c0 | 27 | pretty familiar with her... |
| 0x2b99dc | 44 | What's his relationship with Kuon, anyway?\n |
| 0x2b9a09 | 23 | Who exactly... IS Kuon? |
| 0x2b9a21 | 48 | I'm burning to know, but now doesn't feel like\n |
| 0x2b9a52 | 16 | the time to ask. |
| 0x2b9a63 | 43 | The others are probably thinking the same\n |
| 0x2b9a8f | 45 | thing, but nobody gives voice to the uneasy\n |
| 0x2b9abd | 9 | thoughts. |
| 0x2b9ac7 | 48 | Hey, boss. Isn't the fortress looking a little\n |
| 0x2b9af8 | 13 | weird to you? |
| 0x2b9b06 | 5 | What? |
| 0x2b9b0c | 47 | Oh, dear. It's awfully quiet. And there's no... |
| 0x2b9b3c | 50 | No fires, yeah. Night's falling, but I don't see\n |
| 0x2b9b6f | 19 | so much as a torch. |
| 0x2b9b83 | 47 | We should hurry. I've got a bad feeling about\n |
| 0x2b9bb3 | 43 | this. Nosuri, Ougi, could you scope it out? |
| 0x2b9bdf | 48 | Understood. Ougi, with me. Let's see what's up\n |
| 0x2b9c10 | 6 | ahead. |
| 0x2b9c17 | 17 | Right behind you. |
| 0x2b9c29 | 20 | ...Completely empty? |
| 0x2b9c3e | 47 | What the hell is going on? Why'd they abandon\n |
| 0x2b9c6e | 13 | the fortress? |
| 0x2b9c7c | 38 | We searched it front and back, Haku.\n |
| 0x2b9ca3 | 19 | The place is empty. |
| 0x2b9cb7 | 33 | All the footmen's tents, as well. |
| 0x2b9cd9 | 34 | Hey, did the enemy get here first? |
| 0x2b9cfc | 51 | I don't think so. There are no signs of a struggle. |
| 0x2b9d30 | 39 | Could it be they abandoned the tower?\n |
| 0x2b9d58 | 36 | Sounded the retreat for some reason? |
| 0x2b9d7d | 39 | Th-Then... did they... leave us behind? |
| 0x2b9da5 | 47 | Quite possible, but this is far too sudden to\n |
| 0x2b9dd5 | 24 | be an organized retreat. |
| 0x2b9dee | 40 | Uruuru, Saraana. Can you sense anything? |
| 0x2b9e17 | 21 | ...Something nearing. |
| 0x2b9e2d | 39 | Somebody appears to be heading our way. |
| 0x2b9e55 | 23 | Is that you, Lord Haku? |
| 0x2b9e6d | 11 | Munechika-- |
| 0x2b9e79 | 47 | Lord Haku, all of you... I am glad to see you\n |
| 0x2b9ea9 | 5 | safe. |
| 0x2b9eaf | 48 | And you as well... We were quite worried about\n |
| 0x2b9ee0 | 4 | you. |
| 0x2b9ee5 | 50 | You look like you've been through a tough fight.\n |
| 0x2b9f18 | 46 | Seems like you pulled through somehow, though. |
| 0x2b9f47 | 16 | ...Yes, somehow. |
| 0x2b9f58 | 48 | You did good. Our plan wouldn't have succeeded\n |
| 0x2b9f89 | 26 | if not for your diversion. |
| 0x2b9fa4 | 42 | It just gladdens me to see you unharmed.\n |
| 0x2b9fcf | 44 | Unfortunately, we cannot continue this war\n |
| 0x2b9ffc | 11 | any longer. |
| 0x2ba008 | 7 | Huh...? |
| 0x2ba010 | 35 | Something happened, I'm guessing?\n |
| 0x2ba034 | 21 | Could Benawi have...? |
| 0x2ba04a | 35 | Munechika, why isn't anyone here?\n |
| 0x2ba06e | 43 | Where are the other generals, the soldiers? |
| 0x2ba09e | 18 | Lady Munechika...? |
| 0x2ba0b1 | 38 | We've received word from the mainland. |
| 0x2ba0d8 | 43 | Ah... A-Are you all right? You look pale... |
| 0x2ba104 | 4 | I... |
| 0x2ba109 | 39 | My liege... has passed from this world. |
| 0x2ba131 | 7 | ...Huh? |
| 0x2ba139 | 10 | Passed...? |
| 0x2ba144 | 36 | My brother... The Mikado is... dead? |
| 0x2ba169 | 49 | Th-That... No, that can't be. This is some kind\n |
| 0x2ba19b | 15 | of joke, right? |
| 0x2ba1ab | 11 | I... see... |
| 0x2ba1b7 | 46 | No, that can't... The Mikado, he can't just... |
| 0x2ba1e6 | 49 | That's... That's impossible. The Mikado cannot... |
| 0x2ba218 | 42 | There's no way the Mikado could be gone!\n |
| 0x2ba243 | 16 | That's not true! |
| 0x2ba254 | 43 | Sh-She's right. There must be some mistake. |
| 0x2ba280 | 28 | My liege is akin to a god... |
| 0x2ba29d | 46 | He... He looked just fine last time I saw him. |
| 0x2ba2cc | 47 | And you got this from a reliable source? This\n |
| 0x2ba2fc | 36 | ain't the time for miscommunication. |
| 0x2ba321 | 21 | Yeah, that's right... |
| 0x2ba337 | 42 | It's also possible it's deliberate false\n |
| 0x2ba362 | 38 | information. We've been cut off from\n |
| 0x2ba389 | 25 | communications until now. |
| 0x2ba3a3 | 43 | No. The message came through Lord Raiko's\n |
| 0x2ba3cf | 42 | personal network. There's no mistaking it. |
| 0x2ba3fa | 49 | I hardly want to believe such a thing, but it's\n |
| 0x2ba42c | 23 | the indisputable truth. |
| 0x2ba444 | 19 | It... It cannot be. |
| 0x2ba458 | 5 | Ah... |
| 0x2ba45e | 10 | Rulutieh!? |
| 0x2ba469 | 46 | Rulutieh sways, then crumples to the ground,\n |
| 0x2ba498 | 47 | fainting. I barely manage to catch her in time. |
| 0x2ba4c8 | 47 | Lords Raiko and Dekopompo have withdrawn with\n |
| 0x2ba4f8 | 45 | their troops. Of the Pillars, only I remain\n |
| 0x2ba526 | 5 | here. |
| 0x2ba52c | 47 | So you've been waiting for us this entire time. |
| 0x2ba55c | 38 | Well, I could hardly leave you behind. |
| 0x2ba583 | 13 | ...Thank you. |
| 0x2ba591 | 44 | I am merely fulfilling my duties. All that\n |
| 0x2ba5be | 46 | remains is for you to be gone from this place. |
| 0x2ba5ed | 5 | Haku? |
| 0x2ba5f3 | 25 | Huh? O-Oh... Yeah, right. |
| 0x2ba60d | 50 | Our priority right now is to get back to Yamato.\n |
| 0x2ba640 | 44 | We can figure out how to address this from\n |
| 0x2ba66d | 6 | there. |
| 0x2ba674 | 41 | Everyone. We're heading back immediately. |
| 0x2ba69e | 49 | All right, all of you. Up on your feet. You can\n |
| 0x2ba6d0 | 46 | mourn later. Mopin' won't fix anything right\n |
| 0x2ba6ff | 4 | now. |
| 0x2ba704 | 39 | Miss Munechika, you should come with... |
| 0x2ba72c | 45 | I cannot. I will remain here and waylay the\n |
| 0x2ba75a | 23 | enemy as best I'm able. |
| 0x2ba772 | 13 | ...Munechika? |
| 0x2ba780 | 43 | They'll have already discerned that we've\n |
| 0x2ba7ac | 20 | abandoned the field. |
| 0x2ba7c1 | 49 | Someone must remain behind to hold them at bay,\n |
| 0x2ba7f3 | 48 | else they'll run our troops down and slaughter\n |
| 0x2ba824 | 5 | them. |
| 0x2ba82a | 46 | I am the Guardian. My duty to my liege is to\n |
| 0x2ba859 | 8 | protect. |
| 0x2ba862 | 17 | Miss Munechika... |
| 0x2ba874 | 46 | Go now. And do not worry--I hardly intend to\n |
| 0x2ba8a3 | 29 | forfeit my life to these men. |
| 0x2ba8c1 | 46 | Understood. We'll be looking forward to your\n |
| 0x2ba8f0 | 7 | return. |
| 0x2ba8f8 | 33 | C'mon, let's go. All of you. Now. |
| 0x2ba91a | 13 | ...Very well. |
| 0x2ba928 | 22 | Nekone, can you stand? |
| 0x2ba93f | 19 | Here, take my hand. |
| 0x2ba953 | 25 | I-I am capable on my own. |
| 0x2ba96d | 23 | Rulie? You OK, darling? |
| 0x2ba985 | 33 | Yes... Thank you for you concern. |
| 0x2ba9a7 | 49 | All right. Let's organize our stuff and get out\n |
| 0x2ba9d9 | 8 | of here. |
| 0x2ba9e2 | 36 | ...Please stay safe, Miss Munechika. |
| 0x2baa07 | 28 | Worry not. We'll meet again. |
| 0x2baa24 | 47 | I look forward to seeing you at the Hakurokaku. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_15.json` com a forma:
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
