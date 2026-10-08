# TOKEN_ECONOMY.md — onde está a economia de tokens

As técnicas que reduzem o custo de tradução, com o mecanismo e a origem de cada número. Visão
da stack inteira → [`STACK.md`](STACK.md).

Um ponto que evita confusão: **a busca semântica não reduz tokens; ela acrescenta.** Cada vizinho
é texto a mais no prompt. O que ela compra é consistência de fraseado, e os tetos de recuperação existem
para que esse acréscimo seja pequeno e previsível (no máximo 8 pares, 3 decisões e 3 seções por
cena). A economia vem das técnicas abaixo, em ordem de impacto.

| Técnica | O que corta | Como | Efeito |
|---|---|---|---|
| **Reuso exato de TM** | tokens de saída, os mais caros (5× o preço de entrada) | `model._select_reuse`: fala com o mesmo hash de fonte já aprovada em outra cena não é enviada ao modelo | cena 100% repetida custa zero; responsável pelos −24% do ADR 0016 |
| **Pacote limitado por cena** | tokens de entrada | seleção por presença de termo, com teto por seção (glossário 60, decisões 12, KB 5, TM de voz 3 por falante) | o prompt não cresce com o projeto |
| **Thinking desligado na tradução** | tokens de saída | `effort: low`, `thinking: disabled`; thinking é cobrado como saída | cerca de 5× de diferença na medição |
| **Roteamento por complexidade** | preço por token | no lote, falas de uma linha só vão para Haiku; as com quebra de linha ficam no Sonnet | −67% por fala roteada |
| **Batch API** | preço por token | `run_chapter` envia as cenas em lote assíncrono | −50% |
| **Retry por fala** | reenvio | se a saída vem incompleta ou inválida, a nova tentativa manda só as falas que falharam; as já pagas ficam em checkpoint | custo do retry proporcional ao que quebrou |
| **Verificação amostrada** | chamadas ao modelo mais caro | back-translation só nas falas de risco alto, mais 5% das demais | Opus vê uma fração do corpus |
| **Prompt caching** | tokens de entrada repetidos | a doutrina de tradução vai no `system` com `cache_control` | pequeno: a doutrina tem cerca de 1.300 tokens, e num capítulo medido custou US$ 0,14 contra US$ 3,41 de saída. No lote as requisições rodam em paralelo e regravam o cache, então o ganho ali é praticamente nulo |

As três técnicas de maior efeito são detalhadas a seguir, com o mecanismo e a origem de cada
número.

## Reuso exato de TM: −24% de custo

**Mecanismo.** Antes de chamar o modelo, `model._prefilled` separa as falas da cena em dois
grupos:

1. Para cada fala, calcula a chave `sha1(fonte normalizada)[:16]` e procura na TM exata do pacote
   (`tm_exact`), que só contém traduções aprovadas.
2. Se achou, e a entrada veio de **outra** cena, e a tradução guardada tem a mesma contagem de
   quebras de linha e de tokens de formatação que a fala atual (`_line_ok`), a fala é preenchida
   com a tradução guardada e marcada como `intent: reuso_tm`.
3. As falas restantes (`novel`) são as únicas que entram no prompt. Se a lista fica vazia, a
   função retorna sem criar o cliente da API: uso `{in: 0, out: 0}`.

O corte é em tokens de **saída**. Cada fala traduzida devolve um objeto JSON com tradução,
falante, registro, intenção e risco, em média 66 tokens, e saída custa 5× a entrada (Sonnet:
US$ 3 por milhão de tokens de entrada, US$ 15 de saída).

As duas condições do passo 2 existem porque reusar errado custa mais do que traduzir de novo:

- **Paridade de estrutura.** A chave ignora quebras de linha, então duas falas com o mesmo texto
  podem quebrar em pontos diferentes. Reusar uma tradução com quebras diferentes reprova na
  reinserção.
- **Nunca a própria cena.** Ao re-traduzir uma cena para encurtar o texto, reusar a saída anterior
  dela devolveria justamente a tradução que não coube. Por isso o reuso também é desligado nas
  rodadas de re-tradução por estouro de espaço.

**Medição** ([ADR 0016](adr/0016-rag-roi-validado-reindex-obrigatorio.md)). As mesmas 10 cenas do
Breath of Fire IV foram traduzidas duas vezes: uma sem o banco, outra com o banco reindexado
depois de cada cena.

| | Sem banco | Com banco | Diferença |
|---|---:|---:|---:|
| Custo total das 10 cenas | US$ 1,2797 | US$ 0,9714 | **−24%** |
| Cenas concluídas | 5 de 10 | 7 de 10 | +2 |
| Custo por cena concluída | US$ 0,138 | US$ 0,086 | −38% |

Duas das dez cenas saíram a US$ 0,00 com o banco (todas as falas reusadas), contra US$ 0,066 a
US$ 0,155 nas mesmas cenas sem ele. Eram cenas de texto de sistema e de menu, repetido entre áreas
do jogo. O ganho veio daí, e não dos vizinhos semânticos.

Limites: a amostra é de 10 cenas, e o efeito depende de quanto o jogo repete texto. Em outra
medição, num capítulo de Utawarerumono, só 2,8% das falas eram reusáveis. O percentual cresce com
o corpus já traduzido, e por isso a tradução aprovada precisa estar disponível logo na cena
seguinte: a reindexação acontece a cada aprovação, e não em lote no fim.

## Thinking desligado na tradução: cerca de 5×

**Mecanismo.** A chamada de tradução é montada com `thinking: {"type": "disabled"}` e
`output_config.effort: "low"` (constantes `THINK_TRANSLATE` e `EFFORT_TRANSLATE`). Os tokens de
raciocínio do modelo são cobrados como tokens de saída, ao mesmo preço da resposta.

**Medição.** Na primeira rodada real, com `effort: high` e thinking adaptativo, uma cena de 37
falas gerou cerca de 20.000 tokens de saída. Com os valores atuais, uma cena de 37 falas gera
2.529. No custo, a diferença registrada foi de cerca de 5×; projetado para o jogo inteiro, de
aproximadamente US$ 285 para US$ 36.

**Por que não perde qualidade.** O raciocínio que o thinking faria (que termo usar, como o
personagem fala, o que já foi decidido) já chega resolvido no pacote de contexto. No benchmark sem
thinking, uma cena coberta pela TM saiu com 37 de 37 falas idênticas à referência, e uma cena de
comédia de 408 falas, fora da TM, manteve registro e humor no nível da versão de referência.

A back-translation mantém thinking: ali o modelo precisa comparar sentido entre duas versões, e
ela só roda nas falas de risco alto.

## Haiku para falas de uma linha: −67% por fala

**Mecanismo.** No caminho de lote, cada fala é classificada por uma regra de uma linha:

```python
def _tier_of(source):
    return "main" if TOKEN in source else "cheap"   # TOKEN = marcador de quebra de linha do jogo
```

As falas `cheap` de uma cena vão em requisições para `claude-haiku-4-5`; as `main`, para
`claude-sonnet-4-6`. As respostas são fundidas por fala antes da validação.

**De onde vem o número.** É a razão de preço, e não uma medição: Haiku custa US$ 1 e US$ 5 por
milhão de tokens (entrada e saída), Sonnet custa US$ 3 e US$ 15. Um terço do preço nos dois
sentidos, logo −67% em cada fala roteada.

**Por que o critério é a quebra de linha.** O benchmark mostrou a voz do Haiku no nível da do
Sonnet, inclusive em registro arcaico. A fraqueza medida foi outra: em escala, Haiku erra a
contagem do marcador de quebra de linha, e a tradução reprova na validação. Esse erro só pode
acontecer em fala que tem quebra. Mandar para o Haiku só as falas sem quebra usa o modelo barato
exatamente onde a fraqueza dele não se manifesta.

**Alcance.** Medido em 44.116 falas de um jogo: 59% são de uma linha só (26.004 contra 18.112),
com variação de 56% a 67% entre capítulos. Em tokens a fatia é menor, porque falas de uma linha
são mais curtas. A economia agregada de um capítulo inteiro não foi medida isoladamente.

O roteamento vale só no lote. O caminho em tempo real (re-tentativas e casos difíceis) fica no
Sonnet. Um detalhe de API: Haiku 4.5 rejeita o parâmetro `effort` com erro 400, então ele é
omitido nas requisições desse modelo.

A amostragem de 5% na back-translation existe por causa desse roteamento: as falas de risco baixo
e médio, que incluem as que vão ao Haiku, não passariam por nenhuma verificação de sentido. A
amostra dá um piso de qualidade medido para o modelo barato.
