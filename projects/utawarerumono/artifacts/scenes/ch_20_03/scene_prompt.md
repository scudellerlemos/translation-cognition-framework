# Cena ch_20_03 — pacote de traducao (448 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nakwan | Termo | Nakwan | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Woman | UI | Mulher | traduzir | none |
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
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `country.` -> `país.` (Haku, 17_01)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `like this.` -> `dessas.` (Kuon, 11_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Really?` -> `Mesmo?` (Kuon, 14_03)
- `dear sister.` -> `querida irmã.` (Nekone, 14_10)
- `Miss Kuon...` -> `Senhora Kuon...` (Rulutieh, 13_05)
- `them.` -> `deles.` (Kuon, 11_05)
- `mountains.` -> `remotas.` (Kuon, 11_02)
- `anything else.` -> `nada mais.` (Haku, 18_01)
- `Whoa.` -> `Nossa.` (Haku, 14_01)
- `usual.` -> `costumeiro.` (Haku, 19_08)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `R-Right...` -> `C-Certo...` (Haku, 11_09)
- `What do you mean?` -> `O que você quer dizer?` (Haku, 13_01)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `herself.` -> `ela mesma.` (Haku, 15_02)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `But...` -> `mas...` (Kuon, 11_01)
- `Yes.` -> `Sim.` (Haku, 17_01)
- `Atuy...` -> `Atuy...` (Atuy, 16_02)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `What?` -> `Que?` (Haku, 12_02)
- `...*Nod*` -> `...*Acena*` (Garota, 19_08)
- `Yes, dear sister.` -> `Sim, querida irmã.` (Nekone, 15_05)
- `another.` -> `outra.` (Rulutieh, 17_01)
- `them on.` -> `colocá-los.` (Haku, 16_01)
- `Haku.` -> `Haku.` (Kuon, 12_08)
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
| 0x1b51a3 | 14 | *Yawn*... Mmf. |
| 0x1b51b2 | 47 | I try to suppress the large yawn, but it will\n |
| 0x1b51e2 | 14 | not be denied. |
| 0x1b51f1 | 30 | Hmhm. That was quite the yawn. |
| 0x1b5210 | 38 | Yeah, guess I'm still a little sleepy. |
| 0x1b5237 | 48 | I glance up. Little by little, the eastern sky\n |
| 0x1b5268 | 20 | is getting brighter. |
| 0x1b527d | 43 | Usually I'd be snoring in bed at this hour. |
| 0x1b52a9 | 47 | This isn't the first time I've gone with Kuon\n |
| 0x1b52d9 | 49 | to morning market, but I could still use a nap... |
| 0x1b530b | 5 | Haku? |
| 0x1b5311 | 3 | Mm? |
| 0x1b5315 | 18 | Thanks for coming. |
| 0x1b5328 | 20 | ...Sure, no problem. |
| 0x1b533d | 45 | I hear a lot of shouting around the area...\n |
| 0x1b536b | 42 | Merchants trying to get the attention of\n |
| 0x1b5396 | 20 | potential customers. |
| 0x1b53ab | 47 | I peer around. I'm actually kind of impressed\n |
| 0x1b53db | 48 | by how many people are so functional this early. |
| 0x1b540c | 43 | ...Seems more lively than usual today, huh? |
| 0x1b5438 | 46 | Kuon gives a small nod in response, glancing\n |
| 0x1b5467 | 15 | around herself. |
| 0x1b5477 | 49 | You're right. There's rumors that there's going\n |
| 0x1b54a9 | 32 | to be a war... Maybe that's why? |
| 0x1b54ca | 6 | A war? |
| 0x1b54d1 | 47 | I heard that Uzurusha in the west is invading\n |
| 0x1b5501 | 43 | Yamato. They've already taken a bordering\n |
| 0x1b552d | 8 | country. |
| 0x1b5536 | 48 | Yamato must be gathering their troops to fight\n |
| 0x1b5567 | 17 | off the invaders. |
| 0x1b5579 | 49 | What!? That's the first I've heard of it. Isn't\n |
| 0x1b55ab | 49 | it pretty bad if they already took someone else\n |
| 0x1b55dd | 5 | down? |
| 0x1b55e3 | 47 | Then again, I don't see a single worried face\n |
| 0x1b5613 | 9 | out here. |
| 0x1b561d | 48 | In fact, there's almost a sense of excitement.\n |
| 0x1b564e | 40 | Like there's going to be a festival or\n |
| 0x1b5677 | 10 | something. |
| 0x1b5682 | 44 | I imagine that not a single citizen thinks\n |
| 0x1b56af | 44 | there's a chance Yamato could lose this war. |
| 0x1b56dc | 43 | Kuon probably guessed my question from my\n |
| 0x1b5708 | 29 | expression. She continues on. |
| 0x1b5726 | 48 | It just goes to show how much faith the people\n |
| 0x1b5757 | 35 | of this country have in the Mikado. |
| 0x1b577b | 28 | Faith in the Mikado, huh...? |
| 0x1b5798 | 99 | The unified country of Yamato, made up of smaller\n provinces. And the owlo that rules over them... |
| 0x1b57fc | 45 | That old geezer's... No, never mind. Didn't\n |
| 0x1b582a | 34 | see anything, don't KNOW anything. |
| 0x1b584d | 51 | That should do it. We've gotten everything on the\n |
| 0x1b5881 | 30 | list, so we can head home now. |
| 0x1b58a0 | 49 | We need to get this to Rulutieh before everyone\n |
| 0x1b58d2 | 36 | wakes up, or breakfast will be late. |
| 0x1b58f7 | 14 | Right you are. |
| 0x1b5906 | 15 | Ohhh... Hmmm... |
| 0x1b5916 | 48 | What to do? I can't just ignore a direct order\n |
| 0x1b5947 | 12 | from Papa... |
| 0x1b5954 | 51 | And it DOES sound like a bash... but I definitely\n |
| 0x1b5988 | 43 | don't want all those sweaty boys with me... |
| 0x1b59b4 | 49 | After we finish breakfast, Atuy sits there with\n |
| 0x1b59e6 | 41 | a letter in hand, looking deeply pensive. |
| 0x1b5a10 | 25 | Atuy? Is something wrong? |
| 0x1b5a2a | 48 | It's pretty rare to see you so deep in thought\n |
| 0x1b5a5b | 10 | like this. |
| 0x1b5a66 | 46 | Well, I got a letter from Papa today, and...\n |
| 0x1b5a95 | 29 | oh, it's a touch complicated. |
| 0x1b5ab3 | 45 | Is it something serious? You don't look too\n |
| 0x1b5ae1 | 29 | happy about whatever it says. |
| 0x1b5aff | 18 | Well, you see--Oh! |
| 0x1b5b12 | 49 | Just as Atuy is about to explain, she claps her\n |
| 0x1b5b44 | 43 | hands together, as if inspiration's struck. |
| 0x1b5b70 | 42 | I know. Are you two busy at all right now? |
| 0x1b5b9b | 3 | Hm? |
| 0x1b5b9f | 47 | No. There aren't any pressing matters we need\n |
| 0x1b5bcf | 26 | to take care of right now. |
| 0x1b5bea | 7 | Really? |
| 0x1b5bf2 | 47 | Well there's nothing urgent, but that doesn't\n |
| 0x1b5c22 | 29 | mean we're completely free... |
| 0x1b5c40 | 44 | Well, in that case, could you come with me\n |
| 0x1b5c6d | 44 | for a bit? There's somewhere I'd like to go. |
| 0x1b5c9a | 25 | Atuy smiles cheerfully... |
| 0x1b5cb4 | 43 | Hah! What a shame for you, Kuon. It seems\n |
| 0x1b5ce0 | 16 | victory is mine. |
| 0x1b5cf1 | 21 | We'll see about that. |
| 0x1b5d07 | 47 | Well, I hope for your sake you don't cry when\n |
| 0x1b5d37 | 15 | you lose! Hyah! |
| 0x1b5d47 | 48 | Five, huh... One, two, three... Now, take this\n |
| 0x1b5d78 | 47 | piece... or move two more to take the other...? |
| 0x1b5da8 | 22 | ...I'll take this one! |
| 0x1b5dbf | 47 | So sorry, but that was a mistake. The trap is\n |
| 0x1b5def | 44 | sprung. What you really should've watched \n |
| 0x1b5e1c | 16 | out for is this! |
| 0x1b5e2d | 15 | Im... possible! |
| 0x1b5e3d | 25 | All right... my turn now. |
| 0x1b5e57 | 47 | Five and three, that makes eight... So I take\n |
| 0x1b5e87 | 21 | this piece at four... |
| 0x1b5e9d | 9 | Grrrrr... |
| 0x1b5ea7 | 48 | And I think that's game. You lose double points. |
| 0x1b5ed8 | 46 | W-Wait! M-My hand slipped back there! What I\n |
| 0x1b5f07 | 29 | really wanted was THAT piece! |
| 0x1b5f25 | 41 | A good woman would never go back on her\n |
| 0x1b5f4f | 16 | word, I'd think? |
| 0x1b5f60 | 47 | Arrrgh! How!? How could I have lost like this!? |
| 0x1b5f90 | 41 | So many wins in a row. Most impressive,\n |
| 0x1b5fba | 12 | dear sister. |
| 0x1b5fc7 | 51 | I didn't know you were so skilled in these games,\n |
| 0x1b5ffb | 12 | Miss Kuon... |
| 0x1b6008 | 47 | My mothers were all fond of games like these.\n |
| 0x1b6038 | 47 | I just naturally got better from playing with\n |
| 0x1b6068 | 5 | them. |
| 0x1b606e | 49 | ...Hmhmhm. I would expect no less from a worthy\n |
| 0x1b60a0 | 44 | rival like yourself. It's no fun without a\n |
| 0x1b60cd | 10 | challenge. |
| 0x1b60d8 | 46 | But now... you have awakened the BEAST WITHIN. |
| 0x1b6107 | 46 | Looks like it's time I show you what happens\n |
| 0x1b6136 | 21 | when I get serious... |
| 0x1b614c | 9 | O... K... |
| 0x1b6156 | 44 | I hear the girls happily chatting behind me. |
| 0x1b6183 | 44 | Sounds like they're having fun back there... |
| 0x1b61b0 | 50 | With reins in hand, keeping an eye on the steeds\n |
| 0x1b61e3 | 42 | moving us forward, I let out a small sigh. |
| 0x1b620e | 46 | We're in the mountains north of the imperial\n |
| 0x1b623d | 48 | capital. A dense forest covers the mountainside. |
| 0x1b626e | 45 | In the carriage behind us, Ougi, Kiwru, and\n |
| 0x1b629c | 20 | Cocopo follow along. |
| 0x1b62b1 | 47 | And where the hell did they get this carriage\n |
| 0x1b62e1 | 8 | from...? |
| 0x1b62ea | 48 | The carriage Kuon turned up with had all kinds\n |
| 0x1b631b | 45 | of travel supplies. We're fine, even in the\n |
| 0x1b6349 | 10 | mountains. |
| 0x1b6354 | 47 | Not only did it have enough food and clothes,\n |
| 0x1b6384 | 45 | it included beds, and even a simple cooking\n |
| 0x1b63b2 | 6 | stove. |
| 0x1b63b9 | 46 | It also had all the amenities for bathing...\n |
| 0x1b63e8 | 46 | It seems designed for long-term traveling in\n |
| 0x1b6417 | 8 | comfort. |
| 0x1b6420 | 44 | Even had a couple games packed in for road\n |
| 0x1b644d | 22 | entertainment. Swanky. |
| 0x1b6464 | 38 | That's all fine. It's all fine, but... |
| 0x1b648b | 49 | ...We've clearly been traveling for longer than\n |
| 0x1b64bd | 37 | "a bit." It's been quite a while now. |
| 0x1b64e3 | 44 | That's right... It's been about three days\n |
| 0x1b6510 | 17 | since we set out. |
| 0x1b6522 | 43 | This is becoming more of a road trip than\n |
| 0x1b654e | 14 | anything else. |
| 0x1b655d | 41 | I think we might be pretty close to the\n |
| 0x1b6587 | 21 | country's border now. |
| 0x1b659d | 38 | Danger. Evasive maneuvers recommended. |
| 0x1b65c4 | 47 | Master, there appears to be a large tree root\n |
| 0x1b65f4 | 42 | protruding from the ground in front of us. |
| 0x1b661f | 5 | Whoa. |
| 0x1b6625 | 45 | I quickly shift the reins, guiding our path\n |
| 0x1b6653 | 12 | around them. |
| 0x1b6660 | 16 | Thanks, you two. |
| 0x1b6671 | 45 | I glance both right and left to acknowledge\n |
| 0x1b669f | 18 | each of the twins. |
| 0x1b66b2 | 44 | The two of them aren't joining in with the\n |
| 0x1b66df | 43 | others' games, and they sit next to me as\n |
| 0x1b670b | 6 | usual. |
| 0x1b6712 | 47 | Aren't you guys going to play a couple rounds\n |
| 0x1b6742 | 10 | with them? |
| 0x1b674d | 48 | The two of them shake their heads instantly at\n |
| 0x1b677e | 38 | my question; no deliberation required. |
| 0x1b67a5 | 25 | We stay with you, Master. |
| 0x1b67bf | 43 | The only place we belong is at your side,\n |
| 0x1b67eb | 7 | Master. |
| 0x1b67f3 | 48 | O-OK, I get it. But could you two quit leaning\n |
| 0x1b6824 | 6 | on me? |
| 0x1b682b | 44 | All that warmth and softness is getting...\n |
| 0x1b6858 | 14 | distracting... |
| 0x1b6867 | 16 | Hey there, love! |
| 0x1b6878 | 5 | Gah!? |
| 0x1b687e | 40 | And now Atuy's jumped on me from behind. |
| 0x1b68a7 | 22 | Get off. You're heavy. |
| 0x1b68be | 50 | Hee hee, you shouldn't ever joke about something\n |
| 0x1b68f1 | 32 | like that to a girl, you know... |
| 0x1b6912 | 11 | *Badump*... |
| 0x1b691e | 44 | I don't know why, but Atuy's smile sends a\n |
| 0x1b694b | 21 | shiver down my spine. |
| 0x1b6961 | 27 | Y-Yeah, guess you're right. |
| 0x1b697d | 48 | I'm glad you understand. If you actually meant\n |
| 0x1b69ae | 49 | it, well, I might have to start a teensy little\n |
| 0x1b69e0 | 4 | war. |
| 0x1b69e5 | 10 | R-Right... |
| 0x1b69f0 | 46 | Hmm, we should be pretty close now... 'Scuse\n |
| 0x1b6a1f | 9 | me, love. |
| 0x1b6a29 | 48 | Atuy leans forward on me to get a look around.\n |
| 0x1b6a5a | 44 | And, of course, pressing on the back of my\n |
| 0x1b6a87 | 7 | head... |
| 0x1b6a8f | 14 | What are you-- |
| 0x1b6a9e | 41 | Hmmm, still might be a little ways off... |
| 0x1b6ac8 | 49 | Hey, Atuy. Do you mind telling me where exactly\n |
| 0x1b6afa | 12 | we're going? |
| 0x1b6b07 | 17 | What do you mean? |
| 0x1b6b19 | 49 | Don't play dumb with me. This has gone way past\n |
| 0x1b6b4b | 28 | "coming with you for a bit." |
| 0x1b6b68 | 48 | I thought you just wanted a little sightseeing\n |
| 0x1b6b99 | 43 | trip, but we've gone way too far out now.\n |
| 0x1b6bc5 | 24 | Where are we even going? |
| 0x1b6bde | 47 | Oh, you needn't worry. I already got Oshtor's\n |
| 0x1b6c0e | 26 | permission and everything! |
| 0x1b6c29 | 19 | What? What do you-- |
| 0x1b6c3d | 28 | ...Oh! I think I see it now. |
| 0x1b6c5a | 33 | I wonder where Atuy is taking us. |
| 0x1b6c7c | 48 | We're quite far from the capital. And all this\n |
| 0x1b6cad | 43 | ominous talk of war coming... I wonder if\n |
| 0x1b6cd9 | 10 | it's safe. |
| 0x1b6ce4 | 46 | I'm certain there is little cause for worry.\n |
| 0x1b6d13 | 47 | Our compatriots certainly seem cheerful enough. |
| 0x1b6d43 | 50 | Ougi gestures towards the carriage in front with\n |
| 0x1b6d76 | 15 | a placid smile. |
| 0x1b6d86 | 45 | Through the window of the car, they can see\n |
| 0x1b6db4 | 24 | the girls playing games. |
| 0x1b6dcd | 46 | They've switched from sugoroku to shogi, but\n |
| 0x1b6dfc | 42 | they still look to be having fun together. |
| 0x1b6e27 | 23 | That would be... check. |
| 0x1b6e3f | 41 | What!? N-No, what I MEANT to do was this! |
| 0x1b6e69 | 44 | As you please. Then I will take your hisha\n |
| 0x1b6e96 | 8 | instead. |
| 0x1b6e9f | 7 | Wha--!? |
| 0x1b6ea7 | 49 | I am glad indeed to see my dear sister enjoying\n |
| 0x1b6ed9 | 8 | herself. |
| 0x1b6ee2 | 48 | A life with more subordinates than friends has\n |
| 0x1b6f13 | 49 | left her quite lonely. I much prefer to see her\n |
| 0x1b6f45 | 9 | smile so. |
| 0x1b6f4f | 48 | It would appear that the others' circumstances\n |
| 0x1b6f80 | 46 | are not dissimilar... Birds of a feather, as\n |
| 0x1b6faf | 9 | they say. |
| 0x1b6fb9 | 51 | Ougi. Why do I get the feeling you're insulting--\n |
| 0x1b6fed | 4 | Huh? |
| 0x1b6ff2 | 39 | A shadow falls over Kiwru's expression. |
| 0x1b701a | 17 | Ougi, is that...? |
| 0x1b702c | 23 | Yes. Without a doubt... |
| 0x1b7044 | 47 | We finally get out of the forest, and proceed\n |
| 0x1b7074 | 19 | into an open field. |
| 0x1b7088 | 9 | *Whistle* |
| 0x1b7092 | 11 | Whoa there. |
| 0x1b709e | 7 | ...Huh? |
| 0x1b70a6 | 32 | I'm not sure what just happened. |
| 0x1b70c7 | 42 | I thought I saw something fly towards me\n |
| 0x1b70f2 | 12 | really fast. |
| 0x1b70ff | 50 | Then Atuy's hand appeared, and... I see an arrow\n |
| 0x1b7132 | 50 | caught between her fingers, still vibrating with\n |
| 0x1b7165 | 6 | force. |
| 0x1b716c | 47 | Ahahaha! Looks like they've started without us. |
| 0x1b719c | 45 | I finally realize. A stray arrow had almost\n |
| 0x1b71ca | 45 | pierced my head, and Atuy somehow caught it\n |
| 0x1b71f8 | 8 | in time. |
| 0x1b7201 | 23 | Wh-Wh... What in the... |
| 0x1b7219 | 46 | My near-death reaction finally kicks in, and\n |
| 0x1b7248 | 36 | a cold sweat breaks out all over me. |
| 0x1b726d | 46 | We can hear yelling in the distance, and the\n |
| 0x1b729c | 38 | sound of metal clashing against metal. |
| 0x1b72c3 | 45 | The infrequent crackling of a fire, and the\n |
| 0x1b72f1 | 21 | scent of burnt flesh. |
| 0x1b7307 | 19 | Well, well, well... |
| 0x1b731b | 21 | ..."Dear Grandfather, |
| 0x1b7331 | 42 | The moment I was free from the forest...\n |
| 0x1b735c | 42 | I suddenly found myself on a battlefield." |
| 0x1b7387 | 49 | What the hell is going on here!? What is this!?\n |
| 0x1b73b9 | 47 | What the hell IS this!? Where the hell are we!? |
| 0x1b73e9 | 50 | Oh, it's just as it looks, love. A lovely little\n |
| 0x1b741c | 11 | playground. |
| 0x1b7428 | 21 | A playground!? This!? |
| 0x1b743e | 28 | Don't you play dumb with me! |
| 0x1b745b | 50 | I heard there was a war going on at the borders,\n |
| 0x1b748e | 6 | but... |
| 0x1b7495 | 45 | Anyways, let's get out of here before we're\n |
| 0x1b74c3 | 28 | caught in even more trouble. |
| 0x1b74e0 | 4 | Why? |
| 0x1b74e5 | 27 | What do you mean, "why?"... |
| 0x1b7501 | 44 | We came all the way here to have some fun!\n |
| 0x1b752e | 47 | It'd be a bit of a waste if we turn around now. |
| 0x1b755e | 48 | For this...? Wait... Did you know that the war\n |
| 0x1b758f | 18 | was going on here? |
| 0x1b75a2 | 50 | More than that. I came to join the war in Papa's\n |
| 0x1b75d5 | 45 | stead. He's too busy to come himself, so he\n |
| 0x1b7603 | 9 | asked me. |
| 0x1b760d | 29 | Wait a minute. That letter... |
| 0x1b762b | 44 | I was rather looking forward to it, but he\n |
| 0x1b7658 | 44 | demanded I take some of his men along. And\n |
| 0x1b7685 | 25 | they're a bit too sweaty. |
| 0x1b769f | 51 | Just imagine it. A glistening mob of muscle-bound\n |
| 0x1b76d3 | 48 | lunks chasing after me yelling "Milady, milady!" |
| 0x1b7704 | 49 | That all sounds a bit nasty to me, so I decided\n |
| 0x1b7736 | 47 | to invite you loves along for some fun instead. |
| 0x1b7766 | 13 | Fun? This...? |
| 0x1b7774 | 45 | I asked Oshtor, and he said he didn't mind.\n |
| 0x1b77a2 | 44 | He said if I'm having a party, then go wild! |
| 0x1b77cf | 45 | Party!? He just wanted us to be his advance\n |
| 0x1b77fd | 6 | party! |
| 0x1b7804 | 45 | Look, to you this may be all fun and games,\n |
| 0x1b7832 | 16 | but this is war. |
| 0x1b7843 | 43 | You shouldn't be dragging us all into this. |
| 0x1b786f | 15 | I... shouldn't? |
| 0x1b787f | 50 | Of course you aren't! You can't be dragging your\n |
| 0x1b78b2 | 46 | friends onto a battlefield. That's ridiculous. |
| 0x1b78e1 | 42 | But... I just wanted to have fun... with\n |
| 0x1b790c | 12 | everybody... |
| 0x1b791d | 47 | Oh, I guess we've arrived. Things look pretty\n |
| 0x1b794d | 17 | hectic out there. |
| 0x1b795f | 46 | Just as my dear brother was saying, it seems\n |
| 0x1b798e | 29 | the war has indeed escalated. |
| 0x1b79ac | 5 | Whuh? |
| 0x1b79b2 | 38 | Nosuri, Ougi, can I ask you for some\n |
| 0x1b79d9 | 44 | reconnaissance? I'd like to know where the\n |
| 0x1b7a06 | 18 | enemy's stationed. |
| 0x1b7a19 | 49 | Leave it to us. And let me remind you: I demand\n |
| 0x1b7a4b | 21 | a rematch after this! |
| 0x1b7a61 | 47 | Rulutieh, Nekone, I want you two to scope out\n |
| 0x1b7a91 | 48 | the area. We need to get a feel for the terrain. |
| 0x1b7ac2 | 4 | Yes. |
| 0x1b7ac7 | 29 | Understood. Let's go, Cocopo. |
| 0x1b7afc | 42 | How are they acting so calmly...? Wait a\n |
| 0x1b7b27 | 36 | minute. Did they know about this...? |
| 0x1b7b4c | 47 | H-Hey, Kuon. Was all this... an inconvenience\n |
| 0x1b7b7c | 8 | for you? |
| 0x1b7b85 | 45 | Should I have... not invited my friends here? |
| 0x1b7bb3 | 7 | Atuy... |
| 0x1b7bbb | 44 | I don't think that's true. I've never been\n |
| 0x1b7be8 | 44 | invited out by a friend like this. It made\n |
| 0x1b7c15 | 9 | me happy. |
| 0x1b7c1f | 7 | Kuon... |
| 0x1b7c27 | 45 | Kuon, you don't seem too fazed by all this.\n |
| 0x1b7c55 | 23 | Did you know all along? |
| 0x1b7c6d | 5 | What? |
| 0x1b7c73 | 49 | Wait, Haku, are you telling me you DIDN'T know?\n |
| 0x1b7ca5 | 38 | I thought you knew from the beginning. |
| 0x1b7ccc | 42 | How was I supposed to know this from the\n |
| 0x1b7cf7 | 10 | beginning? |
| 0x1b7d02 | 48 | Well, it was pretty apparent what her father's\n |
| 0x1b7d33 | 22 | letter would be about. |
| 0x1b7d4a | 47 | Atuy is royalty, so it makes sense that she'd\n |
| 0x1b7d7a | 48 | represent her father and lead soldiers against\n |
| 0x1b7dab | 13 | the invasion. |
| 0x1b7db9 | 43 | My dear brother has also departed for the\n |
| 0x1b7de5 | 28 | battlefield with his troops. |
| 0x1b7e02 | 42 | Wait, did you two know about this as well? |
| 0x1b7e2d | 8 | ...*Nod* |
| 0x1b7e36 | 11 | Oh... OK... |
| 0x1b7e42 | 31 | Did Nosuri know about this too? |
| 0x1b7e62 | 48 | Indubitably. We were the ones who gathered the\n |
| 0x1b7e93 | 22 | supplies for the trip. |
| 0x1b7eaa | 23 | Yes, I was aware of it. |
| 0x1b7ec2 | 20 | What about Rulutieh? |
| 0x1b7ed7 | 14 | Um... I was... |
| 0x1b7ee6 | 49 | Rulutieh's also royalty. I imagine she's in the\n |
| 0x1b7f18 | 47 | same position as Atuy. She also knew from the\n |
| 0x1b7f48 | 6 | start. |
| 0x1b7f4f | 16 | Um, I'm sorry... |
| 0x1b7f60 | 47 | What about you, Kiwru? You knew about this too? |
| 0x1b7f90 | 46 | U-Um... O-Of course I knew about it! What do\n |
| 0x1b7fbf | 16 | you take me for? |
| 0x1b7fd0 | 49 | Dammit, so I was the only one out of the loop...? |
| 0x1b8002 | 31 | Argh, my stomach... It hurts... |
| 0x1b8022 | 20 | Hm...? This sound... |
| 0x1b8037 | 10 | What's up? |
| 0x1b8042 | 40 | The scent on the wind... It's changed.\n |
| 0x1b806b | 28 | Something's coming, I think. |
| 0x1b8088 | 30 | Where? I don't see anything... |
| 0x1b80a7 | 41 | Um... I believe it might be over there... |
| 0x1b80d1 | 49 | I can see birds flying away... I feel there may\n |
| 0x1b8103 | 34 | be a group of people over there... |
| 0x1b8126 | 48 | Now that she mentions it, I hear a lot of bird\n |
| 0x1b8157 | 24 | cries from the forest... |
| 0x1b8170 | 49 | But I can't really tell where it's coming from.\n |
| 0x1b81a2 | 20 | It's all indistinct. |
| 0x1b81b7 | 35 | It's coming from over there. Ougi-- |
| 0x1b81db | 17 | Yes, dear sister. |
| 0x1b81ed | 51 | Nosuri hands her luggage to Ougi and darts to the\n |
| 0x1b8221 | 47 | closest tree, nimbly leaping onto its branches. |
| 0x1b8251 | 51 | Hm... I see them. Over there. It definitely looks\n |
| 0x1b8285 | 42 | as though there's a group heading our way. |
| 0x1b82b0 | 43 | I still don't know which direction you're\n |
| 0x1b82dc | 16 | talking about... |
| 0x1b82ed | 48 | It's hard to tell through all the trees... But\n |
| 0x1b831e | 48 | they don't look like Yamatan soldiers' uniforms. |
| 0x1b834f | 43 | Wait--there's something strange about them. |
| 0x1b837b | 43 | They seem to be split up into two groups.\n |
| 0x1b83a7 | 43 | It looks like they're... arguing with one\n |
| 0x1b83d3 | 8 | another. |
| 0x1b83dc | 35 | Are they fighting among themselves? |
| 0x1b8400 | 32 | ...No, it doesn't seem that way. |
| 0x1b8421 | 50 | One group has injured people that are struggling\n |
| 0x1b8454 | 47 | to keep going, and the other group is forcing\n |
| 0x1b8484 | 8 | them on. |
| 0x1b848d | 49 | It doesn't look as though the two groups are on\n |
| 0x1b84bf | 16 | equal footing... |
| 0x1b84d0 | 46 | Nosuri, can you tell us more about the group\n |
| 0x1b84ff | 17 | with the injured? |
| 0x1b8511 | 48 | Let's see... By their clothing, they look more\n |
| 0x1b8542 | 48 | like citizens of Yamato than Uzurushan military. |
| 0x1b8573 | 47 | They don't seem to be wearing armor, but they\n |
| 0x1b85a3 | 20 | are holding weapons. |
| 0x1b85b8 | 48 | Then... that group may be those who were taken\n |
| 0x1b85e9 | 26 | captive by the Uzurushans. |
| 0x1b8604 | 46 | I have heard that the Uzurushans force their\n |
| 0x1b8633 | 48 | hostages to become nakwans, and fight in their\n |
| 0x1b8664 | 5 | wars. |
| 0x1b866a | 8 | Nakwans? |
| 0x1b8673 | 45 | Expendable slave soldiers, forced to fight.\n |
| 0x1b86a1 | 43 | Their families are taken hostage, and the\n |
| 0x1b86cd | 37 | army uses them as expendable pawns... |
| 0x1b86f3 | 46 | ...I've heard the same. They kill stragglers\n |
| 0x1b8722 | 47 | without hesitation. They just treat them like\n |
| 0x1b8752 | 6 | tools. |
| 0x1b8759 | 18 | That's so cruel... |
| 0x1b876c | 34 | Can you tell where they're headed? |
| 0x1b878f | 46 | They're not moving fast, but they look to be\n |
| 0x1b87be | 40 | heading towards the valley over there... |
| 0x1b87e7 | 18 | Isn't that where-- |
| 0x1b87fa | 44 | Yes, the Yamato encampment is located there. |
| 0x1b8827 | 46 | So they went all the way around to attempt a\n |
| 0x1b8856 | 18 | surprise attack... |
| 0x1b8869 | 23 | ...Who ARE these girls? |
| 0x1b8881 | 51 | Not only was that perfect reconnaissance, they've\n |
| 0x1b88b5 | 41 | predicted the enemy's movements, as well. |
| 0x1b88df | 50 | I see. Well, why don't we have a little fun with\n |
| 0x1b8912 | 10 | them then? |
| 0x1b891d | 44 | Right. We should give them a proper welcome. |
| 0x1b894a | 46 | Ahaha! I knew you and I would be on the same\n |
| 0x1b8979 | 11 | page, Kuon. |
| 0x1b8985 | 49 | Nekone, do you think you can predict which path\n |
| 0x1b89b7 | 13 | they'll take? |
| 0x1b89c5 | 42 | I believe so. It may take some time, but\n |
| 0x1b89f0 | 26 | I should be able to do it. |
| 0x1b8a0b | 31 | Rulutieh, if this is too much-- |
| 0x1b8a2b | 48 | Oh... I'll be fine... So would you allow me...\n |
| 0x1b8a5c | 20 | to accompany you...? |
| 0x1b8a71 | 48 | ...Mhm, of course. I'm sure Haku will be happy\n |
| 0x1b8aa2 | 38 | to be your shield if anything happens. |
| 0x1b8ac9 | 25 | Are you ready, Cocopo...? |
| 0x1b8af7 | 46 | Wait, why are you all itching for a fight so\n |
| 0x1b8b26 | 5 | much? |
| 0x1b8b2c | 35 | You guys are... kinda scaring me... |
| 0x1b8b50 | 44 | Well. It would seem they are all acting in\n |
| 0x1b8b7d | 22 | perfect synchronicity. |
| 0x1b8b94 | 47 | Indeed, I'm surprised you were able to gather\n |
| 0x1b8bc4 | 38 | a team of so many skilled individuals. |
| 0x1b8beb | 51 | I'm beginning to understand why Oshtor prizes you\n |
| 0x1b8c1f | 10 | so highly. |
| 0x1b8c2a | 36 | Er, I didn't really gather them...\n |
| 0x1b8c4f | 43 | They kinda just gathered up on their own... |
| 0x1b8c7b | 50 | I look around the group once more. They all seem\n |
| 0x1b8cae | 37 | pretty bloodthirsty--uh, hot-blooded. |
| 0x1b8cd4 | 34 | ...So we're really going to fight? |
| 0x1b8cf7 | 50 | I'm counting on you to think up a good strategy,\n |
| 0x1b8d2a | 5 | Haku. |
| 0x1b8d30 | 36 | Could you listen to me? For once...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_03.json` com a forma:
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
