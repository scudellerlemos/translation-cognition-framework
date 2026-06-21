# Cena ch_15_01 — pacote de traducao (778 linhas)

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
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/evidence/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acent
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| aperyu | Item | aperyu | manter_original | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ozen | Personagem | Ozen | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
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
### Ozen — criticality: low
- Ozen — `voice_criticality: low`. General-Pilar, pai da Rulutieh; registro grave/nobre.
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `you?` -> `pode?` (Haku, 13_01)
- `...Huh!?` -> `...Hein!?` (Haku, 13_06)
- `U-Um...` -> `E-Ei...` (Rulutieh, 14_09)
- `table.` -> `na mesa.` (Haku, 13_02)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `her face.` -> `ver ela.` (Haku, 14_03)
- `suspicious.` -> `suspeito demais.` (Kuon, 13_05)
- `though...` -> `porém...` (Haku, 13_03)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `right.` -> `direito.` (Kuon, root)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `Oh?` -> `Oh?` (Haku, 14_04)
- `Mikado.` -> `Mikado.` (Rulutieh, 14_02)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `Here you are.` -> `Aqui estão.` (Estalajadeira, 12_04)
- `Wh... Wh-Wha...` -> `Q... Q-Quê...` (Man, root)
- `but...` -> `mas...` (Kuon, 12_16)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `What?` -> `Que?` (Haku, 12_02)
- `Me...?` -> `Eu...?` (Protagonista, root)
- `Wha--` -> `Quê--` (Man, root)
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
- Homem: `The way you were carrying on, you got us all\n` -> `Do jeito que você estava, nos deixou todos\n`
- Homem: `anxious, too!` -> `ansiosos também!`
- Homem: `Wahahahaha!!` -> `Wahahahaha!!`
- Rulutieh: `Oh, pardon me.` -> `Ah, com licença.`
- Rulutieh: `I'm... sorry about, um...` -> `Eu... desculpe, é que...`
- Rulutieh: `That's a relief... Come on, Cocopo. We'll just be\n` -> `Ainda bem... Vamos, Cocopo. Só estamos\n`

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0xa44ae | 47 | Expression somewhat depressed, Kuon rests her\n |
| 0xa44de | 26 | hands against her temples. |
| 0xa44f9 | 49 | How do I put it... It was a pretty easy mistake\n |
| 0xa452b | 49 | to make, but I still feel a little sorry for her. |
| 0xa455d | 50 | It happened while we were out sightseeing in the\n |
| 0xa4590 | 19 | imperial capital... |
| 0xa45a4 | 44 | Hey Kuon, do you know what this place sells? |
| 0xa45d1 | 45 | It's a big shop facing the main street, but\n |
| 0xa45ff | 47 | I can't tell what kind of shop it is from the\n |
| 0xa462f | 17 | storefront alone. |
| 0xa4641 | 32 | Huh? Oh, this is a fabric store. |
| 0xa4662 | 42 | It says so on that signboard, right there. |
| 0xa468d | 13 | Signboard...? |
| 0xa469b | 40 | I peer at the signboard she's indicated. |
| 0xa46c4 | 47 | There certainly is something written on there\n |
| 0xa46f4 | 33 | with huge, blocky writing, but... |
| 0xa4716 | 50 | Well, I can't read it... Actually, what language\n |
| 0xa4749 | 14 | is this, even? |
| 0xa4758 | 7 | ...Huh? |
| 0xa4760 | 47 | I can't forget Nekone's face as she awkwardly\n |
| 0xa4790 | 45 | averted her eyes, or Kuon squeaking in shock. |
| 0xa47be | 48 | I never imagined that you might be illiterate... |
| 0xa47ef | 47 | You were able to read numbers, and you seemed\n |
| 0xa481f | 35 | good at arithmetic, so I thought... |
| 0xa4843 | 44 | I thought you might do well enough to be a\n |
| 0xa4870 | 46 | civil servant, but math or not, if you can't\n |
| 0xa489f | 12 | even read... |
| 0xa48ac | 37 | Urgh, my negligence is inexcusable... |
| 0xa48d2 | 42 | I don't think it's... my fault, exactly,\n |
| 0xa48fd | 45 | but I still feel... incredibly uncomfortable. |
| 0xa492b | 48 | W-Well, there's no helping it if I can't read.\n |
| 0xa495c | 46 | We just need to find work that I CAN do, then. |
| 0xa498b | 50 | I won't be picky. There's gotta be something out\n |
| 0xa49be | 41 | there. Like a seat warmer, or... flower\n |
| 0xa49e8 | 12 | arrangement. |
| 0xa49f5 | 45 | I'd rather not work in the first place, but\n |
| 0xa4a23 | 48 | they seem receptive to some suggestions at the\n |
| 0xa4a54 | 9 | moment... |
| 0xa4a5e | 48 | What nonsense are you spewing now? There is no\n |
| 0xa4a8f | 41 | way there would be such a convenient job. |
| 0xa4ab9 | 34 | We wouldn't know unless we looked. |
| 0xa4adc | 48 | I assure you, I know without looking. Just how\n |
| 0xa4b0d | 32 | lightly are you taking all this? |
| 0xa4b2e | 47 | Let us suppose there was such a job. How long\n |
| 0xa4b5e | 44 | would you search for it? What if you could\n |
| 0xa4b8b | 12 | not find it? |
| 0xa4b98 | 7 | Urgh... |
| 0xa4ba0 | 52 | Well, this is a fine mess. Haku isn't very strong,\n |
| 0xa4bd5 | 43 | so physical labor is out of the question... |
| 0xa4c01 | 49 | So he does not even have any redeeming physical\n |
| 0xa4c33 | 9 | skills... |
| 0xa4c3d | 31 | He really is utterly worthless. |
| 0xa4c5d | 50 | Urgh... I can't take this much pity. But they're\n |
| 0xa4c90 | 41 | not wrong... so I can't really talk back. |
| 0xa4cba | 29 | U-Um... In that case, then... |
| 0xa4cd8 | 3 | Hm? |
| 0xa4cdc | 26 | If... If you'd like, ah... |
| 0xa4cf7 | 8 | Y-You... |
| 0xa4d00 | 4 | You? |
| 0xa4d05 | 35 | You... can... a-at my estate, ah... |
| 0xa4d29 | 36 | Huh? Sorry, can't hear you too well. |
| 0xa4d4e | 37 | ...Well, I suppose we have no choice. |
| 0xa4d74 | 8 | ...Oh... |
| 0xa4d7d | 47 | Let's keep searching for a little while longer. |
| 0xa4dad | 42 | If we keep searching, and don't give up,\n |
| 0xa4dd8 | 33 | we'll find the right job someday. |
| 0xa4dfa | 30 | Oh... Well, sorry about this.  |
| 0xa4e19 | 37 | Don't worry about it. We've already\n |
| 0xa4e3f | 34 | started, so we can't back out now. |
| 0xa4e62 | 49 | Oh, right. What were you trying to say earlier?\n |
| 0xa4e94 | 29 | I couldn't hear you too well. |
| 0xa4eb2 | 26 | Uh... I-It's... nothing... |
| 0xa4ecd | 9 | You sure? |
| 0xa4ed7 | 35 | It didn't seem like it was nothing. |
| 0xa4efb | 22 | ...I don't understand. |
| 0xa4f12 | 48 | I cannot help but wonder why you do not simply\n |
| 0xa4f43 | 45 | abandon this stray dog of a man, dear sister. |
| 0xa4f71 | 51 | Why...? Well, I suppose you always feel obligated\n |
| 0xa4fa5 | 36 | to root for the underdog, don't you? |
| 0xa4fca | 9 | That's... |
| 0xa4fd4 | 47 | I understand. Certainly, then, we have a duty\n |
| 0xa5004 | 39 | to stand by the farthest under of dogs. |
| 0xa502c | 39 | Hey, am I allowed to get angry at that? |
| 0xa5054 | 47 | Dear sister. I did not want to tell you this,\n |
| 0xa5084 | 42 | but I have a message from my dear brother. |
| 0xa50af | 10 | From Ukon? |
| 0xa50ba | 48 | He said... "There's something I've got to tell\n |
| 0xa50eb | 48 | you. It may help, so I want you to come see me." |
| 0xa511c | 50 | It feels as though it might have something to do\n |
| 0xa514f | 20 | with this miscreant. |
| 0xa5164 | 47 | ...That's what Ukon says, hm? So he's already\n |
| 0xa5194 | 44 | getting to work... I expected as much from\n |
| 0xa51c1 | 13 | him, I think. |
| 0xa51cf | 38 | Er, do you know anything about this,\n |
| 0xa51f6 | 12 | dear sister? |
| 0xa5203 | 49 | Hm? No, not a thing. But I'm sure I can imagine\n |
| 0xa5235 | 37 | the sort of thing he'd propose to us. |
| 0xa525b | 42 | Heheh... Now I have to wonder what it is\n |
| 0xa5286 | 20 | he likes about Haku. |
| 0xa529b | 48 | Saying that, Kuon teasingly taps Nekone on the\n |
| 0xa52cc | 5 | nose. |
| 0xa52d2 | 36 | M-My dear brother does not like him. |
| 0xa52f7 | 30 | What, something wrong with me? |
| 0xa5316 | 43 | Ahahah... I believe it means that Ukon is\n |
| 0xa5342 | 24 | interested in you, Haku. |
| 0xa535b | 8 | ...Huh!? |
| 0xa5364 | 36 | B-But, uh, not in THAT sense, right? |
| 0xa5389 | 49 | Come to think of it, he did seem to hang around\n |
| 0xa53bb | 35 | real close for a lot of the time... |
| 0xa53df | 34 | What is this person talking about? |
| 0xa5402 | 37 | ...And now, once again, the classic\n |
| 0xa5428 | 36 | "are-you-some-kind-of-dung-beetle"\n |
| 0xa544d | 13 | Nekone stare. |
| 0xa545b | 45 | I wondered where she'd take us, but I think\n |
| 0xa5489 | 44 | this is the manor of the Imperial Guard of\n |
| 0xa54b6 | 10 | the Right. |
| 0xa54c1 | 48 | No doubt about it. We were just here yesterday\n |
| 0xa54f2 | 32 | to deliver Rulutieh's offerings. |
| 0xa5513 | 49 | The gatekeeper gives us a hard stare, but eases\n |
| 0xa5545 | 42 | up and bows his head when he sees Nekone\n |
| 0xa5570 | 9 | approach. |
| 0xa557a | 27 | Thank you for your service. |
| 0xa5596 | 42 | We then pass through the gate as if it's\n |
| 0xa55c1 | 43 | routine for us, and follow Nekone through\n |
| 0xa55ed | 14 | the corridors. |
| 0xa55fc | 49 | Judging from the other day, and how we were led\n |
| 0xa562e | 36 | here, is Ukon connected to this guy? |
| 0xa5653 | 48 | Nekone makes her way through the manor without\n |
| 0xa5684 | 47 | hesitation, and stops before a particular room. |
| 0xa56b4 | 32 | I have brought the both of them. |
| 0xa56d5 | 6 | Enter. |
| 0xa56dc | 46 | After Nekone calls out from just outside the\n |
| 0xa570b | 32 | door, a reply comes from within. |
| 0xa572c | 21 | We are coming in now. |
| 0xa5742 | 28 | The room seems like a study. |
| 0xa575f | 49 | Several picture scrolls and books are organized\n |
| 0xa5791 | 44 | and stacked, as if to emphasize the simple\n |
| 0xa57be | 12 | furnishings. |
| 0xa57cb | 41 | And sitting at the far end of the room... |
| 0xa57f5 | 7 | Hrm...! |
| 0xa57fd | 24 | How good of you to come. |
| 0xa5816 | 42 | The Imperial Guard of the Right... Oshtor. |
| 0xa5841 | 48 | It's that mysterious masked man... Oshtor, the\n |
| 0xa5872 | 36 | Imperial Guard of the Right himself. |
| 0xa5897 | 28 | Wait a second, why is he...? |
| 0xa58b4 | 46 | Well, this is his manor, obviously, but what\n |
| 0xa58e3 | 48 | happened to Ukon? He's the guy who called us in. |
| 0xa5914 | 46 | Lord Haku. Lady Kuon. Thank you for your aid\n |
| 0xa5943 | 52 | with the bandits. Allow me a formal introduction--\n |
| 0xa5978 | 12 | I am Oshtor. |
| 0xa5985 | 49 | I'm sure you must have questions regarding your\n |
| 0xa59b7 | 46 | sudden summons, but first, please have a seat. |
| 0xa59e6 | 32 | Nekone, some tea for our guests. |
| 0xa5a07 | 10 | Very well. |
| 0xa5a12 | 45 | Nekone bows to Oshtor and obediently leaves\n |
| 0xa5a40 | 9 | the room. |
| 0xa5a4a | 49 | So Nekone knew about this... Actually, I didn't\n |
| 0xa5a7c | 36 | even know that they knew each other. |
| 0xa5aa1 | 47 | I sit myself down on the comfortable cushion,\n |
| 0xa5ad1 | 20 | as Oshtor suggested. |
| 0xa5ae6 | 46 | Are we to reintroduce ourselves as well, then? |
| 0xa5b15 | 44 | If you wish. However, I do not require it.\n |
| 0xa5b42 | 47 | I mean no discourtesy, but my reports already\n |
| 0xa5b72 | 13 | tell me much. |
| 0xa5b80 | 7 | U-Um... |
| 0xa5b88 | 34 | Is it OK for me to be here too...? |
| 0xa5bab | 26 | If I'm in the way, then... |
| 0xa5bc6 | 50 | It is no trouble. Especially since this concerns\n |
| 0xa5bf9 | 31 | your father's request, as well. |
| 0xa5c19 | 15 | From Father...? |
| 0xa5c29 | 44 | Yes. He asked that I ensure his daughter's\n |
| 0xa5c56 | 8 | welfare. |
| 0xa5c5f | 15 | Father asked... |
| 0xa5c6f | 50 | ...I don't get it. I thought Ukon called for us,\n |
| 0xa5ca2 | 45 | but here's this guy instead. Now Rulutieh's\n |
| 0xa5cd0 | 9 | involved? |
| 0xa5cda | 23 | I have brought the tea. |
| 0xa5cf2 | 46 | Nekone begins placing the cups of tea on the\n |
| 0xa5d21 | 6 | table. |
| 0xa5d28 | 47 | And after she's arranged everything, she sits\n |
| 0xa5d58 | 40 | at Oshtor's side with a matter-of-fact\n |
| 0xa5d81 | 11 | expression. |
| 0xa5d8d | 48 | ...There's something weirdly... ceremonial, or\n |
| 0xa5dbe | 43 | prim, about all this. It's freaking me out. |
| 0xa5dea | 46 | She didn't seem to like being lumped in with\n |
| 0xa5e19 | 43 | the screaming girls... I guess this is why. |
| 0xa5e45 | 22 | ...This is quite good. |
| 0xa5e5c | 21 | It is very delicious. |
| 0xa5e72 | 10 | Thank you. |
| 0xa5e7d | 45 | I pick up the cup placed before me and take\n |
| 0xa5eab | 6 | a sip. |
| 0xa5eb2 | 23 | ...Gah, that's bitter!! |
| 0xa5eca | 26 | I almost spit it back out. |
| 0xa5ee5 | 33 | What is this? It's really bitter. |
| 0xa5f07 | 46 | I can't help but furtively glance between my\n |
| 0xa5f36 | 24 | tea and everyone else's. |
| 0xa5f4f | 42 | ...Everyone seems to be enjoying theirs... |
| 0xa5f7a | 46 | ...Ah, well, we need to stick to the subject\n |
| 0xa5fa9 | 16 | for now, anyway. |
| 0xa5fba | 38 | ...So, what does the top brass want,\n |
| 0xa5fe1 | 20 | calling us out here? |
| 0xa5ff6 | 41 | Hrm. As I expected, you do not care for\n |
| 0xa6020 | 42 | roundabout discussions. Allow me to come\n |
| 0xa604b | 22 | straight to the point. |
| 0xa6062 | 45 | I invited you here for one reason. It is my\n |
| 0xa6090 | 29 | intent to become your patron. |
| 0xa60ae | 46 | Patron...? Does that mean you want to hire us? |
| 0xa60dd | 47 | You may think of it that way if it pleases you. |
| 0xa610d | 47 | So... you're asking us to be your subordinates? |
| 0xa613d | 48 | Correct. Although I would not wish so formal a\n |
| 0xa616e | 43 | hierarchy. I propose instead a partnership. |
| 0xa619a | 14 | Partnership... |
| 0xa61a9 | 46 | What does this mean? From what I heard, this\n |
| 0xa61d8 | 25 | guy is a pretty big deal. |
| 0xa61f2 | 46 | And a person like that wants to hire a bunch\n |
| 0xa6221 | 20 | of nobodies like us? |
| 0xa6236 | 33 | This seems... incomprehensible.\n |
| 0xa6258 | 17 | In a lot of ways. |
| 0xa626a | 47 | Though it could be that he wants us to do his\n |
| 0xa629a | 38 | dirty work, or he wants to use us as\n |
| 0xa62c1 | 19 | disposable pawns... |
| 0xa62d5 | 45 | But if that was his angle, then he wouldn't\n |
| 0xa6303 | 27 | reveal his identity, right? |
| 0xa631f | 42 | I honestly don't have any idea what he's\n |
| 0xa634a | 10 | plotting.  |
| 0xa6355 | 29 | I exchange glances with Kuon. |
| 0xa6373 | 45 | But Kuon remains silent, an amused smile on\n |
| 0xa63a1 | 9 | her face. |
| 0xa63ab | 44 | I don't get why she isn't saying anything... |
| 0xa63d8 | 49 | Knowing Kuon, I figure she'd jump at the chance\n |
| 0xa640a | 38 | to start some cutthroat negotiation... |
| 0xa6431 | 26 | Does it seem that strange? |
| 0xa644c | 46 | Oshtor breaks the silence a bit abruptly, as\n |
| 0xa647b | 30 | though sensing our hesitation. |
| 0xa649a | 44 | This isn't just strange. It's TOO strange.\n |
| 0xa64c7 | 45 | Someone in your position should have plenty\n |
| 0xa64f5 | 17 | of pawns already. |
| 0xa6507 | 49 | But here you are, inviting a bunch of strangers\n |
| 0xa6539 | 48 | into your retinue. It'd be weird if we WEREN'T\n |
| 0xa656a | 11 | suspicious. |
| 0xa6576 | 44 | I'd think it's only natural we'd think you\n |
| 0xa65a3 | 24 | were plotting something. |
| 0xa65bc | 46 | What? Don't give me that look. It's not like\n |
| 0xa65eb | 18 | I could help it... |
| 0xa65fe | 49 | Hrm. I suppose it is only natural to reach such\n |
| 0xa6630 | 13 | a conclusion. |
| 0xa663e | 50 | I am afraid you will have to take me at my word,\n |
| 0xa6671 | 34 | but I am not trying to set you up. |
| 0xa6694 | 46 | For certain reasons, I have been looking for\n |
| 0xa66c3 | 22 | someone I can rely on. |
| 0xa66da | 41 | And not a simple subordinate... Someone\n |
| 0xa6704 | 42 | unaffiliated, who will speak frankly and\n |
| 0xa672f | 15 | openly with me. |
| 0xa673f | 35 | Yet I could find no such confidant. |
| 0xa6763 | 46 | So when I consulted my friend regarding this\n |
| 0xa6792 | 44 | matter--another partner--he recommended you. |
| 0xa67bf | 43 | Oshtor pauses a moment to sip at his tea,\n |
| 0xa67eb | 22 | and continues talking. |
| 0xa6802 | 51 | I have heard of your efforts in the extermination\n |
| 0xa6836 | 50 | of the gigiri, and the suppression of the bandits. |
| 0xa6869 | 46 | A fine apothecary of keen mind and reflex...\n |
| 0xa6898 | 44 | A man who, strength aside, has a quick wit\n |
| 0xa68c5 | 20 | and an odd charisma. |
| 0xa68da | 44 | I can understand the parts about Kuon, but\n |
| 0xa6907 | 40 | I get the feeling I'm being overrated... |
| 0xa6930 | 48 | He has not been with you long, but he declares\n |
| 0xa6961 | 43 | you reliable--that you together withstood\n |
| 0xa698d | 13 | mortal peril. |
| 0xa699b | 48 | A friend... Oh right, Ukon... So that's what's\n |
| 0xa69cc | 14 | going on here. |
| 0xa69db | 41 | Maroro was most happy to vouch for you.\n |
| 0xa6a05 | 42 | I concluded that if he spoke true, there\n |
| 0xa6a30 | 20 | could be no mistake. |
| 0xa6a45 | 42 | ...It was Maroro!? Then where did Ukon go? |
| 0xa6a70 | 22 | Ah, this is delicious. |
| 0xa6a87 | 47 | Kuon sips her tea without a care as she smiles. |
| 0xa6ab7 | 9 | Though... |
| 0xa6ac1 | 50 | Honestly, I figure I woulda done it even without\n |
| 0xa6af4 | 11 | his say-so. |
| 0xa6b00 | 13 | Oshtor grins. |
| 0xa6b0e | 45 | What the--His speech and his whole demeanor\n |
| 0xa6b3c | 39 | feel totally different... But there's\n |
| 0xa6b64 | 20 | something familiar-- |
| 0xa6b79 | 45 | What, you still haven't connected the dots?\n |
| 0xa6ba7 | 46 | That's cold, man. And here I thought we were\n |
| 0xa6bd6 | 8 | friends. |
| 0xa6bdf | 8 | ...What? |
| 0xa6be8 | 48 | Well, let me answer your other question, then.\n |
| 0xa6c19 | 39 | Where did Ukon go? That was it, right?  |
| 0xa6c41 | 46 | With a smile on his face, Oshtor tousles his\n |
| 0xa6c70 | 45 | hair, and dons another aperyu he pulls from\n |
| 0xa6c9e | 10 | somewhere. |
| 0xa6ca9 | 49 | Then, he puts his hands to his mouth, and in an\n |
| 0xa6cdb | 44 | instant, he's got a stubbly-looking beard... |
| 0xa6d08 | 42 | Then finally, he slowly removes the mask\n |
| 0xa6d33 | 20 | covering his eyes... |
| 0xa6d48 | 15 | I'm right here. |
| 0xa6d58 | 11 | ...U-Ukon!? |
| 0xa6d64 | 46 | Yep. Ukon's my secret identity. And the real\n |
| 0xa6d93 | 47 | identity is Oshtor, the Imperial Guard of the\n |
| 0xa6dc3 | 6 | Right. |
| 0xa6dca | 23 | Heheheh...... Ahahahah! |
| 0xa6de2 | 46 | I can hear Kuon's laughter from beside me as\n |
| 0xa6e11 | 31 | she tries in vain to stifle it. |
| 0xa6e31 | 47 | I look over to Kuon--shoulders shaking, mouth\n |
| 0xa6e61 | 43 | covered--and Rulutieh looking between us,\n |
| 0xa6e8d | 10 | flustered. |
| 0xa6e98 | 16 | Don't tell me... |
| 0xa6ea9 | 47 | So Kuon knew from the beginning... And by her\n |
| 0xa6ed9 | 44 | expression, she was just enjoying watching\n |
| 0xa6f06 | 14 | this play out. |
| 0xa6f15 | 45 | Nekone grumpily shoots a sidelong glance at\n |
| 0xa6f43 | 7 | Oshtor. |
| 0xa6f4b | 50 | And Nekone obviously knew as well... I guess she\n |
| 0xa6f7e | 44 | doesn't really approve of these shenanigans. |
| 0xa6fab | 47 | Rulutieh seems to be more perplexed by Kuon's\n |
| 0xa6fdb | 47 | laughter than actually being surprised by this. |
| 0xa700b | 42 | Did you know about this as well, Rulutieh? |
| 0xa7036 | 49 | Huh? Oh, yes... I was told about it in the very\n |
| 0xa7068 | 12 | beginning... |
| 0xa7075 | 43 | What? The kid was the only one surprised?\n |
| 0xa70a1 | 43 | The missy saw through it, eh... I thought\n |
| 0xa70cd | 10 | I had you. |
| 0xa70d8 | 45 | Ukon lets out an obviously disappointed sigh. |
| 0xa7106 | 47 | So, what gave it away? I was pretty confident\n |
| 0xa7136 | 25 | in this disguise, y'know. |
| 0xa7150 | 43 | In fact, only a few people know about this. |
| 0xa717c | 45 | You were watching Nekone during the patrol,\n |
| 0xa71aa | 12 | weren't you? |
| 0xa71b7 | 50 | Yeah, she seemed like she was having a real good\n |
| 0xa71ea | 42 | time with the kid. I couldn't help myself. |
| 0xa7215 | 48 | N-No, I was not playing with him. I was trying\n |
| 0xa7246 | 23 | to defend your honor... |
| 0xa725e | 22 | Sure, hokay, I get it. |
| 0xa7275 | 28 | You certainly do NOT get it! |
| 0xa7292 | 11 | Those eyes. |
| 0xa729e | 3 | Oh? |
| 0xa72a2 | 44 | Those kind eyes that were watching Nekone.\n |
| 0xa72cf | 29 | They were the same as Ukon's. |
| 0xa72ed | 27 | Hunh. Well, uh... I... see. |
| 0xa7309 | 47 | And however beloved Oshtor may be, I found it\n |
| 0xa7339 | 48 | odd that Nekone would be so infatuated with him. |
| 0xa736a | 45 | It was almost like her attitude towards her\n |
| 0xa7398 | 47 | older brother... And I think that made it all\n |
| 0xa73c8 | 6 | clear. |
| 0xa73cf | 46 | Cripes. You really are a sharp one, Missy...\n |
| 0xa73fe | 37 | ah, but we're gettin' off-track here. |
| 0xa7424 | 48 | So, you know I was granted the undeserved rank\n |
| 0xa7455 | 43 | of the Imperial Guard of the Right by the\n |
| 0xa7481 | 7 | Mikado. |
| 0xa7489 | 46 | If I say so myself, the Imperial Guard is an\n |
| 0xa74b8 | 40 | extremely important official position... |
| 0xa74e1 | 48 | ...One whose duty is to protect the Mikado and\n |
| 0xa7512 | 46 | the citizens of Yamato from all kinds of harm. |
| 0xa7541 | 43 | Honestly? I have no idea how I got the job. |
| 0xa756d | 44 | Ukon scratches his head, looking comically\n |
| 0xa759a | 24 | bewildered for a moment. |
| 0xa75b3 | 50 | Of course, it comes with a huge amount of power.\n |
| 0xa75e6 | 41 | I can command entire armies if I have to. |
| 0xa7610 | 49 | But that means it's hard for me to move freely.\n |
| 0xa7642 | 43 | What with my title, I get all this public\n |
| 0xa766e | 10 | attention. |
| 0xa7679 | 47 | Which is why you're hiding your true identity\n |
| 0xa76a9 | 10 | like that? |
| 0xa76b4 | 47 | You got it. I'm kind of paralyzed like this--\n |
| 0xa76e4 | 46 | or... like everything I do turns into a huge\n |
| 0xa7713 | 11 | production. |
| 0xa771f | 49 | You guys saw, right? I just wanted a quick look\n |
| 0xa7751 | 43 | around the city, and suddenly it's a damn\n |
| 0xa777d | 7 | parade. |
| 0xa7785 | 47 | That is an obligation that befits your station. |
| 0xa77b5 | 46 | Yeah, true. I understand that--really, I do,\n |
| 0xa77e4 | 46 | but... I can't hear the voices of the people\n |
| 0xa7813 | 10 | as Oshtor. |
| 0xa781e | 45 | If I wanna hear what the people are saying,\n |
| 0xa784c | 44 | just changing my appearance isn't going to\n |
| 0xa7879 | 7 | cut it. |
| 0xa7881 | 43 | Sometimes I have to go into shady places.\n |
| 0xa78ad | 44 | Sometimes I end up having to deceive people. |
| 0xa78da | 46 | And I've gotta be prepared to shoulder those\n |
| 0xa7909 | 8 | crimes.  |
| 0xa7912 | 49 | So I needed another identity. One that can move\n |
| 0xa7944 | 48 | freely by deceiving the public's eyes like this. |
| 0xa7975 | 47 | So you're saying, now that you're famous, you\n |
| 0xa79a5 | 48 | can't partake in all the shady things you like\n |
| 0xa79d6 | 8 | to do... |
| 0xa79df | 47 | So you came up with this disguise as a way to\n |
| 0xa7a0f | 39 | let you keep having your illegal fun.\n |
| 0xa7a37 | 11 | Is that it? |
| 0xa7a43 | 24 | Have another cup of tea. |
| 0xa7a5c | 5 | Hm?\n |
| 0xa7a62 | 11 | Oh, thanks. |
| 0xa7a6e | 15 | Bleaghaaaah!!\n |
| 0xa7a7e | 19 | Yargh, that's HOT-- |
| 0xa7a92 | 46 | Wh-Why, that little--She just full-on dumped\n |
| 0xa7ac1 | 21 | hot water on my head! |
| 0xa7ad7 | 43 | Here are some crumpets to go with your tea. |
| 0xa7b03 | 6 | *Stab* |
| 0xa7b0a | 14 | Hrgheeeegh!!\n |
| 0xa7b19 | 25 | M-My eyes... I can't see! |
| 0xa7b33 | 35 | Th-The crumpets... are in my eyes!! |
| 0xa7b57 | 32 | I flail helplessly on the floor. |
| 0xa7b78 | 49 | Wh-What the hell are you doing, you little brat!? |
| 0xa7baa | 45 | Oh, you would like some more? By all means.\n |
| 0xa7bd8 | 13 | Here you are. |
| 0xa7be6 | 17 | Bleeerghaaaargh!! |
| 0xa7bf8 | 43 | It serves you right for insulting my dear\n |
| 0xa7c24 | 10 | brother... |
| 0xa7c2f | 48 | What the heck did you do that for!? And what's\n |
| 0xa7c60 | 30 | with these weird accusations!? |
| 0xa7c7f | 47 | Who is the one that suggested my dear brother\n |
| 0xa7caf | 39 | was partaking in suspicious activities? |
| 0xa7cd7 | 43 | My dear brother would never lower himself\n |
| 0xa7d03 | 23 | to such base indecency! |
| 0xa7d1b | 49 | How do you even decide what's decent and what's\n |
| 0xa7d4d | 46 | not? And your brother isn't indecent, you say? |
| 0xa7d7c | 47 | But of course. My dear brother would never be\n |
| 0xa7dac | 31 | driven by such impure impulses. |
| 0xa7dcc | 50 | That's ridiculous. There's no way a man wouldn't\n |
| 0xa7dff | 48 | think indecent thoughts. That's just delusional! |
| 0xa7e30 | 49 | Man or woman, the three primal desires will not\n |
| 0xa7e62 | 10 | be denied! |
| 0xa7e6d | 49 | I declare triumphantly, sternly pointing at her\n |
| 0xa7e9f | 45 | from the floor. I hear someone snickering...? |
| 0xa7ecd | 27 | Th-Three primal... desires? |
| 0xa7ee9 | 50 | What, you don't know? The desires for sleep, for\n |
| 0xa7f1c | 47 | food, and for sex. Nobody can possibly escape\n |
| 0xa7f4c | 5 | them! |
| 0xa7f52 | 5 | Se... |
| 0xa7f58 | 42 | Taken aback, Nekone's face turns several\n |
| 0xa7f83 | 14 | shades redder. |
| 0xa7f92 | 43 | She's trying to muster a comeback, but it\n |
| 0xa7fbe | 32 | seems she's at a loss for words. |
| 0xa7fdf | 49 | You blushed when you saw Oshtor earlier, right?\n |
| 0xa8011 | 47 | That's no different from an extension of your\n |
| 0xa8041 | 7 | desire! |
| 0xa8049 | 15 | Wh... Wh-Wha... |
| 0xa8059 | 50 | Wait, what? Oshtor and Ukon are the same person,\n |
| 0xa808c | 49 | so... Holy crap. He's your brother, and you're... |
| 0xa80be | 19 | Wha...! Wh-Wha...!! |
| 0xa80d2 | 38 | Just saying. That's kind of messed up. |
| 0xa80f9 | 7 | Wwwh... |
| 0xa8101 | 5 | Wwwh? |
| 0xa8107 | 11 | Wwhhaa...!! |
| 0xa8113 | 11 | Grhaaargh!! |
| 0xa811f | 40 | Dear brother, this simply will NOT do!\n |
| 0xa8148 | 41 | It is no good! A man of such despicable\n |
| 0xa8172 | 22 | character is no good!! |
| 0xa8189 | 16 | Daaaaahahahahah! |
| 0xa819a | 45 | I glance over to see Ukon holding his sides\n |
| 0xa81c8 | 42 | with laughter, and Kuon trying to stifle\n |
| 0xa81f3 | 18 | her own amusement. |
| 0xa8206 | 49 | Though it seems Rulutieh is trying to stop her... |
| 0xa8238 | 33 | Ukon, quit laughing and stop her! |
| 0xa825a | 48 | Ho boy, what a shock. Nekone's usually so shy!\n |
| 0xa828b | 45 | I never figured she'd get attached this fast. |
| 0xa82b9 | 25 | I am NOT attached to him! |
| 0xa82d3 | 41 | What could possibly have given you that\n |
| 0xa82fd | 43 | impression!? Look, level with me--are you\n |
| 0xa8329 | 6 | blind? |
| 0xa8330 | 45 | I believe I told you not to speak ill of my\n |
| 0xa835e | 8 | brother! |
| 0xa8367 | 45 | She begins another assault with the boiling\n |
| 0xa8395 | 20 | water in the teapot. |
| 0xa83aa | 37 | Ow, that's HOT! Would you stop that-- |
| 0xa83d0 | 15 | Daaahahahaha... |
| 0xa83e0 | 35 | And YOU! Quit laughing and help--\n |
| 0xa8404 | 11 | Yargh, hot! |
| 0xa8410 | 52 | Hoo, that really got me... Nekone, give it a rest,\n |
| 0xa8445 | 45 | huh? The kid's an important guest, after all. |
| 0xa8473 | 8 | Hrmph... |
| 0xa847c | 51 | Being told that, Nekone shoots me a venomous look\n |
| 0xa84b0 | 24 | and returns to her seat. |
| 0xa84c9 | 41 | Sheesh, that was a terrible experience... |
| 0xa84f3 | 46 | Well, forgive her, eh? She's been a bookworm\n |
| 0xa8522 | 41 | since she was little. She's not used to\n |
| 0xa854c | 12 | socializing. |
| 0xa8559 | 17 | D-Dear brother... |
| 0xa856b | 36 | Now, what were we talking about...\n |
| 0xa8590 | 36 | Right, all that suspicious business. |
| 0xa85b5 | 44 | Nekone might have gotten herself worked up\n |
| 0xa85e2 | 43 | about it, but what you said wasn't really\n |
| 0xa860e | 6 | wrong. |
| 0xa8615 | 44 | My other identity's meant to do things the\n |
| 0xa8642 | 36 | Imperial Guard of the Right can't.\n |
| 0xa8667 | 19 | Like break the law. |
| 0xa867b | 46 | I only wanted to be a soldier who helped the\n |
| 0xa86aa | 44 | people--sharing in their joys and sorrows,\n |
| 0xa86d7 | 16 | like my dad did. |
| 0xa86e8 | 49 | With that ambition, I set out from the boonies.\n |
| 0xa871a | 47 | Thanks to the help of my old mentor, I became\n |
| 0xa874a | 22 | a rank-and-file guard. |
| 0xa8761 | 46 | Then, through a bunch of good luck and weird\n |
| 0xa8790 | 44 | coincidences, I rose up through the ranks,\n |
| 0xa87bd | 6 | but... |
| 0xa87c4 | 45 | Dunno where or how it happened, but somehow\n |
| 0xa87f2 | 46 | I ended up being named the Imperial Guard of\n |
| 0xa8821 | 47 | I worked hard to get ahead so I could go home\n |
| 0xa8851 | 49 | with my head high, but I never imagined I'd end\n |
| 0xa8883 | 17 | up with all this. |
| 0xa8895 | 46 | To be honest, it wasn't even my intention to\n |
| 0xa88c4 | 27 | get such a big fancy title. |
| 0xa88e0 | 51 | If certain people heard that, they would probably\n |
| 0xa8914 | 48 | cry and throw a shameless tantrum on the spot... |
| 0xa8945 | 48 | I don't think it's a position one can get only\n |
| 0xa8976 | 43 | with coincidence, luck, and minimal effort. |
| 0xa89a2 | 49 | Haha... Well, however it happened, the Imperial\n |
| 0xa89d4 | 48 | Guard of the Right can't share in the people's\n |
| 0xa8a05 | 5 | joys. |
| 0xa8a0b | 46 | The most I can do is patrol the city. I only\n |
| 0xa8a3a | 49 | caught the bandits by working with the imperial\n |
| 0xa8a6c | 7 | guards. |
| 0xa8a74 | 47 | If you have that much power, why don't you do\n |
| 0xa8aa4 | 43 | whatever you want and not worry about the\n |
| 0xa8ad0 | 8 | details? |
| 0xa8ad9 | 49 | You understand nothing. If that were an option,\n |
| 0xa8b0b | 35 | we would not be having these talks. |
| 0xa8b2f | 46 | As the Imperial Guard of the Right, Yamato's\n |
| 0xa8b5e | 48 | prestige rests upon my dear brother's shoulders. |
| 0xa8b8f | 41 | If my dear brother moves, Yamato moves.\n |
| 0xa8bb9 | 43 | Warriors gather if he calls, and soldiers\n |
| 0xa8be5 | 17 | ride if he rides. |
| 0xa8bf7 | 31 | He cannot move about so easily. |
| 0xa8c17 | 42 | That is why we are in our present state,\n |
| 0xa8c42 | 43 | with no choice but to leave various tasks\n |
| 0xa8c6e | 16 | to other people. |
| 0xa8c7f | 46 | I don't really understand, but it seems like\n |
| 0xa8cae | 18 | a load of trouble. |
| 0xa8cc1 | 43 | S'pose so. That's the reason I became Ukon. |
| 0xa8ced | 45 | I've exposed corrupt officials, fought with\n |
| 0xa8d1b | 45 | thugs, cracked down on thieves... all kinds\n |
| 0xa8d49 | 9 | of stuff. |
| 0xa8d53 | 47 | ...I get all choked up when I think of how my\n |
| 0xa8d83 | 46 | father watched over the lives of the people,\n |
| 0xa8db2 | 6 | too... |
| 0xa8db9 | 43 | ...But even that's been getting difficult\n |
| 0xa8de5 | 14 | recently, too. |
| 0xa8df4 | 50 | I've done too much, and now even Ukon's starting\n |
| 0xa8e27 | 23 | to become widely known. |
| 0xa8e3f | 46 | Recently, folks have been snooping around...\n |
| 0xa8e6e | 44 | and now if I do anything else, I might get\n |
| 0xa8e9b | 10 | found out. |
| 0xa8ea6 | 47 | So now I can't cause any huge ruckus like I'm\n |
| 0xa8ed6 | 45 | used to doing. Probably time I call it quits. |
| 0xa8f04 | 30 | Wait, he isn't going to ask... |
| 0xa8f23 | 36 | I see. So that's what this is about. |
| 0xa8f48 | 45 | This is just a wild guess... but you aren't\n |
| 0xa8f76 | 43 | going to tell us to do that stuff in your\n |
| 0xa8fa2 | 13 | place, right? |
| 0xa8fb0 | 45 | Ukon grins, as though he's been waiting for\n |
| 0xa8fde | 12 | those words. |
| 0xa8feb | 45 | You catch on quick. Just as I expected from\n |
| 0xa9019 | 9 | you, kid. |
| 0xa9023 | 46 | I want the kid to take over Ukon's duty, and\n |
| 0xa9052 | 50 | protect the people and the capital as undercover\n |
| 0xa9085 | 7 | agents. |
| 0xa908d | 44 | We haven't known each other for that long,\n |
| 0xa90ba | 21 | but I trust you guys. |
| 0xa90d0 | 49 | Hmhm... You have an awfully high opinion of Haku. |
| 0xa9102 | 49 | Well, I might not look it, but I'm a good judge\n |
| 0xa9134 | 38 | of character. So how about you, Missy? |
| 0xa915b | 24 | How about me, indeed...? |
| 0xa9174 | 45 | Hold it, hold it! This is all way too sudden. |
| 0xa91a2 | 19 | ...This isn't good. |
| 0xa91b6 | 48 | I had a bad feeling about this from the start.\n |
| 0xa91e7 | 42 | This guy's planning on putting me to work. |
| 0xa9212 | 49 | I just wanted to lead an idle life for a while... |
| 0xa9244 | 40 | So, what kind of jobs are you planning\n |
| 0xa926d | 25 | on making us amateurs do? |
| 0xa9287 | 48 | Oh, easy stuff. Patrols, tidying up... there's\n |
| 0xa92b8 | 46 | cleaning the gutters, or exterminating pests\n |
| 0xa92e7 | 14 | like before... |
| 0xa92f6 | 47 | Wait, what's with that "tidying" and cleaning\n |
| 0xa9326 | 12 | the gutters? |
| 0xa9333 | 49 | Hm? Oh, I do whatever's requested. If anything,\n |
| 0xa9365 | 43 | those jobs show up more than anything else. |
| 0xa9391 | 15 | There's also... |
| 0xa93a1 | 29 | He hesitates for some reason. |
| 0xa93bf | 10 | What else? |
| 0xa93ca | 37 | Well, there's plenty of other things. |
| 0xa93f0 | 42 | I guess he's telling us to figure it out\n |
| 0xa941b | 10 | ourselves? |
| 0xa9426 | 46 | He mentioned something about crime, so there\n |
| 0xa9455 | 41 | should also be dangerous, illegal stuff\n |
| 0xa947f | 18 | included in there. |
| 0xa9492 | 49 | Though that gigiri extermination and the bandit\n |
| 0xa94c4 | 46 | suppression were unexpected, there were some\n |
| 0xa94f3 | 11 | casualties. |
| 0xa94ff | 45 | It's the triple threat of tough, dirty, and\n |
| 0xa952d | 12 | dangerous... |
| 0xa953a | 50 | So on top of being forced to work, I'd be saying\n |
| 0xa956d | 28 | goodbye to my peaceful life? |
| 0xa958a | 33 | No chance. Yep. No chance at all. |
| 0xa95ac | 40 | I'm not cut out for the violent stuff.\n |
| 0xa95d5 | 46 | I know you wanted to rely on us, but... sorry. |
| 0xa9604 | 18 | So, how's the pay? |
| 0xa9617 | 4 | Wh-- |
| 0xa961c | 43 | You... what are you asking him, with that\n |
| 0xa9648 | 18 | unconcerned smile? |
| 0xa965b | 7 | Nekone. |
| 0xa9663 | 50 | Ignoring my confusion, Ukon looks to his sister,\n |
| 0xa9696 | 46 | who pulls out a small bag and sets it on her\n |
| 0xa96c5 | 5 | tray. |
| 0xa96cb | 46 | First off, this oughta cover initial expenses. |
| 0xa96fa | 46 | Ukon opens the small bag and empties some of\n |
| 0xa9729 | 36 | the gleaming contents onto the tray. |
| 0xa974e | 29 | You're being awfully careful. |
| 0xa976c | 39 | Unmarked gold leaves less of a trail.\n |
| 0xa9794 | 41 | We gotta take our security where we can\n |
| 0xa97be | 7 | get it. |
| 0xa97c6 | 46 | Use this funding to secure your post or hire\n |
| 0xa97f5 | 17 | some extra hands. |
| 0xa9807 | 47 | Succeeding Ukon or not, it'd be tough for you\n |
| 0xa9837 | 40 | and the missy to start out with nothing. |
| 0xa9860 | 24 | All right. We'll accept. |
| 0xa9879 | 7 | ...Hey! |
| 0xa9881 | 13 | What's wrong? |
| 0xa988f | 43 | Don't "what's wrong" me! You can't accept\n |
| 0xa98bb | 40 | something that easily without thinking\n |
| 0xa98e4 | 9 | about it. |
| 0xa98ee | 41 | Don't worry. It might not seem like it,\n |
| 0xa9918 | 34 | but I have thought things through. |
| 0xa993b | 45 | ...I don't know if that should make me even\n |
| 0xa9969 | 15 | MORE worried... |
| 0xa9979 | 47 | I know I'm the one who asked, but you're sure\n |
| 0xa99a9 | 49 | about this? I'm sure you can already tell, but... |
| 0xa99db | 42 | Are you talking about the expenses budget? |
| 0xa9a06 | 46 | ...Gah, should've figured you'd pick up on it. |
| 0xa9a35 | 47 | Well, it would be more than enough if we were\n |
| 0xa9a65 | 37 | to accept this as an advance payment. |
| 0xa9a8b | 49 | But if it's intended to outfit an entire group,\n |
| 0xa9abd | 47 | it's a bit short, no matter how I calculate it. |
| 0xa9aed | 8 | Right... |
| 0xa9af6 | 41 | Ukon scratches his disheveled hair in a\n |
| 0xa9b20 | 16 | familiar motion. |
| 0xa9b31 | 39 | But it's all I can offer at the moment. |
| 0xa9b59 | 45 | 'Cause it isn't official employment through\n |
| 0xa9b87 | 44 | the court, see. That's all coming outta my\n |
| 0xa9bb4 | 7 | pocket. |
| 0xa9bbc | 45 | Hmm. We're in a bit of a bind if that's the\n |
| 0xa9bea | 36 | case. Though I don't mind that much. |
| 0xa9c0f | 45 | Hey, why are you accepting this so easily!?\n |
| 0xa9c3d | 37 | That's a real hasty commitment there! |
| 0xa9c63 | 49 | Well, it sounds interesting. I've always wanted\n |
| 0xa9c95 | 39 | to try this sort of... undercover work. |
| 0xa9cbd | 49 | Working behind the scenes, carrying out orders,\n |
| 0xa9cef | 44 | hidden among the public. There's something\n |
| 0xa9d1c | 16 | cool about that. |
| 0xa9d2d | 18 | "Cool"? Come on... |
| 0xa9d40 | 43 | I know it's unreasonable, but is this OK?\n |
| 0xa9d6c | 46 | We haven't negotiated pay yet. It's not like\n |
| 0xa9d9b | 11 | you, missy. |
| 0xa9da7 | 50 | What, he brought this to us KNOWING it's totally\n |
| 0xa9dda | 13 | unreasonable? |
| 0xa9de8 | 46 | It's fine. I couldn't pass up something this\n |
| 0xa9e17 | 23 | interesting, after all. |
| 0xa9e2f | 40 | I'm tired of coming up with comebacks... |
| 0xa9e58 | 40 | Thank you, Lady Kuon. I am in your debt. |
| 0xa9e81 | 45 | With a grave look, Ukon bows low, as though\n |
| 0xa9eaf | 47 | observing the formality as the Imperial Guard\n |
| 0xa9edf | 13 | of the Right. |
| 0xa9eed | 23 | Thank you, dear sister. |
| 0xa9f05 | 50 | Nekone bows just as Ukon does. It's plain to see\n |
| 0xa9f38 | 35 | her overflowing adoration for Kuon. |
| 0xa9f5c | 43 | Well, that being the case... Lady Rulutieh. |
| 0xa9f88 | 13 | Huh... Y-Yes? |
| 0xa9f96 | 49 | Rulutieh, who had only been an outside listener\n |
| 0xa9fc8 | 43 | until now, turns red at the sudden direct\n |
| 0xa9ff4 | 8 | address. |
| 0xa9ffd | 48 | As you have heard, I will be leaving my duties\n |
| 0xaa02e | 28 | to Lady Kuon and the others. |
| 0xaa04b | 8 | Y-Yes... |
| 0xaa054 | 33 | And I am thinking of asking you\n |
| 0xaa076 | 28 | to help them, Lady Rulutieh. |
| 0xaa093 | 5 | What? |
| 0xaa099 | 6 | Me...? |
| 0xaa0a0 | 45 | Yes. A suggestion to that effect was in the\n |
| 0xaa0ce | 48 | owlo of Kujyuri's letter... the one I received\n |
| 0xaa0ff | 9 | from you. |
| 0xaa109 | 49 | Lord Ozen wrote that out of great love for you,\n |
| 0xaa13b | 46 | he feels as though he kept you trapped, like\n |
| 0xaa16a | 13 | a caged bird. |
| 0xaa178 | 49 | Thus, while you remain in the capital, he would\n |
| 0xaa1aa | 39 | have you meet others and broaden your\n |
| 0xaa1d2 | 11 | experience. |
| 0xaa1de | 15 | Father said...? |
| 0xaa1ee | 45 | I see no better chance than this. It may be\n |
| 0xaa21c | 42 | hard, but a storm can prove the strength\n |
| 0xaa247 | 15 | of one's wings. |
| 0xaa257 | 36 | ...Yes... I also... wish to do that. |
| 0xaa27c | 48 | So, with that said, can I ask you to take care\n |
| 0xaa2ad | 26 | of Lady Rulutieh too, kid? |
| 0xaa2c8 | 45 | Hey, hold on! Now he's just dumping all the\n |
| 0xaa2f6 | 41 | stuff he doesn't want to deal with on us! |
| 0xaa320 | 50 | It makes it worse that I can't say that in front\n |
| 0xaa353 | 14 | of Rulutieh... |
| 0xaa362 | 48 | Sir Haku... Miss Kuon... It will be a pleasure\n |
| 0xaa393 | 17 | working with you. |
| 0xaa3a5 | 20 | Rulutieh bows to us. |
| 0xaa3ba | 26 | Mhm. I look forward to it. |
| 0xaa3d5 | 36 | Kuon shakes Rulutieh's hand happily. |
| 0xaa3fa | 46 | Her face holds a cordial smile, but her tail\n |
| 0xaa429 | 17 | sways vigorously. |
| 0xaa43b | 44 | It seems she approves of all this business\n |
| 0xaa468 | 22 | with Rulutieh joining. |
| 0xaa47f | 47 | That bastard... Just offhandedly asking us to\n |
| 0xaa4af | 22 | look after a princess. |
| 0xaa4c6 | 45 | I glare at Ukon, making sure Rulutieh can't\n |
| 0xaa4f4 | 7 | see me. |
| 0xaa4fc | 45 | Well now, I don't know if it'll make up for\n |
| 0xaa52a | 42 | much, but I'll have this one join you too. |
| 0xaa555 | 5 | Wha-- |
| 0xaa55b | 44 | He nudges his sister forward, who had been\n |
| 0xaa588 | 48 | waiting at his side with ceremonious politeness. |
| 0xaa5b9 | 34 | What are you saying, dear brother? |
| 0xaa5dc | 43 | Flapping her hands in a flustered manner,\n |
| 0xaa608 | 21 | Nekone looks to Ukon. |
| 0xaa61e | 44 | Feel free to have her handle whatever jobs\n |
| 0xaa64b | 15 | need doing, eh? |
| 0xaa65b | 16 | D-Dear brother-- |
| 0xaa66c | 43 | Dahahahah! Honestly, she may not look it,\n |
| 0xaa698 | 45 | but she's got a good head on her shoulders.\n |
| 0xaa6c6 | 16 | She'll help you. |
| 0xaa6d7 | 49 | Good thing she's not as recognizable as I am yet. |
| 0xaa709 | 43 | Dear brother, that is cruel even as a joke! |
| 0xaa735 | 44 | I have my studies to attend to, and I have\n |
| 0xaa762 | 35 | a duty to assist you, dear brother. |
| 0xaa786 | 47 | Besides, if I stay with this pervert... um...\n |
| 0xaa7b6 | 24 | who knows what he'll do? |
| 0xaa7cf | 49 | Hey, I'm not gonna lay a finger on some scrawny\n |
| 0xaa801 | 42 | little kid. Try again when you know what\n |
| 0xaa82c | 14 | sex appeal is! |
| 0xaa83b | 8 | Urngh... |
| 0xaa844 | 45 | It's fine. Some things you can't learn from\n |
| 0xaa872 | 44 | behind a desk. A scholar can't limit their\n |
| 0xaa89f | 12 | perspective. |
| 0xaa8ac | 49 | Nekone, I don't want your only knowledge of the\n |
| 0xaa8de | 40 | world based on things you read in books. |
| 0xaa907 | 46 | But... dear brother... that is no reason to... |
| 0xaa936 | 47 | Well, I think you oughta see the world before\n |
| 0xaa966 | 45 | your naivete causes something that can't be\n |
| 0xaa994 | 7 | undone. |
| 0xaa99c | 48 | And what are we to do, if this degenerate DOES\n |
| 0xaa9cd | 31 | something that can't be undone? |
| 0xaa9ed | 40 | Have him take responsibility, I guess?\n |
| 0xaaa16 | 43 | It's safer than attracting some sleazebag\n |
| 0xaaa42 | 15 | off the street. |
| 0xaaa52 | 13 | Hey, hold on! |
| 0xaaa60 | 44 | As I have been saying, before you sits the\n |
| 0xaaa8d | 31 | sleaziest of all possible bags. |
| 0xaaaad | 19 | Who's a sleazebag!? |
| 0xaaac1 | 47 | Ah, that reminds me--Nekone is Ukon's sister.\n |
| 0xaaaf1 | 42 | Not Oshtor's. So you be careful with that. |
| 0xaab1c | 44 | If people found out she's Oshtor's sister,\n |
| 0xaab49 | 49 | we might get folks showing up to take advantage\n |
| 0xaab7b | 10 | of Nekone. |
| 0xaab86 | 22 | If you'd just listen-- |
| 0xaab9d | 46 | There is no way that this foul pervert, this\n |
| 0xaabcc | 41 | bag of unadulterated SLEAZE, is reliable! |
| 0xaabf6 | 48 | Don't worry. I know it's hard to tell, but the\n |
| 0xaac27 | 38 | one thing I have is an eye for people. |
| 0xaac4e | 45 | And my eye's tellin' me I can trust this kid. |
| 0xaac7c | 45 | Are you ignoring the fact that there is not\n |
| 0xaacaa | 43 | a single decent person among your allies,\n |
| 0xaacd6 | 13 | dear brother? |
| 0xaace4 | 30 | Huh? W-Well, uh, that's not... |
| 0xaad03 | 50 | An eye for people is not the one thing you have.\n |
| 0xaad36 | 38 | It is the one thing you do NOT have.\n |
| 0xaad5d | 14 | You ARE blind! |
| 0xaad6c | 48 | You should have simply called for dear sister,\n |
| 0xaad9d | 47 | but your calling THIS cretin is proof of poor\n |
| 0xaadcd | 10 | judgement. |
| 0xaadd8 | 42 | The blind is attempting to lead the blind. |
| 0xaae03 | 45 | And this cretin is blind enough to say I am\n |
| 0xaae31 | 23 | merely a "scrawny kid." |
| 0xaae49 | 46 | Ukon averts his eyes, looking carefully away\n |
| 0xaae78 | 19 | from Nekone's gaze. |
| 0xaae8c | 47 | ...And why do you look away from me at that...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_01.json` com a forma:
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
