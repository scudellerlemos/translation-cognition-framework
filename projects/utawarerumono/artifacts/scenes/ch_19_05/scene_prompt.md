# Cena ch_19_05 — pacote de traducao (435 linhas)

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
| aperyu | Item | aperyu | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Woman | UI | Mulher | traduzir | none |
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
- **Processo de Despertar** (moderate): Mantenha o enquadramento ambiguo e tecnico (CAPS p/ Sistema). NAO explique a natureza sci-fi nem conecte ao enredo maior. (Obs.: 'system of gears'/engrenagens do moinho NAO e isto.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `right?` -> `né?` (Haku, 12_03)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Well...` -> `Bom...` (Haku, 12_03)
- `Yamato...` -> `Yamato...` (Kuon, 17_01)
- `to the palace.` -> `para o palácio.` (Narrador/Haku, 18_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `case.` -> `caso.` (Haku, 16_02)
- `throne.` -> `Mikado.` (Nekone, 15_03)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `Uh...` -> `Ahn...` (Haku, 14_03)
- `N-No, not at all.` -> `N-Não, de jeito nenhum.` (Kuon, 14_04)
- `As you wish.` -> `Como desejar.` (Nekone, 14_04)
- `somewhere.` -> `de algum lugar.` (Haku, 15_01)
- `Mysterious duo` -> `Dupla misteriosa` (sistema, 13_02)
- `me.` -> `mim.` (Garota, 17_01)
- `work.` -> `trabalho.` (Protagonista, 16_01)
- `sight.` -> `cena estranha.` (Haku, 13_04)
- `skin.` -> `pele.` (Haku, 18_01)
- `of me.` -> `de mim.` (Nosuri, 18_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `Gah!?` -> `Gah!?` (Haku, 13_01)
- `You mean...` -> `Você quer dizer...` (Garota, 18_01)
- `...Huh!?` -> `...Hein!?` (Haku, 13_06)
- `Hey, wait--` -> `Ei, espera--` (Haku, 11_08)
- `Generals.` -> `Generais.` (Haku, 18_01)
- `This?` -> `Esta?` (Haku, 11_09)
- `I'd think.` -> `eu pensaria.` (Haku, 19_01)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `it.` -> `aí.` (Haku, 15_03)
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
| 0x17de7e | 49 | Well, not everything went the way I planned it,\n |
| 0x17deb0 | 40 | but... we did all right in the end...!\n |
| 0x17ded9 | 6 | Right? |
| 0x17dee0 | 46 | I suppose in this case, we may have done too\n |
| 0x17df0f | 29 | good of a job... so to speak. |
| 0x17df2d | 48 | They could be suspicious of us now, as a result. |
| 0x17df5e | 49 | Crap. If that's true, this could be pretty bad... |
| 0x17df90 | 50 | A while after fram--uh, taking down the bandits,\n |
| 0x17dfc3 | 46 | Oshtor called us to his manor for "something\n |
| 0x17dff2 | 11 | important." |
| 0x17dffe | 41 | Something about the way he worded it...\n |
| 0x17e028 | 43 | This definitely doesn't feel like another\n |
| 0x17e054 | 19 | undercover mission. |
| 0x17e068 | 24 | Then, does that mean...? |
| 0x17e081 | 32 | I apologize for making you wait. |
| 0x17e0a2 | 48 | After a little while, Oshtor arrives and takes\n |
| 0x17e0d3 | 7 | a seat. |
| 0x17e0db | 44 | So, what's up? Did they find out about the\n |
| 0x17e108 | 23 | operation or something? |
| 0x17e120 | 43 | Operation...? Oh, no. That is not the case. |
| 0x17e14c | 45 | Although I daresay it may be better for you\n |
| 0x17e17a | 12 | if they had. |
| 0x17e187 | 3 | Hm? |
| 0x17e18b | 45 | Well, being that you all saved the imperial\n |
| 0x17e1b9 | 47 | princess, you pleased a certain individual of\n |
| 0x17e1e9 | 12 | distinction. |
| 0x17e1f6 | 44 | They would extend their thanks personally.\n |
| 0x17e223 | 43 | I am to escort you to them as the group's\n |
| 0x17e24f | 15 | representative. |
| 0x17e25f | 34 | An individual of distinction...?\n |
| 0x17e282 | 11 | Who's this? |
| 0x17e28e | 7 | Well... |
| 0x17e296 | 18 | You don't mean...? |
| 0x17e2a9 | 30 | Correct... The Mikado himself. |
| 0x17e2c8 | 44 | The Mikado... The god incarnate that rules\n |
| 0x17e2f5 | 9 | Yamato... |
| 0x17e2ff | 46 | You're... joking, right? He wants to see me?\n |
| 0x17e32e | 31 | Just a regular old commoner...? |
| 0x17e34e | 44 | Whether you're a "regular old commoner"...\n |
| 0x17e37b | 33 | is a discussion for another time. |
| 0x17e39d | 48 | You saved the imperial princess and caught her\n |
| 0x17e3ce | 45 | kidnappers. It is little wonder my liege is\n |
| 0x17e3fc | 8 | pleased. |
| 0x17e405 | 48 | In other words, you may have accomplished your\n |
| 0x17e436 | 36 | task perhaps a little too perfectly. |
| 0x17e45f | 46 | So. That is how the matter currently stands.\n |
| 0x17e48e | 44 | I am afraid I must ask you to accompany me\n |
| 0x17e4bb | 14 | to the palace. |
| 0x17e4ca | 48 | H-Hold on a sec. You can't be serious! I can't\n |
| 0x17e4fb | 40 | go somewhere like that! That's way too\n |
| 0x17e524 | 10 | stressful! |
| 0x17e52f | 50 | My liege wishes to present your reward directly.\n |
| 0x17e562 | 48 | It is the highest honor for a citizen of Yamato. |
| 0x17e593 | 47 | A reward from the most powerful person in the\n |
| 0x17e5c3 | 46 | country!? That's gonna be nothing but trouble! |
| 0x17e5f2 | 45 | I was expecting a reaction like this... but\n |
| 0x17e620 | 47 | I'm afraid refusing this invitation is not an\n |
| 0x17e650 | 7 | option. |
| 0x17e658 | 36 | My liege issued an imperial order.\n |
| 0x17e67d | 44 | Should you reject it, I am afraid I cannot\n |
| 0x17e6aa | 22 | guarantee your safety. |
| 0x17e6c1 | 46 | What, I'd be executed for insubordination to\n |
| 0x17e6f0 | 25 | the emperor or something? |
| 0x17e70a | 49 | No. In fact, it would likely not anger my liege\n |
| 0x17e73c | 17 | in the slightest. |
| 0x17e74e | 37 | The citizenry of Yamato, however...\n |
| 0x17e774 | 41 | To them, the Mikado is akin to the sun.\n |
| 0x17e79e | 23 | Absolute and immutable. |
| 0x17e7b6 | 44 | To refuse the gratitude of such a ruler...\n |
| 0x17e7e3 | 45 | I am sure many would see it as grave insult\n |
| 0x17e811 | 14 | to the throne. |
| 0x17e820 | 51 | And I am sure you can imagine what the inevitable\n |
| 0x17e854 | 22 | consequences would be. |
| 0x17e86b | 7 | Urgh... |
| 0x17e873 | 44 | Should someone try to assassinate you, the\n |
| 0x17e8a0 | 42 | people--perhaps even the guards may turn\n |
| 0x17e8cb | 12 | a blind eye. |
| 0x17e8d8 | 47 | In all honesty, even I would have a difficult\n |
| 0x17e908 | 26 | time ensuring your safety. |
| 0x17e923 | 20 | This is so unfair... |
| 0x17e938 | 46 | That is what it means to disobey the Mikado.\n |
| 0x17e967 | 46 | And... I suggest you do not feign illness to\n |
| 0x17e996 | 24 | escape your obligations. |
| 0x17e9af | 47 | I would be forced to cut you down on the spot\n |
| 0x17e9df | 45 | for attempting to deceive my liege, in that\n |
| 0x17ea0d | 5 | case. |
| 0x17ea13 | 49 | H-Hey! Y-You can't just say that so nonchalantly! |
| 0x17ea45 | 52 | I am sorry. But as your friend and ally, I believe\n |
| 0x17ea7a | 42 | I must give you the truth in its entirety. |
| 0x17eaa5 | 41 | Then would you at least act like you're\n |
| 0x17eacf | 15 | ACTUALLY sorry? |
| 0x17eadf | 48 | Now then. I hope you understand your situation\n |
| 0x17eb10 | 47 | and standing. The carriage awaits us out front. |
| 0x17eb40 | 50 | Ah... Before your audience, you will change into\n |
| 0x17eb73 | 46 | clothes I have prepared. Consider them a gift. |
| 0x17eba2 | 50 | As Oshtor rises, multiple soldiers rush into the\n |
| 0x17ebd5 | 45 | room from both sides and grab me by the arms. |
| 0x17ec03 | 45 | Wait--!? H-Hey, Kuon! Don't just sit there,\n |
| 0x17ec31 | 11 | do someth-- |
| 0x17ec3d | 49 | I look desperately over to Kuon, to try and get\n |
| 0x17ec6f | 10 | some help. |
| 0x17ec7a | 30 | ...Where the hell did she go!? |
| 0x17ec99 | 34 | Lady Kuon left a little while ago. |
| 0x17ecbc | 32 | Sh-She just made a run for it... |
| 0x17ecdd | 45 | All my struggling amounts to nothing as the\n |
| 0x17ed0b | 34 | soldiers haul me outside the room. |
| 0x17ed2e | 43 | Our guest from afar, Sir Haku, has arrived! |
| 0x17ed5a | 49 | I didn't have enough time to straighten out the\n |
| 0x17ed8c | 42 | clothes. I'm all puffed up as I exit the\n |
| 0x17edb7 | 9 | carriage. |
| 0x17edc1 | 22 | I feel like a clown... |
| 0x17edd8 | 46 | I look towards the throne. Both sides of the\n |
| 0x17ee07 | 39 | path are lined by pompous-looking guys. |
| 0x17ee2f | 48 | I just stand there, clueless. Oshtor, standing\n |
| 0x17ee60 | 44 | at my side, murmurs under his breath for me. |
| 0x17ee8d | 48 | Just do as I do. Walk forward, head down, then\n |
| 0x17eebe | 43 | kneel when I do when we arrive before the\n |
| 0x17eeea | 7 | throne. |
| 0x17eef2 | 48 | When my liege bids you raise your head, do so.\n |
| 0x17ef23 | 45 | Answer honestly, and graciously accept your\n |
| 0x17ef51 | 15 | reward. Simple. |
| 0x17ef61 | 45 | So do I ask for a brain, a heart, or courage? |
| 0x17ef8f | 27 | What are you talking about? |
| 0x17efab | 29 | Eh, nothing. Obligatory joke. |
| 0x17efc9 | 34 | Well, you needn't be so nervous.\n |
| 0x17efec | 35 | Just act as your usual brazen self. |
| 0x17f010 | 50 | My liege is well aware that you are but a common\n |
| 0x17f043 | 48 | citizen. Minor breaches of etiquette are fine,\n |
| 0x17f074 | 18 | and even expected. |
| 0x17f087 | 48 | In truth, attempting to keep up some facade or\n |
| 0x17f0b8 | 46 | groveling may only sour his impression of you. |
| 0x17f0e7 | 48 | His comments hanging in the air, Oshtor begins\n |
| 0x17f118 | 34 | moving forward, and I follow suit. |
| 0x17f13b | 44 | We both arrive before the throne, and kneel. |
| 0x17f168 | 50 | It is an honor to be in your presence, my liege.\n |
| 0x17f19b | 20 | I trust all is well. |
| 0x17f1b0 | 49 | By your command, I, Oshtor, have brought before\n |
| 0x17f1e2 | 41 | you the man you desired an audience with. |
| 0x17f20c | 41 | ...So the man at your side would be Haku? |
| 0x17f236 | 48 | After a short silence, his voice echoes across\n |
| 0x17f267 | 28 | the audience hall once more. |
| 0x17f284 | 30 | I would look upon your face.\n |
| 0x17f2a3 | 24 | You may raise your head. |
| 0x17f2bc | 11 | Yes, sir... |
| 0x17f2c8 | 38 | At those words, I slowly lift my head. |
| 0x17f2ef | 50 | I look up to the throne to see an old man seated\n |
| 0x17f322 | 46 | there, his face hidden. The Mikado, I presume. |
| 0x17f351 | 46 | ...More normal than I expected. With all the\n |
| 0x17f380 | 43 | "akin to a god" stuff, I expected someone\n |
| 0x17f3ac | 14 | more... godly. |
| 0x17f3bb | 49 | But my train of thought comes to an abrupt halt\n |
| 0x17f3ed | 49 | when I see the face of the young woman standing\n |
| 0x17f41f | 12 | next to him. |
| 0x17f42c | 10 | ...Wha--!? |
| 0x17f437 | 12 | H-Honoka...? |
| 0x17f444 | 47 | The woman standing there is, without a doubt,\n |
| 0x17f474 | 7 | Honoka. |
| 0x17f47c | 35 | What... What's she doing here...?\n |
| 0x17f4a0 | 42 | Why is she standing next to the Mikado...? |
| 0x17f4cb | 5 | Haku? |
| 0x17f4d1 | 5 | Uh... |
| 0x17f4d7 | 46 | I snap back to reality, realizing the Mikado\n |
| 0x17f506 | 19 | is calling my name. |
| 0x17f51a | 34 | Haku... is something the matter?\n |
| 0x17f53d | 38 | Perhaps there is something on my face? |
| 0x17f564 | 17 | N-No, not at all. |
| 0x17f576 | 34 | Is he going senile or something?\n |
| 0x17f599 | 42 | I can't see his face in the first place... |
| 0x17f5c4 | 47 | This is hardly the time to say I think I know\n |
| 0x17f5f4 | 42 | the woman beside him. I'd sound like I'm\n |
| 0x17f61f | 15 | hitting on her. |
| 0x17f62f | 50 | I-I just... I've got a strange feeling we've met\n |
| 0x17f662 | 17 | somewhere before. |
| 0x17f674 | 13 | All officials |
| 0x17f685 | 47 | I try and improvise, but it sounds like I hit\n |
| 0x17f6b5 | 48 | a landmine. I feel the air in the hall freeze,\n |
| 0x17f6e6 | 5 | but-- |
| 0x17f6ec | 46 | Hohoho... It has been some time since I have\n |
| 0x17f71b | 47 | appeared in public, but paintings and such do\n |
| 0x17f74b | 6 | exist. |
| 0x17f752 | 49 | I am certain you must have encountered one such\n |
| 0x17f784 | 10 | depiction. |
| 0x17f78f | 16 | Y-Yes, probably. |
| 0x17f7a0 | 49 | The tension in the hall fades a little with the\n |
| 0x17f7d2 | 42 | Mikado's words, but my questions remain... |
| 0x17f7fd | 46 | What does this mean? Is she the same person?\n |
| 0x17f82c | 45 | Maybe they just look alike? Are they sisters? |
| 0x17f85a | 47 | Still, I can't say anything careless in front\n |
| 0x17f88a | 47 | of the Mikado. Just have to keep my mouth shut. |
| 0x17f8ba | 15 | Now then, Haku. |
| 0x17f8ca | 48 | I have heard that it was by your brave actions\n |
| 0x17f8fb | 46 | that my daughter is safe. My gratitude knows\n |
| 0x17f92a | 10 | no bounds. |
| 0x17f935 | 36 | I do not deserve such praise, sir... |
| 0x17f95a | 40 | You have performed admirably. For your\n |
| 0x17f983 | 45 | accomplishments, I bestow upon you a worthy\n |
| 0x17f9b1 | 7 | reward. |
| 0x17f9b9 | 46 | Mikado gives a small nod to Honoka, as if to\n |
| 0x17f9e8 | 11 | signal her. |
| 0x17f9f4 | 16 | Grant it to him. |
| 0x17fa05 | 12 | As you wish. |
| 0x17fa12 | 38 | Honoka gives a deep bow to the Mikado. |
| 0x17fa39 | 43 | Suddenly, I hear music begin to play from\n |
| 0x17fa65 | 10 | somewhere. |
| 0x17fa70 | 33 | An elegant and entrancing tune... |
| 0x17fa92 | 45 | Then two figures gracefully land before me,\n |
| 0x17fac0 | 31 | like they just flew in somehow. |
| 0x17fae0 | 12 | These two... |
| 0x17faed | 43 | It's that mysterious duo... the ones from\n |
| 0x17fb19 | 24 | before, with the aperyu. |
| 0x17fb32 | 29 | What are these two doing he-- |
| 0x17fb50 | 14 | Mysterious duo |
| 0x17fb5f | 47 | They stand utterly still, back to back... and\n |
| 0x17fb8f | 45 | suddenly, like breaking a spell, they raise\n |
| 0x17fbbd | 11 | their arms. |
| 0x17fbc9 | 48 | They fluidly shift in opposite directions, and\n |
| 0x17fbfa | 47 | sway their arms and hips to the music's rhythm. |
| 0x17fc2a | 50 | They gradually lower their arms in time with the\n |
| 0x17fc5d | 47 | music, and they begin to take steps away from\n |
| 0x17fc8d | 3 | me. |
| 0x17fc91 | 44 | Facing each other, they leap into the air.\n |
| 0x17fcbe | 48 | The aperyu are cast off, fluttering in the air\n |
| 0x17fcef | 12 | behind them. |
| 0x17fcfc | 7 | Huh--!? |
| 0x17fd04 | 17 | They're... girls? |
| 0x17fd16 | 48 | They're both stunning. Their faces look almost\n |
| 0x17fd47 | 44 | sculpted... like a master artisan's finest\n |
| 0x17fd74 | 5 | work. |
| 0x17fd7a | 44 | Their hair glimmers like silk under light,\n |
| 0x17fda7 | 44 | and their smooth skin looks as delicate as\n |
| 0x17fdd4 | 10 | porcelain. |
| 0x17fddf | 51 | They might be twins... They have identical faces.\n |
| 0x17fe13 | 48 | But their skin tone differs--one fair, one dark. |
| 0x17fe44 | 45 | They seem to be making some sign with their\n |
| 0x17fe72 | 49 | fingers as they spin around me in their flowing\n |
| 0x17fea4 | 6 | dance. |
| 0x17feab | 49 | I can only stand there mutely, entranced by the\n |
| 0x17fedd | 6 | sight. |
| 0x17fee4 | 44 | Their movements quicken as the tempo does.\n |
| 0x17ff11 | 48 | Sweat glistens and sparkles in jewels on their\n |
| 0x17ff42 | 5 | skin. |
| 0x17ff48 | 46 | They revolve and sway, switching sides again\n |
| 0x17ff77 | 50 | and again until they finally stop right in front\n |
| 0x17ffaa | 6 | of me. |
| 0x17ffb1 | 45 | And as they both kneel before me, the music\n |
| 0x17ffdf | 6 | stops. |
| 0x17ffe6 | 15 | Wh-What is...\n |
| 0x17fff6 | 25 | What is going on here...? |
| 0x180010 | 35 | What are these two doing here...?\n |
| 0x180034 | 44 | I thought he was going to give me a reward\n |
| 0x180061 | 13 | or something. |
| 0x18006f | 28 | This shall be your reward.\n |
| 0x18008c | 35 | You may do as you please with them. |
| 0x1800b0 | 7 | ...Huh? |
| 0x1800b8 | 18 | Do as I please...? |
| 0x1800cb | 47 | The two of them look up, meeting my eyes with\n |
| 0x1800fb | 12 | keen stares. |
| 0x180108 | 7 | Uruuru. |
| 0x180110 | 32 | Beside me is my sister Uruuru.\n |
| 0x180131 | 19 | My name is Saraana. |
| 0x180145 | 42 | I feel something oddly... moist and soft\n |
| 0x180170 | 11 | on my feet. |
| 0x18017c | 42 | I look down to find the two of them have\n |
| 0x1801a7 | 38 | prostrated themselves to kiss my feet. |
| 0x1801ce | 5 | Gah!? |
| 0x1801d4 | 17 | To mark our oath. |
| 0x1801e6 | 33 | We hereby swear upon this oath,\n |
| 0x180208 | 40 | and offer to you everything that we are. |
| 0x180231 | 30 | Eternal loyalty to our Master. |
| 0x180250 | 11 | You mean... |
| 0x18025c | 48 | From this moment on, those two belong to you--\n |
| 0x18028d | 21 | body, mind, and soul. |
| 0x1802a3 | 49 | Command them as you see fit. You may treat them\n |
| 0x1802d5 | 45 | with care, or toy with them to satisfy your\n |
| 0x180303 | 40 | own desires. You will be denied nothing. |
| 0x18032c | 29 | H-Hold on. This is a little-- |
| 0x18034a | 41 | I thank you, Haku, for time well spent.\n |
| 0x180374 | 35 | I look forward to our next meeting. |
| 0x180398 | 44 | Honoka bows quietly at the Mikado's words,\n |
| 0x1803c5 | 34 | and slowly pushes the throne away. |
| 0x1803e8 | 47 | Looks like that throne is really an elaborate\n |
| 0x180418 | 47 | wheelchair. It glides smoothly toward the back. |
| 0x180448 | 42 | As Honoka leaves, she quickly turns to me. |
| 0x180473 | 38 | Please take good care of my daughters. |
| 0x18049a | 8 | ...HUH!? |
| 0x1804a3 | 17 | Wha--!? Dau--!?\n |
| 0x1804b5 | 16 | Your daughters!? |
| 0x1804c6 | 47 | Her only reply is a smile, and she returns to\n |
| 0x1804f6 | 48 | pushing the wheelchair. The two disappear into\n |
| 0x180527 | 9 | the back. |
| 0x180531 | 11 | Hey, wait-- |
| 0x18053d | 41 | I rise, calling to them without thinking. |
| 0x180567 | 48 | But this time, there is no protest, no outcry.\n |
| 0x180598 | 31 | The hall remains deadly silent. |
| 0x1805b8 | 21 | It is time to depart. |
| 0x1805ce | 26 | Huh? But... what about...? |
| 0x1805e9 | 16 | We should hurry. |
| 0x1805fa | 49 | Oshtor sharply looks back--some kind of signal.\n |
| 0x18062c | 44 | A clamor begins rippling through the grand\n |
| 0x180659 | 7 | hall... |
| 0x180661 | 34 | Wh-What is the meaning of this!?\n |
| 0x180684 | 46 | H-H-How can an insignificant little boy like\n |
| 0x1806b3 | 7 | him--!? |
| 0x1806bb | 48 | He may have rescued Her Highness, but even so... |
| 0x1806ec | 45 | Granting him the kamunagi? What is my liege\n |
| 0x18071a | 46 | thinking...? Or is he truly worthy of such a\n |
| 0x180749 | 8 | gift...? |
| 0x180752 | 49 | Absolutely right! What in the world is my liege\n |
| 0x180784 | 32 | thinking!? This is unforgivable! |
| 0x1807a5 | 8 | Silence! |
| 0x1807ae | 11 | Nyergh...!? |
| 0x1807ba | 49 | Unforgivable, you say? And why would the Mikado\n |
| 0x1807ec | 44 | ever need the forgiveness of offal like you? |
| 0x180819 | 47 | You dare question the authority of our liege,\n |
| 0x180849 | 41 | insolent fool!? You will know your place! |
| 0x180873 | 39 | Nyeh... H-H-How dare you challenge me-- |
| 0x18089b | 48 | And what of it? Have you deluded yourself into\n |
| 0x1808cc | 35 | thinking you're special in any way? |
| 0x1808f0 | 43 | You disgrace the name of the Eight Pillar\n |
| 0x18091c | 9 | Generals. |
| 0x180926 | 12 | Nyarrrrgh... |
| 0x180933 | 50 | Please, not here. We are in the audience hall...\n |
| 0x180966 | 48 | I do sympathize, but we must keep our composure. |
| 0x180997 | 44 | Hmhmhm... A mere commoner, gifted with the\n |
| 0x1809c4 | 45 | Kamunagi of Chains...? What sort of joke is\n |
| 0x1809f2 | 5 | this? |
| 0x1809f8 | 47 | Now... I must say, that was quite unexpected.\n |
| 0x180a28 | 48 | You seem destined to have a strange life indeed. |
| 0x180a59 | 48 | So all that stuff that just happened... that's\n |
| 0x180a8a | 11 | not normal? |
| 0x180a96 | 49 | I would have thought it impossible. Even saving\n |
| 0x180ac8 | 47 | the princess should not mark you as worthy of\n |
| 0x180af8 | 23 | the Kamunagi of Chains. |
| 0x180b10 | 44 | Impossible. So they're that big a deal...?\n |
| 0x180b3d | 41 | Actually, you know what? Don't tell me.\n |
| 0x180b67 | 17 | Don't wanna know. |
| 0x180b79 | 48 | They are the Kamunagi of Chains, and daughters\n |
| 0x180baa | 46 | of High Priestess Lady Honoka--her successors. |
| 0x180bd9 | 33 | Would you listen to me for once!? |
| 0x180bfb | 43 | They come from a long line of kamunagi of\n |
| 0x180c27 | 43 | incomparable power... called upon only in\n |
| 0x180c53 | 10 | dire need. |
| 0x180c5e | 45 | There are some rare cases in which they are\n |
| 0x180c8c | 45 | bestowed upon another, but only to those of\n |
| 0x180cba | 15 | great standing. |
| 0x180cca | 43 | Not only that, but these two hold special\n |
| 0x180cf6 | 36 | meaning as the Kamunagi of Chains... |
| 0x180d1b | 35 | Chains...? I don't really get it.\n |
| 0x180d3f | 20 | What does that mean? |
| 0x180d54 | 49 | I have not the slightest clue. I cannot hope to\n |
| 0x180d86 | 39 | fathom the depths of my liege's wisdom. |
| 0x180dae | 37 | However, one thing remains certain.\n |
| 0x180dd4 | 47 | In this, my liege has truly acknowledged your\n |
| 0x180e04 | 10 | abilities. |
| 0x180e0f | 27 | You've got to be kidding... |
| 0x180e2b | 37 | I would not say such a thing in jest. |
| 0x180e51 | 47 | In the long history of Yamato, none have ever\n |
| 0x180e81 | 43 | received such honor as you did moments ago. |
| 0x180ead | 50 | It is equal to receiving a gift of land from the\n |
| 0x180ee0 | 42 | Mikado. Words do not do the honor justice. |
| 0x180f0b | 47 | It would also appear that you have caught the\n |
| 0x180f3b | 45 | eyes of us figureheads of the nation... for\n |
| 0x180f69 | 20 | better or for worse. |
| 0x180f7e | 42 | So there's going to be trouble up ahead,\n |
| 0x180fa9 | 16 | is your point... |
| 0x180fba | 43 | I did say you are fated for a strange life. |
| 0x180fe6 | 49 | I can tell from Oshtor's smile that the subtext\n |
| 0x181018 | 32 | is "just give up and accept it." |
| 0x181039 | 39 | Urgh... how did it end up like this...? |
| 0x181061 | 46 | Just one problem after another, but not much\n |
| 0x181090 | 41 | we can do about it. Next on the list is-- |
| 0x1810ba | 49 | What the hell am I supposed to do with these two? |
| 0x1810ec | 43 | Returning them... is out of the question.\n |
| 0x181118 | 45 | I'd get eaten alive. This kamunagi-whatever\n |
| 0x181146 | 7 | crap... |
| 0x18114e | 48 | The hell is that guy thinking, giving me these\n |
| 0x18117f | 43 | two? And on top of that, they're Honoka's\n |
| 0x1811ab | 12 | daughters... |
| 0x1811b8 | 49 | God, her DAUGHTERS... Even her just being there\n |
| 0x1811ea | 48 | was a shock, but she has daughters this old too? |
| 0x18121b | 49 | Welcome back, Haku. So, what about this reward?\n |
| 0x18124d | 49 | A gift from the Mikado must be quite something,\n |
| 0x18127f | 10 | I'd think. |
| 0x18128a | 50 | And... unfortunately... Kuon and the others were\n |
| 0x1812bd | 27 | waiting for me at the gate. |
| 0x1812d9 | 37 | Oh, Kuon. Well, the reward was, uh... |
| 0x1812ff | 44 | Not jewels or fine pottery... Too mundane!\n |
| 0x18132c | 44 | It has to be something special... Hee hee,\n |
| 0x181359 | 11 | what IS it? |
| 0x181365 | 51 | Kuon dashes forward, a curious smile on her face,\n |
| 0x181399 | 42 | but then she stops with her brow furrowed. |
| 0x1813c4 | 24 | And, ah... Who are they? |
| 0x1813dd | 47 | Kuon points at the two girls leaning on me...\n |
| 0x18140d | 41 | and dressed in rather revealing clothing. |
| 0x181437 | 16 | His gaze wavers. |
| 0x181448 | 32 | Is something the matter, Master? |
| 0x181469 | 11 | Mas... ter? |
| 0x181475 | 32 | Well, uh. How do I put this...\n |
| 0x181496 | 38 | The Mikado kinda said I can have them. |
| 0x1814bd | 10 | Have them? |
| 0x1814c8 | 12 | As a reward. |
| 0x1814d5 | 10 | ...Reward. |
| 0x1814e0 | 28 | These two... are the reward? |
| 0x1814fd | 28 | We now belong to our Master. |
| 0x18151a | 43 | We have just recently become our Master's\n |
| 0x181546 | 36 | flesh puppets. Uruuru and Saraana.\n |
| 0x18156b | 23 | A pleasure to meet you. |
| 0x181583 | 8 | Bfwrfh!? |
| 0x18158c | 27 | From awakening until sleep. |
| 0x1815a8 | 48 | To bed, bathe, and even matters of the toilet.\n |
| 0x1815d9 | 37 | We shall take care of all your needs. |
| 0x1815ff | 12 | Our purpose. |
| 0x18160c | 51 | Anything our Master orders, we will do. Anything.\n |
| 0x181640 | 44 | If he desires, we will @@ or ** or even %%\n |
| 0x18166d | 7 | his &&. |
| 0x181675 | 46 | For that is the sole purpose of our existence. |
| 0x1816a4 | 18 | N-No, that's not-- |
| 0x1816b7 | 38 | What the hell are these girls saying!? |
| 0x1816de | 18 | ...You disgust me. |
| 0x1816f1 | 46 | Those eyes... She's looking at me like I'm a\n |
| 0x181720 | 20 | maggot--no, lower... |
| 0x181735 | 48 | Hee hee. Well now, love, looks like you've got\n |
| 0x181766 | 45 | yourself a little harem here. Marvelous work. |
| 0x181794 | 46 | That's not it at all! I didn't ask for this,\n |
| 0x1817c3 | 41 | OK? I can't just refuse a gift from the\n |
| 0x1817ed | 7 | Mikado! |
| 0x1817f5 | 48 | I guess you're right. You couldn't have helped\n |
| 0x181826 | 3 | it. |
| 0x18182a | 33 | Something about her smile is...\n |
| 0x18184c | 17 | kinda scaring me. |
| 0x18185e | 31 | I-I believe in you, Sir Haku... |
| 0x18187e | 48 | I-I believe that... that you are not that sort\n |
| 0x1818af | 32 | of person... I believe in you... |
| 0x1818d0 | 43 | ...Somehow, it's Rulutieh's reaction that\n |
| 0x1818fc | 18 | stings the most... |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_05.json` com a forma:
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
