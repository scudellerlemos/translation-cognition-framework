# Cena ch_23_14 — pacote de traducao (203 linhas)

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
| Akuruka | Objeto | Akuruka | manter_original | moderate |
| Benawi | Personagem | Benawi | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Earth | Local | Terra | traduzir | major |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurou | Personagem | Kurou | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Warmaster | Titulo | Mestre de Guerra | traduzir | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `ch_401_00` -> `ch_401_00` (, 23_12)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `Right...` -> `É...` (Ukon, 15_01)
- `What?` -> `Que?` (Haku, 12_02)
- `Cocopo?` -> `Cocopo?` (Kurou, 23_13)
- `Wh--` -> `Q--` (Haku, 11_07)
- `of you?` -> `de vocês?` (Haku, 19_08)
- `for you.` -> `para você.` (Ougi, 13_08)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `Yes!` -> `Sim!` (Rulutieh, 14_04)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Gah!` -> `Ai!` (Man, 11_01)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `out.` -> `fora.` (Atuy, 17_01)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `What are y--\n` -> `O que você--\n` (Kuon, 23_12)
- `Understood!` -> `Entendido!` (Soldado, 23_13)
- `HYAH!` -> `HYAH!` (Haku, 18_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `It's Haku.` -> `É Haku.` (Haku, 18_01)
- `Jachdwalt.` -> `Jachdwalt.` (Haku, 20_07)
- `What the--` -> `Mas que--` (Haku, 11_03)
- `Heh... Ah heh heh.` -> `Heh... Ah heh heh.` (Homem, 14_06)
- `Yes, sir.` -> `Sim, senhor.` (Bokoinante, 20_14)
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
| 0x2b6a2f | 9 | ch_401_00 |
| 0x2b6a39 | 8 | GYAAAAH! |
| 0x2b6a42 | 17 | Huff, hah, hah... |
| 0x2b6a54 | 11 | W-We won... |
| 0x2b6a60 | 50 | What prowess. I had no idea men like him existed\n |
| 0x2b6a93 | 10 | in Tuskur. |
| 0x2b6aa2 | 7 | Kuon... |
| 0x2b6aaa | 10 | Right...\n |
| 0x2b6ab5 | 29 | He was someone she knew, huh? |
| 0x2b6ad3 | 46 | It's not over yet! Nobody let your guard down. |
| 0x2b6b02 | 5 | What? |
| 0x2b6b08 | 47 | This man... The Kurou I know wouldn't go down\n |
| 0x2b6b38 | 10 | so easily. |
| 0x2b6b43 | 19 | Huh... But he's...? |
| 0x2b6b57 | 41 | We did quite a number on him. He may be\n |
| 0x2b6b81 | 42 | breathing, but he's not in fighting shape. |
| 0x2b6bac | 27 | He's likely toying with us. |
| 0x2b6bc8 | 50 | Chances are, he's waiting for us to be convinced\n |
| 0x2b6bfb | 45 | of our victory so he can have the last laugh. |
| 0x2b6c29 | 45 | I highly doubt he's any danger to us in the\n |
| 0x2b6c57 | 14 | state he's in. |
| 0x2b6c66 | 48 | She's right. I've never had anyone take a blow\n |
| 0x2b6c97 | 42 | from me and be quite all right afterwards. |
| 0x2b6cd1 | 7 | Cocopo? |
| 0x2b6cd9 | 45 | Come on, now. Why would you go and ruin the\n |
| 0x2b6d07 | 19 | surprise like that? |
| 0x2b6d1b | 4 | Wh-- |
| 0x2b6d20 | 8 | Huh...!? |
| 0x2b6d29 | 16 | This guy's good. |
| 0x2b6d3a | 27 | That can't be... We just... |
| 0x2b6d56 | 50 | How? I was sure we hit all sorts of vital spots... |
| 0x2b6d89 | 47 | That really stings, you know. I thought I was\n |
| 0x2b6db9 | 37 | really in danger for a moment, there. |
| 0x2b6ddf | 34 | Hee hee. Just an act, then? I see. |
| 0x2b6e02 | 43 | No, no, really. That beating you gave me?\n |
| 0x2b6e2e | 39 | Knocked the drowsiness RIGHT out of me. |
| 0x2b6e56 | 46 | Ooh, what a man... You might go and actually\n |
| 0x2b6e85 | 20 | make me get serious! |
| 0x2b6e9a | 43 | But is that really what you expect of me,\n |
| 0x2b6ec6 | 47 | my lady? That I'd just try to get a laugh out\n |
| 0x2b6ef6 | 7 | of you? |
| 0x2b6efe | 47 | Could it be you're still nursing grudges from\n |
| 0x2b6f2e | 10 | years ago? |
| 0x2b6f39 | 47 | I mean, sure, I pinched your snacks from time\n |
| 0x2b6f69 | 47 | to time, but it was a spur-of-the-moment thing. |
| 0x2b6f99 | 27 | ...So you were the culprit. |
| 0x2b6fb5 | 47 | Huh? Heh, didn't expect you to remember that.\n |
| 0x2b6fe5 | 35 | Guess I walked right into that one. |
| 0x2b7009 | 47 | Easy, now. I wouldn't do that, if I were you.\n |
| 0x2b7039 | 46 | If you don't retreat soon, it'll be too late\n |
| 0x2b7068 | 8 | for you. |
| 0x2b7071 | 9 | Too late? |
| 0x2b707b | 45 | Some other force is acting as a distraction\n |
| 0x2b70a9 | 44 | while you make off with the supplies, right? |
| 0x2b70d6 | 45 | The longer you take, the more danger you're\n |
| 0x2b7104 | 43 | putting your comrades in. I know I'm right. |
| 0x2b7130 | 48 | I appreciate your concern, but the one leading\n |
| 0x2b7161 | 38 | that force isn't as weak as you think. |
| 0x2b7188 | 12 | Oh? That so? |
| 0x2b7195 | 47 | If I were you, I wouldn't talk such a big game. |
| 0x2b71c5 | 17 | Nngh! I knew it-- |
| 0x2b71d7 | 48 | That's right. How long will your "distraction"\n |
| 0x2b7208 | 36 | last against the Chief, I wonder...? |
| 0x2b722d | 48 | I shall open the "gate." All forces, defensive\n |
| 0x2b725e | 24 | bulkhead formation! Now! |
| 0x2b7277 | 7 | Soldier |
| 0x2b727f | 44 | No, you mustn't! Releasing your full power\n |
| 0x2b72ac | 41 | will tax you too much, Lady Munechika--!! |
| 0x2b72d6 | 43 | It's likely that these soldiers are their\n |
| 0x2b7302 | 6 | elite. |
| 0x2b7309 | 47 | It is our duty to hold their attention for as\n |
| 0x2b7339 | 15 | long as we can. |
| 0x2b7349 | 48 | Lord Haku and the others are trusting in us so\n |
| 0x2b737a | 47 | their plan can succeed. We shall not fail them. |
| 0x2b73aa | 50 | I am sorry, but... I must ask you all to entrust\n |
| 0x2b73dd | 17 | your lives to me. |
| 0x2b73ef | 18 | ...Lady Munechika. |
| 0x2b7402 | 49 | Speak no more. We will follow you to the bitter\n |
| 0x2b7434 | 4 | end! |
| 0x2b7439 | 48 | ...You have my apologies and my greatest thanks. |
| 0x2b746a | 48 | I am the Guardian! Open the way to the origin,\n |
| 0x2b749b | 49 | O Akuruka, and through it grant me the heavens'\n |
| 0x2b74cd | 6 | aegis! |
| 0x2b74d4 | 45 | With a flash of blinding light, Munechika's\n |
| 0x2b7502 | 40 | power manifests before her as a great,\n |
| 0x2b752b | 18 | shielding barrier. |
| 0x2b753e | 28 | All soldiers, ready weapons! |
| 0x2b755b | 11 | ...Forward. |
| 0x2b7567 | 43 | Benawi and his rakusharai charge forward,\n |
| 0x2b7593 | 48 | unflappable in the face of Munechika's display\n |
| 0x2b75c4 | 9 | of power. |
| 0x2b75ce | 24 | You shall go no further! |
| 0x2b75e7 | 48 | The earth before Munechika rolls and undulates\n |
| 0x2b7618 | 44 | in a great wave, as if to swallow Benawi's\n |
| 0x2b7645 | 9 | forces... |
| 0x2b764f | 4 | Yes! |
| 0x2b7654 | 49 | But Benawi and his soldiers gracefully sidestep\n |
| 0x2b7686 | 44 | it, charging instead from Munechika's flank. |
| 0x2b76b3 | 5 | Hah!! |
| 0x2b76b9 | 47 | As Benawi's soldiers close in from the sides,\n |
| 0x2b76e9 | 44 | they release a hail of arrows, pinning the\n |
| 0x2b7716 | 14 | Yamatans down. |
| 0x2b7725 | 6 | What!? |
| 0x2b772c | 48 | The tables turn quickly as arrows rain down on\n |
| 0x2b775d | 21 | Munechika's forces... |
| 0x2b7773 | 20 | Tch. Ring formation! |
| 0x2b7788 | 42 | Munechika quickly rallies her troops and\n |
| 0x2b77b3 | 44 | protects them from the archers, but Benawi\n |
| 0x2b77e0 | 14 | surrounds her. |
| 0x2b77ef | 14 | They're fast-- |
| 0x2b77fe | 43 | Benawi's rakusharai circle like a pack of\n |
| 0x2b782a | 48 | predators seeking an opening in the herd, then\n |
| 0x2b785b | 7 | charge. |
| 0x2b7863 | 4 | Gah! |
| 0x2b7868 | 45 | The Yamatan line buckles under the pressure\n |
| 0x2b7896 | 45 | from Benawi, and soon, Munechika's position\n |
| 0x2b78c4 | 14 | is threatened. |
| 0x2b78d3 | 7 | Nngh... |
| 0x2b78db | 48 | With nothing between her and Benawi, Munechika\n |
| 0x2b790c | 47 | quickly takes a gash from his spear and cries\n |
| 0x2b793c | 4 | out. |
| 0x2b7941 | 44 | Rgh... If I use my abilities in such close\n |
| 0x2b796e | 49 | quarters, I can't avoid hitting my own soldiers-- |
| 0x2b79a0 | 45 | Munechika manages to block each of Benawi's\n |
| 0x2b79ce | 49 | attacks, but the ferocity of them slowly drives\n |
| 0x2b7a00 | 9 | her back. |
| 0x2b7a0a | 46 | This man... He's well-versed in how to fight\n |
| 0x2b7a39 | 32 | people with abilities like mine. |
| 0x2b7a5a | 43 | Munechika grits her teeth, keeping up her\n |
| 0x2b7a86 | 40 | defense, the clash of steel continuing\n |
| 0x2b7aaf | 13 | relentlessly. |
| 0x2b7abd | 44 | I see now. This is what Lady Kuon had meant. |
| 0x2b7aea | 42 | She was not worried for her countrymen's\n |
| 0x2b7b15 | 21 | safety... but my own. |
| 0x2b7b2b | 49 | I've grown sloppy. Haphazard. When did I become\n |
| 0x2b7b5d | 37 | so overconfident in my own skills...? |
| 0x2b7b83 | 44 | Suddenly, Benawi lowers his spear, and the\n |
| 0x2b7bb0 | 43 | menacing aura about him dissipates almost\n |
| 0x2b7bdc | 10 | instantly. |
| 0x2b7be7 | 43 | His rakusharai also cease their fighting,\n |
| 0x2b7c13 | 41 | instead lining up behind their commander. |
| 0x2b7c3d | 8 | What...? |
| 0x2b7c46 | 46 | I believe that will be enough, Lady Munechika. |
| 0x2b7c75 | 21 | Wh--You know my name? |
| 0x2b7c8b | 40 | I am Benawi, and mine is the mantle of\n |
| 0x2b7cb4 | 20 | Warmaster of Tuskur. |
| 0x2b7cc9 | 46 | So it IS you. I am General Munechika, of the\n |
| 0x2b7cf8 | 24 | Eight Pillars of Yamato. |
| 0x2b7d11 | 41 | You'd do best to fall back now, Pillar.\n |
| 0x2b7d3b | 39 | Your plan has already ended in failure. |
| 0x2b7d63 | 45 | Fall back...? You're not demanding surrender? |
| 0x2b7d91 | 49 | Yes. Forcing a surrender from you would be a...\n |
| 0x2b7dc3 | 15 | costly pursuit. |
| 0x2b7dd3 | 14 | And besides... |
| 0x2b7de2 | 8 | Besides? |
| 0x2b7deb | 37 | You no longer have a reason to fight. |
| 0x2b7e11 | 49 | Regardless of the outcome here, you will return\n |
| 0x2b7e43 | 27 | to your country and begone. |
| 0x2b7e5f | 12 | What are y-- |
| 0x2b7e6c | 45 | Well, I'm warmed up, now. Why don't we have\n |
| 0x2b7e9a | 17 | another bout, hm? |
| 0x2b7eac | 17 | Jachdwalt, on me. |
| 0x2b7ebe | 11 | Understood! |
| 0x2b7eca | 5 | HYAH! |
| 0x2b7ed0 | 24 | Gah! That was close...\n |
| 0x2b7ee9 | 4 | Huh? |
| 0x2b7eee | 50 | You were talking about letting us go, so I think\n |
| 0x2b7f21 | 37 | we'll be taking you up on that offer. |
| 0x2b7f47 | 49 | Oh...? Turning tail when you realize the wind's\n |
| 0x2b7f79 | 43 | not in your favor? Quick tactical thinking. |
| 0x2b7fa5 | 22 | What's your name, boy? |
| 0x2b7fbc | 10 | It's Haku. |
| 0x2b7fc7 | 19 | Haku? But that's... |
| 0x2b7fdb | 10 | Jachdwalt. |
| 0x2b7fe6 | 23 | Yessir. Last one, yeah? |
| 0x2b7ffe | 12 | What the--\n |
| 0x2b800b | 30 | Oh, you HAVE to be kidding me. |
| 0x2b802a | 43 | We'll gladly accept these gifts, as well.\n |
| 0x2b8056 | 15 | Later, old man! |
| 0x2b8066 | 18 | Heh... Ah heh heh. |
| 0x2b8079 | 47 | Ahahaha! What in the world? The nerve on that\n |
| 0x2b80a9 | 17 | kid... He's good. |
| 0x2b80bb | 47 | No one would've expected an idiotic plan like\n |
| 0x2b80eb | 44 | that to go off without a hitch. No one sane. |
| 0x2b8118 | 43 | And his name's Haku. What exactly is that\n |
| 0x2b8144 | 28 | supposed to mean... my lady? |
| 0x2b8161 | 21 | Kurou, status report. |
| 0x2b8177 | 35 | ...They got me. Got me good, too.\n |
| 0x2b819b | 24 | Sorry about that, chief. |
| 0x2b81b4 | 47 | It won't be an issue. As I said, they'll have\n |
| 0x2b81e4 | 46 | no choice but to pull out, regardless of the\n |
| 0x2b8213 | 8 | outcome. |
| 0x2b821c | 49 | I never expected them to execute on a plan like\n |
| 0x2b824e | 13 | that, though. |
| 0x2b825c | 32 | Bold, almost insane tactics...\n |
| 0x2b827d | 29 | Remind you of anyone we know? |
| 0x2b829b | 24 | You seem happy about it. |
| 0x2b82b4 | 41 | I'm not the only one here smiling, chief. |
| 0x2b82de | 44 | My lady was with him, too. She seems to be\n |
| 0x2b830b | 28 | doing well. Good to see her. |
| 0x2b8328 | 47 | I see. She accompanied them all the way here... |
| 0x2b8358 | 36 | Kurou, with me. We shall give chase. |
| 0x2b837d | 9 | Yes, sir. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_14.json` com a forma:
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
