# SKILL 03 — KNOWLEDGE BUILDING
## Pesquisar o universo e construir a base de conhecimento de localização

> **Quando usar:** Após o ENTITY RESOLUTION. Este passo tem duas fases: primeiro pesquisa ativa (IA + humano em paralelo), depois síntese do conhecimento. Nenhuma tradução acontece aqui.

---

## OBJETIVO

Construir um mapa estrutural do domínio narrativo baseado em fontes verificadas. O processo é colaborativo: a IA conduz sua própria pesquisa, o humano conduz a dele, e os dois conjuntos são reconciliados antes da síntese. O resultado alimenta diretamente o glossário e as regras de tradução.

---

## ⬛ INPUT GATE — VERIFICAR ANTES DE INICIAR

| Artefato | Critério |
|----------|---------|
| `entities_candidates.json` | Existe (Passo 1 concluído) |
| `entities.csv` | Existe (Passo 2 concluído) |
| `tone_analysis.md` | Existe (Passo 1 concluído) |

❌ **Se qualquer verificação falhar: PARAR. Executar os passos anteriores antes de continuar.**

---

## FASE 1A — PESQUISA PARALELA

A IA e o humano pesquisam simultaneamente, cada um com suas ferramentas. Documentar todos os achados — mesmo os que parecem óbvios.

---

### IA EXECUTA

#### 1. Mineração do corpus (sempre disponível, sem internet)

Varrer o corpus-fonte (`project.json → source.file`) e `entities_candidates.json` e extrair:

- **Definições in-corpus:** linhas que explicam um termo diretamente (ex: "O [termo de lore] é o poder que...")
- **Auto-apresentações:** padrões do tipo "Eu sou X, o Y de Z", "Meu nome é X, General dos..."
- **Termos de alta frequência sem contexto:** nomes próprios que aparecem muitas vezes mas nunca são explicados no texto → candidatos prioritários para busca externa
- **Referências a lore implícito:** personagens que reagem como se o leitor já soubesse algo (contexto pressuposto)

Anotar cada achado com o ID da linha (`id_column`) de origem para citação posterior.

#### 2. Web search (se ferramentas de busca disponíveis)

Executar buscas estruturadas por categoria:

| Categoria | Buscas sugeridas |
|-----------|-----------------|
| Personagens | `"[Título] characters wiki"`, `"[Nome] [Título] fandom"` |
| Mundo e lore | `"[Título] world lore"`, `"[Título] factions explained"`, `"[Título] worldbuilding"` |
| Precedentes de localização | `"[Título] [idioma-alvo] localization"`, `"[Título] official translation notes"` |
| Material oficial | `"[Título] official guide"`, `"[Dev/Publisher] [Título] lore"` |
| Versões em outros idiomas | `"[Título] [outro idioma] translation"` — referência para decisões terminológicas |

`[Título]`, `[idioma-alvo]` etc. resolvem a partir do `project.json`.

Para cada fonte encontrada:
- Atribuir tier (ver tabela de tiering abaixo)
- Anotar cobertura de spoiler (até qual ponto da história a fonte vai)
- Documentar no `research_log.md` provisório

#### 3. Gestão de spoilers durante a busca

🚨 **Crítico:** wikis contêm spoilers de late-game. Definir antes de ler qualquer fonte:

1. **Definir fronteira:** até qual capítulo / segmento o corpus atual chega?
2. **Ler apenas até essa fronteira** — não avançar para seções que revelam plot posterior
3. **Documentar seções ignoradas** no `research_log.md` para referência futura

> Exemplo: para uma obra cujo corpus vai até o Cap. 5, ler apenas as seções da wiki que cobrem
> até esse ponto. Não ler "Identidades reveladas", "Final", ou qualquer seção de arco posterior.

---

### HUMANO EXECUTA (em paralelo)

Mesmas categorias, com acesso a fontes que o agente pode não conseguir:
- Contas em fandom (conteúdo behind-the-wall)
- Discord de comunidades de fãs
- Guias físicos, artbooks, material de imprensa
- Versões localizadas em outros idiomas (físico ou digital)
- Entrevistas com desenvolvedores/autores em fontes fechadas

Documentar achados no mesmo formato: fonte, tier, cobertura de spoiler, URL/caminho.

---

### TIERING DE FONTES

| Tier | Tipo | Exemplos | Como usar |
|------|------|----------|-----------|
| 1 — Canônico | Primeira mão, definitivo | Corpus-fonte da obra, guia oficial, site do dev/estúdio, artbook oficial | Usar diretamente; conflitos resolvem em favor do Tier 1 |
| 2 — Verificado | Comunitário com evidências | Wiki de fandom bem mantida com citações, tradução oficial em outro idioma, FAQ detalhado | Usar com verificação cruzada; preferir quando corroborado por múltiplas entradas |
| 3 — Especulativo | Sem evidências sólidas | Teorias de fã, wikis sem citação, postagens de fórum isoladas | Usar apenas para preencher gaps — marcar como `confidence: low` |

---

## FASE 1B — RECONCILIAÇÃO

Após ambos (IA e humano) concluírem a pesquisa, comparar os conjuntos:

### 1. Concordâncias
Mesmas fontes encontradas por ambos → Tier confirmado, confiança aumentada.

### 2. Fontes exclusivas do humano
Avaliar e adicionar ao log. Se Tier 1 ou 2: incorporar. Se Tier 3: verificar se a IA também encontrou algo parecido.

### 3. Fontes exclusivas da IA
Humano valida: a fonte é confiável? O conteúdo está correto?

### 4. Divergências de conteúdo
Quando IA e humano encontraram informação conflitante sobre o mesmo termo:

| Critério de resolução | Ordem |
|----------------------|-------|
| Tier mais alto prevalece | 1º |
| Fonte mais recente prevalece (quando mesmo tier) | 2º |
| Múltiplas corroborações prevalecem | 3º |
| Humano decide quando critérios empatam | 4º |

Documentar cada conflito resolvido no `research_log.md`.

### 5. Gaps compartilhados
Termos sem cobertura em nenhuma fonte por nenhum dos dois → marcar como UNSOURCED na Fase 2. Não inventar.

### Output da reconciliação
`research_log.md` com campo `status: reconciled`.

---

## 🔴 GATE PÓS-PESQUISA

| Resultado da pesquisa | Decisão |
|----------------------|---------|
| ≥1 fonte Tier 1 ou 2 no `research_log.md` com `status: reconciled` | ✅ Avançar para Fase 2 |
| Apenas fontes Tier 3 | ⚠️ AVISO — prosseguir com `confidence: low` em todas as entradas; registrar no decision_log |
| Nenhuma fonte encontrada (Tier 1, 2 ou 3) | ❌ BLOQUEADO — não inferir. Perguntar ao humano se há material adicional |

**Se bloqueado, perguntar:**

> "A pesquisa não encontrou fontes verificáveis para este projeto. Você tem material adicional?"
>
> - arquivo local (lore.md, artbook digitalizado, guia)
> - URL de wiki ou site
> - outro material externo
>
> ⚠️ Sem fonte Tier 1 ou 2, a base de conhecimento não pode ser construída.

---

## FASE 2 — SÍNTESE

Com o `research_log.md` reconciliado, construir o `universe_knowledge_base.md`.

**Regra fundamental:** só descrever o que está suportado por fonte. Sem evidência → `UNSOURCED`.

### Tarefas

#### 1. Entidades
Para cada entidade do `entities.csv` com `importance: main` ou `secondary`:
- Descrever baseado exclusivamente nas fontes do log
- Citar ID de fonte para cada afirmação

#### 2. Relações
Somente relações explicitamente observadas ou documentadas nas fontes. Nada inferido.

#### 3. Papel narrativo
Derivado das fontes — descritivo, nunca interpretativo.

#### 4. Contexto de uso
Onde e como a entidade aparece. Quais IDs de linha no corpus confirmam.

#### 5. Fases narrativas
Se a obra tem fases tonais distintas (ex: início leve → drama político → guerra → revelação),
documentar a progressão. Isso alimenta a verificação de tom por fase no QA Final (Passo 7).

---

## FORMATO POR ENTIDADE

```md
## [Entidade]

**Definição:**
(baseada em fonte — 1-2 frases)

**Fontes:**
- SRC-001 (Wiki): seção "[nome da seção]"
- SRC-002 (corpus): linha [id]

**Relações:**
- A → B (fonte: SRC-001)

**Papel narrativo:**
(apenas descritivo, não interpretativo)

**Contexto de uso:**
(onde aparece no corpus)

**Status de confiança:**
high / medium / low / UNSOURCED
```

---

## OUTPUTS OBRIGATÓRIOS

| Arquivo | Conteúdo |
|---------|----------|
| `research_log.md` | Fontes avaliadas, conflitos resolvidos, gaps, fronteira de spoiler — com `status: reconciled` |
| `universe_knowledge_base.md` | Uma entrada por entidade relevante, cada afirmação citando ID de fonte; fases narrativas |

---

## ARTEFATO: `research_log.md`

```markdown
# Research Log — [Projeto]

**Status:** reconciled
**Data de reconciliação:** YYYY-MM-DD
**Fronteira de spoiler:** [Capítulo X / segmento Y / pré-reveal de Z]
**Seções ignoradas intencionalmente:** [lista — ex: "Identidades reveladas", "Arco final"]

---

## Fontes Avaliadas

| ID | Fonte | Tipo | Tier | Cobertura de Spoiler | URL/Caminho | Encontrada por | Usada | Notas |
|----|-------|------|------|----------------------|-------------|----------------|-------|-------|
| SRC-001 | [Nome] Fandom Wiki | Wiki | 2 | Caps. 1–10 (parcial) | [URL] | IA + Humano | Sim | Seções de arco final não lidas |
| SRC-002 | corpus-fonte | Corpus | 1 | Corpus completo | local | IA | Sim | Fonte primária |
| SRC-003 | [Guia/FAQ] | Guia | 2 | Caps. 1–15 | [URL] | Humano | Sim | Detalha mecânicas |

---

## Conflitos Resolvidos

| Termo | Versão IA | Versão Humano | Decisão | Razão |
|-------|-----------|---------------|---------|-------|
| [termo] | "[versão A]" | "[versão B]" | Humano | SRC-003 cita guia oficial |

---

## Gaps de Pesquisa

Termos sem cobertura em nenhuma fonte:
- [termo]: [o que se sabe / por que é UNSOURCED]
```

---

## CRITÉRIOS DE COMPLETUDE

O `universe_knowledge_base.md` está pronto para avançar ao Passo 4 quando:

| Critério | Mínimo |
|----------|--------|
| `research_log.md` com `status: reconciled` | Obrigatório |
| Entidades `importance: main` com entrada no KB | 100% |
| Entidades `importance: secondary` com entrada | 80% |
| Entradas UNSOURCED em entidades `importance: main` | 0 exceções |
| Cada afirmação com citação de ID de fonte | ≥1 por entidade high/medium |

**Bloquear prosseguimento se:** `research_log.md` não está reconciliado, ou qualquer entidade `importance: main` está ausente ou UNSOURCED.

**Para entidades `confidence: low`:** documentar que a fonte é Tier 3 ou especulativa. Não omitir — marcar e explicar.

**O KB não é uma wiki completa** — é uma referência de localização. Cobertura das entidades narrativamente relevantes, não exaustividade enciclopédica.
