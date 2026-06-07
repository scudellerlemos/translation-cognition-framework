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
| `term` | Termo no original (inglês ou japonês romanizado) |
| `category` | Categoria da entidade |
| `pt_br_translation` | Forma final em português do Brasil |
| `handling_rule` | `manter_original` / `traduzir` / `traduzir_parcial` |
| `spoiler_level` | none / moderate / major / critical |
| `aliases` | Aliases do termo com nível de spoiler |
| `notes` | Instruções específicas de uso |

### Regras de handling_rule

**`manter_original`** — usar exatamente o termo em inglês/japonês romanizado:
- Todos os nomes de personagens
- Locais inventados
- Títulos culturais (Owlo, Mononofu, Kamunagi)
- Termos de lore (Akuruka, Tatari, Ohn Riyaak)
- Alimentos inventados
- Criaturas inventadas
- Mecânicas de unidade (Rakusharai, Ankuam)
- Moeda (Sen)

**`traduzir`** — usar a tradução em pt-BR:
- UI de jogo (menus, modos de batalha)
- Títulos políticos/militares (Eight Pillar Generals → Oito Generais dos Pilares)
- Facções com nome descritivo (Nosuri's Thieves → Ladrões de Nosuri)
- Elementos descritivos genéricos de locais (Inn, River, Province)

**`traduzir_parcial`** — manter o nome próprio, traduzir o elemento descritivo:
- Hakurokaku Inn → Estalagem Hakurokaku
- Omuchakko River → Rio Omuchakko
- Kamunagi of Chains → Kamunagi das Correntes

---

## TRANSLATION_RULES.MD — ESTRUTURA

O documento deve cobrir obrigatoriamente:

1. **Nomes Próprios de Personagens** — regra geral + justificativa
2. **Identidades Duplas e Spoilers** — os pares de identidade, regras de separação, diferenças de voz por par, checklist de verificação
3. **Títulos e Honoríficos** — culturais (manter) vs. políticos (traduzir)
4. **Termos de Lore** — princípio geral + lista
5. **Alimentos e Culinária** — por que são nomes próprios + casos especiais
6. **Criaturas e Montarias** — regra geral + casos especiais
7. **Locais e Nações** — manter vs. traduzir + elementos descritivos
8. **Facções e Grupos** — tabela completa
9. **Mecânicas de Jogo e UI** — UI traduz, unidades mantêm
10. **Registro de Voz por Personagem** — perfil completo de cada personagem principal
11. **Tratamento de Comédia** — tipos de comédia e suas regras específicas
12. **Gestão de Spoilers** — classificação + regras práticas por nível + cenas de armadilha
13. **Consistência entre Ocorrências** — processo de verificação + termos obrigatórios

---

## DECISION LOG — ESTRUTURA

**Novo arquivo obrigatório a partir desta versão do processo.**

Arquivo: `decision_log.md`

Para cada decisão de localização não-óbvia, registrar:

```markdown
## [Termo]

**Data:** [data]
**Decisão:** [o que foi decidido]
**Alternativas consideradas:** [o que foi rejeitado]
**Razão:** [por que esta decisão e não outra]
**Impacto:** [onde essa decisão afeta o texto]
```

O decision log é o mecanismo de auditoria do processo. Quando uma decisão for questionada futuramente, a razão está documentada.

---

## VERIFICAÇÃO DE COBERTURA DO GLOSSÁRIO

Após criar o `glossary.csv`, executar esta verificação antes de avançar:

### 1. Cobertura de entidades (entities.csv → glossary.csv)

- Verificar que cada `canonical_name` do `entities.csv` com `importance: main` ou `secondary` tem entrada correspondente em `glossary.csv`
- Entidades `importance: background` (UI): verificar presença, mas não bloquear se ausentes
- Gerar lista de lacunas: entidades sem entrada no glossário

### 2. Integridade de regras

| Verificação | Critério de bloqueio |
|------------|---------------------|
| Entradas com `handling_rule` vazio | 0 — bloquear se > 0 |
| Entradas com `pt_br_translation` vazio onde `handling_rule: traduzir` | 0 — bloquear se > 0 |
| Entidades `importance: main` sem entrada no glossário | 0 — bloquear se > 0 |

### 3. Resultado esperado antes de avançar

- 100% das entidades main/secondary têm entrada no glossário
- 0% de entradas com `handling_rule` vazio
- 0% de entradas com `pt_br_translation` vazio para `handling_rule: traduzir`

---

## ATUALIZAÇÃO DE GLOSSÁRIO MID-PROJECT

Quando uma entrada existente do `glossary.csv` for modificada após o início do Passo 6:

**1. Identificar impacto:**
- Buscar em `translated.csv` todas as ocorrências da forma ANTERIOR do termo
- Listar os offsets afetados

**2. Classificar urgência:**

| Tipo de mudança | Urgência |
|----------------|---------|
| `manter_original` → `traduzir` (ou vice-versa) | Crítica — toda ocorrência anterior está errada |
| Mudança de forma em `pt_br_translation` | Alta — inconsistência entre lotes |
| Adição de nota/instrução sem mudança de forma | Baixa |

**3. Registrar no decision_log.md** com tipo `revision`:
```
Tipo: revision
Razão: [por que a regra mudou]
Impacto: [lista de offsets afetados e estimativa de linhas]
Ação: re-QA dos segmentos afetados no próximo ciclo 06c
```

**4. Agendar correção:** adicionar offsets afetados ao próximo ciclo de correção (Passo 06c).

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
