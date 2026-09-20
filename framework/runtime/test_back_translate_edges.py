"""test_back_translate_edges.py — back_translate/kb_fetch: ramos de falha (batch que trava/erra,
back_translation ilegível, extratores de PDF/DOCX). Cliente e bibliotecas falsos, sem rede.
"""
import json
import sys
import types
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import back_translate as bt  # noqa: E402
import kb_fetch  # noqa: E402
import paths  # noqa: E402
import pytest  # noqa: E402

SCENE = "ch_95_01"


class _Result:
    def __init__(self, cid, typ="succeeded", message=None):
        self.custom_id = cid
        self.result = types.SimpleNamespace(type=typ, message=message)


def _client(results):
    batches = types.SimpleNamespace(create=lambda requests: types.SimpleNamespace(id="b1"),
                                    results=lambda _id: iter(results))
    return types.SimpleNamespace(messages=types.SimpleNamespace(batches=batches))


@pytest.fixture
def batch_env(monkeypatch):
    monkeypatch.setattr(bt, "_await_batch", lambda *a, **k: True)
    monkeypatch.setattr(bt, "_usage_of", lambda msg: {})
    monkeypatch.setattr(bt, "log_api_call", lambda *a, **k: None)


def test_back_chunk_timeout_marks_every_request(monkeypatch, tmp_path):
    monkeypatch.setattr(bt, "_await_batch", lambda *a, **k: False)
    st = bt._submit_back_chunk(_client([]), [{"custom_id": "a"}, {"custom_id": "b"}], 0, 1, "m", tmp_path)
    assert st == {"a": "timeout", "b": "timeout"}


def test_back_chunk_errored_request_and_unparseable_output(batch_env, monkeypatch, tmp_path):
    paths.scene_dir(tmp_path, SCENE).mkdir(parents=True)
    monkeypatch.setattr(bt, "_text_of", lambda msg: msg)
    results = [_Result("bad_scene", typ="errored"),
               _Result(SCENE, message="isto nao e json"),
               _Result("ch_95_02", message=json.dumps({"entries": [{"offset": "0x1"}]}))]
    paths.scene_dir(tmp_path, "ch_95_02").mkdir(parents=True)
    st = bt._submit_back_chunk(_client(results), [{"custom_id": "x"}], 0, 1, "m", tmp_path)
    assert st == {"bad_scene": "errored", SCENE: "parse_failed", "ch_95_02": "reviewed"}
    saved = json.loads(paths.back_translation(tmp_path, "ch_95_02", "95_02").read_text(encoding="utf-8"))
    assert saved["reviewed"] == 1


def test_invalidate_ignores_unreadable_back_translation(tmp_path):
    paths.scene_dir(tmp_path, SCENE).mkdir(parents=True)
    paths.back_translation(tmp_path, SCENE, "95_01").write_text("{nao e json", encoding="utf-8")
    assert bt.invalidate_back_translation(tmp_path, SCENE, ["0x1"]) == 0


def test_has_stale_is_false_for_unreadable_file(tmp_path):
    f = tmp_path / "bt.json"
    f.write_text("{nao e json", encoding="utf-8")
    assert bt._has_stale(f, [{"offset": "0x1"}]) is False


def test_in_session_back_translate_reports_ready_when_output_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(bt, "_write_back_prompt", lambda *a, **k: None)
    paths.scene_dir(tmp_path, SCENE).mkdir(parents=True)
    paths.back_translation(tmp_path, SCENE, "95_01").write_text("{}", encoding="utf-8")
    r = bt.back_translate(tmp_path, SCENE, [{"offset": "0x1"}], backend="in-session")
    assert r["status"] == bt.READY and r["reviewed"] == 1


# --- kb_fetch: extratores com bibliotecas falsas -----------------------------------------------------
def test_extract_pdf_joins_non_empty_pages(monkeypatch):
    class _Pdf:
        pages = [types.SimpleNamespace(extract_text=lambda: "pag1"),
                 types.SimpleNamespace(extract_text=lambda: None),
                 types.SimpleNamespace(extract_text=lambda: "pag3")]

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda p: _Pdf()))
    assert kb_fetch._extract_pdf(Path("x.pdf")) == "pag1\n\npag3"


def test_extract_docx_skips_blank_paragraphs(monkeypatch):
    doc = types.SimpleNamespace(paragraphs=[types.SimpleNamespace(text="um"),
                                            types.SimpleNamespace(text="   "),
                                            types.SimpleNamespace(text="dois")])
    monkeypatch.setitem(sys.modules, "docx", types.SimpleNamespace(Document=lambda p: doc))
    assert kb_fetch._extract_docx(Path("x.docx")) == "um\ndois"
