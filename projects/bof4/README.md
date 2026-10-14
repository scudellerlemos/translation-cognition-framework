# Breath of Fire IV — Tradução PT-BR (modo banco)

> Status: **tradução em escala concluída, fechamento pendente** (2026-10-12) — 286 de 286 cenas `verified`
> (19.873 linhas). Passe de consistência (4.1) e reinserção (4.2) fechados; faltam o gate visual no jogo (4.3) e a QA humana (4.4).
> Substitui `projects/breath_of_fire_4/` (flat files), removido do repositório.

Mesma obra, mesmo conector Capcom DAT, mesma KB — mas com `db` declarado no `project.json`:
SQLite (`bof4.db`, não versionado) como store e busca semântica obrigatória (o `kb_gate` bloqueia a
tradução sem a stack de `requirements-ml.txt`).

## O que veio do projeto antigo

- `connector/` — cópia do conector de referência (o `connector_gate` não aceita script fora do projeto).
- `artifacts/dialogs.csv` e `artifacts/scenes/*/dialogs.csv` — corpus extraído (286 cenas, 19.873 linhas).
- KB e perfis: `entities.csv`, `glossary.csv`, `tone_analysis.md`, `universe_knowledge_base.md`,
  `research_log.md`, `spoiler_ledger.json`, `profile/`.

Não veio: traduções, TM, `run_state.json`, ledgers de custo e QA. A tradução começou do zero.

## Piloto — `AREAS001` (taverna de Sarai)

Rodado por `run_scene.py` com verify, sem bypass de gate: round-trip 104/104 linhas, 0 overflow,
back-translation 4/4 `pass` nas linhas de risco alto, vereditos confirmados pelo usuário. `connector_gate` e `kb_gate` verdes.

## Antes de traduzir em escala

- [x] Gate visual in-game do trajeto do piloto (OK do usuário, 2026-10-12).

O que foi feito na sessão de 2026-10-11/12 (conector, custo, observabilidade, economia do caminho da sessão) está
no "Registro da sessão" do [`ROADMAP.md`](ROADMAP.md).

Passos e ordem completos: [`ROADMAP.md`](ROADMAP.md).

## Ambiente

O verify precisa de `BOF4_DAT_DIR`. Nada carrega o `.env` sozinho — exporte antes de rodar:

```
cp .env.example .env                     # BOF4_DAT_DIR = <jogo>/english/DAT
set -a; . projects/bof4/.env; set +a     # bash; no PowerShell: $env:BOF4_DAT_DIR = "..."
pytest projects/bof4/connector/ --dat-dir "<jogo>/english/DAT"
```
