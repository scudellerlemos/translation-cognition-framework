# Cena ch_15_02 — pacote de traducao (411 linhas)

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
| Gigiri | Criatura | Gigiri | manter_original | none |
| Haku | Personagem | Haku | manter_original | moderate |
| Imperial Guard | Organizacao | Guarda Imperial | traduzir | none |
| Kuon | Personagem | Kuon | manter_original | none |
| Maro | Personagem | Maro | manter_original | none |
| Maroro | Personagem | Maroro | manter_original | none |
| Master | Cultural | Mestre | traduzir | none |
| Mikado | Titulo | Mikado | manter_original | major |
| Nekone | Personagem | Nekone | manter_original | moderate |
| Oshtor | Personagem | Oshtor | manter_original | major |
| Rulutieh | Personagem | Rulutieh | manter_original | none |
| Ukon | Personagem | Ukon | manter_original | major |
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

## 6. Memoria de traducao (consistencia — nao reinventar)
**Falas identicas ja traduzidas (reusar):**
- `that.` -> `disso.` (Estalajadeira, 11_08)
- `I guess.` -> `eu acho.` (Haku, 11_10)
- `Kuon?` -> `Kuon?` (Haku, 12_04)
- `I guess I have no choice...` -> `Acho que não tenho escolha...` (Haku, 13_02)
- `least.` -> `enfim.` (Ukon, 12_12)
- `right?` -> `né?` (Haku, 12_03)
- `Thank you, dear sister.` -> `Obrigada, cara irmã.` (Nekone, 15_01)
- `What?` -> `Que?` (Haku, 12_02)
- `now...` -> `agora...` (Haku, 12_03)
- `Urgh...` -> `Argh...` (Haku, 11_06)
- `noticing.` -> `perceber.` (Haku, 12_11)
- `basically.` -> `basicamente.` (Kuon, 11_06)
- `...Huh?` -> `...Hein?` (Kuon, 11_07)
- `surely.` -> `certamente.` (Ougi, 13_08)
- `What's this?` -> `O que é isso?` (Haku, 12_08)
- `eyes.` -> `olhar.` (Haku, 14_04)
- `Huh...?` -> `Hein...?` (Haku, 11_03)
- `Here.` -> `Aqui.` (Kuon, 11_09)
- `Ahahahaha!` -> `Ahahaha!` (Homem, 14_06)
- `you?` -> `pode?` (Haku, 13_01)
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
| 0xac746 | 27 | All right, let's get to it. |
| 0xac762 | 47 | No sooner than we return to the inn does Kuon\n |
| 0xac792 | 44 | lay claim to a section of the room, saying\n |
| 0xac7bf | 5 | that. |
| 0xac7c5 | 6 | Why... |
| 0xac7cc | 49 | I hold my head in my hands, taking in the state\n |
| 0xac7fe | 43 | of the room. Kuon and Nekone stand at the\n |
| 0xac82a | 8 | ready... |
| 0xac833 | 14 | Have some tea. |
| 0xac842 | 48 | ...While Rulutieh serves tea and cakes, as ever. |
| 0xac873 | 44 | Is it really OK for a princess to be doing\n |
| 0xac8a0 | 45 | stuff like this...? As long as she's happy,\n |
| 0xac8ce | 8 | I guess. |
| 0xac8d7 | 48 | So, what are we going to do? Like, in general,\n |
| 0xac908 | 44 | from here on out? I'm at a loss for how to\n |
| 0xac935 | 8 | proceed. |
| 0xac93e | 49 | Didn't Kuon say we were gonna give the job hunt\n |
| 0xac970 | 43 | a rest for a bit? And now I'm back to the\n |
| 0xac99c | 13 | grindstone... |
| 0xac9aa | 46 | Don't worry about that. For now, we're going\n |
| 0xac9d9 | 42 | to focus on turning you into our group's\n |
| 0xaca04 | 7 | "face." |
| 0xaca0c | 8 | ...Face. |
| 0xaca15 | 42 | Would you prefer "representative" instead? |
| 0xaca40 | 49 | We need a face, considering the kinds of things\n |
| 0xaca72 | 44 | we'll be doing. Someone who can be our Ukon. |
| 0xaca9f | 47 | Oh, no, I get that much. I just... don't know\n |
| 0xacacf | 47 | what's really expected of me, if I'm gonna be\n |
| 0xacaff | 9 | that guy. |
| 0xacb09 | 43 | It's not complicated. You just have to...\n |
| 0xacb35 | 41 | well, represent us. Project our group's\n |
| 0xacb5f | 9 | attitude. |
| 0xacb69 | 32 | Eh, I guess that's not so bad... |
| 0xacb8a | 33 | Seems easy enough, if that's all. |
| 0xacbac | 42 | But representing the whole group, huh...\n |
| 0xacbd7 | 43 | Wouldn't you be a better choice for that,\n |
| 0xacc03 | 5 | Kuon? |
| 0xacc09 | 43 | You think? Someone popular and well-liked\n |
| 0xacc35 | 46 | would be best, which is why I think you'd be\n |
| 0xacc64 | 13 | suited to it. |
| 0xacc72 | 43 | I-I see. Well, when you put it like that,\n |
| 0xacc9e | 27 | I guess I have no choice... |
| 0xaccbe | 43 | So Haku will be our face, and... If we're\n |
| 0xaccea | 43 | emulating Ukon, we're going to need to do\n |
| 0xacd16 | 11 | recruiting. |
| 0xacd22 | 45 | Yeah, he's got, what--more than twenty men?\n |
| 0xacd50 | 35 | The four of us won't really cut it. |
| 0xacd74 | 47 | My dear brother indicated to me he handpicked\n |
| 0xacda4 | 46 | each of those twenty. All are men who showed\n |
| 0xacdd3 | 8 | promise. |
| 0xacddc | 44 | Well, about that. I'd like to start with a\n |
| 0xace09 | 45 | smaller, trustworthy group--do stuff on our\n |
| 0xace37 | 13 | own to start. |
| 0xace45 | 11 | Just us...? |
| 0xace51 | 43 | Won't that be making things unnecessarily\n |
| 0xace7d | 24 | difficult for ourselves? |
| 0xace96 | 50 | Ahaha, well, um. We don't exactly have... money.\n |
| 0xacec9 | 32 | To recruit new comrades, I mean. |
| 0xaceea | 48 | What? Wait a second, didn't we just get, like,\n |
| 0xacf1b | 15 | a HEAP of cash? |
| 0xacf2b | 46 | Mm, we did, but... I used it up to arrange a\n |
| 0xacf5a | 47 | long-term contract with the inn so we can use\n |
| 0xacf8a | 12 | these rooms. |
| 0xacf97 | 39 | ...Huh? What do you mean, "used it up"? |
| 0xacfbf | 44 | We need a base of operations. The contract\n |
| 0xacfec | 42 | includes rooms for everyone, at the very\n |
| 0xad017 | 6 | least. |
| 0xad01e | 46 | Wait, wait. I understand we need a base, but\n |
| 0xad04d | 39 | we can't do much with it if you spend\n |
| 0xad075 | 14 | ALL OUR MONEY. |
| 0xad084 | 45 | It won't be a problem. I wasn't planning on\n |
| 0xad0b2 | 45 | hiring any outside contractors to begin with. |
| 0xad0e0 | 7 | ...Why? |
| 0xad0e8 | 38 | Based on what Ukon told us, a small,\n |
| 0xad10f | 38 | inconspicuous group can move without\n |
| 0xad136 | 21 | attracting attention. |
| 0xad14c | 48 | In which case, I think keeping our numbers low\n |
| 0xad17d | 14 | would be best. |
| 0xad18c | 45 | And how did you arrive at that conclusion...? |
| 0xad1ba | 41 | Even though Ukon hired us to act as his\n |
| 0xad1e4 | 48 | counterparts, I don't think he intends to stop\n |
| 0xad215 | 14 | working fully. |
| 0xad224 | 46 | I suspect he'll continue working just enough\n |
| 0xad253 | 34 | to keep attention off of OUR work. |
| 0xad276 | 46 | In which case, we can pass jobs that require\n |
| 0xad2a5 | 46 | manpower to him, and take more delicate ones\n |
| 0xad2d4 | 10 | ourselves. |
| 0xad2df | 48 | That way, we won't be as likely to be hindered\n |
| 0xad310 | 10 | by others. |
| 0xad31b | 9 | Hindered? |
| 0xad325 | 18 | You noticed, then. |
| 0xad338 | 45 | I couldn't help but notice. One of the Twin\n |
| 0xad366 | 47 | Shields struggling to drum up funds stinks of\n |
| 0xad396 | 10 | foul play. |
| 0xad3a1 | 45 | Does your brother have enemies who would be\n |
| 0xad3cf | 20 | out to sabotage him? |
| 0xad3e4 | 42 | Our family was low-ranked, noble only in\n |
| 0xad40f | 42 | title--so his rise to Imperial Guard was\n |
| 0xad43a | 14 | unprecedented. |
| 0xad449 | 50 | On top of that, he's well-liked and the Mikado's\n |
| 0xad47c | 46 | confidant. Older titled families must resent\n |
| 0xad4ab | 4 | him. |
| 0xad4b0 | 46 | Yes. We must remain vigilant of conspiracies\n |
| 0xad4df | 47 | against our house at all times. Discretion is\n |
| 0xad50f | 10 | paramount. |
| 0xad51a | 47 | Is that why you refer to yourself as "Ukon's"\n |
| 0xad54a | 30 | younger sister, instead of...? |
| 0xad569 | 11 | ...Just so. |
| 0xad575 | 42 | So even a superpower like Yamato has its\n |
| 0xad5a0 | 43 | conniving underbelly... or perhaps that's\n |
| 0xad5cc | 19 | natural for nobles. |
| 0xad5e0 | 47 | I know the old imperial courts were rife with\n |
| 0xad610 | 41 | intrigue, but even Oshtor has it rough... |
| 0xad63a | 49 | I'm not really sure I understand, but I take it\n |
| 0xad66c | 44 | that means things won't exactly go smoothly? |
| 0xad699 | 18 | Um, dear sister... |
| 0xad6ac | 42 | Ah heh heh. I have to thank you, really,\n |
| 0xad6d7 | 41 | Nekone. You've pulled us into something\n |
| 0xad701 | 12 | interesting. |
| 0xad70e | 6 | Eh...? |
| 0xad715 | 6 | Right? |
| 0xad71c | 14 | Dear sister... |
| 0xad72b | 45 | Well, I guess Kuon WOULD say something like\n |
| 0xad759 | 50 | That's fine and all, but even if a "small" group\n |
| 0xad78c | 45 | is our goal, isn't just us four... TOO small? |
| 0xad7ba | 47 | I understand we don't have any kind of budget\n |
| 0xad7ea | 41 | now, but we're still going to need more\n |
| 0xad814 | 7 | people. |
| 0xad81c | 46 | Hrm. I suppose if there's no other choice...\n |
| 0xad84b | 34 | I can dip into the secret savings. |
| 0xad86e | 34 | Oh? We have some money, after all? |
| 0xad891 | 23 | Thank you, dear sister. |
| 0xad8a9 | 46 | Oh, no, thank Haku. It's his money, after all. |
| 0xad8d8 | 5 | WHAT? |
| 0xad8de | 42 | Hey, hey, wait, what do you mean it's my-- |
| 0xad909 | 47 | You heard me. It WAS your pay from the gigiri\n |
| 0xad939 | 48 | hunt. I was planning on saving it for you, but\n |
| 0xad96a | 6 | now... |
| 0xad971 | 21 | What do you mean WAS? |
| 0xad987 | 35 | Well, you're our leader, after all. |
| 0xad9ab | 7 | Urgh... |
| 0xad9b3 | 34 | I-If that's the case, then I qui-- |
| 0xad9d6 | 45 | Kuon stops me, indicating the others with a\n |
| 0xada04 | 14 | furtive point. |
| 0xada13 | 31 | I see. I misjudged you, Haku.\n |
| 0xada33 | 33 | Your selflessness is commendable. |
| 0xada55 | 7 | Hurk... |
| 0xada5d | 44 | Great. If I refuse now, I'll look like the\n |
| 0xada8a | 10 | bad guy... |
| 0xada95 | 48 | Now, if we're using Haku's secret savings, all\n |
| 0xadac6 | 40 | we have to do is FIND someone to hire.\n |
| 0xadaef | 23 | Nekone, do y--{W510}Hm? |
| 0xadb07 | 48 | Kuon turns her gaze to the side. There, in the\n |
| 0xadb38 | 47 | corner, sits Maroro--who'd come in without us\n |
| 0xadb68 | 9 | noticing. |
| 0xadb72 | 46 | What are you doing, Maro? Come over here and\n |
| 0xadba1 | 8 | join us. |
| 0xadbaa | 49 | Oho? Master Haku, how my heart singeth, to hear\n |
| 0xadbdc | 33 | thee call me "Maro!" O, what joy! |
| 0xadbfe | 39 | What's he getting so worked up about?\n |
| 0xadc26 | 23 | It's just a nickname... |
| 0xadc3e | 46 | But lo! Master Haku. Words that speak of thy\n |
| 0xadc6d | 43 | plight have reached mine ears, in assured\n |
| 0xadc99 | 8 | secrecy. |
| 0xadca2 | 30 | Sorry, run that by me again?\n |
| 0xadcc1 | 18 | What did you hear? |
| 0xadcd4 | 43 | Why, Lord Osht--ah, rather, Master Ukon's\n |
| 0xadd00 | 43 | request! The duty milord hath laid at thy\n |
| 0xadd2c | 5 | feet. |
| 0xadd32 | 42 | Oh, right. I forgot Maroro was in on that. |
| 0xadd5d | 47 | Speak now, speak! Art thou perhaps in need of\n |
| 0xadd8d | 48 | counsel? Wisdom? Hold not thy tongue, for Maro\n |
| 0xaddbe | 8 | is here! |
| 0xaddc7 | 26 | *Glance, glance, glance--* |
| 0xadde2 | 49 | What's he looking around all shiftily like that\n |
| 0xade14 | 7 | for...? |
| 0xade1c | 33 | There isn't anything troub--wait. |
| 0xade3e | 41 | We're shorthanded... And Maroro has his\n |
| 0xade68 | 39 | magecraft, on top of being a scholar.\n |
| 0xade90 | 13 | I get it now. |
| 0xade9e | 48 | A talented mage would be quite the acquisition\n |
| 0xadecf | 16 | for our group... |
| 0xadee0 | 10 | Hey, Maro. |
| 0xadeeb | 31 | Wh-What dost thou desire of me? |
| 0xadf0b | 47 | If it's OK with you, would you like to help us? |
| 0xadf3b | 30 | I-In what capacity, pray tell? |
| 0xadf5a | 48 | Well, Ukon asked us to work for him, but we're\n |
| 0xadf8b | 19 | really shorthanded. |
| 0xadf9f | 49 | We're looking for... comrades? At least, that's\n |
| 0xadfd1 | 45 | the word Kuon used. We could use your help,\n |
| 0xadfff | 10 | basically. |
| 0xae00f | 18 | What's the matter? |
| 0xae022 | 9 | Heigh-ho! |
| 0xae02c | 49 | F-F-Forsooth, what choice in the matter have I?\n |
| 0xae05e | 47 | A friend hath need of Maroro's aid, and so he\n |
| 0xae08e | 7 | aideth! |
| 0xae096 | 44 | So be it! Thou mayst leave all in Maroro's\n |
| 0xae0c3 | 14 | capable hands. |
| 0xae0d2 | 11 | Is that so? |
| 0xae0de | 49 | Uh... Um. Not to rain on anyone's parade, but I\n |
| 0xae110 | 36 | don't think we can have you do that. |
| 0xae135 | 7 | ...Huh? |
| 0xae13d | 44 | Wh-Wherefore dost thou speak such cruelties? |
| 0xae16a | 43 | I fear we cannot have you as our comrade,\n |
| 0xae196 | 7 | Maroro. |
| 0xae19e | 25 | D-Dost thou revile me so? |
| 0xae1b8 | 47 | M-Mistress Nekone? Pray hold thine silence no\n |
| 0xae1e8 | 6 | more-- |
| 0xae1ef | 50 | It's because you're an imperial scholar, Maroro.\n |
| 0xae222 | 38 | That's why we can't bring you onboard. |
| 0xae249 | 44 | Mine erudition is to blame? What piffle is\n |
| 0xae276 | 45 | this? A scholar doth make for a fine asset,\n |
| 0xae2a4 | 7 | surely. |
| 0xae2ac | 23 | And that's exactly why. |
| 0xae2c4 | 45 | If we took you in, we'd have to pay you for\n |
| 0xae2f2 | 30 | the services you'd provide us. |
| 0xae311 | 47 | Being an imperial scholar, your commission is\n |
| 0xae341 | 48 | just too high. Far outside our available budget. |
| 0xae372 | 31 | What? He gets paid that highly? |
| 0xae392 | 8 | B-But... |
| 0xae39b | 47 | I-I see. Mayhaps thou couldst take me as... a\n |
| 0xae3cb | 20 | friend? Naught more? |
| 0xae3e0 | 47 | Verily, a rate of recompense rightly reduce'd\n |
| 0xae410 | 47 | is no sticking point for service unto a friend. |
| 0xae440 | 28 | ...We can't do that, either. |
| 0xae45d | 7 | Zounds! |
| 0xae465 | 46 | It would be all kinds of messy if we reduced\n |
| 0xae494 | 36 | your pay on the basis of friendship. |
| 0xae4b9 | 50 | And if we lower a scholar's wages, then everyone\n |
| 0xae4ec | 48 | else's would need to be slashed to be fair, too. |
| 0xae51d | 17 | Urk. That... I... |
| 0xae52f | 46 | What then of milady Nekone, milady Rulutieh?\n |
| 0xae55e | 47 | A scholar of philosophy, surely, doth command\n |
| 0xae58e | 12 | far more a-- |
| 0xae59b | 40 | I, ah... I'm j-just here to learn, so... |
| 0xae5c4 | 24 | ...I am also a student.  |
| 0xae5dd | 12 | What's this? |
| 0xae5ea | 49 | I am still a student, not yet a proper scholar.\n |
| 0xae61c | 43 | Your insinuations scathe me, o great sage\n |
| 0xae648 | 48 | Gah! No, prithee--I meant naught in the way of\n |
| 0xae679 | 17 | offense, milady-- |
| 0xae68b | 39 | Well, Nekone and Rulutieh are here as\n |
| 0xae6b3 | 24 | assistants, in any case. |
| 0xae6cc | 48 | It'd be great to have someone with your skills\n |
| 0xae6fd | 48 | along, but paying you fairly is prohibitive at\n |
| 0xae72e | 5 | best. |
| 0xae734 | 8 | Alack... |
| 0xae73d | 33 | Maroro withers in disappointment. |
| 0xae75f | 26 | We can't have Maro, huh?\n |
| 0xae77a | 17 | That's a shame... |
| 0xae78c | 48 | ...Which means our problem of the day is still\n |
| 0xae7bd | 40 | finding potential hirees, and doing so\n |
| 0xae7e6 | 11 | discreetly. |
| 0xae7f2 | 45 | That's about the shape of it. Nothing to do\n |
| 0xae820 | 47 | but keep an eye out for good candidates for a\n |
| 0xae850 | 6 | while. |
| 0xae857 | 48 | Calling this a rocky start would be putting it\n |
| 0xae888 | 9 | mildly... |
| 0xaf79b | 50 | Lying alone in my room, I let my thoughts swirl... |
| 0xaf7ce | 16 | The "face," huh. |
| 0xaf7df | 47 | Everyone around me seems oddly excited by the\n |
| 0xaf80f | 45 | prospect, but I can't imagine it's gonna be\n |
| 0xaf83d | 5 | easy. |
| 0xaf843 | 50 | Doubt I'll even be able to string twenty minutes\n |
| 0xaf876 | 25 | together for a good rest. |
| 0xaf894 | 45 | So I should sleep now while I can, naturally. |
| 0xaf8c2 | 46 | And of course, the door chooses that precise\n |
| 0xaf8f1 | 30 | moment to open and admit Kuon. |
| 0xaf910 | 12 | Here you go. |
| 0xaf91d | 42 | Kuon drops a bundle of papers into my lap. |
| 0xaf948 | 12 | What's this? |
| 0xaf955 | 43 | From the look of it... They seem to be...\n |
| 0xaf981 | 19 | books of some sort? |
| 0xaf995 | 8 | Open it. |
| 0xaf99e | 47 | I flip the cover of the top one, and an array\n |
| 0xaf9ce | 48 | of unfamiliar letters and characters greets my\n |
| 0xaf9ff | 5 | eyes. |
| 0xafa05 | 17 | ...I was napping. |
| 0xafa17 | 48 | It's an embarrassment to our group if our face\n |
| 0xafa48 | 26 | can't read or write, Haku. |
| 0xafa63 | 7 | Nrgh... |
| 0xafa6b | 20 | Just try to read it. |
| 0xafa80 | 35 | Even if you command me like that... |
| 0xafaa4 | 46 | It's not like I'm gonna be able to make head\n |
| 0xafad3 | 37 | or tail of this at the drop of a hat. |
| 0xafaf9 | 49 | Besides, this looks way too hard for beginners.\n |
| 0xafb2b | 44 | Don't you have anything like a picture book? |
| 0xafb58 | 47 | If it's difficult, then that makes it perfect\n |
| 0xafb88 | 13 | for learning. |
| 0xafb96 | 41 | Kuon begins to read from the page slowly. |
| 0xafbc0 | 42 | "He, is, al, ways, talk, ing, non, sense." |
| 0xafbeb | 30 | Come on, try reading after me. |
| 0xafc0a | 25 | He... is... al... ways... |
| 0xafc24 | 43 | Reluctantly, I track the letters after her. |
| 0xafc50 | 31 | Talk... ing... nonsense. There. |
| 0xafc70 | 13 | Is that good? |
| 0xafc7e | 39 | For now. C'mon, let's do the next line. |
| 0xafca6 | 31 | "The king said to his servant." |
| 0xafcc6 | 45 | The... king... said to... his... ser... vant. |
| 0xafcf4 | 44 | See, there you go. You're doing it properly. |
| 0xafd21 | 39 | Just parsing the letters takes all my\n |
| 0xafd49 | 24 | concentration, though... |
| 0xafd62 | 47 | Even so, I find myself getting adjusted to it\n |
| 0xafd92 | 40 | strangely fast as I continue to read on. |
| 0xafdbb | 49 | I've never actually hated reading. Fortunately,\n |
| 0xafded | 47 | the letters aren't complex, and the words are\n |
| 0xafe1d | 40 | "The king said, 'I am cold and hungry.'" |
| 0xafe46 | 46 | The king... said. I am... cold. And... hungry. |
| 0xafe75 | 33 | Hey, try reading this one for me? |
| 0xafe97 | 46 | Saying that, she indicates a particular line\n |
| 0xafec6 | 44 | with her finger, but doesn't read it aloud\n |
| 0xafef3 | 8 | herself. |
| 0xafefc | 49 | Doubting that I'm not just repeating her words,\n |
| 0xaff2e | 7 | huh...? |
| 0xaff36 | 45 | Uh... "Is there... some... thing... warm...\n |
| 0xaff64 | 32 | and deli... cious... somewhere?" |
| 0xaff85 | 32 | ...I didn't get it wrong, did I? |
| 0xaffa6 | 40 | You really COULD read it on your own...! |
| 0xaffcf | 29 | Can you not sound so shocked? |
| 0xaffed | 39 | Here, here, try reading from this part! |
| 0xb0015 | 30 | You want me to read all that!? |
| 0xb0034 | 48 | You can skip over the bits you don't understand. |
| 0xb0065 | 48 | With Kuon forcing the book back into my hands,\n |
| 0xb0096 | 39 | I reluctantly pick up where I left off. |
| 0xb00be | 50 | "There's... a... most... wonder... ful... smell,\n |
| 0xb00f1 | 47 | coming... from... in here. Servant... what is\n |
| 0xb0121 | 6 | that?" |
| 0xb0128 | 45 | "The ser... vant... said, that... is not...\n |
| 0xb0156 | 17 | the king's food." |
| 0xb0168 | 48 | Haltingly and erratically, I manage to stumble\n |
| 0xb0199 | 44 | through it, Kuon stifling a smirk behind me. |
| 0xb01c6 | 30 | ...What, is this funny to you? |
| 0xb01e5 | 44 | Just parsing each line letter-by-letter is\n |
| 0xb0212 | 43 | taking all my attention. I can't actually\n |
| 0xb023e | 17 | follow the story. |
| 0xb0250 | 36 | Is all literature here like this...? |
| 0xb0275 | 44 | It seems like a narrative of some kind...?\n |
| 0xb02a2 | 31 | Like a fable, but more refined. |
| 0xb02c2 | 45 | I get the feeling I've read stuff like this\n |
| 0xb02f0 | 7 | before. |
| 0xb02f8 | 32 | Don't think about it too hard.\n |
| 0xb0319 | 18 | Just keep reading. |
| 0xb032c | 43 | Uh. "What... is... that food, the shop...\n |
| 0xb0358 | 17 | worker... asked." |
| 0xb036a | 7 | "Nyaa." |
| 0xb0372 | 39 | Hey, uh, Kuon? Am I reading this right? |
| 0xb039a | 46 | Mhm. It's right, don't worry. Just keep going. |
| 0xb03c9 | 28 | What does it mean by "nyaa?" |
| 0xb03e6 | 36 | You'll understand as you keep going. |
| 0xb040b | 45 | "...Then... give me... that... nyaa, the...\n |
| 0xb0439 | 27 | shop... worker... replied." |
| 0xb0455 | 47 | "All... right... one negima, with... pleasure." |
| 0xb0485 | 9 | Pfffhaha. |
| 0xb048f | 47 | ...Yeah, I'm not sure if I get the punchline,\n |
| 0xb04bf | 5 | here. |
| 0xb04c5 | 42 | Don't worry about that. Just keep reading. |
| 0xb04f0 | 47 | Like, what's up with the negima? Why did that\n |
| 0xb0520 | 47 | come up all of a sudden? Where did the nyaa go? |
| 0xb0550 | 37 | I said don't worry about it! Come on. |
| 0xb0576 | 50 | I genuinely can't tell if this is actually meant\n |
| 0xb05a9 | 45 | to be funny, or if she's just laughing at me. |
| 0xb05d7 | 45 | I push forward disconsolately, beginning to\n |
| 0xb0605 | 41 | run into wording that's... difficult to\n |
| 0xb062f | 10 | interpret. |
| 0xb063a | 47 | "This... is not... a nyaa. This... is... a...\n |
| 0xb066a | 7 | chyuu?" |
| 0xb0672 | 47 | "What... the king... wants... to eat... is...\n |
| 0xb06a2 | 20 | nyaa... the calico." |
| 0xb06b7 | 10 | Ahahahaha! |
| 0xb06c2 | 45 | Come on, now. This is just weird, no matter\n |
| 0xb06f0 | 17 | how you slice it. |
| 0xb0702 | 33 | No, it's not weird at all, not... |
| 0xb0724 | 10 | ...Pfffft. |
| 0xb072f | 12 | Ahahahaha... |
| 0xb073c | 35 | Kuon dissolves into a laughing fit. |
| 0xb0760 | 34 | What kind of book is this, anyway? |
| 0xb0783 | 43 | Ah... Ahem. It's writing passed down from\n |
| 0xb07af | 45 | ancient times, but no one can agree on what\n |
| 0xb07dd | 9 | it means. |
| 0xb07e7 | 43 | Don't make a beginner read something that\n |
| 0xb0813 | 23 | difficult straight off! |
| 0xb082b | 42 | But you ARE able to read it, aren't you?\n |
| 0xb0856 | 13 | So it's fine. |
| 0xb0864 | 45 | But that's beside the point. I think you'll\n |
| 0xb0892 | 45 | understand it a bit more once you reach the\n |
| 0xb08c0 | 4 | end. |
| 0xb08c5 | 24 | Uh huh. If you say so... |
| 0xb08de | 38 | "Bring... the barrel... of soy sauce." |
| 0xb0905 | 35 | "Every... one... else... is ready." |
| 0xb0929 | 8 | The end. |
| 0xb0932 | 46 | ...That's, uh, really it? That's all there is? |
| 0xb0961 | 27 | Ahh, that was really funny. |
| 0xb097d | 47 | That didn't make a lick of sense, all the way\n |
| 0xb09ad | 19 | through to the end! |
| 0xb09c1 | 40 | And somehow Kuon found the whole thing\n |
| 0xb09ea | 10 | hilarious. |
| 0xb09f5 | 47 | I'm not feeling too satisfied with any of this. |
| 0xb0a25 | 47 | Even if you don't understand the meaning, the\n |
| 0xb0a55 | 48 | sounds are funny. Too early in the morning for\n |
| 0xb0a86 | 4 | you? |
| 0xb0a8b | 48 | It's not a matter of whether it's early or late. |
| 0xb0abc | 23 | Now, which one next...? |
| 0xb0ad4 | 23 | We're still doing this? |
| 0xb0aec | 42 | We'll be practicing every day from now on. |
| 0xb0b17 | 49 | Without hesitation, Kuon begins picking through\n |
| 0xb0b49 | 39 | the pile for another book to read from. |
| 0xb0b71 | 20 | Practice, practice~! |
| 0xb0b86 | 10 | Hey, Kuon? |
| 0xb0b91 | 43 | You're just doing this for a giggle at my\n |
| 0xb0bbd | 20 | expense, aren't you? |
| 0xb0bd2 | 29 | Why, whatever could you mean? |

## 8. Formato de saida EXIGIDO
Escreva `translations_15_02.json` com a forma:
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
