### PRD: translation-cognition-framework — Benchmark do caminho de sessão

Versão: 0.1 (rascunho)
Data: 2026-10-14
Responsável: Felipe (decisão); execução pelo agente

Origem: item 3 do "Pós-bof4" em `docs/ROADMAP.md` e bloco 3 do levantamento em `projects/bof4/ROADMAP.md`.
Texto de fala do jogo não entra aqui nem em nenhum artefato versionado do benchmark.

---

### Resumo

O bof4 foi traduzido pelo caminho de sessão (a IA da sessão traduz, sem API): 305 cenas, 27.021 falas, $0 de API
(equivalente a $239). Esse caminho nasceu junto com o processo, então não há medida limpa dele contra o caminho de
API. O benchmark roda o mesmo recorte pelos dois caminhos num projeto novo e mede qualidade, custo, tempo e
retrabalho. Só entra no framework o que o benchmark mostrar ganho.

---

### Contexto e problema

Público-alvo
- Quem opera o framework num projeto novo e escolhe o caminho (assinatura/sessão ou API).
- Quem mantém o framework e decide o que sobe do bof4.

Cenários de uso chave
- Escolher o caminho do projeto novo com número, não com impressão.
- Decidir se uma otimização do bof4 (onda em um comando, `/clear` entre ondas, modelos por papel) vale levar.

Onde essa feature será implantada
- Medição fora do pipeline de produção: scripts de leitura sobre os artefatos do projeto novo. Nenhum passo do
  pipeline muda por causa do benchmark.

Problemas priorizados
- Sem comparação limpa entre os caminhos (alta): o bof4 construiu o processo enquanto traduzia; $227 dos $239 foram orquestração e construção.
- Gargalo no Pro é a orquestração na janela principal (alta): ~13 comandos por onda, cada um relê o contexto.
- Qualidade medida só no bof4 (média): 14,5% de erro na amostra antes das correções (26,1% pesada por repetição).

---

### Objetivos e métricas

| Objetivo | Métrica | Meta |
| --- | --- | --- |
| Comparar qualidade entre caminhos | taxa de erro da amostra cega (`quality_sample`), com IC 95% | sessão não pior que API além do IC |
| Comparar custo | tokens lidos da transcrição (sessão) vs `api_ledger` (API), em USD equivalente | relatar; ganho exigido só para o que for levado |
| Medir o gargalo de orquestração | tokens de `overhead` e `window` por onda (`session_usage`) | queda mensurável com onda em um comando |
| Comparar tempo e retrabalho | `events.jsonl` por etapa; reprovas e retraduções por cena | relatar |
| Declarar o erro da medição | `out_est` / total de saída (erro do medidor) | impresso no relatório |

---

### Escopo

Incluso
- Um recorte (um capítulo) do projeto novo, traduzido do zero pelos dois caminhos, mesma TM e mesmo glossário no início.
- Variáveis do caminho de sessão: um comando por onda (`wave.py`) vs ~13; ondas menores com `/clear` entre elas;
  Sonnet traduz e Opus retrotraduz; Haiku só para rótulo curto; lote de correção automático.
- Relatório com os números e a decisão por variável (entra / não entra).

Fora de escopo
- Mudar o pipeline, os gates ou o prompt durante a rodada.
- Tradução do jogo inteiro pelos dois caminhos.
- Benchmark de modelo da API (já feito: `docs/MODEL_INTERFACE.md`, Sonnet aprovado).
- Qualquer bypass de gate para ganhar tempo.

---

### Requisitos funcionais

#### BS-1 Recorte comparável
Mesmo capítulo, mesmo estado inicial, nos dois caminhos.

**Fluxo principal**
- Fixar o capítulo e a semente da amostra (`--seed`) antes de começar.
- Copiar o estado inicial (TM, glossário, decisões de voz) para cada braço.
- Rodar cada braço até todas as cenas `verified`.

**Fluxos alternativos e exceções**
- Cena que não fecha num braço fica registrada como falha, não é trocada nem retirada.

**Erros previstos**
- TM contaminada entre braços (um braço escreve na TM do outro).

**Prioridade:** alta

---

#### BS-2 Medição de custo e tempo
**Fluxo principal**
- Marcar a fase de cada rodada (`session_usage.py mark <projeto> <fase>`).
- `session_usage.py sync` e `cost_report.py` ao fim de cada onda; `obs_report.py` ao fim do braço.

**Fluxos alternativos e exceções**
- Mensagem de subagente sem `usage` final: saída estimada (`_OUT_FIT`); o relatório mostra o erro.

**Erros previstos**
- Transcrição de sessão antiga apagada do disco: custo daquela onda fica incompleto (declarar).

**Prioridade:** alta

---

#### BS-3 Qualidade cega
**Fluxo principal**
- `quality_sample.py export` por braço, mesma `--seed` e mesmo N; humano julga sem saber o braço.
- `quality_sample.py score` grava a taxa de erro com IC 95%.

**Erros previstos**
- Amostra pequena demais para separar os braços (IC largo): ampliar N antes de concluir.

**Prioridade:** alta

---

#### BS-4 Relatório e decisão
**Fluxo principal**
- Tabela por braço e por variável: erro, custo, tempo, retrabalho, erro do medidor.
- Decisão registrada por variável; o que ganhar sobe para o framework, o resto vira nota.

**Prioridade:** média

---

### Requisitos não funcionais

Performance
- O benchmark não pode acrescentar passo ao caminho medido.

Segurança e autorização
- Braço de API gasta dinheiro: só roda com aval explícito do Felipe e teto de gasto definido antes.

Observabilidade
- Só contadores, nomes de modelo e ids de cena saem das transcrições (regra do `session_usage`).

Confiabilidade e integridade de dados
- Execução resumível; `session_usage` é idempotente por cursor.

Compliance
- Relatório e artefatos versionados sem fala do jogo; amostras e planilhas ficam gitignored.

---

### Arquitetura e abordagem

Abordagem
- Reaproveitar o que já mede: `session_usage`, `cost_report`, `obs_report`, `quality_sample`, `wave`. Não escrever
  medidor novo; se faltar um número, acrescentar ao `obs_report`.

Componentes
- Braço sessão: `session_lot.py` + `wave.py` + subagentes `scene-translator`.
- Braço API: `run_chapter.py --backend api`.
- Medição: ver `HLD.md`.

### Decisões e trade-offs

#### Decisão: um capítulo, não o jogo
- **Justificativa:** o braço de API custa dinheiro e o de sessão custa cota; um capítulo já separa as variáveis.
- **Trade-off:** um capítulo pode não representar o jogo (gêneros de cena, repetição).

#### Decisão: medir com o que existe
- **Justificativa:** menos código novo, números comparáveis com o bof4.
- **Trade-off:** a atribuição `window` é aproximada.

---

### Dependências

#### Projeto: instância nova do framework
Precisa existir com Fase 0 (extração) e glossário prontos. Ainda não existe; sem ele o benchmark não começa.

#### Humano: julgamento da amostra
Quem julga a amostra cega é o Felipe (ou revisor indicado); sem isso não há número de qualidade.

---

### Riscos e mitigação

#### Ruído maior que a diferença entre braços
- **Probabilidade:** média
- **Impacto:** conclusão sem base
- **Mitigação:**
  - Mesmo recorte, mesma semente, N suficiente para IC estreito.
  - Declarar o IC no relatório.
- **Plano de contingência:** repetir com outro capítulo antes de decidir.

#### Aprendizado do braço rodado primeiro contamina o segundo
- **Probabilidade:** alta
- **Impacto:** o segundo braço parece melhor
- **Mitigação:**
  - Estado inicial copiado e isolado por braço; ordem dos braços alternada se houver segunda rodada.
- **Plano de contingência:** relatar o viés de ordem.

---

### Critérios de aceitação

- Os dois braços com todas as cenas do recorte `verified` (ou falha registrada).
- Qualidade, custo, tempo e retrabalho por braço e por variável, com erro do medidor declarado.
- Decisão registrada por variável; item 3 do ROADMAP marcado `[x]` com link para o relatório.
- `content_guard` OK; nada de fala do jogo versionado.

---

### Testes e validação

Tipos de teste obrigatórios
- Os testes existentes dos módulos de medição seguem verdes; nenhum módulo novo sem teste.

Estratégia de validação
- Ensaio curto (uma cena por braço) antes da rodada completa, para conferir que o medidor enxerga os dois caminhos.
