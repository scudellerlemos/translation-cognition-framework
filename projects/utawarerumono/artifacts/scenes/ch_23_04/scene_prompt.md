# Cena ch_23_04 — pacote de traducao (294 linhas)

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
| Aruruu | Personagem | Aruruu | manter_original | moderate |
| Camyu | Personagem | Camyu | manter_original | moderate |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Mito | Personagem | Mito | manter_original | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Onkamiyamukai | Local | Onkamiyamukai | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `me.` -> `mim.` (Garota, 17_01)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `as well.` -> `também.` (Haku, 17_01)
- `I see...` -> `Entendo...` (Haku, 11_02)
- `army.` -> `exército.` (Homem, 22_08)
- `Lady Munechika.` -> `Senhora Munechika.` (Atuy, 18_01)
- `around.` -> `por aí.` (Kuon, 14_02)
- `...What do you mean?` -> `...O que você quer dizer?` (Garota, 16_01)
- `something...` -> `alguma coisa...` (Anju, 18_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `him.` -> `dele.` (Nekone, 15_02)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
- `Munechika.` -> `Munechika.` (Narração, 23_02)
- `capital...` -> `capital...` (Haku, 15_09)
- `everything.` -> `tudo.` (Maroro, 19_06)
- `Right?` -> `né?` (Haku, 11_01)
- `job.` -> `trabalho.` (Falante (Kuon ou Maroro), 18_01)
- `ourselves.` -> `para nós.` (Kuon, 15_02)
- `That's all.` -> `É isso.` (Ukon, 13_02)
- `Master Mito calls for you.` -> `Mestre Mito o chama.` (Garota, 19_08)
- `Got it.` -> `Entendi.` (Haku, 16_01)
- `it.` -> `aí.` (Haku, 15_03)
- `...Oh?` -> `...Ah?` (Garota, 17_01)
- `today.` -> `hoje.` (Atuy, 18_01)
- `for you.` -> `para você.` (Ougi, 13_08)
- `Is this...?` -> `É isto...?` (Haku, 20_21)
- `of them.` -> `deles.` (Haku, 19_06)
- `yourself.` -> `você.` (Kuon, 13_01)
- `culture.` -> `cultura.` (Kuon, 18_01)
- `knowledge.` -> `conhecimento.` (Maroro, 12_12)
- `way.` -> `jeito.` (Atuy, 18_01)
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
| 0x27d08c | 45 | So, Oshtor, what did you want to talk to me\n |
| 0x27d0ba | 36 | about? I came alone, like you asked. |
| 0x27d0df | 47 | I enter the room to find Oshtor seated in his\n |
| 0x27d10f | 45 | chair with eyes closed, as though meditating. |
| 0x27d13d | 27 | I sit down across from him. |
| 0x27d15d | 48 | I didn't bring Kuon, Nekone, or even the twins\n |
| 0x27d18e | 14 | with me today. |
| 0x27d19d | 47 | Oshtor had instructed me to come alone... and\n |
| 0x27d1cd | 47 | specifically asked that I not bring Kuon with\n |
| 0x27d1fd | 3 | me. |
| 0x27d201 | 39 | Oshtor opens his eyes in grave silence. |
| 0x27d229 | 47 | ...We have lost contact with the army we sent\n |
| 0x27d259 | 10 | to Tuskur. |
| 0x27d264 | 8 | ...What? |
| 0x27d26d | 47 | We sent reinforcements immediately after, but\n |
| 0x27d29d | 46 | we shortly lost our communications with them\n |
| 0x27d2cc | 8 | as well. |
| 0x27d2d5 | 44 | Are you saying... Munechika's been defeated? |
| 0x27d302 | 48 | No, it does not appear as though the enemy has\n |
| 0x27d333 | 45 | fallen back yet. We seem locked in stalemate. |
| 0x27d361 | 8 | I see... |
| 0x27d36a | 28 | A sigh of relief escapes me. |
| 0x27d387 | 45 | However, the situation is dire. The army is\n |
| 0x27d3b5 | 42 | isolated, and beyond the reach of supply\n |
| 0x27d3e0 | 8 | convoys. |
| 0x27d3e9 | 48 | Their supplies may last a while yet, but it is\n |
| 0x27d41a | 41 | only a matter of time until they run dry. |
| 0x27d444 | 37 | So what is it you're trying to say?\n |
| 0x27d46a | 34 | Don't tell me you're planning on-- |
| 0x27d48d | 48 | Hm. Your keen mind makes this much simpler, as\n |
| 0x27d4be | 49 | usual. I would have you deliver supplies to our\n |
| 0x27d4f0 | 5 | army. |
| 0x27d4f6 | 18 | Figured as much... |
| 0x27d509 | 46 | At the same time, depending on the situation\n |
| 0x27d538 | 43 | there, I wish for you to lend your aid to\n |
| 0x27d564 | 15 | Lady Munechika. |
| 0x27d574 | 44 | Hold it. Delivering supplies is one thing,\n |
| 0x27d5a1 | 47 | but we don't exactly have a bunch of soldiers\n |
| 0x27d5d1 | 7 | around. |
| 0x27d5d9 | 47 | I seriously doubt we're going to be much help\n |
| 0x27d609 | 9 | to her... |
| 0x27d613 | 48 | I did not mean martially. I had hoped that you\n |
| 0x27d644 | 47 | would be able to provide more... moral support. |
| 0x27d674 | 20 | ...What do you mean? |
| 0x27d689 | 35 | You remember Dekopompo, do you not? |
| 0x27d6ad | 47 | Fatass general, basically a petty crook, only\n |
| 0x27d6dd | 41 | has his position because of nepotism or\n |
| 0x27d707 | 12 | something... |
| 0x27d714 | 15 | What about him? |
| 0x27d724 | 46 | Firstly, you must know why he was chosen for\n |
| 0x27d753 | 42 | this campaign. In the last war, he erred\n |
| 0x27d77e | 8 | gravely. |
| 0x27d787 | 41 | To put it plainly, he has been given an\n |
| 0x27d7b1 | 30 | opportunity to redeem himself. |
| 0x27d7d0 | 48 | Thus, I believe Dekopompo is likely to attempt\n |
| 0x27d801 | 43 | to seize glory in a blind, artless assault. |
| 0x27d82d | 45 | However, Lady Munechika's expertise lies in\n |
| 0x27d85b | 23 | defensive strategies... |
| 0x27d873 | 50 | One can say they are like oil and water. Without\n |
| 0x27d8a6 | 42 | the cooperation of her allies, even Lady\n |
| 0x27d8d1 | 31 | Munechika will be hard-pressed. |
| 0x27d8f1 | 44 | But isn't the marshal Mikazuchi's brother?\n |
| 0x27d91e | 15 | That Raiko guy? |
| 0x27d92e | 43 | I don't know him that well, but Mikazuchi\n |
| 0x27d95a | 39 | says he's a tactician beyond compare.\n |
| 0x27d982 | 28 | I doubt he'd let that slide. |
| 0x27d99f | 44 | I speak in all earnestness when I tell you\n |
| 0x27d9cc | 43 | I am certain Dekopompo will not obey Lord\n |
| 0x27d9f8 | 15 | Raiko's orders. |
| 0x27da08 | 4 | Huh? |
| 0x27da0d | 44 | He sees Lord Raiko as an upstart, and Lady\n |
| 0x27da3a | 49 | Munechika as a novice who won her title through\n |
| 0x27da6c | 16 | wiles and charm. |
| 0x27da7d | 45 | Blinded by pride, and believing himself the\n |
| 0x27daab | 46 | greatest of us, he considers those below him\n |
| 0x27dada | 10 | worthless. |
| 0x27dae5 | 49 | In fact, he would likely blame a poor situation\n |
| 0x27db17 | 47 | on the perceived incompetence of those around\n |
| 0x27db47 | 4 | him. |
| 0x27db4c | 44 | Eager to regain honor, he will act rashly,\n |
| 0x27db79 | 48 | forcing Lord Raiko and Lady Munechika to clean\n |
| 0x27dbaa | 14 | up his messes. |
| 0x27dbb9 | 10 | I-I see... |
| 0x27dbc4 | 50 | I don't get it. How the hell did a guy like that\n |
| 0x27dbf7 | 45 | ever become one of the Eight Pillar Generals? |
| 0x27dc25 | 48 | I'm not too clear on the politics around here,\n |
| 0x27dc56 | 38 | but is corruption really that rampant? |
| 0x27dc7d | 8 | ...Hm... |
| 0x27dc86 | 46 | Oh, uh, if it's complicated stuff, you don't\n |
| 0x27dcb5 | 48 | have to explain. I don't want to know anything\n |
| 0x27dce6 | 18 | too incriminating. |
| 0x27dcf9 | 30 | No... it is nothing like that. |
| 0x27dd18 | 49 | Yamato once had a general of great integrity...\n |
| 0x27dd4a | 46 | On his deathbed, he begged our liege to look\n |
| 0x27dd79 | 40 | after his child, worried for his future. |
| 0x27dda2 | 48 | That general... was a true paragon of honesty,\n |
| 0x27ddd3 | 19 | honor, and loyalty. |
| 0x27dde7 | 48 | I cannot go into too much detail, but I assume\n |
| 0x27de18 | 38 | you can gather the gist of the matter. |
| 0x27de3f | 29 | Yeah... I think I get it now. |
| 0x27de5d | 46 | ...Now, the topic at hand. In any case, that\n |
| 0x27de8c | 44 | is why I wish for you to join up with Lady\n |
| 0x27deb9 | 10 | Munechika. |
| 0x27dec4 | 44 | I would go myself, but as I have inherited\n |
| 0x27def1 | 49 | Lady Munechika's duty of defending the imperial\n |
| 0x27df23 | 10 | capital... |
| 0x27df2e | 34 | I am not able to leave this place. |
| 0x27df51 | 24 | Will you do this for me? |
| 0x27df6a | 49 | I am sure Munechika will be well pleased to see\n |
| 0x27df9c | 33 | familiar faces coming to her aid. |
| 0x27dfbe | 13 | What to do... |
| 0x27dfcc | 46 | Accepting this job means, however minor of a\n |
| 0x27dffb | 41 | role, we're taking part in the invasion\n |
| 0x27e025 | 10 | of Tuskur. |
| 0x27e030 | 50 | It's not just me wanting to keep my hands clean.\n |
| 0x27e063 | 47 | After all, there's no right or wrong in war--\n |
| 0x27e093 | 25 | just opposing ideologies. |
| 0x27e0ad | 49 | But Tuskur is Kuon's homeland, and that changes\n |
| 0x27e0df | 11 | everything. |
| 0x27e0eb | 49 | I can't help invade the homeland of the one who\n |
| 0x27e11d | 40 | saved me. And even for Munechika, Kuon\n |
| 0x27e146 | 17 | wouldn't--Wait... |
| 0x27e158 | 46 | Taking on this job might be better than just\n |
| 0x27e187 | 21 | mulling over it here. |
| 0x27e19d | 41 | I do not wish to rush you for an answer-- |
| 0x27e1c7 | 12 | No, I'll go. |
| 0x27e1d4 | 19 | Hm... You are sure? |
| 0x27e1e8 | 50 | We handle the jobs you give us. That's just what\n |
| 0x27e21b | 37 | we do, and that's all there is to it. |
| 0x27e241 | 6 | Right? |
| 0x27e248 | 20 | ...I see. Thank you. |
| 0x27e25d | 48 | And besides, whichever way this ends up going,\n |
| 0x27e28e | 46 | I want to be there to see it with my own eyes. |
| 0x27e2bd | 45 | And I'm sure Kuon would say the same thing... |
| 0x27e2eb | 21 | To Tuskur? All of us? |
| 0x27e301 | 49 | After returning, I gather everyone to tell them\n |
| 0x27e333 | 44 | we're going to Tuskur. Shock is visible on\n |
| 0x27e360 | 11 | every face. |
| 0x27e36c | 50 | Yeah, sorry this is so sudden. Long story short,\n |
| 0x27e39f | 46 | we need to deliver some supplies to Munechika. |
| 0x27e3ce | 49 | But it probably won't just be a simple delivery\n |
| 0x27e400 | 4 | job. |
| 0x27e405 | 25 | And by that, you mean...? |
| 0x27e41f | 44 | The war's locked in a stalemate. If Tuskur\n |
| 0x27e44c | 47 | forces try to stop us, we'll have to fend for\n |
| 0x27e47c | 10 | ourselves. |
| 0x27e487 | 22 | But that would mean... |
| 0x27e49e | 39 | Nekone glances uncertainly toward Kuon. |
| 0x27e4c6 | 45 | Her expression's hardened. That's expected,\n |
| 0x27e4f4 | 48 | though--she's shut herself away ever since the\n |
| 0x27e525 | 15 | invasion began. |
| 0x27e535 | 48 | ...But telling everyone except Kuon about this\n |
| 0x27e566 | 42 | would be unfair. I have to be honest here. |
| 0x27e591 | 50 | Depending on the situation, we may be doing more\n |
| 0x27e5c4 | 45 | than just protecting ourselves if Munechika\n |
| 0x27e5f2 | 9 | needs us. |
| 0x27e5fc | 48 | It is entirely possible that some of us may die. |
| 0x27e62d | 43 | We have two days. Pay's good, but it's no\n |
| 0x27e659 | 46 | ordinary job. If you don't want to come, you\n |
| 0x27e688 | 14 | don't have to. |
| 0x27e697 | 11 | That's all. |
| 0x27e6a3 | 16 | Master, wake up. |
| 0x27e6b4 | 26 | Master Mito calls for you. |
| 0x27e6cf | 7 | Got it. |
| 0x27e6d7 | 49 | I get out of bed before the twins can slip into\n |
| 0x27e709 | 3 | it. |
| 0x27e70d | 45 | Had a feeling he'd be calling for me tonight. |
| 0x27e73b | 47 | Guess I was right to sleep in my clothes so I\n |
| 0x27e76b | 42 | don't have to waste time getting ready...  |
| 0x27e796 | 23 | What's wrong? Let's go. |
| 0x27e7ae | 14 | Disappointing. |
| 0x27e7bd | 38 | You are an incorrigible tease, Master. |
| 0x27e7e4 | 40 | ...What exactly do you two want from me? |
| 0x27e80d | 31 | Hoho... I thank you for coming. |
| 0x27e82d | 36 | Welcome. Please, come sit down here. |
| 0x27e852 | 49 | The two of them welcome me with familiar smiles\n |
| 0x27e884 | 22 | when I enter the room. |
| 0x27e89b | 45 | I had a feeling you'd want to see me tonight. |
| 0x27e8c9 | 6 | ...Oh? |
| 0x27e8d0 | 43 | You've already heard from Oshtor about me\n |
| 0x27e8fc | 25 | heading to Tuskur, right? |
| 0x27e916 | 29 | ...Yes. You're exactly right. |
| 0x27e934 | 43 | It appears we must part ways for a while.\n |
| 0x27e960 | 46 | I wanted to see you one more time before you\n |
| 0x27e98f | 7 | depart. |
| 0x27e997 | 43 | Oh, right. I actually have a gift for you\n |
| 0x27e9c3 | 6 | today. |
| 0x27e9ca | 45 | The twins standing by my side move forward,\n |
| 0x27e9f8 | 40 | placing a parcel on the table at my cue. |
| 0x27ea21 | 8 | For you. |
| 0x27ea2a | 40 | Please have some while it is still cold. |
| 0x27ea53 | 48 | As the twins open up the parcel, the two faces\n |
| 0x27ea84 | 33 | before me break into soft smiles. |
| 0x27eaa6 | 18 | Oho...! This is... |
| 0x27eab9 | 11 | Is this...? |
| 0x27eac5 | 49 | On the tray are two plates, with puffs for each\n |
| 0x27eaf7 | 8 | of them. |
| 0x27eb00 | 27 | ...Did you make this, Haku? |
| 0x27eb1c | 49 | Nah. I mean, I might have worked on the recipe,\n |
| 0x27eb4e | 39 | but the actual cooking is all Rulutieh. |
| 0x27eb76 | 47 | She's gotten really good at it now. She makes\n |
| 0x27eba6 | 25 | it way better than I can. |
| 0x27ebc0 | 47 | Rulutieh... The youngest princess of Kujyuri,\n |
| 0x27ebf0 | 17 | if memory serves. |
| 0x27ec02 | 47 | Ah, yes. Now that I recall, you quite enjoyed\n |
| 0x27ec32 | 42 | sweets like these... You often made them\n |
| 0x27ec5d | 9 | yourself. |
| 0x27ec67 | 48 | Oho, the outer shell is nice and crunchy, with\n |
| 0x27ec98 | 49 | a soft center...! It brings back such memories... |
| 0x27ecca | 46 | He wasn't too picky back then, but he always\n |
| 0x27ecf9 | 46 | loved sweets like these. Said sugar was good\n |
| 0x27ed28 | 11 | brain food. |
| 0x27ed34 | 46 | Hm? Memories, huh...? Now that I think about\n |
| 0x27ed63 | 45 | it, this country has a pretty distinct food\n |
| 0x27ed91 | 8 | culture. |
| 0x27ed9a | 32 | Did you teach them all that too? |
| 0x27edbb | 38 | No, Yamato's cuisine arose on its own. |
| 0x27ede2 | 49 | I taught them agriculture and the use of simple\n |
| 0x27ee14 | 47 | seasonings, but they did not ask for culinary\n |
| 0x27ee44 | 10 | knowledge. |
| 0x27ee4f | 49 | It seems they wished for more practical things... |
| 0x27ee81 | 49 | Of course, even had they asked me, I would have\n |
| 0x27eeb3 | 46 | had little to offer... I am certainly no chef. |
| 0x27eee2 | 48 | Oh yeah. I guess he didn't know anything about\n |
| 0x27ef13 | 18 | cooking back then. |
| 0x27ef26 | 33 | I sneak a small glance at Honoka. |
| 0x27ef48 | 50 | And as for my sister-in-law, she was a brilliant\n |
| 0x27ef7b | 49 | scientist too, but her culinary skills were, uh-- |
| 0x27efad | 50 | I can almost hear Honoka's neck straining as she\n |
| 0x27efe0 | 29 | pointedly avoids eye contact. |
| 0x27effe | 48 | For a while, we talk about the simpler things,\n |
| 0x27f02f | 47 | enjoying the green tea poured for us by Honoka. |
| 0x27f05f | 43 | Even knowing these two are my brother and\n |
| 0x27f08b | 46 | sister-in-law from the past, we act the same\n |
| 0x27f0ba | 4 | way. |
| 0x27f0bf | 49 | As usual, I talk about my boring everyday life,\n |
| 0x27f0f1 | 47 | and my brother and Honoka happily listen to me. |
| 0x27f121 | 47 | Time passes peacefully here, as it always does. |
| 0x27f151 | 45 | Hey... Could you tell me why you decided to\n |
| 0x27f17f | 14 | invade Tuskur? |
| 0x27f18e | 45 | The smile fades from my brother's face, and\n |
| 0x27f1bc | 34 | Honoka's gentle expression clouds. |
| 0x27f1df | 46 | Are you disappointed in me for starting this\n |
| 0x27f20e | 9 | invasion? |
| 0x27f218 | 36 | No. I know politics is dirty work.\n |
| 0x27f23d | 46 | But this is you we're talking about--there's\n |
| 0x27f26c | 18 | gotta be a reason. |
| 0x27f27f | 30 | So what I want to know is why. |
| 0x27f29e | 26 | ...Hah. How very like you. |
| 0x27f2b9 | 49 | I suppose you have the right and responsibility\n |
| 0x27f2eb | 16 | to know, then... |
| 0x27f2fc | 42 | You are aware of the region known as the\n |
| 0x27f327 | 29 | Onkamiyamukai, within Tuskur? |
| 0x27f345 | 47 | The holy land, where the one who calls itself\n |
| 0x27f375 | 15 | a god sleeps... |
| 0x27f385 | 45 | But when I probed further, I found that the\n |
| 0x27f3b3 | 45 | land is filled with myths, legends, and all\n |
| 0x27f3e1 | 20 | manner of mysteries. |
| 0x27f3f6 | 49 | All the information I gathered... led me to one\n |
| 0x27f428 | 11 | conclusion. |
| 0x27f434 | 16 | Wait, you mean-- |
| 0x27f445 | 48 | Yes. There is most likely a grand ruin located\n |
| 0x27f476 | 19 | within that region. |
| 0x27f48a | 48 | And I have come to believe that it may contain\n |
| 0x27f4bb | 19 | the answers I seek. |
| 0x27f4cf | 46 | In order to find that out, I must first take\n |
| 0x27f4fe | 18 | control of Tuskur. |
| 0x27f511 | 42 | But why go to war? Couldn't we just have\n |
| 0x27f53c | 41 | negotiated with them and gotten them to\n |
| 0x27f566 | 10 | cooperate? |
| 0x27f571 | 42 | Camyu and Aruruu seemed friendly enough.\n |
| 0x27f59c | 47 | If we try to talk things over, maybe we could-- |
| 0x27f5cc | 35 | Negotiations have come to no avail. |
| 0x27f5f0 | 44 | To the people of Tuskur, the Onkamiyamukai\n |
| 0x27f61d | 20 | is a forbidden land. |
| 0x27f632 | 42 | They would never allow outsiders such as\n |
| 0x27f65d | 32 | ourselves within its boundaries. |
| 0x27f67e | 48 | Moreover, years ago, a massive war wracked the\n |
| 0x27f6af | 46 | nation, over control of the power slumbering\n |
| 0x27f6de | 22 | within those lands...  |
| 0x27f6f5 | 48 | If they will not allow us in, I have no choice\n |
| 0x27f726 | 24 | but to take it by force. |
| 0x27f73f | 48 | Haku... Each and every one of us has one thing\n |
| 0x27f770 | 30 | that they refuse to sacrifice. |
| 0x27f78f | 47 | The only way for you to realize your goals is\n |
| 0x27f7bf | 31 | to crush those that oppose you. |
| 0x27f7df | 47 | You should know this well, for we are all the\n |
| 0x27f80f | 36 | same. These people... and we humans. |
| 0x27f834 | 49 | Heh... I only wanted to accomplish what I still\n |
| 0x27f866 | 40 | can, before you succeed me. That is all. |
| 0x27f88f | 44 | This... will be my final act of selfishness. |
| 0x27f8bc | 48 | As the old man before me smiles, I see a flash\n |
| 0x27f8ed | 30 | of my brother behind his eyes. |
| 0x27f90c | 46 | ...There's nothing more I can say in response. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_04.json` com a forma:
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
