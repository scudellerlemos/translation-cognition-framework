# ADR 0012 — Esteira em repo único: `main` governada, release por tag, poda de branches

**Status:** aceito · **Data:** 2026-09-06

## Contexto

Este repositório (`translation-cognition-framework`) sempre foi tratado, na cabeça do projeto,
como "HML" — um par com um segundo repositório `prd-translation-cognition-framework` ("PRD"),
alimentado por `sync-prd.yml`: a cada push em `main`, um snapshot curado (allowlist/denylist de
arquivo) era squash-commitado no PRD, escondendo `.claude/`, `CLAUDE.md`, as ADRs e os dirs de POC
(`translation_local`/`translation_software`) de quem visitasse o link público do portfólio.

Ao revisar essa separação, confirmou-se (`gh repo view`) que **este repo já é público**
(`visibility: PUBLIC`). Isso muda o cálculo: a curadoria do PRD nunca escondeu nada que já não
estivesse acessível publicamente neste repo — o ganho real era só estético (não mostrar tooling
interno no link do portfólio), não segurança. O conteúdo genuinamente sensível (dump de diálogo de
jogo comercial: `dialogs.csv`, `translation_plan*.json`, `translation_memory.jsonl` etc.) nunca
dependeu da separação de repo — sempre ficou de fora via `.gitignore`, e continua assim.

Decisão do projeto: não vale manter 2 repos, 1 secret cross-repo (`PRD_REPO_TOKEN`) e 1 job de
drift-check só por preferência estética de curadoria. Consolidar em 1 repo só.

## Decisão

- **1 repo só.** `sync-prd.yml` é removido; o repo `prd-translation-cognition-framework` fica órfão
  (arquivamento é limpeza manual futura, fora desta ADR).
- **`main` é a única branch governada.** Branch protection (PR obrigatório, status checks de
  `quality.yml`/`test.yml`, sem push direto/force-push) + `environment: Production` (approval
  manual) — mesmo gate que já existia para o `merge-gate`. Branches de feature continuam livres,
  sem gate, sem approval — é o espaço de trabalho.
- **`environment: Production` passa a exigir branch/tag correspondente** (`deployment_branch_policy`
  restrito a protected branches + tags `v*.*.*`) — hoje está `null` (qualquer ref pode disparar um
  job gated), o que não faz sentido pra um ambiente chamado "Production".
- **Release imutável por tag** (`release.yml`, novo): `git tag vX.Y.Z` dispara validação de que
  `VERSION` bate com a tag e `CHANGELOG.md` tem a seção da versão, depois cria uma GitHub Release
  neste mesmo repo (job gated por `environment: Production`, mesmo padrão do `merge-gate`). A
  validação VERSION/CHANGELOG é um **oráculo** no vocabulário da ADR 0011 (fato objetivo sobre o
  estado do repo, não um parâmetro ajustável).
- **Poda semanal de branches** (`branch-hygiene.yml`, novo): cron semanal remove branches já
  mergeadas em `main` além das 50 mais recentes (ordenadas por atividade), nunca toca branch não
  integrada. Primeira execução em modo dry-run antes de habilitar remoção real.

Esta ADR cobre a camada de **topologia de repo/branch/release**. A camada de **gates de
CI/qualidade** continua descrita pela ADR 0011 (`0011-ci-gate-governance-oraculo-vs-knob.md`,
status `proposto`) e roda igual em qualquer branch via `quality.yml`/`test.yml` — as duas ADRs
descrevem a mesma esteira, em camadas diferentes.

## Consequências

- (+) Uma fonte de verdade só: sem sync cross-repo, sem secret cross-repo, sem job de drift-check
  allow/deny pra manter.
- (+) `main` passa a ser protegida de fato (branch protection real), não só "gate de aprovação
  dentro do workflow" — fecha o gap concreto do `deployment_branch_policy: null`.
- (+) Release vira um evento rastreável (tag + GitHub Release), não um número em `VERSION` mantido
  só de memória.
- (−) O link público do portfólio passa a mostrar `.claude/`, `CLAUDE.md`, ADRs internas e dirs de
  POC — aceito conscientemente (sem ganho de segurança em escondê-los, já que o repo é público de
  qualquer forma).
- (−) Poda automática de branch é uma ação destrutiva rodando sem revisão a cada semana — mitigado
  por dry-run obrigatório na primeira execução e por só tocar branches já mergeadas (nunca
  trabalho não integrado).
- Fora de escopo (decidir na implementação): arquivamento efetivo do repo PRD; remoção do secret
  `PRD_REPO_TOKEN`/variável `PRD_REPO` (ação manual em Settings, não versionada).

## Atualização (2026-09-06): `release.yml`/`VERSION` removidos

Decisão revertida: `release.yml` e o arquivo `VERSION` foram removidos. "Release" é um conceito de
software versionado com consumidor externo baixando um artefato — não se aplica a um projeto de
tradução (o entregável é o corpus traduzido em `artifacts/scenes/`, não um pacote instalável).
Manter o mecanismo era governança emprestada de outro tipo de projeto sem propósito real aqui.

Isso também fecha, por eliminação, o motivo original do `deployment_branch_policy: null` do
`environment: Production`: a incompatibilidade vinha de dois consumidores com necessidade de
política diferente compartilhando o mesmo environment (`merge-gate`, ref de PR-merge, vs.
`publish-release`, padrão de tag). Com `publish-release` fora, sobra só o `merge-gate` — e ali
`deployment_branch_policy` seguir `null` deixa de ser um gap: job disparado por PR roda contra
`refs/pull/<PR>/merge`, uma ref que nunca corresponde a nome de branch/tag, então nenhuma política
de branch conseguiria restringi-lo de qualquer forma. O controle real ali sempre foi o approval
manual (`required_reviewers`), que continua ativo.

## Atualização (2026-09-06, parte 2): release volta, mas com motivo e desenho diferentes

Segunda reversão da mesma decisão, por um motivo diferente do que a derrubou: este repo não é só o
corpus de tradução, é um **framework reutilizável** — o README já versiona proveniência de
doutrina/prompt por artefato (`doctrine_hash`, `skills_revision`), mas nunca versionou o *código do
framework* em si. Sem tag, não há como responder "essa tradução foi feita com qual versão do
framework" se um bug for encontrado depois. `release.yml` e `VERSION` voltam.

Ao mesmo tempo, ficou claro que o `merge-gate` original (aprovação manual em `environment:
Production` antes de **todo** merge em `main`) era teatro pra dev solo: sempre a mesma pessoa
aprovando o próprio PR, sem checar nada que o botão "Merge pull request" já não force. Esse job
perde a aprovação manual e vira só um agregador automático (`all-checks`) — a aprovação manual de
verdade migra pra onde faz sentido: `publish-release`, evento raro e deliberado.

Isso também permite fechar o `deployment_branch_policy` de verdade, não por eliminação como da
primeira vez: em vez de 1 environment com 2 consumidores incompatíveis, agora são **2 environments,
cada um com exatamente 1 consumidor**:
- `Staging` — marcador automático (sem aprovação) de qual SHA de `main` está validado; policy
  restrita a protected branches.
- `Production` — só `publish-release` (padrão de tag `v*.*.*`); continua com aprovação manual, agora
  aplicada a um evento que realmente vale a pena parar pra confirmar.

`CHANGELOG.md` continua cronológico sem número de versão (decisão anterior, não revertida) —
`validate-release` confere só `VERSION == tag`; as notas da Release usam `gh release
create --generate-notes` (lista de PRs desde a última tag, gerada pelo próprio GitHub) em vez de
extrair uma seção do CHANGELOG.
