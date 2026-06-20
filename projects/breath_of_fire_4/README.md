# Breath of Fire IV — Tradução PT-BR

> Framework SDD — segunda instância. Piloto de portabilidade multi-engine.
> Status: **FASE 00 — MAPEAMENTO DO CONECTOR PENDENTE**

## O que é este projeto

Tradução EN→PT-BR de Breath of Fire IV (PC port, Capcom, 2000) usando o
Translation Cognition Framework (SDD). Esta é a segunda instância do framework —
o objetivo principal é validar a portabilidade para um engine Capcom diferente do
Aquaplus/SDAT usado no Utawarerumono.

## Pré-requisito imediato

Antes de qualquer coisa: **mapear o formato do binário de diálogo** (Passo 00).

```
connector/table_schema.md  ← preencher com charset, tokens, estrutura de ponteiros
connector/extract.py       ← implementar load_table e iter_string_offsets
```

Ver `framework/docs/NEW_PROJECT_ONBOARDING.md` para o guia completo.

## Estrutura

```
project.json              ← configuração central (campos TBD = mapeamento pendente)
connector/
  table_schema.md         ← PREENCHER no Passo 00
  extract.py              ← IMPLEMENTAR após mapeamento
  reinsert.py             ← IMPLEMENTAR após mapeamento
  test_roundtrip.py       ← 2 testes ativos (sem texto hardcoded, sem paths absolutos)
                             2 testes em skip até conector implementado
profile/
  voice_profiles_reference.md    ← perfis preliminares dos 6 personagens principais
  identity_pairs_reference.md    ← par Ryu↔Fou-Lu documentado
  terminology_seeds.md           ← seeds de glossário
  example_test_suites.md         ← stub (preencher no Passo 05b)
artifacts/                ← vazio até extração (Passo 00)
output/                   ← vazio até reinserção (Passo 08)
```

## Próximo passo

1. Fornecer o binário de diálogo em `artifacts/`
2. Analisar com HxD: localizar strings reconhecíveis, mapear charset
3. Preencher `connector/table_schema.md`
4. Implementar `extract.py` → rodar → validar round-trip
5. `pytest connector/test_roundtrip.py -v` → habilitar os testes de skip

## Questões abertas (piloto multi-game)

Ver [ROADMAP.md raiz](../../ROADMAP.md) — Fase D. As 4 questões (família de engine,
versionamento do conector, onboarding mínimo, TM compartilhada) serão respondidas
à medida que este projeto avança.
