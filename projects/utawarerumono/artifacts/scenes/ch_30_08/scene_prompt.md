# Cena ch_30_08 — pacote de traducao (258 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
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
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `darkness.` -> `escuridão.` (Narrator, 31_02)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `Vurai...` -> `Vurai...` (Haku, 30_01)
- `Father...` -> `Pai...` (Garota, 20_21)
- `I... I...` -> `E-E...` (Haku, 17_01)
- `I...` -> `Eu...` (Nekone, 14_04)
- `Yamato.` -> `Yamato.` (Haku, 17_01)
- `now.` -> `já.` (Kuon, 14_04)
- `her back.` -> `para trás.` (Narrador, 23_14)
- `Oshtor...` -> `Oshtor...` (Haku, 18_01)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Rrrgh...` -> `Agh...` (Kuon, 18_01)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `Silence!` -> `Silêncio!` (Maroro, 19_05)
- `instantly.` -> `de imediato.` (Narrador, 23_14)
- `others.` -> `outros.` (Haku, 23_09)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Eep...` -> `Uih...` (Haku, 20_05)
- `woman.` -> `mulher.` (Mulher, 17_01)
- `Wh--!?` -> `Q-Quê!?` (Haku, 18_01)
- `forward.` -> `adiante.` (Oshtor, 19_01)
- `mask` -> `mask` (SYSTEM, 20_14)
- `Haku...` -> `Haku...` (Kuon, 11_02)
- `Yeah, I know.` -> `Sim, eu sei.` (Protagonista, 14_07)
- `Lady-in-waiting` -> `Dama de companhia` (Ukon, 30_04)
- `U-Understood!` -> `Eu- Entendi!` (Garota, 30_01)
- `your judgement.` -> `seu julgamento.` (Ougi, 13_05)
- `attention.` -> `muita atenção.` (Ukon, 15_01)
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
| 0x2e6b96 | 47 | Within the confines of a lonely room, faintly\n |
| 0x2e6bc6 | 29 | illuminated in the dim air... |
| 0x2e6be4 | 44 | Anju sits alone, staring blankly into space. |
| 0x2e6c11 | 46 | Her eyes, once so full of energy, are devoid\n |
| 0x2e6c40 | 44 | of life. All that now remains is reflected\n |
| 0x2e6c6d | 9 | darkness. |
| 0x2e6c7b | 49 | Her mind feels clouded, weighed down by a heavy\n |
| 0x2e6cad | 36 | mist... as though adrift in a dream. |
| 0x2e6cd2 | 27 | What... What am I doing...? |
| 0x2e6cee | 38 | Why... does my body refuse to move...? |
| 0x2e6d15 | 46 | From time to time, questions rise in her mind. |
| 0x2e6d44 | 49 | But before they can solidify, they are engulfed\n |
| 0x2e6d76 | 43 | by darkness, vanishing like popped bubbles. |
| 0x2e6da2 | 30 | Is... Is there anyone here...? |
| 0x2e6dc1 | 10 | Anyone...? |
| 0x2e6dcc | 39 | Suddenly, the door opens with a slam.\n |
| 0x2e6df4 | 46 | A shadow falls over Anju's vision, darkening\n |
| 0x2e6e23 | 17 | the room further. |
| 0x2e6e35 | 7 | Huh...? |
| 0x2e6e3d | 44 | She slowly raises her head to see a large,\n |
| 0x2e6e6a | 34 | cold-eyed man looking down at her. |
| 0x2e6e8d | 13 | Ah... hhhh... |
| 0x2e6e9b | 8 | Vurai... |
| 0x2e6ea4 | 49 | Her lifeless eyes cloud over, ever so slightly,\n |
| 0x2e6ed6 | 20 | with a hint of fear. |
| 0x2e6eeb | 21 | Princess... No, Anju. |
| 0x2e6f01 | 47 | Vurai continues to stare down at Anju, but he\n |
| 0x2e6f31 | 41 | soon speaks, rumbling voice pitying and\n |
| 0x2e6f5b | 11 | disdainful. |
| 0x2e6f67 | 44 | You are yet far too small, and far too weak. |
| 0x2e6f94 | 47 | What can you protect, with those feeble arms?\n |
| 0x2e6fc4 | 43 | What can you kill? What can you accomplish? |
| 0x2e6ff0 | 44 | The answer... is nothing. You are pitiful,\n |
| 0x2e701d | 43 | you are powerless, and that is all you are. |
| 0x2e7049 | 29 | What... What is he saying...? |
| 0x2e7067 | 47 | Our liege has passed. However, there are none\n |
| 0x2e7097 | 23 | left to take his place. |
| 0x2e70af | 46 | What are you saying...? I... I am to succeed\n |
| 0x2e70de | 9 | Father... |
| 0x2e70e8 | 45 | Do you think you... you, of all people, can\n |
| 0x2e7116 | 45 | stand and lead us? The Eight Pillar Generals? |
| 0x2e7144 | 9 | I... I... |
| 0x2e714e | 43 | What can you possibly show us to earn our\n |
| 0x2e717a | 8 | loyalty? |
| 0x2e7183 | 49 | Your frail arms, that could snap under the most\n |
| 0x2e71b5 | 18 | meager of weights? |
| 0x2e71c8 | 49 | Your radiance, barely that of a dying firefly's\n |
| 0x2e71fa | 15 | flickering ass? |
| 0x2e720a | 4 | I... |
| 0x2e720f | 10 | Ludicrous. |
| 0x2e721a | 48 | As Vurai extends his fist, Anju can only stare\n |
| 0x2e724b | 39 | blankly, her focus drifting in and out. |
| 0x2e7273 | 36 | You have no right to stand above me. |
| 0x2e7298 | 49 | The only one that does... is one who has proven\n |
| 0x2e72ca | 21 | their absolute power. |
| 0x2e72e0 | 43 | A new era of war now dawns on our land of\n |
| 0x2e730c | 7 | Yamato. |
| 0x2e7314 | 32 | This is the will of the heavens. |
| 0x2e7335 | 47 | Only one who can conquer all else may rise to\n |
| 0x2e7365 | 43 | Yamato's summit. One chosen by the heavens! |
| 0x2e7391 | 11 | Ah... hh... |
| 0x2e739d | 47 | And I... I, Vurai, shall be the one to ascend\n |
| 0x2e73cd | 23 | victorious in this war! |
| 0x2e73e5 | 29 | Anju. You will bow before me. |
| 0x2e7403 | 43 | For that is the only path left for one as\n |
| 0x2e742f | 14 | feeble as you. |
| 0x2e743e | 45 | You shall become my puppet, and shall serve\n |
| 0x2e746c | 38 | as a sacrifice on my road to conquest. |
| 0x2e7493 | 18 | Nh... hh... hhh... |
| 0x2e74a6 | 19 | No... I will not... |
| 0x2e74ba | 32 | I... I do not wish for Yamato... |
| 0x2e74db | 31 | ...to become... such a place... |
| 0x2e74fb | 41 | Through the mental fog and hazy vision,\n |
| 0x2e7525 | 28 | Anju weakly shakes her head. |
| 0x2e7542 | 46 | Oh? Your pride as the imperial princess will\n |
| 0x2e7571 | 32 | not allow such submission, then? |
| 0x2e7592 | 45 | Very well. For that, you shall have my mercy. |
| 0x2e75c0 | 44 | Vurai tosses a single dagger at Anju's feet. |
| 0x2e75ed | 7 | Use it. |
| 0x2e75f5 | 44 | If you truly do not wish to live a life of\n |
| 0x2e7622 | 48 | shame, then end your life with your own hands.\n |
| 0x2e7653 | 4 | Now. |
| 0x2e7658 | 45 | Anju picks up the blade with shaking hands,\n |
| 0x2e7686 | 25 | and slowly unsheathes it. |
| 0x2e76a0 | 12 | Ah... hhh... |
| 0x2e76ad | 45 | The cold glint of the blade reflects in her\n |
| 0x2e76db | 11 | empty eyes. |
| 0x2e76e7 | 30 | N-No... I... do not wish to... |
| 0x2e7706 | 47 | Her whole body shivers as sweat trickles down\n |
| 0x2e7736 | 9 | her back. |
| 0x2e7740 | 28 | I do not... want to die...\n |
| 0x2e775d | 17 | I am so afraid... |
| 0x2e776f | 48 | She can hear a part of her crying out, but her\n |
| 0x2e77a0 | 46 | body refuses to obey, as if she is no longer\n |
| 0x2e77cf | 11 | in control. |
| 0x2e77db | 29 | Please... someone... help...! |
| 0x2e77f9 | 44 | The dagger held in her hands slowly inches\n |
| 0x2e7826 | 16 | toward her neck. |
| 0x2e7837 | 29 | Please save me... Father...\n |
| 0x2e7855 | 9 | Oshtor... |
| 0x2e785f | 49 | The blade's tip slips against her throat almost\n |
| 0x2e7891 | 46 | gently, a trickle of blood trailing down her\n |
| 0x2e78c0 | 10 | pale skin. |
| 0x2e78cb | 16 | Help me... Haku! |
| 0x2e78dc | 25 | Princess! You all right!? |
| 0x2e78f6 | 5 | Ah... |
| 0x2e78fc | 8 | Rrrgh... |
| 0x2e7905 | 30 | Vurai slowly turns to face us. |
| 0x2e7924 | 29 | Your Highness, are you hurt!? |
| 0x2e7942 | 41 | Looks like we made it just in time, yeah? |
| 0x2e796c | 43 | Despite our bursting in, Anju only stares\n |
| 0x2e7998 | 42 | blankly ahead, showing no sign of having\n |
| 0x2e79c3 | 13 | noticed us... |
| 0x2e79d1 | 41 | But looking closer, we can see her eyes\n |
| 0x2e79fb | 22 | welling up with tears. |
| 0x2e7a12 | 50 | In her hand she holds a dagger, pointed directly\n |
| 0x2e7a45 | 18 | at her own throat. |
| 0x2e7a58 | 18 | Nh... ah... hhh... |
| 0x2e7a6b | 6 | Anju-- |
| 0x2e7a72 | 34 | Shit, we barely made it in time... |
| 0x2e7a95 | 48 | And there's something wrong with the princess.\n |
| 0x2e7ac6 | 32 | We have to do something, quick-- |
| 0x2e7ae7 | 36 | What have you done to Her Highness!? |
| 0x2e7b0c | 7 | Soldier |
| 0x2e7b14 | 45 | Lord Vurai! What was that sound just... Huh!? |
| 0x2e7b45 | 41 | Intruders! How did you enter this place!? |
| 0x2e7b6f | 8 | SILENCE! |
| 0x2e7b78 | 7 | S-Sir!! |
| 0x2e7b80 | 40 | Vurai roars at the flustered soldiers,\n |
| 0x2e7ba9 | 30 | then fixes his gaze on Oshtor. |
| 0x2e7bc8 | 9 | ...Vurai. |
| 0x2e7bd2 | 34 | So you came after all... Oshtor.\n |
| 0x2e7bf5 | 44 | This is it. This is what I had hoped to see. |
| 0x2e7c22 | 48 | But what will you do now? However powerful you\n |
| 0x2e7c53 | 44 | may be, you can barely stand as you are now. |
| 0x2e7c80 | 34 | That will be none of your concern. |
| 0x2e7ca3 | 4 | Hrm? |
| 0x2e7ca8 | 42 | Sorry to disappoint, but your opponent's\n |
| 0x2e7cd3 | 10 | over here. |
| 0x2e7cde | 46 | Vurai's gaze flickers momentarily to me, but\n |
| 0x2e7d0d | 41 | his hard glare returns to Oshtor almost\n |
| 0x2e7d37 | 10 | instantly. |
| 0x2e7d42 | 36 | Even now, you still mock me, Oshtor? |
| 0x2e7d67 | 45 | Looks like he doesn't think we're worth his\n |
| 0x2e7d95 | 46 | time. I wasn't expecting him to take us this\n |
| 0x2e7dc4 | 8 | lightly. |
| 0x2e7dcd | 47 | Well, well, look at the big macho Akuruturuka\n |
| 0x2e7dfd | 48 | over here. He's so full of himself, it's kinda\n |
| 0x2e7e2e | 11 | refreshing. |
| 0x2e7e3a | 46 | Is that so...? You don't think we'll even be\n |
| 0x2e7e69 | 40 | a match, eh? Oh, that's just precious... |
| 0x2e7e92 | 7 | Rrgh... |
| 0x2e7e9a | 46 | You never change, Vurai. You take such pride\n |
| 0x2e7ec9 | 46 | in your might, and deem all without power to\n |
| 0x2e7ef8 | 13 | be worthless. |
| 0x2e7f06 | 47 | Rule is won through strength. Our liege ruled\n |
| 0x2e7f36 | 49 | this land of Yamato with absolute and ineffable\n |
| 0x2e7f68 | 6 | power. |
| 0x2e7f6f | 41 | I do not deny it. Yet regardless of his\n |
| 0x2e7f99 | 44 | strength, our liege never looked down upon\n |
| 0x2e7fc6 | 7 | others. |
| 0x2e7fce | 45 | By all means, test if this is mere mockery.\n |
| 0x2e7ffc | 44 | Or do you fear you will taste defeat for a\n |
| 0x2e8029 | 12 | second time? |
| 0x2e8036 | 10 | You dare-- |
| 0x2e8041 | 7 | Ahah... |
| 0x2e8049 | 47 | Indeed... Maybe that is why you lost to Oshtor. |
| 0x2e8079 | 5 | *Crk* |
| 0x2e807f | 49 | Something snaps at her words. A deadly pressure\n |
| 0x2e80b1 | 47 | falls over us, like Vurai holds our hearts in\n |
| 0x2e80e1 | 18 | his clenched fist. |
| 0x2e80f4 | 7 | Nngh... |
| 0x2e80fc | 35 | ...Woman. Do you mean to insult me? |
| 0x2e8120 | 6 | Eep... |
| 0x2e8127 | 45 | Hm? I was just commenting that perhaps that\n |
| 0x2e8155 | 16 | is why you lost. |
| 0x2e8166 | 51 | Strong or not, you will fail if you underestimate\n |
| 0x2e819a | 46 | your opponent. It seems only natural that he\n |
| 0x2e81c9 | 22 | would win against you. |
| 0x2e81e0 | 46 | I will say only this: You will never be able\n |
| 0x2e820f | 23 | to defeat Oshtor. Ever. |
| 0x2e8227 | 23 | Or us, for that matter. |
| 0x2e823f | 50 | ...Such audacity... You run your mouth overmuch,\n |
| 0x2e8272 | 6 | woman. |
| 0x2e8279 | 6 | Wh--!? |
| 0x2e8280 | 21 | Aha... Hee hee hee... |
| 0x2e8296 | 50 | Oh, come on... Sure, the plan was to provoke him\n |
| 0x2e82c9 | 48 | so he goes all out, but you might be overdoing\n |
| 0x2e82fa | 8 | it here! |
| 0x2e8303 | 17 | Insolent child... |
| 0x2e8315 | 47 | Vurai mutters quietly, then takes a slow step\n |
| 0x2e8345 | 8 | forward. |
| 0x2e834e | 4 | mask |
| 0x2e8354 | 42 | Very well. Then prove to me... your worth! |
| 0x2e837f | 7 | Haku... |
| 0x2e8387 | 13 | Yeah, I know. |
| 0x2e8395 | 44 | We have to make him activate his Akuruka's\n |
| 0x2e83c2 | 45 | power, so we have a chance to finish him off. |
| 0x2e83f0 | 24 | Stay back now, Shinonon. |
| 0x2e8409 | 28 | What're you talkin' about?\n |
| 0x2e8426 | 18 | I wanna fight too! |
| 0x2e8439 | 46 | Thank you, Shinonon. But we need you to stay\n |
| 0x2e8468 | 42 | with the nice lady and Oshtor so you can\n |
| 0x2e8493 | 13 | protect them. |
| 0x2e84a1 | 27 | You want me to protect Osh? |
| 0x2e84bd | 28 | Mhm. Can you do that for us? |
| 0x2e84da | 38 | Hokay, got it. You can leave it to me! |
| 0x2e8501 | 33 | That's my girl. Thanks, bosslady. |
| 0x2e8523 | 29 | You need to stay back, too.\n |
| 0x2e8541 | 31 | Look after Shinonon and Oshtor. |
| 0x2e8561 | 15 | Lady-in-waiting |
| 0x2e8571 | 46 | U-Understood. And... I wish you all the best\n |
| 0x2e85a0 | 8 | of luck. |
| 0x2e85a9 | 48 | Jachdwalt, Ougi, I want you guys needling him.\n |
| 0x2e85da | 26 | Keep his attention on you! |
| 0x2e85f5 | 48 | Very well. I must say, though, I never dreamed\n |
| 0x2e8626 | 41 | I'd find myself in the thick of such an\n |
| 0x2e8650 | 14 | insane scheme. |
| 0x2e865f | 45 | Got that right. I thought I was used to the\n |
| 0x2e868d | 47 | boss's crazy orders, and now we're up against\n |
| 0x2e86bd | 16 | Vurai himself... |
| 0x2e86ce | 33 | Doesn't get any better than this. |
| 0x2e86f0 | 45 | Nosuri, Kiwru, I want you on crowd control.\n |
| 0x2e871e | 23 | Keep his backup at bay. |
| 0x2e8736 | 13 | U-Understood! |
| 0x2e8744 | 48 | You dare hurt Her Highness... Vurai, you are a\n |
| 0x2e8775 | 47 | villain, unfit for your title. I will deliver\n |
| 0x2e87a5 | 15 | your judgement. |
| 0x2e87b5 | 49 | I... will not falter. I am my sworn brother's--\n |
| 0x2e87e7 | 40 | no... the Imperial Guard of the Right,\n |
| 0x2e8810 | 15 | Oshtor's sword! |
| 0x2e8820 | 47 | Nekone, Rulutieh, get the princess as soon as\n |
| 0x2e8850 | 45 | you see an opening. We need to get her away\n |
| 0x2e887e | 11 | from Vurai. |
| 0x2e888a | 45 | I need no reminding. Make sure you keep his\n |
| 0x2e88b8 | 10 | attention. |
| 0x2e88e8 | 41 | Miss Anju... I promise I will save you,\n |
| 0x2e8912 | 41 | no matter what, so please wait a little\n |
| 0x2e893c | 9 | longer... |
| 0x2e8946 | 36 | Atuy... just do whatever you want.\n |
| 0x2e896b | 35 | I'm not gonna stop you this time.\n |
| 0x2e898f | 8 | Go nuts. |
| 0x2e8998 | 34 | Hee hee hee... music to my ears.\n |
| 0x2e89bb | 22 | You're the BEST, love! |
| 0x2e89d2 | 49 | ...We can't afford to hold back. I promise I'll\n |
| 0x2e8a04 | 47 | do anything you two want me to later. Uruuru,\n |
| 0x2e8a34 | 33 | Saraana... we're counting on you. |
| 0x2e8a56 | 33 | We obey your call without fail.\n |
| 0x2e8a78 | 32 | We offer our all to you, Master. |
| 0x2e8a99 | 44 | I expected their usual schtick when I said\n |
| 0x2e8ac6 | 46 | I'd do anything... The strain must be really\n |
| 0x2e8af5 | 8 | serious. |
| 0x2e8afe | 8 | ...Kuon. |
| 0x2e8b07 | 39 | Don't worry. I've got everyone's backs. |
| 0x2e8b2f | 42 | You just concentrate on the tactics, Haku. |
| 0x2e8b5a | 28 | Thanks... I'll do just that. |
| 0x2e8b77 | 26 | Everyone... Let's do this! |
| 0x2e8b92 | 40 | Show me the power... of the Akuruturuka. |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_08.json` com a forma:
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
