# ADR 0011 — Governança de gates de CI: oráculo vs knob, meta-gate, preflight e mutation testing

**Status:** proposto · **Data:** 2026-09-06

## Contexto

O CI (`test.yml`, `quality.yml`, `api-smoke.yml`) cresceu reativamente em cima do que foi
produzido: cada lacuna virou um job novo depois do fato (schema — ADR 0010; abort/fallback do
batch — commit `0509230`; achados de code-review — commit `e688f80`). Isso deu uma suíte robusta,
mas com um buraco estrutural: nada distingue "o gate está errado" de "o código está errado" quando
um check falha. Na prática, a mesma sessão que escreveu o código também pode afrouxar o teste, o
`pytest`, ou o próprio `.github/workflows/*.yml` pra ficar verde — silenciosamente, sem deixar
rastro do porquê.

O padrão certo pra fechar esse buraco já existe no repo, só que aplicado a outro escopo: o
drift-check de `sync-prd.yml` (allowlist/denylist de arquivo publicado no PRD) falha o job se um
arquivo novo não está classificado explicitamente. Esta ADR generaliza esse padrão pros próprios
gates de qualidade/teste.

Estado atual (bom, não mexer): round-trip byte-idêntico com fixture sintética
(`test_roundtrip_synthetic.py`), enum de `risk_level` (ADR 0010), citação obrigatória de fonte no
KB (`kb_review.py --gate`), ledger de custo (I4, `GOVERNANCE.md`), coverage 90% com
`precision=2` (achado real — sem isso, 89.97% passava arredondado), mypy/ruff/bandit/gitleaks/
pip-audit, `api-smoke.yml` em cron sem custo obrigatório, `merge-gate` com approval manual.

Lacunas identificadas:
1. Nenhum controle impede *afrouxar* um knob (threshold de coverage caindo, escopo do mypy
   encolhendo, severidade do bandit relaxando, skip/xfail novo, o próprio YAML de CI) sem que isso
   fique visível como tal — só *fortalecer* um knob (ex.: `mypy.ini` ganhando arquivo novo,
   commit `e688f80`) é inofensivo e não deveria disparar a mesma fricção.
2. `validate.py` valida os campos obrigatórios de `translation_plan_<scene_id>.json` com tupla
   hardcoded solta (`validate.py:138,162`), separada da prosa em `framework/schemas/*.md` que se
   declara "fonte de verdade" — as duas podem divergir em silêncio (mesma classe do achado "docs
   stale" do commit `e688f80`). O enum de risco já foi deduplicado pra `connector_io.RISK_LEVELS`
   no mesmo commit; os campos obrigatórios, não.
3. Não existe um teste E2E sintético do pipeline completo (extract→plan→apply→verify) por
   conector — só round-trip isolado.
4. Não existe preflight bloqueante de custo: uma corrida de capítulo caro pode falhar no meio por
   causa externa (API key inválida, binário do jogo ausente) depois de já ter gasto dinheiro.
5. Coverage 90% audita linha executada, não se o teste de fato assere alguma coisa — gameável com
   teste tautológico.

## Risco aceito (exemplo concreto, não hipotético)

Nem toda lacuna de oráculo é uma lacuna esquecida — às vezes é uma decisão consciente de
custo-benefício, e essa distinção precisa ficar registrada em algum lugar em vez de virar dúvida
recorrente em toda auditoria futura. Caso real: o conector Souldiers (`projects/souldiers/`) usa
bundles Unity Addressables (UnityFS) via UnityPy, uma lib que só *lê* bundles existentes —
`SerializedFile.__init__`/`BundleFile.__init__` exigem um `EndianBinaryReader` de bytes já
existentes, sem API pra construir um bundle do zero. Isso torna inviável (sem reimplementar o
formato UnityFS à mão) o padrão de fixture sintética que BoF4/Utawarerumono usam pros próprios
formatos binários (bespoke, simples, parseados 100% por código do próprio projeto). Decisão: o
oráculo de round-trip byte-idêntico do container continua rodando só localmente
(`test_roundtrip.py`, exige `--data-dir` com o jogo instalado, `pytest.skip` na CI); a CI cobre
sempre a lógica que É código nosso e onde bugs reais aconteceriam (reescrita do CSV interno,
`test_rebuild_table_logic.py`) — a serialização do container em si é responsabilidade do UnityPy,
não nosso código. Ver `projects/souldiers/README.md` para o detalhamento.

## Decisão (faseada)

### Fase 1 — Meta-gate (oráculo vs knob)

Classificar todo check numa de duas categorias:

| Classe | Exemplos | Regra |
|---|---|---|
| **Oráculo** (fato externo, não deriva do código sob teste) | round-trip, enum de `risk_level`, citação de fonte no KB, "sem work-text em `.py`" | Nunca se ajusta pra passar — se falhou, o código está errado. |
| **Knob** (parâmetro governável) | `setup.cfg` (`[coverage:*]` thresholds/omit/exclude_lines), `mypy.ini` (escopo `files=`), `pyproject.toml` (`[tool.bandit]` severity), `.github/workflows/*.yml`, `.pre-commit-config.yaml`, skip/xfail em `conftest.py`/testes | Pode mudar, mas só com ADR novo no mesmo PR — mesmo padrão já usado nos ADR 0009/0010. |

Implementação:
- Novo job `gate-drift` (mesmo bash-pattern do drift-check de `sync-prd.yml`, adaptado): compara o
  diff do PR contra a lista de knob-files e busca sinal de **enfraquecimento** — número em
  `--cov-fail-under`/`severity-level` caindo, linha removida de `files=`/`source=`, `skip`/`xfail`/
  `pragma: no cover` novo. Não é hard-fail (heurística de diff é sujeita a falso-negativo/positivo);
  sai como **anotação no PR** ("knob X ficou mais frouxo — ADR?"), pra forçar visibilidade, não pra
  ser um segundo juiz automático. Fortalecimento de knob (arquivo/linha nova, threshold subindo)
  não dispara nada.
- Regra nova em `CLAUDE.md` (projeto): gate vermelho → ação padrão é corrigir a fonte. Editar
  teste/CI/threshold pra fazer passar (afrouxando) exige sinalizar explicitamente ao humano ANTES
  de aplicar, e idealmente vem acompanhado de ADR — nunca silencioso na mesma tentativa de ficar
  verde. Quem trava de verdade é o approval humano do `merge-gate`; a anotação do CI só garante que
  o afrouxamento não passe despercebido no diff.

### Fase 2 — Contrato declarativo + preflight

- `translation_plan_<scene_id>.json`: hoje os campos obrigatórios vivem em tupla hardcoded solta
  dentro de `validate.py` (`("offset", "text_source", "speaker", "risk_level",
  "base_translation")`), separada da prosa em `framework/schemas/artifacts_schema.md`. Em vez de
  introduzir jsonschema/pydantic (dependência nova, e contraria a decisão já tomada em
  `config.py:236-239` — `validate_connector_types` evita essas libs de propósito), estender o
  **mesmo padrão já em uso**: um `TypedDict` pro schema da linha de plano + `get_type_hints()` pra
  introspecção, igual `ConnectorConfig`/`validate_connector_types`. Um único lugar tipado que
  `validate.py` introspecciona, em vez de tupla duplicada — dedup no mesmo espírito do
  `RISK_LEVELS` (commit `e688f80`).
- `doctor.py` novo (`framework/runtime/`): preflight bloqueante chamado no início de
  `run_chapter.py` antes de qualquer chamada cobrada — API key presente e respondendo (reusa
  `batch_smoke.py`), binário do jogo presente, git working tree limpo, DB acessível. Aborta antes
  de gastar, não depois.

### Fase 3 — E2E sintético + auditoria do teste

- Um teste E2E sintético por família de conector (extract→plan→apply→verify, tudo em memória via
  fixture, sem depender do binário comercial) — job novo obrigatório em `test.yml`.
- Mutation testing (`mutmut`) em cron semanal, mesmo padrão do `api-smoke.yml`: relatório de
  mutantes sobreviventes não bloqueia push (caro em tempo de runner), mas expõe teste tautológico
  que só executa linha sem assertar comportamento.

## Consequências

- (+) Fecha o self-bias: afrouxamento de gate fica anotado no PR em vez de passar despercebido
  dentro de uma sessão sob pressão de ficar verde — sem criar fricção nos fortalecimentos (que
  continuam livres, como sempre foram).
- (+) Campos obrigatórios do plano viram um `TypedDict` introspeccionável (mesmo padrão de
  `ConnectorConfig`), não tupla duplicada que diverge em silêncio da prosa em
  `framework/schemas/*.md` — sem dependência nova (jsonschema/pydantic seguem de fora, como já
  decidido em `config.py`).
- (+) Preflight evita gasto de API em corrida fadada a falhar por causa externa.
- (+) Mutation testing audita a suíte de teste em si, fechando a lacuna que coverage % não cobre.
- (−) Mais um job de CI (`gate-drift`, barato — só `git diff` + heurística de texto, sem custo de
  API; anotação, não bloqueio — falso-positivo/negativo é aceitável porque não trava merge sozinho).
- (−) Mais um cron semanal (`mutmut`, custo de tempo de runner, não de API — mesmo perfil do
  `api-smoke.yml`).
- Fora de escopo desta ADR (decidir na implementação de cada fase): heurística exata de
  "enfraquecimento" do `gate-drift` (regex por knob-file); threshold de mutation score pra virar
  sinal acionável; se `doctor.py` é CLI separada ou flag de `run_chapter.py`; lista definitiva de
  knob-files da Fase 1 (a tabela acima é o ponto de partida, não exaustiva).
