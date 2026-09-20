"""L01 — retries esgotados nao podem jogar fora as linhas ja pagas (checkpoint parcial) + contador."""
import json

import context_pack
import cost_report
import model
import paths
import pytest

SCENE = "ch_95_01"
_ZERO = {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}


def _good(off, t="ok"):
    return {"offset": off, "speaker": "X", "tone_register": "n", "intent": "i",
            "risk_level": "low", "risk_notes": "", "t": t}


def _offs(content):
    """Offsets-alvo de um prompt enviado (a 1a linha do render; o resto e regra/nota de correcao)."""
    return content.split("\n", 1)[0]


def _pack(doctrine="d1", srcs=("Hello", "World", "Friend")):
    return {"scene_id": "95_01", "tm_exact": [], "doctrine_hash": doctrine,
            "lines": [{"offset": f"0x{i}", "source": s} for i, s in enumerate(srcs, 1)]}


@pytest.fixture
def env(monkeypatch, tmp_path):
    paths.scene_dir(tmp_path, SCENE).mkdir(parents=True)
    # o conteudo enviado revela o subconjunto de linhas-alvo
    monkeypatch.setattr(context_pack, "render_prompt",
                        lambda p, carta="": " ".join(r["offset"] for r in p["lines"]))
    monkeypatch.setattr(model, "_carta_text", lambda: "CARTA")
    monkeypatch.setattr(model, "_client", lambda: object())
    monkeypatch.setattr(model, "_text_of", lambda msg: json.dumps(msg))
    monkeypatch.setattr(model, "_usage_of", lambda msg: dict(_ZERO))
    sent, replies = [], []

    def fake_stream(client, **kw):
        sent.append(kw["messages"][0]["content"])
        return replies.pop(0)
    monkeypatch.setattr(model, "_stream_final", fake_stream)
    return tmp_path, sent, replies


def _exhaust(root, replies, pack, **kw):
    """3 tentativas em que 0x3 nunca vem -> esgota."""
    replies.extend([{"lines": [_good("0x1"), _good("0x2")]}] * model._MAX_TRIES)
    with pytest.raises(RuntimeError) as ei:
        model._api_translate(root, SCENE, pack, model.MODEL_TRANSLATE, **kw)
    return str(ei.value)


def test_exhaustion_saves_partial_and_next_run_sends_only_the_rest(env):
    root, sent, replies = env
    msg = _exhaust(root, replies, _pack())
    part = paths.translations_partial(root, SCENE, "95_01")
    assert set(json.loads(part.read_text(encoding="utf-8"))["lines"]) == {"0x1", "0x2"}
    assert "2 linha(s) boa(s) salvas" in msg
    n_first = len(sent)

    replies.append({"lines": [_good("0x3")]})
    data, _u, _m = model._api_translate(root, SCENE, _pack(), model.MODEL_TRANSLATE)
    assert set(data["lines"]) == {"0x1", "0x2", "0x3"}
    assert _offs(sent[n_first]) == "0x3", "o modelo recebeu SO a linha que faltava"
    assert not part.exists(), "checkpoint apagado ao concluir"


def test_partial_path_does_not_match_build_plan_glob(env):
    root, _sent, replies = env
    _exhaust(root, replies, _pack())
    assert paths.translations_partial(root, SCENE, "95_01").exists()
    assert not list(paths.scene_dir(root, SCENE).glob("translations_*.json"))


def test_exhaustion_is_logged(env):
    root, _sent, replies = env
    _exhaust(root, replies, _pack())
    rows = [json.loads(ln) for ln in paths.translate_exhausted(root).read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["scene"] == SCENE and rows[0]["stage"] == "first"
    assert (rows[0]["missing"], rows[0]["kept"]) == (1, 2)


def test_doctrine_change_discards_checkpoint(env):
    root, sent, replies = env
    _exhaust(root, replies, _pack(doctrine="d1"))
    n = len(sent)
    replies.append({"lines": [_good("0x1"), _good("0x2"), _good("0x3")]})
    model._api_translate(root, SCENE, _pack(doctrine="d2"), model.MODEL_TRANSLATE)
    assert _offs(sent[n]) == "0x1 0x2 0x3", "doutrina mudou: traduz tudo de novo, nao reusa o checkpoint"


def test_changed_source_line_is_retranslated(env):
    root, sent, replies = env
    _exhaust(root, replies, _pack())
    n = len(sent)
    replies.append({"lines": [_good("0x2", "novo"), _good("0x3")]})
    data, _u, _m = model._api_translate(root, SCENE, _pack(srcs=("Hello", "Mundo", "Friend")),
                                        model.MODEL_TRANSLATE)
    assert _offs(sent[n]) == "0x2 0x3", "0x1 (source igual) retomada; 0x2 (source mudou) e 0x3 (faltava) reenviadas"
    assert data["lines"]["0x2"]["t"] == "novo" and data["lines"]["0x1"]["t"] == "ok"


def test_retighten_never_uses_checkpoint(env):
    root, _sent, replies = env
    msg = _exhaust(root, replies, _pack(), budget_tolerance=1.0)
    assert not paths.translations_partial(root, SCENE, "95_01").exists()
    assert "checkpoint" not in msg
    row = json.loads(paths.translate_exhausted(root).read_text(encoding="utf-8").splitlines()[0])
    assert row["stage"] == "retighten" and row["kept"] == 0


def test_corrupt_checkpoint_is_ignored_with_warning(env, capsys):
    root, sent, replies = env
    paths.translations_partial(root, SCENE, "95_01").write_text("{nao e json", encoding="utf-8")
    replies.append({"lines": [_good("0x1"), _good("0x2"), _good("0x3")]})
    data, _u, _m = model._api_translate(root, SCENE, _pack(), model.MODEL_TRANSLATE)
    assert set(data["lines"]) == {"0x1", "0x2", "0x3"} and _offs(sent[0]) == "0x1 0x2 0x3"
    assert "AVISO" in capsys.readouterr().out


def test_cost_report_counts_exhaustions(env):
    root, _sent, replies = env
    _exhaust(root, replies, _pack())
    ex = cost_report.report(root)["exhausted"]
    assert (ex["n"], ex["scenes"], ex["kept"]) == (1, 1, 2)
    assert cost_report.report(root, chapter="94")["exhausted"]["n"] == 0
    assert "esgotamentos: 1" in cost_report._fmt(cost_report.report(root), by_scene=False)
