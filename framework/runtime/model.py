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
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402

# --- model-mix (defaults; cost_model cenario 'mix'): Sonnet traduz, Opus verifica alto risco ---
MODEL_TRANSLATE = "claude-sonnet-4-6"
MODEL_BACK = "claude-opus-4-8"

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
        data = _api_translate(root, scene, pack, model or MODEL_TRANSLATE)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "sfx": sfx, "n_lines": pack["n_lines"]}
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
        data = _api_back_translate(high_lines, model or MODEL_BACK)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "reviewed": len(high_lines)}
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
# Endurecimento contra o SDK vivo (messages.parse / output_config) = P1.

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


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("backend 'api' requer o pacote 'anthropic' (pip install anthropic). "
                           "Use backend 'in-session' p/ o caminho assinatura.") from e
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("backend 'api' requer ANTHROPIC_API_KEY no ambiente.")
    return anthropic.Anthropic()


def _carta_text() -> str:
    return context_pack._read(context_pack.CARTA_PATH)


def _api_translate(root, scene, pack, model):
    client = _client()
    # system = doutrina estavel (cacheada ~1x via cache_control); user = pacote da cena
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    user = context_pack.render_prompt(pack, carta="")     # sem reembutir a Carta (ja no system)
    msg = client.messages.create(
        model=model, max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": user}],
        thinking={"type": "adaptive"},
        output_config={"effort": "high",
                       "format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}},
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    return json.loads(text)


def _api_back_translate(high_lines, model):
    client = _client()
    payload = [{"offset": h["offset"], "source": h["source"], "target": h["target"],
                "speaker": h.get("speaker", "")} for h in high_lines]
    instr = ("Para cada item, traduza o 'target' (pt-BR) de volta p/ EN, compare com 'source' e "
             "responda JSON {\"reviewed\":N,\"entries\":[{offset,back_en,verdict:pass|revise,note}]}. "
             "verdict=revise se sentido/ambiguidade/voz divergirem.\n\n")
    msg = client.messages.create(
        model=model, max_tokens=8000,
        messages=[{"role": "user", "content": instr + json.dumps(payload, ensure_ascii=False)}],
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    return json.loads(text)


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
