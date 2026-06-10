# Cena ch_12_08 — pacote de traducao (136 linhas)

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
- `thing.` -> `coisa.` (Haku, 12_03)
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Man` -> `Hom` (Sistema, 12_04)
- `Ukon's Cohorts` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Is something wrong?` -> `Algum problema?` (Kuon, 11_06)
- `...It's nothing.` -> `...Não é nada.` (Kuon, root)
- `Hm?` -> `Hum?` (Kuon, 11_04)
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
| 0x3ac18 | 26 | It was around here, right? |
| 0x3ac33 | 8 | Villager |
| 0x3ac3c | 34 | Y-Yeah... Yeah, no doubt about it. |
| 0x3ac5f | 46 | The injured man's voice trembles, visions of\n |
| 0x3ac8e | 49 | yesterday's encounter no doubt returning to his\n |
| 0x3acc0 | 5 | mind. |
| 0x3acc6 | 53 | From the look of things, there don't seem to be any\n |
| 0x3acfc | 16 | gigiri nearby... |
| 0x3ad0d | 51 | All right. Everyone take a breather while we hash\n |
| 0x3ad41 | 17 | out our strategy. |
| 0x3ad53 | 49 | At Ukon's command, his men break rank to take a\n |
| 0x3ad85 | 50 | rest, sitting down and drinking from their flasks. |
| 0x3adb8 | 39 | Maroro, I'll leave the briefing to you. |
| 0x3ade0 | 9 | Unnhhh... |
| 0x3adea | 52 | Despite Ukon's prompting, Maroro remains face-down\n |
| 0x3ae1f | 46 | on the ground, flat on his belly and groaning. |
| 0x3ae4e | 48 | Good grief. All right, I'll do it. This really\n |
| 0x3ae7f | 31 | isn't my strong suit, y'know... |
| 0x3ae9f | 52 | Ukon sighs and steps up beside a large, folded net\n |
| 0x3aed4 | 45 | in the bed of the cart, patting it pointedly. |
| 0x3af02 | 50 | All right, before anything else, we're gonna lay\n |
| 0x3af35 | 25 | out this net. And then... |
| 0x3af4f | 47 | He knocks on a large container next to the net. |
| 0x3af7f | 52 | We'll pour this stew of rotten meat over the whole\n |
| 0x3afb4 | 6 | thing. |
| 0x3afbb | 50 | Urgh. I was wondering what the cart's cargo was.\n |
| 0x3afee | 30 | So that's what was in there... |
| 0x3b00d | 48 | Good thing that didn't spill on the journey up\n |
| 0x3b03e | 12 | here. Yikes. |
| 0x3b04b | 50 | Seems like rotting meat's their favorite. If all\n |
| 0x3b07e | 51 | goes as planned, it'll lure the gigiri in the area. |
| 0x3b0b2 | 52 | Once they step on the net, it'll tangle their legs\n |
| 0x3b0e7 | 20 | and immobilize them. |
| 0x3b0fc | 54 | So, they're going to use a trap to eliminate them...\n |
| 0x3b133 | 7 | But...? |
| 0x3b13b | 53 | No, no, that's not going to work. Those monsters'll\n |
| 0x3b171 | 47 | tear through that flimsy net like it's nothing. |
| 0x3b1a1 | 53 | Then Maroro'll hit 'em with a big one, and we'll be\n |
| 0x3b1d7 | 51 | stationed at the perimeter to catch any stragglers. |
| 0x3b20b | 33 | Those gigiri are no match for us! |
| 0x3b22d | 51 | Ukon grins, and his company lets out a collective\n |
| 0x3b261 | 6 | laugh. |
| 0x3b26c | 51 | Is it... really gonna be that simple? Is that net\n |
| 0x3b2a0 | 14 | strong enough? |
| 0x3b2af | 50 | I don't think those creatures are gonna be taken\n |
| 0x3b2e2 | 20 | care of that easily. |
| 0x3b2f7 | 20 | Still anxious, Haku? |
| 0x3b30c | 50 | Ah, well... I just can't help but think the trap\n |
| 0x3b33f | 41 | should be... sturdier. Among other stuff. |
| 0x3b369 | 53 | Stop being such a worrywart. Even if they're on the\n |
| 0x3b39f | 47 | bigger side for gigiri, it should be just fine. |
| 0x3b3cf | 53 | You say that, but I'm having a vision of everything\n |
| 0x3b405 | 38 | collapsing and our party scattering... |
| 0x3b42c | 13 | Ukon's Cohort |
| 0x3b43a | 53 | C'mon, kid, you don't gotta worry about that stuff.\n |
| 0x3b470 | 15 | Relax a little. |
| 0x3b480 | 47 | Yeah! We've done extermination jobs like this\n |
| 0x3b4b0 | 33 | before. Gigiri aren't a big deal. |
| 0x3b4d2 | 25 | See? Don't worry so much. |
| 0x3b4ec | 50 | He's right about one thing, though. Let's not be\n |
| 0x3b51f | 37 | careless. Nobody let your guard down. |
| 0x3b545 | 52 | And don't even think about getting hurt on purpose\n |
| 0x3b57a | 42 | just so you can get treated by missy here. |
| 0x3b5a5 | 48 | I catch anyone doing that, I'm halving your pay. |
| 0x3b5d6 | 3 | Man |
| 0x3b5da | 27 | Oops! Caught us red-handed! |
| 0x3b5f6 | 14 | Ukon's Cohorts |
| 0x3b605 | 8 | Ahahaha! |
| 0x3b60e | 48 | The sound of jovial laughter rings through the\n |
| 0x3b63f | 9 | clearing. |
| 0x3b649 | 50 | I catch snatches of conversation about how being\n |
| 0x3b67c | 50 | treated by Kuon would make it worth the pay hit... |
| 0x3b6af | 50 | Kuon smiles vaguely, but she seems troubled more\n |
| 0x3b6e2 | 19 | than anything else. |
| 0x3b6f6 | 53 | Everyone's calm and composed--even relaxed. I guess\n |
| 0x3b72c | 45 | the gigiri really aren't so big a problem...? |
| 0x3b75a | 52 | If that's the case, these guys' physical abilities\n |
| 0x3b78f | 24 | must be beyond belief... |
| 0x3b7a8 | 49 | God. I'm starting to understand what Kuon meant\n |
| 0x3b7da | 51 | when she said she was worried I'd just die by the\n |
| 0x3b80e | 42 | roadside, left to my own devices out here. |
| 0x3b839 | 19 | Is something wrong? |
| 0x3b84d | 16 | ...It's nothing. |
| 0x3b85e | 22 | Haku, are you nervous? |
| 0x3b875 | 18 | No, not... really. |
| 0x3b888 | 53 | I'm lying, of course. Just the memory of the gigiri\n |
| 0x3b8be | 37 | is enough to make me shudder in fear. |
| 0x3b8e4 | 51 | I'm not like these guys. For me, it'd be stranger\n |
| 0x3b918 | 48 | NOT to be nervous going up against that beast... |
| 0x3b949 | 5 | Haku. |
| 0x3b94f | 18 | Kuon smiles at me. |
| 0x3b962 | 3 | Hm? |
| 0x3b966 | 44 | ...You don't have to be like them, you know. |
| 0x3b993 | 51 | You have other talents that you should be proud of. |
| 0x3b9c7 | 11 | Am I wrong? |
| 0x3b9d3 | 16 | ...You think so? |
| 0x3b9e4 | 10 | Mhm. I do. |
| 0x3b9ef | 51 | Kuon's smile relieves my worries for some reason... |
| 0x3ba23 | 22 | ...Guess you're right. |
| 0x3ba3a | 49 | Besides, with luck like yours? You might die by\n |
| 0x3ba6c | 52 | the roadside some day, but you'll survive a scrape\n |
| 0x3baa1 | 19 | or two before then. |
| 0x3bab5 | 9 | Hey, now. |
| 0x3babf | 49 | ...I must have looked pretty worried for her to\n |
| 0x3baf1 | 30 | have cracked a joke like that. |
| 0x3bb10 | 49 | I guess she's right, though. I don't have to be\n |
| 0x3bb42 | 52 | like those guys, so I shouldn't waste time worrying. |
| 0x3bb77 | 54 | If the gap between me and the others is so dramatic,\n |
| 0x3bbae | 39 | I'm not sure I care that much any more. |
| 0x3bbd6 | 11 | Ah heh heh. |
| 0x3bbe2 | 36 | What, is there something on my face? |
| 0x3bc07 | 48 | Oh, no, I just... You seem to be feeling better. |
| 0x3bc38 | 28 | I think you'll be just fine. |
| 0x3bc55 | 40 | Oh, right--I was gonna give this to you. |
| 0x3bc7e | 33 | Kuon proffers a slender object... |
| 0x3bca0 | 12 | What's this? |
| 0x3bcad | 48 | A metal fan...? Is this that thing they call a\n |
| 0x3bcde | 9 | "tessen"? |
| 0x3bce8 | 48 | Even though it's made of metal, I can tell the\n |
| 0x3bd19 | 38 | grip's been worn down from long use... |
| 0x3bd40 | 49 | I'd rather you have a weapon to defend yourself\n |
| 0x3bd72 | 51 | with, so go ahead and use that if you get cornered. |
| 0x3bda6 | 51 | I appreciate it, but this looks like an heirloom.\n |
| 0x3bdda | 37 | Isn't this something precious to you? |
| 0x3be00 | 49 | Even though it's been well-used, it's also been\n |
| 0x3be32 | 48 | well-kept, polished and buffed free of any rust. |
| 0x3be63 | 40 | It's probably been maintained regularly. |
| 0x3be8c | 47 | I'm only lending it to you. I'll want it back\n |
| 0x3bebc | 22 | eventually, all right? |
| 0x3bed3 | 10 | All right. |
| 0x3bede | 18 | "Eventually," huh. |
| 0x3bef1 | 47 | I tightly clench Kuon's metal fan in my hand... |
| 0x3bf21 | 48 | It's my first time holding it, but somehow, it\n |
| 0x3bf52 | 51 | feels like it fits in my palm with perfect comfort. |
| 0x3bf86 | 51 | ...And I can't help but wonder... If those stains\n |
| 0x3bfba | 34 | on the blade aren't rust, then...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_08.json` com a forma:
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
