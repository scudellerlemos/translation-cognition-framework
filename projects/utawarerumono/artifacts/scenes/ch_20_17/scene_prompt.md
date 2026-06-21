# Cena ch_20_17 — pacote de traducao (174 linhas)

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
| Akuruturuka | Termo | Akuruturuka | manter_original | major |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Nugwisomkami | Termo | Nugwisomkami | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Yamatan | Etnia | de Yamato | traduzir | none |

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
- **Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)**: Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo" (bicho mole) com **duplo-sentido proposital**. **Decisões de tradução não-óbvias:** - **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2

## 5b. CONTROLE DE SPOILER — fatos AINDA NAO revelados nesta cena
> Estes fatos so se revelam DEPOIS desta cena. Preserve a ambiguidade do original; a
> traducao NAO pode antecipa-los (cuidado especial com genero/identidade/relacao em pt-BR).
- **Raiko** (major): Trate Raiko apenas como um dos Oito Generais-Pilar ('o Sabio'), frio e calculista, recem-apresentado. NAO antecipe vinculo familiar com outros personagens nem seu papel/acoes futuras. Sem foreshadowing.
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Uzurushan soldier` -> `soldado Uzurushan` ([SYSTEM], 20_04)
- `Uzurushan commander` -> `comandante Uzurushan` (SISTEMA, 20_05)
- `Gah!` -> `Ai!` (Man, 11_01)
- `Wh-What's going on?` -> `Quê-O que está acontecendo?` (Homem, 17_01)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `a trap.` -> `uma cilada.` (Ougi, 19_02)
- `Hm.` -> `Hm.` (Ukon, 12_12)
- `cornered.` -> `encurralados.` (Nosuri, 19_02)
- `Hm?` -> `Hum?` (Kuon, 11_02)
- `Hmph...` -> `Hmph...` (Nekone, 16_02)
- `ch400_00_base` -> `ch400_00_base` (SYSTEM, 20_11)
- `ch400_00_wheel` -> `ch400_00_wheel` (SYSTEM, 20_11)
- `target` -> `target` (SYSTEM, 20_11)
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
| 0x206452 | 17 | Uzurushan soldier |
| 0x206464 | 16 | Raaaaaaaaaaaaah! |
| 0x206475 | 13 | Ghaaaaaaahhk! |
| 0x206483 | 12 | Ah... AAAGH! |
| 0x206490 | 19 | Uzurushan commander |
| 0x2064a4 | 33 | N-Nngh... We can't get close...\n |
| 0x2064c6 | 36 | The arrows just keep raining down... |
| 0x2064eb | 40 | They seem to have two rows of archers,\n |
| 0x206514 | 17 | alternating fire. |
| 0x206526 | 46 | And even if we pass the barrage, the path is\n |
| 0x206555 | 43 | blocked by stakes and spearmen. We cannot\n |
| 0x206581 | 12 | charge up... |
| 0x20658e | 50 | Damn it! We cannot reach their camp...! Cowards!\n |
| 0x2065c1 | 46 | Come down and fight! How long will they hide!? |
| 0x2065f0 | 30 | Or are they... They must be!\n |
| 0x20660f | 45 | They're thinning our numbers in preparation\n |
| 0x20663d | 19 | for a grand charge! |
| 0x206651 | 21 | Damn. At this rate... |
| 0x206667 | 7 | Adviser |
| 0x20666f | 50 | The Yamatan army has begun their counterassault.\n |
| 0x2066a2 | 42 | Our frontline is slowly being pushed back. |
| 0x2066cd | 44 | Impossible... We had them in shambles mere\n |
| 0x2066fa | 46 | moments ago. How did they turn the tables so\n |
| 0x206729 | 11 | quickly...? |
| 0x206735 | 48 | Khukakakaka! So, they DO know more than idling\n |
| 0x206766 | 49 | in their golden city. They resist us with these\n |
| 0x206798 | 9 | tricks... |
| 0x2067a2 | 35 | Hmph. So this is the Akuruturuka... |
| 0x2067c6 | 51 | You amuse me, Mikado. Creating a nation protected\n |
| 0x2067fa | 32 | by abominations such as these... |
| 0x20681b | 46 | But wars are not decided on the might of one\n |
| 0x20684a | 14 | soldier alone. |
| 0x206859 | 46 | Main force, advance! Our numbers will finish\n |
| 0x206888 | 45 | this. This ends on the plains! Their tricks\n |
| 0x2068b6 | 12 | are useless! |
| 0x2068c3 | 35 | Let our roars resound in the air!\n |
| 0x2068e7 | 16 | Sound the gongs! |
| 0x2068f8 | 37 | Surround all soldiers with shields!\n |
| 0x20691e | 46 | Our numbers shall crush them! Our iron wills\n |
| 0x20694d | 26 | shall dispel their tricks! |
| 0x206968 | 49 | That damned old prune... You shall know what it\n |
| 0x20699a | 42 | means to challenge Gundhurua, soon enough. |
| 0x2069c5 | 46 | Hyahahahaha! Look at those Yamatan soldiers,\n |
| 0x2069f4 | 47 | so full of themselves! They will crumble once\n |
| 0x206a24 | 10 | we charge! |
| 0x206a2f | 45 | Brave of you to show yourselves, but do you\n |
| 0x206a5d | 42 | truly think you stand a chance against a\n |
| 0x206a88 | 17 | frontal assault!? |
| 0x206a9a | 44 | Hyahahahahaha! Pathetic! Utterly pathetic!\n |
| 0x206ac7 | 49 | Besides the Nugwisomkami, there's nothing to be\n |
| 0x206af9 | 10 | afraid of! |
| 0x206b04 | 22 | Forward! Forwaaaaaard! |
| 0x206b1b | 45 | They didn't even put up a fight before they\n |
| 0x206b49 | 17 | fled! After them! |
| 0x206b5b | 33 | We'll finish them in one fell--\n |
| 0x206b7d | 20 | What!? What is this? |
| 0x206b92 | 43 | A smokescreen...? Damned Yamatan cowards!\n |
| 0x206bbe | 39 | They're trying to escape in this smoke! |
| 0x206be6 | 47 | Don't let their tricks confuse you! The enemy\n |
| 0x206c16 | 37 | is still right before us! Chaaaaarge! |
| 0x206c3c | 4 | Gah! |
| 0x206c41 | 27 | What!? Was this... a trap!? |
| 0x206c5d | 46 | Damn it! What happened to the unit in front?\n |
| 0x206c8c | 20 | I can't see a thing! |
| 0x206ca1 | 19 | Wh-What's going on? |
| 0x206cb5 | 34 | Th-They're coming! They're coming! |
| 0x206cd8 | 7 | Huh...? |
| 0x206ce0 | 17 | RAAAAAAAAAAAAAAH! |
| 0x206cf5 | 7 | Ghaaah! |
| 0x206cfd | 51 | Our pursuing unit was scattered by a smokescreen.\n |
| 0x206d31 | 48 | Yamatan archers then fired on them in the chaos. |
| 0x206d62 | 47 | They attempted retreat, but they were blocked\n |
| 0x206d92 | 48 | by the unaware units behind them, causing more\n |
| 0x206dc3 | 10 | confusion. |
| 0x206dce | 46 | They were then charged by the enemy cavalry,\n |
| 0x206dfd | 17 | and... wiped out. |
| 0x206e0f | 45 | This must have been their plan. The Yamatan\n |
| 0x206e3d | 46 | soldiers fled only to lead our soldiers into\n |
| 0x206e6c | 7 | a trap. |
| 0x206e74 | 48 | A daring plan. If they had missed their timing\n |
| 0x206ea5 | 45 | by even a second, we would have overrun them. |
| 0x206ed3 | 48 | Yes. Without precise coordination, such a plan\n |
| 0x206f04 | 46 | would be impossible. How did they accomplish\n |
| 0x206f33 | 6 | it...? |
| 0x206f3a | 10 | Rrrrrgh... |
| 0x206f45 | 3 | Hm. |
| 0x206f49 | 45 | Raiko's sharp eyes survey a map spread on a\n |
| 0x206f77 | 45 | massive desk adorned in beautiful engravings. |
| 0x206fa5 | 44 | Those behind Raiko constantly give him new\n |
| 0x206fd2 | 46 | reports, as though witness to every movement\n |
| 0x207001 | 12 | of the army. |
| 0x20700e | 46 | The enemy's main force will soon be in range\n |
| 0x20703d | 25 | of our perierai's arrows! |
| 0x207057 | 47 | All progressing as intended. Spread the units\n |
| 0x207087 | 36 | on the side of the enemy as planned. |
| 0x2070ac | 49 | Proceed as planned! Perierai, move to flank the\n |
| 0x2070de | 43 | enemy! Coordinates: the hill at 4234, 4541! |
| 0x20710a | 41 | Our third unit seems to be taking heavy\n |
| 0x207134 | 44 | casualties. Call them back and advance the\n |
| 0x207161 | 12 | fourth unit. |
| 0x20716e | 49 | Those around the table quickly move translucent\n |
| 0x2071a0 | 44 | gamepieces across the map according to his\n |
| 0x2071cd | 7 | orders. |
| 0x2071d5 | 48 | Hmph, is this really all...? I suppose an owlo\n |
| 0x207206 | 48 | of barbarians is still only a barbarian himself. |
| 0x207237 | 49 | Lord Raiko, it would be unwise to underestimate\n |
| 0x207269 | 43 | the enemy. A beast is most dangerous when\n |
| 0x207295 | 9 | cornered. |
| 0x20729f | 35 | Then perhaps I will do just that.\n |
| 0x2072c3 | 45 | That way, they may actually provide me some\n |
| 0x2072f1 | 14 | entertainment. |
| 0x207300 | 44 | Now, let us see just what you will do when\n |
| 0x20732d | 19 | cornered... Hmhmhm. |
| 0x207341 | 40 | Come now. What will your next move be?\n |
| 0x20736a | 34 | I could use a bit more excitement. |
| 0x20738d | 47 | Lord Raiko, you mustn't treat this as a game... |
| 0x2073bd | 48 | War is decided by tactics. Man and beast alike\n |
| 0x2073ee | 48 | dance in the palm of my hand, to whatever tune\n |
| 0x20741f | 7 | I wish. |
| 0x207427 | 43 | Oh... Lord Raiko, a new report has come in. |
| 0x207453 | 3 | Hm? |
| 0x207457 | 48 | It is from Lord Mikazuchi. He has succeeded in\n |
| 0x207488 | 22 | saving Lord Dekopompo. |
| 0x20749f | 46 | Hmhm. Saved, eh? And here I might never have\n |
| 0x2074ce | 48 | had to see that fattened face again. His luck,\n |
| 0x2074ff | 10 | I suppose. |
| 0x20750a | 45 | That was quite the feat for Lord Mikazuchi.\n |
| 0x207538 | 44 | One can only wonder how he resolved such a\n |
| 0x207565 | 15 | dire situation. |
| 0x207575 | 51 | It is only the natural outcome. He is my brother,\n |
| 0x2075a9 | 46 | and one granted honor and title by the Mikado. |
| 0x2075d8 | 47 | It may serve you to be more honest about your\n |
| 0x207608 | 23 | feelings, Lord Raiko... |
| 0x207620 | 7 | Hmph... |
| 0x207628 | 47 | Lord Mikazuchi thrives in the heat of battle.\n |
| 0x207658 | 45 | A flower, one might say, that blooms on the\n |
| 0x207686 | 15 | field of war... |
| 0x207696 | 24 | The field of war, hm...? |
| 0x2076af | 45 | What Mikazuchi does is altogether different\n |
| 0x2076dd | 27 | from what I would call war. |
| 0x2076f9 | 13 | Lord Raiko... |
| 0x207707 | 45 | Animalistic instinct and impulse, requiring\n |
| 0x207735 | 49 | neither intellect nor forethought. Mere violence. |
| 0x207767 | 46 | War, however, is a science. Know your enemy,\n |
| 0x207796 | 49 | know your own power and all properties thereof,\n |
| 0x2077c8 | 31 | and calculate an answer thusly. |
| 0x2077e8 | 48 | In all situations, we must quickly adapt, move\n |
| 0x207819 | 44 | before the enemy does, and strike at their\n |
| 0x207846 | 9 | weakness. |
| 0x207850 | 45 | Through that, one may conquer even with few\n |
| 0x20787e | 46 | soldiers, as inevitably as objects must fall\n |
| 0x2078ad | 12 | from height. |
| 0x2078ba | 43 | Even without relying on the strength of a\n |
| 0x2078e6 | 13 | select few... |
| 0x2078f4 | 37 | Bravery and heroes do not win wars.\n |
| 0x20791a | 47 | What DOES is power... how you use it, and how\n |
| 0x20794a | 15 | you control it. |
| 0x20795e | 42 | But how boorish of me, to cheapen my own\n |
| 0x207989 | 21 | brother's victory so. |
| 0x20799f | 36 | Perhaps it smacks of jealousy, hm?\n |
| 0x2079c4 | 50 | The bitterness of a man who wields only the pen,\n |
| 0x2079f7 | 20 | and never the sword? |
| 0x207a0c | 19 | Not at all, milord. |
| 0x207a20 | 46 | I jest, of course. But perhaps I can show my\n |
| 0x207a4f | 45 | unworthy brother what a perfect battlefield\n |
| 0x207a7d | 11 | looks like. |
| 0x207a89 | 40 | Alert all forces! We end this war now!\n |
| 0x207ab2 | 44 | Send every soldier available! We eliminate\n |
| 0x207adf | 22 | them once and for all! |
| 0x207af6 | 16 | Yes, Lord Raiko. |
| 0x207b07 | 13 | ch400_00_base |
| 0x207b16 | 14 | ch400_00_wheel |
| 0x207b25 | 6 | target |
| 0x207b2c | 7 | L_yoroi |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_17.json` com a forma:
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
