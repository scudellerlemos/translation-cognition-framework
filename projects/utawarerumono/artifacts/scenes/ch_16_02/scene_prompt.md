# Cena ch_16_02 — pacote de traducao (447 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| Ukon | Personagem | Ukon | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| Yuuri | Personagem | Yuuri | manter_original | none |

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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Phew...` -> `Ufa...` (Haku, 12_16)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `are you?` -> `coisa assim, vai?` (Haku, 13_02)
- `us.` -> `nós.` (Haku, 15_03)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Huh...` -> `Hum...` (Ukon, 15_05)
- `dear sister?` -> `cara irmã?` (Nekone, 15_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Dear brother...` -> `Querido irmão...` (Nekone, 14_04)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Uh.` -> `Ah.` (Kuon, 11_10)
- `after all.` -> `afinal.` (Haku, 11_07)
- `Heh.` -> `Heh.` (Haku, 14_02)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `you know.` -> `você sabe.` (Nosuri, 16_01)
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
- `around.` -> `por aí.` (Kuon, 14_02)
- `I-I see.` -> `A-Entendo.` (Nekone, 14_04)
- `the city.` -> `da cidade.` (Haku, 14_02)
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
| 0xda853 | 7 | Phew... |
| 0xda85b | 43 | I lean back from the notebook to crack my\n |
| 0xda887 | 41 | shoulders, finished with my reading and\n |
| 0xda8b1 | 20 | writing for the day. |
| 0xda8c6 | 48 | It's a pain in the ass, but I really shouldn't\n |
| 0xda8f7 | 14 | be illiterate. |
| 0xda906 | 23 | I glance to the side... |
| 0xda91e | 12 | Hrm... ah... |
| 0xda92b | 46 | Kuon sits beside me, working through her own\n |
| 0xda95a | 46 | daily exercises from that arithmetic workbook. |
| 0xda989 | 48 | I guess it's good that she's finally giving it\n |
| 0xda9ba | 41 | some attention, but what brought this on? |
| 0xda9e4 | 49 | Mm... hm. I worked pretty hard, so I think I'll\n |
| 0xdaa16 | 30 | just call it here for today... |
| 0xdaa39 | 26 | We briefly exchange looks. |
| 0xdaa54 | 46 | Ahem. Maybe I'll do one or two more, actually. |
| 0xdaa83 | 49 | I somehow manage to refrain from observing it's\n |
| 0xdaab5 | 36 | only been an hour since she started. |
| 0xdaada | 40 | Sir Haku, Miss Kuon, the tea is ready... |
| 0xdab03 | 43 | Ah, just when I was getting thirsty, too.\n |
| 0xdab2f | 17 | Thanks, Rulutieh. |
| 0xdab41 | 14 | Mm, thank you. |
| 0xdab50 | 48 | I accept the offered teacup, steam rising from\n |
| 0xdab81 | 13 | its contents. |
| 0xdab8f | 27 | Ahh, that's the good stuff. |
| 0xdabab | 48 | A single sip of the tea is all it takes for an\n |
| 0xdabdc | 47 | indescribably sweet, brisk flavor to overcome\n |
| 0xdac0c | 9 | my mouth. |
| 0xdac16 | 44 | It goes without saying that Rulutieh's tea\n |
| 0xdac43 | 32 | tastes great. It's so...calming. |
| 0xdac64 | 44 | Mm! This is delicious. You always serve us\n |
| 0xdac91 | 27 | something superb, Rulutieh. |
| 0xdacad | 18 | Th-Thank you...... |
| 0xdacc0 | 46 | I wonder why that is. I can brew a good cup,\n |
| 0xdacef | 42 | but no matter what I try, I never get on\n |
| 0xdad1a | 17 | Rulutieh's level. |
| 0xdad2c | 46 | I'm making it exactly the way my mother did,\n |
| 0xdad5b | 5 | so... |
| 0xdad61 | 49 | Well, I kind of understand why. Kuon's cuisine,\n |
| 0xdad93 | 46 | be it food or tea, always comes out a bit...\n |
| 0xdadc2 | 10 | haphazard? |
| 0xdadcd | 45 | It doesn't taste bad, but it's like a man's\n |
| 0xdadfb | 31 | cooking. Just kind of mediocre. |
| 0xdae1b | 22 | Hey, love, you around? |
| 0xdae32 | 4 | Eep! |
| 0xdae37 | 45 | Ah, there you are. Thought I might find you\n |
| 0xdae65 | 11 | here, love. |
| 0xdae71 | 5 | Atuy? |
| 0xdae77 | 34 | Oh, the girl from the other day... |
| 0xdae9a | 31 | Oh? Who's this cute girl, here? |
| 0xdaeba | 13 | Huh? U-Um...? |
| 0xdaec8 | 34 | Hey, love. Is THIS one your lover? |
| 0xdaeeb | 46 | Quit taking everything there. No, she's not,\n |
| 0xdaf1a | 17 | I'm sorry to say. |
| 0xdaf2c | 46 | Aw, so she isn't? I missed my chance to hear\n |
| 0xdaf5b | 29 | about the good stuff again... |
| 0xdaf79 | 41 | This is Rulutieh. She's a friend of mine. |
| 0xdafa3 | 26 | I-I'm R-Rulutieh, yes...\n |
| 0xdafbe | 17 | Nice to meet you. |
| 0xdafd0 | 48 | Is that right? Aw, how polite you are, though!\n |
| 0xdb001 | 43 | I'm Atuy. It's nice to meet you too, Rulie. |
| 0xdb02d | 9 | Ru...lie? |
| 0xdb037 | 47 | You aren't seriously going to call her Rulie,\n |
| 0xdb067 | 8 | are you? |
| 0xdb070 | 46 | So, what's up? What brings you here all of a\n |
| 0xdb09f | 7 | sudden? |
| 0xdb0a7 | 45 | I had nothing better to do, so I decided to\n |
| 0xdb0d5 | 41 | come down for a visit! Hey, what's that\n |
| 0xdb0ff | 23 | you're d--{W350}oh, ew. |
| 0xdb117 | 44 | Atuy takes one look at my desk and pulls a\n |
| 0xdb144 | 15 | disgusted face. |
| 0xdb154 | 18 | You're studying... |
| 0xdb167 | 46 | The expression on her face is, suffice it to\n |
| 0xdb196 | 47 | say, not one a sweet young maiden should ever\n |
| 0xdb1c6 | 5 | make. |
| 0xdb1cc | 16 | I hate studying. |
| 0xdb1dd | 47 | Really? I couldn't tell at all... Yeah, no, I\n |
| 0xdb20d | 33 | pretty much got that immediately. |
| 0xdb22f | 48 | Hey, why don't you just leave all that behind?\n |
| 0xdb260 | 28 | Let's go hang out somewhere! |
| 0xdb27d | 44 | Huh? Uh, I'm not sure I can. This stuff is\n |
| 0xdb2aa | 16 | kinda important. |
| 0xdb2bb | 49 | I don't want to be stuck studying any more than\n |
| 0xdb2ed | 45 | she does, but basic reading and writing are\n |
| 0xdb31b | 9 | critical. |
| 0xdb325 | 49 | And with Kuon pushing herself to work, I'd just\n |
| 0xdb357 | 30 | feel ashamed to flake out now. |
| 0xdb376 | 43 | I'm not sticking around just to watch her\n |
| 0xdb3a2 | 39 | squirm and annoy her. Nope. Not at all. |
| 0xdb3ca | 45 | Yeah. We might as well, so why don't we all\n |
| 0xdb3f8 | 26 | go out somewhere together? |
| 0xdb413 | 7 | --Welp. |
| 0xdb41b | 47 | It goes against my principles not to take her\n |
| 0xdb44b | 46 | up on it after she made the time to come see\n |
| 0xdb47a | 3 | us. |
| 0xdb47e | 35 | What principles are those, exactly? |
| 0xdb4a2 | 43 | Kuon doesn't have an answer for that one,\n |
| 0xdb4ce | 38 | suddenly looking everywhere but at me. |
| 0xdb4f5 | 47 | It's obvious that she just wants an excuse to\n |
| 0xdb525 | 33 | be free of her studies right now. |
| 0xdb547 | 49 | Usually I'm the one slacking off. This is a bit\n |
| 0xdb579 | 26 | of an unsettling reversal. |
| 0xdb594 | 7 | Atuy... |
| 0xdb59c | 5 | Kuon? |
| 0xdb5a2 | 20 | The two lock eyes... |
| 0xdb5b7 | 11 | Kuon & Atuy |
| 0xdb5c3 | 14 | We're friends. |
| 0xdb5d2 | 45 | And then they exchange a firm, enthusiastic\n |
| 0xdb600 | 10 | handshake. |
| 0xdb60b | 40 | You really hate studying that much, huh? |
| 0xdb634 | 44 | ...And what, pray tell, is going on in here? |
| 0xdb661 | 44 | Nekone hovers in the doorway, watching the\n |
| 0xdb68e | 37 | handshake with an awkward expression. |
| 0xdb6b4 | 48 | My, you're just swimming in cuties. Who's this\n |
| 0xdb6e5 | 34 | girl, then? Are you lost, sweetie? |
| 0xdb708 | 33 | ...Who is this subtly rude woman? |
| 0xdb72a | 40 | Uh, don't mind her. Did he say anything? |
| 0xdb753 | 45 | I asked Nekone to give a periodic report to\n |
| 0xdb781 | 44 | Oshtor, which it seems she's just returned\n |
| 0xdb7ae | 5 | from. |
| 0xdb7b4 | 45 | Lord Oshtor summons you. He wishes to ask a\n |
| 0xdb7e2 | 6 | favor. |
| 0xdb7e9 | 21 | Oshtor wants a favor? |
| 0xdb7ff | 50 | She explicitly used Oshtor's name, not Ukon's...\n |
| 0xdb832 | 34 | Must be something important, then. |
| 0xdb855 | 7 | Oshtor? |
| 0xdb85d | 45 | Like, Oshtor, "Imperial Guard of the Right"\n |
| 0xdb88b | 40 | Oshtor? Half of the Twin Shields Oshtor? |
| 0xdb8b4 | 43 | ...As I was saying, who is this, precisely? |
| 0xdb8e0 | 45 | I'm Atuy. But hey, you DO mean that Oshtor,\n |
| 0xdb90e | 33 | right? Oshtor the Imperial Guard? |
| 0xdb930 | 31 | Are you an acquaintance of his? |
| 0xdb950 | 13 | Uh, that's... |
| 0xdb95e | 45 | Crap, we probably shouldn't talk about this\n |
| 0xdb98c | 45 | with outsiders around. Our work with him is\n |
| 0xdb9ba | 13 | still secret. |
| 0xdb9c8 | 35 | Acquaintances... Well, not quite.\n |
| 0xdb9ec | 28 | We're his undercover agents. |
| 0xdba09 | 4 | Wh-- |
| 0xdba0e | 6 | Huh... |
| 0xdba15 | 12 | Dear sister? |
| 0xdba22 | 42 | Why are you disclosing that so casually?\n |
| 0xdba4d | 24 | That can't be all right. |
| 0xdba66 | 51 | Oh, is that so? Tell me. This Imperial Guard guy.\n |
| 0xdba9a | 22 | Is he the perfect man? |
| 0xdbab1 | 3 | Uh? |
| 0xdbab5 | 46 | What? That's, uh... an awfully unceremonious\n |
| 0xdbae4 | 45 | response to getting that bomb dropped on you. |
| 0xdbb12 | 20 | Mm, without a doubt. |
| 0xdbb27 | 48 | I've seen great men, but only a handful of his\n |
| 0xdbb58 | 8 | caliber. |
| 0xdbb61 | 7 | Hmph... |
| 0xdbb69 | 45 | Nekone puffs out her (flat) chest at Kuon's\n |
| 0xdbb97 | 47 | words, looking vaguely proud of her brother's\n |
| 0xdbbc7 | 11 | reputation. |
| 0xdbbd3 | 45 | I'm more surprised that there are still men\n |
| 0xdbc01 | 32 | like him in the world, honestly. |
| 0xdbc22 | 43 | Oh, dear, I'll bet he's a real hunk, too... |
| 0xdbc4e | 45 | Nekone nods emphatically. Several times, in\n |
| 0xdbc7c | 5 | fact. |
| 0xdbc82 | 45 | Hee hee. I never knew friends could be this\n |
| 0xdbcb0 | 45 | great. To think I'll be introduced to a man\n |
| 0xdbcde | 12 | like that... |
| 0xdbceb | 7 | ...Huh? |
| 0xdbcf3 | 46 | I fail to comprehend your excitement. We are\n |
| 0xdbd22 | 39 | not introducing you to my dear brother. |
| 0xdbd4a | 15 | "Dear brother"? |
| 0xdbd5a | 6 | Uh oh. |
| 0xdbd61 | 7 | Nngh... |
| 0xdbd69 | 44 | Does that make you Oshtor's little sister,\n |
| 0xdbd96 | 5 | then? |
| 0xdbd9c | 48 | Nekone freezes at those words, glancing around\n |
| 0xdbdcd | 47 | anxiously. She crouches low, head in her hands. |
| 0xdbdfd | 36 | M-Miss Nekone, are you... all right? |
| 0xdbe22 | 38 | Ah, well. Cat's out of the bag anyway. |
| 0xdbe49 | 36 | Ahaha. I guess it can't be helped.\n |
| 0xdbe6e | 36 | Keep this under your hat, all right? |
| 0xdbe93 | 46 | Hey, you don't get to say that when you blew\n |
| 0xdbec2 | 29 | our cover in the first place. |
| 0xdbee0 | 44 | Sure! You're going to introduce me to him,\n |
| 0xdbf0d | 26 | so it's no problem at all. |
| 0xdbf28 | 36 | ...Is she making implicit threats?\n |
| 0xdbf4d | 46 | I'm not sure if it's worse if she's aware of\n |
| 0xdbf7c | 24 | what she's doing or not. |
| 0xdbf95 | 29 | So, I ask again. Who is this? |
| 0xdbfb3 | 46 | Mm, she's my new friend. Haku introduced her\n |
| 0xdbfe2 | 37 | to me, which I need to thank him for. |
| 0xdc008 | 35 | So. This is your fault, once again. |
| 0xdc02c | 33 | What do you mean, "once again"?\n |
| 0xdc04e | 40 | And why are you glaring at me like that? |
| 0xdc077 | 48 | Still... a summons from Oshtor. I just hope it\n |
| 0xdc0a8 | 30 | isn't another troublesome job. |
| 0xdc0c7 | 46 | Lord Oshtor, I have brought them as requested. |
| 0xdc0f6 | 25 | Thank you all for coming. |
| 0xdc110 | 48 | Kuon, Rulutieh, and I arrange ourselves before\n |
| 0xdc141 | 27 | Oshtor, who remains seated. |
| 0xdc15d | 45 | It's so strange. Even though I know this is\n |
| 0xdc18b | 44 | Ukon, when he's in Oshtor mode, everything\n |
| 0xdc1b8 | 15 | feels... tense. |
| 0xdc1c8 | 16 | ...Incidentally. |
| 0xdc1d9 | 46 | Oshtor shifts his gaze to the person next to\n |
| 0xdc208 | 28 | me, looking faintly puzzled. |
| 0xdc225 | 12 | Who is this? |
| 0xdc232 | 27 | Nice to meet you. I'm Atuy. |
| 0xdc24e | 47 | Trying to tell her to go back to her room was\n |
| 0xdc27e | 45 | a wasted effort, and Kuon's no help, so she\n |
| 0xdc2ac | 12 | followed us. |
| 0xdc2b9 | 26 | Don't, uh. Don't mind her. |
| 0xdc2d4 | 18 | ...Hm. As you say. |
| 0xdc2e7 | 15 | Dear brother... |
| 0xdc2f7 | 49 | He carries on, seemingly paying no mind to Atuy\n |
| 0xdc329 | 28 | without further questioning. |
| 0xdc346 | 48 | I can see a little of Ukon in that, honestly--\n |
| 0xdc377 | 28 | taking things at face value. |
| 0xdc394 | 5 | Ah... |
| 0xdc39a | 3 | Hm? |
| 0xdc39e | 46 | What's wrong? You wanted to be introduced so\n |
| 0xdc3cd | 32 | badly, so what's with that face? |
| 0xdc3ee | 47 | Oh, dear. See--he's definitely a perfect man!\n |
| 0xdc41e | 44 | Sincere, forthright, not a flaw to speak of. |
| 0xdc44b | 10 | But, um... |
| 0xdc456 | 28 | What? Unsatisfied with that? |
| 0xdc473 | 45 | He's all... stiff. It'd probably be way too\n |
| 0xdc4a1 | 30 | exhausting to go out with him. |
| 0xdc4c0 | 40 | Well... Yeah, all right. I can see that. |
| 0xdc4e9 | 45 | Ukon aside, I could see that being the case\n |
| 0xdc517 | 40 | with Oshtor. But geez, isn't she being\n |
| 0xdc540 | 17 | needlessly picky? |
| 0xdc552 | 45 | *Sigh* My arduous quest for the perfect man\n |
| 0xdc580 | 12 | continues... |
| 0xdc58d | 38 | So, what did you need to see us about? |
| 0xdc5b4 | 46 | I called you here because someone in my care\n |
| 0xdc5e3 | 19 | requires escorting. |
| 0xdc5f7 | 12 | Escorting... |
| 0xdc604 | 44 | So it'll be like when we escorted Rulutieh\n |
| 0xdc631 | 15 | to the capital? |
| 0xdc641 | 43 | Hrm. That's ostensibly correct, but there\n |
| 0xdc66d | 28 | are... complicating factors. |
| 0xdc68a | 24 | Well, I figured as much. |
| 0xdc6a3 | 43 | Seeing as we're Oshtor's deniable assets,\n |
| 0xdc6cf | 46 | I would've been surprised if that wasn't the\n |
| 0xdc6fe | 5 | case. |
| 0xdc704 | 19 | ...I appreciate it. |
| 0xdc718 | 45 | I'll have the person in question illuminate\n |
| 0xdc746 | 12 | the details. |
| 0xdc753 | 46 | Oshtor claps his hands once, then calls over\n |
| 0xdc782 | 13 | his shoulder. |
| 0xdc790 | 8 | Come in. |
| 0xdc799 | 10 | Y-Yes sir. |
| 0xdc7a4 | 12 | Pardon me... |
| 0xdc7b1 | 7 | Whoa... |
| 0xdc7b9 | 32 | This is who you'll be escorting. |
| 0xdc7da | 42 | I am Yuuri. I-It's a pleasure to meet you. |
| 0xdc805 | 39 | The young man bows respectfully as he\n |
| 0xdc82d | 19 | introduces himself. |
| 0xdc841 | 44 | Looks like the timid, slightly androgynous\n |
| 0xdc86e | 31 | type, but he seems nice enough. |
| 0xdc88e | 46 | So, what exactly are we protecting you from,\n |
| 0xdc8bd | 48 | if you need escorts? We need details to do our\n |
| 0xdc8ee | 9 | job well. |
| 0xdc8f8 | 22 | Yes, well. About that. |
| 0xdc90f | 6 | Y-Yes. |
| 0xdc916 | 45 | Oshtor gives Yuuri a pregnant look, and the\n |
| 0xdc944 | 27 | boy sheepishly steps forth. |
| 0xdc960 | 20 | This must be fate... |
| 0xdc975 | 4 | Huh? |
| 0xdc97a | 42 | Indeed, this must be... what they call a\n |
| 0xdc9a5 | 20 | fateful encounter... |
| 0xdc9ba | 18 | You say something? |
| 0xdc9cd | 22 | I accept your request! |
| 0xdc9e4 | 3 | Uh. |
| 0xdc9e8 | 29 | What is she blithering about? |
| 0xdca06 | 42 | Ahaha, interested in joining up with us,\n |
| 0xdca31 | 10 | Of course! |
| 0xdca3c | 15 | Dear... sister? |
| 0xdca4c | 42 | W-Would, um... Would that be all right...? |
| 0xdca77 | 45 | It's fine, it's fiiine. We're understaffed,\n |
| 0xdcaa5 | 10 | after all. |
| 0xdcab0 | 44 | You brought her with us in anticipation of\n |
| 0xdcadd | 17 | this, didn't you? |
| 0xdcaef | 4 | Heh. |
| 0xdcaf4 | 27 | Kuon only smiles and winks. |
| 0xdcb10 | 23 | Bingo. I had a feeling. |
| 0xdcb28 | 42 | I was getting frustrated because we just\n |
| 0xdcb53 | 44 | couldn't find a skilled person... and then\n |
| 0xdcb80 | 21 | one came right to us! |
| 0xdcb96 | 48 | A skilled person joining up for free, no less.\n |
| 0xdcbc7 | 43 | Ahaha... I can't stop laughing at all this. |
| 0xdcbf3 | 47 | I figured Kuon didn't have many friends, so I\n |
| 0xdcc23 | 45 | can understand this, but... are you totally\n |
| 0xdcc51 | 5 | sure? |
| 0xdcc57 | 46 | I'm just waiting for the other shoe to drop,\n |
| 0xdcc86 | 45 | now. She seems harmless enough, but at what\n |
| 0xdccb4 | 5 | cost? |
| 0xdccba | 46 | Is she really skilled as all that, with that\n |
| 0xdcce9 | 20 | warm outward d--huh? |
| 0xdccfe | 36 | Is... By any chance, is Atuy strong? |
| 0xdcd23 | 3 | Eh? |
| 0xdcd27 | 35 | Wh-What, did I say something weird? |
| 0xdcd4b | 47 | You're going to end up in trouble some day if\n |
| 0xdcd7b | 44 | you don't learn how to read people better,\n |
| 0xdcda8 | 9 | you know. |
| 0xdcdb2 | 42 | Hey, Yuuri, I know a place that has some\n |
| 0xdcddd | 17 | fantastic drinks. |
| 0xdcdef | 8 | O-OK...? |
| 0xdcdf8 | 46 | How about we go get a drink to celebrate our\n |
| 0xdce27 | 16 | fateful meeting? |
| 0xdce38 | 28 | Huh? N-No, I have to talk... |
| 0xdce55 | 45 | It's fiiiine. We'll talk after we've relaxed! |
| 0xdce83 | 18 | Come on, let's go! |
| 0xdce96 | 15 | *Drag, drag*... |
| 0xdcea6 | 17 | Huh? U-Um, wait-- |
| 0xdceb8 | 26 | Don't worry about a thing~ |
| 0xdced3 | 47 | ...And I'M the one who needs to learn to read\n |
| 0xdcf03 | 7 | people? |
| 0xdcf0b | 44 | There's no telling where they'll end up if\n |
| 0xdcf38 | 46 | they go off on their own. I should tag along\n |
| 0xdcf67 | 15 | and watch them. |
| 0xdcf77 | 27 | Nekone, Rulutieh, let's go. |
| 0xdcf93 | 9 | So be it. |
| 0xdcf9d | 7 | O-OK... |
| 0xdcfa5 | 47 | I'll leave the rest of the nitty-gritty stuff\n |
| 0xdcfd5 | 24 | in your hands, OK, Haku? |
| 0xdcfee | 49 | What? H-Hey, don't just drop this in my lap and\n |
| 0xdd020 | 9 | run off-- |
| 0xdd02a | 44 | You're just trying to force the bothersome\n |
| 0xdd057 | 29 | stuff on m--aaand she's gone. |
| 0xdd075 | 48 | It gladdens me to see you enjoying yourselves.\n |
| 0xdd0a6 | 19 | I'm jealous, truly. |
| 0xdd0ba | 49 | In what way do I look like I'm enjoying myself?\n |
| 0xdd0ec | 45 | Let's swap some time, so you can get pushed\n |
| 0xdd11a | 7 | around. |
| 0xdd122 | 49 | I think it's a fine sign. They trust you enough\n |
| 0xdd154 | 44 | to leave the business matters in your hands. |
| 0xdd181 | 48 | I was starting to wonder who your new ally is,\n |
| 0xdd1b2 | 48 | but to find HER of all people in your company... |
| 0xdd1e3 | 43 | You lead an unusual life, to say the least. |
| 0xdd20f | 27 | Hm? You actually know Atuy? |
| 0xdd22b | 47 | Not personally. Her father boasts to me about\n |
| 0xdd25b | 41 | his beloved daughter quite often, though. |
| 0xdd285 | 47 | ...Often enough that I suspected he was doing\n |
| 0xdd2b5 | 23 | it only to irritate me. |
| 0xdd2cd | 8 | I-I see. |
| 0xdd2d6 | 50 | I sympathize with her desire to distance herself\n |
| 0xdd309 | 20 | from her upbringing. |
| 0xdd31e | 50 | Out of consideration for that, I feign ignorance\n |
| 0xdd351 | 14 | of who she is. |
| 0xdd360 | 40 | Guess he's got it all figured out, then. |
| 0xdd389 | 45 | Well, putting that aside for now--What else\n |
| 0xdd3b7 | 33 | do I need to know about this job? |
| 0xdd3d9 | 32 | You mentioned there are, uh...\n |
| 0xdd3fa | 26 | extenuating circumstances? |
| 0xdd415 | 50 | Your men could act as escorts in broad daylight.\n |
| 0xdd448 | 41 | You need us because it's something more\n |
| 0xdd472 | 10 | sensitive. |
| 0xdd47d | 39 | You have the right of it. Yuuri is an\n |
| 0xdd4a5 | 48 | illegitimate child caught up in a matter of...\n |
| 0xdd4d6 | 12 | inheritance. |
| 0xdd4e3 | 43 | Inheritance, huh. I think I know how this\n |
| 0xdd50f | 11 | story goes. |
| 0xdd51b | 49 | It saddens me that I cannot say anything to the\n |
| 0xdd54d | 9 | contrary. |
| 0xdd557 | 48 | Yuuri was originally a manor servant, you see.\n |
| 0xdd588 | 47 | No relations to speak of, no particular status. |
| 0xdd5b8 | 46 | But when the master of the house passed, his\n |
| 0xdd5e7 | 46 | will detailed a bequest to be made... to his\n |
| 0xdd616 | 14 | bastard child. |
| 0xdd625 | 49 | Ah, I see where this is going. You want to keep\n |
| 0xdd657 | 35 | the scandal secret from the public? |
| 0xdd67b | 47 | That, and securing a stealthy escape from the\n |
| 0xdd6ab | 18 | capital for Yuuri. |
| 0xdd6be | 47 | Formerly reticent blood relatives are closing\n |
| 0xdd6ee | 42 | in like vultures, seeking a piece of the\n |
| 0xdd719 | 10 | bequest... |
| 0xdd724 | 41 | So there is, regrettably, an element of\n |
| 0xdd74e | 34 | potential danger to be considered. |
| 0xdd771 | 47 | The important wrinkle is that Yuuri has since\n |
| 0xdd7a1 | 45 | renounced the inheritance, and wishes to be\n |
| 0xdd7cf | 18 | rid of the matter. |
| 0xdd7e2 | 44 | Wait, if the inheritance isn't part of the\n |
| 0xdd80f | 44 | picture, then why do you need us to act as\n |
| 0xdd83c | 8 | escorts? |
| 0xdd845 | 42 | Many do not believe the sincerity of the\n |
| 0xdd870 | 45 | renouncement. They think it a ruse to throw\n |
| 0xdd89e | 15 | them off-guard. |
| 0xdd8ae | 43 | The amount is only a small portion of the\n |
| 0xdd8da | 43 | will's total bequests, but still far from\n |
| 0xdd906 | 14 | insignificant. |
| 0xdd915 | 50 | Deception and threats of abduction have rendered\n |
| 0xdd948 | 45 | armed escorts the only viable countermeasure. |
| 0xdd976 | 47 | Living amongst the wolves of the capital at a\n |
| 0xdd9a6 | 44 | time like this must be difficult, as I can\n |
| 0xdd9d3 | 13 | only imagine. |
| 0xdd9e1 | 48 | Yeah, no kidding. It's just greed and intrigue\n |
| 0xdda12 | 27 | all the way down, isn't it? |
| 0xdda2e | 20 | Just so, I'm afraid. |
| 0xdda43 | 45 | Even so, to disregard a man's last wish for\n |
| 0xdda71 | 24 | his child's happiness... |
| 0xdda8a | 43 | Yuuri is letting go of the inheritance to\n |
| 0xddab6 | 39 | protect the family name from scandal.\n |
| 0xddade | 8 | For him. |
| 0xddae7 | 43 | All that is left is to meet Yuuri's lover\n |
| 0xddb13 | 42 | outside the city, so they can start over\n |
| 0xddb3e | 24 | together in a new place. |
| 0xddb57 | 45 | I've arranged for another escort after that\n |
| 0xddb85 | 48 | point. All you need to do is get Yuuri outside\n |
| 0xddbb6 | 9 | the city. |
| 0xddbc0 | 30 | I see. I think I get the idea. |
| 0xddbdf | 16 | Will you accept? |
| 0xddbf0 | 48 | Not like I have a choice, seeing as the others\n |
| 0xddc21 | 29 | have already dragged him off. |
| 0xddc3f | 28 | Heh. I appreciate it, truly. |
| 0xddc5c | 46 | But this means he's gonna disappear from the\n |
| 0xddc8b | 24 | capital altogether, huh? |
| 0xddca4 | 44 | Atuy'll be disappointed. She seems totally\n |
| 0xddcd1 | 8 | smitten. |
| 0xddcda | 47 | Hopefully she doesn't just end up running off\n |
| 0xddd0a | 13 | with... wait. |
| 0xddd18 | 45 | Hold on, who did you say he was leaving the\n |
| 0xddd46 | 13 | capital with? |
| 0xddd54 | 29 | Yuuri. Who's he leaving with? |
| 0xddd72 | 47 | A lover. Someone Yuuri has pledged both heart\n |
| 0xddda2 | 12 | and body to. |
| 0xdddaf | 12 | Oh... I see. |
| 0xdddbc | 40 | Ah, Atuy. Sunk before you even started\n |
| 0xddde5 | 11 | fighting... |
| 0xdddf1 | 44 | We spoke only briefly, but he seems a fine\n |
| 0xdde1e | 17 | enough young man. |
| 0xdde30 | 44 | He thinks nothing of the riches that might\n |
| 0xdde5d | 22 | fall into his hands... |
| 0xdde74 | 49 | He places her happiness first. He asserted that\n |
| 0xddea6 | 47 | he'll make her happy by the fruits of his own\n |
| 0xdded6 | 7 | labors. |
| 0xddede | 42 | She ought to be fine, left under his care. |
| 0xddf09 | 42 | Now, that's something I'd be embarrassed\n |
| 0xddf34 | 9 | to s--uh? |
| 0xddf3e | 18 | Did you say "she"? |
| 0xddf51 | 46 | Yes, I had Yuuri disguised as a man to throw\n |
| 0xddf80 | 47 | off her pursuers. Altered gender presentation\n |
| 0xddfb0 | 13 | is effective. |
| 0xddfbe | 46 | ...Atuy's designs continue to blow up in her\n |
| 0xddfed | 5 | face. |
| 0xddff3 | 34 | How do I even explain this to her? |
| 0xde016 | 45 | I can't just crush her and say "Hey, you've\n |
| 0xde044 | 47 | been had, sorry." Not when she's in such high\n |
| 0xde074 | 8 | spirits. |
| 0xde07d | 42 | I'll just act like I didn't hear anything. |

## 8. Formato de saida EXIGIDO
Escreva `translations_16_02.json` com a forma:
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
