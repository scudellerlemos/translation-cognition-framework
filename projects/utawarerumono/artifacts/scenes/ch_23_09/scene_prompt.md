# Cena ch_23_09 — pacote de traducao (242 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `ground.` -> `do chão.` (Man, 11_01)
- `Haku...` -> `Haku...` (Kuon, 11_02)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `on us.` -> `em nós.` (Personagem-UI, 20_06)
- `voice.` -> `voz.` (Garota, 22_08)
- `soon.` -> `em breve.` (Haku, 18_01)
- `now.` -> `já.` (Kuon, 14_04)
- `Hey.` -> `Ei.` (Maroro, 18_01)
- `them!` -> `deles!` (Haku, 15_01)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `Head` -> `Head` (rotulo, 11_03)
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
| 0x29527f | 36 | Whew... We've walked a fair bit now. |
| 0x2952a4 | 40 | Hey, bosslady. About how far are we now? |
| 0x2952cd | 42 | I think we should be seeing the road soon. |
| 0x2952f8 | 42 | This took much longer than we anticipated. |
| 0x295323 | 46 | Well, we can't help it, with these bumpy and\n |
| 0x295352 | 16 | winding roads... |
| 0x295363 | 43 | Perhaps it would behoove us to hurry. Our\n |
| 0x29538f | 44 | progress will stall if we do not arrive by\n |
| 0x2953bc | 10 | nightfall. |
| 0x2953c7 | 45 | Yeah, you're right. Let's pick up the pace,\n |
| 0x2953f5 | 46 | everyone. Gotta get there before it gets dark. |
| 0x295424 | 46 | Just as I try to rally the rest of the group\n |
| 0x295453 | 36 | forward, the twins suddenly stop me. |
| 0x295478 | 5 | Wait. |
| 0x29547e | 49 | Please be careful, Master. Something is drawing\n |
| 0x2954b0 | 5 | near. |
| 0x2954b6 | 8 | What...? |
| 0x2954bf | 44 | At the twins' words, Jachdwalt immediately\n |
| 0x2954ec | 43 | lowers himself down to put his ear to the\n |
| 0x295518 | 7 | ground. |
| 0x295520 | 43 | ...Footsteps. Not just one or two people,\n |
| 0x29554c | 36 | either. Whole lot of 'em on the way. |
| 0x295571 | 16 | Tuskur soldiers? |
| 0x295582 | 9 | Safe bet. |
| 0x29558c | 40 | A sudden anxiety hangs in the air with\n |
| 0x2955b5 | 18 | Jachdwalt's words. |
| 0x2955c8 | 48 | Wh-What do we do? At this rate, we're going to\n |
| 0x2955f9 | 22 | run right into them... |
| 0x295610 | 25 | We should turn back! Now! |
| 0x29562a | 43 | We cannot turn around so easily on such a\n |
| 0x295656 | 14 | narrow road... |
| 0x295665 | 46 | We may easily hide ourselves, but concealing\n |
| 0x295694 | 37 | these carts would be nigh impossible. |
| 0x2956ba | 33 | Then can we... take care of them? |
| 0x2956dc | 45 | Atuy eagerly readies her spear. Faces grim,\n |
| 0x29570a | 46 | Nosuri and Jachdwalt begin drawing their own\n |
| 0x295739 | 8 | weapons. |
| 0x295742 | 48 | Hold on, hold on! We haven't been found out yet. |
| 0x295773 | 36 | I hastily try to calm everyone down. |
| 0x295798 | 44 | The Tuskur army must be using this road to\n |
| 0x2957c5 | 26 | ambush the Yamatan forces. |
| 0x2957e0 | 29 | I'm sorry, Haku... I didn't-- |
| 0x2957fe | 47 | Hey, don't worry. This path was our only shot\n |
| 0x29582e | 43 | anyways, and I'm glad you told us about it. |
| 0x29585a | 7 | Haku... |
| 0x295862 | 42 | The Tuskur army knows this path is here.\n |
| 0x29588d | 50 | I figured there was a chance something like this\n |
| 0x2958c0 | 13 | would happen. |
| 0x2958ce | 28 | Well, ain't that reassurin'. |
| 0x2958eb | 50 | It sounds like you've already got a plan in that\n |
| 0x29591e | 31 | clever head of yours, eh, love? |
| 0x29593e | 43 | I knew it could happen... I just hoped it\n |
| 0x29596a | 22 | wouldn't come to this. |
| 0x295981 | 48 | Kuon, you said that only the locals know about\n |
| 0x2959b2 | 17 | this path, right? |
| 0x2959c4 | 11 | Huh? Yes... |
| 0x2959d0 | 29 | Then... I might have an idea. |
| 0x2959ee | 14 | You do, Haku!? |
| 0x2959fd | 30 | It's gonna be risky, though.\n |
| 0x295a1c | 21 | Listen up, everybody. |
| 0x295a32 | 49 | I'm pretty sure the Tuskur army isn't expecting\n |
| 0x295a64 | 26 | any Yamatans on this path. |
| 0x295a7f | 46 | So their first assumption would be that only\n |
| 0x295aae | 45 | other people from Tuskur would use this road. |
| 0x295adc | 24 | A sound enough theory... |
| 0x295af5 | 45 | Luckily, we're not real soldiers of Yamato.\n |
| 0x295b23 | 48 | No uniforms or anything. We might just be able\n |
| 0x295b54 | 13 | to fool them. |
| 0x295b62 | 47 | Even if we defeat them, it won't make our job\n |
| 0x295b92 | 49 | any easier. Let's hide our weapons, and play it\n |
| 0x295bc4 | 5 | cool! |
| 0x295bca | 46 | As I'm explaining all this, I sneak a glance\n |
| 0x295bf9 | 8 | at Kuon. |
| 0x295c02 | 45 | I want to avoid bloodshed wherever possible\n |
| 0x295c30 | 5 | here. |
| 0x295c36 | 45 | Gotcha. Guess we'll go with the boss's plan\n |
| 0x295c64 | 11 | then, yeah? |
| 0x295c70 | 47 | It is the best course of action we've come up\n |
| 0x295ca0 | 12 | with so far. |
| 0x295cad | 48 | Yes. If we can get through this without having\n |
| 0x295cde | 46 | to fight, that would be the best outcome for\n |
| 0x295d0d | 4 | all. |
| 0x295d12 | 46 | But do you really think this is going to work? |
| 0x295d41 | 47 | Well if it doesn't, then we just take care of\n |
| 0x295d71 | 12 | them, right? |
| 0x295d7e | 12 | I-I suppose. |
| 0x295d8f | 49 | Still feeling uneasy, we shift the carts to the\n |
| 0x295dc1 | 40 | roadside. Eventually, in the distance... |
| 0x295dea | 24 | Just like we expected... |
| 0x295e03 | 31 | Fully-armed soldiers of Tuskur. |
| 0x295e23 | 50 | They idly chat among themselves as they close in\n |
| 0x295e56 | 6 | on us. |
| 0x295e5d | 48 | Judging by how relaxed they are, they might be\n |
| 0x295e8e | 46 | on patrol or just heading to an assigned post. |
| 0x295ebd | 47 | Maybe their guards will be down if they don't\n |
| 0x295eed | 46 | expect the Yamatans to have found this path... |
| 0x295f1c | 50 | They seem too deep in conversation at first, but\n |
| 0x295f4f | 47 | then they notice us clustered around the carts. |
| 0x295f7f | 14 | Tuskur soldier |
| 0x295f8e | 26 | Hm? Who are all of you...? |
| 0x295fa9 | 46 | The man at the front, their apparent leader,\n |
| 0x295fd8 | 28 | eyes us warily as he speaks. |
| 0x295ff5 | 36 | Argh, just gonna have to wing it...! |
| 0x29601a | 45 | I hunch slightly and put my hands together,\n |
| 0x296048 | 45 | striding toward their leader with a booming\n |
| 0x296076 | 6 | voice. |
| 0x29607d | 51 | Heh hyeh hyeh! A most delightful and rejuvenating\n |
| 0x2960b1 | 28 | morning to you, my good sir! |
| 0x2960ce | 20 | And you would be...? |
| 0x2960e3 | 49 | Y-Yes, ah, the big cheeses over at the fortress\n |
| 0x296115 | 47 | needed supplies delivered, so we're on the job! |
| 0x296145 | 17 | The fortress, hm? |
| 0x296157 | 50 | He seems to understand whatever I'm referencing,\n |
| 0x29618a | 43 | even though it was just a shot in the dark. |
| 0x2961b6 | 47 | Ah, then you must be from the nearby village... |
| 0x2961e6 | 25 | Y-Yes, there you have it! |
| 0x296200 | 46 | That explains it then. Fine work you're doing. |
| 0x29622f | 41 | Their leader gives me an approving nod.\n |
| 0x296259 | 43 | It doesn't look like he doubts me at all... |
| 0x296285 | 38 | He's even praising us for our efforts. |
| 0x2962ac | 47 | I'm sorry to put you through all this. Still,\n |
| 0x2962dc | 47 | we should have them driven back to their land\n |
| 0x29630c | 5 | soon. |
| 0x296312 | 36 | Th-That is most relieving to hear!\n |
| 0x296337 | 43 | But I heard that the Yamatan soldiers are\n |
| 0x296363 | 16 | really strong... |
| 0x296374 | 43 | It seems they believed us to be backwater\n |
| 0x2963a0 | 42 | bumpkins. They were all talk and no skill. |
| 0x2963cb | 49 | Some have genuine ability, but the majority are\n |
| 0x2963fd | 45 | mere novices. And their commander is simply\n |
| 0x29642b | 9 | hopeless. |
| 0x296435 | 9 | Hopeless? |
| 0x29643f | 50 | What was his name again? Something like Deppa...\n |
| 0x296472 | 34 | Dekopachi, maybe, or Degarashi...? |
| 0x296495 | 46 | Wait, Dekopompo...!? I mean--I believe there\n |
| 0x2964c4 | 32 | was a general by such, er, name. |
| 0x2964e5 | 48 | Yes, that's it! You certainly are well-informed. |
| 0x296516 | 39 | Anyhow, his name doesn't really matter. |
| 0x29653e | 26 | Th-That was a close one.\n |
| 0x296559 | 27 | Almost blew my cover there. |
| 0x296575 | 47 | So this Dekopachi guy yells out his name like\n |
| 0x2965a5 | 38 | an idiot when he shows up in battle.\n |
| 0x2965cc | 25 | Everyone knows it by now. |
| 0x2965e6 | 42 | Well, you clearly haven't remembered it... |
| 0x296611 | 44 | Yes, the commander is a lost cause. I know\n |
| 0x29663e | 48 | they're the enemy, but you really have to pity\n |
| 0x29666f | 15 | his soldiers... |
| 0x29667f | 50 | We just provoke him, and he charges blindly into\n |
| 0x2966b2 | 46 | our hidden mud pits. It's worked three times\n |
| 0x2966e1 | 4 | now. |
| 0x2966e6 | 15 | I-Is that so... |
| 0x2966f6 | 45 | He just always falls for it! We're honestly\n |
| 0x296724 | 48 | starting to wonder if it's part of some scheme\n |
| 0x296755 | 7 | of his. |
| 0x29675d | 36 | He is a disgrace to all of Yamato... |
| 0x296782 | 46 | I don't know why, but... I feel like crying... |
| 0x2967b1 | 46 | They should be running out of supplies soon,\n |
| 0x2967e0 | 42 | and their patience is likely running thin. |
| 0x29680b | 48 | They may go for an all-out assault if they get\n |
| 0x29683c | 38 | too desperate. Be careful on your way. |
| 0x296863 | 22 | Th-Thank you. We will. |
| 0x29687a | 50 | As I nod in agreement, I feel something prodding\n |
| 0x2968ad | 12 | at my knees. |
| 0x2968ba | 48 | I look over to see Nekone, trying to send me a\n |
| 0x2968eb | 28 | message with her eyes alone. |
| 0x296908 | 47 | ...Yeah, I know. Staying here won't do us any\n |
| 0x296938 | 46 | good. We should get a move on before someone\n |
| 0x296967 | 9 | slips up. |
| 0x296971 | 46 | W-Well, we will be going on our way now, then. |
| 0x2969a0 | 11 | Katana_mesh |
| 0x2969ad | 9 | Saya_mesh |
| 0x2969b7 | 45 | I end the conversation and turn back to the\n |
| 0x2969e5 | 7 | others. |
| 0x2969ed | 48 | Jachdwalt sees my intent, and goes to push the\n |
| 0x296a1e | 30 | carts back on the road, when-- |
| 0x296a3d | 4 | Hey. |
| 0x296a42 | 47 | I jump a little, not expecting to be directly\n |
| 0x296a72 | 10 | called to. |
| 0x296a7d | 34 | Y-Yes? Is there something else...? |
| 0x296aa0 | 44 | I look back in fear, but the leader stands\n |
| 0x296acd | 25 | there with an easy smile. |
| 0x296ae7 | 47 | The road here is pretty uneven. It'll be hard\n |
| 0x296b17 | 47 | setting the carts on your own. Men, we assist\n |
| 0x296b47 | 5 | them! |
| 0x296b4d | 45 | N-No need, my good sir. I would not want to\n |
| 0x296b7b | 18 | get in your way... |
| 0x296b8e | 45 | It's fine. Don't worry about it--we need to\n |
| 0x296bbc | 42 | help each other when we're in need, right? |
| 0x296be7 | 47 | The soldiers ignore my words and approach the\n |
| 0x296c17 | 43 | carts... but one of them pauses, sounding\n |
| 0x296c43 | 7 | unsure. |
| 0x296c4b | 6 | Hm...? |
| 0x296c52 | 45 | I follow the soldier's gaze to Kuon, who is\n |
| 0x296c80 | 47 | determinedly looking in the opposite direction. |
| 0x296cb0 | 10 | Wh--Kuon!! |
| 0x296cbb | 32 | She's acting way too suspicious. |
| 0x296cdc | 48 | And of course, the soldier walks over to where\n |
| 0x296d0d | 42 | Kuon is, trying to get a look at her face. |
| 0x296d38 | 31 | I swear I've seen you before... |
| 0x296d58 | 48 | Kuon's neck strains slightly as she avoids the\n |
| 0x296d89 | 28 | peering eyes of the soldier. |
| 0x296da6 | 43 | The soldier continues to step around her,\n |
| 0x296dd2 | 38 | trying to get a good look at her face. |
| 0x296df9 | 45 | Gradually, the other Tuskur soldiers notice\n |
| 0x296e27 | 19 | this strange scene. |
| 0x296e3b | 45 | Hey, I know she's pretty, but that's enough\n |
| 0x296e69 | 19 | bothering the lady! |
| 0x296e7d | 44 | This is why you never get any girls, y'know! |
| 0x296eaa | 33 | Th-That's not what this is about! |
| 0x296ecc | 50 | The soldier reddens as the other men in the unit\n |
| 0x296eff | 41 | taunt him, and he yells back defensively. |
| 0x296f29 | 43 | I swear I've seen her before... Not in my\n |
| 0x296f55 | 45 | village, but at a festival after I moved to\n |
| 0x296f83 | 15 | the capital...? |
| 0x296f93 | 46 | He pauses a moment longer, still in thought,\n |
| 0x296fc2 | 47 | but seems to recall something in a sudden jolt. |
| 0x296ff2 | 4 | Head |
| 0x296ff7 | 31 | I-I remember now! Are you--!?\n |
| 0x297017 | 21 | But... you CAN'T be-- |
| 0x29702d | 7 | Tch...! |
| 0x297035 | 9 | K-Kuon... |
| 0x29703f | 44 | Sh-She just chopped him right in the neck... |
| 0x29706c | 44 | He's not dead, but he's definitely out cold. |
| 0x297099 | 42 | Kuon hastily crouches down, and sits the\n |
| 0x2970c4 | 45 | unconscious soldier up as she begins to rub\n |
| 0x2970f2 | 25 | his shoulders vigorously. |
| 0x29710c | 46 | A-Aha... Ahahaha... H-His shoulders looked a\n |
| 0x29713b | 26 | little stiff, you know...? |
| 0x297156 | 50 | But the soldier's eyes have completely rolled up\n |
| 0x297189 | 40 | into his head, his body flopping limply. |
| 0x2971b2 | 11 | Ah... um... |
| 0x2971be | 48 | Everyone's expression is frozen. The area goes\n |
| 0x2971ef | 18 | completely silent. |
| 0x297202 | 48 | The first one to snap back to reality is their\n |
| 0x297233 | 47 | leader. He shouts, pointing an accusing finger. |
| 0x297263 | 34 | Y-You're from Yamato, aren't you!? |
| 0x297286 | 15 | D-Dear sister!? |
| 0x297296 | 48 | Hah... I suppose we could not deceive the keen\n |
| 0x2972c7 | 48 | eyes of Tuskur warriors after all! Well spotted! |
| 0x2972f8 | 46 | Hee hee! Finally, things are picking up a bit. |
| 0x297327 | 31 | It would seem she has given up. |
| 0x297347 | 22 | "Well spotted" my ASS! |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_09.json` com a forma:
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
