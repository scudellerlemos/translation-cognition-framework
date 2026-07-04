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


def test_choose_pattern_token_table():
    ev = {"has_control_tokens": True, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    assert sg._choose_pattern(ev)[0] == "token_table"
    out = sg.generate(ev)
    assert "BYTE_TO_CHAR" in out and "GERADO AUTOMATICAMENTE" in out


def test_choose_pattern_linear_scan():
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    assert sg._choose_pattern(ev)[0] == "linear_scan"
    out = sg.generate(ev)
    assert "iter_string_offsets" in out and "_MIN_STRING_LEN" in out


def test_choose_pattern_pointer_table():
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.3}, "string_density": 0.1}
    assert sg._choose_pattern(ev)[0] == "pointer_table"
    out = sg.generate(ev)
    assert "_TOC_OFFSET" in out and "struct.unpack_from" in out
