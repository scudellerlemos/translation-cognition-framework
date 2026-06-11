# Convenção de nomes — código e artefatos

> Por que este doc existe: o framework cresceu com nomes abreviados/crípticos que dificultavam a
> manutenção (`sfx`, `fase0`…). Esta convenção fixa as regras e — o mais importante — documenta o
> **contrato estável** (nomes que NÃO podem ser renomeados sem migração) que antes só vivia na cabeça
> de quem escreveu. Vale para `framework/` e para os `projects/<obra>/`.

## 1. Idioma

- **Identificadores de código (módulos, funções, variáveis, chaves) em INGLÊS.** O framework é
  genérico/neutro de idioma (ver `framework/README.md`): nenhum nome de personagem, termo de lore ou
  idioma-alvo vive em `framework/`. Inglês mantém o código portável entre obras e pares de idioma.
- **Comentários e docstrings em pt-BR** (house style do projeto). É onde o "porquê" é explicado.
- **Conteúdo de obra** (diálogo, tradução) NUNCA aparece hardcoded em `.py` — vem dos artefatos
  (travado pelo teste `test_no_work_text_in_runtime_scripts`).

## 2. Clareza > brevidade

- **Sem abreviações não-explicadas.** Prefira o nome por extenso: `scene_id` (não `sfx`),
  `build_plan_script` (não `bp`), `verify_script` (não `vf`).
- Aliases de import curtos são tolerados quando idiomáticos e locais ao módulo: `import model as M`,
  `import run_scene as RS`. Não invente abreviação nova fora desse padrão.
- Nome de arquivo de módulo = comando CLI (ver §4): escolha um nome auto-explicativo em inglês
  (`kb_phase.py`, não `fase0.py`).

## 3. Glossário de abreviações ACEITAS

Estas são as ÚNICAS abreviações permitidas sem escrever por extenso (são jargão estabelecido do
domínio). Qualquer outra deve ser expandida.

| Sigla | Significado | Onde aparece |
|---|---|---|
| `KB` | Knowledge Base (base de conhecimento reconciliada) | `kb_gate.py`, `kb_phase.py`, `kb_frontier` |
| `TM` | Translation Memory (memória de tradução) | `tm_exact`, `tm_voice`, `translation_memory.jsonl` |
| `QA` | Quality Assurance | skills 06b/07, `qa_report.md` |
| `BIN` / `SDAT` | formatos de container binário do jogo | conector (`sdat_format.py`) |
| `T4` | Tier 4 do cascade de reinserção (resíduo que exige cognição) | `t4_residue.json`, skill 08 |
| `scene_id` | id da cena (ex.: `12_03`), derivado de `ch_12_03` por `scene_id_of()` | todo o runtime |

## 4. Contrato CONGELADO (APIs estáveis — NÃO renomear sem migração)

Estes nomes são **load-bearing**: há dados em disco, comandos que usuários digitam e config que o
runtime lê. Renomear quebra os capítulos já traduzidos (11–13) e/ou scripts/documentação. Mudança aqui
exige script de migração + revalidação de round-trip — não é um "rename de clareza".

**a) Nomes de artefato persistidos** (gerados/consumidos entre execuções):
`dialogs.csv`, `glossary.csv`, `entities.csv`, `translations_<scene_id>.json`,
`translation_plan_<scene_id>.json`, `back_translation_<scene_id>.json`, `approved_<scene_id>.csv`,
`pack.json`, `scene_prompt.md`, `run_state.json`, `api_ledger.jsonl`, `metrics.jsonl`,
`translation_memory.jsonl`, `voice_cards.json`, `decision_index.json`, `spoiler_ledger.json`,
`research_log.md`, `universe_knowledge_base.md`, `tone_analysis.md`.
> O **infixo** `<scene_id>` é o VALOR (ex.: `12_03`), não o nome da variável — renomear a variável
> `scene_id` no código NÃO muda o nome do arquivo gerado.

**b) Comandos CLI** (caminho do módulo = comando que o usuário roda):
`context_pack.py`, `state_index.py`, `model.py`, `run_scene.py`, `run_chapter.py`, `kb_gate.py`,
`kb_phase.py`, `cost_report.py`, e os conectores `build_plan_chapter.py` / `verify_chapter.py`.

**c) Chaves de `project.json`:**
`connector.build_plan_script`, `connector.verify_script`, `kb_frontier`, `formatting_tokens`,
`system_line_convention`, `length_constraints`, `target_charset_supported`, e o resto de `connector`.

## 5. O que É seguro renomear (clareza interna)

- Variáveis e funções **internas** (`_`-prefixadas ou não exportadas), desde que TODOS os call sites
  do repo sejam atualizados juntos. Ex.: `sfx`→`scene_id`, `sfx_of`→`scene_id_of` (feito).
- Chaves de dicionário que são **contrato interno entre dois módulos** e cujo arquivo em disco é
  **regenerado** a cada run (ex.: a chave `scene_id` do `pack.json`) — não são estado durável.
- Comentários/docstrings, sempre.

Regra de ouro: rodar `pytest framework/runtime/test_runtime.py` (determinismo + idempotência + guard de
work-text) DEPOIS de qualquer rename. Verde = seguro.
