# Cena ch_21_01 — pacote de traducao (202 linhas)

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
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `place.` -> `lugar.` (Protagonista, 16_01)
- `sure.` -> `não.` (Haku, 12_16)
- `for you.` -> `para você.` (Ougi, 13_08)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `after all...` -> `afinal...` (Man, 11_01)
- `Huh...` -> `Hum...` (Ukon, 15_05)
- `Honoka.` -> `Honoka.` (Haku, 19_05)
- `Whoa!` -> `Uou!` (Haku, 11_11)
- `out.` -> `fora.` (Atuy, 17_01)
- `to happen.` -> `acontecer.` (Homem, 17_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `What are you--` -> `O que você está--` (Haku, 20_03)
- `now.` -> `já.` (Kuon, 14_04)
- `yet.` -> `ainda.` (Homem, 18_01)
- `of that.` -> `disso.` (Rulutieh, 16_01)
- `Well...` -> `Bom...` (Haku, 12_03)
- `excitement.` -> `frenéticos.` (Haku, 14_03)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `this...?` -> `isto...?` (Haku, 18_01)
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
| 0x2166f6 | 45 | Several days after what became known as the\n |
| 0x216724 | 22 | "Uzurusha Conquest"... |
| 0x21673b | 49 | I'm lounging in my room after getting back from\n |
| 0x21676d | 45 | Uzurusha, taking a rest, when the twins tug\n |
| 0x21679b | 13 | on my sleeve. |
| 0x2167a9 | 24 | That time again, huh...? |
| 0x2167c2 | 46 | I force my weary body up, and soon the twins\n |
| 0x2167f1 | 34 | are leading me forward once again. |
| 0x216814 | 50 | And just like before, we arrive at the old guy's\n |
| 0x216847 | 6 | place. |
| 0x21684e | 42 | Lord Haku, I thank you for accepting our\n |
| 0x216879 | 22 | invitation once again. |
| 0x216890 | 23 | Er, it's no big deal... |
| 0x2168a8 | 36 | Ho ho ho. No need to be so modest.\n |
| 0x2168cd | 30 | Please, make yourself at home. |
| 0x2168ec | 5 | Sure. |
| 0x2168f2 | 45 | I take a seat in front of the old man as he\n |
| 0x216920 | 12 | tells me to. |
| 0x21692d | 44 | Now that I think about it, why is this old\n |
| 0x21695a | 32 | geezer so friendly to me anyway? |
| 0x21697b | 48 | If I'm right, I'd normally never be allowed to\n |
| 0x2169ac | 39 | speak to him, let alone see his face... |
| 0x2169d4 | 8 | For you. |
| 0x2169dd | 11 | Oh, thanks. |
| 0x2169e9 | 49 | I accept the cup of tea that Honoka offers to me. |
| 0x216a1b | 47 | Inside is a clear green liquid, a light steam\n |
| 0x216a4b | 19 | wafting up from it. |
| 0x216a5f | 40 | I recalled that you preferred green tea. |
| 0x216a88 | 17 | You remembered... |
| 0x216a9a | 49 | I can feel a warmth in my chest as I take a sip\n |
| 0x216acc | 15 | of the hot tea. |
| 0x216adc | 44 | So, was there something you wanted to talk\n |
| 0x216b09 | 9 | about...? |
| 0x216b13 | 46 | Indeed. There was something that I wished to\n |
| 0x216b42 | 17 | discuss with you. |
| 0x216b54 | 41 | To tell the truth, I am something of an\n |
| 0x216b7e | 42 | enthusiast of ancient ruins and artifacts. |
| 0x216ba9 | 8 | Ruins... |
| 0x216bb2 | 48 | You are aware of the recent war between Yamato\n |
| 0x216be3 | 37 | and the nation north of us, Uzurusha? |
| 0x216c09 | 11 | Well, yeah. |
| 0x216c15 | 45 | I was kind of thrown into the middle of it,\n |
| 0x216c43 | 12 | after all... |
| 0x216c50 | 47 | After the war ended and we surveyed uncharted\n |
| 0x216c80 | 45 | Uzurushan lands, we were able to locate new\n |
| 0x216cae | 6 | ruins. |
| 0x216cb5 | 48 | The Uzurushan barbarians showed no interest in\n |
| 0x216ce6 | 44 | these ruins, and so they seem yet untouched. |
| 0x216d13 | 6 | Huh... |
| 0x216d1a | 46 | Not really my thing, but I'm sure if Kuon or\n |
| 0x216d49 | 41 | Nekone heard about it they'd be ecstatic. |
| 0x216d73 | 50 | I would like nothing more than to investigate it\n |
| 0x216da6 | 48 | myself... but with my legs, I could not travel\n |
| 0x216dd7 | 7 | so far. |
| 0x216ddf | 50 | Are you asking me to go take a look at the place\n |
| 0x216e12 | 17 | in your stead...? |
| 0x216e24 | 50 | Precisely. Of course, I wouldn't ask you without\n |
| 0x216e57 | 50 | compensation. An adequate reward will be prepared. |
| 0x216e8a | 26 | Well, that sounds a bit... |
| 0x216ea5 | 7 | Honoka. |
| 0x216ead | 14 | Yes, my liege. |
| 0x216ebc | 50 | With a thud and a clink, Honoka drops what looks\n |
| 0x216eef | 44 | like a rather hefty bag on top of the table. |
| 0x216f1c | 5 | Whoa! |
| 0x216f22 | 47 | The bag is absolutely stuffed with glittering\n |
| 0x216f52 | 14 | golden pieces. |
| 0x216f61 | 38 | This should cover preparatory costs.\n |
| 0x216f88 | 46 | We will prepare the reward upon your return.\n |
| 0x216fb7 | 17 | If you need mor-- |
| 0x216fc9 | 16 | I'm on the case. |
| 0x216fda | 29 | Hmhm... Thank you, Lord Haku. |
| 0x216ff8 | 44 | Good, good. I had a feeling that you would\n |
| 0x217025 | 7 | accept. |
| 0x21702d | 37 | This much gold just for prep costs?\n |
| 0x217053 | 48 | I could live like a tycoon for a while on this\n |
| 0x217084 | 6 | alone! |
| 0x21708b | 51 | And we haven't had any jobs from Oshtor recently.\n |
| 0x2170bf | 42 | We've all got some free time on our hands. |
| 0x2170ea | 50 | And if it involves investigating ruins, Kuon and\n |
| 0x21711d | 45 | Nekone wouldn't even care if the reward was\n |
| 0x21714b | 6 | small. |
| 0x217152 | 49 | I'm sure they won't suspect a thing if I skim a\n |
| 0x217184 | 42 | little off the top. Heh heh heh heh heh... |
| 0x2171af | 44 | Well! I am glad that is settled. I am in a\n |
| 0x2171dc | 46 | splendid mood... Honoka, please prepare us a\n |
| 0x21720b | 17 | suitable banquet. |
| 0x21721d | 29 | Mmm, hmhmhm hmmm hmmm...♪\n |
| 0x21723b | 5 | *Hic* |
| 0x217241 | 45 | Whew, what a feast. The food was delicious,\n |
| 0x21726f | 26 | the drinks were amazing... |
| 0x21728a | 47 | Can't believe there are people out there that\n |
| 0x2172ba | 36 | enjoy this stuff on a daily basis... |
| 0x2172df | 49 | Might've drank a little too much, but how can I\n |
| 0x217311 | 44 | refuse when Honoka's the one pouring them?\n |
| 0x21733e | 19 | I couldn't help it. |
| 0x217352 | 51 | I totter back home, Uruuru and Saraana supporting\n |
| 0x217386 | 48 | me. By the time I get back, it's already light\n |
| 0x2173b7 | 4 | out. |
| 0x2173bc | 23 | Honeeey, I'm hoooooome. |
| 0x2173d4 | 13 | Welcome back. |
| 0x2173e6 | 36 | Well, you certainly came back early. |
| 0x21740b | 15 | Bwuh!? K-Kuon!? |
| 0x21741b | 30 | What is she doing in my room!? |
| 0x21743a | 51 | You seem to be in a good mood. I suppose I'd like\n |
| 0x21746e | 42 | to know where exactly you were last night. |
| 0x217499 | 17 | W-Well, that's... |
| 0x2174ab | 28 | Y-You see, these two here... |
| 0x2174c8 | 31 | I turn around for some support. |
| 0x2174e8 | 17 | ...They're gone!? |
| 0x2174fa | 47 | ...Yeah, I kinda had a feeling this was going\n |
| 0x21752a | 10 | to happen. |
| 0x217535 | 40 | I was having dinner at a friend's place. |
| 0x21755e | 41 | I sit down on a seat as I give my excuse. |
| 0x217588 | 47 | I don't think you're sitting in the right spot. |
| 0x2175b8 | 4 | Huh? |
| 0x2175bd | 36 | Sit up straight here. On your knees. |
| 0x2175e2 | 14 | What are you-- |
| 0x2175f1 | 4 | Now. |
| 0x2175f6 | 13 | ...Yes ma'am. |
| 0x217604 | 52 | For some reason, I can't fight her quiet pressure.\n |
| 0x217639 | 24 | I meekly do as she says. |
| 0x217652 | 50 | I can't tell you that you shouldn't drink, or go\n |
| 0x217685 | 34 | fooling around with strange women. |
| 0x2176a8 | 43 | Hold on, I'll admit I was drinking, but I\n |
| 0x2176d4 | 8 | wasn't-- |
| 0x2176dd | 48 | I understand sometimes you just want to have a\n |
| 0x21770e | 47 | good time, but you aren't quite fully fledged\n |
| 0x21773e | 4 | yet. |
| 0x217743 | 50 | And I can't really approve of a person like that\n |
| 0x217776 | 45 | fooling around and stumbling home at sunrise. |
| 0x2177a4 | 51 | Argh, she sounds like a mom, but she has a point.\n |
| 0x2177d8 | 44 | I'm still in her care. Maybe I screwed up... |
| 0x217805 | 31 | But I still have my trump card. |
| 0x217825 | 42 | There's actually a good reason for this.\n |
| 0x217850 | 20 | I just got us a job. |
| 0x217865 | 48 | What does that have to do with you coming home\n |
| 0x217896 | 13 | at this hour? |
| 0x2178a4 | 40 | Just hear me out. The job I got was to\n |
| 0x2178cd | 23 | investigate some ruins. |
| 0x2178e5 | 45 | I can see Kuon's ears twitch at the mention\n |
| 0x217913 | 8 | of that. |
| 0x21791c | 50 | And from what I hear, they're totally untouched.\n |
| 0x21794f | 27 | Who knows how old they are. |
| 0x21796b | 19 | ...Details, please. |
| 0x21797f | 25 | Yesss. She took the bait. |
| 0x217999 | 7 | Well... |
| 0x2179a1 | 47 | I give her an explanation of the job, keeping\n |
| 0x2179d1 | 33 | the details vague on the old man. |
| 0x2179f3 | 48 | But I make sure to bring attention to the fact\n |
| 0x217a24 | 35 | that this ruin is still unexplored. |
| 0x217a48 | 46 | Kuon stays silent for a while after I finish\n |
| 0x217a77 | 24 | telling her the details. |
| 0x217a90 | 45 | She's trying to look calm, but her ears and\n |
| 0x217abe | 46 | tail are twitching. Guess she can't hide her\n |
| 0x217aed | 11 | excitement. |
| 0x217af9 | 46 | Looks like that strategy was pretty effective. |
| 0x217b28 | 51 | All right. If that's the case, I'll need to start\n |
| 0x217b5c | 21 | on some preparations. |
| 0x217b72 | 12 | Sounds good. |
| 0x217b7f | 47 | Well, I think I'll just get some sleep in the\n |
| 0x217baf | 5 | mea-- |
| 0x217bb5 | 28 | You still need to sit there. |
| 0x217bd2 | 30 | Wh... Now hold on, I thought-- |
| 0x217bf1 | 47 | Oh, and by the way, I'll be hanging on to this. |
| 0x217c21 | 5 | Gah!? |
| 0x217c27 | 43 | The funds I had hid under my clothes are,\n |
| 0x217c53 | 25 | somehow, in Kuon's hands. |
| 0x217c6d | 50 | You sit there and think about what you did until\n |
| 0x217ca0 | 34 | everyone wakes up. Any objections? |
| 0x217cc3 | 13 | ...No, ma'am. |
| 0x217cd1 | 51 | We tell the rest of the group about investigating\n |
| 0x217d05 | 25 | the ruins over breakfast. |
| 0x217d1f | 47 | We quickly arrange for a carriage, and by the\n |
| 0x217d4f | 46 | time the sun's risen, we're ready to set out\n |
| 0x217d7e | 6 | north. |
| 0x217d85 | 50 | And so our two carriages set off on the mountain\n |
| 0x217db8 | 46 | path, on the morning of a beautiful sunny day. |
| 0x217de7 | 21 | An unexplored ruin... |
| 0x217dfd | 47 | You seem... very excited about this, Miss Kuon. |
| 0x217e2d | 51 | Most ruins in Yamato have already been thoroughly\n |
| 0x217e61 | 49 | investigated. An untouched one is quite exciting. |
| 0x217e93 | 18 | Hey, hey, whassat? |
| 0x217ea6 | 41 | Shinonon, it's dangerous to lean so far\n |
| 0x217ed0 | 8 | outside. |
| 0x217ed9 | 47 | Hee hee! You seem pretty excited too, Shinonon. |
| 0x217f09 | 47 | And so I hold the reins, listening once again\n |
| 0x217f39 | 35 | to all the cheery voices behind me. |
| 0x217f5d | 7 | Argh... |
| 0x217f65 | 38 | A dull pain throbs around my temple.\n |
| 0x217f8c | 15 | Damn hangovers. |
| 0x217f9c | 26 | Master, are you all right? |
| 0x217fb7 | 47 | You may leave the reins to us and lie down to\n |
| 0x217fe7 | 17 | rest if you wish. |
| 0x217ff9 | 48 | She pats her thigh invitingly as she makes the\n |
| 0x21802a | 6 | offer. |
| 0x218031 | 21 | Thanks, but I'm good. |
| 0x218047 | 48 | Now that I think about it, I didn't get a wink\n |
| 0x218078 | 20 | of sleep last night. |
| 0x21808d | 47 | Man... I feel awful. So sleepy. And I'm being\n |
| 0x2180bd | 45 | forced to drive the carriage in this state... |
| 0x2180eb | 49 | I say this a lot, but... how did it end up like\n |
| 0x21811d | 8 | this...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_21_01.json` com a forma:
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
