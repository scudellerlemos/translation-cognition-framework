# Diagramas — C4 do pipeline e do patcher

Visão por níveis do modelo C4 (contexto, contêineres, componentes) mais um fluxo de sequência e um de estados.
Feitos a partir do código e de [`ARCHITECTURE.md`](ARCHITECTURE.md), [`SDD_RUNTIME.md`](../framework/SDD_RUNTIME.md)
e de `framework/distribution/`. Estão em `flowchart` do Mermaid (a sintaxe `C4*` do Mermaid ainda é experimental e
renderiza mal no GitHub). Nenhum diagrama traz fala de jogo.

## 1. Pipeline de tradução

### Fluxo de ponta a ponta (hoje)

```
═══════════════════ A. PREPARAÇÃO (uma vez por projeto) ═══════════════════

 jogo ─► 00 extração (conector) ──► dialogs.csv + byte_budget
              │                      gate: round-trip extract→reinsert idêntico
              ▼
         [HITL] humano aceita o ESCOPO ──► [HITL] humano escolhe o CAMINHO
              │                                   (sessão ou API; um só por projeto)
              ▼
         01 entidades/tom ─► 02 resolução ─► 03 KB (pesquisa IA+humano)
              │                                   gate: kb_gate (reconciled)
              ▼
         04 glossário + 04b decision_log ─► 05 plano ─► 05b corpus sintético
              │
              ▼
         PILOTO: poucas cenas ─► instala ─► humano confere no jogo
              └── só escala se o piloto fechar (retrotradução + gate visual)

══════════════ B. LAÇO POR CENA / ONDA (repete até tudo `verified`) ═══════════

   escolha do caminho (hitl.choose-path)
        │
        ├── API ────────► run_chapter (lote, Sonnet pelo código, só diálogo)
        └── SESSÃO ─────► wave.py / session_lot.py (subagente Sonnet na sessão)
                                    │
   ┌────────────────────────────────▼─────────────────────────────────────┐
   │ run_scene  (job resumível; checkpoint em run_state.json)              │
   │                                                                      │
   │ [0] GATES ──► connector_gate + kb_gate ... bloqueia antes de modelo  │
   │ [1] context_pack ──► scene_prompt.md (glossário, voz, TM, falas)     │
   │ [2] TRADUZ (IA) ──► translations_<cena>.json                         │
   │       └ antes: scene_dedup (texto repetido traduz 1 vez)             │
   │ [3] build_plan ──► cobertura, tokens, orçamento de bytes             │
   │ [4] verify_chapter ──► round-trip byte a byte (resíduo = 0)          │
   │ [5] retrotradução (IA) ──► por fala, risco alto + 5% amostra         │
   │ [6] checkpoint ──► `verified`; TM e banco crescem                    │
   │                                                                      │
   │ pula cena `verified` sem fala tocada (touched.py; --full força)      │
   └──────────────────────────────────────────────────────────────────────┘
        │ na onda, depois: glossary_lint ─► quality_gate ─► cost/obs_report
        │                      │
        │        06b micro-QA: reprovou ─► correção cirúrgica ─► revalida
        │                      │
        │        fila de escalonamento (ambiguidade) ─► HUMANO decide
        ▼
   a cada 10 cenas: amostra de 15 falas para o humano (aviso, não bloqueia)

══════════════════════ C. FECHAMENTO ══════════════════════════════════════

   triagem de risco (juiz barato; paga) ─► sobe falas suspeitas p/ `high`
        ▼
   07 amostra de qualidade (200 pares) ─► humano marca ok/erro ─► taxa + IC 95%
        ▼
   08 reinserção (determinística) ─► 08b texto de sistema e rótulos em imagem
        ▼
   instalação ─► 08c teste no jogo (print do humano ─► causa raiz)
        ▼
   09 distribuição: delta + patcher .exe de um clique ─► release (só com aval)

══════════════════════════ RETORNOS ════════════════════════════════════════

   07 achou erro ─────┐
   08c achou no jogo ─┼──► 06b corrige SÓ as falas tocadas ──► volta ao laço B
   glossário mudou ───┘    (cenas viram `stale` ─► re-QA)

 Em todo o fluxo: nenhum gate tem bypass; a IA nunca escreve byte nem ponteiro.
```

Quem decide: humano em escopo, caminho, escalonamento, amostra de qualidade, print do jogo e release; o resto é
gate automático. O bloco B é o que o benchmark do caminho de sessão vai medir nos dois caminhos
(`benchmark_sessao/`).

### Skills: três blocos e dois retornos

As skills `00..09` são lidas em ordem, mas executadas em três blocos; o laço do meio repete por cena.

```mermaid
flowchart LR
  subgraph A["A. Preparação (uma vez)"]
    s0["00 extração"] --> s1["01–03 entidades, tom, KB"] --> s4["04 glossário<br/>04b decisões"] --> s5["05 plano<br/>05b corpus sintético"]
  end
  subgraph B["B. Laço por cena/onda"]
    s6["06 tradução<br/>(api ou sessão)"] --> s6b["06b micro-QA<br/>e correção cirúrgica"]
  end
  subgraph C["C. Fechamento"]
    s7["07 amostra de qualidade"] --> s8["08 reinserção<br/>08b texto de sistema"] --> s8c["08c teste no jogo"] --> s9["09 distribuição"]
  end
  A -->|gates: connector_gate, kb_gate, HITL| B
  B -->|cenas verified| C
  s7 -.->|erro achado: só as falas tocadas| s6b
  s8c -.->|print: causa raiz| s6b
  s4 -.->|glossário ou doutrina mudou: stale, re-QA| B
```

### Nível 1 — Contexto

```mermaid
flowchart LR
  op(["Operador<br/>Felipe: decide, ratifica, julga amostra"])
  rev(["Revisor humano<br/>planilha e página de revisão"])
  fw["translation-cognition-framework<br/>extrai, traduz, valida e reinsere o texto de um jogo"]
  claude["Claude Code<br/>sessão: a IA da sessão traduz"]
  api["API da Anthropic<br/>caminho de API"]
  jogo[("Arquivos do jogo<br/>binários originais, só leitura")]
  op --> fw
  fw --> rev
  rev --> fw
  fw <--> claude
  fw <--> api
  jogo --> fw
  fw --> jogo2[("Arquivos remontados<br/>entrega ao jogador")]
```

### Nível 2 — Contêineres

```mermaid
flowchart TB
  subgraph repo["Repositório"]
    skills["skills/ 00–09<br/>o processo (Markdown)"]
    runtime["runtime/<br/>orquestração determinística + interface de modelo (Python)"]
    connectors["connectors/ + projects/&lt;obra&gt;/connector/<br/>extração e reinserção do formato"]
    validation["validation/<br/>gates, custo, naturalidade"]
    dist["distribution/<br/>pacote, patcher, .exe"]
  end
  subgraph inst["projects/&lt;obra&gt;/ (instância)"]
    pj["project.json<br/>manifesto"]
    art[("artifacts/<br/>estado externo: run_state, TM, glossário, ledger")]
  end
  ia{{"IA: Claude<br/>sessão ou API"}}
  skills --> runtime
  pj --> runtime
  runtime --> connectors
  runtime --> validation
  runtime <--> ia
  runtime <--> art
  connectors --> dist
  classDef aiNode fill:#f6d6e8,stroke:#c0397b,color:#000;
  class ia aiNode;
```

### Nível 3 — Componentes do `runtime/` (uma cena)

```mermaid
flowchart TB
  rs["run_scene / run_chapter / run_game<br/>orquestra e grava checkpoint"]
  cg["connector_gate + kb_gate<br/>bloqueiam antes de qualquer modelo"]
  cp["context_pack<br/>pacote limitado: doutrina, glossário, voz, TM, falas"]
  tr{{"model.translate<br/>IA"}}
  bp["build_plan_chapter<br/>cobertura, tokens, orçamento de bytes"]
  vf["verify_chapter<br/>round-trip byte a byte"]
  bt{{"back_translate<br/>IA, só risco alto"}}
  si["state_index<br/>TM, voice cards, decisões"]
  ob["cost_report / obs_report / session_usage<br/>custo e tempo"]
  st[("run_state.json<br/>api_ledger.jsonl")]
  rs --> cg --> cp --> tr --> bp --> vf --> bt --> si
  rs <--> st
  si --> cp
  rs -.-> ob
  ob --> st
  classDef ia fill:#f6d6e8,stroke:#c0397b,color:#000;
  class tr,bt ia;
```

Ondas do caminho de sessão: `wave.py` encadeia `run_scene`, `scene_dedup`, `glossary_lint`, `quality_gate`,
`cost_report` e `obs_report` num comando só. `session_lot.py` monta o prompt de várias cenas.

### Sequência — uma cena no caminho de sessão

```mermaid
sequenceDiagram
  autonumber
  participant O as Operador
  participant W as Janela principal
  participant S as Subagente scene-translator
  participant R as run_scene
  participant C as Conector
  O->>W: dispara a onda
  W->>S: cena(s) do lote
  S->>R: run_scene (backend in-session)
  R->>R: gates e context_pack
  R-->>S: AGUARDANDO tradução (scene_prompt.md)
  S->>S: escreve translations_cena.json
  S->>R: run_scene de novo
  R->>C: build_plan e verify_chapter
  C-->>R: exit 0 (round-trip igual)
  R-->>S: AGUARDANDO back-translation (se risco alto)
  S->>R: run_scene de novo
  R->>R: checkpoint verified, state_index
  R-->>W: uma linha de status
```

## 2. Patcher de distribuição

### Nível 1 — Contexto

```mermaid
flowchart LR
  dev(["Mantenedor<br/>gera e publica o patch"])
  jog(["Jogador<br/>roda o .exe"])
  patch["Patcher<br/>aplica a tradução nos arquivos do jogo, com desinstalar"]
  steam["Steam<br/>instala e atualiza o jogo"]
  gh["GitHub Releases<br/>hospeda o .exe (só com aval)"]
  dev --> patch
  patch --> gh
  jog --> gh
  jog --> patch
  patch <--> steam
```

### Nível 2 — Contêineres

```mermaid
flowchart LR
  subgraph build["Máquina do mantenedor (Python)"]
    bp["build_package.py<br/>deltas bsdiff + manifest.json + arte"]
    be["build_exe.py<br/>PyInstaller embute o pacote"]
  end
  pkg[("dist/ do pacote<br/>manifest.json, deltas/*.bsdiff, arte, ícone")]
  exe["Patch_&lt;obra&gt;.exe<br/>patcher.py + pacote embutido"]
  subgraph pc["PC do jogador (sem Python)"]
    jogo[("Pasta DAT do jogo<br/>arquivos + .bak")]
  end
  src[("source_dat + output/<br/>originais e remontados")] --> bp --> pkg --> be --> exe
  exe --> jogo
```

### Nível 3 — Componentes do `patcher.py`

```mermaid
flowchart TB
  main["main / gui<br/>escolhe o comando e a pasta do jogo"]
  aj["achar_jogo / resolver_pasta<br/>biblioteca Steam ou --jogo"]
  ab["jogo_aberto<br/>tasklist: bloqueia se o jogo roda"]
  es["estado(arquivo)<br/>ausente, original, traduzido, desconhecido (por SHA-256)"]
  ins["instalar<br/>backup .bak, bsdiff.patch, confere hash, troca atômica"]
  des["desinstalar<br/>restaura o .bak validado por hash"]
  ver["verificar<br/>conta os estados"]
  man[("manifest.json<br/>hashes e identidade do jogo")]
  main --> aj
  main --> ins
  main --> des
  main --> ver
  ins --> ab
  des --> ab
  ins --> es
  des --> es
  ver --> es
  man --> es
```

### Sequência — instalar

```mermaid
sequenceDiagram
  autonumber
  participant J as Jogador
  participant P as patcher.exe
  participant F as Pasta do jogo
  J->>P: abre o .exe (instalar)
  P->>P: lê manifest.json
  P->>F: jogo está aberto?
  F-->>P: não
  P->>F: SHA-256 de cada arquivo
  alt algum arquivo desconhecido
    P-->>J: nada foi alterado, use verificar arquivos da Steam
  else todos original ou traduzido
    loop cada arquivo original
      P->>F: copia para .bak (se preciso)
      P->>P: bsdiff.patch em memória
      P->>P: confere SHA-256 final
      P->>F: troca o arquivo (.novo para o nome final)
    end
    alt falha no meio
      P->>F: restaura os já trocados a partir do .bak
      P-->>J: falha, estado original mantido
    else tudo certo
      P-->>J: tradução instalada
    end
  end
```

### Estados de cada arquivo

```mermaid
stateDiagram-v2
  [*] --> ausente: arquivo não existe
  [*] --> original: SHA = sha_original
  [*] --> traduzido: SHA = sha_final
  [*] --> desconhecido: qualquer outro SHA
  original --> traduzido: instalar
  traduzido --> original: desinstalar (restaura o .bak)
  desconhecido --> [*]: o patcher recusa e não altera nada
  ausente --> [*]: o patcher recusa e não altera nada
```
