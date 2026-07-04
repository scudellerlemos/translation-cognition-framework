"""test_script_generator.py — cobre a geracao de esqueletos de build_plan/verify:
generate_build_plan_chapter() e generate_verify_chapter() leem o _skeleton/ e retornam o
protocolo comum (nao ha branching por evidencia aqui, ao contrario de generate()/extract.py)."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import script_generator as sg  # noqa: E402


def test_generate_build_plan_chapter_returns_skeleton_content():
    out = sg.generate_build_plan_chapter()
    assert "def main()" in out
    assert "ADAPTAR" in out
    assert "translation_plan_" in out


def test_generate_verify_chapter_returns_skeleton_content():
    out = sg.generate_verify_chapter()
    assert "VERIFY_STATUS" in out
    assert "ADAPTAR" in out
    assert "sys.exit(3 if fitting_failure else 1)" in out


def test_generate_verify_chapter_documents_exit_code_protocol():
    out = sg.generate_verify_chapter()
    assert "exit 0" in out and "exit 3" in out and "exit 1" in out
