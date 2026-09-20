"""test_migrate_edges.py — entradas malformadas/legadas na migração flat → SQLite.

Complementa test_migrate.py (caminho feliz): cada artefato ruim (JSON corrompido, linha sem chave,
formato legado de voice_cards) é pulado ou avisa, nunca aborta a migração inteira nem grava lixo.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

from migrate_from_flat import migrate  # noqa: E402


def _w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_corrupt_project_json_falls_back_to_defaults(tmp_path):
    root = tmp_path / "meuproj"
    _w(root / "project.json", "{nao e json")
    result = migrate(root, tmp_path / "x.db")
    assert result["project_id"] == "bof4"          # último fallback quando project.json ilegível
    assert result["scenes"] == result["translations"] == result["kb"] == 0


def test_malformed_artifacts_are_skipped_or_warned(tmp_path, capsys):
    root = tmp_path / "edgeproj"
    art = root / "artifacts"
    _w(root / "project.json", json.dumps({"title": "Edge"}))
    _w(art / "run_state.json", json.dumps({"scenes": {"AREAD001": {"status": "translated"}}}))
    _w(art / "scenes" / "stray.txt", "arquivo solto, nao e cena")
    (art / "scenes" / "AREAD002").mkdir()                       # cena sem dialogs.csv
    scene = art / "scenes" / "AREAD001"
    _w(scene / "dialogs.csv", "offset,text_en,byte_budget\n0x1,Hello,10\n0x2,World,abc\n")
    _w(scene / "translation_plan_a.json", "{corrompido")
    _w(scene / "translation_plan_b.json",
       json.dumps({"lines": {"0x1": {"speaker": "Poko", "risk_level": "high"}}}))   # lines como dict
    _w(scene / "approved_pt.csv",
       "offset,text_target\n,sem offset\n0x2,\n0x1,Ola\n")      # 2 linhas invalidas, 1 valida
    _w(scene / "back_translation_bad.json", "{corrompido")
    _w(scene / "back_translation_ok.json", json.dumps({"entries": [{"offset": "0x1", "verdict": "pass"}]}))
    _w(art / "glossary.csv", "term,translation\nPoko,Poko\nSemTraducao,\n")
    _w(art / "entities.csv", "name,type\nPoko,character\n,orphan\n")
    _w(art / "state" / "voice_cards.json",
       json.dumps([{"speaker": "A"}, {"name": "B"}, {"aliases": ["sem-nome"]}]))   # formato legado (lista)
    _w(art / "state" / "decision_index.json",
       json.dumps({"decisions": [{"title": "Regra", "universal": True}, {"summary": "sem titulo"}]}))
    _w(art / "spoiler_ledger.json",
       json.dumps({"entries": [{"entity": "Vilao", "fact": "x"}, {"fact": "sem entidade"}]}))
    _w(art / "kb_ratified.csv", "name,ratified_by,date,note\nPoko,eu,2026-01-01,ok\n  ,eu,2026-01-01,vazio\n")
    _w(art / "metrics.jsonl", '\n{corrompido\n{"n_lines": 1}\n{"scene": "AREAD001", "n_lines": 2}\n')

    r = migrate(root, tmp_path / "edge.db", project_id="edge")
    out = capsys.readouterr().out

    assert (r["scenes"], r["scene_lines"], r["translations"]) == (1, 2, 1)
    assert (r["back_translations"], r["glossary"], r["entities"]) == (1, 1, 1)
    assert (r["voice_cards"], r["decisions"], r["spoiler"]) == (2, 1, 1)
    assert (r["kb_ratified"], r["metrics"]) == (1, 1)
    assert "translation_plan_a.json" in out and "ilegivel" in out       # plano corrompido só avisa
    assert "back_translation_bad.json" in out                            # idem back-translation
