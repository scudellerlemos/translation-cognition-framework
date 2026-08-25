# Research Log — The Legend of Heroes: Trails in the Sky 2nd Chapter

**Status:** reconciled
**Data de reconciliação:** 2026-08-23
**Fronteira de spoiler:** escopo do corpus atual (demo Steam, `artifacts/dialogs.csv`, 71 cenas —
`mp0000`–`mp8010`-ish, trecho inicial do jogo). O desaparecimento de Joshua e a menção a
"true identity" são a PREMISSA do jogo (estabelecida antes do ponto onde a demo começa, é como
a SC se apresenta oficialmente) — não tratado como spoiler para fins de tradução. Reveals
posteriores (identidade de Ouroboros, backstory de Renne, antagonista final) foram **pesquisados
integralmente** via SRC-007 e capturados em `artifacts/spoiler_ledger.json` — o framework tem
mecanismo próprio de guard temporal (`spoiler_ledger.json` + `context_pack.select_spoiler_guards()`
+ `spoiler_check.py`) para controlar a exposição desses fatos na tradução por posição de cena; a
pesquisa não precisa esperar o corpus avançar, só a exposição na prosa/tradução é que fica
gated pelo ledger.

---

## Fontes Avaliadas

| ID | Fonte | Tipo | Tier | Cobertura de Spoiler | URL/Caminho | Encontrada por | Usada | Notas |
|----|-------|------|------|----------------------|-------------|----------------|-------|-------|
| SRC-001 | `artifacts/dialogs.csv` (corpus da demo) | Corpus | 1 | Escopo da demo | local | IA | Sim | Fonte primária — mineração de frequência de nomes próprios (41.834 linhas) |
| SRC-002 | operationrainfall.com — "Trails in the Sky 2nd Chapter Introduces Main Characters and Voice Cast" | Imprensa/material de divulgação do publisher | 1 | Personagens principais (bios de anúncio, sem reveals) | https://operationrainfall.com/2026/03/09/trails-in-the-sky-2nd-chapter-introduces-main-characters-and-voice-cast/ | IA | Sim | Reproduz descrições oficiais de divulgação (8 personagens jogáveis principais) |
| SRC-003 | Trails Wiki (Fandom) — "Trails in the Sky - Second Chapter" | Wiki | 2 | Premissa geral + elenco de personagens introduzidos; sem reveals de plot | https://trails.fandom.com/wiki/Trails_in_the_Sky_-_Second_Chapter | IA | Sim | Fetch direto bloqueado (HTTP 402); lida via busca segmentada restrita ao domínio (mesmo workaround do SRC-006/007). Corrobora premissa e cita Josette Capua, Mueller Vander, Julia Schwarz |
| SRC-004 | Site oficial — trails2ndchapter.com/characters/ | Oficial (dev/publisher) | 1 | Bios oficiais de personagens (incl. Ouroboros: Leonhardt, Campanella) | https://trails2ndchapter.com/characters/ | IA | Sim | Fetch direto bloqueado (HTTP 403); lida via busca segmentada restrita ao domínio. Fonte Tier 1 (material oficial do publisher) |
| SRC-005 | Gematsu — "Trails in the Sky 2nd Chapter details more characters, fishing and Viewer Mode" | Imprensa | 2 | Personagens secundários novos (recepcionistas da Bracer Guild) | https://www.gematsu.com/2026/07/trails-in-the-sky-2nd-chapter-details-more-characters-fishing-and-viewer-mode | IA | Sim | Fetch direto bloqueado (HTTP 403); lida via busca segmentada restrita ao domínio. Confirma Aina Holden (recepcionista da filial de Rolent) — fecha o gap de personagem de fundo identificado na mineração do corpus (SRC-001) |
| SRC-006 | Kiseki Wiki (Fandom) — "The Legend of Heroes: Trails in the Sky SC" (jogo original, 2006) | Wiki | 2 | Introdução/premissa + bios de personagens principais; NÃO lido além disso | https://kiseki.fandom.com/wiki/The_Legend_of_Heroes:_Trails_in_the_Sky_SC | Usuário | Sim | Enviado pelo usuário. Fetch direto da página bloqueado (HTTP 402, mesmo padrão do SRC-003); contornado via busca segmentada (personagem por personagem) sobre o domínio, sem abrir a página de "Story"/plot completa — preserva a fronteira de spoiler |
| SRC-007 | Kiseki Wiki (Fandom) — "...SC/Story" (sinopse completa do jogo original, 2006) | Wiki | 2 | **COMPLETA: Prólogo até o Finale** — cobre o jogo inteiro, incluindo todos os plot twists (revelação de Weissmann/Angel Weissmann, Stigma do Joshua, backstory e reveal da Renne, morte do Loewe, final "Trails in the Sky") | `manual_tests/artifacts/kb_0_human_fonts.pdf` (PDF enviado pelo usuário, print da página) | Usuário | Sim | Lida integralmente. Fatos de prólogo/premissa corroboram SRC-002/SRC-006 (ver Conflitos Resolvidos). Os reveals de Cap.1 em diante (Stigma, Renne, Weissmann, Loewe/Leonhardt, Kevin Graham, final) foram pesquisados por completo e capturados em `spoiler_ledger.json` — **não omitidos**: o framework tem mecanismo próprio para isso (`spoiler_ledger.json` + `context_pack.select_spoiler_guards()` + `spoiler_check.py`), então pesquisar até o fim e quarentenar via ledger é o padrão correto, não deixar de pesquisar por o corpus atual ser uma demo. Ver `artifacts/spoiler_ledger.json` |

**Nota de conhecimento prévio:** este é um remake (2026) da história original de *Trails in the Sky
SC* (2006, Liberl arc). A IA tem conhecimento de treino sobre a obra original, mas **não usou esse
conhecimento como fonte** para nenhuma afirmação do KB — só o que está citado em
SRC-001/SRC-002/SRC-006/SRC-007. O usuário confirmou o vínculo ao enviar o link do wiki do jogo
original (SRC-006) como referência válida para o remake — registrado aqui como a fonte que
estabelece essa ponte.

**Uso de SRC-007 e mecanismo de spoiler do framework:** SRC-007 é a sinopse completa do jogo
original (prólogo → finale), enviada pelo usuário como PDF porque a página não era acessível para
fetch direto. Lida integralmente. Fatos do Prólogo corroboram o que já estava sourced por
SRC-002/SRC-006 (motivo da partida de Estelle, papel de Kevin Graham na viagem de airship, local de
treino de Estelle/Anelace — Le Locle, região de Leman, sede da Bracer Guild) e foram incorporados
diretamente ao `universe_knowledge_base.md`. Os reveals de Cap.1 em diante (Stigma do Joshua,
Tragédia de Hamel, verdadeira natureza da Renne, Plano do Evangelho de Weissmann, Loewe = Leonhardt,
missão real de Kevin Graham, final do jogo em Liber Ark) **foram pesquisados por completo** e
capturados em `artifacts/spoiler_ledger.json` (fato completo por entrada, sourced SRC-007) —
corrigindo uma abordagem anterior deste log que tratava "corpus é demo" como motivo para não
pesquisar: o framework já tem o mecanismo certo para isso (`spoiler_ledger.json` lido por
`context_pack.select_spoiler_guards()` para injetar guards pré-tradução, auditado por
`spoiler_check.py` pós-tradução), então a pesquisa não precisa — e não deve — parar na fronteira do
corpus; só a *exposição* na prosa do KB e nas traduções é que fica temporalmente controlada pelo
ledger. Todas as entradas usam `reveal: "beyond_frontier"` por ora, pois ainda não há mapeamento
confirmado capítulo→scene_id para este corpus (default seguro do framework).

---

## Conflitos Resolvidos

Nenhum conflito de conteúdo entre SRC-002 (imprensa/divulgação do remake), SRC-006 (wiki do jogo
original, bios) e SRC-007 (sinopse do prólogo, uso restrito) nas entidades pesquisadas — os 8
personagens principais, a Bracer Guild, o Royal Army of Liberl e a Ouroboros descrevem de forma
consistente entre as fontes (SRC-002 cobre o elenco do remake; SRC-006/SRC-007 aprofundam papel/
personalidade a partir do jogo original). Tratado como corroboração (critério "múltiplas
corroborações prevalecem"), não como divergência. SRC-007 acrescentou um dado novo sem conflito:
Le Locle (campo de treino de bracers) fica na região/país de Leman, sede principal da Bracer Guild —
detalhe ausente de SRC-002/SRC-006, incorporado à entrada de Anelace Elfead.

---

## Gaps de Pesquisa

- ~~SRC-003/SRC-004/SRC-005 não lidas~~ **RESOLVIDO 2026-08-23**: lidas via busca segmentada
  restrita ao domínio (mesmo workaround do SRC-006/007). Ver tabela de Fontes Avaliadas.
- **Personagens secundários/background de menor frequência no corpus** (Norman, Luke, Portos,
  Herio) — identificados pela mineração (SRC-001) mas ainda não pesquisados externamente; ficam
  UNSOURCED/background, a aprofundar via `kb_phase.py` quando a cena real que os usa for traduzida.
  **Aina** foi resolvida (ver SRC-005 — Aina Holden, recepcionista da Bracer Guild em Rolent).
- ~~Renne/Ouroboros/Weissmann/Loewe/final do jogo não pesquisados~~ **RESOLVIDO 2026-08-23**: SRC-007
  lida integralmente; reveals capturados em `artifacts/spoiler_ledger.json` (7 entradas — Stigma do
  Joshua, Tragédia de Hamel, verdadeira natureza da Renne, Weissmann/Plano do Evangelho,
  Loewe = Leonhardt, missão real de Kevin Graham, final em Liber Ark). Todas com `reveal:
  "beyond_frontier"` (sem mapeamento capítulo→scene_id confirmado ainda para este corpus). O KB
  (`universe_knowledge_base.md`) mantém a prosa visível espoiler-safe (mesmo padrão do
  `utawarerumono`: reveals além da fronteira ficam no ledger, não expandidos na prosa principal),
  com nota cruzada apontando para o ledger onde relevante.
- **Mapeamento capítulo→scene_id** ainda não existe para este corpus (71 cenas, prefixos
  `mp0000`/`mp2000`/`mp4000`/`mp6000`/`mp8000`+sufixos, sem correspondência confirmada aos
  capítulos do jogo original) — necessário para trocar `reveal: "beyond_frontier"` por scene_ids
  concretos no `spoiler_ledger.json` conforme a tradução avança. Deferido a `kb_phase.py`/revisão
  humana quando os capítulos reais forem trabalhados.
