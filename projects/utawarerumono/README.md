# Projeto: Utawarerumono: Mask of Deception
## Primeira instância de referência do framework SDD

Este é o projeto de localização que originou o framework. Serve como **referência viva**: prova de que o processo genérico em `/framework/` funciona em um título real, e exemplo de como preencher uma instância nova.

---

## Estado: **JOGO COMPLETO** — 16 capítulos traduzidos e verificados ✅

O projeto evoluiu de "valida em 2 cenas" para **a obra inteira traduzida pelo harness stateless**
(`framework/runtime/`). Cada cena roda como um **job isolado** (contexto O(cena)) via API headless; o
chat só lança o driver de capítulo e lê o resumo. **Os 16 capítulos** (toda a história do jogo) estão
**traduzidos e verificados ponta-a-ponta** — round-trip byte-idêntico (resíduo 0) + back-translation de
alto risco — **146 cenas, ~45.100 linhas**:

| Capítulo | Cenas | Status |
|---|---|---|
| **11** | 11 | ✅ verificado |
| **12** | 16 | ✅ verificado |
| **13** | 9 | ✅ verificado (Batch API −50%) |
| **14** | 9 | ✅ verificado |
| **15** | 9 | ✅ verificado |
| **16** | 5 | ✅ verificado |
| **17** | 5 | ✅ verificado |
| **18** | 5 | ✅ verificado |
| **19** | 8 | ✅ verificado |
| **20** | 19 | ✅ verificado |
| **21** | 7 | ✅ verificado |
| **22** | 7 | ✅ verificado (reveal sci-fi do final) |
| **23** | 19 | ✅ verificado |
| **30** | 11 | ✅ verificado |
| **31** | 2 | ✅ verificado |
| **39** | 4 | ✅ verificado (DLC/pós-jogo) |

Gasto real acumulado: **~$65,9** (Sonnet $50,6 · Opus $7,8 · Haiku $7,5), **$0 desperdiçado** (medido
pelo `api_ledger.jsonl`). Alavancas comprovadas/codadas no caminho de escala: **Sonnet aprovado** por
benchmark (nível Opus-à-mão); **Batch −50%** vivo; **tiering** Haiku/Sonnet/Opus por complexidade;
**dedup por TM**; **recuperação por-linha** (defeito de 1 linha re-traduz ~1 linha, não a cena);
**estimativa pré-voo + teto duro** (gasto de pior-caso conhecido antes de pagar — ver
[README → Engenharia de custo](../../README.md#engenharia-de-custo-e-previsibilidade)); **back-translation
em batch**; **controle de spoiler/gênero** por ledger temporal (reveal Ukon=Oshtor em `ch_13_08`);
**gate de fonte de KB** (`kb_review.py` + `kb_phase.py`); **revisão humana via XLSX** com **TM como
coração** (o jogo não é re-traduzido inteiro após o QA). Governança com desenhos:
[`../../framework/docs/GOVERNANCE.md`](../../framework/docs/GOVERNANCE.md).

### Marco anterior — validação in-game do conector ✅ (1025 linhas, cap. 11_01/02)

Antes da escala, o pipeline 00→08 foi provado no jogo real (Steam): o pt-BR **renderiza corretamente
in-game**. Esse marco destravou tudo o que veio depois.

| Etapa | Resultado |
|-------|-----------|
| **Passo 00 — extração** | `extract.py` extrai **por arco** usando `sdat_format.py` → `artifacts/dialogs.csv` (com `byte_budget`). Container `.sdat` mapeado (header `Filename`/`Pack`, 353 scripts) |
| **Gate de round-trip** | ✅ byte-a-byte — travado por `connector/test_roundtrip.py` (pytest, **16 testes**) |
| **Gate de charset** | ❌ `false` (acentos viram `@` in-game) → **transliteração na gravação**; tradução canônica mantém acentos |
| **Passo 08 — reinserção** | `reinsert.py` → `output/ScriptEvent.sdat` + `.ips`. **Resíduo T4=0**; **ponteiros relocados resolvem dentro do arquivo** |
| **Gate in-game** | ✅ **validado** — pt-BR exibe (`artifacts/evidence/Fasea*.png`); linha relocada pelo Plano B exibe e o jogo avança (`artifacts/evidence/testeplanob*.png`) |

**Aprendizados** em [`artifacts/decision_log.md`](artifacts/decision_log.md) e [`artifacts/extraction_log.md`](artifacts/extraction_log.md).
Destaques: **modelo de ponteiro é FILE-RELATIVO** (não absoluto — correção crítica); **EOF-append
reprovado in-game** → `space_strategy` = **in_place + relocação INTRA-ARQUIVO**; tradução aplicada por
**arquivo aprovado** + script (a IA não edita dados à mão).

**Saída final:** [`output/ScriptEvent.sdat`](output/) + patch `.ips` — mesmo nome/extensão do input, pronto para repatch.

> **Governança de scripts:** os scripts do conector (`extract.py`, `reinsert.py`, `sdat_format.py`,
> `charset_check.py`, `poc_pipeline.py`) são determinísticos e **executados** — não refeitos pela IA, e
> **nunca contêm texto da obra** (um teste genérico falha se houver frase hardcoded em `.py`). Criar
> script novo só com permissão; uma vez existindo, apenas rodar.

---

## Configuração

Toda a config deste título vive em [`project.json`](project.json):

- **Mídia:** jogo (visual novel) — usa o perfil `games`
- **Idiomas:** EN → pt-BR
- **Fonte:** `artifacts/dialogs.csv` (formato CSV com offset hex)
- **Tokens de engine:** `{W75}`, `{W80}`, `{W10}`, `{COLOR}`, `{END}`
- **Convenção de sistema:** linhas em CAPS = texto de sistema
- **Lote:** 200 linhas

---

## Dados curados (`profile/`)

| Arquivo | Conteúdo | Equivalente no pipeline |
|---------|----------|-------------------------|
| [`voice_profiles_reference.md`](profile/voice_profiles_reference.md) | Perfis de voz dos personagens + `voice_criticality` | `tone_analysis.md` (Passo 1) |
| [`identity_pairs_reference.md`](profile/identity_pairs_reference.md) | Pares de identidade dupla + regras de separação | `aliases_map.json` / `entities.csv` (Passos 1–2) |
| [`terminology_seeds.md`](profile/terminology_seeds.md) | Decisões terminológicas + formas exatas + fases narrativas | `glossary.csv` (Passo 4) |
| [`example_test_suites.md`](profile/example_test_suites.md) | Suites de teste sintético concretas | `synthetic_test_corpus.json` (Passo 5b) |

> Estes arquivos são **referência/exemplo**. No pipeline real, o conteúdo equivalente
> é produzido como artefato gerado. Eles registram o conhecimento deste título e
> servem de modelo de preenchimento para projetos novos.

---

## Artefatos gerados (`artifacts/`)

Onde os outputs do pipeline vivem: `dialogs.csv` (output do Passo 00, depois imutável), `entities.csv`,
`entities_candidates.json`, `aliases_map.json`, `tone_analysis.md`, `glossary.csv`, `research_log.md`,
`universe_knowledge_base.md`, `translation_plan.json` (proposta), `approved_translations.csv` (aprovado —
fonte de verdade da tradução aplicada), `translation_status.json`, `micro_qa_log.json`, `qa_report.md`,
`reinsertion_report.md`, e a saída em `output/` (Passo 08). Ver `framework/schemas/artifacts_schema.md`.

> A tradução **não** é escrita à mão pela IA dentro dos dados: ela propõe em `translation_plan.json`,
> o usuário aprova em `approved_translations.csv`, e o script aplica. (`translated.csv` foi depreciado.)

---

## Conector (`connector/`)

Jogo antigo: o texto vive num binário e é extraído/reinserido por código determinístico
(conector `hex_binary`). Ver [`connector/README.md`](connector/README.md). Estado: **formato do
`ScriptEvent.sdat` totalmente mapeado** (header `Filename`/`Pack`, 353 scripts contíguos alinhados a
16 bytes; ponteiros `50 00` **file-relativos**); `extract.py`/`reinsert.py` escritos e compartilhando
`sdat_format.py`. Encaixe: **in_place + relocação intra-arquivo** (run que estoura é anexado ao fim da
região do próprio arquivo, com a tabela Pack reescrita por `rebuild_container` — o EOF-append foi
reprovado in-game). Round-trip, within-file e integridade do Pack travados por
`connector/test_roundtrip.py` (pytest, 16 testes). A entrega final é um patch IPS.

Rodar: `python connector/extract.py <bin>` → `python connector/reinsert.py <bin>` → `pytest connector/`.

---

## Como rodar

O processo é definido em [`/framework/skills/`](../../framework/skills/_index.md).
Executar as skills na ordem do pipeline (00 → 08), cada uma lendo `project.json` +
os artefatos do passo anterior. Os Input Gates de cada skill bloqueiam execução fora de ordem.
O Passo 00 (extração) só avança se o gate de round-trip passar.

---

## Características críticas deste título

- **Múltiplos pares de identidade dupla** com spoilers críticos (Ukon/Oshtor, Sakon/Mikazuchi, Mito/Mikado)
- **Gestão de spoiler** rigorosa: nomes revelados nunca aparecem antes do `reveal_timing`
- **Comédia com timing** sensível (Haku, Nosuri)
- **Corpus extenso** (~45.100 linhas traduzidas, 16 capítulos)
- **Glifos especiais do charset** (dígitos circulados ①②③ em sequências de puzzle) — preservados pela
  transliteração NFD do conector (ver `connector/README.md`)
