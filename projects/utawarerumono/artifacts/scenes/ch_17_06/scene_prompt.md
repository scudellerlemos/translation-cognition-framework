# Cena ch_17_06 — pacote de traducao (92 linhas)

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
| Girl | UI | Garota | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
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
- **Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)**: **Decisão tomada:** Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`, 75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa). **Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `trouble...` -> `incomodar...` (Rulutieh, 13_01)
- `again.` -> `vez.` (Ougi, 13_05)
- `Man` -> `Hom` (Sistema, 12_04)
- `the job.` -> `o trabalho.` (Ukon, 17_04)
- `surface.` -> `superfície.` (Haku, 14_03)
- `to you.` -> `com você.` (Ukon, 13_02)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `Woman` -> `Mulher` (sistema, 14_07)
- `Girl` -> `Garota` (sistema, 13_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
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
| 0x11badf | 44 | Figured as much. This network has a pretty\n |
| 0x11bb0c | 24 | beefy firewall in place. |
| 0x11bb25 | 46 | Nothing an elite hacker can't slice through,\n |
| 0x11bb54 | 45 | of course. Just one crack to widen is all I\n |
| 0x11bb82 | 5 | need. |
| 0x11bb88 | 37 | Wh--? Shit! Did I get traced already? |
| 0x11bbae | 26 | Retreat! Tactical retreat! |
| 0x11bbc9 | 21 | Gotta dump out, fast! |
| 0x11bbdf | 46 | ...Urgh. I think I got away before the trace\n |
| 0x11bc0e | 40 | could get all the way back to me, but... |
| 0x11bc37 | 43 | Man. Their security protocols are getting\n |
| 0x11bc63 | 20 | tighter and tighter. |
| 0x11bc78 | 41 | Gotta wonder what they're scrambling so\n |
| 0x11bca2 | 42 | desperately to hide at the first sign of\n |
| 0x11bccd | 10 | trouble... |
| 0x11bcd8 | 45 | Must be something shady, for sure. It'll be\n |
| 0x11bd06 | 49 | worth it, but I should wait awhile before I try\n |
| 0x11bd38 | 6 | again. |
| 0x11bd3f | 47 | Ah, well. I'll just kill time 'til that whole\n |
| 0x11bd6f | 17 | storm blows over. |
| 0x11bd81 | 44 | Hello? Yes, who's calli--Oh, hey, what's up? |
| 0x11bdae | 3 | Man |
| 0x11bdb2 | 49 | Don't you "what's up" me. You haven't contacted\n |
| 0x11bde4 | 11 | us in days. |
| 0x11bdf0 | 47 | Huh...? Oh. Oh, right. Yeah, I totally forgot\n |
| 0x11be20 | 15 | to call, sorry. |
| 0x11be30 | 48 | You never change, do you? Why don't you go out\n |
| 0x11be61 | 44 | for a bit--get some fresh air, enjoy nature? |
| 0x11be8e | 48 | I had enough "nature" to last me when you made\n |
| 0x11bebf | 45 | me visit that growth experiment farm, thanks. |
| 0x11beed | 40 | How did that end up shaking out, anyway? |
| 0x11bf16 | 49 | The project lead had nothing but good things to\n |
| 0x11bf48 | 47 | say about you. They seem to want to offer you\n |
| 0x11bf78 | 8 | the job. |
| 0x11bf81 | 44 | No thanks. Roots that scream when you pull\n |
| 0x11bfae | 44 | them out, daikon with LEGS? And that giant\n |
| 0x11bfdb | 10 | nepenthes? |
| 0x11bfe6 | 45 | I don't want any part of that monster movie\n |
| 0x11c014 | 45 | world they're trying to cultivate up on the\n |
| 0x11c042 | 8 | surface. |
| 0x11c04b | 44 | ...I see. Have you given any thought to my\n |
| 0x11c078 | 25 | other proposal, at least? |
| 0x11c092 | 48 | Helping you out with your research? Gonna have\n |
| 0x11c0c3 | 31 | to pass on that one too, sorry. |
| 0x11c0e3 | 48 | I'm pretty confident in my skills, but I don't\n |
| 0x11c114 | 48 | think I'm on a level where I can be of any use\n |
| 0x11c145 | 7 | to you. |
| 0x11c14d | 46 | You have a habit of severely underestimating\n |
| 0x11c17c | 31 | yourself. You know that, right? |
| 0x11c19c | 48 | Having witnessed your abilities firsthand, I'm\n |
| 0x11c1cd | 47 | fully confident you can help with this project. |
| 0x11c1fd | 48 | And I'M fully confident you're just playing at\n |
| 0x11c22e | 25 | nepotism to get me a job. |
| 0x11c248 | 49 | I'm hardly so sentimental as to let my feelings\n |
| 0x11c27a | 27 | cloud my judgement on this. |
| 0x11c296 | 37 | We'll talk about this another time.\n |
| 0x11c2bc | 14 | But for now... |
| 0x11c2cb | 48 | Have you been eating well? Don't think I don't\n |
| 0x11c2fc | 44 | know you've been shutting yourself away in\n |
| 0x11c329 | 6 | there. |
| 0x11c330 | 28 | Huh? Yeah, I've been eating. |
| 0x11c34d | 35 | You're getting enough sleep, too?\n |
| 0x11c371 | 45 | And I hope you're cleaning up after yourself. |
| 0x11c39f | 43 | I'm not a child! I'm perfectly capable of\n |
| 0x11c3cb | 22 | taking care of myself. |
| 0x11c3e2 | 46 | I see. So if someone came around for a visit\n |
| 0x11c411 | 46 | right now, your room would be in presentable\n |
| 0x11c440 | 6 | order? |
| 0x11c447 | 8 | Wh-What? |
| 0x11c450 | 47 | Excellent. It relieves me to hear there'll be\n |
| 0x11c480 | 12 | no problems. |
| 0x11c48d | 22 | What are you on about? |
| 0x11c4a4 | 42 | They should be arriving any minute, now... |
| 0x11c4cf | 30 | Arriving? Wait, hold on, who-- |
| 0x11c4ee | 5 | Woman |
| 0x11c4f4 | 31 | Hello there! How have you been? |
| 0x11c514 | 23 | Wh-Whoa, what are you-- |
| 0x11c52c | 47 | Ah, you've gone and made a mess of the place.\n |
| 0x11c55c | 42 | Are these MREs...? Do you have ANY clean\n |
| 0x11c587 | 7 | dishes? |
| 0x11c58f | 48 | Just hold on and I'll pull a meal together out\n |
| 0x11c5c0 | 23 | of all this... Somehow. |
| 0x11c5d8 | 50 | A meal...? L-Look, uh--I appreciate the thought,\n |
| 0x11c60b | 36 | really, but... your cooking's, uh... |
| 0x11c630 | 39 | So rude. But worry not, brother dear!\n |
| 0x11c658 | 41 | I have the esteemed master with me today. |
| 0x11c682 | 7 | Master? |
| 0x11c68a | 4 | Girl |
| 0x11c68f | 28 | Hey, uncle! I came to visit! |
| 0x11c6ac | 7 | Urgh... |
| 0x11c6b4 | 48 | Aw, come on, don't be like that! I'm gonna fix\n |
| 0x11c6e5 | 46 | up some curry just for you. Cheer up a little! |

## 8. Formato de saida EXIGIDO
Escreva `translations_17_06.json` com a forma:
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
