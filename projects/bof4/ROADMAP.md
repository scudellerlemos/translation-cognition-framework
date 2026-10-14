# Roadmap — Breath of Fire IV (PT-BR, modo banco)

> Última atualização: 2026-10-14
> Status atual: **305/305 cenas `verified` (27.021 falas), Fases 0 a 4 fechadas; distribuição: patcher `.exe` beta testado em cópia, falta o teste no jogo real e a release** (ver "Retomada").
> Histórico da Fase 0 (mapeamento do conector): estava em `projects/breath_of_fire_4/ROADMAP.md`, removido do repositório (segue no histórico do git).

Os passos são seguidos na ordem. Nenhum gate é pulado; item aberto bloqueia o seguinte.

## Retomada (ler primeiro numa sessão nova)

Atualizar antes de cada `/clear`. Estado em 2026-10-14 (fim do dia):

- **Próximo passo (2026-10-14):** teste do `.exe` no jogo real (`projects/bof4/output/Patch_BoF4_PTBR_Gajshield.exe`,
  SHA-256 `5bfebb461e8b0cef8b20ef6c30d7bf2f056847d467e710b3f6503afcc2c7fa66`, v0.1.0-beta; só o Felipe opera a
  janela), depois máquina sem Python e trajeto do piloto; em paralelo, print da tela para conferir a largura de
  44 colunas e as 2 descrições reescritas (`artifacts/qa_revisao/teste_ingame/prints/`). Só então release (aval
  do Felipe), guia da Steam (`Desktop/teste_bof4/guia_steam.txt`) e `v1.0.0` com reamostragem de qualidade.
- **Fechado em 2026-10-14 (tarde/noite):** 305/305 cenas `verified` (`AREAS032`, `AREAS054` e `AREAM024`/`AREAS048`
  fechadas); fala 7 de `AREAD115` corrigida ("Vossa Majestade", decisão de 2026-10-12); 10 falas com "tu" mantidas
  como registro arcaico de Fou-Lu e dos Eternos (revisão do Felipe); 2 descrições acima da caixa corrigidas
  (`AB000_00`, `CAMP`, `COMMU03`, `MASTER`, `MSHOP`, `SGAMEN`, `SHOP`); reinserção refeita (8 arquivos mudaram),
  instalada no jogo e pacote do patcher regenerado (305 deltas). Patcher: corrigido estouro quando o `tasklist`
  devolve saída fora do UTF-8; teste instalar/idempotente/desinstalar/arquivo modificado/jogo aberto passou numa cópia.
  Framework: `scene_dedup` lia a coluna errada (`text_en`) e corrompia JSON com aspas escapadas — corrigido, com teste.
  Não provado: limite de 44 colunas (inferido do inglês), 27 falas `pt-PT?` sem revisão humana além das 10 acima.
- **Fechado em 2026-10-14:**
  1. **115 cenas divergentes: resolvido.** Reconferidas (116 de 116, round-trip íntegro, 0 overflow); 23 falas de
     risco alto cujo texto mudou foram rejulgadas (23 `pass`, revisor Opus em agente separado); gates verdes;
     305 arquivos reinseridos e 116 instalados no jogo (`.bak` mantido; o jogo está igual ao disco).
     Lição: `BOF4_DAT_DIR` tem de apontar para `source_dat` (originais), não para a pasta do jogo, que agora
     tem o texto traduzido. Sem a variável o round-trip falha em todas as cenas.
  2. **4.4c feita** (o Felipe voltou atrás da dispensa e quis medir): amostra de 227 falas, taxa de erro
     **14,5%** (29/200 sorteadas; IC 95%: 10,3% a 20,1%), **26,1%** pesada por repetição; o juiz apontou 0,7%
     do que leu, precisão 51,9%, alcance 0,0% (não pegou nenhum erro da amostra sorteada). Revisor: Felipe
     Scudeller. Os erros reais se repetem em poucos textos: "fl" = "and." nos rótulos de andar, "Wgt" = "Pes.",
     "em alvo(s)" no lugar de "no(s) alvo(s)", "Golpe Sorte", "Região Wyndia". **Correção desses padrões: feita em parte**
     (decisão do Felipe; mexe em texto instalado e exige reconferência e gates; ver as duas correções abaixo).
     **Correção feita em 2026-10-14, depois da amostra:** "Região Wyndia" = "Região de Wyndia" (5 cenas) e
     "Golpe Sorte" = "Golpe de Sorte" (`BTLEND` e glossário); na lista de habilidades (`AB000_00:10100:30`)
     fica "Golpe Sorte", porque a forma com "de" custa +2 bytes. 6 arquivos reinstalados, gates verdes.
     **Segunda rodada (2026-10-14):** "Wgt" = "Peso" por extenso (mesmo tamanho de "Pes."); rótulos de andar do
     elevador só com o número (`5`, `B1`) e nas faixas "Castelo, andar 5"; a frase de alvo passou de "em um
     alvo(s)" para "em um alvo" / "em todo alvo" (`[07][00]` = tabela "one/all" de cada cena; "1 alvo" daria +2
     bytes, acima da regra de +1). 30 arquivos reinstalados.
     **A taxa de 14,5% vale para o texto de antes dessas correções.** Linha `AB000_00:2:256` ainda tem "[07][04][01]alvo(s)" (variável diferente, não conferida).
  3. **Distribuir a tradução na Steam.** Formato e canal decididos (patcher `.exe` com deltas, release no GitHub);
     pacote e `.exe` beta prontos e testados em cópia; falta teste no jogo real e a release.
  4. **Commit.** Os da `feat/bof4-instance` (framework e bof4) foram feitos em 2026-10-13, sem push e sem PR.
     Ficaram de fora: `tm/`, `hitl_log.jsonl` e `phase_marks.jsonl` (ignorados) e `qa_effectiveness.jsonl`
     (aguarda o Felipe decidir o texto do campo de revisor).
  - O levantamento de fim de projeto está no fim deste arquivo, com os quatro blocos aceitos.

- **Onde estamos:** Fase 4, 4.4a e 4.4b fechados; 4.4c fechado (taxa de erro 14,5%). Projeto em escopo `completo`
  (diálogo + sistema), caminho `in-session`; 305 cenas, 27.021 linhas, todas traduzidas e instaladas no jogo
  (`.bak` de todos os arquivos).
  - Feito desde a última retomada: texto de sistema traduzido e instalado; rótulos em imagem das folhas
    principal, de sistema e de batalha, incluindo os botões de batalha (ver "Rótulos em imagem", etapas 1 e 2);
    acabamento de abreviações (só trocas de até +1 byte, registradas em `byte_budget_exceptions`).
  - 4.4a: triagem aplicada (5.518 pares únicos, 14 lotes, 40 textos apontados -> 218 falas em 68 cenas subiram
    para risco alto); retrotradução de 343 falas: 303 aprovadas, 40 reprovadas (16 textos distintos), todas
    corrigidas e reconferidas (40 de 40 aprovadas). `quality_gate`, `connector_gate` e `pilot_gate` verdes;
    34 arquivos instalados em 2026-10-13. **4.4a fechado.**
  - Na mesma instalação: botão "Charge" = "Auto" e "Escape" = "Fuga" (folha de batalha e 8 falas de
    ajuda), tela de carregar ("Abrir", "Carregado.", "Erro de leitura!"), fadas no feminino (`AREAS041/042`).
- **Material de 4.4b/4.4c gerado em 2026-10-13** (fora do git, em `artifacts/qa_revisao/para_revisar/`):
  `review_all.xlsx` (27.021 linhas, 3.350 marcadas) e `amostra_qualidade.csv` (227 falas, nenhuma julgada).
- **4.4b feito (2026-10-13):** revisão da planilha de QA por Felipe Scudeller. 1.478 textos distintos marcados
  revisados; 56 textos (364 falas, 110 cenas) corrigidos pela coluna `Correcao`. As 13 falas de risco alto
  tocadas voltaram pela retrotradução (13 de 13 aprovadas). Gates verdes; 110 arquivos instalados. Planilha
  marcada guardada em `artifacts/qa_revisao/aplicado/` (fora do git). Fila de escalonamento: 0.
  - Na mesma rodada, a pedido do usuário: fala do Manillo unificada em "oui?" (`CAMP`, `MASTER`) e "stamps" =
    "selos" em todo lugar (`MSHOP`). Print da batalha dispensado pelo usuário.
- **Depois disso:** 4.4c feita em 2026-10-14. A coluna `veredito` não é preenchida pelo agente.
  No fechamento: levantamento para o framework; projeto novo só depois.
- **Retirado do fluxo pelo usuário:** gate visual 4.3 (jogar o trajeto inteiro), no bof4 e no framework.
- **Ficam em inglês por decisão do usuário:** nomes de item, arma, armadura, acessório, habilidade e item-chave;
  nomes de inimigo; botões do menu da tela de título; Zenny, Max, Min; "Manillo Shop", "Stamp Card"; nomes de
  forma de dragão; Hits e Will.
- **HITL:** o usuário decide na conversa e o agente registra o comando com `--quote "<frase literal dele>"`;
  nunca a partir de aviso do sistema ou de relato de subagente. Planilha de revisão, fila de escalonamento e
  coluna `veredito` da amostra de qualidade continuam sendo preenchidas só pelo usuário.
  `python ../../framework/runtime/hitl.py status .` mostra o que falta.
- **Instalar no jogo não pede mais OK caso a caso** (regra do usuário, 2026-10-12). Condições: gates fechados,
  jogo fechado (`tasklist | grep -ic bof4` = 0), `.bak` mantido, relatar depois o que entrou.
  Comando, a partir de `projects/bof4`, com `G` = pasta `english/DAT` do jogo na Steam:
  `python -I -X utf8 tools_local/install.py output source_dat "$G"` (ensaio) e o mesmo com `--go` (instala).
- **Reconferência** (só caminho de sessão): cena completa e sem mudança de falas/doutrina reaproveita o
  `pack.json` salvo; cerca de 3 a 8 s por cena mais 1 min fixo por comando.
- **Ferramentas locais** em `projects/bof4/tools_local/` (fora do git): `install.py`; `lot.py`, `dup.py` e
  `plan.py` são as do lote da Fase 3 (prompt por lote, reuso de fala repetida, plano de ondas).
- **Tela do jogo:** o agente não captura a tela; depende de print do usuário em
  `artifacts/qa_revisao/teste_ingame/prints/`.
- **Custo:** economia só no caminho de sessão; caminho de API e `context_pack.py` não mudam. Primeiro comando
  da sessão nova: `python ../../framework/runtime/session_usage.py mark . <fase>`.

## Fase 0 — Conector

- [x] **0.1.** Conector Capcom DAT copiado do projeto de referência (`connector/`).
- [x] **0.2.** Corpus extraído: 223 cenas, 19.234 linhas (99 conteúdos distintos, 5.257 linhas únicas). Re-extraído em 2026-10-11: a string vai do ponteiro até o próximo ponteiro (antes cortava no primeiro `00` e perdia o resto de ~25% das falas) e as famílias `AREAM`/`AREAE` entraram (cidade de Sarai e abertura estavam fora).
- [x] **0.3.** `connector_gate` verde, refeito depois da re-extração (round-trip registrado pelo piloto).
- [x] **0.4.** Terceira re-extração (2026-10-11, teste in-game run1 achou falas em inglês): 286 cenas, 19.873 linhas. O detector de seção de texto descartava cenas curtas (tabela fixa de 256 ponteiros maior que o texto; critério de destinos únicos) — 62 cenas entraram e `AREAS056` passou a ler a seção certa. O `INIT.DAT` entrou com as duas seções de texto de sistema (5 e 6). Nenhuma linha já extraída mudou; round-trip de identidade nos 286 arquivos; `connector_gate` verde.

## Fase 1 — KB (Passos 01–05)

- [x] **1.1.** Entidades, glossário, voice cards e base de conhecimento migrados e ampliados.
- [x] **1.2.** `research_log.md` reconciliado; ratificações do usuário em `kb_ratified.csv`.
- [x] **1.3.** `decision_log.md` com as 16 decisões ratificadas (eram 15 quando o item fechou), indexadas no banco.
- [x] **1.4.** `kb_gate` verde, com busca semântica ativa.
- [x] **1.5.** Candidatos da re-extração reconciliados (`Buy`, `Sell`, `Stop`, `Normal`, `Sink`, golpes `Pilfer…`/`Spray…`): glossário + `research_log`, `kb_phase.py all --check` verde ( do backlog).
- [x] **1.6.** Worklist da re-extração com `AREAM`/`AREAE` reconciliada: +152 termos no glossário, +9 entidades, seção nova no `research_log`; `kb_phase.py all --check` e `kb_gate` verdes. Propostas de lore aguardando ratificação do usuário: Purifiers→Purificadores, Elders→Anciões, Nameless→Sem Nome, Gateway→Portal, Dragon of Doom→Dragão da Perdição.

- [x] **1.7.** Worklist da re-extração 0.4 reconciliada: +159 termos no glossário, +6 entidades, seção nova no `research_log`; `kb_phase.py all --check` verde. Traduções são proposta, aguardando ratificação do usuário.

## Fase 2 — Piloto (trajeto do início do jogo até a taverna de Sarai)

- [x] **2.1.** Tradução das 104 linhas (backend `in-session`).
- [x] **2.2.** Round-trip via `run_scene.py` com verify, sem bypass: 104/104, 0 overflow.
- [x] **2.3.** Back-translation das 4 linhas de risco alto: 4/4 `pass` (vereditos da IA).
- [x] **2.4.** Revisão humana dos vereditos de back-translation (4/4 confirmados, 2026-10-11).
- [x] **2.5.** Cena re-rodada com a doutrina atual (`--check-stale` limpo).
- [x] **2.6.** Sonda de glifos in-game: a fonte original não tem glifo acentuado, mas o atlas do `INIT.DAT` aceita glifos novos e código ≥ `0x88` desenha sem avançar o cursor (acento sobreposto). `connector/font.py` + `table_schema.md`.
- [x] **2.6a.** Piloto refeito com `target_charset_supported: true` (orçamento conta 2 bytes por acento): `run_scene` sem bypass, 104/104, 0 overflow, `--check-stale` limpo. "You got:" virou "Obteve:" (3 linhas) para caber.
- [x] **2.6b.** Piloto ampliado para o trajeto inteiro (pedido do usuário, 2026-10-11): abertura `AREAE023`(=`E030`), queda do sandflier `AREAE015`(=`E016`,`E017`), cratera `AREAD013`, Fou-Lu `AREAD026` e `AREAD057`, penhascos `AREAD020`(=`D030`,`D070`), Sarai `AREAM000`, taverna `AREAS001`(=`S004`, refeita sobre o source novo). 14 cenas, 372 linhas distintas; `run_scene` sem bypass em todas: round-trip OK, 0 overflow.
- [x] **2.6c.** Back-translation das 21 linhas de risco alto do trajeto: 21/21 `pass` (vereditos da IA).
- [x] **2.6d.** Revisão humana dos vereditos de back-translation das cenas novas (17 linhas + 7 de 2.6g; as 4 da taverna já foram confirmadas em 2.4). OK do usuário via chat (2026-10-12), cobrindo também as linhas de risco alto das 12 cenas de 2.6j.
- [x] **2.6e.** Agudo do `í` redesenhado (teste in-game run1: saía como pingo + risco solto à direita). `_ACUTE_I` em `connector/font.py` agora tem 3 px e pousa em cima do pingo; `output/INIT.DAT` regenerado. Substituído pelo glifo dedicado de 2.6h, que o usuário aprovou in-game (2026-10-12).
- [x] **2.6f.** Títulos de capítulo (cartão "I: …" da abertura) entram no escopo (decisão do usuário, 2026-10-11). É imagem, não texto. Feito: codec das seções de imagem comprimida decodificado (`connector/imgcodec.py`, `table_schema.md` §9 — LZ77 + Huffman dinâmico no molde do LHA `-lh1-`); cartão localizado (uma imagem com os quatro títulos, em `AREAE023`/`AREAE029`/`AREAM013`/`AREAM052`); `connector/cards.py` redesenha em português (I: Despertar · II: Os Eternos · III: Correntes · IV: Aquilo Que Passa) e o `reinsert` regrava os quatro; round-trip sintético com Hypothesis. Limite: imagens acima de 32768 símbolos (reconstrução da árvore) ainda não abrem — não afeta o cartão. Cartão da abertura instalado no jogo (`AREAE023`); falta o usuário conferir. Títulos II–IV ratificados pelo usuário (2026-10-11, `kb_ratified.csv`) e os outros três arquivos instalados; o título I ("Despertar") e o cartão foram ratificados pelo usuário via chat (2026-10-12).
- [x] **2.6g.** Cenas do trajeto que saíam em inglês no teste run1: `AREAD014` (despertar do Fou-Lu), `AREAD024` (emboscada no bosque) e `AREAE020`(=`E044`, estrada). 43 linhas distintas, `run_scene` sem bypass: round-trip OK, 0 overflow; back-translation das 7 linhas de risco alto: 7/7 `pass` (vereditos da IA, entram na revisão de 2.6d). Instaladas no jogo.
- [x] **2.6h.** Rótulo do informante: "Try:" → "Tent.:" ("Tentativa:" não cabe no orçamento da linha; decisão do usuário, 2026-10-11: rótulo curto que não cabe é abreviado, o orçamento não muda). Instalado.
- [x] **2.6i.** Textos de sistema do `INIT.DAT` (avisos de item, loja, salvar, rótulos de tecla, menu e mapa — 173 linhas) traduzidos com rótulo curto abreviado; `run_scene` sem bypass: 173/173, 0 overflow. Instalado. A conferir in-game: abreviações e se os rótulos de mapa/menu desenham os acentos (podem usar outra fonte).
- [x] **2.6h.** `í` natural. Run2: o agudo sobreposto nao parece letra (o pingo nao some). Run3: glifo proprio na vaga de `]` saiu cortado. Sonda 3 (`run3/ascento2.png`) mediu janela e avanco das vagas sem uso (tabela em `table_schema.md`, secao 4); o `í` agora e glifo proprio na vaga de `>` (`0x3E`), dentro da janela medida, ~11 px de avanco contra 8 do `i`. Instalado e conferido in-game pelo usuario (2026-10-12). Na mesma rodada: cena `AREAD059` (ponte) passada pelo piloto, e tratamento ao imperador acertado em `AREAD014`/`AREAD024` (decision_log, 2026-10-12).
- [x] **2.6j.** Gate de cobertura do piloto (`connector/pilot_gate.py`, pedido do usuário, 2026-10-12): toda cena extraída tem decisão `sim`/`nao` em `artifacts/pilot_scope.csv` (classificação por conteúdo dos 130 grupos de texto fora do piloto, já que os IDs não seguem a história) e toda cena `sim` está `verified` sem gate pulado. Trajeto = do New Game até a saída de Sarai e o primeiro trecho do Fou-Lu (até onde run1/run2 chegaram). Apontou 12 cenas (6 textos): túmulo com Won-qu `AREAD038`(=`D039`,`D040`,`D041`,`D043`,`D078`,`D117`), bosque `AREAD027`, saída de Sarai `AREAD110`, menu do mapa `AREAE005`, menu e conversas de acampamento `AREAS030`/`AREAM026`. Pré-requisito de 2.7: `python connector/pilot_gate.py` verde.
- [x] **2.7.** Gate visual in-game do trajeto inteiro, incluindo a forma e a posição dos acentos: OK geral do usuário via chat (2026-10-12). O OK foi dado antes de o usuário ver no jogo as 13 cenas instaladas em 2.6j e o rótulo "Porta Oeste"; o que aparecer nelas entra como correção na Fase 3.

## Fase 3 — Tradução em escala

> Só começa com a Fase 2 inteira fechada.

- [x] **3.1.** Tradução das cenas restantes pelo caminho da sessão (`run_scene.py --backend in-session --require-back`, em lote, sem bypass de gate): 286/286 cenas `verified`, 19.873 linhas (2026-10-12). Configuração usada e o que foi medido: ver "Registro da sessão" no fim deste arquivo.
- [x] **3.2.** Back-translation das linhas de risco alto por cena (revisor Opus em agente separado): 328 linhas julgadas; 17 reprovadas, corrigidas e rejulgadas até `pass`. `quality_gate.py` limpo no jogo inteiro (nenhum `revise`, nenhuma linha de risco alto sem cobertura). Vereditos são da IA; a revisão humana fica em 4.4.

## Fase 4 — Fechamento

- [x] **4.1.** Passe global de consistência (`glossary_lint`): 0 candidatos em 2026-10-12 (ver registro abaixo).
- [x] **4.2.** `reinsert` do jogo inteiro: 286 arquivos em `output/`, `connector_gate` e `pilot_gate` limpos (2026-10-12).
- [x] **4.3.** Gate visual in-game. **Retirado do fluxo por decisão do usuário (2026-10-12):** não há mais a passada única pelo trajeto inteiro; a conferência visual ficou nos prints das runs 1 a 5 e nos oks pontuais de cada instalação.
- [x] **4.4a.** Triagem de risco (`risk_triage.py export` → juiz barato em sessão → `apply`) e retrotradução das falas que subirem (`run_scene --require-back`). Corpus medido em 2026-10-12: 4.532 pares únicos cobrindo 15.048 falas, em 12 lotes.
- [x] **4.4b.** QA humana via `quality_review.py` sobre a fila priorizada; fila de escalonamento zerada (`hitl.py resolve`).
- [x] **4.4c.** Medida de qualidade (2026-10-14: 14,5%, ver Retomada): `quality_sample.py export` depois da triagem completa, veredito humano na planilha, `score` (taxa de erro, taxa da triagem, acerto do juiz).

Humano no laço ligado em 2026-10-12 (`"hitl": true`): o `run_scene` só roda com escopo aceito (`hitl.py accept-scope`) e os 30 termos mais frequentes do glossário ratificados (`hitl.py ratify`). Descrição em `docs/TRANSLATION_PIPELINE.md`.

## Registro da sessão de 2026-10-11 e 2026-10-12

Resumo do que foi feito, para quem retomar o projeto. Sem falas do jogo; detalhes de formato binário ficam em
`connector/table_schema.md`, decisões de tradução em `artifacts/decision_log.md`.

### Repositório e proteção de conteúdo

- Repositório público recriado com histórico limpo; o antigo ficou privado.
- `content_guard.py` (hook local + job `Guard` da CI): bloqueia binário de jogo, roteiro extraído,
  tradução de cena, planilha de revisão, print, worklist gerada, saída de descompilador, chave de API e e-mail
  pessoal. `projects/*/artifacts/` é default-deny (só entra o que está em `ARTIFACTS_ALLOWED`). Vale para
  todos os projetos. Regras resumidas no `CLAUDE.md` da raiz.

### Conector (teste no jogo, run1 a run3)

- Acentos: a fonte original não tem glifo acentuado. Primeiro acento sobreposto, depois glifos próprios nas
  vagas sem uso do atlas; o `í` foi medido por sonda no jogo (janela e avanço de cada vaga) antes de fechar.
- Cartão de título da abertura: é imagem. Codec das seções de imagem comprimida decodificado
  (`connector/imgcodec.py`, `connector/cards.py`); títulos I a IV ratificados.
- `INIT.DAT` entrou no extrator (textos de sistema: avisos de item, loja, salvar, menu, mapa).
- Corpus re-extraído: 286 cenas, 19.873 linhas (antes 124 cenas). Linhas velhas no banco eram mantidas
  depois de re-extração; corrigido em `framework/db/store.py`.
- `connector/pilot_gate.py` + `artifacts/pilot_scope.csv`: toda cena extraída tem decisão `sim`/`nao` de
  escopo do piloto; cena do trajeto sem tradução bloqueia.
- Fora de escopo por decisão do usuário: rótulos em imagem da interface ("Min/Max", "Zenny").

### Decisões de tradução ratificadas

- Fou-Lu e os Eternos falam em registro arcaico (tu/vós); os demais em português atual; quem fala com
  Fou-Lu usa "Vossa Majestade" + 3ª pessoa.
- Rótulo curto que não cabe no orçamento é abreviado; o orçamento não muda.
- Acento em rótulo de menu: ver `decision_log.md`.

### Custo, uso e observabilidade

- Medição de tokens por origem (API ou sessão) e por tipo (entrada, saída, leitura e escrita de cache), em
  tokens e em dólares: `framework/runtime/session_usage.py`, `cost.py`, `cost_report.py`,
  `artifacts/api_ledger.jsonl`. Limite conhecido: o medidor da sessão subconta tokens de saída.
- Eventos do pipeline e relatório: `framework/runtime/events.py`, `obs_report.py`, `docs/OBSERVABILITY.md`.
  `events.jsonl` não é versionado.

### Pipeline: lote e desempenho

- `run_scene.py` aceita várias cenas por chamada (lote) e o `run_state.json` tem trava de arquivo, então
  agentes em paralelo não corrompem o estado.
- Otimizações medidas: vetor de consulta em binário na busca semântica, memo da checagem de texto residual
  e memo da leitura de transcrições.

### Caminho da sessão (`--backend in-session`): o que economiza

Todas as mudanças abaixo valem só para o caminho da sessão. O caminho da API e o `context_pack.py` não
foram alterados. Medida: tokens de contexto (leitura + escrita de cache) por fala traduzida; ruído entre
dois lotes iguais de cerca de 20%.

Adotado:

| O que | Efeito medido |
|---|---|
| Reuso da memória de tradução dentro do ramo `in-session` de `model.py` (fala já traduzida em outra cena não vai ao agente) e cópia direta de cena de texto idêntico | 746 falas fechadas com 8 traduzidas; dezenas de cenas-cópia fechadas sem agente |
| Agente enxuto `scene-translator` (`.claude/agents/`) | contexto inicial de 11 mil tokens em vez de 44 mil |
| Um prompt por lote (seções comuns uma vez só) e lotes grandes, de 250 a 350 falas | 0,8 a 1,4 mil tokens por fala, contra cerca de 2,3 mil em lotes de 120 a 150 |
| Conferência de tokens `[xx]`, orçamento de bytes e cobertura antes de rodar os gates | a falha mais comum (contagem do token de quebra de linha) é pega antes do pipeline |
| Disparo por workflow, um aviso por leva | a janela principal custava tanto quanto todos os subagentes juntos |
| Lotes agrupados por área, para a fala repetida cair no mesmo lote | até 14% menos falas pagas (medida estática) |

Testado e descartado (ganho dentro do ruído ou pior): carta de doutrina resumida, limite de exemplos da
memória, prompt sem lore, esforço baixo, conferidor entregue pronto, comando único de conferência + gate,
dedup de fala repetida sozinho, pré-tradução de rótulos do glossário (3% das falas) e tabela de saída de 4
campos (5 vezes mais cara: o plano exige `risk_notes` para risco médio ou maior). Haiku em lote de rótulos
foi o mais barato, mas a única fala de alto risco do lote foi reprovada; fica para revisão. Saída em tabela
de 7 campos convertida para JSON por script não piora e simplifica a conferência, mas não mostrou economia
consistente.

O prompt de lote e a conferência foram feitos por script temporário de sessão, fora do repositório. Levar
isso para o framework entra no levantamento de fim de projeto.

Modelos na sessão: Sonnet traduz, Opus faz a retrotradução em agente separado.

### Retrotradução: veredito `revise`

`run_scene --require-back` cobra a existência da retrotradução, não o veredito: cena com fala reprovada
chega a `verified`. Quem bloqueia por veredito é `framework/runtime/quality_gate.py`. Fluxo usado nesta
sessão: corrigir a fala, marcar o veredito antigo como vencido (`invalidate_back_translation`), rejulgar com
revisor independente e rodar `quality_gate.py` até ficar limpo. Fala editada à mão no caminho da sessão não
invalida o veredito sozinha; é preciso marcar.

### Fechamento da Fase 3 (2026-10-12)

- 286/286 cenas `verified`; `quality_gate.py`, `connector_gate.py` e `connector/pilot_gate.py` limpos;
  `connector/reinsert.py` grava os 286 arquivos em `output/`.
- A reinserção do jogo inteiro pegou um caractere que nenhum gate de cena pega: o sinal ordinal (`º`) não
  existe na fonte do jogo. Sete rótulos foram reescritos sem ele. Checagem de caractere fora da fonte só
  roda na reinserção; antecipar para o gate de cena entra no levantamento de fim de projeto.
- Nada da Fase 3 foi instalado no jogo ainda: o gate visual (4.3) depende disso.

### Pontos em aberto para revisão humana

- Cenas traduzidas sob variante de teste que pode afetar qualidade: `AREAM010` a `AREAM015`, `AREAM022` a
  `AREAM029`, `AREAD075`, `AREAM003`, `AREAM005`, `AREAE024`.
- Risco alto é marcado de forma desigual entre agentes; onde quase nada é marcado, a retrotradução quase
  não roda. Tom e intenção por fala às vezes saem genéricos. Falante de código de retrato desconhecido é
  palpite. O prompt de retrotradução mostra o original ao revisor (não é cego).
- Abreviações de menu e de mapa, acento em rótulo com a fonte de 16 px, nomes de habilidade mantidos em
  inglês, termos de lore e propostas de glossário ainda não ratificados.
- Não garantido: texto dentro de imagem e dentro do executável.

### Passo 4.1: consistência de glossário (2026-10-12)

- Primeira rodada: 5.327 candidatos em 173 termos, quase tudo ruído. Causa: rótulos de menu e de minijogo
  entraram no glossário como palavra comum de uma palavra só, e o lint as procurava em toda fala.
- Correção no lint (`framework/runtime/glossary_lint.py`, com teste): ignora código de controle no meio do
  termo; termo com maiúscula casa na caixa exata; aceita flexão e abreviação da forma canônica; termo de
  uma palavra que só abre frase não é auditado (como linha inteira, que é o rótulo, continua).
- Sobraram 50 casos distintos, resolvidos assim:
  - Tradução corrigida em 153 falas de 35 cenas (cópias incluídas): iscas do minijogo de pesca, rótulo de
    câmera, tipo de fada, índice de aprovação, um título de faixa, nome de dragão que tinha duas formas e
    um que ficara em inglês, "pousada" e "vila" unificados. Duas falas tinham veredito de retrotradução:
    vencido, rejulgado por revisor independente, `pass`.
  - 24 aliases no glossário para variante legítima (rótulo que não cabe na forma canônica, verbo x
    substantivo, título de faixa) e 1 alvo trocado para a forma usada em todas as falas (ponto de pesca
    no mar, igual aos de rio e de lago).
- Três rótulos da lista de destinos não comportam a forma do glossário: a abreviação ficou ruim e, por
  decisão do usuário, voltaram à forma curta anterior, registrada como alias.
- Rótulo do botão de troca de fileira no combate corrigido para a forma do glossário (12 cenas-cópia); o
  alias criado por engano foi removido.
- "town" como "vila" só aparece para a colônia das fadas; mantido.
- Depois das correções: `glossary_lint` 0, `quality_gate` limpo, `reinsert` 286 arquivos, gates do
  conector e do piloto limpos.

### Acabamento do texto de sistema (2026-10-12, noite)

Estado: 296 cenas verificadas (286 de diálogo, 10 de sistema); fila de escalonamento zerada; lint com 0
candidatos; `quality_gate` OK. Ponto de controle da onda aberto, esperando `hitl.py ack` do usuário; depois
dele entram as nove cenas de sistema restantes (E077BTL, DEMO, D152BTL, D142BTL, D141BTL, COMMU09B, COMMU03,
BTLRET, BTLEND). Nada disso foi reinserido nem instalado ainda.

- Fila de 59: resolvida por alias no glossário; entrada "Guard Focus Counter" apagada (era descrição de
  efeito, não termo); nome de item composto entra como `manter_original` para o lint não acusar a palavra de dentro.
- "Cat.:" virou "Categoria:" onde coube (294 de 306). Acento reposto onde os bytes deixam (letra acentuada
  custa 2 bytes); menu de escolha desenha acento normalmente. Lista de tipos de inimigo fica em caixa alta.
- Gentílico: "de Wyndia", nunca "Wyndian" (entrada no glossário). "Dragon of Doom" = "Dragão da Perdição".
- Sotaque francês dos comerciantes: marca leve, uma muleta por fala onde couber ("non?", "oui", "mon ami"),
  sem grafia fonética. Vale para diálogo e sistema.
- A fonte não tem o sinal ordinal: o conector trocava por "?". Ordinal se escreve "3o", "1000o".
- Menus, caixa de Info e faixa de lugar usam a fonte de 24 px (com acento); só a legenda de botões do
  mapa-múndi parece usar a de 16 px. A régua do próximo teste no jogo confirma.
- Revisão humana: `tools_local/revisar.py` gera uma página local no lugar do CSV.
- Pendente de decisão: lista de entradas de palavra comum a apagar do glossário; ratificação dos termos de
  história (Purifiers, Elders, Nameless, Gateway, Dragon of Doom).

Atualização (2026-10-12, 23h): visto da onda dado e cinco termos de história ratificados pelo usuário
(`hitl.py ratify` passou a aceitar termo nomeado fora dos 30 mais frequentes). Glossário limpo: 414 entradas na época (hoje 415),
títulos entram inteiros. As nove cenas de sistema restantes vieram 100% por reuso; 305 cenas verificadas, lint 0,
`quality_gate` e `pilot_gate` OK. Reinserção feita e instalada no jogo com a régua nas folhas de imagem
(`tools_local/probe.py`): a régua é só de medição e sai na próxima instalação. Próximo: prints do usuário
(menu, loja, salvar, acampamento, batalha, fim de batalha) para ler a largura real de cada rótulo.

**Botão do mestre (2026-10-12, 23h30).** O rótulo "Join" da tela do mestre e do acampamento passa de "Unir" para "Mestre" (decisão do usuário, opção B). Estoura o orçamento da fala em 1 byte; a exceção fica registrada em `project.json` (`byte_budget_exceptions`, só essas duas falas) e é lida por `verify_chapter.py` e `reinsert.py`. A seção inteira cabe (o reinseridor reconstrói a tabela). Gates fechados, instalado e aprovado pelo usuário no jogo.

**Instalação (regra do usuário, 2026-10-12):** instalar na pasta do jogo não pede mais ok caso a caso. Condições que seguem: gates fechados, jogo fechado, `.bak` preservado, e avisar o que foi instalado.

**Acabamento das abreviações (2026-10-12).** Regra do usuário: troca só com custo de até +1 byte sobre o
orçamento da linha; acima disso, nunca. Passaram a palavra inteira: Salvar, Mestre, Dormir, Santuário,
Planície, todos, Opções, Bosque Kasq. Ficaram abreviados: Sag., Rep., Escond., os quatro elementos
combinados, Habil., Vel., Equip. São 35 exceções de +1 byte em `byte_budget_exceptions` (`project.json`).
Gates fechados (lint 0, quality_gate, pilot_gate), 22 arquivos instalados sem a régua. As exceções fora
"Mestre" ainda não foram vistas na tela. Passos 14–15 (prints/régua) fechados pelo usuário.

**HITL (pedido do usuário, 2026-10-12; framework, os dois caminhos).** Só bloqueia decisão de verdade:
escopo, caminho e fila de escalonamento. Ratificação dos termos frequentes e visto da onda viraram aviso.
Decisão dada na conversa é registrada pelo assistente com `--quote "frase literal"` (log: `via=conversa`);
sem frase literal do usuário não há registro.

**Rótulos em imagem, etapa 1 — folha principal (2026-10-12).** `connector/labels.py` (chamado pelo `reinsert.py`) redesenha os rótulos da folha de interface com letras tiradas da própria folha; a tabela fica em `project.json` (`image_labels`). 40 rótulos em português, 18 mantidos (decisão anterior ou sem tradução melhor). Três variantes da folha reconhecidas pelo conteúdo; 10 arquivos instalados (CAMP, COMMU03, COMMU09B, D143END, MASTER, MSHOP, SAVE, SGAMEN, SHOP, START). Fora dos retângulos dos rótulos nada muda (teste). Letras desenhadas à mão por não existirem na folha: `V`, `v`, `j`, e os acentos; `O` vem do `C` espelhado. Abreviados por largura: "Próx." e "Compr." (estilo claro), "Venda", "Passo". **Não visto na tela:** a largura de recorte foi medida só em 10 rótulos; nos demais vale a célula até o vizinho, então pode haver corte (os mais longos: Habilidade, Acessório, Completo!, Armadura). Falta: conferir por print; folha de sistema (`INIT.DAT` seção 2 e 0) e os botões de batalha (passo 18).

**Rótulos em imagem, etapa 2 — botões de batalha (2026-10-13, passo 18).** Folha de batalha (`AB000_00.DAT` seção 4), tabela `image_labels.botoes` do `project.json`, código em `connector/labels.py` (`buttons`, `ordinals`). Botões de comando: Atacar, Auto, Especial, Fuga, Item, Defesa ("Charge" liga o ataque automático, daí "Auto", decisão do usuário; "Fuga" acompanha o texto de ajuda) ("Usar Item" mede 58 px num botão de 45; ficou "Item"). Aviso de comando: "Escolha / Comando". Ordem de turno: 1º/2º/3º (anel sublinhado desenhado no lugar do sufixo). A letra `h` dos botões entrou no alfabeto da folha, então "Key" passou a "Chave". O `g` e o `p` dos rótulos desta folha passaram a usar a letra dos botões, com descendente (o `g` original da caixa é achatado e lia como "8"/"B" em "Inimigos"); as folhas principal e de sistema não têm essa fonte e seguem com o `g` original. Instalado em 2026-10-13. Ficam em inglês nesta folha: Exp., Menu, Info, Status, Zenny, Item, Slot, Combo. Conferido: 0 pixel fora dos retângulos; no arquivo remontado só a seção 4 muda. Fora desta etapa (arte em outra fonte, sem letras para compor): "Level up", "Next up", "PAUSE", "EMPTY" da loja, "PgUp/PgDn". Larguras de recorte na tela ainda não conferidas.

**Rótulos em imagem, etapa 1 — folhas de sistema e de batalha (2026-10-13).** Passo 17 fechado. Folha de sistema (`INIT.DAT` seção 2 e cópias em BTLEND, BTLRET, D141BTL, D142BTL, D152BTL, E077BTL, SGAMENX): 27 rótulos em português, 14 mantidos. Folha de batalha (`AB000_00.DAT` seção 4, só nesse arquivo): 21 em português, 9 mantidos (o "Key" ficou em inglês ali por faltar a letra `h` na folha). Tabelas `sistema` e `batalha` em `project.json["image_labels"]`. Conserto no `reinsert.patch_dat_file`: seção 0 que muda de tamanho agora atualiza o próprio tamanho no TOC (a folha é a seção 0 em SGAMENX). Instalado: 9 arquivos. Falta conferir em print: largura de recorte dos rótulos não medidos. Ficam para o passo 18: os botões de batalha (fonte maior) e "Level up", "Next up", "PAUSE", "EMPTY".

### Para o levantamento de fim de projeto

- A planilha da amostra deixa à vista a letra do código de retrato (`A"…`, `@"…`) e isso levou o revisor a
  marcar 31 falas corretas como `erro` até explicarmos. Mostrar o retrato como rótulo separado, não como letra.
- Planilha de QA mostra o texto sem os códigos de controle, e o filtro que os remove come a letra seguinte
  quando ela é A–F; a correção verbatim precisa do texto com códigos. Revisão a partir da planilha exige
  reencaixe. Uma correção passou na conta de bytes e estourou no `verify` por 1 byte (causa não investigada).

- Gate visual 4.3 (jogar o trajeto inteiro uma vez): o usuário tirou do fluxo no bof4. Já levado ao framework a pedido dele (2026-10-12): `docs/TRANSLATION_PIPELINE.md` e o modelo de ROADMAP do scaffold; vale para sessão e API.

- **Reconferência por fala, não por cena.** Uma correção em massa de texto já aprovado (2026-10-12: 786 falas em
  115 cenas, acento e termo) obriga a reconferir a cena inteira de cada fala tocada, em série: cerca de 8 s por
  cena mais 1 min fixo, 15 a 20 min no total. Avaliar: (a) reconferir só as falas tocadas, reaproveitando o
  veredito das demais; (b) rodar as cenas em paralelo, o que pede gravação do `run_state.json` sem disputa.
- **Lista de cenas de um comando de onda** deve ser validada contra o `run_state` antes de rodar: um nome
  inexistente fez a onda parar no ponto de controle como se fosse cena nova, sem processar nenhuma.

## Levantamento de fim de projeto — o que levar para o framework

Aceito por Felipe Scudeller em 2026-10-13. Cada bloco só entra aqui depois do aceite dele.

### 1. Processo e gates (aceito por inteiro)

| Tema | O que o bof4 mostrou | Mudança no framework |
|---|---|---|
| Escopo de extração | Interface, texto de sistema e rótulo em imagem só apareceram no teste dentro do jogo. | Varredura completa na Fase 0, incluindo folhas de imagem; os dois escopos (`dialogo` e `completo`) como padrão. |
| Largura de linha | O limite fixo de 62 nunca dispara neste jogo; 266 textos passavam da caixa. | Limite por caixa, derivado do inglês do próprio jogo; requebra mecânica como passo do pipeline. |
| Códigos de controle | Um parâmetro pode ser `[01]` ou `[02]`; o corte ingênuo corrompe a fala. Menu de escolha tem de ser separado do diálogo ao medir. | Tabela de opcodes com parâmetros no conector, usada por todo passo que mede ou edita. |
| Glossário | Um termo foi traduzido de três formas sem o lint acusar; entraram palavras comuns e entradas malformadas. O lint lê o banco, então edição do glossário exige `state_index` antes. | Entrada por sentido, título inteiro, nome mantido que atravessa quebra de linha, filtro de palavra comum. |
| Decisões cedo | Sotaque, gentílico, gênero de personagem/criatura e registro arcaico foram decididos tarde e custaram retrabalho. | Lista de decisões de voz na fase de KB, antes do piloto. |
| Reconferência | Corrigir 1 fala reprocessava a cena inteira (12 min; 8 s com o atalho de contexto salvo). | Reconferir por fala tocada e em paralelo; validar a lista da onda contra o `run_state`. |
| Retrotradução | O veredito fica velho quando a fala muda; a correção proposta pelo juiz não é medida em bytes nem em códigos. | Invalidar por fala; passar a proposta do juiz pelo mesmo verificador da cena. |
| Revisão humana | CSV e planilha sem códigos são ruins de ler; 1.475 das 3.350 marcações eram nome mantido (ruído). | Página de revisão no framework; planilha com texto codificado e sem nome mantido. |
| Amostra de qualidade | Fica velha a cada correção de texto. | Último passo do fluxo; pré-julgamento por modelo e conferência humana das apontadas mais um sorteio das aprovadas. |
| Orçamento de bytes | A conta feita fora do `verify_chapter` errou por 1 byte. | Uma única função de contagem; exceção de +1 registrada no `project.json`. |
| Rótulos em imagem | Funcionou compor com as letras da própria folha e aplicar por hash do conteúdo. | Passo documentado, com régua antes do desenho. |
| HITL | O comando no terminal quase não foi usado; a decisão na conversa, registrada com a frase literal, funcionou. | Manter decisão na conversa com registro; só ambiguidade real vai para o humano. |

### 2. Skills (aceito por inteiro)

Hoje são 13; o número está razoável, o problema é cobertura. Fica em 14 ou 15.

- **Juntar:** `06b_micro_qa` e `06c_correction_cycle` viram uma só; na prática foram um ciclo único.
- **Criar:** uma para texto de sistema e rótulos em imagem; uma para o teste dentro do jogo (diagnóstico de print até a causa raiz), onde mais tempo se gastou sem roteiro.
- **Ampliar:** `00_extraction` com a varredura de escopo; `04_glossary_creation` com as regras de sentido; `07_qa` com largura e amostra no fim.
- **Caminho de sessão:** hoje vive em scripts locais do projeto (`lot.py`, `dup.py`, `plan.py`, `part.py`, `triagem.py`, `revisar.py`, `install.py`). Sobe para o framework, com a skill `06_translation` descrevendo os dois caminhos.

### 3. Caminho de sessão (aceito, com condição: benchmark antes de levar)

Nada deste bloco entra no framework sem benchmark que meça o ganho antes.

- **Ponta a ponta:** funcionou em 305 cenas, 27.021 falas, sem gasto de API.
- **Portões novos:** uma só escolha de caminho por projeto, com HITL; recusa na entrada do caminho de API quando o projeto é de sessão.
- **Ideias da API que não vieram:** lote de correção automático, melhor versão por fala entre tentativas, modelo barato primeiro. Só a primeira vale a pena.
- **Ranking de modelo:** não era aplicado na sessão. Ficou Sonnet traduz e Opus retrotraduz; Haiku só se mostrou seguro para rótulo curto.

### 4. Custo (aceito)

Leitura do Felipe: o resultado é positivo, porque o bof4 traduziu e construiu o processo ao mesmo tempo; o segundo projeto é a medida limpa.

- **Medido:** equivalente a $239 de API, pago $0 pela sessão. Cache $163 (68%); tradução + governança $12,50; o resto ($227) é orquestração, conector, construção do framework e diagnóstico do jogo.
- **O que reduziu de verdade:** disparo por onda com um aviso só, subagente enxuto, um agente de retrotradução por onda, pré-filtro em memória na busca semântica, `/clear` na virada de fase, Sonnet na janela principal.
- **Para caber no Pro:** o gargalo é a orquestração na janela principal. Testar um comando por onda em vez de uns 13 (ainda não testado) e ondas menores com `/clear` entre elas.
- **Medidor:** 37% dos tokens de saída são estimados, não lidos; corrigir antes do projeto novo.
- **Projeto novo:** só depois de levar os blocos 1 e 2 e de fazer o benchmark do bloco 3.
