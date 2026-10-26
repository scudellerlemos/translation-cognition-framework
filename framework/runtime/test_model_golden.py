"""ADR 0019 (guardrail): saida dos dois caminhos travada byte a byte, antes de dividir model.py/context_pack.py.

- API: o que `_api_translate` envia ao cliente (system, mensagens, thinking, output_config) no 1o passe e no retry.
- Sessao: o scene_prompt.md e o retorno de translate(backend="in-session").
Dados 100% sinteticos. Se um destes testes falhar depois de uma divisao, a divisao mudou o comportamento.
"""
import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _p in (_HERE, _HERE.parent / "db"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import context_pack  # noqa: E402
import model  # noqa: E402
import model_api  # noqa: E402
import paths  # noqa: E402
from store import Store  # noqa: E402

SCENE = "S1"
_ZERO = {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}


def _projeto(d):
    with Store(d / "p.db") as db:
        db.upsert_project("p", "T")
        db.upsert_scene_lines("p", SCENE, [
            {"offset": f"X:0:{k}", "source": f"Linha sintetica numero {k}.", "byte_budget": 60} for k in range(6)])
        db.upsert_glossary("p", "termo", "alvo")
        db.upsert_voice_card("p", "Ana", lines=["fala"])
        db.upsert_decision("p", "Regra", summary="resumo", tags=["termo"])
    paths.atomic_write(d / "project.json", json.dumps(
        {"title": "T", "media_type": "game", "db": {"path": "p.db", "project_id": "p", "semantic": False},
         "connector": {}}))
    return d


def _sha(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def _entry(off, t="ok"):
    return {"offset": off, "speaker": "X", "tone_register": "n", "intent": "i",
            "risk_level": "low", "risk_notes": "", "t": t}


def _captura_api(tmp_path, monkeypatch):
    root = _projeto(tmp_path)
    pack = context_pack.build_pack(root, SCENE)
    offs = [r["offset"] for r in pack["lines"]]
    paths.scene_dir(root, SCENE).mkdir(parents=True, exist_ok=True)
    enviado = []
    # 1o passe: devolve so metade das linhas -> forca um retry com nota de correcao
    respostas = [{"lines": [_entry(o) for o in offs[:3]]}, {"lines": [_entry(o) for o in offs[3:]]}]

    def fake_stream(client, **kw):
        enviado.append({k: kw[k] for k in ("model", "max_tokens", "system", "messages", "thinking", "output_config")})
        return respostas.pop(0)

    monkeypatch.setattr(model_api, "_client", lambda: object())
    monkeypatch.setattr(model_api, "_carta_text", lambda: "CARTA")
    monkeypatch.setattr(model_api, "_stream_final", fake_stream)
    monkeypatch.setattr(model_api, "_text_of", lambda m: json.dumps(m))
    monkeypatch.setattr(model_api, "_usage_of", lambda m: dict(_ZERO))
    monkeypatch.setattr(model_api, "log_api_call", lambda *a, **k: None)
    data, usage, meta = model._api_translate(root, SCENE, pack, model.MODEL_TRANSLATE)
    return enviado, data, usage, meta


def test_api_entrada_e_saida_travadas(tmp_path, monkeypatch):
    enviado, data, usage, meta = _captura_api(tmp_path, monkeypatch)
    assert len(enviado) == 2
    assert enviado[0]["system"] == [{"type": "text", "text": "CARTA", "cache_control": {"type": "ephemeral"}}]
    assert "CORRECAO NECESSARIA" in enviado[1]["messages"][0]["content"]
    assert _sha(enviado) == GOLDEN["api_enviado"]
    assert _sha(data) == GOLDEN["api_dados"]
    assert (usage, meta) == (_ZERO, {"reused": 0, "novel": 6, "n_lines": 6})


def test_sessao_prompt_e_retorno_travados(tmp_path, monkeypatch):
    carta = tmp_path / "carta.md"                              # hermetico: nao depende da Carta real do repo
    carta.write_text("CARTA SINTETICA\n", encoding="utf-8")
    monkeypatch.setattr(context_pack, "CARTA_PATH", carta)
    root = _projeto(tmp_path)
    r = model.translate(root, SCENE, backend="in-session")
    assert r["status"] == model.AWAITING and r["n_lines"] == 6
    prompt = paths.scene_prompt(root, SCENE).read_text(encoding="utf-8")
    assert _sha(prompt) == GOLDEN["sessao_prompt"]
    assert _sha({k: v for k, v in r.items() if k not in ("prompt", "expected_output")}) == GOLDEN["sessao_retorno"]
    # com a traducao pronta, o retorno muda para READY e aponta o arquivo
    out = paths.translations(root, SCENE, r["scene_id"])
    pack = context_pack.build_pack(root, SCENE)
    paths.atomic_write(out, json.dumps({"lines": {x["offset"]: _entry(x["offset"]) for x in pack["lines"]}}))
    assert model.translate(root, SCENE, backend="in-session")["status"] == model.READY


# 2026-10-25: a tabela de linhas ganhou a coluna `nl` (quebras do source) -> mudaram `api_enviado` e `sessao_prompt`
GOLDEN = {"api_enviado": "68eb11a14a303b10", "api_dados": "c64a33d7db5c3594",
          "sessao_prompt": "0da3b475f2e599e4", "sessao_retorno": "297e57b1cd3e7b10"}
