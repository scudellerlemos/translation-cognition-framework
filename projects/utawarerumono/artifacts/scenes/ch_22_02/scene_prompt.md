# Cena ch_22_02 — pacote de traducao (332 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `here?` -> `afinal?` (Haku, 13_02)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `Huh? What do you mean?` -> `Hein? Como assim?` (Kuon, 11_09)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Haku...` -> `Haku...` (Kuon, 11_02)
- `yourself?` -> `você mesmo?` (Haku, 18_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `All` -> `Todos` (SYSTEM, 19_08)
- `Cheers!!` -> `Saúde!!` (Haku/Ukon, 17_01)
- `the air.` -> `ecoa no ar.` (Haku, 14_09)
- `drink.` -> `bebida.` (Homem, 16_01)
- `before...` -> `assim...` (Nekone, 14_10)
- `table.` -> `na mesa.` (Haku, 13_02)
- `man.` -> `cara.` (Haku, 14_04)
- `are.` -> `são.` (Haku, 19_08)
- `Master Haku.` -> `Mestre Haku.` (Maroro, 17_01)
- `it.` -> `aí.` (Haku, 15_03)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `from you.` -> `de você.` (Rulutieh, 15_01)
- `Master Haku...` -> `Mestre Haku...` (Maroro, 12_13)
- `around?` -> `mesmo?` (Haku, 19_02)
- `of you.` -> `de você.` (Ukon, 13_01)
- `of course.` -> `claro.` (Haku, 18_01)
- `excitement.` -> `frenéticos.` (Haku, 14_03)
- `...Uh.` -> `...Ahn.` (Haku, 14_04)
- `...You disgust me.` -> `...Você me repugna.` (Maroro, 19_05)
- `frozen.` -> `congelado.` (SYSTEM or context, 21_04)
- `...How did it end up like this?` -> `...Como é que chegou nessa situação?` (Haku, 19_06)
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
| 0x22cad3 | 49 | Nothing much comes in for a few days. All we do\n |
| 0x22cb05 | 44 | is clean in the morning and patrol at night. |
| 0x22cb32 | 46 | Today is no different. Breakfast first, then\n |
| 0x22cb61 | 21 | clean up main street. |
| 0x22cb77 | 44 | Hee hee! And what'll we have for breakfast\n |
| 0x22cba4 | 6 | today? |
| 0x22cbab | 49 | I've made lots, so please don't hesitate to ask\n |
| 0x22cbdd | 11 | for more... |
| 0x22cbe9 | 46 | We all enjoy the mountain of food piled atop\n |
| 0x22cc18 | 11 | the plates. |
| 0x22cc24 | 25 | How... How does it taste? |
| 0x22cc3e | 47 | It's delicious as always... but as a personal\n |
| 0x22cc6e | 44 | request, I would like a stronger flavor to\n |
| 0x22cc9b | 10 | the dango. |
| 0x22cca6 | 45 | Oh, all right... I'll keep that in mind for\n |
| 0x22ccd4 | 26 | the next time I make them. |
| 0x22ccef | 39 | I thought they were just right, though. |
| 0x22cd17 | 47 | I would prefer a more mature, salty flavoring\n |
| 0x22cd47 | 9 | to these. |
| 0x22cd51 | 25 | Mature... salty flavor... |
| 0x22cd6b | 45 | She is not requesting a complicated flavor.\n |
| 0x22cd99 | 48 | Those who do more physical work prefer saltier\n |
| 0x22cdca | 6 | meals. |
| 0x22cdd1 | 47 | Sounds a bit like the tastes of a drinker, too. |
| 0x22ce01 | 46 | Haku, do you mind passing the soy sauce over\n |
| 0x22ce30 | 5 | here? |
| 0x22ce36 | 8 | ...Sure. |
| 0x22ce3f | 43 | Just enough to enhance the flavor, and...\n |
| 0x22ce6b | 45 | *munch, munch*... Yes, this fresh saltiness\n |
| 0x22ce99 | 9 | is exac-- |
| 0x22cea3 | 13 | Pffffffffft!! |
| 0x22ceb1 | 47 | That is not soy sauce. It is obviously vinegar. |
| 0x22cee1 | 42 | Urgh... this sourness... It's an assault\n |
| 0x22cf0c | 14 | on my mouth... |
| 0x22cf1b | 30 | Oh... my bad. It was this one. |
| 0x22cf3a | 45 | I can finish your vinegary ones, if you like? |
| 0x22cf68 | 49 | No. It is the responsibility of the seasoner to\n |
| 0x22cf9a | 46 | eat what they've seasoned. *Munch, munch*...\n |
| 0x22cfc9 | 18 | Hlgh... So sour... |
| 0x22cfdc | 44 | That's awfully big of you, but it might be\n |
| 0x22d009 | 14 | rough going... |
| 0x22d01c | 45 | I'll take charge of this area, Haku. You go\n |
| 0x22d04a | 39 | clean up the area around market street. |
| 0x22d072 | 25 | ...Market street. Got it. |
| 0x22d08c | 9 | *Sigh*... |
| 0x22d098 | 12 | ...*Sigh*... |
| 0x22d0a5 | 30 | Haku, is something the matter? |
| 0x22d0c4 | 22 | Huh? What do you mean? |
| 0x22d0db | 41 | Well, you've just been sighing so much... |
| 0x22d105 | 46 | Sorry. I guess I've just got a lot on my mind. |
| 0x22d134 | 20 | Haku... I suppose... |
| 0x22d149 | 36 | Haku, why don't you go take a break? |
| 0x22d16e | 28 | No, I'm fine. I'd better go. |
| 0x22d18b | 5 | Ah... |
| 0x22d191 | 7 | Haku... |
| 0x22d199 | 47 | After we finish cleaning and head back toward\n |
| 0x22d1c9 | 46 | the Hakurokaku, I feel a sudden hand clap on\n |
| 0x22d1f8 | 12 | my shoulder. |
| 0x22d205 | 44 | How's it going, kid? Fancy meeting you here. |
| 0x22d232 | 13 | ...Hey, Ukon. |
| 0x22d240 | 29 | What's up? Why the long face? |
| 0x22d25e | 30 | Do I... really look like that? |
| 0x22d27d | 44 | What? You mean you haven't even noticed it\n |
| 0x22d2aa | 9 | yourself? |
| 0x22d2b4 | 45 | I thought I was just acting like I always do. |
| 0x22d2e2 | 44 | Ho boy. This looks a lot more serious than\n |
| 0x22d30f | 12 | I thought... |
| 0x22d31c | 46 | All right, kid. You're comin' with me tonight. |
| 0x22d34b | 4 | Huh? |
| 0x22d350 | 45 | We haven't had a drink together in a while!\n |
| 0x22d37e | 39 | Let's invite Sakon and Maroro over too. |
| 0x22d3a6 | 45 | Tonight's on me, boys! All of you can drink\n |
| 0x22d3d4 | 28 | as much as you like! Cheers! |
| 0x22d3f1 | 3 | All |
| 0x22d3f5 | 8 | Cheers!! |
| 0x22d3fe | 46 | The sound of our clinking cups rings through\n |
| 0x22d42d | 8 | the air. |
| 0x22d436 | 47 | I arrive at our headquarters at the appointed\n |
| 0x22d466 | 46 | time to find the table covered with food and\n |
| 0x22d495 | 6 | drink. |
| 0x22d49c | 47 | I thought it was going to be more of a quiet,\n |
| 0x22d4cc | 18 | subdued evening... |
| 0x22d4df | 48 | But with Ougi, Kiwru, and Jachdwalt here, this\n |
| 0x22d510 | 46 | whole thing seems to have turned into a party. |
| 0x22d53f | 44 | So you're the Jachdwalt I've heard so much\n |
| 0x22d56c | 45 | about... They say you're a handy fella with\n |
| 0x22d59a | 8 | a sword. |
| 0x22d5a3 | 45 | You don't seem half bad yourself. We oughta\n |
| 0x22d5d1 | 46 | square off sometime if we ever get the chance. |
| 0x22d600 | 48 | Now that I think about it, I don't think we've\n |
| 0x22d631 | 45 | ever had a get-together with all of us guys\n |
| 0x22d65f | 9 | before... |
| 0x22d669 | 50 | When I look around at all of us, I realize we're\n |
| 0x22d69c | 18 | a... unique bunch. |
| 0x22d6af | 48 | Actually, I'm kinda curious as to why Mikazu--\n |
| 0x22d6e0 | 25 | why Sakon's here tonight. |
| 0x22d6fa | 28 | Kiwru, please. Have a drink. |
| 0x22d717 | 47 | Oh, it's all right, really, you don't have to\n |
| 0x22d747 | 17 | worry about me... |
| 0x22d759 | 38 | Tush! What need have we for modesty,\n |
| 0x22d780 | 13 | Master Kiwru? |
| 0x22d78e | 33 | Ah! N-No, this is far too much... |
| 0x22d7b0 | 48 | Each of them sits with a cup in hand, animated\n |
| 0x22d7e1 | 17 | in idle chitchat. |
| 0x22d7f3 | 47 | To be honest, I wasn't really feeling it when\n |
| 0x22d823 | 48 | Ukon invited me, but I'm starting to enjoy this. |
| 0x22d854 | 48 | I sip my drink little by little, and nibble at\n |
| 0x22d885 | 22 | the food on the table. |
| 0x22d89c | 41 | ...Hm? This tastes like it was made by... |
| 0x22d8c6 | 38 | So how is it, kid? Feelin' any better? |
| 0x22d8ed | 45 | Ukon grins at me from the other side of the\n |
| 0x22d91b | 6 | table. |
| 0x22d922 | 20 | Yeah, thanks to you. |
| 0x22d937 | 45 | ...Guess I should thank Kuon and the others\n |
| 0x22d965 | 11 | later, too. |
| 0x22d971 | 33 | Eh? What's that supposed to mean? |
| 0x22d993 | 42 | You're gonna be like that? Well, whatever. |
| 0x22d9be | 31 | Rulutieh made this, didn't she? |
| 0x22d9de | 34 | Heh... Nothin' gets past this kid. |
| 0x22da01 | 48 | It wasn't just the bosslady. Everyone else was\n |
| 0x22da32 | 29 | pretty worried about you too. |
| 0x22da50 | 48 | It would appear you are something of a ladies'\n |
| 0x22da81 | 4 | man. |
| 0x22da86 | 49 | Anyhow, we all thought it might be nice to just\n |
| 0x22dab8 | 46 | have a guy's night like this. So here we all\n |
| 0x22dae7 | 4 | are. |
| 0x22daec | 22 | That about sums it up. |
| 0x22db03 | 47 | Man, the Sakon disguise always makes him seem\n |
| 0x22db33 | 31 | like such a good-natured guy... |
| 0x22db53 | 11 | Eheheheh... |
| 0x22db5f | 35 | Yeah... I get it now. Thanks, guys. |
| 0x22db83 | 45 | Fwaaah? Was THAT the occasion's intendment?\n |
| 0x22dbb1 | 26 | I knew naught of all this. |
| 0x22dbcc | 48 | It is remarkable to me, Maroro, how you always\n |
| 0x22dbfd | 43 | manage to remain so obliviously happy and\n |
| 0x22dc29 | 9 | carefree. |
| 0x22dc33 | 32 | Oho? Ah, thy praise is too kind! |
| 0x22dc54 | 35 | You know that wasn't praise, right? |
| 0x22dc78 | 51 | Ah, but methinks thy sentiment is well justified,\n |
| 0x22dcac | 12 | Master Haku. |
| 0x22dcb9 | 50 | After such harrowing circumstance, little wonder\n |
| 0x22dcec | 44 | that thou shouldst be overtaken with glooms. |
| 0x22dd19 | 41 | Zounds... Even the mere thought sendeth\n |
| 0x22dd43 | 30 | dreadful chill along my spine. |
| 0x22dd62 | 48 | For grisly Tatari to assume the countenance of\n |
| 0x22dd93 | 47 | man... Even I so young-eyed could not discern\n |
| 0x22ddc3 | 3 | it. |
| 0x22ddcc | 41 | M-Maroro, we shouldn't be talking about-- |
| 0x22ddf6 | 43 | Oh! I... I blather skimble-skamble stuff!\n |
| 0x22de22 | 44 | Heed not that prattle! Heardst thou aught?\n |
| 0x22de4f | 18 | N-Not I! *Whistle* |
| 0x22de62 | 47 | ...Master Kiwru... I am not to disappear now,\n |
| 0x22de92 | 39 | am I? I beg thee, tell me I shall not\n |
| 0x22deba | 10 | disappear! |
| 0x22dec5 | 37 | Wh-What am I supposed to do about it? |
| 0x22deeb | 47 | Even in this safe place, I can still remember\n |
| 0x22df1b | 34 | everything that happened that day. |
| 0x22df3e | 47 | A Tatari disguised as a human, huh... I guess\n |
| 0x22df6e | 41 | that's what we decided it was in the end. |
| 0x22df98 | 48 | It's not the truth... but it's what we decided\n |
| 0x22dfc9 | 7 | we saw. |
| 0x22dfd1 | 15 | But that was... |
| 0x22dfe1 | 31 | *Sigh* This is going nowhere... |
| 0x22e001 | 50 | Ukon looks straight into my eyes, his expression\n |
| 0x22e034 | 14 | turning grave. |
| 0x22e043 | 45 | Kid, I think you'd better tell me everything. |
| 0x22e071 | 36 | ...What exactly happened over there? |
| 0x22e096 | 50 | Whoa there. No need to get in his face about it,\n |
| 0x22e0c9 | 4 | huh? |
| 0x22e0ce | 48 | ...Kuon and I gave a full report on why we had\n |
| 0x22e0ff | 44 | to seal the ruins. Everything should be in\n |
| 0x22e12c | 6 | there. |
| 0x22e133 | 45 | Kid, you know damn well that's not what I'm\n |
| 0x22e161 | 24 | talking about right now. |
| 0x22e17a | 49 | I want you to tell me everything you're keeping\n |
| 0x22e1ac | 45 | bottled up inside. I wanna hear it straight\n |
| 0x22e1da | 9 | from you. |
| 0x22e1e4 | 12 | ...That's... |
| 0x22e1f1 | 11 | I hesitate. |
| 0x22e1fd | 14 | Master Haku... |
| 0x22e20c | 49 | Why don't you try talking it over with everyone\n |
| 0x22e23e | 47 | here? Sometimes just letting it out is enough\n |
| 0x22e26e | 8 | to help. |
| 0x22e277 | 48 | True. Maybe telling someone about it will help\n |
| 0x22e2a8 | 15 | me feel better. |
| 0x22e2b8 | 45 | But... I don't know if I can find the words\n |
| 0x22e2e6 | 14 | to explain it. |
| 0x22e2f5 | 49 | The thing we saw in the ruins, those fragmented\n |
| 0x22e327 | 25 | memories I kept seeing... |
| 0x22e341 | 48 | Everything's jumbled up in my brain, like tiny\n |
| 0x22e372 | 40 | pieces of a puzzle I can't put together. |
| 0x22e39b | 43 | No, that's not right... I know the answer\n |
| 0x22e3c7 | 17 | I have to give... |
| 0x22e3d9 | 42 | ...Sorry... but I need a little more time. |
| 0x22e404 | 46 | But... I promise... one day, I'll be able to\n |
| 0x22e433 | 24 | tell you all everything. |
| 0x22e44c | 41 | Mm. Still havin' trouble sortin' it out\n |
| 0x22e476 | 42 | yourself... Awright, we can wait. I know\n |
| 0x22e4a1 | 22 | you'll get through it. |
| 0x22e4b8 | 41 | Guess that's that then. Well then, kid,\n |
| 0x22e4e2 | 29 | let's drink 'til we collapse! |
| 0x22e500 | 7 | Ukon... |
| 0x22e508 | 47 | Makes me grumpy, seeing you all glum like that. |
| 0x22e538 | 49 | Doesn't help to just obsess over your problems.\n |
| 0x22e56a | 48 | After all, if you could fix 'em that easy, you\n |
| 0x22e59b | 26 | already would have, right? |
| 0x22e5b6 | 48 | So if that's how it is, for now... We can just\n |
| 0x22e5e7 | 46 | drink until we can laugh all our problems off. |
| 0x22e616 | 28 | ...Yeah. Maybe you're right. |
| 0x22e633 | 45 | That's the spirit. Here, you can have this!\n |
| 0x22e661 | 36 | I'm sure it'll make you feel better. |
| 0x22e686 | 44 | Sakon fishes the gigiri candy out from his\n |
| 0x22e6b3 | 27 | pocket and offers it to me. |
| 0x22e6cf | 42 | I thought I told you I don't want that--\n |
| 0x22e6fa | 47 | Wait a minute, do you always carry that thing\n |
| 0x22e72a | 7 | around? |
| 0x22e732 | 30 | Course I do. Why wouldn't I?\n |
| 0x22e751 | 29 | I knew you'd be here tonight. |
| 0x22e76f | 22 | Ukon, Sakon... Thanks. |
| 0x22e786 | 44 | Awright, everyone! Let's get those clothes\n |
| 0x22e7b3 | 5 | off!! |
| 0x22e7b9 | 10 | Heigh-ho!! |
| 0x22e7c4 | 47 | Not a bad idea, yeah? If we're supposed to be\n |
| 0x22e7f4 | 41 | sharing tonight, might as well not hide\n |
| 0x22e81e | 9 | anything! |
| 0x22e828 | 46 | I see! Well, in that case, don't mind if I do! |
| 0x22e857 | 47 | So you intend for us to thus bare all to each\n |
| 0x22e887 | 45 | other... so to speak? Aha... An interesting\n |
| 0x22e8b5 | 12 | proposition. |
| 0x22e8c2 | 22 | Huh? Wha--Wait, WHAT!? |
| 0x22e8d9 | 11 | Everyone... |
| 0x22e8e5 | 41 | All right! Let's get this party started!! |
| 0x22e90f | 26 | What do you think, Nekone? |
| 0x22e92a | 40 | He seems like he is doing much better.\n |
| 0x22e953 | 39 | I can hear him laughing and having fun. |
| 0x22e97b | 33 | Hee hee... That's good to hear.\n |
| 0x22e99d | 29 | Haku's been so gloomy lately. |
| 0x22e9bb | 38 | He can be quite a handful sometimes... |
| 0x22e9e2 | 49 | Kuon and Nekone sigh in relief as they hear the\n |
| 0x22ea14 | 23 | men having a good time. |
| 0x22ea2c | 46 | Nosuri and Atuy restrain the twins, who seem\n |
| 0x22ea5b | 46 | determined to join Haku, while Kurarin keeps\n |
| 0x22ea8a | 11 | them bound. |
| 0x22ea96 | 10 | Mmf. Mmmf. |
| 0x22eaa1 | 13 | Mmmf! Mmmmmf! |
| 0x22eaaf | 45 | You have my respect for boldly chasing your\n |
| 0x22eadd | 18 | desires! However-- |
| 0x22eaf0 | 45 | Make sure you don't let them go now, Kurarin. |
| 0x22eb1e | 22 | *Jiggle jiggle jiggle* |
| 0x22eb35 | 6 | Mmf... |
| 0x22eb3c | 9 | Mmmmmf... |
| 0x22eb46 | 49 | Ahaha... I understand you two are worried about\n |
| 0x22eb78 | 47 | Haku too, but I feel your methods may be less\n |
| 0x22eba8 | 10 | helpful... |
| 0x22ebb3 | 20 | Oh, hello, everyone. |
| 0x22ebc8 | 34 | Oh, Rulutieh. Where have you been? |
| 0x22ebeb | 29 | Oh wow... That smells lovely. |
| 0x22ec09 | 43 | Um... I thought they might be running low\n |
| 0x22ec35 | 21 | on food by now, so... |
| 0x22ec4b | 47 | Rulutieh carries a large tray, bearing a wide\n |
| 0x22ec7b | 34 | array of smaller dishes and bowls. |
| 0x22ec9e | 50 | Good thinking, Rulutieh. That's very considerate\n |
| 0x22ecd1 | 7 | of you. |
| 0x22ecd9 | 38 | Mmm! I see you've chosen the perfect\n |
| 0x22ed00 | 27 | accompaniments for a drink. |
| 0x22ed1c | 26 | Um... Thank you very much. |
| 0x22ed37 | 47 | Well, Rulutieh, shall we go take these to them? |
| 0x22ed67 | 10 | Of course. |
| 0x22ed72 | 32 | Haku? Everyone? We're coming in. |
| 0x22ed93 | 43 | Haaa, chunga chonga chunga chonga chunga... |
| 0x22edbf | 45 | Everyone in the room besides Kiwru is stark\n |
| 0x22eded | 42 | naked, and dancing around in a flurry of\n |
| 0x22ee18 | 11 | excitement. |
| 0x22ee24 | 45 | Oooh, Master Haku! Thy dance is a wonder to\n |
| 0x22ee52 | 8 | behold!! |
| 0x22ee5b | 44 | Not good enough, kid! You gotta move those\n |
| 0x22ee88 | 41 | trays faster! Hide the goods! Like this!! |
| 0x22eeb2 | 48 | Come on, left to right! A stance that embodies\n |
| 0x22eee3 | 50 | attack and defense! You've got a long way to go!\n |
| 0x22ef16 | 34 | FEEL the dance!! Feel the purpose! |
| 0x22ef39 | 36 | I get it! How's this!? Like this!?\n |
| 0x22ef5e | 32 | This!? Hoo, hah, hoo, hoo, HAH!! |
| 0x22ef7f | 46 | Gaaahahahahaw! I can see it! You're floppin'\n |
| 0x22efae | 36 | around right out in the open, boss!! |
| 0x22efd3 | 44 | Come now, Kiwru. We simply cannot have you\n |
| 0x22f000 | 28 | remain the only man clothed! |
| 0x22f01d | 46 | With that, Ougi deftly slips off Kiwru's sash. |
| 0x22f04c | 49 | I can't!! P-Please, Ougi! Stop! G-Give it back!\n |
| 0x22f07e | 20 | Please! Stooooooop!! |
| 0x22f093 | 33 | Oh... Oh dear... Oh no, no, no... |
| 0x22f0b5 | 6 | ...Uh. |
| 0x22f0bc | 48 | ...Hello, Haku. It would appear you are having\n |
| 0x22f0ed | 22 | the time of your life. |
| 0x22f104 | 19 | K...Kuon? Everyone? |
| 0x22f118 | 11 | N-Nekone... |
| 0x22f124 | 46 | Th-Th-This isn't what it looks like, Nekone!\n |
| 0x22f153 | 28 | This is just--Um, I... uh... |
| 0x22f170 | 46 | Well, well. Looks like they picked the worst\n |
| 0x22f19f | 26 | time to wander in! Hahaha! |
| 0x22f1ba | 46 | What are you saying!? Behold this incredible\n |
| 0x22f1e9 | 44 | body! I am never ashamed to put it on full\n |
| 0x22f216 | 8 | display! |
| 0x22f21f | 18 | ...You disgust me. |
| 0x22f232 | 5 | Ghk!? |
| 0x22f238 | 45 | Nekone abruptly exits, leaving the men with\n |
| 0x22f266 | 17 | that icy comment. |
| 0x22f278 | 13 | ...Hoooo boy. |
| 0x22f286 | 10 | Nekoneee!! |
| 0x22f291 | 45 | Sakon stands locked in his pose, completely\n |
| 0x22f2bf | 7 | frozen. |
| 0x22f2c7 | 32 | Dear sister, I must apologize.\n |
| 0x22f2e8 | 45 | Inebriation notwithstanding, I have clearly\n |
| 0x22f316 | 20 | lapsed in decorum... |
| 0x22f32b | 51 | I had no idea my brother had such... interests...\n |
| 0x22f35f | 48 | As your sister, I support your endeavors, but... |
| 0x22f390 | 48 | Dear sister, I do believe you may have gravely\n |
| 0x22f3c1 | 17 | misunderstood...! |
| 0x22f3d3 | 9 | Gadzooks. |
| 0x22f3dd | 38 | Everyone's like Dad. So many wigglies. |
| 0x22f404 | 43 | Shinonon... why don't we go somewhere else? |
| 0x22f430 | 22 | Kiwru's is the cutest. |
| 0x22f447 | 13 | C-Cutest...!? |
| 0x22f455 | 25 | Kiwru falls to his knees. |
| 0x22f46f | 11 | Gadzooooks. |
| 0x22f47b | 49 | She's hiding her face with her hands, but she's\n |
| 0x22f4ad | 36 | clearly peeking through her fingers. |
| 0x22f4d2 | 33 | Mhm... Well, you seem fine now.\n |
| 0x22f4f4 | 28 | Come on, Rulutieh, let's go. |
| 0x22f511 | 16 | ...Gadzooooooks. |
| 0x22f522 | 38 | ...It's a few days after the incident. |
| 0x22f549 | 37 | The girls still refuse to talk to us. |
| 0x22f56f | 31 | ...How did it end up like this? |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_02.json` com a forma:
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
