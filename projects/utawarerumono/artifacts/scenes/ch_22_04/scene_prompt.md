# Cena ch_22_04 — pacote de traducao (1066 linhas)

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
| amam | Item | amam | manter_original | none |
| Aruruu | Personagem | Aruruu | manter_original | moderate |
| Camyu | Personagem | Camyu | manter_original | moderate |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Cloister | Local | Claustro Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `day.` -> `dia.` (SYSTEM, 20_18)
- `them.` -> `deles.` (Kuon, 11_05)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `*Gulp*` -> `*Gole*` (Haku, 17_01)
- `face?` -> `rosto?` (Ougi, 19_08)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `wall.` -> `parede.` (Haku, 17_04)
- `Urk...` -> `Argh...` (Haku, 12_06)
- `...Oh.` -> `...Ah.` (Haku, 13_03)
- `...Who the--` -> `Q--Quem é--` (Protagonista, 19_01)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Nnngh...` -> `Nnh...` (Protagonista, 17_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `much.` -> `isso.` (Ukon, 13_09)
- `her.` -> `a ela.` (Kuon, 11_02)
- `that?` -> `né?` (Haku, 14_09)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `it.` -> `aí.` (Haku, 15_03)
- `this.` -> `essa.` (Moznu, 13_05)
- `questions.` -> `perguntas.` (Homem, 20_05)
- `then?` -> `então?` (Kuon, 16_02)
- `person.` -> `terrível.` (Nekone, 15_03)
- `sister.` -> `irmã.` (Ukon, 14_04)
- `sisters.` -> `irmãs.` (Protagonista, 17_01)
- `situation.` -> `ruim.` (Kuon, 11_02)
- `Ohhh...` -> `Ohhh...` (Haku, 19_06)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `I think.` -> `acho.` (Kuon, 12_11)
- `earlier.` -> `antes.` (Kuon, 11_02)
- `take care of.` -> `cuidar de.` (Ukon, 16_01)
- `Uh, Kuon?` -> `Hm, Kuon?` (Haku, 13_02)
- `*FWUMPH*` -> `*PLUFT*` (Haku, 18_01)
- `Eek!?` -> `Iiih!?` (Rulutieh, 21_03)
- `time.` -> `vez.` (Raurau, 18_01)
- `Excuse me.` -> `Com licença.` (Mikazuchi, 19_07)
- `like this...` -> `assim...` (Rulutieh, 17_01)
- `country.` -> `país.` (Haku, 17_01)
- `perspective.` -> `se fechar.` (Ukon, 15_01)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `Sure thing.` -> `Claro.` (Ukon, 20_21)
- `Nnnngh...` -> `Nnh...` (Nekone, 18_01)
- `a little more.` -> `um pouco mais.` (Garota, 18_01)
- `Yeah.` -> `É.` (Haku, 15_04)
- `Hmph...` -> `Hmph...` (Nekone, 16_02)
- `speaks.` -> `fala.` (Haku, 19_07)
- `Yes.` -> `Sim.` (Haku, 17_01)
- `enough...` -> `o suficiente...` (Haku, 19_08)
- `down.` -> `andem.` (Ukon, 15_05)
- `Er...` -> `É...` (Garota, 17_01)
- `...Kuon?` -> `...Kuon?` (Haku, 11_11)
- `Yes?` -> `Sim?` (Yuuri, 16_05)
- `Whew...` -> `Ufa...` (Haku, 18_01)
- `though.` -> `porém.` (Kuon, 12_04)
- `*Slurp*...` -> `*Golo*...` (Haku, 18_01)
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
| 0x237c12 | 43 | Dammit, Kuon. Where the hell did you go...? |
| 0x237c3e | 43 | Several days after the Tuskur ambassadors\n |
| 0x237c6a | 35 | arrived at the Imperial Cloister... |
| 0x237c8e | 50 | Just as Ukon asked, we stick to our mundane jobs\n |
| 0x237cc1 | 46 | while we observe the Tuskur ambassadors each\n |
| 0x237cf0 | 4 | day. |
| 0x237cf5 | 44 | However, ever since we took this job, Kuon\n |
| 0x237d22 | 40 | always finds some excuse to go work on\n |
| 0x237d4b | 15 | something else. |
| 0x237d5b | 44 | Needless to say, it usually falls to me to\n |
| 0x237d88 | 18 | pick up her slack. |
| 0x237d9b | 43 | Well, on the bright side, the ambassadors\n |
| 0x237dc7 | 36 | themselves seem pretty good-natured. |
| 0x237dec | 49 | Even though we're basically their minions, they\n |
| 0x237e1e | 44 | don't treat us with contempt or overwork us. |
| 0x237e4b | 49 | But since they're all such hard workers, I feel\n |
| 0x237e7d | 44 | bad when we're not working just as hard as\n |
| 0x237eaa | 5 | them. |
| 0x237eb0 | 49 | Didn't get to have a proper lunch today because\n |
| 0x237ee2 | 10 | of that... |
| 0x237eed | 50 | And I haven't caught a glimpse of those beauties\n |
| 0x237f20 | 47 | from the procession. Might be holed up in the\n |
| 0x237f50 | 12 | backrooms... |
| 0x237f5d | 17 | *Crack, crack*... |
| 0x237f6f | 37 | Ugh, this job gets no perks at all.\n |
| 0x237f95 | 11 | This sucks. |
| 0x237fa1 | 47 | ...Man, I'm hungry. Maybe I'll grab something\n |
| 0x237fd1 | 47 | from the kitchens real quick before I head to\n |
| 0x238001 | 8 | my room. |
| 0x23800a | 3 | Hm? |
| 0x23800e | 14 | ...What the... |
| 0x23801d | 47 | I'm confronted with butt... I mean, with half\n |
| 0x23804d | 43 | a woman's body stuck in the kitchen window. |
| 0x238079 | 46 | She's wriggling around like she's struggling\n |
| 0x2380a8 | 8 | to move. |
| 0x2380b1 | 44 | Did she try to climb through, but get stuck? |
| 0x2380de | 8 | *Fwoomp* |
| 0x2380e7 | 44 | With that, the butt--and, uh, the attached\n |
| 0x238114 | 32 | person--slips out of the window. |
| 0x238139 | 13 | ...Good haul. |
| 0x238147 | 49 | The woman before me cradles an armful of puffs,\n |
| 0x238179 | 41 | which she pops into her mouth one by one. |
| 0x2381a3 | 6 | ...Hm? |
| 0x2381aa | 5 | Oh... |
| 0x2381b0 | 36 | We stare at each other in silence.\n |
| 0x2381d5 | 25 | A couple seconds tick by. |
| 0x2381ef | 32 | ...*nomf* *nomf* *nomf* *nomf*\n |
| 0x238210 | 20 | *nomf* *nomf* *nomf* |
| 0x238225 | 47 | And the puffs begin to disappear at lightning\n |
| 0x238255 | 6 | speed. |
| 0x23825c | 45 | Hey, wait a minute! That was supposed to be\n |
| 0x23828a | 20 | our snack for today! |
| 0x23829f | 6 | *Gulp* |
| 0x2382a6 | 46 | And with that, the final one disappears into\n |
| 0x2382d5 | 18 | the woman's mouth. |
| 0x2382e8 | 29 | ...What're you talking about? |
| 0x238306 | 47 | Do you really think you can talk your way out\n |
| 0x238336 | 45 | of this with all that kondens all over your\n |
| 0x238364 | 5 | face? |
| 0x23836a | 7 | *Slurp* |
| 0x238372 | 46 | The beautiful woman sticks out her tongue to\n |
| 0x2383a1 | 20 | lap up the remnants. |
| 0x2383b6 | 49 | I'm sure it sounds alluring in theory, but it's\n |
| 0x2383e8 | 45 | not the most attractive thing I've ever seen. |
| 0x238416 | 21 | Evidence disposed of. |
| 0x23842c | 48 | She just blatantly got rid of all the evidence\n |
| 0x23845d | 47 | when I'm standing right here in front of her... |
| 0x23848d | 46 | She suddenly approaches me and puts her face\n |
| 0x2384bc | 24 | right next to my collar. |
| 0x2384d5 | 20 | ... *Sniff, sniff*\n |
| 0x2384ea | 20 | *Sniff, sniff sniff* |
| 0x2384ff | 20 | U-Uh, what are you-- |
| 0x238514 | 13 | ...Found her. |
| 0x238522 | 4 | Huh? |
| 0x238527 | 11 | Where's Ku? |
| 0x238533 | 6 | ...Ku? |
| 0x23853a | 28 | What the fresh hell is a Ku? |
| 0x238557 | 18 | You smell like Ku. |
| 0x23856a | 49 | Smell like...? I don't even know what she means\n |
| 0x23859c | 46 | by "Ku" in the first place. I don't know any-- |
| 0x2385cb | 36 | Excuse me. I must pass behind you... |
| 0x2385f0 | 8 | Huh? Oh. |
| 0x2385f9 | 50 | A worker gives me a polite warning as she passes\n |
| 0x23862c | 46 | me, carrying stacked trays with meals on them. |
| 0x23865b | 13 | Oops. My bad. |
| 0x238669 | 38 | No need to apologize. Excuse me, then. |
| 0x238690 | 45 | The worker peeks out from behind the trays,\n |
| 0x2386be | 31 | with a small nod of deference-- |
| 0x2386e5 | 12 | She freezes. |
| 0x2386f2 | 19 | A... Ar... Aru...!? |
| 0x238706 | 4 | Aru? |
| 0x23870b | 42 | The worker quickly hides back behind the\n |
| 0x238736 | 6 | trays. |
| 0x23873d | 6 | Hmmmm? |
| 0x238744 | 48 | The woman called Aru leans over to peek around\n |
| 0x238775 | 10 | the trays. |
| 0x238780 | 9 | *Shuffle* |
| 0x23878a | 45 | But the worker plants her back to the wall,\n |
| 0x2387b8 | 47 | and slowly tries to leave while hidden behind\n |
| 0x2387e8 | 5 | Hm... |
| 0x2387ee | 43 | Aru (?) stands in front of the worker and\n |
| 0x23881a | 38 | crouches down to look from below the\n |
| 0x238841 | 48 | Immediately, the worker shifts to the opposite\n |
| 0x238872 | 5 | wall. |
| 0x238878 | 49 | This Aru, in turn, blocks her way by continuing\n |
| 0x2388aa | 36 | to shuffle along her back and sides. |
| 0x2388cf | 6 | Urk... |
| 0x2388d6 | 21 | ...What're you doing? |
| 0x2388ec | 30 | Please, do not look upon me!\n |
| 0x23890b | 14 | Not like this! |
| 0x23891a | 47 | The worker falls to the ground with her hands\n |
| 0x23894a | 34 | over her head, groaning something. |
| 0x23896d | 44 | Aru responds only with a tilt of her head,\n |
| 0x23899a | 46 | looking down at her with a puzzled expression. |
| 0x2389c9 | 37 | What the hell are these two doing...? |
| 0x2389ef | 47 | I don't really get what's going on, but I can\n |
| 0x238a1f | 47 | tell getting involved in this would be a huge\n |
| 0x238a4f | 7 | hassle. |
| 0x238a57 | 29 | Better let sleeping dogs lie. |
| 0x238a75 | 47 | I'm not sure what this all means, but staying\n |
| 0x238aa5 | 47 | will do me no good, so I take the opportunity\n |
| 0x238ad5 | 12 | for an exit. |
| 0x238ae2 | 40 | ...Dammit. Missed my chance to get food. |
| 0x238b0b | 37 | But who the hell was that just now?\n |
| 0x238b31 | 22 | Felt kinda familiar... |
| 0x238b48 | 6 | ...Oh. |
| 0x238b4f | 42 | She was one of those beauties from Tuskur. |
| 0x238b7a | 41 | But what's she doing at the Hakurokaku?\n |
| 0x238ba4 | 31 | And what did she mean by Ku...? |
| 0x238bc4 | 50 | And now I'm even hungrier, but I don't have much\n |
| 0x238bf7 | 49 | of a choice if the snacks are gone... I'll wait\n |
| 0x238c29 | 12 | 'til dinner. |
| 0x238c36 | 51 | You know what they say. The secret to good health\n |
| 0x238c6a | 51 | is a nice bath, a morning drink, and a long nap--\n |
| 0x238c9e | 15 | Mmmm... *Snore* |
| 0x238cae | 12 | ...Who the-- |
| 0x238cbb | 48 | I pull back the sheets to reveal an unfamiliar\n |
| 0x238cec | 44 | woman, lying spread-eagled with belly bared. |
| 0x238d19 | 28 | This... IS my room... right? |
| 0x238d36 | 43 | Why the hell is someone I've never seen--\n |
| 0x238d62 | 46 | wait a minute. Maybe I HAVE seen her before... |
| 0x238d91 | 46 | Right, it must be the other one of those two\n |
| 0x238dc0 | 9 | beauties. |
| 0x238dca | 15 | Beautiful woman |
| 0x238dda | 22 | *Snore*... zzz... nmm. |
| 0x238df1 | 22 | *Scratch* *scratch*... |
| 0x238e08 | 47 | She scratches her exposed stomach, blissfully\n |
| 0x238e38 | 36 | oblivious as she continues to sleep. |
| 0x238e5d | 41 | She's gorgeous all right, but... I dunno. |
| 0x238e87 | 48 | Seeing a beautiful woman sleeping like this is\n |
| 0x238eb8 | 36 | a little... you know. Disappointing. |
| 0x238edd | 35 | What do I do? Should I wake her up? |
| 0x238f01 | 20 | Disappointing beauty |
| 0x238f16 | 7 | ...Mmm. |
| 0x238f1e | 10 | *Boing*... |
| 0x238f29 | 7 | Nngh... |
| 0x238f31 | 43 | However disappointing the sight is, she's\n |
| 0x238f5d | 15 | still gorgeous. |
| 0x238f6d | 45 | And the way she's breathing is accentuating\n |
| 0x238f9b | 47 | her, uh... assets. I hesitate, unsure of what\n |
| 0x238fcb | 6 | to do. |
| 0x238fd2 | 8 | Nnngh... |
| 0x238fdb | 48 | As I stand there dithering, the disappointing-\n |
| 0x23900c | 42 | yet-beautiful woman's eyes flutter, then\n |
| 0x239037 | 12 | slowly open. |
| 0x239044 | 18 | Good. She's awake. |
| 0x239057 | 24 | *Yawn* Welcome back, Ku. |
| 0x239070 | 3 | Ku? |
| 0x239074 | 46 | This Ku person again? As I puzzle over this,\n |
| 0x2390a3 | 39 | she sits up properly, rubbing her eyes. |
| 0x2390cb | 46 | What took you so long, Ku? I've been waiting\n |
| 0x2390fa | 16 | this whole time. |
| 0x23910b | 47 | You traveled so far away from us, didn't even\n |
| 0x23913b | 36 | send any letters... I was so worri-- |
| 0x239160 | 7 | ...Huh? |
| 0x239168 | 17 | M-Mister... Hak-- |
| 0x23917a | 42 | She then blinks several times and stares\n |
| 0x2391a5 | 16 | carefully at me. |
| 0x2391b6 | 31 | Waaaah!? Wh-Why aren't you Ku!? |
| 0x2391d6 | 43 | That's kind of a hard question to answer.\n |
| 0x239202 | 39 | And I should be asking the questions!\n |
| 0x23922a | 23 | Why are you in my room? |
| 0x239242 | 42 | That's my bed you're sitting in right now. |
| 0x23926d | 22 | This isn't Ku's room!? |
| 0x239284 | 44 | I dunno who this Ku person is, but my name\n |
| 0x2392b1 | 44 | sure as hell isn't Ku. I can tell you that\n |
| 0x2392de | 5 | much. |
| 0x2392e4 | 45 | But why? I was sure I tracked Ku's presence\n |
| 0x239312 | 10 | to here... |
| 0x23931d | 46 | Who would've thought that the ambassadors of\n |
| 0x23934c | 26 | Tuskur would show up here. |
| 0x239367 | 28 | How do you know about that!? |
| 0x239384 | 46 | She drew quite a lot of attention during the\n |
| 0x2393b3 | 48 | procession, so I'm sure anyone would recognize\n |
| 0x2393e4 | 4 | her. |
| 0x2393e9 | 47 | I thought she might be some kind of operative\n |
| 0x239419 | 42 | using the ambassador title as a front...\n |
| 0x239444 | 12 | I guess not. |
| 0x239451 | 45 | Or is she just acting like this to fool me?\n |
| 0x23947f | 45 | Is this all part of some genius master plan\n |
| 0x2394ad | 11 | of hers...? |
| 0x2394b9 | 36 | Maybe I should go call for somebody. |
| 0x2394de | 44 | What do I do? If word gets out about this... |
| 0x23950b | 25 | I guess I have no choice. |
| 0x239543 | 4 | Yah! |
| 0x239548 | 19 | Wh... What in the-- |
| 0x23955c | 26 | Whew... That should do it. |
| 0x239577 | 46 | Hahaha! Say goodbye to the clueless Camyu of\n |
| 0x2395a6 | 47 | before. See, I can cast an invisibility spell\n |
| 0x2395d6 | 10 | perfectly! |
| 0x2395e1 | 16 | ...Invisibility? |
| 0x2395f2 | 34 | ...Can you, by any chance, see me? |
| 0x239615 | 47 | I don't really get what's going on, but yeah,\n |
| 0x239645 | 10 | I see you. |
| 0x239650 | 13 | HUUUUUUUUUH!? |
| 0x23965e | 46 | What? Why? I've never been spotted with this\n |
| 0x23968d | 44 | before... Oh, if they find out, it'll mean\n |
| 0x2396ba | 12 | big trouble. |
| 0x2396c7 | 46 | Why is she holding her head and moaning like\n |
| 0x2396f6 | 5 | that? |
| 0x2396fc | 45 | I thought this might all be an act, but I'm\n |
| 0x23972a | 47 | starting to think I don't have to worry about\n |
| 0x23975a | 5 | that. |
| 0x239760 | 32 | Fine, if that's the case... Yah! |
| 0x239781 | 6 | *Poke* |
| 0x239788 | 22 | Gaaaaaaaaah! My eyes!! |
| 0x23979f | 14 | Farewell then! |
| 0x2397ae | 36 | Rrrrgh... What in the hell was that? |
| 0x2397d3 | 10 | Eeeeeeek!? |
| 0x2397de | 30 | Wh-Whanyamyaghyowryawhababah!? |
| 0x2397fd | 44 | ...And now she's back. And she's even more\n |
| 0x23982a | 37 | disappointing to look at than before. |
| 0x239850 | 23 | Get it off! Get it off! |
| 0x239868 | 43 | Looks like Kurarin has wrapped itself all\n |
| 0x239894 | 11 | around her. |
| 0x2398a0 | 44 | Huh... That's rare. It's not often Kurarin\n |
| 0x2398cd | 36 | takes a liking to someone like that. |
| 0x2398f2 | 8 | Ewwww... |
| 0x2398fb | 29 | *Jiggle* *jiggle* *jiggle*... |
| 0x239919 | 39 | Sounds like it's in a real good mood.\n |
| 0x239941 | 21 | Must really like you. |
| 0x239957 | 39 | I don't want it to like me this much!\n |
| 0x23997f | 43 | I've never seen anything like it before--\n |
| 0x2399ab | 23 | I just gave it a snack! |
| 0x2399c3 | 46 | Oh, well, there you go. It's not going to do\n |
| 0x2399f2 | 48 | you any harm, so you don't have to worry about\n |
| 0x239a23 | 3 | it. |
| 0x239a27 | 19 | No! I want it off!! |
| 0x239a3b | 45 | Ah, fine. The way she's all bound up is too\n |
| 0x239a69 | 46 | risque anyway. Can't let anyone see her like\n |
| 0x239a98 | 5 | this. |
| 0x239a9e | 30 | ...But man. Just LOOK at them. |
| 0x239abd | 44 | After I finally manage to separate her and\n |
| 0x239aea | 46 | Kurarin, I turn to the teary-eyed woman with\n |
| 0x239b19 | 10 | questions. |
| 0x239b24 | 37 | So you came here looking for someone? |
| 0x239b4a | 34 | Mhm. I came here looking for Ku.\n |
| 0x239b6d | 46 | I don't know how I'd make a mistake like this. |
| 0x239b9c | 37 | Camyu... I mean, Miss Camyu, right?\n |
| 0x239bc2 | 47 | So why exactly did you think this "Ku" was in\n |
| 0x239bf2 | 8 | my room? |
| 0x239bfb | 23 | Scent? And power waves? |
| 0x239c13 | 12 | Power waves? |
| 0x239c20 | 47 | Mhm. How do I explain it? It's a... presence.\n |
| 0x239c50 | 50 | Radiance singular to one person... Like an aura,\n |
| 0x239c83 | 8 | sort of. |
| 0x239c8c | 46 | And this room was full of Ku's, so I thought\n |
| 0x239cbb | 34 | this was her room. I don't get it. |
| 0x239cde | 48 | So this "Ku" you keep talking about is a girl,\n |
| 0x239d0f | 5 | then? |
| 0x239d15 | 47 | Yep! She's the cutest thing in the whole world! |
| 0x239d45 | 43 | I think I know who it might be. I mean, a\n |
| 0x239d71 | 46 | nickname like "Ku" definitely narrows it down. |
| 0x239da0 | 40 | She's pretty and cute and a good girl.\n |
| 0x239dc9 | 47 | Her hair's beautiful and silky and she smells\n |
| 0x239df9 | 20 | good when I hug her. |
| 0x239e0e | 50 | And her voice rings out like the beautiful chime\n |
| 0x239e41 | 48 | of a bell. I love to hear her call out "Sister"! |
| 0x239e72 | 47 | But the best part, the BEST part is her tail!\n |
| 0x239ea2 | 45 | I'd even call it the prettiest in the three\n |
| 0x239ed0 | 6 | lands! |
| 0x239ed7 | 49 | ...I thought I had a guess, but her description\n |
| 0x239f09 | 46 | makes them sound like a completely different\n |
| 0x239f38 | 7 | person. |
| 0x239f40 | 46 | So would this "Ku" person's full name be Kuon? |
| 0x239f6f | 27 | Yep, that's absolutely ri-- |
| 0x239f8b | 6 | wrong! |
| 0x239f92 | 15 | ...Which is it? |
| 0x239fa2 | 43 | Wh-Who is this Kuon person? I don't know!\n |
| 0x239fce | 45 | I've never heard of someone like that before! |
| 0x239ffc | 49 | When your poker face is that bad, it's the same\n |
| 0x23a02e | 46 | as flat-out saying yes. Still, she must have\n |
| 0x23a05d | 14 | her reasons... |
| 0x23a06c | 44 | Well, in any case, judging by how you talk\n |
| 0x23a099 | 46 | about her, you must be really close with Kuon. |
| 0x23a0c8 | 45 | Of course. Ku is everyone's adorable little\n |
| 0x23a0f6 | 7 | sister. |
| 0x23a0fe | 44 | So she's the little sister of someone with\n |
| 0x23a12b | 41 | enough clout to be an ambassador, huh...? |
| 0x23a155 | 46 | I got the feeling she had SOME kind of noble\n |
| 0x23a184 | 18 | background, but... |
| 0x23a197 | 44 | ...Hey! That wasn't fair! That was a trick\n |
| 0x23a1c4 | 9 | question! |
| 0x23a1ce | 48 | I dunno if you could exactly call that a trick\n |
| 0x23a1ff | 11 | question... |
| 0x23a20b | 10 | Nnnnngh... |
| 0x23a216 | 45 | She comes off as kind of cute. Not just her\n |
| 0x23a244 | 31 | looks, but her personality too. |
| 0x23a264 | 47 | Probably not blood-related to Kuon, but I can\n |
| 0x23a294 | 45 | see the similarities. Guess they really are\n |
| 0x23a2c2 | 8 | sisters. |
| 0x23a2cb | 10 | ...Mister? |
| 0x23a2d6 | 7 | Mister? |
| 0x23a2de | 29 | Huh!? Uh... I-It's nothing.\n |
| 0x23a2fc | 15 | Nothing at all! |
| 0x23a30c | 46 | Did she mistake me for someone else? I don't\n |
| 0x23a33b | 40 | think I'm old enough to be a "mister"... |
| 0x23a364 | 24 | Cammie, did you find Ku? |
| 0x23a37d | 5 | Aru-- |
| 0x23a383 | 18 | Hm? Wait, you're-- |
| 0x23a396 | 14 | ...Where's Ku? |
| 0x23a3a5 | 43 | You came here by mistake too, didn't you?\n |
| 0x23a3d1 | 31 | It doesn't look like Ku's here. |
| 0x23a3f1 | 32 | But I can smell Ku's scent here. |
| 0x23a412 | 47 | I don't know why either. But this person here\n |
| 0x23a442 | 49 | seems suspicious. He might know something about\n |
| 0x23a474 | 46 | The disappointing-but-beautiful Camyu stares\n |
| 0x23a4a3 | 32 | directly at me as she says this. |
| 0x23a4c4 | 49 | Yeah, like I'M the suspicious character in this\n |
| 0x23a4f6 | 10 | situation. |
| 0x23a501 | 44 | Well, I guess I do know her... She's kinda\n |
| 0x23a52e | 41 | taking care of me. I owe my life to Kuon. |
| 0x23a558 | 14 | Owe your life? |
| 0x23a567 | 22 | So Ku saved your life? |
| 0x23a57e | 48 | Yeah. When I was left out in the wilderness to\n |
| 0x23a5af | 47 | die, Kuon found me and let me come along with\n |
| 0x23a5df | 47 | Huh!? Wait, does that mean that you're living\n |
| 0x23a60f | 18 | together with Ku!? |
| 0x23a622 | 48 | Standing by each other through thick and thin... |
| 0x23a653 | 48 | Something about that sounds a little off, but... |
| 0x23a684 | 46 | I guess... loosely speaking, that's not wrong? |
| 0x23a6b3 | 45 | S-So you two live together... So the reason\n |
| 0x23a6e1 | 33 | I can sense Ku here so much is... |
| 0x23a703 | 7 | Ohhh... |
| 0x23a70b | 41 | Hold on, I'm getting the feeling you're\n |
| 0x23a735 | 31 | misunderstanding the situation. |
| 0x23a755 | 48 | Gwee hee hee! Man up. You can't wriggle out of\n |
| 0x23a786 | 44 | this! I can sense Ku's waves everywhere in\n |
| 0x23a7b3 | 5 | here. |
| 0x23a7b9 | 44 | I put my sleeve to my nose and take a whiff. |
| 0x23a7e6 | 42 | Don't tell me it's seeped in or something? |
| 0x23a811 | 48 | Love has finally blossomed for Ku. Oh, I don't\n |
| 0x23a842 | 45 | know if I feel happy or sad about all this... |
| 0x23a870 | 6 | ...Hm. |
| 0x23a877 | 46 | I'm telling you, our relationship isn't like\n |
| 0x23a8a6 | 45 | that. Why are you so happy about it, anyways? |
| 0x23a8d4 | 46 | If Kuon really is like your sister, wouldn't\n |
| 0x23a903 | 47 | you be more protective? I mean, I'm just some\n |
| 0x23a933 | 8 | schmuck. |
| 0x23a93c | 40 | If Ku is happy, that's all that matters. |
| 0x23a965 | 47 | Mhm. And besides, Ku's standards for men were\n |
| 0x23a995 | 13 | way too high. |
| 0x23a9a3 | 48 | She'd ignore every single person that tried to\n |
| 0x23a9d4 | 37 | make a move on her. So that's why--\n |
| 0x23a9fa | 14 | wait a minute. |
| 0x23aa09 | 30 | Her standards are so high...\n |
| 0x23aa28 | 14 | So why HIM...? |
| 0x23aa37 | 48 | ...Quit staring at me. And what's with all the\n |
| 0x23aa68 | 9 | mumbling? |
| 0x23aa72 | 20 | Some prefer nettles. |
| 0x23aa87 | 5 | Rude. |
| 0x23aa8d | 47 | As we talk, the one called "Aru" perks up her\n |
| 0x23aabd | 34 | ears suddenly, and sniffs the air. |
| 0x23aae0 | 21 | Something wrong, Aru? |
| 0x23aaf6 | 10 | Ku's back. |
| 0x23ab01 | 26 | Really!? Oh, you're right! |
| 0x23ab1c | 41 | Can they really tell just from the scent? |
| 0x23ab46 | 49 | I listen and hear close footfalls, or creaks of\n |
| 0x23ab78 | 49 | the floor. Someone's coming down the hallway...\n |
| 0x23abaa | 8 | I think. |
| 0x23abb3 | 13 | Cammie, hide. |
| 0x23abc1 | 47 | Aruruu dives into my bed, and Camyu hurriedly\n |
| 0x23abf1 | 12 | follows her. |
| 0x23abfe | 20 | I-It's so cramped... |
| 0x23ac13 | 8 | Bear it. |
| 0x23ac1c | 44 | The two of them burrow under the blankets.\n |
| 0x23ac49 | 43 | I guess it's better than that fishy spell\n |
| 0x23ac75 | 8 | earlier. |
| 0x23ac7e | 50 | ...Has it occurred to either of you that I could\n |
| 0x23acb1 | 15 | just TELL Kuon? |
| 0x23acc1 | 11 | No telling. |
| 0x23accd | 17 | Yeah, no telling! |
| 0x23acdf | 38 | Fine, fine... I'll keep my mouth shut. |
| 0x23ad06 | 46 | Guess I might as well keep this farce going... |
| 0x23ad35 | 50 | Just as the resigned acceptance crosses my mind,\n |
| 0x23ad68 | 32 | the door to my room slides open. |
| 0x23ad89 | 26 | Oh, you were already back. |
| 0x23ada4 | 47 | Yeah. That reminds me, quit going off on your\n |
| 0x23add4 | 47 | own like that. Thanks to you, I've had a hell\n |
| 0x23ae04 | 9 | of a day. |
| 0x23ae0e | 47 | Ahaha, sorry. I had some business I needed to\n |
| 0x23ae3e | 13 | take care of. |
| 0x23ae4c | 49 | I've been working all day today. I'm exhausted... |
| 0x23ae7e | 38 | Hey, Haku... would you do THAT for me? |
| 0x23aea5 | 8 | ...That? |
| 0x23aeae | 10 | Mhm. That. |
| 0x23aeb9 | 49 | Kuon takes a seat, rolling up the bottom of her\n |
| 0x23aeeb | 27 | clothes to reveal her legs. |
| 0x23af07 | 7 | Whoaaa. |
| 0x23af0f | 34 | K-Ku! She's so up-front about it!? |
| 0x23af32 | 29 | ...Was I just hearing things? |
| 0x23af50 | 50 | I can feel two sets of eyes keenly staring at me\n |
| 0x23af83 | 24 | from below the blankets. |
| 0x23af9c | 48 | Usually Kuon picks up on these kinds of things\n |
| 0x23afcd | 19 | really fast, but... |
| 0x23afe1 | 22 | Whew... So, would you? |
| 0x23aff8 | 44 | Kuon, looking pretty exhausted, sticks her\n |
| 0x23b025 | 20 | legs out towards me. |
| 0x23b03a | 43 | Oh, she wants me to massage her legs like\n |
| 0x23b066 | 36 | before. Well, I guess that's fine... |
| 0x23b08b | 48 | Wow... I don't think I've seen Ku so laid-back\n |
| 0x23b0bc | 11 | in a while. |
| 0x23b0c8 | 4 | Mhm. |
| 0x23b0cd | 32 | I can hear you guys, you know... |
| 0x23b0ee | 25 | Oh... Mmf, right there... |
| 0x23b108 | 45 | It's kind of embarrassing knowing I'm being\n |
| 0x23b136 | 20 | watched like this... |
| 0x23b14b | 39 | I continue to follow Kuon's requests,\n |
| 0x23b173 | 24 | massaging down her legs. |
| 0x23b18c | 19 | Nh--Ahhh... Ohhh... |
| 0x23b1a0 | 46 | Whoooaaa--I never thought I'd see the day Ku\n |
| 0x23b1cf | 43 | would let a man touch her legs like that... |
| 0x23b1fb | 10 | Massage... |
| 0x23b206 | 26 | Whew! That enough for you? |
| 0x23b221 | 44 | ...Huh? But that was only a light massage... |
| 0x23b24e | 45 | Do the soles of my feet, too. And I like it\n |
| 0x23b27c | 17 | a little rougher. |
| 0x23b28e | 10 | Rougher... |
| 0x23b299 | 31 | That sounds a little naughty... |
| 0x23b2b9 | 15 | Hmm, naughty... |
| 0x23b2c9 | 17 | Shut up, you two. |
| 0x23b2db | 48 | I dunno if I can massage harder. I already put\n |
| 0x23b30c | 46 | all my strength into this, and that's barely\n |
| 0x23b33b | 16 | enough as it is. |
| 0x23b34c | 23 | Oh, fine. Is this good? |
| 0x23b364 | 38 | Oh, that's it... there... Oh! Mmf...\n |
| 0x23b38b | 31 | Haku, you're so good at this... |
| 0x23b3ab | 9 | Uh, Kuon? |
| 0x23b3b5 | 46 | There's a strangely affectionate tone to her\n |
| 0x23b3e4 | 45 | voice. Her tail slinks around my arm, as if\n |
| 0x23b412 | 13 | urging me on. |
| 0x23b420 | 42 | You can grind a little harder, you know?\n |
| 0x23b44b | 27 | Don't be afraid to go deep. |
| 0x23b467 | 25 | Ku's all grown up now...! |
| 0x23b481 | 34 | She's making the face of an adult. |
| 0x23b4a4 | 45 | ...Oh, goddammit! Would you two stop hiding\n |
| 0x23b4d2 | 22 | and come out already!? |
| 0x23b4e9 | 8 | *Fwumph* |
| 0x23b4f2 | 49 | I finally decide I can't take any more of this,\n |
| 0x23b524 | 42 | and rip off the blankets covering the two. |
| 0x23b54f | 5 | Eek!? |
| 0x23b555 | 47 | The moment Kuon sees the two hiding under the\n |
| 0x23b585 | 45 | blanket, her relaxed expression immediately\n |
| 0x23b5b3 | 8 | shifts-- |
| 0x23b5bc | 10 | NWHAAAAA!? |
| 0x23b5c7 | 16 | *Crrrraaaack*... |
| 0x23b5d8 | 22 | OwowowowowowowowOWOW!! |
| 0x23b5ef | 50 | As she yelps in surprise, her tail tightens into\n |
| 0x23b622 | 27 | a death grip around my arm. |
| 0x23b63e | 44 | Dammit--that HURTS!! Kuon! Let go! Please,\n |
| 0x23b66b | 40 | let--Owowowowow--ghh, it's gonna break-- |
| 0x23b694 | 46 | Wh-Wh-Wh-Why are you--!? When did--!? What!?\n |
| 0x23b6c3 | 34 | What are those two doing here...!? |
| 0x23b6e6 | 41 | Ahahahaha, looks like you found us out... |
| 0x23b710 | 22 | It's been a while, Ku. |
| 0x23b727 | 34 | Don't you "it's been a while" me!! |
| 0x23b74a | 48 | Kuon--your tail--My... My arm--I-I don't think\n |
| 0x23b77b | 33 | it's supposed to bend like that-- |
| 0x23b79d | 45 | I-I am sorry to have, ah, lost my composure\n |
| 0x23b7cb | 43 | like that... S-So, Haku, are they your...\n |
| 0x23b7f7 | 17 | acquaintances...? |
| 0x23b809 | 44 | Ku, I think he's figured it out by now, so\n |
| 0x23b836 | 40 | there's no point in trying to play dumb. |
| 0x23b85f | 49 | I-I'm sure I don't know what you mean, I think... |
| 0x23b891 | 46 | I don't think I've seen you make a face like\n |
| 0x23b8c0 | 26 | that in a while. I'm glad. |
| 0x23b8db | 45 | Would you stop!? You're embarrassing me...!\n |
| 0x23b909 | 47 | I mean, I-I have no idea what you are talking\n |
| 0x23b939 | 6 | about! |
| 0x23b940 | 46 | Oh, Ku. You were so cute and so honest about\n |
| 0x23b96f | 46 | your feelings back then, but things changed... |
| 0x23b99e | 20 | You should trust us. |
| 0x23b9b3 | 49 | I'm getting a lot of flashbacks... to the times\n |
| 0x23b9e5 | 46 | I trusted you and it ended up terrible for me. |
| 0x23ba14 | 44 | Hey, so tell me about him. You're going to\n |
| 0x23ba41 | 36 | introduce me to your man, right, Ku? |
| 0x23ba66 | 48 | He's not my man! I can't imagine how you'd get\n |
| 0x23ba97 | 44 | that impression! My relationship with Haku\n |
| 0x23bac4 | 7 | isn't-- |
| 0x23bacc | 46 | I want to see that honest little Ku one more\n |
| 0x23bafb | 5 | time. |
| 0x23bb01 | 19 | I am ALWAYS honest! |
| 0x23bb15 | 46 | And after that, I heard tales of "Ku's first\n |
| 0x23bb44 | 44 | grocery shopping, but she got lost and wet\n |
| 0x23bb71 | 11 | herself"... |
| 0x23bb7d | 46 | "Ku's rebellious stage and when she ran away\n |
| 0x23bbac | 48 | from home (She came back at sunset because she\n |
| 0x23bbdd | 15 | was hungry)"... |
| 0x23bbed | 47 | "The time Ku had a nightmare and ran all over\n |
| 0x23bc1d | 46 | the house crying (and wetting herself)", and\n |
| 0x23bc4c | 7 | more... |
| 0x23bc54 | 49 | And so, through anecdote after anecdote, Kuon's\n |
| 0x23bc86 | 36 | embarrassing past is revealed to me. |
| 0x23bcab | 13 | That aside... |
| 0x23bcb9 | 40 | My arm is STILL bending the wrong way.\n |
| 0x23bce2 | 44 | It would be great if someone could fix that. |
| 0x23e784 | 26 | Geez, it's getting cold... |
| 0x23e79f | 49 | I finish my shift for night patrol and walk the\n |
| 0x23e7d1 | 36 | back alleys of the imperial capital. |
| 0x23e7f6 | 47 | Even the busiest areas in town are completely\n |
| 0x23e826 | 46 | deserted in the middle of the night like this. |
| 0x23e855 | 27 | God, I could use a snack... |
| 0x23e871 | 47 | Unfortunately I told the others I wouldn't be\n |
| 0x23e8a1 | 43 | needing dinner, since I'd be getting back\n |
| 0x23e8cd | 5 | late. |
| 0x23e8d3 | 46 | It's going to be lonely eating all by myself\n |
| 0x23e902 | 21 | after getting back... |
| 0x23e918 | 46 | As I walk and think to myself, I see a store\n |
| 0x23e947 | 29 | that still has its lights on. |
| 0x23e965 | 49 | I check the contents of my wallet and make sure\n |
| 0x23e997 | 34 | I've got enough to treat myself... |
| 0x23e9ba | 34 | Might as well drop in for a drink. |
| 0x23e9dd | 9 | Pub owner |
| 0x23e9e7 | 6 | Welc-- |
| 0x23e9ee | 17 | ...Oh, hey there! |
| 0x23ea00 | 46 | There aren't any customers aside from me, so\n |
| 0x23ea2f | 35 | I grab a random table and sit down. |
| 0x23ea53 | 47 | I guess one drink for starters, and something\n |
| 0x23ea83 | 19 | on the side to eat. |
| 0x23ea97 | 41 | Gotcha. One random plate coming right up! |
| 0x23eac1 | 47 | A bottle and some salted fish are immediately\n |
| 0x23eaf1 | 19 | placed on my table. |
| 0x23eb05 | 20 | *Glug*...Pffaaaaaah! |
| 0x23eb1a | 48 | I enjoy the taste of a hard-earned drink after\n |
| 0x23eb4b | 35 | work, wondering what else to order. |
| 0x23eb6f | 37 | Warm alcohol's good on cold nights.\n |
| 0x23eb95 | 39 | Some simmered fish or shellfish, too.\n |
| 0x23ebbd | 26 | Might get expensive, but-- |
| 0x23ebdc | 10 | Excuse me. |
| 0x23ebe7 | 33 | May we share this table with you? |
| 0x23ec0f | 46 | I almost spit out my drink as I see the same\n |
| 0x23ec3e | 25 | face on both sides of me. |
| 0x23ec58 | 48 | Twin girls... Wait, maybe boys? They both have\n |
| 0x23ec89 | 31 | very adorable features, anyway. |
| 0x23eca9 | 25 | Yeah, I don't really mi-- |
| 0x23ecc3 | 48 | As I'm answering, I realize that all the other\n |
| 0x23ecf4 | 16 | tables are open. |
| 0x23ed05 | 41 | Uh, are you sure you wouldn't prefer to-- |
| 0x23ed2f | 42 | Before I can finish, the two have seated\n |
| 0x23ed5a | 41 | themselves at the other side of my table. |
| 0x23ed84 | 32 | Young master, please. Over here. |
| 0x23eda5 | 47 | And right between them sits a slim man with a\n |
| 0x23edd5 | 47 | piercing glare, seated directly opposite of me. |
| 0x23ee05 | 40 | A little hard to say no at this point... |
| 0x23ee2e | 14 | Sharp-eyed man |
| 0x23ee41 | 45 | This Young Master of theirs just sits there\n |
| 0x23ee6f | 23 | quietly, looking surly. |
| 0x23ee87 | 48 | I'm guessing those two boys work for him then.\n |
| 0x23eeb8 | 48 | Although I don't know if I'd call him "young"... |
| 0x23eee9 | 47 | Fine, clean clothes... If he's traveling, I'd\n |
| 0x23ef19 | 45 | guess he's an heir or some kind of merchant\n |
| 0x23ef47 | 7 | prince. |
| 0x23ef4f | 48 | But... he's got this air of aggression to him.\n |
| 0x23ef80 | 45 | Maybe from a warrior house, and they're his\n |
| 0x23efae | 40 | squires...? Yeah, something like that... |
| 0x23efd7 | 47 | Anyhow, why the hell is he staring at me like\n |
| 0x23f007 | 47 | that? And he definitely doesn't look to be in\n |
| 0x23f037 | 14 | a good mood... |
| 0x23f046 | 9 | Left twin |
| 0x23f050 | 18 | Um, our apologies. |
| 0x23f063 | 10 | Right twin |
| 0x23f06e | 38 | The young master is often like this.\n |
| 0x23f095 | 31 | Please don't let it bother you. |
| 0x23f0b5 | 49 | There's probably something wrong if he's always\n |
| 0x23f0e7 | 12 | like this... |
| 0x23f0f4 | 29 | I keep my thoughts to myself. |
| 0x23f112 | 44 | Whatever. Not like I'll ever see them ever\n |
| 0x23f13f | 40 | again. I may as well humor them for now. |
| 0x23f168 | 25 | Welcome! Friend of yours? |
| 0x23f182 | 27 | Nah, we literally just met. |
| 0x23f19e | 30 | We requested to share a table. |
| 0x23f1bd | 46 | We just arrived in the imperial capital, and\n |
| 0x23f1ec | 43 | wished to talk with one of the locals here. |
| 0x23f218 | 48 | I get the feeling one of you isn't in the mood\n |
| 0x23f249 | 8 | to chat. |
| 0x23f252 | 26 | Hokay then--what'll it be? |
| 0x23f26d | 40 | We're not very familiar with the menu.\n |
| 0x23f296 | 35 | May we simply trust your judgement? |
| 0x23f2ba | 45 | If you don't mind, could you bring out your\n |
| 0x23f2e8 | 44 | recommendations? Oh, and money is no object. |
| 0x23f315 | 25 | Well, aren't THEY swanky. |
| 0x23f32f | 50 | However, a true connoisseur enjoys the challenge\n |
| 0x23f362 | 47 | of finding the best drink and food on limited\n |
| 0x23f392 | 7 | funds-- |
| 0x23f39a | 26 | Would you like to join us? |
| 0x23f3b5 | 46 | Of course, we will cover the entirety of the\n |
| 0x23f3e4 | 5 | bill. |
| 0x23f3ea | 45 | I pretend to take a slow drink as I hastily\n |
| 0x23f418 | 18 | review my options. |
| 0x23f42b | 45 | What to do... Free food is the best kind of\n |
| 0x23f459 | 45 | food, and if they're rich, I might get some\n |
| 0x23f487 | 18 | real delicacies... |
| 0x23f49a | 47 | But at the same time, I feel these guys might\n |
| 0x23f4ca | 23 | spell trouble for me... |
| 0x23f4e2 | 49 | As I think, one of the boys signals over to the\n |
| 0x23f514 | 8 | kitchen. |
| 0x23f51d | 47 | Soon after, the pub owner comes out with four\n |
| 0x23f54d | 13 | more bottles. |
| 0x23f55b | 28 | Er, I still have enough to-- |
| 0x23f578 | 32 | A small token of our friendship. |
| 0x23f599 | 28 | Please, no need to hesitate. |
| 0x23f5b6 | 45 | Looks like they know how to sway a drinker... |
| 0x23f5e4 | 43 | Guess there's no getting out of this one.\n |
| 0x23f610 | 36 | I decide to join their little feast. |
| 0x23f635 | 14 | A toast, then. |
| 0x23f644 | 27 | To our newfound friendship! |
| 0x23f660 | 45 | Delicious. It tastes almost like a juice of\n |
| 0x23f68e | 12 | some kind... |
| 0x23f69b | 48 | Yes. You can't find something like this in our\n |
| 0x23f6cc | 8 | country. |
| 0x23f6d5 | 24 | ...Hmph. Decent at best. |
| 0x23f6ee | 47 | The two boys seem impressed, but their master\n |
| 0x23f71e | 43 | seems to hold quite the opposite sentiment. |
| 0x23f74a | 44 | Young Master, I thought that this was your\n |
| 0x23f777 | 17 | current favorite. |
| 0x23f789 | 46 | I think it'd be best to be more honest about\n |
| 0x23f7b8 | 14 | your feelings. |
| 0x23f7c7 | 47 | Don't know what you're talking about. Nothing\n |
| 0x23f7f7 | 38 | can beat the drinks from our homeland. |
| 0x23f81e | 44 | True, but this one is not quite as strong,\n |
| 0x23f84b | 36 | and can be drunk much more smoothly. |
| 0x23f870 | 45 | Not to mention there is much less danger of\n |
| 0x23f89e | 43 | becoming inebriated to the point of being\n |
| 0x23f8ca | 5 | sick. |
| 0x23f8d0 | 47 | It's just something to indulge in. There's no\n |
| 0x23f900 | 44 | better or worse, just different preferences. |
| 0x23f92d | 39 | The man glares at me after I offer my\n |
| 0x23f955 | 12 | perspective. |
| 0x23f962 | 40 | Hmph. You've got quite the mouth on you. |
| 0x23f98b | 46 | Still, he stops complaining. Maybe he agrees\n |
| 0x23f9ba | 8 | with me. |
| 0x23f9c3 | 43 | Seems like he's got some passion for this\n |
| 0x23f9ef | 44 | "homeland" of his. I wonder where he's from? |
| 0x23fa1c | 49 | I wonder if I should ask about it, but it might\n |
| 0x23fa4e | 43 | be rude of me to pry at someone I just met. |
| 0x23fa7a | 44 | I'm sure they'd tell me if they wanted to... |
| 0x23faa7 | 16 | And here we are! |
| 0x23fab8 | 46 | Numerous fresh entrees and dishes are placed\n |
| 0x23fae7 | 17 | across the table. |
| 0x23faf9 | 43 | At the center is a large plate with amam,\n |
| 0x23fb25 | 44 | surrounded by multitudes of meat and other\n |
| 0x23fb52 | 16 | fillings for it. |
| 0x23fb63 | 25 | Well, this looks fancy... |
| 0x23fb7d | 45 | It makes you realize how much variety there\n |
| 0x23fbab | 39 | truly is when it's laid out before you. |
| 0x23fbd3 | 50 | So you use this to wrap up all the other things,\n |
| 0x23fc06 | 20 | and then eat that... |
| 0x23fc1b | 42 | The twins look down at the table in awe.\n |
| 0x23fc46 | 43 | It kind of reminds me of when I first saw\n |
| 0x23fc72 | 11 | this stuff. |
| 0x23fc7e | 46 | Guess everybody tends to react the same when\n |
| 0x23fcad | 42 | they encounter food from a foreign land... |
| 0x23fcd8 | 42 | If you'd like, we could wrap this for you. |
| 0x23fd03 | 45 | Please let us know if there's anything that\n |
| 0x23fd31 | 15 | you don't like. |
| 0x23fd41 | 47 | The two busily help with my food, in complete\n |
| 0x23fd71 | 46 | sync. It's like they've been doing work like\n |
| 0x23fda0 | 15 | this for years. |
| 0x23fdb0 | 45 | Reminds me of a certain other set of twins.\n |
| 0x23fdde | 44 | They're different, but similar, too. Kinda\n |
| 0x23fe0b | 14 | feels weird... |
| 0x23fe1a | 49 | Is this some kind of jerky? So you wrap it like\n |
| 0x23fe4c | 31 | this... and here. Please enjoy. |
| 0x23fe6c | 7 | Thanks. |
| 0x23fe74 | 41 | Here, young master. One for you, as well. |
| 0x23fe9e | 44 | The man silently takes it and begins to eat. |
| 0x23fecb | 42 | Since the young master here doesn't seem\n |
| 0x23fef6 | 45 | inclined to chat, I decide to ask the twins\n |
| 0x23ff24 | 8 | instead. |
| 0x23ff2d | 46 | What kind of stuff do you eat in your country? |
| 0x23ff5c | 43 | In our homeland, most of our meals center\n |
| 0x23ff88 | 16 | around mororo... |
| 0x23ff99 | 7 | Mororo? |
| 0x23ffa1 | 34 | Where have I heard that before...? |
| 0x23ffc4 | 45 | How to explain... It's a type of root tuber\n |
| 0x23fff2 | 46 | that swells up. It is a staple food where we\n |
| 0x240021 | 10 | come from. |
| 0x24002c | 44 | We steam it, roast it, grind it and mix it\n |
| 0x240059 | 20 | with other things... |
| 0x24006e | 25 | So kind of like a potato? |
| 0x240088 | 47 | It's quite interesting to see how other lands\n |
| 0x2400b8 | 37 | have very different customs for food. |
| 0x2400de | 47 | In this country, because these amam wraps are\n |
| 0x24010e | 43 | used, most dishes are roasted with little\n |
| 0x24013a | 11 | moisture... |
| 0x240146 | 46 | But in our case, because we eat with mororo,\n |
| 0x240175 | 42 | stewed and simmered dishes are much more\n |
| 0x2401a0 | 7 | common. |
| 0x2401a8 | 44 | The food here is very delicious, I must say. |
| 0x2401d5 | 42 | Right? And it goes well with these drinks. |
| 0x240200 | 44 | All the food in our homeland is far better\n |
| 0x24022d | 26 | than that of this country! |
| 0x240248 | 44 | The fact that he seems to have cleaned his\n |
| 0x240275 | 29 | plate isn't helping his case. |
| 0x240293 | 46 | Young master, why can't you be a little more\n |
| 0x2402c2 | 39 | honest and give praise where it is due? |
| 0x2402ea | 42 | You were wolfing down those wraps rather\n |
| 0x240315 | 9 | intently. |
| 0x24031f | 42 | Now then, here are some of the rarest of\n |
| 0x24034a | 13 | delicacies... |
| 0x240358 | 49 | The next dish brought out seems to be a roasted\n |
| 0x24038a | 24 | fish, cut directly open. |
| 0x2403a3 | 48 | As the plate touches down on the table, a very\n |
| 0x2403d4 | 43 | distinct smell begins wafting up from it... |
| 0x240400 | 45 | It's not something I serve often, but since\n |
| 0x24042e | 42 | you're travelers from far-off lands, you\n |
| 0x240459 | 21 | should give it a try. |
| 0x24046f | 48 | The young master wrinkles his nose at the smell. |
| 0x2404a0 | 41 | D-Does this store regularly serve their\n |
| 0x2404ca | 23 | customers rotten fish!? |
| 0x2404e2 | 36 | This here's a dish called kusayan.\n |
| 0x240507 | 45 | Smells a bit strange, I'll grant you, but I\n |
| 0x240535 | 25 | guarantee it tastes fine. |
| 0x24054f | 41 | He slowly lifts it up to his mouth, but\n |
| 0x240579 | 46 | grimaces at the intense scent of fermentation. |
| 0x2405a8 | 15 | ...You take it. |
| 0x2405b8 | 48 | He throws the piece onto my plate, like scraps\n |
| 0x2405e9 | 14 | for an animal. |
| 0x2405f8 | 20 | You mustn't be rude. |
| 0x24060d | 44 | The piece is quickly returned to the young\n |
| 0x24063a | 15 | master's plate. |
| 0x24064a | 7 | Urgh... |
| 0x240652 | 47 | He again brings the piece to his mouth, takes\n |
| 0x240682 | 20 | a sniff, and scowls. |
| 0x240697 | 45 | Yeah, that'd be the natural reaction. I was\n |
| 0x2406c5 | 35 | the same way when I first tried it. |
| 0x2406e9 | 43 | Pops, get me a warm one. In a large bottle. |
| 0x240715 | 19 | Gotcha. Right away. |
| 0x240729 | 10 | Warm sake? |
| 0x240734 | 34 | It's really nice with the kusayan. |
| 0x240757 | 29 | That does sound quite good... |
| 0x240775 | 50 | Would you mind if we join you? Pardon me, sir...\n |
| 0x2407a8 | 24 | could we get three cups? |
| 0x2407c1 | 11 | Sure thing. |
| 0x2407cd | 47 | Three of us enjoying the kusayan, and one guy\n |
| 0x2407fd | 26 | sulking and glaring at it. |
| 0x240818 | 47 | Soon, the warm sake is brought out and poured\n |
| 0x240848 | 28 | into each of our three cups. |
| 0x240865 | 46 | Would you please teach us the correct way to\n |
| 0x240894 | 9 | eat this? |
| 0x24089e | 18 | If you don't mind. |
| 0x2408b1 | 41 | Well, there really isn't much to teach... |
| 0x2408db | 50 | As they watch me, I cut apart the kusayan piece,\n |
| 0x24090e | 34 | and pop a small one into my mouth. |
| 0x240931 | 24 | *Munch, munch*... *gulp* |
| 0x24094a | 44 | And then you take a quick drink of the hot\n |
| 0x240977 | 7 | sake... |
| 0x24097f | 46 | The sake envelops the powerful flavor of the\n |
| 0x2409ae | 43 | kusayan, giving it all a rich and layered\n |
| 0x2409da | 6 | taste. |
| 0x2409e1 | 19 | ...Ah, that's good. |
| 0x2409f5 | 44 | After hearing my comment, the young master\n |
| 0x240a22 | 41 | stares at me as though I'm some kind of\n |
| 0x240a4c | 8 | monster. |
| 0x240a55 | 48 | ...My, you're right. The smell blends into the\n |
| 0x240a86 | 33 | sake and makes it very flavorful. |
| 0x240aa8 | 38 | Young master, you should try it too!\n |
| 0x240acf | 15 | It's very good. |
| 0x240adf | 9 | Nnnngh... |
| 0x240ae9 | 19 | Come, young master! |
| 0x240afd | 34 | Now is the time to prove yourself! |
| 0x240b20 | 47 | With the two of them cheering as he glares at\n |
| 0x240b50 | 25 | the kusayan, he finally-- |
| 0x240b6a | 25 | Urgh, I can't eat this... |
| 0x240b84 | 10 | Both twins |
| 0x240b8f | 13 | Young master! |
| 0x240b9d | 49 | This is starting to look more like some kind of\n |
| 0x240bcf | 37 | contest then relaxing with a drink... |
| 0x240bf5 | 45 | As we continue to drink, I get to know them\n |
| 0x240c23 | 14 | a little more. |
| 0x240c32 | 49 | Seems they're traveling incognito as merchants.\n |
| 0x240c64 | 46 | They can't openly sightsee, so they ask me a\n |
| 0x240c93 | 4 | lot. |
| 0x240c98 | 47 | The two boys are very polite, and give proper\n |
| 0x240cc8 | 43 | and measured responses to everything I say. |
| 0x240cf4 | 46 | They're so easy to talk to, I end up talking\n |
| 0x240d23 | 41 | for a long time about everything that's\n |
| 0x240d4d | 15 | happened to me. |
| 0x240d5d | 30 | ...So yeah. And here I am now. |
| 0x240d7c | 26 | That is quite the story... |
| 0x240d97 | 49 | To think that someone would find you as you lay\n |
| 0x240dc9 | 42 | unconscious. You were very lucky indeed... |
| 0x240df4 | 43 | Maybe it was fate more than luck. Anyway,\n |
| 0x240e20 | 42 | thanks to that, I can sit here and enjoy\n |
| 0x240e4b | 13 | a nice drink. |
| 0x240e59 | 45 | I see... So she is your savior and not your\n |
| 0x240e87 | 12 | lover, then. |
| 0x240e94 | 44 | ...I'm pretty sure I made that very clear,\n |
| 0x240ec1 | 5 | yeah. |
| 0x240ec7 | 45 | I see, I see. Well, I should've expected as\n |
| 0x240ef5 | 7 | much... |
| 0x240efd | 47 | He nods, looking to be in higher spirits, and\n |
| 0x240f2d | 38 | finishes off his cup in a single gulp. |
| 0x240f54 | 7 | Pfah... |
| 0x240f5c | 43 | His cheeks look flushed, and his eyes are\n |
| 0x240f88 | 21 | getting a bit droopy. |
| 0x240f9e | 43 | I don't think he drank THAT much, has he?\n |
| 0x240fca | 45 | The "young master" hasn't even refilled his\n |
| 0x240ff8 | 9 | cup once. |
| 0x241002 | 46 | I must say, though, the view of the imperial\n |
| 0x241031 | 40 | capital is impressive, to say the least. |
| 0x24105a | 47 | Indeed, it deserves its title of "the ancient\n |
| 0x24108a | 42 | city." I can feel the weight of its long\n |
| 0x2410b5 | 8 | history. |
| 0x2410be | 40 | And the women here are all so beautiful. |
| 0x2410e7 | 27 | Yes, I certainly envy them. |
| 0x241103 | 31 | Yeah, guess you can say that... |
| 0x241123 | 49 | Hm? Wait a minute. Not sure what that last part\n |
| 0x241155 | 23 | was supposed to mean... |
| 0x24116d | 7 | Hmph... |
| 0x241175 | 43 | The young master gives a proud grunt, and\n |
| 0x2411a1 | 7 | speaks. |
| 0x2411a9 | 34 | My daughter is far more beautiful. |
| 0x2411cc | 20 | You have a daughter? |
| 0x2411e1 | 45 | That catches me off-guard, and I can't keep\n |
| 0x24120f | 23 | myself from exclaiming. |
| 0x241227 | 30 | Do you wish to hear about her? |
| 0x241246 | 18 | Nah, that's fine-- |
| 0x241259 | 33 | Very well then! I shall tell you. |
| 0x24127b | 44 | My daughter is the most perfect daughter a\n |
| 0x2412a8 | 21 | father could ask for. |
| 0x2412be | 48 | For one, her grace is unmatched, her looks are\n |
| 0x2412ef | 47 | unparalleled, and her charm is without compare. |
| 0x24131f | 35 | ...I think that was three, not one. |
| 0x241343 | 47 | Second, she was born with a dignified aura of\n |
| 0x241373 | 44 | a mystic quality bordering on the ethereal-- |
| 0x2413a0 | 43 | The guy completely ignores my retort, and\n |
| 0x2413cc | 43 | continues on in a frenzy of paternal pride. |
| 0x2413f8 | 45 | ...Even flowers hide in shame, and the moon\n |
| 0x241426 | 46 | retreats to hide its face behind the clouds.\n |
| 0x241455 | 36 | My daughter DEFINES stunning beauty. |
| 0x24147a | 47 | And so the conversation becomes all about the\n |
| 0x2414aa | 45 | guy's daughter. Or more accurately, he just\n |
| 0x2414d8 | 19 | won't stop talking. |
| 0x2414ec | 48 | Her sweet and pure beauty leaves one in awe...\n |
| 0x24151d | 46 | She is graceful and delicate; sophisticated,\n |
| 0x24154c | 21 | yet full of warmth... |
| 0x241562 | 47 | She has a kind heart, and is very considerate\n |
| 0x241592 | 48 | of others, but has the courage to be bold when\n |
| 0x2415c3 | 11 | she must... |
| 0x2415cf | 46 | Having to listen to this stranger brag about\n |
| 0x2415fe | 47 | a daughter I've never met is nothing short of\n |
| 0x24162e | 8 | torture. |
| 0x241637 | 48 | He might... just MIGHT... be exaggerating a bit. |
| 0x241668 | 48 | ...He is only talking about one daughter, right? |
| 0x241699 | 4 | Yes. |
| 0x24169e | 19 | As far as I know... |
| 0x2416b2 | 47 | Hey, pipe down and listen up when I'm talking\n |
| 0x2416e2 | 18 | about my daughter! |
| 0x2416f5 | 18 | E-Er, well, look-- |
| 0x241708 | 46 | Even when she was young, it was clear as day\n |
| 0x241737 | 44 | that her charm was unrivaled. Her smallest\n |
| 0x241764 | 31 | smile melted everyone's hearts. |
| 0x241784 | 49 | There were times I thought "Surely! Yes, surely\n |
| 0x2417b6 | 42 | this must be the work of some bewitching\n |
| 0x2417e1 | 10 | spell...!" |
| 0x2417ec | 48 | I force a smile. I guess I'll just have to sit\n |
| 0x24181d | 14 | and take this. |
| 0x24182c | 40 | Shouldn't have let them buy me drinks.\n |
| 0x241855 | 45 | My instincts were right, but I wasn't quick\n |
| 0x241883 | 9 | enough... |
| 0x24188d | 45 | I listen to this doting father for about an\n |
| 0x2418bb | 45 | hour, and the flood of praise finally winds\n |
| 0x2418e9 | 5 | down. |
| 0x2418ef | 46 | ...And lastly, she cares for her father very\n |
| 0x24191e | 5 | much. |
| 0x241924 | 21 | ...Yes, young master. |
| 0x24193a | 48 | I think I catch a glimpse of the twins rolling\n |
| 0x24196b | 19 | their eyes at this. |
| 0x24197f | 47 | As the one-man show finally grinds to a halt,\n |
| 0x2419af | 40 | I give a sigh and turn back to my drink. |
| 0x2419d8 | 44 | Looks like this guy can't hold his liquor.\n |
| 0x241a05 | 31 | He looks pretty wasted already. |
| 0x241a25 | 48 | You know, this nation's drinks aren't bad, but\n |
| 0x241a56 | 43 | they feel weak. I'm hardly affected at all. |
| 0x241a82 | 41 | Sounds exactly like the type of thing a\n |
| 0x241aac | 44 | lightweight says to try to show off. Is he\n |
| 0x241ad9 | 12 | gonna be OK? |
| 0x241ae6 | 47 | If you want something stronger, why don't you\n |
| 0x241b16 | 19 | drink some of that? |
| 0x241b2a | 47 | I gesture unthinkingly towards the drinks the\n |
| 0x241b5a | 11 | twins have. |
| 0x241b66 | 5 | Er... |
| 0x241b6c | 21 | Ah, that might not... |
| 0x241b82 | 43 | What? I didn't know they had such drinks!\n |
| 0x241bae | 37 | Barkeep, bring me something stronger! |
| 0x241bd4 | 45 | The young master may not be able to back up\n |
| 0x241c02 | 45 | his talk. The two boys look at him, clearly\n |
| 0x241c30 | 10 | uncertain. |
| 0x241c3b | 46 | I suppose they're used to being able to stop\n |
| 0x241c6a | 44 | him from drinking more than he can handle... |
| 0x241c97 | 45 | Ah, well. It looks like just one small push\n |
| 0x241cc5 | 29 | would knock him out, anyways. |
| 0x241ce3 | 11 | Here ya go. |
| 0x241cef | 44 | Just as I expected, the owner brings out a\n |
| 0x241d1c | 43 | bottle of ushka, one of the harder spirits. |
| 0x241d48 | 47 | The man's cup is filled with an amber-colored\n |
| 0x241d78 | 7 | liquid. |
| 0x241d80 | 42 | Young Master, that liquor is quite strong. |
| 0x241dab | 43 | It would probably be best if you drank it\n |
| 0x241dd7 | 33 | slowly, and savored the flavor... |
| 0x241df9 | 30 | Hmph! Who do you think I am?\n |
| 0x241e18 | 46 | I am not a man to be laid low by mere alcohol. |
| 0x241e47 | 14 | *Gulp* *thunk* |
| 0x241e56 | 47 | And as if to punctuate his bold proclamation,\n |
| 0x241e86 | 34 | he downs the contents in one gulp. |
| 0x241ea9 | 45 | Ghaah! Hmph... you challenge me... But I am\n |
| 0x241ed7 | 44 | not CONQUERED... so easily? Not so easy...\n |
| 0x241f04 | 17 | Oh, not sho eejy! |
| 0x241f16 | 27 | Uh, was that "sho eejy"...? |
| 0x241f32 | 37 | Motor functions: declining quickly.\n |
| 0x241f58 | 43 | His eyes look unfocused, but I doubt he's\n |
| 0x241f84 | 22 | sleeping anytime soon. |
| 0x241f9b | 38 | Gimme another. Another! Phew... Gah!\n |
| 0x241fc2 | 23 | Come on now... 'nother! |
| 0x241fda | 39 | Young master, perhaps that is enough... |
| 0x242002 | 38 | That's why we told you not to do it... |
| 0x242029 | 30 | Oh... This does NOT look good. |
| 0x242048 | 32 | I'm gonna go use the restroom... |
| 0x242069 | 43 | I quickly get out of my seat to try for a\n |
| 0x242095 | 17 | swift exit, but-- |
| 0x2420a7 | 41 | Hollldit, pal. Where ya thinkyer goin'.\n |
| 0x2420d1 | 37 | I... haven't ffffinished talkin' yet! |
| 0x2420f7 | 27 | Urgh... can't get away now. |
| 0x242113 | 39 | Y'drink too! We don' need any of them\n |
| 0x24213b | 14 | ffformalities. |
| 0x24214a | 45 | You've already thrown formalities right out\n |
| 0x242178 | 11 | the window! |
| 0x242184 | 30 | S'alllll on me... Now drink!\n |
| 0x2421a3 | 13 | Drink it all! |
| 0x2421b1 | 37 | He splashes more alcohol into my cup. |
| 0x2421d7 | 32 | Ugh... This guy's a rowdy drunk. |
| 0x2421f8 | 38 | I look to his two attendants for help. |
| 0x24221f | 29 | ...We are deeply sorry, but-- |
| 0x24223d | 31 | ...You no longer have a choice. |
| 0x24225d | 44 | M'daughter, she's... she's grown up sho...\n |
| 0x24228a | 26 | beautiful, and sho kind... |
| 0x2422a5 | 39 | And so begins Act Two of the daughter\n |
| 0x2422cd | 11 | monologues. |
| 0x2422d9 | 40 | Her mother... not a shtrong body, see.\n |
| 0x242302 | 47 | Died jus' after birth... S'why I gave my girl\n |
| 0x242332 | 25 | a name means longevity... |
| 0x24234c | 43 | Dunno, but maybe thass why she was such a\n |
| 0x242378 | 42 | boist'rous lil' girl... S'pose she still\n |
| 0x2423a3 | 23 | needs t'work on that... |
| 0x2423bb | 45 | An' now she's been wanderin' off all on her\n |
| 0x2423e9 | 46 | own... I tell her to come home, but she don'\n |
| 0x242418 | 9 | listen... |
| 0x242422 | 41 | They shay a child, right, a child dun't\n |
| 0x24244c | 41 | undershtand how much their parents care\n |
| 0x242476 | 10 | aboutem... |
| 0x242481 | 38 | I jus' wanna be by her shide until--\n |
| 0x2424a8 | 47 | Nuh. I'm bein' shelfish... I wan' her to lead\n |
| 0x2424d8 | 23 | a long, healthy life... |
| 0x2424f0 | 45 | Bein' with her... is like seein' her mother\n |
| 0x24251e | 14 | happy again... |
| 0x24252d | 49 | ...Beautiful. Jus' like her mother... She looks\n |
| 0x24255f | 31 | ssso much... like her mother... |
| 0x24257f | 8 | *Sob*... |
| 0x242588 | 35 | Waaaaaaahaahaahaagh! *sob* Waaah,\n |
| 0x2425ac | 16 | aaahaaaaauugh... |
| 0x2425bd | 44 | The man's weathered face crinkles as tears\n |
| 0x2425ea | 32 | begin streaming down his cheeks. |
| 0x24260b | 36 | Great, he's a weepy drunk as well... |
| 0x242630 | 42 | Silence falls on the table, as though to\n |
| 0x24265b | 36 | envelop the man's anguished wailing. |
| 0x242680 | 48 | From what I can make out between his sobs, the\n |
| 0x2426b1 | 46 | mother's passed on. His pain and sorrow feel\n |
| 0x2426e0 | 8 | genuine. |
| 0x2426e9 | 45 | That's why I can't think of anything to say\n |
| 0x242717 | 7 | to him. |
| 0x24271f | 46 | This is a lot heavier than the usual drunken\n |
| 0x24274e | 11 | rambling... |
| 0x24275a | 48 | ...*Sob*... I'm... I'm not ashkin' for much...\n |
| 0x24278b | 44 | I don't wan' her to come back againsht her\n |
| 0x2427b8 | 7 | will... |
| 0x2427c0 | 48 | I jusht... I jusht want her to grow up healthy\n |
| 0x2427f1 | 44 | an' happy... Thassall... Thassall I really\n |
| 0x24281e | 7 | want... |
| 0x242826 | 9 | Kghwun... |
| 0x242830 | 8 | ...Kuon? |
| 0x242839 | 21 | Zzzzz... Zzzzzzzzz... |
| 0x24284f | 44 | Within moments, the man's head sags to the\n |
| 0x24287c | 37 | table, and he begins to snore loudly. |
| 0x2428a2 | 50 | Man... When this guy gets drunk, he goes through\n |
| 0x2428d5 | 31 | the whole spectrum of emotions. |
| 0x2428f5 | 47 | Young Master, you shouldn't be sleeping here... |
| 0x242925 | 49 | Let's head back to the inn. Owner, we thank you\n |
| 0x242957 | 13 | for the meal. |
| 0x242965 | 28 | Can I just... ask one thing? |
| 0x242982 | 16 | Yes. What is it? |
| 0x242993 | 17 | That last part... |
| 0x2429a5 | 4 | Yes? |
| 0x2429aa | 28 | ...You know what, nevermind. |
| 0x2429c7 | 33 | I just can't bring myself to ask. |
| 0x2429e9 | 44 | After the twins hurriedly handle the bill,\n |
| 0x242a16 | 44 | they politely stand before me to say their\n |
| 0x242a43 | 9 | goodbyes. |
| 0x242a4d | 36 | We thank you for joining us tonight. |
| 0x242a72 | 45 | We apologize for having caused such a fuss.\n |
| 0x242aa0 | 29 | I hope our paths cross again. |
| 0x242abe | 49 | They thank me, and drag away their drunk master\n |
| 0x242af0 | 45 | in a fashion that seems all too familiar to\n |
| 0x242b1e | 5 | them. |
| 0x242b24 | 24 | And so the storm passes. |
| 0x242b3d | 7 | Whew... |
| 0x242b45 | 49 | I give a small sigh as the silence of the night\n |
| 0x242b77 | 19 | returns to the pub. |
| 0x242b8b | 34 | ...Wonder what that was all about? |
| 0x242bae | 45 | I don't feel like heading home immediately,\n |
| 0x242bdc | 7 | though. |
| 0x242be4 | 47 | I right one of the tipped-over cups, and pour\n |
| 0x242c14 | 48 | myself a drink from one of the bottles not yet\n |
| 0x242c45 | 6 | empty. |
| 0x242c4c | 12 | ...I'm home. |
| 0x242c59 | 43 | I think I feel someone here, so I make my\n |
| 0x242c85 | 38 | presence known. Just as I thought...\n |
| 0x242cac | 15 | Kuon's waiting. |
| 0x242cbc | 27 | A job well done, I suppose. |
| 0x242cd8 | 12 | Still awake? |
| 0x242ce5 | 44 | I thought you might be hungry, so I made a\n |
| 0x242d12 | 31 | little snack. Do you want some? |
| 0x242d32 | 38 | I see a bowl of stew, still steaming\n |
| 0x242d59 | 11 | invitingly. |
| 0x242d65 | 42 | She must have just heated it up when she\n |
| 0x242d90 | 22 | noticed I'd come back. |
| 0x242da7 | 29 | Yeah, I think I'll have some. |
| 0x242dc5 | 49 | Thanks to that drunk, I ended up too distracted\n |
| 0x242df7 | 22 | to have a proper meal. |
| 0x242e0e | 5 | Here. |
| 0x242e14 | 9 | Thanks... |
| 0x242e1e | 34 | I pick up the bowl. It's warm...\n |
| 0x242e41 | 16 | comfortingly so. |
| 0x242e52 | 10 | *Slurp*... |
| 0x242e5d | 46 | A light fish broth, with plenty of vegetables. |
| 0x242e8c | 18 | How does it taste? |
| 0x242e9f | 12 | It's good... |
| 0x242eac | 44 | Kuon looks over at me, a gentle expression\n |
| 0x242ed9 | 12 | on her face. |
| 0x242ee6 | 45 | I suddenly find myself staring into her eyes. |
| 0x242f14 | 21 | Something the matter? |
| 0x242f2a | 20 | ...No. It's nothing. |
| 0x242f3f | 6 | ...OK? |
| 0x242f46 | 47 | I want to ask her something, but I stop myself. |
| 0x242f76 | 45 | And so we pass the time in the comfortable,\n |
| 0x242fa4 | 47 | companionable peace that I've grown so used to. |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_04.json` com a forma:
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
