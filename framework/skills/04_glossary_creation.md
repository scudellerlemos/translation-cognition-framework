# SKILL 04 — GLOSSARY CREATION
## Criar o glossário de localização e as regras de tradução

> **Quando usar:** Após o KNOWLEDGE BUILDING. Produz os dois documentos normativos que governam toda a execução da tradução.

---

## OBJETIVO

Definir de forma definitiva como cada termo deve ser tratado na tradução, e documentar o raciocínio por trás de cada decisão. O glossário é a fonte de verdade operacional; as regras explicam o porquê.

---

## INPUTS

- `entities.csv`
- `universe_knowledge_base.md`
- `research_log.md`
- `tone_analysis.md`
- `aliases_map.json`
- `project.json` (para `source_language` / `target_language`)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `entities.csv` | Existe; campos obrigatórios presentes; nenhum `canonical_name` vazio |
| `universe_knowledge_base.md` | Existe; critérios de completude do Passo 3 atendidos |
| `research_log.md` | Existe; campo `status: reconciled` presente |
| `tone_analysis.md` | Existe |
| `aliases_map.json` | Existe |

❌ **Se qualquer verificação falhar: PARAR. Resolver o passo anterior antes de continuar.**

---

## GLOSSARY.CSV — ESTRUTURA

Colunas obrigatórias:

| Coluna | Descrição |
|--------|-----------|
| `term` | Termo no idioma-fonte |
| `category` | Categoria da entidade |
| `target_translation` | Forma final no idioma-alvo (`project.json → target_language`) |
| `handling_rule` | `verbatim` / `translate` / `translate_partial` |
| `spoiler_level` | none / moderate / major / critical |
| `aliases` | Aliases do termo (separados por `;`) |
| `notes` | Instruções específicas de uso |

> **ATENÇÃO — valores do runtime:** o CSV deve usar os valores em inglês exibidos acima
> (`verbatim`, `translate`, `translate_partial`). Esses são os valores que
> `context_pack.select_glossary()` e `state_index` leem. Usar os equivalentes em português
> (`manter_original`, `traduzir`) produz `glossary_subset: 0` silenciosamente.
> Rodar `python framework/runtime/state_index.py <projeto>` — se retornar aviso de coluna
> faltando ou glossary=0 em cena que deveria ter hits, é sinal de schema errado.

### Regras de handling_rule

**`verbatim`** — usar exatamente o termo no idioma-fonte (ou romanização). Aplica-se tipicamente a:
- Nomes de personagens
- Locais inventados
- Títulos culturais
- Termos de lore inventados pelo universo
- Alimentos e criaturas inventados
- Mecânicas com nome próprio
- Moeda inventada

**`translate`** — usar a tradução no idioma-alvo. Aplica-se tipicamente a:
- UI (menus, modos, prompts)
- Títulos políticos/militares descritivos
- Facções com nome descritivo
- Elementos descritivos genéricos de locais (Inn, River, Province)

**`translate_partial`** — manter o nome próprio, traduzir o elemento descritivo:
- `[NomePróprio] Inn` → `Estalagem [NomePróprio]`
- `[NomePróprio] River` → `Rio [NomePróprio]`

> A decisão de qual termo cai em qual regra é **específica do projeto** e deve ser registrada
> no `glossary.csv`. Sementes/exemplos do título de referência: ver os arquivos de perfil do
> projeto (`project.json → profile.terminology_seeds`).

---

## TRANSLATION_RULES.MD — ESTRUTURA

O documento deve cobrir obrigatoriamente (omitir seções não-aplicáveis à obra, justificando):

1. **Nomes Próprios de Personagens** — regra geral + justificativa
2. **Identidades Duplas e Spoilers** — os pares de identidade, regras de separação, diferenças de voz por par, checklist de verificação
3. **Títulos e Honoríficos** — culturais (manter) vs. políticos (traduzir)
4. **Termos de Lore** — princípio geral + lista
5. **Alimentos e Culinária** — quando são nomes próprios + casos especiais
6. **Criaturas e Montarias** — regra geral + casos especiais
7. **Locais e Nações** — manter vs. traduzir + elementos descritivos
8. **Facções e Grupos** — tabela completa
9. **Mecânicas e UI** — UI traduz, mecânicas com nome próprio mantêm
10. **Registro de Voz por Personagem** — perfil completo de cada personagem principal (de `tone_analysis.md`)
11. **Tratamento de Comédia** — tipos de comédia e suas regras específicas
12. **Gestão de Spoilers** — classificação + regras práticas por nível + cenas de armadilha
13. **Consistência entre Ocorrências** — processo de verificação + termos obrigatórios (formas exatas)

---

## TONE_ANALYSIS.MD — FORMATO DE VOICE CARDS (obrigatório para runtime)

O `tone_analysis.md` é lido por `state_index.build_voice_cards()`. Para gerar voice cards
utilizáveis pelo `context_pack`, **cada personagem relevante deve ter uma seção `###`** com
o marcador `voice_criticality:` inline. Sem esse marcador, o state_index retorna 0 cards.

### Formato obrigatório

```markdown
### NomePersonagem — `voice_criticality: high|medium|low`
- **Registro:** (breve descrição do registro)
- **Características:** (traços de voz mais marcantes)
- **Red flags:** (erros típicos a evitar)
```

### Aliases (nomes alternativos / formas em múltiplos idiomas)

Usar `/` entre os nomes no cabeçalho:

```markdown
### Valkirie/Valkyrie/Valquíria — `voice_criticality: medium`
```

O parser extrai todos os nomes separados por `/` como aliases. Isso é necessário quando
o nome no corpus-fonte (EN) difere do nome no target (PT) — sem alias, `_present()` não
encontra o personagem no texto-fonte e o card não aparece na cena.

### Scaffold

Rodar `python framework/runtime/scaffold_project.py <projeto>` gera o template com as
seções `###` e o marcador `voice_criticality` no lugar certo.

---

## DECISION LOG — ESTRUTURA

Ver `04b_decision_log.md` para o protocolo completo. O `decision_log.md` começa vazio neste passo e é preenchido ao longo de todo o projeto. É o mecanismo de auditoria do processo.

---

## VERIFICAÇÃO DE COBERTURA DO GLOSSÁRIO

Após criar o `glossary.csv`, executar esta verificação antes de avançar:

### 1. Cobertura de entidades (entities.csv → glossary.csv)
- Cada `canonical_name` do `entities.csv` com `importance: main` ou `secondary` tem entrada no `glossary.csv`
- Entidades `importance: background` (UI): verificar presença, mas não bloquear se ausentes
- Gerar lista de lacunas: entidades sem entrada no glossário

### 2. Integridade de regras

| Verificação | Critério de bloqueio |
|------------|---------------------|
| Entradas com `handling_rule` vazio | 0 — bloquear se > 0 |
| Entradas com `target_translation` vazio onde `handling_rule: traduzir` | 0 — bloquear se > 0 |
| Entidades `importance: main` sem entrada no glossário | 0 — bloquear se > 0 |

### 3. Resultado esperado antes de avançar
- 100% das entidades main/secondary têm entrada no glossário
- 0% de entradas com `handling_rule` vazio
- 0% de entradas com `target_translation` vazio para `handling_rule: traduzir`

---

## ATUALIZAÇÃO DE GLOSSÁRIO MID-PROJECT

Quando uma entrada existente do `glossary.csv` for modificada após o início do Passo 6:

**1. Identificar impacto:**
- Buscar em `approved_translations.csv` todas as ocorrências da forma ANTERIOR do termo
- Listar os IDs de linha afetados

**2. Classificar urgência:**

| Tipo de mudança | Urgência |
|----------------|---------|
| `manter_original` → `traduzir` (ou vice-versa) | Crítica — toda ocorrência anterior está errada |
| Mudança de forma em `target_translation` | Alta — inconsistência entre lotes |
| Adição de nota/instrução sem mudança de forma | Baixa |

**3. Registrar no decision_log.md** com tipo `revision` (razão + impacto + ação).

**4. Agendar correção:** adicionar IDs afetados ao próximo ciclo de correção (Passo 06c).

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `glossary.csv` | Fonte de verdade operacional para todos os termos |
| `translation_rules.md` | Documento normativo completo com justificativas |
| `decision_log.md` | Registro de decisões não-óbvias (inicialmente vazio, preenchido ao longo do projeto) |

---

## REGRAS CRÍTICAS

- Em caso de conflito entre `translation_rules.md` e `glossary.csv`, **o CSV prevalece para a forma final**.
- O `translation_rules.md` explica o raciocínio; o CSV contém a decisão.
- O `decision_log.md` deve ser atualizado sempre que uma decisão nova for tomada — não retroativamente em lote.
- Nenhum termo pode ter `handling_rule` vazio. Toda entrada tem uma regra explícita.
