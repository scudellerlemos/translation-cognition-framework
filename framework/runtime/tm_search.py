"""
tm_search.py — índice semântico flat-file para a TM (caminho sem SQLite).

Complementa o caminho DB (embedder.py + sqlite-vec): quando o projeto não tem um
banco SQLite configurado (project.json sem 'db'), este módulo constrói e consulta o
índice em arquivos locais (artifacts/state/).

Arquivos gerados:
  tm_embeddings.npy  — matriz numpy (n, 384), vetores unit-norm
  tm_index.json      — metadados (n, model_name) + entradas (source/target/speaker/src_key)

Os .npy ficam no .gitignore (regeneráveis; pesados). O tm_index.json não é commitado
porque depende das traduções aprovadas do projeto.

Dependência opcional: sentence-transformers. Se ausente, build_index lança ImportError
com mensagem clara; load_index + search retornam None / [] silenciosamente (CI segura).
"""
from __future__ import annotations

import json
from pathlib import Path

_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_INDEX_FILE = "tm_index.json"
_EMBED_FILE = "tm_embeddings.npy"


def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(_MODEL_NAME)
    except ModuleNotFoundError as e:
        raise ImportError(
            "sentence-transformers não instalado. "
            "Instale: pip install -r requirements-ml.txt"
        ) from e


def build_index(tm_entries: list[dict], state_dir: Path) -> int:
    """Encoda todos os source da TM e grava tm_embeddings.npy + tm_index.json.

    Idempotente: pula se o índice já existe com o mesmo número de entradas e modelo.
    Retorna o número de vetores gravados (0 se pulou por cache válido).
    Lança ImportError se sentence-transformers não estiver instalado.
    """
    import numpy as np

    state_dir = Path(state_dir)
    idx_path = state_dir / _INDEX_FILE
    emb_path = state_dir / _EMBED_FILE

    # validação de cache: mesmo n + mesmo modelo → pula
    if idx_path.is_file() and emb_path.is_file():
        try:
            meta = json.loads(idx_path.read_text(encoding="utf-8"))
            if meta.get("n") == len(tm_entries) and meta.get("model") == _MODEL_NAME:
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    if not tm_entries:
        # limpa índice vazio para não servir dados stale
        idx_path.unlink(missing_ok=True)
        emb_path.unlink(missing_ok=True)
        return 0

    # _load_model() primeiro: garante ImportError claro sobre sentence-transformers
    # antes de qualquer acesso a numpy (ambos ausentes na CI sem requirements-ml.txt).
    model = _load_model()
    texts = [e.get("source", "") for e in tm_entries]
    vecs = model.encode(texts, convert_to_numpy=True, batch_size=64,
                        show_progress_bar=False, normalize_embeddings=True)

    np.save(str(emb_path), vecs)

    entries_meta = [
        {
            "source": e.get("source", ""),
            "target": e.get("target", ""),
            "speaker": e.get("speaker", ""),
            "src_key": e.get("src_key", ""),
        }
        for e in tm_entries
    ]
    idx_path.write_text(
        json.dumps({"n": len(tm_entries), "model": _MODEL_NAME, "entries": entries_meta},
                   ensure_ascii=False),
        encoding="utf-8",
    )
    return len(tm_entries)


def load_index(state_dir: Path) -> dict | None:
    """Carrega o índice do disco. Retorna None se não existe ou está corrompido."""
    state_dir = Path(state_dir)
    idx_path = state_dir / _INDEX_FILE
    emb_path = state_dir / _EMBED_FILE
    if not idx_path.is_file() or not emb_path.is_file():
        return None
    try:
        import numpy as np
        meta = json.loads(idx_path.read_text(encoding="utf-8"))
        vecs = np.load(str(emb_path))
        if vecs.shape[0] != meta.get("n", -1):
            return None
        return {"vecs": vecs, "entries": meta["entries"]}
    except Exception:
        return None


def search(
    query: str,
    index: dict,
    top_k: int = 3,
    max_hits: int = 8,
    exclude_keys: set[str] | None = None,
) -> list[dict]:
    """Busca semântica por cosine similarity (dot product com vetores unit-norm).

    exclude_keys: src_key das linhas já presentes no match exato — evita duplicar.
    Retorna lista de {source, target, speaker, score} ordenada por score desc.
    """
    if not query.strip() or not index:
        return []
    try:
        import numpy as np
        model = _load_model()
        q_vec = model.encode([query], convert_to_numpy=True,
                             show_progress_bar=False, normalize_embeddings=True)[0]
        scores = index["vecs"].dot(q_vec)
        top_idx = scores.argsort()[::-1]
        out = []
        seen_keys: set[str] = set()
        for i in top_idx:
            if len(out) >= max_hits:
                break
            e = index["entries"][i]
            sk = e.get("src_key", "")
            if (exclude_keys and sk in exclude_keys) or sk in seen_keys:
                continue
            score = float(scores[i])
            if score >= 0.999:
                continue  # match quase-exato: já está no tm_exact
            seen_keys.add(sk)
            out.append({
                "source": e["source"],
                "target": e["target"],
                "speaker": e.get("speaker", ""),
                "score": round(score, 3),
            })
            if len(out) >= top_k:
                break
        return out
    except Exception:
        return []
