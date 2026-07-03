# Research Log — Souldiers PT-BR

status: reconciled

---

## cap.all — pesquisa global (corpus flat)

> Seção única para o modelo flat (jogo sem estrutura de capítulo). Reconstruído em 2026-07-02 a
> partir do material já reconciliado em `decision_log.md`, `tone_analysis.md`,
> `profile/voice_profiles_reference.md`, `profile/terminology_seeds.md` e `glossary.csv` — sem
> pesquisa externa nova nesta passagem. Ver [[onboarding-scaffold-kb-gate-drift]] para o contexto
> de por que este arquivo não existia antes.

### Fontes utilizadas

| ID | Fonte | Tipo | Tier | Cobertura | Encontrada por | Usada | Notas |
|----|-------|------|------|-----------|-----------------|-------|-------|
| SRC-001 | corpus `artifacts/dialogs.csv` (2561 strings, extração direta do connector Unity Addressables) | Corpus | 1 | Corpus completo (texts_DIALOGS + INGAME + SIDE) | IA | Sim | Fonte primária — frequências e speaker codes citados abaixo são contagem real sobre este arquivo |
| SRC-002 | Wikipedia (artigo Souldiers) | Wiki | 2 | Personagens principais, lore geral | IA | Sim | — |
| SRC-003 | HandWiki (espelho/derivado de conteúdo wiki) | Wiki | 2 | Personagens, mecânicas | IA | Sim | — |
| SRC-004 | TheGamer (guia/artigo editorial) | Guia | 2 | Visão geral de mundo/lore | IA | Sim | — |
| SRC-005 | Steam Discussions (threads da comunidade) | Fórum | 3 | Detalhes pontuais de mecânica/lore | IA | Sim | Especulativo — usar com cautela, não é fonte oficial |
| — | Fandom Wiki oficial de Souldiers | Wiki | — | — | IA | **Não** | Retornou HTTP 402 (bot-blocked) — não foi possível ler. Se o usuário tiver acesso, é a fonte de maior cobertura provável. |

### Fronteira de spoiler

Não há corte de capítulo definido para este jogo (extração é do corpus completo de diálogo,
não faseada). `kb_frontier` em `project.json` usa a convenção já validada em produção (BoF4): um
caminho de arquivo em vez de scene_id numérico, porque os IDs de cena aqui são nomeados
(`EUDER_PRESENTATION`, `AAF_GARTUA_1_1`, ...), não sequenciais — a checagem de fronteira do
`kb_gate.py` reduz a tupla vazia em ambos os lados e não bloqueia, mesmo comportamento do BoF4.

---

### Entidades e fontes por categoria

#### Personagens principais (SRC-002/003/004, corroborados pelo corpus SRC-001)
- **Brigard**: general do regimento, comandante da campanha; registro formal-militar seco. 102 linhas no corpus (speaker `BRIGARD`). Fonte: SRC-002/003 + SRC-001.
- **Euder**: soldado companheiro, dá missões no Fyr Forest; coloquial informal arrogante. 101 linhas (speaker `EUDER`). Fonte: SRC-002/003 + SRC-001.
- **Jivan**: coruja fundadora de Hafin, questiona Valquírias. 61 linhas (speaker `JIVAN`). Fonte: SRC-002/003 + SRC-001.
- **Balof**: mercador javali, principal vetor de humor do jogo. 60 linhas (speaker `BALOF`). Fonte: SRC-002/003/004 + SRC-001.
- **Sirfiel**: capitã e estudiosa, irmã de Melian. 56 linhas (speaker `SIRFIEL`). Fonte: SRC-002/003 + SRC-001.
- **Beigon**: Guardião de Terragaya. 54 linhas (speaker `BEIGON`). Fonte: SRC-002 + SRC-001.
- **Edil**: garota maga de Hafin, casual-positiva. 43 linhas (speaker `EDIL`). Fonte: SRC-002/003 + SRC-001.
- **Melian**: soldado sentinela, irmão de Sirfiel. 33 linhas (speaker `MELIAN`). Fonte: SRC-002/003 + SRC-001.
- **Gartua**: anão mecânico, fornece upgrades. 24 linhas (speaker `GARTUA`). Fonte: SRC-002/003 + SRC-001.
- **Makarel/Gruper**: dupla cômica de soldados medrosos. Gruper: 10 linhas (+1 `GRUPERMAKEREL`). Makarel: corpus usa speaker `MAKEREL` (12 linhas). Fonte: SRC-002/003 + SRC-001.
- **Valquíria**: entidade que abre a história, leva almas para Terragaya; formal-solene. 17 linhas somadas (`VALKIRIE`/`VALKIRIE1`/`VALKIRIE2`). Fonte: SRC-002/003/004 + SRC-001.
- **Arkzel**: feiticeiro/conselheiro do rei, antagonista revelado tarde. Fonte: SRC-002/004 (sem speaker code confirmado no corpus do piloto ainda).
- **Ratatosk**: criatura mitológica nórdica. 6 linhas (speaker `RATATOSK`). Fonte: SRC-002 (mitologia nórdica geral) + SRC-001.

#### Mundo e lore (SRC-002/003/004)
- **Terragaya**: mundo do além. 16 menções textuais. Fonte: SRC-002/003.
- **Zarga**: nação do protagonista. 36 menções textuais. Fonte: SRC-002/003.
- **Hafin City / Hafin**: capital de Terragaya. 43 menções textuais. Fonte: SRC-002/003.
- **Ascil**: continente de origem. Fonte: SRC-002/003 (0 menção textual direta confirmada no corpus do piloto — verificar grafia ao escalar).
- **Dadelm**: exército inimigo. 4 menções textuais. Fonte: SRC-002/003.
- **Fyr Forest**: floresta com missões de tempo. Fonte: tone_analysis.md (0 menção textual direta confirmada — pode estar só em tag `<color=LOC>`).

#### Termos de sistema (SRC-001, corpus)
- **Scout/Archer/Caster**: classes do protagonista. Fase 3 (texts_GUI/texts_MENU) ainda pendente — já registrado em `kb_phase_worklist.md`.

---

### Gaps de pesquisa — NPCs com fala relevante SEM cobertura em nenhuma fonte

> Descoberto ao contar linhas por `speaker` no `dialogs.csv` real durante esta reconstrução
> (2026-07-02) — **nenhuma das fontes SRC-002 a SRC-005 cobre estes nomes**. Alguns têm MAIS
> linhas que personagens já pesquisados (ex.: Liandris 80 linhas > Sirfiel 56). Marcados
> `UNSOURCED` em `entities.csv`. Não inventados — apenas contados.

| Speaker | Linhas | Nota |
|---|---|---|
| LIANDRIS | 80 | mais linhas que Sirfiel/Beigon/Edil — provável personagem relevante |
| ADAMONT | 70 | — |
| GALATH | 43 | — |
| CROMACHIEF | 53 | nome sugere chefe da facção "Croma" (ver CROMAMINION) |
| FISHCHIEF | 53 | nome sugere chefe de facção aquática (ver FISHMINION) |
| SANGRIGOR | 37 | — |
| SINKA | 34 | também nome de cena (SINKA_AC_INTRO) |
| BIRK | 24 | — |
| FREYDIN | 21 | — |
| FINSE | 19 | também nome de cena (AC_FINSE_HOUSE_DOOR) |
| SKRIBLES | 18 | — |
| DARKSWORD | 17 | provável boss |
| ANUBIS | 14 | referência mitológica egípcia — consistente com o tom nórdico+egípcio do jogo |
| DARKWARRIOR, IRONCLAD, ESFINGE | 4/2/2 | baixo volume; ESFINGE já é PT/ES p/ Sphinx — pode vir pré-localizado |

**Decisão 2026-07-02 (ratificação humana):** seguir verbatim com estes 22 nomes e escalar a
tradução agora — nomes próprios não são traduzíveis de qualquer forma, risco baixo mesmo sem lore
confirmada. Não retentar a Fandom Wiki nesta rodada. Todos os 22 adicionados ao `glossary.csv`
como `handling_rule: verbatim` com nota UNSOURCED. QA humano deve prestar atenção extra às linhas
desses personagens (falta contexto de personalidade/registro que a pesquisa externa daria).

---

### Decisões resolvidas (2026-07-02 — ratificação humana)

1. **Grafia Makarel vs Makerel** ✓ — ratificado pelo usuário: **"Makarel"** é a grafia canônica
   (pesquisa externa/wiki); "MAKEREL" no corpus fica só como ID interno do dev, não a grafia de
   exibição. Atualizado em `entities.csv` (confidence medium→high).
2. **9 NPCs com >15 linhas sem nenhuma fonte** ✓ — ratificado: seguir verbatim, não bloquear a
   escala (ver decisão acima). Atualizado em `glossary.csv` (19 novas entradas verbatim) e
   `entities.csv` (nota de decisão em cada linha UNSOURCED).
3. **Arkzel sem speaker code confirmado** ✓ — investigado: Arkzel **nunca fala diretamente** no
   corpus extraído até agora — é personagem ausente/referenciado (não é falha de extração).
   Evidência real: `STR_DIALOGS_BRIGARD_AC_TOPIC_ARKZEL_1_1` ("Arkzel's whereabouts are still
   unknown..."), `STR_DIALOGS_SIRFIEL_PRESENTATION_1_1` ("Arkzel would be amazed..." — par de
   estudos de Sirfiel), `STR_INGAME_NOTE_BRIGARD_DIARY` (Brigard suspeita que Arkzel foi corrompido
   por um parasita após um terremoto). Grafia "Arkzel" confirmada e consistente em toda menção —
   sem ambiguidade. Promovido de `secondary/medium` para `main/high` em `entities.csv` — é peça
   central do reveal tardio, não coadjuvante. As 2 linhas `AC_TOPIC_ARKZEL_*` têm `speaker` vazio
   no `dialogs.csv` (formato de verbete/codex, não bate o regex `_D\d+_` de fala — não bloqueia,
   `handling_rule` já é verbatim).

### Decisões pendentes

Nenhuma — todas as 3 decisões desta rodada resolvidas em 2026-07-02.

---

### Human input

human_input: confirmed

> 2026-07-02: usuário ratificou as 2 decisões acima interativamente (grafia Makarel; seguir
> verbatim nos 22 NPCs sem fonte e escalar agora). A reconstrução inicial deste arquivo
> (mesma data) tinha sido feita sem contribuição humana nova — corrigido nesta atualização.
