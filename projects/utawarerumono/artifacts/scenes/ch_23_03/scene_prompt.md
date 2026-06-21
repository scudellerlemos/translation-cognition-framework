# Cena ch_23_03 — pacote de traducao (161 linhas)

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
| Bokoinante | Personagem | Bokoinante | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Raiko | Personagem | Raiko | manter_original | none |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `spirits.` -> `espíritos.` (Garota, 16_02)
- `Generals.` -> `Generais.` (Haku, 18_01)
- `caution.` -> `precaução.` (Haku, 19_08)
- `Munechika.` -> `Munechika.` (Narração, 23_02)
- `responsibilities.` -> `responsabilidades.` (Oshtor, 19_08)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `to.` -> `a.` (Protagonista, 19_08)
- `Messenger` -> `MENSAGEIRO` (MESSENGER, 20_01)
- `Reporting!` -> `Relatando!` (SOLDIER, 20_01)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `army.` -> `exército.` (Homem, 22_08)
- `Miss Munechika...` -> `Senhorita Munechika...` (Haku(?) ou Nosuri, 23_02)
- `then.` -> `então.` (Kuon, 13_01)
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
| 0x279e7a | 47 | As the Yamatans set foot on Tuskur soil, they\n |
| 0x279eaa | 41 | occupy the coast and set up a port as a\n |
| 0x279ed4 | 18 | military foothold. |
| 0x279ee7 | 48 | A great road leads inland from the shoreline--\n |
| 0x279f18 | 41 | an essential tool for transporting goods. |
| 0x279f42 | 46 | The road leads directly to the very heart of\n |
| 0x279f71 | 7 | Tuskur. |
| 0x279f79 | 48 | And so Yamato's invasion of the land of Tuskur\n |
| 0x279faa | 7 | begins. |
| 0x279fb2 | 47 | Tuskur, caught completely unawares, is forced\n |
| 0x279fe2 | 31 | to take quick defensive action. |
| 0x27a002 | 49 | Soldiers are stationed at points throughout the\n |
| 0x27a034 | 44 | road, but they are unable to halt Yamato's\n |
| 0x27a061 | 15 | advance inland. |
| 0x27a071 | 49 | Soon, the Yamatan army succeeds in establishing\n |
| 0x27a0a3 | 43 | a fort along the road; a headquarters for\n |
| 0x27a0cf | 16 | invasion forces. |
| 0x27a0e0 | 46 | That night, the three commanders--Dekopompo,\n |
| 0x27a10f | 45 | Munechika, and Raiko--hold a meeting within\n |
| 0x27a13d | 13 | the fortress. |
| 0x27a14b | 42 | The only other members present are their\n |
| 0x27a176 | 33 | retainers, who stand in the back. |
| 0x27a198 | 49 | All the other soldiers rejoice in their victory\n |
| 0x27a1ca | 48 | by the large central bonfire with food, drink,\n |
| 0x27a1fb | 9 | and song. |
| 0x27a205 | 46 | From time to time, the generals can hear the\n |
| 0x27a234 | 39 | soldiers' raucous laughter on the wind. |
| 0x27a25c | 47 | Their easy victories so far have buoyed their\n |
| 0x27a28c | 8 | spirits. |
| 0x27a295 | 45 | We are advancing swiftly, without question!\n |
| 0x27a2c3 | 40 | I would expect no less from the Pillar\n |
| 0x27a2ec | 9 | Generals. |
| 0x27a2f6 | 44 | It seems we have little to fear from Tuskur. |
| 0x27a323 | 48 | Nyuh huh huh huh. So much for this "land where\n |
| 0x27a354 | 48 | god sleeps"... They're just a backwater little\n |
| 0x27a385 | 7 | island! |
| 0x27a38d | 42 | They pose no more of a threat than those\n |
| 0x27a3b8 | 21 | Uzurushan barbarians. |
| 0x27a3ce | 23 | Well... P-Perhaps so... |
| 0x27a3e6 | 48 | We shall continue to ride this wave of triumph\n |
| 0x27a417 | 40 | all the way to the very heart of Tuskur! |
| 0x27a440 | 34 | Ah! Outstanding, Lord Dekopompo!\n |
| 0x27a463 | 28 | What great insight you have! |
| 0x27a480 | 39 | Of course I do. Here, you drink up too! |
| 0x27a4a8 | 27 | Ah, thank you so much, sir! |
| 0x27a4c4 | 46 | You treat this with far too much carelessness. |
| 0x27a4f3 | 44 | We still know very little about this land.\n |
| 0x27a520 | 43 | What is more, they still have the terrain\n |
| 0x27a54c | 10 | advantage. |
| 0x27a557 | 49 | If we rush heedlessly in, we may find the enemy\n |
| 0x27a589 | 42 | eager to welcome us with heavy casualties. |
| 0x27a5b4 | 46 | It is my opinion that we should proceed with\n |
| 0x27a5e3 | 8 | caution. |
| 0x27a5ec | 50 | Well, well, well. Sounds to me like the strategy\n |
| 0x27a61f | 12 | of a coward. |
| 0x27a62c | 50 | I hardly believe such words come from one of the\n |
| 0x27a65f | 40 | proud Eight Pillar Generals of Yamato,\n |
| 0x27a688 | 10 | Munechika. |
| 0x27a693 | 47 | Being wary is all fine and good, but we shall\n |
| 0x27a6c3 | 45 | never seize victory if we withdraw into our\n |
| 0x27a6f1 | 7 | shells! |
| 0x27a6fd | 45 | Anyhow, why don't we ask the opinion of our\n |
| 0x27a72b | 20 | marshal, Lord Raiko? |
| 0x27a740 | 33 | Munechika presents a valid point. |
| 0x27a762 | 49 | A general must never underestimate their enemy,\n |
| 0x27a794 | 32 | regardless of the circumstances. |
| 0x27a7b5 | 9 | Nyegh...? |
| 0x27a7bf | 45 | Yet allowing caution in excess to slow down\n |
| 0x27a7ed | 43 | our forces would also be a foolish mistake. |
| 0x27a819 | 50 | Whether it is a trap or not, I am sure that with\n |
| 0x27a84c | 45 | Dekopompo's valor, we may triumph over such\n |
| 0x27a87a | 10 | obstacles. |
| 0x27a885 | 18 | Yes! Yes, exactly! |
| 0x27a898 | 48 | Just as I expected, Raiko, it seems you have a\n |
| 0x27a8c9 | 35 | solid grasp of the greater picture! |
| 0x27a8ed | 9 | Even so-- |
| 0x27a8f7 | 47 | Munechika, I am the one appointed marshal for\n |
| 0x27a927 | 41 | this expedition. I am fully aware of my\n |
| 0x27a951 | 17 | responsibilities. |
| 0x27a963 | 49 | No doubt you have your own opinion on this, but\n |
| 0x27a995 | 39 | I will have you obey my decisions here. |
| 0x27a9bd | 11 | Understood. |
| 0x27a9c9 | 50 | Nyoo hoo hoo! Then if you will excuse me, I have\n |
| 0x27a9fc | 47 | much to prepare for. Bokoinante, Maroro, we go! |
| 0x27aa2c | 14 | A-Aye, master. |
| 0x27aa3b | 35 | I will excuse myself as well, then. |
| 0x27aa5f | 30 | ...Are you certain about this? |
| 0x27aa7e | 44 | I believe Lady Munechika may be correct in\n |
| 0x27aaab | 46 | thinking that the enemy is preparing a trap... |
| 0x27aada | 18 | It hardly matters. |
| 0x27aaed | 49 | I am getting rather sick and tired of having to\n |
| 0x27ab1f | 30 | see that swine's bloated face. |
| 0x27ab3e | 45 | If he aims to jump into the flames himself,\n |
| 0x27ab6c | 44 | all the more convenient for me. He is more\n |
| 0x27ab99 | 16 | than welcome to. |
| 0x27abaa | 48 | Of course, regardless of how well the swine is\n |
| 0x27abdb | 40 | roasted, I doubt anyone would find him\n |
| 0x27ac04 | 11 | appetizing. |
| 0x27ac10 | 36 | Haha... A cold assessment, milord... |
| 0x27ac35 | 7 | Also... |
| 0x27ac3d | 5 | Also? |
| 0x27ac43 | 49 | If I play my hand correctly, I may even be able\n |
| 0x27ac75 | 42 | to rid myself of that bothersome guardian. |
| 0x27aca0 | 9 | ...I see. |
| 0x27acaa | 45 | In truth, Munechika's fears are well-founded. |
| 0x27acd8 | 48 | The Yamatan fortress had been set up precisely\n |
| 0x27ad09 | 48 | where the Tuskur army had cleverly guided them\n |
| 0x27ad3a | 3 | to. |
| 0x27ad3e | 9 | Messenger |
| 0x27ad48 | 10 | Reporting! |
| 0x27ad53 | 49 | We have lost contact with units one, three, and\n |
| 0x27ad85 | 5 | four! |
| 0x27ad8b | 8 | Nyargh!? |
| 0x27ad94 | 47 | We've also received reports that unit two has\n |
| 0x27adc4 | 47 | been ambushed from the rear. Major casualties\n |
| 0x27adf4 | 10 | sustained! |
| 0x27adff | 39 | From the rear!? Wh-What is going on!?\n |
| 0x27ae27 | 44 | Bokoinante! Where is the enemy coming from!? |
| 0x27ae54 | 42 | I-I am not sure what is going on either... |
| 0x27ae7f | 49 | Throughout the mountains is a network of hidden\n |
| 0x27aeb1 | 42 | pathways, utterly unknown to the Yamatans. |
| 0x27aedc | 50 | The Tuskur soldiers use these paths to go around\n |
| 0x27af0f | 48 | the Yamatan army, making their fortress useless. |
| 0x27af40 | 22 | And, on top of that... |
| 0x27af57 | 18 | O unhappy fortune! |
| 0x27af6a | 47 | The supply units bound from our landing point\n |
| 0x27af9a | 37 | have been set upon by enemy forces... |
| 0x27afc0 | 6 | WHAT!? |
| 0x27afc7 | 45 | There is only one traversable road from the\n |
| 0x27aff5 | 22 | shore to the fortress. |
| 0x27b00c | 50 | Every Yamatan supply unit heading by road to the\n |
| 0x27b03f | 47 | fortress is soon attacked, and their supplies\n |
| 0x27b06f | 6 | taken. |
| 0x27b076 | 41 | So it has come to this... just as I had\n |
| 0x27b0a0 | 9 | expected. |
| 0x27b0aa | 49 | We can neither take the offensive, nor retreat.\n |
| 0x27b0dc | 49 | We are completely isolated from the rest of the\n |
| 0x27b10e | 5 | army. |
| 0x27b114 | 44 | We have yet to clash head-on, but if these\n |
| 0x27b141 | 50 | skirmishes continue, our forces will be whittled\n |
| 0x27b174 | 7 | down... |
| 0x27b17c | 49 | But who could have foreseen such difficulty...?\n |
| 0x27b1ae | 37 | No... perhaps this is what she meant. |
| 0x27b1d4 | 17 | Miss Munechika... |
| 0x27b1e6 | 45 | Is there no way that the invasion of Tuskur\n |
| 0x27b214 | 15 | can be stopped? |
| 0x27b224 | 44 | I am afraid it is impossible. If our liege\n |
| 0x27b251 | 45 | commands it, we are duty-bound to carry out\n |
| 0x27b27f | 9 | his will. |
| 0x27b289 | 44 | But many people will die if this war begins. |
| 0x27b2b6 | 47 | Ah, yes... You have relations in Tuskur, if I\n |
| 0x27b2e6 | 44 | recall. I am sorry, but I have no power to\n |
| 0x27b313 | 12 | change this. |
| 0x27b320 | 50 | I see... I suppose there's not much left to say,\n |
| 0x27b353 | 5 | then. |
| 0x27b359 | 20 | Please be careful.\n |
| 0x27b36e | 17 | Come home safe... |
| 0x27b380 | 48 | Perhaps... this entire invasion was a mistake... |
| 0x27b3b1 | 47 | No... I cannot afford to let my resolve waver\n |
| 0x27b3e1 | 41 | now. I must find a way out of this dire\n |
| 0x27b40b | 12 | situation... |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_03.json` com a forma:
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
