# Cena ch_11_06 — pacote de traducao (146 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `...Just how long have we been walking...?` -> `...Faz quanto tempo que a gente tá andando...?` (Haku, 11_06)
- `The sun is dipping toward the horizon, but the\n` -> `O sol está caindo na direção do horizonte, mas a\n` (Haku, 11_06)
- `village Kuon mentioned is nowhere in sight.` -> `vila que a Kuon mencionou não aparece em lugar nenhum.` (Haku, 11_06)
- `It feels like we've been walking for miles, but Kuon\n` -> `Parece que a gente andou quilômetros, mas a Kuon\n` (Haku, 11_06)
- `looks like she hasn't even broken a sweat.` -> `parece que nem suou.` (Haku, 11_06)
- `She's been hiking at quite a clip, too.` -> `E ainda por cima vem num ritmo e tanto.` (Haku, 11_06)
- `Me, on the other hand...` -> `Eu, por outro lado...` (Haku, 11_06)
- `Huff... hah... hah... Nnnngh...` -> `Uf... haah... haah... Nnnngh...` (Haku, 11_06)
- `I don't exactly have much stamina to begin with,\n` -> `Eu já não tenho lá muita energia pra começo de conversa,\n` (Haku, 11_06)
- `but on top of that...` -> `mas ainda por cima disso...` (Haku, 11_06)
- `M-My feet...` -> `M-Meus pés...` (Haku, 11_06)
- `I drag my feet as I walk. They're as heavy as lead.` -> `Arrasto os pés enquanto ando. Estão pesados como chumbo.` (Haku, 11_06)
- `But I can't exactly complain when a girl half my size\n` -> `Mas não dá bem pra reclamar quando uma garota da metade do meu tamanho\n` (Haku, 11_06)
- `is keeping pace effortlessly.` -> `acompanha o ritmo sem esforço.` (Haku, 11_06)
- `I shouldn't whine, but...` -> `Eu não devia choramingar, mas...` (Haku, 11_06)
- `H-Hey, Kuon?` -> `E-Ei, Kuon?` (Haku, 11_06)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Kuon glances over her shoulder without stopping.` -> `A Kuon olha por cima do ombro sem parar.` (Haku, 11_06)
- `Uh... How should I put this? We've been walking for\n` -> `Ahn... Como é que eu digo? A gente tá andando faz\n` (Haku, 11_06)
- `a while now, and, um... Is the village close?` -> `um tempão já, e, hum... A vila tá perto?` (Haku, 11_06)
- `Mm, almost. We should be coming up on it soon--just\n` -> `Hum, quase. A gente já deve chegar logo--só\n` (Kuon, 11_06)
- `a little further, I think.` -> `mais um pouquinho, acho.` (Kuon, 11_06)
- `R-Really?` -> `S-Sério?` (Haku, 11_06)
- `Just a little further.\n` -> `Só mais um pouquinho.\n` (Kuon, 11_06)
- `...She really DOES mean just a little, right?` -> `...Ela quer dizer MESMO só um pouquinho, né?` (Haku, 11_06)
- `I'm starting to figure out that my sense of scale\n` -> `Tô começando a perceber que minha noção de distância\n` (Haku, 11_06)
- `is way different from Kuon's.` -> `é bem diferente da da Kuon.` (Haku, 11_06)
- `Hah... haahhh... Finally... We m-made it...` -> `Haah... haahhh... Finalmente... A gente c-conseguiu...` (Haku, 11_06)
- `I fall to the ground as soon as we cross the\n` -> `Desabo no chão assim que a gente cruza a\n` (Haku, 11_06)
- `threshold, my legs sore beyond reason.` -> `entrada, com as pernas doloridas além da conta.` (Haku, 11_06)
- `I made it. You go, me. You done good.` -> `Consegui. Isso aí, eu. Mandou bem.` (Haku, 11_06)
- `It should be OK to praise myself for making it\n` -> `Acho que posso me elogiar por ter chegado\n` (Haku, 11_06)
- `this far, right? I pushed myself the whole way...` -> `até aqui, né? Me esforcei o caminho todo...` (Haku, 11_06)
- `Hey, you didn't push yourself too hard, right?` -> `Ei, você não se esforçou demais, né?` (Kuon, 11_06)
- `Kuon looks over at me with concern as I sit on the\n` -> `A Kuon me olha preocupada enquanto eu sento no\n` (Haku, 11_06)
- `ground, exhausted.` -> `chão, exausto.` (Haku, 11_06)
- `Huh? N-No, not at all. I'm good. Totally fine.` -> `Hein? N-Não, que nada. Tô bem. Numa boa.` (Haku, 11_06)
- `I stand up in a hurry, denying her accusation.` -> `Levanto às pressas, negando a acusação dela.` (Haku, 11_06)
- `She's choosing these moments to sound so concerned\n` -> `Ela escolhe esses momentos pra soar tão preocupada\n` (Haku, 11_06)
- `deliberately, isn't she? Makes it hard to feel good\n` -> `de propósito, né? Fica difícil me sentir bem\n` (Haku, 11_06)
- `about whining.` -> `em choramingar.` (Haku, 11_06)
- `Really? Let's keep going, then. Not much further to\n` -> `É mesmo? Então vamos seguindo. Não falta muito pra\n` (Kuon, 11_06)
- `go, promise.` -> `chegar, prometo.` (Kuon, 11_06)
- `With that, Kuon smiles mischievously and turns back\n` -> `Com isso, a Kuon sorri travessa e volta\n` (Haku, 11_06)
- `to the path, moving onward.` -> `pro caminho, seguindo em frente.` (Haku, 11_06)
- `...She isn't doing this on purpose... right?` -> `...Ela não tá fazendo isso de propósito... né?` (Haku, 11_06)
- `The road is a simple dirt one, probably common in\n` -> `A estrada é de terra simples, provavelmente comum em\n` (Haku, 11_06)
- `rural villages like this...` -> `vilarejos rurais como este...` (Haku, 11_06)
- `Patches of snow still adorn the town. It looks...\n` -> `Restos de neve ainda enfeitam a vila. Parece...\n` (Haku, 11_06)
- `Not rich, honestly, but probably comfortable to\n` -> `Não rica, sinceramente, mas provavelmente confortável de\n` (Haku, 11_06)
- `live in. Pastoral.` -> `se viver. Bucólica.` (Haku, 11_06)
- `Here we are!` -> `Chegamos!` (Kuon, 11_06)
- `Kuon comes to a stop at an old building, a colorful\n` -> `A Kuon para num prédio velho, com um pano\n` (Haku, 11_06)
- `piece of cloth hanging from its eaves.` -> `colorido pendurado no beiral.` (Haku, 11_06)
- `What's this place?` -> `Que lugar é esse?` (Haku, 11_06)
- `An inn. Places with this mark are always inns--\n` -> `Uma estalagem. Lugares com essa marca são sempre estalagens--\n` (Kuon, 11_06)
- `it'd probably be good for you to remember that.` -> `seria bom você guardar isso.` (Kuon, 11_06)
- `She indicates the pattern on the hanging strip of\n` -> `Ela aponta o padrão na tira de pano\n` (Haku, 11_06)
- `fabric.` -> `pendurada.` (Haku, 11_06)
- `Inside is a large, open space, lined with tables--\n` -> `Lá dentro é um espaço amplo e aberto, cheio de mesas--\n` (Haku, 11_06)
- `probably meant to serve as a mess hall or tavern.` -> `provavelmente pra servir de refeitório ou taverna.` (Haku, 11_06)
- `It's a lot more colorful in here than I thought\n` -> `É bem mais colorido aqui dentro do que eu imaginava\n` (Haku, 11_06)
- `it'd be...` -> `que seria...` (Haku, 11_06)
- `While I glance around, Kuon makes for what looks\n` -> `Enquanto eu olho em volta, a Kuon vai até o que parece\n` (Haku, 11_06)
- `like a reception desk and pulls on a hanging cord.` -> `ser uma recepção e puxa um cordão pendurado.` (Haku, 11_06)
- `A voice from somewhere else in the building shouts\n` -> `Uma voz de algum outro canto do prédio grita\n` (Haku, 11_06)
- `"coming!" and soon a woman appears from another\n` -> `"já vou!" e logo uma mulher aparece de outro\n` (Haku, 11_06)
- `room.` -> `cômodo.` (Haku, 11_06)
- `Innkeeper` -> `Estalajadeira` (rotulo, 11_06)
- `Oh, Miss Kuon! Welcome back.` -> `Ah, Senhorita Kuon! Bem-vinda de volta.` (Estalajadeira, 11_06)
- `I'm sorry for not coming more quickly, dear. We've\n` -> `Desculpe não ter vindo mais rápido, querida. A gente tem\n` (Estalajadeira, 11_06)
- `been terribly busy, is all.` -> `andado terrivelmente ocupada, só isso.` (Estalajadeira, 11_06)
- `Please, don't worry about it. Here--these are the\n` -> `Por favor, não se preocupe. Aqui--essas são as\n` (Kuon, 11_06)
- `medicinal herbs you asked me to get. ` -> `ervas medicinais que você me pediu pra trazer. ` (Kuon, 11_06)
- `Oh! Thank you. You're a lifesaver, you are.` -> `Ah! Obrigada. Você é uma salvadora, isso sim.` (Estalajadeira, 11_06)
- `The innkeeper happily takes the pouch that Kuon\n` -> `A estalajadeira pega contente a bolsinha que a Kuon\n` (Haku, 11_06)
- `offers to her, weighing it with a scale.` -> `oferece, pesando numa balança.` (Haku, 11_06)
- `Hmm. Looks like it comes out to about 400--but I'll\n` -> `Hmm. Parece dar uns 400--mas vou\n` (Estalajadeira, 11_06)
- `throw in a bonus and make it 450, for you.` -> `jogar um bônus e fazer 450, pra você.` (Estalajadeira, 11_06)
- `Ah, thank you!` -> `Ah, obrigada!` (Kuon, 11_06)
- `I should be the one thanking you, dear. Our stock\n` -> `Eu é que devia agradecer, querida. Nosso estoque\n` (Estalajadeira, 11_06)
- `was nearly out. You really came just in time.` -> `tava quase no fim. Você chegou bem na hora.` (Estalajadeira, 11_06)
- `Please, don't worry about it. Just hearing you say\n` -> `Por favor, não se preocupe. Só de ouvir você dizer\n` (Kuon, 11_06)
- `that makes it all worth it.` -> `isso já valeu a pena.` (Kuon, 11_06)
- `Will you stay the night? The room we had for you\n` -> `Vai passar a noite? O quarto que a gente teve pra você\n` (Estalajadeira, 11_06)
- `last time is available.` -> `da última vez está livre.` (Estalajadeira, 11_06)
- `That would be fi--Oh, but there's two of us this\n` -> `Seria ótim--Ah, mas somos dois desta\n` (Kuon, 11_06)
- `time. Is that OK?` -> `vez. Tudo bem?` (Kuon, 11_06)
- `Two?` -> `Dois?` (Estalajadeira, 11_06)
- `Mhm. In the same room, if that's possible.` -> `Aham. No mesmo quarto, se for possível.` (Kuon, 11_06)
- `The innkeeper only just then seems to notice me,\n` -> `A estalajadeira só então parece me notar,\n` (Haku, 11_06)
- `giving me a puzzled look.` -> `me dando um olhar confuso.` (Haku, 11_06)
- `Wait, what was that she just said about being in\n` -> `Espera, o que foi isso que ela falou sobre ficar no\n` (Haku, 11_06)
- `the same room?` -> `mesmo quarto?` (Haku, 11_06)
- `It's a long story. I picked him up on my way back,\n` -> `É uma longa história. Eu o encontrei na volta,\n` (Kuon, 11_06)
- `basically.` -> `basicamente.` (Kuon, 11_06)
- `W-Wait, wait, hold on.` -> `E-Espera, espera, calma aí.` (Haku, 11_06)
- `Is something wrong?` -> `Algum problema?` (Kuon, 11_06)
- `Sharing a room with a guy? You sure you're OK with\n` -> `Dividir quarto com um cara? Você tem certeza que tá de boa com\n` (Haku, 11_06)
- `that? It's not weird?` -> `isso? Não é estranho?` (Haku, 11_06)
- `...Why would that be weird?` -> `...Por que isso seria estranho?` (Kuon, 11_06)
- `She's staring at me with genuine bewilderment.\n` -> `Ela me encara com genuína perplexidade.\n` (Haku, 11_06)
- `Is it really not that big a deal?` -> `Será que não é grande coisa mesmo?` (Haku, 11_06)
- `I mean, wouldn't you prefer to be on your own,\n` -> `Quer dizer, você não preferiria ficar sozinha,\n` (Haku, 11_06)
- `rather than bunk with a total stranger?` -> `em vez de dividir com um completo estranho?` (Haku, 11_06)
- `But you aren't a total stranger. Besides, we slept\n` -> `Mas você não é um completo estranho. Além disso, a gente dormiu\n` (Kuon, 11_06)
- `in the same tent while I was taking care of you.` -> `na mesma barraca enquanto eu cuidava de você.` (Kuon, 11_06)
- `So I figure, why make a big deal out of it now?` -> `Então eu acho: por que fazer disso um drama agora?` (Kuon, 11_06)
- `...Be that as it may, you aren't, like... worried\n` -> `...Mesmo assim, você não tá, tipo... preocupada\n` (Haku, 11_06)
- `you'll be watched while changing, or molested, or...` -> `de ser vigiada enquanto se troca, ou molestada, ou...` (Haku, 11_06)
- `Planning to molest me, Haku?` -> `Pensando em me molestar, Haku?` (Kuon, 11_06)
- `N-No, I didn't mean--Damn it, you know exactly what\n` -> `N-Não, eu não quis--Droga, você sabe exatamente o que\n` (Haku, 11_06)
- `I meant and you're just messing with me, aren't you?` -> `eu quis dizer e tá só me zoando, né?` (Haku, 11_06)
- `Whatever could you be talking about?` -> `Do que você poderia estar falando?` (Kuon, 11_06)
- `I knew it.` -> `Eu sabia.` (Haku, 11_06)
- `You don't seem the vulgar type, and I doubt you'd\n` -> `Você não parece do tipo vulgar, e duvido que fosse\n` (Kuon, 11_06)
- `bite the hand that fed you, so I'm not worried.` -> `morder a mão que te alimentou, então não tô preocupada.` (Kuon, 11_06)
- `We'll just hang up a piece of fabric or something\n` -> `A gente só pendura um pano ou algo assim\n` (Kuon, 11_06)
- `for privacy.` -> `pra ter privacidade.` (Kuon, 11_06)
- `Or is it that you just don't want to stay with me?` -> `Ou é que você simplesmente não quer ficar comigo?` (Kuon, 11_06)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `She's just trying to blindside me, now.` -> `Agora ela só tá tentando me pegar desprevenido.` (Haku, 11_06)
- `Maybe she does trust me, but I don't have a leg to\n` -> `Talvez ela confie em mim mesmo, mas eu não tenho como\n` (Haku, 11_06)
- `stand on to respond to a comment like that.` -> `responder a um comentário desses.` (Haku, 11_06)
- `Who do you think is paying for the room, anyway?\n` -> `Quem você acha que tá pagando o quarto, afinal?\n` (Kuon, 11_06)
- `It'd be wasteful to pay for two.` -> `Seria desperdício pagar por dois.` (Kuon, 11_06)
- `Just the one room, please.` -> `Só um quarto, por favor.` (Kuon, 11_06)
- `Sure thing. You must be tired, so why don't you go\n` -> `Pode deixar. Vocês devem estar cansados, então por que não vão\n` (Estalajadeira, 11_06)
- `take advantage of the baths? Relax for a while.` -> `aproveitar os banhos? Relaxem um pouco.` (Estalajadeira, 11_06)
- `I'll put my heart into making a good meal for you,\n` -> `Vou caprichar numa boa refeição pra vocês,\n` (Estalajadeira, 11_06)
- `so please look forward to dinner.` -> `então esperem ansiosos pelo jantar.` (Estalajadeira, 11_06)
- `We will! {W110}Before we do, though, do you have any chores\n` -> `Vamos sim! {W110}Mas antes, você tem alguma tarefa\n` (Kuon, 11_06)
- `around the inn you need taken care of?` -> `na estalagem que precisa ser feita?` (Kuon, 11_06)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Any menial labor or errands you have are fine, just\n` -> `Qualquer trabalho braçal ou recado serve, desde que\n` (Kuon, 11_06)
- `as long as we can get them done before dark.` -> `a gente consiga terminar antes de escurecer.` (Kuon, 11_06)
- `Don't tell me she's going to WORK after making that\n` -> `Não me diga que ela vai TRABALHAR depois daquela\n` (Haku, 11_06)
- `grueling hike. I don't get it. What's up with her\n` -> `caminhada brutal. Não entendo. Que história é a\n` (Haku, 11_06)
- `stamina?` -> `da energia dela?` (Haku, 11_06)
- `Well, let's see... It's getting late, so there's\n` -> `Bom, deixa ver... Está ficando tarde, então só\n` (Estalajadeira, 11_06)
- `really only the children's chores. Will that do?` -> `sobram mesmo as tarefas das crianças. Serve?` (Estalajadeira, 11_06)
- `Yes, that would be fine.` -> `Sim, serve perfeitamente.` (Kuon, 11_06)
- `But I'm already exhausted! Let me rest. Please.` -> `Mas eu já tô exausto! Me deixa descansar. Por favor.` (Haku, 11_06)
- `Kuon speaks with the innkeeper a while longer, then\n` -> `A Kuon conversa mais um pouco com a estalajadeira, então\n` (Haku, 11_06)
- `swishes her tail in my direction, smiling.` -> `balança o rabo na minha direção, sorrindo.` (Haku, 11_06)
- `All right, then. Let's get to work.` -> `Certo, então. Vamos trabalhar.` (Kuon, 11_06)
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
| 0x18463 | 41 | ...Just how long have we been walking...? |
| 0x1848d | 48 | The sun is dipping toward the horizon, but the\n |
| 0x184be | 43 | village Kuon mentioned is nowhere in sight. |
| 0x184ea | 54 | It feels like we've been walking for miles, but Kuon\n |
| 0x18521 | 42 | looks like she hasn't even broken a sweat. |
| 0x1854c | 39 | She's been hiking at quite a clip, too. |
| 0x18574 | 24 | Me, on the other hand... |
| 0x1858d | 31 | Huff... hah... hah... Nnnngh... |
| 0x185ad | 50 | I don't exactly have much stamina to begin with,\n |
| 0x185e0 | 21 | but on top of that... |
| 0x185f6 | 12 | M-My feet... |
| 0x18603 | 51 | I drag my feet as I walk. They're as heavy as lead. |
| 0x18637 | 55 | But I can't exactly complain when a girl half my size\n |
| 0x1866f | 29 | is keeping pace effortlessly. |
| 0x1868d | 25 | I shouldn't whine, but... |
| 0x186a7 | 12 | H-Hey, Kuon? |
| 0x186b4 | 3 | Hm? |
| 0x186b8 | 48 | Kuon glances over her shoulder without stopping. |
| 0x186e9 | 53 | Uh... How should I put this? We've been walking for\n |
| 0x1871f | 45 | a while now, and, um... Is the village close? |
| 0x1874d | 53 | Mm, almost. We should be coming up on it soon--just\n |
| 0x18783 | 26 | a little further, I think. |
| 0x1879e | 9 | R-Really? |
| 0x187a8 | 24 | Just a little further.\n |
| 0x187c1 | 45 | ...She really DOES mean just a little, right? |
| 0x187ef | 51 | I'm starting to figure out that my sense of scale\n |
| 0x18823 | 29 | is way different from Kuon's. |
| 0x18841 | 43 | Hah... haahhh... Finally... We m-made it... |
| 0x1886d | 46 | I fall to the ground as soon as we cross the\n |
| 0x1889c | 38 | threshold, my legs sore beyond reason. |
| 0x188c3 | 37 | I made it. You go, me. You done good. |
| 0x188e9 | 48 | It should be OK to praise myself for making it\n |
| 0x1891a | 49 | this far, right? I pushed myself the whole way... |
| 0x1894c | 46 | Hey, you didn't push yourself too hard, right? |
| 0x1897b | 52 | Kuon looks over at me with concern as I sit on the\n |
| 0x189b0 | 18 | ground, exhausted. |
| 0x189c3 | 46 | Huh? N-No, not at all. I'm good. Totally fine. |
| 0x189f2 | 46 | I stand up in a hurry, denying her accusation. |
| 0x18a21 | 52 | She's choosing these moments to sound so concerned\n |
| 0x18a56 | 53 | deliberately, isn't she? Makes it hard to feel good\n |
| 0x18a8c | 14 | about whining. |
| 0x18a9b | 53 | Really? Let's keep going, then. Not much further to\n |
| 0x18ad1 | 12 | go, promise. |
| 0x18ade | 53 | With that, Kuon smiles mischievously and turns back\n |
| 0x18b14 | 27 | to the path, moving onward. |
| 0x18b30 | 44 | ...She isn't doing this on purpose... right? |
| 0x18b5d | 51 | The road is a simple dirt one, probably common in\n |
| 0x18b91 | 27 | rural villages like this... |
| 0x18bad | 51 | Patches of snow still adorn the town. It looks...\n |
| 0x18be1 | 49 | Not rich, honestly, but probably comfortable to\n |
| 0x18c13 | 18 | live in. Pastoral. |
| 0x18c26 | 12 | Here we are! |
| 0x18c33 | 53 | Kuon comes to a stop at an old building, a colorful\n |
| 0x18c69 | 38 | piece of cloth hanging from its eaves. |
| 0x18c90 | 18 | What's this place? |
| 0x18ca3 | 49 | An inn. Places with this mark are always inns--\n |
| 0x18cd5 | 47 | it'd probably be good for you to remember that. |
| 0x18d05 | 51 | She indicates the pattern on the hanging strip of\n |
| 0x18d39 | 7 | fabric. |
| 0x18d41 | 52 | Inside is a large, open space, lined with tables--\n |
| 0x18d76 | 49 | probably meant to serve as a mess hall or tavern. |
| 0x18da8 | 49 | It's a lot more colorful in here than I thought\n |
| 0x18dda | 10 | it'd be... |
| 0x18de5 | 50 | While I glance around, Kuon makes for what looks\n |
| 0x18e18 | 50 | like a reception desk and pulls on a hanging cord. |
| 0x18e4b | 52 | A voice from somewhere else in the building shouts\n |
| 0x18e80 | 49 | "coming!" and soon a woman appears from another\n |
| 0x18eb2 | 5 | room. |
| 0x18eb8 | 9 | Innkeeper |
| 0x18ec2 | 28 | Oh, Miss Kuon! Welcome back. |
| 0x18edf | 52 | I'm sorry for not coming more quickly, dear. We've\n |
| 0x18f14 | 27 | been terribly busy, is all. |
| 0x18f30 | 51 | Please, don't worry about it. Here--these are the\n |
| 0x18f64 | 37 | medicinal herbs you asked me to get.  |
| 0x18f8a | 43 | Oh! Thank you. You're a lifesaver, you are. |
| 0x18fb6 | 49 | The innkeeper happily takes the pouch that Kuon\n |
| 0x18fe8 | 40 | offers to her, weighing it with a scale. |
| 0x19011 | 53 | Hmm. Looks like it comes out to about 400--but I'll\n |
| 0x19047 | 42 | throw in a bonus and make it 450, for you. |
| 0x19072 | 14 | Ah, thank you! |
| 0x19081 | 51 | I should be the one thanking you, dear. Our stock\n |
| 0x190b5 | 45 | was nearly out. You really came just in time. |
| 0x190e3 | 52 | Please, don't worry about it. Just hearing you say\n |
| 0x19118 | 27 | that makes it all worth it. |
| 0x19134 | 50 | Will you stay the night? The room we had for you\n |
| 0x19167 | 23 | last time is available. |
| 0x1917f | 50 | That would be fi--Oh, but there's two of us this\n |
| 0x191b2 | 17 | time. Is that OK? |
| 0x191c4 | 4 | Two? |
| 0x191c9 | 42 | Mhm. In the same room, if that's possible. |
| 0x191f4 | 50 | The innkeeper only just then seems to notice me,\n |
| 0x19227 | 25 | giving me a puzzled look. |
| 0x19241 | 50 | Wait, what was that she just said about being in\n |
| 0x19274 | 14 | the same room? |
| 0x19283 | 52 | It's a long story. I picked him up on my way back,\n |
| 0x192b8 | 10 | basically. |
| 0x192c3 | 22 | W-Wait, wait, hold on. |
| 0x192da | 19 | Is something wrong? |
| 0x192ee | 52 | Sharing a room with a guy? You sure you're OK with\n |
| 0x19323 | 21 | that? It's not weird? |
| 0x19339 | 27 | ...Why would that be weird? |
| 0x19355 | 48 | She's staring at me with genuine bewilderment.\n |
| 0x19386 | 33 | Is it really not that big a deal? |
| 0x193a8 | 48 | I mean, wouldn't you prefer to be on your own,\n |
| 0x193d9 | 39 | rather than bunk with a total stranger? |
| 0x19401 | 52 | But you aren't a total stranger. Besides, we slept\n |
| 0x19436 | 48 | in the same tent while I was taking care of you. |
| 0x19467 | 47 | So I figure, why make a big deal out of it now? |
| 0x19497 | 51 | ...Be that as it may, you aren't, like... worried\n |
| 0x194cb | 52 | you'll be watched while changing, or molested, or... |
| 0x19500 | 28 | Planning to molest me, Haku? |
| 0x1951d | 53 | N-No, I didn't mean--Damn it, you know exactly what\n |
| 0x19553 | 52 | I meant and you're just messing with me, aren't you? |
| 0x19588 | 36 | Whatever could you be talking about? |
| 0x195ad | 10 | I knew it. |
| 0x195b8 | 51 | You don't seem the vulgar type, and I doubt you'd\n |
| 0x195ec | 47 | bite the hand that fed you, so I'm not worried. |
| 0x1961c | 51 | We'll just hang up a piece of fabric or something\n |
| 0x19650 | 12 | for privacy. |
| 0x1965d | 50 | Or is it that you just don't want to stay with me? |
| 0x19690 | 7 | Urgh... |
| 0x19698 | 39 | She's just trying to blindside me, now. |
| 0x196c0 | 52 | Maybe she does trust me, but I don't have a leg to\n |
| 0x196f5 | 43 | stand on to respond to a comment like that. |
| 0x19721 | 50 | Who do you think is paying for the room, anyway?\n |
| 0x19754 | 32 | It'd be wasteful to pay for two. |
| 0x19779 | 26 | Just the one room, please. |
| 0x19794 | 52 | Sure thing. You must be tired, so why don't you go\n |
| 0x197c9 | 47 | take advantage of the baths? Relax for a while. |
| 0x197f9 | 52 | I'll put my heart into making a good meal for you,\n |
| 0x1982e | 33 | so please look forward to dinner. |
| 0x19850 | 61 | We will! {W110}Before we do, though, do you have any chores\n |
| 0x1988e | 38 | around the inn you need taken care of? |
| 0x198b5 | 4 | Huh? |
| 0x198ba | 53 | Any menial labor or errands you have are fine, just\n |
| 0x198f0 | 44 | as long as we can get them done before dark. |
| 0x1991d | 53 | Don't tell me she's going to WORK after making that\n |
| 0x19953 | 51 | grueling hike. I don't get it. What's up with her\n |
| 0x19987 | 8 | stamina? |
| 0x19990 | 50 | Well, let's see... It's getting late, so there's\n |
| 0x199c3 | 48 | really only the children's chores. Will that do? |
| 0x199f4 | 24 | Yes, that would be fine. |
| 0x19a0d | 47 | But I'm already exhausted! Let me rest. Please. |
| 0x19a3d | 53 | Kuon speaks with the innkeeper a while longer, then\n |
| 0x19a73 | 42 | swishes her tail in my direction, smiling. |
| 0x19a9e | 35 | All right, then. Let's get to work. |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_06.json` com a forma:
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
