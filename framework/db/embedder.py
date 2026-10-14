"""embedder.py — Embeddings locais para busca semântica na TM, em decisions e na KB.

Stack:
  sentence-transformers  paraphrase-multilingual-MiniLM-L12-v2  (~470 MB)
  sqlite-vec             extensão C para índice vetorial no SQLite

Hardware alvo: AMD RX 6650 XT (ROCm) ou CPU fallback.
O modelo roda em GPU automaticamente se torch+ROCm detectado.

Dependências (instalar via pip):
  pip install sentence-transformers sqlite-vec

Uso:
    emb = Embedder()
    emb.index_project(con, project_id="bof4")   # indexa todas as traduções aprovadas
    hits = emb.search(con, "He's gone...", project_id="bof4", k=5, min_score=0.6)

    emb.index_project(con, project_id="bof4", kind="decision")  # indexa decisions.summary
    hits = emb.search_decisions(con, "onomatopeia", project_id="bof4", k=5)

    emb.index_project(con, project_id="bof4", kind="kb")  # indexa kb.content (seções da KB)
    hits = emb.search_kb(con, "quem é o dragão do vento", project_id="bof4", k=5)

Convenção de chunking (ver docs/adr/0014-chunking-rag-na-ingestao-nao-no-embedder.md):
o embedder NUNCA chunka — sempre 1 linha da tabela-fonte = 1 vetor. Conteúdo que não é
naturalmente atômico (ex.: universe_knowledge_base.md) é quebrado em unidades ANTES de
chegar aqui, na ingestão (migrate_from_flat._migrate_kb quebra por seção `##`/`###` do
markdown). Kind novo = tabela-fonte já atômica + entrada em _KIND_CONFIG; nunca um chunk_fn
no embedder.

NN exato vs ANN: search()/search_decisions() fazem NN exato (cosine sobre TODOS os
vetores do projeto via vec0, sem índice aproximado) — decisão deliberada para corpus pequeno
(~6 mil linhas / 1 jogo, validado em docs/STACK.md), favorece determinismo sobre latência.
Considerar migrar para ANN (sqlite-vec suporta índice aproximado) a partir de ~50-100 mil
vetores por projeto, quando o scan linear passar a pesar na latência do pacote de contexto.
"""
from __future__ import annotations

import contextlib
import json
import os
import sqlite3
import struct
import time

from textclean import strip_codes  # forma limpa: vetor/consulta sem ruído dos códigos

_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_DIM = 384

# indexação genérica por "kind" -- traduções (TM), decisions e kb compartilham
# a MESMA estrutura de indexação (vec0 + tabela de metadados), só trocando tabela/coluna de
# origem. Nenhum kind aqui precisa de chunk_fn: a tabela-fonte já é 1-linha-1-unidade —
# translations/decisions porque diálogo já vem atômico, kb porque a ingestão (ver
# migrate_from_flat._migrate_kb) já quebra o markdown por seção antes de gravar. search()
# continua específico de TM (shape de retorno bem diferente de decisions/kb); ver
# search_decisions() abaixo.
_KIND_CONFIG = {
    "translation": {"table": "translations", "text_col": "source",
                    "vec_table": "tm_vectors", "emb_table": "tm_embeddings",
                    "id_col": "translation_id", "filter_sql": " AND t.approved=1"},
    "decision": {"table": "decisions", "text_col": "summary",
                 "vec_table": "decision_vectors", "emb_table": "decision_embeddings",
                 "id_col": "decision_id", "filter_sql": ""},
    "kb": {"table": "kb", "text_col": "content",
           "vec_table": "kb_vectors", "emb_table": "kb_embeddings",
           "id_col": "kb_id", "filter_sql": ""},
}


def _blob(vec) -> bytes:
    """Vetor de CONSULTA em float32 binario. Em JSON o vec_distance_l2 re-parseava o texto a cada linha
    da tabela (scan linear): ~0,13 s por fala no pacote de contexto, a etapa mais lenta de uma cena."""
    return struct.pack(f"{len(vec)}f", *vec)


_MODELS: dict = {}   # (classe, nome do modelo) -> modelo carregado

# Pre-selecao em bloco da busca na TM (search): o scan linear do vec0 custava ~0,4 s por fala com 20 mil
# vetores. Os vetores do projeto ficam em memoria (1 carga por processo), o numpy escolhe os _PREFILTER_N
# mais proximos e a MESMA consulta de sempre roda so sobre eles -- ordem, nota, agrupamento e cortes
# continuam sendo do SQL. TCF_TM_PREFILTER=0 desliga e volta ao scan completo.
_PREFILTER_ENV = "TCF_TM_PREFILTER"
_PREFILTER_N = 200
_PREFILTER_MIN_ROWS = 2000       # abaixo disso o scan completo ja e rapido
_PREFILTER_MAX_ROWS = 500_000    # teto de memoria (~770 MB); acima, scan completo
_PREFILTER_EPS = 1e-3            # folga entre a distancia do numpy (float32) e a do sqlite-vec
_VEC_CACHE: dict = {}            # (arquivo do banco, project_id) -> (carimbo, ids, matriz); 1 projeto por vez


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
        # 1 carga do modelo (~10 s) por processo, nao por Embedder(): store.py e state_index criam um
        # Embedder a cada chamada, e isso era o custo fixo de cada cena.
        key = (SentenceTransformer, model_name)
        if key not in _MODELS:
            _MODELS[key] = SentenceTransformer(model_name)
        self._model = _MODELS[key]

    def encode(self, texts: list[str]) -> list:
        """Retorna lista de vetores (lista de floats de dim 384)."""
        if not texts:
            return []
        # normalize_embeddings=True -> vetores unit-norm: com L2 do sqlite-vec, cos = 1 - L2²/2
        # (ver search). Sem isso o score `1 - distance` em vetores crus dá similaridade negativa.
        vecs = self._model.encode(texts, convert_to_numpy=True, batch_size=64,
                                  show_progress_bar=False, normalize_embeddings=True)
        return vecs.tolist()

    def _ensure_vec_table(self, con: sqlite3.Connection, kind: str = "translation"):
        """Cria a tabela virtual vec0 se não existir (requer sqlite-vec carregado)."""
        _load_sqlite_vec(con)
        c = _KIND_CONFIG[kind]
        con.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS {c['vec_table']}
            USING vec0(
                {c['id_col']} INTEGER PRIMARY KEY,
                embedding float[{_DIM}]
            )
        """)
        con.commit()

    def index_project(self, con: sqlite3.Connection, project_id: str,
                      force: bool = False, kind: str = "translation") -> int:
        """Indexa as traduções aprovadas (kind='translation', default) ou as decisions
        (kind='decision') de um projeto.

        Pula entradas já indexadas (salvo force=True).
        Retorna número de vetores gravados.
        """
        c = _KIND_CONFIG[kind]
        self._ensure_vec_table(con, kind)

        if force:
            # vec0 não aceita INSERT OR REPLACE confiável (UNIQUE no PK) — reindexa do zero (ex.: ao
            # trocar modelo ou a normalização); os vetores velhos só saem DEPOIS do encode (abaixo),
            # senão um encode que falha deixaria o indice do projeto vazio.
            rows = con.execute(
                f"SELECT id, {c['text_col']} FROM {c['table']} t WHERE t.project_id=?{c['filter_sql']}",  # nosec B608 - fragmentos vem de _KIND_CONFIG (literal interno), não input do usuário
                (project_id,),
            ).fetchall()
        else:
            rows = con.execute(
                f"""SELECT t.id, t.{c['text_col']} FROM {c['table']} t
                   LEFT JOIN {c['emb_table']} e ON t.id = e.{c['id_col']}
                   WHERE t.project_id=?{c['filter_sql']} AND e.{c['id_col']} IS NULL""",  # nosec B608
                (project_id,),
            ).fetchall()

        if not rows:
            return 0

        ids =[r[0] for r in rows]
        texts = [strip_codes(r[1] or "") for r in rows]
        vecs = self.encode(texts)
        # force: vetores+metadado velhos; senão: linha cujo texto mudou perdeu o metadado (trigger) mas
        # ainda tem o vetor velho no vec0
        con.executemany(f"DELETE FROM {c['vec_table']} WHERE {c['id_col']}=?", [(t,) for t in ids])  # nosec B608
        if force:
            con.executemany(f"DELETE FROM {c['emb_table']} WHERE {c['id_col']}=?", [(t,) for t in ids])  # nosec B608

        for tid, vec in zip(ids, vecs, strict=True):
            # vetor velho de linha editada (store apagou só o emb_table): OR REPLACE do vec0 não
            # é confiável (ver force acima) -> DELETE explícito antes.
            con.execute(f"DELETE FROM {c['vec_table']} WHERE {c['id_col']}=?", (tid,))  # nosec B608
            con.execute(
                f"INSERT INTO {c['vec_table']}({c['id_col']}, embedding) VALUES(?,?)",  # nosec B608 - fragmentos vem de _KIND_CONFIG (literal interno), não input do usuário
                (tid, json.dumps(vec)),
            )
            con.execute(
                f"""INSERT INTO {c['emb_table']}({c['id_col']}, model_name, dim, indexed_at)
                   VALUES(?,?,?,?)
                   ON CONFLICT({c['id_col']}) DO UPDATE SET indexed_at=excluded.indexed_at""",  # nosec B608
                (tid, self.model_name, _DIM, time.time()),
            )
        con.commit()
        return len(ids)

    def _candidates(self, con: sqlite3.Connection, q_vec, project_id: str, k: int, lo: float):
        """Pre-selecao em bloco. Devolve (ids, fronteira): os _PREFILTER_N vetores do projeto mais proximos
        da consulta com distancia > lo, e a distancia do mais distante deles (None = nenhum ficou de fora).
        None = sem pre-selecao (desligada, banco pequeno/enorme/em memoria, k<0): scan completo."""
        if os.environ.get(_PREFILTER_ENV, "1") == "0" or k < 0:
            return None
        # carimbo barato: linha nova/reindexada muda MAX(indexed_at); linha editada (trigger) muda COUNT.
        stamp = con.execute("SELECT COUNT(*), MAX(indexed_at) FROM tm_embeddings").fetchone()
        if not stamp or not _PREFILTER_MIN_ROWS <= stamp[0] <= _PREFILTER_MAX_ROWS:
            return None
        path = con.execute("PRAGMA database_list").fetchone()[2]
        if not path:
            return None
        import numpy as np
        hit = _VEC_CACHE.get((path, project_id))
        if hit is None or hit[0] != tuple(stamp):
            rows = con.execute(
                """SELECT v.translation_id, v.embedding FROM tm_vectors v
                   JOIN translations t ON t.id = v.translation_id
                   JOIN tm_embeddings e ON e.translation_id = v.translation_id
                   WHERE t.project_id=?""", (project_id,)).fetchall()
            mat = np.frombuffer(b"".join(r[1] for r in rows), dtype=np.float32).reshape(len(rows), -1)
            _VEC_CACHE.clear()
            _VEC_CACHE[(path, project_id)] = hit = (tuple(stamp), np.array([r[0] for r in rows]), mat)
        _, ids, mat = hit
        if not len(ids):
            return None
        # vetores unit-norm: L2² = 2 - 2·cos
        d = np.sqrt(np.maximum(2.0 - 2.0 * (mat @ np.asarray(q_vec, dtype=np.float32)), 0.0))
        ok = np.nonzero(d > lo)[0]
        if len(ok) <= _PREFILTER_N:
            return ids[ok].tolist(), None
        top = ok[np.argpartition(d[ok], _PREFILTER_N - 1)[:_PREFILTER_N]]
        return ids[top].tolist(), float(d[top].max())

    def search(self, con: sqlite3.Connection, query: str,
               project_id: str, k: int = 5,
               approved_only: bool = True,
               min_score: float | None = None,
               max_score: float | None = None) -> list[dict]:
        """Busca semântica na TM. Retorna top-k hits com score de similaridade.

        min_score: corta hits com score abaixo do threshold. None
        (default) preserva o comportamento atual — sem corte, decisão fica com quem lê a
        seção rotulada no pacote de contexto.

        max_score: exclui hits com score >= max_score NO SQL (antes do LIMIT) — p/ quem quer só
        vizinhos, não o match exato (senão fala curta com >=k exatos consome o top-k inteiro).
        """
        self._ensure_vec_table(con)
        q_vec = self.encode([strip_codes(query)])[0]

        # vec_distance_l2 + LIMIT em vez de `MATCH ... AND k = ?`: o k do vec0 escolhe os k mais
        # próximos da tabela INTEIRA (todos os projetos, aprovados ou não) ANTES do WHERE, então o
        # filtro podia devolver < k hits. Scan linear = mesmo custo do NN exato do vec0.
        # GROUP BY (source, target): o mesmo par repetido em N cenas ocupava N slots do top-k. Com MIN()
        # o SQLite devolve as colunas "bare" da linha de menor distancia (garantia documentada).
        # alias `l2`, nao `distance`: o vec0 tem coluna oculta `distance` que venceria o alias no HAVING.
        cut = max_score is not None and max_score <= 1.0      # >1 = sem corte superior (score max e 1)
        # score cru = 1 - L2²/2  ->  score < max_score  <=>  L2 > sqrt(2*(1-max_score)). Filtro UNICO
        # (so no SQL, sobre o cru): um 2o check no score arredondado discordava na fronteira.
        cut_l2 = (2.0 * (1.0 - max_score)) ** 0.5 if cut and max_score is not None else None
        rows = None
        cand = self._candidates(con, q_vec, project_id, k,
                                cut_l2 - _PREFILTER_EPS if cut_l2 is not None else -1.0)
        if cand is not None and cand[0]:
            ids, edge = cand
            rows = con.execute(
                f"""SELECT v.translation_id, MIN(vec_distance_l2(v.embedding, ?)) AS l2,
                           t.scene_id, t.offset, t.source, t.target,
                           t.speaker, t.tone_register, t.risk_level
                    FROM translations t
                    JOIN tm_vectors v ON v.translation_id = t.id
                    JOIN tm_embeddings e ON e.translation_id = t.id
                    WHERE t.id IN ({",".join(str(int(i)) for i in ids)})
                      AND t.project_id=?
                      {" AND t.approved=1" if approved_only else ""}
                    GROUP BY t.source, t.target
                    {" HAVING l2 > ?" if cut else ""}
                    ORDER BY l2 LIMIT ?""",  # nosec B608 - ids sao inteiros do proprio banco; resto parametrizado
                (_blob(q_vec), project_id, *((cut_l2,) if cut_l2 is not None else ()), k),
            ).fetchall()
            # Quem ficou fora dos candidatos esta a >= `edge`: o resultado so e o do scan completo se
            # vieram k grupos e o ultimo esta folgado aquem da fronteira. Senao, recua.
            if edge is not None and (len(rows) < k or (rows and rows[-1][1] >= edge - _PREFILTER_EPS)):
                rows = None
        elif cand is not None and cand[1] is None:
            rows = []                                          # nenhum vetor do projeto passa do corte
        if rows is None:
            rows = con.execute(
                f"""SELECT v.translation_id, MIN(vec_distance_l2(v.embedding, ?)) AS l2,
                           t.scene_id, t.offset, t.source, t.target,
                           t.speaker, t.tone_register, t.risk_level
                    FROM tm_vectors v
                    JOIN translations t ON t.id = v.translation_id
                    JOIN tm_embeddings e ON e.translation_id = v.translation_id  -- linha editada some ate o reindex
                    WHERE t.project_id=?
                      {" AND t.approved=1" if approved_only else ""}
                    GROUP BY t.source, t.target
                    {" HAVING l2 > ?" if cut else ""}
                    ORDER BY l2 LIMIT ?""",  # nosec B608 - fragmento literal por bool; valores parametrizados
                (_blob(q_vec), project_id, *((cut_l2,) if cut_l2 is not None else ()), k),
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
            raw = 1.0 - float(d["distance"]) ** 2 / 2.0
            d["score"] = round(raw, 4)            # exibicao; os cortes (min/max_score) usam o cru
            if min_score is not None and raw < min_score:
                continue
            results.append(d)

        return results

    def search_decisions(self, con: sqlite3.Connection, query: str,
                         project_id: str, k: int = 5) -> list[dict]:
        """Busca semântica em decisions. Retorna top-k hits (title/summary/universal/
        reveal/score) — shape diferente de search() (TM), por isso método separado em vez de
        forçar as duas formas numa única função genérica. k<0 = todos (LIMIT -1 do SQLite), p/ o
        chamador cortar DEPOIS do seu próprio gate (reveal)."""
        self._ensure_vec_table(con, kind="decision")
        q_vec = self.encode([strip_codes(query)])[0]

        rows = con.execute(
            """SELECT v.decision_id, vec_distance_l2(v.embedding, ?) AS distance,
                       d.title, d.summary, d.universal, d.reveal
                FROM decision_vectors v
                JOIN decisions d ON d.id = v.decision_id
                JOIN decision_embeddings e ON e.decision_id = v.decision_id
                WHERE d.project_id=?
                ORDER BY distance LIMIT ?""",  # nosec B608 - filtro ANTES do top-k (ver search); JOIN emb:
                                                 # linha editada (trigger apagou o emb) some ate o reindex
            (_blob(q_vec), project_id, k),
        ).fetchall()

        results = []
        for r in rows:
            d = dict(zip(
                ["decision_id", "distance", "title", "summary", "universal", "reveal"],
                r,
                strict=True,
            ))
            d["score"] = round(1.0 - float(d["distance"]) ** 2 / 2.0, 4)
            results.append(d)
        return results

    def search_kb(self, con: sqlite3.Connection, query: str,
                  project_id: str, k: int = 5) -> list[dict]:
        """Busca semântica na KB. Retorna top-k hits (section/content/reveal/score) —
        shape análogo a search_decisions(); GATE de spoiler por `reveal` fica por conta do
        chamador (ver context_pack._reveal_allowed), igual search_decisions() faz."""
        self._ensure_vec_table(con, kind="kb")
        q_vec = self.encode([strip_codes(query)])[0]

        rows = con.execute(
            """SELECT v.kb_id, vec_distance_l2(v.embedding, ?) AS distance,
                       kb.section, kb.content, kb.reveal
                FROM kb_vectors v
                JOIN kb ON kb.id = v.kb_id
                JOIN kb_embeddings e ON e.kb_id = v.kb_id
                WHERE kb.project_id=?
                ORDER BY distance LIMIT ?""",  # nosec B608 - filtro ANTES do top-k (ver search); JOIN emb:
                                                 # linha editada (trigger apagou o emb) some ate o reindex
            (_blob(q_vec), project_id, k),
        ).fetchall()

        results = []
        for r in rows:
            d = dict(zip(
                ["kb_id", "distance", "section", "content", "reveal"],
                r,
                strict=True,
            ))
            d["score"] = round(1.0 - float(d["distance"]) ** 2 / 2.0, 4)
            results.append(d)
        return results


if __name__ == "__main__":
    import sys
    with contextlib.suppress(AttributeError, ValueError, OSError):  # Windows cp1252: permitir setas/acentos no stdout
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
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
