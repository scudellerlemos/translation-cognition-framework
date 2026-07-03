"""test_fingerprint_monitor.py — cobre o manifesto/fingerprint de conector (D3).

Puro/determinista: nenhuma funcao chama datetime.now() -- timestamp e passado pelo caller.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import fingerprint_monitor as fm  # noqa: E402


def test_compute_fingerprint_deterministic_and_order_independent(tmp_path):
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"hello")
    b.write_bytes(b"world")
    fp1 = fm.compute_fingerprint([a, b])
    fp2 = fm.compute_fingerprint([b, a])   # ordem de entrada diferente -- mesmo resultado (sorted)
    assert fp1 == fp2


def test_compute_fingerprint_sensitive_to_byte_change(tmp_path):
    a = tmp_path / "a.bin"
    a.write_bytes(b"hello")
    fp1 = fm.compute_fingerprint([a])
    a.write_bytes(b"hellp")   # 1 byte diferente
    fp2 = fm.compute_fingerprint([a])
    assert fp1 != fp2


def test_write_and_read_manifest_roundtrip(tmp_path):
    out = fm.write_manifest(
        tmp_path, tier="T1", engine_id="unity_addressables_csv", connector_version=1,
        scripts_fingerprint="abc123", source_sample_files=[tmp_path / "f.bundle"],
        source_fingerprint="def456", timestamp_iso="2026-07-03T00:00:00+00:00",
        status="green", at_scene="AREAD001",
    )
    assert out.is_file()
    manifest = fm.read_manifest(tmp_path)
    assert manifest["tier"] == "T1"
    assert manifest["scripts_fingerprint"] == "abc123"
    assert manifest["source_fingerprint"] == "def456"
    assert manifest["last_validated"] == {"status": "green", "at_scene": "AREAD001",
                                          "timestamp_iso": "2026-07-03T00:00:00+00:00"}


def test_read_manifest_missing_returns_none(tmp_path):
    assert fm.read_manifest(tmp_path) is None


def test_check_source_drift_detects_change(tmp_path):
    fm.write_manifest(tmp_path, tier="T1", engine_id="x", connector_version=1,
                      scripts_fingerprint="s", source_sample_files=[], source_fingerprint="OLD",
                      timestamp_iso="t")
    assert fm.check_source_drift(tmp_path, "OLD") is False
    assert fm.check_source_drift(tmp_path, "NEW") is True


def test_check_source_drift_true_when_no_manifest(tmp_path):
    assert fm.check_source_drift(tmp_path, "whatever") is True


def test_check_scripts_drift_reuses_connector_hash(tmp_path, monkeypatch):
    import connector_mgr
    monkeypatch.setattr(connector_mgr, "_connector_hash", lambda root, cfg: "CURRENT_HASH")
    monkeypatch.setattr(fm, "_connector_hash", connector_mgr._connector_hash)
    fm.write_manifest(tmp_path, tier="T1", engine_id="x", connector_version=1,
                      scripts_fingerprint="CURRENT_HASH", source_sample_files=[],
                      source_fingerprint="s", timestamp_iso="t")
    assert fm.check_scripts_drift(tmp_path, {}) is False
    monkeypatch.setattr(fm, "_connector_hash", lambda root, cfg: "DIFFERENT_HASH")
    assert fm.check_scripts_drift(tmp_path, {}) is True
