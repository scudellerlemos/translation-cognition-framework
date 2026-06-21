# Cena ch_20_13 — pacote de traducao (186 linhas)

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
| Akuruturuka | Termo | Akuruturuka | manter_original | major |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nakwan | Termo | Nakwan | manter_original | none |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
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
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `Nakwan` -> `Nakwan` (Personagem-Sistema, 20_06)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Uzurushan commander` -> `comandante Uzurushan` (SISTEMA, 20_05)
- `here...?` -> `aqui...?` (Haku, 18_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `...Wha...?` -> `...O quê...?` (Protagonista, 19_06)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `Wh-What...?` -> `Q-Que...?` (Nekone, 14_04)
- `You're probably right...` -> `Você provavelmente tá certo...` (Garota, 17_01)
- `Really?` -> `Mesmo?` (Kuon, 14_03)
- `soldiers.` -> `soldados.` (Oshtor, 20_01)
- `happening.` -> `acontecendo.` (Protagonista, 16_03)
- `Vurai the Vanguard...` -> `Vurai o Vanguarda...` (Kuon, 18_01)
- `Lady Munechika.` -> `Senhora Munechika.` (Atuy, 18_01)
- `everything!` -> `tudo!` (Haku, 18_04)
- `soul.` -> `alma.` (Woman (Kuon), 20_11)
- `The Imperial Guard of the Left, Mikazuchi.` -> `A Guarda Imperial da Esquerda, Mikazuchi.` (Mikazuchi, 18_01)
- `...Yes.` -> `...Sim.` (Rulutieh, 13_01)
- `ch400_00_base` -> `ch400_00_base` (SYSTEM, 20_11)
- `ch400_00_wheel` -> `ch400_00_wheel` (SYSTEM, 20_11)
- `target` -> `target` (SYSTEM, 20_11)
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
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
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
| 0x1e9ca5 | 17 | Uzurushan soldier |
| 0x1e9cb7 | 33 | What are you doing!? Keep moving. |
| 0x1e9cd9 | 6 | Nakwan |
| 0x1e9ce0 | 18 | P-Please, don't... |
| 0x1e9cf3 | 46 | It's impossible... There's no way we can run\n |
| 0x1e9d22 | 35 | down a sheer cliffside like this... |
| 0x1e9d46 | 48 | And you know what will happen to your families\n |
| 0x1e9d77 | 34 | if you don't go down... don't you? |
| 0x1e9d9a | 7 | Nngh... |
| 0x1e9da2 | 40 | You don't have a choice in the matter.\n |
| 0x1e9dcb | 14 | Now go! Go on! |
| 0x1e9dda | 15 | A-Ahhhhhhhhhhh! |
| 0x1e9dea | 29 | Wahahahahaha! Look at them!\n |
| 0x1e9e08 | 24 | They actually went down. |
| 0x1e9e21 | 44 | An easy battle, to be sure. All we must do\n |
| 0x1e9e4e | 46 | is force the nakwan forward, and watch their\n |
| 0x1e9e7d | 16 | fight from here. |
| 0x1e9e8e | 44 | Yes. The Yamatan army is even powerless to\n |
| 0x1e9ebb | 41 | reach us up here. A counteroffensive is\n |
| 0x1e9ee5 | 11 | impossible. |
| 0x1e9ef1 | 19 | Uzurushan commander |
| 0x1e9f05 | 47 | Hahaha... Now, dance. We have plenty of pawns\n |
| 0x1e9f35 | 12 | to toss out. |
| 0x1e9f42 | 30 | We'll slowly whittle you down. |
| 0x1e9f61 | 43 | Why is it that you know such prosperity...? |
| 0x1e9f8d | 46 | And why must we be the ones forced to grovel\n |
| 0x1e9fbc | 16 | like beggars...? |
| 0x1e9fcd | 47 | Why must we scurry around like dirty thieves,\n |
| 0x1e9ffd | 21 | merely to survive...? |
| 0x1ea013 | 49 | I will never forget those mocking eyes that you\n |
| 0x1ea045 | 15 | turned on us... |
| 0x1ea055 | 45 | I shall never forget how you pelted us with\n |
| 0x1ea083 | 24 | rocks and words alike... |
| 0x1ea09c | 50 | But you were right in one thing. We are thieves.\n |
| 0x1ea0cf | 41 | And so shall we take everything from you. |
| 0x1ea0f9 | 34 | And you will know our humiliation. |
| 0x1ea126 | 11 | Y-You're... |
| 0x1ea132 | 25 | H-Hey, what's the matter? |
| 0x1ea14c | 37 | It can't be... Vurai, the Vanguard... |
| 0x1ea172 | 47 | Wha... What is one of the Eight Pillars doing\n |
| 0x1ea1a2 | 8 | here...? |
| 0x1ea1ab | 27 | Maybe he came to save us... |
| 0x1ea1c7 | 48 | Please, help us! My wife and son, they've been\n |
| 0x1ea1f8 | 16 | taken prisoner-- |
| 0x1ea209 | 42 | Please, Lord Vurai, lend us your strength! |
| 0x1ea234 | 37 | ...I have been given imperial orders. |
| 0x1ea25a | 28 | And I will lay waste to all. |
| 0x1ea277 | 7 | ...Huh? |
| 0x1ea27f | 10 | ...Wha...? |
| 0x1ea28a | 9 | A-Ahhhhh! |
| 0x1ea294 | 38 | P-P-P-Please! Wait! Please, save us!\n |
| 0x1ea2bb | 25 | We didn't have a choice-- |
| 0x1ea2d5 | 35 | Th-Th-They... They're forcing us!\n |
| 0x1ea2f9 | 36 | They've taken our families hostage-- |
| 0x1ea31e | 22 | Please... have mercy-- |
| 0x1ea335 | 10 | ...Begone. |
| 0x1ea340 | 10 | A-Ahhh...! |
| 0x1ea34b | 35 | The Mikado's orders are absolute.\n |
| 0x1ea36f | 40 | All who stand in my way will be crushed. |
| 0x1ea398 | 18 | Ah... Aaaaaarrrgh! |
| 0x1ea3ab | 6 | Erupt. |
| 0x1ea3b2 | 6 | Hm...? |
| 0x1ea3b9 | 7 | Wha--!? |
| 0x1ea3c1 | 45 | I take it you are the flies responsible for\n |
| 0x1ea3ef | 23 | this ceaseless buzzing. |
| 0x1ea407 | 11 | Wh-What...? |
| 0x1ea413 | 34 | Wh-What are you!? How did you...\n |
| 0x1ea436 | 36 | What have you done with the nakw--\n |
| 0x1ea45b | 18 | No... it can't be! |
| 0x1ea46e | 46 | He can't have jumped all the way up here...!\n |
| 0x1ea49d | 13 | I-Impossible! |
| 0x1ea4ab | 47 | Argh... I knew those nakwans would be useless\n |
| 0x1ea4db | 11 | in the end! |
| 0x1ea4e7 | 25 | The enemy is before us!\n |
| 0x1ea501 | 17 | To arms! To arms! |
| 0x1ea513 | 45 | You are a fool for wandering up here alone!\n |
| 0x1ea541 | 38 | You will pay with your life! Kill him! |
| 0x1ea568 | 20 | Mere child's play... |
| 0x1ea57d | 9 | What...!? |
| 0x1ea587 | 23 | Y-You can't be... No... |
| 0x1ea59f | 50 | Whew... I think we've gone far enough to be safe\n |
| 0x1ea5d2 | 39 | for now. Let's take a break over there. |
| 0x1ea5fa | 18 | Cocopo, stop here. |
| 0x1ea633 | 49 | The carriage stops with Cocopo's shrill chirping. |
| 0x1ea665 | 50 | We kept going through the night, so we should be\n |
| 0x1ea698 | 48 | pretty far from the barbarian encampment by now. |
| 0x1ea6c9 | 45 | It might be a little difficult to return to\n |
| 0x1ea6f7 | 34 | Yamato immediately, in this state. |
| 0x1ea71a | 24 | You're probably right... |
| 0x1ea733 | 46 | It'll be hard to keep traveling with so many\n |
| 0x1ea762 | 44 | injured, and with the worn-out nakwans and\n |
| 0x1ea78f | 15 | their families. |
| 0x1ea79f | 51 | If I recall correctly, there should be a fortress\n |
| 0x1ea7d3 | 34 | defended by Lady Munechika nearby. |
| 0x1ea7f6 | 34 | All right, let's head there first. |
| 0x1ea819 | 49 | I'm sure Munechika wouldn't treat these nakwans\n |
| 0x1ea84b | 6 | badly. |
| 0x1ea852 | 34 | Looks like I really owe you, boss. |
| 0x1ea875 | 49 | Don't worry about it. We end up doing this kind\n |
| 0x1ea8a7 | 15 | of thing a lot. |
| 0x1ea8b7 | 7 | Really? |
| 0x1ea8bf | 47 | Before I know it, we're usually wrapped up in\n |
| 0x1ea8ef | 41 | some crisis or another... thanks to them. |
| 0x1ea919 | 47 | Seriously. Why does it always end up like this? |
| 0x1ea949 | 21 | Heh... Heh heh heh... |
| 0x1ea95f | 20 | What's so funny now? |
| 0x1ea974 | 45 | Eh, nothin'. Gotta say, boss, you're a real\n |
| 0x1ea9a2 | 18 | interesting fella. |
| 0x1ea9b8 | 29 | Wh-What the hell was that...? |
| 0x1ea9d6 | 17 | Look! Over there! |
| 0x1ea9e8 | 50 | We all look to where Nosuri is pointing, and see\n |
| 0x1eaa1b | 41 | a sight that makes us doubt our own eyes. |
| 0x1eaa45 | 44 | Across the canyon, a lone man--massive and\n |
| 0x1eaa72 | 42 | muscled--faces down an army of Uzurushan\n |
| 0x1eaa9d | 9 | soldiers. |
| 0x1eaaa7 | 39 | Suddenly, the man is engulfed by flame. |
| 0x1eaacf | 50 | Seconds later, the man has turned into something\n |
| 0x1eab02 | 16 | else altogether. |
| 0x1eab13 | 20 | Wh-What in... the... |
| 0x1eab28 | 41 | The giant creature in his place gives a\n |
| 0x1eab52 | 49 | deafening roar, and begins to maul the soldiers\n |
| 0x1eab84 | 15 | surrounding it. |
| 0x1eab94 | 46 | No... "Maul" isn't enough to describe what's\n |
| 0x1eabc3 | 10 | happening. |
| 0x1eabce | 45 | The Uzurushan soldiers can't even touch it.\n |
| 0x1eabfc | 45 | As soon as they draw close, they burst into\n |
| 0x1eac2a | 6 | flame. |
| 0x1eac31 | 16 | It's a massacre. |
| 0x1eac42 | 31 | What the hell is that monster!? |
| 0x1eac62 | 21 | Vurai the Vanguard... |
| 0x1eac78 | 45 | One of the Eight Pillar Generals of Yamato,\n |
| 0x1eaca6 | 45 | granted an Akuruka like my dear brother and\n |
| 0x1eacd4 | 15 | Lady Munechika. |
| 0x1eace4 | 46 | I'm not talking about Eight Pillar Generals!\n |
| 0x1ead13 | 43 | What IS that monster!? He transformed and\n |
| 0x1ead3f | 11 | everything! |
| 0x1ead4b | 34 | How dare you call him a monster.\n |
| 0x1ead6e | 22 | What are you thinking? |
| 0x1ead85 | 47 | Then what the hell am I supposed to call that\n |
| 0x1eadb5 | 7 | thing!? |
| 0x1eadbd | 12 | Akuruturuka. |
| 0x1eadca | 18 | ...An Akuruturuka? |
| 0x1eaddd | 41 | Hold on, Boss. You don't know about the\n |
| 0x1eae07 | 12 | Akuruturuka? |
| 0x1eae14 | 48 | The Akuruka serves as a gate to the great power. |
| 0x1eae45 | 46 | Only mononofu acknowledged by the Mikado and\n |
| 0x1eae74 | 47 | chosen by the Akuruka may take holy form with\n |
| 0x1eaea4 | 10 | its power. |
| 0x1eaeaf | 48 | Yes. I've heard rumors before, but this is the\n |
| 0x1eaee0 | 34 | first time I've set eyes on one... |
| 0x1eaf03 | 48 | The power of the Origin, capable of ending any\n |
| 0x1eaf34 | 49 | life... An all-consuming domain of destruction... |
| 0x1eaf66 | 45 | I only know this from rumor, but it is said\n |
| 0x1eaf94 | 45 | that each Akuruka is blessed with different\n |
| 0x1eafc2 | 18 | special abilities. |
| 0x1eafd5 | 49 | But one must be careful not to use their powers\n |
| 0x1eb007 | 9 | overmuch. |
| 0x1eb011 | 40 | What... happens if they use it too much? |
| 0x1eb03a | 50 | I have heard that the Akuruka slowly assimilates\n |
| 0x1eb06d | 47 | its bearer, and eventually will consume their\n |
| 0x1eb09d | 5 | soul. |
| 0x1eb0a3 | 46 | And they still use these powers, knowing the\n |
| 0x1eb0d2 | 8 | risk...? |
| 0x1eb0db | 44 | That's terrifying. Is that how the Yamatan\n |
| 0x1eb108 | 45 | generals with these Akurukas have to live...? |
| 0x1eb136 | 41 | Correct. And it's said that among them,\n |
| 0x1eb160 | 32 | Lord Vurai's power is unrivaled. |
| 0x1eb181 | 14 | So that guy... |
| 0x1eb190 | 29 | ...is a Yamatan general...?\n |
| 0x1eb1ae | 14 | That thing...? |
| 0x1eb1bd | 46 | Two faces pop up in my mind as I contemplate\n |
| 0x1eb1ec | 12 | the Akuruka. |
| 0x1eb1f9 | 46 | Two people who hide their faces behind masks\n |
| 0x1eb228 | 13 | like Vurai's. |
| 0x1eb236 | 48 | The Imperial Guard of the Right, Oshtor... and\n |
| 0x1eb267 | 42 | the Imperial Guard of the Left, Mikazuchi. |
| 0x1eb292 | 43 | Which means... those two... are the same... |
| 0x1eb2be | 7 | ...Yes. |
| 0x1eb2c6 | 43 | My dear brother, Lord Mikazuchi, and Lady\n |
| 0x1eb2f2 | 48 | Munechika... All chosen by the Mikado to wield\n |
| 0x1eb323 | 50 | All of us just stand there--struck silent by the\n |
| 0x1eb356 | 16 | sight before us. |
| 0x1eb368 | 13 | ch400_00_base |
| 0x1eb376 | 14 | ch400_00_wheel |
| 0x1eb385 | 6 | target |
| 0x1eb38c | 8 | env_bone |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_13.json` com a forma:
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
