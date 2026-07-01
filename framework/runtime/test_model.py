"""test_model.py — cobre as funções DETERMINÍSTICAS do model (sem SDK/rede).

Guards de tradução (paridade de quebra, blow-up, translit-len), passthrough de rótulo de engine,
dedup de TM (_select_reuse), normalização (_norm_t/_to_map). As chamadas de API/batch ficam fora
(precisam de mock pesado do SDK; ver test_runtime para os caminhos de retry/batch já cobertos).
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_DB = _HERE.parents[0] / "db"
for _p in (_HERE, _DB):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import context_pack  # noqa: E402
import model as M  # noqa: E402
import paths  # noqa: E402
from store import Store  # noqa: E402

TOK = context_pack.TOKEN


def _db_scene(root: Path, byte_budget=5, t="uma tradução bem longa demais"):
    """Projeto DB-mode com 1 cena (S1) + translations com t acima do budget."""
    with Store(root / "p.db") as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", "S1", [{"offset": "X:0:1", "source": "Hi", "byte_budget": byte_budget}])
    (root / "project.json").write_text(json.dumps(
        {"title": "T", "media_type": "game", "db": {"path": "p.db", "project_id": "p"},
         "connector": {}}), encoding="utf-8")
    (root / "artifacts" / "scenes" / "S1").mkdir(parents=True)
    paths.translations(root, "S1", "S1").write_text(
        json.dumps({"lines": {"X:0:1": {"t": t}}}), encoding="utf-8")


def test_no_effort_model():
    assert M._no_effort_model("claude-haiku-4-5") is True
    assert M._no_effort_model("claude-opus-4-8") is False


def test_check_translation_flags_newline_and_missing():
    data = {"lines": {"o1": {"t": "tem\nquebra"}, "o2": {"t": "ok"}}}
    bad, missing = M._check_translation(data, ["o1", "o2", "o3"])
    assert "o1" in bad and "o3" in missing and "o2" not in bad


def test_translit_len_drops_accents():
    assert M._translit_len("coração") == len("coracao")
    assert M._translit_len("") == 0


def test_norm_t_and_to_map():
    assert TOK in M._norm_t("linha1\nlinha2")
    out = M._to_map({"lines": [{"offset": "o1", "t": "a\nb", "speaker": "R"}]})
    assert out["lines"]["o1"]["speaker"] == "R" and TOK in out["lines"]["o1"]["t"]
    # idempotente: já-mapa continua mapa
    assert M._to_map({"lines": {"o1": {"t": "x"}}})["lines"]["o1"]["t"] == "x"


def test_parity_fit_strips_spurious_break():
    # fonte SEM token -> alvo não pode ter (troca por espaço + colapsa)
    assert M._parity_fit("no break here", f"a{TOK}b") == "a b"
    # fonte COM token -> mantém
    assert M._parity_fit(f"a{TOK}b", f"x{TOK}y") == f"x{TOK}y"


def test_is_blowup():
    assert M._is_blowup("hi", "x" * 300) is True
    assert M._is_blowup("hi", "ola") is False


def test_is_tokish():
    assert M._is_tokish("body") is True
    assert M._is_tokish("uma frase longa com espacos") is False


def test_label_passthrough_engine_labels():
    pack = {"lines": [{"offset": "o1", "source": "body"},
                      {"offset": "o2", "source": "lightA02"},
                      {"offset": "o3", "source": "Hello there friend"}]}
    out = M._label_passthrough(pack)
    assert "o1" in out and "o2" in out and "o3" not in out
    assert out["o1"]["t"] == "body" and out["o1"]["intent"] == "rotulo_engine"


def test_select_reuse_dedups_from_other_scene():
    pack = {"scene_id": "S1",
            "tm_exact": [{"from_scene": "S0", "source": "Hello", "target": "Olá", "speaker": "Ryu"}],
            "lines": [{"offset": "o1", "source": "Hello"}]}
    reuse = M._select_reuse(pack, enabled=True)
    assert "o1" in reuse and reuse["o1"]["t"] == "Olá" and reuse["o1"]["intent"] == "reuso_tm"
    assert M._select_reuse(pack, enabled=False) == {}          # desligado no escalonamento


def test_select_reuse_skips_own_scene():
    pack = {"scene_id": "S1",
            "tm_exact": [{"from_scene": "S1", "source": "Hello", "target": "Olá"}],
            "lines": [{"offset": "o1", "source": "Hello"}]}
    assert M._select_reuse(pack, enabled=True) == {}           # nunca reusa a própria cena


def test_over_offsets_pure():
    budgets = {"o1": 5, "o2": 100, "o3": None}
    lines = {"o1": {"t": "traducao muito longa"}, "o2": {"t": "ok"}, "o3": {"t": "x"}}
    assert M._over_offsets(budgets, lines) == ["o1"]           # só o1 estoura; o3 sem budget ignorado


def test_coverage_note():
    assert M._coverage_note([], []) == ""
    note = M._coverage_note(["o1"], ["o2"])
    assert "o1" in note and "o2" in note and "CORRECAO" in note


def test_over_budget_offsets_integration(tmp_path):
    _db_scene(tmp_path, byte_budget=5, t="uma tradução bem longa demais")
    assert M.over_budget_offsets(tmp_path, "S1") == ["X:0:1"]


def test_retranslate_offsets_mocked(tmp_path, monkeypatch):
    _db_scene(tmp_path, byte_budget=5, t="longo demais")
    monkeypatch.setattr(M, "_api_translate",
                        lambda root, scene, sub, m, **k: ({"lines": {"X:0:1": {"t": "curto"}}},
                                                          {"in": 1, "out": 1},
                                                          {"reused": 0, "novel": 1}))
    monkeypatch.setattr(M, "invalidate_back_translation", lambda *a, **k: None)
    r = M.retranslate_offsets(tmp_path, "S1", ["X:0:1"], budget_tolerance=1.0)
    assert r["status"] == M.DONE and r["n_lines"] == 1
    data = json.loads(paths.translations(tmp_path, "S1", "S1").read_text(encoding="utf-8"))
    assert data["lines"]["X:0:1"]["t"] == "curto"              # merge aplicou a re-tradução


def test_tier_of():
    assert M._tier_of(f"a{TOK}b") == "main"                    # multi-linha -> Sonnet
    assert M._tier_of("single line") == "cheap"               # single -> Haiku


def test_parse_batch_lines():
    pack = {"scene_id": "S1", "tm_exact": [], "lines": [{"offset": "o1", "source": "Hi"}]}
    out = M._parse_batch_lines(pack, json.dumps({"lines": [{"offset": "o1", "t": "Oi"}]}))
    assert out["o1"]["t"] == "Oi"
    assert M._parse_batch_lines(pack, "json quebrado") == {}   # tolera parse-fail


def test_merge_best_parity_prefers_good():
    srcmap = {"o1": "sem token"}                              # 0 tokens = paridade boa é 0
    dest = {"o1": {"t": f"x{TOK}y"}}                          # ruim (1 token)
    M._merge_best_parity(dest, {"o1": {"t": "z"}}, srcmap)    # nova é boa (0 tokens)
    assert dest["o1"]["t"] == "z"                             # boa substitui a ruim


def test_batch_coverage_finds_missing():
    pack = {"scene_id": "S1", "tm_exact": [],
            "lines": [{"offset": "o1", "source": "a"}, {"offset": "o2", "source": "b"}]}
    missing, bad = M._batch_coverage(pack, {"o1": {"t": "A"}})
    assert "o2" in missing and bad == []
