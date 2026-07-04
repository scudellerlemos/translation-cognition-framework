"""kernel.py — fachada fina de orquestracao (Evolucao do Motor).

NAO reimplementa nada: `run_scene`/`run_chapter`/`run_game` (todos ja tipados, sem dependencia de
Claude/MCP) + `validate_project` (Validation) + `write_pack` (Memory/context_pack -- ja usa
busca semantica via sqlite-vec quando o projeto tem `.db`, ver framework/db/) JA formam o "runtime
que orquestra os passos usando Validation + Memory" que o ROADMAP pedia. Este modulo so consolida
esses nomes sob um import UNICO, pra um agente/CLI/orquestrador externo nao precisar descobrir que
sao 5 modulos espalhados -- e uma fachada, nao uma camada nova de logica.

A parte de Skill DSL nao precisou de codigo novo: `framework/skills/skill_base.py` (Skill ABC) +
`framework/skills/registry.py` ja sao a forma declarativa dos passos 00/06/07/08 (os com
substancia de codigo). Skills cognitivas puras (01-04b/05b/06c) ficam .md por decisao deliberada
(ver skills-registry-boundary) -- nao e lacuna, e fronteira.

Uso: `from kernel import run_scene, run_chapter, run_game, validate_project, write_pack`
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
_VALIDATION_DIR = _HERE.parent / "validation"
if str(_VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(_VALIDATION_DIR))

from context_pack import write_pack  # noqa: E402,F401
from run_chapter import run_chapter  # noqa: E402,F401
from run_game import run_game  # noqa: E402,F401
from run_scene import RunSceneOptions, RunSceneResult, run_scene  # noqa: E402,F401
from validate import validate_project  # noqa: E402,F401

__all__ = [
    "run_scene", "RunSceneOptions", "RunSceneResult",
    "run_chapter", "run_game",
    "validate_project",
    "write_pack",
]
