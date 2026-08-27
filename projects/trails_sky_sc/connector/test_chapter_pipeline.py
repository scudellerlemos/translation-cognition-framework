"""
test_chapter_pipeline.py — Trails in the Sky 2nd Chapter (D6b)

Cobre build_plan_chapter._structural_token_rx (tokens de formatacao de project.json) e
verify_chapter._rebuild (oraculos de round-trip/apply/readback/no-corruption sobre o buffer
FPAC compartilhado) — a logica nova escrita nesta sessao pra fechar a Fase D6b.

Reusa o fixture FPAC sintetico de test_roundtrip_synthetic.py (mesmo container, sem depender
do jogo real/gitignored).

Rodar: pytest connector/test_chapter_pipeline.py -v
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "connector"))
from build_plan_chapter import _structural_token_rx  # noqa: E402
from reinsert import read_scena_strings  # noqa: E402
from test_roundtrip_synthetic import _fixture_pac, _load  # noqa: E402
from verify_chapter import _rebuild  # noqa: E402


def test_structural_token_rx_matches_project_tokens(tmp_path):
    (tmp_path / "project.json").write_text(json.dumps({
        "formatting_tokens": ["<R>"],
        "formatting_token_patterns": [r"<C\d+>"],
    }), encoding="utf-8")
    rx = _structural_token_rx(tmp_path)
    assert rx.findall("hi <C1> there <R> bye") == ["<C1>", "<R>"]
    assert rx.findall("no tokens here") == []


def test_structural_token_rx_empty_when_no_config(tmp_path):
    (tmp_path / "project.json").write_text("{}", encoding="utf-8")
    rx = _structural_token_rx(tmp_path)
    assert rx.findall("<anything>") == []


def _scene_dialogs():
    """Monta o dict de dialogs.csv da cena (offset -> {text_en, file, byte_budget}) direto do
    fixture sintetico, com budget = len(text_en)+1 exato (mesma convencao do extract.py real)."""
    data, entries = _load(_fixture_pac())
    original = read_scena_strings(data, entries)
    return {
        off: {"text_en": text, "file": off.partition(":")[0], "byte_budget": len(text.encode("utf-8")) + 1}
        for off, text in original.items()
    }


def _write_pac(tmp_path, monkeypatch):
    data, _entries = _load(_fixture_pac())
    pac_dir = tmp_path / "pac" / "steam"
    pac_dir.mkdir(parents=True)
    (pac_dir / "script_en.pac").write_bytes(data)
    monkeypatch.setenv("TRAILS_SKY_SC_DATA_DIR", str(tmp_path))


def test_rebuild_roundtrip_and_apply_ok(tmp_path, monkeypatch):
    _write_pac(tmp_path, monkeypatch)
    dialogs = _scene_dialogs()
    target = next(off for off, m in dialogs.items() if m["text_en"] == "My name is Estelle Bright.")
    approved = {target: "Meu nome e Estelle Bright."}

    round_trip_ok, fitting_failure, fails = _rebuild("e0000", dialogs, approved, None)

    assert round_trip_ok, fails
    assert not fitting_failure
    assert fails == []


def test_rebuild_flags_individual_overflow_as_fitting_only(tmp_path, monkeypatch):
    _write_pac(tmp_path, monkeypatch)
    dialogs = _scene_dialogs()
    target = next(off for off, m in dialogs.items() if m["text_en"] == "My name is Estelle Bright.")
    approved = {target: "Um texto em portugues bem mais longo que o budget original permite"}

    round_trip_ok, fitting_failure, fails = _rebuild("e0000", dialogs, approved, None)

    assert round_trip_ok
    assert fitting_failure
    assert any("individual_overflow" in f for f in fails)


def test_rebuild_does_not_touch_bytes_outside_scene(tmp_path, monkeypatch):
    """A entry ani/fis0016.dat (fora de scena/, fora do escopo) precisa sair intacta."""
    _write_pac(tmp_path, monkeypatch)
    dialogs = _scene_dialogs()
    target = next(iter(dialogs))
    approved = {target: "Ola"}

    round_trip_ok, fitting_failure, fails = _rebuild("e0000", dialogs, approved, None)

    assert round_trip_ok
    assert not any("fora da cena" in f for f in fails)
