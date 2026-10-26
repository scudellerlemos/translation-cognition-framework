#!/usr/bin/env python3
"""
model.py — INTERFACE de modelo do harness (agnosticismo de modelo).

Desacopla o run_scene do "como" a IA e chamada. Dois papeis de IA (so o que exige IA):
  - translate(...)      : traduz a cena a partir do pacote limitado (context_pack).
  - back_translate(...) : verifica linhas de alto risco (pt-BR -> EN -> confere sentido/voz).

Dois backends, mesmo contrato:
  (a) "in-session" (ASSINATURA): NAO chama rede. Garante o scene_prompt.md (auto-contido e limitado)
      e checa se o modelo do chat ja produziu o translations_<scene_id>.json. Como o prompt e limitado,
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
import sys
import time  # noqa: F401  (re-exportado p/ test_batch_retries fazer monkeypatch de model.time.sleep)
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)

_FRAMEWORK_CONNECTORS = _HERE.parent / "connectors"
if str(_FRAMEWORK_CONNECTORS) not in sys.path:
    sys.path.insert(0, str(_FRAMEWORK_CONNECTORS))

# Concern de back-translation extraido p/ back_translate.py (re-exportado aqui p/ compat).
from back_translate import (  # noqa: E402,F401
    _BACK_SCHEMA,
    _api_back_translate,
    _back_params,
    _ln_entry,
    _plan_lines,
    _write_back_prompt,
    back_translate,
    back_translate_candidates,
    batch_back_translate,
    high_risk_lines,
    invalidate_back_translation,
    sample_low_risk_lines,
)

# Constantes de tier/custo/status extraidas p/ config.py (re-exportadas aqui p/ compat).
from config import (  # noqa: E402,F401
    _BATCH_CHUNK,
    _MAX_TRIES,
    _TRANSLATE_SUBMIT_CHUNK,
    AWAITING,
    BACK_SAMPLE_RATE,
    BUDGET_ESCALATION,
    BUDGET_TOLERANCE,
    DONE,
    EFFORT_TRANSLATE,
    MAX_OUTPUT_TOKENS,
    MODEL_BACK,
    MODEL_ESCALATION,
    MODEL_TRANSLATE,
    MODEL_TRANSLATE_CHEAP,
    READY,
    THINK_TRANSLATE,
    BackTranslateAwaiting,
    BackTranslateDone,
    BackTranslateDoneApi,
    BackTranslateReady,
    BackTranslateResult,
    TranslateAwaiting,
    TranslateDone,
    TranslateReady,
    TranslateResult,
)

# Plumbing de API extraido p/ llm_client.py (re-exportado aqui p/ compat: model._client/_stream_final/...).
from llm_client import (  # noqa: E402,F401
    _MAX_BACKOFF,
    _add_usage,
    _await_batch,
    _carta_text,
    _client,
    _load_dotenv,
    _stream_final,
    _text_of,
    _transient_errors,
    _usage_of,
    _with_backoff,
)

# Caminhos de traducao (ADR 0019): API em model_api.py, sessao em model_session.py (re-exportados aqui p/ compat).
from model_api import (  # noqa: E402,F401
    _LINE_PROPS,
    _NL_RULE,
    _TRANSLATION_SCHEMA,
    _api_translate,
    _batch_coverage,
    _budget_note,
    _coverage_note,
    _merge_best_parity,
    _no_effort_model,
    _parse_batch_lines,
    _submit_translate_chunk,
    _tier_of,
    _to_map,
    _translate_params,
    _write_translations,
    batch_translate,
    retranslate_offsets,
)
from model_session import (  # noqa: E402,F401
    InvalidTranslationFile,
    read_translation,
    translate_in_session,
)

# Regras compartilhadas extraidas p/ translation_rules.py (re-exportadas aqui p/ compat).
from translation_rules import (  # noqa: E402,F401
    _BLOWUP_FACTOR,
    _BLOWUP_FLOOR,
    _ENGINE_LABEL_RX,
    _ENGINE_LABELS,
    _STRICT_ID,
    _TOKISH,
    _budget_len,
    _check_translation,
    _is_blowup,
    _is_tokish,
    _label_passthrough,
    _line_ok,
    _norm_t,
    _over_budget,
    _over_offsets,
    _parity_fit,
    _prefilled,
    _select_reuse,
    _struct_ok,
    _structural_rx,
    _translit_len,
    fix_newlines,
    over_budget_offsets,
    precheck,
    saved_pack,
)

# ------------------------------- TRANSLATE ------------------------------------







def translate(root, scene, *, backend="api", model=None, budget_tolerance=None) -> TranslateResult:
    """Traduz uma cena (use run_chapter --max-usd para teto duro por capitulo)."""
    root = Path(root)
    pack = saved_pack(root, scene) if backend == "in-session" else None
    if pack:
        print("      reconferencia: contexto da cena reaproveitado (falas e doutrina nao mudaram).")
    else:
        pack = context_pack.write_pack(root, scene)        # (re)gera prompt+pack (determinista)
    scene_id = pack["scene_id"]
    out = paths.translations(root, scene, scene_id)
    if backend == "in-session":
        return translate_in_session(root, scene, pack, out)
    if backend == "api":
        m = model or MODEL_TRANSLATE
        data, usage, meta = _api_translate(root, scene, pack, m, budget_tolerance=budget_tolerance)
        # V1: proveniência — doctrine/modelo gravados junto com a tradução para auditoria posterior
        data["_meta"] = {
            "model_id": m,
            "doctrine_hash": pack.get("doctrine_hash", ""),
            "skills_revision": pack.get("skills_revision", ""),
        }
        paths.atomic_write(out, json.dumps(data, ensure_ascii=False, indent=2))
        return {"status": DONE, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"],
                "model": m, "usage": usage, "reused": meta["reused"], "novel": meta["novel"]}
    raise ValueError(f"backend desconhecido: {backend}")


# BACK-TRANSLATE -> back_translate.py (back_translate/_write_back_prompt importados acima).


# ------------------------------- API backend ----------------------------------
# Implementacao fiel ao skill claude-api; import preguicoso, sem rede em import/teste.
# Endurecido p/ producao: streaming (.get_final_message) p/ saidas longas, output_config json_schema,
# backoff em erro transitorio, e guard do token de quebra + cobertura com retry (ver _api_translate).



# _load_dotenv / _client / _carta_text -> llm_client.py (importados acima).




# _text_of / _usage_of / _add_usage -> llm_client.py (importados acima).
# Preco/custo/ledger extraidos p/ cost.py (re-exportados aqui p/ compat: model.cost_of/log_api_call/_PRICE).
from cost import _PRICE, cost_of, log_api_call  # noqa: E402,F401

# _transient_errors / _with_backoff / _stream_final -> llm_client.py (importados acima).








# --------------------------- escalonamento CIRURGICO --------------------------
# Quando a verify falha por fitting, NAO re-traduzir a cena inteira: so as linhas que ESTOURAM o budget.
# Numa cena de 500 linhas com 2 estouros, re-traduz 2 (nao 500) -> corte de custo grande no caminho caro
# (medido na run viva do cap.13: o re-translate full custou ~$3,4 em 2 cenas).









# invalidate_back_translation -> back_translate.py (importado acima).




# ------------------------------- BATCH backend --------------------------------
# Batch API: 50% de desconto, assincrono (1 requisicao por cena num unico batch). Usa o MESMO system
# cacheado (Carta) -> cache compartilhado entre todas as cenas do batch, alem do desconto. Pre-passe de
# baixo custo: cenas que passam cobertura/paridade na 1a (sem retry) seguem; as que falham caem p/ o
# caminho interativo (streaming, com retry/escalonamento). Quem faz fitting (verify) continua sendo cada
# cena no run_scene. Determinismo da montagem do request isolado em _translate_params (testavel sem rede).















# _await_batch -> llm_client.py (importado acima).






# _BACK_SCHEMA / _back_params / _api_back_translate / high_risk_lines / sample_low_risk_lines /
# back_translate_candidates / batch_back_translate -> back_translate.py (importados acima).


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Interface de modelo do harness (translate).")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="api", choices=["in-session", "api"])
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    r = translate(a.project, a.scene, backend=a.backend, model=a.model)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
