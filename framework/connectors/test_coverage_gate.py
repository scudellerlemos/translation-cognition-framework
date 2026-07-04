"""test_coverage_gate.py — cobre o dry-run de cobertura do candidato de engine desconhecida, sem
precisar de jogo real: escreve um candidato sintetico (scanner ASCII null-terminated simples) +
"arquivos de jogo" fake com bytes conhecidos, e mede cobertura contra eles.
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import coverage_gate as cg  # noqa: E402

_CANDIDATE_SRC = '''
def iter_string_offsets(data, project_cfg):
    i = 0
    while i < len(data):
        if 0x20 <= data[i] <= 0x7E:
            start = i
            while i < len(data) and data[i] != 0:
                i += 1
            if i - start >= 2:
                yield start
            i += 1
        else:
            i += 1

def decode_string(data, offset, table):
    end = offset
    while end < len(data) and data[end] != 0:
        end += 1
    text = data[offset:end].decode("ascii", errors="replace")
    return text, (end + 1) - offset

def load_table(table_path):
    return None
'''

_INCOMPLETE_CANDIDATE_SRC = '''
def iter_string_offsets(data, project_cfg):
    return iter(())

def load_table(table_path):
    return None
'''   # falta decode_string -- contrato incompleto de proposito


def _write_candidate(tmp_path, src=_CANDIDATE_SRC) -> Path:
    p = tmp_path / "candidate.py"
    p.write_text(src, encoding="utf-8")
    return p


def _write_game_file(game_dir: Path, name: str, strings: list[bytes], padding: int = 0) -> Path:
    game_dir.mkdir(parents=True, exist_ok=True)
    data = b"\x00".join(strings) + b"\x00" + b"\xff" * padding
    p = game_dir / name
    p.write_bytes(data)
    return p


def test_load_candidate_imports_dynamically(tmp_path):
    p = _write_candidate(tmp_path)
    mod = cg.load_candidate(p)
    assert hasattr(mod, "iter_string_offsets") and hasattr(mod, "decode_string")


def test_load_candidate_raises_clear_error_on_incomplete_contract(tmp_path):
    p = _write_candidate(tmp_path, _INCOMPLETE_CANDIDATE_SRC)
    try:
        cg.load_candidate(p)
        raise AssertionError("deveria ter levantado ImportError")
    except ImportError as e:
        assert "decode_string" in str(e)


def test_pick_sample_files_returns_largest_n(tmp_path):
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    (game_dir / "small.bin").write_bytes(b"x" * 10)
    (game_dir / "big.bin").write_bytes(b"x" * 1000)
    (game_dir / "medium.bin").write_bytes(b"x" * 100)
    sample = cg.pick_sample_files(game_dir, n=2)
    assert [p.name for p in sample] == ["big.bin", "medium.bin"]


def test_file_coverage_full_extraction(tmp_path):
    candidate = cg.load_candidate(_write_candidate(tmp_path))
    game_dir = tmp_path / "game"
    f = _write_game_file(game_dir, "a.bin", [b"Hello world", b"Another string"])
    r = cg.file_coverage(candidate, f)
    assert r["n_strings"] == 2 and r["coverage_ratio"] >= 0.9


def test_file_coverage_partial_extraction_reports_low_ratio(tmp_path):
    # candidato que so acha 1 string, mas o arquivo tem muito mais texto -- cobertura baixa
    partial_src = _CANDIDATE_SRC.replace(
        "if i - start >= 2:\n                yield start",
        "if i - start >= 2 and start == 0:\n                yield start",
    )
    candidate = cg.load_candidate(_write_candidate(tmp_path, partial_src))
    game_dir = tmp_path / "game"
    f = _write_game_file(game_dir, "a.bin", [b"Hello world", b"Lots more text here too"])
    r = cg.file_coverage(candidate, f)
    assert r["n_strings"] == 1
    assert r["coverage_ratio"] < 0.9


def test_check_fails_below_floor(tmp_path):
    partial_src = _CANDIDATE_SRC.replace(
        "if i - start >= 2:\n                yield start",
        "if i - start >= 2 and start == 0:\n                yield start",
    )
    candidate_path = _write_candidate(tmp_path, partial_src)
    game_dir = tmp_path / "game"
    for i in range(3):
        _write_game_file(game_dir, f"f{i}.bin",
                         [b"Hello world " * 5, b"Lots more real text content here too " * 5])
    r = cg.check(candidate_path, game_dir, floor=0.85, min_files=3)
    assert r["passed"] is False
    assert any("piso" in p for p in r["problems"])


def test_check_fails_with_fewer_than_min_files(tmp_path):
    candidate_path = _write_candidate(tmp_path)
    game_dir = tmp_path / "game"
    _write_game_file(game_dir, "only.bin", [b"Hello world"])
    r = cg.check(candidate_path, game_dir, min_files=3)
    assert r["passed"] is False
    assert any("precisa de >=" in p for p in r["problems"])


def test_check_passes_full_coverage(tmp_path):
    candidate_path = _write_candidate(tmp_path)
    game_dir = tmp_path / "game"
    for i in range(3):
        _write_game_file(game_dir, f"f{i}.bin", [b"Hello world", b"Another full string here"])
    r = cg.check(candidate_path, game_dir, floor=0.85, min_files=3)
    assert r["passed"] is True
    assert r["min_coverage"] >= 0.85
