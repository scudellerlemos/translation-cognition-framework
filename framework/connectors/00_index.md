# CONECTORES — Índice
## A camada de I/O entre o framework e o meio de armazenamento da obra

> Um **conector** é a ponte entre o framework (que opera sobre texto canônico em CSV) e o **meio
> onde a obra guarda o texto** (binário do jogo, arquivo de legenda, etc.). Diferente das skills
> — que são processo cognitivo — o conector é **código determinístico**.

---

## O QUE O CONECTOR FAZ

Duas operações, em direções opostas, governadas pelo **mesmo schema de tabela**:

```
  EXTRAÇÃO  (Passo 00)                    REINSERÇÃO  (Passo 08)
  extract.py(binário) → dialogs.csv       reinsert.py(approved_translations.csv) → output/<nome-original>
        decode (byte→texto)                      encode (texto→byte)
```

- **Extração:** o usuário fornece o binário (dump do HxD); a IA escreve `extract.py`, que decodifica
  o texto usando a tabela de caracteres, mapeia bytes de controle para tokens (`{W75}` etc.) e
  registra o offset de cada string como `id_column`.
- **Reinserção:** `reinsert.py` aplica o `approved_translations.csv` (traduções **aprovadas**),
  **sobrescreve o idioma-fonte pelo idioma-alvo** (ex: inglês → pt-BR) e grava em `output/` um arquivo
  no **mesmo nome e formato** consumido pelo extrator.

---

## GOVERNANÇA DOS SCRIPTS (regra global)

Os scripts do conector (`extract.py`, `reinsert.py`, e qualquer apply) são **ferramentas executadas**,
não trabalho refeito pela IA:

- Se um script **não existe**, a IA **alerta** e **só o cria com permissão** do usuário (a partir do `_skeleton/`).
- Se **existe**, a IA **apenas o executa** — nunca extrai/grava bytes nem traduz à mão dentro dos dados.
- Só reescrever um script se o **formato do binário mudar**.
- A IA **não escreve a tradução à mão**: ela propõe no `translation_plan.json`, o usuário aprova em
  `approved_translations.csv`, e o script aplica.
- **Nenhum texto da obra dentro do `.py`.** Os scripts são determinísticos e **leem as frases de
  artefatos** (`dialogs.csv`, `translation_plan.json`, `approved_translations.csv`) — nunca contêm
  diálogos nem traduções hardcoded no código.
- **Nenhum caminho de input hardcoded.** O **usuário fornece o binário**; o caminho vem de
  `connector.source_binary` no `project.json` (ou de um argumento de CLI). Sem arquivo válido, o
  script **falha com mensagem clara** pedindo o input.

---

## PROPRIEDADE CENTRAL: ROUND-TRIP DETERMINÍSTICO

```
extract.py(binário)        → dialogs.csv
reinsert.py(dialogs.csv)   → binário'          (sem traduzir nada)
INVARIANTE:  binário' === binário              (byte-a-byte idêntico)
```

Antes de qualquer tradução, rodar extract → reinsert-sem-mudanças e comparar com o original.
**Se não for byte-idêntico, o conector está perdendo informação — o pipeline é BLOQUEADO.**
Esse teste prova que os scripts são corretos e que a tradução poderá ser devolvida com segurança.

---

## PRINCÍPIO DE CUSTO: determinístico primeiro, LLM só no resíduo

O patch-back parece caro, mas quase nada nele precisa de LLM:

| Operação | Método | Custo LLM |
|----------|--------|-----------|
| Detectar se a tradução cabe | encode + contar bytes vs orçamento | **zero** (aritmética) |
| Escrever bytes, mapear tokens, ponteiros | `reinsert.py` determinístico | **zero** |
| Fazer caber no byte-space | shift-left + cascata determinística | **~zero** |
| Reescrever o resíduo que ainda estoura | 1 chamada LLM **em lote** | **mínimo** |

LLM é caro, lento e pior que código para byte-math — fica fora do caminho mecânico. Ver `hex_binary.md`
para a cascata T1–T4 e `../skills/08_reinsertion.md` para o protocolo.

---

## RELAÇÃO COM OS MEDIA-PROFILES

O **media-profile** descreve as *preocupações conceituais* da categoria (ver `../media-profiles/`).
O **conector** é o *mecanismo de I/O em código* para aquela categoria:

| Media-profile | Conector típico | Status |
|---------------|-----------------|--------|
| `games` (retrô) | `hex_binary` | ✅ definido (ver `hex_binary.md`) |
| `games` (moderno) | `archive_script` | 🚧 ponto de extensão |
| `films` / `series` | `subtitle_file` (SRT/ASS) | 🚧 ponto de extensão |

O `project.json → connector.type` declara qual conector a instância usa.

---

## ESTRUTURA

```
connectors/
  00_index.md        ← este arquivo
  hex_binary.md      ← contrato do conector de jogos antigos (tabela, ponteiros, byte-space, cascata)
  _skeleton/
    extract.py       ← esqueleto comentado do extrator (a IA adapta por projeto)
    reinsert.py      ← esqueleto comentado do reinseridor (cascata T1–T4 + patch)
    table_schema.md  ← formato do schema de tabela (byte=char + control codes)
```

Os scripts **reais** (adaptados ao binário específico) vivem na instância, em
`projects/<título>/connector/`. O framework fornece apenas contrato + esqueleto.
