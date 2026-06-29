"""test_context_pack_parity.py — oráculo do switch DB/flat do context_pack.

Garante que ler as fontes do SQLite produz o MESMO resultado que ler dos flat files
para as fontes DETERMINÍSTICAS (glossary, voice cards, decisions, spoiler). Se um dia o
adaptador DB→pack divergir do flat, este teste falha — o switch só é confiável enquanto
a paridade fechar.

TM fica de fora da paridade de propósito: a flat vem dos translation_plan*.json (base
pré-revisão) e a do DB vem dos approved_*.csv (pós-revisão humana) — divergência legítima
(o DB é a fonte melhor). Aqui a TM do DB é checada só quanto a não-degradação (bem-formada).

Usa só stdlib — roda em CI sem deps de ML.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

import context_pack as cp  # noqa: E402
from migrate_from_flat import migrate  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def _flat_sources():
    """Fontes flat lidas diretamente (sem passar pelo _load_sources, que tem efeito
    colateral de reconstruir índices)."""
    import paths  # noqa: E402
    fg = cp.load_glossary(paths.glossary(BOF4))
    state = BOF4 / "artifacts" / "state"
    fv = json.loads((state / "voice_cards.json").read_text(encoding="utf-8")) \
        if (state / "voice_cards.json").is_file() else {}
    fd = json.loads((state / "decision_index.json").read_text(encoding="utf-8")) \
        if (state / "decision_index.json").is_file() else []
    sl = BOF4 / "artifacts" / "spoiler_ledger.json"
    fl = json.loads(sl.read_text(encoding="utf-8")) if sl.is_file() else {}
    return fg, fv, fd, fl


def _blob(fg, fv):
    """Blob que força o casamento de todos os termos/vozes — exercita seleção cheia."""
    terms = [g.get("term", "") for g in fg]
    terms += [a for g in fg for a in (g.get("aliases", "") or "").split(";")]
    names = list(fv.keys()) + [a for c in fv.values() for a in c.get("aliases", [])]
    return " ".join(t.lower() for t in terms + names if t)


def test_db_sources_match_flat_for_deterministic_fields(tmp_path):
    migrate(BOF4, tmp_path / "t.db", project_id="bof4")
    dg, dv, dd, dtm, dl = cp._load_sources_db(tmp_path / "t.db", "bof4")
    fg, fv, fd, fl = _flat_sources()
    blob = _blob(fg, fv)

    # Glossário e vozes: seleção do DB == seleção do flat (byte-a-byte na estrutura).
    assert cp.select_glossary(dg, blob) == cp.select_glossary(fg, blob)
    assert cp.select_voices(dv, blob) == cp.select_voices(fv, blob)

    # Decisões: mesma seleção dados os mesmos termos/falantes presentes.
    fgsub = cp.select_glossary(fg, blob)
    fvsel = cp.select_voices(fv, blob)
    pt = [g["term"] for g in fgsub]
    ps = list(fvsel.keys())
    assert cp.select_decisions(dd, pt, ps) == cp.select_decisions(fd, pt, ps)

    # Spoiler guards: mesma saída (BoF4: ledger vazio dos dois lados → []).
    sid = cp.scene_id_of("AREAD001")
    assert cp.select_spoiler_guards(dl, blob, sid) == cp.select_spoiler_guards(fl, blob, sid)


def test_db_tm_is_well_formed(tmp_path):
    """TM do DB (proveniência = approved) não precisa igualar a flat, mas tem que ser
    bem-formada e não-vazia (não-degradação)."""
    migrate(BOF4, tmp_path / "t.db", project_id="bof4")
    _g, _v, _d, dtm, _l = cp._load_sources_db(tmp_path / "t.db", "bof4")
    assert dtm, "TM do DB vazia"
    needed = {"src_key", "source", "target", "speaker", "scene"}
    assert all(needed <= set(t) for t in dtm), "entradas de TM mal-formadas"
