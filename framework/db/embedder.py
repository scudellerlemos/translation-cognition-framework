"""embedder.py — Embeddings locais para busca semântica na TM.

Stack:
  sentence-transformers  paraphrase-multilingual-MiniLM-L12-v2  (~470 MB)
  sqlite-vec             extensão C para índice vetorial no SQLite
  flashrank              reranker MiniLM-L-12 quantizado (~4 MB, opcional)

Hardware alvo: AMD RX 6650 XT (ROCm) ou CPU fallback.
O modelo roda em GPU automaticamente se torch+ROCm detectado.

Dependências (instalar via pip):
  pip install sentence-transformers sqlite-vec flashrank

Uso:
    emb = Embedder()
    emb.index_project(con, project_id="bof4")   # indexa todas as traduções aprovadas
    hits = emb.search(con, "He's gone...", project_id="bof4", k=5)
"""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import time

_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_DIM = 384
_RERANKER_MODEL = "ms-marco-MiniLM-L-12-v2"


def _load_sentence_transformers():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer
    except ModuleNotFoundError as e:
        raise ImportError(
            "sentence-transformers não instalado. Instale: pip install -r requirements-ml.txt"
        ) from e
    # Outros ImportError (ex.: DLL nativa do torch BLOQUEADA por App Control/Smart App Control no
    # Windows, ou wheel incompatível) propagam com a CAUSA REAL — não mascarar como "não instalado".


def _load_sqlite_vec(con: sqlite3.Connection):
    try:
        import sqlite_vec
    except ModuleNotFoundError as e:
        raise ImportError(
            "sqlite-vec não instalado. Instale: pip install -r requirements-ml.txt"
        ) from e
    # O sqlite3 desabilita load de extensão por padrão (-> 'not authorized'). Habilita SÓ p/
    # carregar o vec0 e desabilita de novo — não deixa a conexão aberta a extensões arbitrárias.
    con.enable_load_extension(True)
    try:
        sqlite_vec.load(con)
    finally:
        con.enable_load_extension(False)


class Embedder:
    """Wrapper sobre sentence-transformers + sqlite-vec para TM semântica."""

    def __init__(self, model_name: str = _MODEL_NAME):
        SentenceTransformer = _load_sentence_transformers()
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list:
        """Retorna lista de vetores (lista de floats de dim 384)."""
        if not texts:
            return []
        # normalize_embeddings=True -> vetores unit-norm: com L2 do sqlite-vec, cos = 1 - L2²/2
        # (ver search). Sem isso o score `1 - distance` em vetores crus dá similaridade negativa.
        vecs = self._model.encode(texts, convert_to_numpy=True, batch_size=64,
                                  show_progress_bar=False, normalize_embeddings=True)
        return vecs.tolist()

    def _ensure_vec_table(self, con: sqlite3.Connection):
        """Cria a tabela virtual vec0 se não existir (requer sqlite-vec carregado)."""
        _load_sqlite_vec(con)
        con.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS tm_vectors
            USING vec0(
                translation_id INTEGER PRIMARY KEY,
                embedding float[{_DIM}]
            )
        """)
        con.commit()

    def index_project(self, con: sqlite3.Connection, project_id: str,
                      force: bool = False) -> int:
        """Indexa todas as traduções aprovadas de um projeto.

        Pula entradas já indexadas (salvo force=True).
        Retorna número de vetores gravados.
        """
        self._ensure_vec_table(con)

        # Seleciona traduções aprovadas ainda não indexadas
        if force:
            # vec0 não aceita INSERT OR REPLACE confiável (UNIQUE no PK) — limpa os vetores do
            # projeto e reindexa do zero (ex.: ao trocar modelo ou a normalização).
            tids = [r[0] for r in con.execute(
                "SELECT id FROM translations WHERE project_id=? AND approved=1",
                (project_id,)).fetchall()]
            con.executemany("DELETE FROM tm_vectors WHERE translation_id=?", [(t,) for t in tids])
            con.executemany("DELETE FROM tm_embeddings WHERE translation_id=?", [(t,) for t in tids])
            con.commit()
            rows = con.execute(
                "SELECT id, source FROM translations WHERE project_id=? AND approved=1",
                (project_id,),
            ).fetchall()
        else:
            rows = con.execute(
                """SELECT t.id, t.source FROM translations t
                   LEFT JOIN tm_embeddings e ON t.id = e.translation_id
                   WHERE t.project_id=? AND t.approved=1 AND e.translation_id IS NULL""",
                (project_id,),
            ).fetchall()

        if not rows:
            return 0

        from store import strip_codes  # noqa: E402  (forma limpa: vetor sem ruído dos códigos)
        ids = [r[0] for r in rows]
        texts = [strip_codes(r[1]) for r in rows]
        vecs = self.encode(texts)

        for tid, vec in zip(ids, vecs, strict=True):
            con.execute(
                "INSERT OR REPLACE INTO tm_vectors(translation_id, embedding) VALUES(?,?)",
                (tid, json.dumps(vec)),
            )
            con.execute(
                """INSERT INTO tm_embeddings(translation_id, model_name, dim, indexed_at)
                   VALUES(?,?,?,?)
                   ON CONFLICT(translation_id) DO UPDATE SET indexed_at=excluded.indexed_at""",
                (tid, self.model_name, _DIM, time.time()),
            )
        con.commit()
        return len(ids)

    def search(self, con: sqlite3.Connection, query: str,
               project_id: str, k: int = 5,
               approved_only: bool = True) -> list[dict]:
        """Busca semântica na TM. Retorna top-k hits com score de similaridade."""
        from store import strip_codes  # noqa: E402  (consulta na mesma forma limpa do índice)
        self._ensure_vec_table(con)
        q_vec = self.encode([strip_codes(query)])[0]

        rows = con.execute(
            f"""SELECT v.translation_id, v.distance,
                       t.scene_id, t.offset, t.source, t.target,
                       t.speaker, t.tone_register, t.risk_level
                FROM tm_vectors v
                JOIN translations t ON t.id = v.translation_id
                WHERE t.project_id=?
                  {" AND t.approved=1" if approved_only else ""}
                  AND v.embedding MATCH ?
                  AND k = ?
                ORDER BY v.distance""",  # nosec B608 - fragmento literal por bool; valores parametrizados
            (project_id, json.dumps(q_vec), k),
        ).fetchall()

        results = []
        for r in rows:
            d = dict(zip(
                ["translation_id", "distance", "scene_id", "offset",
                 "source", "target", "speaker", "tone_register", "risk_level"],
                r,
                strict=True,
            ))
            # vetores são unit-norm (encode normaliza) e a distância é L2 -> cos = 1 - L2²/2.
            # Identica: L2=0 -> 1.0; ortogonal: L2=√2 -> 0.0; oposta: L2=2 -> -1.0.
            d["score"] = round(1.0 - float(d["distance"]) ** 2 / 2.0, 4)
            results.append(d)

        return self._rerank(query, results) if results else results

    def _rerank(self, query: str, hits: list[dict]) -> list[dict]:
        """Rerank com FlashRank se disponível; caso contrário retorna como está."""
        try:
            from flashrank import Ranker, RerankRequest  # type: ignore
            ranker = Ranker(model_name=_RERANKER_MODEL,
                            cache_dir=os.path.join(tempfile.gettempdir(), "flashrank"))
            passages = [{"id": i, "text": h["source"], "meta": h}
                        for i, h in enumerate(hits)]
            req = RerankRequest(query=query, passages=passages)
            results = ranker.rerank(req)
            return [r["meta"] for r in results]
        except ImportError:
            return hits


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: python embedder.py <db_path> <project_id> [query]")
        sys.exit(1)
    db_path, project_id = sys.argv[1], sys.argv[2]
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    emb = Embedder()
    if len(sys.argv) > 3:
        query = sys.argv[3]
        hits = emb.search(con, query, project_id=project_id)
        for h in hits:
            print(f"[{h['score']:.3f}] {h['source']!r} → {h['target']!r}")
    else:
        n = emb.index_project(con, project_id)
        print(f"Indexados: {n} vetores em {db_path}")
    con.close()
