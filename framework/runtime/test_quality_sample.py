"""quality_sample.export --scenes: a populacao da amostra fica restrita as cenas pedidas."""
import json
from pathlib import Path

import pattern_lint
import pytest
import quality_sample
import risk_triage


def _fake(monkeypatch):
    allp = {
        "a": {"source": "s1", "target": "t1", "where": [("S00", "0"), ("S01", "0")]},
        "b": {"source": "s2", "target": "t2", "where": [("S01", "1")]},
        "c": {"source": "s3", "target": "t3", "where": [("S02", "0")]},
    }
    monkeypatch.setattr(pattern_lint, "lint", lambda root: {"blocking": {}})
    monkeypatch.setattr(risk_triage, "pairs", lambda root, everything=False: json.loads(json.dumps(allp)))
    monkeypatch.setattr(risk_triage, "judged", lambda root: (set(), {"c"}))


def test_export_scenes_restricts_population_and_flagged(tmp_path, monkeypatch):
    _fake(monkeypatch)
    r = quality_sample.export(tmp_path, n=10, seed="x", scenes=["S01"])
    assert (r["population"], r["sample"], r["flagged"]) == (2, 2, 1)
    meta = json.loads(Path(r["path"]).with_suffix(".json").read_text(encoding="utf-8"))
    assert sorted(meta["sample"]) == ["a", "b"] and meta["weight"] == {"a": 1, "b": 1}   # copia de S00 fora do peso


def test_export_without_scenes_keeps_whole_game(tmp_path, monkeypatch):
    _fake(monkeypatch)
    assert quality_sample.export(tmp_path, n=10)["population"] == 3


def test_export_unknown_scene_fails(tmp_path, monkeypatch):
    _fake(monkeypatch)
    with pytest.raises(SystemExit):
        quality_sample.export(tmp_path, scenes=["NOPE"])


def _sheet(root, verdicts):
    import csv

    import paths
    out = paths.qa_outbox(root)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "amostra_qualidade.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(quality_sample.COLS)
        for i, v in enumerate(verdicts):
            w.writerow([f"id{i}", f"S{i}", str(i), f"src {i}", f"tgt {i}", v, ""])
    return out


def test_judge_export_hides_origin_and_apply_feeds_score(tmp_path):
    out = _sheet(tmp_path, ["", "", ""])
    (out / "amostra_qualidade.json").write_text(json.dumps(
        {"seed": "s", "population": 3, "sample": ["id0", "id1", "id2"], "flagged": [], "seen": 0,
         "weight": {"id0": 1, "id1": 1, "id2": 1}}), encoding="utf-8")
    assert quality_sample.judge_export(tmp_path)["rows"] == 3
    tsv = (out / quality_sample.JUDGE_IN).read_text(encoding="utf-8")
    T = chr(9)
    assert tsv.splitlines()[0] == T.join(["id0", "src 0", "tgt 0"])          # sem cena, offset nem modelo
    (out / quality_sample.JUDGE_OUT).write_text(
        "id0" + T + "ok" + chr(10) + "id1" + T + "erro" + T + "sentido" + chr(10) + "id2" + T + "ok" + chr(10),
        encoding="utf-8")
    assert quality_sample.judge_apply(tmp_path)["judged"] == 3
    got = quality_sample.score(tmp_path, "llm-judge:opus")
    assert (got["judged"], got["errors"], got["reviewer"]) == (3, 1, "llm-judge:opus")


def test_judge_compare_against_human_sheet(tmp_path):
    out = _sheet(tmp_path, ["ok", "erro", "ok", "erro"])
    T = chr(9)
    (out / quality_sample.JUDGE_OUT).write_text(
        chr(10).join(["id0" + T + "ok", "id1" + T + "erro" + T + "x", "id2" + T + "erro" + T + "y", "id3" + T + "ok"]),
        encoding="utf-8")
    r = quality_sample.judge_compare(tmp_path)
    assert (r["compared"], r["human_errors"], r["judge_errors"], r["both_error"], r["judge_only"]) == (4, 2, 2, 1, 1)
    assert r["agreement"] == 0.5
