# Cena ch_18_01 — pacote de traducao (4712 linhas)

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
| Akuruka | Objeto | Akuruka | manter_original | moderate |
| amam | Item | amam | manter_original | none |
| Anju | Personagem | Anju | manter_original | moderate |
| aperyu | Item | aperyu | manter_original | none |
| Atuy | Personagem | Atuy | manter_original | none |
| Boro-Gigiri | Criatura | Boro-Gigiri | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| Divine Scion | Titulo | Descendente Divino | traduzir | moderate |
| Eight Pillar Generals | Termo | Oito Generais-Pilar | traduzir | none |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Guardian | Titulo | Guardia | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kujyuri | Local | Kujyuri | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Kurarin | Criatura | Kurarin | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Master | Cultural | Mestre | traduzir | none |
| Mausoleum | Local | Mausoleu | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Miruhj | Personagem | Miruhj | manter_original | none |
| Mito | Personagem | Mito | manter_original | none |
| Munechika | Personagem | Munechika | manter_original | moderate |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ozen | Personagem | Ozen | manter_original | none |
| Raurau | Personagem | Raurau | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Shyahoro | Local | Shyahoro | manter_original | none |
| Soyankekur | Personagem | Soyankekur | manter_original | moderate |
| Twin Shields | Titulo | Escudos Gemeos | traduzir | major |
| Ukon | Personagem | Ukon | manter_original | major |
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
### Ozen — criticality: low
- Ozen — `voice_criticality: low`. General-Pilar, pai da Rulutieh; registro grave/nobre.
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
- `Yes...` -> `Sim...` (Rulutieh, 14_10)
- `Right...` -> `É...` (Ukon, 15_01)
- `Y-Yes...` -> `S-Sim...` (Rulutieh, 15_01)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `Hee hee...` -> `Hehe...` (Kuon, 17_01)
- `Hm?` -> `Hum?` (Kuon, 11_04)
- `mouth.` -> `boca.` (Garota, 16_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `*Sigh*...` -> `*Suspiro*...` (Homem, 17_01)
- `U-Um...` -> `E-Ei...` (Rulutieh, 14_09)
- `again...` -> `de novo...` (Homem, 13_09)
- `*WHUMP*` -> `*BAM*` (Haku, 11_07)
- `Bwuh!?` -> `Ué!?` (Haku, 16_01)
- `Sir!` -> `Sim!` (Maroro, 12_09)
- `Amazing...` -> `Incrível...` (Haku, 12_04)
- `attention.` -> `muita atenção.` (Ukon, 15_01)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `course.` -> `claro.` (Haku, 16_01)
- `Uh oh.` -> `Uh oh.` (Nekone, 16_02)
- `*FWIP*` -> `*VUP*` (SYSTEM, 14_03)
- `Hm...?` -> `Hum...?` (Kuon, 13_02)
- `*FWOOSH*` -> `*VUSH*` (SISTEMA, 13_05)
- `behind me.` -> `atrás de mim.` (Haku, 14_02)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `Nekone.` -> `Nekone.` (Ukon, 14_04)
- `him.` -> `dele.` (Nekone, 15_02)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `other.` -> `um ao outro.` (Kiwru, 16_01)
- `lady.` -> `moça.` (Haku, 15_04)
- `here?` -> `afinal?` (Haku, 13_02)
- `us.` -> `nós.` (Haku, 15_03)
- `Is that so?` -> `É mesmo?` (Nekone, 15_02)
- `I-I see...` -> `A-Ah é...` (Haku, 12_03)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `speaking.` -> `falando.` (Ougi, 17_04)
- `you know.` -> `você sabe.` (Nosuri, 16_01)
- `Mysterious duo right` -> `Dupla misteriosa dir.` (sistema, 13_02)
- `Mysterious duo left` -> `Dupla misteriosa esq.` (sistema, 13_02)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `actually.` -> `na verdade.` (Kuon, 11_10)
- `love?` -> `amor?` (Atuy, 15_04)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `Then--` -> `Então--` (Haku, 14_03)
- `hand.` -> `mão.` (Haku, 13_01)
- `me?` -> `mim?` (Maroro, 12_13)
- `good.` -> `boas.` (Ukon, 14_03)
- `Worker` -> `Func.` (Haku, 14_03)
- `as I am.` -> `quanto eu.` (Haku, 14_03)
- `Haku...` -> `Haku...` (Kuon, 14_09)
- `Well, let's see...` -> `Bem, deixa eu ver...` (Karulau, 17_01)
- `...I see.` -> `...Entendo.` (Kuon, 14_03)
- `food.` -> `comida.` (Garota, 17_01)
- `Ugh...` -> `Ugh...` (Haku, 13_02)
- `Hey, Kuon.` -> `Ei, Kuon.` (Ukon, 17_01)
- `What is it?` -> `O quê?` (Kuon, 13_02)
- `situation.` -> `ruim.` (Kuon, root)
- `anything.` -> `nada.` (Haku, 17_01)
- `This way.` -> `Por aqui.` (Mulher, 14_06)
- `Yamato.` -> `Yamato.` (Haku, 17_01)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `out.` -> `fora.` (Atuy, 17_01)
- `it.` -> `aí.` (Haku, 15_03)
- `Yes!` -> `Sim!` (Rulutieh, 14_04)
- `Yeah.` -> `É.` (Haku, 15_04)
- `Whoa...` -> `Nossa...` (Haku, 16_02)
- `now.` -> `já.` (Kuon, 14_04)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `Haku?` -> `Haku?` (Kuon, 11_07)
- `me...` -> `mim...` (Haku, 11_03)
- `What's the matter?` -> `O que foi?` (Haku, 15_02)
- `Wh--` -> `Q--` (Haku, 11_07)
- `Rulutieh?` -> `Rulutieh?` (Kuon, 14_09)
- `Oh.` -> `Ah.` (Narrator, 17_03)
- `before...` -> `assim...` (Nekone, 14_10)
- `D-Dear sister?` -> `Q-Querida irmã?` (Haku, 14_09)
- `Kuon...` -> `Kuon...` (Kuon, 13_02)
- `What?` -> `Que?` (Haku, 12_02)
- `It can't be...` -> `Não pode ser...` (Kiwru, 15_05)
- `love.` -> `amor.` (Atuy, 15_04)
- `excitement.` -> `frenéticos.` (Haku, 14_03)
- `Oshtor?` -> `Oshtor?` (Kuon, 16_02)
- `Oshtor.` -> `Oshtor.` (Haku, 14_10)
- `yeah?` -> `tá?` (Ukon, 14_02)
- `Urk...` -> `Urgh...` (Haku, 12_06)
- `sounds.` -> `incomum.` (Haku, 12_03)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `Nnngh...` -> `Nnh...` (Protagonista, 17_01)
- `Atuy?` -> `Atuy?` (Ukon, 16_02)
- `Eh?` -> `Hã?` (Haku, 13_01)
- `Great.` -> `Ótimo.` (Haku, 14_02)
- `Ungh...` -> `Urgh...` (Haku, 14_04)
- `again.` -> `vez.` (Ougi, 13_05)
- `I guess.` -> `eu acho.` (Haku, 11_10)
- `errands.` -> `recados.` (Kuon, 12_03)
- `one...` -> `uma...` (Oshtor, 17_04)
- `Man` -> `Hom` (Sistema, 12_04)
- `capital.` -> `imperial.` (Kuon, 12_04)
- `its contents.` -> `seu conteúdo.` (Haku, 16_02)
- `to this?` -> `a isso?` (Haku, 12_07)
- `now?` -> `agora?` (Haku, 17_04)
- `*Drag, drag*...` -> `*Puxão, puxão*...` (Garota, 16_02)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `all this.` -> `disso tudo.` (Haku, 17_01)
- `tell me.` -> `me diga.` (Kuon, root)
- `things.` -> `faz.` (Nekone, 15_03)
- `...Hm?` -> `...Hum?` (Haku, 11_05)
- `Old man` -> `Velhinho` (Haku, 14_10)
- `Nngh...` -> `Nnh...` (Haku, 11_08)
- `company...` -> `Ukon...` (Haku, 14_01)
- `at least.` -> `pelo menos.` (Ougi, 17_04)
- `Sure...` -> `Claro...` (Haku, 16_01)
- `Uh.` -> `Ah.` (Kuon, 11_10)
- `I said take a seat.` -> `Disse sente-se.` (Kuon, 12_03)
- `That's...` -> `Isso...` (Haku, 15_01)
- `at it.` -> `mexer nela.` (Kuon, root)
- `Dear sister...` -> `Cara irmã...` (Nekone, 15_02)
- `to me.` -> `a mim.` (Narrador, 12_11)
- `for me.` -> `espera.` (Kuon, 11_09)
- `as ever.` -> `como sempre.` (Haku, 16_01)
- `dear sister?` -> `cara irmã?` (Nekone, 15_01)
- `out...` -> `fora...` (Haku, 16_01)
- `this...` -> `isto...` (Kuon, 11_08)
- `then?` -> `então?` (Kuon, 16_02)
- `her.` -> `a ela.` (Kuon, 17_01)
- `princess.` -> `princesinha.` (Kuon, 13_01)
- `Is something the matter?` -> `Aconteceu alguma coisa?` (Kuon, 12_09)
- `Very well.` -> `Sim.` (Nekone, 15_01)
- `somewhere.` -> `de algum lugar.` (Haku, 15_01)
- `Mysterious duo` -> `Dupla misteriosa` (sistema, 13_02)
- `something?` -> `alguma coisa?` (Haku, 16_01)
- `that...` -> `essa...` (Haku, 15_03)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `name?` -> `nome?` (Kuon, root)
- `thinking.` -> `pensando.` (Ukon, 12_17)
- `Could it be...?` -> `Será que...?` (Haku, 12_04)
- `This is...` -> `Isto é...` (Haku, 16_01)
- `experience.` -> `sua vivencia.` (Ukon, 15_01)
- `eagerly.` -> `animados.` (Haku, 14_02)
- `all.` -> `nunca mais.` (Haku, 13_02)
- `...Yes.` -> `...Sim.` (Rulutieh, 13_01)
- `like that.` -> `assim.` (Ukon, 12_16)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `me.` -> `mim.` (Garota, 17_01)
- `left.` -> `sobrado.` (Narrador/Haku, 14_09)
- `Th-Thank you...` -> `O-Obrigado...` (Homem ferido, 12_04)
- `Nekone...` -> `Nekone...` (Maroro, 17_03)
- `politely.` -> `com jeito.` (Haku, 15_04)
- `Then again...` -> `Mas...` (Haku, 13_02)
- `Ahhh...` -> `Ahhh...` (Haku, 11_10)
- `this.` -> `essa.` (Moznu, 13_05)
- `eyes.` -> `olhar.` (Haku, 14_04)
- `*Groan*...` -> `*Rangeee*...` (Haku, 12_03)
- `understand.` -> `entenda.` (Nekone, 15_03)
- `Miss Kuon...` -> `Senhora Kuon...` (Rulutieh, 13_05)
- `You are...` -> `Você é...` (Nekone, 14_09)
- `Really?` -> `Mesmo?` (Kuon, 14_03)
- `Now!` -> `Agora!` (Haku, 17_04)
- `Hm.` -> `Hm.` (Ukon, 12_12)
- `quickly.` -> `rapidamente.` (Nosuri/narração, 17_02)
- `bite...` -> `morder...` (Haku, 16_01)
- `*Gasp*` -> `*Suspiro assustado*` (Garota, 17_01)
- `name.` -> `nome.` (Nekone, 15_03)
- `What!?` -> `O quê!?` (Haku, 12_03)
- `agreement.` -> `acordo.` (Haku, 17_01)
- `Yes?` -> `Sim?` (Yuuri, 16_05)
- `Oh!` -> `Ah!` (Garota, 17_01)
- `at all.` -> `nada.` (Haku, 16_01)
- `flustered.` -> `desconcertada.` (Haku, 15_01)
- `at once.` -> `vez só.` (Haku, 14_02)
- `Good!` -> `Ótimo!` (Kuon, 12_03)
- `flavor.` -> `sabor.` (Protagonista, 17_01)
- `too.` -> `também.` (Garota, 17_01)
- `herself.` -> `ela mesma.` (Haku, 15_02)
- `price.` -> `mais.` (Ukon, 14_03)
- `I see.` -> `Sim.` (Haku, 12_17)
- `so...` -> `todos, então...` (Rulutieh, 13_02)
- `trouble.` -> `de verdade.` (Haku, 12_04)
- `done.` -> `feito.` (Haku, 17_04)
- `...I should have figured.` -> `...Já devia ter imaginado.` (Haku, 12_07)
- `*THUMP--*\n` -> `*THUMP--*\n` (sistema, 13_02)
- `best.` -> `daqui.` (Kuon, 15_02)
- `*Slip*` -> `*Escorrega*` (Haku, 16_01)
- `Ack.` -> `Aff.` (Kiwru, 15_03)
- `*Thwack!*` -> `*Bam!*` (Kuon, 17_01)
- `Hnngah!?` -> `Nhhgh!?` (Maroro, 17_01)
- `Huh!?` -> `Hein!?` (Haku, 15_05)
- `you...` -> `você...` (Haku, 12_11)
- `right?` -> `né?` (Haku, 12_03)
- `Yes.` -> `Sim.` (Haku, 17_01)
- `stuff.` -> `isso.` (Haku, 14_04)
- `that?` -> `né?` (Haku, 14_09)
- `too much.` -> `demais.` (Narração, 17_01)
- `plans.` -> `planos.` (Nosuri, 16_01)
- `Thank you.` -> `Obrigado.` (Homem, 14_09)
- `*Hromf, munch--*` -> `*Hrom, nhac--*` (Kuon, 11_09)
- `What's this?` -> `O que é isso?` (Haku, 12_08)
- `Well...` -> `Bom...` (Haku, 12_03)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `like...` -> `como...` (Kuon, root)
- `...Oh.` -> `...Ah.` (Haku, 13_03)
- `room.` -> `cômodo.` (Haku, 11_06)
- `them.` -> `deles.` (Kuon, 11_05)
- `Lady Rulutieh?` -> `Lady Rulutieh?` (Nekone, 15_03)
- `as well.` -> `também.` (Haku, 17_01)
- `Kuon.` -> `Kuon.` (Kuon, root)
- `sky.` -> `céu.` (Maroro, 16_01)
- `back...` -> `de lá...` (Haku, 14_04)
- `So?` -> `E?` (Kuon, 14_03)
- `Haku.` -> `Haku.` (Kuon, 12_08)
- `see.` -> `né.` (Ukon, 12_10)
- `for her.` -> `pra ela.` (Haku, 15_03)
- `Right.` -> `direito.` (Kuon, 15_01)
- `then...` -> `então...` (Haku, 14_04)
- `...Rulutieh?` -> `...Rulutieh?` (Kuon, 14_03)
- `Ah?` -> `Ah?` (Nosuri, 13_05)
- `for...` -> `para...` (Haku, 17_01)
- `picture.` -> `a mensagem.` (Haku, 15_03)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `Oh...?` -> `Oh...?` (Homem, 14_09)
- `you.` -> `isso.` (Nekone, 15_03)
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
| 0x11df62 | 23 | So, ready to try again? |
| 0x11df7a | 6 | Yes... |
| 0x11df81 | 46 | All right, let's figure out what we learned.\n |
| 0x11dfb0 | 48 | The bitterness of the sap intensifies after it\n |
| 0x11dfe1 | 10 | hardens... |
| 0x11dfec | 49 | So we haven't been giving it the time to harden\n |
| 0x11e01e | 43 | by using sap taken directly from the tree\n |
| 0x11e04a | 7 | itself. |
| 0x11e052 | 45 | The bitterness still persists even then, so\n |
| 0x11e080 | 44 | NOW we'll try absorbing it with amam powder. |
| 0x11e0ad | 20 | That sounds right... |
| 0x11e0c2 | 48 | Rulutieh gives a small nod, then begins to mix\n |
| 0x11e0f3 | 45 | amam powder from a small jar into a bowl of\n |
| 0x11e121 | 4 | sap. |
| 0x11e126 | 47 | Let me know if you want me to jump in. We can\n |
| 0x11e156 | 17 | take turns at it. |
| 0x11e168 | 38 | Thank you, but... I should... be fine. |
| 0x11e18f | 42 | I'd better let her focus. I'm a complete\n |
| 0x11e1ba | 27 | amateur at this, after all. |
| 0x11e1d6 | 42 | Now, we should leave it to set, and then\n |
| 0x11e201 | 44 | separate it after all the amam has sunk to\n |
| 0x11e22e | 11 | the bottom. |
| 0x11e23a | 8 | Right... |
| 0x11e243 | 38 | That way, all the bitterness will be\n |
| 0x11e26a | 45 | concentrated in the powder, leaving us with\n |
| 0x11e298 | 13 | what we want. |
| 0x11e2a6 | 47 | We originally tried to mix in ash to do this,\n |
| 0x11e2d6 | 45 | but who'd have guessed amam powder would do\n |
| 0x11e304 | 13 | the same job? |
| 0x11e312 | 43 | Just as expected, the powder sinks to the\n |
| 0x11e33e | 40 | bottom, leaving a clear liquid on top... |
| 0x11e367 | 30 | ...Oh, it's faintly sweet now! |
| 0x11e386 | 47 | Rulutieh smiles as she tastes the final result. |
| 0x11e3b6 | 49 | That powerful flavor it had is all but... gone.\n |
| 0x11e3e8 | 37 | It's strange, tasting it like this... |
| 0x11e40e | 47 | We can usually get this far with no problems.\n |
| 0x11e43e | 10 | But now... |
| 0x11e449 | 46 | Next, we need to boil it since it's so thin,\n |
| 0x11e478 | 28 | but this is the tricky part. |
| 0x11e495 | 34 | Rulutieh, would you do the honors? |
| 0x11e4b8 | 8 | Y-Yes... |
| 0x11e4c1 | 49 | Rulutieh separates and scoops up our prize into\n |
| 0x11e4f3 | 38 | a pot, moving it over to the cookfire. |
| 0x11e51a | 20 | There... It's ready. |
| 0x11e52f | 49 | All right, I'm ready too. Let's try not to burn\n |
| 0x11e561 | 13 | it this time. |
| 0x11e56f | 39 | And don't worry about messing up, OK?\n |
| 0x11e597 | 40 | Failure is always an option. Just relax. |
| 0x11e5c0 | 15 | U-Understood... |
| 0x11e5d0 | 46 | Rulutieh stirs the supernatant liquid in the\n |
| 0x11e5ff | 45 | pot with an anxious expression on her face... |
| 0x11e62d | 46 | And finally, the clear liquid begins to turn\n |
| 0x11e65c | 6 | amber! |
| 0x11e663 | 48 | Now, hold up--maybe we should take the pot off\n |
| 0x11e694 | 22 | of the stove for a m-- |
| 0x11e6ab | 5 | Oh... |
| 0x11e6b1 | 43 | Almost instantly, the thick amber mixture\n |
| 0x11e6dd | 45 | blackens and begins to give off a smoky odor. |
| 0x11e70b | 17 | It's all burnt... |
| 0x11e71d | 49 | We failed again. I doubt any of this is edible,\n |
| 0x11e74f | 9 | either... |
| 0x11e759 | 31 | I'm sorry... I-I... I failed... |
| 0x11e779 | 47 | Don't apologize! I could tell you were paying\n |
| 0x11e7a9 | 35 | the utmost attention. You did well. |
| 0x11e7cd | 48 | Who'd have thought this stuff burns so easily,\n |
| 0x11e7fe | 43 | though? Boiling it is turning out to be a\n |
| 0x11e82a | 7 | pain... |
| 0x11e832 | 43 | We, could, um... try heating it through a\n |
| 0x11e85e | 21 | water bath, maybe...? |
| 0x11e874 | 47 | No, that'll take way too much time to hit its\n |
| 0x11e8a4 | 47 | boiling point. It wouldn't be efficient at all. |
| 0x11e8d4 | 33 | Yes... y-you're right, of course. |
| 0x11e8f6 | 46 | We've come this far, though. It feels like a\n |
| 0x11e925 | 24 | waste to give up here... |
| 0x11e93e | 44 | If only I were... better. A-At this, I mean. |
| 0x11e96b | 49 | This is the first time you've done this, right?\n |
| 0x11e99d | 46 | Nobody's expecting you to have it down right\n |
| 0x11e9cc | 5 | away. |
| 0x11e9d2 | 40 | Every failure's a learning experience,\n |
| 0x11e9fb | 37 | Rulutieh. We'll get there eventually! |
| 0x11ea21 | 31 | I... suppose you're right, yes. |
| 0x11ea41 | 48 | Well, being all depressed about it isn't going\n |
| 0x11ea72 | 46 | to do us any good. Let's move on for now, huh? |
| 0x11eaa1 | 15 | Yes, of course! |
| 0x11eab1 | 46 | Rulutieh takes the remaining murky fluid and\n |
| 0x11eae0 | 40 | pours it into another pot on the fire... |
| 0x11eb09 | 44 | After a while, the liquid in the pot turns\n |
| 0x11eb36 | 31 | viscous without burning at all. |
| 0x11eb56 | 47 | And for some reason, this one doesn't burn at\n |
| 0x11eb86 | 40 | all... I don't get it. What's different? |
| 0x11ebaf | 47 | We've figured out a recipe, at least. Cooling\n |
| 0x11ebdf | 44 | it in a mold makes for a sweet, gelatinous\n |
| 0x11ec0c | 6 | snack. |
| 0x11ec13 | 47 | Not quite the result we wanted, but tasty all\n |
| 0x11ec43 | 9 | the same. |
| 0x11ec4d | 34 | Looks like it's just about done.\n |
| 0x11ec70 | 18 | What do you think? |
| 0x11ec83 | 24 | Y-Yes, I think so too... |
| 0x11ec9c | 46 | Rulutieh takes the mold out of the water and\n |
| 0x11eccb | 37 | flips it over onto a cutting board... |
| 0x11ecf1 | 45 | Then, she takes a knife and deftly cuts the\n |
| 0x11ed1f | 39 | jiggling mass into neat, orderly cubes. |
| 0x11ed47 | 22 | And that should do it! |
| 0x11ed5e | 24 | Now, to sample our work. |
| 0x11ed77 | 28 | Hromf... *Smack... smack*... |
| 0x11ed94 | 15 | Ahh, delicious! |
| 0x11eda4 | 40 | Yes, it is! Such a... bizarre texture.\n |
| 0x11edcd | 33 | It's strange, but... very good... |
| 0x11edef | 46 | Hard to believe something this good came out\n |
| 0x11ee1e | 31 | of our random experiments, huh? |
| 0x11ee3e | 43 | Making this stuff has definitely been our\n |
| 0x11ee6a | 13 | focus lately. |
| 0x11ee78 | 10 | Hee hee... |
| 0x11ee83 | 3 | Hm? |
| 0x11ee87 | 44 | You're amazing, Sir Haku. You came up with\n |
| 0x11eeb4 | 47 | something so fantastic, completely by accident! |
| 0x11eee4 | 49 | It was more coincidence than anything. Besides,\n |
| 0x11ef16 | 36 | I had you here to help me, didn't I? |
| 0x11ef3b | 45 | If it wasn't for you, this whole plan would\n |
| 0x11ef69 | 28 | have been dead in the water. |
| 0x11ef8a | 47 | Oh, that smells so nice! You made that jiggly\n |
| 0x11efba | 23 | stuff again didn't you? |
| 0x11efd2 | 44 | It gives off a very pleasing scent, I must\n |
| 0x11efff | 6 | admit. |
| 0x11f006 | 45 | Uh-oh, looks like we've attracted the pack.\n |
| 0x11f034 | 44 | Hide the goods before the hounds steal our\n |
| 0x11f061 | 16 | share, Rulutieh! |
| 0x11f072 | 17 | Um... I ... uh... |
| 0x11f084 | 47 | Too bad, but this wolf's already got her prize! |
| 0x11f0b4 | 15 | Mmm! Delicious. |
| 0x11f0c4 | 51 | This sweetness and strange, alluring mouthfeel...\n |
| 0x11f0f8 | 44 | I doubt I'll ever grow tired of this, truly. |
| 0x11f125 | 48 | As Nekone ruminates, Kuon spears another piece\n |
| 0x11f156 | 45 | on a toothpick and places it in her waiting\n |
| 0x11f184 | 6 | mouth. |
| 0x11f18b | 20 | Here you go, Nekone. |
| 0x11f1a0 | 19 | Ah, d-dear sister-- |
| 0x11f1b4 | 7 | Mmff... |
| 0x11f1bc | 49 | Nekone looks embarrassed at being hand-fed, but\n |
| 0x11f1ee | 47 | her expression turns to a smile in short order. |
| 0x11f21e | 46 | Those two sure do get along. It puts a smile\n |
| 0x11f24d | 45 | on my face to see them enjoying themselves... |
| 0x11f27b | 36 | Hromf... *munch*... Ah, delicious!\n |
| 0x11f2a0 | 42 | Haku, love, do you mind if I have a bite\n |
| 0x11f2cb | 8 | of this? |
| 0x11f2d4 | 46 | ...Typically you ask that BEFORE you eat it,\n |
| 0x11f303 | 5 | Atuy. |
| 0x11f309 | 47 | Hey, what's this one? Looks like you two have\n |
| 0x11f339 | 35 | been working on something else, eh? |
| 0x11f35d | 47 | Atuy bends over the pot containing our failed\n |
| 0x11f38d | 45 | attempt, scooping some of it up on a spatula. |
| 0x11f3bb | 14 | Wait, that's-- |
| 0x11f3ca | 39 | I think I'll just have a taste of this. |
| 0x11f3f2 | 46 | Before I can tell her it was an unsuccessful\n |
| 0x11f421 | 24 | batch, she slurps it up. |
| 0x11f43a | 44 | Haku, love, what's this black syrup you've\n |
| 0x11f467 | 24 | got here? It's so sweet! |
| 0x11f480 | 7 | ...Huh? |
| 0x11f488 | 33 | Oh, now THERE'S an idea. Hold on. |
| 0x11f4aa | 47 | Atuy drizzles the black syrup over a piece of\n |
| 0x11f4da | 37 | gelatin and pops it into her mouth... |
| 0x11f500 | 46 | Oh, love, how DARE you? Keeping this syrup a\n |
| 0x11f52f | 31 | secret from us! It's wonderful! |
| 0x11f54f | 20 | Really? Let's see... |
| 0x11f564 | 21 | ...Hey, this IS good! |
| 0x11f57a | 46 | This texture and sweet scent... Subtle notes\n |
| 0x11f5a9 | 45 | of blended flavor... Truly, appearances can\n |
| 0x11f5d7 | 8 | deceive. |
| 0x11f5e0 | 48 | They're eating the burnt batch like there's no\n |
| 0x11f611 | 36 | tomorrow. Is it really that good...? |
| 0x11f636 | 19 | *Munch... munch*... |
| 0x11f64a | 47 | Huh? I... uh... thought... T-Taste testing is\n |
| 0x11f67a | 46 | an important step of... the process, isn't it? |
| 0x11f6a9 | 26 | Here now, love. Open wide. |
| 0x11f6c4 | 47 | She stabs one of the snacks with a toothpick,\n |
| 0x11f6f4 | 45 | then dips it in syrup, holding it out to me\n |
| 0x11f722 | 12 | expectantly. |
| 0x11f72f | 46 | Why does everybody try to feed me like this?\n |
| 0x11f75e | 9 | *Sigh*... |
| 0x11f768 | 48 | Reluctantly, I eat the substance right off the\n |
| 0x11f799 | 21 | end of the toothpick. |
| 0x11f7af | 15 | Hey, this is... |
| 0x11f7bf | 50 | The snack is only faintly sweet without anything\n |
| 0x11f7f2 | 43 | on it, but with the syrup, it's VERY sweet! |
| 0x11f81e | 48 | The black syrup's flavor is a little strong on\n |
| 0x11f84f | 46 | its own, but as a sauce, it balances out well. |
| 0x11f87e | 35 | Never would've noticed on my own.\n |
| 0x11f8a2 | 46 | I was so wrapped up in trying to perfect it,\n |
| 0x11f8d1 | 18 | I never thought... |
| 0x11f8e4 | 49 | I was sure this was a failure, but it turns out\n |
| 0x11f916 | 29 | there's a perfect use for it! |
| 0x11f934 | 31 | I-I see what you mean, now...\n |
| 0x11f954 | 30 | "Failure is always an option." |
| 0x11f973 | 37 | W-Well, when I said that, I meant--\n |
| 0x11f999 | 41 | It's... a little different in this case-- |
| 0x11f9c3 | 44 | So, Haku, what're you gonna call this stuff? |
| 0x11f9f0 | 43 | What it's called? Uh. Tree... sap... snack? |
| 0x11fa1c | 32 | No, I mean a proper name for it. |
| 0x11fa3d | 44 | I've never seen anything like it, and it's\n |
| 0x11fa6a | 37 | REALLY good. It ought to have a name! |
| 0x11fa90 | 46 | Come on, do we have to NAME it? It just came\n |
| 0x11fabf | 43 | about by coincidence; it's not THAT big a\n |
| 0x11faeb | 7 | deal... |
| 0x11faf3 | 46 | Points for trying, but I think you're wrong,\n |
| 0x11fb22 | 43 | love. I've never tasted anything like this! |
| 0x11fb4e | 48 | Kuon's right. This deserves a right proper name. |
| 0x11fb7f | 45 | I agree. It would be inconvenient not to be\n |
| 0x11fbad | 43 | able to refer to this concoction by a name. |
| 0x11fbd9 | 30 | I guess that's a fair point... |
| 0x11fbf8 | 7 | U-Um... |
| 0x11fc00 | 45 | I th-think these snacks would be very happy\n |
| 0x11fc2e | 28 | if you named them, Sir Haku. |
| 0x11fc4b | 43 | I, um--s-sorry, that... sounds silly when\n |
| 0x11fc77 | 20 | I say it out loud... |
| 0x11fc8c | 47 | No, you're right. It would be more convenient\n |
| 0x11fcbc | 30 | to have a name for this thing. |
| 0x11fcdb | 48 | It's going to get confusing if we keep calling\n |
| 0x11fd0c | 44 | it "the sweet stuff Haku and Rulutieh make\n |
| 0x11fd39 | 11 | sometimes." |
| 0x11fd45 | 48 | A name, huh? I've never been good at that kind\n |
| 0x11fd76 | 28 | of stuff. Let's see... uh... |
| 0x11fd93 | 45 | Well, it's your recipe, isn't it? Why don't\n |
| 0x11fdc1 | 32 | you just name it after yourself? |
| 0x11fde2 | 42 | What, "Haku?" Shall we call it that, then? |
| 0x11fe0d | 45 | What kind of crazy logic is THAT? You can't\n |
| 0x11fe3b | 28 | just name it after a person! |
| 0x11fe58 | 45 | I dunno. It's pretty common for foods to be\n |
| 0x11fe86 | 19 | named after people. |
| 0x11fe9a | 23 | Whoa, hang on, hang on. |
| 0x11feb2 | 47 | I'm not sure I'm comfortable with the idea of\n |
| 0x11fee2 | 39 | it being JUST my name and nothing else. |
| 0x11ff0a | 48 | I make eye contact with the girl standing next\n |
| 0x11ff3b | 27 | to me, and I get an idea... |
| 0x11ff57 | 42 | The person who actually MADE all this is\n |
| 0x11ff82 | 47 | Rulutieh, so why don't we base it on her name\n |
| 0x11ffb2 | 8 | instead? |
| 0x11ffbb | 36 | Something like... Rulu, for example. |
| 0x11ffe0 | 8 | ...Huh?! |
| 0x11ffe9 | 46 | After that, I got too lazy to make the stuff\n |
| 0x120018 | 42 | on my own, so I shared the recipe with a\n |
| 0x120043 | 16 | nearby teahouse. |
| 0x120054 | 45 | They began to offer it, and soon enough, it\n |
| 0x120082 | 40 | became known as the capital's hallmark\n |
| 0x1200ab | 11 | confection! |
| 0x1200b7 | 46 | Every time we pass a shop with a "Rulu" sign\n |
| 0x1200e6 | 40 | out front, Rulutieh can't help but get\n |
| 0x12010f | 14 | embarrassed... |
| 0x12011e | 48 | But I don't think it's my imagination that she\n |
| 0x12014f | 48 | likes seeing others enjoy what we made together. |
| 0x120180 | 45 | ...and Kuon seems to be in a strangely good\n |
| 0x1201ae | 32 | mood since all of this happened. |
| 0x1201cf | 47 | I just hope she's not planning anything weird\n |
| 0x1201ff | 8 | again... |
| 0x121f2c | 45 | I keep pace with Nekone as she turns down a\n |
| 0x121f5a | 30 | busy street, leading me along. |
| 0x121f79 | 45 | Oshtor asked me to accompany her today, but\n |
| 0x121fa7 | 22 | something feels off... |
| 0x121fc2 | 43 | Nekone's been awfully quiet, for one thing. |
| 0x121fee | 47 | It's not as though she's a lively person, but\n |
| 0x12201e | 31 | she's never as quiet as THIS... |
| 0x12203e | 47 | Is she just in a bad mood, or is it something\n |
| 0x12206e | 5 | else? |
| 0x122074 | 40 | Is it because we're going to the other\n |
| 0x12209d | 45 | Imperial Guard's manor? Oshtor's counterpart? |
| 0x1220cb | 47 | Oshtor gave us a letter to deliver to the guy\n |
| 0x1220fb | 47 | on his behalf... I think his name is Mikazuchi? |
| 0x12212b | 47 | I only caught a glimpse of him before, but he\n |
| 0x12215b | 38 | seems like the violent type. Maybe...? |
| 0x122182 | 37 | Don't tell me you're nervous, Nekone? |
| 0x1221a8 | 24 | ...No. I am not nervous. |
| 0x1221c1 | 29 | Yeah? If you say so, I guess. |
| 0x1221df | 50 | All we really have to do is drop off the letter.\n |
| 0x122212 | 43 | Not sure why that has her in such a mood... |
| 0x12223e | 13 | Or maybe...\n |
| 0x12224c | 27 | Nah, couldn't be. Could it? |
| 0x122268 | 6 | Speak. |
| 0x12226f | 45 | Is it that time of the month? I mean, n-not\n |
| 0x12229d | 46 | that it's--you're probably way too young for-- |
| 0x1222cc | 7 | *WHUMP* |
| 0x1222d4 | 6 | BWUH!? |
| 0x1222db | 45 | Before I can even finish my thought, Nekone\n |
| 0x122309 | 35 | savagely kicks me across the shins. |
| 0x12232d | 36 | Hnngh, ow--Wh-Why would you do that? |
| 0x122352 | 46 | I admit I do not know what you were accusing\n |
| 0x122381 | 38 | me of, but a judicious response felt\n |
| 0x1223a8 | 12 | appropriate. |
| 0x1223b5 | 43 | Ow, shit. Are all kids so mean at this age? |
| 0x1223e1 | 44 | The rest of the journey toward Mikazuchi's\n |
| 0x12240e | 18 | manor is silent... |
| 0x122421 | 45 | We inform the guards we're here on business\n |
| 0x12244f | 40 | from Oshtor, and they direct us to the\n |
| 0x122478 | 17 | training grounds. |
| 0x12248a | 45 | The manor feels similar to Oshtor's, but it\n |
| 0x1224b8 | 37 | feels... more austere. More military? |
| 0x1224de | 44 | Lord Mikazuchi prizes the arts of war over\n |
| 0x12250b | 29 | all else, as I understand it. |
| 0x122529 | 16 | The arts of war? |
| 0x12253a | 38 | A sharp cry from nearby interrupts us. |
| 0x122561 | 16 | Form one, begin! |
| 0x122572 | 6 | Guards |
| 0x122579 | 4 | Sir! |
| 0x12257e | 42 | On the grounds ahead, assembled soldiers\n |
| 0x1225a9 | 44 | practice battlefield techniques in perfect\n |
| 0x1225d6 | 7 | unison. |
| 0x1225de | 9 | Form two! |
| 0x1225e8 | 18 | Wow, impressive... |
| 0x1225fb | 45 | Sure, Oshtor's subordinates are organized--\n |
| 0x122629 | 44 | but I've never seen discipline this rigid.\n |
| 0x122656 | 10 | Amazing... |
| 0x122661 | 49 | As I look on, dumbstruck, the man giving orders\n |
| 0x122693 | 47 | notices us and raises his hand to the soldiers. |
| 0x1226c3 | 11 | Atten-SHUN! |
| 0x1226cf | 6 | *Snap* |
| 0x1226d6 | 48 | Despite their arduous exercise, not one of the\n |
| 0x122707 | 44 | soldiers looks even winded as they snap to\n |
| 0x122734 | 10 | attention. |
| 0x12273f | 48 | The man shouting commands leaves them standing\n |
| 0x122770 | 42 | like that as he crosses the grounds to us. |
| 0x12279b | 5 | Hm... |
| 0x1227a1 | 46 | As he grows closer, I recognize his face, of\n |
| 0x1227d0 | 7 | course. |
| 0x1227d8 | 42 | The Imperial Guard of the Left, Mikazuchi. |
| 0x122803 | 42 | He grins menacingly when he spots Nekone\n |
| 0x12282e | 10 | beside me. |
| 0x122839 | 47 | Ah, Nekone. I recall seeing you recently, but\n |
| 0x122869 | 47 | it's been a while since we've had a chance to\n |
| 0x122899 | 5 | talk. |
| 0x12289f | 6 | Uh oh. |
| 0x1228a6 | 47 | His smile is almost sinister, like a predator\n |
| 0x1228d6 | 40 | that's just identified the perfect prey. |
| 0x1228ff | 47 | Now that I meet him in person, he has an even\n |
| 0x12292f | 43 | scarier presence to him than a Boro-Gigiri. |
| 0x12295b | 43 | So this is the other half of the Mikado's\n |
| 0x122987 | 15 | Twin Shields... |
| 0x122997 | 20 | You look well, girl. |
| 0x1229ac | 42 | But you're still so small. Eat more, eh?\n |
| 0x1229d7 | 32 | It will make you bigger in time. |
| 0x1229f8 | 48 | The words are those of a caring elder, but his\n |
| 0x122a29 | 49 | tone makes it sound like he's telling livestock\n |
| 0x122a5b | 15 | to fatten up... |
| 0x122a6b | 40 | ...Nekone, why are you hiding behind me? |
| 0x122a94 | 9 | Nnnngh... |
| 0x122a9e | 45 | I didn't even notice Nekone moving to cower\n |
| 0x122acc | 15 | behind my legs. |
| 0x122adc | 48 | Then, as I scoot over to let her and Mikazuchi\n |
| 0x122b0d | 20 | speak face-to-face-- |
| 0x122b22 | 6 | *Fwip* |
| 0x122b29 | 6 | Hm...? |
| 0x122b30 | 8 | *Fwoosh* |
| 0x122b39 | 45 | Every time I reposition myself, Nekone zips\n |
| 0x122b67 | 33 | behind me in the blink of an eye. |
| 0x122b89 | 27 | What the hell is she do--\n |
| 0x122ba5 | 15 | Oohh. I get it. |
| 0x122bb5 | 43 | Now, I suddenly understand the reason for\n |
| 0x122be1 | 36 | Nekone's discomfort on the way here. |
| 0x122c06 | 48 | She's even more scared of Mikazuchi than I am!\n |
| 0x122c37 | 27 | Not like I can blame her... |
| 0x122c53 | 49 | P-Please--accept this missive from Lord Oshtor,\n |
| 0x122c85 | 6 | s-sir. |
| 0x122c8c | 43 | Struggling to keep the tremble out of her\n |
| 0x122cb8 | 43 | voice, Nekone holds out the envelope from\n |
| 0x122ce4 | 10 | behind me. |
| 0x122cef | 48 | Hey, now, Nekone. Don't you think you're being\n |
| 0x122d20 | 14 | a little rude? |
| 0x122d2f | 39 | Her attitude doesn't change, of course. |
| 0x122d57 | 3 | Hn. |
| 0x122d5b | 46 | Mikazuchi's eyes narrow, possibly in offense\n |
| 0x122d8a | 21 | at Nekone's rudeness. |
| 0x122da0 | 4 | Eep! |
| 0x122da5 | 31 | God, this guy is scary as hell. |
| 0x122dc5 | 48 | I can feel Nekone shivering in fear behind me.\n |
| 0x122df6 | 44 | If looks could kill, Mikazuchi would be an\n |
| 0x122e23 | 9 | assassin. |
| 0x122e2d | 27 | I... I'm not afraid of you! |
| 0x122e49 | 34 | I-I-I am not afraid of you at all! |
| 0x122e6c | 13 | *Swish* *jab* |
| 0x122e7a | 46 | As Nekone proclaims her defiance, she throws\n |
| 0x122ea9 | 47 | anemic little punches as if to prove her words. |
| 0x122ed9 | 45 | Of course, she's doing all this while still\n |
| 0x122f07 | 19 | hiding behind me... |
| 0x122f1b | 40 | W--Would you stop using me as a shield!? |
| 0x122f44 | 19 | *Mumble, mumble*... |
| 0x122f58 | 48 | At Nekone's declaration, the previously silent\n |
| 0x122f89 | 38 | soldiers begin to grow visibly uneasy. |
| 0x122fb0 | 5 | Guard |
| 0x122fb6 | 43 | Is that girl mad? Challenging the general\n |
| 0x122fe2 | 10 | himself... |
| 0x122fed | 26 | He'll utterly destroy her! |
| 0x123008 | 48 | Th-This guy's so bloodthirsty he inspires THAT\n |
| 0x123039 | 44 | much fear in his own soldiers? What in the\n |
| 0x123066 | 6 | world? |
| 0x12306d | 16 | *Swish* *swoosh* |
| 0x12307e | 46 | Nekone doesn't stop swinging, still throwing\n |
| 0x1230ad | 30 | little punches around my legs. |
| 0x1230cc | 7 | Oho...? |
| 0x1230d4 | 45 | Mikazuchi grins wolfishly, eyes gleaming as\n |
| 0x123102 | 46 | though he's deciding how best to devour poor\n |
| 0x123131 | 7 | Nekone. |
| 0x123139 | 34 | A-A-Are you looking for a fight?\n |
| 0x12315c | 42 | Well, you'll have to get past him f-first. |
| 0x123187 | 48 | Wait, WHAT? D-Don't pull me into this any more\n |
| 0x1231b8 | 22 | than you already have! |
| 0x1231cf | 33 | Stop using me as a shield and--\n |
| 0x1231f1 | 25 | Damn it, she won't budge. |
| 0x12320b | 46 | Somehow, I manage to turn myself to push her\n |
| 0x12323a | 45 | forward, but she won't move--in fact, SHE'S\n |
| 0x123268 | 11 | pushing ME. |
| 0x123274 | 20 | Hey--hey, stop that! |
| 0x123289 | 47 | Th-That man... he intends on championing that\n |
| 0x1232b9 | 43 | young lady's challenge to Lord Mikazuchi... |
| 0x1232e5 | 45 | The idiot. Is he throwing his life away for\n |
| 0x123313 | 8 | nothing? |
| 0x12331c | 43 | I commend the noble fool for his courage.\n |
| 0x123348 | 45 | I'll see to it he receives a proper burial... |
| 0x123376 | 43 | Are you all idiots!? How the hell is this\n |
| 0x1233a2 | 45 | CHALLENGING him? I'm going to get killed at\n |
| 0x1233d0 | 10 | this rate! |
| 0x1233db | 16 | *Shove, shove--* |
| 0x1233ec | 28 | Would you PLEASE stop push-- |
| 0x123409 | 46 | Nekone gives a rough shove, and suddenly, my\n |
| 0x123438 | 37 | face is bare inches from Mikazuchi's. |
| 0x12345e | 25 | Mnnhh. Heh. Aheh heh heh. |
| 0x123478 | 49 | Mikazuchi's lips curl back into a smile, and he\n |
| 0x1234aa | 45 | jerks his head to indicate we should follow\n |
| 0x1234d8 | 4 | him. |
| 0x1234dd | 8 | Wh-What? |
| 0x1234e6 | 27 | ...We're following him. Go. |
| 0x123502 | 45 | Huh? H-Hey! I got it, OK? You don't have to\n |
| 0x123530 | 37 | keep PUSHING--Damn it, Nekone, stop-- |
| 0x123556 | 44 | ...Somehow, we find ourselves invited into\n |
| 0x123583 | 25 | Mikazuchi's manor proper. |
| 0x12359d | 42 | ...The air in here is thick and awkward... |
| 0x1235c8 | 46 | Neither Mikazuchi nor Nekone has said a word\n |
| 0x1235f7 | 47 | since we came inside. They only glare at each\n |
| 0x123627 | 6 | other. |
| 0x12362e | 46 | Nekone, however, is beginning to crack under\n |
| 0x12365d | 43 | the pressure--and she breaks eye contact,\n |
| 0x123689 | 14 | glancing down. |
| 0x123698 | 17 | *Shove, shove*... |
| 0x1236aa | 46 | Could she stop trying to shield herself with\n |
| 0x1236d9 | 44 | me? We're sitting in CHAIRS, for God's sake. |
| 0x123706 | 12 | Miruhj, tea. |
| 0x123713 | 22 | By your will, my lord. |
| 0x12372a | 48 | A smooth, erudite-sounding voice precedes what\n |
| 0x12375b | 45 | must be Mikazuchi's squire entering the room. |
| 0x123789 | 18 | Your tea, my lord. |
| 0x12379c | 45 | The boy Mikazuchi called Miruhj efficiently\n |
| 0x1237ca | 20 | arranges the cups... |
| 0x1237df | 49 | Please enjoy. If you'll excuse me, my lords and\n |
| 0x123811 | 5 | lady. |
| 0x123817 | 46 | It's all right, you can stay. In fact, could\n |
| 0x123846 | 47 | you, uh, do something about the atmosphere in\n |
| 0x123876 | 5 | here? |
| 0x12387c | 8 | Nnnhh... |
| 0x123885 | 47 | Nekone prods me with the envelope Oshtor gave\n |
| 0x1238b5 | 3 | us. |
| 0x1238b9 | 37 | Huh? You want me to give this to him? |
| 0x1238df | 45 | Nekone nods vigorously. The poor girl is so\n |
| 0x12390d | 41 | scared, tears are welling up in her eyes. |
| 0x123937 | 19 | Fine, fine... Here. |
| 0x12394b | 48 | I grab the envelope from Nekone and proffer it\n |
| 0x12397c | 13 | to Mikazuchi. |
| 0x12398a | 45 | Lord Mikazuchi, Oshtor himself entrusted us\n |
| 0x1239b8 | 46 | with this missive, if you'd be so kind as to\n |
| 0x1239e7 | 11 | receive it. |
| 0x1239f3 | 11 | Is that so? |
| 0x1239ff | 48 | Mikazuchi takes the message and sets it aside.\n |
| 0x123a30 | 36 | He doesn't seem too concerned with\n |
| 0x123a55 | 14 | formalities... |
| 0x123a64 | 31 | ...You're not going to read it? |
| 0x123a84 | 42 | Is that... an ORDER you're giving me, boy? |
| 0x123aaf | 48 | Mikazuchi's eyes snap wide as he glares at me.\n |
| 0x123ae0 | 6 | Yikes. |
| 0x123ae7 | 49 | I don't get this guy's thinking at all. How the\n |
| 0x123b19 | 40 | hell would he arrive at that conclusion? |
| 0x123b42 | 43 | My dear brother requires an answer of you\n |
| 0x123b6e | 33 | before we can return to him, sir. |
| 0x123b90 | 44 | R-Read the letter and furnish us with your\n |
| 0x123bbd | 9 | response! |
| 0x123bc7 | 42 | What, NOW you grow a spine? Get out from\n |
| 0x123bf2 | 47 | behind me and say that stuff to him directly,\n |
| 0x123c22 | 8 | damn it! |
| 0x123c2b | 46 | Mikazuchi seems to have heard her perfectly,\n |
| 0x123c5a | 43 | for he unfolds the envelope and begins to\n |
| 0x123c86 | 7 | read... |
| 0x123c8e | 41 | After looking through Oshtor's message,\n |
| 0x123cb8 | 46 | Mikazuchi looks at us with that same wolfish\n |
| 0x123ce7 | 5 | grin. |
| 0x123ced | 24 | *Shove, shove, shove*... |
| 0x123d06 | 46 | For God's sake, Nekone, will you cut that ou-- |
| 0x123d35 | 50 | So. You're Oshtor's man... This letter describes\n |
| 0x123d68 | 27 | you as quite the character. |
| 0x123d84 | 10 | I-I see... |
| 0x123d8f | 45 | Wait, why is Oshtor outing me as his agent?\n |
| 0x123dbd | 44 | I thought he wanted to keep that a secret... |
| 0x123dea | 39 | Very interesting. Interesting indeed... |
| 0x123e12 | 4 | Huh? |
| 0x123e17 | 40 | Oshtor's respect is not won so easily.\n |
| 0x123e40 | 32 | You've piqued my curiosity, boy. |
| 0x123e61 | 42 | I look forward to whatever entertainment\n |
| 0x123e8c | 16 | you'll bring me. |
| 0x123e9d | 23 | Wait, entertainment...? |
| 0x123eb5 | 41 | You WILL entertain me, will you not, boy? |
| 0x123edf | 47 | Wait, wait, wait, wait. I don't have anything\n |
| 0x123f0f | 44 | up my sleeve. What exactly is he expecting\n |
| 0x123f3c | 8 | from me? |
| 0x123f45 | 39 | Well, then. It appears as though Lord\n |
| 0x123f6d | 44 | Mikazuchi's business is with you alone, so\n |
| 0x123f9a | 19 | I'll take my leave. |
| 0x123fae | 41 | You wait just a goddamn second, Nekone!\n |
| 0x123fd8 | 27 | You're not going anywhere-- |
| 0x123ff4 | 43 | Unhand me! H-How dare you touch me there,\n |
| 0x124020 | 5 | cur!? |
| 0x124026 | 44 | Yeah, that protest only holds water if you\n |
| 0x124053 | 33 | actually have curves. Sorry, kid. |
| 0x124075 | 7 | Grrr... |
| 0x12407d | 9 | Hnnngh... |
| 0x124087 | 48 | Nekone and I lock like grappling bulls, trying\n |
| 0x1240b8 | 38 | to push each other toward Mikazuchi... |
| 0x1240df | 49 | ...Heh. To think little Nekone has opened up to\n |
| 0x124111 | 37 | another besides her "dear brother."\n |
| 0x124137 | 17 | Monumental, that. |
| 0x124149 | 33 | Open u--I-I beg your pardon, sir! |
| 0x12416b | 47 | Blushing, Nekone? Ah, I've gone and entranced\n |
| 0x12419b | 44 | another one... It's hard being so handsome\n |
| 0x1241c8 | 10 | sometimes. |
| 0x1241d3 | 45 | Unfortunately, I can't recommend falling in\n |
| 0x124201 | 48 | love with me. You'll get burned if you get too\n |
| 0x124232 | 6 | close. |
| 0x124239 | 43 | But maybe you should wait until there's a\n |
| 0x124265 | 44 | visible difference between your front side\n |
| 0x124292 | 10 | and back-- |
| 0x12429d | 5 | HYAH! |
| 0x1242a3 | 10 | Hnngaaah!! |
| 0x1242ae | 46 | Nekone deals the fateful blow and storms out\n |
| 0x1242dd | 34 | of the room, her face utterly red. |
| 0x124300 | 47 | W-Wait... you... Oh, God, my precious parts--\n |
| 0x124330 | 32 | Th-That was all your strength... |
| 0x124351 | 44 | I try to chase after Nekone, but all I can\n |
| 0x12437e | 37 | manage right now is a loping stumble. |
| 0x1243a4 | 29 | Your name is Haku, is it not? |
| 0x1243c2 | 6 | Hnngh? |
| 0x1243c9 | 44 | Mikazuchi is glaring sharper daggers at me\n |
| 0x1243f6 | 17 | than ever before. |
| 0x124408 | 45 | Shit. That little display just now probably\n |
| 0x124436 | 14 | annoyed him... |
| 0x124445 | 46 | I swallow dryly, dreading whatever Mikazuchi\n |
| 0x124474 | 40 | has in store for me next. He continues\n |
| 0x12449d | 9 | speaking. |
| 0x1244a7 | 45 | It seems as though that girl has placed her\n |
| 0x1244d5 | 13 | trust in you. |
| 0x1244e3 | 47 | Are--are you fucking serious? After what just\n |
| 0x124513 | 44 | happened? I thought my jewels were done for! |
| 0x124540 | 44 | Mikazuchi glances down, speaking almost to\n |
| 0x12456d | 43 | I used to have a sister myself, you know.\n |
| 0x124599 | 39 | Our relationship wasn't especially bad. |
| 0x1245c1 | 47 | Inform Oshtor that all will be arranged as he\n |
| 0x1245f1 | 46 | wills it. And... I trust you to protect that\n |
| 0x124620 | 17 | girl, understand? |
| 0x124632 | 26 | What's that supposed to... |
| 0x12464d | 43 | With that, Mikazuchi falls silent. Again.\n |
| 0x124679 | 48 | I think... I'm starting to understand this guy\n |
| 0x1246aa | 14 | a little more. |
| 0x1246b9 | 39 | He really is concerned for Nekone, huh? |
| 0x1246e1 | 42 | I will see our guests out, Lord Mikazuchi. |
| 0x12470c | 43 | The squire from before reappears, sensing\n |
| 0x124738 | 39 | that Mikazuchi is done talking for now. |
| 0x124760 | 31 | If you would follow me, please? |
| 0x124780 | 16 | Yeah, all right. |
| 0x124791 | 45 | And please, take a token of our hospitality\n |
| 0x1247bf | 42 | back with you. I'll show you to the main\n |
| 0x1247ea | 11 | entrance... |
| 0x1247f6 | 36 | This boy seems so kind and gentle.\n |
| 0x12481b | 40 | Totally the opposite of his commander... |
| 0x124844 | 47 | By the time I take Miruhj's gift and exit the\n |
| 0x124874 | 42 | manor, it dawns on me just how late it is. |
| 0x12489f | 34 | God, I finally got out of there... |
| 0x1248c2 | 42 | All the tension leaves me in one go, and\n |
| 0x1248ed | 27 | suddenly, I feel exhausted. |
| 0x124909 | 26 | A job well done, Sir Haku. |
| 0x124924 | 36 | Nekone comes running over as I exit. |
| 0x124949 | 46 | Nekone? Were you waiting out here that whole\n |
| 0x124978 | 5 | time? |
| 0x12497e | 46 | I actually AM capable of worrying about you,\n |
| 0x1249ad | 9 | you know. |
| 0x1249b7 | 47 | I don't believe it. Of all people, Nekone was\n |
| 0x1249e7 | 17 | worried about me? |
| 0x1249f9 | 45 | I was far from certain of whether you would\n |
| 0x124a27 | 35 | come out of there alive, after all. |
| 0x124a4b | 10 | H-Ha ha... |
| 0x124a56 | 42 | Her words may sound like a joke, but I'm\n |
| 0x124a81 | 40 | getting chills just thinking about the\n |
| 0x124aaa | 12 | possibility. |
| 0x124ab7 | 46 | Shall we make our return? There is no reason\n |
| 0x124ae6 | 25 | to tarry here any longer. |
| 0x124b00 | 46 | Sounds good. I'll fill you in on the details\n |
| 0x124b2f | 16 | on the way back. |
| 0x125a69 | 40 | I take a bite of my skewer as we walk,\n |
| 0x125a92 | 19 | savoring the taste. |
| 0x125aa6 | 42 | Mmf. Looks like I made the right choice.\n |
| 0x125ad1 | 38 | That stall's kokoromo is pretty tasty. |
| 0x125af8 | 46 | The juicy fat mixes perfectly with sweet and\n |
| 0x125b27 | 44 | spicy sauce, suffusing my mouth with bold,\n |
| 0x125b54 | 14 | rich flavor... |
| 0x125b63 | 20 | Mysterious duo right |
| 0x125b7c | 19 | Mysterious duo left |
| 0x125b90 | 33 | And what exactly do you two want? |
| 0x125bb2 | 43 | All of a sudden, that mysterious duo from\n |
| 0x125bde | 44 | before appears on either side of me, quiet\n |
| 0x125c0b | 16 | and unannounced. |
| 0x125c1c | 48 | You two just disappeared as soon as we arrived\n |
| 0x125c4d | 43 | at the capital. Where did you get off to,\n |
| 0x125c79 | 7 | anyway? |
| 0x125c81 | 45 | Yeah, you're about as chatty as I remember.\n |
| 0x125caf | 10 | Good talk. |
| 0x125cba | 49 | I can't even make out their expressions because\n |
| 0x125cec | 26 | of those head coverings... |
| 0x125d07 | 48 | Y'know, it's kinda hard to see where I'm going\n |
| 0x125d38 | 46 | with you two all snuggled up to me like this-- |
| 0x125d67 | 45 | These two don't seem to have any concept of\n |
| 0x125d95 | 42 | personal space, but at least they're not\n |
| 0x125dc0 | 15 | hurting anyone. |
| 0x125dd0 | 44 | I don't THINK they have any particular ill\n |
| 0x125dfd | 29 | intent toward me, at least... |
| 0x125e1b | 8 | ...What? |
| 0x125e24 | 49 | I can't see their eyes, so it's just a feeling,\n |
| 0x125e56 | 46 | but I could swear they're staring at me. Or... |
| 0x125e85 | 49 | Or they're staring at the bag of skewers I just\n |
| 0x125eb7 | 18 | bought. Of course. |
| 0x125eca | 23 | Oh. You guys want some? |
| 0x125ee2 | 46 | You know, I'm not sure why I was expecting a\n |
| 0x125f11 | 9 | response. |
| 0x125f1b | 13 | Here, dig in. |
| 0x125f29 | 26 | I hand them each a skewer. |
| 0x125f44 | 49 | They both accept the skewers, then quietly tuck\n |
| 0x125f76 | 42 | in, holding them up beneath their masks... |
| 0x125fa1 | 45 | I mean, I think they're eating? Hard to see\n |
| 0x125fcf | 32 | anything through all that cloth. |
| 0x125ff0 | 12 | You like it? |
| 0x125ffd | 35 | In unison, they nod their approval. |
| 0x126021 | 23 | Yeah? Glad you like it. |
| 0x126039 | 46 | We walk in silence for a while, eating while\n |
| 0x126068 | 43 | we take in the city... It's kind of nice,\n |
| 0x126094 | 9 | actually. |
| 0x12609e | 16 | Ah, Sir Haku...? |
| 0x1260af | 30 | Oh, hullo, love. Out shopping? |
| 0x1260ce | 40 | Eating out more than shopping, really.\n |
| 0x1260f7 | 22 | What're you two up to? |
| 0x12610e | 45 | Rulie tipped me off to the CUTEST hair pins\n |
| 0x12613c | 43 | at this one stall. She took me to see the\n |
| 0x126168 | 6 | place! |
| 0x12616f | 45 | Y-Yes, I think they suit Miss Atuy very well. |
| 0x12619d | 15 | Hair pins, huh? |
| 0x1261ad | 45 | Nearby, I spy the vendor in question, their\n |
| 0x1261db | 44 | stall loaded up with hair ornaments of all\n |
| 0x126208 | 6 | kinds. |
| 0x12620f | 45 | That Rulutieh is interested is a given, but\n |
| 0x12623d | 48 | Atuy? I didn't think she'd be into this frilly\n |
| 0x12626e | 8 | stuff... |
| 0x126277 | 46 | Just taking in the sights on your own, then,\n |
| 0x1262a6 | 5 | love? |
| 0x1262ac | 40 | On my own? What are you talking about,\n |
| 0x1262d5 | 19 | I've got th... Huh? |
| 0x1262e9 | 47 | That strange pair, of course, has disappeared\n |
| 0x126319 | 35 | without so much as a word. Figures. |
| 0x12633d | 14 | This again...? |
| 0x12634c | 44 | Those two just come and go as they please,\n |
| 0x126379 | 4 | huh. |
| 0x12637e | 8 | "Again?" |
| 0x126387 | 45 | A-At any rate, I was just taking a walk and\n |
| 0x1263b5 | 45 | got hungry. I picked up some food along the\n |
| 0x1263e3 | 4 | way. |
| 0x1263e8 | 21 | Oh! That smells good. |
| 0x1263fe | 45 | Atuy's ears prick up as she takes notice of\n |
| 0x12642c | 12 | the skewers. |
| 0x126439 | 43 | Hee. I'll just have a little sample, here-- |
| 0x126465 | 47 | Atuy snatches the final skewer out of the bag\n |
| 0x126495 | 21 | before I can protest. |
| 0x1264ab | 31 | Wh--Hey? That was the last one! |
| 0x1264cb | 17 | *Hromf, munch*... |
| 0x1264dd | 47 | I-I already took a bite out of that one, too... |
| 0x12650d | 12 | M-Miss Atuy? |
| 0x12651a | 32 | Mmf, thif if really good--ulp.\n |
| 0x12653b | 26 | Hey, could I have another? |
| 0x126556 | 33 | Like hell! That was the last one. |
| 0x126578 | 32 | Aw, that's too bad. Sorry, love. |
| 0x126599 | 46 | Why don't we go and get some more, then, eh?\n |
| 0x1265c8 | 32 | Come on, it was this way, right? |
| 0x1265e9 | 45 | Atuy wraps her arm around mine before I can\n |
| 0x126617 | 8 | protest. |
| 0x126620 | 23 | C'mon, Rulie, let's go. |
| 0x126638 | 5 | Um... |
| 0x12663e | 46 | And so, I ended up going back the way I came\n |
| 0x12666d | 30 | with Rulutieh and Atuy in tow. |
| 0x12668c | 47 | So did you already buy that hair pin you were\n |
| 0x1266bc | 12 | looking for? |
| 0x1266c9 | 49 | Well, there were so many kinds, I couldn't make\n |
| 0x1266fb | 40 | up my mind! Shopping in the capital is\n |
| 0x126724 | 13 | mind-blowing. |
| 0x126732 | 44 | Um... I-I thought that red one looked very\n |
| 0x12675f | 12 | nice on you. |
| 0x12676c | 43 | Hee! Rulie, you know how to flatter a girl. |
| 0x126798 | 22 | What did it look like? |
| 0x1267af | 42 | Well, it was about this big... and had a\n |
| 0x1267da | 24 | floral pattern all over. |
| 0x1267f3 | 35 | Yeah, that one was really pretty... |
| 0x126817 | 32 | Oh... I'm sorry, I didn't mean-- |
| 0x126838 | 47 | Aw, no need to apologize. It's nobody's fault\n |
| 0x126868 | 15 | but mine, dear. |
| 0x126878 | 49 | Judging by their disappointment, it sounds like\n |
| 0x1268aa | 40 | someone else bought it while they were\n |
| 0x1268d3 | 9 | browsing. |
| 0x1268dd | 45 | And besides, it's more romantic to get that\n |
| 0x12690b | 48 | sort of thing from your lover as a gift, don't\n |
| 0x12693c | 10 | you think? |
| 0x126947 | 45 | He'd say something like, "Atuy, this is the\n |
| 0x126975 | 43 | only charm I could find that matches your\n |
| 0x1269a1 | 10 | beauty..." |
| 0x1269ac | 49 | And then he'll gently stroke my hair, and slide\n |
| 0x1269de | 44 | the pin on while staring into my eyes, and\n |
| 0x126a0b | 6 | then-- |
| 0x126a12 | 45 | Yeah, yeah. Keep the fantasies to a minimum\n |
| 0x126a40 | 18 | around me, please. |
| 0x126a53 | 47 | It doesn't even have to be that expensive, as\n |
| 0x126a83 | 44 | long as it's chosen by my sweetheart's own\n |
| 0x126ab0 | 5 | hand. |
| 0x126ab6 | 38 | Atuy gives a small, embarrassed laugh. |
| 0x126add | 45 | Oh, but I've forgotten all about the skewers! |
| 0x126b0b | 44 | Let's hurry up, eh? Wouldn't want those to\n |
| 0x126b38 | 36 | sell out before I get there, either! |
| 0x126b5d | 49 | She trots forward, pulling me along by the arm,\n |
| 0x126b8f | 34 | and Rulutieh struggles to keep up. |
| 0x126bb2 | 47 | Must be tough hanging out with Atuy. Does she\n |
| 0x126be2 | 47 | pull you around everywhere like she does with\n |
| 0x126c12 | 3 | me? |
| 0x126c16 | 37 | N-Not at all! I enjoy every moment... |
| 0x126c3c | 47 | And besides... those skewers looked, um, very\n |
| 0x126c6c | 5 | good. |
| 0x126c72 | 47 | She seems shy about expressing an interest in\n |
| 0x126ca2 | 25 | the food for some reason. |
| 0x126cbc | 47 | Well, I can guarantee the taste will be up to\n |
| 0x126cec | 25 | scratch, if nothing else. |
| 0x126d06 | 47 | Ah, here we are. 'Scuse me, sir, could we get\n |
| 0x126d36 | 21 | another bag of these? |
| 0x126d4c | 37 | Hee. And you're paying, of course--\n |
| 0x126d72 | 12 | right, love? |
| 0x126d7f | 33 | She looks eagerly back toward me. |
| 0x126da1 | 24 | Oh... Um... no, I can... |
| 0x126dba | 21 | Urk. Yeah, all right. |
| 0x126dd0 | 46 | I decide to play the gentleman and treat the\n |
| 0x126dff | 35 | two of them, pulling out my wallet. |
| 0x128ccf | 7 | Yawn... |
| 0x128cd7 | 3 | Hm? |
| 0x128cdb | 46 | Nngh. It's too early in the morning for this\n |
| 0x128d0a | 14 | much racket... |
| 0x128d19 | 6 | Worker |
| 0x128d20 | 43 | Pardon me! Excuse me, sir, coming through-- |
| 0x128d4c | 5 | Whup. |
| 0x128d52 | 48 | The inn's housekeepers and workers dash up and\n |
| 0x128d83 | 38 | down the hallway with determination... |
| 0x128daa | 49 | Are they setting up for a banquet or something?\n |
| 0x128ddc | 43 | They're working awfully hard, and awfully\n |
| 0x128e08 | 8 | early... |
| 0x128e11 | 22 | Something wrong, Haku? |
| 0x128e28 | 48 | Kuon nudges me from behind, looking as puzzled\n |
| 0x128e59 | 8 | as I am. |
| 0x128e62 | 20 | Oh, morning, Kuon... |
| 0x128e77 | 45 | Go wash up and get yourself properly awake,\n |
| 0x128ea5 | 20 | huh? Big day today.  |
| 0x128eba | 8 | Big day? |
| 0x128ec3 | 42 | My confusion only grows. Am I forgetting\n |
| 0x128eee | 18 | something obvious? |
| 0x128f01 | 43 | Uh, were we supposed to do something today? |
| 0x128f2d | 7 | Haku... |
| 0x128f35 | 24 | Kuon sounds exasperated. |
| 0x128f4e | 44 | The nativity festival? Today? We've talked\n |
| 0x128f7b | 44 | about this before. Multiple times, actually. |
| 0x128fa8 | 48 | You can't have missed all the decorations that\n |
| 0x128fd9 | 30 | have been going up recently... |
| 0x128ff8 | 21 | Nativity... festival? |
| 0x12900e | 41 | ...Oh. The princess of Yamato's birthday? |
| 0x129038 | 48 | I know you're not from around here, but try to\n |
| 0x129069 | 42 | show at least a LITTLE interest in local\n |
| 0x129094 | 8 | culture. |
| 0x12909d | 38 | I do show interest in local culture!\n |
| 0x1290c4 | 32 | Like... the food. And the booze. |
| 0x1290e9 | 45 | A-And the princess's birthday above all, of\n |
| 0x129117 | 33 | course. What is she like, anyway? |
| 0x129139 | 47 | I mean, I hear a lot about the Mikado, but it\n |
| 0x129169 | 47 | doesn't seem like anyone ever talks about his\n |
| 0x129199 | 4 | kid. |
| 0x12919e | 18 | Well, let's see... |
| 0x1291b1 | 48 | Kuon tilts her head in thought as she conjures\n |
| 0x1291e2 | 11 | a response. |
| 0x1291ee | 48 | If the rumors are true, she's quite young, but\n |
| 0x12921f | 43 | she's supposed to be very intelligent and\n |
| 0x12924b | 9 | charming. |
| 0x129255 | 9 | ...I see. |
| 0x12925f | 45 | "Intelligent and charming" is pretty bland,\n |
| 0x12928d | 42 | honestly. That just makes her more of an\n |
| 0x1292b8 | 9 | enigma... |
| 0x1292c2 | 49 | Kuon lets out a small sound as she looks at me,\n |
| 0x1292f4 | 8 | smiling. |
| 0x1292fd | 44 | Could it be a mysterious imperial flower's\n |
| 0x12932a | 22 | caught your eye, Haku? |
| 0x129341 | 46 | Eh, not particularly. I'm curious, more than\n |
| 0x129370 | 14 | anything else. |
| 0x12937f | 40 | No point in chasing after the empire's\n |
| 0x1293a8 | 42 | "beautiful flower" if it grows up beyond\n |
| 0x1293d3 | 11 | the clouds. |
| 0x1293df | 46 | Honestly, I'm more excited about the vendors\n |
| 0x12940e | 46 | at this festival. I bet there'll be loads of\n |
| 0x12943d | 5 | food. |
| 0x129443 | 42 | Ahaha! Haku, you can really be childlike\n |
| 0x12946e | 10 | sometimes. |
| 0x129479 | 48 | What, I'm the childlike one? Then why did your\n |
| 0x1294aa | 46 | tail start wagging when I mentioned the food\n |
| 0x1294d9 | 6 | carts? |
| 0x1294e0 | 46 | Kuon quickly stills her tail with her hands,\n |
| 0x12950f | 10 | going red. |
| 0x12951a | 4 | Urk. |
| 0x12951f | 46 | I-In any case, I was going to ask--Would you\n |
| 0x12954e | 40 | want to... go see the festival together? |
| 0x129577 | 4 | Huh? |
| 0x12957c | 47 | The talk is that the princess will be paraded\n |
| 0x1295ac | 43 | through the city atop a mikoshi--a grand,\n |
| 0x1295d8 | 14 | mobile shrine. |
| 0x1295e7 | 49 | Kuon grabs my hand and starts pulling me along,\n |
| 0x129619 | 44 | innocent wonder on her face at the prospect. |
| 0x129646 | 41 | If she wants to spend a day having fun,\n |
| 0x129670 | 20 | I can hardly object. |
| 0x129685 | 46 | All right, all right. Let me go get dressed,\n |
| 0x1296b4 | 45 | OK? I can't exactly go out looking like this. |
| 0x1296e2 | 14 | OK, but hurry! |
| 0x1296f1 | 11 | Yeah, yeah. |
| 0x1296fd | 47 | As I turn to go get ready, it suddenly occurs\n |
| 0x12972d | 8 | to me... |
| 0x129736 | 39 | Where did Rulutieh and Atuy get off to? |
| 0x12975e | 44 | Well, they're princesses too, aren't they?\n |
| 0x12978b | 47 | They'll have duties of some kind at the palace. |
| 0x1297bb | 10 | Oh, right. |
| 0x1297c6 | 43 | It's easy to forget they're here as their\n |
| 0x1297f2 | 48 | fathers' representatives. I'm so familiar with\n |
| 0x129823 | 12 | them, now... |
| 0x129830 | 40 | Nekone and Kiwru will be with them, too. |
| 0x129859 | 48 | Shame we won't all be able to see it together,\n |
| 0x12988a | 48 | but it's a festival, isn't it? I'm gonna enjoy\n |
| 0x1298bb | 7 | myself. |
| 0x1298c3 | 6 | Ugh... |
| 0x1298ca | 48 | As Kuon and I reach the main plaza, we find it\n |
| 0x1298fb | 29 | already packed with people... |
| 0x129919 | 43 | Looks like everyone is clamoring to get a\n |
| 0x129945 | 33 | glimpse of the imperial princess. |
| 0x129967 | 42 | I should've expected this place would be\n |
| 0x129992 | 9 | packed... |
| 0x12999c | 10 | Hey, Kuon. |
| 0x1299a7 | 11 | What is it? |
| 0x1299b3 | 47 | Can I go home? All these people around me are\n |
| 0x1299e3 | 27 | making me claustrophobic... |
| 0x1299ff | 47 | At this rate, we're not even gonna get a look\n |
| 0x129a2f | 38 | at the shrine, let alone the princess. |
| 0x129a56 | 45 | I think... I think I may have misjudged the\n |
| 0x129a84 | 10 | situation. |
| 0x129a8f | 43 | A particularly loud cheer in the distance\n |
| 0x129abb | 14 | interrupts us. |
| 0x129aca | 48 | It seems as though the princess's palanquin is\n |
| 0x129afb | 19 | fast approaching... |
| 0x129b0f | 46 | So, what do we do? If we stay here, the only\n |
| 0x129b3e | 46 | view we're getting is the back of this guy's\n |
| 0x129b6d | 5 | head. |
| 0x129b73 | 30 | And then an idea occurs to me. |
| 0x129b92 | 50 | Hey, hang on. The parade goes all the way around\n |
| 0x129bc5 | 48 | the capital, right? Does it go to the Mausoleum? |
| 0x129bf6 | 21 | I would imagine so... |
| 0x129c0c | 45 | That's where she's supposed to step off the\n |
| 0x129c3a | 29 | shrine to greet the cityfolk. |
| 0x129c58 | 43 | Wouldn't it be better for us to wait over\n |
| 0x129c84 | 12 | there, then? |
| 0x129c91 | 45 | Maybe, but the parade travels slowly. It'll\n |
| 0x129cbf | 38 | take a while for it to get over there. |
| 0x129ce6 | 46 | Even better. It's a pretty big place, and if\n |
| 0x129d15 | 43 | it'll be a while yet, it shouldn't be too\n |
| 0x129d41 | 8 | crowded. |
| 0x129d4a | 50 | We came all the way here for this, and I'm gonna\n |
| 0x129d7d | 42 | be disappointed if we don't actually SEE\n |
| 0x129da8 | 9 | anything. |
| 0x129db2 | 49 | I won't be satisfied until I can marvel at this\n |
| 0x129de4 | 44 | grand "imperial flower" you keep talking up. |
| 0x129e11 | 46 | Heh, I suppose you're right. We did come all\n |
| 0x129e40 | 9 | this way. |
| 0x129e4a | 16 | Oh, but first... |
| 0x129e5b | 47 | If it's going to take a while, let's get some\n |
| 0x129e8b | 11 | food first. |
| 0x129e97 | 9 | *Sigh*... |
| 0x129ea1 | 48 | Ultimately, we make our way out of the crowded\n |
| 0x129ed2 | 30 | plaza and on to the Mausoleum. |
| 0x129ef1 | 48 | It's a much wider area than the plaza, and not\n |
| 0x129f22 | 35 | nearly as mobbed--at least not yet. |
| 0x129f46 | 29 | This ought to be a good spot. |
| 0x129f64 | 7 | Agreed. |
| 0x129f6c | 47 | We manage to find a spot near the front, then\n |
| 0x129f9c | 47 | settle in to wait for the parade with our food. |
| 0x129fcc | 6 | Hm...? |
| 0x129fd3 | 43 | As I glance over to where the princess is\n |
| 0x129fff | 47 | supposed to arrive in front of the Mausoleum... |
| 0x12a02f | 47 | I spy a row of intimidating figures assembled\n |
| 0x12a05f | 43 | there, as though waiting for the palanquin. |
| 0x12a08b | 41 | They have to be mononofu of some kind--\n |
| 0x12a0b5 | 33 | all of them are carrying weapons. |
| 0x12a0d7 | 29 | Who're those guys over there? |
| 0x12a0f5 | 43 | Kuon follows my gaze to the figures, then\n |
| 0x12a121 | 15 | nods knowingly. |
| 0x12a131 | 26 | The Eight Pillar Generals. |
| 0x12a14c | 47 | I suppose all eight of them have assembled to\n |
| 0x12a17c | 18 | meet the princess. |
| 0x12a18f | 17 | So that's them... |
| 0x12a1a1 | 46 | Mhm. Just as their name implies, they're the\n |
| 0x12a1d0 | 43 | pillars that uphold the empire's military\n |
| 0x12a1fc | 8 | might... |
| 0x12a205 | 21 | Vurai the Vanguard... |
| 0x12a21b | 48 | He's extremely devoted to the Mikado, even for\n |
| 0x12a24c | 48 | a general, and is renowned for his raw strength. |
| 0x12a27d | 46 | Rumor is that his Akuruka was granted to him\n |
| 0x12a2ac | 42 | because he showed astounding battlefield\n |
| 0x12a2d7 | 8 | prowess. |
| 0x12a2e0 | 43 | An Akuruka...? You mean like Oshtor's mask? |
| 0x12a30c | 48 | Yep. They're something of a symbol of power in\n |
| 0x12a33d | 7 | Yamato. |
| 0x12a345 | 40 | Not even all of the Pillars have them.\n |
| 0x12a36e | 47 | The Mikado has to recognize you as a peerless\n |
| 0x12a39e | 15 | warrior, first. |
| 0x12a3ae | 8 | I see... |
| 0x12a3b7 | 17 | Raiko the Sage... |
| 0x12a3c9 | 45 | Word is he's not very skilled with weapons,\n |
| 0x12a3f7 | 45 | but he's an unmatched master of tactics and\n |
| 0x12a425 | 9 | strategy. |
| 0x12a42f | 43 | Supposedly, he's taken entire strongholds\n |
| 0x12a45b | 45 | without a fight. Not a single drop of blood\n |
| 0x12a489 | 17 | spilled, I think. |
| 0x12a49b | 49 | Capturing a fortress without fighting an actual\n |
| 0x12a4cd | 34 | battle? Is he some kind of wizard? |
| 0x12a4f0 | 45 | He's also the elder brother of the Imperial\n |
| 0x12a51e | 34 | Guard of the Left, Lord Mikazuchi. |
| 0x12a541 | 26 | A family of bigwigs, eh... |
| 0x12a55c | 25 | Soyankekur the Mariner... |
| 0x12a576 | 48 | He's Shyahoro's ruling owlo, but also commands\n |
| 0x12a5a7 | 48 | Yamato's seas. All maritime trade goes through\n |
| 0x12a5d8 | 4 | him. |
| 0x12a5dd | 44 | Not to mention he's a naval combat expert.\n |
| 0x12a60a | 43 | There's a reason pirates don't operate in\n |
| 0x12a636 | 16 | Shyahoro waters. |
| 0x12a647 | 44 | So that's Atuy's father... She really is a\n |
| 0x12a674 | 25 | bona fide princess, then. |
| 0x12a68e | 38 | ...I can see the resemblance, I guess. |
| 0x12a6b5 | 21 | Ozen the Harvester... |
| 0x12a6cb | 44 | He fights well, but more important are the\n |
| 0x12a6f8 | 47 | agricultural miracles he works as owlo of the\n |
| 0x12a728 | 11 | wastelands. |
| 0x12a734 | 32 | And he's also Rulutieh's father. |
| 0x12a755 | 49 | Who would've thought that a dainty little thing\n |
| 0x12a787 | 44 | like Rulutieh is this guy's daughter? He's\n |
| 0x12a7b4 | 13 | terrifying... |
| 0x12a7c2 | 23 | Tokifusa the Attuner... |
| 0x12a7da | 42 | He's not... really renowned for anything\n |
| 0x12a805 | 45 | specific, but he adapts easily to all sorts\n |
| 0x12a833 | 11 | of tactics. |
| 0x12a83f | 47 | He's usually sent to put down rebellions, and\n |
| 0x12a86f | 48 | holds the line for the more specialized Pillars. |
| 0x12a8a0 | 47 | He must be skilled, to adapt to any role like\n |
| 0x12a8d0 | 48 | that--but next to the others, he doesn't stand\n |
| 0x12a901 | 4 | out. |
| 0x12a906 | 44 | He wields a bow that's longer than his own\n |
| 0x12a933 | 46 | height. Maybe Oshtor could set up a sparring\n |
| 0x12a962 | 14 | match for you? |
| 0x12a971 | 16 | Yeah, no thanks. |
| 0x12a982 | 25 | Woshis the Shadowlight... |
| 0x12a99c | 47 | He acts as a mediator for the other generals,\n |
| 0x12a9cc | 47 | mostly. His serene personality is perfect for\n |
| 0x12a9fc | 3 | it. |
| 0x12aa00 | 49 | Huh... Could be my imagination, but have I seen\n |
| 0x12aa32 | 16 | that guy before? |
| 0x12aa43 | 47 | I don't know much about his past, but if he's\n |
| 0x12aa73 | 44 | a Pillar, he must have the Mikado's utmost\n |
| 0x12aaa0 | 6 | trust. |
| 0x12aaa7 | 13 | ...Dekopompo. |
| 0x12aab5 | 49 | Urgh, right. He's one of the Eight Pillars too,\n |
| 0x12aae7 | 9 | isn't he? |
| 0x12aaf1 | 46 | Pretty sure you already know all you NEED to\n |
| 0x12ab20 | 15 | know about him. |
| 0x12ab30 | 44 | Welp. You don't have any other info on the\n |
| 0x12ab5d | 4 | guy? |
| 0x12ab62 | 40 | Not a lot. There's not much out there,\n |
| 0x12ab8b | 45 | honestly--I don't know why he's a Pillar to\n |
| 0x12abb9 | 11 | begin with. |
| 0x12abc5 | 45 | I totally forgot that windbag is one of the\n |
| 0x12abf3 | 46 | Eight Pillar Generals. Must be a pillar full\n |
| 0x12ac22 | 18 | of bugs and rot... |
| 0x12ac35 | 48 | And that leaves... oh, doesn't look like she's\n |
| 0x12ac66 | 41 | up there, but her name is Munechika the\n |
| 0x12ac90 | 9 | Guardian. |
| 0x12ac9a | 48 | Her specialty is defensive strategy, and she's\n |
| 0x12accb | 40 | defended entire nations from barbarians. |
| 0x12acf4 | 46 | The Mikado bestowed an Akuruka upon her when\n |
| 0x12ad23 | 44 | her extraordinary abilities became apparent. |
| 0x12ad50 | 46 | Munechika must be accompanying the princess,\n |
| 0x12ad7f | 43 | since she bears the duty of acting as her\n |
| 0x12adab | 9 | guardian. |
| 0x12adb5 | 14 | Makes sense... |
| 0x12adc4 | 32 | I'm surprised you know all this. |
| 0x12ade5 | 45 | You know their names, matched their faces--\n |
| 0x12ae13 | 47 | you even knew about Raiko and Mikazuchi being\n |
| 0x12ae43 | 8 | related. |
| 0x12ae4c | 43 | Have you been gathering info on them this\n |
| 0x12ae78 | 11 | whole time? |
| 0x12ae84 | 38 | I-I just... enjoy learning, I suppose? |
| 0x12aeab | 8 | That so? |
| 0x12aeb4 | 44 | Y-Yes! It pays to know things. You need to\n |
| 0x12aee1 | 41 | stop being so ignorant of all this, Haku. |
| 0x12af0b | 45 | The Eight Pillar Generals are all household\n |
| 0x12af39 | 40 | names! Even children know them by heart. |
| 0x12af62 | 6 | O...K? |
| 0x12af69 | 4 | Yes! |
| 0x12af6e | 34 | ...Oh! Look, the parade is coming! |
| 0x12af91 | 5 | Oh... |
| 0x12af97 | 45 | A loud cheer goes up around us as I catch a\n |
| 0x12afc5 | 45 | glimpse of the mikoshi--the mobile shrine--\n |
| 0x12aff3 | 12 | not far off. |
| 0x12b000 | 42 | It's hard to make out her face, but that\n |
| 0x12b02b | 38 | general walking out in front must be\n |
| 0x12b052 | 12 | Munechika... |
| 0x12b05f | 46 | And Oshtor and Mikazuchi have taken up their\n |
| 0x12b08e | 45 | positions on either side as the Twin Shields. |
| 0x12b0bc | 46 | It's easy to forget Oshtor is a proper noble\n |
| 0x12b0eb | 42 | sometimes. But when I see him like this... |
| 0x12b116 | 5 | Yeah. |
| 0x12b11c | 47 | It makes me think the Oshtor we actually know\n |
| 0x12b14c | 16 | is just a dream. |
| 0x12b15d | 46 | The portable shrine comes to a stop, and the\n |
| 0x12b18c | 44 | princess descends to meet the Eight Pillar\n |
| 0x12b1b9 | 9 | Generals. |
| 0x12b1c3 | 17 | Here she comes... |
| 0x12b1d5 | 47 | Now then, let's see what the beloved princess\n |
| 0x12b205 | 20 | actually looks like. |
| 0x12b21a | 43 | I lean forward toward the shrine to get a\n |
| 0x12b246 | 14 | better look... |
| 0x12b255 | 7 | Whoa... |
| 0x12b25d | 47 | I can't help but exclaim as I lay eyes on the\n |
| 0x12b28d | 45 | elegant, glittering clothing she's wearing... |
| 0x12b2bb | 34 | ...but I can't quite see her face. |
| 0x12b2de | 49 | A decorative cloth covers up most of her face--\n |
| 0x12b310 | 38 | I can't see a thing, no features, no\n |
| 0x12b337 | 13 | expression... |
| 0x12b345 | 49 | Her frame is very small, though. She must still\n |
| 0x12b377 | 11 | be a child. |
| 0x12b383 | 46 | The regal princess stops before the crowd to\n |
| 0x12b3b2 | 45 | raise her hand, and the people around me go\n |
| 0x12b3e0 | 5 | wild. |
| 0x12b3e6 | 44 | All eyes are on the princess--not just the\n |
| 0x12b413 | 41 | crowd's, but the Pillars' and the other\n |
| 0x12b43d | 18 | authorities', too. |
| 0x12b450 | 48 | Seems she isn't fazed a bit by all the crowds.\n |
| 0x12b481 | 41 | I guess I should expect as much from an\n |
| 0x12b4ab | 20 | imperial princess... |
| 0x12b4c0 | 48 | As I jostle to try and get a look at her face,\n |
| 0x12b4f1 | 44 | she disappears into the Mausoleum with her\n |
| 0x12b51e | 10 | retainers. |
| 0x12b529 | 45 | Damn. I was able to see her wave, at least,\n |
| 0x12b557 | 48 | if not her face... I guess we should head back\n |
| 0x12b588 | 4 | now. |
| 0x12b58d | 5 | Kuon? |
| 0x12b593 | 27 | You see something you like? |
| 0x12b5af | 43 | No, it's nothing. Come on, let's get going. |
| 0x12b5db | 48 | It was hard to tell with the princess, but the\n |
| 0x12b60c | 43 | presence those Eight Pillar Generals had... |
| 0x12b638 | 46 | It terrified me, in a way. Makes me glad I'm\n |
| 0x12b667 | 14 | just a nobody. |
| 0x12b676 | 35 | Hope I never get on their bad side. |
| 0x12b69a | 5 | Haku? |
| 0x12b6a0 | 49 | Sorry, yeah, let's head back. Want to hit those\n |
| 0x12b6d2 | 29 | food stalls again on the way? |
| 0x12b6f0 | 39 | That sounds like a great idea, I think. |
| 0x12ea0f | 22 | Whew... Man, I'm full. |
| 0x12ea26 | 40 | It's getting on toward late afternoon... |
| 0x12ea4f | 47 | We all relished Rulutieh's cooking for lunch,\n |
| 0x12ea7f | 47 | and now, we're slowly making our way back home. |
| 0x12eaaf | 49 | Now all I have to do is contrive a way to sneak\n |
| 0x12eae1 | 49 | in a power nap where Kuon and Nekone can't find\n |
| 0x12eb13 | 5 | me... |
| 0x12eb19 | 46 | They're catching onto my secret technique of\n |
| 0x12eb48 | 44 | sleeping with my eyes open. Time for a new\n |
| 0x12eb75 | 7 | tactic. |
| 0x12eb7d | 3 | Hm? |
| 0x12eb86 | 46 | I open the door to our base of operations to\n |
| 0x12ebb5 | 37 | find a girl I've never seen before... |
| 0x12ebdb | 48 | She's lazily draped over the couch and reading\n |
| 0x12ec0c | 18 | some kind of book. |
| 0x12ec1f | 44 | And she has snacks and a drink just within\n |
| 0x12ec4c | 43 | arm's reach. She certainly looks relaxed... |
| 0x12ec78 | 47 | Because of her position, her skirt is splayed\n |
| 0x12eca8 | 35 | wide, baring everything underneath. |
| 0x12eccc | 47 | She hums innocently, flipping the page of her\n |
| 0x12ecfc | 43 | book, and reaches for another bite of her\n |
| 0x12ed28 | 9 | snacks... |
| 0x12ed32 | 50 | She's just... lying there. As I watch, she takes\n |
| 0x12ed65 | 39 | a swig of her drink, indulging herself. |
| 0x12ed8d | 37 | ...and now she's scratching her butt. |
| 0x12edb3 | 43 | Truly, I behold a paragon of lazing around. |
| 0x12eddf | 10 | ...My bad. |
| 0x12edea | 49 | Yikes. Almost made a fool of myself, going into\n |
| 0x12ee1c | 18 | the wrong... Wait. |
| 0x12ee2f | 48 | I look around to make sure. This definitely is\n |
| 0x12ee60 | 9 | our room. |
| 0x12ee6a | 34 | I don't THINK I'm wrong, at least? |
| 0x12ee8d | 18 | What's the matter? |
| 0x12eea0 | 27 | You're not gonna go inside? |
| 0x12eebc | 44 | There's, uh, a girl I don't know in there.\n |
| 0x12eee9 | 13 | Butt and all. |
| 0x12eef7 | 12 | Sir Haku...? |
| 0x12ef04 | 32 | What are you even talking about? |
| 0x12ef25 | 44 | Hold on, hold on. Rulutieh, would you stop\n |
| 0x12ef52 | 29 | looking at me like I'm crazy? |
| 0x12ef70 | 43 | Rulutieh's gaze in particular digs into me. |
| 0x12ef9c | 28 | ...Maybe I just imagined it. |
| 0x12efb9 | 41 | There's no way there'd just be a random\n |
| 0x12efe3 | 25 | uninvited girl in our r-- |
| 0x12effd | 13 | Who the hell? |
| 0x12f00b | 20 | Ah, you've returned! |
| 0x12f020 | 46 | I've waited upon your arrival for quite some\n |
| 0x12f04f | 44 | time, now. You must be the Haku I've heard\n |
| 0x12f07c | 14 | so much about. |
| 0x12f08b | 48 | The stranger tosses aside her book and sits up\n |
| 0x12f0bc | 12 | to greet us. |
| 0x12f0c9 | 20 | W-Wait, that book... |
| 0x12f0de | 44 | I can hear the tremble in Rulutieh's voice\n |
| 0x12f10b | 10 | behind me. |
| 0x12f116 | 44 | Hm? Something about this book bothers you?\n |
| 0x12f143 | 43 | I chanced upon it, I admit, hidden in the\n |
| 0x12f16f | 11 | lining of-- |
| 0x12f17b | 5 | A-Ah! |
| 0x12f181 | 46 | In a flash, Rulutieh darts into the room and\n |
| 0x12f1b0 | 44 | snatches the book, holding it to her chest\n |
| 0x12f1dd | 8 | tightly. |
| 0x12f1e6 | 15 | What... the...? |
| 0x12f1f6 | 49 | I gaze in amazement. This doesn't seem like the\n |
| 0x12f228 | 18 | Rulutieh I know... |
| 0x12f23b | 40 | I must say, that volume's contents are\n |
| 0x12f264 | 45 | fascinating indeed. I'd never heard of such\n |
| 0x12f292 | 6 | tales. |
| 0x12f299 | 47 | The depths of friendship shared by two men...\n |
| 0x12f2c9 | 33 | they are touching stories indeed. |
| 0x12f2eb | 43 | Tell me, have you the sequel it promises?\n |
| 0x12f317 | 48 | I would have you bring it, that I may read more. |
| 0x12f348 | 20 | Ah... u-uhm... ah... |
| 0x12f35d | 43 | Could you perhaps explain this particular\n |
| 0x12f389 | 45 | passage to me? The one about "his excited m-" |
| 0x12f3b7 | 20 | Aaa! AAAA! AAAAAAA!! |
| 0x12f3cc | 4 | Wh-- |
| 0x12f3d1 | 42 | Why is she yelling to drown the kid out?\n |
| 0x12f3fc | 44 | I've never seen Rulutieh like this before... |
| 0x12f429 | 33 | What exactly has gotten into her? |
| 0x12f44b | 9 | Rulutieh? |
| 0x12f455 | 4 | Eep! |
| 0x12f45a | 40 | Rulutieh jumps at the sound of my voice. |
| 0x12f483 | 10 | *Krrrk*... |
| 0x12f48e | 47 | She slowly turns her head like a rusty screw,\n |
| 0x12f4be | 42 | her cheeks red and her eyes full of tears. |
| 0x12f4e9 | 49 | She's holding that book to her chest like she's\n |
| 0x12f51b | 46 | hiding it, but what could possible be so emb-- |
| 0x12f54a | 5 | Oh.\n |
| 0x12f550 | 21 | I think I get it now. |
| 0x12f566 | 51 | Hey, Rulutieh, it's nothing to be embarrassed by.\n |
| 0x12f59a | 49 | It's only natural to be interested in that stuff. |
| 0x12f5cc | 46 | Actually, I've never read the ones meant for\n |
| 0x12f5fb | 47 | women. I'm sort of interested in what they're\n |
| 0x12f62b | 5 | like. |
| 0x12f635 | 41 | Huh? Now she's getting even redder than\n |
| 0x12f65f | 9 | before... |
| 0x12f669 | 43 | ...S-Sir Haku is... i-interested in...???\n |
| 0x12f695 | 12 | But that's-- |
| 0x12f6a2 | 49 | Rulutieh covers her face and barrels out of the\n |
| 0x12f6d4 | 27 | room as quickly as she can. |
| 0x12f6f0 | 8 | ...What? |
| 0x12f6f9 | 45 | Wow, Haku. You must be quite the sadist, to\n |
| 0x12f727 | 31 | take her apart in so few words. |
| 0x12f747 | 18 | ...I don't get it. |
| 0x12f75a | 34 | What are you all mumbling about?\n |
| 0x12f77d | 41 | Can you not see I've RUN OUT of snacks?\n |
| 0x12f7a7 | 26 | I order you to bring more. |
| 0x12f7c2 | 12 | More? What!? |
| 0x12f7cf | 41 | Those were supposed to be for EVERYONE!\n |
| 0x12f7f9 | 37 | A-And is that the mead I was saving!? |
| 0x12f81f | 33 | Urp. Yes, it was quite palatable. |
| 0x12f841 | 24 | Urgh, this girl reeks... |
| 0x12f85a | 44 | It's really hard to come by this st--a-and\n |
| 0x12f887 | 46 | you're supposed to water it down, and--I was\n |
| 0x12f8b6 | 16 | looking forwar-- |
| 0x12f8c7 | 10 | *Thump*... |
| 0x12f8d2 | 41 | Kuon sinks to the ground, in utter shock. |
| 0x12f8fc | 14 | D-Dear sister? |
| 0x12f90b | 7 | Kuon... |
| 0x12f913 | 44 | Oh, dear... she's rather torn up, isn't she? |
| 0x12f940 | 37 | You lot are quite... what's the word? |
| 0x12f966 | 40 | Insolent, yes. How dare you enjoy such\n |
| 0x12f98f | 47 | delicacies, when I've never tasted their ilk?\n |
| 0x12f9bf | 13 | Preposterous. |
| 0x12f9cd | 49 | I DEMAND seconds. Hurry along, now. I command it. |
| 0x12f9ff | 34 | Th-This girl--No, it can't be...\n |
| 0x12fa22 | 7 | Can it? |
| 0x12fa2a | 45 | Kiwru, who'd been watching the whole fiasco\n |
| 0x12fa58 | 40 | unfold in silence, begins muttering in\n |
| 0x12fa81 | 10 | disbelief. |
| 0x12fa8c | 23 | Friend of yours, Kiwru? |
| 0x12faa4 | 36 | W-Well... no, it's not that, just... |
| 0x12fac9 | 47 | Enough tarrying! I ordered you to be about it\n |
| 0x12faf9 | 19 | QUICKLY, did I not? |
| 0x12fb0d | 45 | Silently, Nekone pushes the gibbering Kiwru\n |
| 0x12fb3b | 24 | aside and steps forward. |
| 0x12fb54 | 50 | Please, Your Highness. I humbly request that you\n |
| 0x12fb87 | 45 | mind yourself amongst those of lower station. |
| 0x12fbb5 | 5 | What? |
| 0x12fbbb | 17 | Your Highness...? |
| 0x12fbcd | 37 | Oh, no. Oh, no, no, it really IS her! |
| 0x12fbf3 | 45 | Kiwru suddenly flings himself to the floor,\n |
| 0x12fc21 | 42 | bowed so low his head nearly touches the\n |
| 0x12fc4c | 12 | floorboards. |
| 0x12fc59 | 3 | Ah! |
| 0x12fc5d | 47 | Gah!? Kiwru, what the hell are you bowing for\n |
| 0x12fc8d | 17 | all of a sudden-- |
| 0x12fc9f | 47 | What are YOU doing? You're in the presence of\n |
| 0x12fccf | 29 | the princess, Haku! Bow down! |
| 0x12fced | 11 | A princess? |
| 0x12fcf9 | 40 | But... you're a prince, too. So is she\n |
| 0x12fd22 | 38 | another princess like Rulutieh, or...? |
| 0x12fd49 | 43 | Please, d-don't draw such base comparisons! |
| 0x12fd75 | 42 | This is the exalted Mikado's own blood--\n |
| 0x12fda0 | 42 | his only daughter, the Imperial Princess\n |
| 0x12fdcb | 22 | and Divine Scion Anju. |
| 0x12fde2 | 27 | The... imperial princess... |
| 0x12fdfe | 14 | It can't be... |
| 0x12fe0d | 49 | Oh, wow, I didn't recognize her. I KNEW I'd met\n |
| 0x12fe3f | 45 | her before! That's definitely the princess,\n |
| 0x12fe6d | 5 | love. |
| 0x12fe73 | 44 | She spends so much time all cooped up, I'd\n |
| 0x12fea0 | 35 | forgotten what her face looks like! |
| 0x12fec4 | 46 | How could you even BEGIN to forget something\n |
| 0x12fef3 | 18 | that important...? |
| 0x12ff06 | 48 | Why are you all just idly ch-chatting!? We are\n |
| 0x12ff37 | 41 | in the PRESENCE of HER IMPERIAL HIGHNESS. |
| 0x12ff61 | 48 | Please, be at ease. This day, I wear the guise\n |
| 0x12ff92 | 38 | of a mere city girl, not a princess.\n |
| 0x12ffb9 | 11 | Understood? |
| 0x12ffc5 | 43 | Dispense with such overblown formalities,\n |
| 0x12fff1 | 14 | I implore you. |
| 0x130000 | 44 | I don't imagine you came here on your own... |
| 0x13002d | 47 | Of course I came alone! A lowly commoner girl\n |
| 0x13005d | 38 | hardly struts about flanked by guards. |
| 0x130084 | 8 | Alone... |
| 0x13008d | 45 | Alas, you needn't worry. I did leave a note\n |
| 0x1300bb | 45 | before I made my timely escape and snuck out. |
| 0x1300e9 | 15 | Snuck... out... |
| 0x1300f9 | 42 | Kiwru collapses into the fetal position,\n |
| 0x130124 | 43 | clutching his stomach. Is he still hungry\n |
| 0x130150 | 14 | after lunch..? |
| 0x13015f | 43 | Do you care to explain why you came here,\n |
| 0x13018b | 40 | Highness? I can't begin to fathom why... |
| 0x1301b4 | 43 | Ah, yes, yes. I'd nearly forgotten in the\n |
| 0x1301e0 | 11 | excitement. |
| 0x1301ec | 49 | There is but one reason I descend upon your inn\n |
| 0x13021e | 17 | this eve: Oshtor! |
| 0x130230 | 7 | Oshtor? |
| 0x130238 | 33 | Why's she talking about Oshtor?\n |
| 0x13025a | 20 | Did he do something? |
| 0x13026f | 48 | Indeed, the KNAVE Oshtor claims he has no time\n |
| 0x1302a0 | 47 | to speak with me in the palace when I entreat\n |
| 0x1302d0 | 4 | him. |
| 0x1302d5 | 48 | So, I have come to seek him out on my own terms. |
| 0x130306 | 47 | Truly, I do SO much to express myself to him,\n |
| 0x130336 | 33 | and he seems to take no notice... |
| 0x130358 | 41 | So Oshtor is the princess's favorite or\n |
| 0x130382 | 35 | something? Unless it's more like... |
| 0x1303a6 | 44 | Nekone is slowly losing all emotion in her\n |
| 0x1303d3 | 7 | face... |
| 0x1303db | 36 | It's actually scaring me a little.\n |
| 0x130400 | 18 | I wish she'd stop. |
| 0x130413 | 48 | So? Speak words to me. Where is Oshtor hiding?\n |
| 0x130444 | 17 | I demand to know. |
| 0x130456 | 44 | There's hardly any reason for my dear--for\n |
| 0x130483 | 46 | Oshtor to be here. Now, if you'd be so kind,\n |
| 0x1304b2 | 16 | Highness--scram. |
| 0x1304c3 | 12 | Wh--Nekone!? |
| 0x1304d0 | 44 | You cannot fool me so easily. I've already\n |
| 0x1304fd | 45 | surmised that YOU'RE somehow connected with\n |
| 0x13052b | 7 | Oshtor. |
| 0x130533 | 33 | Now bring him to me, posthaste.\n |
| 0x130555 | 13 | I command it. |
| 0x130563 | 49 | Hold on! Hold on one second. You keep asking us\n |
| 0x130595 | 41 | to bring him here, but that's impossible. |
| 0x1305bf | 46 | First of all, Oshtor's not even here. We can\n |
| 0x1305ee | 43 | hardly bring you someone who isn't in the\n |
| 0x13061a | 9 | building. |
| 0x130624 | 49 | Second, it's true we're doing work for him, but\n |
| 0x130656 | 33 | that's supposed to be classified. |
| 0x130678 | 42 | Him coming here would be a big red flag.\n |
| 0x1306a3 | 46 | We can't let people know he's connected to us. |
| 0x1306d2 | 48 | Typically, we go to him, whenever he has a new\n |
| 0x130703 | 11 | job for us. |
| 0x13070f | 5 | You-- |
| 0x130715 | 47 | Of course, he does put in appearances here as\n |
| 0x130745 | 41 | Ukon, but I'm not about to tell her that. |
| 0x13076f | 49 | So, no matter how much you may want to see him,\n |
| 0x1307a1 | 34 | you're not going to find him here. |
| 0x1307c4 | 9 | *Grrr...* |
| 0x1307ce | 11 | Haku! HAKU! |
| 0x1307da | 5 | Yeah? |
| 0x1307e0 | 46 | Her Highness may have granted us permission,\n |
| 0x13080f | 43 | but still, to speak to her in such a way... |
| 0x13083b | 46 | ...I guess I see your point, but eh. Whatever. |
| 0x13086a | 8 | H-Haku!? |
| 0x130873 | 48 | Now that she knows she won't find Oshtor here,\n |
| 0x1308a4 | 37 | I doubt we'll see her again anyway... |
| 0x1308ca | 27 | Are you done talking, then? |
| 0x1308e6 | 6 | Urk... |
| 0x1308ed | 46 | Kuon's voice is no different from its usual,\n |
| 0x13091c | 45 | kind tones, but why did I just feel a chill\n |
| 0x13094a | 14 | down my spine? |
| 0x130959 | 32 | Kuon slowly rises behind Anju... |
| 0x13097a | 9 | *Sshf*... |
| 0x130984 | 32 | Eh? What is the meaning of this? |
| 0x1309a5 | 49 | And an all-too-familiar, rope-like length wraps\n |
| 0x1309d7 | 19 | around Anju's head. |
| 0x1309eb | 9 | *Krkk*... |
| 0x1309f5 | 45 | Kuon's tail starts to tighten around Anju's\n |
| 0x130a23 | 11 | forehead... |
| 0x130a2f | 47 | I don't know quite how tight she can make it,\n |
| 0x130a5f | 43 | but I'm definitely starting to hear weird\n |
| 0x130a8b | 7 | sounds. |
| 0x130a93 | 15 | A-Aagh! AAAAA!! |
| 0x130aa3 | 41 | Rulutieh poured her heart and soul into\n |
| 0x130acd | 46 | preparing those snacks you devoured, you know. |
| 0x130afc | 48 | And you washed it all down with the mead I was\n |
| 0x130b2d | 19 | specially saving... |
| 0x130b41 | 43 | You even drank it straight. Such a waste... |
| 0x130b6d | 22 | *Krkk*... *krrrkkk*... |
| 0x130b84 | 41 | A-Ah--Wh-Who do you think I am, knave!?\n |
| 0x130bae | 18 | Unhand me at once! |
| 0x130bc1 | 36 | Just a random city girl, aren't you? |
| 0x130be6 | 50 | Surely the honorable princess of Yamato wouldn't\n |
| 0x130c19 | 45 | go back on her word just because she's in a\n |
| 0x130c47 | 5 | bind. |
| 0x130c4d | 7 | Urgh... |
| 0x130c55 | 48 | And I would certainly think she wouldn't be so\n |
| 0x130c86 | 44 | petty as to use her rank for leverage over\n |
| 0x130cb3 | 9 | others... |
| 0x130cbd | 24 | *Krrkk*... *KRRRKKKK*... |
| 0x130cd6 | 8 | Nnngh... |
| 0x130cdf | 48 | And it's most CERTAINLY my duty as this little\n |
| 0x130d10 | 47 | city girl's elder to scold her when she's out\n |
| 0x130d40 | 8 | of line. |
| 0x130d49 | 42 | What do we say when we've done something\n |
| 0x130d74 | 6 | wrong? |
| 0x130d7b | 10 | *Krrkk*... |
| 0x130d86 | 28 | I... I have... done noth--!! |
| 0x130da3 | 15 | *Krrrrkkkk*.... |
| 0x130db3 | 48 | Ow, ow, ow--I-I am--the scion of--the heavens!\n |
| 0x130de4 | 43 | W-Were I to lie, the very HONOR of Yamato-- |
| 0x130e10 | 19 | *Krrkkk krkk krk*-- |
| 0x130e24 | 22 | What's the magic word? |
| 0x130e3b | 44 | F-for me, there is no retreat, no begging,\n |
| 0x130e68 | 11 | no remorse! |
| 0x130e74 | 9 | Ahahaa... |
| 0x130e7e | 19 | Kuon smiles widely. |
| 0x130e92 | 21 | *Krrkk*... *KRRKKK*-- |
| 0x130ea8 | 43 | She makes fists with both her hands, then\n |
| 0x130ed4 | 42 | places them on either side of Anju's head. |
| 0x130eff | 16 | *Grind, grind--* |
| 0x130f10 | 8 | Gaaahh!! |
| 0x130f19 | 26 | Whaaat's the magic wooord? |
| 0x130f34 | 24 | *Grind, grind, grind*... |
| 0x130f4d | 8 | Hhhhgh-- |
| 0x130f56 | 38 | Stop, stop, stop! That's enough, Kuon. |
| 0x130f7d | 47 | I quickly step in to stop Kuon before she can\n |
| 0x130fad | 19 | squeeze any harder. |
| 0x130fc1 | 48 | I'm pretty sure doing any more could be really\n |
| 0x130ff2 | 4 | bad. |
| 0x130ff7 | 47 | The fact that Anju's head is starting to look\n |
| 0x131027 | 43 | like an hourglass is probably a bad sign... |
| 0x131053 | 7 | Haku... |
| 0x13105b | 39 | Yeah, I think she's learned her lesson. |
| 0x131083 | 5 | Atuy? |
| 0x131089 | 43 | Really, Kuon, it isn't like you to get so\n |
| 0x1310b5 | 36 | worked up over something so trivial. |
| 0x1310da | 43 | Of course she has not learned her lesson.\n |
| 0x131106 | 45 | It is for her own good. Let us see how long\n |
| 0x131134 | 12 | she lasts... |
| 0x131141 | 47 | I think there's someone whispering behind me,\n |
| 0x131171 | 38 | but it's probably just my imagination. |
| 0x131198 | 37 | I do understand how you feel, Kuon... |
| 0x1311be | 25 | Atuy smiles meaningfully. |
| 0x1311d8 | 46 | Hee. I guess I'll take one for the team, then. |
| 0x131207 | 28 | ...What do you mean by that? |
| 0x131224 | 48 | Weeeell, love. It just so happens I'm prepared\n |
| 0x131255 | 29 | for this sort of development! |
| 0x131273 | 44 | She moves toward a shelf and puts her hand\n |
| 0x1312a0 | 32 | against it, beginning to push... |
| 0x1312c1 | 12 | *Grrrnnn...* |
| 0x1312ce | 47 | The entire shelf slides over to one side, and\n |
| 0x1312fe | 38 | behind it--a small hidden compartment! |
| 0x131325 | 46 | Wow. I never knew there was a mechanism like\n |
| 0x131354 | 35 | that, hiding in such plain sight... |
| 0x131378 | 49 | Kuon finally unwraps her tail from Anju's head,\n |
| 0x1313aa | 23 | impressed by the shelf. |
| 0x1313c2 | 45 | To tell the truth, I found it completely by\n |
| 0x1313f0 | 48 | accident, but I've been using it for my secret\n |
| 0x131421 | 6 | stash. |
| 0x131428 | 45 | Just as she reaches inside the compartment,\n |
| 0x131456 | 19 | however, she stops. |
| 0x13146a | 3 | Eh? |
| 0x13146e | 48 | What's going on here? Where's my special stash\n |
| 0x13149f | 10 | of drinks? |
| 0x1314aa | 8 | Special? |
| 0x1314b3 | 47 | That's so strange. I had some expensive stuff\n |
| 0x1314e3 | 15 | in here, too... |
| 0x1314f3 | 30 | Where is it? Where did it go!? |
| 0x131512 | 44 | Haku? You look a little pale. Is something\n |
| 0x13153f | 25 | I-It's, uh. It's nothing. |
| 0x131559 | 17 | It's not nothing. |
| 0x13156b | 49 | A while back, the other guys and I got together\n |
| 0x13159d | 42 | for drinks at home base, but we ended up\n |
| 0x1315c8 | 12 | running out. |
| 0x1315d5 | 49 | We were looking around, trying to find at least\n |
| 0x131607 | 48 | one spare bottle, when I tripped and moved the\n |
| 0x131638 | 8 | shelf... |
| 0x131641 | 18 | Gah!? What's this? |
| 0x131654 | 48 | Oh ho! Mine eyes doth behold a trove of finest\n |
| 0x131685 | 47 | libations--and how their siren song tempteth... |
| 0x1316b5 | 46 | Well, would you look at that. We could start\n |
| 0x1316e4 | 36 | all over and still have drinks left. |
| 0x131709 | 44 | I don't know. Who does this all belong to,\n |
| 0x131736 | 10 | anyway...? |
| 0x131741 | 49 | Don't be such a stiff, Kiwru. It's in our base,\n |
| 0x131773 | 32 | so it's ours to drink, isn't it? |
| 0x131794 | 39 | Bwahaha! I like the way you think, kid. |
| 0x1317bc | 46 | Gentle lords, I believe we have arrived at a\n |
| 0x1317eb | 46 | concord most splendid. Let us unto our revels! |
| 0x13181a | 49 | And so we ended up drinking all of it. We never\n |
| 0x13184c | 39 | replaced the bottles we took, either... |
| 0x131874 | 46 | The only other one in the room who knows the\n |
| 0x1318a3 | 44 | truth is Kiwru. I look over to him quickly-- |
| 0x1318d0 | 49 | He looks back to me, trying to mouth something.\n |
| 0x131902 | 47 | His hands are on his stomach like he's in pain. |
| 0x131932 | 44 | Yeah. The best plan would be to pretend we\n |
| 0x13195f | 20 | don't know anything. |
| 0x13197a | 46 | It looks like Kiwru is desperately trying to\n |
| 0x1319a9 | 48 | communicate something to me, but I pretend not\n |
| 0x1319da | 10 | to notice. |
| 0x1319e5 | 29 | We have to stay quiet, Kiwru. |
| 0x131a03 | 47 | Atuy and Kuon, meanwhile--having no idea what\n |
| 0x131a33 | 40 | we did--turn to the most likely culprit. |
| 0x131a5c | 48 | ...N-Now, hold! I'm innocent of whatever crime\n |
| 0x131a8d | 5 | you-- |
| 0x131a93 | 12 | *Krrrkkk*... |
| 0x131aa0 | 43 | And Kuon's tail, of course, finds its way\n |
| 0x131acc | 30 | around Anju's head once again. |
| 0x131aeb | 7 | Hurgh-- |
| 0x131af3 | 46 | A proper ruler must learn not to take things\n |
| 0x131b22 | 31 | that aren't hers, I think, hmm? |
| 0x131b42 | 21 | *Krrkk*, *krrkkkk*... |
| 0x131b58 | 50 | Owowow--th-this is all a great misunderstanding,\n |
| 0x131b8b | 26 | please! I had no idea of-- |
| 0x131ba6 | 13 | *Krrrkkkk*... |
| 0x131bb4 | 43 | This is starting to eat at my conscience.\n |
| 0x131be0 | 47 | At this rate, things could quickly get out of\n |
| 0x131c10 | 7 | hand... |
| 0x131c18 | 35 | Uh, Kuon? I don't think she meant\n |
| 0x131c3c | 29 | any harm. She's just a kid... |
| 0x131c5a | 31 | *Krrrkkkk... krkk*, *krrkkk*... |
| 0x131c7a | 38 | She's not listening to a word I say.\n |
| 0x131ca1 | 6 | Great. |
| 0x131ca8 | 45 | Now is the time to dethrone this foul tyrant! |
| 0x131cd6 | 48 | Suddenly, Atuy produces her spear and puts the\n |
| 0x131d07 | 25 | blade against Anju's ear! |
| 0x131d21 | 45 | H-Hold it! Just hold it, would you? This is\n |
| 0x131d4f | 26 | spiraling out of control-- |
| 0x131d6a | 15 | Evil shall pay! |
| 0x131d7a | 49 | Before I can stop her, she drags her nails down\n |
| 0x131dac | 45 | the spear's blade, giving a chalkboard-like\n |
| 0x131dda | 8 | screech. |
| 0x131de3 | 12 | EEEEEEEEEE-- |
| 0x131df0 | 8 | GYAAAH!! |
| 0x131df9 | 13 | --EEEEEEEEE-- |
| 0x131e07 | 18 | My ears! My ears!! |
| 0x131e1a | 47 | The hellish punishment only continues, until... |
| 0x131e4a | 46 | Anju is left limp on the ground, her will to\n |
| 0x131e79 | 23 | fight completely spent. |
| 0x131e91 | 34 | I hope you've learned your lesson. |
| 0x131eb4 | 48 | Kuon slowly begins to loosen her tail's grasp... |
| 0x131ee5 | 47 | Y-Yes, yes. I'll apologize. I'll a-apologize,\n |
| 0x131f15 | 22 | so please, release me! |
| 0x131f2c | 33 | I can let you go then, I suppose. |
| 0x131f4e | 48 | Kuon finally relents, letting go of Anju's head. |
| 0x131f7f | 7 | Ungh... |
| 0x131f87 | 47 | Anju crumbles, holding her aching head, tears\n |
| 0x131fb7 | 22 | brewing in her eyes... |
| 0x131fce | 41 | Then, in a flash, she bolts for the door. |
| 0x131ff8 | 46 | As if I would ever apologize to the likes of\n |
| 0x132027 | 48 | you, cretin! Drunkard! I bet you'll never find\n |
| 0x132058 | 10 | a husband! |
| 0x132063 | 7 | *NYOOM* |
| 0x13206b | 45 | Ah, well. There she goes. I'll just have to\n |
| 0x132099 | 42 | dole out more punishment if she turns up\n |
| 0x1320c4 | 6 | again. |
| 0x1320cb | 45 | Wh-What have we done... to Her H-Highness...? |
| 0x1320f9 | 45 | Kiwru mutters to himself with lifeless eyes\n |
| 0x132127 | 41 | as he watches the whole ordeal transpire. |
| 0x132151 | 34 | I-If word of this ever gets out... |
| 0x132174 | 49 | No need to worry. She's just a plain city girl,\n |
| 0x1321a6 | 9 | remember? |
| 0x1321b0 | 39 | I made EXTRA sure she'll remember that. |
| 0x1321d8 | 19 | Kuon smiles smugly. |
| 0x1321ec | 38 | So that's why she said it like that... |
| 0x132213 | 34 | Impressive as always, dear sister. |
| 0x132236 | 41 | Nekone seems much more upbeat than usual. |
| 0x132260 | 42 | Hee hee. Well, if she's just a commoner,\n |
| 0x13228b | 43 | there's no harm in teaching her a lesson,\n |
| 0x1322b7 | 8 | I guess. |
| 0x1322c0 | 45 | If I recall correctly, I'm fairly sure Atuy\n |
| 0x1322ee | 33 | was trying to prevent all this... |
| 0x132310 | 21 | Urgh... My stomach... |
| 0x132326 | 39 | ...I'm keeping this secret to my grave. |
| 0x1350d6 | 22 | Uuaahh... so sleepy... |
| 0x1350ed | 49 | Kuon found me napping when I was supposed to be\n |
| 0x13511f | 42 | doing accounting work, so she sent me on\n |
| 0x13514a | 8 | errands. |
| 0x135153 | 49 | Rulutieh is sewing and the others are all busy,\n |
| 0x135185 | 42 | so I'm the only one available to go out... |
| 0x1351b0 | 46 | I was under the impression Kiwru is supposed\n |
| 0x1351df | 46 | to do these random errands. Why is it always\n |
| 0x13520e | 3 | me? |
| 0x135212 | 47 | And Atuy tottered off on her own, claiming to\n |
| 0x135242 | 34 | be patrolling the city, of course. |
| 0x135265 | 46 | Urf. I'm pretty sure that's everything taken\n |
| 0x135294 | 10 | care of... |
| 0x13529f | 45 | As I walk, I double-check the list of tasks\n |
| 0x1352cd | 13 | Kuon gave me. |
| 0x1352db | 17 | Yeah, looks good. |
| 0x1352ed | 40 | This took a lot longer than I thought.\n |
| 0x135316 | 17 | Better head back. |
| 0x135328 | 47 | Don't want Kuon to think I'm slacking off, or\n |
| 0x135358 | 37 | else she'll cut my allowance again... |
| 0x13537e | 44 | I can't really talk back when I owe her so\n |
| 0x1353ab | 43 | much, but man, who does she think she is,\n |
| 0x1353d7 | 10 | my mother? |
| 0x1353e2 | 3 | Hm? |
| 0x1353e6 | 47 | Halfway back to the Hakurokaku Inn, I stop as\n |
| 0x135416 | 44 | a tantalizing smell steals across my nose... |
| 0x135443 | 33 | This fragrant smell of sauce...\n |
| 0x135465 | 34 | It must be from a kokoromo skewer. |
| 0x135488 | 45 | Kokoromo dishes use the meat of a packbeast\n |
| 0x1354b6 | 44 | that's usually slaughtered for fur and bone. |
| 0x1354e3 | 48 | It has a pungent scent and tends to be sinewy,\n |
| 0x135514 | 46 | but when prepared well, it's a flavorful meal. |
| 0x135543 | 11 | *Grrmbl*... |
| 0x13554f | 43 | The smell the cooking skewers give off is\n |
| 0x13557b | 27 | almost criminally tempting. |
| 0x135597 | 46 | I take out my wallet and check it carefully... |
| 0x1355c6 | 43 | I should have enough for a skewer or two.\n |
| 0x1355f2 | 46 | It'll be a while until dinner, so a snack is\n |
| 0x135621 | 11 | in order... |
| 0x13562d | 11 | Man's voice |
| 0x135639 | 42 | Look, missy, that ain't gonna fly with me. |
| 0x135664 | 48 | As I follow my nose to the stall, an agitated,\n |
| 0x135695 | 37 | confused voice fades into my hearing. |
| 0x1356bb | 30 | What, pray tell, will not fly? |
| 0x1356da | 3 | Eh? |
| 0x1356de | 42 | Give it a rest, already! I'm a busy man,\n |
| 0x135709 | 7 | y'know! |
| 0x135711 | 43 | Ah, in that case, pay me no mind. You may\n |
| 0x13573d | 33 | continue your work uninterrupted. |
| 0x13575f | 46 | It is, after all, my duty as a ruler to mind\n |
| 0x13578e | 34 | the will and comfort of my people. |
| 0x1357b1 | 46 | Look, missy, will you quit spouting nonsense\n |
| 0x1357e0 | 41 | and pay up for what you've eaten already? |
| 0x13580a | 45 | It is you who spouts nonsense, sir. What is\n |
| 0x135838 | 27 | this "pay up" you speak of? |
| 0x135854 | 46 | You ate my skewers, yeah? A whole damn bunch\n |
| 0x135883 | 7 | of 'em? |
| 0x13588b | 47 | Indeed. I must say, your flavoring techniques\n |
| 0x1358bb | 42 | are crude, but it was a satisfying meal.\n |
| 0x1358e6 | 15 | My compliments. |
| 0x1358f6 | 46 | So now comes the part where you pay for what\n |
| 0x135925 | 8 | you ate. |
| 0x13592e | 7 | ...Pay? |
| 0x135936 | 45 | Aaaargh! Would somebody please do something\n |
| 0x135964 | 11 | about this? |
| 0x135970 | 43 | The deeper voice must be the meat vendor.\n |
| 0x13599c | 47 | And I have a sinking feeling I know the other\n |
| 0x1359cc | 6 | one... |
| 0x1359d3 | 43 | I really want to know what the hell she's\n |
| 0x1359ff | 48 | doing here. I've got a bad feeling about this... |
| 0x135a30 | 44 | ...I'm gonna pretend I didn't hear anything. |
| 0x135a5d | 46 | I better get away from here before she ropes\n |
| 0x135a8c | 9 | me into-- |
| 0x135a96 | 18 | Hm? Ah, you there. |
| 0x135aa9 | 7 | Urgh... |
| 0x135ab1 | 20 | Crap, she noticed... |
| 0x135ac6 | 35 | Oshtor's servant boy, aren't you?\n |
| 0x135aea | 9 | Well met. |
| 0x135af4 | 34 | What exactly are you doing here?\n |
| 0x135b17 | 47 | And hey, wh-who are you calling "servant boy!?" |
| 0x135b47 | 38 | Your name was... Saku? Or was it Deku? |
| 0x135b6e | 10 | It's Haku. |
| 0x135b79 | 14 | Ah, yes. Yaku. |
| 0x135b88 | 12 | I said Haku! |
| 0x135b95 | 3 | Man |
| 0x135b99 | 29 | Hey, you. You know this girl? |
| 0x135bb7 | 49 | Huh? I-I--in the technical sense, I guess, sure-- |
| 0x135be9 | 31 | Then knock some sense into her! |
| 0x135c09 | 47 | This girl's eaten a whole mess of skewers and\n |
| 0x135c39 | 41 | she's tryin' to get outta paying for 'em. |
| 0x135c63 | 42 | I'm runnin' a business, here! I can't go\n |
| 0x135c8e | 41 | giving out free meals. I gotta eat too,\n |
| 0x135cb8 | 9 | you know. |
| 0x135cc2 | 47 | I look at Anju's feet to find an astronomical\n |
| 0x135cf2 | 43 | number of skewers scattered on the cobbles. |
| 0x135d1e | 29 | Just how much DID she eat...? |
| 0x135d3c | 4 | Hey. |
| 0x135d41 | 11 | What is it? |
| 0x135d4d | 49 | Those skewers on the ground. Are those all from\n |
| 0x135d7f | 13 | what you ate? |
| 0x135d8d | 41 | Indeed. I was finally able to escape my\n |
| 0x135db7 | 44 | chambers again, so I decided to wander the\n |
| 0x135de4 | 8 | capital. |
| 0x135ded | 49 | And as I walked past this place, I found myself\n |
| 0x135e1f | 39 | enchanted by these skewers' arresting\n |
| 0x135e47 | 10 | fragrance. |
| 0x135e52 | 50 | I could hardly help myself when this kind vendor\n |
| 0x135e85 | 47 | presented me with what he was cooking, you see. |
| 0x135eb5 | 50 | It would have been rude to reject such an offer,\n |
| 0x135ee8 | 43 | and now he refuses to cease talking about\n |
| 0x135f14 | 9 | "paying." |
| 0x135f1e | 13 | Is this true? |
| 0x135f2c | 36 | Well, she kept lookin' over, yeah?\n |
| 0x135f51 | 33 | So I asked her if she'd like one. |
| 0x135f73 | 46 | She ate the thing in an instant and demanded\n |
| 0x135fa2 | 5 | more. |
| 0x135fa8 | 47 | I asked if she could pay, and she said not to\n |
| 0x135fd8 | 8 | worry... |
| 0x135fe1 | 48 | And then the moment she's done, she says she's\n |
| 0x136012 | 47 | got no idea what I'm talkin' about. You get me? |
| 0x136042 | 46 | All right, I think I understand what's going\n |
| 0x136071 | 8 | on here. |
| 0x13607a | 37 | Hey, Anju. Do you know what money is? |
| 0x1360a0 | 17 | No, what is that? |
| 0x1360b2 | 26 | Ever hear the words, uh.\n |
| 0x1360cd | 27 | "Accounting?" Or "payment?" |
| 0x1360e9 | 46 | Your speech is foreign to me. For your sake,\n |
| 0x136118 | 48 | I hope you aren't trying to make a fool of me... |
| 0x136149 | 48 | Looks like this princess is so secluded and of\n |
| 0x13617a | 48 | such high station, nobody's told her how money\n |
| 0x1361ab | 6 | works. |
| 0x1361b2 | 16 | Well, you see... |
| 0x1361c3 | 46 | With that in mind, I begin to explain to her\n |
| 0x1361f2 | 45 | the concept of paying for goods and services. |
| 0x136220 | 47 | I see. So this man is requesting a reward for\n |
| 0x136250 | 23 | entertaining me, is he? |
| 0x136268 | 34 | That's not quite--you know what?\n |
| 0x13628b | 46 | Yes. Yes, that's exactly what he's asking for. |
| 0x1362ba | 46 | Hm. I suppose I understand, but ordinarily I\n |
| 0x1362e9 | 47 | only reward those of the highest distinction... |
| 0x136319 | 45 | Ah, no matter. It is quite true that you've\n |
| 0x136347 | 44 | entertained me, sir. I'll consider this an\n |
| 0x136374 | 10 | exception. |
| 0x13637f | 43 | Anju reaches into her pockets to withdraw\n |
| 0x1363ab | 12 | something... |
| 0x1363b8 | 7 | Whoa... |
| 0x1363c0 | 42 | She holds up a glittering gold necklace,\n |
| 0x1363eb | 43 | studded with gems. Even a layman can tell\n |
| 0x136417 | 12 | its value... |
| 0x136424 | 19 | Hm, this should do. |
| 0x13643c | 43 | Why are you just standing there? I cannot\n |
| 0x136468 | 44 | present you with your reward if you do not\n |
| 0x136495 | 6 | kneel. |
| 0x13649c | 41 | Wh--I-I can't accept something like that! |
| 0x1364c6 | 17 | Yeah, thought so. |
| 0x1364d8 | 45 | Even at a glance, I can tell it's artisanal\n |
| 0x136506 | 41 | work. It'd fetch an extremely high price. |
| 0x136530 | 44 | No matter how many skewers you scarf down,\n |
| 0x13655d | 46 | it'd never match the amount of money this is\n |
| 0x13658c | 6 | worth. |
| 0x136593 | 40 | And to accept it as payment for such a\n |
| 0x1365bc | 19 | mundane service...? |
| 0x1365d0 | 38 | Anyone would be looking for the catch. |
| 0x1365f7 | 47 | It's not difficult to imagine heads literally\n |
| 0x136627 | 46 | rolling over this necklace, if it's the real\n |
| 0x136656 | 5 | deal. |
| 0x13665c | 47 | Only someone with a lot of guts or a complete\n |
| 0x13668c | 46 | lack of sense would accept, in this vendor's\n |
| 0x1366bb | 9 | position. |
| 0x1366c5 | 44 | He seems to realize as much, sizing up the\n |
| 0x1366f2 | 31 | unusual girl in front of him... |
| 0x136712 | 40 | He leans toward me and whispers quietly. |
| 0x13673b | 42 | Hey, buddy. You said you know this girl?\n |
| 0x136766 | 19 | Who exactly is she? |
| 0x13677a | 41 | No idea. Probably some rich family's kid. |
| 0x1367a4 | 34 | Whatever. How much you got on you? |
| 0x1367c7 | 49 | Huh? I don't have nearly enough to pay for what\n |
| 0x1367f9 | 10 | she--HEY!? |
| 0x136804 | 47 | I pull out my wallet to check, and the vendor\n |
| 0x136834 | 46 | immediately snatches it and helps himself to\n |
| 0x136863 | 13 | its contents. |
| 0x136871 | 44 | One, two, three... eh, not exactly enough,\n |
| 0x13689e | 47 | but it'll do. Pleasure doin' business with you. |
| 0x1368ce | 46 | He shoves my wallet back into my hands, empty. |
| 0x1368fd | 23 | Hold on just a minute-- |
| 0x136915 | 47 | Come on over, folks! Step right up for cheap,\n |
| 0x136945 | 19 | delicious kokoromo! |
| 0x136959 | 48 | The vendor pretends not to hear me, going back\n |
| 0x13698a | 46 | to shouting at potential customers passing by. |
| 0x1369b9 | 46 | Damn it all! My allowance... How did it come\n |
| 0x1369e8 | 8 | to this? |
| 0x1369f1 | 30 | Well, where are we going next? |
| 0x136a10 | 44 | WE'RE not going anywhere. I'M going home--\n |
| 0x136a3d | 36 | and why are you still following me!? |
| 0x136a62 | 44 | I have arrived at the conclusion that your\n |
| 0x136a8f | 41 | company provides great amusement to me,\n |
| 0x136ab9 | 10 | of course. |
| 0x136ac4 | 45 | Now that you've mentioned it, visiting your\n |
| 0x136af2 | 44 | "base" may produce more of those delicious\n |
| 0x136b1f | 9 | snacks... |
| 0x136b29 | 46 | Seems you've already forgotten what happened\n |
| 0x136b58 | 23 | to you there last time. |
| 0x136b70 | 44 | Ah, but now I'm reminded. Those delicacies\n |
| 0x136b9d | 47 | I sampled on my previous visit, what are they\n |
| 0x136bcd | 7 | called? |
| 0x136bd5 | 44 | I had never eaten, nor even laid eyes upon\n |
| 0x136c02 | 29 | such magnificent food before. |
| 0x136c20 | 46 | I attempted to describe them to my cook, but\n |
| 0x136c4f | 38 | she assured me no such things exist!\n |
| 0x136c76 | 13 | Preposterous. |
| 0x136c84 | 51 | Oh, that stuff was a recreation of something I...\n |
| 0x136cb8 | 17 | sort of remember? |
| 0x136cca | 43 | I'm pretty sure it can't be found in this\n |
| 0x136cf6 | 44 | country, anyway. I wouldn't blame your cook. |
| 0x136d23 | 40 | Ah, is that so? I'm relieved to hear it. |
| 0x136d4c | 9 | Relieved? |
| 0x136d56 | 46 | The imperial cook is considered the greatest\n |
| 0x136d85 | 44 | paragon of her craft in all Yamato, you see. |
| 0x136db2 | 44 | That there might have been a dish she knew\n |
| 0x136ddf | 40 | nothing of came as quite a shock to her. |
| 0x136e08 | 48 | Apparently she felt so ashamed, she offered to\n |
| 0x136e39 | 39 | take her own life to reclaim her honor. |
| 0x136e61 | 45 | I managed to convince her otherwise, but it\n |
| 0x136e8f | 31 | continues to perturb her daily. |
| 0x136eaf | 21 | Wh--Yikes. Holy shit. |
| 0x136ec5 | 47 | In any event, I have a wonderful proposal for\n |
| 0x136ef5 | 44 | you. You shall guide me around the capital\n |
| 0x136f22 | 9 | this eve! |
| 0x136f2c | 43 | What? No. I'm going home, and so are you,\n |
| 0x136f58 | 11 | understand? |
| 0x136f64 | 46 | I go through all the trouble of escaping the\n |
| 0x136f93 | 41 | palace, and you would send me back? How\n |
| 0x136fbd | 10 | heartless. |
| 0x136fc8 | 47 | Look, consider your own position. Do you have\n |
| 0x136ff8 | 48 | any idea how much trouble you're causing right\n |
| 0x137029 | 4 | now? |
| 0x13702e | 45 | I admit you have a point, but I remind you:\n |
| 0x13705c | 47 | I am the heir to the Mikado, and will one day\n |
| 0x13708c | 8 | inherit. |
| 0x137095 | 49 | If I am to rule with any kind of wisdom, I must\n |
| 0x1370c7 | 47 | observe my people living their lives firsthand. |
| 0x1370f7 | 42 | That is why I venture out into the city.\n |
| 0x137122 | 41 | To witness for myself the people I must\n |
| 0x13714c | 15 | one day govern. |
| 0x13715c | 48 | I see. So you're actually thinking of Yamato's\n |
| 0x13718d | 9 | people... |
| 0x137197 | 45 | Of course. What kind of fool do you take me\n |
| 0x1371c5 | 4 | for? |
| 0x1371ca | 47 | You expect me to buy that story? It's obvious\n |
| 0x1371fa | 45 | you just want to sneak out and have some fun. |
| 0x137228 | 45 | You DARE level such false accusations at me!? |
| 0x137256 | 16 | Yeah, I figured. |
| 0x137267 | 34 | Y-You have no proof of such wild-- |
| 0x13728a | 49 | Why don't you try looking at me? That's a habit\n |
| 0x1372bc | 47 | you'll have to fix if you want me to buy your\n |
| 0x1372ec | 4 | lie. |
| 0x1372f1 | 48 | I AM looking at you. Wh-What habit is this you\n |
| 0x137322 | 9 | speak of? |
| 0x13732c | 40 | She's still playing dumb after all this? |
| 0x137355 | 44 | M-More importantly, you will obey at once!\n |
| 0x137382 | 43 | Guide me around the capital. The princess\n |
| 0x1373ae | 12 | commands it. |
| 0x1373bb | 21 | Hold on a minu--bwuh! |
| 0x1373d1 | 42 | How is she this strong? I can't stop her-- |
| 0x1373fc | 15 | *Drag, drag*... |
| 0x13740c | 31 | L-Let go of me! I said let go-- |
| 0x13742c | 42 | Tell me, what is that there? What is its\n |
| 0x137457 | 8 | purpose? |
| 0x137460 | 38 | Why does it always end up like this... |
| 0x137487 | 29 | That? Oh, that's a show-tent. |
| 0x1374a5 | 12 | A show-tent? |
| 0x1374b2 | 44 | You've never heard of them? They're public\n |
| 0x1374df | 29 | places for people to perform. |
| 0x1374fd | 39 | I see. Similar to the Imperial Theater. |
| 0x137525 | 48 | They do occasionally put on plays, yes, but...\n |
| 0x137556 | 48 | it looks like today they're showing off a rare\n |
| 0x137587 | 7 | animal. |
| 0x13758f | 40 | Oh? My interest is piqued. Let us enter. |
| 0x1375b8 | 14 | Not happening. |
| 0x1375c7 | 13 | Why is that!? |
| 0x1375d5 | 47 | My wallet's completely empty. I can't pay for\n |
| 0x137605 | 42 | it. Remember my explanation about payment? |
| 0x137630 | 28 | Tch. Would this not suffice? |
| 0x13764d | 33 | Anju produces the necklace again. |
| 0x13766f | 21 | No, not that, please. |
| 0x137685 | 34 | Ah, what a lively place THIS is!\n |
| 0x1376a8 | 44 | So many different kinds of fruits, sweets... |
| 0x1376d5 | 44 | This is the place that keeps the capital's\n |
| 0x137702 | 25 | kitchens full, basically. |
| 0x13771c | 45 | I would expect no less from Yamato. This is\n |
| 0x13774a | 46 | unequivocally the best selection in the world. |
| 0x137779 | 41 | Anju makes the proclamation proudly and\n |
| 0x1377a3 | 30 | excitedly as she looks around. |
| 0x1377c2 | 44 | She sniffs the air as though picking out a\n |
| 0x1377ef | 48 | particular scent, then turns in one direction... |
| 0x137820 | 19 | *Sizzle, sizzle*... |
| 0x137834 | 45 | You've got to be kidding. She just ate a ton. |
| 0x137862 | 49 | Ah, it seems they rotate the meat as they roast\n |
| 0x137894 | 10 | it, there. |
| 0x13789f | 20 | Yeah, seems like it. |
| 0x1378b4 | 46 | Damn, but that smells good. Now I'M starting\n |
| 0x1378e3 | 14 | to get hungry. |
| 0x1378f2 | 46 | Its scent differs from the skewers I sampled\n |
| 0x137921 | 13 | previously... |
| 0x13792f | 14 | Seems like it. |
| 0x13793e | 41 | So it is different from the dish called\n |
| 0x137968 | 9 | kokoromo? |
| 0x137972 | 49 | With that, you shave off the meat that's cooked\n |
| 0x1379a4 | 48 | and wrap it in amam. It's pretty common around\n |
| 0x1379d5 | 5 | here. |
| 0x1379db | 45 | What are you talking about? I've never seen\n |
| 0x137a09 | 45 | such a dish. It's eaten directly from one's\n |
| 0x137a37 | 13 | hands, I see? |
| 0x137a45 | 43 | She's never seen it before? Are the meals\n |
| 0x137a71 | 42 | prepared for the court so different from\n |
| 0x137a9c | 16 | commoners' food? |
| 0x137aad | 45 | And what of that one? The one adjacent to it? |
| 0x137adb | 46 | That's cooked karakatsua. It's cooked whole.\n |
| 0x137b0a | 48 | I doubt it's really up to your refined tastes... |
| 0x137b3b | 21 | *Grumble, grumble*... |
| 0x137b51 | 11 | Would you-- |
| 0x137b5d | 41 | No money, remember? I'm completely broke. |
| 0x137b87 | 35 | Would you quit flashing that thing? |
| 0x137bab | 47 | And so, Anju drags me all around the capital... |
| 0x137bdb | 50 | At long last, we reach the edge of the capital--\n |
| 0x137c0e | 47 | the city gates. The sunset has turned the sky\n |
| 0x137c3e | 4 | red. |
| 0x137c43 | 49 | It's this late already? We must've spent a wh--\n |
| 0x137c75 | 47 | aw, crap. I forgot I'm supposed to be running\n |
| 0x137ca5 | 48 | I'm getting a headache just thinking about the\n |
| 0x137cd6 | 39 | telling-off Kuon is going to give me... |
| 0x137cfe | 47 | ...but I guess my first problem is what to do\n |
| 0x137d2e | 18 | with the princess. |
| 0x137d41 | 49 | I'm sure she's already caused some alarm in the\n |
| 0x137d73 | 43 | court, and the last thing I want to do is\n |
| 0x137d9f | 12 | escalate it. |
| 0x137dac | 46 | I'm the one being dragged around, but that's\n |
| 0x137ddb | 41 | not what it's going to look like if I'm\n |
| 0x137e05 | 16 | caught up in it. |
| 0x137e16 | 13 | Over there... |
| 0x137e24 | 29 | What lies beyond those gates? |
| 0x137e42 | 42 | Beyond the...? A lot of things, I guess.\n |
| 0x137e6d | 47 | Mountains, rivers, plains, other countries...\n |
| 0x137e9d | 10 | the ocean. |
| 0x137ea8 | 12 | The ocean... |
| 0x137eb5 | 48 | I'm told the water stretches as far as the eye\n |
| 0x137ee6 | 42 | can see. I wonder how far it truly goes... |
| 0x137f11 | 21 | You've never seen it? |
| 0x137f27 | 47 | I have... never been beyond the bounds of the\n |
| 0x137f57 | 17 | imperial capital. |
| 0x137f69 | 43 | I've not the slightest idea of what other\n |
| 0x137f95 | 38 | countries are like, let alone the sea. |
| 0x137fbc | 9 | ...I see. |
| 0x137fc6 | 48 | I knew she was brought up sheltered, but I had\n |
| 0x137ff7 | 28 | no idea it was this extreme. |
| 0x138014 | 40 | No wonder she wants to leave her cage.\n |
| 0x13803d | 47 | I guess her line about the people of the city\n |
| 0x13806d | 15 | wasn't a lie... |
| 0x13807d | 47 | 'Course, it still sucks that I got roped into\n |
| 0x1380ad | 9 | all this. |
| 0x1380b7 | 44 | My knowledge of the outside world consists\n |
| 0x1380e4 | 46 | only of what my studies and Oshtor's stories\n |
| 0x138113 | 8 | tell me. |
| 0x13811c | 7 | Oshtor? |
| 0x138124 | 48 | Her voice, full of loneliness, brightens a bit\n |
| 0x138155 | 27 | at the mention of his name. |
| 0x138171 | 48 | Indeed. Oshtor has shared with me a great many\n |
| 0x1381a2 | 7 | things. |
| 0x1381aa | 38 | How beautiful the views outside are... |
| 0x1381d1 | 38 | How the people of this country live... |
| 0x1381f8 | 48 | The strange and varied creatures of the wilds... |
| 0x138229 | 6 | ...Hm? |
| 0x138230 | 45 | Anju's eyes begin to fill with tears as she\n |
| 0x13825e | 20 | casts them downward. |
| 0x138273 | 35 | ...He used to tell me... so much... |
| 0x138297 | 41 | Damn it, Oshtor, look what you've done.\n |
| 0x1382c1 | 48 | You make her sad by leaving her alone, and now\n |
| 0x1382f2 | 13 | I pay for it? |
| 0x138300 | 46 | You there, young man. How dare you make such\n |
| 0x13832f | 17 | a young girl cry? |
| 0x138341 | 49 | Hey, hold up. I'm not the one who made her cr--\n |
| 0x138373 | 4 | Huh? |
| 0x138378 | 50 | I glance behind me to find that old candy vendor\n |
| 0x1383ab | 34 | from before glaring daggers at me. |
| 0x1383ce | 19 | The candy vendor... |
| 0x1383e2 | 7 | Old man |
| 0x1383ea | 50 | Look who it is. Not only were you dragging those\n |
| 0x13841d | 47 | girls around last time, now you're making one\n |
| 0x13844d | 4 | cry? |
| 0x138452 | 45 | I told you, I'm not the one who made her cry. |
| 0x138480 | 48 | Bah. That she's saddened in your company makes\n |
| 0x1384b1 | 24 | you just as guilty, boy. |
| 0x1384ca | 21 | Hey, that's not fair. |
| 0x1384e0 | 45 | You're as hopeless as ever. Here--buy this.\n |
| 0x13850e | 35 | A sweet ought to help cheer her up. |
| 0x138532 | 44 | Sorry, but I actually don't have any money\n |
| 0x13855f | 12 | right now... |
| 0x13856c | 45 | Not only do you make a girl cry, but you're\n |
| 0x13859a | 29 | completely useless? Pathetic. |
| 0x1385b8 | 7 | Nngh... |
| 0x1385c0 | 45 | I can't really argue with him, but what did\n |
| 0x1385ee | 24 | I do to deserve this...? |
| 0x138607 | 49 | Here, girl. Take this. I don't know what's made\n |
| 0x138639 | 44 | you so sad, but I hope this helps your mood. |
| 0x138666 | 6 | Candy! |
| 0x13866d | 47 | Anju's face immediately brightens as she sees\n |
| 0x13869d | 46 | the candy the old man hands her, wagging her\n |
| 0x1386cc | 5 | tail. |
| 0x1386d2 | 48 | But this is so beautiful! I've never seen such\n |
| 0x138703 | 32 | craftsmanship in a candy before. |
| 0x138724 | 49 | Hohoho, you flatter me! And every word is true,\n |
| 0x138756 | 49 | The old vendor gives me a smirk, as if gloating\n |
| 0x138788 | 17 | over his victory. |
| 0x13879a | 46 | Gh... I can't put my finger on why, but he's\n |
| 0x1387c9 | 24 | starting to piss me off. |
| 0x1387e2 | 44 | Hm? You want one too, boy? Well, since you\n |
| 0x13880f | 22 | asked so nicely--here! |
| 0x138826 | 38 | The old man tosses something my way,\n |
| 0x13884d | 27 | and I catch it reflexively. |
| 0x138869 | 24 | This gigiri thing again. |
| 0x138882 | 45 | It's starting to get darker, so I decide to\n |
| 0x1388b0 | 26 | walk Anju to the palace... |
| 0x1388cb | 40 | Hey, about what you were saying earlier. |
| 0x1388f4 | 11 | You mean... |
| 0x138900 | 13 | About Oshtor. |
| 0x13890e | 3 | Oh. |
| 0x138912 | 48 | He's been kept pretty busy, lately. I mean, he\n |
| 0x138943 | 44 | even hired a nobody like me to help him out. |
| 0x138970 | 47 | 'Course, I don't think it's gonna be this bad\n |
| 0x1389a0 | 44 | forever. He'll be able to tell you stories\n |
| 0x1389cd | 11 | again soon. |
| 0x1389d9 | 26 | Do you... really think so? |
| 0x1389f4 | 45 | Yeah, I do. So try not to worry about it so\n |
| 0x138a22 | 16 | much, all right? |
| 0x138a33 | 48 | I doubt he'd distance himself from her without\n |
| 0x138a64 | 34 | good reason. Something must be up. |
| 0x138a87 | 35 | I see... Yes, you are surely right! |
| 0x138aab | 47 | When the time comes, why don't you ask Oshtor\n |
| 0x138adb | 30 | to take you outside the walls? |
| 0x138afa | 45 | You can tell him it's punishment for making\n |
| 0x138b28 | 18 | you worry so much. |
| 0x138b3b | 46 | Ah, of course... I hadn't thought of framing\n |
| 0x138b6a | 13 | it like that. |
| 0x138b78 | 41 | Geez, why am I the one telling her this\n |
| 0x138ba2 | 9 | stuff...? |
| 0x138bac | 44 | ...Incidentally, are you going to eat that\n |
| 0x138bd9 | 6 | candy? |
| 0x138be0 | 46 | Anju's eyes linger on the gigiri candy in my\n |
| 0x138c0f | 5 | hand. |
| 0x138c15 | 44 | N-Nah, I don't really have much of a sweet\n |
| 0x138c42 | 19 | tooth. You want it? |
| 0x138c56 | 45 | May I? Ah, this one is crafted beautifully,\n |
| 0x138c84 | 16 | as well... Mmff. |
| 0x138c95 | 47 | The sight of a young child sucking on what by\n |
| 0x138cc5 | 47 | all appearances is an insect is nothing short\n |
| 0x138cf5 | 9 | of gross. |
| 0x138cff | 43 | Urgh... I'm getting chills down my spine... |
| 0x138d2b | 40 | Mm! This one is quite delicious as well. |
| 0x138d54 | 20 | G-Glad to hear it... |
| 0x138d69 | 29 | This was... quite delightful. |
| 0x138d87 | 49 | Tell me, have you any aspirations of serving me\n |
| 0x138db9 | 9 | directly? |
| 0x138dc3 | 43 | I find myself taken with your brazenness.\n |
| 0x138def | 44 | You know who I am, yet show no fear of me... |
| 0x138e1c | 40 | All the courtiers in the palace are so\n |
| 0x138e45 | 48 | inflexible. I find myself suffocating in their\n |
| 0x138e76 | 10 | company... |
| 0x138e81 | 44 | O-Oh. Right. I completely forgot she's the\n |
| 0x138eae | 18 | imperial princess. |
| 0x138ec1 | 47 | And I find speaking with you to be a delight.\n |
| 0x138ef1 | 43 | With someone like you, life would be more\n |
| 0x138f1d | 13 | entertaining. |
| 0x138f2b | 17 | So? What say you? |
| 0x138f3d | 46 | U-Uhm, I don't know. This is... pretty sudden. |
| 0x138f6c | 46 | So be it. I hardly intend to press an answer\n |
| 0x138f9b | 45 | from you. Take your time and think over it,\n |
| 0x138fc9 | 9 | at least. |
| 0x138fd3 | 38 | As we talk, we find ourselves at our\n |
| 0x138ffa | 47 | destination--and the point I can't go beyond,\n |
| 0x13902a | 14 | unfortunately. |
| 0x139039 | 42 | I'll see you again. I thank you for your\n |
| 0x139064 | 20 | assistance this eve. |
| 0x139079 | 46 | I guess we all need a break from things from\n |
| 0x1390a8 | 18 | time to time, huh? |
| 0x1390bb | 16 | Truly, it is so. |
| 0x1390cc | 42 | At least we can agree on this one thing... |
| 0x1390f7 | 33 | I enjoyed myself greatly today.\n |
| 0x139119 | 19 | We will meet again. |
| 0x13912d | 7 | Sure... |
| 0x139135 | 46 | She's planning on escaping again, isn't she... |
| 0x139164 | 48 | It's extremely late by the time I make it back\n |
| 0x139195 | 13 | to the inn... |
| 0x1391a3 | 14 | Hey, I'm back. |
| 0x1391b2 | 41 | And where have you been out to so late,\n |
| 0x1391dc | 5 | Haku? |
| 0x1391e2 | 47 | Kuon smiles unsettlingly as she "welcomes" me\n |
| 0x139212 | 5 | back. |
| 0x139218 | 46 | Just let me explain, please. It's not like I\n |
| 0x139247 | 20 | was goofing off, OK? |
| 0x13925c | 45 | To make a very long story very short, I had\n |
| 0x13928a | 33 | another run-in with the princess. |
| 0x1392ac | 31 | Nngh. THAT princess again, huh? |
| 0x1392cc | 47 | I swear I was minding my own business and got\n |
| 0x1392fc | 45 | roped into it. Complaining won't do any good. |
| 0x13932a | 47 | I suppose you're right. It can't be helped...\n |
| 0x13935a | 38 | Did you finish your errands, at least? |
| 0x139381 | 3 | Uh. |
| 0x139385 | 46 | Shit. I totally left the groceries somewhere\n |
| 0x1393b4 | 16 | out in the city! |
| 0x1393c5 | 7 | Haku... |
| 0x1393cd | 46 | Look, please, this whole day has been out of\n |
| 0x1393fc | 12 | my control-- |
| 0x139409 | 12 | Take a seat. |
| 0x139416 | 20 | Just let me explain! |
| 0x13942b | 19 | I said take a seat. |
| 0x13943f | 14 | ...Yes, ma'am. |
| 0x13b3a2 | 28 | Whew, glad that's over with. |
| 0x13b3bf | 41 | They said it was a dirty job, but I was\n |
| 0x13b3e9 | 44 | expecting to work undercover or something,\n |
| 0x13b416 | 20 | not gutter cleaning. |
| 0x13b42b | 45 | I mean, yeah, that's LITERALLY a dirty job,\n |
| 0x13b459 | 45 | but not exactly what I was expecting, y'know? |
| 0x13b487 | 36 | Would you please stop complaining?\n |
| 0x13b4ac | 43 | Remember, those who work not shall eat not. |
| 0x13b4d8 | 44 | Then as one who has worked, I demand to eat. |
| 0x13b505 | 49 | I'm parched, could you get me some tea? And get\n |
| 0x13b537 | 45 | me a snack while you're up. I worked myself\n |
| 0x13b565 | 7 | hungry. |
| 0x13b56d | 44 | You fail to recall that WE were working as\n |
| 0x13b59a | 11 | well, Haku. |
| 0x13b5a6 | 47 | True, but think about it. Who'd you prefer to\n |
| 0x13b5d6 | 46 | pour you tea, a cute girl, or some crusty guy? |
| 0x13b605 | 19 | What's it gonna be? |
| 0x13b619 | 9 | That's... |
| 0x13b623 | 44 | If you don't want to, I can get it myself.\n |
| 0x13b650 | 39 | I'll make enough for everyone, but no\n |
| 0x13b678 | 12 | complaining. |
| 0x13b685 | 45 | My tea-brewing skills are mediocre at best,\n |
| 0x13b6b3 | 15 | you may recall. |
| 0x13b6c3 | 29 | I... can just get my own tea. |
| 0x13b6e1 | 46 | That so? Then pour me a cup too while you're\n |
| 0x13b710 | 6 | at it. |
| 0x13b717 | 38 | Wha--Why does it come back to that!?\n |
| 0x13b73e | 42 | I get my own and you get your own. It is\n |
| 0x13b769 | 16 | not complicated. |
| 0x13b77a | 49 | If we brew our own tea separately, it's a waste\n |
| 0x13b7ac | 34 | of time, tea leaves, and charcoal. |
| 0x13b7cf | 44 | It can't be... Is the great scholar Nekone\n |
| 0x13b7fc | 37 | suggesting such inefficiency as that? |
| 0x13b822 | 8 | Rrrgh... |
| 0x13b82b | 47 | Haku, I know it's fun to tease Nekone because\n |
| 0x13b85b | 36 | she's so cute, but lay off a little. |
| 0x13b880 | 12 | Aheh heh.... |
| 0x13b88d | 14 | Dear sister... |
| 0x13b89c | 45 | Perfect timing, Rulutieh. Could you brew us\n |
| 0x13b8ca | 48 | some tea? I'd love to have some prepared by you. |
| 0x13b8fb | 38 | Y-Yes... I'll prepare it right away... |
| 0x13b922 | 47 | Haku, need I remind you, LADY Rulutieh is the\n |
| 0x13b952 | 42 | princess of Kujyuri. Address her properly. |
| 0x13b97d | 49 | That may be true, but she's still just Rulutieh\n |
| 0x13b9af | 6 | to me. |
| 0x13b9b6 | 21 | Um... I don't mind... |
| 0x13b9cc | 22 | I prefer it, really... |
| 0x13b9e3 | 29 | If you insist, Lady Rulutieh. |
| 0x13ba01 | 47 | A-Ah, and... I bought snacks on the way home.\n |
| 0x13ba31 | 43 | I thought we could have them after work...? |
| 0x13ba5d | 47 | Um... I-I'm sorry I couldn't cook them myself\n |
| 0x13ba8d | 32 | today. Work kept me very busy... |
| 0x13baae | 22 | Hm? Wait, these are--? |
| 0x13bac5 | 47 | They've been a popular snack amongst women of\n |
| 0x13baf5 | 21 | the capital, of late. |
| 0x13bb0b | 46 | To my memory, they consist of egg and nuts--\n |
| 0x13bb3a | 44 | a crispy texture, but they rapidly melt in\n |
| 0x13bb67 | 12 | one's mouth. |
| 0x13bb74 | 48 | I've been meaning to try them, but the line is\n |
| 0x13bba5 | 48 | always huge. They're sold out by the time it's\n |
| 0x13bbd6 | 8 | my turn. |
| 0x13bbdf | 46 | I've yet to obtain a sample, myself. How did\n |
| 0x13bc0e | 43 | you acquire such a high-demand item, Lady\n |
| 0x13bc3a | 9 | Rulutieh? |
| 0x13bc44 | 29 | W-Well... I didn't do much... |
| 0x13bc62 | 46 | I just... made friends with the owner of the\n |
| 0x13bc91 | 47 | store since I go a lot, and she... saved some\n |
| 0x13bcc1 | 7 | for me. |
| 0x13bcc9 | 19 | ...Wait, seriously? |
| 0x13bcdd | 43 | Interesting. That shop is known for never\n |
| 0x13bd09 | 45 | giving special treatment to customers, even\n |
| 0x13bd37 | 9 | regulars. |
| 0x13bd41 | 30 | Yeah... that's pretty amazing. |
| 0x13bd60 | 27 | It... really wasn't much... |
| 0x13bd7c | 50 | Please, have some. I got a lot of them, so don't\n |
| 0x13bdaf | 30 | worry about taking too much... |
| 0x13bdce | 49 | If we've got so many of them, why don't we call\n |
| 0x13be00 | 47 | the others? They'll be mad if they miss their\n |
| 0x13be30 | 7 | chance. |
| 0x13be38 | 18 | Hee... yes, let's. |
| 0x13be4b | 47 | Oh, if we're making a gathering of it, let me\n |
| 0x13be7b | 37 | get out the leftovers from last time. |
| 0x13bea1 | 39 | I'll find the best tea we have, then... |
| 0x13bec9 | 47 | I-I'll assist you, then. It would be improper\n |
| 0x13bef9 | 43 | not to help while the two of you labor to\n |
| 0x13bf25 | 10 | prepare... |
| 0x13bf30 | 32 | And so the three of them get up. |
| 0x13bf51 | 44 | Haku, could you go find Atuy and Kiwru and\n |
| 0x13bf7e | 17 | invite them, too? |
| 0x13bf90 | 42 | Kuon's tail sways happily as she speaks.\n |
| 0x13bfbb | 43 | She must really be looking forward to this. |
| 0x13bfe7 | 27 | Hee hee, snack time, is it? |
| 0x13c003 | 33 | Ah, yes! I'd be glad to join you. |
| 0x13c025 | 44 | After inviting Atuy and Kiwru, I have some\n |
| 0x13c052 | 43 | time alone with my thoughts as I walk back. |
| 0x13c07e | 46 | I'm still surprised Rulutieh was able to get\n |
| 0x13c0ad | 45 | special treatment from a shop known for not\n |
| 0x13c0db | 12 | giving it... |
| 0x13c0e8 | 47 | But I suppose that's part of her charm. She's\n |
| 0x13c118 | 44 | the sort of girl everybody wants to protect. |
| 0x13c145 | 32 | She must be loved by her people. |
| 0x13c166 | 48 | Now that I think about it, Kuon seemed awfully\n |
| 0x13c197 | 44 | perturbed by Rulutieh's special attention... |
| 0x13c1c4 | 47 | Or did she just want these snacks that badly?\n |
| 0x13c1f4 | 45 | I guess that's not totally out-of-character\n |
| 0x13c222 | 9 | for her-- |
| 0x13c22c | 44 | Ah, you've returned. Forgive my intrusion,\n |
| 0x13c259 | 8 | as ever. |
| 0x13c262 | 4 | Huh? |
| 0x13c267 | 48 | To my disbelief, I return to find a person who\n |
| 0x13c298 | 46 | shouldn't be there--none other than Princess\n |
| 0x13c2c7 | 5 | Anju. |
| 0x13c2cd | 44 | She shouldn't be here, yet there she sits,\n |
| 0x13c2fa | 39 | laying on the couch with a book. Again. |
| 0x13c322 | 49 | The same as ever... she eats a snack, scratches\n |
| 0x13c354 | 43 | her butt, refuses to pull her skirt down... |
| 0x13c380 | 48 | There's nothing proper or ladylike about this.\n |
| 0x13c3b1 | 46 | Were her subjects to see her now, there'd be\n |
| 0x13c3e0 | 6 | tears. |
| 0x13c3e7 | 37 | Brother... please forgive me for my\n |
| 0x13c40d | 16 | powerlessness... |
| 0x13c41e | 48 | Correction, there ARE tears. Kiwru has already\n |
| 0x13c44f | 43 | collapsed to his knees, sobbing in despair. |
| 0x13c47b | 48 | Kuon and the others return with the snacks and\n |
| 0x13c4ac | 6 | tea... |
| 0x13c4b3 | 29 | I'm sorry to make you wait... |
| 0x13c4d1 | 45 | Um, is something the matter? Why aren't you\n |
| 0x13c4ff | 13 | going inside? |
| 0x13c50d | 48 | I guess you could say something's wrong, yeah... |
| 0x13c53e | 49 | What are you babbling about? Come, the tea will\n |
| 0x13c570 | 37 | get cold if you hold us up like this. |
| 0x13c596 | 48 | Nekone elbows her way to the front and freezes\n |
| 0x13c5c7 | 27 | when she sees who's inside. |
| 0x13c5e3 | 19 | Your... Highness... |
| 0x13c5f7 | 18 | She's here. Again. |
| 0x13c60a | 42 | Kuon also seems to be at a loss for words. |
| 0x13c635 | 48 | I'm pretty sure I know the answer, but... what\n |
| 0x13c666 | 27 | exactly are you doing here? |
| 0x13c682 | 42 | Anju, absorbed in her book, doesn't even\n |
| 0x13c6ad | 20 | glance up to answer. |
| 0x13c6c2 | 17 | Can you not tell? |
| 0x13c6d4 | 48 | It's clear as day what you came here for, yes,\n |
| 0x13c705 | 44 | but someone has to ask and get it over with. |
| 0x13c732 | 40 | I merely slipped out of my chambers to\n |
| 0x13c75b | 48 | "have fun." Pay me no mind and continue as you\n |
| 0x13c78c | 5 | were. |
| 0x13c796 | 44 | It seems my presence alone gives commoners\n |
| 0x13c7c3 | 41 | reason to shrink away. Please, I can be\n |
| 0x13c7ed | 12 | magnanimous. |
| 0x13c7fa | 42 | OK, that's nice. And why exactly did you\n |
| 0x13c825 | 30 | come here to have your fun...? |
| 0x13c844 | 47 | Ah, yes, the root of the matter... I was bored. |
| 0x13c874 | 49 | Would you please stop sneaking out just because\n |
| 0x13c8a6 | 49 | you're bored? You're gonna cause a stir at this\n |
| 0x13c8d8 | 5 | rate. |
| 0x13c8de | 49 | Not to worry. A decoy has been secured and left\n |
| 0x13c910 | 42 | in my place. No man shall suspect my ruse. |
| 0x13c93b | 46 | Heh. I must remember to thank them for their\n |
| 0x13c96a | 8 | service. |
| 0x13c973 | 39 | Highness, I implore you--consider the\n |
| 0x13c99b | 47 | repercussions before you act so rashly in the\n |
| 0x13c9cb | 7 | future. |
| 0x13c9d3 | 36 | Do you not agree, dear sister? Atuy? |
| 0x13c9f8 | 28 | ...Huh? Um, u-uh, yes? Sure? |
| 0x13ca15 | 34 | Kuon abruptly glances away. Odd... |
| 0x13ca38 | 12 | Dear sister? |
| 0x13ca45 | 24 | ...Y-Yeah, that's right. |
| 0x13ca5e | 26 | Atuy also averts her eyes. |
| 0x13ca79 | 5 | Atuy? |
| 0x13ca7f | 48 | This princess has no sense of danger. What are\n |
| 0x13cab0 | 46 | we gonna do with her? We can't just kick her\n |
| 0x13cadf | 6 | out... |
| 0x13cae6 | 47 | Just leaving a double to fill your spot won't\n |
| 0x13cb16 | 46 | cut it. Shouldn't you head back? People will\n |
| 0x13cb45 | 11 | be worried. |
| 0x13cb51 | 27 | Rulutieh nods in agreement. |
| 0x13cb6d | 3 | No. |
| 0x13cb71 | 21 | That--Now, look here. |
| 0x13cb87 | 48 | I said no! I wish not to return! The palace is\n |
| 0x13cbb8 | 47 | cramped, boring, and I'm constantly forced to\n |
| 0x13cbe8 | 6 | study! |
| 0x13cbef | 47 | Anju flails about on the couch, caring little\n |
| 0x13cc1f | 40 | for how her gown fails to hide anything. |
| 0x13cc48 | 41 | Compared to that place, this is paradise. |
| 0x13cc72 | 48 | Nobody regiments my life, tells me to study or\n |
| 0x13cca3 | 45 | mind my manners; I may eat and nap whenever\n |
| 0x13ccd1 | 9 | I desire. |
| 0x13ccdb | 38 | Perhaps I shall LIVE here from now on. |
| 0x13cd02 | 45 | Eat wh--You know all those snacks you scarf\n |
| 0x13cd30 | 30 | down are actually ours, right? |
| 0x13cd4f | 45 | H-Haku, what do we do? If news of this gets\n |
| 0x13cd7d | 43 | out, I'll be executed! My family, banished! |
| 0x13cda9 | 48 | I think you're asking the wrong guy here, Kiwru. |
| 0x13cdda | 47 | Even if we leave her be, if anything happens,\n |
| 0x13ce0a | 40 | we're likely to be held culpable anyway. |
| 0x13ce33 | 48 | Kiwru's right. The worst possible outcome here\n |
| 0x13ce64 | 43 | is we really do get our heads cut off for\n |
| 0x13ce90 | 7 | this... |
| 0x13ce98 | 23 | Hey, kid. You in there? |
| 0x13ceb0 | 45 | As we puzzle over what to do next, a cheery\n |
| 0x13cede | 32 | voice interrupts us from behind. |
| 0x13ceff | 21 | Ukon, perfect timing! |
| 0x13cf15 | 46 | Whoa, what's with the warm reception? Are we\n |
| 0x13cf44 | 31 | celebrating something, or what? |
| 0x13cf64 | 25 | Nekone smiles behind him. |
| 0x13cf7e | 24 | When the hell did she... |
| 0x13cf97 | 48 | Got some good booze and food, so I thought I'd\n |
| 0x13cfc8 | 13 | drop by and-- |
| 0x13cfd6 | 46 | Ukon looks past me and sees just who else is\n |
| 0x13d005 | 12 | in the room. |
| 0x13d012 | 10 | Holy shit! |
| 0x13d01d | 46 | And suddenly, he gives a bark of a shout I'd\n |
| 0x13d04c | 46 | never expect to hear from him, clearly taken\n |
| 0x13d07b | 10 | off-guard. |
| 0x13d086 | 21 | What's all this, now? |
| 0x13d09c | 43 | Anju looks over at Ukon from her lounging\n |
| 0x13d0c8 | 22 | position on the couch. |
| 0x13d0df | 49 | Ah, I see a guest has arrived. Who is this man,\n |
| 0x13d111 | 5 | then? |
| 0x13d117 | 46 | Ukon clears his throat, kneeling before Anju\n |
| 0x13d146 | 18 | with a bowed head. |
| 0x13d159 | 46 | You're Princess Anju, huh? I'm called Ukon--\n |
| 0x13d188 | 36 | a humble mercenary, at your service. |
| 0x13d1ad | 49 | Ukon, is it? There's no need for formalities in\n |
| 0x13d1df | 38 | a place such as this. Be at ease, sir. |
| 0x13d206 | 46 | I think you should be more worried that this\n |
| 0x13d235 | 44 | "stranger" recognized you at first glance... |
| 0x13d262 | 44 | And isn't Oshtor supposed to be her prince\n |
| 0x13d28f | 40 | charming? She doesn't suspect a thing... |
| 0x13d2b8 | 11 | Uh, Nekone? |
| 0x13d2c4 | 47 | Ukon turns to Nekone with a mixed expression,\n |
| 0x13d2f4 | 44 | wordlessly asking what the hell is going on. |
| 0x13d321 | 49 | Nekone doesn't say a word, simply aiming a curt\n |
| 0x13d353 | 20 | gesture toward Anju. |
| 0x13d368 | 34 | Oh, man. So that's what's up, huh? |
| 0x13d38b | 49 | Ukon sighs and briefly looks up to the heavens.\n |
| 0x13d3bd | 47 | He passes me the gifts he'd brought and leaves. |
| 0x13d3ed | 33 | Shortly after Ukon's departure... |
| 0x13d40f | 14 | Your Highness. |
| 0x13d41e | 42 | Eh heh heh. Not now, whoever it is. It's\n |
| 0x13d449 | 47 | getting to the good part. Oh, could you bring\n |
| 0x13d479 | 11 | me seconds? |
| 0x13d485 | 48 | I fear consuming too much of this sort of food\n |
| 0x13d4b6 | 45 | will be detrimental to your health, Highness. |
| 0x13d4e4 | 43 | And you choose now to bother me with that\n |
| 0x13d510 | 46 | revelation? Perhaps observe that I'm READING\n |
| 0x13d53f | 7 | and g-- |
| 0x13d547 | 48 | Anju finally turns to admonish the man chiding\n |
| 0x13d578 | 49 | her, but stops when she sees just who is before\n |
| 0x13d5aa | 4 | her. |
| 0x13d5af | 45 | Your Highness. I've come to escort you back\n |
| 0x13d5dd | 14 | to the palace. |
| 0x13d5ec | 46 | Oshtor bows deeply, kneeling in front of his\n |
| 0x13d61b | 9 | princess. |
| 0x13d625 | 16 | O-Osh... Oshtor! |
| 0x13d636 | 39 | How may I be of service, Your Highness? |
| 0x13d65e | 27 | Wh-What are you doing here? |
| 0x13d67a | 48 | As I stated, Highness. I've come to escort you\n |
| 0x13d6ab | 10 | back home. |
| 0x13d6b6 | 46 | If we leave now, we may be able to hide that\n |
| 0x13d6e5 | 48 | you were ever missing. Please prepare to depart. |
| 0x13d716 | 6 | Erm... |
| 0x13d71d | 46 | Anju seems to notice for the first time that\n |
| 0x13d74c | 45 | her gown is splayed, and hurriedly tries to\n |
| 0x13d77a | 14 | straighten it. |
| 0x13d789 | 16 | *Cough, cough--* |
| 0x13d79a | 24 | Is something the matter? |
| 0x13d7b3 | 28 | N-No. Nothing is the matter. |
| 0x13d7d0 | 10 | Very well. |
| 0x13d7db | 49 | Although Anju is flustered, Oshtor remains calm\n |
| 0x13d80d | 48 | and composed as if to say "I have seen nothing." |
| 0x13d83e | 44 | I-I did not expect you to come personally,\n |
| 0x13d86b | 7 | Oshtor. |
| 0x13d873 | 48 | M-May I ask why you came yourself? You must be\n |
| 0x13d8a4 | 46 | busy... That you came on your own, does that\n |
| 0x13d8d3 | 6 | mean-- |
| 0x13d8da | 47 | As Imperial Guard of the Right, it is my duty\n |
| 0x13d90a | 37 | to see to your safety, Your Highness. |
| 0x13d930 | 8 | I see... |
| 0x13d939 | 49 | Anju deflates at Oshtor's seemingly indifferent\n |
| 0x13d96b | 9 | response. |
| 0x13d975 | 45 | I have made ready a palanquin outside, Your\n |
| 0x13d9a3 | 39 | Highness. If you'd please accompany me? |
| 0x13d9cb | 38 | Oshtor stands, offering Anju his hand. |
| 0x13d9f2 | 45 | She stares into his face for a moment, then\n |
| 0x13da20 | 47 | sighs, accepting the hand and hauling herself\n |
| 0x13da50 | 8 | upright. |
| 0x13da59 | 37 | I thank you all for your hospitality. |
| 0x13da7f | 24 | She's finally leaving... |
| 0x13da98 | 46 | Please take care. I look forward to enjoying\n |
| 0x13dac7 | 19 | your company again. |
| 0x13dadb | 38 | You're still planning on coming back!? |
| 0x13e066 | 4 | Huh? |
| 0x13e06b | 45 | Hey, Nekone. Have you seen that paperweight\n |
| 0x13e099 | 11 | I had here? |
| 0x13e0a5 | 30 | No, I haven't laid eyes on it. |
| 0x13e0c4 | 40 | I see... I swear I left it around here\n |
| 0x13e0ed | 10 | somewhere. |
| 0x13e0f8 | 46 | It's impossible to tell where anything is in\n |
| 0x13e127 | 13 | this clutter. |
| 0x13e135 | 46 | Why do you refuse to tidy up after yourself?\n |
| 0x13e164 | 43 | You always make a mess as soon as we have\n |
| 0x13e190 | 10 | cleaned... |
| 0x13e19b | 50 | See, it may look like a mess to the uninitiated,\n |
| 0x13e1ce | 44 | but the placement of everything in here is\n |
| 0x13e1fb | 8 | precis-- |
| 0x13e204 | 34 | Do not waste my time with excuses. |
| 0x13e227 | 46 | With that, Nekone returns to her own desk to\n |
| 0x13e256 | 29 | begin sorting through papers. |
| 0x13e274 | 7 | Nngh... |
| 0x13e27c | 48 | I can't exactly argue with her when she's right. |
| 0x13e2ad | 13 | *Tap, tap*... |
| 0x13e2bb | 42 | Suddenly, I feel a tapping on my shoulder. |
| 0x13e2e6 | 3 | Hm? |
| 0x13e2ea | 20 | Mysterious duo right |
| 0x13e303 | 19 | Mysterious duo left |
| 0x13e317 | 41 | I look behind to find, once again, that\n |
| 0x13e341 | 39 | mysterious duo. One of them holds the\n |
| 0x13e369 | 21 | paperweight I'd lost. |
| 0x13e37f | 42 | Why are you--oh, hey. You found it for me? |
| 0x13e3aa | 14 | Mysterious duo |
| 0x13e3b9 | 24 | They both nod in unison. |
| 0x13e3d2 | 16 | R-Right. Thanks. |
| 0x13e3e3 | 47 | When the hell did they get here? They weren't\n |
| 0x13e413 | 43 | here before, right...? Why are they here,\n |
| 0x13e43f | 7 | anyway? |
| 0x13e447 | 40 | Did you two have some business here or\n |
| 0x13e470 | 10 | something? |
| 0x13e47b | 23 | They shake their heads. |
| 0x13e493 | 46 | O...K. And for curiosity's sake, you've been\n |
| 0x13e4c2 | 23 | here how long, exactly? |
| 0x13e4df | 49 | They tilt their heads to one side, as if to say\n |
| 0x13e511 | 35 | they don't understand the question. |
| 0x13e535 | 47 | Is something the matter? You've been mumbling\n |
| 0x13e565 | 12 | to yourself. |
| 0x13e572 | 33 | Nekone looks up at me, perturbed. |
| 0x13e594 | 27 | Well, you see, these two... |
| 0x13e5b0 | 38 | Which two? What are you talking about? |
| 0x13e5d7 | 34 | I'm talking about... They're gone? |
| 0x13e5fa | 41 | When I glance behind myself, of course,\n |
| 0x13e624 | 21 | there's no one there. |
| 0x13e63a | 45 | What the hell is going on? They came out of\n |
| 0x13e668 | 29 | nowhere and just... vanished. |
| 0x13e686 | 46 | They'd better not be ghosts or anything like\n |
| 0x13e6b5 | 7 | that... |
| 0x13ff70 | 7 | ...Huh? |
| 0x13ff78 | 50 | While walking my usual way back from my errands,\n |
| 0x13ffab | 33 | I start to get an uneasy feeling. |
| 0x13ffcd | 44 | I was walking on the main street... I think? |
| 0x13fffa | 45 | I'd been taking the main street back to the\n |
| 0x140028 | 46 | Hakurokaku as usual, but somehow ended up in\n |
| 0x140057 | 13 | this alley... |
| 0x140065 | 46 | That's strange. What am I doing in this back\n |
| 0x140094 | 33 | alley? And why is it so... quiet? |
| 0x1400b6 | 49 | Some kind of mist fills the street and obscures\n |
| 0x1400e8 | 45 | my vision, but even so, I can tell no one's\n |
| 0x140116 | 10 | around me. |
| 0x140121 | 49 | The noisy ambience of the city has fallen away,\n |
| 0x140153 | 43 | and an eerie silence reigns in its place... |
| 0x14017f | 47 | My hand closes around the metal fan Kuon gave\n |
| 0x1401af | 33 | me, and I look around cautiously. |
| 0x1401d6 | 21 | Someone's... there... |
| 0x1401ec | 46 | The mist obscures them, but a pair of shapes\n |
| 0x14021b | 38 | approaches in the fog, drawing nearer. |
| 0x140242 | 31 | They're getting pretty close... |
| 0x140262 | 20 | Who is it? An enemy? |
| 0x140277 | 33 | ...and they've disappeared. Who-- |
| 0x140299 | 13 | *Tug, tug*... |
| 0x1402a7 | 4 | Wh-- |
| 0x1402ac | 50 | The approaching twin shadows disappear abruptly,\n |
| 0x1402df | 46 | and I feel a tugging on my sleeve from behind. |
| 0x14030e | 47 | A familiar, silent pair stand there as though\n |
| 0x14033e | 34 | they've been here the entire time. |
| 0x140361 | 25 | When the hell did they... |
| 0x14037b | 36 | You two. Don't scare me like that!\n |
| 0x1403a0 | 34 | You almost gave me a heart attack. |
| 0x1403c3 | 14 | Mysterious duo |
| 0x1403d7 | 47 | They tilt their heads in that same bewildered\n |
| 0x140407 | 37 | manner. Do they not understand, or... |
| 0x14042d | 43 | These two are as much of an enigma as ever. |
| 0x140459 | 31 | Did you want something from me? |
| 0x14047d | 8 | *Tug*... |
| 0x140486 | 3 | Hm? |
| 0x14048a | 44 | They each grab one of my hands and pull me\n |
| 0x1404b7 | 42 | along, heading down the alley in typical\n |
| 0x1404e2 | 8 | silence. |
| 0x1404eb | 22 | You want me to follow? |
| 0x140502 | 50 | They each nod, then begin to walk again, guiding\n |
| 0x140535 | 14 | me as they go. |
| 0x140544 | 35 | Did you two create this mist, then? |
| 0x140568 | 9 | ...I see. |
| 0x140572 | 44 | I don't really get it, but they seem to be\n |
| 0x14059f | 39 | acting this way for a reason, at least. |
| 0x1405c7 | 45 | I'm surprised I'm allowing myself to be led\n |
| 0x1405f5 | 19 | along so blindly... |
| 0x140609 | 46 | But when it comes to these two, I just don't\n |
| 0x140638 | 48 | feel threatened. They haven't done me any harm\n |
| 0x140669 | 4 | yet. |
| 0x14066e | 38 | Whoa, whoa. Where the hell are we now? |
| 0x140695 | 47 | I haven't been paying attention, but suddenly\n |
| 0x1406c5 | 45 | we seem to be in the corridors of a massive\n |
| 0x1406f3 | 9 | building? |
| 0x1406fd | 41 | When the hell did we enter a beast of a\n |
| 0x140727 | 18 | complex like this? |
| 0x14073a | 49 | Ultimately, the winding maze of corridors opens\n |
| 0x14076c | 27 | into a broader, open space. |
| 0x140788 | 11 | Elderly man |
| 0x140794 | 50 | Ah, it seems our guest has arrived. Most timely.\n |
| 0x1407c7 | 31 | Honoka, some tea, if you would? |
| 0x1407e7 | 19 | Woman called Honoka |
| 0x1407fb | 13 | At once, sir. |
| 0x140809 | 42 | Gorgeous stonework pillars ring the open\n |
| 0x140834 | 10 | chamber... |
| 0x14083f | 47 | A small round table sits in the middle, and a\n |
| 0x14086f | 48 | man in a wheelchair and a young woman are both\n |
| 0x1408a0 | 19 | waiting next to it. |
| 0x1408b4 | 38 | Thank you for coming, my dear guest.\n |
| 0x1408db | 12 | Please, sit. |
| 0x1408e8 | 43 | The old man smiles amicably, indicating a\n |
| 0x140914 | 43 | comfortable-looking chair across the table. |
| 0x140940 | 39 | Who the--I-I mean, who... are you, sir? |
| 0x140968 | 46 | Me...? Ah, I WAS a crepe salesman of a kind,\n |
| 0x140997 | 43 | but I'm long retired. Call me Mito, if it\n |
| 0x1409c3 | 11 | please you. |
| 0x1409cf | 14 | Uh, all right. |
| 0x1409de | 45 | Why does that feel suspiciously like a fake\n |
| 0x140a0c | 5 | name? |
| 0x140a12 | 19 | Uh, and I-I'm Haku. |
| 0x140a26 | 44 | Haku, then. I thank you for accepting such\n |
| 0x140a53 | 20 | a sudden invitation. |
| 0x140a68 | 47 | Invitation...? Are you in charge of those two\n |
| 0x140a98 | 17 | back there, then? |
| 0x140aaa | 49 | I've heard quite a lot about you. I thought I'd\n |
| 0x140adc | 45 | arrange a chance to speak to you in person,\n |
| 0x140b0a | 8 | you see. |
| 0x140b13 | 47 | Heard about me? From who? Are those two spies\n |
| 0x140b43 | 8 | for him? |
| 0x140b4c | 50 | I look around, but--of course--the Mystery Twins\n |
| 0x140b7f | 17 | have disappeared. |
| 0x140b91 | 13 | This again... |
| 0x140b9f | 44 | The tea is prepared. Please, if you'd seat\n |
| 0x140bcc | 9 | yourself? |
| 0x140bd6 | 11 | Ah, sure... |
| 0x140be2 | 48 | I look up at the woman Mito had called Honoka,\n |
| 0x140c13 | 47 | and I find it oddly difficult to take my eyes\n |
| 0x140c43 | 8 | off her. |
| 0x140c4c | 48 | Her beauty rivals that of the Hakurokaku Inn's\n |
| 0x140c7d | 45 | mistress. The same poise, the refined aura... |
| 0x140cab | 48 | Entranced by that smile of hers, I sit without\n |
| 0x140cdc | 9 | thinking. |
| 0x140ce6 | 45 | Shit... Am I letting myself be manipulated?\n |
| 0x140d14 | 48 | But... no, she doesn't seem to mean me any harm. |
| 0x140d45 | 49 | I don't know why, but when I look at her, I get\n |
| 0x140d77 | 41 | this... sad feeling. Nostalgic, almost.\n |
| 0x140da1 | 15 | Could it be...? |
| 0x140db1 | 24 | Is something the matter? |
| 0x140dca | 47 | I snap back to attention when she speaks again. |
| 0x140dfa | 30 | Oh... no, sorry, I'm just...\n |
| 0x140e19 | 32 | Have we... met somewhere before? |
| 0x140e3a | 46 | I'm afraid this is the first time we've met,\n |
| 0x140e69 | 4 | sir. |
| 0x140e6e | 11 | I... I see. |
| 0x140e7a | 44 | Figures. Life's not so convenient that I'd\n |
| 0x140ea7 | 47 | suddenly find people who know me from my past\n |
| 0x140ed7 | 7 | life... |
| 0x140edf | 42 | It seems like the old man is the one who\n |
| 0x140f0a | 36 | invited me, though. What's his game? |
| 0x140f2f | 24 | I look him over again... |
| 0x140f48 | 48 | At first glance, he looks like a simple, good-\n |
| 0x140f79 | 46 | natured old man, but he has gravitas to him.\n |
| 0x140fa8 | 7 | Weight. |
| 0x140fb0 | 28 | Who the hell is this geezer? |
| 0x140fcd | 37 | This is the finest tea from Shiozu.\n |
| 0x140ff3 | 35 | Please, drink while it's still hot. |
| 0x141017 | 15 | Oh, thanks...\n |
| 0x141027 | 3 | Eh? |
| 0x14102b | 10 | This is... |
| 0x141036 | 43 | Unlike the tea I've been drinking so far,\n |
| 0x141062 | 43 | this stuff has a vibrant green color to it. |
| 0x14108e | 10 | *Slurp*... |
| 0x141099 | 49 | Oh, that's good. Not too bitter, not too sweet.\n |
| 0x1410cb | 27 | Temperature's just right... |
| 0x1410e7 | 49 | The fragrance and this refreshing bitterness...\n |
| 0x141119 | 39 | Yeah, that's good green tea, all right. |
| 0x141141 | 38 | The nostalgic scent fills my nostrils. |
| 0x141168 | 43 | How long has it been since I've had green\n |
| 0x141194 | 7 | tea...? |
| 0x14119c | 47 | How long HAS it been? I can't recall drinking\n |
| 0x1411cc | 42 | any since waking up on that mountain, so\n |
| 0x1411f7 | 9 | where...? |
| 0x141201 | 24 | Is there a problem, sir? |
| 0x14121a | 13 | Oh... n-no... |
| 0x141228 | 46 | I get that strange feeling again when I look\n |
| 0x141257 | 14 | into her eyes. |
| 0x141266 | 50 | Is this really our first meeting? Then why can't\n |
| 0x141299 | 37 | I shake the feeling I... know her...? |
| 0x1412bf | 38 | So, can I ask why you invited me here? |
| 0x1412e6 | 47 | Ah, yes, that. I was hoping you could tell me\n |
| 0x141316 | 29 | of your travails in the city. |
| 0x141334 | 48 | As you can see, it's difficult for me to leave\n |
| 0x141365 | 46 | this place, let alone visit places I wish to\n |
| 0x141394 | 10 | on a whim. |
| 0x14139f | 45 | The only enjoyment I really have left to me\n |
| 0x1413cd | 42 | is the stories others tell me. Call it a\n |
| 0x1413f8 | 14 | hobby of mine. |
| 0x141407 | 46 | Stories... I dunno what to say. I don't have\n |
| 0x141436 | 46 | any memories of my past, so there's not much\n |
| 0x141465 | 14 | to talk about. |
| 0x141474 | 46 | Ah, yes, I've been informed of your amnesia.\n |
| 0x1414a3 | 47 | It's why I invited YOU in particular, actually. |
| 0x1414d3 | 45 | After losing your memories, you've seen and\n |
| 0x141501 | 40 | done much to find your way here to the\n |
| 0x14152a | 17 | imperial capital. |
| 0x14153c | 39 | Your vision of the world is... clear.\n |
| 0x141564 | 44 | Unaltered by upbringing, culture, customs... |
| 0x141591 | 44 | So, in other words, he wants to hear about\n |
| 0x1415be | 32 | the hardships I've been through? |
| 0x1415df | 43 | Sorry to disappoint, old man, but I don't\n |
| 0x14160b | 46 | consider them hardships. And I'm not here to\n |
| 0x14163a | 14 | entertain you. |
| 0x141649 | 46 | I sense you are angry. You think me a sadist\n |
| 0x141678 | 42 | or a voyeur, deriving pleasure from your\n |
| 0x1416a3 | 15 | hardships, yes? |
| 0x1416b3 | 6 | Urk... |
| 0x1416ba | 45 | Perhaps I was wearing my heart on my sleeve\n |
| 0x1416e8 | 21 | a bit much, just now. |
| 0x1416fe | 48 | Please understand. I wish not to ridicule you;\n |
| 0x14172f | 24 | only to hear your story. |
| 0x141748 | 45 | I would like to ask you again, with that in\n |
| 0x141776 | 45 | mind. Will you humor an old man with little\n |
| 0x1417a4 | 10 | time left? |
| 0x1417af | 39 | Please, Sir Haku. I beg of you as well. |
| 0x1417d7 | 48 | Gah, I can't exactly refuse when they ask like\n |
| 0x141808 | 7 | that... |
| 0x141810 | 46 | Just to warn you, there's not really much to\n |
| 0x14183f | 5 | tell. |
| 0x141845 | 36 | Ah, but you'll tell it all the same? |
| 0x14186a | 34 | A smile splits the old man's face. |
| 0x14188d | 48 | And so, I tell him everything there is to tell\n |
| 0x1418be | 33 | about what happened after I woke. |
| 0x1418e0 | 32 | The snowfield where I came to... |
| 0x141901 | 48 | The gigiri that attacked me, and Kuon's timely\n |
| 0x141932 | 9 | rescue... |
| 0x14193c | 48 | How I tried to find a job in the nearest town,\n |
| 0x14196d | 45 | but turned out to be too weak to be useful... |
| 0x14199b | 44 | How Kuon worried for me and took me to the\n |
| 0x1419c8 | 22 | capital for my sake... |
| 0x1419df | 41 | All the companions I met along the way... |
| 0x141a09 | 47 | The old man listens to every detail intently,\n |
| 0x141a39 | 35 | and the woman smiles all the while. |
| 0x141a5d | 47 | Oh ho ho... I see. And that's how you came to\n |
| 0x141a8d | 16 | the city, is it? |
| 0x141a9e | 49 | An interesting tale, indeed. You live more of a\n |
| 0x141ad0 | 37 | storied life than you claim, I think. |
| 0x141af6 | 26 | I honestly can't stand it. |
| 0x141b11 | 49 | It must be hard to face such a life without any\n |
| 0x141b43 | 25 | knowledge of your past... |
| 0x141b5d | 49 | Thank you for fulfilling an old man's arbitrary\n |
| 0x141b8f | 47 | request. If there's anything I can do for you-- |
| 0x141bbf | 47 | That's all right, thank you. I appreciate the\n |
| 0x141bef | 18 | sentiment, though. |
| 0x141c02 | 22 | Sir, it's almost time. |
| 0x141c19 | 40 | Ah, how time flies. I must be off, but\n |
| 0x141c42 | 41 | thank you for this. It was a worthwhile\n |
| 0x141c6c | 11 | experience. |
| 0x141c78 | 23 | It was nothing, really. |
| 0x141c90 | 45 | I got to drink some good tea and get things\n |
| 0x141cbe | 48 | off my chest. I feel a lot better than before,\n |
| 0x141cef | 9 | actually. |
| 0x141cf9 | 49 | Spending time here with these two wasn't as bad\n |
| 0x141d2b | 32 | as it could have been, honestly. |
| 0x141d4c | 50 | Thank you, Sir Haku. It has been quite some time\n |
| 0x141d7f | 37 | since I've seen my master so content. |
| 0x141da5 | 46 | Oh, it's no problem. I have to thank YOU for\n |
| 0x141dd4 | 16 | the amazing tea. |
| 0x141de5 | 28 | Yeah, not a bad time at all. |
| 0x141e02 | 46 | The old man claps his hands, and the Mystery\n |
| 0x141e31 | 44 | Twins appear as though they'd been waiting\n |
| 0x141e5e | 8 | eagerly. |
| 0x141e67 | 39 | I trust you two can show our guest out? |
| 0x141e8f | 49 | Good. I apologize for taking up so much of your\n |
| 0x141ec1 | 32 | time, Haku. Until we meet again. |
| 0x141ee2 | 9 | ...Bwuh!? |
| 0x141eec | 47 | The next moment, I snap upright in my own room. |
| 0x141f1c | 45 | There's no sign of that old man, the woman,\n |
| 0x141f4a | 21 | or the strange duo... |
| 0x141f60 | 24 | ...Was it... a dream...? |
| 0x141f79 | 48 | The words leave my lips, but somehow I know it\n |
| 0x141faa | 40 | wasn't. Still, the experience feels...\n |
| 0x141fd3 | 10 | dreamlike? |
| 0x141fde | 46 | What's this... nagging feeling I'm getting...? |
| 0x14200d | 48 | And my chest feels... tight? Like I'm in pain... |
| 0x14203e | 48 | No answer to my questions, of course, presents\n |
| 0x14206f | 41 | itself in the silence. Not that it would. |
| 0x145f07 | 46 | I return from patrol duty to find a drained,\n |
| 0x145f36 | 44 | despair-filled Kiwru standing guard at the\n |
| 0x145f63 | 9 | inn room. |
| 0x145f6d | 43 | What're you doing standing there like that? |
| 0x145f99 | 37 | Oh, Haku... Rulutieh. Welcome back... |
| 0x145fbf | 48 | Kiwru forces a smile, eyes lifeless and haggard. |
| 0x145ff0 | 19 | U-Uhm... Thank you. |
| 0x146004 | 48 | Rulutieh smiles back, but backs up a few steps\n |
| 0x146035 | 28 | after seeing his expression. |
| 0x146052 | 36 | Wait, wait, wait. What's going on?\n |
| 0x146077 | 27 | Why do you look so drained? |
| 0x146093 | 45 | Kiwru may not look it, but he's typically a\n |
| 0x1460c1 | 48 | stalwart guard. He's Oshtor's sworn kin, after\n |
| 0x1460f2 | 4 | all. |
| 0x1460f7 | 46 | And to see him this ragged? The last time he\n |
| 0x146126 | 24 | was like this was when-- |
| 0x14613f | 20 | Last time. Oh, hell. |
| 0x146154 | 23 | Is, uh, SHE here again? |
| 0x14616c | 19 | *Twitch, twitch*... |
| 0x146180 | 7 | ...Yes. |
| 0x146188 | 49 | Kiwru nods, shivering like some kind of newborn\n |
| 0x1461ba | 7 | animal. |
| 0x1461c2 | 47 | Her Highness arrived just a little while ago,\n |
| 0x1461f2 | 16 | out of the blue. |
| 0x146203 | 42 | She proceeded to commandeer the room and\n |
| 0x14622e | 43 | ordered me to stand watch in case my lord\n |
| 0x14625a | 25 | brother Oshtor arrives... |
| 0x146274 | 30 | Lady Anju is... here again...? |
| 0x146293 | 13 | Where's Kuon? |
| 0x1462a1 | 46 | She and Nekone had business in the city, so... |
| 0x1462d0 | 5 | Urgh. |
| 0x1462d6 | 45 | So none of the people who can stop Anju are\n |
| 0x146304 | 5 | here. |
| 0x14630a | 9 | *Sigh*... |
| 0x146314 | 46 | I rub my temples to dispel a brewing headache. |
| 0x146343 | 48 | I open the door, and there lies Anju, snacking\n |
| 0x146374 | 35 | and reading on the couch as always. |
| 0x146398 | 23 | Bweh heh--eh heh heh... |
| 0x1463b0 | 46 | And I really don't want to hear her laughing\n |
| 0x1463df | 10 | like that. |
| 0x1463ea | 17 | Ah... ahah hah... |
| 0x1463fc | 21 | Oh... N-No...Ohhhh... |
| 0x146412 | 45 | Upon seeing Anju, Rulutieh turns as pale as\n |
| 0x146440 | 27 | Kiwru and begins to fidget. |
| 0x14645c | 15 | How did she...? |
| 0x14646c | 43 | I thought I... hid it more carefully this\n |
| 0x146498 | 7 | time... |
| 0x1464a0 | 33 | Such friendship... hard work...\n |
| 0x1464c2 | 30 | Victory for men... And then... |
| 0x1464e1 | 42 | Ah, this is so wonderful. Who would have\n |
| 0x14650c | 41 | thought that such a world could exist...? |
| 0x146536 | 37 | She kicks her legs idly as she lazes. |
| 0x14655c | 47 | I'm getting the feeling I'm hearing things no\n |
| 0x14658c | 28 | princess should be saying... |
| 0x1465a9 | 48 | How bizarre. That proud, elegant princess Kuon\n |
| 0x1465da | 48 | and I saw on the day of the nativity festival... |
| 0x14660b | 15 | Bweh heh heh... |
| 0x14661b | 47 | ...reduced to this. How the mighty have fallen. |
| 0x14664b | 46 | I would've thought her little encounter with\n |
| 0x14667a | 49 | Oshtor last time embarrassed her too much, but... |
| 0x1466ac | 49 | Forget 'princess,' this is questionable even as\n |
| 0x1466de | 19 | a common city girl. |
| 0x1466f2 | 44 | If only I was stronger. Then this wouldn't\n |
| 0x14671f | 7 | have... |
| 0x146727 | 44 | Beside me, Kiwru hunches over in shame and\n |
| 0x146754 | 28 | pain, clutching his stomach. |
| 0x146771 | 43 | Looks like he's got it tough. Not that it\n |
| 0x14679d | 21 | really matters to me. |
| 0x1467b3 | 11 | We're b--\n |
| 0x1467bf | 33 | ...What exactly is going on here? |
| 0x1467e1 | 46 | Kuon arrives and takes one look at the messy\n |
| 0x146810 | 7 | room... |
| 0x146818 | 30 | Dear sister? What is the m--\n |
| 0x146837 | 21 | Oh. ...Your Highness. |
| 0x14684d | 50 | Nekone arrives behind Kuon, a furrow in her brow\n |
| 0x146880 | 25 | at the state of the room. |
| 0x14689a | 49 | Hm? Ah, if it isn't Haku. I've returned to your\n |
| 0x1468cc | 21 | company, as promised. |
| 0x1468e2 | 15 | ...As promised? |
| 0x1468f6 | 46 | I can feel Kuon and Nekone's eyes on me like\n |
| 0x146925 | 19 | daggers in my skin. |
| 0x146939 | 45 | H-Hold on, now! I never made a promise like\n |
| 0x146967 | 5 | that. |
| 0x14696d | 46 | Stop looking at me with your puppy-dog eyes!\n |
| 0x14699c | 18 | It's not my fault! |
| 0x1469af | 45 | Hm? Ah, I've depleted my snacks. Haku, your\n |
| 0x1469dd | 38 | princess bids you bring her seconds.\n |
| 0x146a04 | 12 | Be about it. |
| 0x146a11 | 43 | Those were supposed to be for our meeting\n |
| 0x146a3d | 44 | today, Anju. You took them without asking,\n |
| 0x146a6a | 10 | as always. |
| 0x146a75 | 49 | Oh, don't be such a prude. There is little need\n |
| 0x146aa7 | 43 | for modesty in a relationship such as ours. |
| 0x146ad3 | 47 | And what kind of relationship is that, exactly? |
| 0x146b03 | 45 | We partook of that roasted meat together at\n |
| 0x146b31 | 18 | that market stall. |
| 0x146b44 | 32 | You ate all of that by yourself! |
| 0x146b65 | 13 | Bah. Details. |
| 0x146b73 | 46 | You're the princess! You can get any kind of\n |
| 0x146ba2 | 42 | food you want. How did you become such a\n |
| 0x146bcd | 8 | glutton? |
| 0x146bd6 | 45 | Don't be such a fool. I'll have you know my\n |
| 0x146c04 | 47 | diet has been strictly regimented since I was\n |
| 0x146c34 | 7 | a baby. |
| 0x146c3c | 46 | Constant admonishing, 'eat your vegetables,'\n |
| 0x146c6b | 42 | 'eating too much is bad for you,' 'avoid\n |
| 0x146c96 | 10 | sweets'... |
| 0x146ca1 | 44 | When I expressed my desire to sample those\n |
| 0x146cce | 47 | skewers, they said 'vulgar' food is unfit for\n |
| 0x146cfe | 3 | me. |
| 0x146d02 | 49 | Huh, so they're raising her a lot more properly\n |
| 0x146d34 | 44 | than I thought. I figured she'd be spoiled\n |
| 0x146d61 | 5 | more. |
| 0x146d67 | 48 | They nag so much, is it any wonder I leave the\n |
| 0x146d98 | 45 | palace behind when the opportunity presents\n |
| 0x146dc6 | 7 | itself? |
| 0x146dce | 46 | This place has no one to chide me, and I can\n |
| 0x146dfd | 45 | eat all the things I've never been able to.\n |
| 0x146e2b | 14 | It's paradise. |
| 0x146e3a | 35 | It's not an all-you-can-eat buffet! |
| 0x146e5e | 47 | Oh, very well. If you desire a reward, I will\n |
| 0x146e8e | 44 | bestow it upon you--IF you fetch me seconds. |
| 0x146ebb | 49 | Once more, she produces that fine gold necklace\n |
| 0x146eed | 29 | of hers, studded with jewels. |
| 0x146f0b | 34 | I thought I told you to stop that. |
| 0x146f2e | 48 | ...I guess it can't be helped. Rulutieh, could\n |
| 0x146f5f | 3 | y-- |
| 0x146f63 | 48 | How... I hid it so carefully... So she'd never\n |
| 0x146f94 | 21 | be able to find it... |
| 0x146faa | 9 | Rulutieh? |
| 0x146fb4 | 18 | ...Huh? O-Oh, yes! |
| 0x146fc7 | 24 | Something bothering you? |
| 0x146fe0 | 27 | N-No, it's... it's nothing. |
| 0x146ffc | 46 | If you say so. I'm sorry to ask this of you,\n |
| 0x14702b | 31 | but could you get us something? |
| 0x14704b | 43 | It doesn't have to be anything expensive.\n |
| 0x147077 | 45 | I'm sure we have some of that bargain stuff\n |
| 0x1470a5 | 5 | left. |
| 0x1470ab | 43 | U-Um... I don't think it would be proper,\n |
| 0x1470d7 | 26 | considering Lady Anju is-- |
| 0x1470f2 | 48 | What is this 'bargain?' I demand to sample it.\n |
| 0x147123 | 14 | Bring it here. |
| 0x147132 | 47 | You're gonna get fat with all this eating and\n |
| 0x147162 | 36 | lying around you're doing, you know. |
| 0x147187 | 42 | I decide not to hold my tongue, a little\n |
| 0x1471b2 | 42 | irritated at taking orders from this brat. |
| 0x1471dd | 45 | Not to worry. It is quite impossible for me\n |
| 0x14720b | 12 | to grow fat. |
| 0x147218 | 40 | What, do you not gain weight easily or\n |
| 0x147241 | 40 | something? Keep talking like that, and-- |
| 0x14726a | 40 | No, I mean I simply will not grow fat.\n |
| 0x147293 | 48 | I am a Divine Scion, after all, the progeny of\n |
| 0x1472c4 | 33 | the Mikado--not some farm animal. |
| 0x1472e6 | 45 | Mine is an auspicious bloodline. My body is\n |
| 0x147314 | 45 | blessed such that it will forever remain in\n |
| 0x147342 | 10 | peak form. |
| 0x14734d | 42 | What does she mean by that? She seems so\n |
| 0x147378 | 45 | confident about it, I can't bring myself to\n |
| 0x1473a6 | 12 | doubt her... |
| 0x1473b3 | 45 | Though now that you mention it, many of the\n |
| 0x1473e1 | 46 | women at court gossip about how their weight\n |
| 0x147410 | 10 | changes... |
| 0x14741b | 44 | I cannot comprehend why they would concern\n |
| 0x147448 | 37 | themselves with such trivial matters. |
| 0x14746e | 45 | I could probably cut the tension in the air\n |
| 0x14749c | 23 | with a knife right now. |
| 0x1474b4 | 50 | Kuon's smiling, but I can see her eye twitching,\n |
| 0x1474e7 | 48 | and Nekone's lips are shut tighter than a vault. |
| 0x147518 | 47 | I, uhm... I think I'll go get those snacks now. |
| 0x147548 | 46 | Rulutieh seems to sense it, too, and finds a\n |
| 0x147577 | 25 | reason to excuse herself. |
| 0x147591 | 48 | I'll... come with you. I'd feel bad making you\n |
| 0x1475c2 | 16 | do all the work. |
| 0x1475d3 | 15 | Th-Thank you... |
| 0x1475e3 | 43 | After Anju's "never get fat" declaration,\n |
| 0x14760f | 42 | I don't want to be in here with Kuon and\n |
| 0x14763a | 9 | Nekone... |
| 0x147644 | 24 | Excuse me, sir and miss. |
| 0x14765d | 41 | As Rulutieh and I head for the kitchen,\n |
| 0x147687 | 42 | a smooth, composed voice hails us in the\n |
| 0x1476b2 | 9 | corridor. |
| 0x1476bc | 41 | We turn to find a woman approaching us... |
| 0x1476e6 | 50 | Her gaze is cool and collected, and though she's\n |
| 0x147719 | 44 | shorter than me, she FEELS as though she's\n |
| 0x147746 | 8 | looming. |
| 0x14774f | 39 | She's like a quietly towering mountain. |
| 0x147777 | 6 | E-Eh!? |
| 0x14777e | 40 | Who is she? Some new guest at the inn?\n |
| 0x1477a7 | 28 | I haven't seen her around... |
| 0x1477c4 | 47 | My name is Munechika. I'm looking for someone\n |
| 0x1477f4 | 30 | named Haku. Have you seen him? |
| 0x147813 | 33 | That'd be me. How can I help you? |
| 0x147835 | 48 | Ah, I thought so. Lord Oshtor instructed me to\n |
| 0x147866 | 14 | find you here. |
| 0x147875 | 40 | By Oshtor? Wait a minute. Munechika...\n |
| 0x14789e | 29 | Where have I heard that name? |
| 0x1478bc | 50 | She knows Oshtor and carries an immense presence\n |
| 0x1478ef | 45 | like this... She can't be an ordinary person. |
| 0x14791d | 7 | U-Um... |
| 0x147925 | 51 | M-May I... i-if it's all right with you, may I...\n |
| 0x147959 | 22 | shake your hand, miss? |
| 0x147970 | 3 | Hm? |
| 0x147974 | 31 | Oh... I-I mean... never mind... |
| 0x147994 | 38 | I'm not so lofty as all that, child.\n |
| 0x1479bb | 18 | Of course you may. |
| 0x1479ce | 48 | Munechika offers her hand to Rulutieh, smiling\n |
| 0x1479ff | 9 | politely. |
| 0x147a09 | 16 | Ah... Thank you. |
| 0x147a1a | 43 | Clearly still a little hesitant, Rulutieh\n |
| 0x147a46 | 16 | shakes her hand. |
| 0x147a57 | 17 | Someone you know? |
| 0x147a69 | 35 | Yes, she's... someone I look up to. |
| 0x147a8d | 48 | Someone Rulutieh looks up to who knows Oshtor.\n |
| 0x147abe | 22 | Is she someone famous? |
| 0x147ad5 | 43 | I've come to escort the exalted personage\n |
| 0x147b01 | 47 | currently taking refuge in this Hakurokaku Inn. |
| 0x147b31 | 43 | I trust you understand what I mean by that? |
| 0x147b5d | 25 | Exalted personage, huh... |
| 0x147b77 | 43 | Well, she's undoubtedly talking about the\n |
| 0x147ba3 | 24 | princess. What to do...? |
| 0x147bbc | 48 | She did say Oshtor sent her, but taking her at\n |
| 0x147bed | 38 | her word without checking could have\n |
| 0x147c14 | 13 | consequences. |
| 0x147c22 | 43 | After all, Anju is the imperial princess.\n |
| 0x147c4e | 44 | If she's kidnapped or killed on our watch,\n |
| 0x147c7b | 13 | it's on us... |
| 0x147c89 | 13 | Then again... |
| 0x147c97 | 49 | Rulutieh, I'll guide her to the room. Would you\n |
| 0x147cc9 | 46 | mind going to get the snacks from the kitchen? |
| 0x147cf8 | 14 | Oh, of course! |
| 0x147d07 | 45 | It doesn't feel as though this Munechika is\n |
| 0x147d35 | 47 | scheming anything. And if Rulutieh recognizes\n |
| 0x147d65 | 6 | her... |
| 0x147d6c | 47 | To be honest, I don't care who she is as long\n |
| 0x147d9c | 47 | as she takes this little gremlin off our hands. |
| 0x147dcc | 30 | Ah, you've returned already,\n |
| 0x147deb | 10 | Ha--aahh!? |
| 0x147df6 | 17 | Why so surprised? |
| 0x147e08 | 13 | But that's... |
| 0x147e16 | 49 | Don't worry about it. I found a solution to all\n |
| 0x147e48 | 13 | our troubles. |
| 0x147e56 | 18 | Huh? What do you-- |
| 0x147e69 | 18 | Please, excuse me. |
| 0x147e7c | 15 | ...Ehh heh heh. |
| 0x147e8c | 19 | Bweh heh heh heh... |
| 0x147ea0 | 48 | And this is supposed to be the princess of the\n |
| 0x147ed1 | 9 | empire... |
| 0x147edb | 49 | I'm glad to see you safe and evidently enjoying\n |
| 0x147f0d | 24 | yourself, Your Highness. |
| 0x147f26 | 6 | Bweh!? |
| 0x147f2d | 34 | Anju immediately freezes in place. |
| 0x147f50 | 49 | Though that slovenly smile remains plastered on\n |
| 0x147f82 | 40 | her face, she begins to sweat profusely. |
| 0x147fab | 18 | It... cannot be... |
| 0x147fbe | 43 | She slowly shifts her head to look at us... |
| 0x147fea | 10 | AAAAHHHH!! |
| 0x147ff5 | 41 | The next moment, she scrambles into the\n |
| 0x14801f | 46 | nearest corner of the room and cowers in fear. |
| 0x14804e | 38 | M-M-Munechika!? What are you doing h-- |
| 0x148075 | 40 | I could ask you the same, Your Highness. |
| 0x14809e | 49 | I prepared a suitably fulfilling curriculum for\n |
| 0x1480d0 | 47 | you to study in my absence. Instead, you came\n |
| 0x148100 | 7 | Urgh... |
| 0x148108 | 34 | You did promise me, Your Highness. |
| 0x14812b | 4 | Eep! |
| 0x148130 | 45 | And you abandon all of it just to sink into\n |
| 0x14815e | 32 | this sort of debauched behavior? |
| 0x14817f | 7 | Ahhh... |
| 0x148187 | 47 | S-Someone! Assassin! A brigand threatens your\n |
| 0x1481b7 | 30 | princess's life! Someone help! |
| 0x1481d6 | 31 | ...What the hell is she saying? |
| 0x1481f6 | 46 | I can all but feel everyone else in the room\n |
| 0x148225 | 48 | sharing the same thought: this girl is hopeless. |
| 0x148256 | 47 | Her behavior reminds me of when Haku tries to\n |
| 0x148286 | 46 | contrive excuses to Kuon for his slacking off. |
| 0x1482b5 | 6 | Urk... |
| 0x1482bc | 47 | Unperturbed by Anju's outcry, Munechika muses\n |
| 0x1482ec | 19 | quietly to herself. |
| 0x148300 | 46 | I'm afraid I see no assassin, Your Highness.\n |
| 0x14832f | 27 | Or are you referring to me? |
| 0x14834b | 4 | Ulp. |
| 0x148350 | 42 | Your jokes go too far, princess. As your\n |
| 0x14837b | 47 | governess, I think some discipline is in order. |
| 0x1483ab | 46 | I-It was just a jape! A jest! I promise, I--\n |
| 0x1483da | 32 | stay away!! Away with you, you-- |
| 0x1483fb | 47 | HAKU!! What are you doing? I c-command you to\n |
| 0x14842b | 31 | rescue me from this entrapment! |
| 0x14844b | 41 | Yeah, discipline's an important part of\n |
| 0x148475 | 46 | teaching. You do what you gotta do, Munechika. |
| 0x1484a4 | 29 | You dare betray me, y--bwah!! |
| 0x1484c2 | 48 | Munechika seizes Anju midsentence and puts the\n |
| 0x1484f3 | 26 | girl firmly over her knee. |
| 0x14850e | 38 | S-Stop! Desist! I-I'll apologize, so-- |
| 0x148535 | 32 | Gyaaaaaaaaaaaaaaaaaaaaaaaaaaaa!! |
| 0x148556 | 43 | Kiwru's expression is of pure anguish and\n |
| 0x148582 | 8 | despair. |
| 0x14858b | 47 | Nekone seems emotionless at first glance, but\n |
| 0x1485bb | 41 | the corners of her mouth are definitely\n |
| 0x1485e5 | 9 | raised... |
| 0x1485ef | 46 | I'm pretty sure she's deriving a "serves you\n |
| 0x14861e | 42 | right" sort of satisfaction from all this. |
| 0x148649 | 48 | Just how protective of Oshtor is she, that she\n |
| 0x14867a | 46 | has THIS attitude toward the princess of the\n |
| 0x1486a9 | 7 | empire? |
| 0x1486b1 | 50 | And for some reason, Kuon is wincing, looking on\n |
| 0x1486e4 | 41 | with a grimace of... unexpected sympathy. |
| 0x14870e | 42 | The fur on her tail stands on end as she\n |
| 0x148739 | 22 | watches Anju's fate... |
| 0x148750 | 46 | Why is SHE so worked up? It's not like she's\n |
| 0x14877f | 25 | the one getting punished. |
| 0x148799 | 45 | Probably not something entirely appropriate\n |
| 0x1487c7 | 17 | to ask right now. |
| 0x1487d9 | 40 | Hello, loves! I heard it was snack time! |
| 0x148802 | 9 | ...erm... |
| 0x14880c | 42 | Atuy throws open the door with the worst\n |
| 0x148837 | 43 | possible timing, freezing at the threshold. |
| 0x148863 | 47 | I'm sorry to make you all wait. I have snacks\n |
| 0x148893 | 29 | and... tea for... everyone... |
| 0x1488b1 | 44 | Rulutieh, returning from the kitchen, also\n |
| 0x1488de | 39 | freezes in place when she sees what's\n |
| 0x148906 | 12 | transpiring. |
| 0x148913 | 26 | This is just farcical now. |
| 0x14892e | 49 | We've treated the princess pretty poorly, sure,\n |
| 0x148960 | 35 | but this is on a whole other level. |
| 0x148984 | 21 | Urgh... my stomach... |
| 0x14899a | 42 | So, uh, you're the princess's governess?\n |
| 0x1489c5 | 37 | In charge of her education and stuff? |
| 0x1489eb | 43 | Unworthy as I am, my liege has regardless\n |
| 0x148a17 | 42 | appointed me to be caretaker of his only\n |
| 0x148a42 | 9 | daughter. |
| 0x148a4c | 17 | Ungh... urrrgh... |
| 0x148a5e | 43 | Anju writhes on the ground nearby, feebly\n |
| 0x148a8a | 31 | curling up in temporary defeat. |
| 0x148aaa | 44 | Why did you let her in...? I commanded you\n |
| 0x148ad7 | 45 | t-to tell me when unknown visitors arrived... |
| 0x148b05 | 45 | Anju glares reproachfully at us as she says\n |
| 0x148b33 | 5 | this. |
| 0x148b39 | 43 | M-My utmost apologies, princess, but, ah... |
| 0x148b65 | 43 | Your orders were to "inform you if Oshtor\n |
| 0x148b91 | 41 | arrives." You didn't say anything about\n |
| 0x148bbb | 17 | Lady Munechika... |
| 0x148bcd | 42 | Ggghhkk. You will regret this. All of you! |
| 0x148bf8 | 48 | She continues to glare at us, hot tears in her\n |
| 0x148c29 | 5 | eyes. |
| 0x148c2f | 10 | *Groan*... |
| 0x148c3a | 7 | Ungh... |
| 0x148c42 | 43 | Kiwru's sensitive stomach contorts audibly. |
| 0x148c6e | 46 | Now, Your Highness, let us away to the palace. |
| 0x148c9d | 30 | N-No. I do not wish to return. |
| 0x148cbc | 21 | You can't be serious. |
| 0x148cd2 | 36 | Your Highness, I cannot brook such\n |
| 0x148cf7 | 15 | disobedience... |
| 0x148d07 | 41 | I'll die of boredom if I return to that\n |
| 0x148d31 | 15 | wretched place! |
| 0x148d41 | 45 | There's no one to talk to, no fun books, no\n |
| 0x148d6f | 16 | snacks--nothing! |
| 0x148d80 | 22 | I wish to remain here. |
| 0x148d97 | 47 | The imperial palace's library is stocked with\n |
| 0x148dc7 | 48 | literature old and new, princess. You know this. |
| 0x148df8 | 48 | Many would gladly entertain you, and your food\n |
| 0x148e29 | 40 | is but the finest. I'm afraid I do not\n |
| 0x148e52 | 11 | understand. |
| 0x148e5e | 45 | If you are dissatisfied with your environs,\n |
| 0x148e8c | 45 | all you need do is say so. Your wish is our\n |
| 0x148eba | 8 | command. |
| 0x148ec3 | 22 | That is not the issue! |
| 0x148eda | 47 | Your "literature" is dull, and I'd sooner die\n |
| 0x148f0a | 36 | than endure the courtiers' droning\n |
| 0x148f2f | 14 | conversations! |
| 0x148f3e | 48 | Even the food! No matter how fine its quality,\n |
| 0x148f6f | 45 | if I cannot eat it freely, what is the point? |
| 0x148f9d | 45 | That is the nature of the life the imperial\n |
| 0x148fcb | 19 | princess must lead. |
| 0x148fdf | 43 | I wish to live more freely than this, then! |
| 0x14900b | 51 | That is a privilege you cannot have. As princess,\n |
| 0x14903f | 42 | you trade freedom for rule. You know this. |
| 0x14906a | 8 | Rrrgh... |
| 0x149073 | 43 | Why must you be so maddeningly difficult?\n |
| 0x14909f | 43 | This must be why you haven't found a husb-- |
| 0x1490cb | 9 | *Swsh*... |
| 0x1490d5 | 43 | Without a word, Munechika raises her hand\n |
| 0x149101 | 14 | threateningly. |
| 0x149110 | 47 | Anju dives under a blanket and begins to shake. |
| 0x149140 | 36 | I just felt a chill down my spine... |
| 0x149165 | 29 | There, there, Miss Munechika. |
| 0x149183 | 46 | Kuon seems to feel sorry for Anju--somehow--\n |
| 0x1491b2 | 13 | and steps in. |
| 0x1491c0 | 44 | She's at an age where she wants to explore\n |
| 0x1491ed | 33 | new horizons. It can't be helped. |
| 0x14920f | 34 | Oh! So you understand my feelings! |
| 0x149232 | 49 | I can tell you must take excellent care of her,\n |
| 0x149264 | 46 | but sometimes being overprotective can stifle. |
| 0x149293 | 23 | Yes, exactly! Tell her! |
| 0x1492ab | 47 | In a stiff environment where she's being bred\n |
| 0x1492db | 45 | for politics, is it any wonder she tries to\n |
| 0x149309 | 10 | sneak out? |
| 0x149314 | 49 | If I were in her situation as a child, I'd have\n |
| 0x149346 | 23 | done the same, I think. |
| 0x14935e | 12 | Miss Kuon... |
| 0x14936b | 14 | Dear sister... |
| 0x14937a | 43 | Yeah, she's right. Court life gets really\n |
| 0x1493a6 | 41 | boring. All your friends treat you with\n |
| 0x1493d0 | 15 | caution, too... |
| 0x1493e0 | 39 | You really understand, don't you, Kuon? |
| 0x149408 | 44 | Huh? Erm... y-yes. Just a little, I suppose. |
| 0x149435 | 10 | You are... |
| 0x149440 | 36 | Anju looks at Kuon with watery eyes. |
| 0x149465 | 48 | You are truly a good person. I had no inkling... |
| 0x149496 | 3 | Eh? |
| 0x14949a | 47 | I admit I had difficulty in trying to discern\n |
| 0x1494ca | 42 | your intentions. I took you for a shady,\n |
| 0x1494f5 | 16 | secretive woman. |
| 0x149506 | 46 | But rejoice! I shall bestow on you the honor\n |
| 0x149535 | 26 | of being called my friend. |
| 0x149550 | 41 | I understand what you're trying to say.\n |
| 0x14957a | 48 | This behavior may be excusable for a commoner,\n |
| 0x1495ab | 6 | yes... |
| 0x1495b2 | 41 | But there is one, and ONLY one imperial\n |
| 0x1495dc | 47 | princess. She must keep her dignity if she is\n |
| 0x14960c | 8 | to rule. |
| 0x149615 | 45 | To that end, it is imperative she continues\n |
| 0x149643 | 48 | attending her daily studies and learns courtly\n |
| 0x149674 | 5 | arts. |
| 0x14967a | 49 | Only a truly wise ruler, sensitive to the needs\n |
| 0x1496ac | 44 | of the people, can be called fit to govern\n |
| 0x1496d9 | 7 | Yamato. |
| 0x1496e1 | 9 | That's... |
| 0x1496eb | 38 | Urgh... It's as if I'm listening to... |
| 0x149712 | 7 | To who? |
| 0x14971a | 25 | Um, n-never mind. No one. |
| 0x149734 | 42 | What is the matter? Tell her she is wrong! |
| 0x14975f | 48 | I, uh. Don't have a good argument against that\n |
| 0x149790 | 11 | one. Sorry. |
| 0x14979c | 46 | The feeling she gives off is... the kind I'm\n |
| 0x1497cb | 19 | not very good with. |
| 0x1497df | 7 | Really? |
| 0x1497e7 | 48 | Hard to believe even Kuon's unflappability has\n |
| 0x149818 | 11 | its limits. |
| 0x149824 | 48 | Bah. After all I have done, you remain useless\n |
| 0x149855 | 6 | to me. |
| 0x14985c | 13 | Ah, princess? |
| 0x14986a | 46 | Kuon smiles pleasantly, reaching toward Anju\n |
| 0x149899 | 16 | with one hand... |
| 0x1498aa | 47 | I think you should learn to watch that little\n |
| 0x1498da | 15 | mouth of yours. |
| 0x1498ea | 45 | She squeezes Anju's cheek and begins pulling. |
| 0x149918 | 13 | *Tug, tug*... |
| 0x149926 | 27 | Brghah? Vhat are oo voing!? |
| 0x149942 | 47 | You said we're friends now, right? So there's\n |
| 0x149972 | 45 | no need for me to continue being so reserved. |
| 0x1499a0 | 47 | After all, friends aren't shogi tiles for you\n |
| 0x1499d0 | 49 | to command or dolls to manipulate. We're equals\n |
| 0x149a02 | 4 | now! |
| 0x149a07 | 12 | How VARE oo! |
| 0x149a14 | 46 | Anju reaches for Kuon's face and pinches her\n |
| 0x149a43 | 14 | cheek in turn. |
| 0x149a52 | 6 | Hyeh!? |
| 0x149a59 | 9 | Grrr...!! |
| 0x149a63 | 3 | Hm. |
| 0x149a67 | 46 | Munechika rubs her chin, watching the two of\n |
| 0x149a96 | 14 | them struggle. |
| 0x149aa5 | 8 | U-Umm... |
| 0x149aae | 49 | Would you like some tea? It will get cold if we\n |
| 0x149ae0 | 18 | wait any longer... |
| 0x149af3 | 48 | Rulutieh offers Munechika the tray she's still\n |
| 0x149b24 | 9 | carrying. |
| 0x149b2e | 49 | Good girl Rulutieh. Even amidst this chaos, she\n |
| 0x149b60 | 43 | remains polite and hospitable in the storm. |
| 0x149b8c | 45 | Kiwru still looks like he's pulling himself\n |
| 0x149bba | 46 | back together, but Rulutieh composed herself\n |
| 0x149be9 | 8 | quickly. |
| 0x149bf2 | 41 | Chalk it up to girls having more mental\n |
| 0x149c1c | 29 | fortitude than guys, I guess. |
| 0x149c3a | 16 | Thank you, dear. |
| 0x149c4b | 39 | Munechika accepts a cup, then lifts a\n |
| 0x149c73 | 47 | confectionary from the tray and takes a small\n |
| 0x149ca3 | 7 | bite... |
| 0x149cab | 6 | *Gasp* |
| 0x149cb2 | 46 | In that instant, her eyes snap wide, and she\n |
| 0x149ce1 | 47 | looks down at the little cake with wonder and\n |
| 0x149d11 | 4 | awe. |
| 0x149d16 | 10 | This is... |
| 0x149d21 | 48 | She quickly begins pushing more into her mouth\n |
| 0x149d52 | 8 | eagerly. |
| 0x149d5b | 15 | *Hromf, nomf--* |
| 0x149d6b | 49 | The mountain of sweets prepared for Anju begins\n |
| 0x149d9d | 38 | to grow smaller by Munechika's hand... |
| 0x149dc4 | 36 | Eh!? What are you doing, you fool?\n |
| 0x149de9 | 23 | Those are meant for me! |
| 0x149e01 | 49 | The princess releases Kuon's cheek to rush over\n |
| 0x149e33 | 13 | to Munechika. |
| 0x149e41 | 50 | The rest of the room stands dumbstruck, watching\n |
| 0x149e74 | 37 | as the farce continues to play out... |
| 0x149e9a | 12 | *Tap, tap--* |
| 0x149ea7 | 29 | So, what do you intend to do? |
| 0x149ec5 | 11 | About what? |
| 0x149ed1 | 43 | All of it. Everything. The princess, Lady\n |
| 0x149efd | 12 | Munechika... |
| 0x149f0a | 32 | You're asking ME for a solution? |
| 0x149f2b | 47 | This behavior is unheard-of. I expect it from\n |
| 0x149f5b | 33 | the princess, but Lady Munechika? |
| 0x149f7d | 46 | Speaking of her--is she famous or something?\n |
| 0x149fac | 48 | Rulutieh seemed pretty worked up about meeting\n |
| 0x149fdd | 48 | What nonsense are you spouting now? Surely you\n |
| 0x14a00e | 43 | know she's not just a glorified babysitter. |
| 0x14a03a | 46 | Lady Munechika of the Eight Pillar Generals?\n |
| 0x14a069 | 45 | The Mikado appointed her as Guardian himself. |
| 0x14a097 | 46 | Oh, right! No wonder I thought I'd heard her\n |
| 0x14a0c6 | 14 | name before... |
| 0x14a0d5 | 44 | I would have thought it impossible to find\n |
| 0x14a102 | 45 | anyone in the capital who does not know her\n |
| 0x14a130 | 5 | name. |
| 0x14a136 | 49 | Now that I think on it, I wasn't really able to\n |
| 0x14a168 | 44 | get a good look at her during the nativity\n |
| 0x14a195 | 9 | festival. |
| 0x14a19f | 34 | Now, Your Highness. Let us return. |
| 0x14a1c2 | 16 | No. I shall not. |
| 0x14a1d3 | 18 | Never. Never EVER. |
| 0x14a1e6 | 49 | Very well. If that is the case, I will take you\n |
| 0x14a218 | 22 | back by force if I m-- |
| 0x14a22f | 49 | Wait, wait! Please. There is much I have yet to\n |
| 0x14a261 | 22 | learn from this place! |
| 0x14a278 | 43 | A creditable endeavor, princess, but your\n |
| 0x14a2a4 | 45 | studies are just as easily furthered in the\n |
| 0x14a2d2 | 8 | palace-- |
| 0x14a2db | 49 | Look, Munechika. Behold a wonder. Have you ever\n |
| 0x14a30d | 43 | seen such a book within the palace library? |
| 0x14a339 | 39 | What!? H-How did she find THAT one too? |
| 0x14a361 | 6 | Hm...? |
| 0x14a368 | 48 | Munechika takes the book Anju is proffering to\n |
| 0x14a399 | 47 | She opens it and begins to skim its contents... |
| 0x14a3c9 | 50 | ...and as she turns the pages, she stares deeper\n |
| 0x14a3fc | 39 | and deeper into them, totally absorbed. |
| 0x14a424 | 47 | See--are the depths of friendship between two\n |
| 0x14a454 | 43 | men not arresting? The palace has no such\n |
| 0x14a480 | 8 | books... |
| 0x14a489 | 7 | This... |
| 0x14a491 | 46 | You see now. I do not come to this place for\n |
| 0x14a4c0 | 32 | mere distraction and indulgence. |
| 0x14a4e1 | 45 | I come here that I might broaden my horizons. |
| 0x14a50f | 45 | There lies an abundance of knowledge I fear\n |
| 0x14a53d | 45 | I can find nowhere within the palace walls... |
| 0x14a56b | 46 | That's definitely not what you were saying a\n |
| 0x14a59a | 16 | minute ago, kid. |
| 0x14a5ab | 33 | I... see. I believe I understand. |
| 0x14a5cd | 45 | I am moved by your passion to find learning\n |
| 0x14a5fb | 41 | experiences in all things, Your Highness. |
| 0x14a625 | 41 | ...Didn't take much to convince her, huh. |
| 0x14a64f | 21 | Ah! Then that means-- |
| 0x14a665 | 44 | I will inform my liege of your devotion to\n |
| 0x14a692 | 45 | practical studies, learning from the common\n |
| 0x14a6c0 | 7 | folk... |
| 0x14a6c8 | 26 | Yes. Well said, Munechika. |
| 0x14a6e3 | 44 | Now, if you'd kindly return that book to m-- |
| 0x14a710 | 40 | I'm afraid I will be confiscating this\n |
| 0x14a739 | 33 | particular volume, Your Highness. |
| 0x14a75b | 41 | She quickly pockets the offending book,\n |
| 0x14a785 | 18 | secreting it away. |
| 0x14a798 | 6 | What!? |
| 0x14a79f | 45 | I will return it after discerning FIRSTHAND\n |
| 0x14a7cd | 45 | which parts are too... stimulating for Your\n |
| 0x14a7fb | 9 | Highness. |
| 0x14a805 | 35 | U-um... that book is... actually... |
| 0x14a829 | 43 | Give it back. Return it to me this instant! |
| 0x14a855 | 48 | On another note, this confection you've served\n |
| 0x14a886 | 22 | me is truly exquisite. |
| 0x14a89d | 43 | She coolly turns away from Anju to sample\n |
| 0x14a8c9 | 33 | another one of Rulutieh's sweets. |
| 0x14a8eb | 41 | Do not think to change the subject now!\n |
| 0x14a915 | 28 | Give back my book forthwith! |
| 0x14a932 | 29 | Actually... it's, uh... my... |
| 0x14a950 | 21 | My stomach... unhh... |
| 0x14a966 | 46 | Poor Kiwru has been doubled over this entire\n |
| 0x14a995 | 48 | time. Rulutieh looks to be at a loss, tears in\n |
| 0x14a9c6 | 9 | her eyes. |
| 0x14a9d0 | 5 | Um... |
| 0x14a9d6 | 46 | Kuon glances toward me with a look that says\n |
| 0x14aa05 | 45 | 'do something,' and Nekone rapidly nods her\n |
| 0x14aa33 | 10 | agreement. |
| 0x14aa3e | 37 | What the hell do you expect ME to do? |
| 0x14aa64 | 43 | Rulie, your cooking is always so delicious! |
| 0x14aa90 | 49 | Atuy joins Munechika, continuing to eat without\n |
| 0x14aac2 | 20 | a care in the world. |
| 0x14aad7 | 27 | Kurarin, you want some too? |
| 0x14aaf3 | 19 | *Jiggle, jiggle*... |
| 0x14ab07 | 44 | Kurarin wobbles in place, looking a little\n |
| 0x14ab34 | 42 | fearful--as if he might be eaten just as\n |
| 0x14ab5f | 7 | easily. |
| 0x14ab67 | 46 | Seriously, what are we going to do about all\n |
| 0x14ab96 | 8 | this...? |
| 0x14c57d | 17 | *Munch, munch*... |
| 0x14c58f | 45 | Everyone is sharing in a freshly-made batch\n |
| 0x14c5bd | 8 | of Rulu. |
| 0x14c5c6 | 23 | Ahh, this is so good... |
| 0x14c5de | 31 | Hee. I think I'll take another. |
| 0x14c5fe | 47 | I doubt I will ever grow tired of this stuff,\n |
| 0x14c62e | 10 | sincerely. |
| 0x14c639 | 45 | "Rulu" has been getting a reputation as the\n |
| 0x14c667 | 48 | Hakurokaku's signature sweet. People come just\n |
| 0x14c698 | 24 | to ask for the recipe... |
| 0x14c6b1 | 43 | As a result, we've been seeing it sold in\n |
| 0x14c6dd | 43 | teahouses around the capital more and more. |
| 0x14c709 | 44 | A-Ah, I've made some tea if you'd care for\n |
| 0x14c736 | 6 | any... |
| 0x14c73d | 44 | Aw, that's our Rulie. Always so considerate! |
| 0x14c76a | 42 | You should sit down and have a bite too,\n |
| 0x14c795 | 23 | Rulutieh. Take it easy. |
| 0x14c7ad | 44 | Thank you... Oh, but do you want any milk,\n |
| 0x14c7da | 12 | before I...? |
| 0x14c7e7 | 47 | Rulutieh proffers a jug of milk--an essential\n |
| 0x14c817 | 31 | part of drinking tea in Yamato. |
| 0x14c837 | 14 | Sure, I guess. |
| 0x14c846 | 48 | I take the jug and pour a helping into my tea... |
| 0x14c877 | 28 | Thanks. Anyone else want it? |
| 0x14c894 | 13 | In the end... |
| 0x14c8a2 | 31 | I consider the Rulu in my hand. |
| 0x14c8c2 | 48 | In the end, this was a success and all, but we\n |
| 0x14c8f3 | 41 | failed in our original goal of making a\n |
| 0x14c91d | 10 | sweetener. |
| 0x14c928 | 44 | I keep wondering... Why didn't it come out\n |
| 0x14c955 | 24 | like we wanted it to...? |
| 0x14c96e | 49 | Didn't you say something about it burning every\n |
| 0x14c9a0 | 15 | time you tried? |
| 0x14c9b0 | 46 | You didn't experiment with the distance from\n |
| 0x14c9df | 47 | the fire, perhaps tried to boil it in water...? |
| 0x14ca0f | 42 | We tried, but it just took too long. The\n |
| 0x14ca3a | 46 | temperature never got high enough with those\n |
| 0x14ca69 | 8 | methods. |
| 0x14ca72 | 48 | There might be a perfect, optimum temperature,\n |
| 0x14caa3 | 45 | but we can't get that much control out of a\n |
| 0x14cad1 | 9 | cookfire. |
| 0x14cadb | 49 | We might need an entirely new approach to this.\n |
| 0x14cb0d | 44 | What if we cool it instead of heating? No,\n |
| 0x14cb3a | 6 | ugh... |
| 0x14cb41 | 4 | Hey. |
| 0x14cb46 | 3 | Hm? |
| 0x14cb4a | 37 | The stuff that sinks to the bottom.\n |
| 0x14cb70 | 24 | That doesn't burn, yeah? |
| 0x14cb89 | 11 | Well, no... |
| 0x14cb95 | 34 | Can't you just heat that up, then? |
| 0x14cbb8 | 41 | We mixed in amam powder to draw out the\n |
| 0x14cbe2 | 47 | bitterness, so all we'd get from that is more\n |
| 0x14cc12 | 7 | Rulu... |
| 0x14cc1a | 50 | At Atuy's words, however, a flash of inspiration\n |
| 0x14cc4d | 11 | strikes me. |
| 0x14cc59 | 48 | The stuff that goes to the bottom, it's mostly\n |
| 0x14cc8a | 14 | amam powder... |
| 0x14cc99 | 5 | Atuy. |
| 0x14cc9f | 4 | Yes? |
| 0x14cca4 | 48 | You have my permission to eat three times what\n |
| 0x14ccd5 | 17 | you usually take. |
| 0x14cce7 | 11 | S-Sir Haku? |
| 0x14ccf3 | 44 | That's it. What you said is exactly right,\n |
| 0x14cd20 | 46 | The part that sinks doesn't burn because the\n |
| 0x14cd4f | 41 | additive is PREVENTING it from burning... |
| 0x14cd79 | 3 | Oh! |
| 0x14cd7d | 44 | Recognition sparks in Rulutieh's eyes. She\n |
| 0x14cdaa | 42 | seems to understand even before I finish\n |
| 0x14cdd5 | 11 | explaining. |
| 0x14cde1 | 42 | Th-Then... if we were to find a suitable\n |
| 0x14ce0c | 38 | additive for the supernatant liquid... |
| 0x14ce33 | 44 | It's definitely worth exploring. Let's try\n |
| 0x14ce60 | 38 | experimenting with amam powder, first. |
| 0x14ce87 | 9 | Y-Yes...! |
| 0x14ce91 | 47 | Interesting. Just as we suspected, cooking it\n |
| 0x14cec1 | 43 | with an additive mixed in doesn't burn it\n |
| 0x14ceed | 7 | at all. |
| 0x14cef5 | 48 | But I guess using amam powder makes the flavor\n |
| 0x14cf26 | 27 | a little bland, doesn't it? |
| 0x14cf42 | 48 | It does become a little lackluster next to the\n |
| 0x14cf73 | 40 | Rulu... but we still need to kill that\n |
| 0x14cf9c | 11 | bitterness. |
| 0x14cfa8 | 44 | There's gotta be something we can add that\n |
| 0x14cfd5 | 26 | won't change the flavor... |
| 0x14cff0 | 48 | The extra flavor is excessive, right? So maybe\n |
| 0x14d021 | 38 | if you try balancing it out instead... |
| 0x14d048 | 46 | Balance it out? What, like add something else? |
| 0x14d077 | 49 | I see... I was concentrating on diminishing the\n |
| 0x14d0a9 | 41 | bitterness, but if I add something else\n |
| 0x14d0d3 | 10 | instead... |
| 0x14d0de | 31 | But what kind of flavor to add? |
| 0x14d0fe | 47 | I glance toward Rulutieh, thinking carefully... |
| 0x14d12e | 49 | Wait a minute. The milk she brought for the tea\n |
| 0x14d160 | 10 | earlier... |
| 0x14d16b | 7 | U-Um... |
| 0x14d173 | 42 | Rulutieh fidgets as my eyes fall on her,\n |
| 0x14d19e | 10 | flustered. |
| 0x14d1a9 | 10 | That's it! |
| 0x14d1b4 | 7 | Y-Yes!? |
| 0x14d1bc | 31 | That milk jug you had before.\n |
| 0x14d1dc | 26 | Could you bring that here? |
| 0x14d1f7 | 45 | The... milk? Y-Yes, I'll get it right away... |
| 0x14d225 | 44 | Rulutieh nods and retrieves the jug quickly. |
| 0x14d252 | 44 | Good. Now, mix that in with the supernatant. |
| 0x14d27f | 15 | U-Understood... |
| 0x14d28f | 44 | Rulutieh follows my instructions and pours\n |
| 0x14d2bc | 46 | slowly, stirring in the milk while heating it. |
| 0x14d2eb | 27 | Good. Now, mix it evenly... |
| 0x14d307 | 8 | Y-Yes... |
| 0x14d310 | 49 | Everyone crowds around to watch our experiment,\n |
| 0x14d342 | 10 | intrigued. |
| 0x14d34d | 48 | The resulting new mixture begins to bubble and\n |
| 0x14d37e | 14 | boil softly... |
| 0x14d38d | 50 | Ah, this smells much sweeter than anything we've\n |
| 0x14d3c0 | 16 | produced so far. |
| 0x14d3d1 | 32 | Y-Yes, it's a very nice scent... |
| 0x14d3f2 | 23 | Mind if I take a taste? |
| 0x14d40a | 9 | Oh, ah... |
| 0x14d414 | 44 | Impatient, Kuon steps forward and dips her\n |
| 0x14d441 | 28 | finger into the boiling pot. |
| 0x14d45e | 49 | Hey, easy--you're gonna burn yourself if you're\n |
| 0x14d490 | 11 | not caref-- |
| 0x14d49c | 43 | Unperturbed and unburnt, Kuon scoops up a\n |
| 0x14d4c8 | 39 | fingerful of the mix like it's nothing. |
| 0x14d4f0 | 47 | She licks her finger clean without so much as\n |
| 0x14d520 | 11 | hesitating. |
| 0x14d52c | 22 | Oh, wow. That's tasty. |
| 0x14d543 | 7 | Really? |
| 0x14d54b | 48 | Atuy follows suit, dipping her finger--wincing\n |
| 0x14d57c | 47 | a little at the heat--and sampling the mixture. |
| 0x14d5ac | 19 | Oohh, that IS good! |
| 0x14d5c0 | 47 | She proceeds to suck every last drop from her\n |
| 0x14d5f0 | 7 | finger. |
| 0x14d5f8 | 42 | At Atuy and Kuon's reactions, Nekone and\n |
| 0x14d623 | 22 | Rulutieh step forward. |
| 0x14d63a | 10 | Tch, hot-- |
| 0x14d645 | 48 | That's what you get for trying to take so much\n |
| 0x14d676 | 8 | at once. |
| 0x14d67f | 28 | Oww. But it looks so good... |
| 0x14d69c | 27 | ...so soft and delicious... |
| 0x14d6b8 | 13 | Here, Nekone. |
| 0x14d6c6 | 15 | Dear sister...? |
| 0x14d6d6 | 50 | As Nekone nurses her burnt hand, Kuon offers her\n |
| 0x14d709 | 27 | a freshly re-dipped finger. |
| 0x14d725 | 10 | Open wide. |
| 0x14d734 | 46 | Nekone blushes fiercely, but obediently eats\n |
| 0x14d763 | 21 | off of Kuon's finger. |
| 0x14d779 | 24 | Mmf. Ith quite tathty... |
| 0x14d792 | 5 | Good! |
| 0x14d798 | 21 | Care to try it, love? |
| 0x14d7ae | 39 | Atuy playfully dips her finger again,\n |
| 0x14d7d6 | 43 | mimicking Kuon and bringing it to my mouth. |
| 0x14d802 | 24 | Do you really have to... |
| 0x14d81b | 19 | Don't be so modest! |
| 0x14d82f | 8 | Mmmff... |
| 0x14d838 | 46 | She'll probably just shove it in my mouth no\n |
| 0x14d867 | 42 | matter what I say at this point. Ah, well. |
| 0x14d892 | 38 | I steel myself and eat off of Atuy's\n |
| 0x14d8b9 | 20 | outstretched finger. |
| 0x14d8ce | 24 | Mm, that IS pretty good. |
| 0x14d8e7 | 15 | Hee hee, right? |
| 0x14d8f7 | 46 | It has that rich, milky flavor balancing out\n |
| 0x14d926 | 44 | the rest, bringing a smile to everyone who\n |
| 0x14d953 | 11 | tries it... |
| 0x14d95f | 46 | If I were to give this a name... Well, let's\n |
| 0x14d98e | 48 | see. It's made by evaporating the water in the\n |
| 0x14d9bf | 5 | milk. |
| 0x14d9c5 | 31 | So, if it's condensed milk...\n |
| 0x14d9e5 | 3 | Hm. |
| 0x14d9e9 | 11 | Kondens...? |
| 0x14d9f5 | 46 | Rulutieh looks at me, puzzled. Maybe it's an\n |
| 0x14da24 | 16 | unfamiliar term. |
| 0x14da35 | 35 | Sure, kondens. We can call it that. |
| 0x14da59 | 47 | Kondens... a mysterious name for a mysterious\n |
| 0x14da89 | 7 | flavor. |
| 0x14da91 | 49 | Created another notorious sweet to be the pride\n |
| 0x14dac3 | 26 | of the capital, huh, Haku? |
| 0x14dade | 50 | Looks like... And this stuff will actually keep,\n |
| 0x14db11 | 47 | so it would make a good gift to other cities,\n |
| 0x14db41 | 4 | too. |
| 0x14db46 | 33 | Ah, it won't go bad? That's good. |
| 0x14db68 | 46 | If only you stayed in the kitchen instead of\n |
| 0x14db97 | 47 | lazing about. You'd be of much greater use to\n |
| 0x14dbc7 | 11 | the empire. |
| 0x14dbd3 | 49 | Eh, I'm sure it'll line all the stores shelves'\n |
| 0x14dc05 | 47 | soon enough. I'd rather be eating than making\n |
| 0x14dc35 | 3 | it. |
| 0x14dc39 | 45 | With that, I reach for the pot to take some\n |
| 0x14dc67 | 27 | more of the kondens, but... |
| 0x14dc83 | 48 | It's still way too hot. I'm surprised Kuon and\n |
| 0x14dcb4 | 48 | Atuy could just stick their fingers right into\n |
| 0x14dce5 | 49 | Rulutieh seems to notice me hesitating in front\n |
| 0x14dd17 | 25 | of the pot and blushes... |
| 0x14dd31 | 47 | Making up her mind, she holds out her hand to\n |
| 0x14dd61 | 3 | me. |
| 0x14dd65 | 32 | U-Um, I mean--i-if you'd like... |
| 0x14dd86 | 12 | Huh? O-Oh... |
| 0x14dd93 | 50 | I falter for just a moment, but decide to accept\n |
| 0x14ddc6 | 20 | her offer and eat... |
| 0x14dddb | 48 | This stuff tastes a little different each time\n |
| 0x14de0c | 39 | I eat it off of someone else's fingers. |
| 0x14de34 | 43 | I take a glance to the side as I eat from\n |
| 0x14de60 | 18 | Rulutieh's hand... |
| 0x14de75 | 45 | Everyone else in the room is looking at us.\n |
| 0x14dea3 | 8 | Oh, boy. |
| 0x14deac | 35 | I decided to pretend not to notice. |
| 0x14ded0 | 21 | Several days later... |
| 0x14dee6 | 17 | Phew. What a day. |
| 0x14def8 | 44 | All you did was watch us work from the back. |
| 0x14df25 | 29 | Look, I had a lot on my mind. |
| 0x14df43 | 48 | Genius though you may be with confectionaries,\n |
| 0x14df74 | 47 | you are a lazy bum when it comes to your real\n |
| 0x14dfa4 | 4 | job. |
| 0x14dfa9 | 48 | Hey, you know what they say. The right man for\n |
| 0x14dfda | 14 | the right job. |
| 0x14dfe9 | 48 | Why do I get the feeling you are misusing that\n |
| 0x14e01a | 7 | phrase? |
| 0x14e022 | 49 | Nekone sounds exasperated with me, but her mood\n |
| 0x14e054 | 25 | seems to recover quickly. |
| 0x14e06e | 45 | Ah, well. At least there's one thing you've\n |
| 0x14e09c | 22 | done I can appreciate. |
| 0x14e0b3 | 46 | I have something to look forward to treating\n |
| 0x14e0e2 | 26 | myself to after work, now. |
| 0x14e0fd | 49 | Nekone happily opens the door as she says this,\n |
| 0x14e12f | 31 | full of anticipation, to find-- |
| 0x14e14f | 33 | An outrage! This is an outrage!\n |
| 0x14e171 | 22 | Tantamount to treason! |
| 0x14e188 | 5 | What? |
| 0x14e18e | 16 | Y-Your Highness? |
| 0x14e19f | 44 | How dare you keep something so wonderful a\n |
| 0x14e1cc | 15 | secret from me? |
| 0x14e1dc | 49 | Anju paces back and forth, eating greedily from\n |
| 0x14e20e | 24 | a small jar in her arms. |
| 0x14e227 | 26 | Y-You--I was saving that!! |
| 0x14e242 | 47 | Nekone immediately pounces on the jar, trying\n |
| 0x14e272 | 27 | to wrest it away from Anju. |
| 0x14e28e | 6 | Bwah!? |
| 0x14e295 | 44 | Is that... from Nekone's stash of kondens?\n |
| 0x14e2c2 | 25 | How did Anju get into it? |
| 0x14e2dc | 13 | Give it back! |
| 0x14e2ea | 50 | I appreciate your hospitality. Perhaps I'll even\n |
| 0x14e31d | 41 | overlook your tardiness in light of this! |
| 0x14e347 | 49 | Imperial princess you may be, but that does not\n |
| 0x14e379 | 45 | give you the right to take what is not yours! |
| 0x14e3a7 | 47 | Bah. It will find its way to my belly one way\n |
| 0x14e3d7 | 46 | or another. What does it matter if I take it\n |
| 0x14e406 | 4 | now? |
| 0x14e40b | 50 | They shout without listening to a word the other\n |
| 0x14e43e | 33 | has to say, tugging on the jar... |
| 0x14e460 | 43 | Hey, easy--If you keep that up it's gonna-- |
| 0x14e48c | 13 | Nekone & Anju |
| 0x14e49a | 3 | Ah! |
| 0x14e49e | 46 | The jar flies free of Anju's grasp and tips,\n |
| 0x14e4cd | 44 | spilling its contents all over both of them. |
| 0x14e4fa | 7 | Urgh... |
| 0x14e502 | 5 | Ewww. |
| 0x14e508 | 20 | I tried to warn you. |
| 0x14e51d | 19 | What happened here? |
| 0x14e531 | 44 | Kuon arrives to find the mess, laughing to\n |
| 0x14e55e | 8 | herself. |
| 0x14e567 | 47 | Were you two fighting over that little jar of\n |
| 0x14e597 | 48 | kondens? You could have just asked. I have more. |
| 0x14e5c8 | 43 | Kuon's been making it for herself without\n |
| 0x14e5f4 | 11 | telling us? |
| 0x14e600 | 45 | Heh. Judging by the look of things, I guess\n |
| 0x14e62e | 20 | it's pretty popular. |
| 0x14e643 | 46 | As Kuon takes in the scene of the fight, her\n |
| 0x14e672 | 40 | eyes settle on Anju, covered in kondens. |
| 0x14e69b | 45 | That's it! If I advertise that the imperial\n |
| 0x14e6c9 | 46 | princess loves it, it's sure to fetch a high\n |
| 0x14e6f8 | 6 | price. |
| 0x14e6ff | 47 | Kuon grins, pleased with herself, just as she\n |
| 0x14e72f | 48 | had after we created that first batch of Rulu... |
| 0x14e760 | 49 | It doesn't look like there's going to be an end\n |
| 0x14e792 | 28 | to this chaos any time soon. |
| 0x151c2b | 23 | *Ah... ah--AH-BFFFFT--* |
| 0x151c43 | 48 | Kuon's hand claps over my face to interrupt my\n |
| 0x151c74 | 7 | sneeze. |
| 0x151c7c | 5 | Haku? |
| 0x151c82 | 49 | She puts a finger to her lips, telling me to be\n |
| 0x151cb4 | 6 | quiet. |
| 0x151cbb | 25 | Take this more seriously! |
| 0x151cd5 | 38 | Nekone glares at me from her position. |
| 0x151cfc | 46 | What am I supposed to do, NOT sneeze? It's a\n |
| 0x151d2b | 48 | physiological thing. I can't exactly control it. |
| 0x151d5c | 49 | We've been standing here in the cold for hours.\n |
| 0x151d8e | 48 | How can you expect my body NOT to react to that? |
| 0x151dbf | 47 | W-Would, ah... would you like some tea, then?\n |
| 0x151def | 29 | It's cooled off a bit, but... |
| 0x151e0d | 25 | Y-Yeah. That should help. |
| 0x151e27 | 39 | And, ah... would anyone else like some? |
| 0x151e4f | 19 | Mm! Yes, thank you. |
| 0x151e63 | 50 | I'd like some too, if it's not an inconvenience... |
| 0x151e96 | 31 | Ahhh. That really warms you up. |
| 0x151eb6 | 32 | Mm. A sweet, refreshing taste... |
| 0x151ed7 | 50 | Wait, is there honey in this? Is that... Are you\n |
| 0x151f0a | 36 | sure you want to share that with us? |
| 0x151f2f | 49 | Yes! My family specially sent it from our home.\n |
| 0x151f61 | 17 | Please, enjoy it. |
| 0x151f73 | 47 | Aw, Rulie! You're so sweet. If I liked girls,\n |
| 0x151fa3 | 31 | I think I'd be falling for you. |
| 0x151fc7 | 49 | Ah, that really warms me up. Now, for the final\n |
| 0x151ff9 | 8 | touch... |
| 0x152002 | 19 | *Rustle, rustle*... |
| 0x152016 | 49 | I feel around for my "specialty" flask and pull\n |
| 0x152048 | 18 | it from my pocket. |
| 0x15205b | 46 | A drop or two of this, and I'll be warmed up\n |
| 0x15208a | 13 | completely... |
| 0x152098 | 49 | ...I slowly put the flask away when I feel cold\n |
| 0x1520ca | 13 | stares on me. |
| 0x1520d8 | 20 | The dead of night... |
| 0x1520ed | 48 | The sun set hours ago, and even the late-night\n |
| 0x15211e | 42 | city life has given way to silent, empty\n |
| 0x152149 | 8 | streets. |
| 0x152152 | 50 | The days in the capital can get pretty warm, but\n |
| 0x152185 | 32 | it gets just as cold at night... |
| 0x1521a6 | 46 | Just standing here doing nothing, I can feel\n |
| 0x1521d5 | 34 | the chill slowly creeping into me. |
| 0x1521f8 | 46 | God, it's freezing. If we could just light a\n |
| 0x152227 | 20 | fire or something... |
| 0x15223c | 46 | There's nothing we can really do about that.\n |
| 0x15226b | 46 | We're supposed to be keeping watch, after all. |
| 0x15229a | 48 | "Keeping watch," my ass. Nothing is happening!\n |
| 0x1522cb | 42 | Do I even need to be here for this farce?  |
| 0x1522f6 | 48 | A stiff drink really wouldn't go amiss on this\n |
| 0x152327 | 16 | kind of night... |
| 0x152338 | 21 | A notice for a theft? |
| 0x15234e | 45 | Yeah. Y'know that loan shark's office, near\n |
| 0x15237c | 16 | the main street? |
| 0x15238d | 42 | Turns out they got a letter this morning\n |
| 0x1523b8 | 46 | claiming someone's gonna try to rob the place. |
| 0x1523e7 | 47 | Said something about punishing the wicked who\n |
| 0x152417 | 26 | prey on innocent people... |
| 0x152432 | 27 | ...Sounds awfully familiar. |
| 0x15244e | 45 | I probably don't need to tell you, but most\n |
| 0x15247c | 28 | likely it's Nosuri's doing.  |
| 0x152499 | 7 | Nosuri? |
| 0x1524a1 | 23 | Right. Our noble thief. |
| 0x1524b9 | 19 | Yeah. You know 'er. |
| 0x1524cd | 49 | The band of thieves working in the shadows with\n |
| 0x1524ff | 9 | Oshtor... |
| 0x152509 | 43 | It was thanks to them that he was able to\n |
| 0x152535 | 43 | procure evidence of Dekopompo's corruption. |
| 0x152561 | 48 | The way they tell it, they steal from the rich\n |
| 0x152592 | 47 | and corrupt to avenge the poor... or something. |
| 0x1525c2 | 44 | So are we gonna do anything about it, or...? |
| 0x1525ef | 46 | Yeah... About that. Things are a little more\n |
| 0x15261e | 22 | complicated this time. |
| 0x152635 | 48 | When we established our alliance, we agreed to\n |
| 0x152666 | 46 | make thorough plans before any action we take. |
| 0x152695 | 41 | But this heist isn't part of those plans. |
| 0x1526bf | 48 | As far as I know, this is Nosuri acting on her\n |
| 0x1526f0 | 34 | own without consulting the others. |
| 0x152713 | 42 | Seems she witnessed the loan shark using\n |
| 0x15273e | 43 | some... questionable means of getting his\n |
| 0x15276a | 11 | money back. |
| 0x152776 | 49 | She got angry over the injustice of it, and now\n |
| 0x1527a8 | 48 | she's angling to bring "divine retribution" to\n |
| 0x1527d9 | 4 | him. |
| 0x1527de | 47 | Not that I don't sympathize with her motives,\n |
| 0x15280e | 44 | but this is gonna be a big mess to untangle. |
| 0x15283b | 49 | Oh? I wouldn't think you were the type to let a\n |
| 0x15286d | 45 | shady loan shark slip off the hook so easily. |
| 0x15289b | 47 | Of course I'm not. I've been making plans for\n |
| 0x1528cb | 31 | him to disappear for ages, now. |
| 0x1528eb | 44 | It's just that if our "noble thief" friend\n |
| 0x152918 | 47 | butts in now, all my progress goes up in smoke. |
| 0x152948 | 6 | I see. |
| 0x15294f | 5 | So... |
| 0x152955 | 37 | ...That smile gives me a bad feeling. |
| 0x15297b | 50 | Hold on, now. This had better not be building up\n |
| 0x1529ae | 45 | to a request for another pain-in-the-ass job. |
| 0x1529dc | 47 | Oh, come on. You make it sound like EVERY job\n |
| 0x152a0c | 32 | I give you is a pain in the ass. |
| 0x152a2d | 46 | That's largely because every job you give me\n |
| 0x152a5c | 33 | IS a pain in the ass. Am I wrong? |
| 0x152a7e | 48 | Look, all I need you to do is stop Nosuri from\n |
| 0x152aaf | 45 | sneaking in. Just find her and drive her off. |
| 0x152add | 14 | Simple, right? |
| 0x152aec | 46 | Hey, don't change the subject on me! I mean,\n |
| 0x152b1b | 32 | sure, it sounds simple enough... |
| 0x152b3c | 44 | But I'm guessing it's gonna be a huge pain\n |
| 0x152b69 | 40 | when we actually get around to doing it. |
| 0x152b92 | 50 | Why are you even asking us? Just tell her little\n |
| 0x152bc5 | 41 | bandit gang to stop her and save us the\n |
| 0x152bef | 8 | trouble. |
| 0x152bf8 | 47 | They're busy with something else, as far as I\n |
| 0x152c28 | 38 | can tell. Don't be so difficult, here. |
| 0x152c4f | 46 | And I can't exactly ask her on my own, since\n |
| 0x152c7e | 37 | she knows I'm connected to the court. |
| 0x152ca4 | 35 | That leaves you and your gang, kid. |
| 0x152cc8 | 43 | So you just want us to drive her off, not\n |
| 0x152cf4 | 39 | actually catch her? Man, what kind of\n |
| 0x152d1c | 20 | roundabout, weird... |
| 0x152d31 | 50 | What's so bad about that? You've been doing well\n |
| 0x152d64 | 46 | so far. Don't sweat the small stuff like this. |
| 0x152d93 | 48 | ...Seems like every time we talk, I can't help\n |
| 0x152dc4 | 47 | but think about how Ukon is so different from\n |
| 0x152df4 | 7 | Oshtor. |
| 0x152dfc | 46 | Oh, and make sure Nosuri doesn't hear a word\n |
| 0x152e2b | 19 | of this, of course. |
| 0x152e3f | 23 | What a goddamn farce... |
| 0x152e57 | 45 | To be honest, this job IS as much of a pain\n |
| 0x152e85 | 46 | in the ass as I thought, but I can't go back\n |
| 0x152eb4 | 15 | on my word now. |
| 0x152ec4 | 47 | Forget waiting around. Let's just go find her\n |
| 0x152ef4 | 47 | and "accidentally" drive her off so we can be\n |
| 0x152f24 | 5 | done. |
| 0x152f2a | 45 | She wouldn't make a huge fuss of it, I bet.\n |
| 0x152f58 | 49 | In fact, she'd likely run just as soon as she's\n |
| 0x152f8a | 8 | spotted. |
| 0x152f93 | 29 | That's easier said than done. |
| 0x152fb1 | 23 | Yeah, I know, I know... |
| 0x152fc9 | 50 | According to Ukon's info, she plans on using the\n |
| 0x152ffc | 44 | sewers, but if she goes a different route... |
| 0x153029 | 44 | Are you sure we shouldn't split up? Cast a\n |
| 0x153056 | 10 | wider net? |
| 0x153061 | 49 | It'll be difficult to respond to any changes in\n |
| 0x153093 | 46 | the situation if we spread ourselves out too\n |
| 0x1530c2 | 5 | thin. |
| 0x1530c8 | 49 | I'm not trying to just keep you all around just\n |
| 0x1530fa | 38 | so I can take it easy. Definitely not. |
| 0x153121 | 25 | ...I should have figured. |
| 0x15313b | 46 | As we continue whispering, milling aimlessly\n |
| 0x15316a | 35 | about the back alley... IT happens. |
| 0x15318e | 6 | Wh--!? |
| 0x153195 | 8 | *FWUMPH* |
| 0x15319e | 5 | AHH!? |
| 0x1531a4 | 49 | The ground under me gives way, and for a single\n |
| 0x1531d6 | 47 | terrifying moment, I stand on nothing over an\n |
| 0x153206 | 6 | abyss. |
| 0x15320d | 6 | Haku!? |
| 0x153214 | 48 | Before I can take Kuon's outstretched hand and\n |
| 0x153245 | 45 | pull myself to safety, I fall into the sewer. |
| 0x153273 | 9 | AHHHHHH!! |
| 0x15327d | 48 | Flailing blindly as I plummet, I reach out and\n |
| 0x1532ae | 48 | desperately grab hold of the first thing I can-- |
| 0x1532df | 9 | *THUMP--* |
| 0x1532e9 | 12 | What the--!? |
| 0x1532f6 | 18 | G-Gah--falling--!! |
| 0x153309 | 48 | I don't know what I grabbed onto, but it halts\n |
| 0x15333a | 49 | my fall. Even so, I start slipping, unsteady at\n |
| 0x15336c | 5 | best. |
| 0x153372 | 44 | Beneath me gapes an enormous hole into the\n |
| 0x15339f | 48 | sewers. It's a LONG fall. Panicking, I hold on\n |
| 0x1533d0 | 14 | for dear life. |
| 0x1533df | 29 | Urgh--what are y--Unhand me!! |
| 0x1533fd | 41 | *FWUMP {W35}WHOOSH {W35}FWOOSH {W35}WH--* |
| 0x153427 | 40 | Wh--!? Quit flailing, or I'm gonna fall! |
| 0x153450 | 47 | I tighten my grasp on whatever it is that had\n |
| 0x153480 | 45 | broken my fall, holding on with both hands... |
| 0x1534ae | 47 | Something soft brushes past my hand, and with\n |
| 0x1534de | 39 | a ripping sound, I begin to fall again. |
| 0x153506 | 6 | BWAH!? |
| 0x15350d | 44 | Wh-Wh-Where do you think you're grabbing!?\n |
| 0x15353a | 7 | LET GO! |
| 0x153542 | 48 | You've gotta be joking! If I let go, I fall to\n |
| 0x153573 | 9 | my death! |
| 0x15357d | 50 | As much as I cling to safety, the flailing keeps\n |
| 0x1535b0 | 45 | me from climbing any higher to get a secure\n |
| 0x1535de | 5 | grip. |
| 0x1535e4 | 14 | I said let go! |
| 0x1535f3 | 43 | *FWUMP {W35}FWUMP {W35}FWUMP {W35}FWOOSH--* |
| 0x15361f | 46 | Stop! STOP!! This is no laughing matter, OK?\n |
| 0x15364e | 21 | I'm SERIOUSLY gonna-- |
| 0x153664 | 6 | *Slip* |
| 0x15366b | 50 | My right hand slips, and suddenly I drop another\n |
| 0x15369e | 34 | foot, hanging by a strip of cloth. |
| 0x1536c1 | 47 | Even that begins to rip with my entire weight\n |
| 0x1536f1 | 44 | pulling on it... Gotta grab onto something\n |
| 0x15371e | 5 | else! |
| 0x153724 | 29 | *Rustle, rustle--{W120} slip* |
| 0x153742 | 50 | I quickly try to seize what looks like someone's\n |
| 0x153775 | 46 | waist, but grab only cloth, dropping another\n |
| 0x1537a4 | 5 | foot. |
| 0x1537aa | 7 | YAHHH!? |
| 0x1537b2 | 48 | And then I'm immediately up again, faster than\n |
| 0x1537e3 | 34 | I can blink, the cloth going taut. |
| 0x153806 | 45 | For a moment, I... probably saw something I\n |
| 0x153834 | 49 | shouldn't have, but I can't tell because of the\n |
| 0x153866 | 5 | dark. |
| 0x15386c | 31 | Must be my eyes playing tricks. |
| 0x15388c | 36 | Y-Y-You SCOUNDREL! Unhand me NOW!!\n |
| 0x1538b1 | 23 | Let go! Let GO, LET--!! |
| 0x1538c9 | 46 | Though my "rescuer" holds the bunch of cloth\n |
| 0x1538f8 | 47 | up with all her might, my weight drags on it... |
| 0x153928 | 28 | Guh... urgh... HhhhaaAAAHH!! |
| 0x153945 | 42 | She pulls upward with a surge of strength! |
| 0x153970 | 51 | Gah... Urk... C-Can't... get... a good... grip...!! |
| 0x1539a4 | 42 | Distracted as she is with having to keep\n |
| 0x1539cf | 45 | BOTH of us on the ladder with one hand, her\n |
| 0x1539fd | 13 | grip falters. |
| 0x153a0b | 43 | As we continue struggling, it dawns on me\n |
| 0x153a37 | 27 | exactly what just happened: |
| 0x153a53 | 46 | The person we've been waiting to emerge from\n |
| 0x153a82 | 44 | the sewers opened the manhole in that back\n |
| 0x153aaf | 6 | alley. |
| 0x153ab6 | 47 | I happened to be walking right over it at the\n |
| 0x153ae6 | 46 | time, and fell straight in, grabbing onto her. |
| 0x153b15 | 42 | ...or onto her clothes, more accurately.\n |
| 0x153b40 | 48 | Regardless, I feel kinda bad for what I've done. |
| 0x153b71 | 51 | Whatever the circumstances, I have zero intention\n |
| 0x153ba5 | 45 | of letting go. If I let go, I fall into the\n |
| 0x153bd3 | 10 | death pit. |
| 0x153bde | 4 | Ack. |
| 0x153be3 | 31 | An ominous sound fills my ears. |
| 0x153c03 | 48 | The cloth covering my savior begins tearing in\n |
| 0x153c34 | 47 | earnest, and I see things I probably shouldn't. |
| 0x153c64 | 9 | *THWACK!* |
| 0x153c6e | 8 | Hnngah!? |
| 0x153c77 | 46 | A foot connects with my head as she tries to\n |
| 0x153ca6 | 31 | kick me away, face blazing red. |
| 0x153cc6 | 45 | GET. {W50}OFF. {W40}LET. {W35}GO. {W50}OF ME! |
| 0x153cf4 | 50 | Even as the rain of kicks connects with my face,\n |
| 0x153d27 | 9 | I wonder: |
| 0x153d31 | 41 | Does she not understand what she's doing? |
| 0x153d5b | 49 | The fact that I'm still hanging on by the cloth\n |
| 0x153d8d | 47 | means every kick is applying more pressure to\n |
| 0x153dbd | 5 | it... |
| 0x153dc3 | 8 | --NOW!!! |
| 0x153dcc | 48 | In that moment, she puts all her strength into\n |
| 0x153dfd | 47 | a forceful kick, and the cloth rends from end\n |
| 0x153e2d | 7 | to end. |
| 0x153e35 | 9 | ...Bwuh!? |
| 0x153e3f | 8 | ...welp. |
| 0x153e48 | 5 | Huh!? |
| 0x153e4e | 10 | Haku & ??? |
| 0x153e59 | 21 | AAAAAAAAHHHHHHHHH!!?? |
| 0x153e6f | 26 | C-Cold--cold cold cold--!! |
| 0x153e8a | 50 | Mercifully, the bottom of the pit is filled with\n |
| 0x153ebd | 48 | water deep enough that I didn't get hurt, but... |
| 0x153eee | 49 | Now I'm out in the cold Yamato night, soaked to\n |
| 0x153f20 | 26 | the bone. In sewage water. |
| 0x153f3b | 45 | At least it isn't waste water, but that's a\n |
| 0x153f69 | 23 | small blessing at best. |
| 0x153f81 | 33 | What did I do to deserve this...? |
| 0x153fa3 | 50 | So, the person we're supposed to be watching out\n |
| 0x153fd6 | 22 | for is gone, you said? |
| 0x153fed | 47 | Y-Yeah. B-B-By the time I s-surfaced, she was\n |
| 0x15401d | 26 | g-g-g-gone... So c-cold... |
| 0x154038 | 45 | I see... I doubt she drowned down there, so\n |
| 0x154066 | 38 | it's probably best to assume she fled. |
| 0x15408d | 45 | Which... means we accomplished our goal for\n |
| 0x1540bb | 19 | the night, I think? |
| 0x1540cf | 45 | Th-Then--ACHOO!!--let's get the hell out of\n |
| 0x1540fd | 5 | here. |
| 0x154103 | 10 | Hey, love? |
| 0x15410e | 8 | Wh-What? |
| 0x154117 | 10 | You stink. |
| 0x154122 | 8 | No shit. |
| 0x15412b | 43 | I can see everyone wrinkling their noses,\n |
| 0x154157 | 40 | maintaining a cautious distance from me. |
| 0x154180 | 46 | C-Can I get a little sympathy, here? This is\n |
| 0x1541af | 46 | how you appreciate the guy who d-did all the\n |
| 0x1541de | 5 | work? |
| 0x1541e4 | 47 | It's, uh... It's not that we don't appreciate\n |
| 0x154214 | 6 | you... |
| 0x15421b | 45 | "All the work?" All you did was fall into a\n |
| 0x154249 | 15 | hole, though... |
| 0x154259 | 6 | Unngh! |
| 0x154260 | 48 | Color me astounded that you managed to survive\n |
| 0x154291 | 10 | unscathed. |
| 0x15429c | 49 | Do I LOOK uns-s-scathed? You're d-doing this on\n |
| 0x1542ce | 21 | purpose, aren't you!? |
| 0x1542e4 | 45 | Damn it. They could give me some praise for\n |
| 0x154312 | 32 | doing the actual job for once... |
| 0x154333 | 49 | A job well done, anyway. We should head for the\n |
| 0x154365 | 38 | inn. You'll catch a cold at this rate. |
| 0x15438c | 11 | Ah--ACHOO!! |
| 0x154398 | 36 | A-Are you... all right? Here, use... |
| 0x1543bd | 45 | Rulutieh passes me a white, elegant-looking\n |
| 0x1543eb | 15 | handkerchief... |
| 0x1543fb | 48 | I-I appreciate the sentiment, but I'd feel bad\n |
| 0x15442c | 13 | ruining this. |
| 0x15443a | 45 | Kuon meets my eyes as I hesitate, trying to\n |
| 0x154468 | 47 | decide whether to take the handkerchief or not. |
| 0x154498 | 15 | Hmm hmm. Hmmmm. |
| 0x1544a8 | 49 | Kuon laughs, her eyes saying, "I guess it can't\n |
| 0x1544da | 11 | be helped." |
| 0x1544e6 | 49 | I'm afraid you'll just have to grin and bear it\n |
| 0x154518 | 36 | until we get back to the Hakurokaku. |
| 0x15453d | 4 | Huh? |
| 0x154542 | 46 | Relenting, Kuon undoes the aperyu around her\n |
| 0x154571 | 44 | shoulders and wraps it around mine, instead. |
| 0x15459e | 34 | Here. You can borrow this for now. |
| 0x1545c1 | 47 | Walk home like that, and you're gonna get sick. |
| 0x1545f1 | 5 | Oh... |
| 0x1545f7 | 43 | A-Are you sure, dear sister? That'll soil\n |
| 0x154623 | 14 | your aperyu... |
| 0x154632 | 49 | It's fine. I'll wash it later and it'll be good\n |
| 0x154664 | 7 | as new. |
| 0x15466c | 6 | Right? |
| 0x154673 | 4 | Yes. |
| 0x154678 | 45 | Finally, some nice, HOT water for a change... |
| 0x1546a6 | 45 | I rush into the baths, only to find an odd-\n |
| 0x1546d4 | 37 | looking guest using them ahead of me. |
| 0x1546fa | 25 | ...What the hell is THAT? |
| 0x154714 | 47 | For a moment, I couldn't even recognize it as\n |
| 0x154744 | 9 | a person. |
| 0x15474e | 49 | All I can make out is a shape in the quivering,\n |
| 0x154780 | 29 | person-sized mass of bubbles. |
| 0x15479e | 30 | Must be someone washing off... |
| 0x1547bd | 49 | Gotta be scrubbing up a storm if they're making\n |
| 0x1547ef | 18 | that many bubbles. |
| 0x154802 | 44 | I take a seat next to the towering pile of\n |
| 0x15482f | 45 | bubbles and fill my bath pail with hot water. |
| 0x15485d | 27 | Ahh, that's good and hot... |
| 0x154879 | 45 | I pour the water over myself several times.\n |
| 0x1548a7 | 46 | It feels all the hotter, after the cold night. |
| 0x1548d6 | 40 | As the water washes over me, I take an\n |
| 0x1548ff | 39 | experimental sniff at one of my arms... |
| 0x154927 | 45 | Urgh. I guess just rinsing won't get rid of\n |
| 0x154955 | 11 | the stench. |
| 0x154961 | 47 | I grab a soap bar and rub it on a towel until\n |
| 0x154991 | 47 | it starts to foam, then turn it on my reeking\n |
| 0x1549c1 | 5 | skin. |
| 0x1549c7 | 27 | *Bubble, bubble, bubble*... |
| 0x1549e3 | 48 | This soap sure foams up a lot, though. I guess\n |
| 0x154a14 | 44 | the inn is high-end enough to buy the good\n |
| 0x154a41 | 6 | stuff. |
| 0x154a48 | 47 | I repeatedly wash, scrub, and rinse, taking a\n |
| 0x154a78 | 46 | whiff of my skin with each pass as the smell\n |
| 0x154aa7 | 6 | fades. |
| 0x154aae | 48 | Finally, I can only smell the soap, the stench\n |
| 0x154adf | 32 | of sewage banished. But still... |
| 0x154b00 | 46 | I can't quite tell if it's fully gone, and I\n |
| 0x154b2f | 42 | decide to wash once more for good measure. |
| 0x154b5a | 48 | Geez, the guy next to me is still going at it.\n |
| 0x154b8b | 26 | He's been washing forever. |
| 0x154ba6 | 50 | It's more like furious scrubbing than "washing",\n |
| 0x154bd9 | 47 | really, going by the shaking. Must be a clean\n |
| 0x154c09 | 6 | freak. |
| 0x154c10 | 48 | I finish rinsing off with one last bucket over\n |
| 0x154c41 | 46 | my head, hot water washing the bubbles away... |
| 0x154c70 | 45 | The pillar of bubbly cleanliness next to me\n |
| 0x154c9e | 46 | also reaches for a bucket, seemingly finished. |
| 0x154ccd | 14 | In any case... |
| 0x154cdc | 7 | Whew... |
| 0x154ce4 | 21 | What an awful d--Huh? |
| 0x154cfa | 45 | We both let out a relieved sigh at the same\n |
| 0x154d28 | 47 | time, and then I look beside me, only to find-- |
| 0x154d58 | 13 | Haku & Nosuri |
| 0x154d66 | 47 | We both shout and jump away at the same time,\n |
| 0x154d96 | 33 | almost slipping on the wet floor. |
| 0x154db8 | 9 | Y-You--!? |
| 0x154dc2 | 49 | You're Nos--I-I mean, that person from earlier!\n |
| 0x154df4 | 34 | What the hell are YOU doing here!? |
| 0x154e17 | 47 | I could ask you the same, scoundrel! I'm SURE\n |
| 0x154e47 | 35 | I put an "occupied" sign on the d-- |
| 0x154e6b | 42 | As Nosuri glares at me, her eyes wander,\n |
| 0x154e96 | 14 | and she pales. |
| 0x154ea5 | 15 | Th-Th-Th-That-- |
| 0x154eb5 | 5 | That? |
| 0x154ebb | 40 | Sh-Sh-Shut up and p-put that thing away! |
| 0x154ee4 | 46 | She shudders, pointing a shaking finger at me. |
| 0x154f13 | 41 | I follow the line of her finger to--Oh.\n |
| 0x154f3d | 11 | THAT thing. |
| 0x154f49 | 10 | ...My bad. |
| 0x154f54 | 48 | She's hardly making an unreasonable demand, so\n |
| 0x154f85 | 42 | I reach for a towel and wrap myself in it. |
| 0x154fb0 | 43 | ...Aren't you gonna cover up too, though?\n |
| 0x154fdc | 31 | I mean, everything's sort of... |
| 0x154ffc | 13 | Sort of what? |
| 0x15500a | 4 | ACK! |
| 0x15500f | 49 | Only now does she seem to realize she's just as\n |
| 0x155041 | 48 | naked as I am, and she covers herself with her\n |
| 0x155072 | 5 | arms. |
| 0x155078 | 47 | Of course, it's difficult to hide your entire\n |
| 0x1550a8 | 43 | body with just your arms, and she squirms\n |
| 0x1550d4 | 10 | awkwardly. |
| 0x1550df | 47 | Gah--I understand, now. Y-You shadowed me all\n |
| 0x15510f | 26 | the way here, didn't you!? |
| 0x15512a | 5 | What? |
| 0x155130 | 48 | Don't play the fool! I KNOW you were following\n |
| 0x155161 | 3 | me! |
| 0x155165 | 48 | That must be why you dropped me into that pit,\n |
| 0x155196 | 44 | scoundrel. Forcing me into this vulnerable\n |
| 0x1551c3 | 8 | state... |
| 0x1551cc | 47 | Oh, come on! Why would I go through that much\n |
| 0x1551fc | 8 | trouble? |
| 0x155205 | 47 | Quit feigning ignorance, coward! How DARE you\n |
| 0x155235 | 46 | force me to reveal the location of my secret\n |
| 0x155264 | 5 | base? |
| 0x15526a | 47 | ...Nobody said anything about that. She kinda\n |
| 0x15529a | 32 | just blew the secret on her own. |
| 0x1552bb | 45 | I'm kinda hoping she doesn't just blurt out\n |
| 0x1552e9 | 19 | that she's a thief. |
| 0x1552fd | 49 | My job's over and done with. I don't want to be\n |
| 0x15532f | 47 | any more involved in this mess than I already\n |
| 0x15535f | 5 | am... |
| 0x155365 | 46 | And it's only gonna get worse unless I put a\n |
| 0x155394 | 15 | stop to it now. |
| 0x1553a4 | 47 | Ahem--You're sounding awfully suspicious, you\n |
| 0x1553d4 | 45 | know. Almost as if you've been up to no good. |
| 0x155402 | 48 | Like planning on a heist on a certain mansion,\n |
| 0x155433 | 12 | for example. |
| 0x155440 | 6 | Hyeh!? |
| 0x155447 | 50 | Good, she's realizing her mistake. Hopefully she\n |
| 0x15547a | 44 | won't make any more careless remarks after-- |
| 0x1554a7 | 3 | H-- |
| 0x1554ab | 18 | How did you know!? |
| 0x1554be | 48 | You've gotta be kidding me. You aren't denying\n |
| 0x1554ef | 4 | it!? |
| 0x1554f4 | 47 | I gave you a chance to get out of it, and you\n |
| 0x155524 | 16 | confess anyway!? |
| 0x155535 | 38 | Wha--!? O-Oh, no, a leading question!? |
| 0x15555c | 40 | To fall for such a fundamental trick--\n |
| 0x155585 | 27 | how could I be so careless? |
| 0x1555a1 | 48 | I don't think I can talk sense with this girl.\n |
| 0x1555d2 | 40 | What the hell am I supposed to do, here? |
| 0x1555fb | 6 | Hah... |
| 0x155602 | 14 | Ha haaah ha... |
| 0x155611 | 45 | AHAHAHAHAHA!! It seems you've found me out.\n |
| 0x15563f | 9 | So be it! |
| 0x155649 | 46 | Your suspicions are indeed correct. I am the\n |
| 0x155678 | 43 | one and only Nosuri, of the Nosuri Thieves! |
| 0x1556a4 | 49 | Despite struggling to preserve her modesty just\n |
| 0x1556d6 | 43 | now, she suddenly stands up proudly, arms\n |
| 0x155702 | 7 | folded. |
| 0x15570a | 48 | I am but a vagrant, a mendicant of fortune who\n |
| 0x15573b | 43 | seeks to restore her tarnished family name! |
| 0x155767 | 50 | But above these, I am a champion of the people--\n |
| 0x15579a | 40 | the poor of Yamato who suffer from its\n |
| 0x1557c3 | 11 | corruption! |
| 0x1557cf | 9 | Uh... OK. |
| 0x1557d9 | 48 | I pretty much know all of this already, so I'm\n |
| 0x15580a | 34 | not... really sure how to respond? |
| 0x15582d | 46 | And wasn't she JUST trying to cover herself?\n |
| 0x15585c | 44 | I can... kinda see everything at this point. |
| 0x155889 | 41 | What's the matter? I introduced myself.\n |
| 0x1558b3 | 19 | Now it's your turn. |
| 0x1558c7 | 27 | What, I have to do one too? |
| 0x1558e3 | 48 | Somehow, I get the feeling telling her my name\n |
| 0x155914 | 39 | is just asking for trouble. Oh, well... |
| 0x15593c | 9 | I'm Haku. |
| 0x155946 | 43 | I see. Haku, is it...? Where have I heard\n |
| 0x155972 | 17 | that name before? |
| 0x155984 | 25 | Wait, you've heard of me? |
| 0x15599e | 30 | I... can't seem to remember.\n |
| 0x1559bd | 42 | Therefore, it must be my imagination! Yes. |
| 0x1559e8 | 47 | Get my hopes up just to crush them, why don't\n |
| 0x155a18 | 13 | you? Yeesh... |
| 0x155a26 | 45 | But I'll admit you're very good. You're the\n |
| 0x155a54 | 40 | first person to corner me so completely. |
| 0x155a7d | 46 | I understand you're praising me, but somehow\n |
| 0x155aac | 37 | that doesn't make me feel any better. |
| 0x155ad2 | 47 | So, what now? Do you plan on capturing me and\n |
| 0x155b02 | 38 | handing me over to the capital guards? |
| 0x155b29 | 42 | I just told you I'm not planning anything! |
| 0x155b54 | 48 | Give it a rest, already! I've been pulled deep\n |
| 0x155b85 | 30 | enough into all this as it is. |
| 0x155ba4 | 30 | Then that means... aha. I see. |
| 0x155bc3 | 47 | I never expected... someone in this place who\n |
| 0x155bf3 | 19 | shares my ideals... |
| 0x155c07 | 45 | At last, my hard work is starting to pay off. |
| 0x155c35 | 40 | And now she's just muttering to herself. |
| 0x155c5e | 45 | You! How would you like to become one of my\n |
| 0x155c8c | 8 | bandits? |
| 0x155c95 | 48 | You're quite skilled, to have cornered me like\n |
| 0x155cc6 | 45 | this. I would be glad to have you as an ally. |
| 0x155cf4 | 45 | What? There was nothing "skilled" about it.\n |
| 0x155d22 | 47 | You sort of stumbled into this all on your own. |
| 0x155d52 | 47 | What do you say? Not a bad proposition, isn't\n |
| 0x155d82 | 3 | it? |
| 0x155d86 | 44 | Crap... She seems pretty serious about this. |
| 0x155db3 | 38 | I'm afraid I have to modestly decline. |
| 0x155dda | 47 | Ahahaha! There's no need for modesty in front\n |
| 0x155e0a | 6 | of me. |
| 0x155e11 | 48 | ...Did you hear the part where I said "decline"? |
| 0x155e42 | 44 | She keeps going on about people in need of\n |
| 0x155e6f | 46 | saving from oppression, but are there really\n |
| 0x155e9e | 10 | that many? |
| 0x155ea9 | 46 | Yamato is a peaceful, prosperous nation, and\n |
| 0x155ed8 | 47 | the people always seem lively to me. Not much\n |
| 0x155f08 | 10 | suffering. |
| 0x155f13 | 46 | Hey, can I ask you something? What about the\n |
| 0x155f42 | 46 | capital guards? Can't you leave peacekeeping\n |
| 0x155f71 | 8 | to them? |
| 0x155f7a | 46 | From what I've heard, Uk--Oshtor seems to be\n |
| 0x155fa9 | 43 | doing a good job of keeping the place safe. |
| 0x155fd5 | 37 | Hm... that Imperial Guard man, eh...? |
| 0x155ffb | 47 | He just won't do, I'm afraid. I'll admit he's\n |
| 0x15602b | 49 | done good things, but he deliberates and delays\n |
| 0x15605d | 9 | too much. |
| 0x156067 | 49 | Those who reach out for help are those who need\n |
| 0x156099 | 46 | it immediately, and he hesitates in favor of\n |
| 0x1560c8 | 9 | planning. |
| 0x1560d2 | 45 | By the time he has his schemes ready to act\n |
| 0x156100 | 30 | upon, it's often far too late. |
| 0x15611f | 47 | Whenever we follow through with our plans, he\n |
| 0x15614f | 49 | always comes to the scene in a rush, taken off-\n |
| 0x156181 | 8 | guard... |
| 0x15618a | 47 | Like a carrion bird arriving late to pick our\n |
| 0x1561ba | 45 | prey clean. So much for the Twin Shields of\n |
| 0x1561e8 | 7 | Yamato. |
| 0x1561f0 | 47 | Oh, right. I almost forgot she isn't aware of\n |
| 0x156220 | 33 | her group's alliance with Oshtor. |
| 0x156242 | 49 | I was wondering why she hasn't been made aware,\n |
| 0x156274 | 32 | but... I think I understand now. |
| 0x156295 | 48 | Oshtor wouldn't want to work with an impulsive\n |
| 0x1562c6 | 46 | person. She'd do things her way and ruin his\n |
| 0x1562f5 | 6 | plans. |
| 0x1562fc | 48 | Do you understand, now? The hero of the people\n |
| 0x15632d | 45 | isn't Oshtor, but me, Nosuri the noble thief! |
| 0x15635b | 40 | She proudly puffs out her chest, which\n |
| 0x156384 | 17 | promptly jiggles. |
| 0x156396 | 47 | ...She seems to have gotten so impassioned in\n |
| 0x1563c6 | 47 | her speech that she forgot what kind of state\n |
| 0x1563f6 | 9 | she's in. |
| 0x156400 | 49 | Ah, but I suppose it's unfair to push this kind\n |
| 0x156432 | 30 | of decision on you so quickly. |
| 0x156451 | 29 | That's... not the issue here. |
| 0x15646f | 42 | When we meet again, I'll be wanting your\n |
| 0x15649a | 7 | answer! |
| 0x1564a2 | 46 | Smiling with smug satisfaction, Nosuri turns\n |
| 0x1564d1 | 32 | for the exit, still stark naked. |
| 0x1564f2 | 46 | Ah, Sir Haku... I brought you a clean change\n |
| 0x156521 | 10 | of c-clo-- |
| 0x15652c | 10 | *Fwump*... |
| 0x156537 | 46 | I peer around the corner to find Rulutieh, a\n |
| 0x156566 | 46 | rumpled pile of clothes at her feet, staring\n |
| 0x156595 | 12 | at Nosuri... |
| 0x1565a2 | 45 | We shall meet again. I expect you'll have a\n |
| 0x1565d0 | 40 | more favorable answer for me, next time. |
| 0x1565f9 | 15 | Sir... Haku...? |
| 0x156609 | 42 | I swear I can see the life draining from\n |
| 0x156634 | 45 | Rulutieh's eyes as she stares vacantly ahead. |
| 0x158adb | 10 | Pardon me. |
| 0x158ae6 | 14 | Hm? Oh, hullo. |
| 0x158af5 | 47 | One afternoon, Munechika suddenly came by our\n |
| 0x158b25 | 15 | headquarters... |
| 0x158b35 | 46 | I remember you. You were here a little while\n |
| 0x158b64 | 31 | back, weren't you? Miss, erm... |
| 0x158b84 | 15 | Lady Munechika. |
| 0x158b94 | 42 | Right! The general who takes care of the\n |
| 0x158bbf | 21 | princess, that's you. |
| 0x158bd5 | 31 | I'm Atuy! Pleasure to meet you. |
| 0x158bf5 | 5 | Atuy? |
| 0x158bfb | 46 | Pleasant surprise spreads across Munechika's\n |
| 0x158c2a | 27 | face upon hearing the name. |
| 0x158c46 | 36 | Lord Soyankekur's daughter, correct? |
| 0x158c6b | 22 | Oh, you know about me? |
| 0x158c82 | 42 | I owe a great deal to milord Soyankekur.\n |
| 0x158cad | 45 | He taught me much when I was merely a novice. |
| 0x158cdb | 37 | Oh, he--no, no. None of that, please. |
| 0x158d01 | 3 | Hm? |
| 0x158d05 | 50 | This inn is a hideout, yeah? For those of us who\n |
| 0x158d38 | 48 | want to shed all the politics and the "milords." |
| 0x158d69 | 32 | Ah, I see. My deepest apologies. |
| 0x158d8a | 43 | Would you quit making stuff up about this\n |
| 0x158db6 | 12 | place, Atuy? |
| 0x158dc3 | 48 | How can we help you? If you're looking for the\n |
| 0x158df4 | 46 | princess, I'm afraid she's not here. For once. |
| 0x158e23 | 46 | Not to worry. I'm quite certain Her Highness\n |
| 0x158e52 | 39 | is absorbed in her studies, at present. |
| 0x158e7a | 49 | We're... talking about the same princess, here,\n |
| 0x158eac | 6 | right? |
| 0x158eb3 | 48 | The princess's frequent escapes finally roused\n |
| 0x158ee4 | 46 | the high priestess into giving her quite the\n |
| 0x158f13 | 9 | scolding. |
| 0x158f1d | 42 | It takes a fair lot to try her patience.\n |
| 0x158f48 | 44 | Trust me, we'll have no royal problems for\n |
| 0x158f75 | 10 | some time. |
| 0x158f80 | 48 | I should think that even if Her Highness makes\n |
| 0x158fb1 | 44 | an attempt, she'll find her guards doubled\n |
| 0x158fde | 6 | today. |
| 0x158fe5 | 21 | Well, that's a shame. |
| 0x158ffb | 44 | Nah. Serves her right. Retribution for the\n |
| 0x159028 | 7 | wicked. |
| 0x159030 | 50 | I didn't think anyone existed who could give her\n |
| 0x159063 | 47 | a scolding and actually be listened to, though. |
| 0x159093 | 42 | The high priestess is the handler of all\n |
| 0x1590be | 44 | spiritual affairs within the Mikado's court. |
| 0x1590eb | 44 | In addition to those duties, she serves as\n |
| 0x159118 | 21 | Her Highness's tutor. |
| 0x15912e | 44 | Tutor? I thought you were in charge of that. |
| 0x15915b | 45 | It would be disrespectful to claim the full\n |
| 0x159189 | 24 | title for myself, truly. |
| 0x1591a2 | 43 | I merely take over certain duties when my\n |
| 0x1591ce | 46 | responsibilities as a General do not consume\n |
| 0x1591fd | 8 | my time. |
| 0x159206 | 50 | I see. And you're here because...? Shouldn't you\n |
| 0x159239 | 45 | be near the princess if you're her bodyguard? |
| 0x15926b | 46 | Munechika glances at the ceiling for a moment. |
| 0x15929a | 48 | Ahem! I-It's quite... rare to see Her Highness\n |
| 0x1592cb | 44 | working diligently. My presence would only\n |
| 0x1592f8 | 9 | distract. |
| 0x159302 | 45 | More importantly, as Yamato's future ruler,\n |
| 0x159330 | 48 | it is paramount that she understand its people\n |
| 0x159361 | 6 | fully. |
| 0x159368 | 46 | Equally paramount, however, is the princess'\n |
| 0x159397 | 47 | safety. I have come to assess the security of\n |
| 0x1593c7 | 9 | this inn. |
| 0x1593d1 | 46 | I kinda see where you're coming from, but...\n |
| 0x159400 | 45 | maybe we should call the princess here first? |
| 0x15942e | 40 | Th-This is a matter of utmost secrecy!\n |
| 0x159457 | 44 | N-National security! To speak of it to the\n |
| 0x159484 | 15 | princess, you-- |
| 0x159494 | 47 | "Utmost secrecy," my ass. You're digging your\n |
| 0x1594c4 | 16 | own grave, here. |
| 0x1594d5 | 36 | Oh, come on, Haku. Give her a break. |
| 0x1594fa | 5 | Kuon? |
| 0x159500 | 42 | She came all this way to pay us a visit.\n |
| 0x15952b | 25 | Why don't you let her in? |
| 0x159545 | 30 | I thank you for your kindness. |
| 0x159564 | 18 | Here, have a seat. |
| 0x159577 | 10 | Thank you. |
| 0x159582 | 47 | Trailing behind Kuon, Munechika pauses as she\n |
| 0x1595b2 | 29 | catches sight of something... |
| 0x1595d0 | 20 | Hm...? What is this? |
| 0x1595e5 | 43 | Her eyes fall on the plate Atuy is holding. |
| 0x159611 | 45 | Oh, this? Just some Rulu. It's getting real\n |
| 0x15963f | 27 | popular around the capital. |
| 0x15965b | 49 | "Rulu"? Ah, the sweet I've been hearing so much\n |
| 0x15968d | 46 | about. It almost looks like a fruit from the\n |
| 0x1596bc | 6 | south. |
| 0x1596c3 | 43 | That's all you've been having for snacks,\n |
| 0x1596ef | 44 | lately, Atuy... Taken a liking to them, huh? |
| 0x15971c | 49 | Hee! They're my new favorite. They sort of have\n |
| 0x15974e | 35 | a texture like Kurarin, don't they? |
| 0x159772 | 11 | *Jiggle*... |
| 0x15977e | 47 | ...I wonder what the texture would be like if\n |
| 0x1597ae | 24 | I ate Kurarin, though... |
| 0x1597c7 | 31 | *Jiggle-jiggle-jiggle-jiggle--* |
| 0x1597e7 | 36 | Oh, come on, now he's gone all pale. |
| 0x15980c | 38 | Anyway, would you like one, Munechika? |
| 0x159833 | 6 | May I? |
| 0x15983a | 47 | Atuy holds a piece of Rulu on a toothpick for\n |
| 0x15986a | 36 | Munechika, who hesitates slightly... |
| 0x15988f | 48 | Then, with Atuy smiling innocently at her, she\n |
| 0x1598c0 | 22 | nods and takes a bite. |
| 0x1598d7 | 19 | How do you like it? |
| 0x1598eb | 17 | Hrm... This is... |
| 0x1598fd | 51 | Quite good! Its texture... somehow soft, springy,\n |
| 0x159931 | 49 | and slippery at once. I've never tasted its like. |
| 0x159963 | 33 | But this is... hm. This won't do. |
| 0x159985 | 50 | I see, now... How could Her Highness concentrate\n |
| 0x1599b8 | 45 | on studying with temptations like this about? |
| 0x1599e6 | 49 | One must know one's enemies, after all. I shall\n |
| 0x159a18 | 47 | make this sacrifice for the well-being of the\n |
| 0x159a48 | 9 | princess. |
| 0x159a52 | 16 | *Hromf, munch--* |
| 0x159a63 | 15 | Oh... Oh, my... |
| 0x159a73 | 45 | In a matter of seconds, Atuy's entire plate\n |
| 0x159aa1 | 11 | disappears. |
| 0x159aad | 42 | Decadent indeed. Thank you for the Rulu,\n |
| 0x159ad8 | 10 | Lady Atuy. |
| 0x159ae3 | 47 | Munechika clasps her hands together as a sign\n |
| 0x159b13 | 10 | of thanks. |
| 0x159b1e | 10 | My Rulu... |
| 0x159b29 | 40 | Ah, was I... not supposed to eat it all? |
| 0x159b52 | 49 | D-Don't... don't worry about it. There's plenty\n |
| 0x159b84 | 26 | more where that came from. |
| 0x159b9f | 30 | Oh... Hello, Miss Munechika... |
| 0x159bbe | 32 | Rulutieh appears in the doorway. |
| 0x159bdf | 45 | Rulie! Perfect timing. Could you bring some\n |
| 0x159c0d | 10 | more Rulu? |
| 0x159c18 | 42 | Did, uhm... Did you eat all of it already? |
| 0x159c43 | 15 | Not... exactly. |
| 0x159c53 | 14 | You didn't...? |
| 0x159c62 | 45 | "I" didn't, no. But could you make some more? |
| 0x159c90 | 48 | Uhm... I'm sorry, but... I don't have any more\n |
| 0x159cc1 | 21 | ingredients for it... |
| 0x159cd7 | 47 | Hey, it's all right. We'll just pick up a lot\n |
| 0x159d07 | 28 | more tree sap next time, OK? |
| 0x159d24 | 48 | Ah, about that. Due to Rulu's wild popularity,\n |
| 0x159d55 | 47 | sap extraction has seen an unprecedented spike. |
| 0x159d85 | 48 | Small forests around the capital have begun to\n |
| 0x159db6 | 39 | suffer severely, so extraction is now\n |
| 0x159dde | 11 | restricted. |
| 0x159dea | 49 | ...I guess that's what happens when it's people\n |
| 0x159e1c | 46 | who are attracted to it, instead of just ants. |
| 0x159e4b | 29 | Indeed. It has me thinking... |
| 0x159e69 | 44 | I-If you'd still like sweets of some kind,\n |
| 0x159e96 | 23 | you can... try these... |
| 0x159eae | 42 | Rulutieh offers a different plate to the\n |
| 0x159ed9 | 14 | dejected Atuy. |
| 0x159ee8 | 50 | On it sits a batch of confections, crisp, golden\n |
| 0x159f1b | 10 | and round. |
| 0x159f26 | 12 | What's this? |
| 0x159f33 | 39 | I was working on a new recipe today...  |
| 0x159f5b | 47 | Oh, hey, it looks like they turned out pretty\n |
| 0x159f8b | 15 | well this time. |
| 0x159f9b | 46 | Y-Yes... just as you said, Sir Haku, the key\n |
| 0x159fca | 47 | was to fine-tune the temperature of the fire... |
| 0x159ffa | 48 | I seem to remember seeing you two sneak off to\n |
| 0x15a02b | 47 | the kitchens earlier. Working on something new? |
| 0x15a05b | 38 | Thinking up a new kind of sweet, love? |
| 0x15a082 | 49 | I guess. We just tried baking some thinned amam\n |
| 0x15a0b4 | 44 | dough with kondens filling in a gap in the\n |
| 0x15a0e1 | 7 | middle. |
| 0x15a0e9 | 46 | The dough puffs up when we go to bake it, so\n |
| 0x15a118 | 36 | we're calling them... Well, "Puffs." |
| 0x15a13d | 6 | Puffs? |
| 0x15a144 | 47 | That's a strange name, but... it fits, I guess. |
| 0x15a174 | 46 | Indeed. An exotic name and appearance alike... |
| 0x15a1a3 | 48 | Well, we've gotten this far, but we still have\n |
| 0x15a1d4 | 20 | to taste-test. So... |
| 0x15a1e9 | 49 | Y-Yes... I'd appreciate it if you could all try\n |
| 0x15a21b | 34 | some and tell me what you think... |
| 0x15a23e | 28 | Hee hee. Don't mind if I do. |
| 0x15a25b | 27 | I will participate as well. |
| 0x15a277 | 7 | Me too. |
| 0x15a27f | 46 | ...I am also interested in sampling them for\n |
| 0x15a2ae | 7 | myself. |
| 0x15a2b6 | 43 | Each of us grabs a puff from the platter.\n |
| 0x15a2e2 | 47 | In unison, we each take an experimental bite... |
| 0x15a312 | 10 | This is--! |
| 0x15a31d | 18 | Reeaally goooood~! |
| 0x15a330 | 47 | Mm... The crunchy exterior of the amam mixing\n |
| 0x15a360 | 32 | with the kondens' rich flavor... |
| 0x15a381 | 33 | A-Ah, I'm glad you all like it... |
| 0x15a3a3 | 47 | Astounding. The puffed dough creates a hollow\n |
| 0x15a3d3 | 41 | in the middle for the kondens... but how? |
| 0x15a3fd | 49 | Y-You just have to knead properly. My first few\n |
| 0x15a42f | 47 | batches all shriveled up before we discovered\n |
| 0x15a45f | 7 | that... |
| 0x15a467 | 48 | Kneading? True, that process softens the dough\n |
| 0x15a498 | 45 | and eliminates bubbles, but puffing it up...? |
| 0x15a4c6 | 7 | Well... |
| 0x15a4ce | 46 | Rulutieh looks over to me, a little confused\n |
| 0x15a4fd | 30 | on how to answer the question. |
| 0x15a51c | 42 | She made it, sure, but I was the one who\n |
| 0x15a547 | 47 | instructed her on how to do it, since it's...\n |
| 0x15a577 | 12 | complicated. |
| 0x15a584 | 48 | It's mostly because of the moisture trapped in\n |
| 0x15a5b5 | 10 | the dough. |
| 0x15a5c0 | 46 | Moisture? Wait, were you the one who came up\n |
| 0x15a5ef | 29 | with the idea for this, Haku? |
| 0x15a60d | 45 | W-Well... yeah. I understand the principles\n |
| 0x15a63b | 48 | behind it, but I just don't have the practical\n |
| 0x15a66c | 7 | skills. |
| 0x15a674 | 46 | If you wouldn't mind, I am curious as to the\n |
| 0x15a6a3 | 47 | mechanics of how you made the dough rise that\n |
| 0x15a6d3 | 4 | way. |
| 0x15a6d8 | 48 | Well, it took a lot of trial and error, but we\n |
| 0x15a709 | 35 | found if we make the dough into a-- |
| 0x15a72d | 44 | As I begin to explain, I realize I have an\n |
| 0x15a75a | 33 | opportunity to have a little fun. |
| 0x15a77c | 50 | What's this? Could it be the great court scholar\n |
| 0x15a7af | 46 | Nekone has finally found a problem she can't\n |
| 0x15a7de | 6 | crack? |
| 0x15a7e5 | 7 | Nngh... |
| 0x15a7ed | 49 | V-Very well. If there are no other ingredients,\n |
| 0x15a81f | 49 | I should be able to discern the specifics on my\n |
| 0x15a851 | 6 | own... |
| 0x15a858 | 45 | She pops a puff into her mouth as she makes\n |
| 0x15a886 | 37 | this proclamation, focusing intently. |
| 0x15a8ac | 41 | ...Amam powder... milk, salt... eggs...\n |
| 0x15a8d6 | 22 | but that's not all...? |
| 0x15a8ed | 47 | The kondens is making it hard to concentrate... |
| 0x15a91d | 48 | She seems to be too distracted by the taste to\n |
| 0x15a94e | 20 | analyze it properly. |
| 0x15a963 | 46 | If you want to analyze just the outer shell,\n |
| 0x15a992 | 38 | we can prepare one on its own for you? |
| 0x15a9b9 | 34 | N-No! I mean--it would be a waste. |
| 0x15a9dc | 42 | To think such flavor could exist in this\n |
| 0x15aa07 | 47 | world... My experiences are more limited than\n |
| 0x15aa37 | 10 | I thought. |
| 0x15aa42 | 43 | Munechika continues to eat one puff after\n |
| 0x15aa6e | 48 | another, showing no signs of stopping any time\n |
| 0x15aa9f | 5 | soon. |
| 0x15aaa5 | 47 | Mmm. I think it might be even BETTER than the\n |
| 0x15aad5 | 7 | Rulu... |
| 0x15aadd | 35 | Please, have more. I made plenty... |
| 0x15ab01 | 30 | Really? Aw, my little Rulie!\n |
| 0x15ab20 | 14 | Love ya, girl. |
| 0x15ab2f | 46 | You can cook just about anything, can't you?\n |
| 0x15ab5e | 34 | I dunno what I did to deserve you. |
| 0x15ab81 | 32 | You're just too good to be true. |
| 0x15aba2 | 28 | Can I just marry you, Rulie? |
| 0x15abbf | 19 | H-Huh--? M-M-Marr-- |
| 0x15abd3 | 13 | I-I--I, uhm-- |
| 0x15abe1 | 38 | I don't think she's serious, Rulutieh. |
| 0x15ac08 | 7 | Huh...? |
| 0x15ac10 | 44 | Only joking, Rulie. I do love you, really,\n |
| 0x15ac3d | 22 | just... not like that. |
| 0x15ac54 | 44 | H-Heh... Y-You took me by surprise, there... |
| 0x15ac81 | 46 | Please, Miss Atuy, have as many puffs as you\n |
| 0x15acb0 | 7 | like... |
| 0x15acb8 | 20 | Hee hee. Yes, ma'am. |
| 0x15accd | 29 | Atuy reaches for the plate... |
| 0x15aceb | 45 | ...only to find that the mountain of sweets\n |
| 0x15ad19 | 44 | has been reduced to a single, lonesome puff. |
| 0x15ad46 | 47 | In that moment, another hand snaps out like a\n |
| 0x15ad76 | 44 | coiled snake and snatches the final puff up. |
| 0x15ada3 | 4 | Huh? |
| 0x15ada8 | 27 | Mmf... Such sugary bliss... |
| 0x15adc4 | 6 | ...Oh. |
| 0x15adcb | 45 | Positively delectable. I must thank you for\n |
| 0x15adf9 | 17 | your hospitality. |
| 0x15ae0b | 47 | ...ah, perhaps I've eaten more than my share.\n |
| 0x15ae3b | 31 | But I feel strangely wonderful! |
| 0x15ae5b | 50 | With that, Munechika finds a couch to sink into,\n |
| 0x15ae8e | 16 | visibly relaxed. |
| 0x15ae9f | 46 | Atuy continues staring absentmindedly at the\n |
| 0x15aece | 12 | empty plate. |
| 0x15aedb | 41 | I... suppose I feel a little bad for her. |
| 0x15af05 | 50 | Kuon holds about six or seven puffs in her hands\n |
| 0x15af38 | 17 | as she says this. |
| 0x15af4a | 39 | If that's the case, then you could...\n |
| 0x15af72 | 21 | I dunno, share? Mmnf. |
| 0x15af88 | 45 | Not that I'm willing to share my own stash.\n |
| 0x15afb6 | 19 | Perish the thought. |
| 0x15afca | 8 | Rulie... |
| 0x15afd3 | 19 | Uhm... I'm sorry... |
| 0x15afe7 | 46 | I used all the ingredients we had for these,\n |
| 0x15b016 | 39 | and since Rulu and puffs use the same\n |
| 0x15b03e | 14 | ingredients... |
| 0x15b04d | 25 | This is just too cruel... |
| 0x15b067 | 47 | Rulu HAS been very quick to sell out of local\n |
| 0x15b097 | 14 | shops, lately. |
| 0x15b0a6 | 49 | I hardly expected its popularity to boom to the\n |
| 0x15b0d8 | 38 | point of damaging the local ecosystem. |
| 0x15b0ff | 45 | ...Truly, I cannot help but wonder if there\n |
| 0x15b12d | 41 | isn't more to the issue than just that... |
| 0x15b157 | 48 | It's mysterious, y-yeah... but I think you may\n |
| 0x15b188 | 19 | be overthinking it. |
| 0x15b19c | 47 | For such a thing to transpire in the heart of\n |
| 0x15b1cc | 35 | the empire... Hm? What's this here? |
| 0x15b1f0 | 47 | As Munechika listens to Nekone's musings from\n |
| 0x15b220 | 45 | the couch, she notices something across the\n |
| 0x15b24e | 5 | room. |
| 0x15b254 | 14 | Hm? A book...? |
| 0x15b263 | 47 | To see that volume wedged between the shelves\n |
| 0x15b293 | 40 | from across the room... She sure has a\n |
| 0x15b2bc | 16 | mononofu's eyes. |
| 0x15b2cd | 39 | O-Oh, that's--I thought I'd lost it...! |
| 0x15b2f5 | 47 | Does the princess have a habit of hiding away\n |
| 0x15b325 | 35 | the stuff she takes without asking? |
| 0x15b349 | 10 | This is... |
| 0x15b354 | 48 | Munechika flips through the book, pausing on a\n |
| 0x15b385 | 42 | particular page. She flips it around and\n |
| 0x15b3b0 | 12 | displays it. |
| 0x15b3bd | 49 | Is... content like this not considered somewhat\n |
| 0x15b3ef | 8 | extreme? |
| 0x15b3fc | 48 | I can see Rulutieh's entire body twitch at the\n |
| 0x15b42d | 47 | sight of the large illustration in front of us. |
| 0x15b45d | 48 | Splayed across both pages, two young men stare\n |
| 0x15b48e | 47 | into each other's eyes, petals falling around\n |
| 0x15b4be | 5 | them. |
| 0x15b4c4 | 47 | Is it me, or are they just a LITTLE too close\n |
| 0x15b4f4 | 12 | for comfort? |
| 0x15b501 | 39 | Does this... perchance belong to you,\n |
| 0x15b529 | 14 | Lady Rulutieh? |
| 0x15b538 | 27 | U-Uhm... well... th-that... |
| 0x15b554 | 50 | Rulutieh stutters, going rigid as the whole room\n |
| 0x15b587 | 13 | turns to her. |
| 0x15b595 | 48 | N-No, I believe... Miss Anju must have left it\n |
| 0x15b5c6 | 8 | here...? |
| 0x15b5cf | 47 | Oh, boy. That's possibly the worst answer she\n |
| 0x15b5ff | 17 | could have given. |
| 0x15b611 | 38 | The room fills with deafening silence. |
| 0x15b638 | 13 | Her Highness? |
| 0x15b646 | 6 | Ohh... |
| 0x15b64d | 49 | Rulutieh seems to realize the full implications\n |
| 0x15b67f | 48 | of what she just said, curling up and cradling\n |
| 0x15b6b0 | 9 | her head. |
| 0x15b6ba | 41 | I see. If this belongs to the princess... |
| 0x15b6e4 | 43 | Her Highness must have brought all these,\n |
| 0x15b710 | 8 | as well. |
| 0x15b719 | 46 | With that, she turns and begins to pull book\n |
| 0x15b748 | 26 | after book from the shelf. |
| 0x15b763 | 17 | Wh-What are you-- |
| 0x15b775 | 46 | Confiscating these volumes. I have concluded\n |
| 0x15b7a4 | 47 | that such material is far too stimulating for\n |
| 0x15b7d4 | 4 | her. |
| 0x15b7d9 | 47 | She quickly tucks the whole lot away, leaving\n |
| 0x15b809 | 22 | a barren shelf behind. |
| 0x15b820 | 50 | Nonchalantly, she selects the book on the top of\n |
| 0x15b853 | 31 | the stack and begins to read... |
| 0x15b873 | 39 | Oh, th-that's... the limited edition... |
| 0x15b89b | 41 | Rulutieh collapses to the ground again,\n |
| 0x15b8c5 | 20 | muttering distantly. |
| 0x15b8da | 49 | Munechika, however, is far too engrossed in her\n |
| 0x15b90c | 35 | reading to notice the odd behavior. |
| 0x15b930 | 42 | None of us can muster the courage to say\n |
| 0x15b95b | 41 | anything as she reads in intense silence. |
| 0x15b985 | 46 | Ah, I would do well to follow her example...\n |
| 0x15b9b4 | 46 | Such singular focus for one book. I'd expect\n |
| 0x15b9e3 | 13 | nothing less. |
| 0x15b9f1 | 48 | Nekone sounds impressed, but it's all I can do\n |
| 0x15ba22 | 22 | to just shake my head. |
| 0x15ba39 | 41 | I get the feeling we've just traded one\n |
| 0x15ba63 | 25 | troublemaker for another. |
| 0x15c022 | 41 | Urgh, it gets cold out here at night...\n |
| 0x15c04c | 31 | Shouldn't have had so much tea. |
| 0x15c06c | 43 | As I make my way down the hall toward the\n |
| 0x15c098 | 47 | toilets, I notice a figure leaving her room--\n |
| 0x15c0c8 | 5 | Kuon. |
| 0x15c0ce | 46 | What's she doing up this late? Does she need\n |
| 0x15c0fd | 25 | the bathroom, too, or...? |
| 0x15c117 | 48 | She turns in completely the opposite direction\n |
| 0x15c148 | 29 | from me, moving with purpose. |
| 0x15c166 | 47 | As I watch her go, she heads not for the main\n |
| 0x15c196 | 48 | entrance, but slinks out the smaller back one... |
| 0x15c1c7 | 39 | Where could she be going, at this hour? |
| 0x15c1ef | 46 | Curiosity gets the better of me. I decide to\n |
| 0x15c21e | 30 | follow and slip out after her. |
| 0x15c23d | 49 | Kuon walks calmly ahead on the road, looking up\n |
| 0x15c26f | 26 | at the moon as she goes... |
| 0x15c28a | 47 | And here I am, skulking in the shadows behind\n |
| 0x15c2ba | 4 | her. |
| 0x15c2bf | 50 | What business could have called her outside this\n |
| 0x15c2f2 | 14 | late at night? |
| 0x15c301 | 49 | Kuon, who had been walking without breaks up to\n |
| 0x15c333 | 47 | this point, suddenly stops in front of a fence. |
| 0x15c363 | 46 | She looks up through it, eyeing a large tree\n |
| 0x15c392 | 31 | growing on the estate within... |
| 0x15c3b2 | 30 | Just wait a little bit longer. |
| 0x15c3d1 | 30 | No, it won't take... I'll...\n |
| 0x15c3f0 | 23 | ...not going to happen. |
| 0x15c408 | 45 | Now she's muttering to herself. Is she just\n |
| 0x15c436 | 13 | sleepwalking? |
| 0x15c444 | 49 | But by the looks of it, she seems to be pausing\n |
| 0x15c476 | 27 | and... answering questions? |
| 0x15c492 | 44 | It sounds like she's talking with someone,\n |
| 0x15c4bf | 8 | but who? |
| 0x15c4c8 | 32 | She did this once before, too... |
| 0x15c4e9 | 39 | But we're alone in the dead of night.\n |
| 0x15c511 | 24 | Nobody is around but us. |
| 0x15c52a | 35 | ...understand you're... about me.\n |
| 0x15c54e | 16 | ...not a child-- |
| 0x15c55f | 38 | Fine. You may have a little more time. |
| 0x15c586 | 44 | But remember... not... so selfishly forever. |
| 0x15c5b3 | 48 | Is someone else there? It couldn't be a ghost... |
| 0x15c5e4 | 49 | The branches of the tree sway slightly, and the\n |
| 0x15c616 | 40 | night is plunged into silence once more. |
| 0x15c63f | 23 | I don't have... left... |
| 0x15c657 | 46 | Kuon sighs deeply, her eyes returning to the\n |
| 0x15c686 | 4 | sky. |
| 0x15c68b | 48 | I'm not sure I understand what I just saw, but\n |
| 0x15c6bc | 46 | I get the feeling I wasn't supposed to see it. |
| 0x15c6eb | 47 | I'm more anxious than I thought. Suddenly the\n |
| 0x15c71b | 47 | wind feels colder, and sweat trickles down my\n |
| 0x15c74b | 7 | back... |
| 0x15c753 | 33 | Nngh. Cold. I'd better head back. |
| 0x15c779 | 45 | ...I can't shake the feeling, however, that\n |
| 0x15c7a7 | 38 | someone is watching me as I turn away. |
| 0x15c7ce | 43 | But when I look back at Kuon, she's still\n |
| 0x15c7fa | 25 | staring up at the moon... |
| 0x15c814 | 49 | ...and the longer she stares, it seems like her\n |
| 0x15c846 | 27 | eyes are starting to water. |
| 0x15df76 | 39 | You want me to... go shopping with you? |
| 0x15df9e | 49 | Yes. Her Highness has requested a certain item,\n |
| 0x15dfd0 | 42 | and I would enjoy your help in finding it. |
| 0x15dffb | 46 | In truth, this is new territory to me, and I\n |
| 0x15e02a | 48 | could use the aid of someone more knowledgeable. |
| 0x15e05b | 50 | Eh. Not like I'm doing anything more productive.\n |
| 0x15e08e | 47 | I'll come along if you treat me to lunch, fair? |
| 0x15e0be | 41 | A fair accord. Let's be on our way, then. |
| 0x15e0e8 | 37 | W-Wait, you mean right now!? H-Hey--! |
| 0x15e10e | 3 | So? |
| 0x15e112 | 3 | Hm? |
| 0x15e116 | 44 | Don't "hm?" me. What are we supposed to be\n |
| 0x15e143 | 12 | looking for? |
| 0x15e150 | 40 | I admit I'm not quite certain, myself... |
| 0x15e179 | 43 | Huh? What do you mean, "not quite certain"? |
| 0x15e1a5 | 50 | All Her Highness gave me was a map to a shop and\n |
| 0x15e1d8 | 49 | the title of a book she wishes to obtain from it. |
| 0x15e20a | 7 | A book? |
| 0x15e212 | 47 | Yes. Her Highness has long hated studying, so\n |
| 0x15e242 | 49 | this new interest in books is quite the welcome\n |
| 0x15e274 | 7 | change. |
| 0x15e27c | 46 | It would seem I'm finally getting through to\n |
| 0x15e2ab | 41 | her. She's begun to express interest in\n |
| 0x15e2d5 | 14 | politics, too. |
| 0x15e2e4 | 51 | The imperial princess, studying and participating\n |
| 0x15e318 | 46 | in the court. The end of the world is upon us. |
| 0x15e347 | 49 | Regardless, it is unfortunate that the imperial\n |
| 0x15e379 | 47 | markets see new shops open and old ones close\n |
| 0x15e3a9 | 11 | so often... |
| 0x15e3b5 | 51 | It's an unfamiliar realm to me. I appreciate your\n |
| 0x15e3e9 | 46 | help in locating this particular store, Lord\n |
| 0x15e418 | 5 | Haku. |
| 0x15e41e | 49 | It's no big deal, really, but where exactly are\n |
| 0x15e450 | 28 | we looking for this place..? |
| 0x15e46d | 25 | It should be around here. |
| 0x15e487 | 10 | This is... |
| 0x15e492 | 49 | We turn down a street with shops all displaying\n |
| 0x15e4c4 | 48 | books and paintings, mobbed by groups of young\n |
| 0x15e4f5 | 6 | women. |
| 0x15e4fc | 49 | Oh, I've been here before. If I recall, this is\n |
| 0x15e52e | 43 | where Rulutieh came when I first arrived... |
| 0x15e55a | 49 | I only caught a glimpse last time, but now, the\n |
| 0x15e58c | 47 | male characters on various wares are plain to\n |
| 0x15e5bc | 4 | see. |
| 0x15e5c1 | 43 | It's a rather... decorated place, isn't it? |
| 0x15e5ed | 49 | Munechika looks around, a little taken aback by\n |
| 0x15e61f | 22 | the colorful displays. |
| 0x15e636 | 43 | Many of the titles on display have highly\n |
| 0x15e662 | 41 | stylized covers. This must be so-called\n |
| 0x15e68c | 21 | "popular literature." |
| 0x15e6a2 | 34 | This is what she's looking for...? |
| 0x15e6c5 | 47 | Why are there only guys in the illustrations?\n |
| 0x15e6f5 | 48 | I'd have thought there'd be female characters,\n |
| 0x15e726 | 4 | too. |
| 0x15e72b | 50 | Is that... a print of Oshtor? And that one looks\n |
| 0x15e75e | 17 | like Mikazuchi... |
| 0x15e770 | 46 | They ARE the Twin Shields, I guess. It makes\n |
| 0x15e79f | 46 | sense they'd be pretty popular in the capital. |
| 0x15e7ce | 46 | But I'm... not really sure I get why they're\n |
| 0x15e7fd | 43 | gazing into each other's eyes like that...? |
| 0x15e829 | 25 | S-Sir Haku? Why are you-- |
| 0x15e843 | 29 | Hm? That voice sounds like... |
| 0x15e861 | 18 | Ah, Lady Rulutieh. |
| 0x15e874 | 10 | H-Hello... |
| 0x15e87f | 44 | Fancy finding you here, Rulutieh. You were\n |
| 0x15e8ac | 29 | around here last time, too... |
| 0x15e8ca | 44 | I, uhm... What... brings you here, Sir Haku? |
| 0x15e8f7 | 33 | Oh, I'm just tagging along today. |
| 0x15e919 | 48 | Munechika promised to treat me if I helped her\n |
| 0x15e94a | 36 | with some shopping for the princess. |
| 0x15e96f | 10 | I-I see... |
| 0x15e97a | 28 | You out shopping, too, then? |
| 0x15e997 | 7 | Huh...? |
| 0x15e99f | 47 | Rulutieh flinches and quickly hides something\n |
| 0x15e9cf | 38 | behind her back, her cheeks reddening. |
| 0x15e9f6 | 28 | I-I wasn't... really, uhm... |
| 0x15ea13 | 47 | I don't really understand, but if she doesn't\n |
| 0x15ea43 | 43 | want me to pry, I'll pretend I didn't see\n |
| 0x15ea6f | 9 | anything. |
| 0x15ea79 | 47 | I gather you're familiar with this area, Lady\n |
| 0x15eaa9 | 46 | Rulutieh. Could you perhaps help us locate a\n |
| 0x15ead8 | 5 | shop? |
| 0x15eade | 10 | A... shop? |
| 0x15eae9 | 49 | Rulutieh looks over the map Munechika produces,\n |
| 0x15eb1b | 44 | stiffening upon seeing the circled location. |
| 0x15eb48 | 32 | Y-You're sure it's... THAT shop? |
| 0x15eb69 | 45 | Yes, by Her Highness's command. I am certain. |
| 0x15eb97 | 29 | P-Princess Anju commanded y-- |
| 0x15ebb5 | 38 | Are you well, milady? You look pale... |
| 0x15ebdc | 25 | N-No, I--It's... nothing. |
| 0x15ebf6 | 50 | I see. In any case, I was instructed to retrieve\n |
| 0x15ec29 | 21 | a particular title... |
| 0x15ec3f | 41 | Rulutieh fearfully looks at the note in\n |
| 0x15ec69 | 46 | Munechika's hands as the general holds it up\n |
| 0x15ec98 | 8 | for her. |
| 0x15eca1 | 50 | "Clandestine Love! ~ The Cocky General Seeks the\n |
| 0x15ecd4 | 23 | Prince's Secret Sword!" |
| 0x15ecf0 | 48 | That's... a strange title. Is this the kind of\n |
| 0x15ed21 | 26 | stuff that's popular here? |
| 0x15ed3c | 46 | The name on the note doesn't ring any bells,\n |
| 0x15ed6b | 15 | but Rulutieh... |
| 0x15ed7b | 16 | What do I do...? |
| 0x15ed8c | 48 | Rulutieh mutters to herself with tears welling\n |
| 0x15edbd | 40 | up in her eyes, Munechika's gaze on her. |
| 0x15ede6 | 23 | Oh? Ah, could it be...? |
| 0x15edfe | 46 | ...Of all people to encounter in this place,\n |
| 0x15ee2d | 30 | I hardly expected to find you. |
| 0x15ee4c | 44 | And here was I, about to express the same.\n |
| 0x15ee79 | 40 | Truly rare to find you about the city,\n |
| 0x15eea2 | 15 | Lady Munechika. |
| 0x15eeb2 | 51 | An auspicious occasion. Come to do some shopping,\n |
| 0x15eee6 | 8 | have we? |
| 0x15eeef | 49 | Indeed. I've been sent here to handle an affair\n |
| 0x15ef21 | 33 | as part of my duties as Guardian. |
| 0x15ef43 | 18 | Ah, is that so...? |
| 0x15ef56 | 48 | I remember this guy. Last time I saw him, I...\n |
| 0x15ef87 | 47 | bumped into him and scattered all his papers.\n |
| 0x15efb7 | 6 | Right. |
| 0x15efbe | 47 | So he's familiar with Munechika? Going by how\n |
| 0x15efee | 44 | Nekone addressed him last time, he must be\n |
| 0x15f01b | 12 | important... |
| 0x15f028 | 44 | Why do I feel like I've seen him somewhere\n |
| 0x15f055 | 10 | before...? |
| 0x15f060 | 27 | Ah, hello again, my friend. |
| 0x15f07c | 20 | Oh, you remember me? |
| 0x15f091 | 47 | Of course. How could I ever forget a model as\n |
| 0x15f0c1 | 49 | perfect as y... Ah, forgive me. Merely thinking\n |
| 0x15f0f3 | 6 | aloud. |
| 0x15f0fa | 51 | ...Why am I REALLY uncomfortable all of a sudden?\n |
| 0x15f12e | 36 | I have chills going down my spine... |
| 0x15f153 | 49 | A-Ah, uhm--pardon me, but could you... possibly\n |
| 0x15f185 | 22 | be, uhm... Sir Raurau? |
| 0x15f19c | 6 | Raurau |
| 0x15f1a3 | 42 | Oh, dear, have I been found out already?\n |
| 0x15f1ce | 42 | I really should know better than to hope\n |
| 0x15f1f9 | 12 | otherwise... |
| 0x15f206 | 44 | He seems strangely happy, despite his words. |
| 0x15f233 | 41 | I'm, uhm... q-quite a fan of your work.\n |
| 0x15f25d | 48 | If it's... not much trouble, would you... mind\n |
| 0x15f28e | 16 | signing this...? |
| 0x15f29f | 48 | Rulutieh produces the book she'd hidden behind\n |
| 0x15f2d0 | 46 | her back when we bumped into her, holding it\n |
| 0x15f2ff | 4 | out. |
| 0x15f304 | 50 | Oh... I'm sorry, dear, but I make it a matter of\n |
| 0x15f337 | 46 | policy not to give autographs in my personal\n |
| 0x15f366 | 5 | time. |
| 0x15f36c | 47 | I-I see. I'm... s-sorry to have bothered you,\n |
| 0x15f39c | 7 | then... |
| 0x15f3a4 | 50 | ...Ah, but perhaps fate has arranged our meeting\n |
| 0x15f3d7 | 46 | today. Could I have the pleasure of your name? |
| 0x15f406 | 18 | Huh? Uhm... I'm... |
| 0x15f419 | 47 | Rulutieh tells the man her name, and he takes\n |
| 0x15f449 | 47 | the book from her, writing on the inside cover. |
| 0x15f479 | 22 | To... Miss Rulutieh... |
| 0x15f490 | 50 | Th-Thank you very much! I'll be sure to treasure\n |
| 0x15f4c3 | 8 | this...! |
| 0x15f4cc | 41 | Now, I'm afraid I have to be on my way.\n |
| 0x15f4f6 | 28 | If you'll excuse me, please. |
| 0x15f513 | 45 | The man bows, then glides away, moving with\n |
| 0x15f541 | 19 | elegance and grace. |
| 0x15f555 | 49 | Rulutieh looks on, watching him leave with eyes\n |
| 0x15f587 | 21 | full of admiration... |
| 0x15f59d | 12 | ...Rulutieh? |
| 0x15f5aa | 3 | Ah? |
| 0x15f5ae | 47 | Rulutieh snaps out of her stupor, coming back\n |
| 0x15f5de | 30 | to reality as I call her name. |
| 0x15f5fd | 34 | U-Uhm... I--y-you misunderstand.\n |
| 0x15f620 | 22 | Sir R-Raurau is, uhm-- |
| 0x15f637 | 47 | What are you getting so worked up for? C'mon,\n |
| 0x15f667 | 49 | let's get out of the street. We're blocking the\n |
| 0x15f699 | 4 | way. |
| 0x15f69e | 12 | Ow--owow ow! |
| 0x15f6ab | 50 | I don't know why, but Rulutieh turns and pinches\n |
| 0x15f6de | 45 | my arm as hard as she can, tears in her eyes. |
| 0x15f70c | 47 | ...Here, this--this is the one you're looking\n |
| 0x15f73c | 6 | for... |
| 0x15f743 | 39 | Thank you. Your assistance is greatly\n |
| 0x15f76b | 19 | appreciated, child. |
| 0x15f77f | 47 | Munechika thanks Rulutieh as she receives the\n |
| 0x15f7af | 14 | book from her. |
| 0x15f7be | 46 | Rulutieh ended up saying something about the\n |
| 0x15f7ed | 47 | shop being "too complex" and went in alone to\n |
| 0x15f81d | 9 | get it... |
| 0x15f827 | 47 | So this is the volume that Her Highness seeks\n |
| 0x15f857 | 13 | so earnestly. |
| 0x15f865 | 47 | Munechika carefully inspects the cover of the\n |
| 0x15f895 | 18 | book in her hands. |
| 0x15f8a8 | 9 | Oh, wai-- |
| 0x15f8b2 | 50 | Rulutieh tries--unsuccessfully--to pull the book\n |
| 0x15f8e5 | 42 | back as Munechika opens it to a colorful\n |
| 0x15f910 | 8 | picture. |
| 0x15f919 | 4 | Huh? |
| 0x15f91e | 39 | Suddenly, my vision goes entirely dark. |
| 0x15f946 | 46 | Hm? Does something trouble you, Lady Rulutieh? |
| 0x15f975 | 48 | It's hard to tell, but... I think Rulutieh put\n |
| 0x15f9a6 | 42 | her hands over my eyes? Why in the world-- |
| 0x15f9d1 | 45 | Uh, Rulutieh? I can't really... see anything. |
| 0x15f9ff | 46 | U-Uhm. Just--uhm. Please, th-there's nothing\n |
| 0x15fa2e | 19 | to w-worry about... |
| 0x15fa42 | 29 | This clearly isn't "nothing." |
| 0x15fa60 | 47 | For a moment, I thought I caught a glimpse of\n |
| 0x15fa90 | 44 | two figures nestling together without much\n |
| 0x15fabd | 11 | clothing... |
| 0x15fac9 | 47 | ...but I think it's better if I keep my mouth\n |
| 0x15faf9 | 5 | shut. |
| 0x15faff | 48 | M-Miss Munechika, uhm... c-could you possibly,\n |
| 0x15fb30 | 5 | ah... |
| 0x15fb36 | 44 | The only sound I can hear besides the foot\n |
| 0x15fb63 | 46 | traffic nearby is the slow turning of pages... |
| 0x15fb92 | 50 | If I had to guess, I'd say they're both intently\n |
| 0x15fbc5 | 46 | looking through the book while I can't see it. |
| 0x15fbf4 | 6 | Oh...? |
| 0x15fbfb | 50 | Rulutieh stands behind me as she covers my eyes,\n |
| 0x15fc2e | 48 | and I can feel her breath growing hotter on my\n |
| 0x15fc5f | 5 | neck. |
| 0x15fc65 | 26 | What... does this mean...? |
| 0x15fc80 | 24 | See, that... and then... |
| 0x15fc99 | 46 | Their whispered conversation escapes me, too\n |
| 0x15fcc8 | 38 | many unfamiliar terms passing my ears. |
| 0x15fcef | 16 | ...Ah! Ahem! Mm. |
| 0x15fd00 | 49 | Munechika, finally, seems to snap out of it and\n |
| 0x15fd32 | 18 | clears her throat. |
| 0x15fd45 | 48 | One can see quite plainly why this material is\n |
| 0x15fd76 | 47 | so... desired. I had no idea such passion was\n |
| 0x15fda6 | 9 | possible. |
| 0x15fdb0 | 45 | Her Highness is far too young to read books\n |
| 0x15fdde | 39 | like this, so I'll, ah. Hold onto it.\n |
| 0x15fe06 | 19 | Until she is ready. |
| 0x15fe1a | 47 | With that, Munechika quickly secrets the book\n |
| 0x15fe4a | 5 | away. |
| 0x15fe50 | 21 | Several days later... |
| 0x15fe66 | 25 | Is Lady Rulutieh present? |
| 0x15fe80 | 46 | Ah, Miss Munechika...! I've been waiting for\n |
| 0x15feaf | 4 | you. |
| 0x15feb4 | 29 | Shall we be on our way, then? |
| 0x15fed2 | 13 | Yes, let's... |
| 0x15fee0 | 49 | The two of them chat happily as they take their\n |
| 0x15ff12 | 17 | leave of the inn. |
| 0x15ff24 | 50 | ...Is it just me, or have those two been hanging\n |
| 0x15ff57 | 15 | out a lot more? |

## 8. Formato de saida EXIGIDO
Escreva `translations_18_01.json` com a forma:
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
