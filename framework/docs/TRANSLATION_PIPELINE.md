# Translation Pipeline — fluxo de 1 cena no harness

O `framework/runtime/run_scene.py` executa uma cena como um **job determinístico e resumível**. Esta é
a sequência, os artefatos e os pontos de retomada.

## Fluxo

```
python framework/runtime/run_scene.py <projeto> <cena> [--backend in-session|api] [--require-back] [--no-verify]

[1] context_pack   →  artifacts/<cena>/{scene_prompt.md, pack.json}     (determinístico)
[2] translate      →  artifacts/<cena>/translations_<scene_id>.json           (IA; in-session espera o arquivo)
[3] build_plan     →  artifacts/<cena>/{translation_plan_<scene_id>.json, approved_<scene_id>.csv}  (det. + valida)
[4] back_translate →  artifacts/<cena>/back_translation_<scene_id>.json        (IA; só linhas risk>=high)
[5] verify         →  round-trip byte-idêntico + ponteiros within-file    (determinístico)
[6] checkpoint     →  artifacts/run_state.json  + reconstrói artifacts/state/  (TM cresce)
```

`<scene_id>` = nome da cena sem o prefixo `ch_` (ex.: `ch_12_01` → `12_01`).

## Gates (bloqueiam o avanço)

- **[3] build_plan_chapter** valida: cobertura total, token `\n` preservado, interjeição ≠ source,
  `risk >= medium` exige `risk_notes`. Falha → `status: build_plan_failed`.
- **[4] back-translation** em `risk >= high`. Por padrão é **reportada** (não bloqueia); com
  `--require-back` bloqueia até existir `back_translation_<scene_id>.json`.
- **[5] verify_chapter** exige round-trip idêntico (approved={}), cada offset lido == approved
  transliterado, **resíduo T4 = 0**, ponteiros resolvendo dentro do arquivo. Falha → `verify_failed`.

## Checkpoint / resume (`run_state.json`)

`status` por cena: `packed` → `planned` → `verified` (ou `*_failed`, `awaiting_*`). O harness é
idempotente: rode de novo a qualquer momento; ele recomputa o pacote, reusa traduções existentes
(nunca sobrescreve) e retoma na etapa pendente. Crash entre cenas não perde nada — o estado vive nos
artefatos, não na sessão.

## Caminho assinatura (sob congelamento de tradução)

Para traduzir uma cena nova sem estourar a sessão:
1. `run_scene <projeto> <cena>` → para em `awaiting` e aponta o `scene_prompt.md` (pequeno, auto-contido).
2. Numa **sessão limpa**, o modelo responde o prompt produzindo `translations_<scene_id>.json`.
3. `run_scene <projeto> <cena>` de novo → segue build_plan → verify → checkpoint.

Como cada cena é uma sessão independente e limitada, o contexto **nunca acumula** entre cenas.

## Convenções de conector (por projeto)

`run_scene` invoca os scripts do conector do projeto por convenção:
`<projeto>/connector/build_plan_chapter.py` e `verify_chapter.py` (override em `project.json`
→ `connector.build_plan_script` / `connector.verify_script`). Esses scripts são determinísticos,
read-only no binário, e nunca contêm work-text.

## Verificação ponta-a-ponta

```
pytest framework/runtime/ framework/validation/ projects/<projeto>/connector/   # tudo verde
python framework/runtime/context_pack.py <projeto> <cena>   # roda 2x → pack.json idêntico
python framework/runtime/state_index.py <projeto> --rebuild # idempotente
python framework/runtime/run_scene.py <projeto> <cena-já-traduzida>  # dry-run: round-trip ok
```
