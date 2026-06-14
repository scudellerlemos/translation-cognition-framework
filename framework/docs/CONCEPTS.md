# Conceitos — explicados para quem está aprendendo engenharia de IA

> Este doc ensina **os conceitos**, não o código. Público: alguém confortável com engenharia de
> software/dados, mas novo nas decisões de *engenharia de IA*. Cada conceito segue o mesmo molde:
> **o problema → a solução → por que importa em IA**. Para o panorama, volte ao
> [`README`](../../README.md); para o porquê medido, veja [`ARCHITECTURE.md`](ARCHITECTURE.md).

A tese do projeto em uma frase: **a LLM é cara, esquecida e estocástica — então use-a só onde IA é
insubstituível e faça todo o resto com código determinístico, testável e barato.** Tudo abaixo é
consequência disso.

---

## 1. Scene as Stateless Job (cena = job sem estado)

**O problema.** O jeito ingênuo de traduzir um jogo com LLM é um chat longo: "traduza a cena 1… agora
a 2… agora a 3…". A cada turno, o histórico inteiro vai junto. O contexto cresce **O(histórico)** — na
cena 200 você reenvia 199 cenas. Isso estoura a janela do modelo, fica caro e imprevisível, e quando
falha você perde tudo.

**A solução.** Cada cena vira um **job isolado**, como uma função pura: recebe um pacote de contexto,
devolve a tradução, e **não guarda memória** entre execuções. O contexto é **O(cena)** — constante,
não importa se é a cena 2 ou a 2000. O que precisa ser lembrado de cenas anteriores não fica na cabeça
do modelo; vem do **estado externalizado** (conceito 3).

**Por que importa em IA.** Custo previsível (cada cena custa ~o mesmo), escala linear, e
**resumibilidade**: cair na cena 40 não invalida as 39 já feitas (um *checkpoint* em disco marca o
progresso). É a diferença entre "um chatbot que às vezes funciona" e "um pipeline de produção".

> No código: `runtime/run_scene.py` (orquestra 1 cena) + `run_chapter.py` (loop de cenas, resumível).

---

## 2. Context Pack (pacote de contexto)

**O problema.** Se a cena é isolada, como o modelo sabe que "Ukon" já foi traduzido de tal jeito, ou
que tal personagem fala formal? Mandar *tudo* (glossário inteiro + todas as fichas + lore) a cada cena
volta ao problema do custo. Mandar *nada* produz tradução inconsistente.

**A solução.** Um passo **determinístico** monta, por cena, o **pacote mínimo**: a doutrina fixa
(cacheável) + só os termos de glossário que aparecem ali + só as fichas de voz dos personagens que
falam + as linhas a traduzir + dicas de tamanho. É **exatamente o que o LLM vê — e nada além**. Isso é
*context engineering*: a qualidade da saída é função do que entra, então a montagem do contexto é
tratada como engenharia, não como acaso.

**Por que importa em IA.** O *Context Pack* é a peça central: equilibra **custo** (pacote pequeno),
**qualidade** (contexto certo) e **cacheabilidade** (a parte fixa é cobrada ~1×). É também o que torna
o sistema auditável — você pode abrir o `pack.json` de qualquer cena e ver precisamente o que o modelo
recebeu.

> No código: `runtime/context_pack.py` → gera `scene_prompt.md` + `pack.json` por cena.

---

## 3. Estado externalizado (a memória que o chat não tem)

**O problema.** Um LLM não tem memória entre chamadas — e mesmo dentro de uma sessão, a "memória" é só
o texto na janela, que é caro e some quando a sessão acaba. Consistência ao longo de 45 mil linhas não
pode depender disso.

**A solução.** A memória do sistema vive **em arquivos versionados**, fora do modelo:
- **Translation Memory (TM)** — toda tradução já decidida, reusável de graça (conceito 4).
- **Glossário** — termos canônicos e como tratá-los.
- **Voice Cards** — fichas de voz por personagem (registro, tiques, léxico).
- **Decision Index** — decisões não-óbvias e seu porquê.

O passo de cena **lê** desse estado (via Context Pack) e **escreve** de volta (a cada cena nova, a TM
cresce). O modelo nunca "lembra" — ele *consulta*.

**Por que importa em IA.** Consistência vira propriedade do **store**, não da sorte do modelo. Sem
banco de dados, sem embeddings, sem segundo serviço pago — só arquivos `.json`/`.csv`/`.jsonl` que você
versiona no git, faz diff e reconstrói. É RAG levado ao osso: recuperação determinística de estado
curado, em vez de busca vetorial aproximada.

> No código: `runtime/state_index.py` materializa `artifacts/state/` (idempotente, reconstruível).

---

## 4. Translation Memory como "coração"

**O problema.** Depois que um humano revisa e corrige a tradução, você **não** quer re-rodar o jogo
inteiro na IA (caro, e re-introduz variação). E a mesma frase aparece dezenas de vezes — pagar para
traduzir cada repetição é desperdício.

**A solução.** A **TM** é um banco *append-only* (`translation_memory.jsonl`): linha idêntica já
traduzida → reusa **de graça** (zero chamada de IA). Correção do revisor → entra na TM e se propaga.
Por isso a TM é o "coração": o jogo é processado pela IA **uma vez**; depois disso, tudo é reuso e
correção cirúrgica.

**Por que importa em IA.** É a alavanca de custo nº 1 (dedup) **e** o backbone de consistência (a mesma
decisão, em todo lugar). Mostra um princípio geral: **cache semântico de decisões** vale mais que
re-inferência.

---

## 5. Runtime agnóstico ao modelo

**O problema.** Modelos mudam (versões novas, preços, capacidades). Se a lógica do pipeline estiver
amarrada a um modelo específico, cada troca é uma reescrita — e você não consegue usar o modelo *certo
para cada tarefa*.

**A solução.** Existe **uma única fronteira** com o LLM (`runtime/model.py`). O resto do sistema não
sabe qual modelo roda. Isso permite **tiering**: linha simples → modelo barato (Haiku); cena multi-linha
→ intermediário (Sonnet); verificação de alto risco → o melhor (Opus). Trocar ou reescalonar é
**configuração**, não refatoração.

**Por que importa em IA.** Desacoplar a lógica do provedor/modelo é o equivalente, em IA, de programar
contra uma interface e não contra uma implementação. Dá portabilidade, controle de custo por tarefa, e
imunidade a "o modelo X foi descontinuado".

> Detalhe do contrato: [`MODEL_INTERFACE.md`](MODEL_INTERFACE.md).

---

## 6. SDD — Specification-Driven Development

**O problema.** "Traduzir bem" é subjetivo e fácil de perder: decisões tomadas no meio de um chat
somem, ninguém sabe *por que* tal termo foi escolhido, e não dá para checar se a tradução respeita as
regras.

**A solução.** As regras viram **especificações versionadas e checáveis**, produzidas por **etapas
explícitas** (`00..08`): descobrir entidades → reconciliar conhecimento → fixar glossário → planejar →
traduzir → revisar → reinserir. Cada etapa **lê** os artefatos da anterior, **produz** os seus, e tem
um **gate de entrada** que impede rodar fora de ordem ou sobre base incompleta. A "spec" (glossário,
vozes, spoilers) é um artefato de primeira classe, não um comentário perdido.

**Por que importa em IA.** Transforma um prompt artesanal num **processo reproduzível e auditável**. É
o que separa "pedi pro ChatGPT traduzir" de "tenho um pipeline cujas decisões eu consigo justificar,
versionar e re-executar". O "spec-driven" é a aplicação, à IA, da velha lição de engenharia: torne o
implícito explícito.

> As etapas vivem em `framework/skills/00..08` (prosa) + `framework/runtime/` (executável).

---

## 7. Gates explícitos & o laço propõe→aprova→aplica

**O problema.** A IA é **estocástica**: às vezes inventa, encurta demais, vaza um spoiler, quebra um
token de formatação. Se a saída do modelo vai direto para o dado final, um erro silencioso vira um bug
permanente.

**A solução.** A IA nunca tem a palavra final. Ela **propõe** (num arquivo de proposta); **gates
determinísticos aprovam** — round-trip byte-idêntico, back-translation, fonte de KB, spoiler,
naturalidade; e só então um **script aplica** no dado canônico. Gate vermelho **trava** o pipeline.

**Por que importa em IA.** É *defense-in-depth* para sistemas estocásticos: você cerca a parte
imprevisível com verificações previsíveis. O veredito é sempre de uma peça determinística e
reproduzível, então um erro do modelo esbarra num portão em vez de virar dado ruim. Detalhe e desenhos
em [`GOVERNANCE.md`](GOVERNANCE.md).

---

## 8. O "reproduzível com asterisco" (uma sutileza importante)

Cuidado com uma confusão comum: **o pipeline é determinístico; a tradução não é.** Re-rodar uma cena
**não** produz os mesmos bytes de tradução (o LLM é estocástico). O que é reproduzível é **a
orquestração + os gates**: dado um `translations_*.json` fixo, a montagem de contexto, o plano, o
round-trip e a reinserção rodam idênticos toda vez. Em outras palavras: **o veredito é reproduzível; a
geração, não.** Por isso o artefato caro/estocástico (a tradução) é versionado no git, e os derivados
determinísticos são regeneráveis. Não confunda "pipeline determinístico" com "tradução determinística".

---

## Como os conceitos se encaixam (as 4 camadas)

| Camada | Conceitos que a sustentam |
|---|---|
| **① Cognition** | #5 runtime agnóstico ao modelo · #8 o que é (e não é) reproduzível |
| **② State** | #3 estado externalizado · #4 TM como coração |
| **③ Execution** | #1 scene as stateless job · #2 context pack |
| **④ Validation** | #6 SDD (gates de etapa) · #7 gates + propõe→aprova→aplica |

Leia agora [`ARCHITECTURE.md`](ARCHITECTURE.md) (o porquê medido) e [`GOVERNANCE.md`](GOVERNANCE.md)
(quem decide o quê). Para vocabulário rápido, o glossário está no [`README`](../../README.md#glossário-leia-antes-de-mergulhar).
