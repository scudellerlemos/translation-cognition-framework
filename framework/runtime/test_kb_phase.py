"""test_kb_phase.py — cobre o driver de Fase 0 (descoberta de gap de KB + validação de cobertura).

Usa o modo flat ("all", lê artifacts/dialogs.csv). Testa os helpers determinísticos de limpeza de
candidato + discover/coverage/apply_frontier/write_worklist. kb_review.blocking é mockado (outro módulo).
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_phase as kp  # noqa: E402
import paths  # noqa: E402


def test_clean_cand_variants():
    assert kp._clean_cand("Despite Maroro") == "Maroro"             # stopword de borda
    assert kp._clean_cand("CARRY") == ""                            # ALL-CAPS = grito
    assert kp._clean_cand("M-Maroro") == "Maroro"                   # gagueira
    assert kp._clean_cand("Oshtor's") == "Oshtor"                   # possessivo


def test_norm_tok_and_covered():
    assert kp._norm_tok("Haku!") == "Haku"
    kb = kp._kb_blob_from(["Haku"], ["Ukon"])
    assert kp._covered("Master Haku", kb) is True                   # núcleo 'Haku' na KB
    assert kp._covered("Oshtor", kb) is False


def test_midsentence():
    assert kp._midsentence("Oshtor", "then, Oshtor spoke") is True
    assert kp._midsentence("What", "What is that?") is False


def _flat_project(root: Path, source_lines, glossary="term,aliases\nHaku,\n", frontier="0"):
    (root / "artifacts").mkdir(parents=True, exist_ok=True)
    body = "offset,text_source,byte_budget\n" + "".join(
        f'X:0:{i},"{s}",40\n' for i, s in enumerate(source_lines))
    paths.dialogs_flat(root).write_text(body, encoding="utf-8")
    paths.glossary(root).write_text(glossary, encoding="utf-8")
    (root / "project.json").write_text(
        f'{{"title":"T","media_type":"game","kb_frontier":"{frontier}"}}', encoding="utf-8")


def test_discover_flat_gap_and_covered(tmp_path):
    _flat_project(tmp_path, ["When Oshtor arrived, Oshtor bowed.", "Master Haku smiled."])
    d = kp.discover(tmp_path, "all")
    assert "Oshtor" in {r["cand"] for r in d["gap"]}                # não coberto
    assert any("Haku" in r["cand"] for r in d["covered"])          # 'Master Haku' -> núcleo Haku coberto


def test_coverage_ok_and_apply_frontier(tmp_path, monkeypatch):
    _flat_project(tmp_path, ["Haku spoke softly."])
    paths.research_log(tmp_path).write_text("**Status:** reconciled\n", encoding="utf-8")
    monkeypatch.setattr(kp.kb_review, "blocking", lambda r, c, strict=False: [])
    cov = kp.coverage(tmp_path, "all")
    assert cov["problems"] == []                                    # tudo coberto + reconciliado
    assert kp.apply_frontier(tmp_path, "all") == "all"
    assert '"kb_frontier":"all"' in (tmp_path / "project.json").read_text(encoding="utf-8")


def test_coverage_blocks_on_uncovered_recurrent(tmp_path, monkeypatch):
    # 'Oshtor' recorre >=3x, não coberto -> bloqueia; sem research reconciliada -> +1 problema
    _flat_project(tmp_path, ["Oshtor came.", "Then Oshtor spoke, Oshtor left.", "Oshtor again."])
    monkeypatch.setattr(kp.kb_review, "blocking", lambda r, c, strict=False: [])
    cov = kp.coverage(tmp_path, "all")
    assert cov["problems"]                                          # block + sem reconciled


def test_write_worklist(tmp_path):
    _flat_project(tmp_path, ["When Oshtor came, Oshtor left."])
    out = kp.write_worklist(tmp_path, "all")
    assert out.is_file() and "worklist" in out.read_text(encoding="utf-8").lower()
