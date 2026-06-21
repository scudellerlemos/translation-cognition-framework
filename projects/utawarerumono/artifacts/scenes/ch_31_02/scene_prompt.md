# Cena ch_31_02 — pacote de traducao (275 linhas)

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
| aperyu | Item | aperyu | manter_original | none |
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
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
- `Sir!` -> `Sim!` (Maroro, 12_09)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `ground.` -> `do chão.` (Man, 11_01)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `nearby.` -> `perto.` (Ukon, 12_15)
- `What... is that...?` -> `O que... é aquilo...?` (Haku, 14_09)
- `shoulder.` -> `ombro.` (Haku, 17_01)
- `Ngh...` -> `Ngh...` (Haku, 11_01)
- `might.` -> `talvez.` (Ukon, 23_02)
- `Impossible...` -> `Impossível...` (Kuon, 22_05)
- `Wait...` -> `Espera...` (Haku, 21_05)
- `his way.` -> `seu caminho.` (Narrator, 20_20)
- `him.` -> `dele.` (Nekone, 15_02)
- `Man` -> `Hom` (Sistema, 11_01)
- `her.` -> `a ela.` (Kuon, 11_02)
- `Girl` -> `Garota` (sistema, 11_01)
- `But...` -> `mas...` (Kuon, 11_01)
- `I see...` -> `Entendo...` (Haku, 11_02)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `Haku...` -> `Haku...` (Kuon, 11_02)
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
| 0x31aac3 | 45 | Countless shadows dart and leap through the\n |
| 0x31aaf1 | 9 | darkness. |
| 0x31aafb | 48 | They are clothed entirely in black, even their\n |
| 0x31ab2c | 13 | faces hidden. |
| 0x31ab3a | 47 | They traverse the mountainous path with ease,\n |
| 0x31ab6a | 44 | like a dark wind sweeping through the trees. |
| 0x31ab97 | 34 | As one, the shadows suddenly stop. |
| 0x31abbe | 24 | And before their gazes-- |
| 0x31abd7 | 45 | A girl walking alone over the dark mountain\n |
| 0x31ac05 | 38 | path. Her steps are weak and unsteady. |
| 0x31ac2c | 50 | The shadow in front signals with raised fingers,\n |
| 0x31ac5f | 46 | and the others scatter, melting into the dark. |
| 0x31ac8e | 50 | The girl's eyes are clouded, staring forward and\n |
| 0x31acc1 | 15 | seeing nothing. |
| 0x31acd1 | 50 | She continues on, her steps shaky and faltering,\n |
| 0x31ad04 | 25 | stumbling along the path. |
| 0x31ad1e | 49 | And in the darkness, one of the shadows signals\n |
| 0x31ad50 | 47 | the others with a quick downward swing of his\n |
| 0x31ad80 | 4 | arm. |
| 0x31ad85 | 50 | Instantly, ropes fly from the trees on all sides\n |
| 0x31adb8 | 39 | of the girl, binding and ensnaring her. |
| 0x31ade0 | 45 | A number of them bolt out and jump upon the\n |
| 0x31ae0e | 40 | girl, slamming her into the ground and\n |
| 0x31ae37 | 16 | restraining her. |
| 0x31ae48 | 48 | Their apparent leader takes out a drawing, and\n |
| 0x31ae79 | 45 | compares her face with the portrait, nodding. |
| 0x31aea7 | 6 | Shadow |
| 0x31aeae | 39 | It's her. One of Oshtor's subordinates. |
| 0x31aed6 | 47 | So we were right. It seems he has fled to his\n |
| 0x31af06 | 22 | homeland of Ennakamuy. |
| 0x31af1d | 44 | He shouldn't have had enough time to ready\n |
| 0x31af4a | 20 | himself for war yet. |
| 0x31af5f | 43 | We will seize the advantage and strike now. |
| 0x31af8b | 6 | Others |
| 0x31af92 | 4 | Sir! |
| 0x31af97 | 46 | Take the woman away. If she tries to escape,\n |
| 0x31afc6 | 9 | kill her. |
| 0x31afd0 | 48 | The other shadows follow the man's orders, and\n |
| 0x31b001 | 24 | lift up the fallen girl. |
| 0x31b01a | 6 | ...Hm? |
| 0x31b021 | 46 | The faint scent of something burning reaches\n |
| 0x31b050 | 9 | his nose. |
| 0x31b05a | 49 | And he notices a crackling sound on the edge of\n |
| 0x31b08c | 39 | hearing, as though something is aflame. |
| 0x31b0b4 | 45 | The other shadows gradually notice as well,\n |
| 0x31b0e2 | 47 | glancing around... and the girl's body erupts\n |
| 0x31b112 | 11 | in a blaze. |
| 0x31b11e | 25 | GAAAAAAAAAAAAAHHHHHHHHH!! |
| 0x31b138 | 45 | Those engulfed quickly catch fire, becoming\n |
| 0x31b166 | 48 | balls of flame as they fling themselves to the\n |
| 0x31b197 | 7 | ground. |
| 0x31b19f | 45 | Even those not directly caught in the blast\n |
| 0x31b1cd | 26 | burst into searing flames. |
| 0x31b1e8 | 8 | What--!? |
| 0x31b1f1 | 47 | Their look of shock quickly turns into one of\n |
| 0x31b221 | 5 | fear. |
| 0x31b227 | 48 | No matter how much they try to put it out, the\n |
| 0x31b258 | 44 | fire burns hungrily, spreading and growing\n |
| 0x31b285 | 9 | stronger. |
| 0x31b28f | 36 | Ah... Ah... Ahh... Aaaaaaaaaahhhhh!! |
| 0x31b2b4 | 48 | They roll on the ground, thrashing as they try\n |
| 0x31b2e5 | 49 | to put out the flames. Their flailing is almost\n |
| 0x31b317 | 8 | comical. |
| 0x31b320 | 25 | But there is no laughter. |
| 0x31b33a | 45 | Please... Put it out! PUT IT OUT!! PLEASE!!\n |
| 0x31b368 | 25 | Agghh... AAAAAAAAARRRGH!! |
| 0x31b382 | 49 | They scream, and beg, and plead, like terrified\n |
| 0x31b3b4 | 9 | children. |
| 0x31b3be | 41 | But none of the others come to their aid. |
| 0x31b3e8 | 47 | They know that if the fire reaches them, they\n |
| 0x31b418 | 38 | would only share their comrades' fate. |
| 0x31b43f | 10 | GHAAAAGH!! |
| 0x31b44a | 44 | And after several seconds of screaming and\n |
| 0x31b477 | 46 | writhing, wreathed in flame... he falls still. |
| 0x31b4a6 | 47 | After a short silence, the one to break it is\n |
| 0x31b4d6 | 43 | the girl in the center of the deadly blaze. |
| 0x31b502 | 49 | She should have been reduced to ashes, like all\n |
| 0x31b534 | 33 | the rest... yet there she stands. |
| 0x31b556 | 7 | Wha--!? |
| 0x31b55e | 38 | The shadows stare, paralyzed by shock. |
| 0x31b585 | 49 | Her clothes have been consumed by fire, yet her\n |
| 0x31b5b7 | 45 | bare skin is unmarked, not a single burn on\n |
| 0x31b5e5 | 9 | her body. |
| 0x31b5ef | 48 | However, they have little time to recover from\n |
| 0x31b620 | 11 | this shock. |
| 0x31b62c | 18 | A cold wind blows. |
| 0x31b63f | 45 | A freezing wind, like a sudden blizzard has\n |
| 0x31b66d | 47 | blown in... even with the fires still roaring\n |
| 0x31b69d | 7 | nearby. |
| 0x31b6a5 | 25 | *Crack... crack... crack* |
| 0x31b6bf | 42 | A sharp, crystalline sound. The sound of\n |
| 0x31b6ea | 46 | something fracturing, in a deep spiderweb of\n |
| 0x31b719 | 7 | cracks. |
| 0x31b721 | 48 | A creeping cloud of frost mists forth from the\n |
| 0x31b752 | 40 | girl, and begins to swallow up the area. |
| 0x31b77b | 45 | The shadows quickly jump back, but some are\n |
| 0x31b7a9 | 31 | unable to react quickly enough. |
| 0x31b7c9 | 47 | When the mist finally fades, it reveals them.\n |
| 0x31b7f9 | 47 | Frozen like statues. Faces locked in timeless\n |
| 0x31b829 | 6 | agony. |
| 0x31b830 | 47 | Little by little, they tilt over, and shatter\n |
| 0x31b860 | 43 | into brittle shards as they hit the ground. |
| 0x31b88c | 19 | What... is that...? |
| 0x31b8a0 | 39 | One of the shadows mutters, dumbstruck. |
| 0x31b8c8 | 36 | These shadows are lucky, in a way.\n |
| 0x31b8ed | 48 | Thanks to those words, they are able to regain\n |
| 0x31b91e | 13 | their senses. |
| 0x31b92c | 30 | K-Kill it! Kill that monster!! |
| 0x31b94b | 47 | The shadows lunge at the girl as one, surging\n |
| 0x31b97b | 21 | forward at the order. |
| 0x31b991 | 49 | Lucky, perhaps. However, they have chosen poorly. |
| 0x31b9c3 | 32 | The correct choice was to run.\n |
| 0x31b9e4 | 28 | Run, and never stop running. |
| 0x31ba01 | 45 | The blade in the shadow's hand flies to the\n |
| 0x31ba2f | 36 | girl's throat as the shadow lunges-- |
| 0x31ba54 | 37 | But the blade never reaches its mark. |
| 0x31ba7a | 51 | The blade crumbles away... and the arm bearing it\n |
| 0x31baae | 48 | rots, decaying fast, until it falls off at the\n |
| 0x31badf | 9 | shoulder. |
| 0x31bae9 | 33 | It{W15} was{W20} you{W25}...{W15} |
| 0x31bb0b | 47 | A booming voice resounds through the minds of\n |
| 0x31bb3b | 44 | all present, like it's echoing through the\n |
| 0x31bb68 | 12 | very ground. |
| 0x31bb75 | 6 | Ngh... |
| 0x31bb7c | 50 | The shadows are well trained. The loss of a limb\n |
| 0x31bbaf | 45 | would ordinarily not be enough to deter them. |
| 0x31bbdd | 49 | But the moment they hear the voice, a dark fear\n |
| 0x31bc0f | 49 | and despair grips them. Their trained minds are\n |
| 0x31bc41 | 10 | shattered. |
| 0x31bc4c | 6 | Run... |
| 0x31bc53 | 35 | Their instincts scream within them. |
| 0x31bc77 | 32 | This thing cannot be a person... |
| 0x31bc98 | 47 | They finally realize it. Before them stands a\n |
| 0x31bcc8 | 43 | demon that brings calamity upon this world. |
| 0x31bcf4 | 34 | A force that no person can oppose. |
| 0x31bd17 | 13 | Nugwisomkami. |
| 0x31bd25 | 47 | He tries to leap back, but loses his balance.\n |
| 0x31bd55 | 36 | He hits the ground with a wet splat. |
| 0x31bd7a | 47 | He cannot run. His legs have already begun to\n |
| 0x31bdaa | 42 | rot away, and he can no longer even stand. |
| 0x31bdd5 | 11 | H...Help... |
| 0x31bde1 | 46 | Managing only that, he rots away in seconds,\n |
| 0x31be10 | 47 | leaving remains that only barely resemble the\n |
| 0x31be40 | 7 | living. |
| 0x31be48 | 6 | AAGH-- |
| 0x31be4f | 47 | Another shadow screams at the sight and turns\n |
| 0x31be7f | 46 | to run, but his body abruptly begins to swell. |
| 0x31beae | 13 | It was you... |
| 0x31bebc | 12 | HhhYYAAAGH-- |
| 0x31bec9 | 47 | His own scream is cut off by the sound of his\n |
| 0x31bef9 | 43 | body bursting into chunks of lifeless meat. |
| 0x31bf25 | 24 | AAAAAAAAAAAAAAHHHHHHHH!! |
| 0x31bf3e | 20 | Run... Run... Run... |
| 0x31bf53 | 43 | The remaining shadows scatter like spider\n |
| 0x31bf7f | 46 | hatchlings, scrambling to run with all their\n |
| 0x31bfae | 6 | might. |
| 0x31bfb5 | 47 | The girl stretches her arm blankly toward the\n |
| 0x31bfe5 | 40 | running shadows, eyes devoid of emotion. |
| 0x31c00e | 44 | And then she flicks the air with her finger. |
| 0x31c03b | 47 | Somewhere nearby, there is the sound of flesh\n |
| 0x31c06b | 22 | being audibly pierced. |
| 0x31c082 | 51 | And in the same moment, one of the shadows halts;\n |
| 0x31c0b6 | 43 | their torso gone. Their lower half slowly\n |
| 0x31c0e2 | 23 | crumples to the ground. |
| 0x31c0fa | 43 | The sound echoes through the trees again.\n |
| 0x31c126 | 49 | And again. And each time, another body is blown\n |
| 0x31c158 | 11 | to viscera. |
| 0x31c164 | 48 | Explosions of flesh and blood paint the ground\n |
| 0x31c195 | 22 | in rich swaths of red. |
| 0x31c1ac | 16 | Run, run, run... |
| 0x31c1bd | 41 | The group's leader leaves the rest as a\n |
| 0x31c1e7 | 47 | distraction, and desperately runs for his life. |
| 0x31c217 | 43 | But he doesn't realize that he is running\n |
| 0x31c243 | 28 | through a maze with no exit. |
| 0x31c260 | 18 | What was that...!? |
| 0x31c273 | 33 | What the fuck WAS that woman...!? |
| 0x31c295 | 38 | How could we be defeated so easily...? |
| 0x31c2bc | 13 | Impossible... |
| 0x31c2ca | 41 | Impossible... impossible... impossible... |
| 0x31c2f4 | 7 | Wait... |
| 0x31c2fc | 23 | Could that woman be...? |
| 0x31c314 | 37 | I must report this... immediately...! |
| 0x31c33a | 13 | That woman... |
| 0x31c348 | 17 | She has to be a-- |
| 0x31c35a | 24 | She has to be a... what? |
| 0x31c373 | 7 | Ngaah!? |
| 0x31c37b | 21 | A voice from nowhere. |
| 0x31c391 | 46 | Before he even realizes it, a small woman is\n |
| 0x31c3c0 | 46 | looking down at him, sitting atop a mound in\n |
| 0x31c3ef | 9 | his path. |
| 0x31c3f9 | 40 | That girl is our precious little sister. |
| 0x31c422 | 26 | A very cute little sister. |
| 0x31c43d | 18 | That's all she is. |
| 0x31c450 | 47 | The shadow thinks quickly. He has no idea who\n |
| 0x31c480 | 49 | this woman is, but she seems intent on blocking\n |
| 0x31c4b2 | 8 | his way. |
| 0x31c4bb | 7 | Fool... |
| 0x31c4c3 | 48 | He can tell at a glance. Whatever this woman's\n |
| 0x31c4f4 | 50 | ability, she doesn't have the strength to oppose\n |
| 0x31c527 | 4 | him. |
| 0x31c52c | 44 | A foolish act. She has given herself away,\n |
| 0x31c559 | 18 | just to be killed. |
| 0x31c56c | 47 | But no mercy will be shown to those who stand\n |
| 0x31c59c | 26 | in the way of the shadows. |
| 0x31c5b7 | 23 | She will be eliminated. |
| 0x31c5cf | 18 | ...You poor thing. |
| 0x31c5e2 | 39 | You thought you escaped with your life. |
| 0x31c60a | 26 | What is she talking about? |
| 0x31c625 | 18 | But it's too late. |
| 0x31c638 | 26 | You were being mean to Ku. |
| 0x31c656 | 45 | After the awful din subsides... the area is\n |
| 0x31c684 | 31 | once again shrouded in silence. |
| 0x31c6a4 | 46 | The girl walks forward again, feet shaky and\n |
| 0x31c6d3 | 39 | weak, as though nothing had transpired. |
| 0x31c6fb | 50 | But the moonlight reveals three figures standing\n |
| 0x31c72e | 35 | in her path, as if waiting for her. |
| 0x31c752 | 42 | Two of them--apparently twin boys--kneel\n |
| 0x31c77d | 46 | respectfully before her, offering up a white\n |
| 0x31c7ac | 7 | aperyu. |
| 0x31c7b4 | 47 | The girl only continues blindly on, as if she\n |
| 0x31c7e4 | 21 | has not noticed them. |
| 0x31c7fa | 3 | Man |
| 0x31c7fe | 47 | The man with the sharp eyes takes off his own\n |
| 0x31c82e | 47 | aperyu, and drapes it over her as he embraces\n |
| 0x31c85e | 4 | her. |
| 0x31c863 | 42 | The smell of scorched flesh fills the air. |
| 0x31c88e | 45 | The fire that consumed the shadows flickers\n |
| 0x31c8bc | 48 | across the man's body, along with a frigid wind. |
| 0x31c8ed | 49 | The man's skin burns and crackles with heat and\n |
| 0x31c91f | 7 | frost-- |
| 0x31c927 | 47 | Yet he refuses to let go. He holds her close,\n |
| 0x31c957 | 18 | in a warm embrace. |
| 0x31c96a | 50 | He holds her as though to comfort a small child,\n |
| 0x31c99d | 43 | patting her back gently and reassuringly... |
| 0x31c9c9 | 4 | Girl |
| 0x31c9ce | 21 | Father... it hurts... |
| 0x31c9e4 | 36 | It feels like... I cannot breathe... |
| 0x31ca09 | 45 | I know that... it's something that can't be\n |
| 0x31ca37 | 9 | helped... |
| 0x31ca41 | 48 | I know some people never make it back from the\n |
| 0x31ca72 | 45 | battlefield... I know that's a part of war... |
| 0x31caa0 | 6 | But... |
| 0x31caa7 | 27 | But... I just don't know... |
| 0x31cac3 | 50 | It feels like my heart is about to split open...\n |
| 0x31caf6 | 34 | I don't know what to do anymore... |
| 0x31cb19 | 31 | I... don't know what this is... |
| 0x31cb39 | 47 | I've... never felt anything like this before... |
| 0x31cb69 | 37 | He was just... a lazy bum at first... |
| 0x31cb8f | 47 | I thought he'd never survive if I didn't look\n |
| 0x31cbbf | 45 | after him... He was just a hopeless person... |
| 0x31cbed | 39 | But... as I spent more time with him... |
| 0x31cc15 | 38 | It was just so fun... so reassuring... |
| 0x31cc3c | 20 | I felt so at ease... |
| 0x31cc51 | 25 | But... It's so painful... |
| 0x31cc6b | 34 | It hurts... It hurts... so much... |
| 0x31cc8e | 8 | I see... |
| 0x31cc97 | 23 | You... loved him, Kuon. |
| 0x31ccaf | 14 | I... loved...? |
| 0x31ccbe | 18 | Yes, that is it... |
| 0x31ccd1 | 24 | That feeling... is love. |
| 0x31ccea | 30 | A love like your mother's...\n |
| 0x31cd09 | 21 | Sweet, yet painful... |
| 0x31cd1f | 42 | A love that never had a chance to bloom... |
| 0x31cd4a | 5 | Oh... |
| 0x31cd50 | 15 | I... see now... |
| 0x31cd60 | 20 | So... that was it... |
| 0x31cd75 | 21 | I... loved... Haku... |
| 0x31cd8b | 17 | Why... Why did... |
| 0x31cd9d | 30 | Why didn't... I realize it...? |
| 0x31cdbc | 38 | If... only I had... a little sooner... |
| 0x31cde3 | 7 | Haku... |
| 0x31cdeb | 15 | Haku... Haku... |
| 0x31cdfb | 10 | ...Haku... |
| 0x31ce06 | 19 | ...Let's go home.\n |
| 0x31ce1a | 27 | Everyone's waiting for you. |

## 8. Formato de saida EXIGIDO
Escreva `translations_31_02.json` com a forma:
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
