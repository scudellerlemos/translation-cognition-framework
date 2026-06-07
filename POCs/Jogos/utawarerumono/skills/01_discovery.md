# SKILL 01 — DISCOVERY
## Entender o jogo antes de traduzir

> **Quando usar:** No início do projeto, antes de qualquer tradução. Recebe as strings brutas extraídas do jogo.

---

## OBJETIVO

Transformar strings brutas em conhecimento estruturado do universo do jogo. Nenhuma tradução acontece aqui — só análise.

---

## INPUTS

- Arquivo de strings brutas (dialogs.csv ou equivalente)
- Qualquer material de referência disponível (wiki, manual, etc.)

---

## TAREFAS

### 1. Identificar entidades nomeadas
Varrer todas as strings e extrair:
- Personagens (nomes próprios, títulos, apelidos)
- Locais (países, cidades, regiões, estruturas)
- Facções (grupos políticos, militares, religiosos)
- Itens (armas, artefatos, equipamentos com nome próprio)
- Conceitos de lore (termos inventados pelo universo)
- UI (elementos de interface — menus, tutoriais, etc.)

### 2. Agrupar variações do mesmo nome (aliases)
- Detectar quando o mesmo referente aparece com nomes diferentes
- Anotar nível de spoiler de cada alias (none / moderate / major / critical)
- Nunca resolver aliases publicamente antes do reveal narrativo

### 3. Classificar termos por tipo
- **Lore:** termos inventados que devem ser mantidos no original
- **Técnico/UI:** elementos de interface que devem ser traduzidos
- **Cultural:** títulos e marcadores culturais que devem ser mantidos
- **Descritivo:** elementos genéricos que podem ser traduzidos

### 4. Identificar padrões de linguagem e tom
- Registros presentes: sagrado / formal / marcial / cotidiano / cômico
- Personagens com voz distinta
- Padrões de comédia (subreação, performance, caracterização, ironia dramática)

### 5. Detectar spoilers estruturais
- Identidades duplas (personagem A = personagem B revelado mid/late game)
- Revelações de relação (X é irmão de Y)
- Recontextualizações (entidade A era na verdade B)
- Marcar cada um com nível de spoiler e timing narrativo do reveal

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `entities_candidates.json` | Lista bruta de entidades extraídas com categoria e contexto |
| `aliases_map.json` | Mapa alias → canônico com nível de spoiler e timing do reveal |
| `terminology_clusters.json` | Agrupamento de termos por tipo (lore / técnico / cultural / UI) |
| `tone_analysis.md` | Análise de tom, registros, padrões de comédia, perfis de voz |

---

## REGRAS CRÍTICAS

- **Não traduzir nada neste passo.** Só identificar e classificar.
- Aliases de spoiler maior/crítico devem ser marcados com timing do reveal narrativo.
- Termos de lore devem ser identificados como "manter original" já neste passo.
- O `tone_analysis.md` deve incluir perfil de voz de cada personagem principal — isso alimenta o passo 6.
