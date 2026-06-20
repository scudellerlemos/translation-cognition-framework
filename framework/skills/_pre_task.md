# META-GATE — PRÉ-TAREFA
## Verificações obrigatórias antes de qualquer skill deste framework

> **Quando usar:** Antes de iniciar qualquer tarefa neste projeto — independente do skill ou etapa.

---

## ⬛ GATE — DECISÕES FECHADAS

As decisões abaixo estão fechadas neste projeto. Não reinventar — verificar aqui antes de propor solução.

| Decisão | Regra |
|---------|-------|
| Engine labels | Não traduzir — allowlist em `_ENGINE_LABELS` + `_ENGINE_LABEL_RX` (model.py) |
| Batch resume | `run_scene(pretranslated=True, defer_back=True)` — nunca re-traduzir cobertura existente |
| Spoiler control | Ledger de reveal + filtro temporal no context_pack; decisão por linha |
| Otimização de custo | Cortar fitting-fail/re-run, não modelo nem cache |
| Translation Memory | Isolada por série; round-trip byte-idêntico é o oráculo inegociável |

❌ **Se a tarefa contradiz uma decisão fechada: PARAR e apontar o conflito antes de executar.**
