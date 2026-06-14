"""llm_client.py — PLUMBING da API (cliente, auth, streaming, backoff, usage).

Extraido do model.py (god-module). Aqui fica TODO o acoplamento com o SDK anthropic e a resiliencia de
rede — sem nenhuma logica de traducao. `model`/`batch`/`back_translate` importam daqui (re-exportado por
`model` p/ compat). Import de anthropic/httpx e PREGUICOSO (so quando o backend api roda) -> import e
testes do harness nao exigem o SDK. NAO importa model (camada abaixo).
"""
from __future__ import annotations
import os
import time
from pathlib import Path

import context_pack  # noqa: E402  (CARTA_PATH / _read)

_HERE = Path(__file__).resolve().parent
_MAX_BACKOFF = 4        # tentativas de rede com backoff exponencial


def _load_dotenv():
    """Carrega um `.env` (KEY=VALUE) p/ os.environ SEM dependencia externa. Nao sobrescreve
    variavel ja setada no ambiente (env real vence). Procura na raiz do framework e no CWD."""
    roots = [_HERE.parent.parent, Path.cwd()]   # framework/ (raiz do repo) e diretorio de execucao
    for base in roots:
        f = base / ".env"
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("backend 'api' requer o pacote 'anthropic' (pip install anthropic). "
                           "Use backend 'in-session' p/ o caminho assinatura.") from e
    _load_dotenv()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or "cole-sua-chave" in key:
        raise RuntimeError("backend 'api' requer ANTHROPIC_API_KEY: edite o `.env` na raiz do "
                           "framework e troque o placeholder pela sua chave real (veja .env.example).")
    # timeout generoso (fetch de resultados de batch grande) + retries do PROPRIO SDK (1a linha de
    # defesa em 429/500/timeout/conexao); o _with_backoff por cima cobre o que escapar (2a linha).
    return anthropic.Anthropic(timeout=900.0, max_retries=5)


def _carta_text() -> str:
    return context_pack._read(context_pack.CARTA_PATH)


def _transient_errors():
    """Erros de rede TRANSITORIOS (curam com retry): 429/500/timeout + quedas de conexao httpx. NAO
    inclui 400 BadRequest (esse nao 'cura'). Lazy import (anthropic/httpx so quando o backend api roda)."""
    import anthropic
    import httpx
    return (anthropic.RateLimitError, anthropic.InternalServerError,
            anthropic.APITimeoutError, anthropic.APIConnectionError,
            httpx.RemoteProtocolError, httpx.ReadError, httpx.ReadTimeout,
            httpx.ConnectError, httpx.ConnectTimeout)


def _with_backoff(fn):
    """Executa fn() com backoff exponencial em erro transitorio de rede (mesma classe do _stream_final).
    Para chamadas de BATCH (create/retrieve/results) que nao usam streaming — sem isso, um timeout de
    rede num unico GET/POST derrubava todo o batch (ex.: back-batch do cap.18 morreu por timeout)."""
    transient = _transient_errors()
    delay = 2.0
    for i in range(_MAX_BACKOFF):
        try:
            return fn()
        except transient:
            if i == _MAX_BACKOFF - 1:
                raise
            time.sleep(delay)
            delay *= 2


def _stream_final(client, **kwargs):
    """Streaming + backoff. Streaming evita timeout em saidas longas; backoff cobre 429/500/timeout E
    quedas de conexao no meio do stream (httpx RemoteProtocolError/'incomplete chunked read'), comuns
    em cenas grandes (output longo). NAO retenta erros de request (400 BadRequest) — esses nao 'curam'."""
    def _do():
        with client.messages.stream(**kwargs) as s:
            return s.get_final_message()
    return _with_backoff(_do)


def _await_batch(client, batch_id, poll_seconds, max_wait_seconds):
    """Aguarda o batch terminar (processing_status='ended'). True=terminou; False=timeout."""
    waited = 0
    while True:
        b = _with_backoff(lambda: client.messages.batches.retrieve(batch_id))   # poll resiliente a timeout
        if getattr(b, "processing_status", None) == "ended":
            return True
        if waited >= max_wait_seconds:
            return False
        time.sleep(poll_seconds)
        waited += poll_seconds


def _text_of(msg) -> str:
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def _usage_of(msg) -> dict:
    u = getattr(msg, "usage", None)
    if not u:
        return {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    return {"in": getattr(u, "input_tokens", 0) or 0,
            "out": getattr(u, "output_tokens", 0) or 0,
            "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0}


def _add_usage(acc: dict, u: dict) -> dict:
    for k in ("in", "out", "cache_read", "cache_write"):
        acc[k] = acc.get(k, 0) + u.get(k, 0)
    return acc
