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
import re
import sys
import time  # noqa: F401  (re-exportado p/ test_batch_retries fazer monkeypatch de model.time.sleep)
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import context_pack  # noqa: E402
import paths  # noqa: E402  (paths.py: fonte unica do contrato de caminhos de artefato)
import state_index  # noqa: E402  (sibling; _key p/ dedup por TM)

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
    AWAITING,
    BACK_SAMPLE_RATE,
    BUDGET_ESCALATION,
    BUDGET_TOLERANCE,
    DONE,
    EFFORT_TRANSLATE,
    MAX_OUTPUT_TOKENS,
    MODEL_BACK,
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


def _no_effort_model(model: str) -> bool:
    """Modelos que NAO aceitam output_config.effort nem adaptive thinking (400): Haiku 4.5 e Sonnet 4.5.
    Opus 4.x e Sonnet 4.6 aceitam. Usado p/ montar params validos por modelo (tiering de custo)."""
    return model.startswith("claude-haiku") or model == "claude-sonnet-4-5"


# ------------------------------- TRANSLATE ------------------------------------

def translate(root, scene, *, backend="api", model=None, budget_tolerance=None, max_usd=None) -> TranslateResult:
    """Traduz uma cena. `max_usd` e informativo: emite aviso se o custo estimado supera o teto,
    mas NAO aborta (use run_chapter --max-usd para teto duro por capitulo)."""
    root = Path(root)
    pack = context_pack.write_pack(root, scene)            # (re)gera prompt+pack (determinista)
    scene_id = pack["scene_id"]
    out = paths.translations(root, scene, scene_id)
    if backend == "in-session":
        if out.is_file():
            return {"status": READY, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"]}
        return {"status": AWAITING, "scene_id": scene_id, "n_lines": pack["n_lines"],
                "prompt": str(paths.scene_prompt(root, scene)),
                "expected_output": str(out)}
    if backend == "api":
        m = model or MODEL_TRANSLATE
        if max_usd is None:
            import warnings
            warnings.warn(
                f"translate({scene}): sem teto de custo (max_usd=None). "
                "Use run_chapter --max-usd para teto duro por capitulo.", stacklevel=2)
        data, usage, meta = _api_translate(root, scene, pack, m, budget_tolerance=budget_tolerance)
        c = cost_of(m, usage)
        if max_usd is not None and c > max_usd:
            import warnings
            warnings.warn(f"translate({scene}): custo ${c:.4f} excedeu max_usd=${max_usd:.4f}.", stacklevel=2)
        # V1: proveniência — doctrine/modelo gravados junto com a tradução para auditoria posterior
        data["_meta"] = {
            "model_id": m,
            "doctrine_hash": pack.get("doctrine_hash", ""),
            "skills_revision": pack.get("skills_revision", ""),
        }
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": DONE, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"],
                "model": m, "usage": usage, "reused": meta["reused"], "novel": meta["novel"]}
    if backend == "ollama":
        from ollama_client import OLLAMA_MODEL_DEFAULT  # import preguicoso — sem rede em import
        m = model or OLLAMA_MODEL_DEFAULT
        data, usage, meta = _ollama_translate(root, scene, pack, m)
        data["_meta"] = {"model_id": m, "backend": "ollama",
                         "doctrine_hash": pack.get("doctrine_hash", "")}
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        log_api_call(root, scene, "translate", f"ollama:{m}", usage)
        return {"status": DONE, "path": str(out), "scene_id": scene_id, "n_lines": pack["n_lines"],
                "model": m, "usage": usage, "reused": meta["reused"], "novel": meta["novel"]}
    raise ValueError(f"backend desconhecido: {backend}")


# BACK-TRANSLATE -> back_translate.py (back_translate/_write_back_prompt importados acima).


# ------------------------------- API backend ----------------------------------
# Implementacao fiel ao skill claude-api; import preguicoso, sem rede em import/teste.
# Endurecido p/ producao: streaming (.get_final_message) p/ saidas longas, output_config json_schema,
# backoff em erro transitorio, e guard do token de quebra + cobertura com retry (ver _api_translate).

# Structured output ESTRITO exige additionalProperties:false em todo objeto -> nao da p/ usar mapa
# {offset: {...}} (chaves dinamicas). Logo: ARRAY de entradas com 'offset' por item; convertido p/ o
# mapa {offset: {...}} (formato canonico do translations_<scene_id>.json) apos parsear (ver _api_translate).
_LINE_PROPS = {
    "offset": {"type": "string"}, "speaker": {"type": "string"},
    "tone_register": {"type": "string"}, "intent": {"type": "string"},
    "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
    "risk_notes": {"type": "string"}, "t": {"type": "string"},
}
_TRANSLATION_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["lines"],
    "properties": {"lines": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": _LINE_PROPS,
        "required": ["offset", "speaker", "tone_register", "intent",
                     "risk_level", "risk_notes", "t"],
    }}},
}


# _load_dotenv / _client / _carta_text -> llm_client.py (importados acima).


# Regra do token de quebra reforcada na borda da API: em JSON, o literal barra+n e escrito `\\n`.
# O modelo as vezes colapsa isso numa quebra de linha REAL (o bug recorrente) — instruimos e validamos.
_NL_RULE = (
    "\n\n## FORMATO DE SAIDA (sobrepoe a secao 8)\n"
    "Responda um objeto JSON com a chave \"lines\" = ARRAY de entradas; cada entrada tem os campos "
    "`offset, speaker, tone_register, intent, risk_level, risk_notes, t` (preencha todos; `risk_notes` "
    "pode ser \"\" quando risco baixo). Uma entrada por offset da secao 7 — cubra TODOS, sem excecao.\n"
    "## REGRA CRITICA (token de quebra)\n"
    "Onde o source contem o token literal de quebra de linha, o campo \"t\" deve conte-lo como os DOIS "
    "caracteres literais barra-invertida + n (no JSON: escreva `\\\\n`), NUNCA uma quebra de linha real."
)


# _text_of / _usage_of / _add_usage -> llm_client.py (importados acima).
# Preco/custo/ledger extraidos p/ cost.py (re-exportados aqui p/ compat: model.cost_of/log_api_call/_PRICE).
from cost import _PRICE, cost_of, log_api_call  # noqa: E402,F401

# _transient_errors / _with_backoff / _stream_final -> llm_client.py (importados acima).


def _check_translation(data, offsets):
    """Retorna (offsets_com_quebra_real, offsets_faltando). Guard do bug do token \\n + cobertura."""
    lines = data.get("lines", {}) if isinstance(data, dict) else {}
    bad_nl = [off for off, v in lines.items() if "\n" in ((v or {}).get("t", "") or "")]
    missing = [o for o in offsets if o not in lines]
    return bad_nl, missing


def _translit_len(t) -> int:
    """Comprimento em bytes da forma TRANSLITERADA (NFKD + drop combining) — o que o reinsert grava."""
    s = unicodedata.normalize("NFKD", t or "")
    return len("".join(c for c in s if not unicodedata.combining(c)))


def _norm_t(t):
    """Normaliza o campo: CR/LF real -> token literal `\\n` (o modelo as vezes colapsa o token numa
    quebra real). Deterministico/idempotente. A PARIDADE com a fonte e ajustada em _parity_fit."""
    if not isinstance(t, str):
        return t
    tok = context_pack.TOKEN
    return t.replace("\r\n", tok).replace("\n", tok).replace("\r", tok)


def _parity_fit(source, t):
    """Ciente da fonte: se a FONTE nao tem token de quebra, o ALVO tambem nao pode ter (o modelo as
    vezes adiciona uma quebra espuria -> build_plan reprova por paridade). Troca token por espaco e
    colapsa. Se a fonte TEM quebra(s), mantem (o modelo costuma casar; mismatch multi-token -> retry)."""
    if not isinstance(t, str):
        return t
    tok = context_pack.TOKEN
    if tok not in (source or ""):
        out = t.replace(tok, " ")
        while "  " in out:
            out = out.replace("  ", " ")
        return out.strip()
    return t


# Guarda contra BLOW-UP patologico de comprimento: o modelo (raro) emite centenas/milhares de chars de
# lixo p/ uma linha curta (medido: um grito de ~17 chars virou 5872 chars de ruido num batch -> passou o
# fitting so porque AQUELA linha tinha byte_budget; uma sem budget escaparia). Rejeitamos a traducao cuja
# forma TRANSLITERADA passa de _BLOWUP_FACTOR x a fonte (piso _BLOWUP_FLOOR p/ nao punir linha curta
# legitima) -> a linha conta como NAO retornada (re-roda / fica 'missing' -> coverage a pega), nunca aceita.
_BLOWUP_FACTOR = 8
_BLOWUP_FLOOR = 200


def _is_blowup(source, t) -> bool:
    """True se `t` e patologicamente mais longa que `source` (lixo provavel do modelo)."""
    if not isinstance(t, str):
        return False
    return _translit_len(t) > max(_translit_len(source or "") * _BLOWUP_FACTOR, _BLOWUP_FLOOR)


# RÓTULO DE ENGINE: identificadores internos de rig/asset que NAO sao dialogo — body, face,
# hair, mask, Leg_2_B_L, ch120_01, env_bone, lightA02. O LLM os TRADUZIA, estourava o byte_budget e
# disparava o retighten (re-traducao = 58% do custo medido no ledger). Solucao: PASSTHROUGH
# deterministico (t = fonte), fora do lote do LLM.
#
# ALLOWLIST EXPLICITA: labels conhecidos que NUNCA sao dialogo (qualquer um desses => passthrough imediato).
# Adicionar aqui quando aparecer um novo label traduzido indevidamente no ledger.
_ENGINE_LABELS = frozenset({
    "body", "face", "hair", "mask", "env_bone", "bone",
    "light", "lightA", "lightB", "lightC",
})
_ENGINE_LABEL_RX = re.compile(
    r"^(body|face|hair|mask|env_bone|bone|light[A-Za-z0-9]*"
    r"|ch\d+_\d+|Leg_\d+_[A-Z]_[LR]|Spine\d*|Root|Hips"
    r"|[A-Z][a-z]+(?:[A-Z][a-z]+)+\d*"   # CamelCase strict (LeftFoot, RightArm...)
    r"|[a-z]+[A-Z]\w+\d*"                # camelCase (lightA02)
    r")\Z"
)
# Deteccao HEURISTICA de bloco de rotulos (corrida de tokens-unicos com >=1 STRICT_ID):
# detecta casos nao cobertos pela allowlist — nao substitui, complementa.
_TOKISH = re.compile(r"[A-Za-z][\w]*\Z")
_STRICT_ID = re.compile(r"[A-Za-z]\w*_\w+\Z|[A-Za-z]+\d\w*\Z|[A-Z][a-z]+(?:[A-Z][a-z]+)+\Z")


def _is_tokish(s: str) -> bool:
    s = (s or "").strip()
    return bool(s) and len(s) <= 16 and bool(_TOKISH.match(s))


def _label_passthrough(pack) -> dict:
    """Mapa {offset: entry} das linhas que sao rotulo de engine (t = fonte, sem ir ao LLM).
    Prioridade: allowlist explicita (_ENGINE_LABELS / _ENGINE_LABEL_RX) -> heuristica de bloco."""
    lines = pack.get("lines", [])
    out, i, n = {}, 0, len(lines)

    def _passthrough(r):
        return {"speaker": "", "tone_register": "", "intent": "rotulo_engine",
                "risk_level": "low", "risk_notes": "", "t": r.get("source", "") or ""}

    while i < n:
        s = (lines[i].get("source", "") or "").strip()
        # Allowlist explicita: passthrough imediato, sem precisar de bloco vizinho
        if s.lower() in _ENGINE_LABELS or _ENGINE_LABEL_RX.match(s):
            out[lines[i]["offset"]] = _passthrough(lines[i])
            i += 1
            continue
        # Heuristica de bloco: corrida de tokens-unicos com >=1 STRICT_ID
        if not _is_tokish(s):
            i += 1
            continue
        j = i
        while j < n and _is_tokish((lines[j].get("source", "") or "").strip()):
            j += 1
        run = lines[i:j]
        if any(_STRICT_ID.match((r.get("source", "") or "").strip()) for r in run):
            for r in run:
                rs = (r.get("source", "") or "").strip()
                if _STRICT_ID.match(rs) or rs.islower():   # capitalizada (Sim/OK) fica no LLM
                    out[r["offset"]] = _passthrough(r)
        i = j
    return out


def _select_reuse(pack, *, enabled):
    """DEDUP por TM: linhas cuja fonte JA foi traduzida em OUTRA cena -> reusa a traducao estabelecida
    em vez de re-gerar (corta tokens de SAIDA, 5x o custo de entrada; e a consistencia ja vem de graca).
    Guards: (1) nunca reusa a PROPRIA cena — a TM e reconstruida apos cada cena, entao re-rodar a poria
    na TM e a dedup reusaria a saida velha, sabotando o escalonamento de fitting (que quer ENCURTAR);
    (2) paridade de quebra: a chave de TM normaliza ignorando `\\n`, entao so reusa se a contagem do token
    na traducao casar a da fonte ATUAL (senao o build_plan reprova por paridade). Desligado (vazio) no
    escalonamento (enabled=False) p/ re-traduzir fresco e mais curto. Determinista (testavel sem rede)."""
    if not enabled:
        return {}
    tok = context_pack.TOKEN
    scene_id_here = pack.get("scene_id", "")
    by_key = {}
    for e in pack.get("tm_exact", []):
        if context_pack.scene_id_of(str(e.get("from_scene", ""))) == scene_id_here:
            continue                                  # nunca reusar a propria cena
        by_key.setdefault(state_index._key(e.get("source", "")), e)
    reuse = {}
    for r in pack.get("lines", []):
        e = by_key.get(state_index._key(r.get("source", "")))
        if not e:
            continue
        tgt = e.get("target", "")
        if not tgt or tgt.count(tok) != (r.get("source", "") or "").count(tok):
            continue                                  # paridade de quebra com a fonte ATUAL
        reuse[r["offset"]] = {"speaker": e.get("speaker", ""), "tone_register": "",
                              "intent": "reuso_tm", "risk_level": "low", "risk_notes": "",
                              "t": _norm_t(tgt)}
    return reuse


def _to_map(data):
    """Converte a saida estruturada {lines:[{offset,...}]} no formato canonico {lines:{offset:{...}}}.
    Tolera ja vir em mapa (idempotente). Remove 'offset' do corpo da entrada e normaliza o `t`."""
    lines = (data or {}).get("lines")
    if isinstance(lines, dict):
        for v in lines.values():
            if isinstance(v, dict) and "t" in v:
                v["t"] = _norm_t(v["t"])
        return data
    out = {}
    for e in (lines or []):
        off = e.get("offset")
        if not off:
            continue
        body = {k: v for k, v in e.items() if k != "offset"}
        if "t" in body:
            body["t"] = _norm_t(body["t"])
        out[off] = body
    return {"lines": out}


def _api_translate(root, scene, pack, model, *, effort=EFFORT_TRANSLATE, think=THINK_TRANSLATE,
                   budget_tolerance=None, quality_note=""):
    tol = budget_tolerance or BUDGET_TOLERANCE
    tok = context_pack.TOKEN
    # DEDUP por TM (so no 1o passe; desligado no escalonamento de fitting p/ re-traduzir mais curto):
    # linhas com fonte ja traduzida em OUTRA cena nao vao ao modelo (corta tokens de saida).
    reuse = _select_reuse(pack, enabled=(budget_tolerance is None))
    reuse.update(_label_passthrough(pack))            # rotulo de engine: passthrough SEMPRE (ate no retighten)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    meta = {"reused": len(reuse), "novel": len(novel), "n_lines": len(pack["lines"])}
    if not novel:                                     # cena 100% reaproveitada -> zero chamada de API
        return {"lines": dict(reuse)}, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}, meta

    client = _client()
    # system = doutrina estavel (cacheada ~1x via cache_control); user = pacote da cena (so as novas)
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    novel_by_off = {r["offset"]: r for r in novel}
    offsets = [r["offset"] for r in novel]
    offset_set = set(offsets)
    budgets = {r["offset"]: r.get("byte_budget") for r in novel}
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    last, usage = None, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    merged = {}        # ACUMULA linhas entre tentativas: cada retry preenche lacunas -> cobertura converge
    # thinking custa como saida ($15/M). Traducao com contexto curado raramente exige raciocinio
    # profundo -> default sem thinking + effort baixo (medido: corta ~5x o custo; ver OBSERVABILITY).
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort nem adaptive thinking (400) -> omitir.
    no_effort = _no_effort_model(model)
    thinking = {"type": "adaptive"} if (think and not no_effort) else {"type": "disabled"}
    out_cfg = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
    if not no_effort:
        out_cfg["effort"] = effort

    def _over(off, v):
        b = budgets.get(off)
        return b and _translit_len((v or {}).get("t", "")) > b * tol

    def _render(target, note):
        # PREVISIBILIDADE (recuperacao por-linha): o 1o passe manda TODAS as linhas novas; a re-rodada manda
        # SO as quebradas (faltantes/paridade-ruim/acima-do-budget), nunca a cena inteira de novo. O
        # context_pack (glossario/vozes/decisoes/TM) vai junto em qualquer caso -> a coerencia de cena se
        # preserva; muda so a LISTA de linhas a traduzir -> custo de retry ∝ linhas quebradas, nao ∝ cena.
        red = dict(pack); red["lines"] = target; red["n_lines"] = len(target)
        return context_pack.render_prompt(red, carta="") + _NL_RULE + quality_note + note

    target, note = novel, ""   # quality_note (back-translation/quality_fix) entra via _render; "" no fluxo normal
    for attempt in range(_MAX_TRIES):
        msg = _stream_final(
            client, model=model, max_tokens=MAX_OUTPUT_TOKENS,
            system=system,
            messages=[{"role": "user", "content": _render(target, note)}],
            thinking=thinking,
            output_config=out_cfg,
        )
        u_attempt = _usage_of(msg)
        _add_usage(usage, u_attempt)
        log_api_call(root, scene, "translate", model, u_attempt)   # registra ANTES de qualquer parse/gate
        data = _to_map(json.loads(_text_of(msg)))   # array -> mapa {offset:{...}}; CR/LF real -> token
        for off, v in data.get("lines", {}).items():
            if off not in offset_set or not isinstance(v, dict):
                continue
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))   # quebra espuria -> espaco
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue                                 # lixo patologico -> descarta (vira 'missing' -> retry)
            good_parity = (v["t"].count(tok) == srcmap.get(off, "").count(tok))
            if off not in merged:
                merged[off] = v                      # preenche lacuna
            else:
                old = merged[off]
                old_parity = (old.get("t", "").count(tok) == srcmap.get(off, "").count(tok))
                if good_parity and not old_parity:
                    merged[off] = v                  # prioriza paridade correta
                elif good_parity == old_parity and _over(off, old) and \
                        _translit_len(v.get("t", "")) < _translit_len(old.get("t", "")):
                    merged[off] = v                  # mesma paridade: prefere a mais curta (budget)
        missing = [o for o in offsets if o not in merged]
        bad_par = [o for o in merged if merged[o].get("t", "").count(tok) != srcmap.get(o, "").count(tok)]
        over = [(o, budgets[o], _translit_len(merged[o].get("t", "")))
                for o in merged if _over(o, merged[o])]
        last = {"missing": missing, "bad_parity": bad_par, "over_budget": over}
        # HARD (bloqueia): cobertura + paridade de quebra (build_plan reprova). SOFT (best-effort):
        # byte_budget — o conector absorve via head-reloc; a VERIFY (round-trip) e o juiz de residuo.
        if not missing and not bad_par and (not over or attempt == _MAX_TRIES - 1):
            merged.update(reuse)                      # reanexa as linhas reaproveitadas da TM
            return {"lines": merged}, usage, meta
        # PROXIMA RODADA = SO as linhas quebradas (recuperacao por-linha, nao re-traduz a cena inteira)
        broken = set(missing) | set(bad_par) | {o for o, _b, _c in over}
        target = [novel_by_off[o] for o in offsets if o in broken]
        note = "\n\n## CORRECAO NECESSARIA (traduza SO as linhas acima; vamos MESCLAR com o resto ja pronto)\n"
        if missing:
            note += f"- Faltam estes offsets — INCLUA todos: {missing[:40]}\n"
        if bad_par:
            note += (f"- Estes offsets tem nº de quebras `\\n` DIFERENTE da fonte — case EXATO (mesma "
                     f"quantidade e posicao do token): {bad_par[:30]}\n")
        if over:
            note += ("- Estes offsets passam do byte_budget (TRANSLITERADO, sem acentos); ENCURTE "
                     "preservando o sentido (corte redundancia; ex.: 'adicionado ao'->'no'):\n")
            for off, b, cur in over[:25]:
                note += f"  - {off}: budget {b}, atual {cur}\n"
    raise RuntimeError(f"_api_translate: cobertura/paridade incompletas apos {_MAX_TRIES} tentativas: "
                       f"faltam={last['missing']} paridade={last['bad_parity']}")


# ------------------------------- OLLAMA backend -------------------------------
# Backend local (zero custo de API). Usa a mesma prompt do API backend (doutrina + pack)
# e o mesmo schema de saida (_TRANSLATION_SCHEMA). Sem cache nem batch — 1 request por cena.
# Retry simples em cobertura/paridade (ate _MAX_TRIES tentativas).

def _ollama_translate(root, scene, pack, model):
    """Traduz uma cena usando Ollama local. Interface identica ao _api_translate.

    Retorna (data, usage, meta). usage = {in, out, cache_read:0, cache_write:0}.
    Custo = $0 (local). Sem tiering, sem batch — path simples e direto.
    """
    from ollama_client import _chat as _oc_chat
    from ollama_client import _text_of as _oc_text
    from ollama_client import _usage_of as _oc_usage

    reuse = _select_reuse(pack, enabled=True)
    reuse.update(_label_passthrough(pack))
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    meta = {"reused": len(reuse), "novel": len(novel), "n_lines": len(pack["lines"])}
    if not novel:
        return {"lines": dict(reuse)}, {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}, meta

    tok = context_pack.TOKEN
    offsets = [r["offset"] for r in novel]
    offset_set = set(offsets)
    srcmap = {r["offset"]: r.get("source", "") for r in novel}

    system_text = _carta_text()
    merged = {}
    usage = {"in": 0, "out": 0, "cache_read": 0, "cache_write": 0}
    target, note = novel, ""

    for attempt in range(_MAX_TRIES):
        red = dict(pack); red["lines"] = target; red["n_lines"] = len(target)
        user_text = context_pack.render_prompt(red, carta="") + _NL_RULE + note
        messages = [
            {"role": "system", "content": system_text},
            {"role": "user",   "content": user_text},
        ]
        try:
            resp = _oc_chat(model, messages, fmt=_TRANSLATION_SCHEMA)
        except RuntimeError as e:
            raise RuntimeError(f"_ollama_translate (tentativa {attempt+1}): {e}") from e

        u = _oc_usage(resp)
        _add_usage(usage, u)

        try:
            data = _to_map(json.loads(_oc_text(resp)))
        except Exception:
            if attempt < _MAX_TRIES - 1:
                note = "\n\n## CORRECAO: resposta anterior era JSON invalido. Tente novamente.\n"
                continue
            break

        novel_by_off = {r["offset"]: r for r in novel}
        for off, v in data.get("lines", {}).items():
            if off not in offset_set or not isinstance(v, dict):
                continue
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue
            if off not in merged:
                merged[off] = v
            else:
                old_par = merged[off].get("t", "").count(tok) == srcmap.get(off, "").count(tok)
                new_par = v.get("t", "").count(tok) == srcmap.get(off, "").count(tok)
                if new_par and not old_par:
                    merged[off] = v

        missing = [o for o in offsets if o not in merged]
        bad_par = [o for o in merged
                   if merged[o].get("t", "").count(tok) != srcmap.get(o, "").count(tok)]
        if not missing and not bad_par:
            break

        broken = set(missing) | set(bad_par)
        target = [novel_by_off[o] for o in offsets if o in broken]
        note = "\n\n## CORRECAO NECESSARIA (traduza SO as linhas acima)\n"
        if missing:
            note += f"- Faltam: {missing[:30]}\n"
        if bad_par:
            note += f"- Token de quebra errado: {bad_par[:20]}\n"

    merged.update(reuse)
    return {"lines": merged}, usage, meta


# --------------------------- escalonamento CIRURGICO --------------------------
# Quando a verify falha por fitting, NAO re-traduzir a cena inteira: so as linhas que ESTOURAM o budget.
# Numa cena de 500 linhas com 2 estouros, re-traduz 2 (nao 500) -> corte de custo grande no caminho caro
# (medido na run viva do cap.13: o re-translate full custou ~$3,4 em 2 cenas).

def _over_offsets(budgets: dict, lines: dict, tolerance: float = 1.0) -> list:
    """Offsets cuja traducao TRANSLITERADA (sem acentos — o que vai p/ os bytes) excede
    byte_budget*tolerance. Puro/deterministico (testavel sem rede)."""
    over = []
    for off, b in budgets.items():
        if not b:
            continue
        v = lines.get(off)
        if v and _translit_len((v or {}).get("t", "")) > b * tolerance:
            over.append(off)
    return sorted(over)


def over_budget_offsets(root, scene, *, tolerance: float = 1.0) -> list:
    """Le o translations_<scene_id>.json atual e devolve os offsets acima do budget (candidatos a estouro)."""
    root = Path(root)
    pack = context_pack.build_pack(root, scene)
    out = paths.translations(root, scene, pack['scene_id'])
    if not out.is_file():
        return []
    data = json.loads(out.read_text(encoding="utf-8"))
    budgets = {r["offset"]: r.get("byte_budget") for r in pack["lines"]}
    return _over_offsets(budgets, data.get("lines", {}), tolerance)


# invalidate_back_translation -> back_translate.py (importado acima).


def retranslate_offsets(root, scene, offsets, *, model=None, budget_tolerance, quality_note=""):
    """Re-traduz APENAS `offsets` (apertado por budget_tolerance) e MESCLA no translations_<scene_id>.json,
    preservando todas as outras linhas. Caminho cirurgico do escalonamento de fitting (e do quality_fix).
    Reusa _api_translate sobre um pack reduzido (dedup ja vem OFF com budget_tolerance != None -> traduz
    fresco e mais curto). `quality_note` opcional anexa feedback de revisao da back-translation ao prompt."""
    root = Path(root)
    pack = context_pack.build_pack(root, scene)
    scene_id = pack["scene_id"]
    out = paths.translations(root, scene, scene_id)
    full = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {"lines": {}}
    offset_set = set(offsets)
    sub = dict(pack)
    sub["lines"] = [r for r in pack["lines"] if r["offset"] in offset_set]
    sub["n_lines"] = len(sub["lines"])
    if not sub["lines"]:
        return {"status": DONE, "model": model or MODEL_TRANSLATE, "usage": None,
                "n_lines": 0, "reused": 0, "novel": 0}
    m = model or MODEL_TRANSLATE
    data, usage, meta = _api_translate(root, scene, sub, m, budget_tolerance=budget_tolerance,
                                       quality_note=quality_note)
    full.setdefault("lines", {}).update(data.get("lines", {}))   # merge: so os offsets re-traduzidos
    out.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    invalidate_back_translation(root, scene, offset_set)         # o verdict antigo nao vale mais
    return {"status": DONE, "model": m, "usage": usage, "n_lines": sub["n_lines"],
            "reused": meta["reused"], "novel": meta["novel"]}


# ------------------------------- BATCH backend --------------------------------
# Batch API: 50% de desconto, assincrono (1 requisicao por cena num unico batch). Usa o MESMO system
# cacheado (Carta) -> cache compartilhado entre todas as cenas do batch, alem do desconto. Pre-passe de
# baixo custo: cenas que passam cobertura/paridade na 1a (sem retry) seguem; as que falham caem p/ o
# caminho interativo (streaming, com retry/escalonamento). Quem faz fitting (verify) continua sendo cada
# cena no run_scene. Determinismo da montagem do request isolado em _translate_params (testavel sem rede).

def _coverage_note(missing, bad_par) -> str:
    """Nota CORRETIVA p/ a re-rodada: quais offsets faltam (incluir TODOS) e quais tem paridade de `\\n`
    errada (casar EXATO). Vazia se nada a corrigir. Mesma redacao da retry interativa (_api_translate) —
    e o que faz a cena de narracao CONVERGIR no batch em vez de cair pro interativo full-price."""
    if not missing and not bad_par:
        return ""
    note = "\n\n## CORRECAO NECESSARIA (gere a cena COMPLETA de novo; vamos MESCLAR com o anterior)\n"
    if missing:
        note += f"- Faltam estes offsets — INCLUA todos: {sorted(missing)[:40]}\n"
    if bad_par:
        note += ("- Estes offsets tem nº de quebras `\\n` DIFERENTE da fonte — case EXATO (mesma "
                 f"quantidade e posicao do token): {sorted(bad_par)[:30]}\n")
    return note


def _translate_params(pack, model, note=""):
    """Params de UMA requisicao de traducao (compartilhado por batch). Aplica dedup; retorna
    (params|None, reuse, novel). params=None quando a cena e 100% reaproveitada da TM (sem chamada).
    `note`: feedback corretivo (ver _coverage_note) anexado ao prompt nas re-rodadas do batch."""
    reuse = _select_reuse(pack, enabled=True)
    reuse.update(_label_passthrough(pack))            # rotulo de engine: passthrough (fora do lote do LLM)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    if not novel:
        return None, reuse, novel
    system = [{"type": "text", "text": _carta_text(), "cache_control": {"type": "ephemeral"}}]
    red = dict(pack); red["lines"] = novel; red["n_lines"] = len(novel)
    base_user = context_pack.render_prompt(red, carta="") + _NL_RULE + note
    # Haiku 4.5 / Sonnet 4.5 NAO aceitam output_config.effort (400) — igual ao _api_translate, OMITE o
    # effort nesses modelos. BUG MEDIDO (cap.15): o batch sempre mandava effort -> todo request do tier
    # cheap (Haiku) dava 400 -> as linhas single-line nunca voltavam (MISSING) -> coverage_failed.
    out_cfg = {"format": {"type": "json_schema", "schema": _TRANSLATION_SCHEMA}}
    if not _no_effort_model(model):
        out_cfg["effort"] = EFFORT_TRANSLATE
    params = {
        "model": model, "max_tokens": MAX_OUTPUT_TOKENS, "system": system,
        "messages": [{"role": "user", "content": base_user}],
        "thinking": {"type": "disabled"},
        "output_config": out_cfg,
    }
    return params, reuse, novel


def _write_translations(root, scene, data):
    out = paths.translations(root, scene, context_pack.scene_id_of(scene))
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _tier_of(source: str) -> str:
    """Tier de modelo por COMPLEXIDADE: 'main' (Sonnet) p/ linha com token de quebra (multi-linha);
    'cheap' (Haiku) p/ single-line. Driblar a fraqueza medida do Haiku (paridade de \\n so falha onde
    HA \\n)."""
    return "main" if context_pack.TOKEN in (source or "") else "cheap"


def _parse_batch_lines(pack, text):
    """Parseia UMA resposta de batch -> {offset: entry} so das linhas NOVAS validas (parity-fitted).
    Tolera incompletude (devolve o que veio); {} se o JSON quebrar. Usado p/ ACUMULAR entre rodadas."""
    reuse = _select_reuse(pack, enabled=True)
    novel_offsets = {r["offset"] for r in pack["lines"]} - set(reuse)
    srcmap = {r["offset"]: r.get("source", "") for r in pack["lines"]}
    try:
        parsed = _to_map(json.loads(text))
    except Exception:
        return {}
    out = {}
    for off, v in parsed.get("lines", {}).items():
        if off in novel_offsets and isinstance(v, dict):
            v["t"] = _parity_fit(srcmap.get(off, ""), v.get("t", ""))
            if _is_blowup(srcmap.get(off, ""), v["t"]):
                continue                                 # lixo patologico -> descarta (re-roda / missing)
            out[off] = v
    return out


def _merge_best_parity(dest, new, srcmap):
    """Mescla `new` em `dest` ACUMULANDO entre rodadas, preferindo paridade de `\\n` correta — igual ao
    _api_translate (interativo). NUNCA troca uma linha de paridade BOA por uma RUIM: assim uma re-rodada
    que regride uma linha ja boa nao desfaz o ganho (o `dict.update` cego perdia isso e a cena nao
    convergia). Mesma paridade -> usa a mais nova (consistente com o comportamento anterior)."""
    tok = context_pack.TOKEN
    for off, v in new.items():
        src = srcmap.get(off, "")
        good = v.get("t", "").count(tok) == src.count(tok)
        old = dest.get(off)
        if old is None:
            dest[off] = v
            continue
        old_good = old.get("t", "").count(tok) == src.count(tok)
        if good or not old_good:        # melhora a paridade, ou ambas ruins -> aceita a nova
            dest[off] = v
    return dest


def _batch_coverage(pack, merged):
    """(missing, bad_parity) das linhas NOVAS, dado o acumulado `merged` (offset->entry)."""
    tok = context_pack.TOKEN
    reuse = _select_reuse(pack, enabled=True)
    novel = [r for r in pack["lines"] if r["offset"] not in reuse]
    srcmap = {r["offset"]: r.get("source", "") for r in novel}
    missing = [r["offset"] for r in novel if r["offset"] not in merged]
    bad_par = [o for o in srcmap if o in merged
               and merged[o].get("t", "").count(tok) != srcmap[o].count(tok)]
    return missing, bad_par


# _await_batch -> llm_client.py (importado acima).


def batch_translate(root, scenes, *, model=None, poll_seconds=30, max_wait_seconds=24 * 3600,
                    max_rounds=3, tiered=True):
    """Traduz VARIAS cenas em batches (50% off), ACUMULANDO cobertura entre RODADAS. O batch e 1-tiro
    por requisicao (sem retry interno) -> cenas grandes as vezes dropam linhas. Em vez de cair pro
    caminho interativo a preco CHEIO, cada rodada re-batcha SO o que falta (cena inteira na 1a; depois
    apenas os offsets faltantes/de paridade ruim) e mescla — convergindo a -50%.

    TIERING (tiered=True, default): por cena/rodada, as linhas SEM token de quebra vao num request Haiku
    (-67%/linha) e as COM `\\n` num request Sonnet (confiabilidade de paridade). custom_id = 'scene__tier'
    (separador `__` — a Batch API rejeita custom_id fora de ^[a-zA-Z0-9_-]{1,64}$, ex.: '@' dá 400).

    Grava translations_<scene_id>.json das cenas completas; retorna {scene: status} em
    {all_reused, written, coverage_failed, errored:<tipo>, timeout}. Cenas != (written|all_reused) ainda
    caem p/ o caminho interativo (run_scene). NAO roda build_plan/verify (isso e por-cena)."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    root = Path(root)
    m = model or MODEL_TRANSLATE
    cheap = MODEL_TRANSLATE_CHEAP if (tiered and MODEL_TRANSLATE_CHEAP) else m
    tiers = (("cheap", cheap), ("main", m))            # roteamento por complexidade
    client = _client()
    packs, merged, status = {}, {}, {}
    pending = []
    for scene in scenes:
        pack = context_pack.write_pack(root, scene)
        packs[scene] = pack
        reuse = _select_reuse(pack, enabled=True)
        merged[scene] = dict(reuse)                      # reuso pre-preenche o acumulado
        # RESUME (idempotente): se ja existe translations_<scene_id>.json, aproveita -> nao re-batcha o que ja
        # foi pago. Cobertura parcial: re-batcha SO o que falta (ver rodadas). Cobertura completa: pula.
        existing = paths.translations(root, scene, pack['scene_id'])
        if existing.is_file():
            try:
                ex = json.loads(existing.read_text(encoding="utf-8")).get("lines", {})
                merged[scene].update({o: v for o, v in ex.items() if isinstance(v, dict)})
            except Exception:
                pass
        miss, badpar = _batch_coverage(pack, merged[scene])
        if not miss and not badpar:
            _write_translations(root, scene, {"lines": merged[scene]})
            status[scene] = "all_reused" if all(r["offset"] in reuse for r in pack["lines"]) else "written"
        else:
            pending.append(scene)

    for rnd in range(max_rounds):
        if not pending:
            break
        reqs, req_model = [], {}                          # req_model[custom_id] = modelo (p/ custo no ledger)
        for scene in pending:
            miss, badpar = _batch_coverage(packs[scene], merged[scene])
            want = (set(miss) | set(badpar)) if rnd > 0 else None   # rnd0: tudo; depois: so o que falta
            for tier, tmodel in tiers:                    # split por COMPLEXIDADE (cheap=Haiku / main=Sonnet)
                tier_lines = [r for r in packs[scene]["lines"]
                              if _tier_of(r.get("source", "")) == tier
                              and (want is None or r["offset"] in want)]
                # CHUNKING: cada request = ate _BATCH_CHUNK linhas (o batch trunca saidas longas). Cada
                # chunk e auto-contido (render so das suas linhas) e volta completo; a cobertura acumula
                # entre chunks E rodadas via _merge_best_parity.
                for ci in range(0, len(tier_lines), _BATCH_CHUNK):
                    chunk = tier_lines[ci:ci + _BATCH_CHUNK]
                    sub = dict(packs[scene]); sub["lines"] = chunk
                    # FEEDBACK CORRETIVO na re-rodada (rnd>0): nota com os offsets faltando/paridade-errada
                    # DESTE chunk, como o _api_translate faz.
                    note = ""
                    if rnd > 0:
                        coffs = {r["offset"] for r in chunk}
                        note = _coverage_note([o for o in miss if o in coffs],
                                              [o for o in badpar if o in coffs])
                    params, _reuse, _novel = _translate_params(sub, tmodel, note=note)
                    if params is None:                    # tudo reuso nesse chunk -> sem request
                        continue
                    # custom_id 'scene__tier__chunk' — ^[a-zA-Z0-9_-]{1,64}$; split('__',1)[0] = scene
                    cid = f"{scene}__{tier}__{ci // _BATCH_CHUNK}"
                    req_model[cid] = tmodel
                    reqs.append(Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**params)))
        if not reqs:
            break
        batch = _with_backoff(lambda: client.messages.batches.create(requests=reqs))  # noqa: B023  (_with_backoff invoca na hora)
        if not _await_batch(client, batch.id, poll_seconds, max_wait_seconds):
            for scene in pending:
                status.setdefault(scene, "timeout")
            return status
        # materializa os resultados DENTRO do backoff (a iteracao faz I/O lazy -> timeout no meio)
        results = _with_backoff(lambda: list(client.messages.batches.results(batch.id)))  # noqa: B023  (_with_backoff invoca na hora)
        for result in results:
            cid = result.custom_id
            scene = cid.split("__", 1)[0]
            if getattr(result.result, "type", None) != "succeeded":
                continue                                  # tier falho -> cobertura decide (re-batch/fallback)
            msg = result.result.message
            log_api_call(root, scene, "translate", req_model.get(cid, m), _usage_of(msg), batch=True)
            srcmap = {r["offset"]: r.get("source", "") for r in packs[scene]["lines"]}
            _merge_best_parity(merged[scene], _parse_batch_lines(packs[scene], _text_of(msg)), srcmap)
        still = []
        for scene in pending:
            if str(status.get(scene, "")).startswith("errored"):
                continue                                 # erro duro -> nao re-tenta; cai p/ interativo
            miss, badpar = _batch_coverage(packs[scene], merged[scene])
            if not miss and not badpar:
                _write_translations(root, scene, {"lines": merged[scene]})
                status[scene] = "written"
            else:
                still.append(scene)
        pending = still

    for scene in pending:
        status.setdefault(scene, "coverage_failed")      # nao convergiu apos as rodadas -> interativo
    return status


# _BACK_SCHEMA / _back_params / _api_back_translate / high_risk_lines / sample_low_risk_lines /
# back_translate_candidates / batch_back_translate -> back_translate.py (importados acima).


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Interface de modelo do harness (translate).")
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("--backend", default="api", choices=["in-session", "api", "ollama"])
    ap.add_argument("--model", default=None)
    a = ap.parse_args()
    r = translate(a.project, a.scene, backend=a.backend, model=a.model)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
