# Decision Log — The Legend of Heroes: Trails in the Sky 2nd Chapter

## Convenções gerais

- **Convenção de `handling_rule`:** `manter_original` / `traduzir` (PT), não `verbatim` / `translate`
  (EN) — segue o padrão já usado em `utawarerumono`. Razão: `glossary_lint.py` só audita presença
  verbatim quando o valor é exatamente a string `"manter_original"`; qualquer outro valor (incluindo
  o inglês `"verbatim"`) cai no ramo de auditoria de forma traduzida e silenciosamente pula o check
  verbatim. Ver `framework/runtime/glossary_lint.py:86-93`.
- **"você"** (não "tu") em todo o diálogo — PT-BR padrão, sem lusismos.

## Nomes próprios

- Todos os 8 personagens jogáveis principais + Cassius Bright, Renne, Anelace Elfead e Kevin Graham:
  `manter_original` (nomes próprios não têm tradução consagrada; jogo inédito, sem localização
  oficial anterior para pt-BR).
- Locais (Liberl, Rolent, Bose, Ruan, Zeiss, Grancel): `manter_original` — topônimos fantasiosos,
  sem análogo real a traduzir.
- Ouroboros, Aidios: `manter_original` — nomes próprios de organização/divindade.

## Traduções canônicas

- **Bracer Guild → "Guilda dos Bracers"** (CONFIRMADO pelo usuário em 2026-08-23): mantém "Bracer"
  como termo técnico do universo (função/profissão, não traduzível 1:1 — "mercenário licenciado" foi
  descartado por perder o peso de termo próprio do mundo) e traduz só a estrutura "Guild → Guilda".
- **Royal Army of Liberl → "Exército Real de Liberl"** (CONFIRMADO pelo usuário em 2026-08-23):
  tradução direta, sem termo técnico intraduzível envolvido.
- **Goddess → "Deusa"**: tradução direta; termo comum (não nome próprio), sem ambiguidade.
- Nenhuma dessas três traduções tem precedente de localização oficial pt-BR (jogo inédito/remake sem
  versão brasileira anterior). As duas primeiras foram validadas pelo usuário nesta rodada; aplicação
  em massa liberada para `kb_phase.py`.

## Cobertura de vocabulário — Arts/Crafts e UI (2026-08-23)

- **Arts/Crafts/S-Crafts/habilidades reativas** (226 termos, `manter_original` / `Mecânica`):
  descobertos em `pac/steam/table_en.pac -> table_en/t_skill.tbl`. Nomes de habilidade seguem a
  mesma regra dos termos de mecânica já estabelecidos (Quartz, Orbment, Sepith, Mira, Art) — são
  jargão de sistema de jogo, não prosa traduzível. Ver `connector/table_schema.md` RETOMADA #4.
- **Texto de UI/menu** (439 termos, `traduzir` / `UI`): descoberto na mesma tabela `t_text.tbl`
  (1603 pares `TXT_<chave>`→valor, ~40 prefixos de subsistema: CAMP, OPT, NOTE, BTL, SHOP, QUEST,
  HUD etc.). Filtrado por heurística "label-like" (valor único pra chave, sem `.?!%`, ≤28
  caracteres, sem token de ícone `<I...>`) e deduplicado por valor (572→464). Os 446 pares
  `TXT_STEAM_*` (config gráfica/controle específica de porte PC) foram **excluídos** por escopo —
  não são "tela de menu do jogo", candidatos a uma Fase 3.5 futura se necessário. 15 chaves de
  objeto de campo/debug (`TXT_DOOR`, `TXT_TEST_*` etc.) também excluídas do glossário. Ver
  `connector/table_schema.md` RETOMADA #5.
- **Abreviações de stat** (STR/DEF/ATS/ADF/SPD/MOV, `manter_original` / `Mecânica`): adicionadas
  junto com o lote de UI, mesma regra dos demais termos de mecânica.
- **Sem fabricação — 7 legendas de aba do CAMP** (Equip/Orbment/Item/Status/Achievement/
  Costume/System): procuradas exaustivamente em `t_text.tbl` (chaves exatas e padrões
  `*_TAB*`) e **não encontradas** como string extraída própria — só existem variantes `_HELP`
  (descrição da aba, ex. `TXT_CAMP_TOP_TAB_HELP_EQUIP` → "Change equipment."). Decisão: **não
  adicionar ao glossário** sem fonte extraída real (regra de não fabricar termos fora do dado do
  jogo) — pendência registrada e deixada em aberto por decisão do usuário (2026-08-23).
- Resultado: `glossary.csv` 333→772 linhas (breakdown: UI 442, Mecânica 243, Missão 54,
  Personagem 21, Local 6, Facção 3, Conceito 3).

## `system_line_convention: "none"` (2026-08-23)

- Testada a heurística `all_caps` (usada em `utawarerumono`) contra o corpus real de
  `dialogs.csv` (41.834 linhas): 24 linhas totalmente maiúsculas, mas a maioria é diálogo
  gritado/dramático (falso positivo — ex. "LET! ME! GOOOOO!", "JUST ANSWER THE QUESTION!").
  As únicas linhas genuinamente de sistema (15, valores curtos `OFF`/`HIGH`/`MID`/`LOW`) vêm de
  um único arquivo (`scena/mp2052_01.dat`, provável dispositivo interativo de uma cena
  específica), não um padrão geral do corpus.
- Conclusão: texto de sistema/menu não está misturado em `dialogs.csv` — vive inteiramente na
  tabela separada `t_text.tbl` (já catalogada acima, categoria UI). Valor setado em
  `project.json`: `system_line_convention: "none"` (mesma convenção de `souldiers`); as 15 linhas
  de `mp2052_01.dat` recebem tradução literal comum, sem heurística dedicada (escopo pequeno
  demais). Rationale completo também em `project.json` (campo `notes`) e
  `connector/table_schema.md` RETOMADA #5.

## Tratamento de spoiler (correção 2026-08-23)

- Abordagem anterior (não pesquisar reveals além da fronteira do corpus "porque é uma demo") foi
  **corrigida pelo usuário**: o framework já tem mecanismo próprio para lidar com spoiler
  (`spoiler_ledger.json` + `context_pack.select_spoiler_guards()` + `spoiler_check.py`, mesmo padrão
  usado em `utawarerumono`), então a pesquisa deve ser feita por completo (quando a fonte está
  disponível, como SRC-007) e a exposição controlada pelo ledger — não a pesquisa em si.
- `artifacts/spoiler_ledger.json` criado com 7 entradas (Stigma do Joshua, Tragédia de Hamel,
  natureza real da Renne, Weissmann/Plano do Evangelho, Loewe=Leonhardt, missão real de Kevin
  Graham, final em Liber Ark), todas `reveal: "beyond_frontier"` — sem mapeamento capítulo→scene_id
  confirmado ainda para este corpus.
- `universe_knowledge_base.md` mantém a prosa visível espoiler-safe para essas entidades (mesmo
  padrão do `utawarerumono`: reveals além da fronteira ficam detalhados no ledger, não expandidos na
  prosa principal do KB), com nota cruzada apontando para o ledger em cada entrada afetada
  (Renne, Ouroboros, Leonhardt, Kevin Graham, Joshua Bright).

## Correção da métrica de byte_budget + backend de execução (2026-08-24)

- **Bug de raiz corrigido no framework** (não no projeto): a cena `mp0010_01` reportou 308/447 linhas
  `soft_failed` por estouro de `byte_budget`. Causa real: `framework/runtime/model.py` usava a forma
  TRANSLITERADA (sem acento) como métrica de orçamento em todo o pipeline, incondicionalmente — correto
  para `bof4`/`utawarerumono` (translitera na gravação), errado para `trails_sky_sc`, cujo `reinsert.py`
  grava bytes UTF-8 reais (acento não some, custa byte extra). Corrigido via `_budget_len()`, que agora
  lê `connector.target_charset_supported` do `project.json` para escolher a métrica certa. Ver ADR 0005
  (`framework/docs/adr/0005-budget-metric-per-connector-charset.md`) para o design completo.
- `project.json` atualizado: `connector.target_charset_supported: true` + `charset_note` citando a
  confirmação in-game de 2026-08-23 (acentos pt-BR renderizam sem clipping, NPCs Skyler/Fabree,
  `scena/mp0000.dat`) — já registrada em `notes`, agora também no campo estruturado que o gate de tipos
  (`config.py::validate_connector_types`) exige.
- **Backend de execução — decisão human-in-the-loop**: por instrução do usuário, o esforço de tradução
  roda LOCAL via GPU (Ollama) OU via ferramenta de harness (API), com a escolha explícita do humano via
  `--backend`, não decidida unilateralmente pela IA. `in-session` (humano+Claude no chat) fica fora do
  escopo de automação nova. Ambiente confirmado nesta sessão: Ollama **não instalado**; GPU local = AMD
  Radeon RX 6650 XT (8 GB VRAM, RDNA2, driver 32.0.21045.1000) — já era o hardware-alvo documentado em
  `ollama_client.py`. Framework nivelado para que `ollama` tenha a mesma robustez de retry por orçamento
  que `api` já tinha (sem isso, escolher `ollama` seria uma armadilha sem escalonamento de aperto).
  Instalação real do Ollama + `ollama pull qwen2.5:14b` e re-run end-to-end de `mp0010_01` ficam
  pendentes de confirmação do usuário (download de vários GB, risco de ROCm-no-Windows não suportar
  RDNA2 sem `HSA_OVERRIDE_GFX_VERSION` — a validar empiricamente, não assumido).
