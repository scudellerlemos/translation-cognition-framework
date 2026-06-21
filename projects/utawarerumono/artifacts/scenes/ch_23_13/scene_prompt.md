# Cena ch_23_13 — pacote de traducao (260 linhas)

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
| Akuruturuka | Termo | Akuruturuka | manter_original | major |
| Atuy | Personagem | Atuy | manter_original | none |
| Benawi | Personagem | Benawi | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurou | Personagem | Kurou | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Saraana | Personagem | Saraana | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- `favor.` -> `favora.` (Atuy, 16_02)
- `off.` -> `apagar.` (Haku, 23_11)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `D-Dear sister...?` -> `D-Querida irmã...?` (Haku, 20_06)
- `Akuruturuka?` -> `Akuruturuka?` (Oshtor, 20_13)
- `That's...` -> `Isso...` (Haku, 15_01)
- `yet.` -> `ainda.` (Homem, 18_01)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Miss Kuon...` -> `Senhora Kuon...` (Rulutieh, 13_05)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `for you.` -> `para você.` (Ougi, 13_08)
- `Whup.` -> `Opa.` (Personagem genérico, 18_01)
- `Wh--!?` -> `Q-Quê!?` (Haku, 18_01)
- `Gah!` -> `Ai!` (Man, 11_01)
- `Ah!` -> `Ah!` (Garota, 18_01)
- `Hee hee...` -> `Hehe...` (Kuon, 11_02)
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `Tuskur soldier` -> `Soldado de Tuskur` (Haku, 23_09)
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
| 0x2ae6ea | 17 | ...Enemy subdued. |
| 0x2ae6fc | 35 | Breathing and heart rates stable.\n |
| 0x2ae720 | 23 | They are incapacitated. |
| 0x2ae738 | 15 | They're good... |
| 0x2ae748 | 45 | So this is what fighting Tuskur soldiers is\n |
| 0x2ae776 | 29 | like... They're well-trained. |
| 0x2ae794 | 48 | Everyone held to my orders not to kill anyone,\n |
| 0x2ae7c5 | 44 | but we can't keep holding back at this rate. |
| 0x2ae7f2 | 44 | If we'd even made one mistake, it probably\n |
| 0x2ae81f | 25 | would have meant death... |
| 0x2ae839 | 48 | Not bad. Looks like the wind's shiftin' in our\n |
| 0x2ae86a | 6 | favor. |
| 0x2ae871 | 48 | All right. Let's do this just like we planned.\n |
| 0x2ae8a2 | 17 | Ready, Jachdwalt? |
| 0x2ae8b4 | 46 | Sure thing. If you're trustin' me with this,\n |
| 0x2ae8e3 | 37 | 'least I can do is make good on that. |
| 0x2ae909 | 45 | Haku, we need to hurry. We haven't got much\n |
| 0x2ae937 | 10 | time left. |
| 0x2ae942 | 45 | Kuon, I understand we can't lollygag, but I\n |
| 0x2ae970 | 44 | think you're getting too anxious about this. |
| 0x2ae99d | 46 | Haku--Everyone else, too. You're all failing\n |
| 0x2ae9cc | 17 | to understand me. |
| 0x2ae9de | 16 | Understand what? |
| 0x2ae9ef | 48 | I'm worried for my country, sure, but I'm much\n |
| 0x2aea20 | 30 | more worried about all of you. |
| 0x2aea3f | 39 | What do you mean, much MORE worried...? |
| 0x2aea6b | 47 | Haku, do you really think Yamato can win this\n |
| 0x2aea9b | 4 | war? |
| 0x2aeaa0 | 46 | Huh? I mean... Things aren't looking too hot\n |
| 0x2aeacf | 48 | right now, maybe, but I think they can pull it\n |
| 0x2aeb00 | 4 | off. |
| 0x2aeb05 | 48 | I'm fairly sure Yamato's not going to "pull it\n |
| 0x2aeb36 | 5 | off." |
| 0x2aeb3c | 7 | ...Huh? |
| 0x2aeb44 | 46 | In fact, I'm certain that Yamato is going to\n |
| 0x2aeb73 | 14 | lose this war. |
| 0x2aeb82 | 17 | D-Dear sister...? |
| 0x2aeb94 | 44 | Hold on. What do you mean, you're certain?\n |
| 0x2aebc1 | 42 | You know they have Munechika, right? The\n |
| 0x2aebec | 12 | Akuruturuka? |
| 0x2aebf9 | 46 | Sure, Tuskur is a force to be reckoned with,\n |
| 0x2aec28 | 41 | but I wouldn't count Yamato out just yet. |
| 0x2aec52 | 48 | I'm sure you've noticed, Haku. The Tuskur army\n |
| 0x2aec83 | 44 | could annihilate Yamato's if they wanted to. |
| 0x2aecb0 | 46 | But Tuskur's been holding back on taking the\n |
| 0x2aecdf | 10 | offensive. |
| 0x2aecea | 9 | That's... |
| 0x2aecf4 | 49 | She's right. Even with Yamato's forces isolated\n |
| 0x2aed26 | 50 | and weakened, they haven't made a focused attack\n |
| 0x2aed59 | 4 | yet. |
| 0x2aed5e | 48 | If they really intended to take the offensive,\n |
| 0x2aed8f | 42 | they had a chance to take that fortress... |
| 0x2aedba | 45 | But couldn't the same thing be said for the\n |
| 0x2aede8 | 44 | Yamatans? If they had their full strength... |
| 0x2aee15 | 50 | That's not it, Haku. It's not that Yamato wasn't\n |
| 0x2aee48 | 49 | fighting at its full potential--it wasn't being\n |
| 0x2aee7a | 8 | ALLOWED. |
| 0x2aee83 | 49 | Nobody in the Yamato army noticed how they were\n |
| 0x2aeeb5 | 46 | slowly tying the noose around their own necks. |
| 0x2aeee4 | 49 | Whittling down their numbers, holding out false\n |
| 0x2aef16 | 47 | hope of victory until the point of no return... |
| 0x2aef46 | 49 | It's a tactic that a certain mononofu of Tuskur\n |
| 0x2aef78 | 10 | excels at. |
| 0x2aef83 | 49 | And if I had to guess... I'd say that person is\n |
| 0x2aefb5 | 16 | here. Right now. |
| 0x2aefc6 | 14 | "That person"? |
| 0x2aefd5 | 7 | Soldier |
| 0x2aefdd | 43 | Lady Munechika, we've received no word of\n |
| 0x2af009 | 38 | movement from Lord Dekopompo's forces. |
| 0x2af030 | 48 | ...It matters not. I did not intend to rely on\n |
| 0x2af061 | 26 | him for this plan, anyway. |
| 0x2af07c | 50 | Sound the retreat. We will fall back and regroup\n |
| 0x2af0af | 23 | outside of their range. |
| 0x2af0c7 | 11 | Understood! |
| 0x2af0d3 | 48 | My soldiers are highly experienced in the arts\n |
| 0x2af104 | 48 | of war, and yet this fortress eludes my grasp... |
| 0x2af135 | 43 | I must admit that I've underestimated the\n |
| 0x2af161 | 17 | enemy's strength. |
| 0x2af173 | 42 | And this knot of foreboding in my chest... |
| 0x2af19e | 46 | I worry that we're entrenching ourselves far\n |
| 0x2af1cd | 9 | too deep. |
| 0x2af1d7 | 46 | Please be careful, Lord Haku. It may be that\n |
| 0x2af206 | 16 | we are already-- |
| 0x2af217 | 26 | Lady Munechika, the gates! |
| 0x2af232 | 3 | Hm? |
| 0x2af236 | 35 | The gates... Are they launching a\n |
| 0x2af25a | 45 | counteroffensive? But that sacrifices their\n |
| 0x2af288 | 12 | advantage... |
| 0x2af295 | 46 | Are they so conceited as to throw away their\n |
| 0x2af2c4 | 43 | high ground, or...? No. No, that is not it. |
| 0x2af2f0 | 37 | ...I see. We finally meet, you and I. |
| 0x2af316 | 45 | When the perfect opportunity arrives, he'll\n |
| 0x2af344 | 33 | show himself on the battlefield-- |
| 0x2af366 | 49 | Ironic. At the moment I least wish to face him,\n |
| 0x2af398 | 46 | the man I've been waiting for finally appears. |
| 0x2af3c7 | 16 | Kuon & Munechika |
| 0x2af3d8 | 32 | The Warmaster of Tuskur, Benawi! |
| 0x2af3f9 | 27 | The Warmaster of Tuskur...? |
| 0x2af415 | 47 | Benawi's lieutenant is probably on the field,\n |
| 0x2af445 | 36 | too. He craves battle above all el-- |
| 0x2af46a | 43 | Oh, man. Took you long enough to show up,\n |
| 0x2af496 | 10 | didn't it? |
| 0x2af4a4 | 39 | Crap, there were still enemies around-- |
| 0x2af4cc | 47 | And here I was, waiting all patiently for you\n |
| 0x2af4fc | 42 | to try and retake those stolen supplies... |
| 0x2af527 | 17 | It... can't be... |
| 0x2af539 | 43 | But man, FLYING up? Even the chief wasn't\n |
| 0x2af565 | 19 | expecting that one. |
| 0x2af579 | 42 | This guy's... Everyone, stand back. This\n |
| 0x2af5a4 | 26 | could get ugly in a hurry. |
| 0x2af5bf | 28 | Huh? What do you mean, ugly? |
| 0x2af5dc | 7 | Oooh... |
| 0x2af5e4 | 41 | I'll be damned! Who could've expected it? |
| 0x2af60e | 50 | I thought you were busy making a mess across the\n |
| 0x2af641 | 33 | sea. What brings you back here... |
| 0x2af663 | 11 | ...my lady? |
| 0x2af66f | 8 | Kurou... |
| 0x2af678 | 23 | Dear sister, is that... |
| 0x2af690 | 27 | Does... this guy know Kuon? |
| 0x2af6ac | 50 | No, don't focus on that. He said something else.\n |
| 0x2af6df | 44 | Something about expecting an attack from us? |
| 0x2af70c | 12 | Blade_Center |
| 0x2af71a | 12 | Blade_Dummy1 |
| 0x2af727 | 50 | And fraternizing with the enemy, too! Is someone\n |
| 0x2af75a | 35 | having her little rebellious phase? |
| 0x2af77e | 25 | Oh, but how time flies... |
| 0x2af798 | 13 | Kurou... I... |
| 0x2af7a6 | 47 | Come, now, don't make that face. You know the\n |
| 0x2af7d6 | 44 | score. You've got it all figured out, right? |
| 0x2af803 | 40 | We all go through this when we're young. |
| 0x2af82c | 49 | Oh, I know. Could it be you're thinking of this\n |
| 0x2af85e | 44 | as your grand betrayal? Tearing it all down? |
| 0x2af88b | 43 | Heh. But that's not quite true, now, is it? |
| 0x2af8b7 | 46 | As if a pup going on the rampage is going to\n |
| 0x2af8e6 | 44 | hurt anyone. A little nibble at the ankle,\n |
| 0x2af913 | 13 | nothing more. |
| 0x2af921 | 4 | Wh-- |
| 0x2af926 | 49 | I suppose it's your right as a child to see the\n |
| 0x2af958 | 44 | world as you please. Go on, then, pup. Rage! |
| 0x2af985 | 50 | Kurou, is that what you think? That I'm treating\n |
| 0x2af9b8 | 28 | all this as a childish game? |
| 0x2af9d5 | 9 | It isn't? |
| 0x2af9df | 8 | ...Nngh. |
| 0x2af9e8 | 45 | Do you have ANY idea how I've agonized over\n |
| 0x2afa16 | 9 | all this? |
| 0x2afa20 | 43 | And you have the gall to call it a game...? |
| 0x2afa4c | 12 | Miss Kuon... |
| 0x2afa59 | 48 | Ahahahaha! "Agonized," was it? A little trifle\n |
| 0x2afa8a | 48 | like this was all it took to make your resolve\n |
| 0x2afabb | 6 | waver? |
| 0x2afac2 | 14 | In that case-- |
| 0x2afad1 | 4 | Eep! |
| 0x2afad6 | 24 | Nekone, stay behind me-- |
| 0x2afaef | 43 | I think your resolve's just a touch weak,\n |
| 0x2afb1b | 28 | wouldn't you agree, my lady? |
| 0x2afb38 | 43 | Nothing like the kind of resolve it takes\n |
| 0x2afb64 | 28 | to stand on the battlefield! |
| 0x2afb81 | 47 | No matter who they are, if they stand against\n |
| 0x2afbb1 | 41 | you on the field--You cut them down and\n |
| 0x2afbdb | 9 | press on! |
| 0x2afbe5 | 43 | Even if it's your countryman. Your loving\n |
| 0x2afc11 | 24 | parent. Even your child! |
| 0x2afc2a | 48 | Even if that person is the beloved treasure of\n |
| 0x2afc5b | 18 | your sworn liege-- |
| 0x2afc6e | 18 | You cut them down! |
| 0x2afc81 | 37 | THAT'S what it means to have resolve! |
| 0x2afca7 | 43 | I'd appreciate it if you didn't push your\n |
| 0x2afcd3 | 20 | warped ideals on me. |
| 0x2afce8 | 31 | D-Dear sister... This man is... |
| 0x2afd08 | 41 | It's all right, Nekone. I'll protect you. |
| 0x2afd38 | 11 | Cocopo...\n |
| 0x2afd44 | 7 | Cocopo? |
| 0x2afd4c | 50 | Why so surprised? This is what it means to stand\n |
| 0x2afd7f | 27 | on opposite sides of a war. |
| 0x2afd9b | 48 | If you've just come to chat, that's one thing.\n |
| 0x2afdcc | 46 | Otherwise, I can hardly let you skip merrily\n |
| 0x2afdfb | 11 | off, can I? |
| 0x2afe07 | 41 | Especially if you want to play with the\n |
| 0x2afe31 | 43 | grownups. Or is this all a game, after all? |
| 0x2afe5d | 46 | If that's the case, I can just close my eyes\n |
| 0x2afe8c | 42 | and pretend I didn't see anything, if it\n |
| 0x2afeb7 | 12 | pleases you. |
| 0x2afec4 | 26 | So, what's it going to be? |
| 0x2afedf | 49 | If we turn back now, he'll let us off the hook... |
| 0x2aff11 | 48 | How very kind of him... Condescending bastard.\n |
| 0x2aff42 | 42 | We didn't come this far just to back down. |
| 0x2aff6d | 49 | Still, he feels different from the ones we just\n |
| 0x2aff9f | 9 | fought... |
| 0x2affa9 | 41 | Kuon's been on-edge since he showed up.\n |
| 0x2affd3 | 40 | He's definitely not an ordinary soldier. |
| 0x2afffc | 48 | Not to mention how anxious she's been... She's\n |
| 0x2b002d | 41 | been worried about running into this guy. |
| 0x2b0057 | 45 | What should we do? Take the chance, or fall\n |
| 0x2b0085 | 5 | back? |
| 0x2b008b | 39 | What's the matter? If you're not in a\n |
| 0x2b00b3 | 45 | decision making mood, I can speed things up\n |
| 0x2b00e1 | 8 | for you. |
| 0x2b00ea | 23 | Ahaha... Hee hee hee... |
| 0x2b0102 | 24 | Ahahaha... AHAHAHAHA--!! |
| 0x2b011b | 23 | Shit. Shit! Atuy, STOP! |
| 0x2b0133 | 5 | Whup. |
| 0x2b014c | 4 | Aha! |
| 0x2b0151 | 10 | C-Cocopo!? |
| 0x2b015c | 21 | Both of you! With me! |
| 0x2b0172 | 21 | Hup, hup, aaand hup-- |
| 0x2b0188 | 49 | Nngh. All right, if that's how you wish to play\n |
| 0x2b01ba | 4 | it-- |
| 0x2b01bf | 6 | Wh--!? |
| 0x2b01c6 | 45 | Not bad. Not bad at all. You were VERY close. |
| 0x2b01f4 | 29 | Here! You can have this back. |
| 0x2b0212 | 4 | Gah! |
| 0x2b0217 | 15 | And these, too! |
| 0x2b0227 | 3 | Ah! |
| 0x2b022b | 10 | Hee hee... |
| 0x2b0236 | 39 | Well, aren't you a feisty little thing? |
| 0x2b025e | 47 | Tch... Damn it. We'll force our way past him!\n |
| 0x2b028e | 10 | Jachdwalt! |
| 0x2b0299 | 11 | Here, boss. |
| 0x2b02a5 | 37 | Uruuru, Saraana. Keep your guards up. |
| 0x2b02cb | 13 | Acknowledged. |
| 0x2b02d9 | 6 | Kuon-- |
| 0x2b02e0 | 49 | ...I'm... I'm fine. I've already made up my mind. |
| 0x2b0312 | 4 | Oho? |
| 0x2b0317 | 22 | You, boy. You're...?\n |
| 0x2b032e | 13 | Ahaha, I see. |
| 0x2b033c | 31 | This just keeps getting better! |
| 0x2b0719 | 27 | Tuskur & Uzurushan soldiers |
| 0x2b0735 | 48 | Welcome, one and all, to the Tournament of the\n |
| 0x2b0766 | 8 | Bravest! |
| 0x2b076f | 17 | Uzurushan soldier |
| 0x2b0781 | 44 | I am the bravest warrior in all of Uzurusha! |
| 0x2b07ae | 14 | Tuskur soldier |
| 0x2b07bd | 46 | And I am the bravest warrior in all of Tuskur! |
| 0x2b07ec | 45 | Are you the man we await? The man they call\n |
| 0x2b081a | 38 | the bravest warrior in all of Yamato!? |
| 0x2b0841 | 39 | I see. Then as fellow brave warriors... |
| 0x2b0869 | 26 | Tuskur & Uzurushan soldier |
| 0x2b0884 | 47 | Let us fight to see who is the bravest of ALL\n |
| 0x2b08b4 | 9 | warriors! |
| 0x2b08be | 12 | Have at you! |
| 0x2b08cb | 10 | For glory! |
| 0x2b08d6 | 18 | The battle begins! |
| 0x2b08e9 | 8 | HUZZAH!! |
| 0x2b08f2 | 45 | God, these guys are pushy. Well... at least\n |
| 0x2b0920 | 48 | this one's pretty straightforward. Works for me. |
| 0x2b0951 | 18 | Fine! Bring it on! |
| 0x2b0a81 | 14 | Tuskur soldier |
| 0x2b0a90 | 44 | Urgh... I yield! It seems I must admit you\n |
| 0x2b0abd | 24 | are the greater warrior! |
| 0x2b0ad6 | 17 | Uzurushan soldier |
| 0x2b0ae8 | 44 | You truly are the bravest of brave warriors! |
| 0x2b0b15 | 33 | I dub thee the almighty overlord! |
| 0x2b0b37 | 34 | Here stands our almighty overlord! |
| 0x2b0b5a | 27 | Tuskur & Uzurushan soldiers |
| 0x2b0b76 | 37 | Almighty overlord! Almighty overlord! |
| 0x2b0b9c | 44 | Ugh... I can't believe I thought that name\n |
| 0x2b0bc9 | 34 | sounded cool, even for a second... |
| 0x2b0d99 | 36 | Ngh... I can't... let it end here... |
| 0x2b0dbe | 43 | Is that really all your resolve is worth,\n |
| 0x2b0dea | 8 | my lady? |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_13.json` com a forma:
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
