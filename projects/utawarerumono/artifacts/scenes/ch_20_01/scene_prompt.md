# Cena ch_20_01 — pacote de traducao (166 linhas)

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
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Man | UI | Homem | traduzir | none |
| Maruruha | Local | Maruruha | manter_original | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `command.` -> `ordem.` (Maroro, 18_01)
- `imperial capital.` -> `capital imperial.` (Haku, 18_01)
- `them!` -> `deles!` (Haku, 15_01)
- `place.` -> `lugar.` (Protagonista, 16_01)
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
| 0x1aeaa5 | 47 | From what information we have, it may be safe\n |
| 0x1aead5 | 39 | to assume that Maruruha has fallen...\n |
| 0x1aeafd | 17 | Most regrettable. |
| 0x1aeb0f | 50 | That concludes our report on the situation as it\n |
| 0x1aeb42 | 44 | stands. Now, we begin the emergency council. |
| 0x1aeb6f | 48 | My liege, we could not gather all Eight Pillar\n |
| 0x1aeba0 | 43 | Generals on such short notice. I beg your\n |
| 0x1aebcc | 14 | forgiveness... |
| 0x1aebdb | 44 | You have my pardon. Thank you all for your\n |
| 0x1aec08 | 24 | haste and understanding. |
| 0x1aec21 | 40 | The Mikado looks down from his throne,\n |
| 0x1aec4a | 31 | surveying all those before him. |
| 0x1aec6a | 38 | So... Maruruha has fallen to Uzurusha. |
| 0x1aec91 | 45 | If all proceeds as predicted, Uzurusha will\n |
| 0x1aecbf | 48 | doubtlessly progress onward with their invasion. |
| 0x1aecf0 | 47 | They are extremely well-supplied. I am led to\n |
| 0x1aed20 | 45 | believe that they have a vast army at their\n |
| 0x1aed4e | 8 | command. |
| 0x1aed57 | 50 | It seems we have been ensnared by the very roads\n |
| 0x1aed8a | 11 | we built... |
| 0x1aed96 | 50 | Yamato's roads are its veins, its lifeblood, and\n |
| 0x1aedc9 | 49 | its prosperity... My liege, you must not despair. |
| 0x1aedfb | 9 | Indeed... |
| 0x1aee05 | 45 | The Mikado answers with curious detachment,\n |
| 0x1aee33 | 41 | looking off into the distance as though\n |
| 0x1aee5d | 11 | distracted. |
| 0x1aee69 | 50 | Uzurusha... Formerly a loose territory of around\n |
| 0x1aee9c | 37 | a hundred tribes; not truly a nation. |
| 0x1aeec2 | 50 | This was because the majority of the tribes were\n |
| 0x1aeef5 | 43 | nomads, traveling in search of arable land. |
| 0x1aef21 | 47 | However, the arid climate of Uzurusha did not\n |
| 0x1aef51 | 30 | provide for much fertile soil. |
| 0x1aef70 | 43 | The tribes often warred among themselves,\n |
| 0x1aef9c | 47 | battling to control what little land could be\n |
| 0x1aefcc | 11 | cultivated. |
| 0x1aefd8 | 51 | Burdened with famine and poverty, they longed for\n |
| 0x1af00c | 47 | the lush soils of Yamato--soil they needed in\n |
| 0x1af03c | 17 | order to survive. |
| 0x1af04e | 52 | At times, raiding parties would pillage the people\n |
| 0x1af083 | 46 | of Yamato, who grew to see them as barbarians. |
| 0x1af0b2 | 52 | Despite the raids... There were very few instances\n |
| 0x1af0e7 | 47 | in which the Uzurushans clashed with Yamato's\n |
| 0x1af117 | 9 | military. |
| 0x1af121 | 45 | Their primary goal was to obtain resources.\n |
| 0x1af14f | 47 | They would only raid storehouses, or take the\n |
| 0x1af17f | 26 | Yamatans' harvested crops. |
| 0x1af19a | 45 | The Uzurushans knew they would stand little\n |
| 0x1af1c8 | 48 | chance if they drew the full brunt of Yamato's\n |
| 0x1af1f9 | 4 | ire. |
| 0x1af1fe | 42 | However, with the appearance of one man,\n |
| 0x1af229 | 33 | the situation changed completely. |
| 0x1af24b | 48 | Gundhurua... a man who united over one hundred\n |
| 0x1af27c | 41 | tribes to create a mighty nation in one\n |
| 0x1af2a6 | 11 | generation. |
| 0x1af2b2 | 51 | After unifying the Uzurushans, he set his gaze on\n |
| 0x1af2e6 | 48 | invading surrounding nations... And now, Yamato. |
| 0x1af317 | 51 | Though not as prosperous, with an army of veteran\n |
| 0x1af34b | 49 | warriors, their forces vastly outnumber Yamato's. |
| 0x1af37d | 46 | Because most of Uzurusha's bordering nations\n |
| 0x1af3ac | 40 | were not expecting a full-on invasion... |
| 0x1af3d5 | 45 | ...they fell one by one, unable to muster a\n |
| 0x1af403 | 20 | retaliation in time. |
| 0x1af418 | 49 | Although Yamato drove them back, the Uzurushans\n |
| 0x1af44a | 45 | savored their brief victory. Their assaults\n |
| 0x1af478 | 34 | continued, their ferocity renewed. |
| 0x1af49b | 49 | And the lands they took became wastelands, with\n |
| 0x1af4cd | 25 | no hope of restoration... |
| 0x1af4e7 | 44 | Gundhurua... The so-called 'great man' who\n |
| 0x1af514 | 47 | unified the barbarians and raised Uzurusha to\n |
| 0x1af544 | 11 | nationhood. |
| 0x1af550 | 20 | But... he is a fool. |
| 0x1af565 | 48 | To bare fangs against Yamato... Such audacity.\n |
| 0x1af596 | 43 | Does he truly think he stands a chance at\n |
| 0x1af5c2 | 8 | victory? |
| 0x1af5cb | 50 | If he aims to be our jester, then let us indulge\n |
| 0x1af5fe | 14 | him and laugh. |
| 0x1af60d | 43 | Such disregard is unlike you, Lord Raiko.\n |
| 0x1af639 | 46 | Underestimation of their ability may be your\n |
| 0x1af668 | 9 | downfall. |
| 0x1af672 | 49 | Humbling indeed, that I should be admonished by\n |
| 0x1af6a4 | 49 | you. Perhaps I must reconsider my expectations... |
| 0x1af6d6 | 42 | Your words of caution are, I assure you,\n |
| 0x1af701 | 11 | duly noted. |
| 0x1af70d | 13 | Ha... Hahaha. |
| 0x1af71b | 40 | The Uzurushan army is showing signs of\n |
| 0x1af744 | 43 | organization, as is their chain of command. |
| 0x1af770 | 48 | Rather than relying on sheer force of numbers,\n |
| 0x1af7a1 | 48 | it would seem they are employing sophisticated\n |
| 0x1af7d2 | 21 | tactics and strategy. |
| 0x1af7e8 | 21 | Strategy, you say...? |
| 0x1af7fe | 45 | The Mikado faintly smiles, as though he has\n |
| 0x1af82c | 29 | just heard something amusing. |
| 0x1af84a | 21 | ...What a cold smile. |
| 0x1af860 | 46 | Through every defense of the capital, I have\n |
| 0x1af88f | 37 | taken control of countless battles... |
| 0x1af8b5 | 46 | And for my merits, I am now one of the Eight\n |
| 0x1af8e4 | 43 | Pillar Generals, known as Guardian of the\n |
| 0x1af910 | 17 | Imperial Capital. |
| 0x1af922 | 51 | Yet not once before have I seen my liege smile so\n |
| 0x1af956 | 18 | when facing war... |
| 0x1af969 | 50 | The plight of his suffering people must fill him\n |
| 0x1af99c | 10 | with rage. |
| 0x1af9a7 | 46 | The fault is mine, for letting the situation\n |
| 0x1af9d6 | 44 | escalate to push my liege to such emotion.\n |
| 0x1afa03 | 13 | Such shame... |
| 0x1afa11 | 7 | Soldier |
| 0x1afa19 | 10 | Reporting! |
| 0x1afa24 | 42 | What is the meaning of this disruption!?\n |
| 0x1afa4f | 37 | You are in the presence of our liege! |
| 0x1afa75 | 9 | Messenger |
| 0x1afa7f | 47 | This is an urgent matter! The Uzurushans have\n |
| 0x1afaaf | 44 | crossed the border and begun their invasion! |
| 0x1afadc | 36 | What? Where was the defense force?\n |
| 0x1afb01 | 48 | I thought we stationed enough troops to handle\n |
| 0x1afb32 | 5 | them! |
| 0x1afb38 | 49 | Sir, the defenders could not counter an assault\n |
| 0x1afb6a | 46 | from all major roads! They remain under siege! |
| 0x1afb99 | 39 | They're coming from all major roads...? |
| 0x1afbc1 | 50 | I have heard they take hostages, and force their\n |
| 0x1afbf4 | 45 | families to fight for them... as expendable\n |
| 0x1afc22 | 9 | soldiers. |
| 0x1afc30 | 47 | I had thought that they had learned to behave\n |
| 0x1afc60 | 13 | themselves... |
| 0x1afc6e | 48 | But it appears... they have yet to learn their\n |
| 0x1afc9f | 6 | place. |
| 0x1afca6 | 38 | The Mikado mutters, pity in his voice. |
| 0x1afccd | 48 | It seems this owlo of barbarians does not know\n |
| 0x1afcfe | 48 | Yamato's true power. Perhaps pride can drive a\n |
| 0x1afd2f | 8 | man mad. |
| 0x1afd38 | 42 | Ah, my liege. Please, give me your orders! |
| 0x1afd63 | 50 | I promise you, your graciousness, the barbarians\n |
| 0x1afd96 | 40 | will crumple before my genius and might. |
| 0x1afdbf | 10 | Be silent. |
| 0x1afdca | 8 | Nyeh...? |
| 0x1afdd3 | 49 | Wha--Wh--Wh--Wh... How dare you talk to me like\n |
| 0x1afe05 | 26 | that! Who do you think I-- |
| 0x1afe20 | 27 | I will not repeat myself.\n |
| 0x1afe3c | 22 | Close your foul mouth. |
| 0x1afe53 | 16 | Nyeh... p-peh... |
| 0x1afe64 | 37 | Great Mikado, we await your orders.\n |
| 0x1afe8a | 41 | You need but give the word, and we will\n |
| 0x1afeb4 | 25 | eliminate all opposition. |
| 0x1afece | 27 | That will not be necessary. |
| 0x1afeea | 39 | Tell the owlo of the barbarians this.\n |
| 0x1aff12 | 50 | If he offers me his own head, I shall show mercy\n |
| 0x1aff45 | 14 | to his people. |
| 0x1aff54 | 51 | And if he should refuse your benevolent proposal,\n |
| 0x1aff88 | 9 | my liege? |
| 0x1aff92 | 49 | I am not a ruler without mercy. But I am not so\n |
| 0x1affc4 | 45 | indulgent as to let such folly go unpunished. |
| 0x1afff2 | 49 | Those that refuse to learn must be made to learn. |
| 0x1b0024 | 44 | I give you permission to unleash your power. |
| 0x1b0051 | 50 | Destroy them. Let all witness the price of their\n |
| 0x1b0084 | 10 | ignorance. |
| 0x1b008f | 48 | All in the room bow their head at the Mikado's\n |
| 0x1b00c0 | 18 | cold proclamation. |
| 0x1b00d3 | 51 | Outright extermination... I confess, the prospect\n |
| 0x1b0107 | 19 | brings me unease... |
| 0x1b011b | 48 | That is the will of our liege. We must destroy\n |
| 0x1b014c | 33 | all who bring harm to our nation. |
| 0x1b016e | 48 | Well, at least this should keep me entertained\n |
| 0x1b019f | 14 | for a while... |
| 0x1b01ae | 46 | With permission to release their powers, the\n |
| 0x1b01dd | 49 | other Eight Pillar Generals seem keen for battle. |
| 0x1b020f | 50 | I will need Haku and the others' help to keep us\n |
| 0x1b0242 | 37 | from suffering innocent casualties... |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_01.json` com a forma:
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
