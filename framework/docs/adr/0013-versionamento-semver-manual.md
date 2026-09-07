# ADR 0013 — Versionamento SemVer decidido manualmente, sem ferramenta de release

**Status:** aceito · **Data:** 2026-09-06

## Contexto

`release.yml` (ADR 0012) automatiza a *publicação* de uma versão (`validate-release` confere que
`VERSION` bate com a tag; `publish-release` cria a GitHub Release) mas não decide *qual* número vem a
seguir — isso ficou implícito, sem registro. Na prática, quem escolhe é sempre a mesma pessoa (dev
solo) no momento de editar `VERSION` e taguear, e a pergunta "por que esse número e não outro" não
tinha resposta documentada.

Existem ferramentas que automatizam essa escolha a partir de commits (`conventional commits` +
`semantic-release`/`release-please`): um `fix:` vira patch, `feat:` vira minor, `BREAKING CHANGE:` no
corpo vira major, tudo calculado do histórico de commits. Adotar isso exigiria: (a) disciplina de
prefixar 100% dos commits num formato fixo, algo que este repo nunca fez (mensagens em português,
livres, ver `git log`), e (b) mais uma ferramenta/dependência de CI pra um projeto de 1 pessoa onde a
pergunta "o que mudou desde a última tag" já tem resposta de sobra em `gh release create
--generate-notes` (lista de PRs). O ganho de automatizar não paga o custo de adaptar todo o histórico
de commits a um formato novo.

## Decisão

**Versionamento SemVer (`MAJOR.MINOR.PATCH`) decidido manualmente por quem tagueia, no momento de
taguear — sem ferramenta, sem enforcement de formato de commit.** Regra de bolso pra decidir o
número, registrada aqui pra não depender de memória:

- **PATCH** (`x.y.Z+1`) — mudança que não afeta o *comportamento observável* do framework por quem o
  usa (conector, runtime, validação): CI/CD, docs, ADR, refactor interno, correção de bug que não
  muda contrato.
- **MINOR** (`x.Y+1.0`) — adiciona algo novo sem quebrar o que já existe: um conector novo, um formato
  de saída novo, um parâmetro novo com default que preserva o comportamento anterior.
- **MAJOR** (`X+1.0.0`) — quebra compatibilidade: alguém rodando uma versão anterior do framework
  contra o mesmo artefato/config precisaria mudar algo pra continuar funcionando (schema de scene
  incompatível, remoção/rename de CLI flag, mudança de contrato de conector).

`validate-release` continua conferindo só o **oráculo objetivo** (`VERSION` bate com a tag) — a
*escolha* do número é julgamento humano, não uma regra que a CI valida ou deriva.

## Consequências

- (+) Zero ferramenta nova, zero disciplina de commit message pra manter — decisão fica documentada
  aqui, não presa na cabeça de quem tagueia.
- (+) Compatível com o estilo de commit já existente no repo (mensagens livres em português).
- (−) Nada impede um erro de julgamento (chamar de patch algo que era minor) — não há gate automático
  pra isso. Aceito conscientemente: o custo de errar um número de versão num projeto solo é baixo
  (renomear a tag antes de anunciar, se pego a tempo), o custo de automatizar (reescrever histórico de
  commits, manter tooling) não se paga.
- Fora de escopo: adotar conventional commits/semantic-release no futuro, se o projeto ganhar mais de
  um committer e a disciplina de mensagem deixar de ser um custo relativo alto.
