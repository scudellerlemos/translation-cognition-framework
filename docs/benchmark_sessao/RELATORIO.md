# Relatório — benchmark de cota da assinatura Pro

Rascunho vivo, atualizado a cada braço. Protocolo em `FDD.md`. Só ids de cena e números (sem fala do jogo).

## Parâmetros fixos

- Projeto: `utawarerumono_prelude`. Estado inicial: snapshot B2 (`output/bench_b2_inicial`, fora do git).
- Recorte: 6 cenas, 267 falas (`00_00_04`, `00_01_01`, `00_03_01`, `00_03_02`, `00_04_04`, `00_90_01`), `--seed 42`.
- Cada braço roda em `output/bench_<braço>/` (fora do git), com série de TM própria.
- Cota real: `/usage` lido antes e depois (sem medidor automático). Os pontos percentuais incluem também a
  conversa principal da sessão, então valem como teto do braço e não como medida exata.

## Montagem de um braço (lições do V0a)

Itens que o `mk_arm.py` não cobria e que travaram os subagentes (cada tentativa perdida custou ~12 mil tokens por subagente):

1. `hitl.py accept-scope` e `choose-path` por braço (decisão humana, roda o usuário);
2. `artifacts/research_log.md` copiado do projeto real (gate de cobertura da KB);
3. `connector/build_plan_chapter.py` (`ROOT.parents[3]`) e `connector/extract.py` (`parents[5]`) com a raiz do repo
   corrigida para a profundidade `output/bench_<braço>/connector`;
4. `run_state.json` vazio e `dialogs.csv` só das cenas do recorte.

## Tabela

| Variável | Falas | Cenas | USD equiv. | USD/fala | Requisições | /usage sessão | /usage semana | Retrabalho | Decisão |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V0a (ensaio) | 267 | 6 | 2,02 | 0,0076 | 137 | 46% → 65% (+19 pp) | 23% → 25% (+2 pp) | 3 lançamentos perdidos por montagem; 5 pré-checks de `\n` e bytes refeitos | referência, não linha de base |
| V0b (base limpa) | 267 | 6 | 1,17 | 0,0044 | 147 | 68% → 75% (+7 pp) | 27% → 28% (+1 pp) | 4 pré-checks de `\n` e 1 nome omitido refeitos; 0 bloqueios de ambiente | linha de base provisória |
| V0c (repetição limpa) | 267 | 6 | 1,38 | 0,0052 | 158 | 75% → 89% (+14 pp) | 28% → 29% (+1 pp) | 5 execuções refeitas por `
`/bytes; 0 bloqueios de ambiente | par com o V0b: mede o ruído |
| V6 (3 subagentes: 4 cenas + 1 + 1) | 267 | 6 | 0,88 | 0,0033 | n/d | 0% → 6% (+6 pp) | 30% → 31% (+1 pp) | 1 fala refeita por `\n` (`00_03_01:3`); 0 bloqueios de ambiente | ~31% abaixo da média V0b/V0c; passa do ruído (~20%) por pouco, confirmar com V6b |
| V6b (repetição do V6) | 267 | 6 | 1,01 | 0,0038 | n/d | 6% → 12% (+6 pp) | 31% → 32% (+1 pp) | 1 fala refeita por `\n` (`00_03_01:3`); 2 falas encurtadas por bytes na `00_01_01`; 1 linha de interjeição escrita por subagente no `decision_log.md` do braço (efeito desprezível) | V6 e V6b: média US$ 0,95, ~26% abaixo de V0b/V0c; ganho confirmado |
| V7 (roteiro enxuto, mesmos 3 grupos; base com `Mmm`=`Hmm...` e convenção de interjeição) | 267 | 6 | 1,10 | 0,0041 | n/d | 12% → 32% (+20 pp) | 32% → 35% (+3 pp) | `\n` real no lugar do literal nos 3 subagentes (JSON regenerado); 13, 8 e 6 falas acima do orçamento pegas pelo script; `wave` 6x (grupo A), 4x (`00_01_01`), 2x (`00_03_02`); `wave` aceitou `00_90_01:3` com 2 bytes acima do orçamento | sem ganho sobre o V6 (dentro do ruído); +20 pp de sessão e +3 pp de semana destoam do ledger; o V7b (+7 pp, +1 pp) mostrou que foi a conversa principal |
| V7b (repetição do V7, conversa principal quieta) | 267 | 6 | 1,03 | 0,0039 | n/d | 32% → 39% (+7 pp) | 35% → 36% (+1 pp) | `\n` real no lugar do literal em 2 de 3 subagentes; 23 falas encurtadas por bytes antes do `wave` (grupo A) e 7 rodadas de correção na `00_03_02`; `wave` 6x / 2x / 5x; 0 bloqueios de gate | sem ganho sobre o V6; +7 pp confirma que o +20 pp do V7 foi a conversa principal, não o roteiro |
| V9 (Haiku nos 3 grupos do V6; base sem convenção de interjeição) | 267 | 6 | 0,34 | 0,0013 | n/d | 39% → 41% (+2 pp) | 36% → 36% (0 pp) | 6 falas refeitas na `00_03_01`; `
| V9b (V9 + regra "nunca omitir verbo ou palavra de conteúdo para caber nos bytes") | 267 | 6 | 0,33 | 0,0012 | n/d | 49% → 52% (+3 pp) | 37% → 38% (+1 pp) | 2 falas com `escalate` na `00_04_04` (tratamento cortado por byte); qualidade (`--n 120 --seed 42`, às cegas): 2,5% → 1,7% de erro (2/120; IC 95% 0,5 a 5,9%); 55 das 120 reaproveitam veredito do V9/V6 (mesma fonte e tradução); o erro de omissão de verbo (`00_01_01:6`) não reapareceu |
| V9c (Haiku + regra do V9b, cena longa `10_80_00`, cap 10, 197 falas, 1 subagente) | 197 | 1 | 0,33 | 0,0017 | n/d | 53% → 54% (+1 pp) | 38% → 38% (0 pp) | 2 `escalate` (`:69` "Nao" sem acento por byte, `:71` "também" cortado); qualidade (`--n 120 --seed 42`, às cegas): 0,0% de erro (0/120; IC 95% 0,0 a 3,1%), 2 falas `medium` extras também ok; o `:69` "Nao" foi julgado ok pelo usuário |
` real em 1 subagente; 1 `escalate` (`00_90_01:2`); 1 falante `unknown`; Haiku usou 275k tokens de subagente (2x o Sonnet) | ~65% abaixo do V6 no ledger e +2 pp de sessão: maior ganho até aqui; qualidade (40 falas às cegas, `--seed 42`): V9 2,5% de erro (3/120; IC 95% 0,9 a 7,1%) contra V6 3,3% (4/120; IC 1,3 a 8,3%); `--n 120 --seed 42`, 40 falas da primeira rodada reaproveitadas; sem diferença detectável. Erros do V9: omissão de verbo por corte (`00_01_01:6`), 2 outros; os 4 do V6 são de nuance de tradução |
| V8 (fechado por análise, sem braço) | — | — | — | — | — | — | — | Glossário e vozes já saem só da cena (0,1 a 0,8 KB e 1,3 a 1,5 KB). Sobra a Carta de governança, 8 KB fixos por cena (~2 mil tokens; 50% do prompt de cena curta, 30% de cena longa). Cortá-la pela metade economiza ~4 KB por cena (~6 mil tokens de entrada em 6 cenas, quase tudo em cache), 2% a 5% dos ~264 mil tokens de subagente do V9b: abaixo do ruído de ~20% do ledger, indetectável por braço. Decisão do usuário (2026-10-19): fechar por análise. Se algum dia valer: V8' = Carta resumida em cópia isolada do `pack_render.py`, com pontuação cega |

## Observações do V0a

- 6 cenas `verified`, 267 de 267 falas, `quality_gate` sem pendência, nenhuma fala `high`, sem retrotradução.
- 3 candidatos na fila diferida de escalonamento (não resolvidos; decisão do usuário).
- Sem convenção no `decision_log.md` para suspiro, bocejo, risada e onomatopeia: cada subagente improvisou.
- Falante de várias falas inferido do contexto (`npc` quando sem voice card).
- Os +19 pp de sessão incluem a conversa principal e as tentativas perdidas; o V0b (ambiente já corrigido) é o primeiro número limpo.

## Observações do V0b e V0c (base limpa)

- Mesma configuração, mesmas 267 falas: o ledger deu US$ 1,17 e US$ 1,38 (18% de diferença) e 147 e 158 requisições (7%).
- O `/usage` de sessão deu +7 pp e +14 pp: o dobro de uma rodada para a outra. O medidor percentual é grosso (passo de 1 pp)
  e inclui a conversa principal, então só dá para ver diferença grande. O ledger é o número confiável para comparar braços.
- Consequência para V6 a V9: ganho abaixo de ~20% no ledger não se distingue de ruído; no `/usage`, abaixo de ~2x também não.
- Sem convenção de interjeição/onomatopeia no `decision_log.md` (aparece nos três braços).
- Glossário: `Mmm` com regra `traduzir` e alvo placeholder `(adaptar)` faz o lint acusar 2 candidatos na `00_03_01` em todo braço;
  bloqueia o `--fechar`. Decisão do usuário (alvo concreto ou excluir interjeição do lint).

## Retomada (para a próxima sessão)

Estado em 2026-10-19: V0a (ensaio), V0b, V0c (base limpa), V6 e V6b fechados (agrupar cenas curtas rende ~26% no ledger, confirmado). V7 e V7b fechados (roteiro enxuto no prompt: sem ganho, adotar só como código, V10). V9, V9b e V9c fechados (Haiku: custo ~65% menor; qualidade sem diferença detectável com n=120 nos três; V9c confirma em cena longa de outro capítulo, 0/120; falas `high` são só 6 de 13.723 e ficam no Sonnet por regra). Pendências do usuário: fila diferida (`Mmm`, `10_80_00:69` e `:71`). V8 fechado por análise (hipótese já implementada; teto restante ≤5%, indetectável). V10, V11, V13, V14 e V15 fechados por medição (ver tabela de ideias); V12 medido (headless não economiza cota); V16 não rodado. **Benchmark encerrado em 2026-10-19: ver "Conclusão" no fim.**
A partir do V7 o snapshot B2 já traz `Mmm` = `Hmm...` no glossário e a convenção de interjeição no `decision_log.md` (decisão do usuário, 2026-10-19): a régua muda em relação ao V0b/V0c e ao V6.

**Criar um braço**
1. `python docs/benchmark_sessao/mk_arm.py <nome>` a partir da raiz do repo (cria `output/bench_<nome>/` a partir do snapshot B2; falha se já existir).
2. `python framework/runtime/hitl.py accept-scope projects/utawarerumono_prelude/output/bench_<nome> --reviewer Felipe`
3. `python framework/runtime/hitl.py choose-path projects/utawarerumono_prelude/output/bench_<nome> in-session --reviewer Felipe`
4. `python framework/runtime/session_usage.py mark projects/utawarerumono_prelude/output/bench_<nome> 3` (rótulo numérico).
5. Perguntar o `/usage` (sessão e semana) antes; lançar os `scene-translator`; ao fim, `wave.py <braço> --backend in-session`
   sem cenas, `obs_report.py <braço>` e o `/usage` depois. Os passos 2 a 4 são decisão do usuário: só rodam com ordem dele.

**Prompt do subagente** (modelo usado no V0b/V0c): raiz do repo; caminho completo do braço; cena e nº de falas; comando
`python framework/runtime/wave.py <braço> <cena> --backend in-session` sem `export`, `cd` nem pipe; armadilhas
(`\n` literal contado por fala, `byte_budget`, interjeição pelo `decision_log.md`, `lore_novo`/`escalate`); parar sem contornar
gate de ambiente.

**Variáveis**
- V6: um subagente por grupo de cenas curtas (≤ 60 falas cada, soma ≤ 150). No recorte: `00_00_04`+`00_90_01`+`00_03_01`+`00_04_04`
  (17+4+53+46 = 120) é um grupo; `00_01_01` (57) e `00_03_02` (90) ficam sozinhas, ou `00_01_01`+`00_03_01`+... se couber na soma.
- V7: roteiro de poucas voltas por cena (JSON uma vez, conferência por script, sem reler o prompt).
- V9: Haiku nas falas curtas de baixo risco (qualidade: `quality_sample.py export <braço> --n 40 --seed 42`, o usuário pontua às cegas).
- V8: `scene_prompt` enxuto (glossário e vozes só do que aparece na cena). Exige mudança de código só numa cópia isolada; pedir antes de tocar o framework.

**Como ler**
- Comparar pelo ledger (`cost_report.py --summary`, linha "fase 3"), não pelo `/usage`. Ruído medido: ~20% no ledger.
- Régua: V0b US$ 1,17 / 147 req; V0c US$ 1,38 / 158 req; média ~US$ 1,28 e ~150 req para 267 falas.
- Ritmo: cada braço custa ~7 a 14 pp de sessão; começar com a sessão baixa (reset) para não estourar no meio.

**Pendências do usuário**
- 3 candidatos na fila diferida do V0a e 2 por braço (falas `Mmm`) no V0b/V0c: não resolvidos.
- Decidir: alvo concreto para `Mmm` no glossário (hoje placeholder `(adaptar)`) ou excluir interjeição do lint.
- Decidir: convenção de interjeição/onomatopeia no `decision_log.md`.
- Fora do benchmark: ainda não sabemos quando/onde a sessão estoura nos lotes reais (meio da onda ou entre ondas).

## Ideias novas de braço (levantadas em 2026-10-19)

Motivo: viabilizar o framework na assinatura Pro. Leitura dos números do V0: a **semana** sobe ~1,3 pp por 267 falas
(jogo inteiro ≈ 115% da semana, pouco mais de uma semana); a **janela de sessão** é o gargalo (~10 pp por 267 falas ≈ 9 janelas).
Estimativas grossas (medidor de 1 pp), sem dado ainda sobre as 23.933 falas já feitas.

| Id | Variável | O que muda | Mede | Observação |
| --- | --- | --- | --- | --- |
| V10 | Retrabalho de gate | script que calcula `\n` e limite de bytes antes do `wave` | execuções refeitas e requisições por braço | V0c teve 5 execuções refeitas só por `\n`/bytes | **Fechado por medição (2026-10-19), sem braço: nos eventos dos braços recentes o `build_plan` falhou 1 a 2 vezes por braço (V6 1, V7 1, V9b 2, V9c 1) em 6 a 12 execuções; cada falha custa uma volta do subagente. Teto do V10 = 1 a 2 voltas por braço, abaixo do ruído; script não compensa. (O `gate.connector` aparece `block` em todos os braços por exigir `UTAP_DATA_DIR` para o texto residual; independe do braço e da cena.)**
| V11 | Custo fixo | cena de 1 fala (overhead puro do subagente); depois `scene-translator.md` e prompt fixo enxutos | tokens por subagente | base ~30 a 37 mil tokens; dá o valor de cada agrupamento | **Medido (2026-10-19, `99_00_12`, 1 fala, Sonnet): US$ 0,076 equivalente (fase 3), 83 mil tokens com cache, 5 chamadas; `/usage` 59→60 sessão, 38→39 semana. Duas rodadas gastas em retrabalho (ledger ainda inexistente na 1ª rodada do `wave`; `\n` e 51 bytes errados antes de acertar), que é o alvo do V10.**
| V12 | Condução sem conversa | `rodar_ondas.ps1` (uma sessão `claude -p` por onda) no lugar da sessão interativa | parcela do `/usage` que é só conversa | mesma tarefa | **Medido (2026-10-19, `bench_v12`, 6 cenas, 267 falas, `rodar_ondas_v12.ps1` = cópia isolada do script, 1 onda `claude -p` Sonnet): ledger US$ 1,55 equivalente (fase 3), 64 a 67 requisições, overhead 14%; `/usage` sessão 20→35 (+15 pp), semana 41→42 (+1 pp). Contra o V0b/V0c (US$ 1,28 média; +7 a +14 pp de sessão): sem ganho, e a sessão ficou no topo da faixa. Contra o V6 (US$ 0,88 a 1,01): mais caro, o modo headless não agrupou as cenas curtas. Decisão: o modo headless não economiza cota; vale pela autonomia (sem humano na onda), não pelo custo. Primeira tentativa (2026-10-19) rodou no projeto real por engano: a skill leu `projects/<nome>` como o projeto real e ignorou `-Projeto`; 351 falas, +15 pp de sessão e +1 pp de semana, revertida a pedido do usuário. Correção: o prompt da cópia isolada define `<nome>` como o caminho do braço.** |
| V13 | Reuso de cache | um subagente em sequência (ou retomado com `SendMessage`) vs. cinco em paralelo | requisições e USD equiv. | complementa o V6 | **Medido (2026-10-19, recorte de 6 cenas, 1 subagente Sonnet em sequência): US$ 0,89 equivalente (fase 3), 22 requisições; semana 39→39 (0 pp); sessão sem leitura útil (resetou no meio, 61→2). Contra o V6 (3 subagentes) US$ 0,88 e V6b US$ 1,01: sem diferença acima do ruído de ~20%. 3 falas com `\n` refeitas. Decisão: agrupamento em um ou três subagentes é indiferente em custo; manter o do V6.**
| V14 | Menos falas ao modelo | pré-preencher por memória de tradução / quase duplicata | fração de falas sem modelo (ex.: 8 de 90 na `00_03_02`) | contar antes de implementar | **Fechado por medição (2026-10-19): o `_select_reuse` já cobre 20,3% das falas do projeto (repetição entre cenas); fica de fora 2,0% (repetição só dentro da cena, de propósito) e 0,38% (falas sem letra). Teto ~2,4%, abaixo do ruído; não implementar.**
| V15 | Saída enxuta | JSON curto (omitir `speaker`/`risk` padrão) | tokens de saída por fala | saída custa mais que cache | **Fechado por medição (2026-10-19), sem braço: no V13 o JSON das 267 falas pesa 36,5 KB (`t` 25%, `tone_register` 19%, `intent` 15%, `speaker` 14%, `risk_level` 14%). Cortar `tone_register` e `intent` tira ~12 KB, estimados em 3 a 4 mil tokens, contra 47 mil tokens de saída do subagente (~8%); o ganho em USD fica abaixo do ruído de ~20%. Além disso `tone_register` alimenta o embedder da TM semântica e ambos vão para o banco: cortar muda dado que o pipeline usa. Não implementar.**
| V16 | Ritmo e retomada | parar no limite e retomar pelo `run_state` | retrabalho após estouro de janela | meta: estouro custa zero | **Não rodado, por decisão do usuário (2026-10-19): só se mede num estouro real da janela, que não se provoca de propósito. Fica como observação para os lotes reais: anotar onde a sessão estoura (no meio da onda ou entre ondas) e se a retomada pelo `run_state` custa retrabalho.**

**Ordem proposta:** V10 e V11 antes de V6 (baratos, sem mexer em qualidade, mostram quanto sobra para as outras alavancas);
depois V6, V12, V13. V14 e V16 só depois de medir a fração do V14. V7, V8 e V9 seguem como estavam; V8 e V9 pedem pontuação cega do usuário.
V10, V11, V15 e V8 exigem código novo ou mudança de prompt: só em cópia isolada do braço, perguntar antes de tocar o framework.

## Achados de framework durante o benchmark (2026-10-19)

- `opcodes.segments` não tratava como quebra o `\n` literal declarado em `control_codes` com papel `quebra_de_linha`: o lint `largura` media a fala inteira como uma linha (1.795 falsos bloqueios no projeto). Corrigido, com teste.
- `pattern_lint` passou a marcar `largura` só onde a fonte tem quebra do autor (linha única = o motor quebra). Corrigido, com teste. Antes, o `quality_sample export` era barrado em todo braço.


## Conclusão (2026-10-19)

Alavancas que valem, em ordem de ganho medido pelo ledger (fase 3, recorte de 6 cenas, 267 falas):

1. **Haiku nas falas `low`/`medium` (V9, V9b, V9c):** ~65% menos custo (US$ 0,33 a 0,34 contra US$ 0,88 a 1,01 no Sonnet). Qualidade cega sem diferença detectável com n=120 (0 a 3 erros por braço, IC 95% contido em 0 a 7%). Falas `high`/`critical` ficam no Sonnet por regra (6 de 13.723 no projeto real). Haiku corta conteúdo por limite de bytes de vez em quando, mas sempre sinaliza com `escalate`: política é aceitar o corte sinalizado.
2. **Agrupar cenas curtas por subagente (V6, V6b):** ~26% menos custo contra o V0. Um subagente só ou três é indiferente (V13: US$ 0,89 contra US$ 0,88 e US$ 1,01).

Alavancas que NÃO valem (abaixo do ruído de ~20% do ledger ou piores):

- Roteiro enxuto (V7, V7b), prompt de cena enxuto (V8: glossário e vozes já saem só da cena; sobra a Carta, teto ≤5%), script de conferência (V10: 1 a 2 voltas por braço), pré-preenchimento por TM (V14: reuso entre cenas já cobre 20,3%; resto ~2,4%), saída em JSON mais curto (V15: ~8% da saída, e os campos alimentam o embedder e o banco), modo headless `claude -p` (V12: mais caro, sem agrupar; vale por autonomia, não por cota).
- Custo fixo do subagente (V11): US$ 0,076 por subagente com 1 fala; já diluído pelo agrupamento.

Ordem de grandeza para o projeto real: semana ~1,3 pp e sessão ~2 a 10 pp por 267 falas conforme o braço; com Haiku + agrupamento a sessão ficou em +2 a +3 pp (V9, V9b) e +1 pp (V9c, cena longa) e a semana em 0 a +1 pp. Estimativa grossa (medidor de 1 pp).

Pendências fora do benchmark (estado em 2026-10-19):

- **Brecha do gate de bytes: não é brecha.** `byte_budget` não é limite duro neste motor: o membro é reconstruído (`space_strategy: reconstrucao_secao`, `table_schema.md` seção 3) e o limite real é a largura da caixa. Nos braços há de 0 a 15 falas por braço acima do `byte_budget - 1` e todas fecharam `verified`. O `wave` só trata `byte_budget` como alvo de encurtamento.
- **Convenção de interjeição:** o `decision_log.md` do projeto real já a tem (usuário, 2026-10-14: interjeição fora do glossário, adaptar mantendo comprimento). A diferença é só do snapshot B2, que traz `Mmm` = `Hmm...` no glossário. O glossário real não tem `Mmm`.
- **Correções de lint:** `opcodes.py` e `pattern_lint.py` (com testes) commitados na branch `feat/onda4-estrutura` (a026eac, sem push). A correção do alvo `(adaptar)` do `glossary_lint.py` e o teste dela ficam no trabalho da fila diferida (ADR 0020), ainda sem commit, porque o mesmo arquivo carrega `--fechar`, que depende do `hitl.py`.
- **`UTAP_DATA_DIR`:** com a variável apontando para o `DataBase2.sdat`, o `gate.connector` passa (projeto real e braço). Falta só setá-la no ambiente do usuário.
- **Regra do Haiku no fluxo real:** adotada pelo usuário em 2026-10-19 (ver abaixo).

Regra do Haiku, adotada (2026-10-19): o tradutor é quem marca `risk_level`, então o Sonnet não pode ser escolhido antes. O `scene-translator` roda em Haiku; fala que sai `high`/`critical` é retraduzida por Sonnet (passo 5d da skill `rodar-onda`); fala com `escalate` NÃO sobe para Sonnet, segue para a fila do humano (corte de bytes sinalizado por `escalate` é aceito, como decidido). A triagem de risco (`risk_triage.py`) e a retrotradução (Opus) seguem como estavam. Alterados: `model:` do `scene-translator.md`, a linha de modelo do `CLAUDE.md` e a skill `rodar-onda`.

## Primeira onda real com a regra do Haiku (2026-10-19)

Onda de 6 cenas (351 falas): `50_37_99 50_43_02 60_11_00 60_21_00 60_22_00 60_23_00`. Grupo de 4 cenas curtas (47 falas) num só `scene-translator`, `60_21_00` e `60_22_00` sozinhas, tudo em Haiku. Fechou com 187 cenas `verified` (14.074 de 23.933 falas), gates limpos, nenhum `escalate`, nenhum `lore_novo`, nenhuma flag de bypass.

**Custo (USD equivalente da API, ledger e transcritos dos subagentes; ruído do ledger ~20%):**

| Etapa | USD | Por fala (351) |
| --- | --- | --- |
| Tradução em Haiku (3 subagentes) | ~0,37 | ~0,0011 |
| Passo 5d: Sonnet nas 2 falas `high` (2 execuções) | ~0,14 | |
| Passo 5c: Opus na retrotradução (2 execuções) | ~0,31 | |
| **Total da onda** | **~0,83** | **~0,0024** |

- A tradução em Haiku saiu a ~US$ 0,0011 por fala, dentro do que o benchmark mediu (0,0012 a 0,0017) e ~75% abaixo do Sonnet (0,0044 a 0,0052). A economia se confirmou no fluxo real.
- Com os passos 5d e 5c o custo total da onda fica em ~US$ 0,0024 por fala, cerca de metade do baseline do Sonnet. O Opus na retrotradução é 38% do total, por 2 falas `high` (custo fixo por cena com fala `high`, com uma rodada repetida depois de um `revise`).
- A saída nos transcritos aparece subestimada (o `cost_report` já avisa: ~25% da saída é estimada), então Sonnet e Opus podem estar um pouco mais caros do que a tabela.

**Ressalva sobre o ledger (atribuição por cena):** o `cost_report` atribui à cena todo agente que a tocou, de qualquer sessão. Nas 6 cenas, US$ 1,20 dos US$ 1,72 que ele mostrou vinham de 6 agentes Sonnet de outra sessão (`stage: other`, ~57 min antes), fora desta onda. Ler o custo por cena do `wave_last.log` sem separar por sessão e por agente superestima a onda (US$ 0,0049 por fala lido, contra ~0,0024 real). Para medir uma onda: somar por `agent` e `session` as linhas `source: "session"` do `api_ledger.jsonl`, não por cena.

**Qualidade (juiz Opus, mesma régua e mesmo prompt nos dois lados, 120 falas por amostra):** controle em Sonnet (6 cenas de onda anterior) 3 erros (2,5%); onda em Haiku 5 erros (4,2%). A diferença de 2 falas está dentro do ruído. O juiz não substitui a amostra cega humana: na calibração contra 480 falas pontuadas pelo usuário (V6, V9, V9b, V9c; 9 erros humanos) ele pegou 0 dos 9 e apontou outros 15, e a concordância de ~95% vem de ambos dizerem `ok` na maioria. Vale só como comparação relativa, nunca como taxa de erro. Os 5 erros do Haiku (palavra omitida por limite de bytes em 2, sentido perdido em 1, marca de gesto em inglês em 1, imperativo no infinitivo em 1) foram corrigidos por Sonnet nas falas apontadas. Uma amostra humana pequena fica como opção do usuário.

**Pontos de processo:** o Haiku sem `risk_level` `high` em 349 das 351 falas confirmou o desenho do passo 5d (só 2 falas subiram). O tradutor do grupo de 4 cenas trocou uma risada característica pela regra de interjeição localizada e a retrotradução marcou `revise`; o usuário decidiu manter a risada original, e a fala voltou a `pass`. O `decision_log.md` não cobre marca de gesto entre asteriscos; ficou "Aceno" por escolha do subagente, sem convenção.

## Teste de viabilidade no Pro: ondas 32 e 33 (2026-10-19)

Pergunta: com a regra do Haiku e as outras melhorias, a tradução inteira cabe no plano Pro? Duas ondas reais, conversa quieta, sem desenvolver framework, `/usage` lido antes e depois. Critério combinado com o usuário, por onda de ~450 falas: sessão passa com até 8 pp e falha acima de 12 pp; semana passa com até 2 pp e falha acima de 3 pp.

| | Onda 32 | Onda 33 |
| --- | --- | --- |
| Falas / cenas | 443 / 6 | 235 / 6 |
| `/usage` sessão | 62 -> 74 (+12 pp) | 74 -> 83 (+9 pp) |
| `/usage` semana | 46 -> 47 (+1 pp) | 47 -> 49 (+2 pp) |
| Sessão por 100 falas | 2,7 pp | 3,8 pp |
| Custo pelo ledger | US$ 2,21 (~0,0050/fala) | US$ 1,21 (~0,0051/fala) |
| Haiku / Sonnet 5d / Opus 5c | 0,46 / 0,38 / 1,37 | 0,15 / 0,25 / 0,80 |
| Opus na onda | 62% (6 agentes) | 66% (1 agente + rejulgamentos) |

**Leitura:** a sessão da onda 32 caiu na zona cinzenta (entre 8 e 12 pp) e a semana passou. A onda 33 mede mais por fala porque o `/usage` inclui a conversa de planejamento no fim e três rodadas de retrotradução de uma só fala. O agente Opus único (decisão do usuário para a 33) não baixou o dólar por fala. O juiz de erro não foi medido. Restam ~9.181 falas: ~270 pp de sessão e ~27 pp de semana, o que cabe no Pro só espalhado em 3 a 4 janelas de sessão com reset entre elas. Ressalva: o `/usage` tem erro de leitura de ~1 pp, e a conversão de dólar para pp (~6 pp de sessão e ~1 pp de semana por dólar) é extrapolada.

**Melhorias levantadas nas duas ondas** (registradas no `ROADMAP.md` do projeto):

- Novas:
  - O `revise` do gate não tem saída no lote: a marca `escalate` não isenta a fala e uma única fala travou a onda 33 por três rodadas de retrotradução.
  - O Opus é o maior custo da onda (62% e 66%).
  - O `back_prompt` mostra o texto original ao lado do pt-BR, então a retrotradução não é cega.
- Com evidência nova em item existente:
  - Retrotradução fora do fluxo: o Opus gravou o `offset` como número e o gate acusou a chave ausente; o passo 5c da skill não declara o formato `"<cena>:<offset>"`.
  - Orçamento de bytes: uma exclamação de 23 bytes em conflito com o tom aceito pelo Opus.
  - `obs_report`: repete a falha antiga de uma cena já `verified`.
