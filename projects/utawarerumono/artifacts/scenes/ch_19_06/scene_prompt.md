# Cena ch_19_06 — pacote de traducao (318 linhas)

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
| aperyu | Item | aperyu | manter_original | none |
| Atuy | Personagem | Atuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Magecraft | Conceito | Magia | traduzir | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shyahoro | Local | Shyahoro | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |

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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `beside me.` -> `ao meu lado.` (Haku, 18_01)
- `that?` -> `né?` (Haku, 14_09)
- `No.` -> `Não.` (Protagonista (narração), 18_01)
- `but--` -> `mas--` (Oshtor, 19_05)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Uruuru.` -> `Uruuru.` (Garota, 19_05)
- `My name is Saraana.` -> `Meu nome é Saraana.` (Garota, 19_05)
- `reason.` -> `alguma razão.` (Haku, 14_09)
- `into my heart.` -> `algum.` (Haku, 13_05)
- `Ah...?` -> `Ah...?` (Nekone, 14_09)
- `unlikely.` -> `improvável.` (Haku, 17_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `I think.` -> `acho.` (Kuon, 12_11)
- `side.` -> `de lado.` (Haku, 13_02)
- `tea.` -> `chá.` (Haku, 17_01)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Wh-What are you...?` -> `O-O que você está...?` (Rulutieh, 19_04)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `like that?` -> `assim?` (Haku, 15_01)
- `while.` -> `agora.` (Kuon, 15_02)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `What're you talking about?` -> `Como assim?` (Ukon, 13_05)
- `Hnngh...` -> `Hnngh...` (Kuon, 17_04)
- `well.` -> `bem.` (Kuon, 16_01)
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
| 0x183bf7 | 48 | As we make our way back to the Hakurokaku Inn,\n |
| 0x183c28 | 35 | I feel the eyes of passersby on me. |
| 0x183c4c | 43 | I guess it's only natural. I've got Kuon,\n |
| 0x183c78 | 41 | Rulutieh, Atuy, Nekone, and those twins\n |
| 0x183ca2 | 10 | beside me. |
| 0x183cad | 47 | Personalities aside, they're all pretty good-\n |
| 0x183cdd | 48 | looking, and I'm the only guy accompanying all\n |
| 0x183d0e | 8 | of them. |
| 0x183d17 | 47 | Yeah, no wonder. If I saw a guy cruising down\n |
| 0x183d47 | 43 | the street like this, I'd be jealous too... |
| 0x183d77 | 31 | ...How did it end up like this? |
| 0x183d97 | 49 | ...Yeah, I should probably try to accept reality. |
| 0x183dc9 | 50 | The judgemental strangers are one thing, but the\n |
| 0x183dfc | 47 | stares from Kuon and the others hurt even more. |
| 0x183e2c | 50 | I explained the situation, so it's clear I'm not\n |
| 0x183e5f | 47 | at fault here... So why are they glaring like\n |
| 0x183e8f | 5 | that? |
| 0x183e95 | 31 | They do understand, right...?\n |
| 0x183eb5 | 7 | Right!? |
| 0x183ebd | 48 | Maybe it's the chains I've got attached to the\n |
| 0x183eee | 19 | twins like a leash? |
| 0x183f02 | 45 | But I clearly didn't have a choice in that,\n |
| 0x183f30 | 46 | either. I tried to explain it again and again! |
| 0x183f5f | 47 | Um, hey. So... how about we take those chains\n |
| 0x183f8f | 8 | off now? |
| 0x183f98 | 3 | No. |
| 0x183f9c | 13 | No. We can't. |
| 0x183faa | 20 | Until we reach home. |
| 0x183fbf | 47 | We shall keep these on until we reach our home. |
| 0x183fef | 9 | A ritual. |
| 0x183ff9 | 50 | This is a very special ritual in which we become\n |
| 0x18402c | 25 | your possessions, Master. |
| 0x184046 | 18 | A precious memory. |
| 0x184059 | 43 | We wish to etch this moment in our hearts\n |
| 0x184085 | 8 | forever. |
| 0x18408e | 51 | It seems like they're really into this. They keep\n |
| 0x1840c2 | 27 | refusing to take those off. |
| 0x1840de | 47 | If I wanted to, I could make them--I mean, if\n |
| 0x18410e | 49 | I'm assertive about it, they'd probably listen,\n |
| 0x184140 | 5 | but-- |
| 0x184146 | 9 | An order? |
| 0x184150 | 45 | If it is an order, Master, we shall oblige.\n |
| 0x18417e | 25 | We belong to you, Master. |
| 0x184198 | 15 | We shall serve. |
| 0x1841a8 | 46 | Our purpose for existing is your satisfaction. |
| 0x1841d7 | 20 | Orders are absolute. |
| 0x1841ec | 49 | Following your orders brings us nothing but the\n |
| 0x18421e | 24 | greatest of joy, Master. |
| 0x184237 | 7 | Urgh... |
| 0x18423f | 32 | They're... serious. Aren't they. |
| 0x184260 | 37 | OK, what the hell am I going to do?\n |
| 0x184286 | 46 | I highly doubt the nation's ruler would give\n |
| 0x1842b5 | 21 | them to me as a joke. |
| 0x1842cb | 40 | Orders of a sexual nature are permitted. |
| 0x1842f4 | 49 | Orders of a sexual nature are highly recommended. |
| 0x184326 | 7 | Bfwah!? |
| 0x18432e | 37 | Wh-What the hell are they saying...!? |
| 0x184354 | 48 | Kuon's eyes narrow to slits, and Nekone levels\n |
| 0x184385 | 39 | a cold gaze at me, like I'm utter scum. |
| 0x1843ad | 46 | Would those two just stop!? Everyone looking\n |
| 0x1843dc | 31 | is getting the wrong idea here. |
| 0x1843fc | 44 | What is he planning on doing to those poor\n |
| 0x184429 | 9 | girls...? |
| 0x184433 | 45 | Shouldn't we call the guards or something...? |
| 0x184461 | 39 | I can hear people whispering behind me. |
| 0x184489 | 32 | Not giving any orders like that! |
| 0x1844aa | 46 | Sir Haku... so filthy... filthy... filthy...\n |
| 0x1844d9 | 19 | filthy... filthy... |
| 0x1844ed | 43 | I don't know why, but Rulutieh's mumbling\n |
| 0x184519 | 40 | quietly to herself with a blank stare.\n |
| 0x184542 | 21 | It's freaking me out. |
| 0x184558 | 42 | Why is this happening...? I have so many\n |
| 0x184583 | 46 | beautiful girls with me, but I still feel so\n |
| 0x1845b2 | 12 | miserable... |
| 0x1845bf | 45 | The moment we get back to the Hakurokaku, I\n |
| 0x1845ed | 39 | quickly get those chains off the twins. |
| 0x184615 | 41 | The two of them look at me with longing\n |
| 0x18463f | 41 | expressions, but I choose to ignore them. |
| 0x184669 | 44 | Well, anyway. Welcome to the Hakurokaku Inn. |
| 0x184696 | 50 | My name's Kuon, and this is Nekone and Rulutieh.\n |
| 0x1846c9 | 32 | And the girl over there is Atuy. |
| 0x1846ea | 7 | Uruuru. |
| 0x1846f2 | 19 | My name is Saraana. |
| 0x184706 | 49 | I am Nekone. I am deeply sorry for your plight.\n |
| 0x184738 | 46 | I shall do everything in my power to help...\n |
| 0x184767 | 19 | Please, take heart. |
| 0x18477b | 47 | With pity in her voice, she turns her gaze on\n |
| 0x1847ab | 48 | me... a gaze like I'm some dung on the side of\n |
| 0x1847dc | 7 | a road. |
| 0x1847e4 | 43 | I'm Rulutieh. It'll be a pleasure to work\n |
| 0x184810 | 9 | with you. |
| 0x18481a | 49 | Rulutieh's looking abnormally cheerful for some\n |
| 0x18484c | 7 | reason. |
| 0x184854 | 21 | Um... uh... Rulutieh? |
| 0x18486a | 16 | Yes, what is it? |
| 0x18487b | 47 | I don't know why, but that smile strikes fear\n |
| 0x1848ab | 14 | into my heart. |
| 0x1848ba | 42 | Something's wrong here. I don't remember\n |
| 0x1848e5 | 33 | Rulutieh acting like this before. |
| 0x184907 | 33 | She's usually a bit reserved...\n |
| 0x184929 | 46 | I guess a little bashful and hesitant, really. |
| 0x184958 | 46 | Well, aren't you two just the cutest things!\n |
| 0x184987 | 27 | I'm Atuy--nice to meet you. |
| 0x1849a3 | 32 | ...The mad princess of Shyahoro. |
| 0x1849c4 | 49 | We have heard many tales of you. Your beauty is\n |
| 0x1849f6 | 44 | compared to that of flower petals, stained\n |
| 0x184a23 | 10 | vivid red. |
| 0x184a2e | 44 | Hee hee... Oh, stop! You're making me blush. |
| 0x184a5b | 40 | I'm not sure that's how they meant it... |
| 0x184a84 | 46 | Now then, I believe we deserve an explanation. |
| 0x184ab3 | 21 | Mhm, mhm... *sniffle* |
| 0x184ac9 | 48 | Didn't I just explain everything to you already? |
| 0x184afa | 46 | ...Well, I'd LIKE to ask more, but I suppose\n |
| 0x184b29 | 35 | I'll just leave it at that for now. |
| 0x184b4d | 6 | Ah...? |
| 0x184b54 | 50 | Didn't expect that. Kuon's usually curious about\n |
| 0x184b87 | 38 | everything. I figured I'd get a full\n |
| 0x184bae | 14 | interrogation. |
| 0x184bbd | 47 | Sometimes there are things that you're better\n |
| 0x184bed | 16 | off not knowing. |
| 0x184bfe | 12 | Not knowing? |
| 0x184c0b | 49 | ...Are you telling me you didn't even realize it? |
| 0x184c3d | 22 | Realize what, exactly? |
| 0x184c54 | 32 | Oh... So you really didn't know. |
| 0x184c75 | 36 | OK, what are you even talking about? |
| 0x184c9a | 30 | What do you mean, dear sister? |
| 0x184cb9 | 42 | Nekone, you didn't realize it either...?\n |
| 0x184ce4 | 48 | There are so many odd factors in this situation. |
| 0x184d15 | 47 | Normally, a mere commoner would never receive\n |
| 0x184d45 | 42 | direct praise and a reward from the holy\n |
| 0x184d70 | 9 | Mikado... |
| 0x184d7a | 50 | He did save the princess, but surely he realizes\n |
| 0x184dad | 37 | that the whole thing was just a sham. |
| 0x184dd3 | 33 | Yes... Now that you mention it... |
| 0x184df5 | 43 | And from what I hear, these two are quite\n |
| 0x184e21 | 33 | special, even among the kamunagi. |
| 0x184e43 | 47 | Why would the Mikado just give them away as a\n |
| 0x184e73 | 43 | reward, however praiseworthy one's actions? |
| 0x184e9f | 47 | ...Unless there's some kind of deeper meaning\n |
| 0x184ecf | 10 | behind it. |
| 0x184eda | 36 | Well, that's... But is that even...? |
| 0x184eff | 50 | I don't really get what she's implying, but I do\n |
| 0x184f32 | 42 | agree that this whole thing seems pretty\n |
| 0x184f5d | 9 | unlikely. |
| 0x184f67 | 35 | So what are you trying to say here? |
| 0x184f8b | 26 | Oh, nothing in particular. |
| 0x184fa6 | 4 | Huh? |
| 0x184fab | 48 | Like I said, some things you're better off not\n |
| 0x184fdc | 8 | knowing. |
| 0x184fe5 | 50 | "Child of man, love thy knowledge. But mind that\n |
| 0x185018 | 48 | thy curiosity bring not ruin to thee and thine." |
| 0x185049 | 50 | Famous quotes usually have good advice to offer,\n |
| 0x18507c | 8 | I think. |
| 0x185085 | 49 | I don't know what you got roped into this time,\n |
| 0x1850b7 | 46 | Haku... But I'll be cheering you on from the\n |
| 0x1850e6 | 5 | side. |
| 0x1850ec | 42 | Don't say vague ominous stuff like that!\n |
| 0x185117 | 25 | She might be right, but-- |
| 0x185131 | 42 | Hey, you two know anything about all this? |
| 0x185161 | 48 | But the two just look at me, their expressions\n |
| 0x185192 | 17 | meek and puzzled. |
| 0x1851a4 | 48 | How did this happen? Ugh, I've been yelling so\n |
| 0x1851d5 | 28 | much, I'm all thirsty now... |
| 0x1851f2 | 4 | Tea. |
| 0x1851f7 | 42 | We shall prepare you a cup of tea, Master. |
| 0x185222 | 49 | And the two begin to prepare the tea, as though\n |
| 0x185254 | 22 | they had read my mind. |
| 0x18526b | 45 | Oh, uh, thanks. You guys good with all this\n |
| 0x185299 | 22 | housework kinda stuff? |
| 0x1852b0 | 17 | A servant's duty. |
| 0x1852c2 | 40 | We attained proficiency in all things.\n |
| 0x1852eb | 46 | A servant must be able to fulfill a Master's\n |
| 0x18531a | 7 | wishes. |
| 0x185322 | 21 | We will cook as well. |
| 0x185338 | 46 | From now on, you may leave the Master's food\n |
| 0x185367 | 18 | preparation to us. |
| 0x18537a | 7 | Huh...? |
| 0x185382 | 17 | Also the bedroom. |
| 0x185394 | 38 | We have mastered all 108 techniques.\n |
| 0x1853bb | 31 | We shall accompany you in bed-- |
| 0x1853db | 23 | N-No, I won't allow it! |
| 0x1853f3 | 22 | Th-That is my role...! |
| 0x18540a | 7 | In bed? |
| 0x185412 | 47 | So the role of accompanying Master to bed has\n |
| 0x185442 | 21 | been yours until now? |
| 0x185458 | 9 | ...H-Huh? |
| 0x185462 | 23 | I-In bed...? U-Um...?\n |
| 0x18547a | 19 | Wh-What are you...? |
| 0x18548e | 23 | We require information. |
| 0x1854a6 | 48 | We would like you to describe Master's habits.\n |
| 0x1854d7 | 47 | His sexual likes and dislikes. In vivid detail. |
| 0x185507 | 43 | Th-Th-That wasn't what I was talking about! |
| 0x185533 | 21 | We require reference. |
| 0x185549 | 47 | The average number of times Master is able to\n |
| 0x185579 | 43 | perform on a nightly basis. Also, favored\n |
| 0x1855a5 | 10 | positions. |
| 0x1855b0 | 42 | I wasn't talking about things like that!\n |
| 0x1855db | 38 | What do you intend on doing with him!? |
| 0x185602 | 47 | Rulutieh's bright red, and yelling at the top\n |
| 0x185632 | 43 | of her lungs. You don't see that every day. |
| 0x18565e | 48 | Maybe you should pay more attention to reality\n |
| 0x18568f | 35 | and try to do something about this? |
| 0x1856b3 | 49 | I'm hearing so many things I don't think a girl\n |
| 0x1856e5 | 46 | should be saying. What am I supposed to do...? |
| 0x185714 | 48 | Well, aren't you the luckiest fellow? You have\n |
| 0x185745 | 47 | so many cute girls that care so much about you. |
| 0x185775 | 46 | Yeah, when they're this aggressive about it,\n |
| 0x1857a4 | 31 | I'm not sure I feel that lucky. |
| 0x1857c4 | 16 | For you, Master. |
| 0x1857d5 | 45 | The two of them skillfully prepare the tea,\n |
| 0x185803 | 44 | working in total sync to multitask through\n |
| 0x185830 | 11 | everything. |
| 0x18583c | 23 | Let's try it... *Slurp* |
| 0x185854 | 46 | ...Hey, that's really good. The temperature,\n |
| 0x185883 | 31 | the flavor--it's all top notch. |
| 0x1858a3 | 35 | Definitely wasn't expecting this.\n |
| 0x1858c7 | 47 | After all that crazy talk, I didn't know what\n |
| 0x1858f7 | 20 | to expect from them. |
| 0x18590c | 45 | It may just be tea, but good tea takes some\n |
| 0x18593a | 11 | real skill. |
| 0x185946 | 43 | Who knew you could prepare tea as good as\n |
| 0x185972 | 13 | Rulutieh can? |
| 0x185980 | 28 | It is our pleasure to serve. |
| 0x18599d | 50 | They bow without changing expressions, and kneel\n |
| 0x1859d0 | 41 | next to me, as if it's where they belong. |
| 0x1859fa | 48 | Their bodies lean against mine, and I can feel\n |
| 0x185a2b | 19 | their warm touch... |
| 0x185a3f | 8 | Wh-What? |
| 0x185a48 | 43 | Now that I think about it, these two were\n |
| 0x185a74 | 37 | clinging to me like this before, too. |
| 0x185a9a | 50 | At the time though, I didn't really mind because\n |
| 0x185acd | 38 | they were all covered by that aperyu-- |
| 0x185af4 | 44 | OK, no, it was still weird. I just stopped\n |
| 0x185b21 | 41 | thinking about it too much after a while. |
| 0x185b4b | 7 | Ohhh... |
| 0x185b53 | 50 | By the way, Rulutieh, why are you walking around\n |
| 0x185b86 | 10 | like that? |
| 0x185b91 | 25 | Huh? I... um... that's... |
| 0x185bab | 49 | Rulutieh's been walking back and forth in front\n |
| 0x185bdd | 44 | of me, shooting me glances every once in a\n |
| 0x185c0a | 6 | while. |
| 0x185c11 | 7 | *Shuff* |
| 0x185c19 | 3 | Hm? |
| 0x185c1d | 49 | I feel a sudden weight on my back, and I end up\n |
| 0x185c4f | 24 | spilling my tea mid-sip. |
| 0x185c68 | 49 | I peer behind me to see Kuon leaning on my back\n |
| 0x185c9a | 16 | with her elbows. |
| 0x185cab | 5 | Oh... |
| 0x185cb1 | 49 | Haku, that grin on your face is making you look\n |
| 0x185ce3 | 12 | like a fool. |
| 0x185cf0 | 28 | What're you talking about?\n |
| 0x185d0d | 19 | I'm not grinning... |
| 0x185d21 | 29 | I touch my face to make sure. |
| 0x185d3f | 16 | I'm not... am I? |
| 0x185d50 | 36 | Then Kuon gives a mischievous smile. |
| 0x185d75 | 48 | The fact that you checked means you do realize\n |
| 0x185da6 | 9 | it, then? |
| 0x185db0 | 50 | Urgh... Get off, you're heavy. Look, you made me\n |
| 0x185de3 | 13 | spill my tea. |
| 0x185df1 | 21 | Dammit, my clothes... |
| 0x185e07 | 47 | U-Um, Sir Haku, please, use this to wipe your\n |
| 0x185e37 | 10 | face off-- |
| 0x185e42 | 38 | Ahaha, sorry about that. Hold still.\n |
| 0x185e69 | 26 | You've got a tea mustache. |
| 0x185e84 | 47 | Kuon takes out a handkerchief from her pocket\n |
| 0x185eb4 | 38 | and wipes at my face like a fussy mom. |
| 0x185edb | 8 | Hnngh... |
| 0x185ee4 | 28 | Oh! Sir Haku, your clothes-- |
| 0x185f01 | 15 | Covered in tea. |
| 0x185f11 | 26 | Allow us to clean you off. |
| 0x185f2c | 16 | *Wipe* *wipe*... |
| 0x185f3d | 39 | Uh, thanks... but I think I'm fine now. |
| 0x185f65 | 46 | The twins begin to reach into my clothing as\n |
| 0x185f94 | 5 | well. |
| 0x185f9a | 45 | Wh--H-Hey, where do you think you're wiping!? |
| 0x185fc8 | 8 | Seepage. |
| 0x185fd1 | 47 | It seems the tea has spilt in your lap as well. |
| 0x186001 | 44 | Hey, uh, no need to reach around in there... |
| 0x18602e | 20 | *Rustle* *rustle*... |
| 0x186043 | 39 | C-Careful with all that, uh, touching-- |
| 0x18606b | 29 | Gah, now wait a damn minute-- |
| 0x186089 | 10 | Excuse me! |
| 0x186094 | 31 | Uh, wh-what's the matter now?\n |
| 0x1860b4 | 20 | Why are you yelling? |
| 0x1860c9 | 16 | Your overcoat... |
| 0x1860da | 50 | It's going to stain if you leave it like that...\n |
| 0x18610d | 40 | so... if you could please take it off... |
| 0x186136 | 14 | Not a problem. |
| 0x186145 | 45 | Like the mighty gale, sweeping the cloak of\n |
| 0x186173 | 37 | clouds from the heavens' shoulders... |
| 0x186199 | 49 | The twins murmur something quiet together, then\n |
| 0x1861cb | 47 | set their hands over the stain on the overcoat. |
| 0x1861fb | 49 | A flame flickers for an instant over the cloth,\n |
| 0x18622d | 34 | and in seconds, the stain is gone. |
| 0x186250 | 10 | ...Wha...? |
| 0x18625b | 26 | What was that just now...? |
| 0x186276 | 41 | High Magecraft... a secret art known by\n |
| 0x1862a0 | 52 | Yamatan kamunagi, greater than ordinary magecraft.\n |
| 0x1862d5 | 47 | I imagined it would be more like thaumaturgy... |
| 0x186305 | 23 | Magecraft? Thaumaturgy? |
| 0x18631d | 45 | Magecraft is based on innate power, through\n |
| 0x18634b | 45 | training of mind and body. Thaumaturgy uses\n |
| 0x186379 | 38 | natural worldly energy; ambient magic. |
| 0x1863a0 | 20 | H-Huh... I get it... |
| 0x1863b5 | 15 | I don't get it. |
| 0x1863c5 | 47 | Wait, what was the point of wiping me down if\n |
| 0x1863f5 | 47 | you could just use your magecraft to clean me\n |
| 0x186425 | 4 | off? |
| 0x18642a | 46 | Both of them tilt their heads questioningly,\n |
| 0x186459 | 16 | in perfect sync. |
| 0x18646a | 36 | Why are you looking at me like that? |
| 0x18648f | 31 | Hold on, did you realize that-- |
| 0x1864af | 10 | *Pinch*... |
| 0x1864ba | 23 | Owowowowow!? What the-- |
| 0x1864d2 | 15 | Uh... Rulutieh? |
| 0x1864e2 | 31 | Why is Rulutieh pinching me...? |
| 0x186502 | 30 | ...Hmph! I don't care anymore! |
| 0x186521 | 12 | ...Huh? Why? |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_06.json` com a forma:
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
