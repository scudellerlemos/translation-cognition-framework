# Cena ch_30_11 — pacote de traducao (518 linhas)

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
| Akuruka | Objeto | Akuruka | manter_original | moderate |
| Akuruturuka | Termo | Akuruturuka | manter_original | major |
| Atuy | Personagem | Atuy | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
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
### Nosuri — criticality: medium
- Nosuri — `voice_criticality: medium`. Fora-da-lei atrevida e malandra; "aliada da justiça" irônica; oportunista. Registro coloquial/esperto.
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `asleep.` -> `adormecido.` (Narrador (Haku - 1ª pessoa), 19_08)
- `up.` -> `para cima.` (Protagonista, 17_01)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `Wha--` -> `Quê--` (Man, 11_01)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `Oshtor...` -> `Oshtor...` (Haku, 18_01)
- `That is...` -> `Isso é...` (Mulher, 17_01)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `...I am sorry.` -> `...Sinto muito.` (Oshtor, 31_01)
- `THAT thing.` -> `AQUILO.` (Kuon, 18_01)
- `Nekone...` -> `Nekone...` (Maroro, 17_03)
- `But...` -> `mas...` (Kuon, 11_01)
- `Dear brother...` -> `Querido irmão...` (Nekone, 14_04)
- `to me.` -> `a mim.` (Narrador, 12_11)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `Vurai.` -> `Vurai.` (Woshis, 30_02)
- `Y-Yes.` -> `S-Sim.` (Yuuri, 16_02)
- `idea.` -> `ideia.` (Haku, 14_08)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `Nekone--` -> `Nekone--` (Oshtor, 30_06)
- `carriage.` -> `carruagem.` (Maroro, 19_05)
- `from.` -> `de.` (Atuy, 16_02)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `That's--` -> `Isso--` (Nosuri, 19_04)
- `any more.` -> `assim.` (Ukon, 14_04)
- `Haku.` -> `Haku.` (Kuon, 12_08)
- `Sir Haku...` -> `Senhor Haku...` (Garota, 16_03)
- `Then--` -> `Então--` (Haku, 14_03)
- `For him.` -> `Por ele.` (Ukon, 16_02)
- `but--` -> `mas--` (Oshtor, 19_05)
- `her...` -> `dela...` (Nekone, 18_01)
- `eyes.` -> `olhar.` (Haku, 14_04)
- `time.` -> `vez.` (Raurau, 18_01)
- `Ah!?` -> `Ah!?` (Rulutieh, 14_04)
- `Urgh...` -> `Argh...` (Haku, 11_01)
- `Oshtor!!` -> `Oshtor!!` (Zeguni, 20_20)
- `Dear brother!!` -> `Querido irmão!!` (Nekone, 30_05)
- `Gah--` -> `Ai--` (Vurai, 30_01)
- `unscathed.` -> `intacta.` (Garota, 18_01)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `Guh!?` -> `Guh!?` (Soldado, 20_07)
- `Wh--!?` -> `Q-Quê!?` (Haku, 18_01)
- `*Gasp*` -> `*Suspiro assustado*` (Garota, 17_01)
- `Ah... ah...` -> `Ah... ah...` (Protagonista, 19_08)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Osh... tor...` -> `Osh... tor...` (Protagonista, 30_03)
- `D-Dear brother...` -> `C-Caro irmão...` (Nekone, 15_01)
- `Amazing...` -> `Incrível...` (Haku, 12_04)
- `Impossible...` -> `Impossível...` (Kuon, 22_05)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `Oshtor, right?` -> `Oshtor, certo?` (Rulutieh, 18_02)
- `Ha... ku...` -> `Ha... ku...` (Kuon, 11_02)
- `GlobalSRT` -> `GlobalSRT` (SYSTEM, 20_11)
- `target` -> `target` (SYSTEM, 20_11)
- `face` -> `face` (SYSTEM, 20_14)
- `body` -> `body` (SYSTEM, 20_14)
- `hair` -> `hair` (SYSTEM, 20_14)
- `Head` -> `Head` (rotulo, 11_03)
- `LeftFoot` -> `LeftFoot` (system, 13_06)
- `RightFoot` -> `RightFoot` (system, 13_06)
- `RightIndexFinger2` -> `DedoÍndiceDir2` (SYSTEM, 31_01)
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
| 0x30e09e | 45 | Several days of travel have passed since we\n |
| 0x30e0cc | 29 | escaped the imperial capital. |
| 0x30e0ea | 50 | We've avoided detection so far, but Oshtor's not\n |
| 0x30e11d | 47 | looking good. All of us are worn out, or fast\n |
| 0x30e14d | 7 | asleep. |
| 0x30e155 | 49 | It's plain to see we're all still pretty messed\n |
| 0x30e187 | 3 | up. |
| 0x30e18b | 6 | ...Hm? |
| 0x30e192 | 45 | As we pass through a deep gorge, we reach a\n |
| 0x30e1c0 | 46 | rock-strewn wasteland. Oshtor rises, looking\n |
| 0x30e1ef | 13 | back sharply. |
| 0x30e1fd | 16 | Dear brother...? |
| 0x30e20e | 36 | What's up? Something catch your eye? |
| 0x30e233 | 18 | ...So he has come. |
| 0x30e246 | 6 | What!? |
| 0x30e24d | 46 | I'm caught by surprise, and I quickly follow\n |
| 0x30e27c | 34 | his gaze, but I see nothing there. |
| 0x30e29f | 46 | All I see is the gorge growing more and more\n |
| 0x30e2ce | 46 | distant in the setting sun's light, darkness\n |
| 0x30e2fd | 10 | spreading. |
| 0x30e308 | 43 | I don't see anything. Are you sure you're\n |
| 0x30e334 | 26 | not just imagining things? |
| 0x30e34f | 20 | No. I can sense him. |
| 0x30e364 | 47 | I realize Oshtor's mask is lightly vibrating;\n |
| 0x30e394 | 45 | a keening high-pitched noise audible from it. |
| 0x30e3c2 | 42 | This intense rage... this mad thirst for\n |
| 0x30e3ed | 14 | destruction... |
| 0x30e3fc | 47 | I know of only one man that gives off an aura\n |
| 0x30e42c | 13 | such as this. |
| 0x30e43a | 16 | Vurai is coming. |
| 0x30e44b | 5 | Wha-- |
| 0x30e451 | 45 | I feel a bead of cold sweat trickle down my\n |
| 0x30e47f | 6 | cheek. |
| 0x30e486 | 20 | He's... still alive? |
| 0x30e49b | 40 | Lady Rulutieh, kindly stop the carriage. |
| 0x30e4c4 | 7 | Huh...? |
| 0x30e4cc | 19 | O-Oh, yes. Cocopo-- |
| 0x30e4e0 | 48 | The carriage stops, and all eyes look to Oshtor. |
| 0x30e511 | 50 | I shall hold him off here. I wish for all of you\n |
| 0x30e544 | 49 | to gain as much distance as possible while I do\n |
| 0x30e576 | 3 | so. |
| 0x30e57a | 9 | Oshtor... |
| 0x30e584 | 45 | Don't be an idiot. You do realize the state\n |
| 0x30e5b2 | 21 | you're in, don't you? |
| 0x30e5cc | 43 | Boss's right, yeah? If there's gonna be a\n |
| 0x30e5f8 | 44 | showdown here, shouldn't we all take him on? |
| 0x30e625 | 46 | Indeed! We have beaten him once. All we have\n |
| 0x30e654 | 34 | to do is to trounce him once more. |
| 0x30e677 | 47 | That will not be possible, for he has already\n |
| 0x30e6a7 | 20 | released his powers. |
| 0x30e6bc | 44 | We are the Akuruturuka. Of all of us here,\n |
| 0x30e6e9 | 41 | I alone stand a chance against his power. |
| 0x30e713 | 45 | That thing he did back in Uzurusha where he\n |
| 0x30e741 | 38 | wiped out an entire army on his own... |
| 0x30e768 | 46 | But dear brother, if that is true, it is all\n |
| 0x30e797 | 45 | the more reason for us to lend you our aid... |
| 0x30e7c5 | 22 | No. It's the opposite. |
| 0x30e7dc | 43 | You're saying if we stick around, we'd be\n |
| 0x30e808 | 29 | holding you back. Is that it? |
| 0x30e826 | 48 | Oshtor doesn't respond to me, but stands there\n |
| 0x30e857 | 41 | silently, watching the horizon behind us. |
| 0x30e881 | 46 | We're in bad shape, and we struggled against\n |
| 0x30e8b0 | 46 | Vurai even back then. Can we really take him\n |
| 0x30e8df | 14 | at full power? |
| 0x30e8ee | 48 | Sure, he's probably still wounded, but he even\n |
| 0x30e91f | 45 | caught up to our carriage. He's not done yet. |
| 0x30e94d | 10 | That is... |
| 0x30e958 | 48 | Not to mention Atuy used up everything she had\n |
| 0x30e989 | 44 | in that last fight. She's still fast asleep. |
| 0x30e9b6 | 14 | Zzz... zzzz... |
| 0x30e9c5 | 49 | I'm sure she'd be happy to fight if we woke her\n |
| 0x30e9f7 | 10 | up, but... |
| 0x30ea02 | 47 | Ho boy. So we'd just end up slowin' you down,\n |
| 0x30ea32 | 4 | huh? |
| 0x30ea37 | 14 | ...I am sorry. |
| 0x30ea46 | 46 | Don't worry about it. Can't really argue the\n |
| 0x30ea75 | 44 | fact that we wouldn't be much help against\n |
| 0x30eaa2 | 11 | that thing. |
| 0x30eaae | 46 | To be honest, we'd probably get slaughtered.\n |
| 0x30eadd | 45 | I feel bad for Oshtor, but this is probably\n |
| 0x30eb0b | 13 | for the best. |
| 0x30eb19 | 37 | I-I will stay here too, dear brother. |
| 0x30eb3f | 9 | Nekone... |
| 0x30eb49 | 48 | I-I should be fine if I stay far enough behind\n |
| 0x30eb7a | 37 | to simply watch over you. So please-- |
| 0x30eba0 | 48 | What troubles you, Nekone? It is unlike you to\n |
| 0x30ebd1 | 40 | ask for something so directly like this. |
| 0x30ebfa | 45 | But... you are still injured, dear brother.\n |
| 0x30ec28 | 9 | Yet you-- |
| 0x30ec32 | 48 | There is no need for concern. Nekone, could it\n |
| 0x30ec63 | 39 | be that you truly believe I might lose? |
| 0x30ec8b | 41 | No, I would never suggest such a thing!\n |
| 0x30ecb5 | 37 | There is no way that you could lose-- |
| 0x30ecdb | 39 | That is correct. I do not lose. Ever.\n |
| 0x30ed03 | 47 | So, Nekone, I want you to rest easy and await\n |
| 0x30ed33 | 10 | my return. |
| 0x30ed3e | 6 | But... |
| 0x30ed45 | 49 | It'll be all right. I think there's no need for\n |
| 0x30ed77 | 25 | us to worry about Oshtor. |
| 0x30ed91 | 48 | Kuon softly embraces Nekone from behind as she\n |
| 0x30edc2 | 31 | watches her brother, face pale. |
| 0x30ede2 | 15 | Dear brother... |
| 0x30edf2 | 46 | Nekone tries to keep close to Oshtor, but he\n |
| 0x30ee21 | 45 | gently places his hand on her head, looking\n |
| 0x30ee4f | 6 | to me. |
| 0x30ee56 | 50 | Haku, I leave the rest to you. Head to Ennakamuy\n |
| 0x30ee89 | 27 | first, and await my return. |
| 0x30eea5 | 48 | I am undoubtedly biased, but I believe it is a\n |
| 0x30eed6 | 49 | fine home. I am sure that you will come to like\n |
| 0x30ef08 | 11 | it as well. |
| 0x30ef14 | 36 | Yeah? Well, I'll look forward to it. |
| 0x30ef39 | 43 | ...And please ensure that Nekone does not\n |
| 0x30ef65 | 16 | linger overlong. |
| 0x30ef76 | 49 | What, me? You know she's going to end up hating\n |
| 0x30efa8 | 17 | my guts for this. |
| 0x30efba | 45 | My apologies. I promise that I will make it\n |
| 0x30efe8 | 18 | up to you someday. |
| 0x30effb | 37 | Fine, but I'm gonna hold you to that. |
| 0x30f021 | 17 | Aaand up you go-- |
| 0x30f033 | 41 | Ah!? Wh-What do you think you are doing!? |
| 0x30f05d | 47 | Yeah, yeah, quit struggling. Don't you forget\n |
| 0x30f08d | 21 | that promise, Oshtor. |
| 0x30f0a3 | 48 | L-Let me go! Unhand me! Where are you touching!? |
| 0x30f0d4 | 44 | Fwagh!? W-Would you stop flailing--Nosuri!\n |
| 0x30f101 | 19 | Grab Nekone's legs! |
| 0x30f115 | 43 | Yes, leave it to me. Calm down, now, your\n |
| 0x30f141 | 23 | clothes are all a mess. |
| 0x30f159 | 43 | Wh-What do you think you are looking at!?\n |
| 0x30f185 | 36 | Let go of me! Please, dear brother-- |
| 0x30f1aa | 20 | How is Her Highness? |
| 0x30f1bf | 47 | She's resting much easier now, and fast asleep. |
| 0x30f1ef | 9 | ...I see. |
| 0x30f1f9 | 46 | Oshtor's expression softens a little, relief\n |
| 0x30f228 | 18 | clear on his face. |
| 0x30f23b | 44 | Ennakamuy is now only a short distance away. |
| 0x30f268 | 47 | I shall join you there once I have dealt with\n |
| 0x30f298 | 6 | Vurai. |
| 0x30f29f | 45 | Oshtor, perhaps I don't need to remind you,\n |
| 0x30f2cd | 45 | but the medicine I gave you only suppresses\n |
| 0x30f2fb | 5 | pain. |
| 0x30f301 | 43 | I just want to remind you that it doesn't\n |
| 0x30f32d | 42 | necessarily mean you've healed, I suppose. |
| 0x30f358 | 34 | It will serve. You have my thanks. |
| 0x30f37b | 40 | Rulutieh, get the carriage moving again. |
| 0x30f3a4 | 50 | A good woman must trust men in times like these,\n |
| 0x30f3d7 | 45 | and send them off with valor. You understand. |
| 0x30f405 | 15 | ...All right... |
| 0x30f415 | 45 | But if Atuy hears of this later, she may be\n |
| 0x30f443 | 40 | disappointed that we didn't wake her up. |
| 0x30f46c | 7 | Zzzz... |
| 0x30f474 | 12 | Miss Atuy... |
| 0x30f481 | 21 | We should get moving. |
| 0x30f497 | 6 | Y-Yes. |
| 0x30f49e | 37 | The carriage begins moving once more. |
| 0x30f4c4 | 48 | Oshtor's silhouette grows smaller and smaller,\n |
| 0x30f4f5 | 38 | until he disappears into the darkness. |
| 0x30f51c | 47 | Nekone continues to gaze back toward where we\n |
| 0x30f54c | 19 | left Oshtor behind. |
| 0x30f560 | 49 | Well, this isn't good... She's way past grumpy.\n |
| 0x30f592 | 34 | She's probably completely enraged. |
| 0x30f5b5 | 48 | I can tell even with her back to me what she's\n |
| 0x30f5e6 | 45 | thinking. "Don't touch me. Don't talk to me." |
| 0x30f614 | 47 | She was struggling so much, I had to lift her\n |
| 0x30f644 | 50 | by the legs and drag her. Probably wasn't a good\n |
| 0x30f677 | 5 | idea. |
| 0x30f67d | 34 | Nekone suddenly stands up shakily. |
| 0x30f6a0 | 49 | Nekone, these roads are treacherous and uneven.\n |
| 0x30f6d2 | 49 | It's dangerous to stand up on the carriage like\n |
| 0x30f704 | 5 | that. |
| 0x30f70a | 12 | Miss Nekone? |
| 0x30f717 | 43 | Rulutieh looks over worriedly, but Nekone\n |
| 0x30f743 | 45 | doesn't look back at her--only staring into\n |
| 0x30f771 | 13 | the darkness. |
| 0x30f77f | 8 | Nekone-- |
| 0x30f788 | 50 | Kuon seems to sense something wrong, and just as\n |
| 0x30f7bb | 31 | she straightens up, it happens. |
| 0x30f7e0 | 49 | Nekone takes a short breath, then leaps off the\n |
| 0x30f812 | 9 | carriage. |
| 0x30f81c | 47 | She curls her small body and rolls across the\n |
| 0x30f84c | 8 | ground-- |
| 0x30f855 | 42 | Getting to her feet, she instantly bolts\n |
| 0x30f880 | 46 | straight down the path back to where we came\n |
| 0x30f8af | 5 | from. |
| 0x30f8b5 | 13 | You kiddin'!? |
| 0x30f8c3 | 19 | That stubborn kid-- |
| 0x30f8d7 | 42 | Don't tell me she's going back to Oshtor!? |
| 0x30f902 | 48 | As we speak, Nekone keeps running, her outline\n |
| 0x30f933 | 46 | in the darkness getting smaller by the second. |
| 0x30f962 | 36 | NEKONE! Rulutieh, stop the carriage! |
| 0x30f987 | 14 | Huh!? R-Right! |
| 0x30f996 | 15 | Miss Nekone...! |
| 0x30f9a6 | 36 | I'll go get her. All of you should-- |
| 0x30f9cb | 48 | I quickly grab Kuon's shoulder as she rises to\n |
| 0x30f9fc | 14 | follow Nekone. |
| 0x30fa0b | 26 | Hold it. I'll handle this. |
| 0x30fa26 | 5 | Haku? |
| 0x30fa2c | 47 | Who's going to treat the princess without you\n |
| 0x30fa5c | 30 | around? You need to stay here. |
| 0x30fa7b | 8 | That's-- |
| 0x30fa84 | 42 | If that's the case, I shall accompany you. |
| 0x30faaf | 24 | You can count me in too! |
| 0x30fac8 | 49 | Sorry, no. We need guards for the princess, and\n |
| 0x30fafa | 48 | with the twins asleep, we can't afford to lose\n |
| 0x30fb2b | 9 | any more. |
| 0x30fb35 | 42 | Our top priority right now is to get the\n |
| 0x30fb60 | 48 | princess to safety. I'll get Nekone--you go to\n |
| 0x30fb91 | 10 | Ennakamuy. |
| 0x30fb9c | 15 | But, Sir Haku-- |
| 0x30fbac | 45 | Don't worry! When I get back, I'll have 'em\n |
| 0x30fbda | 13 | both with me! |
| 0x30fbe8 | 49 | I yell behind me as I run towards the direction\n |
| 0x30fc1a | 37 | Nekone disappeared into the darkness. |
| 0x30fc40 | 26 | You sure about this, Kuon? |
| 0x30fc5b | 46 | Not really... but I guess we don't have much\n |
| 0x30fc8a | 12 | of a choice. |
| 0x30fc97 | 46 | Let's hurry. I'm sure we can leave Nekone to\n |
| 0x30fcc6 | 5 | Haku. |
| 0x30fccc | 41 | Hm. You really do trust him with a lot... |
| 0x30fcf6 | 36 | I don't know if I'd call it trust.\n |
| 0x30fd1b | 48 | I just know Haku always manages to make it out\n |
| 0x30fd4c | 22 | alive, no matter what. |
| 0x30fd63 | 44 | We'd be wasting our time worrying about him. |
| 0x30fd90 | 20 | Heh, got that right. |
| 0x30fda5 | 11 | Sir Haku... |
| 0x30fdb1 | 23 | Hah... hah... hahh...\n |
| 0x30fdc9 | 16 | Got you, Nekone! |
| 0x30fdda | 17 | Ah!? U-Unhand me! |
| 0x30fdec | 46 | Dear brother! I must go to my dear brother's\n |
| 0x30fe1b | 6 | side-- |
| 0x30fe22 | 19 | I have to help him! |
| 0x30fe36 | 48 | Didn't you hear Oshtor!? He said we'd just get\n |
| 0x30fe67 | 11 | in the way. |
| 0x30fe73 | 12 | That's not-- |
| 0x30fe80 | 36 | Nekone bites her lip in frustration. |
| 0x30fea5 | 43 | I know... I know I cannot be of any help... |
| 0x30fed1 | 49 | I know that I would not be able to do anything,\n |
| 0x30ff03 | 22 | even if I was there... |
| 0x30ff1a | 6 | Then-- |
| 0x30ff21 | 43 | I have seen my dear brother off to many a\n |
| 0x30ff4d | 14 | battle before. |
| 0x30ff5c | 48 | I always felt anxious, but I was never worried\n |
| 0x30ff8d | 8 | for him. |
| 0x30ff96 | 50 | I knew and believed that he would always return,\n |
| 0x30ffc9 | 15 | no matter what. |
| 0x30ffd9 | 5 | But-- |
| 0x30ffdf | 47 | But there has never been a battle between two\n |
| 0x31000f | 19 | Akuruturuka before. |
| 0x310023 | 41 | And on top of that, he is... so gravely\n |
| 0x31004d | 10 | injured... |
| 0x310058 | 47 | Look, I understand how you feel, but if we go\n |
| 0x310088 | 41 | back, we're just going to get in his way. |
| 0x3100b2 | 26 | I know that. That is why-- |
| 0x3100cd | 48 | That is why I wished to at least watch over my\n |
| 0x3100fe | 28 | dear brother as he fights... |
| 0x31011b | 21 | Just watching... huh? |
| 0x310131 | 39 | Would you... not even allow me that...? |
| 0x310159 | 45 | Of course I can't--is what I'd like to tell\n |
| 0x310187 | 6 | her... |
| 0x31018e | 45 | But she'd probably go berserk if I outright\n |
| 0x3101bc | 43 | denied her. Gah, Oshtor's not going to be\n |
| 0x3101e8 | 8 | happy... |
| 0x3101f1 | 45 | *Sigh*...Fine. If you promise you'll stay a\n |
| 0x31021f | 41 | safe distance away. And only watch. You\n |
| 0x310249 | 8 | promise? |
| 0x310252 | 24 | Can you promise me that? |
| 0x31026b | 31 | Y-Yes, I promise, I will do so! |
| 0x31028b | 42 | Let's go. And remember, a safe distance.\n |
| 0x3102b6 | 33 | Make sure not to make any sounds. |
| 0x3102d8 | 15 | I-I understand! |
| 0x3102e8 | 47 | Nekone bows deeply, tears of gratitude in her\n |
| 0x310318 | 5 | eyes. |
| 0x31031e | 46 | Geez. If only she'd act this lovable all the\n |
| 0x31034d | 5 | time. |
| 0x310353 | 14 | Dear brother-- |
| 0x310362 | 46 | You idiot! I thought I told you you can't go\n |
| 0x310391 | 10 | out there! |
| 0x31039c | 4 | Ah!? |
| 0x3103a1 | 24 | Wh-What was that for...? |
| 0x3103ba | 47 | What, you're gonna break the promise you made\n |
| 0x3103ea | 48 | a minute after you made it!? You can only watch. |
| 0x31041b | 7 | Urgh... |
| 0x310423 | 44 | Just don't get in Oshtor's way. He's coming. |
| 0x310450 | 9 | OSHTOR... |
| 0x31045a | 24 | YOU DARED SHOW ME MERCY. |
| 0x310473 | 30 | YOU WOULD HAVE KNOWN EASILY.\n |
| 0x310492 | 39 | YOU COULD SEE THAT I STILL DREW BREATH. |
| 0x3104ba | 36 | YET YOU CHOSE TO LEAVE ME, WITHOUT\n |
| 0x3104df | 30 | DELIVERING THE KILLING BLOW... |
| 0x3104fe | 23 | I SEE. SO IT IS TRUE... |
| 0x310516 | 35 | YOU SULLY MY HONOR AS A MONONOFU,\n |
| 0x31053a | 33 | AND FORCE IMMORTAL SHAME UPON ME. |
| 0x31055c | 17 | UNFORGIVABLE...\n |
| 0x31056e | 21 | THAT IS UNFORGIVABLE! |
| 0x310584 | 32 | YOU SHALL PAY FOR YOUR MOCKERY\n |
| 0x3105a5 | 15 | WITH YOUR HEAD! |
| 0x3105b5 | 41 | So you would value your honor over your\n |
| 0x3105df | 5 | life? |
| 0x3105e5 | 42 | THIS STRENGTH WAS GRANTED BY THE MIKADO.\n |
| 0x310610 | 42 | DEFEAT IS NOT AN OPTION. MY POWER CANNOT\n |
| 0x31063b | 14 | BE TAINTED SO! |
| 0x31064a | 44 | THE DAY I LIE DEFEATED IS THE DAY MY LIMBS\n |
| 0x310677 | 41 | ARE TORN FROM MY BODY, AND MY VERY SOUL\n |
| 0x3106a1 | 12 | OBLITERATED! |
| 0x3106ae | 43 | AND YOU WILL NEVER CONVINCE ME OTHERWISE,\n |
| 0x3106da | 8 | OSHTOR!! |
| 0x3106e3 | 45 | ...Then I will apologize for having tainted\n |
| 0x310711 | 41 | your honor. It was my own weakness that\n |
| 0x31073b | 15 | stayed my hand. |
| 0x31074b | 40 | And it is my weakness that led to this\n |
| 0x310774 | 20 | confrontation today. |
| 0x310789 | 49 | However, I am afraid I cannot let you have this\n |
| 0x3107bb | 13 | head of mine. |
| 0x3107c9 | 46 | Akuruka, open thy gates and guide my path to\n |
| 0x3107f8 | 18 | the primal origin! |
| 0x31080b | 33 | I HAVE PROMISED A FRIEND THAT I\n |
| 0x31082d | 31 | SHALL RETURN... NO MATTER WHAT! |
| 0x31084d | 22 | RRRRAAAAAAAAAAAAAAAH!! |
| 0x310864 | 22 | HAAAAAAAAAAAAAAAHHHH!! |
| 0x31087b | 14 | Dear brother!! |
| 0x31088a | 19 | Urgh... Hold on...! |
| 0x31089e | 49 | This has to be some kind of joke. What the hell\n |
| 0x3108d0 | 47 | is this force!? I never imagined it'd be this\n |
| 0x310900 | 9 | strong... |
| 0x31090a | 48 | Oshtor's right. No normal person would be able\n |
| 0x31093b | 29 | to force their way past that. |
| 0x310959 | 43 | I thought I understood, but I had no idea\n |
| 0x310985 | 31 | what it would really be like... |
| 0x3109a5 | 5 | GAH-- |
| 0x3109ab | 14 | SUCH WEAKNESS! |
| 0x3109ba | 29 | Oshtor's being overpowered... |
| 0x3109d8 | 46 | He could barely walk. Fighting in that state\n |
| 0x310a07 | 34 | was far more than he could take... |
| 0x310a2a | 45 | Oshtor, this better not be some martyr shit\n |
| 0x310a58 | 22 | just to buy us time... |
| 0x310a6f | 44 | If you're planning on breaking the promise\n |
| 0x310a9c | 9 | we made-- |
| 0x310aa6 | 44 | ...No, this is Oshtor we're talking about.\n |
| 0x310ad3 | 46 | He's probably waiting for the perfect chance\n |
| 0x310b02 | 10 | to strike. |
| 0x310b0d | 41 | He just needs that one hit to end this... |
| 0x310b37 | 40 | IS THAT ALL, OSHTOR? WOULD YOU HAVE ME\n |
| 0x310b60 | 41 | BELIEVE YOUR WOUNDS ARE HOLDING YOU BACK? |
| 0x310b8a | 45 | THIS IS WAR. AND ONE CAN NEVER STAND IN WAR\n |
| 0x310bb8 | 10 | UNSCATHED. |
| 0x310bc3 | 41 | RISE, OSHTOR. OUR DUEL TO THE DEATH HAS\n |
| 0x310bed | 16 | ONLY JUST BEGUN! |
| 0x310bfe | 5 | GAH!? |
| 0x310c04 | 15 | HAAAAAAAHHHHH!! |
| 0x310c14 | 45 | YES, THIS IS IT! THIS IS WHAT I SO HUNGERED\n |
| 0x310c42 | 5 | FOR!! |
| 0x310c48 | 45 | AKURUKA, I REQUIRE MORE! FEAST THOU UPON MY\n |
| 0x310c76 | 43 | SOUL, AND SHOW ME POWER THAT SURPASSES ALL! |
| 0x310ca2 | 15 | GHH... NGAH...? |
| 0x310cb2 | 13 | FALL, VURAI!! |
| 0x310cc0 | 23 | NGH... GAAAAAAAAHHHHH!! |
| 0x310cd8 | 15 | RGH!? NNGH...!! |
| 0x310ce8 | 7 | GOOD... |
| 0x310cf0 | 21 | BUT NOT GOOD ENOUGH!! |
| 0x310d06 | 38 | YOU ARE WEAK! WEAK! WEAK! WEAK! WEAK!! |
| 0x310d2d | 14 | GAH... RRGH... |
| 0x310d3c | 32 | POWER! AKURUKA, GIVE ME POWER!\n |
| 0x310d5d | 37 | DEVOUR MY SOUL, AND GRANT IN RETURN\n |
| 0x310d83 | 11 | THY POWER!! |
| 0x310d8f | 11 | wall_normal |
| 0x310d9c | 10 | wall_crack |
| 0x310da7 | 7 | GAAAH-- |
| 0x310daf | 29 | Oh... no... Dear brother...\n |
| 0x310dcd | 15 | dear brother... |
| 0x310ddd | 18 | THIS IS THE END... |
| 0x310df0 | 39 | OSHTOR. YOU WERE THE ONE MAN I SAW AS\n |
| 0x310e18 | 11 | MY EQUAL... |
| 0x310e24 | 44 | I WILL LEAVE THEM NO CORPSE TO SHAMELESSLY\n |
| 0x310e51 | 18 | FLAUNT AND DEFILE. |
| 0x310e64 | 43 | I GRANT YOU THIS ONE MERCY. RETURN TO THE\n |
| 0x310e90 | 37 | DUST FROM WHENCE YOU CAME... OSHTOR!! |
| 0x310eb6 | 5 | GUH!? |
| 0x310ebc | 6 | Wh--!? |
| 0x310ec3 | 12 | Ah... hh...? |
| 0x310ed0 | 29 | Nekone... what... have you... |
| 0x310eee | 31 | That would've finished him...\n |
| 0x310f0e | 16 | if it had hit... |
| 0x310f1f | 6 | *Gasp* |
| 0x310f26 | 14 | YOU... DARE... |
| 0x310f35 | 11 | Ah... ah... |
| 0x310f41 | 11 | YOU DARE... |
| 0x310f4d | 13 | Nekone, RUN!! |
| 0x310f5b | 20 | Ah... a-ah... nnh... |
| 0x310f70 | 39 | YOU DARE VIOLATE THIS DUEL BETWEEN MEN. |
| 0x310f98 | 21 | ACCURSED... CHILD!!\n |
| 0x310fae | 18 | RRRRRRAAAAAAAAGH!! |
| 0x310fc1 | 26 | Ah... dear... brother...\n |
| 0x310fdc | 19 | I am so... sorry... |
| 0x310ff0 | 50 | Goddammit! What is she... There's no way in hell\n |
| 0x311023 | 21 | she'll survive that-- |
| 0x311039 | 31 | Shit! Think... What do I do...? |
| 0x311059 | 47 | At the very least, I might be able to save her! |
| 0x311089 | 4 | Wh-- |
| 0x31108e | 13 | Osh... tor... |
| 0x31109c | 16 | Dear... brother? |
| 0x3110ad | 7 | GHHK... |
| 0x3110b5 | 19 | D-Dear brother...\n |
| 0x3110c9 | 9 | NOOOOOO!! |
| 0x3110d3 | 9 | What is-- |
| 0x3110dd | 24 | RRRGH... RRRRAAAAAAAHH!! |
| 0x3110f6 | 35 | GATES... THE GATES TO THE ORIGIN... |
| 0x31111a | 45 | GUIDE ME... GUIDE ME TO THE FURTHEST DEPTHS\n |
| 0x311148 | 14 | OF YOUR POWER! |
| 0x311157 | 29 | His wounds... are healing...? |
| 0x311175 | 10 | Amazing... |
| 0x311180 | 18 | HAAAAAAAAAAAHHHH!! |
| 0x311193 | 6 | GRAHH! |
| 0x31119a | 41 | IMPOSSIBLE. HOW CAN YOU EVEN MOVE AFTER\n |
| 0x3111c4 | 16 | SUCH A BLOW...!? |
| 0x3111d5 | 35 | HOW... HOW ARE YOU STILL ALIVE...!? |
| 0x3111f9 | 29 | HAAAAAAAHHHH... HRRRRAAAAGH!! |
| 0x311217 | 17 | GUH...! NNNGGHH!! |
| 0x311229 | 13 | IMPOSSIBLE... |
| 0x311237 | 21 | THIS IS IMPOSSIBLE... |
| 0x31124d | 20 | YOU OVERPOWER ME...? |
| 0x311262 | 45 | HOW... WHERE IS THIS STRENGTH COMING FROM...? |
| 0x311290 | 26 | NO... OSHTOR... YOU HAVE-- |
| 0x3112ab | 16 | VURAAAAAIIIIII!! |
| 0x3112bc | 8 | GHKHH... |
| 0x3112c5 | 9 | I HAVE... |
| 0x3112cf | 15 | I HAVE LOST...? |
| 0x3112df | 30 | NO, IT... IT CANNOT BE OVER.\n |
| 0x3112fe | 30 | I MUST NEVER BE... DEFEATED... |
| 0x31131d | 41 | WHY... WHY DOES MY BODY... NOT MOVE...?\n |
| 0x311347 | 14 | I CAN STILL... |
| 0x311356 | 13 | OSH... TOR... |
| 0x311364 | 19 | OSHTOOOOOOOORRRRR!! |
| 0x311378 | 10 | He... won? |
| 0x311383 | 17 | Nekone... Haku... |
| 0x311395 | 47 | Dammit, Oshtor... just had to scare me with a\n |
| 0x3113c5 | 48 | flashy finish. I was worried for a second there. |
| 0x3113f6 | 49 | But he looks perfectly fine after going through\n |
| 0x311428 | 46 | all that... Guess the Akuruturuka really are-- |
| 0x311457 | 5 | Ah... |
| 0x31145d | 25 | Hm? What's wrong, Nekone? |
| 0x311477 | 7 | Nngh... |
| 0x31147f | 29 | ...Legs still too shaky, huh? |
| 0x31149d | 35 | Ow. Ow! Stop hitting me with that-- |
| 0x3114c1 | 41 | Here, I'll help you up. You're going to\n |
| 0x3114eb | 14 | Oshtor, right? |
| 0x3114fa | 49 | Urgh... Fine, I will accept your help. But know\n |
| 0x31152c | 46 | that I am only doing it for my dear brother... |
| 0x31155b | 21 | Dear brother!! A-Ah-- |
| 0x311571 | 48 | Nekone tries to hurry to him, but she stumbles\n |
| 0x3115a2 | 23 | in her haste and falls. |
| 0x3115ba | 11 | Ha... ku... |
| 0x3115c6 | 11 | O-Oshtor... |
| 0x3115d2 | 31 | Stop, you're--you're injured... |
| 0x3115f2 | 43 | Do you remember... the day we first met...? |
| 0x31161e | 30 | What? What're you saying...?\n |
| 0x31163d | 47 | Look, we need to hurry and treat your wounds... |
| 0x31166d | 44 | If memory serves, we first fought together\n |
| 0x31169a | 38 | under circumstances similar to this.\n |
| 0x3116c1 | 27 | Back to back, at a cliff... |
| 0x3116dd | 49 | If I close my eyes, I can remember it as though\n |
| 0x31170f | 17 | it was yesterday. |
| 0x311721 | 47 | I don't know where all this is coming from...\n |
| 0x311751 | 28 | but now's not the time for-- |
| 0x31176e | 32 | ...Wait... He's not... bleeding? |
| 0x31178f | 48 | Oh... Oh, right. That's it. His wounds must be\n |
| 0x3117c0 | 29 | healing, like... like before. |
| 0x3117de | 42 | But then... what's all this white that's\n |
| 0x311809 | 22 | falling off of him...? |
| 0x311820 | 18 | D-Dear... brother? |
| 0x311833 | 21 | Oshtor... your leg... |
| 0x311849 | 36 | Why is... his leg... fading away...? |
| 0x31186e | 32 | You are... such a bizarre man... |
| 0x31188f | 43 | Always so carefree, never taking life too\n |
| 0x3118bb | 49 | seriously, looking for ways to get out of work... |
| 0x3118ed | 50 | But in times of greatest need, you always manage\n |
| 0x311920 | 27 | to figure out a solution... |
| 0x31193c | 49 | I cannot tell you how comforting it has been to\n |
| 0x31196e | 49 | have you at my side... a man like a warm ray of\n |
| 0x3119a0 | 10 | the sun... |
| 0x3119ab | 46 | You always had companions nearby, and before\n |
| 0x3119da | 48 | I knew it, your little group had grown quite a\n |
| 0x311a0b | 6 | lot... |
| 0x311a12 | 48 | It was my greatest pleasure to watch you grow,\n |
| 0x311a43 | 36 | day by day, into a skilled leader... |
| 0x311a68 | 34 | And the days I spent with you...\n |
| 0x311a8b | 23 | I truly did have fun... |
| 0x311aa3 | 26 | Yes... such fun, indeed... |
| 0x311abe | 32 | So that means... He's already... |
| 0x311adf | 47 | No... It cannot be... Dear brother, please...\n |
| 0x311b0f | 14 | This is not... |
| 0x311b1e | 34 | Heh. Please, do not cry... Nekone. |
| 0x311b41 | 48 | This is the fate that awaits us Akuruturuka...\n |
| 0x311b72 | 18 | I have no regrets. |
| 0x311b85 | 13 | No... no...!! |
| 0x311b93 | 16 | Oshtor, you're-- |
| 0x311ba4 | 41 | ...I leave Her Highness... in your hands. |
| 0x311bce | 28 | ...I'm counting on you, kid. |
| 0x311beb | 40 | Nekone, live on... and find happiness.\n |
| 0x311c14 | 47 | And keep the kid... out of trouble... for me... |
| 0x311c44 | 30 | AAAAAAAAAAAAAAHHHHHHHHHHHHHH!! |
| 0x311c63 | 25 | No! NOOOOOOOOOOOOOOOO!!\n |
| 0x311c7d | 42 | Dear brother!! Dear brother, please...!!\n |
| 0x311ca8 | 13 | AAAAAAHHHHH!! |
| 0x311cb6 | 9 | globalSRT |
| 0x311cc0 | 9 | GlobalSRT |
| 0x311cca | 6 | target |
| 0x311cd1 | 15 | env_DownArm_3_R |
| 0x311ce1 | 7 | env_jaw |
| 0x311ce9 | 20 | env_finger_index_3_R |
| 0x311cfe | 4 | face |
| 0x311d03 | 4 | body |
| 0x311d08 | 4 | hair |
| 0x311d0d | 20 | env_finger_index_1_R |
| 0x311d22 | 4 | Head |
| 0x311d27 | 8 | LeftFoot |
| 0x311d30 | 9 | RightFoot |
| 0x311d3a | 17 | LeftMiddleFinger2 |
| 0x311d4c | 18 | RightMiddleFinger2 |
| 0x311d5f | 17 | RightIndexFinger2 |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_11.json` com a forma:
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
