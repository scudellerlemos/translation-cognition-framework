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
- **Arquivo gerado novo que cita texto do jogo:** entra no `.gitignore` e em `DENIED_PATHS` do guard no mesmo
  PR que o cria. Extensão nova é allowlist no guard — adicionar só com motivo.
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
