"""ollama_client.py — REST client para o Ollama local (zero custo de API).

Backend plugável para model.py. Requer Ollama rodando em OLLAMA_HOST
(padrão: http://localhost:11434) com o modelo configurado em OLLAMA_MODEL.

Configuração via env:
  OLLAMA_HOST         URL base do Ollama  (default: http://localhost:11434)
  OLLAMA_MODEL        Modelo padrão       (default: qwen2.5:14b)
  OLLAMA_NUM_CTX      Janela de contexto  (default: 12288 — cobre doutrina+pack fixo (~3,4k tok) +
                       1 lote de OLLAMA_BATCH_LINES linhas + saída, com folga)
  OLLAMA_BATCH_LINES  Linhas por chamada  (default: 40 — model.py._ollama_translate traduz a cena em
                       lotes, não numa chamada só; existe pra caber a janela de contexto acima na VRAM
                       de placas de 8 GB sem estourar pra CPU (medido: RX 6650 XT, ver ADR 0005))

Hardware alvo: AMD Radeon RX 6650 XT (8 GB VRAM, RDNA2, ROCm no Windows).
Velocidade esperada: ~10–15 tok/s com Qwen2.5-14B (partial GPU offload).
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

OLLAMA_HOST: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL_DEFAULT: str = os.environ.get("OLLAMA_MODEL", "qwen2.5:14b")
# Ollama carrega o modelo com janela de contexto PADRAO (4096) se nao pedirmos explicitamente -- uma
# cena real (glossario+TM+decisoes+linhas) facilmente passa de 8-10k tokens e o excesso e TRUNCADO
# em silencio (sem erro), virando linhas "sem traducao" no build_plan. Qwen2.5-14B suporta 32k nativo.
OLLAMA_NUM_CTX: int = int(os.environ.get("OLLAMA_NUM_CTX", "12288"))
OLLAMA_BATCH_LINES: int = int(os.environ.get("OLLAMA_BATCH_LINES", "40"))

_TIMEOUT = 1800  # segundos — MEDIDO em 2026-08-24 na RX 6650 XT: geracao ~6,2 tok/s com ~57% offload
# GPU (14B em placa de 8 GB); 1 lote de 40 linhas so de geracao ja passa de 600s. 30 min da folga p/
# lote + eventual retry sem matar uma chamada que so estava lenta (perderia o lote inteiro — translate()
# so grava no fim). Nao cobre timeout de rede real (Ollama fora do ar) — isso falha rapido, nao em 30 min.


def health_check() -> bool:
    """True se o Ollama responde em OLLAMA_HOST."""
    try:
        urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5)  # nosec B310 - host local por env (OLLAMA_HOST), POC
        return True
    except Exception:
        return False


def list_models() -> list[str]:
    """Retorna lista de modelos disponíveis no Ollama local."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=10) as resp:  # nosec B310 - host local por env (OLLAMA_HOST), POC
            data = json.loads(resp.read().decode("utf-8"))
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def _chat(model: str, messages: list, *, fmt=None, timeout: int = _TIMEOUT) -> dict:
    """POST /api/chat (stream=False). Retorna response dict completo do Ollama.

    `fmt`: None | "json" | dict (JSON schema — Ollama >= 0.5).
    Exemplo: fmt={"type": "object", ...} para structured output estrito.
    """
    payload: dict = {"model": model, "messages": messages, "stream": False, "options": {"num_ctx": OLLAMA_NUM_CTX}}
    if fmt is not None:
        payload["format"] = fmt
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310 - host local por env (OLLAMA_HOST), POC
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {e.code}: {body[:400]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Ollama inacessível em {OLLAMA_HOST}: {e.reason}. "
            "Verifique se o Ollama está rodando (`ollama serve`)."
        ) from e


def _text_of(resp: dict) -> str:
    """Extrai o conteúdo de texto da resposta do Ollama."""
    return resp.get("message", {}).get("content", "")


def _usage_of(resp: dict) -> dict:
    """Converte contadores do Ollama para o formato do harness {in, out, cache_read, cache_write}."""
    return {
        "in": resp.get("prompt_eval_count", 0),
        "out": resp.get("eval_count", 0),
        "cache_read": 0,
        "cache_write": 0,
    }
