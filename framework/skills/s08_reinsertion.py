"""s08_reinsertion.py — Skill 08: Reinserção (connector/reinsert.py como módulo).

Wraps o reinsert_script do conector — aplica approved_translations.csv no binário e gera o
patch. DETERMINÍSTICA: a reinserção é código do conector; a IA nunca escreve bytes (invariante
#13). Espelha o s00 (extração): gate por project.json:connector.reinsert_script + subprocess.

Uso:
    skill = ReinsertionSkill()
    result = skill.run("projects/breath_of_fire_4", dat_dir="/path/to/DAT")
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RUNTIME = _HERE.parent / "runtime"
sys.path.insert(0, str(_HERE))
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))
from connector_mgr import _connector_script  # noqa: E402  (sandbox contra path traversal)
from skill_base import Skill  # noqa: E402


class ReinsertionSkill(Skill):
    """Skill 08 — Reinserção: roda connector/reinsert.py (det.; LLM só no resíduo de overflow)."""

    skill_id = "08"
    name = "Reinsertion"
    kind = "deterministic"

    def check_inputs(self, project: Path) -> list[str]:
        problems = super().check_inputs(project)
        if problems:
            return problems
        cfg = self.project_cfg(project)
        conn = cfg.get("connector", {})
        script_cfg = conn.get("reinsert_script")
        if not script_cfg:
            problems.append("project.json: connector.reinsert_script não declarado")
            return problems
        try:
            script = _connector_script(Path(project), cfg, "reinsert_script", "reinsert.py")
        except ValueError as e:
            problems.append(str(e))
            return problems
        if not script.is_file():
            problems.append(f"reinsert_script não encontrado: {script_cfg}")
        return problems

    def run(self, project: Path, *, dat_dir: str | None = None, **kwargs) -> dict:
        project = Path(project)
        problems = self.check_inputs(project)
        if problems:
            return {"status": "error", "problems": problems, "artifacts": []}

        cfg = self.project_cfg(project)
        try:
            script = _connector_script(project, cfg, "reinsert_script", "reinsert.py")
        except ValueError as e:
            return {"status": "error", "error": str(e), "artifacts": []}
        env = {**os.environ, "BOF4_DAT_DIR": str(dat_dir)} if dat_dir else None
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(project), capture_output=True, text=True,
                encoding="utf-8", errors="replace", env=env,
                stdin=subprocess.DEVNULL, timeout=600,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "reinsert.py timeout (>600s)", "artifacts": []}
        except Exception as e:  # noqa: BLE001 - reporta qualquer falha de spawn como erro estruturado
            return {"status": "error", "error": str(e), "artifacts": []}

        if result.returncode != 0:
            return {"status": "error", "returncode": result.returncode,
                    "stderr": (result.stderr or "")[:1000], "artifacts": []}

        out_dir = project / "output"
        artifacts = sorted(str(p) for p in out_dir.glob("*")) if out_dir.is_dir() else []
        return {"status": "ok", "artifacts": artifacts,
                "stdout": (result.stdout or "")[:500]}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Skill 08 — Reinserção")
    ap.add_argument("project", help="Raiz do projeto")
    ap.add_argument("--dat-dir", default=None, help="Diretório dos DATs do jogo")
    a = ap.parse_args()
    skill = ReinsertionSkill()
    problems = skill.check_inputs(a.project)
    if problems:
        for p in problems:
            print(f"ERRO: {p}")
        sys.exit(1)
    result = skill.run(a.project, dat_dir=a.dat_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("status") == "ok" else 1)
