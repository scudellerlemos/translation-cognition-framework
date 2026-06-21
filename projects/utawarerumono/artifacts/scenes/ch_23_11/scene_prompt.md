# Cena ch_23_11 — pacote de traducao (1087 linhas)

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
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Earth | Local | Terra | traduzir | major |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Neko | Personagem | Neko | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Amazing...` -> `Incrível...` (Haku, 12_04)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `Lord Haku.` -> `Senhor Haku.` (Oshtor, 23_01)
- `favor.` -> `favora.` (Atuy, 16_02)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `us.` -> `nós.` (Haku, 15_03)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Come in.` -> `Entre.` (Oshtor, 16_02)
- `place.` -> `lugar.` (Protagonista, 16_01)
- `have.` -> `tenho.` (Haku, 19_08)
- `indeed.` -> `com efeito.` (Oshtor, 22_07)
- `However--` -> `Porém--` (Narrator, 20_20)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `right now.` -> `agora.` (Kuon, 22_05)
- `Nyargh!?` -> `Nhargh!?` (Haku, 23_03)
- `forward.` -> `adiante.` (Oshtor, 19_01)
- `Here.` -> `Aqui.` (Kuon, 11_01)
- `Alone?` -> `Sozinho?` (Kuon, 11_02)
- `Be silent.` -> `Fique quieto.` (Oshtor/Ukon, 20_01)
- `speaks.` -> `fala.` (Haku, 19_07)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `after all.` -> `afinal.` (Haku, 11_07)
- `Munechika.` -> `Munechika.` (Narração, 23_02)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `EEP!?` -> `EEEK!?` (Atuy, 16_01)
- `Urk...` -> `Argh...` (Haku, 12_06)
- `...Understood.` -> `...Entendido.` (Haku, 23_01)
- `option.` -> `opção.` (Rulutieh, 19_05)
- `office.` -> `escritório.` (Haku, 17_03)
- `from.` -> `de.` (Atuy, 16_02)
- `sounds.` -> `incomum.` (Haku, 12_03)
- `know.` -> `sei.` (Haku, 19_02)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `possible.` -> `possível.` (Rulutieh, 18_01)
- `this.` -> `essa.` (Moznu, 13_05)
- `thought.` -> `pensamento.` (Haku, 22_08)
- `us...` -> `aproxima...` (Haku, 13_05)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `This?` -> `Esta?` (Haku, 11_09)
- `area.` -> `área.` (Haku/Narrador, 19_08)
- `I see.` -> `Sim.` (Haku, 11_02)
- `ground.` -> `do chão.` (Man, 11_01)
- `Nosuri?` -> `Nosuri?` (Nosuri, 18_01)
- `it.` -> `aí.` (Haku, 15_03)
- `Haku...?` -> `Haku...?` (Kuon, 11_02)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `Nekone?` -> `Nekone?` (Haku, 15_07)
- `while.` -> `agora.` (Kuon, 15_02)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `y'know.` -> `sabia.` (Ukon, 12_07)
- `Haku...` -> `Haku...` (Kuon, 11_02)
- `Are you OK?` -> `Está bem?` (Kuon, 13_09)
- `time.` -> `vez.` (Raurau, 18_01)
- `day.` -> `dia.` (SYSTEM, 20_18)
- `you.` -> `isso.` (Nekone, 15_03)
- `actually.` -> `na verdade.` (Kuon, 11_10)
- `Uh?` -> `Hã?` (Nekone, 16_02)
- `all this.` -> `disso tudo.` (Haku, 17_01)
- `least.` -> `enfim.` (Ukon, 12_12)
- `it...` -> `isso...` (Haku, 18_01)
- `can.` -> `consigo.` (Haku, 19_08)
- `done.` -> `feito.` (Haku, 17_04)
- `something?` -> `alguma coisa?` (Haku, 16_01)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `yeah?` -> `tá?` (Ukon, 14_02)
- `tightly.` -> `apertado.` (Haku, 18_01)
- `Is this...?` -> `É isto...?` (Haku, 20_21)
- `mouth.` -> `boca.` (Garota, 16_01)
- `soldiers?` -> `soldados?` (Haku, 22_03)
- `attention.` -> `muita atenção.` (Ukon, 15_01)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `...Haku.` -> `...Haku.` (Haku, 22_05)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `Please...` -> `Vai lá...` (Nosuri, 20_07)
- `noon.` -> `meio-dia.` (Haku, 22_05)
- `Yeah...` -> `É...` (Kuon, 11_02)
- `Heh.` -> `Heh.` (Haku, 14_02)
- `G-Got it!` -> `E-Entendi!` (Haku, 23_10)
- `Wow...` -> `Nossa...` (Kuon, 14_03)
- `Do you think this will be enough?` -> `Você acha que isso vai dar?` (Garota, 23_06)
- `anything.` -> `nada.` (Haku, 17_01)
- `Master.` -> `Mestre.` (Homem, 12_14)
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
| 0x29b760 | 7 | Eep...! |
| 0x29b768 | 10 | Amazing... |
| 0x29b773 | 46 | Hee hee. Makes my ears tickle, all this noise. |
| 0x29b7a2 | 40 | I wasn't expecting the hero's welcome... |
| 0x29b7cb | 42 | I'm not very good with these situations.\n |
| 0x29b7f6 | 29 | It's a little embarrassing... |
| 0x29b814 | 44 | Their supply lines and communications were\n |
| 0x29b841 | 46 | totally cut off. They were desperate for this. |
| 0x29b870 | 38 | Guess that makes us big damn heroes.\n |
| 0x29b897 | 34 | Not really my thing, to be honest. |
| 0x29b8ba | 48 | Still, a welcome like this makes that grueling\n |
| 0x29b8eb | 33 | trip over the ocean all worth it. |
| 0x29b90d | 45 | Haku. I'll accompany Miss Nekone and see to\n |
| 0x29b93b | 20 | necessary protocols. |
| 0x29b950 | 7 | Thanks. |
| 0x29b958 | 45 | Kiwru, let's go get all this stuff unpacked\n |
| 0x29b986 | 15 | from the carts. |
| 0x29b996 | 10 | Oh, right! |
| 0x29b9a1 | 45 | Guess I'll stay here and keep an eye on the\n |
| 0x29b9cf | 14 | supplies then. |
| 0x29b9de | 47 | I can't feel the usual vigor from the Yamatan\n |
| 0x29ba0e | 48 | soldiers. Morale must be rock-bottom, going by\n |
| 0x29ba3f | 9 | the mood. |
| 0x29ba49 | 10 | Lord Haku. |
| 0x29ba54 | 50 | I look up toward the source of the voice calling\n |
| 0x29ba87 | 8 | my name. |
| 0x29ba90 | 14 | Ah, Munechika. |
| 0x29ba9f | 48 | On behalf of everyone here, I'd like to extend\n |
| 0x29bad0 | 47 | formal thanks to you. You arrived just in time. |
| 0x29bb00 | 50 | Don't worry about it. I'm just here in Tuskur to\n |
| 0x29bb33 | 44 | try its cuisine. The delivery is a side gig. |
| 0x29bb60 | 50 | Hmhm... It's reassuring to hear your nonchalance\n |
| 0x29bb93 | 17 | again, Lord Haku. |
| 0x29bba5 | 49 | Hm. I didn't notice it before, but Munechika...\n |
| 0x29bbd7 | 47 | seems pretty worn down, even if she is smiling. |
| 0x29bc07 | 44 | I doubt she'll say as much openly, but the\n |
| 0x29bc34 | 37 | battles up until now must have been\n |
| 0x29bc5a | 12 | hard-fought. |
| 0x29bc67 | 47 | You've nothing to worry yourself over. Thanks\n |
| 0x29bc97 | 48 | to these provisions, the tide will turn in our\n |
| 0x29bcc8 | 6 | favor. |
| 0x29bccf | 48 | ...I guess I was letting my expressions betray\n |
| 0x29bd00 | 12 | my thoughts. |
| 0x29bd0d | 45 | Oh, right. This is for you. Probably should\n |
| 0x29bd3b | 42 | have led with it, but it's a letter from\n |
| 0x29bd66 | 7 | Oshtor. |
| 0x29bd6e | 50 | I see. It seems my debts to Lord Oshtor continue\n |
| 0x29bda1 | 16 | to accumulate... |
| 0x29bdb2 | 29 | I doubt he sees it like that. |
| 0x29bdd0 | 48 | You're likely right, but even so, I won't soon\n |
| 0x29be01 | 34 | forget all the help he's given me. |
| 0x29be24 | 37 | That goes for you as well, Lord Haku. |
| 0x29be4a | 50 | Such a sense of obligation... But I guess that's\n |
| 0x29be7d | 22 | just how Munechika is. |
| 0x29be94 | 46 | Now, this letter transfers you to my command\n |
| 0x29bec3 | 40 | as long as you're here. Is that correct? |
| 0x29beec | 9 | Hm? Yeah. |
| 0x29bef6 | 45 | Then I bid you follow me. I wish for you to\n |
| 0x29bf24 | 23 | accompany me somewhere. |
| 0x29bf3c | 47 | Munechika leads me to a tent much larger than\n |
| 0x29bf6c | 34 | any of the others in the vicinity. |
| 0x29bf8f | 47 | Along the way, she explains the current state\n |
| 0x29bfbf | 11 | of the war. |
| 0x29bfcb | 44 | You've doubtlessly noticed that conditions\n |
| 0x29bff8 | 25 | are not favorable for us. |
| 0x29c012 | 47 | We've established a foothold in the area, but\n |
| 0x29c042 | 45 | thus far, we've been unable to progress any\n |
| 0x29c070 | 8 | further. |
| 0x29c079 | 45 | We've yet to meet them in a full-on battle,\n |
| 0x29c0a7 | 46 | but skirmishes arise at all times of the day\n |
| 0x29c0d6 | 9 | or night. |
| 0x29c0e0 | 41 | They appear as if from nowhere, raise a\n |
| 0x29c10a | 43 | commotion, then vanish beyond the treeline. |
| 0x29c136 | 47 | Any hunting parties we send out are unable to\n |
| 0x29c166 | 16 | track them down. |
| 0x29c177 | 43 | Many a squad has chased them too far out,\n |
| 0x29c1a3 | 25 | only to fall into a trap. |
| 0x29c1bd | 49 | And so our numbers continue to slowly diminish,\n |
| 0x29c1ef | 45 | while Tuskur's assaults persist relentlessly. |
| 0x29c21d | 45 | Fatigue is the single largest threat to our\n |
| 0x29c24b | 39 | campaign, now. The troops are wearing\n |
| 0x29c273 | 15 | themselves out. |
| 0x29c283 | 50 | Guess the home-turf advantage is a bigger factor\n |
| 0x29c2b6 | 15 | than I thought. |
| 0x29c2c6 | 47 | It's likely their knowledge of local, smaller\n |
| 0x29c2f6 | 46 | paths is enabling their guerilla tactics, yes. |
| 0x29c325 | 44 | Doubtlessly, they use those paths to stage\n |
| 0x29c352 | 45 | strikes on our supply lines, as well. We're\n |
| 0x29c380 | 8 | cut off. |
| 0x29c389 | 47 | I see. So it's possible they meant for you to\n |
| 0x29c3b9 | 45 | camp here all along? The area they know best? |
| 0x29c3e7 | 49 | Quite. The Tuskur general is well-versed in the\n |
| 0x29c419 | 12 | arts of war. |
| 0x29c426 | 50 | I've heard tell that Tuskur fought a large-scale\n |
| 0x29c459 | 47 | civil war some years ago... Perhaps that's why. |
| 0x29c489 | 48 | I remember my brother saying something to that\n |
| 0x29c4ba | 9 | effect... |
| 0x29c4c4 | 47 | How he tried to negotiate a way to study this\n |
| 0x29c4f4 | 48 | land with the kamunagi, and how they denied him. |
| 0x29c525 | 50 | Maybe they've been anticipating Yamato resorting\n |
| 0x29c558 | 48 | to force all this time. They've been ready for\n |
| 0x29c589 | 3 | us. |
| 0x29c58d | 3 | Hm? |
| 0x29c591 | 42 | Munechika's beckoning pulls me out of my\n |
| 0x29c5bc | 43 | thoughts as we arrive in front of the tent. |
| 0x29c5e8 | 45 | This is our forward command center. Please,\n |
| 0x29c616 | 8 | come in. |
| 0x29c61f | 24 | You are LATE, Munechika! |
| 0x29c638 | 45 | Apologies. I was seeing to the resupply and\n |
| 0x29c666 | 21 | reinforcement effort. |
| 0x29c67c | 50 | Oh? Then you must be part of the reinforcements.\n |
| 0x29c6af | 46 | Your name was... Haku? Forgive me, it's been\n |
| 0x29c6de | 8 | a while. |
| 0x29c6e7 | 49 | Yes. Lord Haku will be under my command for the\n |
| 0x29c719 | 46 | duration, so it is my wish that he joins our\n |
| 0x29c748 | 8 | meeting. |
| 0x29c751 | 43 | ...I have no qualms. He may do as he likes. |
| 0x29c77d | 6 | Pffeh. |
| 0x29c784 | 45 | Raiko looks me over, and the corners of his\n |
| 0x29c7b2 | 30 | mouth turn up in a small grin. |
| 0x29c7d1 | 43 | Dekopompo, on the other hand, shoots me a\n |
| 0x29c7fd | 45 | dubious glance as I follow Munechika to her\n |
| 0x29c82b | 6 | place. |
| 0x29c832 | 49 | I THOUGHT you looked familiar. Oshtor's lackey,\n |
| 0x29c864 | 45 | hm? You certainly ran your mouth at the war\n |
| 0x29c892 | 8 | council. |
| 0x29c89b | 44 | In my magnanimousness, I will forgive your\n |
| 0x29c8c8 | 46 | impertinence ONCE. I expect you to hold your\n |
| 0x29c8f7 | 7 | tongue. |
| 0x29c8ff | 42 | Man, he REALLY doesn't like me, does he?\n |
| 0x29c92a | 48 | I guess it's because I'm more a mercenary than\n |
| 0x29c95b | 12 | a soldier... |
| 0x29c968 | 46 | Let's begin, if that's everything. Time is a\n |
| 0x29c997 | 46 | valuable resource. We oughtn't waste what we\n |
| 0x29c9c6 | 5 | have. |
| 0x29c9cc | 7 | Indeed. |
| 0x29c9d4 | 43 | Dekopompo and the others seat themselves,\n |
| 0x29ca00 | 43 | followed by Munechika. When I try to sit,\n |
| 0x29ca2c | 9 | however-- |
| 0x29ca36 | 47 | Eh? O, joyous day! Master Haku! Look upon me,\n |
| 0x29ca66 | 44 | Master Haku, and see a visage wracked with\n |
| 0x29ca93 | 10 | rejoicing! |
| 0x29ca9e | 7 | Huh...? |
| 0x29caa6 | 34 | I'd recognize that voice anywhere. |
| 0x29cac9 | 22 | Maro? How've you been? |
| 0x29cae0 | 48 | Ho ho! Behold me, as fighting-fit as thou dost\n |
| 0x29cb11 | 47 | remember! Maroro remaineth a PARAGON of health. |
| 0x29cb41 | 47 | O, but how our reunion gladdens me! Forsooth,\n |
| 0x29cb71 | 46 | thy presence is worth a hundred men and more-- |
| 0x29cba4 | 45 | Dekopompo levels a glare at him, and Maroro\n |
| 0x29cbd2 | 46 | freezes, sinking silently back into his chair. |
| 0x29cc01 | 47 | Oh, right. I totally forgot he was working as\n |
| 0x29cc31 | 22 | Dekopompo's tactician. |
| 0x29cc48 | 45 | Seems like he's having a rough go of it, as\n |
| 0x29cc76 | 47 | usual. Not sure if I can say anything to help\n |
| 0x29cca6 | 10 | right now. |
| 0x29ccb1 | 35 | Bah, wasting our precious time...\n |
| 0x29ccd5 | 18 | Bokoinante! Begin. |
| 0x29cce8 | 16 | As you say, sir. |
| 0x29ccf9 | 47 | The man called Bokoinante spreads a large map\n |
| 0x29cd29 | 48 | across the table, then points out a particular\n |
| 0x29cd5a | 9 | location. |
| 0x29cd64 | 47 | Scout reports indicate an enemy stronghold in\n |
| 0x29cd94 | 30 | this mountainous region, here. |
| 0x29cdb3 | 43 | We can reasonably assume the enemy troops\n |
| 0x29cddf | 43 | waylaying our forces are deploying from it. |
| 0x29ce0b | 45 | One side is a sheer cliff, and the approach\n |
| 0x29ce39 | 41 | is... made troublesome by the extremely\n |
| 0x29ce63 | 18 | difficult terrain. |
| 0x29ce76 | 45 | The assembled generals and their tacticians\n |
| 0x29cea4 | 41 | lapse into silence at Bokoinante's grim\n |
| 0x29cece | 12 | description. |
| 0x29cedb | 46 | He used the word "troublesome" to glaze over\n |
| 0x29cf0a | 37 | the challenge, but it seems all but\n |
| 0x29cf30 | 15 | insurmountable. |
| 0x29cf40 | 47 | Not to mention the enemy's prior knowledge of\n |
| 0x29cf70 | 51 | the territory, the terrible terrain disadvantage... |
| 0x29cfa4 | 45 | We can't rely on our numbers in such narrow\n |
| 0x29cfd2 | 47 | spaces, but deploying with fewer troops won't\n |
| 0x29d002 | 13 | help, either. |
| 0x29d010 | 46 | Which means the optimal strategy is probably-- |
| 0x29d03f | 48 | Bah! This backwater country has only been able\n |
| 0x29d070 | 46 | to resist us thus far through sheer dumb luck! |
| 0x29d09f | 51 | This feeble "stronghold" will fall in but moments\n |
| 0x29d0d3 | 45 | if we rally our full, combined strength, yes? |
| 0x29d101 | 44 | Dekopompo suddenly bursts out in enthusiasm. |
| 0x29d12e | 48 | Look at our enemy! They avoid a head-on fight,\n |
| 0x29d15f | 43 | continuing to nip at our heels with these\n |
| 0x29d18b | 11 | skirmishes! |
| 0x29d197 | 46 | They fear our military might! They are weak,\n |
| 0x29d1c6 | 24 | pathetic in the extreme! |
| 0x29d1df | 47 | We should rally for a proper, frontal assault\n |
| 0x29d20f | 7 | on th-- |
| 0x29d217 | 44 | No. As one who prides herself on defensive\n |
| 0x29d244 | 20 | tactics, I disagree. |
| 0x29d259 | 47 | I propose we abandon this location and make a\n |
| 0x29d289 | 17 | tactical retreat. |
| 0x29d29b | 8 | Nyargh!? |
| 0x29d2a4 | 44 | Dekopompo, shocked, ceases his flailing at\n |
| 0x29d2d1 | 48 | Munechika's words. She continues, ignoring his\n |
| 0x29d302 | 9 | reaction. |
| 0x29d30c | 48 | Holding our current position will only see our\n |
| 0x29d33d | 46 | numbers continue to diminish. We cannot push\n |
| 0x29d36c | 8 | forward. |
| 0x29d375 | 50 | I submit that our priority should be to retreat,\n |
| 0x29d3a8 | 45 | regroup, and reorganize our available troops. |
| 0x29d3d6 | 15 | Wha--Wh--Wh--!? |
| 0x29d3e6 | 15 | Absolutely not! |
| 0x29d3f6 | 50 | We are here under DIRECT orders from the Mikado!\n |
| 0x29d429 | 28 | Have you already forgotten!? |
| 0x29d446 | 47 | You expect us to stand before the enemy, then\n |
| 0x29d476 | 47 | turn tail and run!? To accept such naked SHAME? |
| 0x29d4a6 | 43 | Tuskur is primarily composed of woods and\n |
| 0x29d4d2 | 46 | mountains, with little in the way of flatland. |
| 0x29d501 | 47 | That is why they equip themselves lightly and\n |
| 0x29d531 | 41 | favor guerilla tactics over traditional\n |
| 0x29d55b | 17 | rakusharai style. |
| 0x29d56d | 47 | Our army is composed of rakusharai accustomed\n |
| 0x29d59d | 45 | to fighting on plains. We have no advantage\n |
| 0x29d5cb | 5 | here. |
| 0x29d5d1 | 47 | Positioned as we are, we cannot fight at even\n |
| 0x29d601 | 33 | a fraction of our full potential. |
| 0x29d623 | 48 | Their fundamental tactics differ too much from\n |
| 0x29d654 | 41 | ours. I bid you remember how much we've\n |
| 0x29d67e | 10 | struggled. |
| 0x29d689 | 48 | They target our weaknesses. They understand we\n |
| 0x29d6ba | 43 | cannot hold out forever. Our supplies are\n |
| 0x29d6e6 | 8 | limited. |
| 0x29d6ef | 49 | Knowing that, would you still force a fight and\n |
| 0x29d721 | 46 | sacrifice the lives of our soldiers for pride? |
| 0x29d750 | 46 | Are you saying we're STRUGGLING against such\n |
| 0x29d77f | 16 | a tiny country!? |
| 0x29d790 | 49 | We have come here to SUBJUGATE these degenerate\n |
| 0x29d7c2 | 36 | primitives, as is the Mikado's will. |
| 0x29d7e7 | 44 | We can hardly afford to shame ourselves in\n |
| 0x29d814 | 28 | front of our enemy and flee! |
| 0x29d831 | 41 | I am not saying we should run outright.\n |
| 0x29d85b | 49 | I merely propose we find a more easily-supplied\n |
| 0x29d88d | 46 | Th-That statement itself REEKS of cowardice!\n |
| 0x29d8bc | 30 | Where is your fighting spirit? |
| 0x29d8db | 45 | Or do you intend to controvert the Mikado's\n |
| 0x29d909 | 6 | will!? |
| 0x29d910 | 46 | Munechika, who'd maintained a conversational\n |
| 0x29d93f | 42 | tone up to this point, abruptly stands up. |
| 0x29d96a | 47 | I cannot abide such slander. You will retract\n |
| 0x29d99a | 17 | those words, sir. |
| 0x29d9ac | 43 | Nyoh? Have I hit a sore spot? To be sure,\n |
| 0x29d9d8 | 44 | I'm astounded so disloyal a woman was made\n |
| 0x29da05 | 33 | one of the Eight Pillar Generals! |
| 0x29da27 | 28 | Dekopompo... Watch yourself. |
| 0x29da44 | 47 | Wh--!? The gall! You would address me by name\n |
| 0x29da74 | 6 | alone? |
| 0x29da7b | 47 | General you may be, but a baseborn RAT hardly\n |
| 0x29daab | 44 | compares to one such as me! You've allowed\n |
| 0x29dad8 | 13 | your ego to-- |
| 0x29dae6 | 10 | Be silent. |
| 0x29daf1 | 18 | Nyeh! You dare...? |
| 0x29db04 | 49 | Munechika glares at Dekopompo, her eyes full of\n |
| 0x29db36 | 46 | cold fire, while he glares back in a furious\n |
| 0x29db65 | 6 | sweat. |
| 0x29db6c | 48 | This isn't good. Munechika's hard to rile, but\n |
| 0x29db9d | 48 | I can tell invoking the Mikado filled her with\n |
| 0x29dbce | 5 | rage. |
| 0x29dbd4 | 49 | The tension continues to escalate, right to the\n |
| 0x29dc06 | 50 | edge of swords being drawn--but then a low voice\n |
| 0x29dc39 | 7 | speaks. |
| 0x29dc41 | 42 | Please, generals. We need you to compose\n |
| 0x29dc6c | 11 | yourselves. |
| 0x29dc78 | 5 | Ah... |
| 0x29dc7e | 46 | Y-You DARE give ME commands!? You are naught\n |
| 0x29dcad | 19 | but Raiko's flunky! |
| 0x29dcc1 | 41 | I apologize. I mean not to offend, Lord\n |
| 0x29dceb | 45 | Dekopompo, but such words are unbefitting a\n |
| 0x29dd19 | 20 | man of your station. |
| 0x29dd2e | 49 | I would very much like to see you return to the\n |
| 0x29dd60 | 47 | kind, understanding Lord Dekopompo I know you\n |
| 0x29dd90 | 6 | to be. |
| 0x29dd97 | 48 | Your brave, courageous demeanor never fails to\n |
| 0x29ddc8 | 28 | enkindle a fire in my heart. |
| 0x29dde5 | 48 | Dekopompo's mood softens as the words of empty\n |
| 0x29de16 | 25 | flattery fill his ears... |
| 0x29de30 | 47 | Hnyeh? Well... Yes, I suppose my behavior has\n |
| 0x29de60 | 46 | been somewhat juvenile. Most uncharacteristic. |
| 0x29de8f | 23 | That guy's pretty good. |
| 0x29dea7 | 48 | Raiko's attendant weaves words of flattery for\n |
| 0x29ded8 | 31 | Dekopompo all but effortlessly. |
| 0x29def8 | 46 | Thank you, milord. I knew your understanding\n |
| 0x29df27 | 43 | heart would forgive me for my impertinence. |
| 0x29df53 | 48 | I always knew you were a man of noble mind and\n |
| 0x29df84 | 11 | soul alike. |
| 0x29df90 | 43 | Ahem! Yes. Well. I am one of noble birth,\n |
| 0x29dfbc | 10 | after all. |
| 0x29dfc7 | 46 | Dekopompo's foul mood immediately dissipates\n |
| 0x29dff6 | 48 | with the praise. I doubt he even remembers why\n |
| 0x29e027 | 13 | he was upset. |
| 0x29e035 | 45 | ...And then Raiko, silent until this point,\n |
| 0x29e063 | 38 | goes and ruins it all in one sentence. |
| 0x29e08a | 40 | I expect this swine to make a habit of\n |
| 0x29e0b3 | 45 | unpleasant displays, but you disappoint me,\n |
| 0x29e0e1 | 10 | Munechika. |
| 0x29e0ec | 5 | Oh... |
| 0x29e0f2 | 6 | Nyeh-- |
| 0x29e0f9 | 42 | My apologies if I caused you discomfort.\n |
| 0x29e124 | 16 | I forgot myself. |
| 0x29e135 | 26 | Munechika nods in apology. |
| 0x29e150 | 9 | Nyurgh... |
| 0x29e15a | 50 | She apologized and admitted wrong in Dekopompo's\n |
| 0x29e18d | 43 | stead, so all he can do is remain silent... |
| 0x29e1b9 | 44 | With his reproach of Munechika done, Raiko\n |
| 0x29e1e6 | 19 | turns on Dekopompo. |
| 0x29e1fa | 50 | Dekopompo... Mine is the duty of "watching over"\n |
| 0x29e22d | 46 | you. This is code for cleaning up after your\n |
| 0x29e25c | 7 | messes. |
| 0x29e264 | 8 | Nyargh!! |
| 0x29e26d | 44 | I do not wish to oppose your every action.\n |
| 0x29e29a | 35 | Such is a waste of time... for now. |
| 0x29e2be | 42 | Should it come to that, I WILL invoke my\n |
| 0x29e2e9 | 41 | office as marshal and assume control of\n |
| 0x29e313 | 14 | this campaign. |
| 0x29e322 | 12 | N-Nyeeargh!? |
| 0x29e32f | 43 | I will not brook whining, nor complaints.\n |
| 0x29e35b | 45 | Return to Yamato and tell them to our liege\n |
| 0x29e389 | 12 | if you wish. |
| 0x29e396 | 45 | But truly, I doubt you are so dim-witted as\n |
| 0x29e3c4 | 46 | not to realize that your presence here is an\n |
| 0x29e3f3 | 13 | act of mercy. |
| 0x29e401 | 48 | Your folly in Uzurusha... You'd do well not to\n |
| 0x29e432 | 48 | forget it. Repeating that mistake will see you\n |
| 0x29e463 | 9 | replaced. |
| 0x29e46d | 49 | B-Bah! My soldiers were unused to the Uzurushan\n |
| 0x29e49f | 47 | terrain. There is no other explanation for my\n |
| 0x29e4cf | 7 | defeat. |
| 0x29e4d7 | 46 | Oh? You make it sound as though victory this\n |
| 0x29e506 | 44 | time is certain. I presume you have a plan\n |
| 0x29e533 | 9 | prepared. |
| 0x29e53d | 48 | O-Of course! A SPLENDID plan. You'd best brace\n |
| 0x29e56e | 46 | yourself, for my plan is astoundingly elegant! |
| 0x29e59d | 48 | We gracefully maneuver around our enemies, use\n |
| 0x29e5ce | 48 | their weaknesses, and adapt until the fortress\n |
| 0x29e5ff | 8 | is ours! |
| 0x29e608 | 53 | A splendid plan indeed! Brilliant in its simplicity\n |
| 0x29e63e | 42 | and elegance. I, Bokoinante, stand in awe. |
| 0x29e669 | 44 | ...How in the world is that a "plan?" Even\n |
| 0x29e696 | 40 | worse, he seems deadly serious about it. |
| 0x29e6bf | 39 | Munechika. You will lead the offensive. |
| 0x29e6e7 | 44 | ...I am a mononofu. It is my sworn duty to\n |
| 0x29e714 | 30 | cross blades with our enemies. |
| 0x29e733 | 44 | That being said... Mine are abilities best\n |
| 0x29e760 | 48 | suited to defense. Don't you wish to reconsider? |
| 0x29e791 | 49 | That is precisely why. A defender of fortresses\n |
| 0x29e7c3 | 41 | should know how best to dismantle one's\n |
| 0x29e7ed | 15 | fortifications. |
| 0x29e7fd | 45 | I will bring up the rear! Rest easy knowing\n |
| 0x29e82b | 34 | I am protecting your supply lines. |
| 0x29e84e | 38 | Dekopompo's mouth curls into a smug,\n |
| 0x29e875 | 20 | self-satisfied grin. |
| 0x29e88a | 47 | We must all play our roles in this war, after\n |
| 0x29e8ba | 27 | all. Will you accept yours? |
| 0x29e8d6 | 50 | Ah, erm--Prithee, hold a moment! Were we to give\n |
| 0x29e909 | 48 | Lady Munechika's proposition its due, mayhaps... |
| 0x29e93a | 45 | Imbecile! You dare suggest we put any stock\n |
| 0x29e968 | 37 | in this "tactical retreat" nonsense!? |
| 0x29e98e | 5 | Eep!? |
| 0x29e994 | 46 | We need no retreat! No trickery! All we need\n |
| 0x29e9c3 | 46 | to do is CRUSH these barbarians in a frontal\n |
| 0x29e9f2 | 8 | assault! |
| 0x29e9fb | 53 | Just so. If their army is truly as lightly-equipped\n |
| 0x29ea31 | 43 | as you say, their defensive capability is\n |
| 0x29ea5d | 11 | paper-thin. |
| 0x29ea69 | 6 | Urk... |
| 0x29ea70 | 28 | So? Does that plan suit you? |
| 0x29ea8d | 47 | Very well. If this course enthuses you so, do\n |
| 0x29eabd | 41 | as you will. Merely remember what I said. |
| 0x29eae7 | 41 | Nyech. A-As long as I win in the end...\n |
| 0x29eb11 | 15 | I know, I know. |
| 0x29eb21 | 45 | I can tell you disagree, Munechika, but you\n |
| 0x29eb4f | 31 | have your orders. Fulfill them. |
| 0x29eb6f | 14 | ...Understood. |
| 0x2a3426 | 48 | I must apologize. I asked you to accompany me,\n |
| 0x2a3457 | 40 | but you must be tired from your travels. |
| 0x2a3480 | 47 | I don't really mind, but why did I need to be\n |
| 0x2a34b0 | 35 | at that meeting in the first place? |
| 0x2a34d4 | 46 | One reason is that I wish you to fully grasp\n |
| 0x2a3503 | 46 | our circumstances. Even now, we generals are\n |
| 0x2a3532 | 8 | divided. |
| 0x2a353b | 48 | I kinda gathered. Raiko doesn't seem too happy\n |
| 0x2a356c | 34 | about having to babysit Dekopompo. |
| 0x2a358f | 45 | The other reason... I was rather hoping you\n |
| 0x2a35bd | 46 | might be able to devise a plan of action for\n |
| 0x2a35ec | 3 | us. |
| 0x2a35f0 | 47 | Well, I'm honored that you think so highly of\n |
| 0x2a3620 | 10 | me, but... |
| 0x2a362b | 48 | Dispense with the modesty. Lord Oshtor himself\n |
| 0x2a365c | 38 | praises your capacity for forethought. |
| 0x2a3683 | 47 | As you've likely gathered, Lord Dekopompo has\n |
| 0x2a36b3 | 48 | become blinded by his reliance on sheer numbers. |
| 0x2a36e4 | 49 | The added pressure of his previous failures has\n |
| 0x2a3716 | 45 | him agitated. In his mind, defeat is not an\n |
| 0x2a3744 | 7 | option. |
| 0x2a374c | 45 | And so he remains adamant that we hold this\n |
| 0x2a377a | 44 | position and fight on, only whittling down\n |
| 0x2a37a7 | 12 | our numbers. |
| 0x2a37b4 | 49 | Should this stalemate continue... It will force\n |
| 0x2a37e6 | 18 | Lord Raiko's hand. |
| 0x2a37f9 | 50 | He mentioned that should he take action, it will\n |
| 0x2a382c | 44 | be to assert total control by invoking his\n |
| 0x2a3859 | 7 | office. |
| 0x2a3861 | 47 | In his capacity as marshal, the ramifications\n |
| 0x2a3891 | 45 | of any strategy he employs would be forgiven. |
| 0x2a38bf | 13 | Any strategy? |
| 0x2a38cd | 26 | I fear it is as it sounds. |
| 0x2a38e8 | 45 | As Munechika's voice adopts a heavy, somber\n |
| 0x2a3916 | 34 | tone, a chill rolls down my spine. |
| 0x2a3939 | 47 | Now that I think about it, I don't think I've\n |
| 0x2a3969 | 48 | ever seen Raiko's battlefield style firsthand... |
| 0x2a399a | 27 | So that's... bad, I assume? |
| 0x2a39b6 | 50 | Lord Raiko views soldiers as pawns upon a board.\n |
| 0x2a39e9 | 43 | To him, war is as a game of numbers. Cold\n |
| 0x2a3a15 | 28 | mathematics and little else. |
| 0x2a3a32 | 41 | I do not mean to question his efficacy.\n |
| 0x2a3a5c | 47 | Only... He is not swayed by such petty things\n |
| 0x2a3a8c | 13 | as "emotion." |
| 0x2a3a9a | 45 | Under his banner, I fear the losses on both\n |
| 0x2a3ac8 | 48 | sides of this war would be too dire to recover\n |
| 0x2a3af9 | 5 | from. |
| 0x2a3aff | 46 | Not simply soldiers on the field--civilians,\n |
| 0x2a3b2e | 46 | too, if he has his way. All of them, corpses\n |
| 0x2a3b5d | 14 | to tread over. |
| 0x2a3b6c | 44 | Think it naive if you must, but I will act\n |
| 0x2a3b99 | 48 | against the coming of such an end any way I can. |
| 0x2a3bca | 49 | I see now. Oshtor did tell me to help Munechika\n |
| 0x2a3bfc | 47 | however I could, and I'd really like to, but... |
| 0x2a3c2c | 47 | It's not like a magic solution to the problem\n |
| 0x2a3c5c | 31 | is just gonna pop into my head. |
| 0x2a3c80 | 43 | Sounds like she's got some kind of animal\n |
| 0x2a3cac | 18 | caged up in there. |
| 0x2a3cbf | 41 | Just pretend not to have heard it, and... |
| 0x2a3ce9 | 44 | ...Tuskur's insect life makes such bizarre\n |
| 0x2a3d16 | 7 | sounds. |
| 0x2a3d1e | 47 | Yeah, you're not fooling anyone. Gutsy to try\n |
| 0x2a3d4e | 39 | and cover up a sound that loud, though. |
| 0x2a3d76 | 47 | You can be rather mean-spirited at times, you\n |
| 0x2a3da6 | 5 | know. |
| 0x2a3dac | 30 | Have you eaten anything today? |
| 0x2a3dcb | 31 | I have, ah... thoughts on that. |
| 0x2a3deb | 3 | Eh? |
| 0x2a3def | 48 | Something about the way she said that feels...\n |
| 0x2a3e20 | 4 | off. |
| 0x2a3e25 | 47 | Munechika, you... haven't been eating at all,\n |
| 0x2a3e55 | 9 | have you? |
| 0x2a3e5f | 45 | I thought she was looking pale. Sickly, even. |
| 0x2a3e8d | 46 | Why haven't you eaten yet? We brought enough\n |
| 0x2a3ebc | 35 | provisions for everyone, I thought. |
| 0x2a3ee0 | 48 | Yes, and I thank you deeply for them--but they\n |
| 0x2a3f11 | 22 | will not last forever. |
| 0x2a3f28 | 48 | We must conserve supplies wherever and however\n |
| 0x2a3f59 | 9 | possible. |
| 0x2a3f63 | 49 | That doesn't mean you should sacrifice your own\n |
| 0x2a3f95 | 38 | health. That's just counterproductive. |
| 0x2a3fbc | 49 | Besides, if the soldiers see their general like\n |
| 0x2a3fee | 37 | this, it's only going to hurt morale. |
| 0x2a4014 | 47 | I know. I... I understand how foolish it must\n |
| 0x2a4044 | 5 | seem. |
| 0x2a404a | 44 | I know how you feel, but we can't have the\n |
| 0x2a4077 | 47 | general stumbling around weak and hungry like\n |
| 0x2a40a7 | 5 | this. |
| 0x2a40ad | 48 | You are right. You are undoubtedly right, but... |
| 0x2a40de | 48 | I mean, I get where she's coming from. If this\n |
| 0x2a410f | 48 | stalemate keeps up, even the new supplies will\n |
| 0x2a4140 | 6 | drain. |
| 0x2a4147 | 45 | In other words, Munechika thinks conquering\n |
| 0x2a4175 | 44 | Tuskur is going to be a long, hard campaign. |
| 0x2a41a2 | 48 | Which means we need to prioritize securing our\n |
| 0x2a41d3 | 48 | supply lines for the future. It's worse than I\n |
| 0x2a4204 | 8 | thought. |
| 0x2a420d | 49 | Fighting in a land where the enemy has complete\n |
| 0x2a423f | 46 | control of the roads must be hitting you hard. |
| 0x2a426e | 32 | It was carelessness on our part. |
| 0x2a428f | 42 | No matter how many resupply missions are\n |
| 0x2a42ba | 45 | mounted, if they're taken before they reach\n |
| 0x2a42e8 | 5 | us... |
| 0x2a42ee | 12 | Stolen, huh. |
| 0x2a42fb | 45 | It's probably easier said than done that we\n |
| 0x2a4329 | 44 | should just steal the provisions back again. |
| 0x2a4356 | 46 | If the back of the fortress is a sheer drop,\n |
| 0x2a4385 | 44 | that means the only angle of attack is the\n |
| 0x2a43b2 | 8 | front... |
| 0x2a43bb | 46 | ...Where all their defenses will be focused.\n |
| 0x2a43ea | 35 | They'd hardly just let us waltz in. |
| 0x2a440e | 49 | Which means attacking the fortress head-on is a\n |
| 0x2a4440 | 28 | pointless endeavor. Unless-- |
| 0x2a445d | 30 | ...Uruuru. Saraana. You there? |
| 0x2a447c | 13 | By your side. |
| 0x2a448a | 27 | Speak, and we shall listen. |
| 0x2a44a6 | 47 | I'm going to go have a look at this fortress.\n |
| 0x2a44d6 | 20 | Tell the others to-- |
| 0x2a44eb | 19 | We will escort you. |
| 0x2a44ff | 43 | We remain forever by your side, our Master. |
| 0x2a452b | 47 | Yeeeaaah, I had a feeling you'd say something\n |
| 0x2a455b | 20 | like that. Whatever. |
| 0x2a4570 | 27 | You're going...? Thank you. |
| 0x2a458c | 48 | Don't worry about it. Besides, it's not like I\n |
| 0x2a45bd | 46 | can do anything before I scope this place out. |
| 0x2a45ec | 24 | I await good news, then. |
| 0x2a4605 | 32 | So I'm here for recon and all... |
| 0x2a4626 | 8 | Hee hee. |
| 0x2a462f | 7 | Ah heh. |
| 0x2a4637 | 34 | But why the hell are you all here? |
| 0x2a465a | 45 | Well, it's not like there's anything better\n |
| 0x2a4688 | 19 | to do back at camp. |
| 0x2a469c | 47 | Yeah, this is way more fun than anything back\n |
| 0x2a46cc | 6 | there. |
| 0x2a46d3 | 50 | Reconnaissance and infiltration of secure places\n |
| 0x2a4706 | 45 | is what I do. Why didn't you call on me for\n |
| 0x2a4734 | 5 | this? |
| 0x2a473a | 47 | I'm hardly about to let you do something this\n |
| 0x2a476a | 22 | dangerous alone, Haku. |
| 0x2a4781 | 47 | I was just planning on checking out the area.\n |
| 0x2a47b1 | 20 | Don't worry so much. |
| 0x2a47c6 | 49 | So what kind of sightseeing did we come here to\n |
| 0x2a47f8 | 3 | do? |
| 0x2a47fc | 45 | Sightseeing...? We're not here for leisure.\n |
| 0x2a482a | 42 | We're scouting out the Tuskur fortress's\n |
| 0x2a4855 | 9 | defenses. |
| 0x2a485f | 49 | I want to see if we might be able to steal back\n |
| 0x2a4891 | 24 | those pillaged supplies. |
| 0x2a48aa | 45 | From what I've heard, the defenses are rock\n |
| 0x2a48d8 | 47 | solid, but I wanted to see firsthand if there\n |
| 0x2a4908 | 15 | might be a gap. |
| 0x2a4918 | 32 | Take back the stolen supplies... |
| 0x2a4939 | 19 | If we can, that is. |
| 0x2a494d | 48 | I guess it can't be helped, if you all plan on\n |
| 0x2a497e | 35 | following me. Let's go around back. |
| 0x2a49a2 | 20 | Damn, that's tall... |
| 0x2a49b7 | 48 | According to scout reports, atop this cliff is\n |
| 0x2a49e8 | 42 | the warehouse they keep their supplies in. |
| 0x2a4a13 | 48 | Not only is the cliff tall, but it's extremely\n |
| 0x2a4a44 | 11 | steep, too. |
| 0x2a4a50 | 45 | Imagine the effort that must have gone into\n |
| 0x2a4a7e | 45 | building a stronghold in a place like this... |
| 0x2a4aac | 20 | Any sign of enemies? |
| 0x2a4ac1 | 12 | Searching... |
| 0x2a4ace | 50 | We cannot sense enemy movements in the immediate\n |
| 0x2a4b01 | 5 | area. |
| 0x2a4b07 | 44 | I don't see anything... nor do I sense any\n |
| 0x2a4b34 | 21 | presence around here. |
| 0x2a4b4a | 46 | So they don't guard this area heavily, then... |
| 0x2a4b79 | 49 | Well, if I were them, I wouldn't exactly expect\n |
| 0x2a4bab | 43 | an enemy force to charge up the cliff face. |
| 0x2a4bd7 | 38 | Ougi, would you be able to climb this? |
| 0x2a4bfe | 44 | Ah, let's see... There aren't a great many\n |
| 0x2a4c2b | 43 | handholds, and the angle gets steeper and\n |
| 0x2a4c57 | 10 | steeper... |
| 0x2a4c62 | 42 | I never say never, but I'd rather not try. |
| 0x2a4c8d | 6 | I see. |
| 0x2a4c94 | 43 | To be honest, it'd be close to impossible\n |
| 0x2a4cc0 | 21 | unless you could fly. |
| 0x2a4cd6 | 11 | Fly, huh... |
| 0x2a4ce2 | 36 | Hey, Neko. You know any ways to fly? |
| 0x2a4d07 | 48 | Please. Beyond defying all logic and sprouting\n |
| 0x2a4d38 | 43 | wings, none of us are flying any time soon. |
| 0x2a4d64 | 47 | Really? But wasn't Kuon's sister flying about\n |
| 0x2a4d94 | 26 | in the sky, that one time? |
| 0x2a4daf | 47 | If SHE can fly, maybe we ought to strap wings\n |
| 0x2a4ddf | 38 | to our arms and flap until we can fly! |
| 0x2a4e06 | 11 | That, ah... |
| 0x2a4e12 | 50 | Nekone looks troubled for a moment, until Nosuri\n |
| 0x2a4e45 | 45 | steps in to answer the question in her stead. |
| 0x2a4e73 | 45 | That would be impossible. You may gain some\n |
| 0x2a4ea1 | 49 | airtime, but not lift. You'd crash right to the\n |
| 0x2a4ed3 | 7 | ground. |
| 0x2a4edb | 46 | Oh. You're pretty knowledgeable, aren't you,\n |
| 0x2a4f0a | 7 | Nosuri? |
| 0x2a4f12 | 50 | Ahaha, I don't mean to brag, of course--but yes!\n |
| 0x2a4f45 | 46 | I am. A good woman has knowledge of all kinds. |
| 0x2a4f74 | 47 | Yes, well--she also has firsthand experience.\n |
| 0x2a4fa4 | 47 | I remember when she fell out of a tree trying\n |
| 0x2a4fd4 | 3 | it. |
| 0x2a4fd8 | 10 | Ahahaha... |
| 0x2a4fe3 | 48 | Astounding. I never would have thought someone\n |
| 0x2a5014 | 30 | would attempt that in reality. |
| 0x2a5033 | 49 | I figured as much. I'm surprised you managed to\n |
| 0x2a5065 | 30 | get airtime trying it, though. |
| 0x2a5084 | 47 | Then how did Kuon's sister fly with such thin\n |
| 0x2a50b4 | 6 | wings? |
| 0x2a50bb | 48 | My sister and... others of Onkamiyaryu possess\n |
| 0x2a50ec | 28 | mastery over certain powers. |
| 0x2a5109 | 30 | She was flying by other means. |
| 0x2a5128 | 47 | Besides, from what I can tell, it's more like\n |
| 0x2a5158 | 39 | floating or gliding than actual flight. |
| 0x2a5180 | 46 | I guess so. Now that I think back on it, she\n |
| 0x2a51af | 39 | was just sort of... hanging in the air. |
| 0x2a51d7 | 26 | Like a balloon or someth-- |
| 0x2a51f2 | 13 | ...A balloon. |
| 0x2a5200 | 8 | Haku...? |
| 0x2a5209 | 16 | That--That's it! |
| 0x2a521a | 21 | Wh-What's the matter? |
| 0x2a5230 | 46 | If we can use a balloon to get up there--no,\n |
| 0x2a525f | 47 | a regular one is too small. We need a hot-air\n |
| 0x2a528f | 8 | balloon! |
| 0x2a5298 | 42 | It wouldn't even need to be able to move\n |
| 0x2a52c3 | 48 | laterally. As long as I can build one to go up\n |
| 0x2a52f4 | 11 | and down... |
| 0x2a5300 | 48 | It's just an armchair theory, though. I mean--\n |
| 0x2a5331 | 35 | what would I even do for materials? |
| 0x2a5355 | 44 | Where would I find something even remotely\n |
| 0x2a5382 | 45 | appropriate? It'd need to be light, sturdy,\n |
| 0x2a53b0 | 11 | airtight... |
| 0x2a53bc | 45 | Everyone watches me suspiciously as I go on\n |
| 0x2a53ea | 43 | muttering. Kuon, meanwhile, seems to find\n |
| 0x2a5416 | 10 | something. |
| 0x2a5421 | 22 | Oh, look what I found. |
| 0x2a543a | 48 | Kuon wanders over to a bizarrely large flower,\n |
| 0x2a546b | 31 | digging at the dirt beneath it. |
| 0x2a548b | 33 | Is that flower special somehow?\n |
| 0x2a54ad | 48 | ...Is it even a flower? It's got an odd scent... |
| 0x2a54de | 26 | Could that be a yanmororo? |
| 0x2a54f9 | 48 | Mhm. The roots are edible, if you prepare them\n |
| 0x2a552a | 50 | right. It could help the food shortage. Help me,\n |
| 0x2a555d | 7 | Nekone? |
| 0x2a5565 | 14 | Ah, of course. |
| 0x2a5574 | 45 | As the rest of us watch on, Kuon and Nekone\n |
| 0x2a55a2 | 47 | dig out a large, plump bulb, easily as big as\n |
| 0x2a55d2 | 12 | their hands. |
| 0x2a55df | 44 | Ah, so that's the edible part? How does it\n |
| 0x2a560c | 6 | taste? |
| 0x2a5613 | 47 | Uh... I'd say it doesn't really HAVE a taste?\n |
| 0x2a5643 | 47 | It's bland, but it should keep you full for a\n |
| 0x2a5673 | 6 | while. |
| 0x2a567a | 31 | I see. It's... pretty big, huh. |
| 0x2a569a | 44 | Hard to imagine something like this has no\n |
| 0x2a56c7 | 31 | taste... May I, ah, hold it...? |
| 0x2a56e7 | 48 | Oh, be careful when you handle a yanmororo bulb. |
| 0x2a5718 | 7 | Huh...? |
| 0x2a5720 | 46 | Yes. It's poisonous uncooked. Keep it out of\n |
| 0x2a574f | 32 | your eyes, and never eat it raw. |
| 0x2a5770 | 46 | Wh--poisonous!? Are you sure we can eat these? |
| 0x2a579f | 42 | Mhm. It's completely safe as long as you\n |
| 0x2a57ca | 26 | observe proper procedures. |
| 0x2a57e5 | 48 | There seem to be a lot of them around here, so\n |
| 0x2a5816 | 45 | do me a favor and dig up any you come across. |
| 0x2a5844 | 47 | Something wrong, Haku? If you could help dig,\n |
| 0x2a5874 | 25 | too, I'd appreciate it... |
| 0x2a588e | 49 | Judging by the shape, the texture... Could this\n |
| 0x2a58c0 | 13 | be... konjac? |
| 0x2a58ce | 7 | Konjac? |
| 0x2a58d6 | 27 | Konjac...hot air balloon... |
| 0x2a58f2 | 5 | Ah... |
| 0x2a58f8 | 42 | That's it. I've got it. It'll be a risky\n |
| 0x2a5923 | 34 | proposition, but with some luck... |
| 0x2a5946 | 5 | Haku? |
| 0x2a594c | 46 | Kuon... I know how we're going to get at the\n |
| 0x2a597b | 18 | storage warehouse. |
| 0x2a598e | 4 | Huh? |
| 0x2a5993 | 18 | A-Are you certain? |
| 0x2a59a6 | 42 | How do you plan on surpassing the cliff?\n |
| 0x2a59d1 | 41 | I hardly imagine you intend on making a\n |
| 0x2a59fb | 16 | frontal assault. |
| 0x2a5a0c | 44 | No, this isn't that reckless. I mean--yes,\n |
| 0x2a5a39 | 43 | OK, it's reckless, but not STUPID reckless. |
| 0x2a5a65 | 48 | More importantly--Kuon, what are you gonna do?\n |
| 0x2a5a96 | 46 | You can... pretend you didn't hear anything,\n |
| 0x2a5ac5 | 7 | y'know. |
| 0x2a5acd | 7 | Haku... |
| 0x2a5ad5 | 45 | You still have time. Think carefully before\n |
| 0x2a5b03 | 22 | you give me an answer. |
| 0x2a5b1a | 50 | We quickly dig up as many of the yanmororo bulbs\n |
| 0x2a5b4d | 41 | as we can, then go back to camp to make\n |
| 0x2a5b77 | 13 | preparations. |
| 0x2a5b85 | 5 | Ouch! |
| 0x2a5b8b | 38 | Nekone gives a surprised yelp as she\n |
| 0x2a5bb2 | 41 | accidentally pricks her finger with the\n |
| 0x2a5bdc | 14 | sewing needle. |
| 0x2a5beb | 11 | Are you OK? |
| 0x2a5bf7 | 40 | I-I am all right. Merely a small poke... |
| 0x2a5c20 | 35 | Oh, you're bleeding! Here, let me-- |
| 0x2a5c44 | 49 | Kuon takes Nekone's hand in hers, then sucks on\n |
| 0x2a5c76 | 19 | the injured finger. |
| 0x2a5c8a | 34 | D-Dear sister, you don't have to-- |
| 0x2a5cad | 10 | It's fine. |
| 0x2a5cb8 | 39 | Those two are getting along, as ever... |
| 0x2a5ce0 | 31 | Haku, your hands aren't moving. |
| 0x2a5d00 | 17 | Oh, right. Sorry. |
| 0x2a5d12 | 45 | Jachdwalt, Kiwru, and I all grate yanmororo\n |
| 0x2a5d40 | 41 | while Kuon's group sews pieces of cloth\n |
| 0x2a5d6a | 11 | together... |
| 0x2a5d76 | 49 | All the extra scraps of cloth I'd gathered from\n |
| 0x2a5da8 | 46 | camp will ultimately form a single, enormous\n |
| 0x2a5dd7 | 6 | sheet. |
| 0x2a5dde | 45 | With Munechika's help, I was able to obtain\n |
| 0x2a5e0c | 44 | permission to gather all the cloth I needed. |
| 0x2a5e39 | 48 | Rulutieh and the twins seem to be decent hands\n |
| 0x2a5e6a | 44 | at sewing, so that part is going smoothly... |
| 0x2a5e97 | 41 | ...While I watch Nekone and Nosuri stab\n |
| 0x2a5ec1 | 49 | themselves with their needles for the umpteenth\n |
| 0x2a5ef3 | 5 | time. |
| 0x2a5ef9 | 46 | With Rulutieh overseeing the sewing, though,\n |
| 0x2a5f28 | 20 | I'm not too worried. |
| 0x2a5f3d | 11 | Hm hm hm... |
| 0x2a5f49 | 14 | Hup, hup, hup. |
| 0x2a5f58 | 48 | I didn't expect you two to be this good with a\n |
| 0x2a5f89 | 28 | needle and thread, honestly. |
| 0x2a5fa6 | 32 | Well, that's just rude, I think. |
| 0x2a5fc7 | 46 | Sewing is a key skill for the solo traveler.\n |
| 0x2a5ff6 | 46 | Your clothes go through a lot when you're on\n |
| 0x2a6025 | 7 | the go. |
| 0x2a602d | 31 | Yeah, I guess that makes sense. |
| 0x2a604d | 49 | Of course, it's not just mending I have a knack\n |
| 0x2a607f | 48 | for. I can make stuff, too. Like these clothes\n |
| 0x2a60b0 | 10 | I have on! |
| 0x2a60bb | 48 | Ah--I can make some new clothes for you later,\n |
| 0x2a60ec | 12 | if you like? |
| 0x2a60f9 | 15 | Clothes for me? |
| 0x2a6109 | 48 | Yeah. You don't seem like you're, uh, terribly\n |
| 0x2a613a | 48 | big on fashion. You wear the same things every\n |
| 0x2a616b | 4 | day. |
| 0x2a6170 | 49 | Well, if you're offering, I'm not gonna refuse... |
| 0x2a61a2 | 8 | Clothes? |
| 0x2a61ab | 11 | For Master? |
| 0x2a61b7 | 35 | Do you desire new clothing, Master? |
| 0x2a61db | 46 | Suddenly, several of the girls in the sewing\n |
| 0x2a620a | 42 | circle approach me, needles still in hand. |
| 0x2a6235 | 20 | I will fashion some. |
| 0x2a624a | 47 | I will also set about making new garments for\n |
| 0x2a627a | 4 | you. |
| 0x2a627f | 48 | I-I'll make some, too, if we have any leftover\n |
| 0x2a62b0 | 8 | cloth... |
| 0x2a62b9 | 42 | U-Um, well--I'd prefer if you... didn't,\n |
| 0x2a62e4 | 9 | actually. |
| 0x2a62ee | 23 | You... don't want them? |
| 0x2a6306 | 45 | Gah, no, it's not that I don't want clothes\n |
| 0x2a6334 | 13 | made by you-- |
| 0x2a6342 | 40 | Even if no cloth remains, I will do as\n |
| 0x2a636b | 10 | commanded. |
| 0x2a6376 | 44 | If you wish it, we can disassemble our own\n |
| 0x2a63a3 | 45 | clothing and fashion your new wardrobe from\n |
| 0x2a63d1 | 11 | the pieces. |
| 0x2a63dd | 44 | Don't... Don't take off your clothes here,\n |
| 0x2a640a | 47 | please. Or at all. We'll talk about this later. |
| 0x2a643a | 49 | In a bid to change the subject, I turn abruptly\n |
| 0x2a646c | 8 | to Atuy. |
| 0x2a6475 | 49 | S-So, uh, Atuy. You're pretty good at this too,\n |
| 0x2a64a7 | 7 | huh...? |
| 0x2a64af | 45 | Well, my reason's pretty similar to Kuon's!\n |
| 0x2a64dd | 48 | Living on a ship, you learn to repair canvases\n |
| 0x2a650e | 9 | and nets. |
| 0x2a6518 | 46 | Most of Papa's clothes are things I made for\n |
| 0x2a6547 | 14 | him, actually. |
| 0x2a6556 | 19 | Oh, you made those? |
| 0x2a656a | 37 | Maybe I'll do the same for you, love. |
| 0x2a6590 | 3 | Uh? |
| 0x2a6594 | 48 | I'm starting to get a really bad feeling about\n |
| 0x2a65c5 | 9 | all this. |
| 0x2a65cf | 24 | How go the preparations? |
| 0x2a65e8 | 47 | I turn to the source of the new voice to find\n |
| 0x2a6618 | 10 | Munechika. |
| 0x2a6623 | 34 | Eh, it's... going. So-so, I guess. |
| 0x2a6646 | 39 | You speak the truth when you say this\n |
| 0x2a666e | 34 | contrivance will float in the air? |
| 0x2a6691 | 51 | Munechika looks over the giant, stitched-together\n |
| 0x2a66c5 | 40 | sheet of cloth the girls are working on. |
| 0x2a66ee | 41 | Yes. I admit to never encountering this\n |
| 0x2a6718 | 41 | particular technique, but the governing\n |
| 0x2a6742 | 21 | principles are sound. |
| 0x2a6758 | 50 | ...Has nobody pointed out yet that it's going to\n |
| 0x2a678b | 46 | hurt if we fall? There'll be broken arms, at\n |
| 0x2a67ba | 6 | LEAST. |
| 0x2a67c1 | 50 | If we fall from that cliff, I think that's gonna\n |
| 0x2a67f4 | 33 | be more like "broken everything." |
| 0x2a6816 | 33 | M-Miss Atuy, please don't joke... |
| 0x2a6838 | 45 | Don't worry about it. We've pulled off more\n |
| 0x2a6866 | 47 | ridiculous schemes than this. It'll be a walk\n |
| 0x2a6896 | 12 | in the park. |
| 0x2a68a3 | 47 | Well, you ARE the king of ridiculous schemes,\n |
| 0x2a68d3 | 47 | Haku--even if you're a layabout and a lazy bum. |
| 0x2a6903 | 47 | This "hot air balloon" seems quite plausible.\n |
| 0x2a6933 | 48 | I know of a small-scale proof of concept using\n |
| 0x2a6964 | 8 | paper... |
| 0x2a696d | 48 | But never a full-size application. No material\n |
| 0x2a699e | 45 | would work--but cloth rubbed with yanmororo\n |
| 0x2a69cc | 12 | could do it. |
| 0x2a69d9 | 50 | The air tightness lent by the yanmororo fiber is\n |
| 0x2a6a0c | 47 | a sound principle, but I had never considered\n |
| 0x2a6a3c | 5 | it... |
| 0x2a6a42 | 47 | Ahaha, well, sometimes you just need to think\n |
| 0x2a6a72 | 16 | outside the box. |
| 0x2a6a83 | 47 | The group turns to me with no small amount of\n |
| 0x2a6ab3 | 20 | awe in their eyes... |
| 0x2a6ac8 | 49 | ...Is what I'd LIKE to say, but I'm pretty sure\n |
| 0x2a6afa | 29 | I just got lucky on this one. |
| 0x2a6b18 | 43 | But I have to keep the aura of confidence\n |
| 0x2a6b44 | 44 | rolling if this crazy plan is going to work. |
| 0x2a6b71 | 36 | Exaggeration is the word of the day. |
| 0x2a6b96 | 44 | ...I'm still not certain I fully grasp the\n |
| 0x2a6bc3 | 45 | details, but we will support you however we\n |
| 0x2a6bf1 | 4 | can. |
| 0x2a6bf6 | 46 | This'll sound weird from the guy who came up\n |
| 0x2a6c25 | 43 | with it--I'm surprised you agreed to this\n |
| 0x2a6c51 | 12 | insane idea. |
| 0x2a6c5e | 38 | Lord Oshtor trusts you, and so do I.\n |
| 0x2a6c85 | 49 | Perhaps it sounds odd, but... You give me hope,\n |
| 0x2a6cb7 | 10 | Lord Haku. |
| 0x2a6cc2 | 49 | I'm not sure I've done anything to deserve this\n |
| 0x2a6cf4 | 21 | much of your trust... |
| 0x2a6d0a | 38 | But you have. The princess is smiling. |
| 0x2a6d31 | 20 | The princess... huh? |
| 0x2a6d46 | 42 | You heard me. It is no easy feat to make\n |
| 0x2a6d71 | 22 | Her Highness smile so. |
| 0x2a6d88 | 50 | As of late, however, she often smiles so broadly\n |
| 0x2a6dbb | 48 | that it infects those around her... Ever since\n |
| 0x2a6dec | 9 | you came. |
| 0x2a6df6 | 46 | I sense a kind of greatness in you for that.\n |
| 0x2a6e25 | 36 | As such, you have my implicit trust. |
| 0x2a6e4a | 32 | Still not sure I quite get it... |
| 0x2a6e6b | 43 | Well, we'll do our best to pull this off,\n |
| 0x2a6e97 | 40 | just... Don't get your hopes too high.\n |
| 0x2a6ec0 | 18 | It makes pressure. |
| 0x2a6ed3 | 43 | Haha.... I don't think anyone's ever said\n |
| 0x2a6eff | 26 | something like that to me. |
| 0x2a6f1a | 24 | Thank you for your time. |
| 0x2a6f33 | 49 | Welp. As you all may have heard, certain people\n |
| 0x2a6f65 | 47 | are putting their trust in us. Let's get this\n |
| 0x2a6f95 | 5 | done. |
| 0x2a6f9b | 45 | I remain surprised you managed to find this\n |
| 0x2a6fc9 | 17 | much scrap cloth. |
| 0x2a6fdb | 49 | Yes... Sir Haku and Sir Ougi went all over camp\n |
| 0x2a700d | 15 | gathering it... |
| 0x2a701d | 47 | ...Even so, it is not abundantly clean, either. |
| 0x2a704d | 47 | *Sniff*... There's something off about how it\n |
| 0x2a707d | 12 | smells, too. |
| 0x2a708a | 48 | Really? I made sure to wash it all beforehand,\n |
| 0x2a70bb | 30 | so it shouldn't be that bad... |
| 0x2a70da | 45 | Wash? You mean they were even dirtier before? |
| 0x2a7108 | 44 | ...Did you pick these up off the ground or\n |
| 0x2a7135 | 10 | something? |
| 0x2a7140 | 46 | Oh, come on. You'll hurt the feelings of the\n |
| 0x2a716f | 38 | people who kindly donated these to us. |
| 0x2a7196 | 11 | Beg pardon? |
| 0x2a71a2 | 47 | Be a little more careful with them. These are\n |
| 0x2a71d2 | 44 | the loincloths of every soldier in the army. |
| 0x2a71ff | 50 | Kuon and the others immediately drop the needles\n |
| 0x2a7232 | 15 | in their hands. |
| 0x2a7242 | 5 | Gah!? |
| 0x2a724b | 15 | Urp... Hrrrk... |
| 0x2a725b | 14 | Ah... ahaha... |
| 0x2a726a | 5 | Oh... |
| 0x2a7270 | 46 | Oh, and all us guys donated a few extras, too. |
| 0x2a729f | 10 | Hey, Haku? |
| 0x2a72aa | 5 | Yeah? |
| 0x2a72b0 | 41 | Kuon smiles at me sweetly... Then in an\n |
| 0x2a72da | 41 | eyeblink, wraps her tail around my head\n |
| 0x2a7304 | 8 | tightly. |
| 0x2a730d | 16 | W-Wait! Hold on! |
| 0x2a731e | 33 | Nope. No getting out of this one. |
| 0x2a7340 | 48 | Argh... You're not gonna be satisfied until my\n |
| 0x2a7371 | 41 | head looks like an hourglass, are you...? |
| 0x2a739b | 43 | Now, be sure you're wearing those leather\n |
| 0x2a73c7 | 42 | gloves. Don't touch this stuff with your\n |
| 0x2a73f2 | 11 | bare hands. |
| 0x2a73fe | 47 | We all pour the grated yanmororo into buckets\n |
| 0x2a742e | 43 | and begin to rub it like a paste into the\n |
| 0x2a745a | 11 | loincloths. |
| 0x2a7466 | 46 | It's rote work, and it takes ages--I'm bored\n |
| 0x2a7495 | 43 | half to death by the time Atuy breaks the\n |
| 0x2a74c1 | 9 | monotony. |
| 0x2a74cb | 45 | Hey, you said this stuff is edible and all,\n |
| 0x2a74f9 | 44 | right? Should we be using this much of it,\n |
| 0x2a7526 | 15 | considering...? |
| 0x2a7536 | 47 | Ah, um... You shouldn't eat it raw, remember... |
| 0x2a7566 | 47 | I thought you'd say something like that, so I\n |
| 0x2a7596 | 47 | prepared some yanmororo to eat. Shall we take\n |
| 0x2a75c6 | 8 | a break? |
| 0x2a75cf | 31 | That's my Kuon! So considerate. |
| 0x2a75ef | 41 | Kuon steps away from pasting the ground\n |
| 0x2a7619 | 47 | yanmororo onto the cloth to carefully set out\n |
| 0x2a7649 | 7 | dishes. |
| 0x2a7651 | 47 | She produces a cutting board and a knife from\n |
| 0x2a7681 | 44 | somewhere, then carefully unwraps a package. |
| 0x2a76ae | 28 | This ought to do, I suppose? |
| 0x2a76cb | 46 | Kuon fishes a grey, jelly-like lump from the\n |
| 0x2a76fa | 22 | package as she speaks. |
| 0x2a7711 | 11 | Is this...? |
| 0x2a771d | 25 | It feels... very springy? |
| 0x2a7737 | 18 | Is this like Rulu? |
| 0x2a774a | 43 | Oh... I-I think I know what this is. It's\n |
| 0x2a7776 | 44 | nyaku-nyaku, right...? I've never actually\n |
| 0x2a77a3 | 10 | seen it... |
| 0x2a77ae | 50 | I have read of nyaku-nyaku. A traditional health\n |
| 0x2a77e1 | 35 | food through the ages, if I recall. |
| 0x2a7805 | 39 | How exactly are you supposed to eat it? |
| 0x2a782d | 44 | Well, first you slice it into thin strips... |
| 0x2a785a | 47 | Kuon takes the knife and cuts into the lump--\n |
| 0x2a788a | 46 | apparently made from yanmororo liquefied and\n |
| 0x2a78b9 | 19 | then reconstituted. |
| 0x2a78cd | 30 | All right, let's have a taste. |
| 0x2a78ec | 44 | Jachdwalt snatches several pieces with his\n |
| 0x2a7919 | 43 | chopsticks and pops them into his waiting\n |
| 0x2a7945 | 6 | mouth. |
| 0x2a794c | 13 | This stuff... |
| 0x2a795a | 11 | This stuff? |
| 0x2a7966 | 23 | ...has no taste at all. |
| 0x2a797e | 45 | No taste? No way. It looks so much like the\n |
| 0x2a79ac | 22 | Rulu, it's gotta be... |
| 0x2a79c3 | 50 | Well, it's got a funny texture, if nothing else.\n |
| 0x2a79f6 | 45 | Kinda squishy? Feels like I'm eating a cloud. |
| 0x2a7a24 | 42 | D-Dear sister, could you perhaps have...\n |
| 0x2a7a4f | 20 | mistaken the recipe? |
| 0x2a7a64 | 46 | Ahahaha, it's not SUPPOSED to have a flavor.\n |
| 0x2a7a93 | 46 | That's how you know you did it right. Try it\n |
| 0x2a7ac2 | 11 | with sauce. |
| 0x2a7ace | 21 | Ah, this is better... |
| 0x2a7ae4 | 17 | Quite intriguing. |
| 0x2a7af6 | 33 | This sauce is unfamiliar to me... |
| 0x2a7b18 | 40 | It's just common Tuskur seasonings and\n |
| 0x2a7b41 | 8 | vinegar. |
| 0x2a7b4a | 46 | We all take some time to enjoy the yanmororo\n |
| 0x2a7b79 | 7 | dish... |
| 0x2a7b81 | 48 | And with our break complete, we finish pasting\n |
| 0x2a7bb2 | 47 | on the yanmororo. Now to let it dry for a day\n |
| 0x2a7be2 | 6 | or so. |
| 0x2a7be9 | 48 | That's all the preparations done. Nothing left\n |
| 0x2a7c1a | 44 | to do but wait and see how it all turns out. |
| 0x2a7c47 | 16 | Well, off we go. |
| 0x2a7c58 | 44 | Are you sure you don't need any additional\n |
| 0x2a7c85 | 9 | soldiers? |
| 0x2a7c8f | 41 | This is more of a heist than a military\n |
| 0x2a7cb9 | 48 | operation. More people will only attract undue\n |
| 0x2a7cea | 10 | attention. |
| 0x2a7cf5 | 45 | Besides, only so many people can fit in the\n |
| 0x2a7d23 | 49 | balloon, and we're used to these kinds of jobs.\n |
| 0x2a7d55 | 11 | Moreover... |
| 0x2a7d61 | 48 | I understand. I will place a group of soldiers\n |
| 0x2a7d92 | 43 | within sight of the gates to divert their\n |
| 0x2a7dbe | 9 | sentries. |
| 0x2a7dc8 | 7 | Thanks. |
| 0x2a7dd0 | 42 | I look forward to hearing of your success. |
| 0x2a7dfb | 47 | I turn toward Kuon, who seems to be wearing a\n |
| 0x2a7e2b | 30 | stiffer expression than usual. |
| 0x2a7e4a | 34 | I guess I should ask just in case. |
| 0x2a7e6d | 46 | I take a moment to work up the resolve, then\n |
| 0x2a7e9c | 34 | open my mouth to ask her directly. |
| 0x2a7ebf | 47 | I'm going to ask one last time, Kuon. Are you\n |
| 0x2a7eef | 38 | OK with this? We'll be fighting your\n |
| 0x2a7f16 | 11 | countrymen. |
| 0x2a7f22 | 46 | I understand you've seen this through so far\n |
| 0x2a7f51 | 27 | because we're your friends. |
| 0x2a7f6d | 47 | But Tuskur is your home. I don't want to make\n |
| 0x2a7f9d | 22 | you kill your own kin. |
| 0x2a7fb4 | 44 | If we end up encountering someone you know-- |
| 0x2a7fe1 | 46 | I'm going with you. I'm worried about you all. |
| 0x2a8010 | 23 | ...That is my decision. |
| 0x2a8028 | 21 | Kuon mutters quietly. |
| 0x2a803e | 7 | Kuon... |
| 0x2a8046 | 31 | It's true that I'm from Tuskur. |
| 0x2a8066 | 45 | But I wouldn't be able to live with myself,\n |
| 0x2a8094 | 44 | knowing you're far away, risking your lives. |
| 0x2a80c1 | 9 | ...I see. |
| 0x2a80cb | 51 | It's all right. All I need to do is incapacitate,\n |
| 0x2a80ff | 38 | not kill... I can go for their legs... |
| 0x2a8126 | 46 | ...I just... I hope those two don't show up... |
| 0x2a8155 | 22 | Hm? You say something? |
| 0x2a816c | 17 | No, it's nothing. |
| 0x2a817e | 44 | Maybe the threat of Raiko's scorched-earth\n |
| 0x2a81ab | 28 | tactics is motivating her... |
| 0x2a81c8 | 49 | She wants to keep casualties on both sides to a\n |
| 0x2a81fa | 34 | minimum to avoid approaching that. |
| 0x2a821d | 45 | Maybe she plans on brokering negotiations...? |
| 0x2a824b | 50 | All right, I understand. I really appreciate you\n |
| 0x2a827e | 15 | coming with us. |
| 0x2a828e | 8 | ...Haku. |
| 0x2a8297 | 3 | Hm? |
| 0x2a829b | 10 | Thank you. |
| 0x2a82a6 | 12 | Huh? Sure... |
| 0x2a82b3 | 42 | Kuon finally smiles, then moves to where\n |
| 0x2a82de | 22 | Munechika is standing. |
| 0x2a82f5 | 47 | Miss Munechika, I... need to ask you something. |
| 0x2a8325 | 10 | Lady Kuon? |
| 0x2a8330 | 44 | Have you seen an enemy commander, riding a\n |
| 0x2a835d | 46 | white steed? And another man who seems to be\n |
| 0x2a838c | 15 | his lieutenant? |
| 0x2a839c | 49 | Yes... I have clapped eyes on the pair of them.\n |
| 0x2a83ce | 47 | They seem to be a cut above most other Tuskur\n |
| 0x2a83fe | 9 | warriors. |
| 0x2a8408 | 43 | Please... don't fight them. Either of them. |
| 0x2a8434 | 6 | Hm...? |
| 0x2a843b | 44 | I apologize, Lady Kuon, but one's personal\n |
| 0x2a8468 | 48 | feelings have no place in a war. I cannot keep\n |
| 0x2a8499 | 13 | that promise. |
| 0x2a84a7 | 9 | Please... |
| 0x2a84b1 | 49 | Kuon looks at her with pleading eyes for a long\n |
| 0x2a84e3 | 46 | moment, and Munechika finally seems to relent. |
| 0x2a8512 | 46 | ...I shall do my best. If we cross blades, I\n |
| 0x2a8541 | 39 | will prioritize securing a surrender.\n |
| 0x2a8569 | 21 | That is all I can do. |
| 0x2a857f | 13 | ...Thank you. |
| 0x2a858d | 47 | Shall we be off? We have a big load to carry,\n |
| 0x2a85bd | 45 | and we need to be at our destination before\n |
| 0x2a85eb | 5 | noon. |
| 0x2a85f1 | 7 | Yeah... |
| 0x2a85f9 | 44 | I didn't expect Kuon to say something like\n |
| 0x2a8626 | 33 | that. Does she know those two...? |
| 0x2a8648 | 46 | Form ranks! We depart as soon as Lord Haku's\n |
| 0x2a8677 | 16 | contingent does. |
| 0x2a8688 | 47 | Yes, yes, lead the charge! I leave it to you.\n |
| 0x2a86b8 | 44 | I shall see to our most IMPREGNABLE defense! |
| 0x2a86e5 | 19 | Milady Munechika... |
| 0x2a86f9 | 12 | Let us move. |
| 0x2a8706 | 15 | And so they go. |
| 0x2a8716 | 49 | It seems the swine seeks to make more hindrance\n |
| 0x2a8748 | 34 | than help of himself to Munechika. |
| 0x2a876b | 32 | And you are all right with that? |
| 0x2a878c | 39 | Should I not be? It hardly demands my\n |
| 0x2a87b4 | 13 | interference. |
| 0x2a87c2 | 49 | The filth is exceptionally crafty in matters of\n |
| 0x2a87f4 | 47 | subterfuge. He would be a fine general, if he\n |
| 0x2a8824 | 10 | desired... |
| 0x2a882f | 46 | ...But instead he seeks to tighten the noose\n |
| 0x2a885e | 32 | around his own neck. What folly. |
| 0x2a887f | 41 | "Craft brings nothing home" is a phrase\n |
| 0x2a88a9 | 31 | applicable to fools such as he. |
| 0x2a88c9 | 43 | He satisfies his immediate desires at the\n |
| 0x2a88f5 | 47 | exclusion of all else. Even children know not\n |
| 0x2a8925 | 14 | to indulge so. |
| 0x2a8934 | 46 | But Munechika...in all her naivete, may have\n |
| 0x2a8963 | 30 | only made the situation worse. |
| 0x2a8982 | 41 | Lady Munechika? I wouldn't think her so\n |
| 0x2a89ac | 47 | oblivious as to fall for a trap laid by a man\n |
| 0x2a89dc | 9 | like him. |
| 0x2a89e6 | 4 | Heh. |
| 0x2a89eb | 11 | Lord Raiko? |
| 0x2a89f7 | 47 | Then keep watching. You may yet see something\n |
| 0x2a8a27 | 29 | interesting come of this war. |
| 0x2a8a45 | 46 | Fan it more! We need the hot air to fill the\n |
| 0x2a8a74 | 9 | cloth up. |
| 0x2a8a7e | 9 | G-Got it! |
| 0x2a8a88 | 30 | You may leave it in our hands. |
| 0x2a8aa7 | 44 | We've returned to the bottom of the cliff,\n |
| 0x2a8ad4 | 45 | where we immediately lit a fire beneath the\n |
| 0x2a8b02 | 8 | balloon. |
| 0x2a8b0b | 46 | Wouldja look at that. It's really fillin' out. |
| 0x2a8b3a | 6 | Wow... |
| 0x2a8b41 | 10 | Amazing... |
| 0x2a8b4c | 24 | It really is floating... |
| 0x2a8b65 | 42 | Indeed. It seems my sacrifice of falling\n |
| 0x2a8b90 | 41 | headfirst into the ground was no waste,\n |
| 0x2a8bba | 10 | after all. |
| 0x2a8bc5 | 44 | Things look like they're coming along much\n |
| 0x2a8bf2 | 29 | better than I'd hoped, but... |
| 0x2a8c10 | 25 | I look over at the twins. |
| 0x2a8c2a | 31 | Don't push yourselves too hard. |
| 0x2a8c4a | 12 | We are fine. |
| 0x2a8c57 | 39 | The barrier is... No, pay it no mind.\n |
| 0x2a8c7f | 19 | This is no problem. |
| 0x2a8c93 | 46 | The two of them have been using their powers\n |
| 0x2a8cc2 | 47 | to stoke the flame enough to make the balloon\n |
| 0x2a8cf2 | 6 | float. |
| 0x2a8cf9 | 9 | Whooaa... |
| 0x2a8d03 | 33 | Do you think this will be enough? |
| 0x2a8d25 | 43 | I would never have imagined this to work.\n |
| 0x2a8d51 | 39 | As a theory, perhaps, but in reality... |
| 0x2a8d79 | 33 | No, we need more! To the skies,\n |
| 0x2a8d9b | 28 | Loincloth Force One! Onward! |
| 0x2a8db8 | 34 | Gah!? Why are you all kicking me!? |
| 0x2a8ddb | 43 | Why don't you look deep inside your heart\n |
| 0x2a8e07 | 22 | and ask yourself that? |
| 0x2a8e1e | 45 | I-I don't think my heart's going to tell me\n |
| 0x2a8e4c | 9 | anything. |
| 0x2a8e56 | 31 | You never change, do you, Haku? |
| 0x2a8e76 | 43 | Seems the attack on the fortress has begun. |
| 0x2a8ea2 | 23 | Ougi, how does it look? |
| 0x2a8eba | 45 | Lady Munechika never ceases to amaze. She's\n |
| 0x2a8ee8 | 34 | quite handily drawn off the enemy. |
| 0x2a8f0b | 46 | All right, then. Everyone go when I give the\n |
| 0x2a8f3a | 7 | signal. |
| 0x2a8f42 | 16 | You ready, Kuon? |
| 0x2a8f53 | 17 | Whenever you are. |
| 0x2a8f65 | 30 | ...Good. She seems to be fine. |
| 0x2a8f84 | 27 | All right. Untie the ropes. |
| 0x2a8fa0 | 11 | You got it! |
| 0x2a8fac | 10 | We ascend. |
| 0x2a8fb7 | 43 | We have achieved enough lift to take off,\n |
| 0x2a8fe3 | 7 | Master. |
| 0x2a8feb | 46 | With a thunk and a shake, the basket holding\n |
| 0x2a901a | 24 | us all begins to rise... |
| 0x2a9033 | 48 | Ahahaha, I'll bet they were never expecting us\n |
| 0x2a9064 | 48 | to FLY up the cliff. I can't wait to see their\n |
| 0x2a9095 | 6 | faces. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_11.json` com a forma:
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
