# Cena ch_15_03 — pacote de traducao (386 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Divine Scion | Titulo | Descendente Divino | traduzir | moderate |
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `yourself.` -> `abalado.` (Kuon, 13_01)
- `Oh?` -> `Oh?` (Haku, 14_04)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
- `Is that so?` -> `É mesmo?` (Nekone, 15_02)
- `capital.` -> `imperial.` (Kuon, 12_04)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `though.` -> `porém.` (Kuon, 12_04)
- `Uh...` -> `Ahn...` (Haku, 14_03)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `them.` -> `deles.` (Kuon, 11_05)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Nekone!` -> `Nekone!` (Homens, 14_04)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Gyeh!?` -> `Gueh!?` (Maroro, 12_07)
- `acquaintance.` -> `conhecer você.` (Kuon, 13_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `U-Um...` -> `E-Ei...` (Rulutieh, 14_09)
- `approach.` -> `chegar.` (Haku, 15_01)
- `but...` -> `mas...` (Kuon, 12_16)
- `me?` -> `mim?` (Maroro, 12_13)
- `dear sister?` -> `cara irmã?` (Nekone, 15_01)
- `Is something the matter?` -> `Aconteceu alguma coisa?` (Kuon, 12_09)
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
| 0xb3196 | 50 | Somehow, even more bodies pack the market street\n |
| 0xb31c9 | 41 | than usual, making it nigh-untraversable. |
| 0xb31f3 | 46 | Yeesh. Isn't this a bigger crowd than usual?\n |
| 0xb3222 | 46 | I'm having trouble walking through all this... |
| 0xb3251 | 21 | Are you OK, Rulutieh? |
| 0xb3267 | 48 | Yes, I'm... I'm all ri--O-Oh, sorry, excuse me-- |
| 0xb3298 | 48 | The streets are always like this, this time of\n |
| 0xb32c9 | 5 | year. |
| 0xb32cf | 27 | Is something big happening? |
| 0xb32eb | 43 | Yes. Look there--they appear to have just\n |
| 0xb3317 | 8 | arrived. |
| 0xb3320 | 43 | Nekone points down the road, indicating a\n |
| 0xb334c | 45 | colorful, garish procession parading toward\n |
| 0xb337a | 3 | us. |
| 0xb337e | 16 | ...What is that? |
| 0xb338f | 49 | A large, embellished cart, inlaid with gold and\n |
| 0xb33c1 | 51 | silver filigree, leads a caravan of others like it. |
| 0xb33f5 | 49 | The capital will be playing host to a number of\n |
| 0xb3427 | 47 | owlos and their families as the nativity nears. |
| 0xb3457 | 48 | Each will pledge their loyalty to the imperial\n |
| 0xb3488 | 46 | princess, who someday will take the Mikado's\n |
| 0xb34b7 | 7 | throne. |
| 0xb34bf | 43 | Hm. So, kids from well-to-do families are\n |
| 0xb34eb | 33 | coming to the capital for that... |
| 0xb350d | 48 | Awful lot of trouble to go through just to bow\n |
| 0xb353e | 25 | to someone and head home. |
| 0xb3558 | 46 | A truth I do not deny, but it would probably\n |
| 0xb3587 | 41 | be best to keep that kind of comment to\n |
| 0xb35b1 | 9 | yourself. |
| 0xb35bb | 3 | Oh? |
| 0xb35bf | 46 | Not everyone shares in the temperament of my\n |
| 0xb35ee | 24 | dear br--of Lord Oshtor. |
| 0xb3607 | 45 | Her Highness Princess Anju is the only heir\n |
| 0xb3635 | 38 | to the Mikado. A true Divine Scion--\n |
| 0xb365c | 39 | the blood of the God Incarnate himself. |
| 0xb3684 | 48 | A great many people in the capital--no, all in\n |
| 0xb36b5 | 46 | Yamato, have devoted their very lives to her\n |
| 0xb36e4 | 5 | name. |
| 0xb36ea | 45 | Lord Oshtor may let your japes pass, but if\n |
| 0xb3718 | 42 | such remarks fall on less tolerant ears... |
| 0xb3743 | 46 | You may find yourself vanishing one day, you\n |
| 0xb3772 | 11 | understand. |
| 0xb377e | 10 | I-I see... |
| 0xb3789 | 48 | Nekone's matter-of-fact tone is unnerving, but\n |
| 0xb37ba | 41 | she's stating fact--she's not trying to\n |
| 0xb37e4 | 14 | intimidate me. |
| 0xb37f3 | 21 | That's... unexpected. |
| 0xb3809 | 8 | What is? |
| 0xb3812 | 44 | That you'd show actual concern for me, for\n |
| 0xb383f | 5 | once. |
| 0xb3845 | 46 | It would have a negative impact on my mental\n |
| 0xb3874 | 45 | health if an acquaintance just disappeared.\n |
| 0xb38a2 | 17 | I get bad dreams. |
| 0xb38b4 | 11 | Is that so? |
| 0xb38c0 | 41 | So it... wasn't actually a threat, or...? |
| 0xb38ea | 48 | Besides, the nativity festival is far from the\n |
| 0xb391b | 27 | only reason they have come. |
| 0xb3937 | 52 | The festival aside, influential families typically\n |
| 0xb396c | 46 | send their heirs to the city around this time. |
| 0xb399b | 50 | Once they arrive, they will spend years studying\n |
| 0xb39ce | 43 | here, acquiring the skills needed for rule. |
| 0xb39fa | 44 | Some apprentice themselves to the greatest\n |
| 0xb3a27 | 45 | scholars in the empire, devoting themselves\n |
| 0xb3a55 | 14 | to academia... |
| 0xb3a64 | 46 | Others who excel in the arts of war can also\n |
| 0xb3a93 | 45 | find mentors among the famed masters of the\n |
| 0xb3ac1 | 8 | capital. |
| 0xb3aca | 31 | Is that all true...? Amazing... |
| 0xb3aea | 43 | Um... You, ah. You are one of those heirs\n |
| 0xb3b16 | 24 | yourself, Lady Rulutieh. |
| 0xb3b2f | 3 | Eh? |
| 0xb3b33 | 30 | Rulutieh exclaims in surprise. |
| 0xb3b52 | 24 | Were you, um... unaware? |
| 0xb3b6b | 46 | I-I was only told... to deliver my country's\n |
| 0xb3b9a | 34 | tribute... t-to the Mikado, as a\n |
| 0xb3bbd | 17 | representative... |
| 0xb3bcf | 47 | Your father might've kept the true reason for\n |
| 0xb3bff | 46 | your visit a secret. To keep your anxiety at\n |
| 0xb3c2e | 11 | bay, maybe? |
| 0xb3c3a | 5 | Oh... |
| 0xb3c40 | 48 | Now that she mentions it, that feels like it's\n |
| 0xb3c71 | 18 | probably the case. |
| 0xb3c84 | 47 | I only say so because your father sounds like\n |
| 0xb3cb4 | 35 | he loves you quite a lot, Rulutieh. |
| 0xb3cdc | 46 | This whole thing is thought out pretty well,\n |
| 0xb3d0b | 7 | though. |
| 0xb3d13 | 46 | This power structure. Making the capital the\n |
| 0xb3d42 | 46 | center of learning for noble scions instills\n |
| 0xb3d71 | 8 | loyalty. |
| 0xb3d7a | 46 | Early exposure to its power quells any seeds\n |
| 0xb3da9 | 44 | of defiance, and noble coin stimulates the\n |
| 0xb3dd6 | 14 | local economy. |
| 0xb3de5 | 47 | And those are just the advantages I can think\n |
| 0xb3e15 | 38 | of right now. I'm sure there are more. |
| 0xb3e3c | 41 | Just as I expected of you, dear sister.\n |
| 0xb3e66 | 37 | You grasped the implications quickly. |
| 0xb3e8c | 43 | Nekone smiles proudly, glancing back at me. |
| 0xb3eb8 | 27 | What's with that smug look? |
| 0xb3ed4 | 31 | I realized as much too, y'know. |
| 0xb3ef4 | 48 | It's clever. At any time, the capital can keep\n |
| 0xb3f25 | 42 | its vassals in check by holding the kids\n |
| 0xb3f50 | 8 | hostage. |
| 0xb3f59 | 5 | Uh... |
| 0xb3f5f | 3 | Hm? |
| 0xb3f63 | 47 | I was... deliberately not mentioning that part. |
| 0xb3f93 | 34 | Kuon sighs deeply for some reason. |
| 0xb3fb6 | 6 | Hrm... |
| 0xb3fbd | 7 | ...Huh. |
| 0xb3fc5 | 27 | Oh--N-No, that was just--\n |
| 0xb3fe1 | 15 | I didn't mean-- |
| 0xb3ff1 | 49 | No, I... I don't mind, so... Please don't worry\n |
| 0xb4023 | 11 | about me... |
| 0xb402f | 46 | Urgh, now I've just made her worry about me,\n |
| 0xb405e | 8 | instead. |
| 0xb4067 | 48 | As our conversation carries on, the procession\n |
| 0xb4098 | 22 | passes by our group... |
| 0xb40af | 37 | Man, what a flashy display, though.\n |
| 0xb40d5 | 45 | Between the gaudy clothes, the singing, the\n |
| 0xb4103 | 10 | dancing... |
| 0xb410e | 37 | It's like a festival all unto itself. |
| 0xb4134 | 41 | Way different than when we arrived with\n |
| 0xb415e | 26 | Rulutieh, that's for sure. |
| 0xb4179 | 49 | Rulutieh seems to be in the same class as these\n |
| 0xb41ab | 45 | guys, but she's... really plain compared to\n |
| 0xb41d9 | 5 | them. |
| 0xb41df | 48 | Then again, I'd be at a total loss if she told\n |
| 0xb4210 | 49 | me to dress like that and put on a dance number\n |
| 0xb4242 | 8 | for her. |
| 0xb424b | 47 | Savvy families often flaunt their wealth like\n |
| 0xb427b | 46 | this to project power. It is to be expected,\n |
| 0xb42aa | 7 | really. |
| 0xb42b2 | 48 | That festivals and celebrations are so popular\n |
| 0xb42e3 | 47 | with the commonfolk only spurs these debacles\n |
| 0xb4313 | 3 | on. |
| 0xb4317 | 48 | Well, it's nothing if not a golden opportunity\n |
| 0xb4348 | 29 | for the nobility to show off. |
| 0xb4366 | 49 | Anyone with notions of upward mobility is going\n |
| 0xb4398 | 44 | to be vying for renown and public adoration. |
| 0xb43c5 | 44 | Personally, I find it tacky. The unbridled\n |
| 0xb43f2 | 43 | egotism on display is disgraceful, not to\n |
| 0xb441e | 14 | mention noisy. |
| 0xb442d | 49 | It also breeds an unseemly phenomenon of people\n |
| 0xb445f | 46 | going above their means to put on airs for it. |
| 0xb448e | 48 | Whole families will lead frugal lives just for\n |
| 0xb44bf | 46 | this chance to make an extravagant, wasteful\n |
| 0xb44ee | 6 | debut. |
| 0xb44f5 | 53 | I see. Garish stuff like this isn't really Nekone's\n |
| 0xb452b | 17 | cup of tea, then. |
| 0xb453d | 48 | She seems to avoid noise and chaos in general,\n |
| 0xb456e | 31 | so I guess it's understandable. |
| 0xb458e | 47 | We all watch the first cart in the procession\n |
| 0xb45be | 48 | go by, and before long, another follows behind\n |
| 0xb45ef | 3 | it. |
| 0xb45f3 | 32 | Now, that's an awfully drab one. |
| 0xb4614 | 44 | I want to be able to say it's drab only by\n |
| 0xb4641 | 47 | comparison to the others, but... it's really,\n |
| 0xb4671 | 12 | REALLY drab. |
| 0xb467e | 47 | The cart we brought Rulutieh in on wasn't too\n |
| 0xb46ae | 49 | flashy. Some colorful decorations, but tasteful\n |
| 0xb46e0 | 5 | ones. |
| 0xb46e6 | 47 | Hardly any decorations or ornaments adorn the\n |
| 0xb4716 | 24 | approaching cart at all. |
| 0xb472f | 48 | "Strong, simple elegance" is a fine aesthetic,\n |
| 0xb4760 | 44 | but done wrong, it can just look like farm\n |
| 0xb478d | 10 | equipment. |
| 0xb4798 | 46 | It doesn't look to be dirty or beaten-up, at\n |
| 0xb47c7 | 8 | least... |
| 0xb47d0 | 45 | The crowd that had gathered to watch slowly\n |
| 0xb47fe | 36 | begins to splinter, losing interest. |
| 0xb4823 | 44 | Is something simple like that more to your\n |
| 0xb4850 | 13 | liking, then? |
| 0xb485e | 7 | Urgh... |
| 0xb4866 | 47 | For some reason, Nekone averts her eyes in...\n |
| 0xb4896 | 14 | embarrassment? |
| 0xb48a5 | 7 | Nekone! |
| 0xb48ad | 45 | Then, a voice cuts through the noise of the\n |
| 0xb48db | 29 | crowd, calling Nekone's name. |
| 0xb48f9 | 48 | As I look around for the source of it, my eyes\n |
| 0xb492a | 38 | land on a young boy, waving from the\n |
| 0xb4951 | 18 | drab-looking cart. |
| 0xb4964 | 16 | Do you know him? |
| 0xb4975 | 6 | Hhnnh. |
| 0xb497c | 25 | Nekone scowls wordlessly. |
| 0xb4996 | 45 | The boy dismounts from the cart, running at\n |
| 0xb49c4 | 24 | full tilt toward Nekone. |
| 0xb49dd | 3 | Boy |
| 0xb49e1 | 47 | It's been so long, Nekone! I didn't think I'd\n |
| 0xb4a11 | 47 | see you as soon as I arrived. I'm so happy to\n |
| 0xb4a41 | 8 | see you! |
| 0xb4a4a | 9 | ...Hello. |
| 0xb4a54 | 27 | I'm glad to see you well.\n |
| 0xb4a70 | 20 | What's new with you? |
| 0xb4a85 | 16 | Nothing, really. |
| 0xb4a96 | 48 | The boy speaks to Nekone like they're lifelong\n |
| 0xb4ac7 | 46 | friends, but her responses are conspicuously\n |
| 0xb4af6 | 5 | curt. |
| 0xb4afc | 44 | Her attitude about this whole situation is\n |
| 0xb4b29 | 46 | pretty clear, but he doesn't seem to get the\n |
| 0xb4b58 | 8 | picture. |
| 0xb4b61 | 46 | If they're friends, Nekone's being unusually\n |
| 0xb4b90 | 5 | cold. |
| 0xb4b96 | 50 | He looks to be a good-natured young man, though.\n |
| 0xb4bc9 | 45 | Not the type to really... be disliked easily. |
| 0xb4bf7 | 48 | If anything, he's the kind of pretty boy older\n |
| 0xb4c28 | 46 | women who like that kind of stuff would fawn\n |
| 0xb4c57 | 5 | over. |
| 0xb4c5d | 39 | Allow me to introduce you. This is my\n |
| 0xb4c85 | 18 | countryman, Kiwru. |
| 0xb4c98 | 48 | The boy--Kiwru--looks disappointed at Nekone's\n |
| 0xb4cc9 | 45 | overly brief introduction, and he bows to us. |
| 0xb4cf7 | 36 | Ah, you're Nekone's acquaintances?\n |
| 0xb4d1c | 40 | Forgive me for not introducing myself.\n |
| 0xb4d45 | 25 | I am Kiwru, of Ennakamuy. |
| 0xb4d5f | 39 | Nice to meet you. You can call me Kuon. |
| 0xb4d87 | 31 | Dear sister is an apothecary.\n |
| 0xb4da7 | 35 | She is a very knowledgeable person. |
| 0xb4dcb | 32 | I see. An apothecary... {W260}\n |
| 0xb4dec | 24 | But, um? Dear... sister? |
| 0xb4e05 | 44 | Not my blood relative, to be clear. She is\n |
| 0xb4e32 | 46 | someone I admire as a cherished, sworn sister. |
| 0xb4e61 | 41 | O-Oh, I see. That just... surprised me.\n |
| 0xb4e8b | 43 | Especially from you, of all people, Nekone. |
| 0xb4eb7 | 26 | The boy glances at Kuon... |
| 0xb4ed2 | 44 | When she smiles back at him, he freezes as\n |
| 0xb4eff | 17 | though entranced. |
| 0xb4f11 | 8 | ...Bwuh. |
| 0xb4f1a | 48 | Soon enough, he averts his eyes, snapping back\n |
| 0xb4f4b | 13 | to attention. |
| 0xb4f59 | 49 | Captivated by Kuon's gentle outward appearance,\n |
| 0xb4f8b | 7 | huh...? |
| 0xb4f93 | 47 | Don't be fooled, kid. Her true colors are far\n |
| 0xb4fc3 | 12 | worse than-- |
| 0xb4fd0 | 9 | *WHUNK*\n |
| 0xb4fda | 7 | *THWAP* |
| 0xb4fe2 | 6 | Gyeh!? |
| 0xb4fe9 | 48 | Kuon's elbow and Nekone's shin connect with me\n |
| 0xb501a | 47 | before I can finish the thought. How did they-- |
| 0xb504a | 44 | This is Lady Rulutieh, a companion of ours\n |
| 0xb5077 | 15 | for... reasons. |
| 0xb5087 | 45 | Oh... I-I am... Rulutieh of Kujyuri. It's a\n |
| 0xb50b5 | 37 | pleasure to make your acquaintance... |
| 0xb50db | 28 | Rulutieh... of Kujyuri...?\n |
| 0xb50f8 | 15 | Could you be... |
| 0xb5108 | 40 | Ah, n-never mind. Pleased to make your\n |
| 0xb5131 | 13 | acquaintance. |
| 0xb513f | 44 | Ah... Sir Kiwru of Ennakamuy, you wouldn't\n |
| 0xb516c | 16 | happen to be...? |
| 0xb517d | 38 | Just as I thought. You're, ah, also... |
| 0xb51a4 | 28 | I-I'm very glad to meet you. |
| 0xb51c1 | 28 | No, the pleasure's all mine. |
| 0xb51de | 48 | What's this strange vibe they're giving me...?\n |
| 0xb520f | 24 | Oh, looks like I'm next. |
| 0xb5228 | 47 | I straighten myself and prepare to greet Kiwru. |
| 0xb5258 | 13 | This is Haku. |
| 0xb5266 | 15 | ...That is all. |
| 0xb5276 | 4 | Huh? |
| 0xb527b | 46 | Hey, come on. That's it? Why'd you stop there? |
| 0xb52aa | 48 | Tiresome explanations bore me. Especially when\n |
| 0xb52db | 40 | there is little of substance to explain. |
| 0xb5304 | 33 | What? There's a bunch of stuff.\n |
| 0xb5326 | 20 | Like... a WHOLE lot. |
| 0xb533b | 48 | I don't hear you volunteering any information.\n |
| 0xb536c | 45 | Presumptuous of you, to ask me to do it for\n |
| 0xb539a | 4 | you. |
| 0xb539f | 31 | Then, how should I put this...? |
| 0xb53bf | 47 | What about how reliable I am, or trustworthy,\n |
| 0xb53ef | 37 | or how I'm like another dear brother. |
| 0xb5415 | 47 | So you would rather I say things I don't even\n |
| 0xb5445 | 46 | believe. I might add that you are a fiendish\n |
| 0xb5474 | 7 | person. |
| 0xb547c | 44 | Yikes. That frown... Like she's viscerally\n |
| 0xb54a9 | 39 | disgusted from the bottom of her heart. |
| 0xb54d1 | 7 | U-Um... |
| 0xb54d9 | 17 | Oh... This, ah... |
| 0xb54eb | 44 | He's Haku. You could call him... our leader. |
| 0xb5518 | 41 | He may not look it, but he really is an\n |
| 0xb5542 | 48 | interesting guy. I hope you can get along with\n |
| 0xb5573 | 9 | him, too. |
| 0xb557d | 45 | Rulutieh nods in fervent agreement with Kuon. |
| 0xb55ab | 22 | Your "leader," though? |
| 0xb55c2 | 47 | The boy looks between me, Kuon, Rulutieh, and\n |
| 0xb55f2 | 41 | Nekone, confusion writ plain on his face. |
| 0xb561c | 47 | Reluctant though I am to admit it, that would\n |
| 0xb564c | 47 | be the most accurate description of his duties. |
| 0xb567c | 18 | I'm Haku. Charmed. |
| 0xb568f | 45 | Oh, yes, it's a pleasure to meet you as well! |
| 0xb56bd | 46 | Kiwru hurriedly bows his head several times,\n |
| 0xb56ec | 17 | bobbing in place. |
| 0xb56fe | 47 | Did you come to study in the capital as well,\n |
| 0xb572e | 11 | Lord Kiwru? |
| 0xb573a | 48 | Oh, yes! I finally received permission from my\n |
| 0xb576b | 31 | grandfather to start this year. |
| 0xb578b | 45 | Yet another child from a high noble family,\n |
| 0xb57b9 | 4 | huh? |
| 0xb57be | 49 | But for someone from a powerful background like\n |
| 0xb57f0 | 7 | that... |
| 0xb57f8 | 47 | I hazard a look over at the cart he arrived in. |
| 0xb5828 | 45 | I'm a little embarrassed that we don't have\n |
| 0xb5856 | 49 | decorations. People see us as country bumpkins,\n |
| 0xb5888 | 11 | no doubt... |
| 0xb5894 | 45 | Kiwru seems to catch my glance, but despite\n |
| 0xb58c2 | 46 | his words, he doesn't look embarrassed at all. |
| 0xb58f1 | 43 | That would be because you are, in fact, a\n |
| 0xb591d | 16 | country bumpkin. |
| 0xb592e | 4 | Ack. |
| 0xb5933 | 39 | Kiwru deflates at Nekone's flat remark. |
| 0xb595b | 46 | That being said, I admit I prefer how you do\n |
| 0xb598a | 7 | things. |
| 0xb5992 | 45 | R-Really? Ah, hearing you say that makes me\n |
| 0xb59c0 | 27 | glad to be a bumpkin, then. |
| 0xb59dc | 46 | You used to say stuff like "too much panache\n |
| 0xb5a0b | 47 | makes things ugly," so I decided on a low-key\n |
| 0xb5a3b | 9 | approach. |
| 0xb5a45 | 44 | Ahaha... It was well worth it, if it meets\n |
| 0xb5a72 | 14 | your approval. |
| 0xb5a81 | 14 | Is that... so? |
| 0xb5a90 | 48 | Well, at least the kid's awfully easy to read.\n |
| 0xb5ac1 | 48 | Strange tastes, if he likes this little shrew,\n |
| 0xb5af2 | 6 | but... |
| 0xb5af9 | 32 | I guess everyone has their own\n |
| 0xb5b1a | 12 | preferences. |
| 0xb5b27 | 36 | That aside, you should get moving.\n |
| 0xb5b4c | 39 | You appear to be holding up the parade. |
| 0xb5b74 | 45 | Nekone points at the main procession, which\n |
| 0xb5ba2 | 41 | has ground to a halt behind Kiwru's cart. |
| 0xb5bcc | 33 | Ack! S-Sorry. I won't keep you.\n |
| 0xb5bee | 36 | I'll drop by and say hi later, then! |
| 0xb5c13 | 22 | I-If you'll excuse me! |
| 0xb5c2a | 48 | Kiwru hurriedly climbs back into his cart, and\n |
| 0xb5c5b | 39 | the parade trundles on before too long. |
| 0xb5c83 | 38 | ...Nice kid, him. Cheerful and polite. |
| 0xb5caa | 43 | I wouldn't go so far as to say you should\n |
| 0xb5cd6 | 43 | emulate him, but maybe you could stand to\n |
| 0xb5d02 | 18 | cheer up a little? |
| 0xb5d15 | 15 | Leave me alone. |
| 0xb5d25 | 14 | Still... hmhm. |
| 0xb5d34 | 36 | Kuon prods Nekone's cheek, giggling. |
| 0xb5d59 | 15 | ...Dear sister? |
| 0xb5d69 | 45 | You seemed to get along very well with that\n |
| 0xb5d97 | 4 | boy. |
| 0xb5d9c | 47 | Really? I hardly think our relationship to be\n |
| 0xb5dcc | 17 | anything special. |
| 0xb5dde | 49 | He brightened right up when you started talking\n |
| 0xb5e10 | 46 | to him. I think he probably... no, definitely. |
| 0xb5e3f | 26 | Don't you agree, Rulutieh? |
| 0xb5e5a | 43 | Yes, he... projects a very... warm feeling. |
| 0xb5e86 | 44 | I know women have a reputation for getting\n |
| 0xb5eb3 | 46 | excited over romance, but come on. This is a\n |
| 0xb5ee2 | 9 | bit much. |
| 0xb5eec | 49 | You are sorely mistaken. Kiwru only talks to me\n |
| 0xb5f1e | 43 | because I happen to be my brother's sister. |
| 0xb5f4a | 25 | What do you mean by that? |
| 0xb5f64 | 45 | Kiwru is my dear brother's sibling by oath.\n |
| 0xb5f92 | 47 | They share in a bond of sworn brotherhood and\n |
| 0xb5fc2 | 8 | kinship. |
| 0xb5fcb | 49 | Because of that, he often expresses concern for\n |
| 0xb5ffd | 49 | me--his sister-by-proxy--and how "alone" I look\n |
| 0xb602f | 12 | when I read. |
| 0xb603c | 40 | He says I needn't mind his attentions.\n |
| 0xb6065 | 35 | He talks to me because he wants to. |
| 0xb6089 | 39 | I... see. And what do you think of him? |
| 0xb60b1 | 3 | Me? |
| 0xb60b5 | 47 | I find him tiresome, clingy, and possessed of\n |
| 0xb60e5 | 46 | the mental fortitude of a gnat. He squanders\n |
| 0xb6114 | 11 | his talent. |
| 0xb6120 | 46 | He never knows when to give up, and has zero\n |
| 0xb614f | 48 | aesthetic taste. He often confuses the refined\n |
| 0xb6180 | 14 | and the crude. |
| 0xb618f | 30 | I could go on, but I will not. |
| 0xb61ae | 20 | That's... excessive. |
| 0xb61c3 | 12 | Dear sister? |
| 0xb61d0 | 14 | Lady Rulutieh? |
| 0xb61df | 14 | Huh? Oh, um... |
| 0xb61ee | 34 | Ah... Well, how should I put this. |
| 0xb6211 | 40 | By any chance, do you find him annoying? |
| 0xb623c | 23 | Nekone shakes her head. |
| 0xb6254 | 44 | I fail to understand. Why would I find him\n |
| 0xb6281 | 9 | annoying? |
| 0xb628b | 24 | Is something the matter? |
| 0xb62a4 | 18 | Um... No, nothing. |
| 0xb62b7 | 24 | Y-Yes, nothing at all... |
| 0xb62d0 | 47 | So she doesn't even acknowledge him enough to\n |
| 0xb6300 | 14 | hate him. Wow. |
| 0xb630f | 9 | Poor kid. |
| 0xb6319 | 44 | Looking on as the procession trails out of\n |
| 0xb6346 | 36 | sight, I quietly shed a single tear. |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_03.json` com a forma:
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
