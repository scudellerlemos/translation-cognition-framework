# Cena ch_13_09 — pacote de traducao (211 linhas)

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
| Cohort | Organizacao | Coorte | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Ah...` -> `Ah...` (Haku, 13_01)
- `again.` -> `vez.` (Ougi, 13_05)
- `this...` -> `isto...` (Kuon, 11_08)
- `Man` -> `Hom` (Sistema, 12_04)
- `instead.` -> `em vez disso.` (Haku, 11_10)
- `like that.` -> `assim.` (Ukon, 12_16)
- `Ukon's Cohorts` -> `Coorte do Ukon` (SISTEMA, 12_04)
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
| 0x79bcb | 51 | Even in lands across the sea, people speak of the\n |
| 0x79bff | 43 | Twin Shields, Lords Oshtor and Mikazuchi... |
| 0x79c2b | 50 | That aura he projects... He might even be on par\n |
| 0x79c5e | 7 | with... |
| 0x79c66 | 49 | I never imagined he'd be such a great, noble man. |
| 0x79c98 | 48 | If he's earning that kind of praise from Kuon... |
| 0x79cc9 | 22 | Is he really all that? |
| 0x79ce0 | 50 | Mm. There's that, yes, but I'm just... struck by\n |
| 0x79d13 | 49 | how much of this world is still unfamiliar to me. |
| 0x79d45 | 51 | Kuon speaks distantly, her eyes following the man\n |
| 0x79d79 | 41 | himself as he rides away with his troops. |
| 0x79da3 | 5 | Ah... |
| 0x79da9 | 49 | With a long-held exhale, Rulutieh slumps to the\n |
| 0x79ddb | 47 | ground like a puppet with strings suddenly cut. |
| 0x79e0b | 11 | Are you OK? |
| 0x79e17 | 49 | Ah... It feels like all the strength in my body\n |
| 0x79e49 | 10 | is gone... |
| 0x79e54 | 52 | I don't blame you, after all that. I know you were\n |
| 0x79e89 | 49 | scared, but it's gonna be all right now. Promise. |
| 0x79ebb | 16 | N-No, I meant... |
| 0x79ecc | 48 | It was just nervewracking... r-really speaking\n |
| 0x79efd | 24 | with Sir Oshtor himself. |
| 0x79f16 | 14 | So that's why. |
| 0x79f25 | 49 | I understand he's an important guy and all, but\n |
| 0x79f57 | 28 | you're a princess, Rulutieh. |
| 0x79f74 | 35 | Is he so high up the chain as that? |
| 0x79f98 | 34 | N-No, I'm... nothing, next to him. |
| 0x79fbb | 50 | Lord Oshtor began as but a footman unrank'd, and\n |
| 0x79fee | 51 | as a man unthinkably young aspire'd to the mantle\n |
| 0x7a022 | 18 | of Imperial Guard. |
| 0x7a035 | 47 | A more humble man--a man so loved amongst his\n |
| 0x7a065 | 31 | peers--th'art unlikely to meet. |
| 0x7a085 | 52 | I'faith, milady Rulutieh's quaking at his presence\n |
| 0x7a0ba | 52 | hath warrant, for even the Mikado laudeth his name\n |
| 0x7a0ef | 12 | with honors! |
| 0x7a0fc | 52 | Alas, there are those who brand milord an upstart,\n |
| 0x7a131 | 38 | but Maroro--Maroro knoweth far better. |
| 0x7a158 | 33 | So he's like the ideal folk hero. |
| 0x7a17a | 49 | Verily so. Great pride hath Maroro in his young\n |
| 0x7a1ac | 9 | lordship! |
| 0x7a1b6 | 23 | Why would you be proud? |
| 0x7a1ce | 47 | Ah--merely that his lordship and I share in a\n |
| 0x7a1fe | 46 | benefactor. Naught more complicated than that. |
| 0x7a22d | 41 | I'm not sure I get it, but if you say so. |
| 0x7a257 | 51 | Another thing, though, has anyone seen Ukon? He's\n |
| 0x7a28b | 16 | still not back-- |
| 0x7a29c | 19 | Did I hear my name? |
| 0x7a2b0 | 52 | The members of Ukon's company who had gone to meet\n |
| 0x7a2e5 | 48 | with the strike team reappear in timely fashion. |
| 0x7a316 | 50 | You sure took your sweet time. We didn't exactly\n |
| 0x7a349 | 24 | have it easy, back here. |
| 0x7a362 | 52 | My bad. We ran into some delays securing the cargo\n |
| 0x7a397 | 6 | again. |
| 0x7a39e | 49 | Ukon points over his shoulder, and sure enough,\n |
| 0x7a3d0 | 35 | the caravan is back together again. |
| 0x7a3f4 | 43 | Transporting this stuff safely is our top\n |
| 0x7a420 | 17 | priority, y'know. |
| 0x7a432 | 45 | How fared thy strike at the brigands' hold,\n |
| 0x7a460 | 12 | Master Ukon? |
| 0x7a46d | 47 | Ah, the surprise attack went almost TOO well.\n |
| 0x7a49d | 46 | The guidance from the strike team was perfect. |
| 0x7a4cc | 45 | We've got a few wounded, but no casualties.\n |
| 0x7a4fa | 17 | Everybody's fine. |
| 0x7a50c | 48 | But hey, I heard something about you capturing\n |
| 0x7a53d | 20 | the bandits' leader? |
| 0x7a552 | 51 | Oho, so the good tidings have reached thine ears.\n |
| 0x7a586 | 44 | All praise unto Master Haku for his triumph! |
| 0x7a5b3 | 34 | I was just looking out for myself. |
| 0x7a5d6 | 51 | C'mon, what're you talking about? I thought I was\n |
| 0x7a60a | 50 | putting you nice and safely out of the way, but... |
| 0x7a63d | 48 | You went and stole the show. I'm surprised you\n |
| 0x7a66e | 36 | rounded them up like that, honestly. |
| 0x7a693 | 44 | What? No, we just got caught up in a crazy\n |
| 0x7a6c0 | 24 | coincidence, that's all. |
| 0x7a6d9 | 46 | Hey, don't be so modest! Makes you seem like\n |
| 0x7a708 | 42 | you're being sarcastic, y'know? Gwahahaha! |
| 0x7a733 | 47 | It all fell into place by chance, but I don't\n |
| 0x7a763 | 39 | know if that's good luck or bad luck... |
| 0x7a78b | 51 | I'm sorry for putting Rulutieh in danger, though.\n |
| 0x7a7bf | 40 | I really didn't mean for that to happen. |
| 0x7a7e8 | 50 | Well, all's well that ends well. Besides, it's a\n |
| 0x7a81b | 39 | nice prestige booster for the princess. |
| 0x7a843 | 52 | You're really OK with it? It doesn't seem like the\n |
| 0x7a878 | 41 | kind of thing to subject a princess to... |
| 0x7a8a2 | 51 | Circumstances might demand she go out into battle\n |
| 0x7a8d6 | 52 | sooner or later. This was some experience for her,\n |
| 0x7a90b | 16 | if nothin' else. |
| 0x7a91c | 16 | Prestige, huh... |
| 0x7a92d | 50 | Now, if only she'd gain a little confidence from\n |
| 0x7a960 | 7 | this... |
| 0x7a968 | 24 | Ukon mumbles to himself. |
| 0x7a981 | 22 | Did you say something? |
| 0x7a998 | 42 | Nah, it's nothing. Just talking to myself. |
| 0x7a9c3 | 50 | All that aside, I'll bet there's a big reward in\n |
| 0x7a9f6 | 46 | store for the guy who caught the bandit chief! |
| 0x7aa25 | 47 | Come to think of it, he did mention a "formal\n |
| 0x7aa55 | 39 | commendation" or something like that... |
| 0x7aa7d | 48 | We're talking big. Probably enough for another\n |
| 0x7aaae | 45 | celebration, even if you split it a few ways. |
| 0x7aadc | 21 | S-Speakest thou true? |
| 0x7aaf2 | 49 | Yeah, I think it's safe to expect at least that\n |
| 0x7ab24 | 5 | much. |
| 0x7ab2a | 47 | H-Huzzah! Fate doth smile upon Maroro this day! |
| 0x7ab5a | 46 | Maroro suddenly bursts with such joy that he\n |
| 0x7ab89 | 22 | nearly starts dancing. |
| 0x7aba0 | 37 | Well, someone's in high spirits, huh? |
| 0x7abc6 | 49 | Though it doth shame me to admit, mine accounts\n |
| 0x7abf8 | 41 | of late are starved of gold to fill them. |
| 0x7ac22 | 47 | But lo, fortune ever turns! I-I may yet avail\n |
| 0x7ac52 | 48 | myself of a new inkstone, brushes, letter-paper! |
| 0x7ac83 | 48 | Maroro puts on a dopey smile at the thought of\n |
| 0x7acb4 | 31 | his newfound wealth, imagining. |
| 0x7acd4 | 42 | Dahahaha! I see. Look forward to it, then. |
| 0x7acff | 48 | Ukon laughs, patting Maroro's shoulder, though\n |
| 0x7ad30 | 25 | his expression is... odd. |
| 0x7ad4a | 3 | Man |
| 0x7ad4e | 48 | Man, we gotta get Lord Maroro to treat us to a\n |
| 0x7ad7f | 6 | drink! |
| 0x7ad86 | 11 | You idiot-- |
| 0x7ad92 | 18 | Oh, crap, right... |
| 0x7ada5 | 49 | The men surrounding Maroro, muttering, suddenly\n |
| 0x7add7 | 8 | clam up. |
| 0x7ade0 | 50 | Hm? There wasn't anything particularly offensive\n |
| 0x7ae13 | 21 | about that comment... |
| 0x7ae29 | 51 | Eh? What ails ye? A filled cup is hardly so great\n |
| 0x7ae5d | 40 | an expense, with such riches to my name. |
| 0x7ae86 | 50 | Despite Maroro's generous offer, the men shuffle\n |
| 0x7aeb9 | 34 | their feet, looking uncomfortable. |
| 0x7aedc | 31 | Wh-What is the matter, friends? |
| 0x7aefc | 48 | N-No worries. We appreciate the offer, though... |
| 0x7af2d | 51 | Thou needst not hold to such modesty! Let us eat,\n |
| 0x7af61 | 29 | drink, and be merry together! |
| 0x7af7f | 49 | Maroro insists, but the way the men decline him\n |
| 0x7afb1 | 24 | seems almost... pitying. |
| 0x7afca | 33 | Th-Thou desirest not such revels? |
| 0x7afec | 48 | Prithee! Master Haku! Thy bosom company amidst\n |
| 0x7b01d | 39 | our merry-making would be most welcome! |
| 0x7b045 | 48 | Well, I won't refuse being treated to a drink.\n |
| 0x7b076 | 29 | Especially a celebratory one. |
| 0x7b094 | 51 | Why won't you guys accept his invitation, though?\n |
| 0x7b0c8 | 42 | Wouldn't it be gracious to drink with him? |
| 0x7b0f3 | 50 | It's not like we don't appreciate the sentiment.\n |
| 0x7b126 | 48 | It's just that we know he's been saving money... |
| 0x7b157 | 51 | Yeah. Wouldn't it be better to use that money for\n |
| 0x7b18b | 19 | your family's debt? |
| 0x7b19f | 21 | Th-This is so, but... |
| 0x7b1b5 | 51 | If Maroro hath aught to offer, let him avail each\n |
| 0x7b1e9 | 38 | man of a cup of finest sake, at least. |
| 0x7b210 | 49 | You'll need money again after that, right? Boss\n |
| 0x7b242 | 47 | said your family asked him to repair the roof\n |
| 0x7b272 | 8 | again... |
| 0x7b27b | 30 | Eh? What's this thou speakest? |
| 0x7b29a | 38 | ...I thought so. You didn't know, huh? |
| 0x7b2c1 | 51 | Yeah, and if I recall, they ordered a whole bunch\n |
| 0x7b2f5 | 17 | of textiles, too. |
| 0x7b307 | 29 | Wh-What? Thou speakest truth? |
| 0x7b325 | 24 | Y-Yeah, I'm afraid so... |
| 0x7b33e | 49 | N-No! Say not such words to me. Say 'tis a lie... |
| 0x7b370 | 33 | Maroro looks at Ukon imploringly. |
| 0x7b392 | 48 | Um... Well. We all have to wake up from dreams\n |
| 0x7b3c3 | 13 | eventually... |
| 0x7b3d1 | 48 | A-And so Maroro descendeth into the torment of\n |
| 0x7b402 | 17 | debt once more... |
| 0x7b414 | 48 | Sorry, man. I couldn't bring myself to tell you. |
| 0x7b445 | 48 | Maroro sinks to the ground as though sapped of\n |
| 0x7b476 | 32 | life, Ukon's words a final blow. |
| 0x7b497 | 48 | Only the sounds of the forest break the silence. |
| 0x7b4c8 | 45 | ...All right. I've had about enough of this\n |
| 0x7b4f6 | 12 | somber mood. |
| 0x7b503 | 44 | Hey, don't get so down. It'll be my treat,\n |
| 0x7b530 | 8 | instead. |
| 0x7b539 | 8 | T-Truly? |
| 0x7b542 | 31 | Sure. We're friends, aren't we? |
| 0x7b562 | 51 | I don't really get what's going on, but I can buy\n |
| 0x7b596 | 49 | the guy a drink. I can't watch him be so pitiful. |
| 0x7b5c8 | 34 | That's very generous of you, Haku. |
| 0x7b5eb | 51 | But... I suppose it's fine. You earned this money\n |
| 0x7b61f | 20 | yourself, after all. |
| 0x7b634 | 50 | And I think it's very admirable to help a friend\n |
| 0x7b667 | 10 | like that. |
| 0x7b672 | 49 | I'll just take it out of your allowance, shall I? |
| 0x7b6a4 | 10 | Allowance? |
| 0x7b6af | 49 | Ah... Right. As long as I'm taking care of you,\n |
| 0x7b6e1 | 47 | I'll be managing your finances. You'll get an\n |
| 0x7b711 | 10 | allowance. |
| 0x7b71c | 35 | N-No, wait a second, why an allow-- |
| 0x7b740 | 48 | If I leave you in charge of your money, you're\n |
| 0x7b771 | 49 | going to blow it all on spending. You know it's\n |
| 0x7b7a3 | 5 | true. |
| 0x7b7a9 | 33 | Hngh... That's not true. Come on. |
| 0x7b7cb | 50 | You even said you'd treat everyone to drinks, so\n |
| 0x7b7fe | 39 | I think it's a fair assumption to make. |
| 0x7b826 | 47 | This is why I like you, kid. Hear that, boys?\n |
| 0x7b856 | 37 | Haku's footing the bill for everyone! |
| 0x7b87c | 50 | At Ukon's suggestion, everyone erupts into cheers. |
| 0x7b8af | 50 | Wha? Wait a second. I said I'd treat MARORO, not\n |
| 0x7b8e2 | 18 | the whole company! |
| 0x7b8f5 | 49 | You can't just say "it'll be my treat" in front\n |
| 0x7b927 | 38 | of everyone and only treat one person. |
| 0x7b94e | 51 | This is exactly what I'm talking about. I'll make\n |
| 0x7b982 | 48 | an exception this time and cover you. THIS time. |
| 0x7b9b3 | 51 | We'll make it a blowout at our usual place in the\n |
| 0x7b9e7 | 8 | capital! |
| 0x7b9f0 | 14 | Ukon's Cohorts |
| 0x7b9ff | 21 | Thanks for the treat! |
| 0x7ba15 | 29 | Wh--Who said anything about-- |
| 0x7ba33 | 49 | M-Master Haku! Thou wouldst go to such ends for\n |
| 0x7ba65 | 50 | me... Thy charity warmeth the cockles of my heart! |
| 0x7ba98 | 49 | Maroro clings to me as tears stream freely down\n |
| 0x7baca | 9 | his face. |
| 0x7bad4 | 30 | How... did it come to this...? |

## 8. Formato de saida EXIGIDO
Escreva `translations_13_09.json` com a forma:
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
