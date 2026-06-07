# SKILL 02 — ENTITY RESOLUTION
## Quem é o quê — classificação e unificação de entidades

> **Quando usar:** Após o DISCOVERY. Recebe `entities_candidates.json` e produz o `entities.csv` definitivo.

---

## OBJETIVO

Transformar a lista bruta de entidades candidatas em um registro canônico estruturado, resolvendo ambiguidades, unificando aliases e marcando importância narrativa.

---

## INPUTS

- `entities_candidates.json` (output do DISCOVERY)
- `aliases_map.json` (output do DISCOVERY)
- Material de referência externo (wiki, créditos, manual)

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `entities_candidates.json` | Existe; campo `name` presente em todas as entradas; ≥1 entidade |
| `aliases_map.json` | Existe; campos `alias` e `canonical_name` presentes em todas as entradas |

❌ **Se qualquer verificação falhar: PARAR. Executar o Passo 1 (Discovery) antes de continuar.**

---

## TAREFAS

### 1. Classificar cada entidade
Categorias aceitas:
- `Personagem`
- `Local`
- `Facção`
- `Item`
- `Conceito`
- `Título`
- `Criatura`
- `Alimento`
- `Cultural`
- `Mecânica`
- `UI`

### 2. Resolver ambiguidades
Quando uma entidade pode pertencer a mais de uma categoria:
- Registrar a categoria primária
- Adicionar nota explicando a ambiguidade
- Exemplo: Akuruka é Item (objeto físico) + Conceito (sistema de poder) → classificar como Item com nota conceitual

### 3. Unificar aliases
- Definir o `canonical_name` (forma oficial usada na tradução)
- Listar todos os aliases conhecidos com nível de spoiler
- Para aliases de spoiler maior/crítico: registrar o timing do reveal

### 4. Marcar importância narrativa
- `main` — personagem/entidade central, presente no arco principal
- `secondary` — relevante para arcos secundários ou para o mundo
- `background` — existe no mundo mas não tem arco próprio

### 5. Marcar confiança
- `high` — identificado com certeza por múltiplas ocorrências ou confirmação externa
- `medium` — identificado com razoável certeza
- `low` — candidato fraco, pode ser ruído

---

## OUTPUTS OBRIGATÓRIOS

### `entities.csv`

Colunas obrigatórias:

| Coluna | Descrição |
|--------|-----------|
| `canonical_name` | Nome canônico oficial usado na tradução |
| `category` | Categoria da entidade |
| `aliases` | Lista de aliases com nível de spoiler entre parênteses |
| `importance` | main / secondary / background |
| `confidence` | high / medium / low |
| `notes` | Observações de tradução, ambiguidades, regras específicas |

---

## CRITÉRIOS DE COMPLETUDE DO ENTITIES.CSV

O `entities.csv` está pronto para avançar ao Passo 3/4 quando:

| Critério | Mínimo |
|----------|--------|
| Entidades de `entities_candidates.json` processadas | 100% (resolvidas ou explicitamente descartadas com nota) |
| Entradas com `confidence: low` sem nota explicativa | 0 |
| Ambiguidades sem registro em `notes` | 0 |

**Entidades descartadas** devem ter uma linha com `notes: "descartado — [razão]"`, não podem ser simplesmente omitidas.

---

## REGRAS CRÍTICAS

- O `canonical_name` é a fonte de verdade. Se houver conflito entre este arquivo e qualquer outro, este prevalece na definição da identidade — o `glossary.csv` prevalece na forma final da tradução.
- Aliases de spoiler maior/crítico **nunca** devem ser usados como `canonical_name`.
- Entidades de UI sempre têm `importance: background` — não são narrativas.
- Ambiguidades não resolvidas devem ser registradas em `notes` para revisão humana.
