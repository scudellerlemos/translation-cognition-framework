# Onboarding — Novo Projeto de Tradução

> Guia passo a passo para instanciar um projeto no framework SDD.
> Criado após o piloto Utawarerumono (jun/2026) — primeira validação multi-game; atualizado após
> o onboarding de baixo custo (scaffold + descoberta automática de engine + KB híbrida, validado
> no Souldiers, jul/2026).

---

## Pré-requisitos

- Você tem o binário (ou arquivo de texto/legenda) da obra-fonte.
- A branch de trabalho está criada.
- O framework está em `framework/` e os testes passam (`pytest framework/`).
- **No Windows**: setar `PYTHONIOENCODING=utf-8` (ou `chcp 65001`) antes de rodar qualquer CLI do
  framework (`discover.py` e afins). Sem isso, `print()` com acento/seta quebra com
  `UnicodeEncodeError` em console cp1252 — bug pré-existente, não corrigido no código
  (issue #119; confirmado reproduzindo ainda em 23/08/2026 durante o bring-up do Trails in the
  Sky 2nd Chapter). Nenhum projeto até aqui foi bloqueado porque o texto-fonte é ASCII, mas é
  verificação obrigatória antes de rodar `discover.py` num ambiente novo.

---

## Caminho rápido (recomendado): scaffold + descoberta automática

Antes de seguir o passo a passo manual abaixo, use as ferramentas de onboarding de baixo custo —
reduzem o custo de dar início a um projeto novo de ~40k para ~5k tokens de sessão:

1. **`scaffold_project.py`** cria a estrutura de diretórios (`connector/`, `profile/`, `artifacts/`)
   e um `project.json` inicial, e roda um self-check de `kb_gate.py`/`connector_gate.py` — reporta
   exatamente o que falta preencher, sem criar stub fake pra enganar o gate.
2. **`python framework/connectors/discover.py <game_dir>`** varre o diretório do jogo e classifica
   automaticamente o engine:
   - **engine conhecida** (já no `connector_registry.json`, ex.: Aquaplus/Capcom DAT/Unity
     Addressables): aponta direto pro conector de referência — copiar e adaptar, pular a etapa
     manual de mapeamento hex.
   - **engine desconhecida**: `--generate-stub` gera o PAR `extract.py` + `reinsert.py`
     pré-preenchidos (#108; mesmo padrão nos dois — linear_scan/token_table/pointer_table,
     escolhido pelas evidências) — ponto de partida bem mais adiantado que o `_skeleton/`
     genérico. Validar cobertura ANTES do round-trip completo:
     `python framework/connectors/coverage_gate.py <candidato.py> <game_dir>`. Loop de
     refino documentado em `framework/connectors/agentic_synthesis.md`.
   - **bloqueada** (cifrado/comprimido): fora do escopo do framework, exige engenharia reversa.
3. **KB sem custo de API**: `kb_fetch.py` normaliza qualquer fonte (URL, PDF, .docx, arquivo local)
   pra texto plano; `kb_build_ollama.py` gera um RASCUNHO de research/KB via Ollama LOCAL (zero
   custo, mas sempre `status: draft_ollama`); `kb_reconcile.py` promove pra `reconciled` só depois
   de ratificação humana por entidade — a governança de "fonte confiável antes de traduzir"
   continua intacta, só a extração bruta fica mais barata.

O passo a passo manual abaixo continua válido — é o que essas ferramentas automatizam por baixo,
e é o caminho pra qualquer parte que a descoberta automática não cobrir (engine desconhecida sem
candidato gerado, formato exótico, etc.).

---

## Estrutura esperada

```
projects/<slug>/
  project.json          ← configuração central (ver abaixo)
  connector/
    table_schema.md     ← schema de caracteres/tokens (mapear no Passo 00)
    extract.py          ← extrator determinístico (adaptar do _skeleton)
    reinsert.py         ← reinseridor determinístico (adaptar do _skeleton)
    test_roundtrip.py   ← testes de contrato do conector (ver _skeleton)
  profile/
    voice_profiles_reference.md
    identity_pairs_reference.md
    terminology_seeds.md
    example_test_suites.md
  artifacts/
    dialogs.csv         ← gerado por extract.py (Passo 00)
  output/               ← gerado por reinsert.py (Passo 08)
  README.md
```

---

## Passo a passo

### 0. Criar project.json

Copiar `framework/connectors/project.template.json` e preencher:

| Campo obrigatório | O que colocar |
|---|---|
| `title` | Nome exato da obra |
| `media_type` | `"game"` / `"film"` / `"series"` |
| `source_language` | `"en"` (ou `"ja"`, etc.) |
| `target_language` | `"pt-BR"` |
| `connector.type` | `"hex_binary"` (jogos antigos) / `"subtitle_file"` / `"unknown"` |
| `connector.source_binary` | Caminho relativo ao artefato (ex: `"artifacts/DIALOG.BIN"`) |

Deixar como `"TBD"` qualquer campo que depende do mapeamento do Passo 00.

### 1. Mapear o formato (Passo 00 — Extração)

O objetivo é entender **como o texto está guardado** no binário antes de escrever qualquer código.

1. Abrir o binário no HxD (ou similar) e localizar strings reconhecíveis.
2. Documentar em `connector/table_schema.md`: charset, encoding, terminadores, tokens de controle.
3. Identificar a estratégia de ponteiros: inline, tabela central, ou nenhum.
4. Preencher `connector.control_codes` e `connector.pointer_table` no `project.json`.

Referência: `projects/utawarerumono/connector/table_schema.md` e `framework/connectors/hex_binary.md`.

### 2. Escrever extract.py

Adaptar `framework/connectors/_skeleton/extract.py` ao formato mapeado.

Critério de conclusão: `extract.py <binário>` gera `artifacts/dialogs.csv` com colunas `offset`, `text_en`, `byte_budget`.

### 2b. Dividir em cenas

`run_scene`/`build_plan_chapter` exigem `artifacts/scenes/<cena>/dialogs.csv` (`paths.py`, contrato
congelado) — o `dialogs.csv` flat do passo anterior **não** é lido pelo runtime de tradução, só serve
de corpus bruto. Se o corpus tiver uma coluna que já identifica a cena 1:1 (ex.: `file` — 1
arquivo-fonte = 1 cena, padrão do BoF4 e do Trails Sky SC):

```
python framework/runtime/split_scenes.py <projeto> [--by file] [--dry-run]
```

Projetos com regra de agrupamento diferente (offset com prefixo de cena embutido, corpus sem coluna
de cena) continuam exigindo split manual/específico — a ferramenta cobre só o caso comum.

### 3. Validar o round-trip (gate obrigatório)

```
python connector/extract.py artifacts/<BINARIO>
python connector/reinsert.py artifacts/dialogs.csv   # sem traduzir nada
diff <original> output/<BINARIO>                      # deve ser vazio
```

**Se não for byte-idêntico: PARAR. O conector está perdendo informação.**

Rodar os testes de contrato:

```
pytest connector/test_roundtrip.py -v
```

### 4. Escrever reinsert.py

Adaptar `framework/connectors/_skeleton/reinsert.py`. O script deve:
- Implementar a cascata direct (in-place) → repoint (shift-left) → trimmed (relocação) → residue (resíduo LLM).
- Gravar em `output/` sem modificar `artifacts/`.
- Sair com código 0 (sucesso), 1 (erro fatal) ou 3 (overflow irredutível — resíduo necessário).

### 5. Preencher os perfis

- `voice_profiles_reference.md`: registrar o que já se sabe dos personagens (pode ser stub inicial).
- `terminology_seeds.md`: termos canônicos do universo que precisam de handling rule.
- `identity_pairs_reference.md`: pares de identidade dupla (se houver).

### 6. Rodar os testes de contrato

```
pytest connector/test_roundtrip.py -v
```

Os testes do skeleton verificam:
- Round-trip byte-idêntico
- Nenhum texto da obra hardcoded nos `.py` do conector
- Nenhum caminho de input hardcoded

---

## Checklist de gate antes de traduzir

- [ ] `project.json` preenchido (sem `"TBD"` nos campos de conector)
- [ ] `dialogs.csv` gerado e com offset, texto e byte_budget
- [ ] Round-trip byte-idêntico confirmado
- [ ] `pytest connector/test_roundtrip.py` verde
- [ ] `profile/voice_profiles_reference.md` com ao menos os personagens principais
- [ ] `profile/terminology_seeds.md` com os termos críticos do universo

Só após todos os itens acima: iniciar o Passo 01 (Descoberta de Entidades).

---

## Questões do piloto multi-game — respondidas pela Fase D + Souldiers

> Três engines distintos validados (Aquaplus, Capcom DAT, Unity Addressables) responderam as
> questões abaixo na prática.

1. ~~**Família de engine:** o conector de um jogo é reutilizável para outros jogos do mesmo engine?~~
   → **Sim, via `connector_registry.json` (Fase D1): engine idêntica reusa o conector de referência
   direto; engine variante reclassifica como desconhecida e gera candidato novo.**
2. ~~**Versionamento do conector:** como lidar com mudanças no conector após cenas já traduzidas?~~
   → **`connector_manifest.json` por projeto (Fase D3, `fingerprint_monitor.py`): fingerprint dos
   scripts do conector + dos arquivos-fonte do jogo; detecta patch do jogo e drift de script.**
3. ~~**TM compartilhada:** faz sentido compartilhar TM entre jogos da mesma série/engine?~~
   → **Sim, `tm/<série>.json` (Fase D4, `tm_lookup.py`/`tm_updater.py`): declarada via
   `project.json["series"]`, isolamento estrutural entre franquias diferentes.**
