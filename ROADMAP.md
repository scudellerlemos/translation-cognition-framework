# Roadmap — Translation Cognition Framework (SDD)

> Última atualização: 2026-06-13
> Escopo: framework genérico + instância de referência Utawarerumono.
> O roadmap detalhado de decisões vive em `projects/<título>/artifacts/decision_log.md`.

---

## Onde estamos (maturidade)

> Atualizado: 2026-06-15.

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro (~92/100) |
| Perfil de jogos | 🟢 validado |
| Harness de escala (`framework/runtime/`) | 🟢 **em produção** — cena = job stateless O(cena); recuperação por-linha + teto previsível; 122 testes |
| Instância Utawarerumono | 🟢 **JOGO COMPLETO — 16 capítulos, 146 cenas, ~45.100 linhas** traduzidos e verificados (round-trip + back-translation), **validado in-game**; **~$65,9 gastos, $0 desperdiçado** |
| Conector hex_binary | 🟢 formato mapeado; **ponteiros FILE-RELATIVOS**; **relocação INTRA-ARQUIVO + rebuild do Pack** (EOF-append reprovado in-game); **transliteração NFD** (preserva ①②③); **pytest** (16 testes) |
| Perfis filme/série + conector subtitle_file | 🟠/🔴 stub / não iniciado |

**Resumo:** o *processo* está maduro (~92) e a *escala* entregou: o **jogo de referência está 100%
traduzido e verificado ponta-a-ponta** (16 capítulos), com pt-BR renderizando no jogo real. O bloqueador
de correção ("funciona no jogo?") acabou há tempos. O que resta é **pós-produção** (passe global da
Fase 3, build jogável, QA in-game completo do jogo inteiro, release) + **abrangência** (2ª obra/engine,
filmes/séries). Governança com desenhos em [`framework/docs/GOVERNANCE.md`](framework/docs/GOVERNANCE.md).

### Riscos do projeto

Níveis alto / médio / baixo. O que está **sólido** e o que **ainda não está**. (Esta é a fonte única de
riscos do projeto — o README só aponta para cá.)

**🟢 Sólido (provado em produção):** harness stateless (**146 cenas, 16 capítulos = jogo inteiro**) ·
round-trip byte-idêntico in-game · governança propõe→aprova→aplica · **custo previsível** (estimativa
pré-voo + teto duro + recuperação por-linha; `$0` desperdiçado) · **122 testes**.

| Risco | Nível | O que significa | Mitigação / estado |
|---|---|---|---|
| **Validação estreita** | 🔴 Alto | Provado em **1 obra, 1 engine** (`hex_binary`, jogo). Filmes/séries e outros engines são pontos de extensão **não validados** — genérico no papel, não na prática. | Conector é camada isolada; perfis de mídia documentados. |
| **QA humana em escala** | 🔴 Alto | Qualidade *literária* do **jogo inteiro (16 caps)** ainda **não foi lida por humano** — depende de IA + linter + back-translation. O piso de qualidade real está pendente. | `quality_review.py` (XLSX) + TM-coração prontos; falta **executar** a revisão. |
| **Pós-produção (build + release)** | 🟡 Médio *(era Alto; tradução 100% feita)* | A **tradução está completa e verificada** (16 caps), mas **build jogável do jogo inteiro + release não existem** ainda — só patches por capítulo. | Mecânica por-capítulo provada; falta o passe global (Fase 3) + empacotar. |
| **Fechamento global (Fase 3)** | 🟢 Baixo *(fechado 2026-06-15)* | reinsert do **jogo inteiro** rodou byte-perfeito (`reinsert_game`); **consistência de glossário cross-capítulo** agora tem linter determinístico (`glossary_lint`, 96 candidatos de nome próprio). | Passe global provado; linter $0 + revisão humana dos candidatos. |
| **Conector em cenas distantes** | 🟡 Médio | Round-trip + reinsert **verdes em todos os 16 caps** (inclusive 30/39 e os 6 arquivos do `ch_30_09`, que exigiram o fix NFKD→NFD); o **gate visual in-game** dos saltos grandes ainda não foi rodado na tela. | Round-trip garante bytes; falta a conferência visual. |
| **KB sem ratificação humana** | 🟢 Baixo *(resolvido 2026-06-14)* | **55 entidades (caps 12–22) ratificadas** por Felipe Scudeller no `kb_ratified.csv`. `--strict` verde nos caps em uso (15,19,20,21,22). Resíduo: caps 12/13 (entidades antigas pré-gate, sem seção no research_log + ruído) e gênero de 2 menores (Chalafun/Bokoinante, corpus-only) — gate bloqueando **corretamente** até confirmar. | Ratificação feita; resíduo é cleanup pré-gate + 2 gêneros a ver in-game. |
| **Re-tradução (R-CUSTO)** | 🟢 Baixo *(era Alto; raiz atacada 2026-06-14)* | Re-tradução era **58% do gasto** (medido), dominada por fitting-fail→retighten ao traduzir **rótulo de engine** (body/face/mask/`Leg_2_B_L`). | ✅ **Cabeado:** `model._label_passthrough` agora passa rótulos de rig como verbatim (fora do LLM) → sem estouro de budget → sem retighten. +teste. Resta (menor): cap/observabilidade de retighten. |
| **Custo depende de disciplina** | 🟢 Baixo *(reduzido 2026-06-15)* | Barato (~$0,0012–0,0016/linha) em batch. A dependência de disciplina caiu: agora há **estimativa pré-voo**, **teto duro** (gate de submissão do batch + por-cena → gasto de pior-caso ≤ teto) e **recuperação por-linha** (defeito de 1 linha não re-traduz a cena). | `run_chapter` imprime estimativa + `_fit_budget` + Batch −50% + dedup por TM. |
| **Sinais derivados stale** | 🟢 Baixo | Editar tradução pode deixar back-translation/relatórios desatualizados. | Invalidação automática + gate `tm_correct --check-sync`. |

> **Leitura honesta:** os riscos que sobram **não são de arquitetura/engenharia** (maduras) — são de
> **abrangência** (1 obra/engine), **execução humana** (QA, ratificação) e **conclusão** (terminar +
> empacotar). Padrão de arquitetura para estudar/reusar: pronto. Produto de tradução acabado: ainda não.

---

## Próximos passos

### Fase A — Fechar o caminho até produção (Utawarerumono)

- [x] **A1. Gate in-game.** ✅ **VALIDADO.**
  - ✅ **pt-BR renderiza no jogo real** (in_place) — objetivo de ponta a ponta atingido (`Fasea2/3/8/9/10`).
  - ❌ **EOF-append reprovado**: linhas relocadas ao fim do CONTAINER viram `@@@@` e travam (`Fasea11`).
    Causa: o engine carrega cada arquivo num buffer do tamanho do `size` no Pack. Ver `decision_log.md`.
  - ✅ **Plano B validado in-game** (`--validate-one 0x3442`): "ERRO DE SISTEMA." (que antes era `@@@@`)
    exibiu e o jogo seguiu para a cena seguinte sem travar (`testeplanob.png`, `testeplanob_avanco.png`).
    Relocação intra-arquivo + reescrita do Pack é a estratégia correta. **Run completa liberada.**
- [x] **A2. Ordem offset × ordem narrativa.** ✅ **VALIDADO EM ESCALA.** A extração é determinística:
  varre cada script linearmente por offset e retorna **em ordem de armazenamento (= ordem de exibição
  deste engine)** — documentado em `sdat_format.py` (`Retorna [...] em ordem de armazenamento (= ordem
  narrativa)`). Confirmado não só na abertura, mas em **9 capítulos (11–19, 77 cenas)**: você jogou
  in-game até o Haku ser nomeado e a back-translation/QA pegaria diálogo embaralhado — nenhuma divergência
  observada. **Limite arquitetural:** cada cena é job independente O(cena) + round-trip byte-idêntico →
  uma eventual divergência em cena distante não corrompe bytes; apareceria como contexto incoerente
  (capturado pela back-translation). Fallback (caminhar o bytecode por ordem de comando) documentado, mas
  **nunca foi necessário** em 77 cenas. Ver `decision_log.md`.

- [x] **A3. Estratégia de JOGO INTEIRO (~45k linhas) — loop incremental, resumível.** 🟢 **CONCLUÍDA —
  jogo inteiro traduzido.** O loop incremental virou o **harness de escala** (`framework/runtime/`):
  cena = job stateless O(cena), resumível por `run_state.json`. **Os 16 capítulos (146 cenas) traduzidos
  e verificados.** O que resta é só a Fase 3 (fechamento/pós-produção).
  - ✅ **Fase 1 — "Ler o jogo":** o corpus foi extraído; o KB/glossário cresce por **fronteira de
    spoiler móvel** (`kb_phase.py` por capítulo) em vez de um único passe global — funcionalmente
    equivalente, e mais seguro p/ spoiler (termos canônicos congelam ao entrar na fronteira).
  - ✅ **Fase 2 — Loop por capítulo (11→39):** **16 de 16 capítulos feitos** pelo driver
    `run_chapter.py` (Knowledge Building com fronteira → traduzir → back-translation alto risco →
    verify round-trip → checkpoint). Resumível; modo `--batch` (−50%) comprovado.
  - [ ] **Fase 3 — Fechamento:** passe global de **consistência de glossário** (linter determinístico) →
    `reinsert` do jogo inteiro num passe só + `pytest` + patch IPS final + **gate visual in-game**. **Pendente.**
  - **Consistência em escala:** glossário congelado + voice cards + TM + fronteira de spoiler móvel —
    tudo externalizado em flat-files (não na janela). ✅ provado em 146 cenas.
  - **Aceleração opcional:** tradução por cena é paralelizável (glossário/voz congelados) → candidata a
    **workflow multi-agente** (fan-out por cena + passe de consistência). Caminho caro; só sob demanda.
  - Esta é a **prova de produção** do framework. Casa com A4 (custo) e A5 (redução de custo).
- [x] **A4. Estimativa de custo real** — ✅ baseline medido (`framework/validation/cost_model.py` +
  `artifacts/cost_report.md`): **$/1k linhas 3.12 (forte) → 1.75 (model-mix + caching)**; projeção
  ~33k **$103 → $58 (−44%)**. Tokens ≈chars/3.8 (refinar com `count_tokens` na run real). Desbloqueia A5.
- [~] **A5. Analisar o custo atual e reduzir.** 🟢 **Alavancas no ar e medidas.** Gasto real dos caps
  11–19: **~$43,5** (Sonnet $36,7 · Haiku $3,6 · Opus $3,2), **$0 desperdiçado** (`api_ledger.jsonl` +
  `cost_report.py`). Contra a projeção da A4 com modelo forte (~$103 no jogo inteiro), o caminho atual já
  roda bem abaixo. Alavancas implementadas:
  - ✅ **Modelo certo por tarefa:** tiering Haiku (linha simples) / Sonnet (multi-linha) / Opus (só
    back-translation de alto risco).
  - ✅ **Prompt/context caching:** doutrina cacheável (~4K tok) cobrada ~1×; cache de leitura medido no
    `cost_report` (~46% — alvo de melhora).
  - ✅ **Batching e shift-left:** Batch API **−50%** comprovado vivo; T1–T3 determinístico + `byte_budget`
    no prompt; **escalonamento cirúrgico** re-traduz só a linha que estoura o budget.
  - ✅ **Evitar retrabalho:** **dedup por TM** (reuso $0); revisão humana aplica **verbatim a $0**; o jogo
    **não** é re-traduzido inteiro após o QA.
  - ✅ **Teto de gasto:** `--max-usd` uniforme nos drivers caros (para e reporta o que sobra).
  *Resta:* fechar a 2ª metade e tirar o **$/1k linhas final**; subir a taxa de cache; revisitar a meta de
  −80% com o baseline completo (hoje a redução real vs. modelo-forte já é substancial).

### Fase B — Evolução do motor (só DEPOIS da produção)

> Decisão estratégica: estes itens transformam o framework de "documento" em "motor executável".
> Construí-los antes da run completa = abstração prematura. Sequência recomendada (cada um habilita
> o próximo). Cada item vira uma rodada de planejamento própria quando chegar a vez.

- [x] **B1. Validation leve.** ✅ `framework/validation/validate.py` — validadores executáveis dos
  schemas + invariantes (glossary/handling_rule, cobertura plan↔dialogs↔approved, preservação de
  tokens, `risk_notes` quando `risk≥medium`, enums, `reveal_timing`). Genérico (lê `project.json`),
  ERROR/WARN, **7 testes pytest** (passa na ref + pega violações injetadas). Roda como Input Gate.
- [ ] **B2. Memory leve** (glossário + character state básico). Estado vivo e consultável entre os
  165 lotes, no lugar de re-ler CSV ad-hoc. Desenhar **informado pela run real** (A3).
- [ ] **B3. Kernel simples.** Runtime que orquestra os passos usando Validation (gates) + Memory
  (estado), no lugar de scripts ad-hoc. Compensa com repetibilidade (≥2 projetos ou re-runs).
- [ ] **B4. Skill DSL.** Forma declarativa dos passos 00–08 (hoje prosa .md) que o Kernel lê. Por
  último: só vale com 2–3 projetos e o Kernel existente (maior risco de abstração prematura).

### Fase C — Escalar para outras mídias

- [ ] **C1. Validar perfil de filmes** com projeto real (legenda/dublagem) → implementar conector
  `subtitle_file` (SRT/ASS), constraint de CPS. `framework/media-profiles/films.md` (stub).
- [ ] **C2. Validar perfil de séries** (≥2 episódios): glossário/decision_log compartilhados,
  spoiler-check cross-episódio, QA de continuidade. `framework/media-profiles/series.md` (stub).

---

### Adiado (baixa prioridade agora — fazer no momento certo)

- [x] **T4 em lote (LLM) — plumbing pronto.** `reinsert.py` exporta o resíduo irredutível para
  `artifacts/t4_residue.json` (lote pronto p/ reescrita LLM em 1 passada → volta pelo plano → reaplica).
  Hoje **inerte** (resíduo=0 com a relocação intra-arquivo); ativa sozinho se um corpus futuro gerar
  overflow não-relocável. 2 testes pytest (lote vazio no corpus + caso sintético).
- [x] **Metadados cognitivos por linha em escala (F2):** ✅ resolvido pelo harness. O `context_pack`
  monta por cena o pacote com `speaker`/`tone_register`/`intent` + risco calibrado data-driven
  (spoiler/glossário/entidade) + `risk_notes`, e o `translate` faz o **passe contextual por cena** — não
  mais só nas 1025 linhas da abertura, mas nas **77 cenas** dos caps 11–19. O `tone_register` fino por
  situação/emoção passou a ser produto natural do contexto montado por cena. Ver `decision_log.md`.
- ~~CI + empacotamento de release~~ — **removido** (não há release planejada agora).

---

### Backlog de qualidade de tradução (casos reais vistos in-game)

> Não quebram o jogo, mas "não fazem sentido" na leitura. Coletados de spot-checks in-game.

- [x] **⭐ processar até METADE do jogo (coleta de métricas).** ✅ **ALCANÇADO.** A **1ª metade está
  traduzida e verificada** (caps 11–19, 77 cenas) pelo harness incremental/resumível — exatamente o
  experimento de "medir em escala antes de comprometer com a run completa". Métricas colhidas:
  - ✅ **Custo real:** **~$43,5** acumulados, **$0 desperdiçado** (`cost_report.py`); recalibra A4/A5.
  - ✅ **Qualidade/contexto:** linter de naturalidade + back-translation de alto risco rodando; voz
    consistente via voice cards + TM; risco calibrado data-driven (deixou de ser 0-high).
  - ✅ **Conector em escala:** relocação intra-arquivo aguenta capítulos inteiros; round-trip
    byte-idêntico verde nas 77 cenas; resíduo controlado.
  - ✅ **Governança:** a Carta + os gates (round-trip/back/KB/spoiler) foram aplicados ponta-a-ponta num
    volume real, sem gasto invisível.
  *Decisão habilitada:* a 2ª metade (caps 20+) está **liberada** — o experimento de métricas cumpriu o papel.

- [x] **Carta de Governança de Tradução (diretrizes que a IA SEGUE).** ✅
  `framework/skills/translation_governance.md` — contrato de qualidade (voz/lore/situação/processo +
  checklist), referenciado pelos Input Gates de 06/06b/07 e por `_index.md` (regra global 14). Estrutura:
  - **Personagem (voz):** toda linha respeita o perfil de voz do falante (`tone_analysis.md`: registro,
    léxico, comprimento, tiques); `voice_criticality: high` → checagem por linha; identidade dupla nunca
    vaza a identidade revelada antes do `reveal_timing`; o personagem soa igual em todo o corpus.
  - **Mundo (lore):** glossário/`handling_rule` respeitados; formas exatas sem variação; spoilers só
    após `reveal_timing`; honoríficos e registro formal/informal conforme a relação no mundo.
  - **Situação (cena/emoção):** traduzir pela **intenção/emoção** da cena (susto, dor, comédia,
    solenidade), não pela letra; interjeições localizadas; junção de linhas quebradas soa natural;
    âncora obrigatória — *"uma pessoa lê isto nesta situação e entende com naturalidade?"*.
  - **Processo:** metadados por linha **reais** (speaker, situação/`tone_register`, risco) — não
    auto-default, pois são o que dirige a QA contextual; risco calibrado (identidade dupla, comédia,
    1ª menção de lore, spoiler = alto → **back-translation obrigatória**); IA **propõe** → humano
    **aprova** → script **aplica**; decisões não-óbvias no `decision_log.md`.
- [x] **Governança de tradução — linter determinístico (genérico, sem LLM).** ✅
  `framework/validation/naturalness_lint.py`: `copia_crua` (alvo==source fora da whitelist de
  nomes/gritos/numérico), `fragmento_residual` (hesitação `X...` copiada), `rotulo_cru` → grava
  `artifacts/naturalness_lint.json` (input do 06c). **12 testes pytest**. Varre os planos por cena do
  harness; `fragmento_residual` refinado (não dá falso-positivo em `a/e/o/é`); pula identificadores de
  asset. Na instância real (caps 11–19): **0 stammer residual** (os "U..." já viraram "Nnh...").
- [x] **Stammers/hesitações residuais.** ✅ **RESOLVIDO.** Os casos concretos já estão localizados no
  dado (`0x3640`/`0x124b1` `"U... Urgh..."` → **`"Nnh... Argh..."`**). Mecanismo de prevenção fechado:
  (a) `naturalness_lint.py` agora **varre os planos por cena** do harness (`ch_*/translation_plan_*.json`),
  não só o legado; (b) `fragmento_residual` refinado — só sinaliza inicial **copiada crua** que NÃO é
  começo pt-BR legítimo (`a/e/o/é` ficam; `U.../W.../K...` viram resíduo); (c) convenção de **stammer
  inicial** documentada (`interjection_reference.md`, regra 5 + linha na tabela). Gate: `pytest`
  (`fragmento_residual` = **0** nos caps 11–19) — não regride. $0 (offline).
- [x] **Interjeições EN copiadas cruas (achado do linter em escala).** ✅ **RESOLVIDO ($0, offline).**
  O linter em escala achou **266 `copia_crua`**; a maioria era **falso-positivo legítimo** (grito/risada/
  grunhido, SFX `*CRASH*`, cognato `animal./crime?`, nome `Sir Haku?`, label `RightFoot`). Duas frentes:
  - **Precisão do linter:** `_is_pure_onomatopoeia` agora pega grunhido sem vogal (`Ngh`,`Grr`,`Mmf`),
    risada (`hahaha`/`fufu`) e sopa-de-consoante (vogal ≤25%); pula SFX entre `*...*`, labels
    CamelCase/alfanuméricos (`RightFoot`,`lightA02`) e `speaker: rotulo`. (Família "hm/mm" segue
    sinalizada — `Hein?` vs `Hum?` é decisão de contexto.) **+4 testes** (16 no total).
  - **Localização governada:** CSV `interjection_corrections.csv` (dado) → `tm_correct.py` aplicou
    **168 substituições** em 62 arquivos só nas formas **inequívocas e sem colisão pt-BR** (`Gah→Ai`,
    `Urgh→Argh`, `Guh→Agh`, `Eep→Iik`, `Ack/Urk→Kh`, `Erm→Hum`, `Ahem→Ehem`; **deixei de fora** `Ugh`/`Uh`
    por colidirem com nojo/`Uh-oh`). **31 cenas re-verificadas** (round-trip byte-idêntico, resíduo T4=0,
    charset íntegro). `copia_crua`: **266 → 107** (o resto = cognato/nome/lore legítimo + família hm/mm,
    advisory p/ a revisão humana — não-erros).
- [x] **Rótulo de falante "Girl" em inglês in-game.** ✅ RE: o nome do falante usa o opcode **`53 00`**
  (file-relativo, ignorado pelo conector). `sdat_format.POINTER_OPCODES` agora indexa/repointa `50 00`
  **e** `53 00` → rótulos relocam como heads próprios (17/17 sites do "Girl" leem "Garota"). Travado por
  `test_label_pointers_53`. **Pendente: gate in-game** (`--validate-one 0x36a0` → exibir "Garota").
- [x] **Atribuição de speaker vs. rótulo do jogo.** ✅ Reconcile data-driven (rótulo do `53 00` mais
  próximo): 10 linhas "Mulher/Homem (memória)" eram rotuladas "Girl" → "Garota (memória)" (faithful;
  identidade segue gap de pesquisa). Ver `decision_log.md`.

---

## Já concluído (para referência)

- ✅ **Deep pass do arco (Carta exercida) + custo medido:** back-translation real nas 9 high (2 fixes
  de ambiguidade/voz), voz spot-checada (0 drift), risco cognitivo (+4 reveals), e **baseline de custo**
  ($/1k 3.12→1.75; ~33k $103→$58). Artefatos: `qa_report.md`, `back_translation_log.json`, `cost_report.md`.
  Carta de Governança, linter e Validation leve em uso. (De-risca a meia-maratona.)
- ✅ Framework SDD genérico (camadas: processo / perfil / conector / instância).
- ✅ Conector hex_binary: container `.sdat` mapeado (header `Filename`/`Pack`, 353 scripts; texto UTF-8
  contíguo por script).
- ✅ **Modelo de ponteiro corrigido para FILE-RELATIVO** (`50 00` + uint32 relativo ao início do
  arquivo) — descoberta que invalidou o modelo absoluto anterior. Ver `decision_log.md`.
- ✅ **Primeiro pt-BR do framework renderizado no jogo real** (Steam) — prova de ponta a ponta. `Fasea*.png`.
- ✅ **Plano B no conector:** relocação **intra-arquivo** + `rebuild_container` (reescreve a tabela Pack,
  padding a 16 bytes) — substitui o EOF-append reprovado in-game. 1025 linhas: T1=595, RELOC=430,
  resíduo 0; 425/425 ponteiros relocados resolvem dentro do arquivo; 9 testes pytest verdes.
- ✅ **Plano B validado in-game** (`--validate-one`): linha relocada intra-arquivo exibe e o jogo segue
  (`testeplanob.png`/`testeplanob_avanco.png`) — bloqueador "funciona no jogo?" encerrado.
- ✅ **QA de naturalidade contextual + interjeições:** regra genérica no framework (06/06b/07/games) +
  referência curada do projeto; 19 interjeições localizadas (`Nh?→Hein?`, `Ngh...→Nnh...`, `Gah!→Ai!`).
- ✅ Charset: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração na gravação**.
- ✅ Round-trip byte-idêntico + patch IPS + **teste de regressão `pytest` (9 testes: modelo file-relativo
  não-circular, relocação within-file, integridade do Pack, governança)**.
- ✅ Extração **por arco/script** (`SCENES`) com limpeza de bordas; container totalmente parseado.
- ✅ Pipeline cognitivo 00→08 rodado de verdade em **2 cenas / 1025 linhas** (entities, glossário,
  research_log com gate de cobrança, plano, micro-QA, QA, approved, reinsert).
- ✅ `.gitignore` para não versionar `.sdat` (assets com copyright).
