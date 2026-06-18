# Onboarding — Novo Projeto de Tradução

> Guia passo a passo para instanciar um projeto no framework SDD.
> Criado após o piloto Utawarerumono (jun/2026) — primeira validação multi-game.

---

## Pré-requisitos

- Você tem o binário (ou arquivo de texto/legenda) da obra-fonte.
- A branch de trabalho está criada.
- O framework está em `framework/` e os testes passam (`pytest framework/`).

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
- Implementar a cascata T1 (in-place) → T2 (shift-left) → T3 (relocação) → T4 (resíduo LLM).
- Gravar em `output/` sem modificar `artifacts/`.
- Sair com código 0 (sucesso), 1 (erro fatal) ou 3 (overflow irredutível — T4 necessário).

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

## Questões abertas para o piloto multi-game

> Registradas em `memory/connector-multi-game-future.md`. A responder à medida que o piloto avança.

1. **Família de engine:** o conector do jogo 2 é reutilizável para outros jogos Capcom PS1?
2. **Versionamento do conector:** como lidar com mudanças no conector após cenas já traduzidas?
3. **TM compartilhada:** faz sentido compartilhar TM entre jogos da mesma série/engine?
