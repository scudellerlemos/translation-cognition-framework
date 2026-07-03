# Roadmap — Translation Cognition Framework (SDD)

> Última atualização: 2026-07-01
> Histórico do projeto piloto Utawarerumono em `projects/utawarerumono/ROADMAP_history.md`.

---

## Maturidade do framework

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro (~92/100) |
| Harness de escala (`framework/runtime/`) | 🟢 em produção — validado em 16 capítulos, ~45.100 linhas, R$ 0 desperdiçado |
| Conector hex_binary (Utawarerumono) | 🟢 completo — round-trip byte-idêntico, validado in-game |
| Generic Connector System (Fase D) | 🟡 piloto concluído (BoF4) — automação D1–D5 pós-produção |
| Perfis filme/série + subtitle_file | 🔴 stub / não iniciado |

---

## BoF4 — CONCLUÍDO ✅

> 125 cenas (AREAD + AREAS), pipeline 00–08, QA humana, 125 DAT files em `output/`, T4=0.
> Custo: ~$11,04 USD. Plano detalhado: `projects/breath_of_fire_4/ROADMAP.md`.

Débito remanescente: TM semântica (B2) — quando corpus multi-game justificar.

---

## Próximos passos do framework

### ⚡ PRIORIDADE ATUAL — P2.5: Maturidade de execução (barato, agora)

> Framework em produção e BoF4 concluído. Os três itens abaixo são orquestração
> local (sem nova chamada de LLM) e desbloqueiam escala de múltiplos capítulos
> sem intervenção manual.

- [x] **run_game** — ✅ **feito (2026-07-03)** `framework/runtime/run_game.py`: driver ponta-a-ponta, descobre capítulos (`ch_<N>_*`) ou cai no modo flat (Souldiers-like, rótulo `"full"` + `--scenes-glob`); `--max-usd` é teto GLOBAL (encolhe entre capítulos); retomada automática de graça (reusa `run_state.json`, zero estado novo). Testes: `test_run_game.py` (5).
- [x] **Observabilidade de progresso** — ✅ **feito** `framework/runtime/progress_report.py`: % do jogo, linhas/min, ETA, taxa de falha — puro/determinístico (elapsed_s passado pelo caller, sem `time.time()` interno). Impresso pelo `run_game` após cada capítulo. Testes: `test_progress_report.py` (5).
- [x] **`state_index` rebuild 1×/capítulo** — ✅ **feito**: `run_scene.py` ganhou `rebuild_index` (default `True`, preserva o modo interativo); `run_chapter.py` passa `rebuild_index=False` em modo batch e faz 1 rebuild só para o capítulo inteiro após o loop (`_rebuild_index_phase`). Testes: `test_batch_mode_rebuilds_state_index_once_per_chapter` + 2 em `test_run_scene.py`.

---

### ✅ PRIORIDADE #1 — Versionamento de Artefatos e Prompts (ENTREGUE)

> **Por quê:** sem proveniência, qualquer melhoria de doutrina é retroativamente cega — não há como saber quais cenas foram traduzidas com instrução obsoleta.

- [x] **V1. Proveniência nos artefatos** — `translations_*.json` recebe `_meta` com `doctrine_hash`, `model_id`, `skills_revision`; `pack.json` expõe `doctrine_hash` e `skills_revision`.
- [x] **V2. Prompt como artefato versionado** — `scene_prompt.md` auditável; `prompt_hash` gravado no `run_state.json` por cena via `_pack_and_translate`.
- [x] **V3. Detecção de stale** — `_doctrine_hash()` em `context_pack.py`; `run_scene.py --check-stale` lista cenas desatualizadas por projeto.
- [x] **V4. Invalidação seletiva via TM** — cada entrada de TM carrega `doctrine_version`; `state_index.py --check-sync` lista cenas afetadas pela mudança de doutrina.

---

### Evolução do Motor (pós-produção BoF4)

- [x] **B1. Validation leve.** ✅ `framework/validation/validate.py` — genérico, ERROR/WARN, 7 testes pytest.
- [x] **B2. Memory leve** — ✅ **feito (confirmado 2026-07-03, checkbox estava desatualizado)** — TM/KB
  consultáveis por relevância via busca semântica, não o CSV inteiro no prompt.

  #### Implementação real: sqlite-vec + embedder (não o tm_search.py documentado originalmente)

  > A abordagem `tm_search.py` (cache `.npy` flat, `sentence-transformers` local) documentada abaixo
  > foi **superada** por uma implementação DB-based mais integrada, sem nunca ter sido cabeada —
  > ficou como código órfão (zero callers). **Removido em 2026-07-03** (`tm_search.py` +
  > `test_tm_search.py`) para não deixar duas implementações concorrentes do mesmo conceito.

  **Solução real, em produção:** `framework/runtime/context_pack.py::build_pack` chama
  `_load_tm_semantic()` (linha 394) e `_load_kb()` (linha 437), que usam `framework/db/embedder.py` +
  `framework/db/store.py` (SQLite + extensão `sqlite-vec`) — gated por `_db_path(root, cfg)`: só
  ativa se o projeto tiver banco `.db` configurado (switch deliberado; sem `.db`, cai pro fallback de
  sempre, testado). Validado com 6046 vetores no `translation_software` (busca exata → score 1.0,
  variação de vocabulário → 0.944). Testes: `framework/db/test_context_pack_parity.py`,
  `test_export.py`, `test_migrate.py`. Ver memória `semantic-stack-validated`.

  **Upgrade path (ainda válido):** SQLite FTS5 como complemento léxico quando o corpus tiver >500k
  entradas e a latência de busca vetorial virar gargalo.
- [x] **B3. Kernel simples** — ✅ **feito (2026-07-03, escopo reduzido: fachada, não reimplementação)**.
  `run_scene.run_scene`/`run_chapter.run_chapter`/`run_game.run_game` (todos já tipados, sem
  Claude/MCP) + `validate.validate_project` + `context_pack.write_pack` já formam o "runtime que
  orquestra usando Validation + Memory" pedido — `framework/runtime/kernel.py` só consolida sob um
  import único (fachada pura, testada por identidade — `test_kernel.py`). Reimplementar do zero
  duplicaria 442+353+100 linhas já testadas (315+ testes) sem ganho real.
- [x] **B4. Skill DSL** — ✅ **já feito, descoberto na auditoria (nenhum código novo necessário)**.
  `framework/skills/skill_base.py` (`Skill` ABC: `skill_id`/`required_inputs`/`check_inputs`/`run`)
  + `registry.py` (`get`/`all_skills`) já são a forma declarativa dos passos 00/06/07/08 (os com
  substância de código). Cognitivas puras (01-04b/05b/06c) ficam `.md` por decisão deliberada — não
  é lacuna, é a fronteira já documentada em `skills-registry-boundary`.

---

### Outras Mídias (Filmes e Séries)

- [ ] **C1. Perfil de filmes** — conector `subtitle_file` (SRT/ASS), constraint de CPS. `framework/media-profiles/films.md` (stub).
- [ ] **C2. Perfil de séries** — glossário/decision_log compartilhados, spoiler-check cross-episódio. `framework/media-profiles/series.md` (stub).

  #### Stack de voz (filmes/séries — pós-produção BoF4)

  > Para filmes e séries, "voz" deixa de ser só texto (voice card) e passa a incluir áudio real.
  > Pipeline novo: áudio → ASR → diarização → voice card enriquecida → pipeline existente.
  > Todos os componentes rodam local em CPU; baixados on-demand (~900 MB total).

  | Componente | Modelo/Lib | Tamanho | Função |
  |---|---|---|---|
  | **ASR** | `faster-whisper` (medium) | ~500 MB | Transcreve áudio em texto com timestamps |
  | **Diarização** | `pyannote/speaker-diarization-3.1` | ~300 MB | Identifica quem fala em cada segmento |
  | **Combinado** | WhisperX | wrapper | ASR + diarização integrados |
  | **Prosódia** | SpeechBrain | ~100 MB | Extrai pitch, tempo, energia por personagem |

  Voice card enriquecida: adiciona `pitch_range`, `tempo`, `energia`, `cps_máximo` (characters per second medido do áudio) — o `cps_máximo` por personagem substitui o byte_budget fixo como constraint de fitting em filmes.

---

### Fase D — Generic Connector System

> Jogo-piloto: **Breath of Fire IV** — ver `projects/breath_of_fire_4/ROADMAP.md`.
> Score do framework: **86/100** (jun/2026, pós-gap-closure) → alvo após D4: **97/100**.

**Visão:** quando o framework encontra um novo jogo, descobre automaticamente os arquivos de diálogo, entende a estrutura, gera um conector determinístico, valida via round-trip. O LLM participa **apenas no bootstrap** — após aprovação, o conector roda sem IA.

#### Arquitetura

```
novo jogo
    │
    ▼
[1] evidence_collector      ← entropia, string scan, magic bytes, encoding detection
    │
    ▼
[2] tier_classifier         ← T1 / T2 / T3
    │
    ├── T1 ──► connector_registry (engine conhecida — script direto, sem LLM)
    ├── T2 ──► script_generator  (LLM + evidências → candidato → confirmação humana)
    └── T3 ──► contrato de escape (humano implementa extract / reinsert / validate)
                   │
    ┌──────────────┘
    ▼
[3] coverage_gate           ← dry-run obrigatório; COVERAGE_FLOOR=85%; 3+ arquivos
    │
    ▼
[4] adversarial_validator   ← multi-arquivo + distribuição estatística + consistência
    │
    ▼
[5] round_trip_validator    ← portão final de aceitação (inegociável)
    │
    ▼
[6] connector_manifest      ← tier, versão, fingerprints, validation_status
```

#### TM por série

- `tm/{série}.json` — isolada por série; jogos da mesma série compartilham, séries diferentes nunca se misturam
- TM usada apenas na entrada; traduções aprovadas pelo QA alimentam a TM de volta
- Retradução de um jogo: warning explícito + delete das entradas daquele jogo na TM da série

> ✅ **Implementado (2026-07-03).** `tm_lookup.py`: série declarada via `project.json["series"]`
> (opcional — fallback = slug do título, zero mudança de comportamento pros 3 projetos existentes
> até um humano declarar a mesma série em 2+ `project.json`). `tm/<série>.json` fica na RAIZ do repo
> (committed — acumula conhecimento cross-projeto, diferente do cache-por-projeto regenerável).
> Isolamento estrutural: cada série tem seu próprio arquivo, impossível misturar por construção.
> `tm_updater.py`: `sync_scenes()` faz upsert por `(source_game, src_key)` lendo
> `translation_plan_<sid>.json` (não `approved_<sid>.csv` — esse é projeção do conector que o ciclo
> de QA não regenera; achado real durante a implementação) das cenas VERIFIED tocadas pelo QA;
> `reset_game()` remove só as entradas de 1 jogo (retradução), avisa explicitamente antes (ação
> irreversível sem backup manual). Integração: `quality_review.apply()` chama `sync_scenes()` ao
> final (best-effort, nunca derruba o apply); novo subcomando `quality_review.py sync-tm <projeto>
> [<cap>]` força sync manual de capítulos já verified sem nenhuma correção (gap aceito: cena 100%
> limpa nunca é "tocada" por `apply()`). `context_pack.py` ganhou `tm_series` no pack + seção "6b"
> no prompt, só aparece se não-vazia. Testes: `test_tm_lookup.py` (8), `test_tm_updater.py` (5) +
> 3 de integração em `context_pack`/`quality_review`.

#### Implementação

- [x] **D1.** ✅ **feito e testado** (confirmado 2026-07-03 — checkbox estava desatualizado)
  Evidence Collector + Registry T1 — `evidence_collector.py`, `tier_classifier.py`,
  `connector_registry.json`, `script_generator.py`. Testes: `test_evidence_collector.py`. Score: **~87**
- [x] **D2.** ✅ **feito (2026-07-03)** Coverage Gate + Adversarial Validator —
  `coverage_gate.py` (dry-run do candidato T2 contra os 3 maiores arquivos reais, sem subprocess —
  importa `iter_string_offsets`/`decode_string` via `importlib`; piso 85% no MÍNIMO entre arquivos,
  não na média) + `adversarial_validator.py` (arquivo zerado entre populados, variância >1.5 entre
  arquivos, offsets sobrepostos). Interface T3: reusa os mesmos gates sem adaptação — dependem só
  do contrato de função, não da origem do módulo. `discover.py` aponta pro gate no passo-a-passo T2,
  antes do `connector_smoke.py`. Testes: `test_coverage_gate.py` (9), `test_adversarial_validator.py`
  (5). Score: **~92**
- [x] **D3.** ✅ **feito (2026-07-03)** Manifesto + Versionamento + Fingerprint —
  `framework/runtime/fingerprint_monitor.py`: `connector_manifest.json` por projeto (tier, engine,
  versão, `scripts_fingerprint` + `source_fingerprint`, `last_validated`), fingerprint de
  ARQUIVOS-FONTE do jogo (novo — `_connector_hash` existente só cobria os scripts do conector, não
  reimplementado, só reusado via `check_scripts_drift`). CLI standalone, não amarrado no hot path
  de `run_scene`/`run_chapter` (exige `data_dir` da instalação real). Testes:
  `test_fingerprint_monitor.py` (7). Score: **~95**
- [x] **D4.** ✅ **feito (2026-07-03)** TM por série + integração QA — ver detalhe abaixo. Score: **~97**
- [x] **D5.** ✅ **feito (2026-07-03)** Gates de autonomia AI-agnostic:
  - **Gate de existência:** `tier_classifier.existence_gate()` — formaliza o que `discover.py` já
    fazia via if/elif implícito; `must_generate=True` SÓ em T2 (T1 aponta pro conector de
    referência, T3 fica bloqueado — geração via LLM estruturalmente impossível fora de T2).
    `discover.py` refatorado pra usar. Testes: `test_tier_classifier_gate.py` (3).
  - **Gate de leitura completa:** `connector_gate.assert_fresh_read(script_path, claimed_content)`
    — interpretação operacional escolhida (mais codificável/testável): o caller passa o CONTEÚDO
    INTEIRO que alega ter lido (não um path); o gate compara hash do alegado vs. hash do disco
    agora — diverge = `StaleReadError` (arquivo mudou, ou conteúdo nunca foi lido de verdade).
    Testes: 3 novos em `test_connector_gate.py`. **Honestidade de status**: a função existe e está
    testada, mas NÃO tem nenhum caller em produção ainda (`run_scene.py`/`connector_mgr.py` não a
    chamam) — não há um ponto natural no runtime determinístico pra isso, já que "editar um
    conector existente" é ação humana/Claude durante onboarding/manutenção, não algo que acontece
    dentro do loop de tradução por cena. Infraestrutura pronta, disponível pra quem for editar um
    conector manualmente chamar antes de escrever — não uma garantia ativamente imposta hoje.

#### D6 — Gate de completude de Fase 0/1 (`connector_gate.py`)

> Descoberto no onboarding do Souldiers (2026-07-02): `project.json` declarava "Fase 0 concluída"
> com só `extract.py`/`reinsert.py` prontos — `build_plan_chapter.py`/`verify_chapter.py`/
> `test_roundtrip.py` nunca existiram, ou seja, round-trip NUNCA tinha sido validado de verdade.
> Mesma classe de bug do gap de KB (ver `kb_gate.py` — [[onboarding-scaffold-kb-gate-drift]]):
> "fase declarada concluída" sem nenhum gate automático checando o conjunto completo de artefatos
> antes do primeiro gasto real em tradução. O piloto pago é que acabou achando os dois, tarde.

- [x] **D6a.** ✅ **feito (2026-07-03)** `framework/runtime/connector_gate.py` (espelha `kb_gate.py`)
  — hard-block se `build_plan_script`/`verify_script` (via `connector_mgr`) não existirem no disco;
  soft-block (bypassável via `--skip-connector-gate`) se nenhuma cena do projeto tem `verified=True`
  em `run_state.json` (reusa o estado que já existe — sem manifest/timestamp novo). `run_scene.py` e
  `run_chapter.py` chamam ANTES do `kb_gate` (conector é pré-requisito mais fundamental). Testes:
  `test_connector_gate.py` (6) + integração em `test_run_scene.py`/`test_run_chapter.py`.
- [x] **D6b.** ✅ **feito** `script_generator.py` ganhou `generate_build_plan_chapter()`/
  `generate_verify_chapter()` — lêem os esqueletos novos em `framework/connectors/_skeleton/`
  (`build_plan_chapter.py`, `verify_chapter.py`), generalizados a partir dos 3 conectores reais
  (BoF4/Utawarerumono/Souldiers). Diferente do `extract.py` (3 padrões por evidência), aqui não há
  branching — é sempre o mesmo esqueleto com pontos `# ADAPTAR` (tokens estruturais do engine em
  `build_plan_chapter.py`; a reconstrução byte-a-byte, 100% específica do formato, em
  `verify_chapter.py`). O protocolo de SAÍDA (exit 0/1/3 + `VERIFY_STATUS:{json}`) é fixo/reusável.
  Testes: `test_script_generator.py` (3).
- [x] **D6c.** ✅ **feito** `scaffold_project.py` ganhou `_report_connector_gate_status()` (mesmo
  padrão de `_report_kb_gate_status`) — reporta no fim do scaffold se os scripts estão ausentes,
  visível no dia 1 do onboarding; nunca cria stub fake (mesma governança do KB). Testes: 2 novos em
  `test_scaffold_kb_gate.py`.

#### Teto dos 3 pontos (irredutível)

Formatos cifrados/ofuscados exigem engenharia reversa — fora do escopo. O `evidence_collector` os detecta e classifica como `T3-bloqueado`.

---

### Adiado

- [x] **T4 em lote (LLM).** Plumbing pronto em `reinsert.py` (`t4_residue.json`). Inerte hoje (resíduo=0); ativa sozinho se corpus futuro gerar overflow não-relocável.
- ~~CI + empacotamento de release~~ — removido (escopo antigo; substituído por CI offline e packaging nas seções abaixo).

---

### Produto e Distribuição (pós-validação BoF4)

> **Pré-requisito:** round-trip do BoF4 verde + Generic Connector System validado.
> **Valor:** comunicação externa (portfolio, open-source) — zero valor operacional para uso interno.

- [ ] **E1. CLI instalável** — entrypoint `tcf` via `pyproject.toml` (`tcf translate`, `tcf extract`, `tcf verify`).
- [ ] **E2. README de produto** — reescrever o README raiz como "você instala e usa" em vez de tour pela árvore.
- [ ] **E3. Consolidar documentação** — mover `.md` puramente documentais para `docs/`; os `.md` de runtime (skills, schemas) ficam onde estão.
- [ ] **E4. Distribuição como `.exe`** — PyInstaller ou Nuitka empacotam CLI + runtime Python em binário standalone para usuários sem Python. Modelo `paraphrase-multilingual-MiniLM-L12-v2` (~470 MB) baixado on-demand no primeiro uso.

---

### CI e Qualidade Contínua (pós-validação BoF4)

> **Pré-requisito:** framework estável com ≥2 projetos ativos.
> **Valor:** garante que nenhum commit regride o harness silenciosamente — crítico quando virar produto.

- [x] **F1. CI offline** — 3 workflows paralelos (quality, test, api-smoke); 316 testes, cobertura 90.17%; matrix 3.11/3.12. ✅
- [ ] **F2. CI de packaging** — após `pytest` passar, PyInstaller builda o `.exe` e um smoke test valida o binário gerado.
- [ ] **F3. LLM judge** — segundo modelo avalia fidelidade + naturalidade + aderência ao personagem com score numérico por linha; complementa o back-translate e prioriza o QA humano melhor que o risco heurístico atual.
