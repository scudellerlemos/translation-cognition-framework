# Cena ch_22_08 — pacote de traducao (1579 linhas)

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
| Amaterasu | Termo | Amaterasu | manter_original | major |
| Anju | Personagem | Anju | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Chii | Personagem | Chii | manter_original | major |
| Earth | Local | Terra | traduzir | major |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mausoleum | Local | Mausoleu | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mito | Personagem | Mito | manter_original | none |
| Neko | Personagem | Neko | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Onvitaikayan | Termo | Onvitaikayan | manter_original | none |
| Onvitaikayan | Termo | Onvitaikayan | manter_original | major |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Saraana | Personagem | Saraana | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `onward.` -> `para frente.` (Haku, 17_01)
- `Master?` -> `Mestre?` (SYSTEM, 17_06)
- `you?` -> `pode?` (Haku, 13_01)
- `these two.` -> `estes dois.` (Haku, 17_01)
- `out.` -> `fora.` (Atuy, 17_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `This way.` -> `Por aqui.` (Mulher, 14_06)
- `cold.` -> `fria.` (Haku, 15_03)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `to him.` -> `para ele.` (Haku, 22_04)
- `Is something the matter?` -> `Aconteceu alguma coisa?` (Kuon, 12_09)
- `like this?` -> `assim?` (Haku, 16_01)
- `Please, this way.` -> `Por aqui, por favor.` (Oshtor, 19_07)
- `looking back.` -> `olhando para trás.` (Haku, 20_21)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Now...` -> `agora...` (Haku, 11_02)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `me.` -> `mim.` (Garota, 17_01)
- `Whoa--` -> `Uou--` (Man, 11_01)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `building.` -> `edifício.` (Oshtor, 18_01)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `security.` -> `segurança.` (Oshtor, 17_03)
- `world.` -> `mundo.` (Haku, 16_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `things.` -> `faz.` (Nekone, 15_03)
- `as well.` -> `também.` (Haku, 17_01)
- `Wha--` -> `Quê--` (Man, 11_01)
- `Tatari...` -> `Tatari...` (Garota, 21_05)
- `shape.` -> `Assim.` (Nekone, 14_09)
- `That's--` -> `Isso--` (Nosuri, 19_04)
- `Ngh...` -> `Ngh...` (Haku, 11_01)
- `you...` -> `você...` (Haku, 12_11)
- `age.` -> `idade.` (Garota, 19_07)
- `everything you know.` -> `tudo que você sabe.` (Ukon, 22_06)
- `That's...` -> `Isso...` (Haku, 15_01)
- `left.` -> `sobrado.` (Narrador/Haku, 14_09)
- `brother...` -> `irmão...` (Nekone, 15_01)
- `No...` -> `Não...` (Touka, 17_01)
- `myself.` -> `sozinho.` (Haku, 18_01)
- `them.` -> `deles.` (Kuon, 11_05)
- `again.` -> `vez.` (Ougi, 13_05)
- `Wh--` -> `Q--` (Haku, 11_07)
- `surface.` -> `superfície.` (Haku, 14_03)
- `ruins.` -> `ruínas.` (Haku, 21_01)
- `knowledge.` -> `conhecimento.` (Maroro, 12_12)
- `you.` -> `isso.` (Nekone, 15_03)
- `the imperial capital.` -> `a capital imperial.` (Haku, 17_01)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `...Haku.` -> `...Haku.` (Haku, 22_05)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `away.` -> `embora.` (Ukon, 18_01)
- `Alone...` -> `Sozinha...` (Haku, 18_01)
- `footsteps.` -> `passos.` (Haku, 16_01)
- `Hey--` -> `Ei--` (Haku, 12_04)
- `into the dark.` -> `para a escuridão.` (Nosuri, 16_01)
- `fingers.` -> `dedos.` (Kuon, 11_02)
- `Now then...` -> `Bom, então...` (Kuon, 11_02)
- `something...` -> `alguma coisa...` (Anju, 18_01)
- `...Mm?` -> `...Hm?` (Haku, 19_08)
- `of them.` -> `deles.` (Haku, 19_06)
- `...Mm...` -> `...Hm...` (Haku, 19_08)
- `behind me.` -> `atrás de mim.` (Haku, 14_02)
- `it hurts!` -> `dói!` (Haku, 16_01)
- `a bit.` -> `pouco.` (Haku, 13_01)
- `move.` -> `se mover.` (narração, 17_01)
- `hand...` -> `mão...` (Maroro, 18_01)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `A bit?` -> `Um...?` (Haku, 12_17)
- `then?` -> `então?` (Kuon, 16_02)
- `woman.` -> `mulher.` (Mulher, 17_01)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `to you.` -> `com você.` (Ukon, 13_02)
- `me?` -> `mim?` (Maroro, 12_13)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `eyes.` -> `olhar.` (Haku, 14_04)
- `love?` -> `amor?` (Atuy, 15_04)
- `complicated.` -> `complicado.` (Haku, 18_01)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Atuy.` -> `Atuy.` (Haku, 18_01)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `it...?` -> `isto...?` (Narrator/Haku, 20_17)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `*THUMP*` -> `*BUMB*` (Narrador, 12_11)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `Gah!` -> `Ai!` (Man, 11_01)
- `now?` -> `agora?` (Haku, 17_04)
- `Hmm...` -> `Hum...` (Haku, 14_10)
- `alone.` -> `...Tem razão.` (Haku, 22_03)
- `Dear brother...` -> `Querido irmão...` (Nekone, 14_04)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `We should hurry.` -> `Devemos nos apressar.` (Oshtor, 19_05)
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
| 0x25d6dc | 44 | I walk along as Uruuru and Saraana hold my\n |
| 0x25d709 | 42 | hands, guiding me through the foggy night. |
| 0x25d734 | 46 | It's been a while since Mito last invited me\n |
| 0x25d763 | 49 | over, but my heart's a little heavier as I walk\n |
| 0x25d795 | 7 | onward. |
| 0x25d79d | 45 | Well, he did give me the job to inspect the\n |
| 0x25d7cb | 44 | ruins. I'm sure he wants a detailed report\n |
| 0x25d7f8 | 6 | on it. |
| 0x25d7ff | 45 | For some reason, the old man didn't call me\n |
| 0x25d82d | 41 | immediately after I returned to the city. |
| 0x25d857 | 45 | To be honest, I don't want to remember what\n |
| 0x25d885 | 48 | happened there. It was convenient for me, but... |
| 0x25d8b6 | 44 | Just when I had almost forgotten the whole\n |
| 0x25d8e3 | 26 | thing, he calls me over... |
| 0x25d8fe | 47 | And I'm guessing he wants to talk to me about\n |
| 0x25d92e | 14 | what happened. |
| 0x25d93d | 45 | About how the Tatari are what's left of the\n |
| 0x25d96b | 13 | human race... |
| 0x25d979 | 46 | I wonder if I'm allowed to tell him the truth. |
| 0x25d9a8 | 41 | But knowing that old man, I wouldn't be\n |
| 0x25d9d2 | 30 | surprised if he already knows. |
| 0x25d9f1 | 36 | The problem is whether he knows...\n |
| 0x25da16 | 12 | that I know. |
| 0x25da23 | 50 | Kuon's right. This could be dangerous knowledge.\n |
| 0x25da56 | 21 | If things go badly... |
| 0x25da6c | 7 | Master? |
| 0x25da74 | 46 | You do not look well. Does something trouble\n |
| 0x25daa3 | 4 | you? |
| 0x25daa8 | 47 | And keeping silent... probably isn't an option. |
| 0x25dad8 | 46 | I mean, he gave me all that advance pay, and\n |
| 0x25db07 | 44 | he's probably already got some report from\n |
| 0x25db34 | 10 | these two. |
| 0x25db3f | 46 | I might lose his trust if I try to hide this\n |
| 0x25db6e | 21 | information from him. |
| 0x25db84 | 23 | Oh, uh... It's nothing. |
| 0x25db9c | 46 | ...Overanalyzing it like this isn't going to\n |
| 0x25dbcb | 45 | help.  All I can do is just let things play\n |
| 0x25dbf9 | 4 | out. |
| 0x25dc02 | 44 | The two lean in a little closer, as though\n |
| 0x25dc2f | 21 | trying to comfort me. |
| 0x25dc45 | 34 | Do I really look that uneasy...?\n |
| 0x25dc68 | 3 | Hm? |
| 0x25dc6c | 47 | As we walk the misty road, I suddenly realize\n |
| 0x25dc9c | 38 | we've arrived in that strange hallway. |
| 0x25dcc3 | 43 | It's different from the verdant garden we\n |
| 0x25dcef | 42 | usually reach. This is a path, regal and\n |
| 0x25dd1a | 13 | ornamented... |
| 0x25dd28 | 48 | It's a huge hallway. So big, one could mistake\n |
| 0x25dd59 | 14 | it for a road. |
| 0x25dd68 | 40 | And at the very end, I see a grand and\n |
| 0x25dd91 | 15 | beautiful door. |
| 0x25dda1 | 10 | This is... |
| 0x25ddac | 9 | This way. |
| 0x25ddb6 | 44 | The two continue to lead me forward, and I\n |
| 0x25dde3 | 7 | follow. |
| 0x25ddeb | 46 | I recognize this place... No, there's no way\n |
| 0x25de1a | 15 | I would forget. |
| 0x25de2a | 15 | This place is-- |
| 0x25de3a | 22 | The door slowly opens. |
| 0x25de51 | 32 | And beyond it lies a giant hall. |
| 0x25de72 | 49 | The place where the most powerful man in Yamato\n |
| 0x25dea4 | 24 | sits... The throne room. |
| 0x25debd | 49 | Far in the distance, I see Honoka standing next\n |
| 0x25deef | 41 | to the throne, a quiet smile on her face. |
| 0x25df19 | 44 | And beside her sits the man who the people\n |
| 0x25df46 | 35 | call the god incarnate. The Mikado. |
| 0x25df6a | 44 | He has an air of kingly dignity about him,\n |
| 0x25df97 | 44 | just like I remember from my last audience\n |
| 0x25dfc4 | 9 | with him. |
| 0x25dfce | 46 | I suppose the only thing that's different is\n |
| 0x25dffd | 41 | that this time, we're the only ones here. |
| 0x25e027 | 40 | So you have come... I have been waiting. |
| 0x25e050 | 28 | We thank you for joining us. |
| 0x25e06d | 43 | Gramps, what's the meaning behind all this? |
| 0x25e099 | 48 | Or in this case... Do I have to address you as\n |
| 0x25e0ca | 11 | the Mikado? |
| 0x25e0d6 | 44 | ...That's right. The old geezer who called\n |
| 0x25e103 | 36 | himself Mito is actually the Mikado. |
| 0x25e128 | 41 | The Mikado's eyes narrow to slits as he\n |
| 0x25e152 | 49 | observes me. Still, it's like he's looking past\n |
| 0x25e184 | 14 | me, not at me. |
| 0x25e193 | 48 | Either will suffice. You may address me as you\n |
| 0x25e1c4 | 8 | see fit. |
| 0x25e1cd | 47 | His voice is different from the amicable tone\n |
| 0x25e1fd | 48 | he usually greets me with. He sounds stern and\n |
| 0x25e22e | 5 | cold. |
| 0x25e234 | 45 | You are correct... I am the Mikado of Yamato. |
| 0x25e262 | 31 | ...Does this face surprise you? |
| 0x25e282 | 40 | Nah, I kind of figured it out already.\n |
| 0x25e2ab | 14 | Saw it coming. |
| 0x25e2ba | 9 | ...I see. |
| 0x25e2c4 | 46 | True, I already guessed that the old man was\n |
| 0x25e2f3 | 11 | the Mikado. |
| 0x25e2ff | 43 | So it's not surprising, but when he comes\n |
| 0x25e32b | 20 | right out with it... |
| 0x25e340 | 49 | My gaze flickers toward Honoka, who stands next\n |
| 0x25e372 | 7 | to him. |
| 0x25e37a | 33 | Honoka looks the same as usual.\n |
| 0x25e39c | 30 | Kind of a relief to see her... |
| 0x25e3bb | 24 | Is something the matter? |
| 0x25e3d4 | 9 | Uh... no. |
| 0x25e3de | 42 | What use is there in changing now, Haku?\n |
| 0x25e409 | 44 | You may act as you wish. There are none to\n |
| 0x25e436 | 14 | reprimand you. |
| 0x25e445 | 40 | ...Then I'll go with Mito, like usual.\n |
| 0x25e46e | 42 | Formalities seem kind of useless by now,\n |
| 0x25e499 | 19 | and they're tiring. |
| 0x25e4ad | 39 | Yes, good. I expected as much from you. |
| 0x25e4d5 | 24 | So, what's the occasion? |
| 0x25e4ee | 30 | Hrm. What do you mean by that? |
| 0x25e50d | 49 | Why reveal your secret identity all of a sudden\n |
| 0x25e53f | 10 | like this? |
| 0x25e54a | 36 | Ah... That is what you wish to know. |
| 0x25e56f | 44 | You're... making it sound like I should be\n |
| 0x25e59c | 27 | asking about anything else. |
| 0x25e5b8 | 48 | The old man's expression softens for a moment,\n |
| 0x25e5e9 | 41 | as though looking at something long gone. |
| 0x25e613 | 46 | There is but one reason I speak to you here.\n |
| 0x25e642 | 47 | I would hear your account not as Mito, but as\n |
| 0x25e672 | 46 | Now then, would you tell me what happened in\n |
| 0x25e6a1 | 12 | those ruins? |
| 0x25e6ae | 16 | Here it comes... |
| 0x25e6bf | 49 | This was a job the old man gave me in the first\n |
| 0x25e6f1 | 40 | place. I need to report something. But-- |
| 0x25e71a | 42 | Should I really be telling him the whole\n |
| 0x25e745 | 9 | truth...? |
| 0x25e74f | 47 | ...Haven't you already heard the details from\n |
| 0x25e77f | 19 | Uruuru and Saraana? |
| 0x25e793 | 47 | No. It seems there was some sort of incident,\n |
| 0x25e7c3 | 31 | so I avoided prying too deeply. |
| 0x25e7e3 | 43 | Ah... It seems you are wary of something,\n |
| 0x25e80f | 30 | but you need not be concerned. |
| 0x25e82e | 48 | Whatever is in your report, I shall swear here\n |
| 0x25e85f | 43 | that no harm will befall you because of it. |
| 0x25e88e | 47 | I instinctively glance up, looking at the old\n |
| 0x25e8be | 11 | man's face. |
| 0x25e8ca | 14 | Wait, do you-- |
| 0x25e8d9 | 30 | ...So you saw it, did you not? |
| 0x25e8f8 | 45 | The old man's attitude hasn't changed at all. |
| 0x25e926 | 45 | But something's different. Something that I\n |
| 0x25e954 | 26 | never saw in him before... |
| 0x25e96f | 15 | Who... are you? |
| 0x25e97f | 43 | This guy knew what I'd find in those ruins. |
| 0x25e9ab | 48 | More importantly, it sounds like he knows what\n |
| 0x25e9dc | 19 | those things are... |
| 0x25e9f0 | 43 | He was just an old man that went on about\n |
| 0x25ea1c | 44 | nonsense like being named Mito and being a\n |
| 0x25ea49 | 16 | crepe salesman-- |
| 0x25ea5a | 47 | But in reality, he's the most powerful man in\n |
| 0x25ea8a | 42 | Yamato. Its ruler, the Mikado... or so I\n |
| 0x25eab5 | 8 | thought. |
| 0x25eabe | 40 | But is that really the end of the story? |
| 0x25eae7 | 47 | What the hell is the Mikado? "God incarnate",\n |
| 0x25eb17 | 40 | keeper of machines, Yamato's ruler for\n |
| 0x25eb40 | 12 | centuries... |
| 0x25eb4d | 47 | I didn't believe a word of it. It all sounded\n |
| 0x25eb7d | 46 | like crazy rumors, but if any of it is true... |
| 0x25ebac | 46 | Where did he get all that tech? How could he\n |
| 0x25ebdb | 43 | survive for hundreds of years...? There's\n |
| 0x25ec07 | 12 | just no way. |
| 0x25ec14 | 48 | Just saying it's because he's the Mikado isn't\n |
| 0x25ec45 | 22 | enough to convince me. |
| 0x25ec5c | 13 | ...Follow me. |
| 0x25ec6a | 47 | After he says that, Honoka begins to push his\n |
| 0x25ec9a | 16 | wheelchair away. |
| 0x25ecab | 17 | Please, this way. |
| 0x25ecbd | 5 | Wai-- |
| 0x25ecc3 | 45 | My resolve wavers. I try to call out to the\n |
| 0x25ecf1 | 47 | two... but they've gone beyond the drapes, no\n |
| 0x25ed21 | 13 | looking back. |
| 0x25ed2f | 7 | Nngh... |
| 0x25ed37 | 43 | Guess I have no choice but to follow them\n |
| 0x25ed63 | 6 | now... |
| 0x25ed6a | 47 | I follow the two of them behind the drapes to\n |
| 0x25ed9a | 41 | find a dark area spreading out before me. |
| 0x25edc4 | 22 | ...A downward incline? |
| 0x25eddb | 49 | I almost trip on the slope and stop uncertainly\n |
| 0x25ee0d | 45 | in the darkness. But the twins take my hands. |
| 0x25ee3b | 7 | Master. |
| 0x25ee43 | 45 | ...After that, I don't know how long I walk\n |
| 0x25ee71 | 31 | forward, letting them guide me. |
| 0x25ee91 | 47 | Eventually, another giant door appears before\n |
| 0x25eec1 | 3 | me. |
| 0x25eec5 | 46 | It looks like a heavy door, but not like the\n |
| 0x25eef4 | 47 | entrance to the throne room. This one is made\n |
| 0x25ef24 | 9 | of metal. |
| 0x25ef2e | 6 | Whoa-- |
| 0x25ef35 | 44 | The door opens, and light floods out along\n |
| 0x25ef62 | 44 | with a light wind--a gentle breeze, with a\n |
| 0x25ef8f | 12 | fresh scent. |
| 0x25ef9c | 7 | Wha--!? |
| 0x25efa4 | 48 | I squint slightly, and once I can see past the\n |
| 0x25efd5 | 47 | brightness, I see a huge forest spreading out\n |
| 0x25f005 | 9 | below me. |
| 0x25f00f | 46 | The trees go on for as far as the eye can see. |
| 0x25f03e | 46 | I look up to find a clear blue sky... Clear,\n |
| 0x25f06d | 45 | vast and wide, like I could fall into it at\n |
| 0x25f09b | 11 | any moment. |
| 0x25f0a7 | 43 | Where the hell is this? Why can I see the\n |
| 0x25f0d3 | 7 | sky...? |
| 0x25f0db | 44 | It isn't a steep slope, but I'm definitely\n |
| 0x25f108 | 13 | heading down. |
| 0x25f116 | 45 | The imperial capital is merely the surface.\n |
| 0x25f144 | 44 | These underground areas are the true Yamato. |
| 0x25f171 | 47 | Yet... it is also a place where the forgotten\n |
| 0x25f1a1 | 41 | past has been sealed. A past long since\n |
| 0x25f1cb | 10 | discarded. |
| 0x25f1d6 | 12 | The past...? |
| 0x25f1e3 | 47 | Honoka places the wheelchair on a transparent\n |
| 0x25f213 | 43 | glowing flight of stairs, leading downward. |
| 0x25f23f | 42 | As she steps atop them, the stairs begin\n |
| 0x25f26a | 42 | smoothly and soundlessly gliding downward. |
| 0x25f295 | 44 | I follow her, and the stairs carry me down\n |
| 0x25f2c2 | 24 | without a sound as well. |
| 0x25f2db | 44 | A calm breeze flows past me, flower petals\n |
| 0x25f308 | 20 | dancing on the wind. |
| 0x25f31d | 41 | Far beyond, I can see a lake's surface,\n |
| 0x25f347 | 41 | glittering with light. A flock of birds\n |
| 0x25f371 | 15 | clusters above. |
| 0x25f381 | 31 | I'm looking down on a paradise. |
| 0x25f3a1 | 50 | Who would've thought there could be a huge place\n |
| 0x25f3d4 | 42 | like this beneath the imperial capital...? |
| 0x25f3ff | 50 | The blue sky and horizon are likely simulations,\n |
| 0x25f432 | 47 | but still... judging by the trees, this place\n |
| 0x25f462 | 8 | is deep. |
| 0x25f46b | 50 | I'd say its size is just right for the Mausoleum\n |
| 0x25f49e | 27 | on the surface to fit here. |
| 0x25f4ba | 49 | I look around, wide-eyed, and see a clearing at\n |
| 0x25f4ec | 42 | the base of the staircase... and a giant\n |
| 0x25f517 | 9 | building. |
| 0x25f521 | 13 | This place... |
| 0x25f52f | 45 | I get it now. This is... the garden where I\n |
| 0x25f55d | 17 | talk with Mito... |
| 0x25f56f | 49 | Did the old man want to show me this? Why would\n |
| 0x25f5a1 | 29 | he do something like that...? |
| 0x25f5bf | 5 | Here. |
| 0x25f5c5 | 46 | Beyond here... there is something we wish to\n |
| 0x25f5f4 | 9 | show you. |
| 0x25f5fe | 29 | You want me to see something? |
| 0x25f61c | 48 | They lead me to small, somewhat shabby-looking\n |
| 0x25f64d | 47 | doors that seem to lead into a simple building. |
| 0x25f67d | 8 | ...Open. |
| 0x25f686 | 41 | After the old man speaks, a small crack\n |
| 0x25f6b0 | 44 | appears, and the doors begin to slowly open. |
| 0x25f6dd | 47 | The door's easily the smallest of the ones so\n |
| 0x25f70d | 48 | far, but it seems the densest and has the most\n |
| 0x25f73e | 9 | security. |
| 0x25f748 | 44 | Almost like it was meant to seal something\n |
| 0x25f775 | 7 | away... |
| 0x25f77d | 45 | We enter through the doorway and continue on. |
| 0x25f7ab | 41 | After taking a few steps inside, lights\n |
| 0x25f7d5 | 47 | illuminate the hallway all the way to the back. |
| 0x25f805 | 16 | This place is... |
| 0x25f816 | 47 | The view is unlike anything I've seen in this\n |
| 0x25f846 | 6 | world. |
| 0x25f84d | 43 | Everything is made up of a cold, lifeless\n |
| 0x25f879 | 47 | material, neither stone nor wood. Glass panes\n |
| 0x25f8a9 | 11 | in windows. |
| 0x25f8b5 | 48 | Remnants of a memory, just like the ruins I saw. |
| 0x25f8e6 | 44 | But this one isn't just a remnant. There's\n |
| 0x25f913 | 48 | something alive in it... like the entire place\n |
| 0x25f944 | 13 | is breathing. |
| 0x25f952 | 38 | A nostalgic and comfortable feeling.\n |
| 0x25f979 | 32 | Something left behind by time... |
| 0x25f99a | 24 | So... there still was... |
| 0x25f9b3 | 46 | I can feel the pieces of the puzzle starting\n |
| 0x25f9e2 | 20 | to click into place. |
| 0x25f9f7 | 44 | Honoka stops pushing the wheelchair forward. |
| 0x25fa24 | 42 | It seems we've hit the end of the hallway. |
| 0x25fa4f | 33 | This may cause some discomfort.\n |
| 0x25fa71 | 22 | Please brace yourself. |
| 0x25fa88 | 4 | Huh? |
| 0x25fa8d | 46 | The next moment, a sensation runs through my\n |
| 0x25fabc | 31 | body, like I'm floating upward. |
| 0x25fadc | 47 | I can see the walls around us rising up at an\n |
| 0x25fb0c | 17 | alarming speed... |
| 0x25fb1e | 50 | For a moment, I think that's what's happening...\n |
| 0x25fb51 | 22 | but it's the opposite. |
| 0x25fb68 | 37 | W-We're falling... We're going down!? |
| 0x25fb8e | 46 | The floor beneath us is moving downward at a\n |
| 0x25fbbd | 17 | tremendous speed. |
| 0x25fbcf | 47 | Eventually the walls around us disappear, and\n |
| 0x25fbff | 45 | we move slower and slower... and grind to a\n |
| 0x25fc2d | 5 | halt. |
| 0x25fc33 | 49 | Now, this is where I... There is something here\n |
| 0x25fc65 | 27 | that I wish for you to see. |
| 0x25fc81 | 45 | A beacon that may guide you to the past you\n |
| 0x25fcaf | 10 | have lost. |
| 0x25fcba | 24 | The past... that I lost? |
| 0x25fcd3 | 31 | ...What do you... mean by that? |
| 0x25fcf3 | 27 | Lord Haku, are you certain? |
| 0x25fd0f | 41 | You still have the option to turn back,\n |
| 0x25fd39 | 19 | should you wish it. |
| 0x25fd4d | 9 | Honoka... |
| 0x25fd57 | 45 | My apologies, but I believe he deserves the\n |
| 0x25fd85 | 16 | right to choose. |
| 0x25fd96 | 31 | ...Very well. Do as you please. |
| 0x25fdb6 | 44 | Honoka gives a deep bow to the old man and\n |
| 0x25fde3 | 17 | turns towards me. |
| 0x25fdf5 | 26 | What did you mean by that? |
| 0x25fe10 | 46 | Now is your last chance to turn back. If you\n |
| 0x25fe3f | 35 | wish to do so, I will not stop you. |
| 0x25fe63 | 47 | You may leave this place, and pretend nothing\n |
| 0x25fe93 | 44 | ever happened. You may forget all you have\n |
| 0x25fec0 | 11 | seen today. |
| 0x25fecc | 47 | If you choose to do so, you may remain living\n |
| 0x25fefc | 45 | the same peaceful life you have always known. |
| 0x25ff2a | 49 | But... if you do choose to proceed forward from\n |
| 0x25ff5c | 36 | here, there will be no turning back. |
| 0x25ff81 | 12 | Lord Haku... |
| 0x25ff8e | 46 | You have regained your memories, have you not? |
| 0x25ffbd | 46 | However, you do not understand the situation\n |
| 0x25ffec | 13 | you are in... |
| 0x25fffa | 45 | What has happened to you, why the world has\n |
| 0x260028 | 48 | changed so much... You do not understand these\n |
| 0x260059 | 7 | things. |
| 0x260061 | 13 | Am I correct? |
| 0x26006f | 21 | Honoka, who exactly-- |
| 0x260085 | 48 | If you choose to proceed, then these questions\n |
| 0x2600b6 | 17 | will be answered. |
| 0x2600c8 | 44 | However, everything around you will change\n |
| 0x2600f5 | 8 | as well. |
| 0x2600fe | 44 | The world you live in... and you yourself... |
| 0x26012b | 32 | Do you still... wish to proceed? |
| 0x26014c | 43 | Honoka cautions me... as though somewhere\n |
| 0x260178 | 27 | between warning and threat. |
| 0x260194 | 47 | Meaningful words, as though she already knows\n |
| 0x2601c4 | 13 | all about me. |
| 0x2601d2 | 49 | Coming here has made it clear. The Mikado never\n |
| 0x260204 | 44 | invited "some random nobody" over by chance. |
| 0x260231 | 23 | He knows something...\n |
| 0x260249 | 24 | No. He knows everything. |
| 0x260262 | 21 | About my lost past... |
| 0x260278 | 45 | When I first came to, I found myself in the\n |
| 0x2602a6 | 40 | middle of the mountains, with no memory. |
| 0x2602cf | 48 | Kuon saved me, and I continued to live on with\n |
| 0x260300 | 46 | this nagging feeling, unable to remember any\n |
| 0x26032f | 11 | of my past. |
| 0x26033b | 33 | But now that I remember it all... |
| 0x26035d | 13 | The cities... |
| 0x26036b | 11 | My house... |
| 0x260377 | 12 | My family... |
| 0x260384 | 18 | Everything's gone. |
| 0x260397 | 37 | What the hell do those ruins mean...? |
| 0x2603bd | 44 | Why isn't anyone around me a human being...? |
| 0x2603ea | 43 | What... What happened to the human race...? |
| 0x260416 | 33 | No, I already know that answer.\n |
| 0x260438 | 29 | The human race... is extinct. |
| 0x260456 | 42 | But what the hell was that thing, then...? |
| 0x260481 | 19 | That slimy thing... |
| 0x260495 | 17 | Was that really-- |
| 0x2604a7 | 9 | Master... |
| 0x2604b1 | 46 | I was trying to not think about it, but now... |
| 0x2604e0 | 22 | Tell me... everything. |
| 0x2604f7 | 26 | But now... I have to know. |
| 0x260512 | 48 | ...Very well. Then there is nothing more I can\n |
| 0x260543 | 4 | say. |
| 0x260548 | 50 | Honoka bows softly and steps behind the old man,\n |
| 0x26057b | 35 | her mouth pressed into a thin line. |
| 0x26059f | 20 | You are ready, then? |
| 0x2605b4 | 28 | The old man raises his hand. |
| 0x2605d1 | 48 | Suddenly the floor goes transparent, as though\n |
| 0x260602 | 48 | made of glass. The light above illuminates the\n |
| 0x260633 | 14 | dark depths... |
| 0x260642 | 38 | What I see is... a disturbing sight.\n |
| 0x260669 | 41 | A substance like vivid red rotting flesh. |
| 0x260693 | 40 | From time to time, it pulsates, like a\n |
| 0x2606bc | 10 | heartbeat. |
| 0x2606c7 | 5 | Wha-- |
| 0x2606cd | 16 | No mistaking it. |
| 0x2606de | 9 | Tatari... |
| 0x2606e8 | 37 | Yes. That is what the people call it. |
| 0x26070e | 46 | Ironic indeed. The very ones they worship as\n |
| 0x26073d | 47 | gods are what they fear and loathe, oblivious\n |
| 0x26076d | 13 | to the truth. |
| 0x26077b | 15 | Onvitaikayan... |
| 0x26078b | 46 | The race that once ruled this world, long ago. |
| 0x2607ba | 20 | What... do you mean? |
| 0x2607cf | 46 | You have already figured it out, have you not? |
| 0x2607fe | 45 | The old man swipes his finger across the air. |
| 0x26082c | 43 | The walls around the thing below begin to\n |
| 0x260858 | 29 | blink, making strange sounds. |
| 0x260876 | 48 | Immediately, the surface of the Tatari ripples\n |
| 0x2608a7 | 18 | with tiny bubbles. |
| 0x2608ba | 50 | As though a reaction to this, the amorphous blob\n |
| 0x2608ed | 44 | slowly begins to form into a very familiar\n |
| 0x26091a | 6 | shape. |
| 0x260921 | 42 | Four long spindly limbs, and a small head. |
| 0x26094c | 45 | The two black holes that line its head look\n |
| 0x26097a | 20 | straight back at us. |
| 0x26098f | 41 | Grotesque, malformed, but unmistakable.\n |
| 0x2609b9 | 8 | That's-- |
| 0x2609c8 | 49 | In the next instant, the shape all but explodes\n |
| 0x2609fa | 45 | apart, returning to its amorphous, lurching\n |
| 0x260a28 | 5 | form. |
| 0x260a2e | 6 | Ngh... |
| 0x260a35 | 46 | Nausea washes over me. I put my hand over my\n |
| 0x260a64 | 27 | mouth and take a step back. |
| 0x260a80 | 29 | So then... they really are... |
| 0x260a9e | 44 | I already knew... what had happened to the\n |
| 0x260acb | 47 | But there was a part of me that was trying to\n |
| 0x260afb | 33 | deny it. Refusing to accept it... |
| 0x260b1d | 27 | So the Tatari really are... |
| 0x260b39 | 9 | Humans... |
| 0x260b43 | 48 | That is correct. Before you is what remains of\n |
| 0x260b74 | 15 | the human race. |
| 0x260b84 | 31 | So you finally accept it, then? |
| 0x260ba4 | 10 | Old man... |
| 0x260baf | 28 | You never change, do you...? |
| 0x260bcc | 44 | You have a keen mind, but when you find an\n |
| 0x260bf9 | 44 | inconvenient truth, you desperately try to\n |
| 0x260c26 | 10 | ignore it. |
| 0x260c31 | 42 | I can't blame you, of course, but it's a\n |
| 0x260c5c | 22 | bad habit nonetheless. |
| 0x260c73 | 18 | You... can't be... |
| 0x260c86 | 47 | Hah... It really has been a while since we've\n |
| 0x260cb6 | 40 | talked like this, hasn't it, Hiroshi...? |
| 0x260cdf | 18 | ...Bro... ther...? |
| 0x260cf2 | 41 | That's impossible... Is it... really you? |
| 0x260d1c | 44 | He's aged a lot, but this face, the way he\n |
| 0x260d49 | 34 | carries himself... He has to be... |
| 0x260d6c | 29 | Then that means... Honoka...? |
| 0x260d8a | 36 | You really haven't changed at all... |
| 0x260daf | 32 | Just the way I remembered you.\n |
| 0x260dd0 | 22 | Just like back then... |
| 0x260de7 | 47 | Heh... Hohoho... I've been waiting... so long\n |
| 0x260e17 | 11 | for this... |
| 0x260e23 | 47 | A long, long time... So long that I have lost\n |
| 0x260e53 | 46 | count of the years. But I have finally found\n |
| 0x260e82 | 6 | you... |
| 0x260e89 | 26 | So it... really is you...? |
| 0x260ea4 | 22 | ...Hold on. "Hiroshi"? |
| 0x260ebb | 29 | ...Hm? Or... was it Hiroyuki? |
| 0x260ed9 | 31 | What do you mean "or was it"?\n |
| 0x260ef9 | 25 | Who the hell is Hiroyuki? |
| 0x260f13 | 38 | No, perhaps it was Kazuki...? I think. |
| 0x260f3a | 15 | You're kidding. |
| 0x260f4a | 14 | ...Gonsuke...? |
| 0x260f59 | 41 | ...How... do you forget your own little\n |
| 0x260f83 | 18 | brother's name...? |
| 0x260f96 | 49 | ...I promise I haven't forgotten because of how\n |
| 0x260fc8 | 46 | long it's been. I would never lose it to old\n |
| 0x260ff7 | 4 | age. |
| 0x260ffc | 47 | You really forgot--OK, this kind of ruins the\n |
| 0x26102c | 39 | whole touching reunion thing, you know? |
| 0x261054 | 32 | No no no! I haven't forgotten.\n |
| 0x261075 | 42 | I just... can't think of it at the moment. |
| 0x2610a0 | 34 | There's a word for that. "Forgot." |
| 0x2610c3 | 48 | I guess I'd forgotten too, but I'd lost ALL my\n |
| 0x2610f4 | 38 | memories by then. Not my fault, right? |
| 0x26111b | 45 | I suppose I will continue to call you Haku.\n |
| 0x261149 | 45 | It is your new name, and a comfortable one,\n |
| 0x261177 | 9 | I'm sure. |
| 0x261181 | 44 | ...Guess you're right. If you called me by\n |
| 0x2611ae | 41 | another name, it would just feel strange. |
| 0x2611d8 | 43 | More importantly, how in the hell did you\n |
| 0x261204 | 28 | become the Mikado of Yamato? |
| 0x261221 | 44 | And what is that... thing!? How did humans\n |
| 0x26124e | 18 | end up like that!? |
| 0x261261 | 47 | I can understand how you must feel, but I can\n |
| 0x261291 | 35 | only answer one question at a time. |
| 0x2612b5 | 45 | Now, where to begin... Well, I suppose I'll\n |
| 0x2612e3 | 26 | explain it from the start. |
| 0x2612fe | 47 | Of course... I lack details on precisely what\n |
| 0x26132e | 30 | happened, all those years ago. |
| 0x26134d | 48 | I wasn't directly involved, and because of the\n |
| 0x26137e | 46 | chaos, I could not gather all the information. |
| 0x2613ad | 44 | Doesn't matter. I just want you to tell me\n |
| 0x2613da | 20 | everything you know. |
| 0x2613ef | 47 | Very well. I will start with what happened to\n |
| 0x26141f | 10 | you, then. |
| 0x26142a | 44 | You became a test subject for my research.\n |
| 0x261457 | 46 | You remember I put you in cold sleep for the\n |
| 0x261486 | 12 | final phase? |
| 0x261493 | 20 | ...Is that... right? |
| 0x2614a8 | 45 | To be honest, my memory around that part is\n |
| 0x2614d6 | 19 | still kinda hazy... |
| 0x2614ea | 47 | Hmm... If I recall correctly, I may have told\n |
| 0x26151a | 45 | you it was only a small medicinal experiment. |
| 0x261548 | 48 | What!? Did you make me your guinea pig without\n |
| 0x261579 | 17 | even telling me!? |
| 0x26158b | 48 | Calm down. The tests had been most conclusive.\n |
| 0x2615bc | 45 | It was absolutely, perfectly safe... I think. |
| 0x2615ea | 44 | That last part doesn't sound too sure to me. |
| 0x261617 | 46 | So, the final adjustments were in place, and\n |
| 0x261646 | 42 | all that remained was to wait for you to\n |
| 0x261671 | 8 | awaken-- |
| 0x26167a | 50 | But then, for reasons beyond my understanding...\n |
| 0x2616ad | 12 | it happened. |
| 0x2616ba | 8 | ..."It"? |
| 0x2616c3 | 13 | The calamity. |
| 0x2616d1 | 46 | A strange disease spread all across the world. |
| 0x261700 | 49 | An illness which melted--no... converted humans\n |
| 0x261732 | 26 | into gelatinous creatures. |
| 0x26174d | 9 | That's... |
| 0x261757 | 43 | Yes. Those things are what remains of them. |
| 0x261783 | 43 | That is not all. Those abominations would\n |
| 0x2617af | 47 | consume humans... consume anything considered\n |
| 0x2617df | 12 | to be alive. |
| 0x2617ec | 48 | As if its sole purpose is to wipe out all life\n |
| 0x26181d | 14 | as we know it. |
| 0x26182c | 50 | We knew not its cause, its mode of transmission,\n |
| 0x26185f | 46 | or its cure. One day your body would just...\n |
| 0x26188e | 10 | give way.  |
| 0x261899 | 46 | We spiraled into fear and chaos. Imagine the\n |
| 0x2618c8 | 50 | person next to you suddenly melting, then trying\n |
| 0x2618fb | 14 | to kill you... |
| 0x26190a | 46 | Even shelters completely closed off from the\n |
| 0x261939 | 28 | outside world meant nothing. |
| 0x261956 | 48 | Whether they were a god's divine punishment or\n |
| 0x261987 | 42 | a demon's infernal scourge, there was no\n |
| 0x2619b2 | 9 | escaping. |
| 0x2619bc | 42 | You must know by now that those who have\n |
| 0x2619e7 | 34 | dissolved into slime are immortal. |
| 0x261a0a | 38 | Whatever we did, there was no way to\n |
| 0x261a31 | 17 | exterminate them. |
| 0x261a43 | 46 | The few survivors panicked. They reached the\n |
| 0x261a72 | 46 | mad conclusion to try to wipe them out using\n |
| 0x261aa1 | 10 | Amaterasu. |
| 0x261aac | 47 | Hold on. Wasn't Amaterasu the weather control\n |
| 0x261adc | 47 | satellite...? I don't like where this is going. |
| 0x261b0c | 27 | It's just as you guessed.\n |
| 0x261b28 | 25 | They used it as a weapon. |
| 0x261b42 | 47 | ...What were they thinking? Amaterasu was the\n |
| 0x261b72 | 40 | whole key to Gaiaremediation, wasn't it? |
| 0x261b9b | 42 | If it's not used right, it could drop an\n |
| 0x261bc6 | 48 | artificial sun on Earth, or cause some kind of\n |
| 0x261bf7 | 18 | super hurricane... |
| 0x261c0a | 46 | Or even cause another ice age. They could've\n |
| 0x261c39 | 29 | turned Earth into an iceberg! |
| 0x261c57 | 42 | Even a child would understand that using\n |
| 0x261c82 | 44 | something like that as a weapon would just\n |
| 0x261caf | 12 | be bad news. |
| 0x261cbc | 47 | Indeed. The natural infrastructure collapsed,\n |
| 0x261cec | 46 | and the environment we had fought so hard to\n |
| 0x261d1b | 22 | rebuild was destroyed. |
| 0x261d32 | 43 | No one knew who would turn next. Paranoia\n |
| 0x261d5e | 46 | reigned, and everyone saw each other only as\n |
| 0x261d8d | 18 | potential enemies. |
| 0x261da0 | 42 | And so, society devolved into all-out war. |
| 0x261dcb | 36 | No... one could not call that war.\n |
| 0x261df0 | 44 | It was mindless carnage. Humans butchering\n |
| 0x261e1d | 19 | each other blindly. |
| 0x261e31 | 45 | At that point, human society had collapsed.\n |
| 0x261e5f | 47 | We were far beyond the point of regimented war. |
| 0x261e8f | 46 | The Earth quaked and burned with the heat of\n |
| 0x261ebe | 44 | many miniature suns, and tsunamis engulfed\n |
| 0x261eeb | 11 | the coasts. |
| 0x261ef7 | 47 | But I managed to survive somehow. As everyone\n |
| 0x261f27 | 45 | around me turned to slime, I ran for my life. |
| 0x261f55 | 48 | In the chaos, I miraculously found this place.\n |
| 0x261f86 | 45 | It was yet unfinished--near completion, but\n |
| 0x261fb4 | 9 | deserted. |
| 0x261fbe | 35 | I don't know how much time passed\n |
| 0x261fe2 | 22 | while I was in here... |
| 0x261ff9 | 44 | I regained control of Amaterasu with these\n |
| 0x262026 | 46 | systems, and created the flora in this small\n |
| 0x262055 | 36 | space... after much trial and error. |
| 0x26207a | 46 | And when I finally emerged, it was all over.\n |
| 0x2620a9 | 46 | I had been left behind... I was the only one\n |
| 0x2620d8 | 5 | left. |
| 0x2620de | 49 | I did everything I could to try to find others.\n |
| 0x262110 | 43 | But... I could find no trace of any other\n |
| 0x26213c | 7 | humans. |
| 0x262144 | 10 | Brother... |
| 0x26214f | 39 | I was left all alone in this world...\n |
| 0x262177 | 18 | It was unbearable. |
| 0x26218a | 47 | H-Hold on. Alone...? What about your wife and\n |
| 0x2621ba | 8 | Chii...? |
| 0x2621c3 | 46 | A smile crosses the Mikado's face--grim, and\n |
| 0x2621f2 | 7 | hollow. |
| 0x2621fa | 45 | ...They both melted away before my very eyes. |
| 0x262228 | 47 | My words could no longer reach them. They had\n |
| 0x262258 | 46 | become beings with no purpose but to consume\n |
| 0x262287 | 9 | all life. |
| 0x262291 | 5 | No... |
| 0x262297 | 30 | Then... Then what about her?\n |
| 0x2622b6 | 19 | She's right here... |
| 0x2622ca | 45 | I must have been sentimental, then. I found\n |
| 0x2622f8 | 46 | that these proxies survived the calamity and\n |
| 0x262327 | 20 | replaced humanity... |
| 0x26233c | 46 | And so... I walked in the footsteps of those\n |
| 0x26236b | 48 | who came before me, and committed the selfsame\n |
| 0x26239c | 4 | sin. |
| 0x2623a1 | 23 | Proxies...? You mean... |
| 0x2623b9 | 46 | That sick experiment they called "research"?\n |
| 0x2623e8 | 46 | Artificially-created humans... You can't have! |
| 0x262417 | 49 | The same. All thanks to the data you retrieved.\n |
| 0x262449 | 44 | Funny... I felt no guilt when playing god,\n |
| 0x262476 | 7 | myself. |
| 0x26247e | 45 | Indeed. This Honoka was created by using my\n |
| 0x2624ac | 41 | late wife's genetic data as a template.\n |
| 0x2624d6 | 31 | She is a proxy... a demi-human. |
| 0x2624f6 | 48 | They are beings different from us. They may be\n |
| 0x262527 | 31 | people, but they are not human. |
| 0x262547 | 32 | Then this Honoka... isn't her... |
| 0x262568 | 42 | Honoka smiles sadly at the Mikado's words. |
| 0x262593 | 28 | Wait... that means Chii is-- |
| 0x2625b0 | 42 | I created Anju in the same way, using my\n |
| 0x2625db | 31 | daughter's genetic information. |
| 0x2625fb | 19 | So the princess...? |
| 0x26260f | 48 | I created them... The people here. I gave them\n |
| 0x262640 | 47 | language, arithmetic, methods for hunting and\n |
| 0x262670 | 22 | farming... Many gifts. |
| 0x262687 | 44 | It was fun, seeing the innocents uplifted.\n |
| 0x2626b4 | 48 | Growing smarter. But an emptiness still filled\n |
| 0x2626e5 | 9 | my heart. |
| 0x2626ef | 46 | For these beings are not, and will never be,\n |
| 0x26271e | 6 | human. |
| 0x262725 | 50 | They worshipped me as a god, and I felt the rift\n |
| 0x262758 | 49 | between us widen. I knew I could not live among\n |
| 0x26278a | 5 | them. |
| 0x262790 | 45 | My interest in the surface world waned, and\n |
| 0x2627be | 47 | once again I sealed myself within this sanctum. |
| 0x2627ee | 44 | I had a mission... to find a way to return\n |
| 0x26281b | 45 | humanity to its true form. To see my family\n |
| 0x262849 | 6 | again. |
| 0x262850 | 45 | I understood perfectly well how reckless an\n |
| 0x26287e | 44 | undertaking this was, but it was all I had\n |
| 0x2628ab | 44 | ...I cannot say how much time passed after\n |
| 0x2628d8 | 44 | that. It felt like I spent an eternity here. |
| 0x262905 | 41 | A hundred years... two hundred years...\n |
| 0x26292f | 15 | Perhaps longer. |
| 0x26293f | 34 | Wait, what!? Two hundred years...? |
| 0x262962 | 47 | Right, the people say the Mikado's been alive\n |
| 0x262992 | 47 | for centuries. What's going on? That makes no\n |
| 0x2629c2 | 6 | sense. |
| 0x2629c9 | 48 | Well... I presume that would be the effects of\n |
| 0x2629fa | 45 | the medical trials and testing I put myself\n |
| 0x262a28 | 8 | through. |
| 0x262a31 | 4 | Wh-- |
| 0x262a36 | 47 | The intent was merely to increase my stamina,\n |
| 0x262a66 | 45 | but who knew it would extend my lifespan to\n |
| 0x262a94 | 15 | such lengths... |
| 0x262aa4 | 47 | I assume that is also the reason why I myself\n |
| 0x262ad4 | 42 | have not yet devolved into formless slime. |
| 0x262aff | 17 | What have you...? |
| 0x262b11 | 46 | I continued my research, but I soon realized\n |
| 0x262b40 | 39 | that even this facility has its limits. |
| 0x262b68 | 48 | That is why I chose once more to return to the\n |
| 0x262b99 | 8 | surface. |
| 0x262ba2 | 46 | Cities and facilities alike were lost to the\n |
| 0x262bd1 | 43 | calamity, but I thought to look among the\n |
| 0x262bfd | 42 | shelters for a way to continue my efforts. |
| 0x262c28 | 43 | However, when I emerged from underground,\n |
| 0x262c54 | 40 | what I saw waiting above astounded me... |
| 0x262c7d | 47 | Truly, it was an even greater shock than when\n |
| 0x262cad | 47 | I first ascended and found the world destroyed. |
| 0x262cdd | 34 | Before me lay the proxies' city.\n |
| 0x262d00 | 47 | It was no mere village... Entire kingdoms had\n |
| 0x262d30 | 21 | arisen in my absence. |
| 0x262d46 | 47 | I decided to ask their help in excavating the\n |
| 0x262d76 | 6 | ruins. |
| 0x262d7d | 49 | I offered them ample rewards--food and medicine\n |
| 0x262daf | 39 | I had synthesized within my facilities. |
| 0x262dd7 | 46 | However, their intellect had grown too much.\n |
| 0x262e06 | 41 | Their innocent, obedient minds had been\n |
| 0x262e30 | 19 | corrupted by greed. |
| 0x262e44 | 39 | They demanded more rewards, every time. |
| 0x262e6c | 38 | I tried to meet their demands. Their\n |
| 0x262e93 | 43 | developments did not please me, but I was\n |
| 0x262ebf | 19 | desperate for help. |
| 0x262ed3 | 45 | However, their avarice grew, and they began\n |
| 0x262f01 | 46 | plundering the ruins, asking high prices for\n |
| 0x262f30 | 12 | their finds. |
| 0x262f3d | 39 | ...Things that held no value to them.\n |
| 0x262f65 | 41 | Things that they had no understanding of. |
| 0x262f8f | 35 | I answered these demands as well.\n |
| 0x262fb3 | 46 | I grew angry with their hubris, but I had no\n |
| 0x262fe2 | 7 | choice. |
| 0x262fea | 49 | Metallurgic secrets for composing alloys, seeds\n |
| 0x26301c | 48 | for agriculture, secrets of well-digging, star\n |
| 0x26304d | 47 | charts... Trifles to me, revolutionary to them. |
| 0x26307d | 48 | Such prizes would overturn their power balance\n |
| 0x2630ae | 47 | almost overnight, but their political affairs\n |
| 0x2630de | 19 | did not concern me. |
| 0x2630f2 | 47 | Until one day, they chose to stand in my way... |
| 0x263122 | 22 | Such foolish children. |
| 0x263139 | 44 | They stole my secrets from each other, and\n |
| 0x263166 | 45 | some thought to capture me to monopolize my\n |
| 0x263194 | 10 | knowledge. |
| 0x26319f | 38 | It was the second time I had felt so\n |
| 0x2631c6 | 45 | disappointed. They were like us not only in\n |
| 0x2631f4 | 24 | appearance, but in soul. |
| 0x26320d | 46 | Most machinery they stole from the ruins was\n |
| 0x26323c | 42 | treated carelessly. They knew nothing...\n |
| 0x263267 | 43 | They ruined almost everything they touched. |
| 0x263293 | 44 | ...So I decided to discard my sympathy for\n |
| 0x2632c0 | 46 | them. They became mere obstacles to be dealt\n |
| 0x2632ef | 5 | with. |
| 0x2632f5 | 46 | I used the advanced knowledge and technology\n |
| 0x263324 | 48 | at my disposal to conquer them and form my own\n |
| 0x263355 | 5 | army. |
| 0x26335b | 46 | These demihumans are genetically predisposed\n |
| 0x26338a | 43 | to obey us humans, after all. It all went\n |
| 0x2633b6 | 22 | surprisingly smoothly. |
| 0x2633cd | 47 | I took those who were loyal to me, and seized\n |
| 0x2633fd | 43 | control of the ruins. I conquered all who\n |
| 0x263429 | 11 | opposed me. |
| 0x263435 | 34 | That... was the birth of Yamato... |
| 0x263458 | 44 | My liege, you mustn't lose your composure... |
| 0x263485 | 27 | H-Hmm, yes... You're right. |
| 0x2634a1 | 42 | After being calmed by Honoka's words, my\n |
| 0x2634cc | 46 | brother relaxes, leaning against the back of\n |
| 0x2634fb | 10 | his chair. |
| 0x263506 | 43 | Guess he's been through a lot... No, that\n |
| 0x263532 | 41 | doesn't even come close to describing it. |
| 0x26355c | 20 | And that is why I... |
| 0x263571 | 44 | There is another reason why I continued to\n |
| 0x26359e | 21 | excavate those ruins. |
| 0x2635b4 | 22 | I was looking for you. |
| 0x2635cb | 15 | Looking for me? |
| 0x2635db | 42 | The lab in which you underwent the final\n |
| 0x263606 | 48 | adjustments was an isolated facility, doubling\n |
| 0x263637 | 13 | as a shelter. |
| 0x263645 | 45 | I had lost track of it during the calamity,\n |
| 0x263673 | 48 | but I still had hope that I might one day find\n |
| 0x2636a4 | 4 | you. |
| 0x2636a9 | 44 | Haha... Yet I did not expect in my wildest\n |
| 0x2636d6 | 47 | dreams that you would be the one to come to me. |
| 0x263706 | 43 | After hearing the reports from Uruuru and\n |
| 0x263732 | 48 | Saraana, I could only laugh. It seemed my work\n |
| 0x263763 | 37 | had all been for nothing, in the end. |
| 0x263789 | 42 | Then, you knew about me from a while back? |
| 0x2637b4 | 47 | Yes, around the time you first arrived within\n |
| 0x2637e4 | 21 | the imperial capital. |
| 0x2637fa | 39 | So you knew from the beginning, then?\n |
| 0x263822 | 30 | Why didn't you tell me sooner? |
| 0x263841 | 47 | Be sensible, Haku. Of course I wanted to tell\n |
| 0x263871 | 46 | But would you have believed me if I suddenly\n |
| 0x2638a0 | 46 | appeared before you and declared myself your\n |
| 0x2638cf | 8 | brother? |
| 0x2638d8 | 7 | Urgh... |
| 0x2638e0 | 48 | Upon hearing of your presence, I had time only\n |
| 0x263911 | 48 | to rejoice briefly... before I learned of your\n |
| 0x263942 | 8 | amnesia. |
| 0x26394b | 48 | Because of that, I was unable to reveal myself\n |
| 0x26397c | 45 | to you. I was quite troubled, and unsure of\n |
| 0x2639aa | 11 | what to do. |
| 0x2639b6 | 45 | Well, you can't blame me for that. I didn't\n |
| 0x2639e4 | 43 | WANT to lose my memories. I had it pretty\n |
| 0x263a10 | 15 | rough myself... |
| 0x263a20 | 45 | Wait, so the reason you gave me these girls\n |
| 0x263a4e | 35 | and invited me over so many times-- |
| 0x263a72 | 45 | Yes, you seem to have the gist of it. These\n |
| 0x263aa0 | 39 | girls are fine caretakers, as well as\n |
| 0x263ac8 | 11 | bodyguards. |
| 0x263ad4 | 42 | Well, they are good at what they do, but\n |
| 0x263aff | 44 | they're still kind of a handful sometimes... |
| 0x263b2c | 8 | ...Haku. |
| 0x263b35 | 41 | His tone suddenly changes. I look to my\n |
| 0x263b5f | 44 | brother, surprised at the weariness in his\n |
| 0x263b8c | 6 | voice. |
| 0x263b93 | 47 | What I see before me isn't the absolute ruler\n |
| 0x263bc3 | 40 | of Yamato, the indomitable Mikado, but-- |
| 0x263bec | 24 | A tired, lonely old man. |
| 0x263c05 | 34 | I wish for you... to succeed me... |
| 0x263c28 | 25 | ...Huh? What did you say? |
| 0x263c42 | 29 | I don't mean... right away... |
| 0x263c60 | 46 | But I wish for you... to carry on my legacy... |
| 0x263c8f | 49 | Whoa, whoa, hold on. What are you saying all of\n |
| 0x263cc1 | 25 | a sudden...? Succeed you? |
| 0x263cdb | 41 | What about the princess!? Isn't she the\n |
| 0x263d05 | 29 | rightful heir to your throne? |
| 0x263d23 | 46 | That is true. I have arranged it so that she\n |
| 0x263d52 | 34 | will replace me as ruler, one day. |
| 0x263d75 | 33 | Then why are you telling me this? |
| 0x263d97 | 46 | I will have her continue to guide the people\n |
| 0x263dc6 | 12 | of Yamato... |
| 0x263dd3 | 48 | However... I... want you to carry on my legacy\n |
| 0x263e04 | 19 | as a human being... |
| 0x263e18 | 23 | I still don't get it.\n |
| 0x263e30 | 18 | What do you mean-- |
| 0x263e43 | 31 | I... do not have much longer... |
| 0x263e63 | 7 | ...Huh? |
| 0x263e6b | 49 | I have spent all my life trying to find a means\n |
| 0x263e9d | 19 | to save humanity... |
| 0x263eb1 | 43 | I have extended my life through countless\n |
| 0x263edd | 43 | procedures, but it seems my limit is fast\n |
| 0x263f09 | 14 | approaching... |
| 0x263f18 | 31 | W-Wait. You're joking... right? |
| 0x263f38 | 48 | Haha... I would never say such things in jest... |
| 0x263f69 | 44 | I may be revered as a god... but I am only\n |
| 0x263f96 | 44 | human... The laws of nature will bend, but\n |
| 0x263fc3 | 22 | they will not break... |
| 0x263fda | 50 | I do not have much time left. So... before I go,\n |
| 0x26400d | 36 | I would entrust everything to you... |
| 0x264032 | 43 | And... I want you to carry on my dream...\n |
| 0x26405e | 46 | one which I will never see become a reality... |
| 0x26408d | 42 | You want me... to carry on your legacy...? |
| 0x2640b8 | 29 | I can feel my body rising up. |
| 0x2640d6 | 44 | It's the opposite of the view from before.\n |
| 0x264103 | 45 | The scenery below shrinks gradually farther\n |
| 0x264131 | 5 | away. |
| 0x264137 | 47 | I silently stare at the view spreading across\n |
| 0x264167 | 10 | my vision. |
| 0x264172 | 28 | There's no turning back...\n |
| 0x26418f | 29 | So this is what Honoka meant. |
| 0x2641ad | 48 | I never expected things to play out like this... |
| 0x2641de | 46 | I didn't think in my wildest dreams that the\n |
| 0x26420d | 39 | Mikado would turn out to be my brother. |
| 0x264235 | 47 | That's why I felt like I've met him before...\n |
| 0x264265 | 23 | How could I not notice? |
| 0x26427d | 42 | The looks, the voice, the way he carries\n |
| 0x2642a8 | 45 | himself--it all matches up with the old man\n |
| 0x2642d6 | 15 | and my brother. |
| 0x2642e6 | 47 | I take a glance at my sister-in-l--at Honoka,\n |
| 0x264316 | 43 | who is standing next to my brother with a\n |
| 0x264342 | 13 | serene smile. |
| 0x264350 | 39 | Created from her genetic information... |
| 0x264378 | 28 | ...I can't really blame him. |
| 0x264395 | 49 | He said he had lived as the Mikado for hundreds\n |
| 0x2643c7 | 46 | of years. I can only imagine how lonely that\n |
| 0x2643f6 | 15 | must have been. |
| 0x264406 | 19 | And the princess... |
| 0x26441a | 45 | She was an exasperating self-centered brat,\n |
| 0x264448 | 42 | but a part of me couldn't just leave her\n |
| 0x264473 | 8 | alone... |
| 0x26447c | 45 | I see. I must have unconsciously remembered\n |
| 0x2644aa | 37 | Chii when I looked at the princess... |
| 0x2644d0 | 42 | ...But I still don't know the whole story. |
| 0x2644fb | 46 | He said he'd entrust everything to me, but I\n |
| 0x26452a | 44 | don't know what he plans on doing--what he\n |
| 0x264557 | 17 | wants ME to do... |
| 0x264569 | 47 | The dream that he said he wasn't able to make\n |
| 0x264599 | 47 | reality. He called it "humanity's salvation"... |
| 0x2645c9 | 33 | No, I can't. It's impossible...\n |
| 0x2645eb | 47 | That's too much for me. I can't follow in his\n |
| 0x26461b | 10 | footsteps. |
| 0x264626 | 5 | Hey-- |
| 0x26462c | 43 | I'm about to tell him, "Sorry, but I just\n |
| 0x264658 | 18 | can't," and then-- |
| 0x26466b | 20 | It was... so long... |
| 0x264680 | 45 | A dry, low whisper, as if all life has been\n |
| 0x2646ae | 17 | drained from him. |
| 0x2646c0 | 48 | That withered voice stops me from finishing my\n |
| 0x2646f1 | 9 | sentence. |
| 0x2646fb | 16 | So... So long... |
| 0x26470c | 48 | It almost felt as if an eternity had passed...\n |
| 0x26473d | 34 | But now... it's almost all over... |
| 0x264760 | 11 | My liege... |
| 0x26476c | 12 | Look... I... |
| 0x264779 | 49 | Hm... I do not wish to rush an answer from you.\n |
| 0x2647ab | 45 | You must take time to think of your future... |
| 0x2647d9 | 35 | Do not worry. We still have time.\n |
| 0x2647fd | 42 | I intend to live at least until Anju has\n |
| 0x264828 | 14 | come of age... |
| 0x264837 | 41 | But there is one thing I would have you\n |
| 0x264861 | 33 | remember. You are my last hope... |
| 0x264883 | 46 | Thanks to you... all my work will not be for\n |
| 0x2648b2 | 10 | nothing... |
| 0x2648bd | 43 | I have... finally been rewarded... for my\n |
| 0x2648e9 | 10 | actions... |
| 0x2648f4 | 22 | I leave... the rest... |
| 0x26490b | 41 | The last seems more to himself than me.\n |
| 0x264935 | 47 | The reedy voice is barely audible as he fades\n |
| 0x264965 | 14 | into the dark. |
| 0x2661ca | 25 | Finally done with work.\n |
| 0x2661e4 | 17 | Man, I'm tired... |
| 0x2661f6 | 20 | Hnngh!? M-My back... |
| 0x26620b | 45 | As I stretch, a dull pain spreads across my\n |
| 0x266239 | 38 | back, like a wave of pins and needles. |
| 0x266260 | 9 | Owowow... |
| 0x26626a | 45 | I guess I was sitting down all day. Maybe I\n |
| 0x266298 | 22 | should just go to bed. |
| 0x2662af | 30 | Hope it lets up by tomorrow... |
| 0x2662ce | 21 | Welcome back, Master. |
| 0x2662e4 | 32 | Gah!? Oh, it's just you two...\n |
| 0x266305 | 25 | Don't scare me like that. |
| 0x26631f | 43 | I jump back, startled by the twins in the\n |
| 0x26634b | 48 | darkness of my room. I never know when they'll\n |
| 0x26637c | 8 | show up. |
| 0x266385 | 45 | Sorry. If you need something, it'll have to\n |
| 0x2663b3 | 46 | wait until tomorrow. Right now, I just wanna\n |
| 0x2663e2 | 10 | go to bed. |
| 0x2663ed | 9 | Fatigued. |
| 0x2663f7 | 34 | You seem very exhausted, Master.\n |
| 0x26641a | 17 | Allow us to help. |
| 0x26642c | 38 | Help? How exactly do you plan to help? |
| 0x266453 | 8 | Healing. |
| 0x26645c | 42 | If you do not mind, we can help you relax. |
| 0x266487 | 9 | Lie down. |
| 0x266491 | 33 | Please, lie facedown on your bed. |
| 0x2664b3 | 12 | Facedown...? |
| 0x2664c0 | 50 | Since they usually try to seduce me every chance\n |
| 0x2664f3 | 47 | they get, I'm wary of any of their suggestions. |
| 0x266523 | 43 | Thankfully, they've stopped spontaneously\n |
| 0x26654f | 43 | stripping except to go to bed, but still,\n |
| 0x26657b | 10 | I dunno... |
| 0x266586 | 50 | I can't help but hesitate before following their\n |
| 0x2665b9 | 44 | directions... Honestly, I'm kinda scared to. |
| 0x2665e6 | 20 | We will massage you. |
| 0x2665fb | 41 | We shall give you a comforting rubdown,\n |
| 0x266625 | 27 | that it may help you relax. |
| 0x266641 | 19 | Just the shoulders. |
| 0x266655 | 45 | We will only touch your shoulders and back,\n |
| 0x266683 | 24 | to help you feel better. |
| 0x26669c | 22 | It will be over quick. |
| 0x2666b3 | 44 | All you must do is count the stains on the\n |
| 0x2666e0 | 43 | ceiling, and it will be over in an instant. |
| 0x26670c | 40 | How do I look at the ceiling while I'm\n |
| 0x266735 | 10 | facedown!? |
| 0x266740 | 47 | The two don't seem to be listening to me, and\n |
| 0x266770 | 42 | slowly close in on me as they flex their\n |
| 0x26679b | 8 | fingers. |
| 0x2667a4 | 50 | Oh, fine... Whatever. I'm starting to get a read\n |
| 0x2667d7 | 35 | on their actions recently, anyways. |
| 0x2667fb | 45 | And besides, if they can do something about\n |
| 0x266829 | 32 | this pain, I'd gladly accept it. |
| 0x26684a | 48 | I follow their instructions, and lie face down\n |
| 0x26687b | 10 | in my bed. |
| 0x266886 | 8 | This OK? |
| 0x26688f | 10 | Now relax. |
| 0x26689a | 47 | Please relax every muscle in your body, Master. |
| 0x2668ca | 48 | They sit on either side of me, and place their\n |
| 0x2668fb | 22 | hands on my shoulders. |
| 0x266912 | 48 | I can feel the warmth from their hands through\n |
| 0x266943 | 11 | my clothes. |
| 0x26694f | 11 | Now then... |
| 0x26695b | 20 | We will begin now... |
| 0x266970 | 20 | *Rub* *rub* *rub*... |
| 0x266985 | 14 | Hnngh!? Ahh... |
| 0x266994 | 49 | I can't restrain a little yelp of surprise when\n |
| 0x2669c6 | 26 | their hands begin to move. |
| 0x2669e1 | 45 | They methodically rub in slow patterns from\n |
| 0x266a0f | 46 | my neck down to my back, with just the right\n |
| 0x266a3e | 9 | pressure. |
| 0x266a48 | 48 | While Uruuru taps against me, Saraana runs her\n |
| 0x266a79 | 44 | fingers down my back as if to smooth it out. |
| 0x266aa6 | 43 | Hey, you two are... pretty good at this--\n |
| 0x266ad2 | 24 | Yeah, that's the spot... |
| 0x266aeb | 13 | Only natural. |
| 0x266af9 | 46 | It is a skill necessary to serve one's Master. |
| 0x266b28 | 23 | Know the flow of blood. |
| 0x266b40 | 49 | With just the right amount of pressure, we wash\n |
| 0x266b72 | 31 | away all the built-up tensions. |
| 0x266b92 | 48 | After that, they move themselves over my lower\n |
| 0x266bc3 | 14 | back and legs. |
| 0x266bd2 | 16 | Lower back next. |
| 0x266be3 | 49 | We will loosen up your lower back to relax your\n |
| 0x266c15 | 46 | whole body. It seems very stiff today, Master. |
| 0x266c44 | 49 | They then proceed to massage my back and thighs\n |
| 0x266c76 | 19 | in the same manner. |
| 0x266c8a | 47 | My spine and legs, achy from sitting down all\n |
| 0x266cba | 44 | day, gradually relax as the weariness fades. |
| 0x266ce7 | 45 | Man, this is amazing... I can feel all that\n |
| 0x266d15 | 27 | fatigue just slipping away. |
| 0x266d31 | 50 | I can feel myself getting more and more relaxed.\n |
| 0x266d64 | 37 | It's like I'm taking a nice bath or\n |
| 0x266d8a | 12 | something... |
| 0x266d97 | 23 | Hngh, ahh... That's it. |
| 0x266daf | 46 | Uruuru, can you do it a little stronger there? |
| 0x266dde | 14 | With pleasure. |
| 0x266ded | 45 | I am glad to hear that you are enjoying this. |
| 0x266e1b | 26 | To even greater heights... |
| 0x266e36 | 46 | We shall continue, so that you may know true\n |
| 0x266e65 | 6 | bliss! |
| 0x266e6c | 45 | They continue to massage me enthusiastically. |
| 0x266e9a | 47 | They now begin to massage my neck and thighs,\n |
| 0x266eca | 33 | as if to compete with each other. |
| 0x266eec | 43 | Ah... That feels great. I might just fall\n |
| 0x266f18 | 17 | asleep like this. |
| 0x266f2a | 28 | Maybe I could just doze off. |
| 0x266f47 | 42 | Little by little, I let my guard down as\n |
| 0x266f72 | 31 | drowsiness slowly overtakes me. |
| 0x266f92 | 11 | *Squish*... |
| 0x266f9e | 6 | ...Mm? |
| 0x266fa5 | 20 | *Squish*... *rub*... |
| 0x266fba | 23 | ...That better not be-- |
| 0x266fd2 | 44 | I tried to laugh it off, but the sensation\n |
| 0x266fff | 23 | definitely felt like... |
| 0x267017 | 24 | What exactly are you--\n |
| 0x267030 | 12 | Oh, come on! |
| 0x26703d | 48 | I look up to find Uruuru's exposed thigh right\n |
| 0x26706e | 11 | in my face. |
| 0x26707a | 46 | Goddamn these two. One-track minds, the pair\n |
| 0x2670a9 | 8 | of them. |
| 0x2670b2 | 48 | Saraana's also adjusted herself so her clothes\n |
| 0x2670e3 | 38 | are hiking up, exposing her even more. |
| 0x26710a | 46 | Clever. They must have learned that I'll run\n |
| 0x267139 | 43 | if they're too open about their intentions. |
| 0x267165 | 42 | Whatever. I'm gonna take a nap. I'm sure\n |
| 0x267190 | 32 | they'll both give up eventually. |
| 0x2671b1 | 46 | As I mumble to myself, the drowsiness begins\n |
| 0x2671e0 | 25 | to overtake me once more. |
| 0x2671fe | 9 | Uruuru... |
| 0x267208 | 46 | Saraana signals with her head. One twin goes\n |
| 0x267237 | 42 | for my top half, the other for the bottom. |
| 0x267262 | 46 | They wrap their legs around an arm and a leg\n |
| 0x267291 | 47 | respectively, and begin rubbing them back and\n |
| 0x2672c1 | 6 | forth. |
| 0x2672c8 | 8 | ...Mm... |
| 0x2672d1 | 8 | ...Ah... |
| 0x2672da | 45 | I can hear their heavy breathing every time\n |
| 0x267308 | 25 | they writhe closer to me. |
| 0x267322 | 47 | Nnngh... What's that noise? Wish they'd quiet\n |
| 0x267352 | 14 | down a little. |
| 0x267361 | 9 | ...Ohh... |
| 0x26736b | 9 | ...Ahh... |
| 0x267375 | 43 | They gasp out loudly, shuddering as their\n |
| 0x2673a1 | 45 | movements slow, but none of it feels really\n |
| 0x2673cf | 15 | relevant to me. |
| 0x2673df | 46 | I think... I'll be fine just going to sleep... |
| 0x26740e | 24 | I'm sure if I... fall... |
| 0x267427 | 10 | ...Master? |
| 0x267432 | 32 | Master, is something the matter? |
| 0x267453 | 48 | I let myself doze off. No matter how much they\n |
| 0x267484 | 47 | try to seduce me, it has no effect as I drift\n |
| 0x2674b4 | 9 | to sleep. |
| 0x2674be | 15 | ...No reaction. |
| 0x2674ce | 46 | It seems he has fallen asleep. In that case,\n |
| 0x2674fd | 43 | we will continue where we left off... Hmhm. |
| 0x267529 | 42 | They observe their master as he breathes\n |
| 0x267554 | 40 | rhythmically, and they carefully get up. |
| 0x26757d | 22 | All according to plan. |
| 0x267594 | 39 | All that is left is for us to finish... |
| 0x2675bc | 47 | And so they begin to take off his outer wear,\n |
| 0x2675ec | 34 | as though to mark the final touch. |
| 0x26760f | 45 | Completely asleep and breathing softly, his\n |
| 0x26763d | 29 | torso is now completely bare. |
| 0x26765b | 10 | And now... |
| 0x267666 | 16 | Master, do you-- |
| 0x267677 | 13 | ...!? Uruuru! |
| 0x26768a | 48 | Mm...? Why does my body feel so light all of a\n |
| 0x2676bb | 10 | sudden...? |
| 0x2676c6 | 37 | And I was just falling asleep, too.\n |
| 0x2676ec | 14 | What happened? |
| 0x2676fb | 32 | Someone standing behind me...?\n |
| 0x26771c | 23 | Oh, they're still here. |
| 0x267734 | 48 | Hey, could you keep going? My body still feels\n |
| 0x267765 | 15 | a little stiff. |
| 0x267775 | 47 | I call to the twins. I can feel them standing\n |
| 0x2677a5 | 10 | behind me. |
| 0x2677b0 | 11 | Keep going? |
| 0x2677bc | 38 | Yeah, I want you to do my back next.\n |
| 0x2677e3 | 28 | Especially around the spine. |
| 0x267800 | 16 | Are you sure...? |
| 0x267811 | 47 | Yeah, and make it a little stronger if you can. |
| 0x267841 | 32 | All right, if you insist... Hah! |
| 0x267862 | 33 | *CRUNCH* *Grind, grind, grind*... |
| 0x267884 | 18 | Hngk!? HaaaAAARGH! |
| 0x267897 | 44 | This is the exact opposite of the relaxing\n |
| 0x2678c4 | 43 | sensation moments ago. It's excruciating.\n |
| 0x2678f0 | 17 | I try to get up-- |
| 0x267902 | 31 | Gah... They're sitting on me!\n |
| 0x267922 | 15 | I can't get up! |
| 0x267932 | 29 | Haku, you have to stay still. |
| 0x267950 | 26 | W-Wait, that voice--Kuon!? |
| 0x26796b | 47 | You seem pretty tired. You're stiff all over.\n |
| 0x26799b | 42 | I'll do it a bit stronger, just like you\n |
| 0x2679c6 | 10 | requested. |
| 0x2679d1 | 13 | *Crrrrrrrrrk* |
| 0x2679df | 18 | GHK! Ghaaaaaaaahh! |
| 0x2679f2 | 46 | W-Wait a second... Where's Uruuru and Saraana? |
| 0x267a21 | 47 | Huh? I only saw you lying in your room when I\n |
| 0x267a51 | 8 | came in. |
| 0x267a5a | 46 | What!? But they were here just a moment ago... |
| 0x267a89 | 44 | Still pinned down, I crane my head to look\n |
| 0x267ab6 | 19 | around frantically. |
| 0x267aca | 42 | They're not here. When the hell did they\n |
| 0x267af5 | 7 | leave!? |
| 0x267afd | 17 | *Grind* *grrrrrk* |
| 0x267b0f | 45 | Hrgaaah! A-Anyway, you have to get off now... |
| 0x267b3d | 21 | You've done enough... |
| 0x267b53 | 44 | No, you need to get all the tension points\n |
| 0x267b80 | 31 | relaxed before you fall asleep. |
| 0x267ba0 | 46 | It looks like you're still pretty exhausted.\n |
| 0x267bcf | 24 | I'll keep going for now. |
| 0x267be8 | 8 | W-Wait-- |
| 0x267bf1 | 29 | Now, I need you to lie still! |
| 0x267c0f | 47 | She then presses down hard around my shoulder\n |
| 0x267c3f | 40 | blades, grinding her thumb into my back. |
| 0x267c68 | 26 | Guh!? P-Please... mercy... |
| 0x267c83 | 43 | If this continues, the only sleep I'll be\n |
| 0x267caf | 44 | getting is the one you never wake up from... |
| 0x267cdc | 48 | These pressure points might hurt a little, but\n |
| 0x267d0d | 49 | they work. Don't grin and bear it--just tell me\n |
| 0x267d3f | 12 | if it hurts. |
| 0x267d4c | 9 | It HURTS! |
| 0x267d56 | 46 | Well, maybe you need to bear it a little more. |
| 0x267d85 | 17 | Huh? Wait, Kuon-- |
| 0x267d97 | 18 | *THUNK* *Grrrrrrk* |
| 0x267daa | 26 | Hngyaaaaaaaaaaaaaarrgghh!! |
| 0x267dc5 | 48 | I feel a jolt of pain shoot through me as Kuon\n |
| 0x267df6 | 45 | jams her finger into where my back and neck\n |
| 0x267e24 | 8 | connect. |
| 0x267e2d | 44 | The drowsiness that was washing over me is\n |
| 0x267e5a | 10 | long gone. |
| 0x267e65 | 42 | Guhhh... Hhhow did it end up like this...? |
| 0x267e90 | 34 | There is nobody remaining in the\n |
| 0x267eb3 | 32 | room who can answer my question. |
| 0x267ed4 | 12 | Interrupted. |
| 0x267ee1 | 40 | Yes, Kuon's actions have interrupted us. |
| 0x267f0a | 16 | Change of plans. |
| 0x267f1b | 46 | It seems we may have to rethink our strategy\n |
| 0x267f4a | 6 | a bit. |
| 0x267f51 | 10 | Next time. |
| 0x267f5c | 44 | Yes. Next time we will succeed in enticing\n |
| 0x267f89 | 7 | Master. |
| 0x267f91 | 17 | Gwaaaaaarrrgghh!! |
| 0x267fa3 | 8 | Failure. |
| 0x267fac | 45 | Yes. Today ended in failure. But next time,\n |
| 0x267fda | 19 | we shall prevail... |
| 0x267fee | 48 | The twins harden their resolve as their Master\n |
| 0x26801f | 28 | writhes in pain behind them. |
| 0x26803c | 48 | And so another peaceful day passes at the inn... |
| 0x2697f7 | 21 | *Grind*... *Grind*... |
| 0x26980d | 46 | A little past noon, the sound of herbs being\n |
| 0x26983c | 30 | ground down fills Kuon's room. |
| 0x26985b | 18 | Is this... enough? |
| 0x26986e | 47 | My pestle slows, and I peer into the contents\n |
| 0x26989e | 14 | of the mortar. |
| 0x2698ad | 48 | How are things coming along on your end, Haku?\n |
| 0x2698de | 16 | Is it ready yet? |
| 0x2698ef | 27 | Well, you think this'll do? |
| 0x26990b | 47 | Mhm, that should work fine. And next we add a\n |
| 0x26993b | 19 | pinch of pecalpe... |
| 0x26994f | 49 | She takes the mortar I pass over, and adds some\n |
| 0x269981 | 46 | kind of powder I've never heard of to the mix. |
| 0x2699b0 | 49 | ...Good. That should do it. Thanks for all your\n |
| 0x2699e2 | 11 | help, Haku. |
| 0x2699ee | 50 | Whew, finally over... I'm exhausted. This really\n |
| 0x269a21 | 49 | does take a lot. My arms are sore--I can barely\n |
| 0x269a53 | 5 | move. |
| 0x269a59 | 47 | Nicely done, Haku. You were a big help today.\n |
| 0x269a89 | 49 | This takes so many ingredients, so I needed the\n |
| 0x269abb | 7 | hand... |
| 0x269ac3 | 46 | Well, I didn't mind helping... I just wasn't\n |
| 0x269af2 | 29 | expecting it to be this hard. |
| 0x269b10 | 43 | Haha, let me at least get you some tea as\n |
| 0x269b3c | 7 | thanks. |
| 0x269b44 | 45 | Thanks. Make it real strong, with plenty of\n |
| 0x269b72 | 15 | milk and sugar. |
| 0x269b82 | 36 | Fine, fine. Just wait here a moment. |
| 0x269ba7 | 45 | As Kuon gets up to leave, the door suddenly\n |
| 0x269bd5 | 27 | opens and someone peeks in. |
| 0x269bf1 | 46 | Hey, you in here, Kuon? You want to hang out\n |
| 0x269c20 | 6 | a bit? |
| 0x269c27 | 14 | Oh, hey, Atuy. |
| 0x269c36 | 46 | Oh, you're here too, love? What were you two\n |
| 0x269c65 | 20 | doing here together? |
| 0x269c7a | 48 | Been helping Kuon with this stuff since morning. |
| 0x269cab | 45 | Help... Oh, dear. This looks like something\n |
| 0x269cd9 | 31 | terribly bitter. What's it for? |
| 0x269cf9 | 46 | This one's a nourishing tonic. I thought I'd\n |
| 0x269d28 | 19 | have Haku drink it. |
| 0x269d3c | 47 | ...Hang on. You want ME to drink this medicine? |
| 0x269d6c | 39 | Did I not mention before? You've been\n |
| 0x269d94 | 45 | complaining so much recently about being so\n |
| 0x269dc2 | 19 | tired all the time. |
| 0x269dd6 | 46 | First I've heard of it! You want me to drink\n |
| 0x269e05 | 46 | this when it's clearly going to be bitter as\n |
| 0x269e34 | 8 | hell...? |
| 0x269e3d | 45 | Don't worry. It might look bitter, but it's\n |
| 0x269e6b | 39 | actually sweet and quite easy to drink. |
| 0x269e93 | 11 | S-Sweet...? |
| 0x269e9f | 49 | She's lying. She's gotta be. The only word that\n |
| 0x269ed1 | 41 | comes to my head when I look at this is\n |
| 0x269efb | 11 | "bitter"... |
| 0x269f07 | 47 | I eye the murky green paste in the bowl. Even\n |
| 0x269f37 | 48 | trying to imagine the taste just makes my face\n |
| 0x269f68 | 8 | contort. |
| 0x269f71 | 48 | Really? I wasn't expecting that. I thought all\n |
| 0x269fa2 | 35 | medicine was supposed to be bitter. |
| 0x269fc6 | 45 | Medicine doesn't have to taste bad to work.\n |
| 0x269ff4 | 45 | And besides, sweet things are often good as\n |
| 0x26a022 | 11 | stimulants. |
| 0x26a02e | 48 | Some things even taste spicy, so as to elevate\n |
| 0x26a05f | 23 | the body's temperature. |
| 0x26a077 | 50 | Hmmm. Sounds like there's all kinds of medicine,\n |
| 0x26a0aa | 5 | then? |
| 0x26a0b0 | 49 | Mhm. There are a multitude of effects depending\n |
| 0x26a0e2 | 42 | on the mixture, so it's a lot to remember. |
| 0x26a10d | 47 | A multitude... Ooh, ooh, do you have anything\n |
| 0x26a13d | 25 | like a medicine for love? |
| 0x26a157 | 17 | Huh...? For love? |
| 0x26a169 | 46 | At the bizarre question, Kuon just stares at\n |
| 0x26a198 | 26 | Atuy for a couple seconds. |
| 0x26a1b3 | 49 | Yep! I was just wondering if you knew something\n |
| 0x26a1e5 | 45 | about it, since you're an apothecary and all. |
| 0x26a213 | 47 | What, a medicine that literally makes someone\n |
| 0x26a243 | 13 | fall in love? |
| 0x26a251 | 45 | Something like that! I'm not so good on the\n |
| 0x26a27f | 47 | details, but I've been curious about it for a\n |
| 0x26a2af | 10 | long time. |
| 0x26a2ba | 15 | A long time...? |
| 0x26a2ca | 48 | I saw someone selling one, back in my country.\n |
| 0x26a2fb | 43 | This really shady fellow was talking to a\n |
| 0x26a327 | 6 | woman. |
| 0x26a32e | 50 | I eavesdropped a bit, and heard the lady was sad\n |
| 0x26a361 | 43 | that her husband wasn't interested in her\n |
| 0x26a38d | 7 | lately. |
| 0x26a395 | 49 | So the man goes "Roight, luv, give 'im this and\n |
| 0x26a3c7 | 43 | 'e'll be all over yeh!" And he gave her a\n |
| 0x26a3f3 | 7 | bottle! |
| 0x26a3fb | 48 | A-All over her...? So that's your "medicine of\n |
| 0x26a42c | 12 | love", Atuy? |
| 0x26a439 | 48 | From how the guy was selling it, I'd be pretty\n |
| 0x26a46a | 42 | suspicious of whatever's in that bottle... |
| 0x26a495 | 41 | Um, Atuy. Are you perhaps talking about-- |
| 0x26a4bf | 46 | I asked for one too, but he just scowled and\n |
| 0x26a4ee | 47 | said, "Yeh're too young, kid." I couldn't get\n |
| 0x26a51e | 4 | any! |
| 0x26a523 | 30 | *Sigh*... I suspected as much. |
| 0x26a542 | 45 | Kuon gives an understanding nod, apparently\n |
| 0x26a570 | 35 | realizing what she's talking about. |
| 0x26a594 | 44 | I'm pretty sure this salesman of yours was\n |
| 0x26a5c1 | 29 | talking about an aphrodisiac. |
| 0x26a5df | 15 | An aphrodisiac? |
| 0x26a5ef | 43 | It seems like Atuy's never heard the term\n |
| 0x26a61b | 41 | before. She tilts her head in puzzlement. |
| 0x26a645 | 43 | What's that? What kind of medicine is it?\n |
| 0x26a671 | 38 | Is it a proper medicine of love? Well? |
| 0x26a698 | 33 | What... kind of medicine is it.\n |
| 0x26a6ba | 12 | Um, well...? |
| 0x26a6c7 | 6 | Well!? |
| 0x26a6ce | 44 | Atuy leans over, focused intently on Kuon.\n |
| 0x26a6fb | 40 | She seems very interested in this topic. |
| 0x26a724 | 46 | Well... it stimulates your body so that you,\n |
| 0x26a753 | 5 | ah... |
| 0x26a759 | 47 | You what? What is it? What does it make you do? |
| 0x26a789 | 45 | Y-You, ah... Haku! Why don't you explain it\n |
| 0x26a7b7 | 7 | to her? |
| 0x26a7bf | 48 | Kuon's gaze drifts around the room and finally\n |
| 0x26a7f0 | 35 | settles on me, her face bright red. |
| 0x26a814 | 44 | I'm sure he can explain it better than me!\n |
| 0x26a841 | 44 | Right, Haku? See, he says he'll explain it\n |
| 0x26a86e | 7 | to you. |
| 0x26a876 | 45 | Me? Aren't YOU the authority on this herbal\n |
| 0x26a8a4 | 6 | stuff? |
| 0x26a8ab | 23 | Just explain it to her! |
| 0x26a8c3 | 42 | Kuon quickly turns away after making her\n |
| 0x26a8ee | 8 | demands. |
| 0x26a8f7 | 46 | Why's she acting like that? She seems pretty\n |
| 0x26a926 | 44 | agitated... Whatever, I don't see any harm\n |
| 0x26a953 | 6 | in it. |
| 0x26a95a | 47 | Well, to be blunt, an aphrodisiac is a sexual\n |
| 0x26a98a | 47 | stimulant. By manipulating body chemistry, it\n |
| 0x26a9ba | 39 | makes one more inclined to fornication. |
| 0x26a9e2 | 43 | So when you drink it, your libido greatly\n |
| 0x26aa0e | 48 | intensifies, and you end up consumed with your\n |
| 0x26aa3f | 9 | own lust. |
| 0x26aa4d | 50 | Kuon is blushing furiously. She's staying quiet,\n |
| 0x26aa80 | 46 | but I can see her ears perking at every word\n |
| 0x26aaaf | 6 | I say. |
| 0x26aab6 | 47 | Ooh, it sounds like a proper drop of passion.\n |
| 0x26aae6 | 49 | You think that'd make someone fall in love with\n |
| 0x26ab18 | 3 | me? |
| 0x26ab1c | 48 | I mean, loosely speaking, sort of? But I think\n |
| 0x26ab4d | 44 | you're misunderstanding what this stuff is\n |
| 0x26ab7a | 12 | meant for... |
| 0x26ab87 | 44 | Oh, that sounds lovely! I wonder how a man\n |
| 0x26abb4 | 40 | would approach me after a sip of that... |
| 0x26abdd | 48 | Seems like she's not listening to a word I say\n |
| 0x26ac0e | 43 | anymore. She's off in her own little world. |
| 0x26ac3a | 46 | She's not listening at all... Wait a second,\n |
| 0x26ac69 | 30 | though, do those really exist? |
| 0x26ac88 | 44 | If I remember right, most of the so-called\n |
| 0x26acb5 | 48 | aphrodisiacs are fake. I've never heard of one\n |
| 0x26ace6 | 19 | actually working... |
| 0x26acfa | 44 | Hey, Kuon... Quick question; are there any\n |
| 0x26ad27 | 18 | real aphrodisiacs? |
| 0x26ad3a | 44 | ...Wh-What exactly is that supposed to mean? |
| 0x26ad67 | 47 | Just curious. I've heard most stuff they call\n |
| 0x26ad97 | 28 | aphrodisiacs are just fakes. |
| 0x26adb4 | 24 | Oh dear... is that true? |
| 0x26adcd | 48 | Yeah, I hear most of them are just stimulants,\n |
| 0x26adfe | 27 | or they energize you a bit. |
| 0x26ae1a | 42 | Then was that one a fake too? Now that I\n |
| 0x26ae45 | 49 | remember, that lady looked awfully disappointed\n |
| 0x26ae77 | 13 | the next day. |
| 0x26ae85 | 29 | So what's the answer, Kuon?\n |
| 0x26aea3 | 27 | Do real aphrodisiacs exist? |
| 0x26aebf | 5 | Um... |
| 0x26aec5 | 26 | Tell me, tell me, tell me! |
| 0x26aee0 | 43 | Kuon backs off a little, pressured by the\n |
| 0x26af0c | 48 | combination of innocence and resolve in Atuy's\n |
| 0x26af3d | 5 | eyes. |
| 0x26af43 | 43 | ...They do exist in a manner of speaking.\n |
| 0x26af6f | 40 | I have been taught how to make such...\n |
| 0x26af98 | 11 | substances. |
| 0x26afa4 | 48 | And just so we're clear, I'm not going to make\n |
| 0x26afd5 | 12 | any for you. |
| 0x26afe2 | 26 | Why? It sounds like fun... |
| 0x26affd | 48 | Just as Haku said, you're misunderstanding the\n |
| 0x26b02e | 15 | core problem... |
| 0x26b03e | 47 | But the medicine does make a man want a girl,\n |
| 0x26b06e | 28 | right? That's what you said. |
| 0x26b08b | 47 | It makes them want--It just excites them. But\n |
| 0x26b0bb | 36 | that doesn't mean they fall in love. |
| 0x26b0e0 | 49 | Oh... So it's different. So does a medicine for\n |
| 0x26b112 | 15 | love not exist? |
| 0x26b122 | 42 | That's not quite true... I'm pretty sure\n |
| 0x26b14d | 33 | you're looking for a love potion. |
| 0x26b16f | 44 | A love potion...? So if someone drinks it,\n |
| 0x26b19c | 44 | they'll fall in love with me? Real, proper\n |
| 0x26b1c9 | 5 | love? |
| 0x26b1cf | 23 | ...Something like that. |
| 0x26b1e7 | 27 | So could you make it, then? |
| 0x26b203 | 48 | ...I could, but preparing it would be a little\n |
| 0x26b234 | 12 | complicated. |
| 0x26b241 | 45 | What part of the process is so complicated,\n |
| 0x26b26f | 40 | It's a very difficult mixture to make.\n |
| 0x26b298 | 47 | I'm sure my mother would have been able to do\n |
| 0x26b2c8 | 10 | it, but... |
| 0x26b2d3 | 48 | I see... So it'd be impossible for you to whip\n |
| 0x26b304 | 6 | it up. |
| 0x26b30b | 48 | Atuy droops her shoulders, clearly disappointed. |
| 0x26b33c | 47 | I'm not saying I can't, but since handling it\n |
| 0x26b36c | 45 | requires a lot of care, I've been forbidden\n |
| 0x26b39a | 15 | from making it. |
| 0x26b3aa | 25 | Forbidden? Why's that...? |
| 0x26b3c4 | 50 | That kind of potion is considered taboo. Forcing\n |
| 0x26b3f7 | 46 | someone to love you is a form of mind control. |
| 0x26b426 | 49 | If something like that gets in the wrong hands,\n |
| 0x26b458 | 49 | it'd be disastrous... You see the implications,\n |
| 0x26b48a | 5 | Haku? |
| 0x26b490 | 45 | Yeah, true... if that was common, it'd be a\n |
| 0x26b4be | 48 | huge mess. Make an owlo drink it, and you'd be\n |
| 0x26b4ef | 13 | set for life. |
| 0x26b4fd | 50 | Heck, it would only take a single potion to take\n |
| 0x26b530 | 45 | control of a whole country. No wonder she's\n |
| 0x26b55e | 6 | antsy. |
| 0x26b565 | 47 | ...So you're saying it's a terribly dangerous\n |
| 0x26b595 | 48 | potion...? I suppose I mustn't ask you to make\n |
| 0x26b5c6 | 9 | it, then. |
| 0x26b5d0 | 47 | That's why Mother told me time and time again\n |
| 0x26b600 | 48 | to never use it. So it's not that I can't make\n |
| 0x26b631 | 7 | it, OK? |
| 0x26b639 | 26 | ...But isn't that curious? |
| 0x26b654 | 44 | What is? It's rare to see you this serious\n |
| 0x26b681 | 16 | about something. |
| 0x26b692 | 47 | Well, if this potion is so awfully dangerous,\n |
| 0x26b6c2 | 46 | why do they still teach people how to make it? |
| 0x26b6f1 | 47 | ...You're right. It does sound as though they\n |
| 0x26b721 | 32 | keep passing down the formula... |
| 0x26b742 | 46 | And the fact that you can make it means that\n |
| 0x26b771 | 48 | somebody, somewhere in the past, has confirmed\n |
| 0x26b7a2 | 9 | it works. |
| 0x26b7ac | 45 | The lady's got a point! Pretty sharp there,\n |
| 0x26b7da | 5 | Atuy. |
| 0x26b7e0 | 7 | Huh...? |
| 0x26b7e8 | 48 | Kuon, do you know any stories of people who've\n |
| 0x26b819 | 45 | tried it? Say... Maybe your mama, or someone! |
| 0x26b847 | 47 | Um... I... don't think I've heard any stories\n |
| 0x26b877 | 26 | of it being used recently. |
| 0x26b892 | 46 | Kuon slowly averts her eyes from Atuy's wide\n |
| 0x26b8c1 | 18 | and curious stare. |
| 0x26b8d4 | 50 | Doesn't have to be recently! I'd love it ever so\n |
| 0x26b907 | 15 | if you told me. |
| 0x26b917 | 50 | The more vague answers Kuon gives, the more Atuy\n |
| 0x26b94a | 41 | zeroes in on her, slowly shifting closer. |
| 0x26b974 | 50 | Why do you want to hear so much about it? Do you\n |
| 0x26b9a7 | 46 | have someone in particular you want to drink\n |
| 0x26b9d6 | 6 | it...? |
| 0x26b9dd | 47 | Me? Mmm, no, nobody's popping into my head...\n |
| 0x26ba0d | 42 | but you know, it sounds like such a laugh! |
| 0x26ba38 | 47 | ...I get the feeling you wouldn't really like\n |
| 0x26ba68 | 16 | the story, Atuy. |
| 0x26ba79 | 27 | So you won't tell me, then? |
| 0x26ba95 | 32 | Umm... Let's leave it at that!\n |
| 0x26bab6 | 30 | I'm going to go make some tea! |
| 0x26bad5 | 22 | Huh? Why, Kuon!? Why!? |
| 0x26baec | 48 | Atuy pleads with her, but Kuon quickly escapes\n |
| 0x26bb1d | 45 | into the hallway, dashing off with a clatter. |
| 0x26bb4b | 46 | ...If they do exist, I'm sure it'd be a real\n |
| 0x26bb7a | 48 | hassle for the people who know how to make them. |
| 0x26bbab | 50 | People would do anything they could to get ahold\n |
| 0x26bbde | 47 | of it, and the makers would have to run, like\n |
| 0x26bc0e | 19 | Kuon's doing now... |
| 0x26bc22 | 28 | C'mon Kuon, pretty please!\n |
| 0x26bc3f | 17 | I want to knooow! |
| 0x26bc51 | 13 | I said noooo! |
| 0x26bc5f | 46 | The two of them continue their pointless cat\n |
| 0x26bc8e | 40 | and mouse chase for the rest of the day. |
| 0x26cf1b | 43 | Oshtor's assignment ended up taking a lot\n |
| 0x26cf47 | 23 | longer than I expected. |
| 0x26cf5f | 43 | Thanks to that, by the time we head home,\n |
| 0x26cf8b | 26 | the sun's already setting. |
| 0x26cfaa | 43 | Nekone walks silently a little ahead of me. |
| 0x26cfd6 | 49 | I guess it's pretty rare for just the two of us\n |
| 0x26d008 | 22 | to be out like this... |
| 0x26d01f | 43 | As the thought crosses my mind, I call to\n |
| 0x26d04b | 7 | Nekone. |
| 0x26d053 | 20 | ...You tired at all? |
| 0x26d068 | 48 | It is only natural. We have just performed our\n |
| 0x26d099 | 5 | task. |
| 0x26d09f | 41 | She answers me without even looking back. |
| 0x26d0c9 | 45 | No reason to rush home, right? Why don't we\n |
| 0x26d0f7 | 35 | visit the shops before we get back? |
| 0x26d11b | 46 | Our task is not complete until we return home. |
| 0x26d14a | 48 | Don't be so stiff. I'm getting a little hungry\n |
| 0x26d17b | 42 | after having a drink back at that mansion. |
| 0x26d1a6 | 50 | Your function there was to serve as a bodyguard.\n |
| 0x26d1d9 | 47 | Why would you get drunk during a job like that? |
| 0x26d209 | 20 | Hey, I wasn't drunk! |
| 0x26d21e | 44 | And THEY challenged ME. "A crony to such a\n |
| 0x26d24b | 46 | prissy lord wouldn't know good drink." I had\n |
| 0x26d27a | 20 | to defend his honor! |
| 0x26d28f | 41 | See? Clearly I had no choice, under the\n |
| 0x26d2b9 | 14 | circumstances. |
| 0x26d2c8 | 45 | I am speechless. You are positively full of\n |
| 0x26d2f6 | 8 | excuses. |
| 0x26d2ff | 46 | Even her usual uptight speech can't hide the\n |
| 0x26d32e | 23 | weariness in her voice. |
| 0x26d346 | 43 | There was a conference between a bunch of\n |
| 0x26d372 | 48 | powerful nobles just now. Oshtor was too busy,\n |
| 0x26d3a3 | 5 | so... |
| 0x26d3a9 | 48 | Nekone attended the conference in his stead as\n |
| 0x26d3da | 48 | the prodigy scholar, and fulfilled the role of\n |
| 0x26d40b | 8 | advisor. |
| 0x26d414 | 49 | And I was given the job of being her bodyguard... |
| 0x26d446 | 47 | But in the end, none of the nobles needed any\n |
| 0x26d476 | 46 | information from Nekone on the status of the\n |
| 0x26d4a5 | 7 | city... |
| 0x26d4ad | 50 | So in the end, we were just there sitting around\n |
| 0x26d4e0 | 32 | uselessly to appease the nobles. |
| 0x26d501 | 46 | And that's why Nekone's in such a foul mood... |
| 0x26d530 | 45 | You know, when I see her walking like this,\n |
| 0x26d55e | 41 | she just looks like a normal little girl. |
| 0x26d588 | 49 | She's smarter than other scholars, and aced her\n |
| 0x26d5ba | 46 | exam... She must face a lot of curiosity and\n |
| 0x26d5e9 | 9 | jealousy. |
| 0x26d5f3 | 46 | But Nekone does her best for the sake of her\n |
| 0x26d622 | 45 | brother. I'm sure she keeps a lot bottled up. |
| 0x26d650 | 46 | I think she could act her age a little more,\n |
| 0x26d67f | 42 | though. After all, she's still only a kid. |
| 0x26d6aa | 42 | ...And what are you pondering so intently? |
| 0x26d6d5 | 18 | Crap. She's sharp. |
| 0x26d6e8 | 48 | Guess there's no helping it. I usually try not\n |
| 0x26d719 | 29 | to be such a busybody, but... |
| 0x26d737 | 12 | Hey, Nekone. |
| 0x26d744 | 49 | If something troubles you, you must speak of it\n |
| 0x26d776 | 47 | freely, not keep it pent up. That is best for\n |
| 0x26d7a6 | 4 | all. |
| 0x26d7ab | 47 | You have a bad habit of trying to take on all\n |
| 0x26d7db | 49 | the burdens yourself. You can afford to rely on\n |
| 0x26d80d | 18 | others a bit more. |
| 0x26d820 | 48 | I give Nekone some sage advice while mimicking\n |
| 0x26d851 | 14 | Oshtor's tone. |
| 0x26d860 | 43 | She doesn't seem to be reacting much to it. |
| 0x26d88c | 48 | ...Or she's completely ignoring me. Come on, I\n |
| 0x26d8bd | 48 | thought my Oshtor impression was getting better. |
| 0x26d8ee | 30 | Fine, I'll play my trump card. |
| 0x26d90d | 47 | I pull out the object I carry around for such\n |
| 0x26d93d | 37 | an occasion, and affix it to my face. |
| 0x26d963 | 49 | ...Nekone. I will not be able to remain at your\n |
| 0x26d995 | 13 | side forever. |
| 0x26d9a3 | 45 | If you ever feel lonely, do not hesitate to\n |
| 0x26d9d1 | 48 | treat Haku as another brother. You may ask him\n |
| 0x26da02 | 7 | anyth-- |
| 0x26da0a | 7 | *Thump* |
| 0x26da12 | 5 | Gah!? |
| 0x26da18 | 33 | She kicked me right in the shins! |
| 0x26da3a | 45 | I cannot BELIEVE you still carry that cheap\n |
| 0x26da68 | 28 | imitation around with you... |
| 0x26da85 | 47 | You... Would you stop kicking me every single\n |
| 0x26dab5 | 44 | damn time!? C'mon, I thought it was pretty\n |
| 0x26dae2 | 6 | funny! |
| 0x26dae9 | 9 | ...*Sigh* |
| 0x26daf3 | 34 | Nekone fixes me with a cold stare. |
| 0x26db16 | 48 | Because of the dim light, I can't tell whether\n |
| 0x26db47 | 40 | the expression on her face is anger or\n |
| 0x26db70 | 13 | exasperation. |
| 0x26db7e | 48 | Oh, Neko and Oshtor! What a lovely coincidence\n |
| 0x26dbaf | 30 | to run into you two like this. |
| 0x26dbce | 49 | Hm, well met. I did not expect to encounter you\n |
| 0x26dc00 | 26 | by chance in such an area. |
| 0x26dc1b | 41 | Did I get in the way of some family time? |
| 0x26dc45 | 49 | Not at all. I was just having some trouble with\n |
| 0x26dc77 | 48 | Nekone. She does not seem to want to listen to\n |
| 0x26dca8 | 11 | my counsel. |
| 0x26dcb4 | 45 | Nekone not listening to you? Well, that's a\n |
| 0x26dce2 | 25 | bit curious, isn't it...? |
| 0x26dcfc | 26 | Neko, what's the matt--Hm? |
| 0x26dd17 | 48 | A sudden gust blows the paper mask askew for a\n |
| 0x26dd48 | 48 | moment, revealing my true face. Guess it's not\n |
| 0x26dd79 | 12 | that secure. |
| 0x26dd86 | 48 | I quickly replace it as Atuy tilts her head in\n |
| 0x26ddb7 | 34 | bafflement, staring closely at me. |
| 0x26ddda | 45 | Something's kind of strange with you today,\n |
| 0x26de08 | 43 | Oshtor... Or is that you under there, love? |
| 0x26de34 | 41 | Ha ha ha! Well, I suppose the jig is up-- |
| 0x26de5e | 4 | Gah! |
| 0x26de63 | 46 | I get kicked again, and as I recoil in pain,\n |
| 0x26de92 | 34 | Nekone yanks the mask off my face. |
| 0x26deb5 | 28 | W-Would you quit that alre-- |
| 0x26ded2 | 35 | This is what I think of your "jig"! |
| 0x26def6 | 48 | Nekone crushes my paper mask in her hands, and\n |
| 0x26df27 | 49 | throws my masterwork on the ground like a piece\n |
| 0x26df59 | 9 | of trash. |
| 0x26df63 | 44 | Awwww, c'mon. That one was my masterpiece... |
| 0x26df90 | 45 | I quickly snatch it up, but it seems beyond\n |
| 0x26dfbe | 7 | repair. |
| 0x26dfc6 | 31 | Oh, so it really was you, love. |
| 0x26dfe6 | 45 | Your voice and your demeanor were just like\n |
| 0x26e014 | 48 | Oshtor. I honestly couldn't tell the difference. |
| 0x26e045 | 47 | But why were you pretending to be Oshtor just\n |
| 0x26e075 | 4 | now? |
| 0x26e07a | 49 | Eh, no real reason. Just thought it might be...\n |
| 0x26e0ac | 6 | funny. |
| 0x26e0b3 | 47 | It's a little too embarrassing to admit I was\n |
| 0x26e0e3 | 26 | trying to cheer Nekone up. |
| 0x26e0fe | 48 | I guess the fact that I mistook you for Oshtor\n |
| 0x26e12f | 45 | means you've developed a dignified air, love. |
| 0x26e15d | 45 | Oh, you think so too? I don't want to brag,\n |
| 0x26e18b | 45 | but I've been thinking the same thing lately! |
| 0x26e1b9 | 42 | 'Course, flattery isn't going to get you\n |
| 0x26e1e4 | 17 | anything from me. |
| 0x26e1f6 | 31 | Hee hee, you're too sly for me. |
| 0x26e216 | 41 | ...There are no similarities whatsoever\n |
| 0x26e240 | 12 | between you. |
| 0x26e24d | 33 | Nekone mutters softly to herself. |
| 0x26e26f | 45 | There is no way my dear brother is anything\n |
| 0x26e29d | 9 | like you. |
| 0x26e2a7 | 45 | Well, of course. Oshtor is Oshtor, and he's\n |
| 0x26e2d5 | 34 | just... himself. Aren't you, love? |
| 0x26e2f8 | 6 | Hmm... |
| 0x26e2ff | 34 | Oh, were you two on your way back? |
| 0x26e322 | 48 | Atuy prods Nekone's pouting cheeks as she asks\n |
| 0x26e353 | 13 | her question. |
| 0x26e361 | 43 | I suggested we stop by some vendors as we\n |
| 0x26e38d | 24 | head back. I'm starving. |
| 0x26e3a6 | 46 | Oooh, sounds like a plan. I'll come with, if\n |
| 0x26e3d5 | 29 | you've got room for one more. |
| 0x26e3f3 | 27 | ...You two can go on, then. |
| 0x26e40f | 43 | Oh c'mon, don't be like that. Oshtor'd be\n |
| 0x26e43b | 42 | pissed at me if I told him you went back\n |
| 0x26e466 | 6 | alone. |
| 0x26e46d | 47 | I kneel down a bit, getting to eye level with\n |
| 0x26e49d | 50 | And besides, Oshtor asked me in the first place.\n |
| 0x26e4d0 | 46 | He wanted me to take you somewhere nice first. |
| 0x26e4ff | 23 | Dear brother said that? |
| 0x26e517 | 42 | Why don't you ask Oshtor about it later,\n |
| 0x26e542 | 23 | if you think I'm lying? |
| 0x26e55a | 42 | I'm lying. Obviously. But Nekone needs a\n |
| 0x26e585 | 46 | breather, and I'm sure Oshtor will back me up. |
| 0x26e5b4 | 47 | But if we don't hurry back, dear brother will\n |
| 0x26e5e4 | 4 | be-- |
| 0x26e5e9 | 48 | It was your "dear brother" who wanted this for\n |
| 0x26e61a | 4 | you. |
| 0x26e61f | 15 | Dear brother... |
| 0x26e62f | 47 | Nekone's mouth curves up in an awkward smile.\n |
| 0x26e65f | 48 | It's pretty clear she's trying to stifle a grin. |
| 0x26e690 | 45 | Haku's right. C'mon, Neko, let's all have a\n |
| 0x26e6be | 17 | nice evening out! |
| 0x26e6d0 | 31 | Nekone finally nods, giving in. |
| 0x26e6f0 | 45 | You have to eat lots, Neko. It's so you can\n |
| 0x26e71e | 12 | grow bigger. |
| 0x26e72b | 6 | Um...? |
| 0x26e732 | 11 | What is it? |
| 0x26e73e | 35 | You are... weighing my head down.\n |
| 0x26e762 | 38 | And why are you poking at my cheek...? |
| 0x26e789 | 43 | Atuy hugs Nekone from the back, her bosom\n |
| 0x26e7b5 | 43 | resting on Nekone's head, while she keeps\n |
| 0x26e7e1 | 11 | poking her. |
| 0x26e7ed | 19 | Do you not like it? |
| 0x26e801 | 39 | Well... I would not specifically say... |
| 0x26e829 | 39 | Aww, Neko! You're so cute when you're\n |
| 0x26e851 | 12 | embarrassed. |
| 0x26e85e | 21 | I am not embarrassed. |
| 0x26e874 | 8 | Hee hee! |
| 0x26e87d | 45 | Come on, Haku. If we are going to get food,\n |
| 0x26e8ab | 16 | we should hurry. |
| 0x26e8bc | 46 | She's right. And you're paying, right, love?\n |
| 0x26e8eb | 39 | I can order however much I want, right? |
| 0x26e913 | 44 | What!? When did I say I'd pay for your food? |
| 0x26e940 | 48 | Really? I would've expected Oshtor to give you\n |
| 0x26e971 | 48 | a little money if he's the one who told you to\n |
| 0x26e9a2 | 6 | do it. |
| 0x26e9a9 | 22 | Er... Well, you see... |
| 0x26e9c0 | 45 | That was just a lie to get Nekone to agree!\n |
| 0x26e9ee | 25 | C'mon, can't you tell...? |
| 0x26ea08 | 14 | Or am I wrong? |
| 0x26ea17 | 21 | N-No... you're not... |
| 0x26ea2d | 47 | Kuon manipulating me with devious forethought\n |
| 0x26ea5d | 45 | is one thing, but Atuy doing it obliviously\n |
| 0x26ea8b | 13 | is another... |
| 0x26ea99 | 44 | Dammit, my wallet gets lighter by the day... |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_08.json` com a forma:
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
