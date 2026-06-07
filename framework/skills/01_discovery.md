# SKILL 01 — DISCOVERY
## Entender a obra antes de traduzir

> **Quando usar:** Após a EXTRAÇÃO (Passo 00) e antes de qualquer tradução. Recebe o corpus-fonte (`dialogs.csv`) produzido pelo conector.

---

## OBJETIVO

Transformar o texto-fonte bruto em conhecimento estruturado do universo da obra. Nenhuma tradução acontece aqui — só análise.

---

## INPUTS

- `project.json` (manifesto do projeto — define fonte, idiomas, formato)
- O corpus-fonte declarado em `project.json → source.file`
- Qualquer material de referência disponível (wiki, manual, etc.)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `project.json` | Existe; campos obrigatórios presentes (ver `framework/schemas/project_schema.md`) |
| Corpus-fonte (`source.file`) | Existe (output do Passo 00); não-vazio; `id_column` único por linha |
| Extração (Passo 00) | Concluída; gate de round-trip passou (quando há `connector`) |

❌ **Se o manifesto ou o corpus não existir: PARAR. O corpus é produzido pelo Passo 00 (extração) — rodar o conector antes.**

> Para detalhes de como o corpus é estruturado por tipo de mídia, ver o media-profile
> indicado em `project.json → media_profile` (ex: `framework/media-profiles/games.md`).

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

## PERFIS DE VOZ — `tone_analysis.md`

O `tone_analysis.md` deve incluir um perfil de voz por personagem com voz distinta. Cada perfil:

- **`voice_criticality`:** high / medium / low — quão sensível é a voz do personagem
- **Registro:** o tom base
- **Características:** traços que definem a voz
- **Red flags:** o que sinaliza que a voz saiu do personagem

Personagens `voice_criticality: high` recebem auto-revisão em **cada linha** no Passo 6 e
verificação dedicada no Micro-QA (Passo 6b). Este campo é o gancho que torna a verificação de
voz genérica — as skills posteriores leem o perfil, não nomes hardcoded.

> Exemplo de perfis preenchidos: `projects/utawarerumono/profile/voice_profiles_reference.md`.

---

## REGRAS CRÍTICAS

- **Não traduzir nada neste passo.** Só identificar e classificar.
- Aliases de spoiler maior/crítico devem ser marcados com timing do reveal narrativo.
- Termos de lore devem ser identificados como "manter original" já neste passo.
- O `tone_analysis.md` deve incluir perfil de voz de cada personagem principal — isso alimenta o passo 6.
