# Cena ch_16_01 — pacote de traducao (1334 linhas)

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
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Karulau | Personagem | Karulau | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| yacchip | Item | yacchip | manter_original | none |

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
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `...Kuon?` -> `...Kuon?` (Haku, 11_11)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `This one?` -> `Esta aqui?` (Nekone, 14_09)
- `Lady` -> `Lorde` (UI, 14_06)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Is something the matter?` -> `Aconteceu alguma coisa?` (Kuon, 12_09)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `The unusual architecture's to the owner's\n` -> `A arquitetura incomum é do gosto pessoal\n` (Haku, 14_03)
- `personal taste, apparently.` -> `da proprietária, ao que parece.` (Haku, 14_03)
- `Just between us, the proprietress is a drop-dead\n` -> `Só entre nós, a proprietária é de cair o\n` (Ukon, 14_03)
- `gorgeous woman. She's got crazy strength, too.` -> `queixo. E tem uma força absurda também.` (Ukon, 14_03)
- `you.` -> `isso.` (Nekone, 15_03)
- `then.` -> `então.` (Kuon, 13_01)
- `you?` -> `pode?` (Haku, 13_01)
- `sleep...` -> `sono...` (Garota, 12_01)
- `Yes...` -> `Sim...` (Rulutieh, 14_10)
- `Kuon...` -> `Kuon...` (Kuon, 13_02)
- `Haku...` -> `Haku...` (Kuon, 14_09)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Right...` -> `É...` (Ukon, 15_01)
- `but...` -> `mas...` (Kuon, 12_16)
- `Whoa--` -> `Uou--` (Man, root)
- `Girl` -> `Garota` (sistema, 13_01)
- `her face.` -> `ver ela.` (Haku, 14_03)
- `that...` -> `essa...` (Haku, 15_03)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `though.` -> `porém.` (Kuon, 12_04)
- `about it.` -> `sem pensar.` (Haku, 15_01)
- `Urgh--` -> `Argh--` (Man, 13_05)
- `Uh--` -> `Ãh--` (Kuon, root)
- `What's this?` -> `O que é isso?` (Haku, 12_08)
- `What ho?` -> `O que é?` (Maroro, 12_11)
- `the city.` -> `da cidade.` (Haku, 14_02)
- `attitude.` -> `do grupo.` (Kuon, 15_02)
- `now.` -> `já.` (Kuon, 14_04)
- `happened.` -> `acabou de acontecer.` (Kuon, root)
- `people.` -> `pessoas.` (Haku, 15_02)
- `us.` -> `nós.` (Haku, 15_03)
- `things.` -> `faz.` (Nekone, 15_03)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `you, kid.` -> `de você.` (Ukon, 15_01)
- `yeah?` -> `tá?` (Ukon, 14_02)
- `well.` -> `bem.` (Kuon, root)
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `Gah!?` -> `Gah!?` (Haku, 13_01)
- `*WHUMP*` -> `*BAM*` (Haku, 11_07)
- `understand.` -> `entenda.` (Nekone, 15_03)
- `for a bit.` -> `um pouco.` (Ukon, 13_02)
- `here?` -> `afinal?` (Haku, 13_02)
- `person.` -> `terrível.` (Nekone, 15_03)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `y'know.` -> `sabia.` (Ukon, 12_07)
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
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
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
| 0xc59dc | 5 | Hm... |
| 0xc59e2 | 25 | Urgh. Toilet. Gotta go... |
| 0xc59fc | 8 | ...Phew. |
| 0xc5a05 | 48 | Gah, that'll teach me to drink tea before bed.\n |
| 0xc5a36 | 19 | It's cold out here. |
| 0xc5a4a | 9 | *CLATTER* |
| 0xc5a54 | 3 | Hm? |
| 0xc5a58 | 50 | Halfway back to my room from the toilet, a sound\n |
| 0xc5a8b | 42 | from the inn's main entrance distracts me. |
| 0xc5ab6 | 49 | Curious to know what could be making such noise\n |
| 0xc5ae8 | 40 | at this hour, I decide to have a peek... |
| 0xc5b11 | 8 | ...Kuon? |
| 0xc5b1a | 46 | From a distance, I can distinguish the shape\n |
| 0xc5b49 | 36 | of Kuon's back as she slips outside. |
| 0xc5b6e | 46 | What's she doing, leaving the inn this late?\n |
| 0xc5b9d | 45 | Isn't it dangerous to go out alone? What if\n |
| 0xc5bcb | 13 | something...? |
| 0xc5bd9 | 47 | Nah, I shouldn't worry. Kuon can take care of\n |
| 0xc5c09 | 16 | herself, anyway. |
| 0xc5c1a | 13 | Ah... Sleepy. |
| 0xc5c28 | 50 | Well, whatever. Maybe she just wanted to go look\n |
| 0xc5c5b | 48 | at the moon and get some fresh air or something. |
| 0xc5c8c | 46 | As long as I'm out here, I guess I'll have a\n |
| 0xc5cbb | 45 | drink and stargaze before I go back to bed... |
| 0xc7c60 | 13 | ...I'm bored. |
| 0xc7c6e | 46 | It's one of those rare days where, for once,\n |
| 0xc7c9d | 38 | no crisis needs my attention. A free\n |
| 0xc7cc4 | 12 | afternoon... |
| 0xc7cd1 | 41 | Everyone seems to be out of the inn, too. |
| 0xc7cfb | 41 | Kuon went out with Nekone and Rulutieh.\n |
| 0xc7d25 | 46 | They did invite me, but I'm not up for being\n |
| 0xc7d54 | 12 | a pack mule. |
| 0xc7d61 | 48 | Kiwru seemed perfectly happy to go carry stuff\n |
| 0xc7d92 | 31 | for them in my stead, anyway... |
| 0xc7db2 | 47 | Gotta wonder if being treated so dismissively\n |
| 0xc7de2 | 32 | is that guy's kink or something. |
| 0xc7e03 | 28 | Now that I think about it... |
| 0xc7e20 | 32 | I take a sip of tea, ruminating. |
| 0xc7e41 | 35 | We've been calling this place our\n |
| 0xc7e65 | 46 | "headquarters," but I don't really know much\n |
| 0xc7e94 | 21 | about the Hakurokaku. |
| 0xc7eaa | 47 | I guess this is my opportunity to explore the\n |
| 0xc7eda | 42 | place a bit. And who knows? I might find\n |
| 0xc7f05 | 10 | something. |
| 0xc7f10 | 48 | With my mind made up, I venture out of my room\n |
| 0xc7f41 | 21 | and into the hallway. |
| 0xc7f57 | 46 | Huh, it's a lot more spacious back here than\n |
| 0xc7f86 | 19 | I'd have thought... |
| 0xc7f9a | 47 | And all these stairs... It's like a labyrinth\n |
| 0xc7fca | 21 | with multiple floors. |
| 0xc7fe0 | 46 | Well, I guess I'll explore the upper floors,\n |
| 0xc800f | 41 | since I haven't been up there at all yet. |
| 0xc8039 | 47 | The stairs all lead to different places, too.\n |
| 0xc8069 | 49 | Hope I don't get lost. Why would they design it\n |
| 0xc809b | 10 | like this? |
| 0xc80a6 | 41 | I wander around the upper floors of the\n |
| 0xc80d0 | 42 | Hakurokaku, occasionally passing workers\n |
| 0xc80fb | 19 | cleaning the rooms. |
| 0xc810f | 47 | Walking around like this is giving me a sense\n |
| 0xc813f | 46 | for how strangely laid-out this building is... |
| 0xc816e | 21 | What's this place...? |
| 0xc8184 | 47 | Finally, after a long ascent, I emerge into a\n |
| 0xc81b4 | 45 | spacious room with no more stairs that lead\n |
| 0xc81e2 | 7 | upward. |
| 0xc81ea | 47 | Can't go up any more. Is this the top floor...? |
| 0xc821a | 50 | The room's wide windows lie open to the outside.\n |
| 0xc824d | 31 | An observatory of some kind...? |
| 0xc826d | 41 | Wow, that view... I think I can see the\n |
| 0xc8297 | 33 | whole imperial capital from here. |
| 0xc82b9 | 48 | The patterns of greenery in the city's gardens\n |
| 0xc82ea | 43 | are a sight to behold from above like this. |
| 0xc8316 | 39 | Hm. Kuon might appreciate this place.\n |
| 0xc833e | 43 | Guess I'll let her know about it whenever\n |
| 0xc836a | 14 | she gets back. |
| 0xc8379 | 30 | Ah... What a nice day, though. |
| 0xc8398 | 43 | A warm breeze filters in through the open\n |
| 0xc83c4 | 44 | windows, and I stretch my arms with a long\n |
| 0xc83f1 | 5 | sigh. |
| 0xc83f7 | 47 | Not a single cloud mars the perfection of the\n |
| 0xc8427 | 45 | blue sky, and the sun makes the city sparkle. |
| 0xc8455 | 49 | A nice, cold drink to enjoy under the sun would\n |
| 0xc8487 | 30 | be great on a day like this... |
| 0xc84aa | 46 | Might as well go and get something to drink,\n |
| 0xc84d9 | 40 | since I found this place to savor it in. |
| 0xc8502 | 46 | With Kuon and the others gone, it isn't like\n |
| 0xc8531 | 43 | I'm going to get told off for day-drinking. |
| 0xc855d | 23 | Guess I'll head d--huh? |
| 0xc8575 | 47 | Just as I turn to go back to my room, my eyes\n |
| 0xc85a5 | 38 | fall on a strange pattern on the wall. |
| 0xc85cc | 15 | This pattern... |
| 0xc85dc | 47 | Upon closer inspection, it appears to be made\n |
| 0xc860c | 47 | of multiple wooden, interlocking square pieces. |
| 0xc863c | 45 | And it looks... decidedly jumbled. All over\n |
| 0xc866a | 10 | the place. |
| 0xc8675 | 43 | Are the pieces in the wrong order, maybe?\n |
| 0xc86a1 | 37 | I could swear this piece goes here... |
| 0xc86c7 | 7 | *CLACK* |
| 0xc86cf | 9 | It moves? |
| 0xc86d9 | 46 | When I touch a piece of the apparent puzzle,\n |
| 0xc8708 | 39 | it slides ever-so-slightly to the side. |
| 0xc8730 | 18 | Does that mean...? |
| 0xc8743 | 14 | *CLACK, CLICK* |
| 0xc8752 | 47 | If this goes here, and that slides into place\n |
| 0xc8782 | 13 | down there... |
| 0xc8790 | 48 | Is it really a puzzle, then? My curiosity gets\n |
| 0xc87c1 | 43 | the better of me, and I begin to move the\n |
| 0xc87ed | 7 | pieces. |
| 0xc87f5 | 17 | *CLICK, CLACK*... |
| 0xc8807 | 46 | Gradually, the pieces begin to form a proper\n |
| 0xc8836 | 40 | geometric pattern, coaxed out of their\n |
| 0xc885f | 9 | disarray. |
| 0xc8869 | 24 | And that should do it... |
| 0xc8882 | 7 | *CLUNK* |
| 0xc888a | 19 | *Rumble, rumble*... |
| 0xc889e | 3 | Wh- |
| 0xc88a2 | 46 | As the last piece slots into its place, some\n |
| 0xc88d1 | 44 | mechanism triggers, and a staircase slides\n |
| 0xc88fe | 10 | into view. |
| 0xc8909 | 47 | A staircase... So there's another floor above\n |
| 0xc8939 | 9 | this one? |
| 0xc8943 | 35 | This is quite an elaborate setup.\n |
| 0xc8967 | 34 | Now I HAVE to see what's up there. |
| 0xc898a | 44 | I hesitate only a moment, failing to fight\n |
| 0xc89b7 | 44 | down my curiosity as I ascend the revealed\n |
| 0xc89e4 | 6 | steps. |
| 0xc89eb | 47 | A faintly sweet-smelling fragrance wafts down\n |
| 0xc8a1b | 13 | the stairs... |
| 0xc8a29 | 48 | Hm? Ah, that... That smells nice. Some kind of\n |
| 0xc8a5a | 8 | incense? |
| 0xc8a63 | 10 | This is... |
| 0xc8a6e | 47 | The stairs emerge into a room filled with the\n |
| 0xc8a9e | 32 | smoke of the mysterious incense. |
| 0xc8abf | 47 | Though dark, my eyes quickly grow accustomed,\n |
| 0xc8aef | 46 | and I can tell the room is furnished lavishly. |
| 0xc8b1e | 43 | I thought I would find an unused attic or\n |
| 0xc8b4a | 25 | something up here, but... |
| 0xc8b64 | 48 | ...Maybe I shouldn't have come up here without\n |
| 0xc8b95 | 11 | permission. |
| 0xc8ba1 | 31 | Well, now. Do I have a visitor? |
| 0xc8bc1 | 6 | Bwuh!? |
| 0xc8bc8 | 43 | In a corner of the room draped with furs,\n |
| 0xc8bf4 | 47 | a beautiful, elegantly-dressed woman reclines\n |
| 0xc8c24 | 11 | on a couch. |
| 0xc8c30 | 46 | She has an alluring, graceful air about her,\n |
| 0xc8c5f | 41 | coiled and composed like a self-assured\n |
| 0xc8c89 | 9 | predator. |
| 0xc8c93 | 43 | The sight is enough to take me off guard,\n |
| 0xc8cbf | 46 | enamored for a fleeting moment. She sips her\n |
| 0xc8cee | 6 | drink. |
| 0xc8cf5 | 34 | That looks good, whatever it is.\n |
| 0xc8d18 | 17 | Wish I had a cup. |
| 0xc8d2a | 4 | Lady |
| 0xc8d2f | 32 | Did you have some business here? |
| 0xc8d50 | 42 | O-Oh, uh, no. Sorry for entering without\n |
| 0xc8d7b | 47 | I'm not up to anything shady, promise--I just\n |
| 0xc8dab | 42 | sort of... wandered in here. I'll excuse\n |
| 0xc8dd6 | 11 | myself now. |
| 0xc8de2 | 44 | Mm. Hm hm. There's no need to be in such a\n |
| 0xc8e0f | 6 | hurry. |
| 0xc8e16 | 47 | Halfway to the door, the woman's amused laugh\n |
| 0xc8e46 | 15 | gives me pause. |
| 0xc8e56 | 23 | How about this instead? |
| 0xc8e6e | 31 | She tosses something toward me. |
| 0xc8e8e | 46 | I almost drop it in my surprise, but somehow\n |
| 0xc8ebd | 43 | manage to recover and maintain a good grip. |
| 0xc8ee9 | 12 | Um... A cup? |
| 0xc8ef6 | 42 | There are rules to this place, you know.\n |
| 0xc8f21 | 44 | Any who enter must partake in at least one\n |
| 0xc8f4e | 14 | drink with me. |
| 0xc8f5d | 44 | You have entered, and so the rules must be\n |
| 0xc8f8a | 9 | observed. |
| 0xc8f94 | 7 | ...Huh? |
| 0xc8f9c | 44 | What is this awesome rule? Drinking in the\n |
| 0xc8fc9 | 38 | middle of the day? Outrageous, surely. |
| 0xc8ff0 | 45 | Of course, I don't want to break the rules,\n |
| 0xc901e | 45 | so I GUESS I have no choice. I'll just have\n |
| 0xc904c | 9 | to drink. |
| 0xc9056 | 44 | I quickly step over to the couch and avail\n |
| 0xc9083 | 38 | myself of an odd-shaped bottle nearby. |
| 0xc90aa | 48 | Oh, come now. I'm not a barbarian. It would be\n |
| 0xc90db | 43 | uncouth to make a guest pour his own drink. |
| 0xc9107 | 43 | The woman takes the bottle from my hands,\n |
| 0xc9133 | 33 | tilting it toward me in offering. |
| 0xc9155 | 43 | Shall we start with just the one cup, then? |
| 0xc9181 | 14 | ...Whoa, whoa. |
| 0xc9190 | 47 | Her graceful, honest air catches me off-guard\n |
| 0xc91c0 | 40 | once again, and my cup nearly overflows. |
| 0xc91e9 | 28 | Welp. Without further ado... |
| 0xc9206 | 44 | I bring the cup to my lips and drink deeply. |
| 0xc9233 | 29 | Ahh... That's the good stuff. |
| 0xc9251 | 42 | Smooth, rich flavors, faintly sweet, and\n |
| 0xc927c | 46 | refreshing brightness, to say nothing of the\n |
| 0xc92ab | 8 | scent... |
| 0xc92b4 | 47 | Whew. This, truly, is the meaning of enjoying\n |
| 0xc92e4 | 25 | something to its fullest. |
| 0xc92fe | 41 | I wonder what kind of alcohol this is...? |
| 0xc9328 | 49 | I would say I've never tasted anything like it,\n |
| 0xc935a | 31 | but it's a... nostalgic flavor? |
| 0xc937a | 46 | I've definitely had this before, but where...? |
| 0xc93a9 | 13 | What is this? |
| 0xc93b7 | 45 | Mm, you like it? It's nothing less than the\n |
| 0xc93e5 | 42 | crown jewel of my reserves. A masterpiece. |
| 0xc9410 | 46 | It's foreign in origin, of course, so it may\n |
| 0xc943f | 21 | taste strange to you. |
| 0xc9455 | 8 | Foreign? |
| 0xc945e | 46 | I almost remember something, but the alcohol\n |
| 0xc948d | 46 | slowly begins to take effect, and the memory\n |
| 0xc94bc | 11 | evaporates. |
| 0xc94c8 | 24 | Is something the matter? |
| 0xc94e1 | 21 | It's nothing, just... |
| 0xc94f7 | 39 | I think I've had this somewhere before. |
| 0xc951f | 41 | I don't really remember it, but it's...\n |
| 0xc9549 | 15 | just a feeling. |
| 0xc9559 | 9 | ...I see. |
| 0xc9563 | 44 | The woman gives a small, quiet smile, then\n |
| 0xc9590 | 44 | gracefully tilts her cup back and drains it. |
| 0xc95bd | 51 | After seeing that, I pick up the bottle and offer\n |
| 0xc95f1 | 25 | it towards her empty cup. |
| 0xc960b | 7 | Hmhm... |
| 0xc9613 | 47 | I was curious as to what kind of man you are,\n |
| 0xc9643 | 49 | you know. I'm pleased to find you good drinking\n |
| 0xc9675 | 8 | company. |
| 0xc967e | 23 | Huh? You know who I am? |
| 0xc9696 | 45 | Nothing that goes on in this inn escapes my\n |
| 0xc96c4 | 47 | notice. You've been the talk of my employees,\n |
| 0xc96f4 | 9 | you know. |
| 0xc96fe | 26 | ...Talk of your employees? |
| 0xc9719 | 27 | What does she mean by that? |
| 0xc9735 | 44 | To hear them talk, it seems a man of great\n |
| 0xc9762 | 49 | wealth has moved in, said to be especially fond\n |
| 0xc9794 | 11 | of baths... |
| 0xc97a0 | 46 | They also whisper of a menacing nugwisomkami\n |
| 0xc97cf | 46 | that threatens to devour the kitchen's whole\n |
| 0xc97fe | 7 | larder. |
| 0xc9806 | 43 | Wait, wait, hold on. That's definitely my\n |
| 0xc9832 | 38 | partner they're talking about, not me. |
| 0xc9859 | 47 | I genuinely had no idea rumors like that were\n |
| 0xc9889 | 26 | spreading among the staff. |
| 0xc98a4 | 46 | I guess it's only natural, when you consider\n |
| 0xc98d3 | 47 | her appetite and the time she spends bathing... |
| 0xc9903 | 44 | Ah, is that so? Then you're her companion,\n |
| 0xc9930 | 6 | or...? |
| 0xc9937 | 3 | Or? |
| 0xc993b | 12 | Mm, nothing. |
| 0xc9948 | 49 | ...I don't know why, but now I'm really curious\n |
| 0xc997a | 32 | as to what she was going to say. |
| 0xc999b | 49 | Maybe it's a little late to be asking this now,\n |
| 0xc99cd | 31 | but... just who is this person? |
| 0xc99ed | 43 | Judging by the luxurious room, the hidden\n |
| 0xc9a19 | 41 | entryway, the fact that it's on the top\n |
| 0xc9a43 | 8 | floor... |
| 0xc9a4c | 43 | The unusual architecture's to the owner's\n |
| 0xc9a78 | 27 | personal taste, apparently. |
| 0xc9a94 | 50 | Just between us, the proprietress is a drop-dead\n |
| 0xc9ac7 | 46 | gorgeous woman. She's got crazy strength, too. |
| 0xc9af6 | 48 | This woman must be the owner of the Hakurokaku\n |
| 0xc9b27 | 4 | Inn. |
| 0xc9b2c | 46 | That she said "my employees" and knows about\n |
| 0xc9b5b | 47 | everything in the inn only makes me more sure\n |
| 0xc9b8b | 8 | of that. |
| 0xc9b94 | 48 | What bugs me more are the vibes I keep getting\n |
| 0xc9bc5 | 13 | off of her... |
| 0xc9bd3 | 38 | She reminds me of someone, but who...? |
| 0xc9bfa | 30 | Is there something on my face? |
| 0xc9c19 | 18 | Oh... S-Sorry, no. |
| 0xc9c2c | 30 | Crap. I was staring, wasn't I? |
| 0xc9c4b | 47 | Ah, but how rude of me. I've yet to introduce\n |
| 0xc9c7b | 48 | myself. You may call me Karulau, if it pleases\n |
| 0xc9cac | 4 | you. |
| 0xc9cb1 | 43 | Karulau... I guess it was my imagination.\n |
| 0xc9cdd | 33 | I don't know anyone by that name. |
| 0xc9cff | 13 | I go by Haku. |
| 0xc9d0d | 8 | ...Haku? |
| 0xc9d16 | 40 | That's... quite a rare name, these days. |
| 0xc9d3f | 41 | Yeah, well. It sounds pretty simple and\n |
| 0xc9d69 | 12 | bland to me. |
| 0xc9d76 | 48 | It's not a name from around here, that much is\n |
| 0xc9da7 | 44 | certain--and parents avoid using it in its\n |
| 0xc9dd4 | 9 | homeland. |
| 0xc9dde | 20 | ...What do you mean? |
| 0xc9df3 | 48 | It's the name of a great, beloved owlo in that\n |
| 0xc9e24 | 46 | country. A household name, one even children\n |
| 0xc9e53 | 8 | respect. |
| 0xc9e5c | 48 | It would be as if a Yamatan parent named their\n |
| 0xc9e8d | 47 | child after the Mikado himself. A name beyond\n |
| 0xc9ebd | 8 | station. |
| 0xc9ec6 | 45 | Now that I think about it, Kuon did say she\n |
| 0xc9ef4 | 35 | got my name from a famous person... |
| 0xc9f18 | 29 | Wonder why she decided on it. |
| 0xc9f36 | 41 | That girl... gave you that name, did she? |
| 0xc9f60 | 45 | Yeah. When she found me, I was an amnesiac.\n |
| 0xc9f8e | 46 | Having no name would be inconvenient, so she\n |
| 0xc9fbd | 12 | gave me one. |
| 0xc9fca | 45 | ...I guess there isn't really any reason to\n |
| 0xc9ff8 | 37 | hide that. It won't hurt to tell her. |
| 0xca01e | 33 | Is that... so? Your memories...\n |
| 0xca040 | 36 | That must be very difficult for you. |
| 0xca065 | 16 | Well, I guess... |
| 0xca076 | 46 | I mean, the first thing I remember is almost\n |
| 0xca0a5 | 49 | getting eaten by a gigiri and a Tatari, in that\n |
| 0xca0d7 | 6 | order. |
| 0xca0de | 46 | I thought I was saved, but then I was forced\n |
| 0xca10d | 41 | to walk until my legs seized with pain... |
| 0xca137 | 47 | I don't know how many times I said I couldn't\n |
| 0xca167 | 15 | go on any more. |
| 0xca177 | 44 | It appears you've endured quite an ordeal,\n |
| 0xca1a4 | 5 | then. |
| 0xca1aa | 37 | You seem to have led a rather amu--\n |
| 0xca1d0 | 46 | Ahem, eventful life. Would you be opposed to\n |
| 0xca1ff | 21 | sharing more details? |
| 0xca215 | 50 | Being pent up in a place like this all the time,\n |
| 0xca248 | 49 | it's hard to come by entert--ah, stories of the\n |
| 0xca27a | 6 | world. |
| 0xca281 | 39 | ...The way she says it kinda bugs me,\n |
| 0xca2a9 | 19 | but whatever. Sure. |
| 0xca2bd | 43 | ...And after we dispatched the gigiri, we\n |
| 0xca2e9 | 44 | decided to head for the capital together--\n |
| 0xca316 | 23 | whoop, that's enough... |
| 0xca32e | 48 | Karulau nods along with my story, refilling my\n |
| 0xca35f | 44 | cup with impeccable timing as it runs empty. |
| 0xca38c | 49 | Through the whole retelling of the gigiri hunt,\n |
| 0xca3be | 46 | she's been wordlessly keeping me topped off... |
| 0xca3ed | 47 | And on the road to the capital, of course, we\n |
| 0xca41d | 46 | end up fighting a group of bandits and their\n |
| 0xca44c | 6 | chief. |
| 0xca453 | 47 | Seriously, why does this stuff keep happening\n |
| 0xca483 | 6 | to me? |
| 0xca48a | 46 | I have a feeling you're just the sort of man\n |
| 0xca4b9 | 20 | who attracts danger. |
| 0xca4ce | 44 | It's a rare fate, but not unheard of. Some\n |
| 0xca4fb | 46 | people are born under odd stars, destined to\n |
| 0xca52a | 15 | lead odd lives. |
| 0xca53a | 45 | Stars? Fate? Not sure if I put any stock in\n |
| 0xca568 | 11 | all that... |
| 0xca574 | 48 | You believe such things are absurdities, don't\n |
| 0xca5a5 | 4 | you? |
| 0xca5aa | 46 | But sometimes they're all we have to explain\n |
| 0xca5d9 | 47 | the inexplicable. I'm sure you know all about\n |
| 0xca609 | 7 | it, hm? |
| 0xca611 | 22 | Urgh. Give me a break. |
| 0xca628 | 47 | Although... Now that she frames it like that,\n |
| 0xca658 | 47 | maybe fate IS to blame for how my life's been\n |
| 0xca688 | 6 | going. |
| 0xca68f | 49 | Of course, it's not all bad. Poor fortune isn't\n |
| 0xca6c1 | 35 | all that's attracted to you, is it? |
| 0xca6e5 | 47 | It's also been facilitating meetings, putting\n |
| 0xca715 | 46 | you in the paths of those you now hold dear... |
| 0xca744 | 34 | An enviable quality, to be sure.\n |
| 0xca767 | 15 | And a rare one. |
| 0xca777 | 42 | My cup fills again just as quickly as it\n |
| 0xca7a2 | 8 | emptied. |
| 0xca7ab | 29 | Yooouuuu really think sho...? |
| 0xca7c9 | 31 | Urk. Alcohol's getting to me.\n |
| 0xca7e9 | 41 | I can't seem to form my words properly... |
| 0xca813 | 32 | Sssho, where did I leave off...? |
| 0xca834 | 46 | Ahh... Mmrgnh. Sleepy... Maybe I got carried\n |
| 0xca863 | 30 | away with the expensive booze. |
| 0xca882 | 41 | Is something the matter? You've stopped\n |
| 0xca8ac | 9 | drinking. |
| 0xca8b6 | 14 | Oh... right... |
| 0xca8c5 | 31 | Oh, my. Asleep already, are we? |
| 0xca8e5 | 45 | Hm hm. Such an innocent expression when you\n |
| 0xca913 | 8 | sleep... |
| 0xca91c | 6 | Yes... |
| 0xca923 | 40 | That gift you hold is a rare one indeed. |
| 0xca94c | 45 | The same gift, I think, as the man you take\n |
| 0xca97a | 17 | your name from... |
| 0xca98c | 43 | It can only be fate that led you to meet.\n |
| 0xca9b8 | 47 | Yes, you were destined to cross one another's\n |
| 0xca9e8 | 8 | paths... |
| 0xca9f1 | 42 | Everything in its proper place and time,\n |
| 0xcaa1c | 28 | predetermined by providence. |
| 0xcaa39 | 49 | What paths does fate hold for you from here on,\n |
| 0xcaa6b | 12 | I wonder...? |
| 0xcaa78 | 48 | Will you become a conqueror, plunging the land\n |
| 0xcaaa9 | 46 | into turmoil as you recklessly make your wars? |
| 0xcaad8 | 48 | Or... perhaps you will shoulder the burdens of\n |
| 0xcab09 | 42 | the many, and rule with kindness and love. |
| 0xcab34 | 33 | I thought I could hear a voice... |
| 0xcab56 | 42 | It tickled my ears, whispering pleasantly. |
| 0xcab81 | 34 | It... felt soft. Like Kuon's tail. |
| 0xcaba4 | 47 | Oh... That was it. That's... who she reminded\n |
| 0xcabd4 | 6 | me of. |
| 0xcabdb | 7 | Kuon... |
| 0xcabe3 | 43 | When I awaken, I find myself in my own bed. |
| 0xcac0f | 29 | ...Was all that just a dream? |
| 0xcac2d | 46 | A familiar, oddly-shaped bottle sitting next\n |
| 0xcac5c | 36 | to the water pitcher begs to differ. |
| 0xcc449 | 16 | Late at night... |
| 0xcc45a | 42 | Kiwru and I make our patrol of the city,\n |
| 0xcc485 | 49 | keeping a wary eye out for fires and suspicious\n |
| 0xcc4b7 | 8 | figures. |
| 0xcc4c0 | 44 | Gah, but it's cold... Working for free was\n |
| 0xcc4ed | 46 | never my cup of tea, especially in this chill. |
| 0xcc51c | 46 | But this is our duty! It falls to us to help\n |
| 0xcc54b | 26 | maintain the public peace. |
| 0xcc566 | 47 | You're earnest to a fault, y'know. Try saying\n |
| 0xcc596 | 45 | that to the others, in their warm beds back\n |
| 0xcc5c4 | 11 | at the inn. |
| 0xcc5d0 | 41 | It's no coincidence Kuon and the others\n |
| 0xcc5fa | 39 | assigned this job to us, conveniently\n |
| 0xcc622 | 21 | exempting themselves. |
| 0xcc638 | 46 | Under the pretext of "sharing the workload,"\n |
| 0xcc667 | 44 | we've been stuck with patrols and they get\n |
| 0xcc694 | 12 | beauty rest. |
| 0xcc6a1 | 47 | And with this weather... Sheesh, we've really\n |
| 0xcc6d1 | 34 | drawn the short straw on this one. |
| 0xcc6f4 | 45 | It certainly is chilly. I just hope none of\n |
| 0xcc722 | 40 | the usual drunks pass out in the cold... |
| 0xcc74b | 44 | I could go for a drink, myself. I would've\n |
| 0xcc778 | 42 | brought some sake, had I known about the\n |
| 0xcc7a3 | 8 | weather. |
| 0xcc7ac | 46 | You shouldn't patrol drunk! What state would\n |
| 0xcc7db | 43 | that leave you in if something needs your\n |
| 0xcc807 | 10 | attention? |
| 0xcc812 | 32 | Kiwru smiles wryly as he speaks. |
| 0xcc833 | 46 | Well, think of it this way. The cold impedes\n |
| 0xcc862 | 33 | how effectively we patrol, right? |
| 0xcc884 | 49 | Wouldn't it make us more efficient peacekeepers\n |
| 0xcc8b6 | 47 | if we had a drink to warm us up and raise our\n |
| 0xcc8e6 | 8 | spirits? |
| 0xcc8ef | 5 | Eh... |
| 0xcc8f5 | 44 | So, in light of that reasoning, you should\n |
| 0xcc922 | 18 | lend me some cash. |
| 0xcc935 | 10 | What? Why? |
| 0xcc940 | 38 | They made me leave my wallet behind.\n |
| 0xcc967 | 29 | It's not like I had a choice. |
| 0xcc985 | 7 | Haku... |
| 0xcc98d | 34 | Don't give me that pitying look.\n |
| 0xcc9b0 | 8 | Come on. |
| 0xcc9b9 | 46 | All right. I'm a little hungry myself, so if\n |
| 0xcc9e8 | 46 | it's only a light drink... Let's find a place. |
| 0xcca17 | 27 | ...Y'know what, never mind. |
| 0xcca33 | 4 | Huh? |
| 0xcca38 | 44 | Nngh. I know I'm the one who suggested it,\n |
| 0xcca65 | 29 | but now I just feel pathetic. |
| 0xcca83 | 28 | Let's keep patrolling, then. |
| 0xccaa0 | 48 | In the end, the cold continues to relentlessly\n |
| 0xccad1 | 7 | bite... |
| 0xccad9 | 46 | Just then, something catches my eye--a straw\n |
| 0xccb08 | 35 | mat, left out to dry and forgotten. |
| 0xccb2c | 29 | Well, now. There's an idea... |
| 0xccb4a | 45 | Um, Haku? What are you going to do with that? |
| 0xccb78 | 45 | What? Waste not, want not. It's just common\n |
| 0xccba6 | 7 | wisdom. |
| 0xccbae | 44 | I wrap the borrowed mat about my shoulders\n |
| 0xccbdb | 15 | like a cloak... |
| 0xccbeb | 32 | Phew, this'll insulate me a bit. |
| 0xccc0c | 47 | Hey, don't look at me like that. I'm freezing\n |
| 0xccc3c | 24 | half to death over here. |
| 0xccc55 | 45 | At this rate, YOU'RE the one who's going to\n |
| 0xccc83 | 36 | attract suspicion dressed like that. |
| 0xccca8 | 46 | What are you talking about? A true gentleman\n |
| 0xcccd7 | 48 | can make anything work for his outfit, if worn\n |
| 0xccd08 | 10 | stylishly. |
| 0xccd13 | 41 | ...I give up. I can't keep up with your\n |
| 0xccd3d | 28 | extremely positive thinking. |
| 0xccd5a | 41 | You should work on that, then. Practice\n |
| 0xccd84 | 41 | thoughts like that every day, if you can. |
| 0xccdae | 8 | Right... |
| 0xccdb7 | 3 | Hm? |
| 0xccdbb | 38 | Stop right there! You're under arrest! |
| 0xccde2 | 19 | ...What's all this? |
| 0xccdf6 | 49 | Sounds like bandits. It came from over there...\n |
| 0xcce28 | 20 | We should go assist. |
| 0xcce3d | 47 | No, we shouldn't. Everyone has their assigned\n |
| 0xcce6d | 39 | patrol route. We need to stick to ours. |
| 0xcce95 | 6 | But... |
| 0xcce9c | 49 | What if we leave our post and something happens\n |
| 0xccece | 39 | here without us? We can't move around\n |
| 0xccef6 | 11 | carelessly. |
| 0xccf02 | 46 | You're... You're right. We'd best patrol the\n |
| 0xccf31 | 47 | area we're assigned. It would be imprudent to\n |
| 0xccf61 | 11 | abandon it. |
| 0xccf6d | 47 | That's right. I'm not trying to weasel out of\n |
| 0xccf9d | 45 | something tiresome--it's just the safer play. |
| 0xccfcf | 50 | Then, all at once, a figure seems to materialize\n |
| 0xcd002 | 47 | from nothing as it bolts toward us around the\n |
| 0xcd032 | 7 | corner. |
| 0xcd03a | 6 | Whoa-- |
| 0xcd041 | 17 | Gh--Who are you!? |
| 0xcd053 | 4 | Girl |
| 0xcd058 | 49 | I'm sorry, but could you help me out? I'm being\n |
| 0xcd08a | 38 | chased by some awfully unpleasant men. |
| 0xcd0b1 | 48 | Going by her voice, she sounds to be a woman--\n |
| 0xcd0e2 | 47 | but she hides in the shadows before I can see\n |
| 0xcd112 | 9 | her face. |
| 0xcd11c | 13 | Capital guard |
| 0xcd12a | 47 | You there! Did anyone suspicious pass through\n |
| 0xcd15a | 14 | here just now? |
| 0xcd169 | 44 | A group of capital guards appears in short\n |
| 0xcd196 | 48 | order, tromping through the streets with heavy\n |
| 0xcd1c7 | 10 | footsteps. |
| 0xcd1d2 | 46 | She said she was being chased by "unpleasant\n |
| 0xcd201 | 34 | men," but it's these guys, huh...? |
| 0xcd224 | 48 | They're definitely capital guards, not ruffians. |
| 0xcd255 | 46 | Which means... I should turn her in to them,\n |
| 0xcd284 | 22 | right? Or... No, wait. |
| 0xcd29b | 47 | I only caught a momentary glimpse of her, but\n |
| 0xcd2cb | 48 | I'm fairly sure I've seen her before. She's...\n |
| 0xcd2fc | 7 | that... |
| 0xcd304 | 28 | I see. If that's the case... |
| 0xcd321 | 10 | Um, well-- |
| 0xcd32c | 46 | Eh, no one unusual. Why? Did something happen? |
| 0xcd35b | 7 | Huh...? |
| 0xcd363 | 46 | We're tracking a suspect spotted fleeing the\n |
| 0xcd392 | 46 | scene of a storehouse robbery. Have you seen\n |
| 0xcd3c1 | 9 | anything? |
| 0xcd3cb | 44 | Now that you mention it, I did hear pretty\n |
| 0xcd3f8 | 46 | frantic footsteps over that way. That's all,\n |
| 0xcd427 | 7 | though. |
| 0xcd42f | 49 | That's probably our thief. There's no mistaking\n |
| 0xcd461 | 10 | it, right? |
| 0xcd46c | 47 | Mm, well. To the best of my memory, they took\n |
| 0xcd49c | 29 | off down that alleyway there. |
| 0xcd4ba | 45 | All right, then we'll pursue. Thank you for\n |
| 0xcd4e8 | 25 | your assistance, citizen. |
| 0xcd502 | 43 | The guard turns to run in the direction I\n |
| 0xcd52e | 44 | indicated, then pauses and turns back to me. |
| 0xcd55b | 48 | Oh, and citizen? If you've no work, you should\n |
| 0xcd58c | 44 | visit the job placement office when you can. |
| 0xcd5b9 | 43 | The guard avoids looking at the straw mat\n |
| 0xcd5e5 | 18 | wrapped around me. |
| 0xcd5f8 | 47 | I know you've got stuff to say, but I have my\n |
| 0xcd628 | 8 | reasons. |
| 0xcd631 | 40 | I don't think the mat was a good idea.\n |
| 0xcd65a | 42 | I-I think they mistook you for a beggar... |
| 0xcd685 | 22 | ...Yeah, you're right. |
| 0xcd69c | 36 | Thank you. You both did wonderfully. |
| 0xcd6c1 | 47 | As the guards' booted footfalls grow more and\n |
| 0xcd6f1 | 48 | more distant, the girl peeks out of her cover,\n |
| 0xcd722 | 5 | wary. |
| 0xcd728 | 48 | I should thank you properly. I'll never forget\n |
| 0xcd759 | 11 | this favor. |
| 0xcd765 | 42 | I thought I'd seen her face once before.\n |
| 0xcd790 | 34 | Her name was... Nosuri, that's it. |
| 0xcd7b3 | 44 | I made the right choice after all. Handing\n |
| 0xcd7e0 | 48 | someone working with us to the guards would've\n |
| 0xcd811 | 12 | ended badly. |
| 0xcd81e | 43 | Don't worry about it. I had my own reasons. |
| 0xcd84a | 8 | Reasons? |
| 0xcd853 | 40 | By "reasons," surely you don't mean...\n |
| 0xcd87c | 21 | You know who I am...? |
| 0xcd892 | 25 | Well, you could say that. |
| 0xcd8ac | 48 | I see. You recognized me and hoped to preserve\n |
| 0xcd8dd | 48 | my freedom... All my hard work hasn't been for\n |
| 0xcd90e | 7 | naught. |
| 0xcd916 | 43 | Misunderstanding, Nosuri looks at me with\n |
| 0xcd942 | 48 | grateful eyes, moved to the point of her voice\n |
| 0xcd973 | 9 | wavering. |
| 0xcd97d | 45 | You'd best get out of here before too long.\n |
| 0xcd9ab | 16 | They'll be back. |
| 0xcd9bc | 37 | Yes, I'll be away shortly. But you... |
| 0xcd9e2 | 46 | Hm. So even in the affluence of the capital,\n |
| 0xcda11 | 42 | there are those who live in the shadows... |
| 0xcda3c | 46 | My mission hasn't been in error, after all...! |
| 0xcda6b | 45 | To live so honorably, even as a poor man...\n |
| 0xcda99 | 48 | For the sake of people like you, I will strive\n |
| 0xcdaca | 11 | yet harder. |
| 0xcdad6 | 47 | Nosuri sheds a dramatic tear, then produces a\n |
| 0xcdb06 | 26 | small bag from her pocket. |
| 0xcdb21 | 46 | Here, friend. Use this to eat something warm\n |
| 0xcdb50 | 19 | on this cold night. |
| 0xcdb64 | 10 | This is... |
| 0xcdb6f | 36 | The bag feels heavy for some reason. |
| 0xcdb94 | 46 | Don't say anything, sir. I know. Even in the\n |
| 0xcdbc3 | 47 | Mikado's own city, the destitute of the world\n |
| 0xcdbf3 | 9 | endure... |
| 0xcdbfd | 47 | Try not to catch a cold in this weather, sir.\n |
| 0xcdc2d | 8 | Be well! |
| 0xcdc36 | 48 | Then, with surprising dexterity, Nosuri nimbly\n |
| 0xcdc67 | 26 | bounds off into the night. |
| 0xcdc82 | 20 | What's with the bag? |
| 0xcdc97 | 21 | No idea. Feels heavy. |
| 0xcdcad | 50 | I loosen the bag's drawstrings to find... money.\n |
| 0xcdce0 | 47 | A LOT of money. The bag is stuffed to the brim. |
| 0xcdd10 | 48 | ...Um. So she was a bandit, right? A fugitive?\n |
| 0xcdd41 | 43 | Is it OK that we just let her off the hook? |
| 0xcdd6d | 26 | Yeah. I've got my reasons. |
| 0xcdd88 | 47 | Oshtor's aware of her, so it ought to be just\n |
| 0xcddb8 | 5 | fine. |
| 0xcddbe | 45 | B-Brother knows of her...? That's OK, then,\n |
| 0xcddec | 39 | but what are you going to do with that? |
| 0xcde14 | 42 | I regard the bag lying open in my hands.\n |
| 0xcde3f | 46 | It's... really not a small amount. This is a\n |
| 0xcde6e | 16 | fat wad of cash. |
| 0xcde7f | 46 | Isn't that... the money stolen in the robbery? |
| 0xcdeae | 44 | I doubt it would look good if we have that\n |
| 0xcdedb | 28 | when the guards come back... |
| 0xcdef8 | 46 | ...In that case, I'll leave it in your care,\n |
| 0xcdf27 | 6 | Kiwru. |
| 0xcdf2e | 47 | Huh? N-No! I can't be seen with that; I'll be\n |
| 0xcdf5e | 9 | arrested! |
| 0xcdf68 | 44 | Well, it's not like I can keep it, either!\n |
| 0xcdf95 | 26 | Just hold onto it for now. |
| 0xcdfb0 | 43 | Don't be unreasonable! Y-You do something\n |
| 0xcdfdc | 9 | about it. |
| 0xcdfe6 | 6 | Urgh-- |
| 0xcdfed | 7 | Nngh--! |
| 0xcdff5 | 47 | The coin pouch jingles as we toss it back and\n |
| 0xce025 | 47 | forth frantically, trying to force it on each\n |
| 0xce055 | 6 | other. |
| 0xce05c | 4 | Uh-- |
| 0xce061 | 10 | Wh--Uh oh. |
| 0xce06c | 9 | *Toss*... |
| 0xce076 | 45 | As our struggle continues, someone--I'm not\n |
| 0xce0a4 | 45 | sure who--fumbles the bag, and it sails off\n |
| 0xce0d2 | 14 | into the dark. |
| 0xce0e1 | 40 | Well! We've got a patrol to get back to. |
| 0xce10a | 33 | ...Yeah, let's finish our patrol. |
| 0xce12c | 44 | Alack, how the cold doth bore into my very\n |
| 0xce159 | 41 | bones! To say nothing of the late hour... |
| 0xce183 | 48 | Upon so chill a night as this, a drink to warm\n |
| 0xce1b4 | 42 | the spirit could--Nay, thrift. I must be\n |
| 0xce1df | 8 | thrifty. |
| 0xce1e8 | 40 | GYAH!? Pain! Whence doth this pain come? |
| 0xce211 | 47 | Maroro suddenly flinches, writhing in pain as\n |
| 0xce241 | 35 | a blunt object takes him off-guard. |
| 0xce265 | 41 | Wh-Who? Who would hold such cruelty and\n |
| 0xce28f | 47 | discontent for poor Maroro as to throw stones\n |
| 0xce2bf | 7 | at him? |
| 0xce2c7 | 45 | ...Alas, no voice doth answer. But how now!\n |
| 0xce2f5 | 12 | What's this? |
| 0xce302 | 44 | Wh-Why--such lucre! Wealth beyond compare!\n |
| 0xce32f | 46 | A great hoard of coin, in so plain a vessel... |
| 0xce35e | 44 | Praise the day, blessed coin, for thou art\n |
| 0xce38b | 47 | sufficient to pay Maroro's debts for once and\n |
| 0xce3bb | 7 | always! |
| 0xce3c3 | 36 | Oh, a prescient blessing thou art.\n |
| 0xce3e8 | 44 | Heaven doth smile sweetly upon poor Maroro\n |
| 0xce415 | 19 | this day, forsooth! |
| 0xce429 | 47 | Whence this blessing cometh, so too doth good\n |
| 0xce459 | 42 | fortune fall at last as a mantle o'er my\n |
| 0xce484 | 10 | shoulders. |
| 0xce48f | 29 | Ah, you there. A moment, sir. |
| 0xce4ad | 8 | What ho? |
| 0xce4b6 | 42 | I want you to tell me where you got that\n |
| 0xce4e1 | 11 | money from. |
| 0xce4ed | 44 | Wh-Wherefore dost thou ask? This coin hath\n |
| 0xce51a | 48 | bestowed itself upon me, as befits a gift from\n |
| 0xce54b | 8 | on high. |
| 0xce554 | 48 | ...Very well. I'll hear all the details at the\n |
| 0xce585 | 9 | garrison. |
| 0xce58f | 48 | Wh--Stay thy hands! I told thee, this money is\n |
| 0xce5c0 | 34 | the heavens' own blessing upon me! |
| 0xce5e3 | 31 | All right, let's take him away. |
| 0xce603 | 46 | Dragged by his arms, Maroro is taken away to\n |
| 0xce632 | 29 | the capital guards' garrison. |
| 0xce650 | 46 | I've done naught wrong! 'Tis a blessing from\n |
| 0xce67f | 34 | the heavens, I say! A blessing...! |
| 0xce6a2 | 46 | The scholar's cries fall on deaf ears as the\n |
| 0xce6d1 | 46 | faint light of dawn begins to creep into the\n |
| 0xce700 | 4 | sky. |
| 0xcfed1 | 16 | Kid, you around? |
| 0xcfee2 | 45 | In the middle of a perfectly good afternoon\n |
| 0xcff10 | 44 | of lazing around at our headquarters, Ukon\n |
| 0xcff3d | 8 | pops in. |
| 0xcff46 | 46 | What, another job already? I'd prefer if you\n |
| 0xcff75 | 41 | saved that stuff for when Kuon is around. |
| 0xcff9f | 44 | Nah, that's not it. I've got some business\n |
| 0xcffcc | 43 | with you, kid. Come tag along with me for\n |
| 0xcfff8 | 12 | awhile, huh? |
| 0xd0005 | 40 | Y'know, whenever you make a roundabout\n |
| 0xd002e | 46 | invitation like that, it typically ends with\n |
| 0xd005d | 14 | me in trouble. |
| 0xd006c | 47 | Come on, don't be like that. I was just gonna\n |
| 0xd009c | 46 | go for a little walk, maybe look into one or\n |
| 0xd00cb | 11 | two things. |
| 0xd00d7 | 34 | So, how about it? You coming with? |
| 0xd00fa | 48 | I may be putting my work as Ukon in your guys'\n |
| 0xd012b | 45 | hands, but I'm not about to stop patrolling\n |
| 0xd0159 | 9 | the city. |
| 0xd0163 | 46 | Man, I was gonna take a nap while everyone's\n |
| 0xd0192 | 6 | out... |
| 0xd0199 | 49 | Bah, it's nothing big. We'll walk around a bit,\n |
| 0xd01cb | 44 | grab a drink on the way back. My treat, of\n |
| 0xd01f8 | 7 | course. |
| 0xd0200 | 13 | His treat...? |
| 0xd020e | 43 | Well, if it's just patrolling the area...\n |
| 0xd023a | 46 | I mean, it is JUST patrolling the area, right? |
| 0xd0269 | 26 | Yeah, that's all. Promise. |
| 0xd0284 | 45 | Ukon gives his answer with a nonchalant grin. |
| 0xd02b2 | 48 | All right, all right. How can I say no to you?\n |
| 0xd02e3 | 16 | Let's get going. |
| 0xd02f4 | 28 | Knew you'd come around, kid. |
| 0xd0311 | 46 | Hurry up and get ready. We'll talk on the way. |
| 0xd0340 | 7 | Got it. |
| 0xd0348 | 43 | So, when you say "contraband," you mean...? |
| 0xd0374 | 28 | Hey, sshh. Not so loud, kid. |
| 0xd0391 | 47 | But yeah. Word is they've been sneaking stuff\n |
| 0xd03c1 | 47 | through here, so we're gonna find some answers. |
| 0xd03f1 | 48 | What? You said we were just gonna be patrolling. |
| 0xd0422 | 45 | Yeah, and we're doing this while we patrol.\n |
| 0xd0450 | 33 | See? I didn't lie about anything. |
| 0xd0472 | 9 | You jerk. |
| 0xd047c | 7 | Anyway! |
| 0xd0484 | 44 | To be straight with you, I don't even know\n |
| 0xd04b1 | 37 | what the contraband item actually is. |
| 0xd04d7 | 43 | Heard it was "live" and "fresh," but that\n |
| 0xd0503 | 20 | could mean anything. |
| 0xd0518 | 43 | Live and fresh... Some kind of food, maybe. |
| 0xd0544 | 44 | Or pleasure-seekers smuggling in something\n |
| 0xd0571 | 46 | psychoactive. Herbs or mushrooms of some kind? |
| 0xd05a0 | 46 | All right, I get the gist. Where do I figure\n |
| 0xd05cf | 8 | into it? |
| 0xd05d8 | 42 | Nah, you're good. I just want you to get\n |
| 0xd0603 | 45 | familiar with the faces of folks who run in\n |
| 0xd0631 | 14 | these circles. |
| 0xd0640 | 49 | Just act like you're my buddy. Smile, nod, look\n |
| 0xd0672 | 32 | like you're supposed to be here. |
| 0xd0693 | 46 | Gotta say, though, I'm glad you were the one\n |
| 0xd06c2 | 16 | at headquarters. |
| 0xd06d3 | 46 | Walking around with one of the princesses...\n |
| 0xd0702 | 41 | We'd stick out like big, throbbing sore\n |
| 0xd072c | 7 | thumbs. |
| 0xd0734 | 26 | So you chose me because... |
| 0xd074f | 44 | I'm not trying to say you look like a bum.\n |
| 0xd077c | 47 | You've got a good... I dunno, like a friendly\n |
| 0xd07ac | 9 | attitude. |
| 0xd07b6 | 47 | And you're not bad-looking. You've got a face\n |
| 0xd07e6 | 19 | people wanna trust. |
| 0xd07fa | 38 | I'm not sure if you're insulting me,\n |
| 0xd0821 | 26 | complimenting me, or both. |
| 0xd083c | 48 | As requested, I stick close to Ukon and follow\n |
| 0xd086d | 32 | him through the city after that. |
| 0xd088e | 46 | Ukon's popularity with the city's commonfolk\n |
| 0xd08bd | 43 | becomes more and more apparent as we walk\n |
| 0xd08e9 | 9 | downtown. |
| 0xd08f3 | 9 | Townsfolk |
| 0xd08fd | 39 | Ah! If it isn't Ukon. Long time no see! |
| 0xd0925 | 48 | Master Ukon! I haven't thanked you for all you\n |
| 0xd0956 | 27 | did for me the other day... |
| 0xd0972 | 23 | Hey, look! Ukon's here! |
| 0xd098a | 24 | Ukon, come play with us! |
| 0xd09a3 | 49 | I've just finished off a fresh batch of mamutu.\n |
| 0xd09d5 | 29 | Here, don't be shy--take one. |
| 0xd09f3 | 39 | Oh, have some dango with it, as well!\n |
| 0xd0a1b | 23 | Here, this one's fresh. |
| 0xd0a33 | 47 | Really, now? Thanks. I'll help myself, if you\n |
| 0xd0a63 | 7 | insist. |
| 0xd0a6b | 44 | Why don't you rest your heels here awhile?\n |
| 0xd0a98 | 20 | I'll put the tea on. |
| 0xd0aad | 44 | Thanks for the offer, but I'm a little bit\n |
| 0xd0ada | 38 | busy. This here's my friend from the\n |
| 0xd0b01 | 17 | countryside, see. |
| 0xd0b13 | 48 | He just arrived in the capital, so I'm showing\n |
| 0xd0b44 | 48 | him around the place. Can't stop to chat right\n |
| 0xd0b75 | 4 | now. |
| 0xd0b7a | 36 | Ah, that's a shame. Maybe next time. |
| 0xd0b9f | 44 | I'll drop by for tea later. For right now,\n |
| 0xd0bcc | 40 | though... You guys hear anything lately? |
| 0xd0bf5 | 44 | The kid's been asking if I've got any good\n |
| 0xd0c22 | 42 | stories. Y'know, strange stuff that only\n |
| 0xd0c4d | 13 | happens here. |
| 0xd0c5b | 46 | That's how he's doing this, huh? Guess I can\n |
| 0xd0c8a | 15 | play my part... |
| 0xd0c9a | 49 | Yeah, I can't get enough of those. I was hoping\n |
| 0xd0ccc | 46 | for more juicy gossip about the capital, but\n |
| 0xd0cfb | 11 | Ukon's out. |
| 0xd0d07 | 46 | Bahaha! Well, I've been away for a long time\n |
| 0xd0d36 | 25 | ...Heard anything, eh...? |
| 0xd0d50 | 44 | Well, this place's nice and quiet with you\n |
| 0xd0d7d | 49 | around, Ukon. Nothing too out of the ordinary's\n |
| 0xd0daf | 9 | happened. |
| 0xd0db9 | 41 | Guess I'll try the other neighborhoods.\n |
| 0xd0de3 | 43 | I'm looking for something to really leave\n |
| 0xd0e0f | 14 | an impression. |
| 0xd0e1e | 43 | Now that I think on it... I suppose those\n |
| 0xd0e4a | 45 | folks in the tenant houses HAVE been on-edge. |
| 0xd0e78 | 44 | Oh, yeah. Definitely smells like something\n |
| 0xd0ea5 | 29 | fishy is going on down there. |
| 0xd0ec3 | 47 | Some pretty wealthy-looking folk going in and\n |
| 0xd0ef3 | 37 | out at all hours, talking nonsense... |
| 0xd0f19 | 27 | Oh? Now that's interesting. |
| 0xd0f35 | 47 | The longer we hang around, the more old women\n |
| 0xd0f65 | 43 | seem to emerge from the woodwork, hearing\n |
| 0xd0f91 | 12 | Ukon's name. |
| 0xd0f9e | 44 | Soon enough, they begin to chat up a storm\n |
| 0xd0fcb | 43 | about their husbands' shortcomings, local\n |
| 0xd0ff7 | 9 | rumors... |
| 0xd1001 | 44 | Little girls--undoubtedly their children--\n |
| 0xd102e | 41 | flock about Ukon's feet and tug on him,\n |
| 0xd1058 | 16 | begging to play. |
| 0xd1069 | 43 | Guess that's Oshtor for you. Charming the\n |
| 0xd1095 | 27 | ladies no matter their age. |
| 0xd10b1 | 43 | ...So why do I get stuck with the old men\n |
| 0xd10dd | 17 | giving me snacks? |
| 0xd10ef | 47 | Thanks. All right, kid, let's get moving along. |
| 0xd111f | 5 | Hrmf? |
| 0xd1125 | 44 | Finally. Listening to old women talk takes\n |
| 0xd1152 | 41 | forever no matter where you are, I guess. |
| 0xd117c | 47 | Here, try these. The mamutu and the dango are\n |
| 0xd11ac | 17 | both pretty good. |
| 0xd11be | 11 | Ah, thanks. |
| 0xd11ca | 43 | Was that really OK, back there? All I did\n |
| 0xd11f6 | 36 | was chat them up and eat their food. |
| 0xd121b | 43 | Yep, you did perfect. Just keep it up for\n |
| 0xd1247 | 22 | the next place we hit. |
| 0xd125e | 29 | I guess that's easy enough... |
| 0xd127c | 28 | All right, c'mon. Next stop. |
| 0xd1299 | 16 | Yo! Anyone home? |
| 0xd12aa | 43 | Ukon calls into the run-down tenant home... |
| 0xd12d6 | 45 | ...And after a moment, a gaggle of scruffy-\n |
| 0xd1304 | 44 | looking men emerge, giving off a shady vibe. |
| 0xd1331 | 6 | Tenant |
| 0xd1338 | 36 | Wheh? Who the--Oh! If it ain't Ukon. |
| 0xd135d | 49 | Haven't seen you 'round these parts in a while.\n |
| 0xd138f | 32 | Thought you'd up and died on us. |
| 0xd13b0 | 47 | Everything all right, chief? Been a long time\n |
| 0xd13e0 | 17 | since we saw you. |
| 0xd13f2 | 45 | Yeah, sorry about that. I had some stuff to\n |
| 0xd1420 | 13 | take care of. |
| 0xd142e | 45 | Ukon raises his pinky, then sticks his hand\n |
| 0xd145c | 47 | inside his shirt to mimic a bulging, pregnant\n |
| 0xd148c | 14 | belly crudely. |
| 0xd149b | 44 | I-I had no idea you had a girl tucked away\n |
| 0xd14c8 | 16 | somewhere, geez! |
| 0xd14d9 | 48 | Bahahaha! I'm just pulling your leg. I was out\n |
| 0xd150a | 39 | of the capital on business, that's all. |
| 0xd1532 | 42 | Huh. These guys might look a little, uh,\n |
| 0xd155d | 47 | questionable... but they don't seem to be bad\n |
| 0xd158d | 7 | people. |
| 0xd1595 | 47 | My, my. Ukon! Babe. Honey. I've missed you SO\n |
| 0xd15c5 | 29 | much. It's been far too long! |
| 0xd15e3 | 44 | ...A distressingly muscular man in women's\n |
| 0xd1610 | 46 | clothing emerges from the house, approaching\n |
| 0xd163f | 3 | us. |
| 0xd1643 | 42 | What brings you around our little den of\n |
| 0xd166e | 43 | iniquity? And who's the cutie you brought\n |
| 0xd169a | 9 | with you? |
| 0xd16a4 | 6 | Bwuh!? |
| 0xd16ab | 45 | The man(?) winks at me, and suddenly I feel\n |
| 0xd16d9 | 24 | supremely uncomfortable. |
| 0xd16f2 | 48 | I-I take it all back. This place is definitely\n |
| 0xd1723 | 25 | dangerous. Too dangerous. |
| 0xd173d | 48 | Ah, this is a friend of mine from out of town.\n |
| 0xd176e | 44 | You'll probably be seeing a lot more of him. |
| 0xd179b | 46 | I'm Haku. It's a pleasure. Yeah, Ukon picked\n |
| 0xd17ca | 43 | me up on the road and now I'm getting the\n |
| 0xd17f6 | 11 | grand tour. |
| 0xd1802 | 46 | He's a countryside kid, so no need to be all\n |
| 0xd1831 | 26 | stiff and formal with him. |
| 0xd184c | 43 | Nah, nah! Wouldn't dream of disrespecting\n |
| 0xd1878 | 25 | a friend of yours, chief. |
| 0xd1892 | 46 | It wouldn't take much to brush up his looks,\n |
| 0xd18c1 | 47 | y'know, Ukon. I could get him looking as cute\n |
| 0xd18f1 | 7 | as you. |
| 0xd18f9 | 7 | Gfrah!? |
| 0xd1901 | 48 | Every time that infernal wink is aimed my way,\n |
| 0xd1932 | 43 | I feel like my throat is sealing itself up. |
| 0xd195e | 43 | Oh, babe, relax! Look at you, getting all\n |
| 0xd198a | 42 | nervous. You're lucky you're just my type. |
| 0xd19b5 | 43 | Eh? Getting on good terms with the locals\n |
| 0xd19e1 | 32 | already, huh? Good for you, kid. |
| 0xd1a02 | 43 | Wait, wh--How can you even interpret this\n |
| 0xd1a2e | 11 | like that!? |
| 0xd1a3a | 50 | Oh, but back to the serious stuff--You guys been\n |
| 0xd1a6d | 36 | holding up OK? Nothing weird lately? |
| 0xd1a92 | 43 | Nothing real unusual. You know how it is.\n |
| 0xd1abe | 47 | Brothels and gambling dens are doin' business\n |
| 0xd1aee | 8 | as ever. |
| 0xd1af7 | 46 | Oh, but... Babe. I'd stay away from that new\n |
| 0xd1b26 | 41 | place that just popped up, if I were you. |
| 0xd1b50 | 30 | New place? Care to fill me in? |
| 0xd1b6f | 48 | That old storehouse by the river. Used to just\n |
| 0xd1ba0 | 43 | be for shipping booze by canal boat, but... |
| 0xd1bcc | 41 | The old owner's out of the picture now,\n |
| 0xd1bf6 | 45 | apparently. Some new crew has been using it\n |
| 0xd1c24 | 10 | as a base. |
| 0xd1c2f | 48 | Pretty aggressive folk. They do as they please\n |
| 0xd1c60 | 45 | over there, and no one is really doin' much\n |
| 0xd1c8e | 9 | about it. |
| 0xd1c98 | 45 | Doesn't seem like anyone we know is running\n |
| 0xd1cc6 | 47 | the show, but they walk around here like they\n |
| 0xd1cf6 | 13 | own the town. |
| 0xd1d04 | 48 | They pay well, so we kinda turn a blind eye to\n |
| 0xd1d35 | 42 | the ruckus, but we oughta teach 'em some\n |
| 0xd1d60 | 8 | respect. |
| 0xd1d69 | 42 | Rumor's that they have some sorta bigwig\n |
| 0xd1d94 | 49 | backing 'em. Nobles! Not a drop of honor in the\n |
| 0xd1dc6 | 10 | lot, pfeh. |
| 0xd1dd1 | 50 | That's... very interesting. Sorry, guys, but I'm\n |
| 0xd1e04 | 46 | gonna have to ask you to leave this one to me. |
| 0xd1e33 | 43 | Huh? A'ight, I guess. If you say so, chief. |
| 0xd1e5f | 47 | Much appreciated. What else do you know about\n |
| 0xd1e8f | 11 | these guys? |
| 0xd1e9b | 45 | OK. Leave the rest to me. Don't do anything\n |
| 0xd1ec9 | 34 | stupid in the meantime, all right? |
| 0xd1eec | 48 | Gotcha. And thanks, chief. We can always count\n |
| 0xd1f1d | 27 | on you for stuff like this. |
| 0xd1f39 | 47 | Come back any time. Door's always open for you. |
| 0xd1f69 | 45 | You too, young man. If you ever come by the\n |
| 0xd1f97 | 47 | brothel, I can take GOOD care of a cutie like\n |
| 0xd1fc7 | 4 | you. |
| 0xd1fcc | 47 | I don't know why, but I'm sweating like crazy\n |
| 0xd1ffc | 36 | even though it's not even hot out... |
| 0xd2021 | 36 | Seems you're well-liked around here. |
| 0xd2046 | 43 | Think so? It makes me happy to hear that,\n |
| 0xd2072 | 7 | thanks. |
| 0xd207a | 44 | This was exactly how my old man used to do\n |
| 0xd20a7 | 7 | things. |
| 0xd20af | 8 | I see... |
| 0xd20b8 | 45 | You oughta be just fine. They're a bunch of\n |
| 0xd20e6 | 47 | moody guys, yeah, but you seemed to get along\n |
| 0xd2116 | 10 | perfectly. |
| 0xd2121 | 36 | Life's full of surprises, I guess.\n |
| 0xd2146 | 35 | You'll be fast friends soon enough. |
| 0xd216a | 38 | I might need to reconsider that one... |
| 0xd2191 | 44 | Our patrol stretches on, and as we finally\n |
| 0xd21be | 43 | start to wrap up, the sun dips low in the\n |
| 0xd21ea | 11 | orange sky. |
| 0xd21f6 | 48 | Guess that's good enough for now. I think I've\n |
| 0xd2227 | 30 | got a general lay of the land. |
| 0xd2246 | 37 | You're talking about that storehouse? |
| 0xd226c | 46 | Yeah. Judging by what we heard today, that's\n |
| 0xd229b | 18 | gotta be our mark. |
| 0xd22ae | 43 | You told those guys to "leave it to you,"\n |
| 0xd22da | 37 | but what exactly do you intend to do? |
| 0xd2300 | 47 | Can't quite say for certain. Not yet, anyway.\n |
| 0xd2330 | 47 | I'll look into it a little more before I make\n |
| 0xd2360 | 6 | plans. |
| 0xd2367 | 49 | Well, just... don't do anything reckless over it. |
| 0xd2399 | 44 | You've helped me out a lot. I'd prefer not\n |
| 0xd23c6 | 47 | risking my life, but if you need my help, I'm\n |
| 0xd23f6 | 11 | right here. |
| 0xd2402 | 46 | Glad to hear it. Good to know I can count on\n |
| 0xd2431 | 9 | you, kid. |
| 0xd243b | 36 | Kinda strange, don't you think...?\n |
| 0xd2460 | 40 | For some reason, it feels right, this.\n |
| 0xd2489 | 24 | Just walkin' beside you. |
| 0xd24a2 | 18 | Ukon grins widely. |
| 0xd24b5 | 49 | It's an energetic, genuine smile--the kind that\n |
| 0xd24e7 | 45 | can charm courtly nobles and commoners alike. |
| 0xd3641 | 50 | I decided to hit up the dining hall for a snack,\n |
| 0xd3674 | 44 | but it looks like someone had the same idea. |
| 0xd36a1 | 37 | What was her name... Atuy, wasn't it? |
| 0xd36c7 | 35 | Oh, hullo. The disappointing guy.\n |
| 0xd36eb | 39 | I haven't seen you since that one time. |
| 0xd3713 | 25 | Who's disappointing, now? |
| 0xd372d | 46 | It's the girl I guided to the Hakurokaku Inn\n |
| 0xd375c | 40 | the other day... The one with no filter. |
| 0xd3785 | 23 | You here to grab lunch? |
| 0xd379d | 44 | Oh, it's not for me. I'm just here to feed\n |
| 0xd37ca | 19 | this little fellow. |
| 0xd37de | 35 | Atuy indicates the hat on her head. |
| 0xd3802 | 23 | Your hat...? Your head? |
| 0xd381a | 42 | Hat? Oh, hee hee. Yeah, I guess that's a\n |
| 0xd3845 | 22 | pretty common mistake. |
| 0xd385c | 27 | This little one is Kurarin. |
| 0xd3878 | 13 | ...Kurarin?\n |
| 0xd3886 | 17 | What's a Kurarin? |
| 0xd3898 | 19 | Kurarin is Kurarin! |
| 0xd38ac | 48 | Atuy pats the Kurarin(???) on her head fondly... |
| 0xd38dd | 46 | ...which jiggles enthusiastically, as though\n |
| 0xd390c | 11 | responding. |
| 0xd3918 | 14 | It's... alive? |
| 0xd3927 | 45 | Of course! Kurarin's a proud denizen of the\n |
| 0xd3955 | 15 | sea, after all. |
| 0xd3965 | 42 | Now that she mentions it... It does look\n |
| 0xd3990 | 47 | slimy and lifelike. Not like cloth or leather\n |
| 0xd39c0 | 7 | at all. |
| 0xd39c8 | 43 | We really don't quite understand Kurarin.\n |
| 0xd39f4 | 45 | They just sort of drift around the beaches,\n |
| 0xd3a22 | 5 | yeah? |
| 0xd3a28 | 50 | They go where the wind takes them, eat anything,\n |
| 0xd3a5b | 47 | and they're gentle as long as we leave them be. |
| 0xd3a8b | 41 | I'm surprised you'd wear something that\n |
| 0xd3ab5 | 30 | mysterious as, uh... as a hat. |
| 0xd3ad4 | 49 | Hee hee. This little guy's no trouble. Seems to\n |
| 0xd3b06 | 47 | like riding up there and wouldn't hurt a fly,\n |
| 0xd3b36 | 4 | so-- |
| 0xd3b3b | 49 | Atuy takes the creature from her head and talks\n |
| 0xd3b6d | 44 | lovingly to it, holding it in front of her\n |
| 0xd3b9a | 6 | chest. |
| 0xd3ba1 | 19 | Kurarin, say hullo. |
| 0xd3bb5 | 47 | Then, it floats out of Atuy's grip and toward\n |
| 0xd3be5 | 44 | me, waving a tentacle as though in greeting. |
| 0xd3c12 | 16 | Whoa, it floats? |
| 0xd3c23 | 28 | Yeah, I just said, didn't I? |
| 0xd3c40 | 45 | Well, when you said floating, I figured you\n |
| 0xd3c6e | 43 | meant, like--floating in the water. At sea. |
| 0xd3c9a | 25 | It's really alive, huh... |
| 0xd3cb4 | 48 | You don't get them around here? They're pretty\n |
| 0xd3ce5 | 25 | common along the coast... |
| 0xd3cff | 24 | No, I've never seen one. |
| 0xd3d18 | 46 | The sight of this translucent, wobbling mass\n |
| 0xd3d47 | 46 | in the air... It's like I'm watching a magic\n |
| 0xd3d76 | 6 | trick. |
| 0xd3d7d | 46 | It obeyed Atuy's commands, so it must have a\n |
| 0xd3dac | 35 | pretty good amount of intelligence. |
| 0xd3dd0 | 30 | Hey, isn't it a cutie, though? |
| 0xd3def | 28 | ...Yeah, it's not that cute. |
| 0xd3e0c | 43 | You said you were here to feed it, right?\n |
| 0xd3e38 | 17 | What does it eat? |
| 0xd3e4a | 47 | You said it eats up anything, but what about,\n |
| 0xd3e7a | 47 | like... people? Does it scavenge for carrion,\n |
| 0xd3eaa | 5 | or... |
| 0xd3eb0 | 45 | I pull back my hand cautiously, asking Atuy\n |
| 0xd3ede | 25 | about my sudden concerns. |
| 0xd3ef8 | 45 | Oh, no, nothing like that. A young one like\n |
| 0xd3f26 | 44 | this? Insects, fish, maybe some fresh meat\n |
| 0xd3f53 | 19 | would do the trick. |
| 0xd3f67 | 47 | It'll get playful and shock people sometimes,\n |
| 0xd3f97 | 29 | but it doesn't mean any harm. |
| 0xd3fb5 | 9 | ...Shock? |
| 0xd3fbf | 37 | Yeah, with this little tentacle here. |
| 0xd3fe5 | 47 | Atuy points at one of the dangling appendages\n |
| 0xd4015 | 28 | hanging from Kurarin's side. |
| 0xd4032 | 29 | Yikes. I almost touched that. |
| 0xd4050 | 44 | Oh, don't be so scared! It's just a little\n |
| 0xd407d | 11 | baby shock. |
| 0xd4089 | 7 | Sure... |
| 0xd4091 | 47 | Going by what I've experienced so far, taking\n |
| 0xd40c1 | 48 | people at their word for this stuff never ends\n |
| 0xd40f2 | 5 | well. |
| 0xd40f8 | 12 | *Poke, poke* |
| 0xd4105 | 30 | Kurarin pokes Atuy's shoulder. |
| 0xd4124 | 31 | Hm? Yeah, it IS taking a while. |
| 0xd4144 | 16 | Something wrong? |
| 0xd4155 | 46 | Yeah, it's just that it's been a while since\n |
| 0xd4184 | 45 | I asked for Kurarin's food. Maybe there's a\n |
| 0xd41b2 | 11 | problem...? |
| 0xd41be | 46 | No choice, I s'pose. I'll duck in and see if\n |
| 0xd41ed | 23 | everything's all right. |
| 0xd4205 | 44 | Look after this little one, won't you, love? |
| 0xd4232 | 12 | Huh? H-Hey-- |
| 0xd423f | 45 | With that, Atuy leaves the dining hall in a\n |
| 0xd426d | 6 | hurry. |
| 0xd4274 | 44 | ...She asked me to look after it, but what\n |
| 0xd42a1 | 31 | exactly am I... supposed to do? |
| 0xd42c1 | 46 | As instructed, I watch over Kurarin... which\n |
| 0xd42f0 | 45 | gracefully floats about, distinctly lacking\n |
| 0xd431e | 9 | cuteness. |
| 0xd4328 | 20 | This is "cute," huh. |
| 0xd433d | 46 | No matter how I look at it, I just can't get\n |
| 0xd436c | 44 | "cute" out of this. It's not like it has a\n |
| 0xd4399 | 14 | charming face. |
| 0xd43ac | 14 | ...Charm, huh. |
| 0xd43bb | 47 | I take a writing brush from my pocket and set\n |
| 0xd43eb | 37 | it against the creature's slimy skin. |
| 0xd4411 | 42 | Let's draw one up, here... There you go.\n |
| 0xd443c | 34 | Maybe you'll be cuter with a face. |
| 0xd445f | 48 | You never know. You could be more popular with\n |
| 0xd4490 | 39 | the girls this way. Ladykiller Kurarin. |
| 0xd44b8 | 47 | Two quick circles, a half-moon crescent for a\n |
| 0xd44e8 | 24 | mouth, and we're golden. |
| 0xd4501 | 47 | ...Weird. That was supposed to make you cute,\n |
| 0xd4531 | 17 | not even weirder. |
| 0xd4543 | 37 | ...Maybe if I add the pupils, too...? |
| 0xd4569 | 40 | ...OK, now we've crossed the line into\n |
| 0xd4592 | 9 | "creepy." |
| 0xd459c | 44 | This thing is gonna haunt my nightmares if\n |
| 0xd45c9 | 17 | I don't erase it. |
| 0xd45db | 46 | I gently take Kurarin and wipe its face(???)\n |
| 0xd460a | 18 | with a hand towel. |
| 0xd461d | 33 | Ngh, slippery. Hard to wipe--Gah! |
| 0xd463f | 6 | *Slip* |
| 0xd4646 | 44 | Ah, Haku. So this is where you got off to.\n |
| 0xd4673 | 17 | Dear sister was-- |
| 0xd4685 | 7 | *Stick* |
| 0xd468d | 5 | EEP!? |
| 0xd4693 | 44 | Kurarin adheres to Nekone's cheek, and she\n |
| 0xd46c0 | 48 | flings the creature away with all the strength\n |
| 0xd46f1 | 8 | she has. |
| 0xd46fa | 47 | I understand how she feels, but c'mon, that's\n |
| 0xd472a | 11 | just cruel. |
| 0xd4736 | 23 | Wh-Wh-Wh-What is that!? |
| 0xd474e | 13 | It's Kurarin. |
| 0xd475c | 33 | And a Kurarin is WHAT, pray tell? |
| 0xd477e | 19 | Kurarin is Kurarin. |
| 0xd4792 | 43 | Well, uh, how should I put this. I was...\n |
| 0xd47be | 43 | trying to make it cuter? But it's hard to\n |
| 0xd47ea | 14 | wipe off, so-- |
| 0xd47f9 | 46 | And that is your notion of "cute"? I will be\n |
| 0xd4828 | 40 | seeing that horror in my dreams tonight. |
| 0xd4851 | 46 | Don't say that. I didn't think it would turn\n |
| 0xd4880 | 14 | out like this! |
| 0xd488f | 48 | It would be a disaster if you let the stuff of\n |
| 0xd48c0 | 25 | nightmares out in public. |
| 0xd48da | 39 | "Disaster" is stretching it a little... |
| 0xd4902 | 49 | Anyway. Dear sister is looking for you. And now\n |
| 0xd4934 | 48 | that I have delivered the message, I will take\n |
| 0xd4965 | 9 | my leave. |
| 0xd496f | 44 | With that, Nekone quickly exits the dining\n |
| 0xd499c | 5 | hall. |
| 0xd49a2 | 4 | Huh? |
| 0xd49a7 | 45 | ...And as my attention returns to the room,\n |
| 0xd49d5 | 46 | I realize I don't see the flung-away Kurarin\n |
| 0xd4a04 | 9 | anywhere. |
| 0xd4a0e | 5 | GAH!? |
| 0xd4a14 | 4 | EEK! |
| 0xd4a19 | 46 | Geh!? S-So you've shown yourself, you monster! |
| 0xd4a48 | 48 | Then--faintly muffled--I can hear the sound of\n |
| 0xd4a79 | 47 | someone falling down stairs, breaking plates,\n |
| 0xd4aa9 | 10 | yelling... |
| 0xd4ab4 | 24 | Oof. S-Sorry about that. |
| 0xd4acd | 47 | Oh, for shame, love! I thought I asked you to\n |
| 0xd4afd | 18 | keep an eye on it. |
| 0xd4b10 | 46 | Sorry, sorry. I only took my eyes away for a\n |
| 0xd4b3f | 9 | second... |
| 0xd4b49 | 36 | Oh, but aren't you lucky, Kurarin?\n |
| 0xd4b6e | 32 | Getting such pretty makeup done! |
| 0xd4b8f | 24 | *Jiggle, jiggle, jiggle* |
| 0xd4ba8 | 24 | Hee. Kurarin's so happy. |
| 0xd4bc1 | 49 | Kurarin wraps its tentacles around my face with\n |
| 0xd4bf3 | 38 | every indication of eager affection... |
| 0xd4c1a | 44 | And the nightmarish face begins to emit an\n |
| 0xd4c47 | 12 | eerie light. |
| 0xd4c54 | 17 | BLRGLRGHLRGLRGH-- |
| 0xd4c66 | 45 | Aw! Hee, you see? So happy! That's a thanks\n |
| 0xd4c94 | 44 | for doing such a good job with the makeover. |
| 0xd4cc1 | 13 | BLGLRGHRLGH-- |
| 0xd4ccf | 44 | H-How is this a "tiny little baby shock"!?\n |
| 0xd4cfc | 5 | Buh-- |
| 0xd4d02 | 47 | As I slip into unconsciousness, I make a note\n |
| 0xd4d32 | 43 | not to trust anyone else's sense of scale\n |
| 0xd4d5e | 12 | around here. |
| 0xd5ef7 | 7 | *WHUMP* |
| 0xd5eff | 5 | Agh-- |
| 0xd5f05 | 46 | Finally freed from my desk work, I lean back\n |
| 0xd5f34 | 45 | to stretch, only to bash my arm against the\n |
| 0xd5f62 | 15 | table's corner. |
| 0xd5f72 | 25 | Ow, ow... Tch. Grazed it. |
| 0xd5f8c | 47 | I roll up my sleeve to find blood oozing from\n |
| 0xd5fbc | 23 | the scratch, grimacing. |
| 0xd5fd4 | 43 | I should tell Kuon... Eh, no, I shouldn't\n |
| 0xd6000 | 39 | bother her. This'll heal up on its own. |
| 0xd6028 | 45 | If it were a more serious wound, maybe, but\n |
| 0xd6056 | 47 | I'd feel bad bothering her over a tiny scratch. |
| 0xd6086 | 28 | *Grind, grind, grind, grind* |
| 0xd60a3 | 46 | Grinding noises echo from behind Kuon's door\n |
| 0xd60d2 | 15 | as I pass by... |
| 0xd60e2 | 18 | What's that sound? |
| 0xd60f5 | 11 | Hm hm-hm... |
| 0xd6101 | 32 | And she's... humming to herself? |
| 0xd6122 | 47 | I decide to peek into her room, and a strange\n |
| 0xd6152 | 39 | fragrance wafts across my nose--and I\n |
| 0xd617a | 11 | understand. |
| 0xd6186 | 27 | Ah, I see. She's working... |
| 0xd61a2 | 41 | What are you doing, hovering out there?\n |
| 0xd61cc | 29 | C'mon, why don't you come in? |
| 0xd61ea | 42 | Oh, just being curious. I didn't want to\n |
| 0xd6215 | 17 | interrupt, sorry. |
| 0xd6227 | 47 | I see. I'll be done soon, so just hang around\n |
| 0xd6257 | 10 | for a bit. |
| 0xd6262 | 45 | She indicates a cushion, and I take a seat,\n |
| 0xd6290 | 18 | watching her work. |
| 0xd62a3 | 49 | Kuon grinds something dark green and paste-like\n |
| 0xd62d5 | 44 | into a mortar, continuing to hum pleasantly. |
| 0xd6302 | 44 | ...So I, uh, assume you're making medicine\n |
| 0xd632f | 43 | there? I mean, I doubt you're grinding up\n |
| 0xd635b | 11 | condiments. |
| 0xd6367 | 49 | This? This'll be a new salve, I think. I wanted\n |
| 0xd6399 | 45 | to put some rare herbs I found to proper use. |
| 0xd63c7 | 44 | That's impressive. You're always prepared,\n |
| 0xd63f4 | 7 | huh...? |
| 0xd63fc | 45 | Looking around her room, there's a lot more\n |
| 0xd642a | 44 | equipment in here than when we first moved\n |
| 0xd6457 | 5 | in... |
| 0xd645d | 48 | ...all of it inscrutable to the untrained eye,\n |
| 0xd648e | 25 | its uses unclear at best. |
| 0xd64a8 | 49 | They're probably tools for her apothecary work,\n |
| 0xd64da | 38 | but to me they're not much more than\n |
| 0xd6501 | 12 | curiosities. |
| 0xd650e | 47 | Confused? Anything in here look curious to you? |
| 0xd653e | 43 | Yeah, the equipment looks curious, but...\n |
| 0xd656a | 45 | What sort of effect does this weird-looking\n |
| 0xd6598 | 11 | fruit have? |
| 0xd65a4 | 44 | I mean, I understand that it's probably an\n |
| 0xd65d1 | 42 | ingredient or reagent of some kind, but... |
| 0xd65fc | 41 | I gingerly pick up a poisonous-looking,\n |
| 0xd6626 | 46 | reddish-black fruit replete with yellow spots. |
| 0xd6655 | 42 | That's an ikoraship. Ingested, it has an\n |
| 0xd6680 | 46 | antipyretic effect--lowers body temperature,\n |
| 0xd66af | 13 | I should say. |
| 0xd66bd | 45 | Ingest? If I saw this laying in the forest,\n |
| 0xd66eb | 34 | I'd stay away. It looks poisonous. |
| 0xd670e | 47 | Even if I knew its effects, I don't think I'd\n |
| 0xd673e | 15 | want to eat it. |
| 0xd674e | 44 | That's why I grind it up in a mortar. It's\n |
| 0xd677b | 37 | easier to take as a pill or a powder. |
| 0xd67a1 | 47 | And that way, I can add analgesics like tenma\n |
| 0xd67d1 | 46 | or piwayo, which makes it a really effective\n |
| 0xd6800 | 14 | cold medicine. |
| 0xd680f | 48 | It's got a fatal flaw, though--it's so bitter,\n |
| 0xd6840 | 47 | even a stunning beauty would make a sour face\n |
| 0xd6870 | 17 | after tasting it. |
| 0xd6882 | 47 | That's... sort of understandable, but sort of\n |
| 0xd68b2 | 48 | not? That doesn't make me want to put it in my\n |
| 0xd68e3 | 6 | mouth. |
| 0xd68ea | 45 | The best medicines are always the ones with\n |
| 0xd6918 | 22 | the most bitter taste. |
| 0xd692f | 44 | I'll be really careful not to catch a cold\n |
| 0xd695c | 17 | around you, then. |
| 0xd696e | 48 | Ahaha. That's probably for the best. No better\n |
| 0xd699f | 45 | medicine than not getting sick in the first\n |
| 0xd69cd | 6 | place. |
| 0xd69d4 | 46 | You really are knowledgeable, though. Do you\n |
| 0xd6a03 | 45 | know the names and effects of everything in\n |
| 0xd6a31 | 5 | here? |
| 0xd6a37 | 45 | Mhm. My mother was my instructor when I was\n |
| 0xd6a65 | 30 | just an apprentice apothecary. |
| 0xd6a84 | 48 | She was normally very gentle and kind, but she\n |
| 0xd6ab5 | 33 | became strict when she taught me. |
| 0xd6ad7 | 39 | She'd hit me if I made a mistake, and\n |
| 0xd6aff | 46 | oftentimes, we'd study through the night and\n |
| 0xd6b2e | 17 | into the morning. |
| 0xd6b40 | 46 | Sounds like a pretty stern woman to have for\n |
| 0xd6b6f | 10 | a teacher. |
| 0xd6b7a | 45 | Mm, well--she had to be. There are a lot of\n |
| 0xd6ba8 | 45 | dangerous substances involved in apothecary\n |
| 0xd6bd6 | 5 | work. |
| 0xd6bdc | 46 | Even a small error when measuring dosage can\n |
| 0xd6c0b | 42 | cause serious trouble, so you have to be\n |
| 0xd6c36 | 11 | meticulous. |
| 0xd6c42 | 16 | Serious trouble? |
| 0xd6c53 | 48 | Medicines in high concentrations might as well\n |
| 0xd6c84 | 44 | be toxins. They can disable or even kill a\n |
| 0xd6cb1 | 7 | person. |
| 0xd6cb9 | 46 | Kill a person... Yeah, I can see why she was\n |
| 0xd6ce8 | 36 | so strict with your education, then. |
| 0xd6d0d | 48 | Yep. There's no such thing as being too strict\n |
| 0xd6d3e | 45 | when you've got people's lives in your hands. |
| 0xd6d6c | 48 | I understand that much, but didn't your mother\n |
| 0xd6d9d | 48 | being so overbearing... I dunno, get to you at\n |
| 0xd6dce | 4 | all? |
| 0xd6dd3 | 46 | Did you ever just rebel and go "I don't want\n |
| 0xd6e02 | 21 | to be an apothecary?" |
| 0xd6e18 | 44 | Hm. I mean, it's not as though I never had\n |
| 0xd6e45 | 26 | thoughts like that, but... |
| 0xd6e60 | 46 | Kuon puts down her tools and looks up at the\n |
| 0xd6e8f | 46 | ceiling, as though reflecting on her memories. |
| 0xd6ebe | 44 | She had a proper reason for being so tough\n |
| 0xd6eeb | 47 | about medicine, and otherwise, she was a warm\n |
| 0xd6f1b | 47 | I remember whenever I got sick, she'd stay by\n |
| 0xd6f4b | 33 | my bedside and take care of me... |
| 0xd6f6d | 44 | And when I finally started making medicine\n |
| 0xd6f9a | 34 | properly myself, she was ecstatic. |
| 0xd6fbd | 49 | ...Though I can't say I'm a huge fan of how she\n |
| 0xd6fef | 45 | made me take bitter medicine "for my health." |
| 0xd701d | 44 | Even so, it must be a good memory--Kuon is\n |
| 0xd704a | 23 | smiling with nostalgia. |
| 0xd7066 | 47 | But just for a moment. A shadow of loneliness\n |
| 0xd7096 | 30 | seems to creep into her smile. |
| 0xd70b5 | 5 | Kuon? |
| 0xd70bb | 20 | ...Ah. It's nothing. |
| 0xd70d0 | 48 | Shaking her head, she returns to grinding with\n |
| 0xd7101 | 22 | her mortar and pestle. |
| 0xd7118 | 44 | Unfamiliar liquids and powders go into the\n |
| 0xd7145 | 30 | deep-green mix from earlier... |
| 0xd7164 | 35 | Mm, that should just about do it.\n |
| 0xd7188 | 11 | Here, Haku. |
| 0xd7194 | 47 | The salve-like contents of the mortar go into\n |
| 0xd71c4 | 41 | a shell container, which she hands to me. |
| 0xd71ee | 28 | The salve you just made...\n |
| 0xd720b | 23 | You're giving it to me? |
| 0xd7223 | 49 | You always seem to be getting cuts and scrapes,\n |
| 0xd7255 | 48 | so you should hold onto a fresh supply, I think. |
| 0xd7286 | 49 | I'll make more again when you run out, so don't\n |
| 0xd72b8 | 18 | be stingy with it. |
| 0xd72cb | 32 | I see. I'll use it well, then.\n |
| 0xd72ec | 10 | Thank you. |
| 0xd72f7 | 49 | That said... This stuff won't make me all itchy\n |
| 0xd7329 | 49 | like last time, will it? I'd rather not revisit\n |
| 0xd735b | 7 | that... |
| 0xd7363 | 49 | Well, I should get going. I've got some work to\n |
| 0xd7395 | 13 | take care of. |
| 0xd73a3 | 17 | Hold on a moment. |
| 0xd73b7 | 37 | Kuon grabs my sleeve as I turn to go. |
| 0xd73dd | 23 | Show me your arm, Haku. |
| 0xd73f5 | 43 | She rolls up my sleeve, exposing my arm--\n |
| 0xd7421 | 43 | or rather, the scrape I'd acquired earlier. |
| 0xd744d | 42 | Wh-What? I'm surprised you noticed that.\n |
| 0xd7478 | 21 | It's just a scrape... |
| 0xd748e | 46 | It's not worth bothering an apothecary over.\n |
| 0xd74bd | 41 | I'll just let it heal up naturally, so... |
| 0xd74e7 | 47 | Nope. That won't fly with me. Have a seat, you. |
| 0xd7517 | 47 | Despite my objections, Kuon pushes me back to\n |
| 0xd7547 | 33 | her workstation and makes me sit. |
| 0xd7569 | 49 | Better to be safe than sorry. Even small wounds\n |
| 0xd759b | 43 | can become problems if they fester or get\n |
| 0xd75c7 | 9 | infected. |
| 0xd75d1 | 18 | Apothecary wisdom? |
| 0xd75e4 | 45 | That's right. I'll put an antiseptic on it,\n |
| 0xd7612 | 14 | so hold still. |
| 0xd7621 | 41 | No matter what I say, I don't think I'm\n |
| 0xd764b | 33 | worming my way out of this one... |
| 0xd766d | 44 | Hey, uh... If you can avoid it, I'd really\n |
| 0xd769a | 41 | prefer a salve that doesn't itch so much. |
| 0xd76c4 | 33 | Ah, this one won't itch, I think. |
| 0xd76e6 | 37 | Kuon gives me a wide, toothy smile.\n |
| 0xd770c | 34 | I think I've seen that one before. |
| 0xd772f | 43 | Really? So I'll be all right even if it's\n |
| 0xd775b | 21 | totally slathered on? |
| 0xd7771 | 29 | Well, that I can't guarantee. |
| 0xd778f | 4 | Huh? |
| 0xd7794 | 45 | Disregarding my confusion, Kuon scrapes the\n |
| 0xd77c2 | 46 | last of the mortar's contents out and pastes\n |
| 0xd77f1 | 8 | them on. |
| 0xd77fa | 29 | Ack...! Ow, ow, it stings--!! |
| 0xd7818 | 48 | What sort of medicine is this? It doesn't just\n |
| 0xd7849 | 16 | sting--it hurts! |
| 0xd785a | 50 | Sharp prickling sensations assault the irritated\n |
| 0xd788d | 21 | parts of the wound... |
| 0xd78a3 | 38 | It stings, then? I figured it might.\n |
| 0xd78ca | 40 | It's effective, but its drawback is it\n |
| 0xd78f3 | 19 | irritates a little. |
| 0xd7907 | 41 | What do you mean, "drawback?" Ow, ow...\n |
| 0xd7931 | 41 | Wh-Why don't you improve the formula or\n |
| 0xd795b | 10 | something? |
| 0xd7966 | 48 | I told you before, the best medicine is always\n |
| 0xd7997 | 44 | bitter. If it has faults, you know it will\n |
| 0xd79c4 | 42 | I-I hear what you're saying, but... Gah.\n |
| 0xd79ef | 44 | I'd prefer something that helps more than \n |
| 0xd7a1c | 9 | it hurts! |
| 0xd7a26 | 48 | All right, bear with me and let me bandage it.\n |
| 0xd7a57 | 49 | You shouldn't rush this--your body's important,\n |
| 0xd7a89 | 7 | y'know. |
| 0xd7a91 | 27 | I guess that's true, but... |
| 0xd7aad | 48 | Point taken. I trail off and let Kuon go about\n |
| 0xd7ade | 14 | her treatment. |
| 0xd7aed | 12 | ...Ow ow ow. |
| 0xd7afa | 48 | A prickling pain shoots up my arm as she wraps\n |
| 0xd7b2b | 27 | a bandage around the wound. |
| 0xd7b47 | 22 | A-Are you almost done? |
| 0xd7b5e | 48 | My body tenses up at the strange, exotic pain,\n |
| 0xd7b8f | 43 | altogether different from the pain of the\n |
| 0xd7bbb | 9 | scrape... |
| 0xd7bc5 | 44 | That should do it. Next time you get hurt,\n |
| 0xd7bf2 | 43 | don't write it off like it's no big deal.\n |
| 0xd7c1e | 12 | Come see me. |
| 0xd7c2b | 13 | U-Understood. |
| 0xd7c39 | 40 | I can't help but nod as she projects a\n |
| 0xd7c62 | 31 | professional, doctor-like aura. |

## 8. Formato de saida EXIGIDO
Escreva `translations_16_01.json` com a forma:
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
