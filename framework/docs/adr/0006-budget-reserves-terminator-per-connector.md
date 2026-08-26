# ADR 0006 — Reserva do byte de terminador no byte_budget, por conector

**Status:** aceito · **Data:** 2026-08-26

## Contexto

`trails_sky_sc` cena `mp0010_01`: após a correção de métrica por charset ([[0005]]), a escalação de
budget (`run_scene.py::_fitting_loop`, 3 tiers de tolerância) ainda deixava 65/447 linhas em
overflow no round-trip real contra o `.pac`. Investigação (agente Explore, read-only) achou duas
causas distintas:

- **56/65 (86%) — off-by-one, não é problema de tradução.** `extract.py` grava `byte_budget =
  len(bytes) + 1`, reservando 1 byte pro terminador `\0`. O oráculo real (`verify_chapter.py`)
  exige `len(encoded) + 1 <= budget`. Mas toda a família `model.py::_budget_len`/`_over_budget`/
  `_budget_note`/`over_budget_offsets` (e o texto do prompt em `context_pack.py`) tratava
  `encoded == budget` como cabendo — nunca reservava esse byte. Essas 56 linhas terminavam a
  escalação exatamente no limite errado e só falhavam no round-trip real.
- 9/65 (14%) — overflow genuíno (fora de escopo desta ADR; resolvido por retighten manual/dirigido).

A reserva do terminador **não é universal**: `bof4`/`trails_sky_sc` reservam fisicamente o byte no
CSV (docstring de `extract.py` confirma); `utawarerumono` grava `byte_budget` **sem** reserva
(`reinsert.py::build_output` confere `len(enc) > budget`, sem +1, e zera o terminador depois do
budget); `souldiers` não usa `byte_budget` (`length_constraints.mode: "none"`). Uma correção
genérica em `_budget_len`/`_over_budget` que sempre subtraísse 1 quebraria `utawarerumono` (passaria
a marcar como overflow linhas que cabem de verdade lá).

## Decisão

Novo campo `budget_reserves_terminator` em `project.json` (bloco `connector`), no mesmo padrão de
`target_charset_supported` — lido por `context_pack.project_constraints()` e propagado no dict `pc`
por toda a fonte única de `model.py`. Default `False` quando ausente (zero mudança de comportamento
para quem não seta).

- `_over_budget(t, budget, pc, tol)`: quando `pc["budget_reserves_terminator"]` é `True`, o limiar
  usável passa a ser `(budget - 1) * tol` em vez de `budget * tol` — casa exatamente com o oráculo
  real (`encoded + 1 <= budget`) quando `tol == 1.0`.
- `_budget_note`: acrescenta à métrica exibida ao LLM que o `byte_budget` já reserva 1 byte, pra o
  retry entender o motivo do corte pedido.
- `render_prompt`: acrescenta aviso equivalente na seção "DISCIPLINA DE ORÇAMENTO" do prompt.
- `budget_reserves_terminator: true` setado em `breath_of_fire_4`, `trails_sky_sc`,
  `translation_local`, `translation_software` (os 4 conectores cujo `extract.py` reserva o byte
  fisicamente — `translation_local`/`translation_software` reusam o `extract.py` do bof4). Não
  setado em `utawarerumono`/`souldiers` (ficam no default `False`, comportamento correto pra eles).

## Consequências

- (+) `trails_sky_sc` para de promover no pipeline traduções que estouram o round-trip real por 1
  byte — validado end-to-end em `mp0010_01` (re-extração completa após patch do Steam, remap +
  tradução das linhas órfãs, round-trip real: `{"ok": true, "n_fails": 0}`).
- (+) `bof4`/`translation_local`/`translation_software` ganham a mesma correção (mesmo bug
  estrutural, mesmo `extract.py`), sem trabalho extra.
- (+) `utawarerumono`/`souldiers` mantêm comportamento anterior byte-a-byte — sem regressão
  (`test_over_budget_reserves_terminator_when_flagged` cobre o caso ligado; suíte completa de
  `test_model.py`/`test_context_pack.py`/`test_run_scene.py`/`test_runtime.py`, 201 testes, segue
  passando sem editar nenhum teste pré-existente).
- (−) mais um campo booleano por-conector pra manter sincronizado com a realidade do `extract.py`
  daquele conector — mitigado por viver ao lado de `target_charset_supported` no mesmo bloco
  `connector`, com o mesmo padrão de leitura defensiva (`.get(..., False)`).
- Fora de escopo: as 9 linhas de overflow genuíno (resolvidas manualmente, não por mudança de
  arquitetura), truncamento em fronteira de palavra, e resíduo/relocação pro conector do Trails Sky
  (candidatos registrados em `ROADMAP.md`, não implementados).
