# Cena ch_30_05 — pacote de traducao (242 linhas)

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
| Akuruka | Objeto | Akuruka | manter_original | moderate |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| Yamatan | Etnia | de Yamato | traduzir | none |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `building.` -> `edifício.` (Oshtor, 18_01)
- `quiet.` -> `calado.` (Haku, 18_01)
- `As you wish.` -> `Como desejar.` (Nekone, 14_04)
- `This way.` -> `Por aqui.` (Mulher, 14_06)
- `Well...` -> `Bom...` (Haku, 12_03)
- `Are you serious...?` -> `É sério mesmo...?` (Ukon, 17_04)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `Ngh...!` -> `Ngh...!` (Protagonist, 20_18)
- `Yamatan Soldier` -> `Soldado de Yamato` (SYSTEM, 12_10)
- `Vurai the Vanguard...` -> `Vurai o Vanguarda...` (Kuon, 18_01)
- `I see...` -> `Entendo...` (Haku, 11_02)
- `Know your place! ` -> `Conheça seu lugar!` (Oshtor, 20_14)
- `Vurai.` -> `Vurai.` (Woshis, 30_02)
- `Mikado!` -> `Mikado!` (Haku, 19_05)
- `like this?` -> `assim?` (Haku, 16_01)
- `Haku!?` -> `Haku!?` (Haku, 18_01)
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
| 0x2d990c | 20 | Kuon, where to next? |
| 0x2d9921 | 34 | Take a right on the next corner.\n |
| 0x2d9944 | 45 | From there, it's a straight shot to a water\n |
| 0x2d9972 | 8 | channel. |
| 0x2d997b | 38 | Got it. Rulutieh, careful not to fall. |
| 0x2d99a2 | 48 | Y-Yes... Thank you. Cocopo, please be careful... |
| 0x2d99e6 | 39 | We've been walking for quite a while.\n |
| 0x2d9a0e | 35 | Wonder what's above us right now... |
| 0x2d9a32 | 52 | You kinda lose track of directions when everything\n |
| 0x2d9a67 | 37 | keeps twisting and turning like this. |
| 0x2d9a8d | 43 | Wooow, look how huge that water channel is. |
| 0x2d9ab9 | 37 | Whoa, a river? That's a river, right? |
| 0x2d9adf | 46 | The water channel before us is about as wide\n |
| 0x2d9b0e | 19 | as the main street. |
| 0x2d9b22 | 45 | Multiple small waterways flow into it, like\n |
| 0x2d9b50 | 20 | angular tributaries. |
| 0x2d9b65 | 49 | Upstream is a slight slope, and there are large\n |
| 0x2d9b97 | 49 | bars that keep anyone from going further forward. |
| 0x2d9bc9 | 39 | One, two, three... Here. It's this one. |
| 0x2d9bf1 | 43 | Kuon grabs the bar and begins to rotate it. |
| 0x2d9c1d | 8 | There... |
| 0x2d9c26 | 48 | After a little while, the bar comes loose from\n |
| 0x2d9c57 | 21 | the floor, unscrewed. |
| 0x2d9c6d | 45 | With the bar loose, there's a gap just wide\n |
| 0x2d9c9b | 35 | enough for a person to get through. |
| 0x2d9cbf | 49 | If we climb this all the way up, it should lead\n |
| 0x2d9cf1 | 24 | onto the palace grounds. |
| 0x2d9d0e | 49 | We rip the map up into meaningless shreds, then\n |
| 0x2d9d40 | 34 | throw them into the water channel. |
| 0x2d9d63 | 8 | ...Well? |
| 0x2d9d6c | 33 | All clear. There's no one around. |
| 0x2d9d8e | 31 | Nice. Looks like we made it in. |
| 0x2d9dae | 31 | Hm... So where exactly is this? |
| 0x2d9dce | 42 | It looks to be the garden near the inner\n |
| 0x2d9df9 | 9 | building. |
| 0x2d9e11 | 46 | Shhh...! Cocopo, please... we need you to be\n |
| 0x2d9e40 | 6 | quiet. |
| 0x2d9e47 | 49 | Haku, I don't think we have much time. We might\n |
| 0x2d9e79 | 42 | only have moments until a patrol walks by. |
| 0x2d9ea4 | 45 | Uruuru, Saraana, we made it in just like we\n |
| 0x2d9ed2 | 39 | planned. Can you take care of the rest? |
| 0x2d9efa | 12 | As you wish. |
| 0x2d9f07 | 33 | Veiled from the eyes of heaven,\n |
| 0x2d9f29 | 34 | veiled from the eyes of the sun... |
| 0x2d9f4c | 40 | Bend natural law to our Master's will,\n |
| 0x2d9f75 | 18 | and open the path. |
| 0x2d9f88 | 10 | A mist...? |
| 0x2d9f93 | 29 | Whooaa. Look, it's all foggy! |
| 0x2d9fb1 | 47 | After Saraana and Uruuru close their eyes and\n |
| 0x2d9fe1 | 45 | chant, a white mist begins to form around us. |
| 0x2da00f | 17 | It's this mist... |
| 0x2da021 | 23 | Now they cannot see us. |
| 0x2da039 | 47 | We have shifted the planes. If we follow this\n |
| 0x2da069 | 41 | path, no one should be able to detect us. |
| 0x2da093 | 9 | This way. |
| 0x2da09d | 18 | Please, follow us. |
| 0x2da0b0 | 44 | Hey, Rulie, what exactly does all that mean? |
| 0x2da0dd | 49 | Um... well... I think we can... reach where Sir\n |
| 0x2da10f | 48 | Oshtor is without anyone finding us...? I think? |
| 0x2da140 | 48 | Oooh, you actually understood all that, Rulie?\n |
| 0x2da171 | 38 | But are you sure it'll be that simple? |
| 0x2da198 | 7 | Well... |
| 0x2da1a0 | 38 | Um... are you sure we'll be all right? |
| 0x2da1c7 | 50 | Hm... I don't think there's much to worry about.\n |
| 0x2da1fa | 44 | Those two should be able to take care of it. |
| 0x2da227 | 13 | You can tell? |
| 0x2da235 | 29 | Yes... I've got a good hunch. |
| 0x2da253 | 19 | Are you serious...? |
| 0x2da267 | 43 | Haku, did you know that they could do this? |
| 0x2da293 | 42 | Do this...? Oh, you mean the "path" thing? |
| 0x2da2be | 47 | Well, yeah. I've actually used it a number of\n |
| 0x2da2ee | 14 | times already. |
| 0x2da2fd | 13 | What's wrong? |
| 0x2da30b | 50 | No, it's nothing. Some things you're just better\n |
| 0x2da33e | 25 | off not knowing, I guess. |
| 0x2da358 | 43 | Huh? Wait, what's that supposed to mean...? |
| 0x2da384 | 20 | S-Somebody's coming. |
| 0x2da399 | 44 | We can see multiple shadows heading our way. |
| 0x2da3c6 | 10 | Worry not. |
| 0x2da3d1 | 48 | Please rest assured. They will not take notice\n |
| 0x2da402 | 18 | of anything we do. |
| 0x2da415 | 13 | Not anything? |
| 0x2da423 | 6 | Heeey! |
| 0x2da42a | 52 | Shinonon suddenly walks away from Kiwru, and heads\n |
| 0x2da45f | 47 | for the shadows while waving her hand cheerily. |
| 0x2da48f | 7 | Gah--!? |
| 0x2da497 | 10 | Shinonon!? |
| 0x2da4a2 | 7 | ...Huh? |
| 0x2da4aa | 7 | Soldier |
| 0x2da4b2 | 11 | ...What...? |
| 0x2da4be | 47 | But the patrol doesn't even seem to notice her. |
| 0x2da4ee | 51 | Actually, the soldiers' bodies just phase through\n |
| 0x2da522 | 35 | hers as they walk past obliviously. |
| 0x2da546 | 42 | Whooaa, so cool! Did you see that, Kiwru!? |
| 0x2da571 | 51 | Shinonon, fascinated, keeps pace with them as she\n |
| 0x2da5a5 | 46 | waggles her hand in and out of the soldiers'\n |
| 0x2da5d4 | 6 | shins. |
| 0x2da5db | 44 | *Sigh*... Please don't scare me like that... |
| 0x2da608 | 49 | Now that is quite an impressive sight. A fellow\n |
| 0x2da63a | 43 | cannot help but marvel at such a spectacle. |
| 0x2da666 | 44 | Didn't think it'd work THAT well. Holy shit. |
| 0x2da693 | 10 | A warning. |
| 0x2da69e | 46 | Please do not stray from our barrier. If you\n |
| 0x2da6cd | 44 | wander off, you may never return to reality. |
| 0x2da6fa | 50 | Sh-Shinonon! Come back! You can't go off on your\n |
| 0x2da72d | 14 | own like that. |
| 0x2da73c | 3 | Hm? |
| 0x2da740 | 46 | Aw, Kiwru. Do you need me to hold your hand?\n |
| 0x2da76f | 49 | I guess a woman's gotta make sure a man doesn't\n |
| 0x2da7a1 | 19 | feel scared, right? |
| 0x2da7b5 | 9 | *Sigh*... |
| 0x2da7bf | 7 | Ngh...! |
| 0x2da7c7 | 15 | Yamatan Soldier |
| 0x2da7d7 | 42 | Why don't you just admit to your crimes,\n |
| 0x2da802 | 12 | Lord Oshtor? |
| 0x2da80f | 41 | The evidence against you is undeniable.\n |
| 0x2da839 | 40 | Staying silent will not help your cause. |
| 0x2da862 | 7 | ...Ghh! |
| 0x2da86a | 52 | We serve a different general, but we all looked up\n |
| 0x2da89f | 49 | to you. Please--do not disgrace yourself further. |
| 0x2da8d1 | 52 | ...I'm afraid this must continue, then. As long as\n |
| 0x2da906 | 48 | you keep silent, you will be whipped and lashed. |
| 0x2da937 | 47 | If you will not tell us where Lady Honoka has\n |
| 0x2da967 | 33 | hidden herself, we will make you. |
| 0x2da989 | 23 | I suggest you prepare-- |
| 0x2da9a1 | 7 | Gah...! |
| 0x2da9a9 | 50 | The first thing we hear upon entering the prison\n |
| 0x2da9dc | 37 | is the sound of a whip hitting flesh. |
| 0x2daa02 | 40 | A rasping wheeze of pain soon follows.\n |
| 0x2daa2b | 44 | The scent of blood hangs heavy in the air... |
| 0x2daa58 | 54 | We've arrived in the middle of Oshtor's interrogation. |
| 0x2daa8f | 14 | Dear brother!! |
| 0x2daa9e | 48 | Once we exit the "path," Nekone shouts out and\n |
| 0x2daacf | 51 | starts towards Oshtor. I quickly grab hold of her\n |
| 0x2dab03 | 30 | before she can blow our cover. |
| 0x2dab22 | 7 | Hmngh!? |
| 0x2dab2a | 44 | Don't be an idiot! If we make a scene now,\n |
| 0x2dab57 | 25 | they're going to find us! |
| 0x2dab71 | 12 | Mngh! Mmmf!! |
| 0x2dab7e | 37 | Shh! Someone's coming from behind us! |
| 0x2daba4 | 47 | I lift Nekone and quickly hide behind a pillar. |
| 0x2dabd4 | 21 | Vurai the Vanguard... |
| 0x2dabea | 46 | Has he revealed the location of the vixen yet? |
| 0x2dac19 | 42 | N-No, sir... Not yet. I am terribly sorry. |
| 0x2dac44 | 39 | No matter how much pain we cause him,\n |
| 0x2dac6c | 22 | he refuses to speak... |
| 0x2dac83 | 48 | I suppose we should have expected such resolve\n |
| 0x2dacb4 | 17 | of Lord Oshtor... |
| 0x2dacc6 | 43 | The two soldiers immediately fall silent,\n |
| 0x2dacf2 | 49 | shuddering as Vurai glares at them--eyes blazing. |
| 0x2dad24 | 36 | I-I... I meant nothing by that, sir. |
| 0x2dad49 | 47 | Vurai coldly stares down at the bound Oshtor,\n |
| 0x2dad79 | 18 | chained and bowed. |
| 0x2dad8c | 50 | ...The man I once considered my equal has fallen\n |
| 0x2dadbf | 11 | far indeed. |
| 0x2dadcb | 14 | Ghh...Vurai... |
| 0x2dadda | 41 | What is it...? Begging for your life now? |
| 0x2dae04 | 33 | Her Highness... Is she safe...?\n |
| 0x2dae26 | 28 | What is her... condition...? |
| 0x2dae43 | 49 | You... You still spout these absurd pretenses!?\n |
| 0x2dae75 | 49 | She is safe because YOU have been locked in here! |
| 0x2daea7 | 8 | I see... |
| 0x2daeb0 | 43 | How long do you intend on continuing this\n |
| 0x2daedc | 17 | pathetic display? |
| 0x2daeee | 49 | Why did you not use the power of the Akuruka to\n |
| 0x2daf20 | 49 | evade capture? A man of your ability could have\n |
| 0x2daf52 | 15 | escaped easily. |
| 0x2daf62 | 16 | ...It is simple. |
| 0x2daf73 | 32 | I have no reason to run or hide. |
| 0x2daf94 | 46 | Still you persist in this facade of loyalty?\n |
| 0x2dafc3 | 44 | Do you intend for your death to prove your\n |
| 0x2daff0 | 10 | innocence? |
| 0x2daffb | 49 | Words are not necessary. My life belongs to the\n |
| 0x2db02d | 49 | imperial house... I remain loyal to Her Highness. |
| 0x2db05f | 52 | Laughable. And what do you believe can come of that? |
| 0x2db094 | 48 | Be you guilty or innocent, I have no reason to\n |
| 0x2db0c5 | 43 | pledge my loyalty to a girl as weak as she! |
| 0x2db0f1 | 32 | Vurai... have you gone mad...?\n |
| 0x2db112 | 48 | Such a statement is treachery to the throne...\n |
| 0x2db143 | 16 | Know your place! |
| 0x2db154 | 44 | Silence! Our glorious liege has passed on.\n |
| 0x2db181 | 47 | The powerless have no right to speak of lofty\n |
| 0x2db1b1 | 7 | ideals. |
| 0x2db1b9 | 38 | I have finally realized this. Yes...\n |
| 0x2db1e0 | 47 | Yamato can only be governed by one who wields\n |
| 0x2db210 | 11 | true power! |
| 0x2db21c | 53 | And so you would put yourself forth for the task...\n |
| 0x2db252 | 6 | Vurai. |
| 0x2db259 | 50 | No! The heavens alone decide who reigns supreme!\n |
| 0x2db28c | 47 | But a girl of such weakness will never be the\n |
| 0x2db2bc | 7 | Mikado! |
| 0x2db2c4 | 52 | Oshtor, you shall understand that the truly strong\n |
| 0x2db2f9 | 24 | are the truly righteous! |
| 0x2db312 | 45 | With our liege gone, we must prove Yamato's\n |
| 0x2db340 | 49 | unwavering might! One so weak can never inherit\n |
| 0x2db372 | 11 | the throne! |
| 0x2db37e | 43 | Vurai... why? Why has a man like yourself-- |
| 0x2db3aa | 45 | Has our liege's death... twisted you so...?\n |
| 0x2db3d8 | 43 | Has such grief truly driven you to madness? |
| 0x2db404 | 31 | Call me a madman if you wish.\n |
| 0x2db424 | 41 | Your words have only rid me of all doubt. |
| 0x2db44e | 37 | My only course is to continue onward! |
| 0x2db474 | 28 | What... do you intend to do? |
| 0x2db491 | 46 | It matters not to you. You shall rot in this\n |
| 0x2db4c0 | 49 | prison. Without your Akuruka, you have no escape. |
| 0x2db4f2 | 47 | Do not think that you will ever see the sun's\n |
| 0x2db522 | 12 | light again. |
| 0x2db52f | 39 | Stop... Vurai! Are you--You dare to--\n |
| 0x2db557 | 22 | Her Highness--Nghh...! |
| 0x2db56e | 31 | Gah...! Hahh... hahh... hahh... |
| 0x2db58e | 49 | The moment Vurai's footsteps pass, a collective\n |
| 0x2db5c0 | 32 | exhale escapes the entire group. |
| 0x2db5e1 | 40 | Holy shit... that guy's scary as hell... |
| 0x2db60a | 29 | Damn... That guy's a monster! |
| 0x2db628 | 47 | Even just viewing him from afar makes my hair\n |
| 0x2db658 | 15 | stand on end... |
| 0x2db668 | 42 | Ahaha, you can let go of me now, Kuon...\n |
| 0x2db693 | 16 | I'll behave now. |
| 0x2db6a4 | 48 | I'd rather not have to go head-to-head against\n |
| 0x2db6d5 | 18 | a guy like that... |
| 0x2db6e8 | 46 | How long do you intend on keeping hold of me\n |
| 0x2db717 | 10 | like this? |
| 0x2db722 | 39 | Right, I forgot I was holding her back. |
| 0x2db74a | 10 | Oh, sorry. |
| 0x2db755 | 43 | Forgot it was a person I was holding onto\n |
| 0x2db781 | 27 | and not just some pillar... |
| 0x2db79d | 9 | ...Rrrgh! |
| 0x2db7a7 | 7 | GYAGH!? |
| 0x2db7af | 6 | Haku!? |
| 0x2db7b6 | 35 | You need to keep your voice down... |
| 0x2db7da | 13 | Dear brother! |
| 0x2db7e8 | 8 | Nekone!? |
| 0x2db7f1 | 45 | Nekone jumps out from behind the pillar and\n |
| 0x2db81f | 21 | dashes toward Oshtor. |
| 0x2db83a | 5 | Shit! |
| 0x2db840 | 45 | What the--!? What was that simpering little\n |
| 0x2db86e | 7 | voice!? |
| 0x2db876 | 38 | How did--Where did you all come from!? |
| 0x2db89d | 34 | Uh-oh, looks like they found us... |
| 0x2db8c0 | 13 | That idiot... |
| 0x2db8ce | 49 | We gotta move, boss! The little lady's in danger! |
| 0x2db900 | 28 | Dammit! Everyone, positions! |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_05.json` com a forma:
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
