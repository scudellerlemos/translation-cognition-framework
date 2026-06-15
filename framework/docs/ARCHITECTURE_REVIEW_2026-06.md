# Architecture Review #2 — pós-harness de escala (2026-06)

> Segunda revisão de arquitetura, no mesmo espírito da #1 (que diagnosticou o estouro de sessão e
> propôs o harness). Esta revisão avalia o estado **depois** de o harness ter sido construído e
> endurecido, e registra **duas lacunas estruturais novas** que só ficaram visíveis agora.
> Aterrada no código real (`framework/runtime/`), não em memória.

## Veredito geral

A cura diagnosticada na revisão #1 **foi construída e endurecida**, mas **nunca rodou end-to-end** (sem
chave de API). Passamos de *"a cura existe no papel"* para *"existe em código, testada offline (9/9
pytest), mas não comprovada em produção"*. A revisão expôs duas lacunas que não eram visíveis antes: o
**conhecimento (KB reconciliada)** e o **controle de spoiler** são doutrina nas skills, mas **não estão
cabeados no runtime de escala**. A evidência viva do problema antigo está no próprio
`projects/utawarerumono/artifacts/run_state.json`: **ch_12_03 travado em `packed`** — exatamente a cena
onde a tradução in-session estourou a sessão.

## O que mudou desde a revisão #1

| Dimensão | Revisão #1 | Agora |
|---|---|---|
| Orquestração fora do chat | 🔨 plano | ✅ `run_scene.py` + `run_chapter.py` |
| Contexto O(cena) | 🔨 plano | ✅ `context_pack.py` (glossário-subset, voice cards, TM hits) |
| Estado externo | parcial | ✅ `state_index.py` (TM/cards/decisions, idempotente) |
| Interface de modelo | 🔨 stub | ✅ `model.py` endurecido (streaming, schema, guard `\n`+retry, backoff, `usage`) |
| Caminho API (escala) | 🔨 não ligado | ⚠️ **codado, não comprovado** (falta `.env`) |
| Métricas | ❌ | ✅ `metrics.jsonl` (custo segmentado, back-pass-rate) |
| KB reconciliada como gate | implícita nas skills | ❌ **não cabeada no runtime** (gap novo) |
| Controle de spoiler por linha | não enxergado | ❌ **não existe** no `context_pack` (gap novo) |

## Quão perto do alvo "cena = job stateless e limitado"

| Propriedade-alvo | Status | Evidência |
|---|---|---|
| Contexto por execução **constante** (O(cena)) | ✅ | `context_pack`; `test_context_pack_bounded` |
| Cena **reproduzível a partir de artefatos**, sem o chat | ✅ | `pack.json` byte-idêntico 2× |
| `/clear` entre cenas sem perda | ✅ | estado em `run_state.json` + artefatos |
| Consistência vem de **store**, não da janela | 🟡 parcial | store existe, mas a tradução ainda não roda via store (default in-session) |
| Chat **deixa de ser runtime** | 🟡 só quando `api` liga | default ainda `in-session` (`model.py`) → chat ainda é o tradutor |

A infraestrutura está pronta; falta **virar a chave** (`.env` + default `api`). Enquanto o default for
`in-session`, o estouro continua possível — o harness só protege se a IA-tradutora for headless.

## Determinismo vs IA — mapa atualizado

| Responsabilidade | Onde deve viver | Status |
|---|---|---|
| Parser / extração / reinserção / round-trip | Determinístico | ✅ |
| Orquestração / fluxo / checkpoint | Determinístico | ✅ `run_scene`/`run_chapter` |
| Montagem de contexto limitado | Determinístico | ✅ `context_pack` |
| Memória de consistência (TM/voz/decisões) | Store externo | ✅ `state_index` |
| **Cobertura de conhecimento (KB) como pré-condição** | Determinístico (gate) | ❌ **falta** |
| **Gating temporal de spoiler** | Determinístico (filtro por posição) | ❌ **falta** |
| Tradução | IA | ✅ atrás de `model.py` (não comprovada) |
| Back-translation alto risco | IA | ✅ atrás de `model.py` |
| Custo / observabilidade | Determinístico | ✅ `metrics.jsonl` |

## Gaps reais hoje (ranqueados por severidade)

1. **🔴 Caminho API não comprovado empiricamente.** Tudo testado offline; zero chamada real → qualidade
   (Sonnet vs Opus), custo real, e robustez do guard `\n` em saída de modelo são **inferência, não
   medição**. Destrava com `.env` + benchmark.
2. **🔴 Default ainda `in-session`.** Enquanto não virar `api` por padrão (ou o `run_chapter` não for o
   entrypoint de fato), o chat continua sendo compute → estouro possível. ch_12_03 `packed` é a cicatriz.
3. **🟠 KB reconciliada não é gate no runtime.** `context_pack` consome glossário/cards/decisões como se
   existissem e estivessem completos; **não falha** se um termo/falante da cena não tiver cobertura. Arco
   novo entra "às cegas". (Ver plano: Fase 0 + gate de cobertura; memória `kb-reconciliation-mandatory`.)
4. **🟠 Spoiler sem gating temporal.** `context_pack` lê `spoiler_level` do glossário mas **só repassa** —
   não filtra por posição de cena nem injeta guard de ambiguidade. Risco concreto de vazamento por
   **gênero em pt-BR**. (Ver plano: `spoiler_ledger` + filtro temporal; memória `spoiler-control-strategy`.)
5. **🟡 Otimizações de custo pendentes** (dedup TM/intra-corpus, slim de schema, batch) — limpas,
   não-bloqueantes, levam o jogo de ~$58 a ~$20.
6. **🟡 KB cobre só ~cap. 11/12.** A 2ª metade do jogo não tem conhecimento construído — pré-requisito da
   Fase 0 antes de traduzir além.

## Readiness — notas revisadas

- **Operar sem memória de sessão:** **8/10** (era ~3). Sobe a 9–10 quando o default vira `api` e o
  `run_chapter` for o entrypoint padrão.
- **Sonnet readiness:** **arquitetura 9/10** (contexto curado + cache + store externo prontos);
  **empírica: N/A** (não medida) — o benchmark fecha essa nota.
- **Maturidade de governança:** **alta** — round-trip byte-idêntico, back-translation, lint, guard de
  work-text, tudo determinístico e testado. As lacunas KB/spoiler são de **cobertura cognitiva**, não de
  integridade técnica.

## Confiança

- **ALTA (código verificado):** harness existe, determinístico/idempotente, testes passam, API endurecida
  fielmente ao SDK, gaps KB/spoiler reais.
- **MÉDIA (inferido):** custo real (~$58–104), qualidade do Sonnet, taxa de retry do guard `\n`. Só o
  `metrics.jsonl` da 1ª rodada fecha.
- **Assumido:** caminho assinatura segue útil p/ spot-check; por isso `model.py` mantém os dois backends.

## Prioridades recomendadas (ordem)

1. **Ligar e comprovar o caminho API** (`.env` + benchmark de centavos) → fecha o gap #1 e a nota
   empírica do Sonnet.
2. **Tornar `api` o default de produção** (gap #2) — ou documentar `run_chapter --backend api` como
   entrypoint único.
3. **Cabear a Fase 0 + gate de cobertura de KB** (gap #3) antes de qualquer arco novo.
4. **Implementar `spoiler_ledger` + filtro temporal no `context_pack`** (gap #4) antes de traduzir
   trechos com identidades ocultas.
5. **Bundle de custo** (gap #5) — opcional, antes da tradução em massa.

## Resumo de uma linha

A arquitetura saiu de *"desenho correto, execução frágil"* para *"execução robusta e testada, mas (a)
não comprovada em produção e (b) com duas camadas cognitivas — conhecimento e spoiler — ainda na
doutrina, não no runtime"*. Os próximos passos não reescrevem nada: são **ligar** (API), **comprovar**
(benchmark/métricas) e **cabear** (KB-gate + spoiler-filter) o que já foi desenhado.
