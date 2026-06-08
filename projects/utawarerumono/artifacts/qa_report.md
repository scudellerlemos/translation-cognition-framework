# QA Report — Utawarerumono: Mask of Deception
## Cenas 11_01 + 11_02 (abertura — 1025 linhas) · pt-BR

**Data:** 2026-06-08
**Veredito:** ✅ APROVADO (0 issues bloqueantes)

## Escopo
- 1025 linhas (4 sub-scripts: `11_01_000S`, `11_01_100C`, `11_01_150S`, `11_02_000S`).
- Pipeline 00→08 executado de ponta a ponta no corpus em escala (≈14× o arco anterior de 75).
- Conteúdo: despertar → fuga na caverna (inseto gigante → Tatari) → resgate por Kuon → cena cômica
  de vestir → revelação do nome **Haku** (de *Utawarerumono*).

## Cobertura por dimensão

| Dimensão | Resultado |
|----------|-----------|
| **Tokens** (`{W..}`) + **`\n`** | OK — preservados (validação determinística `poc_pipeline.py`: 0 erros de token nas 1025). |
| **Convenção de sistema** (CAPS) | OK — falas de "Sistema" em maiúsculas (11_01_000S). |
| **Vozes** | Curadas em 11_01_000S; em escala, voz de narração (Haku 1ª pessoa) e diálogo de Kuon (gentil/firme) preservadas. |
| **Glossário/entidades** | Tatari, aperyu, Utawarerumono, Kuon, Haku, Kujyuri/Shishiri → manter original; rótulos traduzidos. |
| **Spoilers** | Figuras de memória (Mulher/Homem) mantidas genéricas/ambíguas; reveal de Haku tratado no ponto correto (11_02). |
| **Lacunas do source** | Preservadas (ex.: 6 espaços em 0x3937). |

## Aplicação no binário (Passo 08) — modelo de ponteiro FILE-RELATIVO
- **Round-trip self-test:** OK (byte-idêntico na identidade).
- **Distribuição de tier:** T1 in_place = 595 · REPOINT_head = 425 · REPOINT_cont = 5 · **resíduo T4 = 0**
  (sem nenhum ajuste in_place forçado).
- **Charset:** transliteração na gravação (fonte sem diacríticos).
- **Saída:** `output/ScriptEvent.sdat` + `output/ScriptEvent.sdat.ips`.

## Achados de engenharia (a escala + a investigação revelaram dois problemas — corrigidos)
1. **Runs longos:** `MAX_RUN=32` truncava runs de narração (127 resíduos). Corrigido: run completo +
   head-finding pelo binário + índice de ponteiros (tempo ~80s → ~0.5s).
2. **Modelo de ponteiro errado (crítico):** os `50 00`+uint32 são **RELATIVOS ao início do arquivo**,
   não absolutos (42.101 vs 63 nos testes). O repoint gravava absoluto → **quebraria in-game**; os
   testes passavam por autoconsistência. Corrigido em `sdat_format`/`reinsert`; as "9 órfãs" eram as
   entradas de bloco file-relativas → agora repointáveis (gambiarra in_place revertida, traduções
   completas restauradas). `REPOINT_cont` caiu 811→5 (quase toda linha tem ponteiro próprio).

## Verificação automatizada (gate de regressão)
- `pytest connector/` → **6/6 verdes**: round-trip de identidade, binário-fonte intacto, **resíduo 0**,
  **verificação do VALOR do ponteiro (file_start+valor, não-circular)**, **teste do modelo file-relativo**,
  e patch IPS aplicável.

## Issues abertas
- Nenhuma bloqueante.

## Pendências (fora deste escopo)
- **In-game:** confirmar que strings relocadas (apêndice ao fim do arquivo) exibem corretamente.
- **Modelo de ponteiro:** mapear o opcode que exibe a **1ª string de cada bloco** (hoje sem `50 00`),
  para repointá-las em vez de exigir fit in_place.
- **T4 em lote (LLM):** adiado pelo usuário — só seria necessário se sobrasse resíduo irredutível.
- Metadados por linha do plano: curados em 11_01_000S; auto-defaultados nas demais.
