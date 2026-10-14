# CLAUDE.md — translation-cognition-framework

## Ferramentas de reverse engineering (uso automático, sem pedir permissão)

- Kaitai Struct (Web IDE ide.kaitai.io ou compiler local) + ImHex: ao iniciar Fase 0 de descoberta de conector novo (formato binário desconhecido), antes de escrever extract.py à mão.
- Hypothesis: ao escrever/revisar test_roundtrip_synthetic.py de qualquer conector.
- Diff binário: sempre que um teste de round-trip falhar, antes de debugar no código — diff em script (original × saída) apontando o offset da primeira diferença e o tamanho dos dois arquivos. O vbindiff é TUI interativa (o agente não opera): fica como opção do usuário, com o comando pronto `VBinDiff <original> <saida>`.
- binwalk: primeiro passo ao receber arquivo binário de jogo desconhecido.
- GARbro: ao identificar jogo novo de engine de visual novel conhecida.
- FModel: se o jogo novo for Unreal Engine (.pak/.uasset).
- UndertaleModTool: se o jogo novo for GameMaker (data.win).
- UABEA: companion do UnityPy quando ele não parsear uma versão nova do Unity.

Nunca usar fora do contexto de bring-up/debug de conector — apoio à fase de descoberta, não dependência de pipeline em produção.

## GitHub Project #4 — regras de campo

Sempre que uma issue receber a label `bug`, setar também `Prioridade=P0` no Project #4 na mesma ação
(campo Prioridade: P0/P2/P2.5/P4). Vale tanto para issue nova quanto pra relabeling de existente.

## Nunca commitar — conteúdo de jogo e dado pessoal

O repo é público e contém só o framework. Antes de qualquer `git add`/`commit`, vale a regra de
`.claude/hooks/content_guard.py` (hook local + job `Guard` da CI — bloqueou = resolver, não contornar):

- **Nunca versionar:** binário de jogo (original ou remontado: `source_dat/`, `output/`, `manual_tests/`,
  `.dat/.sdat/.pak/.exe`…), roteiro extraído e tradução de cena (`dialogs.csv`, `translations_*.json`,
  `approved_*.csv`, `translation_memory.jsonl`, `_build_translations.py`, `bench_*.json`), planilha de
  revisão (`qa_revisao/para_revisar|devolvido/`, `review_*.csv`, `.xlsx`), print/imagem do jogo, worklist
  gerada (`kb_phase_worklist_<cap>.md` — traz trechos de fala), texto bruto de fonte (`research_cache/`),
  `.env`, nota `*.local.md`.
- **Nunca escrever em arquivo versionado:** saída de descompilador (Ghidra/IDA: `FUN_…`, `DAT_…`, listagem
  de assembly do executável), fala do jogo além de citação curta e pontual, cópia literal de wiki, chave de
  API, e-mail pessoal. Nota de RE do executável fica fora do repo.
- **Commit sempre com o e-mail noreply do GitHub** (`git config user.email`), nunca o pessoal.
- **`projects/*/artifacts/` é default-deny:** só é versionado o que está em `ARTIFACTS_ALLOWED` no guard.
  Arquivo gerado novo nasce bloqueado; se cita texto do jogo, vai pro `.gitignore`; se não cita, libera-se
  na allowlist depois de conferir o conteúdo. Extensão nova também é allowlist — adicionar só com motivo.
- Issue, PR e mensagem de commit são públicos: mesma regra (sem fala do jogo, sem inventário de risco).

## Processo — seguir rigidamente, sem pular passo

Os processos deste projeto (fases do pipeline, gates, skills, ordem dos passos de cada ROADMAP) são
seguidos à risca, na ordem, sem atalho.

- Nunca usar flag de bypass (`--skip-connector-gate`, `--skip-kb-gate`, `--no-back` e equivalentes)
  nem contornar um gate por outro caminho. Gate bloqueou = resolver a causa, não pular.
- Nunca avançar para o passo seguinte com o anterior incompleto (ex.: escalar tradução sem
  back-translation e gate visual do piloto fechados).
- Se um passo parecer desnecessário ou impossível de cumprir, parar e perguntar ao usuário — a decisão
  de pular é só dele, explícita e caso a caso.

## Sessão — contexto e medição de custo

- Nunca rodar nem sugerir `/compact` manual: a compactação é a automática.
- Virada de fase = `/clear`. Antes dele, atualizar a seção "Retomada" do ROADMAP do projeto; depois dele, o
  primeiro comando é `python framework/runtime/session_usage.py mark <projeto> <fase>`.
- Ao fechar uma fase, avisar o usuário que é hora do `/clear` (quem digita é ele).
- Detalhe e motivo em `docs/TRANSLATION_PIPELINE.md` ("Sessão: contexto e medição de custo").

## Sessão — só ferramenta do projeto ligada

Servidor MCP, conector do claude.ai ou plugin sem relação com o projeto não fica ligado aqui: cada um entra
no contexto de toda requisição (nomes de ferramenta + instruções), mesmo sem uso.

- `.claude/settings.json` já desliga os conectores do claude.ai (`disableClaudeAiConnectors`) e nega os
  servidores listados em `deniedMcpServers`. Servidor novo na máquina que não serve ao projeto: acrescentar
  o nome ali, na mesma ação.
- Nunca remover essas chaves nem ligar um servidor "só para testar" sem pedido explícito do usuário.
- Integração com o Chrome não tem chave de projeto: abrir a sessão com `claude --no-chrome`.
- Conferir: `/mcp` na sessão tem de vir vazio.

## Sessão — modelo

- A janela principal roda em **Sonnet** (`"model": "sonnet"` em `.claude/settings.json`), igual ao tradutor
  do caminho de API. Não trocar o padrão do projeto sem pedido explícito do usuário.
- Opus só quando o usuário trocar à mão (`/model opus`), para bring-up de conector ou diagnóstico difícil;
  ao terminar, voltar para Sonnet.
- Subagentes seguem o próprio arquivo: `scene-translator` em Sonnet, retrotradução em Opus.
