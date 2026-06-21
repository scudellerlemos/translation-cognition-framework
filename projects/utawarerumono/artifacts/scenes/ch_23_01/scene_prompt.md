# Cena ch_23_01 — pacote de traducao (492 linhas)

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
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kamunagi | Titulo | Kamunagi | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nakwan | Termo | Nakwan | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Raiko | Personagem | Raiko | manter_original | none |
| Shichirya | Personagem | Shichirya | manter_original | none |
| Soyankekur | Personagem | Soyankekur | manter_original | moderate |
| Tuskur | Local | Tuskur | manter_original | moderate |
| Ukon | Personagem | Ukon | manter_original | major |
| Uzurusha | Local | Uzurusha | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
| Woshis | Personagem | Woshis | manter_original | major |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `important...` -> `importante...` (Haku, 18_01)
- `In any case...` -> `Em todo caso...` (Haku, 18_01)
- `Yes?` -> `Sim?` (Yuuri, 16_05)
- `hall.` -> `corredor.` (Atuy, 16_01)
- `the throne.` -> `do trono.` (Narrador, 14_06)
- `...Huh?` -> `...Hein?` (Kuon, 11_01)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `Understood.` -> `Entendido.` (Ukon, 13_08)
- `...Oh?` -> `...Ah?` (Garota, 17_01)
- `question.` -> `meio injusta.` (Kuon, 11_02)
- `time.` -> `vez.` (Raurau, 18_01)
- `way.` -> `jeito.` (Atuy, 18_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Lord Oshtor...` -> `Lorde Oshtor...` (Transeunte, 14_10)
- `Hm...?` -> `Hum...?` (Kuon, 11_02)
- `Wh-What...?` -> `Q-Que...?` (Nekone, 14_04)
- `me.` -> `mim.` (Garota, 17_01)
- `make things worse.` -> `piorar as coisas.` (Ukon, 20_07)
- `Ngh...` -> `Ngh...` (Haku, 11_01)
- `As you wish.` -> `Como desejar.` (Nekone, 14_04)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `of you.` -> `de você.` (Ukon, 13_01)
- `Hmmm...` -> `Hmmm...` (Garota, 19_08)
- `Yes, my liege.` -> `Sim, meu senhor.` (Oshtor, 21_01)
- `army.` -> `exército.` (Homem, 22_08)
- `option.` -> `opção.` (Rulutieh, 19_05)
- `immediately.` -> `na hora.` (Haku, 14_04)
- `What...?` -> `O quê...?` (Protagonista, 11_01)
- `Oh...?` -> `Oh...?` (Homem, 14_09)
- `circumstances.` -> `circunstâncias.` (Nekone, 22_08)
- `land.` -> `terra.` (Maroro, 20_11)
- `to you.` -> `com você.` (Ukon, 13_02)
- `Lord Oshtor.` -> `Lorde Oshtor.` (Ukon, 15_05)
- `Rrrgh...` -> `Agh...` (Kuon, 18_01)
- `again.` -> `vez.` (Ougi, 13_05)
- `say.` -> `dizer.` (Garota, 22_08)
- `task.` -> `tarefa.` (Nekone, 22_08)
- `Very well.` -> `Sim.` (Nekone, 15_01)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `...Hm?` -> `...Hum?` (Haku, 11_01)
- `Gah!?` -> `Ai!?` (Haku, 13_01)
- `alone.` -> `...Tem razão.` (Haku, 22_03)
- `for a while...` -> `por um tempo...` (Maroro, 20_01)
- `before...?` -> `antes...?` (Haku, 18_01)
- `that guy.` -> `esse cara.` (Haku, 15_02)
- `sir.` -> `senhor.` (Haku, 18_01)
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
| 0x271d39 | 6 | How... |
| 0x271d40 | 45 | I have no idea how things ended up like this. |
| 0x271d6e | 48 | As per usual, Ukon asked to see me, and I left\n |
| 0x271d9f | 16 | for his manor... |
| 0x271db0 | 50 | But it was Oshtor waiting for me. And he dragged\n |
| 0x271de3 | 36 | me all the way to the throne hall... |
| 0x271e08 | 46 | What the hell am I doing in a place like this? |
| 0x271e37 | 47 | I feel like every time I've come here so far,\n |
| 0x271e67 | 42 | it's been related to something extremely\n |
| 0x271e92 | 12 | important... |
| 0x271e9f | 50 | And just as I expected, I look around to see all\n |
| 0x271ed2 | 39 | the bigwigs of Yamato lining the place. |
| 0x271efa | 19 | Oshtor on one side. |
| 0x271f0e | 23 | Mikazuchi on the other. |
| 0x271f26 | 39 | Munechika, standing a little ways away. |
| 0x271f4e | 46 | And that giant... Vurai, I think? One of the\n |
| 0x271f7d | 38 | bearers of the Akuruka, like Oshtor... |
| 0x271fa4 | 49 | And that skinny guy over there's Woshis... He's\n |
| 0x271fd6 | 48 | the one who keeps the Eight Pillar Generals in\n |
| 0x272007 | 5 | line. |
| 0x27200d | 49 | And over there is Mikazuchi's brother, Raiko...\n |
| 0x27203f | 48 | the undefeated general, if I remember correctly. |
| 0x272070 | 46 | ...Great. He's here too. Talk about a cliche\n |
| 0x27209f | 28 | corrupt government official. |
| 0x2720bc | 47 | In a weird way, though, it's kind of a relief\n |
| 0x2720ec | 48 | to see him. He's easier to read than the others. |
| 0x27211d | 14 | In any case... |
| 0x27212c | 48 | All the government and military officials I've\n |
| 0x27215d | 39 | glimpsed within the court are all here. |
| 0x272185 | 39 | It's quite the distinguished gathering. |
| 0x2721ad | 46 | And a civilian like me... definitely doesn't\n |
| 0x2721dc | 12 | belong here. |
| 0x2721e9 | 14 | Hey... Oshtor. |
| 0x2721f8 | 4 | Yes? |
| 0x2721fd | 46 | Why exactly am I here? It's pretty obvious I\n |
| 0x27222c | 29 | don't fit in with this crowd. |
| 0x27224a | 46 | You were summoned here by direct order of my\n |
| 0x272279 | 46 | liege. You belong here without question, Haku. |
| 0x2722a8 | 47 | What!? Bro, what the hell are you thinking...!? |
| 0x2722d8 | 46 | He was talking about having me "succeed" him\n |
| 0x272307 | 34 | and all, but is this part of that? |
| 0x27232a | 44 | He better not be planning on revealing our\n |
| 0x272357 | 35 | relationship to all these people... |
| 0x27237b | 8 | Official |
| 0x272384 | 16 | Who is that man? |
| 0x272395 | 39 | The face is not one I've seen before... |
| 0x2723bd | 46 | What is a man like that doing in our midst...? |
| 0x2723ec | 46 | The curious gazes of the officials around us\n |
| 0x27241b | 28 | are all concentrating on me. |
| 0x272438 | 48 | It's like sleeping on a bed of nails. Why does\n |
| 0x272469 | 39 | this kind of stuff always happen to me? |
| 0x272491 | 49 | I don't know what this is all about, but I just\n |
| 0x2724c3 | 28 | want to go home and sleep... |
| 0x2724e0 | 47 | As I stand there thinking to myself, I notice\n |
| 0x272510 | 31 | the hall's suddenly gone quiet. |
| 0x272530 | 9 | He comes. |
| 0x27253a | 21 | Our liege now enters! |
| 0x272550 | 45 | The austere bamboo blinds open up to reveal\n |
| 0x27257e | 37 | a man in an extravagant wheelchair.\n |
| 0x2725a4 | 23 | The Mikado--my brother. |
| 0x2725bc | 47 | Beside him is Honoka, followed by a number of\n |
| 0x2725ec | 13 | court ladies. |
| 0x2725fa | 28 | You may all lift your heads. |
| 0x272617 | 45 | At Honoka's voice, all the retainers within\n |
| 0x272645 | 34 | the hall humbly raise their heads. |
| 0x272668 | 45 | The Mikado lazily casts his eyes across the\n |
| 0x272696 | 5 | hall. |
| 0x27269c | 47 | Your valor in the previous war was commendable. |
| 0x2726cc | 48 | Those Uzurushans have now surely learned their\n |
| 0x2726fd | 37 | place, and will trouble us no longer. |
| 0x272723 | 48 | We need no such praise. We hone our skills for\n |
| 0x272754 | 47 | your use, my liege. We conquer all who oppose\n |
| 0x272784 | 11 | the throne. |
| 0x272790 | 47 | Good. The recent past has given me much cause\n |
| 0x2727c0 | 47 | to rethink my philosophy on the governance of\n |
| 0x2727f0 | 13 | this country. |
| 0x2727fe | 48 | I have concluded that sitting idle and content\n |
| 0x27282f | 40 | on this land will not bring us further\n |
| 0x272858 | 11 | prosperity. |
| 0x272864 | 46 | That is why... I have chosen to continue our\n |
| 0x272893 | 12 | path onward. |
| 0x2728a0 | 7 | ...Huh? |
| 0x2728a8 | 45 | The time has come for Yamato to commence an\n |
| 0x2728d6 | 25 | attack on a foreign land. |
| 0x2728f0 | 38 | We shall begin our invasion of Tuskur. |
| 0x27291a | 46 | So, the time has finally come to set foot in\n |
| 0x272949 | 12 | that land... |
| 0x272956 | 47 | Very well... I shall annihilate all who stand\n |
| 0x272986 | 11 | in our way. |
| 0x272992 | 17 | ...Invade Tuskur? |
| 0x2729a4 | 41 | Wait, why!? Didn't they just send their\n |
| 0x2729ce | 17 | ambassadors here? |
| 0x2729e0 | 44 | Did they start something...? No, can't be.\n |
| 0x272a0d | 37 | I haven't heard anything of the sort. |
| 0x272a33 | 45 | So this invasion is... completely unprovoked? |
| 0x272a61 | 45 | Bro, why are you doing this...? And what am\n |
| 0x272a8f | 21 | I going to tell Kuon? |
| 0x272aa5 | 7 | Oshtor. |
| 0x272aad | 9 | My liege. |
| 0x272ab7 | 41 | I would hear your opinion on this matter. |
| 0x272ae1 | 48 | The hall suddenly fills with restless murmuring. |
| 0x272b16 | 11 | Nyurrrgh... |
| 0x272b22 | 42 | It's clear the other generals are upset.\n |
| 0x272b4d | 46 | They can't understand why Oshtor was chosen,\n |
| 0x272b7c | 13 | and not them. |
| 0x272b8a | 11 | Understood. |
| 0x272b96 | 37 | Oshtor bows as all eyes focus on him. |
| 0x272bbc | 49 | It pains me to say... that I must disagree with\n |
| 0x272bee | 14 | you, my liege. |
| 0x272bfd | 6 | ...Oh? |
| 0x272c04 | 43 | The air in the hall freezes at these words. |
| 0x272c30 | 47 | It has been mere days since Yamato peacefully\n |
| 0x272c60 | 42 | welcomed ambassadors from the country in\n |
| 0x272c8b | 9 | question. |
| 0x272c95 | 47 | The two kamunagi wished for peace between our\n |
| 0x272cc5 | 47 | nations. We have the chance to forge a strong\n |
| 0x272cf5 | 9 | alliance. |
| 0x272cff | 47 | What is more, the invasion would require that\n |
| 0x272d2f | 47 | we cross the sea, costing ample resources and\n |
| 0x272d5f | 5 | time. |
| 0x272d65 | 49 | Even should we claim victory, their differences\n |
| 0x272d97 | 46 | in ideology would cause unrest in occupation\n |
| 0x272dc6 | 15 | and governance. |
| 0x272dd6 | 49 | I ask that you please reconsider your decision,\n |
| 0x272e08 | 9 | my liege. |
| 0x272e12 | 45 | The surrounding murmur raises in volume and\n |
| 0x272e40 | 18 | indignant outrage. |
| 0x272e53 | 50 | Oshtor's argument is a reasonable one, but those\n |
| 0x272e86 | 46 | in the hall don't seem to have taken it that\n |
| 0x272eb5 | 4 | way. |
| 0x272eba | 5 | Hm... |
| 0x272ec0 | 50 | S-Silence that impudent tongue of yours, Oshtor!\n |
| 0x272ef3 | 42 | How dare you talk to our liege with such\n |
| 0x272f1e | 10 | audacity!? |
| 0x272f29 | 33 | Bold of him. A bold move, indeed. |
| 0x272f4b | 14 | Lord Oshtor... |
| 0x272f5a | 25 | Mikazuchi remains silent. |
| 0x272f74 | 47 | Munechika seems to want to say something, but\n |
| 0x272fa4 | 41 | she can't seem to gather the right words. |
| 0x272fce | 45 | This isn't good... Nobody's on our side for\n |
| 0x272ffc | 9 | this one. |
| 0x273006 | 45 | Control yourselves. You are in the presence\n |
| 0x273034 | 13 | of our ruler. |
| 0x273042 | 10 | Hm. I see. |
| 0x27304d | 46 | And what about you? What do you think... Haku? |
| 0x27307c | 48 | I'm caught completely by surprise. For several\n |
| 0x2730ad | 41 | seconds, I just stand there, dumbfounded. |
| 0x2730d7 | 46 | I would hear your perspective on the matter.\n |
| 0x273106 | 14 | You may speak. |
| 0x273115 | 37 | For some reason, he turns to me next. |
| 0x27313b | 27 | I feel all eyes turn to me. |
| 0x273157 | 42 | DAMMIT, MAN! What the hell are you DOING!? |
| 0x273182 | 6 | Hm...? |
| 0x273189 | 11 | Wh-What...? |
| 0x273195 | 46 | All besides Oshtor, Munechika, and Mikazuchi\n |
| 0x2731c4 | 48 | stare, as if unable to believe what's happening. |
| 0x2731f5 | 42 | Believe me, I'm with you guys on this one. |
| 0x273220 | 46 | This is how anyone would react if the Mikado\n |
| 0x27324f | 45 | suddenly asked some random nobody for their\n |
| 0x27327d | 8 | opinion. |
| 0x273286 | 49 | I can feel countless piercing gazes boring into\n |
| 0x2732b8 | 3 | me. |
| 0x2732bc | 45 | Surprise, confusion, curiosity... Among the\n |
| 0x2732ea | 48 | emotions in their gazes, I also sense anger...\n |
| 0x27331b | 12 | even enmity. |
| 0x273328 | 48 | Gimme a break. I've attracted enough attention\n |
| 0x273359 | 46 | from just being here. What are you thinking,\n |
| 0x273388 | 4 | man? |
| 0x27338d | 46 | But standing there silently is just going to\n |
| 0x2733bc | 18 | make things worse. |
| 0x2733cf | 45 | I should probably give my honest opinion in\n |
| 0x2733fd | 10 | this case. |
| 0x273408 | 39 | I... agree with what Oshtor has to say. |
| 0x273430 | 23 | *Murmur*... *Rumble*... |
| 0x273448 | 40 | So, you too would defy our liege's will. |
| 0x273471 | 45 | Gah, this guy's scaring the shit out of me... |
| 0x27349f | 41 | I wouldn't say defying. I just answered\n |
| 0x2734c9 | 42 | honestly, since he asked for my opinion... |
| 0x2734f4 | 37 | And who permitted your presence here? |
| 0x27351a | 48 | A worm like you is unfit to even exist in such\n |
| 0x27354b | 8 | a place. |
| 0x273554 | 47 | Yeah, you definitely have a point, but "worm"\n |
| 0x273584 | 20 | might be a bit much. |
| 0x273599 | 28 | Lord Vurai, you will desist. |
| 0x2735b6 | 47 | Lord Haku has been granted leave by our liege\n |
| 0x2735e6 | 43 | to be present here as Oshtor's subordinate. |
| 0x273612 | 45 | If you would question his presence, that is\n |
| 0x273640 | 48 | tantamount to questioning the will of our liege. |
| 0x273671 | 6 | Ngh... |
| 0x273678 | 52 | It was I who gave him permission. Stand down, Vurai. |
| 0x2736ad | 12 | As you wish. |
| 0x2736ba | 47 | The giant man gives a deep bow to the Mikado,\n |
| 0x2736ea | 23 | and backs down from me. |
| 0x273702 | 45 | You could cut the tension in the air with a\n |
| 0x273730 | 8 | knife... |
| 0x273739 | 17 | Oshtor, and Haku. |
| 0x27374b | 23 | Your argument is sound. |
| 0x273763 | 48 | Your conclusions are only natural when viewing\n |
| 0x273794 | 42 | this situation in a more objective manner. |
| 0x2737bf | 44 | Thank you, my liege. I do not deserve such\n |
| 0x2737ec | 7 | praise. |
| 0x2737f4 | 11 | Nyerrrgh... |
| 0x273800 | 47 | Truly, the kamunagi of Tuskur were persons of\n |
| 0x273830 | 47 | great character, as leaders and as individuals. |
| 0x273860 | 48 | As you said, Oshtor, we might have established\n |
| 0x273891 | 46 | a lasting and fruitful relationship with them. |
| 0x2738c0 | 41 | However... my decision remains unchanged. |
| 0x2738ea | 7 | Wha--!? |
| 0x2738f2 | 15 | ...As you wish. |
| 0x273902 | 19 | Oshtor, what're y-- |
| 0x273916 | 10 | Lord Haku. |
| 0x273921 | 50 | Oshtor halts me with one raised hand, and I have\n |
| 0x273954 | 29 | no choice but to keep silent. |
| 0x273972 | 31 | There is no further opposition? |
| 0x273992 | 49 | Your will is our command, my liege. There shall\n |
| 0x2739c4 | 35 | be none that question your command. |
| 0x2739e8 | 49 | Good. Then our next task would be to decide who\n |
| 0x273a1a | 20 | to send to Tuskur... |
| 0x273a2f | 46 | Nya-HA! If that is the case, then please let-- |
| 0x273a5e | 7 | Nyegh!? |
| 0x273a66 | 48 | As the pudgy man begins to waddle forward, one\n |
| 0x273a97 | 42 | glare from Vurai immediately shuts him up. |
| 0x273ac2 | 47 | My liege. Please allow me to execute this task. |
| 0x273af2 | 47 | My annihilation of Tuskur's feeble army shall\n |
| 0x273b22 | 24 | be swift and inevitable. |
| 0x273b3b | 42 | The grim smile on Vurai's face is almost\n |
| 0x273b66 | 35 | predatory as he clenches his fists. |
| 0x273b8a | 49 | Please, my liege, a moment. My sources say that\n |
| 0x273bbc | 48 | Tuskur's military is well-trained and organized. |
| 0x273bed | 46 | A mere show of brute force will not bring us\n |
| 0x273c1c | 46 | victory. If it please you, allow me the honor. |
| 0x273c4b | 49 | Be silent, Raiko. I need no help from the likes\n |
| 0x273c7d | 7 | of you. |
| 0x273c85 | 44 | Help? Perhaps you misunderstand me, Vurai.\n |
| 0x273cb2 | 43 | Allow me to clarify: I shall succeed alone. |
| 0x273cde | 47 | And what do you hope to accomplish with those\n |
| 0x273d0e | 40 | frail scribe's-arms? Stay out of my way. |
| 0x273d37 | 43 | Hmph. However one may pride their martial\n |
| 0x273d63 | 46 | ability, brute strength does not command the\n |
| 0x273d92 | 12 | battlefield. |
| 0x273d9f | 32 | What is your decision, my liege? |
| 0x273dc0 | 7 | Hmmm... |
| 0x273dc8 | 39 | Woshis, please present your assessment. |
| 0x273df0 | 14 | Yes, my liege. |
| 0x273dff | 28 | My humble opinion is that... |
| 0x273e1c | 49 | To begin with, we must secure Lord Soyankekur's\n |
| 0x273e4e | 42 | aid in order to cross the ocean to Tuskur. |
| 0x273e79 | 48 | There exists a path by land, but its viability\n |
| 0x273eaa | 49 | varies with the tide. It will not serve a large\n |
| 0x273edc | 5 | army. |
| 0x273ee2 | 46 | Thus, a sea route would prove the far better\n |
| 0x273f11 | 7 | option. |
| 0x273f19 | 34 | Mm. Send word to Soyankekur, then. |
| 0x273f3c | 46 | Yes, my liege. The arrangements will be made\n |
| 0x273f6b | 12 | immediately. |
| 0x273f78 | 13 | And the rest? |
| 0x273f86 | 46 | Just as the generals seem ready to say their\n |
| 0x273fb5 | 47 | pieces again, Woshis interrupts with his calm\n |
| 0x273fe5 | 8 | counsel. |
| 0x273fee | 50 | I would nominate Lord Raiko, Lord Dekopompo, and\n |
| 0x274021 | 29 | Lady Munechika for this task. |
| 0x27403f | 8 | What...? |
| 0x274048 | 6 | Oh...? |
| 0x27404f | 47 | I would appoint Lord Raiko as marshal of this\n |
| 0x27407f | 9 | campaign. |
| 0x274089 | 47 | As we must cross the ocean for this invasion,\n |
| 0x2740b9 | 40 | our numbers will necessarily be limited. |
| 0x2740e2 | 46 | Moreover, Tuskur would have the advantage of\n |
| 0x274111 | 46 | terrain. Lord Raiko would be perfectly suited. |
| 0x274140 | 46 | And Lord Dekopompo shall serve as our offense. |
| 0x27416f | 49 | In the previous war, he... was able to turn the\n |
| 0x2741a1 | 38 | tides when faced with extremely dire\n |
| 0x2741c8 | 14 | circumstances. |
| 0x2741d7 | 48 | I know he will be more than capable of meeting\n |
| 0x274208 | 40 | your expectations in this war, my liege. |
| 0x274231 | 46 | Wasn't Dekopompo the one who dumped his army\n |
| 0x274260 | 45 | into such "dire circumstances" in the first\n |
| 0x27428e | 6 | place? |
| 0x274295 | 50 | And I thought I heard Mikazuchi was the one that\n |
| 0x2742c8 | 36 | made it just in time to save them... |
| 0x2742ed | 46 | I guess he's trying to gloss over that part,\n |
| 0x27431c | 30 | so Dekopompo gets some credit. |
| 0x27433b | 27 | H-Hmhmhm... Very well then. |
| 0x274357 | 29 | You may leave it in my hands! |
| 0x274375 | 44 | Dekopompo energetically puffs his chest out. |
| 0x2743a2 | 46 | I get it... Woshis is giving him a chance to\n |
| 0x2743d1 | 44 | redeem himself, in a way that doesn't hurt\n |
| 0x2743fe | 10 | his pride. |
| 0x274409 | 47 | And certainly, I believe Lady Munechika would\n |
| 0x274439 | 38 | be the obvious choice for our defense. |
| 0x274460 | 49 | I am sure she will fight in a fashion befitting\n |
| 0x274492 | 40 | one bestowed with the title of Guardian. |
| 0x2744bb | 12 | Lord Woshis. |
| 0x2744c8 | 48 | It is my responsibility to defend the imperial\n |
| 0x2744f9 | 44 | capital with my life, should the need ever\n |
| 0x274526 | 6 | arise. |
| 0x27452d | 49 | This duty was granted me by our liege, and must\n |
| 0x27455f | 44 | be held over all else. I cannot leave this\n |
| 0x27458c | 5 | land. |
| 0x274592 | 47 | Yet the invasion of Tuskur is the will of our\n |
| 0x2745c2 | 15 | liege, as well. |
| 0x2745d2 | 42 | Our liege's desires are our own desires.\n |
| 0x2745fd | 15 | Is this not so? |
| 0x27460d | 37 | Very well. I humbly accept this task. |
| 0x274633 | 49 | As Munechika bows her head, Woshis gives her an\n |
| 0x274665 | 16 | apologetic look. |
| 0x274676 | 47 | And in Lady Munechika's absence, Lord Oshtor,\n |
| 0x2746a6 | 50 | her duty of defending the imperial capital falls\n |
| 0x2746d9 | 7 | to you. |
| 0x2746e1 | 14 | ...Understood. |
| 0x2746f0 | 42 | That is all. Lord Raiko as marshal, Lord\n |
| 0x27471b | 47 | Dekopompo for offense, and Lady Munechika for\n |
| 0x27474b | 10 | defense... |
| 0x274756 | 43 | These would be my nominations to lead the\n |
| 0x274782 | 19 | conquest of Tuskur. |
| 0x274796 | 14 | Hm. Very well. |
| 0x2747a5 | 13 | Hold, Woshis. |
| 0x2747b3 | 24 | You have some objection? |
| 0x2747cc | 26 | My name was not mentioned. |
| 0x2747e7 | 45 | ...Indeed not. Lord Vurai, I would have you\n |
| 0x274815 | 40 | protect the imperial capital alongside\n |
| 0x27483e | 12 | Lord Oshtor. |
| 0x27484b | 8 | Rrrgh... |
| 0x274854 | 45 | Vurai's eyes narrow at Woshis' curt response. |
| 0x274882 | 46 | Whoa, geez... Can he really talk to him like\n |
| 0x2748b1 | 39 | that? The guy looks ready to explode... |
| 0x2748d9 | 46 | I have read the reports from the campaign in\n |
| 0x274908 | 9 | Uzurusha. |
| 0x274912 | 48 | It would appear you dispatched a great many of\n |
| 0x274943 | 29 | the enemy forces on your own. |
| 0x274961 | 11 | What of it? |
| 0x27496d | 47 | It would also appear that a majority of those\n |
| 0x27499d | 24 | you killed were nakwans. |
| 0x2749b6 | 36 | ...What is it you are trying to say? |
| 0x2749db | 50 | As you may already know, the nakwans were forced\n |
| 0x274a0e | 49 | to fight after their families were taken hostage. |
| 0x274a40 | 43 | If you had eliminated the enemy commander\n |
| 0x274a6c | 46 | sooner, the nakwans may well have surrendered. |
| 0x274a9b | 44 | And much of this bloodshed could have been\n |
| 0x274ac8 | 8 | avoided. |
| 0x274ad1 | 48 | Laughable. You would have had me show mercy to\n |
| 0x274b02 | 24 | weaklings such as those? |
| 0x274b1b | 48 | Our upcoming campaign requires us to fight our\n |
| 0x274b4c | 34 | enemy in a wholly unfamiliar land. |
| 0x274b6f | 50 | It is imperative that we move according to plan,\n |
| 0x274ba2 | 32 | and maintain order in the ranks. |
| 0x274bc3 | 49 | But you have been observed to take far too much\n |
| 0x274bf5 | 33 | pleasure in the thrill of battle. |
| 0x274c17 | 9 | Woshis... |
| 0x274c21 | 49 | One might almost think you aim to say that I am\n |
| 0x274c53 | 12 | a liability. |
| 0x274c60 | 46 | All I mean to say is that each person is fit\n |
| 0x274c8f | 42 | for specific duties, and unfit for others. |
| 0x274cba | 9 | You DARE! |
| 0x274cc4 | 21 | Calm yourself, Vurai. |
| 0x274cda | 50 | Your might is a great asset to me. I promise you\n |
| 0x274d0d | 45 | that the day I need your strength will come\n |
| 0x274d3b | 6 | again. |
| 0x274d42 | 43 | Such words are wasted on the likes of me... |
| 0x274d6e | 48 | Thus do I ask you to stand down. Preserve that\n |
| 0x274d9f | 46 | strength, until the day comes when I require\n |
| 0x274dce | 9 | it again. |
| 0x274dd8 | 49 | Woshis' words seem harsh, but with the Mikado's\n |
| 0x274e0a | 49 | support behind them, there's not much Vurai can\n |
| 0x274e3c | 4 | say. |
| 0x274e41 | 49 | Although his reluctance is clear, Vurai finally\n |
| 0x274e73 | 32 | backs off, calm and stone-faced. |
| 0x274e94 | 42 | As for Lord Mikazuchi, I wish for you to\n |
| 0x274ebf | 49 | continue the eradication of remaining Uzurushan\n |
| 0x274ef1 | 11 | resistance. |
| 0x274efd | 47 | Mikazuchi's kept his silence through all this\n |
| 0x274f2d | 45 | chaos, but seems to have no qualms with his\n |
| 0x274f5b | 5 | task. |
| 0x274f61 | 10 | Very well. |
| 0x274f6c | 44 | That is his only response, along with a nod. |
| 0x274f99 | 49 | Woshis continues to instruct the government and\n |
| 0x274fcb | 35 | military officials lining the hall. |
| 0x274fef | 45 | Damn, he's good. He managed to organize all\n |
| 0x27501d | 43 | these temperamental individuals just like\n |
| 0x275049 | 5 | that. |
| 0x27504f | 47 | I'd have figured him to be much more helpless\n |
| 0x27507f | 40 | from his looks, but I guess I was wrong. |
| 0x2750a8 | 44 | The Mikado nods approvingly from his throne. |
| 0x2750d5 | 45 | Looks like that Woshis guy has my brother's\n |
| 0x275103 | 15 | complete trust. |
| 0x275113 | 47 | He's not skilled on the field like Oshtor and\n |
| 0x275143 | 51 | the rest, but I guess he's a master of all things\n |
| 0x275177 | 10 | political. |
| 0x275182 | 14 | Woshis, huh... |
| 0x275191 | 48 | The conference eventually comes to an end, and\n |
| 0x2751c2 | 42 | the officials begin filing out one by one. |
| 0x2751ed | 47 | To have a man of such questionable background\n |
| 0x27521d | 49 | as subordinate... Learn to temper your caprice,\n |
| 0x27524f | 44 | And you! I hope you do not forget that our\n |
| 0x27527c | 46 | liege's great magnanimity is the only reason\n |
| 0x2752ab | 12 | you're here. |
| 0x2752b8 | 15 | Sure. Whatever. |
| 0x2752c8 | 48 | As we leave, we're bombarded on all sides with\n |
| 0x2752f9 | 44 | harsh criticism. I keep my face polite and\n |
| 0x275326 | 6 | blank. |
| 0x27532d | 38 | I thank you for your words of caution. |
| 0x275354 | 45 | On the other hand, Oshtor turns to them and\n |
| 0x275382 | 30 | gives a grand bow in response. |
| 0x2753a1 | 44 | I guess he doesn't want to cause even more\n |
| 0x2753ce | 34 | trouble by retorting back at them. |
| 0x2753f1 | 48 | Well, he'd never have become an Imperial Guard\n |
| 0x275422 | 48 | if he couldn't do something as simple as this... |
| 0x275453 | 49 | In any case, no point in me staying in an awful\n |
| 0x275485 | 45 | place like this. I'd better get back to the\n |
| 0x2754b3 | 13 | Hakurokaku... |
| 0x2754c1 | 36 | But just as I'm thinking to myself-- |
| 0x2754e6 | 6 | ...Hm? |
| 0x2754ed | 31 | My vision goes completely dark. |
| 0x27550d | 46 | I look up to see what's going on, and find a\n |
| 0x27553c | 21 | giant wall before me. |
| 0x275552 | 44 | I'm pretty sure this path didn't lead to a\n |
| 0x27557f | 12 | dead end...? |
| 0x27558c | 5 | Gah!? |
| 0x275592 | 7 | Vurai!? |
| 0x27559a | 47 | Vurai looks down at me with cold, sharp eyes,\n |
| 0x2755ca | 39 | as though he's trying to intimidate me. |
| 0x2755f2 | 47 | I'm sure he could kill someone with his stare\n |
| 0x275622 | 6 | alone. |
| 0x275629 | 21 | Uh... Can I help you? |
| 0x27563f | 45 | It almost feels like he can't hear a single\n |
| 0x27566d | 12 | thing I say. |
| 0x27567a | 47 | Vurai stares at me and Oshtor in cold silence\n |
| 0x2756aa | 14 | for a while... |
| 0x2756b9 | 36 | And eventually, he turns and leaves. |
| 0x2756de | 42 | I can't help but let out a sigh of relief. |
| 0x275709 | 32 | H-Holy shit... that was scary... |
| 0x27572a | 47 | I am sorry. The fault is mine. Vurai does not\n |
| 0x27575a | 24 | think very highly of me. |
| 0x275773 | 45 | I once managed to tarnish his reputation as\n |
| 0x2757a1 | 41 | undefeated champion by besting him in a\n |
| 0x2757cb | 11 | tournament. |
| 0x2757d7 | 44 | It took all my cunning to outsmart him and\n |
| 0x275804 | 42 | claim victory, but he deemed my strategy\n |
| 0x27582f | 11 | despicable. |
| 0x27583b | 40 | A wry laugh escapes Oshtor as he speaks. |
| 0x275864 | 41 | Wait, he actually managed to beat Vurai\n |
| 0x27588e | 10 | before...? |
| 0x275899 | 28 | God. Oshtor's a monster too. |
| 0x2758b6 | 13 | Vurai, huh... |
| 0x2758c4 | 48 | All the generals besides Munechika seem pretty\n |
| 0x2758f5 | 47 | quirky, but I might never see eye to eye with\n |
| 0x275925 | 9 | that guy. |
| 0x27592f | 50 | You must not speak so. That man's loyalty to the\n |
| 0x275962 | 47 | Mikado is beyond reproach. None compare as an\n |
| 0x275992 | 5 | ally. |
| 0x275998 | 18 | As an ally... huh? |
| 0x2759ab | 47 | But it did look like he held a fair amount of\n |
| 0x2759db | 24 | animosity toward Oshtor. |
| 0x2759f4 | 45 | Guess the existence of my br--the Mikado is\n |
| 0x275a22 | 34 | absolute enough to unite them all. |
| 0x275a45 | 41 | I really don't want to be thrown in the\n |
| 0x275a6f | 44 | spotlight like that again... Come on, Bro,\n |
| 0x275a9c | 18 | give me a break... |
| 0x275aaf | 47 | Later that night, Raiko sits in a room within\n |
| 0x275adf | 28 | the palace, deep in thought. |
| 0x275afc | 22 | I do not understand... |
| 0x275b13 | 42 | Does something trouble you, Lord Raiko...? |
| 0x275b3e | 47 | Yes. This invasion of Tuskur... it feels much\n |
| 0x275b6e | 46 | too rushed. Why would our liege rush to such\n |
| 0x275b9d | 11 | a decision? |
| 0x275ba9 | 42 | What are your thoughts on this, Shichirya? |
| 0x275bd4 | 50 | ...I'm afraid I cannot say. Perhaps it is simply\n |
| 0x275c07 | 46 | beyond us to try to understand the mind of a\n |
| 0x275c36 | 6 | god... |
| 0x275c3d | 45 | Haha... Perhaps that is true. Even I do not\n |
| 0x275c6b | 23 | have an answer to that. |
| 0x275c83 | 47 | Perhaps our liege believes his prior military\n |
| 0x275cb3 | 52 | passivity is to blame for the Uzurushan invasion...? |
| 0x275ce8 | 25 | That was my first theory. |
| 0x275d02 | 44 | However, there was far too much amiss with\n |
| 0x275d2f | 40 | today's assembly. He is moving far too\n |
| 0x275d58 | 10 | quickly... |
| 0x275d63 | 46 | I can only assume that a new factor has been\n |
| 0x275d92 | 22 | added to the equation. |
| 0x275da9 | 16 | A... new factor? |
| 0x275dba | 43 | Yes. It may be appalling to say so... but\n |
| 0x275de6 | 48 | perhaps... our liege does not have much longer\n |
| 0x275e17 | 8 | to live. |
| 0x275e20 | 27 | Lord Raiko!? Such talk is-- |
| 0x275e3c | 49 | You believe it blasphemous? Yet if a new age is\n |
| 0x275e6e | 47 | dawning on this land, I will not sit idly by... |
| 0x275e9e | 10 | Shichirya. |
| 0x275ea9 | 4 | Sir. |
| 0x275eae | 46 | The time may soon come when I ask you to act\n |
| 0x275edd | 47 | where I cannot. Matters may shortly become...\n |
| 0x275f0d | 8 | chaotic. |
| 0x275f16 | 17 | As you command... |

## 8. Formato de saida EXIGIDO
Escreva `translations_23_01.json` com a forma:
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
