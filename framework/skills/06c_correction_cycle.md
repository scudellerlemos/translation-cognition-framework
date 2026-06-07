# SKILL 06c — CORRECTION CYCLE
## Aplicar correções ao corpus sem corromper traduções existentes

> **Quando usar:** Após o passo 06b emitir `batch_approved: false`, ou após o passo 07 produzir `fix_suggestions.json`. Este passo fecha o loop detectar → corrigir → re-validar.

---

## OBJETIVO

Aplicar correções identificadas pelo Micro-QA ou pelo QA Final ao `translated.csv`, com escopo cirúrgico (apenas os IDs identificados), verificação inline de cada correção, e registro auditável do que foi alterado.

---

## INPUTS

- `micro_qa_log.json` (se vindo do passo 06b) **ou** `fix_suggestions.json` (se vindo do passo 07)
- `translated.csv` (estado atual do corpus)
- `project.json` (tokens, length_constraints)
- `glossary.csv`
- `translation_rules.md`
- `tone_analysis.md`

---

## PROTOCOLO DE EXECUÇÃO

### Passo 1 — Separar issues por severidade

| Severidade | Ação neste ciclo |
|------------|-----------------|
| Crítica | Corrigir obrigatoriamente |
| Alta | Corrigir obrigatoriamente |
| Média | Corrigir se possível; marcar como `deferred` caso contrário |
| Baixa | Opcional |

### Passo 2 — Definir o escopo cirúrgico

Montar a lista de IDs (`id_column`) a corrigir. **Esta lista é o único escopo do ciclo.** Nenhuma linha fora desses IDs deve ser tocada — qualquer edição fora do escopo é uma regressão potencial.

### Passo 3 — Aplicar correções

Para cada ID na lista:
1. Localizar a linha em `translated.csv`
2. Aplicar a `suggested` do log, ou uma nova tradução fundamentada na análise
3. Antes de aceitar, verificar checklist obrigatório:

```
CHECKLIST DE CORREÇÃO:
□ O registro está correto para o personagem (ver perfil em tone_analysis.md)?
□ A entidade está tratada conforme glossary.csv?
□ Os tokens (project.json → formatting_tokens) e quebras de linha estão preservados (mesma contagem)?
□ O comprimento respeita project.json → length_constraints?
□ Se risk_level: high ou critical: back-translation confirma sentido?
```

### Passo 4 — Mini-QA pós-correção

Após aplicar todas as correções, executar verificação reduzida **somente nas linhas corrigidas**:
- Re-verificar voz para cada linha alterada
- Re-verificar tokens de cada linha alterada
- Re-verificar entidades de cada linha alterada
- Se a linha é `risk_level: high` ou `critical`: back-translation obrigatória

Se uma linha falhar no mini-QA:
- Registrar novo issue no log
- Se for a segunda tentativa no mesmo ID: escalar para revisão humana com `escalated: true`

### Passo 5 — Atualizar os logs

**Se vindo do 06b** — adicionar entrada ao `micro_qa_log.json` (append):

```json
{
  "batch": "1_correction",
  "offsets": "[ids corrigidos]",
  "lines_reviewed": 0,
  "issues_found": [],
  "corrections_applied": [
    {
      "offset": "[id]",
      "original_issue": "[descrição]",
      "previous_pt": "[tradução anterior]",
      "corrected_pt": "[tradução corrigida]",
      "mini_qa_passed": true
    }
  ],
  "batch_approved": true,
  "notes": "Todas as correções aplicadas e verificadas. Lote liberado."
}
```

**Se vindo do 07** — marcar cada issue resolvido no `fix_suggestions.json`:
```json
{
  "id": "FIX-001",
  "status": "applied",
  "applied_pt": "[tradução aplicada]",
  "verified": true
}
```

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Modificação |
|---------|-------------|
| `translated.csv` | Linhas corrigidas atualizadas (somente os IDs do escopo) |
| `micro_qa_log.json` | Nova entrada de correção adicionada (append) |
| `fix_suggestions.json` | Issues resolvidos marcados com `"status": "applied"` |

---

## REGRAS CRÍTICAS

- **Escopo cirúrgico é inviolável.** Nunca modificar linhas fora da lista de IDs do ciclo.
- **Nunca aceitar uma correção sem passar pelo checklist.** A correção pode introduzir um novo issue.
- Após o ciclo: se `micro_qa_log.json` ainda contém issues críticos não resolvidos → **o bloqueio de avanço para o próximo lote permanece ativo**.
- Issues escalados (`escalated: true`) devem ser resolvidos por humano antes da entrega.
- Este passo é **sempre sequencial** — não aplicar correções em paralelo no mesmo arquivo.
