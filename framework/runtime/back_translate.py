"""back_translate.py — concern de BACK-TRANSLATION (crivo de qualidade pt-BR -> EN -> confere sentido).

Extraido do model.py (god-module). Reune TODO o caminho de back-translation: selecao de candidatos
(high/critical + amostra do tier barato), montagem de request, caminho streaming e BATCH (-50% Opus),
e a invalidacao de sinal stale. Depende so de modulos JA extraidos (config/llm_client/cost/artifact_io)
+ context_pack/paths — NAO importa model -> sem circularidade. `model` importa e re-exporta estes nomes
p/ compat (model.batch_back_translate / high_risk_lines / ... seguem funcionando).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

import artifact_io   # noqa: E402
import context_pack  # noqa: E402
import paths          # noqa: E402
from config import MODEL_BACK, MAX_OUTPUT_TOKENS, BACK_SAMPLE_RATE, AWAITING, READY, DONE  # noqa: E402
from cost import log_api_call  # noqa: E402
from llm_client import (  # noqa: E402
    _client, _stream_final, _await_batch, _with_backoff, _text_of, _usage_of)


def back_translate(root, scene, high_lines, *, backend="api", model=None):
    """high_lines: lista de {offset, source, target, speaker, risk_notes}."""
    root = Path(root)
    scene_id = context_pack.scene_id_of(scene)
    out = paths.back_translation(root, scene, scene_id)
    if not high_lines:
        return {"status": DONE, "reviewed": 0, "path": None}
    if backend == "in-session":
        _write_back_prompt(root, scene, scene_id, high_lines)
        if out.is_file():
            return {"status": READY, "path": str(out), "reviewed": len(high_lines)}
        return {"status": AWAITING, "reviewed": len(high_lines),
                "prompt": str(paths.back_prompt(root, scene, scene_id)),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_BACK
        data, usage = _api_back_translate(root, scene, high_lines, m)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "reviewed": len(high_lines),
                "model": m, "usage": usage}
    raise ValueError(f"backend desconhecido: {backend}")


def _write_back_prompt(root, scene, scene_id, high_lines):
    L = [f"# Back-translation — cena {scene} ({len(high_lines)} linhas de alto risco)", "",
         "> Para cada linha: traduza o pt-BR de volta p/ EN, compare com o source, e confirme que",
         "> SENTIDO, ambiguidade, voz e timing foram preservados. Divergencia -> revisar a traducao.",
         f"> Saida: `back_translation_{scene_id}.json` = {{\"reviewed\": N, \"entries\": [",
         ">   {{offset, source, target, back_en, verdict: pass|revise, note}} ]}}.", ""]
    for h in high_lines:
        L.append(f"## {h['offset']} ({h.get('speaker','')})")
        L.append(f"- source : {h['source']}")
        L.append(f"- target : {h['target']}")
        if h.get("risk_notes"):
            L.append(f"- notas  : {h['risk_notes']}")
        L.append("")
    (paths.back_prompt(root, scene, scene_id)).write_text("\n".join(L), encoding="utf-8")


# Schema ESTRITO p/ a back-translation (garante JSON parseavel — sem ele o Opus as vezes devolvia
# texto vazio/markdown e o parse quebrava DEPOIS de ja cobrar a chamada: vazamento de Opus).
_BACK_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["entries"],
    "properties": {"entries": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["offset", "back_en", "verdict", "note"],
        "properties": {
            "offset": {"type": "string"}, "back_en": {"type": "string"},
            "verdict": {"type": "string", "enum": ["pass", "revise"]},
            "note": {"type": "string"},
        }}}},
}


def _back_params(high_lines, model):
    """Params de UMA requisicao de back-translation (compartilhado pelo caminho streaming e pelo BATCH).
    Determinista (sem rede) -> montagem do request testavel sem SDK."""
    payload = [{"offset": h["offset"], "source": h["source"], "target": h["target"],
                "speaker": h.get("speaker", "")} for h in high_lines]
    instr = ("Para cada item, traduza o 'target' (pt-BR) de volta p/ EN ('back_en'), compare com "
             "'source', e de um 'verdict' (pass|revise) + 'note' curta. verdict=revise se "
             "sentido/ambiguidade/voz divergirem. Inclua o 'offset' de cada item.\n\n")
    return {
        "model": model, "max_tokens": MAX_OUTPUT_TOKENS,
        "messages": [{"role": "user", "content": instr + json.dumps(payload, ensure_ascii=False)}],
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": "high",
                          "format": {"type": "json_schema", "schema": _BACK_SCHEMA}},
    }


def _api_back_translate(root, scene, high_lines, model):
    client = _client()
    msg = _stream_final(client, **_back_params(high_lines, model))
    usage = _usage_of(msg)
    log_api_call(root, scene, "back", model, usage)   # registra antes do parse (Opus cobra mesmo se quebrar)
    data = json.loads(_text_of(msg))
    data["reviewed"] = len(data.get("entries", []))
    return data, usage


def _plan_lines(root, scene):
    """Linhas brutas do translation_plan_<scene_id>.json (lista), ou [] se nao houver plano.
    Delega ao artifact_io (fonte unica do parse de plano)."""
    return artifact_io.plan_lines(root, scene)


def _ln_entry(ln):
    """Normaliza uma linha do plano p/ o shape de candidato de back-translation."""
    return {"offset": ln.get("offset", ""), "source": ln.get("text_source", ""),
            "target": ln.get("base_translation", ""), "speaker": ln.get("speaker", ""),
            "risk_notes": ln.get("risk_notes", "")}


def high_risk_lines(root, scene):
    """Linhas risco>=high/critical do translation_plan_<scene_id>.json (candidatas a back-translation).
    Le o plano do conector (existe apos build_plan). Fonte unica — run_scene e o batch leem daqui."""
    return [_ln_entry(ln) for ln in _plan_lines(root, scene)
            if ln.get("risk_level") in ("high", "critical")]


def sample_low_risk_lines(root, scene, rate=BACK_SAMPLE_RATE, *, seed="bt"):
    """Amostra DETERMINISTICA (~rate) das linhas low/medium — o piso de qualidade do tier barato.
    A inclusao depende so de sha1(seed|scene_id|offset): rodar 2x da o MESMO conjunto (idempotente,
    sem random). rate<=0 -> vazio. Retorna o mesmo shape de high_risk_lines."""
    if rate <= 0:
        return []
    scene_id = context_pack.scene_id_of(scene)
    out = []
    for ln in _plan_lines(root, scene):
        if ln.get("risk_level") in ("high", "critical"):
            continue
        h = hashlib.sha1(f"{seed}|{scene_id}|{ln.get('offset','')}".encode("utf-8")).hexdigest()
        if int(h[:8], 16) % 10000 < rate * 10000:
            out.append(_ln_entry(ln))
    return out


def back_translate_candidates(root, scene, sample_rate=BACK_SAMPLE_RATE):
    """Candidatos a back-translation = high/critical (sempre) UNIAO amostra ~sample_rate das low/medium.
    Dedup por offset (high vence). E a fonte de candidatos do batch_back_translate."""
    cands = high_risk_lines(root, scene)
    seen = {c["offset"] for c in cands}
    for c in sample_low_risk_lines(root, scene, sample_rate):
        if c["offset"] not in seen:
            cands.append(c)
            seen.add(c["offset"])
    return cands


def invalidate_back_translation(root, scene, offsets) -> int:
    """Marca como STALE as entries de back_translation dos `offsets` re-traduzidos: o verdict julgou o
    TEXTO ANTIGO, entao nao vale mais como crivo de qualidade. NAO apaga (preserva historico + permite
    re-julgar). O quality_gate trata entry stale como SEM cobertura. Retorna nº de entries marcadas."""
    root = Path(root)
    scene_id = context_pack.scene_id_of(scene)
    bt = paths.back_translation(root, scene, scene_id)
    if not bt.is_file():
        return 0
    try:
        data = json.loads(bt.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0
    offset_set = set(offsets)
    n = 0
    for e in data.get("entries", []):
        if e.get("offset") in offset_set and not e.get("stale"):
            e["stale"] = True
            n += 1
    if n:
        bt.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return n


def batch_back_translate(root, scenes, *, model=None, poll_seconds=30, max_wait_seconds=24 * 3600,
                         sample_rate=BACK_SAMPLE_RATE):
    """Back-translation de VARIAS cenas num UNICO batch (-50% sobre o Opus, o passo mais caro/linha).
    A back-translation e report-only e roda DEPOIS do verify (precisa do translation_plan) -> e um
    POS-PASSE natural: coleta os candidatos de cada cena (high/critical + amostra ~sample_rate das
    low/medium, p/ dar piso de qualidade ao tier barato), monta 1 request por cena e submete em batch.
    Grava back_translation_<scene_id>.json por cena. custom_id = scene.

    Resume idempotente: cena que ja tem back_translation_<scene_id>.json e pulada (nao re-cobra). Cena sem
    candidato -> 'no_high' (sem request). Retorna {scene: status} em
    {reviewed, no_high, errored, parse_failed, timeout}. NAO bloqueia o pipeline (o run_scene ja seguiu)."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    root = Path(root)
    m = model or MODEL_BACK
    status, highs, reqs = {}, {}, []
    for scene in scenes:
        scene_id = context_pack.scene_id_of(scene)
        out = paths.back_translation(root, scene, scene_id)
        hl = back_translate_candidates(root, scene, sample_rate)
        if not hl:
            status[scene] = "no_high"
            continue
        if out.is_file():                                # ja revisada (run anterior) -> nao re-cobra
            status[scene] = "reviewed"
            continue
        highs[scene] = hl
        reqs.append(Request(custom_id=scene,
                            params=MessageCreateParamsNonStreaming(**_back_params(hl, m))))
    if not reqs:
        return status
    client = _client()
    batch = _with_backoff(lambda: client.messages.batches.create(requests=reqs))
    if not _await_batch(client, batch.id, poll_seconds, max_wait_seconds):
        for scene in highs:
            status.setdefault(scene, "timeout")
        return status
    # materializa os resultados DENTRO do backoff (igual ao batch_translate; foi aqui que o cap.18 morreu)
    results = _with_backoff(lambda: list(client.messages.batches.results(batch.id)))
    for result in results:
        scene = result.custom_id
        if getattr(result.result, "type", None) != "succeeded":
            status[scene] = "errored"
            continue
        msg = result.result.message
        log_api_call(root, scene, "back", m, _usage_of(msg), batch=True)   # registra antes do parse
        try:
            data = json.loads(_text_of(msg))
            data["reviewed"] = len(data.get("entries", []))
            scene_id = context_pack.scene_id_of(scene)
            (paths.back_translation(root, scene, scene_id)).write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            status[scene] = "reviewed"
        except Exception:
            status[scene] = "parse_failed"                # cobrado (ledger), mas saida nao parseou
    return status
