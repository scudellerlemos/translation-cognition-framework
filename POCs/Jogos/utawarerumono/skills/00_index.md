# SDD SKILLS — ÍNDICE GERAL
## Spec-Driven Development para Localização de Jogos

> **Projeto:** Utawarerumono: Mask of Deception  
> **Versão do processo:** 2.0 (com melhorias pós-QA)  
> **Localização das skills:** `/skills/`

---

## FLUXO DO PROCESSO

```
01_discovery
    ↓
02_entity_resolution
    ↓
03_knowledge_building
    ↓
04_glossary_creation  +  04b_decision_log (inicia aqui, acumulativo)
    ↓
05_translation_planning  +  05b_synthetic_test_corpus
    ↓
06_translation  (lotes de 200 linhas + auto-revisão de voz inline)
    ↓
06b_micro_qa  (após cada lote — aprovar antes de avançar)
    ↓
07_qa  (após cada arco/segmento maior e ao final do corpus)
```

---

## ARQUIVOS DO PROCESSO

### Skills (instruções)

| Arquivo | Passo | Descrição |
|---------|-------|-----------|
| `01_discovery.md` | 1 | Identificar entidades, tom, aliases, spoilers |
| `02_entity_resolution.md` | 2 | Classificar e unificar entidades |
| `03_knowledge_building.md` | 3 | Pesquisa colaborativa (IA + humano) + base de conhecimento do universo |
| `04_glossary_creation.md` | 4 | Glossário + regras de tradução |
| `04b_decision_log.md` | 4b | Registro de decisões — auditoria do processo |
| `05_translation_planning.md` | 5 | Plano de tradução por linha |
| `05b_synthetic_test_corpus.md` | 5b | Corpus de teste para pontos críticos |
| `06_translation.md` | 6 | Execução da tradução com controle de progresso |
| `06b_micro_qa.md` | 6b | QA por lote após cada 200 linhas |
| `06c_correction_cycle.md` | 6c | Correções cirúrgicas pós-QA com re-validação |
| `07_qa.md` | 7 | QA final de consistência global |
| `schemas/artifacts_schema.md` | — | Schemas formais de todos os artefatos JSON e CSV |

### Artifacts (outputs do processo)

| Arquivo | Gerado em | Descrição |
|---------|-----------|-----------|
| `entities_candidates.json` | Passo 1 | Entidades brutas extraídas |
| `aliases_map.json` | Passo 1 | Mapa alias → canônico com spoiler levels |
| `terminology_clusters.json` | Passo 1 | Agrupamento por tipo de termo |
| `tone_analysis.md` | Passo 1 | Análise de tom, registros, perfis de voz |
| `entities.csv` | Passo 2 | Entidades resolvidas e classificadas |
| `research_log.md` | Passo 3 | Fontes pesquisadas, conflitos resolvidos, fronteira de spoiler |
| `universe_knowledge_base.md` | Passo 3 | Base de conhecimento por entidade, com citações de fonte |
| `glossary.csv` | Passo 4 | Fonte de verdade operacional dos termos |
| `translation_rules.md` | Passo 4 | Documento normativo com justificativas |
| `decision_log.md` | Passo 4b | Registro acumulativo de decisões |
| `translation_plan.json` | Passo 5 | Plano linha a linha com intenção e risco |
| `synthetic_test_corpus.json` | Passo 5b | Casos de teste sintéticos por suite |
| `synthetic_test_results.json` | Passo 5b | Resultados das execuções de teste |
| `dialogs.csv` | — | Corpus source (todas as linhas, imutável) |
| `translated.csv` | Passo 6 | Corpus com todas as linhas; pt vazio = pendente |
| `translation_status.json` | Passo 6 | Progresso atual + next_offset + length_warnings + needs_human_review |
| `micro_qa_log.json` | Passo 6b/6c | Log acumulativo de issues e correções por lote |
| `qa_report.md` | Passo 7 | Relatório de QA final |
| `fix_suggestions.json` | Passo 7 | Issues com sugestões de correção (input do Passo 6c) |

---

## MELHORIAS DA VERSÃO 2.0

Estas mudanças foram adicionadas após análise crítica do processo v1.0:

| Melhoria | Onde | Problema resolvido |
|----------|------|--------------------|
| Auto-revisão de voz inline | Passo 6 | Tom de personagens deriva sem feedback imediato |
| Micro-QA por lote (passo 6b) | Novo passo | Drift de tom acumula antes de ser detectado |
| Back-translation para alto risco | Passos 6b e 7 | Sentido e tom podem sobreviver na forma mas não no conteúdo |
| Decision log (passo 4b) | Novo passo | Decisões não-óbvias são perdidas entre sessões |
| Corpus de teste sintético (passo 5b) | Novo passo | Erros em identidade dupla são descobertos tarde no corpus real |
| `translation_status.json` | Passo 6 | Tradução para sem rastreamento de onde retomar |
| `next_offset` no output do passo 6 | Passo 6 | Execuções recomeçam do zero em vez de continuar |
| Todas as linhas no `translated.csv` | Passo 6 | Linhas pendentes são invisíveis |
| Passo 5 obrigatório | Passo 5 | Tradução ia direto do glossário para execução sem plano |

---

## REGRAS GLOBAIS DO PROCESSO

1. **Nunca pular passos.** Cada passo é pré-requisito do seguinte.
2. **Nunca sobrescrever traduções existentes** ao retomar — só preencher vazios.
3. **Decision log é acumulativo** — nunca apagar entradas.
4. **Corpus sintético deve ser aprovado** antes de traduzir segmentos reais de identidade dupla.
5. **Micro-QA bloqueia o próximo lote** se houver issues críticos não resolvidos.
6. **Issues críticos no QA final bloqueiam entrega** — sem exceção.
7. **Em caso de conflito** entre `translation_rules.md` e `glossary.csv`, o CSV prevalece na forma final.
8. **Cada passo tem um Input Gate.** Não executar sem verificar os artefatos do passo anterior.
9. **Correções passam pelo Passo 06c.** Não editar `translated.csv` diretamente fora do protocolo 06c.
10. **Atualização de glossário mid-project** exige identificação de impacto + agendamento de re-QA via 06c.

---

## INVARIANTES DO PROCESSO

Estas condições devem ser verdadeiras em qualquer ponto do projeto:

| Invariante | Verificável em |
|-----------|---------------|
| `dialogs.csv` é somente leitura — nunca modificado | A qualquer momento |
| `translated.csv` tem o mesmo número de linhas que `dialogs.csv` | Após criação do arquivo |
| `micro_qa_log.json` contém todas as entradas desde o início | A qualquer momento |
| `decision_log.md` nunca perde entradas | A qualquer momento |
| Nenhuma tradução final usa alias de spoiler major/critical antes do reveal | QA Final |
| `research_log.md` tem `status: reconciled` antes do Passo 4 iniciar | Input Gate do Passo 4 |
| Schemas de todos os artefatos respeitam `schemas/artifacts_schema.md` | A cada passo |

---

## CRITÉRIOS DE ACEITAÇÃO DO PROJETO

O projeto está completo quando:

- [ ] `translation_status.json` com `completion_pct: 1.00`
- [ ] `qa_report.md` com status: **aprovado** (0 issues críticos, ≤ aceitável de altos)
- [ ] `fix_suggestions.json` com todos os issues críticos com `status: applied`
- [ ] `needs_human_review` no `translation_status.json` está vazio ou todos revisados
- [ ] Nenhum `length_warning` sem revisão documentada
- [ ] `decision_log.md` atualizado com todas as decisões não-óbvias do projeto
