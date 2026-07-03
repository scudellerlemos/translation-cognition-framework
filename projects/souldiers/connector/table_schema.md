# Table Schema — Souldiers

> Status: MAPEADO — 2026-07-02 (confirmado rodando round-trip real contra o jogo instalado)

## Engine detectado

Unity 2021 (Mono), Addressables 1.x (Forge Reply, 2022). Texto de diálogo vive em 3
`TextAsset` dentro de 3 AssetBundles, cada `TextAsset.m_Script` é um **CSV tilde-delimitado**
completo (multi-idioma), não um binário customizado.

## Bundles / tabelas

| Tabela | Bundle | Escopo |
|---|---|---|
| `texts_DIALOGS` | `8bbb65e6bcd747af3bbead6db0716968.bundle` | diálogo de cena/área principal |
| `texts_INGAME_DIALOGS` | `8d47b47a21c47126bf303e267a66fc73.bundle` | diálogo in-game curto |
| `texts_SIDE_DIALOGS` | `a77305a96d09041b74e5948e4f67851e.bundle` | diálogo de conteúdo secundário |

## Formato de string

`m_Script` é **`str`** (não `bytes`) nas 3 tabelas neste jogo — escrever de volta como `bytes`
via `.encode()` incondicional quebra o TypeTree writer do UnityPy (`AttributeError` na leitura de
alignment). `reinsert.rebuild_table()` preserva o tipo lido (`was_bytes` flag) antes de gravar.

CSV interno: delimitador `~`, todos os campos quoted (`QUOTE_ALL`), coluna de ID = `::ID::`,
coluna fonte = `::EN::`.

**Coluna de destino pt-BR NÃO é uniforme** (achado real, não estava documentado antes):

| Tabela | Coluna pt-BR |
|---|---|
| `texts_DIALOGS` | `::PT::` |
| `texts_INGAME_DIALOGS` | `::PT::` |
| `texts_SIDE_DIALOGS` | `::BR::` (não tem `::PT::`; `::BR::` é mais correto pra pt-BR mesmo) |

Mapeamento vive em `connector/reinsert.py:_PT_COL_BY_TABLE` — não usar um `target_column` único.

## Pointer table

N/A — não há tabela de ponteiros/offsets binários. Cada linha é identificada por `::ID::`
(string, ex.: `STR_DIALOGS_CAVE_23_D1_BALOF_1`); reconstrução é reescrita do CSV inteiro dentro
do `TextAsset`, não patch de bytes pontual.

## Encoding

UTF-8. Sem restrição de charset conhecida (TextMeshPro renderiza acentuação pt-BR nativamente).

## Grão de round-trip

**Tabela inteira (bundle), não cena.** `reinsert.py` reescreve os 3 bundles inteiros a partir de
um CSV global de aprovados — diferente do BoF4 (arquivo DAT por cena). `verify_chapter.py`
verifica round-trip por tabela tocada pela cena; `test_roundtrip.py` testa as 3 tabelas direto,
sem depender de nenhuma cena específica.
