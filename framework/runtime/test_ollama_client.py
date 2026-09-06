"""test_ollama_client.py — cobre o cliente REST do Ollama local (ollama_client.py).

urllib.request mockado via monkeypatch (mesmo padrao de test_kb_fetch.py) — sem servidor Ollama
vivo. ollama_client.py e dependencia ativa de kb_build_ollama.py (extracao de KB), nao so um
resquicio do tier de traducao descontinuado (ADR 0008) — por isso vale testar isoladamente.
"""
import io
import json
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import ollama_client as oc  # noqa: E402


class _FakeHttpResponse:
    def __init__(self, data: bytes):
        self._data = data

    def read(self, n=-1):
        if n is None or n < 0:
            return self._data
        return self._data[:n]

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_health_check_true_when_ollama_responds(monkeypatch):
    monkeypatch.setattr(oc.urllib.request, "urlopen", lambda req, timeout=None: _FakeHttpResponse(b"{}"))
    assert oc.health_check() is True


def test_health_check_false_when_unreachable(monkeypatch):
    def _raise(*a, **k):
        raise oc.urllib.error.URLError("connection refused")
    monkeypatch.setattr(oc.urllib.request, "urlopen", _raise)
    assert oc.health_check() is False


def test_list_models_returns_names(monkeypatch):
    body = json.dumps({"models": [{"name": "qwen2.5:14b"}, {"name": "llama3:8b"}]}).encode("utf-8")
    monkeypatch.setattr(oc.urllib.request, "urlopen", lambda req, timeout=None: _FakeHttpResponse(body))
    assert oc.list_models() == ["qwen2.5:14b", "llama3:8b"]


def test_list_models_returns_empty_on_error(monkeypatch):
    def _raise(*a, **k):
        raise oc.urllib.error.URLError("connection refused")
    monkeypatch.setattr(oc.urllib.request, "urlopen", _raise)
    assert oc.list_models() == []


def test_chat_posts_model_and_messages_with_num_ctx(monkeypatch):
    captured = {}

    def _fake_urlopen(req, timeout=None):
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        return _FakeHttpResponse(json.dumps({"message": {"content": "ola"}}).encode("utf-8"))

    monkeypatch.setattr(oc.urllib.request, "urlopen", _fake_urlopen)
    resp = oc._chat("qwen2.5:14b", [{"role": "user", "content": "oi"}])
    assert resp == {"message": {"content": "ola"}}
    assert captured["payload"]["model"] == "qwen2.5:14b"
    assert captured["payload"]["messages"] == [{"role": "user", "content": "oi"}]
    assert captured["payload"]["options"]["num_ctx"] == oc.OLLAMA_NUM_CTX
    assert "format" not in captured["payload"]


def test_chat_includes_format_when_given(monkeypatch):
    captured = {}

    def _fake_urlopen(req, timeout=None):
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        return _FakeHttpResponse(json.dumps({"message": {"content": "{}"}}).encode("utf-8"))

    monkeypatch.setattr(oc.urllib.request, "urlopen", _fake_urlopen)
    oc._chat("qwen2.5:14b", [], fmt="json")
    assert captured["payload"]["format"] == "json"


def test_chat_raises_runtime_error_on_http_error(monkeypatch):
    def _raise(req, timeout=None):
        raise oc.urllib.error.HTTPError(req.full_url, 500, "server error", None, io.BytesIO(b"boom"))
    monkeypatch.setattr(oc.urllib.request, "urlopen", _raise)
    with pytest.raises(RuntimeError, match="Ollama HTTP 500"):
        oc._chat("qwen2.5:14b", [])


def test_chat_raises_runtime_error_on_connection_failure(monkeypatch):
    def _raise(*a, **k):
        raise oc.urllib.error.URLError("connection refused")
    monkeypatch.setattr(oc.urllib.request, "urlopen", _raise)
    with pytest.raises(RuntimeError, match="Ollama inacessível"):
        oc._chat("qwen2.5:14b", [])


def test_text_of_extracts_message_content():
    assert oc._text_of({"message": {"content": "traducao aqui"}}) == "traducao aqui"


def test_text_of_missing_content_returns_empty():
    assert oc._text_of({}) == ""


def test_usage_of_maps_ollama_counters_to_harness_format():
    resp = {"prompt_eval_count": 120, "eval_count": 45}
    assert oc._usage_of(resp) == {"in": 120, "out": 45, "cache_read": 0, "cache_write": 0}


def test_usage_of_defaults_missing_counters_to_zero():
    assert oc._usage_of({}) == {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
