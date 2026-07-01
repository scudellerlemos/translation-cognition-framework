"""test_quality_review.py — cobre os sinais determinísticos do piso de QA (flags/caixa/display) e
o export/write_csv. Sem rede: tudo deriva do plano/tradução em disco.
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402
import quality_review as qr  # noqa: E402


def test_display_text_cleans_bof4_codes():
    out = qr._display_text("[01]Ola[02]Mundo[C1]")
    assert "[01]" not in out and "[C1]" not in out and "Ola" in out and "Mundo" in out
    assert qr._display_text("sem codigos") == "sem codigos"     # sem [XX] -> intocado


def test_flags_signals():
    assert "identico-fonte" in qr._flags("Hello", "Hello", "low", False)
    assert "risco:high" in qr._flags("a", "b", "high", False)
    assert "amostra" in qr._flags("a", "b", "low", True)
    assert "micro-qa:revise" in qr._flags("a", "b", "low", False, bt_revise=True)
    assert qr._flags("ok", "beleza", "low", False) == ""        # sem sinal


def test_box_verdict_fits_and_overflows():
    assert qr._box_verdict("Hello there", "Oi") == ""           # menor -> cabe
    v = qr._box_verdict("Hi", "X" * 80)                          # muito mais largo
    assert v.startswith("ESTOUROU") or v.startswith("rever")


def test_envelope_counts_segments():
    w, n = qr._envelope("linha um\\nlinha dois")
    assert n == 2 and w > 0


def _scene_with_plan(root: Path, scene="ch_11_01"):
    sid = context_pack.scene_id_of(scene)
    sd = paths.scene_dir(root, scene)
    sd.mkdir(parents=True)
    (sd / "dialogs.csv").write_text("offset,text_source\nX:0:1,Hello there friend\n", encoding="utf-8")
    paths.translation_plan(root, scene, sid).write_text(json.dumps({
        "scene_group": sid,
        "lines": [{"offset": "X:0:1", "text_source": "Hello there friend",
                   "base_translation": "Olá amigo", "risk_level": "high", "speaker": "Ryu"}]}),
        encoding="utf-8")
    paths.translations(root, scene, sid).write_text(json.dumps(
        {"lines": {"X:0:1": {"t": "Olá amigo"}}}), encoding="utf-8")
    (root / "project.json").write_text('{"title":"T","media_type":"game"}', encoding="utf-8")


def test_export_and_write_csv(tmp_path):
    _scene_with_plan(tmp_path)
    rows = qr.export(tmp_path, "11")
    assert rows and rows[0]["offset"] == "X:0:1" and rows[0]["risk"] == "high"
    assert "risco:high" in rows[0]["revisar"]
    out = tmp_path / "r.csv"
    qr.write_csv(rows, out)
    assert out.is_file() and "X:0:1" in out.read_text(encoding="utf-8-sig")


def test_bt_revise_offsets_reads_verdicts(tmp_path):
    _scene_with_plan(tmp_path)
    sid = context_pack.scene_id_of("ch_11_01")
    paths.back_translation(tmp_path, "ch_11_01", sid).write_text(json.dumps(
        {"entries": [{"offset": "X:0:1", "verdict": "revise"},
                     {"offset": "X:0:2", "verdict": "revise", "stale": True}]}), encoding="utf-8")
    off = qr._bt_revise_offsets(tmp_path, "ch_11_01")
    assert "X:0:1" in off and "X:0:2" not in off       # stale ignorado


def test_width_violations_filters_estourou(tmp_path):
    _scene_with_plan(tmp_path)
    # força um estouro: target muito largo
    sid = context_pack.scene_id_of("ch_11_01")
    paths.translations(tmp_path, "ch_11_01", sid).write_text(json.dumps(
        {"lines": {"X:0:1": {"t": "X" * 120}}}), encoding="utf-8")
    v = qr.width_violations(tmp_path, "11")
    assert v and v[0]["caixa"].startswith("ESTOUROU")
