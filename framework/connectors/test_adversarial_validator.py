"""test_adversarial_validator.py — cobre as 3 checagens de consistencia sobre `per_file`.
Fixtures sinteticas de `per_file` (shape que coverage_gate.check() produz), sem depender dele.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import adversarial_validator as av  # noqa: E402


def _entry(path, n_strings, offsets=None):
    return {"path": path, "n_strings": n_strings, "offsets": offsets or [], "error": None}


def test_flags_zero_string_file_among_populated():
    per_file = [_entry("a.bin", 50), _entry("b.bin", 60), _entry("c.bin", 0)]
    r = av.check(per_file)
    assert r["passed"] is False
    assert any("ZERO strings" in p and "c.bin" in p for p in r["problems"])


def test_flags_high_variance_across_files():
    per_file = [_entry("a.bin", 5), _entry("b.bin", 6), _entry("c.bin", 200)]
    r = av.check(per_file)
    assert r["passed"] is False
    assert any("variancia alta" in p for p in r["problems"])


def test_flags_overlapping_offsets():
    per_file = [_entry("a.bin", 2, offsets=[(0, 10), (5, 10)])]   # 0+10=10 > 5 -> sobreposto
    r = av.check(per_file)
    assert r["passed"] is False
    assert any("sobrepostos" in p for p in r["problems"])


def test_passes_consistent_extraction():
    per_file = [
        _entry("a.bin", 50, offsets=[(0, 10), (10, 10), (20, 10)]),
        _entry("b.bin", 55, offsets=[(0, 5), (5, 5)]),
        _entry("c.bin", 48, offsets=[(0, 3), (3, 3)]),
    ]
    r = av.check(per_file)
    assert r == {"passed": True, "problems": []}


def test_error_entries_excluded_from_variance_and_zero_checks():
    # arquivo com erro no coverage_gate nao deve contaminar as checagens estatisticas
    per_file = [_entry("a.bin", 50), _entry("b.bin", 55),
               {"path": "broken.bin", "n_strings": 0, "offsets": [], "error": "boom"}]
    r = av.check(per_file)
    assert r["passed"] is True
