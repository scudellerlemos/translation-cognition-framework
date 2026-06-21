# Cena ch_17_01 — pacote de traducao (2825 linhas)

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
| Chalafun | Personagem | Chalafun | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Karulau | Personagem | Karulau | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Touka | Personagem | Touka | manter_original | moderate |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| Ukon | Personagem | Ukon | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| woptor | Criatura | woptor | manter_original | none |
| yacchip | Item | yacchip | manter_original | none |
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
- `Worker` -> `Func.` (Haku, 14_03)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `now.` -> `já.` (Kuon, 14_04)
- `trouble...` -> `incomodar...` (Rulutieh, 13_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Uh...` -> `Ahn...` (Haku, 14_03)
- `*THUNK*` -> `*TUM*` (Haku, 11_10)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `spirits.` -> `espíritos.` (Garota, 16_02)
- `What's the matter?` -> `O que foi?` (Haku, 15_02)
- `You know...` -> `Sabe...` (Haku, 11_03)
- `about it.` -> `sem pensar.` (Haku, 15_01)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `then...` -> `então...` (Haku, 14_04)
- `Atuy...` -> `Atuy...` (Atuy, 16_02)
- `expression.` -> `natural.` (Haku, 15_01)
- `first.` -> `primeiro.` (Haku, 13_02)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `Sir Haku?` -> `Sir Haku?` (Rulutieh, 13_02)
- `Man` -> `Hom` (Sistema, 12_04)
- `then.` -> `então.` (Kuon, 13_01)
- `face.` -> `rosto.` (Rulutieh, 16_02)
- `that?` -> `né?` (Haku, 14_09)
- `Um, dear sister...` -> `Hm, cara irmã...` (Nekone, 15_02)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `...Right. ` -> `...Tá.` (Haku, 14_10)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `don't you?` -> `não tem?` (Kuon, 14_10)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `enough.` -> `afinal.` (Ukon, 14_04)
- `Uh?` -> `Hã?` (Nekone, 16_02)
- `case.` -> `caso.` (Haku, 16_02)
- `*Jiggle, jiggle, jiggle*` -> `*Mexe, mexe, mexe*` (Kurarin, 16_01)
- `EEP!?` -> `EEEK!?` (Atuy, 16_01)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `drinking.` -> `bebendo.` (Protagonista, 16_01)
- `Nn...\n` -> `Nnh...\n` (Protagonista, root)
- `Really?` -> `Mesmo?` (Kuon, 14_03)
- `Heh.` -> `Heh.` (Haku, 14_02)
- `Phew...` -> `Ufa...` (Haku, 12_16)
- `Ow!` -> `Ai!` (Haku, 12_11)
- `own.` -> `si.` (Ukon, 15_06)
- `though.` -> `porém.` (Kuon, 12_04)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `like this?` -> `assim?` (Haku, 16_01)
- `Hee hee...` -> `Hehe...` (Kuon, root)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `And...` -> `E...` (Haku, 12_17)
- `What's wrong?` -> `O que foi?` (Kuon, 12_04)
- `myself...` -> `direito...` (Haku, 14_09)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
- `me?` -> `mim?` (Maroro, 12_13)
- `You sure?` -> `Tem certeza?` (Haku, 15_01)
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `interesting.` -> `bem legal.` (Kuon, 15_02)
- `eyes.` -> `olhar.` (Haku, 14_04)
- `Oh?` -> `Oh?` (Haku, 14_04)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `H-Hey...` -> `E-Ei...` (Kuon, root)
- `Cheers!` -> `Saúde!` (Homens, 14_04)
- `What the--` -> `Mas que--` (Haku, 11_03)
- `right?` -> `né?` (Haku, 12_03)
- `yourself.` -> `abalado.` (Kuon, 13_01)
- `Oh... I see.` -> `Ah... entendo.` (Haku, 16_02)
- `How now?` -> `Como assim?` (Maroro, 13_05)
- `Amazing...` -> `Incrível...` (Haku, 12_04)
- `Master Haku...` -> `Mestre Haku...` (Maroro, 12_13)
- `earlier.` -> `antes.` (Kuon, root)
- `For him.` -> `Por ele.` (Ukon, 16_02)
- `with you?` -> `com você?` (Inquilino, 16_01)
- `Are you OK?` -> `Está bem?` (Kuon, 13_09)
- `What's this?` -> `O que é isso?` (Haku, 12_08)
- `Let's see...` -> `Deixa eu ver...` (Haku, 16_05)
- `Wh--` -> `Q--` (Haku, 11_07)
- `attention.` -> `muita atenção.` (Ukon, 15_01)
- `...Eh?` -> `...Hein?` (Rulutieh, 13_01)
- `Homeland?` -> `Terra natal?` (Haku, 11_09)
- `A-All right...` -> `T-Tá bem...` (Haku, 12_09)
- `Hmhm...` -> `Hmhm...` (Garota, 16_01)
- `her.` -> `a ela.` (Kuon, root)
- `sight.` -> `cena estranha.` (Haku, 13_04)
- `Huh...` -> `Hum...` (Ukon, 15_05)
- `thing?` -> `dessas?` (Haku, 13_03)
- `you...` -> `você...` (Haku, 12_11)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `well.` -> `bem.` (Kuon, 16_01)
- `Wha--` -> `Quê--` (Man, 15_01)
- `B-But...` -> `M-Mas...` (Maroro, 15_02)
- `Cheers.` -> `Saúde.` (Haku, 14_04)
- `much.` -> `isso.` (Ukon, 13_09)
- `little.` -> `acorda.` (Garota, 12_01)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `R-Right...` -> `C-Certo...` (Haku, 11_09)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `capital.` -> `imperial.` (Kuon, 12_04)
- `you.` -> `isso.` (Nekone, 15_03)
- `friends.` -> `amigos.` (Ukon, 15_01)
- `mind.` -> `mente.` (NARRAÇÃO, 12_08)
- `Hmhm.` -> `Hmhm.` (Moznu, 13_05)
- `Haku...` -> `Haku...` (Kuon, 14_09)
- `now...` -> `agora...` (Haku, 12_03)
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
| 0xe82a4 | 48 | ....Whew. That about does it for all my errands. |
| 0xe82d5 | 49 | It's already past noon. No point in overworking\n |
| 0xe8307 | 41 | myself... Guess I'll take a little break. |
| 0xe8331 | 47 | I walk out into the hallway, patting my empty\n |
| 0xe8361 | 8 | stomach. |
| 0xe836a | 42 | Guess I'll get something for lunch--Whoa!? |
| 0xe8395 | 42 | Just as I take a step forward, I step on\n |
| 0xe83c0 | 28 | something round, and I slip. |
| 0xe83dd | 49 | Geez, that was close. Almost broke my head open\n |
| 0xe840f | 33 | there. What is this...? A potato? |
| 0xe8431 | 6 | Worker |
| 0xe843d | 11 | Is that...? |
| 0xe8449 | 41 | I look around to see one of the workers\n |
| 0xe8473 | 46 | walking away, holding a basket full of these\n |
| 0xe84a2 | 7 | tubers. |
| 0xe84aa | 32 | Did she accidentally drop it...? |
| 0xe84cb | 46 | As I stand there, thinking, the worker makes\n |
| 0xe84fa | 42 | her way to the back door and goes outside. |
| 0xe8525 | 22 | ...And there she goes. |
| 0xe853c | 38 | Guess I can just give it to her later. |
| 0xe8563 | 48 | What exactly is this, though...? I don't think\n |
| 0xe8594 | 41 | I've seen any crop like this around here. |
| 0xe85be | 39 | I wonder how you're supposed to eat it. |
| 0xe85e6 | 47 | I turn the potatoey thing over and over in my\n |
| 0xe8616 | 29 | hands as I continue to think. |
| 0xe8634 | 46 | Oh, I know--Maybe Kuon knows what this might\n |
| 0xe8663 | 3 | be. |
| 0xe8667 | 48 | She is an apothecary, after all. Edible plants\n |
| 0xe8698 | 43 | should be right up her alley... I'll head\n |
| 0xe86c4 | 9 | over now. |
| 0xe86ce | 46 | ...I place my hand on the door to Kuon's room. |
| 0xe86fd | 23 | Kuon, you got a moment? |
| 0xe8719 | 45 | But Kuon is staring straight at her mortar,\n |
| 0xe8747 | 34 | fully focused on the task at hand. |
| 0xe876a | 30 | ...Making some medicine there? |
| 0xe8789 | 5 | Kuon? |
| 0xe878f | 51 | Her face intent and focused, she continues mixing\n |
| 0xe87c3 | 27 | the contents of the mortar. |
| 0xe87df | 47 | Ah, well. Guess I'll wait until she's finished. |
| 0xe880f | 8 | ...Whew. |
| 0xe8818 | 9 | All done? |
| 0xe8822 | 33 | Mhm, that should be good for now. |
| 0xe8844 | 42 | Sorry about that. I just couldn't let my\n |
| 0xe886f | 30 | attention wander for a moment. |
| 0xe888e | 49 | Don't worry about it. What were you so absorbed\n |
| 0xe88c0 | 18 | in making, anyway? |
| 0xe88d3 | 49 | This? It's for my flash bombs. I'm running low,\n |
| 0xe8905 | 49 | so I thought I'd make more. You'd recognize it,\n |
| 0xe8937 | 8 | I think? |
| 0xe8940 | 44 | Oh, huh... I remember now. Didn't know you\n |
| 0xe896d | 44 | made these by hand. You saved my life with\n |
| 0xe899a | 18 | these back then... |
| 0xe89ad | 43 | Mhm. It's made with a secret recipe of my\n |
| 0xe89d9 | 9 | very own. |
| 0xe89e3 | 20 | A secret recipe, eh? |
| 0xe89f8 | 40 | Mhm. Just as it sounds, it's a secret,\n |
| 0xe8a21 | 36 | so I can't really explain in detail. |
| 0xe8a46 | 48 | Kuon closes up the canister and puts it at her\n |
| 0xe8a77 | 47 | side. I peek in... She has several more bombs\n |
| 0xe8aa7 | 4 | now. |
| 0xe8aac | 44 | You sure made a lot of them. Do you really\n |
| 0xe8ad9 | 15 | need this many? |
| 0xe8ae9 | 45 | Well, I didn't have much of the ingredients\n |
| 0xe8b17 | 46 | left. I decided I might as well use the last\n |
| 0xe8b46 | 6 | of it. |
| 0xe8b4d | 45 | At any rate, was there something you needed\n |
| 0xe8b7b | 14 | from me, Haku? |
| 0xe8b8a | 44 | Well, I finished all my work, so I thought\n |
| 0xe8bb7 | 39 | I'd come by to chat for a little break. |
| 0xe8bdf | 47 | Oh, by the way, you have any clue what this is? |
| 0xe8c0f | 47 | I take out the potato-like vegetable that the\n |
| 0xe8c3f | 23 | worker dropped earlier. |
| 0xe8c57 | 44 | Oh... A mororo. Now that's some unexpected\n |
| 0xe8c84 | 35 | nostalgia... Where did you find it? |
| 0xe8ca8 | 44 | I picked it up along the way. A mororo, huh? |
| 0xe8cd5 | 41 | Mhm. It's a staple food in my homeland.\n |
| 0xe8cff | 46 | I didn't think anyone around here ate these... |
| 0xe8d2e | 47 | Kuon smiles, her expression distant and soft,\n |
| 0xe8d5e | 41 | as though she's remembering her homeland. |
| 0xe8d88 | 46 | Wonder why she had this if it's so rare, then. |
| 0xe8db7 | 48 | Oh, Haku, why don't you stay for a cup of... hm? |
| 0xe8de8 | 44 | Looks like I'm out at the moment. Hold on,\n |
| 0xe8e15 | 26 | I'll go get some more tea. |
| 0xe8e30 | 43 | She doesn't really have to go to all that\n |
| 0xe8e5c | 10 | trouble... |
| 0xe8e67 | 19 | Hmm hmm, hmhmmmm... |
| 0xe8e7b | 4 | Huh? |
| 0xe8e80 | 44 | I look outside the window, hearing humming\n |
| 0xe8ead | 23 | coming from the garden. |
| 0xe8ec5 | 44 | There, I see the worker from before piling\n |
| 0xe8ef2 | 49 | fallen leaves in the center. She seems to be in\n |
| 0xe8f24 | 13 | high spirits. |
| 0xe8f32 | 41 | She seems pretty happy about something... |
| 0xe8f5c | 46 | I look closer to see several mororo sticking\n |
| 0xe8f8b | 18 | out of the leaves. |
| 0xe8f9e | 48 | Mhm. This should do just fine. All that's left\n |
| 0xe8fcf | 24 | is to kindle the fire... |
| 0xe8fe8 | 48 | Hm? A little damp...? Ah, such carelessness is\n |
| 0xe9019 | 44 | inexcusable... I should have aired them out. |
| 0xe9046 | 48 | Looks like she's trying to start a fire there.\n |
| 0xe9077 | 41 | Is she going to heat the mororos with it? |
| 0xe90a1 | 48 | A sudden idea comes to mind, and my gaze turns\n |
| 0xe90d2 | 30 | toward the middle of the room. |
| 0xe90f1 | 43 | She wants a... fire, huh? If she's having\n |
| 0xe911d | 42 | trouble lighting it, I guess I could help. |
| 0xe9148 | 44 | Kuon's secret mixture, and the fire in the\n |
| 0xe9175 | 48 | garden... Out of boredom, I come up with a plan. |
| 0xe91a6 | 42 | ...This'll be perfect to kill some time.\n |
| 0xe91d1 | 38 | I'll just borrow some of this, Kuon... |
| 0xe91f8 | 47 | I take a pinch of the mixture from the mortar\n |
| 0xe9228 | 48 | and mix it with the clay that was used for its\n |
| 0xe9259 | 5 | base. |
| 0xe925f | 46 | This much should be enough to just light the\n |
| 0xe928e | 46 | fire... I think? Could be dangerous if I use\n |
| 0xe92bd | 9 | too much. |
| 0xe92c7 | 35 | I'll just roll it up like this...\n |
| 0xe92eb | 8 | Perfect. |
| 0xe92f4 | 44 | Satisfied, I look again to the window that\n |
| 0xe9321 | 17 | faces the garden. |
| 0xe9333 | 43 | Gotta aim for the center of the leaves...\n |
| 0xe935f | 6 | There! |
| 0xe9366 | 46 | Just as I throw it down, she seems to finish\n |
| 0xe9395 | 35 | her preparations to light the pile. |
| 0xe93b9 | 44 | That should do. Now all that remains is to\n |
| 0xe93e6 | 22 | blow some air on it... |
| 0xe93fd | 24 | She takes a deep breath. |
| 0xe9416 | 13 | Fwooooooooo!! |
| 0xe9424 | 44 | As the air hits it, flames begin to ripple\n |
| 0xe9451 | 45 | across the leaves. And that's when the clay\n |
| 0xe947f | 6 | hits-- |
| 0xe9486 | 43 | Hm? It looked as though something strange\n |
| 0xe94b2 | 10 | fell in... |
| 0xe94bd | 7 | *CRACK* |
| 0xe94cf | 7 | Wha--!? |
| 0xe94d7 | 47 | A blinding light fills the garden, far beyond\n |
| 0xe9507 | 20 | what I had expected. |
| 0xe951c | 46 | Holy crap, that stuff's powerful... I didn't\n |
| 0xe954b | 45 | expect such a small amount to be this potent. |
| 0xe9579 | 17 | Wait, is she OK!? |
| 0xe958b | 44 | She didn't fall into the fire, did she...?\n |
| 0xe95b8 | 34 | I quickly look back at the garden. |
| 0xe95db | 45 | ...S-Such carelessness is... inexcusable...\n |
| 0xe9609 | 44 | I had no idea mororos these days emit such\n |
| 0xe9636 | 8 | light... |
| 0xe963f | 37 | ...Oh, but I must put out the fire!\n |
| 0xe9665 | 36 | I cannot allow it to spread further! |
| 0xe968a | 46 | Yet I cannot see right now... In that case...! |
| 0xe96b9 | 44 | She holds the bamboo pipe--the one she was\n |
| 0xe96e6 | 40 | blowing air through--like a sword, and\n |
| 0xe970f | 29 | lowers her stance, listening. |
| 0xe972d | 47 | A sudden tension fills the air in the garden... |
| 0xe975d | 33 | Whoa, this air she gives off...\n |
| 0xe977f | 29 | She's no ordinary servant...! |
| 0xe979d | 19 | ...Found it. There! |
| 0xe97b1 | 49 | With a swift slash, the bamboo pipe blows apart\n |
| 0xe97e3 | 34 | the fire and puts it out... but... |
| 0xe9806 | 5 | Uh... |
| 0xe980c | 13 | *Whoooooosh!* |
| 0xe981a | 47 | The bamboo pipe knocks one of the mororo into\n |
| 0xe984a | 42 | a miraculous arc straight up into the air. |
| 0xe9875 | 33 | Hm. That should have extingui--\n |
| 0xe9897 | 8 | ...Gah!? |
| 0xe98a0 | 7 | *Thunk* |
| 0xe98a8 | 5 | Oh... |
| 0xe98ae | 49 | And somehow, the airborne mororo comes crashing\n |
| 0xe98e0 | 45 | inexorably down on the worker's head, as if\n |
| 0xe990e | 13 | drawn to her. |
| 0xe991c | 42 | ...S-Such carelessness... inexcusable...\n |
| 0xe9947 | 17 | What a blunder... |
| 0xe9959 | 44 | The garden is empty, except for the worker\n |
| 0xe9986 | 43 | collapsed on the ground, and what remains\n |
| 0xe99b2 | 12 | of the fire. |
| 0xe99bf | 48 | ...I'll just... pretend I never saw any of that. |
| 0xeb703 | 47 | Together with Kuon and the others, our patrol\n |
| 0xeb733 | 47 | takes us across the main street to the vendors. |
| 0xeb763 | 21 | Peaceful as always... |
| 0xeb779 | 49 | The hustle and bustle of the crowds is the same\n |
| 0xeb7ab | 46 | as usual, but there's no arguing or grumbling. |
| 0xeb7da | 16 | Oh... It's Atuy. |
| 0xeb7eb | 3 | Hm? |
| 0xeb7ef | 50 | I follow Nekone's gaze. It's hard to see through\n |
| 0xeb822 | 43 | all the people, but I notice Atuy in high\n |
| 0xeb84e | 8 | spirits. |
| 0xeb857 | 48 | ...Didn't she say she was going to stay in her\n |
| 0xeb888 | 36 | room because she had a stomach ache? |
| 0xeb8b1 | 43 | What is she doing...? It looks like she's\n |
| 0xeb8dd | 42 | talking to that guy sitting in the street. |
| 0xeb908 | 34 | Could that man... be ill, perhaps? |
| 0xeb92b | 36 | I... wonder if something's happened. |
| 0xeb950 | 41 | Are you all right? Here, have some water. |
| 0xeb97a | 8 | Sick man |
| 0xeb983 | 46 | Thank you so much... My body simply fails me\n |
| 0xeb9b2 | 47 | sometimes... and I have these sudden attacks... |
| 0xeb9e2 | 47 | The man brushes his hair up as he accepts the\n |
| 0xeba12 | 41 | water from Atuy, apparently to take his\n |
| 0xeba3c | 9 | medicine. |
| 0xeba46 | 30 | That sounds awfully tough...\n |
| 0xeba65 | 22 | Is your home close by? |
| 0xeba7c | 39 | Yes, it is only a short walk from here. |
| 0xebaa4 | 25 | I'll walk you back, then. |
| 0xebabe | 46 | No, I--I would dare not impose so on someone\n |
| 0xebaed | 36 | I have only just met, milady fair... |
| 0xebb12 | 48 | The man tries to stand, but he staggers as his\n |
| 0xebb43 | 43 | leg gives way, forced to lean against Atuy. |
| 0xebb6f | 5 | Oh... |
| 0xebb75 | 45 | H-Here. Come on, pet, you can't even stand.\n |
| 0xebba3 | 44 | It'd be dangerous for you to walk home all\n |
| 0xebbd0 | 12 | by yourself. |
| 0xebbdd | 47 | My apologies... I do not wish to be a burden,\n |
| 0xebc0d | 47 | but may I rely on you to see me safely home...? |
| 0xebc3d | 23 | Of course I don't mind. |
| 0xebc55 | 50 | Atuy lends the man a hand, propping him up gently. |
| 0xebc88 | 48 | Whew... Thank you... Kind miss, may I have the\n |
| 0xebcb9 | 27 | honor of knowing your name? |
| 0xebcd5 | 15 | My name's Atuy. |
| 0xebce5 | 45 | Atuy... Ah, such a wonderful name. There is\n |
| 0xebd13 | 44 | something so resonant to it... like a vast\n |
| 0xebd40 | 14 | flowing ocean. |
| 0xebd4f | 44 | So kind... beautiful, and accepting of all\n |
| 0xebd7c | 34 | things, like the mother ocean...\n |
| 0xebd9f | 21 | A truly fitting name. |
| 0xebdb5 | 38 | The man smiles softly, gazing at Atuy. |
| 0xebddc | 40 | I-I don't think... anybody's ever said\n |
| 0xebe05 | 31 | something like that... to me... |
| 0xebe25 | 32 | What? That seems... unthinkable. |
| 0xebe46 | 45 | That even in the renowned imperial capital,\n |
| 0xebe74 | 46 | there are still lowborn who do not recognize\n |
| 0xebea3 | 14 | true beauty... |
| 0xebeb2 | 40 | Ooh, my... That's far too much praise,\n |
| 0xebedb | 9 | really... |
| 0xebee5 | 47 | Atuy seems rather pleased with this, blushing\n |
| 0xebf15 | 6 | madly. |
| 0xebf1c | 45 | Ah... Perhaps it was fate that I had fallen\n |
| 0xebf4a | 42 | ill here... for it allowed me to meet you. |
| 0xebf75 | 48 | Yes, it must be... It was destiny that the two\n |
| 0xebfa6 | 40 | of us were able to find each other here. |
| 0xebfcf | 46 | Seems like an anemic noble boy or something.\n |
| 0xebffe | 44 | How can he say such embarrassing crap like\n |
| 0xec02b | 26 | that with a straight face? |
| 0xec046 | 46 | Man, this is awful. What kind of woman would\n |
| 0xec075 | 48 | ever fall for these ridiculous pick-up lines...? |
| 0xec0a6 | 49 | ...Wait a minute. Why is Atuy blushing like that? |
| 0xec0d8 | 48 | ...Don't tell me she goes for pretentious guys\n |
| 0xec109 | 9 | like him? |
| 0xec113 | 50 | Uh... Erm, well, to each their own, as they say.\n |
| 0xec146 | 40 | We don't have the right to judge others. |
| 0xec16f | 19 | ...That is correct. |
| 0xec183 | 23 | Eh, guess you're right. |
| 0xec19b | 45 | Well, I'm getting hungry. Let's get moving.\n |
| 0xec1c9 | 46 | Once patrol's done, we should get some dinner. |
| 0xec1f8 | 50 | I begin walking away, but the other three remain\n |
| 0xec22b | 32 | still, continuing to watch Atuy. |
| 0xec24c | 18 | What's the matter? |
| 0xec25f | 50 | Well, as a friend, I feel it's my responsibility\n |
| 0xec292 | 31 | to see this through to the end. |
| 0xec2b2 | 20 | Yes. It is our duty. |
| 0xec2c7 | 33 | Um, I... I think so... as well... |
| 0xec2e9 | 24 | Are you guys serious...? |
| 0xec302 | 23 | Is your house this way? |
| 0xec31a | 29 | Yes. It is not far from here. |
| 0xec338 | 50 | Atuy keeps supporting the man as the two of them\n |
| 0xec36b | 29 | make their way down the road. |
| 0xec389 | 46 | ...And a ways behind them, the girls shuffle\n |
| 0xec3b8 | 27 | along, paragons of stealth. |
| 0xec3d4 | 11 | You know... |
| 0xec3e0 | 25 | Shh... They'll notice us. |
| 0xec3fa | 30 | Why are we even doing this...? |
| 0xec419 | 45 | Kuon and the others seem awfully interested\n |
| 0xec447 | 48 | in this, but their faces are all pretty serious. |
| 0xec478 | 46 | It doesn't look like they're doing this just\n |
| 0xec4a7 | 48 | for kicks. Guess they're all worried about Atuy. |
| 0xec4d8 | 12 | That said... |
| 0xec4e5 | 49 | After getting to know Atuy, there's some things\n |
| 0xec517 | 21 | I've come to realize. |
| 0xec52d | 48 | She may seem carefree and air-headed, but like\n |
| 0xec55e | 45 | Kuon, she's, uh... Nope. Not going to think\n |
| 0xec58c | 9 | about it. |
| 0xec596 | 47 | ...Suffice it to say, I highly doubt a skinny\n |
| 0xec5c6 | 42 | guy like that could do anything to Atuy... |
| 0xec5f1 | 32 | Oh... beautiful... flatter me... |
| 0xec612 | 38 | Of... not... your... know no bounds... |
| 0xec639 | 48 | We catch bits and pieces of their conversation\n |
| 0xec66a | 42 | at our distance. The man's spouting more\n |
| 0xec695 | 15 | sweet nothings. |
| 0xec6a5 | 45 | Is he really that sick? He sure talks a lot\n |
| 0xec6d3 | 49 | for how he was acting before. It seems weird...\n |
| 0xec705 | 4 | Huh? |
| 0xec70a | 37 | Wait a minute. Is that why Kuon's...? |
| 0xec730 | 48 | As I think, Atuy turns to the right, and stops\n |
| 0xec761 | 27 | in front of a vast mansion. |
| 0xec77d | 41 | This is my manor. Thank you so much for\n |
| 0xec7a7 | 22 | walking me here, Atuy. |
| 0xec7be | 42 | It's only natural to help out if you see\n |
| 0xec7e9 | 19 | someone in trouble! |
| 0xec7fd | 46 | But not many take such ideology beyond empty\n |
| 0xec82c | 48 | words. Truly, you must have a kind heart indeed. |
| 0xec85d | 18 | Attendant-like man |
| 0xec870 | 27 | Young Master, welcome home. |
| 0xec88c | 30 | Yes, I have just now returned. |
| 0xec8ab | 26 | Oh? And who might this be? |
| 0xec8c6 | 48 | She helped me when I suffered an attack in the\n |
| 0xec8f7 | 45 | market. I owe her my life. Please treat her\n |
| 0xec925 | 24 | with the utmost respect. |
| 0xec93e | 46 | Miss Atuy, if you don't mind, would you care\n |
| 0xec96d | 45 | to stop in? I dearly wish to convey my full\n |
| 0xec99b | 7 | thanks. |
| 0xec9a3 | 41 | Oh, no, I really ought to be going now.\n |
| 0xec9cd | 21 | Please don't mind me. |
| 0xec9e3 | 23 | I see. Well then, Atuy? |
| 0xec9fb | 33 | The man takes Atuy's hand in his. |
| 0xeca1d | 13 | Wh, ah, yes!? |
| 0xeca2b | 36 | Would you meet with me again soon?\n |
| 0xeca50 | 45 | I believe destiny brought us to each other.\n |
| 0xeca7e | 22 | Fate cannot be denied. |
| 0xeca95 | 5 | Ah... |
| 0xeca9b | 33 | Or am I... being a bother to you? |
| 0xecabd | 20 | N-No, of course not! |
| 0xecad2 | 7 | Then... |
| 0xecada | 6 | Mhm... |
| 0xecae1 | 44 | Well, if you insist so much, I'll be happy\n |
| 0xecb0e | 10 | to oblige. |
| 0xecb19 | 46 | Ah, what joy you have given humble Chalafun!\n |
| 0xecb48 | 42 | I have not felt such happiness in years.\n |
| 0xecb73 | 31 | May I ask where I can find you? |
| 0xecb93 | 51 | I'm staying over at a place called the Hakurokaku\n |
| 0xecbc7 | 32 | on the outskirts of the capital. |
| 0xecbe8 | 8 | Chalafun |
| 0xecbf1 | 46 | Ah, I know of it. If it allows me to see you\n |
| 0xecc20 | 42 | again, I will happily visit. Until then... |
| 0xecc4b | 32 | Oh, uh, yes. I'll... be waiting. |
| 0xecc6c | 7 | Atuy... |
| 0xecc74 | 31 | ...Something is not right here. |
| 0xecc94 | 46 | If memory serves me correctly, this manor is\n |
| 0xeccc3 | 27 | currently listed as vacant. |
| 0xeccdf | 46 | Nekone looks at the other two with a puzzled\n |
| 0xecd0e | 11 | expression. |
| 0xecd1a | 44 | ...I'd like you to elaborate a bit, I think. |
| 0xecd47 | 48 | The other day, my dear brother received orders\n |
| 0xecd78 | 40 | to conduct a census survey of this area. |
| 0xecda1 | 46 | At that time, this manor was completely empty. |
| 0xecdd0 | 36 | Um, Miss Atuy is heading this way... |
| 0xecdf5 | 46 | We quickly hide in the shadows as Atuy walks\n |
| 0xece24 | 22 | towards our direction. |
| 0xece3b | 52 | Nekone, what are the chances that someone moved in\n |
| 0xece70 | 28 | between that survey and now? |
| 0xece8d | 50 | It was mere days ago, so I believe it incredibly\n |
| 0xecec0 | 9 | unlikely. |
| 0xececa | 46 | Which means those people over there are most\n |
| 0xecef9 | 33 | likely up to no good, I'd assume. |
| 0xecf1b | 47 | Hold it, Kuon. Where do you think you're going? |
| 0xecf4b | 49 | I was considering beating the truth out of them\n |
| 0xecf7d | 20 | right now, actually. |
| 0xecf92 | 35 | Or are you going to try to stop me? |
| 0xecfb6 | 48 | Holy crap, what!? Yeesh, she's terrifying when\n |
| 0xecfe7 | 47 | she gets like this. I know how you feel, but... |
| 0xed017 | 48 | You need to calm down, Kuon. It's not like you\n |
| 0xed048 | 21 | to charge in blindly. |
| 0xed05e | 41 | We still don't know who these guys are.\n |
| 0xed088 | 47 | For stuff like this, we need more information\n |
| 0xed0b8 | 6 | first. |
| 0xed0bf | 48 | It's hard to remember because of how she acts,\n |
| 0xed0f0 | 49 | but Atuy is the daughter of a fancy noble family. |
| 0xed122 | 48 | I don't know if we should just crash in before\n |
| 0xed153 | 41 | finding out WHY these guys are after her. |
| 0xed17d | 53 | Anyway, I just think we should find out more first.\n |
| 0xed1b3 | 45 | Investigate the mansion, tail them, all that. |
| 0xed1e1 | 31 | ...You might be right, I think. |
| 0xed201 | 43 | Whew, looks like she's calmed down a bit... |
| 0xed22d | 47 | Let's split up for now. Nekone, you know tons\n |
| 0xed25d | 47 | about the capital--you and Kuon scout the area. |
| 0xed28d | 11 | Understood. |
| 0xed299 | 46 | Rulutieh and I will watch the manor from here. |
| 0xed2c8 | 48 | As the sun sets, and lights glow within houses\n |
| 0xed2f9 | 46 | across the city, the young man and the valet\n |
| 0xed328 | 7 | emerge. |
| 0xed330 | 50 | Kuon and Nekone aren't back yet... Guess there's\n |
| 0xed363 | 40 | nothing for it. We'd better follow them. |
| 0xed38c | 48 | Rulutieh and I tail the two until they go into\n |
| 0xed3bd | 30 | a pub on the city's outskirts. |
| 0xed3dc | 49 | This pub seems a little shady for some rich boy\n |
| 0xed40e | 17 | to be visiting... |
| 0xed420 | 44 | I'll pretend to be a customer and head in.\n |
| 0xed44d | 42 | Rulutieh, I want you to head back to the\n |
| 0xed478 | 11 | Hakurokaku. |
| 0xed484 | 43 | Um, may I... not accompany you... inside,\n |
| 0xed4b0 | 9 | Sir Haku? |
| 0xed4ba | 49 | I know she wants to help Atuy, but she'll stick\n |
| 0xed4ec | 51 | out like a sore thumb in a hole-in-the-wall place\n |
| 0xed520 | 12 | like this... |
| 0xed52d | 49 | Well, if I go in a place like this with a girl,\n |
| 0xed55f | 49 | we might get unwanted attention. It sucks, but... |
| 0xed591 | 46 | Oh... I'm sorry. I suppose that was a little\n |
| 0xed5c0 | 38 | selfish of me... Please, be careful... |
| 0xed5e7 | 50 | Rulutieh smiles sadly, but she quickly hides it,\n |
| 0xed61a | 40 | murmuring only a word of caution for me. |
| 0xed643 | 50 | It'll be a walk in the park. All I have to do is\n |
| 0xed676 | 50 | buy a drink and listen in. Nothing to worry about. |
| 0xed6a9 | 39 | Yes, but still... Please, be careful... |
| 0xed6d1 | 52 | The "young master" seems to have joined a bunch of\n |
| 0xed706 | 48 | ruffians. They sit in the back, ordering drinks. |
| 0xed737 | 3 | Man |
| 0xed73b | 22 | So, how'd it go, boss? |
| 0xed752 | 48 | Heh, easy. She melted like butter. Fell for it\n |
| 0xed783 | 21 | immediately, she did. |
| 0xed799 | 50 | The slim man laughs crudely, his tone confident.\n |
| 0xed7cc | 43 | He explains what happened to his apparent\n |
| 0xed7f8 | 11 | companions. |
| 0xed804 | 43 | And so, off comes his pretty little mask.\n |
| 0xed830 | 17 | Just like that... |
| 0xed842 | 49 | ...So I even got her to promise to meet up with\n |
| 0xed874 | 9 | me again. |
| 0xed87e | 9 | Attendant |
| 0xed888 | 47 | So wha'bout this girl? Think we'll be able to\n |
| 0xed8b8 | 27 | squeeze any cash outta her? |
| 0xed8d4 | 35 | And of course, that one's no valet. |
| 0xed8f8 | 49 | Yeah. She's dressed fancy, and if she's staying\n |
| 0xed92a | 45 | at the Hakurokaku, she must be loaded, right? |
| 0xed958 | 49 | Must be from some rich family from the boonies.\n |
| 0xed98a | 44 | Who else talks in that hick Miyako dialect\n |
| 0xed9b7 | 11 | these days? |
| 0xed9c3 | 49 | Heheheh, seriously. Well, that just means she's\n |
| 0xed9f5 | 35 | gonna be all the easier to rope in. |
| 0xeda19 | 21 | So what happens next? |
| 0xeda2f | 49 | Our strategy all comes down to whatever they're\n |
| 0xeda61 | 35 | planning. Go on, let's hear it all. |
| 0xeda85 | 51 | Biggest catch we've ever had. With all that cash,\n |
| 0xedab9 | 45 | I'll marry in and live like a king for years. |
| 0xedae7 | 45 | Means we'll be able to lay low for a while,\n |
| 0xedb15 | 5 | then. |
| 0xedb1b | 48 | True. We've been conning people left and right\n |
| 0xedb4c | 45 | lately. The guards are starting to get antsy. |
| 0xedb7a | 44 | All right. Next time, you guys ambush her.\n |
| 0xedba7 | 45 | I'll jump in, save her, and she'll fall all\n |
| 0xedbd5 | 8 | over me. |
| 0xedbde | 48 | I mean, this sickly little noble's riskin' his\n |
| 0xedc0f | 37 | life for her. What lady could resist? |
| 0xedc35 | 49 | Man, you've never been sick a day in your life,\n |
| 0xedc67 | 48 | and you still look like a frail little rich boy. |
| 0xedc98 | 48 | That's the only reason this shit keeps working\n |
| 0xedcc9 | 44 | so well. Thank your lucky stars I'm such a\n |
| 0xedcf6 | 11 | pretty-boy. |
| 0xedd02 | 42 | Yeah, sure. Just don't forget we've been\n |
| 0xedd2d | 24 | handling the dirty work. |
| 0xedd46 | 51 | 'Course I won't. Once I'm married and everything,\n |
| 0xedd7a | 27 | you lads'll get your share. |
| 0xedd96 | 48 | Glad to hear it. That cash we got from selling\n |
| 0xeddc7 | 41 | off the last girl is starting to run out. |
| 0xeddf1 | 37 | So they've gotten to others before... |
| 0xede17 | 47 | I take a swig of the drink--predictably, it's\n |
| 0xede47 | 44 | awful--and then leave my money on the table. |
| 0xede74 | 47 | Heh, these girls fall for this shit every time. |
| 0xedea4 | 31 | Gahahahaha! You got that right! |
| 0xedec4 | 32 | Glad Kuon wasn't here this time. |
| 0xedee5 | 44 | Just remembering her expression earlier is\n |
| 0xedf12 | 37 | already giving me the heebie-jeebies. |
| 0xedf38 | 42 | You should all be thankful she's not here. |
| 0xedf63 | 44 | I leave behind the pub and the men's crude\n |
| 0xedf90 | 30 | laughter as I make my way out. |
| 0xedfaf | 42 | Doesn't seem like they were specifically\n |
| 0xedfda | 17 | targeting Atuy... |
| 0xedfec | 41 | Well that makes my job a little easier.\n |
| 0xee016 | 42 | Now, how to explain all this to Kuon and\n |
| 0xee041 | 11 | the others? |
| 0xee04d | 47 | Makes me feel like I'm siccing a crazed tiger\n |
| 0xee07d | 13 | on someone... |
| 0xee08b | 47 | Still, they're the ones who trod on its tail.\n |
| 0xee0bb | 36 | Everyone gets what's coming to them. |
| 0xee0e0 | 44 | ...Problem is, I need to figure out how to\n |
| 0xee10d | 21 | explain this to Atuy. |
| 0xee123 | 50 | Hm... Well... Guess I'll just let things play out. |
| 0xee156 | 31 | It'll all work out... probably. |
| 0xf17bc | 44 | Around sunset, a message from the slim man\n |
| 0xf17e9 | 42 | arrives. Atuy begins dressing up, beaming. |
| 0xf1814 | 34 | ...Well, someone's in a good mood. |
| 0xf1837 | 51 | Hee hee, well, I happened to help out a stranger,\n |
| 0xf186b | 40 | and they said they'd treat me to dinner. |
| 0xf1894 | 38 | Oh yeah? Sounds like a real gentleman. |
| 0xf18bb | 37 | Oh, he IS. He was such a dreamboat!\n |
| 0xf18e1 | 40 | This could be the start of my very own\n |
| 0xf190a | 11 | love story. |
| 0xf1916 | 46 | This love of hers is going to be over before\n |
| 0xf1945 | 47 | it even starts... but I can't say that to her\n |
| 0xf1975 | 5 | face. |
| 0xf197b | 46 | Really now? Well, hope you have a nice night\n |
| 0xf19aa | 4 | out. |
| 0xf19af | 33 | Thanks. I'm going to try my best. |
| 0xf19d1 | 44 | I see the giddy Atuy off to the front door\n |
| 0xf19fe | 20 | and watch her leave. |
| 0xf1a13 | 42 | ...*Sigh* I still feel guilty about this\n |
| 0xf1a3e | 12 | whole thing. |
| 0xf1a4b | 33 | Shall we get going as well, then? |
| 0xf1a6d | 47 | Whoa--Geez, would you not sneak up on me like\n |
| 0xf1a9d | 5 | that? |
| 0xf1aa3 | 46 | Remember the plan. Hide, follow Atuy, and if\n |
| 0xf1ad2 | 45 | anything bad happens, we act. That would be\n |
| 0xf1b00 | 14 | best, I think. |
| 0xf1b0f | 46 | I'm sure Atuy can handle anything that comes\n |
| 0xf1b3e | 44 | her way, but we should be prepared for the\n |
| 0xf1b6b | 6 | worst. |
| 0xf1b72 | 44 | Kuon's smiling as she speaks, but her tail\n |
| 0xf1b9f | 45 | flicks and twists in short, violent motions\n |
| 0xf1bcd | 8 | as well. |
| 0xf1bd6 | 42 | That's usually a sign she's in a bad mood. |
| 0xf1c01 | 44 | She seems really worked up about all this... |
| 0xf1c2e | 50 | She's been like this ever since I explained what\n |
| 0xf1c61 | 32 | I heard about those guys' plans. |
| 0xf1c82 | 45 | You know, if Haku had apprehended those men\n |
| 0xf1cb0 | 46 | on the spot, we would not have to go through\n |
| 0xf1cdf | 9 | all this. |
| 0xf1ce9 | 44 | It's one thing to confront them AFTER they\n |
| 0xf1d16 | 44 | actually do something, but doing it BEFORE\n |
| 0xf1d43 | 12 | gets tricky. |
| 0xf1d50 | 45 | And you're asking the impossible! How can I\n |
| 0xf1d7e | 46 | "apprehend" them alone? They'd beat the shit\n |
| 0xf1dad | 10 | out of me. |
| 0xf1db8 | 18 | Um, dear sister... |
| 0xf1dcb | 46 | Are you sure we should not inform Atuy about\n |
| 0xf1dfa | 36 | this...? If her feelings are hurt... |
| 0xf1e23 | 50 | If we don't have any proof to back up what we're\n |
| 0xf1e56 | 38 | saying, she might not even believe us. |
| 0xf1e7d | 51 | ...Hm. You do have a point. I do not believe that\n |
| 0xf1eb1 | 37 | Atuy has full trust in you yet, Haku. |
| 0xf1ed7 | 49 | People tend not to believe in truths that might\n |
| 0xf1f09 | 25 | mean bad things for them. |
| 0xf1f23 | 49 | And what if she asks HIM and he says I misheard\n |
| 0xf1f55 | 44 | them? Then this would just get even messier. |
| 0xf1f82 | 24 | You're probably right... |
| 0xf1f9b | 48 | Urgh, I... I see. But could we not have solved\n |
| 0xf1fcc | 45 | this all behind Atuy's back? Was that not a\n |
| 0xf1ffa | 12 | possibility? |
| 0xf2007 | 23 | You mean your big plan? |
| 0xf201f | 49 | Yes! If we follow my plan, this will all end up\n |
| 0xf2051 | 45 | a pleasant memory for Atuy, and nobody will\n |
| 0xf207f | 9 | get hurt. |
| 0xf2089 | 46 | Nekone pridefully puffs out her chest with a\n |
| 0xf20b8 | 26 | triumphant little chuckle. |
| 0xf20d3 | 52 | Right, the plan... Take down the conmen ourselves,\n |
| 0xf2108 | 50 | disguise one of us as the guy, and go on the date. |
| 0xf213b | 47 | And afterwards, we say the guy left on a long\n |
| 0xf216b | 50 | journey, and let Atuy have her emotional farewell. |
| 0xf219e | 47 | ...The end in particular sounds more like the\n |
| 0xf21ce | 46 | synopsis of a cheap novel than an actual plan. |
| 0xf21fd | 31 | Yeah, that's not going to work. |
| 0xf221d | 47 | Wh-Why do you say that? Are you not concerned\n |
| 0xf224d | 10 | for Atuy!? |
| 0xf2258 | 48 | Sure I am... But why do you think neither Kuon\n |
| 0xf2289 | 33 | nor Rulutieh agreed to that plan? |
| 0xf22ab | 7 | Huh...? |
| 0xf22b3 | 13 | Um... well... |
| 0xf22c1 | 23 | Ahem, *cough, cough*... |
| 0xf22d9 | 28 | Dear sister...? Rulutieh...? |
| 0xf22f6 | 35 | Well, there are a lot of reasons.\n |
| 0xf231a | 42 | The disguise part actually isn't so bad,\n |
| 0xf2345 | 27 | since she barely knows him. |
| 0xf2361 | 47 | Putting aside how we're supposed to even make\n |
| 0xf2391 | 20 | a disguise of him... |
| 0xf23a6 | 31 | Of course it is not a bad idea. |
| 0xf23c6 | 47 | ...So which one of us is supposed to play the\n |
| 0xf23f6 | 5 | part? |
| 0xf23fc | 16 | Well, that is... |
| 0xf240d | 47 | I obviously can't do it because of my height.\n |
| 0xf243d | 44 | And even if that wasn't a problem, there's\n |
| 0xf246a | 14 | our physiques. |
| 0xf2479 | 47 | If I remember right, that guy was a full head\n |
| 0xf24a9 | 48 | shorter than me. I think she'd notice that much. |
| 0xf24da | 23 | Nekone glances at Kuon. |
| 0xf24f2 | 47 | Awkwardness prevails as Kuon strains her neck\n |
| 0xf2522 | 13 | to look away. |
| 0xf2530 | 40 | Confused, Nekone then turns to Rulutieh. |
| 0xf255e | 47 | Rulutieh begins to frantically shake her head\n |
| 0xf258e | 18 | from side to side. |
| 0xf25a1 | 28 | Yeah, that's what I thought. |
| 0xf25be | 41 | From the looks of it, Kuon's a loner...\n |
| 0xf25e8 | 31 | I mean, not a social butterfly. |
| 0xf2608 | 46 | She's talented, but if you asked her to play\n |
| 0xf2637 | 47 | a dashing and charming nobleman, she might...\n |
| 0xf2667 | 18 | have some trouble. |
| 0xf267a | 45 | And judging by her reaction, she's probably\n |
| 0xf26a8 | 20 | fully aware of this. |
| 0xf26bd | 46 | Rulutieh also would have problems with this,\n |
| 0xf26ec | 37 | just because of who she is by nature. |
| 0xf2712 | 47 | You went into a lot of detail, but theory and\n |
| 0xf2742 | 41 | practice are entirely different things.\n |
| 0xf276c | 28 | It won't be as easy as that. |
| 0xf2789 | 47 | Not to mention this all centers around a love\n |
| 0xf27b9 | 50 | affair. That'll be rough for the disguised person. |
| 0xf27ec | 52 | Um... Sorry, Nekone. I'd be glad to take an active\n |
| 0xf2821 | 38 | role, but if that plan were to fail... |
| 0xf2848 | 45 | N-No, you are not at fault here, dear sister. |
| 0xf2876 | 45 | When I think about it, she is a good actor.\n |
| 0xf28a4 | 53 | I guess only when it involves trickery and deceit...? |
| 0xf28da | 33 | ...Did I hear something just now? |
| 0xf28fc | 30 | N-Nope. I didn't say anything. |
| 0xf291b | 46 | A-Anyways, seeing as failure isn't really an\n |
| 0xf294a | 45 | option, we can't go through with your plan,\n |
| 0xf2978 | 7 | Nekone. |
| 0xf2980 | 7 | Nngh... |
| 0xf2988 | 51 | And this is Atuy we're talking about. If she sees\n |
| 0xf29bc | 48 | an obstacle in her way, she'd just get fired up. |
| 0xf29ed | 52 | If we do something that makes her go nuts, there's\n |
| 0xf2a22 | 33 | no way we'll be able to stop her. |
| 0xf2a44 | 46 | Don't let it get you down. You're smart, but\n |
| 0xf2a73 | 45 | you're still just a kid. It's OK to not get\n |
| 0xf2aa1 | 14 | adult matters. |
| 0xf2ab0 | 9 | *Thwack!* |
| 0xf2aba | 8 | Hnngah!? |
| 0xf2ac3 | 49 | That was supposed to be a good piece of advice!\n |
| 0xf2af5 | 33 | Why did she kick me in the shins? |
| 0xf2b17 | 37 | An open area beyond a deserted alley. |
| 0xf2b3d | 45 | Atuy stands there, excitedly looking around\n |
| 0xf2b6b | 16 | in anticipation. |
| 0xf2b7c | 45 | It appears as though they are not here yet... |
| 0xf2baa | 50 | We loiter at a distance, far enough that neither\n |
| 0xf2bdd | 38 | Atuy nor the ruffians would notice us. |
| 0xf2c04 | 5 | Oh... |
| 0xf2c0a | 45 | After a while, the men from the pub appear,\n |
| 0xf2c38 | 24 | slowly surrounding Atuy. |
| 0xf2c51 | 15 | They're here... |
| 0xf2c61 | 50 | Didn't think they'd go straight for her, though.\n |
| 0xf2c94 | 34 | They're making it way too obvious. |
| 0xf2cb7 | 4 | Thug |
| 0xf2cbc | 52 | Hey there, beautiful. What're you doin' in a place\n |
| 0xf2cf1 | 26 | like this all by yourself? |
| 0xf2d0c | 49 | Heh heh heh. How about you spend some time with\n |
| 0xf2d3e | 33 | us, if you're free for the night? |
| 0xf2d60 | 45 | Um... Wasn't that person over there the one\n |
| 0xf2d8e | 31 | pretending to be the attendant? |
| 0xf2dae | 47 | What? You're right... Are these guys serious?\n |
| 0xf2dde | 37 | Do they even know what they're doing? |
| 0xf2e04 | 50 | It sounded like they've used this plan for quite\n |
| 0xf2e37 | 46 | a while now. I suppose they might be getting\n |
| 0xf2e66 | 9 | careless. |
| 0xf2e70 | 41 | So what Haku was saying was true, then... |
| 0xf2e9a | 46 | ...Wait, you didn't believe me until just now? |
| 0xf2ecb | 48 | No, I did believe. Dear sister seemed to trust\n |
| 0xf2efc | 44 | you, so... there's no reason for me not to\n |
| 0xf2f29 | 10 | trust you. |
| 0xf2f34 | 9 | ...Right. |
| 0xf2f3e | 50 | But even Atuy would be able to catch on if these\n |
| 0xf2f71 | 31 | guys are being this careless... |
| 0xf2f91 | 48 | I kinda feel bad for her, but this is probably\n |
| 0xf2fc2 | 45 | for the best before she actually gets hurt... |
| 0xf2ff0 | 49 | But Atuy doesn't even seem to notice the thugs.\n |
| 0xf3022 | 33 | She keeps eagerly looking around. |
| 0xf3044 | 44 | Being ignored... does not seem to sit well\n |
| 0xf3071 | 29 | with her would-be assailants. |
| 0xf308f | 46 | Oh, you waitin' out here for someone, little\n |
| 0xf30be | 6 | missy? |
| 0xf30c5 | 49 | Forget that guy. Come have some real fun with us. |
| 0xf30f7 | 47 | Heh heh heh... yeah. We'll take you somewhere\n |
| 0xf3127 | 13 | real special. |
| 0xf3135 | 42 | Hmmm...? Oh, sorry, but do you have some\n |
| 0xf3160 | 17 | business with me? |
| 0xf3172 | 48 | ...Tch. We're asking if you wanna go have some\n |
| 0xf31a3 | 12 | fun with us. |
| 0xf31b0 | 42 | Yeah, we'll show you a reeeaaal good time. |
| 0xf31db | 30 | Ohhh, so that's what it was.\n |
| 0xf31fa | 25 | You were hitting on me... |
| 0xf3214 | 51 | Hee hee, guess I'm not such a lost cause after all. |
| 0xf3248 | 50 | Sorry, boys, but none of you are really my type.\n |
| 0xf327b | 26 | Better luck next time, eh? |
| 0xf3296 | 7 | ...Huh? |
| 0xf329e | 27 | U-Um... Could it be that... |
| 0xf32ba | 40 | Atuy... has not noticed at all, has she? |
| 0xf32e3 | 51 | Maybe she has so little interest in them that she\n |
| 0xf3317 | 39 | hasn't even bothered to look at them... |
| 0xf333f | 51 | What's that? Don't get all high and mighty on us,\n |
| 0xf3373 | 12 | little girl. |
| 0xf3380 | 49 | We don't mind, really. We can have just as much\n |
| 0xf33b2 | 13 | fun here too. |
| 0xf33c0 | 5 | Thugs |
| 0xf33c6 | 12 | Geheheheheh! |
| 0xf33d3 | 34 | ...You boys kinda smell, you know? |
| 0xf33f6 | 36 | Your clothes are all so ugly, too.\n |
| 0xf341b | 42 | You should pay more attention to how you\n |
| 0xf3446 | 19 | present yourselves. |
| 0xf345a | 50 | ...I bet you boys have trouble picking up girls,\n |
| 0xf348d | 10 | don't you? |
| 0xf3498 | 46 | Wh-What!? You saying we don't get the ladies!? |
| 0xf34c7 | 48 | 'Course we get the girls! They're all over us!\n |
| 0xf34f8 | 14 | All the time!! |
| 0xf3507 | 45 | Mm... Boys, deceiving yourself is never the\n |
| 0xf3535 | 45 | answer. You have to wake up and face reality. |
| 0xf3563 | 29 | That's none of your business! |
| 0xf3581 | 51 | You little bitch! You think you can get away with\n |
| 0xf35b5 | 50 | sayin' that shit just 'cause you're kinda cute!?\n |
| 0xf35e8 | 5 | Huh!? |
| 0xf35ee | 8 | Chalafun |
| 0xf35f7 | 44 | Halt!! You scoundrels! Step away from Atuy!! |
| 0xf3624 | 15 | Oh, Chalafun... |
| 0xf3634 | 45 | Are you unhurt, Atuy? You must have been so\n |
| 0xf3662 | 44 | scared... but fear not. I have come for you. |
| 0xf368f | 51 | ...Hm? Scared...? But what's there to be scared of? |
| 0xf36c3 | 46 | O-Oh... Y-Yes, your stoutheartedness is also\n |
| 0xf36f2 | 24 | one of your many charms. |
| 0xf370b | 38 | Hee hee! Oh, you flatter me, Chalafun. |
| 0xf3732 | 48 | Atuy seems completely oblivious, dithering and\n |
| 0xf3763 | 34 | blushing in girlish embarrassment. |
| 0xf3786 | 43 | U-Uh... And who do you think you are, you\n |
| 0xf37b2 | 13 | little shit!? |
| 0xf37c0 | 43 | Heh! You think you're so cool, pretty-boy!? |
| 0xf37ec | 47 | You think you can take us on with that skinny\n |
| 0xf381c | 12 | little body? |
| 0xf3829 | 52 | Hah. The size of my body matters not. I shall stop\n |
| 0xf385e | 27 | anyone who dares harm Atuy. |
| 0xf387a | 50 | Whoa, looks like we got a tough guy! Guess we'll\n |
| 0xf38ad | 33 | have to beat you down first then! |
| 0xf38cf | 35 | Geheheheh! Lemme hear you scream!\n |
| 0xf38f3 | 45 | What kind of sounds're you gonna make after\n |
| 0xf3921 | 21 | we're done with you!? |
| 0xf3937 | 46 | The ruffians raise their arms as they slowly\n |
| 0xf3966 | 9 | close in. |
| 0xf3970 | 16 | Atuy, stay back. |
| 0xf3981 | 45 | So, where are you going to take me tonight?\n |
| 0xf39af | 23 | Ooh, I can hardly wait! |
| 0xf39c7 | 9 | Uh, Atuy? |
| 0xf39d1 | 24 | Quit ignoring us, bitch! |
| 0xf39ea | 49 | You think this is some kinda joke or somethin'?\n |
| 0xf3a1c | 34 | Are we going to go watch a show?\n |
| 0xf3a3f | 48 | Ooh, or maybe we could just go clothes shopping! |
| 0xf3a70 | 11 | Er, well... |
| 0xf3a7c | 7 | Hello!? |
| 0xf3a84 | 30 | At least look at us, dammit!\n |
| 0xf3aa3 | 12 | LOOK AT US!! |
| 0xf3ab0 | 31 | ...Oh, you were all still here? |
| 0xf3ad0 | 26 | Yeah! The whole damn time! |
| 0xf3aeb | 47 | Oh dear. You know, if I were you, I'd go have\n |
| 0xf3b1b | 38 | a bath instead of hanging around here. |
| 0xf3b42 | 33 | You should learn from Chalafun!\n |
| 0xf3b64 | 46 | Your faces may be hopeless, but you could be\n |
| 0xf3b93 | 25 | a bit easier on the eyes. |
| 0xf3bad | 44 | ...You're gonna pay for this, you asshole... |
| 0xf3bda | 41 | H-Hold it. I didn't say it, she did...!\n |
| 0xf3c04 | 42 | N-Now begone, scum, or I shall teach you\n |
| 0xf3c2f | 9 | a lesson! |
| 0xf3c39 | 44 | Heh, fine by me! We'll beat you down until\n |
| 0xf3c66 | 29 | you're never gettin' back up! |
| 0xf3c84 | 48 | You fools. You shall regret your decision soon\n |
| 0xf3cb5 | 7 | enough. |
| 0xf3cbd | 24 | ...Ohhh, I get it now.\n |
| 0xf3cd6 | 20 | So that's how it is. |
| 0xf3ceb | 4 | Huh? |
| 0xf3cf0 | 3 | Uh? |
| 0xf3cf4 | 47 | Sorry I didn't notice earlier, but you really\n |
| 0xf3d24 | 42 | should've told me sooner if that was the\n |
| 0xf3d4f | 5 | case. |
| 0xf3d55 | 48 | I was wondering why you were still hanging out\n |
| 0xf3d86 | 47 | around here, but you wanted some fun with me,\n |
| 0xf3db6 | 4 | huh? |
| 0xf3dbb | 34 | Uh... Yeah, that's what we said.\n |
| 0xf3dde | 35 | Did you really only realize now...? |
| 0xf3e02 | 37 | This girl really is a nut, ain't she? |
| 0xf3e28 | 43 | What are you saying, Atuy? Do not worry--\n |
| 0xf3e54 | 26 | I shall dispose of them... |
| 0xf3e6f | 32 | Well, let's have a go, shall we? |
| 0xf3e90 | 11 | Fgyaaaarh!? |
| 0xf3e9c | 52 | In an instant, with a thunderous sound, one of the\n |
| 0xf3ed1 | 45 | ruffians' face swells into a malformed shape. |
| 0xf3eff | 47 | It takes a second for me to realize it's from\n |
| 0xf3f2f | 43 | Atuy just slapping the guy across the face. |
| 0xf3f5b | 18 | Augh... Hrgghhh... |
| 0xf3f6e | 47 | Of course, the amount of force was incredible\n |
| 0xf3f9e | 16 | for just a slap. |
| 0xf3faf | 49 | His face looks practically caved in, and we can\n |
| 0xf3fe1 | 48 | see his teeth askew past the blood dripping out. |
| 0xf4012 | 6 | Wh...? |
| 0xf4019 | 48 | All the ruffians stand staring dumbly at Atuy,\n |
| 0xf404a | 47 | as if they can't comprehend what just happened. |
| 0xf407a | 37 | What, you're not even going to dodge? |
| 0xf40a0 | 37 | Wh-Wh-Wh-What the FUCK was that for!? |
| 0xf40c6 | 45 | Y-You bitch! We were taking it easy on you,\n |
| 0xf40f4 | 37 | and you just take advantage of that!? |
| 0xf411a | 20 | You'll pay for that! |
| 0xf412f | 7 | W-Wait! |
| 0xf4137 | 48 | Two of the thugs swing at Atuy, but she stands\n |
| 0xf4168 | 48 | there nonchalantly, with no apparent intent to\n |
| 0xf4199 | 5 | move. |
| 0xf419f | 12 | Gfaaaaaah... |
| 0xf41ac | 12 | Grbraaaah... |
| 0xf41b9 | 50 | With two sharp sounds, the two men roll and skid\n |
| 0xf41ec | 50 | across the alley pavement until they hit the wall. |
| 0xf421f | 21 | Wh-Who IS this girl!? |
| 0xf4235 | 28 | I-I-I-I'll fuckin' KILL you! |
| 0xf4252 | 45 | The remaining men come to, and quickly draw\n |
| 0xf4280 | 24 | daggers and shortswords. |
| 0xf4299 | 22 | Y-You idio--Hey, stop! |
| 0xf42b0 | 47 | Don't think you're gettin' off easy for this!\n |
| 0xf42e0 | 23 | I'll cut you to pieces! |
| 0xf42f8 | 34 | It's too late to grovel and beg.\n |
| 0xf431b | 48 | I'm gonna make your pretty face bleed all over\n |
| 0xf434c | 13 | these stones. |
| 0xf435a | 44 | Ooooh! Is that how we're going to play next? |
| 0xf4387 | 45 | Atuy grins in delight, and she opens up the\n |
| 0xf43b5 | 31 | object she carries on her back. |
| 0xf43d5 | 16 | Wh-What the...!? |
| 0xf43e6 | 49 | The terrifying two-pronged spear unfolds to its\n |
| 0xf4418 | 23 | full size in her hands. |
| 0xf4430 | 40 | Th-This girl... She's fucking crazy...\n |
| 0xf4459 | 23 | Come on, do your thing! |
| 0xf4471 | 7 | Got it! |
| 0xf4479 | 51 | One of the ruffians opens up a cage at his waist.\n |
| 0xf44ad | 35 | Dangerous-looking bugs skitter out. |
| 0xf44d1 | 49 | These're some of the most venomous bugs I could\n |
| 0xf4503 | 50 | find. One sting, and you'll be in agony 'til you\n |
| 0xf4536 | 4 | die. |
| 0xf453b | 33 | You think we're a joke, huh...?\n |
| 0xf455d | 46 | Well, now you've done it... You pissed us off! |
| 0xf458c | 48 | Heh... Heh heh heh... It's too late to cry for\n |
| 0xf45bd | 12 | mercy now... |
| 0xf45ca | 9 | *Wriggle* |
| 0xf45d4 | 21 | *Fwoop, fwoop, fwoop* |
| 0xf45ea | 44 | Kurarin leaves the top of Atuy's head, and\n |
| 0xf4617 | 41 | reaches out to nimbly snatch up the bugs. |
| 0xf4641 | 23 | *Crunch, munch, crunch* |
| 0xf4659 | 9 | WHAAAAT!? |
| 0xf4663 | 51 | Kurarin! What have I told you about eating things\n |
| 0xf4697 | 47 | off the ground? What if you make yourself sick? |
| 0xf46c7 | 24 | *Jiggle, jiggle, jiggle* |
| 0xf46e0 | 30 | *Fwoop, crunch, fwoop, crunch* |
| 0xf46ff | 25 | A-AHHHHHHH!? M-My bugs!\n |
| 0xf4719 | 17 | My precious bugs! |
| 0xf472b | 24 | *Crunch, crunch, crunch* |
| 0xf4744 | 38 | S-Stop! Please, I'm begging you! Stop! |
| 0xf476b | 50 | They're not venomous, I was just trying to scare\n |
| 0xf479e | 49 | you--th-they just paralyze you for a little bit!! |
| 0xf47d0 | 18 | PLEASE! STOOOOOP!! |
| 0xf47e3 | 10 | Whaaaat... |
| 0xf47ee | 42 | But... I've barely even done anything yet. |
| 0xf4819 | 51 | Oh well. I guess this is my chance to show myself\n |
| 0xf484d | 16 | off to Chalafun! |
| 0xf485e | 39 | Keep your eyes on me now, OK, Chalafun? |
| 0xf4886 | 47 | Suddenly... a palpable menace descends on the\n |
| 0xf48b6 | 46 | air in the area. It feels dark and oppressive. |
| 0xf48e5 | 46 | ...It's all Atuy. If she actually intends on\n |
| 0xf4914 | 52 | killing them, the pressure alone could stop a heart. |
| 0xf4949 | 44 | A simple thug has no chance of standing up\n |
| 0xf4976 | 23 | to something like this. |
| 0xf498e | 30 | Eeeeeeeek! Please! Spare me!\n |
| 0xf49ad | 19 | I-I'll do anything! |
| 0xf49c1 | 41 | I'm so sorry! I'll never do this again!\n |
| 0xf49eb | 23 | Please! Don't kill me!! |
| 0xf4a03 | 11 | ...Oh dear. |
| 0xf4a0f | 45 | But I haven't even gotten to do anything yet. |
| 0xf4a3d | 49 | Oh well. I guess I ought to finish this up, then. |
| 0xf4a6f | 48 | The ruffians are frozen in terror. Atuy scoops\n |
| 0xf4aa0 | 47 | them both up by the necks, in the gap between\n |
| 0xf4ad0 | 11 | the prongs. |
| 0xf4adc | 21 | Hee hee, what a haul! |
| 0xf4af2 | 49 | It almost looks like she's holding some kind of\n |
| 0xf4b24 | 26 | giant skewer in her hands. |
| 0xf4b3f | 12 | Oh, right... |
| 0xf4b4c | 51 | Thanks for being so concerned about me, Chalafun.\n |
| 0xf4b80 | 20 | I was sooo scared... |
| 0xf4b95 | 49 | Atuy bashfully looks at the slim man, eyelashes\n |
| 0xf4bc7 | 49 | fluttering... the thugs hanging limply from the\n |
| 0xf4bf9 | 20 | spearhead above her. |
| 0xf4c0e | 48 | Well, shall we get going, then? I'd still love\n |
| 0xf4c3f | 47 | to know where you were planning on taking me... |
| 0xf4c6f | 50 | Atuy eagerly sidles up, her voice still carrying\n |
| 0xf4ca2 | 12 | a cute lilt. |
| 0xf4caf | 12 | ...Chalafun? |
| 0xf4cbc | 31 | Atuy looks into the man's face. |
| 0xf4cdc | 5 | Eep!? |
| 0xf4ce2 | 48 | The man suddenly breaks free from being frozen\n |
| 0xf4d13 | 50 | with terror, staggers back, and falls on his rear. |
| 0xf4d46 | 44 | ...A pungent, sharp odor gradually becomes\n |
| 0xf4d73 | 11 | noticeable. |
| 0xf4d7f | 20 | AAAAAAAAHHHHHHHHHH!! |
| 0xf4d94 | 49 | And with a scream of sheer terror, he scrambles\n |
| 0xf4dc6 | 48 | away on all fours, desperately trying to escape. |
| 0xf4df7 | 45 | Atuy, clearly unsure of what just happened,\n |
| 0xf4e25 | 31 | stands dumbfounded and forlorn. |
| 0xf4e45 | 8 | Another! |
| 0xf4e4e | 45 | Atuy empties her tenth glass in one go, and\n |
| 0xf4e7c | 20 | demands another cup. |
| 0xf4e91 | 8 | ANOTHER! |
| 0xf4e9a | 37 | Maybe it's time to slow down there.\n |
| 0xf4ec0 | 34 | I think you've had enough already. |
| 0xf4ee3 | 46 | Those damn girls forced Atuy on me and left!\n |
| 0xf4f12 | 45 | I'm no expert, but aren't girls supposed to\n |
| 0xf4f40 | 39 | console each other for stuff like this? |
| 0xf4f68 | 37 | Nooooo, I'm not drunk at allllll yet. |
| 0xf4f8e | 48 | I'm pretty sure saying classic lines like that\n |
| 0xf4fbf | 30 | is when you KNOW you're drunk. |
| 0xf4fde | 39 | Pfaaaah, this drink is what I live for. |
| 0xf5006 | 46 | *Sigh* Fine. I guess I can let her do as she\n |
| 0xf5035 | 30 | pleases for tonight, at least. |
| 0xf5054 | 44 | Mister! Can I get some tripe stew over here? |
| 0xf5081 | 4 | Cook |
| 0xf5086 | 11 | You got it. |
| 0xf5092 | 31 | ...If things had gone my way... |
| 0xf50b2 | 49 | If only things had gone my way, this would have\n |
| 0xf50e4 | 43 | been the start of a beautiful love story... |
| 0xf5110 | 19 | I don't know why... |
| 0xf5124 | 40 | Why? Why...? Why does this happen, love? |
| 0xf514d | 34 | Great. She's a complainer-drunk.\n |
| 0xf5170 | 33 | I didn't know she got this bad... |
| 0xf5192 | 44 | Her eyes droop heavily as she continues on\n |
| 0xf51bf | 26 | with her drunken rambling. |
| 0xf51da | 45 | Something about this is still a little odd,\n |
| 0xf5208 | 47 | but now she's talking nonstop as she complains. |
| 0xf5238 | 47 | Honestly, she feels a lot more relatable than\n |
| 0xf5268 | 44 | usual, but I'm not sure that's a good thing. |
| 0xf5295 | 48 | Tell me something, love... Am I not attractive\n |
| 0xf52c6 | 10 | as a girl? |
| 0xf52d1 | 48 | Er... Well, I'd say nine out of ten guys would\n |
| 0xf5302 | 29 | probably find you attractive. |
| 0xf5320 | 29 | Really? You really mean that? |
| 0xf533e | 49 | She's got curves in all the right places, so as\n |
| 0xf5370 | 49 | long as they don't find out how weird she gets... |
| 0xf53a2 | 38 | Then why do they all run away from me? |
| 0xf53c9 | 48 | Atuy leans towards me to get closer, intent on\n |
| 0xf53fa | 18 | hearing my answer. |
| 0xf540d | 53 | I feel said curves pressing up against me slightly,\n |
| 0xf5443 | 34 | and I try to edge delicately back. |
| 0xf5466 | 52 | ...Maybe they've got... specific tastes? You know,\n |
| 0xf549b | 42 | like they like younger girls or something. |
| 0xf54c6 | 48 | I'm pretty sure that terrifying presence would\n |
| 0xf54f7 | 22 | scare off most guys... |
| 0xf550e | 48 | I can't bring myself to tell her the truth, so\n |
| 0xf553f | 31 | I fumble out some other reason. |
| 0xf555f | 47 | I was pretty far from her, but I was about to\n |
| 0xf558f | 45 | collapse on the spot after feeling that aura. |
| 0xf55bd | 50 | Hm? Wait, maybe that's why Kuon grabbed Rulutieh\n |
| 0xf55f0 | 25 | and Nekone and ran off... |
| 0xf560a | 46 | Now that I think about it, Nekone was on the\n |
| 0xf5639 | 46 | verge of tears. It must've really spooked her. |
| 0xf5668 | 48 | She may be a genius, but she's still just a kid. |
| 0xf5699 | 9 | Pfaaaaah! |
| 0xf56a3 | 49 | To be honest, there's really nothing wrong with\n |
| 0xf56d5 | 12 | her looks... |
| 0xf56e2 | 52 | I see. Well, I suppose it wouldn't have worked out\n |
| 0xf5717 | 41 | if we didn't have any common interests... |
| 0xf5741 | 45 | You shouldn't worry about it. I know you'll\n |
| 0xf576f | 30 | eventually find the right guy. |
| 0xf578e | 22 | Really!? You think so? |
| 0xf57a5 | 28 | Here you go, one tripe stew. |
| 0xf57c2 | 41 | Yeah. *Munch, munch* Pfah, desh hoht...\n |
| 0xf57ec | 50 | You aren't planning on giving up already, are you? |
| 0xf581f | 53 | I mean, that's why you came to the imperial capital\n |
| 0xf5855 | 29 | in the first place, isn't it? |
| 0xf5873 | 49 | Oh... you're right. If I give up because of one\n |
| 0xf58a5 | 45 | little setback, I'll never find my true love. |
| 0xf58d3 | 52 | Hey, some stewed clams and grilled fish please...?\n |
| 0xf5908 | 46 | There you go. There's always next time, right? |
| 0xf5937 | 47 | Here you go, an order of stewed clams and one\n |
| 0xf5967 | 13 | grilled fish. |
| 0xf5975 | 51 | I try to end the conversation there. I don't know\n |
| 0xf59a9 | 35 | how much longer I can cheer her up. |
| 0xf59cd | 36 | You know what, love, you're right!\n |
| 0xf59f2 | 48 | The past is the past. It's time to look to the\n |
| 0xf5a23 | 18 | men of the future! |
| 0xf5a36 | 33 | In that case, here's to new love. |
| 0xf5a58 | 46 | Hee hee! I'm going to drink until I pass out\n |
| 0xf5a87 | 45 | tonight. No more sad thoughts in the morning! |
| 0xf5ab5 | 8 | ...What? |
| 0xf5abe | 45 | Hey, buddy, we're closing up soon, and your\n |
| 0xf5aec | 46 | lady's out cold. Can I ask you to pack it up\n |
| 0xf5b1b | 13 | and head out? |
| 0xf5b29 | 32 | Yeah, sorry for staying so long. |
| 0xf5b4a | 47 | No worries. A pub is where people go to drink\n |
| 0xf5b7a | 47 | and talk about their lives, eh? You come back\n |
| 0xf5baa | 9 | any time. |
| 0xf5bb4 | 36 | I think I will. Thanks for the food. |
| 0xf5bd9 | 43 | I pay our bill and pick up Atuy... who is\n |
| 0xf5c05 | 22 | completely conked out. |
| 0xf5c1c | 50 | The cold morning air feels good after a night of\n |
| 0xf5c4f | 9 | drinking. |
| 0xf5c59 | 49 | Looks like she's even a handful for you, Kurarin. |
| 0xf5c8b | 47 | I can feel the soft weight of Atuy on my back\n |
| 0xf5cbb | 48 | and arms as I carry her. I talk to Kurarin for\n |
| 0xf5cec | 14 | a distraction. |
| 0xf5cfb | 50 | Kurarin extends a tentacle and pats my shoulder,\n |
| 0xf5d2e | 38 | as though to acknowledge my hard work. |
| 0xf5d55 | 21 | You know what, man?\n |
| 0xf5d6b | 17 | You're all right. |
| 0xf5d7d | 43 | Its tentacles waggle airily, as if to say\n |
| 0xf5da9 | 22 | "all in a day's work." |
| 0xf5dc0 | 5 | Nn... |
| 0xf5dc6 | 36 | Atuy's grip on me suddenly tightens. |
| 0xf5deb | 48 | I feel the back of my shirt dampening a little\n |
| 0xf5e1c | 29 | as she buries her face in it. |
| 0xf5e3a | 40 | ...Guess it's not that easy to get over. |
| 0xf5e63 | 49 | Ah, well. For her sake, I'll deal with it, just\n |
| 0xf5e95 | 10 | this once. |
| 0xf6bc9 | 47 | Hey, Rulutieh, how about we make a hotpot for\n |
| 0xf6bf9 | 8 | tonight? |
| 0xf6c02 | 42 | Ah, there should be some fish in season,\n |
| 0xf6c2d | 11 | actually... |
| 0xf6c39 | 44 | They have plenty of fat this time of year.\n |
| 0xf6c66 | 25 | They should be delicious. |
| 0xf6c80 | 40 | Fish, huh... Mm. That does sound good.\n |
| 0xf6ca9 | 22 | All right! Fish it is. |
| 0xf6cc0 | 47 | If you need a fishmonger, I know of one I can\n |
| 0xf6cf0 | 10 | recommend. |
| 0xf6cfb | 46 | The one across the street over there makes a\n |
| 0xf6d2a | 45 | point of keeping very fresh catches on offer. |
| 0xf6d58 | 49 | Well, if it's got a glowing review from Nekone,\n |
| 0xf6d8a | 22 | I think that seals it. |
| 0xf6da1 | 38 | Oh, yeah. Haku, any requests for food? |
| 0xf6dc8 | 47 | No, I've been wondering about something for a\n |
| 0xf6df8 | 47 | while. Why has Rulutieh been cooking our meals? |
| 0xf6e28 | 48 | The inn has kitchen staff. She doesn't have to\n |
| 0xf6e59 | 32 | inconvenience herself like this. |
| 0xf6e7a | 47 | A-Ah, actually, Sir Haku... I'm doing this at\n |
| 0xf6eaa | 15 | my own request. |
| 0xf6eba | 7 | Really? |
| 0xf6ec2 | 43 | Y-Yes! I... I want to be of help somehow.\n |
| 0xf6eee | 35 | And I'm... good with cooking, so... |
| 0xf6f12 | 40 | Lady Kuon and the Hakurokaku staff are\n |
| 0xf6f3b | 45 | graciously allowing me to use the kitchens... |
| 0xf6f69 | 30 | Um. Is it... an inconvenience? |
| 0xf6f88 | 46 | O-Oh, no, not at all. Your cooking is always\n |
| 0xf6fb7 | 20 | excellent, Rulutieh. |
| 0xf6fd0 | 48 | I wouldn't mind if you cooked for me every day\n |
| 0xf7001 | 26 | from here on out, in fact. |
| 0xf701c | 15 | ...Dear sister. |
| 0xf702c | 44 | Yes, he probably doesn't even realize what\n |
| 0xf7059 | 32 | that just sounded like, I think. |
| 0xf707a | 34 | ...What are you two talking about? |
| 0xf709d | 46 | Clear the road! Make a path, and make it wide! |
| 0xf70cc | 3 | Hm? |
| 0xf70d0 | 45 | A loud voice suddenly cuts the conversation\n |
| 0xf70fe | 6 | short. |
| 0xf7105 | 43 | The crowd filling the marketplace splits,\n |
| 0xf7131 | 36 | moving to the sides of the street... |
| 0xf7156 | 19 | Wh-What's going on? |
| 0xf716a | 48 | If I recall correctly, today should be the day\n |
| 0xf719b | 7 | for it. |
| 0xf71a3 | 30 | Today? What's happening today? |
| 0xf71c2 | 23 | Well... Here they come. |
| 0xf71da | 48 | At the far end of the market street, a woptor-\n |
| 0xf720b | 30 | mounted group marches forward. |
| 0xf722a | 21 | Oh, it's Oshtor...?\n |
| 0xf7240 | 33 | Or... Huh? Something seems off... |
| 0xf7262 | 40 | Mm, they're flying a different banner.\n |
| 0xf728b | 44 | Unless I've missed my guess, that must be... |
| 0xf72b8 | 44 | Before long, the mounted figures draw near\n |
| 0xf72e5 | 36 | enough to be identified more easily. |
| 0xf730a | 48 | Each soldier is heavily armed and armored, and\n |
| 0xf733b | 40 | assembled as they are, they project an\n |
| 0xf7364 | 13 | imposing air. |
| 0xf7372 | 46 | One man in particularly fine armor leads his\n |
| 0xf73a1 | 37 | fellows, standing out from the group. |
| 0xf73c7 | 46 | More than likely, he's the commanding officer. |
| 0xf73f6 | 47 | The Imperial Guard of the Left, Lord Mikazuchi. |
| 0xf7426 | 18 | Mikazuchi? Then... |
| 0xf7439 | 29 | So he's Oshtor's counterpart? |
| 0xf7457 | 47 | Recalling rumors I'd heard before, I voice my\n |
| 0xf7487 | 16 | confusion aloud. |
| 0xf7498 | 49 | Yes. Together with my dear b--with Lord Oshtor,\n |
| 0xf74ca | 43 | he is famed as one of the Twin Shields of\n |
| 0xf74f6 | 7 | Yamato. |
| 0xf74fe | 46 | Today is his day to make his symbolic patrol\n |
| 0xf752d | 20 | of the city streets. |
| 0xf7542 | 34 | An officer equal to Oshtor, huh... |
| 0xf7565 | 38 | I guess the pomp and circumstance is\n |
| 0xf758c | 30 | understandable, then. Still... |
| 0xf75ab | 27 | I take a quick look around. |
| 0xf75c7 | 45 | The market street, previously bustling, has\n |
| 0xf75f5 | 25 | fallen completely silent. |
| 0xf760f | 48 | When Oshtor showed up on his patrol, the crowd\n |
| 0xf7640 | 41 | had cheered him. With this guy, though... |
| 0xf766a | 35 | Everyone seems to avert their eyes. |
| 0xf768e | 28 | Probably because of... that. |
| 0xf76ab | 34 | That terrifying aura he gives off. |
| 0xf76ce | 50 | While Oshtor's demeanor seems to embrace people,\n |
| 0xf7701 | 46 | this guy's feels more like a brandished sword. |
| 0xf7730 | 47 | It feels like I might cut myself if I get too\n |
| 0xf7760 | 44 | close... before I even get a chance to say\n |
| 0xf778d | 9 | anything. |
| 0xf7797 | 44 | The procession continues, and before long,\n |
| 0xf77c4 | 40 | the soldiers pass in front of our group. |
| 0xf77ed | 47 | Abruptly, Mikazuchi calls a halt and turns to\n |
| 0xf781d | 21 | stare directly at us. |
| 0xf7833 | 4 | Hrk. |
| 0xf7838 | 46 | His woptor comes to a stop, and his piercing\n |
| 0xf7867 | 30 | eyes bore straight through us. |
| 0xf7886 | 4 | Heh. |
| 0xf788b | 43 | He grins wolfishly, like a hunter finally\n |
| 0xf78b7 | 24 | catching up to its prey. |
| 0xf78d0 | 41 | Nekone hurriedly ducks behind me, hiding. |
| 0xf78fa | 8 | Wh--Hey! |
| 0xf7903 | 49 | The movement attracts his gaze, and inevitably,\n |
| 0xf7935 | 30 | those awful eyes settle on me. |
| 0xf7954 | 49 | Wha... What's this terrible sense of... dread...? |
| 0xf7986 | 45 | Letting his stare linger on me, Mikazuchi's\n |
| 0xf79b4 | 14 | smile widens-- |
| 0xf79c3 | 22 | Heh... Ah heh heh heh. |
| 0xf79da | 47 | Then, seemingly satisfied, he sets his woptor\n |
| 0xf7a0a | 13 | moving again. |
| 0xf7a18 | 8 | Heh heh. |
| 0xf7a21 | 46 | With his unsettling laughter echoing through\n |
| 0xf7a50 | 47 | the silent street, Mikazuchi leads his troops\n |
| 0xf7a80 | 7 | onward. |
| 0xf7a88 | 45 | The market crowd breathes a collective sigh\n |
| 0xf7ab6 | 10 | of relief. |
| 0xf7ac1 | 7 | Phew... |
| 0xf7ac9 | 41 | Nekone, too, finally seems to relax and\n |
| 0xf7af3 | 25 | steps out from behind me. |
| 0xf7b0d | 46 | So that was Mikazuchi, Imperial Guard of the\n |
| 0xf7b3c | 7 | Left... |
| 0xf7b44 | 31 | He seems like a scary person... |
| 0xf7b64 | 45 | Yeah. It was enough to frighten this little\n |
| 0xf7b92 | 24 | squirt, that's for sure. |
| 0xf7bb0 | 3 | Ow! |
| 0xf7bb4 | 31 | Little brat. N-Not the shins... |
| 0xf84fb | 47 | Hey, Haku. Wanna go on a shopping trip with me? |
| 0xf852b | 46 | The door suddenly opens, admitting Kuon into\n |
| 0xf855a | 45 | my room, where I've been relaxing with some\n |
| 0xf8588 | 4 | tea. |
| 0xf858d | 44 | I don't mind, but what are you planning on\n |
| 0xf85ba | 7 | buying? |
| 0xf85c2 | 46 | I was going to see if the produce market has\n |
| 0xf85f1 | 41 | the fresh fruit I need to make bath oils. |
| 0xf861b | 10 | Bath oils? |
| 0xf8626 | 44 | You haven't heard of it? You put it in the\n |
| 0xf8653 | 49 | water, and it gives off a fragrance and soothes\n |
| 0xf8685 | 10 | your skin. |
| 0xf8690 | 44 | One of the inn workers told me I could use\n |
| 0xf86bd | 45 | some in the baths, so I thought I'd make my\n |
| 0xf86eb | 4 | own. |
| 0xf86f0 | 46 | Oh, she must be talking about a bath additive. |
| 0xf871f | 46 | Hm? Additives, though...? Is it really OK to\n |
| 0xf874e | 29 | put those in a communal bath? |
| 0xf876c | 44 | The face of the inn's proprietress flashes\n |
| 0xf8799 | 16 | through my mind. |
| 0xf87aa | 46 | ...She's sure it won't be a big deal... right? |
| 0xf87d9 | 45 | I need a lot of fruit to make a full batch,\n |
| 0xf8807 | 35 | though, which is where you come in. |
| 0xf882b | 44 | Oh. You just want me to be a pack mule, in\n |
| 0xf8858 | 12 | other words. |
| 0xf8865 | 12 | Do you mind? |
| 0xf8872 | 32 | Eh. I'm not busy, so not really. |
| 0xf8893 | 25 | All right! Then let's go. |
| 0xf88ad | 39 | Kuon smiles and grabs ahold of my hand. |
| 0xf88d5 | 37 | Whoa, easy. Don't pull me so roughly. |
| 0xf88fb | 43 | And as usual, "bath" is the magic word to\n |
| 0xf8927 | 27 | unlock Kuon's enthusiasm... |
| 0xf8943 | 43 | I haven't been to the market here before.\n |
| 0xf896f | 42 | It's full of all kinds of fresh produce,\n |
| 0xf899a | 20 | fruit and otherwise. |
| 0xf89af | 47 | Fragrances both sweet and sour attack my nose\n |
| 0xf89df | 24 | from every single booth. |
| 0xf89f8 | 45 | Just looking at the colorful array of fruit\n |
| 0xf8a26 | 43 | laid out for sale is enough to excite and\n |
| 0xf8a52 | 12 | tantalize... |
| 0xf8a5f | 45 | To be expected of the center of the empire,\n |
| 0xf8a8d | 44 | I guess. There's stuff here I haven't even\n |
| 0xf8aba | 9 | heard of. |
| 0xf8ac4 | 48 | With a pensive look on her face, Kuon inspects\n |
| 0xf8af5 | 36 | a colorful, prickly-looking fruit... |
| 0xf8b1a | 45 | Even something like this, huh? So much I've\n |
| 0xf8b48 | 20 | never seen before... |
| 0xf8b5d | 48 | That's a weird one. You're gonna make bath oil\n |
| 0xf8b8e | 12 | out of that? |
| 0xf8b9b | 46 | Ahahaha, not this one, but the variety is...\n |
| 0xf8bca | 13 | intimidating. |
| 0xf8bd8 | 46 | I know! Excuse me, could I get some of these\n |
| 0xf8c07 | 19 | cut up for samples? |
| 0xf8c1b | 47 | The shop owner complies with her request, and\n |
| 0xf8c4b | 41 | Kuon takes in the fragrance of each new\n |
| 0xf8c75 | 8 | slice... |
| 0xf8c7e | 47 | This one's pretty sweet. I think Nekone would\n |
| 0xf8cae | 14 | appreciate it. |
| 0xf8cbd | 44 | Hmhm. It is the kind of thing Nekone would\n |
| 0xf8cea | 15 | like, isn't it? |
| 0xf8cfa | 49 | This one... Eh, a bit grassy. Not exactly ideal\n |
| 0xf8d2c | 43 | for a scent you want to put in your bath... |
| 0xf8d58 | 46 | I pluck what seems to be a citrus fruit from\n |
| 0xf8d87 | 30 | the display and inhale deeply. |
| 0xf8da6 | 38 | So you like those types of fruit, huh. |
| 0xf8dcd | 45 | Eh, it's not that I have a preference, they\n |
| 0xf8dfb | 46 | just... seem like the kind you'd put in your\n |
| 0xf8e2a | 5 | bath? |
| 0xf8e30 | 42 | I can see it easily, if I close my eyes.\n |
| 0xf8e5b | 36 | Citrus fruits floating in a bathtub. |
| 0xf8e80 | 27 | Hmhm, I see... And I agree. |
| 0xf8e9c | 47 | I'll take these red ones, those little orange\n |
| 0xf8ecc | 34 | ones, and... that long one, there. |
| 0xf8eef | 46 | That one too? It's got a pretty weird smell,\n |
| 0xf8f1e | 7 | though. |
| 0xf8f26 | 41 | Well, we don't want the sweetness to be\n |
| 0xf8f50 | 45 | overpowering. The whole thing wouldn't come\n |
| 0xf8f7e | 20 | together, otherwise. |
| 0xf8f93 | 24 | Is that how it works...? |
| 0xf8fac | 25 | Yes, that's how it works. |
| 0xf8fc6 | 44 | Kuon happily plucks another fruit from the\n |
| 0xf8ff3 | 6 | stand. |
| 0xf8ffa | 47 | She really does love her baths, doesn't she...? |
| 0xf902a | 47 | I think we might've bought a little too much,\n |
| 0xf905a | 42 | They're all useful, so it should be fine\n |
| 0xf9085 | 11 | either way. |
| 0xf9091 | 43 | Many pieces of fruit bob and float in the\n |
| 0xf90bd | 45 | bathwater that evening, and they suffuse it\n |
| 0xf90eb | 18 | with their scents. |
| 0xf90fe | 49 | We bought quite a bit to make the oils, so this\n |
| 0xf9130 | 42 | will do until Kuon finishes refining it... |
| 0xf915b | 48 | It seems to be a hit with the rest of the inn,\n |
| 0xf918c | 46 | for more than one guest has emerged smelling\n |
| 0xf91bb | 9 | of fruit. |
| 0xf91c5 | 38 | I suppose I should go take one, too... |
| 0xf91ec | 46 | Yeah. I think I'll go take a nice, long bath\n |
| 0xf921b | 30 | and munch on a piece of fruit. |
| 0xfa680 | 36 | A trip to the mountains? Tomorrow?\n |
| 0xfa6a5 | 25 | This is kind of sudden... |
| 0xfa6bf | 47 | Rulutieh said she was going to go harvest the\n |
| 0xfa6ef | 46 | wild vegetables in season. I thought I'd tag\n |
| 0xfa71e | 6 | along. |
| 0xfa725 | 45 | Oh, for fresh ingredients and all that stuff? |
| 0xfa753 | 47 | Yes... Um... These vegetables taste best when\n |
| 0xfa783 | 48 | they're in season... And they're good for your\n |
| 0xfa7b4 | 9 | health... |
| 0xfa7be | 45 | I'm running low on herbs as well. A perfect\n |
| 0xfa7ec | 49 | opportunity, I'd say. You're coming too, right,\n |
| 0xfa81e | 5 | Haku? |
| 0xfa824 | 46 | ...Wouldn't it be faster to just go buy some\n |
| 0xfa853 | 19 | from the market...? |
| 0xfa867 | 36 | My suggestion is immediately denied. |
| 0xfa88c | 22 | Hahh... guh... phew... |
| 0xfa8a3 | 47 | We've been climbing since before the sun even\n |
| 0xfa8d3 | 49 | rose, and it's noon! How high do they intend on\n |
| 0xfa905 | 9 | going...? |
| 0xfa90f | 47 | I NEED a break, but since Rulutieh and Nekone\n |
| 0xfa93f | 48 | aren't even out of breath, I keep my mouth shut. |
| 0xfa970 | 47 | Um, everyone... how about we use this area...\n |
| 0xfa9a0 | 37 | as the focal point for our search...? |
| 0xfa9c6 | 46 | Rulutieh stops in an open area and calls out\n |
| 0xfa9f5 | 12 | to everyone. |
| 0xfaa02 | 46 | Are you sure we do not have to go any farther? |
| 0xfaa31 | 48 | Yes... I believe that... we'll be able to find\n |
| 0xfaa62 | 19 | much around here... |
| 0xfaa76 | 47 | I'll leave this area to all of you, then. I'm\n |
| 0xfaaa6 | 47 | going a bit higher up to find the herbs I need. |
| 0xfaad6 | 44 | If you are still going, dear sister, I can\n |
| 0xfab03 | 12 | accompany... |
| 0xfab10 | 45 | Sorry, but those cliffs can be treacherous.\n |
| 0xfab3e | 49 | I'd prefer it if you looked for my herbs around\n |
| 0xfab70 | 5 | here. |
| 0xfab76 | 50 | Understood. If that is what you wish, dear sister. |
| 0xfaba9 | 45 | She's so obedient whenever it's Kuon asking\n |
| 0xfabd7 | 10 | something. |
| 0xfabe2 | 49 | As I think to myself, Kuon vanishes deeper into\n |
| 0xfac14 | 11 | the forest. |
| 0xfac20 | 48 | I don't know much about the mountains, so I'll\n |
| 0xfac51 | 21 | stick with you, Neko. |
| 0xfac67 | 37 | You can help me look for herbs, then. |
| 0xfac8d | 24 | Lovely! So will this do? |
| 0xfaca6 | 49 | Ugh, that smells! N-No, that is not any herb of\n |
| 0xfacd8 | 5 | note. |
| 0xfacde | 20 | How about this then? |
| 0xfacf3 | 45 | Wh--That one is extremely poisonous! Please\n |
| 0xfad21 | 27 | dispose of it, and quickly! |
| 0xfad3d | 47 | Nekone and Atuy seem to be having fun as they\n |
| 0xfad6d | 45 | chat together, poking through the roots and\n |
| 0xfad9b | 6 | weeds. |
| 0xfada2 | 51 | I'll remain on watch here, then. I'm sure there's\n |
| 0xfadd6 | 49 | no real danger about, but better safe than sorry. |
| 0xfae08 | 52 | He watches Nekone and Atuy leave, smiling amicably\n |
| 0xfae3d | 34 | at me as he makes his declaration. |
| 0xfae60 | 48 | This could have been a perfect opportunity for\n |
| 0xfae91 | 48 | you to take the initiative with her, you know... |
| 0xfaec2 | 10 | ...Pardon? |
| 0xfaecd | 48 | Never mind. Well, I guess watch duty is yours,\n |
| 0xfaefe | 5 | then. |
| 0xfaf04 | 46 | Ah, well. I guess you can't expect people to\n |
| 0xfaf33 | 19 | change that easily. |
| 0xfaf47 | 50 | Welp, what should I do? I don't even have a clue\n |
| 0xfaf7a | 41 | what I'm supposed to be looking for here. |
| 0xfafa4 | 46 | U-Um... Sir Haku... If you'd like, would you\n |
| 0xfafd3 | 16 | accompany me...? |
| 0xfafe4 | 33 | Rulutieh asks me very hesitantly. |
| 0xfb006 | 52 | Yeah, sure. I wouldn't know what to pick if I went\n |
| 0xfb03b | 49 | off on my own. Just tell me what to do, Rulutieh. |
| 0xfb06d | 49 | O-Oh no. I wouldn't dare... I just wanted to go\n |
| 0xfb09f | 35 | searching with you... That's all... |
| 0xfb0c3 | 49 | She's as shy as ever. She doesn't have to be so\n |
| 0xfb0f5 | 34 | reserved around me all the time... |
| 0xfb118 | 51 | Well, in any case, I'd appreciate it if you could\n |
| 0xfb14c | 44 | teach me a thing or two about the mountains. |
| 0xfb179 | 46 | Y-Yes... Well, there are many things... that\n |
| 0xfb1a8 | 37 | can only be found during this season. |
| 0xfb1ce | 49 | I carry a basket along with me as I amble along\n |
| 0xfb200 | 16 | behind Rulutieh. |
| 0xfb211 | 51 | Rulutieh's vast knowledge on the subject helps us\n |
| 0xfb245 | 44 | find various interesting plants, one after\n |
| 0xfb272 | 8 | another. |
| 0xfb27b | 51 | And on these trees... you can find mushrooms with\n |
| 0xfb2af | 26 | a very distinct texture... |
| 0xfb2ca | 18 | Hmmm, lemme see... |
| 0xfb2dd | 27 | It's this one, here... Eep! |
| 0xfb2f9 | 22 | Hm? What's the matter? |
| 0xfb310 | 45 | I stand closer, trying to get a look at the\n |
| 0xfb33e | 45 | mushrooms, but she yelps as I look over her\n |
| 0xfb36c | 9 | shoulder. |
| 0xfb376 | 43 | N-No... you're... just a little... close... |
| 0xfb3a2 | 47 | She's talking so quietly. I can't really hear\n |
| 0xfb3d2 | 18 | what she's saying. |
| 0xfb3e5 | 29 | Uh... It's... It's nothing... |
| 0xfb403 | 48 | OK...? Hm, yeah, you're right. These mushrooms\n |
| 0xfb434 | 23 | do feel really springy. |
| 0xfb44c | 46 | If you steam them... they get a firm, almost\n |
| 0xfb47b | 34 | crunchy texture. It's very good... |
| 0xfb49e | 14 | Really... Huh? |
| 0xfb4ad | 46 | When I try to pluck one of the mushrooms, it\n |
| 0xfb4dc | 31 | instantly crumbles in my hands. |
| 0xfb4fc | 48 | Oh... If you grab it directly like that, it'll\n |
| 0xfb52d | 47 | fall apart... You have to break it off at the\n |
| 0xfb55d | 7 | stem... |
| 0xfb565 | 10 | Like this? |
| 0xfb570 | 49 | I copy Rulutieh's motions, plucking it directly\n |
| 0xfb5a2 | 44 | from the base. This time, it remains intact. |
| 0xfb5cf | 28 | Yes... That was very good... |
| 0xfb5ec | 50 | I see... Not so bad once you get the hang of it.\n |
| 0xfb61f | 43 | Here, you can put yours in this basket too. |
| 0xfb64b | 20 | O-Oh... Thank you... |
| 0xfb660 | 44 | Might've been a lot easier if we had taken\n |
| 0xfb68d | 17 | Cocopo with us... |
| 0xfb69f | 49 | I'm sorry... but if we had brought Cocopo here... |
| 0xfb6d1 | 20 | What? Something bad? |
| 0xfb6e6 | 49 | I'm sure that everything in the vicinity that's\n |
| 0xfb718 | 41 | even remotely edible... would be eaten... |
| 0xfb742 | 12 | Ah... I see. |
| 0xfb74f | 45 | Well, sounds like a good enough reason to me. |
| 0xfb77d | 41 | We continue to talk for a while, until... |
| 0xfb7a7 | 18 | Oh... This tree... |
| 0xfb7ba | 49 | Rulutieh stops in front of a tree, and puts her\n |
| 0xfb7ec | 18 | hand to its trunk. |
| 0xfb7ff | 21 | Something up with it? |
| 0xfb815 | 38 | It looks like just an ordinary tree.\n |
| 0xfb83c | 50 | No weird nuts, or mushrooms, or tuber-based vines. |
| 0xfb86f | 48 | Rulutieh pinches a reddish-brown substance off\n |
| 0xfb8a0 | 40 | the trunk, and touches it to her tongue. |
| 0xfb8c9 | 10 | Hee hee... |
| 0xfb8d4 | 50 | Her face brightens into a fond, childlike smile,\n |
| 0xfb907 | 42 | as though remembering something nostalgic. |
| 0xfb932 | 52 | I follow her lead--taking a pinch of the substance\n |
| 0xfb967 | 30 | and throwing it into my mouth. |
| 0xfb986 | 16 | ...That's sweet. |
| 0xfb997 | 48 | It has a powerful flavor of sap, with a subtle\n |
| 0xfb9c8 | 38 | sweetness that seems to fill my mouth. |
| 0xfb9ef | 52 | When I was little... my elder brothers and sisters\n |
| 0xfba24 | 50 | would take me out to play... and we'd eat these... |
| 0xfba57 | 49 | Sweets were rather expensive, so we would often\n |
| 0xfba89 | 32 | have this for a snack instead... |
| 0xfbaaa | 38 | Ah, she was remembering her childhood. |
| 0xfbad1 | 47 | Around us are several more of the same trees,\n |
| 0xfbb01 | 21 | growing in a cluster. |
| 0xfbb17 | 48 | I had no idea this tree grew in these lands as\n |
| 0xfbb48 | 32 | well... It feels so nostalgic... |
| 0xfbb69 | 32 | A little taste of home, I guess. |
| 0xfbb8a | 46 | I wonder... how they're all doing right now... |
| 0xfbbb9 | 48 | She looks up at the tree, a strange expression\n |
| 0xfbbea | 42 | on her face. She must be thinking of her\n |
| 0xfbc15 | 11 | siblings... |
| 0xfbc21 | 46 | Yeah, I heard you have a lot of brothers and\n |
| 0xfbc50 | 8 | sisters. |
| 0xfbc59 | 34 | Yes... All told, we make fourteen. |
| 0xfbc7c | 49 | That sounds... hectic. Bet you were never bored\n |
| 0xfbcae | 19 | as a kid, at least. |
| 0xfbcc2 | 49 | Hee... Yes. My brothers... and sisters... would\n |
| 0xfbcf4 | 25 | often visit me to play... |
| 0xfbd0e | 51 | Visit...? Right, she spent a lot of her childhood\n |
| 0xfbd42 | 14 | sick in bed... |
| 0xfbd51 | 47 | They must have been good siblings to you, then. |
| 0xfbd81 | 49 | Yes... They were very kind... I'm proud to call\n |
| 0xfbdb3 | 29 | them my brothers and sisters. |
| 0xfbdd1 | 50 | When I had fallen ill, and was bedridden... They\n |
| 0xfbe04 | 37 | would often bring me this very sap... |
| 0xfbe2a | 47 | As we talk, I realize the sap in my mouth has\n |
| 0xfbe5a | 12 | melted away. |
| 0xfbe67 | 45 | If this sap was just a little more mild, it\n |
| 0xfbe95 | 34 | could've been used as a sweetener. |
| 0xfbeb8 | 36 | Sugar and honey can get expensive.\n |
| 0xfbedd | 49 | If I collect some of this and heat--Ah, but the\n |
| 0xfbf0f | 22 | flavor's too strong... |
| 0xfbf26 | 51 | It has a slight bitterness, and it's a bit sharp.\n |
| 0xfbf5a | 45 | Adding it to drinks and food would ruin the\n |
| 0xfbf88 | 7 | flavor. |
| 0xfbf90 | 50 | I wonder if there's something I can do about it... |
| 0xfbfc3 | 27 | Is... something the matter? |
| 0xfbfdf | 51 | Eh, nothing. Just wondering whether we could make\n |
| 0xfc013 | 39 | some kind of sweetener with this stuff. |
| 0xfc03b | 15 | A... sweetener? |
| 0xfc04b | 50 | Yeah. I was thinking if we gather some, we could\n |
| 0xfc07e | 43 | try heating it to make it a little sweeter. |
| 0xfc0aa | 46 | But it's got a pretty distinct flavor to it,\n |
| 0xfc0d9 | 29 | so it might not be that easy. |
| 0xfc0f7 | 5 | Oh... |
| 0xfc0fd | 3 | Hm? |
| 0xfc101 | 45 | Well, um... I tried doing the same thing...\n |
| 0xfc12f | 21 | when I was a child... |
| 0xfc145 | 50 | I asked my brother to collect the sap back then... |
| 0xfc178 | 20 | Yeah? How did it go? |
| 0xfc191 | 6 | ...Hm? |
| 0xfc198 | 52 | It started spouting smoke, and a horrible smell...\n |
| 0xfc1cd | 36 | The whole castle was in an uproar... |
| 0xfc1f2 | 31 | O-Oh. So... it didn't work out. |
| 0xfc212 | 5 | Uh... |
| 0xfc218 | 51 | B-But that was back when I was still quite young.\n |
| 0xfc24c | 37 | Maybe now, I am experienced enough... |
| 0xfc272 | 28 | A sweetener using the sap... |
| 0xfc28f | 49 | Sounds good. If you need any help, just come to\n |
| 0xfc2c1 | 3 | me. |
| 0xfc2c5 | 7 | Huh...? |
| 0xfc2cd | 52 | Oh, sorry, I didn't mean to impose myself. It just\n |
| 0xfc302 | 49 | sounds interesting. Plus, I've got a sweet tooth. |
| 0xfc334 | 16 | Are you... sure? |
| 0xfc345 | 44 | 'Course I'm sure. I volunteered, didn't I?\n |
| 0xfc372 | 45 | Wouldn't it be kinda fun to invent some new\n |
| 0xfc3a0 | 14 | kind of sweet? |
| 0xfc3af | 15 | Ah... It would! |
| 0xfe18e | 45 | While having a relaxing evening in my room,\n |
| 0xfe1bc | 46 | I'm surprised to see Nekone visiting me alone. |
| 0xfe1eb | 50 | What's wrong? I don't usually see you around here. |
| 0xfe21e | 53 | ...I only came to see if dear sister and the others\n |
| 0xfe254 | 47 | were here. I do not have any business with you. |
| 0xfe284 | 47 | Kuon and the others? I think they went out to\n |
| 0xfe2b4 | 26 | take care of some errands. |
| 0xfe2cf | 9 | ...I see. |
| 0xfe2d9 | 39 | What? Did you want something with them? |
| 0xfe301 | 48 | No, I wanted to go to my dear brother's manor,\n |
| 0xfe332 | 6 | and... |
| 0xfe339 | 43 | Ukon's place? Right, OK. Well, be careful\n |
| 0xfe365 | 10 | out there. |
| 0xfe374 | 13 | What's wrong? |
| 0xfe382 | 50 | Actually, it's already dark. They say the city's\n |
| 0xfe3b5 | 44 | pretty safe, but I can't send her out alone. |
| 0xfe3e2 | 51 | Though I'm not wild about going outside right now\n |
| 0xfe416 | 9 | myself... |
| 0xfe420 | 49 | I know, Nekone. It's already dark, so why don't\n |
| 0xfe452 | 30 | you have Kiwru take you there? |
| 0xfe471 | 48 | It's a good opportunity, and he'll be thrilled\n |
| 0xfe4a2 | 51 | for the chance. He'd better appreciate the favor... |
| 0xfe4d6 | 23 | Kiwru is out on patrol. |
| 0xfe4ee | 41 | ...And this would have been such a good\n |
| 0xfe518 | 44 | opportunity... That kid really can't catch\n |
| 0xfe545 | 8 | a break. |
| 0xfe54e | 50 | But today isn't even his shift. Working is fine,\n |
| 0xfe581 | 44 | but if he won't take breaks, he'll burn out. |
| 0xfe5ae | 52 | Very persuasive, from someone who spares no effort\n |
| 0xfe5e3 | 35 | to slack off on his own shift days. |
| 0xfe607 | 44 | Nice try, but flattery will get you nowhere. |
| 0xfe634 | 50 | The wind must be picking up... The screen nearby\n |
| 0xfe667 | 45 | suddenly shakes and rattles, interrupting us. |
| 0xfe695 | 5 | Eep!! |
| 0xfe69d | 23 | Wh-What was that noise? |
| 0xfe6b5 | 44 | Hm? It's probably just the windows rattling. |
| 0xfe6e2 | 10 | I-I see... |
| 0xfe6ed | 46 | It looks like they're going to be back late,\n |
| 0xfe71c | 43 | but do you want to wait until Kuon returns? |
| 0xfe748 | 28 | It... It is urgent business. |
| 0xfe765 | 39 | Um... Can I ask you to take me instead? |
| 0xfe78d | 3 | Me? |
| 0xfe791 | 14 | You... cannot? |
| 0xfe7a0 | 30 | Well, it's not like I can't... |
| 0xfe7bf | 47 | Ah, well. It sounds like a lot of effort, but\n |
| 0xfe7ef | 25 | I can't just abandon her. |
| 0xfe809 | 41 | OK, let's go. I was just thinking about\n |
| 0xfe833 | 35 | inviting Ukon out to drink, anyway. |
| 0xfe857 | 48 | Thank y--{W180}Oh, of course that is your true\n |
| 0xfe888 | 10 | intention. |
| 0xfe893 | 6 | *Gasp* |
| 0xfe89a | 47 | Nekone jolts at the sound of the wind blowing\n |
| 0xfe8ca | 30 | forcefully against the window. |
| 0xfe8e9 | 18 | What's the matter? |
| 0xfe8fc | 27 | N-Nothing... is the matter. |
| 0xfe918 | 9 | You sure? |
| 0xfe922 | 39 | Why is she being so weirdly fidgety...? |
| 0xfe94a | 34 | Hm? Nekone, who's that behind you? |
| 0xfe96d | 7 | ...Huh? |
| 0xfe975 | 41 | That person, standing right behind you... |
| 0xfe99f | 8 | Aaaaah!! |
| 0xfe9a8 | 32 | Oop, just a shadow flickering.\n |
| 0xfe9c9 | 37 | Wait... What was that weird yelp for? |
| 0xfe9ef | 7 | *Smack* |
| 0xfe9f7 | 10 | Hrgraaah!! |
| 0xfea02 | 38 | ...Why are you turning on this street? |
| 0xfea29 | 32 | Why? Because this is a shortcut. |
| 0xfea4a | 51 | To get there from the inn, there's a path through\n |
| 0xfea7e | 48 | the market, or a path past a run-down graveyard. |
| 0xfeaaf | 46 | If you're going to his place, then this path\n |
| 0xfeade | 10 | is faster. |
| 0xfeae9 | 22 | Yes... that is true... |
| 0xfeb00 | 50 | Nekone stops in the street and stands there with\n |
| 0xfeb33 | 24 | downcast eyes, unmoving. |
| 0xfeb4c | 50 | What's wrong? You said you were in a hurry, right? |
| 0xfeb7f | 9 | I-I know! |
| 0xfeb89 | 49 | Whoa! What's with the yelling all of a sudden...? |
| 0xfebbb | 26 | Fine, let us go. Hurry up. |
| 0xfebd6 | 49 | Raising her voice, she hurriedly walks on ahead\n |
| 0xfec08 | 16 | to the shortcut. |
| 0xfec19 | 22 | ...What's up with her? |
| 0xfec30 | 47 | As we finally reach the graveyard, I notice a\n |
| 0xfec60 | 42 | strange chill in the air... not just the\n |
| 0xfec8b | 12 | temperature. |
| 0xfec98 | 50 | A sudden silence falls over us, and we walk down\n |
| 0xfeccb | 34 | the field path in the eerie quiet. |
| 0xfecee | 47 | The wind blows, and the sound of the rustling\n |
| 0xfed1e | 26 | leaves breaks the silence. |
| 0xfed39 | 53 | Nekone suddenly jumps, her eyes darting uncertainly\n |
| 0xfed6f | 35 | around in the surrounding darkness. |
| 0xfed93 | 16 | Something wrong? |
| 0xfeda4 | 21 | ...No, it is nothing. |
| 0xfedba | 45 | Though she's been keeping her distance, she\n |
| 0xfede8 | 47 | quickly rushes up alongside me as she responds. |
| 0xfee18 | 46 | It is hard to hear you over the wind, if you\n |
| 0xfee47 | 25 | do not come a bit closer. |
| 0xfee61 | 41 | Really? I could still hear you just fine. |
| 0xfee8b | 19 | It IS hard to hear. |
| 0xfee9f | 12 | Uh... Right. |
| 0xfeeac | 49 | Nekone insists with a firm voice that brooks no\n |
| 0xfeede | 46 | argument... but it sounds like she's shaking\n |
| 0xfef0d | 9 | slightly. |
| 0xfef17 | 50 | I dunno. She's been acting weird... or antsy, or\n |
| 0xfef4a | 43 | SOMETHING for a while. It's almost as if... |
| 0xfef76 | 36 | Aha... Is this little squirt scared? |
| 0xfef9b | 51 | Ukon's talked about when they were young--how she\n |
| 0xfefcf | 47 | had to wake him up to walk her to the bathroom. |
| 0xfefff | 52 | And... how after the nights when she couldn't wake\n |
| 0xff034 | 48 | him up, he'd see parts of the futon would be a\n |
| 0xff065 | 37 | bit darker than usual in the morning. |
| 0xff08b | 49 | Wh-Why do you have that weird smile on your face? |
| 0xff0bd | 49 | Oh, nothing. Which reminds me--This area's dark\n |
| 0xff0ef | 45 | because it's away from the street, so watch\n |
| 0xff11d | 10 | your step. |
| 0xff128 | 20 | I already know that. |
| 0xff13d | 6 | And... |
| 0xff144 | 9 | And what? |
| 0xff14e | 41 | As I trail off, Nekone presses me on my\n |
| 0xff178 | 23 | "unintentional murmur." |
| 0xff190 | 46 | Well, there's just a rumor that... something\n |
| 0xff1bf | 20 | appears around here. |
| 0xff1d4 | 30 | Nekone freezes at those words. |
| 0xff1f3 | 48 | Th-Thieves are no match for us! I have learned\n |
| 0xff224 | 40 | fine defensive arts from my dear sister. |
| 0xff24d | 44 | Nekone starts jabbing and throwing some...\n |
| 0xff27a | 24 | seriously wimpy punches. |
| 0xff293 | 31 | No, I'm not talking about that. |
| 0xff2b3 | 15 | Not about that? |
| 0xff2c3 | 37 | They say... ghosts and such appear.\n |
| 0xff2e9 | 34 | Or were they called Nugwisomkami\n |
| 0xff30c | 12 | around here? |
| 0xff31f | 33 | Th-That is simple superstition.\n |
| 0xff341 | 18 | It is just a lie.  |
| 0xff354 | 41 | Well, we can't say that for sure, can we? |
| 0xff37e | 34 | Ridiculous! Mere superstition...\n |
| 0xff3a1 | 27 | Are you trying to scare me? |
| 0xff3bd | 34 | Well, normally you'd think that.\n |
| 0xff3e0 | 49 | That it's just superstition, I mean. But, well... |
| 0xff412 | 50 | I used to be a rationalist too, but... I've seen\n |
| 0xff445 | 43 | way too many unexplainable things recently. |
| 0xff471 | 47 | Hmm. But Kuon was the one who said it, right?\n |
| 0xff4a1 | 42 | She said she saw something like that once. |
| 0xff4cc | 50 | It was pretty lighthearted, but she didn't sound\n |
| 0xff4ff | 20 | like she was joking. |
| 0xff514 | 48 | "It felt like something was hunting me down...\n |
| 0xff545 | 30 | I thought I was going to die." |
| 0xff564 | 47 | She looked pretty troubled by it, and I doubt\n |
| 0xff594 | 39 | she was acting. It was probably true... |
| 0xff5bc | 45 | Would you still say it's only superstition,\n |
| 0xff5ea | 21 | even if Kuon said it? |
| 0xff600 | 7 | Nngh... |
| 0xff608 | 49 | I mean, she said the magic you use is based off\n |
| 0xff63a | 36 | that kind of "superstition" as well. |
| 0xff65f | 42 | Speaking of which, I asked her about the\n |
| 0xff68a | 45 | Nugwisomkami at the time, and it was pretty\n |
| 0xff6b8 | 12 | interesting. |
| 0xff6c5 | 55 | Monsters that make you sprout mold all over yourself,\n |
| 0xff6fd | 50 | flying heads that suck your blood, imps that eat\n |
| 0xff730 | 16 | rotting flesh... |
| 0xff741 | 8 | Nnngh... |
| 0xff74a | 3 | Hm? |
| 0xff74e | 47 | What's this? THE Nekone is grabbing my sleeve\n |
| 0xff77e | 19 | and not letting go! |
| 0xff792 | 29 | I-It is getting a bit cold.\n |
| 0xff7b0 | 31 | I-I am not... getting scared... |
| 0xff7d0 | 24 | And she's crying, too... |
| 0xff7e9 | 49 | No, wait a second, I didn't say anything that'd\n |
| 0xff81b | 23 | make her THAT scared... |
| 0xff833 | 47 | Actually, I haven't even gotten to the actual\n |
| 0xff863 | 17 | scary stories...? |
| 0xff875 | 50 | ...Maybe I got a little carried away, seeing her\n |
| 0xff8a8 | 22 | react so dramatically. |
| 0xff8bf | 7 | Aaah... |
| 0xff8c7 | 52 | Nekone twitches at a sound from the swaying plants\n |
| 0xff8fc | 49 | in the vacant lot, beginning to silently tremble. |
| 0xff92e | 15 | Nngh... Nnnn... |
| 0xff93e | 35 | You don't need to be that scared.\n |
| 0xff962 | 17 | It's just a bird. |
| 0xff974 | 51 | I-I just could not hear it properly. That is all.\n |
| 0xff9a8 | 41 | I-I am... I-I am not scared, of course... |
| 0xff9d2 | 41 | Despite her words, Nekone maintains her\n |
| 0xff9fc | 24 | death grip on my sleeve. |
| 0xffa15 | 52 | Maybe she doesn't even realize that she's grabbing\n |
| 0xffa4a | 16 | onto my clothes. |
| 0xffa5b | 47 | I'm scared of how things will turn out later.\n |
| 0xffa8b | 41 | Like when she comes back to her senses... |
| 0xffab5 | 47 | ...We should probably hurry up, before we run\n |
| 0xffae5 | 13 | into trouble. |
| 0xffaf3 | 33 | *Hic* A toast! L'ss make a toast. |
| 0xffb15 | 45 | *Hic*... Hokay. What're we toastin' again...? |
| 0xffb43 | 51 | Uhh, don' remember. Dunno what it is, or why it's\n |
| 0xffb77 | 47 | a good thing... but... probably worth toastin'. |
| 0xffba7 | 50 | I know. How 'bout we toast 'cause we're drinkin'\n |
| 0xffbda | 26 | the good stuff today, too! |
| 0xffbf5 | 48 | Heeey, not bad! I don' really get it, but I'll\n |
| 0xffc26 | 9 | toast it! |
| 0xffc30 | 11 | Haku & Ukon |
| 0xffc3c | 8 | Cheers!! |
| 0xffc45 | 8 | Gahahah! |
| 0xffc4e | 48 | We make another toast. I have no idea how many\n |
| 0xffc7f | 41 | we've made now, but it won't be the last. |
| 0xffca9 | 47 | Nekone pops her head in, while we enjoy being\n |
| 0xffcd9 | 17 | pleasantly drunk. |
| 0xffceb | 46 | Mm? You gonna give us a lecture, and tell us\n |
| 0xffd1a | 19 | we've had too much? |
| 0xffd2e | 50 | After telling you numerous times, I have already\n |
| 0xffd61 | 41 | concluded that that would be pointless... |
| 0xffd8b | 9 | Anyway... |
| 0xffd95 | 19 | Um, dear brother... |
| 0xffda9 | 20 | Mm? Something wrong? |
| 0xffdbe | 49 | Nekone looks at Ukon with strangely pained, wet\n |
| 0xffdf0 | 5 | eyes. |
| 0xffdf6 | 42 | I have... a request for you, dear brother. |
| 0xffe21 | 51 | A request? Something in the shops catch your eye?\n |
| 0xffe55 | 34 | Maybe on my next day off, we can-- |
| 0xffe78 | 32 | N-No, it is nothing like that... |
| 0xffe99 | 3 | Oh? |
| 0xffe9d | 24 | Y-You see... um... ah... |
| 0xffeb6 | 48 | She's squirming uncomfortably, and rubbing her\n |
| 0xffee7 | 37 | legs together in an odd way. Is she-- |
| 0xfff0d | 16 | I see. I got it. |
| 0xfff1e | 7 | Wha...? |
| 0xfff26 | 47 | Hey, don't worry, I get it. It's a hard thing\n |
| 0xfff56 | 46 | to come right out and say. Basically, Nekone-- |
| 0xfff85 | 30 | N-No... You must not say it... |
| 0xfffa4 | 33 | --wants to join our party, right? |
| 0xfffc6 | 30 | ...What are you talking about? |
| 0xfffe5 | 48 | I see. I didn't realize! Nekone IS getting old\n |
| 0x100016 | 44 | enough to start being interested in booze... |
| 0x100043 | 45 | Never thought there'd come a day we'd drink\n |
| 0x100071 | 46 | together as siblings. Ngh... I'm gettin' all\n |
| 0x1000a0 | 6 | misty. |
| 0x1000a7 | 31 | This calls for a celebration!\n |
| 0x1000c7 | 51 | All right, time for me to break out the good stuff! |
| 0x1000fb | 32 | Not you as well, dear brother... |
| 0x10011c | 38 | Come on, Nekone. Let's toast together! |
| 0x100143 | 48 | I will decline. If I drink that, it would make\n |
| 0x100174 | 25 | the problem even worse... |
| 0x10018e | 6 | Worse? |
| 0x100195 | 6 | Ngh... |
| 0x10019c | 21 | Anyway, I shall pass. |
| 0x1001b2 | 8 | H-Hey... |
| 0x1001bb | 41 | Nekone leaves the room in an apparently\n |
| 0x1001e5 | 11 | bad temper. |
| 0x1001f1 | 23 | ...What was that about? |
| 0x100209 | 45 | Ah, teenage girls are so hard to deal with... |
| 0x100237 | 50 | Well, can't be helped. A woman's mind is forever\n |
| 0x10026a | 26 | a mystery for us poor men. |
| 0x100285 | 34 | I know, but it still makes me sad. |
| 0x1002a8 | 29 | Welp. Time for another toast. |
| 0x1002c6 | 50 | Yep, here's to Nekone reaching a difficult age...! |
| 0x1002f9 | 7 | Cheers! |
| 0x100301 | 12 | *Yawn*...... |
| 0x10030e | 51 | That was quite a feast last night. And to think I\n |
| 0x100342 | 33 | passed right out, on top of that. |
| 0x100364 | 52 | But after a night of drinking, the air feels nice.\n |
| 0x100399 | 50 | Even the laundry is fluttering pleasantly in the\n |
| 0x1003cc | 5 | wind. |
| 0x1003d2 | 9 | ...Hm...? |
| 0x1003dc | 13 | Hey, morning. |
| 0x1003ea | 49 | But Nekone keeps her head bowed in moody silence. |
| 0x10041c | 51 | What's wrong? It's a nice morning, right? Doesn't\n |
| 0x100450 | 44 | the laundry look nice out there in the yard? |
| 0x10047d | 6 | *Kick* |
| 0x100484 | 5 | Ow!\n |
| 0x10048a | 10 | What the-- |
| 0x100495 | 7 | H-Hey-- |
| 0x10049d | 10 | *Kick*, \n |
| 0x1004a8 | 12 | Ow, W-Wait-- |
| 0x1004b5 | 8 | *Kick--* |
| 0x1004be | 34 | Sto--Wai--Hey, why--M-Miss Nekone? |
| 0x101a82 | 52 | Ukon dropped by the Hakurokaku to tell us that the\n |
| 0x101ab7 | 46 | guards will be in charge of the patrols today. |
| 0x101ae6 | 47 | Seems there's some kind of training exercise,\n |
| 0x101b16 | 45 | so a lot of them will be spread out through\n |
| 0x101b44 | 12 | the capital. |
| 0x101b51 | 48 | Running into them could cause some unnecessary\n |
| 0x101b82 | 45 | confusion, so we're taking the day off from\n |
| 0x101bb0 | 8 | patrols. |
| 0x101bb9 | 52 | Guess we do tend to stand out when we walk around.\n |
| 0x101bee | 41 | Makes sense for us to stay put this time. |
| 0x101c18 | 16 | That's the idea. |
| 0x101c29 | 35 | You here for the same reason, Maro? |
| 0x101c4d | 49 | Nay, but I do seize upon this opportunity for a\n |
| 0x101c7f | 45 | visit, and which is more, a gifting of gifts! |
| 0x101cad | 53 | Seems his family bought some quality alcohol again.\n |
| 0x101ce3 | 38 | And of course, they're in debt. Again. |
| 0x101d0a | 50 | Still having to deal with your family's spending\n |
| 0x101d3d | 14 | habits, huh... |
| 0x101d4c | 15 | Ay... ay, me... |
| 0x101d5c | 44 | Um, if there's anything I can do to help...? |
| 0x101d89 | 49 | O, being pitied so... only serveth to intensify\n |
| 0x101dbb | 13 | the misery... |
| 0x101dc9 | 52 | Well, that's how it is. I bought some of the booze\n |
| 0x101dfe | 43 | off Maroro so we could have a little party. |
| 0x101e2a | 53 | All the girls are out watching a play or something,\n |
| 0x101e60 | 6 | right? |
| 0x101e67 | 49 | Yeah, they said they wouldn't be back until late. |
| 0x101e99 | 44 | Perfect. I can drink to my heart's content\n |
| 0x101ec6 | 42 | without worrying about anyone complaining! |
| 0x101ef1 | 49 | Ohoho! Every spirit is of the finest provision!\n |
| 0x101f23 | 42 | Thou wilt not be disappointed, to be sure. |
| 0x101f4e | 43 | In that case, let's get this party started! |
| 0x101f7a | 49 | Erm... I'm actually not very good with alcohol... |
| 0x101fac | 49 | In contrast to the three eager men, Kiwru looks\n |
| 0x101fde | 16 | a little uneasy. |
| 0x101fef | 52 | Kiwru, it's time you learned the taste of alcohol!\n |
| 0x102024 | 46 | The sooner you learn these things, the better. |
| 0x102053 | 53 | He's right. You gotta figure out what kind of drunk\n |
| 0x102089 | 50 | you are while you're in a safe space with friends! |
| 0x1020bc | 49 | And if you want to woo the ladies, you're gonna\n |
| 0x1020ee | 40 | have to learn proper drinking etiquette. |
| 0x102117 | 49 | Is... that true? Something tells me you're just\n |
| 0x102149 | 14 | saying that... |
| 0x102158 | 49 | Hey, don't sweat the details! This is some good\n |
| 0x10218a | 45 | stuff here. Don't be so uptight--just enjoy\n |
| 0x1021b8 | 9 | yourself. |
| 0x1021c2 | 50 | Ukon sits down an unwilling Kiwru, and begins to\n |
| 0x1021f5 | 38 | line up rows of the snacks he brought. |
| 0x10221c | 49 | ...Yep. Now this is quality. Don't want to down\n |
| 0x10224e | 39 | it all at once--it'd be an awful waste. |
| 0x102276 | 52 | Ukon picks up a bottle and takes a whiff, sounding\n |
| 0x1022ab | 33 | fairly impressed in his reaction. |
| 0x1022cd | 50 | We could hardly ask more opportune circumstances\n |
| 0x102300 | 16 | for... the Game. |
| 0x102311 | 48 | Maroro swiftly pours the drinks into identical\n |
| 0x102342 | 44 | cups and places them in front of each of us. |
| 0x10236f | 41 | ...The "Game"? What exactly are we doing? |
| 0x102399 | 47 | A little tasting of sorts. A game we sots and\n |
| 0x1023c9 | 23 | drunkards like to play. |
| 0x1023e1 | 44 | Why, I would thank thee to treat this as a\n |
| 0x10240e | 46 | pursuit reserved for the noble and majestical! |
| 0x10243d | 50 | Behold five prized libations! Each shall we sip,\n |
| 0x102470 | 51 | and determine which is what by taste and wit alone. |
| 0x1024a4 | 47 | Even yon rinse-water is of the highest quality. |
| 0x1024d4 | 43 | A cup of water is filled, next to all the\n |
| 0x102500 | 14 | harder drinks. |
| 0x10250f | 30 | Um, this water is special too? |
| 0x10252e | 46 | You drink it in between the alcohol to reset\n |
| 0x10255d | 12 | your palate. |
| 0x10256a | 28 | Oh, you need to do that too? |
| 0x102587 | 37 | The game is to recognize the taste.\n |
| 0x1025ad | 48 | Can't have your tongue getting too drunk, now,\n |
| 0x1025de | 7 | can we? |
| 0x1025e6 | 12 | Oh... I see. |
| 0x1025f3 | 33 | Now then! We are thus commence'd! |
| 0x102615 | 49 | Each of us takes a cup and carefully drinks it,\n |
| 0x102647 | 36 | noting the scent and flavor of each. |
| 0x10266c | 33 | Oh, ALL these drinks are great.\n |
| 0x10268e | 42 | They're all so smooth, and go down easy... |
| 0x1026b9 | 46 | But, since they're all so good, it's hard to\n |
| 0x1026e8 | 25 | distinguish between them. |
| 0x102702 | 47 | I try to keep in mind the nuances of each one\n |
| 0x102732 | 29 | as I take a sip of the water. |
| 0x102750 | 31 | Mmm-mm! This one's fantastic... |
| 0x102770 | 48 | Ukon's surprise and delight at the fifth cup's\n |
| 0x1027a1 | 20 | contents is audible. |
| 0x1027b6 | 45 | Something that impresses Ukon that much...?\n |
| 0x1027e4 | 28 | Can't wait to try it myself. |
| 0x102801 | 47 | You're right... Even I can tell that this one\n |
| 0x102831 | 21 | is particularly fine. |
| 0x102847 | 34 | Kiwru stares at the cup in wonder. |
| 0x10286a | 48 | That much, huh...? Well, let's give it a shot... |
| 0x10289b | 6 | *Gulp* |
| 0x1028a2 | 47 | Th-This is...! Oh man, this stuff's incredible! |
| 0x1028d2 | 47 | It just feels so much denser than the others.\n |
| 0x102902 | 48 | It's got a powerful flavor and scent. How do I\n |
| 0x102933 | 9 | put it... |
| 0x10293d | 22 | ...Maro, hit me again. |
| 0x102954 | 50 | Master Haku, that is not the purpose of a tasting! |
| 0x102987 | 45 | This was the only one I could really tell a\n |
| 0x1029b5 | 16 | difference in... |
| 0x1029c6 | 43 | Well, you could recognize the good stuff.\n |
| 0x1029f2 | 15 | That's a start. |
| 0x102a02 | 47 | All of us once again taste the five different\n |
| 0x102a32 | 7 | drinks. |
| 0x102a3a | 50 | Now then, time for the real test... Maroro, turn\n |
| 0x102a6d | 30 | around for a second, will you? |
| 0x102a8c | 49 | Ukon brusquely switches around the order of the\n |
| 0x102abe | 10 | five cups. |
| 0x102ac9 | 46 | ...That oughta do it. You two remember which\n |
| 0x102af8 | 12 | one's which? |
| 0x102b05 | 4 | Yes. |
| 0x102b0a | 9 | Think so. |
| 0x102b14 | 20 | Prithee, if I may... |
| 0x102b29 | 45 | Maroro picks up the cup, and carefully sips\n |
| 0x102b57 | 8 | from it. |
| 0x102b60 | 50 | This one... subtle and sweet in seeming, and the\n |
| 0x102b93 | 51 | still-young taste doth much to soothe the tongue... |
| 0x102bc7 | 50 | He takes a sip of the water to cleanse his palate. |
| 0x102bfa | 18 | And so the second. |
| 0x102c0d | 37 | A shade more floral than the first.\n |
| 0x102c33 | 49 | It calleth to one's mind the dew-aired southern\n |
| 0x102c65 | 13 | distilleries. |
| 0x102c73 | 42 | He rearranges the drinks as he continues\n |
| 0x102c9e | 13 | thoughtfully. |
| 0x102cac | 35 | The third... A north-drink, is't?\n |
| 0x102cd0 | 50 | It suggesteth medicinal alcohol, liable to swell\n |
| 0x102d03 | 17 | one's appetite... |
| 0x102d15 | 44 | The fourth... Why, it hardly bears saying.\n |
| 0x102d42 | 41 | Such age, such arresting potency! Truly\n |
| 0x102d6c | 13 | mervailous... |
| 0x102d7a | 49 | The cups clink as he continues to rearrange them. |
| 0x102dac | 23 | And the final spirit... |
| 0x102dc4 | 40 | He carefully sips from this cup as well. |
| 0x102ded | 52 | A subtle freshness... The make is alike the third,\n |
| 0x102e22 | 33 | but I mark an element distinct... |
| 0x102e44 | 50 | A whisper of fruit, like that of delicacies from\n |
| 0x102e77 | 10 | the south. |
| 0x102e82 | 50 | A perplexment! Did yon flavor birth upon contact\n |
| 0x102eb5 | 41 | with the air? Was there aught I missed?\n |
| 0x102edf | 13 | Or perhaps... |
| 0x102eed | 45 | Maroro closes his eyes, pausing in thought... |
| 0x102f1b | 48 | And all becometh clear! Why, Master Ukon, thou\n |
| 0x102f4c | 39 | deceiver! Seeking to bamboozle me so... |
| 0x102f74 | 19 | Dahahahaha! Guilty! |
| 0x102f88 | 25 | Huh...? What do you mean? |
| 0x102fa2 | 48 | I splashed some of the other drink on my thumb\n |
| 0x102fd3 | 50 | and mixed it into this one while I moved the cups. |
| 0x103006 | 43 | I was wondering why he did it so roughly.\n |
| 0x103032 | 19 | That explains it... |
| 0x103046 | 36 | If that is so, the rest I know...!\n |
| 0x10306b | 8 | How now? |
| 0x103074 | 52 | The five cups have been rearranged back to exactly\n |
| 0x1030a9 | 18 | the correct order. |
| 0x1030bc | 41 | Well, I'll be damned. You got it perfect. |
| 0x1030e6 | 10 | Amazing... |
| 0x1030f1 | 50 | A trifle, master! This much and more can I judge\n |
| 0x103124 | 23 | with the barest effort! |
| 0x10313c | 51 | Look thou this cup here--clay, mixed with bestial\n |
| 0x103170 | 49 | bones. It is basted in glass glaze, then thusly\n |
| 0x1031a2 | 6 | baked. |
| 0x1031a9 | 31 | That sounds pretty complicated. |
| 0x1031c9 | 53 | The simple texture is well prized among collectors.\n |
| 0x1031ff | 45 | Using such cups for tasting is luxury itself. |
| 0x10322d | 46 | I think I've seen something similar to these\n |
| 0x10325c | 31 | at the market before, though... |
| 0x10327c | 48 | Ah, one should be ever vigilant, for there are\n |
| 0x1032ad | 43 | many counterfeits of fine and careful make. |
| 0x1032d9 | 48 | True vessels have sides enthinned, so that the\n |
| 0x10330a | 49 | light of the sun may pierce through to thine eye. |
| 0x10333c | 45 | I raise the cup as I'm told, peering to see\n |
| 0x10336a | 37 | if any light shines through this one. |
| 0x103390 | 23 | ...Nope, still no clue. |
| 0x1033a8 | 42 | ...I'm sure I'd be easily fooled by such\n |
| 0x1033d3 | 13 | counterfeits. |
| 0x1033e1 | 47 | You ain't from a noble family for nothing, huh? |
| 0x103411 | 48 | I fear any true nobility we may have upheld is\n |
| 0x103442 | 16 | long since gone. |
| 0x103453 | 46 | Such skill is attained only through rampant,\n |
| 0x103482 | 46 | frivolous waste of money. A skill of no true\n |
| 0x1034b1 | 10 | purpose... |
| 0x1034bc | 28 | Hey, that's not true at all. |
| 0x1034d9 | 50 | All that spending wasn't a total waste if you've\n |
| 0x10350c | 49 | at least gotten something out of it, right, Maro? |
| 0x10353e | 36 | Your skill isn't a waste of money.\n |
| 0x103563 | 23 | It's an asset of yours. |
| 0x10357b | 14 | Master Haku... |
| 0x10358a | 49 | Thou art the only one who hath ever spoken such\n |
| 0x1035bc | 31 | sentiment to me, Master Haku... |
| 0x1035dc | 41 | I think you're exaggerating way too much. |
| 0x103606 | 21 | 'Tis no exaggeration! |
| 0x10361c | 51 | All my life, I have been cast down, insulted as a\n |
| 0x103650 | 46 | noble fallen from all grace. A truest failure. |
| 0x10367f | 47 | Before I dedicated mind and heart to the life\n |
| 0x1036af | 44 | of a scholar, I had but naught of mine own\n |
| 0x1036dc | 8 | worth... |
| 0x1036e5 | 9 | I... I... |
| 0x1036ef | 47 | A gloomy air descends over our attempted party. |
| 0x10371f | 47 | ...C-Come on, now, look at all the good stuff\n |
| 0x10374f | 34 | in front of us. Just enjoy, buddy. |
| 0x103772 | 36 | ...As ever, thou art in the right.\n |
| 0x103797 | 47 | Let us drink down all solemnity, and drink up\n |
| 0x1037c7 | 18 | till dawn's light. |
| 0x1037da | 46 | Got some good food here, too. Go on, have as\n |
| 0x103809 | 19 | much as you'd like. |
| 0x10381d | 36 | I wouldn't mind having some as well. |
| 0x103842 | 48 | Is this bottle supposed to be high-grade stuff\n |
| 0x103873 | 4 | too? |
| 0x103878 | 45 | Ah, I see that hath not escaped thy notice!\n |
| 0x1038a6 | 46 | Thou art bless'd with a discerning eye, good\n |
| 0x1038d5 | 12 | Master Haku. |
| 0x1038e2 | 46 | This bottle is one oft used for celebrations\n |
| 0x103911 | 41 | held by a family of lineage most royal... |
| 0x10393b | 34 | Such slender and symmetric form!\n |
| 0x10395e | 43 | Such delicate make! Art thou not bedazzled? |
| 0x10398a | 47 | When you put it that way, it does seem pretty\n |
| 0x1039ba | 8 | fancy... |
| 0x1039c3 | 39 | Such decadence is not easily come by!\n |
| 0x1039eb | 47 | While at a trusted dealer's, my father spared\n |
| 0x103a1b | 17 | no expense, and-- |
| 0x103a2d | 33 | My father... spared no expense... |
| 0x103a53 | 22 | ...Just drink up, man. |
| 0x103a6a | 18 | ...Aye. My thanks. |
| 0x103a7d | 15 | *Gulp, gulp*... |
| 0x103a8d | 47 | This has gotten strangely morose, hasn't it...? |
| 0x103abd | 45 | Well, when you're drinkin', sometimes these\n |
| 0x103aeb | 19 | things just happen. |
| 0x103aff | 49 | And so the men drink quietly through the night... |
| 0x10434f | 47 | Praise the day... Ere the fateful hour comes,\n |
| 0x10437f | 21 | my debts are settled. |
| 0x104395 | 49 | Maroro walks the busy street alone, having just\n |
| 0x1043c7 | 46 | dashed about the city making payments to his\n |
| 0x1043f6 | 10 | creditors. |
| 0x104401 | 45 | Wherefore must poor Maroro run this moneyed\n |
| 0x10442f | 31 | gauntlet with each new moon...? |
| 0x10444f | 45 | Alas. Erelong, I should slake my thirst and\n |
| 0x10447d | 23 | seek an evening's rest. |
| 0x104495 | 45 | With tired steps, Maroro trudges toward his\n |
| 0x1044c3 | 45 | favorite bar--one that keeps a drinking tab\n |
| 0x1044f1 | 13 | open for him. |
| 0x1044ff | 48 | Relief and comfort wash over him as he settles\n |
| 0x104530 | 20 | into his usual seat. |
| 0x104545 | 48 | Ah... Mayhap Master Haku and his company would\n |
| 0x104576 | 28 | enjoy an evening hereabouts. |
| 0x104593 | 7 | Barkeep |
| 0x10459b | 31 | Welcome. What will it be today? |
| 0x1045bb | 47 | Prithee, drinkmaster--my throat is in need of\n |
| 0x1045eb | 47 | fire to warm and wet it. Bring thee something\n |
| 0x10461b | 7 | strong. |
| 0x104623 | 43 | We have an excellent imported liquor this\n |
| 0x10464f | 39 | evening. Shall I open a bottle for you? |
| 0x104677 | 40 | Though mindful of his finances, Maroro\n |
| 0x1046a0 | 45 | considers it, and decides to put the bottle\n |
| 0x1046ce | 11 | on his tab. |
| 0x1046da | 39 | Surely, besiege'd Maroro deserveth an\n |
| 0x104702 | 29 | indulgence once each while... |
| 0x104720 | 49 | Here we are, sir. The finest sake, aged no less\n |
| 0x104752 | 18 | than thirty years. |
| 0x104765 | 50 | Ah, such color! Such fragrance. A fine potation,\n |
| 0x104798 | 24 | ere I laid eyes upon it. |
| 0x1047b1 | 5 | *Sip* |
| 0x1047b7 | 42 | A strong, honey-like fragrance fills his\n |
| 0x1047e2 | 44 | nostrils as he drinks, flavors harmonizing\n |
| 0x10480f | 14 | on his tongue. |
| 0x10481e | 43 | An elixir most deserving of its prestige.\n |
| 0x10484a | 44 | Methinks Master Haku would take to it with\n |
| 0x104877 | 5 | glee. |
| 0x10487d | 48 | Mayhap, ere I return here, I shall entreat him\n |
| 0x1048ae | 39 | for his company on some lonesome eve... |
| 0x1048d6 | 44 | Slowly nursing the sake, Maroro allows his\n |
| 0x104903 | 48 | worries to melt away, enjoying a gentle, tipsy\n |
| 0x104934 | 5 | buzz. |
| 0x10493a | 46 | ...Bah. A lone cup ill satisfies the demands\n |
| 0x104969 | 26 | my thirst doth make of me. |
| 0x104984 | 23 | Would you like another? |
| 0x10499c | 48 | Seeing Maroro staring wistfully into his empty\n |
| 0x1049cd | 29 | cup, the bartender speaks up. |
| 0x1049eb | 35 | So be it. Prithee, barman--another. |
| 0x104a0f | 47 | Unable to resist the temptation of fine sake,\n |
| 0x104a3f | 26 | Maroro continues to drink. |
| 0x104a5a | 44 | Gadzooks. An exercise in excess, methinks.\n |
| 0x104a87 | 33 | My poor head, how it doth spin... |
| 0x104aa9 | 46 | Barkeep, speak words. What coin do I owe thee? |
| 0x104ad8 | 16 | Here, your bill. |
| 0x104ae9 | 44 | Maroro accepts the bill as the bar's owner\n |
| 0x104b16 | 43 | hands it to him, eyes scanning the total... |
| 0x104b42 | 48 | Ah, m-more a strain on the pocketbook than one\n |
| 0x104b73 | 18 | expected, I see... |
| 0x104b86 | 44 | Yes, it's a very rare sake. We only have a\n |
| 0x104bb3 | 37 | few dozen bottles left in our stores. |
| 0x104bd9 | 46 | On top of that, I'm only barely charging you\n |
| 0x104c08 | 44 | above cost, since you're one of my regulars. |
| 0x104c35 | 44 | I-I see. Pray forgive me, sir, but wouldst\n |
| 0x104c62 | 42 | thou consider adding the sum to my tab...? |
| 0x104c8d | 45 | Upon hearing that, the bartender shakes his\n |
| 0x104cbb | 20 | head apologetically. |
| 0x104cd0 | 46 | Any other day, I'd be willing to do that for\n |
| 0x104cff | 45 | you, but... the head of your family came in\n |
| 0x104d2d | 8 | earlier. |
| 0x104d36 | 39 | Mine own father? Wh-What did he seek?\n |
| 0x104d5e | 8 | Tell me! |
| 0x104d67 | 45 | He stopped in to see to some items that had\n |
| 0x104d95 | 19 | accumulated, and... |
| 0x104da9 | 34 | Speak! Wh-What did he say to you!? |
| 0x104dcc | 50 | He said... "Having a tab at a bar besmirches our\n |
| 0x104dff | 43 | family's name. Pay it all in one lump sum." |
| 0x104e2b | 9 | Wh-What!? |
| 0x104e35 | 46 | After working and apologizing frantically in\n |
| 0x104e64 | 43 | his father's place, this is the treatment\n |
| 0x104e90 | 12 | Maroro gets. |
| 0x104e9d | 42 | O, woe. How could it have come to this...? |
| 0x104ec8 | 48 | Maroro rubs his face, letting out a tired groan. |
| 0x104ef9 | 47 | The barkeep, watching on, sheds a sympathetic\n |
| 0x104f29 | 13 | tear for him. |
| 0x104f37 | 47 | I, ah... Please, forget about it for tonight.\n |
| 0x104f67 | 39 | You can pay for it next time you visit. |
| 0x104f8f | 44 | That small mercy is all the barkeep can do\n |
| 0x104fbc | 8 | for him. |
| 0x105770 | 6 | Ngh... |
| 0x105777 | 37 | Ach... I guess I overdid it a little. |
| 0x10579d | 45 | I woke up thirsty in the middle of the night. |
| 0x1057cb | 45 | Tch, forgot to refill the carafe. No choice\n |
| 0x1057f9 | 22 | but to go out, then... |
| 0x105810 | 47 | The only sound in the hall is a quiet breeze.\n |
| 0x105840 | 44 | It's like I can feel everyone else sleeping. |
| 0x10586d | 12 | ...Chilly... |
| 0x10587a | 49 | I try not to disturb the peaceful quiet, moving\n |
| 0x1058ac | 23 | silently down the hall. |
| 0x1058c4 | 12 | ...? Voices? |
| 0x1058d1 | 48 | I strain to make out a voice on the edge of my\n |
| 0x105902 | 32 | hearing. Where's it coming from? |
| 0x105923 | 19 | Kuon's room, huh... |
| 0x105937 | 36 | I pause next to her room, listening. |
| 0x10595c | 41 | Who could she be talking to at this hour? |
| 0x105986 | 47 | ...that said, of course... young master, too,\n |
| 0x1059b6 | 5 | is... |
| 0x1059bc | 30 | ...yes, ever since you left... |
| 0x1059db | 46 | ...intention of going back... mind... made up. |
| 0x105a0a | 44 | Who's she talking to? That's not a voice I\n |
| 0x105a37 | 7 | know... |
| 0x105a3f | 46 | Their conversation is too faint to make out.\n |
| 0x105a6e | 33 | I can't tell what they're saying. |
| 0x105a90 | 47 | I should just refill my carafe and go back to\n |
| 0x105ac0 | 31 | bed. No point in eavesdropping. |
| 0x105ae0 | 26 | ...staying a bit longer.\n |
| 0x105afb | 23 | Please tell him that... |
| 0x105b13 | 44 | ...but... should talk to the young master... |
| 0x105b40 | 22 | We urge... reconsider. |
| 0x105b57 | 47 | As I walk away, their conversation only seems\n |
| 0x105b87 | 20 | to grow more heated. |
| 0x105b9c | 42 | Maybe I ought to at least check on her...? |
| 0x105bc7 | 42 | Letting my concern get the better of me,\n |
| 0x105bf2 | 36 | I knock on her door. All goes quiet. |
| 0x105c17 | 10 | Who is it? |
| 0x105c22 | 35 | S-Sorry to bother you at this hour. |
| 0x105c46 | 45 | Is that you, Haku? What are you doing up so\n |
| 0x105c74 | 5 | late? |
| 0x105c7a | 43 | I heard you arguing with somebody and got\n |
| 0x105ca6 | 32 | worried. Everything OK in there? |
| 0x105cc7 | 44 | What are you talking about? There's nobody\n |
| 0x105cf4 | 42 | besides me... Here, come inside for a sec. |
| 0x105d1f | 44 | What? I could have sworn I'd heard voices.\n |
| 0x105d4c | 20 | That makes no sense. |
| 0x105d61 | 45 | I slide the door open to find Kuon drinking\n |
| 0x105d8f | 22 | tea, remarkably alone. |
| 0x105da6 | 45 | ...Huh. You're sure nobody else was in here\n |
| 0x105dd4 | 9 | with you? |
| 0x105dde | 17 | Somebody like...? |
| 0x105df0 | 28 | Ah, I'm not... I don't know. |
| 0x105e0d | 42 | I was just taking a break from studying.\n |
| 0x105e38 | 11 | Are you OK? |
| 0x105e44 | 48 | She does, in fact, have a textbook laid out in\n |
| 0x105e75 | 13 | front of her. |
| 0x105e83 | 39 | Bizarre. I'm sure I heard conversation. |
| 0x105eab | 46 | As I puzzle over the strange situation, Kuon\n |
| 0x105eda | 38 | pulls something from her medicine bag. |
| 0x105f01 | 40 | I know THAT look. Drank too much, huh?\n |
| 0x105f2a | 46 | Take this if you don't wanna feel it tomorrow. |
| 0x105f59 | 44 | It's not a good idea to overdo it, you know. |
| 0x105f86 | 46 | She hands me the medicine with a look that's\n |
| 0x105fb5 | 32 | somehow both blaming and caring. |
| 0x105fd6 | 38 | Y-Yeah... sorry. I'll be more careful. |
| 0x105ffd | 45 | I'm certain I wasn't hearing things, but it\n |
| 0x10602b | 39 | definitely looks like she's alone. Huh. |
| 0x106053 | 42 | Get some rest, Haku. I'll see you in the\n |
| 0x10607e | 8 | morning. |
| 0x106087 | 17 | Yeah, good night. |
| 0x106099 | 34 | Right... I should get back to bed. |
| 0x1060bc | 44 | I take Kuon's medicine on my way back, and\n |
| 0x1060e9 | 44 | suddenly I remember what I left for in the\n |
| 0x106116 | 12 | first place. |
| 0x106123 | 42 | Hhhurgh--! B--Bitter! Water! I need water! |
| 0x10aa37 | 46 | Finally, I can relax in my room for a while... |
| 0x10aa66 | 47 | I returned to the Hakurokaku to find a letter\n |
| 0x10aa96 | 12 | on my table. |
| 0x10aaa3 | 12 | What's this? |
| 0x10aab0 | 20 | Let's have a look... |
| 0x10aac9 | 42 | Yikes, this is... really formal-looking.\n |
| 0x10aaf4 | 12 | Let's see... |
| 0x10ab01 | 49 | ...have recently acquired... fine libations and\n |
| 0x10ab33 | 37 | food... Presence requested forthwith? |
| 0x10ab59 | 47 | Please extend... warmest regards and likewise\n |
| 0x10ab89 | 32 | invite any of your companions... |
| 0x10abaa | 21 | ...Yours sincerely,\n |
| 0x10abc0 | 25 | the Hakurokaku Inn Owner. |
| 0x10abda | 47 | The paper used to write the letter is finely-\n |
| 0x10ac0a | 36 | made, and smells faintly of incense. |
| 0x10ac2f | 41 | Seems like the proprietor of the inn is\n |
| 0x10ac59 | 36 | inviting us for drinks and dinner... |
| 0x10ac7e | 40 | I'll bet it's that woman I met. Karulau. |
| 0x10aca7 | 44 | The beautiful woman I met on the top floor\n |
| 0x10acd4 | 29 | of the inn. It has to be her. |
| 0x10acf2 | 44 | And since when do you get invited for fine\n |
| 0x10ad1f | 33 | dining from people like that, hm? |
| 0x10ad41 | 4 | Wh-- |
| 0x10ad46 | 48 | Kuon appears in front of me before I even have\n |
| 0x10ad77 | 18 | a chance to react. |
| 0x10ad8a | 36 | We just met the other day, is all!\n |
| 0x10adaf | 23 | Nothing more than that. |
| 0x10adc7 | 46 | Looks like a woman's handwriting. What's she\n |
| 0x10adf6 | 5 | like? |
| 0x10adfc | 24 | What's she like? Well... |
| 0x10ae15 | 23 | Mysterious, maybe...?\n |
| 0x10ae2d | 10 | Enigmatic? |
| 0x10ae38 | 38 | She's beautiful, that much is certain. |
| 0x10ae5f | 26 | An enigmatic beauty, eh... |
| 0x10ae7a | 38 | Kuon seems suspicious for some reason. |
| 0x10aea1 | 28 | Do you want to come with me? |
| 0x10aebe | 18 | Eh? Come with you? |
| 0x10aed1 | 45 | I try inviting Kuon along, but her response\n |
| 0x10aeff | 18 | seems... hesitant. |
| 0x10af12 | 23 | Are you sure that's OK? |
| 0x10af2a | 41 | Says here to "extend invitations" to my\n |
| 0x10af54 | 27 | friends. It oughta be fine. |
| 0x10af70 | 45 | Ah, so it does. All right, I'm curious now.\n |
| 0x10af9e | 19 | I'll come with you. |
| 0x10afb2 | 45 | I've been wanting to meet the owner of this\n |
| 0x10afe0 | 38 | place, but I haven't had a chance yet. |
| 0x10b007 | 47 | And the "fine libations and food" part has my\n |
| 0x10b037 | 10 | attention. |
| 0x10b042 | 46 | Of course that's what you're actually after... |
| 0x10b071 | 45 | With Kuon in tow, I head for the top floor,\n |
| 0x10b09f | 47 | where we find wide, open windows looking over\n |
| 0x10b0cf | 21 | the imperial capital. |
| 0x10b0e5 | 48 | The cityscape stretches all the way out to the\n |
| 0x10b116 | 8 | horizon. |
| 0x10b11f | 46 | Wow, that's some view. I never imagined THIS\n |
| 0x10b14e | 30 | was hiding on the top floor... |
| 0x10b16d | 41 | Kuon's eyes fix on the distant horizon,\n |
| 0x10b197 | 27 | overlooking the city below. |
| 0x10b1b3 | 42 | ...are you sure this is the right place?\n |
| 0x10b1de | 13 | It's empty... |
| 0x10b1ec | 27 | No, this isn't it. Hold on. |
| 0x10b208 | 4 | Huh? |
| 0x10b20d | 45 | I wink at Kuon and walk up to the mechanism\n |
| 0x10b23b | 40 | locking the stairs--and find a surprise. |
| 0x10b264 | 6 | Worker |
| 0x10b26b | 42 | If I recall correctly, this goes here...\n |
| 0x10b296 | 18 | No... was it here? |
| 0x10b2a9 | 45 | One of the Hakurokaku's workers crouches by\n |
| 0x10b2d7 | 46 | the mechanism, talking to herself obliviously. |
| 0x10b306 | 37 | Then this piece goes... vertically?\n |
| 0x10b32c | 28 | No, that is not it either... |
| 0x10b349 | 43 | She seems to be struggling with the puzzle. |
| 0x10b375 | 47 | This foul contrivance. Have I made a mistake?\n |
| 0x10b3a5 | 35 | Such carelessness is inexcusable... |
| 0x10b3c9 | 40 | Perhaps the workings are merely loose?\n |
| 0x10b3f2 | 24 | Should I push harder...? |
| 0x10b40b | 21 | H-Hey, hold on! Wait! |
| 0x10b421 | 45 | I manage to stop her just before she throws\n |
| 0x10b44f | 35 | her full weight against the device. |
| 0x10b473 | 6 | ...Eh? |
| 0x10b47a | 24 | A-Augh!! Who goes th--\n |
| 0x10b493 | 30 | I-I mean, can I help you, sir? |
| 0x10b4b2 | 34 | Hm? That pattern... isn't that...? |
| 0x10b4d5 | 6 | Hyah!? |
| 0x10b4dc | 47 | The worker's eyes fall on Kuon, and she makes\n |
| 0x10b50c | 13 | an odd noise. |
| 0x10b51a | 43 | Pardon us. We were invited up here by the\n |
| 0x10b546 | 30 | owner, and we'd like to go up. |
| 0x10b565 | 10 | The owner? |
| 0x10b570 | 47 | Truly? Karu--? I mean, ah. Yes, sir. Of course. |
| 0x10b5a0 | 43 | Go... up? Haku, aren't we on the top floor? |
| 0x10b5cc | 19 | You'd think that... |
| 0x10b5e0 | 44 | There's a gimmick to it. A hidden stairway\n |
| 0x10b60d | 42 | appears if you work this puzzle correctly. |
| 0x10b638 | 42 | Aha, I knew it! An old clockwork device... |
| 0x10b663 | 43 | Kuon traces the intricate workings with a\n |
| 0x10b68f | 36 | finger, her eyes positively shining. |
| 0x10b6b4 | 44 | Ah, this takes me back. I had no idea this\n |
| 0x10b6e1 | 30 | country had devices like this. |
| 0x10b700 | 38 | You have something like this in your\n |
| 0x10b727 | 9 | homeland? |
| 0x10b731 | 9 | Uh-huh.\n |
| 0x10b73b | 17 | My mother, see... |
| 0x10b74d | 46 | She begins to shift the pieces of the puzzle\n |
| 0x10b77c | 13 | as she talks. |
| 0x10b78a | 51 | She collected objects like this. It always seemed\n |
| 0x10b7be | 32 | out-of-character for her, but... |
| 0x10b7df | 44 | There we are. This one goes here, that one\n |
| 0x10b80c | 22 | like this, and then... |
| 0x10b823 | 43 | The puzzle-like patterns of the lock snap\n |
| 0x10b84f | 44 | together, and the stairs descend from above. |
| 0x10b87c | 27 | There we go. Impressed yet? |
| 0x10b898 | 26 | I solved it too, you know. |
| 0x10b8b3 | 34 | Just... not as quickly as you did. |
| 0x10b8d6 | 33 | Could I ask you a question, miss? |
| 0x10b8f8 | 41 | I am--that is to say, ah--Housekeeping!\n |
| 0x10b922 | 39 | I'm very busy. Doing housekeeping. Yes. |
| 0x10b94a | 45 | The worker abruptly turns to begin wiping a\n |
| 0x10b978 | 36 | perfectly clean section of the wall. |
| 0x10b99d | 28 | Have we... met before, miss? |
| 0x10b9ba | 40 | Hah! See there! Stubborn stains in the\n |
| 0x10b9e3 | 9 | paneling! |
| 0x10b9ed | 48 | As Kuon approaches her to get a better look at\n |
| 0x10ba1e | 44 | her face, she crouches quickly to the floor. |
| 0x10ba4b | 5 | Miss? |
| 0x10ba51 | 46 | Next to us, the stairs slide out and unfold,\n |
| 0x10ba80 | 29 | unlocked by Kuon's handiwork. |
| 0x10ba9e | 42 | There's our way up. If you'll excuse us,\n |
| 0x10bac9 | 6 | ma'am. |
| 0x10bad0 | 34 | Y-Yes, sir! Please do not mind me! |
| 0x10baf3 | 46 | With that, the worker returns to her wiping,\n |
| 0x10bb22 | 31 | her nose inches from the floor. |
| 0x10bb47 | 37 | Come on, Kuon. She's got a job to do. |
| 0x10bb6d | 14 | A-All right... |
| 0x10bb7c | 48 | She'll be fine. I think she's just embarrassed\n |
| 0x10bbad | 29 | we saw her screw up the lock. |
| 0x10bbcb | 46 | I whisper my suspicion to Kuon, and she lets\n |
| 0x10bbfa | 30 | it go, moving to follow me up. |
| 0x10bc19 | 46 | As we emerge into the hidden attic, the same\n |
| 0x10bc48 | 35 | incense as before assaults my nose. |
| 0x10bc6c | 46 | My eyes take a moment to adjust to the dark.\n |
| 0x10bc9b | 27 | I scan the familiar room... |
| 0x10bcb7 | 48 | But the enigmatic woman from before is nowhere\n |
| 0x10bce8 | 12 | to be found. |
| 0x10bcf5 | 19 | ...Maybe she's out? |
| 0x10bd09 | 23 | Hm. She has good taste. |
| 0x10bd21 | 46 | Kuon breathes her admiration as she takes in\n |
| 0x10bd50 | 12 | the scenery. |
| 0x10bd5d | 28 | This atmosphere, though...\n |
| 0x10bd7a | 18 | It reminds me of-- |
| 0x10bd8d | 7 | Hmhm... |
| 0x10bd95 | 50 | Playful, satisfied laughter, like a chess master\n |
| 0x10bdc8 | 36 | admiring a move, echoes in the dark. |
| 0x10bdf3 | 33 | Kuon flinches, freezing in place. |
| 0x10be15 | 45 | I look over my shoulder, and there sits the\n |
| 0x10be43 | 48 | Hakurokaku's owner, as if she'd been there the\n |
| 0x10be74 | 12 | entire time. |
| 0x10be81 | 45 | I never expected such a compliment from YOU\n |
| 0x10beaf | 20 | of all people, dear. |
| 0x10bec4 | 48 | Kuon turns, still rooted in place, and I swear\n |
| 0x10bef5 | 43 | I can hear her slowly grinding to face her. |
| 0x10bf21 | 47 | I'm pleased to see your tastes have developed\n |
| 0x10bf51 | 45 | quite nicely. It's been some time, hasn't it? |
| 0x10bf7f | 32 | I'm happy to see you well, Kuon. |
| 0x10bfa0 | 11 | M-Mothe--!? |
| 0x10bfac | 36 | Kuon doesn't get to finish the word. |
| 0x10bfd1 | 46 | A sudden, palpable air of intimidation fills\n |
| 0x10c000 | 31 | the room, blade-like and sharp. |
| 0x10c020 | 45 | If looks could kill, I might have just seen\n |
| 0x10c04e | 39 | Kuon's head severed from her shoulders. |
| 0x10c076 | 35 | Could it just be my imagination...? |
| 0x10c09a | 8 | U-Urk... |
| 0x10c0a3 | 45 | Or maybe Kuon felt it too. Her hand goes to\n |
| 0x10c0d1 | 46 | her neck, as though the hair on it had stood\n |
| 0x10c100 | 3 | up. |
| 0x10c104 | 44 | What was that, now? Did you say something,\n |
| 0x10c131 | 8 | my dear? |
| 0x10c13a | 40 | A-Ah, no--nothing, dear sister. Nothing. |
| 0x10c163 | 18 | Huh? You know her? |
| 0x10c176 | 40 | They definitely don't seem like simple\n |
| 0x10c19f | 37 | acquaintances, that much is for sure. |
| 0x10c1c5 | 41 | Sh-She's, ah... one of the m--Sisters!!\n |
| 0x10c1ef | 23 | Sisters, who raised me. |
| 0x10c207 | 45 | A few years back, she said she was going on\n |
| 0x10c235 | 34 | a trip and disappeared, but now... |
| 0x10c258 | 46 | Fate weaves such an... interesting tapestry,\n |
| 0x10c287 | 19 | wouldn't you agree? |
| 0x10c29b | 46 | She smiles self-assuredly, but it only seems\n |
| 0x10c2ca | 32 | to make Kuon more uncomfortable. |
| 0x10c2eb | 46 | Karulau must have some kind of leverage over\n |
| 0x10c31a | 4 | her. |
| 0x10c31f | 47 | Please have a seat, won't you? You're guests,\n |
| 0x10c34f | 30 | after all. Welcome to my room. |
| 0x10c36e | 42 | We each find seats across the table from\n |
| 0x10c399 | 29 | Karulau. Something feels off. |
| 0x10c3b7 | 31 | What are we supposed to do now? |
| 0x10c3d7 | 46 | The "fine libations and food" are nowhere in\n |
| 0x10c406 | 6 | sight. |
| 0x10c40d | 44 | Karulau simply sits, eyes resting on Kuon,\n |
| 0x10c43a | 14 | smiling oddly. |
| 0x10c449 | 41 | Kuon avoids her stare, stiff and awkward. |
| 0x10c473 | 45 | This feels more like an interview for a job\n |
| 0x10c4a1 | 15 | than a feast... |
| 0x10c4b1 | 10 | Hey, Kuon. |
| 0x10c4bc | 45 | I whisper to Kuon, who remains frozen in...\n |
| 0x10c4ea | 7 | terror? |
| 0x10c4f2 | 43 | She's your family, right? Don't you have,\n |
| 0x10c51e | 29 | y'know, things to talk about? |
| 0x10c53c | 32 | I've never seen her like this... |
| 0x10c55d | 33 | Don't tell me you're clamming up? |
| 0x10c57f | 9 | W-Well... |
| 0x10c589 | 49 | A-Among my mothers, you see--Karulau is the one\n |
| 0x10c5bb | 35 | I most admire, the one I emulate... |
| 0x10c5df | 8 | Mothers? |
| 0x10c5e8 | 42 | The unusual plural catches me off-guard.\n |
| 0x10c613 | 6 | Huh... |
| 0x10c61a | 45 | Karulau is difficult to figure out. She has\n |
| 0x10c648 | 35 | a noble bearing, a knowing smile... |
| 0x10c66c | 49 | But... if there's one thing I know for certain,\n |
| 0x10c69e | 32 | she's important to Kuon somehow. |
| 0x10c6bf | 45 | Oh? Don't be whispering to each other, now.\n |
| 0x10c6ed | 22 | What's the big secret? |
| 0x10c704 | 34 | Anything you care to let me in on? |
| 0x10c727 | 43 | She smiles teasingly, and Kuon decides to\n |
| 0x10c753 | 18 | break her silence. |
| 0x10c766 | 41 | You haven't asked me why I came here to\n |
| 0x10c790 | 9 | Yamato... |
| 0x10c79a | 46 | I see. You want me to be curious about that,\n |
| 0x10c7c9 | 7 | do you? |
| 0x10c7d1 | 36 | Her smile renders Kuon silent again. |
| 0x10c7f6 | 46 | It's like a sulking child being seen through\n |
| 0x10c825 | 29 | by her parents. So strange... |
| 0x10c843 | 46 | Just as the "conversation" seems to be going\n |
| 0x10c872 | 36 | nowhere, I start to speak up, when-- |
| 0x10c897 | 43 | Lord and ladies, forgive m--Ah, I mean...\n |
| 0x10c8c3 | 38 | Thank you for waiting, honored guests. |
| 0x10c8ea | 48 | That strange worker returns with cups balanced\n |
| 0x10c91b | 10 | on a tray. |
| 0x10c926 | 28 | Thank you two for waiting.\n |
| 0x10c943 | 27 | Now, shall we have a toast? |
| 0x10c95f | 43 | The cups she places down are masterworks,\n |
| 0x10c98b | 26 | even to an amateur's eyes. |
| 0x10c9a6 | 45 | I-I'm very sorry! I'll clean it right away... |
| 0x10c9d4 | 42 | But her movement is strange and stilted.\n |
| 0x10c9ff | 43 | She's clearly used to this work, but it's\n |
| 0x10ca2b | 16 | oddly awkward... |
| 0x10ca3c | 48 | Be that as it may, why is she serving us while\n |
| 0x10ca6d | 45 | looking away...? Some weird local etiquette\n |
| 0x10ca9b | 6 | thing? |
| 0x10caa2 | 7 | ...Hmm? |
| 0x10caaa | 37 | Kuon seems to have noticed something. |
| 0x10cad0 | 25 | Wait... You can't be...!? |
| 0x10caea | 48 | Kuon bolts up in a swift motion and stares the\n |
| 0x10cb1b | 24 | housekeeper in her face. |
| 0x10cb34 | 20 | ...Mother... Touka!? |
| 0x10cb49 | 46 | Hyah!? N-No! I have no idea who you could be\n |
| 0x10cb78 | 40 | referring to! At all! I am a... a mere\n |
| 0x10cba1 | 14 | housekeeper... |
| 0x10cbb0 | 49 | I knew there was something strange about you...\n |
| 0x10cbe2 | 28 | But it's really you, mother. |
| 0x10cbff | 43 | Ughhh... I-I am not this... this Touka...\n |
| 0x10cc2b | 5 | No... |
| 0x10cc31 | 46 | If you've been so close to me all this time,\n |
| 0x10cc60 | 34 | why didn't you tell me, I wonder!? |
| 0x10cc83 | 39 | Touka, why don't you stop serving us?\n |
| 0x10ccab | 34 | Our beloved sister is with us now. |
| 0x10ccce | 7 | Nngh... |
| 0x10ccd6 | 46 | Touka the housekeeper... well, the lady in a\n |
| 0x10cd05 | 44 | housekeeper's uniform... finally turns her\n |
| 0x10cd32 | 11 | face to us. |
| 0x10cd3e | 47 | She seems different from the owner, but she's\n |
| 0x10cd6e | 43 | definitely pretty. Kind of masculine, but\n |
| 0x10cd9a | 11 | charming... |
| 0x10cda6 | 13 | ...Karulau... |
| 0x10cdb4 | 16 | Something wrong? |
| 0x10cdc5 | 44 | You knew Kuon would be coming up here, and\n |
| 0x10cdf2 | 22 | told me nothing of it? |
| 0x10ce09 | 47 | Oh, but I'm sure I did, didn't I? I said that\n |
| 0x10ce39 | 48 | I would invite someone important; someone also\n |
| 0x10ce6a | 16 | familiar to you. |
| 0x10ce7b | 39 | ...I will listen to your excuses later. |
| 0x10cea3 | 48 | The housekeeper quakes with anger for a moment\n |
| 0x10ced4 | 46 | more, but finally turns her calm face to Kuon. |
| 0x10cf03 | 45 | It's been a long time... How have you been?\n |
| 0x10cf31 | 42 | You have grown since the last time I saw\n |
| 0x10cf5c | 6 | you... |
| 0x10cf63 | 31 | Touka hugs Kuon with both arms. |
| 0x10cf83 | 47 | I wanted to say something to you on the first\n |
| 0x10cfb3 | 42 | day, but I lost my chance. My apologies... |
| 0x10cfde | 49 | Her gestures are a bit uncouth and awkward, but\n |
| 0x10d010 | 45 | I can feel her sincere love for Kuon in them. |
| 0x10d03e | 9 | Mother... |
| 0x10d048 | 43 | Kuon seems a bit embarrassed by this, but\n |
| 0x10d074 | 45 | there's a genuine and deep happiness there,\n |
| 0x10d0a2 | 4 | too. |
| 0x10d0a7 | 40 | The owner watches them peaceably, eyes\n |
| 0x10d0d0 | 12 | half-lidded. |
| 0x10d0dd | 46 | That face says... "My girl can be so defiant\n |
| 0x10d10c | 44 | to me. But she can act so sweet with other\n |
| 0x10d139 | 8 | people." |
| 0x10d142 | 31 | Did you say something just now? |
| 0x10d162 | 21 | ...No, miss, nothing. |
| 0x10d178 | 45 | Touka, don't forget that we're entertaining\n |
| 0x10d1a6 | 8 | a guest. |
| 0x10d1af | 18 | Hm. You are right. |
| 0x10d1c2 | 48 | Touka gently releases Kuon, and politely turns\n |
| 0x10d1f3 | 20 | her attention to me. |
| 0x10d208 | 43 | Allow me to introduce myself. I am Touka,\n |
| 0x10d234 | 44 | a worker of the Hakurokaku Inn. A pleasure\n |
| 0x10d261 | 17 | to meet you, sir. |
| 0x10d273 | 40 | You realize we are the only ones here?\n |
| 0x10d29c | 47 | You don't have to worry so much about showing\n |
| 0x10d2cc | 15 | your true self. |
| 0x10d2dc | 47 | Currently, I am nothing more than a worker of\n |
| 0x10d30c | 46 | the Hakurokaku Inn. No more, no less... ma'am. |
| 0x10d33b | 46 | Karulau smiles wryly as Touka says this, and\n |
| 0x10d36a | 31 | gives a small sigh in response. |
| 0x10d38a | 45 | It feels like I'm missing something here...\n |
| 0x10d3b8 | 38 | but probably best I don't pry into it. |
| 0x10d3df | 47 | Pleasure to meet you. I guess both Kuon and I\n |
| 0x10d40f | 29 | have been in your care, then. |
| 0x10d42d | 47 | I'm pretty sure I'm the one who's been taking\n |
| 0x10d45d | 18 | care of you, Haku. |
| 0x10d470 | 48 | Kuon interjects for some reason, but she seems\n |
| 0x10d4a1 | 47 | a little more childlike and playful than usual. |
| 0x10d4d1 | 47 | Likewise... Please look after Kuon for me, if\n |
| 0x10d501 | 10 | you would. |
| 0x10d50c | 47 | She bows deeply as she speaks. She seems more\n |
| 0x10d53c | 37 | like a mononofu than a simple worker. |
| 0x10d562 | 43 | Now then, shall we resume our little party? |
| 0x10d58e | 26 | Let us start with a drink. |
| 0x10d5a9 | 48 | The cup she passes to me is filled to the brim\n |
| 0x10d5da | 12 | with liquor. |
| 0x10d5e7 | 5 | Hm... |
| 0x10d5ed | 45 | It looks like the same kind I've drank here\n |
| 0x10d61b | 39 | before, but the scent is more powerful. |
| 0x10d643 | 42 | Looks like you still have some excellent\n |
| 0x10d66e | 28 | drinks in your collection... |
| 0x10d68b | 41 | Oh, but you haven't even tasted it yet.\n |
| 0x10d6b5 | 43 | Good drinks aren't meant to be enjoyed on\n |
| 0x10d6e1 | 22 | aroma alone, you know? |
| 0x10d6f8 | 33 | She chuckles a bit as she speaks. |
| 0x10d71a | 41 | If I may, I'd like to pour you a cup as\n |
| 0x10d744 | 5 | well. |
| 0x10d74a | 25 | I would gladly accept it. |
| 0x10d764 | 47 | You will be drinking with us, of course, Touka? |
| 0x10d794 | 45 | Then I will have... I mean, if you would be\n |
| 0x10d7c2 | 20 | so kind, dear guest. |
| 0x10d7d7 | 40 | Touka raises her cup as she says this.\n |
| 0x10d800 | 16 | But, uh, that... |
| 0x10d811 | 48 | That's... a little big for drinking. It's more\n |
| 0x10d842 | 23 | like a full-on tankard. |
| 0x10d85a | 45 | I guess some people enjoy it in big cups as\n |
| 0x10d888 | 43 | well. She must really be a heavy drinker... |
| 0x10d8b4 | 40 | If you're OK with it straight from the\n |
| 0x10d8dd | 16 | bottle, I can... |
| 0x10d8ee | 45 | Oh, no, you misunderstand me... Dear guest,\n |
| 0x10d91c | 24 | I wish to have some tea. |
| 0x10d935 | 46 | My, my. Bringing down the mood a bit, aren't\n |
| 0x10d964 | 46 | you, Touka? This is a party, is it not, dear\n |
| 0x10d993 | 6 | guest? |
| 0x10d99a | 48 | Karulau's glance flickers toward me, as though\n |
| 0x10d9cb | 41 | pressing me to go along with what she's\n |
| 0x10d9f5 | 7 | saying. |
| 0x10d9fd | 43 | Oh, you don't have to be so modest. Here,\n |
| 0x10da29 | 26 | drink as much as you want. |
| 0x10da44 | 43 | Oh, no, I am in the middle of work at the\n |
| 0x10da70 | 48 | moment, and--Stop stop stop stop stop stop stop! |
| 0x10daa1 | 9 | *Sigh*... |
| 0x10daab | 20 | Haku, what about me? |
| 0x10dac0 | 29 | I'll pour your drink for you. |
| 0x10dade | 22 | Huh? Mo... ah, Sister? |
| 0x10daf5 | 41 | W-Wait, Karulau. I should be the one to-- |
| 0x10db1f | 41 | Allow me this, and we can call our debt\n |
| 0x10db49 | 8 | settled. |
| 0x10db52 | 5 | Wha-- |
| 0x10db58 | 8 | B-But... |
| 0x10db61 | 45 | You won't remain a child forever. I suppose\n |
| 0x10db8f | 46 | it is time I permit you to drink. So, do you\n |
| 0x10dbbe | 7 | accept? |
| 0x10dbc6 | 5 | Uh... |
| 0x10dbcc | 42 | Hmhm... I never thought I'd see the day.\n |
| 0x10dbf7 | 21 | I suppose time flies. |
| 0x10dc0d | 41 | Urgh... If only I had not owed her that\n |
| 0x10dc37 | 8 | favor... |
| 0x10dc40 | 46 | Let us have a toast, then, to celebrate this\n |
| 0x10dc6f | 15 | happy occasion. |
| 0x10dc7f | 50 | To this wonderful day, and this wonderful place.\n |
| 0x10dcb2 | 36 | To celebrate these wonderful people. |
| 0x10dcd7 | 7 | Cheers. |
| 0x10dcdf | 10 | ...Cheers. |
| 0x10dcea | 42 | We all begin to drink, and the mood soon\n |
| 0x10dd15 | 10 | brightens. |
| 0x10dd20 | 48 | Guess all her talk of rare liquors and foreign\n |
| 0x10dd51 | 30 | delicacies wasn't for nothing. |
| 0x10dd70 | 45 | The dishes being brought out are all things\n |
| 0x10dd9e | 43 | I've never seen before, with distinct and\n |
| 0x10ddca | 17 | delicious tastes. |
| 0x10dddc | 44 | They try to explain the origin of each new\n |
| 0x10de09 | 46 | treat, but I'm way too busy stuffing my face\n |
| 0x10de38 | 10 | to listen. |
| 0x10de43 | 13 | What's more-- |
| 0x10de51 | 11 | ...Amazing! |
| 0x10de5d | 50 | I can't help but exclaim as I taste the liquors.\n |
| 0x10de90 | 45 | Every single one they bring out is fantastic. |
| 0x10debe | 42 | It gives me a certain pride as the inn's\n |
| 0x10dee9 | 44 | proprietor to see you enjoying yourself so\n |
| 0x10df16 | 5 | much. |
| 0x10df1c | 49 | This one's different. An Ushka, maybe? It's got\n |
| 0x10df4e | 41 | a strong flavor, but a smooth aftertaste. |
| 0x10df78 | 45 | Yes, that is something we imported from our\n |
| 0x10dfa6 | 47 | homeland. I thought it would go well with the\n |
| 0x10dfd6 | 5 | food. |
| 0x10dfdc | 15 | Oh, definitely. |
| 0x10dfec | 44 | It is from a seller we often go to, but it\n |
| 0x10e019 | 42 | seems much rarer these days. Perhaps its\n |
| 0x10e044 | 23 | popularity is waning... |
| 0x10e05c | 46 | I am quite proud of myself for being able to\n |
| 0x10e08b | 17 | find some at all. |
| 0x10e09d | 42 | She fills my cup as she tells me all this. |
| 0x10e0c8 | 46 | This really is paradise... I guess sometimes\n |
| 0x10e0f7 | 46 | what you want most is right in front of you.\n |
| 0x10e126 | 22 | Or above you, I guess? |
| 0x10e13d | 46 | I slip into a nice buzz, feeling my thoughts\n |
| 0x10e16c | 28 | beginning to slow and relax. |
| 0x10e189 | 45 | This mead... I remember the taste. It's the\n |
| 0x10e1b7 | 47 | same one I drank behind your backs when I was\n |
| 0x10e1e7 | 7 | little. |
| 0x10e1ef | 45 | I've been looking for this for a while now,\n |
| 0x10e21d | 41 | but I could never find it... This is so\n |
| 0x10e247 | 12 | nostalgic... |
| 0x10e254 | 43 | Of course you wouldn't find it. This is a\n |
| 0x10e280 | 45 | particularly special one... It was homemade\n |
| 0x10e2ae | 7 | by her. |
| 0x10e2b6 | 18 | Then... this is... |
| 0x10e2c9 | 44 | I saved it for this very day. Make sure to\n |
| 0x10e2f6 | 21 | savor the taste, now. |
| 0x10e30c | 10 | ...I will. |
| 0x10e317 | 31 | Touka watches Kuon for a while. |
| 0x10e337 | 48 | Pensive and quiet, she seems for a moment like\n |
| 0x10e368 | 48 | she's about to cry, but she takes a long drink\n |
| 0x10e399 | 8 | instead. |
| 0x10e3a2 | 19 | *Gulp, gulp, gulp.* |
| 0x10e3b6 | 32 | You sure you don't want seconds? |
| 0x10e3d7 | 35 | ...I will have some, if you please. |
| 0x10e3fb | 45 | I decide not to ask any questions, and pour\n |
| 0x10e429 | 25 | more liquor into her mug. |
| 0x10e443 | 12 | *Gulp, gulp* |
| 0x10e450 | 7 | Mother? |
| 0x10e458 | 47 | Why don't you leave her be for now? Sometimes\n |
| 0x10e488 | 47 | one simply wishes to lose themselves in liquor. |
| 0x10e4b8 | 10 | R-Right... |
| 0x10e4c3 | 46 | Have you tried any of these? This is made by\n |
| 0x10e4f2 | 48 | fermenting freshwater fish in a barrel of salt\n |
| 0x10e523 | 10 | for years. |
| 0x10e52e | 46 | It can be a bit strong, but I confess it has\n |
| 0x10e55d | 16 | me quite hooked. |
| 0x10e56e | 22 | I'll have some then... |
| 0x10e585 | 46 | Oh, heshuko! I loved this when I was little,\n |
| 0x10e5b4 | 44 | but they never allowed me to eat much of it. |
| 0x10e5e1 | 44 | I couldn't have you eating away at all the\n |
| 0x10e60e | 42 | snacks I intended to have on my drinking\n |
| 0x10e639 | 7 | nights. |
| 0x10e641 | 45 | Can you imagine the heartbreak when I found\n |
| 0x10e66f | 47 | the barrel I had preserved for years, emptied\n |
| 0x10e69f | 7 | by you? |
| 0x10e6a7 | 49 | A-Ahahaha... I do recall... something like that\n |
| 0x10e6d9 | 10 | happening? |
| 0x10e6e4 | 40 | Kuon seems to be feeling a little more\n |
| 0x10e70d | 16 | comfortable now. |
| 0x10e71e | 26 | By the way, Mothe--Sister. |
| 0x10e739 | 33 | And why all the sudden formality? |
| 0x10e75b | 49 | May I ask why you are running an inn in a place\n |
| 0x10e78d | 10 | like this? |
| 0x10e798 | 6 | ...Oh? |
| 0x10e79f | 44 | Was that really the question you wanted to\n |
| 0x10e7cc | 7 | ask me? |
| 0x10e7d4 | 5 | Er... |
| 0x10e7da | 44 | Kuon averts her eyes a little guiltily, as\n |
| 0x10e807 | 39 | Karulau fixes her gaze directly on her. |
| 0x10e82f | 18 | Well, let's see... |
| 0x10e842 | 49 | Karulau sets down her cup as she pauses, trying\n |
| 0x10e874 | 33 | to remember how everything began. |
| 0x10e896 | 45 | Kuon, what did you think when you first saw\n |
| 0x10e8c4 | 23 | this country of Yamato? |
| 0x10e8dc | 48 | Um... I hate to admit it, but it's much larger\n |
| 0x10e90d | 37 | and more developed than our homeland. |
| 0x10e933 | 43 | Although... That's not to say our land is\n |
| 0x10e95f | 11 | inferior... |
| 0x10e96b | 44 | Indeed, the technological advances of this\n |
| 0x10e998 | 30 | country were quite astounding. |
| 0x10e9b7 | 44 | Their culture, technology, average wealth,\n |
| 0x10e9e4 | 45 | roadways, irrigation... and, of course, the\n |
| 0x10ea12 | 30 | peaceful rule of their Mikado. |
| 0x10ea31 | 42 | Yes, I do agree that there are many good\n |
| 0x10ea5c | 28 | points about this country... |
| 0x10ea79 | 46 | Kuon answers promptly, as though called upon\n |
| 0x10eaa8 | 15 | in a classroom. |
| 0x10eab8 | 45 | After we saw this, we decided to change our\n |
| 0x10eae6 | 47 | plans for a brief visit... and instead reside\n |
| 0x10eb16 | 20 | here a while longer. |
| 0x10eb2b | 42 | You see, we wished to learn more of this\n |
| 0x10eb56 | 8 | country. |
| 0x10eb5f | 47 | Are you saying that you prefer living here to\n |
| 0x10eb8f | 12 | our home...? |
| 0x10eb9c | 46 | Hmhm... You know, I find it's better to wait\n |
| 0x10ebcb | 47 | until one finishes talking before responding,\n |
| 0x10ebfb | 5 | dear. |
| 0x10ec01 | 43 | ...So, as we grew accustomed to our lives\n |
| 0x10ec2d | 45 | here, we began to understand the full scale\n |
| 0x10ec5b | 10 | of Yamato. |
| 0x10ec66 | 31 | ...As well as its shortcomings. |
| 0x10ec86 | 13 | Shortcomings? |
| 0x10ec94 | 33 | Yes. And the most egregious one\n |
| 0x10ecb6 | 24 | of all... was its baths. |
| 0x10eccf | 7 | ...Huh? |
| 0x10ecd7 | 3 | Oh! |
| 0x10ecdb | 43 | It seems this country's custom is to take\n |
| 0x10ed07 | 46 | steam baths. There are few places to immerse\n |
| 0x10ed36 | 19 | oneself in a tub... |
| 0x10ed4a | 48 | Some inns out there have water baths, but they\n |
| 0x10ed7b | 46 | are few and far between... and expensive, at\n |
| 0x10edaa | 5 | that. |
| 0x10edb0 | 17 | Yes, that's true! |
| 0x10edc2 | 45 | I thought I was misunderstanding this whole\n |
| 0x10edf0 | 39 | conversation, but Kuon nods in fierce\n |
| 0x10ee18 | 10 | agreement. |
| 0x10ee23 | 47 | I heard steam baths are common in this region\n |
| 0x10ee53 | 45 | because of past water shortages. A relic of\n |
| 0x10ee81 | 11 | its past... |
| 0x10ee8d | 48 | You could just call it cultural differences...\n |
| 0x10eebe | 49 | but I never imagined I would miss water bathing\n |
| 0x10eef0 | 8 | so much. |
| 0x10eef9 | 23 | I see, so that's why... |
| 0x10ef11 | 42 | Yes. Thus the Hakurokaku Inn came to be.\n |
| 0x10ef3c | 46 | I couldn't stand it anymore, so I decided to\n |
| 0x10ef6b | 23 | fix the problem myself. |
| 0x10ef83 | 45 | Thanks to that, I can now enjoy a nice bath\n |
| 0x10efb1 | 30 | in hot water every single day. |
| 0x10efd0 | 39 | Amazing... That certainly is the mo--\n |
| 0x10eff8 | 18 | the sister I know. |
| 0x10f00b | 49 | ...Wait, wait, wait. That conversation just now\n |
| 0x10f03d | 19 | made sense to you!? |
| 0x10f051 | 47 | Oh? Were my baths not to your liking? I pride\n |
| 0x10f081 | 43 | myself on having the best in the imperial\n |
| 0x10f0ad | 8 | capital. |
| 0x10f0b6 | 47 | Look, I kind of see where you're coming from... |
| 0x10f0e6 | 46 | But would anyone really go to the trouble of\n |
| 0x10f115 | 44 | building an inn just so they can bathe the\n |
| 0x10f142 | 17 | way they want...? |
| 0x10f154 | 36 | That said, it wasn't easy, you know? |
| 0x10f179 | 45 | Karulau swirls the liquid in her cup as she\n |
| 0x10f1a7 | 39 | stares off into the distance wistfully. |
| 0x10f1cf | 49 | Water baths require a plentiful water source...\n |
| 0x10f201 | 41 | but it seems the imperial capital lacks\n |
| 0x10f22b | 9 | aquifers. |
| 0x10f235 | 44 | And using water from the irrigation system\n |
| 0x10f262 | 27 | would cost a small fortune. |
| 0x10f27e | 46 | Oh, right. Water is usually free, but if you\n |
| 0x10f2ad | 42 | use it for business, it's pretty heavily\n |
| 0x10f2d8 | 8 | taxed... |
| 0x10f2e1 | 43 | Hm, guess that's why steam baths are more\n |
| 0x10f30d | 24 | common in these areas... |
| 0x10f326 | 41 | Yes. It's quite well thought out, really. |
| 0x10f350 | 44 | With little option, we looked for a nearby\n |
| 0x10f37d | 40 | water source, and asked a friend to...\n |
| 0x10f3a6 | 16 | nudge it closer. |
| 0x10f3b7 | 44 | Oh, you are one to talk of its difficulty.\n |
| 0x10f3e4 | 39 | It was I who had done most of the work. |
| 0x10f40c | 48 | I was the one who brought Ul--ahem. "Her" here\n |
| 0x10f43d | 44 | in the first place. You did nothing at all\n |
| 0x10f46a | 14 | then, Karulau. |
| 0x10f479 | 43 | Wait... you don't mean you brought Mother\n |
| 0x10f4a5 | 43 | Ulthury all the way here just to move the\n |
| 0x10f4d1 | 13 | water source? |
| 0x10f4df | 42 | Karulau avoids the question as she takes\n |
| 0x10f50a | 25 | another sip from her cup. |
| 0x10f524 | 49 | But... But if she was brought here.. that means\n |
| 0x10f556 | 43 | the Oruyankuru came all the way here just\n |
| 0x10f582 | 6 | for... |
| 0x10f589 | 46 | Oh, it wasn't that bad. I wished to give her\n |
| 0x10f5b8 | 47 | a little vacation. She had been all cooped up\n |
| 0x10f5e8 | 10 | with work. |
| 0x10f5f3 | 48 | If your intentions were so kind, I suggest you\n |
| 0x10f624 | 39 | actually tell her beforehand next time. |
| 0x10f64c | 40 | I thought you told her of your plight!\n |
| 0x10f675 | 45 | Can you imagine my panic, realizing we were\n |
| 0x10f6a3 | 28 | spiriting her away unawares? |
| 0x10f6c0 | 44 | Oh, I had no choice! That was the only way\n |
| 0x10f6ed | 43 | that girl would ever get to sneak out and\n |
| 0x10f719 | 22 | enjoy some nice baths. |
| 0x10f730 | 48 | Then that time she was reported as missing for\n |
| 0x10f761 | 23 | a while... Was that...? |
| 0x10f779 | 44 | The whole place was in an uproar when that\n |
| 0x10f7a6 | 21 | happened, you know... |
| 0x10f7bc | 45 | My deepest apologies. Oh, such carelessness\n |
| 0x10f7ea | 17 | is inexcusable... |
| 0x10f7fc | 49 | However, I did send back a message immediately.\n |
| 0x10f82e | 44 | I am sure all the panic subsided after that. |
| 0x10f85b | 29 | I didn't hear a word of it.\n |
| 0x10f879 | 19 | I was so worried... |
| 0x10f88d | 49 | It isn't something easily explained to a child,\n |
| 0x10f8bf | 48 | I suppose. That's probably why they never told\n |
| 0x10f8f0 | 4 | you. |
| 0x10f8f5 | 42 | Well... I suppose it couldn't be helped... |
| 0x10f920 | 45 | Ahem. There were those ruffians that forced\n |
| 0x10f94e | 47 | their way in and demanded a "protection" fee.\n |
| 0x10f97e | 17 | Very troublesome. |
| 0x10f990 | 42 | Oh, but I did offer to take care of them\n |
| 0x10f9bb | 45 | myself. Tell me, who was the one who locked\n |
| 0x10f9e9 | 11 | me up then? |
| 0x10f9f5 | 45 | How could I not? Those scoundrels destroyed\n |
| 0x10fa23 | 44 | your baths. You would have had their blood\n |
| 0x10fa50 | 20 | rain from the skies! |
| 0x10fa65 | 46 | All my efforts to settle matters quietly and\n |
| 0x10fa94 | 34 | discreetly would have been ruined. |
| 0x10fab7 | 49 | Quite the accusation. I only intended on giving\n |
| 0x10fae9 | 28 | them a little... talking-to. |
| 0x10fb06 | 43 | So you settled it quietly and discreetly,\n |
| 0x10fb32 | 15 | did you now...? |
| 0x10fb42 | 47 | Ngh... If you would say something, then say it. |
| 0x10fb72 | 43 | Kuon, do you know what happened after that? |
| 0x10fb9e | 40 | If I recall, I believe I heard someone\n |
| 0x10fbc7 | 44 | spending the rest of the night fleeing the\n |
| 0x10fbf4 | 15 | authorities...? |
| 0x10fc04 | 45 | W-Wait! Nevermind! Kuon, do not listen to a\n |
| 0x10fc32 | 36 | word Karulau says. It was nothing!\n |
| 0x10fc57 | 17 | Nothing happened. |
| 0x10fc69 | 49 | A-Ahahaha... I guess neither of you have really\n |
| 0x10fc9b | 8 | changed. |
| 0x10fca4 | 48 | I don't really get what they're talking about,\n |
| 0x10fcd5 | 34 | but I guess I shouldn't interrupt. |
| 0x10fcf8 | 43 | I wonder what the relationship is between\n |
| 0x10fd24 | 10 | these two. |
| 0x10fd2f | 45 | An innkeeper and a worker... but they don't\n |
| 0x10fd5d | 44 | feel like a boss and an employee, nor just\n |
| 0x10fd8a | 8 | friends. |
| 0x10fd93 | 24 | How should I put this... |
| 0x10fdac | 45 | So... Mother, why are you just a worker here? |
| 0x10fdda | 48 | Kuon asks, just as the same question enters my\n |
| 0x10fe0b | 5 | mind. |
| 0x10fe11 | 10 | That is... |
| 0x10fe1c | 45 | I would've thought that you would prefer to\n |
| 0x10fe4a | 41 | take a job more like... a bodyguard, or\n |
| 0x10fe74 | 9 | somesuch. |
| 0x10fe7e | 51 | Ahem, that is, if I am to give a proper answer...\n |
| 0x10feb2 | 47 | I would say it is training to become a better\n |
| 0x10fee2 | 6 | woman. |
| 0x10fee9 | 3 | Oh? |
| 0x10feed | 46 | ...I did work as a bodyguard here, for a time. |
| 0x10ff1c | 46 | However, the imperial capital is mostly free\n |
| 0x10ff4b | 40 | of crime, and few would antagonize the\n |
| 0x10ff74 | 15 | Hakurokaku Inn. |
| 0x10ff84 | 43 | The peace continued, and I had no further\n |
| 0x10ffb0 | 47 | duties. All I could do was wait for something\n |
| 0x10ffe0 | 10 | to happen. |
| 0x10ffeb | 40 | Those ruffians must have had quite the\n |
| 0x110014 | 43 | terrifying experience. Poor things, indeed. |
| 0x110040 | 28 | Nngh... You are one to talk. |
| 0x11005d | 5 | Hmhm. |
| 0x110063 | 47 | So... it was rather hard for me to sit around\n |
| 0x110093 | 44 | and do nothing whilst those around me were\n |
| 0x1100c0 | 13 | hard at work. |
| 0x1100ce | 7 | ...How? |
| 0x1100d6 | 3 | Hm? |
| 0x1100da | 16 | Oh, uh, nothing. |
| 0x1100eb | 48 | Why would it be hard to just sit around and do\n |
| 0x11011c | 19 | nothing all day...? |
| 0x110130 | 7 | Haku... |
| 0x110138 | 42 | What? Why are you looking at me like that? |
| 0x110163 | 38 | One day, I could stand it no longer.\n |
| 0x11018a | 48 | I decided to work in this manner until my true\n |
| 0x1101bb | 23 | skills would be needed. |
| 0x1101d3 | 46 | If you'd ask me, I would have preferred that\n |
| 0x110202 | 28 | you stay put and keep quiet. |
| 0x11021f | 45 | What are you saying? Those that do not work\n |
| 0x11024d | 48 | do not deserve to eat. Do you not remember our\n |
| 0x11027e | 13 | lord's words? |
| 0x11028c | 47 | I suppose you're right. He was fond of saying\n |
| 0x1102bc | 18 | that, wasn't he... |
| 0x1102cf | 48 | Karulau smiles despite herself, as if dwelling\n |
| 0x110300 | 23 | on some distant memory. |
| 0x110318 | 49 | Those that do not work do not deserve to eat...\n |
| 0x11034a | 34 | Ugh. What a horrible thing to say. |
| 0x11036d | 48 | I dunno if I'd ever get along with this "Lord"\n |
| 0x11039e | 12 | of theirs... |
| 0x1103ab | 42 | Just as I pour another drink, a new dish\n |
| 0x1103d6 | 43 | arrives as if it had been waiting for the\n |
| 0x110402 | 15 | perfect moment. |
| 0x110412 | 42 | The food piled on top of the plate looks\n |
| 0x11043d | 23 | vaguely familiar to me. |
| 0x110455 | 29 | Oh... Mororo! And so many...! |
| 0x110473 | 44 | Kuon's eyes glimmer with excitement at the\n |
| 0x1104a0 | 45 | I thought you might be missing them by now,\n |
| 0x1104ce | 32 | so I obtained some just for you. |
| 0x1104ef | 44 | We wished you to have them, Kuon. They are\n |
| 0x11051c | 45 | quite rare in this land... I am sure it has\n |
| 0x11054a | 13 | been a while. |
| 0x110558 | 12 | Yes, it has! |
| 0x110565 | 46 | Kuon answers distractedly, taking one of the\n |
| 0x110594 | 34 | mororo and biting eagerly into it. |
| 0x1105b7 | 21 | *Munch, munch, munch* |
| 0x1105cd | 15 | Mmmmm, s' good! |
| 0x1105dd | 44 | I also made those pickles that you like so\n |
| 0x11060a | 39 | much. They should be perfect about now. |
| 0x110632 | 37 | Wow! Thank you! *Munch, munch, munch* |
| 0x110658 | 45 | I recalled you liking these meatballs, too.\n |
| 0x110686 | 34 | I do hope they are to your liking. |
| 0x1106a9 | 25 | Homf--*munch, munch*...\n |
| 0x1106c3 | 17 | Mmmmm, delicious! |
| 0x1106d5 | 35 | Wait... did you make these, Sister? |
| 0x1106f9 | 47 | I can cook well enough to make these, at least. |
| 0x110729 | 50 | Never thought I'd see Kuon treated like a child.\n |
| 0x11075c | 44 | But I guess to those two... she still is a\n |
| 0x110789 | 6 | child. |
| 0x110790 | 42 | It's a little embarrassing to watch them\n |
| 0x1107bb | 21 | pamper her like that. |
| 0x1107d1 | 37 | C'mon, Haku, you should try some too. |
| 0x1107f7 | 33 | Oh, yeah. I think I will, then... |
| 0x110819 | 44 | Guess food from her homeland has a special\n |
| 0x110846 | 48 | significance to her. She's in such a good mood\n |
| 0x110877 | 6 | now... |
| 0x11087e | 45 | You can put other food on top of the mororo\n |
| 0x1108ac | 47 | and eat it, or you can pour some of the sauce\n |
| 0x1108dc | 7 | on too! |
| 0x1108e4 | 48 | The classy little party we were having quickly\n |
| 0x110915 | 48 | turned into a sight I see at dinner every night. |
| 0x110946 | 42 | Oh well. I guess this is fun all the same. |
| 0x110971 | 41 | ...This is even kind of nostalgic for me. |
| 0x11099b | 48 | If I remember correctly, the first night after\n |
| 0x1109cc | 36 | I met Kuon... was kind of like this. |
| 0x1109f1 | 45 | I've come a long way since then... but this\n |
| 0x110a1f | 26 | feeling is still the same. |
| 0x110a3a | 44 | Hmhm, I see your appetite has not changed.\n |
| 0x110a67 | 46 | It brings a smile to my face, seeing you eat\n |
| 0x110a96 | 12 | like you do. |
| 0x110aa3 | 43 | I agree with you there. It makes all that\n |
| 0x110acf | 43 | effort to prepare the food feel worthwhile. |
| 0x110afb | 45 | Something about their calm gazes on Kuon...\n |
| 0x110b29 | 46 | It's like their eyes alone are brimming with\n |
| 0x110b58 | 9 | kindness. |
| 0x110b62 | 47 | No need to hold back now. You may eat all you\n |
| 0x110b92 | 5 | want. |
| 0x110b98 | 46 | Yes, we have plenty more where that came from. |
| 0x110bc7 | 36 | Mnf--*munch, munch, munch, munch*... |
| 0x110bec | 43 | Kuon continues to eat as she is told, her\n |
| 0x110c18 | 39 | expression childlike and full of bliss. |
| 0x110c40 | 38 | And beside her, the two women watch... |
| 0x110c67 | 47 | With eyes like those of proud mothers, fondly\n |
| 0x110c97 | 30 | looking upon their dear child. |

## 8. Formato de saida EXIGIDO
Escreva `translations_17_01.json` com a forma:
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
