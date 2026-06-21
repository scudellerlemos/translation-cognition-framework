# Cena ch_14_03 — pacote de traducao (318 linhas)

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
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
| Woman | UI | Mulher | traduzir | none |

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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Huh?` -> `Hein?` (Haku, 11_06)
- `here?` -> `afinal?` (Haku, 13_02)
- `How about it?` -> `Que tal?` (Ukon, 14_02)
- `I'll bet.` -> `aposto.` (Haku, 12_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `...Did you say something?` -> `...Você disse alguma coisa?` (Kuon, root)
- `door.` -> `porta.` (Haku, 11_07)
- `water.` -> `água.` (Haku, 13_03)
- `anyway.` -> `de agora.` (Ougi, 13_08)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Wh--` -> `Q--` (Haku, 11_07)
- `for a moment.` -> `por um instante.` (Kuon, root)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `H-Huh?` -> `H-Hein?` (Rulutieh, 13_01)
- `...\n` -> `...\n` (Haku, 11_08)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `...eep.` -> `...Ai.` (Rulutieh, 14_02)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `Whoa!` -> `Uou!` (Haku, 11_11)
- `Gah!` -> `Ai!` (Man, 13_01)
- `Haku.` -> `Haku.` (Kuon, 12_08)
- `Did you say something?` -> `Disse alguma coisa?` (Haku, 13_09)
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
| 0x831a7 | 49 | We chat idly amongst ourselves as Ukon leads us\n |
| 0x831d9 | 35 | through the streets of the capital. |
| 0x831fd | 46 | We move outward from the center of the city,\n |
| 0x8322c | 43 | eventually coming upon a district full of\n |
| 0x83258 | 9 | greenery. |
| 0x83262 | 50 | Here we are--the Hakurokaku Inn. It's a renowned\n |
| 0x83295 | 34 | establishment here in the capital. |
| 0x832b8 | 49 | Hm. This building has a different architectural\n |
| 0x832ea | 47 | style to it. It's... pretty tasteful, actually. |
| 0x8331a | 47 | It's built spaciously and sumptuously, but it\n |
| 0x8334a | 42 | doesn't feel overly grand or ostentatious. |
| 0x83375 | 41 | The outer facade has a strangely exotic\n |
| 0x8339f | 46 | atmosphere to it, departing from the rest of\n |
| 0x833ce | 17 | the city's style. |
| 0x833e0 | 43 | The unusual architecture's to the owner's\n |
| 0x8340c | 27 | personal taste, apparently. |
| 0x83428 | 50 | Just between us, the proprietress is a drop-dead\n |
| 0x8345b | 46 | gorgeous woman. She's got crazy strength, too. |
| 0x8348a | 23 | Sexy and strong, huh... |
| 0x834a2 | 42 | Hearing that, I glance over my shoulder... |
| 0x834cd | 44 | Kuon seems like she hasn't been listening,\n |
| 0x834fa | 38 | looking around at the exotic building. |
| 0x83521 | 33 | ...Well, she's definitely strong. |
| 0x83543 | 48 | Hey, keep up, you two. Let's not keep everyone\n |
| 0x83574 | 8 | waiting. |
| 0x8357d | 47 | 'Scuse me, miss. There should be a group here\n |
| 0x835ad | 12 | ahead of me? |
| 0x835ba | 6 | Worker |
| 0x835c1 | 41 | Hm? Ah, yes... Your friends are already\n |
| 0x835eb | 40 | gathered in the Wild Chrysanthemum Room. |
| 0x83614 | 15 | Gotcha. Thanks. |
| 0x83624 | 42 | The worker bustles off before Ukon has a\n |
| 0x8364f | 20 | chance to thank her. |
| 0x83664 | 32 | ...Huh. Someone's busy, I guess. |
| 0x83685 | 50 | So they started off on their own without waiting\n |
| 0x836b8 | 40 | for the guests of honor to show up, huh? |
| 0x836e1 | 47 | Sorry about that. I feel bad, since I invited\n |
| 0x83711 | 12 | you and all. |
| 0x8371e | 44 | Eh, it's fine. I'd feel just as bad making\n |
| 0x8374b | 40 | them wait. As long as they're enjoying\n |
| 0x83774 | 11 | themselves. |
| 0x83780 | 44 | You seemed pretty familiar with the people\n |
| 0x837ad | 42 | here. Are you a regular here or something? |
| 0x837d8 | 47 | Huh? Yeah, I guess you could say that. It's a\n |
| 0x83808 | 47 | little upscale, but the food and the booze is\n |
| 0x83838 | 5 | good. |
| 0x8383e | 49 | I guess you could say they hit the mark for me?\n |
| 0x83870 | 31 | The ambience isn't bad, either. |
| 0x83890 | 49 | Yes, the atmosphere certainly is nice. It seems\n |
| 0x838c2 | 45 | like they maintain the place with great care. |
| 0x838f0 | 36 | Kuon enters behind us as she speaks. |
| 0x83915 | 48 | They don't just put an effort forth where it's\n |
| 0x83946 | 47 | visible. Every little nook and cranny is clean. |
| 0x83976 | 22 | Heh, you got the idea. |
| 0x8398d | 18 | So! Lady Rulutieh. |
| 0x839a0 | 43 | Any objections? If this inn isn't to your\n |
| 0x839cc | 39 | liking, there's another I can show you. |
| 0x839f4 | 4 | Huh? |
| 0x839f9 | 45 | Rulutieh jumps, having been looking around,\n |
| 0x83a27 | 41 | Ukon's question catching her by surprise. |
| 0x83a51 | 5 | Here? |
| 0x83a57 | 48 | If you don't like it, we've got other options.\n |
| 0x83a88 | 13 | How about it? |
| 0x83a96 | 46 | N-No, it's... it's not that I don't like it... |
| 0x83ac5 | 47 | She doesn't seem displeased. If anything, she\n |
| 0x83af5 | 17 | seems... anxious? |
| 0x83b07 | 30 | This is such a lovely place... |
| 0x83b26 | 48 | Doesn't hold a candle to your family's castle,\n |
| 0x83b57 | 9 | I'll bet. |
| 0x83b61 | 46 | Th-That's not true! I don't... I don't think\n |
| 0x83b90 | 44 | that place can... be considered... lovely... |
| 0x83bbd | 45 | Is this your first time in a place like this? |
| 0x83beb | 13 | Huh? Y-Yes... |
| 0x83bf9 | 41 | I d-don't... leave the castle much, so... |
| 0x83c23 | 9 | ...I see. |
| 0x83c2d | 40 | At Rulutieh's words, Kuon smiles kindly. |
| 0x83c56 | 47 | Which reminds me. You mentioned this place is\n |
| 0x83c86 | 42 | a little upscale, but how upscale exactly? |
| 0x83cb1 | 47 | Hm? Well, it varies by floor, but the cheaper\n |
| 0x83ce1 | 45 | rooms are 'bout fifty, maybe eighty percent\n |
| 0x83d0f | 13 | over average. |
| 0x83d1d | 7 | Urgh... |
| 0x83d25 | 11 | I-I... see. |
| 0x83d31 | 44 | Seems like she was ready to settle on this\n |
| 0x83d5e | 46 | place for Rulutieh's sake, but balked at the\n |
| 0x83d8d | 12 | high cost... |
| 0x83d9a | 25 | ...Did you say something? |
| 0x83db4 | 26 | No, I didn't say anything. |
| 0x83dcf | 42 | Well, there's a reason why this inn's so\n |
| 0x83dfa | 18 | expensive, y'know. |
| 0x83e0d | 49 | Ah... I know. I s'pose we don't have to rush if\n |
| 0x83e3f | 29 | the men have already started. |
| 0x83e5d | 46 | Follow me. I'll show you something nice this\n |
| 0x83e8c | 23 | place has goin' for it. |
| 0x83ea4 | 48 | As Ukon leads the way through a side corridor,\n |
| 0x83ed5 | 29 | Kuon begins sniffing the air. |
| 0x83ef3 | 13 | This scent... |
| 0x83f01 | 21 | No... Could it be...? |
| 0x83f17 | 42 | Kuon quickens her pace, her tail wagging\n |
| 0x83f42 | 41 | sinuously behind her in quick, frenetic\n |
| 0x83f6c | 11 | excitement. |
| 0x83f78 | 47 | Right over here, missy. Go ahead and open the\n |
| 0x83fa8 | 5 | door. |
| 0x83fae | 45 | Kuon, in high spirits, throws the door open\n |
| 0x83fdc | 47 | with great force. Steam billows into the hall\n |
| 0x8400c | 12 | from within. |
| 0x84019 | 45 | Well, I won't lie. This is pretty impressive. |
| 0x84047 | 6 | Wow... |
| 0x8404e | 46 | The chamber is wide and spacious, and a deep\n |
| 0x8407d | 45 | wooden bathtub inside brims with piping-hot\n |
| 0x840ab | 6 | water. |
| 0x840b2 | 44 | Billowing steam and the scent of rich wood\n |
| 0x840df | 42 | wafts outward from the luxurious bathroom. |
| 0x8410a | 31 | It's a nice fragrance. Calming. |
| 0x8412e | 47 | So, what d'you think? Big communal baths like\n |
| 0x8415e | 37 | this are hard to come by in the city. |
| 0x84184 | 13 | Incredible... |
| 0x84192 | 40 | I-I've... never seen anything like it... |
| 0x841bb | 46 | Right? You won't see a bath like this in any\n |
| 0x841ea | 48 | other inn in town. Not with running hot water,\n |
| 0x8421b | 7 | anyway. |
| 0x84223 | 42 | Even the court nobles' manors don't have\n |
| 0x8424e | 15 | tubs this huge. |
| 0x8425e | 46 | I figured our resident bath-crazy apothecary\n |
| 0x8428d | 48 | would appreciate it, even if it meant a higher\n |
| 0x842be | 6 | price. |
| 0x842c5 | 48 | Anyway! If you feel like it, go ahead and wash\n |
| 0x842f6 | 17 | off before we--\n |
| 0x84308 | 21 | ...Are you listening? |
| 0x8431e | 15 | M-Miss Kuon...? |
| 0x8432e | 43 | Kuon stares forward with wide eyes, hands\n |
| 0x8435a | 29 | trembling as she reaches out. |
| 0x84378 | 45 | She looks for all the world like a starving\n |
| 0x843a6 | 48 | wanderer in the desert, finally coming upon an\n |
| 0x843d7 | 6 | oasis. |
| 0x843de | 40 | ...She's REALLY shaking. Is she having\n |
| 0x84407 | 43 | withdrawal symptoms from handling so many\n |
| 0x84433 | 12 | drugs, or... |
| 0x84440 | 14 | H-Hot water... |
| 0x8444f | 47 | She staggers forward to the bath, dipping her\n |
| 0x8447f | 47 | hand into the water and gliding it across its\n |
| 0x844af | 8 | surface. |
| 0x844b8 | 22 | R-Running hot water... |
| 0x844cf | 24 | What? Yeah, it's a bath. |
| 0x844e8 | 26 | Bath... hot... hot bath... |
| 0x84503 | 5 | Kuon? |
| 0x84509 | 48 | Since Kuon's behavior is starting to worry me,\n |
| 0x8453a | 45 | I step forward into the room, trying to see\n |
| 0x84568 | 9 | her face. |
| 0x84572 | 12 | HOT BATHS!!! |
| 0x8457f | 4 | Wh-- |
| 0x84584 | 6 | *FWIP* |
| 0x8458b | 47 | In an eyeblink, Kuon slips out of her clothes\n |
| 0x845bb | 45 | so quickly, they hang behind her in the air\n |
| 0x845e9 | 13 | for a moment. |
| 0x845f7 | 43 | She stands before everyone, how you say--\n |
| 0x84623 | 46 | in her birthday suit. Au naturel. In the buff. |
| 0x84652 | 43 | From my vantage point, I can only see her\n |
| 0x8467e | 37 | backsi--well, the back side of her.\n |
| 0x846a4 | 26 | There's not a stitch left. |
| 0x846bf | 6 | Then-- |
| 0x846c6 | 7 | Woohoo! |
| 0x846ce | 46 | Kuon vaults the side of the tub and leaps in\n |
| 0x846fd | 13 | bottom-first. |
| 0x8470b | 46 | Her whole body breaks through the water, and\n |
| 0x8473a | 43 | the resulting spray soaks everyone in the\n |
| 0x84766 | 12 | splash zone. |
| 0x84773 | 9 | Urghbwa-- |
| 0x8477d | 42 | Ahhh. Ah ha! Ahahaha, hot water, RUNNING\n |
| 0x847a8 | 11 | hot water!! |
| 0x847b4 | 44 | She energetically fills her hands with the\n |
| 0x847e1 | 47 | steaming water, letting it run down her arms,\n |
| 0x84811 | 6 | giddy. |
| 0x84818 | 11 | Ahahahaha!! |
| 0x84824 | 47 | Kuon flops her whole body down into the bath,\n |
| 0x84854 | 38 | rollicking about like a gleeful child. |
| 0x8487b | 47 | I'm stunned into silence. I have no words for\n |
| 0x848ab | 19 | Kuon's sudden romp. |
| 0x848bf | 13 | Wahahahaaaa!! |
| 0x848cd | 45 | Kuon pops her head out of the bath to begin\n |
| 0x848fb | 45 | splashing water at me, grinning broadly and\n |
| 0x84929 | 9 | giggling. |
| 0x84933 | 47 | Next to me, Rulutieh seems just as bewildered\n |
| 0x84963 | 8 | as I am. |
| 0x8496c | 48 | But of course she would be. Calm, erudite Kuon\n |
| 0x8499d | 43 | is flailing naked before us without a care. |
| 0x849c9 | 47 | Just how much does she love baths, that she's\n |
| 0x849f9 | 33 | totally beside herself like this? |
| 0x84a1b | 43 | She seems totally checked out, too. She's\n |
| 0x84a47 | 44 | oblivious to the fact that we're all still\n |
| 0x84a74 | 5 | here. |
| 0x84a7a | 43 | Her chest, her legs, even what's directly\n |
| 0x84aa6 | 45 | between them--everything is just sort of...\n |
| 0x84ad4 | 12 | in the open. |
| 0x84ae1 | 6 | *Sigh* |
| 0x84ae8 | 47 | Under typical circumstances, the sight of her\n |
| 0x84b18 | 38 | nudity would be a pleasant one, but... |
| 0x84b3f | 48 | That she's shamelessly rollicking about like a\n |
| 0x84b70 | 44 | little kid is off-putting, to say the least. |
| 0x84b9d | 37 | Ah! Miss Kuon--Th-They're showing--\n |
| 0x84bc3 | 30 | I mean, I can see your, um--\n |
| 0x84be2 | 35 | Y-Your clothes, Miss Kuon, please-- |
| 0x84c06 | 51 | Rulutieh quickly snaps back to reality, gathering\n |
| 0x84c3a | 38 | up Kuon's clothes and approaching her. |
| 0x84c61 | 50 | Ah ha haaaa! Hmmm? Rulutieh, you can't wear your\n |
| 0x84c94 | 28 | kimono into the bath, silly! |
| 0x84cb1 | 6 | H-Huh? |
| 0x84cb8 | 46 | You have to take your clothes off for a ba~th! |
| 0x84ce7 | 46 | Kuon reaches for the sash binding Rulutieh's\n |
| 0x84d16 | 7 | kimono. |
| 0x84d1e | 5 | ...\n |
| 0x84d24 | 7 | ...Huh? |
| 0x84d2c | 16 | And here we go~! |
| 0x84d3d | 45 | By some ungodly sleight of hand, Rulutieh's\n |
| 0x84d6b | 45 | clothes slip off in an instant, leaving her\n |
| 0x84d99 | 11 | fully bare. |
| 0x84da5 | 41 | She slowly, agonizingly turns her head,\n |
| 0x84dcf | 23 | and her eyes meet mine. |
| 0x84de7 | 7 | ...Eep. |
| 0x84def | 28 | Rulutieh gasps, going stiff. |
| 0x84e0c | 47 | Large tears well up in her eyes, and her face\n |
| 0x84e3c | 14 | turns crimson. |
| 0x84e4b | 15 | D-Don't look... |
| 0x84e5b | 25 | Please... don't l-look... |
| 0x84e75 | 46 | Though she says that, she makes no effort to\n |
| 0x84ea4 | 40 | cover herself, just standing there and\n |
| 0x84ecd | 10 | trembling. |
| 0x84ed8 | 36 | She can't even move, frozen stiff-\n |
| 0x84efd | 21 | still from the shock. |
| 0x84f13 | 33 | Just... cover yourself... please. |
| 0x84f35 | 47 | Somehow, I can't bring myself to look away as\n |
| 0x84f65 | 45 | Rulutieh just stands there, stuck at Kuon's\n |
| 0x84f93 | 6 | mercy. |
| 0x84f9a | 42 | Ahahaaaa... You've got really nice skin,\n |
| 0x84fc5 | 10 | Rulutieh~! |
| 0x84fd0 | 50 | Kuon hugs Rulutieh tightly, almost nuzzling her,\n |
| 0x85003 | 31 | careless of their surroundings. |
| 0x85023 | 15 | Ah... ah... um. |
| 0x85033 | 13 | What's wrong? |
| 0x85041 | 44 | Rulutieh slowly sinks into the bath, still\n |
| 0x8506e | 13 | frozen stiff. |
| 0x8507c | 12 | ...Rulutieh? |
| 0x85089 | 48 | Kuon looks at Rulutieh, now partially obscured\n |
| 0x850ba | 48 | by bathwater, then follows the line of her gaze. |
| 0x850eb | 21 | Her eyes meet mine... |
| 0x85101 | 34 | ...and her enormous smile freezes. |
| 0x85124 | 12 | KYAAAAAAAH!! |
| 0x85131 | 47 | Suddenly finding her modesty, Kuon covers her\n |
| 0x85161 | 42 | chest with her arms, diving for cover as\n |
| 0x8518c | 13 | Rulutieh had. |
| 0x8519a | 47 | Kuon raises her eyes above the surface of the\n |
| 0x851ca | 29 | water, glaring daggers at me. |
| 0x851e8 | 15 | Grglrglblbblbe. |
| 0x851f8 | 12 | Grgleblrgle? |
| 0x85205 | 40 | I have no idea what she's trying to say. |
| 0x8522e | 25 | Glurgleblrgl! Blrblgrgl!! |
| 0x85248 | 18 | GLRGBBLBRLRGGLE!!! |
| 0x8525b | 45 | She turns red like a lobster boiling in the\n |
| 0x85289 | 46 | hot water of the bath, and the steam becomes\n |
| 0x852b8 | 6 | heavy. |
| 0x852bf | 41 | I don't understand what she's trying to\n |
| 0x852e9 | 37 | communicate, but she seems enraged... |
| 0x8530f | 50 | Looks like I don't have a choice. I'll just push\n |
| 0x85342 | 51 | the blame on Ukon and... Where the hell did he go!? |
| 0x85376 | 22 | Well, enjoy your bath! |
| 0x8538d | 42 | I turn and bolt at full tilt for the exit. |
| 0x853b8 | 27 | Hngh. Just a bit closer--!! |
| 0x853d4 | 22 | I reach for the door-- |
| 0x853eb | 6 | *YANK* |
| 0x853f2 | 5 | Whoa! |
| 0x853f8 | 48 | Then, something long and sinuous snakes around\n |
| 0x85429 | 31 | my ankle and sends me toppling. |
| 0x85449 | 21 | Ow... Ow, what just-- |
| 0x8545f | 48 | I look down to find Kuon's unusually dexterous\n |
| 0x85490 | 28 | tail wrapped around my foot. |
| 0x854ad | 4 | Gah! |
| 0x854b2 | 37 | Just where do you think you're going? |
| 0x854d8 | 7 | *PTOO!* |
| 0x854e0 | 47 | A hole the size of a fingertip suddenly tears\n |
| 0x85510 | 32 | through the wall beside my head. |
| 0x85531 | 49 | I don't approve of you trying to run away after\n |
| 0x85563 | 48 | sneaking a look at a maiden's soft, fair skin,\n |
| 0x85594 | 5 | Haku. |
| 0x8559a | 7 | No, I-- |
| 0x855a2 | 32 | I wouldn't say "snuck a look."\n |
| 0x855c3 | 33 | More like you outright SHOWED me. |
| 0x855e5 | 6 | Geez-- |
| 0x855ec | 22 | Did you say something? |
| 0x85603 | 16 | N-No, nothing... |
| 0x85614 | 43 | Kuon squeezes her fists together over the\n |
| 0x85640 | 49 | surface of the water, squirting a high-pressure\n |
| 0x85672 | 7 | stream. |
| 0x8567a | 46 | She's using her hands to squirt water like a\n |
| 0x856a9 | 44 | kid at the pool, but with her unbelievable\n |
| 0x856d6 | 11 | strength... |
| 0x856e2 | 47 | Hey, c-calm down, you're putting holes in the\n |
| 0x85712 | 44 | walls--and I didn't see anything, I promise! |
| 0x8573f | 7 | Really? |
| 0x85747 | 47 | I want to say "How could I NOT see everything\n |
| 0x85777 | 46 | you were just shaking around," but my life's\n |
| 0x857a6 | 9 | at stake. |
| 0x857b0 | 37 | Well, there was a lot of steam, so... |
| 0x857d6 | 3 | So? |
| 0x857da | 49 | So I didn't see anything! Your back was turned,\n |
| 0x8580c | 40 | and Rulutieh sank straight in the water. |
| 0x85835 | 47 | And I definitely didn't make eye contact with\n |
| 0x85865 | 43 | you. You're imagining things. That's crazy. |
| 0x85891 | 41 | ...So in other words, you saw everything. |
| 0x858bb | 5 | Uh... |
| 0x858c1 | 48 | The phrase "digging my own grave" feels apt at\n |
| 0x858f2 | 14 | this juncture. |
| 0x85901 | 47 | Haku, the sight of a maiden's soft, bare skin\n |
| 0x85931 | 23 | doesn't come cheaply... |
| 0x85949 | 40 | Time to exact a little payment, I think. |
| 0x85972 | 44 | N-No, stop--Come on, let's talk this over,\n |
| 0x8599f | 18 | you'll understand! |
| 0x859b2 | 25 | Time for your punishment! |
| 0x859cc | 11 | GYAAAAAAH!! |

## 8. Formato de saida EXIGIDO
Escreva `translations_14_03.json` com a forma:
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
