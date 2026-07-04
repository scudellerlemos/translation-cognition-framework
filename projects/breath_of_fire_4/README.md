# Breath of Fire IV — Tradução PT-BR

> Framework SDD — segunda instância. Piloto de portabilidade multi-engine.
> Status: **CICLO DE TRADUÇÃO COMPLETO**

## O que é este projeto

Tradução EN→PT-BR de Breath of Fire IV (PC port, Capcom, 2000) usando o
Translation Cognition Framework (SDD). Esta é a segunda instância do framework —
objetivo principal: validar a portabilidade para um engine Capcom diferente do
Aquaplus/SDAT usado no Utawarerumono.

---

## Status — junho 2026

### Objetivos alcançados

- Conector Capcom DAT: extração + reinserção + round-trip byte-idêntico ✅
- Pipeline completo (Fases 00–08): KB, glossário, planejamento, tradução, QA, reinserção ✅
- **125 cenas (AREAD + AREAS), todas `verified`** — round-trip byte-idêntico, back-translation de alto risco ✅
- 125 DAT files em `output/`, 0 overflows ✅
- QA humana concluída ✅
- Validação in-game: OK ✅
- Custo: **~$11,04 USD** (Haiku $6,04 · Opus $2,61 · Sonnet $2,40)

### Dívidas e débitos técnicos

| Item | Tipo |
|---|---|
| TM busca semântica (B2: `paraphrase-multilingual-MiniLM-L12-v2` local) — não implementada | débito técnico |

### Próximos passos

1. TM semântica (B2) — quando corpus multi-game justificar

---

## Estrutura

```
project.json              ← configuração central (formato Capcom DAT mapeado)
connector/
  table_schema.md         ← formato Capcom DAT TOC documentado
  extract.py              ← implementado; gera artifacts/dialogs.csv
  reinsert.py             ← implementado; round-trip byte-idêntico green
  test_roundtrip.py       ← 10/10 passando (pytest --dat-dir <english/DAT>)
  conftest.py             ← opção --dat-dir para pytest
profile/
  voice_profiles_reference.md    ← perfis dos personagens principais
  identity_pairs_reference.md    ← par Ryu↔Fou-Lu documentado
  terminology_seeds.md           ← seeds de glossário
  example_test_suites.md         ← suites de teste sintético
artifacts/
  dialogs.csv             ← 23582 strings de 264 arquivos (AREAD/AREAS)
  entities.csv, glossary.csv, research_log.md, tone_analysis.md ← artefatos do pipeline
  translation_memory.jsonl ← TM gerada (append-only)
  run_state.json          ← 125/125 cenas verified
  api_ledger.jsonl        ← ledger de custo auditável
  qa_revisao/             ← XLSX de revisão humana (gerado + revisado)
output/                   ← 125 DAT files traduzidos e reinseridos
```

## Questões abertas (piloto multi-game)

Ver [ROADMAP.md raiz](../../ROADMAP.md). As 4 questões (família de engine,
versionamento do conector, onboarding mínimo, TM compartilhada) foram parcialmente
respondidas por este piloto — a TM semântica (B2) é a questão principal em aberto
para o reuso cross-game.
