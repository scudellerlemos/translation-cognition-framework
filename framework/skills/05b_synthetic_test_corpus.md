# SKILL 05b — SYNTHETIC TEST CORPUS
## Corpus de teste sintético para pontos críticos

> **Quando usar:** No final do passo 5, antes de traduzir qualquer segmento que contenha personas de identidade dupla, personagens de voz crítica, ou outros pontos sensíveis. Também ao início do projeto para calibrar a voz do protagonista/narrador.

---

## OBJETIVO

Testar a capacidade de manter vozes distintas e tratar spoilers corretamente **antes** de entrar no corpus real. Um erro no corpus sintético custa zero — o mesmo erro em centenas de linhas de corpus real custa revisão completa.

---

## COMO GERAR AS SUITES (regra de geração)

As suites **não são fixas** — são derivadas dos artefatos do projeto. Gerar uma suite para cada um destes gatilhos:

| Gatilho | Fonte | Suite a gerar |
|---------|-------|---------------|
| Protagonista / narrador | `tone_analysis.md` | 1 suite de **calibração** da voz base |
| Cada par de identidade dupla | `aliases_map.json` (aliases major/critical) | 1 suite de **distinção** (persona pública vs. revelada) |
| Cada personagem `voice_criticality: high` | `tone_analysis.md` | 1 suite de **voz** dedicada |
| Cada entidade-monstro/ameaça com reveal | `entities.csv` + `aliases_map.json` | 1 suite **pré-reveal** (sem vazar a natureza revelada) |
| Cada momento de reveal | `aliases_map.json → reveal_timing` | 1 suite de **impacto de reveal** |

> Exemplo concreto de suites geradas para um título real: ver
> `projects/<título>/profile/example_test_suites.md` (referenciado em
> `project.json → profile.example_test_suites`).

---

## QUANDO EXECUTAR CADA SUITE

| Gatilho de execução | Suite |
|---------------------|-------|
| Início do projeto | Calibração da voz do protagonista/narrador |
| Antes dos primeiros segmentos de uma persona de identidade dupla | Suite de distinção daquele par |
| Antes dos primeiros segmentos de um personagem de voz crítica | Suite de voz daquele personagem |
| Antes de qualquer segmento que nomeie uma entidade-ameaça pré-reveal | Suite pré-reveal |
| Antes dos segmentos de qualquer reveal | Suite de impacto de reveal |

---

## ESTRUTURA DO ARQUIVO

`synthetic_test_corpus.json`

```json
{
  "test_suites": [
    {
      "suite_id": "SUITE-[NOME]",
      "purpose": "[o que a suite valida]",
      "execute_before": "[gatilho de execução]",
      "cases": [...]
    }
  ]
}
```

Cada caso de teste:

```json
{
  "id": "TEST-001",
  "suite": "SUITE-[NOME]",
  "purpose": "[o que o caso verifica]",
  "speaker": "[personagem]",
  "context": "[situação]",
  "text_en": "[linha sintética no idioma-fonte]",
  "expected_register": "[registro esperado]",
  "expected_characteristics": ["...", "..."],
  "red_flags": ["...", "..."],
  "pass_criteria": "[o que define aprovação]",
  "fail_criteria": "[o que define falha]"
}
```

Os `expected_characteristics` e `red_flags` de cada personagem vêm diretamente do perfil de voz
correspondente no `tone_analysis.md`.

---

## TIPOS DE SUITE (padrões de geração)

### Suite de calibração (protagonista/narrador)
Casos que cobrem: reação ao inesperado, desconforto físico, competência sem drama, humor no registro próprio do personagem. Testa a voz base que permeia todo o corpus.

### Suite de distinção (par de identidade dupla)
Casos que contrastam a persona pública e a identidade revelada. Incluir linhas de **ambas** as personas.
**Critério da suite:** as duas devem soar como pessoas diferentes, mas reconhecíveis como a mesma em retrospecto.
**Critério crítico (anti-ironia):** reler as linhas da persona pública e perguntar — "isso soaria irônico se o leitor já soubesse a identidade revelada?" Se sim → revisar.

### Suite de voz (personagem de voz crítica)
Casos que estressam os red flags específicos do personagem (do `tone_analysis.md`).

### Suite pré-reveal (entidade-ameaça)
Casos que descrevem a entidade sem vazar sua natureza revelada (ex: sem pathos para um monstro cuja humanidade só é revelada depois).

### Suite de impacto de reveal
Casos do momento exato da revelação — devem ter peso sem melodrama.

---

## PROCESSO DE EXECUÇÃO

1. Traduzir todos os casos da suite relevante
2. Revisar cada tradução contra os `red_flags` e `pass_criteria`
3. Se algum caso falhar: identificar a causa raiz antes de continuar
   - Causa raiz no prompt? → ajustar instrução de voz para o passo 6
   - Causa raiz na regra? → atualizar `translation_rules.md` + registrar no `decision_log.md`
   - Causa raiz pontual? → corrigir o caso e verificar se o padrão não se repete
4. Só avançar para o corpus real após aprovação completa da suite

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `synthetic_test_corpus.json` | Todos os casos de teste por suite |
| `synthetic_test_results.json` | Resultados de cada execução: passed / failed + notas |

### Estrutura do `synthetic_test_results.json`

```json
{
  "execution_date": "YYYY-MM-DD",
  "suite": "SUITE-[NOME]",
  "results": [
    {
      "id": "TEST-001",
      "status": "passed",
      "translation_produced": "[tradução]",
      "notes": "[observação]"
    },
    {
      "id": "TEST-002",
      "status": "failed",
      "translation_produced": "[tradução]",
      "failure_reason": "[por que falhou]",
      "suggested_fix": "[correção sugerida]",
      "notes": "[observação]"
    }
  ],
  "suite_approved": false,
  "blocking_issues": 1,
  "action_required": "[o que corrigir e re-executar]"
}
```

---

## CRITÉRIO DE APROVAÇÃO DAS SUITES

| Condição | Resultado |
|---------|----------|
| 0 casos com `status: failed` | Suite aprovada — avançar |
| 1+ casos `failed` com `suggested_fix` aceito e re-testado | Suite aprovada condicionalmente — documentar no decision_log |
| 1+ casos `failed` por causa raiz sistêmica (instrução de prompt) | **Suite bloqueada** — toda a suite reprovada |
| 1+ casos `failed` sem fix identificado | **Suite bloqueada** — escalar para revisão humana |

**Mínimo de 3 casos por suite** — menos que isso não tem cobertura suficiente para validar a distinção.

---

## REGRAS CRÍTICAS

- **Nenhum segmento real de persona de identidade dupla deve ser traduzido antes da suite correspondente ser aprovada.** Inegociável.
- Aprovação da suite não é automática — cada caso revisado explicitamente.
- Casos que falham por causa raiz sistêmica bloqueiam **toda a suite**, não só o caso individual.
- Os resultados alimentam o `decision_log.md` quando revelam necessidade de ajuste de regra.
- Re-execução após ajuste de regra: re-testar **todos** os casos, não só os que falharam — uma correção pode quebrar casos que passavam.
