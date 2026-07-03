"""test_tm_lookup.py — cobre a TM por serie (D4): fallback de serie, lookup exato, serie ausente,
isolamento cross-serie. Usa monkeypatch de tm_lookup._REPO_ROOT pra nao escrever em tm/ de verdade.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import tm_lookup as tl  # noqa: E402


def test_series_of_uses_declared_field(monkeypatch, tmp_path):
    assert tl.series_of({"series": "Breath of Fire"}, tmp_path) == "breath_of_fire"


def test_series_of_falls_back_to_title_slug(tmp_path):
    assert tl.series_of({"title": "Utawarerumono!"}, tmp_path) == "utawarerumono"


def test_series_of_falls_back_to_dirname_without_title(tmp_path):
    proj = tmp_path / "My Game"
    proj.mkdir()
    assert tl.series_of({}, proj) == "my_game"


def test_load_series_tm_missing_is_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    assert tl.load_series_tm("nao_existe") == []


def test_lookup_exact_match(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    p = tl.series_tm_path("bof")
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps([{"src_key": tl.tm_key("Hello"), "source": "Hello", "target": "Ola"}]),
                encoding="utf-8")
    hit = tl.lookup("bof", tl.tm_key("Hello"))
    assert hit["target"] == "Ola"
    assert tl.lookup("bof", tl.tm_key("Goodbye")) is None


def test_isolation_between_series(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    key = tl.tm_key("Dragon")
    tl.series_tm_path("series_a").parent.mkdir(parents=True, exist_ok=True)
    tl.series_tm_path("series_a").write_text(
        json.dumps([{"src_key": key, "source": "Dragon", "target": "Dragao (serie A)"}]), encoding="utf-8")
    tl.series_tm_path("series_b").write_text(
        json.dumps([{"src_key": key, "source": "Dragon", "target": "Dragao (serie B)"}]), encoding="utf-8")
    a = tl.lookup("series_a", key)
    b = tl.lookup("series_b", key)
    assert a["target"] == "Dragao (serie A)"
    assert b["target"] == "Dragao (serie B)"
    assert a["target"] != b["target"]


def test_context_pack_load_tm_series_hits_and_dedups(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    p = tl.series_tm_path("bof")
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps([
        {"source_game": "bof3", "src_key": tl.tm_key("Ryu"), "source": "Ryu", "target": "Ryu"},
    ]), encoding="utf-8")
    rows = [{"source": "Ryu"}, {"source": "Ryu"}, {"source": "sem match"}]   # 1a e 2a duplicam a chave
    hits = context_pack._load_tm_series({"series": "bof"}, tmp_path, rows)
    assert len(hits) == 1   # dedup por src_key, mesmo com 2 linhas iguais
    assert hits[0] == {"source": "Ryu", "target": "Ryu", "from_game": "bof3"}


def test_context_pack_load_tm_series_empty_when_no_match(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_REPO_ROOT", tmp_path)
    hits = context_pack._load_tm_series({"series": "sem_dados"}, tmp_path, [{"source": "x"}])
    assert hits == []
