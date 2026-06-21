# Cena ch_11_10 — pacote de traducao (157 linhas)

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
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |

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
- `Urp...` -> `Buerp...` (Haku, 11_10)
- `Blurgh. I ate way too much. I feel like food's gonna\n` -> `Bleh. Comi demais. Sinto que a comida vai\n` (Haku, 11_10)
- `come out the wrong way if I open my mouth...` -> `voltar pelo caminho errado se eu abrir a boca...` (Haku, 11_10)
- `As I lie down rubbing my stomach, Kuon digs through\n` -> `Enquanto deito esfregando a barriga, a Kuon vasculha\n` (Haku, 11_10)
- `her bags, searching for something.` -> `as bolsas dela, procurando alguma coisa.` (Haku, 11_10)
- `How can she still move around like that? She ate\n` -> `Como ela ainda consegue se mexer assim? Ela comeu\n` (Haku, 11_10)
- `more than double her own body weight...` -> `mais que o dobro do próprio peso...` (Haku, 11_10)
- `She REALLY doesn't look like she eats as much as she\n` -> `Ela REALMENTE não parece comer tudo o que\n` (Haku, 11_10)
- `does. Where does it all go, with that figure?` -> `come. Onde será que tudo vai parar, com aquela silhueta?` (Haku, 11_10)
- `Hmmhmm...` -> `Hummhumm...` (Kuon, 11_10)
- `What are you doing?` -> `O que você tá fazendo?` (Haku, 11_10)
- `She seems to be in a good mood, humming to herself\n` -> `Ela parece estar de bom humor, cantarolando\n` (Haku, 11_10)
- `happily.` -> `feliz.` (Haku, 11_10)
- `Eh heh heh. Getting ready to take a bath, of course.` -> `Eheheh. Me preparando pra um banho, é claro.` (Kuon, 11_10)
- `I've just been wiping down for the past few days,\n` -> `Faz uns dias que só venho me limpando com pano,\n` (Kuon, 11_10)
- `so as long as we have baths, I'm taking advantage.` -> `então já que tem banho, vou aproveitar.` (Kuon, 11_10)
- `Kuon has a dreamy look on her face...` -> `A Kuon fica com um olhar sonhador...` (Haku, 11_10)
- `A bath, huh? You can't get a proper one on the road,\n` -> `Um banho, né? Na estrada não dá pra ter um decente,\n` (Haku, 11_10)
- `that's for sure.` -> `isso é certo.` (Haku, 11_10)
- `It's too bad we can't soak, but a bath's a bath.` -> `É uma pena não dar pra mergulhar, mas banho é banho.` (Kuon, 11_10)
- `Huh? It's a bath, but you can't soak in it?` -> `Hein? É banho, mas não dá pra mergulhar nele?` (Haku, 11_10)
- `Oh, they're steam baths! They're much more common\n` -> `Ah, são banhos a vapor! São muito mais comuns\n` (Kuon, 11_10)
- `than baths with running water around here.` -> `que banhos de água corrente por aqui.` (Kuon, 11_10)
- `Ah, I see.` -> `Ah, saquei.` (Haku, 11_10)
- `No hot tubs, then... I'd prefer a good soak, but a\n` -> `Sem banheira, então... Eu preferia um bom mergulho, mas\n` (Haku, 11_10)
- `steam bath still sounds pretty good right now.` -> `um banho a vapor já soa bem bom agora.` (Haku, 11_10)
- `You should go take one later, too. It'll melt away\n` -> `Você devia ir tomar um depois também. Ele derrete\n` (Kuon, 11_10)
- `the fatigue and cleanse you, body and soul.` -> `a fadiga e limpa você, corpo e alma.` (Kuon, 11_10)
- `Guess you're right...` -> `Acho que você tem razão...` (Haku, 11_10)
- `Now that she mentions it, I did sweat a whole lot\n` -> `Agora que ela mencionou, eu suei pra caramba\n` (Haku, 11_10)
- `exerting myself on the trek earlier...` -> `me esforçando na trilha mais cedo...` (Haku, 11_10)
- `Too bad about the hot water, but it'll feel nice to\n` -> `Pena a questão da água quente, mas vai ser gostoso\n` (Haku, 11_10)
- `relax in the steam.` -> `relaxar no vapor.` (Haku, 11_10)
- `All right, I'll go do that, then.` -> `Tá bom, vou fazer isso então.` (Haku, 11_10)
- `Uh.` -> `Ah.` (Kuon, 11_10)
- `Kuon makes a noise as if she's suddenly remembering\n` -> `A Kuon solta um som, como se de repente lembrasse\n` (Haku, 11_10)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `Uh... hm. Hmm...` -> `Ahn... hum. Hum...` (Kuon, 11_10)
- `Then she puts a finger to her chin, deep in thought.` -> `Aí ela põe o dedo no queixo, mergulhada em pensamentos.` (Haku, 11_10)
- `...Why is she looking at me like that?` -> `...Por que ela está me olhando desse jeito?` (Haku, 11_10)
- `I still have a few things I need to take care of,\n` -> `Ainda tenho umas coisinhas que preciso resolver,\n` (Kuon, 11_10)
- `actually.` -> `na verdade.` (Kuon, 11_10)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Yeah. It might take a while, so why don't you go\n` -> `É. Pode demorar um pouco, então por que você não vai\n` (Kuon, 11_10)
- `take a bath first?` -> `tomar banho primeiro?` (Kuon, 11_10)
- `Oh, I don't mind waiting.` -> `Ah, eu não me importo de esperar.` (Haku, 11_10)
- `My stomach's so full, I don't think I can move from\n` -> `Tô tão cheio que acho que nem saio deste lugar de\n` (Haku, 11_10)
- `this spot anyway. Besides, I want to relax.` -> `qualquer jeito. Além disso, eu quero relaxar.` (Haku, 11_10)
- `No, you're probably tired, right? Go ahead and take\n` -> `Não, você deve estar cansado, né? Vai logo e toma\n` (Kuon, 11_10)
- `it now. Here--a spare change of clothes for you.` -> `agora. Aqui--uma muda de roupa pra você.` (Kuon, 11_10)
- `She pushes a set of clothes into my hands. When did\n` -> `Ela enfia um conjunto de roupas nas minhas mãos. Quando\n` (Haku, 11_10)
- `she put those together?` -> `foi que ela preparou isso?` (Haku, 11_10)
- `You haven't forgotten how to take a bath, right?` -> `Você não esqueceu como se toma banho, né?` (Kuon, 11_10)
- `I seriously doubt that. I mean, I HOPE I haven't.` -> `Duvido muito. Quer dizer, eu ESPERO que não.` (Haku, 11_10)
- `Then you should be fine on your own. Don't worry\n` -> `Então você se vira sozinho. Não se preocupa\n` (Kuon, 11_10)
- `about me and go relax, OK?` -> `comigo e vai relaxar, tá?` (Kuon, 11_10)
- `If you insist...` -> `Se você insiste...` (Haku, 11_10)
- `I have a weird feeling about this, but it'd be rude\n` -> `Tenho uma sensação estranha sobre isso, mas seria rude\n` (Haku, 11_10)
- `to refuse her goodwill, so...` -> `recusar a boa vontade dela, então...` (Haku, 11_10)
- `The bath's downstairs and to the left, at the end\n` -> `O banho fica lá embaixo e à esquerda, no fim\n` (Kuon, 11_10)
- `of the corridor, OK?` -> `do corredor, tá?` (Kuon, 11_10)
- `OK, got it.` -> `Tá, entendi.` (Haku, 11_10)
- `As I leave the room and head left, a long hallway\n` -> `Saio do quarto e viro à esquerda, e um corredor\n` (Haku, 11_10)
- `greets me, as promised.` -> `comprido me recebe, como prometido.` (Haku, 11_10)
- `The door at the end of the hall opens into something\n` -> `A porta no fim do corredor abre pra algo\n` (Haku, 11_10)
- `like a changing room, lined with shelves.` -> `como um vestiário, com prateleiras nas paredes.` (Haku, 11_10)
- `Doesn't seem like anyone else is using the bath\n` -> `Não parece que mais alguém está usando o banho\n` (Haku, 11_10)
- `right now. I should be able to unwind without worry.` -> `agora. Devo conseguir relaxar sem preocupação.` (Haku, 11_10)
- `I untie my sash and toss my clothes haphazardly\n` -> `Desamarro a faixa e jogo minhas roupas de qualquer jeito\n` (Haku, 11_10)
- `onto a random shelf.` -> `numa prateleira qualquer.` (Haku, 11_10)
- `I open another door at the far end of the changing\n` -> `Abro outra porta no fundo do vestiário, e uma\n` (Haku, 11_10)
- `room, and a blast of hot air washes over me...` -> `rajada de ar quente me envolve...` (Haku, 11_10)
- `The bath beyond is spacious for an inn like this.\n` -> `O banho lá dentro é espaçoso pra uma estalagem assim.\n` (Haku, 11_10)
- `Benches line the walls, enough to seat five people.` -> `Bancos forram as paredes, dá pra cinco pessoas sentarem.` (Haku, 11_10)
- `Set into the opposite wall is something like a\n` -> `Na parede oposta há algo como uma\n` (Haku, 11_10)
- `furnace without an opening, fenced in by wood.` -> `fornalha sem abertura, cercada por madeira.` (Haku, 11_10)
- `Judging by the heat waves rising from it, you\n` -> `A julgar pelas ondas de calor que sobem dela, você\n` (Haku, 11_10)
- `probably pour water over that to make the steam...` -> `provavelmente joga água em cima pra fazer o vapor...` (Haku, 11_10)
- `Hoomph. Ah...` -> `Ufa. Ah...` (Haku, 11_10)
- `I flop onto one of the wooden benches and let out\n` -> `Me jogo num dos bancos de madeira e solto\n` (Haku, 11_10)
- `a deep sigh.` -> `um suspiro fundo.` (Haku, 11_10)
- `The room's warmth suffuses me. I didn't realize how\n` -> `O calor do recinto me envolve. Eu não imaginava\n` (Haku, 11_10)
- `good this would feel.` -> `o quanto isso seria bom.` (Haku, 11_10)
- `Ahhh...` -> `Ahhh...` (Haku, 11_10)
- `I zone out, staring up at the ceiling and thinking.\n` -> `Desligo, encarando o teto e pensando.\n` (Haku, 11_10)
- `The day's events wash over me...` -> `Os acontecimentos do dia passam por mim...` (Haku, 11_10)
- `I woke up in a strange place...` -> `Acordei num lugar estranho...` (Haku, 11_10)
- `Then, a monstrous creature attacked me, only for\n` -> `Aí uma criatura monstruosa me atacou, e a\n` (Haku, 11_10)
- `Kuon to save me in the nick of time.` -> `Kuon me salvou bem em cima da hora.` (Haku, 11_10)
- `And now, here I am with no memory, no belongings,\n` -> `E agora, aqui estou eu, sem memória, sem pertences,\n` (Haku, 11_10)
- `no power. No place to go home to. A lot of nothing.` -> `sem poder. Sem um lar pra onde voltar. Um bocado de nada.` (Haku, 11_10)
- `What am I going to do...?` -> `O que é que eu vou fazer...?` (Haku, 11_10)
- `Bah, no point stressing over it. As it stands,\n` -> `Bah, não adianta me estressar com isso. Como estão\n` (Haku, 11_10)
- `I can't do much but trust in Kuon's hospitality.` -> `as coisas, só me resta confiar na hospitalidade da Kuon.` (Haku, 11_10)
- `We'll see how things play out...` -> `Vamos ver como as coisas vão se desenrolar...` (Haku, 11_10)
- `Taking a ladle from the bench, I throw water over\n` -> `Pegando uma concha do banco, jogo água sobre\n` (Haku, 11_10)
- `the heating apparatus.` -> `o aparelho de aquecimento.` (Haku, 11_10)
- `The hiss of evaporating water and a cloud of steam\n` -> `O chiado da água evaporando e uma nuvem de vapor\n` (Haku, 11_10)
- `fill the room, heating the air.` -> `enchem o recinto, aquecendo o ar.` (Haku, 11_10)
- `Gah. I walked so much, my calves are all swollen.` -> `Ai. Andei tanto que minhas panturrilhas estão todas inchadas.` (Haku, 11_10)
- `The arches of my feet, too. Ow.` -> `As plantas dos pés também. Ai.` (Haku, 11_10)
- `A dull pain shoots through my foot when I try to\n` -> `Uma dor surda atravessa meu pé quando tento\n` (Haku, 11_10)
- `rub the ache away...` -> `esfregar pra aliviar a dor...` (Haku, 11_10)
- `Perturbed, I lift my foot, looking at the sole to\n` -> `Incomodado, levanto o pé e olho a sola pra\n` (Haku, 11_10)
- `find the source of the pain...` -> `achar a origem da dor...` (Haku, 11_10)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `A loud thud interrupts me from the other side of\n` -> `Um baque alto me interrompe do outro lado\n` (Haku, 11_10)
- `the wall.` -> `da parede.` (Haku, 11_10)
- `What the... Did something collapse? Doesn't matter,\n` -> `Mas que... Caiu alguma coisa? Tanto faz,\n` (Haku, 11_10)
- `I guess.` -> `eu acho.` (Haku, 11_10)
- `I look back down at the poor sole of my foot--rife\n` -> `Volto a olhar a coitada da sola do meu pé--cheia\n` (Haku, 11_10)
- `with blisters, some of them torn and bloodied.` -> `de bolhas, algumas estouradas e ensanguentadas.` (Haku, 11_10)
- `Yikes, the skin's peeling, too. I guess we did walk\n` -> `Eca, a pele tá descascando também. Acho que a gente\n` (Haku, 11_10)
- `a pretty long way...` -> `andou um bom tanto mesmo...` (Haku, 11_10)
- `Probably better not to touch that. Left with no\n` -> `Melhor não mexer nisso. Sem opção, volto a\n` (Haku, 11_10)
- `choice, I return to massaging my sore calves\n` -> `massagear minhas panturrilhas doloridas\n` (Haku, 11_10)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Suddenly, I get the feeling I'm being watched.` -> `De repente, tenho a sensação de que estou sendo observado.` (Haku, 11_10)
- `I glance around the steam-filled room, but of\n` -> `Olho ao redor do recinto cheio de vapor, mas\n` (Haku, 11_10)
- `course, no one is in here with me...` -> `claro, não tem ninguém aqui comigo...` (Haku, 11_10)
- `...Probably just my imagination.` -> `...Provavelmente é só imaginação minha.` (Haku, 11_10)
- `Oh, well. I should loosen up my other muscles while\n` -> `Enfim. Vou soltar os outros músculos enquanto\n` (Haku, 11_10)
- `I'm in here--it's not just my calves that hurt.` -> `estou aqui--não é só a panturrilha que dói.` (Haku, 11_10)
- `Up we go...` -> `Lá vamos nós...` (Haku, 11_10)
- `Careful of my feet, I ease myself up and stand\n` -> `Com cuidado com os pés, me ergo e fico\n` (Haku, 11_10)
- `upright, stretching out my whole body.` -> `de pé, esticando o corpo inteiro.` (Haku, 11_10)
- `*Flutter, fwumph*` -> `*Flap, pof*` (Haku, 11_10)
- `*THUNK*` -> `*TUM*` (Haku, 11_10)
- `Oops, the washcloth around my waist is--wait, there's\n` -> `Ops, a toalha na minha cintura tá-- espera, lá\n` (Haku, 11_10)
- `that noise again. Where's that coming from?` -> `vem aquele barulho de novo. De onde vem isso?` (Haku, 11_10)
- `*Squeeeaak. Squeak, squeak, chirp.*` -> `*Iiiii. Ii, ii, piu.*` (Haku, 11_10)
- `...some kind of small animal? Who knows what weird\n` -> `...algum bichinho pequeno? Vai saber que criaturas\n` (Haku, 11_10)
- `creatures the innkeeper might have around...` -> `esquisitas a estalajadeira pode ter por aqui...` (Haku, 11_10)
- `Well, no big deal. As long as it minds its own\n` -> `Bom, tanto faz. Desde que cuide da própria\n` (Haku, 11_10)
- `business. Now, I'll start with some loosening up...` -> `vida. Agora, vou começar com um alongamento...` (Haku, 11_10)
- `Shake-shake-shake-shake--` -> `Treme-treme-treme-treme--` (Haku, 11_10)
- `*Thwap, fwup, thwap--*` -> `*Pá, fup, pá--*` (Haku, 11_10)
- `*WHOMP, CRASH, THUNK*` -> `*BAM, CABRUM, TUM*` (Haku, 11_10)
- `Gyeek!` -> `Iiek!` (Kuon, 11_10)
- `That thing's making a lot of noise out there. What's\n` -> `Aquela coisa tá fazendo um bocado de barulho lá fora.\n` (Haku, 11_10)
- `with the ruckus?` -> `Que algazarra é essa?` (Haku, 11_10)
- `Whatever. Next, some hip swivels--` -> `Tanto faz. Agora, uns giros de quadril--` (Haku, 11_10)
- `Hup! Hup, hmph, hah!` -> `Upa! Upa, hmf, hep!` (Haku, 11_10)
- `*Thwip, thwip, thwap--*` -> `*Fiu, fiu, pá--*` (Haku, 11_10)
- `*Rattle, rattle*...` -> `*Tarrac, tarrac*...` (Haku, 11_10)
- `All right, here we go! Pick up the pace!` -> `Beleza, lá vamos nós! Vamos acelerar!` (Haku, 11_10)
- `*Jiggle, jiggle, thwip--*` -> `*Treme, treme, fiu--*` (Haku, 11_10)
- `*WHUMP* *clatter*` -> `*BAM* *tlec-tlec*` (Haku, 11_10)
- `Fwaaaaaaaaah!!...` -> `Fuaaaaaaaaah!!...` (Kuon, 11_10)
- `Something crashes loudly and scampers off...` -> `Alguma coisa cai com estrondo e sai correndo...` (Haku, 11_10)
- `Just animals fighting. I don't really know the\n` -> `Só animais brigando. Não conheço bem as estações\n` (Haku, 11_10)
- `seasons here, but I guess spring must be close.` -> `daqui, mas acho que a primavera deve estar perto.` (Haku, 11_10)
- `Loosened up, I sit back down on the bench and\n` -> `Já solto, sento de volta no banco e me\n` (Haku, 11_10)
- `surrender myself to the relaxing steam.` -> `entrego ao vapor relaxante.` (Haku, 11_10)
- `Ahhh, that hits the spot...` -> `Ahhh, isso sim é que é bom...` (Haku, 11_10)
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
| 0x22595 | 6 | Urp... |
| 0x2259c | 54 | Blurgh. I ate way too much. I feel like food's gonna\n |
| 0x225d3 | 44 | come out the wrong way if I open my mouth... |
| 0x22600 | 53 | As I lie down rubbing my stomach, Kuon digs through\n |
| 0x22636 | 34 | her bags, searching for something. |
| 0x22659 | 50 | How can she still move around like that? She ate\n |
| 0x2268c | 39 | more than double her own body weight... |
| 0x226b4 | 54 | She REALLY doesn't look like she eats as much as she\n |
| 0x226eb | 45 | does. Where does it all go, with that figure? |
| 0x22719 | 9 | Hmmhmm... |
| 0x22723 | 19 | What are you doing? |
| 0x22737 | 52 | She seems to be in a good mood, humming to herself\n |
| 0x2276c | 8 | happily. |
| 0x22775 | 52 | Eh heh heh. Getting ready to take a bath, of course. |
| 0x227aa | 51 | I've just been wiping down for the past few days,\n |
| 0x227de | 50 | so as long as we have baths, I'm taking advantage. |
| 0x22811 | 37 | Kuon has a dreamy look on her face... |
| 0x22837 | 54 | A bath, huh? You can't get a proper one on the road,\n |
| 0x2286e | 16 | that's for sure. |
| 0x2287f | 48 | It's too bad we can't soak, but a bath's a bath. |
| 0x228b0 | 43 | Huh? It's a bath, but you can't soak in it? |
| 0x228dc | 51 | Oh, they're steam baths! They're much more common\n |
| 0x22910 | 42 | than baths with running water around here. |
| 0x2293b | 10 | Ah, I see. |
| 0x22946 | 52 | No hot tubs, then... I'd prefer a good soak, but a\n |
| 0x2297b | 46 | steam bath still sounds pretty good right now. |
| 0x229aa | 52 | You should go take one later, too. It'll melt away\n |
| 0x229df | 43 | the fatigue and cleanse you, body and soul. |
| 0x22a0b | 21 | Guess you're right... |
| 0x22a21 | 51 | Now that she mentions it, I did sweat a whole lot\n |
| 0x22a55 | 38 | exerting myself on the trek earlier... |
| 0x22a7c | 53 | Too bad about the hot water, but it'll feel nice to\n |
| 0x22ab2 | 19 | relax in the steam. |
| 0x22ac6 | 33 | All right, I'll go do that, then. |
| 0x22ae8 | 3 | Uh. |
| 0x22aec | 53 | Kuon makes a noise as if she's suddenly remembering\n |
| 0x22b22 | 10 | something. |
| 0x22b2d | 16 | Uh... hm. Hmm... |
| 0x22b3e | 52 | Then she puts a finger to her chin, deep in thought. |
| 0x22b73 | 38 | ...Why is she looking at me like that? |
| 0x22b9a | 51 | I still have a few things I need to take care of,\n |
| 0x22bce | 9 | actually. |
| 0x22bd8 | 3 | Hm? |
| 0x22bdc | 50 | Yeah. It might take a while, so why don't you go\n |
| 0x22c0f | 18 | take a bath first? |
| 0x22c22 | 25 | Oh, I don't mind waiting. |
| 0x22c3c | 53 | My stomach's so full, I don't think I can move from\n |
| 0x22c72 | 43 | this spot anyway. Besides, I want to relax. |
| 0x22c9e | 53 | No, you're probably tired, right? Go ahead and take\n |
| 0x22cd4 | 48 | it now. Here--a spare change of clothes for you. |
| 0x22d05 | 53 | She pushes a set of clothes into my hands. When did\n |
| 0x22d3b | 23 | she put those together? |
| 0x22d53 | 48 | You haven't forgotten how to take a bath, right? |
| 0x22d84 | 49 | I seriously doubt that. I mean, I HOPE I haven't. |
| 0x22db6 | 50 | Then you should be fine on your own. Don't worry\n |
| 0x22de9 | 26 | about me and go relax, OK? |
| 0x22e04 | 16 | If you insist... |
| 0x22e15 | 53 | I have a weird feeling about this, but it'd be rude\n |
| 0x22e4b | 29 | to refuse her goodwill, so... |
| 0x22e69 | 51 | The bath's downstairs and to the left, at the end\n |
| 0x22e9d | 20 | of the corridor, OK? |
| 0x22eb2 | 11 | OK, got it. |
| 0x22ebe | 51 | As I leave the room and head left, a long hallway\n |
| 0x22ef2 | 23 | greets me, as promised. |
| 0x22f0a | 54 | The door at the end of the hall opens into something\n |
| 0x22f41 | 41 | like a changing room, lined with shelves. |
| 0x22f6b | 49 | Doesn't seem like anyone else is using the bath\n |
| 0x22f9d | 52 | right now. I should be able to unwind without worry. |
| 0x22fd2 | 49 | I untie my sash and toss my clothes haphazardly\n |
| 0x23004 | 20 | onto a random shelf. |
| 0x23019 | 52 | I open another door at the far end of the changing\n |
| 0x2304e | 46 | room, and a blast of hot air washes over me... |
| 0x2307d | 51 | The bath beyond is spacious for an inn like this.\n |
| 0x230b1 | 51 | Benches line the walls, enough to seat five people. |
| 0x230e5 | 48 | Set into the opposite wall is something like a\n |
| 0x23116 | 46 | furnace without an opening, fenced in by wood. |
| 0x23145 | 47 | Judging by the heat waves rising from it, you\n |
| 0x23175 | 50 | probably pour water over that to make the steam... |
| 0x231a8 | 13 | Hoomph. Ah... |
| 0x231b6 | 51 | I flop onto one of the wooden benches and let out\n |
| 0x231ea | 12 | a deep sigh. |
| 0x231f7 | 53 | The room's warmth suffuses me. I didn't realize how\n |
| 0x2322d | 21 | good this would feel. |
| 0x23243 | 7 | Ahhh... |
| 0x2324b | 53 | I zone out, staring up at the ceiling and thinking.\n |
| 0x23281 | 32 | The day's events wash over me... |
| 0x232a2 | 31 | I woke up in a strange place... |
| 0x232c2 | 50 | Then, a monstrous creature attacked me, only for\n |
| 0x232f5 | 36 | Kuon to save me in the nick of time. |
| 0x2331a | 51 | And now, here I am with no memory, no belongings,\n |
| 0x2334e | 51 | no power. No place to go home to. A lot of nothing. |
| 0x23382 | 25 | What am I going to do...? |
| 0x2339c | 48 | Bah, no point stressing over it. As it stands,\n |
| 0x233cd | 48 | I can't do much but trust in Kuon's hospitality. |
| 0x233fe | 32 | We'll see how things play out... |
| 0x2341f | 51 | Taking a ladle from the bench, I throw water over\n |
| 0x23453 | 22 | the heating apparatus. |
| 0x2346a | 52 | The hiss of evaporating water and a cloud of steam\n |
| 0x2349f | 31 | fill the room, heating the air. |
| 0x234bf | 49 | Gah. I walked so much, my calves are all swollen. |
| 0x234f1 | 31 | The arches of my feet, too. Ow. |
| 0x23511 | 50 | A dull pain shoots through my foot when I try to\n |
| 0x23544 | 20 | rub the ache away... |
| 0x23559 | 51 | Perturbed, I lift my foot, looking at the sole to\n |
| 0x2358d | 30 | find the source of the pain... |
| 0x235ac | 4 | Huh? |
| 0x235b1 | 50 | A loud thud interrupts me from the other side of\n |
| 0x235e4 | 9 | the wall. |
| 0x235ee | 53 | What the... Did something collapse? Doesn't matter,\n |
| 0x23624 | 8 | I guess. |
| 0x2362d | 52 | I look back down at the poor sole of my foot--rife\n |
| 0x23662 | 46 | with blisters, some of them torn and bloodied. |
| 0x23691 | 53 | Yikes, the skin's peeling, too. I guess we did walk\n |
| 0x236c7 | 20 | a pretty long way... |
| 0x236dc | 49 | Probably better not to touch that. Left with no\n |
| 0x2370e | 46 | choice, I return to massaging my sore calves\n |
| 0x2373d | 8 | instead. |
| 0x23746 | 7 | ...Huh? |
| 0x2374e | 46 | Suddenly, I get the feeling I'm being watched. |
| 0x2377d | 47 | I glance around the steam-filled room, but of\n |
| 0x237ad | 36 | course, no one is in here with me... |
| 0x237d2 | 32 | ...Probably just my imagination. |
| 0x237f3 | 53 | Oh, well. I should loosen up my other muscles while\n |
| 0x23829 | 47 | I'm in here--it's not just my calves that hurt. |
| 0x23859 | 11 | Up we go... |
| 0x23865 | 48 | Careful of my feet, I ease myself up and stand\n |
| 0x23896 | 38 | upright, stretching out my whole body. |
| 0x238bd | 17 | *Flutter, fwumph* |
| 0x238cf | 7 | *THUNK* |
| 0x238d7 | 55 | Oops, the washcloth around my waist is--wait, there's\n |
| 0x2390f | 43 | that noise again. Where's that coming from? |
| 0x2393b | 35 | *Squeeeaak. Squeak, squeak, chirp.* |
| 0x2395f | 52 | ...some kind of small animal? Who knows what weird\n |
| 0x23994 | 44 | creatures the innkeeper might have around... |
| 0x239c1 | 48 | Well, no big deal. As long as it minds its own\n |
| 0x239f2 | 51 | business. Now, I'll start with some loosening up... |
| 0x23a26 | 25 | Shake-shake-shake-shake-- |
| 0x23a40 | 22 | *Thwap, fwup, thwap--* |
| 0x23a57 | 21 | *WHOMP, CRASH, THUNK* |
| 0x23a6d | 6 | Gyeek! |
| 0x23a74 | 54 | That thing's making a lot of noise out there. What's\n |
| 0x23aab | 16 | with the ruckus? |
| 0x23abc | 34 | Whatever. Next, some hip swivels-- |
| 0x23adf | 20 | Hup! Hup, hmph, hah! |
| 0x23af4 | 23 | *Thwip, thwip, thwap--* |
| 0x23b0c | 9 | *THUNK*\n |
| 0x23b16 | 19 | *Rattle, rattle*... |
| 0x23b2a | 40 | All right, here we go! Pick up the pace! |
| 0x23b53 | 25 | *Jiggle, jiggle, thwip--* |
| 0x23b6d | 17 | *WHUMP* *clatter* |
| 0x23b7f | 17 | Fwaaaaaaaaah!!... |
| 0x23b91 | 44 | Something crashes loudly and scampers off... |
| 0x23bbe | 48 | Just animals fighting. I don't really know the\n |
| 0x23bef | 47 | seasons here, but I guess spring must be close. |
| 0x23c1f | 47 | Loosened up, I sit back down on the bench and\n |
| 0x23c4f | 39 | surrender myself to the relaxing steam. |
| 0x23c77 | 27 | Ahhh, that hits the spot... |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_10.json` com a forma:
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
