# CONECTOR — archive_script
## Conector para jogos cujo texto vive dentro de um container de ENGINE de terceiro

> **Status:** definido. Instância de referência: Souldiers (Unity Addressables).
> Este documento é o **contrato** dos scripts `extract.py` / `reinsert.py` para esta categoria. Não
> contém código específico de jogo — esse código é escrito pela IA por projeto e vive em
> `projects/<título>/connector/`.

---

## QUANDO USAR (diferença de `hex_binary`)

`hex_binary.md` cobre formatos **proprietários e simples**: nós mesmos fazemos a engenharia reversa
do layout de bytes (a Capcom/Aquaplus inventaram o formato, mas é struct-based e cabe inteiro na
nossa cabeça — TOC + ponteiros + strings). `archive_script` cobre o caso oposto: o texto vive dentro
de um **container serializado por uma ENGINE de terceiro** (Unity, Godot, RPG Maker, Ren'Py, etc.),
com formato **versionado, comprimido e/ou com metadata de tipos** que a engine controla — não é
"HxD-editável no lugar" (ver `hex_binary.md`, seção "Reserva"), exige **unpack → editar → repack**
usando a biblioteca/SDK daquela engine.

Use `archive_script` quando:
- O container não abre num hex editor genérico sem corromper (compressão, checksum, TypeTree).
- Existe uma biblioteca de leitura/escrita **específica da engine** (ex: UnityPy pra Unity) que faz
  o papel do "hex editor" — ela entende a estrutura, nós não editamos bytes crus.
- A mesma engine provavelmente vai aparecer em **outros títulos** (jogos Unity são o caso mais comum) —
  o conector agrupa por família de engine, não por título (ver memória `connector-evolution-vision`).

---

## PROPRIEDADE CENTRAL: a mesma do `hex_binary`

```
extract.py(container)        → dialogs.csv
reinsert.py(dialogs.csv)     → container'          (sem traduzir nada)
INVARIANTE:  container' === container               (byte-a-byte idêntico)
```

O invariante de round-trip **não muda** — só a ferramenta que garante que ele seja verificável muda
(biblioteca da engine em vez de `struct.pack`/`struct.unpack` puro).

---

## CONTRATO: `extract.py`

```
extract.py(container, biblioteca_da_engine) → dialogs.csv + extraction_log.md
```

1. Carregar o container via biblioteca da engine (ex: `UnityPy.load(path)`).
2. Localizar o(s) asset(s)/tabela(s) que contêm texto de diálogo (ex: `TextAsset` por nome).
3. Decodificar o payload interno (pode ser CSV, JSON, ou outro formato aninhado dentro do asset).
4. Registrar cada linha em `dialogs.csv` com `<id_column>`, `text_source`, `byte_budget` (ou
   equivalente — engines modernas raramente têm limite rígido de bytes; usar `char_budget` se for
   o caso).
5. Acumular metadados em `extraction_log.md` (versão da engine/lib usada, nomes de asset cobertos).

---

## CONTRATO: `reinsert.py`

```
reinsert.py(approved_translations.csv, dialogs.csv, container) → output/<nome-original>'
```

1. Carregar o MESMO container original via biblioteca da engine.
2. Localizar o mesmo asset/payload interno.
3. Sobrescrever o payload com a tradução aprovada (ex: reescrever a coluna do CSV interno).
4. **Resalvar** via biblioteca da engine (ex: `env.file.save()` do UnityPy) — a biblioteca cuida de
   recompressão/checksum/serialização; nós nunca escrevemos esses bytes à mão.
5. Gravar em `output/` com o mesmo nome/formato.

---

## ESTRATÉGIA DE FIXTURE SINTÉTICA — a diferença real vs. `hex_binary`

Em `hex_binary`, a fixture de teste (`test_roundtrip_synthetic.py`) é bytes puros escritos à mão em
Python (`struct.pack`) — não precisa de nenhuma ferramenta externa, porque nós entendemos 100% do
formato (é nosso, ou simples o bastante pra reproduzir).

Em `archive_script`, isso **não é possível**: bibliotecas de leitura de engine (UnityPy e
equivalentes) são desenhadas pra **ler e modificar** containers existentes, não pra **criar um do
zero** — o serializador de verdade é o pipeline de build da própria engine (ex: Unity
`BuildPipeline.BuildAssetBundles`). Confirmado no código do UnityPy instalado:
`SerializedFile.__init__(self, reader: EndianBinaryReader, ...)` exige bytes já existentes, sem
construtor vazio. Isso não é uma limitação de ferramenta ruim — é a fronteira real de quem é "dono"
do formato.

**Padrão recomendado (template + patch-helper), por família de engine:**

```
framework/connectors/fixtures/<engine>/template.<ext>   ← gerado 1x, fora do CI, com a
                                                            ferramenta de build da própria engine
                                                            (conteúdo autoral nosso, sem dado
                                                            do jogo real)
framework/connectors/<engine>/fixture_helper.py          ← patch_content(template_path, ...) -> bytes
                                                            reusa a biblioteca de leitura (UnityPy
                                                            etc.) pra carregar o template, sobrescrever
                                                            o payload de teste, e resalvar
```

Cada `projects/<título>/connector/test_roundtrip_synthetic.py` de um jogo daquela engine chama o
helper compartilhado — reuso real de família, sem reimplementar a leitura/escrita do container em
cada projeto.

**Se ainda não há o template gerado** (caso atual do Souldiers/Unity): não force uma fixture frágil
que finja cobrir o round-trip do container inteiro. Alternativa honesta: extrair e testar **só a
lógica pura de transformação do payload interno** (ex: reescrita da coluna do CSV dentro do
`TextAsset`), deixando explícito no docstring do teste que isso NÃO é o oráculo de round-trip
completo do container — esse continua validado contra o arquivo real do jogo, localmente, antes de
cada entrega (ver `projects/souldiers/connector/test_rebuild_table_logic.py` e
`test_roundtrip.py`).

---

## CHECKLIST DE CONFORMIDADE DO CONECTOR

```
□ extract.py e reinsert.py usam a MESMA biblioteca/versão de leitura da engine?
□ Round-trip (extract → reinsert idêntico === original) validado contra o arquivo REAL do jogo?
□ A lógica pura de transformação do payload interno (fora da camada da engine) tem teste sempre-ativo,
  mesmo sem o arquivo real disponível no CI?
□ Se existir template sintético da engine: fixture gerada com a ferramenta de build oficial da
  engine, sem dado do jogo real, documentada em framework/connectors/fixtures/<engine>/?
□ Nenhum caminho de input hardcoded (mesma regra do hex_binary)?
```

> **Decisão de categoria (pra quem for adicionar o próximo conector):** o formato é proprietário e
> simples o bastante pra reproduzir em bytes puros (mesmo que a codificação não seja ASCII)? →
> `hex_binary.md`. É um container serializado por uma engine de terceiro que só abre com a lib/SDK
> daquela engine? → este documento (`archive_script.md`).
