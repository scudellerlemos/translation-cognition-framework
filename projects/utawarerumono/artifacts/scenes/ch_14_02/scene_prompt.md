# Cena ch_14_02 — pacote de traducao (302 linhas)

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
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mausoleum | Local | Mausoleu | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ozen | Personagem | Ozen | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `them.` -> `deles.` (Kuon, 11_05)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `That's all.` -> `É isso.` (Ukon, 13_02)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `What?` -> `Que?` (Haku, 12_02)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `I see.` -> `Sim.` (Haku, 12_17)
- `Did you say something?` -> `Disse alguma coisa?` (Haku, 13_09)
- `here?` -> `afinal?` (Haku, 13_02)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
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
| 0x7e6d7 | 18 | Whoa, it's huge... |
| 0x7e6ea | 46 | Dwarfed by the shadow of the capital's outer\n |
| 0x7e719 | 47 | walls, I can't help but let out an exclamation. |
| 0x7e749 | 49 | The front gates are a splendid, opulent affair,\n |
| 0x7e77b | 46 | towering as high as the thick walls flanking\n |
| 0x7e7aa | 5 | them. |
| 0x7e7b0 | 45 | They have a faint luster to them, as though\n |
| 0x7e7de | 35 | they've been polished to a shine... |
| 0x7e802 | 12 | Magnificent. |
| 0x7e80f | 40 | The decorations and embellishments are\n |
| 0x7e838 | 46 | tastefully done--not just garish splashes of\n |
| 0x7e867 | 15 | gold or silver. |
| 0x7e877 | 49 | It's not gaudy, though. More... Stately. Solid.\n |
| 0x7e8a9 | 38 | This is a gate built for magnificence. |
| 0x7e8d4 | 44 | The enormity of the gates must have struck\n |
| 0x7e901 | 47 | Kuon, too--she's gazing up with her hand over\n |
| 0x7e931 | 10 | her mouth. |
| 0x7e93c | 45 | My eyes meet hers, and she seems to realize\n |
| 0x7e96a | 21 | how she's behaving... |
| 0x7e980 | 41 | Kuon's neat brows twitch for some reason. |
| 0x7e9aa | 33 | Ahahaha... No, nothing's wrong.\n |
| 0x7e9cc | 15 | Nothing at all. |
| 0x7e9dc | 25 | ...I didn't say anything? |
| 0x7e9f6 | 44 | We pass through the huge, open gates as we\n |
| 0x7ea23 | 28 | make this puzzling exchange. |
| 0x7ea40 | 44 | Inside, splendid buildings unlike any I've\n |
| 0x7ea6d | 23 | seen dot the cityscape. |
| 0x7ea85 | 47 | Far more people bustle to and fro than in the\n |
| 0x7eab5 | 41 | village, crowds swarming on every street. |
| 0x7eadf | 47 | We passed by plenty of people on the mountain\n |
| 0x7eb0f | 48 | road, but this is far more than I've ever seen\n |
| 0x7eb40 | 8 | at once. |
| 0x7eb49 | 43 | Some do business in the shops, others are\n |
| 0x7eb75 | 46 | earning their keep performing in the street... |
| 0x7eba4 | 48 | There are patrolling soldiers, porters weighed\n |
| 0x7ebd5 | 48 | down with their loads... people, people, people. |
| 0x7ec06 | 44 | Just listening to the ambient noise of the\n |
| 0x7ec33 | 33 | throng is enough to overwhelm me. |
| 0x7ec55 | 47 | Ukon said the village didn't hold a candle to\n |
| 0x7ec85 | 47 | the capital, but the difference is like night\n |
| 0x7ecb5 | 8 | and day. |
| 0x7ecbe | 53 | It's a lot to take in. The people, the buildings...\n |
| 0x7ecf4 | 16 | It's staggering. |
| 0x7ed05 | 46 | Is... Is there some kind of special occasion\n |
| 0x7ed34 | 36 | today? Like a festival or something? |
| 0x7ed59 | 45 | Hm? No, there shouldn't be anything going on. |
| 0x7ed87 | 34 | I... see. Still, so many people... |
| 0x7edaa | 47 | Eh? It's always like this. We're in the heart\n |
| 0x7edda | 14 | of the empire. |
| 0x7ede9 | 26 | Always? I-Is that... so... |
| 0x7ee04 | 13 | Something up? |
| 0x7ee12 | 4 | Huh? |
| 0x7ee17 | 45 | You've been mumbling under your breath ever\n |
| 0x7ee45 | 46 | since we passed the gates. Is something wrong? |
| 0x7ee74 | 28 | Oh... N-No, nothing's wrong. |
| 0x7ee91 | 47 | I'm just, ah... a bit taken off-guard. It's a\n |
| 0x7eec1 | 35 | little busier here than in my home. |
| 0x7eee5 | 11 | That's all. |
| 0x7eef1 | 49 | Ah, I get it now. That's why she's wearing that\n |
| 0x7ef23 | 21 | perturbed expression. |
| 0x7ef39 | 24 | She seems... frustrated? |
| 0x7ef52 | 41 | Could it be that this place puts Kuon's\n |
| 0x7ef7c | 38 | hometown to...? No, I shouldn't make\n |
| 0x7efa3 | 12 | assumptions. |
| 0x7efb0 | 44 | We're gonna head straight for the imperial\n |
| 0x7efdd | 48 | cloister to deliver all this stuff. What about\n |
| 0x7f00e | 9 | you kids? |
| 0x7f018 | 48 | Well, I suppose we should find a place to stay\n |
| 0x7f049 | 47 | for the night. We'll locate an inn as we walk\n |
| 0x7f079 | 7 | around. |
| 0x7f081 | 48 | Hm. I know a good place, if you're interested.\n |
| 0x7f0b2 | 13 | How about it? |
| 0x7f0c0 | 21 | A good place, huh...? |
| 0x7f0d6 | 46 | Kuon mulls Ukon's suggestion over, putting a\n |
| 0x7f105 | 30 | finger to her chin in thought. |
| 0x7f124 | 44 | Besides, we--Ah, crap, right. I completely\n |
| 0x7f151 | 7 | forgot. |
| 0x7f159 | 3 | Hm? |
| 0x7f15d | 39 | Well, we've got this tradition, yeah?\n |
| 0x7f185 | 46 | We hold a banquet whenever we come back home\n |
| 0x7f1b4 | 11 | from a job. |
| 0x7f1c0 | 45 | I already made reservations with this place\n |
| 0x7f1ee | 19 | ahead of time, see. |
| 0x7f202 | 19 | A banquet, you say? |
| 0x7f216 | 34 | My stomach growls at the prospect. |
| 0x7f239 | 40 | Come to think of it, I'm hungry as hell. |
| 0x7f262 | 47 | We skipped lunch on the road since we were so\n |
| 0x7f292 | 23 | close to the capital... |
| 0x7f2aa | 42 | Hmhm. In other words, you're giving us a\n |
| 0x7f2d5 | 17 | proper reception? |
| 0x7f2e7 | 48 | Kuon smiles slyly, putting special emphasis on\n |
| 0x7f318 | 14 | the word "us." |
| 0x7f327 | 45 | Weeell, it's also a good way to let the men\n |
| 0x7f355 | 15 | blow off steam. |
| 0x7f365 | 42 | I'm guessing that's the real reason, then. |
| 0x7f390 | 48 | Ahaha, I see. If that's the case, we'll gladly\n |
| 0x7f3c1 | 24 | join in the festivities. |
| 0x7f3da | 33 | Is that all right with you, Haku? |
| 0x7f3fc | 19 | Yeah, I don't mind. |
| 0x7f410 | 46 | Yes! A welcoming party. Time to score a free\n |
| 0x7f43f | 5 | meal. |
| 0x7f445 | 41 | Kuon warned me I'd be paying for things\n |
| 0x7f46f | 43 | out-of-pocket now that we're in the city,\n |
| 0x7f49b | 16 | but free food... |
| 0x7f4ac | 40 | The guys'll be happy to see you there.\n |
| 0x7f4d5 | 44 | Especially since the kid's footing the bill. |
| 0x7f502 | 5 | What? |
| 0x7f508 | 47 | Ain't nothing more delicious than free booze!\n |
| 0x7f538 | 10 | Gwahahaha! |
| 0x7f543 | 43 | ...I totally forgot. I promised I'd treat\n |
| 0x7f56f | 46 | everyone once we reached the imperial capital. |
| 0x7f59e | 46 | I'm kidding, kidding. I promised you a drink\n |
| 0x7f5cd | 42 | first, didn't I? Let me make good on that. |
| 0x7f5f8 | 40 | I-If you insist, then... Thank you for\n |
| 0x7f621 | 12 | treating me. |
| 0x7f62e | 23 | Haku, you've gone pale. |
| 0x7f646 | 44 | H-Haha, uhm. Y-You must be imagining things. |
| 0x7f673 | 46 | Anyway, we're gonna be having the banquet at\n |
| 0x7f6a2 | 46 | the inn I was gonna recommend to you anyway,\n |
| 0x7f6d1 | 5 | so... |
| 0x7f6d7 | 49 | Just take my word for it and give 'em a chance.\n |
| 0x7f709 | 29 | For one thing, they've got... |
| 0x7f727 | 45 | Well, you'll see. I think you'll especially\n |
| 0x7f755 | 15 | like it, missy. |
| 0x7f765 | 41 | Almost there. You can see it up ahead--\n |
| 0x7f78f | 22 | it's that gate, there. |
| 0x7f7a6 | 23 | Where's he pointing...? |
| 0x7f7be | 48 | I try to follow the line of Ukon's finger with\n |
| 0x7f7ef | 8 | my eyes. |
| 0x7f7f8 | 44 | ...He's talking about that gate way off in\n |
| 0x7f825 | 47 | the distance. It's so far off, it looks tiny.\n |
| 0x7f855 | 6 | Great. |
| 0x7f85c | 47 | I continue to follow behind him, griping in a\n |
| 0x7f88c | 12 | small voice. |
| 0x7f899 | 13 | What is that? |
| 0x7f8a7 | 43 | Kuon points at something--it looks like a\n |
| 0x7f8d3 | 46 | white, flat-topped mountain in the center of\n |
| 0x7f902 | 9 | the city. |
| 0x7f90c | 47 | It's tall enough that it can probably be seen\n |
| 0x7f93c | 29 | from anywhere in the capital. |
| 0x7f95a | 25 | Ah, that's the Mausoleum. |
| 0x7f974 | 10 | Mausoleum? |
| 0x7f97f | 47 | It's like... Yamato's grand altar, or shrine,\n |
| 0x7f9af | 23 | or something like that. |
| 0x7f9c7 | 47 | You could call it the spiritual center of the\n |
| 0x7f9f7 | 42 | city. Festivals go on there, prayers for\n |
| 0x7fa22 | 11 | harvests... |
| 0x7fa2e | 6 | I see. |
| 0x7fa35 | 45 | Kuon replies distantly, but her eyes remain\n |
| 0x7fa63 | 37 | fixed on the shrine, lingering on it. |
| 0x7fa89 | 47 | She seems more interested in it than her tone\n |
| 0x7fab9 | 19 | of voice implied... |
| 0x7facd | 22 | Did you say something? |
| 0x7fae4 | 16 | Hm? No, nothing. |
| 0x7faf5 | 48 | This place looks important. It's probably some\n |
| 0x7fb26 | 46 | kind of governmental or administrative center. |
| 0x7fb55 | 47 | Walls and a gate separate it from the rest of\n |
| 0x7fb85 | 43 | the city, and guards stand vigilant watch\n |
| 0x7fbb1 | 12 | around it... |
| 0x7fbbe | 47 | With the dull roar of the crowd more distant,\n |
| 0x7fbee | 45 | now, I can pick up a quiet, murmuring voice\n |
| 0x7fc1c | 10 | behind me. |
| 0x7fc27 | 47 | I am Rulutieh, daughter and emissary of Ozen,\n |
| 0x7fc57 | 18 | owlo of Kujyuri... |
| 0x7fc6a | 47 | I have come to humbly present the trade goods\n |
| 0x7fc9a | 42 | of my country and pay due tribute to the\n |
| 0x7fcc5 | 7 | Mikado. |
| 0x7fccd | 48 | Ah, I get it. She's rehearsing what she'll say\n |
| 0x7fcfe | 42 | when she presents her country's offerings. |
| 0x7fd29 | 43 | Rulutieh continues to recite her lines to\n |
| 0x7fd55 | 34 | herself, muttering under breath... |
| 0x7fd78 | 42 | A gatekeeper flags us down as we approach. |
| 0x7fda3 | 10 | Gate guard |
| 0x7fdae | 45 | State your name and business. What seek you\n |
| 0x7fddc | 5 | here? |
| 0x7fde2 | 35 | ...What do we do in this situation? |
| 0x7fe06 | 30 | I glance over at Ukon, lost... |
| 0x7fe25 | 45 | ...who, in turn--well, more like everyone--\n |
| 0x7fe53 | 30 | looks at Rulutieh expectantly. |
| 0x7fe72 | 7 | ...eep. |
| 0x7fe7a | 48 | No doubt feeling the eyes of the group on her,\n |
| 0x7feab | 31 | Rulutieh walks forward stiffly. |
| 0x7fecb | 20 | I, I-I--I am, uhm... |
| 0x7fee0 | 44 | Rulutieh, d-d-daughter and em--emissary of\n |
| 0x7ff0d | 19 | O-Ozen, and, uhm... |
| 0x7ff21 | 49 | Her voice gradually becomes smaller and smaller\n |
| 0x7ff53 | 42 | as she speaks, her eyes fixed on her feet. |
| 0x7ff7e | 40 | Before long, she's mumbling in a tiny,\n |
| 0x7ffa7 | 44 | inaudible voice, and no one can make out a\n |
| 0x7ffd4 | 12 | single word. |
| 0x7ffe1 | 41 | ...Which the gatekeeper probably wasn't\n |
| 0x8000b | 46 | expecting, because he looks to us, then back\n |
| 0x8003a | 18 | at her, flummoxed. |
| 0x8004d | 32 | Ahem... I'm sorry, miss, but--\n |
| 0x8006e | 22 | Could you repeat that? |
| 0x80085 | 23 | I... I am, uhm. I am... |
| 0x8009d | 47 | Calling her out may have been the wrong thing\n |
| 0x800cd | 40 | to do. She shrinks away and pulls into\n |
| 0x800f6 | 10 | herself... |
| 0x80101 | 45 | Looks like she's having difficulty with all\n |
| 0x8012f | 39 | this. Can we get a move on? I'm hungry. |
| 0x80157 | 41 | We're gonna be here all day at this rate. |
| 0x80181 | 42 | I guess I have no choice. I'm gonna take\n |
| 0x801ac | 26 | matters into my own hands. |
| 0x801c7 | 49 | We're envoys of Lord Ozen, the owlo of Kujyuri.\n |
| 0x801f9 | 45 | This is his esteemed daughter, Lady Rulutieh. |
| 0x80227 | 9 | H-Huh...? |
| 0x80231 | 48 | We have come to humbly present the trade goods\n |
| 0x80262 | 43 | of her country and pay due tribute to the\n |
| 0x8028e | 45 | Understood. Please forgive my impertinence.\n |
| 0x802bc | 39 | I didn't realize you were Lord Ozen's\n |
| 0x802e4 | 11 | contingent. |
| 0x802f0 | 44 | If you would allow me to verify your seal,\n |
| 0x8031d | 7 | please? |
| 0x80325 | 16 | Milady Rulutieh? |
| 0x80336 | 23 | Huh? Y-Yes, of course-- |
| 0x8034e | 23 | If I may see your seal? |
| 0x80366 | 18 | Yes, right away... |
| 0x80379 | 47 | Rulutieh produces a palm-sized block from her\n |
| 0x803a9 | 39 | sleeve, carved with some kind of sigil. |
| 0x803d1 | 44 | ...Very well. Thank you for journeying all\n |
| 0x803fe | 31 | this way, milady. You may pass. |
| 0x8041e | 5 | Ah... |
| 0x80424 | 15 | Thank... you... |
| 0x80434 | 10 | Thank you? |
| 0x8043f | 9 | For what? |
| 0x80449 | 32 | Did I do something worth thanks? |
| 0x8046a | 11 | Well, ah... |
| 0x80476 | 39 | Erm... Wh-What you did for me just now. |
| 0x8049e | 48 | I think she's talking about how you bailed her\n |
| 0x804cf | 38 | out and made her introduction for her. |
| 0x804f6 | 14 | Huh? Oh. That. |
| 0x80505 | 46 | You didn't strike me as the type to run to a\n |
| 0x80534 | 46 | lady's rescue, Haku. I'm seeing you in a new\n |
| 0x80563 | 6 | light. |
| 0x8056a | 17 | R-Really? Haha... |
| 0x8057c | 37 | ...I can't bring myself to tell them. |
| 0x805a2 | 44 | I only spoke over Rulutieh because I'm the\n |
| 0x805cf | 47 | hungriest I've ever been and just want to get\n |
| 0x805ff | 12 | to the food. |
| 0x8060c | 7 | Urgh... |
| 0x80614 | 37 | Rulutieh shyly bows in front of me... |
| 0x8063a | 45 | Please don't look at me with those innocent\n |
| 0x80668 | 45 | eyes. I don't deserve this. I am a charlatan. |
| 0x80696 | 4 | Heh. |
| 0x8069b | 47 | Rulutieh looks at me with warm gratitude, and\n |
| 0x806cb | 23 | Kuon smiles at us both. |
| 0x806e3 | 47 | ...Kuon probably would have helped her out if\n |
| 0x80713 | 23 | I hadn't done anything. |
| 0x8072b | 30 | Did I need to speak up at all? |
| 0x8074a | 41 | Eventually, we arrive in a rich-looking\n |
| 0x80774 | 45 | neighborhood, the road lined by manors with\n |
| 0x807a2 | 12 | tiled roofs. |
| 0x807af | 50 | Each estate has a proper moat and thick, earthen\n |
| 0x807e2 | 46 | walls, giving them an old-fashioned, stately\n |
| 0x80811 | 5 | look. |
| 0x80817 | 41 | All right, this is the place. We're here. |
| 0x80841 | 38 | At Ukon's words, I look up to find a\n |
| 0x80868 | 45 | particularly large, splendid manor standing\n |
| 0x80896 | 18 | out from the rest. |
| 0x808a9 | 43 | Finally. This city is way too big to walk\n |
| 0x808d5 | 42 | We've been waiting for you, Master Ukon.\n |
| 0x80900 | 36 | I trust your excursion was fruitful. |
| 0x80925 | 44 | Another gatekeeper comes jogging up to our\n |
| 0x80952 | 6 | group. |
| 0x80959 | 45 | We just got back. This is the offering from\n |
| 0x80987 | 34 | Kujyuri. Take good care of it now. |
| 0x809aa | 9 | Yes, sir! |
| 0x809b4 | 32 | I'll leave the rest to you guys. |
| 0x809d5 | 31 | Yes, s... Sir? W-Wait a minute! |
| 0x809f5 | 46 | Ukon wearily rubs at his shoulders and turns\n |
| 0x80a24 | 40 | to go, only stopped by a hurried sentry. |
| 0x80a4d | 42 | Wh-Where are you going? You need to file\n |
| 0x80a78 | 45 | paperwork, observe the standard protocols...! |
| 0x80aa6 | 48 | Eh, sorry. I'm beat. I'll handle all that later. |
| 0x80ad7 | 6 | Wait-- |
| 0x80ade | 46 | Was it really OK to just leave them with the\n |
| 0x80b0d | 20 | offerings like that? |
| 0x80b22 | 44 | Though I am grateful that we don't have to\n |
| 0x80b4f | 36 | sit around and wait for paperwork... |
| 0x80b74 | 44 | Rulutieh sways uneasily, looking as though\n |
| 0x80ba1 | 47 | she wants to say something, but remains silent. |
| 0x80bd1 | 42 | Yeah, the plan was always to bring it to\n |
| 0x80bfc | 15 | Oshtor's manor. |
| 0x80c0c | 38 | Oshtor... That guy with the mask, huh? |
| 0x80c33 | 47 | Yep. He'll take care of all that protocol and\n |
| 0x80c63 | 19 | bureaucratic stuff. |
| 0x80c77 | 39 | So don't worry about it, Lady Rulutieh. |
| 0x80c9f | 46 | I know you're anxious and you want to make a\n |
| 0x80cce | 49 | good impression, but let people help sometimes,\n |
| 0x80d00 | 5 | yeah? |
| 0x80d06 | 7 | O-OK... |
| 0x80d0e | 45 | Now! I think we've got a banquet to get to,\n |
| 0x80d3c | 17 | isn't that right? |
| 0x80d4e | 45 | Ukon leads the way, and we all follow along\n |
| 0x80d7c | 8 | eagerly. |
| 0x80d85 | 40 | ...Hm? I only noticed just now, but...\n |
| 0x80dae | 31 | Where did the twins run off to? |
| 0x80dce | 43 | I could've sworn they were with us at the\n |
| 0x80dfa | 8 | gates... |
| 0x80e03 | 49 | As is their wont, it seems like that mysterious\n |
| 0x80e35 | 42 | duo has wandered off again without a word. |

## 8. Formato de saida EXIGIDO
Escreva `translations_14_02.json` com a forma:
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
