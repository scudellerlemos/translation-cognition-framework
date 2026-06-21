# Cena ch_19_04 — pacote de traducao (166 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Nosuri Bandits | Organizacao | Bandidos Nosuri | traduzir | none |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |

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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
### Oshtor — criticality: high
- Oshtor — `voice_criticality: high`. = Ukon até 13_08 (ver spoiler_ledger). Registro formal, nobre, comedido; General da Direita. Antes do reveal, traduzir como o mercenário "Ukon" (espirituoso, informal) — NÃO antecipar a pompa de general
### Ougi — criticality: low
- Ougi — `voice_criticality: low`. Irmão da Nosuri; pragmático, parceria com a irmã.
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `*Snap*` -> `*Clique*` (SISTEMA, 18_01)
- `tears.` -> `lágrimas.` (Protagonista (narração), 18_01)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `here!` -> `fora!` (Ukon, 15_07)
- `Ah--` -> `Ah--` (Rulutieh, 13_02)
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
- Moznu: `Ha! Well done, Nosuri. A right impressive show,\n` -> `Ha! Bom trabalho, Nosuri. Foi uma boa encenação,\n`
- Moznu: `this.` -> `essa.`
- Moznu: `Heh heh. Now, ain't this one a beauty? Lookers\n` -> `Heh heh. Ora, essa aqui é uma beldade. Cara\n`
- Nosuri: `Moznu, enough. If you're going to be working with\n` -> `Moznu, chega. Se vai trabalhar com os Ladrões\n`
- Nosuri: `the Nosuri Thieves from now on, you abide by our\n` -> `de Nosuri de agora em diante, segue nossas\n`
- Nosuri: `rules, not yours.` -> `regras, não as suas.`
- Ougi: `Truly most impressive, dearest sister. Your\n` -> `Muito impressionante, querida irmã. Seu charme\n`
- Ougi: `feminine charms dazzle, as ever.` -> `feminino encanta, como sempre.`
- Ougi: `How positively boorish. A good MAN simply\n` -> `Que grosseria. Um bom HOMEM simplesmente\n`
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
| 0x179a45 | 38 | Your days of villainy are over, Moznu! |
| 0x179a6c | 38 | Grah, gah, *cough*... D-Damn it all... |
| 0x179a93 | 47 | Yes! Thanks to Kuon's smoke bombs, everything\n |
| 0x179ac3 | 25 | went off without a hitch. |
| 0x179add | 41 | We round up all the unconscious bandits\n |
| 0x179b07 | 16 | and tie them up. |
| 0x179b18 | 46 | There's barely any resistance, so we're done\n |
| 0x179b47 | 11 | in no time. |
| 0x179b53 | 45 | ...That smoke really was our ace in the hole. |
| 0x179b81 | 49 | ...Are these people really going to be all right? |
| 0x179bb3 | 40 | Eh, nothing life threatening... I think. |
| 0x179bdc | 13 | You think...? |
| 0x179bea | 50 | Kuon didn't know how it would turn out, and it's\n |
| 0x179c1d | 40 | not like we tested the thing beforehand. |
| 0x179c46 | 45 | Now all that remains is to serve them up to\n |
| 0x179c74 | 8 | justice. |
| 0x179c7d | 7 | Urgh... |
| 0x179c85 | 50 | I suggest you use your stay in prison to reflect\n |
| 0x179cb8 | 48 | on your crimes against the Nosuri Bandits' name. |
| 0x179ce9 | 14 | Hold on a sec. |
| 0x179cf8 | 6 | *Snap* |
| 0x179cff | 48 | As Nosuri begins striding toward Moznu, I stop\n |
| 0x179d30 | 24 | her and snap my fingers. |
| 0x179d49 | 31 | Wh-Wha... Who are all these--\n |
| 0x179d69 | 35 | Wait! What are you...!? S-Stop...\n |
| 0x179d8d | 22 | STOOOOOOOOOOOOOOOOP!!! |
| 0x179da4 | 51 | Suddenly, Ougi and the Nosuri Bandits emerge from\n |
| 0x179dd8 | 50 | the shadows... and begin stripping Moznu and his\n |
| 0x179e0b | 26 | gang of all their clothes. |
| 0x179e26 | 6 | Eeek!? |
| 0x179e2d | 19 | Wh-What are you...? |
| 0x179e45 | 28 | ...And what exactly is this? |
| 0x179e62 | 38 | Oogh... I believe I'm going to be ill. |
| 0x179e89 | 53 | Everybody looks appalled by the scene taking place.\n |
| 0x179ebf | 40 | All the girls hastily avert their gazes. |
| 0x179ee8 | 20 | Wh-What is all this? |
| 0x179efd | 46 | The finishing touch. We need to make this as\n |
| 0x179f2c | 23 | convincing as possible. |
| 0x179f44 | 49 | Convincing? What's going to be convincing about\n |
| 0x179f76 | 26 | a horde of naked thugs...? |
| 0x179f91 | 50 | If we bring them in now, it'll just look like we\n |
| 0x179fc4 | 41 | took down a regular old group of bandits. |
| 0x179fee | 50 | We want it absolutely clear that this guy's been\n |
| 0x17a021 | 45 | posing as the leader of the Nosuri Bandits... |
| 0x17a04f | 14 | Which is why-- |
| 0x17a05e | 15 | WHAT the FUCK!? |
| 0x17a06e | 46 | Before I can finish, I hear Moznu wailing in\n |
| 0x17a09d | 8 | anguish. |
| 0x17a0a6 | 47 | Nosuri glances over to see what's going on...\n |
| 0x17a0d6 | 12 | and freezes. |
| 0x17a0e3 | 45 | Wh-Wh-What the shit are you tryin' to pull,\n |
| 0x17a111 | 26 | dressin' me up like this!? |
| 0x17a12c | 35 | Before her is... a whole new Moznu. |
| 0x17a150 | 45 | He's dressed in the same clothes as Nosuri,\n |
| 0x17a17e | 31 | his face slathered in makeup.\n |
| 0x17a19e | 26 | The sight is... arresting. |
| 0x17a1b9 | 49 | I've fought in a number of wars now... but I've\n |
| 0x17a1eb | 39 | still never seen anything this awful... |
| 0x17a213 | 46 | Atuy hastily dashes to the far corner of the\n |
| 0x17a242 | 29 | area the moment she sees him. |
| 0x17a260 | 13 | Bleaagghhh... |
| 0x17a26e | 21 | Wh-What exactly is... |
| 0x17a284 | 29 | ...This is cruel and unusual. |
| 0x17a2a2 | 44 | The disgust is clear in everyone's voices.\n |
| 0x17a2cf | 49 | Nekone and Rulutieh... seem to be at a complete\n |
| 0x17a301 | 5 | loss. |
| 0x17a307 | 31 | ...OK, I think we're all ready. |
| 0x17a327 | 49 | Ready for WHAT!? What the fuck are you plannin'\n |
| 0x17a359 | 47 | on doin' to me after dressin' me in THIS shit!? |
| 0x17a389 | 48 | With all of them disguised like this, it'll be\n |
| 0x17a3ba | 39 | clear they've been masquerading as...\n |
| 0x17a3e2 | 11 | uh, Nosuri? |
| 0x17a3ee | 46 | Ignoring Moznu's yells, I glance to my side.\n |
| 0x17a41d | 46 | Nosuri's shaking, like she's on the verge of\n |
| 0x17a44c | 6 | tears. |
| 0x17a453 | 49 | M-My bandit finery...! I-I was saving those for\n |
| 0x17a485 | 19 | a special occasion! |
| 0x17a499 | 42 | G-Gaaah!? Wh-What're yeh doin' to me NOW!? |
| 0x17a4c4 | 46 | Hey, come on! We just finished squeezing him\n |
| 0x17a4f3 | 10 | into that! |
| 0x17a4fe | 49 | Are you insane!? Th-That came out of MY wardrobe! |
| 0x17a530 | 50 | It's a necessary evil. Sorry, but you'll have to\n |
| 0x17a563 | 16 | just give it up. |
| 0x17a574 | 50 | I manage to hold Nosuri back from reclaiming her\n |
| 0x17a5a7 | 19 | clothes from Moznu. |
| 0x17a5bb | 46 | She stares at Moznu with soulless eyes for a\n |
| 0x17a5ea | 40 | while, then weakly slumps to the ground. |
| 0x17a613 | 46 | M-My favorite ensemble... It took almost all\n |
| 0x17a642 | 38 | my savings to satisfy that merchant... |
| 0x17a669 | 48 | A-And now... it's ruined... I'll never be able\n |
| 0x17a69a | 19 | to wear it again... |
| 0x17a6ae | 46 | Ougi, who appears to have finished his work,\n |
| 0x17a6dd | 49 | places a reassuring hand on her shaking shoulder. |
| 0x17a70f | 49 | I know how difficult this must be, but you must\n |
| 0x17a741 | 44 | understand that it was for the greater good. |
| 0x17a76e | 13 | But... But... |
| 0x17a77c | 47 | Huh. I get the feeling she didn't hear a word\n |
| 0x17a7ac | 30 | of my explanation... Ah, well. |
| 0x17a7cb | 33 | All right, time to wrap this up-- |
| 0x17a7ed | 28 | W-Wait just a damn second!\n |
| 0x17a80a | 50 | Y-You're not gonna turn me in like this, are yeh!? |
| 0x17a83d | 13 | 'Course I am. |
| 0x17a84b | 24 | Not like this... N-No!\n |
| 0x17a864 | 27 | Anythin' but THIS! PLEASE!! |
| 0x17a880 | 49 | Take 'em away. And make it flashy when you haul\n |
| 0x17a8b2 | 45 | them in. Make sure everyone gets a good look. |
| 0x17a8e0 | 17 | NOOOOOOOOOOOOOO!! |
| 0x17a8f2 | 44 | Heh heh heh... And now, time to get a look\n |
| 0x17a91f | 19 | at this treasure... |
| 0x17a933 | 46 | All their stolen goodies belong to me now...\n |
| 0x17a962 | 47 | and I can finally start living the easy life... |
| 0x17a992 | 44 | You're still scheming something, aren't you? |
| 0x17a9bf | 51 | Well, how about we take a quick look in the... Huh? |
| 0x17a9f3 | 51 | Just as I drift back to reality, I suddenly smell\n |
| 0x17aa27 | 18 | something burning. |
| 0x17aa3a | 8 | ...What? |
| 0x17aa43 | 48 | My stomach sinks, and I turn around to find...\n |
| 0x17aa74 | 40 | the bandits' hideout engulfed in flames. |
| 0x17aa9d | 4 | Huh? |
| 0x17aaa2 | 49 | The fire dances and rises, casting a warm light\n |
| 0x17aad4 | 48 | over the caves, like a massive, guttering torch. |
| 0x17ab05 | 21 | Wh--!? Fire!? H-How!? |
| 0x17ab1b | 31 | My, what a magnificent blaze.\n |
| 0x17ab3b | 42 | I daresay the spectacle is a fitting end\n |
| 0x17ab66 | 22 | to a victorious night. |
| 0x17ab7d | 44 | Wh-What are you... How did it catch fire!?\n |
| 0x17abaa | 38 | What could possibly have caused this!? |
| 0x17abd1 | 34 | Well, about those smoke bombs...\n |
| 0x17abf4 | 47 | I think I did mention they were a bit unstable. |
| 0x17ac24 | 49 | Why didn't you SAY--W-We need to put it out, NOW! |
| 0x17ac56 | 43 | W-We can't. Now that the fire's that big,\n |
| 0x17ac82 | 25 | there's no stopping it... |
| 0x17ac9c | 27 | It's not too late! Water!\n |
| 0x17acb8 | 19 | Where's the water!? |
| 0x17accc | 45 | U-Um... I think I see a bucket over there...? |
| 0x17acfa | 5 | Here! |
| 0x17ad00 | 4 | Ah-- |
| 0x17ad05 | 8 | That's-- |
| 0x17ad0e | 10 | Take this! |
| 0x17ad19 | 11 | WHAAAARGH!? |
| 0x17ad25 | 45 | The moment I douse the fire, it immediately\n |
| 0x17ad53 | 29 | begins burning even stronger. |
| 0x17ad71 | 27 | Hot, HOT! What's going on!? |
| 0x17ad8d | 51 | I believe that is oil you just threw on the fire.\n |
| 0x17adc1 | 37 | Of course it will burn more fiercely. |
| 0x17ade7 | 43 | OIL!? Who the hell leaves a bucket of oil\n |
| 0x17ae13 | 14 | lying around!? |
| 0x17ae22 | 49 | The wooden platforms burn even brighter, before\n |
| 0x17ae54 | 45 | beginning to crumble with a crunch of timber. |
| 0x17ae82 | 32 | I-It's burning... all burning... |
| 0x17aea3 | 28 | What are you doing, Haku!?\n |
| 0x17aec0 | 24 | It's dangerous to go in! |
| 0x17aed9 | 34 | Let go of me! My life of luxury!\n |
| 0x17aefc | 27 | I could almost taste it...! |
| 0x17af18 | 30 | What are you talking about!?\n |
| 0x17af37 | 39 | You're going to kill yourself in there! |
| 0x17af5f | 48 | Kiwru hurriedly rushes to me, holding me back.\n |
| 0x17af90 | 50 | The fire burns merrily, spreading across the camp. |
| 0x17afc3 | 45 | Why...? It wasn't supposed to be like this... |
| 0x17aff1 | 52 | It'll be nothing but ash soon. I fall to my knees,\n |
| 0x17b026 | 46 | slamming my fist against the ground miserably. |
| 0x17b055 | 39 | Easy come, easy go, I suppose they say. |
| 0x17b07d | 36 | And this is a prime example of it.\n |
| 0x17b0a2 | 21 | How very educational. |
| 0x17b0b8 | 48 | It just goes to show that the best way to make\n |
| 0x17b0e9 | 35 | money is through hard, honest work. |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_04.json` com a forma:
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
