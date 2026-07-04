"""test_tier_classifier_gate.py — cobre existence_gate: engine conhecida nunca aciona geracao,
engine desconhecida e o UNICO tier que aciona, bloqueado nunca gera. Formaliza o que discover.py
ja fazia via if/elif."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import tier_classifier as tc  # noqa: E402

_REGISTRY = [{"id": "known_engine", "reference_connector": "projects/ref/connector",
             "signatures": {"file_patterns": ["*.KNOWN"], "min_file_count": 1}}]


def test_existence_gate_known_engine_never_generates_and_points_to_reference():
    evidence = {"file_count": 5, "families": {"X.KNOWN": 5}, "magic_bytes": {},
               "sample_encodings": {}, "has_control_tokens": False,
               "entropy_mean": 4.0, "string_density": 0.5}
    r = tc.existence_gate(evidence, _REGISTRY)
    assert r["tier"] == "known_engine"
    assert r["must_generate"] is False
    assert r["reference_connector"] == "projects/ref/connector"


def test_existence_gate_unknown_engine_is_only_tier_that_generates():
    evidence = {"file_count": 5, "families": {}, "magic_bytes": {}, "sample_encodings": {},
               "has_control_tokens": False, "entropy_mean": 4.0, "string_density": 0.5}
    r = tc.existence_gate(evidence, _REGISTRY)
    assert r["tier"] == "unknown_engine"
    assert r["must_generate"] is True
    assert r["reference_connector"] is None


def test_existence_gate_blocked_never_generates():
    evidence = {"file_count": 5, "families": {}, "magic_bytes": {}, "sample_encodings": {},
               "has_control_tokens": False, "entropy_mean": 7.9, "string_density": 0.5}
    r = tc.existence_gate(evidence, _REGISTRY)
    assert r["tier"] == "blocked"
    assert r["must_generate"] is False
    assert r["reference_connector"] is None
