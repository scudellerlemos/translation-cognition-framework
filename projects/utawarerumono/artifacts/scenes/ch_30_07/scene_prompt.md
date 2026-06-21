# Cena ch_30_07 — pacote de traducao (313 linhas)

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
| Akuruturuka | Termo | Akuruturuka | manter_original | major |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Ohn Riyaak | Local | Ohn Riyaak | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Sir Haku...` -> `Senhor Haku...` (Garota, 16_03)
- `Vurai...` -> `Vurai...` (Haku, 30_01)
- `hopeless.` -> `perdido.` (Soldado de Tuskur, 23_09)
- `Ghh...` -> `Argh...` (Man, 11_01)
- `like that?` -> `assim?` (Haku, 15_01)
- `Right?` -> `né?` (Haku, 11_01)
- `of me.` -> `de mim.` (Nosuri, 18_01)
- `brother...` -> `irmão...` (Nekone, 15_01)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Wha--` -> `Quê--` (Man, 11_01)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `everything.` -> `tudo.` (Maroro, 19_06)
- `I... I...` -> `E-E...` (Haku, 17_01)
- `Y-Yes...?` -> `S-Sim...?` (Rulutieh, 13_08)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `you.` -> `isso.` (Nekone, 15_03)
- `this...` -> `isto...` (Kuon, 11_08)
- `...Mm?` -> `...Hm?` (Haku, 19_08)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `Miss Kuon?` -> `Querida Nekone?` (Kuon, 21_03)
- `Yeah...` -> `É...` (Kuon, 11_02)
- `Are you sure about this?` -> `Você tem certeza disso?` (Kuon, 23_06)
- `As you wish.` -> `Como desejar.` (Nekone, 14_04)
- `Lady-in-waiting` -> `Dama de companhia` (Ukon, 30_04)
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
| 0x2e18f2 | 34 | Just a little more. Hang in there. |
| 0x2e1915 | 44 | The twins' only response to my reassurance\n |
| 0x2e1942 | 15 | is a small nod. |
| 0x2e1952 | 49 | The two of them usually don't show any emotion,\n |
| 0x2e1984 | 40 | but I can see this is taking its toll.\n |
| 0x2e19ad | 33 | They're sweating from the effort. |
| 0x2e19cf | 48 | They're turning paler, too. The strain must be\n |
| 0x2e1a00 | 38 | incredible if they can't even speak... |
| 0x2e1a27 | 11 | Sir Haku... |
| 0x2e1a33 | 43 | Rulutieh must be thinking the same thing.\n |
| 0x2e1a5f | 31 | She looks towards me worriedly. |
| 0x2e1a7f | 46 | At this rate, we may not even make it to the\n |
| 0x2e1aae | 47 | princess's room. We might need a backup plan... |
| 0x2e1ade | 12 | Hey, Oshtor. |
| 0x2e1aed | 48 | What's our plan of action if we end up running\n |
| 0x2e1b1e | 20 | into that Vurai guy? |
| 0x2e1b33 | 8 | Vurai... |
| 0x2e1b3c | 43 | Oshtor takes a small breath, then speaks,\n |
| 0x2e1b68 | 28 | his answer quiet and simple. |
| 0x2e1b85 | 20 | We do not fight him. |
| 0x2e1b9a | 42 | Yet I am afraid that may be unavoidable... |
| 0x2e1bc5 | 34 | Eheh, I suppose that sums it up... |
| 0x2e1be8 | 40 | We all knew it might come to this, yeah? |
| 0x2e1c11 | 47 | Indeed. How do I prove my loyalty if I do not\n |
| 0x2e1c41 | 38 | vanquish those that oppose the throne? |
| 0x2e1c68 | 49 | If that is my sister's decision, I have nothing\n |
| 0x2e1c9a | 15 | further to add. |
| 0x2e1caa | 49 | I'll take 'em all down! Oh, but I'll leave some\n |
| 0x2e1cdc | 15 | for you, Kiwru. |
| 0x2e1cec | 47 | Shinonon, please don't do anything dangerous... |
| 0x2e1d1c | 46 | Thankfully, our banter somewhat lightens the\n |
| 0x2e1d4b | 35 | heavy atmosphere that surrounds us. |
| 0x2e1d6f | 48 | But... The only reason we're talking like this\n |
| 0x2e1da0 | 46 | is because we all understand the danger ahead. |
| 0x2e1dcf | 32 | Isn't there something we can do? |
| 0x2e1df0 | 15 | I'm afraid not. |
| 0x2e1e00 | 47 | Without the Akuruka in my possession, we have\n |
| 0x2e1e30 | 33 | no sure way of stopping that man. |
| 0x2e1e52 | 49 | In a direct confrontation, we would most likely\n |
| 0x2e1e84 | 44 | be consumed by his flames... Reduced to ash. |
| 0x2e1eb1 | 14 | ...Direct, eh? |
| 0x2e1ec0 | 46 | So you're saying if we fight him INDIRECTLY,\n |
| 0x2e1eef | 21 | we might have a shot? |
| 0x2e1f05 | 46 | We may stare death in the face, but we would\n |
| 0x2e1f34 | 32 | have... the slimmest of chances. |
| 0x2e1f55 | 47 | There is but one moment in which we may grasp\n |
| 0x2e1f85 | 44 | victory--the moment when he calls upon his\n |
| 0x2e1fb2 | 8 | Akuruka. |
| 0x2e1fbb | 51 | If we force him to use his full strength, he will\n |
| 0x2e1fef | 33 | release the power of the Akuruka. |
| 0x2e2011 | 27 | The power of the Akuruka... |
| 0x2e202d | 27 | Um... So does that mean...? |
| 0x2e2049 | 52 | Nekone and Rulutieh stop themselves mid-utterance,\n |
| 0x2e207e | 25 | and everyone goes silent. |
| 0x2e2098 | 46 | Hold on. Release its power...? You mean that\n |
| 0x2e20c7 | 27 | giant transformation thing? |
| 0x2e20e3 | 50 | ...Our chances are looking pretty grim as it is.\n |
| 0x2e2116 | 45 | I didn't think you could make it sound MORE\n |
| 0x2e2144 | 9 | hopeless. |
| 0x2e214e | 41 | Imagine the Akuruka as a locked door...\n |
| 0x2e2178 | 47 | behind which, power lies. The lock must first\n |
| 0x2e21a8 | 11 | be removed. |
| 0x2e21b4 | 47 | And this process, this unlocking, takes time.\n |
| 0x2e21e4 | 46 | It requires that the wielder focus their mind. |
| 0x2e2213 | 49 | In that moment, he will have to stop and become\n |
| 0x2e2245 | 11 | vulnerable. |
| 0x2e2251 | 47 | He would be unable to counter us... unable to\n |
| 0x2e2281 | 42 | even defend himself. A golden opportunity. |
| 0x2e22ac | 42 | ...That's when we'd all pile on him, then? |
| 0x2e22d7 | 48 | So how likely do you think it is that we could\n |
| 0x2e2308 | 33 | take him down in that one moment? |
| 0x2e232a | 44 | This is the man that even Oshtor calls the\n |
| 0x2e2357 | 24 | strongest in all Yamato. |
| 0x2e2370 | 46 | Vulnerable or not, if we can't shut him down\n |
| 0x2e239f | 48 | in that one moment, what the hell do we do next? |
| 0x2e23d0 | 43 | I would not say that it is... impossible... |
| 0x2e23fc | 31 | Great. Thanks. Very reassuring. |
| 0x2e241c | 21 | Excuse me, brother... |
| 0x2e2432 | 50 | What if we aren't able to subdue him in that time? |
| 0x2e2465 | 46 | Ugh, I was deliberately avoiding asking that\n |
| 0x2e2494 | 12 | right out... |
| 0x2e24a1 | 43 | ...We will all be vaporized where we stand. |
| 0x2e24cd | 29 | A silence falls at his words. |
| 0x2e24eb | 6 | Ghh... |
| 0x2e24f2 | 44 | Kiwru's shoulders slump as Nekone shoots a\n |
| 0x2e251f | 19 | cold glare his way. |
| 0x2e2533 | 48 | So we've gotta take on that thing without your\n |
| 0x2e2564 | 44 | help...? You always did like giving me the\n |
| 0x2e2591 | 12 | crappy jobs. |
| 0x2e259e | 51 | ...Wait, don't tell me you intend on fighting him\n |
| 0x2e25d2 | 10 | like THAT? |
| 0x2e25dd | 47 | ...The key to this plan would be making Vurai\n |
| 0x2e260d | 16 | use the Akuruka. |
| 0x2e261e | 37 | He is a man of pride. Of arrogance.\n |
| 0x2e2644 | 48 | If he deems his opponent unworthy, he will not\n |
| 0x2e2675 | 24 | use the Akuruka's might. |
| 0x2e268e | 47 | Thus, we need a way to provoke him to use his\n |
| 0x2e26be | 16 | full strength... |
| 0x2e26cf | 49 | And you think that's enough of a reason for you\n |
| 0x2e2701 | 21 | to go up against him? |
| 0x2e2717 | 42 | Don't even joke about that! Look at you.\n |
| 0x2e2742 | 45 | All you could do like that is get in the way. |
| 0x2e2770 | 43 | And besides, they've still got your mask,\n |
| 0x2e279c | 6 | right? |
| 0x2e27a3 | 50 | If it's all the same to you... I'd prefer not to\n |
| 0x2e27d6 | 46 | see my best friend ripped to shreds in front\n |
| 0x2e2805 | 6 | of me. |
| 0x2e280c | 10 | Brother... |
| 0x2e2817 | 10 | And yet... |
| 0x2e2822 | 46 | Oshtor, I wouldn't underestimate these guys.\n |
| 0x2e2851 | 29 | We're your agents, after all. |
| 0x2e286f | 6 | ...Hm? |
| 0x2e2876 | 42 | We just need General Meatloaf to take us\n |
| 0x2e28a1 | 40 | seriously. So we'll beat him down 'til\n |
| 0x2e28ca | 15 | he's convinced. |
| 0x2e28da | 33 | ...I mean, THEY'LL beat him down. |
| 0x2e28fc | 32 | ...Not including yourself, then? |
| 0x2e291d | 49 | Don't be ridiculous. What could I do against him? |
| 0x2e294f | 50 | And here I was almost impressed by your words...\n |
| 0x2e2982 | 20 | How foolish of me... |
| 0x2e2997 | 46 | It's called sending the right person for the\n |
| 0x2e29c6 | 45 | right job. And besides, I don't wanna steal\n |
| 0x2e29f4 | 17 | anyone's thunder. |
| 0x2e2a06 | 52 | Hee hee, I really get to go all out against Vurai?\n |
| 0x2e2a3b | 37 | An Akuruturuka, just like Oshtor...\n |
| 0x2e2a61 | 13 | I can't wait! |
| 0x2e2a6f | 49 | Ho boy. I gotta fight Yamato's best warrior...?\n |
| 0x2e2aa1 | 45 | Well, you're the boss, boss. Heh heh heh...\n |
| 0x2e2acf | 19 | This oughta be fun. |
| 0x2e2ae3 | 43 | Dear sister, I understand your sentiment,\n |
| 0x2e2b0f | 25 | but you must remain calm. |
| 0x2e2b29 | 40 | I know, but... it twists me up inside,\n |
| 0x2e2b52 | 36 | not knowing if Her Highness is safe. |
| 0x2e2b77 | 48 | Your Highness, I shall rescue you, I swear it... |
| 0x2e2ba8 | 52 | So that's how it is. You leave the fighting to us.\n |
| 0x2e2bdd | 49 | Just kick back and watch while you get some rest. |
| 0x2e2c0f | 50 | I mean, isn't this the kind of crap you hired us\n |
| 0x2e2c42 | 23 | for in the first place? |
| 0x2e2c5a | 51 | Haku's right, I think. And besides, our objective\n |
| 0x2e2c8e | 45 | is to save the princess, not eliminate Vurai. |
| 0x2e2cbc | 47 | As long as we're able to secure the princess,\n |
| 0x2e2cec | 7 | we win. |
| 0x2e2cf4 | 27 | Hm... Yes, you are correct. |
| 0x2e2d10 | 50 | And let me remind you that this is the last time\n |
| 0x2e2d43 | 48 | any of us are going to pull this dangerous crap! |
| 0x2e2d74 | 48 | And you'd better have a nice fat reward ready!\n |
| 0x2e2da5 | 44 | I don't want this turning into a total bust. |
| 0x2e2dd2 | 51 | Oh? Mere reward pay...? If you save Her Highness,\n |
| 0x2e2e06 | 38 | you could have status, reputation...\n |
| 0x2e2e2d | 41 | You could be an owlo, should you wish it. |
| 0x2e2e57 | 48 | Yyyyeah, I don't really care about that stuff.\n |
| 0x2e2e88 | 43 | Sounds like an easy way to get roped into\n |
| 0x2e2eb4 | 14 | more bullshit. |
| 0x2e2ec3 | 50 | All I need is enough money to live the rich life\n |
| 0x2e2ef6 | 19 | for a little while. |
| 0x2e2f0a | 25 | Heh... How very like you. |
| 0x2e2f24 | 50 | Very well. I shall accept your offer, and remain\n |
| 0x2e2f57 | 22 | in the back this time. |
| 0x2e2f6e | 22 | Good. Glad to hear it. |
| 0x2e2f85 | 8 | Nghhh... |
| 0x2e2f8e | 10 | ...Scared? |
| 0x2e2f99 | 44 | I-I would be useless... against one of the\n |
| 0x2e2fc6 | 24 | Eight Pillar Generals... |
| 0x2e2fdf | 50 | I don't blame him. What with the others being so\n |
| 0x2e3012 | 49 | eager, I forgot that this is the normal reaction. |
| 0x2e3044 | 40 | I know I sound like a coward... but...\n |
| 0x2e306d | 8 | but I... |
| 0x2e3076 | 35 | You have no reason to feel shame.\n |
| 0x2e309a | 45 | It is natural to hold fear for the unknown,\n |
| 0x2e30c8 | 24 | and for unmatched power. |
| 0x2e30e1 | 35 | But... I do not have the courage... |
| 0x2e3105 | 10 | Courage... |
| 0x2e3110 | 23 | Kiwru. What is courage? |
| 0x2e3128 | 4 | Huh? |
| 0x2e312d | 43 | Courage is a heart that conquers its fears. |
| 0x2e3159 | 33 | It is not one that denies fear.\n |
| 0x2e317b | 44 | It is one that accepts fear, and finds its\n |
| 0x2e31a8 | 21 | strength within that. |
| 0x2e31be | 45 | Courage without doubt is mere recklessness.\n |
| 0x2e31ec | 44 | True courage is never born without fear...\n |
| 0x2e3219 | 36 | They are two sides of the same coin. |
| 0x2e323e | 48 | What is important is how you face those fears.\n |
| 0x2e326f | 46 | So feel no shame in cowardice. You must only\n |
| 0x2e329e | 23 | accept and confront it. |
| 0x2e32b6 | 48 | Kiwru... courage is already within your grasp.\n |
| 0x2e32e7 | 38 | You need only take the first step...\n |
| 0x2e330e | 29 | You must believe in yourself. |
| 0x2e332c | 21 | Believe in myself...? |
| 0x2e3342 | 50 | Kiwru, if you really think this will be too much\n |
| 0x2e3375 | 30 | for you, you can duck out now. |
| 0x2e3394 | 5 | Wha-- |
| 0x2e339a | 50 | Nobody's gonna think any less of you for wanting\n |
| 0x2e33cd | 46 | out of something this crazy. Not me, and not\n |
| 0x2e33fc | 7 | Oshtor. |
| 0x2e3404 | 28 | Are you not afraid, Haku!?\n |
| 0x2e3421 | 9 | This is-- |
| 0x2e342b | 43 | 'Course I'm afraid! I'd love to just drop\n |
| 0x2e3457 | 40 | everything and get the hell out of here. |
| 0x2e3480 | 19 | Then why do you...? |
| 0x2e3494 | 48 | 'Cause if I did, I'd never sleep well at night\n |
| 0x2e34c5 | 51 | again. I don't think I've got it in me to run away. |
| 0x2e34f9 | 51 | Nobody'll judge me for running now, but if I did,\n |
| 0x2e352d | 44 | I couldn't live with myself for abandoning\n |
| 0x2e355a | 11 | everything. |
| 0x2e3566 | 46 | So I figure... It's a lot easier to face off\n |
| 0x2e3595 | 46 | with this guy then spend the rest of my life\n |
| 0x2e35c4 | 14 | hating myself. |
| 0x2e35d3 | 26 | That's all there is to it. |
| 0x2e35ee | 9 | I... I... |
| 0x2e35f8 | 34 | So, Kiwru, what do you want to do? |
| 0x2e361b | 10 | I'll go... |
| 0x2e3626 | 51 | I'm not sure if... I know how to believe in myself. |
| 0x2e365a | 38 | But... I agree... If I run now, I...\n |
| 0x2e3681 | 44 | I'll never be able to forgive myself for it. |
| 0x2e36ae | 8 | Kiwru... |
| 0x2e36b7 | 9 | Y-Yes...? |
| 0x2e36c1 | 47 | You have done well. You have taken that first\n |
| 0x2e36f1 | 13 | step forward. |
| 0x2e36ff | 7 | Huh...? |
| 0x2e3707 | 46 | You choose to move forward, even through the\n |
| 0x2e3736 | 48 | fear. That's courage. That's why he's praising\n |
| 0x2e3767 | 4 | you. |
| 0x2e376c | 22 | So take pride in that. |
| 0x2e3783 | 21 | A-Ah... Th-Thank you! |
| 0x2e3799 | 30 | Rulutieh, are you all right?\n |
| 0x2e37b8 | 30 | Not pushing yourself too hard? |
| 0x2e37d7 | 52 | No... I'm a little scared... but Cocopo's with me.\n |
| 0x2e380c | 48 | And... I believe in Sir Haku. I know he can do\n |
| 0x2e383d | 7 | this... |
| 0x2e3856 | 27 | I see... Mhm. You're right. |
| 0x2e3872 | 37 | Haha... Give it your best shot, Haku. |
| 0x2e3898 | 38 | Wait, what are you even talking about? |
| 0x2e38bf | 50 | ...But even if we can make him use the Akuruka's\n |
| 0x2e38f2 | 45 | powers, that's where our real problems start. |
| 0x2e3920 | 53 | If we can't finish him in that one moment when he's\n |
| 0x2e3956 | 37 | wide open, it's all going to be over. |
| 0x2e397c | 48 | I told Oshtor to leave it to us, but I need to\n |
| 0x2e39ad | 29 | think of some kind of plan... |
| 0x2e39cb | 10 | *Tug, tug* |
| 0x2e39d6 | 6 | ...Mm? |
| 0x2e39dd | 47 | I feel someone pulling at my sleeve, and turn\n |
| 0x2e3a0d | 40 | to see the twins staring straight at me. |
| 0x2e3a36 | 7 | Master. |
| 0x2e3a3e | 30 | You may leave that role to us. |
| 0x2e3a5d | 8 | ...What? |
| 0x2e3a66 | 30 | We are the Kamunagi of Chains. |
| 0x2e3a85 | 50 | We have the means to subdue those who bare their\n |
| 0x2e3ab8 | 21 | fangs against Yamato. |
| 0x2e3ace | 7 | You do? |
| 0x2e3ad6 | 25 | The Kamunagi of Chains... |
| 0x2e3af0 | 46 | Oshtor seems to have noticed something as he\n |
| 0x2e3b1f | 13 | mutters this. |
| 0x2e3b2d | 49 | I have heard they are able to seal away any who\n |
| 0x2e3b5f | 40 | become a threat to the imperial capital. |
| 0x2e3b88 | 29 | Are the rumors true, then...? |
| 0x2e3ba6 | 47 | Hey, a little context would be great, thanks.\n |
| 0x2e3bd6 | 42 | These two are the Kamunagi of Chains, and? |
| 0x2e3c01 | 41 | It is said that the imperial capital is\n |
| 0x2e3c2b | 47 | equipped with certain countermeasures against\n |
| 0x2e3c5b | 11 | calamities. |
| 0x2e3c67 | 46 | And the ones that reign over them... are the\n |
| 0x2e3c96 | 19 | Kamunagi of Chains. |
| 0x2e3caa | 48 | Some say that whoever controls the Kamunagi of\n |
| 0x2e3cdb | 44 | Chains holds the imperial capital in their\n |
| 0x2e3d08 | 7 | palm... |
| 0x2e3d10 | 49 | It all makes sense now. That's why everyone got\n |
| 0x2e3d42 | 43 | so worked up when they were gifted to me... |
| 0x2e3d6e | 50 | Now that you mention it... I believe I have read\n |
| 0x2e3da1 | 35 | about that somewhere. If I recall-- |
| 0x2e3dc5 | 46 | The Kamunagi of Chains have a way of sealing\n |
| 0x2e3df4 | 36 | enemies of the imperial capital...\n |
| 0x2e3e19 | 15 | the Ohn Riyaak. |
| 0x2e3e29 | 25 | Ohn Riyaak... Is that...? |
| 0x2e3e43 | 10 | Miss Kuon? |
| 0x2e3e4e | 33 | Oh... Uh, I suppose it's nothing. |
| 0x2e3e70 | 37 | ...How did Yamato get ahold of it...? |
| 0x2e3e96 | 44 | So you two are saying you can take care of\n |
| 0x2e3ec3 | 6 | Vurai? |
| 0x2e3eca | 40 | We shall execute your wish without fail. |
| 0x2e3ef3 | 44 | If they're this confident, it has to be an\n |
| 0x2e3f20 | 42 | effective method... But the pair of them\n |
| 0x2e3f4b | 15 | look exhausted. |
| 0x2e3f5b | 46 | They must have used too much of their powers\n |
| 0x2e3f8a | 39 | on the way here... They look ready to\n |
| 0x2e3fb2 | 9 | collapse. |
| 0x2e3fbc | 46 | ...Haku, I'm not sure they can take much more. |
| 0x2e3feb | 7 | Yeah... |
| 0x2e3ff3 | 47 | I've heard overusing spells can kill someone.\n |
| 0x2e4023 | 43 | I don't know how much more they can take... |
| 0x2e404f | 13 | No other way. |
| 0x2e405d | 44 | To put it plainly, the only ones currently\n |
| 0x2e408a | 44 | capable of subduing an Akuruturuka are the\n |
| 0x2e40b7 | 10 | two of us. |
| 0x2e40c2 | 26 | Please. Give us the order. |
| 0x2e40dd | 35 | The twins meet my eyes, resolute.\n |
| 0x2e4101 | 43 | Something tells me that even if I say no,\n |
| 0x2e412d | 20 | they'll still do it. |
| 0x2e4142 | 37 | ...You guys sure you can pull it off? |
| 0x2e4168 | 19 | The two nod curtly. |
| 0x2e417c | 13 | Without fail. |
| 0x2e418a | 35 | We shall seal him once and for all. |
| 0x2e41ae | 41 | ...All right. I'll leave it to you, then. |
| 0x2e41d8 | 26 | Are you sure about this?\n |
| 0x2e41f3 | 11 | Those two-- |
| 0x2e41ff | 45 | I know, but we need to do everything we can\n |
| 0x2e422d | 44 | to improve our chances of winning right now. |
| 0x2e425a | 29 | Even if that means they'll... |
| 0x2e4278 | 51 | ...Remember, though, you two are our last resort.\n |
| 0x2e42ac | 41 | So don't do anything reckless until then. |
| 0x2e42d6 | 12 | As you wish. |
| 0x2e42e3 | 15 | Lady-in-waiting |
| 0x2e42f3 | 42 | We have almost reached her room, everyone. |
| 0x2e431e | 30 | Please... save Her Highness... |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_07.json` com a forma:
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
