# Cena ch_22_03 — pacote de traducao (362 linhas)

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
| Atuy | Personagem | Atuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Ukon | Personagem | Ukon | manter_original | major |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Woman | UI | Mulher | traduzir | none |
| woptor | Criatura | woptor | manter_original | none |
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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `them.` -> `deles.` (Kuon, 11_05)
- `thing.` -> `coisa.` (Haku, 12_03)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `Hmmm...` -> `Hmmm...` (Garota, 19_08)
- `here...` -> `o fim...` (Haku, 12_03)
- `Agreed.` -> `Combinado.` (Kuon, 18_01)
- `things.` -> `faz.` (Nekone, 15_03)
- `W-Well, that's...` -> `B-Bem, isso é...` (Haku, 21_01)
- `job.` -> `trabalho.` (Falante (Kuon ou Maroro), 18_01)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `dear sister.` -> `querida irmã.` (Nekone, 14_10)
- `somewhere.` -> `de algum lugar.` (Haku, 15_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Kuon.` -> `Kuon.` (Kuon, 11_02)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Bwah!?` -> `Ué!?` (Rulutieh ou Anju (exclamação), 18_01)
- `quiet.` -> `calado.` (Haku, 18_01)
- `look.` -> `sólido.` (Haku, 14_02)
- `over me.` -> `pra mim.` (Homem, 17_01)
- `wings.` -> `flancos.` (Haku, 13_06)
- `reason.` -> `alguma razão.` (Haku, 14_09)
- `*Sigh*` -> `*Ah*` (Haku, 14_03)
- `with...` -> `para...` (Kuon, 13_09)
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
| 0x231772 | 14 | Bodyguards...? |
| 0x231781 | 50 | Correct. I would have you act as security detail\n |
| 0x2317b4 | 36 | for a particular group of officials. |
| 0x2317d9 | 47 | After I answer Oshtor's summons, he greets me\n |
| 0x231809 | 26 | with a strange assignment. |
| 0x231824 | 45 | Tomorrow, ambassadors from a certain nation\n |
| 0x231852 | 41 | will be arriving in the imperial capital. |
| 0x23187c | 44 | They are from a country far to the west of\n |
| 0x2318a9 | 43 | Yamato... An island nation beyond the seas. |
| 0x2318d5 | 48 | Huh. Must be a real hassle, coming all the way\n |
| 0x231906 | 5 | here. |
| 0x23190c | 45 | They are indeed a much smaller country than\n |
| 0x23193a | 45 | Yamato, but my liege seems quite interested\n |
| 0x231968 | 8 | in them. |
| 0x231971 | 46 | Their homeland is known as... the land where\n |
| 0x2319a0 | 11 | god sleeps. |
| 0x2319ac | 25 | Where god sleeps, huh...? |
| 0x2319c6 | 47 | Naturally, we must take utmost care to ensure\n |
| 0x2319f6 | 29 | that nothing happens to them. |
| 0x231a14 | 47 | That is where you come in, Lord Haku. I would\n |
| 0x231a44 | 33 | have you act as their protection. |
| 0x231a66 | 24 | Us as bodyguards, huh... |
| 0x231a7f | 23 | Something troubles you? |
| 0x231a97 | 32 | Not really. I just don't get it. |
| 0x231ab8 | 44 | Isn't that kind of job reserved for actual\n |
| 0x231ae5 | 9 | soldiers? |
| 0x231aef | 42 | Our usual jobs aren't in the public eye.\n |
| 0x231b1a | 43 | Shady stuff. That's what I thought, anyway. |
| 0x231b46 | 34 | You need not discredit yourself.\n |
| 0x231b69 | 43 | I am asking you to do this because I have\n |
| 0x231b95 | 21 | faith in your skills. |
| 0x231bab | 45 | Believe me, I'll take all the credit I can.\n |
| 0x231bd9 | 44 | I fully understand that people like us are\n |
| 0x231c06 | 10 | necessary. |
| 0x231c11 | 50 | But I'm not so sure how that's going to come off\n |
| 0x231c44 | 19 | to the ambassadors. |
| 0x231c58 | 48 | If Yamato sends them a bunch of ragtag misfits\n |
| 0x231c89 | 47 | instead of soldiers, it doesn't give the best\n |
| 0x231cb9 | 11 | impression. |
| 0x231cc5 | 46 | I'm just saying, it might not be in Yamato's\n |
| 0x231cf4 | 46 | best interests to send us if it might offend\n |
| 0x231d23 | 5 | them. |
| 0x231d29 | 44 | Haha... A keen eye, as ever. You truly are\n |
| 0x231d56 | 18 | full of surprises. |
| 0x231d69 | 49 | Very well. Then allow me to speak with complete\n |
| 0x231d9b | 8 | honesty. |
| 0x231da4 | 35 | With that, Oshtor suddenly rises... |
| 0x231dc8 | 49 | And strides into the backroom, abruptly leaving\n |
| 0x231dfa | 10 | me behind. |
| 0x231e05 | 24 | Hey! Sorry for the wait. |
| 0x231e22 | 44 | Ukon scratches his head as he ambles back,\n |
| 0x231e4f | 35 | and flumps back down onto his seat. |
| 0x231e73 | 47 | Whew. Feels a lot more natural to talk to you\n |
| 0x231ea3 | 27 | when I'm back to this look. |
| 0x231ebf | 44 | I see. Well, honestly, I don't really care\n |
| 0x231eec | 25 | which one I'm talking to. |
| 0x231f06 | 43 | Man, this guy's as complicated as ever...\n |
| 0x231f32 | 44 | Well, I guess I'm kind of used to it by now. |
| 0x231f5f | 21 | ...Well, where was I? |
| 0x231f75 | 50 | Of course, we'll have our soldiers guarding them\n |
| 0x231fa8 | 49 | as well. Your group will be more like a support\n |
| 0x231fda | 5 | team. |
| 0x231fe0 | 50 | Basically, you'll be guides for the ambassadors,\n |
| 0x232013 | 45 | handle their everyday needs... That kind of\n |
| 0x232041 | 6 | thing. |
| 0x232048 | 44 | Yeah, all right. That sounds more like our\n |
| 0x232075 | 6 | style. |
| 0x23207c | 45 | But, of course... This is all just a front.\n |
| 0x2320aa | 44 | There's actually something else I want you\n |
| 0x2320d7 | 11 | to do, kid. |
| 0x2320e3 | 47 | I figured you were going somewhere with this... |
| 0x232113 | 38 | So, what exactly do you need me to do? |
| 0x23213a | 42 | Put plainly... I want you to observe them. |
| 0x232165 | 8 | Observe? |
| 0x23216e | 47 | Yep. Yamato's only had a bit of trade contact\n |
| 0x23219e | 41 | with this island nation. Nothing big or\n |
| 0x2321c8 | 9 | official. |
| 0x2321d2 | 42 | Of course, we've got all their basic info. |
| 0x2321fd | 47 | The state of their country, their government,\n |
| 0x23222d | 25 | their military might...\n |
| 0x232247 | 16 | The usual stuff. |
| 0x232258 | 47 | But it's all just words on a page. Can't jump\n |
| 0x232288 | 45 | to any conclusions about them based on that\n |
| 0x2322b6 | 6 | alone. |
| 0x2322bd | 26 | ...Guess you have a point. |
| 0x2322d8 | 45 | I want you to trust your own eyes, your own\n |
| 0x232306 | 44 | ears, your own senses... Learn all you can\n |
| 0x232333 | 11 | about them. |
| 0x23233f | 46 | We need to learn whether or not this country\n |
| 0x23236e | 42 | of theirs can be a good ally for Yamato... |
| 0x232399 | 29 | ...And that's pretty much it. |
| 0x2323b7 | 47 | *Sigh*... I should have known my dear brother\n |
| 0x2323e7 | 33 | would devise something like this. |
| 0x232409 | 42 | So these ambassadors are arriving in the\n |
| 0x232434 | 22 | imperial capital soon. |
| 0x23244b | 44 | Hmmm. I wonder what kind of people they are? |
| 0x232478 | 44 | But it will be a little while until we are\n |
| 0x2324a5 | 43 | officially appointed as their bodyguards,\n |
| 0x2324d1 | 8 | correct? |
| 0x2324da | 45 | Yeah. In the meantime, let's see what these\n |
| 0x232508 | 30 | foreign ambassadors look like. |
| 0x232527 | 47 | Hm... I see. I was wondering why you gathered\n |
| 0x232557 | 46 | us here on the main street. So that was your\n |
| 0x232586 | 7 | plan... |
| 0x23258e | 3 | Hm? |
| 0x232592 | 47 | I look over to see Kuon holding a steaming cup. |
| 0x2325c2 | 33 | What're you drinking there, Kuon? |
| 0x2325e4 | 45 | Huh? Oh, it was a little chilly today, so I\n |
| 0x232612 | 43 | bought some warm tea from the vendor over\n |
| 0x23263e | 6 | there. |
| 0x232645 | 49 | Huh. This market sells practically anything you\n |
| 0x232677 | 27 | could think of, doesn't it? |
| 0x232693 | 48 | So, what country exactly are these ambassadors\n |
| 0x2326c4 | 13 | representing? |
| 0x2326d2 | 45 | Oh, it was an island country to the west of\n |
| 0x232700 | 32 | The name was something like...\n |
| 0x232721 | 14 | To... Tuss...? |
| 0x232733 | 25 | Oh, right. It was Tuskur. |
| 0x23274d | 9 | Pffffft!! |
| 0x232757 | 50 | Kuon immediately spits the tea she's drinking...\n |
| 0x23278a | 37 | straight into the nearby Atuy's face. |
| 0x2327b0 | 10 | Ack! Hot!! |
| 0x2327bb | 15 | S-Sorry, Atuy!! |
| 0x2327cb | 46 | You caught me completely off my guard there... |
| 0x2327fa | 45 | I'm so sorry... Let me wipe that off for you. |
| 0x232828 | 46 | Um... Miss Kuon, do you know something about\n |
| 0x232857 | 20 | this Tuskur country? |
| 0x23286c | 26 | What kind of nation is it? |
| 0x232887 | 41 | Huh? Wh-Whatever are you talking about?\n |
| 0x2328b1 | 43 | I have no idea, I think--not the slightest! |
| 0x2328dd | 47 | She's an open book. She must know a lot about\n |
| 0x23290d | 15 | this country... |
| 0x23291d | 42 | B-But I suppose I... I may have heard it\n |
| 0x232948 | 26 | mentioned before, I think! |
| 0x232963 | 29 | I-I see... So Tuskur has...\n |
| 0x232981 | 7 | Hmmm... |
| 0x232989 | 46 | She mutters to herself as she rubs furiously\n |
| 0x2329b8 | 28 | at Atuy's face with a cloth. |
| 0x2329d5 | 23 | *Rub* *rub* *rub* *rub* |
| 0x2329ed | 28 | Owie... Kuon!? That huuurts! |
| 0x232a0a | 33 | You heard of them before, Nekone? |
| 0x232a2c | 35 | I have not heard much about them.\n |
| 0x232a50 | 44 | All I know is that they are a small island\n |
| 0x232a7d | 19 | nation to the west. |
| 0x232a91 | 49 | That must have been quite the journey for them.\n |
| 0x232ac3 | 45 | To have crossed the sea to come all the way\n |
| 0x232af1 | 7 | here... |
| 0x232af9 | 46 | Yeah, right? And I hear one of the officials\n |
| 0x232b28 | 41 | coming here is a kamunagi or something.\n |
| 0x232b52 | 18 | Someone important. |
| 0x232b65 | 15 | A kamunagi...!? |
| 0x232b75 | 31 | *Grind* *grind* *grind* *grind* |
| 0x232b95 | 46 | Kuon's grip tightens on the cloth in her hand. |
| 0x232bc4 | 40 | Owowowowowow! Kuon, you're hurting me!\n |
| 0x232bed | 43 | You're going to grate my skin off at this\n |
| 0x232c19 | 5 | rate! |
| 0x232c1f | 44 | Oh! S-S-S-Sorry! I wasn't paying attention!! |
| 0x232c4c | 48 | This visiting kamunagi... It must be difficult\n |
| 0x232c7d | 46 | for her, being in a completely different land. |
| 0x232cac | 47 | Indeed. I would like to be of service to her,\n |
| 0x232cdc | 26 | regardless of her station. |
| 0x232cf7 | 7 | Agreed. |
| 0x232cff | 47 | I'm sure that concern would only go to waste.\n |
| 0x232d2f | 44 | They're not the type to be daunted by such\n |
| 0x232d5c | 7 | things. |
| 0x232d64 | 29 | Huh? How would you know that? |
| 0x232d82 | 17 | W-Well, that's... |
| 0x232d94 | 46 | I-In any case! I think we should reject this\n |
| 0x232dc3 | 4 | job. |
| 0x232dc8 | 5 | Huh!? |
| 0x232dce | 48 | I don't think we need to be the ones to handle\n |
| 0x232dff | 19 | such an assignment. |
| 0x232e13 | 45 | If these people are strange enough to cross\n |
| 0x232e41 | 45 | an entire ocean to come here, we should let\n |
| 0x232e6f | 8 | them be. |
| 0x232e78 | 48 | I mean, they might not even like the fact that\n |
| 0x232ea9 | 37 | they're getting bodyguards, you know? |
| 0x232ecf | 41 | ...You're acting rather cold today, Kuon. |
| 0x232ef9 | 42 | You are not acting like your usual self,\n |
| 0x232f24 | 12 | dear sister. |
| 0x232f31 | 7 | E-Er... |
| 0x232f39 | 6 | Eeep!? |
| 0x232f40 | 48 | Aha. It would seem the dignitaries in question\n |
| 0x232f71 | 13 | have arrived. |
| 0x232f7f | 43 | We look back to see a number of carriages\n |
| 0x232fab | 41 | heading our way from off in the distance. |
| 0x232fd5 | 46 | We can hear the cheering of the crowd as the\n |
| 0x233004 | 15 | carriages pass. |
| 0x233014 | 32 | Wha--!? What are those steeds?\n |
| 0x233035 | 34 | There's not a single hair on them! |
| 0x233058 | 16 | You are right... |
| 0x233069 | 47 | The woptors pulling the carriages look pretty\n |
| 0x233099 | 8 | strange. |
| 0x2330a2 | 48 | They make an odd sight compared to the woptors\n |
| 0x2330d3 | 49 | from Yamato. Instead of a light fur, their skin\n |
| 0x233105 | 9 | is scaly. |
| 0x23310f | 40 | Well, Tuskur's climate is much warmer... |
| 0x233138 | 27 | Oh... So that's what it is. |
| 0x233154 | 38 | Wait, how do you even know that, Kuon? |
| 0x23317b | 46 | O-Oh, you know... I just remember reading it\n |
| 0x2331aa | 10 | somewhere. |
| 0x2331b5 | 42 | I must say, this is quite the spectacle... |
| 0x2331e0 | 23 | It's... so beautiful... |
| 0x2331f8 | 47 | The carriages pulled by these furless woptors\n |
| 0x233228 | 45 | also have very strange decorations over them. |
| 0x233256 | 44 | It's not flashy, but it has a delicate yet\n |
| 0x233283 | 44 | elaborate pattern... just enough not to be\n |
| 0x2332b0 | 6 | gaudy. |
| 0x2332b7 | 44 | Even someone without an eye for this stuff\n |
| 0x2332e4 | 46 | can tell their culture has a different style\n |
| 0x233313 | 14 | from Yamato's. |
| 0x233322 | 9 | Oh, look! |
| 0x23332c | 50 | The window on the carriage slides open to reveal\n |
| 0x23335f | 15 | a woman inside. |
| 0x23336f | 42 | Immediately, we hear gasps from the crowd. |
| 0x23339a | 29 | She's... extremely beautiful. |
| 0x2333b8 | 44 | Her glossy pale cyan hair is neatly cut to\n |
| 0x2333e5 | 42 | around her shoulders, and her face has a\n |
| 0x233410 | 13 | gentle smile. |
| 0x23341e | 48 | What draws the most of our attention, however,\n |
| 0x23344f | 38 | are the large black wings on her back. |
| 0x233476 | 42 | I've seen all kinds since we came to the\n |
| 0x2334a1 | 46 | imperial capital, but never anyone with wings. |
| 0x2334d0 | 34 | Could that person be the kamunagi? |
| 0x2334f3 | 26 | I'd say that's a safe bet. |
| 0x23350e | 47 | Uruuru and Saraana suddenly glide in front of\n |
| 0x23353e | 43 | me, glaring at her as if to scare her away. |
| 0x23356a | 45 | Worrying that she might be offended, I send\n |
| 0x233598 | 48 | them back, and take a good look at the foreign\n |
| 0x2335c9 | 9 | kamunagi. |
| 0x2335d3 | 42 | She looks very gentle, and so elegant...\n |
| 0x2335fe | 44 | Pretty much the complete opposite of Kuon... |
| 0x23362b | 7 | ...Huh? |
| 0x233633 | 47 | ...I suddenly realize that I've lost track of\n |
| 0x233663 | 5 | Kuon. |
| 0x233669 | 46 | I glance around, and see her trying to sidle\n |
| 0x233698 | 33 | inconspicuously into an alleyway. |
| 0x2336ba | 31 | What do you think you're doing? |
| 0x2336da | 25 | I-I'm not doing anything. |
| 0x2336f4 | 49 | Quit skulking around. Why don't you take a good\n |
| 0x233726 | 41 | look at the people we're supposed to be\n |
| 0x233750 | 9 | guarding? |
| 0x23375a | 49 | I-I'm not hiding! And besides, they really have\n |
| 0x23378c | 30 | no need for bodyguards anyway. |
| 0x2337ab | 45 | Yeah, like that excuse is gonna fly. C'mon... |
| 0x2337d9 | 45 | I struggle to pull Kuon out of the alleyway\n |
| 0x233807 | 45 | as she tries desperately to hide herself...\n |
| 0x233835 | 16 | for some reason. |
| 0x23384b | 38 | As the kamunagi looks around her new\n |
| 0x233872 | 45 | surroundings eagerly, we happen to lock eyes. |
| 0x2338a0 | 9 | ...*Grin* |
| 0x2338aa | 4 | Huh? |
| 0x2338af | 6 | *Wave* |
| 0x2338b6 | 45 | I'm not sure why, but the kamunagi suddenly\n |
| 0x2338e4 | 26 | smiles and begins to wave. |
| 0x2338ff | 31 | Huh? What? Is she waving at me? |
| 0x23391f | 45 | I don't really get it, but I figure I might\n |
| 0x23394d | 18 | as well wave back. |
| 0x233960 | 44 | The kamunagi smiles back at me, apparently\n |
| 0x23398d | 10 | satisfied. |
| 0x233998 | 51 | The carriage eventually passes us, and disappears\n |
| 0x2339cc | 25 | into the crowd of people. |
| 0x2339e6 | 31 | Wooooow... She was sooo pretty. |
| 0x233a06 | 45 | Yes... I don't think I've ever seen someone\n |
| 0x233a34 | 22 | so beautiful before... |
| 0x233a4b | 40 | Atuy and Rulutieh are still giddy with\n |
| 0x233a74 | 34 | excitement after seeing the woman. |
| 0x233a97 | 24 | Was she... waving at me? |
| 0x233ab0 | 28 | But if she was, then... why? |
| 0x233acd | 46 | As I bemusedly watch the procession move on,\n |
| 0x233afc | 37 | another shocking sight fills my view. |
| 0x233b22 | 5 | Rrwr? |
| 0x233b28 | 6 | Bwah!? |
| 0x233b2f | 36 | A giant white beast trudges forth.\n |
| 0x233b54 | 46 | It's huge--easily bigger than a normal person. |
| 0x233b83 | 18 | Wh-What the hell!? |
| 0x233b96 | 47 | The previously boisterous crowd suddenly goes\n |
| 0x233bc6 | 6 | quiet. |
| 0x233bcd | 45 | The beast seems completely unbothered as it\n |
| 0x233bfb | 32 | continues along the main street. |
| 0x233c1c | 46 | The crowd holds its breath as they watch it,\n |
| 0x233c4b | 42 | but they don't seem afraid. More like...\n |
| 0x233c76 | 7 | in awe? |
| 0x233c7e | 36 | Wh-What in the world is THAT beast!? |
| 0x233ca3 | 35 | Please stay your hand, dear sister. |
| 0x233cc7 | 43 | Nosuri reaches for her bow instinctively,\n |
| 0x233cf3 | 26 | but Ougi calmly stops her. |
| 0x233d0e | 5 | Look. |
| 0x233d14 | 40 | Ougi points his finger in its direction. |
| 0x233d3d | 49 | Around the giant four-legged beast appear to be\n |
| 0x233d6f | 44 | its guards, following along as they keep a\n |
| 0x233d9c | 8 | lookout. |
| 0x233da5 | 42 | The fact that they're more wary of their\n |
| 0x233dd0 | 46 | surroundings than the beast itself shows how\n |
| 0x233dff | 19 | much they trust it. |
| 0x233e13 | 44 | That means... that thing is from Tuskur as\n |
| 0x233e40 | 8 | well...? |
| 0x233e49 | 26 | They even sent Mukkuru...? |
| 0x233e64 | 24 | You say something, Kuon? |
| 0x233e7d | 36 | Huh!? Uh, no. I didn't say anything! |
| 0x233ea2 | 46 | As I peer at Kuon, I realize that everything\n |
| 0x233ed1 | 45 | is suddenly a little darker. I look back to\n |
| 0x233eff | 6 | find-- |
| 0x233f06 | 13 | ...Wh--Holy-- |
| 0x233f14 | 51 | The beast is right next to us, looming menacingly\n |
| 0x233f48 | 8 | over me. |
| 0x233f51 | 34 | It's stopped right in front of us. |
| 0x233f74 | 27 | Wh-Why is it looking at us? |
| 0x233f90 | 36 | N-N-N-Nekone! Please, get behind me! |
| 0x233fb5 | 40 | I wouldn't make a nice meal, you know?\n |
| 0x233fde | 45 | I recommend something with a little more fat. |
| 0x23400c | 32 | Wh--!? Hey, s-stop pushing me!\n |
| 0x23402d | 28 | And I am definitely NOT fat! |
| 0x23404a | 42 | Suddenly, the back of the beast seems to\n |
| 0x234075 | 9 | bulge up. |
| 0x23407f | 47 | Over the frizzy fur, a girl pokes her face out. |
| 0x2340af | 42 | Even my fear disappears from the surprise. |
| 0x2340da | 47 | She's just as beautiful as the woman with the\n |
| 0x23410a | 6 | wings. |
| 0x234111 | 46 | But she feels a little more... approachable.\n |
| 0x234140 | 43 | A different kind of charm--more mysterious. |
| 0x23416c | 48 | Perched on her shoulder is a small furry white\n |
| 0x23419d | 9 | creature. |
| 0x2341a7 | 7 | *Stare* |
| 0x2341af | 31 | Wait, why is she staring at me? |
| 0x2341cf | 11 | H-Hi there. |
| 0x2341db | 46 | I give in and give her a friendly smile, but\n |
| 0x23420a | 47 | the beast and the girl continue to stare at me. |
| 0x23423a | 25 | This is a little weird... |
| 0x234254 | 43 | I suddenly realize I'm still holding onto\n |
| 0x234280 | 12 | Kuon's hand. |
| 0x23428d | 43 | I look around to see Kuon shrinking back,\n |
| 0x2342b9 | 42 | a guilty expression on her face for some\n |
| 0x2342e4 | 7 | reason. |
| 0x2342ec | 29 | ...What the hell is going on? |
| 0x23430a | 10 | ...*Smile* |
| 0x234315 | 28 | Did she just... smile at me? |
| 0x234332 | 48 | Just as I think that, the giant beast suddenly\n |
| 0x234363 | 27 | turns its huge head around. |
| 0x23437f | 48 | Before I can even figure out the reason behind\n |
| 0x2343b0 | 42 | her smile, the massive feline is already\n |
| 0x2343db | 38 | prowling away, moving down the street. |
| 0x234402 | 47 | And eventually its enormous figure disappears\n |
| 0x234432 | 23 | from our line of sight. |
| 0x23444a | 43 | The bubble of silence pops, and the crowd\n |
| 0x234476 | 35 | immediately begins murmuring again. |
| 0x23449a | 5 | Crowd |
| 0x2344a0 | 33 | What was that!? What WAS that!?\n |
| 0x2344c2 | 21 | That thing was huge!! |
| 0x2344d8 | 46 | Do those things just wander around freely in\n |
| 0x234507 | 26 | the lands across the sea!? |
| 0x234522 | 47 | The crowd's gone from being mesmerized by the\n |
| 0x234552 | 44 | winged woman's beauty to this sudden uproar. |
| 0x23457f | 6 | *Sigh* |
| 0x234586 | 44 | Kuon seems to deflate with a sigh, and she\n |
| 0x2345b3 | 26 | slowly sags to the ground. |
| 0x2345ce | 46 | ...Tuskur, huh. Looks like they're kind of a\n |
| 0x2345fd | 9 | big deal. |
| 0x234607 | 44 | And we're supposed to be the ones guarding\n |
| 0x234634 | 8 | THEM...? |
| 0x23463d | 46 | I can't even imagine what we'll have to deal\n |
| 0x23466c | 7 | with... |

## 8. Formato de saida EXIGIDO
Escreva `translations_22_03.json` com a forma:
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
