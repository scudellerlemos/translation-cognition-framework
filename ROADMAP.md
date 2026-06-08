# Roadmap — Translation Cognition Framework (SDD)

> Última atualização: 2026-06-07
> Escopo: framework genérico + instância de referência Utawarerumono.
> O roadmap detalhado de decisões vive em `projects/<título>/artifacts/decision_log.md`.

---

## Onde estamos (maturidade)

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro |
| Perfil de jogos | 🟢 validado |
| Instância Utawarerumono | 🟡 POC validada (20 linhas) — extração + tradução + **repoint** + **transliteração** + patch IPS |
| Conector hex_binary | 🟢 formato mapeado; reinserção com repoint por run validada |
| Perfis filme/série + conector subtitle_file | 🟠/🔴 stub / não iniciado |

**Resumo:** o *processo* está maduro; a *aplicação* (Utawarerumono completo) ainda é POC de 20 linhas.
O caminho até produção são bloqueadores concretos, não polimento.

---

## Próximos passos

### Fase A — Fechar o caminho até produção (Utawarerumono)

- [ ] **A1. Confirmar in-game as strings relocadas (repoint).** ⏳ *pendente — só o usuário faz.*
  Aplicar `output/ScriptEvent.sdat.ips` e verificar que as linhas relocadas (apêndice ao fim do
  arquivo) exibem corretamente no jogo. Ex.: "ERRO DE SISTEMA.", "Onde... estou...?".
  *Risco:* o engine pode não aceitar ler strings na região apêndice. Se falhar → relocar para espaço
  livre interno em vez do EOF.
- [ ] **A2. Bloqueador 3 — ordem offset × ordem narrativa.**
  Hoje a POC usa ordem por offset como aproximação. Para o corpus completo, interpretar o script
  (sequência dos opcodes `50 00`) para obter a ordem real de exibição, quando a continuidade exigir.
  Ver `decision_log.md` → "Ordem de offset ≠ ordem de exibição".
- [ ] **A3. Run completa das ~33.000 linhas.**
  Estender `extract.py` (hoje limitado às 20 primeiras de `0x3398`) para varrer todo o bloco de texto.
  Rodar o pipeline 01–08 completo (discovery → glossário → tradução em lotes → QA → reinserção).
  Esta é a **prova de produção** do framework.
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

## Já concluído (para referência)

- ✅ Framework SDD genérico (camadas: processo / perfil / conector / instância).
- ✅ Conector hex_binary: formato do `.sdat` mapeado (UTF-8 contíguo; opcode `50 00` + ptr uint32 LE).
- ✅ Repoint real por **run** (head + continuações relocados; ponteiros reescritos); resíduo T4=0 na POC.
- ✅ Charset: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração na gravação**.
- ✅ Round-trip byte-idêntico + patch IPS.
- ✅ `.gitignore` para não versionar `.sdat` (assets com copyright).
