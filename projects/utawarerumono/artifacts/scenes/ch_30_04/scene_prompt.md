# Cena ch_30_04 — pacote de traducao (816 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Earth | Local | Terra | traduzir | major |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Karulau | Personagem | Karulau | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Touka | Personagem | Touka | manter_original | moderate |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
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
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
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
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `for nothing.` -> `de graça.` (Kuon, 19_07)
- `again...` -> `de novo...` (Homem, 13_09)
- `right now.` -> `agora.` (Kuon, 22_05)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Yes, dear sister.` -> `Sim, querida irmã.` (Nekone, 15_05)
- `*Whistle*` -> `*Apito*` (Haku, 20_03)
- `this.` -> `essa.` (Moznu, 13_05)
- `No...` -> `Não...` (Touka, 17_01)
- `chaos.` -> `caos.` (Raiko, 30_02)
- `Mikado.` -> `Mikado.` (Rulutieh, 14_02)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `What?` -> `Que?` (Haku, 12_02)
- `brother?` -> `irmão?` (Garota, 22_08)
- `Impossible...` -> `Impossível...` (Kuon, 22_05)
- `Mikado!` -> `Mikado!` (Haku, 19_05)
- `Nekone...` -> `Nekone...` (Maroro, 17_03)
- `OK.` -> `OK.` (Haku, 15_04)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `through.` -> `através.` (Honoka, 22_08)
- `Yeah...` -> `É...` (Kuon, 11_02)
- `Townsfolk` -> `Moradores` (Sistema, 16_01)
- `danger...` -> `perigo...` (Haku, 12_12)
- `like this?` -> `assim?` (Haku, 16_01)
- `Woohoo!` -> `Uhuu!` (Kuon, 14_03)
- `I think.` -> `acho.` (Kuon, 12_11)
- `'Course I am.` -> `Claro que sim.` (Nosuri, 19_04)
- `her.` -> `a ela.` (Kuon, 11_02)
- `What do you think?` -> `O que você acha?` (Garota, 18_01)
- `to you.` -> `com você.` (Ukon, 13_02)
- `...Uh?` -> `...Hã?` (Haku, 15_05)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `security.` -> `segurança.` (Oshtor, 17_03)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `like?` -> `gosto?` (Rulutieh, 17_01)
- `What do you mean?` -> `O que você quer dizer?` (Haku, 13_01)
- `Yes...` -> `Sim...` (Rulutieh, 14_10)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `nothing more.` -> `nada mais.` (Kurou, 23_13)
- `thinking.` -> `pensando.` (Ukon, 12_17)
- `Lord Oshtor.` -> `Lorde Oshtor.` (Ukon, 15_05)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `...Right. ` -> `...Tá.` (Haku, 14_10)
- `question.` -> `meio injusta.` (Kuon, 11_02)
- `Dear brother...` -> `Querido irmão...` (Nekone, 14_04)
- `retainers.` -> `servidores.` (Haku, 18_01)
- `Nosuri?` -> `Nosuri?` (Nosuri, 18_01)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `a trap.` -> `uma cilada.` (Ougi, 19_02)
- `before.` -> `antes.` (Haku, 15_02)
- `work.` -> `trabalho.` (Protagonista, 16_01)
- `but--` -> `mas--` (Oshtor, 19_05)
- `then.` -> `então.` (Kuon, 13_01)
- `is...` -> `é...` (Narração/Voz, 17_01)
- `do.` -> `faria.` (Haku, 15_06)
- `maybe?` -> `talvez?` (Ukon, 15_05)
- `anyway.` -> `de agora.` (Ougi, 13_08)
- `*FWUMP*` -> `*BAQUE*` (sistema, 13_02)
- `strong.` -> `forte.` (Estalajadeira, 17_01)
- `that--` -> `isso--` (Ougi, 17_04)
- `this one.` -> `este.` (Mikazuchi, 23_01)
- `sister.` -> `irmã.` (Ukon, 14_04)
- `any more.` -> `assim.` (Ukon, 14_04)
- `late.` -> `tarde.` (Haku, 22_04)
- `Speak.` -> `Fale.` (Mikazuchi, 18_01)
- `way.` -> `jeito.` (Atuy, 18_01)
- `world.` -> `mundo.` (Haku, 16_01)
- `I...` -> `Eu...` (Nekone, 14_04)
- `behind.` -> `para trás.` (Garota, 13_05)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `That will not be necessary.` -> `Isso não será necessário.` (Oshtor/Ukon, 20_01)
- `*Jiggle, jiggle*...` -> `*Tremidinha, tremidinha*...` (Haku, 18_01)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `Lord Haku.` -> `Senhor Haku.` (Oshtor, 23_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `...I will.` -> `...Vou.` (Haku, 17_01)
- `...OK.` -> `...Beleza.` (Yuuri, 16_03)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `without them.` -> `sem elas.` (Ukon, 19_08)
- `But...` -> `mas...` (Kuon, 11_01)
- `I see.` -> `Sim.` (Haku, 11_02)
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
- Rulutieh: `Oh, pardon me.` -> `Ah, com licença.`
- Rulutieh: `I'm... sorry about, um...` -> `Eu... desculpe, é que...`
- Rulutieh: `That's a relief... Come on, Cocopo. We'll just be\n` -> `Ainda bem... Vamos, Cocopo. Só estamos\n`
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
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
| 0x2cc7f2 | 47 | No sooner than the ship arrives in port do we\n |
| 0x2cc822 | 33 | set out for the imperial capital. |
| 0x2cc844 | 46 | Our carriage barrels down the road, stopping\n |
| 0x2cc873 | 12 | for nothing. |
| 0x2cc880 | 49 | The atmosphere isn't nearly as cheerful as when\n |
| 0x2cc8b2 | 42 | we set out. Far fewer words are exchanged. |
| 0x2cc8dd | 30 | Well, we've made our way back. |
| 0x2cc8fc | 38 | It feels like so long since we left... |
| 0x2cc923 | 30 | Indeed. Finally, we're home... |
| 0x2cc942 | 48 | Oh, I'm so hungry. I can't wait to eat skewers\n |
| 0x2cc973 | 8 | again... |
| 0x2cc980 | 47 | Rulutieh's expression only grows gloomier the\n |
| 0x2cc9b0 | 26 | closer we get to the city. |
| 0x2cc9cb | 45 | Kuon tries her best to cheer her up, but it\n |
| 0x2cc9f9 | 47 | doesn't seem to be having terribly much effect. |
| 0x2cca29 | 49 | Kuon glances back at me, hoping I might be able\n |
| 0x2cca5b | 23 | to help somehow, but... |
| 0x2cca73 | 49 | Sorry. I've got too much on my mind to sort out\n |
| 0x2ccaa5 | 10 | right now. |
| 0x2ccab0 | 22 | Hm? Stop the carriage. |
| 0x2ccac7 | 44 | Aren't those Raiko and Dekopompo's soldiers? |
| 0x2ccaf4 | 38 | They left a lot earlier than we did.\n |
| 0x2ccb1b | 36 | Why are they still outside the city? |
| 0x2ccb40 | 41 | Any particular reason the gate would be\n |
| 0x2ccb6a | 10 | closed...? |
| 0x2ccb75 | 4 | Huh? |
| 0x2ccb7a | 42 | It would appear they've been barred from\n |
| 0x2ccba5 | 15 | entering. Hm... |
| 0x2ccbb5 | 45 | The soldiers are being kept out? That seems\n |
| 0x2ccbe3 | 43 | strange... Just what is happening in there? |
| 0x2ccc0f | 26 | Nosuri, Ougi, do you mind? |
| 0x2ccc2a | 32 | Yes, it's worth investigating.\n |
| 0x2ccc4b | 14 | With me, Ougi. |
| 0x2ccc5a | 17 | Yes, dear sister. |
| 0x2ccc6c | 9 | *Whistle* |
| 0x2ccc76 | 42 | They just... ran up the walls. Impressive. |
| 0x2ccca1 | 18 | You seem cautious. |
| 0x2cccb4 | 47 | Yeah, well. I've just got a bad feeling about\n |
| 0x2ccce4 | 5 | this. |
| 0x2cccea | 26 | ...That's the only reason? |
| 0x2ccd05 | 44 | You're a bad liar, Haku. I don't know what\n |
| 0x2ccd32 | 45 | you're hiding, but it's obvious something's\n |
| 0x2ccd60 | 13 | on your mind. |
| 0x2ccd6e | 7 | Uh huh? |
| 0x2ccd76 | 44 | I... would like it if you'd explain it all\n |
| 0x2ccda3 | 19 | to me...eventually. |
| 0x2ccdb7 | 27 | I will. Someday. I promise. |
| 0x2ccdd3 | 27 | All right. I'll be waiting. |
| 0x2ccdef | 49 | Thanks, Kuon. I promise I'll explain everything\n |
| 0x2cce21 | 19 | to you, some day... |
| 0x2cce35 | 22 | Sorry we took so long. |
| 0x2cce4c | 47 | Worst news first, I suppose... The Mikado has\n |
| 0x2cce7c | 17 | indeed passed on. |
| 0x2cce8e | 5 | Nngh. |
| 0x2cce94 | 5 | No... |
| 0x2cce9a | 50 | The city is in mourning, and the Pillars' armies\n |
| 0x2ccecd | 45 | are being barred from entry for the duration. |
| 0x2ccefb | 43 | Now, I'd like to preface the following by\n |
| 0x2ccf27 | 45 | saying it's merely conjecture substantiated\n |
| 0x2ccf55 | 10 | by rumor-- |
| 0x2ccf60 | 40 | My sources can only give me unreliable\n |
| 0x2ccf89 | 43 | information, but it seems the court is in\n |
| 0x2ccfb5 | 6 | chaos. |
| 0x2ccfbc | 43 | Stop talking in circles and give it to us\n |
| 0x2ccfe8 | 9 | straight. |
| 0x2ccff2 | 32 | Very well. In small words, then. |
| 0x2cd013 | 45 | The popular rumor is that Oshtor killed the\n |
| 0x2cd041 | 7 | Mikado. |
| 0x2cd049 | 7 | ...Huh? |
| 0x2cd051 | 5 | What? |
| 0x2cd057 | 46 | Oshtor... assassinated the Mikado? Killed my\n |
| 0x2cd086 | 8 | brother? |
| 0x2cd08f | 13 | Impossible... |
| 0x2cd09d | 19 | Utterly ridiculous! |
| 0x2cd0b1 | 45 | My dear brother... even were the heavens to\n |
| 0x2cd0df | 47 | crumble upon the earth, he'd NEVER betray the\n |
| 0x2cd10f | 7 | Mikado! |
| 0x2cd117 | 44 | That's not all. They also claim he made an\n |
| 0x2cd144 | 31 | attempt on the princess's life. |
| 0x2cd164 | 48 | Mercifully, Her Highness survived, but lies in\n |
| 0x2cd195 | 19 | critical condition. |
| 0x2cd1a9 | 37 | There must be some kind of mistake!\n |
| 0x2cd1cf | 16 | He would NEVER-- |
| 0x2cd1e0 | 9 | Nekone... |
| 0x2cd1ea | 47 | H-He would... He'd never d-do such a horrible\n |
| 0x2cd21a | 8 | thing... |
| 0x2cd223 | 47 | It's all right. Everyone here trusts in Oshtor. |
| 0x2cd253 | 21 | Please don't cry. OK? |
| 0x2cd269 | 10 | Sniff...\n |
| 0x2cd274 | 3 | OK. |
| 0x2cd278 | 30 | So, where is Oshtor right now? |
| 0x2cd297 | 35 | Oh, right. He's... been arrested.\n |
| 0x2cd2bb | 31 | They're holding him in custody. |
| 0x2cd2db | 43 | There was another name, as well. The high\n |
| 0x2cd307 | 45 | priestess, Lady Honoka, is accused of being\n |
| 0x2cd335 | 14 | a conspirator. |
| 0x2cd344 | 47 | She was the one to actually convey the poison\n |
| 0x2cd374 | 48 | to the Mikado via his food... or so the rumors\n |
| 0x2cd3a5 | 6 | state. |
| 0x2cd3ac | 6 | What!? |
| 0x2cd3b3 | 41 | Honoka killed my brother? No, that's...\n |
| 0x2cd3dd | 23 | That's just ridiculous. |
| 0x2cd3f5 | 47 | Someone is definitely trying to frame her and\n |
| 0x2cd425 | 44 | Oshtor. This whole thing reeks of foul play. |
| 0x2cd452 | 46 | Haku, what exactly are you thinking right now? |
| 0x2cd481 | 43 | There aren't many who know we're Oshtor's\n |
| 0x2cd4ad | 9 | agents... |
| 0x2cd4b7 | 45 | But that doesn't mean there's no one in the\n |
| 0x2cd4e5 | 15 | city who knows. |
| 0x2cd4f5 | 49 | Worst-case scenario, I imagine we're all wanted\n |
| 0x2cd527 | 10 | criminals. |
| 0x2cd532 | 45 | Yeah. We can't afford to walk around in the\n |
| 0x2cd560 | 46 | open. We should take care to hide our faces,\n |
| 0x2cd58f | 10 | if we can. |
| 0x2cd59a | 47 | We do our best to disguise ourselves with the\n |
| 0x2cd5ca | 25 | supplies we have on hand. |
| 0x2cd5e4 | 43 | That being said, "the supplies we have on\n |
| 0x2cd610 | 48 | hand" are scarves to hide our faces. It's more\n |
| 0x2cd641 | 13 | of a costume. |
| 0x2cd64f | 31 | Better than nothing, I suppose. |
| 0x2cd66f | 49 | The primary gates have been sealed off, but the\n |
| 0x2cd6a1 | 47 | western gate remains open to allow passage to\n |
| 0x2cd6d1 | 10 | merchants. |
| 0x2cd6dc | 48 | I submit we pose as merchants in order to pass\n |
| 0x2cd70d | 8 | through. |
| 0x2cd716 | 7 | Yeah... |
| 0x2cd71e | 43 | ...Phew. Looks like we managed it, somehow. |
| 0x2cd74a | 46 | They let us through a lot more easily than I\n |
| 0x2cd779 | 48 | thought. There wasn't even really an inspection. |
| 0x2cd7aa | 48 | Yeah, I noticed that, too. Maybe we're being a\n |
| 0x2cd7db | 48 | little too--No, we shouldn't let our guard down. |
| 0x2cd80c | 50 | Considering what might lie in store for us, it's\n |
| 0x2cd83f | 43 | better to be cautious than sloppy, I think. |
| 0x2cd86b | 32 | Hey, aren't any of you hungry?\n |
| 0x2cd88c | 30 | Where'd all the vendors go...? |
| 0x2cd8ab | 45 | Man, she's right. The streets are dead. You\n |
| 0x2cd8d9 | 46 | weren't kidding about the capital going into\n |
| 0x2cd908 | 9 | mourning. |
| 0x2cd912 | 49 | Is that the reason? I've never seen the city so\n |
| 0x2cd944 | 8 | quiet... |
| 0x2cd94d | 47 | There are people on the streets, but they all\n |
| 0x2cd97d | 47 | walk in silence, keeping quietly to themselves. |
| 0x2cd9ad | 39 | I... never realized how enormous this\n |
| 0x2cd9d5 | 27 | thoroughfare was, before... |
| 0x2cd9f1 | 9 | Townsfolk |
| 0x2cd9fb | 46 | How could this be...? Not only has our liege\n |
| 0x2cda2a | 46 | left us, but the imperial princess in mortal\n |
| 0x2cda59 | 9 | danger... |
| 0x2cda63 | 27 | What will become of Yamato? |
| 0x2cda7f | 45 | The mood's tense. I guess I can't blame them. |
| 0x2cdaad | 49 | How am I supposed to do any trade with the city\n |
| 0x2cdadf | 10 | like this? |
| 0x2cdaea | 32 | One bad thing after another...\n |
| 0x2cdb0b | 29 | It's like some kind of curse. |
| 0x2cdb29 | 41 | I hope this is the end of the bad news... |
| 0x2cdb53 | 43 | Eavesdropping on the conversations of the\n |
| 0x2cdb7f | 47 | cityfolk, everyone seems overwhelmingly gloomy. |
| 0x2cdbaf | 18 | What do we do now? |
| 0x2cdbc2 | 48 | We've no reason to tarry here. We should avoid\n |
| 0x2cdbf3 | 45 | attracting attention in the street like this. |
| 0x2cdc21 | 49 | You're right. Let's make for the Hakurokaku for\n |
| 0x2cdc53 | 15 | the time being. |
| 0x2cdc63 | 47 | Taking care not to draw too much attention to\n |
| 0x2cdc93 | 42 | ourselves, we head for the Hakurokaku Inn. |
| 0x2d22e8 | 7 | Woohoo! |
| 0x2d22f0 | 45 | Atuy immediately divebombs the plush couch,\n |
| 0x2d231e | 26 | sinking into the cushions. |
| 0x2d2339 | 40 | Ahh. It's such a relief to be back here. |
| 0x2d2362 | 22 | I'll go brew some tea. |
| 0x2d2379 | 50 | Oh, Rulie! Could you bring back something to eat\n |
| 0x2d23ac | 19 | while you're at it? |
| 0x2d23c0 | 45 | Of course. I'll fix up something we can all\n |
| 0x2d23ee | 17 | share together... |
| 0x2d2400 | 21 | Hee. That's my Rulie. |
| 0x2d2416 | 40 | Phew. Finally, we can take a breather... |
| 0x2d243f | 48 | This place never changes. It's nice to be back\n |
| 0x2d2470 | 11 | here again. |
| 0x2d247c | 40 | Kuon smiles as Atuy switches into full\n |
| 0x2d24a5 | 12 | Lounge Mode. |
| 0x2d24b2 | 46 | How can you relax? We can't waste any time...! |
| 0x2d24e1 | 49 | We can spend at least a little while like this,\n |
| 0x2d2513 | 8 | I think. |
| 0x2d251c | 18 | Yeah, she's right. |
| 0x2d252f | 48 | Thanks to Atuy's enthusiasm, the heavy, somber\n |
| 0x2d2560 | 40 | air is starting to dissipate somewhat... |
| 0x2d2589 | 49 | Before anyone can speak, tiny footfalls thunder\n |
| 0x2d25bb | 45 | down the hall outside, and the door crashes\n |
| 0x2d25e9 | 5 | open. |
| 0x2d25ef | 18 | Welcome back, Dad! |
| 0x2d2602 | 49 | Hey, Shinonon. Were you a good girl while I was\n |
| 0x2d2634 | 5 | gone? |
| 0x2d263a | 36 | 'Course I was good! I'm ALWAYS good. |
| 0x2d265f | 38 | Shinonon, you mustn't run like that!\n |
| 0x2d2686 | 30 | You'll trip and hurt yourself. |
| 0x2d26a5 | 47 | Oh, hey. We just got back. Thanks for looking\n |
| 0x2d26d5 | 32 | after Shinonon while I was gone. |
| 0x2d26f6 | 41 | The woman who'd brought Shinonon smiles\n |
| 0x2d2720 | 27 | bashfully at being thanked. |
| 0x2d273c | 42 | Welcome back. Truly, it was no trouble--\n |
| 0x2d2767 | 32 | she's a very well-behaved child. |
| 0x2d2788 | 47 | She even helped out with chores around the inn. |
| 0x2d27b8 | 14 | Yep! I helped. |
| 0x2d27c7 | 45 | That's my Shinonon. You're gonna be quite a\n |
| 0x2d27f5 | 28 | woman when you grow up, kid. |
| 0x2d2812 | 13 | 'Course I am. |
| 0x2d2820 | 47 | Jachdwalt runs his fingers through Shinonon's\n |
| 0x2d2850 | 25 | hair fondly, ruffling it. |
| 0x2d286a | 19 | Welcome back, boss. |
| 0x2d287e | 48 | Thanks for holding down the fort while we were\n |
| 0x2d28af | 46 | gone. You didn't get lonely without us, right? |
| 0x2d28de | 39 | No, I didn't! I wasn't lonely at all.\n |
| 0x2d2906 | 22 | Not even a little bit. |
| 0x2d291d | 33 | I... guess I'll leave it at that. |
| 0x2d293f | 45 | Here, I got you something--a little souvenir. |
| 0x2d296d | 46 | I hand Shinonon a doll--something I found in\n |
| 0x2d299c | 43 | Tuskur, a mononofu with posable limbs and\n |
| 0x2d29c8 | 7 | joints. |
| 0x2d29d0 | 50 | I'd never seen anything quite like it in Yamato,\n |
| 0x2d2a03 | 48 | so I was sure it would make a good present for\n |
| 0x2d2a34 | 4 | her. |
| 0x2d2a39 | 13 | O-Oh, that... |
| 0x2d2a47 | 24 | Wow, this guy's so cool! |
| 0x2d2a60 | 50 | Awright, buddy, your name's gonna be Goodbadguy.\n |
| 0x2d2a93 | 29 | Nice to meet you, Goodbadguy! |
| 0x2d2ab1 | 16 | Why the hell...? |
| 0x2d2ac2 | 20 | And this is from me. |
| 0x2d2ad7 | 47 | Kuon produces a pristine seashell, glittering\n |
| 0x2d2b07 | 29 | in all colors of the rainbow. |
| 0x2d2b25 | 24 | Whoooaa! It's so pretty! |
| 0x2d2b3e | 37 | I found it on the beach over there.\n |
| 0x2d2b64 | 28 | I thought you might like it. |
| 0x2d2b81 | 18 | What do you think? |
| 0x2d2b94 | 17 | I really like it! |
| 0x2d2ba6 | 45 | Dad, look how cool this is! It's all sparkly! |
| 0x2d2bd4 | 31 | Glad you're happy with it, kid. |
| 0x2d2bf4 | 47 | ...And I've procured a book for you. It's not\n |
| 0x2d2c24 | 47 | a challenging read, but someone could read it\n |
| 0x2d2c54 | 7 | to you. |
| 0x2d2c5c | 47 | Ooh! Will you read it to me later, little lady? |
| 0x2d2c90 | 28 | You're... not gonna read it? |
| 0x2d2cad | 33 | ...I suppose I will, if you like. |
| 0x2d2ccf | 36 | Dad, she said she's gonna read it!\n |
| 0x2d2cf4 | 31 | Little lady's gonna read to me! |
| 0x2d2d14 | 18 | Good for you, kid. |
| 0x2d2d27 | 6 | ...Uh? |
| 0x2d2d2e | 9 | Um... Uh. |
| 0x2d2d38 | 33 | Whatcha bring back for me, Kiwru? |
| 0x2d2d5a | 14 | Um!? Well, I-- |
| 0x2d2d69 | 26 | Did you... Did you forget? |
| 0x2d2d84 | 18 | H-Hahaha... Sorry. |
| 0x2d2d97 | 28 | You're so hopeless, Kiwru... |
| 0x2d2db4 | 7 | Urgh... |
| 0x2d2dbc | 45 | This is why no one has anything good to say\n |
| 0x2d2dea | 18 | about you, y'know. |
| 0x2d2dfd | 48 | Kiwru slumps to the ground and groans, burying\n |
| 0x2d2e2e | 21 | his face in his arms. |
| 0x2d2e44 | 45 | Man, I'm exhausted from all that traveling.\n |
| 0x2d2e72 | 31 | I wanna take a good, long rest. |
| 0x2d2e92 | 43 | I'm afraid that's a luxury we don't have.\n |
| 0x2d2ebe | 44 | The Hakurokaku may not remain a safe haven\n |
| 0x2d2eeb | 14 | for very long. |
| 0x2d2efa | 36 | So, Haku? What's our plan from here? |
| 0x2d2f1f | 34 | Everyone focuses their gaze on me. |
| 0x2d2f42 | 26 | Our plan from here, huh... |
| 0x2d2f5d | 42 | Regardless of what we do, we still don't\n |
| 0x2d2f88 | 34 | have a lot of crucial information. |
| 0x2d2fab | 43 | My brother, the princess, Oshtor, Honoka... |
| 0x2d2fd7 | 48 | There's just too many unknown factors at play,\n |
| 0x2d3008 | 5 | here. |
| 0x2d300e | 50 | We need to gather as much information as we can.\n |
| 0x2d3041 | 26 | And in order to do that... |
| 0x2d305c | 45 | Nosuri, I'm going to need you to infiltrate\n |
| 0x2d308a | 47 | the... No, no, that's too dangerous. Too much\n |
| 0x2d30ba | 9 | security. |
| 0x2d30c4 | 47 | I apologize for the interruption, but a guest\n |
| 0x2d30f4 | 42 | is asking after you. Shall I show them in? |
| 0x2d311f | 3 | Eh? |
| 0x2d3123 | 26 | Are they after us already? |
| 0x2d313e | 46 | Oh, dear. Have they figured out where we are?  |
| 0x2d316d | 46 | How big a group is it? And what do they look\n |
| 0x2d319c | 5 | like? |
| 0x2d31a2 | 42 | Ah, merely the one woman, it would seem.\n |
| 0x2d31cd | 24 | She appears to be alone. |
| 0x2d31e6 | 45 | I... She would appear to be a noble lady of\n |
| 0x2d3214 | 10 | some sort. |
| 0x2d321f | 32 | A lady of the court, alone...?\n |
| 0x2d3240 | 12 | Why would... |
| 0x2d324d | 44 | So it's not someone trying to hunt us down\n |
| 0x2d327a | 10 | after all? |
| 0x2d3285 | 15 | Lady-in-waiting |
| 0x2d3295 | 50 | Please forgive the intrusion. I am gravely sorry\n |
| 0x2d32c8 | 28 | to disturb you at this hour. |
| 0x2d32e5 | 46 | I... I am here on behalf of my mistress, the\n |
| 0x2d3314 | 41 | Lady Honoka, who bade me relay a message. |
| 0x2d333e | 22 | A message from Honoka? |
| 0x2d3355 | 36 | At that, the entire room goes stiff. |
| 0x2d337a | 48 | I have been acting as interim caretaker of the\n |
| 0x2d33ab | 36 | princess under Lady Honoka's orders. |
| 0x2d33d0 | 49 | I know you must harbor your suspicions, but the\n |
| 0x2d3402 | 37 | accusations against milady are false. |
| 0x2d3428 | 40 | Someone seeks to besmirch her good name. |
| 0x2d3451 | 17 | What do you mean? |
| 0x2d3463 | 45 | By now I'm sure you've heard that after the\n |
| 0x2d3491 | 46 | Mikado's death, someone tried to assassinate\n |
| 0x2d34c0 | 13 | the princess. |
| 0x2d34ce | 44 | Yeah, we've heard the rumors. Is there any\n |
| 0x2d34fb | 14 | truth to them? |
| 0x2d350a | 6 | Yes... |
| 0x2d3511 | 45 | Her Highness drank tea tainted with poison,\n |
| 0x2d353f | 23 | and... a-and collapsed. |
| 0x2d3557 | 33 | And what's her current condition? |
| 0x2d3579 | 47 | Mercifully, Her Highness survived the ordeal,\n |
| 0x2d35a9 | 40 | but... she's yet to regain any kind of\n |
| 0x2d35d2 | 14 | consciousness. |
| 0x2d35e1 | 9 | ...I see. |
| 0x2d35eb | 12 | Miss Anju... |
| 0x2d35f8 | 27 | Truth be told, this is...\n |
| 0x2d3614 | 21 | This is all my fault. |
| 0x2d362a | 4 | Huh? |
| 0x2d362f | 50 | I-I was... I was the one who served Her Highness\n |
| 0x2d3662 | 17 | the poisoned tea. |
| 0x2d3677 | 50 | I was told to take a cup of tea to the princess,\n |
| 0x2d36aa | 13 | nothing more. |
| 0x2d36b8 | 49 | I did as instructed, of course, but th-then the\n |
| 0x2d36ea | 49 | princess collapsed, and the palace plunged into\n |
| 0x2d371c | 6 | chaos. |
| 0x2d3723 | 43 | I... I let fear rule me, and fled without\n |
| 0x2d374f | 9 | thinking. |
| 0x2d3759 | 38 | Lady Honoka hid me, thankfully, but... |
| 0x2d3780 | 49 | She explained she is suspected of assassinating\n |
| 0x2d37b2 | 43 | the Mikado, and remains in hiding, herself. |
| 0x2d37de | 42 | She told me I'd been made a pawn of some\n |
| 0x2d3809 | 46 | conspiracy in the court. She said she was...\n |
| 0x2d3838 | 6 | sorry. |
| 0x2d383f | 46 | Who was the one who told you to take the tea\n |
| 0x2d386e | 16 | to the princess? |
| 0x2d387f | 17 | L-Lord... Oshtor. |
| 0x2d3891 | 46 | That... That's a lie. My brother would never\n |
| 0x2d38c0 | 16 | do such a thing. |
| 0x2d38d1 | 14 | It was you...! |
| 0x2d38e0 | 36 | YOU'RE the one plotting against him! |
| 0x2d3905 | 13 | Nekone, stop! |
| 0x2d3913 | 46 | Just as Nekone tries to fling herself at the\n |
| 0x2d3942 | 36 | woman, I manage to grab hold of her. |
| 0x2d3967 | 47 | Unhand me! It's her! She's the one responsible! |
| 0x2d3997 | 30 | ...I do not deny what you say. |
| 0x2d39bc | 47 | The person who told me to take the tea to Her\n |
| 0x2d39ec | 47 | Highness... At the time, I was certain it was\n |
| 0x2d3a1c | 12 | Lord Oshtor. |
| 0x2d3a29 | 49 | But... Now that I dwell upon it, it's as though\n |
| 0x2d3a5b | 36 | the memory is shrouded in thick fog. |
| 0x2d3a80 | 46 | I feel as though I was put in some manner of\n |
| 0x2d3aaf | 46 | trance, and merely THOUGHT it was Lord Oshtor. |
| 0x2d3ade | 47 | Now, I think... I think I was made to believe\n |
| 0x2d3b0e | 42 | an illusion. To presume this phantom was\n |
| 0x2d3b39 | 15 | Oshtor himself. |
| 0x2d3b49 | 46 | Were I to reveal this truth, I feel it would\n |
| 0x2d3b78 | 42 | prove his innocence, but Lady Honoka has\n |
| 0x2d3ba3 | 13 | forbidden it. |
| 0x2d3bb1 | 44 | She believes it is past the time for that.\n |
| 0x2d3bde | 45 | The true culprit would kill me to ensure my\n |
| 0x2d3c0c | 8 | silence. |
| 0x2d3c15 | 45 | Instead, she sends me to beg your aid, Lord\n |
| 0x2d3c43 | 45 | Haku--and asks that I relay a message to you. |
| 0x2d3c71 | 10 | A message? |
| 0x2d3c7c | 30 | Her Highness is yet in danger. |
| 0x2d3c9b | 47 | In her weakened state, there are those in the\n |
| 0x2d3ccb | 48 | court who will use her as a tool for their own\n |
| 0x2d3cfc | 5 | ends. |
| 0x2d3d02 | 32 | Please... Rescue the princess.\n |
| 0x2d3d23 | 33 | That is the message milady sends. |
| 0x2d3d45 | 27 | Wh--Hold on a second, here. |
| 0x2d3d61 | 49 | Save the princess? I'm starting to get a better\n |
| 0x2d3d93 | 45 | idea of the whole picture, here, but that's\n |
| 0x2d3dc1 | 6 | crazy. |
| 0x2d3dc8 | 34 | Where exactly is Honoka right now? |
| 0x2d3deb | 49 | I know not exactly where. I... I simply arrived\n |
| 0x2d3e1d | 44 | there before I was aware of my surroundings. |
| 0x2d3e4a | 46 | The same is true of the journey to this inn.\n |
| 0x2d3e79 | 46 | I was in one place, then in the next moment,\n |
| 0x2d3ea8 | 11 | I was here. |
| 0x2d3eb4 | 17 | The usual, huh... |
| 0x2d3ec6 | 42 | Guess I'll just consult the experts, then. |
| 0x2d3ef1 | 47 | You two know anything about where she might be? |
| 0x2d3f21 | 8 | Unknown. |
| 0x2d3f2a | 49 | ...Our connection with Mother has been severed.\n |
| 0x2d3f5c | 47 | Either it has become blocked somehow, or she... |
| 0x2d3f8c | 9 | ...Right. |
| 0x2d3f96 | 41 | Looks like we can't contact Honoka, then. |
| 0x2d3fc0 | 42 | I turn back to the woman and ask another\n |
| 0x2d3feb | 9 | question. |
| 0x2d3ff5 | 28 | Do you know where Oshtor is? |
| 0x2d4012 | 49 | I apologize, but... someone of my station would\n |
| 0x2d4044 | 30 | not be given that information. |
| 0x2d4063 | 46 | From the rumors I've heard... I imagine Lord\n |
| 0x2d4092 | 47 | Vurai is holding him in the underground prison. |
| 0x2d40c2 | 50 | He's likely interrogating milord for information\n |
| 0x2d40f5 | 32 | as to Lady Honoka's whereabouts. |
| 0x2d4116 | 44 | Vurai... one of those Eight Pillar Generals. |
| 0x2d4143 | 15 | Dear brother... |
| 0x2d4153 | 31 | Well, far from good news, that. |
| 0x2d4173 | 48 | Ougi whispers beside me, keeping his words out\n |
| 0x2d41a4 | 23 | of the others' earshot. |
| 0x2d41bc | 49 | Vurai is known to be a violent man with a short\n |
| 0x2d41ee | 39 | temper, and I've heard similar of his\n |
| 0x2d4216 | 10 | retainers. |
| 0x2d4221 | 46 | If such men are leading the interrogation, I\n |
| 0x2d4250 | 43 | cannot speak to how long Lord Oshtor will\n |
| 0x2d427c | 7 | last... |
| 0x2d4284 | 24 | Vurai the Vanguard, huh. |
| 0x2d429d | 11 | ...I'll go. |
| 0x2d42a9 | 7 | Nosuri? |
| 0x2d42b1 | 50 | I've been gathering intelligence on the security\n |
| 0x2d42e4 | 45 | of the palace in case of something like this. |
| 0x2d4312 | 47 | If my information is correct, an infiltration\n |
| 0x2d4342 | 41 | is... possible. I'll rescue the princess. |
| 0x2d436c | 19 | I can't allow that. |
| 0x2d4380 | 4 | Wh-- |
| 0x2d4385 | 17 | You're not going. |
| 0x2d4397 | 42 | Kuon, have you no compassion? Aren't you\n |
| 0x2d43c2 | 26 | worried for Her Highness!? |
| 0x2d43dd | 49 | Of course I'm worried, but I'm not about to let\n |
| 0x2d440f | 38 | a friend recklessly rush to her death. |
| 0x2d4436 | 51 | I am not being reckless. I'll rescue Her Highness\n |
| 0x2d446a | 20 | without fail, then-- |
| 0x2d447f | 44 | How can you say that with such confidence?\n |
| 0x2d44ac | 46 | You don't even believe you'll succeed, do you? |
| 0x2d44db | 7 | Nngh... |
| 0x2d44e3 | 48 | It sounded like you were seriously prepared to\n |
| 0x2d4514 | 21 | throw your life away. |
| 0x2d452a | 47 | Some things simply must be done, even if it's\n |
| 0x2d455a | 45 | in vain. That is what it means to be a good\n |
| 0x2d4588 | 6 | woman! |
| 0x2d458f | 47 | And sometimes you have to tell someone not to\n |
| 0x2d45bf | 46 | be stupid. That's what it means to be a good\n |
| 0x2d45ee | 7 | friend. |
| 0x2d45f6 | 48 | ...Give it to me straight, Ougi. Freakish luck\n |
| 0x2d4627 | 43 | aside, do we stand any chance of actually\n |
| 0x2d4653 | 17 | pulling this off? |
| 0x2d4665 | 50 | It would not be easy. Sneaking in is one thing--\n |
| 0x2d4698 | 49 | finding the princess and exfiltrating safely is\n |
| 0x2d46ca | 14 | quite another. |
| 0x2d46d9 | 5 | Ougi! |
| 0x2d46df | 41 | We don't know where she is. I have some\n |
| 0x2d4709 | 45 | inklings, but searching them WHILE avoiding\n |
| 0x2d4737 | 19 | security? Daunting. |
| 0x2d474b | 47 | Furthermore, there will be pursuit. If we are\n |
| 0x2d477b | 49 | to steal a princess, you realize, there will be\n |
| 0x2d47ad | 9 | a search. |
| 0x2d47b7 | 49 | No stone would be left unturned, including this\n |
| 0x2d47e9 | 44 | inn. We would have no safe haven whatsoever. |
| 0x2d4816 | 45 | Not to mention the barrier around the palace. |
| 0x2d4844 | 50 | It's not just a ward for spells. It has features\n |
| 0x2d4877 | 49 | that protect the grounds from intruders, as well. |
| 0x2d48a9 | 48 | If we try to penetrate it without some kind of\n |
| 0x2d48da | 49 | countermeasure, we're likely to walk right into\n |
| 0x2d490c | 7 | a trap. |
| 0x2d4914 | 47 | The moment we realize something's wrong, it'd\n |
| 0x2d4944 | 43 | already be too late--like struggling in a\n |
| 0x2d4970 | 13 | spider's web. |
| 0x2d497e | 43 | I--I've never heard of anything like that\n |
| 0x2d49aa | 7 | before. |
| 0x2d49b2 | 49 | I have it from a reliable source. If it weren't\n |
| 0x2d49e4 | 42 | the case, I wouldn't be so adamant about\n |
| 0x2d4a0f | 13 | stopping you. |
| 0x2d4a1d | 45 | Well, someone seems to be quite informed on\n |
| 0x2d4a4b | 36 | Yamato's state secrets, doesn't she? |
| 0x2d4a70 | 43 | Ah, I just... I heard a rumor about it in\n |
| 0x2d4a9c | 20 | passing, that's all. |
| 0x2d4ab1 | 42 | A rumor from your "reliable source," I'm\n |
| 0x2d4adc | 42 | certain. I suppose we'll leave it at that. |
| 0x2d4b07 | 16 | I appreciate it. |
| 0x2d4b18 | 42 | ...Guess that's how things'll shake out.\n |
| 0x2d4b43 | 45 | Sorry, Nosuri, but that plan isn't going to\n |
| 0x2d4b71 | 5 | work. |
| 0x2d4b77 | 5 | But-- |
| 0x2d4b7d | 48 | Easy, easy. I'm not saying we're just going to\n |
| 0x2d4bae | 18 | abandon them both. |
| 0x2d4bc1 | 14 | You... aren't? |
| 0x2d4bd0 | 49 | Whatever our next move is, we only get one shot\n |
| 0x2d4c02 | 40 | at it. If we screw it up, it's all over. |
| 0x2d4c2b | 50 | We can't go all-in on one risky plan. To stretch\n |
| 0x2d4c5e | 45 | a metaphor, we can't gamble with their lives. |
| 0x2d4c8c | 49 | Just hold on and let's formulate a proper plan.\n |
| 0x2d4cbe | 32 | Everyone's racking their brains. |
| 0x2d4cdf | 50 | Is that so? You should have said as much sooner,\n |
| 0x2d4d12 | 5 | then. |
| 0x2d4d18 | 48 | You're the one chomping at the bit to rush off\n |
| 0x2d4d49 | 28 | before anyone can explain... |
| 0x2d4d66 | 20 | If that's the case-- |
| 0x2d4d7b | 49 | I know, I know. Just... sit tight until we have\n |
| 0x2d4dad | 44 | a plan. A little patience is all I'm asking. |
| 0x2d4dda | 30 | That's all I needed to hear.\n |
| 0x2d4df9 | 33 | You're as reliable as ever, Haku. |
| 0x2d4e1b | 50 | We still need to discern the princess's location\n |
| 0x2d4e4e | 25 | and plot an escape route. |
| 0x2d4e68 | 46 | The person who would know where the princess\n |
| 0x2d4e97 | 5 | is... |
| 0x2d4e9d | 35 | Oh! Hey, it's you! How've you been? |
| 0x2d4ec1 | 43 | I've been well, but we need to stay quiet\n |
| 0x2d4eed | 10 | right now. |
| 0x2d4ef8 | 11 | OK, got it! |
| 0x2d4f04 | 42 | Shinonon seems to have taken a liking to\n |
| 0x2d4f2f | 29 | whoever this courtly lady is. |
| 0x2d4f4d | 48 | Uruuru, Saraana. Do you think you can use your\n |
| 0x2d4f7e | 43 | powers to reach Oshtor's prison undetected? |
| 0x2d4faa | 18 | Within parameters. |
| 0x2d4fbd | 48 | It is possible, if only from within the palace\n |
| 0x2d4fee | 8 | grounds. |
| 0x2d4ff7 | 12 | From within? |
| 0x2d5004 | 44 | Our connection with Mother is severed. The\n |
| 0x2d5031 | 47 | barrier bars us from creating a new path into\n |
| 0x2d5061 | 9 | the keep. |
| 0x2d506b | 47 | Within the barrier, however, we would be free\n |
| 0x2d509b | 47 | to shift between planes and shape our pathways. |
| 0x2d50cb | 44 | Simply place us beyond the barrier itself,\n |
| 0x2d50f8 | 25 | and we shall move unseen. |
| 0x2d5112 | 47 | A "path," huh. Must be that thing they always\n |
| 0x2d5142 | 3 | do. |
| 0x2d5146 | 33 | Hey, what does she mean by paths? |
| 0x2d5168 | 50 | Not a clue, I'm afraid. Code for something else,\n |
| 0x2d519b | 6 | maybe? |
| 0x2d51a2 | 11 | Quiet down. |
| 0x2d51ae | 11 | Oh, dear... |
| 0x2d51ba | 18 | Ngh. My apologies. |
| 0x2d51cd | 29 | They can move about within... |
| 0x2d51eb | 49 | In other words, as long as we can get the twins\n |
| 0x2d521d | 46 | to the palace, we'll be able to rescue Oshtor. |
| 0x2d524c | 50 | And then with Oshtor's help, we can pinpoint the\n |
| 0x2d527f | 40 | princess' exact location and rescue her. |
| 0x2d52a8 | 43 | ...But then we're still hung up on how to\n |
| 0x2d52d4 | 46 | infiltrate the palace, so it's the same plan\n |
| 0x2d5303 | 7 | anyway. |
| 0x2d530b | 7 | *FWUMP* |
| 0x2d5313 | 6 | Youch! |
| 0x2d531a | 42 | Nekone silently kicks me across the shins. |
| 0x2d5345 | 43 | Look, I want to save them. You KNOW I do.\n |
| 0x2d5371 | 43 | It's just impossible with the information\n |
| 0x2d539d | 12 | we have now. |
| 0x2d53aa | 33 | Unless you have any bright ideas? |
| 0x2d53cc | 31 | *FWUMP, {W20}FWUMP, {W20}FWUMP* |
| 0x2d53ec | 35 | See, you don't know eith--Ow! Ow,\n |
| 0x2d5410 | 20 | OK, stop kicking me! |
| 0x2d5425 | 50 | Beside me, Kuon looks at the floor with a somber\n |
| 0x2d5458 | 36 | expression. She's out of ideas, too. |
| 0x2d547d | 45 | If I even mention giving up, she's probably\n |
| 0x2d54ab | 30 | going to start biting me next. |
| 0x2d54ca | 48 | ...So, correct me if I'm wrong, dears. You can\n |
| 0x2d54fb | 46 | pull this off so long as you reach the palace? |
| 0x2d552a | 47 | Suddenly, a voice from behind me cuts through\n |
| 0x2d555a | 12 | the silence. |
| 0x2d5567 | 46 | I turn to find Karulau, smiling confidently,\n |
| 0x2d5596 | 40 | with Touka standing silently beside her. |
| 0x2d55bf | 50 | If that's the case, perhaps I can simply arrange\n |
| 0x2d55f2 | 18 | to take you there. |
| 0x2d5605 | 8 | Mother-- |
| 0x2d560e | 13 | ...Moth what? |
| 0x2d561c | 43 | I-I, ah... Madame, you shouldn't eavesdrop. |
| 0x2d5648 | 47 | Oh? I don't believe I made any effort to hide\n |
| 0x2d5678 | 12 | my presence. |
| 0x2d5685 | 46 | Or is it possible you simply didn't notice me? |
| 0x2d56b4 | 45 | You're very free with your words, you know.\n |
| 0x2d56e2 | 47 | It'd spell your end if I tell the authorities\n |
| 0x2d5712 | 13 | what I heard. |
| 0x2d5720 | 37 | Oh? Are you going to report us, then? |
| 0x2d5746 | 44 | Oh, relax, child. I hardly make a habit of\n |
| 0x2d5773 | 45 | tattling on little girls who play at rescuer. |
| 0x2d57a1 | 32 | Or have I misread the situation? |
| 0x2d57c2 | 48 | Hey, why's it so cold in here all of a sudden?\n |
| 0x2d57f3 | 20 | Is anyone else cold? |
| 0x2d5808 | 38 | By taking us to the palace, you mean-- |
| 0x2d582f | 48 | Just as it sounds. You seek a way in, don't you? |
| 0x2d5860 | 37 | I... don't think she's joking around. |
| 0x2d5886 | 49 | But how is she--? No, what's more important is... |
| 0x2d58b8 | 23 | Why are you helping us? |
| 0x2d58d0 | 45 | Isn't it the lot of siblings to assist each\n |
| 0x2d58fe | 49 | other in a bind? Dear little Kuon seems to need\n |
| 0x2d5930 | 8 | my help. |
| 0x2d5939 | 41 | Everyone immediately turns toward Kuon,\n |
| 0x2d5963 | 21 | who reddens abruptly. |
| 0x2d5979 | 47 | Help just because of that? Sounds like a load\n |
| 0x2d59a9 | 23 | of bull, if you ask me. |
| 0x2d59c1 | 51 | Karulau's more the type to throw Kuon off a cliff\n |
| 0x2d59f5 | 46 | and lecture about how climbing will make her\n |
| 0x2d5a24 | 7 | strong. |
| 0x2d5a2c | 45 | ...I doubt we're going to get an explanation. |
| 0x2d5a5a | 35 | What do you want in return, then?\n |
| 0x2d5a7e | 18 | What's your angle? |
| 0x2d5a91 | 50 | Do I need to repeat myself? I'm lending my sweet\n |
| 0x2d5ac4 | 48 | little sister a hand. I require no compensation. |
| 0x2d5af5 | 50 | That's so transparent it hurts. She's doing this\n |
| 0x2d5b28 | 22 | on purpose, isn't she? |
| 0x2d5b3f | 48 | I'm starting to get a pretty good idea of just\n |
| 0x2d5b70 | 11 | who she is. |
| 0x2d5b7c | 47 | We've been on pretty friendly terms, but even\n |
| 0x2d5bac | 49 | considering that, I'm not sure I should accept... |
| 0x2d5bde | 34 | Are you... very sure about this?\n |
| 0x2d5c01 | 6 | That-- |
| 0x2d5c08 | 45 | It's quite all right. We wouldn't have ever\n |
| 0x2d5c36 | 47 | used it except for a situation precisely like\n |
| 0x2d5c66 | 9 | this one. |
| 0x2d5c70 | 43 | I... I guess we don't really have a choice. |
| 0x2d5c9c | 46 | I peer over Karulau's shoulder at Touka, and\n |
| 0x2d5ccb | 14 | our eyes meet. |
| 0x2d5cda | 28 | Touka smiles back awkwardly. |
| 0x2d5cf7 | 45 | ...I guess I'll have to trust her as Kuon's\n |
| 0x2d5d25 | 7 | sister. |
| 0x2d5d2d | 31 | All right, everyone. Listen up. |
| 0x2d5d4d | 47 | What we're about to do is more dangerous than\n |
| 0x2d5d7d | 45 | anything else we've been through in the past. |
| 0x2d5dab | 49 | I don't have the full picture, and I don't know\n |
| 0x2d5ddd | 49 | what the right thing to do is. But I'm doing it\n |
| 0x2d5e0f | 42 | We have to save Oshtor and Anju with the\n |
| 0x2d5e3a | 48 | information we have, because we're not getting\n |
| 0x2d5e6b | 9 | any more. |
| 0x2d5e75 | 44 | We're just going to be winging it. This is\n |
| 0x2d5ea2 | 42 | insane. We don't even have a plan beyond\n |
| 0x2d5ecd | 20 | "grab them and run." |
| 0x2d5ee2 | 40 | And we don't have any time to get more\n |
| 0x2d5f0b | 45 | complicated than that, or else we'll be too\n |
| 0x2d5f39 | 5 | late. |
| 0x2d5f3f | 46 | For all the world, we're storming the palace\n |
| 0x2d5f6e | 47 | and taking the princess. They'll have a price\n |
| 0x2d5f9e | 34 | on our heads before the day's out. |
| 0x2d5fc1 | 49 | A small silence passes. Kuon opens her mouth to\n |
| 0x2d5ff3 | 6 | speak. |
| 0x2d5ffa | 27 | What are you trying to say? |
| 0x2d6016 | 42 | If anyone wants out, now is your chance.\n |
| 0x2d6041 | 46 | Nobody is going to look down on you or think\n |
| 0x2d6070 | 12 | less of you. |
| 0x2d607d | 49 | In fact, I'd prefer if you all said you're out.\n |
| 0x2d60af | 48 | The fewer people endangered by this, the better. |
| 0x2d60e0 | 43 | This is their last chance to throw in the\n |
| 0x2d610c | 8 | towel... |
| 0x2d6115 | 34 | ...But of course, nobody speaks.\n |
| 0x2d6138 | 27 | Everyone's mind is made up. |
| 0x2d6154 | 40 | *Sigh*... Yeah, I should have figured.\n |
| 0x2d617d | 37 | You guys are all insane, y'know that? |
| 0x2d61a3 | 48 | Just about, I think. That includes you, by the\n |
| 0x2d61d4 | 4 | way. |
| 0x2d61d9 | 13 | We are yours. |
| 0x2d61e7 | 49 | At your side, Master, is our true place in this\n |
| 0x2d6219 | 6 | world. |
| 0x2d6220 | 46 | Never a dull moment when I'm with you, love.\n |
| 0x2d624f | 34 | See, Kurarin's all pumped up, too! |
| 0x2d6272 | 16 | *Jiggle, jiggle* |
| 0x2d6283 | 39 | This is my duty as a noble of Yamato.\n |
| 0x2d62ab | 41 | I'll see my sworn brother safe from harm. |
| 0x2d62d5 | 44 | I-I'll accompany you, of course, Sir Haku... |
| 0x2d6302 | 37 | Save the imperial house from ruin--\n |
| 0x2d6328 | 50 | Did you even need to ask? Ougi, are preparations\n |
| 0x2d635b | 9 | complete? |
| 0x2d6365 | 30 | We're ready any time you like. |
| 0x2d6384 | 50 | You saved my life, boss. Even into the depths of\n |
| 0x2d63b7 | 45 | Denebokshiri, I'll be right behind you, yeah? |
| 0x2d63e5 | 35 | We'll follow you all the way, yeah? |
| 0x2d6409 | 22 | Everyone... Thank you. |
| 0x2d6420 | 20 | So, what will it be? |
| 0x2d6435 | 20 | If you'd be so kind. |
| 0x2d644a | 22 | Hm hm hm. As you wish. |
| 0x2d6461 | 41 | Karulau leads us down the stairs to the\n |
| 0x2d648b | 37 | Hakurokaku Inn's bottom-most floor... |
| 0x2d64b1 | 46 | Ultimately, we arrive in a completely barren\n |
| 0x2d64e0 | 26 | room, devoid of furniture. |
| 0x2d64fb | 37 | A dead end...? Oh, but that pattern-- |
| 0x2d6521 | 47 | Karulau sets a hand to the wall, manipulating\n |
| 0x2d6551 | 45 | another of those odd, puzzle-like mechanisms. |
| 0x2d657f | 9 | *Whistle* |
| 0x2d6589 | 45 | A hidden door... I had no idea the inn held\n |
| 0x2d65b7 | 16 | such secrets...! |
| 0x2d65c8 | 30 | I hear flowing water in there. |
| 0x2d65e7 | 40 | This leads into the city's underground\n |
| 0x2d6610 | 10 | aqueducts. |
| 0x2d661b | 42 | Karulau passes me a folded sheet of paper. |
| 0x2d6646 | 48 | When all's said and done, you are to tear this\n |
| 0x2d6677 | 38 | up and throw it away. Am I understood? |
| 0x2d669e | 16 | "This" being...? |
| 0x2d66af | 48 | A map of the waterways. Follow the path marked\n |
| 0x2d66e0 | 48 | in red, and you will arrive beneath the palace\n |
| 0x2d6711 | 27 | What!? Are you telling me-- |
| 0x2d672d | 15 | Mm. Impressive. |
| 0x2d673d | 39 | Wait, what? She already had plans for\n |
| 0x2d6765 | 34 | infiltrating the palace? That...\n |
| 0x2d6788 | 21 | That's risky as hell. |
| 0x2d679e | 44 | What exactly has our landlady been up to...? |
| 0x2d67cb | 50 | Now, hold! I've never heard a WHISPER of a route\n |
| 0x2d67fe | 44 | into the palace like this--explain yourself! |
| 0x2d682b | 47 | Tempting, but I believe you're short on time,\n |
| 0x2d685b | 41 | are you not? You'd best hurry along, now. |
| 0x2d6885 | 4 | I... |
| 0x2d688a | 6 | Hm hm. |
| 0x2d6891 | 47 | Nekone's shoulders slump, and the mistress of\n |
| 0x2d68c1 | 29 | the inn smiles kindly at her. |
| 0x2d68df | 44 | She's right, though. We don't have time to\n |
| 0x2d690c | 6 | waste. |
| 0x2d6913 | 45 | Hey, uh. You can probably leave this to us.\n |
| 0x2d6941 | 46 | You might want to lay low here until this is\n |
| 0x2d6970 | 9 | all over. |
| 0x2d697a | 44 | I refuse. Please, allow me to accompany you. |
| 0x2d69a7 | 43 | It is my responsibility to look after Her\n |
| 0x2d69d3 | 22 | Highness. So, please-- |
| 0x2d69ea | 35 | All right, all right. You can come. |
| 0x2d6a0e | 27 | Please stay safe, everyone. |
| 0x2d6a2a | 42 | Th-Thank you for all you've done for us.\n |
| 0x2d6a55 | 27 | I wish you both the best... |
| 0x2d6a78 | 51 | C-Cocopo? I thought I told you to wait outside...\n |
| 0x2d6aac | 38 | Y-You can't just barge in like this... |
| 0x2d6ad9 | 47 | Oh, dear. He seems to have already made quite\n |
| 0x2d6b09 | 25 | the mess of the interior. |
| 0x2d6b23 | 49 | I'm so sorry... I-I'll be sure to scold him for\n |
| 0x2d6b55 | 12 | misbehaving. |
| 0x2d6b62 | 49 | You needn't worry. I... I believe I'm beginning\n |
| 0x2d6b94 | 46 | to get used to working here. I will see to it. |
| 0x2d6bc3 | 39 | Th-Thank you... Cocopo, can you fit...? |
| 0x2d6bf1 | 50 | Don't worry about it, princess. You go on ahead,\n |
| 0x2d6c24 | 47 | and I'll give the big fella a good shove from\n |
| 0x2d6c54 | 7 | behind. |
| 0x2d6c5c | 12 | Go on ahead! |
| 0x2d6c69 | 37 | S-Sorry to cause so much trouble...\n |
| 0x2d6c8f | 10 | Thank you. |
| 0x2d6c9a | 29 | N-Nekone! It's dark inside.\n |
| 0x2d6cb8 | 21 | Please, take my han-- |
| 0x2d6cce | 27 | That will not be necessary. |
| 0x2d6cea | 20 | Master, your hand... |
| 0x2d6cff | 24 | Touch your skin to ours. |
| 0x2d6d18 | 38 | Our bodies shall embrace yours wholly. |
| 0x2d6d3f | 33 | I, uh. I'll decline, thank you.\n |
| 0x2d6d61 | 37 | I'd like to keep using both my hands. |
| 0x2d6d87 | 48 | I had so much fun here. I'm gonna treasure all\n |
| 0x2d6db8 | 42 | the memories I made here forever. Right,\n |
| 0x2d6de3 | 8 | Kurarin? |
| 0x2d6dec | 19 | *Jiggle, jiggle*... |
| 0x2d6e00 | 19 | Shall we get going? |
| 0x2d6e14 | 47 | I'll never forget the kindness you have shown\n |
| 0x2d6e44 | 33 | me. May we meet again some day... |
| 0x2d6e66 | 35 | Thanks for taking care of Shinonon. |
| 0x2d6e8a | 49 | It was no trouble, but... are you sure you wish\n |
| 0x2d6ebc | 40 | not to leave her here, considering th--? |
| 0x2d6ee5 | 48 | Nah. I might not be back here for a long time.\n |
| 0x2d6f16 | 36 | She sticks with me this time around. |
| 0x2d6f3b | 46 | I see. Shinonon, dear, you can come back any\n |
| 0x2d6f6a | 35 | time you'd like to play, all right? |
| 0x2d6f8e | 47 | I look forward to seeing you again, Shinonon.\n |
| 0x2d6fbe | 42 | Please, ah, be sure to cover up for bed.\n |
| 0x2d6fe9 | 16 | Walk, don't run! |
| 0x2d6ffa | 28 | Gotcha. See ya later, Touka. |
| 0x2d7017 | 26 | Yes, I will see you later. |
| 0x2d7032 | 46 | Thank you for taking care of my dear sister.\n |
| 0x2d7061 | 32 | Someday, I shall repay the debt. |
| 0x2d7082 | 46 | Lady Touka, I'm sorry I can't do anything to\n |
| 0x2d70b1 | 37 | thank you for all you've done for us. |
| 0x2d70d7 | 34 | Oh, no need to tr--I mean, ah...\n |
| 0x2d70fa | 23 | Truly, it's no trouble. |
| 0x2d7112 | 48 | Never did I expect to meet kinfolk abroad like\n |
| 0x2d7143 | 47 | this, much less those who uphold the honor we\n |
| 0x2d7173 | 11 | so cherish. |
| 0x2d717f | 46 | I won't forget the kindness you've shown me.\n |
| 0x2d71ae | 22 | Until we meet again... |
| 0x2d71c5 | 40 | Yes, I look forward to it. Until then,\n |
| 0x2d71ee | 42 | remember--even when the path seems lost,\n |
| 0x2d7219 | 20 | justice reveals all. |
| 0x2d722e | 11 | Yes, ma'am. |
| 0x2d723a | 14 | Nosuri & Touka |
| 0x2d7249 | 32 | Upon the name of the Evenkuruga. |
| 0x2d726a | 42 | What's wrong, Kuon? Aren't you gonna say\n |
| 0x2d7295 | 8 | goodbye? |
| 0x2d729e | 44 | You exaggerate, Haku. We'll be right back.\n |
| 0x2d72cb | 34 | We're just going out for a stroll. |
| 0x2d72ee | 20 | Kuon, what are you-- |
| 0x2d7303 | 40 | We're probably never coming back here.\n |
| 0x2d732c | 21 | Kuon knows that much. |
| 0x2d7342 | 15 | Let's go, Haku. |
| 0x2d7352 | 7 | Kuon... |
| 0x2d735a | 48 | Still angry at us for leaving for our travels?\n |
| 0x2d738b | 46 | So stubborn. I can only wonder whom you took\n |
| 0x2d73ba | 6 | after. |
| 0x2d73c1 | 48 | I think it's clear enough. I took after you...\n |
| 0x2d73f2 | 7 | Mother. |
| 0x2d73fa | 10 | Lord Haku. |
| 0x2d7405 | 3 | Hm? |
| 0x2d7409 | 29 | Please watch over her for me. |
| 0x2d7427 | 10 | ...I will. |
| 0x2d7432 | 47 | We'll be back soon, so have a feast prepared,\n |
| 0x2d7462 | 10 | all right? |
| 0x2d746d | 48 | Of course. I'll prepare all your favorites, so\n |
| 0x2d749e | 48 | come home straight away, young lady. No detours. |
| 0x2d74cf | 6 | ...OK. |
| 0x2d74d6 | 48 | Whether we succeed or not, it's... likely that\n |
| 0x2d7507 | 38 | we'll never be able to come back here. |
| 0x2d752e | 46 | Even so... I might not have lived here long,\n |
| 0x2d755d | 26 | but... it feels like home. |
| 0x2d7578 | 5 | So... |
| 0x2d757e | 14 | We'll be back. |
| 0x2d758d | 16 | And off they go. |
| 0x2d759e | 46 | Mm. Things around here will be awfully quiet\n |
| 0x2d75cd | 13 | without them. |
| 0x2d75db | 47 | Are you certain you don't wish to go with them? |
| 0x2d760b | 50 | To be sure, that was my intent in the beginning,\n |
| 0x2d763e | 6 | but... |
| 0x2d7645 | 48 | I believe Kuon no longer requires my protection. |
| 0x2d7676 | 48 | True. She's grown up into quite the young lady\n |
| 0x2d76a7 | 11 | without us. |
| 0x2d76b3 | 45 | Thanks to Lord Haku and the others, no doubt. |
| 0x2d76e1 | 20 | You're likely right. |
| 0x2d76f6 | 46 | Such a strange man. He almost reminds me of... |
| 0x2d7725 | 8 | Of what? |
| 0x2d772e | 45 | Ah, think nothing of it. Merely reminiscing\n |
| 0x2d775c | 19 | over a bygone time. |
| 0x2d7770 | 26 | Nostalgic, faraway days... |
| 0x2d778b | 6 | I see. |
| 0x2d7792 | 27 | Time truly does slip us by. |
| 0x2d77ae | 30 | Yes. Kuon has grown so much... |
| 0x2d77cd | 46 | I suppose this is a feeling all mothers must\n |
| 0x2d77fc | 47 | experience, watching their children brave the\n |
| 0x2d782c | 8 | Yes...\n |
| 0x2d7835 | 17 | You may be right. |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_04.json` com a forma:
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
