# Cena ch_14_09 — pacote de traducao (591 linhas)

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
| amam | Item | amam | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mausoleum | Local | Mausoleu | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Omuchakko | Local | Omuchakko | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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
### Oshtor — criticality: high
- Oshtor — `voice_criticality: high`. = Ukon até 13_08 (ver spoiler_ledger). Registro formal, nobre, comedido; General da Direita. Antes do reveal, traduzir como o mercenário "Ukon" (espirituoso, informal) — NÃO antecipar a pompa de general
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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `Haku...` -> `Haku...` (Kuon, root)
- `anyway.` -> `de agora.` (Ougi, 13_08)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Did you say something?` -> `Disse alguma coisa?` (Haku, 13_09)
- `Just where do you think you're going?` -> `Para onde você acha que está indo?` (Kuon, 14_03)
- `for a bit.` -> `um pouco.` (Ukon, 13_02)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `capital.` -> `imperial.` (Kuon, 12_04)
- `Wow...` -> `Nossa...` (Kuon, 14_03)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `I think.` -> `acho.` (Kuon, 12_11)
- `Huh? Oh...` -> `Hein? Ah...` (Rulutieh, 14_04)
- `nearby.` -> `perto.` (Ukon, 12_15)
- `Is something wrong?` -> `Algum problema?` (Kuon, 11_06)
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

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x94ba6 | 12 | *Yaaaawn*... |
| 0x94bb3 | 47 | I wanted to sleep a little more, but I try to\n |
| 0x94be3 | 40 | stifle my yawn, ambling to the entrance. |
| 0x94c0c | 39 | Sorry to keep you waiting, dear sister. |
| 0x94c34 | 29 | Thanks for doing this for us. |
| 0x94c52 | 39 | O-Oh no, anything for you, dear sister. |
| 0x94c7a | 14 | D-Dear sister? |
| 0x94c89 | 49 | The odd way Kuon and Nekone are addressing each\n |
| 0x94cbb | 18 | other startles me. |
| 0x94cce | 50 | The two pause and look at me, as though noticing\n |
| 0x94d01 | 12 | my reaction. |
| 0x94d0e | 7 | Haku?\n |
| 0x94d16 | 13 | What's wrong? |
| 0x94d24 | 46 | You guys... aren't long-lost sisters, are you? |
| 0x94d53 | 7 | Haku... |
| 0x94d5b | 48 | Oh, so the purpose of your journey was to find\n |
| 0x94d8c | 49 | your younger sister... Well, that'd make sense,\n |
| 0x94dbe | 7 | anyway. |
| 0x94dc6 | 45 | What inane gibberish are you spouting now...? |
| 0x94df4 | 39 | Hmhm. I'm surprised you figured it out. |
| 0x94e1c | 7 | ...Huh? |
| 0x94e24 | 42 | Yes, it's true! All along, Nekone was my\n |
| 0x94e4f | 24 | long-lost little sister. |
| 0x94e68 | 47 | Kuon pulls Nekone dramatically into her arms.\n |
| 0x94e98 | 44 | Nekone looks... startled by this plot twist. |
| 0x94ec5 | 46 | Nekone... I won't ever let you go, ever again. |
| 0x94ef4 | 21 | Er, d-dear sister...? |
| 0x94f0a | 48 | Nekone blushes slightly as Kuon rubs her cheek\n |
| 0x94f3b | 12 | against her. |
| 0x94f48 | 22 | U-Um... I, ah, I am... |
| 0x94f5f | 35 | And... that's enough joking around. |
| 0x94f87 | 46 | As Kuon chuckles, shifting back from Nekone,\n |
| 0x94fb6 | 24 | she starts explaining... |
| 0x94fcf | 45 | You see, Nekone and I promised ourselves to\n |
| 0x94ffd | 31 | each other in sworn sisterhood. |
| 0x9501d | 26 | Promised to each other...? |
| 0x95038 | 41 | ...That has... a suspicious ring to it.\n |
| 0x95062 | 37 | In a "no minors allowed" kind of way. |
| 0x95088 | 45 | Somehow, I feel he is thinking of something\n |
| 0x950b6 | 16 | reprehensible... |
| 0x950c7 | 45 | You could say that though we aren't related\n |
| 0x950f5 | 49 | by blood, we will remain devoted to each other,\n |
| 0x95127 | 17 | come what may...  |
| 0x95139 | 48 | Simply put, it's a promise between us to trust\n |
| 0x9516a | 50 | and treat each other like we are sisters by blood. |
| 0x9519d | 44 | Ahaha... I've always wanted a little sister. |
| 0x951ca | 50 | Kuon pulls Nekone close once again, and hugs her\n |
| 0x951fd | 41 | more tightly than she did the first time. |
| 0x95227 | 16 | D-Dear sister... |
| 0x95238 | 47 | I-I also...wanted a... like you, dear sister... |
| 0x95268 | 22 | Did you say something? |
| 0x9527f | 20 | N-No, it is nothing. |
| 0x95294 | 51 | I watch the two's antics. They may not be related\n |
| 0x952c8 | 50 | by blood, but I sense a beautiful sisterly love... |
| 0x952fb | 40 | ...Yep. Friendship is a beautiful thing. |
| 0x95324 | 46 | I have a feeling he is thinking of something\n |
| 0x95353 | 22 | reprehensible again... |
| 0x9536a | 42 | How dare she impugn my clear conscience.\n |
| 0x95395 | 23 | My pure, innocent mind? |
| 0x953ad | 49 | Um... Everyone... I'm sorry... to have kept you\n |
| 0x953df | 10 | waiting... |
| 0x953ea | 39 | Don't worry, it wasn't a bother at all. |
| 0x95412 | 42 | Lady Rulutieh is here, so shall we be off? |
| 0x9543d | 47 | Kuon and Rulutieh follow behind Nekone as she\n |
| 0x9546d | 31 | strides out the front entrance. |
| 0x9548d | 18 | Yeah, have fun. \n |
| 0x954a0 | 11 | *Yaaawn*... |
| 0x954ac | 49 | The three girls seem excited, so I doubt they'd\n |
| 0x954de | 47 | notice if I went missing... Time for a n--URGH! |
| 0x9550e | 47 | I stumble backwards, like I got myself caught\n |
| 0x9553e | 13 | on something. |
| 0x9554c | 52 | As I look for the cause, I notice Kuon has grabbed\n |
| 0x95581 | 45 | me by the back of my neck, smiling ominously. |
| 0x955af | 37 | Just where do you think you're going? |
| 0x955d5 | 48 | Where? I was just... going to go back to sleep\n |
| 0x95606 | 10 | for a bit. |
| 0x95611 | 51 | What are you saying? The plan was that you'd come\n |
| 0x95645 | 21 | along with us, right? |
| 0x9565b | 50 | Oh, well, I figured I'd be in the way. This time\n |
| 0x9568e | 33 | around, you three girls should... |
| 0x956b0 | 47 | Do you intend to abandon us, then? After I so\n |
| 0x956e0 | 44 | eagerly came here to show everyone around... |
| 0x9570d | 50 | I see. Rulutieh was so looking forward to seeing\n |
| 0x95740 | 25 | the sights together, too. |
| 0x9575a | 19 | N-No... I didn't... |
| 0x9576e | 22 | Rulutieh's face falls. |
| 0x95785 | 52 | O-Oh no, I thought I'd... hang back a bit, is all.\n |
| 0x957ba | 44 | I was looking forward to it too! Really. OK? |
| 0x957e7 | 5 | OK... |
| 0x957ed | 41 | Urgh, I can't handle that smile... That\n |
| 0x95817 | 49 | "I-believe-in-you" expression is making me feel\n |
| 0x95849 | 12 | so guilty... |
| 0x95856 | 37 | Then again, those scornful gazes of\n |
| 0x9587c | 44 | "I-don't-believe-in-you-at-all" aren't any\n |
| 0x958a9 | 9 | better... |
| 0x958b3 | 46 | There was a little struggle at first, but we\n |
| 0x958e2 | 45 | make our way south on the capital's massive\n |
| 0x95910 | 13 | central road. |
| 0x9591e | 47 | I've seen it before, but the Imperial Capital\n |
| 0x9594e | 32 | really is an impressive sight... |
| 0x9596f | 52 | Y-Yes... It's so large that it makes my head swim... |
| 0x959a4 | 49 | This capital is in a basin-like area surrounded\n |
| 0x959d6 | 50 | by mountains. Its size certainly boggles the mind. |
| 0x95a09 | 45 | But even more amazing than the size of this\n |
| 0x95a37 | 22 | capital is its layout. |
| 0x95a4e | 46 | Judging by the map, the capital is a perfect\n |
| 0x95a7d | 49 | rectangle with carefully laid out perpendicular\n |
| 0x95aaf | 6 | roads. |
| 0x95ab6 | 50 | Just who exactly designed this amazing capital...? |
| 0x95ae9 | 48 | This capital was formed hundreds of years ago,\n |
| 0x95b1a | 37 | by the Mikado, the founder of Yamato. |
| 0x95b40 | 51 | I see. Whoever was the Mikado back then must have\n |
| 0x95b74 | 34 | had a real knack for architecture. |
| 0x95b97 | 50 | What nonsense are you spewing now? The Mikado of\n |
| 0x95bca | 44 | today is the same Mikado we have always had. |
| 0x95bf7 | 6 | ...Hm? |
| 0x95bfe | 53 | I tilt my head in confusion at Nekone's interjection. |
| 0x95c34 | 49 | Wait, you said he's here now, but... didn't you\n |
| 0x95c66 | 45 | say this was developed hundreds of years ago? |
| 0x95c94 | 46 | No, there's no way the Mikado from back then\n |
| 0x95cc3 | 23 | is still alive today... |
| 0x95cdb | 46 | Nekone nods at what I said, her face looking\n |
| 0x95d0a | 39 | somewhat exasperated, a wordless "duh." |
| 0x95d32 | 43 | Why are you stating the obvious about the\n |
| 0x95d5e | 25 | Mikado still being alive? |
| 0x95d78 | 47 | Huh...? He's really alive? Wait, why am I the\n |
| 0x95da8 | 41 | weird one for saying something like that? |
| 0x95dd7 | 52 | I glance to Rulutieh, but even she's looking at me\n |
| 0x95e0c | 49 | in confusion, as if to ask the same question as\n |
| 0x95e3e | 7 | Nekone. |
| 0x95e46 | 21 | Hey, is the Mikado... |
| 0x95e5c | 18 | I whisper to Kuon. |
| 0x95e6f | 47 | It seems he has lived for centuries after the\n |
| 0x95e9f | 47 | nation's founding... or, well, his appearance\n |
| 0x95ecf | 15 | hasn't changed. |
| 0x95edf | 51 | Centuries... is it even possible to live that long? |
| 0x95f13 | 51 | Maybe it seems like he's lived for ages, but they\n |
| 0x95f47 | 49 | secretly switch in new ones, or some trick like\n |
| 0x95f79 | 5 | that? |
| 0x95f7f | 42 | Not under normal circumstances, I think.\n |
| 0x95faa | 45 | The longest people live is near two hundred\n |
| 0x95fd8 | 36 | years old, and most die long before. |
| 0x95ffd | 51 | Right...? Wait, they can still live for two whole\n |
| 0x96031 | 10 | centuries? |
| 0x9603c | 30 | Who exactly is this Mikado...? |
| 0x9605b | 48 | He is the Great Father of we people of Yamato.\n |
| 0x9608c | 44 | One vested with omniscience and omnipotence. |
| 0x960b9 | 43 | Oh, come on. There's no way he's actually\n |
| 0x960e5 | 26 | omniscient and omnipotent. |
| 0x96100 | 46 | Omniscient AND omnipotent, huh? Well, that's\n |
| 0x9612f | 50 | pretty impressive. No wonder he can do everything. |
| 0x96162 | 52 | Legend tells that he used his power to cut through\n |
| 0x96197 | 49 | mountains, and piled great stones to build this\n |
| 0x961c9 | 8 | capital. |
| 0x961d2 | 52 | In a war long ago, he called upon lightning, shook\n |
| 0x96207 | 51 | the ground with quakes, and blew tornadoes across\n |
| 0x9623b | 28 | the land. Such is his might. |
| 0x96258 | 45 | OK, this seemed fake to start with, but now\n |
| 0x96286 | 52 | it's even fishier. She seems sure, but who knows...? |
| 0x962bb | 26 | I glance over at Rulutieh. |
| 0x962d6 | 48 | Rulutieh nods reverently. It seems the stories\n |
| 0x96307 | 9 | are true. |
| 0x96311 | 53 | Well, stuff like this tends to get exaggerated over\n |
| 0x96347 | 46 | time... I should take it with a grain of salt. |
| 0x96376 | 47 | It is impossible for ones such as us to truly\n |
| 0x963a6 | 53 | comprehend the Mikado. It is best we remain mindful\n |
| 0x963dc | 13 | of our place. |
| 0x963ea | 46 | Otherwise, it will lead to your ruin, you see? |
| 0x96419 | 51 | So I shouldn't take this so lightly? Eh, that's a\n |
| 0x9644d | 47 | shame. I was hoping he could grant me a wish,\n |
| 0x9647d | 22 | if he can do anything. |
| 0x96494 | 46 | Such impudence. To gain an audience with the\n |
| 0x964c3 | 49 | Mikado, you must perform great meritorious deeds. |
| 0x964f5 | 46 | And to have a wish granted, you must perform\n |
| 0x96524 | 44 | an even more extraordinary meritorious deed. |
| 0x96551 | 48 | Huh. I was just joking, but he actually grants\n |
| 0x96582 | 12 | wishes, huh? |
| 0x9658f | 47 | Well, what sort of rewards has he given people? |
| 0x965bf | 16 | Why, there was-- |
| 0x965d0 | 50 | As I tune out the legends of the capital and the\n |
| 0x96603 | 48 | Mikado, we reach a river that spans across the\n |
| 0x96634 | 5 | city. |
| 0x9663a | 28 | This is the Omuchakko River. |
| 0x96657 | 53 | Boats of all sizes load and unload cargo across it,\n |
| 0x9668d | 47 | and the chatter of sailors and laborers fills\n |
| 0x966bd | 8 | the air. |
| 0x966c6 | 48 | This river is central to the city's logistics,\n |
| 0x966f7 | 45 | and it supports the lives of all within the\n |
| 0x96725 | 47 | Hmm. The capital's got wide roads, but a cart\n |
| 0x96755 | 52 | supply line still couldn't keep up with the city's\n |
| 0x9678a | 6 | needs. |
| 0x96791 | 49 | The city has a mountain behind it, hills around\n |
| 0x967c3 | 49 | it, and a river through it... Like for the Four\n |
| 0x967f5 | 32 | Symbols in eastern mythology...? |
| 0x96816 | 45 | ...Nah, I doubt it's for any feng shui stuff. |
| 0x96844 | 36 | Where are you going to take us next? |
| 0x96869 | 46 | We are going to go further south, to the gate. |
| 0x96898 | 6 | Wow... |
| 0x9689f | 49 | No matter how many times I see it, I suppose it\n |
| 0x968d1 | 33 | always stays just as marvelous... |
| 0x968f3 | 43 | I nod silently at Kuon's awestruck comment. |
| 0x9691f | 47 | We also saw this the first time we came here,\n |
| 0x9694f | 42 | but it really is huge. Unnecessarily huge. |
| 0x9697a | 50 | A gate of this size... They say the Mikado built\n |
| 0x969ad | 48 | this in one night, too. Maybe he's just really\n |
| 0x969de | 7 | ripped? |
| 0x969e6 | 53 | ...I don't know what you are thinking, but I advise\n |
| 0x96a1c | 23 | you sit and stay quiet. |
| 0x96a34 | 46 | It's so big... It makes me wonder why it was\n |
| 0x96a63 | 10 | made so... |
| 0x96a6e | 47 | Aside from the Mikado wanting it to represent\n |
| 0x96a9e | 43 | Yamato's commanding presence, it has some\n |
| 0x96aca | 27 | ceremonial purpose as well. |
| 0x96ae6 | 51 | I see. So it being so huge and impressive is just\n |
| 0x96b1a | 27 | meant to intimidate people. |
| 0x96b36 | 38 | It's probably a psychological thing.\n |
| 0x96b5d | 43 | Giving the impression that it'll never be\n |
| 0x96b89 | 24 | climbed, or torn down... |
| 0x96ba7 | 27 | Rulutieh freezes suddenly.  |
| 0x96bc3 | 9 | Rulutieh? |
| 0x96bcd | 16 | Um... Is that... |
| 0x96bde | 50 | Rulutieh's shaking hand points to the inner part\n |
| 0x96c11 | 12 | of the gate. |
| 0x96c1e | 19 | What... is that...? |
| 0x96c32 | 47 | On both sides of the gate are giant monstrous\n |
| 0x96c62 | 44 | statues, standing there as though guarding\n |
| 0x96c8f | 9 | the gate. |
| 0x96c99 | 13 | Are those...? |
| 0x96ca7 | 34 | Those are the guardians of Yamato. |
| 0x96cca | 48 | The guardian spirits of the Mikado and Yamato,\n |
| 0x96cfb | 41 | defenders of the people and the city...\n |
| 0x96d25 | 16 | the Akuruturuka. |
| 0x96d36 | 14 | Akuruturuka... |
| 0x96d45 | 51 | I have heard of them several times in fairy tales\n |
| 0x96d79 | 47 | and such, but... I've never seen them so big... |
| 0x96da9 | 38 | I-I'm sorry... for being frightened... |
| 0x96dd0 | 44 | Rulutieh then bows her head meekly towards\n |
| 0x96dfd | 12 | the statues. |
| 0x96e0a | 48 | It cannot be helped. Their fearsome appearance\n |
| 0x96e3b | 50 | wards off evil--it shows their desire to protect\n |
| 0x96e6e | 11 | our people. |
| 0x96e7a | 50 | Part of why the main gate is so large is so they\n |
| 0x96ead | 48 | can pass through it for their triumphant return. |
| 0x96ede | 38 | Does that mean these guys... can move? |
| 0x96f05 | 47 | They take off from there, and strike down any\n |
| 0x96f35 | 23 | approaching enemies...? |
| 0x96f4d | 7 | Huh...? |
| 0x96f55 | 24 | What is this drivel now? |
| 0x96f6e | 51 | Mere statues cannot move. They are hollow inside.\n |
| 0x96fa2 | 38 | My dear brother has shown me as much.  |
| 0x96fc9 | 12 | R-Really...? |
| 0x96fd6 | 46 | ...I also imagined they concealed some grand\n |
| 0x97005 | 40 | secret, so it was a touch disappointing. |
| 0x9702e | 48 | Oh, so we were all basically thinking the same\n |
| 0x9705f | 16 | thing after all. |
| 0x97070 | 36 | Kuon, is it bothering you that much? |
| 0x97095 | 51 | Hm? Oh, no, I was just thinking about the curious\n |
| 0x970c9 | 45 | similarities in our countries' lore and myth. |
| 0x970f7 | 51 | There's something like this in your homeland too,\n |
| 0x9712b | 5 | Kuon? |
| 0x97131 | 49 | I suppose you could say that. Nekone, where are\n |
| 0x97163 | 26 | you going to show us next? |
| 0x9717e | 50 | Yes--next, we will return north from the central\n |
| 0x971b1 | 42 | main road, and head towards the Mausoleum. |
| 0x971dc | 17 | It's beautiful... |
| 0x971ee | 53 | Rulutieh marvels at this Mausoleum--too vivid white\n |
| 0x97224 | 51 | to be metallic, but too reflective to be porcelain. |
| 0x97258 | 50 | A stone building...? No, it must be covered with\n |
| 0x9728b | 52 | some kind of glaze... That's why it looks so smooth. |
| 0x972c0 | 49 | The gates and manors lining the high street are\n |
| 0x972f2 | 50 | elaborate, but the size and detail pale compared\n |
| 0x97325 | 8 | to this. |
| 0x9732e | 47 | This is a place where various rituals are held. |
| 0x9735e | 50 | Beyond this point is sacred ground. None but the\n |
| 0x97391 | 43 | highest authorities are permitted to enter. |
| 0x973bd | 52 | The summit especially is strictly forbidden to all\n |
| 0x973f2 | 50 | but the Mikado's attendants and religious figures. |
| 0x97425 | 47 | Well, even if we had permission, I'm not wild\n |
| 0x97455 | 50 | about climbing all the way up something like that. |
| 0x97488 | 46 | Some say it contains countless secret rooms,\n |
| 0x974b7 | 50 | ancient knowledge, great treasure... and suchlike. |
| 0x974ea | 46 | I have heard that high-ranking scholars have\n |
| 0x97519 | 50 | permission to look inside, but I am not certain... |
| 0x9754c | 24 | ...Did she say treasure? |
| 0x97565 | 48 | And the twin buildings you see in front of the\n |
| 0x97596 | 28 | mausoleum make up the court. |
| 0x975b3 | 45 | Oh, I've been in there before. Accompanying\n |
| 0x975e1 | 17 | Rulutieh, anyway. |
| 0x975f3 | 13 | Huh... I see. |
| 0x97601 | 48 | Hrm, she didn't react much to that. Maybe that\n |
| 0x97632 | 21 | one's not off-limits? |
| 0x97648 | 35 | It's very... polished, I suppose.\n |
| 0x9766c | 45 | This must be what they mean by "elegant," hm? |
| 0x9769a | 30 | Y-Yes... It's quite beautiful. |
| 0x976b9 | 50 | I can agree with that. The intricate and elegant\n |
| 0x976ec | 40 | decorations... the majestic structure... |
| 0x97715 | 48 | It's polished to a gleam, and it has this high\n |
| 0x97746 | 46 | atmosphere, like... A building you'd find in\n |
| 0x97775 | 7 | heaven. |
| 0x9777d | 49 | It certainly does feel like a residence fit for\n |
| 0x977af | 32 | some holy ruler like the Mikado. |
| 0x977d0 | 47 | Man, everything's way too big in the capital.\n |
| 0x97800 | 47 | The city, the streets, the gate, the court...\n |
| 0x97830 | 9 | All huge. |
| 0x9783a | 44 | Walking all this way on foot is a real pain. |
| 0x97867 | 48 | But of course we would walk. Do you propose we\n |
| 0x97898 | 35 | would ride a steed the entire time? |
| 0x978bc | 22 | No, not steeds, but... |
| 0x978d3 | 49 | ...But if not that... then what? I can't put my\n |
| 0x97905 | 41 | finger on what I thought we'd be doing... |
| 0x9792f | 48 | Nekone looks at me questioningly as I open and\n |
| 0x97960 | 15 | close my mouth. |
| 0x97970 | 46 | Bah, whatever. Not like I can really explain\n |
| 0x9799f | 9 | myself... |
| 0x979a9 | 43 | Well, it's already past noon, so let's go\n |
| 0x979d5 | 14 | eat somewhere. |
| 0x979e4 | 48 | Yes... We have been walking all this time, so... |
| 0x97a15 | 40 | Seconded. This capital is way too big.\n |
| 0x97a3e | 28 | I'm hungry and my feet hurt. |
| 0x97a5b | 39 | All right. If that is the case, then... |
| 0x97a83 | 44 | We head onto a side street and come out on\n |
| 0x97ab0 | 44 | another road far from the main thoroughfare. |
| 0x97add | 48 | The relatively narrow street has vast lines of\n |
| 0x97b0e | 46 | stalls. It's totally different from the main\n |
| 0x97b3d | 7 | street. |
| 0x97b45 | 17 | It smells good... |
| 0x97b57 | 45 | Huh, nice. I could get used to this kind of\n |
| 0x97b85 | 8 | variety. |
| 0x97b8e | 46 | There were shops on the main street as well,\n |
| 0x97bbd | 43 | but they were more formal compared to the\n |
| 0x97be9 | 18 | folksy stuff here. |
| 0x97bfc | 14 | Well, first... |
| 0x97c0b | 16 | Are you thirsty? |
| 0x97c1c | 44 | I notice Nekone passing drinks to Kuon and\n |
| 0x97c49 | 42 | Rulutieh. Must have got them while I was\n |
| 0x97c74 | 15 | looking around. |
| 0x97c84 | 21 | Oh, it's delicious... |
| 0x97c9a | 41 | Y-Yes... It has a unique flavor indeed... |
| 0x97cc4 | 36 | I see... so it's delicious, huh...\n |
| 0x97ce9 | 21 | Yep. Sounds... great. |
| 0x97cff | 42 | U-Um... If you'd like, please have this... |
| 0x97d2a | 49 | I look over to see Rulutieh timidly offering me\n |
| 0x97d5c | 48 | her container. There's about half of the drink\n |
| 0x97d8d | 5 | left. |
| 0x97d93 | 51 | You sure? It looks like there's still quite a bit\n |
| 0x97dc7 | 42 | I-It's fine... I-I can't drink that much\n |
| 0x97df2 | 14 | at once, so... |
| 0x97e01 | 46 | If that's the case, then sure, I'd be glad to. |
| 0x97e30 | 50 | I take the drink from her and lift it to my mouth. |
| 0x97e63 | 5 | Oh... |
| 0x97e69 | 42 | As I do, Rulutieh realizes something and\n |
| 0x97e94 | 41 | covers her lips while blushing furiously. |
| 0x97ebe | 50 | Huh, that's a unique flavor. It's sour, and it's\n |
| 0x97ef1 | 47 | got this nice scent to it... A bit bubbly, too. |
| 0x97f21 | 46 | It's a strange drink, but it's not bad at all. |
| 0x97f50 | 30 | Phew, that was refreshing...\n |
| 0x97f6f | 3 | Hm? |
| 0x97f73 | 47 | S-Sir Haku's lips were... wh-where mine were... |
| 0x97fa3 | 31 | Whoa, your face is all red...\n |
| 0x97fc3 | 14 | Are you tired? |
| 0x97fd2 | 27 | N-No, n-nothing is wrong... |
| 0x97fee | 13 | Are you sure? |
| 0x97ffc | 24 | Now, what should we eat? |
| 0x98015 | 48 | I'm distracted from Rulutieh's odd distress as\n |
| 0x98046 | 48 | Kuon turns my attention to the huge variety of\n |
| 0x98077 | 6 | shops. |
| 0x9807e | 30 | What's that fried thing there? |
| 0x9809d | 51 | You mean the kamuka? That is a mix of minced meat\n |
| 0x980d1 | 50 | and vegetables, fried with dough in a triangular\n |
| 0x98104 | 6 | shape. |
| 0x9810b | 38 | I've never had that before, I think.\n |
| 0x98132 | 31 | Then I guess I'll try that one. |
| 0x98152 | 47 | I'll try this... fishy cake thing. Is it even\n |
| 0x98182 | 50 | ready, though? The fish looks kind of raw still... |
| 0x981b5 | 51 | That is called a sheruchichi, and it is comprised\n |
| 0x981e9 | 51 | of salted fish folded into a thick, steamed piece\n |
| 0x9821d | 15 | of amam dough.  |
| 0x9822d | 44 | Let's see... Mmn. It's delicious, but it's\n |
| 0x9825a | 36 | pretty salty. Then this calls for... |
| 0x9827f | 50 | ...I am not going to allow you to start drinking\n |
| 0x982b2 | 25 | in the middle of the day. |
| 0x982cc | 26 | ...Urgh, how did you know? |
| 0x982e7 | 41 | It is obvious, if you act with the same\n |
| 0x98311 | 37 | inclinations as my dear brother does. |
| 0x98337 | 7 | Urgh... |
| 0x9833f | 47 | U-Um... Miss Nekone... What is that yellow...\n |
| 0x9836f | 24 | sweet-smelling thing...? |
| 0x98388 | 30 | I have never seen it before... |
| 0x983a7 | 49 | Sweets called kunyui--a batter of sweetened and\n |
| 0x983d9 | 45 | beaten eggs, filled with fruit and herbs...\n |
| 0x98407 | 10 | I believe. |
| 0x98412 | 47 | Hee hee, it looks like the gold is sparkling... |
| 0x98442 | 42 | Whoa-ho-ho, shining golden sweets, huh...? |
| 0x9846d | 49 | ...I'm not sure why, but it seems charming when\n |
| 0x9849f | 48 | Rulutieh says it, but suspect when Haku says it. |
| 0x984d0 | 45 | I expect it is because his entire existence\n |
| 0x984fe | 19 | is morally suspect. |
| 0x98512 | 8 | Hey now. |
| 0x9851b | 43 | They're a rude bunch. What about me is so\n |
| 0x98547 | 8 | dubious? |
| 0x98550 | 33 | S-Sir Haku is... a kind person... |
| 0x98572 | 46 | Rulutieh is so kind... but then again, she's\n |
| 0x985a1 | 32 | not denying what they're saying. |
| 0x985c2 | 38 | Are these round ones here sweets, too? |
| 0x985e9 | 46 | That is a furyan. It is so well-loved by the\n |
| 0x98618 | 42 | locals that some call it a staple dessert. |
| 0x98643 | 15 | Oh... Yorkur... |
| 0x98653 | 7 | Yorkur? |
| 0x9865b | 51 | It's fermented and solidified lanya... animal milk. |
| 0x9868f | 48 | So you have that here too. You use a different\n |
| 0x986c0 | 46 | kind of milk, but we have something similar,\n |
| 0x986ef | 8 | I think. |
| 0x986f8 | 54 | Just based on appearance, it looks sweet and sour...\n |
| 0x9872f | 24 | It's probably delicious. |
| 0x98748 | 31 | ...Mhm. I think it's very nice. |
| 0x98768 | 21 | Yes, it is delicious. |
| 0x9877e | 26 | Guess I'll try some, then. |
| 0x98799 | 39 | Given a piece, I toss it into my mouth. |
| 0x987c1 | 10 | Huh? Oh... |
| 0x987cc | 7 | Hngh--! |
| 0x987d4 | 13 | I-It's sour-- |
| 0x987e2 | 49 | That is usually used for cooking... or drinking\n |
| 0x98814 | 42 | after it's been dissolved and sweetened... |
| 0x9883f | 9 | Mmpfff... |
| 0x98849 | 23 | Wh-Why, those little... |
| 0x98861 | 52 | As we continue strolling on our way, a deliciously\n |
| 0x98896 | 39 | savory scent wafts in from somewhere... |
| 0x988be | 33 | Ah, it smells good. Is that meat? |
| 0x988e0 | 49 | That is a shishukepu. A dish from the nomads of\n |
| 0x98912 | 47 | Uzurusha--marinated and cooked meat on skewers. |
| 0x98942 | 50 | They say it is eaten with a yorkur drink in such\n |
| 0x98975 | 41 | regions. It is quite delicious, you know? |
| 0x9899f | 18 | It does look good. |
| 0x989b2 | 48 | In this area, many stalls sell foodstuffs from\n |
| 0x989e3 | 36 | all kinds of cultures and countries. |
| 0x98a08 | 47 | That stall you see there serves a traditional\n |
| 0x98a38 | 44 | dish from Shyahoro, a nation of the south... |
| 0x98a65 | 49 | An isokattso. They take a fish called a kattsu,\n |
| 0x98a97 | 48 | coat it, fry it, and cover it in a spiced sauce. |
| 0x98ac8 | 45 | And here, a fukutomasuo. They're fish balls\n |
| 0x98af6 | 43 | made from maso paste, fried and boiled in\n |
| 0x98b22 | 12 | a red sauce. |
| 0x98b2f | 47 | That stall offers foka, which is a home-style\n |
| 0x98b5f | 17 | dish from Nakoku. |
| 0x98b71 | 49 | One puts sukuru and sauce on dough, then adding\n |
| 0x98ba3 | 46 | herbs, eggs and smoked meats, baking the lot\n |
| 0x98bd2 | 11 | in an oven. |
| 0x98bde | 43 | Different varieties can be made by simply\n |
| 0x98c0a | 22 | changing the toppings. |
| 0x98c21 | 45 | I suppose it's because this is the imperial\n |
| 0x98c4f | 44 | capital that we have such a wide selection\n |
| 0x98c7c | 10 | available. |
| 0x98c87 | 50 | Yes, here in our imperial capital, the center of\n |
| 0x98cba | 47 | Yamato, we have dishes from all over the world. |
| 0x98cea | 52 | She seems awfully proud, but I kind of understand.\n |
| 0x98d1f | 35 | It's not easy, conquering all this. |
| 0x98d43 | 50 | ...But the more I look, the harder it's gonna be\n |
| 0x98d76 | 19 | to make a decision. |
| 0x98d8a | 33 | Phew, we ended up eating a ton... |
| 0x98dac | 52 | I'm a bit thirsty. I wouldn't mind a little break,\n |
| 0x98de1 | 45 | so we can have a little between-meal snack... |
| 0x98e0f | 49 | I knew it. She ate all that, and it still isn't\n |
| 0x98e41 | 23 | anywhere near enough... |
| 0x98e59 | 32 | Rulutieh suddenly stops walking. |
| 0x98e7a | 50 | She keeps glancing restlessly into a small alley\n |
| 0x98ead | 7 | nearby. |
| 0x98eb5 | 19 | Is something wrong? |
| 0x98ec9 | 47 | I look and see what appears to be some stores\n |
| 0x98ef9 | 47 | selling picture scrolls and books in the alley. |
| 0x98f29 | 46 | U-Um... Miss Nekone... What is this street...? |
| 0x98f58 | 9 | This one? |
| 0x98f62 | 48 | If I recall, it is a street where one can find\n |
| 0x98f93 | 35 | many vendors of books and pictures. |
| 0x98fb7 | 48 | Though I do not know much about them, as their\n |
| 0x98fe8 | 40 | focus seems to be on popular literature. |
| 0x99011 | 47 | The narrow alleyway bustles with young ladies\n |
| 0x99041 | 46 | around Rulutieh's age, coming and going from\n |
| 0x99070 | 10 | the shops. |
| 0x9907b | 44 | It's full of women... well, girls, anyway.\n |
| 0x990a8 | 45 | And because of that, the place is pretty...\n |
| 0x990d6 | 9 | colorful. |
| 0x990e0 | 46 | In the crowd, we see girls dressed in dainty\n |
| 0x9910f | 45 | clothes so frilly that they easily stand out. |
| 0x9913d | 7 | U-Um... |
| 0x99145 | 49 | U-Um... would it be all right if I went to look\n |
| 0x99177 | 13 | for a bit...? |
| 0x99185 | 40 | You looking for some book in particular? |
| 0x991ae | 40 | Huh...? Oh, um... something like that... |
| 0x991d7 | 49 | I think it's fine. If you like, I can accompany\n |
| 0x99209 | 7 | you...? |
| 0x99211 | 24 | N-No, I'll go by myself! |
| 0x9922a | 51 | Oh... no... It's fine... I've done my research...\n |
| 0x9925e | 37 | I-I mean... I know about this area... |
| 0x99284 | 25 | No... Um... Never mind... |
| 0x9929e | 46 | Rulutieh seems fidgety and restless for some\n |
| 0x992cd | 7 | reason. |
| 0x992d5 | 45 | Then we'll be waiting at that teahouse over\n |
| 0x99303 | 15 | there, I think. |
| 0x99313 | 36 | I'll give you the map, just in case. |
| 0x99338 | 36 | Th-Thank you... I'll be off, then... |
| 0x9935d | 48 | Rulutieh bows several times upon receiving the\n |
| 0x9938e | 44 | map, and promptly hurries into the alleyway. |
| 0x993bb | 25 | She seemed awfully antsy. |
| 0x993d5 | 46 | I guess she has moments like that as well...\n |
| 0x99404 | 34 | Let's wait for Rulutieh to return. |
| 0x99427 | 36 | Kuon seems to understand, somehow... |
| 0x9944c | 8 | ...Whoa. |
| 0x99455 | 46 | I bump into a man as he makes his way out of\n |
| 0x99484 | 35 | the alleyway, trying to pass by us. |
| 0x994a8 | 51 | Bundles of paper flutter out from the parcel that\n |
| 0x994dc | 25 | the man has in his hands. |
| 0x994f6 | 8 | S-Sorry. |
| 0x994ff | 36 | Oh no, the fault is mine entirely.\n |
| 0x99524 | 36 | I was not looking where I was going. |
| 0x99549 | 47 | The man gracefully kneels, starting to gather\n |
| 0x99579 | 39 | his papers. I hastily move to help him. |
| 0x995a1 | 46 | All the papers look like they're filled with\n |
| 0x995d0 | 33 | strange symbols and characters... |
| 0x995f2 | 45 | He has a beautiful face for a man. From his\n |
| 0x99620 | 46 | appearance, I assume he must be some kind of\n |
| 0x9964f | 16 | merchant prince. |
| 0x99660 | 10 | Thank you. |
| 0x9966b | 43 | The man bows graciously as I hold out the\n |
| 0x99697 | 45 | gathered bundle of papers, taking it from me. |
| 0x996c5 | 6 | Oh...? |
| 0x996cc | 45 | As the man looks my way, a soft exclamation\n |
| 0x996fa | 46 | escapes him, as though he's noticed something. |
| 0x99729 | 6 | Ah...? |
| 0x99730 | 44 | Something seems to dawn on Nekone as well.\n |
| 0x9975d | 22 | She hesitates, unsure. |
| 0x99774 | 43 | It isn't clear if he understands Nekone's\n |
| 0x997a0 | 41 | expression or not, but he walks to her,\n |
| 0x997ca | 16 | smiling broadly. |
| 0x997db | 50 | If it isn't Miss Nekone. What an odd coincidence\n |
| 0x9980e | 44 | it is, to meet you out in a place like this. |
| 0x9983b | 10 | You are... |
| 0x99846 | 24 | You two know each other? |
| 0x9985f | 47 | I direct my question at Nekone, seeing what's\n |
| 0x9988f | 33 | going on between the two of them. |
| 0x998b1 | 46 | I would not go so far as to say that we know\n |
| 0x998e0 | 13 | each other... |
| 0x998ee | 44 | Well, Miss Nekone is renowned as a girl of\n |
| 0x9991b | 46 | uncommon genius amongst the well-informed of\n |
| 0x9994a | 8 | society. |
| 0x99953 | 47 | It is unfortunate that you cannot yet don the\n |
| 0x99983 | 48 | mantle of a scholar, merely because of your age. |
| 0x999b4 | 46 | It is nothing so significant. And if you say\n |
| 0x999e3 | 30 | that, then you yourself are... |
| 0x99a02 | 50 | Quickly, the man lifts his index finger in front\n |
| 0x99a35 | 12 | of his lips. |
| 0x99a42 | 32 | Oh... I-I meant nothing by that. |
| 0x99a63 | 40 | Please, do not concern yourself over it. |
| 0x99a8c | 33 | Huh? What are they talking about? |
| 0x99aae | 46 | It would appear you are guiding some foreign\n |
| 0x99add | 32 | friends around our fair capital? |
| 0x99afe | 50 | Yes, that is correct. But what are you doing here? |
| 0x99b31 | 49 | Is it wrong for me to be in a place such as this? |
| 0x99b63 | 50 | Not precisely, but it does not suit you somehow.\n |
| 0x99b96 | 46 | I would expect you in high-class shops along\n |
| 0x99bc5 | 12 | main street. |
| 0x99bd2 | 45 | My, no, I usually send an emissary for such\n |
| 0x99c00 | 43 | errands. But I had an important task today. |
| 0x99c2c | 23 | Something... important? |
| 0x99c44 | 50 | Nekone tilts her head in puzzlement at the man's\n |
| 0x99c77 | 10 | admission. |
| 0x99c82 | 53 | Yes, I've come to finally submit a new manuscript--\n |
| 0x99cb8 | 41 | ah... a delivery. I wished to see to it\n |
| 0x99ce2 | 11 | personally. |
| 0x99cee | 45 | Inspiration has been guiding my pen lately.\n |
| 0x99d1c | 47 | Though my secondary job has suffered somewhat\n |
| 0x99d4c | 15 | as a result...  |
| 0x99d5c | 34 | Oh dear. Truly troublesome indeed. |
| 0x99d7f | 49 | Surely that should be your primary concern, not\n |
| 0x99db1 | 44 | a "secondary job"... Tsk. You yourself are\n |
| 0x99dde | 12 | troublesome. |
| 0x99deb | 47 | Ah, I forget myself... my next script awaits.\n |
| 0x99e1b | 48 | Regrettably, I must be off. My warmest regards\n |
| 0x99e4c | 16 | to your brother. |
| 0x99e5d | 12 | Very well... |
| 0x99e6a | 49 | Well then, my fine sir and miss, I must take my\n |
| 0x99e9c | 37 | leave. Perhaps we shall meet again... |
| 0x99ec2 | 48 | The man gives a quick final bow and glides off\n |
| 0x99ef3 | 15 | into the crowd. |
| 0x99f03 | 46 | Hmhmhm. He could make a fine muse... Perhaps\n |
| 0x99f32 | 46 | I may find some means of coaxing him into my\n |
| 0x99f61 | 15 | next pairing... |
| 0x99f71 | 47 | Haku, why are you squirming around like that?\n |
| 0x99fa1 | 45 | No, just... I felt some kind of weird dread\n |
| 0x99fcf | 15 | for a second... |
| 0x99fdf | 51 | I don't know why, but... I feel like I'm straying\n |
| 0x9a013 | 25 | in dangerous territory... |

## 8. Formato de saida EXIGIDO
Escreva `translations_14_09.json` com a forma:
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
