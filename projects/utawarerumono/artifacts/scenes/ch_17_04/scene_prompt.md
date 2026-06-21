# Cena ch_17_04 — pacote de traducao (423 linhas)

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
| Bokoinante | Personagem | Bokoinante | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Yeah? What's up?` -> `Oi? O que foi?` (Ukon, 13_01)
- `anyway.` -> `de agora.` (Ougi, 13_08)
- `Nekone?` -> `Nekone?` (Haku, 15_07)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `Bwuh!?` -> `Ué!?` (Haku, 16_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Brigand` -> `Bandido` (SISTEMA, 13_05)
- `now...` -> `agora...` (Haku, 12_03)
- `toward us.` -> `para nós.` (Haku, 13_05)
- `judgement.` -> `julgamento.` (Nekone, 15_01)
- `brother.` -> `irmão.` (Ukon, 15_05)
- `Anyway...` -> `Enfim...` (Haku, 17_01)
- `What're you talking about?` -> `Como assim?` (Ukon, 13_05)
- `like this.` -> `dessas.` (Kuon, root)
- `another.` -> `outra.` (Rulutieh, 17_01)
- `least.` -> `enfim.` (Ukon, 12_12)
- `What?` -> `Que?` (Haku, 12_02)
- `What the--` -> `Mas que--` (Haku, 11_03)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `that...` -> `essa...` (Haku, 15_03)
- `Haku...` -> `Haku...` (Kuon, 14_09)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `it.` -> `aí.` (Haku, 15_03)
- `arrived.` -> `chegar.` (Nekone, 15_03)
- `allowance.` -> `mesada.` (Kuon, 13_09)
- `love?` -> `amor?` (Atuy, 15_04)
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
| 0x117a1a | 12 | Now, then... |
| 0x117a27 | 46 | I begin to unpack the supplies I brought for\n |
| 0x117a56 | 41 | standing watch at Dekopompo's storehouse. |
| 0x117a80 | 5 | Haku? |
| 0x117a86 | 16 | Yeah? What's up? |
| 0x117a97 | 37 | What, uh... What exactly is all that? |
| 0x117abd | 40 | Necessities for the job. Can't you tell? |
| 0x117ae6 | 47 | Those just look like booze and games, though... |
| 0x117b16 | 42 | Didn't you say you wanted to get a drink\n |
| 0x117b41 | 22 | AFTER the job is done? |
| 0x117b58 | 45 | THESE drinks are to warm us up when it gets\n |
| 0x117b86 | 49 | cold. And the games will help us pass the time,\n |
| 0x117bb8 | 4 | see? |
| 0x117bbd | 19 | Are you serious...? |
| 0x117bd1 | 35 | Um, are you sure this is all right? |
| 0x117bf5 | 23 | I... suppose it's fine. |
| 0x117c0d | 47 | We don't necessarily have to give our all for\n |
| 0x117c3d | 42 | this job. We could use a change of pace,\n |
| 0x117c68 | 7 | anyway. |
| 0x117c74 | 7 | Nekone? |
| 0x117c7c | 47 | ...It is as my dear sister says. We have been\n |
| 0x117cac | 27 | pushing ourselves, of late. |
| 0x117cc8 | 47 | If you show this lack of discipline around my\n |
| 0x117cf8 | 45 | dear brother, however, you will NOT see the\n |
| 0x117d26 | 13 | next morning. |
| 0x117d34 | 11 | G-Got it... |
| 0x117d40 | 9 | N-Nekone? |
| 0x117d4a | 45 | Oh, you've got shogi! Wanna play a match or\n |
| 0x117d78 | 10 | two, love? |
| 0x117d83 | 39 | I may not look it, but I'm pretty good. |
| 0x117dab | 29 | I'll call next game, I think. |
| 0x117dc9 | 33 | I will have the match after that. |
| 0x117deb | 25 | And then Rulutieh's turn! |
| 0x117e05 | 18 | I-I'm playing too? |
| 0x117e18 | 31 | Yep. You like shogi, don't you? |
| 0x117e38 | 45 | U-Uhm... if everyone else is playing, then... |
| 0x117e66 | 39 | Heh. All right, I'll take you all on.\n |
| 0x117e8e | 9 | Let's go! |
| 0x117e98 | 49 | Um... I'll move here to take your hisha, and...\n |
| 0x117eca | 21 | I think that's check. |
| 0x117ee0 | 8 | Hnngh... |
| 0x117ee9 | 49 | Damn it, this isn't how this was supposed to go\n |
| 0x117f1b | 7 | at all! |
| 0x117f23 | 45 | Haku, love? You're... not very good at this\n |
| 0x117f51 | 14 | game, are you? |
| 0x117f60 | 48 | This marks your fourth loss. I believe this is\n |
| 0x117f91 | 40 | what is referred to as being "all talk." |
| 0x117fba | 9 | Nngh...!! |
| 0x117fc4 | 33 | Oh, Haku, you shouldn't move th-- |
| 0x117fe6 | 43 | No, no, I don't need advice! I've got this. |
| 0x118012 | 12 | But if you-- |
| 0x11801f | 48 | I said I've got it. I just need to move... here! |
| 0x118050 | 31 | And that gets me my hisha back. |
| 0x118070 | 5 | Um... |
| 0x118076 | 6 | Uh-oh. |
| 0x11807d | 9 | *Sigh*... |
| 0x118087 | 8 | Wh-What? |
| 0x118090 | 46 | Um... OK. I'm sorry, but I'll be taking your\n |
| 0x1180bf | 12 | keima, then. |
| 0x1180cc | 6 | Bwuh!? |
| 0x1180d3 | 43 | Goodness. That was a really bad move, love. |
| 0x1180ff | 46 | You could've blocked her with your fu, Haku... |
| 0x11812e | 39 | This isn't how it was supposed to be... |
| 0x118156 | 41 | Holy shit, I can't watch this any more!\n |
| 0x118180 | 40 | Your fu was right there! RIGHT. THERE.\n |
| 0x1181a9 | 17 | For the love of-- |
| 0x1181bb | 4 | Huh? |
| 0x1181c5 | 4 | Wh-- |
| 0x1181ca | 43 | Get outta the way, amateur. I'll show you\n |
| 0x1181f6 | 31 | how to fuckin' PLAY. I swear... |
| 0x118216 | 22 | W-Wait, aren't you...? |
| 0x11822d | 3 | Hm? |
| 0x118231 | 9 | Aw, shit! |
| 0x11823b | 6 | Heh... |
| 0x118242 | 45 | AhaHA! Caught you right in my trap, intruder! |
| 0x118270 | 45 | I knew if I kept losing I'd eventually lure\n |
| 0x11829e | 29 | you out of your hiding place! |
| 0x1182bc | 6 | What!? |
| 0x1182c3 | 35 | Whaaat? You were losing on PURPOSE? |
| 0x1182e7 | 44 | Did you really think I'd lose that easily?\n |
| 0x118314 | 46 | Come on. To fool your enemy, first fool your\n |
| 0x118343 | 7 | allies. |
| 0x11834b | 47 | Oh, wow. Do you know how cool you sound right\n |
| 0x11837b | 4 | now? |
| 0x118380 | 27 | That's amazing, Sir Haku... |
| 0x11839c | 48 | Crap, I'm just spewing nonsense. I can't think\n |
| 0x1183cd | 35 | of anything to back that up with... |
| 0x1183f1 | 48 | Please, don't look at me with such admiration.\n |
| 0x118422 | 47 | You're making me feel guilty for deceiving you. |
| 0x118452 | 9 | No way... |
| 0x11845c | 47 | And now I'm uncomfortable for ANOTHER reason... |
| 0x11848c | 12 | Gah, dammit! |
| 0x118499 | 44 | Don't think we're going to let you go that\n |
| 0x1184c6 | 5 | easy! |
| 0x1184cc | 44 | You're not getting away, mainly for my sake. |
| 0x1184f9 | 37 | Argh. FINE! Let's wrap this up, boys! |
| 0x11851f | 47 | Figures materialize from the shadows at their\n |
| 0x11854f | 16 | leader's call... |
| 0x118560 | 7 | Brigand |
| 0x118568 | 28 | Boss, what's WRONG with you? |
| 0x118585 | 44 | We got THIS far without being noticed, and\n |
| 0x1185b2 | 6 | now... |
| 0x1185b9 | 41 | Shut up, you idiots! What's done is done! |
| 0x1185e3 | 31 | U-Um... Sir, about last time... |
| 0x118614 | 20 | No! Y-You're that--! |
| 0x118629 | 39 | Boss, the guards know we're here now.\n |
| 0x118651 | 40 | If we stick around too long, we might... |
| 0x11867a | 45 | Shit, shit, shit! Let's just book it, then.\n |
| 0x1186a8 | 41 | Damn it all, this won't happen next time! |
| 0x1186d2 | 25 | Stay right where you are! |
| 0x1186ec | 47 | Like I'm gonna stick around for you, shitbrain! |
| 0x11871c | 48 | Before I can blink, Kiwru has an arrow out and\n |
| 0x11874d | 49 | is taking aim--but they're already vaulting the\n |
| 0x11877f | 5 | wall. |
| 0x118785 | 47 | YERGH! Who the fuck left dog shit here of all\n |
| 0x1187b5 | 8 | places!? |
| 0x1187be | 43 | They got away, huh... I hate to give them\n |
| 0x1187ea | 47 | credit, but they're damn fast. We might never\n |
| 0x11881a | 15 | catch them now. |
| 0x11882a | 47 | I would prefer you at least try to PRETEND to\n |
| 0x11885a | 39 | catch them before you make such claims. |
| 0x118882 | 48 | Nighttime is perfect for an ambush. If we give\n |
| 0x1188b3 | 48 | chase now, they'll have friends lying in wait,\n |
| 0x1188e4 | 9 | no doubt. |
| 0x1188ee | 33 | And what are you REALLY thinking? |
| 0x118910 | 48 | Too much of a pain. We were hired to guard the\n |
| 0x118941 | 35 | storehouse, not go on bandit hunts. |
| 0x118965 | 46 | Hell if I'm going to chase them all over the\n |
| 0x118994 | 46 | capital. As long as they're gone, our job is\n |
| 0x1189c3 | 5 | done. |
| 0x1189c9 | 48 | I barely even want to argue with you any more... |
| 0x1189fa | 45 | Nekone gives me a sidelong look, exasperated. |
| 0x118a28 | 45 | Those were the criminals we dealt with last\n |
| 0x118a56 | 45 | time, right? Why are they running about the\n |
| 0x118a84 | 11 | city again? |
| 0x118a90 | 44 | Probably broke out again, going by the way\n |
| 0x118abd | 45 | they were talking. They're a tenacious bunch. |
| 0x118aeb | 46 | Escaped again... Are you sure it's all right\n |
| 0x118b1a | 26 | that we let them get away? |
| 0x118b35 | 45 | For now. It's our job to stand guard, so we\n |
| 0x118b63 | 27 | shouldn't abandon our post. |
| 0x118b7f | 45 | Suddenly, hurried footsteps come thundering\n |
| 0x118bad | 10 | toward us. |
| 0x118bb8 | 50 | Where are they!? Where are those lowborn ROGUES?\n |
| 0x118beb | 22 | Is my storehouse safe? |
| 0x118c02 | 45 | Dekopompo stomps toward us with rage in his\n |
| 0x118c30 | 39 | eyes and spittle flying from his mouth. |
| 0x118c58 | 46 | I was warned about his greed, but yikes. One\n |
| 0x118c87 | 49 | storehouse works him up this much? Guy needs to\n |
| 0x118cb9 | 6 | chill. |
| 0x118cc0 | 46 | You there, Oshtor's man! Answer my question.\n |
| 0x118cef | 4 | Now! |
| 0x118cf4 | 47 | There's no need to worry. Bandits attempted a\n |
| 0x118d24 | 42 | raid, but we drove them off easily enough. |
| 0x118d4f | 38 | Is that so? Then where are they now?\n |
| 0x118d76 | 25 | No corpses, no prisoners? |
| 0x118d90 | 45 | We were able to protect the storehouse, but\n |
| 0x118dbe | 18 | the bandits esca-- |
| 0x118dd1 | 44 | I quickly slap my hand over Kiwru's mouth.\n |
| 0x118dfe | 15 | That was close. |
| 0x118e0e | 47 | We CONSIDERED chasing after them, but decided\n |
| 0x118e3e | 42 | to prioritize protecting your stores, sir. |
| 0x118e69 | 44 | ...You let intruders on my property escape\n |
| 0x118e96 | 10 | unharried? |
| 0x118ea1 | 42 | It's likely the group we drove off was a\n |
| 0x118ecc | 46 | distraction. If we pursued, another would've\n |
| 0x118efb | 16 | cleaned you out. |
| 0x118f0c | 48 | Tch... Well, then. I commend you for your good\n |
| 0x118f3d | 10 | judgement. |
| 0x118f48 | 47 | Dekopompo talks through his teeth, unhappy as\n |
| 0x118f78 | 35 | he walks past us to the storehouse. |
| 0x118f9c | 47 | As he ducks inside with his entourage, Nekone\n |
| 0x118fcc | 7 | scowls. |
| 0x118fd4 | 49 | It is difficult for me to believe a man such as\n |
| 0x119006 | 44 | THAT is as exalted a general as my dearest\n |
| 0x119033 | 8 | brother. |
| 0x11903c | 47 | I suppose it can't be helped. Not all men can\n |
| 0x11906c | 21 | be as good as Oshtor. |
| 0x119082 | 46 | That was a pain. I don't think I'm accepting\n |
| 0x1190b1 | 48 | again if he offers more guard jobs. So sleepy... |
| 0x1190e2 | 46 | ...for example, we have someone like THIS in\n |
| 0x119111 | 10 | our ranks. |
| 0x11911c | 43 | Um, Haku? Why did you cover my mouth back\n |
| 0x119148 | 41 | there? You ended up saying they escaped\n |
| 0x119172 | 9 | anyway... |
| 0x11917c | 49 | Hm? Oh, it's not really a big deal or anything.\n |
| 0x1191ae | 26 | It was just your phrasing. |
| 0x1191c9 | 46 | When you make something sound like it's your\n |
| 0x1191f8 | 48 | fault, people like that guy will try to use it\n |
| 0x119229 | 12 | against you. |
| 0x119236 | 47 | But we DID let them escape. How could we have\n |
| 0x119266 | 44 | failed like that, on a job for Brother, no\n |
| 0x119293 | 8 | less...? |
| 0x11929c | 28 | What're you talking about?\n |
| 0x1192b9 | 24 | We did just fine, Kiwru. |
| 0x1192d2 | 49 | Like I said. Our job was to keep the storehouse\n |
| 0x119304 | 5 | safe. |
| 0x11930a | 49 | Nobody told us what to do with any bandits that\n |
| 0x11933c | 47 | might turn up. We're within the parameters of\n |
| 0x11936c | 8 | the job. |
| 0x119375 | 23 | You can't be serious... |
| 0x11938d | 41 | You're... TECHNICALLY right, I suppose.\n |
| 0x1193b7 | 45 | Why is it you only find a way with words in\n |
| 0x1193e5 | 17 | these situations? |
| 0x1193f7 | 49 | I still fail to understand what my dear brother\n |
| 0x119429 | 14 | sees in him... |
| 0x119438 | 45 | Care for another round of shogi when we get\n |
| 0x119466 | 46 | back, love? I'd like to see how you play for\n |
| 0x119495 | 10 | real, now. |
| 0x1194a0 | 48 | You never finished your game with Rulie, after\n |
| 0x1194d1 | 22 | all. Isn't that right? |
| 0x1194e8 | 40 | Yes, I'd love to see your real skills... |
| 0x119511 | 49 | I-I'm, uh... I'm a little tired after all that,\n |
| 0x119543 | 31 | honestly. M-Maybe another time? |
| 0x119563 | 24 | Th-This is an emergency! |
| 0x11957c | 49 | Out of nowhere, a figure comes barreling toward\n |
| 0x1195ae | 25 | us from the manor proper. |
| 0x1195c8 | 43 | An emergency! An emergency, Lord Dekopompo! |
| 0x1195f4 | 46 | What is it now, Bokoinante? I'm ensuring the\n |
| 0x119623 | 46 | integrity of my inventory, and I'm NOT to be\n |
| 0x119652 | 5 | dis-- |
| 0x119658 | 34 | A-Another time, my lord! Please!\n |
| 0x11967b | 21 | It seems as though... |
| 0x119691 | 46 | The tall man bends to whisper something into\n |
| 0x1196c0 | 34 | Dekopompo's ear, seeing us nearby. |
| 0x1196e3 | 6 | WHAT!? |
| 0x1196ea | 48 | I can't quite see inside the storehouse, but I\n |
| 0x11971b | 44 | can tell his expression has turned to panic. |
| 0x119748 | 43 | Have you ensured NOBODY entered after that? |
| 0x119774 | 47 | I-I'm afraid a patrol has begun an inspection\n |
| 0x1197a4 | 25 | of the premises, my lord. |
| 0x1197be | 33 | WHAT!? Curse them to the grave!\n |
| 0x1197e0 | 37 | How DARE they intrude in such things? |
| 0x119806 | 43 | Clearly in a panic, Dekopompo hurries off\n |
| 0x119832 | 44 | somewhere else, Bokoinante close behind him. |
| 0x11985f | 38 | Uh...I wonder if something's happened. |
| 0x119886 | 14 | Eh. Who knows. |
| 0x119895 | 45 | Dear brother, we have finished the task you\n |
| 0x1198c3 | 20 | sent us to complete. |
| 0x1198d8 | 43 | I thank you for your tireless efforts, my\n |
| 0x119904 | 34 | friends. I trust nobody is harmed? |
| 0x119927 | 22 | Yes, everyone is fine. |
| 0x11993e | 44 | So, Oshtor. You mind letting us in on what\n |
| 0x11996b | 48 | exactly happened behind the scenes for this one? |
| 0x11999c | 37 | I'm a little curious myself, I think. |
| 0x1199c2 | 18 | Behind the scenes? |
| 0x1199d5 | 50 | Oshtor smiles knowingly at Kiwru's bewilderment,\n |
| 0x119a08 | 26 | then gives me a small nod. |
| 0x119a23 | 21 | So you noticed, then. |
| 0x119a39 | 40 | It wasn't difficult to figure out that\n |
| 0x119a62 | 43 | something's up. Everything about that job\n |
| 0x119a8e | 15 | was suspicious. |
| 0x119a9e | 45 | ...Perhaps I ought to explain myself, then.\n |
| 0x119acc | 47 | This matter may well concern you in the future. |
| 0x119afc | 14 | In the future? |
| 0x119b0b | 45 | To speak candidly, Dekopompo is under heavy\n |
| 0x119b39 | 45 | suspicion of illegal dealings and activities. |
| 0x119b67 | 44 | What, like embezzlement? Tax evasion, that\n |
| 0x119b94 | 14 | kind of thing? |
| 0x119ba3 | 49 | Certainly those, but no, he seems more directly\n |
| 0x119bd5 | 42 | involved in this. I suspect he possesses\n |
| 0x119c00 | 11 | contraband. |
| 0x119c0c | 29 | "Contraband?" That's ominous. |
| 0x119c2a | 45 | Items like that are usually very dangerous.\n |
| 0x119c58 | 45 | I would've thought that Yamato had stricter\n |
| 0x119c86 | 11 | trade laws. |
| 0x119c92 | 49 | Indeed. There are rigorous customs inspections,\n |
| 0x119cc4 | 44 | especially on goods in the imperial capital. |
| 0x119cf1 | 47 | Perhaps it's improper of me, but if you asked\n |
| 0x119d21 | 48 | me whether Dekopompo deserves to be a general... |
| 0x119d52 | 44 | I would hesitate to say yes. That doesn't,\n |
| 0x119d7f | 44 | however, disqualify his cunning in matters\n |
| 0x119dac | 10 | like this. |
| 0x119db7 | 46 | He deftly sidesteps surveillance, defies any\n |
| 0x119de6 | 44 | attempt at spying or tracking that targets\n |
| 0x119e13 | 6 | him... |
| 0x119e1a | 44 | And most frustratingly, uses his office as\n |
| 0x119e47 | 49 | one of the Eight Pillar Generals as leverage to\n |
| 0x119e79 | 18 | avoid inspections. |
| 0x119e8c | 44 | As you can imagine, gathering any evidence\n |
| 0x119eb9 | 46 | against him has been an exercise in futility\n |
| 0x119ee8 | 11 | before now. |
| 0x119ef4 | 47 | Last night, I ensured you would be guarding a\n |
| 0x119f24 | 44 | particular storehouse while bandits raided\n |
| 0x119f51 | 8 | another. |
| 0x119f5a | 46 | All crime scenes--even those on the property\n |
| 0x119f89 | 46 | of a general--are to be inspected by a guard\n |
| 0x119fb8 | 7 | patrol. |
| 0x119fc0 | 47 | Per my duty as an Imperial Guard, I sent such\n |
| 0x119ff0 | 46 | a patrol to the manor after the raid, and lo\n |
| 0x11a01f | 12 | and behold-- |
| 0x11a02c | 48 | They discovered such contraband in Dekopompo's\n |
| 0x11a05d | 46 | stores. It's caused quite a stir, to say the\n |
| 0x11a08c | 6 | least. |
| 0x11a093 | 45 | He'll try to talk his way out of things, of\n |
| 0x11a0c1 | 41 | course, but it's fairly damning evidence. |
| 0x11a0eb | 48 | It should allow for an exhaustive case against\n |
| 0x11a11c | 47 | him--and unavoidable punishment for his crimes. |
| 0x11a14c | 32 | So you used us as a distraction. |
| 0x11a16d | 44 | In order to get at the storehouse you were\n |
| 0x11a19a | 44 | after, you orchestrated a scene at another\n |
| 0x11a1c7 | 6 | one... |
| 0x11a1ce | 45 | Doesn't that mean the bandits we chased off\n |
| 0x11a1fc | 31 | were working under your orders? |
| 0x11a21c | 5 | What? |
| 0x11a222 | 29 | Ah, that's not quite correct. |
| 0x11a240 | 46 | A new voice causes everyone in the room save\n |
| 0x11a26f | 19 | Oshtor to tense up. |
| 0x11a283 | 49 | I'd hardly consider them comrades. We merely...\n |
| 0x11a2b5 | 47 | ensured certain words reached certain ears to\n |
| 0x11a2e5 | 10 | bait them. |
| 0x11a2f0 | 12 | What the--\n |
| 0x11a2fd | 23 | Where did HE come from? |
| 0x11a315 | 48 | Hmm... You've got a pretty face, but you don't\n |
| 0x11a346 | 39 | look like a very interesting man. Pass. |
| 0x11a36e | 33 | Quite a frank assessment, madame. |
| 0x11a390 | 46 | In a flash of memories, I suddenly recognize\n |
| 0x11a3bf | 23 | the man in front of us. |
| 0x11a3d7 | 12 | This guy's-- |
| 0x11a3e4 | 48 | That's right. I THOUGHT I recognized this guy!\n |
| 0x11a415 | 45 | He was there when we took down those bandits. |
| 0x11a443 | 48 | This is Ougi, a collaborator of mine. He works\n |
| 0x11a474 | 48 | with the 'noble thief' I'm sure you've heard of. |
| 0x11a4a5 | 45 | It happens that Oshtor's interests and mine\n |
| 0x11a4d3 | 47 | align, on happy occasion. We, ah... cooperate\n |
| 0x11a503 | 14 | in such times. |
| 0x11a512 | 45 | Ougi sounds faintly amused as he produces a\n |
| 0x11a540 | 44 | ledger, leafing through it to a particular\n |
| 0x11a56d | 5 | page. |
| 0x11a573 | 39 | Is that ledger what you were after in\n |
| 0x11a59b | 18 | Dekopompo's manor? |
| 0x11a5ae | 44 | Just so. This is a record of his moonlight\n |
| 0x11a5db | 47 | transactions, as it were. You have my deepest\n |
| 0x11a60b | 7 | thanks. |
| 0x11a613 | 44 | Brother Oshtor... working with thieves and\n |
| 0x11a640 | 46 | bandits? N-No, there must be more to it than\n |
| 0x11a66f | 7 | that... |
| 0x11a677 | 47 | As Kiwru mutters to himself, poor Nekone just\n |
| 0x11a6a7 | 47 | seems to be in shock, staring straight at her\n |
| 0x11a6d7 | 48 | Oshtor spares them both a glance, then resumes\n |
| 0x11a708 | 9 | speaking. |
| 0x11a712 | 46 | Just as a person can have two identities, so\n |
| 0x11a741 | 44 | can the capital. It pays to unify opposing\n |
| 0x11a76e | 6 | sides. |
| 0x11a775 | 46 | To be sure, these men are thieves, but their\n |
| 0x11a7a4 | 48 | intent is not evil. They can reach places that\n |
| 0x11a7d5 | 9 | I cannot. |
| 0x11a7df | 46 | Ours may be opposing sides of the law, but I\n |
| 0x11a80e | 37 | believe our aspirations are the same. |
| 0x11a834 | 45 | You exaggerate, surely. It's not so lofty a\n |
| 0x11a862 | 20 | partnership as that. |
| 0x11a877 | 24 | But I'm not wrong, am I? |
| 0x11a890 | 43 | So you're saying these guys are our allies? |
| 0x11a8bc | 48 | Ah, but let's be clear on one point. Ours is a\n |
| 0x11a8ed | 47 | relationship of equals, not a chain of command. |
| 0x11a91d | 46 | Oshtor gives an assuring nod as Ougi finishes. |
| 0x11a94c | 17 | No problems here. |
| 0x11a95e | 7 | Haku... |
| 0x11a966 | 46 | C'mon, Kiwru. Sometimes you have to get your\n |
| 0x11a995 | 39 | hands dirty to get the bad guys, right? |
| 0x11a9bd | 44 | And it's not something we can all say with\n |
| 0x11a9ea | 44 | pride, but there's good and bad in everyone. |
| 0x11aa17 | 26 | I... I guess you're right. |
| 0x11aa32 | 47 | In any event, you have my end of the bargain,\n |
| 0x11aa62 | 7 | Oshtor. |
| 0x11aa6a | 44 | I appreciate your assistance in this matter. |
| 0x11aa97 | 40 | Mm... there are quite a few names with\n |
| 0x11aac0 | 37 | concerning implications on this list. |
| 0x11aae6 | 46 | If you'll be acting on this new information,\n |
| 0x11ab15 | 45 | I suggest you do so quickly. My sister will\n |
| 0x11ab43 | 12 | hardly wait. |
| 0x11ab50 | 47 | If you could stall the 'noble thief' until my\n |
| 0x11ab80 | 47 | preparations are in order, I would appreciate\n |
| 0x11abb0 | 3 | it. |
| 0x11abb4 | 50 | Surely you jest, sir. I would sooner do anything\n |
| 0x11abe7 | 41 | else than get in my beloved sister's way. |
| 0x11ac11 | 49 | Only when she runs freely, you must understand,\n |
| 0x11ac43 | 36 | does she shine with utmost radiance. |
| 0x11ac68 | 28 | Hah. I suppose you're right. |
| 0x11ac85 | 43 | Ah, yes, one more item--my sister remains\n |
| 0x11acb1 | 47 | unaware of these little chats, and I'd prefer\n |
| 0x11ace1 | 14 | she remain so. |
| 0x11acf0 | 25 | Seriously? Is that... OK? |
| 0x11ad0a | 47 | Assuredly. Were she to discover us, she would\n |
| 0x11ad3a | 47 | be outraged at my apparent alignment with the\n |
| 0x11ad6a | 6 | Court. |
| 0x11ad71 | 45 | Doesn't that mean you're going against your\n |
| 0x11ad9f | 19 | sister's wishes...? |
| 0x11adb3 | 50 | Not at all. Her discontent is born of adoration,\n |
| 0x11ade6 | 46 | you see--and she doubts even her own feelings. |
| 0x11ae15 | 35 | Ougi smiles fondly as he says this. |
| 0x11ae39 | 45 | Should you ever encounter my dear sister by\n |
| 0x11ae67 | 43 | chance--not a word of any of this to her,\n |
| 0x11ae93 | 14 | if you please. |
| 0x11aea2 | 45 | With that, Ougi disappears as quietly as he\n |
| 0x11aed0 | 8 | arrived. |
| 0x11aed9 | 47 | ...What a strange guy. Hard to figure out his\n |
| 0x11af09 | 16 | real intentions. |
| 0x11af1a | 42 | Hm. It seems he's taken a liking to you,\n |
| 0x11af45 | 9 | at least. |
| 0x11af4f | 19 | What? Him, like me? |
| 0x11af63 | 41 | Never you mind. Merely talking to myself. |
| 0x11af8d | 46 | I have added a bonus to your reward for this\n |
| 0x11afbc | 40 | job. Please, accept it with my blessing. |
| 0x11afe5 | 30 | Well, if you insist so much... |
| 0x11b004 | 47 | Oh, man, this bag has some HEFT. I'll finally\n |
| 0x11b034 | 43 | be able to rest easy with this much in my\n |
| 0x11b060 | 9 | pocket... |
| 0x11b06a | 45 | I can't help but smile at the weight of the\n |
| 0x11b098 | 45 | coin pouch, and the telltale jingling within. |
| 0x11b0c6 | 50 | First, I'll definitely hit up that candy vendor,\n |
| 0x11b0f9 | 47 | then grab some good food and booze--and after\n |
| 0x11b129 | 6 | that-- |
| 0x11b130 | 20 | I'll just take that. |
| 0x11b145 | 47 | My victory turns to ashes in my mouth as Kuon\n |
| 0x11b175 | 25 | snatches the bag from me. |
| 0x11b18f | 14 | Wh--H-Hold on! |
| 0x11b19e | 49 | Let's see... deducting food, rent, expenses for\n |
| 0x11b1d0 | 53 | previous jobs... {W680}This should suffice for your\n |
| 0x11b206 | 10 | allowance. |
| 0x11b211 | 46 | Kuon's got a tight leash on you, hasn't she,\n |
| 0x11b240 | 5 | love? |
| 0x11b246 | 8 | Shut up! |

## 8. Formato de saida EXIGIDO
Escreva `translations_17_04.json` com a forma:
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
