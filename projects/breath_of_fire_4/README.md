# Breath of Fire IV — Tradução PT-BR

> Framework SDD — segunda instância. Piloto de portabilidade multi-engine.
> Status: **FASE 01 — PIPELINE COGNITIVO (passo 1.1 pendente)**

## O que é este projeto

Tradução EN→PT-BR de Breath of Fire IV (PC port, Capcom, 2000) usando o
Translation Cognition Framework (SDD). Esta é a segunda instância do framework —
o objetivo principal é validar a portabilidade para um engine Capcom diferente do
Aquaplus/SDAT usado no Utawarerumono.

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
  voice_profiles_reference.md    ← perfis preliminares dos 6 personagens principais
  identity_pairs_reference.md    ← par Ryu↔Fou-Lu documentado
  terminology_seeds.md           ← seeds de glossário
  example_test_suites.md         ← stub (preencher no Passo 05b)
artifacts/
  dialogs.csv             ← 23582 strings de 264 arquivos (AREAD/AREAS/AREAE/AREAM/UI)
output/                   ← vazio até reinserção (Passo 08)
```

## Próximo passo

1. **Passo 1.1 — Descoberta de Entidades**: varrer `dialogs.csv`, listar personagens/locais/termos únicos
2. Passo 1.2 — Resolução de Entidades (nomes canônicos pt-BR)
3. Passo 1.3 — Knowledge Building (pesquisa de lore + ratificação humana)

## Questões abertas (piloto multi-game)

Ver [ROADMAP.md raiz](../../ROADMAP.md). As 4 questões (família de engine,
versionamento do conector, onboarding mínimo, TM compartilhada) serão respondidas
à medida que este projeto avança.
