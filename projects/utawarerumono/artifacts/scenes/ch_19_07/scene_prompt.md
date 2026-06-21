# Cena ch_19_07 — pacote de traducao (659 linhas)

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
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Miruhj | Personagem | Miruhj | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Shichirya | Personagem | Shichirya | manter_original | none |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| Ukon | Personagem | Ukon | manter_original | major |
| Uncle | Cultural | Tio | traduzir | none |
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
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Woman` -> `Mulher` (sistema, 14_07)
- `OK?` -> `tá?` (Garota, 12_01)
- `Hmmm... Then if you still aren't married even\n` -> `Hmmm... Então se você ainda não casou nem\n` (Garota (memória), root)
- `when you're really old, I can marry you, OK?` -> `quando estiver bem velho, eu caso com você, tá?` (Garota (memória), root)
- `right?` -> `né?` (Haku, 12_03)
- `You better come. Pinky swear! Cross your heart\n` -> `É bom você vir. Promessa de mindinho! Jura\n` (Garota (memória), root)
- `manor.` -> `mansão.` (Oshtor, 19_01)
- `anything.` -> `nada.` (Haku, 17_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `something.` -> `de alguma coisa.` (Haku, 11_10)
- `Nnnngh...` -> `Nnh...` (Nekone, 18_01)
- `Yeah, yeah.` -> `É, é.` (Haku, 18_01)
- `U-Understood...` -> `E-Entendido...` (Rulutieh, 18_01)
- `door.` -> `porta.` (Haku, 11_07)
- `I believe.` -> `acho eu.` (Nekone, 14_09)
- `U-Um...` -> `E-Ei...` (Rulutieh, 14_09)
- `me.` -> `mim.` (Garota, 17_01)
- `her head.` -> `sua cabeça.` (Garota, 18_01)
- `of it.` -> `disso.` (Haku, 17_01)
- `too...` -> `também...` (Ukon, 15_01)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `a bit.` -> `um bit.` (Haku, 13_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Urk...` -> `Urgh...` (Haku, 12_06)
- `Grrr...` -> `Grrr...` (Haku, 18_01)
- `hands.` -> `as mãos.` (Kuon, root)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `Right.` -> `direito.` (Kuon, 15_01)
- `You like it?` -> `Estão gostando?` (Haku, 18_01)
- `EEP!?` -> `EEEK!?` (Atuy, 16_01)
- `food.` -> `comida.` (Garota, 17_01)
- `*Shudder*` -> `*Tremor*` (Kuon, root)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `agree?` -> `concorda?` (Ougi, 18_05)
- `hostage.` -> `reféns.` (Haku, 15_03)
- `another.` -> `outra.` (Rulutieh, 17_01)
- `stuff.` -> `isso.` (Haku, 14_04)
- `them.` -> `deles.` (Kuon, 11_05)
- `about this?` -> `sobre isso?` (Nosuri, 18_01)
- `Nn...` -> `Nnh...` (Haku, 17_01)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `today.` -> `hoje.` (Atuy, 18_01)
- `for you.` -> `para você.` (Ougi, 13_08)
- `Mikado.` -> `Mikado.` (Rulutieh, 14_02)
- `hand.` -> `mão.` (Haku, 13_01)
- `brother...` -> `irmão...` (Nekone, 15_01)
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
| 0x186a58 | 17 | Hey Uncle. Uncle! |
| 0x186a6a | 42 | Quit calling me that. Makes me feel old.\n |
| 0x186a95 | 49 | I dunno if I've lived long enough to be 'Uncle'\n |
| 0x186ac7 | 4 | age. |
| 0x186acc | 33 | But you are my uncle, aren't you? |
| 0x186aee | 17 | Enough with that! |
| 0x186b00 | 6 | Whah!? |
| 0x186b07 | 28 | Mo-om, Uncle's being meeaan! |
| 0x186b24 | 5 | Woman |
| 0x186b2a | 48 | Oh dear. Is he now? But boys are often mean to\n |
| 0x186b5b | 50 | the girls they like most, so try to forgive him.\n |
| 0x186b8e | 3 | OK? |
| 0x186b92 | 32 | Is that supposed to be a joke?\n |
| 0x186bb3 | 20 | Don't be ridiculous. |
| 0x186bc8 | 47 | Really? Well, I wouldn't mind at all, you know. |
| 0x186bf8 | 47 | Hmmm... Then if you still aren't married even\n |
| 0x186c28 | 44 | when you're really old, I can marry you, OK? |
| 0x186c55 | 11 | Quiet, you. |
| 0x186c61 | 10 | Nyah-nyah! |
| 0x186c6c | 41 | Urgh... That little brat. She gets more\n |
| 0x186c96 | 20 | annoying every year. |
| 0x186cab | 34 | Fine. No more of my curry for you. |
| 0x186cce | 34 | H-Hey, let's not be too hasty...\n |
| 0x186cf1 | 36 | That stuff was honestly pretty good. |
| 0x186d16 | 6 | Right? |
| 0x186d1d | 50 | ...Eh, fine. I'll drop by sometime. But I better\n |
| 0x186d50 | 36 | see some of that curry on the table. |
| 0x186d75 | 44 | Hee hee, OK. But you gotta play with me too. |
| 0x186da2 | 19 | Yeah, yeah. I will. |
| 0x186db6 | 48 | You better come. Pinky swear! Cross your heart\n |
| 0x186de7 | 32 | and hope to die! It's a promise. |
| 0x186e08 | 43 | OK, OK, I got it! Geez, why am I making a\n |
| 0x186e34 | 28 | stupid promise like this...? |
| 0x186e51 | 48 | Cross my heart and hope to die, stick a needle\n |
| 0x186e82 | 17 | in my eye. There! |
| 0x18a878 | 25 | A summons from Mikazuchi? |
| 0x18a892 | 46 | I was working on my literacy assignments one\n |
| 0x18a8c1 | 42 | afternoon when Nekone told me, grim-faced. |
| 0x18a8ec | 49 | Yes. A message has been sent to us to go to his\n |
| 0x18a91e | 6 | manor. |
| 0x18a925 | 46 | Mikazuchi... that guy we visited on Oshtor's\n |
| 0x18a954 | 39 | behalf? Imperial Guard of the Left...\n |
| 0x18a97c | 6 | right? |
| 0x18a983 | 46 | He felt like Oshtor's opposite... He's kinda\n |
| 0x18a9b2 | 46 | menacing, and seems like a soldier more than\n |
| 0x18a9e1 | 9 | anything. |
| 0x18a9eb | 49 | Yes, that Lord Mikazuchi. The message requested\n |
| 0x18aa1d | 35 | that the two of us go to his manor. |
| 0x18aa41 | 14 | The two of us? |
| 0x18aa50 | 31 | What does the guy want with us? |
| 0x18aa74 | 41 | What's the sour face? You nervous about\n |
| 0x18aa9e | 46 | something...? I can't blame you, considering\n |
| 0x18aacd | 14 | it's THAT guy. |
| 0x18aadc | 31 | This must be some kind of ploy. |
| 0x18aafc | 7 | ...Huh? |
| 0x18ab04 | 46 | He must be inviting those closest to my dear\n |
| 0x18ab33 | 46 | brother... to beguile them into becoming his\n |
| 0x18ab62 | 10 | own pawns. |
| 0x18ab6d | 47 | I have no doubt in my mind that is why he has\n |
| 0x18ab9d | 14 | called for us. |
| 0x18abac | 39 | Well, I've got SOME doubt in my mind... |
| 0x18abd4 | 50 | You must be cautious. You are falling right into\n |
| 0x18ac07 | 38 | the Imperial Guard of the Left's trap. |
| 0x18ac2e | 47 | Yeah, I dunno... I think it'd be a little too\n |
| 0x18ac5e | 43 | obvious. Aren't you just overthinking this? |
| 0x18ac8a | 50 | I sigh in exasperation, but I also remember that\n |
| 0x18acbd | 36 | ferocious smile on Mikazuchi's face. |
| 0x18ace2 | 22 | It can't be... can it? |
| 0x18acf9 | 49 | If you knew what kind of person he actually is,\n |
| 0x18ad2b | 36 | you would not be saying such things. |
| 0x18ad50 | 42 | I can tell, though. That man is plotting\n |
| 0x18ad7b | 10 | something. |
| 0x18ad86 | 52 | Those cold, merciless eyes, and his cruel laugh...\n |
| 0x18adbb | 16 | They say it all. |
| 0x18adcc | 34 | I'm not sure that's exactly proof. |
| 0x18adef | 42 | That said, she might have a point there... |
| 0x18ae1a | 49 | Do you understand? You must not let him deceive\n |
| 0x18ae4c | 4 | you! |
| 0x18ae51 | 46 | General Mikazuchi has been my dear brother's\n |
| 0x18ae80 | 43 | enemy for years... If you falter, he will\n |
| 0x18aeac | 12 | consume you. |
| 0x18aeb9 | 40 | And thus we arrive at Mikazuchi's manor. |
| 0x18aee2 | 47 | Lord Haku, Lady Nekone, welcome. We have been\n |
| 0x18af12 | 35 | waiting for you... Please, come in. |
| 0x18af36 | 9 | Nnnngh... |
| 0x18af40 | 47 | Before she even sees Mikazuchi, Nekone cowers\n |
| 0x18af70 | 47 | behind my back, peeking nervously from my side. |
| 0x18afa0 | 45 | Miruhj chuckles quietly, noting her blatant\n |
| 0x18afce | 16 | display of fear. |
| 0x18afdf | 17 | Please, this way. |
| 0x18aff1 | 29 | C-Come on. We need to follow. |
| 0x18b00f | 11 | Yeah, yeah. |
| 0x18b01b | 46 | Looks as though she still feels compelled to\n |
| 0x18b04a | 17 | fulfill her duty. |
| 0x18b05c | 50 | I proceed into the manor, Nekone trailing behind\n |
| 0x18b08f | 27 | me and pushing from behind. |
| 0x18b0ab | 48 | But what does Mikazuchi want with us? It's not\n |
| 0x18b0dc | 42 | like last time, when we had something to\n |
| 0x18b107 | 10 | deliver... |
| 0x18b112 | 48 | I am afraid there is not much I can say on the\n |
| 0x18b143 | 47 | matter... I am sure Lord Mikazuchi will brief\n |
| 0x18b173 | 12 | you in full. |
| 0x18b180 | 45 | "Heh heh heh. I suggest you look forward to\n |
| 0x18b1ae | 44 | this."... are the only words I was told to\n |
| 0x18b1db | 7 | convey. |
| 0x18b1e3 | 8 | E-Eep... |
| 0x18b1ec | 50 | I must apologize, but another guest is currently\n |
| 0x18b21f | 47 | present, and you may have to wait in the back\n |
| 0x18b24f | 8 | briefly. |
| 0x18b258 | 14 | Another guest? |
| 0x18b267 | 45 | Yes. It was a rather sudden visit, and Lord\n |
| 0x18b295 | 33 | Mikazuchi could not refuse him... |
| 0x18b2b7 | 44 | A guest that even Mikazuchi can't refuse...? |
| 0x18b2e4 | 17 | Has someone come? |
| 0x18b2f9 | 45 | As we walk, a voice calls out from beyond a\n |
| 0x18b327 | 44 | sliding door. Must have heard our footsteps. |
| 0x18b354 | 47 | U-Um! Th-These are... personal guests of Lord\n |
| 0x18b384 | 47 | Mikazuchi. I can vouch for their credibility... |
| 0x18b3b4 | 49 | Miruhj's voice cracks noticeably as he responds\n |
| 0x18b3e6 | 29 | to the voice beyond the door. |
| 0x18b404 | 31 | The voice wasn't Mikazuchi's.\n |
| 0x18b424 | 40 | Who could make Miruhj this flustered...? |
| 0x18b44d | 48 | Hm. Guests for you? Wonders truly never cease.\n |
| 0x18b47e | 42 | Perhaps it will begin to rain spears next. |
| 0x18b4a9 | 48 | So this must be that other guest. Who could it\n |
| 0x18b4da | 44 | be if he's talking to Mikazuchi so casually? |
| 0x18b507 | 45 | U-Um, I truly apologize for any displeasure\n |
| 0x18b535 | 42 | I may have caused. We shall leave at once. |
| 0x18b560 | 41 | I do not mind. By all means, let them in. |
| 0x18b58a | 12 | B-B-B-But... |
| 0x18b597 | 50 | These guests have piqued my interest. You do not\n |
| 0x18b5ca | 16 | mind, of course? |
| 0x18b5db | 8 | ...No... |
| 0x18b5e4 | 51 | I hear Mikazuchi give his permission to the guest\n |
| 0x18b618 | 17 | behind the doors. |
| 0x18b62a | 15 | U-Understood... |
| 0x18b63a | 47 | Miruhj has paled, and I can see sweat beading\n |
| 0x18b66a | 45 | on his forehead as he whispers, hand on the\n |
| 0x18b698 | 5 | door. |
| 0x18b69e | 49 | I am... deeply sorry about this... but will you\n |
| 0x18b6d0 | 16 | accompany me in? |
| 0x18b6e1 | 50 | He is a more merciful man than Lord Mikazuchi...\n |
| 0x18b714 | 10 | I believe. |
| 0x18b71f | 34 | Is that supposed to be reassuring? |
| 0x18b742 | 14 | A-After you... |
| 0x18b751 | 25 | I appreciate your coming. |
| 0x18b76b | 31 | Mikazuchi is first to greet us. |
| 0x18b78b | 39 | Across from him sits the other guest,\n |
| 0x18b7b3 | 47 | presumably...in military attire, with a young\n |
| 0x18b7e3 | 12 | page nearby. |
| 0x18b7f0 | 49 | Who is this guy...? I can tell he's no ordinary\n |
| 0x18b822 | 43 | person just from the atmosphere. He's got\n |
| 0x18b84e | 9 | presence. |
| 0x18b858 | 7 | U-Um... |
| 0x18b860 | 47 | Miruhj seems confused as to where to seat us,\n |
| 0x18b890 | 42 | dithering anxiously. The man looks over,\n |
| 0x18b8bb | 14 | appraising us. |
| 0x18b8ca | 9 | H-He's... |
| 0x18b8d4 | 21 | Hm? Someone you know? |
| 0x18b8ea | 47 | I ask Nekone, as she seems to have recognized\n |
| 0x18b91a | 48 | him. She shrinks back even more, hiding behind\n |
| 0x18b94b | 3 | me. |
| 0x18b94f | 52 | Th-That man is one of the Eight Pillar Generals...\n |
| 0x18b984 | 11 | Lord Raiko! |
| 0x18b990 | 46 | Raiko... the general Kuon was talking about,\n |
| 0x18b9bf | 30 | with the brilliant strategies! |
| 0x18b9de | 45 | Nekone, having been hiding this whole time,\n |
| 0x18ba0c | 47 | suddenly scampers out from behind me and bows\n |
| 0x18ba3c | 9 | her head. |
| 0x18ba46 | 15 | U-Um, I-I am... |
| 0x18ba56 | 45 | Raiko's gaze falls on Nekone, and something\n |
| 0x18ba84 | 23 | appears to dawn on him. |
| 0x18ba9c | 46 | You would be... Oshtor's younger sister, then? |
| 0x18bacb | 7 | H-Huh!? |
| 0x18bad3 | 47 | H-How did you know about that...? Only a very\n |
| 0x18bb03 | 45 | small group of people are supposed to know... |
| 0x18bb31 | 48 | Nekone darts a suspicious glance at Mikazuchi,\n |
| 0x18bb62 | 46 | but he shrugs, as if to say he knows nothing\n |
| 0x18bb91 | 6 | of it. |
| 0x18bb98 | 44 | Then how does this guy know she's Oshtor's\n |
| 0x18bbc5 | 48 | sister? I thought she was supposed to be known\n |
| 0x18bbf6 | 10 | as Ukon's. |
| 0x18bc01 | 49 | Raiko responds with some reluctance, though his\n |
| 0x18bc33 | 40 | detached tone suggests it's no big deal. |
| 0x18bc5c | 36 | Information is the key to control.\n |
| 0x18bc81 | 47 | I have known for some time now that that girl\n |
| 0x18bcb1 | 20 | is Oshtor's sibling. |
| 0x18bcc6 | 17 | And I also know-- |
| 0x18bcd8 | 28 | Raiko then looks towards me. |
| 0x18bcf5 | 45 | That you, Haku, work undercover as Oshtor's\n |
| 0x18bd23 | 50 | agent, and perform tasks that he cannot publicly\n |
| 0x18bd56 | 8 | support. |
| 0x18bd5f | 47 | I didn't expect him to have information on me\n |
| 0x18bd8f | 6 | too... |
| 0x18bd96 | 48 | You seem surprised. Yet surely ignorance would\n |
| 0x18bdc7 | 41 | hardly befit one bearing the title of a\n |
| 0x18bdf1 | 15 | Pillar General. |
| 0x18be01 | 48 | I know quite a lot about you... but this would\n |
| 0x18be32 | 36 | mark our first meeting face-to-face. |
| 0x18be57 | 48 | It would appear my reputation precedes me, but\n |
| 0x18be88 | 43 | allow me to give you a proper introduction. |
| 0x18beb4 | 47 | As he speaks, Raiko gracefully rises from his\n |
| 0x18bee4 | 5 | seat. |
| 0x18beea | 49 | I have been granted the post of one of Yamato's\n |
| 0x18bf1c | 33 | Eight Pillar Generals. And also-- |
| 0x18bf3e | 49 | Raiko's gaze turns to Mikazuchi, sitting across\n |
| 0x18bf70 | 9 | from him. |
| 0x18bf7a | 30 | I am the brother of Mikazuchi. |
| 0x18bf99 | 46 | Right, I remember now. I guess it's not that\n |
| 0x18bfc8 | 27 | strange for him to be here. |
| 0x18bfe4 | 49 | Well, I'm Haku, and this is Nekone... Though...\n |
| 0x18c016 | 30 | I guess you already know that. |
| 0x18c035 | 41 | I am Shichirya. I serve as Lord Raiko's\n |
| 0x18c05f | 10 | attendant. |
| 0x18c06a | 50 | The boy alongside Raiko smiles cheerfully at us,\n |
| 0x18c09d | 22 | and gives a small bow. |
| 0x18c0b4 | 39 | Hm? That guy looks kinda like Miruhj... |
| 0x18c0dc | 45 | Miruhj seems to have noticed my expression,\n |
| 0x18c10a | 31 | and he whispers for my benefit. |
| 0x18c12a | 45 | Both Shichirya and I come from the same clan. |
| 0x18c158 | 25 | Aha. Well, that'll do it. |
| 0x18c172 | 24 | But certainly, Oshtor... |
| 0x18c18b | 48 | Raiko once again turns his eyes on us, and his\n |
| 0x18c1bc | 43 | mouth curls into a thoughtful smirk as he\n |
| 0x18c1e8 | 7 | speaks. |
| 0x18c1f0 | 8 | Wh-What? |
| 0x18c1f9 | 46 | The man does have a tendency to trust others\n |
| 0x18c228 | 48 | easily, but it is rare indeed for him to fully\n |
| 0x18c259 | 13 | rely on them. |
| 0x18c267 | 48 | I hear you two have not known each other long.\n |
| 0x18c298 | 46 | For him to rely on a man such as yourself...\n |
| 0x18c2c7 | 19 | Fascinating indeed. |
| 0x18c2db | 29 | But that begs the question.\n |
| 0x18c2f9 | 20 | Who exactly are you? |
| 0x18c30e | 46 | Raiko's eyes become sharper, his stare fixed\n |
| 0x18c33d | 13 | and piercing. |
| 0x18c34b | 45 | You met while Oshtor was traveling as Ukon,\n |
| 0x18c379 | 43 | escorting a caravan bound from Kujyuri...\n |
| 0x18c3a5 | 19 | That much is clear. |
| 0x18c3b9 | 43 | Yet you seem to have left no trail at all\n |
| 0x18c3e5 | 41 | prior... as if you just appeared out of\n |
| 0x18c40f | 43 | the blue one day, with no past to speak of. |
| 0x18c43b | 15 | Who are you...? |
| 0x18c44b | 49 | Honestly, I think I'm the one who wants to know\n |
| 0x18c47d | 14 | that the most. |
| 0x18c48c | 45 | If you find out anything, I'd appreciate it\n |
| 0x18c4ba | 19 | if you let me know. |
| 0x18c4ce | 48 | I shrug wryly as I reply. The tension in Raiko\n |
| 0x18c4ff | 48 | immediately fades, and his expression lightens\n |
| 0x18c530 | 6 | a bit. |
| 0x18c537 | 49 | I see. Yes, most interesting. A question easily\n |
| 0x18c569 | 45 | answered makes poor entertainment, after all. |
| 0x18c597 | 47 | With that, Raiko glides right past us, making\n |
| 0x18c5c7 | 13 | for the door. |
| 0x18c5d5 | 14 | Going already? |
| 0x18c5e4 | 46 | Raiko answers Mikazuchi without bothering to\n |
| 0x18c613 | 5 | turn. |
| 0x18c619 | 46 | ...Yes. I was merely close by, and thought I\n |
| 0x18c648 | 48 | would check in with my poor reprobate brother,\n |
| 0x18c679 | 3 | hm? |
| 0x18c67d | 44 | ...Mother would very much like to see you.\n |
| 0x18c6aa | 45 | You should come by the house, if the chance\n |
| 0x18c6d8 | 7 | arises. |
| 0x18c6e0 | 5 | Hm... |
| 0x18c6e6 | 42 | Mikazuchi's brow furrows at Raiko's words. |
| 0x18c711 | 9 | Farewell. |
| 0x18c71b | 44 | Raiko leaves with a strange abruptness, as\n |
| 0x18c748 | 43 | though he had suddenly lost interest in us. |
| 0x18c774 | 50 | Shichirya hurriedly follows... and Miruhj, after\n |
| 0x18c7a7 | 46 | a small bow, quietly exits to escort them out. |
| 0x18c7d6 | 50 | Mikazuchi remains where he is, motionless, still\n |
| 0x18c809 | 27 | staring at the closed door. |
| 0x18c825 | 6 | Urk... |
| 0x18c82c | 45 | Nekone once again hides behind my back, the\n |
| 0x18c85a | 43 | gloomy atmosphere apparently breaking her\n |
| 0x18c886 | 8 | resolve. |
| 0x18c88f | 42 | Who knows how much time passed after that. |
| 0x18c8ba | 45 | Mikazuchi suddenly turns his piercing stare\n |
| 0x18c8e8 | 48 | on us, as if to ask what we're still doing here. |
| 0x18c919 | 16 | Nngh... Nnngh... |
| 0x18c92a | 49 | What's going on here...? Ugh, you could cut the\n |
| 0x18c95c | 49 | tension with a knife. This feels so damn awkward. |
| 0x18c98e | 37 | Mikazuchi's cold stare bores into us. |
| 0x18c9b4 | 47 | Unable to handle the pressure, Nekone shrinks\n |
| 0x18c9e4 | 47 | further behind my back, hiding as best she can. |
| 0x18ca14 | 47 | She was talking a big game, but the second we\n |
| 0x18ca44 | 43 | end up alone with him--Gah!? I'm not your\n |
| 0x18ca70 | 7 | shield! |
| 0x18ca78 | 7 | Grrr... |
| 0x18ca80 | 46 | From time to time, Nekone glares at him in a\n |
| 0x18caaf | 44 | show of intimidation, but recoils from his\n |
| 0x18cadc | 13 | staring back. |
| 0x18caea | 47 | Uhh... so why exactly did you want us to come\n |
| 0x18cb1a | 11 | here today? |
| 0x18cb26 | 24 | ...Should be about time. |
| 0x18cb3f | 48 | At my timid question, Mikazuchi finally breaks\n |
| 0x18cb70 | 18 | his heavy silence. |
| 0x18cb83 | 11 | About time? |
| 0x18cb8f | 45 | D-Do you wish for a fight? Fine, I shall be\n |
| 0x18cbbd | 14 | your opponent! |
| 0x18cbcc | 14 | *jab* *fwoosh* |
| 0x18cbdb | 48 | If she's going to threaten him, could she stop\n |
| 0x18cc0c | 24 | using me as a shield...? |
| 0x18cc25 | 41 | Her little punches aren't doing much to\n |
| 0x18cc4f | 42 | intimidate him, but he might be annoyed.\n |
| 0x18cc7a | 17 | It's too quiet... |
| 0x18cc8c | 10 | Excuse me. |
| 0x18cc97 | 8 | ...Eep!? |
| 0x18cca0 | 51 | Nekone jumps in surprise at the voice and tightly\n |
| 0x18ccd4 | 38 | grabs on to my clothes, hands shaking. |
| 0x18ccfb | 18 | Ah, you have come. |
| 0x18cd0e | 46 | The preparations are complete, Lord Mikazuchi. |
| 0x18cd3d | 19 | Carry it over here. |
| 0x18cd51 | 13 | Yes, at once. |
| 0x18cd5f | 48 | Miruhj and several others show their deference\n |
| 0x18cd90 | 46 | to Mikazuchi, then enter with trays in their\n |
| 0x18cdbf | 6 | hands. |
| 0x18cdc6 | 20 | Sweets... and fruit? |
| 0x18cddb | 42 | Nekone tries her best to look completely\n |
| 0x18ce06 | 44 | unruffled as the table is filled with tray\n |
| 0x18ce33 | 11 | after tray. |
| 0x18ce3f | 47 | Holy crap, that's a lot... I've never seen so\n |
| 0x18ce6f | 38 | many fancy sweets in one place before. |
| 0x18ce96 | 50 | All these fruits are from the south, and they're\n |
| 0x18cec9 | 43 | even fresh--not that usual preserved stuff. |
| 0x18cef5 | 48 | I hear fresh fruit from the south costs an arm\n |
| 0x18cf26 | 46 | and a leg... Everything here must be worth a\n |
| 0x18cf55 | 8 | fortune. |
| 0x18cf5e | 46 | I gaze in awe at all the high-quality treats\n |
| 0x18cf8d | 28 | being placed in front of me. |
| 0x18cfaa | 10 | This is... |
| 0x18cfb5 | 39 | I have received all of these as reward. |
| 0x18cfdd | 10 | ...Reward? |
| 0x18cfe8 | 44 | These sweets and fruits were gifts that we\n |
| 0x18d015 | 25 | received from the Mikado. |
| 0x18d02f | 50 | The fruits are finest ambrosial, handpicked from\n |
| 0x18d062 | 45 | all across Yamato. And the artisanal luxury\n |
| 0x18d090 | 9 | bonbons-- |
| 0x18d09a | 10 | ...Miruhj. |
| 0x18d0a5 | 49 | Oh... M-My apologies! I did not mean to overstep. |
| 0x18d0d7 | 44 | Mikazuchi glowers in his servant's general\n |
| 0x18d104 | 41 | direction, and Miruhj hastily apologizes. |
| 0x18d12e | 22 | No matter. You may go. |
| 0x18d145 | 26 | Y-Yes, my lord. Excuse me. |
| 0x18d160 | 47 | Miruhj quickly bows his head, then returns to\n |
| 0x18d190 | 35 | his place among the other servants. |
| 0x18d1b4 | 33 | Finest fruits of the south, eh?\n |
| 0x18d1d6 | 26 | And these luxury sweets... |
| 0x18d1f1 | 47 | What exactly did he do to get all this? Guess\n |
| 0x18d221 | 45 | they don't call him one of the Twin Shields\n |
| 0x18d24f | 12 | for nothing. |
| 0x18d25c | 34 | So why is he offering it to us...? |
| 0x18d27f | 30 | Do you not think it beautiful? |
| 0x18d29e | 4 | Huh? |
| 0x18d2a3 | 50 | These sweets of the high court... Such intricate\n |
| 0x18d2d6 | 45 | patterns are near works of art in their own\n |
| 0x18d304 | 6 | right. |
| 0x18d30b | 14 | I... guess...? |
| 0x18d31a | 42 | And these brilliant fruits of the south.\n |
| 0x18d345 | 45 | The vivid colors truly are a beautiful sight. |
| 0x18d373 | 15 | Well... sure... |
| 0x18d383 | 27 | And the taste is exquisite. |
| 0x18d39f | 47 | The bonbons... soft jam within, crunchy shell\n |
| 0x18d3cf | 48 | without. The fruit... juicier and sweeter than\n |
| 0x18d400 | 10 | any other. |
| 0x18d40b | 9 | *Gulp*... |
| 0x18d415 | 41 | Sounds like somebody's mouth is watering. |
| 0x18d43f | 12 | A-Amazing... |
| 0x18d44c | 44 | I can smell the sweet and sour scents from\n |
| 0x18d479 | 48 | here... Fruits of the south... Court sweets...\n |
| 0x18d4aa | 10 | So many... |
| 0x18d4b5 | 50 | Nekone looks on in wonder, admiring the mountain\n |
| 0x18d4e8 | 42 | of treats before us... beginning to waver. |
| 0x18d513 | 49 | That pitapita... so big and glossy... It almost\n |
| 0x18d545 | 42 | looks like a completely different fruit... |
| 0x18d570 | 49 | And these sweets, they all look so beautiful...\n |
| 0x18d5a2 | 35 | I have never seen such decadence... |
| 0x18d5c6 | 43 | These gold ones... I have had one before.\n |
| 0x18d5f2 | 48 | My dear brother brought me some. They are made\n |
| 0x18d623 | 12 | from eggs... |
| 0x18d630 | 50 | Haltingly, Nekone draws closer and closer to the\n |
| 0x18d663 | 45 | delicious spread, as though she is entranced. |
| 0x18d691 | 51 | Did this guy just invite us here to show all this\n |
| 0x18d6c5 | 39 | off? He doesn't really seem the type... |
| 0x18d6ed | 12 | You like it? |
| 0x18d6fa | 51 | At the sound of Mikazuchi's voice, Nekone finally\n |
| 0x18d72e | 24 | crashes back to reality. |
| 0x18d747 | 14 | Heh heh heh... |
| 0x18d756 | 51 | She's completely frozen... locked in place by the\n |
| 0x18d78a | 48 | leer of a vicious predator toying with its prey. |
| 0x18d7bb | 5 | Eep!? |
| 0x18d7c1 | 50 | Nekone's body stiffens as the fog lifts, leaving\n |
| 0x18d7f4 | 32 | her trapped in Mikazuchi's gaze. |
| 0x18d815 | 4 | Eat. |
| 0x18d81a | 33 | What's wrong? You don't want any? |
| 0x18d83c | 39 | Um, I don't really get what you mean... |
| 0x18d864 | 49 | With such simple commands, I can't get a handle\n |
| 0x18d896 | 49 | on his intentions. All I can do is stare at the\n |
| 0x18d8c8 | 5 | food. |
| 0x18d8ce | 10 | *Smirk*... |
| 0x18d8d9 | 8 | Guh...!? |
| 0x18d8e2 | 13 | Ah... urgh... |
| 0x18d8f0 | 48 | This guy's terrifying. What a sinister grin...\n |
| 0x18d921 | 37 | He's gotta have some ulterior motive! |
| 0x18d947 | 19 | Why so modest? Eat. |
| 0x18d95b | 29 | That's why I invited you...\n |
| 0x18d979 | 31 | It was the perfect opportunity. |
| 0x18d999 | 50 | A... perfect opportunity...? If someone as great\n |
| 0x18d9cc | 45 | as one of the Twin Shields is offering us a\n |
| 0x18d9fa | 8 | feast... |
| 0x18da03 | 44 | D-Does that mean... he intends to kill us,\n |
| 0x18da30 | 30 | and this is our last meal...!? |
| 0x18da4f | 36 | Then Nekone was right all along...!? |
| 0x18da74 | 47 | Wh-What... What exactly are you... plotting...? |
| 0x18daa4 | 42 | ...Hm? I have no idea what you could mean. |
| 0x18dacf | 47 | D-Do not play games with me! I-I know exactly\n |
| 0x18daff | 18 | what your plan is! |
| 0x18db12 | 49 | These... These sweets. All these things I like.\n |
| 0x18db44 | 45 | You intend to use them to try to win me over! |
| 0x18db72 | 48 | And once you have done that, you intend for me\n |
| 0x18dba3 | 44 | to be your spy in my dear brother's ranks,\n |
| 0x18dbd0 | 12 | do you not!? |
| 0x18dbdd | 48 | Whew... That was close. I almost fell directly\n |
| 0x18dc0e | 14 | into his trap. |
| 0x18dc1d | 48 | Tough talk for someone who keeps hiding behind\n |
| 0x18dc4e | 10 | my back... |
| 0x18dc59 | 15 | ...Heh heh heh. |
| 0x18dc69 | 9 | *Shudder* |
| 0x18dc73 | 48 | Wh-Wh-What is it now? Trying to intimidate me,\n |
| 0x18dca4 | 48 | now your bribery has failed? I-I will not yield! |
| 0x18dcd5 | 14 | *Fwoosh* *jab* |
| 0x18dce4 | 49 | Dammit, quit challenging people from behind me... |
| 0x18dd16 | 43 | Hah... Worry not, child. I'm not planning\n |
| 0x18dd42 | 43 | anything of the sort. Nothing... at... all. |
| 0x18dd6e | 7 | *Smirk* |
| 0x18dd76 | 4 | Eep! |
| 0x18dd7b | 46 | Despite his words, his grin is more sinister\n |
| 0x18ddaa | 47 | than ever... He's done something to the food.\n |
| 0x18ddda | 15 | I just know it. |
| 0x18ddea | 30 | You could say... I wanted tea. |
| 0x18de09 | 45 | My liege bestowed these delicacies upon me.\n |
| 0x18de37 | 47 | I wished to have tea, but it would be awfully\n |
| 0x18de67 | 11 | dull alone. |
| 0x18de73 | 43 | Which is why I wished to have tea with you. |
| 0x18de9f | 8 | With us? |
| 0x18dea8 | 49 | I heard the girl enjoys sweets, and it would be\n |
| 0x18deda | 49 | nice to get to know a friend better. Do you not\n |
| 0x18df0c | 6 | agree? |
| 0x18df13 | 12 | ...A friend? |
| 0x18df20 | 30 | By friend, does he mean... me? |
| 0x18df3f | 47 | So you're saying you just... wanted to invite\n |
| 0x18df6f | 16 | us over for tea? |
| 0x18df80 | 39 | What else would I have invited you for? |
| 0x18dfa8 | 41 | Now that he says that... He still looks\n |
| 0x18dfd2 | 46 | terrifying... but I don't feel any animosity\n |
| 0x18e001 | 16 | from him at all. |
| 0x18e012 | 49 | If he really was plotting something, I probably\n |
| 0x18e044 | 42 | would have felt something more sinister... |
| 0x18e06f | 10 | ...*Smirk* |
| 0x18e07a | 49 | ...Yep, nevermind, that's pretty damn sinister.\n |
| 0x18e0ac | 45 | However you look at this, he's up to no good. |
| 0x18e0da | 42 | But Nekone aside, why set a trap for me?\n |
| 0x18e105 | 49 | Let's be real; I'm worth basically nothing as a\n |
| 0x18e137 | 8 | hostage. |
| 0x18e140 | 49 | And really, if he wanted to do us in, there are\n |
| 0x18e172 | 47 | easier ways of doing it than inviting us over\n |
| 0x18e1a2 | 8 | for tea. |
| 0x18e1ab | 47 | If he used plain old brute force, it would be\n |
| 0x18e1db | 24 | long over for us by now. |
| 0x18e1f4 | 42 | I glance to Nekone, and though she still\n |
| 0x18e21f | 41 | looks wary, her eyes keep flickering to\n |
| 0x18e249 | 17 | Dessert Mountain. |
| 0x18e25b | 44 | Ah well. Guess I'll take the plunge, then... |
| 0x18e288 | 45 | I pick up one of the so-called court sweets\n |
| 0x18e2b6 | 26 | and take a bite out of it. |
| 0x18e2d1 | 7 | Ah...!? |
| 0x18e2d9 | 27 | Whoa... this stuff's great! |
| 0x18e2f5 | 23 | Wh-What are you doing!? |
| 0x18e30d | 29 | Well, uh, y'know... Poison.\n |
| 0x18e32b | 19 | Testing for poison. |
| 0x18e33f | 46 | So this one's that eggy thing you mentioned,\n |
| 0x18e36e | 35 | H-Haku...!? What are you thinking!? |
| 0x18e392 | 46 | Just hold on for a second. It's gonna take a\n |
| 0x18e3c1 | 33 | moment before we get any results. |
| 0x18e3e3 | 47 | And with that, I begin to eat one treat after\n |
| 0x18e413 | 8 | another. |
| 0x18e41c | 48 | Mmph--! Thif crumbry texfture'f interefting...\n |
| 0x18e44d | 45 | Looks like it was fried in oil. It's really\n |
| 0x18e47b | 8 | filling. |
| 0x18e484 | 46 | And this fruit is...? It's red, and it has a\n |
| 0x18e4b3 | 18 | bunch of thorns... |
| 0x18e4c6 | 46 | That is a fruit found in the south, known as\n |
| 0x18e4f5 | 11 | a pitapita. |
| 0x18e501 | 50 | They spoil quite quickly, so you rarely see them\n |
| 0x18e534 | 45 | in the capital... at least, not as ripe and\n |
| 0x18e562 | 6 | sweet. |
| 0x18e569 | 48 | That one was cultivated in one of the Mikado's\n |
| 0x18e59a | 46 | private conservatories. It should be at peak\n |
| 0x18e5c9 | 9 | ripeness. |
| 0x18e5d3 | 47 | Owned by the Mikado? So these were originally\n |
| 0x18e603 | 46 | for him, huh... This is some real high-class\n |
| 0x18e632 | 6 | stuff. |
| 0x18e639 | 28 | ...S-So that is the fabled-- |
| 0x18e656 | 45 | She gulps. It sounds like she's practically\n |
| 0x18e684 | 24 | drooling at the thought. |
| 0x18e69d | 12 | Ah... ahh... |
| 0x18e6aa | 47 | You can even eat the seeds on these? It's got\n |
| 0x18e6da | 47 | a nice crunchy texture... Ah, that's delicious. |
| 0x18e70a | 48 | Oh man, this is just too good! If anyone chose\n |
| 0x18e73b | 48 | not to eat this, I would suuure feel sorry for\n |
| 0x18e76c | 5 | them. |
| 0x18e772 | 10 | N-Nnngh... |
| 0x18e77d | 48 | At long last, Nekone's hand slowly reaches for\n |
| 0x18e7ae | 18 | one of the fruits. |
| 0x18e7c1 | 33 | Hey, whoa, you sure about that?\n |
| 0x18e7e3 | 34 | Remember, it could be... poisoned! |
| 0x18e806 | 46 | Th-This is all part of my academic research!\n |
| 0x18e835 | 47 | I-I rarely have a chance to eat fruits of the\n |
| 0x18e865 | 11 | south, yes? |
| 0x18e871 | 45 | And culinary science will not advance if it\n |
| 0x18e89f | 45 | goes untasted. I-If I die, I die for science! |
| 0x18e8cd | 50 | *Munch*... Mmm! This sweetness, this sourness...\n |
| 0x18e900 | 44 | Is this the flavor of the tropical sun...?\n |
| 0x18e92d | 10 | *Munch*... |
| 0x18e938 | 16 | Guh...? N-Nngh!? |
| 0x18e949 | 40 | Nekone's face suddenly contorts in pain. |
| 0x18e972 | 36 | Wh-What!? Was it ACTUALLY poisoned!? |
| 0x18e997 | 27 | My gaze whips to Mikazuchi. |
| 0x18e9b3 | 46 | Unruffled, he pours something into a cup and\n |
| 0x18e9e2 | 19 | hands it to Nekone. |
| 0x18e9f6 | 17 | ...Have some tea. |
| 0x18ea08 | 45 | I was granted this as well... I hear it was\n |
| 0x18ea36 | 37 | harvested from the Kujyuri highlands. |
| 0x18ea5c | 47 | It has a rich and flavorful scent, like fruit\n |
| 0x18ea8c | 41 | itself. A very high-quality tea, you see? |
| 0x18eab6 | 45 | Miruhj adds brightly as his lord hands over\n |
| 0x18eae4 | 8 | the tea. |
| 0x18eaed | 14 | Unngh! Nnnngh! |
| 0x18eafc | 48 | She must be desperate. She seizes the tea from\n |
| 0x18eb2d | 41 | his hands, and gulps it down immediately. |
| 0x18eb57 | 47 | *Gulp* Whew... I thought I was going to choke\n |
| 0x18eb87 | 11 | to death... |
| 0x18eb93 | 43 | So you just got it stuck in your throat!?\n |
| 0x18ebbf | 32 | You really need to eat slower... |
| 0x18ebe0 | 45 | I-I put my life on the line for the sake of\n |
| 0x18ec0e | 11 | science...! |
| 0x18ec1a | 13 | A-And also... |
| 0x18ec28 | 27 | Nekone glares at Mikazuchi. |
| 0x18ec49 | 47 | I-I only accepted your help because it was an\n |
| 0x18ec79 | 46 | emergency. Do not think that you have earned\n |
| 0x18eca8 | 9 | my trust. |
| 0x18ecb2 | 49 | Oh, come on. You're really gonna treat him like\n |
| 0x18ece4 | 25 | that after he helped you? |
| 0x18ecfe | 44 | I-It... I do not recall asking for his help. |
| 0x18ed2b | 35 | Nekone looks away as she says this. |
| 0x18ed4f | 50 | Geez. What would Oshtor say if he ever found out\n |
| 0x18ed82 | 11 | about this? |
| 0x18ed8e | 33 | Urgh... A-Are you threatening me? |
| 0x18edb0 | 46 | Why the hell would I go to all that trouble?\n |
| 0x18eddf | 43 | Look, you should at least say "sorry" and\n |
| 0x18ee0b | 19 | "thank you" to him. |
| 0x18ee1f | 5 | Nn... |
| 0x18ee25 | 46 | Nekone holds her head, falling silent. She's\n |
| 0x18ee54 | 44 | probably dealing with some complex emotions. |
| 0x18ee81 | 25 | ...I am sorry. A-And...\n |
| 0x18ee9b | 10 | Thank you. |
| 0x18eea6 | 50 | After deliberating for a while, Nekone awkwardly\n |
| 0x18eed9 | 21 | mutters to Mikazuchi. |
| 0x18eeef | 14 | ...No problem. |
| 0x18eefe | 46 | After a moment, Mikazuchi gives her a nod of\n |
| 0x18ef2d | 14 | understanding. |
| 0x18ef3c | 50 | It almost seemed like Nekone's apology flustered\n |
| 0x18ef6f | 38 | him for a second. Maybe it's just my\n |
| 0x18ef96 | 12 | imagination? |
| 0x18efa3 | 29 | *Homf*... *nomf*... *munch*\n |
| 0x18efc1 | 10 | *munch*... |
| 0x18efcc | 50 | And despite her earlier mishap, Nekone continues\n |
| 0x18efff | 49 | to wolf down the snacks, tail wagging in delight. |
| 0x18f031 | 42 | It looks as though she's been completely\n |
| 0x18f05c | 32 | entranced by all the delicacies. |
| 0x18f07d | 21 | So, pretty good, huh? |
| 0x18f093 | 36 | I-It is... I do not find it, er...\n |
| 0x18f0b8 | 16 | It is tolerable. |
| 0x18f0c9 | 46 | Nekone falters as she answers, but continues\n |
| 0x18f0f8 | 18 | reaching for more. |
| 0x18f10b | 49 | I see... Well, at least it seems I was right in\n |
| 0x18f13d | 18 | inviting you then. |
| 0x18f150 | 7 | Urgh... |
| 0x18f158 | 43 | Nekone looks a little guilty as she faces\n |
| 0x18f184 | 10 | Mikazuchi. |
| 0x18f18f | 51 | Um, I th-thank you for... i-inviting us to tea...\n |
| 0x18f1c3 | 6 | today. |
| 0x18f1ca | 27 | It was... It was delicious. |
| 0x18f1e6 | 51 | ...I see. Well, glad you've taken a liking to it.\n |
| 0x18f21a | 38 | No need for modesty--eat all you want. |
| 0x18f241 | 36 | ...Th-Thank you. I will do so, then. |
| 0x18f266 | 28 | *Homf* *munch, munch, munch* |
| 0x18f283 | 46 | Heh heh heh... Good! It's best when children\n |
| 0x18f2b2 | 47 | can speak their mind and act as they'd like to. |
| 0x18f2e2 | 43 | Drink up. This tea is from your homeland,\n |
| 0x18f30e | 47 | Ennakamuy. I thought it might taste nostalgic\n |
| 0x18f33e | 8 | for you. |
| 0x18f347 | 14 | Oh... *sip*... |
| 0x18f356 | 46 | I'll have my men pack up the sweets and tea.\n |
| 0x18f385 | 32 | Take home as much as you please. |
| 0x18f3a6 | 22 | Can we really!? O-Oh-- |
| 0x18f3bd | 45 | Although she couldn't conceal her glee, she\n |
| 0x18f3eb | 47 | quickly covers her mouth, looking between him\n |
| 0x18f41b | 15 | and the treats. |
| 0x18f42b | 49 | Yes, you may. Take home as much as you can, and\n |
| 0x18f45d | 24 | share with your friends. |
| 0x18f476 | 46 | I tried sharing with my underlings, but they\n |
| 0x18f4a5 | 49 | all said they couldn't share in a gift from the\n |
| 0x18f4d7 | 7 | Mikado. |
| 0x18f4df | 48 | All that modesty. What's the point of being so\n |
| 0x18f510 | 15 | humble with me? |
| 0x18f520 | 50 | Mikazuchi gives another sinister grin, like he's\n |
| 0x18f553 | 29 | got some evil scheme in mind. |
| 0x18f571 | 50 | A smile like that would make you think you'd get\n |
| 0x18f5a4 | 47 | sent to the front lines for taking one of his\n |
| 0x18f5d4 | 6 | gifts. |
| 0x18f5db | 21 | Nekone gulps in fear. |
| 0x18f5f1 | 46 | Hmmm, but after preparing all the sweets and\n |
| 0x18f620 | 41 | fruits for Nekone, and even getting her\n |
| 0x18f64a | 17 | homeland's tea... |
| 0x18f65c | 33 | I mutter, for Nekone's ears only. |
| 0x18f67e | 47 | Hey, Nekone. He's kinda terrifying, but... he\n |
| 0x18f6ae | 34 | might actually be a real nice guy. |
| 0x18f6d1 | 47 | ...I don't think he realizes how other people\n |
| 0x18f701 | 8 | see him. |
| 0x18f70a | 22 | Th-That is impossible. |
| 0x18f721 | 32 | This man is my dear brother's... |
| 0x18f742 | 50 | Nekone takes an angry chomp of the bonbon in her\n |
| 0x18f775 | 5 | hand. |
| 0x18f77b | 45 | But I couldn't sense any hostility from her\n |
| 0x18f7a9 | 26 | towards Mikazuchi, either. |
| 0x18f7c4 | 44 | Maybe she just doesn't want to acknowledge\n |
| 0x18f7f1 | 48 | Oshtor's rival? What with how she dotes on her\n |
| 0x18f822 | 10 | brother... |
| 0x18f82d | 32 | I guess Mikazuchi's an OK guy.\n |
| 0x18f84e | 49 | His appearance and word choice just give people\n |
| 0x18f880 | 15 | the wrong idea. |
| 0x18f890 | 45 | But maybe if we have the right opportunity,\n |
| 0x18f8be | 14 | we could be... |
| 0x18f8cd | 48 | I glimpse him slowly extending his hand toward\n |
| 0x18f8fe | 47 | Nekone's head, just out of her range of vision. |
| 0x18f92e | 47 | Heh heh, that's right. Eat your fill! Eat all\n |
| 0x18f95e | 26 | you can and grow strong... |
| 0x18f979 | 26 | I get it now! He's just... |
| 0x18f994 | 45 | But just as he's about to pat Nekone's head-- |
| 0x18f9c2 | 9 | ...*Gasp* |
| 0x18f9cc | 9 | *Skitter* |
| 0x18f9d6 | 19 | Hrrngh... So close. |
| 0x18f9ea | 48 | A crooked grin crosses Mikazuchi's face, as if\n |
| 0x18fa1b | 48 | to end his sentence with "to wringing her neck." |
| 0x18fa4c | 44 | Wh-What are you trying to do!? I take back\n |
| 0x18fa79 | 45 | everything I said! You are not to be trusted! |
| 0x18faa7 | 21 | Y-You cannot fool me! |
| 0x18fabd | 31 | ...This is absolutely hopeless. |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_07.json` com a forma:
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
