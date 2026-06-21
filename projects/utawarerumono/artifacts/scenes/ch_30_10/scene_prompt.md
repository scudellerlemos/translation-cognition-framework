# Cena ch_30_10 — pacote de traducao (489 linhas)

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
| Bokoinante | Personagem | Bokoinante | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Entua | Personagem | Entua | manter_original | major |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Shichirya | Personagem | Shichirya | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
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
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Lord Vurai.` -> `Senhor Vurai.` (Vurai, 30_01)
- `with.` -> `com.` (Homem, 22_08)
- `Yeah.` -> `É.` (Haku, 15_04)
- `Gate guard` -> `Guarda` (Sistema, 14_02)
- `off?` -> `off?` (Haku, 19_06)
- `Speak.` -> `Fale.` (Mikazuchi, 18_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Hmmm...` -> `Hmmm...` (Garota, 19_08)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `command.` -> `ordem.` (Maroro, 18_01)
- `A-Ah...` -> `A-Ah...` (Garota, 15_06)
- `Phew...` -> `Ufa...` (Haku, 12_16)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Yeah, I know.` -> `Sim, eu sei.` (Protagonista, 14_07)
- `Why...` -> `Por...` (Haku, 15_02)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `OSHTOOOOOOOORRRRR!!` -> `OSHTOOOOOOOOOOORRRR!!` (Vurai, 30_11)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `sight.` -> `cena estranha.` (Haku, 13_04)
- `alive.` -> `vivo.` (Man, 11_01)
- `I-I say!?` -> `E-Então!?` (Bokoinante, 20_14)
- `What is going on!?` -> `O que está acontecendo!?` (Homem, 30_01)
- `capital!` -> `na capital!` (Ukon, 13_09)
- `Nyargh!?` -> `Nhargh!?` (Haku, 23_03)
- `YES SIR!` -> `SIM, SENHOR!` (Marinheiro, 23_08)
- `Then--` -> `Então--` (Haku, 14_03)
- `front...` -> `frente...` (Haku, 23_11)
- `Mikazuchi.` -> `Mikazuchi.` (Haku, 19_07)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `Mikado!` -> `Mikado!` (Haku, 19_05)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `city.` -> `a cidade.` (Haku, 14_09)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `Eek!?` -> `Iiih!?` (Rulutieh, 21_03)
- `...Completely empty?` -> `...Completamente vazio?` (Nosuri, 23_15)
- `correct?` -> `certo?` (Oshtor, 22_03)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `Oshtor...` -> `Oshtor...` (Haku, 18_01)
- `first.` -> `primeiro.` (Haku, 13_02)
- `What?` -> `Que?` (Haku, 12_02)
- `Mm?` -> `Hum?` (Protagonista, 20_03)
- `ourselves.` -> `para nós.` (Kuon, 15_02)
- `Lady-in-waiting` -> `Dama de companhia` (Ukon, 30_04)
- `Yes, sir...` -> `Sim, senhor...` (Haku, 19_05)
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
| 0x2fd74d | 6 | I say? |
| 0x2fd754 | 21 | Lord Dekopompo, look! |
| 0x2fd76a | 39 | Ah, the gates... The gates are opening! |
| 0x2fd792 | 45 | Well, they certainly took their sweet time!\n |
| 0x2fd7c0 | 45 | Bokoinante, Maroro! We march inside! Follow\n |
| 0x2fd7ee | 8 | my lead! |
| 0x2fd7f7 | 17 | At once, my lord! |
| 0x2fd809 | 46 | Ah, Master Dekopompo, we are yet unawares of\n |
| 0x2fd838 | 44 | what hath transpired. Let our steps remain\n |
| 0x2fd865 | 13 | light, wary-- |
| 0x2fd873 | 32 | W-Wait! Please! Wait for meeee!! |
| 0x2fd894 | 30 | The gates... have been opened? |
| 0x2fd8b3 | 43 | Raiko's eyes narrow, observing the events\n |
| 0x2fd8df | 10 | unfolding. |
| 0x2fd8ea | 44 | Yes, my lord. By the account of the guards\n |
| 0x2fd917 | 41 | at the gate, it was a direct order from\n |
| 0x2fd941 | 11 | Lord Vurai. |
| 0x2fd94d | 50 | Oh? It would seem that there are others scheming\n |
| 0x2fd980 | 23 | in the shadows, then... |
| 0x2fd998 | 45 | Hmhm. Intriguing. Let us see, then, how far\n |
| 0x2fd9c6 | 13 | they can get. |
| 0x2fd9d4 | 47 | Shichirya chuckles wryly, seeing Raiko's face\n |
| 0x2fda04 | 46 | light up like a child with a new toy to play\n |
| 0x2fda33 | 5 | with. |
| 0x2fda39 | 44 | As usual, your ruthlessness knows no bounds. |
| 0x2fda66 | 46 | I advise waiting and analyzing the situation\n |
| 0x2fda95 | 45 | further before we act, but... What are your\n |
| 0x2fdac3 | 7 | orders? |
| 0x2fdacb | 45 | With the gates open, we have little choice.\n |
| 0x2fdaf9 | 46 | Follow Dekopompo's soldiers inside once they\n |
| 0x2fdb28 | 14 | have advanced. |
| 0x2fdb37 | 15 | As you command. |
| 0x2fdb4b | 48 | I can confirm that the gates have been opened... |
| 0x2fdb7c | 48 | About a thousand footsteps running through the\n |
| 0x2fdbad | 45 | gate and heading to the palace via the main\n |
| 0x2fdbdb | 9 | street... |
| 0x2fdbe5 | 47 | Nosuri grins, lifting her ear from the ground\n |
| 0x2fdc15 | 23 | and rising to her feet. |
| 0x2fdc2d | 47 | ...Impressive as always. All according to plan. |
| 0x2fdc5d | 39 | Guess it's time to make our move, then. |
| 0x2fdc85 | 5 | Yeah. |
| 0x2fdc8b | 44 | We slowly push the carriage forward as the\n |
| 0x2fdcb8 | 40 | guards at the side gate rush over to us. |
| 0x2fdce1 | 10 | Gate guard |
| 0x2fdcec | 47 | You there, with the carriage! Stop right there! |
| 0x2fdd1c | 50 | Where do you intend on going this late at night?\n |
| 0x2fdd4f | 46 | Don't you know the main gate has been closed\n |
| 0x2fdd7e | 4 | off? |
| 0x2fdd83 | 46 | We are here to fulfill the final wish of our\n |
| 0x2fddb2 | 46 | liege before his passing! Now, let us through! |
| 0x2fdde1 | 17 | O-Our liege's...? |
| 0x2fddf3 | 29 | Let this serve as my proof.\n |
| 0x2fde11 | 7 | Behold. |
| 0x2fde19 | 44 | I take out the small box with the Mikado's\n |
| 0x2fde46 | 46 | crest, and hold it aloft. The guards freeze,\n |
| 0x2fde75 | 10 | eyes wide. |
| 0x2fde80 | 45 | That is... That is unmistakably our liege's\n |
| 0x2fdeae | 8 | seal...! |
| 0x2fdeb7 | 31 | P-Please, forgive our rudeness! |
| 0x2fded7 | 44 | They immediately kneel down to the ground,\n |
| 0x2fdf04 | 19 | bowing their heads. |
| 0x2fdf18 | 44 | The guards behind them also hastily follow\n |
| 0x2fdf45 | 5 | suit. |
| 0x2fdf4b | 46 | Holy crap, this thing is way too convenient... |
| 0x2fdf7a | 50 | I wanted to get through without causing a scene,\n |
| 0x2fdfad | 43 | but they'll definitely remember this now... |
| 0x2fdfd9 | 12 | C-Captain... |
| 0x2fdfe6 | 50 | Yes, I know. Messenger of the throne, may I have\n |
| 0x2fe019 | 7 | a word? |
| 0x2fe021 | 6 | Speak. |
| 0x2fe028 | 45 | Regrettably, I must inform you that we must\n |
| 0x2fe056 | 48 | inspect the carriage. My orders compel me, not\n |
| 0x2fe087 | 11 | disrespect. |
| 0x2fe093 | 47 | Hm... That is something I cannot allow. I was\n |
| 0x2fe0c3 | 44 | specifically ordered not to open the seals\n |
| 0x2fe0f0 | 10 | upon them. |
| 0x2fe0fb | 49 | I say again: these are the direct orders of our\n |
| 0x2fe12d | 31 | liege. You will let us through. |
| 0x2fe14d | 46 | We attempt to proceed with our carriage, but\n |
| 0x2fe17c | 46 | as we move, one of the guards notices Nekone\n |
| 0x2fe1ab | 8 | atop it. |
| 0x2fe1b4 | 3 | Hm? |
| 0x2fe1b8 | 41 | You... seem rather small for a soldier... |
| 0x2fe1e2 | 11 | Uh... um... |
| 0x2fe1ee | 7 | Hmmm... |
| 0x2fe1f6 | 44 | I am sorry, but we must check the contents\n |
| 0x2fe223 | 47 | regardless. Such is our duty as guards of the\n |
| 0x2fe253 | 5 | gate. |
| 0x2fe259 | 32 | Tch, guess I'm out of options... |
| 0x2fe27a | 48 | ...Very well. If you insist so, then I suppose\n |
| 0x2fe2ab | 45 | I do not have much of a choice in the matter. |
| 0x2fe2d9 | 48 | Kuon makes eye contact with everyone, and they\n |
| 0x2fe30a | 32 | all silently move into position. |
| 0x2fe32b | 17 | Very well. Then-- |
| 0x2fe33d | 44 | However! I will have to report this to the\n |
| 0x2fe36a | 45 | current guardian of Her Highness, Lord Vurai. |
| 0x2fe398 | 44 | If you are unlucky, you may incur not only\n |
| 0x2fe3c5 | 45 | the anger of Lord Vurai, but Yamato's heir.\n |
| 0x2fe3f3 | 13 | You are sure? |
| 0x2fe401 | 4 | Huh? |
| 0x2fe406 | 48 | Just as you must carry out your duty as guards\n |
| 0x2fe437 | 44 | of the gate, I must uphold my own imperial\n |
| 0x2fe464 | 8 | command. |
| 0x2fe46d | 7 | A-Ah... |
| 0x2fe475 | 49 | The gate guard hesitates for a moment, his eyes\n |
| 0x2fe4a7 | 46 | on me... and he eventually nods, backing down. |
| 0x2fe4d6 | 30 | ...Understood. Open the gates. |
| 0x2fe4f5 | 30 | Y-Yes sir... Open the gates!\n |
| 0x2fe514 | 15 | Open the gates! |
| 0x2fe524 | 49 | As we finally pass through the gate, Atuy pokes\n |
| 0x2fe556 | 31 | her head out from the carriage. |
| 0x2fe576 | 43 | Hee hee, looks like it went off without a\n |
| 0x2fe5a2 | 6 | hitch. |
| 0x2fe5a9 | 32 | I suppose we somehow managed it. |
| 0x2fe5ca | 48 | For now, anyway. God, I thought I was going to\n |
| 0x2fe5fb | 20 | have a heart attack. |
| 0x2fe610 | 48 | I'm sure if Ougi were here, he would've pulled\n |
| 0x2fe641 | 26 | this off a lot smoother... |
| 0x2fe65c | 30 | So how do the main gates look? |
| 0x2fe67b | 48 | Just as we expected. It looks like total chaos\n |
| 0x2fe6ac | 11 | over there. |
| 0x2fe6b8 | 49 | Judging by how things are going, I doubt anyone\n |
| 0x2fe6ea | 16 | would notice us. |
| 0x2fe6fb | 24 | Rulie, now's our chance. |
| 0x2fe714 | 12 | Yes. Cocopo? |
| 0x2fe735 | 45 | At Rulutieh's word, the carriage speeds up,\n |
| 0x2fe763 | 41 | trundling across the road into the night. |
| 0x2fe78d | 7 | Phew... |
| 0x2fe795 | 50 | I rest my back against the edge of the carriage,\n |
| 0x2fe7c8 | 24 | a huge sigh escaping me. |
| 0x2fe7e1 | 5 | Haku? |
| 0x2fe7e7 | 13 | Yeah, I know. |
| 0x2fe7f5 | 38 | Still too early to celebrate just yet. |
| 0x2fe81c | 6 | tuzura |
| 0x2fe824 | 10 | tuzura_kin |
| 0x2fe82f | 11 | tuzura_futa |
| 0x2fe83b | 16 | Ngh... Guhhhh... |
| 0x2fe84c | 6 | Why... |
| 0x2fe853 | 24 | Why... do I yet live...? |
| 0x2fe86c | 45 | Why... did you not end my life when you had\n |
| 0x2fe89a | 14 | the chance...? |
| 0x2fe8a9 | 15 | Was it pity...? |
| 0x2fe8b9 | 16 | Was it mercy...? |
| 0x2fe8ca | 26 | You would spare my life... |
| 0x2fe8e5 | 34 | Why do you mock me so... Oshtor... |
| 0x2fe908 | 21 | WRRRRAAAAAAAAGGHHHH!! |
| 0x2fe91e | 22 | OSHTOOOOOOOOOORRRRRR!! |
| 0x2fe935 | 50 | Vurai leaps upward, soaring into the pitch-black\n |
| 0x2fe968 | 46 | sky. His eyes can no longer see anything but\n |
| 0x2fe997 | 7 | Oshtor. |
| 0x2fe99f | 28 | WHERE!? WHERE ARE YOU...!?\n |
| 0x2fe9bc | 19 | OSHTOOOOOOOORRRRR!! |
| 0x2fe9d0 | 40 | With his powerful body, he bounds over\n |
| 0x2fe9f9 | 45 | unbelievable distances, easily leaping over\n |
| 0x2fea27 | 20 | the palace rooftops. |
| 0x2fea3c | 42 | And finally... he hits the ground with a\n |
| 0x2fea67 | 38 | terrible impact born of immense speed. |
| 0x2fea8e | 7 | Soldier |
| 0x2fea96 | 25 | H-Halt! All of you, halt! |
| 0x2feab0 | 24 | Wh-What was that noise!? |
| 0x2feac9 | 27 | It was... something huge!\n |
| 0x2feae5 | 21 | It came from the sky! |
| 0x2feafb | 47 | The soldiers heading toward the palace cannot\n |
| 0x2feb2b | 40 | hide their unease at the sudden descent. |
| 0x2feb54 | 48 | As the dust begins to clear... they slowly see\n |
| 0x2feb85 | 39 | the outline of Vurai's gargantuan body. |
| 0x2febad | 13 | L-Lord Vurai? |
| 0x2febbb | 30 | Th-That form... You mustn't!\n |
| 0x2febda | 27 | We are within the palace... |
| 0x2febf6 | 14 | STAND ASIDE... |
| 0x2fec05 | 45 | With one swing of his arm, the heads of the\n |
| 0x2fec33 | 47 | surrounding soldiers burst like overripe fruit. |
| 0x2fec63 | 41 | WHERE ARE YOU...? WHERE ARE YOU, OSHTOR!? |
| 0x2fec8d | 42 | A little ways off, on a nearby mansion's\n |
| 0x2fecb8 | 10 | rooftop... |
| 0x2fecc3 | 45 | Two small figures are looking down upon the\n |
| 0x2fecf1 | 29 | chaos surrounding the palace. |
| 0x2fed0f | 43 | One of the figures chuckles mildly at the\n |
| 0x2fed3b | 6 | sight. |
| 0x2fed42 | 26 | That is... General Vurai!? |
| 0x2fed5d | 44 | My. I didn't expect that he would still be\n |
| 0x2fed8a | 6 | alive. |
| 0x2fed91 | 47 | Wh-What do we do? The others have barely left\n |
| 0x2fedc1 | 12 | the gates... |
| 0x2fedce | 45 | Let's see. Perhaps it would be best to have\n |
| 0x2fedfc | 35 | him linger where he is, for a time. |
| 0x2fee20 | 45 | Oh noooo! 'Tis rebellion! General Vurai has\n |
| 0x2fee4e | 26 | turned against the throne! |
| 0x2fee69 | 11 | O-Oh. Ah... |
| 0x2fee75 | 44 | V-Vurai intends on claiming the throne for\n |
| 0x2feea2 | 8 | himself! |
| 0x2feeab | 48 | That's what I heard too! They say he's keeping\n |
| 0x2feedc | 45 | Her Highness locked up somewhere inside the\n |
| 0x2fef0a | 8 | palace!! |
| 0x2fef13 | 9 | I-I say!? |
| 0x2fef1d | 18 | WHAT IS GOING ON!? |
| 0x2fef30 | 39 | A rebellion!? How dare he devise such\n |
| 0x2fef58 | 12 | treachery... |
| 0x2fef65 | 43 | W-We have not yet ensured the veracity of-- |
| 0x2fef91 | 48 | Still, I would not put it past him to go so far. |
| 0x2fefc2 | 41 | Yes, absolutely right. This has to be a\n |
| 0x2fefec | 10 | rebellion! |
| 0x2feff7 | 46 | Curse you, Vurai... How dare you commit such\n |
| 0x2ff026 | 41 | savage crime during my absence from the\n |
| 0x2ff050 | 8 | capital! |
| 0x2ff059 | 8 | Nyargh!? |
| 0x2ff062 | 8 | Soldiers |
| 0x2ff06b | 12 | Arrrrrrrgh!! |
| 0x2ff078 | 16 | Th-Th-This is... |
| 0x2ff089 | 20 | O-O unhappy fortune! |
| 0x2ff09e | 45 | Master Dekopompo! Please, recall the troops\n |
| 0x2ff0cc | 42 | thou sent forward! The danger is far too\n |
| 0x2ff0f7 | 6 | great! |
| 0x2ff0fe | 46 | Call them back!? What are you talking about,\n |
| 0x2ff12d | 11 | you moron!? |
| 0x2ff139 | 45 | If we let this--this TRAITOR off like this,\n |
| 0x2ff167 | 47 | we shame the name of the Eight Pillar Generals! |
| 0x2ff197 | 46 | Do you hear!? He is a traitor, and no longer\n |
| 0x2ff1c6 | 46 | one of us! Bokoinante, take the soldiers and\n |
| 0x2ff1f5 | 11 | find Vurai! |
| 0x2ff201 | 8 | Yes sir! |
| 0x2ff20a | 47 | N-No! Please, desist! Such a course will only\n |
| 0x2ff23a | 33 | bring greater casualties upon us! |
| 0x2ff25c | 45 | P-Please, Lord Vurai, you must calm yourself! |
| 0x2ff28a | 35 | We are within the palace grounds!\n |
| 0x2ff2ae | 21 | You must not do this! |
| 0x2ff2c4 | 30 | YOU STAND IN MY WAY... BEGONE! |
| 0x2ff2e3 | 6 | Ahhhh! |
| 0x2ff2ea | 46 | Suddenly, a loud crack of thunder interrupts\n |
| 0x2ff319 | 19 | the roaring flames. |
| 0x2ff32d | 44 | When the blinding lightning fades, an even\n |
| 0x2ff35a | 50 | blacker darkness and a silence fills the area...\n |
| 0x2ff38d | 6 | Then-- |
| 0x2ff394 | 6 | RRGH!? |
| 0x2ff39b | 45 | Vurai's glare falls upon a figure holding a\n |
| 0x2ff3c9 | 47 | giant sword, crackling clouds sparking behind\n |
| 0x2ff3f9 | 9 | his back. |
| 0x2ff403 | 43 | I rush back, hearing that Yamato is going\n |
| 0x2ff42f | 43 | through a crisis... and what do I stumble\n |
| 0x2ff45b | 7 | across? |
| 0x2ff463 | 29 | Oh...! It's Lord Mikazuchi!\n |
| 0x2ff481 | 27 | He has come to save us all! |
| 0x2ff49d | 45 | Yes... If anyone could stop him, it must be\n |
| 0x2ff4cb | 18 | Lord Mikazuchi...! |
| 0x2ff4de | 50 | What!? Mikazuchi!? Curses... Is he here to steal\n |
| 0x2ff511 | 26 | away my glory once again!? |
| 0x2ff52c | 48 | Ah. Just in time for the festival, my unworthy\n |
| 0x2ff55d | 47 | brother. Such a swift return from the western\n |
| 0x2ff58d | 8 | front... |
| 0x2ff596 | 49 | You have my praise. A pleasant surprise indeed,\n |
| 0x2ff5c8 | 47 | to see you hurry back into the palm of my hand. |
| 0x2ff5f8 | 50 | Have you gone mad, Vurai? Pillar General or not,\n |
| 0x2ff62b | 41 | such a crime... demands cold retribution. |
| 0x2ff655 | 37 | SO YOU TOO WOULD STAND IN MY WAY...\n |
| 0x2ff67b | 10 | MIKAZUCHI. |
| 0x2ff686 | 48 | Indeed, for strange rumors have reached my ears. |
| 0x2ff6b7 | 48 | Vurai... do they speak the truth when they say\n |
| 0x2ff6e8 | 33 | you have imprisoned Her Highness? |
| 0x2ff70a | 8 | WHAT...? |
| 0x2ff713 | 26 | I will have your answer.\n |
| 0x2ff72e | 17 | Speak with care-- |
| 0x2ff740 | 47 | For your answer... may force me to shred that\n |
| 0x2ff770 | 37 | fearsome body of yours into ribbons!! |
| 0x2ff796 | 43 | THE SUN I HAD LIVED UNDER FOR SO LONG HAS\n |
| 0x2ff7c2 | 6 | SET... |
| 0x2ff7c9 | 38 | THE SUN THAT BATHED ME IN LIGHT, AND\n |
| 0x2ff7f0 | 22 | ILLUMINATED MY PATH... |
| 0x2ff807 | 31 | THE SUN WE CALLED THE MIKADO... |
| 0x2ff827 | 37 | ...A SUN MUST SHINE DOWN UPON YAMATO. |
| 0x2ff84d | 40 | THE HEAVENS CALL! THEY DESIRE A NEW SUN! |
| 0x2ff876 | 48 | The sun may sink, but it will ever rise again.\n |
| 0x2ff8a7 | 38 | And this new sun will be Her Highness. |
| 0x2ff8ce | 15 | HA... HAHAHA... |
| 0x2ff8de | 38 | SUCH A WEAK CHILD IS TO BECOME MY SUN? |
| 0x2ff905 | 8 | ABSURD!! |
| 0x2ff90e | 46 | ...Hah. If our liege is the radiant sun, Her\n |
| 0x2ff93d | 45 | Highness is the Timanonna, the sun's flower\n |
| 0x2ff96b | 24 | that brings joy to all.  |
| 0x2ff984 | 49 | I know her brilliant light will bring peace and\n |
| 0x2ff9b6 | 24 | prosperity to this land. |
| 0x2ff9cf | 9 | RRRRGH... |
| 0x2ff9d9 | 47 | And you tell me that you have not come to see\n |
| 0x2ffa09 | 33 | this? How blind can your eyes be? |
| 0x2ffa2b | 47 | And what is more, you dare to tread upon this\n |
| 0x2ffa5b | 18 | precious flower... |
| 0x2ffa6e | 9 | Hmhmhm... |
| 0x2ffa78 | 21 | ...Heh heh heh heh... |
| 0x2ffa8e | 27 | AHAHAHAHAHAHAHAHAHAHAHAHA!! |
| 0x2ffaaa | 53 | YOU WILL NEVER,{W90} EVER REPLACE THE MIKADO,{W105}\n |
| 0x2ffae0 | 25 | YOU SICK SON OF A BITCH!! |
| 0x2ffafa | 27 | Abuh-buh-buh-buh-buh-buh... |
| 0x2ffb16 | 48 | H-H-H-How hath such dire course befallen us...!? |
| 0x2ffb47 | 47 | What are you idiots just standing there for!?\n |
| 0x2ffb77 | 33 | We need to get out of here, fast! |
| 0x2ffb99 | 12 | Aye, master! |
| 0x2ffba6 | 47 | B-But were you not just saying that you would\n |
| 0x2ffbd6 | 40 | be the one to capture Vurai, my lord...? |
| 0x2ffbff | 38 | Now is NOT the time! Hurry up, fool!\n |
| 0x2ffc26 | 44 | If those two monsters want to duke it out,\n |
| 0x2ffc53 | 24 | I intend to be far away! |
| 0x2ffc6c | 38 | Y-Yes, a point well made... Of course. |
| 0x2ffc93 | 7 | Nyargh! |
| 0x2ffc9b | 29 | A-A moment, Master Dekopompo! |
| 0x2ffcb9 | 42 | What!? What are you blathering about now!? |
| 0x2ffce4 | 46 | W-W-Well... by such testimony overheard, Her\n |
| 0x2ffd13 | 47 | Highness may yet be imprison'd in the palace... |
| 0x2ffd43 | 6 | Nyah!? |
| 0x2ffd4a | 43 | Now that you mention it, I do recall them\n |
| 0x2ffd76 | 29 | saying something of the sort. |
| 0x2ffd94 | 11 | N-Nyergh... |
| 0x2ffda0 | 46 | If such oaths be true, then 'tis our duty to\n |
| 0x2ffdcf | 23 | fly to her aid at once! |
| 0x2ffde7 | 44 | D-Don't be an idiot! If we even try to get\n |
| 0x2ffe14 | 45 | close to the palace now, we'll be caught in\n |
| 0x2ffe42 | 13 | their battle! |
| 0x2ffe50 | 39 | Please wait a moment, Lord Dekopompo.\n |
| 0x2ffe78 | 46 | I believe that Maroro has the right of things! |
| 0x2ffea7 | 6 | Y-Yea? |
| 0x2ffeae | 5 | Nyuh? |
| 0x2ffeb4 | 40 | Think of it this way. This is a golden\n |
| 0x2ffedd | 12 | opportunity! |
| 0x2ffeea | 49 | While everyone scrambles in this chaos, you can\n |
| 0x2fff1c | 49 | be the one to rescue Her Highness with your own\n |
| 0x2fff4e | 6 | hands! |
| 0x2fff55 | 27 | M-Me, rescue Her Highness!? |
| 0x2fff71 | 50 | Indeed! Her Highness will swoon at your bravery!\n |
| 0x2fffa4 | 50 | You shall be as a charming prince, riding to her\n |
| 0x2fffd7 | 4 | aid! |
| 0x2fffdc | 11 | N-Nyeh heh! |
| 0x2fffe8 | 49 | And having won the Princess's heart, it is only\n |
| 0x30001a | 44 | a matter of time until you become the next\n |
| 0x300047 | 7 | Mikado! |
| 0x30004f | 33 | M-Mikado...? Me, the... Mikado... |
| 0x300071 | 38 | And being his right hand man... Oho!\n |
| 0x300098 | 24 | What a promotion for me! |
| 0x3000b1 | 32 | Nyeh... Nyeh heh hyeh heh heh... |
| 0x3000d2 | 20 | Oho, ohoo hoo hoo... |
| 0x3000e7 | 50 | W-Wait, the both of you! That was not the thrust\n |
| 0x30011a | 7 | of my-- |
| 0x300122 | 36 | Bokoinante, Maroro, we head forward. |
| 0x300147 | 46 | Follow my lead! We shall rescue Her Highness\n |
| 0x300176 | 13 | at any cost!! |
| 0x300184 | 27 | Yes, milord! With pleasure! |
| 0x3001a0 | 43 | Waugh!? N-No! I meant not such outrageous\n |
| 0x3001cc | 39 | schemes! Oh, how hath it come to this!? |
| 0x3001f4 | 34 | ...What will you do next, my lord? |
| 0x300217 | 41 | All within expectations. Leave them be.\n |
| 0x300241 | 47 | Declare martial law at once, and evacuate the\n |
| 0x300271 | 22 | surrounding districts. |
| 0x300288 | 11 | Understood. |
| 0x300294 | 8 | HYAAAH!! |
| 0x30029d | 14 | HRRRRAAAAAGH!! |
| 0x3002ac | 42 | Mikazuchi's slashes are vicious blurs of\n |
| 0x3002d7 | 46 | lightning, and Vurai's fists turn to crimson\n |
| 0x300306 | 7 | flames. |
| 0x30030e | 15 | GRRRAAAAAGGHH!! |
| 0x30031e | 6 | Nghh!! |
| 0x300325 | 47 | Vurai puts all his force into each punch, and\n |
| 0x300355 | 47 | Mikazuchi's blade clashes against it. Neither\n |
| 0x300385 | 12 | one falters. |
| 0x300392 | 50 | But as they battle... their flames and lightning\n |
| 0x3003c5 | 49 | lash out, setting homes ablaze and damaging the\n |
| 0x3003f7 | 5 | city. |
| 0x3003fd | 46 | Raiko watches their duel raging, a cold look\n |
| 0x30042c | 12 | in his eyes. |
| 0x300439 | 50 | Yes, that's it... Fight to your heart's content,\n |
| 0x30046c | 36 | Vurai... and you as well, Mikazuchi. |
| 0x300491 | 49 | Your flames and lightning shall be the balefire\n |
| 0x3004c3 | 46 | that lights the new Yamato, rebuilt atop the\n |
| 0x3004f2 | 6 | old... |
| 0x3004f9 | 48 | Hah... phew... hahh... P-Please wait a moment,\n |
| 0x30052a | 15 | Lord Dekopompo! |
| 0x30053a | 30 | Please, master, calm thyself!! |
| 0x300559 | 41 | Argh, shut it! And get your hands off me! |
| 0x300583 | 47 | Tch... damnable swine. It seems he has made a\n |
| 0x3005b3 | 29 | habit of getting in my way... |
| 0x3005d1 | 48 | You! Vurai! Where have you hidden Her Highness!? |
| 0x300602 | 6 | What!? |
| 0x300609 | 9 | HRNGH...? |
| 0x300613 | 4 | Eep! |
| 0x300618 | 47 | The two warriors pause, glaring at Dekopompo,\n |
| 0x300648 | 41 | who hastily grabs Bokoinante as a shield. |
| 0x300672 | 5 | Eek!? |
| 0x300678 | 46 | Bokoinante, in turn, quickly grabs Maroro as\n |
| 0x3006a7 | 16 | a shield-shield. |
| 0x3006b8 | 27 | Gah! Wha--P-Please--Zounds! |
| 0x3006d4 | 40 | Dekopompo's gut bulges from behind his\n |
| 0x3006fd | 46 | subordinates as he points a trembling finger\n |
| 0x30072c | 9 | at Vurai. |
| 0x300736 | 47 | I-I-I-I-I am asking where you have hidden Her\n |
| 0x300766 | 40 | Highness! H-Her sleeping quarters were\n |
| 0x30078f | 17 | completely empty! |
| 0x3007a1 | 20 | ...Completely empty? |
| 0x3007b6 | 45 | Shichirya. Our sources said that Oshtor had\n |
| 0x3007e4 | 45 | been imprisoned and was being interrogated,\n |
| 0x300812 | 8 | correct? |
| 0x30081b | 42 | Yes. I have received reports that he had\n |
| 0x300846 | 37 | sustained heavy injuries as a result. |
| 0x30086c | 9 | ...I see. |
| 0x300876 | 44 | The princess's dog still had fangs to bite\n |
| 0x3008a3 | 25 | back... Quite impressive. |
| 0x3008bd | 41 | Yet all things have their consequences,\n |
| 0x3008e7 | 9 | Oshtor... |
| 0x3008f1 | 49 | The winds had been blowing still for this long,\n |
| 0x300923 | 42 | but it was your spark that drove them to\n |
| 0x30094e | 9 | ignite... |
| 0x300958 | 20 | ...the fires of war. |
| 0x30096d | 42 | Meanwhile, Vurai continues to stare down\n |
| 0x300998 | 41 | Dekopompo, eyes filled with burning rage. |
| 0x3009c2 | 28 | Nyeh, nyah-ha-ha-ha... ha... |
| 0x3009df | 12 | O-O-Ooogh... |
| 0x3009ec | 12 | E-E-Eeegh... |
| 0x3009f9 | 44 | But Vurai suddenly turns his back on them,\n |
| 0x300a26 | 33 | heading instead toward the gates. |
| 0x300a48 | 32 | Where do you think you're going? |
| 0x300a69 | 35 | Answer me. Where is Her Highness?\n |
| 0x300a8d | 28 | If you refuse to answer me-- |
| 0x300aaa | 46 | ...THERE IS A MAN I MUST SETTLE THINGS WITH,\n |
| 0x300ad9 | 6 | FIRST. |
| 0x300ae0 | 5 | What? |
| 0x300ae6 | 15 | ...STAND ASIDE. |
| 0x300af6 | 10 | Mikazuchi. |
| 0x300b01 | 3 | Mm? |
| 0x300b05 | 46 | We do not have time to waste on the likes of\n |
| 0x300b34 | 49 | him. We must confirm the safety of Her Highness\n |
| 0x300b66 | 10 | ourselves. |
| 0x300b71 | 30 | Let him go. He matters little. |
| 0x300b90 | 47 | Mikazuchi faces towards Vurai once more, eyes\n |
| 0x300bc0 | 41 | locked on his back with a venomous glare. |
| 0x300bea | 45 | After a long silence, he sheathes his sword\n |
| 0x300c18 | 44 | brusquely, as if to sever the rage burning\n |
| 0x300c45 | 11 | within him. |
| 0x300c51 | 17 | Leave this place. |
| 0x300c63 | 43 | Vurai remains silent, and begins striding\n |
| 0x300c8f | 42 | forward without looking back at Mikazuchi. |
| 0x300cba | 50 | Once beyond the main gate, he takes a great leap\n |
| 0x300ced | 45 | and disappears into the dark expanse of the\n |
| 0x300d1b | 10 | night sky. |
| 0x300d26 | 44 | With that last murmur, Mikazuchi turns and\n |
| 0x300d53 | 28 | walks into the palace alone. |
| 0x300d70 | 47 | Continue your mad dash, Vurai. From the chaos\n |
| 0x300da0 | 45 | you sow in your wake, a new era will be born. |
| 0x300dce | 15 | Lady-in-waiting |
| 0x300dde | 48 | How could this be...? General Vurai was still... |
| 0x300e0f | 49 | Entua stands there in awe, having witnessed the\n |
| 0x300e41 | 42 | fierce battle between Mikazuchi and Vurai. |
| 0x300e6c | 47 | Her Highness and the others... They are still\n |
| 0x300e9c | 10 | unaware... |
| 0x300ea7 | 49 | I must warn them immediately! Lord Oshtor would\n |
| 0x300ed9 | 36 | be no match in the state he is in... |
| 0x300efe | 49 | She quickly leaps astride a steed that had lost\n |
| 0x300f30 | 43 | its rider in the preceding chaos, swiftly\n |
| 0x300f5c | 11 | riding out. |
| 0x300f68 | 35 | Please forgive me, Lady Honoka...\n |
| 0x300f8c | 23 | I pray for your safety. |
| 0x300fa4 | 44 | Reporting, Lord Raiko. On the local damage\n |
| 0x300fd1 | 46 | sustained during the battle between Generals\n |
| 0x301000 | 21 | Vurai and Mikazuchi-- |
| 0x301016 | 44 | Many structures took heavy damage, but the\n |
| 0x301043 | 46 | swift evacuation kept civilian casualties to\n |
| 0x301072 | 10 | a minimum. |
| 0x30107d | 9 | ...Noted. |
| 0x301087 | 43 | Now, what will it be, Oshtor? Will you be\n |
| 0x3010b3 | 48 | incinerated by Vurai's fire? Or will you again\n |
| 0x3010e4 | 19 | stand before me...? |
| 0x3010f8 | 48 | Whatever the result, it seems we must readjust\n |
| 0x301129 | 25 | our schedule accordingly. |
| 0x301143 | 12 | You mean...? |
| 0x301150 | 46 | It is time to make our next move. Shichirya,\n |
| 0x30117f | 34 | you are prepared in mind and body? |
| 0x3011a2 | 23 | As you wish, my lord... |
| 0x3011ba | 42 | I see. So Oshtor has taken Her Highness... |
| 0x3011e5 | 11 | Yes, sir... |
| 0x3011f1 | 40 | I understand your feelings, Lord Woshis. |
| 0x30121a | 47 | We have already made arrangements to send out\n |
| 0x30124a | 36 | messengers to the surrounding areas. |
| 0x30126f | 42 | We shall find Her Highness without fail.\n |
| 0x30129a | 32 | No stone shall be left unturned. |
| 0x3012bb | 17 | Yes... Thank you. |
| 0x3012cd | 49 | Woshis continues to gaze at the ground until he\n |
| 0x3012ff | 48 | rises slowly, his eyes bleak as he looks around. |
| 0x301330 | 45 | Within the room destroyed by Vurai's wrath,\n |
| 0x30135e | 46 | nothing remains but the low howl of the cold\n |
| 0x30138d | 13 | night's wind. |
| 0x30139b | 21 | A storm is brewing... |
| 0x3013b1 | 47 | A great storm is coming. One that will engulf\n |
| 0x3013e1 | 47 | all of Yamato, one that will drive its people\n |
| 0x301411 | 8 | apart... |
| 0x30141a | 35 | One that is now beyond our control. |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_10.json` com a forma:
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
