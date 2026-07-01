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
# 'handling_rule'. Adicionar outras colunas aqui muda o template mas não quebra nada.
_GLOSSARY_HEADERS = [
    "term", "category", "target_translation", "handling_rule",
    "spoiler_level", "aliases", "notes",
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
