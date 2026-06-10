# Decision Log — Utawarerumono: Mask of Deception

Registro acumulativo de decisões não-óbvias. Nunca apagar entradas (ver `framework/skills/04b_decision_log.md`).

---

## Deep pass do arco (Carta exercida) + custo de produção medido

**Data:** 2026-06-08
**Passo do SDD:** 05/06b/07
**Tipo:** revision

**Decisão tomada:**
Exercer a Carta de Governança **de verdade** no arco (1025 linhas) e medir custo, para de-riscar a
meia-maratona. Entregas: `back_translation_log.json`, `qa_report.md`, `cost_report.md` + `cost_model.py`.

**Back-translation (a verificação que nunca rodara):** 9 linhas high revisadas → **2 fixes reais**:
- `0x3b3b` "make it for you" (dúbio: fazer / conseguir) → "não vou mais **poder** fazer isso por você" (restaura inabilidade/despedida).
- `0x3ac3` "waiting for you" → "te **aguarda**" (voz profética do Homem, não casual).
As outras 7 preservavam ambiguidade/tom.

**Voz:** spot-check de 3 vozes (Kuon fofa↔firme, Homem tenso, Protagonista fragmentado) → consistente,
sem drift no sample. **Risco cognitivo:** +4 reveals de identidade/lore (Kuon/Haku/Tatari) elevados a
medium (os sinais de dados não pegam, pois o nome é a forma canônica).

**Processo funcionando:** o `validate.py` pegou um erro de token (`\n` dropado) numa revisão minha
durante o deep pass — corrigido antes de gravar. É a camada de validação fazendo o trabalho dela.

**Custo de produção (medido, não da sessão):** `cost_model.py` estima $/1k linhas **3.12 (forte) →
1.75 (model-mix + caching)**; projeção ~33k: **$103 → $58 (−44%)**. Tokens ≈chars/3.8 (refinar com
`count_tokens`); é ordem de grandeza + deltas de cenário, não centavos.

**Limitação assumida:** o `tone_register` fino por situação das ~948 linhas `dialogo` segue defaultado —
re-tag completo é o passe contextual da meia-maratona (este deep pass priorizou alto risco + voz).

**Revisão necessária:** não para o método. O re-tag situacional completo entra na run de escala.

## Opcode de RÓTULO DE FALANTE `53 00` + reconcile de speaker (data-driven)

**Data:** 2026-06-08
**Passo do SDD:** 08 / 05
**Tipo:** revision (corrige bug do conector + atribuição de speaker)

**Problema:** in-game, o rótulo de falante aparecia em **inglês** ("Girl") mesmo com a tradução
("Garota") aprovada e gravada. RE: o nome do falante usa um **2º opcode de ponteiro, `53 00`** (mesmo
formato file-relativo do `50 00` de diálogo), que o conector ignorava. Resultado: "Girl"→"Garota"
(estoura 4→6 bytes) era varrida pra um run `50 00` na relocação, e os ~17 sites `53 00` do rótulo
seguiam apontando pro "Girl" original. Há 5 rótulos no corpus (`Girl`×3, `Woman`, `Man`).

**Decisão:**
1. `sdat_format.POINTER_OPCODES = (50 00, 53 00)` — `index_pointers` indexa AMBOS; `is_head`/`read_run`
   tratam rótulos como heads próprios; a relocação reescreve TODOS os sites do head (o valor é o mesmo
   offset file-relativo; o byte do opcode não muda). Verificado: 17/17 sites do "Girl" passam a ler
   "Garota" dentro do arquivo; round-trip segue byte-idêntico. (Travado por `test_label_pointers_53`.)
2. **Reconcile de speaker (data-driven):** o falante de cada fala = rótulo do `53 00` mais próximo
   antes do seu `50 00`. Derivando do binário, **10 linhas** taguadas como adultos da memória
   ("Mulher/Homem (memória)") são na verdade rotuladas **"Girl"** pelo jogo → reconciliadas para
   **"Garota (memória)"**. (As 7 "Woman" e 4 "Man" estavam corretas.)

**Por que "Garota (memória)" e não "Kuon":** a identidade da figura da memória é **gap de pesquisa**
(`research_log.md`) — a Carta de Governança proíbe afirmar lore incerto. Logo, taguamos pelo **rótulo
do jogo** (faithful), sem reivindicar que a garota da memória é a Kuon.

**Revisão necessária:** sim — **gate in-game**: confirmar que o rótulo exibe "Garota" (era "Girl").
Se a identidade da memória for confirmada na pesquisa, reavaliar o canônico.

---

## Calibração de risco/metadados (F2) — data-driven, sem achatamento

**Data:** 2026-06-08
**Passo do SDD:** 05/06
**Tipo:** revision

**Decisão tomada:**
Calibrar o `risk_level` do `translation_plan.json` por **sinais de dados** (não auto-default), só
**subindo** o risco e exigindo `risk_notes`:
- `spoiler_flags` não-vazio → **high**.
- `glossary_flags` não-vazio **ou** `entities_present` ∩ (termos do glossário com `spoiler_level≠none`)
  → **medium**.
- `tone_register`: `dialogo`→`interjeicao` nos offsets de interjeição; sistema→`frio_tecnico`.

**Resultado:** risco saiu de **0 high / 13 medium (achatado)** para **9 high / 9 medium**; 13 linhas
re-tagueadas como interjeição. `base_translation` intacto (metadata-only). Invariante: toda linha
`risk≥medium` tem `risk_notes`.

**Limitação assumida (deferido):** o `tone_register` fino por **situação/emoção** das ~948 linhas
`dialogo` **não** foi mapeado aqui — isso exige a leitura contextual por personagem (passe LLM da
meia-maratona). A calibração atual é o piso determinístico que dispara a back-translation nas linhas
certas; o refino situacional vem com a run de escala.

**Impacto:** a QA (06b/07) agora tem alvos reais de alto risco; a Carta de Governança (backlog) usará
esses campos. **Revisão necessária:** refino situacional no passe contextual de escala.

## space_strategy — in_place → repoint

**Data:** POC
**Passo do SDD:** 00 / 08
**Tipo:** revision

**Decisão tomada:**
Mudar `connector.space_strategy` de `in_place` para `repoint`.

**Alternativas consideradas:**
- Manter `in_place` — rejeitada: só 12/20 (60%) das traduções cabem no `byte_budget` original.
- Abreviar tudo para caber in_place — rejeitada: degrada qualidade/tom de quase metade das linhas.

**Razão da decisão final:**
pt-BR é mais longo que o inglês e seus acentos custam 2 bytes em UTF-8. Medição real da POC:
8/20 linhas estouram o orçamento de bytes. `repoint` (recalcular ponteiros) é o caminho viável.

**Impacto:**
Reinserção (Passo 08). Repoint completo exige mapear a tabela de ponteiros do `.sdat` (próximo passo).
A POC gravou apenas as 12 que cabem in_place como prova de conceito.

**Revisão necessária:** sim — implementar repoint real (pointer table) antes de traduzir o corpus completo.

---

## Gate de charset pt-BR — método e veredito

**Data:** POC
**Passo do SDD:** 00
**Tipo:** external

**Decisão tomada:**
Marcar `target_charset_supported: likely` e exigir confirmação in-game antes de produção.

**Alternativas consideradas:**
- Confirmar por presença no texto-fonte — **insuficiente**: o fonte é inglês e quase não usa acentos
  (só `õ` e `À` aparecem em texto real).
- Parsear o `Font.fnt` por suposição de layout (uint16 LE) — resultado inconsistente, não confiável.

**Razão da decisão final:**
`õ` (U+00F5) e `À` (U+00C0) já são renderizados pelo jogo; ambos do bloco Latin-1 Supplement, onde
vivem TODOS os acentos pt-BR. Suporte é altamente provável, mas não confirmado glifo-a-glifo.

**Impacto:**
Tradução pt-BR (acentos). Se algum glifo faltar, precisa expandir a fonte ou transliterar.

**Revisão necessária:** sim — teste in-game com pangrama pt-BR (`áéíóú âêô ãõ ç ÁÉÍ ÃÕ Ç`) ou parse correto do `Font.fnt`.

---

## Anomalia 0x33f9 — texto PT/EN corrompido na fonte

**Data:** POC
**Passo do SDD:** 00
**Tipo:** formatting

**Decisão tomada:**
Marcar a linha `0x33f9` como anomalia de fonte (não traduzir em cima do lixo; tratar como linha de sistema reescrita).

**Razão:**
A string original já vem misturada PT/EN e truncada ("...SISTEMAS AM . RESTARTING...") no próprio jogo.
Não é erro de extração. O conector deve sinalizar esse tipo de anomalia no `extraction_log.md`.

**Impacto:** linha 0x33f9. **Revisão necessária:** não (tratada como sistema na POC).

---

## Modelo de execução da tradução — arquivo aprovado + script

**Data:** POC (revisão de governança)
**Passo do SDD:** 06 / 08
**Tipo:** revision

**Decisão tomada:**
A IA **não escreve a tradução à mão** nos dados. Ela propõe no `translation_plan.json`
(`base_translation`); após aprovação, o conjunto vai para `approved_translations.csv`
(`offset`, `text_target`); o script `reinsert.py` aplica esse arquivo ao binário.

**Alternativas consideradas:**
- IA preenchendo `text_target` no `translated.csv` (source+target juntos) — rejeitada: mistura
  proposta com aplicação e arrisca contaminar o source.

**Razão da decisão final:**
Separar cognição (propor) → aprovação (usuário) → aplicação (script determinístico). O `translated.csv`
escrito à mão foi depreciado.

**Impacto:** Passos 06/08, schema dos artefatos, scripts da instância.
**Revisão necessária:** não.

---

## Saída em output/ + governança de scripts

**Data:** POC (revisão de governança)
**Passo do SDD:** 08
**Tipo:** formatting

**Decisão tomada:**
A saída final vai para `output/ScriptEvent.sdat` (mesmo nome e extensão do input), substituindo
`artifacts/build/`. Os scripts do conector são **executados, não refeitos**; criar script novo só com permissão.

**Impacto:** localização da entrega; fluxo de trabalho da IA.
**Revisão necessária:** não.

---

## Ordem de offset ≠ ordem de exibição

**Data:** POC
**Passo do SDD:** 00
**Tipo:** revision

**Decisão tomada:**
Usar ordem por offset como aproximação da ordem narrativa na POC.

**Razão:**
A ordem real de exibição é controlada pelo script (ponteiros). Interpretar o script é mais custoso e
fica como próximo passo; para a cena de abertura, a ordem por offset coincide com a narrativa.

**Impacto:** sequência das linhas. **Revisão necessária:** sim, se a continuidade/contexto exigir ordem exata.

---

## Repoint real implementado — relocação por run

**Data:** 2026-06-07
**Passo do SDD:** 08
**Tipo:** revision (resolve o "Revisão necessária" de `space_strategy — in_place → repoint`)

**Decisão tomada:**
Implementar repoint no `reinsert.py` por **relocação de run**. Formato descoberto (ver
`connector/table_schema.md`): não há tabela central de ponteiros; cada fala ("head") é referenciada
inline pelo opcode `50 00` + ponteiro absoluto uint32 LE. Strings sem ponteiro próprio
("continuações") são lidas em sequência após o head. Um **run** = head + continuações.

Quando qualquer membro de um run estoura o `byte_budget`, o run inteiro é **anexado ao fim do
arquivo** e **todos** os ponteiros `50 00`+ptr do head são reescritos para o novo endereço. As
continuações viajam contíguas → a semântica sequencial é preservada.

**Alternativas consideradas:**
- Reescrever ponteiros pelo valor uint32 cru — rejeitada: gera falsos-positivos (4 bytes que casam
  por acaso). O filtro `50 00`+ptr elimina isso.
- Relocar string isolada (não o run) — rejeitada: quebraria continuações sem ponteiro próprio
  (ex.: `0x35bf`, continuação de `0x35ad`).

**Razão da decisão final:**
Determinístico, sem LLM, e robusto contra falsos-positivos e continuações. Validado na POC.

**Impacto / resultado (POC 20 linhas, pós-transliteração):**
T1 in_place = 12; repoint = 8 strings (7 runs); **resíduo T4 = 0**. Round-trip self-test
byte-idêntico. Patch IPS gerado (arquivo cresce ~280 bytes). Verificação independente: todos os
ponteiros reescritos leem a string esperada; continuação `0x35bf` segue o head `0x35ad` no novo
endereço.

**Revisão necessária:** não para o mecanismo. Confirmar in-game que strings relocadas (apêndice ao
fim do arquivo) exibem corretamente, antes da run completa das 33k.

---

## Charset — transliteração na gravação (gate FALHOU)

**Data:** 2026-06-07
**Passo do SDD:** 00 / 08
**Tipo:** external (supersede a decisão "Gate de charset pt-BR — método e veredito")

**Decisão tomada:**
Marcar `target_charset_supported: false` e **transliterar** (acento → ASCII) na gravação do binário.
A tradução canônica (`approved_translations.csv`, `translation_plan.json`) **mantém os acentos**
(correta para QA/revisão); apenas os bytes escritos no jogo são dobrados para ASCII
(NFKD + descarte de combining marks; `ç→c`), implementado em `reinsert.py`.

**Razão da decisão final:**
O teste in-game com pangrama pt-BR (`áéíóú âêô ãõ ç ÁÉÍ ÃÕ`) renderizou os acentos como `@`
(evidência: `artifacts/char1.png`, `artifacts/char2.png`). A fonte do jogo não possui os glifos.

**Alternativas consideradas:**
- Expandir a fonte (atlas + mapa de chars) — rejeitada nesta fase: esforço alto (asset não está no
  repo); fica como melhoria futura de qualidade.
- Remapear glifos não usados — rejeitada: depende de slots livres; mais frágil.

**Impacto:** ortografia degradada (sem acentos) no texto exibido, porém 100% legível e funcional.
**Efeito colateral positivo:** acento (2 bytes UTF-8) → ASCII (1 byte) reduz o estouro de byte_budget.
**Revisão necessária:** não (decisão do usuário). Reavaliar se um dia a fonte for expandida.

---

## Container ScriptEvent.sdat — formato totalmente mapeado + extração por script

**Data:** 2026-06-08
**Passo do SDD:** 00
**Tipo:** revision

**Decisão tomada:**
Mapear o índice do container e extrair o corpus **por script** (não mais varredura sequencial cega de
N linhas). Formato (ver `connector/sdat_format.py`):
- Header `Filename    ` + tabela de nomes (registros de 15 bytes `CC_SS_NNNT.BIN`).
- Seção `Pack        ` + `count` + `count`×(offset, size) — **par interleaved**, offsets contíguos do
  início ao fim do arquivo. 353 scripts, capítulos 11–39.
- Cada script = `[bytecode 'STSC' + opcodes][bloco de texto: strings UTF-8 null-terminated]`. O bloco
  de texto de cada script está em **ordem de armazenamento = ordem narrativa** (verificado na abertura).

**Razão:** permite escolher um **arco real** (ex.: cena `11_01_000S`) com fronteiras de verdade, em vez
de "as N primeiras linhas". Resolve em parte o "Revisão necessária" de *Ordem de offset ≠ ordem de
exibição*: a extração agora segue a ordem de armazenamento por script (≡ narrativa na abertura).

**Impacto:** `extract.py` extrai por prefixo de nome de script (`SCENES`); `sdat_format.py` é o módulo
único de formato (compartilhado por extract+reinsert → garante o round-trip).

**Revisão necessária:** sim — para cenas longe da abertura, validar que ordem de armazenamento ainda
acompanha a narrativa (senão, caminhar o bytecode por ordem de comando).

---

## Anomalia 0x33f9 — reclassificada (binário-fonte está íntegro)

**Data:** 2026-06-08
**Passo do SDD:** 00
**Tipo:** revision (revisa "Anomalia 0x33f9 — texto PT/EN corrompido na fonte")

**Decisão tomada:**
Reclassificar: o binário-fonte **não está corrompido**. A extração limpa do arco mostra em `0x33f9`
o texto inglês íntegro **"INITIALIZING AWAKENING PROCESS."** (31 bytes) e, separada, `0x3419`
**"SYSTEMS YELLOW. RESTARTING IN 5 SECONDS."** (40 bytes).

**Razão:** o "texto PT/EN misturado/truncado" registrado antes era artefato de uma extração anterior
sobre um `.sdat` **já modificado** pela própria POC (uma linha de 72 bytes que abarcava as duas strings
através do `\0`). Com a extração por bloco de texto do script, as duas strings aparecem corretas.

**Impacto:** nenhuma linha precisa ser tratada como "lixo de sistema"; traduzir normalmente.
**Revisão necessária:** não.

---

## Escopo do teste cognitivo — 20 linhas soltas → arco 11_01_000S (75 linhas)

**Data:** 2026-06-08
**Passo do SDD:** 00–07
**Tipo:** revision

**Decisão tomada:**
Trocar o corpus de teste das "20 primeiras linhas" para o **1º script do 1º arco** (`11_01_000S`,
75 linhas) — cena de abertura completa e autocontida (despertar → Kuon → sonho/memória → promessa).

**Razão:** rodar o pipeline cognitivo (01→07) de verdade num arco coerente, não em linhas avulsas.
Tamanhos reais medidos: cena 11_01 inteira ≈470 linhas; 11_02 ≈557; 11_03 ≈119 — grandes demais para
um ciclo manual. `11_01_000S` (75 linhas, verificado limpo) equilibra realismo e esforço.

**Impacto:** `dialogs.csv`, `translation_plan.json`, `entities.csv` etc. regenerados para este arco.
**Revisão necessária:** não; estender para 11_01_100C/150S e 11_02/11_03 em rodadas futuras.

---

## Repoint em escala — bug do MAX_RUN + órfãos de início de bloco + otimização O(1)

**Data:** 2026-06-08
**Passo do SDD:** 08
**Tipo:** revision (corrige o repoint para o corpus de 2 cenas, 1025 linhas)

**Decisão tomada:**
Ao rodar a reinserção em escala (1025 linhas), o repoint **falhou parcialmente** (127 resíduos T4).
Correções:
1. **Run completo:** `MAX_RUN=32` truncava runs longos de narração (1 head + dezenas de continuações),
   orfanando linhas — e relocar um run truncado **corromperia** a exibição. Elevado para capturar o run
   inteiro (term. por próximo head / fim de bloco). Resíduo caiu 127 → 9.
2. **Head-finding pelo binário:** a busca do head passou a caminhar **pelas strings reais do binário**
   (não só pelos offsets do `dialogs.csv`), pois o head de uma continuação pode não ser uma linha extraída.
3. **Índice de ponteiros O(1)** (`sdat_format.index_pointers`): uma varredura mapeia `target→[sites]`;
   `is_head`/`find_pointers`/`read_run` usam o índice. Tempo da reinserção caiu de **~80s → ~0.5s**.
4. **Órfãos de início de bloco (9):** a 1ª string de cada bloco de texto **não tem ponteiro `50 00`**
   (não repointável). Quando estouram, foram **encurtadas para caber in_place**. Resíduo final = **0**.

**Alternativas consideradas:**
- Deixar resíduo>0 e resolver via T4 (LLM em lote) — **adiado** pelo usuário; e o resíduo aqui é por
  falta de ponteiro, não por overflow irredutível.

**Impacto:** `sdat_format.py` (run completo, índice), `reinsert.py` (head-finding pelo binário, índice).
**Revisão necessária:** sim — mapear o **opcode de exibição da 1ª string de bloco** (hoje sem `50 00`)
para torná-las repointáveis em vez de exigir fit in_place.

---

## Escopo cognitivo — 75 → 1025 linhas (cenas 11_01 + 11_02); reveal de Haku in-corpus

**Data:** 2026-06-08
**Passo do SDD:** 00–08
**Tipo:** revision

**Decisão tomada:**
Re-rodar o pipeline completo em escala (cenas 11_01 + 11_02 = 1025 linhas). Novos termos canônicos:
**Kuon** (nome revelado em 0x108db), **Haku** (nome dado ao protagonista em 0x12668 — reveal
agora **dentro do corpus**), **Tatari** (criatura imortal), **aperyu** (vestimenta), **Utawarerumono**
(origem do nome; título), **Kujyuri**/**Província de Shishiri** (topônimos). Todos `manter_original`.

**Governança:** as traduções foram autoradas via geradores transientes (`_build_plan*.py`) e então
**removidas** — nenhum texto da obra permanece em `.py`; a fonte de verdade é `translation_plan.json`.
Metadados por linha: curados em 11_01_000S; auto-defaultados (speaker heurístico, risk low) nas demais.

**Impacto:** todos os artefatos regenerados; `test_roundtrip.py` (pytest) trava a regressão (4 verdes).
**Revisão necessária:** não para este escopo. T4-LLM e mapeamento do opcode de início de bloco ficam pendentes.

---

## CORREÇÃO CRÍTICA — ponteiros são FILE-RELATIVOS, não absolutos

**Data:** 2026-06-08
**Passo do SDD:** 08
**Tipo:** revision (corrige o modelo de ponteiro do conector — superseda a SEÇÃO 4 anterior)

**Decisão tomada:**
Ao investigar o "opcode de início de bloco", descobri que **`50 00`+uint32 é um offset RELATIVO ao
início do arquivo (Pack)**, não absoluto. Endereço da string = `file_start_do_site + uint32`. Prova:
dos ~47k sites, **42.101** só apontam para string como file-relativos vs **63** como absolutos.

**O que estava errado:**
- `find_pointers`/`index_pointers`/`reinsert` tratavam o uint32 como **absoluto**. O repoint gravava
  valores absolutos → **o jogo leria `file_start + valor` e cairia no lugar errado** (texto relocado
  quebraria in-game). Os testes passavam por **autoconsistência** (mesma lógica errada nos 2 lados).
- As "9 órfãs de início de bloco" eram, na verdade, os **ponteiros de entrada** (`50 00`+rel32) que o
  matcher absoluto não via. Com o modelo correto, viram heads normais → **repointáveis** (a gambiarra
  in_place foi revertida; traduções completas restauradas).

**Correção:**
1. `sdat_format.index_pointers(data, files)` → `target_abs = file_start + uint32`; `find_pointers`
   devolve `(site, file_start)`; `is_head`/`read_run` file-relativos.
2. `reinsert` reescreve o ponteiro como `novo_offset − file_start_do_site`.
3. `test_roundtrip.py`: `test_translated_pointers` agora valida o **valor gravado** (file_start+valor ==
   novo head, não-circular); novo `test_pointer_model_is_file_relative` trava o modelo.

**Resultado:** aplicação das 1025 linhas → T1=595, REPOINT_head=425, REPOINT_cont=5, **resíduo T4=0**
(sem in_place forçado). `REPOINT_cont` despencou de 811→5: quase toda linha tem seu próprio ponteiro
(o modelo absoluto as via como continuações órfãs). **6 testes verdes.**

**Insight de processo:** verificação por ponteiro que reusa a mesma leitura dos dois lados é
**circular** — passou com o modelo errado. O teste foi corrigido para validar contra o modelo do engine
(file_start + valor), e um teste de modelo separado prova file-relativo vs absoluto.

**Revisão necessária:** sim — **gate in-game**: confirmar que strings relocadas ao fim do arquivo
(offset file-relativo grande) exibem; se o engine limitar ao `size` do Pack, usar Plano B (relocar
dentro do arquivo + reescrever a tabela Pack).

---

## GATE IN-GAME — EOF-append REPROVADO; adotar relocação intra-arquivo (Plano B)

**Data:** 2026-06-08
**Passo do SDD:** 08
**Tipo:** external (resolve o "Revisão necessária" da CORREÇÃO CRÍTICA file-relativo)

**Decisão tomada:**
Abandonar a relocação por **anexo ao fim do container** (EOF-append) e adotar **relocação
intra-arquivo + reescrita da tabela Pack** (Plano B): o run que estoura é anexado ao **fim da região
do próprio arquivo**, o arquivo **cresce**, e a tabela Pack (offset/size) é **reescrita**
reconstruindo o container. Texto in_place permanece in_place.

**Evidência (teste in-game do usuário — Steam, Mask of Deception, abertura `11_01_000S`):**
Prints `artifacts/Fasea1..11.png`. Padrão, cruzado com `reinsertion_report.md`:

| Linha | Tier no build | Resultado in-game |
|---|---|---|
| `0x33c3` "Q-Quem...", `0x33cd` "...me chama...?", `0x34ea` "5,4,3,2,1...", `0x350f` "TENHA UM BOM DESPERTAR", `0x359d` "On... Onde...?" | **T1_in_place** | **✅ exibe pt-BR** |
| linhas REPOINT → fim do container (`0x31f5xx`) | **REPOINT (EOF-append)** | **❌ `@@@@`; jogo TRAVA (Fasea11)** |

**Prova:** o `.sdat` original tem **`0x31f570` bytes** e os repoints apontam para `0x31f570`+ → o texto
relocado ficou **fora da região declarada do arquivo no Pack**. O engine Aquaplus carrega **cada
arquivo do `.sdat` num buffer próprio** (dimensionado pelo `size` do Pack); um ponteiro file-relativo
só alcança dentro desse buffer. Logo, o problema **não é o modelo de ponteiro** (file-relativo está
certo) nem charset — é o **endereço fora do arquivo**. As linhas que cabem no espaço original (in_place)
exibem 100%.

**Marco do projeto:** primeiro pt-BR do framework **renderizado no jogo real** — prova de ponta a ponta
de que a pipeline SDD → conector → binário funciona em título comercial.

**Alternativas consideradas:**
- EOF-append (anterior) — **rejeitada**: comprovadamente quebra in-game.
- in_place-only (encurtar tudo) — **rejeitada para produção**: em escala, **42% (431/1025)** das linhas
  estouram; forçar in_place truncaria quase metade do texto.
- **Relocação intra-arquivo + rebuild do Pack** — **escolhida**: preserva 100% da qualidade e mantém o
  texto dentro do `size` declarado (o engine lê). Determinístico, sem LLM.

**Validação gate-first:** primeiro um patch com **1 linha** relocada intra-arquivo (modo
`--validate-one`), testado in-game, **antes** da run completa das 1025 linhas.

**Impacto:** `reinsert.py` (remove EOF-append; adiciona relocação intra-arquivo) e `sdat_format.py`
(novo `rebuild_container` que reescreve o Pack). `space_strategy` efetiva: `in_place + reloc_intra_arquivo`.

**✅ GATE APROVADO IN-GAME (2026-06-08):** patch `--validate-one 0x3442` testado no jogo —
"ERRO DE SISTEMA." (a mesma linha que antes virava `@@@@`) **exibiu corretamente** e o jogo
**avançou normalmente** para a cena seguinte (tenda, Kuon), sem travar. Evidência:
`artifacts/testeplanob.png` (linha relocada) e `artifacts/testeplanob_avanco.png` (continuidade).
Conclusão: a relocação INTRA-ARQUIVO + reescrita do Pack é a estratégia correta e está validada
in-game. Liberada a run completa das 1025 linhas. **Revisão necessária:** não.


---

## Calibração: 1 capítulo do zero (11_03_000C, 118 linhas) — modo padrão (2026-06-08)

**Objetivo:** de-riscar a meia-maratona rodando o pipeline completo num capítulo novo e medir ritmo+custo.

**Decisões de tradução não-óbvias:**
- **`toriuma`** (ave-montaria, 1ª menção) → glossário como termo de mundo `manter_original`. Em diálogo
  o EN usa `steed`/`horse` → traduz `montaria`/`cavalo`; o termo de mundo aparece só no rótulo interno.
- **Apelidos cômicos do Haku:** `Ostrich Prime` → `Avestruz Supremo` (mantém a pompa-comica; perde o eco
  pop de "Prime", aceito). Gag do "avestruz" tratado como banal pela Kuon = contraste cômico preservado.
- **Back-translation (catch real):** `common sense draining away` traduzido `indo embora` (achatou a
  imagem) → revisado para **`evaporando`** numa tirada-assinatura do Haku.
- **Interjeições localizadas:** `Geez`→`Aff`, `Huh`→`Hein`, `HOLY--`→`MEU DEU--` (corte seco),
  gagueiras `Wh-/W-/H-/Y-`→`Q-/E-/E-/V-`. Gritos animais `GREHHHH`/`GRRRR` espelhados (universal).

**Pendência sinalizada (não inventada):** rótulos internos `Head` (0x14a7b) e `Head_toriuma` (0x1538c)
→ `needs_human_review`. Reinserem byte-OK verbatim, mas é incerto se o motor os EXIBE como falante;
verificar in-game antes de traduzir. Comportamento conforme a Carta (sinalizar, não improvisar).

**Verificação:** round-trip byte-idêntico; 118/118 linhas conferidas (dirigido por ponteiro, visão do
motor); tiers T1=56/RELOC_head=61/RELOC_cont=1; resíduo T4=0; 0 ponteiro fora-do-arquivo; pytest 29/29.

**Custo medido:** produção API ~**$1,14/1k linhas** (Opus+caching, modo padrão) → meia-maratona ~16k
linhas ≈ **$18** uma vez. Caminho assinatura (o do usuário): sem conta de API; limite é ritmo
(~15–25 janelas, incremental via `translation_status.json`). Ver `ch_11_03/calibration_report.md`.

**Isolamento:** artefatos do 11_03 em `artifacts/ch_11_03/` — não tocam o build principal de 1025.
Fold no build principal (merge approved + estender `SCENES`) fica opcional/quando desejado.
**Revisão necessária:** não (rótulos pendentes de checagem in-game já sinalizados).


---

## Incremento: cap. 11_04 (45 linhas, batalha/tutorial) — modo padrão (2026-06-08)

Cena do tutorial de combate: pose chuuni do Haku, bronca da Kuon, e o gag do "exemplo negativo"
(bicho mole) com **duplo-sentido proposital**.

**Decisões de tradução não-óbvias:**
- **Duplo-sentido preservado num único termo:** `screwing around` → **`sacanagem`** (BR carrega os 2
  sentidos: palhaçada + malícia). O mal-entendido (apresentador ecoa `...Sacanagem?` sem captar a
  malícia) sobrevive 1:1. Cadeia da insinuação: `soft/hard`→`mole/duro`, `throbs`→`pulsa`,
  `expands larger`→`incha cada vez mais` — deniável (descreve o bicho), como no EN.
- **Trocadilho soft:** `Gooshy-soft`→`Mole-gelatina`, `WEAK-soft`→`mole-FRACO`, `wimpy`→`banana`.
- **Chuuni:** `Ultimate justice slash!`→`Corte supremo da justiça!`, `fiend`→`verme`, `Taaake this!`→
  `Tomaaa essa!` (alongamento preservado).
- **Interjeições:** `H-Huh?`→`H-Hein?` (evita `Ha`=riso na transliteração), `Uh`→`Ahn`.

**Descobertas técnicas (importantes pra escala):**
1. **Tokens de cor `{c5}` / `{c-1}`** aparecem em texto de UI (tutorial) e **NÃO estão** no
   `formatting_tokens` do `project.json` (lá só há `{COLOR}`/`{END}` abstratos). Preservados
   **verbatim**. *Pendência de framework:* catalogar/abstrair esses tokens crus.
2. **Linha HEAD-LESS:** a notificação de sistema `0x15d01` **não tem ponteiro `50 00`/`53 00`** — é
   referenciada de outra forma. Logo **não é relocável**: só cabe **in_place**. A tradução estourou
   62 bytes → caiu como **resíduo T4**; reescrita mais curta (drop "foi") p/ caber. Confirma que o
   mecanismo T4 (encurtar o irredutível) é necessário mesmo com o Plano B.

**Verificação:** round-trip byte-idêntico; 45/45 conferidas (file-aware, 6 sub-scripts); tiers
T1=24/RELOC=21; resíduo T4=0; 0 ponteiro fora-do-arquivo; back-translation 12 high → 0 revisão
(duplo-sentido confirmado); naturalness_lint limpo; pytest 29/29.

**Ferramentas genéricas (reúso na meia-maratona):** `connector/build_plan_chapter.py` e
`verify_chapter.py` — parametrizados por `ch_<cena>/`, file-aware, sem work-text. Substituem os
scripts one-off por-capítulo. **Revisão necessária:** não.
