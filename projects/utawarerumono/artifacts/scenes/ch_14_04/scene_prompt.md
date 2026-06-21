# Cena ch_14_04 — pacote de traducao (645 linhas)

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
| amamunii | Comida | amamunii | manter_original | none |
| Cohort | Organizacao | Coorte | traduzir | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Onvitaikayan | Termo | Onvitaikayan | manter_original | none |
| Ozen | Personagem | Ozen | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |

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
### Ozen — criticality: low
- Ozen — `voice_criticality: low`. General-Pilar, pai da Rulutieh; registro grave/nobre.
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Yeah!` -> `Isso!` (Bandidos, 13_05)
- `Whoa.` -> `Nossa.` (Haku, 14_01)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `All right.` -> `Tudo bem.` (Haku, 12_08)
- `her mouth.` -> `sobre a boca.` (Haku, 14_02)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `Girl` -> `Garota` (sistema, 13_01)
- `Man` -> `Hom` (Sistema, 12_04)
- `in my head.` -> `me faz imaginar.` (Haku, 13_02)
- `conversation.` -> `normal.` (Kuon, root)
- `Rulutieh.` -> `Rulutieh.` (Haku, 13_02)
- `I think.` -> `acho.` (Kuon, 12_11)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `regardless.` -> `de qualquer forma.` (Ukon, 13_02)
- `right?` -> `né?` (Haku, 12_03)
- `yeah?` -> `tá?` (Ukon, 14_02)
- `Wh--` -> `Q--` (Haku, 11_07)
- `little.` -> `acorda.` (Garota, 12_01)
- `Um.` -> `Ahn.` (Haku, 11_09)
- `Hngh--` -> `Hngh--` (Haku, 12_11)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `That's all.` -> `É isso.` (Ukon, 13_02)
- `...Rulutieh?` -> `...Rulutieh?` (Kuon, 14_03)
- `but...` -> `mas...` (Kuon, 12_16)
- `Urk...` -> `Urgh...` (Haku, 12_06)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `them.` -> `deles.` (Kuon, 11_05)
- `Here you are.` -> `Aqui estão.` (Estalajadeira, 12_04)
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
| 0x8a02e | 43 | All right, everyone. You all got your cups? |
| 0x8a05a | 13 | Ukon's Cohort |
| 0x8a068 | 5 | Yeah! |
| 0x8a06e | 49 | Here's to our triumphant return to the capital,\n |
| 0x8a0a0 | 28 | and to new comrades! Cheers! |
| 0x8a0bd | 7 | Cheers! |
| 0x8a0c5 | 7 | Cheers. |
| 0x8a0cd | 12 | Ch-Cheers... |
| 0x8a0da | 14 | *Gulp*... Ahh. |
| 0x8a0e9 | 47 | At Ukon's toast, Kuon drains her cup in one go. |
| 0x8a119 | 28 | Oh, please have some more... |
| 0x8a136 | 5 | Whoa. |
| 0x8a13c | 5 | Ah... |
| 0x8a142 | 46 | Cold sake after a bath always hits the spot.\n |
| 0x8a171 | 4 | Mmf. |
| 0x8a176 | 46 | Kuon drains her cup as quickly as it filled,\n |
| 0x8a1a5 | 25 | seemingly in a good mood. |
| 0x8a1bf | 46 | Ostensibly, the earlier incident at the bath\n |
| 0x8a1ee | 38 | seems to have been forgotten entirely. |
| 0x8a215 | 46 | Her language and her mannerisms are elegant,\n |
| 0x8a244 | 31 | but she acts like an old man... |
| 0x8a264 | 36 | Glad she's in a good mood, anyway.\n |
| 0x8a289 | 22 | Rulutieh, meanwhile... |
| 0x8a2a0 | 24 | My eyes meet Rulutieh's. |
| 0x8a2bd | 48 | Her face quickly turns red, and she averts her\n |
| 0x8a2ee | 5 | eyes. |
| 0x8a2f4 | 49 | I guess getting HER back in a good mood will be\n |
| 0x8a326 | 18 | a little harder... |
| 0x8a339 | 44 | Hey, kid, what's the deal? Your cup's empty. |
| 0x8a366 | 49 | With bottle in hand and face already reddening,\n |
| 0x8a398 | 42 | Ukon sits down beside us. His men chatter. |
| 0x8a3c3 | 43 | Here, let's toast again. To wonderful new\n |
| 0x8a3ef | 7 | allies! |
| 0x8a3f7 | 45 | And to the allies who ditched the guests of\n |
| 0x8a425 | 47 | honor and started the festivities without them. |
| 0x8a455 | 26 | Ah, that's the good stuff. |
| 0x8a470 | 31 | Hey, don't ignore me over here. |
| 0x8a490 | 46 | Bahahaha! C'mon, what's the fuss? You got to\n |
| 0x8a4bf | 42 | feast your eyes and got off pretty easy,\n |
| 0x8a4ea | 11 | didn't you? |
| 0x8a4f6 | 34 | Ukon raises his cup in good humor. |
| 0x8a519 | 7 | Ungh... |
| 0x8a521 | 44 | I get his logic, but that's not really the\n |
| 0x8a54e | 26 | response I was hoping for. |
| 0x8a569 | 47 | ...But strangely enough, I can't bring myself\n |
| 0x8a599 | 41 | to be mad at this guy. He's got this...\n |
| 0x8a5c3 | 17 | magnetism to him. |
| 0x8a5d5 | 18 | Ah, that's good... |
| 0x8a5e8 | 44 | Here. You were late, so you've gotta drink\n |
| 0x8a615 | 28 | three cups. That's the rule. |
| 0x8a632 | 15 | ...Allies, huh. |
| 0x8a642 | 22 | Phew. Here, your turn. |
| 0x8a659 | 10 | All right. |
| 0x8a664 | 46 | Ahhh. After a job well done, that's just the\n |
| 0x8a693 | 6 | stuff. |
| 0x8a69a | 48 | Come to think of it, we've been traveling with\n |
| 0x8a6cb | 27 | Ukon for over ten days now. |
| 0x8a6e7 | 46 | ...And I don't think I can count on one hand\n |
| 0x8a716 | 42 | the number of times we've been in mortal\n |
| 0x8a741 | 7 | danger. |
| 0x8a749 | 49 | I never even dreamed that things would play out\n |
| 0x8a77b | 24 | like this when we met... |
| 0x8a794 | 27 | But it hasn't all been bad. |
| 0x8a7b0 | 26 | Here, Haku, this is yours. |
| 0x8a7cb | 48 | Kuon passes an enormous, stuffed amamunii to me. |
| 0x8a7fc | 47 | Joyfully, she tucks into another from a stack\n |
| 0x8a82c | 21 | waiting on her plate. |
| 0x8a842 | 14 | Mm! Delicious. |
| 0x8a851 | 47 | Kuon sighs with a distant, dreamy look in her\n |
| 0x8a881 | 34 | She really enjoys her food, huh?\n |
| 0x8a8a4 | 40 | Glad she's having a good time, at least. |
| 0x8a8cd | 47 | She was in a foul mood all the way over here,\n |
| 0x8a8fd | 46 | but as soon as she saw the meal, her spirits\n |
| 0x8a92c | 7 | lifted. |
| 0x8a934 | 47 | Good to know for the future. I'll have to buy\n |
| 0x8a964 | 44 | her an expensive meal next time I upset her. |
| 0x8a991 | 47 | I've been feeling Rulutieh's eyes on me for a\n |
| 0x8a9c1 | 48 | while now, but whenever I look toward her, she\n |
| 0x8a9f2 | 11 | looks away. |
| 0x8a9fe | 48 | I did see her naked. That's probably a natural\n |
| 0x8aa2f | 32 | reaction, all things considered. |
| 0x8aa50 | 44 | ...Still, I can't help but feel like she's\n |
| 0x8aa7d | 40 | avoiding me. That's a little depressing. |
| 0x8aaa6 | 43 | I'll have to apologize to her again, later. |
| 0x8aad2 | 31 | Here, Rulutieh. You should eat. |
| 0x8aaf2 | 10 | Huh? Oh... |
| 0x8aafd | 31 | Kuon proffers another amamunii. |
| 0x8ab1d | 12 | Thank you... |
| 0x8ab2a | 47 | Flustered, Rulutieh tries to accept the food,\n |
| 0x8ab5a | 48 | but Kuon bypasses her hands and goes right for\n |
| 0x8ab8b | 10 | her mouth. |
| 0x8ab96 | 4 | Huh? |
| 0x8ab9b | 17 | Here, say "ah..." |
| 0x8abad | 10 | H-Huh? Uh? |
| 0x8abb8 | 3 | Ah. |
| 0x8abbc | 8 | I, um... |
| 0x8abc5 | 4 | Ah!? |
| 0x8abca | 14 | Um... ah...?\n |
| 0x8abd9 | 12 | Mmf... mm... |
| 0x8abe6 | 18 | Ahaha. Taste good? |
| 0x8abf9 | 12 | Um... y-yes. |
| 0x8ac06 | 46 | Pleased, Kuon takes the wrap and holds it up\n |
| 0x8ac35 | 29 | to Rulutieh's lips once more. |
| 0x8ac53 | 37 | All right, then, have another bite.\n |
| 0x8ac79 | 9 | Say "ah." |
| 0x8ac83 | 5 | Um... |
| 0x8ac89 | 13 | C'mon, ah?♪ |
| 0x8ac97 | 12 | Ah... mmf... |
| 0x8aca4 | 18 | And another toast! |
| 0x8acb7 | 22 | O-Oh, um... Cheers...? |
| 0x8acce | 47 | ...Is Kuon trying to be considerate and break\n |
| 0x8acfe | 15 | the ice, or...? |
| 0x8ad0e | 48 | It feels like all she's doing is making things\n |
| 0x8ad3f | 18 | even more awkward. |
| 0x8ad52 | 40 | Hey, kid. Empty cup. You know the rules. |
| 0x8ad7b | 10 | Oh, yeah-- |
| 0x8ad86 | 47 | Master Haku!? Pri-THEE, a drink! A drink with\n |
| 0x8adb6 | 25 | thy BOSHOM friend Maroro! |
| 0x8add0 | 48 | Maroro's white face suddenly materializes from\n |
| 0x8ae01 | 42 | the crowd, poking into my field of vision. |
| 0x8ae2c | 16 | Oh, you're here. |
| 0x8ae3d | 38 | SHUCH ill manner! Of COURSH I am here. |
| 0x8ae64 | 22 | He's totally wasted... |
| 0x8ae7b | 47 | Ah, there you go. Maroro, fill the kid's cup,\n |
| 0x8aeab | 8 | wouldja? |
| 0x8aeb4 | 16 | It shall be sho! |
| 0x8aec5 | 34 | Now, MASHTER Haku, thou shalt dr-- |
| 0x8aee8 | 3 | Oh? |
| 0x8aeec | 47 | The reception room door slams open with great\n |
| 0x8af1c | 23 | force, cutting him off. |
| 0x8af34 | 38 | At the interruption, the chatter and\n |
| 0x8af5b | 37 | merrymaking quiets, then goes silent. |
| 0x8af81 | 40 | Everyone turns to look at the open door. |
| 0x8afaa | 4 | Girl |
| 0x8afaf | 44 | Across the threshold stands a cute, albeit\n |
| 0x8afdc | 26 | grumpy-looking young girl. |
| 0x8aff7 | 11 | Who's that? |
| 0x8b003 | 31 | And just as I begin to wonder-- |
| 0x8b023 | 3 | Man |
| 0x8b027 | 11 | Yeeeaaahhh! |
| 0x8b033 | 30 | Hey, we've been waitin' on ya! |
| 0x8b052 | 7 | Nekone! |
| 0x8b05a | 49 | Adoring cheers--well, more like adoring drunken\n |
| 0x8b08c | 28 | shouts--go up among the men. |
| 0x8b0a9 | 6 | ...Uh. |
| 0x8b0b0 | 38 | The girl--apparently called Nekone--\n |
| 0x8b0d7 | 32 | flinches at that, but recovers\n |
| 0x8b0f8 | 33 | quickly, crossing the room to me. |
| 0x8b11a | 39 | And just what are you doing, pray tell? |
| 0x8b142 | 49 | She plants her feet in front of me and gives me\n |
| 0x8b174 | 16 | a weighty glare. |
| 0x8b185 | 34 | What's with her all of a sudden?\n |
| 0x8b1a8 | 19 | Who is she, anyway? |
| 0x8b1bc | 40 | She's cute, but she seems awfully scary. |
| 0x8b1e5 | 47 | And furthermore... why is she reprimanding me\n |
| 0x8b215 | 41 | if this is the first time we've ever met? |
| 0x8b23f | 37 | I am speaking to you, dear brother.\n |
| 0x8b265 | 24 | Just what are you doing? |
| 0x8b27e | 47 | D-Dear... brother? Wait, she's not talking to\n |
| 0x8b2ae | 37 | me, she's looking... behind me. At... |
| 0x8b2d4 | 47 | Hey, Nekone! Great timing. C'mon and join us,\n |
| 0x8b304 | 9 | won'tcha? |
| 0x8b30e | 37 | Ukon's... sister? THIS is his sister? |
| 0x8b334 | 47 | In the haze of alcohol, I don't quite realize\n |
| 0x8b364 | 46 | I said that out loud until Nekone is staring\n |
| 0x8b393 | 6 | at me. |
| 0x8b39a | 33 | What, something weird about that? |
| 0x8b3bc | 27 | No, I wouldn't say weird... |
| 0x8b3d8 | 45 | As they stand face-to-face with each other,\n |
| 0x8b406 | 27 | I mentally compare the two. |
| 0x8b422 | 47 | A cute, petite girl and a bearded, boisterous\n |
| 0x8b452 | 4 | man. |
| 0x8b457 | 44 | Rather than siblings, they're more like...\n |
| 0x8b484 | 17 | father and child? |
| 0x8b496 | 48 | Nekone's grumpy expression grows even grumpier\n |
| 0x8b4c7 | 48 | as--once again--I fail to keep my observations\n |
| 0x8b4f8 | 11 | in my head. |
| 0x8b504 | 49 | Eh? C'mon, Nekone, what's with that scary face?\n |
| 0x8b536 | 45 | You're gonna scare all the boys away, y'know. |
| 0x8b564 | 31 | That is none of your concern.\n |
| 0x8b584 | 33 | Besides, boys interest me little. |
| 0x8b5a6 | 43 | Well, you can't stay clingin' to your big\n |
| 0x8b5d2 | 47 | brother forever, kiddo. You'll be of age soon\n |
| 0x8b602 | 7 | enough. |
| 0x8b60a | 45 | Never mind all that. What are you doing here? |
| 0x8b638 | 46 | Your long-awaited return to the capital, and\n |
| 0x8b667 | 46 | the first thing you do is get wasted instead\n |
| 0x8b696 | 10 | of report? |
| 0x8b6a1 | 36 | What exactly is the meaning of this? |
| 0x8b6c6 | 44 | Ah, I've got guys takin' care of all that.\n |
| 0x8b6f3 | 16 | Don't you worry. |
| 0x8b704 | 45 | This is not a task you can simply delegate.\n |
| 0x8b732 | 35 | It requires your personal presence. |
| 0x8b756 | 44 | Bah! Don't say stuff like that. We need to\n |
| 0x8b783 | 46 | welcome our new allies, and reward ourselves\n |
| 0x8b7b2 | 13 | for our work! |
| 0x8b7c0 | 45 | Which reminds me--since I'm not gonna get a\n |
| 0x8b7ee | 45 | better opportunity... This here's my little\n |
| 0x8b81c | 7 | sister. |
| 0x8b824 | 49 | Ukon turns toward me, introducing Nekone with a\n |
| 0x8b856 | 34 | jab of his thumb in her direction. |
| 0x8b879 | 47 | She's a good kid. I don't deserve her at all.\n |
| 0x8b8a9 | 45 | She might be a little stiff, but I hope you\n |
| 0x8b8d7 | 10 | get along. |
| 0x8b8e2 | 20 | Urk--ah. A pleasure. |
| 0x8b8f7 | 45 | The girl bows uncomfortably, seemingly only\n |
| 0x8b925 | 41 | just now realizing I was party to their\n |
| 0x8b94f | 13 | conversation. |
| 0x8b95d | 43 | The hapless-lookin' kid here is Haku, the\n |
| 0x8b989 | 46 | beauty over there's Kuon, and the cute one's\n |
| 0x8b9b8 | 9 | Rulutieh. |
| 0x8b9c2 | 31 | Nice to meet y--Hey, "hapless"? |
| 0x8b9e2 | 34 | My name is Kuon. Nice to meet you. |
| 0x8ba05 | 47 | Oh, I'm Rulutieh... I-It's a pleasure to make\n |
| 0x8ba35 | 18 | your acquaintance. |
| 0x8ba48 | 45 | ...I would rather you not change the subject. |
| 0x8ba76 | 27 | Now, now, dear LADY Nekone! |
| 0x8ba92 | 43 | A drunken Maroro sticks his face into the\n |
| 0x8babe | 42 | We merry lot are in the very MIDSHT of a\n |
| 0x8bae9 | 47 | SHELEBRATION. Pray banish aught upon thy face\n |
| 0x8bb19 | 18 | but shmiles aglow! |
| 0x8bb2c | 45 | I thank you for your opinion on the matter,\n |
| 0x8bb5a | 48 | o great and masterful scholar, who art full of\n |
| 0x8bb8b | 8 | himself. |
| 0x8bb94 | 47 | Nekone gives Maroro a flat, unamused look, as\n |
| 0x8bbc4 | 43 | though regarding a dead insect in her food. |
| 0x8bbf0 | 33 | Urk--N-Nay, good lady, I meant... |
| 0x8bc12 | 47 | Maroro trails off, then returns to the corner\n |
| 0x8bc42 | 47 | of the room, holding his knees and dissolving\n |
| 0x8bc72 | 10 | into sobs. |
| 0x8bc7d | 49 | Bwahaha! C'mon, don't be so angry all the time.\n |
| 0x8bcaf | 44 | Your cute face is gonna get stuck like that. |
| 0x8bcdc | 20 | Tch. I am NOT angry. |
| 0x8bcf1 | 48 | If I look angry, it is anger you have given me\n |
| 0x8bd22 | 24 | cause for, dear brother. |
| 0x8bd3b | 49 | Nekone glares at Ukon, but there's a note of...\n |
| 0x8bd6d | 22 | sadness in there, too. |
| 0x8bd84 | 27 | Ukon, this simply won't do. |
| 0x8bda0 | 47 | I appreciate the hospitality you've shown us,\n |
| 0x8bdd0 | 46 | but really, you should have gone to see your\n |
| 0x8bdff | 13 | sister first. |
| 0x8be0d | 47 | ...So she's sulking because her older brother\n |
| 0x8be3d | 31 | isn't giving her any attention? |
| 0x8be5d | 48 | She was lonely while he was away, only to find\n |
| 0x8be8e | 48 | out he forsook her for merrymaking when he got\n |
| 0x8bebf | 7 | back... |
| 0x8bec7 | 42 | And that's why she's gotten all worked up. |
| 0x8bef2 | 47 | Poor thing. See, look how worried you've made\n |
| 0x8bf22 | 10 | her, Ukon. |
| 0x8bf2d | 49 | If you have a younger sibling who worries about\n |
| 0x8bf5f | 46 | you, it's your duty to show her you're safe,\n |
| 0x8bf8e | 8 | I think. |
| 0x8bf97 | 6 | Ngh... |
| 0x8bf9e | 48 | It's not like this was anything worth worrying\n |
| 0x8bfcf | 33 | over. No more than usual, anyway. |
| 0x8bff1 | 44 | I go on excursions like that all the time!\n |
| 0x8c01e | 47 | She knows it's no big deal. I always come back. |
| 0x8c04e | 43 | I think whether she worries is up to her,\n |
| 0x8c07a | 14 | not you, Ukon. |
| 0x8c089 | 48 | No matter how much you rationalize it, anxiety\n |
| 0x8c0ba | 42 | is rarely subject to logic. She'll worry\n |
| 0x8c0e5 | 11 | regardless. |
| 0x8c0f1 | 25 | That's how it is, huh...? |
| 0x8c10b | 45 | That's how it is. As her older brother, you\n |
| 0x8c139 | 23 | should understand that. |
| 0x8c151 | 31 | Nekone stares at Kuon, stunned. |
| 0x8c171 | 6 | Right? |
| 0x8c178 | 4 | I... |
| 0x8c17d | 44 | Noticing Nekone's eyes on her, Kuon smiles\n |
| 0x8c1aa | 41 | sweetly. Nekone's face instantly reddens. |
| 0x8c1d4 | 4 | Hrm. |
| 0x8c1d9 | 29 | Ukon tilts his head, puzzled. |
| 0x8c1f7 | 45 | Seems like he honestly thought there was no\n |
| 0x8c225 | 18 | cause for worry... |
| 0x8c238 | 48 | Having had a few near-death experiences myself\n |
| 0x8c269 | 35 | recently, I have to wonder at that. |
| 0x8c28d | 48 | Does he even realize the underlying reason for\n |
| 0x8c2be | 43 | his sister's anger, let alone her worrying? |
| 0x8c2ea | 47 | He seems like a considerate enough guy, but I\n |
| 0x8c31a | 48 | guess even he has blind spots when it comes to\n |
| 0x8c34b | 7 | family. |
| 0x8c353 | 43 | If that's the case, then I have to feel a\n |
| 0x8c37f | 26 | little sorry for the girl. |
| 0x8c39a | 43 | ...All right, I'll help out a little bit.\n |
| 0x8c3c6 | 43 | Doesn't hurt anyone to be nice to children. |
| 0x8c3f2 | 5 | Ukon. |
| 0x8c3f8 | 5 | Yeah? |
| 0x8c3fe | 47 | Basically, she's sad because you haven't been\n |
| 0x8c42e | 31 | around to pay attention to her. |
| 0x8c44e | 44 | She's lonely and wants you to see that, so\n |
| 0x8c47b | 45 | she's sulking and making a scene. Won't you\n |
| 0x8c4a9 | 11 | notice her? |
| 0x8c4b5 | 4 | Wh-- |
| 0x8c4ba | 11 | Wha... I... |
| 0x8c4c6 | 42 | Ah... That's what this was all about, huh? |
| 0x8c4f1 | 34 | What are you talking about? That-- |
| 0x8c514 | 43 | I'm sorry for not noticing how lonely you\n |
| 0x8c540 | 13 | were, Nekone. |
| 0x8c54e | 7 | ...ngh. |
| 0x8c556 | 41 | Haha, look at her getting all shy, now.\n |
| 0x8c580 | 25 | No need to thank me, kid. |
| 0x8c59a | 29 | Feels good to do nice things. |
| 0x8c5b8 | 13 | Upsy-daisy.\n |
| 0x8c5c6 | 28 | Ha, you're as light as ever. |
| 0x8c5e3 | 48 | Ukon gently--bodily--lifts Nekone and puts her\n |
| 0x8c614 | 22 | on his knee, laughing. |
| 0x8c62b | 14 | What are y--!? |
| 0x8c63a | 47 | She wriggles, resisting, but ultimately gives\n |
| 0x8c66a | 34 | in as Ukon begins to pat her head. |
| 0x8c68d | 47 | You've grown a whole lot, y'know? You stopped\n |
| 0x8c6bd | 48 | demanding attention like you did when you were\n |
| 0x8c6ee | 7 | little. |
| 0x8c6f6 | 46 | So I just assumed you didn't need me as much\n |
| 0x8c725 | 9 | any more. |
| 0x8c72f | 17 | I... I was NOT... |
| 0x8c741 | 45 | Nekone tries to deny it vehemently, but her\n |
| 0x8c76f | 45 | objections grow quieter and quieter as Ukon\n |
| 0x8c79d | 17 | continues to pat. |
| 0x8c7af | 31 | I really am a bad brother, huh. |
| 0x8c7cf | 28 | Th-That... That is not true. |
| 0x8c7ec | 45 | Bahaha! Been a while since we've done this,\n |
| 0x8c81a | 10 | hasn't it? |
| 0x8c825 | 34 | Dear brother, you reek of alcohol. |
| 0x8c848 | 45 | Nekone turns away from Ukon, but remains on\n |
| 0x8c876 | 27 | his lap, unwilling to move. |
| 0x8c892 | 18 | Ha! Sorry, my bad. |
| 0x8c8a5 | 16 | ...Dear brother. |
| 0x8c8b6 | 13 | Welcome home. |
| 0x8c8c4 | 25 | Yeah. 's good to be back. |
| 0x8c8de | 43 | Everyone around the two siblings shares a\n |
| 0x8c90a | 33 | smile, seeing how close they are. |
| 0x8c92c | 48 | But I gotta say, I'm relieved you're growing up. |
| 0x8c95d | 48 | You used to throw these tantrums when you were\n |
| 0x8c98e | 46 | little, demanding that we take baths together. |
| 0x8c9bd | 3 | Um. |
| 0x8c9c1 | 44 | You've stopped doin' that, and you stopped\n |
| 0x8c9ee | 46 | crawling into my bed when you couldn't sleep\n |
| 0x8ca1d | 9 | at night. |
| 0x8ca27 | 18 | A bath together... |
| 0x8ca3a | 17 | Someone muttered. |
| 0x8ca4c | 6 | Bed... |
| 0x8ca53 | 20 | She'd climb in, huh? |
| 0x8ca68 | 32 | Ukon's men mutter to themselves. |
| 0x8ca89 | 20 | Um, d-dear brother-- |
| 0x8ca9e | 43 | You don't wake me up to use the privy any\n |
| 0x8caca | 48 | more, either, to say nothin' of the bedwetting-- |
| 0x8cafb | 10 | Wh--Wha--! |
| 0x8cb06 | 45 | She seems mortified that Ukon is airing her\n |
| 0x8cb34 | 34 | embarrassing memories like this... |
| 0x8cb57 | 46 | Nekone writhes on his lap, face crimson, but\n |
| 0x8cb86 | 24 | Ukon remains unaffected. |
| 0x8cb9f | 46 | H-How far back must you dig? I will have you\n |
| 0x8cbce | 43 | know I've not wet the bed in at LEAST two\n |
| 0x8cbfa | 7 | years-- |
| 0x8cc02 | 46 | Nekone cuts herself off, as though realizing\n |
| 0x8cc31 | 44 | her circumstances, casting furtive glances\n |
| 0x8cc5e | 15 | about the room. |
| 0x8cc6e | 36 | Her eyes meet mine, and she freezes. |
| 0x8cc93 | 15 | Two years, huh? |
| 0x8cca3 | 6 | Hngh-- |
| 0x8ccaa | 18 | Two years aback... |
| 0x8ccbd | 12 | Two years... |
| 0x8ccca | 46 | The whispering spreads like wildfire through\n |
| 0x8ccf9 | 10 | the party. |
| 0x8cd06 | 31 | Nekone begins to wriggle again. |
| 0x8cd26 | 45 | ...She's acting like she wants to get away,\n |
| 0x8cd54 | 45 | but she must be comfy, seeing as she hasn't\n |
| 0x8cd82 | 6 | moved. |
| 0x8cd89 | 39 | Maybe she's secretly thankful for the\n |
| 0x8cdb1 | 38 | opportunity for attention from Ukon.\n |
| 0x8cdd8 | 26 | She's still looking at me. |
| 0x8cdf3 | 34 | Look at that earnest expression.\n |
| 0x8ce16 | 21 | She's such a darling. |
| 0x8ce2c | 44 | I guess it can't be helped. C'mon, you can\n |
| 0x8ce59 | 31 | thank me out loud if you wanna. |
| 0x8ce79 | 26 | Why are you leering at me? |
| 0x8ce94 | 3 | Hm? |
| 0x8ce98 | 44 | Aw, now she's playing it shy. Does she not\n |
| 0x8cec5 | 34 | know how to express her gratitude? |
| 0x8cee8 | 40 | Hey, now, don't talk like that to your\n |
| 0x8cf11 | 19 | brother's comrades. |
| 0x8cf25 | 41 | With another pat on the head from Ukon,\n |
| 0x8cf4f | 20 | Nekone settles down. |
| 0x8cf64 | 39 | Ah, she is a really cute little sister. |
| 0x8cf8c | 4 | Nnh. |
| 0x8cf91 | 23 | Yeah, I'm proud of her. |
| 0x8cfa9 | 8 | I see... |
| 0x8cfb2 | 47 | Once again, it's a pleasure to meet you, Miss\n |
| 0x8cfe2 | 35 | Nekone. Can I just call you Nekone? |
| 0x8d006 | 32 | Eh? Y-Yes, that... That is fine. |
| 0x8d027 | 48 | I'm Kuon. I got to know your big brother while\n |
| 0x8d058 | 39 | I was traveling to broaden my horizons. |
| 0x8d080 | 48 | My favorite foods are sweet things, especially\n |
| 0x8d0b1 | 6 | honey. |
| 0x8d0b8 | 40 | And I like to travel the world and see\n |
| 0x8d0e1 | 28 | different places... I think? |
| 0x8d0fe | 32 | And this is my friend, Rulutieh. |
| 0x8d11f | 4 | Eep. |
| 0x8d124 | 42 | Kuon pulls Rulutieh, who'd been hovering\n |
| 0x8d14f | 44 | silently by her side, into the conversation. |
| 0x8d17c | 27 | Come on, Rulutieh, you too. |
| 0x8d198 | 47 | O-OK. Um... I'm... Rulutieh? I'm the youngest\n |
| 0x8d1c8 | 40 | daughter of the owlo of Kujyuri, s-so... |
| 0x8d1f1 | 46 | Um, my favorite food is yubeshi. And I like,\n |
| 0x8d220 | 33 | um... cooking... and needlepoint. |
| 0x8d242 | 20 | The owlo of Kujyuri? |
| 0x8d257 | 44 | Yep. Her dad's Lord Ozen, one of the Eight\n |
| 0x8d284 | 46 | Pillar Generals and an owlo--which makes her\n |
| 0x8d2b3 | 11 | a princess. |
| 0x8d2bf | 40 | Ah, p-please excuse my rudeness, then.\n |
| 0x8d2e8 | 34 | I was unaware you were a princess. |
| 0x8d30b | 43 | Nekone straightens herself on Ukon's lap,\n |
| 0x8d337 | 20 | bowing respectfully. |
| 0x8d34c | 18 | Ah, yes, w-well... |
| 0x8d35f | 47 | Rulutieh's expression grows faintly sadder as\n |
| 0x8d38f | 44 | Nekone suddenly adopts a formal, rigid tone. |
| 0x8d3bc | 44 | Nekone, you're going about this all wrong,\n |
| 0x8d3e9 | 47 | If you can, I wouldn't worry about stuff like\n |
| 0x8d419 | 46 | that. It would probably make Rulutieh happier. |
| 0x8d448 | 5 | Oh... |
| 0x8d44e | 44 | Ah... Are you from a prestigious family as\n |
| 0x8d47b | 16 | well, Miss Kuon? |
| 0x8d48c | 31 | Me? Ahahaha, do I look like it? |
| 0x8d4ac | 38 | You said honey was your favorite food. |
| 0x8d4d3 | 45 | Such a delicacy, expensive and difficult to\n |
| 0x8d501 | 10 | come by... |
| 0x8d50c | 4 | And? |
| 0x8d511 | 28 | And... how shall I put this? |
| 0x8d52e | 46 | Ahahaha, no, it's all right. My family is in\n |
| 0x8d55d | 45 | trading, so we're just a little better off,\n |
| 0x8d58b | 11 | that's all. |
| 0x8d597 | 8 | I-I see. |
| 0x8d5a0 | 46 | Nekone nods, but doesn't quite seem convinced. |
| 0x8d5cf | 49 | Miss Nekone... J-Just as Miss Kuon said, I'd...\n |
| 0x8d601 | 40 | prefer if you just called me Rulutieh... |
| 0x8d62a | 27 | V-Very well. If you insist. |
| 0x8d646 | 34 | It's a pleasure to meet you, M--\n |
| 0x8d669 | 12 | ...Rulutieh? |
| 0x8d676 | 4 | Yes! |
| 0x8d67b | 24 | Rulutieh smiles happily. |
| 0x8d694 | 48 | I'm pleased to make your acquaintance as well,\n |
| 0x8d6c5 | 12 | Miss Nekone. |
| 0x8d6d7 | 45 | Oh... I am Nekone. I enjoy sweet foods over\n |
| 0x8d705 | 12 | most others. |
| 0x8d712 | 42 | My hobby is researching the lives of the\n |
| 0x8d73d | 9 | ancients. |
| 0x8d747 | 13 | The ancients? |
| 0x8d755 | 46 | At Kuon's reaction, Nekone shrinks as though\n |
| 0x8d784 | 35 | she'd said something inappropriate. |
| 0x8d7a8 | 17 | N-No, never mind. |
| 0x8d7ba | 16 | You too, Nekone? |
| 0x8d7cb | 36 | I'm fascinated by the ancients, too. |
| 0x8d7f0 | 49 | Especially the Onvitaikayan--the Great Fathers.\n |
| 0x8d822 | 31 | It's all so exciting, isn't it? |
| 0x8d842 | 46 | I've been travelling all over the world so I\n |
| 0x8d871 | 29 | can see the historical ruins. |
| 0x8d88f | 21 | Nekone's ears twitch. |
| 0x8d8a5 | 15 | I-Is that true? |
| 0x8d8b5 | 46 | Of course. I've delved into more than a few,\n |
| 0x8d8e4 | 4 | now. |
| 0x8d8e9 | 44 | Nekone looks up at Kuon with sparkling eyes. |
| 0x8d916 | 30 | Do stories like this bore you? |
| 0x8d935 | 17 | N-No, not at all. |
| 0x8d947 | 45 | I can tell you all about it in more detail,\n |
| 0x8d975 | 20 | then, if you'd like? |
| 0x8d98a | 12 | Yes, please! |
| 0x8d997 | 43 | Kuon, Nekone, and Rulutieh quickly huddle\n |
| 0x8d9c3 | 48 | together, diving into an academic conversation\n |
| 0x8d9f4 | 12 | about ruins. |
| 0x8da01 | 44 | Every other word is unrecognizable jargon.\n |
| 0x8da2e | 14 | I'm at a loss. |
| 0x8da3d | 47 | ...Not exactly usual "girl talk" fare, but as\n |
| 0x8da6d | 36 | long as they're enjoying themselves. |
| 0x8da92 | 45 | Looks like she's completely forgotten about\n |
| 0x8dac0 | 20 | thanking me, though. |
| 0x8dad5 | 50 | Ah, so rare a sight 'tis, to see Mistress Nekone\n |
| 0x8db08 | 32 | delighting in conversation thus. |
| 0x8db29 | 45 | Maroro mutters next to me in fond wonderment. |
| 0x8db57 | 46 | Hers is a vast intellect, bestow'd with love\n |
| 0x8db86 | 43 | by the Great Fathers as befits one titled\n |
| 0x8dbb2 | 11 | Kunneietai. |
| 0x8dbbe | 49 | The vaunted imperial examination was as nothing\n |
| 0x8dbf0 | 46 | before her gifts. A scholar of philosophy so\n |
| 0x8dc1f | 8 | young... |
| 0x8dc28 | 46 | Imperial examination? You mean the test Kuon\n |
| 0x8dc57 | 18 | was talking about? |
| 0x8dc6a | 39 | Is it that difficult? The exam, I mean. |
| 0x8dc92 | 48 | Beyond compare. But one or two applicants in a\n |
| 0x8dcc3 | 43 | decade who seek the challenge conquer its\n |
| 0x8dcef | 9 | travails. |
| 0x8dcf9 | 48 | Mistress Nekone doth hold the honor of besting\n |
| 0x8dd2a | 42 | the beast at more tender an age than any\n |
| 0x8dd55 | 11 | before her. |
| 0x8dd61 | 16 | Huh. Impressive. |
| 0x8dd72 | 46 | Wait, come to think of it--you took the same\n |
| 0x8dda1 | 17 | test, didn't you? |
| 0x8ddb3 | 49 | But of course! Arduous was my journey, i'faith,\n |
| 0x8dde5 | 44 | but fate conspired to see me a scholar true. |
| 0x8de12 | 36 | Maroro proudly sticks out his chest. |
| 0x8de37 | 48 | ...Is it really that big a deal if HE passed it? |
| 0x8de68 | 42 | ...Alas, Maroro is an underscholar only.\n |
| 0x8de93 | 41 | Meek and wither'd are my laurels before\n |
| 0x8debd | 18 | Mistress Nekone's. |
| 0x8ded0 | 43 | So there are different kinds of scholars,\n |
| 0x8defc | 7 | then... |
| 0x8df04 | 46 | Forsooth, would such things transpire 'neath\n |
| 0x8df33 | 24 | ordinary circumstance... |
| 0x8df4c | 22 | Ordinary circumstance? |
| 0x8df63 | 49 | Bah, pay it no mind, prithee. Be not mistaken--\n |
| 0x8df95 | 46 | Mistress Nekone's is a mind bestow'd a spark\n |
| 0x8dfc4 | 10 | of genius. |
| 0x8dfcf | 6 | But... |
| 0x8dfd6 | 48 | Alas, 'tis both gift and curse. Her peers shun\n |
| 0x8e007 | 46 | her, aberrant as they perceive her mind to be. |
| 0x8e036 | 41 | Ah, yeah, I've heard of that. The whole\n |
| 0x8e060 | 28 | "geniuses are lonely" thing. |
| 0x8e07d | 48 | None were able to comprehend the lofty matters\n |
| 0x8e0ae | 47 | of which she spoke, so beyond their level was\n |
| 0x8e0de | 6 | she... |
| 0x8e0e5 | 46 | Forsooth, it feels an age and longer since I\n |
| 0x8e114 | 47 | have seen so childlike a smile upon her visage. |
| 0x8e144 | 43 | Hearing that, it strikes me that Nekone's\n |
| 0x8e170 | 41 | expression is one of girlish innocence... |
| 0x8e19a | 46 | ...more befitting a child playing with dolls\n |
| 0x8e1c9 | 43 | or picking flowers than an erudite scholar. |
| 0x8e1f5 | 45 | That's really incredible, being an imperial\n |
| 0x8e223 | 23 | student at your age...! |
| 0x8e23b | 44 | There is little point if I cannot have the\n |
| 0x8e268 | 43 | proper title of scholar. I matter nothing\n |
| 0x8e294 | 11 | without it. |
| 0x8e2a0 | 44 | It's actually amazing. She's being way too\n |
| 0x8e2cd | 23 | self-deprecating, here. |
| 0x8e2e5 | 24 | She was too young, alas. |
| 0x8e2fe | 47 | 'Neath ordinary circumstance, hers would have\n |
| 0x8e32e | 44 | been the proper mantle. She was deemed too\n |
| 0x8e35b | 20 | young to receive it. |
| 0x8e370 | 48 | In any case, it's clear she's an extraordinary\n |
| 0x8e3a1 | 42 | kid, based on everyone's reactions to her. |
| 0x8e3cc | 45 | I don't think you're giving yourself enough\n |
| 0x8e3fa | 7 | credit. |
| 0x8e402 | 47 | When I was your age, all I did was run around\n |
| 0x8e432 | 30 | and play in the hills all day. |
| 0x8e451 | 33 | But you're an imperial scholar!\n |
| 0x8e473 | 30 | You should take pride in that. |
| 0x8e492 | 22 | Yes, I think so too... |
| 0x8e4a9 | 40 | You are a very hard worker, Miss Nekone. |
| 0x8e4d2 | 46 | Being so openly praised seems to make Nekone\n |
| 0x8e501 | 39 | shy, for she falls silent at Kuon and\n |
| 0x8e529 | 17 | Rulutieh's words. |
| 0x8e53b | 48 | Eh heh, and you're cute, to boot. I wish I had\n |
| 0x8e56c | 31 | a little sister as cute as you. |
| 0x8e58c | 6 | Urk... |
| 0x8e593 | 7 | Nekone. |
| 0x8e59b | 47 | Ukon gently strokes Nekone's head, sitting in\n |
| 0x8e5cb | 47 | silence with her. I can sense the strength of\n |
| 0x8e5fb | 11 | their bond. |
| 0x8e607 | 15 | Dear brother... |
| 0x8e617 | 46 | Nekone leans back on Ukon's lap comfortably,\n |
| 0x8e646 | 30 | wearing a peaceful expression. |
| 0x8e665 | 22 | I really am jealous... |
| 0x8e67c | 45 | Yes... it... makes me miss my own brothers... |
| 0x8e6aa | 47 | How wonderful it is for everyone to get along\n |
| 0x8e6da | 36 | like this. All in a day's work, yep. |
| 0x8e6ff | 40 | ...Why do you look so proud of yourself? |
| 0x8e728 | 7 | ...Huh? |
| 0x8e730 | 48 | Dear brother, are you picking up strays again?\n |
| 0x8e761 | 47 | You really should leave things where you find\n |
| 0x8e791 | 5 | them. |
| 0x8e797 | 45 | Nekone stares at me coldly as she addresses\n |
| 0x8e7c5 | 46 | I can feel her gaze pass through me, talking\n |
| 0x8e7f4 | 29 | about me like I barely exist. |
| 0x8e812 | 42 | Bahahaha! Don't be so hard on him, Nekone. |
| 0x8e83d | 46 | He may seem bland on the surface, but Haku's\n |
| 0x8e86c | 46 | proven himself to be a pretty interesting guy. |
| 0x8e89b | 42 | Besides, I owe him a favor for helping me. |
| 0x8e8c6 | 45 | If he hadn't come along, I'd have gotten in\n |
| 0x8e8f4 | 28 | real trouble this time, see? |
| 0x8e911 | 47 | He's right. If not for Haku's quick thinking,\n |
| 0x8e941 | 31 | we might not have made it here. |
| 0x8e961 | 14 | Is that so...? |
| 0x8e970 | 46 | That's about the shape of it. Pour the kid a\n |
| 0x8e99f | 45 | drink. We're exchanging cups to signify our\n |
| 0x8e9cd | 11 | friendship. |
| 0x8e9d9 | 22 | At that, Nekone sighs. |
| 0x8e9f0 | 49 | If you say so, dear brother... I suppose thanks\n |
| 0x8ea22 | 40 | should be offered for services rendered. |
| 0x8ea4b | 42 | Nekone sits on her knees and retrieves a\n |
| 0x8ea76 | 14 | nearby bottle. |
| 0x8ea85 | 41 | Haku, was it? Allow me to pour you a cup. |
| 0x8eaaf | 33 | If you're offering, by all means. |
| 0x8ead1 | 28 | I hold out my cup to Nekone. |
| 0x8eaee | 14 | Right, then... |
| 0x8eafd | 45 | Nekone tips the bottle's neck into the cup,\n |
| 0x8eb2b | 43 | her grip a touch awkward. She must not do\n |
| 0x8eb57 | 10 | this much. |
| 0x8eb62 | 13 | Here you are. |
| 0x8eb70 | 18 | Whoa, easy, easy-- |
| 0x8eb83 | 50 | When I bring the cup back to my lap, it sloshes,\n |
| 0x8ebb6 | 47 | overfull. I take a quick drink to contain the\n |
| 0x8ebe6 | 6 | spill. |
| 0x8ebed | 45 | Oh, that's good. Sake poured by a cute girl\n |
| 0x8ec1b | 21 | always tastes better. |
| 0x8ec31 | 45 | Still, I can't believe you're Ukon's little\n |
| 0x8ec5f | 9 | sister... |
| 0x8ec69 | 38 | You're way too cute to be related to\n |
| 0x8ec90 | 45 | rough-and-tumble Ukon. Are you sure you two\n |
| 0x8ecbe | 11 | are family? |
| 0x8ecca | 50 | Ha, of course we're family! Nekone's my beloved,\n |
| 0x8ecfd | 44 | brilliant little sis. Cute as a button, too. |
| 0x8ed2a | 11 | Wh-What...? |
| 0x8ed36 | 47 | Really, her only flaw's that she can be a bit\n |
| 0x8ed66 | 15 | cold sometimes. |
| 0x8ed76 | 49 | Come on. That's what they call charm, isn't it?\n |
| 0x8eda8 | 44 | A perfect person is boring. Flaws make you\n |
| 0x8edd5 | 8 | likable. |
| 0x8edde | 47 | Nekone's face heats up from red to crimson in\n |
| 0x8ee0e | 16 | a split instant. |
| 0x8ee1f | 24 | Wh-What are you saying!? |
| 0x8ee38 | 45 | Besides, you're still little. You shouldn't\n |
| 0x8ee66 | 44 | stress over not outgrowing your bedwetting\n |
| 0x8ee93 | 6 | habit. |
| 0x8ee9a | 47 | Better to be a genius who wets the bed than a\n |
| 0x8eeca | 41 | smart, prim, perfect girl. It makes you\n |
| 0x8eef4 | 10 | endearing. |
| 0x8eeff | 47 | He's got a point. You're cute as you are, but\n |
| 0x8ef2f | 45 | it'd be all right if you became even cuter,\n |
| 0x8ef5d | 7 | y'know? |
| 0x8ef65 | 12 | Bwahahahaha! |
| 0x8ef72 | 5 | Hurk? |
| 0x8ef78 | 48 | Before I can react, Nekone's hands wrap around\n |
| 0x8efa9 | 40 | my throat. Darkness envelops me almost\n |
| 0x8efd2 | 12 | immediately. |
| 0x8efdf | 16 | Eh? Kid, you OK? |
| 0x8eff0 | 45 | Dearest brother, I believe your friend Haku\n |
| 0x8f01e | 43 | has passed out from partaking in too much\n |
| 0x8f04a | 8 | alcohol. |
| 0x8f053 | 43 | What a shame. He might catch a cold if he\n |
| 0x8f07f | 12 | sleeps here. |
| 0x8f08c | 39 | Ah, well. Throw a blanket over him or\n |
| 0x8f0b4 | 20 | something, will you? |
| 0x8f0c9 | 12 | As you wish. |
| 0x8f0d6 | 45 | Truly, I never thought that technique would\n |
| 0x8f104 | 15 | work so well... |
| 0x8f114 | 47 | How weak must he be, for so simple a maneuver\n |
| 0x8f144 | 22 | to be so effective...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_14_04.json` com a forma:
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
