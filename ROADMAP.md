# Roadmap — Translation Cognition Framework (SDD)

> Última atualização: 2026-06-08
> Escopo: framework genérico + instância de referência Utawarerumono.
> O roadmap detalhado de decisões vive em `projects/<título>/artifacts/decision_log.md`.

---

## Onde estamos (maturidade)

| Camada | Status |
|---|---|
| Processo genérico (skills 00–08) | 🟢 maduro (~92/100) |
| Perfil de jogos | 🟢 validado |
| Instância Utawarerumono | 🟢 pipeline 00→08 em **2 cenas / 1025 linhas**, **validado in-game** (Plano B ✅); **resíduo T4=0**; QA de naturalidade/interjeições aplicada |
| Conector hex_binary | 🟢 formato mapeado; **ponteiros FILE-RELATIVOS**; **relocação INTRA-ARQUIVO + rebuild do Pack** (EOF-append reprovado in-game); **pytest** (9 testes) |
| Perfis filme/série + conector subtitle_file | 🟠/🔴 stub / não iniciado |

**Resumo:** o *processo* está maduro (~92) e a *validação de produção* foi **fechada nas 2 cenas**: o
**pt-BR renderiza no jogo real** e a relocação **intra-arquivo (Plano B)** foi validada in-game (o
EOF-append fora reprovado — `@@@@`/trava). O bloqueador de correção ("funciona no jogo?") **acabou**;
o que resta é **escala** (jogo inteiro, A3) + **economia** (A4/A5) + **qualidade contínua** (naturalidade
contextual, já incorporada ao processo).

---

## Próximos passos

### Fase A — Fechar o caminho até produção (Utawarerumono)

- [x] **A1. Gate in-game.** ✅ **VALIDADO.**
  - ✅ **pt-BR renderiza no jogo real** (in_place) — objetivo de ponta a ponta atingido (`Fasea2/3/8/9/10`).
  - ❌ **EOF-append reprovado**: linhas relocadas ao fim do CONTAINER viram `@@@@` e travam (`Fasea11`).
    Causa: o engine carrega cada arquivo num buffer do tamanho do `size` no Pack. Ver `decision_log.md`.
  - ✅ **Plano B validado in-game** (`--validate-one 0x3442`): "ERRO DE SISTEMA." (que antes era `@@@@`)
    exibiu e o jogo seguiu para a cena seguinte sem travar (`testeplanob.png`, `testeplanob_avanco.png`).
    Relocação intra-arquivo + reescrita do Pack é a estratégia correta. **Run completa liberada.**
- [x] **A2. Ordem offset × ordem narrativa.** *(resolvido p/ a abertura)* A extração agora segue a
  **ordem de armazenamento por script** (= narrativa, verificado nas cenas iniciais). Para cenas
  distantes, validar; se divergir, caminhar o bytecode por ordem de comando. Ver `decision_log.md`.

- [ ] **A3. Estratégia de JOGO INTEIRO (~30k+ linhas) — loop incremental, resumível.**
  Fazer tudo de uma vez é inviável. Separar o **determinístico** (rápido, automático) do **cognitivo**
  (gargalo) e fatiar por capítulo. Pré-requisito: **A1 verde**.
  - **Fase 1 — "Ler o jogo" (barato, sem traduzir):** `SCENES`=todos os 353 scripts → medir o tamanho
    exato; rodar Discovery+Entity sobre o corpus inteiro **uma vez** → **glossário/entidades GLOBAL**
    (termos canônicos nascem uma vez e **congelam**) + mapa de tamanho por capítulo.
  - **Fase 2 — Loop por capítulo (11→39, ~16 caps):** para cada cap.: extrair → Knowledge Building
    com **fronteira de spoiler que avança** só até o cap. atual → traduzir em **lotes de 200**
    (`translation_status.json` marca a fronteira → resumível) → micro-QA + `reinsert` + `pytest` →
    spot-check in-game a cada poucos caps. Ritmo: **1–2 capítulos por sessão**, nunca tudo de uma vez.
  - **Fase 3 — Fechamento:** passe global de **consistência de glossário** (linter determinístico) →
    `reinsert` do jogo inteiro + `pytest` + patch IPS final.
  - **Consistência em escala:** glossário congelado + voice profiles + **handoff de contexto** (últimas
    N linhas da cena anterior) + fronteira de spoiler móvel.
  - **Aceleração opcional:** tradução por cena é paralelizável (glossário/voz congelados) → candidata a
    **workflow multi-agente** (fan-out por cena + passe de consistência). Caminho caro; só sob demanda.
  - Esta é a **prova de produção** do framework. Casa com A4 (custo) e A5 (redução de custo).
- [ ] **A4. Estimativa de custo real (em $/tokens/tempo)** da run de 33k.
  Lacuna do diagnóstico: hoje só há análise arquitetural (shift-left, ~330 chamadas máx). Calcular
  custo monetário e tempo de relógio. Cabe junto da A3. **Pré-requisito da A5** (sem baseline não há
  o que reduzir).
- [ ] **A5. Analisar o custo atual e reduzir — meta: −80%** *(agressiva, pode mudar).*
  Tomar o baseline da A4 como ponto de partida e atacar os maiores ofensores de custo. Linhas de
  investigação:
  - **Modelo certo por tarefa:** usar modelo barato (ex.: Haiku) para passos mecânicos/baixo risco e
    reservar o modelo forte para linhas `risk_level ≥ high` e identidades duplas.
  - **Prompt/context caching:** reaproveitar glossário, perfil de voz e regras entre lotes em vez de
    reenviar (o glossário/voz é estável → ótimo candidato a cache).
  - **Batching e shift-left:** já existe (T1–T3 determinístico, byte_budget no prompt); medir o
    quanto realmente evita reescrita LLM e empurrar mais trabalho para o determinístico.
  - **Evitar retrabalho:** Micro-QA/06c só re-tocam o que falhou; medir taxa de reprocessamento.
  - **Triagem:** linhas de sistema/anomalias (ex.: `0x33f9`) e strings triviais podem sair do
    caminho do LLM.
  Definir a métrica ($ por 1.000 linhas) e acompanhar a redução contra a meta. A meta de 80% é alvo
  inicial — recalibrar quando houver o baseline real.

### Fase B — Evolução do motor (só DEPOIS da produção)

> Decisão estratégica: estes itens transformam o framework de "documento" em "motor executável".
> Construí-los antes da run completa = abstração prematura. Sequência recomendada (cada um habilita
> o próximo). Cada item vira uma rodada de planejamento própria quando chegar a vez.

- [x] **B1. Validation leve.** ✅ `framework/validation/validate.py` — validadores executáveis dos
  schemas + invariantes (glossary/handling_rule, cobertura plan↔dialogs↔approved, preservação de
  tokens, `risk_notes` quando `risk≥medium`, enums, `reveal_timing`). Genérico (lê `project.json`),
  ERROR/WARN, **7 testes pytest** (passa na ref + pega violações injetadas). Roda como Input Gate.
- [ ] **B2. Memory leve** (glossário + character state básico). Estado vivo e consultável entre os
  165 lotes, no lugar de re-ler CSV ad-hoc. Desenhar **informado pela run real** (A3).
- [ ] **B3. Kernel simples.** Runtime que orquestra os passos usando Validation (gates) + Memory
  (estado), no lugar de scripts ad-hoc. Compensa com repetibilidade (≥2 projetos ou re-runs).
- [ ] **B4. Skill DSL.** Forma declarativa dos passos 00–08 (hoje prosa .md) que o Kernel lê. Por
  último: só vale com 2–3 projetos e o Kernel existente (maior risco de abstração prematura).

### Fase C — Escalar para outras mídias

- [ ] **C1. Validar perfil de filmes** com projeto real (legenda/dublagem) → implementar conector
  `subtitle_file` (SRT/ASS), constraint de CPS. `framework/media-profiles/films.md` (stub).
- [ ] **C2. Validar perfil de séries** (≥2 episódios): glossário/decision_log compartilhados,
  spoiler-check cross-episódio, QA de continuidade. `framework/media-profiles/series.md` (stub).

---

### Adiado (baixa prioridade agora — fazer no momento certo)

- [x] **T4 em lote (LLM) — plumbing pronto.** `reinsert.py` exporta o resíduo irredutível para
  `artifacts/t4_residue.json` (lote pronto p/ reescrita LLM em 1 passada → volta pelo plano → reaplica).
  Hoje **inerte** (resíduo=0 com a relocação intra-arquivo); ativa sozinho se um corpus futuro gerar
  overflow não-relocável. 2 testes pytest (lote vazio no corpus + caso sintético).
- [~] **Metadados cognitivos por linha em escala (F2):** `speaker`/`tone_register`/`intent` existem
  para as 1025 linhas; **risco calibrado** (data-driven: spoiler/glossário/entidade → 9 high / 9 medium,
  saindo do achatamento 0-high) com `risk_notes`. *Resta:* o **`tone_register` fino por situação/emoção**
  das ~948 linhas `dialogo` — depende do passe contextual LLM (meia-maratona). Ver `decision_log.md`.
- ~~CI + empacotamento de release~~ — **removido** (não há release planejada agora).

---

### Backlog de qualidade de tradução (casos reais vistos in-game)

> Não quebram o jogo, mas "não fazem sentido" na leitura. Coletados de spot-checks in-game.

- [ ] **⭐ PRIORIDADE — processar até METADE do jogo (coleta de métricas).** Antes de comprometer com a
  run completa (~33k), traduzir/reinserir **incrementalmente até ~cap. 25** (metade dos 353 scripts /
  caps. 11–39) para **medir em escala** e decidir o resto com dados, não com palpite. Métricas a coletar:
  - **Custo real** ($/tokens/tempo por 1.000 linhas) — alimenta A4/A5.
  - **Qualidade/contexto:** taxa de interjeições/calques pegos pelo linter; consistência de voz da Kuon
    e dos demais em escala; quantas linhas exigem `risk` alto de verdade (hoje 0).
  - **Conector em escala:** % in_place vs RELOC; resíduo; **rótulos de falante** (o bug do opcode ≠ `50 00`);
    se a relocação intra-arquivo aguenta caps. inteiros.
  - **Governança:** validar a Carta de Governança aplicada de ponta a ponta num volume real.
  Saída: relatório de métricas que recalibra A3/A4/A5 e a Carta. Ritmo: incremental e resumível
  (`translation_status.json`), 1–2 caps. por sessão. **Não fazer a 2ª metade até revisar essas métricas.**

- [ ] **Carta de Governança de Tradução (diretrizes que a IA SEGUE).** Formalizar num doc do framework
  (ex.: `framework/skills/translation_governance.md`) o contrato de qualidade — a IA traduz **conforme
  a carta**, não improvisa fora dela. Estrutura por contexto:
  - **Personagem (voz):** toda linha respeita o perfil de voz do falante (`tone_analysis.md`: registro,
    léxico, comprimento, tiques); `voice_criticality: high` → checagem por linha; identidade dupla nunca
    vaza a identidade revelada antes do `reveal_timing`; o personagem soa igual em todo o corpus.
  - **Mundo (lore):** glossário/`handling_rule` respeitados; formas exatas sem variação; spoilers só
    após `reveal_timing`; honoríficos e registro formal/informal conforme a relação no mundo.
  - **Situação (cena/emoção):** traduzir pela **intenção/emoção** da cena (susto, dor, comédia,
    solenidade), não pela letra; interjeições localizadas; junção de linhas quebradas soa natural;
    âncora obrigatória — *"uma pessoa lê isto nesta situação e entende com naturalidade?"*.
  - **Processo:** metadados por linha **reais** (speaker, situação/`tone_register`, risco) — não
    auto-default, pois são o que dirige a QA contextual; risco calibrado (identidade dupla, comédia,
    1ª menção de lore, spoiler = alto → **back-translation obrigatória**); IA **propõe** → humano
    **aprova** → script **aplica**; decisões não-óbvias no `decision_log.md`.
- [ ] **Governança de tradução — linter determinístico (genérico, sem LLM).** A ideia: um passe
  automático que **sinaliza** linhas suspeitas antes da aprovação, pegando o que a amostragem não pega:
  - interjeição/linha curta **idêntica ao source** (`base==source`) fora da whitelist (gritos de vogais, nomes);
  - **fragmentos do idioma-fonte** que sobraram (ex.: `U...`, `Wh-`, `Hm`, `-ing`) no alvo;
  - **rótulos de falante** (UI) ainda no idioma-fonte;
  - alvo == source em linha não-trivial.
  Sai um relatório (`naturalness_lint.json`) que vira input do 06c. Barato, roda sempre, complementa a
  revisão contextual humana/LLM do 06b/07.
- [ ] **Stammers/hesitações residuais.** Ex.: `0x3640` `"U... Urgh... Everything's... distorted..."` →
  `"U... Argh... Está tudo... distorcido..."` — o `"U..."` solto não foi localizado (deveria virar
  `"Ugh..."`/`"Nh..."` ou fundir). Estender a localização de interjeições para **stammers iniciais**.
- [ ] **Rótulo de falante "Girl" aparece em inglês in-game** apesar de `approved="Garota"`
  (`0x36a0`/`0xa98e`/`0xe1da` estão extraídos e traduzidos). Hipótese: o **rótulo é referenciado por um
  opcode ≠ `50 00`**, então o repoint (que só reescreve `50 00`) deixa o label apontando para os bytes
  originais. **Investigar** o opcode de rótulo de falante e incluí-lo no repoint. (Bug técnico do conector.)
- [ ] **Atribuição de speaker vs. rótulo do jogo:** a linha do casamento (`0x395f`/`0x398f`) está como
  `speaker: "Mulher (memória)"` no plano, mas o jogo rotula "Girl/Garota" — reconciliar a metadata.

---

## Já concluído (para referência)

- ✅ Framework SDD genérico (camadas: processo / perfil / conector / instância).
- ✅ Conector hex_binary: container `.sdat` mapeado (header `Filename`/`Pack`, 353 scripts; texto UTF-8
  contíguo por script).
- ✅ **Modelo de ponteiro corrigido para FILE-RELATIVO** (`50 00` + uint32 relativo ao início do
  arquivo) — descoberta que invalidou o modelo absoluto anterior. Ver `decision_log.md`.
- ✅ **Primeiro pt-BR do framework renderizado no jogo real** (Steam) — prova de ponta a ponta. `Fasea*.png`.
- ✅ **Plano B no conector:** relocação **intra-arquivo** + `rebuild_container` (reescreve a tabela Pack,
  padding a 16 bytes) — substitui o EOF-append reprovado in-game. 1025 linhas: T1=595, RELOC=430,
  resíduo 0; 425/425 ponteiros relocados resolvem dentro do arquivo; 9 testes pytest verdes.
- ✅ **Plano B validado in-game** (`--validate-one`): linha relocada intra-arquivo exibe e o jogo segue
  (`testeplanob.png`/`testeplanob_avanco.png`) — bloqueador "funciona no jogo?" encerrado.
- ✅ **QA de naturalidade contextual + interjeições:** regra genérica no framework (06/06b/07/games) +
  referência curada do projeto; 19 interjeições localizadas (`Nh?→Hein?`, `Ngh...→Nnh...`, `Gah!→Ai!`).
- ✅ Charset: gate FALHOU (fonte sem diacríticos → `@`); resolvido por **transliteração na gravação**.
- ✅ Round-trip byte-idêntico + patch IPS + **teste de regressão `pytest` (9 testes: modelo file-relativo
  não-circular, relocação within-file, integridade do Pack, governança)**.
- ✅ Extração **por arco/script** (`SCENES`) com limpeza de bordas; container totalmente parseado.
- ✅ Pipeline cognitivo 00→08 rodado de verdade em **2 cenas / 1025 linhas** (entities, glossário,
  research_log com gate de cobrança, plano, micro-QA, QA, approved, reinsert).
- ✅ `.gitignore` para não versionar `.sdat` (assets com copyright).
