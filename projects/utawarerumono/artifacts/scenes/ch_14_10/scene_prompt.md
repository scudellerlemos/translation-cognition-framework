# Cena ch_14_10 — pacote de traducao (373 linhas)

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
| Cocopo | Criatura | Cocopo | manter_original | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| toriuma | Criatura | toriuma | manter_original | none |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| woptor | Criatura | woptor | manter_original | none |
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
- **Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)**: **Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo. **Decisões de tradução não-óbvias:** - **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo o EN usa `steed`/`horse` → traduz `montaria`/`cavalo
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `O-OK...` -> `B-Beleza...` (Haku, 11_05)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `but...` -> `mas...` (Kuon, 12_16)
- `trouble.` -> `de verdade.` (Haku, 12_04)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Ngh...` -> `Ngh...` (Haku, 12_04)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `sure.` -> `não.` (Haku, 12_16)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `HURTS.` -> `DOI.` (Haku, 13_01)
- `street.` -> `principal.` (Haku, 14_09)
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

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x9c71f | 49 | After that, we meet up with a delighted-looking\n |
| 0x9c751 | 47 | Rulutieh, and Nekone leads us down main street. |
| 0x9c781 | 30 | There are so many... people... |
| 0x9c7a0 | 46 | It's quite lively. Everyone looks so cheerful. |
| 0x9c7cf | 46 | I guess that's what you get on the main road\n |
| 0x9c7fe | 42 | of the imperial capital. Look at all the\n |
| 0x9c829 | 19 | shops and people... |
| 0x9c83d | 43 | Mhm. But my homeland is just as impressive. |
| 0x9c869 | 48 | I wonder what that was about. I can understand\n |
| 0x9c89a | 49 | patriotism, but she sounds weirdly competitive... |
| 0x9c8cc | 30 | U-Um... Please, wait for me... |
| 0x9c8eb | 47 | Come more this way, Lady Rulutieh. You'll get\n |
| 0x9c91b | 44 | separated if you let the crowd sweep you up. |
| 0x9c948 | 45 | Well then, let's hold hands so we don't get\n |
| 0x9c976 | 10 | separated. |
| 0x9c981 | 7 | O-OK... |
| 0x9c989 | 45 | Kuon holds Rulutieh's hand as she makes the\n |
| 0x9c9b7 | 11 | suggestion. |
| 0x9c9c3 | 25 | OK then. You too, Nekone. |
| 0x9c9dd | 10 | Me... too? |
| 0x9c9e8 | 46 | Mhm. We'd be in trouble if you got separated\n |
| 0x9ca17 | 8 | from us. |
| 0x9ca20 | 45 | She makes it seem like she's doing this for\n |
| 0x9ca4e | 46 | Rulutieh's benefit, but it's clear Kuon just\n |
| 0x9ca7d | 20 | wants to hold hands. |
| 0x9ca92 | 46 | She seems awfully happy and excited, and she\n |
| 0x9cac1 | 33 | has a cheerful smile on her face. |
| 0x9cae3 | 48 | Oh? That looks like... Here, let's check it out. |
| 0x9cb14 | 49 | Kuon seems to have found something, and in high\n |
| 0x9cb46 | 49 | spirits, she pulls the girls towards a colorful\n |
| 0x9cb78 | 6 | stall. |
| 0x9cb7f | 48 | Following behind, I see the shelves are packed\n |
| 0x9cbb0 | 46 | with sculpted candy in vivid reds, blues and\n |
| 0x9cbdf | 8 | yellows. |
| 0x9cbe8 | 27 | Hmm. A candy stall, huh...? |
| 0x9cc04 | 27 | Wow... They're beautiful... |
| 0x9cc20 | 26 | Rulutieh mumbles dreamily. |
| 0x9cc3b | 52 | They really are pretty, all glittering and shining\n |
| 0x9cc70 | 41 | like that. They look almost like jewelry. |
| 0x9cc9a | 47 | Now this is amazing. They can even make stuff\n |
| 0x9ccca | 29 | like this out of candy, huh.  |
| 0x9cce8 | 44 | They're intricately modeled after flowers,\n |
| 0x9cd15 | 47 | animals... and some things I can't recognize.\n |
| 0x9cd45 | 17 | They're gorgeous. |
| 0x9cd57 | 44 | ...I too was amazed by all the sights when\n |
| 0x9cd84 | 31 | I first arrived in the capital. |
| 0x9cda4 | 48 | I had never seen candy crafted like this, even\n |
| 0x9cdd5 | 32 | during festivals in my homeland. |
| 0x9cdf6 | 47 | Yes, I've never seen... such beautiful treats\n |
| 0x9ce26 | 9 | before... |
| 0x9ce30 | 7 | Old man |
| 0x9ce38 | 45 | Hoo hoo! I'm flattered, so I am. Such sweet\n |
| 0x9ce66 | 44 | girlies! Would you like one? I'll give you\n |
| 0x9ce93 | 11 | a discount. |
| 0x9ce9f | 41 | Then we'll take four candies please, sir. |
| 0x9cec9 | 25 | Good, good. Much obliged. |
| 0x9cee3 | 5 | Um... |
| 0x9cee9 | 38 | Don't worry about it. I'll pick it up. |
| 0x9cf10 | 48 | But even conventional sweets are expensive, so\n |
| 0x9cf41 | 42 | a hand-crafted candy like this would be... |
| 0x9cf6c | 10 | Really...? |
| 0x9cf77 | 47 | Don't worry about it. I'm the one that wanted\n |
| 0x9cfa7 | 13 | to have some. |
| 0x9cfb5 | 33 | Which ones do you recommend, sir? |
| 0x9cfd7 | 29 | Hoo hoo hoo, let's see now... |
| 0x9cff5 | 45 | The amiable old candyman pokes through some\n |
| 0x9d023 | 46 | of the candies on sticks, and passes them out. |
| 0x9d052 | 47 | You, young lady, have the beauty and grace of\n |
| 0x9d082 | 46 | a flower... I think a floral candy suits you\n |
| 0x9d0b1 | 11 | finely, eh? |
| 0x9d0bd | 46 | Ahahah, you certainly have a way with words,\n |
| 0x9d0ec | 10 | don't you? |
| 0x9d0f7 | 47 | Despite her words, Kuon looks fairly pleased,\n |
| 0x9d127 | 40 | accepting the large flower-shaped candy. |
| 0x9d150 | 42 | Wow... It looks just like a real flower... |
| 0x9d17b | 50 | Yes, it is quite pretty. It suits you perfectly,\n |
| 0x9d1ae | 12 | dear sister. |
| 0x9d1bb | 46 | Hey, uh... That flower wouldn't happen to be\n |
| 0x9d1ea | 46 | insectivorous? Or have venomous thorns, maybe? |
| 0x9d21d | 43 | And for the sweet little lady there, this\n |
| 0x9d249 | 34 | little birdie should do the trick. |
| 0x9d26c | 44 | Oh, how cute...! It looks just like Cocopo\n |
| 0x9d299 | 24 | did as a little chick... |
| 0x9d2b2 | 48 | It seems like it's shaped like a chubby little\n |
| 0x9d2e3 | 34 | baby bird. It's rather charming... |
| 0x9d306 | 47 | Hee hee... It seems almost a waste to eat it... |
| 0x9d336 | 49 | Size aside, I guess it does look like that bird\n |
| 0x9d368 | 8 | somehow. |
| 0x9d371 | 47 | Though it's hard to accept the idea that THAT\n |
| 0x9d3a1 | 25 | thing was once this cute. |
| 0x9d3bb | 28 | ...Nothing to say this time? |
| 0x9d3d8 | 17 | ...Say? Say what? |
| 0x9d3ea | 28 | Like that it is too "tubby." |
| 0x9d407 | 46 | Perhaps this time it will be "homely-looking." |
| 0x9d436 | 43 | How can you say something like that about\n |
| 0x9d462 | 45 | something this cute? Geez, you guys are mean. |
| 0x9d490 | 4 | Huh? |
| 0x9d495 | 40 | All this stuff about it being tubby or\n |
| 0x9d4be | 15 | homely-looking. |
| 0x9d4ce | 41 | N-No, I-I didn't mean to say that it's... |
| 0x9d4f8 | 41 | Th-That's right. I think it is very cute. |
| 0x9d522 | 49 | You say that, but did you just reveal your true\n |
| 0x9d554 | 12 | feelings...? |
| 0x9d561 | 8 | Gyaagh!! |
| 0x9d56a | 49 | And lastly, for the exceptionally lovely little\n |
| 0x9d59c | 32 | lady... Yes, how about this one? |
| 0x9d5bd | 15 | Oh, how cute... |
| 0x9d5cd | 22 | ...Well, it is cute... |
| 0x9d5e4 | 49 | Compared to the candies that the other two got,\n |
| 0x9d616 | 27 | this one is twice as large. |
| 0x9d632 | 18 | Why is mine so...? |
| 0x9d645 | 23 | Nekone is also baffled. |
| 0x9d65d | 48 | It doesn't feel like it's the first time we've\n |
| 0x9d68e | 45 | met, so it's just a little extra now, girlie. |
| 0x9d6bc | 6 | But... |
| 0x9d6c3 | 38 | Hoo hoo! No extra charge, of course.\n |
| 0x9d6ea | 16 | No need to fuss. |
| 0x9d6fb | 44 | Saying that, he gives Nekone a knowing wink. |
| 0x9d728 | 41 | So I guess she's this old man's type...\n |
| 0x9d752 | 24 | He's got strange tastes. |
| 0x9d76b | 34 | Is this... the divine beast, Nuko? |
| 0x9d78e | 46 | Nuko? The creature from... all the old fairy\n |
| 0x9d7bd | 8 | tales..? |
| 0x9d7c6 | 49 | Yes. It would toy with people on a whim, but it\n |
| 0x9d7f8 | 47 | would help from the shadows if someone was in\n |
| 0x9d828 | 9 | trouble.  |
| 0x9d832 | 46 | That certainly is just like Nekone, I think.\n |
| 0x9d861 | 44 | There's something cute about it hiding its\n |
| 0x9d88e | 12 | true nature. |
| 0x9d89b | 48 | It definitely is adorable at first glance, but\n |
| 0x9d8cc | 51 | I think its true nature might be a vicious beast... |
| 0x9d900 | 46 | And this one should be perfect for you, m'boy! |
| 0x9d92f | 6 | Hm? \n |
| 0x9d936 | 14 | Oh, thank y... |
| 0x9d945 | 48 | My words fail me. Before me is a shape I hoped\n |
| 0x9d976 | 48 | never to see again... but on the end of a stick. |
| 0x9d9a7 | 44 | Wait a second. What is this... gigiri candy? |
| 0x9d9d4 | 43 | And unlike the others, this one is almost\n |
| 0x9da00 | 47 | offensively realistic. It's well-made, but...\n |
| 0x9da30 | 11 | disgusting. |
| 0x9da3c | 45 | The fruits of my painstaking labor! I'd say\n |
| 0x9da6a | 44 | you're worthy of receiving this work of art. |
| 0x9da97 | 50 | I think I prefer my art abstract. It could start\n |
| 0x9daca | 48 | moving any second... Is this just a bug coated\n |
| 0x9dafb | 9 | in candy? |
| 0x9db05 | 43 | No need to be modest. Go ahead and take a\n |
| 0x9db31 | 34 | big old bite. Start with the head! |
| 0x9db54 | 22 | Mmm... It's delicious! |
| 0x9db6b | 42 | Yes... It's so sweet, and very refreshing. |
| 0x9db96 | 44 | It is fruit flavored. You should stop your\n |
| 0x9dbc3 | 36 | complaining--hurry up and eat yours. |
| 0x9dbe8 | 6 | Ngh... |
| 0x9dbef | 45 | Paying me no heed, Kuon and the others lick\n |
| 0x9dc1d | 32 | contentedly at their candy pops. |
| 0x9dc3e | 48 | I look between my candy and theirs, going back\n |
| 0x9dc6f | 46 | and forth several times, but they don't even\n |
| 0x9dc9e | 10 | notice me. |
| 0x9dca9 | 47 | Maybe it's just me, but it feels like the gap\n |
| 0x9dcd9 | 34 | is widening between them and me... |
| 0x9dcfc | 48 | What's wrong, eh? You're not gonna tell me you\n |
| 0x9dd2d | 28 | don't like my work, are you? |
| 0x9dd4a | 49 | Come on, who can eat something as creepy as this? |
| 0x9dd7c | 51 | Quit complaining and eat the damn thing. It suits\n |
| 0x9ddb0 | 42 | a man ferrying around these lovely ladies! |
| 0x9dddb | 47 | This old fart's attitude clearly changes when\n |
| 0x9de0b | 21 | he's talking to me... |
| 0x9de21 | 23 | ...*grumble, rumble*... |
| 0x9de39 | 6 | ...Hm? |
| 0x9de40 | 49 | During our little exchange, the already-crowded\n |
| 0x9de72 | 41 | main street seems to have gotten noisier. |
| 0x9de9c | 23 | Oh, it's Lord Oshtor... |
| 0x9deb4 | 15 | Lord Oshtor...! |
| 0x9dec4 | 48 | As I turn to see what's going on, the shoppers\n |
| 0x9def5 | 44 | all shift to the roadside, clearing the way. |
| 0x9df22 | 5 | Ah... |
| 0x9df28 | 43 | Nekone's eyes widen, as though she's just\n |
| 0x9df54 | 20 | realizing something. |
| 0x9df69 | 19 | What's going on...? |
| 0x9df7d | 47 | From down the road, a group of several people\n |
| 0x9dfad | 46 | riding woptors are stoically heading this way. |
| 0x9dfdc | 14 | That man is... |
| 0x9dfeb | 50 | It's... that masked man. That guy that commanded\n |
| 0x9e01e | 43 | the subjugation of the bandits back then... |
| 0x9e04a | 40 | If I remember correctly, his name was... |
| 0x9e073 | 38 | Oshtor, Imperial Guard of the Right... |
| 0x9e09a | 42 | That's right, Oshtor... That was the name. |
| 0x9e0c5 | 50 | The people stare, watching the man in the center\n |
| 0x9e0f8 | 28 | of the unit from a distance. |
| 0x9e115 | 19 | Oh, Lord Oshtor...! |
| 0x9e129 | 14 | Lord Oshtor... |
| 0x9e138 | 46 | The excited murmurs of the girls from market\n |
| 0x9e167 | 15 | rise around us. |
| 0x9e177 | 49 | I can see a lot of things in their eyes as they\n |
| 0x9e1a9 | 46 | watch him. Reverence, admiration, affection,\n |
| 0x9e1d8 | 12 | and trust... |
| 0x9e1e5 | 48 | Whatever the Imperial Guard of the Right does,\n |
| 0x9e216 | 26 | he definitely is famous... |
| 0x9e231 | 45 | Huh? Oh... I don't think there is anyone in\n |
| 0x9e25f | 45 | Yamato... that doesn't know of Lord Oshtor... |
| 0x9e28d | 39 | Rulutieh replies as I mutter to myself. |
| 0x9e2b5 | 20 | He's that famous...? |
| 0x9e2ca | 46 | Eh now? What kind of country bumpkin doesn't\n |
| 0x9e2f9 | 15 | know of Oshtor? |
| 0x9e309 | 44 | Ahahah, we've been traveling quite a ways,\n |
| 0x9e336 | 44 | and we just came to this city the other day. |
| 0x9e363 | 31 | Aha, I see. That might do it.\n |
| 0x9e383 | 26 | S'pose it can't be helped. |
| 0x9e39e | 47 | Ahem! He is the very equal of Lord Mikazuchi,\n |
| 0x9e3ce | 43 | Imperial Guard of the Left and one of the\n |
| 0x9e3fa | 25 | Twin Shields of Yamato... |
| 0x9e414 | 45 | Lord Oshtor, the Imperial Guard of the Right. |
| 0x9e442 | 45 | Even though he's a busy man, he goes out to\n |
| 0x9e470 | 38 | patrol the city like this on occasion. |
| 0x9e497 | 45 | The old man bows his head to the patrolling\n |
| 0x9e4c5 | 22 | party as they pass by. |
| 0x9e4dc | 42 | He's a man of distinction! Versed in the\n |
| 0x9e507 | 40 | literary and military arts, honorable,\n |
| 0x9e530 | 24 | and a man of the people! |
| 0x9e549 | 40 | Why, it's thanks to Lord Mikazuchi and\n |
| 0x9e572 | 47 | Lord Oshtor that life in our imperial capital\n |
| 0x9e5a2 | 15 | is so peaceful. |
| 0x9e5b2 | 6 | Hmm... |
| 0x9e5b9 | 39 | It seems like he certainly is adored.\n |
| 0x9e5e1 | 43 | I had a feeling he was, but I didn't know\n |
| 0x9e60d | 15 | to this extent. |
| 0x9e61d | 6 | Yes... |
| 0x9e624 | 50 | Rulutieh follows the Imperial Guard of the Right\n |
| 0x9e657 | 29 | with her eyes as she replies. |
| 0x9e675 | 49 | I wonder why it's been so quiet, and then I see\n |
| 0x9e6a7 | 48 | Nekone blushing as she stares at the man, in a\n |
| 0x9e6d8 | 5 | daze. |
| 0x9e6de | 38 | She looks like a young maiden in love. |
| 0x9e705 | 30 | Heheh... What's wrong, Nekone? |
| 0x9e724 | 47 | ...Huh? Uh, n-nothing is wrong! Nothing at all! |
| 0x9e754 | 15 | Her too, huh... |
| 0x9e764 | 47 | He's gotta be quite a guy to enthrall a young\n |
| 0x9e794 | 15 | girl like that. |
| 0x9e7a4 | 47 | I don't know this Mikazuchi, but Oshtor seems\n |
| 0x9e7d4 | 23 | like a pretty big deal. |
| 0x9e7ec | 31 | Whaddaya mean you "don't know"? |
| 0x9e80c | 50 | It's true that Lord Oshtor's renowned in Yamato,\n |
| 0x9e83f | 5 | sure. |
| 0x9e845 | 50 | But it's always the ones that keep their talents\n |
| 0x9e878 | 41 | hidden, right, that have the REAL skills. |
| 0x9e8a2 | 46 | Lord Mikazuchi, aye! Now there's a man TRULY\n |
| 0x9e8d1 | 23 | worthy of being adored! |
| 0x9e8e9 | 49 | His strength in battle! His silent care for the\n |
| 0x9e91b | 43 | people of the city! His chivalry to young\n |
| 0x9e947 | 11 | girlies...! |
| 0x9e953 | 48 | You can say he's as good as Lord Oshtor in all\n |
| 0x9e984 | 50 | things--he's better than Lord Oshtor in every way! |
| 0x9e9b7 | 10 | ...Right.  |
| 0x9e9c2 | 47 | Hey, what's with the half-assed response, kid!? |
| 0x9e9f2 | 46 | Rulutieh, is what this old guy is saying true? |
| 0x9ea21 | 44 | Yes... There isn't a person in Yamato that\n |
| 0x9ea4e | 28 | doesn't know Lord Mikazuchi. |
| 0x9ea6b | 52 | ...If Lord Oshtor is kindness, then Lord Mikazuchi\n |
| 0x9eaa0 | 49 | is strength. They are equally ranked in that way. |
| 0x9ead2 | 8 | I see... |
| 0x9eadb | 48 | Even if I'm told how great these two guys are,\n |
| 0x9eb0c | 32 | it just feels unrealistic to me. |
| 0x9eb2d | 31 | Have you met him too, Nekone?\n |
| 0x9eb4d | 19 | This Mikazuchi guy? |
| 0x9eb61 | 17 | Lord Mikazuchi... |
| 0x9eb73 | 30 | I do not care for his company. |
| 0x9eb92 | 47 | She answers awkwardly after a brief moment of\n |
| 0x9ebc2 | 8 | silence. |
| 0x9ebcb | 45 | For some reason, the old man suddenly flops\n |
| 0x9ebf9 | 44 | forward, facedown on the stall's countertop. |
| 0x9ec26 | 50 | I get that the Twin Shields of Yamato are adored\n |
| 0x9ec59 | 16 | by the public... |
| 0x9ec6a | 43 | But the more I hear about them, it starts\n |
| 0x9ec96 | 48 | sounding too excessive, and it starts sounding\n |
| 0x9ecc7 | 15 | really dubious. |
| 0x9ecd7 | 45 | Who're ya callin' a dubious old man now, eh!? |
| 0x9ed05 | 42 | No, not you. I'm talking about that man,\n |
| 0x9ed30 | 7 | Oshtor. |
| 0x9ed38 | 35 | Hngh--And what do you mean by that? |
| 0x9ed5c | 46 | Maybe she takes offense at my musing--Nekone\n |
| 0x9ed8b | 46 | turns on me with an unusual sharpness to her\n |
| 0x9edba | 5 | tone. |
| 0x9edc0 | 46 | Well, people normally have one or two things\n |
| 0x9edef | 17 | to be ashamed of. |
| 0x9ee01 | 46 | I just get suspicious when I hear about some\n |
| 0x9ee30 | 44 | paragon of virtue with no skeletons in his\n |
| 0x9ee5d | 7 | closet. |
| 0x9ee65 | 35 | Wh...What are you talking about!?\n |
| 0x9ee89 | 25 | He has no such blemishes! |
| 0x9eea3 | 48 | Nekone denies it so furiously, it almost looks\n |
| 0x9eed4 | 35 | like her hairs are standing on end. |
| 0x9eef8 | 50 | Come on, it's fine if he has a few weird quirks!\n |
| 0x9ef2b | 42 | People would feel closer to him if he did. |
| 0x9ef56 | 50 | Maybe he's a huge voyeur. Maybe he likes wearing\n |
| 0x9ef89 | 49 | frilly dresses now and then. It'd make him more\n |
| 0x9efbb | 10 | relatable. |
| 0x9efc6 | 20 | *Thud, thud, thud--* |
| 0x9efdb | 46 | Without saying a word, Nekone starts kicking\n |
| 0x9f00a | 27 | me in the shins repeatedly. |
| 0x9f026 | 39 | Ow, ow, OW--Hey, ow, stop kicking me,\n |
| 0x9f04e | 16 | stop KICKING me! |
| 0x9f05f | 46 | Why are you so angry? It's fine if he's like\n |
| 0x9f08e | 15 | that, isn't it? |
| 0x9f09e | 45 | Ngh... She's tiny, so her kicks aren't that\n |
| 0x9f0cc | 45 | powerful, but being booted repeatedly still\n |
| 0x9f0fa | 6 | hurts. |
| 0x9f101 | 46 | Hemph! Serves you right. That's what you get\n |
| 0x9f130 | 43 | for saying something that oughtn't be said. |
| 0x9f15c | 43 | You wouldn't get off so easy if the other\n |
| 0x9f188 | 43 | girlies heard you. You oughta be grateful\n |
| 0x9f1b4 | 16 | to these ladies. |
| 0x9f1c5 | 44 | So in other words, they're the same as the\n |
| 0x9f1f2 | 46 | fangirls in the crowd that were just cheering. |
| 0x9f221 | 47 | Nekone kicks my shin even harder, as if she's\n |
| 0x9f251 | 16 | reading my mind. |
| 0x9f262 | 42 | Mhm. I suppose there's nothing to be done. |
| 0x9f28d | 48 | Gah... This Oshtor guy's even got this vicious\n |
| 0x9f2be | 45 | girl head over heels for him. How terrifying. |
| 0x9f2ec | 47 | Ngh... Wait... Stop... It's actually starting\n |
| 0x9f31c | 14 | to hurt now... |
| 0x9f32b | 44 | Damn it, everything is that guy's fault...\n |
| 0x9f358 | 46 | As I look to the procession, I see that he's\n |
| 0x9f387 | 42 | stopped his steed, staring straight at us. |
| 0x9f3b2 | 50 | Those sharp eyes behind that mask are fixed on us. |
| 0x9f3e5 | 46 | ...Hey, your Lord Oshtor's looking this way.\n |
| 0x9f414 | 42 | And while you're being so unladylike, too. |
| 0x9f43f | 43 | Do you think I could be fooled by such an\n |
| 0x9f46b | 18 | obvious... lie...? |
| 0x9f47e | 50 | Despite her words, Nekone's gaze flickers toward\n |
| 0x9f4b1 | 23 | Uh... er... A-Ah, uh... |
| 0x9f4c9 | 52 | Her eyes meet Oshtor's, and her cheeks immediately\n |
| 0x9f4fe | 16 | turn bright red. |
| 0x9f50f | 47 | Maybe I'm imagining things, but for a moment,\n |
| 0x9f53f | 38 | it looks almost like Oshtor's smiling. |
| 0x9f566 | 44 | And then the moment passes. The procession\n |
| 0x9f593 | 46 | continues on, fading into the far end of the\n |
| 0x9f5c2 | 7 | street. |
| 0x9f5ca | 48 | After a while, the road goes back to its usual\n |
| 0x9f5fb | 18 | hustle and bustle. |
| 0x9f60e | 51 | Young maidens chatter with girlish glee about how\n |
| 0x9f642 | 49 | their eyes met his, or that he saw them waving... |
| 0x9f674 | 44 | Aren't you lucky. You're probably the only\n |
| 0x9f6a1 | 20 | person he smiled at. |
| 0x9f6b6 | 10 | *Thunk*--! |
| 0x9f6c1 | 8 | Ghurgh!! |
| 0x9f6ca | 50 | Nekone's expression changes from shame to anger,\n |
| 0x9f6fd | 45 | and she headbutts me directly in the stomach. |
| 0x9f72b | 26 | Wh-What was... that for... |
| 0x9f746 | 47 | Kuon and Rulutieh stare at me with wry smiles\n |
| 0x9f776 | 48 | as I struggle to regain control of my breathing. |
| 0x9f7a7 | 51 | *Sigh*... You really shouldn't play with a girl's\n |
| 0x9f7db | 49 | feelings, I think. That can only lead to trouble. |
| 0x9f80d | 42 | I-I don't understand what you're saying... |
| 0x9f838 | 19 | *Hiss, hiss, hiss!* |
| 0x9f84c | 47 | Urgh, she's still angry. Only one thing to do\n |
| 0x9f87c | 22 | in times like these... |
| 0x9f893 | 50 | I'm not sure what's the matter, but it's clearly\n |
| 0x9f8c6 | 46 | my fault. You can have my candy, so calm down. |
| 0x9f8f5 | 52 | I shove the candy I'm holding into Nekone's mouth,\n |
| 0x9f92a | 31 | in an attempt to calm her down. |
| 0x9f94a | 44 | They say sweet things enrich the heart, or\n |
| 0x9f977 | 15 | something. Yep. |
| 0x9f987 | 7 | Nrgh--! |
| 0x9f98f | 43 | Ugh, wh-what did you make me eat all of a\n |
| 0x9f9bb | 8 | sudden!? |
| 0x9f9c4 | 45 | What...? Just candy. I haven't put my mouth\n |
| 0x9f9f2 | 39 | on it or anything... It should be fine. |
| 0x9fa1a | 43 | That's not the poin--Egh, what is... this\n |
| 0x9fa46 | 18 | bizarre flavor...? |
| 0x9fa59 | 50 | It's insect flavored. An acquired taste, as they\n |
| 0x9fa8c | 48 | call it. I had a hard time getting it to taste\n |
| 0x9fabd | 28 | like the real thing, hoo my! |
| 0x9fada | 9 | *Thud--*! |
| 0x9fae4 | 12 | Dwaaargh--!! |

## 8. Formato de saida EXIGIDO
Escreva `translations_14_10.json` com a forma:
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
