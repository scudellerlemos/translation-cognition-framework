# Cena ch_18_05 — pacote de traducao (163 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Divine Scion | Titulo | Descendente Divino | traduzir | moderate |
| Girl | UI | Garota | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Woman | UI | Mulher | traduzir | none |
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `him.` -> `dele.` (Nekone, 15_02)
- `Wh-What...?` -> `Q-Que...?` (Nekone, 14_04)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Oshtor...` -> `Oshtor...` (Haku, 18_01)
- `you...?` -> `você...?` (Kuon, 14_09)
- `Wh-What are you talking about?` -> `O-O que você quer dizer?` (Rulutieh, 18_02)
- `a bit.` -> `um bit.` (Haku, 13_01)
- `Head` -> `Head` (rotulo, 11_03)
- `S-Stop! Desist! I-I'll apologize, so--` -> `P-Para! Desista! Eu me p-peço desculpas, então--` (Anju, 18_01)
- `unison.` -> `em uníssono.` (SISTEMA, 18_01)
- `RightFoot` -> `RightFoot` (system, 13_06)
- `LeftFoot` -> `LeftFoot` (system, 13_06)
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
| 0x16be66 | 33 | Urk... This... this isn't good... |
| 0x16be88 | 37 | Satisfied? Come on. We're going back. |
| 0x16beae | 46 | No, no, NO! I will stay here until my Oshtor\n |
| 0x16bedd | 13 | comes for me! |
| 0x16beeb | 45 | You little brat. I told you, Oshtor doesn't\n |
| 0x16bf19 | 31 | know a thing about any of this. |
| 0x16bf39 | 44 | He'll come! Oshtor will come! He'll save me! |
| 0x16bf66 | 9 | *Sigh*... |
| 0x16bf70 | 47 | I know how she feels. That princess really is\n |
| 0x16bfa0 | 30 | just a girl head-over-heels... |
| 0x16bfbf | 48 | This entire affair is becoming a tiresome farce. |
| 0x16bff0 | 45 | ...Something has been bothering me for some\n |
| 0x16c01e | 45 | time, now. This Oshtor you keep mentioning... |
| 0x16c04c | 27 | I have returned, my sister. |
| 0x16c068 | 33 | You're late, Ougi. What kept you? |
| 0x16c08a | 48 | I made a small detour. This whole ordeal would\n |
| 0x16c0bb | 45 | be pointless without its star, wouldn't you\n |
| 0x16c0e9 | 6 | agree? |
| 0x16c0f0 | 49 | Just as planned, he is presently on his way here. |
| 0x16c122 | 6 | WHAT!? |
| 0x16c129 | 34 | You speak true? Oshtor is coming!? |
| 0x16c14c | 46 | I see. Chin up, men! We just have to hang in\n |
| 0x16c17b | 49 | there a little longer until the princess's love\n |
| 0x16c1ad | 8 | arrives! |
| 0x16c1b6 | 49 | Heh, that's right. A good woman always fulfills\n |
| 0x16c1e8 | 13 | her promises! |
| 0x16c1f6 | 50 | Now hold on a minute! You--What do you mean, you\n |
| 0x16c229 | 41 | informed Oshtor? What the hell were you\n |
| 0x16c253 | 10 | thinking!? |
| 0x16c25e | 46 | Do you understand what's going to happen now\n |
| 0x16c28d | 14 | that he knows? |
| 0x16c29c | 29 | I haven't the slightest idea. |
| 0x16c2ba | 44 | This guy's out of his damn mind. Of course\n |
| 0x16c2e7 | 9 | he knows. |
| 0x16c2f1 | 45 | If this blows up any further, it's not just\n |
| 0x16c31f | 46 | going to be disastrous for us, but for these\n |
| 0x16c34e | 12 | bandits too. |
| 0x16c35b | 26 | Ah, it seems he's arrived. |
| 0x16c376 | 17 | Wha--Wh-Wh-Wh--!? |
| 0x16c388 | 42 | Ah, Oshtor! Oshtor! Over here! Your Anju\n |
| 0x16c3b3 | 22 | awaits you right here! |
| 0x16c3ca | 28 | It... can't be. Osh...tor... |
| 0x16c3e7 | 41 | Indeed! My most loyal retainer, Oshtor,\n |
| 0x16c411 | 28 | Imperial Guard of the Right! |
| 0x16c42e | 44 | Regardless of how loyal he is to you, he's\n |
| 0x16c45b | 31 | definitely not YOUR retainer... |
| 0x16c47b | 7 | ...Huh? |
| 0x16c483 | 35 | Oshtor... loyal retainer... Anju... |
| 0x16c4a7 | 21 | Anju... the princess? |
| 0x16c4bd | 27 | I-It can't--You CAN'T be... |
| 0x16c4d9 | 17 | I cannot be what? |
| 0x16c4eb | 49 | Pardon me for asking, but... could you be Anju,\n |
| 0x16c51d | 22 | the imperial princess? |
| 0x16c534 | 45 | Hm? Ah, indeed. I am the Divine Scion Anju,\n |
| 0x16c562 | 40 | heiress to the Mikado and future ruler\n |
| 0x16c58b | 14 | of all Yamato. |
| 0x16c59a | 26 | Have I not mentioned this? |
| 0x16c5b5 | 42 | I-I hadn't heard it spoken of even once!\n |
| 0x16c5e0 | 49 | Please, Your Highness, f-forgive any disrespect\n |
| 0x16c612 | 10 | I may ha-- |
| 0x16c61d | 42 | Bah, worry not over such trivial things.\n |
| 0x16c648 | 27 | We are friends, are we not? |
| 0x16c664 | 46 | Th-Thank you... Such words are wasted on the\n |
| 0x16c693 | 12 | likes of me! |
| 0x16c6a0 | 41 | Look to your role, now. Oshtor is here.\n |
| 0x16c6ca | 31 | I am counting upon you, Nosuri. |
| 0x16c6ea | 23 | Huh? Counting on... me? |
| 0x16c702 | 48 | Of course. Do you not remember? You shall play\n |
| 0x16c733 | 46 | the part of the villain and face off against\n |
| 0x16c762 | 4 | him. |
| 0x16c767 | 28 | You mean... fight... Oshtor? |
| 0x16c784 | 13 | Yes, just so! |
| 0x16c792 | 49 | I-It would appear he's brought his subordinates\n |
| 0x16c7c4 | 35 | with him... All of them, in fact... |
| 0x16c7e8 | 38 | Good! Now you shall be evenly matched. |
| 0x16c80f | 17 | Um... but... I... |
| 0x16c821 | 13 | I pity you... |
| 0x16c82f | 50 | Well. Now that Her Highness's escort has arrived\n |
| 0x16c862 | 40 | to pick her up, we'd best be on our way. |
| 0x16c88b | 27 | Shall we be off, my sister? |
| 0x16c8a7 | 11 | Wh-What...? |
| 0x16c8b3 | 47 | I've secured our escape. Now that the man she\n |
| 0x16c8e3 | 49 | loves is here, it behooves us not to interfere,\n |
| 0x16c915 | 3 | hm? |
| 0x16c919 | 48 | Y--Yes, of course. You're right. We should get\n |
| 0x16c94a | 25 | out of her way at once... |
| 0x16c964 | 46 | We shall take our leave immediately. Farewell! |
| 0x16c993 | 49 | Wh--Where are you going!? You have to challenge\n |
| 0x16c9c5 | 37 | Oshtor to a fateful duel for my hand! |
| 0x16c9eb | 50 | I fail to comprehend. Why were they so desperate\n |
| 0x16ca1e | 48 | to leave...? {W480}Ah, but now it matters not.\n |
| 0x16ca4f | 9 | Oshtor... |
| 0x16ca59 | 16 | Princess Anju... |
| 0x16ca6a | 47 | You've done well to fly to my rescue, Oshtor!\n |
| 0x16ca9a | 40 | Truly, you are my most devoted retainer. |
| 0x16cac7 | 46 | Is something the matter? Why are you so quiet? |
| 0x16caf6 | 48 | I am sorry. If not for my own negligence, your\n |
| 0x16cb27 | 47 | judgement would never have become so clouded... |
| 0x16cb57 | 48 | Do not be so serious. See? No harm has come to\n |
| 0x16cb88 | 19 | me. Nary a scratch. |
| 0x16cb9c | 47 | Were it not for these people who came to your\n |
| 0x16cbcc | 44 | aid, who knows what might have happened to\n |
| 0x16cbf9 | 7 | you...? |
| 0x16cc01 | 48 | For the princess to be so easily abducted is a\n |
| 0x16cc32 | 46 | product of my own inattention, punishable by\n |
| 0x16cc61 | 6 | death. |
| 0x16cc68 | 30 | Wh-What are you talking about? |
| 0x16cc87 | 46 | I accept full responsibility for this lapse,\n |
| 0x16ccb6 | 47 | and hereby resign from my post. I... apologize. |
| 0x16cce6 | 32 | W-Wait--No, I cannot allow that! |
| 0x16cd07 | 47 | This evening was my fault alone. I-I won't do\n |
| 0x16cd37 | 36 | anything of this sort again. Please! |
| 0x16cd5c | 47 | What am I to tell Father, if I am to lose our\n |
| 0x16cd8c | 42 | most devoted retainer to a childish prank? |
| 0x16cdb7 | 45 | Please, I beg of you. P-Please remain at my\n |
| 0x16cde5 | 16 | side and aid me. |
| 0x16cdf6 | 48 | Looks like she's finally starting to grasp the\n |
| 0x16ce27 | 25 | gravity of her actions... |
| 0x16ce41 | 49 | She may go overboard way too much, but at least\n |
| 0x16ce73 | 50 | she knows when to say sorry. I can respect that,\n |
| 0x16cea6 | 6 | a bit. |
| 0x16cead | 41 | Your Highness... Please, no more tears.\n |
| 0x16ced7 | 16 | Raise your head. |
| 0x16cee8 | 46 | I thank you for your kindness in allowing me\n |
| 0x16cf17 | 43 | another chance despite this grave blunder\n |
| 0x16cf43 | 12 | I have made. |
| 0x16cf50 | 47 | I, Oshtor, hereby swear that I shall continue\n |
| 0x16cf80 | 38 | to uphold the peace of Yamato for you. |
| 0x16cfa7 | 44 | S-So you will not resign? Oh, Oshtor, I've\n |
| 0x16cfd4 | 26 | never been so relieved...! |
| 0x16cfef | 45 | Man. Everything seems to have worked out in\n |
| 0x16d01d | 19 | the end, but God... |
| 0x16d031 | 37 | Ah, one thing I neglected to mention. |
| 0x16d057 | 47 | Bwuh--You're still here!? Aren't you supposed\n |
| 0x16d087 | 41 | to, y'know, be making your timely escape? |
| 0x16d0b1 | 43 | Yes, but I thought of something I felt it\n |
| 0x16d0dd | 21 | important to mention. |
| 0x16d0f3 | 48 | Your Highness, I took the liberty of informing\n |
| 0x16d124 | 45 | your guardian of the evening's events on my\n |
| 0x16d152 | 9 | "detour." |
| 0x16d15c | 4 | Head |
| 0x16d161 | 15 | ...My guardian? |
| 0x16d171 | 50 | Indeed. If you'll excuse me, she appears to have\n |
| 0x16d1a4 | 17 | arrived just now. |
| 0x16d1b7 | 9 | AAAAACK!! |
| 0x16d1c1 | 43 | And just where do you think you're going,\n |
| 0x16d1ed | 14 | Your Highness? |
| 0x16d1fc | 45 | I seem to recall advising you not to follow\n |
| 0x16d22a | 31 | through with this foolish idea. |
| 0x16d24a | 43 | I believe some punishment is in order for\n |
| 0x16d276 | 42 | causing such a disturbance, wouldn't you\n |
| 0x16d2a1 | 26 | No, please, anything but-- |
| 0x16d2bc | 8 | NOOOOO!! |
| 0x16d2c5 | 26 | Cover your ears, everyone. |
| 0x16d2e0 | 45 | Wait, why exactly do we need to cover our...? |
| 0x16d30e | 38 | S-Stop! Desist! I-I'll apologize, so-- |
| 0x16d335 | 11 | AAAAAAAGH!! |
| 0x16d341 | 33 | I am sorry! I'm sorry! I'M SORRY! |
| 0x16d363 | 24 | Ow! Ow! OOOWWOWOW OW OW! |
| 0x16d37c | 45 | We all share a look, then cover our ears in\n |
| 0x16d3aa | 7 | unison. |
| 0x16d3b2 | 9 | RightFoot |
| 0x16d3bc | 8 | LeftFoot |

## 8. Formato de saida EXIGIDO
Escreva `translations_18_05.json` com a forma:
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
