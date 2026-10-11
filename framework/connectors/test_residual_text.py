"""residual_text: extracao que corta a string no primeiro 0x00 passa no round-trip mas deixa texto para tras."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import residual_text  # noqa: E402

# 3 falas no estilo Capcom DAT: [14][00][00] = speaker com parametro 0x00, texto continua depois dele
_LINES = [b'\x14\x00\x00"So what was in this\x01crater you found today?"',
          b'\x14\x00\x00"It was a giant monster,\x01I tell you the truth!"',
          b'"You hear all kinds of\x01things in places like this."']


def _project(tmp_path, texts):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "A.DAT").write_bytes(b"\x00".join(_LINES) + b"\x00")
    with open(tmp_path / "dialogs.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "text_en"])
        w.writerows(["A.DAT", t] for t in texts)
    return tmp_path / "dialogs.csv", tmp_path / "src"


def test_extracao_completa_passa(tmp_path):
    full = ['[14][00][00]"So what was in this[01]crater you found today?"',
            '[14][00][00]"It was a giant monster,[01]I tell you the truth!"',
            '"You hear all kinds of[01]things in places like this."']
    r = residual_text.check(*_project(tmp_path, full))
    assert r["passed"] and r["n_residual"] == 0 and r["n_runs"] == 6


def test_corte_no_primeiro_zero_bloqueia(tmp_path):
    cut = ["[14]", "[14]", '"You hear all kinds of[01]things in places like this."']
    r = residual_text.check(*_project(tmp_path, cut))
    assert not r["passed"] and r["n_residual"] == 4 and r["per_file"] == [("A.DAT", 4, 6)]


def test_binario_sem_ascii_nao_bloqueia(tmp_path):
    csv_path, src = _project(tmp_path, ["qualquer"])
    (src / "A.DAT").write_bytes(bytes(range(128, 256)) * 50)
    r = residual_text.check(csv_path, src)
    assert r["passed"] and r["n_runs"] == 0
