# Cena ch_12_17 — pacote de traducao (123 linhas)

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
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acento→ASCII) 
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| amamunii | Comida | amamunii | manter_original | none |
| Cohort | Organizacao | Coorte | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Ukon | Personagem | Ukon | manter_original | major |
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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Ukon** (major): Traduza as falas de/sobre Ukon como o personagem 'Ukon' por si so. NAO insinue outra identidade, patente oculta ou disfarce. Mantenha qualquer ambiguidade do original.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Phew...` -> `Ufa...` (Haku, 12_16)
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Hey, kid, that cutie's gonna be disappointed with\n` -> `Ei, garoto, essa mocinha vai se decepcionar com\n` (Ukon, 12_07)
- `you if you talk like that.` -> `você se falar assim.` (Ukon, 12_07)
- `That's right! A real man sucks it up and goes for\n` -> `É isso! Um homem de verdade aguentaa firme e vai até\n` (Ukon, 12_07)
- `broke!` -> `o fim!` (Ukon, 12_07)
- `but...` -> `mas...` (Kuon, 12_16)
- `I see.` -> `Entendo.` (Kuon, root)
- `All right.` -> `Tudo bem.` (Haku, 12_08)
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

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x51932 | 50 | The party carries on well past midnight, showing\n |
| 0x51965 | 28 | few signs of slowing down... |
| 0x51982 | 50 | I came outside to cool off a bit in the night air. |
| 0x519b5 | 41 | A breeze kicks up, caressing my cheeks... |
| 0x519df | 7 | Phew... |
| 0x519e7 | 53 | The cool air against my body feels nice after being\n |
| 0x51a1d | 31 | inside the hot inn for so long. |
| 0x51a3d | 50 | Behind me, warm light and cheerful voices filter\n |
| 0x51a70 | 21 | out from the party... |
| 0x51a86 | 47 | Pray lend me your ears, friends! Marvel as I,\n |
| 0x51ab6 | 52 | master of impressions, do impersonate our dear Ukon! |
| 0x51aeb | 24 | A raucous cheer goes up. |
| 0x51b04 | 50 | Seems Maroro is giving a performance of some kind. |
| 0x51b37 | 52 | A relaxed atmosphere is finally taking hold, after\n |
| 0x51b6c | 29 | everything that's happened... |
| 0x51b8a | 24 | Everyone seems cheerful. |
| 0x51ba3 | 17 | ...Cheerful, huh. |
| 0x51bb5 | 54 | The faces of those two men who'd spoken to me during\n |
| 0x51bec | 38 | the trip rise unbidden in my thoughts. |
| 0x51c13 | 13 | Ukon's Cohort |
| 0x51c21 | 51 | Hey, kid, that cutie's gonna be disappointed with\n |
| 0x51c55 | 26 | you if you talk like that. |
| 0x51c70 | 51 | That's right! A real man sucks it up and goes for\n |
| 0x51ca4 | 6 | broke! |
| 0x51cab | 44 | And then they'd laughed merrily with their\n |
| 0x51cd8 | 9 | comrades. |
| 0x51ce2 | 6 | But... |
| 0x51ce9 | 49 | Those two were nowhere to be seen in the dining\n |
| 0x51d1b | 15 | hall, just now. |
| 0x51d2b | 53 | They'll never be able to laugh or share drinks with\n |
| 0x51d61 | 23 | their comrades again... |
| 0x51d79 | 52 | And yet everyone inside is able to laugh and cheer\n |
| 0x51dae | 37 | without a care in the world, somehow. |
| 0x51dd4 | 49 | Nobody seems to give any thought toward mourning. |
| 0x51e06 | 38 | Even Kuon doesn't seem too bothered... |
| 0x51e2d | 6 | And... |
| 0x51e34 | 50 | Even after that entire harrowing ordeal, I don't\n |
| 0x51e67 | 46 | feel like I've been terribly affected, either. |
| 0x51e96 | 36 | Hm? What're you doing out here, kid? |
| 0x51ebb | 49 | I turn to the source of the voice and find Ukon\n |
| 0x51eed | 49 | approaching me with a bottle of sake in one hand. |
| 0x51f1f | 40 | Came out to get a bit of fresh air, huh? |
| 0x51f48 | 26 | Something like that, yeah. |
| 0x51f63 | 43 | I see. Hey, care to walk with me for a bit? |
| 0x51f8f | 42 | I accompany Ukon down the darkened path... |
| 0x51fba | 53 | We walk by moonlight, casting long shadows into the\n |
| 0x51ff0 | 25 | already dusky blue night. |
| 0x5200a | 52 | Hey, kid. Something I've been meaning to ask you--\n |
| 0x5203f | 45 | That missy you're traveling with. Who is she? |
| 0x5206d | 14 | You mean Kuon? |
| 0x5207c | 41 | Yeah. I figured you might know something. |
| 0x520a6 | 29 | Why're you interested in her? |
| 0x520c4 | 50 | I wonder myself, honestly. I s'pose I'm just the\n |
| 0x520f7 | 13 | curious type. |
| 0x52105 | 36 | You're not falling for her, are you? |
| 0x5212a | 48 | She's certainly a beautiful woman, but I'm not\n |
| 0x5215b | 45 | attracted to her in the way you're probably\n |
| 0x52189 | 9 | thinking. |
| 0x52193 | 41 | Besides, hitting on her would be a bit... |
| 0x521bd | 6 | A bit? |
| 0x521c4 | 52 | Eh, it's nothing. She certainly is an amazing woman. |
| 0x521f9 | 30 | Her APPETITE'S amazing, maybe. |
| 0x52218 | 50 | Ha! No, I don't mean that, but you're not wrong.\n |
| 0x5224b | 51 | I meant more her aura. The way she carries herself. |
| 0x5227f | 50 | That fearlessness, the lack of hesitation in the\n |
| 0x522b2 | 36 | face of a life-or-death situation... |
| 0x522d7 | 45 | Makes you wonder what kind of life she's led. |
| 0x52305 | 34 | At that, Ukon's voice grows quiet. |
| 0x5232c | 51 | Now that he mentions it, I really don't know much\n |
| 0x52360 | 11 | about Kuon. |
| 0x5236c | 51 | I owe her for saving my life, and I don't want to\n |
| 0x523a0 | 46 | pry, so I haven't really asked about her past. |
| 0x523cf | 53 | ...You dunno anything, huh. Well, you haven't known\n |
| 0x52405 | 40 | her very long. Guess it can't be helped. |
| 0x5242e | 38 | She calls herself a mere apothecary... |
| 0x52455 | 53 | When she said that, I was about to blurt out "where\n |
| 0x5248b | 46 | in the world are there apothecaries like YOU?" |
| 0x524ba | 34 | Before long, Ukon comes to a stop. |
| 0x524dd | 16 | ...Where are we? |
| 0x524ee | 52 | We're a small distance outside the village. Large,\n |
| 0x52523 | 44 | standing stones sit arranged in even rows... |
| 0x52550 | 23 | Is this... a graveyard? |
| 0x52568 | 49 | Sorry for making you come to such a grim place.\n |
| 0x5259a | 50 | Couldn't rest easy without bringing 'em some sake. |
| 0x525cd | 47 | Ukon stands in front of one particular stone,\n |
| 0x525fd | 38 | decorated with multicolored ornaments. |
| 0x52624 | 53 | Offerings of flowers, food, and liquor sit arranged\n |
| 0x5265a | 10 | around it. |
| 0x52665 | 52 | ...Sorry for being so late. Guess I ended up being\n |
| 0x5269a | 15 | the last one... |
| 0x526aa | 51 | Ukon mumbles under his breath, as though speaking\n |
| 0x526de | 34 | to the gravestone in front of him. |
| 0x52701 | 49 | So these offerings were left by the rest of the\n |
| 0x52733 | 11 | company...? |
| 0x5273f | 52 | Seems the others came to pay their respects before\n |
| 0x52774 | 9 | Ukon did. |
| 0x5277e | 47 | Not everyone's so good with this macabre stuff. |
| 0x527ae | 51 | When we see people off, we do it with a smile and\n |
| 0x527e2 | 48 | a cheer. That's what we all decided... together. |
| 0x52813 | 6 | I see. |
| 0x5281a | 49 | ...Yeah. There's no way it wasn't difficult for\n |
| 0x5284c | 31 | him, losing so many comrades... |
| 0x5286c | 49 | Nobody knows when or how death can come for us.\n |
| 0x5289e | 47 | If we die in battle, our bodies might be left\n |
| 0x528ce | 9 | behind... |
| 0x528d8 | 45 | But I'm glad we can at least offer the dead\n |
| 0x52906 | 17 | proper memorials. |
| 0x52918 | 42 | Ukon sinks to a knee, muttering in prayer. |
| 0x52943 | 52 | Following his lead, I kneel beside him and offer a\n |
| 0x52978 | 14 | silent prayer. |
| 0x52987 | 53 | I witness this end to your time in our world. Rest,\n |
| 0x529bd | 47 | now, that we may drink together in Kotuahamuru. |
| 0x529ed | 8 | ...Ukon? |
| 0x529f6 | 10 | All right. |
| 0x52a01 | 43 | Let's head back and get plastered, eh, kid? |
| 0x52a2d | 12 | Huh? Yeah... |
| 0x52a3a | 51 | Puzzled, I follow after Ukon as he takes off down\n |
| 0x52a6e | 15 | the path again. |
| 0x52a7e | 45 | ...What was that strange feeling just now...? |
| 0x52aac | 36 | As I turn away from the graveyard... |
| 0x52ad1 | 48 | ...I can't help but notice an amamunii amongst\n |
| 0x52b02 | 48 | the offerings, stuffed too full to be eaten in\n |
| 0x52b33 | 9 | one bite. |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_17.json` com a forma:
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
