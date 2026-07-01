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

- [ ] **run_game** — driver ponta-a-ponta: roda todos os capítulos em sequência com Fase 0 gating + `--max-usd` + retomada automática. Elimina o "invocar cap-a-cap" manualmente.
- [ ] **Observabilidade de progresso** — linhas/min, % do jogo, ETA, taxa de falha por capítulo. Hoje só custo delta existe (`cost_report.py`).
- [ ] **`state_index` rebuild 1×/capítulo** — no batch, o rebuild por cena é redundante (tradução já concluída); mover para pós-capítulo reduz I/O sem perder consistência.

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
- [ ] **B2. Memory leve** — TM, glossário e KB consultáveis entre lotes via busca por relevância, no lugar de passar o CSV inteiro no contexto.

  #### Abordagem: sentence-transformers local (jun/2026)

  > Decisão final jun/2026: embedding semântico local com `paraphrase-multilingual-MiniLM-L12-v2`.
  > Racional: FTS5 (BM25 léxico) não cobre paráfrases cross-game ("dragon spirit" ≠ "spirit energy");
  > embedding captura significado independente de vocabulário — necessário quando o corpus crescer para 3+ jogos.

  **Solução:** `sentence-transformers` local + numpy para cosine similarity. Cache em `.npy` (não commitado).

  | Propriedade | Valor |
  |---|---|
  | Modelo | `paraphrase-multilingual-MiniLM-L12-v2` |
  | Tamanho | ~470 MB (download on-demand no primeiro uso) |
  | Deps | `sentence-transformers` (puxa torch + transformers) |
  | Query em 100k entradas | <50 ms (numpy cosine, CPU) |
  | Filtros por metadata | pós-filtro em Python (`scene`, `game`) |
  | Cache | `artifacts/state/tm_embeddings.npy` — regenerado se TM mudar |
  | Artefatos commitados | zero — `.npy` no `.gitignore` |

  **Impacto de custo:** context_pack hoje passa o TM inteiro no prompt. Com top-10 semântico, redução ~99%
  nos tokens de TM por chamada — benefício independente da abordagem léxica vs semântica.

  **Implementação:** `framework/runtime/tm_search.py` — `build_index()`, `load_index()`, `search(query, top_k, scene)`.

  **Upgrade path:** SQLite FTS5 como complemento léxico (busca exata mais rápida) quando o corpus tiver
  >500k entradas e a latência de numpy cosine virar gargalo.
- [ ] **B3. Kernel simples** — runtime que orquestra os passos usando Validation + Memory. Compensa com ≥2 projetos.
  - As primitivas (`run_scene`, `validate`, `context_pack`) devem expor contratos Python limpos e tipados — chamáveis por qualquer agente, CLI ou orquestrador externo sem depender do Claude ou de MCP. MCP tools ficam como conveniência de desenvolvimento apenas, nunca entram no produto.
- [ ] **B4. Skill DSL** — forma declarativa dos passos 00–08. Por último: só vale com o Kernel existente e 2–3 projetos.

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

#### Implementação

- [ ] **D1.** Evidence Collector + Registry T1 — `evidence_collector.py`, `tier_classifier.py`, `connector_registry.json`, `script_generator.py`. Score: **~87**
- [ ] **D2.** Coverage Gate + Adversarial Validator — `coverage_gate.py`, `adversarial_validator.py`, interface T3. Score: **~92**
- [ ] **D3.** Manifesto + Versionamento + Fingerprint — `connector_manifest.json`, `fingerprint_monitor.py`. Score: **~95**
- [ ] **D4.** TM por série + integração QA — `tm_lookup.py`, `tm_updater.py`, integração com `quality_review.py`. Score: **~97**
- [ ] **D5.** Gates de autonomia AI-agnostic:
  - **Gate de existência:** verificar `connector_registry` antes de qualquer geração — se engine conhecida, usar diretamente sem acionar LLM.
  - **Gate de leitura completa:** antes de editar conector existente, ler por inteiro e validar contra `connector_manifest.json`. Pipeline não deve depender do assistente de desenvolvimento para garantir isso.

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
