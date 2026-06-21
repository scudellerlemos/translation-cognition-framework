# Cena ch_23_16 — pacote de traducao (143 linhas)

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
| Benawi | Personagem | Benawi | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Saraana | Personagem | Saraana | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `us.` -> `nós.` (Haku, 15_03)
- `Bro...` -> `Irmão...` (Haku, 20_22)
- `others...` -> `outros...` (Kuon, 18_01)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `like.` -> `tipo.` (Rulutieh, 18_01)
- `you.` -> `isso.` (Nekone, 15_03)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `like this.` -> `dessas.` (Kuon, 11_01)
- `...Haku.` -> `...Haku.` (Haku, 22_05)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `Bwuh!?` -> `Ué!?` (Haku, 16_01)
- `approaching.` -> `aproximando.` (Haku, 19_08)
- `Boss!` -> `Chefe!` (Kuon, 20_21)
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
| 0x2bc43a | 46 | Our path back to Yamato is a short and quick\n |
| 0x2bc469 | 4 | one. |
| 0x2bc46e | 49 | This time, we don't have to avoid being seen by\n |
| 0x2bc4a0 | 47 | the enemy or take winding, circuitous routes... |
| 0x2bc4d0 | 49 | Instead, we push straight down the main road to\n |
| 0x2bc502 | 46 | where the ships are moored, making quick time. |
| 0x2bc531 | 47 | Not even once do the soldiers of Tuskur harry\n |
| 0x2bc561 | 3 | us. |
| 0x2bc565 | 47 | Munechika's news, Benawi's ominous words, and\n |
| 0x2bc595 | 48 | the withdrawal of the Tuskur army all weigh on\n |
| 0x2bc5c6 | 10 | my mind... |
| 0x2bc5d1 | 48 | They have to be connected. It's safe to assume\n |
| 0x2bc602 | 35 | Tuskur knows of the Mikado's death. |
| 0x2bc626 | 6 | Bro... |
| 0x2bc62d | 23 | Are you really dead...? |
| 0x2bc645 | 43 | It just isn't hitting me like it's reality. |
| 0x2bc671 | 46 | He told me there was still so much he had to\n |
| 0x2bc6a0 | 5 | do... |
| 0x2bc6a6 | 46 | ...and I doubt the princess is ready to take\n |
| 0x2bc6d5 | 20 | the throne just yet. |
| 0x2bc6ea | 47 | There's just no way he'd up and die like this\n |
| 0x2bc71a | 14 | for no reason. |
| 0x2bc729 | 46 | Gah. Obsessing about it isn't going to do me\n |
| 0x2bc758 | 9 | any good. |
| 0x2bc762 | 46 | I need to get back to Yamato as soon as I can. |
| 0x2bc791 | 46 | The bay where the ships are anchored is just\n |
| 0x2bc7c0 | 23 | a little further off... |
| 0x2bc7d8 | 48 | Someone mentioned that we can make it to shore\n |
| 0x2bc809 | 47 | by sunrise if we push onward through the night. |
| 0x2bc839 | 49 | Still, we might be safe from enemy attacks, but\n |
| 0x2bc86b | 49 | wild predators hunting by night are a very real\n |
| 0x2bc89d | 7 | threat. |
| 0x2bc8a5 | 50 | We decide to set up camp on a riverbank close to\n |
| 0x2bc8d8 | 35 | the road and spend the night there. |
| 0x2bc8fc | 34 | Dinner is an uncomplicated affair. |
| 0x2bc91f | 50 | We all surround the campfire and eat in silence,\n |
| 0x2bc952 | 47 | chewing on smoked meat we'd brought as rations. |
| 0x2bc982 | 14 | No one speaks. |
| 0x2bc991 | 46 | I can't remember the last time I had a quiet\n |
| 0x2bc9c0 | 43 | meal like this since meeting Kuon and the\n |
| 0x2bc9ec | 9 | others... |
| 0x2bc9f6 | 48 | I guess it goes to show how heavy a shadow the\n |
| 0x2bca27 | 24 | Mikado's death has cast. |
| 0x2bca40 | 47 | As soon as dinner is done, we decide on watch\n |
| 0x2bca70 | 47 | order as usual and everyone beds down for the\n |
| 0x2bcaa0 | 6 | night. |
| 0x2bcaa7 | 32 | Kuon and I have the first watch. |
| 0x2bcac8 | 47 | A sinking feeling grips my stomach as I stare\n |
| 0x2bcaf8 | 16 | into the fire... |
| 0x2bcb09 | 33 | This is going to be a long night. |
| 0x2bcb2b | 50 | My thoughts turn to Munechika. I'm worried about\n |
| 0x2bcb5e | 30 | her, staying behind like that. |
| 0x2bcb7d | 46 | Undoubtedly, she would've liked nothing more\n |
| 0x2bcbac | 42 | than to be on the first boat back to the\n |
| 0x2bcbd7 | 9 | mainland. |
| 0x2bcbe5 | 45 | It's hard to get my thoughts in order. As I\n |
| 0x2bcc13 | 48 | throw another log on the fire, Kuon breaks the\n |
| 0x2bcc44 | 8 | silence. |
| 0x2bcc4d | 38 | I wasn't expecting this, to be honest. |
| 0x2bcc74 | 15 | Expecting what? |
| 0x2bcc84 | 45 | How much of an effect the Mikado's death is\n |
| 0x2bccb2 | 7 | having. |
| 0x2bccba | 46 | I guess you can't really help it. I mean, to\n |
| 0x2bcce9 | 35 | the Yamatan people, he's their god. |
| 0x2bcd0d | 45 | Hearing that the center of your religion is\n |
| 0x2bcd3b | 49 | dead and gone... I can only imagine what that's\n |
| 0x2bcd6d | 5 | like. |
| 0x2bcd73 | 34 | Oh... No, that's not what I meant. |
| 0x2bcd96 | 11 | What, then? |
| 0x2bcda2 | 46 | I was talking about how badly it's affecting\n |
| 0x2bcdd1 | 4 | YOU. |
| 0x2bcdd6 | 6 | ...Me? |
| 0x2bcddd | 40 | I... I guess it has been weighing on me. |
| 0x2bce06 | 5 | Haku? |
| 0x2bce0c | 44 | I'm just... thinking about what's going to\n |
| 0x2bce39 | 43 | happen next. Anything goes, now. Makes me\n |
| 0x2bce65 | 7 | uneasy. |
| 0x2bce6d | 12 | Hm... I see. |
| 0x2bce7a | 49 | I'm guessing the capital's in an uproar by this\n |
| 0x2bceac | 6 | point. |
| 0x2bceb3 | 14 | I'd assume so. |
| 0x2bcec2 | 46 | I wonder how Oshtor and Mikazuchi are doing... |
| 0x2bcef1 | 40 | And how are Honoka and Anju taking this? |
| 0x2bcf1a | 48 | Urgh. I can't let my thoughts go into a spiral\n |
| 0x2bcf4b | 10 | like this. |
| 0x2bcf56 | 8 | ...Haku. |
| 0x2bcf5f | 41 | Kuon's kind voice cuts right through my\n |
| 0x2bcf89 | 18 | swirling thoughts. |
| 0x2bcf9c | 47 | I'm sure Anju will be fine. She has Oshtor to\n |
| 0x2bcfcc | 15 | look after her. |
| 0x2bcfdc | 11 | I guess so. |
| 0x2bcfe8 | 44 | But it's not just about my brother and the\n |
| 0x2bd015 | 47 | princess. Something else is eating at me, and\n |
| 0x2bd045 | 10 | I can't... |
| 0x2bd050 | 6 | ...Hm? |
| 0x2bd057 | 43 | What is... There's an odd scent in the air. |
| 0x2bd083 | 7 | Master. |
| 0x2bd08b | 6 | Bwuh!? |
| 0x2bd092 | 43 | I look over my shoulder to find the twins\n |
| 0x2bd0be | 35 | standing behind me in the darkness. |
| 0x2bd0e2 | 27 | Don't scare me like that... |
| 0x2bd0fe | 12 | Approaching. |
| 0x2bd10b | 47 | Something... coarse? Something is drawing near. |
| 0x2bd13b | 7 | Coarse? |
| 0x2bd147 | 34 | Kuon glares out into the darkness. |
| 0x2bd16a | 27 | Something's here. An enemy! |
| 0x2bd186 | 34 | Uruuru, Saraana, wake everyone up! |
| 0x2bd1a9 | 5 | Boss! |
| 0x2bd1af | 19 | Where's the enemy!? |
| 0x2bd1c3 | 47 | The others leap from their tents with weapons\n |
| 0x2bd1f3 | 10 | in hand... |
| 0x2bd1fe | 44 | Nosuri's eyes are the first to adjust. She\n |
| 0x2bd22b | 30 | squints out into the darkness. |
| 0x2bd24a | 39 | This isn't good. We've been surrounded! |
| 0x2bd272 | 45 | As she speaks, multiple figures materialize\n |
| 0x2bd2a0 | 17 | from the shadows. |
| 0x2bd2b2 | 22 | Who the hell are they? |
| 0x2bd2c9 | 24 | Are they bandits, or...? |
| 0x2bd2e2 | 44 | No, that can't be it. They don't seem like\n |
| 0x2bd30f | 14 | petty thieves. |
| 0x2bd31e | 50 | I get a knot in my stomach just looking at them.\n |
| 0x2bd351 | 44 | They seem like something much more sinister. |
| 0x2bd37e | 21 | These guys can't be-- |
| 0x2bd394 | 25 | You know them, Jachdwalt? |
| 0x2bd3ae | 20 | Uzurushan assassins. |
| 0x2bd3c3 | 13 | Assassins...? |
| 0x2bd3d1 | 8 | Shadows. |
| 0x2bd3da | 34 | Ooh, that sounds like a good time. |
| 0x2bd3fd | 38 | "Good" ain't the word I'd use, lady.\n |
| 0x2bd424 | 43 | We can't afford to take these guys lightly. |
| 0x2bd450 | 44 | And something's... off. Usually, they stay\n |
| 0x2bd47d | 46 | hidden. Strollin' up so brazenly isn't their\n |
| 0x2bd4ac | 13 | style at all. |
| 0x2bd4ba | 43 | It's almost like I'm lookin' at a pack of\n |
| 0x2bd4e6 | 44 | starving beasts more than trained killers... |
| 0x2bd513 | 42 | Yeah, this is definitely strange. Tuskur\n |
| 0x2bd53e | 40 | attackers I'd understand, but Uzurushan? |
| 0x2bd567 | 50 | Quite a distance across the ocean, too. Were one\n |
| 0x2bd59a | 46 | of the Pillars their target, I'd understand,\n |
| 0x2bd5c9 | 10 | but us...? |
| 0x2bd5d4 | 46 | We should talk about it later, I think. They\n |
| 0x2bd603 | 33 | don't look like the patient sort. |
| 0x2bd625 | 30 | Yeah. On your guard, everyone! |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_16.json` com a forma:
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
