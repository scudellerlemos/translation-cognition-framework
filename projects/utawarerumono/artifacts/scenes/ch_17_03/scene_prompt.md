# Cena ch_17_03 — pacote de traducao (194 linhas)

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
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `What do you mean?` -> `O que você quer dizer?` (Haku, 13_01)
- `going.` -> `indo.` (Haku, 16_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `What do you mean by that?` -> `O que você quer dizer com isso?` (Haku, 15_03)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `right?` -> `né?` (Haku, 12_03)
- `too?` -> `também?` (Maroro, 17_01)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `but...` -> `mas...` (Kuon, 12_16)
- `you...` -> `você...` (Haku, 12_11)
- `Will you accept?` -> `Você aceita?` (Ukon, 16_02)
- `Haku.` -> `Haku.` (Kuon, 12_08)
- `us...` -> `aproxima...` (Haku, 13_05)
- `me?` -> `mim?` (Maroro, 12_13)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `here?` -> `afinal?` (Haku, 13_02)
- `Bwah!` -> `Bwah!` (Haku, 13_02)
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
| 0x1133d8 | 26 | Wow, this place is huge... |
| 0x1133f3 | 47 | Having received a sudden summons from Oshtor,\n |
| 0x113423 | 34 | we arrive at his impressive manor. |
| 0x113446 | 48 | Didn't he say he doesn't have very much money?\n |
| 0x113477 | 43 | This is definitely a rich person's house... |
| 0x1134a3 | 48 | I think aloud as we walk along the long hallway. |
| 0x1134d4 | 40 | You need to work a little more on your\n |
| 0x1134fd | 24 | appraising skills, Haku. |
| 0x113516 | 17 | What do you mean? |
| 0x113528 | 44 | Yeah! Just because you live in a big place\n |
| 0x113555 | 43 | doesn't mean you have a whole lot of money. |
| 0x113581 | 48 | Atuy seems to be adjusting to our group rather\n |
| 0x1135b2 | 38 | quickly, despite only just joining us. |
| 0x1135d9 | 46 | Atuy is correct. This manor has been granted\n |
| 0x113608 | 43 | for our use, and is not my dear brother's\n |
| 0x113634 | 18 | personal property. |
| 0x113647 | 45 | I figured as much. A lot of the decorations\n |
| 0x113675 | 40 | in here are plain, so I had a feeling... |
| 0x11369e | 47 | I guess you're right. I thought so too, but I\n |
| 0x1136ce | 29 | didn't want to be rude, so... |
| 0x1136ec | 42 | I have no idea what she's talking about.\n |
| 0x113717 | 46 | These decorations look exactly the same to me. |
| 0x11374a | 14 | Oh--excuse me. |
| 0x113759 | 44 | I bump into someone as we turn the corner.\n |
| 0x113786 | 45 | That's what I get for not looking where I'm\n |
| 0x1137b4 | 6 | going. |
| 0x1137bb | 50 | Ah, forgive me, I should be the one apologizing.\n |
| 0x1137ee | 22 | I was lost in thought. |
| 0x113805 | 26 | If you'll excuse me, then. |
| 0x113820 | 40 | The man smiles and continues on his way. |
| 0x113849 | 20 | That man just now... |
| 0x11385e | 4 | Huh? |
| 0x113863 | 30 | I think we've seen him before. |
| 0x113882 | 14 | Really? Where? |
| 0x113891 | 28 | ...I can't quite remember... |
| 0x1138ae | 43 | Maybe you saw him in the manor once before? |
| 0x1138da | 20 | Hrm. I'm not sure... |
| 0x1138ef | 44 | Dear sister, everyone--if you would please\n |
| 0x11391c | 10 | follow me? |
| 0x113927 | 14 | Y-Yes, coming. |
| 0x113936 | 48 | I thank you for coming. Please, seat yourselves. |
| 0x113967 | 48 | That noble bearing, that calm, collected aura... |
| 0x113998 | 49 | It's still hard to believe this is the same guy\n |
| 0x1139ca | 8 | as Ukon. |
| 0x1139d3 | 44 | Oshtor waits for us to be seated before he\n |
| 0x113a00 | 15 | speaks further. |
| 0x113a10 | 46 | I have a job I'd like to speak to you about.\n |
| 0x113a3f | 48 | As you know, a spate of burglaries has plagued\n |
| 0x113a70 | 11 | the city... |
| 0x113a7c | 47 | A contact of mine is concerned for the safety\n |
| 0x113aac | 41 | of his stores, and is hiring additional\n |
| 0x113ad6 | 9 | security. |
| 0x113ae0 | 29 | Guarding a storehouse, huh... |
| 0x113afe | 50 | It's better than cleaning stables and picking up\n |
| 0x113b31 | 44 | trash, but it still seems like a random job. |
| 0x113b5e | 47 | Ordinarily, I have a policy against accepting\n |
| 0x113b8e | 39 | personal requests, but my contact was\n |
| 0x113bb6 | 12 | insistent... |
| 0x113bc3 | 44 | ...and this task in particular presents us\n |
| 0x113bf0 | 38 | with a uniquely promising opportunity. |
| 0x113c17 | 25 | What do you mean by that? |
| 0x113c31 | 44 | Our client for this job is none other than\n |
| 0x113c5e | 40 | Dekopompo, of the Eight Pillar Generals. |
| 0x113c87 | 15 | THAT Dekopompo? |
| 0x113c97 | 47 | Weren't the Eight Pillar Generals the Yamatan\n |
| 0x113cc7 | 45 | military's top brass, or something like that? |
| 0x113cf5 | 46 | Correct. Their positions are granted to them\n |
| 0x113d24 | 22 | by the Mikado himself. |
| 0x113d3b | 43 | All of them come from influential houses,\n |
| 0x113d67 | 40 | and they outrank my dear brother as an\n |
| 0x113d90 | 15 | Imperial Guard. |
| 0x113da0 | 40 | Goodness. I had no idea my papa was so\n |
| 0x113dc9 | 10 | important. |
| 0x113dd4 | 7 | ...Huh? |
| 0x113ddc | 16 | Something wrong? |
| 0x113ded | 49 | Ah, Atuy? Your father, Soyankekur the Mariner--\n |
| 0x113e1f | 48 | he has full command of Yamato's navy. He is of\n |
| 0x113e50 | 48 | the most paramount importance to our prosperity. |
| 0x113e81 | 30 | How are you not aware of that? |
| 0x113ea0 | 22 | Well... yeah, I guess. |
| 0x113eb7 | 46 | I've never really kept track of what my papa\n |
| 0x113ee6 | 49 | does. Besides, there's a lot of those generals,\n |
| 0x113f18 | 6 | right? |
| 0x113f1f | 43 | Eight Pillar Generals. Eight. That is not\n |
| 0x113f4b | 14 | "a lot," Atuy. |
| 0x113f5a | 44 | But isn't Rulie's papa one of those folks,\n |
| 0x113f87 | 4 | too? |
| 0x113f8c | 42 | Well--yes, he is, but that does not mean-- |
| 0x113fb7 | 44 | Hey, Rulie, doesn't that mean you're a big\n |
| 0x113fe4 | 19 | important princess? |
| 0x113ff8 | 46 | Well, er--I'm the youngest of m-my siblings,\n |
| 0x114027 | 5 | so... |
| 0x11402d | 45 | Does Atuy not get that "important princess"\n |
| 0x11405b | 48 | applies to her too? I expected her to be rich,\n |
| 0x11408c | 6 | but... |
| 0x114093 | 47 | Oshtor. You said you're taking this guy's job\n |
| 0x1140c3 | 48 | because he's a bigwig? That doesn't sound like\n |
| 0x1140f4 | 6 | you... |
| 0x1140fb | 40 | Ha, well--let's just leave it at that.\n |
| 0x114124 | 16 | Will you accept? |
| 0x114135 | 48 | Sure, I guess. Not like we have to do anything\n |
| 0x114166 | 21 | particularly special. |
| 0x11417c | 33 | Excellent. You have my gratitude. |
| 0x11419e | 46 | So we just have to camp out in front of this\n |
| 0x1141cd | 17 | storehouse, eh... |
| 0x1141df | 39 | Nekone leads us to Dekopompo's estates. |
| 0x114207 | 33 | Ah, I get what Kuon meant, now... |
| 0x114229 | 45 | Looking around at the grounds, I can't help\n |
| 0x114257 | 12 | but exclaim. |
| 0x114264 | 48 | This must be what she meant by appraisal skills. |
| 0x114295 | 38 | Oshtor's manor was impressive, sure,\n |
| 0x1142bc | 24 | but this is a cut above. |
| 0x1142d5 | 49 | Each room is several times larger than Oshtor's\n |
| 0x114307 | 7 | office. |
| 0x11430f | 44 | The entirety of the manor is decked out in\n |
| 0x11433c | 42 | hanging scrolls, large vases, ceremonial\n |
| 0x114367 | 10 | weapons... |
| 0x114372 | 41 | Every artifact must cost a small fortune. |
| 0x11439c | 46 | Compared to this place, Oshtor's manor seems\n |
| 0x1143cb | 21 | modest in comparison. |
| 0x1143e1 | 48 | Just how corrupt do you have to be, to live in\n |
| 0x114412 | 25 | a place this extravagant? |
| 0x11442c | 46 | Don't say things like that while we're here,\n |
| 0x11445b | 5 | Haku. |
| 0x114461 | 46 | If he's the master of such a splendid manor,\n |
| 0x114490 | 36 | I'm sure he's a deserving gentleman. |
| 0x1144b5 | 44 | Is this what they perceive as tasteful and\n |
| 0x1144e2 | 38 | elegant, then? I guess I can see it... |
| 0x114509 | 33 | Urgh, this place hurts my eyes.\n |
| 0x11452b | 19 | Such awful taste... |
| 0x11453f | 34 | Ah, everyone, I think he's coming. |
| 0x114562 | 3 | Oh. |
| 0x114566 | 47 | A rotund, pompous-looking man enters the room\n |
| 0x114596 | 37 | soon after, flanked by fawning women. |
| 0x1145bc | 47 | He waddles over and seats himself in front of\n |
| 0x1145ec | 5 | us... |
| 0x1145f2 | 46 | I am Dekopompo, lord of these grand estates.\n |
| 0x114621 | 46 | I presume you to be the help Oshtor promised\n |
| 0x114650 | 3 | me? |
| 0x114654 | 6 | Eww... |
| 0x11465b | 50 | Please, don't look so apprehensive! It's natural\n |
| 0x11468e | 47 | to be awestruck by a man of so high a station\n |
| 0x1146be | 8 | as mine. |
| 0x1146c7 | 44 | I'm sure Oshtor informed you of your task.\n |
| 0x1146f4 | 41 | You're to protect a storehouse from any\n |
| 0x11471e | 10 | intruders. |
| 0x114729 | 49 | Rumors abound of this 'noble thief' in the city\n |
| 0x11475b | 49 | of late. A fly, buzzing about and disrupting my\n |
| 0x11478d | 6 | trade. |
| 0x114794 | 45 | Such a nuisance is easily dispatched by the\n |
| 0x1147c2 | 48 | soldiers in my direct employ, to be sure, but... |
| 0x1147f3 | 47 | I have a GREAT many storehouses to guard, you\n |
| 0x114823 | 49 | see. RELUCTANTLY, I asked Oshtor for additional\n |
| 0x114855 | 6 | staff. |
| 0x11485c | 47 | Which is where you come in. I advise that you\n |
| 0x11488c | 25 | try not to screw this up. |
| 0x1148a6 | 49 | With that, Dekopompo gets up and turns to leave\n |
| 0x1148d8 | 29 | before any of us can respond. |
| 0x1148f6 | 34 | Ah, by the way... You there. Girl. |
| 0x114919 | 3 | Me? |
| 0x11491d | 47 | Indeed. I couldn't help but overhear what you\n |
| 0x11494d | 43 | said about the manor befitting a gentleman. |
| 0x114979 | 30 | So he heard everything. Great. |
| 0x114998 | 40 | You have an EXQUISITE eye, to be sure.\n |
| 0x1149c1 | 22 | Discriminating indeed. |
| 0x1149d8 | 48 | The paintings and ornaments you see around you\n |
| 0x114a09 | 49 | are rarities! Items from my personal collection\n |
| 0x114a3b | 4 | all. |
| 0x114a40 | 48 | It pleases me that even commoners like you can\n |
| 0x114a71 | 45 | appreciate the acumen of my artistic taste!\n |
| 0x114a9f | 9 | Nyeh-HAH! |
| 0x114aa9 | 49 | His piece apparently said, Dekopompo leaves the\n |
| 0x114adb | 31 | room with his entourage in tow. |
| 0x114afb | 25 | "Commoners like us," huh. |
| 0x114b15 | 48 | It's fairly clear most of us aren't commoners.\n |
| 0x114b46 | 46 | I mean, HOW many princesses do we have, again? |
| 0x114b75 | 33 | Kind of a pompous dick, isn't he? |
| 0x114b97 | 28 | He's... quite the character. |
| 0x114bb4 | 49 | Never have I met a man whose appearance matched\n |
| 0x114be6 | 29 | his personality so perfectly. |
| 0x114c04 | 47 | It bears mentioning he's foremost among those\n |
| 0x114c34 | 38 | who harbor enmity for my dear brother. |
| 0x114c5b | 9 | ...I see. |
| 0x114c65 | 9 | Nekone... |
| 0x114c6f | 47 | I was expecting something terrible since it's\n |
| 0x114c9f | 46 | one of Ukon's jobs, but at least this one is\n |
| 0x114cce | 7 | simple. |
| 0x114cd6 | 43 | Kiwru, wanna get a drink after we're done\n |
| 0x114d02 | 5 | here? |
| 0x114d08 | 13 | Um... H-Haku? |
| 0x114d16 | 47 | Why're you shaking like that, Nekone? I think\n |
| 0x114d46 | 47 | I saw the bathroom on our way in, if you have\n |
| 0x114d76 | 4 | to-- |
| 0x114d7b | 5 | Bwah! |

## 8. Formato de saida EXIGIDO
Escreva `translations_17_03.json` com a forma:
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
