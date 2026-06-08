# CONECTOR — hex_binary
## Conector para jogos antigos (texto embutido em binário, estilo HxD)

> **Status:** definido. Instância de referência: Utawarerumono.
> Este documento é o **contrato** dos scripts `extract.py` / `reinsert.py`. Não contém código
> específico de jogo — esse código é escrito pela IA por projeto, a partir do esqueleto em
> `_skeleton/`, e vive em `projects/<título>/connector/`.

---

## QUANDO USAR

O texto da obra está embutido em um **arquivo binário** e só é legível com um **hex editor** (HxD)
mais uma **tabela de caracteres** (byte→glifo). Cada string é endereçada por **offset** e
referenciada por **ponteiros**. É o caso clássico de jogos de console antigos / ROMs.

---

## FONTE EM PACOTE (entregue pelo usuário)

Vale também para jogos modernos cujo texto vive **dentro de um pacote** (ex: `.sdat`) e ainda
assim é **editável em hex no lugar** (HxD mostra e edita o texto direto). Nesse caso:

- O pacote é tratado como o **próprio binário-fonte**. `connector.container_format` (ex: `sdat`)
  e `connector.inner_path` apenas **documentam o que foi entregue** (proveniência) — não exigem
  desempacotamento.
- **Governança da entrega:** o **usuário entrega** o arquivo — copiando para `artifacts/`
  (`source_binary` relativo) ou passando por **CLI**. A localização real (ex: pasta da Steam) é
  só **orientação ao humano**; o conector **nunca** guarda caminho absoluto de input.
- **Por que editar na mão "às vezes estraga" — e como o conector resolve:** sobrescrever bytes
  no HxD sem disciplina estoura o slot da string ou desalinha tamanhos/ponteiros. Os mecanismos
  do conector eliminam isso deterministicamente: **`byte_budget`** (anti-overflow),
  **`pointer_table` + `space_strategy: repoint`** (recalcula offsets quando o alvo cresce) e o
  **gate de round-trip** (troca "a maioria abre" por "abre 100% ou trava antes de traduzir").
- **Reserva (fora do escopo atual):** se um pacote for **opaco** (comprimido / com checksum que
  quebra ao sobrescrever bytes), aí é preciso um passo de **unpack → editar → repack
  byte-idêntico** — o conector `archive_script` (🚧 em `00_index.md`), ainda não definido.

---

## O SCHEMA DE TABELA (coração do conector)

Um único `table_schema` (ver `_skeleton/table_schema.md`) é compartilhado por extração e reinserção.
Ele define:
- **Mapa byte→caractere** (e o inverso caractere→byte)
- **Control codes:** sequências de bytes que viram tokens (`{W75}`, `{END}`, quebra de linha, cor)
- **Terminadores** de string
- **Encoding** (largura fixa, variável, custom)

Manter o schema estável é o que garante o round-trip. Extração e reinserção **nunca** divergem na tabela.

---

## CONTRATO: `extract.py`

```
extract.py(source_binary, table_schema) → dialogs.csv + extraction_log.md
```

**Determinístico.** Para cada string localizada no binário:
1. Ler bytes a partir do offset até o terminador
2. Decodificar via tabela (byte→caractere)
3. Substituir sequências de control code pelos tokens correspondentes
4. Registrar a linha em `dialogs.csv` com:
   - `<id_column>` = offset (hex)
   - `text_source` = texto decodificado
   - `byte_budget` = nº de bytes que a string ocupa no binário (**shift-left** — ver Passo 06)
5. Acumular metadados em `extraction_log.md` (tabela usada, encoding, mapa de control codes, total de strings, offsets cobertos)

---

## CONTRATO: `reinsert.py`

```
reinsert.py(approved_translations.csv, dialogs.csv, table_schema, source_binary)
    → output/<nome-original> + patch + reinsertion_report.md
```

**Determinístico.** Para cada string em `approved_translations.csv`:
1. Recodificar `text_target` via tabela (caractere→byte)
2. Substituir tokens pelas sequências de control code
3. Aplicar a **cascata de encaixe** (abaixo)
4. **Sobrescrever** os bytes do idioma-fonte pelos do idioma-alvo, conforme `space_strategy`
5. Gravar em `output/<nome-original>` (**mesmo nome e extensão do input**) **e** um patch (`patch_format`)
6. Registrar overflows, repoints e falhas em `reinsertion_report.md`; **informar o caminho de saída**

> O original-fonte nunca é sobrescrito em disco. A saída vai para `output/` no projeto.
> A IA **não escreve a tradução à mão** — `reinsert.py` aplica o `approved_translations.csv`.

---

## CASCATA DE ENCAIXE (custo crescente — só sobe quem falha)

A reinserção precisa caber a tradução no espaço disponível. Resolver do mais barato ao mais caro:

| Tier | Método | Custo LLM |
|------|--------|-----------|
| **T1** | **Escrita direta** — cabe no byte-space → grava | zero *(maioria)* |
| **T2** | **Recuperação de espaço** — repointing (se permitido); reuso de espaço de strings que encolheram; tabela de abreviações seguras | zero |
| **T3** | **Trim mecânico** — colapsar espaços duplos, reticência tipográfica (…), abreviações do glossário do projeto | zero |
| **T4** | **Reescrita por LLM** — só o resíduo, numa **única chamada em lote**; volta pelo Micro-QA (06b) | mínimo |

A maior parte do custo já foi eliminada no **shift-left** (orçamento de bytes na tradução, Passo 06),
então T4 tende a processar pouquíssimas strings.

---

## ESTRATÉGIA DE ESPAÇO (`space_strategy`)

| Valor | Significado | Restrição de comprimento |
|-------|-------------|--------------------------|
| `in_place` | A tradução é gravada no mesmo slot de bytes da original | Limite **em bytes** (`byte_budget`) — não % de caracteres |
| `repoint` | Ponteiros são recalculados; a tradução pode crescer | Limitada pelo espaço total realocável |

Quando `in_place`, o `length_constraints` do `project.json` opera em **modo byte-space**.

> **Escolha do default (aprendizado de campo):** para idiomas-alvo mais longos que o fonte ou com
> acentos UTF-8 multibyte (ex: EN→pt-BR), `in_place` raramente cabe — na POC do Utawarerumono só
> **60% (12/20)** das linhas couberam no `byte_budget`. **Prefira `repoint`** nesses casos; reserve
> `in_place` para quando o alvo é ≤ o fonte em bytes. Reporte a **taxa de fit** do byte-budget na
> extração/tradução para decidir com dados, não no chute.

---

## FONTE / GLIFOS DO IDIOMA-ALVO (gate de charset)

A fonte do jogo pode não ter os glifos do idioma-alvo (pt-BR: ã, ç, õ, á, ê...). Antes de traduzir, avaliar — **nesta ordem de confiabilidade**:

1. **Inspecionar a fonte/atlas** (método primário) — parsear a charmap e listar os code points do alvo ausentes. É a fonte de verdade sobre quais glifos existem.
2. **Teste in-game** — renderizar um pangrama do alvo (ex: `áéíóú âêô ãõ ç ÁÉÍ ÃÕ Ç`) e observar.
3. **Presença no texto-fonte** (sinal **fraco**, só complementar) — se um acento já aparece no texto que o jogo renderiza, a fonte o tem. ⚠️ **Cuidado:** quando o idioma-fonte não usa os acentos do alvo (ex: inglês), quase nenhum aparecerá — ausência no texto **não** prova ausência na fonte. (POC: no texto EN só `õ`/`À` apareciam, embora a fonte provavelmente cubra todo o bloco Latin-1.)

Valores de `target_charset_supported`: `true` / `false` / `likely` (provável, a confirmar) / `unknown`.

- Se faltarem glifos: **AVISO/BLOQUEIO** documentado. Opções: expandir a fonte/tabela (adicionar glifos)
  ou transliteração determinística de fallback (ã→a, ç→c...).
- A escolha (e o veredito do gate) viram entrada no `decision_log.md`.

---

## ORDEM DE EXTRAÇÃO ≠ ORDEM DE EXIBIÇÃO

A extração por offset produz as strings na ordem de **armazenamento**, que **nem sempre** é a ordem
em que o jogo as **exibe** (a ordem narrativa é controlada pelo script, via ponteiros). Para a maioria
do controle de qualidade (voz, tokens, byte-budget) a ordem por offset basta. Quando a **continuidade
narrativa** importa (contexto entre falas, comédia com timing, revelações), interpretar a ordem do
script é necessário — documentar a limitação no `extraction_log.md`.

---

## ANOMALIAS DE FONTE

O texto-fonte pode vir corrompido ou inconsistente no próprio jogo (idiomas misturados, truncamento,
bytes inesperados). O `extract.py` deve **sinalizar** essas strings no `extraction_log.md` em vez de
tratá-las como texto normal. (POC: a linha `0x33f9` vinha meio PT/EN corrompida no jogo original.)

---

## PONTEIROS

- `pointer_table` no `project.json` declara onde está e o formato (ex: little-endian 16-bit relativo à base).
- Em `space_strategy: repoint`, `reinsert.py` recalcula cada ponteiro deterministicamente após gravar as strings.
- Recalcular ponteiros é **aritmética** — nunca usar LLM para isso.

---

## CHECKLIST DE CONFORMIDADE DO CONECTOR

```
□ extract.py e reinsert.py consomem o MESMO table_schema?
□ extract.py emite byte_budget por string?
□ Round-trip (extract → reinsert idêntico === original) passa byte-a-byte?
□ Control codes mapeiam para os formatting_tokens do project.json?
□ space_strategy declarada (repoint p/ alvo mais longo) e taxa de fit reportada?
□ Gate de charset avaliado inspecionando a FONTE (não só presença no texto)?
□ Anomalias de fonte sinalizadas no extraction_log?
□ Build de saída com a mesma extensão do fonte, em artifacts/build/?
□ Saída inclui o patch no patch_format declarado?
```

> **Os scripts são executados, não refeitos.** Uma vez escritos, `extract.py`/`reinsert.py` são
> **rodados como ferramenta** — a IA não re-extrai nem re-grava bytes manualmente (determinismo +
> economia de tokens). Só reescrever o script se o formato do binário mudar.
