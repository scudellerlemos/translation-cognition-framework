# Cena ch_30_01 — pacote de traducao (367 linhas)

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
| Divine Scion | Titulo | Descendente Divino | traduzir | moderate |
| Girl | UI | Garota | traduzir | none |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Vurai | Personagem | Vurai | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| Woshis | Personagem | Woshis | manter_original | major |
| Yamato | Local | Yamato | manter_original | none |
| Yatanawarabe | Termo | Yatanawarabe | manter_original | none |

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
- `you.` -> `isso.` (Nekone, 15_03)
- `me...` -> `mim...` (Haku, 11_03)
- `to.` -> `a.` (Protagonista, 19_08)
- `to you.` -> `com você.` (Ukon, 13_02)
- `together.` -> `juntas.` (Haku, 20_07)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `W-Well...` -> `B-Bem...` (Kuon, 17_01)
- `What?` -> `Que?` (Haku, 12_02)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `And...` -> `E...` (Haku, 12_17)
- `anyone.` -> `ninguém.` (Kuon, 13_03)
- `Ah!?` -> `Ah!?` (Rulutieh, 14_04)
- `Eek!?` -> `Iiih!?` (Rulutieh, 21_03)
- `wouldn't you agree?` -> `não é verdade?` (Rulutieh, 17_01)
- `forever.` -> `para sempre.` (Rulutieh, 19_06)
- `chest.` -> `peito.` (Atuy, 16_01)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `Your Highness?` -> `Alteza?` (Garota ou Nosuri, 18_05)
- `Wh--` -> `Q--` (Haku, 11_07)
- `quickly.` -> `rapidamente.` (Nosuri/narração, 17_02)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `right.` -> `direito.` (Kuon, 11_01)
- `I see...` -> `Entendo...` (Haku, 11_02)
- `trouble. ` -> `de verdade.` (Haku, 11_01)
- `to him.` -> `para ele.` (Haku, 22_04)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Gah!` -> `Ai!` (Man, 11_01)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `Yes, sir.` -> `Sim, senhor.` (Bokoinante, 20_14)
- `expression.` -> `natural.` (Haku, 15_01)
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
| 0x2c4ebd | 46 | The Mikado's body has been laid out in state\n |
| 0x2c4eec | 24 | in the audience chamber. |
| 0x2c4f05 | 48 | Around his casket, mourners have left flowers,\n |
| 0x2c4f36 | 47 | expressing their grief at their lord's death... |
| 0x2c4f66 | 49 | A proper funeral ceremony will be held when the\n |
| 0x2c4f98 | 48 | generals abroad in Tuskur return to the capital. |
| 0x2c4fc9 | 25 | Hic... *sob*... Father... |
| 0x2c4fe3 | 46 | Anju leans on the casket, sobbing openly and\n |
| 0x2c5012 | 13 | inconsolably. |
| 0x2c5020 | 45 | B-But--I spoke to you i-in the morning, and\n |
| 0x2c504e | 28 | you were just f-fine, and... |
| 0x2c506b | 48 | Y-You patted my head, and... smiled at me like\n |
| 0x2c509c | 16 | you always do... |
| 0x2c50ad | 12 | Why? Why...? |
| 0x2c50ba | 14 | Unh... Uaaah!! |
| 0x2c50c9 | 48 | Various retainers and ladies of the court look\n |
| 0x2c50fa | 26 | on in sorrow, heads bowed. |
| 0x2c5115 | 32 | Your Highness. We should return. |
| 0x2c5136 | 43 | Oshtor gently helps Anju to her feet, and\n |
| 0x2c5162 | 46 | finally, the princess takes a step back from\n |
| 0x2c5191 | 11 | the casket. |
| 0x2c519d | 6 | Unh... |
| 0x2c51a4 | 44 | Anju looks up at Oshtor, eyes full of tears. |
| 0x2c51d1 | 40 | Oshtor... Wh-What is to become of me...? |
| 0x2c51fa | 31 | Without... Without Father, I... |
| 0x2c521a | 49 | Oshtor kneels down before Anju, putting himself\n |
| 0x2c524c | 22 | on eye-level with her. |
| 0x2c5263 | 7 | Nnh...? |
| 0x2c526b | 48 | What you must do, Your Highness, is to live as\n |
| 0x2c529c | 49 | your father wanted. To guide the people he left\n |
| 0x2c52ce | 4 | you. |
| 0x2c52d3 | 50 | Now, dry your tears. My liege would surely laugh\n |
| 0x2c5306 | 33 | to see you in such a sorry state. |
| 0x2c5328 | 47 | I-I cannot... S-Such a thing is... far beyond\n |
| 0x2c5358 | 5 | me... |
| 0x2c535e | 45 | I th-thought I wouldn't succeed him f-for a\n |
| 0x2c538c | 15 | long time, yet. |
| 0x2c539c | 44 | I know naught of... g-governance, nor war,\n |
| 0x2c53c9 | 8 | n-nor... |
| 0x2c53d2 | 44 | I cannot. I can't. It's just i-impossible... |
| 0x2c53ff | 16 | Your Highness... |
| 0x2c5410 | 47 | As the two of them speak, a pair of eyes from\n |
| 0x2c5440 | 35 | a nearby hallway settles upon them. |
| 0x2c5464 | 7 | Vurai-- |
| 0x2c546c | 46 | A mononofu known as the Vanguard, one of the\n |
| 0x2c549b | 44 | Eight Pillars. A man who prides himself on\n |
| 0x2c54c8 | 13 | his strength. |
| 0x2c54d6 | 47 | His ordinarily stony face wears an expression\n |
| 0x2c5506 | 21 | of anger and disgust. |
| 0x2c551c | 21 | What is that...thing? |
| 0x2c5532 | 47 | That whelp, weeping and mewling into Oshtor's\n |
| 0x2c5562 | 33 | arms, careless of who sees her... |
| 0x2c5584 | 48 | It is the way of things that an imperial scion\n |
| 0x2c55b5 | 26 | should inherit the throne. |
| 0x2c55d0 | 42 | But a whimpering babe, unable to contain\n |
| 0x2c55fb | 8 | herself? |
| 0x2c5604 | 43 | THIS is who I am to call my divine liege,\n |
| 0x2c5630 | 10 | my Mikado? |
| 0x2c563b | 50 | I care not whether she's a girl or an old woman,\n |
| 0x2c566e | 50 | so long as she is someone worth pledging my soul\n |
| 0x2c56a1 | 3 | to. |
| 0x2c56a5 | 43 | But it is not this helpless, weeping child. |
| 0x2c56d1 | 29 | What are you doing? Stand up. |
| 0x2c56ef | 44 | Stand and rule. Command us to assemble and\n |
| 0x2c571c | 17 | kneel before you. |
| 0x2c572e | 44 | If you are unable to do even that much, I... |
| 0x2c575b | 43 | Vurai grits his teeth tightly, watching on. |
| 0x2c5787 | 11 | And Oshtor. |
| 0x2c5793 | 45 | It seems the child has taken a great liking\n |
| 0x2c57c1 | 7 | to you. |
| 0x2c57c9 | 48 | Should she succeed my liege, your place in her\n |
| 0x2c57fa | 33 | court is surely secure hereafter. |
| 0x2c581c | 47 | You'll be free to pander to her all you like.\n |
| 0x2c584c | 13 | I, however... |
| 0x2c585a | 41 | Vurai clenches his fists, grinding them\n |
| 0x2c5884 | 9 | together. |
| 0x2c588e | 51 | Let it be known that Vurai will never sway before\n |
| 0x2c58c2 | 47 | one who licks the shoes of a pretender empress. |
| 0x2c58f2 | 23 | Yatanawarabe Shyasurika |
| 0x2c590a | 46 | Lord Woshis, the Mikado's autopsy is complete. |
| 0x2c5939 | 34 | I see. Thank you for informing me. |
| 0x2c595c | 6 | ...Hm? |
| 0x2c5963 | 48 | Vurai turns toward the source of whispering to\n |
| 0x2c5994 | 41 | find Woshis and one of his Yatanawarabe\n |
| 0x2c59be | 11 | conversing. |
| 0x2c59ca | 50 | They both keep their voices low, speaking behind\n |
| 0x2c59fd | 39 | a pillar to avoid attracting attention. |
| 0x2c5a25 | 30 | And? Have they found anything? |
| 0x2c5a44 | 45 | Yes... I'm afraid so. Our liege's death was\n |
| 0x2c5a72 | 23 | a product of poisoning. |
| 0x2c5a8a | 16 | Poison... I see. |
| 0x2c5a9f | 48 | Traces of an identical toxin were found in our\n |
| 0x2c5ad0 | 45 | liege's last meal. This is undoubtedly what\n |
| 0x2c5afe | 10 | ended him. |
| 0x2c5b09 | 43 | But how? The ingredients of his meals are\n |
| 0x2c5b35 | 42 | screened, tested multiple times, tasted... |
| 0x2c5b60 | 43 | Nobody could slip something into his food\n |
| 0x2c5b8c | 22 | without someone noti-- |
| 0x2c5ba3 | 46 | Woshis abruptly cuts himself off, looking up\n |
| 0x2c5bd2 | 24 | with eyes wide in shock. |
| 0x2c5beb | 44 | Lady Honoka. Where is Lady Honoka right now? |
| 0x2c5c18 | 21 | Yatanawarabe Liveruni |
| 0x2c5c2e | 9 | W-Well... |
| 0x2c5c38 | 43 | We've been searching for her with all the\n |
| 0x2c5c64 | 45 | manpower we can spare... To no avail, so far. |
| 0x2c5c92 | 5 | What? |
| 0x2c5c98 | 44 | That cannot possibly... Lady Honoka is the\n |
| 0x2c5cc5 | 24 | last person who would... |
| 0x2c5cde | 46 | This, ah... This is difficult for me to say... |
| 0x2c5d0d | 45 | But I have heard reports of Lady Honoka and\n |
| 0x2c5d3b | 42 | Lord Oshtor speaking in secret in recent\n |
| 0x2c5d66 | 6 | weeks. |
| 0x2c5d6d | 13 | Lord Oshtor!? |
| 0x2c5d7b | 45 | It is unlikely, but perhaps Lady Honoka and\n |
| 0x2c5da9 | 28 | Lord Oshtor conspired to a-- |
| 0x2c5dc6 | 46 | Hold your tongue. Speak not such accusations\n |
| 0x2c5df5 | 17 | without evidence. |
| 0x2c5e07 | 23 | M-My deepest apologies. |
| 0x2c5e1f | 19 | Yatanawarabe Ravieh |
| 0x2c5e33 | 35 | Lord Woshis. Please look at this... |
| 0x2c5e57 | 28 | And "this" is what, exactly? |
| 0x2c5e74 | 43 | W-With these findings in mind, I took the\n |
| 0x2c5ea0 | 46 | liberty of searching Lord Oshtor's chambers... |
| 0x2c5ecf | 44 | The Yatanawarabe holds up a small piece of\n |
| 0x2c5efc | 15 | folded paper... |
| 0x2c5f0c | 44 | Nestled within the fold, a small amount of\n |
| 0x2c5f39 | 33 | whitish powder catches the light. |
| 0x2c5f5b | 10 | This is... |
| 0x2c5f66 | 44 | I had an apothecary identify its contents,\n |
| 0x2c5f93 | 6 | and... |
| 0x2c5f9a | 36 | It is undeniably an ingested poison. |
| 0x2c5fbf | 17 | That would mean-- |
| 0x2c5fd1 | 46 | No... No, that's impossible. Lord Oshtor and\n |
| 0x2c6000 | 46 | Lady Honoka are more loyal to our liege than\n |
| 0x2c602f | 7 | anyone. |
| 0x2c6037 | 44 | Neither would think to participate in such\n |
| 0x2c6064 | 8 | folly... |
| 0x2c606d | 45 | I-It's possible that their "loyalty" was an\n |
| 0x2c609b | 38 | act, in order to secure an opportuni-- |
| 0x2c60c2 | 9 | Liveruni. |
| 0x2c60cc | 32 | B-But with this much evidence... |
| 0x2c60ed | 46 | I wish not to overstep my bounds, but... did\n |
| 0x2c611c | 47 | no one else think Lord Oshtor's rise to power\n |
| 0x2c614c | 11 | oddly fast? |
| 0x2c6158 | 47 | Perhaps some machination in the court allowed\n |
| 0x2c6188 | 8 | him to-- |
| 0x2c6191 | 49 | Now that you mention it, Lord Oshtor has spoken\n |
| 0x2c61c3 | 47 | out against the Mikado before. He opposed the\n |
| 0x2c61f3 | 4 | war! |
| 0x2c61f8 | 49 | Enough. I wish not to hear another word of this\n |
| 0x2c622a | 16 | from any of you. |
| 0x2c623b | 7 | Woshis. |
| 0x2c6243 | 4 | Ah!? |
| 0x2c6248 | 11 | Lord Vurai. |
| 0x2c6254 | 50 | Oshtor... and that harlot. I understand they are\n |
| 0x2c6287 | 35 | responsible for this transgression. |
| 0x2c62ab | 36 | Stay yourself, Lord Vurai! We need\n |
| 0x2c62d0 | 48 | incontrovertible evidence before we can safely-- |
| 0x2c6301 | 46 | There exists no better proof of their crimes\n |
| 0x2c6330 | 30 | than the very poison you hold. |
| 0x2c634f | 5 | Eek!? |
| 0x2c6355 | 34 | Please, Lord Vurai, calm yourself. |
| 0x2c6378 | 49 | This poison... This feels a little too perfect,\n |
| 0x2c63aa | 19 | wouldn't you agree? |
| 0x2c63be | 47 | There remains the possibility that someone is\n |
| 0x2c63ee | 48 | attempting to frame Lord Oshtor and Lady Honoka. |
| 0x2c641f | 20 | Don't make me laugh! |
| 0x2c6434 | 43 | Vurai suddenly seizes Woshis by the collar. |
| 0x2c6460 | 48 | Do you not realize this very passivity is what\n |
| 0x2c6491 | 18 | killed our liege!? |
| 0x2c64a4 | 5 | Gah-- |
| 0x2c64aa | 36 | P-Please, Lord Vurai! Calm yourself! |
| 0x2c64cf | 30 | You mustn't use violence here! |
| 0x2c64ee | 48 | Anju continues clinging to Oshtor desperately,\n |
| 0x2c651f | 46 | looking up at him with tearful, pleading eyes. |
| 0x2c654e | 36 | Oshtor... P-Please, do not leave me. |
| 0x2c6573 | 50 | I bid you... N-No, I wish you to stay by my side\n |
| 0x2c65a6 | 8 | forever. |
| 0x2c65af | 47 | Rest assured that I, Oshtor, will remain your\n |
| 0x2c65df | 32 | most loyal retainer forevermore. |
| 0x2c6600 | 40 | Y-You will? Truly? Promise me, Oshtor.\n |
| 0x2c6629 | 18 | Give me your word. |
| 0x2c663c | 24 | Of course. Upon my life. |
| 0x2c6655 | 34 | Lord Oshtor. Was it really you...? |
| 0x2c6678 | 31 | Oshtor will pay for his sins.\n |
| 0x2c6698 | 24 | He'll pay with his life. |
| 0x2c66b1 | 44 | Anju sits alone in her room, curled into a\n |
| 0x2c66de | 44 | tight ball on her bed, knees hugged to her\n |
| 0x2c670b | 6 | chest. |
| 0x2c6712 | 43 | With Munechika absent, the grief-stricken\n |
| 0x2c673e | 43 | princess' room has fallen into a state of\n |
| 0x2c676a | 13 | dishevelment. |
| 0x2c6778 | 45 | Though her eyes remain red and swollen, her\n |
| 0x2c67a6 | 46 | tears have long since dried, and she sits in\n |
| 0x2c67d5 | 8 | silence. |
| 0x2c67de | 30 | She has no more tears to give. |
| 0x2c67fd | 37 | Oshtor... Y-You are right, of course. |
| 0x2c6823 | 45 | I must follow in my father's footsteps, and\n |
| 0x2c6851 | 47 | rule over Yamato as he would have wanted me to. |
| 0x2c6881 | 46 | I can ill afford to lay here and cry like an\n |
| 0x2c68b0 | 18 | infant any longer. |
| 0x2c68c3 | 42 | Just as Anju moves to rise, a voice cuts\n |
| 0x2c68ee | 20 | through the silence. |
| 0x2c6903 | 29 | Your Highness? Are you awake? |
| 0x2c6921 | 15 | Hm? Yes, enter. |
| 0x2c6931 | 32 | Excuse me. I've brought you tea. |
| 0x2c6952 | 27 | Tea? I did not ask for tea. |
| 0x2c696e | 49 | Lord Oshtor instructed me to brew some for you.\n |
| 0x2c69a0 | 34 | He said it would soothe your mind. |
| 0x2c69c3 | 10 | Oshtor...? |
| 0x2c69ce | 47 | He hopes this tea might help lift your spirits. |
| 0x2c69fe | 36 | I-I see. Oshtor sent this, did he... |
| 0x2c6a23 | 44 | That's right. I am no longer alone. Oshtor\n |
| 0x2c6a50 | 26 | swore to stand by my side. |
| 0x2c6a6b | 47 | So long as he remains with me, I can surmount\n |
| 0x2c6a9b | 16 | any hardship...! |
| 0x2c6aac | 45 | Anju's cheeks flush with color as she speaks. |
| 0x2c6ada | 44 | I thank you. Please extend my gratitude to\n |
| 0x2c6b07 | 21 | Lord Oshtor, as well. |
| 0x2c6b1d | 18 | I will be sure to. |
| 0x2c6b30 | 30 | If you will excuse me, then... |
| 0x2c6b4f | 32 | An herbal tea from Oshtor, eh?\n |
| 0x2c6b70 | 27 | Let's have a taste, then... |
| 0x2c6b8c | 49 | Mm. Exquisite. To be expected, considering Lord\n |
| 0x2c6bbe | 16 | Oshtor's tastes. |
| 0x2c6bcf | 33 | Pray forgive me, Your Highness.\n |
| 0x2c6bf1 | 33 | May I have a moment of your time? |
| 0x2c6c13 | 21 | Ah, Oshtor! You came. |
| 0x2c6c29 | 42 | Anju's expression suddenly splits into a\n |
| 0x2c6c54 | 41 | contented grin at the appearance of her\n |
| 0x2c6c7e | 17 | beloved retainer. |
| 0x2c6c90 | 48 | You have my permission; enter! Really, Oshtor,\n |
| 0x2c6cc1 | 40 | you are far too concerned with protocol. |
| 0x2c6cea | 46 | I was told you required that I attend you at\n |
| 0x2c6d19 | 45 | once. How may I be of service, Your Highness? |
| 0x2c6d47 | 41 | Hm? I-I do not recall asking for you...\n |
| 0x2c6d71 | 35 | But no matter. Please, come closer. |
| 0x2c6d95 | 21 | ...You do not recall? |
| 0x2c6dab | 49 | As long as I have you here, I wanted to express\n |
| 0x2c6ddd | 31 | my thanks for the tea you sent. |
| 0x2c6dfd | 22 | Tea? What tea is this? |
| 0x2c6e14 | 35 | The herbal tea you sent me, Osh--\n |
| 0x2c6e38 | 28 | *cough*--the--*cough, cough* |
| 0x2c6e55 | 14 | Your Highness? |
| 0x2c6e64 | 40 | *cough, cough*--M-My throat, it--*cough* |
| 0x2c6e8d | 28 | Your Highness!? Speak to me! |
| 0x2c6eaa | 33 | S-So hot... my throat, burning... |
| 0x2c6ecc | 17 | I... I can't...\n |
| 0x2c6ede | 44 | My lungs, they can't... I can't breathe...\n |
| 0x2c6f0b | 9 | m-move... |
| 0x2c6f15 | 14 | Osh... tor...! |
| 0x2c6f24 | 14 | Your Highness! |
| 0x2c6f33 | 20 | I-I'm sca--*cough*\n |
| 0x2c6f48 | 9 | Ghhkk--!! |
| 0x2c6f52 | 46 | Your Highness! Someone! Anyone! The princess\n |
| 0x2c6f81 | 32 | needs an apothecary immediately! |
| 0x2c6fa2 | 27 | H-Hah, ha... hah... Hnngh-- |
| 0x2c6fbe | 29 | What could have possibly--Eh? |
| 0x2c6fdc | 45 | She was drinking... No. No, could this be--!? |
| 0x2c700a | 38 | Pardon my impertinence. What happened? |
| 0x2c7031 | 17 | Hah, hah, h-hah-- |
| 0x2c7043 | 18 | Wh--Your Highness! |
| 0x2c7056 | 18 | What is going on!? |
| 0x2c7069 | 10 | Excuse us! |
| 0x2c7074 | 4 | Wh-- |
| 0x2c7079 | 44 | Lord Oshtor. I must ask that you step away\n |
| 0x2c70a6 | 18 | from Her Highness. |
| 0x2c70b9 | 50 | I am sure you wish to defend yourself, but I ask\n |
| 0x2c70ec | 47 | that you make this easy for us both and comply. |
| 0x2c711c | 16 | ...I understand. |
| 0x2c712d | 39 | Oshtor quietly steps away from Anju's\n |
| 0x2c7155 | 47 | pain-wracked form, and Woshis takes his place\n |
| 0x2c7185 | 11 | beside her. |
| 0x2c7191 | 43 | Woshis takes Anju's pulse, then opens her\n |
| 0x2c71bd | 31 | eyelids, checking her pupils... |
| 0x2c71dd | 49 | Eventually, he lets out a relieved sigh, then--\n |
| 0x2c720f | 37 | expression still grim--waves to his\n |
| 0x2c7235 | 13 | Yatanawarabe. |
| 0x2c7243 | 47 | Please take Her Highness to the apothecary's.\n |
| 0x2c7273 | 8 | Quickly. |
| 0x2c727c | 10 | Y-Yes sir! |
| 0x2c7287 | 8 | At once! |
| 0x2c7290 | 40 | The Yatanawarabe carry Anju out of the\n |
| 0x2c72b9 | 28 | bedchamber, faces anxious... |
| 0x2c72d6 | 43 | ...and the guards that had been stationed\n |
| 0x2c7302 | 39 | outside the room step through the door. |
| 0x2c732a | 44 | The tension in the room hangs like a thick\n |
| 0x2c7357 | 41 | curtain, and the guards pause, uncertain. |
| 0x2c7381 | 47 | Please... Please take Lord Oshtor into custody. |
| 0x2c73b1 | 14 | Imperial Guard |
| 0x2c73c0 | 8 | What...? |
| 0x2c73c9 | 7 | B-But-- |
| 0x2c73d1 | 45 | The soldiers hesitate, and Woshis gives the\n |
| 0x2c73ff | 16 | order once more. |
| 0x2c7410 | 42 | As one of the Eight Pillars, I order the\n |
| 0x2c743b | 47 | immediate arrest of the Imperial Guard of the\n |
| 0x2c746b | 6 | Right. |
| 0x2c7472 | 45 | But... treat him respectfully as long as he\n |
| 0x2c74a0 | 22 | puts up no resistance. |
| 0x2c74b7 | 13 | U-Understood! |
| 0x2c74c5 | 47 | Still not quite grasping what's going on, the\n |
| 0x2c74f5 | 45 | soldiers step behind Oshtor and take him by\n |
| 0x2c7523 | 9 | the arms. |
| 0x2c752d | 41 | ...I have only one thing to ask of you.\n |
| 0x2c7557 | 23 | Will the princess live? |
| 0x2c756f | 48 | Being the Divine Scion, Her Highness' heritage\n |
| 0x2c75a0 | 47 | thankfully imparts unto her a high resistance\n |
| 0x2c75d0 | 18 | to natural toxins. |
| 0x2c75e3 | 44 | Though I cannot discern the nature of this\n |
| 0x2c7610 | 43 | poison, it does not appear to have been a\n |
| 0x2c763c | 12 | lethal dose. |
| 0x2c7649 | 8 | I see... |
| 0x2c7652 | 38 | Oshtor lets out a deep sigh of relief. |
| 0x2c7679 | 46 | However... I have little doubt that she'd be\n |
| 0x2c76a8 | 47 | long dead from the pain if not for her divine\n |
| 0x2c76d8 | 6 | blood. |
| 0x2c76df | 12 | Long dead... |
| 0x2c76ec | 33 | Please come with us, Lord Oshtor. |
| 0x2c770e | 42 | I apologize for putting you through this\n |
| 0x2c7739 | 8 | trouble. |
| 0x2c7742 | 15 | ...Lord Oshtor. |
| 0x2c7752 | 45 | As Oshtor turns his head, Woshis produces a\n |
| 0x2c7780 | 45 | medicine pouch from his pocket and shows it\n |
| 0x2c77ae | 7 | to him. |
| 0x2c77b6 | 11 | That is...? |
| 0x2c77c2 | 42 | Something we found amongst your personal\n |
| 0x2c77ed | 8 | effects. |
| 0x2c77f6 | 42 | Upon examination by an apothecary, it is\n |
| 0x2c7821 | 46 | undeniably the same poison that laid low our\n |
| 0x2c7850 | 6 | liege. |
| 0x2c7857 | 6 | What!? |
| 0x2c785e | 47 | I can only assume the same poison was used to\n |
| 0x2c788e | 38 | render Her Highness in such a state... |
| 0x2c78b5 | 41 | Have you anything to say in your defense? |
| 0x2c78df | 48 | I swear upon my oath to our liege that I would\n |
| 0x2c7910 | 22 | never do such a thing. |
| 0x2c7927 | 49 | ...But I suppose such excuses are useless to me\n |
| 0x2c7959 | 17 | now, aren't they? |
| 0x2c796b | 15 | I am afraid so. |
| 0x2c797b | 38 | You mustn't! This area is off-limits-- |
| 0x2c79a2 | 23 | Please, my lord, hold-- |
| 0x2c79ba | 18 | Get out of my way. |
| 0x2c79cd | 4 | Gah! |
| 0x2c79d2 | 48 | Before anyone in the room can react, a shocked\n |
| 0x2c7a03 | 46 | soldier topples into the room from the hall... |
| 0x2c7a32 | 45 | And from behind him, a looming figure enters. |
| 0x2c7a60 | 48 | He glares down at Oshtor, eyes ablaze with fury. |
| 0x2c7a91 | 8 | Vurai... |
| 0x2c7a9a | 6 | Gah... |
| 0x2c7aa1 | 11 | Lord Vurai! |
| 0x2c7aad | 7 | Oshtor. |
| 0x2c7ab5 | 44 | To think that the only man to ever make me\n |
| 0x2c7ae2 | 41 | taste defeat could sink so low as this... |
| 0x2c7b0c | 48 | Vurai clenches his teeth, no longer making any\n |
| 0x2c7b3d | 25 | effort to mask his anger. |
| 0x2c7b57 | 42 | I dirty my fist by deigning to strike you. |
| 0x2c7b82 | 43 | He spits out his words with disgust, then\n |
| 0x2c7bae | 15 | turns to leave. |
| 0x2c7bbe | 40 | Please take Lord Oshtor to the dungeons. |
| 0x2c7be7 | 9 | Yes, sir. |
| 0x2c7bf1 | 46 | The soldiers regain their grip on Oshtor and\n |
| 0x2c7c20 | 23 | begin to lead him away. |
| 0x2c7c38 | 47 | A trickle of blood dribbles down Oshtor's lip\n |
| 0x2c7c68 | 14 | to his chin... |
| 0x2c7c77 | 48 | As Oshtor leaves in the custody of the guards,\n |
| 0x2c7ca8 | 40 | Woshis remains, watching with a pained\n |
| 0x2c7cd1 | 11 | expression. |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_01.json` com a forma:
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
