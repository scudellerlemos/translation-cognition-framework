#!/usr/bin/env python3
"""
scaffold_project.py — Inicializa artefatos KB de um novo projeto com schemas corretos.

Gera os arquivos que state_index.build() e context_pack esperam, com o formato certo
desde o início — elimina iterações de "schema errado descoberto tarde" (~10k tokens/jogo).

Uso:
  python scaffold_project.py <project_root>
  python scaffold_project.py <project_root> --title "Título do Jogo"

Não sobrescreve arquivos existentes (skip seguro).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

# Colunas obrigatórias: context_pack.select_glossary() usa 'term', 'target_translation',
# 'handling_rule'. 'updated_date' e exigida pelo kb_gate.py (bloqueia sem ela) — faltava aqui
# e so foi descoberta quando um projeto scaffoldado (Souldiers) chegou no gate sem a coluna.
_GLOSSARY_HEADERS = [
    "term", "category", "target_translation", "handling_rule",
    "spoiler_level", "aliases", "notes", "updated_date",
]

_TONE_ANALYSIS_TEMPLATE = """\
# Tone Analysis — {title}

## Tom geral do jogo

[Descrever o tom geral: gênero narrativo, atmosfera, tipo de humor, ritmo de leitura esperado.]

## Espectro de registros

| Personagem | Registro | Referência PT-BR |
|---|---|---|
| PersonagemA | formal-solene | Sem contrações, sintaxe formal |
| PersonagemB | coloquial informal | Contrações permitidas |

## Perfis de voz

<!-- FORMATO OBRIGATÓRIO: ### Nome — `voice_criticality: high|medium|low`         -->
<!-- sem esse inline, state_index.build_voice_cards() retorna 0 cards              -->
<!-- aliases: usar / entre nomes alternativos (ex: "### Valkirie/Valkyrie/Valquíria") -->

### PersonagemA — `voice_criticality: high`
- **Registro:** (ex: formal-solene, proclamação ritual)
- **Características:** (ex: sem contrações; sintaxe formal; fala como decreto)
- **Red flags:** (ex: soar coloquial; usar "você" casual)

### PersonagemB — `voice_criticality: medium`
- **Registro:** (ex: coloquial informal com bravatas)
- **Características:** (ex: auto-elogio implícito; contrações coloquiais)
- **Red flags:** (ex: soar humilde ou formal)

### PersonagemC — `voice_criticality: low`
- **Registro:**
- **Características:**
- **Red flags:**

## Convenções de PT-BR

- **"você"** (não "tu") em falas informais a neutras — PT-BR brasileiro padrão
- Evitar lusismos: "miúdos", "fixe", "gajo", "rapariga"
"""

_DECISION_LOG_TEMPLATE = """\
# Decision Log — {title}

## Convenções gerais

[Descrever as convenções gerais de tradução adotadas para este projeto.]

## Nomes próprios

[Listar decisões sobre nomes próprios: verbatim ou traduzir, razão.]

## Traduções canônicas

[Listar termos com tradução canônica fixada e o porquê da escolha.]
"""

_KB_WORKLIST_TEMPLATE = """\
# KB Phase Worklist — {title}

## Fase 1 — Personagens principais
- [ ] Pesquisar personagens via wiki/fandom (skill 03)
- [ ] Reconciliar com usuário
- [ ] Preencher glossary.csv com personagens (handling_rule: verbatim)
- [ ] Preencher tone_analysis.md com voice cards (### Nome — `voice_criticality: X`)

## Fase 2 — Terminologia e lore
- [ ] Identificar termos de lore, locais, facções
- [ ] Preencher glossary.csv com termos (handling_rule: verbatim ou translate)
- [ ] Atualizar decision_log.md com decisões não-óbvias

## Fase 3 — UI/Menus (pós-piloto)
- [ ] Verificar termos de UI em jogo
- [ ] Adicionar ao glossary.csv com handling_rule: translate
"""


def scaffold(project_root: Path, title: str = "") -> None:
    art = project_root / "artifacts"
    art.mkdir(parents=True, exist_ok=True)

    t = title or project_root.name
    created, skipped = [], []

    # 1. glossary.csv — schema correto para context_pack + state_index
    gp = art / "glossary.csv"
    if gp.exists():
        skipped.append(gp)
    else:
        with gp.open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(_GLOSSARY_HEADERS)
        created.append(gp)

    # 2. tone_analysis.md — com voice card sections obrigatórias
    tp = art / "tone_analysis.md"
    if tp.exists():
        skipped.append(tp)
    else:
        tp.write_text(_TONE_ANALYSIS_TEMPLATE.format(title=t), encoding="utf-8")
        created.append(tp)

    # 3. decision_log.md
    dp = art / "decision_log.md"
    if dp.exists():
        skipped.append(dp)
    else:
        dp.write_text(_DECISION_LOG_TEMPLATE.format(title=t), encoding="utf-8")
        created.append(dp)

    # 4. kb_phase_worklist.md
    kp = art / "kb_phase_worklist.md"
    if kp.exists():
        skipped.append(kp)
    else:
        kp.write_text(_KB_WORKLIST_TEMPLATE.format(title=t), encoding="utf-8")
        created.append(kp)

    for f in created:
        print(f"  CRIADO  {f.relative_to(project_root)}")
    for f in skipped:
        print(f"  SKIP    {f.relative_to(project_root)} (já existe)")

    if created:
        print(f"\nScaffold completo para '{t}'.")
        print("Próximos passos:")
        print("  1. Editar tone_analysis.md — substituir PersonagemA/B/C pelos reais")
        print("  2. Editar glossary.csv — adicionar termos (term,category,target_translation,handling_rule,...)")
        print("  3. Editar decision_log.md — documentar decisões de tradução")
        print("  4. Rodar: python framework/runtime/state_index.py <projeto>")

    _report_connector_gate_status(project_root)
    _report_kb_gate_status(project_root)


def _report_connector_gate_status(project_root: Path) -> None:
    """D6c: mesmo principio do _report_kb_gate_status abaixo, agora pro conector (gap real do
    Souldiers: project.json declarava 'Fase 0 concluida' so com extract.py/reinsert.py -- os
    scripts de build_plan/verify nunca existiram, round-trip nunca validado de verdade). NAO cria
    stub fake dos scripts (enganaria o gate); so reporta o que falta, visivel no dia 1."""
    _here = Path(__file__).resolve().parent
    if str(_here) not in sys.path:
        sys.path.insert(0, str(_here))
    import connector_gate  # noqa: E402  (import tardio, mesmo padrao do kb_gate abaixo)
    try:
        r = connector_gate.check(project_root)
    except Exception as e:
        print(f"\n[connector_gate] nao foi possivel checar ainda ({e!r}).")
        return
    for w in r.get("warnings", []):
        print(f"\n[connector_gate] aviso: {w}")
    all_problems = r.get("hard_problems", []) + r.get("problems", [])
    if not all_problems:
        print("\n[connector_gate] OK — conector completo.")
        return
    print(f"\n[connector_gate] AINDA FALTAM {len(all_problems)} item(ns) de completude de conector:")
    for p in r.get("hard_problems", []):
        print(f"  [HARD] {p}")
    for p in r.get("problems", []):
        print(f"  [bloqueia sem --skip-connector-gate] {p}")


def _report_kb_gate_status(project_root: Path) -> None:
    """Roda o kb_gate de verdade (nao um checklist estatico) logo apos o scaffold, para o requisito
    aparecer no dia 1 do onboarding em vez de ser descoberto num piloto pago (gap real do Souldiers:
    scaffold nunca cria universe_knowledge_base.md/research_log.md com conteudo real — nem deveria,
    um placeholder passaria o hard-gate sem pesquisa de verdade — entao so REPORTA o que falta)."""
    if not (project_root / "project.json").is_file():
        print("\n[kb_gate] project.json ainda nao existe — rode o gate depois de cria-lo:")
        print("          python framework/runtime/kb_gate.py <projeto> <qualquer_scene_id>")
        return
    _here = Path(__file__).resolve().parent
    if str(_here) not in sys.path:
        sys.path.insert(0, str(_here))
    import kb_gate  # noqa: E402  (import tardio: so precisa quando project.json ja existe)
    try:
        r = kb_gate.check(project_root, "00_00")
    except Exception as e:
        print(f"\n[kb_gate] nao foi possivel checar ainda ({e!r}) — normal antes da extracao/Fase 0.")
        return
    all_problems = r.get("hard_problems", []) + r.get("problems", [])
    if not all_problems:
        print("\n[kb_gate] OK — cobertura de KB ja suficiente para traduzir.")
        return
    print(f"\n[kb_gate] AINDA FALTAM {len(all_problems)} item(ns) antes de poder traduzir "
          f"(gate obrigatorio, skill 03/04):")
    for p in r.get("hard_problems", []):
        print(f"  [HARD] {p}")
    for p in r.get("problems", []):
        print(f"  [bloqueia sem --skip-kb-gate] {p}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    title_idx = next((i for i, a in enumerate(sys.argv) if a == "--title"), None)
    title = sys.argv[title_idx + 1] if title_idx is not None and title_idx + 1 < len(sys.argv) else ""

    if not args:
        sys.exit("Uso: python scaffold_project.py <project_root> [--title 'Título']")

    root = Path(args[0])
    if not root.is_dir():
        sys.exit(f"ERRO: diretório não encontrado: {root}")

    scaffold(root, title)


if __name__ == "__main__":
    main()
