# SDD SKILLS — ÍNDICE GERAL
## Spec-Driven Development para Localização Baseada em Cognição Narrativa

> **Versão do processo:** 3.0 (framework genérico)
> **Localização das skills:** `framework/skills/`
> **Mídia suportada:** jogos (validado). Filmes e séries: pontos de extensão (ver `framework/media-profiles/`).

Este é o **processo genérico**. Ele não contém dados de nenhuma obra específica — toda a
configuração de um título vive em `projects/<título>/project.json` + `projects/<título>/profile/`.

---

## MODELO DE 3 CAMADAS

```
framework/skills/          ← O PROCESSO (como). Genérico. Nunca contém dados de obra.
        +
framework/media-profiles/  ← A CATEGORIA (jogos/filmes/séries). Formato, tokens, timing.
        +
framework/connectors/      ← A I/O (código det.). Extração/reinserção meio↔corpus.
        +
projects/<título>/         ← A INSTÂNCIA (o quê). Manifesto + perfil + artefatos + scripts do conector.
```

As skills resolvem tudo que é específico lendo `project.json` e os artefatos gerados. Ver
`framework/README.md` para como instanciar um projeto novo.

---

## FLUXO DO PROCESSO

```
00_extraction  (conector: binário → dialogs.csv + byte_budget; gate de round-trip)
    ↓
01_discovery
    ↓
02_entity_resolution
    ↓
03_knowledge_building  (pesquisa colaborativa IA+usuário → research_log.md)
    ↓
04_glossary_creation  +  04b_decision_log (inicia aqui, acumulativo)
    ↓
05_translation_planning  +  05b_synthetic_test_corpus
    ↓
06_translation  (lotes + auto-revisão de voz + orçamento de bytes / shift-left)
    ↓
06b_micro_qa  (após cada lote)
    ↓
06c_correction_cycle  (se o lote for reprovado — correção cirúrgica + re-validação)
    ↓
07_qa  (após cada arco/segmento maior e ao final do corpus)
    ↓
08_reinsertion  (conector: approved_translations.csv → binário traduzido em output/; cascata det., LLM só no resíduo)
```

---

## ARQUIVOS DO PROCESSO

### Skills (instruções genéricas)

| Arquivo | Passo | Descrição |
|---------|-------|-----------|
| `00_extraction.md` | 0 | Extrair o corpus do meio via conector (determinístico) + byte budgets + round-trip |
| `01_discovery.md` | 1 | Identificar entidades, tom, aliases, spoilers |
| `02_entity_resolution.md` | 2 | Classificar e unificar entidades |
| `03_knowledge_building.md` | 3 | Pesquisa colaborativa (IA + usuário) + base de conhecimento |
| `04_glossary_creation.md` | 4 | Glossário + regras de tradução |
| `04b_decision_log.md` | 4b | Registro de decisões — auditoria do processo |
| `05_translation_planning.md` | 5 | Plano de tradução por linha |
| `05b_synthetic_test_corpus.md` | 5b | Geração de suites de teste para pontos críticos |
| `06_translation.md` | 6 | Execução da tradução com controle de progresso |
| `06b_micro_qa.md` | 6b | QA por lote após cada bloco |
| `06c_correction_cycle.md` | 6c | Correções cirúrgicas pós-QA com re-validação |
| `07_qa.md` | 7 | QA final de consistência global |
| `08_reinsertion.md` | 8 | Reinserir a tradução no meio via conector + patch (determinístico, LLM só no resíduo) |
| `translation_governance.md` | — | **Carta de Governança** — contrato de qualidade (voz/lore/situação/processo) que rege os Passos 05–08 |

### Suporte do framework

| Arquivo | Descrição |
|---------|-----------|
| `../schemas/artifacts_schema.md` | Schemas formais de todos os artefatos gerados |
| `../schemas/project_schema.md` | Schema do `project.json` e dos arquivos de perfil |
| `../media-profiles/games.md` | Perfil de jogos (formato, tokens, overflow, segmentação) |
| `../media-profiles/films.md` | Perfil de filmes (stub — ponto de extensão) |
| `../media-profiles/series.md` | Perfil de séries (stub — ponto de extensão) |
| `../connectors/00_index.md` | Conceito de conector (I/O), round-trip, princípio de custo |
| `../connectors/hex_binary.md` | Conector de jogos antigos (extração/reinserção) |
| `../connectors/_skeleton/` | Esqueletos `extract.py` / `reinsert.py` / `table_schema.md` |
| `../README.md` | Guia de instanciação de projeto |

### Artifacts (outputs do processo, por projeto)

| Arquivo | Gerado em | Descrição |
|---------|-----------|-----------|
| `dialogs.csv` | Passo 0 | Corpus canônico extraído do meio (id, text_source, byte_budget) |
| `extraction_log.md` | Passo 0 | Metadados da extração + gates de round-trip e charset |
| `entities_candidates.json` | Passo 1 | Entidades brutas extraídas |
| `aliases_map.json` | Passo 1 | Mapa alias → canônico com spoiler levels |
| `terminology_clusters.json` | Passo 1 | Agrupamento por tipo de termo |
| `tone_analysis.md` | Passo 1 | Análise de tom, registros, perfis de voz (com `voice_criticality`) |
| `entities.csv` | Passo 2 | Entidades resolvidas e classificadas |
| `research_log.md` | Passo 3 | Fontes pesquisadas, conflitos resolvidos, fronteira de spoiler |
| `universe_knowledge_base.md` | Passo 3 | Base de conhecimento por entidade, com citações de fonte |
| `glossary.csv` | Passo 4 | Fonte de verdade operacional dos termos |
| `translation_rules.md` | Passo 4 | Documento normativo com justificativas |
| `decision_log.md` | Passo 4b | Registro acumulativo de decisões |
| `translation_plan.json` | Passo 5 | Plano linha a linha com intenção e risco |
| `synthetic_test_corpus.json` | Passo 5b | Casos de teste sintéticos por suite |
| `synthetic_test_results.json` | Passo 5b | Resultados das execuções de teste |
| `<corpus-fonte>` | — | Corpus source (todas as linhas, imutável) — caminho em `project.json` |
| `approved_translations.csv` | Passo 6 | Traduções aprovadas (`id_column`, `text_target`) — fonte de verdade aplicada no Passo 8 |
| `translation_status.json` | Passo 6 | Progresso + next_offset + length_warnings + needs_human_review |
| `micro_qa_log.json` | Passo 6b/6c | Log acumulativo de issues e correções por lote |
| `qa_report.md` | Passo 7 | Relatório de QA final |
| `fix_suggestions.json` | Passo 7 | Issues com sugestões de correção (input do Passo 6c) |
| binário traduzido + `patch.<fmt>` | Passo 8 | Build com a tradução gravada + patch (ips/bps/xdelta) |
| `reinsertion_report.md` | Passo 8 | Tier por string, overflows, repoints, falhas |

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
9. **Correções passam pelo Passo 06c.** Não editar `approved_translations.csv` diretamente fora do protocolo 06c.
10. **Atualização de glossário mid-project** exige identificação de impacto + agendamento de re-QA via 06c.
11. **Nenhum dado de obra específica vive nas skills.** Tudo específico vem de `project.json` + artefatos.
12. **O corpus é output do Passo 00 (extração); a tradução é devolvida no Passo 08 (reinserção).** O ciclo meio→corpus→meio é fechado.
13. **Reinserção é determinística.** LLM nunca escreve bytes nem recalcula ponteiros — só reescreve o resíduo de overflow, em lote.
14. **Toda tradução segue a Carta de Governança** (`translation_governance.md`): voz/lore/situação/processo. A IA traduz conforme a Carta; quando não consegue satisfazê-la, **sinaliza** (não improvisa).

---

## INVARIANTES DO PROCESSO

| Invariante | Verificável em |
|-----------|---------------|
| Corpus-fonte é somente leitura — nunca modificado | A qualquer momento |
| `dialogs.csv` é output do Passo 00; round-trip (extract→reinsert idêntico === original) passa | Gate do Passo 00 |
| `extract.py` e `reinsert.py` compartilham o mesmo `table_schema` | Passos 00 / 08 |
| `approved_translations.csv` casa cada `id_column` com uma linha do `dialogs.csv` | Antes do Passo 8 |
| A IA nunca escreve a tradução à mão nos dados/binário — só o script aplica o arquivo aprovado | Passos 6/8 |
| `micro_qa_log.json` contém todas as entradas desde o início | A qualquer momento |
| `decision_log.md` nunca perde entradas | A qualquer momento |
| Nenhuma tradução final usa alias de spoiler major/critical antes do reveal | QA Final |
| `research_log.md` tem `status: reconciled` antes do Passo 4 iniciar | Input Gate do Passo 4 |
| Artefatos respeitam `schemas/artifacts_schema.md`; manifesto respeita `schemas/project_schema.md` | A cada passo |

---

## CRITÉRIOS DE ACEITAÇÃO DO PROJETO

O projeto está completo quando:

- [ ] `translation_status.json` com `completion_pct: 1.00`
- [ ] `qa_report.md` com status: **aprovado** (0 issues críticos, ≤ aceitável de altos)
- [ ] `fix_suggestions.json` com todos os issues críticos com `status: applied`
- [ ] `needs_human_review` no `translation_status.json` está vazio ou todos revisados
- [ ] Nenhum `length_warning` sem revisão documentada
- [ ] `decision_log.md` atualizado com todas as decisões não-óbvias do projeto
- [ ] Passo 08 concluído: binário traduzido + patch gerados; `reinsertion_report.md` sem overflows não resolvidos
