"""test_discover.py — cobre run()/--generate-stub do CLI de descoberta.

#108: --generate-stub gerava só extract.py, forçando reinsert.py a ser sempre 100% manual.
Agora gera o PAR (mesma evidência -> mesmo padrão). known_engine/blocked nunca geram nada
(existence_gate() já formaliza isso, coberto em test_tier_classifier_gate.py) -- aqui cobrimos
o efeito em discover.run() especificamente para unknown_engine.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import discover  # noqa: E402

_UNKNOWN_EVIDENCE = {
    "file_count": 3, "families": {}, "magic_bytes": {},
    "sample_encodings": {"ascii": 0.9}, "has_control_tokens": False,
    "entropy_mean": 4.0, "string_density": 0.5,
}


def _stub_collect_and_registry(monkeypatch, evidence):
    monkeypatch.setattr(discover, "collect", lambda game_dir: evidence)
    monkeypatch.setattr(discover, "load_registry", lambda: [])


def test_generate_stub_writes_extract_and_reinsert_pair(tmp_path, monkeypatch):
    _stub_collect_and_registry(monkeypatch, _UNKNOWN_EVIDENCE)
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    out_dir = tmp_path / "connector"

    rc = discover.run(game_dir, generate_stub=out_dir)

    assert rc == 0
    extract = out_dir / "extract.py"
    reinsert = out_dir / "reinsert.py"
    assert extract.is_file() and reinsert.is_file()
    assert "GERADO AUTOMATICAMENTE" in extract.read_text(encoding="utf-8")
    assert "GERADO AUTOMATICAMENTE" in reinsert.read_text(encoding="utf-8")
    assert "Par de: extract.py" in reinsert.read_text(encoding="utf-8")


def test_generate_stub_pair_uses_same_pattern(tmp_path, monkeypatch):
    """extract.py e reinsert.py candidatos precisam vir do MESMO padrão (mesma evidência) --
    nunca um token_table pareado com um pointer_table, por exemplo."""
    ev = dict(_UNKNOWN_EVIDENCE, has_control_tokens=True)
    _stub_collect_and_registry(monkeypatch, ev)
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    out_dir = tmp_path / "connector"

    discover.run(game_dir, generate_stub=out_dir)

    extract_txt = (out_dir / "extract.py").read_text(encoding="utf-8")
    reinsert_txt = (out_dir / "reinsert.py").read_text(encoding="utf-8")
    assert "Padrão escolhido: TOKEN_TABLE" in extract_txt
    assert "Padrão escolhido: TOKEN_TABLE" in reinsert_txt


def test_generate_stub_not_written_when_dir_missing_flag(tmp_path, monkeypatch):
    """Sem --generate-stub (generate_stub=None): só reporta, não escreve nada."""
    _stub_collect_and_registry(monkeypatch, _UNKNOWN_EVIDENCE)
    game_dir = tmp_path / "game"
    game_dir.mkdir()

    rc = discover.run(game_dir, generate_stub=None)

    assert rc == 0
    assert not (tmp_path / "extract.py").exists()
