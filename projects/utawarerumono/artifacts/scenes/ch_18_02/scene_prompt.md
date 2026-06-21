# Cena ch_18_02 — pacote de traducao (311 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| Woman | UI | Mulher | traduzir | none |

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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `herself.` -> `ela mesma.` (Haku, 15_02)
- `T-Truly?` -> `T-Tem certeza?` (Maroro, 13_09)
- `directly?` -> `diretamente?` (Protagonista, 18_01)
- `kid.` -> `miúdo.` (Haku, 18_01)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `him.` -> `dele.` (Nekone, 15_02)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `...Did you say something?` -> `...Você disse alguma coisa?` (Kuon, 14_03)
- `thing.` -> `coisa.` (Haku, 12_03)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `What? Why?` -> `O quê? Por quê?` (Nosuri, 16_01)
- `this.` -> `essa.` (Moznu, 13_05)
- `a person.` -> `uma pessoa.` (Haku, 18_01)
- `...Yes, ma'am.` -> `...Sim, sim.` (Rulutieh, 18_01)
- `What?` -> `Que?` (Haku, 12_02)
- `Wh--!?` -> `Q-Quê!?` (Haku, 18_01)
- `you...` -> `você...` (Haku, 12_11)
- `girl.` -> `aproxima da garota.` (Haku, 13_05)
- `her.` -> `a ela.` (Kuon, 17_01)
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
| 0x161e6b | 47 | I thought I'd relax in our headquarters for a\n |
| 0x161e9b | 49 | while, but Anju and Munechika are already here... |
| 0x161ecd | 45 | Is it just me, or have they been turning up\n |
| 0x161efb | 18 | here a lot lately? |
| 0x161f0e | 44 | Anju sits sullenly, not even reading, just\n |
| 0x161f3b | 44 | snacking and generally being in a foul mood. |
| 0x161f68 | 50 | Must be emotional binging or something. At least\n |
| 0x161f9b | 44 | appreciate the flavor, geez. Rulutieh made\n |
| 0x161fc8 | 6 | those. |
| 0x161fcf | 23 | Manners, Your Highness. |
| 0x161fe7 | 44 | Of course, Munechika SAYS that, but in the\n |
| 0x162014 | 44 | same breath moves to claim some snacks for\n |
| 0x162041 | 8 | herself. |
| 0x16204a | 43 | I know she's the Guardian of the Imperial\n |
| 0x162076 | 47 | Capital and all, but this feels like a misuse\n |
| 0x1620a6 | 14 | of her powers. |
| 0x1620b5 | 37 | Leave me be, lest I unchain my anger. |
| 0x1620db | 47 | Hm. Hmmm hmmm hm. All right, princess, I know\n |
| 0x16210b | 47 | love troubles when I see them. Care to divulge? |
| 0x16213b | 22 | Eh!? How did you know? |
| 0x162152 | 34 | I live for love, don't you know?\n |
| 0x162175 | 33 | I can smell it wherever it lurks. |
| 0x162197 | 36 | Truly? What an incredible ability... |
| 0x1621bc | 49 | Yeah, sure. Get back to me when you've actually\n |
| 0x1621ee | 41 | had success with love in the first place. |
| 0x162218 | 45 | S-So, you've already discerned what plagues\n |
| 0x162246 | 8 | my mind? |
| 0x16224f | 45 | Hmmm hmm. It can only be one thing, really.\n |
| 0x16227d | 14 | Oshtor, right? |
| 0x16228c | 27 | Y-You knew about that too!? |
| 0x1622a8 | 48 | ...Anyone who hangs around you for long enough\n |
| 0x1622d9 | 17 | knows about that. |
| 0x1622ef | 48 | Come on, now, princess. Why don't you tell the\n |
| 0x162320 | 46 | love sage about your problems? I'll fix them\n |
| 0x16234f | 9 | right up. |
| 0x162359 | 8 | T-Truly? |
| 0x162362 | 49 | Of course! Where love's concerned, you can just\n |
| 0x162394 | 23 | leave everything to me. |
| 0x1623ac | 41 | Atuy puffs out her chest, brimming with\n |
| 0x1623d6 | 11 | confidence. |
| 0x1623e2 | 38 | You'll... listen to my troubles, then? |
| 0x162409 | 46 | Anju looks up at Munechika as she says this... |
| 0x162438 | 15 | ...delicious... |
| 0x162448 | 47 | ...but she acts like she hasn't heard a word,\n |
| 0x162478 | 23 | absorbed in her sweets. |
| 0x162490 | 47 | I'm sure she heard her fine, but she probably\n |
| 0x1624c0 | 46 | just doesn't know what kind of advice to give. |
| 0x1624ef | 43 | I suppose it's her way of showing kindness. |
| 0x16251b | 46 | Well. As you've guessed, the matter concerns\n |
| 0x16254a | 18 | my vassal, Oshtor. |
| 0x16255d | 47 | ...Hey, Haku? Doesn't Oshtor serve the Mikado\n |
| 0x16258d | 9 | directly? |
| 0x162597 | 45 | Huh? I mean, yeah, he IS the Imperial Guard\n |
| 0x1625c5 | 15 | of the Right... |
| 0x1625d5 | 43 | H-He will EVENTUALLY be under my command.\n |
| 0x162601 | 38 | My statement was technically accurate. |
| 0x162628 | 48 | Oshtor is among my favorite retainers, and the\n |
| 0x162659 | 41 | man destined to stand by my side one day. |
| 0x162683 | 49 | Hee. That's the attitude I like to see, princess. |
| 0x1626b5 | 47 | Ah, but wait a moment. Nekone, was it? Do you\n |
| 0x1626e5 | 40 | not harbor feelings for Oshtor, as well? |
| 0x16270e | 20 | O-Of course I don't. |
| 0x162723 | 43 | I'm afraid I cannot brook a rival in this\n |
| 0x16274f | 44 | pursuit. You may pine for him, but he WILL\n |
| 0x16277c | 14 | be mine alone. |
| 0x16278b | 30 | You'll simply have to give up. |
| 0x1627aa | 44 | Yikes. I can sense a dark, foreboding aura\n |
| 0x1627d7 | 24 | rolling off of Nekone... |
| 0x1627f0 | 47 | But... no matter how I express myself to him,\n |
| 0x162820 | 38 | Oshtor never seems to take note of me. |
| 0x162847 | 44 | Pretty sure he's pretending not to notice.\n |
| 0x162874 | 12 | Take a hint. |
| 0x162881 | 47 | He may be Imperial Guard of the Right, but he\n |
| 0x1628b1 | 48 | probably can't get too chummy with his liege's\n |
| 0x1628e2 | 4 | kid. |
| 0x1628e7 | 45 | I suppose she's too young to really pick up\n |
| 0x162915 | 26 | on all that, still, but... |
| 0x162930 | 43 | Well, as long as love is on your side, no\n |
| 0x16295c | 46 | obstacle's too great! Oshtor's just a little\n |
| 0x16298b | 8 | uptight. |
| 0x162994 | 49 | If only he was more relaxed about these things,\n |
| 0x1629c6 | 26 | he'd be the perfect man... |
| 0x1629e1 | 44 | It's... highly improbable, but... D-Do you\n |
| 0x162a0e | 41 | suppose Oshtor p-possibly prefers... men? |
| 0x162a38 | 6 | WHAT!? |
| 0x162a3f | 44 | Uh, Rulutieh? Wh-Why are you looking at me\n |
| 0x162a6c | 23 | with that excited face? |
| 0x162a84 | 48 | My dear br--I-I mean, Oshtor has no such tastes! |
| 0x162ab5 | 40 | O-Of course. Friendship between men is\n |
| 0x162ade | 45 | beautiful, but I suppose there's a time and\n |
| 0x162b0c | 10 | a place... |
| 0x162b17 | 45 | Pretty sure the time and place have nothing\n |
| 0x162b45 | 14 | to do with it. |
| 0x162b54 | 45 | Mm... Now that I think about it, I remember\n |
| 0x162b82 | 44 | reading a book about a situation just like\n |
| 0x162baf | 6 | yours. |
| 0x162bb6 | 3 | Hm? |
| 0x162bba | 48 | It was about a girl who fell deep in love with\n |
| 0x162beb | 27 | a stoic, emotionless man... |
| 0x162c07 | 46 | She wanted to know his true feelings, so she\n |
| 0x162c36 | 47 | began to dream up all kinds of ways to "test"\n |
| 0x162c66 | 4 | him. |
| 0x162c6b | 10 | G-Go on... |
| 0x162c76 | 44 | Every plan she concocted went awry, so she\n |
| 0x162ca3 | 46 | decided to fake her own kidnapping as a last\n |
| 0x162cd2 | 7 | gambit. |
| 0x162cda | 37 | And THEN she gets kidnapped for real. |
| 0x162d00 | 24 | A-And what happens next? |
| 0x162d19 | 45 | Well, the man ends up risking everything to\n |
| 0x162d47 | 11 | rescue her! |
| 0x162d53 | 39 | As it turned out, he only came off as\n |
| 0x162d7b | 43 | emotionless because he didn't know how to\n |
| 0x162da7 | 21 | express his feelings. |
| 0x162dbd | 11 | That's it!! |
| 0x162dc9 | 4 | Huh? |
| 0x162dce | 42 | Such a method should allow me to confirm\n |
| 0x162df9 | 33 | Oshtor's true feelings toward me. |
| 0x162e1b | 39 | Riding to my rescue after my capture... |
| 0x162e43 | 48 | That's when Oshtor will finally confess to me.\n |
| 0x162e74 | 47 | "Your Highness... no, Anju. Allow me to speak\n |
| 0x162ea4 | 6 | true." |
| 0x162eab | 35 | And that's how we'll become lovers. |
| 0x162ecf | 31 | Eh heh heh. The perfect plan... |
| 0x162eef | 26 | Oh, that's what you meant. |
| 0x162f0a | 43 | And of course it's the perfect plan! It's\n |
| 0x162f36 | 47 | coming from yours truly, the love sage, after\n |
| 0x162f66 | 4 | all. |
| 0x162f6b | 47 | Indeed. Your assistance is greatly appreciated. |
| 0x162f9b | 27 | Pffft. "Love sage," my ass. |
| 0x162fb7 | 25 | ...Did you say something? |
| 0x162fd1 | 33 | Erm, n-no, I didn't say anything. |
| 0x162ff3 | 42 | Then it is settled. Haku. I order you to\n |
| 0x16301e | 10 | kidnap me! |
| 0x163029 | 39 | ...What the hell are you talking about? |
| 0x163051 | 22 | Are you deaf? Hearken: |
| 0x163068 | 49 | You shall play the role of a sinister evildoer,\n |
| 0x16309a | 48 | kidnap me, and stage a fateful duel with Oshtor. |
| 0x1630cb | 48 | Then, you shall brandish your blade at me, and\n |
| 0x1630fc | 13 | declare this: |
| 0x16310a | 48 | "The princess is my hostage! If you truly care\n |
| 0x16313b | 45 | for her, then come and win her back, if you\n |
| 0x163169 | 6 | dare." |
| 0x163170 | 29 | Do you WANT to get me killed? |
| 0x16318e | 46 | What are you talking about? I desire no such\n |
| 0x1631bd | 6 | thing. |
| 0x1631c4 | 44 | If you want me to face off against Oshtor,\n |
| 0x1631f1 | 45 | there's kinda only one realistic outcome to\n |
| 0x16321f | 5 | that. |
| 0x163225 | 41 | Bah. I fail to understand your concern.\n |
| 0x16324f | 47 | Don't worry yourself with such trivial details. |
| 0x16327f | 47 | Look, if you really want to brew up some kind\n |
| 0x1632af | 46 | of crisis, why don't you have Munechika do it? |
| 0x1632de | 45 | It'd be much more convincing for one of the\n |
| 0x16330c | 44 | Eight Pillars to stage a coup and take you\n |
| 0x163339 | 9 | prisoner. |
| 0x163343 | 32 | Yes... Yes! Haku, that's GENIUS. |
| 0x163364 | 48 | Well, I don't mean to br--Wait, wait, that was\n |
| 0x163395 | 38 | a JOKE. Can't you tell the difference? |
| 0x1633bc | 43 | A stroke of true genius indeed. Munechika-- |
| 0x1633e8 | 17 | I do not approve. |
| 0x1633fa | 10 | What? Why? |
| 0x163405 | 49 | Your Highness, do you not understand the weight\n |
| 0x163437 | 13 | of the crown? |
| 0x163445 | 47 | Were anything to happen to you, it would be a\n |
| 0x163475 | 41 | serious blow to the future of the empire. |
| 0x16349f | 48 | Besides that, you'd involve Lord Oshtor of the\n |
| 0x1634d0 | 46 | Twin Shields in your schemes? I cannot allow\n |
| 0x1634ff | 5 | this. |
| 0x163505 | 24 | B-But... if it's only... |
| 0x16351e | 44 | Are words alone not enough to dissuade you\n |
| 0x16354b | 15 | from this path? |
| 0x16355b | 36 | Munechika lifts her hand menacingly. |
| 0x163580 | 46 | I-I merely jest! A joke! P-Please lower your\n |
| 0x1635af | 6 | hand-- |
| 0x1635b6 | 5 | Ahem. |
| 0x1635bc | 44 | Actually, I have an alternative that might\n |
| 0x1635e9 | 13 | interest you. |
| 0x1635f7 | 48 | I'd go so far as to say it's a pretty flawless\n |
| 0x163628 | 14 | plan, in fact. |
| 0x163637 | 49 | I appreciate the thought, but I shall decline--\n |
| 0x163669 | 36 | not for lack of trusting you, but... |
| 0x16368e | 43 | You have few friends, yes? Let alone love\n |
| 0x1636ba | 46 | experience? I cannot accept a plan from such\n |
| 0x1636e9 | 9 | a person. |
| 0x1636f3 | 40 | ...Dear sister? Is something the matter? |
| 0x16371c | 26 | And now she's depressed... |
| 0x163737 | 50 | I know Anju didn't mean any harm, but that kinda\n |
| 0x16376a | 20 | makes it even worse. |
| 0x16377f | 30 | Wh-What are you talking about? |
| 0x16379e | 46 | I have PLENTY of friends! Just look around--\n |
| 0x1637cd | 25 | Rulutieh, Nekone, Atuy... |
| 0x1637e7 | 48 | Perplexing. I only mention it because I recall\n |
| 0x163818 | 41 | Haku declaring as much in a pitying tone. |
| 0x163842 | 19 | Wh--!? What are y-- |
| 0x163856 | 29 | Ahaha... I see. So that's it. |
| 0x163874 | 44 | Hmm. I suppose it cannot be helped. I will\n |
| 0x1638a1 | 45 | suspend my efforts on this endeavor for the\n |
| 0x1638cf | 7 | moment. |
| 0x1638d7 | 49 | Anju reluctantly lies down on the rug, flipping\n |
| 0x163909 | 28 | a book open with a harrumph. |
| 0x163926 | 29 | And I think I'll head out t-- |
| 0x163944 | 27 | Hakuuu? A moment, please... |
| 0x163960 | 14 | ...Yes, ma'am. |
| 0x16396f | 45 | Urgh. I was sure my head was gonna split...\n |
| 0x16399d | 40 | She's been getting more vicious, lately. |
| 0x1639c6 | 46 | So why exactly did you need to talk to me in\n |
| 0x1639f5 | 10 | secret...? |
| 0x163a00 | 47 | It regards our earlier discussion, naturally.\n |
| 0x163a30 | 42 | Surely there must be SOMETHING you can do. |
| 0x163a5b | 48 | Nnhh. I should've guessed you haven't given up\n |
| 0x163a8c | 8 | on that. |
| 0x163a95 | 48 | Of course not. What manner of girl gives up on\n |
| 0x163ac6 | 45 | the one she loves at the first inconvenience? |
| 0x163af4 | 45 | Look, I understand how you feel, but faking\n |
| 0x163b22 | 38 | your own kidnapping is not the answer. |
| 0x163b49 | 48 | It is the only method by which I can determine\n |
| 0x163b7a | 45 | You said you understand how I feel, but you\n |
| 0x163ba8 | 44 | don't understand the intensity of this love. |
| 0x163bd5 | 42 | You wouldn't speak of such things if you\n |
| 0x163c00 | 40 | understood these feelings of... longing. |
| 0x163c29 | 48 | This isn't good. She might go and do something\n |
| 0x163c5a | 21 | drastic at this rate. |
| 0x163c70 | 50 | It'll be difficult to stop her if she does start\n |
| 0x163ca3 | 47 | down that path... I have to do something, but\n |
| 0x163cd3 | 5 | what? |
| 0x163cd9 | 49 | I beg of you, Haku. The fate of my love depends\n |
| 0x163d0b | 9 | upon you. |
| 0x163d15 | 44 | Oh, come ON. How is all the responsibility\n |
| 0x163d42 | 22 | on me all of a sudden? |
| 0x163d59 | 38 | Fear not, for I have heard your pleas! |
| 0x163d80 | 48 | Suddenly, a floorboard flies open and a person\n |
| 0x163db1 | 21 | crawls into the room! |
| 0x163dc7 | 6 | Wh--!? |
| 0x163dce | 44 | Young maiden, distraught by affairs of the\n |
| 0x163dfb | 39 | heart--I shall help you in your plight! |
| 0x163e23 | 40 | Y-You--what the hell are YOU doing here? |
| 0x163e4c | 46 | Ahahaha! When least expected, the good woman\n |
| 0x163e7b | 8 | appears! |
| 0x163e84 | 50 | Nosuri trails dirt all over, and I'm pretty sure\n |
| 0x163eb7 | 39 | those are twigs and leaves in her hair. |
| 0x163edf | 48 | My desire to continue getting involved in this\n |
| 0x163f10 | 33 | mess is plummeting by the second. |
| 0x163f32 | 30 | You'll aid me? You speak true? |
| 0x163f51 | 44 | You seek someone to pretend to kidnap you,\n |
| 0x163f7e | 46 | then to waylay the man who will come to your\n |
| 0x163fad | 12 | rescue, yes? |
| 0x163fba | 48 | And then to be defeated in spectacular fashion\n |
| 0x163feb | 19 | and make an escape? |
| 0x163fff | 44 | A good woman never hesitates when it comes\n |
| 0x16402c | 29 | to helping a lovesick maiden! |
| 0x16404a | 17 | Am I wrong, Ougi? |
| 0x16405c | 34 | You are correct indeed, my sister. |
| 0x16407f | 28 | Ah--So you really will help! |
| 0x16409c | 6 | You... |
| 0x1640a3 | 27 | Ah, fancy meeting you here. |
| 0x1640bf | 49 | Don't pretend like it's a coincidence! You were\n |
| 0x1640f1 | 43 | listening the whole damn time, weren't you? |
| 0x16411d | 49 | I admit it was a fascinating conversation to be\n |
| 0x16414f | 9 | party to. |
| 0x164159 | 48 | If you're planning on helping her, you need to\n |
| 0x16418a | 27 | stop right now, understand? |
| 0x1641a6 | 47 | Whatever for? You would have us deny the help\n |
| 0x1641d6 | 46 | we're positioned to render to this young lady? |
| 0x164205 | 49 | Look, don't ask for reasons. Just trust me when\n |
| 0x164237 | 18 | I say don't do it. |
| 0x16424a | 47 | I can't exactly just tell them the princess's\n |
| 0x16427a | 15 | true identi--\n |
| 0x16428a | 8 | ...Wait. |
| 0x164293 | 41 | ...if this guy works with Oshtor, then... |
| 0x1642bd | 28 | You already know, don't you? |
| 0x1642da | 29 | What could you possibly mean? |
| 0x1642f8 | 48 | Don't play dumb with me. I'm talking about the\n |
| 0x164329 | 5 | girl. |
| 0x16432f | 47 | I'm certain I know nothing about Her Highness\n |
| 0x16435f | 19 | taking refuge here. |
| 0x164373 | 46 | Asshole. You DO know! You could get beheaded\n |
| 0x1643a2 | 41 | if you go through with this, you realize. |
| 0x1643cc | 47 | I believe we'll be able to manage. This IS my\n |
| 0x1643fc | 47 | beloved sister, after all. I'm quite proud of\n |
| 0x16442c | 4 | her. |
| 0x164431 | 28 | You're not making any sense. |
| 0x16444e | 47 | Few things are more honorable than to respond\n |
| 0x16447e | 39 | to a plea for help from the princess.\n |
| 0x1644a6 | 18 | I cannot stop her. |
| 0x1644b9 | 47 | Beside the point, I believe it is now too late. |
| 0x1644e9 | 27 | Huh...? Wh--When did they-- |
| 0x164505 | 50 | Oh, they took their leave while we were talking,\n |
| 0x164538 | 10 | I imagine. |
| 0x164543 | 44 | That's my dear sister for you, I'm afraid.\n |
| 0x164570 | 46 | Always acting in the manner one least expects. |
| 0x16459f | 50 | Ougi's small, faintly amused smile suggests he's\n |
| 0x1645d2 | 34 | actually enjoying this whole mess. |
| 0x1645f5 | 19 | Are you seriously-- |
| 0x164609 | 29 | Ah, yes, and this is for you. |
| 0x164627 | 31 | Ougi produces a piece of paper. |
| 0x164647 | 47 | Observe. The run-down mountain retreat marked\n |
| 0x164677 | 46 | on this map should do nicely. Escape will be\n |
| 0x1646a6 | 8 | trivial. |
| 0x1646af | 46 | I will delay as best I'm able, but I can buy\n |
| 0x1646de | 48 | only so much time. If you wish to take action,\n |
| 0x16470f | 9 | be quick. |
| 0x164719 | 39 | I look forward to seeing what you do... |
| 0x164741 | 41 | On that strangely nonchalant note, Ougi\n |
| 0x16476b | 27 | disappears without a sound. |
| 0x164787 | 49 | Would it kill these people to give some thought\n |
| 0x1647b9 | 49 | to the guy who has to clean up their damn messes? |
| 0x1647eb | 47 | God. At this rate, all our heads are going to\n |
| 0x16481b | 41 | roll for letting this get so out of hand. |
| 0x164845 | 50 | And the only way to avoid that is to rescue Anju\n |
| 0x164878 | 32 | before word even reaches Oshtor. |
| 0x164899 | 36 | It's just one thing after another... |

## 8. Formato de saida EXIGIDO
Escreva `translations_18_02.json` com a forma:
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
