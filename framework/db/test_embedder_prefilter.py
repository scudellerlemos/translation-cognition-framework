"""test_embedder_prefilter.py — a pre-selecao em bloco de Embedder.search() devolve o MESMO resultado do
scan completo (linha inteira), recua quando os candidatos nao bastam e enxerga o banco que mudou.

Encode falso (so sqlite-vec + numpy): vetores deterministicos por texto, em aglomerados.
"""
import hashlib
import random
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

pytest.importorskip("sqlite_vec")
pytest.importorskip("numpy")

import embedder as E  # noqa: E402
from store import Store  # noqa: E402

_N_CLUSTERS = 12


def _vec(text: str) -> list[float]:
    """Vetor unit-norm deterministico; o 1o token do texto escolhe o aglomerado."""
    def gauss(seed: str, scale: float) -> list[float]:
        rnd = random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16))
        return [rnd.gauss(0, scale) for _ in range(E._DIM)]
    v = [a + b for a, b in zip(gauss(text.split()[0], 1.0), gauss(text, 0.35), strict=True)]
    n = sum(x * x for x in v) ** 0.5
    return [x / n for x in v]


def _embedder() -> E.Embedder:
    emb = E.Embedder.__new__(E.Embedder)
    emb.model_name = "fake"
    emb.encode = lambda texts: [_vec(t) for t in texts]
    return emb


@pytest.fixture
def small(monkeypatch):
    """Limites pequenos para o banco de teste entrar na pre-selecao; cache limpo por teste."""
    monkeypatch.setattr(E, "_PREFILTER_MIN_ROWS", 0)
    monkeypatch.setattr(E, "_PREFILTER_N", 20)
    monkeypatch.setattr(E, "_VEC_CACHE", {})


def _fill(db: Store, n: int = 400) -> None:
    db.upsert_project("p", "p")
    for i in range(n):
        db.upsert_translation("p", f"s{i % 7}", str(i), f"c{i % _N_CLUSTERS} fala {i}",
                              target=f"t{i}", approved=i % 11 != 0)
    for i in range(0, 60, 3):                       # mesmo par (source, target) em outra cena: 1 grupo
        db.upsert_translation("p", "dup", str(i), f"c{i % _N_CLUSTERS} fala {i}", target=f"t{i}", approved=True)


def _both(emb, con, monkeypatch, query, **kw):
    out = []
    for flag in "01":
        monkeypatch.setenv(E._PREFILTER_ENV, flag)
        out.append(emb.search(con, query, project_id="p", **kw))
    return out


def _count_full_scans(con) -> list[int]:
    n = [0]
    con.set_trace_callback(lambda q: n.__setitem__(0, n[0] + ("FROM tm_vectors v" in q and "MIN(" in q)))
    return n


def test_prefilter_igual_ao_scan_completo(tmp_path, monkeypatch, small):
    emb = _embedder()
    with Store(tmp_path / "p.db") as db:
        _fill(db)
        emb.index_project(db._con, project_id="p")
        full = _count_full_scans(db._con)
        for i in range(0, 400, 5):
            q = f"c{i % _N_CLUSTERS} fala {i}"
            for kw in ({"k": 5, "max_score": 0.999}, {"k": 5}, {"k": 3, "min_score": 0.3, "max_score": 0.999},
                       {"k": 5, "approved_only": False}):
                old, new = _both(emb, db._con, monkeypatch, q, **kw)
                assert old == new and old, (q, kw)
        # a pre-selecao de fato rodou: bem menos scans completos que as 2 x 320 buscas
        assert full[0] < 2 * 320 * 0.75


def test_prefilter_recua_quando_um_par_repetido_enche_os_candidatos(tmp_path, monkeypatch, small):
    emb = _embedder()
    with Store(tmp_path / "p.db") as db:
        _fill(db, n=60)
        for i in range(300):                        # 300 linhas, 1 grupo, todas mais perto que o resto
            db.upsert_translation("p", f"r{i}", "0", "c1 eco", target="eco", approved=True)
        emb.index_project(db._con, project_id="p")
        monkeypatch.setenv(E._PREFILTER_ENV, "1")
        full = _count_full_scans(db._con)
        new = emb.search(db._con, "c1 eco perto", project_id="p", k=5)
        assert full[0] == 1                         # recuou
        monkeypatch.setenv(E._PREFILTER_ENV, "0")
        assert new == emb.search(db._con, "c1 eco perto", project_id="p", k=5) and len(new) == 5


def test_prefilter_enxerga_fala_nova_e_esquece_fala_editada(tmp_path, monkeypatch, small):
    emb = _embedder()
    with Store(tmp_path / "p.db") as db:
        _fill(db)
        emb.index_project(db._con, project_id="p")
        q = "c3 fala nova"
        old, new = _both(emb, db._con, monkeypatch, q, k=3)
        assert old == new and q not in {h["source"] for h in new}
        # gravada no meio do lote: a busca seguinte, no mesmo processo, tem de achar
        db.upsert_translation("p", "s0", "9000", q, target="nova", approved=True)
        emb.index_project(db._con, project_id="p")
        old, new = _both(emb, db._con, monkeypatch, q, k=3)
        assert old == new and new[0]["source"] == q
        # editada: some ate o reindex (trigger apaga o metadado), igual ao scan completo
        db.upsert_translation("p", "s0", "9000", "c9 outra coisa", target="nova", approved=True)
        old, new = _both(emb, db._con, monkeypatch, q, k=3)
        assert old == new and q not in {h["source"] for h in new}
        emb.index_project(db._con, project_id="p")
        old, new = _both(emb, db._con, monkeypatch, "c9 outra coisa", k=3)
        assert old == new and new[0]["source"] == "c9 outra coisa"


def test_prefilter_desligado_ou_banco_pequeno_nao_carrega_nada(tmp_path, monkeypatch):
    monkeypatch.setattr(E, "_VEC_CACHE", {})
    emb = _embedder()
    with Store(tmp_path / "p.db") as db:
        _fill(db, n=40)
        emb.index_project(db._con, project_id="p")
        for flag in "01":                           # "1" com o piso real (2000 vetores): banco pequeno
            monkeypatch.setenv(E._PREFILTER_ENV, flag)
            assert emb.search(db._con, "c1 fala 1", project_id="p", k=3)
            assert E._VEC_CACHE == {}
