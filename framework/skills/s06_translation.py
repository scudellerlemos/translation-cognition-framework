"""s06_translation.py — Skill 06: Tradução (run_scene como módulo).

COGNITIVA (kind='cognitive'): o harness é determinístico (orçamento de bytes, fitting loop,
round-trip), mas o miolo — a tradução em si — é a IA, ISOLADA em model.py. A skill orquestra;
não decide a tradução. Por isso entra no registry (tem código), mas marcada como cognitive: não
roda em CI sem rede/backend (ao contrário de 00/07/08).

Uso:
    skill = TranslationSkill()
    result = skill.run("projects/breath_of_fire_4", scene="AREAD001", backend="api")
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


class TranslationSkill(Skill):
    """Skill 06 — Tradução: roda run_scene (plano + tradução + fitting + verify) de uma cena."""

    skill_id = "06"
    name = "Translation"
    kind = "cognitive"

    def check_inputs(self, project: Path) -> list[str]:
        problems = super().check_inputs(project)
        if problems:
            return problems
        if not (Path(project) / "artifacts" / "scenes").is_dir():
            problems.append("artifacts/scenes/ ausente — rode a extração (skill 00) antes")
        return problems

    def run(self, project: Path, *, scene: str | None = None, backend: str = "api",
            require_back: bool = False, do_verify: bool = True,
            skip_kb_gate: bool = False, **kwargs) -> dict:
        problems = self.check_inputs(project)
        if problems:
            return {"status": "error", "problems": problems, "artifacts": []}
        if not scene:
            return {"status": "error", "problems": ["argumento 'scene' obrigatório"], "artifacts": []}
        import run_scene as rs
        result = rs.run_scene(
            str(project), scene, backend=backend, require_back=require_back,
            do_verify=do_verify, skip_kb_gate=skip_kb_gate,
        )
        # run_scene devolve status próprio (verified/planned/...); normaliza p/ o contrato da Skill
        result.setdefault("artifacts", [])
        return result


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Skill 06 — Tradução")
    ap.add_argument("project", help="Raiz do projeto")
    ap.add_argument("scene", help="ID da cena (ex: AREAD001)")
    ap.add_argument("--backend", default="api", choices=["in-session", "api", "ollama"])
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--skip-kb-gate", action="store_true")
    ap.add_argument("--require-back", action="store_true")
    a = ap.parse_args()
    result = TranslationSkill().run(
        a.project, scene=a.scene, backend=a.backend,
        require_back=a.require_back, do_verify=not a.no_verify, skip_kb_gate=a.skip_kb_gate,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("status") in ("verified", "planned") else 1)
