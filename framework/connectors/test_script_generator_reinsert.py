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
    """approved_translations.csv com text_target == text_en -> round-trip deve ser byte-idêntico."""
    approved = tmp_path / "artifacts" / "approved_translations.csv"
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
    approved = tmp_path / "artifacts" / "approved_translations.csv"
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


def _filled_token_reinsert(control):
    ev = {"has_control_tokens": True, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    code = sg.generate_reinsert(ev).replace(
        'CONTROL_MAP: list[tuple[bytes, str]] = [\n    # (b"\\x01\\x00", "\\n"),   # MESMA lista do extract.py gerado\n]',
        f"CONTROL_MAP: list[tuple[bytes, str]] = {control!r}",
    ).replace(
        "BYTE_TO_CHAR: dict[int, str] = {\n    # 0x20: \" \", 0x21: \"!\", ... MESMO dict do extract.py gerado\n}",
        'BYTE_TO_CHAR: dict[int, str] = {0x41: "A"}',
    )
    return ev, code


def test_token_table_reinsert_budget_matches_decode_with_multibyte_control(tmp_path):
    """Sequencia de controle contendo o byte terminador (01 00): o decode a consome inteira, entao o
    reinsert tem que medir o MESMO budget (antes parava no 00 interno -> falso 'excede')."""
    ev, code = _filled_token_reinsert([(b"\x01\x00", "[NL]")])
    raw = b"A\x01\x00A\x00"
    src = tmp_path / "game.bin"
    src.write_bytes(raw)
    project_json = _project_json(tmp_path, "game.bin")
    _write_approved_same_as_source(tmp_path, [{"offset": "0x0", "text_en": "A[NL]A"}])
    _exec_module(code, "gen_reinsert_token_multibyte").main(project_json, str(src))
    assert (tmp_path / "output" / "game.bin").read_bytes() == raw


def test_reinsert_stubs_fail_loudly_without_terminator_instead_of_hanging(tmp_path):
    """Sem terminador ate o EOF o scan `while ... != TERMINATOR: end += 1` nunca terminava."""
    import pytest
    for ev, name in (({"has_control_tokens": False, "sample_encodings": {"ascii": 0.3}, "string_density": 0.1}, "ptr"),
                     ({"has_control_tokens": True, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}, "tok")):
        src = tmp_path / f"{name}.bin"
        src.write_bytes(b"AAA")
        project_json = _project_json(tmp_path, src.name)
        _write_approved_same_as_source(tmp_path, [{"offset": "0x0", "text_en": "AAA"}])
        code = _filled_token_reinsert([])[1] if name == "tok" else sg.generate_reinsert(ev)
        mod = _exec_module(code, f"gen_reinsert_noterm_{name}")
        with pytest.raises(SystemExit, match="sem terminador"):
            mod.main(project_json, str(src))


def test_generated_stub_cli_accepts_project_root_dir(tmp_path):
    """connector_smoke/connector_mgr passam a RAIZ do projeto (nao o project.json) como argv[1]."""
    import subprocess
    import sys
    (tmp_path / "game.bin").write_bytes(b"AAA\x00")
    _project_json(tmp_path, "game.bin")
    _write_approved_same_as_source(tmp_path, [{"offset": "0x0", "text_en": "AAA"}])
    stub = tmp_path / "reinsert.py"
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.9}, "string_density": 0.5}
    stub.write_text(sg.generate_reinsert(ev), encoding="utf-8")
    r = subprocess.run([sys.executable, str(stub), str(tmp_path)], capture_output=True, text=True)  # nosec B603
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "output" / "game.bin").read_bytes() == b"AAA\x00"


def test_linear_reinsert_strict_encode_never_writes_question_mark(tmp_path):
    """Char fora do encoding do stub (ex.: 'é' em ascii) falhava em silencio virando '?' no jogo."""
    import pytest
    src = tmp_path / "game.bin"
    src.write_bytes(b"Hello\x00")
    project_json = _project_json(tmp_path, "game.bin")
    _write_approved_same_as_source(tmp_path, [{"offset": "0x0", "text_en": "Hé"}])
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 1.0}, "string_density": 0.9}
    mod = _exec_module(sg.generate_reinsert(ev), "gen_reinsert_linear_strict")
    with pytest.raises((UnicodeEncodeError, SystemExit)):
        mod.main(project_json, str(src))
    out = tmp_path / "output" / "game.bin"
    assert not out.exists() or b"?" not in out.read_bytes()


def test_pointer_reinsert_shrink_keeps_slot_size_and_dir_override_falls_back(tmp_path):
    """Traducao menor preenche o slot ate o budget (em bytes) e um argv[2] que e DIRETORIO
    (connector_smoke passa game_data_dir) cai no source_binary do project.json."""
    s1, s2 = b"Alpha", b"Beta"
    toc = struct.pack("<II", 8, 8 + len(s1) + 1)
    data = toc + s1 + b"\x00" + s2 + b"\x00"
    (tmp_path / "game.bin").write_bytes(data)
    project_json = _project_json(tmp_path, "game.bin")
    ev = {"has_control_tokens": False, "sample_encodings": {"ascii": 0.3}, "string_density": 0.1}
    extract_code = sg.generate(ev).replace("_TOC_ENTRY_COUNT = None", "_TOC_ENTRY_COUNT = 2")
    _exec_module(extract_code, "gen_x_ptr_shrink").main(project_json, str(tmp_path / "game.bin"))
    rows = list(csv.DictReader((tmp_path / "dialogs.csv").open(encoding="utf-8")))
    approved = tmp_path / "artifacts" / "approved_translations.csv"
    approved.parent.mkdir(parents=True, exist_ok=True)
    with approved.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["offset", "text_target"])
        for r in rows:
            w.writerow([r["offset"], "Al" if r["text_en"] == "Alpha" else r["text_en"]])
    _exec_module(sg.generate_reinsert(ev), "gen_r_ptr_shrink").main(project_json, str(tmp_path))   # dir -> fallback
    out = (tmp_path / "output" / "game.bin").read_bytes()
    assert len(out) == len(data) and out[8:14] == b"Al\x00\x00\x00\x00" and out[14:] == data[14:]
