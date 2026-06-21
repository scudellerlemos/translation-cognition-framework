# Cena ch_20_11 — pacote de traducao (101 linhas)

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
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Magecraft | Conceito | Magia | traduzir | none |
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Uzurushan commander` -> `comandante Uzurushan` (SISTEMA, 20_05)
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `back.` -> `voltei.` (Haku, 18_01)
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
| 0x1dd9de | 19 | Uzurushan commander |
| 0x1dd9f2 | 45 | Hah. Look at those worms holing up in their\n |
| 0x1dda20 | 12 | little nest. |
| 0x1dda2d | 49 | Taking the high ground, though... Devious rats.\n |
| 0x1dda5f | 41 | They are tenacious; I'll grant them that. |
| 0x1dda89 | 40 | You are one to talk. Sitting here just\n |
| 0x1ddab2 | 47 | intimidating them, instead of assaulting them\n |
| 0x1ddae2 | 10 | head-on... |
| 0x1ddaed | 47 | That said, should we be wasting time here so?\n |
| 0x1ddb1d | 44 | Would not our owlo be angered by our delays? |
| 0x1ddb4a | 43 | Hm. Our owlo would not be angered by such\n |
| 0x1ddb76 | 44 | trifles. We would be fools to rush matters\n |
| 0x1ddba3 | 18 | for our own glory. |
| 0x1ddbb6 | 43 | All we must do is wait for reinforcements\n |
| 0x1ddbe2 | 46 | to arrive, then crush them with sheer numbers. |
| 0x1ddc11 | 51 | True. This close to their capital, and with their\n |
| 0x1ddc45 | 47 | full numbers unknown, they may yet surprise us. |
| 0x1ddc75 | 50 | Yamato's numbers are limited. By the look of the\n |
| 0x1ddca8 | 43 | field, they could position at most twenty\n |
| 0x1ddcd4 | 11 | thousand... |
| 0x1ddce0 | 47 | And our reinforcements will be forty thousand\n |
| 0x1ddd10 | 11 | soldiers... |
| 0x1ddd1c | 50 | We shall twice outnumber them. Unless they would\n |
| 0x1ddd4f | 47 | defy all military sense, victory is guaranteed. |
| 0x1ddd7f | 21 | *Stomp, stomp, stomp* |
| 0x1ddd95 | 21 | Ah!? The land shakes! |
| 0x1dddab | 27 | This sound... They're here! |
| 0x1dddc7 | 47 | Ah! The elite soldiers of Lord Gundhurua have\n |
| 0x1dddf7 | 35 | arrived. The time has finally come! |
| 0x1dde1b | 48 | What majesty... So this is the owlo's personal\n |
| 0x1dde4c | 7 | army... |
| 0x1dde54 | 48 | Haha... Hahahahahaha! With this grand a force,\n |
| 0x1dde85 | 43 | that pathetic Yamatan fort is sure to fall. |
| 0x1ddeb1 | 46 | Indeed! We shall trample all who oppose us--\n |
| 0x1ddee0 | 29 | all the way to their capital! |
| 0x1ddefe | 46 | Your resistance has proved admirable indeed!\n |
| 0x1ddf2d | 46 | Surrender now, and our owlo may yet show you\n |
| 0x1ddf5c | 30 | mercy and accept your service! |
| 0x1ddf7b | 44 | I have no intention to serve another lord.\n |
| 0x1ddfa8 | 47 | My sole duty is to protect the people of this\n |
| 0x1ddfd8 | 5 | land. |
| 0x1ddfde | 48 | ...A pity that your duty shall go unfulfilled.\n |
| 0x1de00f | 42 | But I shall grant your life beauty in an\n |
| 0x1de03a | 16 | honorable death! |
| 0x1de04b | 36 | Crush them, like the worms they are! |
| 0x1de070 | 17 | Uzurushan soldier |
| 0x1de082 | 18 | Raaaaaaaaaaaaaah!! |
| 0x1de095 | 34 | I have never seen beauty in death. |
| 0x1de0b8 | 39 | Then we will crush you where you stand! |
| 0x1de0e0 | 31 | Thou shalt trespass no farther. |
| 0x1de100 | 7 | Nghah!? |
| 0x1de108 | 46 | Everything beyond this point is now under my\n |
| 0x1de137 | 45 | control. If you wish to live, you will turn\n |
| 0x1de165 | 5 | back. |
| 0x1de16b | 41 | Wh-What!? Why can't we move forward...?\n |
| 0x1de195 | 17 | What's going on!? |
| 0x1de1a7 | 36 | What is wrong? Why do you falter!?\n |
| 0x1de1cc | 46 | A single woman is all that stands before us!\n |
| 0x1de1fb | 17 | March! Crush her! |
| 0x1de20d | 26 | I will grant you no mercy. |
| 0x1de228 | 41 | Gah... W-Wait...! S-Stop pushing forward! |
| 0x1de252 | 49 | Wh-What trickery is this? Is this magecraft...?\n |
| 0x1de284 | 41 | Rrgh--Soldiers! Cease the attack at once! |
| 0x1de2ae | 27 | Soldiers. One step forward. |
| 0x1de2ca | 26 | What... What is this...?\n |
| 0x1de2e5 | 24 | Can this be possible...? |
| 0x1de2fe | 38 | Impossible... We need to regroup. Now! |
| 0x1de325 | 28 | Soldiers. Two steps forward. |
| 0x1de342 | 30 | Wh... What is... going on...!? |
| 0x1de361 | 22 | No... This can't be... |
| 0x1de378 | 42 | For the salvation of those at my back...\n |
| 0x1de3a3 | 44 | For the destruction of those I confront...\n |
| 0x1de3d0 | 32 | No longer am I woman, but demon. |
| 0x1de3f1 | 20 | Soldiers... forward. |
| 0x1de406 | 50 | How is this even possible!? Soldiers, fall back!\n |
| 0x1de439 | 10 | Fall back! |
| 0x1de444 | 47 | Wait--we cannot fall back! The heavy infantry\n |
| 0x1de474 | 24 | behind us block the way! |
| 0x1de48d | 42 | Rrgh... What do you think you're doing!?\n |
| 0x1de4b8 | 39 | Those who dare retreat will be slain!\n |
| 0x1de4e0 | 24 | Heavy infantry, forward! |
| 0x1de4f9 | 46 | Impossible... Impossible...! This is absurd!\n |
| 0x1de528 | 26 | I will not stand for this! |
| 0x1de543 | 43 | You have gravely misjudged your opponent.\n |
| 0x1de56f | 48 | You have dared touch that which you should not\n |
| 0x1de5a0 | 14 | have awakened. |
| 0x1de5af | 46 | If you have forgotten the terror of opposing\n |
| 0x1de5de | 50 | Yamato, then allow me to carve it into your very\n |
| 0x1de611 | 5 | soul. |
| 0x1de617 | 22 | This is... impossible! |
| 0x1de62e | 38 | I have been given imperial orders...\n |
| 0x1de655 | 23 | to exterminate you all. |
| 0x1de66d | 32 | Ha... Haha... Ahahahahahaha...\n |
| 0x1de68e | 13 | GYAAAAAARRGH! |
| 0x1de69c | 13 | ch400_00_base |
| 0x1de6ab | 14 | ch400_00_wheel |
| 0x1de6ba | 7 | LeftLeg |
| 0x1de6c2 | 6 | target |
| 0x1de6c9 | 5 | kamen |
| 0x1de6cf | 9 | billboard |
| 0x1de6d9 | 9 | GlobalSRT |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_11.json` com a forma:
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
