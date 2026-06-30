"""test_export.py — oráculo da Fase 6 (export DB → flat).

Prova que o DB regenera os flats de intercâmbio SEM PERDA: o ciclo DB→export→re-migrate→DB
preserva as traduções (mesma contagem e mesmo conteúdo por offset). É o oráculo do cutover —
só "ligar" o flat como derivado do DB é seguro enquanto esse round-trip fechar. Só stdlib.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

from export_to_flat import export  # noqa: E402
from store import Store  # noqa: E402


def test_export_approved_matches_db(bof4_migrated, tmp_path):
    """approved_translations.csv exportado == traduções aprovadas do DB (offset→target), sem perda."""
    db_path, _ = bof4_migrated
    result = export(db_path, "bof4", tmp_path)
    with Store(db_path) as db:
        approved = {r["offset"]: r["target"] for r in db.get_translations("bof4", approved_only=True)}
    assert result["approved"] == len(approved), result
    with (tmp_path / "approved_translations.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert {r["offset"] for r in rows} == set(approved), "offsets do CSV divergem do DB"
    for r in rows:
        assert r["text_target"] == approved[r["offset"]], f"target divergiu em {r['offset']}"


def test_export_tm_well_formed(bof4_migrated, tmp_path):
    """translation_memory.jsonl exportado: 1 linha/fala, schema completo, src_key presente."""
    import json
    db_path, _ = bof4_migrated
    result = export(db_path, "bof4", tmp_path)
    lines = [json.loads(ln) for ln in
             (tmp_path / "translation_memory.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == result["tm"], result
    needed = {"scene", "offset", "speaker", "source", "target", "src_key"}
    assert all(needed <= set(e) for e in lines), "entradas de TM mal-formadas"
    assert all(e["src_key"] for e in lines if e["source"]), "src_key vazio p/ source não-vazio"


def test_export_roundtrip_lossless(bof4_migrated, tmp_path):
    """Oráculo do cutover: DB → export approved → re-migrate num DB fresco → mesmas traduções.
    Reusa o approved exportado como se fosse o approved_*.csv de uma cena (mesmo formato)."""
    from migrate_from_flat import migrate
    db_path, _ = bof4_migrated
    export(db_path, "bof4", tmp_path)
    # monta um projeto mínimo que re-importa: 1 "cena" cujo approved_*.csv é o export, com
    # dialogs.csv reconstruído do DB (source por offset) — prova que o par (source,target) sobrevive.
    with Store(db_path) as db:
        tm = db.get_translations("bof4", approved_only=True)
    proj = tmp_path / "proj"
    sc = proj / "artifacts" / "scenes" / "all"
    sc.mkdir(parents=True)
    (proj / "project.json").write_text('{"title":"RT","media_type":"game"}', encoding="utf-8")
    with (sc / "dialogs.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["offset", "text_source"])
        w.writeheader()
        for r in tm:
            w.writerow({"offset": r["offset"], "text_source": r["source"]})
    (sc / "approved_all.csv").write_text(
        (tmp_path / "approved_translations.csv").read_text(encoding="utf-8"), encoding="utf-8")
    fresh = tmp_path / "fresh.db"
    migrate(proj, fresh, project_id="rt")
    with Store(fresh) as db2:
        back = {r["offset"]: r["target"] for r in db2.get_translations("rt", approved_only=True)}
    orig = {r["offset"]: r["target"] for r in tm}
    assert back == orig, "round-trip DB→flat→DB perdeu/alterou traduções"
