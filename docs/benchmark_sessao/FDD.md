### FDD: Benchmark do caminho de sessão — protocolo de execução

Versão: 0.1 (rascunho)
Data: 2026-10-14
Responsável: Felipe (decisão); execução pelo agente

---

### 1. Contexto e motivação técnica

O HLD define dois braços medidos pelos mesmos módulos. Este documento fixa o protocolo: o que roda, em que ordem,
o que se registra e quando o resultado vale. Atores: operador (Felipe), agente da sessão, subagentes
`scene-translator`, humano que julga a amostra.

---

### 2. Objetivos técnicos

- Os dois braços partem do mesmo estado (TM, glossário, decisões de voz) e do mesmo recorte.
- Cada requisição de modelo entra uma só vez na contabilidade (invariante do `session_usage`).
- Erro do medidor impresso no relatório (`out_est` sobre a saída total).
- Amostra de qualidade com mesma semente e mesmo N nos braços.

---

### 3. Escopo e exclusões

**Incluído**
- Protocolo, variáveis do braço de sessão, relatório.

**Excluído**
- Código novo de medição (só se faltar um número no `obs_report`).
- Mudança de gates, prompts ou doutrina durante a rodada.

---

### 4. Fluxos detalhados e diagramas

**Fluxo principal**
1. Definir capítulo, semente (`--seed`), N da amostra, teto de gasto da API. Registrar em `RELATORIO.md`.
2. Copiar o estado inicial para dois diretórios de trabalho (um por braço). TM isolada.
3. Ensaio: uma cena por braço; conferir que `session_usage sync` e `cost_report` enxergam os dois.
4. `session_usage.py mark <projeto> bench_<braço>_<variável>` antes de cada rodada.
5. Braço de sessão, por variável (uma de cada vez):
   - V0 base: ~13 comandos por onda;
   - V1 `wave.py` (um comando por onda);
   - V2 ondas menores com `/clear` entre elas;
   - V3 Sonnet traduz, Opus retrotraduz (já é o padrão do bof4: serve de controle);
   - V4 Haiku só para rótulo curto;
   - V5 lote de correção automático.
6. Braço de API: `run_chapter.py <projeto> <cap> --backend api`, só com aval.
7. Ao fim de cada onda: `session_usage.py sync`, `cost_report.py --summary`; ao fim do braço: `obs_report.py`.
8. `quality_sample.py export <projeto> --n N --seed S` por braço; humano julga; `score --reviewer NOME`.
9. Preencher a tabela do `RELATORIO.md`; decidir por variável.

**Fluxos alternativos e exceções**
- Gate bloqueou: resolver a causa (nunca flag de bypass); a cena fica registrada como retrabalho.
- Cena que não fecha: falha registrada; não sai do recorte.
- Segunda rodada: inverter a ordem dos braços.

**Diagramas**
- Ver `docs/DIAGRAMAS.md` (C4 e sequência de uma cena no caminho de sessão).

---

### 5. Contratos públicos (assinaturas, endpoints, headers, exemplos)

**Medidores** (já existentes)
- Tipo: CLI
- `python framework/runtime/session_usage.py mark|sync <projeto> [<fase>]`
- `python framework/runtime/cost_report.py <projeto> [--by-scene] [--json] [--summary]`
- `python framework/runtime/obs_report.py <projeto> [--json] [--scene CENA]`
- `python framework/runtime/quality_sample.py export <projeto> [--n 200] [--seed q1]` / `score <projeto> --reviewer NOME [planilha.csv]`

**Tabela do relatório (modelo)**

| Variável | Erro (IC 95%) | Tokens/USD equiv. | Tempo | Retrabalho | Erro do medidor | Decisão |
| --- | --- | --- | --- | --- | --- | --- |
| V0 … V5, API | — | — | — | — | — | entra / não entra |

---

### 6. Erros, exceções e fallback

- Falha de ambiente (comando sai ≠ 0): parar e resolver; não seguir com medida parcial.
- Transcrição ausente: custo incompleto; declarar no relatório.
- IC largo: ampliar N e reamostrar antes de concluir.
- Invariantes: braços isolados; semente e N fixos; gates fechados em todas as cenas contadas.

---

### 7. Observabilidade

**Métricas**
- Tokens por categoria, USD equivalente, tempo por etapa, reprovas e retraduções por cena, taxa de erro com IC.

**Logs**
- `events.jsonl`, `api_ledger.jsonl`, `phase_marks.jsonl`, `qa_effectiveness.jsonl`.

**Tracing**
- Não se aplica.

**Dashboards e alertas**
- `obs_report.py` por braço.

---

### 8. Dependências e compatibilidade

| Componente | Versão mínima | Observações |
| --- | --- | --- |
| Claude Code | atual | formato da transcrição lido pelo `session_usage` |
| `anthropic` (SDK) | conforme `requirements*.txt` | só o braço de API |
| Python | o do CI | — |

**Garantias de compatibilidade**
- Mesmo contrato `translate`/`back_translate` nos dois braços (`docs/MODEL_INTERFACE.md`).

---

### 9. Critérios de aceite técnicos

- Todas as cenas do recorte `verified` nos dois braços, ou falha registrada.
- `session_usage sync` rodado ao fim de cada onda; total por sessão confere com a transcrição.
- Relatório com todas as colunas da tabela preenchidas e o erro do medidor declarado.
- `content_guard` OK no commit do relatório.

---

### 10. Riscos e mitigação

### Variáveis misturadas numa mesma rodada
- **Probabilidade:** média
- **Impacto:** não dá para atribuir o ganho
- **Mitigação:**
  - Uma variável por rodada; marca de fase própria.
- **Plano de contingência:** refazer a rodada isolando a variável.

### Gasto da API acima do previsto
- **Probabilidade:** baixa
- **Impacto:** custo real
- **Mitigação:**
  - Teto definido antes; `budget.py` ligado; ensaio de uma cena.
- **Plano de contingência:** parar o braço e relatar o que foi medido.
