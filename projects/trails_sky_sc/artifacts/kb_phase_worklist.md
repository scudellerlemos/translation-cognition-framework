# KB Phase Worklist — The Legend of Heroes: Trails in the Sky 2nd Chapter

## Fase 1 — Personagens principais
- [x] Pesquisar personagens via wiki/fandom (skill 03) — SRC-002/SRC-006, ver `research_log.md`
- [x] Reconciliar com usuário — status: reconciled, 2026-08-23 (usuário contribuiu SRC-006)
- [x] Preencher glossary.csv com personagens (handling_rule: manter_original)
- [x] Preencher tone_analysis.md com voice cards (### Nome — `voice_criticality: X`) — 8 principais

## Fase 2 — Terminologia e lore
- [x] Identificar termos de lore, locais, facções — Liberl e 5 regiões, Bracer Guild, Royal Army,
      Ouroboros, Aidios (ver `universe_knowledge_base.md`)
- [x] Preencher glossary.csv com termos (handling_rule: manter_original ou traduzir)
- [x] Atualizar decision_log.md com decisões não-óbvias — convenção manter_original/traduzir,
      propostas de tradução de Bracer Guild/Royal Army pendentes de confirmação do usuário

## Fase 2.5 — Spoiler ledger (2026-08-23)
- [x] Fonte enviada pelo usuário (SRC-007, sinopse completa do jogo original) lida por completo —
      corrigindo abordagem anterior que evitava pesquisar além da fronteira do corpus "por ser
      demo" (ver `decision_log.md`, seção "Tratamento de spoiler")
- [x] `artifacts/spoiler_ledger.json` criado com 7 entradas (Stigma do Joshua, Tragédia de Hamel,
      natureza real da Renne, Weissmann/Plano do Evangelho, Loewe=Leonhardt, missão real de Kevin
      Graham, final em Liber Ark) — todas `reveal: "beyond_frontier"` (sem mapeamento
      capítulo→scene_id confirmado ainda)
- [x] Guards verificados: `spoiler_check.py projects/trails_sky_sc --list-guards` → 7 guards ativos
- [x] `universe_knowledge_base.md` atualizado com notas cruzadas para o ledger nas entradas Renne,
      Ouroboros, Leonhardt, Kevin Graham, Joshua Bright (prosa visível continua espoiler-safe)
- [x] `research_log.md`/`decision_log.md` revisados para refletir a pesquisa completa (SRC-007
      "Usada: Sim") em vez do framing anterior de uso restrito
- [x] `kb_gate.py` revalidado após as mudanças — `OK: cobertura de KB suficiente.`
- [ ] Mapear capítulo→scene_id do corpus real quando a tradução avançar, para trocar
      `reveal: "beyond_frontier"` por scene_ids concretos nas entradas do ledger

## Fase 3 — UI/Menus (pós-piloto)
- [ ] Verificar termos de UI em jogo
- [ ] Adicionar ao glossary.csv com handling_rule: translate
