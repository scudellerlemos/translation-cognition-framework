# Cena ch_23_02 — pacote de traducao (176 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Ukon | Personagem | Ukon | manter_original | major |
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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `excitement.` -> `frenéticos.` (Haku, 14_03)
- `his face.` -> `escorrem pelo rosto.` (Narrador, 13_09)
- `Ugh...` -> `Ugh...` (Haku, 13_02)
- `leave you behind.` -> `deixe você para trás.` (Haku, 21_03)
- `me!` -> `mim!` (Haku, 18_01)
- `rate.` -> `taxa.` (Protagonista (narração), 18_01)
- `friends?` -> `amiga?` (Kuon, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `for her.` -> `pra ela.` (Haku, 15_03)
- `too much.` -> `demais.` (Narração, 17_01)
- `Dear sister...` -> `Cara irmã...` (Nekone, 15_02)
- `this...?` -> `isto...?` (Haku, 18_01)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `help.` -> `mim.` (Haku, 13_05)
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
| 0x277219 | 47 | The city's been filled with hustle and bustle\n |
| 0x277249 | 20 | since early morning. |
| 0x27725e | 50 | Today is the day Munechika and the others depart\n |
| 0x277291 | 27 | for the invasion of Tuskur. |
| 0x2772ad | 48 | The court musicians, positioned along the main\n |
| 0x2772de | 40 | gate, play a gallant and uplifting tune. |
| 0x277307 | 49 | Soldiers decked out in extravagant parade armor\n |
| 0x277339 | 37 | march in orderly rhythm to the music. |
| 0x27735f | 47 | The people of the city wave and cheer as they\n |
| 0x27738f | 30 | watch the soldiers march past. |
| 0x2773ae | 46 | All seem confident that Yamato will again be\n |
| 0x2773dd | 39 | victorious, and their eyes gleam with\n |
| 0x277405 | 11 | excitement. |
| 0x277411 | 46 | Dekopompo, whose army leads the march, nears\n |
| 0x277440 | 34 | the gates leading out of the city. |
| 0x277463 | 44 | ...And I see one man leave the procession,\n |
| 0x277490 | 46 | running towards me with tears streaming down\n |
| 0x2774bf | 9 | his face. |
| 0x2774c9 | 15 | O, Master Haku! |
| 0x2774d9 | 40 | Here, you can wipe your tears with this. |
| 0x277502 | 17 | Wait, that's my-- |
| 0x277514 | 38 | Oh, thou art too kind... *Pfflfflfflp* |
| 0x27753b | 32 | Egh, it's covered in snot now... |
| 0x27755c | 6 | Ugh... |
| 0x277563 | 45 | You better get going again or they're gonna\n |
| 0x277591 | 17 | leave you behind. |
| 0x2775a3 | 28 | F-Faith, I know this, but... |
| 0x2775c0 | 47 | Alas, my crusade taketh me o'er the wide sea,\n |
| 0x2775f0 | 47 | and already doth my heart grow heavy from our\n |
| 0x277620 | 10 | parting... |
| 0x27762b | 47 | Still, you're their tactician. You gotta keep\n |
| 0x27765b | 13 | your chin up. |
| 0x277669 | 45 | Aye, perhaps, but... in the heat of the war\n |
| 0x277697 | 37 | past, all my efforts were for naught. |
| 0x2776bd | 43 | I'faith, I... I am assailed by doubt, and\n |
| 0x2776e9 | 41 | wracked by fear. Am I unfit to serve as\n |
| 0x277713 | 13 | tactician...? |
| 0x277721 | 7 | Maro... |
| 0x277729 | 43 | I heard that Dekopompo blamed all his own\n |
| 0x277755 | 42 | mistakes on Maroro's strategy during the\n |
| 0x277780 | 11 | last war... |
| 0x27778c | 46 | I feel awful for Maroro, but this time he'll\n |
| 0x2777bb | 48 | have Munechika with him. I'm sure things won't\n |
| 0x2777ec | 13 | get that bad. |
| 0x2777fa | 44 | My sire hath ordered the building of yet a\n |
| 0x277827 | 49 | further storage-shed, to house more dear-priced\n |
| 0x277859 | 11 | antiques... |
| 0x277865 | 48 | Methinks a further blow to my wages would mark\n |
| 0x277896 | 47 | as more fatal than one from a headsman's axe... |
| 0x2778c6 | 47 | I dunno what to say... You've got it as tough\n |
| 0x2778f6 | 19 | as ever, don't you? |
| 0x27790a | 45 | You better get going, though. At this rate,\n |
| 0x277938 | 37 | you really are gonna get left behind. |
| 0x27795e | 23 | O... Thou speakst true. |
| 0x277976 | 46 | Know't, Master Haku... my heart cries out at\n |
| 0x2779a5 | 13 | our farewell. |
| 0x2779b3 | 46 | See you later, Maro. Don't go doing anything\n |
| 0x2779e2 | 13 | reckless, OK? |
| 0x2779f0 | 45 | You can go be a hero and get the glory, but\n |
| 0x277a1e | 44 | it's pointless if you don't come back alive. |
| 0x277a4b | 16 | M-Master Haku... |
| 0x277a5c | 48 | We'll go get a drink when you get home. We can\n |
| 0x277a8d | 46 | invite Ukon, everyone else--we'll all have a\n |
| 0x277abc | 10 | good time. |
| 0x277ac7 | 46 | O, Master Haku, thou art a friend to surpass\n |
| 0x277af6 | 27 | the dearest of all friends! |
| 0x277b12 | 47 | Gah! Get off me! You're getting snot all over\n |
| 0x277b42 | 3 | me! |
| 0x277b46 | 47 | Heh, geez... Guy's gonna miss the war at this\n |
| 0x277b76 | 5 | rate. |
| 0x277b7c | 46 | The procession's moved on considerably since\n |
| 0x277bab | 28 | we started talking with him. |
| 0x277bc8 | 16 | This cheering... |
| 0x277bd9 | 39 | I see. So she was bringing up the rear. |
| 0x277c01 | 48 | Maybe I'll head over to the front of the palace. |
| 0x277c32 | 45 | Yo. Looks like ya made it just in time, Boss. |
| 0x277c60 | 22 | Looks like ya made it! |
| 0x277c77 | 34 | Munechika is just about to depart. |
| 0x277c9a | 19 | Oh! Here she comes! |
| 0x277cb2 | 45 | Oho? Well, she definitely looks damn snazzy\n |
| 0x277ce0 | 10 | with that. |
| 0x277ceb | 18 | Oooh, damn snazzy! |
| 0x277cfe | 31 | Hey, why don't we go with them? |
| 0x277d1e | 10 | Like hell! |
| 0x277d29 | 39 | That's quite a lot of cheering for her. |
| 0x277d51 | 48 | It just goes to show... how much people admire\n |
| 0x277d82 | 17 | Miss Munechika... |
| 0x277d94 | 39 | Nosuri nods, a proud smile on her face. |
| 0x277dbc | 36 | I would expect no less from her...\n |
| 0x277de1 | 40 | And I am proud to count her as a friend. |
| 0x277e0a | 48 | I can count the number of times you've met her\n |
| 0x277e3b | 43 | on one hand. When the hell did you become\n |
| 0x277e67 | 8 | friends? |
| 0x277e70 | 22 | Oh, it's the princess. |
| 0x277e87 | 3 | Hm? |
| 0x277e8b | 42 | We look up to see Anju out on a balcony,\n |
| 0x277eb6 | 21 | high atop the palace. |
| 0x277ecc | 47 | She silently waves to the departing soldiers,\n |
| 0x277efc | 42 | a number of retainers subtly flanking her. |
| 0x277f27 | 50 | She must be out in public in the Mikado's stead,\n |
| 0x277f5a | 25 | to send off the soldiers. |
| 0x277f74 | 48 | When I see her like this, she really does look\n |
| 0x277fa5 | 43 | like a princess. All pristine, and regal... |
| 0x277fd1 | 40 | Or at least the opposite of when she's\n |
| 0x277ffa | 41 | lazing around with us. She looks like a\n |
| 0x278024 | 25 | totally different person. |
| 0x27803e | 44 | I would've thought she'd make a fuss about\n |
| 0x27806b | 35 | Munechika leaving, but I guess not. |
| 0x27808f | 41 | Of course she does. She is the imperial\n |
| 0x2780b9 | 20 | princess, after all. |
| 0x2780ce | 38 | Miss Anju... looks a little forlorn... |
| 0x2780f5 | 43 | I thought I saw Munechika mouth the words\n |
| 0x278121 | 19 | "I have to go now." |
| 0x278135 | 26 | And Anju... slightly nods. |
| 0x278150 | 31 | Awww, and there goes Munechika. |
| 0x278170 | 44 | ...Maybe later I'll buy some of that candy\n |
| 0x27819d | 27 | the princess loves so much. |
| 0x2781b9 | 49 | You may count on us to watch over the princess,\n |
| 0x2781eb | 10 | Munechika. |
| 0x2781f6 | 25 | I pray for your safety... |
| 0x278210 | 48 | Knowing Munechika, there's probably nothing to\n |
| 0x278241 | 12 | worry about. |
| 0x27824e | 47 | I'm sure she wouldn't do something that would\n |
| 0x27827e | 22 | make the princess sad. |
| 0x278295 | 20 | How's it going, kid? |
| 0x2782aa | 37 | So Lady Munechika has already left... |
| 0x2782d0 | 32 | Ukon? What're you doing here...? |
| 0x2782f1 | 43 | Isn't this an official send-off ceremony?\n |
| 0x27831d | 41 | Shouldn't Oshtor be doing his thing here? |
| 0x278347 | 49 | Eh, maybe. But Raiko and Dekopompo would hardly\n |
| 0x278379 | 48 | want a send-off from Oshtor, even if Munechika\n |
| 0x2783aa | 6 | might. |
| 0x2783b1 | 20 | So I'm here instead. |
| 0x2783c6 | 45 | Right. Oshtor's supposed to be against this\n |
| 0x2783f4 | 22 | whole invasion, huh... |
| 0x27840b | 43 | I guess things turned out like this anyway. |
| 0x278437 | 47 | If it's the will of our liege, then it's what\n |
| 0x278467 | 12 | we gotta do. |
| 0x278474 | 48 | What he says is truth, and he'll never lead us\n |
| 0x2784a5 | 42 | astray. We just have to follow his orders. |
| 0x2784d0 | 24 | That's just how it goes? |
| 0x2784e9 | 24 | Yep, that's how it goes. |
| 0x278502 | 29 | The will of our liege... huh. |
| 0x278520 | 25 | The invasion of Tuskur... |
| 0x27853a | 27 | What can he be thinking...? |
| 0x278556 | 47 | Uh... by the way, where's Kuon? Don't see her\n |
| 0x278586 | 18 | anywhere around... |
| 0x278599 | 34 | Kuon's still sleeping in her room. |
| 0x2785bc | 46 | Or, well... she's refusing to get up, I guess. |
| 0x2785eb | 48 | Well, nobody'd want to send off an army that's\n |
| 0x27861c | 48 | about to invade your homeland. I feel terrible\n |
| 0x27864d | 8 | for her. |
| 0x278656 | 46 | She seemed understanding about it. She knows\n |
| 0x278685 | 48 | you're not at fault here, Ukon, so don't worry\n |
| 0x2786b6 | 9 | too much. |
| 0x2786c0 | 42 | Though she can't really hide her bad mood. |
| 0x2786eb | 14 | Dear sister... |
| 0x2786fa | 47 | I'm worried. What if she becomes ill from all\n |
| 0x27872a | 8 | this...? |
| 0x278733 | 32 | I dunno. I think she'll be fine. |
| 0x278754 | 45 | Indeed, Kuon is no pushover. She and I have\n |
| 0x278782 | 49 | acknowledged each other as worthy rivals, after\n |
| 0x2787b4 | 4 | all. |
| 0x2787b9 | 33 | And when exactly did that happen? |
| 0x2787db | 44 | Well, I think she'll be fine too, but that\n |
| 0x278808 | 47 | doesn't mean we should just leave her be like\n |
| 0x278838 | 5 | that. |
| 0x27883e | 45 | So I'm going to head back now. Gotta try to\n |
| 0x27886c | 40 | cheer up our little princess, after all. |
| 0x278895 | 45 | All right. Give her, uh, my regar--you know\n |
| 0x2788c3 | 42 | what, never mind. I'll leave it up to you. |
| 0x2788ee | 16 | I-I will go too. |
| 0x2788ff | 29 | Now... how do I cheer her up? |
| 0x27891d | 42 | I guess... some good food couldn't hurt.\n |
| 0x278948 | 47 | I'll prepare a feast for her, with Rulutieh's\n |
| 0x278978 | 5 | help. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_02.json` com a forma:
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
