# Cena ch_11_07 — pacote de traducao (106 linhas)

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
| Haku | Personagem | Haku | manter_original | moderate |
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
- `Kuon leads me to a squat stone building near the\n` -> `A Kuon me leva até um prédio baixo de pedra perto da\n` (Haku, 11_07)
- `edge of town...` -> `saída da vila...` (Haku, 11_07)
- `It seems to be a storehouse--multiple bags are\n` -> `Parece ser um depósito--vários sacos estão\n` (Haku, 11_07)
- `stacked high inside.` -> `empilhados bem alto lá dentro.` (Haku, 11_07)
- `A few lie open, seemingly full of tiny, seed-like\n` -> `Alguns estão abertos, aparentemente cheios de pequenos\n` (Haku, 11_07)
- `grains...` -> `grãos parecidos com sementes...` (Haku, 11_07)
- `The innkeeper wants eight of these bags carried\n` -> `A estalajadeira quer oito desses sacos levados\n` (Haku, 11_07)
- `over to the mill.` -> `até o moinho.` (Haku, 11_07)
- `I see. These, huh?` -> `Saquei. Esses aqui, né?` (Haku, 11_07)
- `That's right.` -> `Isso mesmo.` (Kuon, 11_07)
- `She says that like it's nothing, but each sack looks\n` -> `Ela fala como se não fosse nada, mas cada saco parece\n` (Haku, 11_07)
- `like it weighs a ton...` -> `pesar uma tonelada...` (Haku, 11_07)
- `I'm surprised she wants to work after walking all\n` -> `Me surpreende ela querer trabalhar depois de andar o dia\n` (Haku, 11_07)
- `day. I wouldn't be able to even if I tried.` -> `todo. Eu não conseguiria nem se tentasse.` (Haku, 11_07)
- `Yep. Eight of these. Over to the mill.` -> `Isso. Oito desses. Até o moinho.` (Kuon, 11_07)
- `Urgh, she wants me to help her? I'm exhausted. I can\n` -> `Argh, ela quer que eu ajude? Tô exausto. Mal\n` (Haku, 11_07)
- `barely move, for crying out loud.` -> `consigo me mexer, pelo amor de Deus.` (Haku, 11_07)
- `But I AM indebted to her, and it'd be bad form to\n` -> `Mas eu DEVO a ela, e seria falta de educação\n` (Haku, 11_07)
- `just stand and watch... She's taking care of me,\n` -> `só ficar parado olhando... Ela está cuidando de mim,\n` (Haku, 11_07)
- `after all.` -> `afinal.` (Haku, 11_07)
- `All right, let me help you out a bit, then.` -> `Tá bom, deixa eu te ajudar um pouco, então.` (Haku, 11_07)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Kuon has an astonished look on her face. Was she not\n` -> `A Kuon fica com uma cara de espanto. Será que ela não\n` (Haku, 11_07)
- `expecting me to offer to help?` -> `esperava que eu me oferecesse pra ajudar?` (Haku, 11_07)
- `I said, let me help you out a bit.` -> `Eu disse: deixa eu te ajudar um pouco.` (Haku, 11_07)
- `Kuon just stares in amazement for a moment, then\n` -> `A Kuon fica me encarando pasma por um instante, então\n` (Haku, 11_07)
- `smiles and nods.` -> `sorri e acena.` (Haku, 11_07)
- `Mm, thanks. I appreciate it. Could you take eight\n` -> `Hum, obrigada. Agradeço. Você pode levar oito\n` (Kuon, 11_07)
- `of these bags over to the mill, then?` -> `desses sacos até o moinho, então?` (Kuon, 11_07)
- `Sure. Just eight?` -> `Claro. Só oito?` (Haku, 11_07)
- `If you'd please.` -> `Se não se importar.` (Kuon, 11_07)
- `Eight... That's... actually quite a few.` -> `Oito... Isso é... bastante coisa, na real.` (Haku, 11_07)
- `...Wait a sec. Eight?` -> `...Pera um pouco. Oito?` (Haku, 11_07)
- `Wait... You mean all of them!?` -> `Espera... Você quer dizer todos eles!?` (Haku, 11_07)
- `Best of luck.` -> `Boa sorte.` (Kuon, 11_07)
- `Wait, wait, hold up. Don't give me a "best of luck"\n` -> `Espera, espera, calma. Não me vem com "boa sorte"\n` (Haku, 11_07)
- `and bail. You're making me do all the work?` -> `e cai fora. Você vai me fazer fazer tudo?` (Haku, 11_07)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Don't "huh?" me! I said I'd help, not do all the\n` -> `Não me venha com "hein?"! Eu disse que ajudaria, não que faria todo o\n` (Haku, 11_07)
- `work for you!` -> `trabalho pra você!` (Haku, 11_07)
- `Um... Haku, I accepted this job for your sake.\n` -> `Ahn... Haku, eu aceitei esse trabalho por você.\n` (Kuon, 11_07)
- `I'm not too keen on taking that away from you.` -> `Não quero muito tirar isso de você.` (Kuon, 11_07)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `"For my sake?" What does she mean by THAT?` -> `"Por mim?" O que ela quer dizer com ISSO?` (Haku, 11_07)
- `I thought that being taken care of all the time\n` -> `Achei que ser cuidado o tempo todo\n` (Kuon, 11_07)
- `might be weighing on you, so I wanted to help.` -> `talvez estivesse te pesando, então quis ajudar.` (Kuon, 11_07)
- `If you had some work to do and earn your keep with,\n` -> `Se você tivesse algum trabalho pra fazer e se sustentar,\n` (Kuon, 11_07)
- `you wouldn't have to feel that way. Right?` -> `não precisaria se sentir assim. Né?` (Kuon, 11_07)
- `Wh--` -> `Q--` (Haku, 11_07)
- `That was... completely unnecessary.` -> `Isso foi... completamente desnecessário.` (Haku, 11_07)
- `It's not like I feel emasculated or guilty or\n` -> `Não é como se eu me sentisse menos homem ou culpado nem\n` (Haku, 11_07)
- `anything like that.` -> `nada do tipo.` (Haku, 11_07)
- `Either way, there's no way I'm going to be able to\n` -> `De todo jeito, não tem como eu conseguir\n` (Haku, 11_07)
- `do this on my own. I'm gonna need her help.` -> `fazer isso sozinho. Vou precisar da ajuda dela.` (Haku, 11_07)
- `The only jobs the innkeeper had left were children's\n` -> `Os únicos trabalhos que sobraram com a estalajadeira eram tarefas\n` (Haku, 11_07)
- `chores, but it's better than nothing...` -> `de criança, mas é melhor que nada...` (Haku, 11_07)
- `Children's... chores?` -> `Tarefas... de criança?` (Haku, 11_07)
- `I look over at the huge, heavy bags, each sack an\n` -> `Olho pros sacos enormes e pesados, cada um um\n` (Haku, 11_07)
- `armful, filled to the brim.` -> `braçado, cheio até a boca.` (Haku, 11_07)
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `KIDS carry these?` -> `CRIANÇAS carregam isso?` (Haku, 11_07)
- `Huh? Yeah, when they want to work for a little\n` -> `Hein? Sim, quando querem trabalhar por um\n` (Kuon, 11_07)
- `pocket money, sure.` -> `trocado, claro.` (Kuon, 11_07)
- `I... I don't mean anything by it. I just wanted you\n` -> `Eu... Não quis dizer nada com isso. Só queria que você\n` (Kuon, 11_07)
- `to know why it's the only job left.` -> `soubesse por que é o único trabalho que sobrou.` (Kuon, 11_07)
- `Kuon adds that last part pretty quickly. I get the\n` -> `A Kuon acrescenta essa última parte bem rápido. Tenho a\n` (Haku, 11_07)
- `feeling she thinks she's hurt my masculinity.` -> `impressão de que ela acha que feriu minha masculinidade.` (Haku, 11_07)
- `Come on, though. If this is just a kids' chore, the\n` -> `Mas qual é. Se isso é só tarefa de criança, os\n` (Haku, 11_07)
- `bags must be way lighter than they look.` -> `sacos devem ser bem mais leves do que parecem.` (Haku, 11_07)
- `It can't be that bad. I guess I'd better just get\n` -> `Não pode ser tão ruim. Acho melhor só\n` (Haku, 11_07)
- `it over with.` -> `acabar logo com isso.` (Haku, 11_07)
- `Urgh... HURGH--!!` -> `Argh... NGHHH--!!` (Haku, 11_07)
- `*WHUMP*` -> `*BAM*` (Haku, 11_07)
- `I stand corrected. They are not light.` -> `Me corrijo. Não são leves.` (Haku, 11_07)
- `The mill isn't far from here, but it's not close,\n` -> `O moinho não é longe daqui, mas também não é perto,\n` (Haku, 11_07)
- `either. And I have to make the trip eight times?` -> `não. E eu tenho que fazer o trajeto oito vezes?` (Haku, 11_07)
- `With bags this heavy, that doesn't seem like work a\n` -> `Com sacos tão pesados, isso não parece trabalho que\n` (Haku, 11_07)
- `child could help with, let alone do on their own.` -> `uma criança ajudaria a fazer, quanto mais sozinha.` (Haku, 11_07)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Kuon, how exactly is this a chore for children?\n` -> `Kuon, como exatamente isso é tarefa pra criança?\n` (Haku, 11_07)
- `Are you pulling my leg?` -> `Você tá me zoando?` (Haku, 11_07)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `Kuon gives an ambiguous reply and averts her eyes.` -> `A Kuon dá uma resposta ambígua e desvia o olhar.` (Haku, 11_07)
- `Why, y--I knew it.` -> `Ora, vo--Eu sabia.` (Haku, 11_07)
- `...He's probably still recovering, yeah... doesn't\n` -> `...Ele ainda deve estar se recuperando, é... não\n` (Kuon, 11_07)
- `have his full strength back. That must be it.` -> `recuperou a força toda. Deve ser isso.` (Kuon, 11_07)
- `Hey, don't avoid the question.` -> `Ei, não foge da pergunta.` (Haku, 11_07)
- `We can't have you overexerting yourself, so sit\n` -> `A gente não pode deixar você se esforçar demais, então senta\n` (Kuon, 11_07)
- `there while I carry them, OK?` -> `ali enquanto eu carrego, tá?` (Kuon, 11_07)
- `Hey, I'm talking to y--` -> `Ei, eu tô falando com vo--` (Haku, 11_07)
- `And she's already gone. Geez. I won't say no to a\n` -> `E ela já foi. Aff. Não vou recusar uma\n` (Haku, 11_07)
- `sit-down, but I can't say I'm not annoyed.` -> `sentada, mas não posso dizer que não tô irritado.` (Haku, 11_07)
- `I manage to rouse myself and chase after her.` -> `Consigo me levantar e vou atrás dela.` (Haku, 11_07)
- `The sight of Kuon stacking multiple enormous bags\n` -> `A cena da Kuon empilhando vários sacos enormes\n` (Haku, 11_07)
- `onto her shoulders greets me inside the storehouse.` -> `nos ombros me recebe dentro do depósito.` (Haku, 11_07)
- `Hup.` -> `Upa.` (Kuon, 11_07)
- `*WHUMP, WHUMP, WHUMP*` -> `*BAM, BAM, BAM*` (Haku, 11_07)
- `She tosses sack after sack onto a pile on her\n` -> `Ela joga saco após saco numa pilha nos\n` (Haku, 11_07)
- `shoulders, as though they were as light as beanbags.` -> `ombros, como se fossem leves feito almofadas.` (Haku, 11_07)
- `Coming through.` -> `Com licença.` (Kuon, 11_07)
- `Kuon, the remaining seven bags piled high on her\n` -> `A Kuon, com os sete sacos restantes empilhados nos\n` (Haku, 11_07)
- `shoulders, bounces effortlessly past me and out the\n` -> `ombros, passa saltitando por mim sem esforço e sai pela\n` (Haku, 11_07)
- `door.` -> `porta.` (Haku, 11_07)
- `A children's... chore...` -> `Uma tarefa... de criança...` (Haku, 11_07)
- `OK. Right. I'm just... I'm gonna act like I didn't\n` -> `Tá. Certo. Eu vou só... vou fingir que não\n` (Haku, 11_07)
- `see that.` -> `vi aquilo.` (Haku, 11_07)
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
| 0x1a6d4 | 50 | Kuon leads me to a squat stone building near the\n |
| 0x1a707 | 15 | edge of town... |
| 0x1a717 | 48 | It seems to be a storehouse--multiple bags are\n |
| 0x1a748 | 20 | stacked high inside. |
| 0x1a75d | 51 | A few lie open, seemingly full of tiny, seed-like\n |
| 0x1a791 | 9 | grains... |
| 0x1a79b | 49 | The innkeeper wants eight of these bags carried\n |
| 0x1a7cd | 17 | over to the mill. |
| 0x1a7df | 18 | I see. These, huh? |
| 0x1a7f2 | 13 | That's right. |
| 0x1a800 | 54 | She says that like it's nothing, but each sack looks\n |
| 0x1a837 | 23 | like it weighs a ton... |
| 0x1a84f | 51 | I'm surprised she wants to work after walking all\n |
| 0x1a883 | 43 | day. I wouldn't be able to even if I tried. |
| 0x1a8b3 | 38 | Yep. Eight of these. Over to the mill. |
| 0x1a8da | 54 | Urgh, she wants me to help her? I'm exhausted. I can\n |
| 0x1a911 | 33 | barely move, for crying out loud. |
| 0x1a933 | 51 | But I AM indebted to her, and it'd be bad form to\n |
| 0x1a967 | 50 | just stand and watch... She's taking care of me,\n |
| 0x1a99a | 10 | after all. |
| 0x1a9a5 | 43 | All right, let me help you out a bit, then. |
| 0x1a9d1 | 7 | ...Huh? |
| 0x1a9d9 | 54 | Kuon has an astonished look on her face. Was she not\n |
| 0x1aa10 | 30 | expecting me to offer to help? |
| 0x1aa2f | 34 | I said, let me help you out a bit. |
| 0x1aa52 | 50 | Kuon just stares in amazement for a moment, then\n |
| 0x1aa85 | 16 | smiles and nods. |
| 0x1aa96 | 51 | Mm, thanks. I appreciate it. Could you take eight\n |
| 0x1aaca | 37 | of these bags over to the mill, then? |
| 0x1aaf0 | 17 | Sure. Just eight? |
| 0x1ab02 | 16 | If you'd please. |
| 0x1ab13 | 40 | Eight... That's... actually quite a few. |
| 0x1ab3c | 21 | ...Wait a sec. Eight? |
| 0x1ab52 | 30 | Wait... You mean all of them!? |
| 0x1ab71 | 13 | Best of luck. |
| 0x1ab7f | 53 | Wait, wait, hold up. Don't give me a "best of luck"\n |
| 0x1abb5 | 43 | and bail. You're making me do all the work? |
| 0x1abe1 | 4 | Huh? |
| 0x1abe6 | 50 | Don't "huh?" me! I said I'd help, not do all the\n |
| 0x1ac19 | 13 | work for you! |
| 0x1ac27 | 48 | Um... Haku, I accepted this job for your sake.\n |
| 0x1ac58 | 46 | I'm not too keen on taking that away from you. |
| 0x1ac87 | 8 | ...What? |
| 0x1ac90 | 42 | "For my sake?" What does she mean by THAT? |
| 0x1acbb | 49 | I thought that being taken care of all the time\n |
| 0x1aced | 46 | might be weighing on you, so I wanted to help. |
| 0x1ad1c | 53 | If you had some work to do and earn your keep with,\n |
| 0x1ad52 | 42 | you wouldn't have to feel that way. Right? |
| 0x1ad7d | 4 | Wh-- |
| 0x1ad82 | 35 | That was... completely unnecessary. |
| 0x1ada6 | 47 | It's not like I feel emasculated or guilty or\n |
| 0x1add6 | 19 | anything like that. |
| 0x1adea | 52 | Either way, there's no way I'm going to be able to\n |
| 0x1ae1f | 43 | do this on my own. I'm gonna need her help. |
| 0x1ae4b | 54 | The only jobs the innkeeper had left were children's\n |
| 0x1ae82 | 39 | chores, but it's better than nothing... |
| 0x1aeaa | 21 | Children's... chores? |
| 0x1aec0 | 51 | I look over at the huge, heavy bags, each sack an\n |
| 0x1aef4 | 27 | armful, filled to the brim. |
| 0x1af10 | 16 | Something wrong? |
| 0x1af21 | 17 | KIDS carry these? |
| 0x1af33 | 48 | Huh? Yeah, when they want to work for a little\n |
| 0x1af64 | 19 | pocket money, sure. |
| 0x1af78 | 53 | I... I don't mean anything by it. I just wanted you\n |
| 0x1afae | 35 | to know why it's the only job left. |
| 0x1afd2 | 52 | Kuon adds that last part pretty quickly. I get the\n |
| 0x1b007 | 45 | feeling she thinks she's hurt my masculinity. |
| 0x1b035 | 53 | Come on, though. If this is just a kids' chore, the\n |
| 0x1b06b | 40 | bags must be way lighter than they look. |
| 0x1b094 | 51 | It can't be that bad. I guess I'd better just get\n |
| 0x1b0c8 | 13 | it over with. |
| 0x1b0d6 | 17 | Urgh... HURGH--!! |
| 0x1b0e8 | 7 | *WHUMP* |
| 0x1b0f0 | 38 | I stand corrected. They are not light. |
| 0x1b117 | 51 | The mill isn't far from here, but it's not close,\n |
| 0x1b14b | 48 | either. And I have to make the trip eight times? |
| 0x1b17c | 53 | With bags this heavy, that doesn't seem like work a\n |
| 0x1b1b2 | 49 | child could help with, let alone do on their own. |
| 0x1b1e4 | 5 | Haku? |
| 0x1b1ea | 49 | Kuon, how exactly is this a chore for children?\n |
| 0x1b21c | 23 | Are you pulling my leg? |
| 0x1b234 | 5 | Um... |
| 0x1b23a | 50 | Kuon gives an ambiguous reply and averts her eyes. |
| 0x1b26d | 18 | Why, y--I knew it. |
| 0x1b280 | 52 | ...He's probably still recovering, yeah... doesn't\n |
| 0x1b2b5 | 45 | have his full strength back. That must be it. |
| 0x1b2e3 | 30 | Hey, don't avoid the question. |
| 0x1b302 | 49 | We can't have you overexerting yourself, so sit\n |
| 0x1b334 | 29 | there while I carry them, OK? |
| 0x1b352 | 23 | Hey, I'm talking to y-- |
| 0x1b36a | 51 | And she's already gone. Geez. I won't say no to a\n |
| 0x1b39e | 42 | sit-down, but I can't say I'm not annoyed. |
| 0x1b3c9 | 45 | I manage to rouse myself and chase after her. |
| 0x1b3f7 | 51 | The sight of Kuon stacking multiple enormous bags\n |
| 0x1b42b | 51 | onto her shoulders greets me inside the storehouse. |
| 0x1b45f | 4 | Hup. |
| 0x1b464 | 21 | *WHUMP, WHUMP, WHUMP* |
| 0x1b47a | 47 | She tosses sack after sack onto a pile on her\n |
| 0x1b4aa | 52 | shoulders, as though they were as light as beanbags. |
| 0x1b4df | 15 | Coming through. |
| 0x1b4ef | 50 | Kuon, the remaining seven bags piled high on her\n |
| 0x1b522 | 53 | shoulders, bounces effortlessly past me and out the\n |
| 0x1b558 | 5 | door. |
| 0x1b55e | 24 | A children's... chore... |
| 0x1b577 | 52 | OK. Right. I'm just... I'm gonna act like I didn't\n |
| 0x1b5ac | 9 | see that. |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_07.json` com a forma:
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
