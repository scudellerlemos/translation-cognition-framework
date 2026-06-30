"""test_skills.py — contrato das skills como módulos + CLI e2e.

Prova a FRONTEIRA cognitivo↔determinístico (registry só com skills de código), o gate de
entrada (check_inputs) e o caminho CLI ponta-a-ponta. A skill 07 (QA) roda de verdade sobre o
BoF4 — read-only, SEM rede — exercitando o stack registry→skill→CLI honestamente. Só stdlib.
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent          # framework/skills
FRAMEWORK = HERE.parent
ROOT = FRAMEWORK.parents[0]
for _p in (str(HERE), str(FRAMEWORK), str(FRAMEWORK / "runtime")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import registry  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def test_registry_has_core_skills():
    ids = {s.skill_id for s in registry.all_skills()}
    assert {"00", "06", "07", "08"} <= ids, ids


def test_registry_kinds_separate_cognitive_from_deterministic():
    """A fronteira é estrutural: 00/07/08 determinísticas, 06 (tradução) cognitiva."""
    by = {s.skill_id: s.kind for s in registry.all_skills()}
    assert by["00"] == "deterministic"
    assert by["07"] == "deterministic"
    assert by["08"] == "deterministic"
    assert by["06"] == "cognitive"


def test_skill_gate_blocks_missing_project(tmp_path):
    problems = registry.get("07").check_inputs(tmp_path)  # sem project.json
    assert problems and "project.json" in problems[0]


def test_reinsertion_gate_ok_on_bof4():
    """Skill 08: gate passa no BoF4 (reinsert_script declarado e presente). NÃO roda (precisa do binário)."""
    if not (BOF4 / "project.json").is_file():
        pytest.skip("BoF4 ausente")
    assert registry.get("08").check_inputs(BOF4) == []


def test_qa_skill_runs_deterministic_no_network():
    """e2e determinístico: skill 07 roda sobre o BoF4 (read-only, sem rede) e devolve coverage."""
    if registry.get("07").check_inputs(BOF4):
        pytest.skip("BoF4 sem artifacts/scenes")
    r = registry.get("07").run(BOF4)
    assert r["status"] in ("ok", "blocked"), r
    assert "coverage" in r and "pct" in r["coverage"], r


def test_cli_skill_list_and_run_e2e(capsys):
    """CLI e2e: `skill list` e `skill run 07 <bof4>` via o parser → func, sem exceção/rede."""
    if registry.get("07").check_inputs(BOF4):
        pytest.skip("BoF4 sem artifacts/scenes")
    import cli
    # list
    rc = cli.build_parser().parse_args(["skill", "list"]).func(
        cli.build_parser().parse_args(["skill", "list"]))
    assert rc == 0
    assert "deterministic" in capsys.readouterr().out
    # run 07
    args = cli.build_parser().parse_args(["skill", "run", "07", str(BOF4)])
    rc = args.func(args)
    assert rc in (0, 1), rc          # 0=ok, 1=blocked — ambos válidos
    assert "coverage" in capsys.readouterr().out
