# Cena ch_15_09 — pacote de traducao (105 linhas)

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
| Cocopo | Criatura | Cocopo | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |

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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
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
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `...Kuon?` -> `...Kuon?` (Haku, 11_11)
- `U-Um...` -> `E-Ei...` (Rulutieh, 14_09)
- `but...` -> `mas...` (Kuon, 12_16)
- `Ack--` -> `Ack--` (Haku, 13_03)
- `Uh...` -> `Ahn...` (Haku, 14_03)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `The end.` -> `Fim.` (Haku, 15_02)
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
- Moznu: `Ha! Well done, Nosuri. A right impressive show,\n` -> `Ha! Bom trabalho, Nosuri. Foi uma boa encenação,\n`
- Moznu: `this.` -> `essa.`
- Moznu: `Heh heh. Now, ain't this one a beauty? Lookers\n` -> `Heh heh. Ora, essa aqui é uma beldade. Cara\n`
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
| 0xc497f | 50 | We handily defeat Moznu's gang, but sure enough,\n |
| 0xc49b2 | 43 | they retreat into the urban jungle of the\n |
| 0xc49de | 10 | capital... |
| 0xc49e9 | 46 | Before long, however, we manage to track the\n |
| 0xc4a18 | 43 | stubborn bandit down and corner him in an\n |
| 0xc4a44 | 9 | alleyway. |
| 0xc4a4e | 48 | Sorry for the cliched line, but I'm gonna need\n |
| 0xc4a7f | 26 | you to come along quietly. |
| 0xc4a9a | 43 | Damn it! Like I'm gonna get caught by you\n |
| 0xc4ac6 | 6 | punks! |
| 0xc4acd | 10 | Ah, wait-- |
| 0xc4ad8 | 24 | Like hell! See ya later! |
| 0xc4af1 | 45 | Do you really think you can get away from us? |
| 0xc4b1f | 41 | We try to give chase, but Moznu quickly\n |
| 0xc4b49 | 25 | disappears into the dark. |
| 0xc4b63 | 23 | Tch, he's getting awa-- |
| 0xc4b7b | 12 | Blurghaaah!! |
| 0xc4b88 | 47 | From the shadow of the alley, a thick, sticky\n |
| 0xc4bb8 | 28 | sound splashes unsettlingly. |
| 0xc4bd5 | 26 | Bwuh--guh--gah! Bluh--Wh-- |
| 0xc4bf0 | 44 | I shine a light on the ground ahead of me,\n |
| 0xc4c1d | 42 | where the sound seems to be coming from... |
| 0xc4c48 | 34 | Whargbl--hurgh, s-someone help m-- |
| 0xc4c6b | 45 | There I laid eyes on the struggling form of\n |
| 0xc4c99 | 40 | Moznu, who had fallen into a pit of mud. |
| 0xc4cc2 | 25 | Or... No, that isn't mud. |
| 0xc4cdc | 12 | Ah, that's-- |
| 0xc4ce9 | 24 | ...A cesspool, isn't it. |
| 0xc4d02 | 45 | Come to think of it, I guess this area IS a\n |
| 0xc4d30 | 23 | waste collection point. |
| 0xc4d48 | 7 | Urgh... |
| 0xc4d50 | 49 | Kuon and Nekone grimace in unison, leaning back\n |
| 0xc4d82 | 15 | from the stink. |
| 0xc4d92 | 46 | We have to take him to Oshtor, but this is a\n |
| 0xc4dc1 | 6 | bit... |
| 0xc4dc8 | 11 | Hey, Kuon-- |
| 0xc4dd4 | 47 | I look to the side to consult Kuon on what to\n |
| 0xc4e04 | 35 | do, but when I do, no one is there. |
| 0xc4e28 | 8 | ...Kuon? |
| 0xc4e31 | 46 | Welp! We're going to report to Oshtor, Haku.\n |
| 0xc4e60 | 26 | The rest is in your hands. |
| 0xc4e7b | 45 | Kuon, Nekone, and Rulutieh then ride off on\n |
| 0xc4ea9 | 37 | Cocopo's back without a further word. |
| 0xc4ecf | 7 | U-Um... |
| 0xc4ed7 | 37 | Yep. We need to let him know quickly. |
| 0xc4efd | 6 | But... |
| 0xc4f04 | 44 | Soldiers value speed. We should make haste\n |
| 0xc4f31 | 22 | and be away from here. |
| 0xc4f48 | 16 | B-But Sir Haku-- |
| 0xc4f5d | 31 | W-Well, I'll... be going, then. |
| 0xc4f7d | 25 | Just where are you going? |
| 0xc4f97 | 6 | *Grab* |
| 0xc4f9e | 7 | Ack--\n |
| 0xc4fa6 | 12 | L-Let me go! |
| 0xc4fb3 | 48 | Ah hm hm. Not so easily. It's come to this, so\n |
| 0xc4fe4 | 44 | you're going to share in this terrible fate. |
| 0xc5011 | 41 | H-Haku, you're scaring me. Your FACE is\n |
| 0xc503b | 11 | scaring me. |
| 0xc5047 | 46 | N-Never mind that! Just hurry up and pull me\n |
| 0xc5076 | 16 | outta this mess! |
| 0xc5087 | 43 | Go on, Kiwru. The poor man is begging for\n |
| 0xc50b3 | 10 | your help. |
| 0xc50be | 47 | I don't want to do it, either. You do it, Haku. |
| 0xc50ee | 32 | Tch. I guess I have no choice.\n |
| 0xc510f | 16 | Here, hold this. |
| 0xc5120 | 45 | I grab a nearby branch of fairly reasonable\n |
| 0xc514e | 45 | thickness, holding it out for Moznu to grab\n |
| 0xc517c | 5 | onto. |
| 0xc5182 | 39 | Haaaa. Haaaahhhh. You're a lifesaver... |
| 0xc51aa | 42 | Gah, he's heavy. Kiwru, help me out, here. |
| 0xc51d5 | 12 | A-All right. |
| 0xc51e2 | 46 | I don't know if it's because his clothes are\n |
| 0xc5211 | 39 | soaking up the liquid, but this guy's\n |
| 0xc5239 | 19 | unbelievably heavy. |
| 0xc524d | 14 | ...It snapped. |
| 0xc525c | 5 | Uh... |
| 0xc5262 | 5 | Ah... |
| 0xc5268 | 6 | Bweh-- |
| 0xc526f | 42 | And now he's sinking face-first into the\n |
| 0xc529a | 7 | pool... |
| 0xc52a2 | 46 | Well! All in a day's work. Let's head on back. |
| 0xc52d1 | 45 | What are you saying? W-We need to save him!\n |
| 0xc52ff | 8 | Quickly! |
| 0xc5308 | 48 | Eh, they'll forgive us, even if we abandon him\n |
| 0xc5339 | 12 | to his fate. |
| 0xc5346 | 46 | I really understand how you feel, but that's\n |
| 0xc5375 | 32 | no reason to--Ack, he's sinking! |
| 0xc5396 | 44 | Finally, the guards round up Moznu and his\n |
| 0xc53c3 | 43 | gang, though they aren't terribly pleased\n |
| 0xc53ef | 16 | with the stench. |
| 0xc5400 | 48 | The bandits allow themselves to be quietly led\n |
| 0xc5431 | 47 | away, seemingly broken of their defiant spirit. |
| 0xc5461 | 48 | ...And Kiwru continues to stare a hole into my\n |
| 0xc5492 | 46 | head. Hey, at least we got him out safely in\n |
| 0xc54c1 | 8 | the end. |
| 0xc54ca | 49 | Be proud of how much he appreciated what we did\n |
| 0xc54fc | 8 | for him! |
| 0xc5505 | 45 | He appreciated it so much, he wept and even\n |
| 0xc5533 | 13 | embraced you. |
| 0xc5541 | 48 | ...Ah, well. This case is closed, at any rate.\n |
| 0xc5572 | 30 | All's shitty that ends shitty. |
| 0xc5591 | 50 | ...It sounds like you're saying something really\n |
| 0xc55c4 | 45 | good and pithy, but this isn't good at all... |
| 0xc55f2 | 46 | C'mon, don't say that with those teary eyes.\n |
| 0xc5621 | 44 | You're making me feel like the bad guy here. |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_09.json` com a forma:
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
