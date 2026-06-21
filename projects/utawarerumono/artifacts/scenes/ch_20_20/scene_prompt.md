# Cena ch_20_20 — pacote de traducao (240 linhas)

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
| Entua | Personagem | Entua | manter_original | major |
| Girl | UI | Garota | traduzir | none |
| Gundhurua | Personagem | Gundhurua | manter_original | moderate |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Yamatan | Etnia | de Yamato | traduzir | none |
| Yamato | Local | Yamato | manter_original | none |
| Zeguni | Personagem | Zeguni | manter_original | none |

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
- **Mikado** (major): Trate o Mikado apenas como o soberano/titulo, a distancia. NAO antecipe vinculo pessoal com nenhum personagem.

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `Adviser` -> `Conselheiro` (Yamatan adviser, 20_17)
- `Soldier` -> `SOLDADO` (SOLDIER, 20_01)
- `back.` -> `voltei.` (Haku, 18_01)
- `Sir!` -> `Sim!` (Maroro, 12_09)
- `No.` -> `Não.` (Protagonista (narração), 18_01)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `And then...` -> `e depois...` (Kuon, 11_02)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `stomach.` -> `estômago.` (Haku, 17_01)
- `the ground.` -> `no chão.` (Haku, 13_05)
- `LeftLeg` -> `LeftLeg` (SYSTEM, 20_11)
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
| 0x20eb0f | 45 | From far off, the cries of the Yamatan army\n |
| 0x20eb3d | 13 | can be heard. |
| 0x20eb4b | 7 | Adviser |
| 0x20eb53 | 46 | My owlo, the Yamatan army is swiftly closing\n |
| 0x20eb82 | 19 | in on our position. |
| 0x20eb96 | 48 | Although we may stall them for now, it is only\n |
| 0x20ebc7 | 45 | a matter of time before they break through... |
| 0x20ebf5 | 19 | We need a decision. |
| 0x20ec09 | 37 | Very well... What will be my options? |
| 0x20ec2f | 46 | For now, we can flee to the west... Uzurusha\n |
| 0x20ec5e | 47 | is wide and vast. Even the Yamatans could not\n |
| 0x20ec8e | 17 | maintain pursuit. |
| 0x20eca0 | 47 | As long as you live, my owlo, we may regroup.\n |
| 0x20ecd0 | 44 | You can reclaim the separated units on our\n |
| 0x20ecfd | 7 | return. |
| 0x20ed05 | 31 | Now is the time to persevere... |
| 0x20ed25 | 10 | Ghhhh...!! |
| 0x20ed30 | 49 | The room falls silent, apart from the sounds of\n |
| 0x20ed62 | 46 | battle outside. All freeze as the man's head\n |
| 0x20ed91 | 6 | rolls. |
| 0x20ed98 | 7 | Soldier |
| 0x20eda0 | 11 | Ah... Ahhh! |
| 0x20edac | 43 | The owlo brandishes his bloodstained blade. |
| 0x20edd8 | 35 | ...You dare tell me to turn tail?\n |
| 0x20edfc | 41 | You dare tell me to abandon my homeland!? |
| 0x20ee26 | 37 | My owlo, please! You must understand! |
| 0x20ee4c | 10 | You DARE!! |
| 0x20ee57 | 9 | My owlo!! |
| 0x20ee61 | 6 | Hmh... |
| 0x20ee6c | 47 | Commander Zeguni stares into Gundhurua's eyes\n |
| 0x20ee9c | 14 | unflinchingly. |
| 0x20eeab | 45 | Gundhurua finally relents at his determined\n |
| 0x20eed9 | 46 | gaze, and sheathes his sword as he turns his\n |
| 0x20ef08 | 5 | back. |
| 0x20ef0e | 28 | We shall go, then... Zeguni. |
| 0x20ef2b | 10 | My owlo... |
| 0x20ef36 | 24 | This is not a retreat... |
| 0x20ef4f | 30 | We are merely shifting course! |
| 0x20ef6e | 17 | Y-Yes, milord...! |
| 0x20ef80 | 29 | We shall return here one day! |
| 0x20ef9e | 45 | Those who yet live, rise and escort our owlo! |
| 0x20efcc | 4 | Sir! |
| 0x20efd1 | 45 | Zeguni follows the retreating soldiers, but\n |
| 0x20efff | 38 | pauses a moment to look up at the sky. |
| 0x20f026 | 9 | ...Entua. |
| 0x20f030 | 46 | Zeguni speaks the name of his absent daughter. |
| 0x20f05f | 45 | Are you still alive...? Then please, do not\n |
| 0x20f08d | 46 | throw your life away in vain. You must live.\n |
| 0x20f0bc | 36 | Grovel, bow, and scrape, but live... |
| 0x20f0e1 | 46 | There are no signs of pursuit. It may be too\n |
| 0x20f110 | 46 | difficult to follow us over such treacherous\n |
| 0x20f13f | 8 | terrain. |
| 0x20f148 | 46 | And with their numbers, it would surely take\n |
| 0x20f177 | 25 | time to get through here. |
| 0x20f191 | 40 | If we are able to regroup in that time-- |
| 0x20f1ba | 44 | Gundhurua, who had been showing no sign of\n |
| 0x20f1e7 | 44 | attention to Zeguni's words, suddenly halts. |
| 0x20f214 | 5 | Owlo? |
| 0x20f21a | 13 | Th-That is... |
| 0x20f228 | 48 | A single man stands before the remnants of the\n |
| 0x20f259 | 36 | Uzurushan army, blocking their way.  |
| 0x20f27e | 31 | Khuhahaha... So that is it...\n |
| 0x20f29e | 42 | I understand now why there was no pursuit. |
| 0x20f2c9 | 46 | The old man's favorite lapdog has come for me. |
| 0x20f2f8 | 40 | The Imperial Guard of the Right, Oshtor! |
| 0x20f321 | 44 | When I did not see your face on the field,\n |
| 0x20f34e | 46 | I thought you cowering behind your capital's\n |
| 0x20f37d | 8 | walls... |
| 0x20f386 | 30 | You gnat! You make me laugh.\n |
| 0x20f3a5 | 34 | Was this supposed to be an ambush? |
| 0x20f3c8 | 40 | You dare think you can stand in my way!? |
| 0x20f3f1 | 3 | No. |
| 0x20f3f5 | 8 | What...? |
| 0x20f3fe | 46 | The orders given to me by the Mikado were to\n |
| 0x20f42d | 12 | exterminate. |
| 0x20f43a | 47 | Hmph. So that old relic thinks me little more\n |
| 0x20f46a | 16 | than a pest, eh? |
| 0x20f47b | 40 | Very well, Oshtor. But I warn you now;\n |
| 0x20f4a4 | 36 | my head will not be so easily taken. |
| 0x20f4c9 | 41 | As Gundhurua draws his blade and begins\n |
| 0x20f4f3 | 46 | advancing, Zeguni kneels before him to block\n |
| 0x20f522 | 8 | his way. |
| 0x20f52b | 8 | My owlo. |
| 0x20f534 | 42 | Oh? So you would obstruct my path as well? |
| 0x20f55f | 41 | No, my owlo. I would ask your permission. |
| 0x20f589 | 11 | Then speak. |
| 0x20f595 | 39 | I ask that you allow me to handle this. |
| 0x20f5bd | 43 | I wish to slay this bearer of the mask to\n |
| 0x20f5e9 | 13 | attain glory. |
| 0x20f5f7 | 48 | Gundhurua stares at the commander's face for a\n |
| 0x20f628 | 21 | moment, then mutters. |
| 0x20f63e | 26 | I see... Martyrdom, is it? |
| 0x20f659 | 37 | Old fool... You may do as you please. |
| 0x20f67f | 29 | I thank you for this honor.\n |
| 0x20f69d | 35 | I promise to kill him without fail! |
| 0x20f6c1 | 47 | Gundhurua does not reply as he turns his back\n |
| 0x20f6f1 | 10 | on Zeguni. |
| 0x20f6fc | 34 | Zeguni stands and draws his blade. |
| 0x20f71f | 41 | Those of you who seek glory, follow me!\n |
| 0x20f749 | 42 | Oshtor's head will be worth one thousand\n |
| 0x20f774 | 5 | gold! |
| 0x20f77a | 13 | Raaaaaaaaah!! |
| 0x20f788 | 49 | Zeguni charges Oshtor together with his soldiers. |
| 0x20f7ba | 44 | You would sacrifice your own life to allow\n |
| 0x20f7e7 | 44 | Gundhurua to escape... I commend your valor. |
| 0x20f814 | 14 | Haaaaaaaaaah!! |
| 0x20f823 | 34 | Then I shall honor your resolve... |
| 0x20f846 | 17 | Gaaaaaaaaaaaaah!! |
| 0x20f858 | 45 | With one swing of Oshtor's massive arm, the\n |
| 0x20f886 | 43 | closest Uzurushan soldiers are flung aside. |
| 0x20f8b2 | 44 | These masked generals are nothing short of\n |
| 0x20f8df | 48 | monsters... Numbers mean nothing against them.\n |
| 0x20f910 | 10 | So, then-- |
| 0x20f91b | 8 | Oshtor!! |
| 0x20f927 | 36 | I am Commander Zeguni of Uzurusha!\n |
| 0x20f94c | 26 | I challenge you to a duel! |
| 0x20f967 | 49 | It would be shameful of me to deny such a brave\n |
| 0x20f999 | 20 | warrior as yourself. |
| 0x20f9ae | 9 | I accept. |
| 0x20f9b8 | 46 | Hm... So you will not use that accursed mask\n |
| 0x20f9e7 | 43 | against me. That's quite arrogant of you... |
| 0x20fa13 | 46 | I would claim victory against a true warrior\n |
| 0x20fa42 | 18 | with my own hands! |
| 0x20fa55 | 41 | Then let your arrogance be your downfall! |
| 0x20fa7f | 13 | Haaaaaaaaaah! |
| 0x20fa8d | 48 | Entua, following the remaining Uzurusha forces\n |
| 0x20fabe | 46 | to the west, tracks their escape to a raging\n |
| 0x20faed | 7 | battle. |
| 0x20faf5 | 31 | ...That... crest on the flag... |
| 0x20fb15 | 8 | Father!! |
| 0x20fb1e | 12 | Hrraaaaaah!! |
| 0x20fb2b | 6 | Hm...! |
| 0x20fb32 | 5 | Ggh!! |
| 0x20fb38 | 45 | Oshtor's powerful strikes knock Zeguni back\n |
| 0x20fb66 | 47 | across the ground, even as he blocks with his\n |
| 0x20fb96 | 6 | blade. |
| 0x20fb9d | 41 | The difference in power is too great...\n |
| 0x20fbc7 | 45 | Zeguni cannot land a single blow, and he is\n |
| 0x20fbf5 | 18 | soon knocked down. |
| 0x20fc08 | 51 | S-Such power... It seems I am no match for you...\n |
| 0x20fc3c | 9 | However-- |
| 0x20fc46 | 5 | Hm... |
| 0x20fc4c | 50 | Zeguni's body is covered in wounds, but he still\n |
| 0x20fc7f | 46 | stands, defying the pain coursing through him. |
| 0x20fcae | 42 | You shall not pass... Even if my body is\n |
| 0x20fcd9 | 39 | destroyed... I shall not let you pass!! |
| 0x20fd01 | 43 | So you still stand... I did not expect to\n |
| 0x20fd2d | 44 | encounter such a warrior as yourself among\n |
| 0x20fd5a | 15 | the Uzurushans. |
| 0x20fd6a | 46 | However, I am a warrior of Yamato in service\n |
| 0x20fd99 | 14 | of the Mikado! |
| 0x20fda8 | 49 | I shall show no forgiveness to those that bring\n |
| 0x20fdda | 48 | despair to my liege, and suffering to my people. |
| 0x20fe0b | 44 | Lord Zeguni, come at me with all your might! |
| 0x20fe38 | 32 | This will be our final strike!\n |
| 0x20fe59 | 22 | Let this end our duel! |
| 0x20fe70 | 45 | Very well. Then taste the might of my final\n |
| 0x20fe9e | 47 | strike... for I shall put my very life behind\n |
| 0x20fece | 3 | it! |
| 0x20fed2 | 14 | HAAAAAAAAAAH!! |
| 0x20fee1 | 45 | It ends in a flash. Each sword strikes with\n |
| 0x20ff0f | 38 | speed beyond the eye's perception...\n |
| 0x20ff36 | 18 | and silence falls. |
| 0x20ff49 | 11 | And then... |
| 0x20ff55 | 8 | Ghh...!! |
| 0x20ff5e | 46 | Blood spurts in a line across Zeguni's chest\n |
| 0x20ff8d | 16 | to his shoulder. |
| 0x20ff9e | 49 | Oshtor's strike has left a fatal cut diagonally\n |
| 0x20ffd0 | 21 | across Zeguni's body. |
| 0x20ffe6 | 11 | Ghaaah...!! |
| 0x20fff2 | 44 | The scent of blood fills the air as Zeguni\n |
| 0x21001f | 45 | staggers, his sword clattering to the ground. |
| 0x21004d | 47 | However... as Zeguni looks toward Oshtor, his\n |
| 0x21007d | 34 | face shows only a gentle serenity. |
| 0x2100a0 | 46 | ...Impressive... I would expect no less from\n |
| 0x2100cf | 34 | the Imperial Guard of the Right... |
| 0x2100f2 | 38 | Your skills are remarkable, as well... |
| 0x210119 | 46 | Hah... So I have succeeded... in landing one\n |
| 0x210148 | 7 | strike. |
| 0x210150 | 47 | A small trickle of blood trails down Oshtor's\n |
| 0x210180 | 43 | body. A small cut, but Zeguni's blade had\n |
| 0x2101ac | 19 | indeed reached him. |
| 0x2101c0 | 27 | Then I have no regrets...\n |
| 0x2101dc | 30 | I thank you for this battle... |
| 0x2101fb | 44 | A satisfied smile crosses Zeguni's face...\n |
| 0x210228 | 30 | and he crumples to the ground. |
| 0x210247 | 37 | What an extraordinary man you were.\n |
| 0x21026d | 46 | You protected your lord, and died with honor\n |
| 0x21029c | 19 | as a brave samurai. |
| 0x2102b0 | 44 | You truly embody the spirit of a mononofu... |
| 0x2102dd | 47 | Lord Zeguni... I can only hope that I one day\n |
| 0x21030d | 33 | meet my end as you did yours...\n |
| 0x21032f | 11 | With honor. |
| 0x21033b | 11 | NOOOOOOOO!! |
| 0x210347 | 6 | Hm...? |
| 0x21034e | 15 | Father! FATHER! |
| 0x21035e | 49 | A girl jumps from the brush and runs to the man\n |
| 0x210390 | 45 | on the ground, tears streaming down her face. |
| 0x2103be | 26 | Entua glares up at Oshtor. |
| 0x2103d9 | 29 | You... You did this to him... |
| 0x2103f7 | 47 | Entua swiftly draws a shortsword from her side. |
| 0x210427 | 34 | You will PAY for what you've done! |
| 0x21044a | 12 | Nh, nnngh... |
| 0x210457 | 46 | Entua's sword strikes Oshtor directly in the\n |
| 0x210486 | 8 | stomach. |
| 0x21048f | 41 | However, the blade does not pierce him.\n |
| 0x2104b9 | 47 | It is stopped at the surface, as Entua's hand\n |
| 0x2104e9 | 16 | begins to shake. |
| 0x2104fa | 49 | ...I am afraid your skill with a sword will not\n |
| 0x21052c | 34 | be enough to make a scratch on me. |
| 0x21054f | 5 | Aah!! |
| 0x210555 | 45 | Oshtor grabs the blade of Entua's sword and\n |
| 0x210583 | 47 | rips it from her hand. The force casts her to\n |
| 0x2105b3 | 11 | the ground. |
| 0x2105bf | 28 | You... You killed my father! |
| 0x2105dc | 49 | ...I cannot excuse what I have done. Nor will I\n |
| 0x21060e | 45 | run from it. I have chosen a path of carnage. |
| 0x21063c | 49 | But... I would not have you share your father's\n |
| 0x21066e | 5 | fate. |
| 0x210674 | 50 | Oshtor turns his back on Entua as if she doesn't\n |
| 0x2106a7 | 41 | even exist, intent on pursuing Gundhurua. |
| 0x2106d1 | 45 | Entua can do nothing but watch as he departs. |
| 0x2106ff | 48 | Oshtor quickly begins pursuing Gundhurua as he\n |
| 0x210730 | 28 | leaves the site of his duel. |
| 0x21074d | 50 | Yet the remaining Uzurushans continue to resist,\n |
| 0x210780 | 43 | and sacrifice themselves to let Gundhurua\n |
| 0x2107ac | 7 | escape. |
| 0x2107b4 | 48 | Many Uzurushans fall to Oshtor's blade, but in\n |
| 0x2107e5 | 45 | the end, Gundhurua is never found among the\n |
| 0x210813 | 5 | dead. |
| 0x210819 | 49 | Meanwhile, the other generals begin subjugating\n |
| 0x21084b | 47 | the rest of Uzurusha, mountains of corpses in\n |
| 0x21087b | 11 | their wake. |
| 0x210887 | 45 | With their leader on the run, the Uzurushan\n |
| 0x2108b5 | 41 | people soon give in, and Yamato assumes\n |
| 0x2108df | 18 | political control. |
| 0x2108f2 | 44 | Thus ends the great war between Yamato and\n |
| 0x21091f | 11 | Uzurusha... |
| 0x21092b | 4 | flag |
| 0x210930 | 7 | LeftLeg |

## 8. Formato de saida EXIGIDO
Escreva `translations_20_20.json` com a forma:
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
