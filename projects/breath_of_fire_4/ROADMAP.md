# Roadmap — Breath of Fire IV (PT-BR)

> Última atualização: 2026-06-20
> Status atual: **FASE 00 — MAPEAMENTO DO CONECTOR PENDENTE**

---

## Objetivos e contexto de engenharia

> Por que este projeto existe além da tradução em si.

O framework foi avaliado em **81/100 como projeto de AI engineering (jun/2026) — top 10–15% do espaço**.
Os dois maiores gaps que BoF4 precisa fechar:

| Gap | Nota atual | O que BoF4 prova |
|---|---|---|
| Generalização | 62/100 | T2 do Generic Connector funcionando num engine Capcom desconhecido |
| Autonomia | 52/100 | Bootstrap de conector via descoberta de diretório sem intervenção manual |

**Se BoF4 validar T2:** nota sobe para ~86. É o maior salto único disponível no roadmap.

### Insights do projeto anterior que se aplicam aqui

- **Round-trip como oráculo** — o gate de aceitação inegociável. Não avançar sem ele verde.
- **Recovery por linha** — quando a extração falhar em N linhas, re-extrair só essas N, não o corpus inteiro.
- **R$0 desperdiçado como métrica** — custo de retry deve ser monitorado desde a Fase 0. O `api_ledger.jsonl` começa junto com o primeiro conector.
- **Engine labels não traduzem** — o Utawarerumono aprendeu isso pagando. BoF4 começa com a allowlist já no lugar.

---

## Próximos passos

### Fase 0 — Mapear o conector (gate obrigatório antes de tudo)

- [ ] **0.1. Fornecer o diretório do jogo**
  - Usuário passa o caminho/link do diretório de instalação do jogo
  - Claude explora o diretório, identifica os arquivos de diálogo e entende a estrutura (bootstrap da Fase D)
  - Não é necessário copiar manualmente para `artifacts/` — a descoberta é parte do processo

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

> Respondidas pelo **Generic Connector System (Fase D do ROADMAP raiz)**.
> BoF4 é o jogo-piloto dessa fase — as decisões de design foram tomadas aqui.

1. ~~O conector BoF4 é reutilizável para outros jogos Capcom PS1?~~ → **Sim, via registry T1 (Fase D1): se engine idêntica, script reutilizado direto; se variante, reclassifica como T2.**
2. ~~Como versionar o conector se mudar após cenas já traduzidas?~~ → **`connector_version` no manifesto (Fase D3): extrações antigas com versão anterior ficam marcadas; framework recomenda re-extração.**
3. ~~TM compartilhada faz sentido entre jogos da série BoF?~~ → **Sim, `tm/breath_of_fire.json` compartilhado entre BoF 3, 4, Dragon Quarter (Fase D4); retradução de 1 jogo deleta só as entradas dele.**
