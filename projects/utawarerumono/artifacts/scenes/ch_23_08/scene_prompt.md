# Cena ch_23_08 — pacote de traducao (212 linhas)

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
| Cocopo | Criatura | Cocopo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Soyankekur | Personagem | Soyankekur | manter_original | moderate |
| toriuma | Criatura | toriuma | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Crew` -> `Grupo` (SISTEMA, 19_08)
- `Tuskur.` -> `Tuskur.` (Haku, 23_03)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `yeah?` -> `tá?` (Ukon, 14_02)
- `happily.` -> `feliz.` (Haku, 11_10)
- `this...` -> `isto...` (Kuon, 11_08)
- `R-Right...` -> `C-Certo...` (Haku, 11_09)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `...Haku.` -> `...Haku.` (Haku, 22_05)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `Thank you, dear sister.` -> `Obrigada, cara irmã.` (Nekone, 15_01)
- `What are you talking about?` -> `Do que você está falando?` (Kuon, 19_05)
- `Dear sister...?` -> `Cara irmã...?` (Nekone, 18_01)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `don't you?` -> `não tem?` (Kuon, 14_10)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `...I don't get it.` -> `...Não entendo.` (Haku, 18_01)
- `this country.` -> `este país.` (Mikado, 23_01)
- `Dear sister...` -> `Cara irmã...` (Nekone, 15_02)
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
| 0x290375 | 23 | All right! Drop anchor! |
| 0x29038d | 4 | Crew |
| 0x290392 | 8 | YES SIR! |
| 0x29039b | 45 | After days of rocking back and forth on the\n |
| 0x2903c9 | 43 | water, the ship coasts up to the shore of\n |
| 0x2903f5 | 7 | Tuskur. |
| 0x2903fd | 46 | Mmmm! This wind, this scent... We're finally\n |
| 0x29042c | 5 | here. |
| 0x290432 | 17 | This is Tuskur... |
| 0x290444 | 48 | By all appearances, the botanical variance and\n |
| 0x290475 | 44 | geological formation seem quite similar to\n |
| 0x2904a2 | 9 | Yamato's. |
| 0x2904ac | 48 | Well, it may be a foreign land across the sea,\n |
| 0x2904dd | 47 | but it's still just a place where folks live,\n |
| 0x29050d | 5 | yeah? |
| 0x290513 | 48 | Honored passengers! We'll be handling all your\n |
| 0x290544 | 30 | luggage. Please, go on ashore. |
| 0x290563 | 22 | Oh... Very good, then. |
| 0x29057a | 45 | Welp, might as well leave the heavy lifting\n |
| 0x2905a8 | 41 | to these guys. Let's head down, shall we? |
| 0x2905d2 | 42 | Oh, land! Sweet, blessed, glorious LAND!\n |
| 0x2905fd | 46 | I give thanks that I have set foot upon you,\n |
| 0x29062c | 35 | into your stable embrace once more! |
| 0x290650 | 50 | Oh, it feels so good! Two feet on sturdy ground!\n |
| 0x290683 | 45 | This scent! This feel! People BELONG on land! |
| 0x2906b1 | 48 | Nosuri appears so glad to reach shore that she\n |
| 0x2906e2 | 50 | falls to the ground, rubbing her face against it\n |
| 0x290715 | 8 | happily. |
| 0x29071e | 49 | Seems a bit much, but it makes sense. She spent\n |
| 0x290750 | 42 | most of the voyage green with seasickness. |
| 0x29077b | 48 | I get what you mean, yeah? Didn't think I'd be\n |
| 0x2907ac | 48 | so glad to stand on somethin' that ain't movin'. |
| 0x2907dd | 40 | Is that how it is? I tend to feel more\n |
| 0x290806 | 41 | comfortable aboard the ship than on land. |
| 0x290830 | 48 | Well, you did spend a lot of your childhood on\n |
| 0x290861 | 19 | a ship, didn't you? |
| 0x290875 | 38 | Give me land over the ocean any day.\n |
| 0x29089c | 18 | Definitely land... |
| 0x2908af | 51 | So, this is the base of operations for the Tuskur\n |
| 0x2908e3 | 11 | invasion... |
| 0x2908ef | 48 | I never thought I'd see a port in a place like\n |
| 0x290920 | 7 | this... |
| 0x290928 | 43 | We look around to see other Yamatan ships\n |
| 0x290954 | 32 | besides ours moored in the area. |
| 0x290975 | 48 | On the shore, there are small supply sheds and\n |
| 0x2909a6 | 42 | barracks areas, and troops stationed for\n |
| 0x2909d1 | 8 | defense. |
| 0x2909da | 23 | ...How's the unloading? |
| 0x2909f2 | 37 | It seems to be going smoothly so far. |
| 0x290a18 | 49 | I follow Kiwru's gaze to see our supplies being\n |
| 0x290a4a | 23 | unloaded from the ship. |
| 0x290a62 | 45 | The crew flows in a stream between land and\n |
| 0x290a90 | 45 | ship, loading supplies onto small boats and\n |
| 0x290abe | 11 | then carts. |
| 0x290aca | 38 | Wooden crates onto the cart, please.\n |
| 0x290af1 | 42 | Ah, that one is heavier than it appears.\n |
| 0x290b1c | 13 | Do take care. |
| 0x290b2a | 33 | Guess we can grab that one, then. |
| 0x290b4c | 37 | Cocopo, could you help us carry this? |
| 0x290b86 | 49 | As usual, Ougi's in his element. Guess I should\n |
| 0x290bb8 | 19 | expect this by now. |
| 0x290bcc | 41 | Looks like we can head out pretty soon,\n |
| 0x290bf6 | 13 | at this rate. |
| 0x290c04 | 29 | Awww, are we leaving already? |
| 0x290c22 | 44 | Yeah. We're delivering emergency supplies.\n |
| 0x290c4f | 42 | We should say goodbye to Lord Soyankekur\n |
| 0x290c7a | 15 | while we can... |
| 0x290c8a | 29 | AAAAAAAAAAAATUUUUUUUYYYYYYY!! |
| 0x290ca8 | 25 | Hm? Speak of the devil... |
| 0x290cc2 | 32 | Sorry to keep you waiting, Atuy! |
| 0x290ce3 | 17 | Whoa!? The hell!? |
| 0x290cf5 | 42 | What do you mean by kept me waiting, Papa? |
| 0x290d20 | 41 | Hahaha, can't you tell, my sweet little\n |
| 0x290d4a | 44 | Atuy? I'm obviously coming along with you,\n |
| 0x290d77 | 23 | my darling sea blossom. |
| 0x290d8f | 47 | After all, we're heading into enemy territory\n |
| 0x290dbf | 45 | now. And I can't very well let my Atuy just\n |
| 0x290ded | 37 | stroll into danger alone, can I, pet? |
| 0x290e13 | 45 | Papa, I appreciate the thought, but I'll be\n |
| 0x290e41 | 27 | fine. You need to stay put. |
| 0x290e5d | 50 | What, are you worried about my ships? Oh, such a\n |
| 0x290e90 | 48 | thoughtful and considerate daughter, my Atuy is! |
| 0x290ec1 | 45 | Don't you worry, my sweetheart, I'm leaving\n |
| 0x290eef | 45 | behind enough soldiers to keep them safe as\n |
| 0x290f1d | 7 | houses. |
| 0x290f25 | 49 | And besides, this port has troops under Raiko's\n |
| 0x290f57 | 44 | direct command. They don't need me hanging\n |
| 0x290f84 | 24 | about, do they, pumpkin? |
| 0x290f9d | 31 | That's not what the problem is. |
| 0x290fbd | 44 | Ahahaha! You worried I've forgotten how to\n |
| 0x290fea | 19 | swing a blade, now? |
| 0x290ffe | 44 | Hmhmhm... Your dear old daddy's not one of\n |
| 0x29102b | 40 | the Eight Pillar Generals for nothing.\n |
| 0x291054 | 37 | I've never skipped a day of training. |
| 0x29107a | 50 | Soyankekur puffs out his chest in pride, flexing\n |
| 0x2910ad | 38 | his muscles beneath the fancy clothes. |
| 0x2910d4 | 45 | In a chain reaction, all the men behind him\n |
| 0x291102 | 44 | start flexing, and things start feeling...\n |
| 0x29112f | 7 | sweaty. |
| 0x291137 | 45 | In other words, this is getting really weird. |
| 0x291165 | 26 | Ugh... Please stop that... |
| 0x291180 | 43 | Soyankekur, our primary mission is supply\n |
| 0x2911ac | 48 | delivery. If we travel in a large group, we'll\n |
| 0x2911dd | 16 | attract enemies. |
| 0x2911ee | 18 | Hm, all the same-- |
| 0x291201 | 45 | We'll be fine! I'm your daughter, aren't I?\n |
| 0x29122f | 42 | Those Tuskur soldiers are no match for me. |
| 0x29125a | 44 | Oh, my Atuy... I suppose every fledgling's\n |
| 0x291287 | 34 | bound to leave the nest one day... |
| 0x2912aa | 44 | Fine, fine. If that's how it is, I'll stay\n |
| 0x2912d7 | 39 | here, my girl. But don't you go doing\n |
| 0x2912ff | 23 | anything reckless, aye? |
| 0x291317 | 22 | We know. Thanks, Papa. |
| 0x29132e | 40 | Haku. I expect you'll keep my daughter\n |
| 0x291357 | 16 | absolutely safe. |
| 0x291368 | 46 | His hand descends on my shoulder with a thump. |
| 0x291397 | 10 | R-Right... |
| 0x2913a2 | 42 | I'm sure you understand, but if anything\n |
| 0x2913cd | 43 | happens to her... well, we know who'll be\n |
| 0x2913f9 | 45 | answering for it, aye? Hope we're clear, lad. |
| 0x291427 | 33 | His grip on my shoulder tightens. |
| 0x291449 | 15 | Gah!? Owowowow! |
| 0x291459 | 45 | He's smiling... but I can see murder in his\n |
| 0x291487 | 7 | eyes... |
| 0x29148f | 27 | Haku, may we have a moment? |
| 0x2914ab | 44 | As Soyankekur leaves (albeit reluctantly),\n |
| 0x2914d8 | 45 | Nekone and Ougi walk over with a map in hand. |
| 0x291506 | 11 | What is it? |
| 0x291512 | 42 | We would like to survey our route to the\n |
| 0x29153d | 20 | fortress beforehand. |
| 0x291552 | 46 | Now, our current position is... here, at the\n |
| 0x291581 | 10 | coastline. |
| 0x29158c | 50 | And the fortress currently housing Munechika and\n |
| 0x2915bf | 22 | the others is... here. |
| 0x2915d6 | 45 | It appears there's a rather large road that\n |
| 0x291604 | 37 | leads from the shore to the fortress. |
| 0x29162a | 29 | It seems to be a direct path. |
| 0x291648 | 47 | It's pretty long. And it's out in the open...\n |
| 0x291678 | 24 | This could be a problem. |
| 0x291691 | 45 | Yes. It would be foolish to directly follow\n |
| 0x2916bf | 10 | this path. |
| 0x2916ca | 43 | We'd be serving ourselves up to the enemy\n |
| 0x2916f6 | 20 | forces on a platter. |
| 0x29170b | 49 | It appears previous attempts have been met with\n |
| 0x29173d | 20 | grievous casualties. |
| 0x291752 | 47 | However... besides this road, the entire area\n |
| 0x291782 | 35 | is far too mountainous to traverse. |
| 0x2917a6 | 44 | Yes. My dear sister and I are used to such\n |
| 0x2917d3 | 45 | areas, but our expertise means little for a\n |
| 0x291801 | 27 | fully-loaded supply convoy. |
| 0x29181d | 47 | Guess we just gotta prepare for the worst and\n |
| 0x29184d | 15 | hit the road... |
| 0x29185d | 8 | ...Haku. |
| 0x291866 | 3 | Hm? |
| 0x29186a | 48 | Is anyone here thirsty? I got some fresh water\n |
| 0x29189b | 45 | from that stream. It should be nice and cool. |
| 0x2918c9 | 11 | Oh, thanks. |
| 0x2918d5 | 23 | Thank you, dear sister. |
| 0x2918ed | 44 | Ah, you needn't have gone to such trouble.\n |
| 0x29191a | 27 | Much appreciated, I'm sure. |
| 0x29193a | 45 | The cool water feels good going down, after\n |
| 0x291968 | 45 | being out in that salty sea wind for so long. |
| 0x291996 | 24 | Whew, that hit the spot. |
| 0x2919af | 44 | Ahhh, it has been a while since I have had\n |
| 0x2919dc | 12 | fresh water. |
| 0x2919e9 | 42 | Indeed. Water is something of a valuable\n |
| 0x291a14 | 25 | resource when out at sea. |
| 0x291a2e | 46 | What's the matter with her? Kuon's just been\n |
| 0x291a5d | 27 | quietly staring this way... |
| 0x291a79 | 36 | Haku, can I take a look at that map? |
| 0x291a9e | 47 | Kuon reaches for the map, studying it intently. |
| 0x291ace | 48 | ...I thought so. Since it's not recorded here,\n |
| 0x291aff | 46 | the Yamatan forces must not have found it yet. |
| 0x291b2e | 27 | What are you talking about? |
| 0x291b4a | 44 | This isn't the only path to this fortress.\n |
| 0x291b77 | 39 | There's another one that's more hidden. |
| 0x291b9f | 13 | Wait, really? |
| 0x291bad | 50 | It'll be a detour, and it's not well-maintained.\n |
| 0x291be0 | 49 | We may be found by beasts, but not Tuskur forces. |
| 0x291c12 | 15 | Dear sister...? |
| 0x291c22 | 49 | You think we'd be able to drive carts through it? |
| 0x291c54 | 50 | If we divide the cargo up into smaller groups...\n |
| 0x291c87 | 11 | then maybe? |
| 0x291c93 | 40 | Got it... OK, let's try that route then. |
| 0x291cbc | 48 | Ougi, you mind telling the guys setting up the\n |
| 0x291ced | 6 | cargo? |
| 0x291cf4 | 49 | If the roads won't be as well-maintained, we'll\n |
| 0x291d26 | 44 | have to adjust the equipment for the steeds. |
| 0x291d53 | 20 | Of course--allow me. |
| 0x291d68 | 9 | *Sigh*... |
| 0x291d72 | 23 | What was that sigh for? |
| 0x291d8a | 39 | Why aren't you at all suspicious of me? |
| 0x291db2 | 14 | ...About what? |
| 0x291dc1 | 48 | And when you just accepted that water from me.\n |
| 0x291df2 | 45 | I'm Kuon of TUSKUR! You do understand this,\n |
| 0x291e20 | 10 | don't you? |
| 0x291e2b | 5 | Oh... |
| 0x291e31 | 18 | ...I don't get it. |
| 0x291e44 | 50 | You're clearly the one that knows the most about\n |
| 0x291e77 | 13 | this country. |
| 0x291e85 | 42 | That's why I asked your opinion on this.\n |
| 0x291eb0 | 24 | What's weird about that? |
| 0x291ecf | 14 | Dear sister... |
| 0x291ede | 28 | I-It's nothing. I think...\n |
| 0x291efb | 30 | I think I'll go help Rulutieh! |
| 0x291f1a | 30 | I-I'll help too, dear sister-- |
| 0x291f39 | 44 | Probably better for Nekone and Rulutieh to\n |
| 0x291f66 | 40 | handle this rather than have me butt in. |
| 0x291f8f | 41 | I should hurry and get ready to head out. |
| 0x291fb9 | 26 | So this is Tuskur, huh...? |
| 0x291fd4 | 41 | They call it the land where god sleeps.\n |
| 0x291ffe | 39 | The question is... what kind of god...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_08.json` com a forma:
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
