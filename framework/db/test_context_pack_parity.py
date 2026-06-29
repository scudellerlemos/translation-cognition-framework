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


def test_db_scene_lines_match_flat(bof4_migrated):
    """Linhas da cena no DB == dialogs.csv flat — o último pedaço que faltava pro
    context_pack montar o pacote 100% do DB."""
    db_path, _ = bof4_migrated
    flat = cp.load_dialogs(BOF4 / "artifacts" / "scenes" / "AREAD001" / "dialogs.csv")
    with Store(db_path) as db:
        dbrows = db.get_scene_lines("bof4", "AREAD001")
    assert dbrows == flat, "scene_lines do DB divergem do dialogs.csv flat"


def test_tm_semantic_fallback_no_deps(bof4_migrated):
    """RAG (Fase 2.5): sem o stack de embeddings (caso da CI), a TM semântica cai p/ []
    sem erro. Com as deps + índice, retorna lista de vizinhos similares (validado local)."""
    db_path, _ = bof4_migrated
    rows = cp.load_dialogs(BOF4 / "artifacts" / "scenes" / "AREAD001" / "dialogs.csv")
    res = cp._load_tm_semantic(db_path, "bof4", rows)
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


def test_kb_spoiler_gate_never_leaks_future_reveal():
    """RAG nº2: o gate de spoiler da KB NUNCA injeta seção com reveal futuro. Validado com
    dado REAL do Utawarerumono (ledger: Ukon reveal=13_08, Oshtor=beyond_frontier; KB tem a
    seção '## Oshtor (= Ukon; reveal ch_13_08)' = o twist)."""
    import json
    uta = ROOT / "projects" / "utawarerumono"
    ledger = json.loads((uta / "artifacts" / "spoiler_ledger.json").read_text(encoding="utf-8"))
    kb = _parse_kb_md(uta / "artifacts" / "universe_knowledge_base.md")
    assert any("Oshtor" in s["section"] for s in kb), "fixture: KB do uta deveria ter seção Oshtor"
    blob = "ukon e oshtor aparecem nesta cena"        # ambos citados
    # cena 11_03 = ANTES do reveal 13_08. Valida o gate p/ spoiler MARCADO (trigger/quarentena).
    # (Furo conhecido — spoiler pt sem marcador, ex. 'Mulher (figura de memória)' — é o motivo
    #  de select_kb NÃO estar ligado no build_pack; ver docstring.)
    sel = cp.select_kb(kb, blob, ledger, "11_03")
    joined = " ".join((s["section"] + " " + s["content"]).lower() for s in sel)
    assert "oshtor" not in joined, "VAZOU o trigger Oshtor (twist) pré-reveal!"
    assert "= ukon" not in joined, "VAZOU a identidade Oshtor=Ukon pré-reveal!"


def test_db_tm_is_well_formed(bof4_migrated):
    """TM do DB (proveniência = approved) não precisa igualar a flat, mas tem que ser
    bem-formada e não-vazia (não-degradação)."""
    db_path, _ = bof4_migrated
    _g, _v, _d, dtm, _l = cp._load_sources_db(db_path, "bof4")
    assert dtm, "TM do DB vazia"
    needed = {"src_key", "source", "target", "speaker", "scene"}
    assert all(needed <= set(t) for t in dtm), "entradas de TM mal-formadas"
    assert all(t["source"] and t["target"] for t in dtm), "TM com source/target vazio (migração quebrada)"
