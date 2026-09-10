"""test_validate_model.py — smoke test do validate_model (#170) com Embedder/sqlite-vec
REAIS. Só roda se a stack ML estiver instalada localmente (requirements-ml.txt); skip
limpo em CI, que não instala essa stack (mesmo padrão de test_context_pack.py)."""
import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from store import Store  # noqa: E402


def test_validate_model_exact_match_high_score(tmp_path):
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from validate_model import validate_model

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        db.upsert_translation("p", "S1", "0:1", "The Dragon speaks to Ryu.",
                               target="O Dragão fala com Ryu.", approved=True)
        db.upsert_translation("p", "S1", "0:2", "Nina flies over the castle.",
                               target="Nina voa sobre o castelo.", approved=True)

    con = sqlite3.connect(dbp)
    result = validate_model(con, "p", sample_size=10)
    con.close()

    assert result["n_samples"] == 2
    # query = source verbatim -> deve recuperar a própria linha com score ~1.0
    assert result["exact_match_avg"] > 0.99
    assert result["vocab_variation_avg"] is None  # sem --paraphrases


def test_validate_model_seed_is_reproducible(tmp_path):
    """#185: amostragem é aleatória sobre todas as linhas aprovadas (não mais as N primeiras
    via LIMIT); --seed fixa a amostra pra reprodutibilidade (mesma seed -> mesmo resultado)."""
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from validate_model import validate_model

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        for i in range(25):
            db.upsert_translation("p", "S1", f"0:{i}", f"Line number {i} of dialogue.",
                                   target=f"Linha numero {i} de dialogo.", approved=True)

    con = sqlite3.connect(dbp)
    r1 = validate_model(con, "p", sample_size=5, seed=42)
    r2 = validate_model(con, "p", sample_size=5, seed=42)
    con.close()

    assert r1["n_samples"] == 5
    assert r1 == r2  # mesma seed -> mesma amostra -> mesmo resultado


def test_validate_model_zero_or_negative_sample_size_raises(tmp_path):
    """Review do #185: sample_size<=0 não pode cair no random.sample()/divisão por zero —
    tem que falhar limpo com ValueError, como o LIMIT 0 antigo fazia."""
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from validate_model import validate_model

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        db.upsert_translation("p", "S1", "0:1", "The Dragon speaks to Ryu.",
                               target="O Dragão fala com Ryu.", approved=True)

    con = sqlite3.connect(dbp)
    with pytest.raises(ValueError):
        validate_model(con, "p", sample_size=0)
    with pytest.raises(ValueError):
        validate_model(con, "p", sample_size=-1)
    con.close()


def test_validate_model_no_approved_translations_raises(tmp_path):
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from validate_model import validate_model

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")

    con = sqlite3.connect(dbp)
    with pytest.raises(ValueError):
        validate_model(con, "p")
    con.close()
