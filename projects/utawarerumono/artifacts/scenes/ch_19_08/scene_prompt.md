# Cena ch_19_08 — pacote de traducao (2018 linhas)

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
| Anju | Personagem | Anju | manter_original | moderate |
| Atuy | Personagem | Atuy | manter_original | none |
| Boro-Gigiri | Criatura | Boro-Gigiri | manter_original | none |
| Dekopompo | Personagem | Dekopompo | manter_original | none |
| General of the Right | Titulo | General da Direita | traduzir | major |
| Gigiri | Criatura | Gigiri | manter_original | none |
| Girl | UI | Garota | traduzir | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Hakurokaku | Local | Hakurokaku | manter_original | none |
| Highness | Titulo | Alteza | traduzir | none |
| Honoka | Personagem | Honoka | manter_original | none |
| Imperial Capital | Local | Capital Imperial | traduzir | none |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kiwru | Personagem | Kiwru | manter_original | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Man | UI | Homem | traduzir | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikazuchi | Personagem | Mikazuchi | manter_original | moderate |
| Mito | Personagem | Mito | manter_original | none |
| Moznu | Personagem | Moznu | manter_original | none |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Nosuri | Personagem | Nosuri | manter_original | none |
| Nosuri Bandits | Organizacao | Bandidos Nosuri | traduzir | none |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Ougi | Personagem | Ougi | manter_original | none |
| Rulie | Personagem | Rulie | manter_original | none |
| Rulu | Personagem | Rulu | manter_original | none |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Saraana | Personagem | Saraana | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
| Uruuru | Personagem | Uruuru | manter_original | none |
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
### Moznu — criticality: low
- Moznu — `voice_criticality: low`. Criminoso (antagonista menor); registro grosseiro.
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
- **Figuras de memoria (Woman/Man)** (major): Use rotulos genericos (Mulher/Homem/Mestre). NAO resolva quem sao nem o vinculo com Haku. Preserve o tom enigmatico. (Obs.: 'Master Ukon' do Maroro NAO e isto — e so o honorifico do Ukon.)

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `waiting.` -> `esperar.` (Ukon, 14_03)
- `Huh?` -> `Hein?` (Haku, 11_06)
- `like that.` -> `assim.` (Ukon, 12_16)
- `over.` -> `logo.` (Haku, 15_03)
- `streets.` -> `ruas.` (Haku, 18_01)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `nearby.` -> `perto.` (Ukon, 12_15)
- `What?` -> `Que?` (Haku, 12_02)
- `then.` -> `então.` (Kuon, 13_01)
- `time.` -> `vez.` (Raurau, 18_01)
- `else.` -> `mais.` (Garota, 16_03)
- `Um...` -> `Ahn...` (Kuon, 11_07)
- `but...` -> `mas...` (Kuon, 12_16)
- `this...` -> `isto...` (Kuon, 11_08)
- `Master.` -> `Mestre.` (Homem, 12_14)
- `tea...` -> `chá...` (Protagonista (narração), 18_01)
- `Oh, thanks.` -> `Ah, obrigado.` (Haku, 11_09)
- `tea.` -> `chá.` (Haku, 17_01)
- `right now...` -> `agora...?` (Protagonista, 18_01)
- `This way.` -> `Por aqui.` (Mulher, 14_06)
- `Ah...` -> `Ah...` (Haku, 13_01)
- `child.` -> `criança.` (Haku, 17_01)
- `right?` -> `né?` (Haku, 12_03)
- `R-Right...` -> `C-Certo...` (Haku, 11_09)
- `Hm...?` -> `Hum...?` (Kuon, 13_02)
- `Gah!` -> `Ai!` (Man, 13_01)
- `Oh...` -> `Ah...` (Kuon, 13_01)
- `going.` -> `indo.` (Haku, 16_01)
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `S-Sure...` -> `P-Pode deixar...` (Haku, 13_08)
- `water.` -> `água.` (Haku, 13_03)
- `to you.` -> `com você.` (Ukon, 13_02)
- `For now.` -> `Por ora.` (Ukon, 15_05)
- `more.` -> `mais.` (Anju, 18_01)
- `Is something the matter?` -> `Aconteceu alguma coisa?` (Kuon, 12_09)
- `Hmhm...` -> `Hmhm...` (Garota, 16_01)
- `...Uh...` -> `...Ãh...` (Kuon, root)
- `anywhere.` -> `lugar nenhum.` (Atuy, 16_01)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `for you.` -> `para você.` (Ougi, 13_08)
- `*THUD*` -> `*BAQUE*` (Kuon, 13_01)
- `ground.` -> `do chão.` (Man, root)
- `Hup.` -> `Upa.` (Kuon, 11_07)
- `H-Haku!?` -> `Q-Haku!?` (Kuon, 18_01)
- `are you?` -> `coisa assim, vai?` (Haku, 13_02)
- `Hm...` -> `Hm...` (Moznu, 13_05)
- `Wh--` -> `Q--` (Haku, 11_07)
- `...Whew.` -> `...Ufa.` (Haku, 17_01)
- `Oh!` -> `Ah!` (Garota, 17_01)
- `face.` -> `rosto.` (Rulutieh, 16_02)
- `Wh-What?` -> `Q-Quê?` (Haku, 11_09)
- `H-Hello...` -> `O-Olá...` (Rulutieh, 18_01)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `What the--` -> `Mas que--` (Haku, 11_03)
- `now.` -> `já.` (Kuon, 14_04)
- `like that?` -> `assim?` (Haku, 15_01)
- `Oh, right...` -> `Ah, verdade...` (Protagonista, 17_01)
- `dance.` -> `dança.` (Garota, 19_05)
- `I see.` -> `Sim.` (Haku, 12_17)
- `again.` -> `vez.` (Ougi, 13_05)
- `Are you serious...?` -> `É sério mesmo...?` (Ukon, 17_04)
- `*FWIP*` -> `*VUP*` (SYSTEM, 14_03)
- `silence.` -> `silêncio.` (Narrador, 14_06)
- `much.` -> `isso.` (Ukon, 13_09)
- `So be it.` -> `Assim seja.` (Homem, 16_02)
- `Heh heh heh...` -> `Hehe hehe...` (Haku, 19_07)
- `Wha--!?` -> `Quê--!?` (Haku, 17_01)
- `Eep!` -> `Iiep!` (Kuon, 11_11)
- `grin.` -> `sorriso.` (Haku, 18_01)
- `*Smirk*` -> `*Sorriso malicioso*` (Homem, 19_07)
- `least.` -> `enfim.` (Ukon, 12_12)
- `same.` -> `assim.` (Haku, 15_05)
- `stories.` -> `histórias.` (Haku, 13_01)
- `respect.` -> `respeito.` (Haku, 16_01)
- `now?` -> `agora?` (Haku, 17_04)
- `admiration.` -> `admiração.` (Haku, 13_02)
- `myself.` -> `sozinho.` (Haku, 18_01)
- `Very well.` -> `Sim.` (Nekone, 15_01)
- `weapons...` -> `armas...` (Haku, 17_03)
- `Is that it?` -> `É isso?` (Haku, 15_01)
- `B-Brother...` -> `I-Irmão...` (Nekone, 15_06)
- `Cheers!` -> `Saúde!` (Homens, 14_04)
- `other.` -> `um ao outro.` (Kiwru, 16_01)
- `too?` -> `também?` (Maroro, 17_01)
- `everything.` -> `tudo.` (Maroro, 19_06)
- `Hmm...` -> `Hum...` (Haku, 14_10)
- `There.` -> `Pronto.` (Kuon, 13_05)
- `person.` -> `terrível.` (Nekone, 15_03)
- `That's all.` -> `É isso.` (Ukon, 13_02)
- `it?` -> `isso?` (Nosuri, 18_01)
- `like this.` -> `dessas.` (Kuon, 17_04)
- `picture.` -> `a mensagem.` (Haku, 15_03)
- `That's...` -> `Isso...` (Haku, 15_01)
- `Something wrong?` -> `Algum problema?` (Kuon, 11_07)
- `you...` -> `você...` (Haku, 12_11)
- `Gah!?` -> `Gah!?` (Haku, 13_01)
- `hall.` -> `corredor.` (Atuy, 16_01)
- `Hrm...` -> `Hmm...` (Kuon, 15_03)
- `I see...` -> `Entendo...` (Haku, 12_04)
- `hungry.` -> `com fome.` (Kuon, 18_01)
- `...What?` -> `...Quê?` (Haku, 11_07)
- `Y-Yeah...` -> `É-É...` (Kuon, root)
- `Who're they?` -> `Quem são elas?` (Kuon, 13_04)
- `Man` -> `Hom` (Sistema, 12_04)
- `Woman` -> `Mulher` (sistema, 14_07)
- `kid.` -> `miúdo.` (Haku, 18_01)
- `for?` -> `pra?` (Haku, 18_01)
- `Two...\n` -> `Dois...\n` (Kuon, 12_11)
- `one...` -> `uma...` (Oshtor, 17_04)
- `Haku & Ukon` -> `Haku & Ukon` (SISTEMA, 17_01)
- `Take this!` -> `Tome isso!` (Rulutieh, 19_04)
- `immediately.` -> `na hora.` (Haku, 14_04)
- `Bwahahahaha!` -> `Bwahahahaha!` (Ukon/Homens, 14_04)
- `vivid red.` -> `vermelho vivo.` (Garota, 19_06)
- `later.` -> `depois.` (Moznu, 13_05)
- `to them.` -> `os chama.` (Narrador, 14_06)
- `Here you go.` -> `Aqui está.` (Kuon, 15_02)
- `thanks.` -> `de nada.` (Ukon, 16_01)
- `Cheers.` -> `Saúde.` (Haku, 14_04)
- `fine.` -> `Tá.` (Haku, 16_01)
- `I really do worry... You don't have to stay here.\n` -> `Eu me preocupo mesmo... Você não precisa ficar aqui.\n` (Mulher (memória), root)
- `You can always...` -> `Você sempre pode...` (Mulher (memória), root)
- `...You know you can come back anytime.` -> `...Sabe que pode voltar quando quiser.` (Mulher (memória), root)
- `Well...` -> `Bom...` (Haku, 12_03)
- `...You seem so distant, these days.` -> `...Você anda tão distante esses dias.` (Mulher (memória), root)
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
- Moznu: `Ha! Well done, Nosuri. A right impressive show,\n` -> `Ha! Bom trabalho, Nosuri. Foi uma boa encenação,\n`
- Moznu: `this.` -> `essa.`
- Moznu: `Heh heh. Now, ain't this one a beauty? Lookers\n` -> `Heh heh. Ora, essa aqui é uma beldade. Cara\n`
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
| 0x19143c | 46 | Dear sister, it would appear the tea is ready. |
| 0x19146b | 25 | Hm. Ah... A lovely scent. |
| 0x191485 | 50 | I was recently fortunate enough to acquire these\n |
| 0x1914b8 | 49 | leaves from Nagira... Tea of once-in-a-lifetime\n |
| 0x1914ea | 48 | rarity. The cost was dear, but worth every coin. |
| 0x19151b | 49 | Very well done. It seems you have improved your\n |
| 0x19154d | 15 | skills as well. |
| 0x19155d | 32 | Your approval is my vindication. |
| 0x19157e | 35 | Would you like some as well, Kiwru? |
| 0x1915a2 | 14 | Please, yes... |
| 0x1915b1 | 45 | ...So... what exactly are you two doing here? |
| 0x1915df | 50 | When I get back to the Hakurokaku, I find Nosuri\n |
| 0x191612 | 49 | and Ougi lounging around like they own the place. |
| 0x191644 | 46 | Oh? You've finally returned! You kept us all\n |
| 0x191673 | 8 | waiting. |
| 0x19167c | 44 | Don't blame me. I don't recall anyone ever\n |
| 0x1916a9 | 43 | making an appointment. So what do you want? |
| 0x1916d5 | 46 | What are you talking about? You were the one\n |
| 0x191704 | 26 | that told us to come here. |
| 0x19171f | 4 | Huh? |
| 0x191724 | 46 | That's exactly why we came all the way here.\n |
| 0x191753 | 41 | To reject us now... What a heartless man! |
| 0x19177d | 48 | Hey, hold on. I don't remember saying anything\n |
| 0x1917ae | 10 | like that. |
| 0x1917b9 | 42 | Hahaha! You card, you! By the way, is it\n |
| 0x1917e4 | 45 | lunchtime yet? I'm famished! For today, I'm\n |
| 0x191812 | 20 | thinking... poultry. |
| 0x191827 | 22 | ...This is hopeless.\n |
| 0x19183e | 20 | She's not listening. |
| 0x191853 | 42 | Whatever could be the matter, Haku? Your\n |
| 0x19187e | 41 | expression bespeaks a sudden... sourness. |
| 0x1918a8 | 34 | Argh... Look, can I have a moment? |
| 0x1918cb | 36 | I drag Ougi to a corner of the room. |
| 0x1918f0 | 48 | Your sister's getting me nowhere, so I'm going\n |
| 0x191921 | 13 | to ask you... |
| 0x19192f | 49 | Why are you two still in the capital? I thought\n |
| 0x191961 | 46 | you were going into hiding until things blow\n |
| 0x191990 | 5 | over. |
| 0x191996 | 48 | Aha... Judging by your reaction, I presume you\n |
| 0x1919c7 | 36 | have not heard the news from Oshtor. |
| 0x1919ec | 46 | He has arranged matters so that we will take\n |
| 0x191a1b | 48 | residence here as well. You do need more help,\n |
| 0x191a4c | 11 | do you not? |
| 0x191a58 | 46 | Oshtor's proposal was particularly favorable\n |
| 0x191a87 | 15 | to us, as well. |
| 0x191a97 | 50 | I think it's a good idea, Haku. With Ougi on our\n |
| 0x191aca | 49 | side, we will be able to accomplish a great deal. |
| 0x191afc | 49 | First I've heard of it! We do need more allies,\n |
| 0x191b2e | 48 | but I wish people would ask me first for these\n |
| 0x191b5f | 16 | big decisions... |
| 0x191b70 | 48 | I do apologize, but had we waited, we would be\n |
| 0x191ba1 | 47 | forced to leave our displaced comrades on the\n |
| 0x191bd1 | 8 | streets. |
| 0x191bda | 50 | The decision was mine alone. If you seek someone\n |
| 0x191c0d | 37 | to blame, I will gladly assume full\n |
| 0x191c33 | 15 | responsibility. |
| 0x191c43 | 47 | Ah, I can't blame him for wanting to keep his\n |
| 0x191c73 | 27 | crew from being homeless... |
| 0x191c8f | 49 | I'm not sure what you're all muttering about...\n |
| 0x191cc1 | 48 | but it is rare to see Ougi so close with others. |
| 0x191cf2 | 50 | Nosuri thinks aloud as she watches us whispering\n |
| 0x191d25 | 14 | to each other. |
| 0x191d38 | 18 | ...Er... Rulutieh? |
| 0x191d4b | 31 | We did bear a similar burden.\n |
| 0x191d6b | 38 | I believe we came to an understanding. |
| 0x191d92 | 28 | An understanding... right... |
| 0x191daf | 37 | Does he mean the Moznu incident...?\n |
| 0x191dd5 | 44 | I'm not sure there was ever a point I felt\n |
| 0x191e02 | 20 | CLOSE to this guy... |
| 0x191e17 | 49 | Well, I'm glad you're getting along. After all,\n |
| 0x191e49 | 37 | it seems we'll be here for some time. |
| 0x191e6f | 45 | ...You sure you're OK with that? What about\n |
| 0x191e9d | 47 | all that "resurrecting your noble house" stuff? |
| 0x191ecd | 48 | You could be more subtle about wanting them to\n |
| 0x191efe | 22 | leave! Have some tact. |
| 0x191f15 | 26 | No, think nothing of it.\n |
| 0x191f30 | 29 | Resurrecting our house, hm... |
| 0x191f4e | 50 | Nosuri stares off into the middle distance for a\n |
| 0x191f81 | 47 | moment... then gives a sad sigh, continuing on. |
| 0x191fb1 | 45 | These past few incidents have definitely...\n |
| 0x191fdf | 33 | put that future beyond our reach. |
| 0x192001 | 46 | Oh, that's... I'm sorry, I don't know what I\n |
| 0x192030 | 10 | can say... |
| 0x19203b | 45 | Nekone hesitates, troubled by Nosuri's glum\n |
| 0x192069 | 46 | outlook... but the bandit clenches her fist,\n |
| 0x192098 | 9 | resolute. |
| 0x1920a2 | 43 | But! That is no reason for us to lose hope! |
| 0x1920ce | 47 | I shall bide my time, and one day reclaim our\n |
| 0x1920fe | 48 | honor! Until then, I lay low here, and plan my\n |
| 0x19212f | 8 | triumph. |
| 0x192138 | 18 | Umm, I... I see... |
| 0x19214b | 45 | And this was a request from Oshtor himself!\n |
| 0x192179 | 50 | Who would be rude enough to decline such earnest\n |
| 0x1921ac | 6 | pleas? |
| 0x1921b3 | 47 | Nosuri can't hide her prideful grin with that\n |
| 0x1921e3 | 13 | proclamation. |
| 0x1921f1 | 44 | ...You sure we should leave her like that?\n |
| 0x19221e | 37 | Sounds like she's getting a big head. |
| 0x192244 | 47 | I will continue in my sole duty of supporting\n |
| 0x192274 | 15 | my dear sister. |
| 0x192284 | 44 | Couldn't you at least try to admonish her?\n |
| 0x1922b1 | 43 | This is why she's always messing things up. |
| 0x1922dd | 46 | I am sure Brother has carefully thought this\n |
| 0x19230c | 49 | through... Was there anything specific he asked\n |
| 0x19233e | 7 | of you? |
| 0x192346 | 48 | Well, he said all we needed to do was help you\n |
| 0x192377 | 46 | all out. And with me here, your troubles are\n |
| 0x1923a6 | 5 | over! |
| 0x1923ac | 35 | That's wonderful news! Right, Haku? |
| 0x1923d0 | 39 | ...In other words, more trouble for me. |
| 0x1923f8 | 45 | I can't help but sigh. But then it suddenly\n |
| 0x192426 | 8 | hits me. |
| 0x19242f | 49 | Wait a minute. Bandits or not, there's a ton of\n |
| 0x192461 | 47 | them. If all of them are staying for a while... |
| 0x192491 | 46 | That's a pretty sizable team working for me!\n |
| 0x1924c0 | 48 | I think we can forget about being short-staffed. |
| 0x1924f1 | 49 | Quality over quantity has been our plan so far,\n |
| 0x192523 | 47 | but it gets tough. And now I don't have to do\n |
| 0x192553 | 14 | night patrols! |
| 0x192562 | 49 | At the thought of my bright new future, I can't\n |
| 0x192594 | 48 | help but grin. Ougi turns, his own smile placid. |
| 0x1925c5 | 47 | I'm afraid the others won't be accompanying us. |
| 0x1925f5 | 7 | ...Huh? |
| 0x1925fd | 50 | What are you talking about? You had a whole crew\n |
| 0x192630 | 26 | of people working for you. |
| 0x19264b | 50 | Precisely. It would hardly be pragmatic to house\n |
| 0x19267e | 30 | that many fugitives in secret. |
| 0x19269d | 28 | I... guess you have a point. |
| 0x1926ba | 43 | Thus, using Oshtor's connections, we have\n |
| 0x1926e6 | 49 | secured them gainful employment in the villages\n |
| 0x192718 | 7 | nearby. |
| 0x192720 | 46 | Then that means... The only ones here at the\n |
| 0x19274f | 17 | Hakurokaku are... |
| 0x192761 | 19 | The two of us, yes. |
| 0x192775 | 51 | Urrgh... No, even two people is more than before!\n |
| 0x1927a9 | 44 | Getting out of crappy jobs should be a lot\n |
| 0x1927d6 | 7 | easier. |
| 0x1927de | 48 | All right then... I guess we'll have you start\n |
| 0x19280f | 24 | off with some paperwork. |
| 0x192828 | 47 | Might as well get rid of the most tedious job\n |
| 0x192858 | 14 | around here... |
| 0x192867 | 47 | No... I think that kind of job should be left\n |
| 0x192897 | 38 | to people who have actual skill in it. |
| 0x1928be | 5 | What? |
| 0x1928c4 | 44 | I'm afraid I don't have much of a head for\n |
| 0x1928f1 | 47 | writing and calculation. Things would... turn\n |
| 0x192921 | 11 | out poorly. |
| 0x19292d | 47 | Poorly, huh...? You know, you could show some\n |
| 0x19295d | 34 | effort before giving up like that. |
| 0x192980 | 46 | To clarify... whenever I try, this dizziness\n |
| 0x1929af | 39 | overwhelms me and I fall unconscious.\n |
| 0x1929d7 | 12 | It's futile! |
| 0x1929e4 | 48 | So in other words, you just fall asleep on the\n |
| 0x192a15 | 11 | job. Great. |
| 0x192a21 | 48 | Then what about patrol duty? That doesn't take\n |
| 0x192a52 | 16 | a lot of brains. |
| 0x192a63 | 49 | A capital idea! My first patrol route should be\n |
| 0x192a95 | 49 | around the gambling halls, as security is often\n |
| 0x192ac7 | 13 | poor around-- |
| 0x192ad5 | 50 | It would behoove us not to make undue appearance\n |
| 0x192b08 | 50 | in public. Oshtor still wishes for us to lay low\n |
| 0x192b3b | 12 | for a while. |
| 0x192b48 | 49 | Hmm... Is that so? Well, I suppose that's that,\n |
| 0x192b7a | 5 | then. |
| 0x192b80 | 51 | I must also ask that you refrain from patronizing\n |
| 0x192bb4 | 49 | gambling parlors. We could be recognized at any\n |
| 0x192be6 | 5 | time. |
| 0x192bec | 45 | H-Hold on, I don't think we need to go that\n |
| 0x192c1a | 7 | far...! |
| 0x192c22 | 19 | I'm afraid we must. |
| 0x192c36 | 48 | Nosuri droops her shoulders in disappointment.\n |
| 0x192c67 | 42 | I'm doing the same, for different reasons. |
| 0x192c92 | 50 | Oshtor has also enlisted my help in some matters\n |
| 0x192cc5 | 47 | of espionage, so I may not have time for much\n |
| 0x192cf5 | 5 | else. |
| 0x192cfb | 48 | No office work, and no patrol duty... What are\n |
| 0x192d2c | 30 | these two... even good for...? |
| 0x192d4b | 46 | Hm! I suppose all we can really help with is\n |
| 0x192d7a | 38 | arrests. Leave it all to us! Hahahaha! |
| 0x192da1 | 47 | Nosuri concludes with a proud laugh. A sudden\n |
| 0x192dd1 | 25 | dizziness washes over me. |
| 0x192deb | 47 | Keep it together, Haku. It's not like they'll\n |
| 0x192e1b | 47 | cut into our budget. Just pretend they're not\n |
| 0x192e4b | 12 | even here... |
| 0x192e58 | 47 | Oh, and I also heard you'll be paying for our\n |
| 0x192e88 | 43 | stay here. Your generosity does you credit! |
| 0x192eb4 | 9 | ...What!? |
| 0x192ebe | 42 | Yes, that was what we were told by Oshtor. |
| 0x192ee9 | 23 | ...Is this true, Kiwru? |
| 0x192f01 | 44 | I believe Brother's words were, "I am sure\n |
| 0x192f2e | 46 | Lord Haku will be able to manage without any\n |
| 0x192f5d | 10 | problems." |
| 0x192f68 | 48 | That ASSHOLE. He just didn't want to deal with\n |
| 0x192f99 | 20 | any of this himself. |
| 0x192fae | 49 | I don't even have the will to complain anymore.\n |
| 0x192fe0 | 49 | I'm not sure if Kuon can tell, but she speaks up. |
| 0x193012 | 45 | ...We may need to cut down on certain things. |
| 0x193040 | 46 | Wait, cut down? Cut down on what? Why is she\n |
| 0x19306f | 41 | sighing...? And why is she looking at ME? |
| 0x193099 | 48 | But to think the day would come that I stay in\n |
| 0x1930ca | 42 | the Hakurokaku as a proper guest... It's\n |
| 0x1930f5 | 11 | astounding. |
| 0x193101 | 32 | Did you have some memories here? |
| 0x193122 | 47 | It's a bit complicated... You just never know\n |
| 0x193152 | 36 | where fate will take you, I suppose. |
| 0x193177 | 37 | ...OK, back up. What do you mean by\n |
| 0x19319d | 15 | "proper guest"? |
| 0x1931ad | 43 | Hahaha... Then even you had no idea at all. |
| 0x1931d9 | 45 | We, the Nosuri bandits, have been using the\n |
| 0x193207 | 44 | Hakurokaku's basement storage as a hideout\n |
| 0x193234 | 9 | for eons! |
| 0x19323e | 34 | To clarify, she means just us two. |
| 0x193261 | 49 | Which would mean these two were angling to live\n |
| 0x193293 | 22 | here from the start... |
| 0x1932aa | 31 | ...U-Um, I've brought some tea. |
| 0x1932ca | 14 | ...Oh, thanks. |
| 0x1932d9 | 49 | Still stiff from the shock, I gratefully accept\n |
| 0x19330b | 43 | Rulutieh's tea. Some tea leaves are still\n |
| 0x193337 | 11 | floating... |
| 0x193343 | 48 | ...Hm. They say that means good fortune on the\n |
| 0x193374 | 10 | horizon... |
| 0x19337f | 44 | No, I'm sure. Something good's just around\n |
| 0x1933ac | 13 | the corner... |
| 0x1933ba | 7 | ...Tea. |
| 0x1933c2 | 33 | We have prepared you tea, Master. |
| 0x1933e4 | 35 | Uh... Huh? Well, I've already got-- |
| 0x193408 | 6 | Enjoy. |
| 0x19340f | 20 | Uh... Great. Thanks. |
| 0x193424 | 30 | Um, I also have some snacks.\n |
| 0x193443 | 31 | Today I prepared some torayaki. |
| 0x193463 | 32 | Oh, thanks! Mm, this looks good. |
| 0x193484 | 7 | Snacks. |
| 0x19348c | 44 | Please, have some snacks. We have prepared\n |
| 0x1934b9 | 15 | tamoyaki today. |
| 0x1934c9 | 36 | Uh, I'm not sure I can eat all thi-- |
| 0x1934ee | 8 | ...Mmph. |
| 0x1934f7 | 5 | Um... |
| 0x1934fd | 49 | Please don't tell me this is supposed to be the\n |
| 0x19352f | 15 | good fortune... |
| 0x19353f | 46 | As I mutter, I hear hurried footsteps coming\n |
| 0x19356e | 47 | closer, and the sliding door opens with a slam. |
| 0x19359e | 35 | Thank you all for the warm welcome! |
| 0x1935c2 | 10 | Excuse us. |
| 0x1935cd | 22 | Great. More trouble... |
| 0x1935e4 | 50 | Everyone's getting used to the princess's visits\n |
| 0x193617 | 43 | by now. But she has made an impact on one\n |
| 0x193643 | 9 | person... |
| 0x19364d | 17 | Y-Your Highness-- |
| 0x19365f | 46 | Nosuri had been reclining, but she bolts up,\n |
| 0x19368e | 43 | hurriedly trying to show deference to Anju. |
| 0x1936ba | 49 | Be at ease! No need for such formalities, Nosuri. |
| 0x1936ec | 6 | But... |
| 0x1936f3 | 50 | We are friends, are we not? And there is no need\n |
| 0x193726 | 33 | to act so humbly between friends. |
| 0x193748 | 44 | Your Highness... I-I am still your friend?\n |
| 0x193775 | 42 | I, whose house is disgraced, and who has\n |
| 0x1937a0 | 23 | disrespected you so...? |
| 0x1937b8 | 46 | It is I who have caused you so much trouble,\n |
| 0x1937e7 | 40 | Nosuri. I must ask for your forgiveness. |
| 0x193810 | 37 | I am not worthy of such kind words,\n |
| 0x193836 | 17 | Your Highness...! |
| 0x193848 | 44 | Nosuri seems deeply moved by Anju's words.\n |
| 0x193875 | 46 | I can see tears welling up in her eyes, too... |
| 0x1938a4 | 49 | Of course, from my perspective, the two of them\n |
| 0x1938d6 | 26 | are nothing but trouble... |
| 0x1938f1 | 45 | Sitting in the corner of the suddenly noisy\n |
| 0x19391f | 38 | room, I feel a sudden sinking feeling. |
| 0x193946 | 47 | Doesn't this just mean we have more good-for-\n |
| 0x193976 | 41 | nothings loafing around the place now...? |
| 0x1939a0 | 42 | ...Forget it. Not going to think about it. |
| 0x1939cb | 50 | I avert my eyes from the chaotic future ahead of\n |
| 0x1939fe | 48 | me, and focus on enjoying my tea while I still\n |
| 0x193a2f | 4 | can. |
| 0x194ac7 | 14 | Nn... urrgh... |
| 0x194ad6 | 9 | So hot... |
| 0x194ae0 | 50 | ...Looks like... the middle of the night, still.\n |
| 0x194b13 | 23 | The heat's woken me up. |
| 0x194b2b | 50 | Why's it so hot...? I'm sweating and everything.\n |
| 0x194b5e | 18 | Ugh, all clammy... |
| 0x194b71 | 50 | It's nice to have the bed warm, but when it gets\n |
| 0x194ba4 | 12 | this hot--\n |
| 0x194bb1 | 4 | Huh? |
| 0x194bb6 | 8 | *Squish* |
| 0x194bbf | 49 | Something much heavier, warmer, and softer than\n |
| 0x194bf1 | 33 | a blanket is clinging to my body. |
| 0x194c13 | 45 | I reach out uncertainly to feel what it is,\n |
| 0x194c41 | 35 | and feel something soft and smooth. |
| 0x194c65 | 14 | Nn...? Wha...? |
| 0x194c74 | 50 | The grogginess gradually fades as I realize this\n |
| 0x194ca7 | 46 | clearly isn't a blanket. I look over to find-- |
| 0x194cda | 37 | Whoa--!? The hell are you two doing!? |
| 0x194d00 | 46 | The twins must have snuck under my blankets.\n |
| 0x194d2f | 36 | They're lying there, clinging to me. |
| 0x194d54 | 24 | Accompanying you in bed. |
| 0x194d6d | 47 | We were worried that you may be cold, Master.\n |
| 0x194d9d | 41 | We have decided to keep you warm like so. |
| 0x194dc7 | 22 | C-Completely naked...? |
| 0x194dde | 47 | These two do all they can to take care of me.\n |
| 0x194e0e | 47 | Wakeup calls, dinner, cleaning my room, doing\n |
| 0x194e3e | 10 | laundry... |
| 0x194e49 | 50 | But they also waltz in with those skimpy outfits\n |
| 0x194e7c | 39 | to wash me in the bath, and now this.\n |
| 0x194ea4 | 13 | Naked in bed. |
| 0x194eb2 | 46 | It keeps escalating, and for some reason I'M\n |
| 0x194ee1 | 47 | always the bad guy, though I feel more like a\n |
| 0x194f11 | 7 | victim. |
| 0x194f19 | 22 | We will keep you warm. |
| 0x194f30 | 50 | Master, if you are feeling cold, you may embrace\n |
| 0x194f63 | 10 | us closer. |
| 0x194f6e | 44 | Urgh... This is bad. If anyone saw me like\n |
| 0x194f9b | 7 | this... |
| 0x194fa3 | 50 | My life is none of their business, but when they\n |
| 0x194fd6 | 45 | look at me with that disgust in their eyes.\n |
| 0x195004 | 7 | It's... |
| 0x19500c | 23 | It cuts deep, you know. |
| 0x195024 | 7 | Master. |
| 0x19502c | 35 | Are we being of use to you, Master? |
| 0x195050 | 22 | Er, y-yeah... I guess. |
| 0x195067 | 19 | All for our Master. |
| 0x19507b | 44 | We shall do all we can to serve you, Master. |
| 0x1950a8 | 37 | Well, don't push yourself too hard.\n |
| 0x1950ce | 46 | It'll all be moot if you overwork yourselves\n |
| 0x1950fd | 13 | and collapse. |
| 0x19510b | 12 | So touching. |
| 0x195118 | 44 | Your caring words bring us unimaginable joy. |
| 0x195145 | 41 | *Sigh* What the hell am I supposed to do? |
| 0x19516f | 50 | I wish they'd stop this excessive servitude, but\n |
| 0x1951a2 | 44 | if I word it wrong, they'll feel rejected.\n |
| 0x1951cf | 18 | And that'd be bad. |
| 0x1951e2 | 31 | It'd end up just like before... |
| 0x195202 | 46 | Hello, Sir Haku... Allow me to pour you some\n |
| 0x195231 | 6 | tea... |
| 0x195238 | 11 | Oh, thanks. |
| 0x195244 | 4 | Tea. |
| 0x195249 | 47 | We have also prepared some pickles for you as\n |
| 0x195279 | 45 | refreshment. Please enjoy it with your tea,\n |
| 0x1952a7 | 19 | Uh, yeah... Thanks. |
| 0x1952bb | 43 | Nekone and Rulutieh's stares really sting\n |
| 0x1952e7 | 12 | right now... |
| 0x1952f4 | 48 | Nekone's looking at me like I'm someone else's\n |
| 0x195325 | 8 | garbage. |
| 0x19532e | 45 | And Rulutieh looks a little down about them\n |
| 0x19535c | 41 | taking over her job... Or is she pouting? |
| 0x195386 | 53 | That stare she's giving me looks almost soulless...\n |
| 0x1953bc | 46 | Nah, what am I saying. Must be my imagination. |
| 0x1953eb | 10 | A massage. |
| 0x1953f6 | 36 | It seems your shoulders are stiff.\n |
| 0x19541b | 46 | If there is any place that is bothering you,\n |
| 0x19544a | 19 | please let us know. |
| 0x19545e | 11 | *Rub* *rub* |
| 0x19546a | 43 | Uh... A little close, aren't you? There's\n |
| 0x195496 | 38 | something soft on the back of my head. |
| 0x1954bd | 15 | Fringe benefit. |
| 0x1954cd | 46 | We have heard that men prefer their massages\n |
| 0x1954fc | 9 | this way. |
| 0x195506 | 28 | Of COURSE it was on purpose! |
| 0x195523 | 47 | I guess I just need to clear this up once and\n |
| 0x195553 | 8 | for all. |
| 0x19555c | 45 | Look, I really do appreciate the two of you\n |
| 0x19558a | 49 | taking care of me, but you really don't have to-- |
| 0x1955bc | 51 | But before I could finish my sentence, the twins'\n |
| 0x1955f0 | 22 | faces suddenly harden. |
| 0x195607 | 17 | Are we of no use? |
| 0x195619 | 37 | Have we been a burden to you, Master? |
| 0x19563f | 48 | No, no, you guys aren't a burden... I'm saying\n |
| 0x195670 | 49 | instead of fussing over me, you can do what YOU\n |
| 0x1956a2 | 12 | really want. |
| 0x1956af | 9 | What we-- |
| 0x1956b9 | 12 | Really want? |
| 0x1956c6 | 48 | The two don't even hesitate for a second. They\n |
| 0x1956f7 | 48 | embrace me, my head caught between their chests. |
| 0x195728 | 20 | That is you, Master. |
| 0x19573d | 47 | All we wish to do is to be of service to you,\n |
| 0x19576d | 49 | W-Would you at least stop clinging on to me all\n |
| 0x19579f | 9 | the time? |
| 0x1957a9 | 20 | Does it trouble you? |
| 0x1957be | 31 | Are we a bother to you, Master? |
| 0x1957de | 48 | A bother...? No, not really, but don't you two\n |
| 0x19580f | 43 | think you're going a little overboard here? |
| 0x19583b | 50 | Suddenly, with no hesitation, the two draw their\n |
| 0x19586e | 40 | self-defense daggers from their sheaths. |
| 0x195897 | 7 | ...Huh? |
| 0x19589f | 36 | We must be together with our Master. |
| 0x1958c4 | 45 | That is the purpose of our existence. If we\n |
| 0x1958f2 | 47 | cannot fulfill our purpose, we are unnecessary. |
| 0x195922 | 47 | Having said this, the two of them immediately\n |
| 0x195952 | 34 | lift the daggers to their throats. |
| 0x195975 | 26 | Wha--!? Hey, dammit, stop! |
| 0x195990 | 22 | That's enough of that. |
| 0x1959a7 | 5 | Ah... |
| 0x1959ad | 43 | I'm not sure when Kuon arrived, but she's\n |
| 0x1959d9 | 44 | suddenly there, two fingers pinched around\n |
| 0x195a06 | 11 | each blade. |
| 0x195a12 | 47 | I'd prefer not to have any blood shed in this\n |
| 0x195a42 | 14 | room, I think. |
| 0x195a51 | 45 | Kuon smiles, as though gently admonishing a\n |
| 0x195a7f | 6 | child. |
| 0x195a86 | 46 | And Haku doesn't want the two of you to die,\n |
| 0x195ab5 | 6 | right? |
| 0x195abc | 10 | R-Right... |
| 0x195ac7 | 37 | Wh-What is wrong with these two...?\n |
| 0x195aed | 48 | If Kuon didn't stop them just now, they'd have\n |
| 0x195b1e | 20 | killed themselves... |
| 0x195b33 | 36 | Not even a moment of hesitation...\n |
| 0x195b58 | 20 | These two are crazy! |
| 0x195b6d | 49 | After that, we somehow managed to convince them\n |
| 0x195b9f | 49 | that I didn't want them to die, and now here we\n |
| 0x195bd1 | 4 | are. |
| 0x195bd6 | 47 | This loyalty... it's total selfless devotion.\n |
| 0x195c06 | 47 | It's way too heavy for me... What the hell do\n |
| 0x195c36 | 5 | I do? |
| 0x195c3c | 48 | I can't just refuse them, but if I let them do\n |
| 0x195c6d | 46 | whatever, my image as a gentleman goes up in\n |
| 0x195c9c | 6 | smoke. |
| 0x195ca3 | 47 | As I'm contemplating this, the two push their\n |
| 0x195cd3 | 45 | breasts against my arms and wrap their legs\n |
| 0x195d01 | 12 | around mine. |
| 0x195d0e | 8 | So warm. |
| 0x195d17 | 35 | You have such inner warmth, Master. |
| 0x195d3b | 37 | It's warm because you're in my bed!\n |
| 0x195d61 | 45 | You don't have to say it all weird like that! |
| 0x195d8f | 39 | Dammit, how did it end up like this...? |
| 0x197336 | 17 | *Tug* *rustle*... |
| 0x197348 | 6 | Hm...? |
| 0x19734f | 15 | Please wake up. |
| 0x19735f | 47 | We are sorry for having disturbed you at this\n |
| 0x19738f | 13 | hour, Master. |
| 0x19739d | 49 | Late at night, I feel someone shaking me awake.\n |
| 0x1973cf | 48 | My head's still pretty muddled as I'm waking up. |
| 0x197400 | 7 | Master. |
| 0x197408 | 51 | So sleepy... What time is it? What's so important\n |
| 0x19743c | 29 | that I've gotta be up now...? |
| 0x19745a | 49 | I push through the sleepy haze, and open my eyes. |
| 0x19748c | 8 | ...Mm... |
| 0x197495 | 4 | Gah! |
| 0x19749a | 47 | I dodge as best I can, seeing the twins' lips\n |
| 0x1974ca | 24 | heading straight for me. |
| 0x1974e3 | 5 | Oh... |
| 0x1974e9 | 45 | Wh-What the hell are you two trying to pull!? |
| 0x197517 | 22 | A kiss to wake you up? |
| 0x19752e | 37 | We were trying to awaken you, Master. |
| 0x197554 | 47 | Couldn't you have tried something normal first? |
| 0x197584 | 48 | God. Can't let my guard down for a damn SECOND\n |
| 0x1975b5 | 17 | around these two. |
| 0x1975c7 | 46 | I've gotten used to them sleeping in my bed,\n |
| 0x1975f6 | 37 | but the nakedness thing, not so much. |
| 0x19761c | 49 | The last thing I want is to do something stupid\n |
| 0x19764e | 30 | while I'm still half-asleep... |
| 0x19766d | 38 | So why are you waking me up this late? |
| 0x197694 | 26 | Master Mito calls for you. |
| 0x1976af | 44 | He has invited you once again to his domain. |
| 0x1976dc | 32 | Master Mito... Oh, that old guy? |
| 0x1976fd | 8 | ...*Nod* |
| 0x197706 | 49 | Always has to do it in the middle of the night.\n |
| 0x197738 | 33 | It was the same last time, too... |
| 0x19775a | 31 | Master Mito is a very busy man. |
| 0x19777a | 46 | It is only in such hours that he is available. |
| 0x1977a9 | 46 | How can a retired crepe merchant be that busy? |
| 0x1977d8 | 50 | Well, whatever. The old coot's clearly got a lot\n |
| 0x19780b | 18 | of secrets anyway. |
| 0x19781e | 47 | And as for his identity... well, I think I've\n |
| 0x19784e | 24 | got a pretty good guess. |
| 0x197867 | 47 | It's probably best I don't pry even if I know\n |
| 0x197897 | 26 | what's going on, right...? |
| 0x1978b2 | 33 | I mean, I do like talking to him. |
| 0x1978d4 | 45 | And that mysterious woman with him... Honoka. |
| 0x197902 | 32 | All right. Let me get changed.\n |
| 0x197923 | 20 | Wait here for a sec. |
| 0x197938 | 28 | We have already prepared it. |
| 0x197955 | 31 | Here is your change of clothes. |
| 0x197975 | 11 | Oh, thanks. |
| 0x197981 | 13 | We will help. |
| 0x19798f | 24 | Allow us to undress you. |
| 0x1979a8 | 38 | Wha--? I can change clothes by myself! |
| 0x1979d3 | 49 | And you can quit that slinking closer! I see you! |
| 0x197a05 | 24 | Not... a damn... second. |
| 0x197a1e | 49 | I head into the moonlit street, led by the twins. |
| 0x197a50 | 49 | Just like the night before, a mist rises around\n |
| 0x197a82 | 46 | us, and I lose track of what direction we're\n |
| 0x197ab1 | 6 | going. |
| 0x197ab8 | 48 | After a long walk through the mist, Uruuru and\n |
| 0x197ae9 | 33 | Saraana stop before a large door. |
| 0x197b0b | 21 | Well met, dear guest. |
| 0x197b21 | 47 | I pass through to find him... Mito... sitting\n |
| 0x197b51 | 36 | there, smiling as he welcomes me in. |
| 0x197b76 | 48 | I apologize for having called upon you at such\n |
| 0x197ba7 | 38 | an hour. It must have been quite the\n |
| 0x197bce | 14 | inconvenience. |
| 0x197bdd | 42 | Honoka stands there next to him, smiling\n |
| 0x197c08 | 21 | apologetically at me. |
| 0x197c1e | 42 | Well, it's not like... Anyway, was there\n |
| 0x197c49 | 29 | something you wanted from me? |
| 0x197c67 | 50 | ...I can't do it. I was all set to snark at them\n |
| 0x197c9a | 49 | for waking me up, but not after an apology like\n |
| 0x197ccc | 5 | that. |
| 0x197cd2 | 50 | Hm. I've no business with you in particular, but\n |
| 0x197d05 | 50 | I have recently acquired some fine drink and food. |
| 0x197d38 | 48 | So I thought I would invite you to join me, as\n |
| 0x197d69 | 21 | thanks for last time. |
| 0x197d7f | 50 | With that, the twins reemerge with a large tray,\n |
| 0x197db2 | 42 | and begin lining the table with gorgeous\n |
| 0x197ddd | 11 | delicacies. |
| 0x197de9 | 20 | Please, have a seat. |
| 0x197dfe | 9 | S-Sure... |
| 0x197e08 | 50 | I take the offered seat, and sit across from the\n |
| 0x197e3b | 8 | old man. |
| 0x197e44 | 46 | Please, no need to be modest. We have enough\n |
| 0x197e73 | 38 | drink to quench the thirst of any man. |
| 0x197e9a | 6 | Enjoy. |
| 0x197ea1 | 45 | Help yourself to whatever you desire, Master. |
| 0x197ecf | 45 | When those two say it, it sounds a lot more\n |
| 0x197efd | 24 | sultry than it should... |
| 0x197f16 | 42 | Ah, whatever. Might as well accept their\n |
| 0x197f41 | 23 | hospitality and dig in. |
| 0x197f59 | 47 | ...Probably shouldn't think about it too much\n |
| 0x197f89 | 35 | if they're offering me free drinks. |
| 0x197fad | 35 | The old man's banquet didn't just\n |
| 0x197fd1 | 14 | look gorgeous. |
| 0x197fe0 | 50 | It felt like... They had chosen only the best of\n |
| 0x198013 | 38 | the best, and served that exclusively. |
| 0x19803a | 42 | I see. What extraordinary circumstances... |
| 0x198065 | 49 | The old man listens contentedly as I chat about\n |
| 0x198097 | 47 | mundane things that happened since we last met. |
| 0x1980c7 | 46 | That must have been quite an ordeal for you... |
| 0x1980f6 | 40 | Honoka also chimes in from time to time. |
| 0x19811f | 48 | It's not really as bad as it sounds, but yeah.\n |
| 0x198150 | 25 | Things were pretty rough. |
| 0x19816a | 51 | I drink a little more than usual, since the twins\n |
| 0x19819e | 46 | are refilling my cup whenever it gets too low. |
| 0x1981cd | 43 | As I talk on and on, I can feel the drink\n |
| 0x1981f9 | 26 | starting to go to my head. |
| 0x198214 | 6 | Water. |
| 0x19821b | 26 | Something to sober you up. |
| 0x198236 | 46 | Crap. Got a little too carried away with the\n |
| 0x198265 | 36 | open bar. Might've drank too much... |
| 0x19828a | 47 | The old man smiles, satisfied, and drinks the\n |
| 0x1982ba | 37 | hot tea that Honoka's poured for him. |
| 0x1982e0 | 44 | ...I am glad to see those two being of use\n |
| 0x19830d | 7 | to you. |
| 0x198315 | 50 | Uh... Yeah. They help me a lot by taking care of\n |
| 0x198348 | 19 | the everyday stuff. |
| 0x19835c | 46 | ...Seems like they've got some screws loose,\n |
| 0x19838b | 39 | of course, but they are pretty helpful. |
| 0x1983b3 | 47 | Hm. That is good to hear. Then I was right in\n |
| 0x1983e3 | 22 | assigning them to you. |
| 0x1983fa | 6 | ...Mm? |
| 0x198401 | 31 | ...Glad that they are of use?\n |
| 0x198421 | 21 | Assigning them to me? |
| 0x198437 | 50 | ...Well, they do follow my every order, but it's\n |
| 0x19846a | 46 | pretty clear they obey the old man, at least\n |
| 0x198499 | 8 | for now. |
| 0x1984a2 | 48 | Guess he's not trying to hide his identity any\n |
| 0x1984d3 | 5 | more. |
| 0x1984d9 | 45 | And that means I've been roped up into this\n |
| 0x198507 | 30 | old man's little secret now... |
| 0x198526 | 45 | I look into the old man's knowing expression. |
| 0x198554 | 49 | I think I may have said some things I shouldn't\n |
| 0x198586 | 5 | have. |
| 0x19858c | 24 | Is something the matter? |
| 0x1985a5 | 18 | ...No. Not really. |
| 0x1985b8 | 50 | Better that I just keep things the way they are,\n |
| 0x1985eb | 34 | and pretend I'm still in the dark. |
| 0x19860e | 7 | Hmhm... |
| 0x198616 | 11 | Ho ho ho... |
| 0x198622 | 51 | With a cheerful expression, the old man continues\n |
| 0x198656 | 12 | watching me. |
| 0x198663 | 30 | Incidentally, my dear guest... |
| 0x198682 | 10 | Oh... Yes? |
| 0x19868d | 35 | Have you partaken of those two yet? |
| 0x1986b1 | 50 | The old man's gaze drifts to the twins, standing\n |
| 0x1986e4 | 21 | on either side of me. |
| 0x1986fa | 7 | ...Huh? |
| 0x198702 | 45 | I merely ask whether you have enjoyed their\n |
| 0x198730 | 31 | company to its full extent yet. |
| 0x198750 | 8 | ...uh... |
| 0x198759 | 45 | It takes a second for his meaning to sink in. |
| 0x198787 | 8 | *Splash* |
| 0x198790 | 15 | Whoa--gah, hot! |
| 0x1987a0 | 28 | Oh dear... Allow me to help. |
| 0x1987bd | 46 | I accidentally knock over my tea, and Honoka\n |
| 0x1987ec | 34 | walks over to dab at the spillage. |
| 0x19880f | 21 | Uh, sorry about that. |
| 0x198825 | 49 | I take it, then, you have not lain with them yet? |
| 0x198857 | 23 | Wh..."Lain?" Seriously? |
| 0x19886f | 46 | Lord Haku... Are you dissatisfied with these\n |
| 0x19889e | 6 | girls? |
| 0x1988a5 | 44 | No, that's not what--Hang on, what are you\n |
| 0x1988d2 | 8 | saying!? |
| 0x1988db | 49 | Look, I know I accepted them, but I don't think\n |
| 0x19890d | 50 | that gives me the right to... DO... stuff to them. |
| 0x198940 | 50 | I mean, you have to respect their feelings, and... |
| 0x198973 | 48 | Oh, come now. It is as clear as day what these\n |
| 0x1989a4 | 18 | two want from you. |
| 0x1989b7 | 13 | Always ready. |
| 0x1989c5 | 46 | We are ready to accept any request, anytime,\n |
| 0x1989f4 | 9 | anywhere. |
| 0x1989fe | 7 | Urgh... |
| 0x198a06 | 20 | Right... I forgot... |
| 0x198a1b | 47 | It is no exaggeration to say that these girls\n |
| 0x198a4b | 50 | were born for you. It would not do to treat them\n |
| 0x198a7e | 7 | coldly. |
| 0x198a86 | 28 | What do you mean by that...? |
| 0x198aa3 | 12 | So lonely... |
| 0x198ab0 | 46 | If you ignore us so, Master... death may come. |
| 0x198adf | 18 | W-Wait, really...? |
| 0x198af2 | 8 | For you. |
| 0x198afb | 8 | Why me!? |
| 0x198b04 | 43 | Ho ho ho... your company is always such a\n |
| 0x198b30 | 8 | delight. |
| 0x198b39 | 33 | Look, this is no laughing matter! |
| 0x198b5b | 50 | He said something kind of worrying back there...\n |
| 0x198b8e | 42 | Eh, whatever. It's probably not important. |
| 0x198bb9 | 45 | It doesn't matter who this old man really is. |
| 0x198be7 | 46 | What's important is that here and now, we're\n |
| 0x198c16 | 37 | having a good time drinking together. |
| 0x198c3c | 38 | I'm sure that's what they want, too... |
| 0x199b70 | 50 | After finishing my work, I'm relaxing in my room\n |
| 0x199ba3 | 33 | when Kuon drops by with some tea. |
| 0x199bc5 | 49 | A job well done. Here, I put some honey in this\n |
| 0x199bf7 | 38 | one. I think it should help you relax. |
| 0x199c1e | 29 | Oh, thanks. Tch... ugh... ow. |
| 0x199c3c | 31 | Hm...? Is something the matter? |
| 0x199c5c | 49 | Well... I thought I was getting used to all the\n |
| 0x199c8e | 29 | physical activity these days. |
| 0x199cac | 48 | I'm definitely stronger than I was before, and\n |
| 0x199cdd | 47 | I can even carry some of the heavier loads now. |
| 0x199d0d | 47 | But... when I rest like this for a bit, I get\n |
| 0x199d3d | 48 | this tiredness and soreness that sets in slowly. |
| 0x199d6e | 40 | Argh... I think I got a cramp in my leg. |
| 0x199d97 | 44 | I'm not surprised. Today's work was pretty\n |
| 0x199dc4 | 19 | strenuous, I guess. |
| 0x199dd8 | 30 | Want me to give you a massage? |
| 0x199df7 | 42 | Huh? Oh, don't bother. I can do it myself. |
| 0x199e22 | 47 | I try kneading my leg a little, to loosen up.\n |
| 0x199e52 | 48 | The muscles feel tight, and it tingles where I\n |
| 0x199e83 | 8 | massage. |
| 0x199e8c | 3 | Ow. |
| 0x199e90 | 52 | Doing it yourself isn't going to do much, I think.\n |
| 0x199ec5 | 40 | You tend to hold back your own strength. |
| 0x199eee | 30 | You... think so? Eegh... ow... |
| 0x199f0d | 50 | Well, most people prefer to avoid damaging their\n |
| 0x199f40 | 9 | own body. |
| 0x199f4a | 26 | I... can sympathize there. |
| 0x199f65 | 50 | Here, just leave it to me. I actually know quite\n |
| 0x199f98 | 41 | a bit about pressure points and all that. |
| 0x199fc2 | 44 | Even so... Kuon has a lot of brute strength. |
| 0x199fef | 49 | Even if she holds back, I don't see this ending\n |
| 0x19a021 | 28 | in anything other than pain. |
| 0x19a03e | 28 | Come on, don't be so modest! |
| 0x19a05b | 9 | Wha--Hey! |
| 0x19a065 | 6 | *Thud* |
| 0x19a06c | 49 | Before I know it, I've been knocked flat on the\n |
| 0x19a09e | 7 | ground. |
| 0x19a0a6 | 46 | Kuon is sitting right on top of me and has a\n |
| 0x19a0d5 | 37 | tight hold on my limbs. I can't move. |
| 0x19a0fb | 19 | Now, let's begin... |
| 0x19a10f | 49 | Kuon's cold hands take a firm grasp of my legs,\n |
| 0x19a141 | 44 | and her fingers press in on a specific spot. |
| 0x19a16e | 13 | Hey, wait a-- |
| 0x19a17c | 4 | Hup. |
| 0x19a181 | 8 | *CRUNCH* |
| 0x19a18a | 21 | Owowowowowowowowow!!! |
| 0x19a1a0 | 11 | Hm... phew. |
| 0x19a1ac | 12 | *C-C-Crunch* |
| 0x19a1b9 | 32 | Oh god oh god oh god oh GOD OH\n |
| 0x19a1da | 8 | GOD OH-- |
| 0x19a1e3 | 48 | Oh, Haku, there's no need to be so melodramatic. |
| 0x19a214 | 34 | I'm not exaggerating a thing...!\n |
| 0x19a237 | 11 | That HURTS! |
| 0x19a243 | 45 | Just like I expected... Dammit, I can't see\n |
| 0x19a271 | 35 | through all the tears in my eyes... |
| 0x19a295 | 51 | O-Oh, sorry! I didn't expect it would hurt enough\n |
| 0x19a2c9 | 18 | to make you cry... |
| 0x19a2dc | 47 | Look, uh... I appreciate the sentiment... but\n |
| 0x19a30c | 31 | could you hold back a bit more? |
| 0x19a32c | 26 | OK, I got it... Hm, hmf... |
| 0x19a347 | 7 | *Grind* |
| 0x19a34f | 36 | Dammit DAMN damn dammit damn DAMMIT! |
| 0x19a374 | 20 | Huh? It still hurts? |
| 0x19a389 | 13 | Urgh... Yeah! |
| 0x19a397 | 43 | I roll feebly around in pain for a while.\n |
| 0x19a3c3 | 22 | Yep, definitely hurts. |
| 0x19a3da | 48 | That's strange. Everyone tells me I give great\n |
| 0x19a40b | 47 | massages. Rulutieh said it felt like a dream... |
| 0x19a43b | 48 | That just proves you're all completely abnormal! |
| 0x19a46c | 47 | Maybe I should try a different technique, then. |
| 0x19a49c | 47 | Actually, you know what, maybe we should stop-- |
| 0x19a4cc | 7 | Hmmm... |
| 0x19a4d4 | 26 | *Tickle* *tickle* *tickle* |
| 0x19a4ef | 17 | Bwahahahahahahah! |
| 0x19a501 | 8 | H-Haku!? |
| 0x19a50a | 47 | Her next strategy is to softly touch my feet,\n |
| 0x19a53a | 31 | which ends up just tickling me. |
| 0x19a55a | 51 | Ha... phew... You're not taking this seriously...\n |
| 0x19a58e | 8 | are you? |
| 0x19a597 | 49 | I should think I am! I'm very serious about this. |
| 0x19a5c9 | 41 | You're being too extreme when you adjust. |
| 0x19a5f3 | 49 | Oh, honestly... You're just difficult to adjust\n |
| 0x19a625 | 3 | to. |
| 0x19a629 | 45 | You have no idea what adjusting even means!\n |
| 0x19a657 | 38 | Here, I'll show you. Give me your leg. |
| 0x19a67e | 40 | H-Huh? I-I don't think I need a massage. |
| 0x19a6a7 | 46 | Just give me your foot. I can't let you keep\n |
| 0x19a6d6 | 21 | doing all THAT to me. |
| 0x19a6ec | 41 | So you'll let me massage you again, then? |
| 0x19a716 | 31 | Y-Yeah, if I ever feel like it. |
| 0x19a736 | 48 | Here, I'll show you what the perfect amount of\n |
| 0x19a767 | 34 | strength is. Let me see your foot. |
| 0x19a78a | 51 | So you're saying I should experience it first...?\n |
| 0x19a7be | 21 | Well, in that case... |
| 0x19a7d4 | 47 | Kuon puts her foot forward, very reluctantly.\n |
| 0x19a804 | 32 | I grasp it firmly and carefully. |
| 0x19a825 | 47 | I study the foot, trying to find the pressure\n |
| 0x19a855 | 32 | point, and place my thumb on it. |
| 0x19a876 | 5 | Hm... |
| 0x19a87c | 39 | Watch and learn. THIS is how you do it! |
| 0x19a8a4 | 7 | *Press* |
| 0x19a8ac | 4 | Wh-- |
| 0x19a8b1 | 50 | I put all my strength into my fingers as revenge\n |
| 0x19a8e4 | 28 | for what she put me through. |
| 0x19a901 | 46 | How's that!? This should give her a taste of\n |
| 0x19a930 | 45 | her own medicine. Hope she learns her lesson. |
| 0x19a95e | 46 | I'm sure if Kuon goes through the same pain,\n |
| 0x19a98d | 48 | she'll never inflict it on another person again. |
| 0x19a9be | 31 | Mwahahahaha! How's that, eh!?\n |
| 0x19a9de | 15 | You like that!? |
| 0x19a9ee | 21 | *Press* *rub* *press* |
| 0x19aa04 | 14 | Mmn... Ngh...! |
| 0x19aa13 | 15 | Hah! Yah! Hyah! |
| 0x19aa23 | 33 | *Rub* *press* *rub* *press* *rub* |
| 0x19aa45 | 10 | ...Nnngm!? |
| 0x19aa50 | 21 | Hah... phew... hah... |
| 0x19aa66 | 8 | ...Whew. |
| 0x19aa6f | 5 | Whew? |
| 0x19aa75 | 48 | I pressed with all my might, but Kuon... has a\n |
| 0x19aaa6 | 47 | dreamy expression on her face, and her cheeks\n |
| 0x19aad6 | 8 | are red. |
| 0x19aadf | 50 | You're... actually very good at giving massages,\n |
| 0x19ab12 | 32 | Haku... I wasn't expecting that. |
| 0x19ab33 | 4 | Huh? |
| 0x19ab38 | 45 | That felt really good... I feel so warm an'\n |
| 0x19ab66 | 10 | relaxed... |
| 0x19ab71 | 42 | Uh, hello? Kuon? You're... slurring your\n |
| 0x19ab9c | 29 | sentences a little, there...? |
| 0x19abba | 48 | Haku... I think I'd like you to do a bit more.\n |
| 0x19abeb | 46 | I might get a better sense of how strong you\n |
| 0x19ac1a | 10 | prefer it. |
| 0x19ac25 | 29 | Huh? Uh, w-well... I guess... |
| 0x19ac43 | 3 | Oh! |
| 0x19ac47 | 15 | *Press* *press* |
| 0x19ac57 | 8 | Oooh...! |
| 0x19ac60 | 45 | ...Hm. Sounds like she really is enjoying it. |
| 0x19ac8e | 30 | Seems like I've discovered a\n |
| 0x19acad | 14 | hidden talent. |
| 0x19acbc | 41 | Kuon seems off in her own little world,\n |
| 0x19ace6 | 42 | blissfully oblivious while I keep working. |
| 0x19ad11 | 49 | Her tail curls around her, and little sounds of\n |
| 0x19ad43 | 37 | delight and relief keep escaping her. |
| 0x19ad69 | 18 | Ah... phew, hah... |
| 0x19ad7c | 45 | Mmf... I could definitely get used to this... |
| 0x19adae | 49 | So at the end of the day, I got no actual rest,\n |
| 0x19ade0 | 49 | and was sentenced to hard labor until Kuon fell\n |
| 0x19ae12 | 7 | asleep. |
| 0x19ae1a | 31 | How did it end up like this...? |
| 0x19e41b | 27 | I thank you all for coming. |
| 0x19e437 | 45 | I came as soon as I heard there'd be lovely\n |
| 0x19e465 | 12 | free drinks! |
| 0x19e472 | 14 | M-Miss Atuy... |
| 0x19e481 | 48 | Rulutieh seems troubled by Atuy's blunt honesty. |
| 0x19e4b2 | 50 | Atuy's got the right idea. Nothing tastes better\n |
| 0x19e4e5 | 44 | than a meal that someone else is paying for. |
| 0x19e512 | 47 | Think nothing of it. I have prepared this for\n |
| 0x19e542 | 43 | you. Please, enjoy to your hearts' content. |
| 0x19e56e | 44 | Oshtor replies with nonchalant ease at the\n |
| 0x19e59b | 17 | group's reaction. |
| 0x19e5ad | 46 | Surely it is better that fine food and drink\n |
| 0x19e5dc | 44 | be enjoyed by those who truly appreciate it. |
| 0x19e609 | 33 | I could not agree more, Oshtor.\n |
| 0x19e62b | 11 | Hear! Hear! |
| 0x19e637 | 34 | Free drinks aside, why exactly...? |
| 0x19e65a | 43 | Is something amiss, Lord Haku? You appear\n |
| 0x19e686 | 49 | troubled... certainly unusual when moments from\n |
| 0x19e6b8 | 8 | a feast. |
| 0x19e6c1 | 48 | Hey, what do you take me for? I'm happy, don't\n |
| 0x19e6f2 | 42 | get me wrong, but I'm wondering what the\n |
| 0x19e71d | 12 | occasion is. |
| 0x19e72a | 52 | Oshtor looks a little taken aback by my statement,\n |
| 0x19e75f | 40 | and answers with all apparent sincerity. |
| 0x19e788 | 47 | Is it not enough to simply wish to deepen the\n |
| 0x19e7b8 | 25 | bonds among dear friends? |
| 0x19e7d2 | 48 | See, that sounds more like an Ukon reason than\n |
| 0x19e803 | 23 | an Oshtor reason to me. |
| 0x19e81b | 46 | At my words, a grin crosses the masked man's\n |
| 0x19e84a | 5 | face. |
| 0x19e850 | 48 | As sharp as ever, I see. You think and analyze\n |
| 0x19e881 | 37 | a great deal, despite how you appear. |
| 0x19e8a7 | 49 | You do know I can tell that's not a compliment,\n |
| 0x19e8d9 | 6 | right? |
| 0x19e8e0 | 49 | I had hoped to explain after the feast began...\n |
| 0x19e912 | 48 | but the truth is, I wished to introduce you to\n |
| 0x19e943 | 8 | someone. |
| 0x19e94c | 19 | Introduce... to me? |
| 0x19e960 | 46 | Yes. Judging by his reaction, he seemed very\n |
| 0x19e98f | 18 | interested in you. |
| 0x19e9a2 | 8 | Wh-What? |
| 0x19e9ab | 25 | I take a step back, wary. |
| 0x19e9c5 | 32 | This guy... is interested in me? |
| 0x19e9e6 | 30 | You need not worry, I am sure. |
| 0x19ea05 | 13 | I HOPE not... |
| 0x19ea13 | 41 | Hm... But I do understand his interest.\n |
| 0x19ea3d | 49 | You have a curious air about you that puts many\n |
| 0x19ea6f | 8 | at ease. |
| 0x19ea78 | 43 | That is why I have such high hopes for you. |
| 0x19eaa4 | 51 | I'm not sure how to take all this when it's a guy\n |
| 0x19ead8 | 12 | saying it... |
| 0x19eae5 | 47 | Heigh-ho, Master Haku! Long have I dream'd of\n |
| 0x19eb15 | 24 | such auspicious reunion! |
| 0x19eb2e | 29 | Maro? What're you doing here? |
| 0x19eb4c | 45 | Wait, don't tell me HE'S the guy Oshtor was-- |
| 0x19eb7a | 44 | 'Tis by honest Master Oshtor's invitation!\n |
| 0x19eba7 | 32 | Fain do I stay upon his leisure! |
| 0x19ebc8 | 39 | Well, if it's a gathering of Oshtor's\n |
| 0x19ebf0 | 46 | acquaintances, I suppose it makes sense that\n |
| 0x19ec1f | 14 | Maroro's here. |
| 0x19ec2e | 48 | While I'm thinking, Maroro swans over, eagerly\n |
| 0x19ec5f | 27 | taking a seat alongside me. |
| 0x19ec7b | 29 | ...Why are you sitting there? |
| 0x19ec99 | 47 | Why, that I may better ensure the fullness of\n |
| 0x19ecc9 | 16 | thy cup, master! |
| 0x19ecda | 31 | Why the hell is he blushing...? |
| 0x19ecfa | 43 | Shouldn't you be serving drinks to Oshtor\n |
| 0x19ed26 | 14 | instead of me? |
| 0x19ed35 | 51 | O, would that I could, master, but such obeisance\n |
| 0x19ed69 | 43 | would ill become my, ah, present offices... |
| 0x19ed95 | 48 | Present offices...? Oh, you mean cause you got\n |
| 0x19edc6 | 27 | hired by some noble bigwig? |
| 0x19ede2 | 50 | And since he's not too fond of Oshtor, you can't\n |
| 0x19ee15 | 31 | get too friendly with him, huh? |
| 0x19ee35 | 10 | Just so... |
| 0x19ee40 | 48 | I think he mentioned his situation before, but\n |
| 0x19ee71 | 42 | I guess he's got some complicated family\n |
| 0x19ee9c | 14 | relationships. |
| 0x19eeab | 45 | Now then, allow me to introduce my guest of\n |
| 0x19eed9 | 6 | honor. |
| 0x19eee0 | 51 | Oshtor returns to the dining hall, having greeted\n |
| 0x19ef14 | 10 | his guest. |
| 0x19ef1f | 49 | Behind Oshtor stands a man who seems... clearly\n |
| 0x19ef51 | 36 | out of place for an event like this. |
| 0x19ef76 | 49 | Ho ho ho... My, my, what a pretty little gaggle\n |
| 0x19efa8 | 11 | of girlies! |
| 0x19efb4 | 41 | The man looks around the room cheerfully. |
| 0x19efde | 13 | That guy's... |
| 0x19efec | 33 | Shiny bald head. Tiny mustache.\n |
| 0x19f00e | 27 | There's no mistaking him... |
| 0x19f02a | 16 | ...The candyman? |
| 0x19f03b | 48 | I remember seeing him from time to time in the\n |
| 0x19f06c | 20 | streets of the city. |
| 0x19f081 | 10 | H-Hello... |
| 0x19f08c | 46 | Hello, Mr. Sakon. It's a pleasure to see you\n |
| 0x19f0bb | 5 | here. |
| 0x19f0c1 | 24 | Ooh, it's old man Sakon! |
| 0x19f0da | 46 | I guess that marks the candyman as Sakon, huh. |
| 0x19f109 | 46 | The girls seem to know him by name, since he\n |
| 0x19f138 | 50 | always includes a little extra when they buy his\n |
| 0x19f16b | 8 | candies. |
| 0x19f174 | 41 | But it seems they didn't know he was an\n |
| 0x19f19e | 25 | acquaintance of Oshtor's. |
| 0x19f1b8 | 41 | So what is that old geezer doing HERE...? |
| 0x19f1e2 | 42 | Having apparently guessed what we're all\n |
| 0x19f20d | 29 | thinking, Oshtor turns to us. |
| 0x19f22b | 42 | This man is someone irreplaceable to me.\n |
| 0x19f256 | 44 | Without him, I could not have fulfilled my\n |
| 0x19f283 | 17 | responsibilities. |
| 0x19f295 | 17 | Responsibilities? |
| 0x19f2a7 | 32 | Indeed. Public... and otherwise. |
| 0x19f2c8 | 47 | Public AND otherwise? Wait, does that mean he\n |
| 0x19f2f8 | 42 | knows Oshtor and Ukon are the same person? |
| 0x19f323 | 51 | Sakon notices my baffled stare, and looks me over\n |
| 0x19f357 | 19 | with a broad smirk. |
| 0x19f36b | 10 | What the-- |
| 0x19f376 | 45 | He then struts over without hesitation, and\n |
| 0x19f3a4 | 38 | seats himself directly in front of me. |
| 0x19f3cb | 49 | I figure this would be the first time we've sat\n |
| 0x19f3fd | 29 | and drank together like this. |
| 0x19f41b | 28 | Why are you sitting here...? |
| 0x19f438 | 49 | What? You a moron, kid? I'm the guest of honor!\n |
| 0x19f46a | 34 | I sit wherever I damn well please. |
| 0x19f490 | 48 | Wait a minute... This old prune is the one who\n |
| 0x19f4c1 | 18 | wanted to meet me? |
| 0x19f4d4 | 45 | Why the hell does he want to talk to me...?\n |
| 0x19f502 | 48 | Well, whatever. I guess he's not doing any harm. |
| 0x19f533 | 48 | So what exactly did Oshtor mean, with all that\n |
| 0x19f564 | 29 | "public and otherwise" stuff? |
| 0x19f582 | 50 | Just as it sounds. I'm sure you already know all\n |
| 0x19f5b5 | 47 | about Ukon and such. But that's not important\n |
| 0x19f5e5 | 4 | now. |
| 0x19f5ea | 47 | I came here for a much bigger reason than that. |
| 0x19f61a | 16 | A bigger reason? |
| 0x19f62b | 49 | It's about you, Haku. You don't realize it, but\n |
| 0x19f65d | 47 | your worth is more than you could ever imagine. |
| 0x19f68d | 28 | OK? What exactly do you me-- |
| 0x19f6aa | 51 | You know exactly what I mean! Just call you over,\n |
| 0x19f6de | 39 | and a bevy of cute girlies soon follow! |
| 0x19f706 | 4 | Huh? |
| 0x19f70b | 41 | You're the biggest gigolo in this city!\n |
| 0x19f735 | 31 | Arrgh... I'm downright jealous! |
| 0x19f759 | 48 | What's the matter, boy? Why the stupid-looking\n |
| 0x19f78a | 5 | face? |
| 0x19f790 | 46 | You called us here just to tell me something\n |
| 0x19f7bf | 10 | like that? |
| 0x19f7ca | 49 | Idiot! You call an ability to summon a horde of\n |
| 0x19f7fc | 42 | cute little ladies "something like that"!? |
| 0x19f827 | 9 | No, but-- |
| 0x19f831 | 47 | Oh, quit your yammerin' and drink up, would ya? |
| 0x19f861 | 9 | Huh? Oh-- |
| 0x19f86b | 44 | Sakon holds out the bottle, and the sudden\n |
| 0x19f898 | 46 | pressure makes me reflexively hold out my cup. |
| 0x19f8c7 | 14 | A toast, then! |
| 0x19f8d6 | 50 | Sakon clinks his cup against mine with startling\n |
| 0x19f909 | 40 | force, then downs the booze in one gulp. |
| 0x19f932 | 36 | I follow suit, and drink up as well. |
| 0x19f957 | 40 | Pfaaaah...! Now that's the good stuff!\n |
| 0x19f980 | 14 | Another round! |
| 0x19f98f | 38 | What's the matter? Your cup's empty.\n |
| 0x19f9b6 | 38 | You tryin' to dry it out or something? |
| 0x19f9dd | 12 | Oh, right... |
| 0x19f9ea | 47 | I hold out my cup, and Sakon quietly pours me\n |
| 0x19fa1a | 5 | more. |
| 0x19fa20 | 7 | Master. |
| 0x19fa28 | 29 | We have brought refreshments. |
| 0x19fa46 | 35 | Well, hello there, little ladies.\n |
| 0x19fa6a | 32 | Mind lettin' me have a bit, too? |
| 0x19fa8b | 49 | The two of them look at me in unison, as though\n |
| 0x19fabd | 26 | waiting for my permission. |
| 0x19fad8 | 9 | Go ahead. |
| 0x19fae2 | 14 | Please, enjoy. |
| 0x19faf1 | 48 | They place down a plate of small simmered cuts\n |
| 0x19fb22 | 8 | of fish. |
| 0x19fb2b | 13 | Much obliged. |
| 0x19fb39 | 50 | After thanking them, Sakon reaches for the plate\n |
| 0x19fb6c | 42 | and pops one of the pieces into his mouth. |
| 0x19fb97 | 5 | Hm... |
| 0x19fb9d | 50 | He leans leisurely on the armrest, eyes drifting\n |
| 0x19fbd0 | 48 | to the girls enjoying themselves with song and\n |
| 0x19fc01 | 6 | dance. |
| 0x19fc08 | 47 | At first, I figure he's just ogling them, but\n |
| 0x19fc38 | 46 | his expression is fond and faraway... almost\n |
| 0x19fc67 | 5 | kind. |
| 0x19fc6d | 44 | What, you're not going to go talk to them?\n |
| 0x19fc9a | 42 | I thought you were here for the "girlies." |
| 0x19fcc5 | 35 | Eh, you're too young to get it...\n |
| 0x19fce9 | 50 | You can gaze at flowers, but never disturb them.\n |
| 0x19fd1c | 17 | It'd be improper. |
| 0x19fd2e | 49 | Remember, there are some flowers out there that\n |
| 0x19fd60 | 34 | will wither at but a single touch. |
| 0x19fd83 | 6 | I see. |
| 0x19fd8a | 51 | When he said he was here for the women, I thought\n |
| 0x19fdbe | 36 | he was just some greasy old pervert. |
| 0x19fde3 | 50 | But I guess he's got a little more class than he\n |
| 0x19fe16 | 9 | seems to. |
| 0x19fe20 | 49 | As I'm observing him, I notice his cup is empty\n |
| 0x19fe52 | 6 | again. |
| 0x19fe59 | 43 | He's weird, sure, but he's not a bad guy.\n |
| 0x19fe85 | 47 | Not to mention he's the one apparently paying\n |
| 0x19feb5 | 13 | for all this. |
| 0x19fec3 | 48 | I offer the bottle to Sakon. The reverie lifts\n |
| 0x19fef4 | 40 | as he notices me, and he takes it, but-- |
| 0x19ff1d | 26 | No, I know what I'll do... |
| 0x19ff3a | 14 | Little Nekone? |
| 0x19ff49 | 45 | At Sakon's beckoning, Nekone looks a little\n |
| 0x19ff77 | 11 | bewildered. |
| 0x19ff83 | 40 | Sakon raises his empty glass toward her. |
| 0x19ffac | 32 | Would you mind pouring me a cup? |
| 0x19ffcd | 26 | I... suppose I don't mind. |
| 0x19ffe8 | 47 | Nekone seems unsure as to why she was the one\n |
| 0x1a0018 | 44 | chosen, but she pours him some more of the\n |
| 0x1a0045 | 20 | spirits nonetheless. |
| 0x1a005a | 36 | Whoa whoa whoa... *gulp*... Pffah!\n |
| 0x1a007f | 44 | It tastes all the better when you pour it,\n |
| 0x1a00ac | 14 | little Nekone. |
| 0x1a00bb | 48 | What happened to all that flower talk a second\n |
| 0x1a00ec | 40 | ago? That doesn't sound like "gazing"... |
| 0x1a0115 | 47 | What, you've never heard of exceptions to the\n |
| 0x1a0145 | 10 | rule, kid? |
| 0x1a0150 | 19 | Are you serious...? |
| 0x1a0164 | 49 | It is fine, Haku. It seems my dear brother owes\n |
| 0x1a0196 | 51 | him a great deal. I can certainly pour his drinks\n |
| 0x1a01ca | 12 | if he likes. |
| 0x1a01d7 | 39 | Well, I guess if you're fine with it... |
| 0x1a01ff | 48 | Oshtor says he owes you a lot, but who exactly\n |
| 0x1a0230 | 8 | are you? |
| 0x1a0239 | 45 | If you know about Ukon's identity, I assume\n |
| 0x1a0267 | 38 | you're not just a candy vendor, right? |
| 0x1a028e | 36 | I look into Sakon's eyes as I speak. |
| 0x1a02b3 | 6 | Oho... |
| 0x1a02ba | 45 | Sakon smirks as he quietly sets down his cup. |
| 0x1a02e8 | 50 | That dark smile looks nothing like the airy grin\n |
| 0x1a031b | 25 | on his face a moment ago. |
| 0x1a0335 | 48 | So, you would know of my connection to Oshtor,\n |
| 0x1a0366 | 6 | hm...? |
| 0x1a036d | 31 | Sakon's voice suddenly changes. |
| 0x1a038d | 51 | What the--!? He feels like a completely different\n |
| 0x1a03c1 | 9 | person... |
| 0x1a03cb | 41 | The breezy, laid-back demeanor is gone.\n |
| 0x1a03f5 | 49 | Instead, his voice is icy, with a hint of menace. |
| 0x1a0427 | 34 | I suppose seeing is believing...\n |
| 0x1a044a | 42 | Maybe this will reveal the truth you seek. |
| 0x1a0475 | 49 | Muttering, Sakon wipes his face with a towel...\n |
| 0x1a04a7 | 34 | and the countless wrinkles vanish. |
| 0x1a04ca | 48 | He slowly sets his hand against the top of his\n |
| 0x1a04fb | 41 | head. He grasps his own bald scalp, and-- |
| 0x1a0525 | 6 | *Fwip* |
| 0x1a052c | 6 | *Fwap* |
| 0x1a0533 | 7 | ...Huh? |
| 0x1a053b | 14 | ...Understand? |
| 0x1a054a | 14 | U-Uhh... Um... |
| 0x1a0559 | 49 | The cheerful atmosphere has given way to uneasy\n |
| 0x1a058b | 8 | silence. |
| 0x1a0594 | 36 | J-Just now, was that...? Wait, no!\n |
| 0x1a05b9 | 41 | I-It could've just been my imagination... |
| 0x1a05e3 | 47 | Y-Yeah, that's it. Maybe I drank a little too\n |
| 0x1a0613 | 5 | much. |
| 0x1a0619 | 4 | Hmm? |
| 0x1a061e | 45 | At my apparent lack of reaction, Sakon once\n |
| 0x1a064c | 34 | again grimly reaches for his head. |
| 0x1a066f | 49 | No one says anything. Silence prevails, growing\n |
| 0x1a06a1 | 45 | heavier and heavier with each passing second. |
| 0x1a06cf | 9 | So be it. |
| 0x1a06d9 | 43 | *Fwip* *Fwap* *Fwip* *Fwap* *Fwip* *Fwap*\n |
| 0x1a0705 | 16 | I-It can't be... |
| 0x1a0716 | 14 | Heh heh heh... |
| 0x1a0725 | 20 | L-Lord Mikazuchi...? |
| 0x1a073a | 7 | Wha--!? |
| 0x1a0742 | 10 | Whaaat...? |
| 0x1a074d | 9 | *Gasp*... |
| 0x1a0757 | 21 | That's... Mikazuchi!? |
| 0x1a076d | 49 | Heh heh... Took you long enough. I was starting\n |
| 0x1a079f | 33 | to think you'd never work it out. |
| 0x1a07c1 | 48 | I'm frozen in shock, the Imperial Guard of the\n |
| 0x1a07f2 | 23 | Left sitting before me. |
| 0x1a080a | 11 | Ah... ah... |
| 0x1a0816 | 53 | Sakon... Or rather, Mikazuchi looks towards Nekone,\n |
| 0x1a084c | 42 | a deathly smirk spreading across his face. |
| 0x1a0877 | 4 | Eep! |
| 0x1a087c | 45 | After Mikazuchi... seemingly glares at her,\n |
| 0x1a08aa | 38 | Nekone bolts up and darts behind me.\n |
| 0x1a08d1 | 18 | Business as usual. |
| 0x1a08e4 | 33 | Is that... really you, Mikazuchi? |
| 0x1a0906 | 49 | Do you see someone else? Perhaps if I plunge my\n |
| 0x1a0938 | 48 | thumbs into your eyes, your vision may clear up. |
| 0x1a0969 | 30 | Uh... That's a joke, right...? |
| 0x1a0988 | 51 | It might seem simple, but his whole personality's\n |
| 0x1a09bc | 19 | completely changed. |
| 0x1a09d0 | 44 | I guess I see it now, but how could I have\n |
| 0x1a09fd | 45 | known without the mask? He didn't have that\n |
| 0x1a0a2b | 20 | murder-stare before! |
| 0x1a0a40 | 24 | So what is this all for? |
| 0x1a0a59 | 48 | Mikazuchi responds with that familiar sinister\n |
| 0x1a0a8a | 5 | grin. |
| 0x1a0a90 | 51 | Do you truly believe that all it takes to protect\n |
| 0x1a0ac4 | 42 | the people is mindlessly swinging a blade? |
| 0x1a0aef | 48 | I use this persona to watch over the people of\n |
| 0x1a0b20 | 10 | this city. |
| 0x1a0b2b | 50 | It also helps me rid the imperial capital of the\n |
| 0x1a0b5e | 35 | maggots that try to nest within it. |
| 0x1a0b82 | 48 | Am I hearing this right? You disguise yourself\n |
| 0x1a0bb3 | 29 | as a candyman to fight crime? |
| 0x1a0bd1 | 45 | OK, I understand you need a disguise, but a\n |
| 0x1a0bff | 16 | candy vendor...? |
| 0x1a0c10 | 47 | Heh heh... A simple candy vendor can hear all\n |
| 0x1a0c40 | 32 | kinds of rumors from the people. |
| 0x1a0c61 | 46 | Things that I would never hear as Mikazuchi.\n |
| 0x1a0c90 | 29 | The real voice of the people. |
| 0x1a0cae | 48 | I guess anyone would have a hard time speaking\n |
| 0x1a0cdf | 38 | their mind in front of the real you... |
| 0x1a0d06 | 45 | And every so often, some idiot will happily\n |
| 0x1a0d34 | 46 | spout off about their villainous exploits to\n |
| 0x1a0d63 | 28 | a simple, harmless candyman. |
| 0x1a0d80 | 50 | Heh heh heh... You should see those fools' faces\n |
| 0x1a0db3 | 48 | when they realize who I truly am. Now that's a\n |
| 0x1a0de4 | 6 | treat. |
| 0x1a0deb | 47 | Of course, when they start begging for mercy,\n |
| 0x1a0e1b | 44 | their faces are nothing short of nauseating. |
| 0x1a0e48 | 7 | *Smirk* |
| 0x1a0e50 | 47 | The fur on Nekone's tail stands on end as she\n |
| 0x1a0e80 | 23 | sees that smile of his. |
| 0x1a0e98 | 13 | Hisssssssss!! |
| 0x1a0ea6 | 46 | I see... So I was right. You weren't just an\n |
| 0x1a0ed5 | 26 | ordinary fellow after all. |
| 0x1a0ef0 | 47 | Atuy has the brightest smile I've seen on her\n |
| 0x1a0f20 | 48 | so far, like a fisherman who's landed a whopper. |
| 0x1a0f51 | 48 | I suppose I'm a little curious to see how good\n |
| 0x1a0f82 | 24 | you really are, as well. |
| 0x1a0f9b | 48 | Kuon smiles ominously as she looks at Mikazuchi. |
| 0x1a0fcc | 46 | Not you too, Kuon! No sparring at the dinner\n |
| 0x1a0ffb | 39 | table! Please don't do anything stupid. |
| 0x1a1023 | 27 | I-I-I-I will take you down! |
| 0x1a103f | 47 | Nekone flails around with little punches from\n |
| 0x1a106f | 21 | behind my back again. |
| 0x1a1085 | 43 | That's not usually something you say when\n |
| 0x1a10b1 | 36 | cowering behind someone else's back. |
| 0x1a10d6 | 48 | I'm getting tired of her, so I grab her by the\n |
| 0x1a1107 | 38 | collar and hand her towards Mikazuchi. |
| 0x1a112e | 9 | Gyaaaah!? |
| 0x1a1138 | 7 | Brfph!? |
| 0x1a1140 | 48 | Nekone struggles with violent desperation, and\n |
| 0x1a1171 | 46 | her foot slams into my chin, knocking me over. |
| 0x1a11a0 | 50 | Nekone quickly scampers toward Kuon and curls up\n |
| 0x1a11d3 | 13 | on her knees. |
| 0x1a11e1 | 21 | Haha, it's all right. |
| 0x1a11f7 | 31 | Kuon gently pets Nekone's back. |
| 0x1a1217 | 50 | Mikazuchi stares at Nekone for a moment, looking\n |
| 0x1a124a | 15 | almost wistful. |
| 0x1a125a | 51 | Look, I get the whole disguise thing, but I still\n |
| 0x1a128e | 44 | don't get it. Why'd you pick a candy vendor? |
| 0x1a12bb | 46 | I ask him again, once the ruckus settles down. |
| 0x1a12ea | 19 | Is it that strange? |
| 0x1a12fe | 50 | I'm not great with small details, so all I do is\n |
| 0x1a1331 | 28 | put on a wig and a mustache. |
| 0x1a134e | 48 | It's not that it's strange... It's more how it\n |
| 0x1a137f | 49 | makes you change into a completely different guy. |
| 0x1a13b1 | 49 | The candyman looks like a friendly old guy, who\n |
| 0x1a13e3 | 36 | would probably be great with kids... |
| 0x1a1408 | 47 | And then there's regular Mikazuchi, who might\n |
| 0x1a1438 | 48 | actually be capable of glaring someone to death. |
| 0x1a1469 | 29 | How the hell did that happen? |
| 0x1a1487 | 47 | Heh heh... Well, I've always admired this look. |
| 0x1a14b7 | 43 | Admired...? A bald old man with a mustache? |
| 0x1a14e3 | 51 | Maybe Oshtor should get this guy's head examined.\n |
| 0x1a1517 | 39 | Sounds like he's a little off in there. |
| 0x1a153f | 44 | I mutter under my breath, but Oshtor grins\n |
| 0x1a156c | 42 | widely, sipping his drink and watching on. |
| 0x1a1597 | 46 | That was back when I was young. One of those\n |
| 0x1a15c6 | 38 | memories that really stays with you... |
| 0x1a15ed | 49 | Well, back then I was a little shit, to say the\n |
| 0x1a161f | 6 | least. |
| 0x1a1626 | 48 | But no matter how I acted, or who I was, there\n |
| 0x1a1657 | 46 | was a candy vendor who always treated me the\n |
| 0x1a1686 | 5 | same. |
| 0x1a168c | 49 | The old man traveled the world, selling candies\n |
| 0x1a16be | 49 | and telling stories. Bizarre, incredible, grand\n |
| 0x1a16f0 | 8 | stories. |
| 0x1a16f9 | 49 | And as he narrated, he made sugar into art with\n |
| 0x1a172b | 45 | his own rough hands. He earned this child's\n |
| 0x1a1759 | 8 | respect. |
| 0x1a1762 | 48 | A cheerful candy seller... a man loved by all.\n |
| 0x1a1793 | 32 | That's the kind of man I admire. |
| 0x1a17b4 | 45 | Mikazuchi rubs his wig as he tells his story. |
| 0x1a17e2 | 23 | This was... unexpected. |
| 0x1a17fa | 43 | Heh. Listen to me, all sentimental. Never\n |
| 0x1a1826 | 49 | imagined I'd get like this. When I look at you,\n |
| 0x1a1858 | 10 | I see him. |
| 0x1a1863 | 51 | Yes... I'd say you're just like that candy vendor\n |
| 0x1a1897 | 46 | I once knew. That's why I called on you today. |
| 0x1a18c6 | 48 | ...Hey, you calling me a bald mustached geezer\n |
| 0x1a18f7 | 4 | now? |
| 0x1a18fc | 47 | Look, it's a very touching story and all, but\n |
| 0x1a192c | 49 | you're making it weird by sitting there rubbing\n |
| 0x1a195e | 12 | on that wig. |
| 0x1a196b | 32 | Heh heh! We'll see about that.\n |
| 0x1a198c | 49 | Here, put it on! I'm sure it would look perfect\n |
| 0x1a19be | 7 | on you! |
| 0x1a19c6 | 44 | 'Course it's not going to look good on me!\n |
| 0x1a19f3 | 42 | I'm staying the hell away from that thing. |
| 0x1a1a1e | 47 | As I struggle against Mikazuchi trying to jam\n |
| 0x1a1a4e | 45 | the wig on my head, we hear a nearby sniffle. |
| 0x1a1a7c | 5 | What? |
| 0x1a1a82 | 48 | I had no idea that there was such deep meaning\n |
| 0x1a1ab3 | 25 | behind that appearance... |
| 0x1a1acd | 40 | Kiwru appears very moved by the story.\n |
| 0x1a1af6 | 33 | His eyes are starting to well up. |
| 0x1a1b18 | 45 | A guise to protect the people... Yet no one\n |
| 0x1a1b46 | 42 | can realize it is you protecting them...\n |
| 0x1a1b71 | 16 | It's so noble... |
| 0x1a1b82 | 49 | I should expect no less of a man that stands as\n |
| 0x1a1bb4 | 18 | Brother's equal... |
| 0x1a1bc7 | 48 | Kiwru gazes at Mikazuchi, eyes full of earnest\n |
| 0x1a1bf8 | 11 | admiration. |
| 0x1a1c04 | 50 | Oshtor's equal, huh. Looks like the fear he felt\n |
| 0x1a1c37 | 44 | for him has all been converted into respect. |
| 0x1a1c64 | 49 | Hmph. I didn't put that much thought into it...\n |
| 0x1a1c96 | 47 | I thought it might be interesting to mimic him. |
| 0x1a1cc6 | 4 | Him? |
| 0x1a1ccb | 45 | He told me he was trying something different. |
| 0x1a1cf9 | 50 | At the time, I too was feeling the burdens of my\n |
| 0x1a1d2c | 50 | title holding me back, so... I decided to try it\n |
| 0x1a1d5f | 7 | myself. |
| 0x1a1d67 | 49 | With that, Mikazuchi places the wig back on his\n |
| 0x1a1d99 | 12 | head. *Fwap* |
| 0x1a1da6 | 21 | By him, do you mean-- |
| 0x1a1dbc | 6 | *SLAM* |
| 0x1a1dc3 | 50 | The door suddenly flies open, drawing everyone's\n |
| 0x1a1df6 | 49 | gaze to the man standing there with arms crossed. |
| 0x1a1e28 | 44 | Sorry to keep you waiting, ladies and gents! |
| 0x1a1e55 | 27 | What the--? When did he--\n |
| 0x1a1e71 | 17 | But he was just-- |
| 0x1a1e83 | 49 | Oshtor, now Ukon, proudly strides into the room\n |
| 0x1a1eb5 | 49 | with a completely different attitude from before. |
| 0x1a1ee7 | 25 | Satch, you old bastard!\n |
| 0x1a1f01 | 11 | How's life? |
| 0x1a1f0d | 24 | Couldn't be better, Uko! |
| 0x1a1f26 | 43 | Ukon gives a thumbs up, and Sakon--who is\n |
| 0x1a1f52 | 45 | suddenly all wrinkly again--responds in kind. |
| 0x1a1f80 | 52 | An awkward silence falls as we observe the change.\n |
| 0x1a1fb5 | 41 | It's even worse now we know their other\n |
| 0x1a1fdf | 11 | identities. |
| 0x1a1feb | 36 | How the hell are you two so in sync? |
| 0x1a2010 | 50 | ...Um. I thought the two of you didn't get along\n |
| 0x1a2043 | 10 | very well. |
| 0x1a204e | 47 | Now who's been spreadin' these dumbass rumors\n |
| 0x1a207e | 9 | about us? |
| 0x1a2088 | 47 | U-Um... I heard that... wh-whenever you spar,\n |
| 0x1a20b8 | 45 | you fight as though to the death, with real\n |
| 0x1a20e6 | 10 | weapons... |
| 0x1a20f1 | 49 | What's wrong with that? It'd be a dream to have\n |
| 0x1a2123 | 43 | a sparring partner you can share that with! |
| 0x1a214f | 48 | Haw haw haw! This girlie's got the right idea!\n |
| 0x1a2180 | 22 | Here, have some candy. |
| 0x1a2197 | 16 | Hee hee! Thanks! |
| 0x1a21a8 | 42 | B-Brother, wh-what are you doing in such\n |
| 0x1a21d3 | 46 | clothes...? Please, think more of decorum in\n |
| 0x1a2202 | 16 | your appearance. |
| 0x1a2213 | 47 | What? You sayin' these clothes aren't fit for\n |
| 0x1a2243 | 48 | folks' eyes? You liked Sakon's style, didn'tcha? |
| 0x1a2274 | 41 | So it's only all right when HE does it.\n |
| 0x1a229e | 11 | Is that it? |
| 0x1a22aa | 35 | Huh!? No, that's not what I meant-- |
| 0x1a22ce | 48 | Well, you've got a point. Oshtor wouldn't wear\n |
| 0x1a22ff | 25 | these, and that's a fact! |
| 0x1a2319 | 13 | Excuse me...? |
| 0x1a2327 | 46 | The only people here are the vagabond, Ukon... |
| 0x1a2356 | 31 | And the humble candyman, Sakon. |
| 0x1a2376 | 12 | Ukon & Sakon |
| 0x1a2383 | 42 | And we don't give two SHITS about decorum! |
| 0x1a23ae | 12 | Gwahahahaha! |
| 0x1a23bb | 17 | Ahaw haw haw haw! |
| 0x1a23cd | 12 | B-Brother... |
| 0x1a23da | 47 | Neko? What's wrong? It's like there's no life\n |
| 0x1a240a | 13 | in your eyes. |
| 0x1a2418 | 46 | ...I'm sorry, Nekone. I'm not sure I can say\n |
| 0x1a2447 | 22 | anything to help here. |
| 0x1a245e | 49 | But, uh, it's usual for men to have an immature\n |
| 0x1a2490 | 41 | side to them, so don't let it get to you. |
| 0x1a24ba | 26 | I mean, just look at Haku. |
| 0x1a24d5 | 30 | Don't compare me to those two! |
| 0x1a24f4 | 49 | Hmhm! All it means is that we never forget what\n |
| 0x1a2526 | 21 | it means to be young. |
| 0x1a253c | 39 | Exactly! Call it a good sense of humor. |
| 0x1a2564 | 42 | So, what do you think about all this, kid? |
| 0x1a258f | 17 | Think about what? |
| 0x1a25a1 | 45 | The two of us here. How would y'say we look\n |
| 0x1a25cf | 13 | in your eyes? |
| 0x1a25dd | 51 | I dunno... I guess I kinda like it. I'm no expert\n |
| 0x1a2611 | 47 | on fancy manners and all that, so it's better\n |
| 0x1a2641 | 40 | than being prim and proper all the time. |
| 0x1a266a | 25 | I knew you'd get it, kid! |
| 0x1a2684 | 39 | Right! From today on, you're one of us. |
| 0x1a26ac | 47 | Hey, Maro, you wanna join? You always admired\n |
| 0x1a26dc | 39 | this kind of full-on friendship, right? |
| 0x1a2704 | 44 | Ack!? P-Please, a moment's consideration...! |
| 0x1a2731 | 28 | Oh yeah, Kiwru can join too. |
| 0x1a274e | 27 | Am I just an afterthought!? |
| 0x1a276a | 20 | Ooh, can I join too? |
| 0x1a277f | 30 | Yeah, sure! Everyone can join. |
| 0x1a279e | 31 | I suppose that includes me too? |
| 0x1a27be | 16 | M-Most likely... |
| 0x1a27cf | 49 | All righty then, I think that's enough chitchat\n |
| 0x1a2801 | 37 | out of everyone. Food's gettin' cold! |
| 0x1a2827 | 14 | Another toast! |
| 0x1a2836 | 3 | All |
| 0x1a283a | 7 | Cheers! |
| 0x1a2842 | 45 | As everyone clinks their cups, Nekone alone\n |
| 0x1a2870 | 46 | stares at me with lifeless eyes and mutters... |
| 0x1a289f | 29 | I just do not care anymore... |
| 0x1a721a | 49 | I wonder how many times I've patrolled the city\n |
| 0x1a724c | 17 | with Ukon now...? |
| 0x1a725e | 48 | As usual, he lures me out with "Drinks on me,"\n |
| 0x1a728f | 35 | and I head out to meet up with him. |
| 0x1a72b3 | 33 | Kind of a lonely place for a bar. |
| 0x1a72d5 | 48 | Not a single other person in the area. After I\n |
| 0x1a7306 | 46 | wait a little, I see Ukon striding towards me. |
| 0x1a7335 | 22 | Hey. Kept you waiting? |
| 0x1a734c | 44 | Not really, but... is there actually a bar\n |
| 0x1a7379 | 20 | somewhere like this? |
| 0x1a738e | 46 | Must be a real hole-in-the-wall kind of place. |
| 0x1a73bd | 49 | Yeah, well, I thought we could go have some fun\n |
| 0x1a73ef | 31 | before we get down to drinking. |
| 0x1a740f | 46 | Everyone's celebrating the solstice tonight.\n |
| 0x1a743e | 45 | If we find the right alley, we might find a\n |
| 0x1a746c | 17 | cockfighting den. |
| 0x1a747e | 19 | Cock... fighting?\n |
| 0x1a7492 | 14 | What the hell? |
| 0x1a74a1 | 47 | You know, roosters. Pitting them against each\n |
| 0x1a74d1 | 6 | other. |
| 0x1a74d8 | 51 | It's pretty popular round these parts. Some folks\n |
| 0x1a750c | 47 | make a living breeding and raising these birds. |
| 0x1a753c | 48 | Oh, that's what you meant... Yeah, I know what\n |
| 0x1a756d | 46 | that is. I'm guessing it's a gambling thing,\n |
| 0x1a759c | 4 | too? |
| 0x1a75a1 | 47 | Yeah. Since it's so popular, it tends to be a\n |
| 0x1a75d1 | 45 | big moneymaker for underground gambling dens. |
| 0x1a75ff | 29 | ...Underground gambling dens. |
| 0x1a761d | 51 | Some assholes start up their own illegal gambling\n |
| 0x1a7651 | 44 | dens. It's shady business--You get frauds,\n |
| 0x1a767e | 11 | cheaters... |
| 0x1a768a | 46 | Folks tend to lose not just their shirt, but\n |
| 0x1a76b9 | 42 | their farms, their property... They lose\n |
| 0x1a76e4 | 11 | everything. |
| 0x1a76f0 | 48 | Sounds rough. Hold on, though... Ukon, weren't\n |
| 0x1a7721 | 44 | you doing some investigation on this before? |
| 0x1a774e | 49 | Yeah, I've been following some rumors. They all\n |
| 0x1a7780 | 27 | led me to one gambling den. |
| 0x1a779c | 44 | It only took a little poking around to see\n |
| 0x1a77c9 | 47 | they're completely under-the-table, just like\n |
| 0x1a77f9 | 15 | I heard. But... |
| 0x1a7809 | 34 | But what...? There's some problem? |
| 0x1a782c | 44 | Well, busting these guys would be a little\n |
| 0x1a7859 | 7 | harder. |
| 0x1a7861 | 45 | Well, that's a new one. I'd figure you'd be\n |
| 0x1a788f | 44 | charging in headfirst no matter what, like\n |
| 0x1a78bc | 6 | usual. |
| 0x1a78c3 | 44 | I would if its clientele wasn't made up of\n |
| 0x1a78f0 | 33 | nobles and influential merchants. |
| 0x1a7912 | 50 | Not to mention, after some more digging, I found\n |
| 0x1a7945 | 43 | out that the one behind all of this is...\n |
| 0x1a7971 | 10 | Dekopompo. |
| 0x1a797c | 28 | Dekopompo...? Oh right, him. |
| 0x1a7999 | 50 | The guy that was busted for owning contraband...\n |
| 0x1a79cc | 32 | Looks like he just never learns. |
| 0x1a79ed | 49 | I need hard, solid proof. Otherwise, the moment\n |
| 0x1a7a1f | 47 | I try meddling, they'll throw everything they\n |
| 0x1a7a4f | 10 | can at me. |
| 0x1a7a5a | 44 | Sounds pretty tedious. Can't you just walk\n |
| 0x1a7a87 | 19 | right in as Oshtor? |
| 0x1a7a9b | 46 | I'd like nothing more. Believe me, I've come\n |
| 0x1a7aca | 40 | close to doing just that, several times. |
| 0x1a7af3 | 46 | Ukon pauses, clearly reluctant to continue--\n |
| 0x1a7b22 | 28 | expression souring somewhat. |
| 0x1a7b3f | 49 | But that'd be the worst possible action I could\n |
| 0x1a7b71 | 48 | take. I can't risk burning my bridges with the\n |
| 0x1a7ba2 | 7 | nobles. |
| 0x1a7baa | 46 | Their connections stretch through the entire\n |
| 0x1a7bd9 | 46 | capital, like a spider's web. Their reach is\n |
| 0x1a7c08 | 12 | inescapable. |
| 0x1a7c15 | 47 | This really doesn't sound like the Ukon I know. |
| 0x1a7c45 | 49 | So harsh! Imperial General of the Right or not,\n |
| 0x1a7c77 | 46 | to them I'm just a lucky kid from the boonies. |
| 0x1a7ca6 | 49 | They already look down on me for my background.\n |
| 0x1a7cd8 | 49 | If I force this, it'll tear open an irreparable\n |
| 0x1a7d0a | 5 | rift. |
| 0x1a7d10 | 50 | Those idiots only care about themselves. They'll\n |
| 0x1a7d43 | 44 | take whatever I say as "unjust persecution." |
| 0x1a7d70 | 46 | And that'd have an impact on my duties as an\n |
| 0x1a7d9f | 46 | Imperial Guard. I have to approach this with\n |
| 0x1a7dce | 8 | caution. |
| 0x1a7dd7 | 47 | I see. He may be rotten to the core, but he's\n |
| 0x1a7e07 | 29 | still a Pillar General... Hm? |
| 0x1a7e25 | 41 | Wait. Stop me if I'm wrong, but are you-- |
| 0x1a7e4f | 34 | You always do catch on quick, kid. |
| 0x1a7e72 | 42 | You remember the storage near the river?\n |
| 0x1a7e9d | 42 | The one those folks in the tenant houses\n |
| 0x1a7ec8 | 19 | were talking about? |
| 0x1a7edc | 49 | Seems Dekopompo's ship is making a stop nearby.\n |
| 0x1a7f0e | 48 | Word is, there'll be a huge cockfighting arena\n |
| 0x1a7f3f | 14 | set up inside. |
| 0x1a7f4e | 46 | This... was the entire reason you invited me\n |
| 0x1a7f7d | 15 | out, wasn't it. |
| 0x1a7f8d | 46 | Nothing to worry about. Just a little bit of\n |
| 0x1a7fbc | 25 | reconnaissance today, eh? |
| 0x1a7fd6 | 47 | I mean, I invited you to go drinking, didn't I? |
| 0x1a8006 | 48 | We're just going to slip in as guests. Nothing\n |
| 0x1a8037 | 40 | so dangerous about that. I've even got\n |
| 0x1a8060 | 12 | invitations. |
| 0x1a806d | 6 | Hmm... |
| 0x1a8074 | 46 | Besides, it's a banquet hosted by Dekopompo.\n |
| 0x1a80a3 | 44 | You can at least count on him to have fine\n |
| 0x1a80d0 | 15 | food and drink. |
| 0x1a80e0 | 33 | Hm... luxurious food and drink... |
| 0x1a8102 | 47 | I hate to admit it, but when it comes to that\n |
| 0x1a8132 | 42 | kind of thing, Dekopompo's got real taste. |
| 0x1a815d | 50 | Fine, I give up. I'm here anyways, might as well\n |
| 0x1a8190 | 49 | tag along... But if things go south, I'm out of\n |
| 0x1a81c2 | 6 | there. |
| 0x1a81c9 | 41 | Fine by me. Things wouldn't be quite as\n |
| 0x1a81f3 | 24 | interesting without you. |
| 0x1a820c | 43 | I didn't expect the ship to be this huge... |
| 0x1a8238 | 48 | Guess gaudiness can get you far. If he put all\n |
| 0x1a8269 | 50 | this effort into life, he could even be a decent\n |
| 0x1a829c | 7 | person. |
| 0x1a82a4 | 49 | All we had to do was show the invitation and we\n |
| 0x1a82d6 | 30 | got in. This feels too easy... |
| 0x1a82f5 | 48 | Well, if he's fixing the games in favor of the\n |
| 0x1a8326 | 46 | nobles, we're his prey. Less questions, more\n |
| 0x1a8355 | 15 | money for them. |
| 0x1a8365 | 41 | Now, then... let's find us some evidence. |
| 0x1a838f | 48 | We sneak down the staff-only stairs, and enter\n |
| 0x1a83c0 | 26 | the ship's storage cabins. |
| 0x1a83db | 46 | Hey, I thought you said we wouldn't be doing\n |
| 0x1a840a | 25 | anything dangerous today. |
| 0x1a8424 | 46 | Just taking a little stroll! Looking around.\n |
| 0x1a8453 | 11 | That's all. |
| 0x1a845f | 9 | Dammit... |
| 0x1a8469 | 42 | Hold it. These are... way too sturdy for\n |
| 0x1a8494 | 17 | ordinary storage. |
| 0x1a84a6 | 47 | Something's fishy here. I know it. Let's peek\n |
| 0x1a84d6 | 46 | inside... Watch the door, kid. We don't want\n |
| 0x1a8505 | 23 | any unexpected company. |
| 0x1a851d | 25 | What the hell is this...? |
| 0x1a8537 | 16 | Whoa. This is... |
| 0x1a8548 | 50 | There are giant cages set all around the room...\n |
| 0x1a857b | 45 | each of them containing vicious-looking bugs. |
| 0x1a85a9 | 48 | This can't be for... cockfighting? Unless it's\n |
| 0x1a85da | 43 | completely different from the one I know... |
| 0x1a8606 | 51 | What do you know. I figured it was just plain old\n |
| 0x1a863a | 43 | cockfighting, but it looks like we've got\n |
| 0x1a8666 | 20 | bugfighting instead. |
| 0x1a867b | 45 | Ukon heaves a sigh, then grimly surveys the\n |
| 0x1a86a9 | 14 | rows of cages. |
| 0x1a86b8 | 46 | What's wrong? I mean, it sounds pretty self-\n |
| 0x1a86e7 | 47 | explanatory, but is there something bad about\n |
| 0x1a8717 | 3 | it? |
| 0x1a871b | 44 | Yeah. It's generally the same in practice,\n |
| 0x1a8748 | 48 | except instead of birds, it's ferocious beasts\n |
| 0x1a8779 | 10 | like this. |
| 0x1a8784 | 45 | It's extremely violent, and they don't stop\n |
| 0x1a87b2 | 45 | until the opponent is dead. Popular in some\n |
| 0x1a87e0 | 13 | parts, but... |
| 0x1a87ee | 4 | But? |
| 0x1a87f3 | 43 | It's illegal to bring these bugs into the\n |
| 0x1a881f | 48 | capital. If they escape and breed, they go out\n |
| 0x1a8850 | 11 | of control. |
| 0x1a885c | 39 | Not gonna lie... This is bad. Real bad. |
| 0x1a8884 | 42 | Back in my dad's time, something similar\n |
| 0x1a88af | 47 | happened. One of these fighting bugs escaped,\n |
| 0x1a88df | 37 | and made itself a nest in the sewers. |
| 0x1a8905 | 52 | A big carnivorous bug like that needs food, and...\n |
| 0x1a893a | 43 | Well. I probably don't have to draw you a\n |
| 0x1a8966 | 8 | picture. |
| 0x1a896f | 9 | That's... |
| 0x1a8979 | 50 | They managed to exterminate them, but there were\n |
| 0x1a89ac | 50 | still plenty of victims. You can imagine how bad\n |
| 0x1a89df | 7 | it was. |
| 0x1a89e7 | 45 | They had to put half-eaten kids outta their\n |
| 0x1a8a15 | 48 | misery... Dad only talked about it when he was\n |
| 0x1a8a46 | 49 | drunk. I can't forget that emptiness in his eyes. |
| 0x1a8a78 | 9 | I... see. |
| 0x1a8a82 | 48 | This is way too heavy. I don't know what I can\n |
| 0x1a8ab3 | 13 | say to him... |
| 0x1a8ac1 | 49 | I look around and see it's not just bugs. There\n |
| 0x1a8af3 | 46 | are all kinds of dangerous creatures in there. |
| 0x1a8b22 | 45 | So I'm assuming this was the contraband you\n |
| 0x1a8b50 | 19 | were looking for... |
| 0x1a8b64 | 50 | I guess there's your solid proof. This should be\n |
| 0x1a8b97 | 30 | enough to bust the guy, right? |
| 0x1a8bb6 | 43 | I... s'pose. No, this still isn't enough.\n |
| 0x1a8be2 | 36 | I might need to dig a little deeper. |
| 0x1a8c07 | 50 | Are you serious? There's no way he could wriggle\n |
| 0x1a8c3a | 40 | out of this... What else would you need? |
| 0x1a8c63 | 39 | Trust me, he's... surprisingly devious. |
| 0x1a8c8b | 45 | No, that's not it. He just flings a load of\n |
| 0x1a8cb9 | 43 | childish excuses until it hurts to listen\n |
| 0x1a8ce5 | 9 | to him... |
| 0x1a8cef | 47 | In any case, it's going to be hard to pin him\n |
| 0x1a8d1f | 21 | down with this alone. |
| 0x1a8d35 | 49 | Let's head back up. Probably a bad idea to stay\n |
| 0x1a8d67 | 17 | here much longer. |
| 0x1a8d79 | 51 | All right. Guess there's not much we can do here.\n |
| 0x1a8dad | 24 | But bugfighting, huh...? |
| 0x1a8dc6 | 44 | I'm a little curious, and so I take a peek\n |
| 0x1a8df3 | 19 | inside the cages... |
| 0x1a8e07 | 3 | Bug |
| 0x1a8e0b | 16 | SSSSSSSSSSSSSS!! |
| 0x1a8e1c | 4 | Gah! |
| 0x1a8e21 | 48 | Rgh, that hurt... You... damn bug! All leaping\n |
| 0x1a8e52 | 30 | up and scaring me like that... |
| 0x1a8e71 | 16 | Something wrong? |
| 0x1a8e82 | 36 | Nah, just bumped into something...\n |
| 0x1a8ea7 | 22 | I'll be over in a sec. |
| 0x1a8ebe | 51 | Gah!? Y-You spineless little... uh, invertebrate!\n |
| 0x1a8ef2 | 46 | Who do you think you are? I bet I could take\n |
| 0x1a8f21 | 6 | you... |
| 0x1a8f28 | 46 | Hmph. Whatever. Not like you can do anything\n |
| 0x1a8f57 | 23 | in that cage and all... |
| 0x1a8f6f | 47 | Lucky for you, I'm feeling merciful today, so\n |
| 0x1a8f9f | 46 | I'll let that slide... Enjoy your life while\n |
| 0x1a8fce | 9 | it lasts. |
| 0x1a8fd8 | 9 | Caretaker |
| 0x1a8fe2 | 27 | Ey, those bugs still alive? |
| 0x1a8ffe | 46 | Heh. Looks like they're all nice and riled up. |
| 0x1a902d | 46 | Well, we've only been feeding them enough to\n |
| 0x1a905c | 42 | keep 'em alive. They must be starving...\n |
| 0x1a9087 | 14 | ready to kill. |
| 0x1a9096 | 47 | Heh heh heh... Well, they can kill each other\n |
| 0x1a90c6 | 37 | to their hearts' content soon enough. |
| 0x1a90ec | 47 | Let's get the job done and count how many are\n |
| 0x1a911c | 46 | left. Some of 'em probably kicked the bucket\n |
| 0x1a914b | 8 | already. |
| 0x1a9154 | 46 | Gotcha. I'll get the back, so you check this\n |
| 0x1a9183 | 5 | area. |
| 0x1a9189 | 51 | Ugh, what a pain in the ass... one, two, three...\n |
| 0x1a91bd | 35 | Huh? They're missing? Where the--\n |
| 0x1a91e1 | 24 | Hey, we're missing some! |
| 0x1a91fa | 48 | H-Hey! Shit, not good...! We're missing a lot!\n |
| 0x1a922b | 47 | They musta opened the cage and got out somehow! |
| 0x1a925b | 49 | They're missing over here, too! But these cages\n |
| 0x1a928d | 45 | don't open unless this lever is--Holy shit,\n |
| 0x1a92bb | 11 | it's down!? |
| 0x1a92c7 | 51 | This is bad... Real bad! That means all the cages\n |
| 0x1a92fb | 49 | on the boat are open! Th-This can't be happening! |
| 0x1a932d | 42 | We need to get out of here and tell the... |
| 0x1a9358 | 43 | What's wrong...? Why'd you go all quiet...? |
| 0x1a9384 | 21 | B-Behind you. Look... |
| 0x1a939a | 13 | Behind me...? |
| 0x1a93a8 | 5 | Gah!? |
| 0x1a93ae | 14 | GYAAAAAAAAHHH! |
| 0x1a93bd | 47 | I am Dekopompo, your master of ceremonies for\n |
| 0x1a93ed | 44 | the evening! I thank you all for joining me! |
| 0x1a941a | 6 | Guests |
| 0x1a9421 | 7 | Huzzah! |
| 0x1a9429 | 44 | Splendidly honored guests! I have prepared\n |
| 0x1a9456 | 46 | thrilling entertainment, and delicacies from\n |
| 0x1a9485 | 13 | far and wide. |
| 0x1a9493 | 45 | Ladies and gentlemen, enjoy to your hearts'\n |
| 0x1a94c1 | 30 | content! Nyeh peh peh peh peh! |
| 0x1a94e0 | 9 | Huzzaaah! |
| 0x1a94ea | 43 | Holy crap, this really is something else... |
| 0x1a9516 | 47 | As the host plays to the crowd, one delicious\n |
| 0x1a9546 | 46 | dish after another is carted out through the\n |
| 0x1a9575 | 5 | hall. |
| 0x1a957b | 48 | Mountains of savory meat and fish, and massive\n |
| 0x1a95ac | 45 | crystalline glasses filled with drink after\n |
| 0x1a95da | 8 | drink... |
| 0x1a95e3 | 47 | Well, it's official. This was totally worth it. |
| 0x1a9613 | 45 | The real question is, what's our first move\n |
| 0x1a9641 | 44 | going to--{W420}Kid, are you even listening? |
| 0x1a966e | 38 | You really seem out of it today, Ukon. |
| 0x1a9695 | 4 | Huh? |
| 0x1a969a | 46 | I don't know if something's up, but it feels\n |
| 0x1a96c9 | 46 | like you're rushing into this way too quickly. |
| 0x1a96f8 | 48 | Usually you'd say something like, "Can't fight\n |
| 0x1a9729 | 49 | on an empty stomach!" and eat before we get the\n |
| 0x1a975b | 9 | job done. |
| 0x1a9765 | 6 | Hrm... |
| 0x1a976c | 46 | Ah, my bad. I'm not complaining or anything.\n |
| 0x1a979b | 23 | Just seems odd, is all. |
| 0x1a97b3 | 49 | Usually you're relaxed, like you got everything\n |
| 0x1a97e5 | 40 | under control even if you joke around.\n |
| 0x1a980e | 14 | But tonight... |
| 0x1a981d | 48 | Kinda feels like you've gone all tunnel vision\n |
| 0x1a984e | 37 | on this. 'Course, maybe it's just me. |
| 0x1a9874 | 8 | I see... |
| 0x1a987d | 34 | Oh, don't take it too seriously.\n |
| 0x1a98a0 | 23 | It just occurred to me. |
| 0x1a98b8 | 45 | No, you have a point. Maybe you're right...\n |
| 0x1a98e6 | 47 | Guess you do need someone else to point these\n |
| 0x1a9916 | 11 | things out. |
| 0x1a9922 | 51 | Hoboy... gotta get a grip. Remembering everything\n |
| 0x1a9956 | 43 | my Dad said just got me a little nervous... |
| 0x1a9982 | 41 | Well, in any case, let's get some food.\n |
| 0x1a99ac | 47 | They say you don't think as quick when you're\n |
| 0x1a99dc | 7 | hungry. |
| 0x1a99e4 | 50 | Heh, right you are. Let's fill up first, then...\n |
| 0x1a9a17 | 36 | We should have enough time for that. |
| 0x1a9a3c | 43 | Can't fight on an empty stomach, after all. |
| 0x1a9a68 | 29 | Well, if that's our plan...\n |
| 0x1a9a86 | 13 | Let's dig in! |
| 0x1a9a94 | 49 | I reach for the giant bird leg I've been eyeing\n |
| 0x1a9ac6 | 42 | for a while, and get ready to chomp down-- |
| 0x1a9af1 | 4 | Crew |
| 0x1a9af6 | 11 | ARRRRRRRGH! |
| 0x1a9b02 | 14 | AHHHHHHHHHHHH! |
| 0x1a9b11 | 8 | ...Wha-- |
| 0x1a9b1a | 42 | But I stop when I hear yelling from below. |
| 0x1a9b45 | 48 | What the hell are they yelling about down there? |
| 0x1a9b76 | 42 | Hm. Maybe the main event's about to start. |
| 0x1a9ba1 | 40 | ...Main event...? Oh, the bugfighting.\n |
| 0x1a9bca | 45 | Completely forgot that's what we're here for. |
| 0x1a9bf8 | 5 | Guest |
| 0x1a9bfe | 16 | AHHHHHHHHHHHHHH! |
| 0x1a9c0f | 31 | Wh-What the--!? AHHHHHHHHHHHHH! |
| 0x1a9c2f | 46 | Whoa... Look at all the bugs coming out from\n |
| 0x1a9c5e | 8 | below... |
| 0x1a9c67 | 25 | P-Please, help meeeeeeee! |
| 0x1a9c81 | 28 | Someone! Please! Heeeeeeelp! |
| 0x1a9c9e | 29 | Wh-What the hell's going on!? |
| 0x1a9cbc | 21 | You gotta be kidding! |
| 0x1a9cd2 | 32 | ...Oh... I think I get it now.\n |
| 0x1a9cf3 | 25 | Damn, they almost had me! |
| 0x1a9d0d | 45 | This must be a little show to get the crowd\n |
| 0x1a9d3b | 40 | going. Phew, they really had me going... |
| 0x1a9d64 | 8 | ...What? |
| 0x1a9d6d | 42 | But those guys are really getting into it. |
| 0x1a9d98 | 46 | That old guy there seemed like he was really\n |
| 0x1a9dc7 | 48 | running for his life--Holy shit, a Boro-Gigiri!? |
| 0x1a9df8 | 10 | A show...? |
| 0x1a9e03 | 49 | Are they insane...? Why would they bring one of\n |
| 0x1a9e35 | 17 | those here, too!? |
| 0x1a9e47 | 47 | H-Hey, uh, this is getting pretty intense for\n |
| 0x1a9e77 | 14 | just a show... |
| 0x1a9e86 | 45 | I think I see why this stuff is so popular.\n |
| 0x1a9eb4 | 47 | After this, any plain old entertainment would\n |
| 0x1a9ee4 | 15 | be pretty dull. |
| 0x1a9ef4 | 9 | Y-Yeah... |
| 0x1a9efe | 25 | So... just a show, eh...? |
| 0x1a9f18 | 33 | I gotta hand it to that fatass.\n |
| 0x1a9f3a | 34 | He's got a flair for the dramatic. |
| 0x1a9f5d | 35 | I had no idea he was this good...\n |
| 0x1a9f81 | 23 | I'm actually impressed. |
| 0x1a9f99 | 9 | A show... |
| 0x1a9fa3 | 9 | Bug tamer |
| 0x1a9fad | 41 | Dammit! One of the caretakers must have\n |
| 0x1a9fd7 | 28 | forgotten to set the lock... |
| 0x1a9ff4 | 49 | What are those shits even good for!? Can't even\n |
| 0x1aa026 | 33 | keep some lousy bugs in a cage... |
| 0x1aa048 | 44 | Two strangely clothed men stand before the\n |
| 0x1aa075 | 12 | Boro-Gigiri. |
| 0x1aa082 | 12 | Who're they? |
| 0x1aa08f | 49 | Tamers. They're supposed to be good at handling\n |
| 0x1aa0c1 | 18 | bugs like these... |
| 0x1aa0d4 | 46 | Oh, so the plan is to calm the bugs down and\n |
| 0x1aa103 | 47 | get the crowd cheering for them. They thought\n |
| 0x1aa133 | 13 | this through! |
| 0x1aa141 | 48 | Now, calm yourself... There's nothing to fear.\n |
| 0x1aa172 | 16 | Nothing to fear. |
| 0x1aa183 | 45 | Whoa, they're actually calming the bugs down. |
| 0x1aa1b1 | 48 | Yeah. Looks like they might actually fix this... |
| 0x1aa1e2 | 21 | Yes, good. Very good. |
| 0x1aa1f8 | 21 | Now, return to your-- |
| 0x1aa20e | 11 | Boro-Gigiri |
| 0x1aa21a | 22 | *CRUNCH* *SNAP* *Drip* |
| 0x1aa231 | 7 | ...Huh? |
| 0x1aa23d | 43 | That was... way flashier than I expected... |
| 0x1aa269 | 49 | It... clearly bit his head off. And now it's...\n |
| 0x1aa29b | 9 | eating... |
| 0x1aa2a5 | 15 | What the HELL!? |
| 0x1aa2b5 | 32 | What were they even good for!?\n |
| 0x1aa2d6 | 27 | They're just getting eaten! |
| 0x1aa2f2 | 48 | This is no show... The bugs have escaped their\n |
| 0x1aa323 | 6 | cages. |
| 0x1aa32a | 3 | Man |
| 0x1aa32e | 27 | AHHHHH! Get away from me!\n |
| 0x1aa34a | 18 | Get awaaaaaaaaaay! |
| 0x1aa35d | 5 | Woman |
| 0x1aa363 | 24 | Help! Please, someone!\n |
| 0x1aa37c | 12 | Heeeeeeeelp! |
| 0x1aa389 | 48 | They're... attacking the rest of the guests on\n |
| 0x1aa3ba | 13 | the ship now. |
| 0x1aa3c8 | 48 | The bugs flooding from belowdecks are starting\n |
| 0x1aa3f9 | 48 | to rampage. The whole situation is getting out\n |
| 0x1aa42a | 10 | of hand... |
| 0x1aa435 | 37 | Wait. Where the hell is Dekopompo!?\n |
| 0x1aa45b | 37 | How does he plan on fixing this mess? |
| 0x1aa481 | 40 | Kid, clearly you don't know Dekopompo.\n |
| 0x1aa4aa | 46 | He bolted the moment we took our eyes off him. |
| 0x1aa4d9 | 49 | What!? So he's just abandoning all these guests\n |
| 0x1aa50b | 11 | he invited? |
| 0x1aa517 | 49 | Well, it's more convenient for us if he's gone.\n |
| 0x1aa549 | 28 | Now he can't get in our way. |
| 0x1aa566 | 50 | Well, I did promise. You can run if you want to,\n |
| 0x1aa599 | 4 | kid. |
| 0x1aa59e | 39 | Ukon... what are you going to do, then? |
| 0x1aa5c6 | 41 | I'm going to help the survivors escape.\n |
| 0x1aa5f0 | 44 | If we can get to the deck, there should be\n |
| 0x1aa61d | 16 | emergency boats. |
| 0x1aa62e | 50 | *Sigh*... If I run now, the guilt would kill me.\n |
| 0x1aa661 | 41 | Whatever... I'll stick it out to the end. |
| 0x1aa68b | 48 | Thanks. I could use the help. C'mon, let's get\n |
| 0x1aa6bc | 47 | folks up top while the bugs are busy fighting\n |
| 0x1aa6ec | 11 | each other. |
| 0x1aa6f8 | 49 | Whew... That should be the last of 'em. I think\n |
| 0x1aa72a | 32 | we've gotten all the guests out. |
| 0x1aa74b | 46 | How are you so relaxed? We just sent out the\n |
| 0x1aa77a | 45 | last escape boat. How are WE getting out of\n |
| 0x1aa7a8 | 6 | this!? |
| 0x1aa7af | 50 | What were we supposed to do? That boat was full.\n |
| 0x1aa7e2 | 44 | If we'd hopped on, we'd sink the damn thing. |
| 0x1aa80f | 40 | And besides, I've still got a job to do. |
| 0x1aa838 | 46 | Not here either... What about under here...?\n |
| 0x1aa867 | 7 | Nope... |
| 0x1aa86f | 34 | Sorry for dragging you along, kid. |
| 0x1aa892 | 45 | No you damn well aren't! Do you have it out\n |
| 0x1aa8c0 | 20 | for me or something? |
| 0x1aa8d5 | 41 | 'Course not. I dunno how I'm ever gonna\n |
| 0x1aa8ff | 33 | thank you for all your help, kid. |
| 0x1aa921 | 42 | I mean, you even stuck around to help me\n |
| 0x1aa94c | 20 | track down evidence! |
| 0x1aa961 | 49 | Never gonna get a better opportunity than this.\n |
| 0x1aa993 | 37 | I've gotta find it while I still can. |
| 0x1aa9b9 | 45 | And having to search all on my own would've\n |
| 0x1aa9e7 | 16 | been real rough. |
| 0x1aa9f8 | 48 | Goddammit. I knew I should have just booked it\n |
| 0x1aaa29 | 35 | at the beginning of all this... Hm? |
| 0x1aaa4d | 49 | A ledger of all the guests... and a list of all\n |
| 0x1aaa7f | 47 | the bugs on board... This what you're looking\n |
| 0x1aaaaf | 4 | for? |
| 0x1aaab4 | 46 | Jackpot! Nice work, kid! Looks like the wind\n |
| 0x1aaae3 | 22 | was at our back today. |
| 0x1aaafa | 46 | Hmph... I feel more like I'm flailing around\n |
| 0x1aab29 | 15 | in a tornado... |
| 0x1aab39 | 46 | Gah! Shit, looks like they've noticed us here. |
| 0x1aab68 | 49 | All righty then. I'd say we're done here. Let's\n |
| 0x1aab9a | 22 | make ourselves scarce. |
| 0x1aabb1 | 31 | Wh--Hey! Don't leave me behind! |
| 0x1aabd1 | 49 | Just as I'm leaving, I notice a golden statue--\n |
| 0x1aac03 | 45 | garish, half-naked, and about as big as two\n |
| 0x1aac31 | 6 | fists. |
| 0x1aac38 | 47 | ...Not really my style, but it could be worth\n |
| 0x1aac68 | 46 | a lot. After all I went through, I deserve a\n |
| 0x1aac97 | 9 | souvenir. |
| 0x1aaca1 | 29 | Hrrngh... Argh, it's heavy... |
| 0x1aacbf | 40 | I secure the golden statue in my sash,\n |
| 0x1aace8 | 35 | trying to keep it from falling out. |
| 0x1aad0c | 26 | What're you DOING, kid!?\n |
| 0x1aad27 | 15 | They're coming! |
| 0x1aad37 | 48 | Oh shit. All right, golden goddess, if you can\n |
| 0x1aad68 | 29 | protect me, now's the time... |
| 0x1aad86 | 47 | We need to get out on deck. As long as we get\n |
| 0x1aadb6 | 17 | outside, we can-- |
| 0x1aadc8 | 11 | SSSSSSSSSS! |
| 0x1aadd4 | 41 | When we try to get out onto the deck, a\n |
| 0x1aadfe | 39 | Boro-Gigiri appears, blocking our path. |
| 0x1aae26 | 46 | We can also hear scuttling across the wooden\n |
| 0x1aae55 | 31 | floor, a little ways behind us. |
| 0x1aae75 | 29 | Dammit, we're surrounded...\n |
| 0x1aae93 | 23 | And we were so close... |
| 0x1aaeab | 48 | We won't be able to get out on the deck unless\n |
| 0x1aaedc | 29 | we get past this Boro-Gigiri. |
| 0x1aaefa | 49 | But that'll be suicide. There's no way we could\n |
| 0x1aaf2c | 32 | get past this thing unscathed... |
| 0x1aaf4d | 47 | If only we had a way to distract it just long\n |
| 0x1aaf7d | 9 | enough... |
| 0x1aaf87 | 46 | I'll hold them off, kid. You gotta run while\n |
| 0x1aafb6 | 11 | you still-- |
| 0x1aafc2 | 5 | Ukon! |
| 0x1aafc8 | 45 | I point to the lamp stand that was standing\n |
| 0x1aaff6 | 8 | near us. |
| 0x1aafff | 24 | Count down from three.\n |
| 0x1ab018 | 15 | You good to go? |
| 0x1ab028 | 8 | ...Yeah. |
| 0x1ab031 | 8 | Three... |
| 0x1ab03a | 6 | Two... |
| 0x1ab041 | 6 | One... |
| 0x1ab048 | 11 | Haku & Ukon |
| 0x1ab054 | 10 | Take this! |
| 0x1ab05f | 44 | We grab the lamp, and hurl it at the Boro-\n |
| 0x1ab08c | 7 | Gigiri. |
| 0x1ab094 | 13 | SSSSSSSSSSSS! |
| 0x1ab0a2 | 51 | It hits the Boro-Gigiri at just the perfect angle\n |
| 0x1ab0d6 | 48 | to spill oil all over it--catching fire almost\n |
| 0x1ab107 | 12 | immediately. |
| 0x1ab114 | 23 | SSSSSSSS! SSSSSSSSSSSS! |
| 0x1ab12c | 46 | The Boro-Gigiri thrashes and writhes, flames\n |
| 0x1ab15b | 23 | coursing over its body. |
| 0x1ab173 | 15 | Yes! We did it! |
| 0x1ab183 | 51 | The Boro-Gigiri's thrashing seems to be spreading\n |
| 0x1ab1b7 | 49 | the fire across the deck. Everything's burning... |
| 0x1ab1e9 | 8 | ...Crap. |
| 0x1ab1f2 | 47 | Of COURSE we had to do that while standing on\n |
| 0x1ab222 | 46 | an extremely flammable deck. Well, that's it\n |
| 0x1ab251 | 13 | for the ship. |
| 0x1ab25f | 40 | What are you being so nonchalant for!?\n |
| 0x1ab288 | 26 | We're out of escape boats! |
| 0x1ab2a3 | 29 | Say, kid, you a good swimmer? |
| 0x1ab2c1 | 22 | You aren't seriously-- |
| 0x1ab2d8 | 47 | If we don't have any boats, we can just swim.\n |
| 0x1ab308 | 30 | The shore's not THAT far away. |
| 0x1ab327 | 34 | Are you kidding!? In this cold!?\n |
| 0x1ab34a | 50 | ...Goddammit. So our choices are freeze to death\n |
| 0x1ab37d | 17 | or burn to death? |
| 0x1ab38f | 12 | Bwahahahaha! |
| 0x1ab39c | 10 | GODDAMMIT! |
| 0x1ab3a7 | 46 | The two of us run across the deck to the side. |
| 0x1ab3d6 | 48 | Once we reach the side of the boat, both of us\n |
| 0x1ab407 | 20 | leap into the river. |
| 0x1ab41c | 49 | ...And I sink like a rock, down into the watery\n |
| 0x1ab44e | 7 | depths. |
| 0x1ab456 | 26 | Blblblb!? Blb blblbl blb!? |
| 0x1ab471 | 50 | As I feel myself slipping away, and the numbness\n |
| 0x1ab4a4 | 50 | sets in, I see the golden statue smiling from my\n |
| 0x1ab4d7 | 5 | sash. |
| 0x1ab4dd | 18 | Or so I thought... |
| 0x1ab4f0 | 21 | Guh, hahh, pfahh...\n |
| 0x1ab506 | 21 | *Cough, cough, cough* |
| 0x1ab51c | 50 | Took you a while there, kid. I was getting kinda\n |
| 0x1ab54f | 35 | worried when you weren't coming up. |
| 0x1ab573 | 23 | Hahh... hahh... hahh... |
| 0x1ab58b | 42 | Hm? What happened to that goddess statue\n |
| 0x1ab5b6 | 8 | you had? |
| 0x1ab5bf | 47 | Goddess my ass! If I hadn't thrown that thing\n |
| 0x1ab5ef | 44 | away when I did, I would've drowned like a\n |
| 0x1ab61c | 4 | rat! |
| 0x1ab621 | 46 | I thought I saw that thing beckoning me into\n |
| 0x1ab650 | 13 | the darkness! |
| 0x1ab65e | 45 | Huh... I wouldn't have thought it was real,\n |
| 0x1ab68c | 31 | but maybe the rumors were true. |
| 0x1ab6ac | 10 | ...Rumors? |
| 0x1ab6b7 | 51 | Well, let's see... I heard a rumor that Dekopompo\n |
| 0x1ab6eb | 50 | found some goddess statue that brings its owners\n |
| 0x1ab71e | 9 | bad luck. |
| 0x1ab728 | 45 | Maybe that goddess was the one you picked up. |
| 0x1ab756 | 45 | After all, look at what happened to the boat. |
| 0x1ab784 | 46 | Ukon jerks his head in the general direction\n |
| 0x1ab7b3 | 12 | of the boat. |
| 0x1ab7c0 | 26 | That thing's up in blazes. |
| 0x1ab7db | 46 | That gorgeous barge is nothing but a ball of\n |
| 0x1ab80a | 46 | flame now. The flames paint the night sky in\n |
| 0x1ab839 | 10 | vivid red. |
| 0x1ab844 | 48 | Good thing you weren't taken in by its beauty.\n |
| 0x1ab875 | 46 | Knowing you, maybe the goddess took a liking\n |
| 0x1ab8a4 | 11 | to you, eh? |
| 0x1ab8b0 | 33 | A knowing smile crosses his face. |
| 0x1ab8d2 | 32 | Wait, then that vision I saw...? |
| 0x1ab8f3 | 18 | Nah... Can't be... |
| 0x1ab906 | 49 | After some effort, we finally make it to shore.\n |
| 0x1ab938 | 44 | The whole area's in a panic because of the\n |
| 0x1ab965 | 12 | ship's fire. |
| 0x1ab972 | 41 | Whew, I'm starting to feel alive again... |
| 0x1ab99c | 47 | One of Ukon's subordinates got us a change of\n |
| 0x1ab9cc | 48 | clothes, but the cold night air of the capital\n |
| 0x1ab9fd | 9 | is rough. |
| 0x1aba07 | 48 | I huddle up near a fire close to the riverbank\n |
| 0x1aba38 | 18 | to warm myself up. |
| 0x1aba4b | 50 | As for Ukon, he's waiting for the capital guards\n |
| 0x1aba7e | 46 | to arrive on the scene. He said he'd join me\n |
| 0x1abaad | 6 | later. |
| 0x1abab4 | 44 | The burning boat is clearly visible in the\n |
| 0x1abae1 | 10 | moonlight. |
| 0x1abaec | 45 | I don't have anything else to do, so I just\n |
| 0x1abb1a | 46 | watch until the ship crumbles and sinks into\n |
| 0x1abb49 | 10 | the river. |
| 0x1abb54 | 47 | With the show over, the spectators head home,\n |
| 0x1abb84 | 48 | and the area is totally silent... like nothing\n |
| 0x1abbb5 | 14 | ever happened. |
| 0x1abbc4 | 39 | After a while, I hear faint footsteps\n |
| 0x1abbec | 12 | approaching. |
| 0x1abbf9 | 31 | Man, oh man. What a day, huh?\n |
| 0x1abc19 | 30 | Thanks for all your help, kid. |
| 0x1abc38 | 13 | You all done? |
| 0x1abc46 | 48 | Yeah. Evacuating all the guests saved us a lot\n |
| 0x1abc77 | 22 | of trouble in the end. |
| 0x1abc8e | 44 | It's the capital guards' job from here on.\n |
| 0x1abcbb | 45 | I explained the situation and left the rest\n |
| 0x1abce9 | 8 | to them. |
| 0x1abcf2 | 41 | Me, well, I just did what had to be done. |
| 0x1abd1c | 43 | Ukon taps his coat as he says this... The\n |
| 0x1abd48 | 40 | pocket containing our hard-won evidence. |
| 0x1abd71 | 45 | More importantly, kid, can you tell me what\n |
| 0x1abd9f | 8 | this is? |
| 0x1abda8 | 44 | With that Ukon raises a rather large bottle. |
| 0x1abdd5 | 46 | The bottle itself is white and ceramic, with\n |
| 0x1abe04 | 48 | a blue overglaze design. Just from that, I can\n |
| 0x1abe35 | 26 | tell it's expensive stuff. |
| 0x1abe50 | 15 | Where did you-- |
| 0x1abe60 | 44 | Eh, found it washed up on shore. Guess not\n |
| 0x1abe8d | 42 | everything on the ship got caught in the\n |
| 0x1abeb8 | 6 | blaze. |
| 0x1abebf | 50 | After all that chaos, it managed to land here in\n |
| 0x1abef2 | 43 | our laps. Only proper that we drink it, eh? |
| 0x1abf1e | 35 | He grins broadly, tossing me a cup. |
| 0x1abf42 | 49 | After all, I promised you drinks, but we didn't\n |
| 0x1abf74 | 36 | even get a bite of that swanky food. |
| 0x1abf99 | 37 | I got some sides to go with it too.\n |
| 0x1abfbf | 45 | Nothin' exactly on the level of Dekopompo's\n |
| 0x1abfed | 22 | feast, but good stuff. |
| 0x1ac004 | 44 | I know this doesn't really make up for it,\n |
| 0x1ac031 | 45 | but hey. It's the thought that counts, right? |
| 0x1ac05f | 47 | ...I dunno. This is pretty good in its own way. |
| 0x1ac08f | 16 | Glad to hear it. |
| 0x1ac0a0 | 26 | Ukon offers me the bottle. |
| 0x1ac0bb | 46 | I lift my cup in response, and he pours me a\n |
| 0x1ac0ea | 23 | beautiful amber liquid. |
| 0x1ac102 | 12 | Here you go. |
| 0x1ac10f | 45 | I take the bottle next, and offer it to Ukon. |
| 0x1ac13d | 7 | Thanks. |
| 0x1ac145 | 19 | Well, in any case-- |
| 0x1ac159 | 7 | Cheers. |
| 0x1ac161 | 44 | The clinking of the two cups echoes with a\n |
| 0x1ac18e | 41 | strange serenity through the still night. |
| 0x1ac1b8 | 5 | Phew. |
| 0x1ac1be | 49 | We both finish our drinks, and let out sighs of\n |
| 0x1ac1f0 | 13 | satisfaction. |
| 0x1ac1fe | 25 | That's some good stuff... |
| 0x1ac218 | 19 | ...Yeah. Damn good. |
| 0x1ac22c | 47 | I'm not a fan of his interior decorating, but\n |
| 0x1ac25c | 40 | you were right about his food and drink. |
| 0x1ac285 | 47 | I have to worry about my wallet when I drink,\n |
| 0x1ac2b5 | 45 | while that fatass chugs this quality stuff... |
| 0x1ac2e3 | 30 | It's a cruel world we live in. |
| 0x1ac302 | 49 | Heh heh... Look at that, kid. The moon's filled\n |
| 0x1ac334 | 22 | up just right tonight. |
| 0x1ac34b | 47 | Drinking and enjoying the moonlight like this\n |
| 0x1ac37b | 46 | with a friend... I'd say that's real luxury,\n |
| 0x1ac3aa | 13 | wouldn't you? |
| 0x1ac3b8 | 46 | Ukon gazes fondly up at a perfect half-moon.\n |
| 0x1ac3e7 | 37 | It almost looks like one of our cups. |
| 0x1ac40d | 50 | Shame it's not a full moon, but after a few days\n |
| 0x1ac440 | 44 | we'll get to see it in all its brilliance... |
| 0x1ac46d | 39 | Hey, a full moon isn't the only kind.\n |
| 0x1ac495 | 47 | I kinda like being able to see both the light\n |
| 0x1ac4c5 | 15 | and the shadow. |
| 0x1ac4d5 | 47 | And besides, it looks a bit like one of these\n |
| 0x1ac505 | 49 | cups. Kinda like we're sharing a drink with the\n |
| 0x1ac537 | 10 | moon, huh? |
| 0x1ac542 | 12 | ...Hahahaha! |
| 0x1ac54f | 47 | Never took you for a poet. Yeah, now that you\n |
| 0x1ac57f | 36 | mention it, it does look like a cup. |
| 0x1ac5a4 | 49 | Heh... Light and darkness. Kinda like a certain\n |
| 0x1ac5d6 | 15 | someone I know. |
| 0x1ac5e6 | 46 | He's got a face that lights up for the world\n |
| 0x1ac615 | 49 | to see, but a shadowy one too. Wonder which one\n |
| 0x1ac647 | 17 | is his real face. |
| 0x1ac659 | 34 | Who knows...? Oshtor and Ukon...\n |
| 0x1ac67c | 35 | Neither of them are whole people.\n |
| 0x1ac6a0 | 17 | Not on their own. |
| 0x1ac6b2 | 48 | Ukon mumbles quietly, like he's saying it more\n |
| 0x1ac6e3 | 45 | for himself. He's quiet for a while, gazing\n |
| 0x1ac711 | 8 | skyward. |
| 0x1ac71a | 51 | ...Hey, kid. There's something I want to ask you.\n |
| 0x1ac74e | 46 | You don't have to answer if you don't want to. |
| 0x1ac77d | 32 | Hm? What's this all of a sudden? |
| 0x1ac79e | 49 | How does it feel... to have no memories of your\n |
| 0x1ac7d0 | 33 | past? Do you ever want them back? |
| 0x1ac7f2 | 42 | Oh, that? Well, it feels... You know, it\n |
| 0x1ac81d | 33 | really hasn't bothered me before. |
| 0x1ac83f | 45 | And wanting my memories back... I mean, I'm\n |
| 0x1ac86d | 44 | pretty satisfied with how my life is going\n |
| 0x1ac89a | 13 | without them. |
| 0x1ac8a8 | 44 | Besides, the memories I get back might not\n |
| 0x1ac8d5 | 35 | necessarily be good ones, you know? |
| 0x1ac8f9 | 45 | Haha... Figures I'd get an answer like that\n |
| 0x1ac927 | 14 | from you, kid. |
| 0x1ac936 | 47 | I may not be whole myself, what with the huge\n |
| 0x1ac966 | 45 | gap in my past, but I'm alive and I'm doing\n |
| 0x1ac994 | 5 | fine. |
| 0x1ac99a | 50 | And having no past means I don't have to act out\n |
| 0x1ac9cd | 33 | two different parts, like you do. |
| 0x1ac9ef | 7 | True... |
| 0x1ac9f7 | 34 | Guess we're similar in that way.\n |
| 0x1aca1a | 43 | Neither of us feel like we're whole people. |
| 0x1aca46 | 49 | 'Course, compared to you, I have a family I can\n |
| 0x1aca78 | 46 | call my own, so maybe I'm a little better off. |
| 0x1acaa7 | 51 | Ukon pensively stares into the distance, drinking\n |
| 0x1acadb | 28 | from his cup in the silence. |
| 0x1acaf8 | 48 | So... do you ever feel afraid about not having\n |
| 0x1acb29 | 25 | anything to fall back on? |
| 0x1acb43 | 31 | Not really. I got used to it.\n |
| 0x1acb63 | 28 | I mean, life happens, right? |
| 0x1acb80 | 43 | Heh... I really envy you for that attitude. |
| 0x1acbac | 5 | Envy? |
| 0x1acbb2 | 50 | I may not look it, but I AM from a noble family.\n |
| 0x1acbe5 | 44 | A poor one, anyway, from out in the country. |
| 0x1acc12 | 41 | There was me, my mom, Nekone, and my dad. |
| 0x1acc3c | 49 | My dad was strict, but kind... He spent all his\n |
| 0x1acc6e | 47 | time with the people. Really understood them.\n |
| 0x1acc9e | 15 | He was my hero. |
| 0x1accae | 50 | I trained myself so I could be like him one day.\n |
| 0x1acce1 | 49 | Studying, cramming my brains out, working hard... |
| 0x1acd13 | 36 | It never felt tough to me, though.\n |
| 0x1acd38 | 21 | All I felt was pride. |
| 0x1acd4e | 45 | I chased my dad's legacy all the way to the\n |
| 0x1acd7c | 42 | imperial capital... and after a bunch of\n |
| 0x1acda7 | 50 | coincidences, I'm now Imperial Guard of the Right. |
| 0x1acdda | 50 | But like I told you, I found out there were more\n |
| 0x1ace0d | 45 | and more things that Oshtor just couldn't do. |
| 0x1ace3b | 48 | And that's why you started to play the part of\n |
| 0x1ace6c | 46 | Ukon. Yeah, I remember you talking about that. |
| 0x1ace9b | 48 | Heh, yeah. It was embarrassing at first, but I\n |
| 0x1acecc | 47 | realized Ukon was a lot closer to my image of\n |
| 0x1acefc | 7 | my dad. |
| 0x1acf04 | 48 | It was... Ukon's life that I had been striving\n |
| 0x1acf35 | 35 | toward all this time. Not Oshtor's. |
| 0x1acf59 | 46 | But I can't just shirk the duties I've taken\n |
| 0x1acf88 | 31 | on... Ah, I'm just venting now. |
| 0x1acfa8 | 46 | The classic rags to riches story. Except you\n |
| 0x1acfd7 | 43 | just see it as a bunch of coincidences...\n |
| 0x1ad003 | 15 | Kind of ironic. |
| 0x1ad013 | 43 | But with you around, I think I'm actually\n |
| 0x1ad03f | 21 | enjoying myself more. |
| 0x1ad055 | 27 | Where'd that one come from? |
| 0x1ad071 | 49 | If I'd gone alone, things might've gone public,\n |
| 0x1ad0a3 | 47 | and made a huge mess. But thanks to you, it's\n |
| 0x1ad0d3 | 27 | all settled, neat and tidy. |
| 0x1ad0ef | 27 | So... just got me thinkin'. |
| 0x1ad10b | 48 | Whatever obstacles lie in our path, as long as\n |
| 0x1ad13c | 43 | you're with me, I'll get over 'em. Somehow. |
| 0x1ad168 | 45 | So... what? You saying you're gonna drag me\n |
| 0x1ad196 | 37 | along on more crazy plans like today? |
| 0x1ad1bc | 7 | Hahaha! |
| 0x1ad1c4 | 45 | "Hahaha" my ass! I asked you a damn question. |
| 0x1ad1f2 | 13 | Gahahahahaha! |
| 0x1ad200 | 46 | And we talk together like this, laughing and\n |
| 0x1ad22f | 24 | drinking, until sunrise. |
| 0x1ad59c | 27 | Well, I should get going.\n |
| 0x1ad5b8 | 43 | You know how my brother gets when I'm late. |
| 0x1ad5e4 | 5 | Woman |
| 0x1ad5ea | 45 | You're sticking your nose into some strange\n |
| 0x1ad618 | 30 | business again, aren't you...? |
| 0x1ad637 | 50 | Wow, rude. For your information, I'm heading out\n |
| 0x1ad66a | 24 | on a very noble mission. |
| 0x1ad683 | 51 | I really do worry... You don't have to stay here.\n |
| 0x1ad6b7 | 17 | You can always... |
| 0x1ad6c9 | 38 | ...You know you can come back anytime. |
| 0x1ad6f0 | 45 | We've kept your room just as you left it...\n |
| 0x1ad71e | 42 | I've made sure to clean it every day, too. |
| 0x1ad749 | 48 | ...Although Chii does sneak in and draw things\n |
| 0x1ad77a | 31 | on the walls from time to time. |
| 0x1ad79a | 33 | But it wouldn't bother us at all. |
| 0x1ad7bc | 7 | Well... |
| 0x1ad7c4 | 49 | ...Yeah, maybe. When this whole business is all\n |
| 0x1ad7f6 | 35 | over, I'll... give it some thought. |
| 0x1ad81a | 45 | She can probably tell I'm just saying it to\n |
| 0x1ad848 | 45 | get her off my case... I can't meet her eyes. |
| 0x1ad876 | 35 | ...You seem so distant, these days. |
| 0x1ad89a | 41 | Back then, it felt like you were always\n |
| 0x1ad8c4 | 39 | trailing around after the two of us...  |
| 0x1ad8ec | 17 | What happened...? |
| 0x1ad8fe | 9 | That's... |
| 0x1ad908 | 32 | That's because I... I mean, I... |

## 8. Formato de saida EXIGIDO
Escreva `translations_19_08.json` com a forma:
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
