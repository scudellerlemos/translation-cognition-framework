# Cena ch_15_05 — pacote de traducao (301 linhas)

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
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `but...` -> `mas...` (Kuon, 12_16)
- `any more.` -> `assim.` (Ukon, 14_04)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Oh?` -> `Oh?` (Haku, 14_04)
- `stuff.` -> `isso.` (Haku, 14_04)
- `the inn.` -> `à pousada.` (Haku, 15_04)
- `it.` -> `aí.` (Haku, 15_03)
- `misunderstanding.` -> `mal-entendido.` (Haku, 12_11)
- `experience.` -> `sua vivencia.` (Ukon, 15_01)
- `That's...` -> `Isso...` (Haku, 15_01)
- `though.` -> `porém.` (Kuon, 12_04)
- `yourself.` -> `abalado.` (Kuon, 13_01)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `OK.` -> `OK.` (Haku, 15_04)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Yessir!` -> `Sim!` (Coorte de Ukon, 12_04)
- `really.` -> `de fato.` (Nekone, 15_03)
- `Ah...` -> `Ah...` (Haku, 13_01)
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
| 0xbb552 | 12 | Ahh... phew. |
| 0xbb55f | 46 | With a satisfied yawn, I shut the children's\n |
| 0xbb58e | 15 | book in my lap. |
| 0xbb59e | 37 | That's the last of the books Nekone\n |
| 0xbb5c4 | 14 | recommended... |
| 0xbb5d3 | 49 | She brought them at Kuon's request. They're all\n |
| 0xbb605 | 38 | like this--picture books for children. |
| 0xbb62c | 49 | It's not like I hate reading. Each one of these\n |
| 0xbb65e | 37 | tales and myths is engaging, but...\n |
| 0xbb684 | 16 | unsophisticated. |
| 0xbb695 | 47 | Since these books are meant for just learning\n |
| 0xbb6c5 | 45 | the letters, I guess that's to be expected,\n |
| 0xbb6f3 | 6 | but... |
| 0xbb6fa | 49 | At least I can read something like this without\n |
| 0xbb72c | 17 | any trouble, now. |
| 0xbb73e | 45 | I won't have to listen to that little twerp\n |
| 0xbb76c | 46 | asking why I can't read in that baffled tone\n |
| 0xbb79b | 9 | any more. |
| 0xbb7a5 | 45 | I wouldn't have figured before she asked me\n |
| 0xbb7d3 | 44 | that words without malice can hurt all the\n |
| 0xbb800 | 5 | same. |
| 0xbb806 | 22 | Yo, kid. Got a moment? |
| 0xbb81d | 28 | Ukon appears in the doorway. |
| 0xbb83a | 20 | ...Sorry to intrude. |
| 0xbb84f | 43 | Behind Ukon trails a boy of small, slight\n |
| 0xbb87b | 8 | stature. |
| 0xbb884 | 49 | Hello. I'm sorry for skipping out the other day\n |
| 0xbb8b6 | 39 | before we could be introduced properly. |
| 0xbb8de | 47 | Ah, this guy... Kiwru, I think? Nekone called\n |
| 0xbb90e | 27 | him Oshtor's sworn brother. |
| 0xbb92a | 46 | I've got a request from Lord Oshtor for you.\n |
| 0xbb959 | 40 | Something he's been meaning to bring up. |
| 0xbb982 | 6 | ...Uh? |
| 0xbb989 | 34 | What do you mean, "Lord Oshtor?"\n |
| 0xbb9ac | 35 | Why's the man himself referring t-- |
| 0xbb9d0 | 36 | Ukon's smirk cuts my thoughts short. |
| 0xbb9f5 | 44 | He... hasn't told Kiwru his true identity,\n |
| 0xbba22 | 7 | has he? |
| 0xbba2a | 51 | Kiwru fidgets, looking puzzled and uncomfortable.\n |
| 0xbba5e | 43 | He doesn't seem to know why he's even here. |
| 0xbba8a | 42 | Good grief. He really doesn't have a clue. |
| 0xbbab5 | 51 | As Oshtor, he's the definition of straight-laced.\n |
| 0xbbae9 | 34 | So why is his Ukon identity so...? |
| 0xbbb0c | 45 | This might be a little fun. Let's keep going. |
| 0xbbb3a | 19 | I grin back at him. |
| 0xbbb4e | 38 | So, this is the message for you from\n |
| 0xbbb75 | 12 | Lord Oshtor. |
| 0xbbb82 | 48 | He says this kid's gonna be doing work for you\n |
| 0xbbbb3 | 37 | so he can get some proper experience. |
| 0xbbbd9 | 5 | Huh!? |
| 0xbbbdf | 42 | Oh, so we're taking him on as a colleague. |
| 0xbbc0a | 47 | That's right. Comes from the big man himself,\n |
| 0xbbc3a | 45 | so do what you please with him. Put the kid\n |
| 0xbbc68 | 8 | to work. |
| 0xbbc71 | 44 | W-Wait, I haven't heard anything about that! |
| 0xbbc9e | 45 | Of course you haven't. I didn't bring it up\n |
| 0xbbccc | 14 | 'til just now. |
| 0xbbcdb | 14 | It can't be... |
| 0xbbcea | 47 | Well, let me finish, here. You'll change your\n |
| 0xbbd1a | 38 | tune if you listen through to the end. |
| 0xbbd41 | 7 | Urgh... |
| 0xbbd49 | 46 | Surprised, Kiwru hesitantly begins to stand,\n |
| 0xbbd78 | 40 | but sits back down at Ukon's placations. |
| 0xbbda1 | 47 | This is all Oshtor's plan to begin with, so I\n |
| 0xbbdd1 | 46 | don't mind, but... is this kid gonna be able\n |
| 0xbbe00 | 11 | to keep up? |
| 0xbbe0c | 47 | The way Lord Oshtor tells it, he's never once\n |
| 0xbbe3c | 49 | missed a session of his military arts training.\n |
| 0xbbe6e | 10 | He's good. |
| 0xbbe79 | 3 | Oh? |
| 0xbbe7d | 42 | I wouldn't have guessed it by his gentle\n |
| 0xbbea8 | 48 | appearance, but if he has Ukon's vote, there's\n |
| 0xbbed9 | 11 | no mistake. |
| 0xbbee5 | 48 | I'll be glad for some more male company around\n |
| 0xbbf16 | 43 | here, honestly. He doesn't seem unpleasant. |
| 0xbbf42 | 47 | Word from our Missy's that you want to keep a\n |
| 0xbbf72 | 47 | small, exceptional pool of talent on call for\n |
| 0xbbfa2 | 6 | stuff. |
| 0xbbfa9 | 26 | Yeah, something like that. |
| 0xbbfc4 | 47 | Not that I had any choice in the matter, what\n |
| 0xbbff4 | 47 | with Kuon blowing all our money on paying for\n |
| 0xbc024 | 8 | the inn. |
| 0xbc02d | 43 | If that's the case, then look no further.\n |
| 0xbc059 | 49 | I figured you could use a guy with some chops--\n |
| 0xbc08b | 11 | here he is. |
| 0xbc097 | 28 | Hold on, um... Ukon, was it? |
| 0xbc0b4 | 45 | You said you were... an agent of my honored\n |
| 0xbc0e2 | 29 | brother. Is that really true? |
| 0xbc100 | 48 | You appeared uninvited, brought me here, roped\n |
| 0xbc131 | 48 | me into this--and he never mentioned a word of\n |
| 0xbc162 | 3 | it. |
| 0xbc166 | 45 | I'd hoped to become my brother's assistant,\n |
| 0xbc194 | 41 | like Nekone. There must be some kind of\n |
| 0xbc1be | 19 | misunderstanding... |
| 0xbc1d2 | 48 | O-Or else you're deciding these things on your\n |
| 0xbc203 | 19 | own, which I doubt. |
| 0xbc217 | 34 | Ah, well, about that. It's not a\n |
| 0xbc23a | 17 | misunderstanding. |
| 0xbc24c | 48 | This guy and I, we're under direct orders from\n |
| 0xbc27d | 47 | Oshtor, and this is how he wants things to go\n |
| 0xbc2ad | 5 | down. |
| 0xbc2b3 | 43 | He said no matter how hard he tries, he's\n |
| 0xbc2df | 46 | always too lenient on his nearest relations... |
| 0xbc30e | 48 | And that becoming a full-fledged warrior means\n |
| 0xbc33f | 45 | overcoming hardships and gaining real-world\n |
| 0xbc36d | 11 | experience. |
| 0xbc37d | 47 | But if you insist, I can have a talk with him\n |
| 0xbc3ad | 43 | and see about putting you somewhere else,\n |
| 0xbc3d9 | 6 | maybe? |
| 0xbc3e0 | 9 | That's... |
| 0xbc3ea | 43 | I definitely... want to be a full-fledged\n |
| 0xbc416 | 45 | warrior, but... if I do this, I won't... be\n |
| 0xbc444 | 14 | with Nekone... |
| 0xbc453 | 47 | And now he's started to fret with his head in\n |
| 0xbc483 | 44 | his hands. Easy to see the inner conflict,\n |
| 0xbc4b0 | 7 | though. |
| 0xbc4b8 | 45 | But if he believes someone he just met this\n |
| 0xbc4e6 | 42 | easily... Maybe we've gotta work on that\n |
| 0xbc511 | 8 | naivete. |
| 0xbc51a | 11 | We're back! |
| 0xbc526 | 17 | We have returned. |
| 0xbc538 | 49 | While Kiwru holds his head in conflicted agony,\n |
| 0xbc56a | 48 | Kuon and Nekone return from their shopping trip. |
| 0xbc59b | 9 | N-Nekone! |
| 0xbc5a5 | 45 | Oh, hello. What are you doing here? With my\n |
| 0xbc5d3 | 24 | dear brother, no less... |
| 0xbc5ec | 42 | Why? I was brought here all of a sudden,\n |
| 0xbc617 | 12 | and this--\n |
| 0xbc624 | 16 | ...Dear brother? |
| 0xbc635 | 11 | Ah, cripes. |
| 0xbc641 | 45 | Kiwru looks between Nekone and Ukon several\n |
| 0xbc66f | 6 | times. |
| 0xbc676 | 46 | Huh? But that's--you--um? I... bwuh? What do\n |
| 0xbc6a5 | 25 | you mean, "dear brother"? |
| 0xbc6bf | 41 | I don't think I could ever get bored of\n |
| 0xbc6e9 | 45 | watching his facial expressions change that\n |
| 0xbc717 | 8 | rapidly. |
| 0xbc720 | 27 | Dear brother, what is this? |
| 0xbc73c | 48 | C'mon, don't call him "this." He's a respected\n |
| 0xbc76d | 30 | prince back home in Ennakamuy. |
| 0xbc78c | 46 | I've told you this before. It's cruel not to\n |
| 0xbc7bb | 34 | treat him with the proper respect. |
| 0xbc7de | 43 | ...Not that you're being rude or anything\n |
| 0xbc80a | 9 | yourself. |
| 0xbc814 | 41 | I-I-I... Are you really... my honorable\n |
| 0xbc83e | 11 | brother...? |
| 0xbc84a | 48 | Ah... Bahahaha! Yeah, I guess the cat's out of\n |
| 0xbc87b | 48 | the bag, huh. It's me, all right. Oshtor! Your\n |
| 0xbc8ac | 8 | brother. |
| 0xbc8b5 | 18 | Hey. What's wrong? |
| 0xbc8c8 | 45 | I might remind you, brother, that Kiwru has\n |
| 0xbc8f6 | 41 | all the strength of heart of a sparrow.\n |
| 0xbc920 | 16 | Hold your jests. |
| 0xbc931 | 45 | I... see. So that's why you're dressed like\n |
| 0xbc95f | 5 | that. |
| 0xbc965 | 45 | Yeah. It's just a disguise to escape public\n |
| 0xbc993 | 7 | notice. |
| 0xbc99b | 41 | But... Y-Your personality is completely\n |
| 0xbc9c5 | 17 | different, too... |
| 0xbc9d7 | 48 | What are you saying? It wouldn't be a disguise\n |
| 0xbca08 | 28 | if it were totally the same. |
| 0xbca25 | 22 | That's... true, but... |
| 0xbca3c | 22 | Getting disillusioned? |
| 0xbca53 | 23 | Huh? N-No, not at all-- |
| 0xbca6b | 20 | I was disillusioned. |
| 0xbca80 | 10 | N-Nekone!? |
| 0xbca8b | 50 | The day I first arrived in the imperial capital,\n |
| 0xbcabe | 44 | I thought to rush immediately to my brother. |
| 0xbcaeb | 49 | Upon finding him, I was greeted by the sight of\n |
| 0xbcb1d | 47 | my dear sibling drunk and dancing naked among\n |
| 0xbcb4d | 10 | other men. |
| 0xbcb58 | 48 | The disillusionment I felt then will stay with\n |
| 0xbcb89 | 27 | me for the rest of my life. |
| 0xbcba5 | 6 | Huh... |
| 0xbcbac | 46 | Ahahaha! We'd all had a little bit to drink,\n |
| 0xbcbdb | 11 | I'll admit. |
| 0xbcbe7 | 47 | I can see the life draining from Kiwru's eyes\n |
| 0xbcc17 | 37 | as he stares off into space vacantly. |
| 0xbcc3d | 45 | Mm, I think it's just about time. Rulutieh,\n |
| 0xbcc6b | 35 | Nekone. Help me get some tea ready. |
| 0xbcc8f | 3 | OK. |
| 0xbcc93 | 17 | Yes, dear sister. |
| 0xbcca5 | 47 | Oh... P-Please, do not trouble yourself with... |
| 0xbccd5 | 44 | Don't worry about all that. I'm making tea\n |
| 0xbcd02 | 43 | because I want to, so you shouldn't be so\n |
| 0xbcd2e | 7 | modest. |
| 0xbcd36 | 49 | We just bought some delicious-looking teacakes!\n |
| 0xbcd68 | 36 | Help yourself to those, if you like. |
| 0xbcd8d | 43 | Sister, should we use... this tea, perhaps? |
| 0xbcdb9 | 50 | Mhm. We have guests, so we should go all-out and\n |
| 0xbcdec | 21 | use the best we have. |
| 0xbce02 | 49 | Besides, it's not like we can use it when there\n |
| 0xbce34 | 32 | isn't a special occasion for it. |
| 0xbce55 | 49 | Nekone smiles as Kuon speaks--as though spurred\n |
| 0xbce87 | 16 | on by her words. |
| 0xbce98 | 44 | That Nekone. She was reluctant when I sent\n |
| 0xbcec5 | 45 | her out here, y'know, but now she's totally\n |
| 0xbcef3 | 9 | attached. |
| 0xbcefd | 47 | Makes a guy feel a little lonely, to be honest. |
| 0xbcf2d | 48 | I think she'll come back to you again when you\n |
| 0xbcf5e | 45 | stop dressing like that and go back to your\n |
| 0xbcf8c | 9 | old self. |
| 0xbcf96 | 34 | ...I'm just glad she's doing well. |
| 0xbcfb9 | 44 | You really prefer this appearance over the\n |
| 0xbcfe6 | 21 | other one, don't you? |
| 0xbcffc | 47 | H-Huh? By any chance... Does Nekone work with\n |
| 0xbd02c | 19 | this group as well? |
| 0xbd040 | 48 | Yeah, Uk--I mean Osh--geez, this is confusing.\n |
| 0xbd071 | 46 | Basically, he sent her to keep us from being\n |
| 0xbd0a0 | 12 | shorthanded. |
| 0xbd0ad | 44 | She runs her mouth and she's a little imp,\n |
| 0xbd0da | 48 | but she's a competent imp, which makes it even\n |
| 0xbd10b | 6 | worse. |
| 0xbd112 | 14 | What was that? |
| 0xbd121 | 48 | He's talking about how I sent you to work with\n |
| 0xbd152 | 8 | the kid. |
| 0xbd15b | 15 | Oh, about that. |
| 0xbd16b | 49 | I asked him what we would do if something awful\n |
| 0xbd19d | 25 | befell me, and he said... |
| 0xbd1b7 | 49 | ...it was better than attracting some sleazebag\n |
| 0xbd1e9 | 43 | off the street. I feel rather like a live\n |
| 0xbd215 | 10 | sacrifice. |
| 0xbd220 | 12 | Huh? H-Huh!? |
| 0xbd22d | 34 | Oh, stop saying stuff like that.\n |
| 0xbd250 | 31 | I haven't laid a finger on you. |
| 0xbd270 | 8 | For now. |
| 0xbd279 | 41 | ...Is he getting that vacant stare again? |
| 0xbd2a3 | 46 | Incidentally, why are you and Kiwru even here? |
| 0xbd2d2 | 43 | Ah, well. I was gonna have Kiwru help out\n |
| 0xbd2fe | 46 | around here, but he doesn't seem too keen on\n |
| 0xbd32d | 4 | Huh? |
| 0xbd332 | 44 | If he doesn't want to, I guess it can't be\n |
| 0xbd35f | 45 | helped. I can put him back in my office and-- |
| 0xbd38d | 25 | I'll do it, I'll do it!\n |
| 0xbd3a7 | 21 | I'll do my best here! |
| 0xbd3bd | 44 | Oh? I'm grateful to hear you say that, but\n |
| 0xbd3ea | 35 | don't force yourself on my account. |
| 0xbd40e | 44 | No, it's fine! I can do it! I'll do my best! |
| 0xbd43b | 48 | Y-Yeesh, all right. If you insist so much, I'm\n |
| 0xbd46c | 45 | hardly complaining. It'd be a big help to me. |
| 0xbd49a | 24 | I'll be countin' on you. |
| 0xbd4b3 | 7 | Yessir! |
| 0xbd4bb | 47 | He'll be under our supervision, then... We're\n |
| 0xbd4eb | 45 | still shorthanded, but this is definitely a\n |
| 0xbd519 | 5 | step. |
| 0xbd51f | 49 | Then we'll be comrades from now on, seems like.\n |
| 0xbd551 | 35 | I look forward to working with you. |
| 0xbd575 | 12 | Yes, me too! |
| 0xbd582 | 49 | Kiwru's joining up with us, hm? It's a pleasure\n |
| 0xbd5b4 | 23 | to be working with you. |
| 0xbd5cc | 45 | Yes, it's a pleasure to be working with you\n |
| 0xbd5fa | 10 | as well... |
| 0xbd605 | 32 | I see. Kiwru is to be one of us. |
| 0xbd626 | 47 | I-I look forward to working with you, Nekone.\n |
| 0xbd656 | 22 | And you too, Rulutieh! |
| 0xbd66d | 39 | I-I look forward to working with you... |
| 0xbd695 | 14 | And I as well. |
| 0xbd6a4 | 6 | O--OK! |
| 0xbd6ab | 46 | I already kinda had it figured out, but man,\n |
| 0xbd6da | 45 | he responded to her way differently than he\n |
| 0xbd708 | 10 | did to me. |
| 0xbd713 | 50 | If that's all settled, then, let's dispense with\n |
| 0xbd746 | 43 | the serious topics. The tea's getting cold. |
| 0xbd772 | 36 | Here, Lord Kiwru. You have some too. |
| 0xbd797 | 45 | Thank you. And please--you don't have to be\n |
| 0xbd7c5 | 10 | so formal. |
| 0xbd7d0 | 44 | My standing and titles don't mean anything\n |
| 0xbd7fd | 24 | here. I'm just a novice. |
| 0xbd816 | 46 | You make for a natural underling either way,\n |
| 0xbd845 | 7 | really. |
| 0xbd84d | 15 | Aha... ahaha... |
| 0xbd85d | 46 | Do try not to cause trouble for anyone while\n |
| 0xbd88c | 13 | you are here. |
| 0xbd89a | 31 | Does Nekone just... hate me...? |
| 0xbd8ba | 44 | Kiwru's face falls as he mutters to himself. |
| 0xbd8e7 | 44 | Don't worry about it. She's like that with\n |
| 0xbd914 | 10 | everybody. |
| 0xbd91f | 29 | Nekone, do you have a moment? |
| 0xbd93d | 24 | What is it, dear sister? |
| 0xbd956 | 48 | Your hair's coming undone. Hold still so I can\n |
| 0xbd987 | 21 | fix it up, all right? |
| 0xbd99d | 5 | Ah... |
| 0xbd9a3 | 23 | I'll help, Miss Kuon... |
| 0xbd9bb | 31 | OK, you do that side, Rulutieh. |
| 0xbd9db | 50 | Your beautiful hair, all disheveled like this...\n |
| 0xbda0e | 35 | The wind must have pulled it loose. |
| 0xbda32 | 38 | Well, the wind was strong today, so... |
| 0xbda59 | 48 | Between them, Kuon and Rulutieh untie Nekone's\n |
| 0xbda8a | 40 | hair and carefully begin to comb it out. |
| 0xbdab3 | 50 | Nekone squints, then seems to relax comfortably,\n |
| 0xbdae6 | 29 | yielding to their attentions. |
| 0xbdb04 | 38 | ...I've never seen Nekone like that... |
| 0xbdb2b | 33 | It's an exception. Doesn't count. |
| 0xbdb4d | 47 | She treats a lot of people the way she treats\n |
| 0xbdb7d | 47 | you. I don't think she specifically hates you\n |
| 0xbdbad | 12 | or anything. |
| 0xbdbba | 36 | Yeah, you're the same as the rest.\n |
| 0xbdbdf | 29 | Don't worry about it so much. |
| 0xbdbfd | 14 | Ahaha... ha... |
| 0xbdc0c | 44 | That's odd. This is supposed to be a sweet\n |
| 0xbdc39 | 33 | snack, but it tastes... salty...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_05.json` com a forma:
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
