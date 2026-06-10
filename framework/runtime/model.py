#!/usr/bin/env python3
"""
model.py — INTERFACE de modelo do harness (agnosticismo de modelo).

Desacopla o run_scene do "como" a IA e chamada. Dois papeis de IA (so o que exige IA):
  - translate(...)      : traduz a cena a partir do pacote limitado (context_pack).
  - back_translate(...) : verifica linhas de alto risco (pt-BR -> EN -> confere sentido/voz).

Dois backends, mesmo contrato:
  (a) "in-session" (ASSINATURA): NAO chama rede. Garante o scene_prompt.md (auto-contido e limitado)
      e checa se o modelo do chat ja produziu o translations_<sfx>.json. Como o prompt e limitado,
      da p/ responder UMA cena por sessao limpa -> o contexto nunca acumula (mata o estouro), sem
      conta de API. Resumivel: rode de novo apos o arquivo aparecer.
  (b) "api" (ESCALA HEADLESS): Anthropic SDK. Model-mix do cost_model — Sonnet traduz, Opus faz a
      back-translation; doutrina (Carta) cacheada via cache_control (cobrada ~1x). Import preguicoso
      e com erro claro se faltar SDK/chave. (Endurecimento contra o SDK vivo = P1; ver docs/MODEL_INTERFACE.)

GOVERNANCA: sem work-text hardcoded. O conteudo vem do pacote/artefatos. Determinismo do harness vem
do context_pack; a chamada de IA e a unica parte nao-determinista (por isso isolada aqui).
"""
from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402

# --- model-mix (defaults; cost_model cenario 'mix'): Sonnet traduz, Opus verifica alto risco ---
MODEL_TRANSLATE = "claude-sonnet-4-6"
MODEL_BACK = "claude-opus-4-8"

# Saida pode ser grande (ate ~500 linhas x speaker/tone/intent/risk/t). Streaming evita timeout;
# este teto cobre a maior cena do corpus com folga (Sonnet/Opus 4.x suportam ate 64k de saida).
MAX_OUTPUT_TOKENS = 64000
_MAX_TRIES = 3        # tentativas p/ corrigir saida invalida (cobertura / token de quebra)
_MAX_BACKOFF = 4      # tentativas de rede com backoff exponencial

AWAITING = "awaiting"   # o operador/modelo do chat precisa produzir a saida
READY = "ready"         # a saida ja existe
DONE = "done"           # chamada de IA concluida (backend api)


# ------------------------------- TRANSLATE ------------------------------------

def translate(root, scene, *, backend="in-session", model=None):
    root = Path(root)
    pack = context_pack.write_pack(root, scene)            # (re)gera prompt+pack (determinista)
    sfx = pack["sfx"]
    out = root / "artifacts" / scene / f"translations_{sfx}.json"
    if backend == "in-session":
        if out.is_file():
            return {"status": READY, "path": str(out), "sfx": sfx, "n_lines": pack["n_lines"]}
        return {"status": AWAITING, "sfx": sfx, "n_lines": pack["n_lines"],
                "prompt": str(root / "artifacts" / scene / "scene_prompt.md"),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_TRANSLATE
        data, usage = _api_translate(root, scene, pack, m)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "sfx": sfx, "n_lines": pack["n_lines"],
                "model": m, "usage": usage}
    raise ValueError(f"backend desconhecido: {backend}")


# ----------------------------- BACK-TRANSLATE ---------------------------------

def back_translate(root, scene, high_lines, *, backend="in-session", model=None):
    """high_lines: lista de {offset, source, target, speaker, risk_notes}."""
    root = Path(root)
    sfx = context_pack.sfx_of(scene)
    out = root / "artifacts" / scene / f"back_translation_{sfx}.json"
    if not high_lines:
        return {"status": DONE, "reviewed": 0, "path": None}
    if backend == "in-session":
        _write_back_prompt(root, scene, sfx, high_lines)
        if out.is_file():
            return {"status": READY, "path": str(out), "reviewed": len(high_lines)}
        return {"status": AWAITING, "reviewed": len(high_lines),
                "prompt": str(root / "artifacts" / scene / f"back_prompt_{sfx}.md"),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_BACK
        data, usage = _api_back_translate(high_lines, m)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "reviewed": len(high_lines),
                "model": m, "usage": usage}
    raise ValueError(f"backend desconhecido: {backend}")


def _write_back_prompt(root, scene, sfx, high_lines):
    L = [f"# Back-translation — cena {scene} ({len(high_lines)} linhas de alto risco)", "",
         "> Para cada linha: traduza o pt-BR de volta p/ EN, compare com o source, e confirme que",
         "> SENTIDO, ambiguidade, voz e timing foram preservados. Divergencia -> revisar a traducao.",
         f"> Saida: `back_translation_{sfx}.json` = {{\"reviewed\": N, \"entries\": [",
         ">   {{offset, source, target, back_en, verdict: pass|revise, note}} ]}}.", ""]
    for h in high_lines:
        L.append(f"## {h['offset']} ({h.get('speaker','')})")
        L.append(f"- source : {h['source']}")
        L.append(f"- target : {h['target']}")
        if h.get("risk_notes"):
            L.append(f"- notas  : {h['risk_notes']}")
        L.append("")
    (root / "artifacts" / scene / f"back_prompt_{sfx}.md").write_text("\n".join(L), encoding="utf-8")


# ------------------------------- API backend ----------------------------------
# Implementacao fiel ao skill claude-api; import preguicoso, sem rede em import/teste.
# Endurecido p/ producao: streaming (.get_final_message) p/ saidas longas, output_config json_schema,
# backoff em erro transitorio, e guard do token de quebra + cobertura com retry (ver _api_translate).

_TRANSLATION_SCHEMA = {
    "type": "object",
    "properties": {"lines": {"type": "object", "additionalProperties": {
        "type": "object",
        "properties": {
            "speaker": {"type": "string"}, "tone_register": {"type": "string"},
            "intent": {"type": "string"},
            "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
            "risk_notes": {"type": "string"}, "t": {"type": "string"},
        }, "required": ["speaker", "tone_register", "risk_level", "t"]}}},
    "required": ["lines"],
}


def _load_dotenv():
    """Carrega um `.env` (KEY=VALUE) p/ os.environ SEM dependencia externa. Nao sobrescreve
    variavel ja setada no ambiente (env real vence). Procura na raiz do framework e no CWD."""
    roots = [_HERE.parent.parent, Path.cwd()]   # framework/ (raiz do repo) e diretorio de execucao
    for base in roots:
        f = base / ".env"
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("backend 'api' requer o pacote 'anthropic' (pip install anthropic). "
                           "Use backend 'in-session' p/ o caminho assinatura.") from e
    _load_dotenv()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or "cole-sua-chave" in key:
        raise RuntimeError("backend 'api' requer ANTHROPIC_API_KEY: edite o `.env` na raiz do "
                           "framework e troque o placeholder pela sua chave real (veja .env.example).")
    return anthropic.Anthropic()


def _carta_text() -> str:
    return context_pack._read(context_pack.CARTA_PATH)


# Regra do token de quebra reforcada na borda da API: em JSON, o literal barra+n e escrito `\\n`.
# O modelo as vezes colapsa isso numa quebra de linha REAL (o bug recorrente) — instruimos e validamos.
_NL_RULE = (
    "\n\n## REGRA CRITICA DE SAIDA (token de quebra)\n"
    "Onde o source contem o token literal de quebra de linha, o campo \"t\" deve conte-lo como os DOIS "
    "caracteres literais barra-invertida + n (no JSON: escreva `\\\\n`), NUNCA uma quebra de linha real. "
    "Cubra TODOS os offsets listados na secao 7 — uma entrada por offset, sem excecao."
)


def _text_of(msg) -> str:
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


def _usage_of(msg) -> dict:
    u = getattr(msg, "usage", None)
    if not u:
        return {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    return {"in": getattr(u, "input_tokens", 0) or 0,
            "out": getattr(u, "output_tokens", 0) or 0,
            "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0}


def _add_usage(acc: dict, u: dict) -> dict:
    for k in ("in", "out", "cache_read", "cache_write"):
        acc[k] = acc.get(k, 0) + u.get(k, 0)
    return acc


def _stream_final(client, **kwargs):
    """Streaming + backoff. Streaming evita timeout em saidas longas; backoff cobre 429/500/timeout."""
    import anthropic
    transient = (anthropic.RateLimitError, anthropic.InternalServerError,
                 anthropic.APITimeoutError, anthropic.APIConnectionError)
    delay = 2.0
    for i in range(_MAX_BACKOFF):
        try:
            with client.messages.stream(**kwargs) as s:
                return s.get_final_message()
        except transient:
            if i == _MAX_BACKOFF - 1:
                raise
            time.sleep(delay)
            delay *= 2


def _check_translation(data, offsets):
    """Retorna (offsets_com_quebra_real, offsets_faltando). Guard do bug do token \\n + cobertura."""
    lines = data.get("lines", {}) if isinstance(data, dict) else {}
    bad_nl = [off for off, v in lines.items() if "\n" in ((v or {}).get("t", "") or "")]
    missing = [o for o in offsets if o not in lines]
    return bad_nl, missing


def _api_translate(root, scene, pack, model):
    client = _client()
    # system = doutrina estavel (cacheada ~1x via cache_control); user = pacote da cena
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    base_user = context_pack.render_prompt(pack, carta="") + _NL_RULE  # Carta ja no system
    offsets = [r["offset"] for r in pack["lines"]]
    note, last, usage = "", None, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    for _ in range(_MAX_TRIES):
        msg = _stream_final(
            client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": base_user + note}],
            thinking={"type": "adaptive"},
            output_config={"effort": "high",
                           "format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}},
        )
        _add_usage(usage, _usage_of(msg))
        data = json.loads(_text_of(msg))
        bad_nl, missing = _check_translation(data, offsets)
        if not bad_nl and not missing:
            return data, usage
        last = {"bad_nl": bad_nl, "missing": missing}
        note = "\n\n## CORRECAO NECESSARIA (regere a saida COMPLETA)\n"
        if bad_nl:
            note += (f"- Estes offsets tem QUEBRA DE LINHA REAL no campo t; use `\\\\n` literal: "
                     f"{bad_nl[:25]}\n")
        if missing:
            note += f"- Faltam estes offsets (cubra TODOS): {missing[:25]}\n"
    raise RuntimeError(f"_api_translate: saida invalida apos {_MAX_TRIES} tentativas: {last}")


def _api_back_translate(high_lines, model):
    client = _client()
    payload = [{"offset": h["offset"], "source": h["source"], "target": h["target"],
                "speaker": h.get("speaker", "")} for h in high_lines]
    instr = ("Para cada item, traduza o 'target' (pt-BR) de volta p/ EN, compare com 'source' e "
             "responda JSON {\"reviewed\":N,\"entries\":[{offset,back_en,verdict:pass|revise,note}]}. "
             "verdict=revise se sentido/ambiguidade/voz divergirem.\n\n")
    msg = _stream_final(
        client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": instr + json.dumps(payload, ensure_ascii=False)}],
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
    )
    return json.loads(_text_of(msg)), _usage_of(msg)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Interface de modelo do harness (translate).")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="in-session", choices=["in-session", "api"])
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    r = translate(a.project, a.scene, backend=a.backend, model=a.model)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
