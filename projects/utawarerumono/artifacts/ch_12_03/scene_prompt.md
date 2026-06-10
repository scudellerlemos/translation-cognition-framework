# Cena ch_12_03 — pacote de traducao (408 linhas)

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
| amam | Item | amam | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |

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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `right?` -> `né?` (Kuon, root)
- `*THUNK*` -> `*TUM*` (Haku, 11_10)
- `Innkeeper` -> `Estalajadeira` (rotulo, 11_06)
- `There's help needed, hm... cutting stones at the\n` -> `Precisa-se de ajuda, hm... corte de pedras na\n` (Sistema, 12_02)
- `quarry, and hauling fresh lumber. How's that sound?` -> `pedreira, e transporte de madeira. Que tal?` (Sistema, 12_02)
- `Is something wrong?` -> `Algum problema?` (Kuon, 11_06)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Now...` -> `Agora...` (Kuon, root)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Ah, I see.` -> `Ah, saquei.` (Haku, 11_10)
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
| 0x2a495 | 49 | Hm. It really isn't moving... It must be broken\n |
| 0x2a4c7 | 16 | after all, then. |
| 0x2a4d8 | 53 | Having given up trying to get the mill moving, Kuon\n |
| 0x2a50e | 41 | mutters to herself, peering at the gears. |
| 0x2a538 | 53 | Ah, so this thing's gotta be the buhrstone mill for\n |
| 0x2a56e | 40 | grinding... And this must be the mortar. |
| 0x2a597 | 51 | I think I get it. The waterwheel rotates the rod,\n |
| 0x2a5cb | 43 | which turns the gears, which move the mill. |
| 0x2a5f7 | 47 | Seems like it's busted at the moment, though.\n |
| 0x2a627 | 37 | How am I supposed to move this thing? |
| 0x2a64d | 53 | That's just how the pieces fall, I guess. Haku, I'm\n |
| 0x2a683 | 47 | going to have you turn the amam-grinding stone. |
| 0x2a6b3 | 23 | Turn? Wait, you mean... |
| 0x2a6cb | 50 | I'll show you. First, take amam from the bag and\n |
| 0x2a6fe | 24 | pour it into the mill... |
| 0x2a717 | 48 | Kuon opens one of the sacks lying piled in the\n |
| 0x2a748 | 49 | corner, pouring its contents out into the mortar. |
| 0x2a77a | 30 | And then... you turn the mill. |
| 0x2a799 | 52 | She grabs ahold of a handle jutting from the round\n |
| 0x2a7ce | 50 | millstone and gives a small, almost casual push... |
| 0x2a801 | 12 | *GRRRRNGGKK* |
| 0x2a80e | 54 | The mill spins with unreasonable force for that tiny\n |
| 0x2a845 | 49 | push, grinding and crushing the amam into powder. |
| 0x2a877 | 52 | Ah, maybe I put my back into that one a little much. |
| 0x2a8ac | 52 | A little much!? Wait, is something b--is that SMOKE? |
| 0x2a8e1 | 47 | Lo and behold, the friction of all that force\n |
| 0x2a911 | 43 | created smoke, gently rising from the mill. |
| 0x2a93d | 27 | Give it a try, in any case. |
| 0x2a959 | 54 | Like hell I'll be able to do that! Where do you even\n |
| 0x2a990 | 41 | get the strength for something like this? |
| 0x2a9ba | 49 | But if I recall... You're supposed to walk in a\n |
| 0x2a9ec | 52 | circle with the handle to get the mill going, right? |
| 0x2aa21 | 53 | I may not be able to do it like her, but getting it\n |
| 0x2aa57 | 39 | spinning should be an easy enough task. |
| 0x2aa7f | 46 | I'd prefer not to work, but I should show my\n |
| 0x2aaae | 47 | gratitude. I take the handle and begin to push. |
| 0x2aade | 10 | Alley-oop. |
| 0x2aae9 | 12 | *Grrrrrk*... |
| 0x2aaf6 | 52 | Not exactly light, but... I think I can handle this. |
| 0x2ab2b | 51 | I mean--how useless would I be if I couldn't? She\n |
| 0x2ab5f | 46 | can't be expecting me to screw this up, right? |
| 0x2ab8e | 52 | Excellent. You shouldn't have any problems, I think. |
| 0x2abc3 | 50 | I have some errands to tend to, so you'll be all\n |
| 0x2abf6 | 45 | right if I leave you alone here, right, Haku? |
| 0x2ac24 | 52 | Yeah. I just need to grind this stuff into powder,\n |
| 0x2ac59 | 6 | right? |
| 0x2ac60 | 35 | Uh huh. I'll leave you to it, then. |
| 0x2ac84 | 39 | Welp. Might as well get this over with. |
| 0x2acac | 27 | Push, push, puuuuuuuuush... |
| 0x2acc8 | 20 | *Grrrrrrrrrrrrrk*... |
| 0x2acdd | 31 | Spin, spin, keep on spinning... |
| 0x2acfd | 24 | *Grrrrrrrrrrrrrrrrrk*... |
| 0x2ad16 | 50 | Don't get me wrong; I'm glad it's not strenuous,\n |
| 0x2ad49 | 44 | but man, I'm bored. This is monotonous work. |
| 0x2ad76 | 25 | *Grrrrrrrrrrrrrrrrrrk*... |
| 0x2ad90 | 53 | Not to mention this thing is barely putting out any\n |
| 0x2adc6 | 49 | powder at all. It took no time at all for Kuon... |
| 0x2adf8 | 52 | This is gonna take forever, at this rate. I should\n |
| 0x2ae2d | 17 | pick up the pace. |
| 0x2ae3f | 24 | *Grrrrrrrrrrrrrrrrk...!* |
| 0x2ae58 | 23 | Phew, first bag down... |
| 0x2ae74 | 29 | Well... Time to take a break. |
| 0x2ae92 | 12 | Hup--whew... |
| 0x2ae9f | 53 | Geez. All that for ONE bag! All that work, and I've\n |
| 0x2aed5 | 45 | only finished the first little bit!? Come on! |
| 0x2af03 | 48 | Gah. There's no way I'm getting all this done.\n |
| 0x2af34 | 45 | I was way too optimistic. What am I gonna do? |
| 0x2af62 | 43 | My legs have turned to jelly, my feet are\n |
| 0x2af8e | 40 | blistering, the boredom is killing me... |
| 0x2afb7 | 51 | Why the hell do I need to turn this thing all day\n |
| 0x2afeb | 40 | like I'm livestock or something, anyway? |
| 0x2b014 | 49 | I wouldn't even have to do this if they'd fixed\n |
| 0x2b046 | 35 | their damn mill in the first place. |
| 0x2b06a | 53 | Laying on the ground, I glance toward the system of\n |
| 0x2b0a0 | 28 | gears connected to the mill. |
| 0x2b0bd | 50 | They said something like... the repairman hasn't\n |
| 0x2b0f0 | 50 | come yet, but it's not like mills are complicated. |
| 0x2b123 | 49 | If someone had the mind to do it, I'm sure they\n |
| 0x2b155 | 10 | could--eh? |
| 0x2b160 | 49 | That's it! All I've gotta do is fix this thing.\n |
| 0x2b192 | 44 | Why didn't I think of that? It's so obvious! |
| 0x2b1bf | 46 | I pick myself up and set about examining the\n |
| 0x2b1ee | 22 | structure of the mill. |
| 0x2b205 | 48 | Carefully, I scrutinize each part in sequence,\n |
| 0x2b236 | 43 | finally coming to a gear that feels... off. |
| 0x2b262 | 53 | ...Yeah, this is the one. The gear for the grinding\n |
| 0x2b298 | 53 | stone cracked and got stuck. No wonder it won't move. |
| 0x2b2ce | 51 | Now, what to do? If the gear itself is broken, is\n |
| 0x2b302 | 27 | there anything I can... hm? |
| 0x2b31e | 45 | This is... Ah, now that I look closely, the\n |
| 0x2b34c | 45 | mechanism for the mortar is exactly the same. |
| 0x2b37a | 51 | If that's the case, can I just pull a gear that's\n |
| 0x2b3ae | 47 | not in use from another part of the machine...? |
| 0x2b3de | 9 | *Crrk*... |
| 0x2b3e8 | 49 | If I drop that right in here, it should spin...\n |
| 0x2b41a | 9 | Probably. |
| 0x2b424 | 7 | *THUNK* |
| 0x2b42c | 49 | I slide off the broken gear and replace it with\n |
| 0x2b45e | 29 | another one of the same size. |
| 0x2b47c | 47 | ...I know this was my idea, but wow. I wasn't\n |
| 0x2b4ac | 33 | expecting it to fit so perfectly. |
| 0x2b4ce | 53 | The gear from the other mechanism is just the right\n |
| 0x2b504 | 43 | size. Did no one else really think of this? |
| 0x2b530 | 45 | Whatever. No way to know until I test it out. |
| 0x2b55e | 52 | Moving over to the window, I find the rope holding\n |
| 0x2b593 | 37 | the waterwheel in place and untie it. |
| 0x2b5b9 | 10 | *Grrrk*... |
| 0x2b5c4 | 11 | *Grrk*...\n |
| 0x2b5d0 | 9 | *CLANK*\n |
| 0x2b5da | 10 | *Groan*... |
| 0x2b5e5 | 50 | With a loud sound, the axle in the center slowly\n |
| 0x2b618 | 19 | begins to rotate... |
| 0x2b62c | 53 | The gears follow suit, and finally, the mill starts\n |
| 0x2b662 | 16 | to move as well. |
| 0x2b673 | 19 | *Gr-Grrrrrrrrrk*... |
| 0x2b687 | 41 | Oh... Hey, all right, we've got movement. |
| 0x2b6b1 | 48 | The amam inside the mill falls out in a steady\n |
| 0x2b6e2 | 22 | stream of fine powder. |
| 0x2b6f9 | 52 | Yes! Success! Now all I have to do is sit and reap\n |
| 0x2b72e | 12 | the rewards. |
| 0x2b73b | 50 | I sit back down on the floor and kick my feet up\n |
| 0x2b76e | 38 | for a nice, long, well-deserved break. |
| 0x2b795 | 15 | *Grrrrrrrrk*... |
| 0x2b7a5 | 47 | The mill continually spins before me, quickly\n |
| 0x2b7d5 | 46 | overtaking my efforts from before. It's amam\n |
| 0x2b804 | 12 | powder city. |
| 0x2b811 | 53 | I figure if it keeps this pace up, I should be done\n |
| 0x2b847 | 13 | by nightfall. |
| 0x2b855 | 45 | Really, I should have done this from the st-- |
| 0x2b883 | 45 | Footsteps from outside interrupt my thoughts. |
| 0x2b8b4 | 52 | Acting on reflex and instinct, I quickly stand and\n |
| 0x2b8e9 | 17 | move to the mill. |
| 0x2b8fb | 41 | Haku, everything going all right in here? |
| 0x2b925 | 51 | Just as I reach the mill, Kuon pokes her head in,\n |
| 0x2b959 | 28 | holding a tray in her hands. |
| 0x2b976 | 31 | Ungh!? O-Oh, yeah. Doing great. |
| 0x2b996 | 53 | For some reason, I find myself with my hands around\n |
| 0x2b9cc | 47 | the handle, "pushing" the freely rotating mill. |
| 0x2b9fc | 52 | Why am I acting like a kid trying to hide shirking\n |
| 0x2ba31 | 30 | his homework from his parents? |
| 0x2ba50 | 43 | Ahaha, looks like it's going well, I guess. |
| 0x2ba7c | 15 | Well, this is-- |
| 0x2ba8c | 17 | ...Wait. Hold up. |
| 0x2ba9e | 53 | I catch myself just as I'm about to explain to Kuon\n |
| 0x2bad4 | 44 | how I swapped in an auxiliary gear, pausing. |
| 0x2bb01 | 49 | If the mill is repaired, there's no point to me\n |
| 0x2bb33 | 27 | spinning this stupid thing. |
| 0x2bb4f | 50 | Which means I wouldn't have to be here, and Kuon\n |
| 0x2bb82 | 48 | would just find another job for me to do, right? |
| 0x2bbb3 | 51 | Thinking back, I recall the conversation Kuon had\n |
| 0x2bbe7 | 21 | with the innkeeper... |
| 0x2bbfd | 9 | Innkeeper |
| 0x2bc07 | 50 | There's help needed, hm... cutting stones at the\n |
| 0x2bc3a | 51 | quarry, and hauling fresh lumber. How's that sound? |
| 0x2bc6e | 50 | No, no, no. No more. I've had my fill. I reject,\n |
| 0x2bca1 | 35 | I renounce, I REFUSE this "work"... |
| 0x2bcc5 | 52 | Guess there's no choice. Kinda sucks lying to her,\n |
| 0x2bcfa | 42 | but I'm gonna pretend I'm working for now. |
| 0x2bd25 | 53 | Kuon doesn't seem to catch on, for she steps inside\n |
| 0x2bd5b | 48 | and sits on a bench with her tray, tail curling. |
| 0x2bd8c | 53 | You're probably tired from all that work. I brought\n |
| 0x2bdc2 | 43 | some tea. C'mon, come take a break with me. |
| 0x2bdee | 5 | Wh--? |
| 0x2bdf4 | 53 | Two cups sit perched on the tray, warm steam rising\n |
| 0x2be2a | 18 | from their depths. |
| 0x2be3d | 12 | ...Not good. |
| 0x2be4a | 53 | If I let go now, this thing is gonna keep moving on\n |
| 0x2be80 | 38 | its own, and it'll be a dead giveaway. |
| 0x2bea7 | 19 | Is something wrong? |
| 0x2bebb | 54 | Uh, no, just... I'll be done with this bag in a bit,\n |
| 0x2bef2 | 30 | so I'll stop for a break then. |
| 0x2bf11 | 36 | Your tea's going to get cold, th--\n |
| 0x2bf36 | 52 | ...No, you shouldn't push yourself so hard. You've\n |
| 0x2bf6b | 22 | only just recovered... |
| 0x2bf82 | 47 | You really should take a small break for your\n |
| 0x2bfb2 | 50 | health, you know. I can switch with you for a bit. |
| 0x2bfe5 | 54 | Huh? Uh... um. No thanks. This is my job, after all.\n |
| 0x2c01c | 9 | Mhm. Yep. |
| 0x2c026 | 52 | ...She'll definitely figure me out if we switch off. |
| 0x2c05b | 51 | You're sure you're not pushing yourself over your\n |
| 0x2c08f | 6 | limit? |
| 0x2c096 | 16 | O-Of course not. |
| 0x2c0a7 | 53 | Well, if you say so. I suppose it was rude of me to\n |
| 0x2c0dd | 39 | interrupt while you're working so hard. |
| 0x2c105 | 50 | Kuon smiles, taking a delicate sip of her own tea. |
| 0x2c138 | 43 | Hmhm. I have to say, I'm a little relieved. |
| 0x2c164 | 13 | A-About what? |
| 0x2c172 | 52 | I was a little worried you were going to starve to\n |
| 0x2c1a7 | 36 | death, the way you were carrying on. |
| 0x2c1cc | 4 | Huh? |
| 0x2c1d1 | 51 | You were so weak. I wasn't sure if you were going\n |
| 0x2c205 | 11 | to survive. |
| 0x2c211 | 47 | ...What? Was I really in that dire a situation? |
| 0x2c241 | 31 | I didn't think it was THAT bad. |
| 0x2c261 | 50 | You were struggling to carry loads even children\n |
| 0x2c294 | 52 | could handle. You could barely walk with them, even. |
| 0x2c2c9 | 52 | In a weakened state like that, I was worried you'd\n |
| 0x2c2fe | 28 | be no good for manual labor. |
| 0x2c31b | 50 | Your hands look very clean, too. I expect you've\n |
| 0x2c34e | 45 | never held a hoe, let alone done any hunting. |
| 0x2c37c | 7 | Urgh... |
| 0x2c384 | 49 | Does she really think I'm that hopeless? Are my\n |
| 0x2c3b6 | 30 | circumstances really THAT bad? |
| 0x2c3d5 | 49 | But judging by how you're doing with that mill,\n |
| 0x2c407 | 38 | I guess your body was just recovering. |
| 0x2c42e | 44 | Seeing you back at full strength is really\n |
| 0x2c45b | 10 | relieving. |
| 0x2c466 | 10 | I-I see... |
| 0x2c471 | 44 | W-Well now what do I do? I can't just ruin\n |
| 0x2c49e | 50 | everything she just said and tell her the truth,\n |
| 0x2c4d1 | 6 | now... |
| 0x2c4d8 | 14 | *Grrrrrrrk*... |
| 0x2c4e7 | 52 | Crap, I'm getting really tired. I actually DO want\n |
| 0x2c51c | 47 | to take a break, but I can't while Kuon's here. |
| 0x2c54c | 52 | I feel like I'm being ungrateful by deceiving her,\n |
| 0x2c581 | 32 | but I'm really at my limit here. |
| 0x2c5a2 | 54 | H-Hey, Kuon. I think I can handle this by myself, so\n |
| 0x2c5d9 | 45 | if you have other stuff to do, don't wait up. |
| 0x2c607 | 51 | Hm. I... I suppose you're right, but I don't feel\n |
| 0x2c63b | 36 | good leaving you all alone, I guess. |
| 0x2c660 | 32 | You don't trust me much, do you? |
| 0x2c681 | 54 | Ngh. Did she figure out that I'm trying not to work?\n |
| 0x2c6b8 | 41 | Please, just take the out and go. Please. |
| 0x2c6e2 | 51 | It's not that. I'm just worried that if I take my\n |
| 0x2c716 | 47 | eyes off you, you might just fall down and die. |
| 0x2c746 | 36 | Come on, even I'm... h-hah... hah.\n |
| 0x2c76b | 20 | I'm not that weak... |
| 0x2c780 | 11 | ...I think? |
| 0x2c78c | 42 | As the one who took you in, it's my duty\n |
| 0x2c7b7 | 22 | to see to your health. |
| 0x2c7ce | 53 | If I'm not capable of doing that, then it was wrong\n |
| 0x2c804 | 36 | of me to bring you along back there. |
| 0x2c829 | 53 | Hah... h-hahh... It's... nice to hear you say that,\n |
| 0x2c85f | 50 | but I'm not too comfortable with so much worrying. |
| 0x2c892 | 44 | I'm sure you're busy. Don't let me keep you. |
| 0x2c8bf | 47 | Really? Well, if you insist, I'll be on my way. |
| 0x2c8ef | 45 | Kuon sets down her cup and gracefully stands. |
| 0x2c91d | 49 | Just remember, don't overdo it, OK? Take breaks\n |
| 0x2c94f | 22 | every once in a while. |
| 0x2c966 | 22 | All right, understood. |
| 0x2c97d | 52 | I get it, so would you please go so I actually CAN\n |
| 0x2c9b2 | 13 | take a break? |
| 0x2c9c0 | 5 | Good! |
| 0x2c9c6 | 11 | Bhhaahhh... |
| 0x2c9d2 | 52 | Once I'm sure Kuon is out of earshot, I crumple to\n |
| 0x2ca07 | 28 | the ground beneath the mill. |
| 0x2ca24 | 49 | Phew. Somehow, I managed to play it off. I feel\n |
| 0x2ca56 | 40 | guilty, but I'll worry about that later. |
| 0x2ca7f | 35 | I guess I'll grab some tea before-- |
| 0x2caa3 | 9 | Oh, Haku? |
| 0x2caad | 10 | Nghyaaah!? |
| 0x2cab8 | 44 | I jump back on the mill in the nick of time. |
| 0x2cae5 | 49 | It's probably a little cold now, but the tea...\n |
| 0x2cb17 | 25 | Is... Is something wrong? |
| 0x2cb31 | 32 | N-Nope. Nothing. Nothing at all. |
| 0x2cb52 | 54 | Really? Well, it's important to stay hydrated. Drink\n |
| 0x2cb89 | 21 | the tea when you can. |
| 0x2cb9f | 17 | Yeah, understood. |
| 0x2cbb1 | 26 | OK, keep up the good work. |
| 0x2cbcc | 48 | This time, I keep my ears open for any unusual\n |
| 0x2cbfd | 7 | sounds. |
| 0x2cc05 | 52 | Kuon's footsteps slowly grow more and more distant\n |
| 0x2cc3a | 43 | until--finally--I can't hear them any more. |
| 0x2cc66 | 54 | Geez... thought my heart was gonna leap right out of\n |
| 0x2cc9d | 9 | my chest. |
| 0x2cca7 | 50 | I wipe the sweat from my brow and regard the mill. |
| 0x2ccda | 52 | What do I do now, though? I have no way of telling\n |
| 0x2cd0f | 50 | when Kuon will be back, or when this will be done. |
| 0x2cd42 | 54 | There's gotta be a way to wrap this up faster. Maybe\n |
| 0x2cd79 | 42 | if I get the mill to turn more quickly...? |
| 0x2cda4 | 53 | Once again, I examine each part of the mechanism in\n |
| 0x2cdda | 42 | sequence, trying to puzzle out my dilemma. |
| 0x2ce05 | 51 | If I want to increase the grinding speed, I could\n |
| 0x2ce39 | 47 | change up the gear ratio. It'd work, in theory. |
| 0x2ce69 | 51 | There's a bunch of gears that aren't moving right\n |
| 0x2ce9d | 39 | now, anyway. If I just swap those in... |
| 0x2cec5 | 37 | Brain, buddy, you are on point today. |
| 0x2ceeb | 54 | It took some trial and error, but sure enough, I got\n |
| 0x2cf22 | 34 | the gears rearranged successfully. |
| 0x2cf45 | 49 | As the last gear slots into place, another loud\n |
| 0x2cf77 | 50 | THUNK heralds the mill groaning to life once more. |
| 0x2cfaa | 34 | *Grrrk*... *Rrr*... *Grrrrrrrk*... |
| 0x2cfcd | 41 | Woah... Nice, it's going at quite a clip. |
| 0x2cff7 | 55 | The axle--and the gears, and the mill--turn the stone\n |
| 0x2d02f | 24 | much faster than before. |
| 0x2d048 | 46 | More amam turns to powder with each rhythmic\n |
| 0x2d077 | 21 | rotation of the mill. |
| 0x2d08d | 49 | All right, this should... double? No, triple my\n |
| 0x2d0bf | 7 | output. |
| 0x2d0c7 | 51 | All I've gotta do is keep throwing amam into this\n |
| 0x2d0fb | 6 | thing. |
| 0x2d102 | 52 | Oh, right. The tea. Kuon went through the trouble,\n |
| 0x2d137 | 44 | so I should drink some. Probably cold now... |
| 0x2d164 | 11 | Footsteps!? |
| 0x2d170 | 54 | Footfalls sound closer and closer, so I quickly jump\n |
| 0x2d1a7 | 24 | back on the mill handle. |
| 0x2d1c0 | 6 | *FWUP* |
| 0x2d1c7 | 6 | Nngh!? |
| 0x2d1ce | 48 | As I get my grip on the handle, I can feel the\n |
| 0x2d1ff | 49 | sped-up mill pulling me along. I have to run to\n |
| 0x2d231 | 8 | keep up. |
| 0x2d23a | 15 | Argh, too fast! |
| 0x2d24a | 49 | I try to slow myself down, but I can't with the\n |
| 0x2d27c | 47 | momentum. Trying to stop just ends in getting\n |
| 0x2d2ac | 8 | dragged. |
| 0x2d2b5 | 48 | I almost forgot. About dinner tonight, would y-- |
| 0x2d2e6 | 53 | Kuon cuts herself off as the sight of me running at\n |
| 0x2d31c | 37 | full tilt around the mill greets her. |
| 0x2d342 | 31 | What exactly is going on, here? |
| 0x2d362 | 47 | A-As you can see, I'm just--ACK--spin--nnning\n |
| 0x2d392 | 16 | the MILL, geez-- |
| 0x2d3a3 | 44 | It looks more like the mill is spinning you. |
| 0x2d3d0 | 53 | Ah--hahh, hah--W-well! I think I've gotten pretty--\n |
| 0x2d406 | 45 | hah--used to it. This speed is nnNO PROBLEM!? |
| 0x2d434 | 50 | I nearly trip over my own feet in my struggle to\n |
| 0x2d467 | 16 | keep my balance. |
| 0x2d478 | 35 | S-Something.. hah... the matter...? |
| 0x2d49c | 5 | Haku? |
| 0x2d4a2 | 38 | Kuon looks at me with suspicious eyes. |
| 0x2d4c9 | 20 | H-Hah. Hahh... Yeah? |
| 0x2d4de | 49 | C-Can't... breathe... I think this is my limit,\n |
| 0x2d510 | 7 | here... |
| 0x2d518 | 40 | Is there anything you'd like to tell me? |
| 0x2d541 | 44 | N-No, I--I'm not--h-hiding anything from y-- |
| 0x2d56e | 53 | L-L-Look, I'll be great! I'll be just fine here, so\n |
| 0x2d5a4 | 51 | you... hah... go and take care of... your... hah... |
| 0x2d5d8 | 52 | Oh, no need for that. I've already finished all my\n |
| 0x2d60d | 8 | errands. |
| 0x2d616 | 49 | I think I'll stay here and watch you work for a\n |
| 0x2d648 | 13 | little while. |
| 0x2d656 | 6 | What!? |
| 0x2d65d | 52 | Kuon resumes her position on the bench, reclaiming\n |
| 0x2d692 | 30 | her tea and sipping elegantly. |
| 0x2d6b1 | 35 | Hm. A bit lukewarm, now, I think... |
| 0x2d6d5 | 49 | Kuon lets her long, sinuous tail swish back and\n |
| 0x2d707 | 33 | forth as she watches me struggle. |
| 0x2d729 | 15 | Hah, hah, hah-- |
| 0x2d739 | 18 | *Wheeze, wheeze--* |
| 0x2d74c | 53 | You sound a little out of breath, Haku. Are you all\n |
| 0x2d782 | 46 | Nngh, wh-what... could you... possibly mean?\n |
| 0x2d7b1 | 29 | I-I'm not... out of breath... |
| 0x2d7cf | 35 | Then why is your face so red, Haku? |
| 0x2d7f3 | 33 | I-It's pretty hot out today! Yep! |
| 0x2d815 | 47 | And why are your arms and legs shaking like a\n |
| 0x2d845 | 17 | newborn animal's? |
| 0x2d857 | 48 | I'm just trembling with excitement here! Work!\n |
| 0x2d888 | 12 | What a rush! |
| 0x2d895 | 10 | Ah, I see. |
| 0x2d8a0 | 10 | *Swish*... |
| 0x2d8ab | 54 | Suddenly, Kuon's tail whips out and snakes around my\n |
| 0x2d8e2 | 36 | legs, taking them out from under me. |
| 0x2d907 | 9 | Nwaaaah!? |
| 0x2d911 | 7 | *Thud!* |
| 0x2d919 | 16 | Wh-What th--GAH! |
| 0x2d92a | 50 | The handle quickly comes full circle without me... |
| 0x2d95d | 8 | *THWACK* |
| 0x2d966 | 7 | Bfaah!? |
| 0x2d96e | 48 | Taken in the back, the might of the waterwheel\n |
| 0x2d99f | 50 | cares little for my body weight, pushing me along. |
| 0x2d9d2 | 27 | Round and round and round-- |
| 0x2d9ee | 15 | NWAAAAAAAAH--!? |
| 0x2d9fe | 18 | Haku, take a seat. |
| 0x2da11 | 18 | W-Well, you see... |
| 0x2da24 | 19 | I said take a seat. |
| 0x2da38 | 34 | Kuon forces me to sit on my knees. |
| 0x2da5b | 54 | So you managed to fix the water mill, but kept quiet\n |
| 0x2da92 | 9 | about it? |
| 0x2da9c | 7 | Well... |
| 0x2daa4 | 53 | Whatever your methods, as long as you were grinding\n |
| 0x2dada | 49 | grains here, I wouldn't have given you more work. |
| 0x2db0c | 11 | Wait, what? |
| 0x2db18 | 41 | Then I went through all that for nothing? |
| 0x2db42 | 50 | But when you do something like this, it makes me\n |
| 0x2db75 | 49 | feel like you don't trust me, not to mention sad. |
| 0x2dba7 | 18 | Nngh... S-Sorry... |
| 0x2dbba | 52 | Anyway. I'll let the innkeeper know the mill is at\n |
| 0x2dbef | 26 | least somewhat usable now. |
| 0x2dc0a | 52 | I'm sure she'll be thrilled by the news, since she\n |
| 0x2dc3f | 41 | seemed pretty down about it being broken. |
| 0x2dc69 | 53 | Wh--But if you tell them that, then I won't be able\n |
| 0x2dc9f | 13 | to slack off! |
| 0x2dcad | 53 | And there aren't any problems with that, are there,\n |
| 0x2dce3 | 52 | Urk!? W-Well, you know... Maybe we could keep it a\n |
| 0x2dd18 | 51 | secret for a while longer? Just, y'know, an idea... |
| 0x2dd4c | 8 | Ahaha... |
| 0x2dd55 | 8 | *BADUMP* |
| 0x2dd5e | 23 | Kuon smiles cheerfully. |
| 0x2dd76 | 54 | It's a very kind, gentle, earnest smile, but a chill\n |
| 0x2ddad | 34 | courses down my spine nonetheless. |
| 0x2ddd0 | 6 | Hurk!? |
| 0x2ddd7 | 53 | And in the next instant, Kuon's whiplike tail wraps\n |
| 0x2de0d | 23 | around my head tightly. |
| 0x2de25 | 51 | Sorry, I couldn't catch what you said there. What\n |
| 0x2de59 | 9 | was that? |
| 0x2de63 | 23 | *KRRRKKK... KRK-KRK*... |
| 0x2de7b | 14 | W-Wait! Guh... |
| 0x2de8a | 54 | An immense force presses inward on my skull, closing\n |
| 0x2dec1 | 28 | with the strength of a vise. |
| 0x2dede | 45 | Oh, right. I didn't finish what I was saying. |
| 0x2df0c | 50 | You did do something of use to the people living\n |
| 0x2df3f | 37 | here, so you get a little reward~♪. |
| 0x2df65 | 24 | And for your reward...\n |
| 0x2df7e | 41 | Your punishment will only be a small one. |
| 0x2dfa8 | 11 | *KRRKKK*... |
| 0x2dfb4 | 21 | GYAAAAAAAAAAAAARGH!!! |
| 0x2dfca | 53 | But... You know, between the arithmetic and this...\n |
| 0x2e000 | 49 | I'm starting to think you aren't a manual worker. |
| 0x2e032 | 52 | I think I had the wrong idea about you, after all... |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_03.json` com a forma:
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
