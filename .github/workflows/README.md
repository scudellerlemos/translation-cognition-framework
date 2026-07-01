# CI/CD — o que roda sozinho neste repositório

> **Em uma frase:** toda vez que o código é enviado para o GitHub, alguns "robôs"
> conferem o código automaticamente. Se está tudo certo fica 🟢 **verde**; se algo
> quebrou fica 🔴 **vermelho** — assim ninguém sobe código com problema sem perceber.

Esses robôs são os **workflows**: cada arquivo `.yml` nesta pasta é um robô com uma
missão. Eles aparecem na aba **Actions** do GitHub.

---

## Visão geral

| Workflow | Arquivo | Quando roda | Pergunta que responde |
|---|---|---|---|
| **Tests** | `test.yml` | Todo push e PR | "O código **funciona**?" |
| **Quality** | `quality.yml` | Todo push e PR | "O código está **limpo e seguro**?" |
| **API Smoke** | `api-smoke.yml` | Domingo de manhã + manual | "A **API da Anthropic** ainda responde?" |

> **Vocabulário mínimo:** *push* = enviar código pro GitHub · *PR (pull request)* =
> pedido pra juntar uma branch na principal · *workflow* = um robô · *job* = uma
> tarefa dentro do robô · *step* = um passo dentro da tarefa.

---

## 1. `test.yml` — "O código funciona?"

Roda a bateria de **testes automatizados** do projeto. Para garantir que funciona em
mais de uma versão do Python, ele roda **duas vezes em paralelo**: uma no Python 3.11
e outra no 3.12 (é a "matriz").

Passo a passo, em português:

1. **Baixa o código** e instala o Python + as ferramentas (`requirements-dev.txt`).
2. **Confere que o `.env` não foi enviado** — o `.env` guarda senhas/chaves e *nunca*
   pode ir pro repositório. Se alguém mandou sem querer, o robô barra.
3. **Checa os tipos (mypy)** — pega erros de "encaixe" (ex.: passar texto onde se
   esperava número) antes mesmo de rodar o programa.
4. **Roda os testes do motor (runtime) com cobertura** — além de passar, exige que pelo
   menos **60%** do código seja exercitado pelos testes (a "cobertura"). Abaixo disso,
   barra.
5. **Roda os testes de validação** — as regras de qualidade do harness.
6. **Roda os testes de contrato dos conectores** (um por jogo) — confere o
   *round-trip*: extrair o texto do jogo e reinserir **sem traduzir** tem que devolver o
   arquivo **byte a byte idêntico** ao original. É a prova de que o conector não corrompe
   o jogo. (Sem o arquivo do jogo, que não vai pro repositório, esses testes se "pulam"
   sozinhos.)

---

## 2. `quality.yml` — "O código está limpo e seguro?"

São **4 conferências independentes** (jobs) que rodam ao mesmo tempo. Cada uma olha um
aspecto diferente:

| Job | Ferramenta | O que faz (em miúdos) |
|---|---|---|
| **Lint** | `ruff` | Revisor de estilo e erros bobos: import que ninguém usa, variável esquecida, etc. |
| **SAST** | `bandit` | Detetive de segurança: procura padrões perigosos no próprio código. |
| **Secret scan** | `gitleaks` | Procura senha/chave/token esquecidos no código ou no histórico. |
| **Dependências** | `pip-audit` | Confere se alguma biblioteca usada tem falha de segurança conhecida (CVE). |

> O **Lint** e o **SAST** olham só a pasta `framework/` (o "produto" reaproveitável). Os
> scripts soltos dentro de `projects/*/connector/` são experimentais e já têm os testes
> de round-trip como rede de segurança, então não entram nesse gate.

---

## 3. `api-smoke.yml` — "A API da Anthropic ainda responde?"

Um teste **opcional** que faz uma chamada **de verdade** na API (custa ~US$ 0,002) só
para ver se ela ainda responde como esperado — útil para detectar mudanças que quebrem o
fluxo antes de começar a traduzir um capítulo novo.

- **Não roda** a cada push (custaria dinheiro à toa). Só **todo domingo de manhã**
  (agendado) ou quando alguém **manda rodar na mão**.
- Precisa do segredo `ANTHROPIC_API_KEY` configurado no repositório.
- **Se a chave não existir, ele pula** (fica verde, com um aviso) em vez de dar erro.
  Para ativá-lo de verdade: *Settings → Secrets and variables → Actions → New secret*.

---

## Como ler o resultado (aba Actions)

- 🟢 **verde** = passou tudo. 🔴 **vermelho** = algo falhou — clique no run e depois no
  passo vermelho para ver a mensagem.
- O **título** de cada execução é a **mensagem do commit** que a disparou (não descreve o
  workflow). Quem descreve o que roda são os **nomes dos jobs** (ex.: *"Lint (ruff) —
  estilo e bugs no framework"*), definidos dentro do `.yml`.

---

## Arquivos relacionados (fora desta pasta)

- **`.github/dependabot.yml`** — robô que, **toda semana**, abre PRs atualizando
  bibliotecas Python e versões de Actions que ficaram desatualizadas.
- **`.pre-commit-config.yaml`** (na raiz) — roda **as mesmas conferências no seu próprio
  PC**, na hora do `git commit`, para pegar problema cedo (antes de subir). Instalar uma
  vez com: `pip install pre-commit && pre-commit install`.

---

## Detalhe técnico: por que as Actions têm um código gigante?

Linhas como `uses: actions/checkout@9c091bb... # v7.0.0` usam um **identificador fixo
(SHA)** da ferramenta em vez de só `@v7`. É uma boa prática de segurança: garante que
estamos usando *exatamente* aquela versão revisada, e não uma futura que alguém possa
ter adulterado. O comentário `# v7.0.0` diz a versão legível, e o Dependabot mantém isso
atualizado sozinho.
