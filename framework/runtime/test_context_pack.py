"""test_context_pack.py — cobre o build_pack no MODO DB (o switch que o test_runtime, em modo
flat, não exercita) + os selectors e o render.

Constrói um SQLite real (store) com projeto/linhas/TM/glossário/voz/decisão/kb/spoiler, declara
`db` no project.json e chama build_pack — isso percorre _db_path/_load_sources_db/_load_lines(db)/
select_kb/select_spoiler_guards/build_pack. Sem deps de ML → a TM semântica cai p/ [] (esperado).
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_DB = _HERE.parents[0] / "db"
for _p in (_HERE, _DB):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import context_pack as cp  # noqa: E402
from store import Store  # noqa: E402


def _make_db_project(root: Path):
    dbp = root / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", "S1", [
            {"offset": "X:0:1", "source": "The Dragon speaks to Ryu.", "byte_budget": 40}])
        db.upsert_translation("p", "S1", "X:0:1", source="The Dragon speaks to Ryu.",
                              target="O Dragão fala com Ryu.", speaker="Ryu", approved=True)
        db.upsert_glossary("p", "Dragon", "Dragão")
        db.upsert_voice_card("p", "Ryu", lines=["fala do heroi"])
        db.upsert_decision("p", "Regra do dragão", summary="dragões preservam nome", tags=["dragon"])
        db.upsert_kb("p", [{"section": "Dragon lore", "content": "lore do dragão", "reveal": "safe"}])
        db.upsert_spoiler_entry("p", "Fou-lu", fact="é o dragão", reveal="beyond_frontier",
                                triggers=["dragon"], pre_reveal="trate como mistério")
    (root / "project.json").write_text(json.dumps(
        {"title": "T", "media_type": "game",
         "db": {"path": "p.db", "project_id": "p"}, "connector": {}}), encoding="utf-8")


def test_build_pack_db_mode(tmp_path):
    _make_db_project(tmp_path)
    pack = cp.build_pack(tmp_path, "S1")
    assert pack["n_lines"] == 1 and pack["scene_id"] == "S1"
    assert any(g["term"] == "Dragon" for g in pack["glossary_subset"]), "glossário DB não entrou"
    assert "Ryu" in pack["voice_cards"], "voice card DB não casou pelo nome no source"
    assert pack["tm_exact"], "TM exata (mesma fonte) deveria casar via src_key"
    assert any(k["section"] == "Dragon lore" for k in pack["kb"]), "KB safe deveria injetar"
    assert pack["spoiler_guards"], "guard de spoiler (beyond_frontier + trigger) deveria disparar"
    assert pack["tm_semantic"] == []          # sem deps de ML → fallback esperado


def test_write_pack_db_mode_renders_and_writes(tmp_path):
    _make_db_project(tmp_path)
    cp.write_pack(tmp_path, "S1")             # cobre render_prompt + mkdir do dir da cena
    sp = tmp_path / "artifacts" / "scenes" / "S1" / "scene_prompt.md"
    pj = tmp_path / "artifacts" / "scenes" / "S1" / "pack.json"
    assert sp.is_file() and pj.is_file()
    txt = sp.read_text(encoding="utf-8")
    assert "Cena S1" in txt and "CARTA DE GOVERNANCA" in txt


def test_load_lines_db_missing_scene_raises(tmp_path):
    """Cena sem linhas no DB → SystemExit legível (não pack silenciosamente vazio)."""
    _make_db_project(tmp_path)
    cfg = json.loads((tmp_path / "project.json").read_text(encoding="utf-8"))
    import pytest
    with pytest.raises(SystemExit):
        cp._load_lines(tmp_path, cfg, "NAOEXISTE")


def test_select_glossary_and_voices_lexical():
    """select_glossary/select_voices casam por presença no blob (limite de palavra)."""
    gloss = [{"term": "Dragon", "translation": "Dragão", "aliases": "Wyrm"},
             {"term": "Sword", "translation": "Espada", "aliases": ""}]
    blob = "the wyrm attacks".lower()
    gsel = cp.select_glossary(gloss, blob)
    assert any(g["term"] == "Dragon" for g in gsel)     # casa por alias 'Wyrm'
    assert not any(g["term"] == "Sword" for g in gsel)  # 'sword' ausente
    voices = cp.select_voices({"Ryu": {"aliases": ["Hero"], "lines": ["x"]}}, "the hero speaks")
    assert "Ryu" in voices                              # casa por alias 'Hero'


def test_select_kb_default_deny_semantics():
    """Gate por seção: safe/past ENTRA; futuro/beyond_frontier/sem-tag NÃO (default-deny)."""
    kb = [
        {"section": "Safe World", "content": "x", "reveal": "safe"},
        {"section": "Past Reveal", "content": "x", "reveal": "1_01"},
        {"section": "Future Reveal", "content": "x", "reveal": "9_09"},
        {"section": "Beyond", "content": "x", "reveal": "beyond_frontier"},
        {"section": "Untagged", "content": "x", "reveal": None},
    ]
    blob = "safe world past reveal future reveal beyond untagged"
    got = {s["section"] for s in cp.select_kb(kb, blob, "1_05")}
    assert got == {"Safe World", "Past Reveal"}
