# Cena ch_23_07 — pacote de traducao (879 linhas)

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
- **pt-BR MODERNO (registro do jogador de hoje):** preferir a forma que um jogador BR atual usaria, não
  a "correta-mas-arcaica/truncada". Dois erros recorrentes pegos em QA in-game:
  - **Resposta de NOME** (`I'm…`/`My name's…`/`I am…` quando responde "qual seu nome?") → **"Meu nome é…"
    / "Eu me chamo…" / "Sou o(a)…"** conforme a voz. NUNCA "Eu sou" seco — refere-se a estado, soa
    truncado para apresentação.
  - **Léxico arcaico/erudito** (ex.: "ruminar"/"Rumino" por "pensar/refletir") só quando a VOZ do
    personagem pede; senão, a palavra que o público entende **de imediato**.
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
□ pt-BR moderno: forma que um jogador de HOJE usaria? (nome → "Meu nome é/Eu me chamo", não "Eu sou"; sem arcaísmo gratuito)
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
| Earth | Local | Terra | traduzir | major |
| Entua | Personagem | Entua | manter_original | major |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Neko | Personagem | Neko | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Shyahoro | Local | Shyahoro | manter_original | none |
| Soyankekur | Personagem | Soyankekur | manter_original | moderate |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
| Woman | UI | Mulher | traduzir | none |
| Woshis | Personagem | Woshis | manter_original | major |
| Yatanawarabe | Termo | Yatanawarabe | manter_original | none |

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

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Oshtor (twist final)** (critical): Trate Oshtor como o General da Direita vivo e atuante. NAO antecipe morte, sacrificio, heranca de mascara, nem que outro personagem assumira sua identidade. Sem foreshadowing desse desfecho.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `the imperial capital.` -> `a capital imperial.` (Haku, 17_01)
- `today.` -> `hoje.` (Atuy, 18_01)
- `Hey, Kuon...` -> `Ei, Haku...` (Kuon, 21_04)
- `What's the matter?` -> `O que foi?` (Haku, 15_02)
- `anything.` -> `nada.` (Haku, 17_01)
- `Atuy?` -> `Atuy?` (Ukon, 16_02)
- `water.` -> `água.` (Haku, 13_03)
- `appraising us.` -> `nos avaliando.` (Haku, 19_07)
- `speed.` -> `velocidade.` (Haku, 22_04)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `Ugh...` -> `Ugh...` (Haku, 13_02)
- `Ah!` -> `Ah!` (Garota, 18_01)
- `bewildered.` -> `confusa.` (Haku, 19_08)
- `Mikazuchi.` -> `Mikazuchi.` (Haku, 19_07)
- `capital.` -> `imperial.` (Kuon, 12_04)
- `...Haku.` -> `...Haku.` (Haku, 22_05)
- `Heh... Heh heh heh...` -> `Heh... Heh heh heh...` (Haku, 20_13)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `...You disgust me.` -> `...Você me repugna.` (Maroro, 19_05)
- `our guide.` -> `nosso guia.` (Protagonista, 21_03)
- `himself.` -> `si mesmo.` (Nekone, 14_04)
- `piece.` -> `peça.` (Haku, 20_06)
- `Kuon...` -> `Kuon...` (Kuon, 11_02)
- `Crew` -> `Grupo` (SISTEMA, 19_08)
- `Sir!` -> `Sim!` (Maroro, 12_09)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `What's up? Why the long face?` -> `Qual é? Que carinha funda é essa?` (Ukon, 22_02)
- `or anything.` -> `especificamente.` (Haku, 15_05)
- `it!` -> `isso!` (Narrator, 20_20)
- `from.` -> `de.` (Atuy, 16_02)
- `properly.` -> `direito.` (Nosuri, 19_02)
- `her.` -> `a ela.` (Kuon, 11_02)
- `Rulutieh.` -> `Rulutieh.` (Haku, 13_02)
- `Oh...` -> `Ah...` (Kuon, 11_01)
- `world.` -> `mundo.` (Haku, 16_01)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `...As you wish.` -> `...Como desejar.` (Oshtor, 23_01)
- `then?` -> `então?` (Kuon, 16_02)
- `What is this?` -> `O que é isto?` (Homem, 16_01)
- `delight.` -> `deleite.` (SYSTEM, 19_08)
- `...Wh--!?` -> `...Que--!?` (Protagonista, 20_21)
- `Hah... Now that I recall, you enjoyed weaving\n` -> `Hah... Agora que me lembro, você preferia tecer\n` (Protagonista, 20_21)
- `and cooking much more than warfare, didn't\n` -> `e cozinhar muito mais do que guerrear, não é?\n` (Protagonista, 20_21)
- `you...?` -> `você...?` (Kuon, 14_09)
- `That's right... You... never belonged on the\n` -> `É verdade... Você... nunca pertenceu ao\n` (Protagonista, 20_21)
- `battlefield...` -> `campo de batalha...` (Protagonista, 20_21)
- `That is not true!` -> `Isso não é verdade!` (Garota, 20_21)
- `I am your daughter! The daughter of a brave\n` -> `Sou sua filha! A filha de um bravo\n` (Protagonista, 20_21)
- `Uzurushan warrior!` -> `Guerreiro Uzurushan!` (Garota, 20_21)
- `That is enough...` -> `Isto é suficiente...` (Garota, 20_21)
- `You may live your life as your own woman...\n` -> `Pode viver sua vida como sua própria mulher...\n` (Protagonista, 20_21)
- `and find your own happiness...` -> `e encontre sua própria felicidade...` (Garota, 20_21)
- `Father...` -> `Pai...` (Garota, 20_21)
- `Father?` -> `Pai?` (Protagonista, 20_21)
- `...F-Father...? No... This can't be happening.\n` -> `...P-Pai...? Não... Isso não pode estar acontecendo.\n` (Protagonista, 20_21)
- `country.` -> `país.` (Haku, 17_01)
- `homeland.` -> `terra natal.` (Haku, 16_01)
- `But...` -> `mas...` (Kuon, 11_01)
- `soul.` -> `alma.` (Woman (Kuon), 20_11)
- `Yes...` -> `Sim...` (Rulutieh, 14_10)
- `you...` -> `você...` (Haku, 12_11)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `Who is it?` -> `Quem é?` (Kuon, 17_01)
- `Honoka.` -> `Honoka.` (Haku, 19_05)
- `work.` -> `trabalho.` (Protagonista, 16_01)
**Voz estabelecida dos falantes (amostra):**
- Protagonista: `Ngh... ghh...` -> `Nnh... aagh...`
- Protagonista: `Nn...\n` -> `Nnh...\n`
- Protagonista: `It's... warm...?` -> `Está... quente...?`
- Haku: `Urgh...` -> `Argh...`
- Haku: `Right?` -> `né?`
- Haku: `Nn...` -> `Nnh...`
- Garota: `Huh? Someone's over there...` -> `Hein? Tem alguém ali...`
- Garota: `Hey, you there! Could you spare a moment?` -> `Ei, você aí! Pode me dar um momento?`
- Garota: `Hey, I'm sorry for bothering you, but could I ask\n` -> `Ei, me desculpe, posso fazer\n`
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
| 0x285ebc | 50 | We leave the imperial capital, and head straight\n |
| 0x285eef | 24 | to the port city nearby. |
| 0x285f08 | 50 | From there we'll take a ship, and head to Tuskur\n |
| 0x285f3b | 47 | by ocean, just as Munechika and the others did. |
| 0x285f6b | 46 | As we get closer to our destination, a scent\n |
| 0x285f9a | 42 | hits our noses that's... hard to describe. |
| 0x285fc5 | 28 | It's the smell of the ocean. |
| 0x285fe2 | 46 | The trees by the roadside have taken strange\n |
| 0x286011 | 42 | shapes, different from the ones back home. |
| 0x28603c | 45 | It makes me realize how far we've gone from\n |
| 0x28606a | 21 | the imperial capital. |
| 0x286080 | 45 | And as I remember the capital... I remember\n |
| 0x2860ae | 46 | Shinonon, and the others we're leaving behind. |
| 0x2860dd | 48 | I'm also worried about Kuon, whose face clouds\n |
| 0x28610e | 41 | more the farther we get from the capital. |
| 0x286138 | 21 | But all that aside... |
| 0x28614e | 16 | I-It's so hot... |
| 0x28615f | 46 | Yeah. I heard it gets warmer in these parts,\n |
| 0x28618e | 48 | but this is way beyond warm... It's hot as hell. |
| 0x2861bf | 47 | What is this heat? It's like I'm trapped in a\n |
| 0x2861ef | 8 | sauna... |
| 0x2861f8 | 50 | We wipe the sweat from our brows, looking to the\n |
| 0x28622b | 30 | sky with anguish on our faces. |
| 0x28624a | 46 | You think so? But it's such a lovely day out\n |
| 0x286279 | 6 | today. |
| 0x286280 | 45 | So compared to Atuy's homeland, this heat's\n |
| 0x2862ae | 22 | practically nothing... |
| 0x2862c5 | 48 | But why the hell is it so hot? We haven't even\n |
| 0x2862f6 | 20 | gone that far south. |
| 0x28630b | 47 | This heat clearly isn't from simple change in\n |
| 0x28633b | 49 | latitude, but what else would affect it to this\n |
| 0x28636d | 7 | degree? |
| 0x286375 | 49 | Are the sea currents affecting weather patterns\n |
| 0x2863a7 | 37 | this much? Or... is it because of...? |
| 0x2863cd | 46 | Haku, what's got you so deep in thought like\n |
| 0x2863fc | 34 | that? Come on, everyone's waiting. |
| 0x28641f | 48 | Kuon calls out. Maybe it's my imagination, but\n |
| 0x286450 | 43 | her chipper tone might be masking her own\n |
| 0x28647c | 9 | feelings. |
| 0x286486 | 47 | Not a word about Tuskur since we left. Kuon's\n |
| 0x2864b6 | 46 | trying to avoid the subject so we don't feel\n |
| 0x2864e5 | 9 | guilty... |
| 0x2864ef | 12 | Hey, Kuon... |
| 0x2864fc | 18 | What's the matter? |
| 0x28650f | 47 | I want to make sure she's not pushing herself\n |
| 0x28653f | 36 | too hard... but I don't want to pry. |
| 0x286564 | 33 | ...Never mind. Be there in a sec. |
| 0x286586 | 41 | In the end, I can't bring myself to say\n |
| 0x2865b0 | 9 | anything. |
| 0x2865ba | 8 | Merchant |
| 0x2865c3 | 44 | Step right up, step right up! We got cheap\n |
| 0x2865f0 | 44 | shama, itow, and mamashu today! Super cheap! |
| 0x28661d | 49 | We arrive in some kind of bazaar with merchants\n |
| 0x28664f | 50 | and shops of all sorts, full of activity and life. |
| 0x286682 | 48 | All of us forget the heat for a moment, gazing\n |
| 0x2866b3 | 39 | around in awe at the unfamiliar sights. |
| 0x2866db | 48 | Hey there, pretty lady! We got some real sweet\n |
| 0x28670c | 44 | rintan fruits in right now! Why not try one? |
| 0x286739 | 41 | The shouts of the merchants fill the air. |
| 0x286763 | 42 | Oh, wow. Look at this hustle and bustle!\n |
| 0x28678e | 33 | I almost feel like I'm back home. |
| 0x2867b0 | 32 | Your hometown's like this place? |
| 0x2867d1 | 46 | This port is governed by Atuy's father, Lord\n |
| 0x286800 | 45 | Soyankekur. Little wonder that it resembles\n |
| 0x28682e | 9 | Shyahoro. |
| 0x286838 | 49 | I see. So you're used to sights like this then,\n |
| 0x28686a | 5 | Atuy? |
| 0x286870 | 46 | It's as lively as the market in the imperial\n |
| 0x28689f | 40 | capital, but everyone seems a bit more\n |
| 0x2868c8 | 11 | aggressive. |
| 0x2868d4 | 48 | The items on offer here are... much different... |
| 0x286905 | 50 | Rulutieh looks around with clear interest at the\n |
| 0x286938 | 48 | products lining the shops, muttering to herself. |
| 0x286969 | 45 | A strange fish that I've never seen before... |
| 0x286997 | 35 | Colorful apparel and accessories... |
| 0x2869bb | 49 | What grabs my attention, though, are those huge\n |
| 0x2869ed | 44 | fruits. You'd need both arms to carry one... |
| 0x286a1a | 45 | They're bright orange, and they give off an\n |
| 0x286a48 | 41 | alluring sweet scent that fills the area. |
| 0x286a72 | 45 | Wonder what that is. Are they going to pack\n |
| 0x286aa0 | 23 | that stuff in the ship? |
| 0x286ab8 | 51 | Ah, you've got your eye on those, have you, love?\n |
| 0x286aec | 13 | Well spotted! |
| 0x286afa | 44 | This fruit's actually a vital tool for any\n |
| 0x286b27 | 9 | seafarer. |
| 0x286b31 | 42 | The rintan fruit? I have read of this...\n |
| 0x286b5c | 44 | It is used to hydrate at sea when drinking\n |
| 0x286b89 | 16 | water is scarce. |
| 0x286b9a | 48 | Ooh, clever clogs Neko! The fruit has a lot of\n |
| 0x286bcb | 46 | sweet juice, and it stays fresh for days and\n |
| 0x286bfa | 5 | days! |
| 0x286c00 | 48 | That's why we often load a ship up with those,\n |
| 0x286c31 | 27 | instead of plain old water. |
| 0x286c4d | 49 | Um... Why don't you just load up a lot of water\n |
| 0x286c7f | 41 | then? Wouldn't that work just as well...? |
| 0x286ca9 | 48 | It doesn't take that long before water spoils,\n |
| 0x286cda | 43 | pet. So we rely on these fruits a lot more. |
| 0x286d06 | 44 | Huh...? Water spoils...? What do you mean?\n |
| 0x286d33 | 25 | Does the water taste bad? |
| 0x286d4d | 47 | ...Oh, right. I suppose Kujyuri's cold enough\n |
| 0x286d7d | 40 | that you don't have to worry about that. |
| 0x286da6 | 45 | We can't have our water out in the sunlight\n |
| 0x286dd4 | 39 | for too long, or it gets undrinkable.\n |
| 0x286dfc | 17 | Spoils like milk. |
| 0x286e0e | 37 | I... I had no idea that was possible. |
| 0x286e34 | 48 | Well, it makes sense. I bet water never spoils\n |
| 0x286e65 | 48 | where you're from, and the capital has running\n |
| 0x286e96 | 6 | water. |
| 0x286e9d | 47 | Atuy's right. There is absolutely no shame in\n |
| 0x286ecd | 47 | not knowing how to handle water situations on\n |
| 0x286efd | 7 | a ship! |
| 0x286f05 | 23 | Yep... That's about it. |
| 0x286f1d | 41 | Oh, this must be the fruit we ate while\n |
| 0x286f47 | 49 | traveling at sea. I was wondering how they kept\n |
| 0x286f79 | 12 | it so fresh. |
| 0x286f86 | 38 | But the flavor was a little... well... |
| 0x286fad | 50 | Hee hee, I think the one you had might have been\n |
| 0x286fe0 | 23 | a touch overripe, Kuon. |
| 0x286ff8 | 9 | Overripe? |
| 0x287002 | 42 | Hey mister. Could me and my friends have\n |
| 0x28702d | 23 | a piece of rintan each? |
| 0x287045 | 14 | Right you are! |
| 0x287054 | 44 | We all get our slices of rintan and take a\n |
| 0x287081 | 17 | bite out of them. |
| 0x287093 | 44 | Hm... It has a unique flavor. Kinda sweet,\n |
| 0x2870c0 | 35 | kinda sour... but it's pretty good. |
| 0x2870e4 | 42 | Yes. I see why they use it for hydration\n |
| 0x28710f | 38 | purposes--it is extraordinarily juicy. |
| 0x287136 | 49 | Ah, brings back memories. I used to eat tons of\n |
| 0x287168 | 46 | these back when I was cruisin' around on the\n |
| 0x287197 | 4 | sea. |
| 0x28719c | 46 | It's very sweet and sour, but quite delicious. |
| 0x2871cb | 47 | Hm? I don't know why... It's a similar taste,\n |
| 0x2871fb | 44 | but a little different from what I remember. |
| 0x287228 | 47 | It felt much thicker. Much sweeter than this... |
| 0x287258 | 29 | Mm. I suppose it's not bad.\n |
| 0x287276 | 26 | Ougi, grab me another one. |
| 0x287291 | 42 | Understood. This one seems to be at peak\n |
| 0x2872bc | 40 | ripeness; doubtless the ideal time for\n |
| 0x2872e5 | 12 | consumption. |
| 0x2872f2 | 45 | Hmm... ngh!? *Cough, hack* What IS this...?\n |
| 0x287320 | 22 | It tastes like liquor! |
| 0x287337 | 45 | Hee hee! Guess you got an overripe one too,\n |
| 0x287365 | 7 | Nosuri. |
| 0x28736d | 47 | The riper the rintan fruit gets, the more its\n |
| 0x28739d | 30 | contents ferment into alcohol. |
| 0x2873bc | 46 | Kuon and Nosuri had the ripe ones, so that's\n |
| 0x2873eb | 29 | what happened to the insides. |
| 0x287409 | 46 | Mister, which one's the ripest one you've got? |
| 0x287438 | 46 | Oh, you're lookin' for a drink? Hold on a sec. |
| 0x287467 | 48 | The merchant brings out another fruit from the\n |
| 0x287498 | 18 | back of his store. |
| 0x2874ab | 49 | This one here's pretty ripe. Ain't all the way,\n |
| 0x2874dd | 36 | but should be a bit easier to drink. |
| 0x287502 | 46 | He opens up a hole on the fruit with a small\n |
| 0x287531 | 46 | knife, and pours its contents out into a bowl. |
| 0x287560 | 44 | A murky-looking liquid gradually fills the\n |
| 0x28758d | 7 | bowl... |
| 0x287595 | 39 | Pretty neat, eh? As it gets ripe, the\n |
| 0x2875bd | 39 | inside-bits start melting in the shell. |
| 0x2875e5 | 46 | And the longer you let it sit, the better it\n |
| 0x287614 | 41 | gets. The really old ones cost a fortune! |
| 0x28763e | 47 | Huh... sounds pretty cool. I'll take a little\n |
| 0x28766e | 23 | sip, if you don't mind. |
| 0x287686 | 41 | Oh, Haku, make sure you save some for me. |
| 0x2876b0 | 49 | Hold it! If we're tasting liquor, you can leave\n |
| 0x2876e2 | 9 | it to me. |
| 0x2876ec | 50 | We all gather around, chatting happily about the\n |
| 0x28771f | 43 | drink. It's like we never left the capital. |
| 0x28774b | 50 | You're all pretty carefree for folks sailin' off\n |
| 0x28777e | 7 | to war. |
| 0x287786 | 45 | It makes me wonder if we're doing the right\n |
| 0x2877b4 | 18 | thing... I mean... |
| 0x2877c7 | 31 | Worried about the bosslady, eh? |
| 0x2877e7 | 46 | Outwardly, she yet remains unreadable... but\n |
| 0x287816 | 45 | who knows how she truly feels about all this. |
| 0x287844 | 25 | ...Yes, it does worry me. |
| 0x28785e | 44 | As for my dear sister, you need not worry.\n |
| 0x28788b | 50 | It has been a long time indeed since I have seen\n |
| 0x2878be | 16 | her so carefree. |
| 0x2878cf | 47 | Doesn't seem to me as though your sister ever\n |
| 0x2878ff | 29 | worries about anything, yeah? |
| 0x287921 | 49 | We look over to find a number of men staring at\n |
| 0x287953 | 13 | us from afar. |
| 0x287961 | 50 | The deputies of the Imperial Guard of the Right,\n |
| 0x287994 | 37 | correct? We have come as your guides. |
| 0x2879ba | 30 | Yes, that's us... and you are? |
| 0x2879d9 | 41 | They don't immediately answer her. They\n |
| 0x287a03 | 45 | carefully look us up and down, like they're\n |
| 0x287a31 | 14 | appraising us. |
| 0x287a40 | 28 | Who the hell are these guys? |
| 0x287a5d | 41 | They're dressed in fancy formal attire,\n |
| 0x287a87 | 31 | like the nobles in the capital. |
| 0x287aa7 | 48 | But they're definitely not giving off the vibe\n |
| 0x287ad8 | 10 | of nobles. |
| 0x287ae3 | 50 | More like their demeanors are completely at odds\n |
| 0x287b16 | 28 | with what they're wearing... |
| 0x287b33 | 48 | All of the men are fairly tall, about the same\n |
| 0x287b64 | 20 | height as Jachdwalt. |
| 0x287b79 | 48 | Maybe not to General-Vurai-levels, but they're\n |
| 0x287baa | 18 | all pretty ripped. |
| 0x287bbd | 47 | Thanks to that, their formalwear is stretched\n |
| 0x287bed | 47 | to its limits. Most of it looks ready to burst. |
| 0x287c1d | 48 | It almost feels like they're being forced into\n |
| 0x287c4e | 43 | those clothes... The disconnect is almost\n |
| 0x287c7a | 7 | creepy. |
| 0x287c82 | 42 | Seriously, who the hell are these guys...? |
| 0x287cad | 28 | Oh, love, those people are-- |
| 0x287cca | 48 | Just as Atuy seems about to explain, it happens. |
| 0x287cfb | 43 | I hear a rumbling in the earth, and I see\n |
| 0x287d27 | 44 | something closing in on us with incredible\n |
| 0x287d54 | 6 | speed. |
| 0x287d5b | 19 | ...uuuuuuUUUYYYYYY! |
| 0x287d6f | 4 | Huh? |
| 0x287d74 | 6 | Ugh... |
| 0x287d7b | 49 | Atuy gives a sigh of resignation, her shoulders\n |
| 0x287dad | 24 | drooping as she notices. |
| 0x287dc6 | 28 | AAAAAAAATUUUUUUUUUYYYYYYYY!! |
| 0x287de3 | 48 | From beyond the road I see a giant scruffy man\n |
| 0x287e14 | 49 | charging toward us, a massive dust cloud in his\n |
| 0x287e46 | 5 | wake. |
| 0x287e4c | 25 | Oh, how I've MISSED you!! |
| 0x287e66 | 50 | The man uses his momentum to bound high into the\n |
| 0x287e99 | 48 | air, then descends on Atuy like an unkempt hawk. |
| 0x287eca | 3 | Ah! |
| 0x287ece | 24 | Wh-Wh-What is all this!? |
| 0x287ee7 | 26 | Oh, Atuy, Atuy, my Atuy!\n |
| 0x287f02 | 19 | How have you been!? |
| 0x287f16 | 43 | The man clutches Atuy in a ferocious hug,\n |
| 0x287f42 | 39 | rubbing his cheek happily against hers. |
| 0x287f6a | 47 | This is clearly an emergency, but it's such a\n |
| 0x287f9a | 43 | weird one that we're all frozen in place,\n |
| 0x287fc6 | 11 | bewildered. |
| 0x287fd2 | 45 | Y-Yes. It's, ah, been a while, hasn't it...\n |
| 0x288000 | 5 | Papa. |
| 0x288006 | 10 | P-Papa...? |
| 0x288011 | 42 | Atuy's father... Soyankekur the Mariner?\n |
| 0x28803c | 43 | He seems pretty different from when I saw\n |
| 0x288068 | 13 | him before... |
| 0x288076 | 44 | Oh, Atuy. You left home without so much as\n |
| 0x2880a3 | 45 | a goodbye! I was worried sick about you, aye! |
| 0x2880d1 | 24 | *Nuzzle, nuzzle, nuzzle* |
| 0x2880ea | 16 | Egh... Uh, Papa? |
| 0x2880fb | 30 | Ah, this feeling in my arms.\n |
| 0x28811a | 34 | It brings back so many memories... |
| 0x28813d | 45 | Papa, would you stop--Your stubble gets all\n |
| 0x28816b | 27 | scratchy when you do that-- |
| 0x288187 | 50 | I rushed over fast as I could when I heard you'd\n |
| 0x2881ba | 8 | arrived! |
| 0x2881c3 | 39 | Owie owie owie! It's getting worse...\n |
| 0x2881eb | 19 | Papa, that huuurts! |
| 0x2881ff | 43 | You must have been so lonely, out on your\n |
| 0x28822b | 43 | own! But now you're back, you can stay by\n |
| 0x288257 | 44 | my side forever and ever and ever and ever-- |
| 0x288284 | 26 | *Nuzzle, nuzzle, nuzzle*\n |
| 0x28829f | 18 | I SAID IT HUUURTS! |
| 0x2882b2 | 44 | Atuy seems to have had enough, and thwacks\n |
| 0x2882df | 42 | the man's head with the butt of her spear. |
| 0x28830a | 33 | ...The man doesn't even flinch.\n |
| 0x28832c | 30 | He just keeps beaming at Atuy. |
| 0x28834b | 35 | You're... the same as always, Papa. |
| 0x28836f | 39 | Well now! Allow me to introduce myself. |
| 0x288397 | 43 | I'm Soyankekur. As you might have figured\n |
| 0x2883c3 | 42 | out, I'm the proud father of dear little\n |
| 0x2883ee | 10 | Atuy here. |
| 0x2883f9 | 47 | Soyankekur the Mariner. After that, I'd think\n |
| 0x288429 | 45 | it was a joke, but... he does have the aura\n |
| 0x288457 | 13 | of a general. |
| 0x288465 | 47 | He's not enormous or anything, but he's lean,\n |
| 0x288495 | 45 | with a lot of muscle. Kinda like Oshtor and\n |
| 0x2884c3 | 10 | Mikazuchi. |
| 0x2884ce | 15 | And as proof... |
| 0x2884de | 47 | She's smiling, but her tail is swaying at the\n |
| 0x28850e | 44 | same time. She's being cautious... and wary. |
| 0x28853b | 47 | Now, you must be Haku. I've heard a lot about\n |
| 0x28856b | 28 | you from all Atuy's letters. |
| 0x288588 | 47 | The way I hear it, Atuy relied on you quite a\n |
| 0x2885b8 | 43 | bit while she was staying in the imperial\n |
| 0x2885e4 | 8 | capital. |
| 0x2885ed | 48 | Well, I suppose I'd better extend my gratitude\n |
| 0x28861e | 43 | in Atuy's stead, aye? Pleasure to finally\n |
| 0x28864a | 29 | make your acquaintance, Haku. |
| 0x288668 | 15 | Uh, likewise... |
| 0x288678 | 48 | I hesitantly take the offered hand as he grins\n |
| 0x2886a9 | 44 | broadly, showing off his pearly-white teeth. |
| 0x2886d6 | 44 | He doesn't seem like a bad person, just...\n |
| 0x288703 | 37 | how do I put it... A tad overbearing? |
| 0x288729 | 49 | Now I think I understand why Atuy hasn't talked\n |
| 0x28875b | 24 | about her family before. |
| 0x288774 | 42 | Now then, boy... Let's move on to a more\n |
| 0x28879f | 16 | important topic. |
| 0x2887b0 | 40 | Soyankekur continues the conversation,\n |
| 0x2887d9 | 29 | my hand still trapped in his. |
| 0x2887f7 | 44 | What, exactly, is the relationship between\n |
| 0x288824 | 16 | you and my Atuy? |
| 0x288835 | 33 | THAT'S the more important topic!? |
| 0x288857 | 47 | Oh, me and him? I suppose he's a very special\n |
| 0x288887 | 31 | person to me, aren't you, love? |
| 0x2888a7 | 50 | You know, we don't keep secrets from each other.\n |
| 0x2888da | 43 | Someone I can speak freely with. Like that! |
| 0x288906 | 46 | I guess you could say that. It's more like I\n |
| 0x288935 | 47 | listen to you vent whenever you get rejected... |
| 0x288965 | 46 | Soyankekur's smile abruptly twists, his face\n |
| 0x288994 | 34 | hardening at his daughter's words. |
| 0x2889b7 | 9 | A...Atuy? |
| 0x2889c1 | 47 | Ooh, and sometimes we meet up for drinks, and\n |
| 0x2889f1 | 37 | go at it until morning. Just nonstop! |
| 0x288a17 | 25 | ...A-ha. Go at it, eh...? |
| 0x288a31 | 31 | His grip instantly intensifies. |
| 0x288a51 | 8 | ...Haku. |
| 0x288a5a | 41 | Seems like you've been taking more care\n |
| 0x288a84 | 34 | of my daughter than I thought...\n |
| 0x288aa7 | 21 | Heh... heh heh heh... |
| 0x288abd | 45 | Um, I think there's been a misunderstanding-- |
| 0x288aeb | 5 | Yeek! |
| 0x288af1 | 47 | H-Holy crap, how is his hand that strong...!?\n |
| 0x288b21 | 41 | It's like I'm being crushed in a vise...! |
| 0x288b4b | 44 | N-No, really! By "go at it" she just means\n |
| 0x288b78 | 45 | we'd DRINK until the morning, it's not like\n |
| 0x288ba6 | 7 | we're-- |
| 0x288bae | 47 | Now that I think about it, you and Atuy do go\n |
| 0x288bde | 39 | out on your own a lot, late at night... |
| 0x288c06 | 45 | Look, the ambiguous commentary ISN'T HELPING! |
| 0x288c34 | 16 | Another servant. |
| 0x288c45 | 42 | She is a new member that also serves our\n |
| 0x288c70 | 7 | Master. |
| 0x288c78 | 18 | ...You disgust me. |
| 0x288c8b | 48 | ...I see. Let's have a little chat, you and I,\n |
| 0x288cbc | 46 | and we can talk about everything you've been\n |
| 0x288ceb | 32 | doing... in excruciating detail. |
| 0x288d0c | 47 | Look, I'm telling you, you've got it all wrong! |
| 0x288d3c | 29 | I look to Atuy for some help. |
| 0x288d5a | 5 | Hmmm? |
| 0x288d60 | 44 | ...She seems totally unaware of where this\n |
| 0x288d8d | 48 | conversation's gone, waving back with a cheery\n |
| 0x288dbe | 6 | smile. |
| 0x288dc5 | 40 | Wha--Are you--Can't you take a hint...!? |
| 0x288dee | 46 | Let's you and I take a little walk, aye, Haku? |
| 0x288e1d | 18 | ...Later that day. |
| 0x288e30 | 45 | With enough explanation and desperation, he\n |
| 0x288e5e | 44 | finally believes that we were only drinking. |
| 0x288e8b | 45 | Atuy... But WE'VE never stayed up all night\n |
| 0x288eb9 | 38 | enjoying fine drink and fine banter... |
| 0x288ee0 | 42 | ...Although I'm not sure if he's totally\n |
| 0x288f0b | 14 | convinced yet. |
| 0x288f1a | 45 | We arrive at the harbor, with Soyankekur as\n |
| 0x288f48 | 10 | our guide. |
| 0x288f53 | 47 | So? How do you like her? You're looking at my\n |
| 0x288f83 | 27 | pride and joy... my castle. |
| 0x288f9f | 48 | He brings us to a massive ship, far beyond the\n |
| 0x288fd0 | 45 | scale of any of the other boats docked there. |
| 0x288ffe | 46 | It's no metaphor. This ship is practically a\n |
| 0x28902d | 24 | castle in its own right. |
| 0x289046 | 20 | That thing's huge... |
| 0x28905b | 47 | Heh heh. A real beauty, isn't she? Aye, she's\n |
| 0x28908b | 42 | my castle, and the finest prize my liege\n |
| 0x2890b6 | 33 | could offer me... The Pororounha! |
| 0x2890d8 | 48 | She and I will see you lot all safely to Tuskur. |
| 0x289109 | 39 | Huh? Wait, you're coming with us, Papa? |
| 0x289131 | 39 | Naturally! Why wouldn't I handle this\n |
| 0x289159 | 11 | personally? |
| 0x289165 | 43 | It was a favor asked of me by Lord Oshtor\n |
| 0x289191 | 8 | himself. |
| 0x28919a | 44 | Come on, it's clear you're only doing this\n |
| 0x2891c7 | 20 | cause Atuy's here... |
| 0x2891dc | 44 | I guess it makes sense, though. Atuy's the\n |
| 0x289209 | 45 | princess of Shyahoro. It figures she'd have\n |
| 0x289237 | 8 | escorts. |
| 0x289240 | 44 | A large number of sailors rush to and fro,\n |
| 0x28926d | 47 | loading up the ship with crate after crate of\n |
| 0x28929d | 9 | supplies. |
| 0x2892a7 | 26 | We'll be departing soon... |
| 0x2892c2 | 44 | Ah, what orderly and swift movements! It's\n |
| 0x2892ef | 48 | almost refreshing to see such efficient command. |
| 0x289320 | 49 | I suppose you aren't Soyankekur the Mariner for\n |
| 0x289352 | 49 | nothing. My father praised you as a worthy rival. |
| 0x289384 | 49 | Not even Kuon can hide her awe at the expertise\n |
| 0x2893b6 | 49 | of the well-trained sailors. Her gloom seems to\n |
| 0x2893e8 | 11 | have faded. |
| 0x2893f4 | 44 | Should be ready before the sun reaches its\n |
| 0x289421 | 43 | zenith, I expect. Just a bit longer until\n |
| 0x28944d | 11 | we set out. |
| 0x289459 | 46 | We're counting on you to get us there in one\n |
| 0x289488 | 6 | piece. |
| 0x28948f | 49 | Oh, no worries, chum. You've absolutely nothing\n |
| 0x2894c1 | 23 | to worry about anymore. |
| 0x2894d9 | 40 | After all, it'll all be SMOOTH SAILING\n |
| 0x289502 | 32 | from here! Get it!? AHAHAHAHAHA! |
| 0x289523 | 45 | At his dad-joke quality pun, the men around\n |
| 0x289551 | 37 | us all laugh heartily along with him. |
| 0x289577 | 9 | ...Ugh... |
| 0x289581 | 44 | ...Anyway, looks like we're about ready to\n |
| 0x2895ae | 11 | leave port. |
| 0x2895ba | 14 | Tuskur, huh... |
| 0x2895c9 | 26 | Munechika... and Maro...\n |
| 0x2895e4 | 23 | Hope they're all right. |
| 0x2895fc | 7 | Kuon... |
| 0x289604 | 34 | All right, boys, anchors aweigh!\n |
| 0x289627 | 9 | Cast off! |
| 0x289631 | 4 | Crew |
| 0x289636 | 4 | SIR! |
| 0x28963b | 48 | A raucous response from the crew erupts as the\n |
| 0x28966c | 17 | ship is unmoored. |
| 0x28967e | 46 | All the sails raise and unfurl, and the ship\n |
| 0x2896ad | 27 | begins to drift out to sea. |
| 0x2896c9 | 26 | Our destination: Shyahoro! |
| 0x2896e4 | 47 | I climb up a short stairway from the cabin to\n |
| 0x289714 | 26 | reach the top of the deck. |
| 0x28972f | 48 | Mysterious. By my calculations, a ship of this\n |
| 0x289760 | 42 | size could never sail as smoothly as this. |
| 0x28978b | 48 | Not to mention the ship moves without a rowing\n |
| 0x2897bc | 35 | crew, or even the spells of a mage. |
| 0x2897e0 | 46 | You're right. I've traveled quite a bit now,\n |
| 0x28980f | 46 | but I've never seen a ship both this big and\n |
| 0x28983e | 5 | fast. |
| 0x289844 | 48 | It's just a thought, but perhaps the ship runs\n |
| 0x289875 | 12 | on eldcraft. |
| 0x289882 | 44 | That is... a possibility. I cannot imagine\n |
| 0x2898af | 28 | any other clear explanation. |
| 0x2898cc | 46 | Hey, Nekone. How much of those stories about\n |
| 0x2898fb | 31 | eldcraft do you think are true? |
| 0x28991b | 7 | Huh...? |
| 0x289923 | 48 | The writings of the ancients talked about such\n |
| 0x289954 | 34 | unimaginable forms of transport... |
| 0x289977 | 49 | Steedless carriages, silver serpents that carry\n |
| 0x2899a9 | 47 | people in their bellies, metallic birds, even\n |
| 0x2899d9 | 28 | ships that sail the stars... |
| 0x2899f6 | 35 | They sound so absurd, said aloud.\n |
| 0x289a1a | 48 | I was often teased as a child for believing in\n |
| 0x289a4b | 13 | such stories. |
| 0x289a59 | 49 | But the more I study it, the more I think these\n |
| 0x289a8b | 30 | can't just be fantastic tales. |
| 0x289aaa | 11 | ...I agree! |
| 0x289ab6 | 45 | The two begin to talk animatedly, comparing\n |
| 0x289ae4 | 31 | their notes on ancient legends. |
| 0x289b04 | 42 | Kuon seems to have forgotten her worries\n |
| 0x289b2f | 21 | for the time being... |
| 0x289b45 | 43 | In actuality, the imperial capital itself\n |
| 0x289b71 | 46 | holds the key. I wonder how they would react\n |
| 0x289ba0 | 15 | if they knew... |
| 0x289bb0 | 44 | Unfortunately for them, I can't bring them\n |
| 0x289bdd | 24 | any closer to the truth. |
| 0x289bf6 | 9 | *Sigh*... |
| 0x289c00 | 22 | Oh, it's not that bad. |
| 0x289c17 | 46 | I get to the starboard side to find Atuy and\n |
| 0x289c46 | 23 | Nosuri in conversation. |
| 0x289c5e | 48 | Atuy seems depressed. She leans on the railing\n |
| 0x289c8f | 47 | with both arms, resting her chin on her hands\n |
| 0x289cbf | 12 | and sighing. |
| 0x289ccc | 29 | What's up? Why the long face? |
| 0x289cea | 22 | Oh, hey there, love... |
| 0x289d01 | 45 | Well, I'm just a touch exhausted right now... |
| 0x289d2f | 42 | I'm pretty sure I know what's got her so\n |
| 0x289d5a | 10 | worn down. |
| 0x289d65 | 43 | Er, well... I think your dad's a great guy. |
| 0x289d91 | 24 | Do you really mean that? |
| 0x289daa | 47 | I think so as well. He seems like a wonderful\n |
| 0x289dda | 14 | father figure. |
| 0x289de9 | 43 | I see... Well... it's not like I hate him\n |
| 0x289e15 | 12 | or anything. |
| 0x289e22 | 45 | I mean, when it comes down to it, I do like\n |
| 0x289e50 | 49 | He's strong, and reliable, and I do admire him... |
| 0x289e82 | 49 | But... that's exactly why I wish he'd act a bit\n |
| 0x289eb4 | 12 | more proper. |
| 0x289ec1 | 49 | I guess she feels conflicted about how he melts\n |
| 0x289ef3 | 25 | into a puddle around her. |
| 0x289f0d | 46 | Now that I think about it, all the crew here\n |
| 0x289f3c | 47 | wear such fashionable clothes, including your\n |
| 0x289f6c | 7 | father. |
| 0x289f74 | 43 | I was expecting something more... ragged.\n |
| 0x289fa0 | 20 | Practical, you know? |
| 0x289fb5 | 46 | Hee hee, you think so? That was actually all\n |
| 0x289fe4 | 8 | my idea. |
| 0x289fed | 46 | A while back, they'd all wear these dreadful\n |
| 0x28a01c | 22 | musky-looking clothes. |
| 0x28a033 | 48 | They'd walk around town in their undies, never\n |
| 0x28a064 | 49 | wash, use such vulgar language--I couldn't have\n |
| 0x28a096 | 3 | it! |
| 0x28a09a | 47 | Hm. I suppose that isn't acceptable behavior.\n |
| 0x28a0ca | 40 | A good man must present themselves well! |
| 0x28a0f3 | 51 | You think so? Aren't all sailors kinda like that?\n |
| 0x28a127 | 42 | That's closer to my mental image of one... |
| 0x28a152 | 42 | No, no, no, no, no! I won't accept that.\n |
| 0x28a17d | 41 | Everything's different now. We don't go\n |
| 0x28a1a7 | 22 | raiding and pillaging! |
| 0x28a1be | 43 | The Mikado needs us to preserve order and\n |
| 0x28a1ea | 43 | oversee trade. We can't have men trotting\n |
| 0x28a216 | 17 | around in undies. |
| 0x28a228 | 46 | I'd rather run away from home than have some\n |
| 0x28a257 | 47 | poor dear think that was the official uniform\n |
| 0x28a287 | 14 | of Shyahoro... |
| 0x28a296 | 45 | Uh, didn't you already run away from home...? |
| 0x28a2c4 | 46 | I guess I can understand where you're coming\n |
| 0x28a2f3 | 5 | from. |
| 0x28a2f9 | 47 | So since I decided all this was unacceptable,\n |
| 0x28a329 | 22 | I came up with a plan. |
| 0x28a340 | 40 | All I had to do was make everyone look\n |
| 0x28a369 | 12 | fashionable! |
| 0x28a376 | 45 | From that point on, I made sure the sailors\n |
| 0x28a3a4 | 43 | tidied up, wore nice clothing, and talked\n |
| 0x28a3d0 | 9 | properly. |
| 0x28a3da | 47 | It was no easy thing! I tried to make them so\n |
| 0x28a40a | 44 | fashionable--I picked out the most popular\n |
| 0x28a437 | 21 | suits I could find... |
| 0x28a44d | 43 | But you have to start somewhere, don't you? |
| 0x28a479 | 43 | Atuy pulls out what looks like a block of\n |
| 0x28a4a5 | 24 | prints as she says this. |
| 0x28a4be | 47 | All of them feature colorful drawings of thin\n |
| 0x28a4ee | 41 | and handsome men wearing flashy clothing. |
| 0x28a518 | 47 | "The hottest new menswear that's all the rage\n |
| 0x28a548 | 25 | in the imperial capital!" |
| 0x28a562 | 47 | "All the girls' eyes are on me thanks to this\n |
| 0x28a592 | 17 | one weird trick!" |
| 0x28a5a4 | 46 | "Mononofu's Warehouse. You're gonna love the\n |
| 0x28a5d3 | 31 | way you look--we guarantee it." |
| 0x28a5f3 | 27 | Hm, those look pretty good. |
| 0x28a60f | 42 | You think so? That's what I thought too... |
| 0x28a63a | 46 | ...at the time, anyway. I don't know where I\n |
| 0x28a669 | 11 | went wrong. |
| 0x28a675 | 48 | In reality, it looked so different from what I\n |
| 0x28a6a6 | 15 | had imagined... |
| 0x28a6b6 | 40 | Really? I don't think it looks THAT bad. |
| 0x28a6df | 36 | Well, it's kind of understandable... |
| 0x28a704 | 48 | The drawings are all of slim and tall handsome\n |
| 0x28a735 | 19 | men with long legs. |
| 0x28a749 | 41 | But the sailors are all barrel-chested,\n |
| 0x28a773 | 44 | musclebound lugs with legs like tree trunks. |
| 0x28a7a0 | 45 | Clothes or not, they'll never look anything\n |
| 0x28a7ce | 32 | like the guys in these drawings. |
| 0x28a7ef | 46 | *Sigh*... I suppose it's best to leave these\n |
| 0x28a81e | 32 | to the boys who can pull it off. |
| 0x28a83f | 47 | I head over to the port side to find Rulutieh\n |
| 0x28a86f | 46 | watching the shore, standing near the railing. |
| 0x28a89e | 47 | I see a number of seagulls circling Rulutieh,\n |
| 0x28a8ce | 46 | as though they're having a conversation with\n |
| 0x28a8fd | 4 | her. |
| 0x28a902 | 47 | I guess animals really do tend to flock to her. |
| 0x28a932 | 9 | Rulutieh. |
| 0x28a93c | 15 | Oh, Sir Haku... |
| 0x28a94c | 25 | What were you looking at? |
| 0x28a966 | 38 | I saw a... very big fish over there... |
| 0x28a98d | 47 | I follow Rulutieh's pointed finger to a large\n |
| 0x28a9bd | 44 | school of fish, swimming alongside the ship. |
| 0x28a9ea | 5 | Oh... |
| 0x28a9f0 | 45 | Their silver scales glitter serenely as the\n |
| 0x28aa1e | 24 | light plays off of them. |
| 0x28aa37 | 43 | I can't help but stare in awe at the sight. |
| 0x28aa63 | 23 | It's so... beautiful... |
| 0x28aa7b | 38 | Yeah, when you see them like this...\n |
| 0x28aaa2 | 13 | It really is. |
| 0x28aab0 | 48 | I've only ever seen dried fish... I never knew\n |
| 0x28aae1 | 38 | how large and beautiful they could be. |
| 0x28ab08 | 49 | I dunno if I've ever seen dried fish that could\n |
| 0x28ab3a | 46 | be beautiful--Ah, better not spoil the moment. |
| 0x28ab69 | 29 | Oh... Sir Haku, look at that! |
| 0x28ab87 | 43 | Again I look, and this time I see a large\n |
| 0x28abb3 | 36 | creature jump up from the waters--\n |
| 0x28abd8 | 25 | big enough to ride, even. |
| 0x28abf2 | 13 | Eee! Eeeee!\n |
| 0x28ac00 | 28 | *click, click, click, click* |
| 0x28ac1d | 42 | They almost seem to be chirping happily,\n |
| 0x28ac48 | 36 | waving their fins as if in greeting. |
| 0x28ac6d | 23 | Oh, they're adorable... |
| 0x28ac85 | 48 | They spin around each other, as if giving us a\n |
| 0x28acb6 | 46 | show, occasionally spouting little bursts of\n |
| 0x28ace5 | 24 | They sure seem friendly. |
| 0x28acfe | 40 | Hee... Maybe they're saying hello to us. |
| 0x28ad27 | 48 | That's exactly right. They're glad to see you,\n |
| 0x28ad58 | 6 | Rulie! |
| 0x28ad5f | 34 | Looks like Atuy's come to join us. |
| 0x28ad82 | 46 | Tantans are awfully clever. They came to say\n |
| 0x28adb1 | 43 | hello, since they've never seen you before. |
| 0x28addd | 37 | Hee hee... that's so sweet of them... |
| 0x28ae03 | 44 | Rulutieh seems unable to take her eyes off\n |
| 0x28ae30 | 21 | the friendly tantans. |
| 0x28ae46 | 27 | Plus, they taste delicious! |
| 0x28ae62 | 6 | ...Um? |
| 0x28ae69 | 30 | Rulutieh's smile turns glassy. |
| 0x28ae88 | 48 | Ooh, they're great in a fry-up. Smoking them's\n |
| 0x28aeb9 | 47 | good too. Just a bite, and you'll be in utter\n |
| 0x28aee9 | 6 | bliss. |
| 0x28aef0 | 10 | Uh... huh? |
| 0x28aefb | 34 | Um... You're... going to eat them? |
| 0x28af1e | 4 | Yup. |
| 0x28af23 | 11 | These ones. |
| 0x28af2f | 38 | It's... erm... "mutual coexistence"?\n |
| 0x28af56 | 47 | They tend to help us on fishing trips, and we\n |
| 0x28af86 | 18 | share our catches. |
| 0x28af99 | 17 | B-But then, why-- |
| 0x28afab | 51 | Sometimes their numbers get a bit out of control.\n |
| 0x28afdf | 42 | That's when we have to draw the line, see. |
| 0x28b00a | 45 | Otherwise they'd eat all the fish right up,\n |
| 0x28b038 | 42 | and there'd be nothing left for us people. |
| 0x28b063 | 14 | Eeeee, eeee!\n |
| 0x28b072 | 22 | *click, click, click*  |
| 0x28b089 | 49 | Hee hee, you guys are so cute... I promise I'll\n |
| 0x28b0bb | 34 | eat you myself to show my respect. |
| 0x28b0de | 45 | When the time comes, I'll make some for you\n |
| 0x28b10c | 11 | too, Rulie! |
| 0x28b118 | 42 | Atuy leaves us with this cheery thought,\n |
| 0x28b143 | 28 | waving goodbye with a smile. |
| 0x28b160 | 8 | ...OK... |
| 0x28b169 | 43 | Rulutieh's expression is pale and distant\n |
| 0x28b195 | 43 | as she contemplates the cruelties of this\n |
| 0x28b1c1 | 6 | world. |
| 0x28b1c8 | 41 | ...I guess she can't reject it outright\n |
| 0x28b1f2 | 42 | because she understands about coexisting\n |
| 0x28b21d | 14 | with nature... |
| 0x28b22c | 47 | ...I don't know if there's anything I can say\n |
| 0x28b25c | 24 | to make her feel better. |
| 0x28b275 | 49 | None of us even get off the boat when we arrive\n |
| 0x28b2a7 | 12 | at Shyahoro. |
| 0x28b2b4 | 44 | The crew quickly gets the ship resupplied,\n |
| 0x28b2e1 | 42 | and soon we're back on the path to Tuskur. |
| 0x28b30c | 45 | I head for the stern of the boat, hearing a\n |
| 0x28b33a | 34 | quiet singing from that direction. |
| 0x28b35d | 31 | That's a really pretty voice... |
| 0x28b37d | 50 | Who could it be? I'm pretty sure I only remember\n |
| 0x28b3b0 | 31 | seeing burly guys on this ship. |
| 0x28b3d0 | 48 | I look over to find Uruuru and Saraana sitting\n |
| 0x28b401 | 48 | at the ship's edge, legs dangling over the side. |
| 0x28b432 | 25 | Oh. Uruuru and Saraana... |
| 0x28b44c | 45 | I lean back against the cabin and listen to\n |
| 0x28b47a | 23 | their song for a while. |
| 0x28b492 | 49 | A gentle song, with the waves as accompaniment.\n |
| 0x28b4c4 | 43 | It's quiet and soft, and somehow nostalgic. |
| 0x28b4f0 | 47 | I initially only listen out of curiosity, but\n |
| 0x28b520 | 40 | after a while, I'm completely entranced. |
| 0x28b549 | 46 | When you look at the both of them like this... |
| 0x28b578 | 39 | They have an ethereal beauty to them.\n |
| 0x28b5a0 | 39 | Like a pair of perfectly crafted dolls. |
| 0x28b5c8 | 47 | As I think to myself, the two of them seem to\n |
| 0x28b5f8 | 25 | notice me standing there. |
| 0x28b612 | 31 | Is there something you require? |
| 0x28b632 | 50 | Oh, sorry. Didn't mean to disturb you. Go ahead,\n |
| 0x28b665 | 41 | just pretend I'm not here or something... |
| 0x28b68f | 30 | More important to be with you. |
| 0x28b6ae | 48 | It is much more important for us to be at your\n |
| 0x28b6df | 13 | side, Master. |
| 0x28b6ed | 10 | That so... |
| 0x28b6f8 | 25 | Master, please come here. |
| 0x28b712 | 50 | ...I have no idea how, but they suddenly produce\n |
| 0x28b745 | 27 | a cushion for me to sit on. |
| 0x28b761 | 11 | Oh, thanks. |
| 0x28b76d | 33 | We shall ready a bed immediately. |
| 0x28b78f | 7 | ...Huh? |
| 0x28b797 | 33 | Blue waters. Blue sky. Passion.\n |
| 0x28b7b9 | 19 | Recipe for romance. |
| 0x28b7cd | 46 | We will be bonded together in the vast ocean\n |
| 0x28b7fc | 44 | under the blue sky. This is our destiny...\n |
| 0x28b829 | 9 | our fate. |
| 0x28b833 | 50 | You guys get more and more aggressive about this\n |
| 0x28b866 | 23 | every time, don't you!? |
| 0x28b87e | 48 | And they're just the same old twins as always.\n |
| 0x28b8af | 7 | Geez... |
| 0x28b8b7 | 24 | ...Hey, about that song. |
| 0x28b8d0 | 10 | A lullaby. |
| 0x28b8db | 44 | It is a lullaby that our mother sang to us\n |
| 0x28b908 | 19 | when we were young. |
| 0x28b91c | 9 | ...I see. |
| 0x28b926 | 49 | Hey, Uruuru, Saraana. Would... you mind singing\n |
| 0x28b958 | 19 | me that song again? |
| 0x28b96c | 15 | ...As you wish. |
| 0x28b97c | 48 | It feels like a song I know... from long, long\n |
| 0x28b9ad | 4 | ago. |
| 0x28b9b2 | 49 | I relax, letting the song take over my thoughts\n |
| 0x28b9e4 | 31 | as I rest at the ship's edge... |
| 0x28ba04 | 45 | All the emotions that have been flooding my\n |
| 0x28ba32 | 32 | mind slowly calm, and fade away. |
| 0x28ba53 | 44 | My mind is filled with peace, and--if only\n |
| 0x28ba80 | 45 | for a little while--I let myself forget the\n |
| 0x28baae | 22 | hardships ahead of us. |
| 0x28d0d4 | 48 | Honoka calls out to a court lady walking alone\n |
| 0x28d105 | 17 | down the hallway. |
| 0x28d117 | 32 | Entua, what impeccable timing.\n |
| 0x28d138 | 37 | Could I ask your help with something? |
| 0x28d15e | 42 | Yes, Lady Honoka. I would be glad to help. |
| 0x28d189 | 46 | Entua gives a respectful bow as Honoka holds\n |
| 0x28d1b8 | 41 | out a small bowl full of assorted sweets. |
| 0x28d1e2 | 44 | Would you try tasting one of these for me,\n |
| 0x28d20f | 5 | then? |
| 0x28d215 | 13 | What is this? |
| 0x28d223 | 25 | Let the taste inform you. |
| 0x28d23d | 49 | Spurred on by Honoka's mischievous smile, Entua\n |
| 0x28d26f | 49 | carefully plucks one of the sweets from the bowl. |
| 0x28d2a1 | 27 | If you do not mind, then... |
| 0x28d2bd | 46 | She takes a small bite, a serious expression\n |
| 0x28d2ec | 43 | on her face... and it shifts to a look of\n |
| 0x28d318 | 8 | delight. |
| 0x28d321 | 17 | ...How delicious! |
| 0x28d333 | 21 | I am glad to hear it. |
| 0x28d349 | 47 | Yes... The outer shell is crisp and fragrant,\n |
| 0x28d379 | 47 | but the inside is soft and sweet. It melts in\n |
| 0x28d3a9 | 12 | the mouth... |
| 0x28d3b6 | 47 | I do not think I have ever eaten a treat such\n |
| 0x28d3e6 | 15 | as this before. |
| 0x28d3f6 | 49 | It relieves me to hear that this is even enough\n |
| 0x28d428 | 28 | to satisfy foreign tastes... |
| 0x28d445 | 47 | A brief shudder runs through Entua at the use\n |
| 0x28d475 | 23 | of the word "foreign."  |
| 0x28d48d | 44 | Her gaze falls to the sweet in her hand, a\n |
| 0x28d4ba | 48 | single bite missing, and a tear glimmers as it\n |
| 0x28d4eb | 6 | falls. |
| 0x28d4f2 | 31 | Is something the matter, Entua? |
| 0x28d512 | 14 | Lady Honoka... |
| 0x28d521 | 50 | You have been truly kind to me. I... do not have\n |
| 0x28d554 | 46 | the words to express how grateful I am to you. |
| 0x28d583 | 46 | I have done nothing to deserve such gratitude. |
| 0x28d5b2 | 26 | That is simply not true... |
| 0x28d5cd | 45 | I took up arms against your land just as my\n |
| 0x28d5fb | 42 | father did. I would expect only death as\n |
| 0x28d626 | 11 | punishment. |
| 0x28d632 | 36 | Leave him be. I forbid you to seek\n |
| 0x28d657 | 12 | vengeance... |
| 0x28d664 | 9 | ...Wh--!? |
| 0x28d66e | 47 | Hah... Now that I recall, you enjoyed weaving\n |
| 0x28d69e | 44 | and cooking much more than warfare, didn't\n |
| 0x28d6cb | 7 | you...? |
| 0x28d6d3 | 46 | That's right... You... never belonged on the\n |
| 0x28d702 | 14 | battlefield... |
| 0x28d711 | 17 | That is not true! |
| 0x28d723 | 45 | I am your daughter! The daughter of a brave\n |
| 0x28d751 | 18 | Uzurushan warrior! |
| 0x28d764 | 17 | That is enough... |
| 0x28d776 | 45 | You may live your life as your own woman...\n |
| 0x28d7a4 | 30 | and find your own happiness... |
| 0x28d7c3 | 9 | Father... |
| 0x28d7cd | 47 | Haha... I suppose my only regret... is that I\n |
| 0x28d7fd | 39 | will never see you in your... bridal... |
| 0x28d825 | 7 | Father? |
| 0x28d82d | 48 | ...F-Father...? No... This can't be happening.\n |
| 0x28d85e | 37 | Father, please... Don't leave me...\n |
| 0x28d884 | 17 | Father... Father! |
| 0x28d896 | 48 | ...My father's dying wish was for me to "leave\n |
| 0x28d8c7 | 41 | the battlefield behind, and find my own\n |
| 0x28d8f1 | 11 | happiness." |
| 0x28d8fd | 47 | I took those words to heart, and traveled the\n |
| 0x28d92d | 44 | barren lands for days until I reached this\n |
| 0x28d95a | 8 | country. |
| 0x28d963 | 49 | Perhaps I wished to see what lay ahead of us...\n |
| 0x28d995 | 38 | had we been able to finish our battle. |
| 0x28d9bc | 46 | And in the country I once hated as an enemy,\n |
| 0x28d9eb | 43 | I found people living just as I did in my\n |
| 0x28da17 | 9 | homeland. |
| 0x28da21 | 50 | Weaving clothes, earning enough to eat each day,\n |
| 0x28da54 | 44 | raising children... It was a very peaceful\n |
| 0x28da81 | 10 | lifestyle. |
| 0x28da8c | 46 | I even saw mothers and children who had lost\n |
| 0x28dabb | 32 | husbands and fathers to the war. |
| 0x28dadc | 45 | I was... at a loss. The happiness my father\n |
| 0x28db0a | 47 | wished for me was to live an ordinary life...\n |
| 0x28db3a | 6 | but... |
| 0x28db41 | 50 | ...How can I allow myself that after fighting in\n |
| 0x28db74 | 49 | the war that claimed so many lives? How could I\n |
| 0x28dba6 | 10 | face them? |
| 0x28dbb5 | 51 | And it was then that you found me, Lady Honoka...\n |
| 0x28dbe9 | 23 | paralyzed by the sight. |
| 0x28dc01 | 46 | I do remember. I had thought only to venture\n |
| 0x28dc30 | 29 | into the city for a change... |
| 0x28dc4e | 49 | I saw you crouched at the side of the street...\n |
| 0x28dc80 | 48 | like a wild young beast that had lost its very\n |
| 0x28dcb1 | 5 | soul. |
| 0x28dcb7 | 6 | Yes... |
| 0x28dcbe | 49 | Not only did you take me back with you, you did\n |
| 0x28dcf0 | 45 | not judge me when I revealed my heritage to\n |
| 0x28dd1e | 6 | you... |
| 0x28dd25 | 43 | Instead, you allowed me to work here as a\n |
| 0x28dd51 | 31 | full-fledged court attendant... |
| 0x28dd71 | 48 | I merely saw the potential within you. And was\n |
| 0x28dda2 | 46 | I not correct? You are helping me as we speak. |
| 0x28ddd1 | 46 | As Entua stiffens in humility, Honoka gently\n |
| 0x28de00 | 34 | rests her hand on the girl's head. |
| 0x28de23 | 43 | I was wrong to have spoken so carelessly.\n |
| 0x28de4f | 44 | I am sorry to have disturbed such terrible\n |
| 0x28de7c | 11 | memories... |
| 0x28de88 | 47 | P-Please, don't be! That is... such words are\n |
| 0x28deb8 | 15 | wasted on me... |
| 0x28dec8 | 47 | Well then, allow me at least to apologize for\n |
| 0x28def8 | 36 | always asking such odd tasks of you. |
| 0x28df1d | 43 | For you, Lady Honoka, I would fulfill any\n |
| 0x28df49 | 41 | request, even at the cost of my own life. |
| 0x28df73 | 46 | ...If that is the case, I would ask one more\n |
| 0x28dfa2 | 13 | thing of you. |
| 0x28dfb0 | 47 | Please, do not hesitate. Ask whatever you wish. |
| 0x28dfe0 | 43 | Honoka can't help but smile at the girl's\n |
| 0x28e00c | 32 | earnest, forthright personality. |
| 0x28e02d | 46 | I would like you to take these sweets to the\n |
| 0x28e05c | 44 | young--Pardon, to Lord Woshis. If you would. |
| 0x28e089 | 46 | Please also deliver this message: "I am sure\n |
| 0x28e0b8 | 47 | you are very busy, but please do not overwork\n |
| 0x28e0e8 | 10 | yourself." |
| 0x28e0f3 | 11 | Understood. |
| 0x28e0ff | 48 | Entua takes another deep bow, then accepts the\n |
| 0x28e130 | 15 | bowl of sweets. |
| 0x28e140 | 10 | Who is it? |
| 0x28e14b | 44 | Woshis raises his head from his paperwork,\n |
| 0x28e178 | 28 | sensing someone at his door. |
| 0x28e195 | 44 | I have come to deliver a message from Lady\n |
| 0x28e1c2 | 7 | Honoka. |
| 0x28e1ca | 16 | Please, come in. |
| 0x28e1db | 12 | Your pardon. |
| 0x28e1e8 | 18 | Ah, so it was you. |
| 0x28e1fb | 50 | Woshis recognizes the girl that enters his room,\n |
| 0x28e22e | 27 | giving her a cordial smile. |
| 0x28e24a | 41 | It seems you are quite the hard worker.\n |
| 0x28e274 | 45 | Lady Honoka must be proud... After all, she\n |
| 0x28e2a2 | 32 | was the one who recommended you. |
| 0x28e2c3 | 46 | I thank you, but I am afraid I am not worthy\n |
| 0x28e2f2 | 17 | of such praise... |
| 0x28e304 | 28 | Oh? And what could these be? |
| 0x28e321 | 50 | I have been told by Lady Honoka to deliver these\n |
| 0x28e354 | 27 | sweets to you, Lord Woshis. |
| 0x28e370 | 16 | I see... sweets. |
| 0x28e381 | 43 | Yes. They are very fine quality, and most\n |
| 0x28e3ad | 11 | palatable-- |
| 0x28e3b9 | 47 | Entua notices that she's smiling, and hastily\n |
| 0x28e3e9 | 17 | covers her mouth. |
| 0x28e3fb | 16 | ...My apologies. |
| 0x28e40c | 46 | I am afraid I am currently quite busy. Would\n |
| 0x28e43b | 43 | you mind setting them there for the moment? |
| 0x28e467 | 47 | Entua places the bowl at the indicated corner\n |
| 0x28e497 | 12 | of his desk. |
| 0x28e4a4 | 34 | And this message from Lady Honoka? |
| 0x28e4c7 | 49 | She wished me to tell you... "I am sure you are\n |
| 0x28e4f9 | 48 | very busy, but please do not overwork yourself." |
| 0x28e52a | 13 | Well, well... |
| 0x28e538 | 40 | Please convey my reply to Lady Honoka:\n |
| 0x28e561 | 29 | "Thank you for your concern." |
| 0x28e57f | 24 | I will be sure to do so. |
| 0x28e598 | 44 | Entua gives a deep bow and turns to leave,\n |
| 0x28e5c5 | 28 | but Woshis calls out to her. |
| 0x28e5e2 | 43 | Ah, that reminds me... There is something\n |
| 0x28e60e | 23 | I should inform you of. |
| 0x28e626 | 19 | ...Yes? What is it? |
| 0x28e63a | 42 | There is yet to be an official decision... |
| 0x28e665 | 50 | But you should know you are being considered for\n |
| 0x28e698 | 41 | the position of the imperial princess's\n |
| 0x28e6c2 | 10 | caretaker. |
| 0x28e6cd | 27 | The imperial princess's...? |
| 0x28e6e9 | 47 | Lady Munechika currently serves as governess,\n |
| 0x28e719 | 44 | but war divides her duties. It behooves us\n |
| 0x28e746 | 20 | to train others, hm? |
| 0x28e75b | 46 | But... It may be unwise to appoint one of my\n |
| 0x28e78a | 39 | background to be so near the princess-- |
| 0x28e7b2 | 49 | Background...? I'm afraid I cannot imagine what\n |
| 0x28e7e4 | 21 | you are referring to. |
| 0x28e7fa | 45 | Woshis tilts his head in polite puzzlement.\n |
| 0x28e828 | 44 | Entua can only bow deeply again in response. |
| 0x28e855 | 48 | None can deny the work you've done. And it may\n |
| 0x28e886 | 48 | serve our eventual ruler to be exposed to many\n |
| 0x28e8b7 | 13 | perspectives. |
| 0x28e8c5 | 20 | ...Do you not agree? |
| 0x28e8da | 46 | I... would not wish to cause trouble for you\n |
| 0x28e909 | 15 | or Lady Honoka. |
| 0x28e919 | 47 | Only Lady Honoka and I know of your ancestry.\n |
| 0x28e949 | 45 | Whatever you are imagining will not come to\n |
| 0x28e977 | 5 | pass. |
| 0x28e97d | 48 | Regardless, I certainly wouldn't want to force\n |
| 0x28e9ae | 40 | you into the position. But what say you? |
| 0x28e9d7 | 40 | Entua is still for a moment, in silent\n |
| 0x28ea00 | 46 | contemplation, then bows low and speaks with\n |
| 0x28ea2f | 15 | solemn gravity. |
| 0x28ea3f | 49 | If you truly believe me fit for such a station,\n |
| 0x28ea71 | 22 | I would gladly accept. |
| 0x28ea88 | 50 | ...Good. That handily solves one of the problems\n |
| 0x28eabb | 33 | recently plaguing me, I must say. |
| 0x28eadd | 47 | You should have more information in due time.\n |
| 0x28eb0d | 48 | Until then, I expect you to continue your hard\n |
| 0x28eb3e | 5 | work. |
| 0x28eb44 | 34 | I have high hopes for you, indeed. |
| 0x28eb67 | 47 | Woshis gives one last smile, then returns his\n |
| 0x28eb97 | 42 | gaze to the field of paperwork before him. |
| 0x28ebc2 | 14 | By your leave. |
| 0x28ebd1 | 46 | Woshis sits there in silence, staring at the\n |
| 0x28ec00 | 47 | bowl of sweets resting on the side of his desk. |
| 0x28ec30 | 48 | ...Please dispose of this. I am not especially\n |
| 0x28ec61 | 15 | fond of sweets. |
| 0x28ec71 | 47 | There is a hint of regret in his voice, as he\n |
| 0x28eca1 | 48 | speaks to one of the Yatanawarabe shadowing him. |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_07.json` com a forma:
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
