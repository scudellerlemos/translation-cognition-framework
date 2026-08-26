"""test_context_pack_parity.py — oráculo do switch DB/flat do context_pack.

Garante que ler as fontes do SQLite produz o MESMO resultado que ler dos flat files para
as fontes DETERMINÍSTICAS (scene_lines, glossary, voice cards, decisions, spoiler). Se o
adaptador DB→pack divergir do flat, falha — o switch só é confiável enquanto a paridade
fechar.

A TM fica fora da paridade de propósito: a flat vem dos translation_plan*.json (base
pré-revisão) e a do DB dos approved_*.csv (pós-revisão humana) — divergência legítima (o
DB é a fonte melhor). Aqui a TM do DB é checada só quanto a não-degradação.

Usa o fixture bof4_migrated (migração única por sessão). Só stdlib — roda em CI sem ML.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "framework" / "runtime"))
sys.path.insert(0, str(HERE))

import context_pack as cp  # noqa: E402
from store import Store  # noqa: E402

BOF4 = ROOT / "projects" / "breath_of_fire_4"


def _flat_sources():
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


def test_db_sources_match_flat_for_deterministic_fields(bof4_migrated):
    db_path, _ = bof4_migrated
    dg, dv, dd, _dtm, dl = cp._load_sources_db(db_path, "bof4")
    fg, fv, fd, fl = _flat_sources()
    blob = _blob(fg, fv)

    assert cp.select_glossary(dg, blob) == cp.select_glossary(fg, blob)
    assert cp.select_voices(dv, blob) == cp.select_voices(fv, blob)

    fgsub = cp.select_glossary(fg, blob)
    fvsel = cp.select_voices(fv, blob)
    pt = [g["term"] for g in fgsub]
    ps = list(fvsel.keys())
    assert cp.select_decisions(dd, pt, ps) == cp.select_decisions(fd, pt, ps)

    sid = cp.scene_id_of("AREAD001")
    assert cp.select_spoiler_guards(dl, blob, sid) == cp.select_spoiler_guards(fl, blob, sid)


def test_db_scene_lines_match_flat(synthetic_migrated):
    """Linhas da cena no DB == dialogs.csv flat — o último pedaço que faltava pro
    context_pack montar o pacote 100% do DB. Fixture sintetica (dialogs.csv real foi
    purgado do BoF4 versionado; ver conftest.synthetic_migrated)."""
    root, db_path, _ = synthetic_migrated
    flat = cp.load_dialogs(root / "artifacts" / "scenes" / "s1" / "dialogs.csv")
    with Store(db_path) as db:
        dbrows = db.get_scene_lines("syn", "s1")
    assert dbrows == flat, "scene_lines do DB divergem do dialogs.csv flat"


def test_tm_semantic_fallback_no_deps(synthetic_migrated):
    """RAG (Fase 2.5): sem o stack de embeddings (caso da CI), a TM semântica cai p/ []
    sem erro. Com as deps + índice, retorna lista de vizinhos similares (validado local)."""
    root, db_path, _ = synthetic_migrated
    rows = cp.load_dialogs(root / "artifacts" / "scenes" / "s1" / "dialogs.csv")
    res = cp._load_tm_semantic(db_path, "syn", rows)
    assert isinstance(res, list)  # sem deps → []; nunca lança


def _parse_kb_md(path):
    """Mesmo split de seções do migrate (## / ###) — p/ validar select_kb sem migrar."""
    entries, section, buf = [], None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(("## ", "### ")):
            if section and "\n".join(buf).strip():
                entries.append({"section": section, "content": "\n".join(buf).strip()})
            section, buf = line.lstrip("# ").strip(), []
        elif section is not None:
            buf.append(line)
    if section and "\n".join(buf).strip():
        entries.append({"section": section, "content": "\n".join(buf).strip()})
    return entries


def test_kb_default_deny_unannotated_injects_nothing():
    """RAG nº2 (default-deny): a KB do Uta NÃO tem tags `<!-- reveal -->`; logo NENHUMA seção é
    injetada — inclui a seção-twist 'Oshtor (= Ukon)', que jamais pode aparecer pré-reveal.
    Prova que dado não-anotado nunca vaza (a segurança não depende de matching de texto)."""
    uta = ROOT / "projects" / "utawarerumono"
    kb = _parse_kb_md(uta / "artifacts" / "universe_knowledge_base.md")
    assert any("Oshtor" in s["section"] for s in kb), "fixture: KB do uta deveria ter seção Oshtor"
    blob = "ukon oshtor mulher kuon haku aperyu maroro"   # cita várias entidades
    assert cp.select_kb(kb, blob, "11_03") == [], "default-deny: KB sem reveal anotado não injeta"


def test_kb_default_deny_semantics():
    """Gate por seção: 'safe' e reveal-passado ENTRAM; futuro/beyond_frontier/sem-tag NÃO."""
    kb = [
        {"section": "Kuon", "content": "x", "reveal": "11_01"},
        {"section": "Glossario do mundo", "content": "x", "reveal": "safe"},
        {"section": "Oshtor", "content": "x", "reveal": "13_08"},
        {"section": "Mulher figura", "content": "x", "reveal": "beyond_frontier"},
        {"section": "SemTag", "content": "x", "reveal": None},
    ]
    blob = "kuon oshtor mulher glossario semtag"
    got = {s["section"] for s in cp.select_kb(kb, blob, "11_03")}
    assert "Kuon" in got                       # reveal 11_01 <= 11_03
    assert "Glossario do mundo" in got         # safe
    assert "Oshtor" not in got                 # reveal 13_08 futuro
    assert "Mulher figura" not in got          # beyond_frontier
    assert "SemTag" not in got                 # sem tag → default-deny


def test_db_tm_is_well_formed(synthetic_migrated):
    """TM do DB (proveniência = approved) não precisa igualar a flat, mas tem que ser
    bem-formada e não-vazia (não-degradação)."""
    _root, db_path, _ = synthetic_migrated
    _g, _v, _d, dtm, _l = cp._load_sources_db(db_path, "syn")
    assert dtm, "TM do DB vazia"
    needed = {"src_key", "source", "target", "speaker", "scene"}
    assert all(needed <= set(t) for t in dtm), "entradas de TM mal-formadas"
    assert all(t["source"] and t["target"] for t in dtm), "TM com source/target vazio (migração quebrada)"
