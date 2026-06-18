# Roadmap — Breath of Fire IV (PT-BR)

> Última atualização: 2026-06-18
> Status atual: **FASE 00 — MAPEAMENTO DO CONECTOR PENDENTE**

---

## Próximos passos

### Fase 0 — Mapear o conector (gate obrigatório antes de tudo)

- [ ] **0.1. Fornecer o binário de diálogo**
  - Copiar o arquivo de diálogo do jogo para `artifacts/`
  - Atualizar `connector.source_binary` em `project.json`

- [ ] **0.2. Análise hex — localizar strings**
  - Abrir no HxD e buscar strings reconhecíveis ("Ryu", "Cray", "Nina")
  - Identificar estrutura: encoding, terminadores, tokens de controle, ponteiros

- [ ] **0.3. Preencher `connector/table_schema.md`**
  - Charset / encoding
  - Tokens de controle (quebra de linha, pausa, cor, etc.)
  - Estratégia de ponteiros (inline, tabela central, varredura)

- [ ] **0.4. Implementar `connector/extract.py`**
  - `load_table` + `iter_string_offsets` + `decode_string`
  - Gera `artifacts/dialogs.csv` com `offset`, `text_en`, `byte_budget`

- [ ] **0.5. Validar round-trip byte-idêntico** ← gate obrigatório
  ```
  python connector/extract.py artifacts/<BINARIO>
  python connector/reinsert.py artifacts/dialogs.csv
  diff <original> output/<BINARIO>   # deve ser vazio
  pytest connector/test_roundtrip.py -v   # habilitar os 2 testes em skip
  ```

- [ ] **0.6. Implementar `connector/reinsert.py`**
  - `encode_string` + cascata T1→T3 + `emit_patch`
  - Atualizar `project.json`: `patch_format`, `encoding`, `space_strategy`

---

### Fase 1 — Pipeline cognitivo (Passos 01–05)

> Iniciar somente após round-trip verde e `pytest` passando.

- [ ] **1.1. Passo 01 — Descoberta de Entidades:** varrer corpus, listar personagens/locais/termos únicos
- [ ] **1.2. Passo 02 — Resolução de Entidades:** confirmar nomes canônicos pt-BR, handling rules, pares de identidade
- [ ] **1.3. Passo 03 — Knowledge Building:** pesquisa de lore, ratificação humana (`kb_ratified.csv`), gate KB
- [ ] **1.4. Passo 04 — Glossário:** `artifacts/glossary.csv` com handling rules formais
- [ ] **1.5. Passo 05 — Plano de tradução:** `translation_plan.json`, corpus de teste sintético

---

### Fase 2 — Tradução em escala (Passos 06–07)

- [ ] **2.1. Traduzir cenas iniciais** (~1 cena piloto a ~$0.30 para validar batch + conector live)
- [ ] **2.2. Loop por capítulo** via `run_chapter.py` com `--max-usd`
- [ ] **2.3. Back-translation** de linhas `risk≥high` por capítulo

---

### Fase 3 — Fechamento e pós-produção

- [ ] **3.1. Passe global de consistência** (`glossary_lint`)
- [ ] **3.2. `reinsert` do jogo inteiro** + `pytest` + patch final
- [ ] **3.3. Gate visual in-game** (spot-check de cenas chave)
- [ ] **3.4. QA humana** via `quality_review.py` (XLSX)

---

## Questões abertas (piloto multi-game)

A responder à medida que o projeto avança (ver `memory/connector-multi-game-future.md`):

1. O conector BoF4 é reutilizável para outros jogos Capcom PS1?
2. Como versionar o conector se mudar após cenas já traduzidas?
3. TM compartilhada faz sentido entre jogos da série BoF?
