"""test_kb_fetch.py — cobre a busca/normalizacao de fontes de KB (kb_fetch.py), sem LLM.

fetch_one (pura, sem cache) + fetch_and_cache (grava front-matter em artifacts/research_cache/).
URL mockada via monkeypatch de urllib.request.urlopen; sem rede real.
"""
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import kb_fetch  # noqa: E402
import paths  # noqa: E402


def test_fetch_local_text_file(tmp_path):
    f = tmp_path / "lore.md"
    f.write_text("# Titulo\nTexto de lore local.", encoding="utf-8")
    r = kb_fetch.fetch_one(str(f))
    assert r["tipo"] == "md" and "Texto de lore local." in r["texto"] and r["truncado"] is False


def test_fetch_local_missing_raises(tmp_path):
    with pytest.raises(RuntimeError, match="nao encontrada"):
        kb_fetch.fetch_one(str(tmp_path / "nao_existe.txt"))


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


def test_fetch_url_strips_html(monkeypatch):
    html = b"<html><body><script>ignore()</script><h1>Titulo</h1><p>Paragrafo um.</p></body></html>"
    monkeypatch.setattr(kb_fetch.urllib.request, "urlopen", lambda req, timeout=None: _FakeHttpResponse(html))
    r = kb_fetch.fetch_one("https://exemplo.test/wiki/X")
    assert r["tipo"] == "url"
    assert "Titulo" in r["texto"] and "Paragrafo um." in r["texto"]
    assert "ignore()" not in r["texto"]
    assert r["truncado"] is False


def test_fetch_url_unclosed_script_does_not_swallow_rest_of_page(monkeypatch):
    # regressao: <script> sem fechamento (HTML malformado real, ou cortado no teto de bytes) travava
    # um contador de profundidade em aberto p/ sempre -> todo texto DEPOIS era descartado em silencio.
    html = (b"<html><body><script>var x = 1;"
            b"<h1>Titulo Real</h1><p>Conteudo apos o script sem fechamento.</p></body></html>")
    monkeypatch.setattr(kb_fetch.urllib.request, "urlopen", lambda req, timeout=None: _FakeHttpResponse(html))
    r = kb_fetch.fetch_one("https://exemplo.test/malformado")
    assert "Titulo Real" in r["texto"]
    assert "Conteudo apos o script sem fechamento." in r["texto"]


def test_fetch_url_truncates_oversized_response(monkeypatch):
    big = b"<p>" + b"x" * (kb_fetch._MAX_BYTES + 100) + b"</p>"
    monkeypatch.setattr(kb_fetch.urllib.request, "urlopen", lambda req, timeout=None: _FakeHttpResponse(big))
    r = kb_fetch.fetch_one("https://exemplo.test/grande")
    assert r["truncado"] is True


def test_fetch_and_cache_writes_frontmatter(tmp_path):
    f = tmp_path / "nota.txt"
    f.write_text("conteudo da nota", encoding="utf-8")
    out = kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="2026-07-03T00:00:00+00:00")
    assert out == paths.research_cache(tmp_path, kb_fetch._hash_of(str(f)))
    raw = out.read_text(encoding="utf-8")
    assert "fonte:" in raw and str(f) in raw
    assert "tipo: txt" in raw
    assert "fetched_em: 2026-07-03T00:00:00+00:00" in raw
    assert "truncado: false" in raw
    assert raw.strip().endswith("conteudo da nota")


def test_fetch_and_cache_same_source_same_hash(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    out1 = kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="t1")
    out2 = kb_fetch.fetch_and_cache(tmp_path, str(f), fetched_em="t2")
    assert out1 == out2   # re-fetch da MESMA fonte -> mesmo arquivo (sobrescreve, idempotente)


def test_fetch_pdf_missing_dep_raises_clear_error(tmp_path, monkeypatch):
    import builtins
    real_import = builtins.__import__

    def _no_pdfplumber(name, *a, **k):
        if name == "pdfplumber":
            raise ImportError("no module named pdfplumber")
        return real_import(name, *a, **k)
    monkeypatch.setattr(builtins, "__import__", _no_pdfplumber)
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-fake")
    with pytest.raises(RuntimeError, match="pdfplumber"):
        kb_fetch.fetch_one(str(f))
