# Cena ch_15_06 — pacote de traducao (233 linhas)

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
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ukon | Personagem | Ukon | manter_original | major |

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
- `Ah, good, everyone's here.` -> `Ah, ótimo, estão todos aqui.` (Ukon, 15_06)
- `Ukon plonks himself down in the middle of the\n` -> `Ukon se joga no meio do\n` (Narrador, 15_06)
- `hall, and everyone gathers to sit around him.` -> `salão, e todos se reúnem ao redor dele.` (Narrador, 15_06)
- `What brings you here on such short notice,\n` -> `O que te traz aqui assim de repente,\n` (Haku, 15_06)
- `dear brother?` -> `caro irmão?` (Nekone, 15_01)
- `Well, I think I'm gonna have work for you guys\n` -> `Bom, acho que logo vou ter trabalho pra vocês\n` (Ukon, 15_06)
- `soon. As undercover agents.` -> `em breve. Como agentes infiltrados.` (Ukon, 15_06)
- `Undercover... agents.` -> `Agentes... infiltrados.` (Haku, 15_06)
- `No one is quite sure how to react.` -> `Ninguém sabe bem como reagir.` (Narrador, 15_06)
- `Ukon--Oshtor--can't really move in public\n` -> `Ukon--Oshtor--não pode se mover em público\n` (Haku, 15_06)
- `because of his position as Imperial Guard of\n` -> `por causa do cargo de Guarda Imperial da\n` (Haku, 15_06)
- `the Right...` -> `Direita...` (Haku, 15_06)
- `...So it falls to us to work in his stead.` -> `...Então cabe a nós agir no lugar dele.` (Haku, 15_06)
- `The only question is, what is he going to make\n` -> `A única questão é: o que ele vai nos mandar\n` (Haku, 15_06)
- `us do...?` -> `fazer...?` (Haku, 15_06)
- `Hey, relax a little. It's your first job, so\n` -> `Ei, relaxem um pouco. É o primeiro serviço,\n` (Ukon, 15_06)
- `I've picked out a few nice and easy contracts.` -> `então escolhi alguns contratos bem tranquilos.` (Ukon, 15_06)
- `Ukon produces a worn, dog-eared notebook,\n` -> `Ukon tira uma caderneta surrada e cheia de\n` (Narrador, 15_06)
- `leafing through the pages carefully.` -> `orelhas, folheando com cuidado.` (Narrador, 15_06)
- `I'll read these off in order, and you guys\n` -> `Vou ler na ordem, e vocês me dizem\n` (Ukon, 15_06)
- `tell me what sounds good. Starting with...` -> `o que parece bom. Começando com...` (Ukon, 15_06)
- `First up, cleaning up the restroom area in the\n` -> `Primeiro: limpar a área dos banheiros na\n` (Ukon, 15_06)
- `plaza.` -> `praça.` (Ukon, 15_06)
- `Second one's transporting the, ah, by-products\n` -> `O segundo é transportar os, ah, subprodutos\n` (Ukon, 15_06)
- `of that process...` -> `desse processo...` (Ukon, 15_06)
- `Third, stirring the contents of the cesspool\n` -> `Terceiro: mexer o conteúdo da fossa\n` (Ukon, 15_06)
- `so it doesn't stagnate...` -> `pra não deixar estagnar...` (Ukon, 15_06)
- `And then the fourth job is taking THAT stuff\n` -> `E o quarto serviço é pegar AQUILO tudo\n` (Ukon, 15_06)
- `and--` -> `e--` (Ukon, 15_06)
- `Wait. Wait a second.` -> `Espera. Espera um segundo.` (Haku, 15_06)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `You can talk around it all you like, but, uh.\n` -> `Pode enrolar à vontade, mas, hm.\n` (Haku, 15_06)
- `There seems to be a... common theme to these\n` -> `Parece haver um... tema em comum nesses\n` (Haku, 15_06)
- `jobs.` -> `serv.` (Haku, 15_06)
- `Ah, not much I can do about that.` -> `Ah, não tem muito o que fazer.` (Ukon, 15_06)
- `What... else do you have?` -> `Que... mais você tem?` (Haku, 15_06)
- `Well, uh. There's one concerning a peruko named\n` -> `Bom, hm. Tem um sobre uma peruko chamada\n` (Ukon, 15_06)
- `Hanako suffering from constipation, wh--` -> `Hanako sofrendo de constipação, q--` (Ukon, 15_06)
- `Like I said, why are they all like that?\n` -> `Como já disse, por que são todos assim?\n` (Haku, 15_06)
- `You've gotta have SOMEthing different.` -> `Você tem que ter ALGUMA coisa diferente.` (Haku, 15_06)
- `B-Brother...` -> `I-Irmão...` (Nekone, 15_06)
- `It may not seem it, but these are the easiest\n` -> `Pode não parecer, mas esses são os serviços\n` (Ukon, 15_06)
- `jobs I have for you.` -> `mais fáceis que tenho.` (Ukon, 15_06)
- `Ukon. Stop fooling around and give us our\n` -> `Ukon. Para de enrolar e nos dê nossas\n` (Kuon, 15_06)
- `choices.` -> `opções.` (Kuon, 15_06)
- `I'm not fooling around.` -> `Não estou enrolando.` (Ukon, 15_06)
- `Yeah, you'll have to endure some...\n` -> `É, vão ter que aguentar algumas...\n` (Ukon, 15_06)
- `unpleasantness. But these are safe, profitable\n` -> `coisas ruins. Mas são seguros e lucrativos\n` (Ukon, 15_06)
- `gigs apart from that.` -> `fora isso.` (Ukon, 15_06)
- `All right, all right, don't give me that\n` -> `Tá bom, tá bom, para de me olhar assim\n` (Ukon, 15_06)
- `murder-stare. Good grief. How about... this one?` -> `com essa cara. Nossa. Que tal... este aqui?` (Ukon, 15_06)
- `Ukon flips to another page, then hands the\n` -> `Ukon vira a página e passa a caderneta\n` (Narrador, 15_06)
- `notebook to Kuon.` -> `para Kuon.` (Narrador, 15_06)
- `A kyorori hunt?` -> `Uma caça ao kyorori?` (Kuon, 15_06)
- `Yep. Job entails going out into the mountains\n` -> `Isso. O serviço é ir às montanhas\n` (Ukon, 15_06)
- `and capturing a wild animal called a kyorori.` -> `e capturar um animal selvagem chamado kyorori.` (Ukon, 15_06)
- `Huh. That sounds good, don't you think?` -> `Hm. Parece bom, não acha?` (Haku, 15_06)
- `And what exactly is this... kyorori?` -> `E o que exatamente é um... kyorori?` (Kuon, 15_06)
- `They're birds that inhabit the frontier.` -> `São aves que habitam a fronteira.` (Ukon, 15_06)
- `Big suckers. Five times a person's height,\n` -> `Grandões. Cinco vezes a altura de uma pessoa,\n` (Ukon, 15_06)
- `feathers tough as stone, armor-shredding beak\n` -> `penas duras que nem pedra, bico e garras\n` (Ukon, 15_06)
- `and talons...` -> `e garras...` (Ukon, 15_06)
- `Ferociously carnivorous, 'course.` -> `Feroz e carnívoro, claro.` (Ukon, 15_06)
- `Oh, and there's matarii fishing.` -> `Ah, e tem a pesca de matarii.` (Ukon, 15_06)
- `...And how many times larger than a person is\n` -> `...E quantas vezes maior que uma pessoa é\n` (Haku, 15_06)
- `this matarii, pray tell?` -> `esse matarii, se me permite?` (Haku, 15_06)
- `Oh, not all that, y'know? Like... about yea\n` -> `Ah, nada disso, sabe? Tipo... assim\n` (Ukon, 15_06)
- `big.` -> `ó.` (Ukon, 15_06)
- `Ukon holds up his hands, perhaps shoulder-width\n` -> `Ukon levanta as mãos, talvez à largura\n` (Narrador, 15_06)
- `apart.` -> `ombros.` (Narrador, 15_06)
- `Then is it very ferocious, or...?` -> `Então ele é muito feroz, ou...?` (Haku, 15_06)
- `Nope. Regular old fish.` -> `Que nada. Peixe normal e comum.` (Ukon, 15_06)
- `It's pretty good grilled. Nice and tender.` -> `É ótimo grelhado. Macio e saboroso.` (Ukon, 15_06)
- `Um, ah--about matarii, though...?` -> `Hm, ah--sobre o matarii...?` (Kiwru, 15_06)
- `You know something about them, Kiwru?` -> `Você sabe algo sobre eles, Kiwru?` (Haku, 15_06)
- `It's a... fairly famous delicacy, traded at\n` -> `É uma... iguaria bem famosa, negociada a\n` (Kiwru, 15_06)
- `high prices. U-Usually you serve it at\n` -> `preços altos. G-Geralmente serve em\n` (Kiwru, 15_06)
- `celebrations...` -> `celebrações...` (Kiwru, 15_06)
- `Regular fish that fetch a high price, huh?\n` -> `Peixe comum que vale caro, hein?\n` (Haku, 15_06)
- `Sounds like a good deal to me.` -> `Parece ótimo pra mim.` (Haku, 15_06)
- `Eh? But aren't those...` -> `Hein? Mas não são aqueles...` (Kiwru, 15_06)
- `Ukon watches in silence as we discuss, a smirk\n` -> `Ukon observa em silêncio enquanto conversamos,\n` (Narrador, 15_06)
- `on his face.` -> `sorrindo.` (Narrador, 15_06)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `Yes, i-if I recall, they only inhabit the\n` -> `S-Se bem me lembro, eles só habitam os\n` (Kiwru, 15_06)
- `frozen seas north of here.` -> `mares gelados ao norte daqui.` (Kiwru, 15_06)
- `A-And what's more, the waves are routinely\n` -> `A-Além disso, as ondas são constantemente\n` (Kiwru, 15_06)
- `rough, and the reefs... Even seasoned sailors\n` -> `violentas, e os recifes... Até marinheiros\n` (Kiwru, 15_06)
- `often die in those waters.` -> `experientes morrem nessas águas.` (Kiwru, 15_06)
- `Nope. Rejecting that one.` -> `Não. Fora essa.` (Haku, 15_06)
- `Come on, I went through all the trouble of\n` -> `Vamos lá, dei trabalho pra encontrar\n` (Ukon, 15_06)
- `finding deals that work out for you. Don't be\n` -> `contratos que valham a pena pra vocês. Não\n` (Ukon, 15_06)
- `a buzzkill.` -> `sejam chatos.` (Ukon, 15_06)
- `"Work out for us?" That one is straight-up\n` -> `"Valha a pena pra nós?" Aquele era\n` (Haku, 15_06)
- `life-threatening.` -> `risco de vida puro.` (Haku, 15_06)
- `Cripes. Picky, picky. Here--there's another\n` -> `Nossa. Enjoados, enjoados. Aqui--tem outro\n` (Ukon, 15_06)
- `contract for capturing a furomun.` -> `contrato pra capturar um furomun.` (Ukon, 15_06)
- `Dear brother, isn't that...?` -> `Caro irmão, não é aquele...?` (Nekone, 15_06)
- `They're extremely venomous. In concentrate,\n` -> `São extremamente venenosos. Concentrado,\n` (Kuon, 15_06)
- `one animal's worth of venom is enough to kill\n` -> `o veneno de um único animal é suficiente\n` (Kuon, 15_06)
- `hundreds.` -> `centenas.` (Kuon, 15_06)
- `Extreme care is required to handle it, but if\n` -> `Requer extremo cuidado no manuseio, mas\n` (Kuon, 15_06)
- `prepared properly, its liver can treat heart\n` -> `se preparado corretamente, seu fígado trata\n` (Kuon, 15_06)
- `diseases.` -> `do coração.` (Kuon, 15_06)
- `Color me impressed, missy. Its venom can be\n` -> `Boa, moça. O veneno também pode ser\n` (Ukon, 15_06)
- `airborne, too--breathe any of it in, and it\n` -> `transmitido pelo ar--respire qualquer parte,\n` (Ukon, 15_06)
- `can knock you out cold.` -> `e você apaga na hora.` (Ukon, 15_06)
- `...I thought so.` -> `...Já desconfiava.` (Kuon, 15_06)
- `So you don't have anything, like... safer?` -> `Então não tem nada mais, tipo... seguro?` (Haku, 15_06)
- `Hey, listen. Safe, sweet deals that turn a\n` -> `Ei, escuta. Serviços seguros e lucrativos\n` (Ukon, 15_06)
- `good profit are hard to come by.` -> `são difíceis de achar.` (Ukon, 15_06)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `And sanitation is important work.\n` -> `E saneamento é um trabalho importante.\n` (Ukon, 15_06)
- `It prevents the spread of disease.` -> `Previne a propagação de doenças.` (Ukon, 15_06)
- `It's a dirty job, but someone's gotta do it.\n` -> `É um serviço sujo, mas alguém tem que fazer.\n` (Ukon, 15_06)
- `You understand, don't you, kid?` -> `Você entende, né, garoto?` (Ukon, 15_06)
- `He's got us there.` -> `Ele tem razão.` (Haku, 15_06)
- `It's a stroke of luck this is even available!\n` -> `É uma sorte incrível isso estar disponível!\n` (Ukon, 15_06)
- `It may be a shitty job, but I trust you'll\n` -> `Pode ser um serviço de merda, mas confio\n` (Ukon, 15_06)
- `toil-it through.` -> `topa o ralo.` (Ukon, 15_06)
- `...Ukon?` -> `...Ukon?` (Haku, 12_17)
- `All right, all right. Relax. Let's move onto\n` -> `Tá bom, tá bom. Relaxem. Vamos ao\n` (Ukon, 15_06)
- `our main subject for now.` -> `assunto principal por agora.` (Ukon, 15_06)
- `Ukon flashes his typical, fearless smile,\n` -> `Ukon abre aquele sorriso típico e destemido,\n` (Narrador, 15_06)
- `posture relaxing slightly.` -> `relaxando levemente a postura.` (Narrador, 15_06)
- `Main subject?` -> `Assunto principal?` (Haku, 15_06)
- `Yeah. You remember the bandits we captured\n` -> `Isso. Lembram dos bandidos que capturamos\n` (Ukon, 15_06)
- `before?` -> `antes?` (Ukon, 15_06)
- `Bandits... You mean the ones that attacked us\n` -> `Bandidos... Os que nos atacaram\n` (Haku, 15_06)
- `on the way to the capital?` -> `no caminho para a capital?` (Haku, 15_06)
- `Is something up with them?` -> `Aconteceu algo com eles?` (Haku, 15_06)
- `You could say that. Seems they escaped custody\n` -> `Pode-se dizer que sim. Parece que escaparam\n` (Ukon, 15_06)
- `after their court sentencing.` -> `após a sentença no tribunal.` (Ukon, 15_06)
- `From what I've heard, they still had comrades\n` -> `Pelo que soube, ainda tinham comparsas\n` (Ukon, 15_06)
- `on the outside who hit their escort during\n` -> `lá fora que atacaram a escolta durante\n` (Ukon, 15_06)
- `transit.` -> `o traslado.` (Ukon, 15_06)
- `So... th-those men...` -> `Então... e-esses homens...` (Haku, 15_06)
- `It can only be called carelessness.` -> `Só pode ser chamado de descuido.` (Kuon, 15_06)
- `A bit of luck, though. Eyewitness reports\n` -> `Uma sorte, porém. Testemunhas os viram\n` (Ukon, 15_06)
- `place them here in the capital, hiding out in\n` -> `aqui na capital, se escondendo\n` (Ukon, 15_06)
- `the city.` -> `da cidade.` (Haku, 14_02)
- `And you want us to find and apprehend them.\n` -> `E você quer que a gente os encontre e prenda.\n` (Haku, 15_06)
- `Am I right?` -> `Estou certo?` (Haku, 15_06)
- `Is that so...? I see. Is this my first test?` -> `Então é isso...? Entendo. Este é meu primeiro teste?` (Haku, 15_06)
- `If that's the case, I'll be sure to exceed your\n` -> `Nesse caso, certifique-se de que vou superar\n` (Haku, 15_06)
- `expectations!` -> `suas expectativas!` (Haku, 15_06)
- `Well, hold on. I do want you to find them,\n` -> `Calma. Quero que os encontrem,\n` (Ukon, 15_06)
- `but when you do, don't try to capture them.\n` -> `mas quando acharem, não tentem prendê-los.\n` (Ukon, 15_06)
- `Just call me.` -> `Me chamem.` (Ukon, 15_06)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `I don't want you trying to take them on your\n` -> `Não quero vocês tentando enfrentá-los\n` (Ukon, 15_06)
- `own.` -> `si.` (Ukon, 15_06)
- `In other words... Your honor takes a hit if you\n` -> `Em outras palavras... Sua honra sai machucada\n` (Haku, 15_06)
- `don't bring them back yourself. Your men, your\n` -> `se não os trouxer você mesmo. Seus homens,\n` (Haku, 15_06)
- `problem.` -> `seu prob.` (Haku, 15_06)
- `Cripes, at least let me get a word in edgewise,\n` -> `Nossa, pelo menos me deixa falar,\n` (Ukon, 15_06)
- `here. I shouldn't have to tell you this, but...` -> `aqui. Nem precisaria dizer isso, mas...` (Ukon, 15_06)
- `They probably remember your faces. If you engage\n` -> `Eles provavelmente lembram das suas caras. Se\n` (Ukon, 15_06)
- `them directly, chances are, they'll want blood.` -> `confrontados diretamente, vão querer sangue.` (Ukon, 15_06)
- `Truth is, we don't have much more than\n` -> `A verdade é que não temos muito mais que\n` (Ukon, 15_06)
- `eyewitness accounts. No hard clues as to where\n` -> `relatos de testemunhas. Nenhuma pista concreta\n` (Ukon, 15_06)
- `they're hiding.` -> `do esconderijo.` (Ukon, 15_06)
- `And they don't want to be found. Searching\n` -> `E eles não querem ser encontrados. Busca\n` (Ukon, 15_06)
- `randomly won't do us any good, but we can't\n` -> `aleatória não vai adiantar, mas não podemos\n` (Ukon, 15_06)
- `just do nothing.` -> `ficar parados.` (Ukon, 15_06)
- `With all that in mind, I'd like to ask you guys\n` -> `Com tudo isso em mente, gostaria que\n` (Ukon, 15_06)
- `to patrol the capital for me, and to just...\n` -> `patrulhassem a capital pra mim, e só...\n` (Ukon, 15_06)
- `stay alert.` -> `fiquem atentos.` (Ukon, 15_06)
- `If that's all, I don't think we have any reason\n` -> `Se é só isso, acho que não temos motivo\n` (Haku, 15_06)
- `to turn you down.` -> `para recusar.` (Haku, 15_06)
- `Next to the, uh... dirtier requests, this\n` -> `Comparado com os pedidos mais... sujos,\n` (Haku, 15_06)
- `sounds pretty manageable.` -> `parece bem tranquilo.` (Haku, 15_06)
- `And all we have to do if we find anything is\n` -> `E tudo que precisamos fazer se acharmos algo\n` (Haku, 15_06)
- `contact Ukon. No problem.` -> `é contatar Ukon. Sem problema.` (Haku, 15_06)
- `All right. We're in.` -> `Tá bom. Estamos dentro.` (Haku, 15_06)
- `So, we took the request for the time being,\n` -> `Então, aceitamos o pedido por enquanto,\n` (Narrador, 15_06)
- `but...` -> `mas...` (Kuon, 12_16)
- `Um... What exactly do we... do now?` -> `Hm... O que exatamente fazemos... agora?` (Haku, 15_06)
- `Well...` -> `Bom...` (Haku, 12_03)
- `Searching for these bandits at random isn't\n` -> `Procurar esses bandidos aleatoriamente não\n` (Haku, 15_06)
- `going to be any kind of efficient.` -> `vai ser eficiente.` (Haku, 15_06)
- `In this situation, it may be best to put\n` -> `Nessa situação, talvez seja melhor se colocar\n` (Kuon, 15_06)
- `ourselves in their shoes and act based on that.` -> `no lugar deles e agir com base nisso.` (Kuon, 15_06)
- `Thinking of things from their perspective,\n` -> `Pensando pelas perspectivas deles,\n` (Kuon, 15_06)
- `Huh...` -> `Hum...` (Ukon, 15_05)
- `To be honest, I can't say I have any clue WHAT\n` -> `Sinceramente, não faço ideia do que\n` (Haku, 15_06)
- `they're thinking.` -> `eles estão pensando.` (Haku, 15_06)
- `Logically, one would seek out a hiding place\n` -> `Logicamente, alguém buscaria um esconderijo\n` (Kuon, 15_06)
- `to lie low and wait out the storm, but...` -> `para se esconder e esperar a poeira baixar, mas...` (Kuon, 15_06)
- `If it were me, I'd probably go out and find a\n` -> `Se fosse eu, provavelmente sairia pra achar\n` (Haku, 15_06)
- `way to live it up. Celebrate my newfound\n` -> `uma forma de curtir. Celebrar a liberdade\n` (Haku, 15_06)
- `freedom.` -> `liberdade.` (Haku, 15_06)
- `Of course your mind would go there. Please,\n` -> `Claro que sua cabeça ia por aí. Por favor,\n` (Kuon, 15_06)
- `try to treat this at least somewhat seriously.` -> `trate isso com um mínimo de seriedade.` (Kuon, 15_06)
- `I'm just saying. Knowing me, that's what I'd\n` -> `Estou só dizendo. Conhecendo a mim, é o que\n` (Haku, 15_06)
- `do.` -> `faria.` (Haku, 15_06)
- `What manner of imbecile would risk attracting\n` -> `Que tipo de imbecil arriscaria atrair\n` (Maroro, 15_06)
- `such attention while the law seeks his head?` -> `tal atenção com a lei em shuas costas?` (Maroro, 15_06)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `Man` -> `Hom` (Sistema, 12_04)
- `Whup! Sorry, miss. Wasn't payin' attention.` -> `Opa! Desculpa, moça. Não tava prestando atenção.` (Bandido, 15_06)
- `N-No, that's all right... I-I'm sorry...` -> `N-Não, tá tudo bem... D-Desculpe...` (Garota, 15_06)
- `Don't worry 'bout it. See ya later, cutie.` -> `Não se preocupa. Até mais, lindinha.` (Bandido, 15_06)
- `Henchman` -> `Capanga` (Sistema, 15_06)
- `Ah! Hey, boss, come check out this bath!\n` -> `Ah! Ei, chefe, vem ver esse banho!\n` (Capanga, 15_06)
- `Thing's freakin' HUGE.` -> `Isso aqui é ENORME.` (Capanga, 15_06)
- `Not bad, not bad! Ain't nothin' like a nice\n` -> `Nada mau, nada mau! Não tem nada como uma\n` (Bandido Chefe, 15_06)
- `drink in a hot bath!` -> `bebida num banho quente!` (Bandido Chefe, 15_06)
- `It's been too long since we been on the outside!\n` -> `Faz tempo demais que não ficamos do lado de fora!\n` (Bandido Chefe, 15_06)
- `We gotta live it large. Large, damn it!` -> `Temos que viver no máximo. No MÁXIMO!` (Bandido Chefe, 15_06)
- `Damn straight! Nothing better'n...\n` -> `Com certeza! Nada melhor que...\n` (Capanga, 15_06)
- `Ah... Uhm...` -> `Ah... Hm...` (Garota, 15_06)
- `Wh--Y-Y-You guys!?` -> `Q-Qu--V-Vocês!?` (Bandido, 15_06)
- `A-Ah...` -> `A-Ah...` (Garota, 15_06)
- `YOU guys!?` -> `VOCÊS!?` (Haku, 15_06)
- `You--You're those--From that one time we--?` -> `Voc--Vocês são aqueles--Daquela vez que--?` (Haku, 15_06)
- `N-No... No, no, no, not that damn bird!\n` -> `N-Não... Não, não, não, não aquele pássaro!\n` (Bandido, 15_06)
- `The nugwisomkami...!` -> `O nugwisomkami...!` (Bandido, 15_06)
- `Stay AWAAAAY!!` -> `Fique LOOOOONGE!!` (Bandido, 15_06)
- `Th-They're making a break for it!\n` -> `E-Eles estão fugindo!\n` (Haku, 15_06)
- `Haku, what do we do!?` -> `Haku, o que fazemos!?` (Kuon, 15_06)
- `Nngh. We have no choice! After them!` -> `Nngh. Sem escolha! Atrás deles!` (Haku, 15_06)
- `Here, of all places--this was supposed to be\n` -> `Aqui, de todos os lugares--era pra ser\n` (Haku, 15_06)
- `an easy job!` -> `serviço fácil!` (Haku, 15_06)
- `They're supposed to be in hiding. Why the hell\n` -> `Eram pra estar escondidos. Por que diabos\n` (Haku, 15_06)
- `are they nonchalantly walking around like this!?` -> `andam por aí tão tranquilos assim!?` (Haku, 15_06)
- `So. Haku's thought process was identical to\n` -> `Então. O raciocínio do Haku era idêntico\n` (Kuon, 15_06)
- `theirs, after all.` -> `ao deles, afinal.` (Kuon, 15_06)
- `Get off my case! We have more important things\n` -> `Me deixa em paz! Temos coisas mais\n` (Haku, 15_06)
- `to be worrying about right now.` -> `importantes pra se preocupar agora.` (Haku, 15_06)
- `If they slip through our fingers now, we might\n` -> `Se eles escaparem agora, pode ser que\n` (Haku, 15_06)
- `never find them again! We can't miss this\n` -> `não os encontremos nunca mais! Não podemos\n` (Haku, 15_06)
- `chance! ` -> `chance!` (Haku, 15_06)
**Voz estabelecida dos falantes (amostra):**
- Haku: `Geez...! Too bright out here...` -> `Aff...! Claridade demais aqui fora...`
- Haku: `Well, guess the sun still rises no matter where\n` -> `Enfim, o sol nasce em qualquer lugar, pelo visto\n`
- Haku: `I am. Still... What am I supposed to do now...?` -> `Pois é. Mesmo assim... O que é que eu faço agora...?`
- Protagonista: `Where... am I?` -> `Onde... estou?`
- Protagonista: `No one else around, or...?` -> `Não tem ninguém... ou...?`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
- Protagonista: `Unh... urgh...` -> `Nnh... argh...`
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
| 0xbf500 | 26 | Ah, good, everyone's here. |
| 0xbf51b | 47 | Ukon plonks himself down in the middle of the\n |
| 0xbf54b | 45 | hall, and everyone gathers to sit around him. |
| 0xbf579 | 44 | What brings you here on such short notice,\n |
| 0xbf5a6 | 13 | dear brother? |
| 0xbf5b4 | 48 | Well, I think I'm gonna have work for you guys\n |
| 0xbf5e5 | 27 | soon. As undercover agents. |
| 0xbf601 | 21 | Undercover... agents. |
| 0xbf617 | 34 | No one is quite sure how to react. |
| 0xbf63a | 43 | Ukon--Oshtor--can't really move in public\n |
| 0xbf666 | 46 | because of his position as Imperial Guard of\n |
| 0xbf695 | 12 | the Right... |
| 0xbf6a2 | 42 | ...So it falls to us to work in his stead. |
| 0xbf6cd | 48 | The only question is, what is he going to make\n |
| 0xbf6fe | 9 | us do...? |
| 0xbf708 | 46 | Hey, relax a little. It's your first job, so\n |
| 0xbf737 | 46 | I've picked out a few nice and easy contracts. |
| 0xbf766 | 43 | Ukon produces a worn, dog-eared notebook,\n |
| 0xbf792 | 36 | leafing through the pages carefully. |
| 0xbf7b7 | 44 | I'll read these off in order, and you guys\n |
| 0xbf7e4 | 42 | tell me what sounds good. Starting with... |
| 0xbf80f | 48 | First up, cleaning up the restroom area in the\n |
| 0xbf840 | 6 | plaza. |
| 0xbf84b | 48 | Second one's transporting the, ah, by-products\n |
| 0xbf87c | 18 | of that process... |
| 0xbf88f | 46 | Third, stirring the contents of the cesspool\n |
| 0xbf8be | 25 | so it doesn't stagnate... |
| 0xbf8d8 | 46 | And then the fourth job is taking THAT stuff\n |
| 0xbf907 | 5 | and-- |
| 0xbf90d | 20 | Wait. Wait a second. |
| 0xbf922 | 11 | What is it? |
| 0xbf92e | 47 | You can talk around it all you like, but, uh.\n |
| 0xbf95e | 46 | There seems to be a... common theme to these\n |
| 0xbf98d | 5 | jobs. |
| 0xbf993 | 33 | Ah, not much I can do about that. |
| 0xbf9b5 | 25 | What... else do you have? |
| 0xbf9cf | 49 | Well, uh. There's one concerning a peruko named\n |
| 0xbfa01 | 40 | Hanako suffering from constipation, wh-- |
| 0xbfa2a | 42 | Like I said, why are they all like that?\n |
| 0xbfa55 | 38 | You've gotta have SOMEthing different. |
| 0xbfa7c | 12 | B-Brother... |
| 0xbfa89 | 47 | It may not seem it, but these are the easiest\n |
| 0xbfab9 | 20 | jobs I have for you. |
| 0xbface | 43 | Ukon. Stop fooling around and give us our\n |
| 0xbfafa | 8 | choices. |
| 0xbfb03 | 23 | I'm not fooling around. |
| 0xbfb1b | 37 | Yeah, you'll have to endure some...\n |
| 0xbfb41 | 48 | unpleasantness. But these are safe, profitable\n |
| 0xbfb72 | 21 | gigs apart from that. |
| 0xbfb88 | 42 | All right, all right, don't give me that\n |
| 0xbfbb3 | 48 | murder-stare. Good grief. How about... this one? |
| 0xbfbe4 | 44 | Ukon flips to another page, then hands the\n |
| 0xbfc11 | 17 | notebook to Kuon. |
| 0xbfc23 | 15 | A kyorori hunt? |
| 0xbfc33 | 47 | Yep. Job entails going out into the mountains\n |
| 0xbfc63 | 45 | and capturing a wild animal called a kyorori. |
| 0xbfc91 | 39 | Huh. That sounds good, don't you think? |
| 0xbfcb9 | 36 | And what exactly is this... kyorori? |
| 0xbfcde | 40 | They're birds that inhabit the frontier. |
| 0xbfd07 | 44 | Big suckers. Five times a person's height,\n |
| 0xbfd34 | 47 | feathers tough as stone, armor-shredding beak\n |
| 0xbfd64 | 13 | and talons... |
| 0xbfd72 | 33 | Ferociously carnivorous, 'course. |
| 0xbfd94 | 32 | Oh, and there's matarii fishing. |
| 0xbfdb5 | 47 | ...And how many times larger than a person is\n |
| 0xbfde5 | 24 | this matarii, pray tell? |
| 0xbfdfe | 45 | Oh, not all that, y'know? Like... about yea\n |
| 0xbfe2c | 4 | big. |
| 0xbfe31 | 49 | Ukon holds up his hands, perhaps shoulder-width\n |
| 0xbfe63 | 6 | apart. |
| 0xbfe6a | 33 | Then is it very ferocious, or...? |
| 0xbfe8c | 23 | Nope. Regular old fish. |
| 0xbfea4 | 42 | It's pretty good grilled. Nice and tender. |
| 0xbfecf | 33 | Um, ah--about matarii, though...? |
| 0xbfef1 | 37 | You know something about them, Kiwru? |
| 0xbff17 | 45 | It's a... fairly famous delicacy, traded at\n |
| 0xbff45 | 40 | high prices. U-Usually you serve it at\n |
| 0xbff6e | 15 | celebrations... |
| 0xbff7e | 44 | Regular fish that fetch a high price, huh?\n |
| 0xbffab | 30 | Sounds like a good deal to me. |
| 0xbffca | 23 | Eh? But aren't those... |
| 0xbffe2 | 48 | Ukon watches in silence as we discuss, a smirk\n |
| 0xc0013 | 12 | on his face. |
| 0xc0020 | 13 | What's wrong? |
| 0xc002e | 43 | Yes, i-if I recall, they only inhabit the\n |
| 0xc005a | 26 | frozen seas north of here. |
| 0xc0075 | 44 | A-And what's more, the waves are routinely\n |
| 0xc00a2 | 47 | rough, and the reefs... Even seasoned sailors\n |
| 0xc00d2 | 26 | often die in those waters. |
| 0xc00ed | 25 | Nope. Rejecting that one. |
| 0xc0107 | 44 | Come on, I went through all the trouble of\n |
| 0xc0134 | 47 | finding deals that work out for you. Don't be\n |
| 0xc0164 | 11 | a buzzkill. |
| 0xc0170 | 44 | "Work out for us?" That one is straight-up\n |
| 0xc019d | 17 | life-threatening. |
| 0xc01af | 45 | Cripes. Picky, picky. Here--there's another\n |
| 0xc01dd | 33 | contract for capturing a furomun. |
| 0xc01ff | 28 | Dear brother, isn't that...? |
| 0xc021c | 45 | They're extremely venomous. In concentrate,\n |
| 0xc024a | 47 | one animal's worth of venom is enough to kill\n |
| 0xc027a | 9 | hundreds. |
| 0xc0284 | 47 | Extreme care is required to handle it, but if\n |
| 0xc02b4 | 46 | prepared properly, its liver can treat heart\n |
| 0xc02e3 | 9 | diseases. |
| 0xc02ed | 45 | Color me impressed, missy. Its venom can be\n |
| 0xc031b | 45 | airborne, too--breathe any of it in, and it\n |
| 0xc0349 | 23 | can knock you out cold. |
| 0xc0361 | 16 | ...I thought so. |
| 0xc0372 | 42 | So you don't have anything, like... safer? |
| 0xc039d | 44 | Hey, listen. Safe, sweet deals that turn a\n |
| 0xc03ca | 32 | good profit are hard to come by. |
| 0xc03eb | 7 | Urgh... |
| 0xc03f3 | 35 | And sanitation is important work.\n |
| 0xc0417 | 34 | It prevents the spread of disease. |
| 0xc043a | 46 | It's a dirty job, but someone's gotta do it.\n |
| 0xc0469 | 31 | You understand, don't you, kid? |
| 0xc0489 | 18 | He's got us there. |
| 0xc049c | 47 | It's a stroke of luck this is even available!\n |
| 0xc04cc | 44 | It may be a shitty job, but I trust you'll\n |
| 0xc04f9 | 16 | toil-it through. |
| 0xc050a | 8 | ...Ukon? |
| 0xc0513 | 46 | All right, all right. Relax. Let's move onto\n |
| 0xc0542 | 25 | our main subject for now. |
| 0xc055c | 43 | Ukon flashes his typical, fearless smile,\n |
| 0xc0588 | 26 | posture relaxing slightly. |
| 0xc05a3 | 13 | Main subject? |
| 0xc05b1 | 44 | Yeah. You remember the bandits we captured\n |
| 0xc05de | 7 | before? |
| 0xc05e6 | 47 | Bandits... You mean the ones that attacked us\n |
| 0xc0616 | 26 | on the way to the capital? |
| 0xc0631 | 26 | Is something up with them? |
| 0xc064c | 48 | You could say that. Seems they escaped custody\n |
| 0xc067d | 29 | after their court sentencing. |
| 0xc069b | 47 | From what I've heard, they still had comrades\n |
| 0xc06cb | 44 | on the outside who hit their escort during\n |
| 0xc06f8 | 8 | transit. |
| 0xc0701 | 21 | So... th-those men... |
| 0xc0717 | 35 | It can only be called carelessness. |
| 0xc073b | 43 | A bit of luck, though. Eyewitness reports\n |
| 0xc0767 | 47 | place them here in the capital, hiding out in\n |
| 0xc0797 | 9 | the city. |
| 0xc07a1 | 45 | And you want us to find and apprehend them.\n |
| 0xc07cf | 11 | Am I right? |
| 0xc07db | 44 | Is that so...? I see. Is this my first test? |
| 0xc0808 | 49 | If that's the case, I'll be sure to exceed your\n |
| 0xc083a | 13 | expectations! |
| 0xc0848 | 44 | Well, hold on. I do want you to find them,\n |
| 0xc0875 | 45 | but when you do, don't try to capture them.\n |
| 0xc08a3 | 13 | Just call me. |
| 0xc08b1 | 4 | Huh? |
| 0xc08b6 | 46 | I don't want you trying to take them on your\n |
| 0xc08e5 | 4 | own. |
| 0xc08ea | 49 | In other words... Your honor takes a hit if you\n |
| 0xc091c | 48 | don't bring them back yourself. Your men, your\n |
| 0xc094d | 8 | problem. |
| 0xc0956 | 49 | Cripes, at least let me get a word in edgewise,\n |
| 0xc0988 | 47 | here. I shouldn't have to tell you this, but... |
| 0xc09b8 | 50 | They probably remember your faces. If you engage\n |
| 0xc09eb | 47 | them directly, chances are, they'll want blood. |
| 0xc0a1b | 40 | Truth is, we don't have much more than\n |
| 0xc0a44 | 48 | eyewitness accounts. No hard clues as to where\n |
| 0xc0a75 | 15 | they're hiding. |
| 0xc0a85 | 44 | And they don't want to be found. Searching\n |
| 0xc0ab2 | 45 | randomly won't do us any good, but we can't\n |
| 0xc0ae0 | 16 | just do nothing. |
| 0xc0af1 | 49 | With all that in mind, I'd like to ask you guys\n |
| 0xc0b23 | 46 | to patrol the capital for me, and to just...\n |
| 0xc0b52 | 11 | stay alert. |
| 0xc0b5e | 49 | If that's all, I don't think we have any reason\n |
| 0xc0b90 | 17 | to turn you down. |
| 0xc0ba2 | 43 | Next to the, uh... dirtier requests, this\n |
| 0xc0bce | 25 | sounds pretty manageable. |
| 0xc0be8 | 46 | And all we have to do if we find anything is\n |
| 0xc0c17 | 25 | contact Ukon. No problem. |
| 0xc0c31 | 20 | All right. We're in. |
| 0xc0c46 | 45 | So, we took the request for the time being,\n |
| 0xc0c74 | 6 | but... |
| 0xc0c7b | 35 | Um... What exactly do we... do now? |
| 0xc0c9f | 7 | Well... |
| 0xc0ca7 | 45 | Searching for these bandits at random isn't\n |
| 0xc0cd5 | 34 | going to be any kind of efficient. |
| 0xc0cf8 | 42 | In this situation, it may be best to put\n |
| 0xc0d23 | 47 | ourselves in their shoes and act based on that. |
| 0xc0d53 | 44 | Thinking of things from their perspective,\n |
| 0xc0d80 | 6 | huh... |
| 0xc0d87 | 48 | To be honest, I can't say I have any clue WHAT\n |
| 0xc0db8 | 17 | they're thinking. |
| 0xc0dca | 46 | Logically, one would seek out a hiding place\n |
| 0xc0df9 | 41 | to lie low and wait out the storm, but... |
| 0xc0e23 | 47 | If it were me, I'd probably go out and find a\n |
| 0xc0e53 | 42 | way to live it up. Celebrate my newfound\n |
| 0xc0e7e | 8 | freedom. |
| 0xc0e87 | 45 | Of course your mind would go there. Please,\n |
| 0xc0eb5 | 46 | try to treat this at least somewhat seriously. |
| 0xc0ee4 | 46 | I'm just saying. Knowing me, that's what I'd\n |
| 0xc0f13 | 3 | do. |
| 0xc0f17 | 47 | What manner of imbecile would risk attracting\n |
| 0xc0f47 | 44 | such attention while the law seeks his head? |
| 0xc0f74 | 4 | Eep! |
| 0xc0f79 | 3 | Man |
| 0xc0f7d | 43 | Whup! Sorry, miss. Wasn't payin' attention. |
| 0xc0fa9 | 40 | N-No, that's all right... I-I'm sorry... |
| 0xc0fd2 | 42 | Don't worry 'bout it. See ya later, cutie. |
| 0xc0ffd | 8 | Henchman |
| 0xc1006 | 42 | Ah! Hey, boss, come check out this bath!\n |
| 0xc1031 | 22 | Thing's freakin' HUGE. |
| 0xc1048 | 45 | Not bad, not bad! Ain't nothin' like a nice\n |
| 0xc1076 | 20 | drink in a hot bath! |
| 0xc108b | 50 | It's been too long since we been on the outside!\n |
| 0xc10be | 39 | We gotta live it large. Large, damn it! |
| 0xc10e6 | 36 | Damn straight! Nothing better'n...\n |
| 0xc110b | 12 | Ah... Uhm... |
| 0xc1118 | 18 | Wh--Y-Y-You guys!? |
| 0xc112b | 7 | A-Ah... |
| 0xc1133 | 10 | YOU guys!? |
| 0xc113e | 43 | You--You're those--From that one time we--? |
| 0xc116a | 41 | N-No... No, no, no, not that damn bird!\n |
| 0xc1194 | 20 | The nugwisomkami...! |
| 0xc11a9 | 14 | Stay AWAAAAY!! |
| 0xc11b8 | 35 | Th-They're making a break for it!\n |
| 0xc11dc | 21 | Haku, what do we do!? |
| 0xc11f2 | 36 | Nngh. We have no choice! After them! |
| 0xc1217 | 46 | Here, of all places--this was supposed to be\n |
| 0xc1246 | 12 | an easy job! |
| 0xc1253 | 48 | They're supposed to be in hiding. Why the hell\n |
| 0xc1284 | 48 | are they nonchalantly walking around like this!? |
| 0xc12b5 | 45 | So. Haku's thought process was identical to\n |
| 0xc12e3 | 18 | theirs, after all. |
| 0xc12f6 | 48 | Get off my case! We have more important things\n |
| 0xc1327 | 31 | to be worrying about right now. |
| 0xc1347 | 48 | If they slip through our fingers now, we might\n |
| 0xc1378 | 43 | never find them again! We can't miss this\n |
| 0xc13a4 | 8 | chance!  |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_06.json` com a forma:
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
