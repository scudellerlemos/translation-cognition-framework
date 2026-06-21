# Cena ch_11_01 — pacote de traducao (468 linhas)

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
| Awakening Process | Conceito | Processo de Despertar | traduzir | moderate |
| Girl | UI | Garota | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Uncle | Cultural | Tio | traduzir | none |
| Woman | UI | Mulher | traduzir | none |

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
- **Anomalia 0x33f9 — reclassificada (binário-fonte está íntegro)**: **Decisão tomada:** Reclassificar: o binário-fonte **não está corrompido**. A extração limpa do arco mostra em `0x33f9` o texto inglês íntegro **"INITIALIZING AWAKENING PROCESS."** (31 bytes) e, separada, `0x3419` **"SYSTEMS YELLOW. RESTARTING IN 5 SECONDS."** (40 bytes).
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)
- **Processo de Despertar** (moderate): Mantenha o enquadramento ambiguo e tecnico (CAPS p/ Sistema). NAO explique a natureza sci-fi nem conecte ao enredo maior. (Obs.: 'system of gears'/engrenagens do moinho NAO e isto.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Ngh... ghh...` -> `Nnh... aagh...` (Protagonista, root)
- `Nn...` -> `Nnh...` (Haku, 17_01)
- `It's... warm...?` -> `Está... quente...?` (Protagonista, root)
- `Nh?` -> `Hein?` (Protagonista, root)
- `Wh-Who...` -> `Q-Quem...` (Protagonista, root)
- `...calls... to me...?` -> `...me chama...?` (Protagonista, root)
- `Wait... I'm still...!` -> `Espera... eu ainda...!` (Protagonista, root)
- `INITIALIZING AWAKENING PROCESS.` -> `INICIANDO PROCESSO DE DESPERTAR.` (Sistema, root)
- `SYSTEMS YELLOW. RESTARTING IN 5 SECONDS.` -> `SISTEMAS EM ALERTA. REINICIANDO EM 5 SEGUNDOS.` (Sistema, root)
- `SYSTEM ERROR.` -> `ERRO DE SISTEMA.` (Sistema, root)
- `PROBLEM DETECTED IN AWAKENING PROCESS.\n` -> `PROBLEMA DETECTADO NO PROCESSO DE DESPERTAR.\n` (Sistema, root)
- `SUBJECT SEVERELY AFFECTED.` -> `SUJEITO GRAVEMENTE AFETADO.` (Sistema, root)
- `ABORT COMMAND: CANCELLED. \n` -> `COMANDO DE ABORTAR: CANCELADO. \n` (Sistema, root)
- `PROCESS UNABLE TO BE TERMINATED.\n` -> `IMPOSSÍVEL ENCERRAR O PROCESSO.\n` (Sistema, root)
- `COMMENCING COUNTDOWN.` -> `INICIANDO CONTAGEM REGRESSIVA.` (Sistema, root)
- `5, {W75}4, {W75}3, {W80}2, {W80}1...` -> `5, {W75}4, {W75}3, {W80}2, {W80}1...` (Sistema, root)
- `H{W10}A{W10}V{W10}E {W10}A{W10} P{W10}L{W10}E{W10}A{W10}S{W10}A{W10}N{W10}T{W10} A{W10}W{W10}A{W10}K{W10}E{W10}N{W10}I{W10}N{W10}G{W10}--` -> `T{W10}E{W10}N{W10}H{W10}A{W10} {W10}U{W10}M{W10} {W10}B{W10}O{W10}M{W10} {W10}D{W10}E{W10}S{W10}P{W10}E{W10}R{W10}T{W10}A{W10}R{W10}--` (Sistema, root)
- `Wh... Where...?` -> `On... Onde...?` (Protagonista, root)
- `Where... am I...?` -> `Onde... estou...?` (Protagonista, root)
- `Above me... some kind of... cloth ceiling...?` -> `Acima de mim... uma espécie de... teto de pano...?` (Protagonista, root)
- `Barely any light...... Or is it just dark out...?` -> `Quase nenhuma luz...... Ou só está escuro lá fora...?` (Protagonista, root)
- `...Noise... Sounds like... fire?` -> `...Barulho... Parece... fogo?` (Protagonista, root)
- `U... Urgh... Everything's... distorted...` -> `Nnh... Argh... Está tudo... distorcido...` (Protagonista, root)
- `Why... am I...?` -> `Por que... eu...?` (Protagonista, root)
- `Are you awake?` -> `Você acordou?` (Kuon, root)
- `Ngh... hh...?` -> `Nnh... hn...?` (Protagonista, root)
- `What...?` -> `O quê...?` (Protagonista, root)
- `Girl` -> `Garota` (sistema, 13_01)
- `How are you feeling? I didn't see any injuries,\n` -> `Como você está se sentindo? Não vi ferimentos,\n` (Kuon, root)
- `but do you feel any pain anywhere?` -> `mas sente dor em algum lugar?` (Kuon, root)
- `...I suppose you might still be delirious...?` -> `...Acho que você ainda pode estar delirando...?` (Kuon, root)
- `Who... are you...?` -> `Quem... é você...?` (Protagonista, root)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `That's... Well, how do I put it...? I think that\n` -> `Isso... Bem, como eu explico...? Acho que isso\n` (Kuon, root)
- `might be a bit too hard to explain right now.` -> `pode ser difícil demais de explicar agora.` (Kuon, root)
- `Well, anyway... do you remember anything about\n` -> `Bom, enfim... você lembra de alguma coisa sobre\n` (Kuon, root)
- `what happened to you?` -> `o que aconteceu com você?` (Kuon, root)
- `Me...?` -> `Eu...?` (Protagonista, 15_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Oh--just try to relax...` -> `Ah--apenas tente relaxar...` (Kuon, root)
- `I can tell you everything you want to know later.` -> `Depois eu te conto tudo o que quiser saber.` (Kuon, root)
- `Ah... I get it...` -> `Ah... entendi...` (Protagonista, root)
- `This is... all just... a dream...` -> `Isso é... tudo só... um sonho...` (Protagonista, root)
- `Just relax for now... and rest.` -> `Por ora, relaxe... e descanse.` (Kuon, root)
- `Nn... hh...` -> `Nnh... hn...` (Protagonista, root)
- `Good night...` -> `Boa noite...` (Kuon, root)
- `Woman` -> `Mulher` (sistema, 14_07)
- `Oh dear, your room is a mess again...` -> `Ai, ai, seu quarto está uma bagunça de novo...` (Mulher (memória), root)
- `Hey, hey, Uncle! I'm here to visit!` -> `Ei, ei, Tio! Vim te visitar!` (Garota (memória), root)
- `Heh heh... You better be really happy! Cause today,\n` -> `Hehe... É bom você ficar bem feliz! Porque hoje,\n` (Garota (memória), root)
- `I'm gonna cook you your favorite      !` -> `vou cozinhar o seu favorito      !` (Garota (memória), root)
- `Hmmm... Then if you still aren't married even\n` -> `Hmmm... Então se você ainda não casou nem\n` (Garota (memória), 19_07)
- `when you're really old, I can marry you, OK?` -> `quando estiver bem velho, eu caso com você, tá?` (Garota (memória), 19_07)
- `I really do worry... You don't have to stay here.\n` -> `Eu me preocupo mesmo... Você não precisa ficar aqui.\n` (Mulher (memória), 19_08)
- `You can always...` -> `Você sempre pode...` (Mulher (memória), 19_08)
- `...You know you can come back anytime.` -> `...Sabe que pode voltar quando quiser.` (Mulher (memória), 19_08)
- `...You seem so distant, these days.` -> `...Você anda tão distante esses dias.` (Mulher (memória), 19_08)
- `Back then, it felt like you were always trailing\n` -> `Antes, parecia que você vivia atrás\n` (Mulher (memória), root)
- `around after the two of us... ` -> `de nós dois o tempo todo... ` (Mulher (memória), root)
- `Man` -> `Hom` (Sistema, 12_04)
- `...You took the medicine, then?` -> `...Então você tomou o remédio?` (Homem (memória), root)
- `There'll be a whole new world waiting for you\n` -> `Um mundo totalmente novo te aguarda\n` (Homem (memória), root)
- `when you wake up... Hmhmhm.` -> `quando você acordar... Hmhmhm.` (Homem (memória), root)
- `Yes... You are the first... and the last...` -> `Sim... Você é o primeiro... e o último...` (Homem (memória), root)
- `I'm not gonna make it for you anymore.` -> `Eu não vou mais poder fazer isso por você.` (Garota (memória), root)
- `right?` -> `né?` (Haku, 12_03)
- `Hee hee, OK.` -> `Hehe, tá bom.` (Garota (memória), root)
- `You better come. Pinky swear! Cross your heart\n` -> `É bom você vir. Promessa de mindinho! Jura\n` (Garota (memória), 19_07)
- `and hope to die!` -> `e que morra se mentir!` (Garota (memória), root)
- `It's a promise.` -> `É uma promessa.` (Protagonista, root)
- `That's... right...` -> `É... verdade...` (Protagonista, root)
- `The promise...` -> `A promessa...` (Protagonista, root)
- `Have to... go...` -> `Tenho que... ir...` (Protagonista, root)
- `She's waiting...` -> `Ela está esperando...` (Protagonista, root)
- `She's... waiting... for...` -> `Ela está esperando... por...` (Man, root)
- `Ah...hah...` -> `Ah...há...` (Man, root)
- `HA-CHOO!` -> `ATCHIM!` (Man, root)
- `Urgh... S-So cold...` -> `Argh... Q-Que frio...` (Man, root)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `I blink at the unfamiliar sight.` -> `Pisco diante da cena desconhecida.` (Man, root)
- `Wh-Where... am I?` -> `O-Onde... estou?` (Man, root)
- `I glance around. Trees, trees, and more trees.\n` -> `Olho ao redor. Árvores, árvores e mais árvores.\n` (Man, root)
- `It's a forest, and a pretty dense one at that.` -> `É uma floresta, e bem densa ainda por cima.` (Man, root)
- `It feels like the endless trees are swallowing\n` -> `Parece que as árvores sem fim engolem\n` (Man, root)
- `everything else up... even sound.` -> `todo o resto... até o som.` (Man, root)
- `Where... exactly am I...?` -> `Onde... exatamente eu estou...?` (Man, root)
- `How did I end up in a place like this...?` -> `Como fui parar num lugar assim...?` (Man, root)
- `Why...? Why...` -> `Por quê...? Por quê...` (Man, root)
- `I frantically search my memories.` -> `Vasculho minhas memórias freneticamente.` (Man, root)
- `Ngh... It's no use. Can't remember. What was\n` -> `Ngh... Não adianta. Não lembro. O que eu\n` (Man, root)
- `I doing up until now...?` -> `estava fazendo até agora...?` (Man, root)
- `Gah!` -> `Ai!` (Man, 13_01)
- `A sudden pain in my foot interrupts my thoughts.\n` -> `Uma dor súbita no pé interrompe meus pensamentos.\n` (Man, root)
- `I look down and realize... I'm barefoot.` -> `Olho para baixo e percebo... estou descalço.` (Man, root)
- `Why...?` -> `Por quê...?` (Man, root)
- `Gah, it's freezing...` -> `Ai, que frio de congelar...` (Man, root)
- `Why am I... No, hold on.` -> `Por que eu... Não, espera.` (Man, root)
- `Why am I dressed like this...?` -> `Por que estou vestido assim...?` (Man, root)
- `Out in this cold, in just a flimsy gown...?` -> `Nesse frio, só com uma camisola fininha...?` (Man, root)
- `Not even any underpants...` -> `Sem nem roupa de baixo...` (Man, root)
- `H-Hurgh... "Chilly"... d-doesn't even begin\n` -> `A-Argh... "Friozinho"... nem chega\n` (Man, root)
- `to describe it.` -> `perto de descrever.` (Man, root)
- `I look around, desperate for some way to get out\n` -> `Olho em volta, desesperado por um jeito de fugir\n` (Man, root)
- `of this cold.` -> `deste frio.` (Man, root)
- `Not a single house or a signpost anywhere...  ` -> `Nenhuma casa, nenhuma placa em lugar nenhum...  ` (Man, root)
- `Gah... Urgh...` -> `Gah... Argh...` (Man, root)
- `My head is splitting, too... Probably related\n` -> `Minha cabeça também está latejando... Deve ser\n` (Man, root)
- `to the empty stomach.` -> `do estômago vazio.` (Man, root)
- `Ah, right. This is all just a dream...` -> `Ah, claro. Isso é tudo só um sonho...` (Man, root)
- `...Dammit, it's no use. I can't fool myself here.` -> `...Droga, não adianta. Não dá pra me enganar aqui.` (Man, root)
- `Somehow, I pull myself together and get back\n` -> `De algum jeito, me recomponho e volto\n` (Man, root)
- `to my feet.` -> `a ficar de pé.` (Man, root)
- `No matter how I look at it, this is no dream.` -> `Por mais que eu tente, isto não é sonho nenhum.` (Man, root)
- `...Ha-choo! Bwa-CHOO!` -> `...Atchim! Aaa-TCHIM!` (Man, root)
- `Hurgh... Stuck out in this cold with nothing\n` -> `Argh... Preso neste frio sem nada\n` (Man, root)
- `but a robe, and totally naked underneath it.` -> `além de um robe, e pelado por baixo dele.` (Man, root)
- `I'm still holding up, but once the sun goes down,\n` -> `Ainda aguento, mas quando o sol se puser,\n` (Man, root)
- `I'll catch cold for sure. Worst-case scenario,\n` -> `vou pegar um resfriado na certa. Na pior das hipóteses,\n` (Man, root)
- `I'll freeze to death.` -> `morro congelado.` (Man, root)
- `If this isn't a dream, then that tent where I was\n` -> `Se isto não é sonho, então aquela tenda onde eu\n` (Man, root)
- `resting has to be out here somewhere.` -> `estava deve estar em algum lugar por aqui.` (Man, root)
- `All things considered, that's probably my best\n` -> `Pensando bem, essa é provavelmente minha melhor\n` (Man, root)
- `shot here...` -> `aposta aqui...` (Man, root)
- `I want to go back the way I came, but I've got\n` -> `Quero voltar pelo caminho que vim, mas não faço\n` (Man, root)
- `no idea which way that even is.` -> `ideia de qual é.` (Man, root)
- `What do I do? Should I just... follow some road\n` -> `O que eu faço? Sigo alguma trilha\n` (Man, root)
- `and hope for the best? Or wait here for help?` -> `e torço pelo melhor? Ou espero ajuda aqui?` (Man, root)
- `If you get lost, rule one is to stay still and\n` -> `Quando se perde, a regra um é ficar parado e\n` (Man, root)
- `wait for help. But the thing is...` -> `esperar ajuda. Mas o problema é...` (Man, root)
- `I don't even know if anyone's coming for me... ` -> `Não sei nem se alguém vem me procurar... ` (Man, root)
- `Can't really expect a search party when I don't\n` -> `Não dá pra esperar um grupo de busca quando nem\n` (Man, root)
- `even know what the hell I'm doing here myself.` -> `eu sei o que diabos faço aqui.` (Man, root)
- `I guess I'll have to risk it if I want to\n` -> `Acho que vou ter que arriscar se quiser\n` (Man, root)
- `get out of here.` -> `sair daqui.` (Man, root)
- `I should get moving before it gets any darker.` -> `Melhor me mexer antes que escureça mais.` (Man, root)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `I feel a shiver run down my spine... but this\n` -> `Sinto um arrepio na espinha... mas desta\n` (Man, root)
- `time it's not the cold.` -> `vez não é do frio.` (Man, root)
- `What...? Something felt... weird...` -> `O quê...? Senti algo... estranho...` (Man, root)
- `...Whoa! Wh-What the--` -> `...Uou! Q-Que diabos--` (Man, root)
- `Oh... just a bird... Phew. Geez, almost gave me\n` -> `Ah... é só um pássaro... Ufa. Quase me deu\n` (Man, root)
- `a heart attack.` -> `um ataque do coração.` (Man, root)
- `Nothing serious. What a relief...` -> `Nada de grave. Que alívio...` (Man, root)
- `Overhead, the birds are still screeching.\n` -> `Lá em cima, os pássaros ainda grasnam.\n` (Man, root)
- `They seem pretty worked up about something...` -> `Parecem bem agitados com alguma coisa...` (Man, root)
- `...These birds just won't shut up. What's got\n` -> `...Esses pássaros não calam a boca. O que os\n` (Man, root)
- `them so freaked out...?` -> `deixou tão assustados...?` (Man, root)
- `*Shiver*` -> `*Arrepio*` (Man, root)
- `...There it is again.` -> `...Lá está de novo.` (Man, root)
- `It feels like... something's watching me.` -> `Sinto como se... algo estivesse me observando.` (Man, root)
- `Urgh... I... feel sick...` -> `Argh... Estou... passando mal...` (Man, root)
- `My vision blurs, and I lose my balance.\n` -> `Minha visão embaça e perco o equilíbrio.\n` (Man, root)
- `I trip on my own feet, and stumble forward. ` -> `Tropeço nos próprios pés e caio pra frente. ` (Man, root)
- `And in that instant--` -> `E nesse instante--` (Man, root)
- `Whoa--` -> `Uou--` (Man, 16_01)
- `*Slash!*` -> `*Zás!*` (Man, root)
- `I hear it just above my head.\n` -> `Ouço logo acima da minha cabeça.\n` (Man, root)
- `A jarring, violent sound, like metal on metal.` -> `Um som violento e estridente, como metal contra metal.` (Man, root)
- `Wh... Wh-Wha...` -> `Q... Q-Quê...` (Man, 15_01)
- `Fallen to one knee, I shift around cautiously\n` -> `Caído de joelhos, me viro com cautela\n` (Man, root)
- `to look back.` -> `para olhar pra trás.` (Man, root)
- `What... is... this...?` -> `O que... é... isto...?` (Man, root)
- `A row of sharp jags and points, like honed\n` -> `Uma fileira de pontas e gumes afiados, como\n` (Man, root)
- `blades, gleams in the cold air.` -> `lâminas, reluz no ar gelado.` (Man, root)
- `They're like scissors... or maybe a saw?` -> `São como tesouras... ou talvez um serrote?` (Man, root)
- `But saws and scissors can't compare to THAT.\n` -> `Mas serrotes e tesouras não chegam perto DAQUILO.\n` (Man, root)
- `It's bigger than a human arm...` -> `É maior que um braço humano...` (Man, root)
- `What the...` -> `Mas que...` (Man, root)
- `What... is THAT!?` -> `O que... é AQUILO!?` (Man, root)
- `Whatever it is, it's definitely insectoid.` -> `Seja lá o que for, é definitivamente um inseto.` (Man, root)
- `But... this thing doesn't look like any bug\n` -> `Mas... essa coisa não parece nenhum inseto\n` (Man, root)
- `I've ever seen.` -> `que eu já vi.` (Man, root)
- `It's at least ten times... no, a hundred\n` -> `É no mínimo dez vezes... não, cem\n` (Man, root)
- `times bigger.` -> `vezes maior.` (Man, root)
- `What is... going on...?` -> `O que está... acontecendo...?` (Man, root)
- `Revulsion wells up inside me, and my skin crawls.\n` -> `A repulsa cresce dentro de mim, e minha pele se arrepia.\n` (Man, root)
- `I just want to look away from this thing.` -> `Só quero desviar o olhar dessa coisa.` (Man, root)
- `What do I do...? What should I do...?` -> `O que eu faço...? O que eu devo fazer...?` (Man, root)
- `Hh... Ah... Aaah--` -> `Hn... Ah... Aaah--` (Man, root)
- `Without looking away, I jump off the cliffside\n` -> `Sem desviar o olhar, salto do penhasco\n` (Man, root)
- `in front of me.` -> `à minha frente.` (Man, root)
- `I feel that unnatural sharpness cut through\n` -> `Sinto aquele corte sobrenatural rasgar\n` (Man, root)
- `the air just behind me as I leap.` -> `o ar logo atrás de mim enquanto pulo.` (Man, root)
- `Aaaaah!` -> `Aaaaah!` (Man, root)
- `I'm... flying!?` -> `Estou... voando!?` (Man, root)
- `For a moment, I'm soaring through the air.` -> `Por um momento, deslizo pelo ar.` (Man, root)
- `I feel myself hit the slope, and tumble down\n` -> `Sinto-me bater na encosta e rolar\n` (Man, root)
- `the snowy cliffside.` -> `pela ladeira nevada.` (Man, root)
- `Guh--` -> `Agh--` (Man, 13_03)
- `My back hits the ground hard. The impact knocks\n` -> `Minhas costas batem com força no chão. O impacto\n` (Man, root)
- `the wind out of me, and I choke.` -> `me tira o fôlego, e eu engasgo.` (Man, root)
- `Urgh... Ghh...` -> `Argh... Ghh...` (Man, root)
- `Ghh!` -> `Agh!` (Man, root)
- `My body's screaming in agony, but I don't have\n` -> `Meu corpo grita de dor, mas não tenho\n` (Man, root)
- `time. I stagger to my feet and start running.` -> `tempo. Cambaleio de pé e começo a correr.` (Man, root)
- `What was that, what was that, what was that...` -> `O que era aquilo, o que era aquilo, o que era aquilo...` (Man, root)
- `WHAT THE HELL WAS THAT!?` -> `QUE DIABOS ERA AQUILO!?` (Man, root)
- `An insect that massive doesn't exist...\n` -> `Um inseto tão imenso não existe...\n` (Man, root)
- `There's no way it COULD exist!` -> `Não tem como existir!` (Man, root)
- `So this has to be a dream! That was all just\n` -> `Então isto só pode ser um sonho! Aquilo foi tudo\n` (Man, root)
- `some illusion!` -> `uma ilusão!` (Man, root)
- `I just have to turn and look... and I'll see\n` -> `Basta eu me virar e olhar... e vou ver\n` (Man, root)
- `everyone smiling, waiting for me--` -> `todo mundo sorrindo, esperando por mim--` (Man, root)
- `And I look back.` -> `E olho pra trás.` (Man, root)
- `Aaaaaargh! I-I-I-It's gonna...\n` -> `Aaaaargh! V-V-V-Vai...\n` (Man, root)
- `It's gonna EAT me!!` -> `Vai me DEVORAR!!` (Man, root)
- `I start zigzagging right and left, serpentine,\n` -> `Começo a ziguezaguear pra direita e esquerda,\n` (Man, root)
- `trying to keep it guessing.` -> `tentando despistá-lo.` (Man, root)
- `Hh... hh... H-How far do I have to run!?` -> `Hh... hh... Q-Quanto eu ainda tenho que correr!?` (Man, root)
- `I-I can't... keep this up...` -> `E-Eu não... aguento mais...` (Man, root)
- `I keep running straight ahead. \n` -> `Continuo correndo em frente. \n` (Man, root)
- `but...` -> `mas...` (Kuon, 12_16)
- `Wha--` -> `Quê--` (Man, 15_01)
- `Something gives way under my heel.` -> `Algo cede sob meu calcanhar.` (Man, root)
- `Aaaaaaaaagghh!` -> `Aaaaaaaaagh!` (Man, root)
- `Ghh...` -> `Argh...` (Man, root)
- `Agh... Did I fall again...? Everything... hurts...` -> `Argh... Caí de novo...? Tudo... dói...` (Man, root)
- `I shade my eyes with my hand, peering up at the\n` -> `Protejo os olhos com a mão, espiando a\n` (Man, root)
- `light shining from above. Looks like a hole...` -> `luz que vem de cima. Parece um buraco...` (Man, root)
- `If that's where I fell from... Must've been\n` -> `Se foi de lá que caí... Deve ter sido\n` (Man, root)
- `a bush or something hiding it...` -> `um arbusto ou algo escondendo o buraco...` (Man, root)
- `It'll be tough, but if I climb the wall here,\n` -> `Vai ser difícil, mas se eu escalar a parede aqui,\n` (Man, root)
- `maybe I can get back above ground...?` -> `talvez consiga voltar pra superfície...?` (Man, root)
- `But even if I could get back up, that thing's\n` -> `Mas mesmo se eu subir, aquela coisa\n` (Man, root)
- `just going to eat me. So...` -> `vai só me comer. Então...` (Man, root)
- `Strangely enough, the walls are giving off\n` -> `Estranhamente, as paredes emitem\n` (Man, root)
- `a faint glow. It's dim, but it's helping me\n` -> `um brilho fraco. É tênue, mas me ajuda\n` (Man, root)
- `see the place.` -> `a enxergar o lugar.` (Man, root)
- `It looks like some kind of cavern. There's a\n` -> `Parece algum tipo de caverna. Há um\n` (Man, root)
- `tunnel that seems like it goes on for a while.` -> `túnel que parece seguir por um bom tempo.` (Man, root)
- `Well, if I can't go up, then I might as well\n` -> `Bem, se não posso subir, é melhor\n` (Man, root)
- `go forward...` -> `seguir em frente...` (Man, root)
- `Still, even with this dim glow, I can't really\n` -> `Ainda assim, mesmo com esse brilho fraco, não dá\n` (Man, root)
- `tell what it's like further inside.` -> `pra ver bem como é mais pra dentro.` (Man, root)
- `Maybe it'd be safer to just wait here quietly\n` -> `Talvez seja mais seguro só esperar aqui quieto\n` (Man, root)
- `after all...` -> `afinal...` (Man, root)
- `Ah...!` -> `Ah...!` (Man, root)
- `...That noise... It's getting closer.` -> `...Aquele barulho... Está chegando mais perto.` (Man, root)
- `If I hang around here, it'll only hunt me down...\n` -> `Se eu ficar por aqui, vai só me caçar...\n` (Man, root)
- `I can't stop now.` -> `Não posso parar agora.` (Man, root)
- `With my decision made, I step forth into\n` -> `Decisão tomada, avanço para dentro\n` (Man, root)
- `the tunnel.` -> `do túnel.` (Man, root)
- `Rrrgh... Why is this happening to me!?` -> `Rrgh... Por que isso está acontecendo comigo!?` (Man, root)
- `Ngh, hah... phew... hah...\n` -> `Ngh, há... ufa... há...\n` (Man, root)
- `I don't feel it... chasing after me...` -> `Não sinto ela... vindo atrás de mim...` (Man, root)
- `I finally let myself sit, exhaustion and relief\n` -> `Finalmente me deixo sentar, exaustão e alívio\n` (Man, root)
- `settling in.` -> `tomando conta.` (Man, root)
- `Hahh... I'm safe now... Th-This... should be\n` -> `Hã... Estou a salvo agora... I-Isto... deve ser\n` (Man, root)
- `far... enough... ` -> `longe... o bastante... ` (Man, root)
- `*Shudder*` -> `*Tremor*` (Kuon, 19_07)
- `I cringe instinctively. A sudden chill,\n` -> `Me encolho por instinto. Um frio súbito,\n` (Man, root)
- `unpleasantly familiar, runs down my spine.` -> `desagradavelmente familiar, desce pela espinha.` (Man, root)
- `My body freezes. I can't move, confronted\n` -> `Meu corpo congela. Não consigo me mexer, diante\n` (Man, root)
- `with something beyond understanding.` -> `de algo além da compreensão.` (Man, root)
- `Wh... Wh-Wh-Why...` -> `Q... P-P-Por...` (Man, root)
- `Why is it HERE!?` -> `Por que está AQUI!?` (Man, root)
- `The colossal insect is right in front of me.` -> `O inseto colossal está bem na minha frente.` (Man, root)
- `Did this thing set me up!?` -> `Será que essa coisa me armou!?` (Man, root)
- `But the specifics... don't really matter\n` -> `Mas os detalhes... já não importam\n` (Man, root)
- `anymore.` -> `mais.` (Man, root)
- `Urgh--` -> `Argh--` (Man, 13_05)
- `It happens in an instant. My back's to the\n` -> `Acontece num instante. Estou de costas pra\n` (Man, root)
- `wall, and any escape is blocked by its\n` -> `parede, e qualquer fuga é bloqueada pelo\n` (Man, root)
- `sinuous body.` -> `corpo sinuoso dele.` (Man, root)
- `I... can't escape.` -> `Eu... não tenho como fugir.` (Man, root)
- `It creeps forward warily, as if it's learned\n` -> `Ele rasteja pra frente com cautela, como se\n` (Man, root)
- `its lesson from its failed attempts earlier.` -> `tivesse aprendido a lição das tentativas falhas.` (Man, root)
- `It leans in, close enough to pull me in with\n` -> `Ele se inclina, perto o bastante pra me agarrar\n` (Man, root)
- `a single snap of its jaws... and stops.` -> `com um só estalo das mandíbulas... e para.` (Man, root)
- `*Drip*` -> `*Pingo*` (Man, root)
- `Something like saliva is dripping from its jaws.` -> `Algo como saliva pinga das mandíbulas dele.` (Man, root)
- `Is this... where I die...?` -> `É aqui... que eu morro...?` (Man, root)
- `Like this... in this senseless situation...\n` -> `Assim... nesta situação sem sentido...\n` (Man, root)
- `eaten by whatever the hell this thing is...` -> `devorado por seja lá o que for essa coisa...` (Man, root)
- `The insect's jaws finally click open, gaping\n` -> `As mandíbulas do inseto enfim se abrem, escancaradas\n` (Man, root)
- `to devour me. ` -> `pra me devorar. ` (Man, root)
- `I'm dead--` -> `Estou morto--` (Man, root)
- `*Drip*... *Drip*... *Drip*...` -> `*Pingo*... *Pingo*... *Pingo*...` (Man, root)
- `The insect suddenly darts aside without biting\n` -> `O inseto de repente se lança pro lado sem morder,\n` (Man, root)
- `me, like it's trying to escape something...` -> `como se tentasse escapar de algo...` (Man, root)
- `...and something descends from far above,\n` -> `...e algo desce lá do alto,\n` (Man, root)
- `translucent and massive, as if to crush\n` -> `translúcido e imenso, como que pra esmagar\n` (Man, root)
- `whatever's below.` -> `tudo o que houver embaixo.` (Man, root)
- `It engulfs the massive insect effortlessly.` -> `Engole o inseto colossal sem esforço.` (Man, root)
- `What... the...` -> `Mas que...` (Man, root)
- `What is that...? Wh-What's... going on now...?` -> `O que é aquilo...? Q-Que está... acontecendo agora...?` (Man, root)
- `I can see the insect writhing and thrashing,\n` -> `Vejo o inseto se contorcendo e debatendo,\n` (Man, root)
- `trapped inside its slick, gelatinous body.` -> `preso dentro do corpo gelatinoso e viscoso.` (Man, root)
- `The insect was already beyond comprehension,\n` -> `O inseto já estava além da compreensão,\n` (Man, root)
- `but this thing... defies all reason. And...` -> `mas essa coisa... desafia toda lógica. E...` (Man, root)
- `It's melting...?` -> `Está derretendo...?` (Man, root)
- `This enormous insect's shell, hard as metal,\n` -> `A carapaça desse inseto enorme, dura feito metal,\n` (Man, root)
- `is bubbling like it's being dissolved.\n` -> `borbulha como se estivesse sendo dissolvida.\n` (Man, root)
- `It's coming apart inside the slime.` -> `Está se desfazendo dentro do limo.` (Man, root)
- `Is it... eating the...?` -> `Será que está... comendo o...?` (Man, root)
- `The insect struggles desperately inside this\n` -> `O inseto luta desesperadamente dentro dessa\n` (Man, root)
- `amorphous creature, but its body is almost\n` -> `criatura amorfa, mas o corpo dele está quase\n` (Man, root)
- `completely digested.` -> `completamente digerido.` (Man, root)
- `All I can do is stare blankly, still in shock.` -> `Só consigo encarar, atônito, ainda em choque.` (Man, root)
- `The insect's face surfaces for an instant,\n` -> `O rosto do inseto vem à tona por um instante,\n` (Man, root)
- `but it has no power left. The viscous red\n` -> `mas não tem mais força. O vermelho viscoso\n` (Man, root)
- `swallows it up.` -> `o engole de vez.` (Man, root)
- `...Am I... safe?` -> `...Estou... a salvo?` (Man, root)
- `I whisper, in sheer gratitude for still being\n` -> `Sussurro, em pura gratidão por ainda estar\n` (Man, root)
- `alive.` -> `vivo.` (Man, root)
- `I... surviv--!` -> `Eu... sobrevi--!` (Man, root)
- `I can't keep myself from letting out a cheer\n` -> `Não consigo conter um grito\n` (Man, root)
- `of relief... until I realize. ` -> `de alívio... até perceber. ` (Man, root)
- `The amorphous creature swells and heaves,\n` -> `A criatura amorfa incha e se agita,\n` (Man, root)
- `a short distance away.` -> `a pouca distância.` (Man, root)
- `If it's somehow still hungry after that huge\n` -> `Se ainda estiver com fome depois daquele inseto\n` (Man, root)
- `insect, there's no reason it won't go for me\n` -> `enorme, não há razão pra não vir atrás de mim\n` (Man, root)
- `next.` -> `em seguida.` (Man, root)
- `I need to get out of here, before--` -> `Preciso sair daqui, antes que--` (Man, root)
- `...Ah!` -> `...Ah!` (Man, root)
- `The amorphous creature begins oozing forward...\n` -> `A criatura amorfa começa a escorrer pra frente...\n` (Man, root)
- `towards me.` -> `na minha direção.` (Man, root)
- `It stops. Just waiting... like it's curious\n` -> `Ela para. Só esperando... como se tivesse curiosidade\n` (Man, root)
- `to see what I do next.` -> `de ver o que faço em seguida.` (Man, root)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `Can it hear me? Is it going off vibrations in\n` -> `Será que me ouve? Será que sente vibrações\n` (Man, root)
- `the ground? Any sudden movements, and I'm dead.` -> `no chão? Qualquer movimento brusco, e eu morro.` (Man, root)
- `No motion. I keep perfectly still, holding\n` -> `Sem me mexer. Fico perfeitamente imóvel, prendendo\n` (Man, root)
- `my breath.` -> `a respiração.` (Man, root)
- `Its viscous surface begins rippling...` -> `A superfície viscosa começa a ondular...` (Man, root)
- `...and little by little, reforms into a\n` -> `...e aos poucos se remodela numa\n` (Man, root)
- `familiar shape.` -> `forma familiar.` (Man, root)
- `Wha--?` -> `Quê--?` (Man, root)
- `My voice dies in my throat.` -> `Minha voz morre na garganta.` (Man, root)
- `The face that appears before me is misshapen, glutinous,\n` -> `O rosto que surge diante de mim é disforme, viscoso,\n` (Man, root)
- `horrifying... but unmistakably human.` -> `horrendo... mas inconfundivelmente humano.` (Man, root)
- `Unfocused eyes fixate on me. Its mouth gasps\n` -> `Olhos perdidos se fixam em mim. A boca arqueja\n` (Man, root)
- `and gapes soundlessly, like a fish drowning\n` -> `e se abre sem som, como um peixe se afogando\n` (Man, root)
- `in air.` -> `no ar.` (Man, root)
- `What... are... you...?` -> `O que... é... você...?` (Man, root)
- `...hh... yh...` -> `...hh... ih...` (Man, root)
- `Is it... trying to talk...? It just sounds\n` -> `Será que... está tentando falar...? Só soa\n` (Man, root)
- `like air escaping--I can't make out what\n` -> `como ar escapando--não consigo entender o\n` (Man, root)
- `it's saying.` -> `que diz.` (Man, root)
- `...khh... yh...` -> `...kh... ih...` (Man, root)
- `By reflex or by curiosity, I move closer to\n` -> `Por reflexo ou curiosidade, me aproximo pra\n` (Man, root)
- `hear what it's saying... and another voice\n` -> `ouvir o que diz... e outra voz\n` (Man, root)
- `rings out.` -> `ressoa.` (Man, root)
- `Cover your eyes and ears!` -> `Cubra os olhos e os ouvidos!` (Man, root)
- `The sharp command is followed by a cylindrical\n` -> `O comando ríspido é seguido por um objeto\n` (Man, root)
- `object bouncing on the stone between us.\n` -> `cilíndrico quicando na pedra entre nós.\n` (Man, root)
- `Looks like--` -> `Parece--` (Man, root)
- `A grenade...? Gah!?` -> `Uma granada...? Gah!?` (Man, root)
- `I instinctively shut my eyes, and clap my hands\n` -> `Por instinto, fecho os olhos e tapo\n` (Man, root)
- `over my ears.` -> `os ouvidos com as mãos.` (Man, root)
- `------------------gghhh------!` -> `------------------gghh------!` (Man, root)
- `It's too bright to make anything out, but\n` -> `Está claro demais pra ver qualquer coisa, mas\n` (Man, root)
- `I feel the ground shake as if the creature's\n` -> `sinto o chão tremer como se a criatura\n` (Man, root)
- `writhing.` -> `se contorcesse.` (Man, root)
- `Is... Is this...?` -> `Será... Será que é...?` (Man, root)
- `A sudden grasp.` -> `Um agarrão súbito.` (Man, root)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Someone grabs my hand with an incredible force,\n` -> `Alguém agarra minha mão com uma força incrível,\n` (Man, root)
- `and when I try to pull away, I get yelled at.` -> `e quando tento me soltar, levo uma bronca.` (Man, root)
- `You can freeze up later!` -> `Você congela depois!` (Man, root)
- `My body's floating in the air...\n` -> `Meu corpo está flutuando no ar...\n` (Man, root)
- `It feels like I'm flying again.` -> `É como se eu estivesse voando de novo.` (Man, root)
- `I nervously open my eyes, and see someone\n` -> `Abro os olhos, nervoso, e vejo alguém\n` (Man, root)
- `bounding forward, my hand in theirs.` -> `saltando à frente, minha mão na dela.` (Man, root)
- `It's so fast...\n` -> `É tão rápido...\n` (Man, root)
- `It's like we're the wind.` -> `É como se fôssemos o vento.` (Man, root)
- `We cut through the air, and the wind roars\n` -> `Cortamos o ar, e o vento ruge\n` (Man, root)
- `past my ears.` -> `passando pelos meus ouvidos.` (Man, root)
- `My rescuer glances back to me, as if checking\n` -> `Minha salvadora olha pra trás, como que\n` (Man, root)
- `on me. ` -> `checando se estou bem. ` (Man, root)
- `A... woman?` -> `Uma... mulher?` (Man, root)
- `No... more like a young lady?` -> `Não... mais pra uma moça?` (Man, root)
- `Her face is beautiful, though oddly childish.\n` -> `O rosto dela é lindo, embora curiosamente infantil.\n` (Man, root)
- `Oversized ears... And a fluffy tail.` -> `Orelhas grandes demais... E uma cauda peluda.` (Man, root)
- `There's something... ethereal about her.\n` -> `Há algo... etéreo nela.\n` (Man, root)
- `I can't look away.` -> `Não consigo desviar o olhar.` (Man, root)
- `Even in this incredible situation, it feels\n` -> `Mesmo nesta situação absurda, parece\n` (Man, root)
- `like time's stopped.` -> `que o tempo parou.` (Man, root)
- `Then, suddenly, her brow furrows.` -> `Então, de repente, ela franze a testa.` (Man, root)
- `I glance back, unsure of what she's looking at...` -> `Olho pra trás, sem saber o que ela está vendo...` (Man, root)
- `Aaagh--` -> `Aaagh--` (Man, root)
- `That amorphous creature surges forward, closing\n` -> `Aquela criatura amorfa avança, se aproximando\n` (Man, root)
- `in on us like some kind of predatory wave.` -> `de nós como uma onda predadora.` (Man, root)
- `In this linear cavern, there's nowhere else\n` -> `Nesta caverna estreita, não há pra onde\n` (Man, root)
- `to run.` -> `fugir.` (Man, root)
- `It's gonna catch up--!` -> `Vai nos alcançar--!` (Man, root)
- `But the girl's already seen it. She whips\n` -> `Mas a garota já viu. Ela saca\n` (Man, root)
- `another cylinder from her waist, and\n` -> `outro cilindro da cintura e o\n` (Man, root)
- `throws it behind us.` -> `joga atrás de nós.` (Man, root)
- `The blinding flash and the explosion follow\n` -> `O clarão ofuscante e a explosão vêm\n` (Man, root)
- `almost instantly.` -> `quase no mesmo instante.` (Man, root)
- `------------------rngghh------!` -> `------------------rngh------!` (Man, root)
- `Gyaaaagh!` -> `Gyaaagh!` (Man, root)
- `Now's our chance!` -> `Agora é nossa chance!` (Man, root)
- `Hahh... hh... hahh...` -> `Há... hh... há...` (Man, root)
- `We're outside... I-I'm finally safe...` -> `Estamos do lado de fora... E-Estou enfim a salvo...` (Man, root)
- `My legs give out. I collapse onto the snowy\n` -> `Minhas pernas cedem. Desabo na neve\n` (Man, root)
- `ground.` -> `do chão.` (Man, 19_08)
- `I can barely even believe I was able to run\n` -> `Mal acredito que consegui correr\n` (Man, root)
- `as much as I did.` -> `tudo aquilo.` (Man, root)
- `I guess humans really can do anything when\n` -> `Acho que humanos conseguem qualquer coisa quando\n` (Man, root)
- `their lives are on the line...` -> `a vida está em jogo...` (Man, root)
- `The girl's exhausted too--can't blame her--\n` -> `A garota também está exausta--não dá pra culpá-la--\n` (Man, root)
- `and she takes a seat, catching her breath.` -> `e se senta, recuperando o fôlego.` (Man, root)
- `...She saved my life... I should at least\n` -> `...Ela salvou minha vida... Eu deveria pelo menos\n` (Man, root)
- `thank her properly.` -> `agradecer direito.` (Man, root)
- `Th-Thank you so much for saving me...` -> `M-Muito obrigado por me salvar...` (Man, root)
- `Did she even hear me? My throat is raspy and\n` -> `Será que ela me ouviu? Minha garganta está rouca e\n` (Man, root)
- `raw, and I can't speak up that well.` -> `áspera, e não consigo falar muito alto.` (Man, root)
- `She notices, and turns towards me.` -> `Ela percebe e se vira pra mim.` (Man, root)
- `She has a strange look on her face, like she's\n` -> `Tem uma expressão estranha no rosto, como se\n` (Man, root)
- `seen something she wasn't expecting to.` -> `tivesse visto algo que não esperava.` (Man, root)
- `Ah... Seeing her face again like this...\n` -> `Ah... Vendo o rosto dela assim de novo...\n` (Man, root)
- `There really is something beautiful about her.` -> `Tem mesmo algo de bonito nela.` (Man, root)
- `That slightly confused expression, too...\n` -> `Aquela expressão um tanto confusa, também...\n` (Man, root)
- `Wow, she's cute.` -> `Nossa, ela é uma graça.` (Man, root)
- `Is there something wrong with my face?` -> `Tem algo de errado com meu rosto?` (Kuon, root)
- `O-Oh, no, not really... ` -> `A-Ah, não, nada não... ` (Kuon, root)
- `Still, though.` -> `Mesmo assim.` (Kuon, root)
- `I take my eyes off you for just a moment and\n` -> `Tiro os olhos de você por um só instante e\n` (Kuon, root)
- `you disappear, but I never imagined something\n` -> `você some, mas nunca imaginei uma coisa\n` (Kuon, root)
- `like this.` -> `dessas.` (Kuon, 17_04)
- `I'm glad I made it in time, but in the future...\n` -> `Ainda bem que cheguei a tempo, mas no futuro...\n` (Kuon, root)
- `I think I'd prefer you don't cause me so much\n` -> `acho que prefiro que você não me dê tanto\n` (Kuon, root)
- `trouble.` -> `de verdade.` (Haku, 12_04)
- `Urgh... I'm sorry.` -> `Argh... Me desculpe.` (Kuon, root)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `Wait, take her eyes off me...?\n` -> `Espera, tirar os olhos de mim...?\n` (Kuon, root)
- `And I disappeared?` -> `E eu sumi?` (Kuon, root)
- `What does she mean by that? She seems somehow...\n` -> `O que ela quer dizer com isso? Ela parece de algum\n` (Kuon, root)
- `familiar, too...` -> `jeito... familiar, também...` (Kuon, root)
- `Does that mean you know who I am...?` -> `Quer dizer que você sabe quem eu sou...?` (Kuon, root)
- `If you know who I am, where I'm from, please--\n` -> `Se você sabe quem eu sou, de onde venho, por favor--\n` (Kuon, root)
- `tell me.` -> `me diga.` (Kuon, 18_01)
- `Huh...? Oh...` -> `Hã...? Ah...` (Kuon, root)
- `Who am I? Where am I? What was that thing\n` -> `Quem sou eu? Onde estou? O que era aquela coisa\n` (Kuon, root)
- `that attacked me? What was--I mean, how--` -> `que me atacou? O que era--quer dizer, como--` (Kuon, root)
- `Ngh... I'm trying to ask all my questions\n` -> `Ngh... Tento fazer todas as perguntas\n` (Kuon, root)
- `at once, and none of them are coming out\n` -> `de uma vez, e nenhuma sai\n` (Kuon, root)
- `Right.` -> `direito.` (Kuon, 15_01)
- `I'm--` -> `Eu sou--` (Kuon, root)
- `The girl stands with a troubled smile on her\n` -> `A garota fica de pé com um sorriso aflito no\n` (Kuon, root)
- `face, and extends her hand to me.` -> `rosto e estende a mão pra mim.` (Kuon, root)
- `We should head back for now.` -> `É melhor voltarmos por enquanto.` (Kuon, root)
- `If you stay out here dressed like that,\n` -> `Se você ficar aqui fora vestido assim,\n` (Kuon, root)
- `you're going to end up with a cold.` -> `vai acabar pegando um resfriado.` (Kuon, root)
- `Dressed...?` -> `Vestido...?` (Kuon, root)
- `The cold air hits me all at once again, and\n` -> `O ar gelado me atinge de novo de uma vez, e\n` (Kuon, root)
- `I finally remember the state I'm in.` -> `finalmente lembro o estado em que estou.` (Kuon, root)
- `Come to think of it, have I really been\n` -> `Pensando bem, será que andei mesmo\n` (Kuon, root)
- `flailing around this whole forest in this\n` -> `perambulando por toda esta floresta nesta\n` (Kuon, root)
- `flimsy thing...?` -> `coisinha fina...?` (Kuon, root)
- `Hah... Ha-CHOO!` -> `Hã... Aaa-TCHIM!` (Kuon, root)
- `...Hee hee.` -> `...Hehe.` (Kuon, root)
- `She lets out a laugh, clear as a bell, at the\n` -> `Ela solta uma risada, clara como um sino, com o\n` (Kuon, root)
- `sound of my sneeze echoing through the forest.` -> `som do meu espirro ecoando pela floresta.` (Kuon, root)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `She takes my hand with her pale, delicate fingers,\n` -> `Ela toma minha mão com seus dedos pálidos e delicados,\n` (Kuon, root)
- `and pulls me to my feet. ` -> `e me ajuda a ficar de pé. ` (Kuon, root)
- `Let's go.` -> `Vamos.` (Kuon, root)
- `H-Hey...` -> `E-Ei...` (Kuon, 17_01)
- `I shift my hand slightly, squeezing back at her\n` -> `Movo a mão de leve, apertando de volta o\n` (Kuon, root)
- `grip. That lone touch of warmth...` -> `aperto dela. Aquele único toque de calor...` (Kuon, root)
- `...I couldn't have known what lay ahead of us.\n` -> `...Eu não tinha como saber o que nos aguardava.\n` (Kuon, root)
- `That this was only the beginning.` -> `Que aquilo era só o começo.` (Kuon, root)
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
| 0x3398 | 13 | Ngh... ghh... |
| 0x33a6 | 7 | Nn...\n |
| 0x33ae | 16 | It's... warm...? |
| 0x33bf | 3 | Nh? |
| 0x33c3 | 9 | Wh-Who... |
| 0x33cd | 21 | ...calls... to me...? |
| 0x33e3 | 21 | Wait... I'm still...! |
| 0x33f9 | 31 | INITIALIZING AWAKENING PROCESS. |
| 0x3419 | 40 | SYSTEMS YELLOW. RESTARTING IN 5 SECONDS. |
| 0x3442 | 13 | SYSTEM ERROR. |
| 0x3450 | 40 | PROBLEM DETECTED IN AWAKENING PROCESS.\n |
| 0x3479 | 26 | SUBJECT SEVERELY AFFECTED. |
| 0x3494 | 28 | ABORT COMMAND: CANCELLED. \n |
| 0x34b1 | 34 | PROCESS UNABLE TO BE TERMINATED.\n |
| 0x34d4 | 21 | COMMENCING COUNTDOWN. |
| 0x34ea | 36 | 5, {W75}4, {W75}3, {W80}2, {W80}1... |
| 0x350f | 137 | H{W10}A{W10}V{W10}E {W10}A{W10} P{W10}L{W10}E{W10}A{W10}S{W10}A{W10}N{W10}T{W10} A{W10}W{W10}A{W10}K{W10}E{W10}N{W10}I{W10}N{W10}G{W10}-- |
| 0x359d | 15 | Wh... Where...? |
| 0x35ad | 17 | Where... am I...? |
| 0x35bf | 45 | Above me... some kind of... cloth ceiling...? |
| 0x35ed | 49 | Barely any light...... Or is it just dark out...? |
| 0x361f | 32 | ...Noise... Sounds like... fire? |
| 0x3640 | 41 | U... Urgh... Everything's... distorted... |
| 0x366a | 15 | Why... am I...? |
| 0x367a | 14 | Are you awake? |
| 0x3689 | 13 | Ngh... hh...? |
| 0x3697 | 8 | What...? |
| 0x36a0 | 4 | Girl |
| 0x36a5 | 49 | How are you feeling? I didn't see any injuries,\n |
| 0x36d7 | 34 | but do you feel any pain anywhere? |
| 0x36fa | 45 | ...I suppose you might still be delirious...? |
| 0x3728 | 18 | Who... are you...? |
| 0x373b | 5 | Oh... |
| 0x3741 | 50 | That's... Well, how do I put it...? I think that\n |
| 0x3774 | 45 | might be a bit too hard to explain right now. |
| 0x37a2 | 48 | Well, anyway... do you remember anything about\n |
| 0x37d3 | 21 | what happened to you? |
| 0x37e9 | 6 | Me...? |
| 0x37f0 | 7 | Urgh... |
| 0x37f8 | 24 | Oh--just try to relax... |
| 0x3811 | 49 | I can tell you everything you want to know later. |
| 0x3843 | 17 | Ah... I get it... |
| 0x3855 | 33 | This is... all just... a dream... |
| 0x3877 | 31 | Just relax for now... and rest. |
| 0x3897 | 11 | Nn... hh... |
| 0x38a3 | 13 | Good night... |
| 0x38b1 | 5 | Woman |
| 0x38b7 | 37 | Oh dear, your room is a mess again... |
| 0x38dd | 35 | Hey, hey, Uncle! I'm here to visit! |
| 0x3901 | 53 | Heh heh... You better be really happy! Cause today,\n |
| 0x3937 | 39 | I'm gonna cook you your favorite      ! |
| 0x395f | 47 | Hmmm... Then if you still aren't married even\n |
| 0x398f | 44 | when you're really old, I can marry you, OK? |
| 0x39bc | 51 | I really do worry... You don't have to stay here.\n |
| 0x39f0 | 17 | You can always... |
| 0x3a02 | 38 | ...You know you can come back anytime. |
| 0x3a29 | 35 | ...You seem so distant, these days. |
| 0x3a4d | 50 | Back then, it felt like you were always trailing\n |
| 0x3a80 | 30 | around after the two of us...  |
| 0x3a9f | 3 | Man |
| 0x3aa3 | 31 | ...You took the medicine, then? |
| 0x3ac3 | 47 | There'll be a whole new world waiting for you\n |
| 0x3af3 | 27 | when you wake up... Hmhmhm. |
| 0x3b0f | 43 | Yes... You are the first... and the last... |
| 0x3b3b | 38 | I'm not gonna make it for you anymore. |
| 0x3b62 | 6 | Right? |
| 0x3b69 | 12 | Hee hee, OK. |
| 0x3b76 | 48 | You better come. Pinky swear! Cross your heart\n |
| 0x3ba7 | 16 | and hope to die! |
| 0x3bb8 | 15 | It's a promise. |
| 0x3bc8 | 5 | Nn... |
| 0x3bce | 18 | That's... right... |
| 0x3be1 | 14 | The promise... |
| 0x3bf0 | 16 | Have to... go... |
| 0x3c01 | 16 | She's waiting... |
| 0x7da5 | 26 | She's... waiting... for... |
| 0x7dc0 | 11 | Ah...hah... |
| 0x7dcc | 8 | HA-CHOO! |
| 0x7dd5 | 20 | Urgh... S-So cold... |
| 0x7dee | 7 | ...Huh? |
| 0x7df6 | 32 | I blink at the unfamiliar sight. |
| 0x7e17 | 17 | Wh-Where... am I? |
| 0x7e29 | 48 | I glance around. Trees, trees, and more trees.\n |
| 0x7e5a | 46 | It's a forest, and a pretty dense one at that. |
| 0x7e89 | 48 | It feels like the endless trees are swallowing\n |
| 0x7eba | 33 | everything else up... even sound. |
| 0x7edc | 25 | Where... exactly am I...? |
| 0x7ef6 | 41 | How did I end up in a place like this...? |
| 0x7f20 | 14 | Why...? Why... |
| 0x7f2f | 33 | I frantically search my memories. |
| 0x7f51 | 46 | Ngh... It's no use. Can't remember. What was\n |
| 0x7f80 | 24 | I doing up until now...? |
| 0x7f99 | 4 | Gah! |
| 0x7f9e | 50 | A sudden pain in my foot interrupts my thoughts.\n |
| 0x7fd1 | 40 | I look down and realize... I'm barefoot. |
| 0x7ffa | 7 | Why...? |
| 0x8002 | 8 | Ha-choo! |
| 0x800b | 21 | Gah, it's freezing... |
| 0x8021 | 24 | Why am I... No, hold on. |
| 0x803a | 30 | Why am I dressed like this...? |
| 0x8059 | 43 | Out in this cold, in just a flimsy gown...? |
| 0x8085 | 26 | Not even any underpants... |
| 0x80a0 | 45 | H-Hurgh... "Chilly"... d-doesn't even begin\n |
| 0x80ce | 15 | to describe it. |
| 0x80de | 50 | I look around, desperate for some way to get out\n |
| 0x8111 | 13 | of this cold. |
| 0x811f | 46 | Not a single house or a signpost anywhere...   |
| 0x814e | 14 | Gah... Urgh... |
| 0x815d | 47 | My head is splitting, too... Probably related\n |
| 0x818d | 21 | to the empty stomach. |
| 0x81a3 | 38 | Ah, right. This is all just a dream... |
| 0x81ca | 49 | ...Dammit, it's no use. I can't fool myself here. |
| 0x81fc | 46 | Somehow, I pull myself together and get back\n |
| 0x822b | 11 | to my feet. |
| 0x8237 | 45 | No matter how I look at it, this is no dream. |
| 0x8265 | 21 | ...Ha-choo! Bwa-CHOO! |
| 0x827b | 46 | Hurgh... Stuck out in this cold with nothing\n |
| 0x82aa | 44 | but a robe, and totally naked underneath it. |
| 0x82d7 | 51 | I'm still holding up, but once the sun goes down,\n |
| 0x830b | 48 | I'll catch cold for sure. Worst-case scenario,\n |
| 0x833c | 21 | I'll freeze to death. |
| 0x8352 | 51 | If this isn't a dream, then that tent where I was\n |
| 0x8386 | 37 | resting has to be out here somewhere. |
| 0x83ac | 48 | All things considered, that's probably my best\n |
| 0x83dd | 12 | shot here... |
| 0x83ea | 48 | I want to go back the way I came, but I've got\n |
| 0x841b | 31 | no idea which way that even is. |
| 0x843b | 49 | What do I do? Should I just... follow some road\n |
| 0x846d | 45 | and hope for the best? Or wait here for help? |
| 0x849b | 48 | If you get lost, rule one is to stay still and\n |
| 0x84cc | 34 | wait for help. But the thing is... |
| 0x84ef | 47 | I don't even know if anyone's coming for me...  |
| 0x851f | 49 | Can't really expect a search party when I don't\n |
| 0x8551 | 46 | even know what the hell I'm doing here myself. |
| 0x8580 | 43 | I guess I'll have to risk it if I want to\n |
| 0x85ac | 16 | get out of here. |
| 0x85bd | 46 | I should get moving before it gets any darker. |
| 0x85ec | 4 | Huh? |
| 0x85f1 | 47 | I feel a shiver run down my spine... but this\n |
| 0x8621 | 23 | time it's not the cold. |
| 0x8639 | 35 | What...? Something felt... weird... |
| 0x865d | 22 | ...Whoa! Wh-What the-- |
| 0x8674 | 49 | Oh... just a bird... Phew. Geez, almost gave me\n |
| 0x86a6 | 15 | a heart attack. |
| 0x86b6 | 33 | Nothing serious. What a relief... |
| 0x86d8 | 43 | Overhead, the birds are still screeching.\n |
| 0x8704 | 45 | They seem pretty worked up about something... |
| 0x8732 | 47 | ...These birds just won't shut up. What's got\n |
| 0x8762 | 23 | them so freaked out...? |
| 0x877a | 8 | *Shiver* |
| 0x8783 | 21 | ...There it is again. |
| 0x8799 | 41 | It feels like... something's watching me. |
| 0x87c3 | 25 | Urgh... I... feel sick... |
| 0x87dd | 41 | My vision blurs, and I lose my balance.\n |
| 0x8807 | 44 | I trip on my own feet, and stumble forward.  |
| 0x8834 | 21 | And in that instant-- |
| 0x884a | 6 | Whoa-- |
| 0x8851 | 8 | *Slash!* |
| 0x885a | 31 | I hear it just above my head.\n |
| 0x887a | 46 | A jarring, violent sound, like metal on metal. |
| 0x88a9 | 15 | Wh... Wh-Wha... |
| 0x88b9 | 47 | Fallen to one knee, I shift around cautiously\n |
| 0x88e9 | 13 | to look back. |
| 0x88fa | 22 | What... is... this...? |
| 0x8911 | 44 | A row of sharp jags and points, like honed\n |
| 0x893e | 31 | blades, gleams in the cold air. |
| 0x895e | 40 | They're like scissors... or maybe a saw? |
| 0x8987 | 46 | But saws and scissors can't compare to THAT.\n |
| 0x89b6 | 31 | It's bigger than a human arm... |
| 0x89d6 | 11 | What the... |
| 0x89e2 | 17 | What... is THAT!? |
| 0x89f4 | 42 | Whatever it is, it's definitely insectoid. |
| 0x8a1f | 45 | But... this thing doesn't look like any bug\n |
| 0x8a4d | 15 | I've ever seen. |
| 0x8a5d | 42 | It's at least ten times... no, a hundred\n |
| 0x8a88 | 13 | times bigger. |
| 0x8a96 | 23 | What is... going on...? |
| 0x8aae | 51 | Revulsion wells up inside me, and my skin crawls.\n |
| 0x8ae2 | 41 | I just want to look away from this thing. |
| 0x8b0c | 37 | What do I do...? What should I do...? |
| 0x8b32 | 18 | Hh... Ah... Aaah-- |
| 0x8b45 | 48 | Without looking away, I jump off the cliffside\n |
| 0x8b76 | 15 | in front of me. |
| 0x8b86 | 45 | I feel that unnatural sharpness cut through\n |
| 0x8bb4 | 33 | the air just behind me as I leap. |
| 0x8bd6 | 7 | Aaaaah! |
| 0x8bde | 15 | I'm... flying!? |
| 0x8bee | 42 | For a moment, I'm soaring through the air. |
| 0x8c19 | 46 | I feel myself hit the slope, and tumble down\n |
| 0x8c48 | 20 | the snowy cliffside. |
| 0x8c5d | 5 | Guh-- |
| 0x8c63 | 49 | My back hits the ground hard. The impact knocks\n |
| 0x8c95 | 32 | the wind out of me, and I choke. |
| 0x8cb6 | 14 | Urgh... Ghh... |
| 0x8cc5 | 4 | Ghh! |
| 0x8cca | 48 | My body's screaming in agony, but I don't have\n |
| 0x8cfb | 45 | time. I stagger to my feet and start running. |
| 0x8d29 | 46 | What was that, what was that, what was that... |
| 0x8d58 | 24 | WHAT THE HELL WAS THAT!? |
| 0x8d71 | 41 | An insect that massive doesn't exist...\n |
| 0x8d9b | 30 | There's no way it COULD exist! |
| 0x8dba | 46 | So this has to be a dream! That was all just\n |
| 0x8de9 | 14 | some illusion! |
| 0x8df8 | 46 | I just have to turn and look... and I'll see\n |
| 0x8e27 | 34 | everyone smiling, waiting for me-- |
| 0x8e4a | 16 | And I look back. |
| 0x8e5b | 32 | Aaaaaargh! I-I-I-It's gonna...\n |
| 0x8e7c | 19 | It's gonna EAT me!! |
| 0x8e90 | 48 | I start zigzagging right and left, serpentine,\n |
| 0x8ec1 | 27 | trying to keep it guessing. |
| 0x8edd | 40 | Hh... hh... H-How far do I have to run!? |
| 0x8f06 | 28 | I-I can't... keep this up... |
| 0x8f23 | 33 | I keep running straight ahead. \n |
| 0x8f45 | 6 | But... |
| 0x8f4c | 5 | Wha-- |
| 0x8f52 | 34 | Something gives way under my heel. |
| 0x8f75 | 14 | Aaaaaaaaagghh! |
| 0x8f84 | 6 | Ghh... |
| 0x8f8b | 50 | Agh... Did I fall again...? Everything... hurts... |
| 0x8fbe | 49 | I shade my eyes with my hand, peering up at the\n |
| 0x8ff0 | 46 | light shining from above. Looks like a hole... |
| 0x901f | 45 | If that's where I fell from... Must've been\n |
| 0x904d | 32 | a bush or something hiding it... |
| 0x906e | 47 | It'll be tough, but if I climb the wall here,\n |
| 0x909e | 37 | maybe I can get back above ground...? |
| 0x90c4 | 47 | But even if I could get back up, that thing's\n |
| 0x90f4 | 27 | just going to eat me. So... |
| 0x9110 | 44 | Strangely enough, the walls are giving off\n |
| 0x913d | 45 | a faint glow. It's dim, but it's helping me\n |
| 0x916b | 14 | see the place. |
| 0x917a | 46 | It looks like some kind of cavern. There's a\n |
| 0x91a9 | 46 | tunnel that seems like it goes on for a while. |
| 0x91d8 | 46 | Well, if I can't go up, then I might as well\n |
| 0x9207 | 13 | go forward... |
| 0x9215 | 48 | Still, even with this dim glow, I can't really\n |
| 0x9246 | 35 | tell what it's like further inside. |
| 0x926a | 47 | Maybe it'd be safer to just wait here quietly\n |
| 0x929a | 12 | after all... |
| 0x92a7 | 6 | Ah...! |
| 0x92ae | 37 | ...That noise... It's getting closer. |
| 0x92d4 | 51 | If I hang around here, it'll only hunt me down...\n |
| 0x9308 | 17 | I can't stop now. |
| 0x931a | 42 | With my decision made, I step forth into\n |
| 0x9345 | 11 | the tunnel. |
| 0x9351 | 38 | Rrrgh... Why is this happening to me!? |
| 0x9378 | 28 | Ngh, hah... phew... hah...\n |
| 0x9395 | 38 | I don't feel it... chasing after me... |
| 0x93bc | 49 | I finally let myself sit, exhaustion and relief\n |
| 0x93ee | 12 | settling in. |
| 0x93fb | 46 | Hahh... I'm safe now... Th-This... should be\n |
| 0x942a | 17 | far... enough...  |
| 0x943c | 9 | *Shudder* |
| 0x9446 | 41 | I cringe instinctively. A sudden chill,\n |
| 0x9470 | 42 | unpleasantly familiar, runs down my spine. |
| 0x949b | 43 | My body freezes. I can't move, confronted\n |
| 0x94c7 | 36 | with something beyond understanding. |
| 0x94ec | 18 | Wh... Wh-Wh-Why... |
| 0x94ff | 16 | Why is it HERE!? |
| 0x9510 | 44 | The colossal insect is right in front of me. |
| 0x953d | 26 | Did this thing set me up!? |
| 0x9558 | 42 | But the specifics... don't really matter\n |
| 0x9583 | 8 | anymore. |
| 0x958c | 6 | Urgh-- |
| 0x9593 | 44 | It happens in an instant. My back's to the\n |
| 0x95c0 | 40 | wall, and any escape is blocked by its\n |
| 0x95e9 | 13 | sinuous body. |
| 0x95f7 | 18 | I... can't escape. |
| 0x960a | 46 | It creeps forward warily, as if it's learned\n |
| 0x9639 | 44 | its lesson from its failed attempts earlier. |
| 0x9666 | 46 | It leans in, close enough to pull me in with\n |
| 0x9695 | 39 | a single snap of its jaws... and stops. |
| 0x96bd | 6 | *Drip* |
| 0x96c4 | 48 | Something like saliva is dripping from its jaws. |
| 0x96f5 | 26 | Is this... where I die...? |
| 0x9710 | 45 | Like this... in this senseless situation...\n |
| 0x973e | 43 | eaten by whatever the hell this thing is... |
| 0x976a | 46 | The insect's jaws finally click open, gaping\n |
| 0x9799 | 14 | to devour me.  |
| 0x97a8 | 10 | I'm dead-- |
| 0x97b3 | 29 | *Drip*... *Drip*... *Drip*... |
| 0x97d6 | 48 | The insect suddenly darts aside without biting\n |
| 0x9807 | 43 | me, like it's trying to escape something... |
| 0x9833 | 43 | ...and something descends from far above,\n |
| 0x985f | 41 | translucent and massive, as if to crush\n |
| 0x9889 | 17 | whatever's below. |
| 0x989b | 43 | It engulfs the massive insect effortlessly. |
| 0x98c7 | 14 | What... the... |
| 0x98d6 | 46 | What is that...? Wh-What's... going on now...? |
| 0x9905 | 46 | I can see the insect writhing and thrashing,\n |
| 0x9934 | 42 | trapped inside its slick, gelatinous body. |
| 0x995f | 46 | The insect was already beyond comprehension,\n |
| 0x998e | 43 | but this thing... defies all reason. And... |
| 0x99ba | 16 | It's melting...? |
| 0x99cb | 46 | This enormous insect's shell, hard as metal,\n |
| 0x99fa | 40 | is bubbling like it's being dissolved.\n |
| 0x9a23 | 35 | It's coming apart inside the slime. |
| 0x9a47 | 23 | Is it... eating the...? |
| 0x9a5f | 46 | The insect struggles desperately inside this\n |
| 0x9a8e | 44 | amorphous creature, but its body is almost\n |
| 0x9abb | 20 | completely digested. |
| 0x9ad0 | 46 | All I can do is stare blankly, still in shock. |
| 0x9aff | 44 | The insect's face surfaces for an instant,\n |
| 0x9b2c | 43 | but it has no power left. The viscous red\n |
| 0x9b58 | 15 | swallows it up. |
| 0x9b68 | 16 | ...Am I... safe? |
| 0x9b79 | 47 | I whisper, in sheer gratitude for still being\n |
| 0x9ba9 | 6 | alive. |
| 0x9bb0 | 14 | I... surviv--! |
| 0x9bbf | 46 | I can't keep myself from letting out a cheer\n |
| 0x9bee | 30 | of relief... until I realize.  |
| 0x9c0d | 43 | The amorphous creature swells and heaves,\n |
| 0x9c39 | 22 | a short distance away. |
| 0x9c50 | 46 | If it's somehow still hungry after that huge\n |
| 0x9c7f | 46 | insect, there's no reason it won't go for me\n |
| 0x9cae | 5 | next. |
| 0x9cb4 | 35 | I need to get out of here, before-- |
| 0x9cd8 | 6 | ...Ah! |
| 0x9cdf | 49 | The amorphous creature begins oozing forward...\n |
| 0x9d11 | 11 | towards me. |
| 0x9d1d | 45 | It stops. Just waiting... like it's curious\n |
| 0x9d4b | 22 | to see what I do next. |
| 0x9d62 | 6 | Ngh... |
| 0x9d69 | 47 | Can it hear me? Is it going off vibrations in\n |
| 0x9d99 | 47 | the ground? Any sudden movements, and I'm dead. |
| 0x9dc9 | 44 | No motion. I keep perfectly still, holding\n |
| 0x9df6 | 10 | my breath. |
| 0x9e03 | 38 | Its viscous surface begins rippling... |
| 0x9e2a | 41 | ...and little by little, reforms into a\n |
| 0x9e54 | 15 | familiar shape. |
| 0x9e64 | 6 | Wha--? |
| 0x9e6b | 27 | My voice dies in my throat. |
| 0x9e87 | 58 | The face that appears before me is misshapen, glutinous,\n |
| 0x9ec2 | 37 | horrifying... but unmistakably human. |
| 0x9ee8 | 46 | Unfocused eyes fixate on me. Its mouth gasps\n |
| 0x9f17 | 45 | and gapes soundlessly, like a fish drowning\n |
| 0x9f45 | 7 | in air. |
| 0x9f4d | 22 | What... are... you...? |
| 0x9f64 | 14 | ...hh... yh... |
| 0x9f73 | 44 | Is it... trying to talk...? It just sounds\n |
| 0x9fa0 | 42 | like air escaping--I can't make out what\n |
| 0x9fcb | 12 | it's saying. |
| 0x9fd8 | 15 | ...khh... yh... |
| 0x9fe8 | 45 | By reflex or by curiosity, I move closer to\n |
| 0xa016 | 44 | hear what it's saying... and another voice\n |
| 0xa043 | 10 | rings out. |
| 0xa04e | 25 | Cover your eyes and ears! |
| 0xa068 | 48 | The sharp command is followed by a cylindrical\n |
| 0xa099 | 42 | object bouncing on the stone between us.\n |
| 0xa0c4 | 12 | Looks like-- |
| 0xa0d1 | 19 | A grenade...? Gah!? |
| 0xa0e5 | 49 | I instinctively shut my eyes, and clap my hands\n |
| 0xa117 | 13 | over my ears. |
| 0xa125 | 30 | ------------------gghhh------! |
| 0xa144 | 43 | It's too bright to make anything out, but\n |
| 0xa170 | 46 | I feel the ground shake as if the creature's\n |
| 0xa19f | 9 | writhing. |
| 0xa1a9 | 17 | Is... Is this...? |
| 0xa1bb | 15 | A sudden grasp. |
| 0xa1cb | 7 | Huh...? |
| 0xa1d3 | 49 | Someone grabs my hand with an incredible force,\n |
| 0xa205 | 45 | and when I try to pull away, I get yelled at. |
| 0xa233 | 24 | You can freeze up later! |
| 0xa24c | 34 | My body's floating in the air...\n |
| 0xa26f | 31 | It feels like I'm flying again. |
| 0xa28f | 43 | I nervously open my eyes, and see someone\n |
| 0xa2bb | 36 | bounding forward, my hand in theirs. |
| 0xa2e0 | 17 | It's so fast...\n |
| 0xa2f2 | 25 | It's like we're the wind. |
| 0xa30c | 44 | We cut through the air, and the wind roars\n |
| 0xa339 | 13 | past my ears. |
| 0xa347 | 47 | My rescuer glances back to me, as if checking\n |
| 0xa377 | 7 | on me.  |
| 0xa37f | 11 | A... woman? |
| 0xa38b | 29 | No... more like a young lady? |
| 0xa3a9 | 47 | Her face is beautiful, though oddly childish.\n |
| 0xa3d9 | 36 | Oversized ears... And a fluffy tail. |
| 0xa3fe | 42 | There's something... ethereal about her.\n |
| 0xa429 | 18 | I can't look away. |
| 0xa43c | 45 | Even in this incredible situation, it feels\n |
| 0xa46a | 20 | like time's stopped. |
| 0xa47f | 33 | Then, suddenly, her brow furrows. |
| 0xa4a1 | 49 | I glance back, unsure of what she's looking at... |
| 0xa4d3 | 7 | Aaagh-- |
| 0xa4db | 49 | That amorphous creature surges forward, closing\n |
| 0xa50d | 42 | in on us like some kind of predatory wave. |
| 0xa538 | 45 | In this linear cavern, there's nowhere else\n |
| 0xa566 | 7 | to run. |
| 0xa56e | 22 | It's gonna catch up--! |
| 0xa585 | 43 | But the girl's already seen it. She whips\n |
| 0xa5b1 | 38 | another cylinder from her waist, and\n |
| 0xa5d8 | 20 | throws it behind us. |
| 0xa5ed | 45 | The blinding flash and the explosion follow\n |
| 0xa61b | 17 | almost instantly. |
| 0xa62d | 31 | ------------------rngghh------! |
| 0xa64d | 9 | Gyaaaagh! |
| 0xa657 | 17 | Now's our chance! |
| 0xa669 | 21 | Hahh... hh... hahh... |
| 0xa67f | 38 | We're outside... I-I'm finally safe... |
| 0xa6a6 | 45 | My legs give out. I collapse onto the snowy\n |
| 0xa6d4 | 7 | ground. |
| 0xa6dc | 45 | I can barely even believe I was able to run\n |
| 0xa70a | 17 | as much as I did. |
| 0xa71c | 44 | I guess humans really can do anything when\n |
| 0xa749 | 30 | their lives are on the line... |
| 0xa768 | 45 | The girl's exhausted too--can't blame her--\n |
| 0xa796 | 42 | and she takes a seat, catching her breath. |
| 0xa7c1 | 43 | ...She saved my life... I should at least\n |
| 0xa7ed | 19 | thank her properly. |
| 0xa801 | 37 | Th-Thank you so much for saving me... |
| 0xa827 | 46 | Did she even hear me? My throat is raspy and\n |
| 0xa856 | 36 | raw, and I can't speak up that well. |
| 0xa87b | 34 | She notices, and turns towards me. |
| 0xa89e | 48 | She has a strange look on her face, like she's\n |
| 0xa8cf | 39 | seen something she wasn't expecting to. |
| 0xa8f7 | 42 | Ah... Seeing her face again like this...\n |
| 0xa922 | 46 | There really is something beautiful about her. |
| 0xa951 | 43 | That slightly confused expression, too...\n |
| 0xa97d | 16 | Wow, she's cute. |
| 0xa98e | 4 | Girl |
| 0xa993 | 38 | Is there something wrong with my face? |
| 0xa9ba | 24 | O-Oh, no, not really...  |
| 0xa9d3 | 14 | Still, though. |
| 0xa9e2 | 46 | I take my eyes off you for just a moment and\n |
| 0xaa11 | 47 | you disappear, but I never imagined something\n |
| 0xaa41 | 10 | like this. |
| 0xaa4c | 50 | I'm glad I made it in time, but in the future...\n |
| 0xaa7f | 47 | I think I'd prefer you don't cause me so much\n |
| 0xaaaf | 9 | trouble.  |
| 0xaab9 | 18 | Urgh... I'm sorry. |
| 0xaacc | 6 | ...Hm? |
| 0xaad3 | 32 | Wait, take her eyes off me...?\n |
| 0xaaf4 | 18 | And I disappeared? |
| 0xab07 | 50 | What does she mean by that? She seems somehow...\n |
| 0xab3a | 16 | familiar, too... |
| 0xab4b | 36 | Does that mean you know who I am...? |
| 0xab70 | 48 | If you know who I am, where I'm from, please--\n |
| 0xaba1 | 8 | tell me. |
| 0xabaa | 13 | Huh...? Oh... |
| 0xabb8 | 43 | Who am I? Where am I? What was that thing\n |
| 0xabe4 | 41 | that attacked me? What was--I mean, how-- |
| 0xac0e | 43 | Ngh... I'm trying to ask all my questions\n |
| 0xac3a | 42 | at once, and none of them are coming out\n |
| 0xac65 | 6 | right. |
| 0xac6c | 5 | I'm-- |
| 0xac72 | 46 | The girl stands with a troubled smile on her\n |
| 0xaca1 | 33 | face, and extends her hand to me. |
| 0xacc3 | 28 | We should head back for now. |
| 0xace0 | 41 | If you stay out here dressed like that,\n |
| 0xad0a | 35 | you're going to end up with a cold. |
| 0xad2e | 11 | Dressed...? |
| 0xad3a | 45 | The cold air hits me all at once again, and\n |
| 0xad68 | 36 | I finally remember the state I'm in. |
| 0xad8d | 41 | Come to think of it, have I really been\n |
| 0xadb7 | 43 | flailing around this whole forest in this\n |
| 0xade3 | 16 | flimsy thing...? |
| 0xadf4 | 15 | Hah... Ha-CHOO! |
| 0xae04 | 11 | ...Hee hee. |
| 0xae10 | 47 | She lets out a laugh, clear as a bell, at the\n |
| 0xae40 | 46 | sound of my sneeze echoing through the forest. |
| 0xae6f | 5 | Here. |
| 0xae75 | 52 | She takes my hand with her pale, delicate fingers,\n |
| 0xaeaa | 25 | and pulls me to my feet.  |
| 0xaec4 | 9 | Let's go. |
| 0xaece | 8 | H-Hey... |
| 0xaed7 | 49 | I shift my hand slightly, squeezing back at her\n |
| 0xaf09 | 34 | grip. That lone touch of warmth... |
| 0xaf2c | 48 | ...I couldn't have known what lay ahead of us.\n |
| 0xaf5d | 33 | That this was only the beginning. |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_01.json` com a forma:
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
