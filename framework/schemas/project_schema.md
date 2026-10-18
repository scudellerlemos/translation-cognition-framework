# SCHEMA DO PROJETO — Referência Formal
## Definição do `project.json` e dos arquivos de perfil de uma instância

> **Propósito:** este documento define o manifesto que cada projeto (`/projects/<título>/`)
> deve fornecer ao framework. As skills genéricas leem o `project.json` para resolver tudo
> que é específico do título (idiomas, tokens, formato de fonte, limites).

---

## `project.json`

| Campo | Tipo | Obrigatório | Valores / Descrição |
|-------|------|-------------|---------------------|
| `title` | string | ✅ | Nome da obra |
| `media_type` | enum | ✅ | `game` / `film` / `series` |
| `media_profile` | string | ✅ | Nome do perfil em `framework/media-profiles/` (ex: `games`) |
| `source_language` | string | ✅ | Código BCP-47 do idioma-fonte (ex: `en`, `ja`) |
| `target_language` | string | ✅ | Código BCP-47 do idioma-alvo (ex: `pt-BR`) |
| `source` | object | ✅ | Descrição da fonte (ver abaixo) |
| `connector` | object | ✅ p/ meios binários | Configuração da extração/reinserção (ver abaixo) |
| `formatting_tokens` | array[string] | ✅ p/ `game` | Tokens de engine a preservar exatamente |
| `system_line_convention` | enum/string | — | Como detectar texto de sistema (ex: `all_caps`, `none`) |
| `length_constraints` | object | — | Limites de comprimento (ver abaixo) |
| `batch_size` | int | — | Linhas por lote de tradução (default 200) |
| `formatting_token_patterns` | array[string] | — | Regex dos tokens estruturais (ex: `\[([0-9A-Fa-f]{2})\]`); somam-se a `formatting_tokens` (lido por `context_pack`/`connector_io`) |
| `line_width` | string | — | `"derive"`: limite de largura de linha = maior segmento visível do texto-fonte entre quebras de caixa (`box_width.py`). Sem `line_width`/`line_width_max`: 62 |
| `line_width_max` | int | — | Limite fixo de largura de linha (vence o `derive`) |
| `byte_budget_exceptions` | object | — | `{offset: novo_budget}` — exceção pontual de orçamento de bytes decidida pelo humano (`budget.effective_budget`) |
| `image_labels` | object | — | Inventário de rótulos em imagem (tabelas `[y, x0, x1, original, candidatas…]`, chave `principal` etc.); lido pelo conector da instância (ver `08b_system_text_labels.md`) |
| `system_scenes` | array[string] | — | Cenas de texto de sistema (escopo `completo`); só caminho de sessão (`run_scene`) |
| `extraction_scope` | string | — | Escopo da extração (`dialogo` por padrão; `completo` inclui texto de sistema) |
| `kb_frontier` | string | — | `scene_id` máximo coberto pela pesquisa de KB; o `kb_gate` bloqueia cenas além dela |
| `series` | string | — | Série para a TM compartilhada (`tm_lookup`); sem o campo = slug do título |
| `hitl` | bool | — | `true` liga os pontos de humano no laço (`hitl.py`) |
| `budget.max_usd_per_wave` | número | — | teto de gasto (USD) por onda do `wave.py`; `--max-usd` na linha de comando vence; sem a chave, sem teto |
| `rag_min_score` | float | — | Score mínimo p/ hits da TM semântica no pacote de contexto; `null`/ausente = sem corte (default) |
| `profile` | object | — | Caminhos para os arquivos de perfil curado (ver abaixo) |
| `notes` | string | — | Observações livres sobre o título |

### `source` (object)

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `file` | string | ✅ | Caminho relativo ao corpus-fonte |
| `format` | enum | ✅ | `csv_offset` / `srt` / `ass` / outro definido pelo media-profile |
| `id_column` | string | ✅ p/ formatos tabulares | Coluna âncora de identidade (ex: `offset`) |
| `text_column` | string | ✅ p/ formatos tabulares | Coluna do texto-fonte |

### `connector` (object)

Configura a camada de I/O que extrai/reinsere texto no meio (ver `framework/connectors/`).
Obrigatório quando a fonte é um meio binário (jogos antigos). Para meios já textuais (CSV pronto,
legendas), pode ser omitido ou simplificado.

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `type` | string | ✅ | Tipo de conector (ex: `hex_binary`) — corresponde a `framework/connectors/<type>.md` |
| `source_binary` | string | ✅ p/ `hex_binary` | Caminho do binário que **o usuário entrega** — **relativo à raiz do projeto** (arquivo copiado para `artifacts/`) **ou** fornecido como **argumento de CLI** no runtime. **Nunca** um caminho absoluto/externo persistido na config (governança: o usuário fornece o binário; nunca hardcoded no script) |
| `container_format` | string | — | Formato do pacote quando a fonte está **empacotada** (ex: `sdat`). Omitir ou `none` se for binário direto. Para pacote editável em hex no lugar, é metadado informativo (proveniência). |
| `inner_path` | string | — | Arquivo de diálogo **dentro** do pacote (quando `container_format` ≠ `none`). |
| `table_schema` | string | ✅ p/ `hex_binary` | Caminho do schema de tabela compartilhado |
| `extract_script` | string | ✅ p/ `hex_binary` | Caminho do `extract.py` da instância |
| `reinsert_script` | string | ✅ p/ `hex_binary` | Caminho do `reinsert.py` da instância |
| `encoding` | string | — | `custom` / `ascii` / `shift-jis` / ... |
| `control_codes` | object | — | Tabela de opcodes (deve cobrir os `formatting_tokens`): chave = código hex (`"01"`), valor = nome curto **ou** objeto `{name, params, width, values}` (ver abaixo; `opcodes.py`) |
| `budget_reserves_terminator` | bool | — | O `byte_budget` já reserva 1 byte para o terminador (default `false`; `budget.usable`) |
| `pointer_table` | object | — | `{ location, format }` da tabela de ponteiros |
| `space_strategy` | enum | ✅ p/ `hex_binary` | `in_place` (cabe em bytes) / `repoint` (recalcula ponteiros). **Prefira `repoint` p/ alvo mais longo/multibyte** (ex: pt-BR). |
| `patch_format` | enum | ✅ p/ `hex_binary` | `ips` / `bps` / `xdelta` |
| `target_charset_supported` | enum | — | `true` / `false` / `likely` / `unknown` — veredito do gate de charset (ver `00_extraction.md`) |
| `charset_note` | string | — | Observação do gate de charset (glifos confirmados, ação pendente) |

#### `control_codes` — valor em forma de objeto

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `name` | string | `""` | Papel do código. `newline`, `page_break` e `choice_start` (abre o menu) **quebram a caixa**; qualquer outro nome não quebra |
| `params` | int | 0 | Quantos tokens `[xx]` seguintes são parâmetro deste código (não são códigos nem quebram) |
| `width` | int | 0 | Glifos que o código exibe na tela (variável como número/nome) |
| `values` | array[string] | `[]` | Valores possíveis do parâmetro (documenta e valida); vazio = livre |

### `length_constraints` (object)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `mode` | enum | `percent` | `percent` (% do fonte) / `byte_space` (limite em bytes; usar quando `connector.space_strategy: in_place`) |
| `dialogue_max_pct` | int | 140 | Comprimento máximo do segmento traduzido como % do fonte (modo `percent`) |
| `ui_max_pct` | int | 110 | Idem para linhas de UI/sistema (modo `percent`) |

> No modo `byte_space`, o limite real por linha é o `byte_budget` extraído no Passo 00 — não uma %.

### `profile` (object)

Mapa de chaves → caminhos para os arquivos de perfil curado da instância. Chaves convencionais:
`voice_profiles`, `identity_pairs`, `terminology_seeds`, `example_test_suites`. Todas opcionais —
no pipeline real o conteúdo equivalente é produzido como artefato gerado; o perfil curado serve de
referência/semente.

---

## Exemplo válido (Utawarerumono)

```json
{
  "title": "Utawarerumono: Mask of Deception",
  "media_type": "game",
  "media_profile": "games",
  "source_language": "en",
  "target_language": "pt-BR",
  "source": {
    "file": "artifacts/dialogs.csv",
    "format": "csv_offset",
    "id_column": "offset",
    "text_column": "text_en"
  },
  "formatting_tokens": ["{W75}", "{W80}", "{W10}", "{COLOR}", "{END}"],
  "system_line_convention": "all_caps",
  "length_constraints": { "mode": "byte_space", "dialogue_max_pct": 140, "ui_max_pct": 110 },
  "batch_size": 200,
  "connector": {
    "type": "hex_binary",
    "source_binary": "artifacts/ScriptEvent.sdat",
    "container_format": "sdat",
    "table_schema": "connector/table_schema.md",
    "extract_script": "connector/extract.py",
    "reinsert_script": "connector/reinsert.py",
    "encoding": "custom",
    "control_codes": { "{W75}": "0x..", "{END}": "0x.." },
    "pointer_table": { "location": "0x..", "format": "le-16" },
    "space_strategy": "repoint",
    "patch_format": "ips",
    "target_charset_supported": "likely"
  }
}
```

---

## Invariantes

- `media_profile` deve corresponder a um arquivo existente em `framework/media-profiles/`.
- `source.file` é resolvido **relativo à raiz do projeto** (`/projects/<título>/`).
- O corpus em `source.file` é **somente leitura** (invariante global do processo).
- O `source.file` é **output do Passo 00** (extração) quando há `connector` — não é dado pré-existente.
- `source_language` ≠ `target_language`.
- Para `media_type: game`, `formatting_tokens` deve estar presente (pode ser lista vazia se o engine não usa tokens).
- `connector.type` deve corresponder a um arquivo em `framework/connectors/`.
- A **localização real da fonte** (ex: pasta de instalação da Steam) é **orientação ao humano e proveniência** — registrada no `extraction_log.md` — e **nunca** um caminho de input. `connector.source_binary` é **relativo à raiz** (arquivo entregue em `artifacts/`) ou vem por **CLI**; jamais um caminho absoluto/externo persistido na config.
- Quando `connector.container_format` ≠ `none`, `connector.inner_path` deve estar declarado.
- `connector.control_codes` deve cobrir todos os `formatting_tokens`.
- Quando `connector.space_strategy: in_place`, `length_constraints.mode` deve ser `byte_space`.
- `extract.py` e `reinsert.py` devem compartilhar o mesmo `table_schema` (garantia de round-trip).
- A saída do Passo 08 vai para `projects/<título>/output/<nome-original>` (mesmo nome e extensão do `source_binary`).
- A tradução é aplicada de `approved_translations.csv` pelo script — a IA não escreve a tradução à mão nos dados.

---

## Arquivos de Perfil Curado (`profile/*.md`)

São markdown legível, específicos do título. Não têm schema rígido de campos, mas seguem convenções:

- **voice_profiles:** uma seção por personagem, com `voice_criticality` (high/medium/low), registro, características, red flags. Consumido por 05b/06/06b/07.
- **identity_pairs:** tabela de pares (persona pública ⟷ identidade revelada), `spoiler_level`, contraste de voz, regras de separação. Consumido por 05/05b/07.
- **terminology_seeds:** decisões `handling_rule`, formas exatas obrigatórias, fases narrativas. Alimenta `glossary.csv` (04) e o QA Final (07).
- **example_test_suites:** instância concreta das suites de teste sintético. Exemplifica o Passo 5b.
