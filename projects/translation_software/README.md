# Translation Software — shell DB-only de validação

> Status: **referência de arquitetura do modo banco** — não é um projeto de tradução em andamento.

Esta pasta só tem o [`project.json`](project.json). Ele aponta para o conector, o perfil e o
`dialogs.csv` do [BoF4](../breath_of_fire_4/README.md) e declara `db`, o que liga o modo SQLite do
framework. Serve para validar o `Store` (`framework/db/`) e o RAG semântico com um corpus real
(BoF4 migrado: 125 cenas / 6046 linhas) sem tocar no projeto original, que segue em flat files.

## Regenerar o banco

O `translation_software.db` não é versionado. Para recriá-lo a partir dos flat files do BoF4:

```
tcf db migrate projects/breath_of_fire_4 projects/translation_software/translation_software.db
pip install -r requirements-ml.txt        # só se for usar a busca semântica
tcf db index projects/translation_software/translation_software.db bof4
```

## Onde está o resto

- Histórico e estado da migração flat → DB (Fases 1–6): [`docs/DB_MIGRATION_ROADMAP.md`](../../docs/DB_MIGRATION_ROADMAP.md)
- Persistência e stack: [`docs/STACK.md`](../../docs/STACK.md)
- Arquitetura do RAG: [`docs/RAG_ARCHITECTURE.md`](../../docs/RAG_ARCHITECTURE.md)
