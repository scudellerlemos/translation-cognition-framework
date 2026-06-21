# Cena ch_20_21 — pacote de traducao (260 linhas)

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
| Entua | Personagem | Entua | manter_original | major |
| Girl | UI | Garota | traduzir | none |
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Haku | Personagem | Haku | manter_original | moderate |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| sainaina | Item | sainaina | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Woman | UI | Mulher | traduzir | none |
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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `No...` -> `Não...` (Touka, 17_01)
- `Nugwisomkami...` -> `Nugwisomkami...` (Ukon, 15_07)
- `you...?` -> `você...?` (Kuon, 14_09)
- `Yamatan Soldier` -> `Soldado de Yamato` (SYSTEM, 12_10)
- `women.` -> `mulheres.` (Haku, 18_01)
- `mean.` -> `quer.` (Ukon, 12_06)
- `complaining.` -> `reclamando.` (Haku, 18_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `to me.` -> `a mim.` (Narrador, 12_11)
- `Ah!?` -> `Ah!?` (Rulutieh, 14_04)
- `fine.` -> `Tá.` (Haku, 16_01)
- `out.` -> `fora.` (Atuy, 17_01)
- `as well.` -> `também.` (Haku, 17_01)
- `Right?` -> `né?` (Haku, 11_01)
- `I...` -> `Eu...` (Nekone, 14_04)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
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
| 0x212744 | 9 | Father... |
| 0x21274e | 28 | Please, father, answer me.\n |
| 0x21276b | 15 | Ungh... nngh... |
| 0x21277b | 35 | Father... Oh... This is so cruel... |
| 0x21279f | 8 | Entua... |
| 0x2127a8 | 42 | The commander's shaking hands find those\n |
| 0x2127d3 | 24 | of his beloved daughter. |
| 0x2127ec | 34 | I am so glad to see you alive...\n |
| 0x21280f | 29 | You are not hurt anywhere...? |
| 0x21282d | 47 | I-I am fine. But we need to hurry and tend to\n |
| 0x21285d | 14 | your wounds... |
| 0x21286c | 27 | Do not... worry about me... |
| 0x212888 | 5 | No... |
| 0x21288e | 46 | How pitiful... To think that... I would have\n |
| 0x2128bd | 24 | lost so easily to him... |
| 0x2128d6 | 50 | I had... no idea... Yamato held this much power... |
| 0x212909 | 36 | "Never incur the wrath of Yamato."\n |
| 0x21292e | 45 | "One must never awaken the Akuruturuka from\n |
| 0x21295c | 17 | their slumber"... |
| 0x21296e | 42 | It seems... our ancestors... spoke true... |
| 0x212999 | 48 | They were... no longer mere mortal soldiers...\n |
| 0x2129ca | 41 | That was... power from the age of gods... |
| 0x2129f4 | 45 | Lord Gundhurua may be a great man... but...\n |
| 0x212a22 | 29 | his opponent was too great... |
| 0x212a40 | 39 | No man can... be victorious over a...\n |
| 0x212a68 | 15 | Nugwisomkami... |
| 0x212a78 | 45 | Beyond the boulder ahead is a small cave...\n |
| 0x212aa6 | 45 | Do you know where it is? We used it to hide\n |
| 0x212ad4 | 15 | our supplies... |
| 0x212ae4 | 30 | As long as you hide there...\n |
| 0x212b03 | 25 | You shouldn't be found... |
| 0x212b1d | 44 | Lay low there, until things begin to calm... |
| 0x212b4a | 38 | Then you will come with me, Father...! |
| 0x212b71 | 49 | Haha... Leave me here... With this wound, there\n |
| 0x212ba3 | 27 | is... no way I will live... |
| 0x212bbf | 12 | No... No...! |
| 0x212bcc | 29 | It's my body, is it not...?\n |
| 0x212bea | 39 | I know its limits better than anyone... |
| 0x212c12 | 36 | That man... The man in the mask...\n |
| 0x212c37 | 42 | He will pay for what he has done to you... |
| 0x212c62 | 47 | Leave him be. I forbid you to seek vengeance... |
| 0x212c92 | 9 | ...Wh--!? |
| 0x212c9c | 47 | Hah... Now that I recall, you enjoyed weaving\n |
| 0x212ccc | 44 | and cooking much more than warfare, didn't\n |
| 0x212cf9 | 7 | you...? |
| 0x212d01 | 46 | That's right... You... never belonged on the\n |
| 0x212d30 | 14 | battlefield... |
| 0x212d3f | 17 | That is not true! |
| 0x212d51 | 45 | I am your daughter! The daughter of a brave\n |
| 0x212d7f | 18 | Uzurushan warrior! |
| 0x212d92 | 17 | That is enough... |
| 0x212da4 | 45 | You may live your life as your own woman...\n |
| 0x212dd2 | 30 | and find your own happiness... |
| 0x212df1 | 45 | Haha... I suppose my only regret... is that\n |
| 0x212e1f | 41 | I will never see you in your... bridal... |
| 0x212e49 | 7 | Father? |
| 0x212e51 | 48 | ...F-Father...? No... This can't be happening.\n |
| 0x212e82 | 47 | Father, please... Don't leave me... Father...\n |
| 0x212eb2 | 7 | Father! |
| 0x212eba | 49 | The girl desperately clutches the lifeless body\n |
| 0x212eec | 40 | of her father, her tears flowing freely. |
| 0x212f15 | 15 | Yamatan soldier |
| 0x212f25 | 47 | Hey! I think I heard someone's voice over here! |
| 0x212f55 | 44 | Still survivors, huh...? I'll put them down! |
| 0x212f85 | 24 | Father... forgive me...! |
| 0x212f9e | 30 | I found something! Over there! |
| 0x212fbd | 26 | What...? It's just a body. |
| 0x212fd8 | 33 | No, I'm sure I heard a voice...\n |
| 0x212ffa | 16 | Search the area! |
| 0x21300b | 43 | Fine! Dammit. If we'd gone to the village\n |
| 0x213037 | 44 | instead, there would've at least been some\n |
| 0x213064 | 6 | women. |
| 0x21306b | 43 | Quit your complaining! If there's a body,\n |
| 0x213097 | 42 | there might be more of them around here!\n |
| 0x2130c2 | 16 | Start searching! |
| 0x2130d3 | 42 | And so Yamato continues to hunt down the\n |
| 0x2130fe | 31 | remnants of the Uzurushan army. |
| 0x21311e | 15 | Hahh... Phew... |
| 0x21312e | 34 | A-At this rate, they'll find me... |
| 0x213151 | 49 | Haku and Jachdwalt, can you search around these\n |
| 0x213183 | 9 | boulders? |
| 0x21318d | 11 | Sure thing. |
| 0x213199 | 26 | Just leave it to us, yeah? |
| 0x2131b4 | 49 | I hold up my torch and step into the dark areas\n |
| 0x2131e6 | 21 | between the boulders. |
| 0x2131fc | 47 | And here I thought I'd finally get to go back\n |
| 0x21322c | 40 | home. Why're we stuck hunting down the\n |
| 0x213255 | 14 | stragglers...? |
| 0x213264 | 45 | Can't really be helped, but I know what you\n |
| 0x213292 | 5 | mean. |
| 0x213298 | 44 | But we can't just leave soldiers behind if\n |
| 0x2132c5 | 37 | they're gonna keep fighting even now. |
| 0x2132eb | 50 | Gotta have 'em at least seem like they're sorry,\n |
| 0x21331e | 48 | otherwise it'll mean trouble for the civilians\n |
| 0x21334f | 19 | and innocent folks. |
| 0x213363 | 23 | I guess you're right... |
| 0x21337b | 48 | I pause, watching the face of the man who went\n |
| 0x2133ac | 42 | from trying to kill me to laughing at my\n |
| 0x2133d7 | 12 | complaining. |
| 0x2133e4 | 36 | So why exactly are you still here?\n |
| 0x213409 | 46 | The war's over. You don't have to stay, right? |
| 0x213438 | 23 | Ah, yeah. About that... |
| 0x213450 | 44 | Jachdwalt scratches his head, then answers\n |
| 0x21347d | 13 | nonchalantly. |
| 0x21348b | 43 | I've decided to stick with you folks, boss. |
| 0x2134b7 | 4 | Huh? |
| 0x2134bc | 45 | I'm no prisoner anymore, but my homeland is\n |
| 0x2134ea | 14 | long gone now. |
| 0x2134f9 | 47 | 'Course, there are those folks who want to go\n |
| 0x213529 | 45 | back and rebuild, but that ain't my business. |
| 0x213557 | 47 | And while I was mulling it over, the bosslady\n |
| 0x213587 | 23 | invited me to join you. |
| 0x21359f | 44 | Solid roof over my head, hot meals, plus a\n |
| 0x2135cc | 45 | little extra cash... I dunno. Sounds like a\n |
| 0x2135fa | 23 | pretty nice deal to me. |
| 0x213612 | 45 | Plus, Shinonon's taken a shine to all those\n |
| 0x213640 | 12 | other girls. |
| 0x21364d | 45 | Not to mention I still owe you bigtime, boss. |
| 0x21367f | 50 | So anyways, it'll be a pleasure workin' with you\n |
| 0x2136b2 | 18 | from now on, boss. |
| 0x2136c5 | 47 | W-Well, I guess if you're OK with it, I don't\n |
| 0x2136f5 | 24 | really have a problem... |
| 0x21370e | 48 | Jachdwalt's got real fighting skills. I'm sure\n |
| 0x21373f | 37 | Kuon was pretty eager to rope him in. |
| 0x213765 | 48 | Well, we might as well look like we're getting\n |
| 0x213796 | 23 | some work done, anyway. |
| 0x2137ae | 37 | After saying that, I look around...\n |
| 0x2137d4 | 41 | and I suddenly feel like something's off. |
| 0x2137fe | 6 | Hm...? |
| 0x213805 | 19 | Something up, boss? |
| 0x213819 | 11 | Is this...? |
| 0x213825 | 50 | I walk closer to the boulder that's standing out\n |
| 0x213858 | 6 | to me. |
| 0x21385f | 8 | Knew it. |
| 0x213868 | 50 | The surrounding boulders and grass cast shadows,\n |
| 0x21389b | 48 | so it's hard to see, but from here I can see a\n |
| 0x2138cc | 5 | cave. |
| 0x2138d2 | 34 | This'd make a perfect hiding spot. |
| 0x2138f5 | 46 | I cautiously look into the hole, as though I\n |
| 0x213924 | 35 | just accidentally stumbled past it. |
| 0x213948 | 14 | ...Well, shit. |
| 0x213957 | 46 | I was hoping they wouldn't fight to the last\n |
| 0x213986 | 46 | person. It'd make negotiations a lot easier... |
| 0x2139b5 | 41 | I lock gazes with a girl glaring at me,\n |
| 0x2139df | 16 | her sword drawn. |
| 0x2139f0 | 48 | Her face is covered in mud, but her eyes still\n |
| 0x213a21 | 15 | glint brightly. |
| 0x213a31 | 23 | Just my goddamn luck... |
| 0x213a49 | 26 | What's the matter, Boss?\n |
| 0x213a64 | 17 | You find someth-- |
| 0x213a76 | 10 | You two... |
| 0x213a81 | 8 | You're-- |
| 0x213a8a | 29 | Why don't we talk this out?\n |
| 0x213aa8 | 38 | I'm sure we can settle this nice and-- |
| 0x213acf | 22 | Yeah, didn't think so. |
| 0x213ae6 | 39 | I shut my mouth after she glares at me. |
| 0x213b0e | 49 | If she takes a step closer, that blade is going\n |
| 0x213b40 | 45 | into my throat. Jachdwalt watches cautiously. |
| 0x213b6e | 50 | It feels like we're going to stand there glaring\n |
| 0x213ba1 | 47 | at each other forever... and we suddenly hear\n |
| 0x213bd1 | 30 | the echoes of a distant voice. |
| 0x213bf0 | 16 | Haku! Jachdwalt! |
| 0x213c04 | 49 | Entua is distracted for just a moment, but it's\n |
| 0x213c36 | 31 | enough for us to make our move. |
| 0x213c56 | 11 | Jachdwalt!! |
| 0x213c62 | 8 | Got it!! |
| 0x213c6b | 4 | Ah!? |
| 0x213c70 | 46 | Jachdwalt dashes forward and twists her arm.\n |
| 0x213c9f | 49 | As soon as she drops the sword, he kicks it away. |
| 0x213cd1 | 47 | He then swiftly covers her mouth with his hand. |
| 0x213d01 | 21 | Mng! Hnnngh! Hmmnnh!? |
| 0x213d17 | 5 | Boss! |
| 0x213d1d | 13 | Yeah, I know! |
| 0x213d2b | 50 | After seeing that Jachdwalt has securely subdued\n |
| 0x213d5e | 33 | Entua, I clamber out of the cave. |
| 0x213d80 | 11 | Hmmmnnngh!! |
| 0x213d8c | 44 | Entua struggles desperately, but Jachdwalt\n |
| 0x213db9 | 46 | quickly whispers in her ear, as if in warning. |
| 0x213de8 | 47 | Relax. Just leave it to the boss and it'll be\n |
| 0x213e18 | 5 | fine. |
| 0x213e1e | 37 | Haku! Were you able to find anything? |
| 0x213e44 | 27 | Nope! Didn't see a thing!\n |
| 0x213e60 | 42 | Looks like everyone's cleared out already! |
| 0x213e91 | 49 | Well, it's almost time we head back. We need to\n |
| 0x213ec3 | 27 | regroup with everyone else. |
| 0x213edf | 17 | I hear you, yeah? |
| 0x213ef1 | 51 | Once we can tell Kiwru's left the area, Jachdwalt\n |
| 0x213f25 | 41 | moves the hand covering the girl's mouth. |
| 0x213f4f | 10 | ...Pfaaah! |
| 0x213f5a | 41 | The girl quickly distances herself from\n |
| 0x213f84 | 29 | Jachdwalt, and glares at him. |
| 0x213fa2 | 46 | I pick up the sword lying on the ground, and\n |
| 0x213fd1 | 25 | place it in front of her. |
| 0x213feb | 27 | Here, you can have it back. |
| 0x214007 | 12 | My... sword? |
| 0x214014 | 46 | She glances down, but still keeps a wary eye\n |
| 0x214043 | 48 | on him. She seems confused by what just played\n |
| 0x214074 | 4 | out. |
| 0x214079 | 43 | Why... do you show mercy to me, your enemy? |
| 0x2140a5 | 49 | The war's over. I've kind of had enough of this\n |
| 0x2140d7 | 23 | whole enemy-ally stuff. |
| 0x2140ef | 48 | Of course, if you're still going to swing that\n |
| 0x214120 | 47 | sword around, we have a response for that, too. |
| 0x214150 | 44 | But if you ask me, it sounds like a lot of\n |
| 0x21417d | 48 | unnecessary trouble. And someone could get hurt. |
| 0x2141ae | 49 | My job here's been over for a while now. I just\n |
| 0x2141e0 | 43 | wanna go home, have a drink, and go to bed. |
| 0x21420c | 25 | ...You are the victors.\n |
| 0x214226 | 31 | You may do whatever you please. |
| 0x214246 | 45 | And the losers can do whatever they please,\n |
| 0x214274 | 8 | as well. |
| 0x21427d | 44 | In war, one side always wins and the other\n |
| 0x2142aa | 48 | loses. But the main thing is that you survive,\n |
| 0x2142db | 6 | right? |
| 0x2142e2 | 31 | ...You Yamatans are so bizarre. |
| 0x214302 | 45 | Trust me, I know for a fact several of them\n |
| 0x214330 | 20 | are completely nuts. |
| 0x214345 | 50 | ...Well then, Boss Nut. How about we go tell 'em\n |
| 0x214378 | 21 | we didn't see anyone? |
| 0x21438e | 45 | Jachdwalt takes off the canteen at his belt\n |
| 0x2143bc | 27 | and drops it on the ground. |
| 0x2143d8 | 43 | Guess she'll need food and water if she's\n |
| 0x214404 | 41 | gonna get away from the search parties... |
| 0x21442e | 33 | I also unfasten a bag of rations. |
| 0x214450 | 43 | We'll be heading back to the capital now.\n |
| 0x21447c | 31 | Don't really need this anymore. |
| 0x21449c | 41 | Thanks for taking care of Shinonon, yeah? |
| 0x2144c6 | 47 | With that, Jachdwalt turns and leaves without\n |
| 0x2144f6 | 13 | looking back. |
| 0x214504 | 45 | Of COURSE he exits with a badass one-liner.\n |
| 0x214532 | 42 | Wish I'd thought of one first... Ah, well. |
| 0x21455d | 35 | I follow Jachdwalt out of the cave. |
| 0x214581 | 41 | Entua, now alone, falls to her knees...\n |
| 0x2145ab | 46 | staring blankly at the ground in front of her. |
| 0x2145da | 49 | There, she sees her sword and the bag of rations. |
| 0x21460c | 22 | What do I do now...?\n |
| 0x214623 | 14 | Where do I go? |
| 0x214632 | 44 | How... How am I to live the rest of my life? |
| 0x21465f | 4 | I... |
| 0x214664 | 46 | Her father dead, unable to avenge his death,\n |
| 0x214693 | 41 | and now receiving mercy from the enemy... |
| 0x2146bd | 42 | And to even be thanked by that very enemy. |
| 0x2146e8 | 44 | For a warrior of Uzurusha, all humiliation\n |
| 0x214715 | 15 | beyond compare. |
| 0x214725 | 7 | Nngh... |
| 0x21472d | 46 | She quickly tries to grab for her sword, but\n |
| 0x21475c | 43 | falters, and her fingers twitch in the air. |
| 0x214788 | 44 | The anger and pride filling her heart have\n |
| 0x2147b5 | 44 | suddenly disappeared, leaving an emptiness\n |
| 0x2147e2 | 11 | within her. |
| 0x2147ee | 47 | And deep within, the conversation moments ago\n |
| 0x21481e | 42 | rings out, like the clear knell of a bell. |
| 0x214849 | 43 | What is important... is that you survive... |
| 0x214875 | 48 | She weakly reaches for the bag of rations, and\n |
| 0x2148a6 | 40 | pulls out a strip of simple dried jerky. |
| 0x2148cf | 45 | She puts it in her mouth, and slowly begins\n |
| 0x2148fd | 8 | to chew. |
| 0x214906 | 21 | ...It tastes... good. |
| 0x21491c | 43 | The tears run down her face, falling from\n |
| 0x214948 | 36 | her chin to the rations in her hand. |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_21.json` com a forma:
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
