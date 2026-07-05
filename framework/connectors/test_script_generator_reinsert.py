"""test_script_generator_reinsert.py — cobre generate_reinsert() (#108): candidato de
reinsert.py PAREADO com o extract.py de generate() (mesma evidência -> mesmo padrão).

Além do conteúdo gerado (mesmo estilo de test_script_generator.py p/ generate()), EXECUTA
de fato o código gerado contra binários sintéticos e prova que ele round-tripa quando a
tradução aprovada == fonte (mesmo padrão/oráculo de test_roundtrip_synthetic.py dos
conectores reais) -- string-content sozinho não prova que o candidato funciona.
"""
import csv
import importlib.util
import json
import struct
import sys
import types
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import script_generator as sg  # noqa: E402


def _exec_module(code: str, name: str) -> types.ModuleType:
    """Escreve o código GERADO num módulo real e executa -- não só inspeciona a string."""
    spec = importlib.util.spec_from_loader(name, loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(code, name, "exec"), mod.__dict__)  # nosec B102 - código do próprio gerador (sg.generate/generate_reinsert), não input externo/não confiável
    return mod


def _project_json(tmp_path: Path, source_binary: str) -> Path:
    p = tmp_path / "project.json"
    p.write_text(json.dumps({
        "connector": {"source_binary": source_binary},
        "source": {"file": "dialogs.csv", "id_column": "offset"},
    }), encoding="utf-8")
    return p


def _write_approved_same_as_source(tmp_path: Path, rows: list[dict]):
    """approved.csv com text_target == text_en -> round-trip deve ser byte-idêntico."""
    approved = tmp_path / "artifacts" / "approved.csv"
    approved.parent.mkdir(parents=True, exist_ok=True)
    with approved.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["offset", "text_target"])
        for r in rows:
            w.writerow([r["offset"], r["text_en"]])
    return approved


# --- conteúdo gerado (mesmo estilo de test_script_generator.py) ---

def test_generate_reinsert_linear_scan_content():
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    out = sg.generate_reinsert(ev)
    assert "encode_string" in out and "GERADO AUTOMATICAMENTE" in out
    assert "Par de: extract.py" in out


def test_generate_reinsert_token_table_content():
    ev = {"has_control_tokens": True, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    out = sg.generate_reinsert(ev)
    assert "CHAR_TO_BYTE" in out and "BYTE_TO_CHAR" in out


def test_generate_reinsert_pointer_table_content():
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.3}, "string_density": 0.1}
    out = sg.generate_reinsert(ev)
    assert "_STR_ENCODING" in out and "realocação de TOC" in out


# --- execução real contra binário sintético (oráculo de round-trip) ---

def test_linear_scan_extract_reinsert_roundtrip(tmp_path):
    data = b"Hello, world!\x00Bye now!\x00"
    src = tmp_path / "game.bin"
    src.write_bytes(data)
    project_json = _project_json(tmp_path, "game.bin")

    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 1.0}, "string_density": 0.9}
    extract_mod = _exec_module(sg.generate(ev), "gen_extract_linear")
    extract_mod.main(project_json, str(src))

    rows = list(csv.DictReader((tmp_path / "dialogs.csv").open(encoding="utf-8")))
    assert {r["text_en"] for r in rows} == {"Hello, world!", "Bye now!"}
    _write_approved_same_as_source(tmp_path, rows)

    reinsert_mod = _exec_module(sg.generate_reinsert(ev), "gen_reinsert_linear")
    reinsert_mod.main(project_json, str(src))

    assert (tmp_path / "output" / "game.bin").read_bytes() == data


def test_linear_scan_reinsert_rejects_translation_too_long(tmp_path):
    """Sem realocação de TOC neste padrão -- tradução maior que o espaço original é erro
    explícito, não corrupção silenciosa de bytes vizinhos."""
    data = b"Hi!\x00"
    src = tmp_path / "game.bin"
    src.write_bytes(data)
    project_json = _project_json(tmp_path, "game.bin")

    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 1.0}, "string_density": 0.9}
    approved = tmp_path / "artifacts" / "approved.csv"
    approved.parent.mkdir(parents=True)
    with approved.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["offset", "text_target"])
        w.writerow(["0x0", "Hello there, much longer!"])   # não cabe no espaço original

    reinsert_mod = _exec_module(sg.generate_reinsert(ev), "gen_reinsert_linear_overflow")
    try:
        reinsert_mod.main(project_json, str(src))
        raised = False
    except SystemExit:
        raised = True
    assert raised


def test_pointer_table_extract_reinsert_roundtrip(tmp_path):
    # TOC: 2 entradas (uint32 LE) apontando pras strings logo em seguida
    strings_off = 8
    s1, s2 = b"Alpha", b"Beta"
    toc = struct.pack("<II", strings_off, strings_off + len(s1) + 1)
    data = toc + s1 + b"\x00" + s2 + b"\x00"
    src = tmp_path / "game.bin"
    src.write_bytes(data)
    project_json = _project_json(tmp_path, "game.bin")

    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.3}, "string_density": 0.1}
    extract_code = sg.generate(ev)
    # candidato exige _TOC_ENTRY_COUNT explícito (None assume 1º uint32 = contagem, não é
    # o caso deste teste) -- ajusta a constante, mesmo tipo de adaptação que o dev/agente faria
    extract_code = extract_code.replace("_TOC_ENTRY_COUNT = None", "_TOC_ENTRY_COUNT = 2")
    extract_mod = _exec_module(extract_code, "gen_extract_ptr")
    extract_mod.main(project_json, str(src))

    rows = list(csv.DictReader((tmp_path / "dialogs.csv").open(encoding="utf-8")))
    assert {r["text_en"] for r in rows} == {"Alpha", "Beta"}
    _write_approved_same_as_source(tmp_path, rows)

    reinsert_mod = _exec_module(sg.generate_reinsert(ev), "gen_reinsert_ptr")
    reinsert_mod.main(project_json, str(src))

    assert (tmp_path / "output" / "game.bin").read_bytes() == data


def test_token_table_encode_decode_are_inverse_once_table_filled(tmp_path):
    """BYTE_TO_CHAR/CONTROL_MAP nascem vazios (dev/agente preenche lendo a tabela do jogo,
    ver docstring do stub) -- injeta uma tabela mínima real e prova que decode(encode(x))==x,
    o mesmo contrato que extract.py/reinsert.py real (BoF4) já garante hoje."""
    ev = {"has_control_tokens": True, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}

    extract_code = sg.generate(ev).replace(
        "BYTE_TO_CHAR: dict[int, str] = {\n    # 0x20: \" \", 0x21: \"!\", ... preencher do table_schema do jogo\n}",
        'BYTE_TO_CHAR: dict[int, str] = {0x41: "A", 0x42: "B", 0x43: "C"}',
    ).replace(
        'CONTROL_MAP: list[tuple[bytes, str]] = [\n    # (b"\\x01\\x00", "\\n"),   # exemplo: control code → token\n    # ordenar por comprimento DECRESCENTE p/ casar sequências longas primeiro\n]',
        'CONTROL_MAP: list[tuple[bytes, str]] = [(b"\\x01", "[NL]")]',
    )
    reinsert_code = sg.generate_reinsert(ev).replace(
        "BYTE_TO_CHAR: dict[int, str] = {\n    # 0x20: \" \", 0x21: \"!\", ... MESMO dict do extract.py gerado\n}",
        'BYTE_TO_CHAR: dict[int, str] = {0x41: "A", 0x42: "B", 0x43: "C"}',
    ).replace(
        'CONTROL_MAP: list[tuple[bytes, str]] = [\n    # (b"\\x01\\x00", "\\n"),   # MESMA lista do extract.py gerado\n]',
        'CONTROL_MAP: list[tuple[bytes, str]] = [(b"\\x01", "[NL]")]',
    )

    extract_mod = _exec_module(extract_code, "gen_extract_token")
    reinsert_mod = _exec_module(reinsert_code, "gen_reinsert_token")

    raw = b"ABC\x01A\x00"   # "A","B","C", control 0x01 ("[NL]"), "A", terminador
    table = extract_mod.load_table(Path("."))
    text, _budget = extract_mod.decode_string(raw, 0, table)
    assert text == "ABC[NL]A"

    reencoded = reinsert_mod.encode_string(text)
    assert reencoded == raw
