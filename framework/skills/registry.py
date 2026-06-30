"""registry.py — registro das skills com CÓDIGO por trás (a camada determinística do pipeline).

FRONTEIRA cognitivo↔determinístico (valor central do framework): SÓ entram aqui skills cuja
substância é código — determinísticas (00 extract, 07 qa, 08 reinsert) ou orquestração com a IA
ISOLADA (06 translate). As skills puramente cognitivas (01 discovery, 02 entity_resolution,
03 knowledge_building, 04 glossary, 04b, 05b, 06b, 06c) NÃO entram: são playbooks .md que a IA
executa, sem lógica determinística a encapsular. Esta lista É a fronteira, em código.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from s00_extraction import ExtractionSkill  # noqa: E402
from s06_translation import TranslationSkill  # noqa: E402
from s07_qa import QaSkill  # noqa: E402
from s08_reinsertion import ReinsertionSkill  # noqa: E402
from skill_base import Skill  # noqa: E402

_SKILLS: dict[str, Skill] = {
    s.skill_id: s for s in (
        ExtractionSkill(), TranslationSkill(), QaSkill(), ReinsertionSkill(),
    )
}


def get(skill_id: str) -> Skill | None:
    """Retorna a instância da skill pelo id ('00','06','07','08') ou None."""
    return _SKILLS.get(skill_id)


def all_skills() -> list[Skill]:
    """Lista as skills registradas, ordenadas por id."""
    return [_SKILLS[k] for k in sorted(_SKILLS)]
