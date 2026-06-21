# Cena ch_31_01 — pacote de traducao (246 linhas)

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
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `body` -> `body` (SYSTEM, 20_14)
- `face` -> `face` (SYSTEM, 20_14)
- `hair` -> `hair` (SYSTEM, 20_14)
- `Gate guard` -> `Guarda` (Sistema, 14_02)
- `you.` -> `isso.` (Nekone, 15_03)
- `right.` -> `direito.` (Kuon, 11_01)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `death.` -> `morte.` (Oshtor, 18_05)
- `around.` -> `por aí.` (Kuon, 14_02)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `the ground.` -> `no chão.` (Haku, 13_05)
- `Dear sister...` -> `Cara irmã...` (Nekone, 15_02)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `Are you sure about this?` -> `Você tem certeza disso?` (Kuon, 23_06)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `notice.` -> `vista.` (Ukon, 15_05)
- `Wh-What...?` -> `Q-Que...?` (Nekone, 14_04)
- `us.` -> `nós.` (Haku, 15_03)
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
| 0x3169af | 8 | RightArm |
| 0x3169b8 | 4 | body |
| 0x3169be | 4 | face |
| 0x3169c3 | 4 | hair |
| 0x3169c8 | 17 | RightIndexFinger2 |
| 0x3169da | 10 | Gate guard |
| 0x3169e5 | 10 | Hey, look! |
| 0x3169f0 | 24 | Yes... they've returned. |
| 0x316a09 | 41 | Thank goodness they've made it back safe! |
| 0x316a33 | 38 | We shall open the gates immediately!\n |
| 0x316a5a | 17 | Please step back! |
| 0x316a6c | 7 | Citizen |
| 0x316a74 | 40 | Oh, what a regal air he has about him... |
| 0x316a9d | 41 | He has grown to become such a fine man... |
| 0x316ac7 | 32 | Open the gates! OPEN THE GATES!! |
| 0x316ae8 | 4 | gate |
| 0x316aed | 16 | polySurface19404 |
| 0x316afe | 16 | polySurface19405 |
| 0x316b0f | 44 | Welcome back! You took a bit longer than I\n |
| 0x316b3c | 48 | expected. Everything went well, then, I suppose? |
| 0x316b71 | 42 | Well, well, looks like I win, Jachdwalt.\n |
| 0x316b9c | 38 | They arrived before sundown after all. |
| 0x316bc3 | 46 | Ah, dammit. And here I thought it'd take 'em\n |
| 0x316bf2 | 47 | a little longer to catch up. Fine, I'll pay up. |
| 0x316c22 | 14 | You lose, Dad! |
| 0x316c31 | 50 | Now, I don't want you running off again, Nekone.\n |
| 0x316c64 | 45 | I know how you must have felt, but that was\n |
| 0x316c92 | 10 | dangerous. |
| 0x316c9d | 47 | Who knows what could've happened? You took so\n |
| 0x316ccd | 48 | long to come back, I was getting worried about\n |
| 0x316cfe | 4 | you. |
| 0x316d03 | 22 | ...Yes... I apologize. |
| 0x316d1a | 10 | ...Nekone? |
| 0x316d25 | 41 | Miss Nekone... is something the matter?\n |
| 0x316d4f | 27 | You don't look very well... |
| 0x316d6b | 45 | Whassamatter, little lady? You have a tummy\n |
| 0x316d99 | 5 | ache? |
| 0x316d9f | 31 | No... It is nothing. I am well. |
| 0x316dbf | 28 | So what about our pursuer?\n |
| 0x316ddc | 21 | What happened to him? |
| 0x316df2 | 43 | ...Our pursuer, General Vurai... has been\n |
| 0x316e1e | 30 | eliminated by my dear brother. |
| 0x316e3d | 45 | The danger that we faced has abated for the\n |
| 0x316e6b | 11 | time being. |
| 0x316e77 | 27 | *Whistle* Damn. Impressive. |
| 0x316e93 | 45 | You actually defeated him... But of course,\n |
| 0x316ec1 | 48 | Oshtor IS Yamato's famed Imperial Guard of the\n |
| 0x316ef2 | 6 | Right. |
| 0x316ef9 | 7 | Soldier |
| 0x316f01 | 46 | Wait, do they mean Vurai of the Eight Pillar\n |
| 0x316f30 | 12 | Generals...? |
| 0x316f3d | 43 | Then those rumors of rebellion were true... |
| 0x316f69 | 45 | Indeed. From what I have heard, Lord Oshtor\n |
| 0x316f97 | 48 | rescued Her Highness from a conspiracy for her\n |
| 0x316fc8 | 6 | death. |
| 0x316fcf | 48 | Her Highness...? Wait, Her Highness is all the\n |
| 0x317000 | 31 | way in this neck of the woods!? |
| 0x317020 | 50 | You didn't know? Her Highness trusts Lord Oshtor\n |
| 0x317053 | 50 | more than any other. Of course she would come to\n |
| 0x317086 | 4 | him! |
| 0x31708b | 28 | Holy crap! That's amazing!\n |
| 0x3170a8 | 23 | That's our Lord Oshtor! |
| 0x3170c0 | 25 | Um... but Sir Haku is...? |
| 0x3170da | 44 | In any case, where's Haku? I don't see him\n |
| 0x317107 | 7 | around. |
| 0x31710f | 27 | Y-Yes... Where is Sir Haku? |
| 0x31712b | 48 | Hmmm, you're right. Where has he scampered off\n |
| 0x31715c | 7 | to now? |
| 0x317164 | 47 | How dare he not wake me up for something that\n |
| 0x317194 | 46 | much fun. I've got to give him a piece of my\n |
| 0x3171c3 | 5 | mind! |
| 0x3171c9 | 49 | I think I can guess. I suppose... he complained\n |
| 0x3171fb | 45 | that he was too tired and fell behind while\n |
| 0x317229 | 13 | slacking off? |
| 0x317237 | 19 | ...Um, Miss Nekone? |
| 0x31724b | 46 | I guess I can't blame him, though. The sun's\n |
| 0x31727a | 41 | setting... I'll head out and get him now. |
| 0x3172a4 | 19 | ...This is for you. |
| 0x3172b8 | 7 | ...Huh? |
| 0x3172c0 | 22 | This is... Haku's fan? |
| 0x3172d7 | 38 | ...He asked that I return this to you. |
| 0x3172fe | 31 | What... exactly... do you mean? |
| 0x31731e | 25 | What do you mean by this? |
| 0x317338 | 34 | What's... What's happened to Haku? |
| 0x31735b | 10 | Answer me! |
| 0x317366 | 14 | ...He is dead. |
| 0x317375 | 3 | Hm? |
| 0x317379 | 10 | ...Huh...? |
| 0x317384 | 42 | It was his wish that I return this to you. |
| 0x3173af | 26 | What... are you saying...? |
| 0x3173ca | 16 | Haku is... dead? |
| 0x3173db | 18 | That's impossible. |
| 0x3173ee | 48 | Haku is a coward. He's extremely cautious, and\n |
| 0x31741f | 12 | sly to boot. |
| 0x31742c | 50 | I know he'd do anything--ANYTHING to stay alive.\n |
| 0x31745f | 37 | That's just the sort of person he is. |
| 0x317485 | 42 | And you're... you're telling me he's dead? |
| 0x3174b0 | 45 | That can't be true. I... I don't believe you. |
| 0x3174de | 48 | Nekone, please tell him to stop with this sick\n |
| 0x31750f | 6 | joke-- |
| 0x317516 | 17 | Dear... sister... |
| 0x317528 | 27 | Th-That... That can't be... |
| 0x317544 | 14 | Sir... Haku... |
| 0x317553 | 44 | Wha--Hey, Rulutieh! Pull yourself together-- |
| 0x317580 | 17 | ...How, I wonder? |
| 0x317592 | 43 | You were with him... How did you let this\n |
| 0x3175be | 10 | happen...? |
| 0x3175c9 | 12 | Answer me... |
| 0x3175d6 | 20 | Answer me, Oshtor... |
| 0x3175eb | 30 | I demand your answer, Oshtor!! |
| 0x31760a | 14 | ...I am sorry. |
| 0x31761c | 6 | Kuon!? |
| 0x317623 | 13 | Dear sister!! |
| 0x317631 | 49 | The metal fan swings straight down at his skull\n |
| 0x317663 | 42 | with enough force to split a tree in half. |
| 0x31768e | 47 | Everyone instinctively looks away just before\n |
| 0x3176be | 24 | the grisly impact, but-- |
| 0x3176d7 | 45 | The metal fan has stopped, a hair's breadth\n |
| 0x317705 | 22 | from contact with him. |
| 0x31771c | 47 | The fan trembles in Kuon's grip as it remains\n |
| 0x31774c | 32 | in the air, just above its mark. |
| 0x31776d | 46 | ..."I'm sorry I broke our promise in the end." |
| 0x31779c | 48 | "All the days I spent with you guys... I had a\n |
| 0x3177cd | 12 | great time." |
| 0x3177da | 15 | "...Thank you." |
| 0x3177ea | 39 | Lord Haku bade me deliver this message. |
| 0x317812 | 48 | Kuon's arm falls limply to her side, the metal\n |
| 0x317843 | 46 | fan slipping from her hand and clattering to\n |
| 0x317872 | 11 | the ground. |
| 0x31787e | 14 | Dear sister... |
| 0x31788d | 26 | What... does it matter...? |
| 0x3178a8 | 5 | Kuon? |
| 0x3178ae | 43 | I only... saved him in the first place...\n |
| 0x3178da | 12 | on a whim... |
| 0x3178e7 | 27 | Kuon, where are you going!? |
| 0x317903 | 20 | I have to go home... |
| 0x317918 | 34 | Go home...? Where exactly is home? |
| 0x31793b | 50 | I could only stay here... until Haku could learn\n |
| 0x31796e | 45 | to live on his own... That was the promise... |
| 0x31799c | 32 | So... I can't be here anymore... |
| 0x3179bd | 7 | Kuon... |
| 0x3179c5 | 24 | Are you sure about this? |
| 0x3179de | 46 | I had so much fun with all of you. Kuon, are\n |
| 0x317a0d | 46 | you sure you want to just leave it all behind? |
| 0x317a3c | 23 | ...Thank you, everyone. |
| 0x317a54 | 25 | I had a lot of fun too... |
| 0x317a6e | 31 | It really was... so much fun... |
| 0x317a8e | 5 | Ah... |
| 0x317a94 | 28 | Bosslady, you're going away? |
| 0x317ab1 | 11 | ...Goodbye. |
| 0x317abd | 9 | Bosslady? |
| 0x317ac7 | 11 | Don't go... |
| 0x317ad3 | 46 | I'm right here... I'm right in front of you... |
| 0x317b02 | 44 | ...Maybe I could just tell Kuon the truth,\n |
| 0x317b2f | 19 | and no one else--\n |
| 0x317b43 | 14 | No... I can't. |
| 0x317b52 | 36 | No one can know of Oshtor's death.\n |
| 0x317b77 | 16 | Not even Kuon... |
| 0x317b88 | 10 | ...Kuon... |
| 0x317b93 | 31 | Don't chase her... You can't.\n |
| 0x317bb3 | 32 | You've already made your choice. |
| 0x317bd4 | 31 | ...There's no turning back now. |
| 0x317bf4 | 49 | I turn my back to Kuon, fighting the urge to go\n |
| 0x317c26 | 10 | after her. |
| 0x317c31 | 48 | I had already made my choice the moment I held\n |
| 0x317c62 | 23 | the Akuruka in my hand. |
| 0x317c7a | 48 | The only path remaining before me is a path of\n |
| 0x317cab | 8 | carnage. |
| 0x317cb4 | 49 | I must not falter. Even if it means I will lose\n |
| 0x317ce6 | 22 | everything dear to me. |
| 0x317cfd | 17 | For my name is... |
| 0x317d0f | 48 | I look down from the podium at the citizens of\n |
| 0x317d40 | 43 | Ennakamuy, who have all gathered on short\n |
| 0x317d6c | 7 | notice. |
| 0x317d74 | 47 | All look up to me silently, their expressions\n |
| 0x317da4 | 30 | creased with worry and unease. |
| 0x317dc3 | 49 | I falter at the sight of hundreds--thousands of\n |
| 0x317df5 | 44 | eyes looking to me for answers. However, I\n |
| 0x317e22 | 21 | cannot step down now. |
| 0x317e38 | 21 | Let us begin, then... |
| 0x317e4e | 30 | Beloved people of Ennakamuy!\n |
| 0x317e6d | 32 | I thank you for gathering today! |
| 0x317e8e | 50 | I know you are wracked by worry and uncertainty,\n |
| 0x317ec1 | 48 | not knowing what has occurred in Yamato of late. |
| 0x317ef2 | 44 | Citizens of Ennakamuy, I bring grim truth.\n |
| 0x317f1f | 48 | Yamato stands on the brink of an unprecedented\n |
| 0x317f50 | 7 | crisis. |
| 0x317f58 | 30 | Our great father, the Mikado-- |
| 0x317f77 | 30 | The god incarnate, has passed! |
| 0x317f96 | 26 | Passed... Does he mean...? |
| 0x317fb1 | 33 | *Gasp*... No... That can't be...! |
| 0x317fd3 | 11 | Wh-What...? |
| 0x317fdf | 36 | The Mikado...? But he can't have...? |
| 0x318004 | 28 | So that means... He's dead!? |
| 0x318021 | 43 | Yet his life ended not by the will of the\n |
| 0x31804d | 41 | heavens, but by malicious plot and dark\n |
| 0x318077 | 11 | conspiracy! |
| 0x318083 | 25 | And there remains more... |
| 0x31809d | 51 | After the Mikado's death, countless seeds of evil\n |
| 0x3180d1 | 45 | began to sprout, as a garden of dark spirits. |
| 0x3180ff | 48 | And they dared even to bare their fangs at the\n |
| 0x318130 | 43 | Mikado's trueborn successor, Her Imperial\n |
| 0x31815c | 9 | Highness! |
| 0x318166 | 46 | By fortune's grace, I was able to rescue Her\n |
| 0x318195 | 45 | Highness. She now lays sick in bed, but she\n |
| 0x3181c3 | 12 | still lives. |
| 0x3181d0 | 44 | However, they that sought to harm her will\n |
| 0x3181fd | 49 | surely reach out again, wretched hands grasping\n |
| 0x31822f | 12 | at her life! |
| 0x31823c | 43 | Such vile acts, such ATROCITY against our\n |
| 0x318268 | 44 | beloved Highness! And will we stand by and\n |
| 0x318295 | 12 | allow this!? |
| 0x3182a2 | 4 | NO!! |
| 0x3182a7 | 50 | How could we hand Her Highness over to traitors,\n |
| 0x3182da | 46 | who have forgotten all they owe to the great\n |
| 0x318309 | 8 | Mikado!? |
| 0x318312 | 47 | A land unjust--a land tainted by shame, lies,\n |
| 0x318342 | 40 | and deceit--is not the land we owe our\n |
| 0x31836b | 20 | children's children! |
| 0x318380 | 42 | Of course, I understand your fears of war. |
| 0x3183ab | 31 | Yet I must ask you, regardless. |
| 0x3183cb | 45 | Please, I ask that you stand with me--No...\n |
| 0x3183f9 | 18 | with Her Highness. |
| 0x31840c | 47 | Her Highness's smile was warm and kind as the\n |
| 0x31843c | 48 | Timanonna, the sun's flower, but now it is gone. |
| 0x31846d | 47 | The smile that we so love has been taken from\n |
| 0x31849d | 3 | us. |
| 0x3184a1 | 46 | And... that I might return that smile to Her\n |
| 0x3184d0 | 45 | Highness's face, I ask the aid of all of you. |
| 0x3184fe | 25 | You are all my last hope! |
| 0x318518 | 46 | And I know for certain that with your help--\n |
| 0x318547 | 42 | if Ennakamuy unites as one, we need fear\n |
| 0x318572 | 8 | nothing! |
| 0x31857b | 46 | I know that with your strength, Her Highness\n |
| 0x3185aa | 17 | will smile again! |
| 0x3185bc | 47 | If all of us act as one, Ennakamuy will never\n |
| 0x3185ec | 12 | know defeat! |
| 0x3185f9 | 47 | And I swear this to you! I shall protect both\n |
| 0x318629 | 42 | Her Imperial Highness and my homeland of\n |
| 0x318654 | 10 | Ennakamuy! |
| 0x31865f | 48 | I swear upon the Akuruka bestowed to me by the\n |
| 0x318690 | 49 | Mikado! Upon the name of Oshtor, Imperial Guard\n |
| 0x3186c2 | 14 | of the Right!! |
| 0x3186d1 | 46 | People of Ennakamuy! My brethren! Now is our\n |
| 0x318700 | 44 | time to rise! Join me under Her Highness's\n |
| 0x31872d | 8 | banner!! |

## 8. Formato de saida EXIGIDO
Escreva `translations_31_01.json` com a forma:
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
