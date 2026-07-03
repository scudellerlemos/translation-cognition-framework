# Universe Knowledge Base — Souldiers (PT-BR)

> Status: reconciled — 2026-07-02
> Fontes: research_log.md (corpus + Wikipedia/HandWiki/TheGamer/Steam Discussions, Fandom bloqueada). Ver research_log.md para proveniência detalhada por entidade.
> Este documento é a referência sintética de KB para o pipeline de tradução (context_pack).

---

## Tom geral

Metroidvania/RPG de ação, dark fantasy com influências nórdicas e egípcias (Valquírias, Ratatosk,
mundo dos mortos, Anubis). Tom sério mas não pesado; humor situacional e de personagem (não meta).
Prioridade: naturalidade e fluidez de leitura rápida. Ver `tone_analysis.md` para perfis de voz
completos por personagem.

---

## Personagens Principais

| Personagem | Tradução/Grafia PT-BR | Notas |
|---|---|---|
| Brigard | Brigard (verbatim) | General, comandante do regimento. Formal-militar seco. 102 linhas no corpus. |
| Euder | Euder (verbatim) | Soldado companheiro, missões no Fyr Forest. Coloquial informal arrogante. 101 linhas. |
| Jivan | Jivan (verbatim) | Coruja fundadora de Hafin, questiona Valquírias. Formal-misterioso. 61 linhas. |
| Balof | Balof (verbatim) | Mercador javali, loja em Hafin City. Principal vetor de humor do jogo. 60 linhas. |
| Sirfiel | Sirfiel (verbatim) | Capitã e estudiosa, irmã de Melian. Formal-médio, enciclopédica. 56 linhas. |
| Beigon | Beigon (verbatim) | Guardião de Terragaya. 54 linhas. |
| Edil | Edil (verbatim) | Garota maga de Hafin. Casual-positiva, incentivadora. 43 linhas. |
| Melian | Melian (verbatim) | Soldado sentinela, irmão de Sirfiel. Casual-militar, impaciente. 33 linhas. |
| Gartua | Gartua (verbatim) | Anão mecânico, fornece upgrades. Áspero, direto. 24 linhas. |
| Makarel/Gruper | Makarel/Gruper (verbatim) | Dupla cômica de soldados medrosos. Corpus usa speaker `MAKEREL` como ID interno; "Makarel" é a grafia canônica ratificada (research_log.md, 2026-07-02). |
| Valquíria | Valquíria (traduzido — equivalente consagrado) | Entidade que abre a história, leva almas a Terragaya. Formal-solene, proclamação ritual. |
| Arkzel | Arkzel (verbatim) | Feiticeiro/conselheiro do rei; antagonista revelado tarde. Formal-calculista, controlado. Amigo de Brigard e par de estudos de Sirfiel; desaparecido desde um terremoto, suspeito de corrupção por parasita (diário de Brigard). Nunca fala diretamente no corpus até agora — personagem ausente/referenciado, não falha de extração. |
| Ratatosk | Ratatosk (verbatim) | Criatura mitológica nórdica (esquilo de Yggdrasil). 6 linhas. |

## NPCs com fala relevante — UNSOURCED (decisão: verbatim, ratificada 2026-07-02)

> Descobertos por contagem real de linhas no corpus (`dialogs.csv`), sem cobertura em nenhuma
> fonte pesquisada. **Handling rule ratificada: verbatim** (nome próprio, baixo risco de erro de
> tradução mesmo sem lore confirmada) — não fabricar biografia/papel narrativo até haver fonte.
> Decisão do usuário: não bloquear a escala por isso; QA humano dá atenção extra a essas linhas.
> Todos os 22 já estão em `glossary.csv` como `handling_rule: verbatim`. Ver research_log.md
> § Decisões resolvidas.

| Speaker | Linhas | Handling rule |
|---|---|---|
| Liandris | 80 | verbatim (UNSOURCED) |
| Adamont | 70 | verbatim (UNSOURCED) |
| Cromachief / Cromaminion(B) | 53 / 33+7 | verbatim (UNSOURCED) — possível relação chefe/minion |
| Fishchief / Fishminion | 53 / 18 | verbatim (UNSOURCED) — possível relação chefe/minion |
| Galath | 43 | verbatim (UNSOURCED) |
| Sangrigor | 37 | verbatim (UNSOURCED) |
| Sinka | 34 | verbatim (UNSOURCED) |
| Birk | 24 | verbatim (UNSOURCED) |
| Freydin | 21 | verbatim (UNSOURCED) |
| Finse | 19 | verbatim (UNSOURCED) |
| Skribles | 18 | verbatim (UNSOURCED) |
| Darksword | 17 | verbatim (UNSOURCED) — provável boss |
| Anubis | 14 | verbatim (UNSOURCED) — referência mitológica egípcia |
| Darkwarrior / Ironclad / Esfinge | 4 / 2 / 2 | verbatim (UNSOURCED); Esfinge já é PT/ES p/ Sphinx |

## Mundo e Lore

| Termo EN | PT-BR | Notas |
|---|---|---|
| Terragaya | Terragaya (verbatim) | Mundo do além. 16 menções. |
| Ascil | Ascil (verbatim) | Continente de origem. |
| Zarga | Zarga (verbatim) | Nação do protagonista. 36 menções. |
| Dadelm | Dadelm (verbatim) | Exército inimigo. 4 menções. |
| Hafin City / Hafin | Hafin City / Hafin (verbatim) | Capital de Terragaya. 43 menções. |
| Fyr Forest | Fyr Forest (verbatim) | Floresta com missões de tempo, ligada a Euder. |
| Valley of Silence | Vale do Silêncio (traduzido) | Local. |
| Fire Temple | Templo do Fogo (traduzido) | Local. |

## Sistema (elementos, status, classes)

| Termo EN | PT-BR | Notas |
|---|---|---|
| Fire / Earth / Lightning / Water / Wind | Fogo / Terra / Raio / Água / Vento | Elementos — traduzido. |
| Burn / Blindness / Frost / Bleeding / Paralysis | Queimadura / Cegueira / Gelo / Sangramento / Paralisia | Status de efeito — traduzido. |
| Legion | Legião | Unidade militar — traduzido. |
| Guardian | Guardião (contexto genérico) | Beigon é verbatim como nome próprio; "Guardian" genérico traduz. |
| Scout / Archer / Caster | Batedor / Arqueiro / Conjurador (proposto) | Classes do protagonista — a confirmar em texts_GUI/texts_MENU (Fase 3, pendente, ver kb_phase_worklist.md). |

---

## Cobertura e limitações desta reconciliação

- **13 personagens principais** com pesquisa externa reconciliada (Wikipedia/HandWiki/TheGamer).
- **22 NPCs com fala relevante (14–80 linhas cada) permanecem UNSOURCED** — nenhuma fonte tentada
  os cobriu. Fandom Wiki (fonte com maior chance de cobertura) retornou 402 (bot-blocked).
- Handling rule para os UNSOURCED é **verbatim** (ratificado 2026-07-02) — seguro para tradução
  (nomes próprios não devem ser traduzidos de qualquer forma), mas não há garantia sobre papel
  narrativo, spoiler ou gênero gramatical até pesquisa real acontecer.
- **Decisão 2026-07-02: escalar a tradução agora**, sem bloquear pelo gap de pesquisa desses 22
  NPCs — especialmente Liandris, Adamont, Cromachief e Fishchief (>50 linhas cada, provavelmente
  personagens centrais de arcos posteriores). QA humano deve prestar atenção extra a essas linhas.
