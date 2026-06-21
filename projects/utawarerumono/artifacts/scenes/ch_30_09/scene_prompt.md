# Cena ch_30_09 — pacote de traducao (761 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Cocopo | Criatura | Cocopo | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Ennakamuy | Local | Ennakamuy | manter_original | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Jachdwalt | Personagem | Jachdwalt | manter_original | moderate |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Ohn Riyaak | Local | Ohn Riyaak | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Raiko | Personagem | Raiko | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Shinonon | Personagem | Shinonon | manter_original | none |
| Uruuru | Personagem | Uruuru | manter_original | none |
| Uzurushan | Etnia | Uzurushan | manter_original | none |
| Vurai | Personagem | Vurai | manter_original | major |
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
- `Impressive, Master. You have earned a tip\n` -> `Impressionante, Mestre. Você merece uma\n` (Haku, 30_09)
- `of the hat.` -> `do chapéu.` (Haku, 30_09)
- `Now, on to the final chapter. We have brought\n` -> `Agora, ao capítulo final. Trouxemos\n` (Haku, 30_09)
- `a combatant suitable to be your final opponent.` -> `um combatente digno de ser seu oponente final.` (Haku, 30_09)
- `There's still MORE? Wait, just give me a sec\n` -> `Ainda tem MAIS? Espera, me dá um segundo\n` (Haku, 30_09)
- `to--` -> `para--` (Protagonist, 17_03)
- `Hm. These are bizarre circumstances indeed.` -> `Hm. Que circunstâncias incomuns, de fato.` (Munechika, 30_09)
- `Still... Hmhm. This does intrigue me somewhat.\n` -> `Ainda assim... Hmhm. Isso me intriga um pouco.\n` (Munechika, 30_09)
- `I always wished to have a match against you,\n` -> `Sempre desejei ter um duelo contra você,\n` (Munechika, 30_09)
- `Lord Haku.` -> `Senhor Haku.` (Oshtor, 23_01)
- `This has to be some kind of joke...` -> `Isso tem que ser algum tipo de brincadeira...` (Haku, 30_09)
- `I presume I need hold nothing back if this\n` -> `Presumo que não preciso me conter se isso\n` (Munechika, 30_09)
- `is a dream.` -> `é um sonho.` (Munechika, 30_09)
- `One of the Eight Pillar Generals... Munechika.` -> `Um dos Oito Generais-Pilar... Munechika.` (Munechika, 30_09)
- `I look forward to your fighting spirit as a\n` -> `Aguardo com expectativa seu espírito de luta como\n` (Munechika, 30_09)
- `man of Yamato, Lord Haku.` -> `homem de Yamato, Senhor Haku.` (Munechika, 30_09)
- `Shall we begin then...? I am Munechika\n` -> `Então começamos...? Sou Munechika\n` (Munechika, 30_09)
- `the Guardian! Prepare yourself!` -> `a Guardiã! Prepare-se!` (Munechika, 30_09)
- `Hmhm... Outplayed, it seems.` -> `Hmhm... Fui superada, ao que parece.` (Munechika, 30_09)
- `Impressive, Lord Haku... You truly are a\n` -> `Impressionante, Senhor Haku... Você é realmente um\n` (Munechika, 30_09)
- `man among men.` -> `homem entre homens.` (Munechika, 30_09)
- `I look forward to the day we may fight\n` -> `Aguardo o dia em que possamos lutar\n` (Munechika, 30_09)
- `side by side.` -> `lado a lado.` (Munechika, 30_09)
- `It's finally over... Geez, that was nearly it\n` -> `Finalmente acabou... Caramba, por pouco\n` (Haku, 30_09)
- `for me.` -> `espera.` (Kuon, 11_09)
- `Actually, it felt more like she let me win...` -> `Na verdade, parece que ela deixou eu ganhar...` (Haku, 30_09)
- `Whatever... I made it this far, all the same.\n` -> `Seja lá como for... cheguei até aqui, de qualquer jeito.\n` (Haku, 30_09)
- `I think I can allow myself a pat on the back.` -> `Acho que mereço me dar os parabéns.` (Haku, 30_09)
- `Your Highness... I am sorry...` -> `Sua Alteza... Eu sinto muito...` (Oshtor, 30_09)
- `polySurface24627` -> `polySurface24627` (, 30_09)
- `polySurface24628` -> `polySurface24628` (, 30_09)
- `polySurface24629` -> `polySurface24629` (, 30_09)
- `polySurface24630` -> `polySurface24630` (, 30_09)
- `polySurface2330` -> `polySurface2330` (, 30_09)
- `Nrrgh... hah.` -> `Nrrgh... hah.` (Vurai, 30_09)
- `Is this... blood...?` -> `Isso é... sangue...?` (Vurai, 30_09)
- `They managed to... wound me?\n` -> `Conseguiram me... ferir?\n` (Vurai, 30_09)
- `To bleed me... my own blood...?` -> `Me sangrar... meu próprio sangue...?` (Protagonista, 30_09)
- `...Very well. You are a worthy opponent.` -> `...Muito bem. Você é um oponente digno.` (Vurai, 30_09)
- `Here it comes--` -> `Lá vem--` (Haku, 30_09)
- `I was not expecting that you would be able to\n` -> `Não esperava que você fosse capaz de\n` (Vurai, 30_09)
- `harm me... I commend you.` -> `me machucar... Meus parabéns.` (Vurai, 30_09)
- `Then here is your reward!!` -> `Então aqui está sua recompensa!!` (Vurai, 30_09)
- `Witness the full extent of my power!` -> `Testemunhe o pleno alcance do meu poder!` (Vurai, 30_09)
- `Akuruka! Feast thou upon my soul, and bestow\n` -> `Akuruka! Alimenta-te da minha alma e me concede\n` (Vurai, 30_09)
- `upon me thy strength!!` -> `tua força!!` (Vurai, 30_09)
- `ORRRRRRRRRAAAAAAAAGGHHHHH!!` -> `ORRRRRRRRRAAAAAAAGHHHHH!!` (Vurai, 30_09)
- `WRRRRAAAAAAAAAAAAGGGHHH!!` -> `WRRRRAAAAAAAAAAAGGGHHH!!` (Vurai, 30_09)
- `Kuon!!` -> `Kuon!!` (Haku, 30_09)
- `I won't let you!` -> `Não vou deixar!` (Kuon, 30_09)
- `Nggh!?` -> `Nggh!?` (Vurai, 30_09)
- `He's stopped in his tracks--` -> `Ele foi detido na hora--` (Haku, 30_09)
- `Uruuru! Saraana!` -> `Uruuru! Saraana!` (Haku, 30_09)
- `①{W12}⑧{W12}...{W12}②{W12}⑥{W12}③{W12}⑤{W12}...{W12}④{W12}⑦{W12}...{W12}\n` -> `①{W12}⑧{W12}...{W12}②{W12}⑥{W12}③{W12}⑤{W12}...{W12}④{W12}⑦{W12}...{W12}\n` (Uruuru/Saraana, 30_09)
- `To the heroes of eld, from whose blood we\n` -> `Aos heróis de outrora, de cujo sangue\n` (Uruuru/Saraana, 30_09)
- `arose, we bow our heads.` -> `surgiu, curvamos a cabeça.` (Haku, 30_09)
- `⑨{W12}⑩{W12}...{W12}③{W12}④{W12}...{W12}②{W12}⑧{W12}...{W12}...{W12}\n` -> `⑨{W12}⑩{W12}...{W12}③{W12}④{W12}...{W12}②{W12}⑧{W12}...{W12}...{W12}\n` (Uruuru/Saraana, 30_09)
- `We plead your benevolence, your deliverance,\n` -> `Imploramos vossa benevolência, vossa libertação,\n` (Uruuru/Saraana, 30_09)
- `your protection.` -> `vossa proteção.` (Uruuru/Saraana, 30_09)
- `⑤{W12}⑧{W12}...{W12}⑥{W12}②{W12}⑦...{W12}⑩{W12}②{W12}①{W12}\n` -> `⑤{W12}⑧{W12}...{W12}⑥{W12}②{W12}⑦...{W12}⑩{W12}②{W12}①{W12}\n` (Uruuru/Saraana, 30_09)
- `Let your power unmasked ward all evils.\n` -> `Que vosso poder revelado afaste todos os males.\n` (Uruuru/Saraana, 30_09)
- `Grant us the peace and harmony that knows no end.` -> `Concedei-nos a paz e harmonia que nunca termina.` (Uruuru/Saraana, 30_09)
- `pPlane1` -> `pPlane1` (, 30_09)
- `pCylinder21` -> `pCylinder21` (, 30_09)
- `pCylinder22` -> `pCylinder22` (, 30_09)
- `pCylinder29` -> `pCylinder29` (, 30_09)
- `pCylinder30` -> `pCylinder30` (, 30_09)
- `pCylinder31` -> `pCylinder31` (, 30_09)
- `polySurface24641` -> `polySurface24641` (, 30_09)
- `polySurface24642` -> `polySurface24642` (, 30_09)
- `polySurface24643` -> `polySurface24643` (, 30_09)
- `polySurface24644` -> `polySurface24644` (, 30_09)
- `polySurface24645` -> `polySurface24645` (, 30_09)
- `pCylinder2` -> `pCylinder2` (, 30_09)
- `pCylinder18` -> `pCylinder18` (, 30_09)
- `pCylinder19` -> `pCylinder19` (, 30_09)
- `pCylinder20` -> `pCylinder20` (, 30_09)
- `pCylinder23` -> `pCylinder23` (, 30_09)
- `pCylinder24` -> `pCylinder24` (, 30_09)
- `pCylinder25` -> `pCylinder25` (, 30_09)
- `pCylinder26` -> `pCylinder26` (, 30_09)
- `pCylinder27` -> `pCylinder27` (, 30_09)
- `pCylinder28` -> `pCylinder28` (, 30_09)
- `pCylinder32` -> `pCylinder32` (, 30_09)
- `polySurface24632` -> `polySurface24632` (, 30_09)
- `polySurface24633` -> `polySurface24633` (, 30_09)
- `polySurface24634` -> `polySurface24634` (, 30_09)
- `polySurface24635` -> `polySurface24635` (, 30_09)
- `polySurface24636` -> `polySurface24636` (, 30_09)
- `polySurface24637` -> `polySurface24637` (, 30_09)
- `polySurface24638` -> `polySurface24638` (, 30_09)
- `polySurface24639` -> `polySurface24639` (, 30_09)
- `polySurface24640` -> `polySurface24640` (, 30_09)
- `polySurface24646` -> `polySurface24646` (, 30_09)
- `polySurface24647` -> `polySurface24647` (, 30_09)
- `Center_desk` -> `Center_desk` (, 30_09)
- `Center_desk1` -> `Center_desk1` (, 30_09)
- `polySurface2086` -> `polySurface2086` (, 30_09)
- `polySurface2087` -> `polySurface2087` (, 30_09)
- `pCube164` -> `pCube164` (, 30_09)
- `polySurface1985` -> `polySurface1985` (, 30_09)
- `polySurface1874` -> `polySurface1874` (, 30_09)
- `polySurface2124` -> `polySurface2124` (, 30_09)
- `polySurface2125` -> `polySurface2125` (, 30_09)
- `polySurface2126` -> `polySurface2126` (, 30_09)
- `fire024` -> `fire024` (, 30_09)
- `fire025` -> `fire025` (, 30_09)
- `fire026` -> `fire026` (, 30_09)
- `fire027` -> `fire027` (, 30_09)
- `fire028` -> `fire028` (, 30_09)
- `fire029` -> `fire029` (, 30_09)
- `fire030` -> `fire030` (, 30_09)
- `fire031` -> `fire031` (, 30_09)
- `fire032` -> `fire032` (, 30_09)
- `fire033` -> `fire033` (, 30_09)
- `fire034` -> `fire034` (, 30_09)
- `fire035` -> `fire035` (, 30_09)
- `fire036` -> `fire036` (, 30_09)
- `fire037` -> `fire037` (, 30_09)
- `fire038` -> `fire038` (, 30_09)
- `fire039` -> `fire039` (, 30_09)
- `polySurface24623` -> `polySurface24623` (, 30_09)
- `polySurface24624` -> `polySurface24624` (, 30_09)
- `polySurface24625` -> `polySurface24625` (, 30_09)
- `polySurface24590` -> `polySurface24590` (, 30_09)
- `polySurface24591` -> `polySurface24591` (, 30_09)
- `polySurface24593` -> `polySurface24593` (, 30_09)
- `polySurface24595` -> `polySurface24595` (, 30_09)
- `polySurface24597` -> `polySurface24597` (, 30_09)
- `target` -> `target` (SYSTEM, 20_11)
- `Ghhh... nghh...\n` -> `Ghhh... nghh...\n` (Vurai, 30_09)
- `GHAAAAAAAAHHHHHHH!?` -> `GHAAAAAAAAHHHHHH!?` (Vurai, 30_09)
- `What... is...?` -> `O que... é isso...?` (Vurai, 30_09)
- `Where there is a collar, so too there is\n` -> `Onde há uma coleira, há também\n` (Vurai, 30_09)
- `a leash.` -> `coleira.` (Haku, 30_09)
- `Did you truly believe the Akuruka would be\n` -> `Você realmente acreditou que a Akuruka seria\n` (Vurai, 30_09)
- `given freely without a way to control the\n` -> `dada livremente sem um meio de controlar a\n` (Vurai, 30_09)
- `raging beast?` -> `fera furiosa?` (Vurai, 30_09)
- `You two... Of course... You are that woman's...!\n` -> `Vocês duas... Claro... Vocês são daquela mulher...!\n` (Vurai, 30_09)
- `The GALL! So you were waiting for this,\n` -> `QUE AUDÁCIA! Então vocês estavam esperando por isso,\n` (Vurai, 30_09)
- `the whole time!` -> `o tempo todo!` (Vurai, 30_09)
- `But I... I will not be stopped by such tricks...` -> `Mas eu... não serei parado por tais truques...` (Vurai, 30_09)
- `We will not let you.` -> `Não vamos deixar.` (Uruuru/Saraana, 30_09)
- `Ngh.... NRRRRRRRRGGHH!!` -> `Ngh.... NRRRRRRRRGGHH!!` (Vurai, 30_09)
- `Gh... agh...!` -> `Gh... agh...!` (Vurai, 30_09)
- `Huh? What's wrong, Kuon?` -> `Hein? O que foi, Kuon?` (Haku, 30_09)
- `N-No, it's nothing... Just feeling a little\n` -> `N-Não, não é nada... Só fiquei um pouco\n` (Kuon, 30_09)
- `dizzy.` -> `tonta.` (Kuon, 30_09)
- `If you say so...` -> `Se você disser...` (Haku, 30_09)
- `It seems to work through a different system...\n` -> `Parece funcionar por um sistema diferente...\n` (Kuon, 30_09)
- `but this is definitely...` -> `mas isso é definitivamente...` (Kuon, 30_09)
- `The Ohn Riyaak!` -> `O Ohn Riyaak!` (Kuon, 30_09)
- `Ugh... gah...` -> `Ugh... gah...` (Kuon, 30_09)
- `A-Are you sure you're OK?\n` -> `V-Você tem certeza que está bem?\n` (Haku, 30_09)
- `You're turning pale!` -> `Você está ficando pálida!` (Haku, 30_09)
- `I'll... be fine... More importantly...\n` -> `Eu... vou ficar bem... Mais importante...\n` (Kuon, 30_09)
- `Now's our chance...` -> `É nossa chance agora...` (Kuon, 30_09)
- `We have to act, now!` -> `Temos que agir, agora!` (Kuon, 30_09)
- `Y-Yeah... got it! Come on, everyone!` -> `T-Tá... entendi! Vamos, todo mundo!` (Haku, 30_09)
- `Got it! Better put your back into this one,\n` -> `Entendido! Vai com tudo dessa vez,\n` (Nosuri, 30_09)
- `Kiwru!` -> `Kiwru!` (Nosuri, 30_09)
- `Right!` -> `Certo!` (Kiwru, 30_09)
- `Time to end this! On my mark, Ougi!` -> `Hora de acabar com isso! No meu sinal, Ougi!` (Nosuri, 30_09)
- `Ready when you are.` -> `Pronto quando você quiser.` (Ougi, 30_09)
- `Hrrrryaaaaaah!` -> `Hrrryaaaah!` (Nosuri, 30_09)
- `Rrraaaaah!!` -> `Rrraaaah!!` (Kiwru, 30_09)
- `Take this!` -> `Tome isso!` (Rulutieh, 19_04)
- `Haaaaaaaaaah!!` -> `Aaaaaaaah!!` (Oshtor, 20_20)
- `NGH...! N-NGHUUOOOOGH!!` -> `NGH...! N-NGHUUOOOOGH!!` (Vurai, 30_09)
- `Atuy, now!` -> `Atuy, agora!` (Haku, 30_09)
- `AhahahaHAHAHAHAHAHAHA!` -> `AhahahaHAHAHAHAHAHAHA!` (Atuy, 30_09)
- `Nghuuurrghh...` -> `Nghuuurrghh...` (Vurai, 30_09)
- `Hiyaaaaaaaaaaaaah!!` -> `Hiyaaaaaaaaaaaaah!!` (Atuy, 30_09)
- `And now... it's over.` -> `E agora... acabou.` (Haku, 30_09)
- `We... did it?` -> `Conseguimos?` (Haku, 30_09)
- `Hmph... Heh heh...` -> `Humph... Heh heh...` (Vurai, 30_09)
- `Is that... truly your best?` -> `Isso é... realmente o seu melhor?` (Vurai, 30_09)
- `Wha--` -> `Quê--` (Man, 11_01)
- `Impossible... After taking so many hits...?` -> `Impossível... Depois de tantos golpes...?` (Haku, 30_09)
- `Ngh...! Everyone, get back!` -> `Ngh...! Todo mundo, recua!` (Haku, 30_09)
- `You believed that would suffice...` -> `Você achou que isso seria suficiente...` (Vurai, 30_09)
- `Do not INSULT ME!!` -> `Não me INSULTE!!` (Vurai, 30_09)
- `Everyone, GET DOWN!!` -> `Todo mundo, ABAIXA!!` (Haku, 30_09)
- `pPlane1_anum` -> `pPlane1_anum` (, 30_09)
- `murasaki` -> `murasaki` (, 30_09)
- `polySurface24777` -> `polySurface24777` (, 30_09)
- `polySurface24778` -> `polySurface24778` (, 30_09)
- `polySurface24779` -> `polySurface24779` (, 30_09)
- `polySurface24780` -> `polySurface24780` (, 30_09)
- `polySurface24781` -> `polySurface24781` (, 30_09)
- `polySurface24782` -> `polySurface24782` (, 30_09)
- `polySurface24783` -> `polySurface24783` (, 30_09)
- `polySurface24784` -> `polySurface24784` (, 30_09)
- `polySurface24785` -> `polySurface24785` (, 30_09)
- `polySurface24786` -> `polySurface24786` (, 30_09)
- `polySurface24787` -> `polySurface24787` (, 30_09)
- `polySurface24788` -> `polySurface24788` (, 30_09)
- `polySurface24789` -> `polySurface24789` (, 30_09)
- `polySurface24790` -> `polySurface24790` (, 30_09)
- `polySurface24791` -> `polySurface24791` (, 30_09)
- `pCylinder33` -> `pCylinder33` (, 30_09)
- `pCylinder34` -> `pCylinder34` (, 30_09)
- `pCylinder35` -> `pCylinder35` (, 30_09)
- `pCylinder36` -> `pCylinder36` (, 30_09)
- `pCylinder37` -> `pCylinder37` (, 30_09)
- `pCylinder38` -> `pCylinder38` (, 30_09)
- `pPlane4` -> `pPlane4` (, 30_09)
- `pPlane5` -> `pPlane5` (, 30_09)
- `pPlane6` -> `pPlane6` (, 30_09)
- `pPlane7` -> `pPlane7` (, 30_09)
- `pPlane8` -> `pPlane8` (, 30_09)
- `pPlane9` -> `pPlane9` (, 30_09)
- `pPlane10` -> `pPlane10` (, 30_09)
- `pPlane11` -> `pPlane11` (, 30_09)
- `pPlane12` -> `pPlane12` (, 30_09)
- `pPlane13` -> `pPlane13` (, 30_09)
- `pPlane14` -> `pPlane14` (, 30_09)
- `pPlane15` -> `pPlane15` (, 30_09)
- `pPlane16` -> `pPlane16` (, 30_09)
- `pPlane17` -> `pPlane17` (, 30_09)
- `pPlane18` -> `pPlane18` (, 30_09)
- `pPlane19` -> `pPlane19` (, 30_09)
- `pPlane20` -> `pPlane20` (, 30_09)
- `pPlane21` -> `pPlane21` (, 30_09)
- `pPlane22` -> `pPlane22` (, 30_09)
- `pPlane23` -> `pPlane23` (, 30_09)
- `pPlane24` -> `pPlane24` (, 30_09)
- `pPlane25` -> `pPlane25` (, 30_09)
- `pPlane26` -> `pPlane26` (, 30_09)
- `pPlane27` -> `pPlane27` (, 30_09)
- `pPlane28` -> `pPlane28` (, 30_09)
- `pPlane29` -> `pPlane29` (, 30_09)
- `pPlane30` -> `pPlane30` (, 30_09)
- `pPlane31` -> `pPlane31` (, 30_09)
- `pPlane32` -> `pPlane32` (, 30_09)
- `pPlane33` -> `pPlane33` (, 30_09)
- `pPlane34` -> `pPlane34` (, 30_09)
- `pPlane35` -> `pPlane35` (, 30_09)
- `pPlane36` -> `pPlane36` (, 30_09)
- `pPlane37` -> `pPlane37` (, 30_09)
- `pPlane38` -> `pPlane38` (, 30_09)
- `pPlane39` -> `pPlane39` (, 30_09)
- `pPlane40` -> `pPlane40` (, 30_09)
- `pPlane41` -> `pPlane41` (, 30_09)
- `pPlane42` -> `pPlane42` (, 30_09)
- `pPlane43` -> `pPlane43` (, 30_09)
- `pPlane44` -> `pPlane44` (, 30_09)
- `pPlane45` -> `pPlane45` (, 30_09)
- `pPlane46` -> `pPlane46` (, 30_09)
- `pPlane47` -> `pPlane47` (, 30_09)
- `pPlane48` -> `pPlane48` (, 30_09)
- `pPlane49` -> `pPlane49` (, 30_09)
- `pPlane50` -> `pPlane50` (, 30_09)
- `pPlane51` -> `pPlane51` (, 30_09)
- `Guh... hahh... You guys... OK?` -> `Guh... hahh... Vocês tão bem?` (Haku, 30_09)
- `Y-Yes... I'm fine... Nekone, are you all right?` -> `S-Sim... estou bem... Nekone, você está bem?` (Nekone, 30_09)
- `Only thanks to your shielding me, dear sister.` -> `Só graças a você me proteger, querida irmã.` (Nekone, 30_09)
- `Perfectly fine over here!` -> `Aqui está tudo ótimo!` (Nosuri, 30_09)
- `...A touch close for comfort.` -> `...Quase passou do limite.` (Ougi, 30_09)
- `A bit TOO close, yeah?` -> `Passou MUITO do limite, né?` (Haku, 30_09)
- `Well, that's worrying...` -> `Bom, isso preocupa...` (Haku, 30_09)
- `What in the world was that...?` -> `O que diabos foi aquilo...?` (Haku, 30_09)
- `Ngh...ah...` -> `Ngh...ah...` (Oshtor, 30_09)
- `Wh-Where is Her Highness--` -> `On-Onde está Sua Alteza--` (Nekone, 30_09)
- `Ngh... She is... safe. She has merely fallen\n` -> `Ngh... Ela está... a salvo. Apenas desmaiou\n` (Oshtor, 30_09)
- `unconscious.` -> `inconsciente.` (Oshtor, 30_09)
- `D-Dear brother!` -> `Q-Querido irmão!` (Nekone, 30_09)
- `Do not worry for me. Above all else, do not\n` -> `Não se preocupe comigo. Acima de tudo, não\n` (Oshtor, 30_09)
- `lower your guard. This is far from over...` -> `baixe a guarda. Isso está longe de acabar...` (Oshtor, 30_09)
- `Huh...?` -> `Hein...?` (Haku, 11_01)
- `FOOLS...` -> `TOLOS...` (Vurai, 30_09)
- `Wh--` -> `Q--` (Haku, 11_07)
- `N-No...` -> `N-Não..` (Protagonista, 12_01)
- `We couldn't do... anything...?` -> `Não conseguimos fazer... nada...?` (Haku, 30_09)
- `env_hip` -> `env_hip` (, 30_09)
- `DID YOU TRULY THINK YOU COULD SEAL ME?\n` -> `VOCÊS REALMENTE ACHARAM QUE PODIAM ME SELAR?\n` (Vurai, 30_09)
- `YOU, WHO LACKED THE STRENGTH EVEN TO\n` -> `VOCÊS, QUE NÃO TINHAM FORÇA SEQUER PARA\n` (Vurai, 30_09)
- `BREATHE?` -> `RESPIRAR?` (Vurai, 30_09)
- `Nnngh...` -> `Nnh...` (Protagonista, 17_01)
- `Urgh... I knew I was pushing the two of them\n` -> `Argh... Eu sabia que estava exigindo demais das duas\n` (Haku, 30_09)
- `too hard.` -> `tão duro.` (Haku, 22_07)
- `Now he's at full power... and escape is\n` -> `Agora ele está em plena força... e escapar\n` (Haku, 30_09)
- `probably out of the question.\n` -> `provavelmente está fora de questão.\n` (Haku, 30_09)
- `This might be it for us...` -> `Talvez seja o fim pra nós...` (Haku, 30_09)
- `What do we do...? I've got no more cards up\n` -> `O que fazemos...? Não tenho mais nada\n` (Haku, 30_09)
- `my sleeve...` -> `na manga...` (Haku, 30_09)
- `It's not over, Haku. It is too early yet to\n` -> `Não acabou, Haku. Ainda é cedo demais para\n` (Oshtor, 30_09)
- `give up. Mark Vurai closely.` -> `desistir. Observe Vurai com atenção.` (Oshtor, 30_09)
- `What?` -> `Que?` (Haku, 12_02)
- `The form that he is in now...\n` -> `A forma em que ele está agora...\n` (Oshtor, 30_09)
- `His powers are still incomplete!` -> `Os poderes dele ainda estão incompletos!` (Oshtor, 30_09)
- `The sealing has had a definite effect on him,\n` -> `O selamento teve um efeito definitivo nele,\n` (Oshtor, 30_09)
- `at least. And if that is true--` -> `pelo menos. E se isso for verdade--` (Oshtor, 30_09)
- `DO YOU BELIEVE YOU CAN STILL OPPOSE ME?\n` -> `VOCÊS ACREDITAM QUE AINDA PODEM ME ENFRENTAR?\n` (Vurai, 30_09)
- `YOU CAN BARELY STAND--` -> `MAL CONSEGUE FICAR DE PE--` (Haku, 30_09)
- `RRGH... Y-YOU...` -> `RRGH... V-VOCÊ...` (Oshtor, 30_09)
- `That's enough! Stop! You can't take--` -> `Chega! Para! Você não aguenta--` (Haku, 30_09)
- `GRRAAAAGH... CEASE THIS FUTILE STRUGGLING!` -> `GRRAAAAGH... PAREM COM ESSA LUTA INÚTIL!` (Vurai, 30_09)
- `You two...` -> `Vocês dois...` (Jachdwalt, 20_21)
- `Haku... stand up.` -> `Haku... levanta.` (Ukon, 30_09)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Haku... if you falter now, then their efforts\n` -> `Haku... se você fraquejar agora, o esforço deles\n` (Ukon, 30_09)
- `will all be for nothing.` -> `terá sido em vão.` (Ukon, 30_09)
- `You guys... still got this, right?` -> `Vocês... ainda dão conta, né?` (Haku, 30_09)
- `Th-This is nothing.` -> `Isso não é nada.` (Nosuri, 30_09)
- `Hah... who do you think I am?` -> `Hah... quem você acha que sou?` (Jachdwalt, 30_09)
- `If my dear sister remains in the fight,\n` -> `Enquanto minha querida irmã permanecer na luta,\n` (Ougi, 30_09)
- `then you shall have my sword until the end.` -> `você terá minha espada até o fim.` (Ougi, 30_09)
- `W-We won't let you fight alone, Sir Haku...\n` -> `N-Não vamos deixar você lutar sozinho, Senhor Haku...\n` (Nekone, 30_09)
- `Right, Cocopo?` -> `Certo, Cocopo?` (Nekone, 30_09)
- `Gotta make sure to finish him off good and\n` -> `Dessa vez vamos garantir que ele caia de vez\n` (Nosuri, 30_09)
- `proper this time.` -> `e não levante mais.` (Nosuri, 30_09)
- `My mind was made up long ago!` -> `Minha decisão foi tomada faz tempo!` (Jachdwalt, 30_09)
- `No need to ask me. Doesn't look like we got\n` -> `Nem precisa perguntar. Parece que não\n` (Haku, 30_09)
- `much of a choice anymore, yeah?` -> `temos muita escolha mais, né?` (Haku, 30_09)
- `I leave the rest... to you.` -> `Deixo o resto... com vocês.` (Oshtor, 30_09)
- `Let's go, Haku.` -> `Vamos, Haku.` (Kuon, 30_04)
- `Yeah!` -> `Isso!` (Bandidos, 13_05)
- `HAH... HAHAHAHA... I SEE.\n` -> `HAH... HAHAHAHA... ENTENDO.\n` (Vurai, 30_09)
- `AND STILL YOU STAND.` -> `E AINDA ESTÃO DE PÉ.` (Vurai, 30_09)
- `ALLOW ME TO APOLOGIZE... IT SEEMS I HAVE\n` -> `PERMITAM-ME PEDIR DESCULPAS... PARECE QUE\n` (Vurai, 30_09)
- `TRULY MISJUDGED YOU.` -> `OS SUBESTIMEI DE VERDADE.` (Vurai, 30_09)
- `AND ALLOW ME TO GIVE YOU YOUR DUE PRAISE.\n` -> `E PERMITAM-ME DAR O CRÉDITO QUE MERECEM.\n` (Vurai, 30_09)
- `YOU ARE WARRIORS WORTHY OF STANDING AS MY\n` -> `VOCÊS SÃO GUERREIROS DIGNOS DE SEREM MEUS\n` (Vurai, 30_09)
- `ENEMY.` -> `INIMIGO.` (SYSTEM, 30_09)
- `VALOR FOR VALOR, I SHALL REPAY YOU IN KIND!\n` -> `VALOR POR VALOR, VOU RETRIBUIR NA MESMA MOEDA!\n` (Vurai, 30_09)
- `RELISH YOUR FORTUNE, THAT YOU NOW EXPERIENCE\n` -> `APRECIEM SUA SORTE, POR ORA EXPERIMENTAM\n` (Vurai, 30_09)
- `MY TRUE POWER!` -> `MEU PODER REAL!` (Haku, 30_09)
- `帝都英霊結界／戦闘開始します` -> `BARREIRA HEROICA DA CAPITAL / INICIANDO COMBATE` (SYSTEM, 30_09)
- `Impossible...` -> `Impossível...` (Kuon, 22_05)
- `I HAVE BEEN... BROUGHT LOW...?` -> `EU FUI... DERRUBADO...?` (Vurai, 30_09)
- `HOW COULD... I have...?` -> `COMO PÔDE... eu...?` (Vurai, 30_09)
- `Hahh... hahh... hahh...` -> `Arre... arre... arre...` (Haku, 19_08)
- `Hee hee, hee hee hee...` -> `Hee hee, hee hee hee...` (Atuy, 30_09)
- `Ahahahahahaha! Oh, what fun...\n` -> `Ahahahahahaha! Que divertido...\n` (Atuy, 30_09)
- `That was SO much FUN!` -> `Foi MUITO divertido!` (Atuy, 30_09)
- `Ngh... hah... gh... hah...` -> `Ngh... hah... gh... hah...` (Nosuri, 30_09)
- `Th-That was... nothing... A good woman never...\n` -> `I-Isso foi... nada... Uma boa mulher nunca...\n` (Nosuri, 30_09)
- `loses her cool...` -> `perde a compostura...` (Nosuri, 30_09)
- `I have nothing... to fear from...\n` -> `Não tenho nada... a temer de...\n` (Nosuri, 30_09)
- `Vurai the Vanguard!` -> `Vurai, o Vanguardeiro!` (Nosuri, 30_09)
- `Dear sister, I suggest you dab at yourself with\n` -> `Querida irmã, sugiro que se seque com\n` (Ougi, 30_09)
- `this. You appear to be perspiring rather\n` -> `isso. Parece que está transpirando bastante\n` (Ougi, 30_09)
- `heavily.` -> `demais.` (Ougi, 30_09)
- `So that's... what it's like to fight one of\n` -> `Então é assim... lutar contra um dos\n` (Haku, 30_09)
- `the bearers of the Akuruka...` -> `portadores da Akuruka...` (Haku, 30_09)
- `Yeah... That was real close...` -> `É... Foi muito por pouco...` (Haku, 30_09)
- `My legs are still shaking...` -> `Minhas pernas ainda estão tremendo...` (Haku, 30_09)
- `If he had released the Akuruka's full power--` -> `Se ele tivesse liberado o poder total da Akuruka--` (Haku, 30_09)
- `Ugh... hh... hahhh...` -> `Ugh... hh... hahhh...` (Kuon, 30_09)
- `I... I'm fine. Just... a little lightheaded.` -> `Eu... estou bem. Só... um pouco tonta.` (Kuon, 30_09)
- `I suppose that fight just wore me out.` -> `Acho que aquela batalha só me deixou esgotada.` (Kuon, 30_09)
- `You sure you're not hurt anywhere?` -> `Está bem? Nada machucado?` (Garota, 30_09)
- `...I'm fine, really... Ahaha, are you worrying\n` -> `...Estou bem, sério... Ahaha, está me preocupando\n` (Kuon, 30_09)
- `about me now?` -> `com isso agora?` (Kuon, 30_09)
- `'Course I am! Why wouldn't I be worried about\n` -> `Claro que sim! Por que não estaria preocupado\n` (Haku, 30_09)
- `you?` -> `pode?` (Haku, 13_01)
- `...Oh, ah... I suppose so.` -> `...Ah, é... suponho que sim.` (Kuon, 30_09)
- `Oshtor looks down upon Vurai's motionless body,\n` -> `Oshtor olha para o corpo imóvel de Vurai,\n` (NARRADOR, 30_09)
- `sorrow in his eyes.` -> `tristeza nos olhos.` (NARRADOR, 30_09)
- `Dear brother, here.` -> `Querido irmão, aqui.` (Nekone, 30_09)
- `A familiar Akuruka has fallen out of Vurai's\n` -> `Uma Akuruka familiar caiu das roupas de Vurai.\n` (NARRADOR, 30_09)
- `clothes. Nekone hands it to Oshtor.` -> `Nekone a entrega a Oshtor.` (NARRADOR, 30_09)
- `Oshtor takes the mask and puts it on. He closes\n` -> `Oshtor pega a máscara e a veste. Ele fecha\n` (NARRADOR, 30_09)
- `his eyes briefly, as if to remember its feel.` -> `os olhos brevemente, como se quisesse lembrar a sensação.` (NARRADOR, 30_09)
- `Once he opens his eyes again, Nekone helps\n` -> `Quando abre os olhos, Nekone o ajuda a\n` (NARRADOR, 30_09)
- `him walk, and he turns to Anju.` -> `andar, e ele se vira para Anju.` (NARRADOR, 30_09)
- `Your Highness. I deeply apologize for my late\n` -> `Sua Alteza. Peço perdão pela minha chegada\n` (Oshtor, 30_09)
- `arrival.` -> `tardia.` (Oshtor, 30_09)
- `I am... so glad...  she's all right...` -> `Eu... fico tão aliviado... ela está bem...` (Haku, 30_09)
- `...Your Highness?` -> `...Sua Alteza?` (Oshtor, 30_09)
- `Ah... hh...` -> `Ah... hh...` (Anju, 30_08)
- `Anju slowly reaches out.` -> `Anju estende a mão lentamente.` (NARRADOR, 30_09)
- `But it doesn't seem as though her empty eyes\n` -> `Mas seus olhos vazios não parecem enxergar\n` (NARRADOR, 30_09)
- `have caught sight of Oshtor.` -> `Oshtor.` (NARRADOR, 30_09)
- `What the...?` -> `O que é isso...?` (Haku, 30_09)
- `Y-Your Highness? What is the matter?` -> `S-Sua Alteza? O que aconteceu?` (Nekone, 30_09)
- `Princess? Can you hear our voices?` -> `Princesa? Você consegue nos ouvir?` (Oshtor, 30_09)
- `Hh... ah...` -> `Hh... ah...` (Anju, 30_09)
- `Oshtor kneels before Anju, and gently takes\n` -> `Oshtor se ajoelha diante de Anju e gentilmente\n` (NARRADOR, 30_09)
- `her hand.` -> `a mão.` (Haku, 30_09)
- `...A-Aa... hh... hh...` -> `...A-Aa... hh... hh...` (Anju, 30_09)
- `Anju attempts to speak again, but all that comes\n` -> `Anju tenta falar de novo, mas tudo que sai\n` (NARRADOR, 30_09)
- `out of her mouth are labored, raspy whimpers.` -> `de sua boca são gemidos esforçados e roufenhos.` (NARRADOR, 30_09)
- `She closes her eyes in frustration, tears\n` -> `Ela fecha os olhos em frustração, lágrimas\n` (NARRADOR, 30_09)
- `beginning to stream down her cheeks.` -> `começando a escorrer pelo rosto.` (NARRADOR, 30_09)
- `...Lady Kuon, may I ask you to--` -> `...Senhora Kuon, posso pedir que--` (Oshtor, 30_09)
- `Yes. Princess, can you hear me?\n` -> `Sim. Princesa, você consegue me ouvir?\n` (Kuon, 30_09)
- `Please open your mouth for me.` -> `Por favor, abra a boca para mim.` (Kuon, 30_09)
- `Kuon examines Anju's throat with a serious\n` -> `Kuon examina a garganta de Anju com expressão\n` (NARRADOR, 30_09)
- `expression.` -> `natural.` (Haku, 15_01)
- `She then holds Anju's eyelids open with delicate\n` -> `Em seguida, abre as pálpebras de Anju com\n` (NARRADOR, 30_09)
- `care, carefully examining her.` -> `delicadeza, examinando-a com cuidado.` (NARRADOR, 30_09)
- `She checks her pulse and her temperature, and\n` -> `Ela verifica o pulso e a temperatura, e\n` (NARRADOR, 30_09)
- `after everything, Kuon sighs and looks up.` -> `depois de tudo, Kuon suspira e olha para cima.` (NARRADOR, 30_09)
- `It must have been a powerful poison. Her throat\n` -> `Deve ter sido um veneno poderoso. A garganta dela\n` (Kuon, 30_09)
- `is all but destroyed.` -> `está praticamente destruída.` (Kuon, 30_09)
- `As long as she's like this, she won't be able\n` -> `Enquanto estiver assim, ela não vai conseguir\n` (Kuon, 30_09)
- `to speak.` -> `falar.` (Kuon, 30_09)
- `No...` -> `Não...` (Touka, 17_01)
- `What's more serious, though... is her mind.` -> `O que é mais sério, porém... é a mente dela.` (Kuon, 30_09)
- `Mind?` -> `Pode?` (Garota, 30_09)
- `The poison in question has a mind-numbing\n` -> `O veneno em questão tem um efeito\n` (Kuon, 30_09)
- `effect.` -> `efeito.` (Haku, 30_09)
- `It's a dangerous drug that can be used to ease\n` -> `É uma droga perigosa que pode ser usada para aliviar\n` (Kuon, 30_09)
- `pain, but overdosing can easily destroy one's\n` -> `a dor, mas em excesso pode facilmente destruir a\n` (Kuon, 30_09)
- `mind...` -> `mente...` (Kuon, 30_09)
- `A sharp inhale ripples through the group.` -> `Uma respiração brusca percorre o grupo.` (NARRADOR, 30_09)
- `...Can she be cured?` -> `...Ela pode ser curada?` (Haku, 30_09)
- `Yes. It won't be easy, but if we act fast with\n` -> `Sim. Não vai ser fácil, mas se agirmos rápido com\n` (Kuon, 30_09)
- `the right treatment, we can avoid any lasting\n` -> `o tratamento certo, podemos evitar sequelas\n` (Kuon, 30_09)
- `effects.` -> `efeitos.` (Homem, 30_01)
- `I... see.` -> `Eu... entendo.` (Haku, 19_08)
- `Thank goodness... Miss Anju...` -> `Graças aos céus... Senhora Anju...` (Nekone, 30_09)
- `Whew, well... that gave me quite a scare.` -> `Ufa, bom... quase me deu um ataque.` (Haku, 30_09)
- `But we'll have to get somewhere we can find some\n` -> `Mas vamos precisar encontrar um lugar tranquilo\n` (Haku, 30_09)
- `peace, first.` -> `antes, primeiro.` (Haku, 30_09)
- `Got it. We need to get out of here before anyone\n` -> `Entendido. Temos que sair daqui antes que\n` (Haku, 30_09)
- `else finds us.` -> `nos encontre.` (Haku, 30_09)
- `Huh? But General Vurai has been defeated...\n` -> `Hein? Mas o General Vurai foi derrotado...\n` (Nekone, 30_09)
- `Why do we need to run now?` -> `Por que precisamos fugir agora?` (Nekone, 30_09)
- `No... If he wasn't the mastermind behind this\n` -> `Não... Se ele não era o responsável por tudo isso,\n` (Oshtor, 30_09)
- `whole plan, we can't stay here for too long.` -> `não podemos ficar aqui por muito tempo.` (Oshtor, 30_09)
- `From an outsider's perspective, we infiltrated\n` -> `Do ponto de vista externo, nós invadimos\n` (Oshtor, 30_09)
- `the princess's room, attacked Vurai, and\n` -> `o quarto da princesa, atacamos Vurai, e\n` (Oshtor, 30_09)
- `kidnapped her.` -> `a sequestramos.` (Oshtor, 30_09)
- `Wh... But... But my brother is innocent!` -> `Qu... Mas... Mas meu irmão é inocente!` (Nekone, 30_09)
- `And how exactly do you plan on proving that?` -> `E como exatamente você planeja provar isso?` (Oshtor, 30_09)
- `That's... It wouldn't be necessary to do such a\n` -> `Isso... Não seria necessário fazer tal\n` (Nekone, 30_09)
- `thing--` -> `coisa--` (Nekone, 30_09)
- `...We have Her Highness as our witness.\n` -> `...Temos Sua Alteza como nossa testemunha.\n` (Oshtor, 30_09)
- `She can tell them--Ah!` -> `Ela pode falar por nós--Ah!` (Oshtor/Nekone, 30_09)
- `That's going to be difficult with the princess\n` -> `Isso vai ser difícil com a princesa\n` (Oshtor, 30_09)
- `in this state.` -> `nesse estado.` (Oshtor, 30_09)
- `Not to mention anyone with a grudge against\n` -> `Sem contar que qualquer um com rancor de\n` (Oshtor, 30_09)
- `Oshtor will jump at the chance to prove him\n` -> `Oshtor vai aproveitar a chance para provar sua\n` (Oshtor, 30_09)
- `guilty.` -> `culpa.` (Oshtor, 30_09)
- `By the time the princess recovers enough to\n` -> `Quando a princesa se recuperar o suficiente para\n` (Oshtor, 30_09)
- `testify, they'd already have our heads on\n` -> `testemunhar, já teriam nossas cabeças em\n` (Oshtor, 30_09)
- `pikes.` -> `estacas.` (Oshtor, 30_09)
- `The evident plan was to keep her silent and use\n` -> `O plano evidente era mantê-la em silêncio e usá-la\n` (Oshtor, 30_09)
- `her for her status. A political marionette, as\n` -> `pelo seu status. Uma marionete política,\n` (Oshtor, 30_09)
- `it were.` -> `assim.` (Haku, 30_09)
- `That's so cruel...` -> `Que cruel...` (Rulutieh, 20_03)
- `Man oh man. So you're saying that the big fella\n` -> `Caramba. Está dizendo que aquele grandão\n` (Jachdwalt, 30_09)
- `over there wasn't even the one behind it all?` -> `nem era o responsável por tudo isso?` (Jachdwalt, 30_09)
- `Jachdwalt rolls his shoulders wearily as he\n` -> `Jachdwalt rola os ombros com cansaço enquanto\n` (NARRADOR, 30_09)
- `glances back to Vurai.` -> `olha de relance para Vurai.` (NARRADOR, 30_09)
- `Yes. Vurai is not one for such scheming as\n` -> `Sim. Vurai não é de fazer esse tipo de trama.\n` (Oshtor, 30_09)
- `this. The mastermind must be elsewhere.` -> `O responsável deve estar em outro lugar.` (Oshtor, 30_09)
- `I get the feeling that Honoka went into hiding\n` -> `Tenho a sensação de que Honoka foi se esconder\n` (Haku, 30_09)
- `because this mastermind had framed her.` -> `porque o responsável a incriminou.` (Haku, 30_09)
- `But the question is, where do we go now...?\n` -> `Mas a questão é, para onde vamos agora...?\n` (Haku, 30_09)
- `Oshtor, any good ideas?` -> `Oshtor, tem alguma boa ideia?` (Haku, 30_09)
- `...Ennakamuy.` -> `...Ennakamuy.` (Oshtor, 30_09)
- `It is in the far reaches of this land,\n` -> `Fica nos confins desta terra,\n` (Oshtor, 30_09)
- `surrounded by mountainous terrain... A natural\n` -> `rodeada por terreno montanhoso... Uma defesa natural.\n` (Oshtor, 30_09)
- `fortress.` -> `fortaleza.` (UI, 23_10)
- `If we go there, we should be able to protect the\n` -> `Se formos lá, devemos conseguir proteger a\n` (Oshtor, 30_09)
- `princess from any pursuers for a time.` -> `princesa de qualquer perseguidor por um tempo.` (Oshtor, 30_09)
- `Isn't Ennakamuy...?` -> `Ennakamuy não é...?` (Kiwru, 30_09)
- `Yes. It is our homeland.` -> `Sim. É nossa terra natal.` (Oshtor, 30_09)
- `I am sorry, Kiwru. This may cause trouble for\n` -> `Sinto muito, Kiwru. Isso pode causar problemas para\n` (Oshtor, 30_09)
- `your family, and the people--` -> `sua família e o povo--` (Oshtor, 30_09)
- `Please don't say such things, brother. This\n` -> `Por favor, não diga isso, irmão. Esta\n` (Kiwru, 30_09)
- `crisis involves all of Yamato.` -> `crise envolve todo Yamato.` (Kiwru, 30_09)
- `...Thank you.` -> `...Obrigado.` (Haku, 23_11)
- `They look so weak... like they could collapse\n` -> `Parecem tão fracas... como se fossem cair\n` (Haku, 30_09)
- `at any moment.` -> `a qualquer momento.` (Haku, 30_09)
- `They're not saying much, but that "path" and the\n` -> `Não estão dizendo muito, mas aquele 'caminho' e o\n` (Haku, 30_09)
- `whole sealing spell thing--` -> `encantamento de selamento--` (Haku, 30_09)
- `It'll be way too dangerous to ask any more of\n` -> `Seria perigoso demais pedir mais delas.\n` (Haku, 30_09)
- `them...` -> `deles...` (Kuon, 22_05)
- `I walk over to the fallen guards and start\n` -> `Vou até os guardas caídos e começo a\n` (Haku, 30_09)
- `pulling off their clothes.` -> `tirar as roupas deles.` (Haku, 30_09)
- `Ougi, give me a hand here.` -> `Ougi, me dá uma mão aqui.` (Haku, 30_09)
- `Aha, you intend on disguising us as soldiers to\n` -> `Ah, pretende nos disfarçar de soldados para\n` (Ougi, 30_09)
- `escape. A fine plan... Exhilaratingly\n` -> `escapar. Bom plano... Deliciosamente\n` (Ougi, 30_09)
- `suspenseful.` -> `emocionante.` (Ougi, 30_09)
- `...Master.` -> `...Mestre.` (Uruuru/Saraana, 30_09)
- `You need not worry about us. Please--we will\n` -> `Não precisa se preocupar conosco. Por favor--\n` (Uruuru/Saraana, 30_09)
- `be able to withstand this.` -> `conseguimos aguentar isso.` (Uruuru/Saraana, 30_09)
- `No, you two rest up. You guys can barely walk.` -> `Não, vocês duas descansam. Mal conseguem andar.` (Haku, 30_09)
- `Irrelevant.` -> `Irrelevante.` (Uruuru/Saraana, 30_09)
- `We intend on carrying out your will, regardless\n` -> `Pretendemos cumprir sua vontade, independentemente\n` (Uruuru/Saraana, 30_09)
- `of whether it may cost us our lives.` -> `de custar nossas vidas.` (Uruuru/Saraana, 30_09)
- `No. This is an order.` -> `Não. Isso é uma ordem.` (Haku, 30_09)
- `Wait, what!? They were planning on sacrificing\n` -> `Espera, o quê!? Elas planejavam se sacrificar\n` (Haku, 30_09)
- `themselves?` -> `de verdade?` (Haku, 30_09)
- `...As you wish.` -> `...Como desejar.` (Oshtor, 23_01)
- `We'll have the princess hide in that wicker\n` -> `Vamos esconder a princesa naquele baú de\n` (Haku, 30_09)
- `trunk.` -> `vime.` (Haku, 30_09)
- `We'll get a cart, and carry her on that. If we\n` -> `Vamos pegar uma carroça e transportá-la. Se\n` (Haku, 30_09)
- `play it cool, I think we can make it out of\n` -> `agirmos com calma, acho que conseguimos sair\n` (Haku, 30_09)
- `the capital.` -> `a capital.` (Ukon, 17_01)
- `And if we are to be discovered during our\n` -> `E se formos descobertos durante a\n` (Haku, 30_09)
- `flight?` -> `fuga?` (Haku, 30_09)
- `We'll say the trunk's full of gifts for nobles.\n` -> `Dizemos que o baú está cheio de presentes para nobres.\n` (Haku, 30_09)
- `If we're confident, they won't suspect a thing.` -> `Se formos confiantes, não vão suspeitar de nada.` (Haku, 30_09)
- `Although I suppose it's a gamble of whether we\n` -> `Embora seja uma aposta se conseguimos\n` (Haku, 30_09)
- `can fool them or not...` -> `enganá-los ou não...` (Haku, 30_09)
- `Wonder if this thing still works?` -> `Será que isso ainda funciona?` (Haku, 30_09)
- `As I speak, I pull out a certain handy little\n` -> `Enquanto falo, tiro uma certa caixinha útil\n` (Haku, 30_09)
- `box.` -> `caixa.` (Haku, 30_09)
- `That is--` -> `Isso é--` (Oshtor, 30_09)
- `The seal of the Mikado... I had no idea that you\n` -> `O selo do Mikado... Não sabia que você havia\n` (Oshtor, 30_09)
- `had been bestowed such a token.` -> `recebido tal item.` (Oshtor, 30_09)
- `It's a little complicated. Last time I showed\n` -> `É um pouco complicado. Na última vez que mostrei\n` (Haku, 30_09)
- `it to the guards at the Uzurushan ruins, it\n` -> `aos guardas nas ruínas de Uzurushan, funcionou\n` (Haku, 30_09)
- `worked fine.` -> `bem.` (Haku, 30_09)
- `Circumstances are different. It may not work,\n` -> `As circunstâncias são diferentes. Pode não funcionar,\n` (Oshtor, 30_09)
- `especially in the case of those who know what\n` -> `especialmente com quem sabe o que\n` (Oshtor, 30_09)
- `transpired here.` -> `aconteceu aqui.` (Oshtor, 30_09)
- `However, the guards outside should still be\n` -> `Porém, os guardas lá fora ainda devem estar\n` (Oshtor, 30_09)
- `unaware of all this. We may be able to convince\n` -> `sem saber de nada. Podemos ser capazes de convencê-los.\n` (Oshtor, 30_09)
- `them.` -> `deles.` (Kuon, 11_05)
- `In the current political confusion, few would be\n` -> `Na confusão política atual, poucos conseguiriam\n` (Oshtor, 30_09)
- `able to maintain their composure at the sight of\n` -> `manter a compostura ao ver\n` (Oshtor, 30_09)
- `that seal.` -> `o selo.` (Oshtor, 30_09)
- `Good to hear. Guess I'll be putting it to\n` -> `Bom ouvir. Acho que vou fazer bom\n` (Haku, 30_09)
- `good use, then.` -> `uso dele, então.` (Haku, 30_09)
- `Are you... sure this is going to work?` -> `Você tem certeza que isso vai funcionar?` (Kiwru, 30_09)
- `Kiwru, this isn't a matter of whether it's\n` -> `Kiwru, não é uma questão de funcionar\n` (Haku, 30_09)
- `going to work.` -> `ou não.` (Haku, 30_09)
- `Huh?` -> `Hein?` (Haku, 11_01)
- `We're going to MAKE it work.` -> `Nós vamos FAZER funcionar.` (Haku, 30_09)
- `Heh. Well said.` -> `Heh. Bem dito.` (Ukon, 30_09)
- `Very like you, Haku. Reminds me of the face you\n` -> `Típico de você, Haku. Me lembra a cara que você\n` (Ukon, 30_09)
- `make when you're talking yourself out of\n` -> `faz quando está se convencendo a parar\n` (Ukon, 30_09)
- `working.` -> `funciona.` (Haku, 30_09)
- `...Hey, that's uncalled for.` -> `...Ei, isso foi desnecessário.` (Haku, 30_09)
- `In any case, there's one last precaution I'd\n` -> `De qualquer forma, há uma última precaução que\n` (Oshtor, 30_09)
- `like to take care of.` -> `quero tomar.` (Oshtor, 30_09)
- `Ougi, can I ask a small favor?` -> `Ougi, posso pedir um pequeno favor?` (Oshtor, 30_09)
- `Ask away.` -> `Pode falar.` (Ougi, 30_09)
- `Raiko and Dekopompo's soldiers should still be\n` -> `Os soldados de Raiko e Dekopompo ainda devem estar\n` (Oshtor, 30_09)
- `stuck outside the city walls.` -> `presos fora das muralhas da cidade.` (Oshtor, 30_09)
- `Yes, it seemed as though their stalemate was\n` -> `Sim, parece que o impasse deles os mantinha\n` (Ougi, 30_09)
- `keeping them rather--` -> `bastante ocupados--` (Ougi, 30_09)
- `As Ougi speaks, however, he seems to understand\n` -> `Mas enquanto Ougi fala, parece que entende\n` (NARRADOR, 30_09)
- `what I'm getting at. A faint smile crosses his\n` -> `o que quero dizer. Um leve sorriso cruza seu rosto.\n` (NARRADOR, 30_09)
- `face.` -> `rosto.` (Rulutieh, 16_02)
- `...I see. So that is your ploy.` -> `...Entendo. Esse é o seu plano, então.` (Ougi, 30_09)
- `Yep. Just say it's an order from Vurai, and\n` -> `Isso. É só dizer que é ordem de Vurai, e\n` (Haku, 30_09)
- `open up the gates.` -> `abrir os portões.` (Haku, 30_09)
- `If that happens, I'm sure all of them will\n` -> `Se isso acontecer, com certeza todos eles vão\n` (Haku, 30_09)
- `try to rush into the capital.` -> `tentar entrar correndo na capital.` (Haku, 30_09)
- `And we slip away amidst the confusion. Haha...\n` -> `E a gente some no meio da confusão. Haha...\n` (Haku, 30_09)
- `your ideas are always quite refreshing.` -> `suas ideias são sempre muito criativas.` (Haku, 30_09)
- `All we need now is something that'll make it\n` -> `Agora só precisamos de algo que pareça mais\n` (Oshtor, 30_09)
- `seem more like an order from Vurai.` -> `uma ordem de Vurai.` (Oshtor, 30_09)
- `...Perhaps we should try searching Vurai for any\n` -> `...Talvez devêssemos procurar nos pertences de Vurai\n` (Oshtor, 30_09)
- `personal effects.` -> `por objetos pessoais.` (Oshtor, 30_09)
- `We look through everything left on Vurai's\n` -> `Vasculhamos tudo que sobrou nos pertences de Vurai.\n` (Haku, 30_09)
- `person.` -> `terrível.` (Nekone, 15_03)
- `We're not exactly comfortable doing it, but we\n` -> `Não nos sentimos muito bem fazendo isso, mas\n` (Haku, 30_09)
- `really don't have the time to complain.` -> `realmente não temos tempo para reclamar.` (Haku, 30_09)
- `After fumbling around for a little while, I feel\n` -> `Depois de revirar por um tempo, sinto\n` (Haku, 30_09)
- `something hard hit my fingertips.` -> `algo duro nas pontas dos dedos.` (Haku, 30_09)
- `I pull out a golden circle about the size of my\n` -> `Tiro um círculo dourado do tamanho da minha\n` (Haku, 30_09)
- `hand, with an intricate engraving on it.` -> `mão, com uma gravura intrincada.` (Haku, 30_09)
- `Some kind of seal...?` -> `Algum tipo de selo...?` (Haku, 30_09)
- `Yes. It is a golden seal that our liege bestows\n` -> `Sim. É um selo dourado que nosso senhor concede\n` (Oshtor, 30_09)
- `as proof of being one of the Eight Pillar\n` -> `como prova de ser um dos Oito\n` (Oshtor, 30_09)
- `Generals.` -> `Generais.` (Haku, 18_01)
- `One who holds this seal is either one of the\n` -> `Quem possui este selo é um dos\n` (Oshtor, 30_09)
- `Eight Pillar Generals, or under the direct\n` -> `Oito Generais-Pilar, ou está sob o comando\n` (Oshtor, 30_09)
- `command of one.` -> `direto de um.` (Oshtor, 30_09)
- `Of course, the same authority would be granted\n` -> `Naturalmente, a mesma autoridade seria concedida\n` (Oshtor, 30_09)
- `to a letter stamped with this seal.` -> `a uma carta com este selo.` (Oshtor, 30_09)
- `Sounds like exactly what we need. I'll just help\n` -> `É exatamente o que precisamos. Vou pegar\n` (Haku, 30_09)
- `myself, then.` -> `para mim, então.` (Haku, 30_09)
- `Now then, Haku, if I may.` -> `Pois bem, Haku, se permite.` (Maroro, 30_09)
- `sure.` -> `não.` (Haku, 12_16)
- `Ougi extracts some paper and a scribe's brush\n` -> `Ougi retira papel e pincel de uma mesa próxima\n` (NARRADOR, 30_09)
- `from a nearby desk, and quickly begins to\n` -> `e rapidamente começa a escrever.\n` (NARRADOR, 30_09)
- `write.` -> `escreve.` (Haku, 30_09)
- `He presses the seal to it, and in no time, he\n` -> `Ele carimba o selo, e em pouco tempo\n` (NARRADOR, 30_09)
- `holds in his hand an "official order" from\n` -> `tem em mãos uma 'ordem oficial' de\n` (NARRADOR, 30_09)
- `Vurai.` -> `Vurai.` (Woshis, 30_02)
- `You'd never be able to tell what a rush job it\n` -> `Impossível dizer que foi feito às pressas\n` (Haku, 30_09)
- `is by looking at it. It's actually pretty\n` -> `só de olhar. É muito bom mesmo.\n` (Haku, 30_09)
- `impressive.` -> `impressionante.` (Haku, 30_09)
- `Hmhmhm. The pieces are in place... Now all that\n` -> `Hmhmhm. As peças estão no lugar... Agora só\n` (Ougi, 30_09)
- `remains is to set the game in motion.` -> `resta iniciar o jogo.` (Ougi, 30_09)
- `You know, it's been on my mind for a while...\n` -> `Sabe, já estou pensando nisso faz um tempo...\n` (Haku, 30_09)
- `but I'd think he'd be a better conman than\n` -> `mas acho que ele seria um golpista melhor do que\n` (Haku, 30_09)
- `anything else.` -> `nada mais.` (Haku, 18_01)
- `I suppose I'm off to go make a scene, then.` -> `Suponho que vou fazer uma cena, então.` (Haku, 30_09)
- `And I shall accompany you.` -> `E eu vou junto.` (Nosuri, 30_09)
- `A moment please, Nosuri.` -> `Um momento, Nosuri.` (Oshtor, 30_09)
- `Oshtor halts the enthusiastic Nosuri, and turns\n` -> `Oshtor detém a animada Nosuri e se volta\n` (NARRADOR, 30_09)
- `instead to Kiwru.` -> `para Kiwru.` (NARRADOR, 30_09)
- `Kiwru, I wish for you to go instead.` -> `Kiwru, quero que você vá no lugar.` (Oshtor, 30_09)
- `Huh!? You want... me to go?` -> `Hein!? Quer que... eu vá?` (Kiwru, 30_09)
- `Yes. There is a duty I would have you perform on\n` -> `Sim. Há uma missão que gostaria que cumprisse\n` (Oshtor, 30_09)
- `my behalf.` -> `em meu nome.` (Oshtor, 30_09)
- `Tell my direct subordinates what happened, and\n` -> `Avise meus subordinados diretos do que aconteceu, e\n` (Oshtor, 30_09)
- `arrange for them and their families to escape\n` -> `ajude-os a fugir com as famílias\n` (Oshtor, 30_09)
- `the city.` -> `da cidade.` (Haku, 14_02)
- `I am afraid that I will be unable to personally\n` -> `Receio que não vou conseguir protegê-los\n` (Oshtor, 30_09)
- `prevent them from coming to harm, as matters\n` -> `pessoalmente de danos, dado como\n` (Oshtor, 30_09)
- `stand now.` -> `estamos.` (Haku, 30_09)
- `B-But I am not ready to take on such an\n` -> `M-Mas não estou pronto para uma tarefa\n` (Kiwru, 30_09)
- `important task!` -> `tão importante!` (Kiwru, 30_09)
- `The others would not have their trust, as you\n` -> `Os outros não teriam a confiança deles como você\n` (Oshtor, 30_09)
- `would. Only you can do this, as my sworn\n` -> `teria. Só você pode fazer isso, como meu jurado\n` (Oshtor, 30_09)
- `brother.` -> `irmão.` (Ukon, 15_05)
- `Kiwru hesitates for a moment, uncertainty in his\n` -> `Kiwru hesita por um momento, incerteza nos\n` (NARRADOR, 30_09)
- `eyes, but eventually he nods--resolute.` -> `olhos, mas por fim acena -- resoluto.` (NARRADOR, 30_09)
- `Understood! You can count on me!` -> `Entendido! Pode contar comigo!` (Kiwru, 30_09)
- `Shall we be on our way, Kiwru?` -> `Partimos então, Kiwru?` (Ougi, 30_09)
- `Yes!` -> `Sim!` (Rulutieh, 14_04)
- `Kiwru nods fiercely, then follows Ougi down the\n` -> `Kiwru acena com determinação, então segue Ougi\n` (NARRADOR, 30_09)
- `stairs.` -> `escada.` (Haku, 30_09)
- `Now then, Your Highness. I do apologize for the\n` -> `Então, Sua Alteza. Peço desculpas pelo\n` (Oshtor, 30_09)
- `discomfort, but please bear it for a while.` -> `desconforto, mas aguente por um momento.` (Oshtor, 30_09)
- `Up you go...` -> `Pronto, venha...` (Oshtor, 30_09)
- `Jachdwalt hoists Anju up, lowering her into the\n` -> `Jachdwalt ergue Anju e a coloca no\n` (NARRADOR, 30_09)
- `Sorry about this, princess. It shouldn't take\n` -> `Desculpe, princesa. Não deve demorar\n` (Jachdwalt, 30_09)
- `long, so just hang on for a little bit.` -> `muito, aguenta mais um pouco.` (Jachdwalt, 30_09)
- `Nh... hhh...` -> `Nh... hhh...` (Anju, 30_09)
- `Oshtor, you get in too.` -> `Oshtor, você entra também.` (Haku, 30_09)
- `No, I shall--` -> `Não, eu vou--` (Oshtor, 30_09)
- `Get in the trunk, Oshtor. Who're you kidding?\n` -> `Entra no baú, Oshtor. Com quem você pensa que está?\n` (Haku, 30_09)
- `You can barely move, and anyone could recognize\n` -> `Você mal consegue se mover, e qualquer um poderia\n` (Haku, 30_09)
- `you.` -> `isso.` (Nekone, 15_03)
- `...Nrrgh.` -> `...Nrrgh.` (Oshtor, 30_09)
- `Oshtor resists a little, but we manage to\n` -> `Oshtor resiste um pouco, mas conseguimos\n` (NARRADOR, 30_09)
- `wrangle him into the trunk as well.` -> `encaixá-lo no baú também.` (NARRADOR, 30_09)
- `Uruuru, Saraana, you two get in this one.` -> `Uruuru, Saraana, vocês duas nesse aqui.` (Haku, 30_09)
- `We highly disapprove of this decision...\n` -> `Discordamos muito desta decisão...\n` (Uruuru/Saraana, 30_09)
- `but an order is an order.` -> `mas uma ordem é uma ordem.` (Uruuru/Saraana, 30_09)
- `Shinonon, make sure you look after the two of\n` -> `Shinonon, cuida das duas por mim.\n` (Haku, 30_09)
- `Yep! You can count on me!` -> `Pode deixar! Pode contar comigo!` (Shinonon, 30_09)
- `After the twins get in, Shinonon nimbly hops\n` -> `Depois que as gêmeas entram, Shinonon pula\n` (NARRADOR, 30_09)
- `into the trunk with them.` -> `agilmente para dentro com elas.` (NARRADOR, 30_09)
- `Now...` -> `agora...` (Haku, 11_02)
- `Hmmm. The hem's not a very good fit, but it'll\n` -> `Hmm. A barra não encaixa muito bem, mas\n` (Haku, 30_09)
- `have to do, I suppose.` -> `vai ter que servir, suponho.` (Haku, 30_09)
- `Oh, drat. It's all baggy on me.` -> `Ah, droga. Ficou tudo largo em mim.` (Haku, 30_09)
- `I guess the soldier's clothes are a bit big on\n` -> `As roupas do soldado ficaram um pouco grandes em\n` (Haku, 30_09)
- `Kuon and the others. Everything's pretty\n` -> `Kuon e nos outros. Tudo muito\n` (Haku, 30_09)
- `loose...` -> `largo...` (Haku, 30_09)
- `And Nekone just looks like a sentient pile of\n` -> `E Nekone parece uma pilha de roupas\n` (Haku, 30_09)
- `fabric.` -> `pendurada.` (Haku, 11_06)
- `...Is there something you would like to say to\n` -> `...Tem algo que você gostaria de me dizer?\n` (Haku, 30_09)
- `me?` -> `mim?` (Maroro, 12_13)
- `Nope. Not a thing.` -> `Não. Nada.` (Nekone, 30_09)
- `I'm getting kind of uneasy about this plan,\n` -> `Estou ficando inseguro com este plano,\n` (Haku, 30_09)
- `but there's no turning back now.` -> `mas não dá para voltar atrás agora.` (Haku, 30_09)
- `I doubt we could stuff any more of us into\n` -> `Duvido que caibam mais de nós\n` (Haku, 30_09)
- `this trunk...` -> `neste baú...` (Haku, 30_09)
- `Let's go, everyone. We'll just have to figure\n` -> `Vamos, pessoal. Vamos resolver o resto\n` (Haku, 30_09)
- `the rest out on the fly.` -> `na hora.` (Haku, 30_09)
- `Lady-in-waiting` -> `Dama de companhia` (Ukon, 30_04)
- `This is... where we part.` -> `É aqui que nos separamos.` (Honoka, 30_09)
- `But... you should come with us...` -> `Mas... você devia vir com a gente...` (Haku, 30_09)
- `She is right. If you remain here alone--` -> `Ele tem razão. Se você ficar aqui sozinha--` (Oshtor, 30_09)
- `I do understand, but I owe a great debt to\n` -> `Eu entendo, mas tenho uma grande dívida com\n` (Honoka, 30_09)
- `Lady Honoka.` -> `Senhora Honoka.` (Haku, 30_09)
- `I have to know if she is safe.` -> `Preciso saber se ela está bem.` (Honoka, 30_09)
- `It's easy to see that if she stays within the\n` -> `É fácil ver que se ela ficar dentro das\n` (Haku, 30_09)
- `capital walls, things aren't going to be easy\n` -> `muralhas da capital, as coisas não vão ser fáceis\n` (Haku, 30_09)
- `for her.` -> `pra ela.` (Haku, 15_03)
- `But... her sense of duty doesn't come just from\n` -> `Mas... o senso de dever dela não vem só\n` (Haku, 30_09)
- `her position. She's already made up her mind.` -> `do cargo. Ela já tomou sua decisão.` (Haku, 30_09)
- `Please take care of Her Highness. I am sorry\n` -> `Por favor, cuidem de Sua Alteza. Sinto muito\n` (Honoka, 30_09)
- `that I could not accompany you to the end.` -> `por não poder acompanhá-los até o fim.` (Honoka, 30_09)
- `I wish the best of luck to all of you.` -> `Desejo a melhor sorte a todos vocês.` (Honoka, 30_09)
- `She bows deeply to us.` -> `Ela nos faz uma reverência.` (Haku, 30_09)
- `Thanks for helping us get this far... C'mon,\n` -> `Obrigado por nos ajudar até aqui... Vamos,\n` (Haku, 30_09)
- `guys.` -> `gente.` (Haku, 30_09)
- `I just leave her with a brief, curt farewell,\n` -> `Só lhe dou um adeus breve e seco,\n` (Haku, 30_09)
- `and pull the cart forward without looking back.` -> `e puxo a carroça sem olhar para trás.` (Haku, 30_09)
- `Somehow, I can feel her remaining in that deep\n` -> `De alguma forma, sinto que ela permanece\n` (Haku, 30_09)
- `bow until we fade from her sight.` -> `naquela reverência até sumir da nossa vista.` (Haku, 30_09)
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
| 0x2e8fdf | 43 | Impressive, Master. You have earned a tip\n |
| 0x2e900b | 11 | of the hat. |
| 0x2e9017 | 47 | Now, on to the final chapter. We have brought\n |
| 0x2e9047 | 47 | a combatant suitable to be your final opponent. |
| 0x2e9077 | 46 | There's still MORE? Wait, just give me a sec\n |
| 0x2e90a6 | 4 | to-- |
| 0x2e90ab | 43 | Hm. These are bizarre circumstances indeed. |
| 0x2e90d7 | 48 | Still... Hmhm. This does intrigue me somewhat.\n |
| 0x2e9108 | 46 | I always wished to have a match against you,\n |
| 0x2e9137 | 10 | Lord Haku. |
| 0x2e9143 | 35 | This has to be some kind of joke... |
| 0x2e9167 | 44 | I presume I need hold nothing back if this\n |
| 0x2e9194 | 11 | is a dream. |
| 0x2e91a0 | 46 | One of the Eight Pillar Generals... Munechika. |
| 0x2e91cf | 45 | I look forward to your fighting spirit as a\n |
| 0x2e91fd | 25 | man of Yamato, Lord Haku. |
| 0x2e9217 | 40 | Shall we begin then...? I am Munechika\n |
| 0x2e9240 | 31 | the Guardian! Prepare yourself! |
| 0x2e93f8 | 28 | Hmhm... Outplayed, it seems. |
| 0x2e9415 | 42 | Impressive, Lord Haku... You truly are a\n |
| 0x2e9440 | 14 | man among men. |
| 0x2e944f | 40 | I look forward to the day we may fight\n |
| 0x2e9478 | 13 | side by side. |
| 0x2e9486 | 47 | It's finally over... Geez, that was nearly it\n |
| 0x2e94b6 | 7 | for me. |
| 0x2e94be | 45 | Actually, it felt more like she let me win... |
| 0x2e94ec | 47 | Whatever... I made it this far, all the same.\n |
| 0x2e951c | 45 | I think I can allow myself a pat on the back. |
| 0x2e969d | 30 | Your Highness... I am sorry... |
| 0x2f044d | 16 | polySurface24627 |
| 0x2f045e | 16 | polySurface24628 |
| 0x2f046f | 16 | polySurface24629 |
| 0x2f0480 | 16 | polySurface24630 |
| 0x2f0491 | 15 | polySurface2330 |
| 0x2f04a1 | 13 | Nrrgh... hah. |
| 0x2f04af | 20 | Is this... blood...? |
| 0x2f04c4 | 30 | They managed to... wound me?\n |
| 0x2f04e3 | 31 | To bleed me... my own blood...? |
| 0x2f0503 | 40 | ...Very well. You are a worthy opponent. |
| 0x2f0532 | 15 | Here it comes-- |
| 0x2f0542 | 47 | I was not expecting that you would be able to\n |
| 0x2f0572 | 25 | harm me... I commend you. |
| 0x2f058c | 26 | Then here is your reward!! |
| 0x2f05a7 | 36 | Witness the full extent of my power! |
| 0x2f05cc | 46 | Akuruka! Feast thou upon my soul, and bestow\n |
| 0x2f05fb | 22 | upon me thy strength!! |
| 0x2f0612 | 27 | ORRRRRRRRRAAAAAAAAGGHHHHH!! |
| 0x2f062e | 25 | WRRRRAAAAAAAAAAAAGGGHHH!! |
| 0x2f0648 | 6 | Kuon!! |
| 0x2f064f | 16 | I won't let you! |
| 0x2f0660 | 6 | Nggh!? |
| 0x2f0667 | 28 | He's stopped in his tracks-- |
| 0x2f0684 | 16 | Uruuru! Saraana! |
| 0x2f0695 | 90 | ①{W12}⑧{W12}...{W12}②{W12}⑥{W12}③{W12}⑤{W12}...{W12}④{W12}⑦{W12}...{W12}\n |
| 0x2f06f0 | 43 | To the heroes of eld, from whose blood we\n |
| 0x2f071c | 24 | arose, we bow our heads. |
| 0x2f0735 | 82 | ⑨{W12}⑩{W12}...{W12}③{W12}④{W12}...{W12}②{W12}⑧{W12}...{W12}...{W12}\n |
| 0x2f0788 | 46 | We plead your benevolence, your deliverance,\n |
| 0x2f07b7 | 16 | your protection. |
| 0x2f07c8 | 77 | ⑤{W12}⑧{W12}...{W12}⑥{W12}②{W12}⑦...{W12}⑩{W12}②{W12}①{W12}\n |
| 0x2f0816 | 41 | Let your power unmasked ward all evils.\n |
| 0x2f0840 | 49 | Grant us the peace and harmony that knows no end. |
| 0x2f0872 | 7 | pPlane1 |
| 0x2f087a | 11 | pCylinder21 |
| 0x2f0886 | 11 | pCylinder22 |
| 0x2f0892 | 11 | pCylinder29 |
| 0x2f089e | 11 | pCylinder30 |
| 0x2f08aa | 11 | pCylinder31 |
| 0x2f08b6 | 16 | polySurface24641 |
| 0x2f08c7 | 16 | polySurface24642 |
| 0x2f08d8 | 16 | polySurface24643 |
| 0x2f08e9 | 16 | polySurface24644 |
| 0x2f08fa | 16 | polySurface24645 |
| 0x2f090b | 10 | pCylinder2 |
| 0x2f0916 | 11 | pCylinder18 |
| 0x2f0922 | 11 | pCylinder19 |
| 0x2f092e | 11 | pCylinder20 |
| 0x2f093a | 11 | pCylinder23 |
| 0x2f0946 | 11 | pCylinder24 |
| 0x2f0952 | 11 | pCylinder25 |
| 0x2f095e | 11 | pCylinder26 |
| 0x2f096a | 11 | pCylinder27 |
| 0x2f0976 | 11 | pCylinder28 |
| 0x2f0982 | 11 | pCylinder32 |
| 0x2f098e | 16 | polySurface24632 |
| 0x2f099f | 16 | polySurface24633 |
| 0x2f09b0 | 16 | polySurface24634 |
| 0x2f09c1 | 16 | polySurface24635 |
| 0x2f09d2 | 16 | polySurface24636 |
| 0x2f09e3 | 16 | polySurface24637 |
| 0x2f09f4 | 16 | polySurface24638 |
| 0x2f0a05 | 16 | polySurface24639 |
| 0x2f0a16 | 16 | polySurface24640 |
| 0x2f0a27 | 16 | polySurface24646 |
| 0x2f0a38 | 16 | polySurface24647 |
| 0x2f0a49 | 11 | Center_desk |
| 0x2f0a55 | 12 | Center_desk1 |
| 0x2f0a62 | 15 | polySurface2086 |
| 0x2f0a72 | 15 | polySurface2087 |
| 0x2f0a82 | 8 | pCube164 |
| 0x2f0a8b | 15 | polySurface1985 |
| 0x2f0a9b | 15 | polySurface1874 |
| 0x2f0aab | 15 | polySurface2124 |
| 0x2f0abb | 15 | polySurface2125 |
| 0x2f0acb | 15 | polySurface2126 |
| 0x2f0adb | 7 | fire024 |
| 0x2f0ae3 | 7 | fire025 |
| 0x2f0aeb | 7 | fire026 |
| 0x2f0af3 | 7 | fire027 |
| 0x2f0afb | 7 | fire028 |
| 0x2f0b03 | 7 | fire029 |
| 0x2f0b0b | 7 | fire030 |
| 0x2f0b13 | 7 | fire031 |
| 0x2f0b1b | 7 | fire032 |
| 0x2f0b23 | 7 | fire033 |
| 0x2f0b2b | 7 | fire034 |
| 0x2f0b33 | 7 | fire035 |
| 0x2f0b3b | 7 | fire036 |
| 0x2f0b43 | 7 | fire037 |
| 0x2f0b4b | 7 | fire038 |
| 0x2f0b53 | 7 | fire039 |
| 0x2f0b5b | 16 | polySurface24623 |
| 0x2f0b6c | 16 | polySurface24624 |
| 0x2f0b7d | 16 | polySurface24625 |
| 0x2f0b8e | 16 | polySurface24590 |
| 0x2f0b9f | 16 | polySurface24591 |
| 0x2f0bb0 | 16 | polySurface24593 |
| 0x2f0bc1 | 16 | polySurface24595 |
| 0x2f0bd2 | 16 | polySurface24597 |
| 0x2f0be3 | 6 | target |
| 0x2f0bea | 17 | Ghhh... nghh...\n |
| 0x2f0bfc | 19 | GHAAAAAAAAHHHHHHH!? |
| 0x2f0c10 | 14 | What... is...? |
| 0x2f0c1f | 42 | Where there is a collar, so too there is\n |
| 0x2f0c4a | 8 | a leash. |
| 0x2f0c53 | 44 | Did you truly believe the Akuruka would be\n |
| 0x2f0c80 | 43 | given freely without a way to control the\n |
| 0x2f0cac | 13 | raging beast? |
| 0x2f0cba | 50 | You two... Of course... You are that woman's...!\n |
| 0x2f0ced | 41 | The GALL! So you were waiting for this,\n |
| 0x2f0d17 | 15 | the whole time! |
| 0x2f0d27 | 48 | But I... I will not be stopped by such tricks... |
| 0x2f0d58 | 20 | We will not let you. |
| 0x2f0d6d | 23 | Ngh.... NRRRRRRRRGGHH!! |
| 0x2f0d85 | 13 | Gh... agh...! |
| 0x2f0d93 | 24 | Huh? What's wrong, Kuon? |
| 0x2f0dac | 45 | N-No, it's nothing... Just feeling a little\n |
| 0x2f0dda | 6 | dizzy. |
| 0x2f0de1 | 16 | If you say so... |
| 0x2f0df6 | 48 | It seems to work through a different system...\n |
| 0x2f0e27 | 25 | but this is definitely... |
| 0x2f0e41 | 15 | The Ohn Riyaak! |
| 0x2f0e51 | 13 | Ugh... gah... |
| 0x2f0e5f | 27 | A-Are you sure you're OK?\n |
| 0x2f0e7b | 20 | You're turning pale! |
| 0x2f0e90 | 40 | I'll... be fine... More importantly...\n |
| 0x2f0eb9 | 19 | Now's our chance... |
| 0x2f0ecd | 20 | We have to act, now! |
| 0x2f0ee2 | 36 | Y-Yeah... got it! Come on, everyone! |
| 0x2f0f07 | 45 | Got it! Better put your back into this one,\n |
| 0x2f0f35 | 6 | Kiwru! |
| 0x2f0f3c | 6 | Right! |
| 0x2f0f43 | 35 | Time to end this! On my mark, Ougi! |
| 0x2f0f67 | 19 | Ready when you are. |
| 0x2f0f7b | 14 | Hrrrryaaaaaah! |
| 0x2f0f8a | 11 | Rrraaaaah!! |
| 0x2f0f96 | 10 | Take this! |
| 0x2f0fa1 | 14 | Haaaaaaaaaah!! |
| 0x2f0fb0 | 23 | NGH...! N-NGHUUOOOOGH!! |
| 0x2f0fc8 | 10 | Atuy, now! |
| 0x2f0fd3 | 22 | AhahahaHAHAHAHAHAHAHA! |
| 0x2f0fea | 14 | Nghuuurrghh... |
| 0x2f0ff9 | 19 | Hiyaaaaaaaaaaaaah!! |
| 0x2f1010 | 21 | And now... it's over. |
| 0x2f1026 | 13 | We... did it? |
| 0x2f1037 | 18 | Hmph... Heh heh... |
| 0x2f104a | 27 | Is that... truly your best? |
| 0x2f1066 | 5 | Wha-- |
| 0x2f106c | 43 | Impossible... After taking so many hits...? |
| 0x2f1098 | 27 | Ngh...! Everyone, get back! |
| 0x2f10b4 | 34 | You believed that would suffice... |
| 0x2f10d7 | 18 | Do not INSULT ME!! |
| 0x2f10ea | 20 | Everyone, GET DOWN!! |
| 0x2f10ff | 12 | pPlane1_anum |
| 0x2f110c | 8 | murasaki |
| 0x2f1115 | 16 | polySurface24777 |
| 0x2f1126 | 16 | polySurface24778 |
| 0x2f1137 | 16 | polySurface24779 |
| 0x2f1148 | 16 | polySurface24780 |
| 0x2f1159 | 16 | polySurface24781 |
| 0x2f116a | 16 | polySurface24782 |
| 0x2f117b | 16 | polySurface24783 |
| 0x2f118c | 16 | polySurface24784 |
| 0x2f119d | 16 | polySurface24785 |
| 0x2f11ae | 16 | polySurface24786 |
| 0x2f11bf | 16 | polySurface24787 |
| 0x2f11d0 | 16 | polySurface24788 |
| 0x2f11e1 | 16 | polySurface24789 |
| 0x2f11f2 | 16 | polySurface24790 |
| 0x2f1203 | 16 | polySurface24791 |
| 0x2f1214 | 11 | pCylinder33 |
| 0x2f1220 | 11 | pCylinder34 |
| 0x2f122c | 11 | pCylinder35 |
| 0x2f1238 | 11 | pCylinder36 |
| 0x2f1244 | 11 | pCylinder37 |
| 0x2f1250 | 11 | pCylinder38 |
| 0x2f125c | 7 | pPlane4 |
| 0x2f1264 | 7 | pPlane5 |
| 0x2f126c | 7 | pPlane6 |
| 0x2f1274 | 7 | pPlane7 |
| 0x2f127c | 7 | pPlane8 |
| 0x2f1284 | 7 | pPlane9 |
| 0x2f128c | 8 | pPlane10 |
| 0x2f1295 | 8 | pPlane11 |
| 0x2f129e | 8 | pPlane12 |
| 0x2f12a7 | 8 | pPlane13 |
| 0x2f12b0 | 8 | pPlane14 |
| 0x2f12b9 | 8 | pPlane15 |
| 0x2f12c2 | 8 | pPlane16 |
| 0x2f12cb | 8 | pPlane17 |
| 0x2f12d4 | 8 | pPlane18 |
| 0x2f12dd | 8 | pPlane19 |
| 0x2f12e6 | 8 | pPlane20 |
| 0x2f12ef | 8 | pPlane21 |
| 0x2f12f8 | 8 | pPlane22 |
| 0x2f1301 | 8 | pPlane23 |
| 0x2f130a | 8 | pPlane24 |
| 0x2f1313 | 8 | pPlane25 |
| 0x2f131c | 8 | pPlane26 |
| 0x2f1325 | 8 | pPlane27 |
| 0x2f132e | 8 | pPlane28 |
| 0x2f1337 | 8 | pPlane29 |
| 0x2f1340 | 8 | pPlane30 |
| 0x2f1349 | 8 | pPlane31 |
| 0x2f1352 | 8 | pPlane32 |
| 0x2f135b | 8 | pPlane33 |
| 0x2f1364 | 8 | pPlane34 |
| 0x2f136d | 8 | pPlane35 |
| 0x2f1376 | 8 | pPlane36 |
| 0x2f137f | 8 | pPlane37 |
| 0x2f1388 | 8 | pPlane38 |
| 0x2f1391 | 8 | pPlane39 |
| 0x2f139a | 8 | pPlane40 |
| 0x2f13a3 | 8 | pPlane41 |
| 0x2f13ac | 8 | pPlane42 |
| 0x2f13b5 | 8 | pPlane43 |
| 0x2f13be | 8 | pPlane44 |
| 0x2f13c7 | 8 | pPlane45 |
| 0x2f13d0 | 8 | pPlane46 |
| 0x2f13d9 | 8 | pPlane47 |
| 0x2f13e2 | 8 | pPlane48 |
| 0x2f13eb | 8 | pPlane49 |
| 0x2f13f4 | 8 | pPlane50 |
| 0x2f13fd | 8 | pPlane51 |
| 0x2f1406 | 30 | Guh... hahh... You guys... OK? |
| 0x2f1425 | 47 | Y-Yes... I'm fine... Nekone, are you all right? |
| 0x2f1455 | 46 | Only thanks to your shielding me, dear sister. |
| 0x2f1484 | 25 | Perfectly fine over here! |
| 0x2f149e | 29 | ...A touch close for comfort. |
| 0x2f14bc | 22 | A bit TOO close, yeah? |
| 0x2f14d3 | 24 | Well, that's worrying... |
| 0x2f14ec | 30 | What in the world was that...? |
| 0x2f150b | 11 | Ngh...ah... |
| 0x2f1517 | 26 | Wh-Where is Her Highness-- |
| 0x2f1532 | 46 | Ngh... She is... safe. She has merely fallen\n |
| 0x2f1561 | 12 | unconscious. |
| 0x2f156e | 15 | D-Dear brother! |
| 0x2f157e | 45 | Do not worry for me. Above all else, do not\n |
| 0x2f15ac | 42 | lower your guard. This is far from over... |
| 0x2f15d7 | 7 | Huh...? |
| 0x2f15df | 8 | FOOLS... |
| 0x2f15e8 | 4 | Wh-- |
| 0x2f15ed | 7 | N-No... |
| 0x2f15f5 | 30 | We couldn't do... anything...? |
| 0x2f1614 | 7 | env_hip |
| 0x2f161c | 40 | DID YOU TRULY THINK YOU COULD SEAL ME?\n |
| 0x2f1645 | 38 | YOU, WHO LACKED THE STRENGTH EVEN TO\n |
| 0x2f166c | 8 | BREATHE? |
| 0x2f1675 | 8 | Nnngh... |
| 0x2f167e | 46 | Urgh... I knew I was pushing the two of them\n |
| 0x2f16ad | 9 | too hard. |
| 0x2f16b7 | 41 | Now he's at full power... and escape is\n |
| 0x2f16e1 | 31 | probably out of the question.\n |
| 0x2f1701 | 26 | This might be it for us... |
| 0x2f171c | 45 | What do we do...? I've got no more cards up\n |
| 0x2f174a | 12 | my sleeve... |
| 0x2f1757 | 45 | It's not over, Haku. It is too early yet to\n |
| 0x2f1785 | 28 | give up. Mark Vurai closely. |
| 0x2f17a2 | 5 | What? |
| 0x2f17a8 | 31 | The form that he is in now...\n |
| 0x2f17c8 | 32 | His powers are still incomplete! |
| 0x2f17e9 | 47 | The sealing has had a definite effect on him,\n |
| 0x2f1819 | 31 | at least. And if that is true-- |
| 0x2f1839 | 41 | DO YOU BELIEVE YOU CAN STILL OPPOSE ME?\n |
| 0x2f1863 | 22 | YOU CAN BARELY STAND-- |
| 0x2f187a | 16 | RRGH... Y-YOU... |
| 0x2f188b | 37 | That's enough! Stop! You can't take-- |
| 0x2f18b1 | 42 | GRRAAAAGH... CEASE THIS FUTILE STRUGGLING! |
| 0x2f18dc | 10 | You two... |
| 0x2f18e7 | 17 | Haku... stand up. |
| 0x2f18f9 | 5 | Kuon? |
| 0x2f18ff | 47 | Haku... if you falter now, then their efforts\n |
| 0x2f192f | 24 | will all be for nothing. |
| 0x2f1948 | 34 | You guys... still got this, right? |
| 0x2f196b | 19 | Th-This is nothing. |
| 0x2f197f | 29 | Hah... who do you think I am? |
| 0x2f199d | 41 | If my dear sister remains in the fight,\n |
| 0x2f19c7 | 43 | then you shall have my sword until the end. |
| 0x2f19f3 | 45 | W-We won't let you fight alone, Sir Haku...\n |
| 0x2f1a21 | 14 | Right, Cocopo? |
| 0x2f1a4d | 44 | Gotta make sure to finish him off good and\n |
| 0x2f1a7a | 17 | proper this time. |
| 0x2f1a8c | 29 | My mind was made up long ago! |
| 0x2f1aaa | 45 | No need to ask me. Doesn't look like we got\n |
| 0x2f1ad8 | 31 | much of a choice anymore, yeah? |
| 0x2f1af8 | 27 | I leave the rest... to you. |
| 0x2f1b14 | 15 | Let's go, Haku. |
| 0x2f1b24 | 5 | Yeah! |
| 0x2f1b2a | 27 | HAH... HAHAHAHA... I SEE.\n |
| 0x2f1b46 | 20 | AND STILL YOU STAND. |
| 0x2f1b5b | 42 | ALLOW ME TO APOLOGIZE... IT SEEMS I HAVE\n |
| 0x2f1b86 | 20 | TRULY MISJUDGED YOU. |
| 0x2f1b9b | 43 | AND ALLOW ME TO GIVE YOU YOUR DUE PRAISE.\n |
| 0x2f1bc7 | 43 | YOU ARE WARRIORS WORTHY OF STANDING AS MY\n |
| 0x2f1bf3 | 6 | ENEMY. |
| 0x2f1bfa | 45 | VALOR FOR VALOR, I SHALL REPAY YOU IN KIND!\n |
| 0x2f1c28 | 46 | RELISH YOUR FORTUNE, THAT YOU NOW EXPERIENCE\n |
| 0x2f1c57 | 14 | MY TRUE POWER! |
| 0x2f1deb | 42 | 帝都英霊結界／戦闘開始します |
| 0x2f4f80 | 13 | IMPOSSIBLE... |
| 0x2f4f8e | 30 | I HAVE BEEN... BROUGHT LOW...? |
| 0x2f4fad | 23 | HOW COULD... I have...? |
| 0x2f4fc5 | 12 | pPlane1_anum |
| 0x2f4fd2 | 8 | murasaki |
| 0x2f4fdb | 16 | polySurface24637 |
| 0x2f4fec | 16 | polySurface24777 |
| 0x2f4ffd | 16 | polySurface24778 |
| 0x2f500e | 16 | polySurface24779 |
| 0x2f501f | 16 | polySurface24780 |
| 0x2f5030 | 16 | polySurface24781 |
| 0x2f5041 | 16 | polySurface24782 |
| 0x2f5052 | 16 | polySurface24783 |
| 0x2f5063 | 16 | polySurface24784 |
| 0x2f5074 | 16 | polySurface24785 |
| 0x2f5085 | 16 | polySurface24786 |
| 0x2f5096 | 16 | polySurface24787 |
| 0x2f50a7 | 16 | polySurface24788 |
| 0x2f50b8 | 16 | polySurface24789 |
| 0x2f50c9 | 16 | polySurface24790 |
| 0x2f50da | 16 | polySurface24791 |
| 0x2f50eb | 11 | pCylinder22 |
| 0x2f50f7 | 11 | pCylinder24 |
| 0x2f5103 | 11 | pCylinder25 |
| 0x2f510f | 11 | pCylinder26 |
| 0x2f511b | 11 | pCylinder27 |
| 0x2f5127 | 11 | pCylinder28 |
| 0x2f5133 | 11 | pCylinder29 |
| 0x2f513f | 11 | pCylinder30 |
| 0x2f514b | 11 | pCylinder31 |
| 0x2f5157 | 11 | pCylinder32 |
| 0x2f5163 | 11 | pCylinder33 |
| 0x2f516f | 11 | pCylinder34 |
| 0x2f517b | 11 | pCylinder35 |
| 0x2f5187 | 11 | pCylinder36 |
| 0x2f5193 | 11 | pCylinder37 |
| 0x2f519f | 11 | pCylinder38 |
| 0x2f51ab | 7 | pPlane4 |
| 0x2f51b3 | 7 | pPlane5 |
| 0x2f51bb | 7 | pPlane6 |
| 0x2f51c3 | 7 | pPlane7 |
| 0x2f51cb | 7 | pPlane8 |
| 0x2f51d3 | 7 | pPlane9 |
| 0x2f51db | 8 | pPlane10 |
| 0x2f51e4 | 8 | pPlane11 |
| 0x2f51ed | 8 | pPlane12 |
| 0x2f51f6 | 8 | pPlane13 |
| 0x2f51ff | 8 | pPlane14 |
| 0x2f5208 | 8 | pPlane15 |
| 0x2f5211 | 8 | pPlane16 |
| 0x2f521a | 8 | pPlane17 |
| 0x2f5223 | 8 | pPlane18 |
| 0x2f522c | 8 | pPlane19 |
| 0x2f5235 | 8 | pPlane20 |
| 0x2f523e | 8 | pPlane21 |
| 0x2f5247 | 8 | pPlane22 |
| 0x2f5250 | 8 | pPlane23 |
| 0x2f5259 | 8 | pPlane24 |
| 0x2f5262 | 8 | pPlane25 |
| 0x2f526b | 8 | pPlane26 |
| 0x2f5274 | 8 | pPlane27 |
| 0x2f527d | 8 | pPlane28 |
| 0x2f5286 | 8 | pPlane29 |
| 0x2f528f | 8 | pPlane30 |
| 0x2f5298 | 8 | pPlane31 |
| 0x2f52a1 | 8 | pPlane32 |
| 0x2f52aa | 8 | pPlane33 |
| 0x2f52b3 | 8 | pPlane34 |
| 0x2f52bc | 8 | pPlane35 |
| 0x2f52c5 | 8 | pPlane36 |
| 0x2f52ce | 8 | pPlane37 |
| 0x2f52d7 | 8 | pPlane38 |
| 0x2f52e0 | 8 | pPlane39 |
| 0x2f52e9 | 8 | pPlane40 |
| 0x2f52f2 | 8 | pPlane41 |
| 0x2f52fb | 8 | pPlane42 |
| 0x2f5304 | 8 | pPlane43 |
| 0x2f530d | 8 | pPlane44 |
| 0x2f5316 | 8 | pPlane45 |
| 0x2f531f | 8 | pPlane46 |
| 0x2f5328 | 8 | pPlane47 |
| 0x2f5331 | 8 | pPlane48 |
| 0x2f533a | 8 | pPlane49 |
| 0x2f5343 | 8 | pPlane50 |
| 0x2f534c | 8 | pPlane51 |
| 0x2f5355 | 25 | Hahh... hahh... hahh...\n |
| 0x2f536f | 23 | Hee hee, hee hee hee... |
| 0x2f5387 | 32 | Ahahahahahaha! Oh, what fun...\n |
| 0x2f53a8 | 21 | That was SO much FUN! |
| 0x2f53be | 26 | Ngh... hah... gh... hah... |
| 0x2f53d9 | 49 | Th-That was... nothing... A good woman never...\n |
| 0x2f540b | 17 | loses her cool... |
| 0x2f541d | 35 | I have nothing... to fear from...\n |
| 0x2f5441 | 19 | Vurai the Vanguard! |
| 0x2f5455 | 49 | Dear sister, I suggest you dab at yourself with\n |
| 0x2f5487 | 42 | this. You appear to be perspiring rather\n |
| 0x2f54b2 | 8 | heavily. |
| 0x2f54bb | 45 | So that's... what it's like to fight one of\n |
| 0x2f54e9 | 29 | the bearers of the Akuruka... |
| 0x2f5507 | 30 | Yeah... That was real close... |
| 0x2f5526 | 28 | My legs are still shaking... |
| 0x2f5543 | 45 | If he had released the Akuruka's full power-- |
| 0x2f5571 | 21 | Ugh... hh... hahhh... |
| 0x2f5587 | 5 | Kuon? |
| 0x2f558d | 44 | I... I'm fine. Just... a little lightheaded. |
| 0x2f55ba | 38 | I suppose that fight just wore me out. |
| 0x2f55e1 | 34 | You sure you're not hurt anywhere? |
| 0x2f5604 | 48 | ...I'm fine, really... Ahaha, are you worrying\n |
| 0x2f5635 | 13 | about me now? |
| 0x2f5643 | 47 | 'Course I am! Why wouldn't I be worried about\n |
| 0x2f5673 | 4 | you? |
| 0x2f5678 | 26 | ...Oh, ah... I suppose so. |
| 0x2f5697 | 49 | Oshtor looks down upon Vurai's motionless body,\n |
| 0x2f56c9 | 19 | sorrow in his eyes. |
| 0x2f56dd | 19 | Dear brother, here. |
| 0x2f56f1 | 46 | A familiar Akuruka has fallen out of Vurai's\n |
| 0x2f5720 | 35 | clothes. Nekone hands it to Oshtor. |
| 0x2f5744 | 49 | Oshtor takes the mask and puts it on. He closes\n |
| 0x2f5776 | 45 | his eyes briefly, as if to remember its feel. |
| 0x2f57a4 | 44 | Once he opens his eyes again, Nekone helps\n |
| 0x2f57d1 | 31 | him walk, and he turns to Anju. |
| 0x2f57f1 | 47 | Your Highness. I deeply apologize for my late\n |
| 0x2f5821 | 8 | arrival. |
| 0x2f582a | 38 | I am... so glad...  she's all right... |
| 0x2f5851 | 17 | ...Your Highness? |
| 0x2f5863 | 11 | Ah... hh... |
| 0x2f586f | 24 | Anju slowly reaches out. |
| 0x2f5888 | 46 | But it doesn't seem as though her empty eyes\n |
| 0x2f58b7 | 28 | have caught sight of Oshtor. |
| 0x2f58d4 | 12 | What the...? |
| 0x2f58e1 | 36 | Y-Your Highness? What is the matter? |
| 0x2f5906 | 34 | Princess? Can you hear our voices? |
| 0x2f5929 | 11 | Hh... ah... |
| 0x2f5935 | 45 | Oshtor kneels before Anju, and gently takes\n |
| 0x2f5963 | 9 | her hand. |
| 0x2f596d | 22 | ...A-Aa... hh... hh... |
| 0x2f5984 | 50 | Anju attempts to speak again, but all that comes\n |
| 0x2f59b7 | 45 | out of her mouth are labored, raspy whimpers. |
| 0x2f59e5 | 43 | She closes her eyes in frustration, tears\n |
| 0x2f5a11 | 36 | beginning to stream down her cheeks. |
| 0x2f5a36 | 32 | ...Lady Kuon, may I ask you to-- |
| 0x2f5a57 | 33 | Yes. Princess, can you hear me?\n |
| 0x2f5a79 | 30 | Please open your mouth for me. |
| 0x2f5a98 | 44 | Kuon examines Anju's throat with a serious\n |
| 0x2f5ac5 | 11 | expression. |
| 0x2f5ad1 | 50 | She then holds Anju's eyelids open with delicate\n |
| 0x2f5b04 | 30 | care, carefully examining her. |
| 0x2f5b23 | 47 | She checks her pulse and her temperature, and\n |
| 0x2f5b53 | 42 | after everything, Kuon sighs and looks up. |
| 0x2f5b7e | 49 | It must have been a powerful poison. Her throat\n |
| 0x2f5bb0 | 21 | is all but destroyed. |
| 0x2f5bc6 | 47 | As long as she's like this, she won't be able\n |
| 0x2f5bf6 | 9 | to speak. |
| 0x2f5c00 | 5 | No... |
| 0x2f5c06 | 43 | What's more serious, though... is her mind. |
| 0x2f5c32 | 5 | Mind? |
| 0x2f5c38 | 43 | The poison in question has a mind-numbing\n |
| 0x2f5c64 | 7 | effect. |
| 0x2f5c6c | 48 | It's a dangerous drug that can be used to ease\n |
| 0x2f5c9d | 47 | pain, but overdosing can easily destroy one's\n |
| 0x2f5ccd | 7 | mind... |
| 0x2f5cda | 41 | A sharp inhale ripples through the group. |
| 0x2f5d04 | 20 | ...Can she be cured? |
| 0x2f5d19 | 48 | Yes. It won't be easy, but if we act fast with\n |
| 0x2f5d4a | 47 | the right treatment, we can avoid any lasting\n |
| 0x2f5d7a | 8 | effects. |
| 0x2f5d83 | 9 | I... see. |
| 0x2f5d8d | 30 | Thank goodness... Miss Anju... |
| 0x2f5dac | 41 | Whew, well... that gave me quite a scare. |
| 0x2f5dd6 | 50 | But we'll have to get somewhere we can find some\n |
| 0x2f5e09 | 13 | peace, first. |
| 0x2f5e17 | 50 | Got it. We need to get out of here before anyone\n |
| 0x2f5e4a | 14 | else finds us. |
| 0x2f5e59 | 45 | Huh? But General Vurai has been defeated...\n |
| 0x2f5e87 | 26 | Why do we need to run now? |
| 0x2f5ea2 | 47 | No... If he wasn't the mastermind behind this\n |
| 0x2f5ed2 | 44 | whole plan, we can't stay here for too long. |
| 0x2f5eff | 48 | From an outsider's perspective, we infiltrated\n |
| 0x2f5f30 | 42 | the princess's room, attacked Vurai, and\n |
| 0x2f5f5b | 14 | kidnapped her. |
| 0x2f5f6a | 40 | Wh... But... But my brother is innocent! |
| 0x2f5f93 | 44 | And how exactly do you plan on proving that? |
| 0x2f5fc0 | 49 | That's... It wouldn't be necessary to do such a\n |
| 0x2f5ff2 | 7 | thing-- |
| 0x2f5ffa | 41 | ...We have Her Highness as our witness.\n |
| 0x2f6024 | 22 | She can tell them--Ah! |
| 0x2f603b | 48 | That's going to be difficult with the princess\n |
| 0x2f606c | 14 | in this state. |
| 0x2f607b | 45 | Not to mention anyone with a grudge against\n |
| 0x2f60a9 | 45 | Oshtor will jump at the chance to prove him\n |
| 0x2f60d7 | 7 | guilty. |
| 0x2f60df | 45 | By the time the princess recovers enough to\n |
| 0x2f610d | 43 | testify, they'd already have our heads on\n |
| 0x2f6139 | 6 | pikes. |
| 0x2f6140 | 49 | The evident plan was to keep her silent and use\n |
| 0x2f6172 | 48 | her for her status. A political marionette, as\n |
| 0x2f61a3 | 8 | it were. |
| 0x2f61ac | 18 | That's so cruel... |
| 0x2f61bf | 49 | Man oh man. So you're saying that the big fella\n |
| 0x2f61f1 | 45 | over there wasn't even the one behind it all? |
| 0x2f621f | 45 | Jachdwalt rolls his shoulders wearily as he\n |
| 0x2f624d | 22 | glances back to Vurai. |
| 0x2f6264 | 44 | Yes. Vurai is not one for such scheming as\n |
| 0x2f6291 | 39 | this. The mastermind must be elsewhere. |
| 0x2f62b9 | 48 | I get the feeling that Honoka went into hiding\n |
| 0x2f62ea | 39 | because this mastermind had framed her. |
| 0x2f6312 | 45 | But the question is, where do we go now...?\n |
| 0x2f6340 | 23 | Oshtor, any good ideas? |
| 0x2f6358 | 13 | ...Ennakamuy. |
| 0x2f6366 | 7 | Huh...? |
| 0x2f636e | 40 | It is in the far reaches of this land,\n |
| 0x2f6397 | 48 | surrounded by mountainous terrain... A natural\n |
| 0x2f63c8 | 9 | fortress. |
| 0x2f63d2 | 50 | If we go there, we should be able to protect the\n |
| 0x2f6405 | 38 | princess from any pursuers for a time. |
| 0x2f642c | 19 | Isn't Ennakamuy...? |
| 0x2f6440 | 24 | Yes. It is our homeland. |
| 0x2f6459 | 47 | I am sorry, Kiwru. This may cause trouble for\n |
| 0x2f6489 | 29 | your family, and the people-- |
| 0x2f64a7 | 45 | Please don't say such things, brother. This\n |
| 0x2f64d5 | 30 | crisis involves all of Yamato. |
| 0x2f64f4 | 13 | ...Thank you. |
| 0x2f6502 | 47 | They look so weak... like they could collapse\n |
| 0x2f6532 | 14 | at any moment. |
| 0x2f6541 | 50 | They're not saying much, but that "path" and the\n |
| 0x2f6574 | 27 | whole sealing spell thing-- |
| 0x2f6590 | 47 | It'll be way too dangerous to ask any more of\n |
| 0x2f65c0 | 7 | them... |
| 0x2f65c8 | 44 | I walk over to the fallen guards and start\n |
| 0x2f65f5 | 26 | pulling off their clothes. |
| 0x2f6610 | 26 | Ougi, give me a hand here. |
| 0x2f662b | 49 | Aha, you intend on disguising us as soldiers to\n |
| 0x2f665d | 39 | escape. A fine plan... Exhilaratingly\n |
| 0x2f6685 | 12 | suspenseful. |
| 0x2f6692 | 10 | ...Master. |
| 0x2f669d | 46 | You need not worry about us. Please--we will\n |
| 0x2f66cc | 26 | be able to withstand this. |
| 0x2f66e7 | 46 | No, you two rest up. You guys can barely walk. |
| 0x2f6716 | 11 | Irrelevant. |
| 0x2f6722 | 49 | We intend on carrying out your will, regardless\n |
| 0x2f6754 | 36 | of whether it may cost us our lives. |
| 0x2f6779 | 21 | No. This is an order. |
| 0x2f678f | 48 | Wait, what!? They were planning on sacrificing\n |
| 0x2f67c0 | 11 | themselves? |
| 0x2f67cc | 15 | ...As you wish. |
| 0x2f67dc | 45 | We'll have the princess hide in that wicker\n |
| 0x2f680a | 6 | trunk. |
| 0x2f6811 | 48 | We'll get a cart, and carry her on that. If we\n |
| 0x2f6842 | 45 | play it cool, I think we can make it out of\n |
| 0x2f6870 | 12 | the capital. |
| 0x2f687d | 43 | And if we are to be discovered during our\n |
| 0x2f68a9 | 7 | flight? |
| 0x2f68b1 | 49 | We'll say the trunk's full of gifts for nobles.\n |
| 0x2f68e3 | 47 | If we're confident, they won't suspect a thing. |
| 0x2f6913 | 48 | Although I suppose it's a gamble of whether we\n |
| 0x2f6944 | 23 | can fool them or not... |
| 0x2f695c | 33 | Wonder if this thing still works? |
| 0x2f697e | 47 | As I speak, I pull out a certain handy little\n |
| 0x2f69ae | 4 | box. |
| 0x2f69b3 | 9 | That is-- |
| 0x2f69bd | 50 | The seal of the Mikado... I had no idea that you\n |
| 0x2f69f0 | 31 | had been bestowed such a token. |
| 0x2f6a10 | 47 | It's a little complicated. Last time I showed\n |
| 0x2f6a40 | 45 | it to the guards at the Uzurushan ruins, it\n |
| 0x2f6a6e | 12 | worked fine. |
| 0x2f6a7b | 47 | Circumstances are different. It may not work,\n |
| 0x2f6aab | 47 | especially in the case of those who know what\n |
| 0x2f6adb | 16 | transpired here. |
| 0x2f6aec | 45 | However, the guards outside should still be\n |
| 0x2f6b1a | 49 | unaware of all this. We may be able to convince\n |
| 0x2f6b4c | 5 | them. |
| 0x2f6b52 | 50 | In the current political confusion, few would be\n |
| 0x2f6b85 | 50 | able to maintain their composure at the sight of\n |
| 0x2f6bb8 | 10 | that seal. |
| 0x2f6bc3 | 43 | Good to hear. Guess I'll be putting it to\n |
| 0x2f6bef | 15 | good use, then. |
| 0x2f6bff | 38 | Are you... sure this is going to work? |
| 0x2f6c26 | 44 | Kiwru, this isn't a matter of whether it's\n |
| 0x2f6c53 | 14 | going to work. |
| 0x2f6c62 | 4 | Huh? |
| 0x2f6c67 | 28 | We're going to MAKE it work. |
| 0x2f6c84 | 15 | Heh. Well said. |
| 0x2f6c94 | 49 | Very like you, Haku. Reminds me of the face you\n |
| 0x2f6cc6 | 42 | make when you're talking yourself out of\n |
| 0x2f6cf1 | 8 | working. |
| 0x2f6cfa | 28 | ...Hey, that's uncalled for. |
| 0x2f6d17 | 46 | In any case, there's one last precaution I'd\n |
| 0x2f6d46 | 21 | like to take care of. |
| 0x2f6d5c | 30 | Ougi, can I ask a small favor? |
| 0x2f6d7b | 9 | Ask away. |
| 0x2f6d85 | 48 | Raiko and Dekopompo's soldiers should still be\n |
| 0x2f6db6 | 29 | stuck outside the city walls. |
| 0x2f6dd4 | 46 | Yes, it seemed as though their stalemate was\n |
| 0x2f6e03 | 21 | keeping them rather-- |
| 0x2f6e19 | 49 | As Ougi speaks, however, he seems to understand\n |
| 0x2f6e4b | 48 | what I'm getting at. A faint smile crosses his\n |
| 0x2f6e7c | 5 | face. |
| 0x2f6e82 | 31 | ...I see. So that is your ploy. |
| 0x2f6ea2 | 45 | Yep. Just say it's an order from Vurai, and\n |
| 0x2f6ed0 | 18 | open up the gates. |
| 0x2f6ee3 | 44 | If that happens, I'm sure all of them will\n |
| 0x2f6f10 | 29 | try to rush into the capital. |
| 0x2f6f2e | 48 | And we slip away amidst the confusion. Haha...\n |
| 0x2f6f5f | 39 | your ideas are always quite refreshing. |
| 0x2f6f87 | 46 | All we need now is something that'll make it\n |
| 0x2f6fb6 | 35 | seem more like an order from Vurai. |
| 0x2f6fda | 50 | ...Perhaps we should try searching Vurai for any\n |
| 0x2f700d | 17 | personal effects. |
| 0x2f701f | 44 | We look through everything left on Vurai's\n |
| 0x2f704c | 7 | person. |
| 0x2f7054 | 48 | We're not exactly comfortable doing it, but we\n |
| 0x2f7085 | 39 | really don't have the time to complain. |
| 0x2f70ad | 50 | After fumbling around for a little while, I feel\n |
| 0x2f70e0 | 33 | something hard hit my fingertips. |
| 0x2f7102 | 49 | I pull out a golden circle about the size of my\n |
| 0x2f7134 | 40 | hand, with an intricate engraving on it. |
| 0x2f715d | 21 | Some kind of seal...? |
| 0x2f7173 | 49 | Yes. It is a golden seal that our liege bestows\n |
| 0x2f71a5 | 43 | as proof of being one of the Eight Pillar\n |
| 0x2f71d1 | 9 | Generals. |
| 0x2f71db | 46 | One who holds this seal is either one of the\n |
| 0x2f720a | 44 | Eight Pillar Generals, or under the direct\n |
| 0x2f7237 | 15 | command of one. |
| 0x2f7247 | 48 | Of course, the same authority would be granted\n |
| 0x2f7278 | 35 | to a letter stamped with this seal. |
| 0x2f729c | 50 | Sounds like exactly what we need. I'll just help\n |
| 0x2f72cf | 13 | myself, then. |
| 0x2f72dd | 25 | Now then, Haku, if I may. |
| 0x2f72f7 | 5 | Sure. |
| 0x2f72fd | 47 | Ougi extracts some paper and a scribe's brush\n |
| 0x2f732d | 43 | from a nearby desk, and quickly begins to\n |
| 0x2f7359 | 6 | write. |
| 0x2f7360 | 47 | He presses the seal to it, and in no time, he\n |
| 0x2f7390 | 44 | holds in his hand an "official order" from\n |
| 0x2f73bd | 6 | Vurai. |
| 0x2f73c4 | 48 | You'd never be able to tell what a rush job it\n |
| 0x2f73f5 | 43 | is by looking at it. It's actually pretty\n |
| 0x2f7421 | 11 | impressive. |
| 0x2f742d | 49 | Hmhmhm. The pieces are in place... Now all that\n |
| 0x2f745f | 37 | remains is to set the game in motion. |
| 0x2f7485 | 47 | You know, it's been on my mind for a while...\n |
| 0x2f74b5 | 44 | but I'd think he'd be a better conman than\n |
| 0x2f74e2 | 14 | anything else. |
| 0x2f74f1 | 43 | I suppose I'm off to go make a scene, then. |
| 0x2f751d | 26 | And I shall accompany you. |
| 0x2f7538 | 24 | A moment please, Nosuri. |
| 0x2f7551 | 49 | Oshtor halts the enthusiastic Nosuri, and turns\n |
| 0x2f7583 | 17 | instead to Kiwru. |
| 0x2f7595 | 36 | Kiwru, I wish for you to go instead. |
| 0x2f75ba | 27 | Huh!? You want... me to go? |
| 0x2f75d6 | 50 | Yes. There is a duty I would have you perform on\n |
| 0x2f7609 | 10 | my behalf. |
| 0x2f7614 | 48 | Tell my direct subordinates what happened, and\n |
| 0x2f7645 | 47 | arrange for them and their families to escape\n |
| 0x2f7675 | 9 | the city. |
| 0x2f767f | 49 | I am afraid that I will be unable to personally\n |
| 0x2f76b1 | 46 | prevent them from coming to harm, as matters\n |
| 0x2f76e0 | 10 | stand now. |
| 0x2f76eb | 41 | B-But I am not ready to take on such an\n |
| 0x2f7715 | 15 | important task! |
| 0x2f7725 | 47 | The others would not have their trust, as you\n |
| 0x2f7755 | 42 | would. Only you can do this, as my sworn\n |
| 0x2f7780 | 8 | brother. |
| 0x2f7789 | 50 | Kiwru hesitates for a moment, uncertainty in his\n |
| 0x2f77bc | 39 | eyes, but eventually he nods--resolute. |
| 0x2f77e4 | 32 | Understood! You can count on me! |
| 0x2f7805 | 30 | Shall we be on our way, Kiwru? |
| 0x2f7824 | 4 | Yes! |
| 0x2f7829 | 49 | Kiwru nods fiercely, then follows Ougi down the\n |
| 0x2f785b | 7 | stairs. |
| 0x2f7863 | 49 | Now then, Your Highness. I do apologize for the\n |
| 0x2f7895 | 43 | discomfort, but please bear it for a while. |
| 0x2f78c1 | 12 | Up you go... |
| 0x2f78ce | 49 | Jachdwalt hoists Anju up, lowering her into the\n |
| 0x2f7900 | 47 | Sorry about this, princess. It shouldn't take\n |
| 0x2f7930 | 39 | long, so just hang on for a little bit. |
| 0x2f7958 | 12 | Nh... hhh... |
| 0x2f7965 | 23 | Oshtor, you get in too. |
| 0x2f797d | 13 | No, I shall-- |
| 0x2f798b | 47 | Get in the trunk, Oshtor. Who're you kidding?\n |
| 0x2f79bb | 49 | You can barely move, and anyone could recognize\n |
| 0x2f79ed | 4 | you. |
| 0x2f79f2 | 9 | ...Nrrgh. |
| 0x2f79fc | 43 | Oshtor resists a little, but we manage to\n |
| 0x2f7a28 | 35 | wrangle him into the trunk as well. |
| 0x2f7a4c | 41 | Uruuru, Saraana, you two get in this one. |
| 0x2f7a76 | 42 | We highly disapprove of this decision...\n |
| 0x2f7aa1 | 25 | but an order is an order. |
| 0x2f7abb | 47 | Shinonon, make sure you look after the two of\n |
| 0x2f7aeb | 25 | Yep! You can count on me! |
| 0x2f7b05 | 46 | After the twins get in, Shinonon nimbly hops\n |
| 0x2f7b34 | 25 | into the trunk with them. |
| 0x2f7b4e | 6 | Now... |
| 0x2f7b55 | 48 | Hmmm. The hem's not a very good fit, but it'll\n |
| 0x2f7b86 | 22 | have to do, I suppose. |
| 0x2f7b9d | 31 | Oh, drat. It's all baggy on me. |
| 0x2f7bbd | 48 | I guess the soldier's clothes are a bit big on\n |
| 0x2f7bee | 42 | Kuon and the others. Everything's pretty\n |
| 0x2f7c19 | 8 | loose... |
| 0x2f7c22 | 47 | And Nekone just looks like a sentient pile of\n |
| 0x2f7c52 | 7 | fabric. |
| 0x2f7c5a | 48 | ...Is there something you would like to say to\n |
| 0x2f7c8b | 3 | me? |
| 0x2f7c8f | 18 | Nope. Not a thing. |
| 0x2f7ca2 | 45 | I'm getting kind of uneasy about this plan,\n |
| 0x2f7cd0 | 32 | but there's no turning back now. |
| 0x2f7cf1 | 44 | I doubt we could stuff any more of us into\n |
| 0x2f7d1e | 13 | this trunk... |
| 0x2f7d2c | 47 | Let's go, everyone. We'll just have to figure\n |
| 0x2f7d5c | 24 | the rest out on the fly. |
| 0x2f7d75 | 15 | Lady-in-waiting |
| 0x2f7d85 | 25 | This is... where we part. |
| 0x2f7d9f | 33 | But... you should come with us... |
| 0x2f7dc1 | 40 | She is right. If you remain here alone-- |
| 0x2f7dea | 44 | I do understand, but I owe a great debt to\n |
| 0x2f7e17 | 12 | Lady Honoka. |
| 0x2f7e24 | 30 | I have to know if she is safe. |
| 0x2f7e43 | 47 | It's easy to see that if she stays within the\n |
| 0x2f7e73 | 47 | capital walls, things aren't going to be easy\n |
| 0x2f7ea3 | 8 | for her. |
| 0x2f7eac | 49 | But... her sense of duty doesn't come just from\n |
| 0x2f7ede | 45 | her position. She's already made up her mind. |
| 0x2f7f0c | 46 | Please take care of Her Highness. I am sorry\n |
| 0x2f7f3b | 42 | that I could not accompany you to the end. |
| 0x2f7f66 | 38 | I wish the best of luck to all of you. |
| 0x2f7f8d | 22 | She bows deeply to us. |
| 0x2f7fa4 | 46 | Thanks for helping us get this far... C'mon,\n |
| 0x2f7fd3 | 5 | guys. |
| 0x2f7fd9 | 47 | I just leave her with a brief, curt farewell,\n |
| 0x2f8009 | 47 | and pull the cart forward without looking back. |
| 0x2f8039 | 48 | Somehow, I can feel her remaining in that deep\n |
| 0x2f806a | 33 | bow until we fade from her sight. |

## 8. Formato de saida EXIGIDO
Escreva `translations_30_09.json` com a forma:
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
