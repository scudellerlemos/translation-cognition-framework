# Cena ch_11_09 — pacote de traducao (213 linhas)

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
| amamunii | Comida | amamunii | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
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
- `Let's eat! Ah...` -> `Vamos comer! Ah...` (Kuon, 11_09)
- `*Hromf, munch--*` -> `*Hrom, nhac--*` (Kuon, 11_09)
- `*--gulp* Mmf, that's good...` -> `*--glup* Mmf, que delícia...` (Kuon, 11_09)
- `Spacing out over there? Come on, this is delicious.\n` -> `Viajando aí? Vai, isso aqui tá uma delícia.\n` (Kuon, 11_09)
- `You're not gonna eat?` -> `Você não vai comer?` (Kuon, 11_09)
- `R-Right...` -> `C-Certo...` (Haku, 11_09)
- `It got dark outside while we were busy organizing\n` -> `Escureceu lá fora enquanto a gente organizava\n` (Haku, 11_09)
- `our belongings...` -> `nossas coisas...` (Haku, 11_09)
- `At some point, a tantalizing aroma wafted into the\n` -> `Em algum momento, um aroma convidativo entrou no\n` (Haku, 11_09)
- `room from somewhere else in the inn.` -> `quarto, vindo de algum canto da estalagem.` (Haku, 11_09)
- `The scent tickled my nose and made my stomach growl\n` -> `O cheiro fez cócegas no meu nariz e meu estômago roncar\n` (Haku, 11_09)
- `with hunger...` -> `de fome...` (Haku, 11_09)
- `Chuckling, Kuon led me downstairs, where we\n` -> `Rindo, a Kuon me levou lá pra baixo, onde\n` (Haku, 11_09)
- `found a group of locals drinking and dining merrily.` -> `achamos um grupo de locais bebendo e jantando alegres.` (Haku, 11_09)
- `Now, a staggering number of dishes are lined up on\n` -> `E agora, um número absurdo de pratos está disposto na\n` (Haku, 11_09)
- `the table before us.` -> `mesa à nossa frente.` (Haku, 11_09)
- `Geez. What's with these portions, though?` -> `Cruzes. Mas que porções são essas?` (Haku, 11_09)
- `The plates are all stacked so high with food they\n` -> `Os pratos estão tão cheios de comida que\n` (Haku, 11_09)
- `threaten to topple. This is way too much for two...` -> `ameaçam desabar. Isso é demais pra dois...` (Haku, 11_09)
- `Hell, there's enough food crowding the table for\n` -> `Caramba, tem comida na mesa pra pelo menos\n` (Haku, 11_09)
- `at least TEN people.` -> `DEZ pessoas.` (Haku, 11_09)
- `Oblivious to my dumbfounded state, Kuon reaches for\n` -> `Alheia ao meu espanto, a Kuon pega um\n` (Haku, 11_09)
- `a plate and hums happily to herself.` -> `prato e cantarola feliz.` (Haku, 11_09)
- `Mm, and I'll try... this one, and this one next!` -> `Hum, e eu vou provar... este, e depois este!` (Kuon, 11_09)
- `She piles heaps of meat and vegetables onto some\n` -> `Ela empilha montes de carne e legumes em alguma\n` (Haku, 11_09)
- `kind of thin dough, wrapping it all up neatly.` -> `espécie de massa fina, embrulhando tudo com capricho.` (Haku, 11_09)
- `*Grmf, hrmf, munch--*` -> `*Grmf, hrmf, nhac--*` (Kuon, 11_09)
- `The wrap, bursting at the seams with ingredients,\n` -> `O embrulho, estourando de tanto recheio,\n` (Haku, 11_09)
- `disappears in just a few bites...!` -> `some em poucas mordidas...!` (Haku, 11_09)
- `Kuon opens her mouth wide and stuffs her face, but\n` -> `A Kuon abre a boca enorme e enfia tudo, mas\n` (Haku, 11_09)
- `somehow, she makes it look refined.` -> `de algum jeito, ela faz parecer refinado.` (Haku, 11_09)
- `Don't hold back, OK? We're celebrating you making\n` -> `Não se segura, tá? A gente tá comemorando você ter\n` (Kuon, 11_09)
- `it back here safely.` -> `voltado são e salvo.` (Kuon, 11_09)
- `While I'm happy to hear you say that...` -> `Apesar de eu gostar de ouvir isso...` (Haku, 11_09)
- `This all looks like quite a feast. I hope she didn't\n` -> `Isso tudo parece um banquetão. Espero que ela não\n` (Haku, 11_09)
- `splurge for my sake...` -> `tenha gastado à toa por minha causa...` (Haku, 11_09)
- `Well, if you aren't eating, I'll just help myself\n` -> `Bom, se você não vai comer, eu mesma me sirvo\n` (Kuon, 11_09)
- `to the rest.` -> `do resto.` (Kuon, 11_09)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Ahhh... *Grmf, hromf--munch, munch--*` -> `Ahhh... *Grmf, hrom--nhac, nhac--*` (Kuon, 11_09)
- `D-Did she say "the rest"?` -> `E-Ela disse "o resto"?` (Haku, 11_09)
- `Oh, right. Do you not know how to eat this, Haku?` -> `Ah, é mesmo. Você não sabe como comer isso, Haku?` (Kuon, 11_09)
- `Um, well. Not... really.` -> `Ahn, bom. Não... muito.` (Haku, 11_09)
- `I nod unconsciously, not quite able to tell her I'm\n` -> `Aceno sem pensar, sem conseguir dizer que o que\n` (Haku, 11_09)
- `more taken aback by the sheer quantity.` -> `mais me espanta é a quantidade.` (Haku, 11_09)
- `Well, then! Allow me to teach you.` -> `Pois então! Deixa eu te ensinar.` (Kuon, 11_09)
- `From the plate in front of her, Kuon grabs another\n` -> `Do prato à frente dela, a Kuon pega outra\n` (Haku, 11_09)
- `one of those thin sheets of flatbread...` -> `daquelas folhas finas de pão achatado...` (Haku, 11_09)
- `First, we get the amam skin ready.` -> `Primeiro, a gente prepara a pele de amam.` (Kuon, 11_09)
- `This?` -> `Esta?` (Haku, 11_09)
- `I pick up another of the flimsy, doughy sheets,\n` -> `Pego outra das folhas finas e macias,\n` (Haku, 11_09)
- `watching it pillow pliantly around my fingers...` -> `vendo ela se moldar fofa nos meus dedos...` (Haku, 11_09)
- `She called it a "skin," but it looks like it's\n` -> `Ela chamou de "pele", mas parece ser\n` (Haku, 11_09)
- `grain pounded and baked like flatbread, not actual\n` -> `grão moído e assado como pão achatado, não\n` (Haku, 11_09)
- `animal hide.` -> `couro de animal de verdade.` (Haku, 11_09)
- `That grain we carried earlier was amam. It turns\n` -> `Aquele grão que a gente carregou era amam. Vira\n` (Kuon, 11_09)
- `into this after you grind it into flour and bake it.` -> `isto depois de moer em farinha e assar.` (Kuon, 11_09)
- `You put ingredients like cooked meats, vegetables,\n` -> `Você põe ingredientes tipo carnes cozidas, legumes\n` (Kuon, 11_09)
- `or fish in the middle, then wrap it all up!` -> `ou peixe no meio, e embrulha tudo!` (Kuon, 11_09)
- `One finished amamunii. Dip in your favorite sauce\n` -> `Um amamunii pronto. Molha no seu molho favorito\n` (Kuon, 11_09)
- `and enjoy!` -> `e aproveita!` (Kuon, 11_09)
- `Kuon hands me the amam-wrapped bundle of food.` -> `A Kuon me passa o embrulho de comida enrolado na pele de amam.` (Haku, 11_09)
- `Talk about extra large...` -> `Isso que é tamanho família...` (Haku, 11_09)
- `The skin looks like it's fit to burst. She\n` -> `A pele parece prestes a estourar. Ela\n` (Haku, 11_09)
- `definitely overstuffed this.` -> `definitivamente exagerou no recheio.` (Haku, 11_09)
- `As I stare in disbelief at mine, Kuon makes another\n` -> `Enquanto eu encaro o meu sem acreditar, a Kuon faz outro\n` (Haku, 11_09)
- `just like it and digs in.` -> `igualzinho e ataca.` (Haku, 11_09)
- `Persuaded, I take a careful bite, cautious not to\n` -> `Convencido, dou uma mordida cuidadosa, tomando cuidado pra não\n` (Haku, 11_09)
- `let any of the filling spill...` -> `deixar o recheio cair...` (Haku, 11_09)
- `*Munch, munch*... Mm.` -> `*Nhac, nhac*... Hum.` (Haku, 11_09)
- `OK, yeah. That's pretty good. A little heavy on\n` -> `Tá, é. Bem bom mesmo. Um pouco pesado no\n` (Haku, 11_09)
- `the seasoning, but still good.` -> `tempero, mas mesmo assim bom.` (Haku, 11_09)
- `And it tastes even better since it's a free meal.` -> `E fica ainda melhor porque é refeição de graça.` (Haku, 11_09)
- `Eh heh heh. I may not look it, but I'm a pretty good\n` -> `Eheheh. Posso não parecer, mas sou uma cozinheira\n` (Kuon, 11_09)
- `cook.` -> `e tanto.` (Kuon, 11_09)
- `Kuon smiles proudly.` -> `A Kuon sorri orgulhosa.` (Haku, 11_09)
- `...I don't think being able to wrap things up in a\n` -> `...Não acho que saber embrulhar as coisas numa\n` (Haku, 11_09)
- `skin makes you a cook, but whatever you say.` -> `pele faça de você cozinheira, mas tá bom.` (Haku, 11_09)
- `I manage to bite my tongue before the quip actually\n` -> `Consigo segurar a língua antes que a piada\n` (Haku, 11_09)
- `escapes my throat.` -> `escape de fato da minha garganta.` (Haku, 11_09)
- `*Mmf, gromf--*` -> `*Mmf, gromf--*` (Kuon, 11_09)
- `It's certainly delicious, but I'm getting parched.\n` -> `É deliciosa mesmo, mas estou ficando com sede.\n` (Haku, 11_09)
- `Probably the seasoning.` -> `Provavelmente o tempero.` (Haku, 11_09)
- `Is there anything to drink...?` -> `Tem algo pra beber...?` (Haku, 11_09)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `As though reading my mind, Kuon slides a bowl of\n` -> `Como se lesse minha mente, a Kuon empurra uma tigela de\n` (Haku, 11_09)
- `amber-colored liquid towards me.` -> `líquido âmbar na minha direção.` (Haku, 11_09)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `I take an experimental sip, tasting the beverage...` -> `Dou um gole experimental, provando a bebida...` (Haku, 11_09)
- `It has an odd, citrusy flavor, but it's not\n` -> `Tem um sabor cítrico esquisito, mas não é\n` (Haku, 11_09)
- `overpowering--in fact, it cleanses my palate pretty\n` -> `intenso demais--na verdade, ele limpa meu paladar\n` (Haku, 11_09)
- `nicely.` -> `direitinho.` (Haku, 11_09)
- `Is this... alcohol?` -> `Isso é... álcool?` (Haku, 11_09)
- `Uh huh. It's a drink you'll find a lot in this\n` -> `Aham. É uma bebida bem comum nesta\n` (Kuon, 11_09)
- `region. It's not too strong, so it's drunk with\n` -> `região. Não é muito forte, então costumam beber com\n` (Kuon, 11_09)
- `meals, usually.` -> `as refeições.` (Kuon, 11_09)
- `Interesting...` -> `Interessante...` (Haku, 11_09)
- `It almost seems like beer, but that citrus taste\n` -> `Quase parece cerveja, mas aquele toque cítrico\n` (Haku, 11_09)
- `distinguishes it from standard lager.` -> `a diferencia de uma lager comum.` (Haku, 11_09)
- `I like it. The bubbles and the sourness go nicely\n` -> `Gostei. As bolhas e a acidez combinam bem\n` (Haku, 11_09)
- `with the heavy seasoning on these dishes.` -> `com o tempero forte desses pratos.` (Haku, 11_09)
- `And we don't really have it in my homeland! So it's\n` -> `E a gente quase não tem isso na minha terra! Então\n` (Kuon, 11_09)
- `still a novelty to me.` -> `ainda é novidade pra mim.` (Kuon, 11_09)
- `Homeland?` -> `Terra natal?` (Haku, 11_09)
- `You're not from around here, then?` -> `Então você não é daqui?` (Haku, 11_09)
- `Hm? Yeah, I'm from across the sea. It was a rough\n` -> `Hum? É, sou de além-mar. Foi uma travessia\n` (Kuon, 11_09)
- `voyage getting here, though.` -> `difícil chegar aqui, no entanto.` (Kuon, 11_09)
- `I see. I don't know what part of the world you're\n` -> `Saquei. Não sei de que parte do mundo você\n` (Haku, 11_09)
- `from, but that... sounds like it's far away.` -> `é, mas isso... parece ser bem longe.` (Haku, 11_09)
- `Uh huh. I've traveled a lot since I was a child,\n` -> `Aham. Eu viajo muito desde criança,\n` (Kuon, 11_09)
- `but this is the first time I've been out this far\n` -> `mas é a primeira vez que vou tão longe\n` (Kuon, 11_09)
- `on my own.` -> `sozinha.` (Kuon, 11_09)
- `It was also my first time traveling by ship, so\n` -> `Também foi minha primeira vez viajando de navio, então\n` (Kuon, 11_09)
- `getting that new experience was fun in the end.` -> `no fim foi divertido ter essa experiência nova.` (Kuon, 11_09)
- `We did have a few close calls, though...` -> `Mas a gente passou por uns perrengues...` (Kuon, 11_09)
- `What, like you got caught in a storm or something?` -> `Quê, tipo pegar uma tempestade ou algo assim?` (Haku, 11_09)
- `Kuon puts a finger to her lips, smiling proudly.` -> `A Kuon põe o dedo nos lábios, sorrindo orgulhosa.` (Haku, 11_09)
- `It wasn't a storm, but we ran into something just\n` -> `Não foi tempestade, mas a gente topou com algo quase\n` (Kuon, 11_09)
- `about as scary. Can you guess?` -> `tão assustador. Adivinha?` (Kuon, 11_09)
- `Something close to a storm... Like a tsunami, or\n` -> `Algo parecido com tempestade... Tipo um tsunami, ou\n` (Haku, 11_09)
- `a giant whirlpool?` -> `um redemoinho gigante?` (Haku, 11_09)
- `Too bad! Both wrong. The correct answer is "giant\n` -> `Que pena! Os dois errados. A resposta certa é "ataque de\n` (Kuon, 11_09)
- `sea monster attack."` -> `monstro marinho gigante."` (Kuon, 11_09)
- `Um.` -> `Ahn.` (Haku, 11_09)
- `It happened on a calm, sunny day, and the ship had\n` -> `Foi num dia calmo e ensolarado, e o navio tinha\n` (Kuon, 11_09)
- `a lot of people packed belowdecks.` -> `muita gente amontoada no porão.` (Kuon, 11_09)
- `The water was peaceful, so I thought I'd go above\n` -> `A água estava tranquila, então pensei em subir\n` (Kuon, 11_09)
- `and watch the waves, but...` -> `pra ver as ondas, mas...` (Kuon, 11_09)
- `When I got up there, I was just in time to see giant\n` -> `Quando cheguei lá em cima, foi bem a tempo de ver braços\n` (Kuon, 11_09)
- `arms--more like legs--emerge and seize the ship!` -> `gigantes--mais pra pernas--surgirem e agarrarem o navio!` (Kuon, 11_09)
- `It tried to pull us beneath the surface, drowning\n` -> `Tentou nos puxar pra debaixo d'água, afogando\n` (Kuon, 11_09)
- `anyone who fell off--it was awful, really.` -> `quem caía--foi horrível, de verdade.` (Kuon, 11_09)
- `That's... nowhere near "like" a storm.` -> `Isso... não chega nem perto de ser "tipo" tempestade.` (Haku, 11_09)
- `Hold on. You're just pulling my leg, aren't you?\n` -> `Calma. Você só tá me zoando, né?\n` (Haku, 11_09)
- `This is some kind of joke.` -> `Isso é algum tipo de piada.` (Haku, 11_09)
- `A joke?` -> `Piada?` (Kuon, 11_09)
- `Kuon tilts her head quizzically.` -> `A Kuon inclina a cabeça, sem entender.` (Haku, 11_09)
- `...Never mind.` -> `...Deixa pra lá.` (Haku, 11_09)
- `I'm starting to get a headache trying to wrap my\n` -> `Tô começando a ter dor de cabeça tentando\n` (Haku, 11_09)
- `head around this. Time to change the subject.` -> `entender isso. Hora de mudar de assunto.` (Haku, 11_09)
- `So, I'm curious. Why are you traveling? Do you have\n` -> `Então, fiquei curioso. Por que você viaja? Tem algum\n` (Haku, 11_09)
- `some goal way out here--some objective?` -> `objetivo aqui longe--alguma meta?` (Haku, 11_09)
- `Objective...` -> `Objetivo...` (Kuon, 11_09)
- `If it's hard to talk about, you don't have to...` -> `Se for difícil falar, não precisa...` (Haku, 11_09)
- `Oh, no, nothing like that. I just haven't had to...\n` -> `Ah, não, nada disso. É que eu nunca precisei...\n` (Kuon, 11_09)
- `Well, put it into words before.` -> `Bom, pôr isso em palavras antes.` (Kuon, 11_09)
- `I just want to take myself to as many new places as\n` -> `Eu só quero me levar a quantos lugares novos\n` (Kuon, 11_09)
- `I can, I think.` -> `eu puder, acho.` (Kuon, 11_09)
- `Like there's a wanderlust deep inside me, whispering\n` -> `Como se tivesse uma sede de viajar bem no fundo de mim, sussurrando\n` (Kuon, 11_09)
- `to my heart, you know?` -> `pro meu coração, sabe?` (Kuon, 11_09)
- `It wants to go places it's never been, have\n` -> `Ela quer ir a lugares onde nunca esteve, ter\n` (Kuon, 11_09)
- `experiences it's never had, try new things...` -> `experiências que nunca teve, provar coisas novas...` (Kuon, 11_09)
- `So as long as there are new places for me to take in\n` -> `Então enquanto houver lugares novos pra eu conhecer\n` (Kuon, 11_09)
- `like that, I'll continue my travels, I suppose.` -> `assim, vou continuar viajando, eu acho.` (Kuon, 11_09)
- `Kuon smiles sweetly, and I have to admit, the beauty\n` -> `A Kuon sorri doce, e admito, a beleza\n` (Haku, 11_09)
- `of it charms me a little.` -> `disso me encanta um pouco.` (Haku, 11_09)
- `Drinks that can only be found here, food that's only\n` -> `Bebidas que só se acham aqui, comida que só se\n` (Kuon, 11_09)
- `cooked there, seeing the sights...` -> `cozinha lá, ver as paisagens...` (Kuon, 11_09)
- `Traveling the open road, wandering a free world with\n` -> `Percorrer a estrada aberta, vagar por um mundo livre sem\n` (Kuon, 11_09)
- `no one to lecture me or force me to study...` -> `ninguém pra me dar sermão ou me obrigar a estudar...` (Kuon, 11_09)
- `Really, I have to wonder if this lifestyle is what\n` -> `Sério, fico me perguntando se esse estilo de vida é o\n` (Kuon, 11_09)
- `they mean when they talk about an earthly paradise.` -> `que chamam de paraíso na Terra.` (Kuon, 11_09)
- `...I feel like that last part somehow spoils the\n` -> `...Sinto que essa última parte meio que estraga o\n` (Haku, 11_09)
- `rest of it.` -> `resto.` (Haku, 11_09)
- `Doesn't your family worry, th--?` -> `Sua família não fica preocupada, en--?` (Haku, 11_09)
- `At that, Kuon's expression turns dark and\n` -> `Com isso, a expressão da Kuon fica sombria e\n` (Haku, 11_09)
- `distant.` -> `distante.` (Haku, 11_09)
- `Urk. Wrong thing to say?` -> `Ops. Falei besteira?` (Haku, 11_09)
- `A normal parent probably wouldn't let their\n` -> `Um pai normal provavelmente não deixaria a\n` (Haku, 11_09)
- `young daughter travel alone, much less\n` -> `filha jovem viajar sozinha, muito menos\n` (Haku, 11_09)
- `overseas, so...` -> `pro outro lado do mar, então...` (Haku, 11_09)
- `...Sorry. I didn't mean...` -> `...Desculpa. Eu não quis...` (Haku, 11_09)
- `Oh, no, it's all right.` -> `Ah, não, tá tudo bem.` (Kuon, 11_09)
- `I ran off without telling anyone, is all. I'm...\n` -> `Eu fugi sem avisar ninguém, só isso. Eu...\n` (Kuon, 11_09)
- `not exactly looking forward to the scolding waiting\n` -> `não tô exatamente ansiosa pela bronca que me\n` (Kuon, 11_09)
- `for me.` -> `espera.` (Kuon, 11_09)
- `What, that's all!?` -> `Quê, só isso!?` (Haku, 11_09)
- `Huh? What do you mean?` -> `Hein? Como assim?` (Kuon, 11_09)
- `That sullen face just now made me think you don't\n` -> `Aquela cara fechada agora me fez achar que você não\n` (Haku, 11_09)
- `have a family. And since I said, y'know--` -> `tinha família. E como eu falei, sabe--` (Haku, 11_09)
- `Family?` -> `Família?` (Kuon, 11_09)
- `Oooh, I see. No, no, I come from a pretty big\n` -> `Aaah, saquei. Não, não, eu venho de uma família bem\n` (Kuon, 11_09)
- `household.` -> `grande.` (Kuon, 11_09)
- `If that's the case, then it's f-- Actually, no, it's\n` -> `Se é assim, então tá tu-- Na verdade, não, não tá\n` (Haku, 11_09)
- `not fine! Won't they be worried about you?` -> `tudo bem! Eles não vão ficar preocupados com você?` (Haku, 11_09)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `My family is, ah... I suppose you could call them...\n` -> `Minha família é, ã... acho que dá pra chamar de...\n` (Kuon, 11_09)
- `Lenient?` -> `Tolerante?` (Kuon, 11_09)
- `Liar. If they were, you wouldn't be dreading the\n` -> `Mentirosa. Se fossem, você não estaria temendo a\n` (Haku, 11_09)
- `scolding they're gonna give you.` -> `bronca que vão te dar.` (Haku, 11_09)
- `I-It's true! They told me I should go where I like,\n` -> `É-É verdade! Me disseram pra eu ir aonde quiser\n` (Kuon, 11_09)
- `and do what I want.` -> `e fazer o que eu quiser.` (Kuon, 11_09)
- `One can only live free of responsibilities while one\n` -> `Só dá pra viver livre de responsabilidades enquanto se\n` (Kuon, 11_09)
- `is still young, so I'm seizing the day!` -> `é jovem, então estou aproveitando o dia!` (Kuon, 11_09)
- `It comes with dangers, of course--you can be left to\n` -> `Vem com perigos, claro--você pode acabar\n` (Kuon, 11_09)
- `die helpless, disgraced, far away from home...` -> `morrendo desamparada, desonrada, longe de casa...` (Kuon, 11_09)
- `But that's the trade-off that comes with freedom...\n` -> `Mas esse é o preço que vem com a liberdade...\n` (Kuon, 11_09)
- `Or so they said.` -> `Ou foi o que disseram.` (Kuon, 11_09)
- `How should I put it? My family... values autonomy.\n` -> `Como eu diria? Minha família... valoriza a autonomia.\n` (Kuon, 11_09)
- `Independence.` -> `Independência.` (Kuon, 11_09)
- `You'd think there'd be a rational limit to what\n` -> `Você pensaria que tem um limite racional pro que\n` (Haku, 11_09)
- `counts as "independence"...` -> `conta como "independência"...` (Haku, 11_09)
- `But enough of all that! Eat up. You'll need your\n` -> `Mas chega disso! Come. Você vai precisar de\n` (Kuon, 11_09)
- `strength for work tomorrow.` -> `energia pro trabalho amanhã.` (Kuon, 11_09)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `We're working... tomorrow, too...?` -> `A gente vai trabalhar... amanhã também...?` (Haku, 11_09)
- `Ah, let's see. Next I'll try... this, then this,\n` -> `Ah, deixa ver. Agora eu provo... este, depois este,\n` (Kuon, 11_09)
- `And then...` -> `e depois...` (Kuon, 11_02)
- `You're STILL eating!?` -> `Você AINDA tá comendo!?` (Haku, 11_09)
- `Somehow, Kuon managed to put a whole new amamunii\n` -> `De algum jeito, a Kuon montou um amamunii inteiro novo\n` (Haku, 11_09)
- `together while I was distracted. She eats eagerly.` -> `enquanto eu me distraía. Ela come com gosto.` (Haku, 11_09)
- `Mmf!` -> `Mmf!` (Kuon, 11_09)
- `I'll give her this--the girl really likes her food.` -> `Tenho que admitir uma coisa--a garota gosta mesmo de comer.` (Haku, 11_09)
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
| 0x1f560 | 16 | Let's eat! Ah... |
| 0x1f571 | 16 | *Hromf, munch--* |
| 0x1f586 | 28 | *--gulp* Mmf, that's good... |
| 0x1f5a3 | 53 | Spacing out over there? Come on, this is delicious.\n |
| 0x1f5d9 | 21 | You're not gonna eat? |
| 0x1f5ef | 10 | R-Right... |
| 0x1f5fa | 51 | It got dark outside while we were busy organizing\n |
| 0x1f62e | 17 | our belongings... |
| 0x1f640 | 52 | At some point, a tantalizing aroma wafted into the\n |
| 0x1f675 | 36 | room from somewhere else in the inn. |
| 0x1f69a | 53 | The scent tickled my nose and made my stomach growl\n |
| 0x1f6d0 | 14 | with hunger... |
| 0x1f6df | 45 | Chuckling, Kuon led me downstairs, where we\n |
| 0x1f70d | 52 | found a group of locals drinking and dining merrily. |
| 0x1f742 | 52 | Now, a staggering number of dishes are lined up on\n |
| 0x1f777 | 20 | the table before us. |
| 0x1f78c | 41 | Geez. What's with these portions, though? |
| 0x1f7b6 | 51 | The plates are all stacked so high with food they\n |
| 0x1f7ea | 51 | threaten to topple. This is way too much for two... |
| 0x1f81e | 50 | Hell, there's enough food crowding the table for\n |
| 0x1f851 | 20 | at least TEN people. |
| 0x1f866 | 53 | Oblivious to my dumbfounded state, Kuon reaches for\n |
| 0x1f89c | 36 | a plate and hums happily to herself. |
| 0x1f8c1 | 48 | Mm, and I'll try... this one, and this one next! |
| 0x1f8f2 | 50 | She piles heaps of meat and vegetables onto some\n |
| 0x1f925 | 46 | kind of thin dough, wrapping it all up neatly. |
| 0x1f954 | 21 | *Grmf, hrmf, munch--* |
| 0x1f96a | 51 | The wrap, bursting at the seams with ingredients,\n |
| 0x1f99e | 34 | disappears in just a few bites...! |
| 0x1f9c1 | 52 | Kuon opens her mouth wide and stuffs her face, but\n |
| 0x1f9f6 | 35 | somehow, she makes it look refined. |
| 0x1fa1a | 51 | Don't hold back, OK? We're celebrating you making\n |
| 0x1fa4e | 20 | it back here safely. |
| 0x1fa63 | 39 | While I'm happy to hear you say that... |
| 0x1fa8b | 54 | This all looks like quite a feast. I hope she didn't\n |
| 0x1fac2 | 22 | splurge for my sake... |
| 0x1fad9 | 51 | Well, if you aren't eating, I'll just help myself\n |
| 0x1fb0d | 12 | to the rest. |
| 0x1fb1a | 7 | ...Huh? |
| 0x1fb22 | 37 | Ahhh... *Grmf, hromf--munch, munch--* |
| 0x1fb48 | 25 | D-Did she say "the rest"? |
| 0x1fb62 | 49 | Oh, right. Do you not know how to eat this, Haku? |
| 0x1fb94 | 24 | Um, well. Not... really. |
| 0x1fbad | 53 | I nod unconsciously, not quite able to tell her I'm\n |
| 0x1fbe3 | 39 | more taken aback by the sheer quantity. |
| 0x1fc0b | 34 | Well, then! Allow me to teach you. |
| 0x1fc2e | 52 | From the plate in front of her, Kuon grabs another\n |
| 0x1fc63 | 40 | one of those thin sheets of flatbread... |
| 0x1fc8c | 34 | First, we get the amam skin ready. |
| 0x1fcaf | 5 | This? |
| 0x1fcb5 | 49 | I pick up another of the flimsy, doughy sheets,\n |
| 0x1fce7 | 48 | watching it pillow pliantly around my fingers... |
| 0x1fd18 | 48 | She called it a "skin," but it looks like it's\n |
| 0x1fd49 | 52 | grain pounded and baked like flatbread, not actual\n |
| 0x1fd7e | 12 | animal hide. |
| 0x1fd8b | 50 | That grain we carried earlier was amam. It turns\n |
| 0x1fdbe | 52 | into this after you grind it into flour and bake it. |
| 0x1fdf3 | 52 | You put ingredients like cooked meats, vegetables,\n |
| 0x1fe28 | 43 | or fish in the middle, then wrap it all up! |
| 0x1fe54 | 51 | One finished amamunii. Dip in your favorite sauce\n |
| 0x1fe88 | 10 | and enjoy! |
| 0x1fe93 | 46 | Kuon hands me the amam-wrapped bundle of food. |
| 0x1fec2 | 25 | Talk about extra large... |
| 0x1fedc | 44 | The skin looks like it's fit to burst. She\n |
| 0x1ff09 | 28 | definitely overstuffed this. |
| 0x1ff26 | 53 | As I stare in disbelief at mine, Kuon makes another\n |
| 0x1ff5c | 25 | just like it and digs in. |
| 0x1ff76 | 51 | Persuaded, I take a careful bite, cautious not to\n |
| 0x1ffaa | 31 | let any of the filling spill... |
| 0x1ffca | 21 | *Munch, munch*... Mm. |
| 0x1ffe0 | 49 | OK, yeah. That's pretty good. A little heavy on\n |
| 0x20012 | 30 | the seasoning, but still good. |
| 0x20031 | 49 | And it tastes even better since it's a free meal. |
| 0x20063 | 54 | Eh heh heh. I may not look it, but I'm a pretty good\n |
| 0x2009a | 5 | cook. |
| 0x200a0 | 20 | Kuon smiles proudly. |
| 0x200b5 | 52 | ...I don't think being able to wrap things up in a\n |
| 0x200ea | 44 | skin makes you a cook, but whatever you say. |
| 0x20117 | 53 | I manage to bite my tongue before the quip actually\n |
| 0x2014d | 18 | escapes my throat. |
| 0x20160 | 14 | *Mmf, gromf--* |
| 0x2016f | 52 | It's certainly delicious, but I'm getting parched.\n |
| 0x201a4 | 23 | Probably the seasoning. |
| 0x201bc | 30 | Is there anything to drink...? |
| 0x201db | 5 | Here. |
| 0x201e1 | 50 | As though reading my mind, Kuon slides a bowl of\n |
| 0x20214 | 32 | amber-colored liquid towards me. |
| 0x20235 | 11 | Oh, thanks. |
| 0x20241 | 51 | I take an experimental sip, tasting the beverage... |
| 0x20275 | 45 | It has an odd, citrusy flavor, but it's not\n |
| 0x202a3 | 53 | overpowering--in fact, it cleanses my palate pretty\n |
| 0x202d9 | 7 | nicely. |
| 0x202e1 | 19 | Is this... alcohol? |
| 0x202f5 | 48 | Uh huh. It's a drink you'll find a lot in this\n |
| 0x20326 | 49 | region. It's not too strong, so it's drunk with\n |
| 0x20358 | 15 | meals, usually. |
| 0x20368 | 14 | Interesting... |
| 0x20377 | 50 | It almost seems like beer, but that citrus taste\n |
| 0x203aa | 37 | distinguishes it from standard lager. |
| 0x203d0 | 51 | I like it. The bubbles and the sourness go nicely\n |
| 0x20404 | 41 | with the heavy seasoning on these dishes. |
| 0x2042e | 53 | And we don't really have it in my homeland! So it's\n |
| 0x20464 | 22 | still a novelty to me. |
| 0x2047b | 9 | Homeland? |
| 0x20485 | 34 | You're not from around here, then? |
| 0x204a8 | 51 | Hm? Yeah, I'm from across the sea. It was a rough\n |
| 0x204dc | 28 | voyage getting here, though. |
| 0x204f9 | 51 | I see. I don't know what part of the world you're\n |
| 0x2052d | 44 | from, but that... sounds like it's far away. |
| 0x2055a | 50 | Uh huh. I've traveled a lot since I was a child,\n |
| 0x2058d | 51 | but this is the first time I've been out this far\n |
| 0x205c1 | 10 | on my own. |
| 0x205cc | 49 | It was also my first time traveling by ship, so\n |
| 0x205fe | 47 | getting that new experience was fun in the end. |
| 0x2062e | 40 | We did have a few close calls, though... |
| 0x20657 | 50 | What, like you got caught in a storm or something? |
| 0x2068a | 48 | Kuon puts a finger to her lips, smiling proudly. |
| 0x206bb | 51 | It wasn't a storm, but we ran into something just\n |
| 0x206ef | 30 | about as scary. Can you guess? |
| 0x2070e | 50 | Something close to a storm... Like a tsunami, or\n |
| 0x20741 | 18 | a giant whirlpool? |
| 0x20754 | 51 | Too bad! Both wrong. The correct answer is "giant\n |
| 0x20788 | 20 | sea monster attack." |
| 0x2079d | 3 | Um. |
| 0x207a1 | 52 | It happened on a calm, sunny day, and the ship had\n |
| 0x207d6 | 34 | a lot of people packed belowdecks. |
| 0x207f9 | 51 | The water was peaceful, so I thought I'd go above\n |
| 0x2082d | 27 | and watch the waves, but... |
| 0x20849 | 54 | When I got up there, I was just in time to see giant\n |
| 0x20880 | 48 | arms--more like legs--emerge and seize the ship! |
| 0x208b1 | 51 | It tried to pull us beneath the surface, drowning\n |
| 0x208e5 | 42 | anyone who fell off--it was awful, really. |
| 0x20910 | 38 | That's... nowhere near "like" a storm. |
| 0x20937 | 50 | Hold on. You're just pulling my leg, aren't you?\n |
| 0x2096a | 26 | This is some kind of joke. |
| 0x20985 | 7 | A joke? |
| 0x2098d | 32 | Kuon tilts her head quizzically. |
| 0x209ae | 14 | ...Never mind. |
| 0x209bd | 50 | I'm starting to get a headache trying to wrap my\n |
| 0x209f0 | 45 | head around this. Time to change the subject. |
| 0x20a1e | 53 | So, I'm curious. Why are you traveling? Do you have\n |
| 0x20a54 | 39 | some goal way out here--some objective? |
| 0x20a7c | 12 | Objective... |
| 0x20a89 | 48 | If it's hard to talk about, you don't have to... |
| 0x20aba | 53 | Oh, no, nothing like that. I just haven't had to...\n |
| 0x20af0 | 31 | Well, put it into words before. |
| 0x20b10 | 53 | I just want to take myself to as many new places as\n |
| 0x20b46 | 15 | I can, I think. |
| 0x20b56 | 54 | Like there's a wanderlust deep inside me, whispering\n |
| 0x20b8d | 22 | to my heart, you know? |
| 0x20ba4 | 45 | It wants to go places it's never been, have\n |
| 0x20bd2 | 45 | experiences it's never had, try new things... |
| 0x20c00 | 54 | So as long as there are new places for me to take in\n |
| 0x20c37 | 47 | like that, I'll continue my travels, I suppose. |
| 0x20c67 | 54 | Kuon smiles sweetly, and I have to admit, the beauty\n |
| 0x20c9e | 25 | of it charms me a little. |
| 0x20cb8 | 54 | Drinks that can only be found here, food that's only\n |
| 0x20cef | 34 | cooked there, seeing the sights... |
| 0x20d12 | 54 | Traveling the open road, wandering a free world with\n |
| 0x20d49 | 44 | no one to lecture me or force me to study... |
| 0x20d76 | 52 | Really, I have to wonder if this lifestyle is what\n |
| 0x20dab | 51 | they mean when they talk about an earthly paradise. |
| 0x20ddf | 50 | ...I feel like that last part somehow spoils the\n |
| 0x20e12 | 11 | rest of it. |
| 0x20e1e | 32 | Doesn't your family worry, th--? |
| 0x20e3f | 43 | At that, Kuon's expression turns dark and\n |
| 0x20e6b | 8 | distant. |
| 0x20e74 | 24 | Urk. Wrong thing to say? |
| 0x20e8d | 45 | A normal parent probably wouldn't let their\n |
| 0x20ebb | 40 | young daughter travel alone, much less\n |
| 0x20ee4 | 15 | overseas, so... |
| 0x20ef4 | 26 | ...Sorry. I didn't mean... |
| 0x20f0f | 23 | Oh, no, it's all right. |
| 0x20f27 | 50 | I ran off without telling anyone, is all. I'm...\n |
| 0x20f5a | 53 | not exactly looking forward to the scolding waiting\n |
| 0x20f90 | 7 | for me. |
| 0x20f98 | 18 | What, that's all!? |
| 0x20fab | 22 | Huh? What do you mean? |
| 0x20fc2 | 51 | That sullen face just now made me think you don't\n |
| 0x20ff6 | 41 | have a family. And since I said, y'know-- |
| 0x21020 | 7 | Family? |
| 0x21028 | 47 | Oooh, I see. No, no, I come from a pretty big\n |
| 0x21058 | 10 | household. |
| 0x21063 | 54 | If that's the case, then it's f-- Actually, no, it's\n |
| 0x2109a | 42 | not fine! Won't they be worried about you? |
| 0x210c5 | 7 | Nngh... |
| 0x210cd | 54 | My family is, ah... I suppose you could call them...\n |
| 0x21104 | 8 | Lenient? |
| 0x2110d | 50 | Liar. If they were, you wouldn't be dreading the\n |
| 0x21140 | 32 | scolding they're gonna give you. |
| 0x21161 | 53 | I-It's true! They told me I should go where I like,\n |
| 0x21197 | 19 | and do what I want. |
| 0x211ab | 54 | One can only live free of responsibilities while one\n |
| 0x211e2 | 39 | is still young, so I'm seizing the day! |
| 0x2120a | 54 | It comes with dangers, of course--you can be left to\n |
| 0x21241 | 46 | die helpless, disgraced, far away from home... |
| 0x21270 | 53 | But that's the trade-off that comes with freedom...\n |
| 0x212a6 | 16 | Or so they said. |
| 0x212b7 | 52 | How should I put it? My family... values autonomy.\n |
| 0x212ec | 13 | Independence. |
| 0x212fa | 49 | You'd think there'd be a rational limit to what\n |
| 0x2132c | 27 | counts as "independence"... |
| 0x21348 | 50 | But enough of all that! Eat up. You'll need your\n |
| 0x2137b | 27 | strength for work tomorrow. |
| 0x21397 | 8 | Wh-What? |
| 0x213a0 | 34 | We're working... tomorrow, too...? |
| 0x213c3 | 50 | Ah, let's see. Next I'll try... this, then this,\n |
| 0x213f6 | 11 | and then... |
| 0x21402 | 21 | You're STILL eating!? |
| 0x21418 | 51 | Somehow, Kuon managed to put a whole new amamunii\n |
| 0x2144c | 50 | together while I was distracted. She eats eagerly. |
| 0x2147f | 4 | Mmf! |
| 0x21484 | 51 | I'll give her this--the girl really likes her food. |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_09.json` com a forma:
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
