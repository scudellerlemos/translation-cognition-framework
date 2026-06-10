# Cena ch_12_16 — pacote de traducao (177 linhas)

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
- ATENCAO charset: Gate FALHOU: a fonte do jogo não tem diacríticos — pangrama pt-BR renderiza como '@' (evidência in-game: artifacts/char1.png, char2.png). Estratégia adotada: TRANSLITERAÇÃO na gravação (acento→ASCII) 
  -> ESCREVA o campo `t` na forma canonica COM acentos/til normais (ex.: "você", "coração"). A transliteracao p/ ASCII e feita DEPOIS pelo script de reinsercao — nao remova acentos voce mesmo. Apenas nao dependa do acento para DISTINGUIR sentido (ex.: evite pares que so diferem por acento), pois ele some no jogo.

## 3. Glossario relevante (subconjunto desta cena)
| termo | categoria | traducao | regra | spoiler |
|---|---|---|---|---|
| amamunii | Comida | amamunii | manter_original | none |
| Boro-Gigiri | Criatura | Boro-Gigiri | manter_original | none |
| Cohort | Organizacao | Coorte | traduzir | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Innkeeper | UI | Estalajadeira | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Tatari | Criatura | Tatari | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |

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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Ukon** (major): Traduza as falas de/sobre Ukon como o personagem 'Ukon' por si so. NAO insinue outra identidade, patente oculta ou disfarce. Mantenha qualquer ambiguidade do original.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Ukon's Cohort` -> `Coorte do Ukon` (SISTEMA, 12_04)
- `Innkeeper` -> `Estalajadeira` (rotulo, 11_06)
- `But...` -> `Mas...` (Man, root)
- `me?` -> `mim?` (Maroro, 12_13)
- `I see...` -> `Entendo...` (Haku, 12_04)
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

## 7. Linhas a traduzir
> **DISCIPLINA DE ORCAMENTO (byte_budget):** a traducao TRANSLITERADA (sem acentos — o `c`
> de cedilha e os acentos somem na gravacao) deve **CABER** no byte_budget da linha. pt-BR
> costuma ser ~15-20% mais longo que EN: em linhas curtas/UI (budget baixo) **seja conciso**
> (ex.: 'adicionado ao' -> 'no'; corte redundancia), preservando sentido. Estourar muito o
> orcamento causa overflow no jogo. Conte os tokens de formatacao ({c5} etc.) no tamanho.
| offset | byte_budget | source |
|---|---|---|
| 0x4f047 | 35 | Here's to our victory, men! Cheers! |
| 0x4f06b | 13 | Ukon's Cohort |
| 0x4f079 | 10 | Cheeeeers! |
| 0x4f084 | 47 | The inn's dining hall fills with laughter and\n |
| 0x4f0b4 | 46 | jovial chatter, giving it a pleasant ambience. |
| 0x4f0e3 | 27 | After the Tatari arrived... |
| 0x4f0ff | 50 | Once it digested the body of the Boro-Gigiri, it\n |
| 0x4f132 | 38 | quietly slunk away back into its cave. |
| 0x4f159 | 53 | From what I've been told, they're loath to come out\n |
| 0x4f18f | 45 | of their pits, so we shouldn't have to worry. |
| 0x4f1bd | 47 | And Ukon's company cleaned up the rest of the\n |
| 0x4f1ed | 13 | gigiri, so... |
| 0x4f1fb | 50 | Travelers can use that mountain pass without any\n |
| 0x4f22e | 12 | danger, now. |
| 0x4f23b | 9 | Innkeeper |
| 0x4f245 | 19 | Come now, drink up. |
| 0x4f259 | 7 | Phew... |
| 0x4f261 | 39 | It's nice to drink and relax like this. |
| 0x4f289 | 50 | Upon hearing of our victory, the innkeeper broke\n |
| 0x4f2bc | 49 | out some of her best sake to share with everyone. |
| 0x4f2ee | 48 | I had to water it down to be able to drink it.\n |
| 0x4f31f | 47 | It's good straight, yeah, but I shouldn't get\n |
| 0x4f34f | 7 | wasted. |
| 0x4f357 | 47 | It's got a peculiar flavor, but it's not bad.\n |
| 0x4f387 | 17 | Just... distinct. |
| 0x4f399 | 49 | I wash down a bite of amamunii with the sake as\n |
| 0x4f3cb | 18 | I watch the crowd. |
| 0x4f3e2 | 53 | Meanwhile, Kuon has been sitting next to me staring\n |
| 0x4f418 | 32 | into her cup, not saying a word. |
| 0x4f439 | 33 | What's wrong? Not to your liking? |
| 0x4f45b | 49 | It's not that it's bad--a little strong, maybe,\n |
| 0x4f48d | 6 | but... |
| 0x4f494 | 48 | At a time like this, it'd be nice to have some\n |
| 0x4f4c5 | 12 | mead around. |
| 0x4f4d2 | 52 | Despite her disappointed tone, Kuon goes on eating\n |
| 0x4f507 | 35 | and drinking heartily all the same. |
| 0x4f52b | 26 | Hey, you kids drinkin' up? |
| 0x4f546 | 48 | Ukon makes his way over with a particularly...\n |
| 0x4f577 | 47 | intimidatingly sized cup, his face already red. |
| 0x4f5a7 | 52 | C'mon, why don't you join us instead of lurking in\n |
| 0x4f5dc | 21 | the corner over here? |
| 0x4f5f2 | 52 | You're the stars of this party, after all. Nothing\n |
| 0x4f627 | 50 | wrong with soaking in the attention a little, huh? |
| 0x4f65a | 51 | I'll pass. I'm not too eager to sit in the middle\n |
| 0x4f68e | 26 | of a crowd of sweaty guys. |
| 0x4f6a9 | 44 | Same here. I'm... not really a crowd person. |
| 0x4f6d6 | 49 | Ahahaha! You really are something, y'know that,\n |
| 0x4f708 | 40 | kid? Your plan went off without a hitch! |
| 0x4f731 | 48 | That... really wasn't enough to call a "plan."\n |
| 0x4f762 | 41 | I was playing things pretty off-the-cuff. |
| 0x4f78c | 17 | That's just fine. |
| 0x4f79e | 50 | You came up with it under pressure and executed,\n |
| 0x4f7d1 | 48 | and got results. It's impressive, staying cool\n |
| 0x4f802 | 10 | like that. |
| 0x4f80d | 49 | Most guys in your situation would've buckled or\n |
| 0x4f83f | 31 | panicked, not scheme a way out. |
| 0x4f85f | 23 | You're overpraising me. |
| 0x4f877 | 53 | I don't know if you're being modest or this is just\n |
| 0x4f8ad | 46 | how you are, but I'm liking you more an' more. |
| 0x4f8dc | 52 | Though, hey, full disclosure--I admit I was pretty\n |
| 0x4f911 | 42 | worried by how much the hike wore you out. |
| 0x4f93c | 51 | Guh... Not like I have a leg to stand on with that. |
| 0x4f970 | 37 | And you shone back there, too, missy. |
| 0x4f996 | 3 | Me? |
| 0x4f99a | 50 | Yeah. If you hadn't lured that Tatari out of its\n |
| 0x4f9cd | 39 | lair, it all would've been for nothing. |
| 0x4f9f5 | 44 | I didn't think you'd actually pull it off!\n |
| 0x4fa22 | 41 | Color me surprised you did something so\n |
| 0x4fa4c | 9 | reckless. |
| 0x4fa56 | 54 | Honestly, when you came up with that plan, I thought\n |
| 0x4fa8d | 36 | you were joking to lighten the mood. |
| 0x4fab2 | 21 | Was it that reckless? |
| 0x4fac8 | 49 | C'mon, now. If I'd told you to do what she did,\n |
| 0x4fafa | 42 | would you be able to carry out that order? |
| 0x4fb25 | 35 | No, I'd tell you it's impossible... |
| 0x4fb49 | 52 | Kuon having to pull me along the first time we ran\n |
| 0x4fb7e | 17 | rises in my mind. |
| 0x4fb90 | 51 | I sure as hell couldn't run like that, that's for\n |
| 0x4fbc4 | 5 | sure. |
| 0x4fbca | 44 | Ahaha, I'm just a little nimble, that's all. |
| 0x4fbf7 | 39 | I see. We'll leave it at that, I guess. |
| 0x4fc1f | 48 | Anyway! The gigiri extermination was a success\n |
| 0x4fc50 | 29 | thanks to you two joining us. |
| 0x4fc6e | 27 | Please accept my gratitude. |
| 0x4fc8a | 17 | Ukon bows deeply. |
| 0x4fc9c | 42 | C'mon, you're giving us too much credit... |
| 0x4fcc7 | 49 | Friendsh, Yamatansh, COUNTRYmen! Exschlude your\n |
| 0x4fcf9 | 46 | DEARESHT Maroro nnnot from your rrrevelsh...\n |
| 0x4fd28 | 13 | What SHAY ye? |
| 0x4fd36 | 41 | Ha! And here's our other conquering hero. |
| 0x4fd60 | 50 | A white shadow, its face fast becoming a fearful\n |
| 0x4fd93 | 38 | red, comes wriggling across toward us. |
| 0x4fdba | 48 | Oh ho HO! Dosht thou partake of mmmosht SHWEET\n |
| 0x4fdeb | 51 | libations? Come, wet thy shpirit with SHMOOTHESHT\n |
| 0x4fe1f | 5 | sake. |
| 0x4fe25 | 25 | Urk. He reeks of booze... |
| 0x4fe3f | 49 | Since he killed the bulk of the gigiri with his\n |
| 0x4fe71 | 44 | magic, Maroro's being hailed as a hero, too. |
| 0x4fe9e | 48 | He's being poured drink after drink, and keeps\n |
| 0x4fecf | 41 | accepting. Guy's already drunk as a fish. |
| 0x4fef9 | 51 | Accoladesh and bonush pay alike FLING themshelves\n |
| 0x4ff2d | 45 | upon my person thanksh to your aid! Nyoho HO! |
| 0x4ff5b | 49 | Thanks, but I didn't really... do anything that\n |
| 0x4ff8d | 31 | warrants a whole lot of praise. |
| 0x4ffad | 50 | Ah, ah, pray silence thy proteshts! Th'art SHUCH\n |
| 0x4ffe0 | 39 | a hhhumble man, Mashter Haku, truuuuly. |
| 0x50008 | 48 | Maroro prods my cheek with his finger. Please,\n |
| 0x50039 | 22 | please leave me alone. |
| 0x50050 | 49 | ForSHOOTH, thou nnnnurshed me to health through\n |
| 0x50082 | 50 | our journey'sh perils, and protected me from the\n |
| 0x500b5 | 18 | loathshome gigiri. |
| 0x500c8 | 40 | Thou art my BOSHOM friend, Mashter Haku. |
| 0x500f1 | 50 | Now I'm his "bosom friend." Great. I've ascended\n |
| 0x50124 | 22 | the ranks in his eyes. |
| 0x5013b | 44 | And now he's totally attached to me. Cripes. |
| 0x50168 | 48 | Hey, missy. Weren't you saying something about\n |
| 0x50199 | 24 | heading for the capital? |
| 0x501b2 | 49 | Mm. We're planning to leave first thing tomorrow. |
| 0x501e4 | 45 | Meanwhile, Kuon and Ukon have moved on to a\n |
| 0x50212 | 29 | completely different subject. |
| 0x50230 | 32 | Hey. You two. Help me out, here. |
| 0x50251 | 45 | Gonna do more sightseeing while you're there? |
| 0x5027f | 50 | There's that, but... it's more to find a job for\n |
| 0x502b2 | 14 | Haku, I think. |
| 0x502c1 | 51 | The kid, huh? So he's not your attendant after all? |
| 0x502f5 | 49 | Wh--Who's an attendant? She's taking care of me\n |
| 0x50327 | 48 | because I was an AMNESIAC LOST IN THE MOUNTAINS. |
| 0x50358 | 50 | Ha! Wouldn't it be better for appearances' sake,\n |
| 0x5038b | 45 | though? And what's this about having amnesia? |
| 0x503b9 | 49 | I don't even remember my own name. "Haku" is an\n |
| 0x503eb | 19 | alias Kuon gave me. |
| 0x503ff | 53 | Since I've accepted looking after him, it's my duty\n |
| 0x50435 | 37 | to see him become safely independent. |
| 0x5045b | 55 | And because he's not really suited to physical labor,\n |
| 0x50493 | 43 | I thought we'd try our luck in the capital. |
| 0x504bf | 38 | Fortunately, he's quite a wise person. |
| 0x504e6 | 8 | I see... |
| 0x504ef | 54 | Ukon takes a gulp from his cup, downing its contents\n |
| 0x50526 | 48 | in one go. He places the empty cup on the table. |
| 0x50557 | 52 | Aahh. Well, if that's the case, why don't you come\n |
| 0x5058c | 14 | along with us? |
| 0x5059b | 25 | To the capital, you mean? |
| 0x505b5 | 51 | Yeah. We originally came out here to pick up some\n |
| 0x505e9 | 40 | cargo and escort it back to the capital. |
| 0x50612 | 51 | Since the cargo got delayed, I decided to take up\n |
| 0x50646 | 27 | the gigiri job, and then... |
| 0x50662 | 34 | Well, we know how that turned out. |
| 0x50685 | 41 | Ukon's expression grows slightly distant. |
| 0x506af | 51 | I've got no choice but to leave the incapacitated\n |
| 0x506e3 | 45 | here in the village, so we're down a few men. |
| 0x50711 | 52 | And if you join up with us, you'll be paid, 'course. |
| 0x50746 | 52 | Kuon would be coming onboard as an apothecary, and\n |
| 0x5077b | 52 | the kid... Well, I guess "consultant" works for you. |
| 0x507b0 | 53 | It's good money. We've got plenty of funds from the\n |
| 0x507e6 | 38 | reward for the gigiri hunt, after all. |
| 0x5080d | 49 | Aren't you worried, kid? Traveling alone with a\n |
| 0x5083f | 47 | delic--fragi--vuln--...alone with a young lady? |
| 0x5086f | 48 | Why did you keep correcting yourself just now,\n |
| 0x508a0 | 9 | I wonder? |
| 0x508aa | 49 | Didn't mean anything by it, promise. Two people\n |
| 0x508dc | 41 | could get outnumbered easily, that's all. |
| 0x50906 | 49 | It's safer to travel with more companions. More\n |
| 0x50938 | 25 | fun, too. What d'you say? |
| 0x50952 | 5 | Mm... |
| 0x50958 | 49 | Thanks for the offer, but I think we'll have to\n |
| 0x5098a | 21 | respectfully decline. |
| 0x509a0 | 22 | Aw, come on. How come? |
| 0x509b7 | 51 | With the number of men you brought with you, that\n |
| 0x509eb | 40 | cargo must be something pretty valuable. |
| 0x50a14 | 37 | Hm. Yeah, I guess you could say that. |
| 0x50a3a | 51 | With that in mind, the risk of a bandit attack on\n |
| 0x50a6e | 45 | your company to get to the cargo is too high. |
| 0x50a9c | 49 | Oh, no, the cargo's guards'll be augmenting our\n |
| 0x50ace | 50 | numbers. No bandit would be dumb enough to try it. |
| 0x50b01 | 52 | But I won't make a pest of myself asking you about\n |
| 0x50b36 | 29 | it. Just think it over, yeah? |
| 0x50b54 | 51 | With that, Ukon returns to the throng of the party. |

## 8. Formato de saida EXIGIDO
Escreva `translations_12_16.json` com a forma:
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
