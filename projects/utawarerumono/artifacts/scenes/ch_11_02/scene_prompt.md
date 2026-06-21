# Cena ch_11_02 — pacote de traducao (557 linhas)

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
| aperyu | Item | aperyu | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Shishiri | Local | Shishiri | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Utawarerumono | Título | Utawarerumono | manter_original | none |

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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Upon returning to the tent, the girl starts\n` -> `Ao voltarmos para a tenda, a garota começa\n` (Kuon, root)
- `digging through her bags.` -> `a remexer nas bolsas dela.` (Kuon, root)
- `Girl` -> `Garota` (sistema, 11_01)
- `Hmm, I'm sure I put it somewhere back here...` -> `Hmm, tenho certeza de que guardei em algum lugar aqui...` (Kuon, root)
- `Aha! There we go.` -> `Aha! Achei.` (Kuon, root)
- `I was wondering what to do with these...\n` -> `Eu estava sem saber o que fazer com isto...\n` (Kuon, root)
- `I certainly didn't think they'd come in handy\n` -> `Realmente não imaginei que fosse ser útil\n` (Kuon, root)
- `like this.` -> `dessas.` (Kuon, 11_01)
- `With those words, the girl holds out some\n` -> `Com essas palavras, a garota estende uns\n` (Kuon, root)
- `folded fabrics.` -> `tecidos dobrados.` (Kuon, root)
- `Here, a change of clothes. If you keep walking\n` -> `Aqui, uma muda de roupa. Se continuar andando\n` (Kuon, root)
- `around like that, you'll catch a cold.` -> `por aí desse jeito, vai pegar um resfriado.` (Kuon, root)
- `Hm...?` -> `Hum...?` (Kuon, 13_02)
- `They definitely seem sturdier than the clothes\n` -> `Parecem bem mais resistentes que as roupas\n` (Kuon, root)
- `I had on, but...` -> `que eu tinha, mas...` (Kuon, root)
- `Ahaha, don't make that face! They're men's\n` -> `Ahaha, não faz essa cara! São roupas\n` (Kuon, root)
- `clothes.` -> `masculinas.` (Kuon, root)
- `O-Oh...` -> `A-Ah...` (Kuon, root)
- `Well, I'm going to go draw some water.` -> `Bem, vou buscar um pouco de água.` (Kuon, root)
- `Oh, she's trying to give me some privacy.\n` -> `Ah, ela está tentando me dar privacidade.\n` (Kuon, root)
- `That's kind of her.` -> `Que gentileza dela.` (Kuon, root)
- `Yikes--` -> `Eita--` (Kuon, root)
- `A burst of cold air streams in as the girl\n` -> `Uma rajada de ar gelado entra quando a garota\n` (Kuon, root)
- `makes her exit.` -> `sai.` (Kuon, root)
- `G-God, that's cold... OK, if I stay in this\n` -> `C-Caramba, que frio... Tá, se eu ficar nessa\n` (Kuon, root)
- `any longer, I'm gonna come down with something...` -> `por mais tempo, vou acabar pegando alguma coisa...` (Kuon, root)
- `I spread out the clothes she gave me.` -> `Estendo as roupas que ela me deu.` (Kuon, root)
- `But... something's missing. One crucial,\n` -> `Mas... está faltando algo. Uma coisa crucial,\n` (Kuon, root)
- `important thing. I stare uncertainly,\n` -> `importante. Encaro, incerto,\n` (Kuon, root)
- `head tilted.` -> `a cabeça inclinada.` (Kuon, root)
- `...Where's the underwear...?` -> `...Cadê a roupa de baixo...?` (Kuon, root)
- `I turn the clothes inside out, right-side out,\n` -> `Viro as roupas do avesso, do lado certo,\n` (Kuon, root)
- `even shake them around... but no underpants.` -> `até sacudo elas... mas nada de cueca.` (Kuon, root)
- `Figures. She wouldn't miraculously just happen\n` -> `Lógico. Ela não teria milagrosamente uma\n` (Kuon, root)
- `to have spare men's underwear around the place...  ` -> `cueca masculina sobrando por aí...  ` (Kuon, root)
- `Which means... I have no choice...` -> `O que significa... que não tenho escolha...` (Kuon, root)
- `Because I have no choice, because I am a slave\n` -> `Como não tenho escolha, como sou um escravo\n` (Kuon, root)
- `to the whims of fate, I'll have to go commando.` -> `dos caprichos do destino, vou ter que ir sem nada.` (Kuon, root)
- `I-It's not like this is something I WANT to do! ` -> `N-Não é como se isto fosse algo que eu QUEIRA fazer! ` (Kuon, root)
- `Primitive man was naked to start with, so don't\n` -> `O homem primitivo já começou pelado, então não\n` (Kuon, root)
- `freak out. It'll just be more... brisk than usual.` -> `surte. Vai ser só mais... arejado que o normal.` (Kuon, root)
- `Trying to reassure myself, I start putting\n` -> `Tentando me tranquilizar, começo a vestir\n` (Kuon, root)
- `on the clothes provided. But...` -> `as roupas que ela deu. Mas...` (Kuon, root)
- `OK, let's see these pants... There's a hole\n` -> `Tá, vamos ver essa calça... Tem um buraco\n` (Kuon, root)
- `here, so this must be the front...?` -> `aqui, então isto deve ser a frente...?` (Kuon, root)
- `*Shuffle*...` -> `*Vish*...` (Kuon, root)
- `Ho-kay... Hm. Doesn't feel all that comfortable...` -> `Bele... Hm. Não parece nada confortável...` (Kuon, root)
- `Ah, whatever. Next, I get this top on...\n` -> `Ah, tanto faz. Agora visto essa parte de cima...\n` (Kuon, root)
- `and I just tie it off with this sash?` -> `e amarro com esta faixa?` (Kuon, root)
- `*Swoosh*` -> `*Vum*` (Kuon, root)
- `There we go...` -> `Pronto...` (Kuon, root)
- `Honestly, though, this thing's pretty\n` -> `Sinceramente, essa coisa é bem\n` (Kuon, root)
- `uncomfortable...` -> `desconfortável...` (Kuon, root)
- `The top's a little off, but the bottom just\n` -> `A parte de cima está meio torta, mas a de baixo\n` (Kuon, root)
- `has way too many things wrong with it.` -> `tem coisa errada demais.` (Kuon, root)
- `The way it's stretching can't be good for it,\n` -> `O jeito que está esticando não pode ser bom,\n` (Kuon, root)
- `and it's... getting a little drafty downstairs.` -> `e está... ficando meio arejado lá embaixo.` (Kuon, root)
- `Since the fly opens so wide, it's pretty\n` -> `Como a braguilha abre tão larga, está bem\n` (Kuon, root)
- `well-ventilated. Well, more like it's letting\n` -> `ventilado. Bem, mais como se deixasse\n` (Kuon, root)
- `the wind right in.` -> `o vento entrar direto.` (Kuon, root)
- `The real problem here is how I'm going to make\n` -> `O verdadeiro problema é como vou fazer\n` (Kuon, root)
- `sure I don't accidentally flash anyone...` -> `pra não mostrar tudo pra alguém sem querer...` (Kuon, root)
- `There are some serious issues with these clothes.\n` -> `Tem problemas sérios com estas roupas.\n` (Kuon, root)
- `I'm a gust of wind away from becoming a streaker.` -> `Estou a uma rajada de virar um exibicionista.` (Kuon, root)
- `Something tells me this isn't going to work.` -> `Algo me diz que isto não vai dar certo.` (Kuon, root)
- `Maybe I should just explain and ask to borrow\n` -> `Talvez eu deva só explicar e pedir uma\n` (Kuon, root)
- `some underwear...? No, no, can't do that.` -> `cueca emprestada...? Não, não, não dá.` (Kuon, root)
- `Even if it's a perfectly innocent and honest\n` -> `Mesmo sendo um pedido perfeitamente inocente e\n` (Kuon, root)
- `request, a guy can't ask a girl for underpants.` -> `honesto, um cara não pode pedir cueca pra uma garota.` (Kuon, root)
- `And she's lending these out of the kindness of\n` -> `E ela está emprestando isto por pura\n` (Kuon, root)
- `her heart! I can't go begging for more.` -> `bondade! Não posso ficar implorando por mais.` (Kuon, root)
- `I don't need to bother her with this.\n` -> `Não preciso incomodá-la com isto.\n` (Kuon, root)
- `Just gotta get a little creative.` -> `Só preciso de um pouco de criatividade.` (Kuon, root)
- `Having settled on a course of action, I fumble\n` -> `Decidido o plano, fico mexendo\n` (Kuon, root)
- `with the fabric for a little longer.` -> `no tecido mais um tempo.` (Kuon, root)
- `Oh, got it. I can use this heavier fabric as\n` -> `Ah, achei. Posso usar este tecido mais grosso como\n` (Kuon, root)
- `a kind of apron, and now this can be... Hm?` -> `uma espécie de avental, e agora isto pode ser... Hm?` (Kuon, root)
- `...uh...` -> `...Ãh...` (Kuon, 19_08)
- `I feel eyes on me, and glance up. She's standing\n` -> `Sinto olhos em mim e ergo a vista. Ela está\n` (Kuon, root)
- `there, staring... amazed, concerned, and\n` -> `ali, encarando... espantada, preocupada e\n` (Kuon, root)
- `exasperated.` -> `exasperada.` (Kuon, root)
- `You aren't... messing around, are you?` -> `Você não está... de brincadeira, está?` (Kuon, root)
- `I see something in her expression twitch\n` -> `Vejo algo na expressão dela estremecer\n` (Kuon, root)
- `as she awaits my response.` -> `enquanto ela aguarda minha resposta.` (Kuon, root)
- `Urgh... that look in her eyes... It's like\n` -> `Argh... aquele olhar dela... É como\n` (Kuon, root)
- `a parent saying "I'm not mad, just\n` -> `um pai dizendo "não estou bravo, só\n` (Kuon, root)
- `disappointed in you."` -> `decepcionado com você".` (Kuon, root)
- `N-No, look, I can explain! I'm only dressed\n` -> `N-Não, olha, eu explico! Só estou vestido\n` (Kuon, root)
- `like this 'cause there wasn't any underwear!` -> `assim porque não tinha nenhuma roupa de baixo!` (Kuon, root)
- `...The thing you have wrapped around your\n` -> `...A coisa que você enrolou na\n` (Kuon, root)
- `waist right now is an aperyu. It goes on\n` -> `cintura agora é um aperyu. Vai\n` (Kuon, root)
- `your shoulders.` -> `nos ombros.` (Kuon, root)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `You've got everything on the wrong sides for\n` -> `Você pôs tudo no lado errado para\n` (Kuon, root)
- `the top, too... and I think the pants are on\n` -> `a parte de cima, também... e acho que a calça está\n` (Kuon, root)
- `backwards.` -> `do avesso.` (Kuon, root)
- `Backwards...? Hold on, the fly's here.\n` -> `Do avesso...? Espera, a braguilha está aqui.\n` (Kuon, root)
- `So that makes it the front, right?` -> `Então isto é a frente, né?` (Kuon, root)
- `That's where the tail's supposed to run\n` -> `É por aí que a cauda deveria\n` (Kuon, root)
- `through...` -> `passar...` (Kuon, root)
- `Huh...? Tail...?` -> `Hã...? Cauda...?` (Kuon, root)
- `I'm caught off guard. A tail's not exactly\n` -> `Sou pego de surpresa. Cauda não é exatamente\n` (Kuon, root)
- `something you expect to come up in normal\n` -> `algo que se espera ouvir numa conversa\n` (Kuon, root)
- `conversation.` -> `normal.` (Kuon, 14_04)
- `I glance over, and notice something swaying\n` -> `Dou uma olhada e noto algo balançando\n` (Kuon, root)
- `behind her.` -> `atrás dela.` (Kuon, root)
- `Something ropelike, extending from just above\n` -> `Algo como uma corda, saindo logo acima\n` (Kuon, root)
- `her rear. Something covered in fur, almost\n` -> `do traseiro dela. Algo coberto de pelo, quase\n` (Kuon, root)
- `like...` -> `como...` (Kuon, 18_01)
- `...a tail?` -> `...uma cauda?` (Kuon, root)
- `Come to think of it, I think I saw it behind\n` -> `Pensando bem, acho que vi isto atrás\n` (Kuon, root)
- `her while we were running in the caves...` -> `dela enquanto corríamos nas cavernas...` (Kuon, root)
- `But I dismissed the thought, of course.\n` -> `Mas descartei a ideia, é claro.\n` (Kuon, root)
- `Common sense says that's ridiculous.` -> `O bom senso diz que isso é ridículo.` (Kuon, root)
- `No, no, no. There's just no way. It must be\n` -> `Não, não, não. Não tem como. Deve ser\n` (Kuon, root)
- `some kind of accessory or something...` -> `algum tipo de acessório ou coisa assim...` (Kuon, root)
- `As I ponder the possibilities, I reach out\n` -> `Enquanto pondero as possibilidades, estendo\n` (Kuon, root)
- `and grasp the swaying tail.` -> `a mão e agarro a cauda que balança.` (Kuon, root)
- `H-Hgh!` -> `Hngh!` (Kuon, root)
- `Wow, this is really something. It looks and\n` -> `Nossa, isto é impressionante. Parece e\n` (Kuon, root)
- `feels like it's an actual tail...` -> `tem o toque de uma cauda de verdade...` (Kuon, root)
- `And this texture! It's even soft to the touch.` -> `E essa textura! É até macia ao toque.` (Kuon, root)
- `H-Haah! Ah... Wh... Wha...` -> `H-Hã! Ah... Q... Quê...` (Kuon, root)
- `Fluffy, soft, and silky smooth. It feels\n` -> `Fofa, macia e sedosa. É uma sensação\n` (Kuon, root)
- `amazing... It'd make a perfect scarf.` -> `incrível... Daria um cachecol perfeito.` (Kuon, root)
- `And it's even wriggling, but I can't work\n` -> `E até se contorce, mas não consigo\n` (Kuon, root)
- `out if there's some mechanism moving it...` -> `descobrir se há algum mecanismo movendo isto...` (Kuon, root)
- `*Floof*` -> `*Pluf*` (Kuon, root)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Ngh... Ghh... Hngh!` -> `Nnh... Argh... Hngh!` (Kuon, root)
- `What's this? It's even getting all fluffed\n` -> `O que é isto? Está até ficando todo arrepiado\n` (Kuon, root)
- `up now...` -> `agora...` (Kuon, root)
- `As I run my hands over the soft fur, it\n` -> `Enquanto passo as mãos pelo pelo macio, ele\n` (Kuon, root)
- `suddenly puffs up, like its hairs are\n` -> `de repente se infla, como se os pelos\n` (Kuon, root)
- `standing on end.` -> `ficassem em pé.` (Kuon, root)
- `The heck...?` -> `Mas que...?` (Kuon, root)
- `Curiosity getting the better of me, I grab it\n` -> `A curiosidade falando mais alto, agarro com\n` (Kuon, root)
- `with both hands. And at that moment...` -> `as duas mãos. E nesse momento...` (Kuon, root)
- `Ah...!` -> `Ah...!` (Man, 11_01)
- `...Waaaaaaaaaah!` -> `...Aaaaaah!` (Kuon, root)
- `...Gah! Wh-What the--` -> `...Gah! Q-Que diabos--` (Kuon, root)
- `Her outburst surprises me, and I instinctively\n` -> `O grito dela me assusta, e instintivamente\n` (Kuon, root)
- `let go of the tail.` -> `solto a cauda.` (Kuon, root)
- `I look back to her, uncertain of what just\n` -> `Olho de volta pra ela, sem saber o que\n` (Kuon, root)
- `happened.` -> `acabou de acontecer.` (Kuon, 16_01)
- `As I meet her eyes, I see her shoulders\n` -> `Quando encontro o olhar dela, vejo os ombros\n` (Kuon, root)
- `trembling... and she's glaring at me?` -> `tremendo... e ela está me encarando furiosa?` (Kuon, root)
- `H-Hey, what's wrong...?` -> `E-Ei, o que foi...?` (Kuon, root)
- `What's... wrong...?` -> `O que... foi...?` (Kuon, root)
- `Staring icily, the girl steps towards me.` -> `Encarando friamente, a garota dá um passo na minha direção.` (Kuon, root)
- `What... do you think you're doing?` -> `O que... você pensa que está fazendo?` (Kuon, root)
- `What do I... what?` -> `O que eu... quê?` (Kuon, root)
- `You heard me!` -> `Você ouviu!` (Kuon, root)
- `What are you doing, grabbing a girl's tail like\n` -> `O que você está fazendo, agarrando a cauda de uma\n` (Kuon, root)
- `that? I was quite clear, I think!` -> `garota assim? Acho que fui bem clara!` (Kuon, root)
- `Grabbing a...? No, that was only...` -> `Agarrando uma...? Não, aquilo foi só...` (Kuon, root)
- `Wait, you don't mean that's... that's real?` -> `Espera, você não quer dizer que isso é... é de verdade?` (Kuon, root)
- `Of course it is! If this beautiful tail of mine\n` -> `Claro que é! Se esta minha linda cauda\n` (Kuon, root)
- `isn't real, then what is?` -> `não é de verdade, então o que é?` (Kuon, root)
- `N-No, it's just...` -> `N-Não, é só que...` (Kuon, root)
- `Urgh--` -> `Argh--` (Man, 11_01)
- `I stagger backwards, feeling a sense of power\n` -> `Cambaleio pra trás, sentindo uma força\n` (Kuon, root)
- `from her completely at odds with her cute\n` -> `vinda dela totalmente em desacordo com a aparência\n` (Kuon, root)
- `looks.` -> `fofa.` (Kuon, root)
- `She strokes her tail lovingly, as if she's\n` -> `Ela acaricia a cauda com carinho, como se\n` (Kuon, root)
- `trying to soothe the thing after my picking\n` -> `tentasse consolar a coisa depois de eu\n` (Kuon, root)
- `at it.` -> `mexer nela.` (Kuon, 18_01)
- `But even still, just grabbing my tail without\n` -> `Mas mesmo assim, agarrar minha cauda sem\n` (Kuon, root)
- `even a warning...` -> `nem um aviso...` (Kuon, root)
- `No... well, I mean... how do I put it...` -> `Não... bem, quer dizer... como eu explico...` (Kuon, root)
- `She lets out a deep sigh.` -> `Ela solta um suspiro fundo.` (Kuon, root)
- `...It looks like you honestly didn't know,\n` -> `...Parece que você honestamente não sabia,\n` (Kuon, root)
- `so I suppose it can't be helped. I'll let\n` -> `então acho que não tem jeito. Vou deixar\n` (Kuon, root)
- `it go for now.` -> `passar por enquanto.` (Kuon, root)
- `Well... sorry.` -> `Bem... desculpa.` (Kuon, root)
- `But it's not like you would expect anyone to\n` -> `Mas não é como se a gente esperasse alguém\n` (Kuon, root)
- `have a real tail.` -> `ter uma cauda de verdade.` (Kuon, root)
- `I mean, humans did evolve from apes, and I\n` -> `Quer dizer, os humanos evoluíram dos macacos, e\n` (Kuon, root)
- `guess there's been cases of reverse evolution...` -> `acho que houve casos de evolução reversa...` (Kuon, root)
- `The girl looks at me strangely, as if she wants\n` -> `A garota me olha estranho, como se quisesse\n` (Kuon, root)
- `to respond to my belated attempt at excuses.` -> `responder à minha tentativa atrasada de desculpa.` (Kuon, root)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `...Am I seeing things?` -> `...Será que estou vendo coisas?` (Kuon, root)
- `A beautiful face, elegant facial features,\n` -> `Um rosto lindo, traços elegantes,\n` (Kuon, root)
- `and shiny black hair. Yep. No problems here.` -> `e cabelo preto brilhante. É. Nada de errado aqui.` (Kuon, root)
- `She's definitely cute, but that's not really\n` -> `Ela é uma graça, sem dúvida, mas não é bem\n` (Kuon, root)
- `the issue right now. The problem is...` -> `essa a questão agora. O problema é...` (Kuon, root)
- `...I-I didn't notice in all the commotion,\n` -> `...E-Eu não tinha notado em meio à confusão,\n` (Kuon, root)
- `but... are those furry tufts on her head?` -> `mas... aquilo são tufos de pelo na cabeça dela?` (Kuon, root)
- `What's wrong now?` -> `O que foi agora?` (Kuon, root)
- `Those big ears... big, furry ears... twitch\n` -> `Aquelas orelhas grandes... grandes e peludas... se mexem\n` (Kuon, root)
- `for a moment.` -> `por um instante.` (Kuon, 14_03)
- `Oh... uh... well, that's... um.` -> `Ah... é... bem, isso é... hum.` (Kuon, root)
- `Ears and a tail... She looks human, but is she\n` -> `Orelhas e cauda... Ela parece humana, mas será\n` (Kuon, root)
- `something else?` -> `que é outra coisa?` (Kuon, root)
- `No, wait. I can't afford for her to leave me\n` -> `Não, espera. Não posso deixar ela me abandonar\n` (Kuon, root)
- `behind for asking too many dumb questions...` -> `por eu fazer perguntas idiotas demais...` (Kuon, root)
- `...It's nothing.` -> `...Não é nada.` (Haku, 12_08)
- `Best to just act like I didn't see anything.` -> `Melhor agir como se eu não tivesse visto nada.` (Kuon, root)
- `Uhh, I'm not too familiar with the customs and\n` -> `Ãh, é que eu não conheço muito bem os costumes\n` (Kuon, root)
- `etiquette around these parts, is the thing.` -> `e a etiqueta destas bandas, sabe.` (Kuon, root)
- `That's plain enough just from looking at you.\n` -> `Isso é bem evidente só de olhar pra você.\n` (Kuon, root)
- `What are you doing with these clothes...?` -> `O que você está fazendo com essas roupas...?` (Kuon, root)
- `The girl lets out a small sigh at my excuse.` -> `A garota solta um suspirinho diante da minha desculpa.` (Kuon, root)
- `Anyhow, we may as well get you properly dressed.` -> `De todo jeito, é melhor te vestir direito.` (Kuon, root)
- `Y-Yeah...` -> `É-É...` (Kuon, 19_08)
- `At her words, I hastily start working on\n` -> `Diante das palavras dela, me apresso a desfazer\n` (Kuon, root)
- `undoing the strings. Maybe I made the knots\n` -> `os nós. Talvez eu tenha apertado os nós\n` (Kuon, root)
- `too tight...` -> `demais...` (Kuon, root)
- `There... we go. Phew... That's one untied.\n` -> `Pronto... Ufa... Esse já desatou.\n` (Kuon, root)
- `Next, I'll... Ngh... This one's knotted\n` -> `Agora vou... Ngh... Este também está\n` (Kuon, root)
- `pretty tight too...` -> `bem apertado...` (Kuon, root)
- `As I fumble, the girl kneels, and patiently\n` -> `Enquanto me atrapalho, a garota se ajoelha e\n` (Kuon, root)
- `starts undoing the knots herself with\n` -> `começa a desatar os nós com\n` (Kuon, root)
- `easy deftness.` -> `destreza tranquila.` (Kuon, root)
- `Hold still.` -> `Fica quieto.` (Kuon, root)
- `A-All right. Thanks.` -> `T-Tá bom. Obrigado.` (Kuon, root)
- `*Swish*` -> `*Vuf*` (Kuon, root)
- `I never imagined you'd use this as a sash...` -> `Nunca imaginei que você usaria isto como faixa...` (Kuon, root)
- `She murmurs with an odd wryness, setting her\n` -> `Ela murmura com uma ironia esquisita, voltando a\n` (Kuon, root)
- `attentions on the sash holding up my pants.` -> `atenção pra faixa que segura minha calça.` (Kuon, root)
- `Really? Well, it's long and narrow, so I just\n` -> `Sério? Bem, é comprido e estreito, então eu só\n` (Kuon, root)
- `figured.` -> `imaginei.` (Kuon, root)
- `I almost miss her muttered reply.` -> `Quase não escuto a resposta murmurada dela.` (Kuon, root)
- `It's underwear.` -> `É roupa de baixo.` (Kuon, root)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Like I said... underwear.` -> `Como eu disse... roupa de baixo.` (Kuon, root)
- `Underwear...? This long strip of cloth is\n` -> `Roupa de baixo...? Esta tira comprida de pano\n` (Kuon, root)
- `supposed to be...?` -> `deveria ser...?` (Kuon, root)
- `How is something this long supposed to cover...\n` -> `Como uma coisa tão comprida deveria cobrir...\n` (Kuon, root)
- `Wait. Is it one of those loincloth things!?` -> `Espera. É uma daquelas tangas de tira!?` (Kuon, root)
- `I suppose you can say that.` -> `Pode-se dizer que sim.` (Kuon, root)
- `I'm sure you didn't know, but still, the fact\n` -> `Tenho certeza de que você não sabia, mas ainda assim, o fato\n` (Kuon, root)
- `that you decided to use it as a sash instead...` -> `de você ter decidido usar como faixa...` (Kuon, root)
- `Hrngh...` -> `Hrgh...` (Kuon, root)
- `Hee hee...` -> `Hehe...` (Kuon, 17_01)
- `The girl giggles at my visible dismay, but\n` -> `A garota dá uma risadinha do meu desânimo visível, mas\n` (Kuon, root)
- `keeps working, hands darting over the cloth.` -> `continua trabalhando, as mãos correndo pelo pano.` (Kuon, root)
- `All that's left is...` -> `Só falta...` (Kuon, root)
- `She pulls the cloth strip off my waist in one\n` -> `Ela puxa a tira de pano da minha cintura num\n` (Kuon, root)
- `smooth tug. But...` -> `puxão só. Mas...` (Kuon, root)
- `...*Flump*` -> `...*Paf*` (Kuon, root)
- `Uh--` -> `Ãh--` (Kuon, 16_01)
- `That loincloth-sash was the only thing holding\n` -> `Aquela faixa-tanga era a única coisa segurando\n` (Kuon, root)
- `up my trousers. If that came off, then\n` -> `minha calça. Se aquilo saiu, então\n` (Kuon, root)
- `naturally--` -> `naturalmente--` (Kuon, root)
- `The pants hit the floor... and "It" flops before\n` -> `A calça cai no chão... e "Aquilo" balança diante\n` (Kuon, root)
- `her eyes, swaying jauntily despite the lack\n` -> `dos olhos dela, oscilando alegremente apesar da falta\n` (Kuon, root)
- `of wind.` -> `de vento.` (Kuon, root)
- `The girl freezes at the visual ambush, unable\n` -> `A garota congela diante da emboscada visual, incapaz\n` (Kuon, root)
- `to tear her eyes from the strange intruder.` -> `de tirar os olhos do estranho intruso.` (Kuon, root)
- `Hello...?` -> `Olá...?` (Kuon, root)
- `The girl's face, neck, hands and body slowly\n` -> `O rosto, o pescoço, as mãos e o corpo da garota aos poucos\n` (Kuon, root)
- `flush bright red, like she's boiling whole.\n` -> `ficam vermelhos vivos, como se ela fervesse inteira.\n` (Kuon, root)
- `and then...` -> `e depois...` (Kuon, 11_09)
- `Ee.` -> `Ii.` (Kuon, root)
- `Ee?` -> `Ii?` (Kuon, root)
- `EEEEEEEEYAAAAAGH!` -> `IIIIIIIIAAAAAAH!` (Kuon, root)
- `Hk--` -> `Hgh--` (Kuon, root)
- `How is that scream coming out of her!?\n` -> `Como esse grito sai dela!?\n` (Kuon, root)
- `I feel faint for a moment, overcome by\n` -> `Fico tonto por um momento, dominado por\n` (Kuon, root)
- `ultrasonic distress.` -> `aflição ultrassônica.` (Kuon, root)
- `And just as I put my hands over my ears,\n` -> `E bem quando ponho as mãos sobre os ouvidos,\n` (Kuon, root)
- `trying to block out the piercing shriek--` -> `tentando bloquear o grito agudo--` (Kuon, root)
- `*THUD*` -> `*BAQUE*` (Kuon, 13_01)
- `NNNAAARRGH!` -> `NNNAAARGH!` (Kuon, root)
- `A terrible, vengeful force hits me below,\n` -> `Uma força terrível e vingativa me atinge embaixo,\n` (Kuon, root)
- `and my world is pain. ` -> `e meu mundo é só dor. ` (Kuon, root)
- `That should be everything!` -> `Pronto, isso deve ser tudo!` (Kuon, root)
- `The girl nods in satisfaction, giving me a\n` -> `A garota acena satisfeita, me dando um\n` (Kuon, root)
- `gentle and encouraging pat on the back.` -> `tapinha gentil e encorajador nas costas.` (Kuon, root)
- `I-I get it. So this is how it's actually worn...` -> `E-Entendi. Então é assim que se veste de verdade...` (Kuon, root)
- `There's another gap in my memory, but I managed\n` -> `Tem outra lacuna na minha memória, mas consegui\n` (Kuon, root)
- `to survive whatever happened, at least. Must be\n` -> `sobreviver ao que quer que tenha acontecido, ao menos. Deve ser\n` (Kuon, root)
- `thanks to all that good karma.` -> `graças a todo aquele bom karma.` (Kuon, root)
- `So this is what it's supposed to feel like...\n` -> `Então é assim que deve ser a sensação...\n` (Kuon, root)
- `It's easy to move in. Much different from\n` -> `É fácil de me mexer. Bem diferente de\n` (Kuon, root)
- `earlier.` -> `antes.` (Kuon, 17_01)
- `I spin in place, trying to get a sense of how\n` -> `Giro no lugar, tentando ter uma noção de como\n` (Kuon, root)
- `the clothes fit.` -> `as roupas servem.` (Kuon, root)
- `Compared to this, the first try was like\n` -> `Comparada a isto, a primeira tentativa foi como\n` (Kuon, root)
- `getting myself into a straitjacket.` -> `me enfiar numa camisa de força.` (Kuon, root)
- `With no tail to speak of, and no intention\n` -> `Sem cauda alguma, e sem intenção\n` (Kuon, root)
- `to show off my ass, we agreed to sew the\n` -> `de mostrar minha bunda, concordamos em costurar\n` (Kuon, root)
- `tail hole shut.` -> `o buraco da cauda.` (Kuon, root)
- `She talks about having a tail like it's\n` -> `Ela fala em ter uma cauda como se fosse\n` (Kuon, root)
- `natural, but she seems fine with me not\n` -> `natural, mas parece tranquila com eu não\n` (Kuon, root)
- `having one.` -> `ter uma.` (Kuon, root)
- `I was a bit curious about that... but I guess\n` -> `Fiquei meio curioso sobre isso... mas acho que\n` (Kuon, root)
- `everyone's different.` -> `cada um é de um jeito.` (Kuon, root)
- `Thanks for everything.` -> `Obrigado por tudo.` (Kuon, root)
- `I turn towards her, formally expressing\n` -> `Viro-me pra ela, expressando formalmente\n` (Kuon, root)
- `my gratitude.` -> `minha gratidão.` (Kuon, root)
- `Oh no, I don't mind. And we did have a few\n` -> `Ah, não, imagina. E a gente teve uns\n` (Kuon, root)
- `misunderstandings, so...` -> `mal-entendidos, então...` (Kuon, root)
- `Now then...` -> `Bom, então...` (Kuon, root)
- `The girl sits up straight, turns to me, and\n` -> `A garota se senta ereta, vira-se pra mim e\n` (Kuon, root)
- `announces in a clear, forthright tone. ` -> `anuncia num tom claro e franco. ` (Kuon, root)
- `Kuon.` -> `Kuon.` (Kuon, 18_01)
- `My name. I haven't told you yet, I think.` -> `Meu nome. Acho que ainda não te disse.` (Kuon, root)
- `Kuon. That is my name.` -> `Kuon. Esse é o meu nome.` (Kuon, root)
- `O-Oh, your name, huh?` -> `A-Ah, seu nome, é?` (Kuon, root)
- `Kuon...` -> `Kuon...` (Kuon, 13_02)
- `And what do they call you?` -> `E como te chamam?` (Kuon, root)
- `My name...` -> `Meu nome...` (Kuon, root)
- `Yes, your name.` -> `Sim, seu nome.` (Kuon, root)
- `Kuon's words stir something in my mind--\n` -> `As palavras de Kuon mexem com algo na minha mente--\n` (Kuon, root)
- `something important.` -> `algo importante.` (Kuon, root)
- `O-Oh right, I'm--` -> `A-Ah, é, eu sou--` (Kuon, root)
- `I'm...?` -> `Eu sou...?` (Kuon, root)
- `I... am...` -> `Eu... sou...` (Kuon, root)
- `Wait... Hold on...` -> `Espera... Calma...` (Kuon, root)
- `I bury my face in my hands, and try to dredge\n` -> `Enterro o rosto nas mãos e tento resgatar\n` (Kuon, root)
- `up any memories. There's bound to be\n` -> `qualquer memória. Tem que haver\n` (Kuon, root)
- `something, anything...` -> `alguma coisa, qualquer coisa...` (Kuon, root)
- `I am... I am...` -> `Eu sou... Eu sou...` (Kuon, root)
- `But for some reason... nothing came.\n` -> `Mas por algum motivo... nada veio.\n` (Kuon, root)
- `No ending to the sentence.` -> `Nenhum fim pra frase.` (Kuon, root)
- `W-Well, where did you come from? Or perhaps...\n` -> `B-Bem, de onde você veio? Ou talvez...\n` (Kuon, root)
- `what have you been doing until now?` -> `o que você andou fazendo até agora?` (Kuon, root)
- `Where... am I from?` -> `De onde... eu venho?` (Kuon, root)
- `Where am I from... Where am I from...\n` -> `De onde eu venho... De onde eu venho...\n` (Kuon, root)
- `Where am I from...` -> `De onde eu venho...` (Kuon, root)
- `The words repeat in my mind like an incantation,\n` -> `As palavras se repetem na minha mente como um mantra,\n` (Kuon, root)
- `but... nothing. I can't think past the haze.` -> `mas... nada. Não consigo pensar além da névoa.` (Kuon, root)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `I can tell Kuon's also troubled, now that my\n` -> `Dá pra ver que Kuon também está preocupada, agora que minha\n` (Kuon, root)
- `memory loss doesn't seem so temporary.` -> `perda de memória não parece tão passageira.` (Kuon, root)
- `What have I been doing until now...?` -> `O que eu andei fazendo até agora...?` (Kuon, root)
- `As the thought crosses my mind, I raise my\n` -> `Conforme o pensamento me ocorre, ergo a\n` (Kuon, root)
- `head again, my gaze falling on her.` -> `cabeça de novo, e meu olhar recai sobre ela.` (Kuon, root)
- `That's right, she was...` -> `É verdade, ela estava...` (Kuon, root)
- `I don't remember much, but if she was the one\n` -> `Não lembro de muita coisa, mas se foi ela quem\n` (Kuon, root)
- `taking care of me, then maybe...` -> `cuidou de mim, então talvez...` (Kuon, root)
- `It looks like she's noticed my look of anticipation.\n` -> `Parece que ela notou meu olhar de expectativa.\n` (Kuon, root)
- `When she speaks, her voice is quiet.` -> `Quando fala, a voz dela é baixa.` (Kuon, root)
- `You were... passed out, alone in these remote\n` -> `Você estava... desmaiado, sozinho nestas montanhas\n` (Kuon, root)
- `mountains.` -> `remotas.` (Kuon, root)
- `alone?` -> `Sozinho?` (Kuon, 19_02)
- `Mhm. And... I'd never sleep well at night again\n` -> `Mhm. E... eu nunca mais dormiria bem à noite\n` (Kuon, root)
- `if I just left you, so... I took care of you.` -> `se simplesmente te deixasse, então... cuidei de você.` (Kuon, root)
- `So I'm sorry to get your hopes up, but I think\n` -> `Então sinto muito por criar esperança, mas acho\n` (Kuon, root)
- `that's really all I know about you for sure.` -> `que é tudo o que sei sobre você ao certo.` (Kuon, root)
- `I... see...` -> `Eu... entendo...` (Kuon, 13_05)
- `I'm sorry.` -> `Desculpa.` (Kuon, root)
- `No, it's my fault for getting my hopes up.` -> `Não, a culpa é minha por criar esperança.` (Kuon, root)
- `That's kind of you to say, but... this is a mess,\n` -> `É gentileza sua dizer isso, mas... isto é uma confusão,\n` (Kuon, root)
- `isn't it? I didn't think it'd turn out like this...` -> `não é? Não pensei que fosse acabar assim...` (Kuon, root)
- `Muttering, Kuon presses her hand to her\n` -> `Resmungando, Kuon pressiona a mão na\n` (Kuon, root)
- `forehead and rubs her temples with her\n` -> `testa e esfrega as têmporas com os\n` (Kuon, root)
- `fingers.` -> `dedos.` (Kuon, root)
- `Yeah, this is a mess all right. Great... what am\n` -> `É, isto é uma baita confusão. Ótimo... o que\n` (Kuon, root)
- `I supposed to do in a situation like this?` -> `é que eu faço numa situação dessas?` (Kuon, root)
- `All I found out was that I have no idea who I am.` -> `Tudo o que descobri foi que não faço ideia de quem sou.` (Kuon, root)
- `By the way... Where am I?` -> `A propósito... Onde estou?` (Kuon, root)
- `Would you understand if I said we're west of\n` -> `Você entenderia se eu dissesse que estamos a oeste de\n` (Kuon, root)
- `Kujyuri...? Deep in the Shishiri Province?` -> `Kujyuri...? Bem no fundo da Província de Shishiri?` (Kuon, root)
- `I see.` -> `Sim.` (Haku, 12_17)
- `...No. No idea.` -> `...Não. Nenhuma ideia.` (Kuon, root)
- `...Ah.` -> `...Ah.` (Kuon, root)
- `Finding out the name of this place doesn't\n` -> `Descobrir o nome deste lugar não\n` (Kuon, root)
- `help me one bit, since I still have no clue\n` -> `me ajuda nem um pouco, já que ainda não faço ideia\n` (Kuon, root)
- `where I am.` -> `de onde estou.` (Kuon, root)
- `Is there anything else...?\n` -> `Tem mais alguma coisa...?\n` (Kuon, root)
- `Something else I can ask her...` -> `Algo mais que eu possa perguntar a ela...` (Kuon, root)
- `Right, that huge thing!` -> `Isso, aquela coisa enorme!` (Kuon, root)
- `Huge thing?` -> `Coisa enorme?` (Kuon, root)
- `Yeah, that's right! That wriggly, slimy...\n` -> `É, isso mesmo! Aquela coisa de limo\n` (Kuon, root)
- `slime thing that attacked me. What was that!?` -> `viscosa que me atacou. O que era aquilo!?` (Kuon, root)
- `...Slime?` -> `...Limo?` (Kuon, root)
- `Kuon cocks her head at first, bewildered, but\n` -> `Kuon inclina a cabeça a princípio, confusa, mas\n` (Kuon, root)
- `then something seems to dawn on her.` -> `então algo parece lhe ocorrer.` (Kuon, root)
- `Oh, perhaps you're talking about the Tatari?` -> `Ah, talvez você esteja falando do Tatari?` (Kuon, root)
- `Tatari...?` -> `Tatari...?` (Kuon, root)
- `That's what it's called. It's a type of...\n` -> `É assim que se chama. É um tipo de...\n` (Kuon, root)
- `creature? I suppose?` -> `criatura? Eu acho?` (Kuon, root)
- `Kuon replies, uncertainty clear in her tone\n` -> `Kuon responde, a incerteza clara no tom\n` (Kuon, root)
- `and expression.` -> `e na expressão.` (Kuon, root)
- `If you asked me what it is, I wouldn't have\n` -> `Se você me perguntasse o que é, eu não teria\n` (Kuon, root)
- `a solid answer for you, to be honest.` -> `uma resposta certa pra te dar, pra ser sincera.` (Kuon, root)
- `All I know is that it lives deep underground,\n` -> `Só sei que vive bem no fundo da terra,\n` (Kuon, root)
- `where the sun doesn't reach.` -> `onde o sol não alcança.` (Kuon, root)
- `And it'll attack and eat living creatures that\n` -> `E ataca e devora criaturas vivas que\n` (Kuon, root)
- `wander inside its lair--for sustenance.` -> `entram no covil dele--pra se alimentar.` (Kuon, root)
- `Also, it never dies... and I think that's all.` -> `Além disso, ele nunca morre... e acho que é só.` (Kuon, root)
- `Never dies...?` -> `Nunca morre...?` (Kuon, root)
- `Right. It just can't.` -> `Isso. Simplesmente não pode.` (Kuon, root)
- `Burn it, cut it, beat it, but it still revives\n` -> `Queime, corte, espanque, mas ele ainda revive\n` (Kuon, root)
- `instantly. No matter what you do, you can't\n` -> `na hora. Não importa o que faça, não dá pra\n` (Kuon, root)
- `kill it.` -> `matar.` (Kuon, root)
- `No, come on. No living creature could actually\n` -> `Não, qual é. Nenhuma criatura viva poderia de fato\n` (Kuon, root)
- `be immortal.` -> `ser imortal.` (Kuon, root)
- `Maybe its body and mind are just that resilient,\n` -> `Talvez o corpo e a mente dele sejam só muito resistentes,\n` (Kuon, root)
- `and that makes it harder to kill it?` -> `e isso torne mais difícil matá-lo?` (Kuon, root)
- `No, it's true. No matter what we do to it,\n` -> `Não, é verdade. Não importa o que façamos com ele,\n` (Kuon, root)
- `it never dies. Doesn't matter what's done,\n` -> `ele nunca morre. Não importa o que se faça,\n` (Kuon, root)
- `or how...` -> `nem como...` (Kuon, root)
- `We just fight to drive it off, or scare it off\n` -> `A gente só luta pra afugentá-lo, ou assustá-lo\n` (Kuon, root)
- `with lights and loud sounds. Those seem to work\n` -> `com luzes e barulhos altos. Isso parece funcionar\n` (Kuon, root)
- `well.` -> `bem.` (Kuon, 16_01)
- `So we don't even know how many there are.\n` -> `Então nem sabemos quantos existem.\n` (Kuon, root)
- `Or much about it at all, really.` -> `Nem muito sobre ele, na verdade.` (Kuon, root)
- `What kind of monster is that? That's way\n` -> `Que tipo de monstro é esse? Isso é assustador\n` (Kuon, root)
- `too spooky...` -> `demais...` (Kuon, root)
- `So you were really lucky. If I'd arrived just\n` -> `Então você teve muita sorte. Se eu tivesse chegado só\n` (Kuon, root)
- `a bit later, there'd be nothing left of you,\n` -> `um pouco mais tarde, não sobraria nada de você,\n` (Kuon, root)
- `Right?` -> `né?` (Haku, 11_01)
- `Her words bring to mind the huge insect,\n` -> `As palavras dela me trazem à mente o inseto enorme,\n` (Kuon, root)
- `swallowed whole and melted away in the\n` -> `engolido inteiro e derretido dentro do\n` (Kuon, root)
- `thing's body.` -> `corpo daquela coisa.` (Kuon, root)
- `Kuon laughs, maybe at the sudden paleness in\n` -> `Kuon ri, talvez da palidez súbita no\n` (Kuon, root)
- `my expression, and continues.` -> `meu rosto, e continua.` (Kuon, root)
- `Don't worry. Stay away from its habitat, and\n` -> `Não se preocupe. Fique longe do habitat dele e\n` (Kuon, root)
- `keep to the paths when you travel in the wilds.` -> `se mantenha nas trilhas quando viajar pelo mato.` (Kuon, root)
- `As long as you keep these rules in mind, you'll\n` -> `Desde que tenha essas regras em mente, você\n` (Kuon, root)
- `rarely run into any trouble.` -> `raramente vai ter problema.` (Kuon, root)
- `R-Rarely, huh...?` -> `R-Raramente, é...?` (Kuon, root)
- `So everything I went through--all that was just\n` -> `Então tudo o que passei--aquilo tudo foi só\n` (Kuon, root)
- `ridiculously improbable bad luck!` -> `um azar absurdamente improvável!` (Kuon, root)
- `Well, you never know. It'd be best to just\n` -> `Bem, nunca se sabe. O melhor é só\n` (Kuon, root)
- `accept that these things happen, and deal\n` -> `aceitar que essas coisas acontecem e lidar\n` (Kuon, root)
- `with it, I think.` -> `com elas, eu acho.` (Kuon, root)
- `After all, a gust of wind at the worst time\n` -> `Afinal, uma rajada de vento na hora errada\n` (Kuon, root)
- `could be all it takes to end someone's life.` -> `pode ser tudo o que precisa pra acabar com uma vida.` (Kuon, root)
- `She says it almost casually.` -> `Ela diz isso quase com naturalidade.` (Kuon, root)
- `Not sure if that matter-of-fact tone is\n` -> `Não sei se esse tom prático é\n` (Kuon, root)
- `because that whole mess is behind us, or...` -> `porque toda aquela confusão ficou pra trás, ou...` (Kuon, root)
- `Well, what do you plan to do now?` -> `Bem, o que você pretende fazer agora?` (Kuon, root)
- `now...` -> `agora...` (Haku, 12_03)
- `What CAN I do...?` -> `O que EU posso fazer...?` (Kuon, root)
- `Ah, sorry. I suppose that's a bit of an unfair\n` -> `Ah, desculpa. Acho que essa é uma pergunta\n` (Kuon, root)
- `question.` -> `meio injusta.` (Kuon, root)
- `How are you supposed to answer a question like\n` -> `Como é que você vai responder uma pergunta dessas\n` (Kuon, root)
- `that when you don't even remember your own\n` -> `quando nem lembra do próprio\n` (Kuon, root)
- `name?` -> `nome?` (Kuon, 18_01)
- `Yeah, that about sums it up.` -> `É, isso resume bem.` (Kuon, root)
- `Hmm. Well, if that's the case...` -> `Hmm. Bem, se é esse o caso...` (Kuon, root)
- `Something occurs to her, and she offers a\n` -> `Algo lhe ocorre, e ela faz uma\n` (Kuon, root)
- `gentle suggestion.` -> `sugestão gentil.` (Kuon, root)
- `Perhaps this is some kind of fate. Why don't\n` -> `Talvez isto seja algum tipo de destino. Por que você\n` (Kuon, root)
- `you let me look after you for a little while?` -> `não me deixa cuidar de você por um tempo?` (Kuon, root)
- `The bizarre idea has me at a brief loss\n` -> `A ideia bizarra me deixa por um instante sem\n` (Kuon, root)
- `for words.` -> `palavras.` (Kuon, root)
- `This girl's going to take care of me?` -> `Esta garota vai cuidar de mim?` (Kuon, root)
- `Oh, no, I couldn't. But I do appreciate the...` -> `Ah, não, eu não poderia. Mas agradeço a...` (Kuon, root)
- `...No, wait.` -> `...Não, espera.` (Kuon, root)
- `If I go off on my own here, I'm either going\n` -> `Se eu sair por conta própria aqui, ou vou\n` (Kuon, root)
- `to get lost, or end up as some monster's\n` -> `me perder, ou virar o jantar de algum\n` (Kuon, root)
- `dinner.` -> `monstro.` (Kuon, root)
- `I'm still unsure, but she's done a lot for me.\n` -> `Ainda estou inseguro, mas ela fez muito por mim.\n` (Kuon, root)
- `She wouldn't turn on me now--not after all this.` -> `Ela não me trairia agora--não depois de tudo isso.` (Kuon, root)
- `I can at least rely on her until I understand\n` -> `Posso ao menos contar com ela até entender\n` (Kuon, root)
- `what's going on. I'll just accept this as some\n` -> `o que está havendo. Vou só aceitar isto como uma\n` (Kuon, root)
- `good fortune.` -> `boa sorte.` (Kuon, root)
- `...Understood. I'll be relying on you, at\n` -> `...Entendido. Vou contar com você, pelo\n` (Kuon, root)
- `least for a bit.` -> `menos por um tempo.` (Kuon, root)
- `Kuon smiles gently as I bow my head to her.` -> `Kuon sorri gentilmente enquanto inclino a cabeça pra ela.` (Kuon, root)
- `Yes, I think that's a wise choice. Obedience is\n` -> `Sim, acho que é uma escolha sábia. Obediência é\n` (Kuon, root)
- `always a good thing.` -> `sempre uma coisa boa.` (Kuon, root)
- `She looks relieved... It's pretty clear if I had\n` -> `Ela parece aliviada... Está bem claro que se eu\n` (Kuon, root)
- `refused, I probably wouldn't have made it on\n` -> `tivesse recusado, provavelmente não teria me virado\n` (Kuon, root)
- `my own...` -> `sozinho...` (Kuon, root)
- `Well, now that that's settled, we should\n` -> `Bem, agora que isso está resolvido, a gente deveria\n` (Kuon, root)
- `at least decide on a name for you.` -> `ao menos decidir um nome pra você.` (Kuon, root)
- `...A name?` -> `...Um nome?` (Kuon, root)
- `Well, you can't stay nameless forever. You\n` -> `Bem, você não pode ficar sem nome pra sempre. Você\n` (Kuon, root)
- `can't remember what you're called, right?` -> `não lembra como te chamam, certo?` (Kuon, root)
- `Yeah...` -> `É...` (Kuon, root)
- `She has a point. Not having a name could get\n` -> `Ela tem razão. Não ter um nome poderia ficar\n` (Kuon, root)
- `inconvenient, especially when we get to town.` -> `inconveniente, principalmente quando chegarmos à cidade.` (Kuon, root)
- `OK, anything's probably...` -> `Tá, qualquer coisa provavelmente serve...` (Kuon, root)
- `Hold on.` -> `Espera aí.` (Kuon, root)
- `Maybe... this is a golden opportunity?` -> `Talvez... esta seja uma oportunidade de ouro?` (Kuon, root)
- `I'm not happy about having no memories, but\n` -> `Não estou feliz por não ter memórias, mas\n` (Kuon, root)
- `it DOES mean I've basically got a clean slate.` -> `ISSO significa que tenho basicamente uma folha em branco.` (Kuon, root)
- `Which brings us to this... I can pick myself\n` -> `O que nos leva a isto... Posso escolher\n` (Kuon, root)
- `a really cool and mysterious name!` -> `um nome bem legal e misterioso!` (Kuon, root)
- `Maybe my name was something bland and dull,\n` -> `Talvez meu nome fosse algo sem graça e chato,\n` (Kuon, root)
- `before all this.` -> `antes de tudo isso.` (Kuon, root)
- `Well, that's not so bad. Could just as easily\n` -> `Bem, isso não é tão ruim. Podia facilmente\n` (Kuon, root)
- `have been something ridiculous and\n` -> `ter sido algo ridículo e\n` (Kuon, root)
- `embarrassing...` -> `vergonhoso...` (Kuon, root)
- `You know what, amnesia's not so bad. It's\n` -> `Quer saber, amnésia não é tão ruim. É\n` (Kuon, root)
- `awesome, even! Gotta make the best of a bad\n` -> `até demais! Tenho que tirar o melhor de uma situação\n` (Kuon, root)
- `situation.` -> `ruim.` (Kuon, 18_01)
- `So this is a real opportunity. Can't just\n` -> `Então esta é uma oportunidade de verdade. Não dá pra\n` (Kuon, root)
- `go with some random name.` -> `escolher um nome qualquer.` (Kuon, root)
- `Just have to think of a name cool enough to\n` -> `Só tenho que pensar num nome legal o bastante pra\n` (Kuon, root)
- `make people jealous, but not something I'd\n` -> `deixar todo mundo com inveja, mas nada de que eu\n` (Kuon, root)
- `regret later...` -> `me arrependa depois...` (Kuon, root)
- `OK! My name is--` -> `Tá! Meu nome é--` (Kuon, root)
- `Hmm. What kind of name would suit you best?` -> `Hmm. Que tipo de nome combinaria mais com você?` (Kuon, root)
- `Kuon seems unconcerned by my dramatically\n` -> `Kuon parece indiferente ao meu braço\n` (Kuon, root)
- `outstretched arm, pondering to herself.` -> `dramaticamente estendido, ponderando consigo mesma.` (Kuon, root)
- `An uneasy feeling rises, and I nervously ask\n` -> `Uma sensação ruim surge, e nervoso pergunto\n` (Kuon, root)
- `her.` -> `a ela.` (Kuon, 17_01)
- `Um... you aren't... planning to think about\n` -> `Ãh... você não está... pensando em decidir\n` (Kuon, root)
- `my new name too, are you?` -> `o meu novo nome também, está?` (Kuon, root)
- `She looks surprised, like she has no idea\n` -> `Ela parece surpresa, como se não fizesse ideia\n` (Kuon, root)
- `what I'm asking.` -> `do que estou perguntando.` (Kuon, root)
- `Planning to? It's my duty.` -> `Pensando em? É meu dever.` (Kuon, root)
- `Y-Your duty?` -> `S-Seu dever?` (Kuon, root)
- `A guardian is essentially a parent. Since I am\n` -> `Um guardião é essencialmente um pai. Já que agora\n` (Kuon, root)
- `now your guardian, it's my duty to give you\n` -> `sou sua guardiã, é meu dever te dar\n` (Kuon, root)
- `a name.` -> `um nome.` (Kuon, root)
- `No, that's...` -> `Não, isso é...` (Kuon, root)
- `Come on... This tiny girl can't honestly think\n` -> `Qual é... Esta garotinha não pode honestamente se achar\n` (Kuon, root)
- `of herself as my parent, right...?` -> `minha mãe, pode...?` (Kuon, root)
- `Though if you'd prefer to go on your own without\n` -> `Embora, se você preferir seguir por conta própria sem\n` (Kuon, root)
- `me, then by all means, make your own decisions.` -> `mim, então fique à vontade, tome suas próprias decisões.` (Kuon, root)
- `U... Urgh...` -> `Nnh... Argh...` (Kuon, root)
- `How can I argue with that...? Kuon smiles\n` -> `Como discutir com isso...? Kuon sorri\n` (Kuon, root)
- `brightly as I sag in defeat, and claps her\n` -> `radiante enquanto eu desabo derrotado, e bate\n` (Kuon, root)
- `hands.` -> `as mãos.` (Kuon, 19_07)
- `Then I think it's decided!` -> `Então acho que está decidido!` (Kuon, root)
- `*Sigh*... So much for the whole "awesome name"\n` -> `*Suspiro*... Lá se foi a ideia toda do "nome\n` (Kuon, root)
- `idea...` -> `incrível"...` (Kuon, root)
- `In the end, I guess I still have no say in\n` -> `No fim, acho que ainda não tenho voz em\n` (Kuon, root)
- `anything--not even my own name.` -> `nada--nem no meu próprio nome.` (Kuon, root)
- `Now, let's see. Your new name is...` -> `Bom, vejamos. Seu novo nome é...` (Kuon, root)
- `Kuon cocks her head, looking thoughtfully\n` -> `Kuon inclina a cabeça, olhando pensativa\n` (Kuon, root)
- `to the ceiling.` -> `para o teto.` (Kuon, root)
- `After a moment of silence, she mutters a couple\n` -> `Após um momento de silêncio, ela murmura algumas\n` (Kuon, root)
- `syllables.` -> `sílabas.` (Kuon, root)
- `Ha... ku...` -> `Ha... ku...` (Kuon, root)
- `Haku...?` -> `Haku...?` (Kuon, root)
- `That's right. Haku.` -> `Isso mesmo. Haku.` (Kuon, root)
- `She seems pretty proud of it. Having said it,\n` -> `Ela parece bem orgulhosa disso. Tendo dito,\n` (Kuon, root)
- `she smiles confidently.` -> `ela sorri confiante.` (Kuon, root)
- `I think you should call yourself Haku from\n` -> `Acho que você deveria se chamar Haku de\n` (Kuon, root)
- `now on.` -> `agora em diante.` (Kuon, root)
- `Haku...` -> `Haku...` (Kuon, 14_09)
- `I ruminate over this name she's given me. ` -> `Rumino o nome que ela me deu. ` (Kuon, root)
- `...It's not that cool...` -> `...Não é lá tão legal...` (Kuon, root)
- `...Did you say something?` -> `...Você disse alguma coisa?` (Kuon, 14_03)
- `*Shudder*` -> `*Tremor*` (Kuon, 11_01)
- `A slight shiver runs through me, and a chill\n` -> `Um leve arrepio me percorre, e um frio\n` (Kuon, root)
- `runs down my spine.` -> `desce pela minha espinha.` (Kuon, root)
- `Though Kuon is smiling as sweetly as ever at me,\n` -> `Embora Kuon esteja sorrindo tão docemente quanto sempre pra mim,\n` (Kuon, root)
- `my blood runs cold for a moment.` -> `meu sangue gela por um momento.` (Kuon, root)
- `Erk! N-Nope, didn't say a word...` -> `Erk! N-Não, não disse nada...` (Kuon, root)
- `In response to my reaction, Kuon clears her\n` -> `Em resposta à minha reação, Kuon limpa a\n` (Kuon, root)
- `throat with a delicate little cough,\n` -> `garganta com uma tossezinha delicada,\n` (Kuon, root)
- `speaking seriously.` -> `falando sério.` (Kuon, root)
- `It's a very distinguished name.` -> `É um nome muito ilustre.` (Kuon, root)
- `It comes from the name of one celebrated in\n` -> `Vem do nome de alguém celebrado em\n` (Kuon, root)
- `ancient legends and stories.` -> `lendas e histórias antigas.` (Kuon, root)
- `Legends...` -> `Lendas...` (Kuon, root)
- `Yes... from the Utawarerumono.` -> `Sim... do Utawarerumono.` (Kuon, root)
- `Without any memories or context, I can't really\n` -> `Sem memórias nem contexto, não consigo bem\n` (Kuon, root)
- `appreciate or understand the significance.` -> `apreciar ou entender o significado.` (Kuon, root)
- `But something about the faraway affection in her\n` -> `Mas algo no afeto distante na expressão\n` (Kuon, root)
- `expression tells me it's an important name.` -> `dela me diz que é um nome importante.` (Kuon, root)
- `All right...` -> `Tudo bem...` (Kuon, root)
- `From now on, then, I'm Haku.\n` -> `De agora em diante, então, sou Haku.\n` (Kuon, root)
- `Please call me that from now on.` -> `Que me chame assim de agora em diante.` (Kuon, root)
- `Mhm. Glad to hear it, I think.` -> `Mhm. Fico feliz em ouvir isso, eu acho.` (Kuon, root)
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
| 0xe192 | 45 | Upon returning to the tent, the girl starts\n |
| 0xe1c0 | 25 | digging through her bags. |
| 0xe1da | 4 | Girl |
| 0xe1df | 45 | Hmm, I'm sure I put it somewhere back here... |
| 0xe20d | 17 | Aha! There we go. |
| 0xe21f | 42 | I was wondering what to do with these...\n |
| 0xe24a | 47 | I certainly didn't think they'd come in handy\n |
| 0xe27a | 10 | like this. |
| 0xe285 | 43 | With those words, the girl holds out some\n |
| 0xe2b1 | 15 | folded fabrics. |
| 0xe2c1 | 48 | Here, a change of clothes. If you keep walking\n |
| 0xe2f2 | 38 | around like that, you'll catch a cold. |
| 0xe319 | 6 | Hm...? |
| 0xe320 | 48 | They definitely seem sturdier than the clothes\n |
| 0xe351 | 16 | I had on, but... |
| 0xe362 | 44 | Ahaha, don't make that face! They're men's\n |
| 0xe38f | 8 | clothes. |
| 0xe398 | 7 | O-Oh... |
| 0xe3a0 | 38 | Well, I'm going to go draw some water. |
| 0xe3c7 | 43 | Oh, she's trying to give me some privacy.\n |
| 0xe3f3 | 19 | That's kind of her. |
| 0xe407 | 7 | Yikes-- |
| 0xe40f | 44 | A burst of cold air streams in as the girl\n |
| 0xe43c | 15 | makes her exit. |
| 0xe44c | 45 | G-God, that's cold... OK, if I stay in this\n |
| 0xe47a | 49 | any longer, I'm gonna come down with something... |
| 0xe4ac | 37 | I spread out the clothes she gave me. |
| 0xe4d2 | 42 | But... something's missing. One crucial,\n |
| 0xe4fd | 39 | important thing. I stare uncertainly,\n |
| 0xe525 | 12 | head tilted. |
| 0xe532 | 28 | ...Where's the underwear...? |
| 0xe54f | 48 | I turn the clothes inside out, right-side out,\n |
| 0xe580 | 44 | even shake them around... but no underpants. |
| 0xe5ad | 48 | Figures. She wouldn't miraculously just happen\n |
| 0xe5de | 51 | to have spare men's underwear around the place...   |
| 0xe612 | 34 | Which means... I have no choice... |
| 0xe635 | 48 | Because I have no choice, because I am a slave\n |
| 0xe666 | 47 | to the whims of fate, I'll have to go commando. |
| 0xe696 | 48 | I-It's not like this is something I WANT to do!  |
| 0xe6c7 | 49 | Primitive man was naked to start with, so don't\n |
| 0xe6f9 | 50 | freak out. It'll just be more... brisk than usual. |
| 0xe72c | 44 | Trying to reassure myself, I start putting\n |
| 0xe759 | 31 | on the clothes provided. But... |
| 0xe779 | 45 | OK, let's see these pants... There's a hole\n |
| 0xe7a7 | 35 | here, so this must be the front...? |
| 0xe7cb | 12 | *Shuffle*... |
| 0xe7d8 | 50 | Ho-kay... Hm. Doesn't feel all that comfortable... |
| 0xe80b | 42 | Ah, whatever. Next, I get this top on...\n |
| 0xe836 | 37 | and I just tie it off with this sash? |
| 0xe85c | 8 | *Swoosh* |
| 0xe865 | 14 | There we go... |
| 0xe874 | 39 | Honestly, though, this thing's pretty\n |
| 0xe89c | 16 | uncomfortable... |
| 0xe8ad | 45 | The top's a little off, but the bottom just\n |
| 0xe8db | 38 | has way too many things wrong with it. |
| 0xe902 | 47 | The way it's stretching can't be good for it,\n |
| 0xe932 | 47 | and it's... getting a little drafty downstairs. |
| 0xe962 | 42 | Since the fly opens so wide, it's pretty\n |
| 0xe98d | 47 | well-ventilated. Well, more like it's letting\n |
| 0xe9bd | 18 | the wind right in. |
| 0xe9d0 | 48 | The real problem here is how I'm going to make\n |
| 0xea01 | 41 | sure I don't accidentally flash anyone... |
| 0xea2b | 51 | There are some serious issues with these clothes.\n |
| 0xea5f | 49 | I'm a gust of wind away from becoming a streaker. |
| 0xea91 | 44 | Something tells me this isn't going to work. |
| 0xeabe | 47 | Maybe I should just explain and ask to borrow\n |
| 0xeaee | 41 | some underwear...? No, no, can't do that. |
| 0xeb18 | 46 | Even if it's a perfectly innocent and honest\n |
| 0xeb47 | 47 | request, a guy can't ask a girl for underpants. |
| 0xeb77 | 48 | And she's lending these out of the kindness of\n |
| 0xeba8 | 39 | her heart! I can't go begging for more. |
| 0xebd0 | 39 | I don't need to bother her with this.\n |
| 0xebf8 | 33 | Just gotta get a little creative. |
| 0xec1a | 48 | Having settled on a course of action, I fumble\n |
| 0xec4b | 36 | with the fabric for a little longer. |
| 0xec70 | 46 | Oh, got it. I can use this heavier fabric as\n |
| 0xec9f | 43 | a kind of apron, and now this can be... Hm? |
| 0xeccb | 8 | ...Uh... |
| 0xecd4 | 50 | I feel eyes on me, and glance up. She's standing\n |
| 0xed07 | 42 | there, staring... amazed, concerned, and\n |
| 0xed32 | 12 | exasperated. |
| 0xed3f | 38 | You aren't... messing around, are you? |
| 0xed66 | 42 | I see something in her expression twitch\n |
| 0xed91 | 26 | as she awaits my response. |
| 0xedac | 44 | Urgh... that look in her eyes... It's like\n |
| 0xedd9 | 36 | a parent saying "I'm not mad, just\n |
| 0xedfe | 21 | disappointed in you." |
| 0xee14 | 45 | N-No, look, I can explain! I'm only dressed\n |
| 0xee42 | 44 | like this 'cause there wasn't any underwear! |
| 0xee6f | 43 | ...The thing you have wrapped around your\n |
| 0xee9b | 42 | waist right now is an aperyu. It goes on\n |
| 0xeec6 | 15 | your shoulders. |
| 0xeed6 | 4 | Huh? |
| 0xeedb | 46 | You've got everything on the wrong sides for\n |
| 0xef0a | 46 | the top, too... and I think the pants are on\n |
| 0xef39 | 10 | backwards. |
| 0xef44 | 40 | Backwards...? Hold on, the fly's here.\n |
| 0xef6d | 34 | So that makes it the front, right? |
| 0xef90 | 41 | That's where the tail's supposed to run\n |
| 0xefba | 10 | through... |
| 0xefc5 | 16 | Huh...? Tail...? |
| 0xefd6 | 44 | I'm caught off guard. A tail's not exactly\n |
| 0xf003 | 43 | something you expect to come up in normal\n |
| 0xf02f | 13 | conversation. |
| 0xf03d | 45 | I glance over, and notice something swaying\n |
| 0xf06b | 11 | behind her. |
| 0xf077 | 47 | Something ropelike, extending from just above\n |
| 0xf0a7 | 44 | her rear. Something covered in fur, almost\n |
| 0xf0d4 | 7 | like... |
| 0xf0dc | 10 | ...a tail? |
| 0xf0e7 | 46 | Come to think of it, I think I saw it behind\n |
| 0xf116 | 41 | her while we were running in the caves... |
| 0xf140 | 41 | But I dismissed the thought, of course.\n |
| 0xf16a | 36 | Common sense says that's ridiculous. |
| 0xf18f | 45 | No, no, no. There's just no way. It must be\n |
| 0xf1bd | 38 | some kind of accessory or something... |
| 0xf1e4 | 44 | As I ponder the possibilities, I reach out\n |
| 0xf211 | 27 | and grasp the swaying tail. |
| 0xf22d | 6 | H-Hgh! |
| 0xf234 | 45 | Wow, this is really something. It looks and\n |
| 0xf262 | 33 | feels like it's an actual tail... |
| 0xf284 | 46 | And this texture! It's even soft to the touch. |
| 0xf2b3 | 26 | H-Haah! Ah... Wh... Wha... |
| 0xf2ce | 42 | Fluffy, soft, and silky smooth. It feels\n |
| 0xf2f9 | 37 | amazing... It'd make a perfect scarf. |
| 0xf31f | 43 | And it's even wriggling, but I can't work\n |
| 0xf34b | 42 | out if there's some mechanism moving it... |
| 0xf376 | 7 | *Floof* |
| 0xf37e | 3 | Hm? |
| 0xf382 | 19 | Ngh... Ghh... Hngh! |
| 0xf396 | 44 | What's this? It's even getting all fluffed\n |
| 0xf3c3 | 9 | up now... |
| 0xf3cd | 41 | As I run my hands over the soft fur, it\n |
| 0xf3f7 | 39 | suddenly puffs up, like its hairs are\n |
| 0xf41f | 16 | standing on end. |
| 0xf430 | 12 | The heck...? |
| 0xf43d | 47 | Curiosity getting the better of me, I grab it\n |
| 0xf46d | 38 | with both hands. And at that moment... |
| 0xf494 | 8 | Ah...!\n |
| 0xf49d | 16 | ...Waaaaaaaaaah! |
| 0xf4ae | 21 | ...Gah! Wh-What the-- |
| 0xf4c4 | 48 | Her outburst surprises me, and I instinctively\n |
| 0xf4f5 | 19 | let go of the tail. |
| 0xf509 | 44 | I look back to her, uncertain of what just\n |
| 0xf536 | 9 | happened. |
| 0xf549 | 41 | As I meet her eyes, I see her shoulders\n |
| 0xf573 | 37 | trembling... and she's glaring at me? |
| 0xf599 | 23 | H-Hey, what's wrong...? |
| 0xf5b1 | 19 | What's... wrong...? |
| 0xf5c5 | 41 | Staring icily, the girl steps towards me. |
| 0xf5ef | 34 | What... do you think you're doing? |
| 0xf612 | 18 | What do I... what? |
| 0xf625 | 13 | You heard me! |
| 0xf633 | 49 | What are you doing, grabbing a girl's tail like\n |
| 0xf665 | 33 | that? I was quite clear, I think! |
| 0xf687 | 35 | Grabbing a...? No, that was only... |
| 0xf6ab | 43 | Wait, you don't mean that's... that's real? |
| 0xf6d7 | 49 | Of course it is! If this beautiful tail of mine\n |
| 0xf709 | 25 | isn't real, then what is? |
| 0xf723 | 18 | N-No, it's just... |
| 0xf736 | 6 | Urgh-- |
| 0xf73d | 47 | I stagger backwards, feeling a sense of power\n |
| 0xf76d | 43 | from her completely at odds with her cute\n |
| 0xf799 | 6 | looks. |
| 0xf7a0 | 44 | She strokes her tail lovingly, as if she's\n |
| 0xf7cd | 45 | trying to soothe the thing after my picking\n |
| 0xf7fb | 6 | at it. |
| 0xf802 | 47 | But even still, just grabbing my tail without\n |
| 0xf832 | 17 | even a warning... |
| 0xf844 | 40 | No... well, I mean... how do I put it... |
| 0xf86d | 25 | She lets out a deep sigh. |
| 0xf887 | 44 | ...It looks like you honestly didn't know,\n |
| 0xf8b4 | 43 | so I suppose it can't be helped. I'll let\n |
| 0xf8e0 | 14 | it go for now. |
| 0xf8ef | 14 | Well... sorry. |
| 0xf8fe | 46 | But it's not like you would expect anyone to\n |
| 0xf92d | 17 | have a real tail. |
| 0xf93f | 44 | I mean, humans did evolve from apes, and I\n |
| 0xf96c | 48 | guess there's been cases of reverse evolution... |
| 0xf99d | 49 | The girl looks at me strangely, as if she wants\n |
| 0xf9cf | 44 | to respond to my belated attempt at excuses. |
| 0xf9fc | 6 | ...Hm? |
| 0xfa03 | 22 | ...Am I seeing things? |
| 0xfa1a | 44 | A beautiful face, elegant facial features,\n |
| 0xfa47 | 44 | and shiny black hair. Yep. No problems here. |
| 0xfa74 | 46 | She's definitely cute, but that's not really\n |
| 0xfaa3 | 38 | the issue right now. The problem is... |
| 0xfaca | 44 | ...I-I didn't notice in all the commotion,\n |
| 0xfaf7 | 41 | but... are those furry tufts on her head? |
| 0xfb21 | 17 | What's wrong now? |
| 0xfb33 | 45 | Those big ears... big, furry ears... twitch\n |
| 0xfb61 | 13 | for a moment. |
| 0xfb6f | 31 | Oh... uh... well, that's... um. |
| 0xfb8f | 48 | Ears and a tail... She looks human, but is she\n |
| 0xfbc0 | 15 | something else? |
| 0xfbd0 | 46 | No, wait. I can't afford for her to leave me\n |
| 0xfbff | 44 | behind for asking too many dumb questions... |
| 0xfc2c | 16 | ...It's nothing. |
| 0xfc3d | 44 | Best to just act like I didn't see anything. |
| 0xfc6a | 48 | Uhh, I'm not too familiar with the customs and\n |
| 0xfc9b | 43 | etiquette around these parts, is the thing. |
| 0xfcc7 | 47 | That's plain enough just from looking at you.\n |
| 0xfcf7 | 41 | What are you doing with these clothes...? |
| 0xfd21 | 44 | The girl lets out a small sigh at my excuse. |
| 0xfd4e | 48 | Anyhow, we may as well get you properly dressed. |
| 0xfd7f | 9 | Y-Yeah... |
| 0xfd89 | 42 | At her words, I hastily start working on\n |
| 0xfdb4 | 45 | undoing the strings. Maybe I made the knots\n |
| 0xfde2 | 12 | too tight... |
| 0xfdef | 44 | There... we go. Phew... That's one untied.\n |
| 0xfe1c | 41 | Next, I'll... Ngh... This one's knotted\n |
| 0xfe46 | 19 | pretty tight too... |
| 0xfe5a | 45 | As I fumble, the girl kneels, and patiently\n |
| 0xfe88 | 39 | starts undoing the knots herself with\n |
| 0xfeb0 | 14 | easy deftness. |
| 0xfebf | 11 | Hold still. |
| 0xfecb | 20 | A-All right. Thanks. |
| 0xfee0 | 7 | *Swish* |
| 0xfee8 | 44 | I never imagined you'd use this as a sash... |
| 0xff15 | 46 | She murmurs with an odd wryness, setting her\n |
| 0xff44 | 43 | attentions on the sash holding up my pants. |
| 0xff70 | 47 | Really? Well, it's long and narrow, so I just\n |
| 0xffa0 | 8 | figured. |
| 0xffa9 | 33 | I almost miss her muttered reply. |
| 0xffcb | 15 | It's underwear. |
| 0xffdb | 7 | ...Huh? |
| 0xffe3 | 25 | Like I said... underwear. |
| 0xfffd | 43 | Underwear...? This long strip of cloth is\n |
| 0x10029 | 18 | supposed to be...? |
| 0x1003c | 49 | How is something this long supposed to cover...\n |
| 0x1006e | 43 | Wait. Is it one of those loincloth things!? |
| 0x1009a | 27 | I suppose you can say that. |
| 0x100b6 | 47 | I'm sure you didn't know, but still, the fact\n |
| 0x100e6 | 47 | that you decided to use it as a sash instead... |
| 0x10116 | 8 | Hrngh... |
| 0x1011f | 10 | Hee hee... |
| 0x1012a | 44 | The girl giggles at my visible dismay, but\n |
| 0x10157 | 44 | keeps working, hands darting over the cloth. |
| 0x10184 | 21 | All that's left is... |
| 0x1019a | 47 | She pulls the cloth strip off my waist in one\n |
| 0x101ca | 18 | smooth tug. But... |
| 0x101dd | 10 | ...*Flump* |
| 0x101e8 | 4 | Uh-- |
| 0x101ed | 48 | That loincloth-sash was the only thing holding\n |
| 0x1021e | 40 | up my trousers. If that came off, then\n |
| 0x10247 | 11 | naturally-- |
| 0x10253 | 50 | The pants hit the floor... and "It" flops before\n |
| 0x10286 | 45 | her eyes, swaying jauntily despite the lack\n |
| 0x102b4 | 8 | of wind. |
| 0x102bd | 47 | The girl freezes at the visual ambush, unable\n |
| 0x102ed | 43 | to tear her eyes from the strange intruder. |
| 0x10319 | 9 | Hello...? |
| 0x10323 | 46 | The girl's face, neck, hands and body slowly\n |
| 0x10352 | 45 | flush bright red, like she's boiling whole.\n |
| 0x10380 | 11 | And then... |
| 0x1038c | 3 | Ee. |
| 0x10390 | 3 | Ee? |
| 0x10394 | 17 | EEEEEEEEYAAAAAGH! |
| 0x103a6 | 4 | Hk-- |
| 0x103ab | 40 | How is that scream coming out of her!?\n |
| 0x103d4 | 40 | I feel faint for a moment, overcome by\n |
| 0x103fd | 20 | ultrasonic distress. |
| 0x10412 | 42 | And just as I put my hands over my ears,\n |
| 0x1043d | 41 | trying to block out the piercing shriek-- |
| 0x10467 | 6 | *THUD* |
| 0x1046e | 11 | NNNAAARRGH! |
| 0x1047a | 43 | A terrible, vengeful force hits me below,\n |
| 0x104a6 | 22 | and my world is pain.  |
| 0x104bd | 26 | That should be everything! |
| 0x104d8 | 44 | The girl nods in satisfaction, giving me a\n |
| 0x10505 | 39 | gentle and encouraging pat on the back. |
| 0x1052d | 48 | I-I get it. So this is how it's actually worn... |
| 0x1055e | 49 | There's another gap in my memory, but I managed\n |
| 0x10590 | 49 | to survive whatever happened, at least. Must be\n |
| 0x105c2 | 30 | thanks to all that good karma. |
| 0x105e1 | 47 | So this is what it's supposed to feel like...\n |
| 0x10611 | 43 | It's easy to move in. Much different from\n |
| 0x1063d | 8 | earlier. |
| 0x10646 | 47 | I spin in place, trying to get a sense of how\n |
| 0x10676 | 16 | the clothes fit. |
| 0x10687 | 42 | Compared to this, the first try was like\n |
| 0x106b2 | 35 | getting myself into a straitjacket. |
| 0x106d6 | 44 | With no tail to speak of, and no intention\n |
| 0x10703 | 42 | to show off my ass, we agreed to sew the\n |
| 0x1072e | 15 | tail hole shut. |
| 0x1073e | 41 | She talks about having a tail like it's\n |
| 0x10768 | 41 | natural, but she seems fine with me not\n |
| 0x10792 | 11 | having one. |
| 0x1079e | 47 | I was a bit curious about that... but I guess\n |
| 0x107ce | 21 | everyone's different. |
| 0x107e4 | 22 | Thanks for everything. |
| 0x107fb | 41 | I turn towards her, formally expressing\n |
| 0x10825 | 13 | my gratitude. |
| 0x10833 | 44 | Oh no, I don't mind. And we did have a few\n |
| 0x10860 | 24 | misunderstandings, so... |
| 0x10879 | 11 | Now then... |
| 0x10885 | 45 | The girl sits up straight, turns to me, and\n |
| 0x108b3 | 39 | announces in a clear, forthright tone.  |
| 0x108db | 5 | Kuon. |
| 0x108e1 | 41 | My name. I haven't told you yet, I think. |
| 0x1090b | 22 | Kuon. That is my name. |
| 0x10922 | 21 | O-Oh, your name, huh? |
| 0x10938 | 7 | Kuon... |
| 0x10940 | 26 | And what do they call you? |
| 0x1095b | 10 | My name... |
| 0x10966 | 15 | Yes, your name. |
| 0x10976 | 42 | Kuon's words stir something in my mind--\n |
| 0x109a1 | 20 | something important. |
| 0x109b6 | 17 | O-Oh right, I'm-- |
| 0x109c8 | 7 | I'm...? |
| 0x109d0 | 10 | I... am... |
| 0x109db | 18 | Wait... Hold on... |
| 0x109ee | 47 | I bury my face in my hands, and try to dredge\n |
| 0x10a1e | 38 | up any memories. There's bound to be\n |
| 0x10a45 | 22 | something, anything... |
| 0x10a5c | 15 | I am... I am... |
| 0x10a6c | 38 | But for some reason... nothing came.\n |
| 0x10a93 | 26 | No ending to the sentence. |
| 0x10aae | 48 | W-Well, where did you come from? Or perhaps...\n |
| 0x10adf | 35 | what have you been doing until now? |
| 0x10b03 | 19 | Where... am I from? |
| 0x10b17 | 39 | Where am I from... Where am I from...\n |
| 0x10b3f | 18 | Where am I from... |
| 0x10b52 | 50 | The words repeat in my mind like an incantation,\n |
| 0x10b85 | 44 | but... nothing. I can't think past the haze. |
| 0x10bb2 | 8 | I see... |
| 0x10bbb | 46 | I can tell Kuon's also troubled, now that my\n |
| 0x10bea | 38 | memory loss doesn't seem so temporary. |
| 0x10c11 | 36 | What have I been doing until now...? |
| 0x10c36 | 44 | As the thought crosses my mind, I raise my\n |
| 0x10c63 | 35 | head again, my gaze falling on her. |
| 0x10c87 | 24 | That's right, she was... |
| 0x10ca0 | 47 | I don't remember much, but if she was the one\n |
| 0x10cd0 | 32 | taking care of me, then maybe... |
| 0x10cf1 | 54 | It looks like she's noticed my look of anticipation.\n |
| 0x10d28 | 36 | When she speaks, her voice is quiet. |
| 0x10d4d | 47 | You were... passed out, alone in these remote\n |
| 0x10d7d | 10 | mountains. |
| 0x10d88 | 6 | Alone? |
| 0x10d8f | 49 | Mhm. And... I'd never sleep well at night again\n |
| 0x10dc1 | 45 | if I just left you, so... I took care of you. |
| 0x10def | 48 | So I'm sorry to get your hopes up, but I think\n |
| 0x10e20 | 44 | that's really all I know about you for sure. |
| 0x10e4d | 11 | I... see... |
| 0x10e59 | 10 | I'm sorry. |
| 0x10e64 | 42 | No, it's my fault for getting my hopes up. |
| 0x10e8f | 51 | That's kind of you to say, but... this is a mess,\n |
| 0x10ec3 | 51 | isn't it? I didn't think it'd turn out like this... |
| 0x10ef7 | 41 | Muttering, Kuon presses her hand to her\n |
| 0x10f21 | 40 | forehead and rubs her temples with her\n |
| 0x10f4a | 8 | fingers. |
| 0x10f53 | 50 | Yeah, this is a mess all right. Great... what am\n |
| 0x10f86 | 42 | I supposed to do in a situation like this? |
| 0x10fb1 | 49 | All I found out was that I have no idea who I am. |
| 0x10fe3 | 25 | By the way... Where am I? |
| 0x10ffd | 46 | Would you understand if I said we're west of\n |
| 0x1102c | 42 | Kujyuri...? Deep in the Shishiri Province? |
| 0x11057 | 6 | I see. |
| 0x1105e | 15 | ...No. No idea. |
| 0x1106e | 6 | ...Ah. |
| 0x11075 | 44 | Finding out the name of this place doesn't\n |
| 0x110a2 | 45 | help me one bit, since I still have no clue\n |
| 0x110d0 | 11 | where I am. |
| 0x110dc | 28 | Is there anything else...?\n |
| 0x110f9 | 31 | Something else I can ask her... |
| 0x11119 | 23 | Right, that huge thing! |
| 0x11131 | 11 | Huge thing? |
| 0x1113d | 44 | Yeah, that's right! That wriggly, slimy...\n |
| 0x1116a | 45 | slime thing that attacked me. What was that!? |
| 0x11198 | 9 | ...Slime? |
| 0x111a2 | 47 | Kuon cocks her head at first, bewildered, but\n |
| 0x111d2 | 36 | then something seems to dawn on her. |
| 0x111f7 | 44 | Oh, perhaps you're talking about the Tatari? |
| 0x11224 | 10 | Tatari...? |
| 0x1122f | 44 | That's what it's called. It's a type of...\n |
| 0x1125c | 20 | creature? I suppose? |
| 0x11271 | 45 | Kuon replies, uncertainty clear in her tone\n |
| 0x1129f | 15 | and expression. |
| 0x112af | 45 | If you asked me what it is, I wouldn't have\n |
| 0x112dd | 37 | a solid answer for you, to be honest. |
| 0x11303 | 47 | All I know is that it lives deep underground,\n |
| 0x11333 | 28 | where the sun doesn't reach. |
| 0x11350 | 48 | And it'll attack and eat living creatures that\n |
| 0x11381 | 39 | wander inside its lair--for sustenance. |
| 0x113a9 | 46 | Also, it never dies... and I think that's all. |
| 0x113d8 | 14 | Never dies...? |
| 0x113e7 | 21 | Right. It just can't. |
| 0x113fd | 48 | Burn it, cut it, beat it, but it still revives\n |
| 0x1142e | 45 | instantly. No matter what you do, you can't\n |
| 0x1145c | 8 | kill it. |
| 0x11465 | 48 | No, come on. No living creature could actually\n |
| 0x11496 | 12 | be immortal. |
| 0x114a3 | 50 | Maybe its body and mind are just that resilient,\n |
| 0x114d6 | 36 | and that makes it harder to kill it? |
| 0x114fb | 44 | No, it's true. No matter what we do to it,\n |
| 0x11528 | 44 | it never dies. Doesn't matter what's done,\n |
| 0x11555 | 9 | or how... |
| 0x1155f | 48 | We just fight to drive it off, or scare it off\n |
| 0x11590 | 49 | with lights and loud sounds. Those seem to work\n |
| 0x115c2 | 5 | well. |
| 0x115c8 | 43 | So we don't even know how many there are.\n |
| 0x115f4 | 32 | Or much about it at all, really. |
| 0x11615 | 42 | What kind of monster is that? That's way\n |
| 0x11640 | 13 | too spooky... |
| 0x1164e | 47 | So you were really lucky. If I'd arrived just\n |
| 0x1167e | 46 | a bit later, there'd be nothing left of you,\n |
| 0x116ad | 6 | right? |
| 0x116b4 | 42 | Her words bring to mind the huge insect,\n |
| 0x116df | 40 | swallowed whole and melted away in the\n |
| 0x11708 | 13 | thing's body. |
| 0x11716 | 46 | Kuon laughs, maybe at the sudden paleness in\n |
| 0x11745 | 29 | my expression, and continues. |
| 0x11763 | 46 | Don't worry. Stay away from its habitat, and\n |
| 0x11792 | 47 | keep to the paths when you travel in the wilds. |
| 0x117c2 | 49 | As long as you keep these rules in mind, you'll\n |
| 0x117f4 | 28 | rarely run into any trouble. |
| 0x11811 | 17 | R-Rarely, huh...? |
| 0x11823 | 49 | So everything I went through--all that was just\n |
| 0x11855 | 33 | ridiculously improbable bad luck! |
| 0x11877 | 44 | Well, you never know. It'd be best to just\n |
| 0x118a4 | 43 | accept that these things happen, and deal\n |
| 0x118d0 | 17 | with it, I think. |
| 0x118e2 | 45 | After all, a gust of wind at the worst time\n |
| 0x11910 | 44 | could be all it takes to end someone's life. |
| 0x1193d | 28 | She says it almost casually. |
| 0x1195a | 41 | Not sure if that matter-of-fact tone is\n |
| 0x11984 | 43 | because that whole mess is behind us, or... |
| 0x119b0 | 33 | Well, what do you plan to do now? |
| 0x119d2 | 6 | Now... |
| 0x119d9 | 17 | What CAN I do...? |
| 0x119eb | 48 | Ah, sorry. I suppose that's a bit of an unfair\n |
| 0x11a1c | 9 | question. |
| 0x11a26 | 48 | How are you supposed to answer a question like\n |
| 0x11a57 | 44 | that when you don't even remember your own\n |
| 0x11a84 | 5 | name? |
| 0x11a8a | 28 | Yeah, that about sums it up. |
| 0x11aa7 | 32 | Hmm. Well, if that's the case... |
| 0x11ac8 | 43 | Something occurs to her, and she offers a\n |
| 0x11af4 | 18 | gentle suggestion. |
| 0x11b07 | 46 | Perhaps this is some kind of fate. Why don't\n |
| 0x11b36 | 45 | you let me look after you for a little while? |
| 0x11b64 | 41 | The bizarre idea has me at a brief loss\n |
| 0x11b8e | 10 | for words. |
| 0x11b99 | 37 | This girl's going to take care of me? |
| 0x11bbf | 46 | Oh, no, I couldn't. But I do appreciate the... |
| 0x11bee | 12 | ...No, wait. |
| 0x11bfb | 46 | If I go off on my own here, I'm either going\n |
| 0x11c2a | 42 | to get lost, or end up as some monster's\n |
| 0x11c55 | 7 | dinner. |
| 0x11c5d | 48 | I'm still unsure, but she's done a lot for me.\n |
| 0x11c8e | 48 | She wouldn't turn on me now--not after all this. |
| 0x11cbf | 47 | I can at least rely on her until I understand\n |
| 0x11cef | 48 | what's going on. I'll just accept this as some\n |
| 0x11d20 | 13 | good fortune. |
| 0x11d2e | 43 | ...Understood. I'll be relying on you, at\n |
| 0x11d5a | 16 | least for a bit. |
| 0x11d6b | 43 | Kuon smiles gently as I bow my head to her. |
| 0x11d97 | 49 | Yes, I think that's a wise choice. Obedience is\n |
| 0x11dc9 | 20 | always a good thing. |
| 0x11dde | 50 | She looks relieved... It's pretty clear if I had\n |
| 0x11e11 | 46 | refused, I probably wouldn't have made it on\n |
| 0x11e40 | 9 | my own... |
| 0x11e4a | 42 | Well, now that that's settled, we should\n |
| 0x11e75 | 34 | at least decide on a name for you. |
| 0x11e98 | 10 | ...A name? |
| 0x11ea3 | 44 | Well, you can't stay nameless forever. You\n |
| 0x11ed0 | 41 | can't remember what you're called, right? |
| 0x11efa | 7 | Yeah... |
| 0x11f02 | 46 | She has a point. Not having a name could get\n |
| 0x11f31 | 45 | inconvenient, especially when we get to town. |
| 0x11f5f | 26 | OK, anything's probably... |
| 0x11f7a | 8 | Hold on. |
| 0x11f83 | 38 | Maybe... this is a golden opportunity? |
| 0x11faa | 45 | I'm not happy about having no memories, but\n |
| 0x11fd8 | 46 | it DOES mean I've basically got a clean slate. |
| 0x12007 | 46 | Which brings us to this... I can pick myself\n |
| 0x12036 | 34 | a really cool and mysterious name! |
| 0x12059 | 45 | Maybe my name was something bland and dull,\n |
| 0x12087 | 16 | before all this. |
| 0x12098 | 47 | Well, that's not so bad. Could just as easily\n |
| 0x120c8 | 36 | have been something ridiculous and\n |
| 0x120ed | 15 | embarrassing... |
| 0x120fd | 43 | You know what, amnesia's not so bad. It's\n |
| 0x12129 | 45 | awesome, even! Gotta make the best of a bad\n |
| 0x12157 | 10 | situation. |
| 0x12162 | 43 | So this is a real opportunity. Can't just\n |
| 0x1218e | 25 | go with some random name. |
| 0x121a8 | 45 | Just have to think of a name cool enough to\n |
| 0x121d6 | 44 | make people jealous, but not something I'd\n |
| 0x12203 | 15 | regret later... |
| 0x12213 | 16 | OK! My name is-- |
| 0x12224 | 43 | Hmm. What kind of name would suit you best? |
| 0x12250 | 43 | Kuon seems unconcerned by my dramatically\n |
| 0x1227c | 39 | outstretched arm, pondering to herself. |
| 0x122a4 | 46 | An uneasy feeling rises, and I nervously ask\n |
| 0x122d3 | 4 | her. |
| 0x122d8 | 45 | Um... you aren't... planning to think about\n |
| 0x12306 | 25 | my new name too, are you? |
| 0x12320 | 43 | She looks surprised, like she has no idea\n |
| 0x1234c | 16 | what I'm asking. |
| 0x1235d | 26 | Planning to? It's my duty. |
| 0x12378 | 12 | Y-Your duty? |
| 0x12385 | 48 | A guardian is essentially a parent. Since I am\n |
| 0x123b6 | 45 | now your guardian, it's my duty to give you\n |
| 0x123e4 | 7 | a name. |
| 0x123ec | 13 | No, that's... |
| 0x123fa | 48 | Come on... This tiny girl can't honestly think\n |
| 0x1242b | 34 | of herself as my parent, right...? |
| 0x1244e | 50 | Though if you'd prefer to go on your own without\n |
| 0x12481 | 47 | me, then by all means, make your own decisions. |
| 0x124b1 | 12 | U... Urgh... |
| 0x124be | 43 | How can I argue with that...? Kuon smiles\n |
| 0x124ea | 44 | brightly as I sag in defeat, and claps her\n |
| 0x12517 | 6 | hands. |
| 0x1251e | 26 | Then I think it's decided! |
| 0x12539 | 48 | *Sigh*... So much for the whole "awesome name"\n |
| 0x1256a | 7 | idea... |
| 0x12572 | 44 | In the end, I guess I still have no say in\n |
| 0x1259f | 31 | anything--not even my own name. |
| 0x125bf | 35 | Now, let's see. Your new name is... |
| 0x125e3 | 43 | Kuon cocks her head, looking thoughtfully\n |
| 0x1260f | 15 | to the ceiling. |
| 0x1261f | 49 | After a moment of silence, she mutters a couple\n |
| 0x12651 | 10 | syllables. |
| 0x1265c | 11 | Ha... ku... |
| 0x12668 | 8 | Haku...? |
| 0x12671 | 19 | That's right. Haku. |
| 0x12685 | 47 | She seems pretty proud of it. Having said it,\n |
| 0x126b5 | 23 | she smiles confidently. |
| 0x126cd | 44 | I think you should call yourself Haku from\n |
| 0x126fa | 7 | now on. |
| 0x12702 | 7 | Haku... |
| 0x1270a | 42 | I ruminate over this name she's given me.  |
| 0x12735 | 24 | ...It's not that cool... |
| 0x1274e | 25 | ...Did you say something? |
| 0x12768 | 9 | *Shudder* |
| 0x12772 | 46 | A slight shiver runs through me, and a chill\n |
| 0x127a1 | 19 | runs down my spine. |
| 0x127b5 | 50 | Though Kuon is smiling as sweetly as ever at me,\n |
| 0x127e8 | 32 | my blood runs cold for a moment. |
| 0x12809 | 33 | Erk! N-Nope, didn't say a word... |
| 0x1282b | 45 | In response to my reaction, Kuon clears her\n |
| 0x12859 | 38 | throat with a delicate little cough,\n |
| 0x12880 | 19 | speaking seriously. |
| 0x12894 | 31 | It's a very distinguished name. |
| 0x128b4 | 45 | It comes from the name of one celebrated in\n |
| 0x128e2 | 28 | ancient legends and stories. |
| 0x128ff | 10 | Legends... |
| 0x1290a | 30 | Yes... from the Utawarerumono. |
| 0x12929 | 49 | Without any memories or context, I can't really\n |
| 0x1295b | 42 | appreciate or understand the significance. |
| 0x12986 | 50 | But something about the faraway affection in her\n |
| 0x129b9 | 43 | expression tells me it's an important name. |
| 0x129e5 | 12 | All right... |
| 0x129f2 | 30 | From now on, then, I'm Haku.\n |
| 0x12a11 | 32 | Please call me that from now on. |
| 0x12a32 | 30 | Mhm. Glad to hear it, I think. |

## 8. Formato de saida EXIGIDO
Escreva `translations_11_02.json` com a forma:
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
