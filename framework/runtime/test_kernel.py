"""test_kernel.py — kernel.py e fachada PURA: confirma que cada nome reexportado e o MESMO
objeto do modulo de origem (identidade, nao copia) -- garante que nao virou reimplementacao."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import kernel  # noqa: E402
import run_chapter  # noqa: E402
import run_game  # noqa: E402
import run_scene  # noqa: E402

sys.path.insert(0, str(_HERE.parent / "validation"))
import validate  # noqa: E402


def test_kernel_reexports_are_identity_not_copies():
    assert kernel.run_scene is run_scene.run_scene
    assert kernel.RunSceneOptions is run_scene.RunSceneOptions
    assert kernel.RunSceneResult is run_scene.RunSceneResult
    assert kernel.run_chapter is run_chapter.run_chapter
    assert kernel.run_game is run_game.run_game
    assert kernel.validate_project is validate.validate_project
    assert kernel.write_pack is context_pack.write_pack
