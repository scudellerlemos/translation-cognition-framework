"""s07_qa.py — Skill 07: QA (piso de qualidade observável) como módulo.

Wraps `quality_gate.check` — varre as back_translation gravadas x linhas high/critical do
plano e levanta 'revise' (verdict do modelo divergiu) e 'uncovered' (linha crítica sem crivo).
DETERMINÍSTICA: read-only, sem rede, sem work-text — lê artefato já pago. É o passo de QA que
PODE rodar em CI sem IA (ao contrário do 06c, que é correção cognitiva).

Uso:
    skill = QaSkill()
    result = skill.run("projects/breath_of_fire_4", chapter="19")  # chapter=None varre tudo
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
for _p in (str(_HERE), str(_RUNTIME)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from skill_base import Skill  # noqa: E402


class QaSkill(Skill):
    """Skill 07 — QA: cruza back_translation x high/critical e bloqueia se houver revise/uncovered."""

    skill_id = "07"
    name = "QA"
    kind = "deterministic"

    def check_inputs(self, project: Path) -> list[str]:
        problems = super().check_inputs(project)
        if problems:
            return problems
        if not (Path(project) / "artifacts" / "scenes").is_dir():
            problems.append("artifacts/scenes/ ausente — nada planejado p/ revisar")
        return problems

    def run(self, project: Path, *, chapter: str | None = None, **kwargs) -> dict:
        problems = self.check_inputs(project)
        if problems:
            return {"status": "error", "problems": problems, "artifacts": []}
        import quality_gate
        r = quality_gate.check(Path(project), chapter)
        rev, unc = r["revise"], r["uncovered"]
        # 'blocked' = gate reprovou (há revise/uncovered); 'ok' = piso satisfeito p/ o escopo coberto
        return {
            "status": "blocked" if (rev or unc) else "ok",
            "artifacts": [],
            "revise": len(rev),
            "uncovered": len(unc),
            "coverage": r["coverage"],
        }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Skill 07 — QA")
    ap.add_argument("project", help="Raiz do projeto")
    ap.add_argument("chapter", nargs="?", default=None, help="filtra por capítulo; default: tudo")
    a = ap.parse_args()
    result = QaSkill().run(a.project, chapter=a.chapter)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("status") == "ok" else 1)
