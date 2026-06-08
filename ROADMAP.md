# Roadmap — Translation Cognition Framework (SDD)

> Última atualização: 2026-06-08
> Escopo: framework genérico + instância de referência Utawarerumono.
> O roadmap detalhado de decisões vive em `projects/<título>/artifacts/decision_log.md`.

---

## Onde estamos (maturidade)

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro (~92/100) |
| Perfil de jogos | 🟢 validado |
| Instância Utawarerumono | 🟡 pipeline 00→08 em **2 cenas / 1025 linhas**; **resíduo T4=0**; pt-BR **renderiza in-game ✅**; pendente o **gate do Plano B** (1 linha) |
| Conector hex_binary | 🟢 formato mapeado; **ponteiros FILE-RELATIVOS**; **relocação INTRA-ARQUIVO + rebuild do Pack** (EOF-append reprovado in-game); **pytest** (9 testes) |
| Perfis filme/série + conector subtitle_file | 🟠/🔴 stub / não iniciado |

**Resumo:** o *processo* está maduro (~92). A *validação de produção* deu um salto: o **pt-BR do
framework já renderizou no jogo real** (prova de ponta a ponta — `artifacts/Fasea*.png`). O mesmo teste
**reprovou o EOF-append** (relocar ao fim do container → `@@@@`/trava porque o engine respeita o `size`
do Pack), o que motivou o **Plano B** (relocação dentro do arquivo + reescrita da tabela Pack), já
implementado e travado por pytest. O bloqueador restante é estreito: confirmar in-game **1 linha**
relocada pelo Plano B antes da run completa.

---

## Próximos passos

### Fase A — Fechar o caminho até produção (Utawarerumono)

- [~] **A1. Gate in-game.** **BLOQUEIA tudo abaixo.** *Parcial:*
  - ✅ **pt-BR renderiza no jogo real** (in_place) — objetivo de ponta a ponta atingido (`Fasea2/3/8/9/10`).
  - ❌ **EOF-append reprovado**: linhas relocadas ao fim do CONTAINER viram `@@@@` e travam (`Fasea11`).
    Causa: o engine carrega cada arquivo num buffer do tamanho do `size` no Pack. Ver `decision_log.md`.
  - ⏳ **Gate do Plano B (pendente — só o usuário faz):** aplicar o patch de **1 linha** gerado por
    `python connector/reinsert.py --validate-one 0x3442` e confirmar que "ERRO DE SISTEMA." exibe e o
    jogo segue. Verde aqui → libera a run completa (A3).
- [x] **A2. Ordem offset × ordem narrativa.** *(resolvido p/ a abertura)* A extração agora segue a
  **ordem de armazenamento por script** (= narrativa, verificado nas cenas iniciais). Para cenas
  distantes, validar; se divergir, caminhar o bytecode por ordem de comando. Ver `decision_log.md`.

- [ ] **A3. Estratégia de JOGO INTEIRO (~30k+ linhas) — loop incremental, resumível.**
  Fazer tudo de uma vez é inviável. Separar o **determinístico** (rápido, automático) do **cognitivo**
  (gargalo) e fatiar por capítulo. Pré-requisito: **A1 verde**.
  - **Fase 1 — "Ler o jogo" (barato, sem traduzir):** `SCENES`=todos os 353 scripts → medir o tamanho
    exato; rodar Discovery+Entity sobre o corpus inteiro **uma vez** → **glossário/entidades GLOBAL**
    (termos canônicos nascem uma vez e **congelam**) + mapa de tamanho por capítulo.
  - **Fase 2 — Loop por capítulo (11→39, ~16 caps):** para cada cap.: extrair → Knowledge Building
    com **fronteira de spoiler que avança** só até o cap. atual → traduzir em **lotes de 200**
    (`translation_status.json` marca a fronteira → resumível) → micro-QA + `reinsert` + `pytest` →
    spot-check in-game a cada poucos caps. Ritmo: **1–2 capítulos por sessão**, nunca tudo de uma vez.
  - **Fase 3 — Fechamento:** passe global de **consistência de glossário** (linter determinístico) →
    `reinsert` do jogo inteiro + `pytest` + patch IPS final.
  - **Consistência em escala:** glossário congelado + voice profiles + **handoff de contexto** (últimas
    N linhas da cena anterior) + fronteira de spoiler móvel.
  - **Aceleração opcional:** tradução por cena é paralelizável (glossário/voz congelados) → candidata a
    **workflow multi-agente** (fan-out por cena + passe de consistência). Caminho caro; só sob demanda.
  - Esta é a **prova de produção** do framework. Casa com A4 (custo) e A5 (redução de custo).
- [ ] **A4. Estimativa de custo real (em $/tokens/tempo)** da run de 33k.
  Lacuna do diagnóstico: hoje só há análise arquitetural (shift-left, ~330 chamadas máx). Calcular
  custo monetário e tempo de relógio. Cabe junto da A3. **Pré-requisito da A5** (sem baseline não há
  o que reduzir).
- [ ] **A5. Analisar o custo atual e reduzir — meta: −80%** *(agressiva, pode mudar).*
  Tomar o baseline da A4 como ponto de partida e atacar os maiores ofensores de custo. Linhas de
  investigação:
  - **Modelo certo por tarefa:** usar modelo barato (ex.: Haiku) para passos mecânicos/baixo risco e
    reservar o modelo forte para linhas `risk_level ≥ high` e identidades duplas.
  - **Prompt/context caching:** reaproveitar glossário, perfil de voz e regras entre lotes em vez de
    reenviar (o glossário/voz é estável → ótimo candidato a cache).
  - **Batching e shift-left:** já existe (T1–T3 determinístico, byte_budget no prompt); medir o
    quanto realmente evita reescrita LLM e empurrar mais trabalho para o determinístico.
  - **Evitar retrabalho:** Micro-QA/06c só re-tocam o que falhou; medir taxa de reprocessamento.
  - **Triagem:** linhas de sistema/anomalias (ex.: `0x33f9`) e strings triviais podem sair do
    caminho do LLM.
  Definir a métrica ($ por 1.000 linhas) e acompanhar a redução contra a meta. A meta de 80% é alvo
  inicial — recalibrar quando houver o baseline real.

### Fase B — Evolução do motor (só DEPOIS da produção)

> Decisão estratégica: estes itens transformam o framework de "documento" em "motor executável".
> Construí-los antes da run completa = abstração prematura. Sequência recomendada (cada um habilita
> o próximo). Cada item vira uma rodada de planejamento própria quando chegar a vez.

- [ ] **B1. Validation leve.** Validadores executáveis dos schemas + invariantes (hoje em prosa:
  `framework/schemas/artifacts_schema.md`, `framework/skills/_index.md`). Maior valor / menor esforço /
  menor risco. *Pode ser puxado para junto da produção* (reduz risco da run de 33k).
- [ ] **B2. Memory leve** (glossário + character state básico). Estado vivo e consultável entre os
  165 lotes, no lugar de re-ler CSV ad-hoc. Desenhar **informado pela run real** (A3).
- [ ] **B3. Kernel simples.** Runtime que orquestra os passos usando Validation (gates) + Memory
  (estado), no lugar de scripts ad-hoc. Compensa com repetibilidade (≥2 projetos ou re-runs).
- [ ] **B4. Skill DSL.** Forma declarativa dos passos 00–08 (hoje prosa .md) que o Kernel lê. Por
  último: só vale com 2–3 projetos e o Kernel existente (maior risco de abstração prematura).

### Fase C — Escalar para outras mídias

- [ ] **C1. Validar perfil de filmes** com projeto real (legenda/dublagem) → implementar conector
  `subtitle_file` (SRT/ASS), constraint de CPS. `framework/media-profiles/films.md` (stub).
- [ ] **C2. Validar perfil de séries** (≥2 episódios): glossário/decision_log compartilhados,
  spoiler-check cross-episódio, QA de continuidade. `framework/media-profiles/series.md` (stub).

---

### Adiado (baixa prioridade agora — fazer no momento certo)

- [ ] **T4 em lote (LLM):** reescrita do resíduo irredutível. Com o modelo file-relativo o resíduo é 0
  → só necessário se algum corpus futuro gerar overflow não-repointável.
- [ ] **Metadados cognitivos por linha em escala:** hoje curados em `11_01_000S`, auto-defaultados no
  resto (speaker heurístico, risk low). Refinar se/quando a qualidade exigir.
- [ ] **CI + empacotamento de release:** baixo valor enquanto for 1 dev / 1 obra e pré-gate-in-game.
  Faz sentido **depois** do gate in-game e de uma 2ª instância (aí CI protege 2 obras de verdade).

---

## Já concluído (para referência)

- ✅ Framework SDD genérico (camadas: processo / perfil / conector / instância).
- ✅ Conector hex_binary: container `.sdat` mapeado (header `Filename`/`Pack`, 353 scripts; texto UTF-8
  contíguo por script).
- ✅ **Modelo de ponteiro corrigido para FILE-RELATIVO** (`50 00` + uint32 relativo ao início do
  arquivo) — descoberta que invalidou o modelo absoluto anterior. Ver `decision_log.md`.
- ✅ **Primeiro pt-BR do framework renderizado no jogo real** (Steam) — prova de ponta a ponta. `Fasea*.png`.
- ✅ **Plano B no conector:** relocação **intra-arquivo** + `rebuild_container` (reescreve a tabela Pack,
  padding a 16 bytes) — substitui o EOF-append reprovado in-game. 1025 linhas: T1=595, RELOC=430,
  resíduo 0; 425/425 ponteiros relocados resolvem dentro do arquivo; 9 testes pytest verdes.
- ✅ Charset: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração na gravação**.
- ✅ Round-trip byte-idêntico + patch IPS + **teste de regressão `pytest` (6 testes, valida o valor do
  ponteiro file-relativo, não-circular)**.
- ✅ Extração **por arco/script** (`SCENES`) com limpeza de bordas; container totalmente parseado.
- ✅ Pipeline cognitivo 00→08 rodado de verdade em **2 cenas / 1025 linhas** (entities, glossário,
  research_log com gate de cobrança, plano, micro-QA, QA, approved, reinsert).
- ✅ `.gitignore` para não versionar `.sdat` (assets com copyright).
