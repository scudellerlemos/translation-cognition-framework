# MEDIA PROFILE — JOGOS
## Especialização do framework SDD para localização de jogos

> **O que é um media-profile:** concentra o que é universal **para uma categoria de mídia**,
> mas não para todo o processo. As skills genéricas referenciam este perfil para o racional;
> o `project.json` de cada jogo declara os **valores concretos** (tokens exatos, caminhos, limites).
>
> **Status:** validado (Utawarerumono é a instância de referência).

---

## 1. FORMATO DA FONTE

Jogos expõem texto como **strings indexadas** — cada linha tem um identificador estável
(offset hex, string ID, chave). Em jogos antigos, esse texto está **embutido num binário** e precisa
ser **extraído por um conector** (ver `framework/connectors/`) antes do pipeline começar — não cai
pronto como CSV. O `dialogs.csv` é o **output do Passo 00 (extração)**, não um dado pré-existente.

Declarado no `project.json`:
```json
"source": {
  "file": "artifacts/dialogs.csv",
  "format": "csv_offset",
  "id_column": "offset",
  "text_column": "text_en"
},
"connector": { "type": "hex_binary", "...": "ver framework/connectors/hex_binary.md" }
```

**Invariante:** a fonte é **somente leitura** a partir do Passo 01. O `id_column` é a âncora de
identidade da linha — nunca muda, nunca é reordenado. Toda a rastreabilidade do pipeline depende dele.

---

## 2. TOKENS DE ENGINE

Jogos embutem **tokens de controle** no texto: timers de espera, tags de cor, marcadores de fim,
quebras de linha, variáveis de substituição. O engine os interpreta em runtime — se a tradução
remover, deslocar ou alterar um token, o texto quebra no jogo.

**Regra universal:** preservar exatamente todos os tokens listados em `project.json → formatting_tokens`.
A contagem de cada token por linha deve **bater** entre fonte e tradução, nas posições correspondentes.

Exemplo de declaração (Utawarerumono):
```json
"formatting_tokens": ["{W75}", "{W80}", "{W10}", "{COLOR}", "{END}"]
```

Quebras de linha (`\n`) são tratadas como token estrutural: a contagem deve bater porque o engine
usa `\n` para paginação/fluxo de caixa.

> **Origem dos tokens:** em jogos antigos, cada token é uma **sequência de bytes de controle** no
> binário. O conector (`connector.control_codes`) define o mapeamento token↔bytes; `extract.py`
> decodifica bytes→token e `reinsert.py` recodifica token→bytes. Os `formatting_tokens` são a forma
> legível desse mapeamento. Ver `framework/connectors/hex_binary.md`.

---

## 3. OVERFLOW: CAIXA DE UI **e** BYTE-SPACE

Há duas restrições de comprimento em jogos, e elas são diferentes:

**(a) Caixa de UI** — espaço visual fixo (balões, botões, HUD). Heurística por % do fonte
(`length_constraints.mode: percent`):
- Diálogo ≤ `dialogue_max_pct`% (default 140%) · UI/sistema ≤ `ui_max_pct`% (default 110%)

**(b) Byte-space** — em jogos antigos com reinserção `in_place`, a restrição **real e dura** é o
número de **bytes** que a string pode ocupar no binário. É o `byte_budget` extraído no Passo 00
(`length_constraints.mode: byte_space`). Estourar bytes corrompe o jogo — é mais sério que estourar a caixa.

Medir **por segmento entre quebras de linha**, não a linha inteira de uma vez.

**Prioridade quando há conflito:** tom > caber > literalidade. Nunca sacrificar voz para encurtar.

> **Shift-left:** o `byte_budget` viaja para o Passo 06 e vira restrição de prompt — a tradução já
> nasce dentro do orçamento, evitando overflow e custo de LLM na reinserção. O resíduo que ainda
> estourar é resolvido pela cascata determinística do Passo 08 (T1–T3), com LLM só no resíduo (T4).
> Ver `framework/connectors/hex_binary.md` e `framework/skills/08_reinsertion.md`.

---

## 4. LINHAS DE SISTEMA

Jogos misturam diálogo narrativo com **texto de sistema** (logs de combate, mensagens de erro,
prompts de UI). Esse texto tem registro próprio: frio, técnico, sem afeto.

Convenção de detecção declarada em `project.json → system_line_convention`. Em Utawarerumono é
`all_caps` (linhas inteiramente em CAPS são de sistema). Outros jogos podem usar prefixos, IDs
de namespace, ou uma coluna de tipo.

Regra: linhas de sistema mantêm a convenção na tradução (CAPS permanece CAPS) e usam estrutura
`OBJETO: ESTADO` quando aplicável.

---

## 5. SEGMENTAÇÃO E LOTES

O corpus é processado em **lotes de tamanho fixo** (`project.json → batch_size`, default 200),
ordenados pelo `id_column`. Lotes permitem Micro-QA incremental (Passo 6b) e retomada.

---

## 6. RETOMADA

Como o corpus é grande, a tradução (Passo 6) é interrompível e retomável. O `translation_status.json`
guarda `next_offset` (o próximo `id_column` a traduzir). Retomar = ler o status e continuar do
`next_offset`, nunca do zero. Ver Passo 6 para o protocolo completo.

---

## 7. LINHAS INCOMPLETAS (continuação de frase)

Em muitos engines, uma frase longa é dividida em múltiplas strings consecutivas, cada uma terminando
em `\n`. Ao traduzir, verificar sempre se a junção da linha atual + próxima soa natural no idioma-alvo —
a ordem das palavras pode precisar ser redistribuída entre os segmentos.

---

## 8. INTERJEIÇÕES E TEXTO DE SFX (susto, dor, surpresa)

Visual novels e RPGs são densos em **interjeições e onomatopeias** de emoção (`Ngh...`, `Hm?`, `Gah!`,
`*Floof*`). Elas **são tradução**, não pontuação: localizar à convenção do idioma-alvo (um susto em
pt-BR é `Hein?`/`Ãhn?`, dor é `Ai!`/`Aagh...`), nunca copiar do source — copiar quebra a imersão tanto
quanto um termo não traduzido. Curar a convenção do projeto num artefato de referência e aplicá-la com
coerência. Se o conector translitera na gravação, escolher formas que sobrevivam (sem depender de
acento). Detalhes do processo: `skills/06_translation.md` (regra) e `skills/06b_micro_qa.md` (check).

---

## RESUMO — o que o `project.json` deve declarar para um jogo

| Campo | Função |
|-------|--------|
| `source.format` / `id_column` / `text_column` | Como parsear o corpus |
| `formatting_tokens` | Tokens de engine a preservar |
| `system_line_convention` | Como detectar texto de sistema |
| `length_constraints` | Limites de overflow de UI |
| `batch_size` | Tamanho do lote de tradução |
