# Cena ch_12_06 — pacote de traducao (103 linhas)

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
| Gigiri | Criatura | Gigiri | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `happen?` -> `alguma coisa?` (Haku, 11_11)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `What?` -> `Que?` (Haku, 12_02)
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
- Homem: `Inside your dream.` -> `No seu sonho.`
- Homem: `We have enchanted you with a spell that will help\n` -> `Lançamos sobre você um feitiço que irá ajudá-lo\n`
- Homem: `you become stronger in sleep, as requested, Master.` -> `a ficar mais forte enquanto dorme, como pedido, Mestre.`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x36f09 | 12 | Yaaaawn...\n |
| 0x36f16 | 9 | Sleepy... |
| 0x36f20 | 22 | Hmhm. Big yawn, there. |
| 0x36f37 | 50 | Since our plans were to leave for the capital at\n |
| 0x36f6a | 43 | dawn, I woke up before the sun even rose... |
| 0x36f96 | 16 | Mmnhh... aahh... |
| 0x36fa7 | 54 | But man, I'm liable to fall asleep right here at the\n |
| 0x36fde | 49 | table. I didn't rest at all after that commotion. |
| 0x37010 | 52 | We're gonna have to walk for a few days, Haku. You\n |
| 0x37045 | 46 | should eat up, or you'll tire out on the road. |
| 0x37074 | 15 | *Nomf, hromf--* |
| 0x37084 | 54 | Kuon, of course, makes short work of the mountain of\n |
| 0x370bb | 43 | food before her--no match for her appetite. |
| 0x370e7 | 52 | ...Even so, I just got up. I don't have much of an\n |
| 0x3711c | 21 | appetite myself, yet. |
| 0x37132 | 35 | Hey, you kids are up awfully early. |
| 0x37156 | 50 | As I reply to Kuon, the man who'd called himself\n |
| 0x37189 | 19 | Ukon approaches us. |
| 0x3719d | 51 | Good morning. You're up early, too. Did something\n |
| 0x371d1 | 7 | happen? |
| 0x371d9 | 53 | Oh, it's nothing major. The village chieftain hired\n |
| 0x3720f | 37 | us to hunt down that swarm of gigiri. |
| 0x37235 | 52 | If we leave 'em like they are, they'll just attack\n |
| 0x3726a | 44 | folks again. The chief wants something done. |
| 0x37297 | 53 | He said he'll compensate us fairly for the work, so\n |
| 0x372cd | 46 | I accepted, circumstances being what they are. |
| 0x372fc | 36 | The others oughta be waking up soon. |
| 0x37321 | 18 | Hunt down... that? |
| 0x37334 | 29 | Hey, can I ask you something? |
| 0x37352 | 3 | Hm? |
| 0x37356 | 49 | You said "hunt down." You're really planning on\n |
| 0x37388 | 37 | going up against a monster like that? |
| 0x373ae | 53 | Huh? Well, yeah, that's the plan. Not sure what you\n |
| 0x373e4 | 5 | mean. |
| 0x373ea | 52 | Isn't it dangerous, even for a company like yours?\n |
| 0x3741f | 39 | Facing off with a creature like that... |
| 0x37447 | 53 | Not at all. I mean, sure, there's some danger since\n |
| 0x3747d | 51 | they're venomous and there's a bunch of 'em, but... |
| 0x374b1 | 52 | They're not a big threat once you isolate 'em, and\n |
| 0x374e6 | 32 | my men are all skilled fighters. |
| 0x37507 | 36 | It's trivial work, really. No sweat. |
| 0x3752c | 54 | Wh--Did he just call that thing "trivial"? Just ONE,\n |
| 0x37563 | 29 | let alone a whole horde, is-- |
| 0x37581 | 52 | Uh... Haku? I don't know how to tell you this, but\n |
| 0x375b6 | 51 | any reasonably strong person can probably kill one. |
| 0x375ea | 5 | What? |
| 0x375f0 | 20 | I mean... I'm sorry? |
| 0x37605 | 51 | T-Take down that monster? What sort of people ARE\n |
| 0x37639 | 9 | you guys? |
| 0x37643 | 55 | The fact remains, their venom is a legitimate threat,\n |
| 0x3767b | 46 | and the sudden nature of the job means we're\n |
| 0x376aa | 14 | underprepared. |
| 0x376b9 | 41 | Ukon sits and leans forward on his elbow. |
| 0x376e3 | 50 | With that said, I'm impressed by your apothecary\n |
| 0x37716 | 48 | chops. What would you say to joining up with us? |
| 0x3774b | 28 | Kuon's apothecary skills...? |
| 0x37768 | 53 | I'll pay you triple what the grunts make. How about\n |
| 0x3779e | 22 | it? Sound fair to you? |
| 0x377b5 | 54 | Kuon chews her bite of amamunii slowly, mulling over\n |
| 0x377ec | 10 | the offer. |
| 0x377f7 | 43 | If that's the case... Yes, let's cooperate. |
| 0x37823 | 17 | So you'll accept? |
| 0x37835 | 51 | Even if Ukon's warriors are skilled, that doesn't\n |
| 0x37869 | 12 | mean Kuon... |
| 0x37876 | 52 | ...No, she'll be all right. I can't really imagine\n |
| 0x378ab | 19 | her falling behind. |
| 0x378bf | 48 | Her constitution isn't exactly something I can\n |
| 0x378f0 | 16 | imitate, though. |
| 0x37901 | 28 | H-Hold on, did you say "us"? |
| 0x3791e | 29 | Is something wrong with that? |
| 0x3793c | 54 | Don't you "is something wrong" me! Are you trying to\n |
| 0x37973 | 14 | get me killed? |
| 0x37982 | 51 | I don't stand a chance against a monster like that! |
| 0x379b6 | 48 | It'll be all right. Even you should be able to\n |
| 0x379e7 | 27 | manage if you get attacked. |
| 0x37a03 | 32 | No. No way. Nope. Not happening. |
| 0x37a24 | 54 | That's my condition for accepting. You have to bring\n |
| 0x37a5b | 11 | Haku along. |
| 0x37a67 | 42 | Would you listen to me for just a second!? |
| 0x37a92 | 53 | The kid too, huh? Are you sure? He doesn't seem too\n |
| 0x37ac8 | 20 | wild about the idea. |
| 0x37add | 54 | He can come, but just because you're with us doesn't\n |
| 0x37b14 | 51 | guarantee his safety, understand? He's gotta pull\n |
| 0x37b48 | 15 | his own weight. |
| 0x37b58 | 23 | Mhm. I don't mind that. |
| 0x37b70 | 47 | Mind it, would you? Because I DIE if you don't! |
| 0x37ba0 | 51 | Haku, it's probably safe to say the amnesia means\n |
| 0x37bd4 | 47 | you don't really know the dangers of the world. |
| 0x37c04 | 53 | And it's also probably fair to say you haven't done\n |
| 0x37c3a | 41 | a whole lot of strenuous activity so far. |
| 0x37c64 | 51 | If you go on like you have been, you really MIGHT\n |
| 0x37c98 | 47 | lose your life in a future dangerous situation. |
| 0x37cc8 | 54 | I'd rather you experience the strenuous stuff that's\n |
| 0x37cff | 31 | manageable now, to prepare you. |
| 0x37d1f | 50 | But if you absolutely won't go, I won't force you. |
| 0x37d52 | 6 | Urk... |
| 0x37d59 | 51 | Won't pressure me? It's not like I have a choice,\n |
| 0x37d8d | 29 | when she says it like that... |
| 0x37dab | 18 | So, what'll it be? |
| 0x37dbe | 39 | All right, all right. I'll go with you. |
| 0x37de6 | 23 | Good! Then that's that. |
| 0x37dfe | 32 | Kuon seems strangely cheerful... |
| 0x37e1f | 31 | She's enjoying this, isn't she? |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_06.json` com a forma:
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
