# Translation Pipeline — fluxo de 1 cena no harness

O `framework/runtime/run_scene.py` executa uma cena como um **job determinístico e resumível**. Esta é
a sequência, os artefatos e os pontos de retomada.

## Fluxo

```
python framework/runtime/run_scene.py <projeto> <cena> [<cena> ...] [--backend in-session|api] [--require-back] [--no-verify]

[0] gates          →  connector_gate + kb_gate (bloqueiam antes de qualquer chamada de modelo)
[1] context_pack   →  artifacts/scenes/<cena>/{scene_prompt.md, pack.json}     (determinístico)
[2] translate      →  artifacts/scenes/<cena>/translations_<scene_id>.json           (IA; in-session espera o arquivo)
[3] build_plan     →  artifacts/scenes/<cena>/{translation_plan_<scene_id>.json, approved_<scene_id>.csv}  (det. + valida)
[4] verify         →  round-trip byte-idêntico + ponteiros within-file    (determinístico)
[5] back_translate →  artifacts/scenes/<cena>/back_translation_<scene_id>.json        (IA; risk>=high; report-only)
[6] checkpoint     →  artifacts/run_state.json  + reconstrói artifacts/state/  (TM cresce)
```

`<scene_id>` = nome da cena sem o prefixo `ch_` (ex.: `ch_12_01` → `12_01`).

## Gates (bloqueiam o avanço)

- **[3] build_plan_chapter** valida: cobertura total, token `\n` preservado, interjeição ≠ source,
  `risk >= medium` exige `risk_notes`. Falha → `status: build_plan_failed`.
- **[5] back-translation** em `risk >= high` (mais amostra de 5% das demais em cenas do batch), depois do verify. Por padrão é **reportada** (não bloqueia); com
  `--require-back` bloqueia até existir `back_translation_<scene_id>.json`.
- **[4] verify_chapter** exige round-trip idêntico (approved={}), cada offset lido == approved
  transliterado, **resíduo = 0**, ponteiros resolvendo dentro do arquivo. Falha → `verify_failed`.
- **Conferência visual no jogo** acontece na Fase 2 (piloto): o humano vê o trajeto do piloto instalado antes
  de escalar. O fechamento (Fase 4) **não** repete uma passada pelo jogo inteiro; depois do piloto, a
  conferência é por print a cada instalação. Vale para os dois caminhos (sessão e API).

## Humano no laço (`hitl.py`, projeto com `"hitl": true` no `project.json`)

Projeto novo nasce com a chave (scaffold); projeto sem ela segue como antes. Toda decisão fica em
`artifacts/hitl_log.jsonl` (quem, quando, o quê — sem o texto da fala). `hitl.py status <projeto>` mostra tudo.

- **Escopo** — antes de traduzir, o humano aceita o corpus extraído (`hitl.py accept-scope`). Re-extração
  que muda cenas/linhas reabre o aceite. Bloqueia o CLI do `run_scene`.
- **Caminho** — sessão ou API é escolha humana (`hitl.py choose-path`). Bloqueia o CLI do `run_scene`.
- **Glossário** — os 30 termos mais frequentes do glossário pedem ratificação (`hitl.py ratify`, grava em
  `kb_ratified.csv`). **Aviso, não bloqueia.**
- **Onda** — a cada 10 cenas recém-verificadas sai uma amostra de 15 falas em
  `qa_revisao/para_revisar/onda_amostra.csv` (`hitl.py ack` registra o visto). **Aviso, não bloqueia.**
- **Só bloqueia o que é decisão de verdade:** escopo, caminho e a fila de escalonamento (ambiguidade).
  Ratificar e dar visto em série não achavam problema; o que rende é a fila.
- **Decisão na conversa** — quando o humano decide conversando com o assistente, é o assistente que roda o
  comando, com `--quote "frase literal do humano"`; o log guarda `via=conversa` e a frase. Sem frase literal
  não há registro: aviso de sistema ou relatório de agente não é decisão.
- **Fila de escalonamento** — fala em que a forma do glossário não entrou, ou que o tradutor marcou com
  `escalate`, vai para `qa_revisao/para_revisar/escalonamento.csv`. O humano responde `alias` (a forma
  passa a valer: vira regra no glossário) ou `correcao` (texto certo) e roda `hitl.py resolve`. Item aberto
  bloqueia o `quality_gate`. Correção do `quality_review apply` que diverge do glossário também cai aqui.
- **Triagem de risco** (`risk_triage.py`, só caminho de sessão) — antes da QA humana, um juiz barato lê
  os pares únicos fonte+tradução de risco baixo e devolve só os ids que merecem segundo olhar; `apply`
  sobe essas falas para `high`, e a retrotradução (`--require-back`) e o `quality_review export` cuidam delas.
- **Medida de qualidade** (`quality_sample.py`, $0) — `export` sorteia 200 pares únicos do jogo inteiro e
  mistura os que o juiz apontou, sem dizer a origem; o humano marca `ok`/`erro`; `score` calcula a taxa de
  erro com intervalo de 95%, a taxa da triagem e o acerto do juiz (precisão e alcance), e grava o registro
  em `qa_effectiveness.jsonl`.

## Onda num comando (`wave.py`, caminho de sessão)

`python framework/runtime/wave.py <projeto> [cena ...] [--require-back]` roda `run_scene` (se houver cenas),
`glossary_lint`, `quality_gate`, `cost_report --summary` e `obs_report` em sequência, para no primeiro passo
que falhar, grava a saída inteira em `artifacts/wave_last.log` e devolve uma linha por passo. Mesmos comandos
e gates; só troca N requisições da janela por uma. `obs_report` é enxuto por padrão (`--all` = todas as cenas).

## Sessão: contexto e medição de custo (caminho de sessão)

Regra, não sugestão:

- **`/compact` nunca à mão.** A compactação fica com a automática do Claude Code. Medido em 62 compactações:
  cada uma custa a reescrita do resumo no cache, e compactar antes da hora paga isso mais vezes do que economiza.
- **`/clear` em toda virada de fase**, e só nela. Antes: tudo o que a fase decidiu está em disco (ROADMAP do
  projeto, `decision_log.md`, `hitl.py status`). Depois: o primeiro comando da sessão nova é
  `python framework/runtime/session_usage.py mark <projeto> <fase>`, que fecha a fase anterior no ledger e
  carimba a nova. É essa marca que faz o `cost_report` mostrar o custo **por fase** sem adivinhar.
- O ROADMAP de cada projeto tem a seção **"Retomada"**: o que uma sessão sem contexto precisa para continuar
  (passo atual, bloqueios, aprovações pendentes, comandos e ferramentas locais). Atualizar antes do `/clear`.
- Ao fechar uma medição: `python framework/runtime/session_usage.py rebuild <projeto>` refaz as linhas de sessão
  a partir das transcrições inteiras. Saída de mensagem sem `usage` final na transcrição é estimada pelo
  conteúdo e o relatório diz quanto do total é estimativa.

## Troca de caminho (sessão ↔ API)

A troca é a flag `--backend` do `run_scene`/`wave`; artefatos, gates, banco e humano no laço são os mesmos.
Toda execução abre dizendo o caminho e o escopo (`caminho: api | escopo do projeto: completo`) e confere:

- **Escopo:** a API só traduz diálogo. Cena listada em `system_scenes` no `project.json` (texto de sistema,
  que só existe com `"extraction_scope": "completo"`) é recusada com `--backend api`; vai pela sessão.
- **Chave:** `--backend api` sem `ANTHROPIC_API_KEY` no ambiente para antes de qualquer chamada. Crédito
  esgotado só aparece na primeira chamada (`ERRO na traducao (api)`).
- **Um projeto, um caminho:** com humano no laço, o caminho é decisão registrada
  (`hitl.py choose-path <projeto> in-session|api --reviewer NOME`). Sem decisão o `run_scene` não roda; pedido
  no outro caminho é recusado até um humano trocar pelo mesmo comando (a troca fica no `hitl_log.jsonl`).
- **Mistura:** cena já traduzida pelo outro caminho não bloqueia, mas sai um `AVISO` com a lista: tradutor e
  modelo mudam (API usa o ranqueamento de modelos; sessão usa o modelo da janela), então o estilo pode variar.
  A origem de cada cena fica em `metrics.jsonl` (`source`) e no `cost_report`.

## Checkpoint / resume (`run_state.json`)

`status` por cena: `packed` → `planned` → `verified` (ou `*_failed`, `awaiting_*`). O harness é
idempotente: rode de novo a qualquer momento; ele recomputa o pacote e retoma na etapa pendente (no backend `in-session` reusa o
`translations_<scene_id>.json` existente; no `api`, cena não-`verified` é re-traduzida). Crash entre cenas não perde nada — o estado vive nos
artefatos, não na sessão.

## Caminho assinatura (sob congelamento de tradução)

Para traduzir uma cena nova sem estourar a sessão:
1. `run_scene <projeto> <cena> --backend in-session` → para em `awaiting_translation` e aponta o `scene_prompt.md` (pequeno, auto-contido).
2. Numa **sessão limpa**, o modelo responde o prompt produzindo `translations_<scene_id>.json`.
3. O mesmo comando de novo → segue build_plan → verify → checkpoint.

Como cada cena é uma sessão independente e limitada, o contexto **nunca acumula** entre cenas.

## Convenções de conector (por projeto)

`run_scene` invoca os scripts do conector do projeto por convenção:
`<projeto>/connector/build_plan_chapter.py` e `verify_chapter.py` (override em `project.json`
→ `connector.build_plan_script` / `connector.verify_script`). Esses scripts são determinísticos,
read-only no binário, e nunca contêm work-text.

## Distribuição (patcher de um clique, `framework/distribution/`, skill `09_distribution`)

Depois do round-trip verde, a tradução sai como **delta**, nunca como DAT remontado. Config por projeto em
`projects/<p>/distribution.json` (título, autor, pasta do jogo, processos que travam os arquivos, aviso, recorte do ícone).

1. `python -I framework/distribution/build_package.py distribution.json source_dat output dist <versao> [arte [capa]]`
   (de dentro do projeto): deltas bsdiff + `manifest.json` com hashes e o bloco `app`. Arte e ícone só no pacote.
2. `python framework/distribution/build_exe.py dist <saida>`: `.exe` único (PyInstaller; sem Python no jogador).
3. Teste: `patcher.py verificar|instalar|desinstalar --jogo <pasta> --pacote dist` numa cópia dos originais; depois
   o `.exe` no jogo real. Regras do patcher: só toca arquivo com hash original, backup `.bak`, confere hash final,
   desfaz tudo se falhar, recusa com o jogo aberto.
4. Publicar: release no GitHub (só o `.exe` e o hash) + guia na comunidade Steam. `dist/` está no `.gitignore`.

Dependências: `bsdiff4`, `pyinstaller`, `Pillow` (só para arte/ícone).

## Verificação ponta-a-ponta

```
pytest framework/runtime/ framework/validation/ projects/<projeto>/connector/   # tudo verde
python framework/runtime/context_pack.py <projeto> <cena>   # roda 2x → pack.json idêntico
python framework/runtime/state_index.py <projeto>           # idempotente
python framework/runtime/run_scene.py <projeto> <cena-já-traduzida>  # dry-run: round-trip ok
```
