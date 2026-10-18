# ROADMAP — Utawarerumono: Prelude to the Fallen

## Retomada (ler primeiro numa sessão nova)

Atualizar antes de cada `/clear` (toda virada de fase). `/compact` manual nunca: a compactação é a automática.
Primeiro comando da sessão nova: `python ../../framework/runtime/session_usage.py mark . <fase>`.

- **Onde estamos:** Fase 3 (tradução em escala), **57 de 349 cenas `verified` = 5.804 de 23.933 falas (24,3%)** (`artifacts/panorama_ondas.md`, atualizar com `panorama.py`). Última onda: o experimento de teto (`11_20_00 11_30_00 11_31_00 11_32_00 11_36_00`, 662 falas, 2026-10-17); overhead 25,0% (> 24%), 1,0 falha por cena, sem estouro de contexto; o usuário **adotou o teto de ~700 falas (até 6 cenas)**. Em 2026-10-17: as 57 cenas ganharam o **visto de Felipe** (`hitl.py ack`, com base numa amostra de 24 falas + varredura das 5.804: 0 caractere corrompido; única correção, `00_90_02:102`, escrita em pt-PT, já regravada e reverificada); fila de escalonamento vazia, lint 0, quality gate OK; ponto de controle fechado. Framework em **v2.1.0** (CHANGELOG; gate por cena, ADR 0017). **Próxima onda:** rodar `panorama.py` para o plano e esperar o "sim" do usuário. Melhorias abertas: seção "Melhorias" abaixo (histórico em `artifacts/historico_melhorias.md`); plano de 2026-10-17: `artifacts/plano_melhorias.md`.
- **Pendências abertas:** (1) próxima onda só com aval do usuário; (2) falante `Teoro` sem voice card (15 falas) — o `resumo_lote.py` já avisa; (3) B3 (`session_usage.py sync` + `cost_report.py`), B4/API só com aval e teto, B5, B6 e Fase 4; (4) conferência visual no jogo é do usuário (checkpoint de instalação a cada ~25%: o de ~85 cenas ainda não chegou; 57 feitas); (5) tag `v2.1.0` só depois do merge (commit/PR só se o usuário pedir).
- **Auditoria de arquitetura (2026-10-17), plano de conformidade executado (framework v2.1.0, ainda sem commit):** gravação de estado atômica e append sob trava (ADR 0018; medido: 1800 de 1800 linhas válidas com 5 processos, antes 27 corrompidas), SQLite com espera de 30 s, `.env` solto apagado (a chave de API deve ser trocada pelo usuário), `ml-coverage-optional` passou a rodar em PR e push, testes novos de `session_part`/`session_lot`, log do `wave` por onda. Suíte: 831 passed, 2 skipped, cobertura 94,19%; mypy (`--follow-imports=silent`) e ruff verdes. Fica para o usuário: commit/PR e exigir o check de ML na proteção de branch.
- **Medição de overhead:** baseline 65,1% → ondas 3 e 4 em 28% e 24% (sessão limpa) → teto ~700: 25,0%. Medir com `gaps.py --sessao <id>` (overhead de uma sessão) ou `--cenas`. Sessão limpa = `/clear`, `mark . 3`, só `rodar-onda`, sem desenvolver framework. Projeto roda com `claude --no-chrome`; `ponytail` e `linkedin-agent@synced` desligados.
- **Como rodar:** `python framework/runtime/wave.py projects/utawarerumono_prelude <cenas> --backend in-session`; 1 `scene-translator` por cena, passando o caminho `projects/utawarerumono_prelude`; o verify exige `UTAP_DATA_DIR=<projeto>/backup_original/DataBase2.sdat` (variável, não argumento). No fim: rebuild de custo, skill `levantar-melhorias`, depois o `/clear`; primeiro comando da sessão nova: `python ../../framework/runtime/session_usage.py mark . 3`. Armadilhas, escalonamento e regras de interjeição: `artifacts/historico_retomada.md` e `artifacts/decision_log.md`.
- **Onda 6 fechada (2026-10-16):** `10_52_00` (456 falas, cena única acima do teto de 380, teste de onda grande) `verified`; o `wave.py` parou no lint e em 5 pendências, resolvidas pelo usuário (formas decididas no glossário e `hitl resolve`), e o `wave.py` da cena passou limpo (lint 0, quality gate OK). A contagem 367×456 era erro de relato do subagente: o JSON tem as 456.
- **Onda 7 fechada (modo contínuo):** `10_80_00` e `10_81_00` `verified`; no disco: **44 de 349 cenas = 4.423 de 23.933 falas (18,5%)**. Escalonamentos e lore sem forma foram adiados em `artifacts/pendencias_finais.md` (fora do git), mas o `quality_gate` do `wave.py` ficou aberto por escalonamento e travou a onda 8: o adiamento **não funciona** e foi trocado pela parada com tabela (ver "Escala" abaixo). Próxima onda pelo `panorama.py`: `10_82_00 10_87_00 10_91_00 10_33_21`.
- **Onda 8 fechada (2026-10-16):** `10_82_00 10_87_00 10_91_00 10_33_21` `verified`; achado do lint corrigido (fala reescrita dentro do orçamento, nome mantido), 13 escalonamentos resolvidos pelo usuário (`hitl resolve`), retrotradução de `10_53_00` feita (3 pass). No disco: **48 de 349 cenas = 4.763 de 23.933 falas (19,9%)**; quality gate OK. Falante de `10_91_00:60` e `:77` não identificável (bytecode `ScriptEvent` não traz falante); tradução independe dele. Glossário: Honey=Querido(a) só como tratamento carinhoso; literal = mel/hidromel (nota e aliases ajustados, lint 0). Próxima onda pelo `panorama.py`: `10_83_70 10_83_88 11_00_00 11_11_00` = 379 falas.
- **Escala (plano aprovado em 2026-10-16; medido nas ondas 5 a 8):** ritmo medido 45–51 falas/min com ondas de ~300 falas (`events.jsonl`: runtime ≈ 3 s por cena, o tempo está no LLM e na sessão; gargalo real é o limite de sessão da assinatura). Restam ~19.200 falas ≈ 7 h de execução pura mais paradas. Ciclo: onda → retrotradução Opus das falas `high` (passo 5c da skill, ~15 s para 3 falas) → `wave.py` → lote de 8 ondas com resumo (`resumo_lote.py`, `logs/resumo_lote_<n>.md`). Escalonamento do tradutor e lore sem forma **param a onda no gate** com tabela única; usuário responde, lote retoma (`logs/estado.json`). Paradas do lint (ondas 6 e 8) vinham de nome cortado pelo `byte_budget`: `scene-translator.md` agora proíbe cortar termo `manter_original` e roda o lint por cena antes de encerrar (falta ver numa onda real). Checkpoints de instalação no jogo a cada ~25% (cenas ~85, ~170, ~260). Rodar num PowerShell novo, sem `FORCE_PROMPT_CACHING_5M`: `.\.claude\skills\rodar-onda\rodar_ondas.ps1 -Lote 1 -OndaInicial 9` (comparar o resumo com o ledger e então `-Lote 8`). Ainda **não testado de ponta a ponta**: espera do limite de sessão, `estado.json`, resumo × ledger (ondas 5 e 6: $0,41/28% e $1,28/12%). Fica para depois: ondas maiores, 2 sessões em paralelo (medir o limite antes) e API (~$61, só com aval).
- **Bloqueios que só o usuário desfaz:** nenhum.
- **Regras que só valem neste projeto:**
  - Projeto novo e independente: nada do `projects/utawarerumono` (Mask of Deception, descontinuado) é reutilizado —
    conector, extrator, TM, glossário, KB, DB, scripts. Série própria em `project.json` (`series`), DB próprio.
  - O `discover.py` classifica a engine como "Aquaplus ScriptEvent SDAT" e manda copiar o conector antigo: **não
    copiar**. Mapear o formato de novo (Fase 0) e escrever o extrator do zero.
  - Release/Steam/ação externa só com aval explícito.
- **Ferramentas locais:** `tools_local/` (fora do git)

## Melhorias para o framework — levantar só no fim do projeto

Não editar o framework no meio do projeto; anotar aqui só o que está **aberto**, uma linha por item. O texto integral de tudo o que já foi levantado, medido ou resolvido (ondas 2 a 9, benchmarks, experimento de teto) está em [`artifacts/historico_melhorias.md`](artifacts/historico_melhorias.md); o plano de 2026-10-17, em `artifacts/plano_melhorias.md`. A skill `levantar-melhorias` acrescenta só o que é novo (e lê o histórico se precisar da evidência).

**Abertas (decisão ou trabalho pendente):**

- **Falante por fala ausente / personagem sem voice card:** o subagente atribui por contexto (palpite) e cai em `npc`/`unknown`. O `resumo_lote.py` já lista falante com nome, sem card e com ≥5 falas na onda (hoje: Teoro, 15); falta criar o card.
- **Orçamento de bytes e onomatopeia curta:** o conector não impõe `byte_budget` por fala (limite real = largura da caixa, a medir no jogo; `connector/table_schema.md`). Falas curtas empobrecem por abreviação. Proposta: `project.json` declarar se e como o orçamento é imposto, e o `precheck` ler isso.
- **`gate.connector` registra `block` em toda rodada:** `connector.data_dir_env` não está declarado no `project.json`; polui o `obs_report`. Conserto de projeto; do framework: avisar quando o gate só reclama disso.
- **Fase 0 sem a ordem de jogo e progresso sem total:** o `discover` deveria gerar `ordem_cenas.txt`; `cost_report` e Retomada deveriam trazer "falas feitas de total" (o `panorama-ondas` já faz, local).
- **Rótulos do ledger divididos** (`translate`, `3.` ao lado de `3`): fundir antes do B3.
- **Ledger sem a onda/execução de cada sessão de overhead:** recorte por horário não isola o overhead de uma onda (ex.: onda 9, 38% × 78%). Gravar a origem da sessão.
- **`gaps.py`:** não mede por onda/sessão (`--sessao`, `--cenas`) e falta incorporar as análises manuais (cache por requisição, custo fixo × marginal, falhas por grupo, compactações por sessão).
- **Chave do JSON da cena sem o offset completo** (menor): mostrar a chave exata no exemplo do `scene-translator.md` e do `scene_prompt.md`.
- **`scene/api_translate_failed` com backend in-session** (menor): não registrar no `events.jsonl`/`obs_report`.
- **Virada de fase manual** (`/clear` + `session_usage.py mark`): automatizar o `mark` por hook `SessionStart` com matcher `clear`; mudar a regra do `CLAUDE.md` só com aval do usuário.
- **Oficializar no framework** as skills `levantar-melhorias` e `panorama-ondas` (decisão do usuário, no fechamento).
- **Declarar no B6:** custo por fase só é dividido tradução/governança a partir da onda 3; `trad:gov` 100:0 quando não há risco alto nem retrotradução.

**Resolvido em 2026-10-17** (código em `docs/CHANGELOG.md`, "Não lançado"; ADR 0017):

- Gate por cena e bloqueio global só na entrada da onda (`wave.entry_problems`); `glossary_lint --scenes` bloqueia só achado da onda e avisa dos demais.
- Evento de falha com `code` e `reason` (`events.jsonl`), então o retrabalho passa a ser medível por causa.
- `model.read_translation`: JSON do subagente fora de UTF-8 vira `invalid_translation_file` com mensagem clara, não falha de API.
- `hitl resolve` conta separado aceite do tradutor e alias de glossário.
- `.gitignore` cobre `scenes/*/_*.py`; `scene-translator.md` avisa que a tabela traz menos falas que o plano (as ausentes vêm da TM); `rodar-onda` agrupa até 3 cenas curtas por subagente; `linkedin-agent@synced` desligado em `enabledPlugins`; `resumo_lote.py` não quebra com linha de ledger sem custo.
- **Fechadas sem ação:** `(adaptar)` no `glossary_lint` (obsoleta), offsets citados sem linha no source (sem lacuna), custo do `precheck` (irrelevante em onda de 4 a 6 cenas), teto de onda (~700 adotado pelo usuário).

## Benchmarks (obrigatórios neste projeto — `docs/ROADMAP.md` item 3; PRD/HLD/FDD em `docs/benchmark_sessao/`)

Nada do bloco "sessão" do bof4 entra no framework sem benchmark que meça o ganho antes. Este projeto é o
projeto novo que o benchmark esperava.

- [x] **B1. Fixar o recorte:** cenas `00_*` (prólogo; piloto `00_00_02`), `--seed 42` (fixado em 2026-10-14).
- [x] **B2. Estado inicial idêntico por braço:** mesma TM, glossário e decisões de voz copiados para cada braço
  (instância/DB isolados por braço: o portão de caminho veda dois caminhos no mesmo projeto, e a TM de um braço
  não pode contaminar o outro). Foto do estado pós-piloto (só `00_00_02` na TM, 31 falas) em
  `output/bench_b2_inicial/` (fora do git) com `MANIFEST.sha256` (16 arquivos: TM, glossário, KB, voz, decisões,
  profile, DB). O braço sessão é este projeto; o braço API nasce como cópia da foto (DB e TM próprios), conferida
  pelo manifest antes de rodar (2026-10-14).
- [ ] **B3. Braço sessão:** `wave.py` (um comando por onda) vs ~13; ondas menores com `/clear` entre elas; Sonnet
  traduz e Opus retrotraduz; Haiku só para rótulo curto; lote de correção automático. Medir com
  `session_usage.py mark/sync`, `cost_report.py`, `obs_report.py`.
- [ ] **B4. Braço API:** `run_chapter.py --backend api` no mesmo recorte. **Só com aval explícito e teto de gasto
  definido antes** (`budget.py`).
- [ ] **B5. Qualidade cega:** `quality_sample.py export/score` por braço, mesma `--seed` e mesmo N; IC 95%.
- [ ] **B6. Relatório e decisão por variável** (entra / não entra); erro do medidor declarado; relatório sem fala
  do jogo. Item 3 do `docs/ROADMAP.md` marcado `[x]` com link.
- Escolha de caminho do projeto: uma só, com HITL (`hitl.choose-path`), antes da Fase 3.

## Fase 0 — Conector

- [ ] Reconhecimento: binwalk nos binários (`.exe`, `.sdat`, `.fnt`, `.tex`), tamanhos e cabeçalhos.
- [ ] Mapear o formato do contêiner e dos scripts de texto; Kaitai/ImHex antes do `extract.py`.
- [ ] `connector/table_schema.md`, `extract.py`, `scope_scan.py`, `split_scenes.py`, `reinsert.py` do zero.
- [ ] Round-trip byte-idêntico (se falhar: diff binário em script) + `test_roundtrip_synthetic.py` (Hypothesis).
- [ ] `build_plan_chapter.py` e `verify_chapter.py` adaptados (o `connector_gate` bloqueia o `_skeleton`).

## Fase 1 — KB

## Fase 2 — Piloto ✅

A conferência visual no jogo é aqui: o humano vê o trajeto do piloto instalado antes de escalar.

## Fase 3 — Tradução em escala

## Fase 4 — Fechamento

Sem passada pelo jogo inteiro: depois do piloto, a conferência visual é por print a cada instalação.
- **Cobertura do subagente e interjeições** (onda `10_15_00 10_25_00`, 2026-10-15): o `scene_prompt` não trazia todos os offsets (subagente partiu de 271 de 330 falas e completou pela memória de tradução); falante das interjeições curtas foi atribuído por heurística; `byte_budget` estourou em ~55 falas. Proposta: prompt com a cobertura completa e orçamento por fala, e o gate de cobertura avisar antes do escalonamento.
