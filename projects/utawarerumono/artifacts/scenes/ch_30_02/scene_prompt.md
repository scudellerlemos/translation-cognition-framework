# Cena ch_30_02 — pacote de traducao (153 linhas)

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
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Highness | Titulo | Alteza | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
| Woshis | Personagem | Woshis | manter_original | major |
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
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Wh-What is the meaning of this!?\n` -> `Q-Que significado tem isso!?\n` (Nobre, 19_05)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `What do you mean?` -> `O que você quer dizer?` (Haku, 13_01)
- `that--` -> `isso--` (Ougi, 17_04)
- `this!?` -> `isso!?` (Haku, 19_08)
- `Well...` -> `Bom...` (Haku, 12_03)
- `orders.` -> `ordens.` (Raiko, 20_17)
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
| 0x2c8cca | 32 | Wh-What is the meaning of this!? |
| 0x2c8ceb | 44 | Spittle flies from Dekopompo's mouth as he\n |
| 0x2c8d18 | 6 | rages. |
| 0x2c8d1f | 10 | This is... |
| 0x2c8d2a | 44 | Raiko, much calmer than his fellow Pillar,\n |
| 0x2c8d57 | 46 | surveys his surroundings with a furrowed brow. |
| 0x2c8d86 | 47 | Their combined forces beat a hasty retreat to\n |
| 0x2c8db6 | 43 | the capital upon the news of the Mikado's\n |
| 0x2c8de2 | 8 | death... |
| 0x2c8deb | 40 | I DEMAND to know what's going on here!\n |
| 0x2c8e14 | 42 | Our liege is DEAD, and we're barred from\n |
| 0x2c8e3f | 19 | entering the city!? |
| 0x2c8e57 | 48 | I'll have none of this! Where are the guards!?\n |
| 0x2c8e88 | 43 | I am Dekopompo of the Eight bloody Pillar\n |
| 0x2c8eb4 | 9 | GENERALS! |
| 0x2c8ebe | 44 | Dekopompo barks at the guard post atop the\n |
| 0x2c8eeb | 32 | high gates, but no answer comes. |
| 0x2c8f0c | 46 | ANSWER! I'll break these wretched gates down\n |
| 0x2c8f3b | 20 | MYSELF if I have to! |
| 0x2c8f50 | 44 | Are you going to let him carry on like that? |
| 0x2c8f7d | 17 | What do you mean? |
| 0x2c8f8f | 47 | At this rate, he could well follow through on\n |
| 0x2c8fbf | 46 | his threats and order an assault on the gates. |
| 0x2c8fee | 44 | Hah, as if that would accomplish anything.\n |
| 0x2c901b | 45 | Even as one, our armies would not budge the\n |
| 0x2c9049 | 14 | imperial gate. |
| 0x2c9058 | 47 | And such an order would be grounds for treason. |
| 0x2c9088 | 49 | Truth be told, it would do my heart good to see\n |
| 0x2c90ba | 38 | this odious cur removed from my sight. |
| 0x2c90e1 | 6 | That-- |
| 0x2c90e8 | 46 | RAIKO! How can you be so calm at a time like\n |
| 0x2c9117 | 6 | this!? |
| 0x2c911e | 49 | Dekopompo turns his fury on Raiko, spitting and\n |
| 0x2c9150 | 43 | flailing, but Raiko continues ignoring him. |
| 0x2c917c | 29 | Any news from the Tiriryarai? |
| 0x2c919a | 7 | Well... |
| 0x2c91a4 | 29 | Hmph. Finally, some movement. |
| 0x2c91c2 | 6 | NYEH!? |
| 0x2c91c9 | 49 | Beside the gates, a much smaller passage opens,\n |
| 0x2c91fb | 22 | and through it steps-- |
| 0x2c9212 | 10 | Woshis...? |
| 0x2c921d | 39 | Woshis. What exactly is happening here? |
| 0x2c9245 | 46 | As the two generals look upon him, demanding\n |
| 0x2c9274 | 47 | answers, Woshis speaks with a grave expression. |
| 0x2c92a4 | 50 | My apologies for keeping the two of you waiting.\n |
| 0x2c92d7 | 45 | Our liege's death has thrown the court into\n |
| 0x2c9305 | 6 | chaos. |
| 0x2c930c | 26 | I don't want your excuses! |
| 0x2c9327 | 47 | Dekopompo barks sharply at Woshis, his entire\n |
| 0x2c9357 | 44 | head reddening to the point of threatening\n |
| 0x2c9384 | 9 | to steam. |
| 0x2c938e | 45 | What is the meaning of this!? The Mikado is\n |
| 0x2c93bc | 49 | DEAD. It is our duty as PILLARS to stand firmly\n |
| 0x2c93ee | 11 | inside th-- |
| 0x2c93fa | 47 | Woshis quietly cuts Dekopompo off with a curt\n |
| 0x2c942a | 18 | shake of his head. |
| 0x2c943d | 48 | I'm afraid I cannot permit that. The gates are\n |
| 0x2c946e | 45 | to remain closed so none may enter--nor exit. |
| 0x2c949c | 44 | It is the command of Her Highness that the\n |
| 0x2c94c9 | 40 | capital mourns in silence and isolation. |
| 0x2c94f2 | 6 | Nyeh!? |
| 0x2c94f9 | 49 | This is preposterous! What purpose do the Eight\n |
| 0x2c952b | 46 | Pillars serve if we cannot enter OUR OWN CITY? |
| 0x2c955a | 49 | I advise you watch your tongue, Lord Dekopompo.\n |
| 0x2c958c | 44 | This order comes directly from the princess. |
| 0x2c95b9 | 48 | Or perhaps you wish to draw your blade against\n |
| 0x2c95ea | 44 | her and seize power while the empire is in\n |
| 0x2c9617 | 9 | disarray? |
| 0x2c9621 | 41 | Gah, I-I would never--That's a BASELESS\n |
| 0x2c964b | 18 | accusation, you... |
| 0x2c965e | 48 | Dekopompo immediately becomes flustered at the\n |
| 0x2c968f | 23 | insinuation of treason. |
| 0x2c96a7 | 47 | Her Highness is the blood of the Mikado, born\n |
| 0x2c96d7 | 41 | and bred to rule. Her word is absolute.\n |
| 0x2c9701 | 10 | However... |
| 0x2c970c | 48 | Her Highness is still naught but a young girl.\n |
| 0x2c973d | 43 | I highly doubt she's in any state to give\n |
| 0x2c9769 | 7 | orders. |
| 0x2c9771 | 51 | Therefore, I can only assume she's been advised--\n |
| 0x2c97a5 | 42 | or worse, coerced into making this decree. |
| 0x2c97d0 | 38 | Raiko steps forward, putting himself\n |
| 0x2c97f7 | 25 | face-to-face with Woshis. |
| 0x2c9811 | 38 | Lord Woshis, thank you for conveying\n |
| 0x2c9838 | 25 | Her Highness' will to me. |
| 0x2c9852 | 47 | However, we are generals sworn to protect our\n |
| 0x2c9882 | 48 | princess. Will you not let us pass, if not our\n |
| 0x2c98b3 | 7 | armies? |
| 0x2c98bb | 48 | I should like to see her in person and express\n |
| 0x2c98ec | 15 | my condolences. |
| 0x2c98fc | 30 | At Raiko's words, Woshis nods. |
| 0x2c991b | 30 | I understand this, Lord Raiko. |
| 0x2c993a | 47 | However, I have not the authority to overturn\n |
| 0x2c996a | 42 | a direct order from the imperial princess. |
| 0x2c9995 | 51 | I shall have to express your wish to Her Highness\n |
| 0x2c99c9 | 43 | and return to you. Please, I ask for your\n |
| 0x2c99f5 | 9 | patience. |
| 0x2c99ff | 43 | Hyargh!? We have no time for such things!\n |
| 0x2c9a2b | 45 | I will ask Her Highness in person about this! |
| 0x2c9a59 | 44 | Dekopompo angrily storms toward the gates... |
| 0x2c9a86 | 46 | ...only for Woshis to efficiently and calmly\n |
| 0x2c9ab5 | 15 | block his path. |
| 0x2c9ac5 | 28 | I would advise against that. |
| 0x2c9ae2 | 8 | HNENGH!? |
| 0x2c9aeb | 25 | Have you not eyes to see? |
| 0x2c9b08 | 45 | Dekopompo follows Woshis' gaze up the wall,\n |
| 0x2c9b36 | 13 | then freezes. |
| 0x2c9b44 | 47 | Raiko also looks up at the parapet, clenching\n |
| 0x2c9b74 | 18 | his teeth tensely. |
| 0x2c9b87 | 22 | So, this is HIS doing? |
| 0x2c9b9e | 6 | Vurai. |
| 0x2c9ba5 | 50 | Atop the walls, soldiers stand at the ready with\n |
| 0x2c9bd8 | 44 | arrows nocked and bowstrings drawn, aiming\n |
| 0x2c9c05 | 9 | downward. |
| 0x2c9c0f | 48 | That armor... That's Vurai's livery. What sort\n |
| 0x2c9c40 | 48 | of bluff is he playing at, threatening us so...? |
| 0x2c9c71 | 41 | No. Calculated posturing is beyond him.\n |
| 0x2c9c9b | 47 | He must truly believe he can stand against us\n |
| 0x2c9ccb | 17 | all, even Woshis. |
| 0x2c9cdd | 36 | Raiko quickly glances toward Woshis. |
| 0x2c9d02 | 49 | If you disobey an imperial command, I will have\n |
| 0x2c9d34 | 47 | no choice but to find you both guilty of high\n |
| 0x2c9d64 | 8 | treason. |
| 0x2c9d6d | 24 | So, how you will choose? |
| 0x2c9d86 | 9 | Y-You...! |
| 0x2c9d90 | 47 | I see. He earned the princess' trust while we\n |
| 0x2c9dc0 | 46 | all played at war, and now he stages a coup... |
| 0x2c9def | 43 | When those gates open, the dust will have\n |
| 0x2c9e1b | 43 | settled. A man unhappy in peacetime WOULD\n |
| 0x2c9e47 | 14 | contrive this. |
| 0x2c9e56 | 48 | Who knows? I certainly can't speak to any such\n |
| 0x2c9e87 | 5 | plot. |
| 0x2c9e8d | 47 | But I will say this: absolute rule--even by a\n |
| 0x2c9ebd | 48 | god--stifles. A vessel under pressure is bound\n |
| 0x2c9eee | 9 | to burst. |
| 0x2c9ef8 | 49 | Within the next few years, perhaps even months,\n |
| 0x2c9f2a | 47 | this empire will fracture. Yamato is doombound. |
| 0x2c9f5a | 46 | And you think Vurai is the man to place your\n |
| 0x2c9f89 | 26 | faith in, to prevent that? |
| 0x2c9fa4 | 47 | Even an overflowing vessel is preferable to a\n |
| 0x2c9fd4 | 14 | shattered one. |
| 0x2c9fe3 | 48 | So, you've accepted a passive role and decided\n |
| 0x2ca014 | 22 | to wait out the storm. |
| 0x2ca02b | 50 | I wish merely to spare my countrymen the horrors\n |
| 0x2ca05e | 43 | of war. I advise you pursue a similar path. |
| 0x2ca08a | 38 | The transition should not take long.\n |
| 0x2ca0b1 | 21 | Of this I am certain. |
| 0x2ca0c7 | 46 | Woshis bows deeply, then retreats behind the\n |
| 0x2ca0f6 | 44 | gates via the small passage he emerged from. |
| 0x2ca123 | 35 | Vurai... You've surely done it now. |
| 0x2ca147 | 48 | And here I thought to accelerate my own plans.\n |
| 0x2ca178 | 30 | You've beaten me to the punch. |
| 0x2ca197 | 48 | But do not think that I, Raiko, will take this\n |
| 0x2ca1c8 | 13 | lying down... |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_02.json` com a forma:
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
