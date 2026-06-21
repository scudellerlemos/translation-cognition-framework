# Cena ch_11_03 — pacote de traducao (118 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |

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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Geez...! Too bright out here...` -> `Aff...! Claridade demais aqui fora...` (Haku, 11_03)
- `Well, guess the sun still rises no matter where\n` -> `Enfim, o sol nasce em qualquer lugar, pelo visto\n` (Haku, 11_03)
- `I am. Still... What am I supposed to do now...?` -> `Pois é. Mesmo assim... O que é que eu faço agora...?` (Haku, 11_03)
- `How are you feeling, I wonder?` -> `Como será que você está se sentindo?` (Kuon, 11_03)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `I glance back at the sudden question, and see\n` -> `Olho pra trás com a pergunta repentina e vejo\n` (Haku, 11_03)
- `Kuon making breakfast.` -> `a Kuon preparando o café da manhã.` (Haku, 11_03)
- `I didn't really see any external signs of injuries,\n` -> `Não vi nenhum sinal de ferimento por fora,\n` (Kuon, 11_03)
- `but you can never be too careful...` -> `mas todo cuidado é pouco...` (Kuon, 11_03)
- `I guess I feel...` -> `Acho que me sinto...` (Haku, 11_03)
- `It's true that I was in a coma when Kuon found me.\n` -> `É verdade que eu estava em coma quando a Kuon me achou.\n` (Haku, 11_03)
- `And then getting chased down by huge monsters...` -> `E depois ser perseguido por monstros enormes...` (Haku, 11_03)
- `So I try stretching my shoulders, and crack my neck\n` -> `Então tento alongar os ombros e estalo o pescoço\n` (Haku, 11_03)
- `with a couple twists of my head.` -> `com algumas viradas de cabeça.` (Haku, 11_03)
- `...Well, seems like everything still works.` -> `...Bom, parece que tudo ainda funciona.` (Haku, 11_03)
- `You're sure?` -> `Tem certeza?` (Kuon, 11_03)
- `Yeah, I'm fine. It's just muscle ache more than\n` -> `Tô bem, sim. É mais dor muscular do que\n` (Haku, 11_03)
- `anything else, really.` -> `qualquer outra coisa, na real.` (Haku, 11_03)
- `My offhanded dismissal seems to get a giggle from\n` -> `Minha resposta despreocupada arranca uma risadinha\n` (Haku, 11_03)
- `Kuon. Maybe I tried too hard to sound macho.` -> `da Kuon. Talvez eu tenha forçado pra soar machão.` (Haku, 11_03)
- `I'm relieved to hear that. Then, let's leave\n` -> `Fico aliviada em saber. Então, vamos partir\n` (Kuon, 11_03)
- `after breakfast, shall we?` -> `depois do café, que tal?` (Kuon, 11_03)
- `Wait, leave?` -> `Espera, partir?` (Haku, 11_03)
- `Leave to where?` -> `Partir pra onde?` (Haku, 11_03)
- `Staying here would be a bad idea, so we'll head\n` -> `Ficar aqui seria má ideia, então vamos seguir\n` (Kuon, 11_03)
- `to a village just nearby.` -> `pra uma vila aqui pertinho.` (Kuon, 11_03)
- `So it's close?` -> `Então é perto?` (Haku, 11_03)
- `Yup, walking distance.` -> `Aham, dá pra ir a pé.` (Kuon, 11_03)
- `I see... I mean, I just thought...` -> `Saquei... Quer dizer, é que eu achei...` (Haku, 11_03)
- `You thought what?` -> `Achou o quê?` (Kuon, 11_03)
- `I kind of figured you lived here, Kuon.` -> `Meio que imaginei que você morasse aqui, Kuon.` (Haku, 11_03)
- `Oh, so I suppose I look like some backwoods\n` -> `Ah, então você acha que eu tenho cara de eremita\n` (Kuon, 11_03)
- `hermit who lives up in the mountains? Is that it? ` -> `do mato, vivendo lá nas montanhas? É isso? ` (Kuon, 11_03)
- `Kuon's eyes narrow, her gaze fixed on me...` -> `Os olhos da Kuon se estreitam, o olhar fixo em mim...` (Haku, 11_03)
- `Well, don't let me stop you. If you want us to\n` -> `Bom, não vou te impedir. Se você quer que a gente\n` (Kuon, 11_03)
- `live in a tent, then by all means. How about\n` -> `viva numa barraca, fique à vontade. O que acha\n` (Kuon, 11_03)
- `it, Haku?` -> `disso, Haku?` (Kuon, 11_03)
- `It sounds like a joke when she says it, but her\n` -> `Soa como piada quando ela fala, mas o\n` (Haku, 11_03)
- `smile doesn't reach her eyes...` -> `sorriso dela não chega aos olhos...` (Haku, 11_03)
- `W-Wait, hold on! That's not what I meant!` -> `E-Espera, calma aí! Não foi isso que eu quis dizer!` (Haku, 11_03)
- `Ahaha... It's just a joke.` -> `Ahaha... É só brincadeira.` (Kuon, 11_03)
- `I just stopped by, since I'm on my journey...\n` -> `Só dei uma passada, já que estou de viagem...\n` (Kuon, 11_03)
- `but now that you're here, we'd better head to\n` -> `mas agora que você está aqui, é melhor irmos pra\n` (Kuon, 11_03)
- `a town.` -> `uma cidade.` (Kuon, 11_03)
- `A journey, huh...` -> `Uma viagem, hum...` (Haku, 11_03)
- `...Well, maybe someone at the village might\n` -> `...Bom, talvez alguém na vila possa\n` (Haku, 11_03)
- `know more about me.` -> `saber mais sobre mim.` (Haku, 11_03)
- `Who knows? Maybe this is all it'll take to\n` -> `Quem sabe? Talvez seja só isso que eu precise pra\n` (Haku, 11_03)
- `clear this up.` -> `esclarecer tudo isso.` (Haku, 11_03)
- `OK then... while I'm working on breakfast,\n` -> `Beleza então... enquanto eu termino o café,\n` (Kuon, 11_03)
- `can you load him up with our baggage, Haku?` -> `você pode carregar a bagagem nele, Haku?` (Kuon, 11_03)
- `Head` -> `Head` (rotulo, 11_03)
- `..."Him"?` -> `..."Nele"?` (Haku, 11_03)
- `I tilt my head, bemused.` -> `Inclino a cabeça, confuso.` (Haku, 11_03)
- `Well, I don't see anyone around except us...` -> `Bom, não vejo ninguém por aqui além da gente...` (Haku, 11_03)
- `GREHHHH!` -> `GREHHHH!` (toriuma, 11_03)
- `HOLY--` -> `MEU DEU--` (Haku, 11_03)
- `Wh-What the heck is this ostrich-looking thing!?` -> `Q-Que diabo é essa coisa que parece um avestruz!?` (Haku, 11_03)
- `I don't know if Ostrich Prime here thinks I'm its\n` -> `Não sei se o Avestruz Supremo aqui acha que eu sou o\n` (Haku, 11_03)
- `dinner, but it keeps trying to take a bite out of\n` -> `jantar, mas ele não para de tentar arrancar um pedaço de\n` (Haku, 11_03)
- `me...` -> `mim...` (Haku, 11_03)
- `Ostrich? I don't know what you mean. He's just\n` -> `Avestruz? Não sei do que você está falando. Ele é só\n` (Kuon, 11_03)
- `my steed.` -> `minha montaria.` (Kuon, 11_03)
- `Steed...? What, like a horse?` -> `Montaria...? Tipo, um cavalo?` (Haku, 11_03)
- `How could this thing be a--well, no, just look\n` -> `Como essa coisa pode ser um--bom, não, é só olhar\n` (Haku, 11_03)
- `at Kuon... I guess if she says it's a horse, it is.` -> `pra Kuon... Acho que se ela diz que é cavalo, então é.` (Haku, 11_03)
- `...God, I can feel common sense draining away\n` -> `...Deus, dá pra sentir o bom senso evaporando\n` (Haku, 11_03)
- `with every minute I spend here... ` -> `a cada minuto que passo aqui... ` (Haku, 11_03)
- `After breakfast, we pack up the tent, and with\n` -> `Depois do café, desmontamos a barraca e, com\n` (Haku, 11_03)
- `the sun low in the sky, we set off. With an\n` -> `o sol baixo no céu, partimos. Com um\n` (Haku, 11_03)
- `ostrich.` -> `avestruz.` (Haku, 11_03)
- `By the way, is this really... OK?` -> `Aliás, isso aqui é... seguro mesmo?` (Haku, 11_03)
- `What could that mean, I wonder?` -> `E o que isso quer dizer, hein?` (Kuon, 11_03)
- `Well, you said you're on some journey.\n` -> `Bom, você disse que está numa viagem.\n` (Haku, 11_03)
- `I hope I'm not messing up any of your plans here.` -> `Espero não estar atrapalhando seus planos.` (Haku, 11_03)
- `Kuon responds easily, like it's nothing.` -> `A Kuon responde tranquila, como se não fosse nada.` (Haku, 11_03)
- `I didn't come to this forest for anything important.\n` -> `Não vim a esta floresta por nada importante.\n` (Kuon, 11_03)
- `You're just a little detour, so don't worry.` -> `Você é só um pequeno desvio, então não se preocupe.` (Kuon, 11_03)
- `Oh yeah?` -> `Ah, é?` (Haku, 11_03)
- `Yes. It's not a focused journey, anyway.\n` -> `Sim. Não é uma viagem com rumo certo, de todo jeito.\n` (Kuon, 11_03)
- `I just go wherever the day takes me, you know?` -> `Eu só vou aonde o dia me levar, sabe?` (Kuon, 11_03)
- `Of course, there is something I'd like to\n` -> `Claro, tem uma coisa que eu gostaria de\n` (Kuon, 11_03)
- `accomplish, but it's nothing too urgent.` -> `realizar, mas não é nada muito urgente.` (Kuon, 11_03)
- `Most of all, I just want to feel the air of new\n` -> `Mais do que tudo, eu só quero sentir o ar de novas\n` (Kuon, 11_03)
- `lands. See and hear things I've never experienced.` -> `terras. Ver e ouvir coisas que nunca vivi.` (Kuon, 11_03)
- `Do things I can only do now...\n` -> `Fazer coisas que só posso fazer agora...\n` (Kuon, 11_03)
- `so I won't have any regrets.` -> `pra não ter nenhum arrependimento.` (Kuon, 11_03)
- `She speaks while staring ahead, somewhere off\n` -> `Ela fala olhando pra frente, pra algum lugar\n` (Haku, 11_03)
- `in the distance... ` -> `lá longe... ` (Haku, 11_03)
- `Still, whatever the reason may be... A young girl\n` -> `Mesmo assim, seja qual for o motivo... Uma garota\n` (Haku, 11_03)
- `like her out on some trip all by herself...?` -> `como ela viajando sozinha por aí...?` (Haku, 11_03)
- `There's a lot of danger out here. I learned that\n` -> `Tem muito perigo por aqui. Eu aprendi isso\n` (Haku, 11_03)
- `myself just yesterday...` -> `na pele ainda ontem...` (Haku, 11_03)
- `I could understand if it were just paved city\n` -> `Até entenderia se fossem só ruas asfaltadas\n` (Haku, 11_03)
- `streets, but hiking over this huge mountain?\n` -> `de cidade, mas atravessar essa montanha enorme a pé?\n` (Haku, 11_03)
- `I dunno.` -> `Sei lá.` (Haku, 11_03)
- `You know...` -> `Sabe...` (Haku, 11_03)
- `I'm about to bring up my concerns...` -> `Estou prestes a falar das minhas preocupações...` (Haku, 11_03)
- `...but Kuon suddenly comes to a halt. She extends\n` -> `...mas a Kuon para de repente. Ela estende\n` (Haku, 11_03)
- `her arm to the side, signaling for me to stop.` -> `o braço pro lado, sinalizando pra eu parar.` (Haku, 11_03)
- `GRRRR...` -> `GRRRR...` (toriuma, 11_03)
- `What the--` -> `Mas que--` (Haku, 11_03)
- `Wild dogs...? No, wolves? I'm no biologist, but\n` -> `Cães selvagens...? Não, lobos? Não sou biólogo, mas\n` (Haku, 11_03)
- `it's safe to say they're something close...` -> `dá pra dizer que são algo parecido...` (Haku, 11_03)
- `H-Hey!! What do we do!?` -> `E-Ei!! O que a gente faz!?` (Haku, 11_03)
- `Do about... what?` -> `Fazer... sobre o quê?` (Kuon, 11_03)
- `Ah, I get it! I think you'll be fine. These\n` -> `Ah, entendi! Acho que você vai ficar bem. Esses\n` (Kuon, 11_03)
- `aren't much to worry about.` -> `não são nada de mais.` (Kuon, 11_03)
- `Y-You think?` -> `V-Você acha?` (Haku, 11_03)
- `Sure. Just wave a stick around, and they'll scatter.` -> `Claro. É só balançar um graveto e eles se espalham.` (Kuon, 11_03)
- `Still, they're coming at us. Well, this is\n` -> `Mesmo assim, eles estão vindo pra cima. Bom, que\n` (Kuon, 11_03)
- `annoying...` -> `saco...` (Kuon, 11_03)
- `Let me just drive them off. It shouldn't take too\n` -> `Deixa que eu enxoto eles. Não deve demorar\n` (Kuon, 11_03)
- `long.` -> `muito.` (Kuon, 11_03)
- `Nah, let me give you a hand.` -> `Que nada, deixa eu te ajudar.` (Haku, 11_03)
- `Heh heh heh... Up til now, I've had it pretty rough.\n` -> `Hehehe... Até agora, a coisa tava bem pesada pro meu lado.\n` (Haku, 11_03)
- `Sorry, guys, but it's time for some stress relief.` -> `Foi mal, rapazes, mas chegou a hora de aliviar o estresse.` (Haku, 11_03)
- `Head_toriuma` -> `Head_toriuma` (rotulo, 11_03)
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
| 0x1436a | 31 | Geez...! Too bright out here... |
| 0x1438a | 49 | Well, guess the sun still rises no matter where\n |
| 0x143bc | 47 | I am. Still... What am I supposed to do now...? |
| 0x143ec | 30 | How are you feeling, I wonder? |
| 0x1440b | 7 | Huh...? |
| 0x14413 | 47 | I glance back at the sudden question, and see\n |
| 0x14443 | 22 | Kuon making breakfast. |
| 0x1445a | 53 | I didn't really see any external signs of injuries,\n |
| 0x14490 | 35 | but you can never be too careful... |
| 0x144b4 | 17 | I guess I feel... |
| 0x144c6 | 52 | It's true that I was in a coma when Kuon found me.\n |
| 0x144fb | 48 | And then getting chased down by huge monsters... |
| 0x1452c | 53 | So I try stretching my shoulders, and crack my neck\n |
| 0x14562 | 32 | with a couple twists of my head. |
| 0x14583 | 43 | ...Well, seems like everything still works. |
| 0x145af | 12 | You're sure? |
| 0x145bc | 49 | Yeah, I'm fine. It's just muscle ache more than\n |
| 0x145ee | 22 | anything else, really. |
| 0x14605 | 51 | My offhanded dismissal seems to get a giggle from\n |
| 0x14639 | 44 | Kuon. Maybe I tried too hard to sound macho. |
| 0x14666 | 46 | I'm relieved to hear that. Then, let's leave\n |
| 0x14695 | 26 | after breakfast, shall we? |
| 0x146b0 | 12 | Wait, leave? |
| 0x146bd | 15 | Leave to where? |
| 0x146cd | 49 | Staying here would be a bad idea, so we'll head\n |
| 0x146ff | 25 | to a village just nearby. |
| 0x14719 | 14 | So it's close? |
| 0x14728 | 22 | Yup, walking distance. |
| 0x1473f | 34 | I see... I mean, I just thought... |
| 0x14762 | 17 | You thought what? |
| 0x14774 | 39 | I kind of figured you lived here, Kuon. |
| 0x1479c | 45 | Oh, so I suppose I look like some backwoods\n |
| 0x147ca | 50 | hermit who lives up in the mountains? Is that it?  |
| 0x147fd | 43 | Kuon's eyes narrow, her gaze fixed on me... |
| 0x14829 | 48 | Well, don't let me stop you. If you want us to\n |
| 0x1485a | 46 | live in a tent, then by all means. How about\n |
| 0x14889 | 9 | it, Haku? |
| 0x14893 | 49 | It sounds like a joke when she says it, but her\n |
| 0x148c5 | 31 | smile doesn't reach her eyes... |
| 0x148e5 | 41 | W-Wait, hold on! That's not what I meant! |
| 0x1490f | 26 | Ahaha... It's just a joke. |
| 0x1492a | 47 | I just stopped by, since I'm on my journey...\n |
| 0x1495a | 47 | but now that you're here, we'd better head to\n |
| 0x1498a | 7 | a town. |
| 0x14992 | 17 | A journey, huh... |
| 0x149a4 | 45 | ...Well, maybe someone at the village might\n |
| 0x149d2 | 19 | know more about me. |
| 0x149e6 | 44 | Who knows? Maybe this is all it'll take to\n |
| 0x14a13 | 14 | clear this up. |
| 0x14a22 | 44 | OK then... while I'm working on breakfast,\n |
| 0x14a4f | 43 | can you load him up with our baggage, Haku? |
| 0x14a7b | 4 | Head |
| 0x14a80 | 9 | ..."Him"? |
| 0x14a8a | 24 | I tilt my head, bemused. |
| 0x14aa3 | 44 | Well, I don't see anyone around except us... |
| 0x14ad0 | 8 | GREHHHH! |
| 0x14ad9 | 6 | HOLY-- |
| 0x14ae0 | 48 | Wh-What the heck is this ostrich-looking thing!? |
| 0x14b11 | 51 | I don't know if Ostrich Prime here thinks I'm its\n |
| 0x14b45 | 51 | dinner, but it keeps trying to take a bite out of\n |
| 0x14b79 | 5 | me... |
| 0x14b7f | 48 | Ostrich? I don't know what you mean. He's just\n |
| 0x14bb0 | 9 | my steed. |
| 0x14bba | 29 | Steed...? What, like a horse? |
| 0x14bd8 | 48 | How could this thing be a--well, no, just look\n |
| 0x14c09 | 51 | at Kuon... I guess if she says it's a horse, it is. |
| 0x14c3d | 47 | ...God, I can feel common sense draining away\n |
| 0x14c6d | 34 | with every minute I spend here...  |
| 0x14c90 | 48 | After breakfast, we pack up the tent, and with\n |
| 0x14cc1 | 45 | the sun low in the sky, we set off. With an\n |
| 0x14cef | 8 | ostrich. |
| 0x14cf8 | 33 | By the way, is this really... OK? |
| 0x14d1a | 31 | What could that mean, I wonder? |
| 0x14d3a | 40 | Well, you said you're on some journey.\n |
| 0x14d63 | 49 | I hope I'm not messing up any of your plans here. |
| 0x14d95 | 40 | Kuon responds easily, like it's nothing. |
| 0x14dbe | 54 | I didn't come to this forest for anything important.\n |
| 0x14df5 | 44 | You're just a little detour, so don't worry. |
| 0x14e22 | 8 | Oh yeah? |
| 0x14e2b | 42 | Yes. It's not a focused journey, anyway.\n |
| 0x14e56 | 46 | I just go wherever the day takes me, you know? |
| 0x14e85 | 43 | Of course, there is something I'd like to\n |
| 0x14eb1 | 40 | accomplish, but it's nothing too urgent. |
| 0x14eda | 49 | Most of all, I just want to feel the air of new\n |
| 0x14f0c | 50 | lands. See and hear things I've never experienced. |
| 0x14f3f | 32 | Do things I can only do now...\n |
| 0x14f60 | 28 | so I won't have any regrets. |
| 0x14f7d | 47 | She speaks while staring ahead, somewhere off\n |
| 0x14fad | 19 | in the distance...  |
| 0x14fc1 | 51 | Still, whatever the reason may be... A young girl\n |
| 0x14ff5 | 44 | like her out on some trip all by herself...? |
| 0x15022 | 50 | There's a lot of danger out here. I learned that\n |
| 0x15055 | 24 | myself just yesterday... |
| 0x1506e | 47 | I could understand if it were just paved city\n |
| 0x1509e | 46 | streets, but hiking over this huge mountain?\n |
| 0x150cd | 8 | I dunno. |
| 0x150d6 | 11 | You know... |
| 0x150e2 | 36 | I'm about to bring up my concerns... |
| 0x15107 | 51 | ...but Kuon suddenly comes to a halt. She extends\n |
| 0x1513b | 46 | her arm to the side, signaling for me to stop. |
| 0x1516a | 8 | GRRRR... |
| 0x15173 | 10 | What the-- |
| 0x1517e | 49 | Wild dogs...? No, wolves? I'm no biologist, but\n |
| 0x151b0 | 43 | it's safe to say they're something close... |
| 0x151dc | 23 | H-Hey!! What do we do!? |
| 0x151f4 | 17 | Do about... what? |
| 0x15206 | 45 | Ah, I get it! I think you'll be fine. These\n |
| 0x15234 | 27 | aren't much to worry about. |
| 0x15250 | 12 | Y-You think? |
| 0x1525d | 52 | Sure. Just wave a stick around, and they'll scatter. |
| 0x15292 | 44 | Still, they're coming at us. Well, this is\n |
| 0x152bf | 11 | annoying... |
| 0x152cb | 51 | Let me just drive them off. It shouldn't take too\n |
| 0x152ff | 5 | long. |
| 0x15305 | 28 | Nah, let me give you a hand. |
| 0x15322 | 54 | Heh heh heh... Up til now, I've had it pretty rough.\n |
| 0x15359 | 50 | Sorry, guys, but it's time for some stress relief. |
| 0x1538c | 12 | Head_toriuma |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_03.json` com a forma:
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
