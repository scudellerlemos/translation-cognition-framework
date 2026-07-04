"""Testes de contrato para evidence_collector.py e tier_classifier.py."""
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from evidence_collector import (
    _estimate_encoding,
    _shannon_entropy,
    _string_density,
    collect,
)
from tier_classifier import classify, load_registry

# ---------------------------------------------------------------------------
# evidence_collector
# ---------------------------------------------------------------------------

def _make_dat_dir(tmp_path: Path, n: int = 60, prefix: str = "AREAD") -> Path:
    """Cria n arquivos DAT com conteúdo ASCII + tokens de controle [01][02]."""
    game = tmp_path / "game"
    game.mkdir()
    for i in range(n):
        content = f"Hello world [01]line {i}[02] end\x00".encode("ascii") * 20
        (game / f"{prefix}{i:03d}.DAT").write_bytes(content)
    return game


def test_collect_capcom_dat(tmp_path):
    game = _make_dat_dir(tmp_path, n=60, prefix="AREAD")
    ev = collect(game)
    assert ev["file_count"] == 60
    # família AREAD.DAT deve aparecer
    families_upper = {k.upper(): v for k, v in ev["families"].items()}
    assert any("AREAD" in k for k in families_upper)
    assert ev["has_control_tokens"] is True
    assert ev["string_density"] > 0.5


def test_collect_areas_dat(tmp_path):
    game = tmp_path / "game"
    game.mkdir()
    for i in range(10):
        (game / f"AREAS{i:03d}.DAT").write_bytes(b"text [01]data\x00" * 30)
    ev = collect(game)
    assert ev["file_count"] == 10
    assert ev["has_control_tokens"] is True


def test_collect_nonexistent_dir(tmp_path):
    ev = collect(tmp_path / "nonexistent")
    assert ev["file_count"] == 0
    assert "error" in ev


def test_collect_empty_dir(tmp_path):
    game = tmp_path / "empty"
    game.mkdir()
    ev = collect(game)
    assert ev["file_count"] == 0
    assert ev["families"] == {}


def test_estimate_encoding_ascii():
    data = b"Hello world, this is ASCII text!\x00"
    assert _estimate_encoding(data) == "ascii"


def test_estimate_encoding_binary():
    data = bytes(range(256))
    assert _estimate_encoding(data) == "binary"


def test_shannon_entropy_text():
    text = b"Hello world " * 100
    assert _shannon_entropy(text) < 5.0


def test_shannon_entropy_high():
    import os
    random_data = os.urandom(4096)
    assert _shannon_entropy(random_data) > 6.5


def test_string_density():
    ascii_data = b"Hello world!" * 100
    assert _string_density(ascii_data) > 0.9
    binary_data = bytes(range(256)) * 10
    assert _string_density(binary_data) < 0.5


# ---------------------------------------------------------------------------
# tier_classifier — engine conhecida (Capcom DAT)
# ---------------------------------------------------------------------------

@pytest.fixture
def registry():
    return load_registry()


def _capcom_evidence():
    return {
        "file_count": 120,
        "families": {"AREAD.DAT": 60, "AREAS.DAT": 60},
        "magic_bytes": {},
        "sample_encodings": {"ascii": 0.95, "binary": 0.05},
        "has_control_tokens": True,
        "entropy_mean": 4.2,
        "string_density": 0.62,
    }


def test_classify_known_engine_capcom(registry):
    result = classify(_capcom_evidence(), registry)
    assert result["tier"] == "known_engine"
    assert result["engine_id"] == "capcom_dat_ps1"
    assert result["confidence"] > 0.5
    assert result["blocked"] is False


def _sdat_evidence():
    return {
        "file_count": 45,
        "families": {"SCENE.SDAT": 45},
        "magic_bytes": {"46696c656e616d65ffff": ["SCENE001.sdat"]},
        "sample_encodings": {"utf8": 0.85, "binary": 0.15},
        "has_control_tokens": False,
        "entropy_mean": 4.5,
        "string_density": 0.45,
    }


def test_classify_known_engine_aquaplus(registry):
    result = classify(_sdat_evidence(), registry)
    assert result["tier"] == "known_engine"
    assert result["engine_id"] == "aquaplus_sdat"
    assert result["blocked"] is False


def _unknown_evidence():
    return {
        "file_count": 30,
        "families": {"DATA.BIN": 30},
        "magic_bytes": {"aabbccdd11223344": ["DATA001.BIN"]},
        "sample_encodings": {"ascii": 0.60, "binary": 0.40},
        "has_control_tokens": False,
        "entropy_mean": 4.8,
        "string_density": 0.35,
    }


def test_classify_unknown_engine(registry):
    result = classify(_unknown_evidence(), registry)
    assert result["tier"] == "unknown_engine"
    assert result["engine_id"] is None
    assert result["blocked"] is False


def test_classify_blocked_encrypted(registry):
    evidence = {
        "file_count": 10,
        "families": {"DATA.PKG": 10},
        "magic_bytes": {},
        "sample_encodings": {"binary": 1.0},
        "has_control_tokens": False,
        "entropy_mean": 7.8,
        "string_density": 0.02,
    }
    result = classify(evidence, registry)
    assert result["tier"] == "blocked"
    assert result["blocked"] is True


# ---------------------------------------------------------------------------
# script_generator — stub de engine desconhecida
# ---------------------------------------------------------------------------

def test_script_generator_returns_string():
    from script_generator import generate
    evidence = _unknown_evidence()
    stub = generate(evidence, engine_hint="unknown_engine")
    assert isinstance(stub, str)
    assert len(stub) > 100
    assert "GERADO AUTOMATICAMENTE" in stub


def test_script_generator_is_documented_stub():
    """O stub gerado deve ter marcadores de 'precisa de ajuste' (TODO ou NotImplementedError).

    O script_generator nunca produz código completamente finalizado — sempre há configuração
    específica do jogo que só o dev/LLM pode preencher inspecionando o arquivo real.
    """
    from script_generator import generate
    evidence = _unknown_evidence()
    stub = generate(evidence)
    has_marker = "NotImplementedError" in stub or "TODO" in stub
    assert has_marker, (
        "Stub deve conter TODO ou NotImplementedError indicando configuração pendente. "
        "Padrão linear_scan: verificar que CONFIG section tem '# TODO:'."
    )


# ---------------------------------------------------------------------------
# discover CLI (smoke — sem chamar main())
# ---------------------------------------------------------------------------

def test_discover_run_known_engine(tmp_path, registry):
    from discover import run
    game = _make_dat_dir(tmp_path, n=60)
    exit_code = run(game, as_json=True)
    assert exit_code == 0


def test_discover_run_blocked(tmp_path, registry):
    import os

    from discover import run
    game = tmp_path / "encrypted"
    game.mkdir()
    for i in range(5):
        (game / f"DATA{i:02d}.PKG").write_bytes(os.urandom(8192))
    exit_code = run(game, as_json=True)
    assert exit_code == 1  # bloqueado → exit 1
