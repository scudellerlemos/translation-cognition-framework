"""s00_extraction.py — Skill 00: Extração (connector/extract.py como módulo Python).

Wraps o script extract.py do conector como uma skill com interface formal.
Gate de entrada: project.json com connector.extract_script declarado.
Saída: artifacts/dialogs.csv com n strings extraídas.

Uso:
    skill = ExtractionSkill()
    problems = skill.check_inputs("projects/translation_software")
    if not problems:
        result = skill.run("projects/translation_software", dat_dir="/path/to/DAT")
"""
from __future__ import annotations

import csv
import json
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


class ExtractionSkill(Skill):
    """Skill 00 — Extração: roda connector/extract.py e valida o dialogs.csv produzido."""

    skill_id = "00"
    name = "Extraction"

    @property
    def required_inputs(self) -> list[str]:
        return []  # Skill 00 é o ponto de entrada — sem pré-requisitos de artefato

    def check_inputs(self, project: Path) -> list[str]:
        problems = super().check_inputs(project)
        if problems:
            return problems
        cfg = self.project_cfg(project)
        conn = cfg.get("connector", {})
        extract = conn.get("extract_script")
        if not extract:
            problems.append("project.json: connector.extract_script não declarado")
            return problems
        try:
            script = _connector_script(Path(project), cfg, "extract_script", "extract.py")
        except ValueError as e:
            problems.append(str(e))
            return problems
        if not script.is_file():
            problems.append(f"extract_script não encontrado: {extract}")
        return problems

    def run(self, project: Path, *, dat_dir: str = None, **kwargs) -> dict:
        """Roda o connector/extract.py.

        Args:
            project:  raiz do projeto
            dat_dir:  diretório dos arquivos DAT do jogo (passado via BOF4_DAT_DIR
                      ou argumento -- nunca persistido no project.json)
        """
        project = Path(project)
        problems = self.check_inputs(project)
        if problems:
            return {"status": "error", "problems": problems, "artifacts": []}

        cfg = self.project_cfg(project)
        try:
            extract_script = _connector_script(project, cfg, "extract_script", "extract.py")
        except ValueError as e:
            return {"status": "error", "error": str(e), "artifacts": []}
        dialogs_csv = project / cfg.get("source", {}).get("file", "artifacts/dialogs.csv")

        import os
        cmd = [sys.executable, str(extract_script)]
        # PYTHONIOENCODING/PYTHONUTF8 + errors="replace": mesma protecao de encoding do
        # connector_mgr._run (conector pode emitir bytes nao-utf-8 no stdout/stderr).
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        if dat_dir:
            env["BOF4_DAT_DIR"] = str(dat_dir)

        try:
            result = subprocess.run(
                cmd,
                cwd=str(project),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                stdin=subprocess.DEVNULL,
                timeout=300,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "extract.py timeout (>300s)", "artifacts": []}
        except Exception as e:
            return {"status": "error", "error": str(e), "artifacts": []}

        if result.returncode != 0:
            return {
                "status": "error",
                "returncode": result.returncode,
                "stderr": result.stderr[:1000],
                "artifacts": [],
            }

        if not dialogs_csv.is_file():
            return {
                "status": "error",
                "error": f"dialogs.csv não gerado em {dialogs_csv}",
                "artifacts": [],
            }

        n_strings = _count_csv_rows(dialogs_csv)
        return {
            "status": "ok",
            "artifacts": [str(dialogs_csv)],
            "n_strings": n_strings,
            "dialogs_csv": str(dialogs_csv),
            "stdout": result.stdout[:500] if result.stdout else "",
        }


def _count_csv_rows(path: Path) -> int:
    try:
        with path.open(encoding="utf-8", newline="") as f:
            return sum(1 for _ in csv.reader(f)) - 1  # exclui header
    except Exception:
        return -1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Skill 00 — Extração")
    ap.add_argument("project", help="Raiz do projeto")
    ap.add_argument("--dat-dir", default=None, help="Diretório dos DATs do jogo")
    a = ap.parse_args()
    skill = ExtractionSkill()
    problems = skill.check_inputs(a.project)
    if problems:
        for p in problems:
            print(f"ERRO: {p}")
        sys.exit(1)
    result = skill.run(a.project, dat_dir=a.dat_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
