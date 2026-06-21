# Cena ch_21_03 — pacote de traducao (341 linhas)

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
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Yamatan | Etnia | de Yamato | traduzir | none |

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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `surface.` -> `superfície.` (Haku, 14_03)
- `Guard` -> `Guarda` (Mikazuchi, 18_01)
- `Yes.` -> `Sim.` (Haku, 17_01)
- `end.` -> `fim.` (Kuon, 15_02)
- `ruins.` -> `ruínas.` (Haku, 21_01)
- `himself.` -> `si mesmo.` (Nekone, 14_04)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `Urk...` -> `Argh...` (Haku, 12_06)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `Yeah...` -> `É...` (Kuon, 11_02)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `dear sister?` -> `cara irmã?` (Nekone, 15_01)
- `Haku.` -> `Haku.` (Kuon, 12_08)
- `Really?` -> `Mesmo?` (Kuon, 14_03)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `But...` -> `mas...` (Kuon, 11_01)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `Ah!?` -> `Ah!?` (Rulutieh, 14_04)
- `...Haku?` -> `...Haku?` (Garota, 16_01)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `Ah... ah...` -> `Ah... ah...` (Protagonista, 19_08)
- `You're...` -> `Você está...` (Protagonista, 16_04)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
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
| 0x219c69 | 47 | Welp, didn't think I'd be coming back to this\n |
| 0x219c99 | 20 | country like this... |
| 0x219cae | 45 | So this is it? These so-called mystic ruins\n |
| 0x219cdc | 14 | they've found? |
| 0x219ceb | 16 | I suppose it is. |
| 0x219cfc | 50 | I see several tents pitched around a rocky area,\n |
| 0x219d2f | 45 | with a number of Yamatan soldiers patrolling. |
| 0x219d5d | 43 | Among them I also see scholars, hurriedly\n |
| 0x219d89 | 20 | bustling to and fro. |
| 0x219d9e | 50 | And beyond that, I see a giant rock, the size of\n |
| 0x219dd1 | 10 | a mansion. |
| 0x219ddc | 46 | On one corner of the rock, I see a hole that\n |
| 0x219e0b | 44 | seems to lead down into a cave beneath the\n |
| 0x219e38 | 8 | surface. |
| 0x219e41 | 49 | Many soldiers stand guard in front, stern looks\n |
| 0x219e73 | 41 | on their faces and spears in their hands. |
| 0x219e9d | 46 | All told, the place looks pretty intimidating. |
| 0x219ecc | 47 | Guess it makes sense. Might be some Uzurushan\n |
| 0x219efc | 41 | army remnants roaming around these parts. |
| 0x219f26 | 48 | It would be a devastating loss if they were to\n |
| 0x219f57 | 37 | damage the precious ruins, after all. |
| 0x219f7d | 43 | Hrm. I thought you said it was untouched... |
| 0x219fa9 | 17 | Hm. So, what now? |
| 0x219fbb | 48 | Well, our job is to investigate the ruins, but\n |
| 0x219fec | 23 | we did just get here... |
| 0x21a004 | 45 | Why don't we rest first, and then begin our\n |
| 0x21a032 | 21 | investigation tomor-- |
| 0x21a04c | 48 | Er, well, standing here won't get us anywhere.\n |
| 0x21a07d | 41 | Why don't we ask them to let us in first? |
| 0x21a0a7 | 48 | I get it, you two. Would you stop glaring like\n |
| 0x21a0d8 | 45 | you're about to pounce? God, they're scary... |
| 0x21a106 | 48 | We head over to talk to one of the guards first. |
| 0x21a137 | 14 | Uh, excuse me. |
| 0x21a146 | 5 | Guard |
| 0x21a14c | 20 | Mm? Who are you lot? |
| 0x21a161 | 16 | Uruuru, Saraana. |
| 0x21a172 | 4 | Yes. |
| 0x21a177 | 49 | The twins step forward, holding out a small box\n |
| 0x21a1a9 | 28 | with a crest engraved in it. |
| 0x21a1c6 | 50 | It's lacquered outside with gold patterns on it,\n |
| 0x21a1f9 | 48 | and has a string with a tassel attached at the\n |
| 0x21a22a | 4 | end. |
| 0x21a22f | 14 | Th-That's...!? |
| 0x21a23e | 48 | The expression on the guard's face immediately\n |
| 0x21a26f | 27 | changes as he sees the box. |
| 0x21a28b | 48 | We've come to investigate the ruins. You don't\n |
| 0x21a2bc | 32 | mind letting us through, do you? |
| 0x21a2dd | 31 | M-My apologies, honored sir!!\n |
| 0x21a2fd | 18 | Please, go ahead!! |
| 0x21a310 | 37 | Instant access, no questions asked... |
| 0x21a336 | 35 | Man, this thing is almost TOO good. |
| 0x21a35a | 44 | After seeing how much authority this thing\n |
| 0x21a387 | 44 | actually holds, we step forward toward the\n |
| 0x21a3b4 | 6 | ruins. |
| 0x21a3bb | 43 | What was all that about? That soldier was\n |
| 0x21a3e7 | 43 | backtracking so hard he was trippin' over\n |
| 0x21a413 | 8 | himself. |
| 0x21a41c | 43 | Haku... I'd like to know exactly what you\n |
| 0x21a448 | 23 | showed to him, I think. |
| 0x21a460 | 17 | What? This thing? |
| 0x21a477 | 46 | Just like the soldier, everyone's expression\n |
| 0x21a4a6 | 40 | immediately changes as they see the box. |
| 0x21a4cf | 40 | H-Haku!? I-Is that... Is that really...? |
| 0x21a4f8 | 35 | The crest engraved in it. That is-- |
| 0x21a51c | 49 | Stop right there. Probably best if nobody pries\n |
| 0x21a54e | 18 | further into that. |
| 0x21a561 | 46 | Wait! But that crest is only ever granted to\n |
| 0x21a590 | 47 | those trusted and chosen by the Mikado himself! |
| 0x21a5c0 | 42 | Thought as much... No wonder the soldier\n |
| 0x21a5eb | 32 | completely changed his attitude. |
| 0x21a60c | 47 | Haku, I'd like to know why you have something\n |
| 0x21a63c | 26 | like that on you, I think! |
| 0x21a657 | 20 | Uhh, well. That's... |
| 0x21a66c | 34 | How do I explain it to these guys? |
| 0x21a68f | 46 | Really, I doubt they'll believe me even if I\n |
| 0x21a6be | 28 | tell them the whole truth... |
| 0x21a6db | 15 | MASTER HAAAKU!! |
| 0x21a6eb | 6 | ...Hm? |
| 0x21a6f2 | 40 | I suddenly hear a voice in the distance. |
| 0x21a71b | 43 | O, what fortuitous chance to reunite upon\n |
| 0x21a747 | 21 | such hallowed ground! |
| 0x21a75d | 28 | That voice... It can't be... |
| 0x21a77a | 41 | My stomach sinking, I slowly turn around. |
| 0x21a7a4 | 34 | O, how my heart hath missed thee!! |
| 0x21a7c7 | 48 | From the cavernous depths, a pasty white-faced\n |
| 0x21a7f8 | 45 | Nugwisomkami bolts toward us, hair whipping\n |
| 0x21a826 | 6 | askew. |
| 0x21a82d | 7 | Wha--!? |
| 0x21a835 | 44 | The Nugwisomkami bounds forward, as though\n |
| 0x21a862 | 29 | trying to jump on top of us-- |
| 0x21a880 | 51 | O nature's axiom, cast yourself before our Master\n |
| 0x21a8b4 | 15 | to form a wall. |
| 0x21a8c4 | 11 | Bhwurff--!? |
| 0x21a8d0 | 46 | The pale figure crashes against an invisible\n |
| 0x21a8ff | 31 | wall, then sinks to the ground. |
| 0x21a91f | 10 | Close one. |
| 0x21a92a | 23 | Master, are you unhurt? |
| 0x21a942 | 40 | ...Maybe it'd be better to ask him that. |
| 0x21a96b | 50 | O generous fates! I did not expect that ye would\n |
| 0x21a99e | 39 | come to plumb these fantastical depths. |
| 0x21a9c6 | 46 | It seemeth, Master Haku, that the threads of\n |
| 0x21a9f5 | 33 | our fates are entwined eternal... |
| 0x21aa17 | 46 | Please don't say creepy stuff like that with\n |
| 0x21aa46 | 13 | a huge smile. |
| 0x21aa54 | 47 | We head deeper into the ruins, with Maroro as\n |
| 0x21aa84 | 10 | our guide. |
| 0x21aa8f | 47 | He tells us that those already here came as a\n |
| 0x21aabf | 49 | reconnaissance team sent by Oshtor to make sure\n |
| 0x21aaf1 | 12 | it was safe. |
| 0x21aafe | 46 | In any case, I guess I'm glad we got off the\n |
| 0x21ab2d | 24 | subject of that crest... |
| 0x21ab46 | 43 | I probably shouldn't go whipping that out\n |
| 0x21ab72 | 22 | without a good reason. |
| 0x21ab89 | 48 | I'faith, such pursuits doth suit me FAR better\n |
| 0x21abba | 22 | than the trade of war. |
| 0x21abd1 | 36 | The thrill of histories unglean'd!\n |
| 0x21abf6 | 34 | Relics unearth'd! Sooths unsaid!\n |
| 0x21ac19 | 29 | My scholar's heart QUIVERETH! |
| 0x21ac37 | 46 | You are not a scholar. You are still only an\n |
| 0x21ac66 | 13 | underscholar. |
| 0x21ac74 | 6 | Urk... |
| 0x21ac7b | 47 | We make our way through the caves as we talk,\n |
| 0x21acab | 46 | until we reach an area where the view changes. |
| 0x21acda | 45 | Even our reach has yet to extend beyond yon\n |
| 0x21ad08 | 11 | corridor... |
| 0x21ad17 | 28 | Kuon's ears perk up at that. |
| 0x21ad34 | 47 | Then that means... we're the first to come to\n |
| 0x21ad64 | 10 | this area? |
| 0x21ad6f | 13 | Yes, just so. |
| 0x21ad7d | 7 | Nekone. |
| 0x21ad85 | 17 | Yes, dear sister! |
| 0x21ad97 | 47 | Both Kuon and Nekone move forward, eager with\n |
| 0x21adc7 | 13 | anticipation. |
| 0x21add5 | 47 | Hey, uh... aren't those girls actin' a little\n |
| 0x21ae05 | 21 | different than usual? |
| 0x21ae1b | 49 | Oh no... Nekone's going somewhere I'll never be\n |
| 0x21ae4d | 16 | able to reach... |
| 0x21ae5e | 41 | You don't see this style much. It looks\n |
| 0x21ae88 | 49 | architecturally unlike ruins near the capital--\n |
| 0x21aeba | 29 | moreso the sites in the west? |
| 0x21aed8 | 45 | Yes, quite. I note some definite structural\n |
| 0x21af06 | 41 | parallels to ruins in the Kotappo region. |
| 0x21af30 | 34 | Oh, take a look at this pattern... |
| 0x21af53 | 49 | It looks like... the same symbology used by the\n |
| 0x21af85 | 28 | Hamyana Island civilization? |
| 0x21afa2 | 44 | Precisely! But the sites are so far apart.\n |
| 0x21afcf | 47 | This may imply some cultural exchange between\n |
| 0x21afff | 16 | the two regions. |
| 0x21b010 | 44 | Consider the area of distribution, though.\n |
| 0x21b03d | 48 | Who is to say this land was not itself settled\n |
| 0x21b06e | 25 | by migrants from Hamyana? |
| 0x21b088 | 43 | ...I have absolutely no idea what they're\n |
| 0x21b0b4 | 14 | talking about. |
| 0x21b0c3 | 45 | We all trail behind the two of them as they\n |
| 0x21b0f1 | 45 | examine the walls and floors with eager eyes. |
| 0x21b11f | 46 | It seems that it would be best to leave this\n |
| 0x21b14e | 17 | job to those two. |
| 0x21b160 | 7 | Yeah... |
| 0x21b168 | 18 | But these ruins... |
| 0x21b17b | 51 | I get the weird feeling I've been here before...?\n |
| 0x21b1af | 33 | No, it's gotta be my imagination. |
| 0x21b1d1 | 7 | Huh...? |
| 0x21b1d9 | 46 | I suddenly feel dizzy, and clutch at my head\n |
| 0x21b208 | 14 | instinctively. |
| 0x21b217 | 36 | Sir Haku... Is something the matter? |
| 0x21b23c | 23 | Uh, no... It's nothing. |
| 0x21b254 | 26 | What... the hell was that? |
| 0x21b26f | 48 | What's the holdup, love? C'mon, we're going to\n |
| 0x21b2a0 | 17 | leave you behind. |
| 0x21b2b2 | 18 | Be there in a sec. |
| 0x21b2c5 | 50 | Oh dear. It would seem we have reached a dead end. |
| 0x21b2f8 | 25 | It's completely caved in. |
| 0x21b312 | 41 | Then hath our investigation drawn to an\n |
| 0x21b33c | 15 | untimely close? |
| 0x21b34c | 48 | No. I think there has to be a place we haven't\n |
| 0x21b37d | 9 | gone yet. |
| 0x21b387 | 48 | But I don't recall anywhere else we could have\n |
| 0x21b3b8 | 21 | gone on the way here. |
| 0x21b3ce | 47 | I've found that these sorts of places tend to\n |
| 0x21b3fe | 45 | have hidden doors that appear to be a wall,\n |
| 0x21b42c | 21 | or something similar. |
| 0x21b442 | 50 | If you look carefully, you'll find small gaps in\n |
| 0x21b475 | 48 | the wall, or some kind of distinguishing mark... |
| 0x21b4a6 | 30 | Oh! Over there, dear sister!\n |
| 0x21b4c5 | 26 | There's a door over there! |
| 0x21b4e0 | 50 | We all look over to see some kind of door hidden\n |
| 0x21b513 | 36 | in the shadow of the collapsed wall. |
| 0x21b538 | 7 | Guh...! |
| 0x21b540 | 42 | Again... What's this strange feeling I'm\n |
| 0x21b56b | 11 | getting...? |
| 0x21b577 | 38 | Sir Haku... Is something the matter?\n |
| 0x21b59e | 18 | You seem unwell... |
| 0x21b5b1 | 21 | No worries. I'm fine. |
| 0x21b5c7 | 7 | Master. |
| 0x21b5cf | 32 | Master, could it be that you...? |
| 0x21b5f0 | 47 | What's going on...? Ever since I stepped into\n |
| 0x21b620 | 41 | this ruin, something's been bugging me... |
| 0x21b64a | 33 | It is no use. It will not open... |
| 0x21b66c | 45 | Is there any way we can attempt to force it\n |
| 0x21b69a | 5 | open? |
| 0x21b6a0 | 46 | You're out of your mind. A door this big and\n |
| 0x21b6cf | 8 | thick... |
| 0x21b6d8 | 33 | Here, lemme take a crack at it.\n |
| 0x21b6fa | 16 | Stand back, now. |
| 0x21b70b | 10 | Jachdwalt? |
| 0x21b716 | 9 | ...HRAH!! |
| 0x21b720 | 34 | There you go. Piece of cake, yeah? |
| 0x21b743 | 14 | Th-The door... |
| 0x21b752 | 14 | Hm, not bad... |
| 0x21b761 | 43 | I think this may be the first time you've\n |
| 0x21b78d | 33 | actually impressed me, Jachdwalt! |
| 0x21b7af | 20 | You serious, kid...? |
| 0x21b7c4 | 27 | It's open now, dear sister. |
| 0x21b7e0 | 25 | This is... It can't be... |
| 0x21b7fa | 12 | Dear sister? |
| 0x21b807 | 19 | Um... It's nothing. |
| 0x21b81b | 41 | Urgh... Dammit, what's happening to me?\n |
| 0x21b845 | 41 | Now my head's starting to hurt as well... |
| 0x21f786 | 9 | capsule01 |
| 0x21f791 | 15 | capsule00_hatch |
| 0x21f7a1 | 17 | capsule01_hatch_3 |
| 0x21f7b3 | 17 | capsule01_hatch_4 |
| 0x21f7c5 | 8 | light_06 |
| 0x21f7ce | 8 | light_00 |
| 0x21f7d7 | 8 | light_01 |
| 0x21f7e0 | 8 | light_02 |
| 0x21f7e9 | 8 | light_03 |
| 0x21f7f2 | 8 | light_04 |
| 0x21f7fb | 8 | light_05 |
| 0x21f804 | 8 | light_07 |
| 0x21f811 | 48 | It looks like something is lining the walls...\n |
| 0x21f842 | 36 | It's too dark for me to see, though. |
| 0x21f867 | 45 | Ah, allow me but a moment more, and I shall\n |
| 0x21f895 | 25 | duly light another torch. |
| 0x21f8af | 13 | ...Lights on. |
| 0x21f8bd | 7 | I say!? |
| 0x21f8ca | 12 | It lit up... |
| 0x21f8d7 | 25 | Wait, what did I just...? |
| 0x21f8f1 | 32 | Did you just do something, Haku? |
| 0x21f912 | 10 | Well, I... |
| 0x21f91d | 46 | The room seemed to light up at your command,\n |
| 0x21f94c | 5 | Haku. |
| 0x21f952 | 32 | That's just... pure coincidence. |
| 0x21f973 | 43 | I was just muttering something to myself,\n |
| 0x21f99f | 27 | and the lights turned on... |
| 0x21f9bb | 7 | Really? |
| 0x21f9c3 | 13 | Well... yeah. |
| 0x21f9d1 | 32 | Nekone, what exactly is this...? |
| 0x21f9f2 | 5 | Oh... |
| 0x21f9f8 | 40 | This... must be some sort of necropolis. |
| 0x21fa21 | 16 | A necropolis...? |
| 0x21fa32 | 43 | Yes, we have discovered others like this.\n |
| 0x21fa5e | 46 | We believe civilizations of old buried their\n |
| 0x21fa8d | 14 | dead this way. |
| 0x21fa9c | 41 | Which would make this place a cemetery,\n |
| 0x21fac6 | 11 | put simply. |
| 0x21fad2 | 8 | Ngh...!? |
| 0x21fadb | 37 | No... It's not just my imagination... |
| 0x21fb01 | 24 | I remember this place... |
| 0x21fb1a | 12 | ...It's not. |
| 0x21fb27 | 4 | Huh? |
| 0x21fb2c | 31 | This place... it's no cemetery. |
| 0x21fb4c | 43 | But, dear sister, all our findings agree.\n |
| 0x21fb78 | 42 | Every single one found contained ancient\n |
| 0x21fba3 | 10 | remains... |
| 0x21fbae | 37 | I know... I used to believe that too. |
| 0x21fbd4 | 6 | But... |
| 0x21fbdb | 24 | I... know this place...? |
| 0x21fbf4 | 27 | Wha--!? Everyone, get back! |
| 0x21fc10 | 10 | This is... |
| 0x21fc1b | 32 | ...exactly the same as before... |
| 0x21fc3c | 10 | Miss Kuon? |
| 0x21fc47 | 35 | Hm!? This... Everyone, take a look. |
| 0x21fc6b | 32 | What is the matter, dear sister? |
| 0x21fc8c | 26 | There's... someone inside. |
| 0x21fcad | 4 | Ah!? |
| 0x21fcb2 | 50 | My goodness. It almost looks as if this person's\n |
| 0x21fce5 | 12 | still alive. |
| 0x21fcf2 | 36 | Yes, but... Is this person frozen?\n |
| 0x21fd17 | 44 | I didn't expect to find something like this. |
| 0x21fd44 | 46 | This is beyond belief. There is not even the\n |
| 0x21fd73 | 32 | slightest sign of natural decay. |
| 0x21fd94 | 31 | Could this person really be...? |
| 0x21fdb4 | 24 | It's exactly the same... |
| 0x21fdcd | 36 | Then... that means this person is... |
| 0x21fdf2 | 19 | Haku, what's wrong? |
| 0x21fe06 | 8 | ...Haku? |
| 0x21fe0f | 12 | Wait! Haku-- |
| 0x21fe1c | 5 | Eek!? |
| 0x21fe22 | 19 | Rulutieh, get back! |
| 0x21fe36 | 26 | Oh, that's awfully cold... |
| 0x21fe51 | 8 | What...? |
| 0x21fe5a | 39 | ...Oh dear. Risen from the dead, is he? |
| 0x21fe82 | 40 | Impossible. I was certain he was dead... |
| 0x21feab | 11 | Ah... Ah... |
| 0x21fed6 | 15 | Ahhh... Ghhh... |
| 0x21fee6 | 8 | Hhhhh... |
| 0x21feef | 9 | Hhhhhh... |
| 0x21fef9 | 6 | Hey... |
| 0x21ff00 | 20 | Uh... Ah... Aghhh... |
| 0x21ff15 | 9 | You're... |
| 0x21ff1f | 31 | Ah... Ah... AaaaAUUuUUgghHH...! |
| 0x21ff3f | 7 | Wha--!? |
| 0x21ff47 | 8 | Eeeeeek! |
| 0x21ff50 | 36 | What in the--!? What IS that thing!? |
| 0x21ff75 | 26 | Wha... What's... What's... |
| 0x21ff90 | 7 | ...Huh? |
| 0x21ff98 | 27 | What just... Wh... What...? |
| 0x21ffb4 | 11 | A Tatari... |
| 0x21ffc0 | 7 | How...? |
| 0x21ffc8 | 19 | How did a Tatari... |
| 0x21ffdc | 31 | But then... what about Haku...? |
| 0x21fffc | 38 | Oh, come on! You gotta be shittin' me! |
| 0x220023 | 49 | What's going on!? What exactly is going on here!? |
| 0x220055 | 50 | I must admit, Haku... I certainly did not expect\n |
| 0x220088 | 23 | such... developments... |
| 0x2200a0 | 32 | Hee... hee hee hee hee hee...♪ |
| 0x2200c1 | 23 | Haku. What do we do...? |
| 0x2200d9 | 51 | Ah...! Everyone, group up. They'll swallow you up\n |
| 0x22010d | 21 | if you get separated! |
| 0x220123 | 47 | There's way too many... We need to get out of\n |
| 0x220153 | 45 | here! Trying to kill them is a waste of time! |
| 0x220181 | 43 | Kuon, back us up! We're gonna bust through! |
| 0x2201ad | 47 | Nekone, Rulutieh! Stay close! I'll use one of\n |
| 0x2201dd | 47 | my flash bombs to stun them! Move on my timing! |
| 0x22020d | 18 | Three, two, one... |
| 0x220220 | 9 | Now! Run! |
| 0x22022a | 34 | Dammit! They've blocked our way... |
| 0x22024d | 44 | They didn't look like they'd be this fast... |
| 0x22027a | 41 | And transforming from a person to THAT?\n |
| 0x2202a4 | 43 | These things are full of nasty surprises... |
| 0x2202d0 | 33 | Kuon, will your bomb work again!? |
| 0x2202f2 | 45 | It won't do any good. With the exit blocked\n |
| 0x220320 | 43 | like that, we'd be caught in the blast too. |
| 0x22034c | 30 | Hee hee... So, love, what now? |
| 0x22036b | 40 | Guess... we have no choice but to fight. |
| 0x220394 | 51 | We're out of options. We'll have to fight our way\n |
| 0x2203c8 | 46 | out. They can't die, so don't waste all your\n |
| 0x2203f7 | 7 | energy. |
| 0x2203ff | 48 | We need to find a way out and make a break for\n |
| 0x220430 | 10 | it, quick! |

## 8. Formato de saida EXIGIDO
Escreva `translations_21_03.json` com a forma:
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
