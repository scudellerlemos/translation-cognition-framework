# Cena ch_12_11 — pacote de traducao (227 linhas)

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
| Cohort | Organizacao | Coorte | traduzir | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
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
- `lightA02` -> `lightA02` (SISTEMA, 12_09)
- `Ukon's Cohorts` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Yessir!` -> `Sim!` (Coorte de Ukon, 12_04)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Man` -> `Hom` (Sistema, 12_04)
- `Well...` -> `Bom...` (Haku, 12_03)
- `What the--` -> `Mas que--` (Haku, 11_03)
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
| 0x42ed7 | 8 | lightA01 |
| 0x42ee1 | 8 | lightA02 |
| 0x42eea | 21 | Hahh, h-hah, hahhh... |
| 0x42f00 | 13 | Not bad, kid. |
| 0x42f0e | 22 | Hah... wheeze... Yeah? |
| 0x42f25 | 24 | I-I survived... somehow. |
| 0x42f3e | 51 | You look beat. Go rest up and leave the rest to us. |
| 0x42f72 | 54 | This is your first time doing stuff like this, yeah?\n |
| 0x42fa9 | 42 | So I'll cut you some slack just this once. |
| 0x42fd4 | 50 | All right, men, let's retrieve our kills! We can\n |
| 0x43007 | 52 | sell bits of 'em for funds, so don't miss a single\n |
| 0x4303c | 4 | leg! |
| 0x43041 | 14 | Ukon's Cohorts |
| 0x43050 | 7 | Yessir! |
| 0x43058 | 51 | Laughing in the wake of their victory, Ukon's men\n |
| 0x4308c | 29 | move to carry out his orders. |
| 0x430aa | 50 | Wow. Not a single casualty, huh? I guess this is\n |
| 0x430dd | 44 | what you can expect from seasoned experts... |
| 0x4310a | 23 | Haku. Show me your arm. |
| 0x43122 | 4 | Huh? |
| 0x43127 | 51 | Kuon comes up beside me and gently takes my hand,\n |
| 0x4315b | 19 | inspecting the arm. |
| 0x4316f | 6 | Ow...? |
| 0x43176 | 51 | Huh. I took a shallow cut on my upper arm without\n |
| 0x431aa | 9 | noticing. |
| 0x431b4 | 53 | I dunno if one of their jaws grazed me or what, but\n |
| 0x431ea | 41 | I didn't notice it until Kuon touched it. |
| 0x43214 | 15 | Hold still, OK? |
| 0x43224 | 52 | Then, without a moment's hesitation, Kuon puts her\n |
| 0x43259 | 42 | lips to the wound and sucks blood from it. |
| 0x43284 | 12 | Ech. Ptooey. |
| 0x43291 | 45 | Venom might've gotten into the wound, so...\n |
| 0x432bf | 13 | Just in case. |
| 0x432cd | 35 | Y-You didn't need to go that far... |
| 0x432f5 | 52 | My gaze locks with hers for a moment, and her eyes\n |
| 0x4332a | 23 | seem to be... laughing? |
| 0x43342 | 32 | I have a bad feeling about this. |
| 0x43363 | 16 | Sssssshhhhhwup-- |
| 0x43374 | 20 | Ow, owowowOWOWOW--!! |
| 0x43389 | 5 | Ptoo! |
| 0x4338f | 48 | Eh heh heh. A man shouldn't raise his voice at\n |
| 0x433c0 | 37 | something as small as this, you know. |
| 0x433e6 | 48 | Why, you... You did that on purpose, didn't you? |
| 0x43417 | 51 | Ignoring my accusation, Kuon skillfully applies a\n |
| 0x4344b | 42 | salve to the cut and bandages it up tight. |
| 0x43476 | 49 | There. All done. That should be enough for now,\n |
| 0x434a8 | 8 | I think. |
| 0x434b1 | 7 | *Whap!* |
| 0x434b9 | 3 | Ow! |
| 0x434bd | 47 | Then, as if to declare her work finished, she\n |
| 0x434ed | 23 | lightly pats the wound. |
| 0x43505 | 7 | Eh heh. |
| 0x4350d | 50 | A complaint brews on my tongue, but it dies when\n |
| 0x43540 | 19 | I see Kuon's smile. |
| 0x43554 | 46 | ...She looks filled with relief that I'm safe. |
| 0x43583 | 15 | Oh, yeah. Here. |
| 0x43593 | 53 | I hold out the tessen--the metal fan I'd borrowed--\n |
| 0x435c9 | 8 | to Kuon. |
| 0x435d2 | 30 | It was a lifesaver. Thank you. |
| 0x435f1 | 49 | It's fine. You should hold onto it for a while,\n |
| 0x43623 | 3 | Hm? |
| 0x43627 | 51 | It'd probably be bad if you got caught unarmed in\n |
| 0x4365b | 46 | a bad situation, so I'll let you hang onto it. |
| 0x4368a | 51 | You sure? I got the sense it's kinda important to\n |
| 0x436be | 6 | you... |
| 0x436c5 | 30 | Mhm. Precious to me, actually. |
| 0x436e4 | 43 | Seriously? If that's the case, then why...? |
| 0x43710 | 52 | Because you need it. That's why I want you to have\n |
| 0x43745 | 11 | it for now. |
| 0x43751 | 46 | OK, OK. If you're gonna keep insisting, I'll\n |
| 0x43780 | 13 | hold onto it. |
| 0x4378e | 53 | Mm. I'm only lending it to you, remember. I'll need\n |
| 0x437c4 | 17 | it back some day. |
| 0x437d6 | 51 | Most noble and valiant master! Master Haku! Didst\n |
| 0x4380a | 37 | thou witness mine eldritch magecraft? |
| 0x43830 | 7 | Urgh... |
| 0x43838 | 51 | Forsooth, such ignoble beasts are as wheat 'neath\n |
| 0x4386c | 46 | the reaperman's scythe before my spellweaving! |
| 0x4389b | 52 | It's probably because I nursed him back to health,\n |
| 0x438d0 | 52 | but Maroro seems to be... getting weirdly attached\n |
| 0x43905 | 6 | to me. |
| 0x4390c | 51 | So, kid. How was it? You were awfully anxious for\n |
| 0x43940 | 40 | how easy that job turned out to be, huh? |
| 0x43969 | 48 | Ukon calls over to me, having finished barking\n |
| 0x4399a | 24 | instructions at his men. |
| 0x439b3 | 3 | Man |
| 0x439b7 | 46 | The way you were carrying on, you got us all\n |
| 0x439e6 | 13 | anxious, too! |
| 0x439f4 | 12 | Wahahahaha!! |
| 0x43a01 | 41 | A roar of laughter rises from Ukon's men. |
| 0x43a2b | 43 | No, that was... I guess it was all just a\n |
| 0x43a57 | 17 | misunderstanding. |
| 0x43a69 | 17 | Misunderstanding? |
| 0x43a7b | 50 | Well, see--I was saved from a much bigger one of\n |
| 0x43aae | 43 | these things attacking me not too long ago. |
| 0x43ada | 48 | So when everyone started talking about gigiri,\n |
| 0x43b0b | 51 | I mistakenly assumed it was gonna be that huge one. |
| 0x43b3f | 45 | If I'd known it was just these little guys,\n |
| 0x43b6d | 37 | I wouldn't have gotten so worked up-- |
| 0x43b93 | 28 | The laughter suddenly stops. |
| 0x43bb0 | 23 | ...Did I kill the mood? |
| 0x43bc8 | 39 | ...What did you... Say that again, kid? |
| 0x43bf0 | 51 | Ukon stares at me, frozen. Not just Ukon--all his\n |
| 0x43c24 | 25 | men freeze in place, too. |
| 0x43c3e | 35 | You said you saw a much bigger one? |
| 0x43c62 | 50 | Y-yeah. It was... similar looking to these guys,\n |
| 0x43c95 | 17 | just... enormous. |
| 0x43ca7 | 50 | Did its body seem hardened? Like an outer shell,\n |
| 0x43cda | 14 | or a carapace? |
| 0x43ce9 | 7 | Well... |
| 0x43cf1 | 54 | At Ukon's questioning, I try to remember the details\n |
| 0x43d28 | 14 | of the attack. |
| 0x43d37 | 54 | Now that you mention it, yeah, its whole body seemed\n |
| 0x43d6e | 39 | to gleam black. It looked really tough. |
| 0x43d96 | 36 | And its horns were much longer, too. |
| 0x43dbb | 51 | Cripes. If that's the case, then we're in serious\n |
| 0x43def | 7 | troub-- |
| 0x43df7 | 48 | Then, it happens before I can blink. A massive\n |
| 0x43e28 | 50 | shape bursts from the bushes, scything toward us-- |
| 0x43e5b | 54 | There isn't any time to react as it blurs past a man\n |
| 0x43e92 | 49 | nearby, sending something flying up into the air. |
| 0x43ec4 | 20 | Krrrkkkk krk krk--!! |
| 0x43ed9 | 32 | Ah, it was something like this-- |
| 0x43efa | 7 | *THUMP* |
| 0x43f02 | 8 | What ho? |
| 0x43f0b | 52 | The flying object lands solidly in Maroro's hands,\n |
| 0x43f40 | 27 | catching him by surprise... |
| 0x43f5c | 54 | It has enough time to look at him and flap its mouth\n |
| 0x43f93 | 43 | in soundless anguish before it falls still. |
| 0x43fbf | 15 | HYEEEEEEEEEEE!? |
| 0x43fcf | 53 | Maroro's piercing scream echoes through the clearing. |
| 0x44005 | 15 | AH--UAAAAAAHH!! |
| 0x44015 | 49 | At the sound of Maroro's cry, the men around us\n |
| 0x44047 | 36 | scramble, fleeing in all directions. |
| 0x4406c | 10 | What the-- |
| 0x44077 | 44 | Gah! There are more little ones coming, too! |
| 0x440a4 | 17 | What's happening? |
| 0x440b6 | 50 | Keep your distance! Fall back and regroup--we'll\n |
| 0x440e9 | 22 | attack it all at once! |
| 0x44100 | 50 | Several of the men nearby take up arms at Ukon's\n |
| 0x44133 | 10 | command... |
| 0x4413e | 51 | But more and more gigiri swarm out of the shadows\n |
| 0x44172 | 43 | nearby, pouring forth in a ceaseless horde. |
| 0x4419e | 33 | B-Be careful, they're--GYAAAAHH!! |
| 0x441c0 | 51 | Before anyone can ready their weapons, the gigiri\n |
| 0x441f4 | 37 | lay into Ukon's men with a vengeance. |
| 0x4421a | 5 | Haku! |
| 0x44220 | 6 | Hngh-- |
| 0x44227 | 49 | At Kuon's call, I snap out of my confused daze,\n |
| 0x44259 | 41 | quickly crushing the gigiri attacking me. |
| 0x44283 | 29 | Thanks. You're a lifesaver... |
| 0x442a1 | 47 | Nnhh. No wonder I thought our stories weren't\n |
| 0x442d1 | 45 | meshing. You were talking about this thing... |
| 0x442ff | 32 | Kuon sighs, rubbing her temples. |
| 0x44320 | 27 | Krrrrrkkkkk krk krk krk--!! |
| 0x4433c | 25 | This is... bad, isn't it? |
| 0x44356 | 12 | RRRAAAAHHH!! |
| 0x44363 | 54 | Fall back! Carry the wounded if you can still stand!\n |
| 0x4439a | 5 | MOVE! |
| 0x443a0 | 41 | Ukon mows down another gigiri, carrying\n |
| 0x443ca | 43 | unconscious men over each of his shoulders. |
| 0x443f6 | 50 | You two! What are you doing, standing there like\n |
| 0x44429 | 18 | that!? Get moving! |
| 0x4443c | 8 | Y-Yeah-- |
| 0x44445 | 53 | With a knot of dread in my stomach, I move to obey,\n |
| 0x4447b | 23 | trying my best to flee. |
| 0x44493 | 9 | I... huh? |
| 0x4449d | 51 | But I can't move. A heavy weight pins my legs down. |
| 0x444d1 | 30 | Bwuh... hyee... hyeeeeeee...!! |
| 0x444f0 | 42 | Wh--What are you clinging to my legs for!? |
| 0x4451b | 18 | Aaaahh--awawawah!! |
| 0x4452e | 44 | Damn it, I can't move! Hurry up and get on\n |
| 0x4455b | 18 | your own two feet! |
| 0x4456e | 52 | Thou m-mayst well ask the very trees to uproot and\n |
| 0x445a3 | 41 | spring legs! I-I'faith, I c-cannot move-- |
| 0x445cd | 49 | And I can't move because you're clinging to me!\n |
| 0x445ff | 16 | Come on, get up! |
| 0x44610 | 53 | I try to pull Maroro up to make him stand, but he's\n |
| 0x44646 | 39 | clinging so tightly, I can't budge him. |
| 0x4466e | 51 | N-No! Alack and cry thunder, but abandon not poor\n |
| 0x446a2 | 29 | Maroro to so pitiable an end! |
| 0x446c0 | 50 | That's why I'm telling you to stand! Do you WANT\n |
| 0x446f3 | 8 | to die!? |
| 0x446fc | 49 | Damn it, I can't move with him on me like this... |
| 0x4472e | 51 | What are you playing at, kid? We need to move, NOW! |
| 0x44762 | 31 | DOES IT LOOK LIKE I'M PLAYING!? |
| 0x44782 | 51 | As we continue to waste precious time, the gigiri\n |
| 0x447b6 | 23 | swarm surges forward... |
| 0x447ce | 48 | And beyond them, the hulking, monstrous gigiri\n |
| 0x447ff | 51 | gorges itself on the severed head of that poor man. |
| 0x44833 | 24 | Uh-oh. We're surrounded. |
| 0x4484c | 54 | You seem awfully calm. You have a plan of some kind,\n |
| 0x44883 | 11 | I'm hoping? |
| 0x4488f | 51 | I wouldn't call it a plan, but I can probably get\n |
| 0x448c3 | 11 | myself out. |
| 0x448cf | 15 | What, JUST you? |
| 0x448df | 14 | Yeah, just me. |
| 0x448ee | 29 | And where does that leave me? |
| 0x4490c | 37 | ...Well, if this isn't a fine pickle. |
| 0x44932 | 52 | Hey, you're not gonna run off and abandon me, right? |
| 0x44967 | 51 | Ahahaha, don't worry. If it were so easy to drive\n |
| 0x4499b | 49 | me off, I would've abandoned you a long time ago. |
| 0x449cd | 33 | But... tch. What should we do...? |
| 0x449ef | 22 | So, this is it, huh... |
| 0x44a06 | 31 | Bah. I guess there's no choice. |
| 0x44a26 | 51 | Kid. Missy. I hate to ask this of you, but I need\n |
| 0x44a5a | 41 | you to get the others far away from here. |
| 0x44a84 | 41 | Ukon's voice carries an unusual weight... |
| 0x44aae | 26 | What is he planning to do? |
| 0x44ac9 | 22 | ...Just wait a moment. |
| 0x44ae0 | 21 | Kuon steps forward... |
| 0x44af6 | 53 | This is my last one, so I'd wanted to save it, but... |
| 0x44b2c | 48 | She takes the small tube hanging from her waist. |
| 0x44b5d | 52 | Ready, everyone? I'm going to open the way for us.\n |
| 0x44b92 | 49 | When I give the signal, cover your eyes and ears. |
| 0x44bc4 | 48 | And then run as fast as your legs can carry you. |
| 0x44bf5 | 34 | Oh, is this what she used when...? |
| 0x44c18 | 28 | I see. A flash grenade, huh? |
| 0x44c35 | 47 | Wh-What manner of weapon art thou making ready? |
| 0x44c65 | 21 | Here goes. Three...\n |
| 0x44c7b | 8 | Two...\n |
| 0x44c84 | 8 | One...!! |
| 0x44c8d | 51 | Kuon yanks something from the flash grenade, then\n |
| 0x44cc1 | 31 | hurls it with all her strength! |
| 0x44ce1 | 25 | All right! Everyone, run! |
| 0x44cfb | 49 | GYEH!? Wh-What infernal light blazeth mine eyes!? |
| 0x44d2d | 39 | Urgh, I almost want to kick him down... |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_11.json` com a forma:
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
