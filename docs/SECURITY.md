# Security — Translation Cognition Framework

> Threat model e controles de segurança do harness. Última revisão: 2026-07-03.

---

## Perfil de uso

Ferramenta de desenvolvedor individual, operada localmente. Não é um serviço web, não processa
dados de usuários, não tem múltiplos operadores concorrentes. O perfil de ameaça é
correspondentemente restrito.

---

## Ativos críticos

| Ativo | Risco se comprometido |
|---|---|
| Chave de API Anthropic (`.env`) | Custo financeiro ilimitado; acesso a modelos via conta do operador |
| Binários do jogo (`*.sdat`, `*.dat`) | Material com copyright; vazamento viola licença do jogo |
| Artefatos de tradução (`artifacts/`) | Perda de trabalho; retradução custosa |
| Scripts de conector (`connector/*.py`) | Execução de código arbitrário se adulterado |

---

## Superfície de ataque e controles

### 1. Chave de API

**Ameaça:** chave vazada para repositório git → uso não autorizado com custo financeiro.

**Controles:**
- `.env` explicitamente em `.gitignore` (com comentário de aviso)
- `.env.example` commitado em vez do `.env` real
- CI verifica (`git ls-files --error-unmatch .env`) que `.env` não está rastreado
- `_load_dotenv` em `llm_client.py` carrega da variável de ambiente ou `.env` local

**Gap residual:** sem processo de rotação de chave; sem detecção de chave em `git log`.

---

### 2. Path traversal

**Ameaça:** argumento `scene` malformado (`../etc/passwd`) acessando arquivos fora de `artifacts/`.

**Controles:**
- `_validate_scene_arg` em `run_scene.py` verifica que o path resolvido está sob `artifacts/`
- `_connector_script` verifica que o script do conector está sob o diretório do projeto
- Testes: `test_run_scene_rejects_path_traversal_scene`, `test_connector_sandbox_blocks_external_path`

---

### 3. Execução de scripts de conector

**Ameaça:** script de conector adulterado executa código arbitrário quando o pipeline roda.

**Controles:**
- Scripts rodam em subprocess isolado com timeout (300s)
- `connector_hash` (SHA1 dos scripts) gravado no `run_state.json` após cada verify bem-sucedido
- `_warn_if_connector_stale` emite aviso se o hash mudou desde o último verify
- Path do script verificado contra o diretório do projeto antes de executar
- `connector_gate.py` bloqueia a tradução se os scripts obrigatórios (build_plan/verify) não
  existirem no disco, ou se nenhum round-trip verde já foi registrado — nenhum conector incompleto
  chega perto de dado real
- `coverage_gate.py` (dry-run de cobertura do candidato de engine desconhecida) carrega o candidato
  via `importlib` **no mesmo processo** (sem subprocess) para inspecionar `iter_string_offsets`/
  `decode_string`/`load_table` — risco de execução de código não confiável ACEITO
  deliberadamente: o candidato é sempre um arquivo que o próprio operador está prestes a copiar
  para `projects/<jogo>/connector/` e rodar de qualquer forma via `connector_smoke.py`/round-trip
  depois; `coverage_gate` só antecipa essa execução para uma etapa anterior, não introduz uma
  superfície nova

**Gap residual:** sem verificação de integridade ANTES da primeira execução (apenas auditoria
posterior via hash); sem assinatura de código. Aceitável para uso pessoal/mono-operador.

---

### 4. Binários do jogo

**Ameaça:** arquivo `.sdat`/`.dat` malformado causa comportamento inesperado no conector.

**Controles:**
- `*.sdat` em `.gitignore` (nunca versionado)
- `game_dat_dir` nunca persistido em `project.json` (passado via CLI)
- Round-trip gate (byte-idêntico): rejeita qualquer modificação que altere bytes não traduzidos

**Gap residual:** parsing de binário arbitrário (heurística + ASCII%) sem fuzzing formal.

---

### 5. Dependências (supply chain)

**Controles atuais:**
- `requirements-dev.txt` com versões compatíveis fixas (`~=`)
- `pip-audit` roda em `quality.yml` (job `deps`) — CVEs em `requirements-dev`
- `dependabot.yml` configurado — PRs automáticos de atualização de dependência
- `gitleaks` roda em `quality.yml` (job `secrets`) — segredo commitado no diff + histórico

**Gap residual:**
- Sem hashes de integridade (`pip-compile --generate-hashes`)
- Aceitável para ferramenta pessoal; hashes de integridade só justificam o custo se o projeto
  evoluir para uso compartilhado

---

## O que este projeto NÃO é

- Não é um serviço web → não há OWASP top 10, CORS, injeção de SQL
- Não processa dados de usuários → não há LGPD/GDPR, PII, compliance de dados
- Não tem múltiplos operadores → não há autenticação, autorização, multi-tenancy

---

## Resposta a incidentes

| Incidente | Ação imediata |
|---|---|
| Chave de API vazada para git | `git filter-repo` para remover do histórico; revogar e rotacionar chave na console Anthropic |
| Binário do jogo commitado | `git rm --cached` + `git filter-repo`; verificar se foi para remoto |
| Script de conector adulterado | Comparar com backup/git history; não executar até verificar; resetar `connector_hash` no `run_state.json` |
