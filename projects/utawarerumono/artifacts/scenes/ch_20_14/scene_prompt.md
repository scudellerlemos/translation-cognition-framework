# Cena ch_20_14 — pacote de traducao (199 linhas)

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
| Bokoinante | Personagem | Bokoinante | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nakwan | Termo | Nakwan | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Yamatan | Etnia | de Yamato | traduzir | none |

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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Meanwhile, in another area along the western\n` -> `Enquanto isso, em outra área ao longo do\n` (NARRADOR, 20_14)
- `border...` -> `fronteira...` (SYSTEM, 20_14)
- `An army lead by Dekopompo of the Eight Pillar\n` -> `Um exército liderado por Dekopompo, dos Oito Pilares,\n` (NARRADOR, 20_14)
- `Generals fights to stall the Uzurushan army.` -> `Generais batem para estancar o exército Uzurushan.` (Oshtor, 20_14)
- `Unlike the other battlefields, the two armies\n` -> `Ao contrário dos outros campos, os dois exércitos\n` (NARRADOR, 20_14)
- `here split into smaller units, skirmishing while\n` -> `se dividiram em unidades menores, escaramuçando enquanto\n` (NARRADOR, 20_14)
- `scattered...` -> `dispersos...` (SYSTEM, 20_14)
- `Reporting!` -> `Relatando!` (SOLDIER, 20_01)
- `Our soldiers have defeated the enemy unit that\n` -> `Nossos soldados derrotaram a unidade inimiga que\n` (NARRADOR, 20_14)
- `was approaching from our left!` -> `se aproximava do nosso lado esquerdo!` (Maroro, 20_14)
- `I see! Good. Good.` -> `Vejo! Bom. Muito bom.` (Oshtor, 20_14)
- `Hm...? Are you certain?` -> `Hm...? Tem certeza?` (Oshtor, 20_14)
- `Lord Dekopompo! The unit approaching our position\n` -> `Lorde Dekopompo! A unidade que se aproximava\n` (SOLDADO, 20_14)
- `has begun to retreat. Another glorious victory\n` -> `começou a recuar. Mais uma gloriosa vitória\n` (SOLDADO, 20_14)
- `for us!` -> `para nós!` (Maroro, 20_14)
- `Nyeh-peh-peh-peh-peh!\n` -> `Nyeh-peh-peh-peh-peh!\n` (Dekopompo, 20_14)
- `Good. Very good.` -> `Bom. Muito bom.` (Oshtor, 20_14)
- `Huzzah! A sweeter missive of relief was never\n` -> `Ótimas novas! Jamais me chegou mensagem mais doce\n` (Dekopompo, 20_14)
- `had...` -> `tínhamos...` (Maroro, 20_14)
- `Good now, let us recall the men, that they may\n` -> `Muito bem, recolhamos os homens para que possam\n` (Dekopompo, 20_14)
- `prepare for battles on the morrow.` -> `preparar para batalhas de amanhã.` (Oshtor, 20_14)
- `Nyeh?` -> `Nhê?` (Maroro, 12_13)
- `What drivel are you spouting? Why would I pass up\n` -> `Que tolice é essa? Por que eu desperdiçaria\n` (Dekopompo, 20_14)
- `such a golden opportunity as this!?` -> `uma oportunidade tão dourada assim!?` (Maroro, 20_14)
- `We shall continue our assault. Bokoinante,\n` -> `Continuaremos o ataque. Bokoinante,\n` (Dekopompo, 20_14)
- `give the order to pursue.` -> `Ordenar a perseguição.` (Oshtor, 20_14)
- `Understood, sir!` -> `Entendido, senhor!` (Maroro, 20_14)
- `N-No, thou mustn't!` -> `N-Não, você não pode!` (Maroro, 20_14)
- `Hast thou forgotten? We are far outmatch'd by\n` -> `Acaso esquecestes? Somos superados em número\n` (Maroro, 20_14)
- `such opposed numbers!` -> `Contra números tão grandes!` (Maroro, 20_14)
- `Hmph. Their numbers don't matter. They are only\n` -> `Hmph. Os números deles não importam. São apenas\n` (Dekopompo, 20_14)
- `an undisciplined mob. Were you not watching the\n` -> `uma turba indisciplinada. Não estava observando o\n` (Dekopompo, 20_14)
- `battle?` -> `Batalha?` (Maroro, 20_14)
- `P-Prithee, master, if we act without caution,\n` -> `P-Peço-vos, mestre, se agirmos sem cautela,\n` (Maroro, 20_14)
- `we act in grave error!` -> `Atuamos em erro grave!` (Maroro, 20_14)
- `Silence! I have heard enough from you!\n` -> `Silêncio! Já ouvi o suficiente de você!\n` (Dekopompo, 20_14)
- `Don't get a big head because of one scrap of\n` -> `Não se envaideça por uma migalha de\n` (Dekopompo, 20_14)
- `praise from me!` -> `Louvor de mim!` (Maroro, 20_14)
- `My lord is absolutely right!\n` -> `Meu senhor está absolutamente certo!\n` (Maroro, 20_14)
- `Know your place! ` -> `Conheça seu lugar!` (Oshtor, 20_14)
- `O-Ohhhh...` -> `O-Oohhh...` (Maroro, 20_14)
- `See! Look at that! Ordering the pursuit was the\n` -> `Vejam! Olhem só! Ordenar a perseguição foi a\n` (Maroro, 20_14)
- `correct course of action!` -> `Curso correto de ação!` (Maroro, 20_14)
- `W-Wait! Please, desist!` -> `E-Espere! Por favor, cesse!` (Maroro, 20_14)
- `Those are all but nakwans!` -> `Todos são apenas nakwans!` (Maroro, 20_14)
- `They are not true countrymen of Uzurusha!` -> `Não são verdadeiros compatriotas de Uzurusha!` (Maroro, 20_14)
- `Hmph. You would have me show them mercy? How\n` -> `Hmph. Querem que eu lhes mostre piedade? Que\n` (Dekopompo, 20_14)
- `foolish. Do you not understand that they are\n` -> `tolice. Não entendem que eles são\n` (Dekopompo, 20_14)
- `traitors?` -> `Traidores?` (Maroro, 20_14)
- `I do not dispute thus! Hark thou, to dispatch\n` -> `Não discuto isso! Ouvi-me bem, mandar abater\n` (Maroro, 20_14)
- `even a thousand nakwans will not hinder Uzurusha\n` -> `mesmo mil nakwans não ameaça Uzurusha\n` (Maroro, 20_14)
- `a whit!` -> `Nada disso!` (Maroro, 20_14)
- `I'faith, it does naught but exhaust our own\n` -> `Na verdade, só serve para esgotar as nossas\n` (Maroro, 20_14)
- `warriors...` -> `Guerreiros...` (Maroro, 20_14)
- `Arrrrgh! I've had enough out of you! Stop\n` -> `Argh! Já chega de você! Pare de\n` (Dekopompo, 20_14)
- `dampening my mood! I am TRYING to enjoy my\n` -> `estragar meu humor! Estou TENTANDO aproveitar minha\n` (Dekopompo, 20_14)
- `victory!` -> `Vitória!` (Oshtor, 20_14)
- `Bokoinante! Give the orders to continue the\n` -> `Bokoinante! Dê as ordens para continuar o\n` (Dekopompo, 20_14)
- `pursuit!` -> `Perseguição!` (Oshtor, 20_14)
- `This bodeth ill... Oh, this bodeth ill indeed...` -> `Isto pressagia mal... Oh, isto pressagia muito mal mesmo...` (Maroro, 20_14)
- `Nyah... If I recall, we had one more unit\n` -> `Hmm... Se bem me lembro, ainda tínhamos uma unidade\n` (Bokoinante, 20_14)
- `stationed somewhere around here.` -> `Posicionado em algum lugar por aqui.` (Maroro, 20_14)
- `What!? Nay, that unit is--!` -> `O quê!? Não, essa unidade é--!` (Maroro, 20_14)
- `Very well, give them the orders to pursue\n` -> `Muito bem, passe a ordem para que persigam\n` (Dekopompo, 20_14)
- `as well. Our time has come! Let us crush\n` -> `também. Nossa hora chegou! Vamos esmagar\n` (Dekopompo, 20_14)
- `Uzurusha!` -> `Uzurusha!` (SYSTEM, 20_14)
- `H-Hold, I say! Move'st thou not those men!\n` -> `E-Espera, digo eu! Não movais esses homens!\n` (Maroro, 20_14)
- `That unit--` -> `Essa unidade--` (Maroro, 20_14)
- `I thought I told you to be silent!` -> `Pensei ter dito para você ficar em silêncio!` (Oshtor, 20_14)
- `Nyeh peh peh peh.\n` -> `Nyeh peh peh peh.\n` (Dekopompo, 20_14)
- `All according to plan...` -> `Tudo conforme o plano...` (Oshtor, 20_14)
- `R-Reporting!` -> `R-Reportando!` (SYSTEM, 20_14)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `Our units in pursuit have been ambushed from\n` -> `Nossas unidades em perseguição foram emboscadas\n` (SOLDADO, 20_14)
- `the side!` -> `Do flanco!` (Maroro, 20_14)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `I-It seems as though the enemy had hidden\n` -> `A-Ao que parece, o inimigo havia se escondido\n` (SOLDADO, 20_14)
- `soldiers within the mountains...` -> `Soldados dentro das montanhas...` (Maroro, 20_14)
- `Nyuurrrrgh...` -> `Nyuurrrrgh...` (Maroro, 20_14)
- `Alack, I knew't!` -> `Ai, eu pressentira!` (Maroro, 20_14)
- `What? What is that supposed to mean!?` -> `O quê? O que se supõe que signifique!?` (Oshtor, 20_14)
- `Those mountains give perfect vantage for a\n` -> `Essas montanhas são perfeitas para uma\n` (Maroro, 20_14)
- `battalion readied in ambush!` -> `Um batalhão preparado em emboscada!` (Maroro, 20_14)
- `In my caution, I had set aside that regiment\n` -> `Com minha cautela, havia reservado aquele regimento\n` (Maroro, 20_14)
- `as safeguard against such skullduggery...` -> `Como proteção contra tal astúcia...` (Maroro, 20_14)
- `Wh-Why didn't you say something earlier!?` -> `P-Por que não disse algo antes!?` (Maroro, 20_14)
- `Earnest attempts were swift rebuffed, Master.` -> `Tentativas sinceras foram rapidamente rejeitadas, Mestre.` (Maroro, 20_14)
- `Wh-What shall we do?` -> `P-O que fazer agora?` (Maroro, 20_14)
- `At this rate, the separated units in front\n` -> `Nesse ritmo, as unidades separadas à frente\n` (Maroro, 20_14)
- `will be decimated!` -> `Serão dizimados!` (Maroro, 20_14)
- `Nyuuurrrrgh... Hm? Wait a minute.` -> `Nyuuurrrrgh... Hm? Espera um minuto.` (Oshtor, 20_14)
- `I-I know! We will have the units in front\n` -> `E-Eu sei! Faremos as unidades à frente\n` (Dekopompo, 20_14)
- `turn back...! And we catch the ambushers in a\n` -> `recuarem...! E pegamos os emboscadores em uma\n` (Dekopompo, 20_14)
- `pincer attack!` -> `Ataque de pinça!` (Oshtor, 20_14)
- `Ah! A flawless strategy, sir!` -> `Ah! Uma estratégia impecável, senhor!` (Maroro, 20_14)
- `No no no! Thou mustn't! The units in front must\n` -> `Não, não, não! Não deveis! As unidades à frente\n` (Maroro, 20_14)
- `soldier on, and thus 'scape their dire straits!` -> `Continue lutando e escapa de seu destino terrível!` (Maroro, 20_14)
- `What? Are you a fool, you painted little\n` -> `O quê? É um tolo, seu palhaço pintado e\n` (Dekopompo, 20_14)
- `imbecile?` -> `Imbecil?` (Maroro, 20_14)
- `Bokoinante, pay no mind to what he says.\n` -> `Bokoinante, não dê ouvidos ao que ele diz.\n` (Dekopompo, 20_14)
- `All he will do is cause more confusion.` -> `Tudo que ele fará é causar mais confusão.` (Maroro, 20_14)
- `Waaaah! I-I pray you, master, a willing ear!` -> `Waaaah! Por favor, Mestre, escuta-me com boa vontade!` (Maroro, 20_14)
- `It did not work... The fleeing enemies have\n` -> `Não funcionou... Os inimigos em fuga\n` (SOLDADO, 20_14)
- `turned in kind, and now WE are caught in a\n` -> `revidaram, e agora NÓS é que estamos em uma\n` (SOLDADO, 20_14)
- `pincer attack...` -> `Ataque de pinça...` (Oshtor, 20_14)
- `Wh... Wh-Wh-Wha...!` -> `Wh... Wh-Wh-O quê...!` (Protagonista, 20_14)
- `I warned, and warned, and warned again, master...` -> `Avisei, avisei e avisei novamente, mestre...` (Maroro, 20_14)
- `Silence! Y-Your babbling distracted me!\n` -> `Silêncio! V-Você me distraiu com sua tagarelice!\n` (Dekopompo, 20_14)
- `Do something, you pasty little clown!\n` -> `Faça alguma coisa, seu palhacinho pálido!\n` (Dekopompo, 20_14)
- `Aren't you my tactician!?` -> `Não me diga que é você meu estrategista!?` (Ukon, 20_14)
- `Th-Thou askest the impossible!` -> `Tu... tu pedis o impossível!` (Maroro, 20_14)
- `Master Haku... Please, help me...!` -> `Mestre Haku... Por favor, me ajude...!` (Maroro, 20_14)
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `Hyahahahahaha! Look at these guys!\n` -> `Hyahahahahaha! Olhem só esses caras!\n` (Mikazuchi, 20_14)
- `They're so pathetic!` -> `Que patéticos!` (Haku, 20_14)
- `What is wrong with these Yamatan soldiers?\n` -> `O que há de errado com esses soldados de Yamato?\n` (Mikazuchi, 20_14)
- `First they charge, then they flee! What are\n` -> `Primeiro atacam, depois fogem! O que são\n` (Mikazuchi, 20_14)
- `they thinking?` -> `eles estão pensando?` (Haku, 20_14)
- `Heh heh! They've gotta have a complete idiot\n` -> `Heh heh! Devem ter um idiota completo\n` (Mikazuchi, 20_14)
- `for a tactician.` -> `de um estrategista.` (Haku, 20_14)
- `No doubt! Hyahahahahaha!` -> `Sem dúvida! Hyahahahahaha!` (Ukon, 20_14)
- `C'mon, let's finish off these pieces of trash.` -> `Vamos, vamos acabar com esses lixos.` (Ukon, 20_14)
- `Yeah, righ... Huh?` -> `É... Hein?` (Haku, 20_14)
- `What was that...? A gust of wind?` -> `O que foi aquilo...? Um golpe de vento?` (Haku, 20_14)
- `Wh-What the--!?` -> `O-O que—!?` (Protagonista, 18_04)
- `What?` -> `Que?` (Haku, 12_02)
- `Your arms... What happened?` -> `Seus braços... O que aconteceu?` (Protagonista, 20_14)
- `My arms? Wh...?` -> `Meus braços? O quê...?` (Protagonista, 20_14)
- `My arms... are gone!?` -> `Meus braços... se foram!?` (Protagonista, 20_14)
- `Why are you... leaning to the side so much...?` -> `Por que você... está se inclinando tanto pra um lado...?` (Haku, 20_14)
- `Huh? What are you... Ahhhh!\n` -> `Hã? O que você...? Aaaaah!\n` (Dekopompo, 20_14)
- `Y-Your head...!` -> `Sua... sua cabeça...!` (Protagonista, 20_14)
- `AAAAAAAGHHH!` -> `AAAAAAAGHHH!` (Protagonista, 20_14)
- `Yamatan Soldier` -> `Soldado de Yamato` (SYSTEM, 12_10)
- `Lord... Mikazuchi?` -> `Senhor... Mikazuchi?` (Protagonista, 20_14)
- `It's Lord Mikazuchi...!` -> `É o Senhor Mikazuchi...!` (Maroro, 20_14)
- `Lord Mikazuchi has come to save us!` -> `O Senhor Mikazuchi veio nos salvar!` (Maroro, 20_14)
- `I am lightning made flesh.\n` -> `Sou o relâmpago feito carne.\n` (Mikazuchi, 20_14)
- `Akuruka, grant me thy infinite power, and\n` -> `Akuruka, concede-me teu poder infinito, e\n` (Mikazuchi, 20_14)
- `I shall fly clad in the storm.` -> `Vou voar cingido pela tempestade.` (Mikazuchi, 20_14)
- `...HAH!` -> `...HÁ!` (Mikazuchi, 20_14)
- `What's going on...? What...?\n` -> `O que está acontecendo...? O que...?\n` (Protagonista, 20_14)
- `The Imperial General of the Left?\n` -> `O General Imperial da Esquerda?\n` (Personagem, 20_14)
- `Mikazuchi is here!?` -> `Mikazuchi está aqui!?` (Maroro, 20_14)
- `Yes, sir.` -> `Sim, senhor.` (Bokoinante, 20_14)
- `Impossible... I have heard nothing of this!\n` -> `Impossível... Não ouvi nada sobre isso!\n` (Personagem, 20_14)
- `I--` -> `Eu—` (Maroro, 20_14)
- `'T-Tis our fortune, master! We must call our\n` -> `É-É nossa sorte, mestre! Devemos chamar nossas\n` (Maroro, 20_14)
- `troops back while the chance yet remaineth!` -> `tropas enquanto a ocasião ainda o permitir!` (Maroro, 20_14)
- `Still you dare talk back!? I can't sit idly by\n` -> `Ainda ousa contradizer!? Não posso ficar parado\n` (Dekopompo, 20_14)
- `while Mikazuchi takes all the glory!\n` -> `enquanto Mikazuchi fica com toda a glória!\n` (Dekopompo, 20_14)
- `We must launch a--` -> `Devemos lançar um—` (Maroro, 20_14)
- `Thou wilt stay thy tongue!` -> `Tu vais calar tua língua!` (Ukon, 20_14)
- `Nyegh...!?` -> `Nyégh...!?` (Maroro, 20_14)
- `If the advance should persist, we are verily\n` -> `Se o avanço persistir, estamos verdadeiramente\n` (Maroro, 20_14)
- `undone!` -> `desfeito!` (Maroro, 20_14)
- `Master Mikazuchi hath carved a path that we\n` -> `O Mestre Mikazuchi abriu um caminho que nós\n` (Maroro, 20_14)
- `might 'scape...` -> `possa escapar...` (Maroro, 20_14)
- `We must needs leave the fray in his hands,\n` -> `Devemos deixar o combate em suas mãos,\n` (Maroro, 20_14)
- `and hie our troops to safety!` -> `e apressemos nossas tropas à segurança!` (Maroro, 20_14)
- `Nyuuurgh...` -> `Nyuuurgh...` (Ukon, 20_14)
- `Please, master!` -> `Por favor, senhor!` (Bokoinante, 20_14)
- `Graaaah, fine. Fine!` -> `Tá bom, tá bom!` (Ukon, 20_14)
- `Bokoinante! Give our troops the order to retreat!` -> `Bokoinante! Dê a ordem de retirada às nossas tropas!` (Ukon, 20_14)
- `You... truly approve of this, sir?` -> `Você... realmente aprova isto, senhor?` (Bokoinante, 20_14)
- `Of course not! But if our tactician wills it,\n` -> `Claro que não! Mas se nosso tático assim quer,\n` (Ukon, 20_14)
- `oh! Well then, it MUST be so!` -> `ah! Bem, então DEVE ser assim!` (Ukon, 20_14)
- `I-I say!?` -> `E-Então!?` (Bokoinante, 20_14)
- `Curses. How humiliating...` -> `Que raiva. Humilhante...` (Oshtor, 20_14)
- `All troops have completed their retreat.` -> `Todas as tropas completaram a retirada.` (Bokoinante, 20_14)
- `There seems to be no pursuit. Lord Mikazuchi\n` -> `Parece que não há perseguição. O Senhor Mikazuchi\n` (Maroro, 20_14)
- `appears still to be holding them off for us.` -> `parece ainda estar os segurando para nós.` (Maroro, 20_14)
- `...*Glare*` -> `...*Olhar fixo*` (Protagonista, 20_14)
- `Er... I mean... Never mind.` -> `Er... Quer dizer... Esqueça.` (Maroro, 20_14)
- `Phew... Lord Mikazuchi, thy fortitude hath\n` -> `Ufa... Senhor Mikazuchi, tua fortitude hath\n` (Maroro, 20_14)
- `saved us all.` -> `nos salvou a todos.` (Maroro, 20_14)
- `However, our casualties were many. We succeeded\n` -> `Porém, nossas baixas foram muitas. Conseguimos\n` (Maroro, 20_14)
- `in halting the enemy invasion, but to call it\n` -> `deter a invasão inimiga, mas chamar isso de\n` (Maroro, 20_14)
- `"victory" would be...` -> `"vitória" seria...` (Oshtor, 20_14)
- `...Bokoinante. You take care of the report.` -> `...Bokoinante. Você fica responsável pelo relatório.` (Oshtor, 20_14)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `NYEH!` -> `NYÉH!` (Bokoinante, 20_14)
- `Nngh... U-Understood, Sir...` -> `Nnh... E-Entendido, Senhor...` (Bokoinante, 20_14)
- `Oh, and you. Maroro.` -> `Ah, e você. Maroro.` (Oshtor, 20_14)
- `Ay...?` -> `Eu...?` (Maroro, 20_14)
- `There will be a detailed report on YOUR blunders\n` -> `Haverá um relatório detalhado dos SEUS erros\n` (Ukon, 20_14)
- `today. I suggest you prepare for a dock in pay.` -> `hoje. Sugiro que você se prepare para um corte no pagamento.` (Oshtor, 20_14)
- `O me!?` -> `Ah, meu Deus!?` (Maroro, 20_14)
- `A-Alas...` -> `Ai... Ai...` (Maroro, 20_14)
- `Damn you, Mikazuchi... Just you watch...!` -> `Maldito você, Mikazuchi... Só espera...!` (Haku, 20_14)
- `GlobalSRT` -> `GlobalSRT` (SYSTEM, 20_11)
- `target` -> `target` (SYSTEM, 20_11)
- `ch120_01` -> `cap120_01` (SYSTEM, 20_14)
- `weapon2` -> `arma2` (SYSTEM, 20_14)
- `body` -> `corpo` (SYSTEM, 20_14)
- `face` -> `rosto` (SYSTEM, 20_14)
- `hair` -> `cabelo` (SYSTEM, 20_14)
- `mask` -> `másc.` (SYSTEM, 20_14)
- `env_bone` -> `env_bone` (Sistema, 20_13)
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
| 0x1fa6a1 | 46 | Meanwhile, in another area along the western\n |
| 0x1fa6d0 | 9 | border... |
| 0x1fa6da | 47 | An army lead by Dekopompo of the Eight Pillar\n |
| 0x1fa70a | 44 | Generals fights to stall the Uzurushan army. |
| 0x1fa737 | 47 | Unlike the other battlefields, the two armies\n |
| 0x1fa767 | 50 | here split into smaller units, skirmishing while\n |
| 0x1fa79a | 12 | scattered... |
| 0x1fa7a7 | 10 | Reporting! |
| 0x1fa7b2 | 48 | Our soldiers have defeated the enemy unit that\n |
| 0x1fa7e3 | 30 | was approaching from our left! |
| 0x1fa802 | 18 | I see! Good. Good. |
| 0x1fa815 | 23 | Hm...? Are you certain? |
| 0x1fa82d | 51 | Lord Dekopompo! The unit approaching our position\n |
| 0x1fa861 | 48 | has begun to retreat. Another glorious victory\n |
| 0x1fa892 | 7 | for us! |
| 0x1fa89a | 23 | Nyeh-peh-peh-peh-peh!\n |
| 0x1fa8b2 | 16 | Good. Very good. |
| 0x1fa8c3 | 47 | Huzzah! A sweeter missive of relief was never\n |
| 0x1fa8f3 | 6 | had... |
| 0x1fa8fa | 48 | Good now, let us recall the men, that they may\n |
| 0x1fa92b | 34 | prepare for battles on the morrow. |
| 0x1fa94e | 5 | Nyeh? |
| 0x1fa954 | 51 | What drivel are you spouting? Why would I pass up\n |
| 0x1fa988 | 35 | such a golden opportunity as this!? |
| 0x1fa9ac | 44 | We shall continue our assault. Bokoinante,\n |
| 0x1fa9d9 | 25 | give the order to pursue. |
| 0x1fa9f3 | 16 | Understood, sir! |
| 0x1faa04 | 19 | N-No, thou mustn't! |
| 0x1faa18 | 47 | Hast thou forgotten? We are far outmatch'd by\n |
| 0x1faa48 | 21 | such opposed numbers! |
| 0x1faa5e | 49 | Hmph. Their numbers don't matter. They are only\n |
| 0x1faa90 | 49 | an undisciplined mob. Were you not watching the\n |
| 0x1faac2 | 7 | battle? |
| 0x1faaca | 47 | P-Prithee, master, if we act without caution,\n |
| 0x1faafa | 22 | we act in grave error! |
| 0x1fab11 | 40 | Silence! I have heard enough from you!\n |
| 0x1fab3a | 46 | Don't get a big head because of one scrap of\n |
| 0x1fab69 | 15 | praise from me! |
| 0x1fab79 | 30 | My lord is absolutely right!\n |
| 0x1fab98 | 17 | Know your place!  |
| 0x1fabaa | 10 | O-Ohhhh... |
| 0x1fabb5 | 49 | See! Look at that! Ordering the pursuit was the\n |
| 0x1fabe7 | 25 | correct course of action! |
| 0x1fac01 | 23 | W-Wait! Please, desist! |
| 0x1fac19 | 26 | Those are all but nakwans! |
| 0x1fac34 | 41 | They are not true countrymen of Uzurusha! |
| 0x1fac5e | 46 | Hmph. You would have me show them mercy? How\n |
| 0x1fac8d | 46 | foolish. Do you not understand that they are\n |
| 0x1facbc | 9 | traitors? |
| 0x1facc6 | 47 | I do not dispute thus! Hark thou, to dispatch\n |
| 0x1facf6 | 50 | even a thousand nakwans will not hinder Uzurusha\n |
| 0x1fad29 | 7 | a whit! |
| 0x1fad31 | 45 | I'faith, it does naught but exhaust our own\n |
| 0x1fad5f | 11 | warriors... |
| 0x1fad6b | 43 | Arrrrgh! I've had enough out of you! Stop\n |
| 0x1fad97 | 44 | dampening my mood! I am TRYING to enjoy my\n |
| 0x1fadc4 | 8 | victory! |
| 0x1fadcd | 45 | Bokoinante! Give the orders to continue the\n |
| 0x1fadfb | 8 | pursuit! |
| 0x1fae04 | 48 | This bodeth ill... Oh, this bodeth ill indeed... |
| 0x1fae35 | 43 | Nyah... If I recall, we had one more unit\n |
| 0x1fae61 | 32 | stationed somewhere around here. |
| 0x1fae82 | 27 | What!? Nay, that unit is--! |
| 0x1fae9e | 43 | Very well, give them the orders to pursue\n |
| 0x1faeca | 42 | as well. Our time has come! Let us crush\n |
| 0x1faef5 | 9 | Uzurusha! |
| 0x1faeff | 44 | H-Hold, I say! Move'st thou not those men!\n |
| 0x1faf2c | 11 | That unit-- |
| 0x1faf38 | 34 | I thought I told you to be silent! |
| 0x1faf5b | 19 | Nyeh peh peh peh.\n |
| 0x1faf6f | 24 | All according to plan... |
| 0x1faf88 | 12 | R-Reporting! |
| 0x1faf95 | 11 | What is it? |
| 0x1fafa1 | 46 | Our units in pursuit have been ambushed from\n |
| 0x1fafd0 | 9 | the side! |
| 0x1fafda | 6 | WHAT!? |
| 0x1fafe1 | 43 | I-It seems as though the enemy had hidden\n |
| 0x1fb00d | 32 | soldiers within the mountains... |
| 0x1fb02e | 13 | Nyuurrrrgh... |
| 0x1fb03c | 16 | Alack, I knew't! |
| 0x1fb04d | 37 | What? What is that supposed to mean!? |
| 0x1fb073 | 44 | Those mountains give perfect vantage for a\n |
| 0x1fb0a0 | 28 | battalion readied in ambush! |
| 0x1fb0bd | 46 | In my caution, I had set aside that regiment\n |
| 0x1fb0ec | 41 | as safeguard against such skullduggery... |
| 0x1fb116 | 41 | Wh-Why didn't you say something earlier!? |
| 0x1fb140 | 45 | Earnest attempts were swift rebuffed, Master. |
| 0x1fb16e | 20 | Wh-What shall we do? |
| 0x1fb183 | 44 | At this rate, the separated units in front\n |
| 0x1fb1b0 | 18 | will be decimated! |
| 0x1fb1c3 | 33 | Nyuuurrrrgh... Hm? Wait a minute. |
| 0x1fb1e5 | 43 | I-I know! We will have the units in front\n |
| 0x1fb211 | 47 | turn back...! And we catch the ambushers in a\n |
| 0x1fb241 | 14 | pincer attack! |
| 0x1fb250 | 29 | Ah! A flawless strategy, sir! |
| 0x1fb26e | 49 | No no no! Thou mustn't! The units in front must\n |
| 0x1fb2a0 | 47 | soldier on, and thus 'scape their dire straits! |
| 0x1fb2d0 | 42 | What? Are you a fool, you painted little\n |
| 0x1fb2fb | 9 | imbecile? |
| 0x1fb305 | 42 | Bokoinante, pay no mind to what he says.\n |
| 0x1fb330 | 39 | All he will do is cause more confusion. |
| 0x1fb358 | 44 | Waaaah! I-I pray you, master, a willing ear! |
| 0x1fb385 | 45 | It did not work... The fleeing enemies have\n |
| 0x1fb3b3 | 44 | turned in kind, and now WE are caught in a\n |
| 0x1fb3e0 | 16 | pincer attack... |
| 0x1fb3f1 | 19 | Wh... Wh-Wh-Wha...! |
| 0x1fb405 | 49 | I warned, and warned, and warned again, master... |
| 0x1fb437 | 41 | Silence! Y-Your babbling distracted me!\n |
| 0x1fb461 | 39 | Do something, you pasty little clown!\n |
| 0x1fb489 | 25 | Aren't you my tactician!? |
| 0x1fb4a3 | 30 | Th-Thou askest the impossible! |
| 0x1fb4c2 | 34 | Master Haku... Please, help me...! |
| 0x1fb4e5 | 17 | Uzurushan soldier |
| 0x1fb4f7 | 36 | Hyahahahahaha! Look at these guys!\n |
| 0x1fb51c | 20 | They're so pathetic! |
| 0x1fb531 | 44 | What is wrong with these Yamatan soldiers?\n |
| 0x1fb55e | 45 | First they charge, then they flee! What are\n |
| 0x1fb58c | 14 | they thinking? |
| 0x1fb59b | 46 | Heh heh! They've gotta have a complete idiot\n |
| 0x1fb5ca | 16 | for a tactician. |
| 0x1fb5db | 24 | No doubt! Hyahahahahaha! |
| 0x1fb5f4 | 46 | C'mon, let's finish off these pieces of trash. |
| 0x1fb623 | 18 | Yeah, righ... Huh? |
| 0x1fb636 | 33 | What was that...? A gust of wind? |
| 0x1fb658 | 15 | Wh-What the--!? |
| 0x1fb668 | 5 | What? |
| 0x1fb66e | 27 | Your arms... What happened? |
| 0x1fb68a | 15 | My arms? Wh...? |
| 0x1fb69a | 21 | My arms... are gone!? |
| 0x1fb6b0 | 46 | Why are you... leaning to the side so much...? |
| 0x1fb6df | 29 | Huh? What are you... Ahhhh!\n |
| 0x1fb6fd | 15 | Y-Your head...! |
| 0x1fb70d | 12 | AAAAAAAGHHH! |
| 0x1fb71e | 15 | Yamatan Soldier |
| 0x1fb72e | 18 | Lord... Mikazuchi? |
| 0x1fb741 | 23 | It's Lord Mikazuchi...! |
| 0x1fb759 | 35 | Lord Mikazuchi has come to save us! |
| 0x1fb77d | 28 | I am lightning made flesh.\n |
| 0x1fb79a | 43 | Akuruka, grant me thy infinite power, and\n |
| 0x1fb7c6 | 30 | I shall fly clad in the storm. |
| 0x1fb7e5 | 7 | ...HAH! |
| 0x1fb7ed | 30 | What's going on...? What...?\n |
| 0x1fb80c | 35 | The Imperial General of the Left?\n |
| 0x1fb830 | 19 | Mikazuchi is here!? |
| 0x1fb844 | 9 | Yes, sir. |
| 0x1fb84e | 45 | Impossible... I have heard nothing of this!\n |
| 0x1fb87c | 3 | I-- |
| 0x1fb880 | 46 | 'T-Tis our fortune, master! We must call our\n |
| 0x1fb8af | 43 | troops back while the chance yet remaineth! |
| 0x1fb8db | 48 | Still you dare talk back!? I can't sit idly by\n |
| 0x1fb90c | 38 | while Mikazuchi takes all the glory!\n |
| 0x1fb933 | 18 | We must launch a-- |
| 0x1fb946 | 26 | Thou wilt stay thy tongue! |
| 0x1fb961 | 10 | Nyegh...!? |
| 0x1fb96c | 46 | If the advance should persist, we are verily\n |
| 0x1fb99b | 7 | undone! |
| 0x1fb9a3 | 45 | Master Mikazuchi hath carved a path that we\n |
| 0x1fb9d1 | 15 | might 'scape... |
| 0x1fb9e1 | 44 | We must needs leave the fray in his hands,\n |
| 0x1fba0e | 29 | and hie our troops to safety! |
| 0x1fba2c | 11 | Nyuuurgh... |
| 0x1fba38 | 15 | Please, master! |
| 0x1fba48 | 20 | Graaaah, fine. Fine! |
| 0x1fba5d | 49 | Bokoinante! Give our troops the order to retreat! |
| 0x1fba8f | 34 | You... truly approve of this, sir? |
| 0x1fbab2 | 47 | Of course not! But if our tactician wills it,\n |
| 0x1fbae2 | 29 | oh! Well then, it MUST be so! |
| 0x1fbb00 | 9 | I-I say!? |
| 0x1fbb0a | 26 | Curses. How humiliating... |
| 0x1fbb25 | 40 | All troops have completed their retreat. |
| 0x1fbb4e | 46 | There seems to be no pursuit. Lord Mikazuchi\n |
| 0x1fbb7d | 44 | appears still to be holding them off for us. |
| 0x1fbbaa | 10 | ...*Glare* |
| 0x1fbbb5 | 27 | Er... I mean... Never mind. |
| 0x1fbbd1 | 44 | Phew... Lord Mikazuchi, thy fortitude hath\n |
| 0x1fbbfe | 13 | saved us all. |
| 0x1fbc0c | 49 | However, our casualties were many. We succeeded\n |
| 0x1fbc3e | 47 | in halting the enemy invasion, but to call it\n |
| 0x1fbc6e | 21 | "victory" would be... |
| 0x1fbc84 | 43 | ...Bokoinante. You take care of the report. |
| 0x1fbcb0 | 5 | Huh!? |
| 0x1fbcb6 | 5 | NYEH! |
| 0x1fbcbc | 28 | Nngh... U-Understood, Sir... |
| 0x1fbcd9 | 20 | Oh, and you. Maroro. |
| 0x1fbcee | 6 | Ay...? |
| 0x1fbcf5 | 50 | There will be a detailed report on YOUR blunders\n |
| 0x1fbd28 | 47 | today. I suggest you prepare for a dock in pay. |
| 0x1fbd58 | 6 | O me!? |
| 0x1fbd5f | 9 | A-Alas... |
| 0x1fbd69 | 41 | Damn you, Mikazuchi... Just you watch...! |
| 0x1fbd94 | 9 | globalSRT |
| 0x1fbd9e | 6 | target |
| 0x1fbda5 | 8 | ch120_01 |
| 0x1fbdae | 7 | weapon2 |
| 0x1fbdb6 | 4 | body |
| 0x1fbdbb | 4 | face |
| 0x1fbdc0 | 4 | hair |
| 0x1fbdc5 | 4 | mask |
| 0x1fbdca | 8 | env_bone |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_14.json` com a forma:
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
