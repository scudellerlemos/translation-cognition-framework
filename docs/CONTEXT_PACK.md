# CONTEXT_PACK.md — o pacote de contexto

Como o prompt de cada cena é montado: o que entra, como é selecionado e por que a seleção é
léxica. Visão da stack inteira → [`STACK.md`](STACK.md). Busca semântica →
[`RAG_ARCHITECTURE.md`](RAG_ARCHITECTURE.md).

O problema que ele resolve: um jogo tem milhares de falas, um glossário de centenas de termos e um
histórico de decisões que só cresce. Colocar tudo isso em cada prompt custa caro e estoura a
janela do modelo. O pacote de contexto (`framework/runtime/context_pack.py`) monta, para cada
cena, um prompt que contém **só o que aquela cena precisa**. O tamanho do prompt depende do
tamanho da cena, e não do tamanho do projeto.

`build_pack(projeto, cena)` é uma função pura sobre arquivos: lê as falas da cena e as fontes do
projeto, seleciona um subconjunto de cada fonte e grava dois arquivos no diretório da cena:
`pack.json` (estruturado, consumido pelo backend `api`) e `scene_prompt.md` (o mesmo conteúdo como
prompt pronto, usado pelo backend `in-session`).

## Como a seleção funciona

O texto-fonte de todas as falas da cena é concatenado e passado para minúsculas (`blob_low`). Cada
fonte é filtrada por **presença de termo** nesse texto. A primitiva é uma só, `_present`:

```python
# termo alfanumérico: limite de palavra, com plural inglês opcional
re.search(r"\b" + re.escape(termo) + r"(?:e?s)?\b", blob_low)
# termo com espaço ou pontuação: substring simples
termo in blob_low
```

O limite de palavra evita falso positivo de substring (o termo `system` não casa dentro de outra
palavra); o sufixo opcional faz `cohort` casar `cohorts` sem abrir para substring solta.

| Seção do pacote | Regra de seleção | Limite | Função |
|---|---|---|---|
| Glossário | o termo ou um de seus aliases está presente na cena | 60 entradas, em ordem alfabética | `select_glossary` |
| Voice cards | o nome ou um alias do personagem está presente; personagens de criticidade alta entram sempre | — | `select_voices` |
| Decisões | as universais (regras do conector) primeiro; depois as que têm tag igual a um termo ou falante presente, ou que citam um deles no resumo | 12 | `select_decisions` |
| TM exata | a fala já foi traduzida antes: `sha1(fonte normalizada)[:16]` igual ao de uma entrada da TM | uma por fala | `select_tm` |
| TM de voz | exemplos de falas já traduzidas do mesmo falante, para fixar o registro | 3 por falante | `select_tm` |
| KB / lore | uma palavra (≥ 4 letras) do título da seção está presente na cena **e** a seção tem marca de revelação já ultrapassada | 5 seções | `select_kb` |
| Guardas de spoiler | um fato ainda **não** revelado neste ponto da história tem um gatilho presente na cena; entra a instrução de como manter a ambiguidade | — | `select_spoiler_guards` |
| Regras do projeto | tokens de formatação, token de quebra de linha, orçamento de bytes por fala | fixo | `project_constraints` |

### A chave da TM exata

A chave que identifica "a mesma fala" é calculada por duas funções em `framework/text_ids.py`:

```python
def norm_source(s: str) -> str:
    # token literal "\n" do jogo vira espaço; minúsculas; espaços colapsados; pontas aparadas
    return re.sub(r"\s+", " ", (s or "").replace("\\n", " ").lower()).strip()

def tm_key(s: str) -> str:
    # SHA-1 do texto normalizado em UTF-8; ficam os 16 primeiros caracteres hex
    return hashlib.sha1(norm_source(s).encode("utf-8"), usedforsecurity=False).hexdigest()[:16]
```

Exemplo: a fala `Where do you\nwant to go?` é normalizada para `where do you want to go?`, e a
chave são os 16 primeiros caracteres do SHA-1 desse texto.

- **A normalização define o que conta como a mesma fala.** Caixa, espaços e posição da quebra de
  linha são ignorados. Qualquer outra diferença (uma vírgula, uma palavra) gera outra chave.
- **O SHA-1 é só um identificador, não uma medida de segurança.** O `usedforsecurity=False`
  declara isso. Qualquer hash estável serviria.
- **16 caracteres hex são 64 bits.** Com milhares de falas por jogo, a chance de duas falas
  diferentes terem a mesma chave é desprezível.
- **A chave é a mesma nos dois modos de persistência.** Arquivos e banco usam essa função, então
  a TM de um é compatível com a do outro.

A busca é um dicionário `chave → tradução`, montado uma vez por cena.

### Por que hash, e como os dois caminhos se dividem

A chave responde uma pergunta só: "esta fala já foi traduzida?". Ela existe para responder isso
sem usar modelo nenhum.

- **É a pergunta certa para a decisão mais cara.** Decidir que uma fala **não vai ao LLM** exige
  certeza. Duas falas com cosseno de 0,97 podem ser "Vá para o norte" e "Vá para o sul"; reusar a
  tradução de uma na outra seria erro. Só igualdade de texto autoriza o reuso.
- **Normalizar antes de comparar aumenta os acertos sem risco.** Comparar o texto cru perderia as
  falas que só mudam em caixa, espaço ou posição da quebra de linha, que são a mesma fala para
  fins de tradução.
- **O hash dá uma chave curta e de tamanho fixo.** A consulta é um acesso a dicionário em memória,
  O(1) por fala.

O sistema identifica uma fala já traduzida por dois caminhos independentes:

| | Caminho exato | Caminho semântico |
|---|---|---|
| Pergunta | esta fala já foi traduzida? | que falas traduzidas se parecem com esta? |
| Como identifica | `tm_key` da fala igual à de uma tradução aprovada | vizinhos por distância em `tm_vectors` |
| Usa embedding | não | sim |
| Match exato | é o alvo | é excluído no SQL (score ≥ 0,999), porque o caminho exato já cuidou dele |
| O que faz com o resultado | a fala **não vai** ao modelo (`_select_reuse`) | o par entra no prompt como referência para as falas novas |
| Efeito em tokens | corta saída | acrescenta entrada, com teto |

No caminho exato, ao montar o pacote o código carrega as traduções aprovadas do projeto, calcula
`tm_key` de cada fonte e monta o dicionário; depois calcula a mesma chave para cada fala da cena e
consulta. No modo arquivos a chave vem gravada na TM (`src_key`); no modo banco ela é calculada na
hora, em Python, e não é coluna da tabela.

Consequências para o RAG:

- **Divisão de trabalho.** O caminho exato decide o que não traduzir; o semântico só informa. É
  por isso que a economia medida veio do hash, e não do embedding.
- **As vagas do top-k ficam para vizinhos de verdade.** Sem a exclusão do match exato, uma fala
  repetida como "Yes." ocuparia os 3 vizinhos com cópias de si mesma.
- **Os dois caminhos só leem `approved=1`.** O que alimenta o reuso e as referências já passou no
  round-trip.

Dois limites conhecidos:

- **A TM é carregada por cena.** No modo banco o dicionário é remontado a cada cena, a partir de
  todas as traduções aprovadas. Com milhares de linhas o custo é desprezível; com milhões valeria
  gravar a chave como coluna indexada e consultar só as falas da cena.
- **"Exato" tem duas definições.** O hash normaliza caixa e espaços; o corte de 0,999 é aplicado
  ao vetor do texto sem os códigos do jogo. Os critérios são parecidos, mas não idênticos.

O pacote também grava `doctrine_hash`: um SHA-1 da doutrina de tradução, do glossário e do log de
decisões. Se qualquer um deles mudar depois, dá para saber quais cenas foram traduzidas com a
versão antiga.

## Por que léxico, e não por embedding

Seleção léxica aqui quer dizer comparar strings (match de termo, hash de texto normalizado), sem
modelo de similaridade. A escolha é deliberada:

- **Os alvos são nomes próprios e termos fechados.** A pergunta "o termo *Gigiri* aparece nesta
  cena?" tem resposta exata. Embedding responde "que texto se parece com este?", que é outra
  pergunta: traria termos parecidos que não estão na cena e poderia deixar de fora um termo que
  está. Um termo de glossário que falta no prompt vira inconsistência de tradução.
- **Cada item do pacote é auditável.** Tudo o que entrou tem uma causa verificável a olho: uma
  string que está na cena. Não há limiar de score para calibrar nem resultado que mude com a
  versão do modelo de embedding.
- **É determinístico sem depender de mais nada.** O mesmo estado de projeto gera o mesmo
  `pack.json`, byte a byte (`test_context_pack_deterministic`). Isso permite cachear, comparar
  runs e reproduzir um bug de tradução a partir do pacote que o gerou.
- **Não tem dependência.** Roda só com a biblioteca padrão, sem banco e sem a stack de ML. É por
  isso que os projetos em arquivos funcionam sem embedding.
- **Custa nada.** São expressões regulares e consultas a dicionário sobre o texto de uma cena.

O que o léxico não cobre é a fala **parecida mas não idêntica** a uma já traduzida: o hash muda
com uma palavra de diferença. Esse é o único caso em que similaridade ajuda, e é o que a busca
semântica acrescenta ([`RAG_ARCHITECTURE.md`](RAG_ARCHITECTURE.md)), sempre em seções separadas do
prompt e sem mexer na seleção acima.
