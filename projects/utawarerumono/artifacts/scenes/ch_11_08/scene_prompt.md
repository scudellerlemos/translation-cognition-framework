# Cena ch_11_08 — pacote de traducao (146 linhas)

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
| amam | Item | amam | manter_original | none |
| Bonus Points | UI | Pontos de Bonus | traduzir | none |
| Free Battle | UI | Batalha Livre | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| kinujiku | Item | kinujiku | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| sainaina | Item | sainaina | manter_original | none |
| sen | Moeda | sen | manter_original | none |
| shyakuni | Item | shyakuni | manter_original | none |
| yacchip | Item | yacchip | manter_original | none |

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
- `We finished moving them to the mill, ma'am.` -> `Terminamos de levá-los ao moinho, senhora.` (Kuon, 11_08)
- `Innkeeper` -> `Estalajadeira` (rotulo, 11_06)
- `Welcome back, you two. Thanks for taking care of\n` -> `Bem-vindos de volta, vocês dois. Obrigada por cuidarem\n` (Estalajadeira, 11_08)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `You were gone longer than I thought you'd be,\n` -> `Vocês demoraram mais do que eu esperava,\n` (Estalajadeira, 11_08)
- `though. Did something happen?` -> `no entanto. Aconteceu alguma coisa?` (Estalajadeira, 11_08)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `I slowed us down, obviously...` -> `Eu atrasei a gente, obviamente...` (Haku, 11_08)
- `We took a little detour, is all. I thought I'd show\n` -> `A gente deu uma volta, só isso. Pensei em mostrar\n` (Kuon, 11_08)
- `Haku around the village.` -> `a vila pro Haku.` (Kuon, 11_08)
- `Is that so? We're a small town at best, so there's\n` -> `É mesmo? Somos uma vila pequena no máximo, então não há\n` (Estalajadeira, 11_08)
- `not much to show, I'm afraid.` -> `muito o que mostrar, infelizmente.` (Estalajadeira, 11_08)
- `Oh, but I like it here! It reminds me of a place\n` -> `Ah, mas eu gosto daqui! Me lembra um lugar\n` (Haku, 11_08)
- `from my childhood. It's a nice feeling.` -> `da minha infância. É uma sensação boa.` (Haku, 11_08)
- `Ahaha, what a sweet thing to say! Now, let me tally\n` -> `Ahaha, que coisa fofa de se dizer! Bom, deixa eu somar\n` (Estalajadeira, 11_08)
- `up your bill...` -> `a sua conta...` (Estalajadeira, 11_08)
- `450 sen for the shyakuni I asked for, 338 for the\n` -> `450 sen pelo shyakuni que pedi, 338 pela\n` (Estalajadeira, 11_08)
- `sainaina grass... yacchip mushrooms, 313 sen...` -> `erva sainaina... cogumelos yacchip, 313 sen...` (Estalajadeira, 11_08)
- `...and the kinujiku berries are 243 sen.` -> `...e as frutinhas kinujiku são 243 sen.` (Estalajadeira, 11_08)
- `The innkeeper lines up a handful of stick-like\n` -> `A estalajadeira alinha um punhado de objetos\n` (Haku, 11_08)
- `objects as she speaks...` -> `parecidos com varetas enquanto fala...` (Haku, 11_08)
- `A calculator, I guess? It's an awfully primitive\n` -> `Uma calculadora, eu acho? É uma bem primitiva,\n` (Haku, 11_08)
- `one, though...` -> `no entanto...` (Haku, 11_08)
- `And 3 sen each for those grain bags, times eight\n` -> `E 3 sen por cada saco de grãos, vezes oito\n` (Estalajadeira, 11_08)
- `is... 24 sen.` -> `dá... 24 sen.` (Estalajadeira, 11_08)
- `3 sen...` -> `3 sen...` (Haku, 11_08)
- `Seems like a pitiful amount next to the rest.\n` -> `Parece uma quantia ridícula perto do resto.\n` (Haku, 11_08)
- `I guess it really is just pocket money for kids.` -> `Acho que é trocado de criança mesmo.` (Haku, 11_08)
- `Lodgings for the night are 720 sen, and... what\n` -> `A hospedagem da noite são 720 sen, e... o que\n` (Estalajadeira, 11_08)
- `will you be doing for food?` -> `vocês vão querer de comida?` (Estalajadeira, 11_08)
- `Please include that, as well.` -> `Inclua isso também, por favor.` (Kuon, 11_08)
- `For two people, food is 80 sen, which brings\n` -> `Para duas pessoas, a comida são 80 sen, o que leva\n` (Estalajadeira, 11_08)
- `your total bill to 800.` -> `sua conta total a 800.` (Estalajadeira, 11_08)
- `Then, ah... subtracting 800 from the total for the\n` -> `Então, ah... subtraindo 800 do total das\n` (Estalajadeira, 11_08)
- `herbs I bought from you...` -> `ervas que comprei de vocês...` (Estalajadeira, 11_08)
- `568 sen.` -> `568 sen.` (Haku, 11_08)
- `...It's 557 sen, I think.` -> `...São 557 sen, eu acho.` (Kuon, 11_08)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `No, it's 568.` -> `Não, são 568.` (Haku, 11_08)
- `450 + 338 + 313 + 243 + 24 - 800 is 568.\n` -> `450 + 338 + 313 + 243 + 24 - 800 dá 568.\n` (Haku, 11_08)
- `There's no mistaking it.` -> `Não tem como errar.` (Haku, 11_08)
- `Ahaha! Sorry, Haku, but you're off by a bit. I may\n` -> `Ahaha! Desculpa, Haku, mas você errou um pouquinho. Posso\n` (Kuon, 11_08)
- `not look it, but I'm pretty good with numbers.` -> `não parecer, mas sou bem boa com números.` (Kuon, 11_08)
- `I can do mental calculations like this easily--even\n` -> `Faço cálculos de cabeça com facilidade--até\n` (Kuon, 11_08)
- `with my eyes closed!` -> `de olhos fechados!` (Kuon, 11_08)
- `...I don't think it matters whether your eyes are\n` -> `...Não acho que importa se os seus olhos estão\n` (Haku, 11_08)
- `open or not.` -> `abertos ou não.` (Haku, 11_08)
- `The answer is 557 sen. You'll see.` -> `A resposta é 557 sen. Você vai ver.` (Kuon, 11_08)
- `...carry the one, and... I owe you 568 sen.` -> `...vai um, e... devo a vocês 568 sen.` (Estalajadeira, 11_08)
- `The innkeeper looks up from the calculating sticks.` -> `A estalajadeira ergue os olhos das varetas de cálculo.` (Haku, 11_08)
- `...\n` -> `...\n` (Haku, 11_08)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Here--please take this.` -> `Aqui--por favor, pegue.` (Estalajadeira, 11_08)
- `The innkeeper fills a pouch with various different\n` -> `A estalajadeira enche uma bolsa com moedas de\n` (Haku, 11_08)
- `sized coins, holding it out toward Kuon.` -> `tamanhos variados e a estende em direção à Kuon.` (Haku, 11_08)
- `Kuon's face gradually reddens.` -> `O rosto da Kuon vai ficando vermelho aos poucos.` (Haku, 11_08)
- `I-I, uhm--d-didn't mean--what I MEANT to say was...\n` -> `E-Eu, ã--n-não quis dizer--o que eu QUIS dizer era...\n` (Kuon, 11_08)
- `I-It was just a tiny error!` -> `F-Foi só um errinho minúsculo!` (Kuon, 11_08)
- `Why are you getting so worked up? Everyone makes\n` -> `Por que você tá ficando tão nervosa? Todo mundo comete\n` (Haku, 11_08)
- `careless mistakes.` -> `erros bobos.` (Haku, 11_08)
- `L-Like I said, I didn't make a mistake! I was just\n` -> `C-Como eu disse, eu não errei! Eu só fui\n` (Kuon, 11_08)
- `careless, is all!` -> `descuidada, só isso!` (Kuon, 11_08)
- `Th-That's right, everyone makes mistakes. It can't\n` -> `I-Isso mesmo, todo mundo comete erros. Não tem\n` (Estalajadeira, 11_08)
- `be helped...` -> `como evitar...` (Estalajadeira, 11_08)
- `But that was... unexpected, Haku. I didn't know you\n` -> `Mas isso foi... inesperado, Haku. Não sabia que você\n` (Kuon, 11_08)
- `could do calculations on the fly like that.` -> `conseguia fazer contas de cabeça desse jeito.` (Kuon, 11_08)
- `Unexpected? That was a simple one. No big deal.` -> `Inesperado? Foi uma conta simples. Nada de mais.` (Haku, 11_08)
- `If that's your idea of "simple"... Are you good at\n` -> `Se isso é o que você chama de "simples"... Você é bom de\n` (Kuon, 11_08)
- `arithmetic, Haku?` -> `conta, Haku?` (Kuon, 11_08)
- `I don't know about "good." I mean, it's just math,\n` -> `Não sei se "bom". Quer dizer, é só conta, né?\n` (Haku, 11_08)
- `right? Anyone could have solved that.` -> `Qualquer um teria resolvido aquilo.` (Haku, 11_08)
- `While Kuon may be smiling at me, her eyebrows are\n` -> `Mesmo a Kuon sorrindo pra mim, as sobrancelhas dela\n` (Haku, 11_08)
- `twitching slightly...` -> `tremem de leve...` (Haku, 11_08)
- `I mean, uh... never mind.` -> `Quer dizer, ahn... deixa pra lá.` (Kuon, 11_08)
- `Could you follow me for a second?` -> `Pode me seguir um segundo?` (Kuon, 11_08)
- `Kuon grabs my hand and pulls me along before I can\n` -> `A Kuon agarra minha mão e me puxa antes que eu\n` (Haku, 11_08)
- `give an answer.` -> `consiga responder.` (Haku, 11_08)
- `Hey, wait--` -> `Ei, espera--` (Haku, 11_08)
- `Just come with me. If you can do that much in your\n` -> `Vem comigo. Se você faz tudo isso de cabeça, quero ver\n` (Kuon, 11_08)
- `head, I want to see how you do with REAL problems.` -> `como você se sai com problemas DE VERDADE.` (Kuon, 11_08)
- `As soon as we enter the room, Kuon reaches for a\n` -> `Assim que entramos no quarto, a Kuon vai até um\n` (Haku, 11_08)
- `trunk and starts digging through her belongings.` -> `baú e começa a remexer nos próprios pertences.` (Haku, 11_08)
- `I was sure I put it away somewhere here...` -> `Tinha certeza que tinha guardado em algum lugar aqui...` (Kuon, 11_08)
- `With her head thrust into her luggage, all I can see\n` -> `Com a cabeça enfiada na bagagem, tudo que dá pra ver\n` (Haku, 11_08)
- `is her butt in the air and her tail wagging.` -> `é o traseiro dela no ar e o rabo balançando.` (Haku, 11_08)
- `There it is. Hmhm, let's see how he deals with\n` -> `Achei. Hmhm, vamos ver como ele se sai com\n` (Kuon, 11_08)
- `this...` -> `isto...` (Kuon, 11_08)
- `Kuon produces a large notebook from her bags,\n` -> `A Kuon tira um caderno grande da bagagem,\n` (Haku, 11_08)
- `thrusting it toward me with a smug smile.` -> `empurrando na minha direção com um sorriso convencido.` (Haku, 11_08)
- `What's that?` -> `O que é isso?` (Haku, 11_08)
- `Puzzled, I glance between the plain looking notebook\n` -> `Confuso, olho do caderno de aparência comum\n` (Haku, 11_08)
- `and Kuon's expectant face...` -> `para o rosto expectante da Kuon...` (Haku, 11_08)
- `Kuon just smiles, wiggling the notebook.` -> `A Kuon só sorri, balançando o caderno.` (Haku, 11_08)
- `Does she want me to read it?` -> `Será que ela quer que eu leia?` (Haku, 11_08)
- `I go ahead and take it from her, opening it to the\n` -> `Vou em frente e pego dela, abrindo na\n` (Haku, 11_08)
- `first page...` -> `primeira página...` (Haku, 11_08)
- `A complex array of numbers and symbols greets me\n` -> `Um arranjo complexo de números e símbolos me recebe\n` (Haku, 11_08)
- `there, all symmetrically lined up.` -> `ali, tudo alinhado simetricamente.` (Haku, 11_08)
- `Mathematical formulae, huh...?` -> `Fórmulas matemáticas, né...?` (Haku, 11_08)
- `They all look to be fairly simple arithmetic, in\n` -> `Parece tudo aritmética bem simples, numa\n` (Haku, 11_08)
- `cute, stylized handwriting.` -> `letra fofa e estilizada.` (Haku, 11_08)
- `Each unfinished equation has a space beneath to\n` -> `Cada equação incompleta tem um espaço embaixo pra\n` (Haku, 11_08)
- `write in an answer...` -> `escrever a resposta...` (Haku, 11_08)
- `And the opposite page, strangely adorable animals\n` -> `E na página oposta, bichinhos estranhamente fofos\n` (Haku, 11_08)
- `give hints on how to solve each problem.` -> `dão dicas de como resolver cada problema.` (Haku, 11_08)
- `Flipping through the rest of the notebook, I find\n` -> `Folheando o resto do caderno, encontro\n` (Haku, 11_08)
- `more of the same--equations and cute drawings.` -> `mais do mesmo--equações e desenhos fofos.` (Haku, 11_08)
- `I see... So it's an arithmetic workbook.` -> `Saquei... Então é um caderno de continhas.` (Haku, 11_08)
- `They're all fairly simple problems, but the book\n` -> `São todos problemas bem simples, mas o caderno\n` (Haku, 11_08)
- `itself is a handmade, painstakingly handwritten piece.` -> `em si é feito a mão, escrito com muito capricho.` (Haku, 11_08)
- `What do you think? I've been learning high\n` -> `O que você acha? Eu venho aprendendo matemática de\n` (Kuon, 11_08)
- `level mathematics from this book.` -> `alto nível com este livro.` (Kuon, 11_08)
- `I glance up from the page to find Kuon puffing out\n` -> `Ergo os olhos da página e vejo a Kuon estufar\n` (Haku, 11_08)
- `her chest proudly.` -> `o peito com orgulho.` (Haku, 11_08)
- `See if you can work through THESE problems, eh?\n` -> `Vê se você consegue resolver ESTES problemas, hein?\n` (Kuon, 11_08)
- `The tough stuff.` -> `Os mais difíceis.` (Kuon, 11_08)
- `I don't really get why, but if she wants me to try\n` -> `Não entendo bem por quê, mas se ela quer que eu tente\n` (Haku, 11_08)
- `solving these... Let's see.` -> `resolver isso... Vamos ver.` (Haku, 11_08)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `W-Wait, Haku, are y--` -> `E-Espera, Haku, você tá--` (Kuon, 11_08)
- `Hm? What, you don't want me to solve these?` -> `Hum? Que foi, você não quer que eu resolva?` (Haku, 11_08)
- `I... I did, but--were those... answers? Are you doing\n` -> `E-Eu queria, mas--aquilo eram... respostas? Você está\n` (Kuon, 11_08)
- `all this just in your head?` -> `fazendo tudo isso só de cabeça?` (Kuon, 11_08)
- `Well, they're all pretty simple.` -> `Bom, são todos bem simples.` (Haku, 11_08)
- `It can't be... Problems of that difficulty, they're\n` -> `Não pode ser... Problemas dessa dificuldade,\n` (Kuon, 11_08)
- `supposed to be...` -> `eles deveriam ser...` (Kuon, 11_08)
- `"Of that difficulty"? That's a bit much. This is\n` -> `"Dessa dificuldade"? Isso é exagero. Esse material é\n` (Haku, 11_08)
- `pretty easy material.` -> `bem fácil.` (Haku, 11_08)
- `Anyone would be able to solve these. Or is my\n` -> `Qualquer um conseguiria resolver. Ou será que minha\n` (Haku, 11_08)
- `perception just different from hers?` -> `percepção é só diferente da dela?` (Haku, 11_08)
- `So, what now? Want me to keep going?` -> `E então? Quer que eu continue?` (Haku, 11_08)
- `Huh? Ah, hold on--` -> `Hein? Ah, espera--` (Kuon, 11_08)
- `Kuon rifles through her bags once more and retrieves\n` -> `A Kuon vasculha a bagagem de novo e tira um\n` (Haku, 11_08)
- `a long, stick-like object...` -> `objeto comprido, parecido com uma vareta...` (Haku, 11_08)
- `...A pencil?` -> `...Um lápis?` (Haku, 11_08)
- `First... 43, 1338, 6084, 55...` -> `Primeiro... 43, 1338, 6084, 55...` (Haku, 11_08)
- `*Scribble, scribble*...` -> `*Rabisco, rabisco*...` (Haku, 11_08)
- `Hey, how about the next one?` -> `Ei, e que tal o próximo?` (Kuon, 11_08)
- `Kuon prompts me, taking the notebook. Seems like\n` -> `A Kuon me incentiva, pegando o caderno. Parece\n` (Haku, 11_08)
- `she's in a good mood for some reason...` -> `estar de bom humor por algum motivo...` (Haku, 11_08)
- `The next one? Uh, 5126.` -> `O próximo? Ah, 5126.` (Haku, 11_08)
- `{c5}Free Battle{c-1} has been added to the system menu.` -> `{c5}Batalha Livre{c-1} adicionada ao menu do sistema.` (Sistema, 11_08)
- `You can replay cleared stages in Free Battle mode.` -> `Você pode rejogar fases concluídas no modo Batalha Livre.` (Sistema, 11_08)
- `Do this at base, or whenever you're organizing for\n` -> `Faça isso na base, ou quando estiver se organizando para a\n` (Sistema, 11_08)
- `battle. Fight, level up, and collect Bonus Points!` -> `batalha. Lute, suba de nível e junte Pontos de Bônus!` (Sistema, 11_08)
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
| 0x1c79d | 43 | We finished moving them to the mill, ma'am. |
| 0x1c7c9 | 9 | Innkeeper |
| 0x1c7d3 | 50 | Welcome back, you two. Thanks for taking care of\n |
| 0x1c806 | 5 | that. |
| 0x1c80c | 47 | You were gone longer than I thought you'd be,\n |
| 0x1c83c | 29 | though. Did something happen? |
| 0x1c85a | 7 | Nngh... |
| 0x1c862 | 30 | I slowed us down, obviously... |
| 0x1c881 | 53 | We took a little detour, is all. I thought I'd show\n |
| 0x1c8b7 | 24 | Haku around the village. |
| 0x1c8d0 | 52 | Is that so? We're a small town at best, so there's\n |
| 0x1c905 | 29 | not much to show, I'm afraid. |
| 0x1c923 | 50 | Oh, but I like it here! It reminds me of a place\n |
| 0x1c956 | 39 | from my childhood. It's a nice feeling. |
| 0x1c97e | 53 | Ahaha, what a sweet thing to say! Now, let me tally\n |
| 0x1c9b4 | 15 | up your bill... |
| 0x1c9c4 | 51 | 450 sen for the shyakuni I asked for, 338 for the\n |
| 0x1c9f8 | 47 | sainaina grass... yacchip mushrooms, 313 sen... |
| 0x1ca28 | 40 | ...and the kinujiku berries are 243 sen. |
| 0x1ca51 | 48 | The innkeeper lines up a handful of stick-like\n |
| 0x1ca82 | 24 | objects as she speaks... |
| 0x1ca9b | 50 | A calculator, I guess? It's an awfully primitive\n |
| 0x1cace | 14 | one, though... |
| 0x1cadd | 50 | And 3 sen each for those grain bags, times eight\n |
| 0x1cb10 | 13 | is... 24 sen. |
| 0x1cb1e | 8 | 3 sen... |
| 0x1cb27 | 47 | Seems like a pitiful amount next to the rest.\n |
| 0x1cb57 | 48 | I guess it really is just pocket money for kids. |
| 0x1cb88 | 49 | Lodgings for the night are 720 sen, and... what\n |
| 0x1cbba | 27 | will you be doing for food? |
| 0x1cbd6 | 29 | Please include that, as well. |
| 0x1cbf4 | 46 | For two people, food is 80 sen, which brings\n |
| 0x1cc23 | 23 | your total bill to 800. |
| 0x1cc3b | 52 | Then, ah... subtracting 800 from the total for the\n |
| 0x1cc70 | 26 | herbs I bought from you... |
| 0x1cc8b | 8 | 568 sen. |
| 0x1cc94 | 25 | ...It's 557 sen, I think. |
| 0x1ccae | 6 | ...Hm? |
| 0x1ccb5 | 3 | Hm? |
| 0x1ccb9 | 13 | No, it's 568. |
| 0x1ccc7 | 42 | 450 + 338 + 313 + 243 + 24 - 800 is 568.\n |
| 0x1ccf2 | 24 | There's no mistaking it. |
| 0x1cd0b | 52 | Ahaha! Sorry, Haku, but you're off by a bit. I may\n |
| 0x1cd40 | 46 | not look it, but I'm pretty good with numbers. |
| 0x1cd6f | 53 | I can do mental calculations like this easily--even\n |
| 0x1cda5 | 20 | with my eyes closed! |
| 0x1cdba | 51 | ...I don't think it matters whether your eyes are\n |
| 0x1cdee | 12 | open or not. |
| 0x1cdfb | 34 | The answer is 557 sen. You'll see. |
| 0x1ce1e | 43 | ...carry the one, and... I owe you 568 sen. |
| 0x1ce4a | 51 | The innkeeper looks up from the calculating sticks. |
| 0x1ce7e | 5 | ...\n |
| 0x1ce84 | 7 | ...Huh? |
| 0x1ce8c | 23 | Here--please take this. |
| 0x1cea4 | 52 | The innkeeper fills a pouch with various different\n |
| 0x1ced9 | 40 | sized coins, holding it out toward Kuon. |
| 0x1cf06 | 30 | Kuon's face gradually reddens. |
| 0x1cf25 | 53 | I-I, uhm--d-didn't mean--what I MEANT to say was...\n |
| 0x1cf5b | 27 | I-It was just a tiny error! |
| 0x1cf77 | 50 | Why are you getting so worked up? Everyone makes\n |
| 0x1cfaa | 18 | careless mistakes. |
| 0x1cfbd | 52 | L-Like I said, I didn't make a mistake! I was just\n |
| 0x1cff2 | 17 | careless, is all! |
| 0x1d004 | 52 | Th-That's right, everyone makes mistakes. It can't\n |
| 0x1d039 | 12 | be helped... |
| 0x1d046 | 53 | But that was... unexpected, Haku. I didn't know you\n |
| 0x1d07c | 43 | could do calculations on the fly like that. |
| 0x1d0a8 | 47 | Unexpected? That was a simple one. No big deal. |
| 0x1d0d8 | 52 | If that's your idea of "simple"... Are you good at\n |
| 0x1d10d | 17 | arithmetic, Haku? |
| 0x1d11f | 52 | I don't know about "good." I mean, it's just math,\n |
| 0x1d154 | 37 | right? Anyone could have solved that. |
| 0x1d17a | 51 | While Kuon may be smiling at me, her eyebrows are\n |
| 0x1d1ae | 21 | twitching slightly... |
| 0x1d1c4 | 25 | I mean, uh... never mind. |
| 0x1d1de | 33 | Could you follow me for a second? |
| 0x1d200 | 52 | Kuon grabs my hand and pulls me along before I can\n |
| 0x1d235 | 15 | give an answer. |
| 0x1d245 | 11 | Hey, wait-- |
| 0x1d251 | 52 | Just come with me. If you can do that much in your\n |
| 0x1d286 | 50 | head, I want to see how you do with REAL problems. |
| 0x1d2b9 | 50 | As soon as we enter the room, Kuon reaches for a\n |
| 0x1d2ec | 48 | trunk and starts digging through her belongings. |
| 0x1d31d | 42 | I was sure I put it away somewhere here... |
| 0x1d348 | 54 | With her head thrust into her luggage, all I can see\n |
| 0x1d37f | 44 | is her butt in the air and her tail wagging. |
| 0x1d3ac | 48 | There it is. Hmhm, let's see how he deals with\n |
| 0x1d3dd | 7 | this... |
| 0x1d3e5 | 47 | Kuon produces a large notebook from her bags,\n |
| 0x1d415 | 41 | thrusting it toward me with a smug smile. |
| 0x1d43f | 12 | What's that? |
| 0x1d44c | 54 | Puzzled, I glance between the plain looking notebook\n |
| 0x1d483 | 28 | and Kuon's expectant face... |
| 0x1d4a0 | 40 | Kuon just smiles, wiggling the notebook. |
| 0x1d4c9 | 28 | Does she want me to read it? |
| 0x1d4e6 | 52 | I go ahead and take it from her, opening it to the\n |
| 0x1d51b | 13 | first page... |
| 0x1d529 | 50 | A complex array of numbers and symbols greets me\n |
| 0x1d55c | 34 | there, all symmetrically lined up. |
| 0x1d57f | 30 | Mathematical formulae, huh...? |
| 0x1d59e | 50 | They all look to be fairly simple arithmetic, in\n |
| 0x1d5d1 | 27 | cute, stylized handwriting. |
| 0x1d5ed | 49 | Each unfinished equation has a space beneath to\n |
| 0x1d61f | 21 | write in an answer... |
| 0x1d635 | 51 | And the opposite page, strangely adorable animals\n |
| 0x1d669 | 40 | give hints on how to solve each problem. |
| 0x1d692 | 51 | Flipping through the rest of the notebook, I find\n |
| 0x1d6c6 | 46 | more of the same--equations and cute drawings. |
| 0x1d6f5 | 40 | I see... So it's an arithmetic workbook. |
| 0x1d71e | 50 | They're all fairly simple problems, but the book\n |
| 0x1d751 | 54 | itself is a handmade, painstakingly handwritten piece. |
| 0x1d788 | 44 | What do you think? I've been learning high\n |
| 0x1d7b5 | 33 | level mathematics from this book. |
| 0x1d7d7 | 52 | I glance up from the page to find Kuon puffing out\n |
| 0x1d80c | 18 | her chest proudly. |
| 0x1d81f | 49 | See if you can work through THESE problems, eh?\n |
| 0x1d851 | 16 | The tough stuff. |
| 0x1d862 | 52 | I don't really get why, but if she wants me to try\n |
| 0x1d897 | 27 | solving these... Let's see. |
| 0x1d8b7 | 4 | Huh? |
| 0x1d8d2 | 21 | W-Wait, Haku, are y-- |
| 0x1d8e8 | 43 | Hm? What, you don't want me to solve these? |
| 0x1d914 | 55 | I... I did, but--were those... answers? Are you doing\n |
| 0x1d94c | 27 | all this just in your head? |
| 0x1d968 | 32 | Well, they're all pretty simple. |
| 0x1d989 | 53 | It can't be... Problems of that difficulty, they're\n |
| 0x1d9bf | 17 | supposed to be... |
| 0x1d9d1 | 50 | "Of that difficulty"? That's a bit much. This is\n |
| 0x1da04 | 21 | pretty easy material. |
| 0x1da1a | 47 | Anyone would be able to solve these. Or is my\n |
| 0x1da4a | 36 | perception just different from hers? |
| 0x1da6f | 36 | So, what now? Want me to keep going? |
| 0x1da94 | 18 | Huh? Ah, hold on-- |
| 0x1daa7 | 54 | Kuon rifles through her bags once more and retrieves\n |
| 0x1dade | 28 | a long, stick-like object... |
| 0x1dafb | 12 | ...A pencil? |
| 0x1db08 | 30 | First... 43, 1338, 6084, 55... |
| 0x1db27 | 23 | *Scribble, scribble*... |
| 0x1db3f | 28 | Hey, how about the next one? |
| 0x1db5c | 50 | Kuon prompts me, taking the notebook. Seems like\n |
| 0x1db8f | 39 | she's in a good mood for some reason... |
| 0x1dbb7 | 23 | The next one? Uh, 5126. |
| 0x1df53 | 55 | {c5}Free Battle{c-1} has been added to the system menu. |
| 0x1df8b | 50 | You can replay cleared stages in Free Battle mode. |
| 0x1dfbe | 52 | Do this at base, or whenever you're organizing for\n |
| 0x1dff3 | 50 | battle. Fight, level up, and collect Bonus Points! |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_08.json` com a forma:
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
