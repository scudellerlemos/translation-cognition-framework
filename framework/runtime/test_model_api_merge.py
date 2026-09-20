"""test_model_api_merge.py — como _api_translate MESCLA respostas entre tentativas (lacuna, paridade,
budget) e o que manda na nota de correção do retry. Reusa o cliente falso de test_translate_checkpoint.
"""
import json

import context_pack
import model
import pytest
import test_translate_checkpoint as ckpt

env = ckpt.env
_good = ckpt._good
TOK = context_pack.TOKEN


def _pack(*lines):
    """lines = (offset, source[, byte_budget])."""
    out = []
    for ln in lines:
        row = {"offset": ln[0], "source": ln[1]}
        if len(ln) > 2:
            row["byte_budget"] = ln[2]
        out.append(row)
    return {"scene_id": "95_01", "tm_exact": [], "doctrine_hash": "d1", "lines": out}


def _run(root, pack):
    return model._api_translate(root, ckpt.SCENE, pack, model.MODEL_TRANSLATE)


def test_unknown_offsets_and_non_dict_entries_are_ignored(env):
    root, sent, replies = env
    replies.append({"lines": {"0x1": "texto solto", "0x9": _good("0x9"), "0x2": _good("0x2")}})
    replies.append({"lines": [_good("0x1")]})
    data, _u, _m = _run(root, _pack(("0x1", "Hello"), ("0x2", "World")))
    assert set(data["lines"]) == {"0x1", "0x2"}          # 0x9 (fora da cena) descartado; 0x1 veio no retry
    assert len(sent) == 2


def test_pathological_blowup_is_dropped_and_retried(env):
    root, sent, replies = env
    replies.append({"lines": [_good("0x1", "x" * 500)]})   # grito curto virou 500 chars de lixo
    replies.append({"lines": [_good("0x1", "Ola")]})
    data, _u, _m = _run(root, _pack(("0x1", "Hi")))
    assert data["lines"]["0x1"]["t"] == "Ola" and len(sent) == 2


def test_retry_replaces_bad_parity_and_asks_for_exact_breaks(env):
    root, sent, replies = env
    replies.append({"lines": [_good("0x1", "AB")]})              # fonte tem 1 quebra, alvo 0
    replies.append({"lines": [_good("0x1", f"A{TOK}B")]})
    data, _u, _m = _run(root, _pack(("0x1", f"A{TOK}B")))
    assert data["lines"]["0x1"]["t"] == f"A{TOK}B"               # a de paridade correta substitui a ruim
    assert "DIFERENTE da fonte" in sent[1]


def test_retry_prefers_shorter_when_same_parity_and_over_budget(env):
    root, sent, replies = env
    replies.append({"lines": [_good("0x1", "x" * 30)]})          # estoura budget 5 (tol 1.4 -> 7)
    replies.append({"lines": [_good("0x1", "curto")]})
    data, _u, _m = _run(root, _pack(("0x1", "Hello", 5)))
    assert data["lines"]["0x1"]["t"] == "curto"
    assert "byte_budget" in sent[1]                              # nota de budget no retry


def test_retry_asks_to_preserve_engine_formatting_tokens(env):
    root, sent, replies = env
    pack = _pack(("0x1", "<C1>Hi"))
    pack["project_constraints"] = {"formatting_tokens": ["<C1>"]}
    replies.append({"lines": [_good("0x1", "Oi")]})              # perdeu <C1>
    replies.append({"lines": [_good("0x1", "<C1>Oi")]})
    data, _u, _m = _run(root, pack)
    assert data["lines"]["0x1"]["t"] == "<C1>Oi"
    assert "tokens de formatacao do engine" in sent[1]


def test_scene_of_only_engine_labels_makes_zero_api_calls(env):
    root, sent, _replies = env
    data, usage, meta = _run(root, _pack(("0x1", "body"), ("0x2", "lightA02")))
    assert sent == [] and usage["in"] == 0 and meta["novel"] == 0
    assert data["lines"]["0x1"]["t"] == "body"                  # passthrough determinístico


# --- translate(): despacho por backend --------------------------------------------------------------
def _stub_pack(monkeypatch):
    monkeypatch.setattr(model.context_pack, "write_pack",
                        lambda root, scene: {"scene_id": "95_01", "n_lines": 3,
                                             "doctrine_hash": "dh", "skills_revision": "sr"})


def test_translate_in_session_awaits_then_reports_ready(tmp_path, monkeypatch):
    _stub_pack(monkeypatch)
    r = model.translate(tmp_path, ckpt.SCENE, backend="in-session")
    assert r["status"] == model.AWAITING and r["expected_output"].endswith(".json")
    out = model.paths.translations(tmp_path, ckpt.SCENE, "95_01")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("{}", encoding="utf-8")
    assert model.translate(tmp_path, ckpt.SCENE, backend="in-session")["status"] == model.READY


def test_translate_api_writes_provenance_meta(tmp_path, monkeypatch):
    _stub_pack(monkeypatch)
    monkeypatch.setattr(model, "_api_translate",
                        lambda *a, **k: ({"lines": {}}, {"in": 1}, {"reused": 2, "novel": 1}))
    model.paths.scene_dir(tmp_path, ckpt.SCENE).mkdir(parents=True)
    r = model.translate(tmp_path, ckpt.SCENE, backend="api", model="m-x")
    saved = json.loads(model.paths.translations(tmp_path, ckpt.SCENE, "95_01").read_text(encoding="utf-8"))
    assert saved["_meta"] == {"model_id": "m-x", "doctrine_hash": "dh", "skills_revision": "sr"}
    assert (r["status"], r["reused"], r["novel"]) == (model.DONE, 2, 1)


def test_translate_unknown_backend_raises(tmp_path, monkeypatch):
    _stub_pack(monkeypatch)
    with pytest.raises(ValueError, match="backend desconhecido"):
        model.translate(tmp_path, ckpt.SCENE, backend="fax")


def test_retranslate_offsets_with_no_matching_lines_is_a_noop(tmp_path, monkeypatch):
    monkeypatch.setattr(model.context_pack, "build_pack",
                        lambda root, scene: {"scene_id": "95_01", "lines": [{"offset": "0x1"}]})
    r = model.retranslate_offsets(tmp_path, ckpt.SCENE, ["0xZ"], budget_tolerance=1.0)
    assert r["status"] == model.DONE and r["n_lines"] == 0 and r["usage"] is None


def test_retranslate_offsets_unknown_backend_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(model.context_pack, "build_pack",
                        lambda root, scene: {"scene_id": "95_01", "lines": [{"offset": "0x1"}]})
    with pytest.raises(ValueError, match="backend desconhecido"):
        model.retranslate_offsets(tmp_path, ckpt.SCENE, ["0x1"], budget_tolerance=1.0, backend="fax")


def test_helpers_pass_non_strings_through():
    assert model._norm_t(None) is None and model._parity_fit("x", 5) == 5
    assert model._is_blowup("x", None) is False


def test_to_map_skips_entries_without_offset():
    out = model._to_map({"lines": [{"t": "sem offset"}, {"offset": "0x1", "t": "ok"}]})
    assert list(out["lines"]) == ["0x1"]


# --- batch: chunk que trava / tier que falha só ficam sem cobertura --------------------------------
class _Res:
    def __init__(self, cid, typ):
        self.custom_id = cid
        self.result = type("R", (), {"type": typ})()


class _FakeBatches:
    def __init__(self, results):
        self._results = results

    def create(self, requests):
        return type("B", (), {"id": "b1"})()

    def results(self, _id):
        return iter(self._results)


def _client_with(results):
    return type("C", (), {"messages": type("M", (), {"batches": _FakeBatches(results)})()})()


def test_submit_chunk_timeout_leaves_scene_without_coverage(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(model, "_await_batch", lambda *a, **k: False)
    merged = {"s": {}}
    model._submit_translate_chunk(_client_with([]), [object()], 0, 1, {}, {}, {}, merged, tmp_path, "m")
    assert "nao concluiu" in capsys.readouterr().out and merged == {"s": {}}


def test_submit_chunk_ignores_failed_tier(monkeypatch, tmp_path):
    monkeypatch.setattr(model, "_await_batch", lambda *a, **k: True)
    merged = {"s": {}}
    model._submit_translate_chunk(_client_with([_Res("s__cheap__0", "errored")]), [object()], 0, 1,
                                  {}, {}, {"s": {"lines": []}}, merged, tmp_path, "m")
    assert merged == {"s": {}}                                   # falha não aceita nada; cobertura decide
