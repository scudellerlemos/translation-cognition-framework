# Souldiers — Tradução PT-BR

> Framework SDD — terceira instância. Piloto de engine Unity Addressables + onboarding de baixo custo.
> Status: **CICLO DE TRADUÇÃO COMPLETO**

## O que é este projeto

Tradução EN→PT-BR de Souldiers (Retro Forge / Dear Villagers, Unity), usando o Translation
Cognition Framework (SDD). Terceira instância do framework — objetivos principais: validar a
portabilidade para engine Unity Addressables (bem diferente de Aquaplus/SDAT e Capcom DAT) e
exercitar o pipeline de onboarding de baixo custo (P1.7) numa estrutura de projeto **flat**
(sem capítulos numerados, ao contrário de Utawarerumono/BoF4).

---

## Status — julho 2026

### Objetivos alcançados

- Conector Unity Addressables: extração + reinserção + round-trip byte-idêntico ✅
  (3 tabelas CSV tilde-delimited embutidas em `TextAsset` dentro de bundles: `texts_DIALOGS`,
  `texts_INGAME_DIALOGS`, `texts_SIDE_DIALOGS` — a última usa coluna `::BR::`, não `::PT::`)
- **470/470 cenas verified** — round-trip byte-idêntico, 100% cobertura de back-translation ✅
- KB reconstruída a partir de material já pesquisado (decision_log, tone_analysis, terminology
  seeds) + evidência real do corpus; 22 entidades UNSOURCED resolvidas (fonte ou verbatim) ✅
- Batch API (−50%) segmentado em pacotes menores (translate + back-translation) — mitiga o risco
  de 1 batch gigante "parecer travado" sem sinal confiável de progresso durante `in_progress` ✅
- Custo: **~$3,06 USD**
- Revisão humana (XLSX) disponibilizada em `artifacts/qa_revisao/para_revisar/` — aplicação
  (`quality_review.py apply`) pendente de priorização humana, não é débito técnico do framework

### Dívidas e débitos técnicos

Nenhum aberto do lado do framework — P1.7 (onboarding), P2.5, D6, Fase D completa e B2-B4
foram fechados nesta mesma janela de trabalho, todos com testes e revisão independente.
A única pendência é operacional: revisão humana do XLSX de QA (fora do escopo do framework).

**Risco aceito e documentado (não é lacuna esquecida):** o round-trip byte-idêntico do bundle
Unity real (`test_roundtrip.py`, 6/6 acima) só roda localmente com `--data-dir` apontando pro jogo
instalado — nunca na CI, que faz `pytest.skip`. Diferente de BoF4/Utawarerumono (formato binário
próprio, sintetizável em memória), o container aqui é UnityFS lido só via UnityPy, que não expõe
API pra construir um bundle do zero (`SerializedFile`/`BundleFile.__init__` exigem um
`EndianBinaryReader` de bytes já existentes) — replicar isso exigiria reimplementar o formato
UnityFS à mão. Decisão consciente de custo-benefício, não descoberta agora: a CI sempre roda
`test_rebuild_table_logic.py` (lógica de reescrita do CSV interno — onde bugs reais de tradução
aconteceriam), cobrindo a superfície de risco que é código nosso; a serialização do container em
si fica por conta do UnityPy (dependência de terceiros, não nosso código). Ver ADR 0011.
Nota lateral: `UnityPy` ainda não está em nenhum `requirements-*.txt` — inofensivo hoje porque
nenhum caminho testado em CI o importa, mas quebraria se o skip acima for removido sem adicionar
a dependência.

---

## Estrutura

```
project.json              ← configuração central (formato Unity Addressables mapeado)
connector/
  table_schema.md         ← formato das 3 tabelas de diálogo documentado
  extract.py               ← implementado; gera artifacts/dialogs.csv (global)
  reinsert.py               ← rebuild_table() por tabela; fast-path byte-idêntico quando sem tradução
  build_plan_chapter.py     ← valida cobertura + tokens de timing/tags TMP por cena
  verify_chapter.py         ← round-trip + apply + readback; protocolo exit 0/1/3 + VERIFY_STATUS
  split_scenes.py           ← agrupa o dialogs.csv global em cenas (AREAD/INGAME por área)
  test_roundtrip.py         ← 6/6 passando (pytest --data-dir <StreamingAssets/aa/StandaloneWindows64>)
  conftest.py               ← opção --data-dir para pytest
artifacts/
  dialogs.csv              ← corpus global (offset, text_en, byte_budget, table)
  entities.csv, glossary.csv, research_log.md, tone_analysis.md, universe_knowledge_base.md
  scenes/                  ← 470 cenas verified (translations_*.json, translation_plan_*.json, ...)
  state/translation_memory.jsonl ← TM gerada (append-only)
  run_state.json           ← 470/470 cenas verified
  api_ledger.jsonl         ← ledger de custo auditável
  qa_revisao/              ← XLSX de revisão humana (gerado, aguardando aplicação)
```

## Questões abertas (piloto multi-game)

Ver [ROADMAP.md raiz](../../docs/ROADMAP.md). Este piloto fechou a Fase D inteira (Generic Connector
System) e validou o terceiro engine distinto — as questões de família de engine, versionamento,
onboarding e TM compartilhada da discussão multi-game já têm resposta prática nos módulos
`tier_classifier.py`/`fingerprint_monitor.py`/`scaffold_project.py`/`tm_lookup.py`.
