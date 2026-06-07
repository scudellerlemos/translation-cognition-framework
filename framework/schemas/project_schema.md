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
| `source_binary` | string | ✅ p/ `hex_binary` | Caminho do binário fornecido pelo usuário (CLI ou este campo; nunca hardcoded no script) |
| `table_schema` | string | ✅ p/ `hex_binary` | Caminho do schema de tabela compartilhado |
| `extract_script` | string | ✅ p/ `hex_binary` | Caminho do `extract.py` da instância |
| `reinsert_script` | string | ✅ p/ `hex_binary` | Caminho do `reinsert.py` da instância |
| `encoding` | string | — | `custom` / `ascii` / `shift-jis` / ... |
| `control_codes` | object | — | Mapa token → bytes (deve cobrir os `formatting_tokens`) |
| `pointer_table` | object | — | `{ location, format }` da tabela de ponteiros |
| `space_strategy` | enum | ✅ p/ `hex_binary` | `in_place` (cabe em bytes) / `repoint` (recalcula ponteiros). **Prefira `repoint` p/ alvo mais longo/multibyte** (ex: pt-BR). |
| `patch_format` | enum | ✅ p/ `hex_binary` | `ips` / `bps` / `xdelta` |
| `target_charset_supported` | enum | — | `true` / `false` / `likely` / `unknown` — veredito do gate de charset (ver `00_extraction.md`) |
| `charset_note` | string | — | Observação do gate de charset (glifos confirmados, ação pendente) |

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
    "source_binary": "artifacts/game_text.bin",
    "table_schema": "connector/table_schema.md",
    "extract_script": "connector/extract.py",
    "reinsert_script": "connector/reinsert.py",
    "encoding": "custom",
    "control_codes": { "{W75}": "0x..", "{END}": "0x.." },
    "pointer_table": { "location": "0x..", "format": "le-16" },
    "space_strategy": "in_place",
    "patch_format": "ips",
    "target_charset_supported": false
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
