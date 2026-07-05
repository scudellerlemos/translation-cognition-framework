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
    assert pack["decisions_semantic"] == []   # idem (#105) — sem deps de ML → fallback esperado


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


def test_load_decisions_semantic_respects_reveal_gate(tmp_path):
    """#105 smoke test com o Embedder/sqlite-vec REAIS -- só roda se a stack ML estiver
    instalada localmente (requirements-ml.txt); skip limpo em CI, que não instala essa stack.
    Decision 'safe' deve entrar; decision com reveal futuro deve ficar de fora (mesmo gate de
    select_kb, ver _reveal_allowed)."""
    import pytest
    pytest.importorskip("sentence_transformers")
    pytest.importorskip("sqlite_vec")
    from embedder import Embedder

    dbp = tmp_path / "p.db"
    with Store(dbp) as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", "S1", [
            {"offset": "X:0:1", "source": "The Dragon speaks to Ryu.", "byte_budget": 40}])
        db.upsert_decision("p", "Regra do dragão", summary="dragões preservam o nome original",
                           reveal="safe")
        db.upsert_decision("p", "Segredo futuro do dragão",
                           summary="dragões preservam o nome original", reveal="9_09")
        emb = Embedder()
        emb.index_project(db._con, project_id="p", kind="decision")

    rows = [{"offset": "X:0:1", "source": "The Dragon speaks to Ryu."}]
    got = cp._load_decisions_semantic(dbp, "p", rows, "the dragon speaks to ryu.", "1_05")
    titles = {d["title"] for d in got}
    assert "Regra do dragão" in titles
    assert "Segredo futuro do dragão" not in titles


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


def test_render_prompt_full_sections():
    """Pacote com TODAS as seções + ramos opcionais (charset off, convenção de sistema, length)."""
    pc = {"newline_token": "[NL]", "formatting_tokens": ["[01]"], "formatting_token_patterns": ["\\[..\\]"],
          "system_line_convention": "sistema em maiúscula", "length_constraints": {"max": 40},
          "target_charset_supported": False, "charset_note": "fonte sem acento"}
    pack = {
        "scene": "S1", "scene_id": "S1", "n_lines": 1, "doctrine": "d", "doctrine_hash": "h",
        "skills_revision": "r", "project_constraints": pc,
        "glossary_subset": [{"term": "Dragon", "category": "creature", "target_translation": "Dragão",
                             "handling_rule": "preserve", "spoiler_level": ""}],
        "voice_cards": {"Ryu": {"criticality": "high", "aliases": ["Hero"], "lines": ["fala curta"]}},
        "decisions": [{"title": "Regra", "summary": "manter", "universal": True}],
        "spoiler_guards": [{"entity": "Fou-lu", "spoiler_level": "high", "guard": "trate como mistério"}],
        "kb": [{"section": "Lore", "content": "lore do mundo"}],
        "tm_exact": [{"source": "Hi", "target": "Oi", "speaker": "Ryu", "from_scene": "S0"}],
        "tm_voice": [{"speaker": "Ryu", "source": "Hi", "target": "Oi"}],
        "tm_semantic": [{"score": 0.9, "source": "Hey", "target": "Ei"}],
        "lines": [{"offset": "X:0:1", "source": "Hello | world", "byte_budget": 20}],
    }
    out = cp.render_prompt(pack, "CARTA DE TESTE")
    for needle in ("Cena S1", "Dragon", "Ryu", "Fou-lu", "Lore", "SIMILARES", "charset", "Hello"):
        assert needle in out, needle


def test_render_prompt_empty_sections():
    """Ramos vazios: sem glossário/TM/carta → mensagens de fallback."""
    pc = {"newline_token": "[NL]", "formatting_tokens": [], "formatting_token_patterns": [],
          "system_line_convention": "", "length_constraints": {}, "target_charset_supported": True,
          "charset_note": ""}
    pack = {"scene": "S1", "scene_id": "S1", "n_lines": 0, "doctrine": "d", "doctrine_hash": "",
            "skills_revision": "", "project_constraints": pc, "glossary_subset": [], "voice_cards": {},
            "decisions": [], "spoiler_guards": [], "kb": [], "tm_exact": [], "tm_voice": [],
            "tm_semantic": [], "lines": []}
    out = cp.render_prompt(pack, "")
    assert "nenhum termo" in out and "sem memoria" in out


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


def test_reveal_allowed_shared_gate(tmp_path):
    """_reveal_allowed (#105): mesmo gate default-deny usado por select_kb (KB léxica) e
    _load_decisions_semantic (decisions semânticas) -- contrato direto, sem passar por seleção."""
    here = cp._pos("1_05")
    assert cp._reveal_allowed("safe", here) is True
    assert cp._reveal_allowed("1_01", here) is True             # já passado
    assert cp._reveal_allowed("9_09", here) is False             # futuro
    assert cp._reveal_allowed("beyond_frontier", here) is False
    assert cp._reveal_allowed(None, here) is False               # sem tag -> default-deny
