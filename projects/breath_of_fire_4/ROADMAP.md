# Roadmap — Breath of Fire IV (PT-BR)

> Última atualização: 2026-06-21
> Status atual: **CICLO DE TRADUÇÃO COMPLETO**

---

## Objetivos e contexto de engenharia

> Por que este projeto existe além da tradução em si.

O framework foi avaliado em **86/100 como projeto de AI engineering (jun/2026, pós-gap-closure) — top 10–15% do espaço**.
Os dois maiores gaps que BoF4 precisa fechar:

| Gap | Nota atual | O que BoF4 prova |
|---|---|---|
| Generalização | 62/100 | T2 do Generic Connector funcionando num engine Capcom desconhecido |
| Autonomia | 52/100 | Bootstrap de conector via descoberta de diretório sem intervenção manual |

**Se BoF4 validar T2:** nota sobe para ~92. É o maior salto único disponível no roadmap — Portabilidade (dim 10) passa de 6 para 9+.

### Insights do projeto anterior que se aplicam aqui

- **Round-trip como oráculo** — o gate de aceitação inegociável. Não avançar sem ele verde.
- **Recovery por linha** — quando a extração falhar em N linhas, re-extrair só essas N, não o corpus inteiro.
- **R$0 desperdiçado como métrica** — custo de retry deve ser monitorado desde a Fase 0. O `api_ledger.jsonl` começa junto com o primeiro conector.
- **Engine labels não traduzem** — o Utawarerumono aprendeu isso pagando. BoF4 começa com a allowlist já no lugar.

---

## Próximos passos

### Fase 0 — Mapear o conector (gate obrigatório antes de tudo)

- [x] **0.1. Fornecer o diretório do jogo**
  - Usuário forneceu: `C:\Program Files (x86)\Steam\steamapps\common\4249150_breathoffire4`
  - Claude explorou o diretório, identificou 609 arquivos DAT, mapeou o formato container Capcom

- [x] **0.2. Análise hex — localizar strings**
  - Formato mapeado: container TOC Capcom (offsets little-endian uint32 × 16 bytes/entrada)
  - Encoding: ASCII puro (0x20–0x7E) + tokens de controle `[XX]`
  - Tabela de ponteiros: uint16 LE no início da seção, first_ptr = tamanho da tabela
  - String sharing: ponteiros podem apontar para o interior de outras strings (requer preservação)

- [x] **0.3. Preencher `connector/table_schema.md`**
  - Charset / encoding documentado
  - 9 tokens de controle conhecidos documentados ([01] newline, [02] page_break, [04] var_char_name, ...)
  - Estratégia de ponteiros (tabela central no início da seção)

- [x] **0.4. Implementar `connector/extract.py`**
  - `parse_toc` + `find_text_section` (heurística pointer table + ASCII% + valid ptrs) + `decode_string`
  - Gera `artifacts/dialogs.csv`: 23582 strings de 264 arquivos
  - Offset format: `FILENAME.DAT:entry_idx:ptr_idx`

- [x] **0.5. Validar round-trip byte-idêntico** ← gate obrigatório ✅
  ```
  pytest connector/test_roundtrip.py -v --dat-dir "<english/DAT>"
  # Resultado: 10/10 passed (30/30 arquivos round-trip perfeito)
  ```
  - Insight crítico: seções Capcom usam string sharing; rebuild_section retorna bytes originais
    quando nenhuma string mudou (preserva sharing, garante byte-idêntico)

- [x] **0.6. Implementar `connector/reinsert.py`**
  - `encode_string` + `rebuild_section` (identity fast-path + rebuild com traduções)
  - `patch_dat_file`: atualiza TOC se seção crescer
  - Cascata T1→T3 documentada em `project.json`: `space_strategy: "reconstrucao_secao"`

---

### Fase 1 — Pipeline cognitivo (Passos 01–05)

> Iniciar somente após round-trip verde e `pytest` passando.

- [x] **1.1. Passo 01 — Descoberta de Entidades:** `artifacts/entities.csv` (78 entidades), `kb_phase discover` OK
- [x] **1.2. Passo 02 — Resolução de Entidades:** nomes canônicos PT-BR + handling rules em `entities.csv` e `glossary.csv`
- [x] **1.3. Passo 03 — Knowledge Building:** `artifacts/research_log.md` status `reconciled`; gate `kb_phase all --check` verde; fonte T1 Wikipedia PT (humano) + T2 corpus (IA)
- [x] **1.4. Passo 04 — Glossário:** `artifacts/glossary.csv` com 101 termos e handling rules formais
- [x] **1.5. Passo 05 — Plano de tradução:** `artifacts/translation_plan.json` — escopo, modelo (Haiku+Sonnet), piloto AREAD001+004 (~$0.30), estimativa full game (~$8 Haiku), `project.json` TBDs preenchidos

---

### Fase 2 — Tradução em escala (Passos 06–07) — CONCLUÍDA ✅

- [x] **2.1. Traduzir cenas iniciais** (AREAD001+004 piloto; `build_plan_chapter.py` + `verify_chapter.py` implementados)
- [x] **2.2. Loop por capítulo** via `run_chapter.py` — 125 cenas, todas `verified`
- [x] **2.3. Back-translation** de linhas `risk≥high` por cena

#### P1 — Bugs ativos — TODOS RESOLVIDOS EM PRODUÇÃO ✅

- [x] **P1-A. T4 fitting** — resolvido durante a tradução em escala (run_state confirma T4=0 global)
- [x] **P1-B. Encoding corrompido (AREAD013)** — resolvido; cena `verified` no estado final
- [x] **P1-C. `coverage_failed` (6 cenas)** — resolvido; todas as 6 cenas `verified` no estado final

#### Memory Layer (piloto desta funcionalidade no framework)

> Pré-requisito: ao menos 1 capítulo traduzido e aprovado (TM com volume suficiente para retrieval útil).
> Infraestrutura: local (CPU), zero custo de API, empacotável em .exe.

  **Stack escolhida (benchmark jun/2026):**

  | Componente | Modelo | Tamanho | Função |
  |---|---|---|---|
  | **Bi-encoder** | `paraphrase-multilingual-MiniLM-L12-v2` | ~470 MB | Embedding de TM, KB e glossário |
  | **Reranker** | FlashRank (`MiniLM-L-12` quantizado) | ~4 MB | Reordena top-N por relevância real |
  | **NER** | `spaCy xx_ent_wiki_sm` | ~31 MB | Extração de entidades Passo 01 (PT+EN) |
  | **Vector DB** | `sqlite-vec` | extensão C | Índice vetorial com filtros SQL nativos |

- [ ] **2.4. TM semântica** — indexar `approved_*.csv` com byte_budget; retrieval por similaridade substitui match exato. Medir hit rate antes/depois.
- [ ] **2.5. Context pack semântico** — `context_pack.py` passa a recuperar só chunks relevantes de glossário e KB em vez de carregar tudo. Medir redução de tokens por cena.
- [ ] **2.6. Few-shot de fitting** — ao traduzir linha nova, recuperar linhas aprovadas semanticamente similares que couberam no byte_budget; passar como exemplos no prompt. Medir redução de fitting failures.

---

### Fase 3 — Fechamento e pós-produção — CONCLUÍDA ✅

- [x] **3.1. Passe global de consistência** (`glossary_lint`)
- [x] **3.2. `reinsert` do jogo inteiro** — 125 DAT files em `output/`, T4=0
- [x] **3.3. Gate visual in-game** — OK
- [x] **3.4. QA humana** via `quality_review.py` (XLSX revisado e aplicado)

### Próximos passos

- [ ] **TM semântica (B2)** — quando corpus multi-game justificar (ver seção Memory Layer acima)

---

## Questões abertas (piloto multi-game)

> Respondidas pelo **Generic Connector System (Fase D do ROADMAP raiz)**.
> BoF4 é o jogo-piloto dessa fase — as decisões de design foram tomadas aqui.

1. ~~O conector BoF4 é reutilizável para outros jogos Capcom PS1?~~ → **Sim, via registry T1 (Fase D1): se engine idêntica, script reutilizado direto; se variante, reclassifica como T2.**
2. ~~Como versionar o conector se mudar após cenas já traduzidas?~~ → **`connector_version` no manifesto (Fase D3): extrações antigas com versão anterior ficam marcadas; framework recomenda re-extração.**
3. ~~TM compartilhada faz sentido entre jogos da série BoF?~~ → **Sim, `tm/breath_of_fire.json` compartilhado entre BoF 3, 4, Dragon Quarter (Fase D4); retradução de 1 jogo deleta só as entradas dele.**
