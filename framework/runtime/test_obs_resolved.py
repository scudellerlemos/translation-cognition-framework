"""test_obs_resolved.py — o obs_report nao repete falha de cena que depois fechou `verified`."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import obs_report  # noqa: E402


def _ev(t, scene, result, stage="scene"):
    return {"t": t, "scene": scene, "stage": stage, "result": result}


def test_failure_before_verified_is_dropped_but_later_or_other_scene_stays():
    evs = [_ev(1, "A", "build_plan_failed"), _ev(2, "A", "verified"),
           _ev(3, "B", "verify_failed"), _ev(1, "C", "build_plan_failed"), _ev(5, "C", "verified"),
           _ev(6, "C", "build_plan_failed"), _ev(4, "D", "x_failed", stage="verify")]
    fails = [e for e in evs if e["result"].endswith("_failed")]
    left = obs_report.drop_resolved(fails, evs)
    assert [(f["scene"], f["t"]) for f in left] == [("B", 3), ("C", 6), ("D", 4)]
