### HLD: Benchmark do caminho de sessão

Versão: 0.1 (rascunho)
Data: 2026-10-14
Responsável: Felipe (decisão); execução pelo agente

---

### Objetivo técnico

Comparar, sobre o mesmo recorte de um projeto novo, o caminho de sessão (a IA da sessão traduz) e o caminho de
API, medindo qualidade, custo, tempo e retrabalho com os medidores que o framework já tem. Requisitos em `PRD.md`.

Dependências com outros sistemas
- Claude Code (transcrições em `~/.claude/projects/…`, de onde o `session_usage` lê o `usage` exato).
- API da Anthropic (braço de API; gasto real em `api_ledger.jsonl`).
- Projeto novo do framework com Fase 0 e glossário prontos.

---

### Arquitetura geral

Dois braços isolados, mesma fonte, mesma medição. Nada novo no caminho de produção: o benchmark só lê.

Ambiente de implantação
- Local, na máquina do operador. Sem serviço.

Tecnologias principais
- Python (módulos de `framework/runtime/`), arquivos JSONL/CSV em `projects/<p>/artifacts/`.

Padrões adotados
- Medição read-only e idempotente (cursor por transcrição no `session_usage`).
- Só contador, nome de modelo e id de cena saem das transcrições; texto de fala não é copiado.

---

### Componentes e responsabilidades

| Componente | Responsabilidades | Dependências |
| --- | --- | --- |
| Braço sessão (`session_lot.py`, `wave.py`, subagente `scene-translator`) | traduzir o recorte e fechar os gates sem API | `run_scene`, transcrições do Claude Code |
| Braço API (`run_chapter.py --backend api`) | traduzir o mesmo recorte com `model.py` | `ANTHROPIC_API_KEY`, `llm_client` |
| `session_usage.py` | tokens reais da sessão por cena, janela e overhead; marcas de fase | transcrições, `phase_marks.jsonl` |
| `cost_report.py` | gasto de API e desperdício por cena | `api_ledger.jsonl`, `run_state.json` |
| `obs_report.py` | visão por cena: estado, qualidade, tempo, retrabalho, gasto | `events.jsonl`, `metrics.jsonl` |
| `quality_sample.py` | amostra cega, taxa de erro com IC 95%, acerto da triagem | planilha julgada pelo humano |
| Relatório (`docs/benchmark_sessao/RELATORIO.md`) | tabela por braço e por variável, decisão | saída dos medidores |

---

### Fluxo de requisições e de dados

**Fluxo de requisição**
- Fixar capítulo, semente e teto de gasto da API → copiar o estado inicial para cada braço → rodar o braço
  → `session_usage sync` e `cost_report` por onda → `quality_sample export` → humano julga → `score` → relatório.

**Fluxo de dados**
- transcrição do Claude Code → `session_usage` → `api_ledger.jsonl` (`source: "session"`) → `cost_report`/`obs_report`
- chamada de API → `model.log_api_call` → `api_ledger.jsonl` → `cost_report`
- tradução verificada → `quality_sample export` → planilha cega → `score` → `qa_effectiveness.jsonl`

---

### Modelo de dados (alto nível)

Entidades principais
- Braço (sessão ou API), onda, cena, linha do `api_ledger`, marca de fase, registro de qualidade.

Relações
- Uma onda tem várias cenas; cada requisição pertence a uma cena (`agent`), a uma janela (`window`) ou ao overhead.

Fonte de verdade
- Gasto de API: `api_ledger.jsonl`. Gasto de sessão: transcrição do Claude Code. Qualidade: planilha julgada.

---

### Interfaces públicas

| Nome | Tipo | Protocolo | Exposição | SLAs/Limites |
| --- | --- | --- | --- | --- |
| CLIs dos medidores | linha de comando | argv | local | sem rede, exceto o braço de API |
| `api_ledger.jsonl` | arquivo | JSONL | local | uma linha por chamada concluída |
| `phase_marks.jsonl` | arquivo | JSONL | local | uma marca por virada de fase |

---

### Considerações de escalabilidade e disponibilidade

Abordagem geral
- Um capítulo por rodada; retomável cena a cena.

Técnicas aplicadas
- Cursor por transcrição; `--jobs N` no `run_scene` quando o braço permitir.

Meta de disponibilidade
- Não se aplica (execução manual pontual).

---

### Segurança

Autenticação
- Chave da API só em `.env` (gitignored).

Autorização
- Braço de API só com aval explícito e teto de gasto.

Proteção de dados
- Amostras, planilhas e traduções ficam gitignored; relatório versionado sem fala do jogo.

Gestão de segredos
- `.env`; nunca no repo.

---

### Observabilidade

Logs
- `events.jsonl` por cena e etapa.

Métricas
- Tokens por categoria (`agent`/`window`/`overhead`), USD equivalente, erro do medidor (`out_est`), taxa de erro com IC.

Tracing
- Não se aplica.

Dashboards e alertas
- `obs_report.py` e `cost_report.py --summary`.

---

### Riscos arquiteturais e mitigação

#### Atribuição `window` aproximada distorce o custo por cena
- **Probabilidade:** média
- **Impacto:** custo por cena impreciso (o total por sessão segue exato)
- **Mitigação:**
  - Comparar totais por braço e por onda, não por cena.
  - Preferir subagente por cena no braço de sessão.
- **Plano de contingência:** declarar o erro no relatório.

#### Transcrição apagada do disco
- **Probabilidade:** baixa
- **Impacto:** custo da onda incompleto
- **Mitigação:**
  - `session_usage sync` ao fim de cada onda.
- **Plano de contingência:** repetir a onda.

---

### ADRs e próximos passos

ADRs associados
- `docs/adr/0004-model-agnostic-interface.md` (interface de modelo).

Decisões pendentes
- Capítulo do recorte e teto de gasto da API (dependem do projeto novo).

Próximos passos
- Escolher o projeto novo; fazer o ensaio de uma cena por braço; rodar o recorte; escrever `RELATORIO.md`.
