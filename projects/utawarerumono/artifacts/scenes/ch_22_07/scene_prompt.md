# Cena ch_22_07 — pacote de traducao (409 linhas)

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
- **pt-BR MODERNO (registro do jogador de hoje):** preferir a forma que um jogador BR atual usaria, não
  a "correta-mas-arcaica/truncada". Dois erros recorrentes pegos em QA in-game:
  - **Resposta de NOME** (`I'm…`/`My name's…`/`I am…` quando responde "qual seu nome?") → **"Meu nome é…"
    / "Eu me chamo…" / "Sou o(a)…"** conforme a voz. NUNCA "Eu sou" seco — refere-se a estado, soa
    truncado para apresentação.
  - **Léxico arcaico/erudito** (ex.: "ruminar"/"Rumino" por "pensar/refletir") só quando a VOZ do
    personagem pede; senão, a palavra que o público entende **de imediato**.
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
□ pt-BR moderno: forma que um jogador de HOJE usaria? (nome → "Meu nome é/Eu me chamo", não "Eu sou"; sem arcaísmo gratuito)
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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
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
- `notice.` -> `vista.` (Ukon, 15_05)
- `you?` -> `pode?` (Haku, 13_01)
- `return.` -> `retirada.` (Zeguni, 20_20)
- `first place.` -> `em primeiro lugar.` (Haku, 17_01)
- `much.` -> `isso.` (Ukon, 13_09)
- `sister.` -> `irmã.` (Ukon, 14_04)
- `...Gah!?` -> `...Ai!?` (Haku, 17_01)
- `for that.` -> `por isso.` (Ukon, 22_06)
- `change.` -> `mudança.` (Haku, 18_01)
- `...Kuon?` -> `...Kuon?` (Haku, 11_11)
- `That is...` -> `Isso é...` (Mulher, 17_01)
- `...All right.` -> `...Tudo bem.` (Protagonista, 21_07)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Ahhh...` -> `Ahhh...` (Haku, 11_10)
- `...Oh.` -> `...Ah.` (Haku, 13_03)
- `state...` -> `estado...` (Haku, 18_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `like that?` -> `assim?` (Haku, 15_01)
**Voz estabelecida dos falantes (amostra):**
- Protagonista: `Ngh... ghh...` -> `Nnh... aagh...`
- Protagonista: `Nn...\n` -> `Nnh...\n`
- Protagonista: `It's... warm...?` -> `Está... quente...?`
- Haku: `Urgh...` -> `Argh...`
- Haku: `Right?` -> `né?`
- Haku: `Nn...` -> `Nnh...`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
- Maroro: `Master Ukon! It pleaseth my heart to report my\n` -> `Mestre Ukon! É com grande satisfação que reporto que meus\n`
- Maroro: `belongings lay duly unpack'd, and await porters.` -> `meus pertences estão desfeitos e aguardam os carregadores.`
- Ukon: `Ah. Well done.` -> `Ah. Bom trabalho.`
- Maroro: `I am VERY tired, sir. Naught more now do I desire\n` -> `Estou MUITO cansado, senhor. Nada mais desejo agora\n`
- Ukon: `Really, Maroro? Seems like you get tired quicker\n` -> `É sério, Maroro? Parece que você se cansa mais rápido\n`
- Ukon: `and quicker these days...` -> `a cada dia que passa...`
- Homem: `The way you were carrying on, you got us all\n` -> `Do jeito que você estava, nos deixou todos\n`
- Homem: `anxious, too!` -> `ansiosos também!`
- Homem: `Wahahahaha!!` -> `Wahahahaha!!`
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
| 0x2544cf | 48 | I am sorry to have called you in on such short\n |
| 0x254500 | 7 | notice. |
| 0x254508 | 48 | Oshtor stops organizing the papers on his desk\n |
| 0x254539 | 36 | as I enter, and he looks towards me. |
| 0x25455e | 44 | I know you are a busy man, but I am afraid\n |
| 0x25458b | 45 | I could think of none more fit for this task. |
| 0x2545b9 | 47 | It's all right. I can always use an excuse to\n |
| 0x2545e9 | 17 | get out of a job. |
| 0x2545fb | 49 | Kuon's been taking jobs more than usual lately.\n |
| 0x25462d | 30 | I don't get any time to relax. |
| 0x25464c | 45 | Haha... Lady Kuon remains true to form. She\n |
| 0x25467a | 47 | knows you relax as soon as you know nobody is\n |
| 0x2546aa | 13 | watching you. |
| 0x2546b8 | 47 | Keeping you busy with work is most likely the\n |
| 0x2546e8 | 22 | best solution to this. |
| 0x2546ff | 49 | Oh, come on. Can't you sympathize a little with\n |
| 0x254731 | 42 | the guy being forced to work all the time? |
| 0x25475c | 49 | Well, whatever. I get Kuon out of my hair and I\n |
| 0x25478e | 48 | can relax a bit here. I'm not turning that down. |
| 0x2547bf | 46 | Oh? Are you sure? There may be repercussions\n |
| 0x2547ee | 13 | for that, hm? |
| 0x2547fc | 45 | It's fine. I was called in by our employer.\n |
| 0x25482a | 36 | I'm not doing anything wrong, right? |
| 0x25484f | 51 | Hah. You always think these things through, don't\n |
| 0x254883 | 4 | you? |
| 0x254888 | 29 | ...So, why'd you call for me? |
| 0x2548a6 | 43 | Ah, right. Now is not the time to be idly\n |
| 0x2548d2 | 9 | chatting. |
| 0x2548dc | 49 | I wanted to ask that you watch the place a while. |
| 0x25490e | 16 | Watch the place? |
| 0x25491f | 48 | Yes. I've been summoned to the Imperial Palace\n |
| 0x254950 | 17 | on urgent notice. |
| 0x254962 | 50 | I wouldn't think you'd need someone to watch the\n |
| 0x254995 | 45 | place just for that. Or is there some other\n |
| 0x2549c3 | 7 | reason? |
| 0x2549cb | 49 | Well, Nekone is on an errand. She should return\n |
| 0x2549fd | 48 | soon--I ask that you keep her company until my\n |
| 0x254a2e | 7 | return. |
| 0x254a36 | 46 | Sure, I guess I can do that... But can't you\n |
| 0x254a65 | 44 | just leave a note or a message in that case? |
| 0x254a92 | 48 | I mean, it IS urgent business, right? I'm sure\n |
| 0x254ac3 | 24 | Nekone would understand. |
| 0x254adc | 48 | True, but I would feel bad making her wait for\n |
| 0x254b0d | 45 | me after I had asked the task of her in the\n |
| 0x254b3b | 12 | first place. |
| 0x254b48 | 50 | ...And you've got no problem doing the same damn\n |
| 0x254b7b | 13 | thing to me!? |
| 0x254b89 | 47 | Oshtor only grins, as though he was expecting\n |
| 0x254bb9 | 19 | a retort like that. |
| 0x254bcd | 45 | God, you spoil that sister of yours way too\n |
| 0x254bfb | 5 | much. |
| 0x254c01 | 49 | I'd say there is hardly fault in that. There is\n |
| 0x254c33 | 46 | no brother that does not care dearly for his\n |
| 0x254c62 | 7 | sister. |
| 0x254c6a | 49 | Yeah, "no brother that does not care dearly for\n |
| 0x254c9c | 20 | his sister..." Sure. |
| 0x254cb1 | 48 | You may use this room however you please while\n |
| 0x254ce2 | 28 | you wait. So, do you accept? |
| 0x254cff | 49 | Sure, whatever. If that's how it's going to be,\n |
| 0x254d31 | 34 | I might as well take it easy here. |
| 0x254d54 | 42 | Thank you. I should be back before sunset. |
| 0x254d7f | 47 | With that, I watch Oshtor depart, then take a\n |
| 0x254daf | 15 | seat and relax. |
| 0x254dbf | 48 | No brother that does not care dearly about his\n |
| 0x254df0 | 38 | sister... What an Oshtor thing to say. |
| 0x254e17 | 46 | I still think he's spoiling her a bit... but\n |
| 0x254e46 | 45 | it's not like I have a sister. Maybe I just\n |
| 0x254e74 | 13 | don't get it. |
| 0x254e82 | 47 | ...Well, he did say I can use this place as I\n |
| 0x254eb2 | 36 | please. That means only one thing... |
| 0x254ed7 | 49 | I check the softness of the cushion nearest me,\n |
| 0x254f09 | 23 | then lay my head on it. |
| 0x254f21 | 36 | Ah, just right. Time to take a nap-- |
| 0x254f46 | 8 | ...Gah!? |
| 0x254f4f | 46 | The image of Nekone's face flashes across my\n |
| 0x254f7e | 32 | mind. If she saw me like this... |
| 0x254f9f | 45 | ...No no no. Nekone's supposed to be coming\n |
| 0x254fcd | 10 | here soon. |
| 0x254fd8 | 46 | If she finds me sleeping here, I might never\n |
| 0x255007 | 20 | escape THAT lecture. |
| 0x25501c | 50 | The thought's engraved in my head now. I wearily\n |
| 0x25504f | 31 | raise my head from the cushion. |
| 0x25506f | 44 | To her, this place might as well be sacred\n |
| 0x25509c | 42 | ground. She'd be pissed if she caught me\n |
| 0x2550c7 | 15 | napping here... |
| 0x2550d7 | 45 | But if I can't take a nap... How can I kill\n |
| 0x255105 | 10 | some time? |
| 0x255110 | 46 | I look around again. As expected of Oshtor's\n |
| 0x25513f | 48 | business room, it's full of countless official\n |
| 0x255170 | 7 | papers. |
| 0x255178 | 47 | Oh, score. Found some snacks. But I guess I'm\n |
| 0x2551a8 | 45 | not that hungry, now that I think about it... |
| 0x2551d6 | 48 | Maybe there's something I can read to pass the\n |
| 0x255207 | 8 | time...? |
| 0x255210 | 47 | I search around the place, but all I can find\n |
| 0x255240 | 32 | are complicated-looking letters. |
| 0x255261 | 45 | Well, this IS where Oshtor works. Not gonna\n |
| 0x25528f | 37 | find much in the way of leisure here. |
| 0x2552b5 | 46 | I'm here in Oshtor's stead, but I don't know\n |
| 0x2552e4 | 39 | what to do even if she comes... Wait.\n |
| 0x25530c | 18 | Oshtor's stead...? |
| 0x25531f | 48 | A sudden inspiration occurs to me, and I can't\n |
| 0x255350 | 40 | help but grin at my flash of brilliance. |
| 0x255379 | 44 | Well, not like I have anything else to do.\n |
| 0x2553a6 | 31 | I think I'll have a little fun. |
| 0x2553c6 | 43 | Let's see, what can I use... Heh heh heh.\n |
| 0x2553f2 | 34 | She's never gonna see this coming. |
| 0x255415 | 46 | I search the room, ready to put my plan into\n |
| 0x255444 | 48 | action. I gradually find everything I'll need... |
| 0x255475 | 47 | This should be enough. Now I just cut it into\n |
| 0x2554a5 | 18 | the proper size... |
| 0x2554b8 | 41 | And fold it here and here... liiike this. |
| 0x2554e2 | 48 | Hmm. Maybe a little too big. If I cut here and\n |
| 0x255513 | 19 | glue it together... |
| 0x255527 | 47 | With time and effort, the object slowly takes\n |
| 0x255557 | 27 | the shape I'm aiming for... |
| 0x255573 | 47 | Oh, looking pretty good. If I straighten this\n |
| 0x2555a3 | 21 | part a little more... |
| 0x2555b9 | 43 | Nice. Just gotta glue this last bit, and... |
| 0x2555e5 | 18 | Ta-da! Complete!\n |
| 0x2555f8 | 14 | Oshtor's mask! |
| 0x255607 | 48 | Huh! Didn't think I could do such a close copy\n |
| 0x255638 | 45 | with just paper. Looks better than I thought. |
| 0x255666 | 49 | A little darker than the real thing, but that's\n |
| 0x255698 | 18 | part of the charm. |
| 0x2556ab | 21 | And now... I wear it! |
| 0x2556c1 | 49 | I can feel the cool paper on my cheek. I didn't\n |
| 0x2556f3 | 49 | go in with much of a plan, but it's the perfect\n |
| 0x255725 | 5 | size. |
| 0x25572b | 48 | Vision's clear. It's been properly positioned,\n |
| 0x25575c | 42 | so it's not going to fall off that easily. |
| 0x255787 | 39 | Next are... the clothes, right, OK...\n |
| 0x2557af | 35 | If I recall, earlier he was just... |
| 0x2557d3 | 48 | I walk over to the drawers in the corner, mask\n |
| 0x255804 | 48 | still on, and take out some of Oshtor's clothes. |
| 0x255835 | 47 | That should do it... This is actually turning\n |
| 0x255865 | 18 | out pretty good... |
| 0x255878 | 43 | I quickly move to the mirror, and see the\n |
| 0x2558a4 | 44 | spitting image of Oshtor looking back at me. |
| 0x2558d1 | 21 | Uh... ahem... Ahhh... |
| 0x2558e7 | 15 | ...Hm, perfect. |
| 0x2558f7 | 48 | So I'm not a great impressionist, but the mask\n |
| 0x255928 | 47 | is almost identical. I think I deserve points\n |
| 0x255958 | 9 | for that. |
| 0x255962 | 47 | I'll have a little fun with Nekone with this.\n |
| 0x255992 | 45 | Though she'll probably see right through it\n |
| 0x2559c0 | 12 | instantly... |
| 0x2559cd | 47 | Not like I have anything better to do anyway.\n |
| 0x2559fd | 31 | No harm in having a little fun. |
| 0x255a1d | 46 | Ahhh... let's see. Ahem! Nekone... thank you\n |
| 0x255a4c | 19 | for your hard work. |
| 0x255a60 | 30 | I have returned, dear brother. |
| 0x255a7f | 6 | NWUH!? |
| 0x255a86 | 46 | I nearly jump in surprise as I suddenly hear\n |
| 0x255ab5 | 30 | Nekone's voice from behind me. |
| 0x255ad4 | 27 | ...Is something the matter? |
| 0x255af0 | 42 | N-Nekone. How long have you been there...? |
| 0x255b1b | 42 | I have just now arrived. You seem rather\n |
| 0x255b46 | 23 | surprised by my return. |
| 0x255b5e | 45 | I was merely lost in thought. I'm sor--I am\n |
| 0x255b8c | 30 | sorry not to have noticed you. |
| 0x255bab | 43 | I see... You have been working quite hard\n |
| 0x255bd7 | 47 | lately. Perhaps you need to take a rest for a\n |
| 0x255c07 | 7 | change. |
| 0x255c0f | 48 | I will consider it. However, I am far too busy\n |
| 0x255c40 | 47 | at the moment... It is difficult to find time\n |
| 0x255c70 | 9 | for rest. |
| 0x255c7a | 37 | ...You always say that, dear brother. |
| 0x255ca0 | 46 | In any case, I will now deliver my report on\n |
| 0x255ccf | 41 | the cultivable herbs I was investigating. |
| 0x255cf9 | 46 | Herbs... So that's what she was doing for him? |
| 0x255d28 | 46 | It took some time, but I believe I have been\n |
| 0x255d57 | 49 | able to summarize the distribution. This is all\n |
| 0x255d89 | 9 | the data. |
| 0x255d93 | 46 | I took care to concentrate my search on ones\n |
| 0x255dc2 | 38 | suitable for cultivation in Ennakamuy. |
| 0x255de9 | 48 | One lengthy file after another is piled on top\n |
| 0x255e1a | 42 | of the desk before me; a mountain of text. |
| 0x255e45 | 45 | ...I am impressed that you found this much.\n |
| 0x255e73 | 42 | This data is clearly beyond one person's\n |
| 0x255e9e | 8 | efforts. |
| 0x255ea7 | 48 | Dear sister told me of them. One can only find\n |
| 0x255ed8 | 44 | so much from books, so I asked her and she\n |
| 0x255f05 | 10 | obliged... |
| 0x255f10 | 49 | Apparently this kind of information falls under\n |
| 0x255f42 | 48 | trade secrets, but she made an exception for me. |
| 0x255f73 | 20 | I see, so Kuon did-- |
| 0x255f88 | 8 | ...Kuon? |
| 0x255f91 | 26 | Ah, I... I mean Lady Kuon. |
| 0x255fac | 48 | ...So that explains why Kuon kept holing up in\n |
| 0x255fdd | 37 | her room and throwing her jobs at me. |
| 0x256003 | 49 | If we can cultivate a number of the more potent\n |
| 0x256035 | 46 | herbs, I believe Ennakamuy can profit greatly. |
| 0x256064 | 46 | I had dear sister mix one as a sample. Here,\n |
| 0x256093 | 47 | dear brother. You have been so busy--this may\n |
| 0x2560c3 | 7 | help... |
| 0x2560cb | 48 | Hm... I don't believe that I am pushing myself\n |
| 0x2560fc | 9 | too hard. |
| 0x256106 | 47 | ...You must see that if you fall ill, it will\n |
| 0x256136 | 42 | cause problems for others. You must take\n |
| 0x256161 | 12 | better care. |
| 0x25616e | 46 | I suppose you are right. I will try to pay a\n |
| 0x25619d | 39 | little more attention to my well-being. |
| 0x2561c9 | 29 | ...And about my next report-- |
| 0x2561e7 | 48 | Hold on a sec. She's acting just like she does\n |
| 0x256218 | 46 | with Oshtor. Has she really not noticed that\n |
| 0x256247 | 8 | it's me? |
| 0x256250 | 46 | ...Maybe I'll keep it up for a while longer.\n |
| 0x25627f | 48 | I'm wondering how long I can get away with this. |
| 0x2562b0 | 48 | ...And that will be all. Is there anything you\n |
| 0x2562e1 | 19 | wish me to clarify? |
| 0x2562f5 | 47 | No, you have done well. By the way, Nekone...\n |
| 0x256325 | 42 | are you pressed for time at all right now? |
| 0x256350 | 48 | No, I currently don't have... anything planned\n |
| 0x256381 | 14 | at the moment. |
| 0x256390 | 32 | Then come over here for a while. |
| 0x2563b1 | 10 | Uh... Ah!? |
| 0x2563bc | 47 | I pick up Nekone as she comes closer, and put\n |
| 0x2563ec | 28 | her on my lap like Ukon did. |
| 0x256409 | 16 | D-Dear brother!? |
| 0x25641a | 48 | You have done well to complete the task I have\n |
| 0x25644b | 47 | given you. You must be weary from your efforts. |
| 0x25647b | 28 | Um... Dear brother, I, uh... |
| 0x256498 | 46 | Nekone protests, but doesn't try to get away\n |
| 0x2564c7 | 32 | as I gently pat her on the head. |
| 0x2564e8 | 46 | Did you not like this? I am sorry, I did not\n |
| 0x256517 | 37 | intend to cause you any discomfort... |
| 0x25653d | 40 | N-No... It's just, this was so sudden.\n |
| 0x256566 | 26 | I was not prepared for it. |
| 0x256581 | 48 | Um... why are you suddenly doing such things...? |
| 0x2565b2 | 27 | Do you wish for me to stop? |
| 0x2565ce | 43 | I believe a brother should need no reason\n |
| 0x2565fa | 21 | to praise his sister. |
| 0x256610 | 46 | Of course, if you truly wish for me to stop,\n |
| 0x25663f | 22 | I shall do so at once. |
| 0x256656 | 35 | ...I would... like you to continue. |
| 0x25667a | 48 | Nekone seems very relaxed, and lets me pat her\n |
| 0x2566ab | 45 | head as she closes her eyes, clearly content. |
| 0x2566d9 | 50 | I apologize. I have not been able to make enough\n |
| 0x25670c | 33 | time to spend with you like this. |
| 0x25672e | 10 | That is... |
| 0x256739 | 47 | But you may ask whatever you wish of me right\n |
| 0x256769 | 32 | now. You need hold no whim back. |
| 0x25678a | 13 | ...All right. |
| 0x256798 | 41 | Let's see. How about something like this? |
| 0x2567c2 | 45 | I decide to lightly rub my finger under her\n |
| 0x2567f0 | 48 | chin, like one would to a cat, to see how that\n |
| 0x256821 | 5 | goes. |
| 0x256827 | 22 | M-Mmf. That tickles... |
| 0x25683e | 14 | Should I stop? |
| 0x25684d | 46 | Nekone doesn't say anything, but she leans a\n |
| 0x25687c | 14 | little closer. |
| 0x25688b | 33 | I decide to try doing it again... |
| 0x2568ad | 39 | Nekone leans, tilting her head into it. |
| 0x2568d5 | 48 | She closes her drooping eyes, her face a blend\n |
| 0x256906 | 27 | of embarrassment and bliss. |
| 0x256922 | 42 | She'd never act like this if I tried it.\n |
| 0x25694d | 45 | She'd probably glare daggers and kick me in\n |
| 0x25697b | 10 | the shins. |
| 0x256986 | 48 | But... Mwa ha ha! Little do you know, this man\n |
| 0x2569b7 | 45 | is not Oshtor! You have lowered your guard,\n |
| 0x2569e5 | 5 | girl! |
| 0x2569eb | 23 | I shall do as I please! |
| 0x256a03 | 17 | Ah!? Th-That's... |
| 0x256a15 | 45 | Nekone jumps a little in surprise. My hands\n |
| 0x256a43 | 43 | settle over her ears, gently stroking them. |
| 0x256a6f | 29 | Hmm... Do you not wish me to? |
| 0x256a8d | 19 | Uh, er... um... ah! |
| 0x256aa1 | 47 | D-Dear brother... the ears are... a bit much... |
| 0x256ad1 | 47 | I apologize. I did not realize it would cause\n |
| 0x256b01 | 13 | you distress. |
| 0x256b0f | 27 | It... tickles too much...\n |
| 0x256b2b | 15 | If you could... |
| 0x256b3b | 45 | I see. I am sorry to have thus surprised you. |
| 0x256b69 | 10 | Oh, but... |
| 0x256b74 | 44 | Nekone stops me as I lift my hands from her. |
| 0x256ba1 | 44 | ...But I do not mind you patting me on the\n |
| 0x256bce | 26 | head... I would like that. |
| 0x256be9 | 48 | Nekone gently rubs her head against my hand as\n |
| 0x256c1a | 11 | she speaks. |
| 0x256c26 | 44 | Sh-She's... actually kinda cute like this.\n |
| 0x256c53 | 47 | I think I get why Mikazuchi wants to pet her... |
| 0x256c83 | 46 | ...But it's not over yet. I won't let it end\n |
| 0x256cb2 | 15 | just like this. |
| 0x256cc2 | 39 | As I let Nekone lean on me and relax,\n |
| 0x256cea | 36 | I withdraw something from my pocket. |
| 0x256d0f | 40 | Nekone. I received some treats... some\n |
| 0x256d38 | 31 | delicacies as a reward earlier. |
| 0x256d58 | 14 | Delicacies...? |
| 0x256d67 | 30 | I had saved it just for you.\n |
| 0x256d86 | 20 | Would you like some? |
| 0x256d9b | 34 | Huh? Oh, yes... I would love some. |
| 0x256dbe | 48 | Good. I have plenty, so eat as much as you like. |
| 0x256def | 19 | Yes... thank you... |
| 0x256e03 | 48 | As she reaches for the sweets, I stop her hand\n |
| 0x256e34 | 10 | with mine. |
| 0x256e3f | 20 | ...Um, dear brother? |
| 0x256e54 | 27 | Here, Nekone... Say "ahhh." |
| 0x256e70 | 4 | Huh? |
| 0x256e75 | 11 | Say "ahhh." |
| 0x256e81 | 41 | I-I can eat on my own. I am not a child\n |
| 0x256eab | 10 | anymore... |
| 0x256eb6 | 44 | Consider this a reward for your hard work.\n |
| 0x256ee3 | 28 | No need to be modest, hm...? |
| 0x256f00 | 7 | Nngh... |
| 0x256f08 | 10 | "Ahhh"...? |
| 0x256f13 | 47 | J-Just this once... Since nobody is watching... |
| 0x256f43 | 9 | A-Ahhh... |
| 0x256f4d | 7 | *Munch* |
| 0x256f55 | 42 | Nekone stays silent, but I can see she's\n |
| 0x256f80 | 8 | beaming. |
| 0x256f89 | 11 | Is it good? |
| 0x256f95 | 44 | Yes, very... It is... very sweet, and just\n |
| 0x256fc2 | 21 | melts in the mouth... |
| 0x256fd8 | 12 | Can I, ah... |
| 0x256fe5 | 50 | ...Hah. I did say there is no need to be modest.\n |
| 0x257018 | 31 | There is plenty more. "Ahhh"... |
| 0x257038 | 7 | Ahhh... |
| 0x257040 | 35 | I feed Nekone more and more sweets. |
| 0x257064 | 46 | I guess that's something you don't see every\n |
| 0x257093 | 41 | day... A valuable experience, to be sure. |
| 0x2570bd | 46 | ...Um, you seem a bit... unusual today, dear\n |
| 0x2570ec | 28 | brother. Is something amiss? |
| 0x257109 | 26 | ...Do you find it strange? |
| 0x257124 | 46 | Well, yes. You usually do not do such things\n |
| 0x257153 | 22 | in that... appearance. |
| 0x25716a | 46 | When you treat me like this, it almost feels\n |
| 0x257199 | 44 | as if you are a completely different person. |
| 0x2571c6 | 48 | I thought it would make a good change of pace.\n |
| 0x2571f7 | 39 | It is nice to have times like this, no? |
| 0x25721f | 46 | And besides, you said so yourself. No one is\n |
| 0x25724e | 46 | watching. So no worries--I mean, there is no\n |
| 0x25727d | 14 | need to worry. |
| 0x25728c | 19 | Um... Dear brother? |
| 0x2572a0 | 39 | Or perhaps you do not like it when...\n |
| 0x2572c8 | 21 | I treat you this way? |
| 0x2572de | 23 | ...No, that's not true. |
| 0x2572f6 | 45 | I see... Well, there are still these sweets\n |
| 0x257324 | 31 | left. Would you like some more? |
| 0x257344 | 32 | Yes... I would like some more.\n |
| 0x257365 | 25 | {W270}Dear... brother...? |
| 0x25737f | 50 | Nekone falters as she seems to notice something,\n |
| 0x2573b2 | 28 | and she suddenly freezes up. |
| 0x2573cf | 29 | What happened? What are you-- |
| 0x2573ed | 32 | I follow Nekone's gaze to find-- |
| 0x25740e | 6 | ...Oh. |
| 0x257415 | 47 | Oshtor leans on the doorframe, grinning as he\n |
| 0x257445 | 22 | watches the two of us. |
| 0x25745c | 46 | Dear... brother? But... But he's right here... |
| 0x25748b | 49 | ...You have returned, Oshtor. It seems you were\n |
| 0x2574bd | 36 | much swifter than I had anticipated. |
| 0x2574e2 | 48 | Yes, it was much briefer than I imagined it to\n |
| 0x257513 | 48 | be. But it would seem I am intruding on you two. |
| 0x257544 | 15 | Huh...? Wha...? |
| 0x257554 | 47 | Not at all. I believe I have found a fine way\n |
| 0x257584 | 20 | to entertain myself. |
| 0x257599 | 48 | I was able to see a side of Nekone that I have\n |
| 0x2575ca | 44 | never seen before. It was time well spent,\n |
| 0x2575f7 | 7 | indeed. |
| 0x2575ff | 24 | Um... What is... Huh...? |
| 0x257618 | 46 | I too wished to watch a little longer. It is\n |
| 0x257647 | 37 | rare to see my sister this unguarded. |
| 0x25766d | 48 | That is most likely because you always talk of\n |
| 0x25769e | 45 | how busy you are, and neglect spending time\n |
| 0x2576cc | 9 | with her. |
| 0x2576d6 | 50 | I see. Perhaps you are right. I may have devoted\n |
| 0x257709 | 44 | a little too much of my time to matters of\n |
| 0x257736 | 8 | state... |
| 0x25773f | 47 | Your chance has not yet passed. You should do\n |
| 0x25776f | 37 | the same to her, when next you have\n |
| 0x257795 | 12 | opportunity. |
| 0x2577a2 | 32 | Hah. I suppose you have a point. |
| 0x2577c3 | 47 | D-Dear brother... What exactly is the meaning\n |
| 0x2577f3 | 11 | of this...? |
| 0x2577ff | 45 | What? You have not unraveled the mystery yet? |
| 0x25782d | 44 | Figured it out...? But I see two of you...\n |
| 0x25785a | 42 | But only one of you can be the real one... |
| 0x257885 | 45 | But you are my dear brother, and he is you.\n |
| 0x2578b3 | 12 | Which is...? |
| 0x2578c0 | 46 | So it seems that you believe I, the occupant\n |
| 0x2578ef | 37 | of this room, am your brother Oshtor. |
| 0x257915 | 11 | However...! |
| 0x257921 | 42 | The truth comes out! This is the man you\n |
| 0x25794c | 37 | believed to be your trueborn brother! |
| 0x257972 | 45 | H-H-H-Haku...!? My dear brother turned into\n |
| 0x2579a0 | 9 | HAKU...!? |
| 0x2579aa | 45 | Nekone's eyes widen in shock, and she looks\n |
| 0x2579d8 | 37 | back and forth between me and Oshtor. |
| 0x2579fe | 46 | Mwuhahahaha! Even I didn't think it would go\n |
| 0x257a2d | 10 | this well. |
| 0x257a38 | 46 | If even Nekone couldn't tell us apart, maybe\n |
| 0x257a67 | 41 | I'd make the perfect body double for you. |
| 0x257a91 | 36 | Oh...? You might be on to something. |
| 0x257ab6 | 34 | ...Wait. Shit. Forget I said that. |
| 0x257ad9 | 5 | Hm... |
| 0x257adf | 50 | Stop looking so pensive! I know you just want me\n |
| 0x257b12 | 47 | to handle all the work so you can go full Ukon. |
| 0x257b42 | 7 | Hm...!? |
| 0x257b4a | 49 | Something wrong, Oshtor? Why're you backing off\n |
| 0x257b7c | 10 | like that? |
| 0x257b87 | 45 | Well, there is something that has caught my\n |
| 0x257bb5 | 12 | attention... |
| 0x257bc2 | 18 | Yeah? What's that? |
| 0x257bd5 | 44 | I would recommend... that you take care to\n |
| 0x257c02 | 17 | guard your flank. |
| 0x257c14 | 16 | Hm? My... flank? |
| 0x257c25 | 51 | As I look back, the last thing I see is Nekone...\n |
| 0x257c59 | 37 | raising her staff as high as she can. |
| 0x257c7f | 12 | Uh, Nekone-- |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_07.json` com a forma:
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
