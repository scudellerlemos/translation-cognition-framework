# Engenharia de Prompt no Framework

O framework não ajusta pesos de modelo nem faz fine-tuning. Todo o comportamento da IA é
controlado via prompt — e as técnicas usadas não são casuais. Este documento explica quais
estratégias de prompting o framework emprega, por que cada uma foi escolhida e qual o custo real
de cada decisão.

---

## Chain-of-thought (CoT) e thinking adaptativo

Chain-of-thought pede que o modelo explicite o raciocínio passo a passo antes de dar a resposta
final. É útil quando a tarefa exige encadeamento lógico: ambiguidade semântica, duplo sentido,
verificação de voz — situações onde o caminho percorrido pelo modelo importa tanto quanto a saída.

**No framework:** CoT aparece exclusivamente na **back-translation** (`back_translate`), rodando com
Opus e `thinking` habilitado. A ideia é simples: linhas de alto risco (risco ≥ `high`) são
retraduzidas de pt-BR para EN e o raciocínio exposto permite detectar onde a tradução original
perdeu sentido ou alterou a voz do personagem.

**Custo:** em produção, descobrimos que `effort:high` + thinking **estourou o custo ~5×** na
tradução comum — 37 linhas geraram 20 000 tokens de saída porque o modelo "pensou em voz alta"
em cada linha. Por isso o framework divide: tradução roda com `effort:low`, sem thinking; só a
back-translation usa CoT. Esse ajuste sozinho reduziu o custo de ~$285 para ~$36 por jogo.

---

## Role-based prompting — a Doutrina

Role-based prompting instrui o modelo a responder como se ocupasse um papel específico. O
objetivo não é mudar o tom superficialmente, mas induzir vocabulário, prioridades e enquadramento
compatíveis com um domínio — neste caso, o de um tradutor literário especializado em localização
de jogos.

**No framework:** a Doutrina (também chamada de Carta) é o `system` prompt enviado a cada chamada
da API. Ela define o papel do modelo: quem ele é, o que o jogo é, quais as restrições de
comprimento, quais tokens de engine não devem ser tocados, quais convenções pt-BR se aplicam
(gênero gramatical, registro de personagem, controle de spoiler). Sem essa instrução de papel,
o modelo responderia como assistente genérico — com registro neutro e sem consciência dos
contratos do jogo.

**Custo e cache:** a Doutrina é o bloco mais longo do prompt e é estática entre cenas. Por isso
ela é enviada com `cache_control` — o SDK a cobra uma vez e reutiliza o cache nas chamadas
seguintes. Em um capítulo de 10 cenas, ela é processada uma vez, não dez.

---

## Instruction tuning via prompt — o context_pack

Instruction tuning via prompt significa formular comandos altamente explícitos sobre conteúdo,
estilo, restrições e formato da saída, sem alterar os pesos do modelo. Em vez de pedir "traduza
isso", o prompt define exatamente o corpus, a saída esperada, o schema JSON, os limites de
token por linha e o que fazer se encontrar um token desconhecido.

**No framework:** o `context_pack` monta o bloco de instrução específico de cada cena. Ele não
manda o histórico inteiro da conversa — manda só o que aquela cena precisa: as linhas a traduzir,
as entradas de TM relevantes, os termos de KB vinculados aos personagens presentes, os perfis de
voz e o schema de saída esperado. Isso mantém o contexto em O(cena), não O(histórico), o que
elimina estouro de sessão e mantém o custo previsível.

O `scene_prompt.md` gerado pelo backend `in-session` é um exemplo concreto: é um arquivo
autocontido que o operador abre numa sessão limpa do chat e responde. Como o contexto é pequeno
e estruturado, um modelo menor resolve sem acumular ruído de conversas anteriores.

**Aprendizado de produção:** descobrimos que um aviso de charset no prompt fazia o modelo remover
acentos do campo `t` canônico. Adicionamos a instrução explícita: "escreva `t` com acentos; a
transliteração ASCII é responsabilidade do módulo de reinserção". Um exemplo de instruction
tuning resolvendo o que parecia ser um bug de modelo.

---

## RAG — recuperação aumentada por geração

RAG combina uma LLM com uma fonte externa de conhecimento para reduzir a dependência exclusiva
do que ficou armazenado nos pesos do modelo. Sem recuperação externa, perguntas sobre termos de
lore, nomes próprios ou convenções do jogo tendem a gerar invenções — o modelo "acha que sabe"
em vez de consultar o que foi decidido.

**No framework, RAG tem duas camadas:**

**Camada 1 — TM (Translation Memory) determinística.** Antes de traduzir qualquer linha, o
pipeline consulta a base de traduções já aprovadas. Se a linha é idêntica a uma entrada anterior,
a tradução é reutilizada diretamente (score 1.0). Se é similar, a TM é injetada no prompt como
sugestão. O modelo não inventa o que já foi decidido — ele herda.

**Camada 2 — KB (Knowledge Base) semântica.** Termos de lore, nomes de lugares e convenções
de voz são indexados com embeddings (`sentence-transformers`). Na montagem do context_pack,
o retriever busca as entradas semanticamente próximas às linhas da cena e as injeta no prompt.
Uma consulta sobre "o ritual de lamentação" recupera a entrada de KB sobre o termo, mesmo que
as palavras exatas não coincidam. Em testes, variações semânticas chegaram a score 0.944.

A diferença para o RAG clássico: aqui a base não é a web nem documentos corporativos, mas o
corpus curado da própria obra — personagens, glossário, decisões de tradução. Isso aumenta
controle: a resposta depende de fontes escolhidas pelo pipeline, não de um universo aberto.

---

## Fine-tuning — por que não usamos

Fine-tuning ajusta os pesos do modelo em dados específicos do domínio, produzindo um modelo
especializado que segue padrões sem precisar de instrução explícita. É útil quando o volume
de exemplos é grande e o comportamento alvo é estável.

**No framework, a escolha foi prompt-only** por três razões:

1. **Auditabilidade.** Qualquer comportamento da IA pode ser rastreado até uma instrução
   explícita no prompt. Com fine-tuning, o comportamento emerge dos pesos — difícil de inspecionar
   e corrigir cirurgicamente.

2. **Portabilidade.** O mesmo framework roda com Sonnet, Opus ou Haiku trocando uma string.
   Um modelo afinado seria específico de um fornecedor e de uma versão — custo alto de migração.

3. **Volume insuficiente.** Cada jogo tem entre 10 000 e 50 000 linhas, e parte significativa
   é cobertura por TM (reuso). A quantidade de pares novos raramente justifica o custo de um
   ciclo de fine-tuning.

A estratégia equivalente aqui é curar a TM e a KB com cuidado: quanto mais preciso o contexto
recuperado, menos o modelo precisa "adivinhar" — e o resultado se aproxima do que fine-tuning
produziria, com a vantagem de ser inspecionável e portável.

---

## Resumo — qual técnica resolve o quê

| Técnica | Onde aparece no framework | Por quê |
|---|---|---|
| Chain-of-thought | Back-translation (Opus + thinking) | Verificar ambiguidade e voz em linhas de alto risco |
| Role-based prompting | Doutrina / Carta no `system` | Definir papel, registro e contratos do jogo |
| Instruction tuning | context_pack + scene_prompt.md | Contexto limitado, schema explícito, restrições por linha |
| RAG determinístico | TM — exact/fuzzy match | Reutilizar traduções aprovadas sem reinventar |
| RAG semântico | KB — embeddings por cena | Recuperar terminologia de lore por significado, não por palavra |
| Fine-tuning | — | Não usado; prompt-only por auditabilidade e portabilidade |

Para os detalhes de implementação da camada de modelo: [`MODEL_INTERFACE.md`](MODEL_INTERFACE.md).
Para como o contexto é montado por cena: [`TRANSLATION_PIPELINE.md`](TRANSLATION_PIPELINE.md).
